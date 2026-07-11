# 模块 9 - 总结与下一步

⏱️ 约5分钟

**恭喜！** 你已经使用 Microsoft Foundry 和 Foundry Toolkit for VS Code 构建、测试并（如果在路径A）部署了一个多代理工作流。

---

## 你构建了什么

**简历 → 职位匹配评估器** - 一个多代理托管工作流，它：
- 通过 HTTP 接收简历和职位描述（`POST /responses`）
- 运行四个专门代理组成的顺序流水线——每个代理传递其后继所需的数据
- 返回匹配分数（0–100 及详细分解）、技能和认证差距列表，以及针对每个差距的个性化学习路线图，包含真实的 Microsoft Learn 链接
- 调用 Microsoft Learn MCP 服务器（`https://learn.microsoft.com/api/mcp`）获取每个识别出的技能差距的官方学习资源
- 作为单个容器化托管代理运行在 Microsoft Foundry 代理服务中

---

## 你学到了哪些关键概念

| 概念 | 你练习了什么 |
|---------|-------------------|
| <strong>多代理编排</strong> | 使用 `WorkflowBuilder` 实现顺序流水线及 `add_edge()` |
| <strong>代理专门化</strong> | 四个聚焦代理优于一个通用代理 |
| <strong>内容路由模式</strong> | ResumeParser 同时作为路由器 —— 它在 `[职位描述直传]` 部分保留 JD 文本供下游代理访问（必需，因为 `context_mode="last_agent"` 意味着只有 `start_executor` 能看到原始用户消息） |
| <strong>内容转发模式</strong> | JD Agent 转发 `[解析简历直传]`，使 MatchingAgent 同时获得两个配置文件；避免合流图导致的 OR 语义双重触发 |
| **MCP 工具集成** | 使用 `@tool` + `streamable_http_client` 调用外部 MCP 服务器 |
| <strong>托管代理生命周期</strong> | 脚手架 → 配置 → 本地测试 → 部署 → 云端验证 |
| **`context_mode="last_agent"`** | 每个执行器仅看到其直接前驱的输出 |
| **Foundry Toolkit 工作流** | 脚手架向导、代理检查器、工作流可视化、一键部署 |

---

## 你完成了哪些内容

<details open>
<summary><strong>🅰️ 路径 A - Foundry 订阅</strong></summary>

- [x] 验证实验 01 设置：项目、模型和 RBAC 仍然有效
- [x] 使用工作流模板搭建了多代理项目
- [x] 编写了四个代理指令集（ResumeParser，JD Agent，MatchingAgent，GapAnalyzer）
- [x] 集成了 Microsoft Learn MCP 工具与 `streamable_http_client`
- [x] 使用 `WorkflowBuilder` 连接工作流图（顺序流水线＋内容转发）
- [x] 本地用三个冒烟测试（代理检查器）测试过——匹配评分、差距卡片和 MCP URL
- [x] 已部署到 Foundry 代理服务（容器化，管理身份）
- [x] 在云端游乐场验证——结构与本地结果一致

</details>

<details open>
<summary><strong>🅱️ 路径 B - Foundry 本地运行</strong></summary>

- [x] 验证实验 01 设置：Foundry 本地运行并连接本地模型
- [x] 使用工作流模板搭建了多代理项目
- [x] 编写了四个代理指令集并连接工作流图
- [x] 集成了 Microsoft Learn MCP 工具
- [x] 本地用三个冒烟测试测试过
- [x] 验证了多代理行为，无需云资源

</details>

---

## 下一步

### 继续学习

| 资源 | 说明 |
|----------|-------------|
| **[Agent Framework SDK 参考](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`，`WorkflowBuilder`，`AgentExecutor` 的 API 文档 |
| **[MCP 工具目录](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | 将代理连接到其他 MCP 服务器（Bing，GitHub，自定义） |
| **[添加知识（RAG）](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 用文档、向量存储或 Bing 搜索为代理赋能 |
| **[Foundry 评估](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | 使用自动化评估器大规模测量代理质量 |
| **[Microsoft Foundry 文档](https://learn.microsoft.com/azure/foundry/)** | 平台完整参考 |
| **[Foundry Toolkit - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 扩展发布说明和更新日志 |

### 扩展此工作流的想法

- <strong>增加第五个代理</strong> - 一个面试教练，基于差距报告生成可能的面试问题
- **增加 Bing 基础工具** - 让 JD Agent 搜索类似职位发布以丰富要求
- <strong>连接简历数据库</strong> - 通过自定义 `@tool` 从数据库拉取候选人资料
- <strong>尝试不同模型</strong> - 比较 `gpt-4.1` 与 `gpt-4.1-mini` 的输出质量和延迟
- **用 Foundry 评估** - 使用评估功能，对匹配报告与黄金数据集进行评分

### 针对路径 B 用户：升级到云端部署

当你准备好部署到云端时：
1. 获取 Azure 订阅（[azure.microsoft.com/free](https://azure.microsoft.com/free/)）
2. 完成 [实验 01，模块 01](../../lab01-single-agent/docs/01-setup.md)（创建项目、部署模型、分配 RBAC）
3. 更新 `.env` 中的 Foundry 项目端点和模型部署名称
4. 从 [模块 06 - 部署到 Foundry](06-deploy-to-foundry.md) 继续

---

## 清理资源（可选）

如果你想删除本次研讨会期间创建的 Azure 资源：

### 选项 1：删除资源组（删除所有内容）

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 选项 2：只删除托管代理

1. 打开 [ai.azure.com](https://ai.azure.com) → 你的项目 → <strong>构建</strong> → <strong>代理</strong>。
2. 找到 **PersonalCareerCopilot** → 点击 <strong>删除</strong>。

### 选项 3：删除模型部署

1. 在 Foundry 侧边栏展开你的项目 → <strong>模型</strong>。
2. 右键模型部署 → <strong>删除</strong>。

> **费用说明：** 托管代理只在运行时产生费用。如果停止或删除代理，则不再收取费用。模型部署可能因保留容量产生少量费用——完成后请删除。

---

**上一篇：** [08 - 故障排除](08-troubleshooting.md) · **主页：** [实验 02 README](../README.md) · [研讨会主页](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->