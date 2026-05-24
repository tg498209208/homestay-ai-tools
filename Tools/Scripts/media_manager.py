#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏡 伴山栖湖 · 素材智能分类 & 批量修图工具
-----------------------------------------
功能：
  1. 扫描 Assets/Raw_Materials/ 中的原始素材
  2. 用 Claude 视觉能力识别图片内容，自动分类到业务文件夹
  3. 用 Pillow 对分类后的图片批量裁剪为 3:4 比例 + 色彩优化

版本：v1.0.0
用法：python3 Tools/Scripts/media_manager.py [--dry-run] [--skip-ai] [--only-enhance]
"""

import os
import re
import sys
import shutil
import base64
import argparse
import datetime
from pathlib import Path
from typing import Optional

import anthropic
from PIL import Image, ImageEnhance

# ==============================
# 路径常量
# ==============================

PROJECT_ROOT  = Path(__file__).resolve().parent.parent.parent
RAW_DIR       = PROJECT_ROOT / "Assets" / "Raw_Materials"
IMAGES_DIR    = PROJECT_ROOT / "Assets" / "Images"
OUTPUT_DIR    = PROJECT_ROOT / "Output" / "Enhanced"

# 分类目标目录（文件夹名 → 路径）
CATEGORY_DIRS = {
    "窑烤面包": IMAGES_DIR / "窑烤面包",
    "湖景房":   IMAGES_DIR / "湖景房",
    "草坪婚礼": IMAGES_DIR / "草坪婚礼",
    "围炉煮茶": IMAGES_DIR / "围炉煮茶",
    "湖畔落日": IMAGES_DIR / "湖畔落日",
    "其他":     IMAGES_DIR / "其他",
}

SUPPORTED_IMG = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic"}
SUPPORTED_VID = {".mp4", ".mov", ".avi", ".m4v"}

# ==============================
# Claude 客户端
# ==============================

claude = anthropic.Anthropic()


# ==============================
# 1. 图片扫描器
# ==============================

class RawScanner:
    """扫描 Raw_Materials 目录，返回待处理素材列表"""

    def __init__(self, raw_dir: Path = RAW_DIR):
        self.raw_dir = raw_dir

    def scan(self) -> tuple[list[Path], list[Path]]:
        """返回 (图片列表, 视频列表)"""
        if not self.raw_dir.exists():
            self.raw_dir.mkdir(parents=True)
            print(f"📁 已创建原始素材目录：{self.raw_dir}")
            return [], []

        images, videos = [], []
        for p in sorted(self.raw_dir.rglob("*")):
            if p.is_file():
                ext = p.suffix.lower()
                if ext in SUPPORTED_IMG:
                    images.append(p)
                elif ext in SUPPORTED_VID:
                    videos.append(p)

        print(f"📸 扫描到图片：{len(images)} 张　🎬 视频：{len(videos)} 个")
        return images, videos


# ==============================
# 2. AI 场景分类器
# ==============================

class AIClassifier:
    """
    用 Claude 视觉能力识别图片内容，返回所属业务场景。
    支持降级：当 AI 不可用时，自动用文件名关键词匹配。
    """

    # 文件名关键词 → 分类（降级用）
    FILENAME_RULES = {
        "窑烤面包": ["面包", "bread", "窑", "烘焙", "欧包", "肉桂", "佛卡夏"],
        "湖景房":   ["客房", "room", "湖景", "大床", "落地窗", "室内", "床"],
        "草坪婚礼": ["婚礼", "wedding", "草坪", "婚纱", "仪式", "花艺"],
        "围炉煮茶": ["围炉", "煮茶", "炭火", "炉", "茶", "烤红薯"],
        "湖畔落日": ["湖", "lake", "日落", "sunset", "栈道", "水", "风景"],
    }

    SYSTEM_PROMPT = """你是伴山栖湖民宿的图片分类助手。
民宿业务分为5类场景：窑烤面包、湖景房、草坪婚礼、围炉煮茶、湖畔落日。
如果图片不属于以上任何一类，返回"其他"。
只返回分类名称，不要任何解释。"""

    def classify_by_ai(self, image_path: Path) -> str:
        """调用 Claude 视觉识别图片场景"""
        try:
            # HEIC 格式先转换
            img_bytes, mime = self._load_image_bytes(image_path)
            if img_bytes is None:
                return self.classify_by_filename(image_path.stem)

            b64 = base64.standard_b64encode(img_bytes).decode("utf-8")

            message = claude.messages.create(
                model="claude-opus-4-5",
                max_tokens=20,
                system=self.SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime,
                                "data": b64,
                            },
                        },
                        {"type": "text", "text": "这张图片属于哪个场景？"},
                    ],
                }],
            )
            result = next(
                (b.text.strip() for b in message.content if hasattr(b, "text")),
                ""
            )
            # 校验返回值合法性
            if result in CATEGORY_DIRS:
                return result
            # 模糊匹配
            for cat in CATEGORY_DIRS:
                if cat in result:
                    return cat
            return "其他"

        except Exception as e:
            print(f"    ⚠️  AI 识别失败（{e.__class__.__name__}），降级用文件名匹配")
            return self.classify_by_filename(image_path.stem)

    def classify_by_filename(self, filename: str) -> str:
        """降级方案：根据文件名关键词分类"""
        name_lower = filename.lower()
        for category, keywords in self.FILENAME_RULES.items():
            if any(kw in name_lower or kw in filename for kw in keywords):
                return category
        return "其他"

    def _load_image_bytes(self, path: Path) -> tuple[Optional[bytes], str]:
        """读取图片字节，HEIC 转为 JPEG"""
        try:
            ext = path.suffix.lower()
            if ext == ".heic":
                # HEIC → JPEG via Pillow（需要 pillow-heif 插件，降级处理）
                try:
                    import pillow_heif
                    pillow_heif.register_heif_opener()
                    img = Image.open(path).convert("RGB")
                    from io import BytesIO
                    buf = BytesIO()
                    img.save(buf, format="JPEG", quality=85)
                    return buf.getvalue(), "image/jpeg"
                except ImportError:
                    print(f"    💡 提示：安装 pillow-heif 可支持 HEIC 格式识别")
                    return None, ""
            else:
                mime_map = {
                    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                    ".png": "image/png", ".webp": "image/webp",
                    ".bmp": "image/jpeg",
                }
                mime = mime_map.get(ext, "image/jpeg")
                # 压缩大图防止 token 超限（限制最长边 1200px）
                img = Image.open(path)
                img = self._downscale(img, max_size=1200)
                from io import BytesIO
                buf = BytesIO()
                fmt = "PNG" if ext == ".png" else "JPEG"
                img.convert("RGB").save(buf, format=fmt, quality=85)
                return buf.getvalue(), mime
        except Exception as e:
            print(f"    ⚠️  图片读取失败：{e}")
            return None, ""

    @staticmethod
    def _downscale(img: Image.Image, max_size: int = 1200) -> Image.Image:
        """等比缩小图片，最长边不超过 max_size"""
        w, h = img.size
        if max(w, h) <= max_size:
            return img
        ratio = max_size / max(w, h)
        return img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)


# ==============================
# 3. 批量修图引擎
# ==============================

class ImageEnhancer:
    """
    小红书专用图片预处理：
    - 裁剪为 3:4 竖版比例（小红书最优排版）
    - 微调对比度 + 饱和度（通透网红感）
    """

    TARGET_RATIO = (3, 4)    # 宽:高

    # 调节参数（1.0 = 原始，可根据司令官偏好微调）
    CONTRAST    = 1.10       # 对比度 +10%
    SATURATION  = 1.15       # 饱和度 +15%
    SHARPNESS   = 1.05       # 锐度 +5%（提升清晰度）
    BRIGHTNESS  = 1.02       # 亮度 +2%（略微提亮）

    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process(self, image_path: Path, category: str) -> Optional[Path]:
        """对单张图片执行裁剪 + 色彩优化，返回输出路径"""
        try:
            img = Image.open(image_path).convert("RGB")

            # Step 1: 裁剪为 3:4
            img = self._crop_to_ratio(img)

            # Step 2: 色彩优化
            img = self._enhance_colors(img)

            # Step 3: 保存
            out_dir = self.output_dir / category
            out_dir.mkdir(parents=True, exist_ok=True)
            stem = image_path.stem
            out_path = out_dir / f"{stem}_enhanced.jpg"
            img.save(out_path, format="JPEG", quality=92, optimize=True)
            return out_path

        except Exception as e:
            print(f"    ❌ 修图失败：{image_path.name} — {e}")
            return None

    def _crop_to_ratio(self, img: Image.Image) -> Image.Image:
        """
        智能居中裁剪为 3:4 比例。
        若原图已经是 3:4 则直接返回。
        """
        w, h = img.size
        target_w_ratio, target_h_ratio = self.TARGET_RATIO

        # 计算目标尺寸（保留最大面积）
        if w / h > target_w_ratio / target_h_ratio:
            # 图片太宽 → 以高为基准，裁左右
            new_w = int(h * target_w_ratio / target_h_ratio)
            new_h = h
        else:
            # 图片太高 → 以宽为基准，裁上下（保留中间部分）
            new_w = w
            new_h = int(w * target_h_ratio / target_w_ratio)

        # 居中裁剪
        left   = (w - new_w) // 2
        top    = int((h - new_h) * 0.35)  # 偏上裁剪，保留天空/主体
        right  = left + new_w
        bottom = top + new_h
        return img.crop((left, top, right, bottom))

    def _enhance_colors(self, img: Image.Image) -> Image.Image:
        """微调对比度、饱和度、锐度、亮度"""
        img = ImageEnhance.Contrast(img).enhance(self.CONTRAST)
        img = ImageEnhance.Color(img).enhance(self.SATURATION)
        img = ImageEnhance.Sharpness(img).enhance(self.SHARPNESS)
        img = ImageEnhance.Brightness(img).enhance(self.BRIGHTNESS)
        return img


# ==============================
# 4. 分类归档器
# ==============================

class FileSorter:
    """将图片复制/移动到对应业务文件夹"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        for d in CATEGORY_DIRS.values():
            d.mkdir(parents=True, exist_ok=True)

    def sort(self, image_path: Path, category: str) -> Path:
        """把图片复制到分类目录，返回目标路径"""
        dest_dir  = CATEGORY_DIRS.get(category, CATEGORY_DIRS["其他"])
        dest_path = dest_dir / image_path.name

        # 文件名冲突处理
        if dest_path.exists():
            stem = image_path.stem
            suffix = image_path.suffix
            ts = datetime.datetime.now().strftime("%H%M%S")
            dest_path = dest_dir / f"{stem}_{ts}{suffix}"

        if not self.dry_run:
            shutil.copy2(image_path, dest_path)
        return dest_path


# ==============================
# 5. 主流程
# ==============================

def parse_args():
    parser = argparse.ArgumentParser(description="伴山栖湖素材分类修图工具")
    parser.add_argument("--dry-run",      action="store_true", help="演习模式，不实际移动或修改文件")
    parser.add_argument("--skip-ai",      action="store_true", help="跳过 AI 识别，全部用文件名规则分类")
    parser.add_argument("--only-enhance", action="store_true", help="跳过分类，只对 Assets/Images/ 现有图片做修图")
    parser.add_argument("--raw-dir",      type=str,            help="指定原始素材目录（默认 Assets/Raw_Materials/）")
    return parser.parse_args()


def run_classify_and_sort(args):
    """主流程：扫描 → 分类 → 归档 → 修图"""
    raw_dir = Path(args.raw_dir) if args.raw_dir else RAW_DIR

    scanner    = RawScanner(raw_dir)
    classifier = AIClassifier()
    enhancer   = ImageEnhancer()
    sorter     = FileSorter(dry_run=args.dry_run)

    images, videos = scanner.scan()

    if videos:
        print(f"\n🎬 视频文件（{len(videos)} 个）：当前版本仅记录，暂不处理")
        for v in videos:
            print(f"   - {v.name}")

    if not images:
        print("\n📭 Raw_Materials 目录暂无图片。")
        print(f"   → 请将原始素材放入：{raw_dir}")
        return

    print(f"\n{'🔍 演习模式（不修改文件）' if args.dry_run else '🚀 开始处理'}：共 {len(images)} 张图片\n")

    stats = {cat: 0 for cat in CATEGORY_DIRS}
    enhanced_count = 0

    for i, img_path in enumerate(images, 1):
        print(f"[{i:>3}/{len(images)}] {img_path.name}")

        # 分类
        if args.skip_ai:
            category = classifier.classify_by_filename(img_path.stem)
            print(f"       📂 文件名规则 → {category}")
        else:
            print(f"       🤖 AI 识别中…", end=" ", flush=True)
            category = classifier.classify_by_ai(img_path)
            print(f"→ {category}")

        # 归档
        dest = sorter.sort(img_path, category)
        stats[category] += 1
        if not args.dry_run:
            print(f"       ✅ 已复制到 Assets/Images/{category}/")

        # 修图
        if not args.dry_run:
            print(f"       🎨 修图中（3:4裁剪 + 色彩优化）…", end=" ", flush=True)
            out = enhancer.process(dest, category)
            if out:
                enhanced_count += 1
                print(f"✅ {out.name}")
            else:
                print("跳过")

    # 汇总报告
    print("\n" + "=" * 50)
    print("📊 分类汇总：")
    for cat, count in stats.items():
        if count > 0:
            bar = "█" * count
            print(f"   {cat:<8} {bar} {count} 张")
    print(f"\n🎨 修图完成：{enhanced_count} 张 → Output/Enhanced/")
    if args.dry_run:
        print("⚠️  演习模式：以上为预览结果，未实际修改任何文件")
    print("=" * 50)


def run_only_enhance():
    """仅对 Assets/Images/ 下已有图片做修图"""
    enhancer = ImageEnhancer()
    count = 0
    for category in CATEGORY_DIRS:
        cat_dir = CATEGORY_DIRS[category]
        if not cat_dir.exists():
            continue
        imgs = [p for p in cat_dir.iterdir()
                if p.suffix.lower() in SUPPORTED_IMG and "_enhanced" not in p.stem]
        for img_path in imgs:
            print(f"🎨 {category}/{img_path.name}", end=" → ", flush=True)
            out = enhancer.process(img_path, category)
            if out:
                print(f"✅ {out.name}")
                count += 1
            else:
                print("❌ 失败")
    print(f"\n✅ 共修图 {count} 张，输出至 Output/Enhanced/")


def main():
    args = parse_args()

    print("=" * 55)
    print("🏡 伴山栖湖 · 素材分类修图工具 v1.0.0")
    if args.dry_run:
        print("   ⚠️  演习模式（--dry-run）")
    if args.skip_ai:
        print("   ⚡ 极速模式（--skip-ai，仅文件名分类）")
    print("=" * 55 + "\n")

    if args.only_enhance:
        run_only_enhance()
    else:
        run_classify_and_sort(args)


if __name__ == "__main__":
    main()
