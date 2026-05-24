#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏡 伴山栖湖 · 自动化营销文案生成器
-----------------------------------------
功能：读取 Assets/Images/ 中的图片，根据场景分类自动匹配小红书文案模板，
      调用 Claude API 生成完整可用的营销文案，存入 Output/Generated/。

当前版本：v0.2.0 — 接入 Claude AI 生成完整文案
"""

import os
import json
import random
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

import anthropic

# ==============================
# 项目路径常量
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_IMAGES = PROJECT_ROOT / "Assets" / "Images"
DOCS_MARKETING = PROJECT_ROOT / "Docs" / "Marketing"
TEMPLATES_FILE = DOCS_MARKETING / "Xiaohongshu_Templates.md"
OUTPUT_DIR = PROJECT_ROOT / "Output" / "Generated"

# ==============================
# Claude 客户端
# ==============================

claude = anthropic.Anthropic()  # 自动读取环境变量 ANTHROPIC_API_KEY

# ==============================
# 场景配置
# ==============================

SCENE_CONFIG = {
    "weilu_tea": {
        "name": "围炉煮茶",
        "keywords": ["围炉", "煮茶", "炭火", "烤红薯", "冬日", "茶具", "炉子"],
        "season": ["秋", "冬"],
        "target_audience": "25-35岁周末出游族，向往慢生活，秋冬出行",
        "core_selling_points": [
            "炭火围炉，炉边烤红薯、橘子",
            "湖景山景落地窗大床房",
            "全屋地暖，五星床品",
            "民宿自制窑烤面包配茶",
            "夜晚安静，能听到落叶声",
        ],
        "hashtags": [
            "伴山栖湖", "围炉煮茶", "山居民宿", "冬日治愈",
            "周末去哪儿", "小众民宿推荐", "逃离城市计划", "秋冬旅行",
            "慢生活", "民宿打卡", "山水之间", "涪陵民宿",
        ],
    },
    "kiln_bread": {
        "name": "窑烤面包",
        "keywords": ["面包", "窑烤", "烘焙", "欧包", "面粉", "柴火", "烤箱"],
        "season": ["春", "夏", "秋", "冬"],
        "target_audience": "美食探店爱好者、烘焙控、碳水爱好者",
        "core_selling_points": [
            "民宿自建柴烧面包窑，300°C+明火直烤",
            "手工揉制面团，低温长时间发酵",
            "招牌窑烤欧包、肉桂卷、佛卡夏",
            "周末限定桂花酒酿面包",
            "住店客人早餐免费，可打包礼盒",
        ],
        "hashtags": [
            "窑烤面包", "手工面包", "碳水快乐", "民宿美食",
            "宝藏面包店", "伴山栖湖", "山间美食", "柴火面包",
            "周末探店", "烘焙控", "重庆美食", "涪陵探店",
        ],
    },
    "lawn_wedding": {
        "name": "草坪婚礼",
        "keywords": ["婚礼", "草坪", "婚纱", "仪式", "花艺", "拱门", "戒指"],
        "season": ["春", "夏", "秋"],
        "target_audience": "备婚女性24-32岁，寻求小众私密非酒店婚礼场地",
        "core_selling_points": [
            "面朝湖泊的天然草坪仪式区",
            "整栋包场，全程私密不围观",
            "一站式：场地+餐饮+住宿+布景",
            "露天长桌+串灯+篝火晚宴",
            "宠物友好，可带狗狗当花童",
        ],
        "hashtags": [
            "草坪婚礼", "小众婚礼", "户外婚礼", "伴山栖湖",
            "备婚日记", "婚礼场地推荐", "山系婚礼", "小型婚礼",
            "目的地婚礼", "婚礼灵感", "重庆婚礼", "涪陵婚礼",
        ],
    },
    "room_view": {
        "name": "客房景观",
        "keywords": ["客房", "落地窗", "大床", "湖景", "室内", "床品", "山景"],
        "season": ["春", "夏", "秋", "冬"],
        "target_audience": "追求高品质住宿体验的都市人，情侣、家庭",
        "core_selling_points": [
            "落地窗直面山湖，早上被阳光叫醒",
            "全屋地暖，冬季温暖如春",
            "五星级床品，躺下就不想起来",
            "11间湖景房，私密独栋体验",
            "湖边栈道日落打卡",
        ],
        "hashtags": [
            "湖景民宿", "落地窗", "伴山栖湖", "精品民宿",
            "周末度假", "山水民宿", "涪陵民宿", "重庆周边游",
            "情侣出行", "亲子民宿", "慢生活", "民宿推荐",
        ],
    },
}


# ==============================
# 数据类
# ==============================

@dataclass
class MarketingPost:
    """一篇营销帖子的完整数据"""
    title: str
    body: str
    tags: list[str]
    scene: str
    image_paths: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


# ==============================
# 图片扫描器
# ==============================

class ImageScanner:
    """遍历 Assets/Images/ 获取待处理图片列表"""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".bmp"}

    def __init__(self, image_dir: Optional[Path] = None):
        self.image_dir = image_dir or ASSETS_IMAGES

    def scan(self) -> list[Path]:
        """扫描图片目录，返回所有图片路径"""
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
        """按子目录分组图片"""
        groups: dict[str, list[Path]] = {}
        for img in images:
            folder = img.parent.name if img.parent != self.image_dir else "_root"
            groups.setdefault(folder, []).append(img)
        return groups


# ==============================
# 场景分类器
# ==============================

class SceneClassifier:
    """根据文件夹名或关键词判断适用场景"""

    def __init__(self):
        self.scene_map = SCENE_CONFIG

    def classify_by_folder_name(self, folder_name: str) -> str:
        """根据文件夹名推断场景"""
        name_lower = folder_name.lower()
        for scene_id, config in self.scene_map.items():
            for kw in config["keywords"]:
                if kw in name_lower or kw in folder_name:
                    return scene_id
        return "room_view"  # 默认回退到客房景观

    def classify_by_keywords(self, keywords: list[str]) -> str:
        """根据关键词列表匹配最佳场景"""
        best_scene = "room_view"
        best_score = 0
        for scene_id, config in self.scene_map.items():
            score = sum(1 for kw in keywords if kw in config["keywords"])
            if score > best_score:
                best_score = score
                best_scene = scene_id
        return best_scene

    def get_seasonal_scenes(self, month: Optional[int] = None) -> list[str]:
        """根据当前月份返回适合的场景"""
        if month is None:
            month = datetime.datetime.now().month
        season_map = {
            1: "冬", 2: "冬", 3: "春", 4: "春", 5: "春",
            6: "夏", 7: "夏", 8: "夏", 9: "秋", 10: "秋",
            11: "秋", 12: "冬",
        }
        current_season = season_map[month]
        return [
            sid for sid, cfg in self.scene_map.items()
            if current_season in cfg["season"]
        ]


# ==============================
# Claude 文案生成引擎
# ==============================

class ClaudeContentEngine:
    """
    调用 Claude API 生成完整小红书营销文案。
    """

    def __init__(self):
        self.client = claude

    def _load_reference_template(self, scene_id: str) -> str:
        """从 Xiaohongshu_Templates.md 加载参考模板文本"""
        if not TEMPLATES_FILE.exists():
            return ""
        content = TEMPLATES_FILE.read_text(encoding="utf-8")
        # 按模板标题切分，提取对应场景的参考文本
        scene_name = SCENE_CONFIG.get(scene_id, {}).get("name", "")
        sections = content.split("## ")
        for section in sections:
            if scene_name in section or (scene_id == "kiln_bread" and "窑烤面包" in section):
                return "## " + section[:1500]  # 取前1500字符作参考
        return sections[1] if len(sections) > 1 else ""  # 默认取第一个模板

    def generate(
        self,
        scene_id: str,
        image_count: int = 0,
        image_descriptions: Optional[list[str]] = None,
    ) -> tuple[str, str]:
        """
        调用 Claude 生成（标题, 正文）。
        返回: (title, body)
        """
        config = SCENE_CONFIG.get(scene_id, SCENE_CONFIG["room_view"])
        reference = self._load_reference_template(scene_id)
        current_month = datetime.datetime.now().month
        season_map = {1:"冬",2:"冬",3:"春",4:"春",5:"春",
                      6:"夏",7:"夏",8:"夏",9:"秋",10:"秋",11:"秋",12:"冬"}
        current_season = season_map[current_month]

        image_info = ""
        if image_descriptions:
            image_info = f"\n\n图片描述（共{image_count}张）：\n" + "\n".join(
                f"- {d}" for d in image_descriptions
            )
        elif image_count > 0:
            image_info = f"\n\n本次配图：{image_count} 张实景照片（场景：{config['name']}）"

        prompt = f"""你是伴山栖湖民宿的小红书运营专家，请为以下场景生成一篇爆款小红书营销笔记。

## 场景信息
- 场景：{config['name']}
- 目标用户：{config['target_audience']}
- 当前季节：{current_season}季
- 核心卖点：
{chr(10).join(f'  • {p}' for p in config['core_selling_points'])}
{image_info}

## 参考风格（已有模板，供参考语气和结构）
{reference}

## 输出要求
请严格按以下 JSON 格式输出，不要有任何多余文字：

{{
  "title": "（一行标题，含emoji，35字以内，要有钩子感）",
  "body": "（完整正文，小红书风格：多分段、多emoji、有故事感、有痛点、有场景感，300-500字）"
}}

要求：
1. 标题要让人想点击，用疑问句/反差/数字/场景带入
2. 正文开头要有代入感的故事或提问，勾住读者
3. 卖点要具体，用感官描写（视觉/嗅觉/味觉/触觉）
4. 结尾要有互动引导（问问题或邀请评论）
5. 语气真实自然，像真实用户分享，不像广告
6. 只输出 JSON，不要说其他话"""

        print(f"  🤖 Claude 正在生成「{config['name']}」文案…")

        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        # 跳过 ThinkingBlock，找到第一个 TextBlock
        raw = next(
            (block.text for block in message.content if hasattr(block, "text")),
            ""
        ).strip()

        # 解析 JSON 输出
        try:
            # 去掉可能的 markdown 代码块
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            return data.get("title", ""), data.get("body", "")
        except json.JSONDecodeError:
            # 容错：直接返回原文
            print("  ⚠️  JSON 解析失败，返回原始输出")
            lines = raw.split("\n")
            title = lines[0].strip().lstrip('"').rstrip('"') if lines else ""
            body = "\n".join(lines[1:]).strip()
            return title, body


# ==============================
# 输出写入器
# ==============================

class OutputWriter:
    """将生成的文案保存为 Markdown 文件"""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or OUTPUT_DIR

    def write(self, post: MarketingPost) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_scene = post.scene.replace("/", "_")
        filename = f"post_{safe_scene}_{timestamp}.md"
        filepath = self.output_dir / filename

        content = [
            f"# {post.title}",
            "",
            f"> **场景**：{post.scene}　**生成时间**：{post.generated_at[:19]}　**配图**：{len(post.image_paths)} 张",
            "",
            "---",
            "",
            post.body,
            "",
            "---",
            "",
            "## 🏷️ Hashtag",
            "",
            " ".join(f"#{t}" for t in post.tags),
            "",
        ]

        if post.image_paths:
            content += [
                "## 📎 配图列表",
                "",
                *[f"- `{img}`" for img in post.image_paths],
                "",
            ]

        content.append("> 🤖 由 auto_marketer.py v0.2 + Claude 自动生成 | 请人工审核后发布")

        filepath.write_text("\n".join(content), encoding="utf-8")
        print(f"  ✅ 已保存：{filepath.name}")
        return filepath


# ==============================
# 主流程
# ==============================

def main():
    print("=" * 55)
    print("🏡 伴山栖湖 · 自动化营销文案生成器 v0.2.0")
    print("   Powered by Claude AI")
    print("=" * 55)
    print()

    # Step 1: 扫描图片
    scanner = ImageScanner()
    images = scanner.scan()

    if not images:
        print()
        print("📭 暂无图片，演示模式：为当前季节所有场景各生成一篇文案")
        print()
        classifier = SceneClassifier()
        engine = ClaudeContentEngine()
        writer = OutputWriter()

        seasonal_scenes = classifier.get_seasonal_scenes()
        print(f"🌿 当前季节适合的场景：{', '.join(SCENE_CONFIG[s]['name'] for s in seasonal_scenes)}")
        print()

        for scene_id in seasonal_scenes:
            config = SCENE_CONFIG[scene_id]
            print(f"📝 生成「{config['name']}」…")
            title, body = engine.generate(scene_id=scene_id, image_count=0)
            post = MarketingPost(
                title=title,
                body=body,
                tags=config["hashtags"],
                scene=config["name"],
            )
            writer.write(post)
            print()

        print(f"🎉 演示完成！输出目录：{OUTPUT_DIR}")
        print("⚠️  请在发布前人工审核并替换 [xxx] 占位符。")
        return

    # Step 2: 按目录分组
    groups = scanner.group_by_folder(images)
    print(f"📂 检测到 {len(groups)} 个图片分组\n")

    classifier = SceneClassifier()
    engine = ClaudeContentEngine()
    writer = OutputWriter()

    # Step 3: 逐组生成文案
    generated = 0
    for folder_name, img_list in groups.items():
        scene_id = classifier.classify_by_folder_name(folder_name)
        config = SCENE_CONFIG[scene_id]
        print(f"📁 「{folder_name}」→ 场景：{config['name']}（{len(img_list)} 张图）")

        title, body = engine.generate(
            scene_id=scene_id,
            image_count=len(img_list),
        )

        post = MarketingPost(
            title=title,
            body=body,
            tags=config["hashtags"],
            scene=config["name"],
            image_paths=[str(p.relative_to(PROJECT_ROOT)) for p in img_list],
        )
        writer.write(post)
        generated += 1
        print()

    print(f"🎉 完成！共生成 {generated} 篇文案。输出目录：{OUTPUT_DIR}")
    print("⚠️  请在发布前人工审核内容。")


if __name__ == "__main__":
    main()
