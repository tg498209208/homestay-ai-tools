# BMW DevOps Dashboard - Claude Configuration

## ⚠️ Worktree 同步检查（每次对话开始必做）

**主仓库路径**: `/Users/frozenleaf/Desktop/DevOps-Dashboard重构版`

每次开始新对话时，必须执行以下步骤确保 worktree 与主仓库同步：

```bash
# 1. 检查主仓库是否有未提交的更改
cd /Users/frozenleaf/Desktop/DevOps-Dashboard重构版 && git status

# 2. 如果有未提交的更改，先在主仓库提交
cd /Users/frozenleaf/Desktop/DevOps-Dashboard重构版 && git add -A && git commit -m "sync: 同步最新更改"

# 3. 在 worktree 中拉取最新更改
git fetch origin && git merge uat --no-edit
```

**常见同步问题**：
- 主仓库有 untracked 文件 → 新功能未 commit，worktree 看不到
- 主仓库在不同分支 → 确保都在 `uat` 分支上

## Project Context
BMW Financial Services China DevOps平台，插件化架构重构版。
2-3人小团队，1-2周迭代周期。

## Tech Stack
- React 18 + TypeScript + Vite
- Zustand状态管理 + TanStack Query
- Supabase PostgreSQL + ShadCN/UI
- 插件化架构 + 动态路由

## Development Commands
```bash
# 开发环境
npm run dev # 启动开发服务器
npm run build # 生产构建
npm run lint # 代码检查
npm run type-check # TypeScript检查
npm test # 运行测试

# 关键路径
/docs/development/task-planning.md # 任务规划记录
/docs/business/user-stories/ # 用户故事
/src/plugins/ # 插件开发
```

## Key Principles
1. **插件优先**: 新功能作为插件实现，注册到动态路由系统
2. **认证检查**: 所有路由需要适当的权限控制
3. **TypeScript严格**: 保持类型安全，避免any类型
4. **Skills工作流强制执行**: 每个功能必须完成对应的Skills流程
5. **禁止未确认的硬编码和Mock数据**: 任何硬编码行为（配置、URL、密钥等）和Mock数据使用必须获得用户确认后执行

## 🔄 基于功能类型的Skills工作流

### 新插件开发 (完整流程)
必须按顺序完成：
1. **requirements-analysis** → 用户故事文档
2. **architecture-design** → 架构设计文档
3. **task-planning** → 详细实施计划
4. **开发实施** + code-review (PR中)
5. **testing** → 完整测试代码和说明

### 现有插件功能增强
必须完成：
1. **requirements-analysis** → 用户故事文档
2. **task-planning** → 轻量级任务清单
3. **testing** → 基础测试验证

### Bug修复
根据影响范围：
- 重要逻辑变更：**code-review** skill + 测试
- 简单修复：PR review + 基本测试

## 📋 文档输出标准

### 所有功能必需
- `docs/business/user-stories/US-XXX-[feature].md` (requirements-analysis)
- `tests/unit/plugins/[plugin-name]/[component].test.ts` + README.md (testing)

### 新插件开发额外文档
- **架构文档** (architecture-design):
  - 简单插件：在根目录 `ARCHITECTURE.md` 中添加插件设计章节
  - 复杂插件：可选择创建 `docs/architecture/[plugin-name]-design.md`
- `docs/development/implementation-plans/US-XXX-implementation.md` (task-planning)
- `docs/development/reviews/architecture-reviews/[plugin-name]-review.md` (重大架构code-review)

### 📁 文件存放结构
```
tests/
├── README.md                          # 整体测试策略
├── unit/plugins/[plugin-name]/
│   ├── README.md                      # 插件测试说明
│   ├── components.test.ts
│   ├── services.test.ts
│   └── hooks.test.ts
├── integration/
│   ├── README.md
│   └── [plugin-name]-integration.test.ts
└── e2e/
    ├── README.md
    └── [user-flow].test.ts

docs/development/reviews/
├── architecture-reviews/              # 新插件架构审查
├── security-reviews/                  # 安全审查
└── code-quality-audits/               # 季度代码质量审计
```

### 工具内记录
- PR代码审查：GitHub/GitLab PR comments (日常reviews)
- 测试覆盖率：`coverage/` 目录自动生成

## ✅ Skills完成检查

### 开发前必检
- [ ] 功能类型已确定？(新插件/功能增强/Bug修复)
- [ ] 对应Skills已执行？
- [ ] 必需文档已生成？

### 开发后必检
- [ ] 所有验收标准通过？
- [ ] 测试覆盖率达标？
- [ ] PR review完成？

## Quick Reference
- 主要架构文档: `ARCHITECTURE.md`
- 项目需求: `PRD.md`
- Skills目录: `.claude/skills/`
- Sub-Agent目录: `.claude/agents/`
- 用户故事目录: `docs/business/user-stories/`
- 测试目录: `tests/`

## 🤖 Plugin Validation Sub-Agent

### 功能
通过 Task tool 隔离上下文运行的插件合规性验证代理。执行 6 阶段深度检查：
目录结构 → 插件注册 → 类型安全 → 文档完整性 → 代码质量 → 交叉验证

### 调用方式

**单插件验证**：用户说 `validate plugin <plugin-name>`
**全量验证**：用户说 `validate all plugins`

### 执行流程
1. 读取 `.claude/agents/validate-plugin-prompt.md` 模板
2. 替换占位符：`{{PLUGIN_NAME}}`、`{{PascalCase}}`、`{{camelCase}}`、`{{VALIDATION_MODE}}`、`{{DATE}}`
3. 通过 `Task(subagent_type="general-purpose", run_in_background=true)` 生成隔离子代理执行验证
4. 子代理后台运行，主对话可继续其他工作
5. 验证完成后通过 `TaskOutput` 读取报告并呈现给用户

### 默认行为
- **始终后台运行**：Validation sub-agent 默认使用 `run_in_background: true`
- 用户无需每次指定，验证自动在后台执行

### 验证模式
| Mode | 适用场景 | 检查范围 |
|------|---------|---------|
| `full` | 新插件开发 | 全部 6 阶段，最严格 |
| `enhancement` | 现有插件功能增强 | 结构 + 注册 + 类型 + 测试 |
| `in-progress` | 开发中的插件 | 仅结构 + 注册 |

### 使用时机
- **必须**：PR 前、Skills 开发阶段完成后
- **可选**：日常健康检查

### 与现有工具的关系
- `scripts/validate-plugins.cjs` — 浅层文件存在性检查（CI 级别）
- **Sub-Agent** — 深度语义分析（开发级别，Claude 执行）
- **Skills 工作流** — 流程合规（人工级别，CLAUDE.md 指导）
