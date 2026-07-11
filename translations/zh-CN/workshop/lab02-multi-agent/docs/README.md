# 实验 02 - 多智能体工作流：简历 → 职位匹配评估器

## 完整学习路径

本文档将引导您构建、测试和部署一个使用四个专用智能体，通过 **WorkflowBuilder** 编排的 <strong>多智能体工作流</strong>，用于评估简历与职位的匹配度。

> **前提条件：** 在开始实验 02 之前，请完成 [实验 01 - 单智能体](../../lab01-single-agent/README.md)。

---

## 模块

| # | 模块 | 您将完成的内容 |
|---|--------|---------------|
| 0 | [介绍](00-prerequisites.md) | 您将构建的内容，实验 01 验证，实验 02 与实验 01 的比较 |
| 1 | [了解多智能体架构](01-understand-multi-agent.md) | 了解 WorkflowBuilder、智能体角色、编排图 |
| 2 | [搭建多智能体项目骨架](02-scaffold-multi-agent.md) | 使用 Foundry 扩展向导搭建基础项目 |
| 3 | [配置智能体与环境](03-configure-agents.md) | 编写 4 个智能体的指令，配置 MCP 工具，设置环境变量 |
| 4 | [编排模式](04-orchestration-patterns.md) | 顺序链，内容转发，以及 WorkflowBuilder 的 OR 语义 |
| 5 | [本地测试](05-test-locally.md) | 使用 Agent Inspector F5 调试，使用简历+职位描述运行冒烟测试 |
| 6 | [部署到 Foundry](06-deploy-to-foundry.md) | 构建容器，推送到 ACR，注册托管智能体 |
| 7 | [在 Playground 验证](07-verify-in-playground.md) | 在 VS Code 和 Foundry 门户 Playground 中测试已部署智能体 |
| 8 | [故障排除](08-troubleshooting.md) | 解决常见多智能体问题（MCP 错误，输出截断，包版本） |
| 9 | [总结与后续步骤](09-summary.md) | 您构建的内容，学习的关键概念，清理，以及下一步方向 |

---

**返回：** [实验 02 README](../README.md) · [工作坊主页](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->