# claude-code-project

> **其他语言：** [English](./README.md)

这个仓库包含 **ShipFlow** —— 一个面向独立开发者的 Claude Code 插件，提供多智能体产品开发工作流
（发现 → 规格 → 构建 → 验证 → 发布），以及生成它的设计文档和交接笔记。

## 目录结构

| 路径 | 说明 |
|------|------|
| [`shipflow/`](./shipflow/) | 插件本体，可安装到 Claude Code 中。 |
| [`handoff.md`](./handoff.md) | 已锁定的设计决策和待办清单的持续记录。记录了事情为何如此设计的权威依据。 |
| [`shipflow-plan.md`](./shipflow-plan.md) | 各阶段的详细设计——智能体、技能、关卡、权衡与横切关注点。 |
| [`shipflow-memory-measurement.md`](./shipflow-memory-measurement.md) | 三层内存模型及预算验证方法。 |
| [`workflow-comparison.md`](./workflow-comparison.md) | 与同类项目的对比分析（BMAD、Agent OS、SuperClaude、Claude-Code-Game-Studios、claude-sub-agent）。 |

## 状态

- **发现阶段**：已搭建完成，可以试用。
- **规格 / 构建 / 验证 / 发布**：已完成设计（见 [`shipflow-plan.md`](./shipflow-plan.md)），尚未搭建。
- **样本 fixture 与测量脚本**：已完成设计，从 Cowork 迁移到 Claude Code 后尚未重建。

当前待办清单见 [`handoff.md`](./handoff.md) 的"下一步"部分。

## 安装插件

在 Claude Code 中，克隆此仓库后执行：

```bash
/plugin add ./shipflow
```

然后在你想使用 ShipFlow 的新仓库中：

```bash
/sf-init                          # 一次性初始化
/sf-discover "你的第一个想法"      # 开始发现对话
```

完整快速入门见 [`shipflow/README.md`](./shipflow/README.md)（英文）或 [`shipflow/README.zh.md`](./shipflow/README.zh.md)（中文）。

## 开发约定

- **简洁清晰，优于巧妙抽象。** 智能体提示词、钩子脚本和技能说明均遵循此原则。
- **智能体提示词 ≤ 80 行。** 钩子脚本 ≤ 40 行 bash。这不是任意限制——它确保每个组件对人类可读，而不只是对模型可读。
- **按需读取。** 阶段技能不得访问归档，除非被明确要求。由智能体提示词强制执行；审计钩子已设计但尚未实现。

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
