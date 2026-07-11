# Foundry 工具包 + Foundry 托管代理研讨会

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

构建、测试并部署 AI 代理到 **Microsoft Foundry 代理服务** 作为 <strong>托管代理</strong> —— 完全通过 VS Code 使用 **Microsoft Foundry 扩展** 和 **Foundry 工具包**。

> **托管代理目前处于预览阶段。** 支持的区域有限 - 请参见[区域可用性](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)。

> 每个实验中的 `agent/` 文件夹由 Foundry 扩展 <strong>自动生成</strong> —— 之后你可以自定义代码、进行本地测试并部署。

### 🌐 多语言支持

#### 通过 GitHub Action 支持（自动且始终最新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](./README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **更喜欢本地克隆？**
>
> 本仓库含有 50 多种语言翻译文件，这大幅增加了下载大小。若想克隆时不包含翻译，请使用稀疏检出：
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD（Windows）：**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> 这样你就可以更快完成课程所需内容的下载。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## 架构

```mermaid
flowchart TB
    subgraph Local["本地开发（VS Code）"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "F5 调试" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["微软Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> 脚手架
    Playground -- "测试提示" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**流程：** Foundry 扩展生成代理脚手架 → 你自定义代码和指令 → 使用 Agent Inspector 本地测试 → 部署到 Foundry（将 Docker 镜像推送到 ACR） → 在 Playground 验证。

---

## 你将构建的内容

| 实验 | 描述 | 状态 |
|-----|-------------|--------|
| **实验 01 - 单一代理** | 构建 **“以高管视角解释”代理**，本地测试并部署至 Foundry | ✅ 可用 |
| **实验 02 - 多代理工作流** | 构建 **“简历 → 职位匹配评估”** —— 4 个代理协作评分匹配度并生成学习路线图 | ✅ 可用 |

---

## 认识高管代理

在本研讨会中，你将构建 **“以高管视角解释”代理** —— 一个将复杂技术术语翻译成冷静、适合董事会汇报摘要的 AI 代理。毕竟，说实话，没有人想听“v3.2 版本引入的同步调用导致线程池耗尽”的内容。

我是在经历了太多次我精心编写的事后分析得到回应：“所以…… 网站到底是挂了还是没挂？”之后，才打造了这个代理。

### 它是如何工作的

你输入一条技术更新，它则返回一个执行摘要——三点说明，无术语，无堆栈跟踪，无存在主义恐慌。只有<strong>发生了什么</strong>、<strong>业务影响</strong>及<strong>下一步</strong>。

### 观看其实际效果

**你说：**
> “由于 v3.2 版本引入的同步调用导致线程池耗尽，API 延迟增加。”

**代理回复：**

> **执行摘要：**
> - **发生了什么：** 最新版本发布后，系统运行变慢。
> - **业务影响：** 部分用户使用服务时体验到延迟。
> - **下一步：** 已回滚变更，并正在准备修复后重新部署。

### 为什么选择这个代理？

它是一个极简且单一用途的代理 - 非常适合学习托管代理的端到端工作流，而不会陷入复杂工具链。而且说实话？每个工程团队都能用上这样的工具。

---

## 研讨会结构

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **注意：** 每个实验中的 `agent/` 文件夹都是当你从命令面板运行 `Microsoft Foundry: Create a New Hosted Agent` 时，**Microsoft Foundry 扩展** 生成的。随后你会根据代理指令、工具和配置定制这些文件。实验 01 会带你从零开始重现这个过程。

---

## 入门

### 1. 克隆仓库

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. 设置 Python 虚拟环境

```bash
python -m venv venv
```

启动它：

- **Windows（PowerShell）：**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux：**
  ```bash
  source venv/bin/activate
  ```

### 3. 安装依赖

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. 配置环境变量

复制代理文件夹内的示例 `.env` 文件并填写你的配置：

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

编辑 `workshop/lab01-single-agent/agent/.env`：

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. 按顺序完成研讨会各实验

每个实验都是独立的模块。先从 **实验 01** 学习基础，再进入 **实验 02** 了解多代理工作流。

#### 实验 01 - 单一代理 ([完整说明](workshop/lab01-single-agent/README.md))

| # | 模块 | 链接 |
|---|--------|------|
| 1 | 阅读前置知识 | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | 安装 Foundry 工具包和 Foundry 扩展 | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | 创建 Foundry 项目 | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | 创建托管代理 | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | 配置指令和环境 | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | 本地测试 | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | 部署到 Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | 在 playground 验证 | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | 故障排查 | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### 实验 02 - 多代理工作流 ([完整说明](workshop/lab02-multi-agent/README.md))

| # | 模块 | 链接 |
|---|--------|------|
| 1 | 前置知识（实验 02） | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | 理解多代理架构 | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | 脚手架多代理项目 | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | 配置代理和环境 | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | 编排模式 | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | 本地测试（多代理） | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | 部署到 Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | 在 playground 中验证 | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | 故障排除（多代理） | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## 维护者

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## 所需权限（快速参考）

| 场景 | 所需角色 |
|----------|---------------|
| 创建新的 Foundry 项目 | Foundry 资源上的 **Azure AI 所有者** |
| 部署到现有项目（新资源） | 订阅上的 **Azure AI 所有者** + <strong>贡献者</strong> |
| 部署到完全配置的项目 | 帐户上的 <strong>读取者</strong> + 项目上的 **Azure AI 用户** |

> **重要:** Azure `所有者` 和 `贡献者` 角色仅包括<em>管理</em>权限，不包括<em>开发</em>（数据操作）权限。您需要 **Azure AI 用户** 或 **Azure AI 所有者** 来构建和部署代理。

---

## 参考资料

- [快速入门：部署您的首个托管代理（VS Code）](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [托管代理是什么？](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [在 VS Code 中创建托管代理工作流](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [部署托管代理](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry 的 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [架构审查代理示例](https://github.com/Azure-Samples/agent-architecture-review-sample) - 具有 MCP 工具、Excalidraw 图表和双重部署的真实托管代理

---


## 许可

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->