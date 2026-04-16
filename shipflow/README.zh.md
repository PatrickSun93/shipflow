# ShipFlow

> **其他语言：** [English](./README.md)

一个面向独立开发者的 Claude Code 插件，提供多智能体产品开发工作流：
**发现 → 规格 → 构建 → 验证 → 发布**，并在阶段间设置四个建议性关卡。

故事卡、架构决策记录（ADR）、需求简报和发布说明均以 Markdown 文件存储于仓库中，
无需任何外部集成。

## 状态

- **发现阶段**：已搭建，可以使用。
- **规格 / 构建 / 验证 / 发布**：已完成设计，尚未搭建。

## 安装（本地 / 开发模式）

```bash
/plugin add ./shipflow
```

或将此文件夹复制到 Claude Code 插件目录，然后执行 `/plugin reload`。

## 快速入门

```bash
/sf-init                          # 仓库一次性初始化
/sf-discover "暗黑模式切换"        # 开始发现对话
# ...回答主持人生成的问题...
/sf-brief                         # 将答案综合为需求简报
/sf-gate-1                        # 进入规格阶段前的建议性评审
```

## 工作原理

`/sf-discover` 会启动一个**发现主持人**，协调三个并行角色——**技术**、**用户体验**、**商业**——进行
两轮对话（初始轮 + 交叉讨论轮）。每个角色各自写入独立的 `dialogue-<角色>.md` 文件，避免并行写入冲突。
主持人将三方意见汇总为去重后的 `questions.md` 供你回答。

`/sf-brief` 会并行重启三个角色，各自综合简报的一个切片（技术：约束条件 + 风险；用户体验：
目标用户 + 未解问题；商业：现在做的理由 + 成功标准 + 非目标），然后拼合成
`docs/shipflow/briefs/BRIEF-NNN-<slug>.md`。

`/sf-gate-1` 并行启动 `product-lead`（产品负责人）和 `tech-lead`（技术负责人）审阅者，
各自写入 `gate-1-review-<角色>.md` 记录文件。技能对最终裁决进行分类
（通过 | 需要修改 | 拒绝），并将结果追加到简报中。

## 约定

- **关卡默认为建议性**（警告，非阻断）。如需更严格的执行，在 `shipflow.config.json`
  中切换为阻断模式。
- **所有阶段技能均按需读取** —— 不访问归档，不读取无关简报。
- **发现阶段角色不提出解决方案。** 那是规格阶段的工作。
- **代码风格：清晰简洁，优于巧妙抽象。** 适用于智能体提示词、钩子脚本和技能说明。

## 目录结构（执行 `/sf-init` 后）

```
your-repo/
├── CLAUDE.md                    # 热层（每次会话自动读取）
├── shipflow.config.json         # 关卡模式、索引重建频率等配置
└── docs/shipflow/
    ├── index.md                 # 温层索引（自动重建）
    ├── stack.md                 # 技术栈参考
    ├── briefs/                  # 已批准的产品需求简报
    ├── stories/                 # 活跃故事卡
    ├── decisions/               # 架构决策记录（ADR）
    ├── releases/                # 已发布的版本说明
    ├── retros/                  # 可选的发布后复盘
    ├── discovery/<slug>/        # 每个想法的对话记录和综合中间文件
    └── archive/                 # 冷层——已完成工作移至此处
```

## 致谢

- **每智能体日记**（`docs/shipflow/diaries/<agent>.md`）和 **Stop + PreCompact 钩子**
  是对 [MemPalace](https://github.com/MemPalace/mempalace) 创意的文件化重新实现，
  无代码共享——ShipFlow 保持零依赖。
- **多阶段多角色工作流结构** 借鉴了父目录 `workflow-comparison.md` 中记录的先行项目
  （相关行待首读后填写）。

## 许可证

MIT。
