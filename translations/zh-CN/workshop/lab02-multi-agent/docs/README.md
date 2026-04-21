# 实验 02 - 多代理工作流：简历 → 职位匹配评估器

## 完整学习路径

本教程将引导你构建、测试和部署一个使用四个专门代理并通过 **WorkflowBuilder** 编排的<strong>多代理工作流</strong>，用于评估简历与职位的匹配度。

> **先决条件：** 开始实验 02 前，请先完成 [实验 01 - 单代理](../../lab01-single-agent/README.md)。

---

## 模块

| # | 模块 | 你将完成的内容 |
|---|--------|---------------|
| 0 | [先决条件](00-prerequisites.md) | 验证实验 01 完成情况，了解多代理概念 |
| 1 | [理解多代理架构](01-understand-multi-agent.md) | 学习 WorkflowBuilder、代理角色、编排图 |
| 2 | [搭建多代理项目骨架](02-scaffold-multi-agent.md) | 使用 Foundry 扩展搭建多代理工作流骨架 |
| 3 | [配置代理与环境](03-configure-agents.md) | 为4个代理编写指令，配置 MCP 工具，设置环境变量 |
| 4 | [编排模式](04-orchestration-patterns.md) | 探索并行扇出、顺序聚合及替代模式 |
| 5 | [本地测试](05-test-locally.md) | 使用 Agent Inspector 进行 F5 调试，运行简历 + 职位描述的冒烟测试 |
| 6 | [部署到 Foundry](06-deploy-to-foundry.md) | 构建容器，推送到 ACR，注册托管代理 |
| 7 | [在 Playground 验证](07-verify-in-playground.md) | 在 VS Code 和 Foundry 门户 playground 测试已部署代理 |
| 8 | [故障排除](08-troubleshooting.md) | 解决常见多代理问题（MCP错误、输出截断、包版本） |

---

## 预计所需时间

| 经验水平 | 时间 |
|-----------------|------|
| 最近完成实验 01 | 45-60 分钟 |
| 有一定 Azure AI 经验 | 60-90 分钟 |
| 第一次接触多代理 | 90-120 分钟 |

---

## 架构一览

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**返回：** [实验 02 说明文档](../README.md) · [工作坊首页](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 生成。尽管我们力求准确，但请注意自动翻译可能包含错误或不准确之处。原始文件的母语版本应被视为权威来源。对于重要信息，建议寻求专业人工翻译。我们对因使用本翻译而产生的任何误解或错误解释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->