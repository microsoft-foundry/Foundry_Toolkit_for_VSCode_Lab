# 模块 7 - 总结与下一步

⏱️ ~5 分钟

**恭喜！** 你已经使用 Microsoft Foundry 和 VS Code 的 Foundry 工具包构建、测试并（如果是路径 A）部署了一个托管 AI 代理。

---

## 你所构建的内容

一个 **“像给高管解释一样”** 的代理，它：
- 通过 HTTP 接收技术事故报告或运营更新（`POST /responses`）
- 将其翻译成通俗易懂的高管摘要
- 遵循结构化输出格式（发生了什么 / 业务影响 / 下一步）
- 拒绝偏题请求和提示注入尝试
- 作为容器化托管代理运行在 Microsoft Foundry 代理服务中

---

## 关键概念

| 概念 | 你练习了什么 |
|---------|-------------------|
| <strong>代理框架架构</strong> | `FoundryChatClient` → `Agent` → `ResponsesHostServer` 流程 |
| <strong>托管代理生命周期</strong> | 脚手架 → 配置 → 本地测试 → 部署 → 云端验证 |
| <strong>系统提示工程</strong> | 角色、受众、输出格式、规则、安全约束和示例 |
| <strong>本地与托管的区别</strong> | 身份（个人凭据 vs. 托管身份）、终端、网络路径 |
| <strong>安全边界</strong> | 提示注入防御、角色遵循、边缘情况的优雅处理 |
| **Foundry 工具包工作流** | 项目创建、模型部署、代理脚手架、代理检查器、一键部署 |

---

## 你完成了什么

### 路径 A（Foundry 订阅）

- [x] 设置 Foundry 工具包并创建了带有已部署模型的 Foundry 项目
- [x] 脚手架托管代理，自动生成项目结构
- [x] 编写了带安全规则的结构化代理指令
- [x] 使用三个功能场景本地测试（代理检查器）
- [x] 部署到 Foundry 代理服务（容器化）
- [x] 在云端沙盒验证，包含4个边缘情况/安全测试

### 路径 B（Foundry 本地）

- [x] 设置 Foundry 工具包，连接本地模型终端
- [x] 脚手架托管代理项目
- [x] 编写带安全规则的结构化代理指令
- [x] 本地使用3个功能场景测试
- [x] 验证代理行为，无需云资源

---

## 下一步

### 继续学习

| 资源 | 描述 |
|----------|-------------|
| **[实验 02 - 多代理编排](../../lab02-multi-agent/docs/README.md)** | 构建一个由4个代理组成的工作流（简历 → 工作适配评估）并使用编排模式 |
| **[为你的代理添加工具](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | 通过工具目录连接 API、数据库或自定义函数 |
| **[添加知识（RAG）](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 使用文档、向量存储或 Bing 搜索为代理提供基础 |
| **[Microsoft Foundry 文档](https://learn.microsoft.com/azure/foundry/)** | 完整的平台参考 |
| **[代理框架 SDK 参考](https://learn.microsoft.com/agent-framework/)** | `agent-framework` 包的 API 文档 |
| **[Foundry 工具包 - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 扩展发布说明和更新日志 |

### 扩展你的代理的想法

- <strong>添加日期工具</strong> - 让代理在摘要中包含“截至今日”的上下文
- <strong>连接到事故数据库</strong> - 通过工具函数获取真实的事故详情
- **添加 Bing 充实工具** - 让代理查找最近新闻以获得更多上下文
- <strong>尝试不同模型</strong> - 比较 `gpt-4.1` 与 `gpt-4.1-mini` 的输出质量
- **使用 Foundry 评估** - 利用评估功能批量测量代理质量

### 针对路径 B 用户：升级至云端部署

当你准备好部署到云端时：
1. 获取一个 Azure 订阅（[azure.microsoft.com/free](https://azure.microsoft.com/free/)）
2. 完成 [模块 01，设置](01-setup.md#step-2-set-up-based-on-your-access)（创建项目，部署模型，分配 RBAC）
3. 更新你的 `.env` 文件，填写 Foundry 项目终端和模型部署名称
4. 从 [模块 05 - 部署到 Foundry](05-deploy-to-foundry.md) 继续

---

## 清理资源（可选）

如果你想移除本次工作坊中创建的 Azure 资源：

### 选项 1：删除资源组（删除所有资源）

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 选项 2：仅删除托管代理

1. 打开 [ai.azure.com](https://ai.azure.com) → 你的项目 → <strong>构建</strong> → <strong>代理</strong>。
2. 点击你的代理 → 点击 <strong>删除</strong>。

### 选项 3：删除模型部署

1. 在 Foundry 侧边栏展开你的项目 → <strong>模型</strong>。
2. 右键模型部署 → <strong>删除</strong>。

> **费用说明：** 托管代理只在运行时计费。停止或删除代理后，不会有持续费用。模型部署可能因预留容量产生少量费用——用完请删除。

---

**上一篇：** [06 - 在沙盒验证](06-verify-in-playground.md) · **下一篇：** [08 - 故障排除（参考）→](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->