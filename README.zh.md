# claude-code-project

> **其他语言：** [English](./README.md)

这个仓库包含 **ShipFlow** —— *一个装在文件夹里的产品团队*。一个 Claude Code 插件，
给独立开发者提供 8 人创业团队的配置：技术负责人、产品负责人、联合创始人、QA、
安全 + 数据库审阅者，外加 6 个领域专家，协调 5 阶段工作流（发现 → 规格 → 构建
→ 验证 → 发布）。仓库里也包含生成它的设计文档和交接笔记。

## 目录结构

| 路径 | 说明 |
|------|------|
| [`shipflow/`](./shipflow/) | 插件本体，可安装到 Claude Code 中。 |
| [`handoff.md`](./handoff.md) | 已锁定的设计决策和待办清单的持续记录。记录了事情为何如此设计的权威依据。 |
| [`shipflow-plan.md`](./shipflow-plan.md) | 各阶段的详细设计——智能体、技能、关卡、权衡与横切关注点。 |
| [`shipflow-memory-measurement.md`](./shipflow-memory-measurement.md) | 三层内存模型及预算验证方法。 |
| [`workflow-comparison.md`](./workflow-comparison.md) | 与同类项目的对比分析（BMAD、Agent OS、SuperClaude、Claude-Code-Game-Studios、claude-sub-agent）。 |

## 状态

- **v0.2.16** —— 五个阶段全部搭建完成，已通过 dogfood 验证（发现 → 规格 →
  构建 → 验证 → 发布）。
- 20 个智能体（其中 8 个具备 Identity & POV 角色具身化）、21 个技能、4 个钩子。
  完整列表 + 快速入门见 [`shipflow/README.zh.md`](./shipflow/README.zh.md)。
- 跨切审阅者（security、DB、cofounder）的 `Verdict: blocking` 会硬阻
  `/sf-ship`，仅可通过 `--force-risk-acknowledged` 显式覆盖。
- **样本 fixture 与测量脚本**：已完成设计，从 Cowork 迁移到 Claude Code 后尚未重建。

当前待办清单见 [`handoff.md`](./handoff.md) 的"下一步"部分。

## 安装插件

在任意 Claude Code 会话中：

```
/plugin marketplace add PatrickSun93/shipflow
/plugin install shipflow@shipflow-marketplace
```

然后在你想使用 ShipFlow 的新仓库中：

```
/sf-init                          # 一次性初始化
/sf-discover "你的第一个想法"      # 3-4 个角色先研究后提问
```

或者直接 `/sf-next` —— 它读仓库状态并执行下一步。完整快速入门见
[`shipflow/README.zh.md`](./shipflow/README.zh.md)。

## 开发约定

- **简洁清晰，优于巧妙抽象。** 智能体提示词、钩子脚本和技能说明均遵循此原则。
- **智能体 ≤ 2000 tokens**（典型 800-1500；带 Identity 段的审阅者可用满范围），
  钩子 ≤ 500 tokens。Tokens 而非行数，因为模型按 token 计预算。
- **按需读取。** 阶段技能不得访问归档，除非被明确要求。

## 致谢

以下项目提供了创意灵感（无代码共享——ShipFlow 中的一切均为原生实现，无外部依赖）：

- **[MemPalace](https://github.com/MemPalace/mempalace)** —— `docs/shipflow/diaries/<agent>.md`
  中的每智能体日记概念，是对 MemPalace 的 `diary_write` / `diary_read` MCP 工具的文件化重新实现。
  Stop + PreCompact 钩子也借鉴了 MemPalace 的钩子设计，但以最简 Markdown 标记替代了逐字记录存储。
- **Claude Code / 智能体开发工作流先行项目** —— 整体阶段结构（发现 → 规格 → 构建 → 验证 → 发布）
  和多角色发现机制借鉴了 BMAD、Agent OS、SuperClaude、Claude-Code-Game-Studios 和 claude-sub-agent
  等项目的模式。详见 [`workflow-comparison.md`](./workflow-comparison.md)。

## 许可证

MIT —— 见 [`LICENSE`](./LICENSE)。
