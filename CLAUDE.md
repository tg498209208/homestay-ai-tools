# 🏡 伴山栖湖民宿 AI 参谋行军条例

> 本文件为最高行动准则，Claude Code 每次启动必须优先读取并严格遵守。
> **项目代号**：伴山栖湖 · 线上参谋部　**总指挥**：司令官（tg498209208）

---

## ⚖️ 铁律 0：先谋后动（双重刹车系统）

**任何任务开始前，禁止直接执行或修改任何文件。**

必须先输出一份中文《战术思路与执行方案》，格式如下：

### 战术思路与执行方案

**技术路线**：[简述实现方法]

**预计影响文件**：
- [文件路径1]
- [文件路径2]

**安全检查**：
- 是否涉及 Assets/Raw_Materials/：是 / 否
- 是否涉及隐私数据或密钥：是 / 否

**潜在风险**：[列出可能的副作用]

---
司令官，以上方案涉及上述文件。确认后我将开始执行，
完成后自动 git commit 并等待您授权后再 git push。
请回复【通过】或【执行】启动操作。

只有收到明确的【通过】或【执行】指令后，才可以动手。

---

## 📦 规范 1：资产防线（素材只增不减）

- `Assets/Raw_Materials/` 为只读原始素材区，**严禁执行任何 `rm`、覆盖或移动操作**
- 所有处理后的图片（裁剪、增强等）必须作为新文件输出到：
  `Assets/Images/[分类名]/`
- 去重或清理脚本只允许操作 `Assets/Images/` 目录，原始区永远不动

---

## 🔐 规范 2：安全防线（隐私绝对隔离）

- **严禁**将 `sk-` 开头的 API 密钥、密码、财务数据直接写入任何脚本或代码文件
- 所有敏感信息必须存放在 `.env` 文件中，通过环境变量调用
- `.gitignore` 中必须包含以下条目，推送前强制核查：

```
.env
.env.local
.env*.local
Assets/Raw_Materials/
```

- 执行任何 `git push` 前，必须确认以上文件未被追踪

---

## 📝 规范 3：运营防线（自媒体文风校准）

- 生成任何小红书、抖音或 OTA 文案前，**必须先读取**：
  `Docs/Marketing/my_history_style.md`
- 文案核心要求：
  - 禁止 AI 流水线腔调，保持真实民宿主人视角
  - 强制包含地域标签：**重庆 / 涪陵 / 伴山栖湖**
  - 严禁地名张冠李戴，所有地理信息必须准确
  - 季节、景色描述必须符合同乐镇海拔 700m 实际情况

---

## 🚀 规范 4：Git 同步（两段式提交）

任务执行成功后，执行以下流程：

**第一段（自动执行）**：

```bash
git add .
git commit -m "特性: [中文描述具体操作内容]"
```

**第二段（等待授权）**：
展示 commit 摘要后询问：

> commit 已就绪：[commit message]
> 司令官，是否授权推送到远端？回复【推送】执行 git push。

收到【推送】指令后才执行：

```bash
git push
```

> 设计原因：push 为不可逆操作，二次确认防止错误同步到远端。

---

## ✅ 每次启动自检清单

Claude Code 每次启动时必须默默完成以下检查：

- [ ] 已读取本 CLAUDE.md 全文
- [ ] 已确认 `.gitignore` 包含 `.env` 和 `Raw_Materials/`
- [ ] 如有文案任务，已确认 `my_history_style.md` 可访问
- [ ] 双重刹车系统处于激活状态

---

*版本：v1.1 | 项目：伴山栖湖民宿 AI 工具库 | 制定人：司令官*

---
---

# 📋 项目档案（背景参考）

> 以下为项目技术背景与资产说明，供 Claude 理解业务上下文时参考。

---

## 📌 项目背景

**伴山栖湖** 是一间依山傍湖的精品民宿，坐落于重庆涪陵同乐镇（海拔约 700m），核心卖点包括：

| 板块 | 内容 |
|------|------|
| 🍵 围炉煮茶 | 秋冬限定体验，炭火+烤物+湖景 |
| 🍞 窑烤面包 | 自有柴烧面包窑，手工制作 |
| 💒 草坪婚礼 | 山湖之间的私密小型婚礼场地 |
| 🛏️ 山景客房 | 落地窗直面山湖，全屋地暖，共 11 间 |
| 🌿 湖畔景观 | 湖边栈道、桨板划水、日落打卡点 |

**官网仓库**：`~/民宿展示/`（纯静态 HTML + 实景图片）
**本仓库**：`~/Desktop/homestay-ai-tools/`（AI 自动化工具）

---

## 🎯 项目目标

### 短期（1-2 周）
- [x] 小红书爆款营销模板库（围炉煮茶 / 窑烤面包 / 草坪婚礼）
- [x] 自动化文案生成器基础框架（`auto_marketer.py`）
- [x] 素材智能分类 + 批量修图（`media_manager.py`）
- [ ] 接入图片 → 文案的全自动管线
- [ ] 小红书多账号定时发布工具

### 中期（1-2 月）
- [ ] 多平台适配：抖音/视频号/B站 的短视频脚本自动生成
- [ ] 客服话术库：微信/私域常见问答自动回复

### 长期（3-6 月）
- [ ] 民宿 PMS 对接：房价/房态数据看板
- [ ] 竞品监控：同区域民宿价格/评价爬虫 + 分析
- [ ] 客户画像系统：订单数据 + 社交媒体互动整合分析

---

## 🏗️ 技术栈

| 层 | 技术选型 | 说明 |
|----|---------|------|
| 后端脚本 | Python 3.10+ | 文案生成、数据处理、图片处理 |
| AI 能力（文案） | DeepSeek API（via LiteLLM） | 走 localhost:4000 代理 |
| AI 能力（视觉） | Claude Sonnet（via LiteLLM） | 图片分类走 localhost:4000 |
| 图片处理 | Pillow | 3:4 裁剪、色彩优化 |
| 数据存储 | SQLite / JSON 文件 | 轻量级，后期可迁 Supabase |
| 版本控制 | Git + GitHub | 仓库：`tg498209208/homestay-ai-tools` |
| 代理环境 | LiteLLM @ localhost:4000 | 统一 AI 接入层 |

---

## 📁 实际目录结构

```
homestay-ai-tools/                   # 项目根目录（~/Desktop/homestay-ai-tools/）
├── CLAUDE.md                        # 本文件——行军条例 + 项目档案
├── .gitignore                       # 忽略规则（图片、密钥等不入库）
│
├── Assets/
│   ├── Raw_Materials/               # 🔒 只读原始素材（不入 Git）
│   └── Images/                      # ✅ 分类后素材输出区
│       ├── 窑烤面包/
│       ├── 客房景观/
│       ├── 草坪婚礼/
│       ├── 围炉煮茶/
│       ├── 湖畔落日/
│       └── 其他/
│
├── Docs/
│   └── Marketing/
│       ├── Xiaohongshu_Templates.md # 小红书营销模板库
│       └── my_history_style.md     # 🔑 文风参考（生成文案前必读）
│
├── Tools/
│   └── Scripts/
│       ├── auto_marketer.py         # 自动化营销文案生成器
│       ├── media_manager.py         # 素材智能分类 + 批量修图
│       └── scheduler.py             # （待建）多平台定时发布工具
│
└── Output/
    ├── Generated/                   # 自动生成的营销文案（不入 Git）
    └── Enhanced/                    # 修图输出（不入 Git）
```

---

## 📋 常用命令

```bash
# 生成营销文案
cd ~/Desktop/homestay-ai-tools && source ~/.zshrc && python3 Tools/Scripts/auto_marketer.py

# 素材分类 + 修图（AI 视觉识别）
python3 Tools/Scripts/media_manager.py

# 演习模式（不修改文件）
python3 Tools/Scripts/media_manager.py --dry-run

# 查看最近提交
git log --oneline -10

# 检查 LiteLLM 代理状态
curl http://localhost:4000/health
```

---

## 🔗 关联资源

| 资源 | 地址 |
|------|------|
| 民宿官网仓库 | `~/民宿展示/` |
| 本工具库 GitHub | https://github.com/tg498209208/homestay-ai-tools |
| LiteLLM 代理 | http://localhost:4000 |
| DeepSeek API | https://api.deepseek.com |

---

> 🫡 **时刻准备着，司令官。**
