# 模块 2 - 搭建多智能体项目骨架

⏱️ ~5 分钟

在本模块中，您将使用 [Foundry Toolkit for VS Code](https://aka.ms/foundrytk) 来<strong>搭建多代理项目的脚手架</strong>。向导将生成 `agent.yaml`、`main.py`、`Dockerfile`、`requirements.txt`、`.env` 以及 VS Code 调试配置——这样您就可以专注于在模块3中连接4代理的工作流。

> **关键概念：** 脚手架是一个带有一个代理的工作存根。您将在模块3中用 `WorkflowBuilder` 图替换占位符逻辑。您无需从头编写模板代码。

> **参考实现：** [`PersonalCareerCopilot/`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 是一个完整的工作示例。您可以用它来逐步对比您的工作。

### 搭建向导流程

```mermaid
flowchart LR
    A[Command Palette: Create New Hosted Agent] --> B[Language: Python]
    B --> C[API Type: Response API]
    C --> D[Template: Workflows]
    D --> E[Select Model]
    E --> F[Workspace Folder and Agent Name]
    F --> G[Generated Project]
```

---

## 第一步：打开创建托管代理向导

1. 按 `Ctrl+Shift+P` 打开<strong>命令面板</strong>。
2. 输入：**Foundry Toolkit: Create new Hosted Agent** 并选择它。
3. 向导在<strong>代理详情</strong>标签页打开。

> **替代方式：** 点击活动栏中的 **Foundry Toolkit** 图标 → 点击 **Hosted Agents** 旁边的 **+** 图标 → 选择 **Create New Hosted Agent**。

---

## 第二步：选择设置

![从示例创建托管代理 - 代理详情标签页，选中工作流模板](../../../../../translated_images/zh-CN/02-scaffold-wizard-details.af4798708b4a87f4.webp)

1. 在左侧导航/选项部分选择以下内容：

| 菜单 | 选择 | 说明 |
|--------|-----------|-------|
| <strong>语言</strong> | Python | 也支持 C# (.NET) |
| <strong>框架</strong> | Agent Framework | 提供 `Agent`、`AgentExecutor`、`WorkflowBuilder` |
| **API 类型** | Response API | `POST /responses` - 平台管理的历史记录，支持流式传输 |
| <strong>模板</strong> | **Workflows** | 按顺序通过多个代理处理请求 |

2. 选择后，点击 <strong>下一步</strong>

![从示例创建托管代理 - 创建标签页，文件夹名为 PersonalCareerCopilot](../../../../../translated_images/zh-CN/02-scaffold-wizard-create.ae0c285c309698ba.webp)

3. 在下一个窗口中选择以下内容：

| 菜单 | 选择 | 说明 |
|--------|-----------|-------|
| <strong>工作区文件夹</strong> | 浏览至目标文件夹 | 例如本仓库中的 `workshop/lab02-multi-agent/` |
| <strong>代理名称</strong> | `PersonalCareerCopilot` | 这将作为项目目录名称 |
| <strong>模型部署</strong> | 选择您部署的模型 | 例如 Lab 01 中的 `gpt-4.1-mini` |

4. 点击 <strong>创建</strong> 来搭建项目脚手架。VS Code 将生成文件并打开文件夹。

> **提示：** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series) 在多代理开发中兼顾速度与质量表现良好。

---

## 第三步：检查生成的项目

搭建完成后，验证您在资源管理器中看到这些文件 (`Ctrl+Shift+E`)：

```
📂 <your-agent-name>/
├── .azdignore          ← Files excluded from Azure Developer CLI deployments
├── .dockerignore       ← Files excluded from Docker builds
├── .env                ← Environment variables (placeholders - fill in Module 3)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted, protocol: responses)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Stub agent entry point (replace with WorkflowBuilder in Module 3)
└── requirements.txt    ← Python dependencies
```

> **重要：** 直接在 VS Code 中打开此搭建的文件夹，以便 `.vscode/launch.json` 和 `tasks.json` 正确应用于 F5 调试。

### 关键文件说明

| 文件 | 用途 |
|------|---------|
| `agent.yaml` | 声明 `kind: hosted`，映射环境变量，定义 `/responses` 协议 |
| `main.py` | 存根：一个 `FoundryChatClient` → `Agent` → `ResponsesHostServer`。您将在模块3用4代理+`WorkflowBuilder`替换它 |
| `Dockerfile` | `python:3.12-slim`，安装 `requirements.txt`，暴露8088端口，运行 `python main.py` |
| `requirements.txt` | `agent-framework-foundry`，`agent-framework-foundry-hosting`，`mcp<2,>=1.24.0`，`debugpy` |

> **参考：** 完整的生成内容见 [`PersonalCareerCopilot/agent.yaml`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) 和 [`PersonalCareerCopilot/requirements.txt`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/requirements.txt)。

---

### ✅ 检查点

- [ ] 搭建向导完成 - 新项目文件夹在资源管理器中可见
- [ ] 所有预期文件存在：`agent.yaml`、`main.py`、`Dockerfile`、`requirements.txt`、`.env`
- [ ] `agent.yaml` 显示 `kind: hosted` 和 `protocol: responses`
- [ ] `main.py` 导入 `Agent`、`FoundryChatClient`、`ResponsesHostServer`
- [ ] 搭建的文件夹作为 VS Code 工作区根目录打开
- [ ] 您理解 `main.py` 是个存根 - `WorkflowBuilder` 会在模块3增加

---

**上一步：** [01 - 理解多代理架构](01-understand-multi-agent.md) · **下一步：** [03 - 配置代理和环境 →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->