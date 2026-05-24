#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏡 伴山栖湖 · 自动化营销文案生成器
-----------------------------------------
功能：读取 Assets/Images/ 中的图片，根据场景分类自动匹配小红书文案模板，
      生成可直接发布或二次编辑的营销内容。

当前版本：v0.1.0 — 基础框架
目标：为后续接入 AI 视觉识别（CLIP/LLaVA）和自动化发布管线预留接口。
"""

import os
import json
import random
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ==============================
# 项目路径常量
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_IMAGES = PROJECT_ROOT / "Assets" / "Images"
DOCS_MARKETING = PROJECT_ROOT / "Docs" / "Marketing"
TEMPLATES_FILE = DOCS_MARKETING / "Xiaohongshu_Templates.md"
OUTPUT_DIR = PROJECT_ROOT / "Output" / "Generated"

# ==============================
# 场景 → 模板映射
# ==============================

SCENE_TEMPLATE_MAP = {
    "weilu_tea": {
        "name": "围炉煮茶",
        "template_id": "template_01",
        "keywords": ["围炉", "煮茶", "炭火", "烤红薯", "冬日", "茶具", "炉子"],
        "season": ["秋", "冬"],
    },
    "kilo_bread": {
        "name": "窑烤面包",
        "template_id": "template_02",
        "keywords": ["面包", "窑烤", "烘焙", "欧包", "面粉", "柴火", "烤箱"],
        "season": ["春", "夏", "秋", "冬"],
    },
    "lawn_wedding": {
        "name": "草坪婚礼",
        "template_id": "template_03",
        "keywords": ["婚礼", "草坪", "婚纱", "仪式", "花艺", "拱门", "戒指"],
        "season": ["春", "夏", "秋"],
    },
    "room_view": {
        "name": "客房景观",
        "template_id": "template_01",  # 复用围炉煮茶模板（住宿部分）
        "keywords": ["客房", "落地窗", "大床", "湖景", "室内", "床品"],
        "season": ["春", "夏", "秋", "冬"],
    },
}


@dataclass
class MarketingPost:
    """一篇营销帖子的数据结构"""

    title: str
    body: str
    tags: list[str]
    scene: str
    image_paths: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


class ImageScanner:
    """
    图片扫描器：遍历 Assets/Images/ 获取待处理图片列表。

    TODO:
    - 支持子目录分类（如 Images/围炉煮茶/、Images/婚礼/）
    - 调用 CLIP/LLaVA 进行视觉内容识别
    - 自动打标签
    """

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".bmp"}

    def __init__(self, image_dir: Optional[Path] = None):
        self.image_dir = image_dir or ASSETS_IMAGES

    def scan(self) -> list[Path]:
        """扫描图片目录，返回所有图片文件路径列表"""
        if not self.image_dir.exists():
            print(f"⚠️  图片目录不存在，正在创建：{self.image_dir}")
            self.image_dir.mkdir(parents=True, exist_ok=True)
            return []

        images = sorted(
            p for p in self.image_dir.rglob("*")
            if p.suffix.lower() in self.SUPPORTED_FORMATS
        )
        print(f"📸 扫描到 {len(images)} 张图片")
        return images

    def group_by_folder(self, images: list[Path]) -> dict[str, list[Path]]:
        """按子目录分组图片，用于自动场景分类"""
        groups: dict[str, list[Path]] = {}
        for img in images:
            folder = img.parent.name if img.parent != self.image_dir else "_root"
            groups.setdefault(folder, []).append(img)
        return groups


class SceneClassifier:
    """
    场景分类器：根据图片内容（或文件夹名）判断适用的营销模板。

    当前 v0.1 基于文件夹名称做启发式匹配；
    未来 v0.2+ 将接入 AI 视觉模型做内容级识别。
    """

    def __init__(self, scene_map: Optional[dict] = None):
        self.scene_map = scene_map or SCENE_TEMPLATE_MAP

    def classify_by_folder_name(self, folder_name: str) -> str:
        """根据文件夹名推断场景类型"""
        name_lower = folder_name.lower()
        for scene_id, config in self.scene_map.items():
            for kw in config["keywords"]:
                if kw in name_lower:
                    return scene_id
        return "weilu_tea"  # 默认回退到围炉煮茶

    def classify_by_keywords(self, keywords: list[str]) -> str:
        """根据关键词列表匹配最佳场景（基于命中数）"""
        best_scene = "weilu_tea"
        best_score = 0
        for scene_id, config in self.scene_map.items():
            score = sum(1 for kw in keywords if kw in config["keywords"])
            if score > best_score:
                best_score = score
                best_scene = scene_id
        return best_scene

    def get_seasonal_scenes(self, month: Optional[int] = None) -> list[str]:
        """根据当前月份返回适合的季节性场景"""
        if month is None:
            month = datetime.datetime.now().month
        season_map = {1: "冬", 2: "冬", 3: "春", 4: "春", 5: "春",
                       6: "夏", 7: "夏", 8: "夏", 9: "秋", 10: "秋",
                       11: "秋", 12: "冬"}
        current_season = season_map[month]
        return [
            sid for sid, cfg in self.scene_map.items()
            if current_season in cfg["season"]
        ]


class TemplateEngine:
    """
    模板引擎：读取 Xiaohongshu_Templates.md 并渲染营销文案。

    当前 v0.1 使用硬编码模板（从模板库文件加载逻辑待实现）；
    未来可从 Markdown 文件热加载模板并支持 Jinja2 变量替换。
    """

    # 硬编码模板（后续改为从 Templates.md 解析加载）
    TEMPLATES = {
        "template_01": {
            "scene_name": "围炉煮茶+住宿",
            "titles": [
                "🔥 住进山水画里是什么体验？这间民宿给了我答案",
                "🍵 冬天最浪漫的事，就是在山里围炉煮茶｜伴山栖湖",
            ],
            "hashtags": [
                "伴山栖湖", "围炉煮茶", "山居民宿", "冬日治愈",
                "周末去哪儿", "小众民宿推荐", "逃离城市计划", "慢生活",
            ],
        },
        "template_02": {
            "scene_name": "窑烤面包",
            "titles": [
                "🍞 为了这口窑烤面包，我驱车200公里来了山里",
                "🤯 民宿老板是面包疯子吧？窑烤出来的也太好吃了！",
            ],
            "hashtags": [
                "窑烤面包", "手工面包", "碳水快乐", "民宿美食",
                "伴山栖湖", "宝藏面包店", "柴火面包", "烘焙控",
            ],
        },
        "template_03": {
            "scene_name": "草坪婚礼",
            "titles": [
                "💍 在山湖之间说'我愿意'｜伴山栖湖婚礼实录",
                "🌿 不想在酒店办婚礼？这间民宿满足了我所有幻想",
            ],
            "hashtags": [
                "草坪婚礼", "小众婚礼", "户外婚礼", "伴山栖湖",
                "备婚日记", "婚礼场地推荐", "山系婚礼", "目的地婚礼",
            ],
        },
    }

    def render_post(
        self,
        scene_id: str,
        image_count: int = 0,
        custom_vars: Optional[dict] = None,
    ) -> MarketingPost:
        """根据场景渲染一篇营销帖子"""
        config = self.scene_map.get(scene_id)
        template = self.TEMPLATES.get(
            config["template_id"] if config else "template_01",
            self.TEMPLATES["template_01"],
        )

        title = random.choice(template["titles"])
        tags = template["hashtags"].copy()
        scene_name = template["scene_name"]

        # 拼接正文（后续改为完整模板渲染）
        body_lines = [
            f"🏡 伴山栖湖 · {scene_name}体验",
            "",
            f"📍 地点：伴山栖湖民宿",
            f"📅 推荐季节：{'/'.join(config['season']) if config else '全年'}",
            f"🖼️ 配图数量：{image_count} 张" if image_count else "",
            "",
            "---",
            "",
            "💬 文案待 AI 生成…（当前为基础框架输出）",
            "",
            f"# {' #'.join(tags[:6])}",
        ]

        return MarketingPost(
            title=title,
            body="\n".join(line for line in body_lines if line != "" or image_count),
            tags=tags,
            scene=scene_name,
        )


class OutputWriter:
    """输出写入器：将生成的文案保存为 Markdown 文件"""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or OUTPUT_DIR

    def write(self, post: MarketingPost) -> Path:
        """将帖子写入 Markdown 文件"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"post_{post.scene}_{timestamp}.md"
        filepath = self.output_dir / filename

        content = [
            f"# {post.title}",
            "",
            f"**场景**: {post.scene}",
            f"**生成时间**: {post.generated_at}",
            f"**配图数量**: {len(post.image_paths)}",
            "",
            "---",
            "",
            post.body,
            "",
            "---",
            "",
            "## 📎 配图列表",
            "",
        ]
        for img in post.image_paths:
            content.append(f"- `{img}`")

        content.extend([
            "",
            "## 🏷️ 完整 Tag",
            "",
            " ".join(f"#{t}" for t in post.tags),
            "",
            "> 🤖 由 auto_marketer.py 自动生成 | 请人工审核后发布",
        ])

        filepath.write_text("\n".join(content), encoding="utf-8")
        print(f"✅ 文案已保存：{filepath}")
        return filepath


# ==============================
# 主流程
# ==============================

def main():
    """主入口：扫描图片 → 场景分类 → 渲染文案 → 输出文件"""
    print("=" * 50)
    print("🏡 伴山栖湖 · 自动化营销文案生成器 v0.1.0")
    print("=" * 50)
    print()

    # Step 1: 扫描图片
    scanner = ImageScanner()
    images = scanner.scan()

    if not images:
        print()
        print("📭 暂无图片，请将民宿实景图放入 Assets/Images/ 目录。")
        print("   支持子目录分类，例如：")
        print("   - Assets/Images/围炉煮茶/")
        print("   - Assets/Images/窑烤面包/")
        print("   - Assets/Images/草坪婚礼/")
        print()
        print("💡 提示：放入图片后重新运行此脚本即可自动分类生成。")
        return

    # Step 2: 按目录分组
    groups = scanner.group_by_folder(images)
    print(f"📂 检测到 {len(groups)} 个图片分组")

    # Step 3: 场景分类
    classifier = SceneClassifier()
    engine = TemplateEngine()
    writer = OutputWriter()

    # Step 4: 批量生成
    generated_count = 0
    for folder_name, img_list in groups.items():
        scene_id = classifier.classify_by_folder_name(folder_name)
        post = engine.render_post(
            scene_id=scene_id,
            image_count=len(img_list),
        )
        post.image_paths = [str(p.relative_to(PROJECT_ROOT)) for p in img_list]
        writer.write(post)
        generated_count += 1

    print()
    print(f"🎉 完成！共生成 {generated_count} 篇营销文案。")
    print(f"📁 输出目录：{OUTPUT_DIR}")
    print()
    print("⚠️  请在使用前人工审核文案内容并替换 [xxx] 占位符。")


if __name__ == "__main__":
    main()
