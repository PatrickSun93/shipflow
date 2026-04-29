# ShipFlow

> **其他语言：** [English](./README.md)

**一个装在文件夹里的产品团队。**

ShipFlow 给独立开发者提供一支 8 人创业团队才有的配置：技术负责人、产品
负责人、联合创始人、QA、安全审阅者、数据库审阅者，外加 6 个领域专家
（教育 / 金融 / 医疗 / 电商 / 开发工具 / 社交）—— 全部由一套 5 阶段工作流
协调：**发现 → 规格 → 构建 → 验证 → 发布**。

每个 agent 都有真实的**观点（POV）**、命名方法论（JTBD / RICE / OWASP /
CAP / 三人测试 / Rollback Test⋯），以及在不对劲的时候敢于 push back 的
姿态。简报、故事卡、ADR、发布说明全部以 Markdown 形式存在你自己的仓库里。
不依赖 SaaS、不依赖 Jira、不依赖任何外部服务。

## 状态

**v0.2.21** —— 五个阶段全部搭建完成，已通过 dogfood 验证。

**诚实统计：22 个智能体，结构如下：**
- **8 个带 Identity & POV 的具身化审阅者** —— `tech-lead`、`product-lead`、
  `cofounder-expert`、`qa-lead`、`security-reviewer`、`db-reviewer`、
  `code-reviewer`、`build-lead`、`challenger`
- **3 个带 Identity & POV 的发现期 persona** —— `discovery-tech-persona`、
  `discovery-ux-persona`、`discovery-business-persona`（v0.2.21 加上
  Identity 段，之前是单纯任务规格）
- **6 个领域专家**（在 Discovery 中根据 domain 自动激活）—— education、
  fintech、healthcare、ecommerce、devtools、social。专注领域专属关注点，
  Identity 比上述 8+3 个浅
- **5 个 specialty / 协调者** —— `discovery-moderator`、`spec-author`、
  `release-manager`、`project-archaeologist`，加上 challenger（也算在审阅者）

**23 个技能** —— init、discover、brief、spec、adr、build、tiny、quick、
hotfix、verify、ship、regen-index、resurvey、next、checkpoint、lint、grill，
外加四道 gate（`/sf-check-{brief,plan,build,ship}`）和三个跨切审阅
（`/sf-security-review`、`/sf-db-review`、`/sf-cofounder-review`）。

**4 个钩子** —— SessionStart、Stop、PreCompact、UserPromptSubmit。

## 安装

### 推荐方式 —— 通过 Claude Code marketplace

在任意 Claude Code 会话中，**两条命令分开发**（一条返回结果后再发下一条）：

```
/plugin marketplace add https://github.com/PatrickSun93/shipflow
```

```
/plugin install shipflow@shipflow-marketplace
```

> slash-command parser 在你一起 paste 时会把两行拼成一条命令，导致 URL
> malformed。一条一条发。
>
> `PatrickSun93/shipflow` 这个 shorthand 默认走 SSH，在
> `~/.ssh/known_hosts` 里没有 github.com key 的机器上会失败。完整 HTTPS
> URL 对 public repo 任何机器都能用。

验证：

```
/help
```

应该能看到 `/sf-init`、`/sf-discover`、`/sf-next`、`/sf-build` 等。

后续更新：

```
/plugin update shipflow@shipflow-marketplace
```

### 备选 —— 本地 / 开发模式

如果你要修改插件源代码本身：

```bash
git clone https://github.com/PatrickSun93/shipflow.git
claude --plugin-dir ./shipflow/shipflow
```

修改插件源代码后，会话内热加载：

```
/reload-plugins
```

## 快速入门

```bash
/sf-init                          # 仓库一次性初始化
/sf-discover "你的想法"            # 3-4 个角色先研究后提问
# ...回答问题...
/sf-brief                         # 综合答案；challenger 做压力测试
/sf-check-brief                   # 关卡 1：product-lead + tech-lead
/sf-spec                          # 将简报切成 5-10 个故事卡
/sf-check-plan                    # 关卡 2：逐故事技术评审
/sf-build                         # 实现一个故事（或用 --all 批量执行）
/sf-check-build                   # 关卡 3：测试 + 验收 + 代码审查
/sf-verify                        # qa-lead 对照简报 Success 验收
/sf-check-ship                    # 关卡 4：结构性检查 + 阻断审阅检查
/sf-ship                          # 出版本、归档、自动重建索引
```

或者直接 `/sf-next` —— 它会读取仓库状态并执行（或推荐）下一步。

## 与众不同之处

**多角度发现 + 自动调研。** Tech / UX / Business 三个角色并行运行，再外加
一个根据 seed 自动匹配的领域专家（education / fintech / healthcare /
ecommerce / devtools / social）。每个角色先用 1-3 次 WebSearch 查事实——
用户只回答判断题，不回答可以查到的事实题。

**审阅者像角色思考，不像清单运行。** 所有一级审阅者（tech-lead、product-lead、
cofounder-expert、qa-lead、security-reviewer、db-reviewer、build-lead、
challenger）都带 Identity & POV 段落 + 命名方法论工具箱 —— 产品有 JTBD /
RICE / Kano，技术有 CAP / OWASP / 12-factor / Rollback Test，联合创始人有
three-person test / forcing function / pre-mortem / Deletion Test，等等。
审阅者有观点和直觉，不是 5 条 bullet 的清单。

**Gate 默认建议性，按需阻断。** 四道关卡（brief / plan / build / ship）默认
只发裁决；在 `shipflow.config.json` 中可单独翻成 `block` 模式以严格执行。
跨切审阅（security / DB / cofounder）的 `Verdict: blocking` 会硬阻 `/sf-ship`，
仅可通过 `--force-risk-acknowledged` 显式覆盖，且覆盖记录会写进发布说明。

**按需调用跨切审阅者。** `/sf-security-review`（7 轮：secrets、auth、
injection、authz、deps、data、defaults）。`/sf-db-review`（6 轮：schema、
indexes、migrations、query patterns、data evolution、sync/consistency）。
`/sf-cofounder-review`（6 个 founder 框架 + 领域 overlay + Founder gut check）。

**在合适的时机自动建议。** `/sf-next` 和 `/sf-check-build` 会扫 build log
寻找路径信号（migrations / auth / token 等），推荐相关跨切审阅 ——
solo 开发者自己决定路径信号是否构成真实风险。

**抗 pause 的 session resume。** `UserPromptSubmit` hook 把每个回合写到
`docs/shipflow/sessions/log-<日期>.md`。`/sf-checkpoint` 在你预感 usage
快到上限时手动捕获 session intent。下次会话的 SessionStart hook 会自动
浮出这两份内容 —— Claude Code 撞 usage cap 时不会丢工作上下文。

**工作流完整性检查。** `/sf-lint` 严格检查：frontmatter、悬空的
`depends_on`、孤立的 `needs-ADR` 标记、断的 brief↔story 链接、`index.md`
死链接、verdict-vs-status 漂移。

**三种规模 —— 选对入口很重要。** Solo 开发者的工作不是一个 shape；
ShipFlow 提供三条明确路径，避免为了改个 typo 跑完整 5 阶段流程：

| 规模 | 路径 | 适用 |
|---|---|---|
| 🪶 **Tiny** | `/sf-tiny "<修改>"` | 一文件级琐碎：typo、文案、注释 |
| 🚀 **Quick** | `/sf-quick "<feature 或 fix>"` | **老项目，中等 feature/bug —— 你已经知道 scope。** 跳过 Discover + Spec 流程，直接生成 minimal brief + 1-3 个可立即 build 的 story |
| 🛠️ **Full** | `/sf-discover "<想法>"` → ... | 全新产品、重要 bet、scope 不清楚 |
| 🚨 **Hotfix** | `/sf-hotfix "<bug>"` | 生产紧急，跳到 Build → Ship |

老项目你已经 ship 过的，`/sf-quick` 通常是对的入口。一个 2 行的
bug fix 不需要 18 个 persona 问题。

## 约定

- **大小上限。** 智能体 ≤2000 tokens（典型 800-1500；带 Identity 段的
  审阅者可用满范围），钩子 ≤500 tokens。上限是参考不是红线 ——
  实质内容比机械压缩重要。
- **模型由用户控制。** Agent frontmatter 不写 `model:` 字段；subagent 继承
  用户当前 session 的模型（Opus / Sonnet / Haiku）。
- **窄读取。** 阶段技能不访问归档，除非显式要求。
- **发现期角色不提解决方案。** 那是规格阶段的工作。
- **清晰简洁优于巧妙抽象。** 适用于智能体 prompt、钩子脚本、skill 说明，
  以及 `/sf-build` 产出的代码（KISS/YAGNI、信任内部边界 + 在边界处加 log、
  Rule of Three、不留半成品代码、跟随邻居文件风格）。

## 目录结构（执行 `/sf-init` 之后）

```
your-repo/
├── CLAUDE.md                    # 热层（每次 session 自动读取）
├── shipflow.config.json         # gate 模式、cofounder review 模式、归档配置
└── docs/shipflow/
    ├── index.md                 # 温层索引（通过 /sf-regen-index 重建）
    ├── stack.md                 # 技术栈 + 约定
    ├── briefs/                  # 已批准的产品简报
    ├── stories/                 # 活跃故事（STORY / TINY / HOTFIX 记录）
    ├── decisions/               # ADR
    ├── releases/                # 已发布的版本说明
    ├── retros/                  # 发布后复盘
    ├── diaries/                 # 每个 agent 的审阅日记
    ├── discovery/<slug>/        # 每个 idea 的对话 + 综合
    ├── sessions/                # per-turn 日志 + checkpoints
    └── archive/                 # 冷层 —— 已发布工作迁移至此
```

## 致谢

- **每 agent 日记 + Stop/PreCompact 钩子** —— 思路借鉴
  [MemPalace](https://github.com/MemPalace/mempalace)，重新以文件化
  Markdown 实现（无代码共享）。
- **cofounder-expert 的命名思维模型 + research-first 协议** —— 受
  [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) 的人物视角技能启发。
- **Anthropic 官方 Claude Opus 4.7 prompt engineering best practices** ——
  影响了 build-lead、cofounder-expert、security-reviewer、db-reviewer 中
  使用的 XML tag 结构（`<investigate_before_answering>`、
  `<default_to_action>`、`<coverage_first>`）。
- **多阶段多角色工作流结构** —— 借鉴了 `../workflow-comparison.md` 中
  记录的先行项目（BMAD、Agent OS、SuperClaude、Claude-Code-Game-Studios、
  claude-sub-agent）。

无跨项目代码共享 —— ShipFlow 保持零依赖。

## 许可证

MIT。
