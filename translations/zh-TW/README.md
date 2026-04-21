# Foundry Toolkit + Foundry Hosted Agents 工作坊

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.0.0rc3-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents/)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

從 VS Code 使用 **Microsoft Foundry 擴充功能** 與 **Foundry Toolkit**，建立、測試及部署 AI 代理到 **Microsoft Foundry Agent Service** 作為 **Hosted Agents**。

> **Hosted Agents 目前為預覽版本。** 支援的區域有限 - 請參閱 [區域可用性](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)。

> 每個實驗室中的 `agent/` 資料夾是由 Foundry 擴充功能 <strong>自動腳手架生成</strong> 的 - 然後你可以自訂代碼，進行本地測試並部署。

### 🌐 多語言支援

#### 透過 GitHub Action 支援（自動且持續更新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[阿拉伯語](../ar/README.md) | [孟加拉語](../bn/README.md) | [保加利亞語](../bg/README.md) | [緬甸語](../my/README.md) | [簡體中文](../zh-CN/README.md) | [繁體中文（香港）](../zh-HK/README.md) | [繁體中文（澳門）](../zh-MO/README.md) | [繁體中文（台灣）](./README.md) | [克羅埃西亞語](../hr/README.md) | [捷克語](../cs/README.md) | [丹麥語](../da/README.md) | [荷蘭語](../nl/README.md) | [愛沙尼亞語](../et/README.md) | [芬蘭語](../fi/README.md) | [法語](../fr/README.md) | [德語](../de/README.md) | [希臘語](../el/README.md) | [希伯來語](../he/README.md) | [印地語](../hi/README.md) | [匈牙利語](../hu/README.md) | [印尼語](../id/README.md) | [義大利語](../it/README.md) | [日語](../ja/README.md) | [坎那達語](../kn/README.md) | [高棉語](../km/README.md) | [韓語](../ko/README.md) | [立陶宛語](../lt/README.md) | [馬來語](../ms/README.md) | [馬拉雅拉姆語](../ml/README.md) | [馬拉地語](../mr/README.md) | [尼泊爾語](../ne/README.md) | [奈及利亞皮欽語](../pcm/README.md) | [挪威語](../no/README.md) | [波斯語（法爾西語）](../fa/README.md) | [波蘭語](../pl/README.md) | [葡萄牙語（巴西）](../pt-BR/README.md) | [葡萄牙語（葡萄牙）](../pt-PT/README.md) | [旁遮普語（古魯穆奇文）](../pa/README.md) | [羅馬尼亞語](../ro/README.md) | [俄語](../ru/README.md) | [塞爾維亞語（西里爾字母）](../sr/README.md) | [斯洛伐克語](../sk/README.md) | [斯洛維尼亞語](../sl/README.md) | [西班牙語](../es/README.md) | [斯瓦希里語](../sw/README.md) | [瑞典語](../sv/README.md) | [他加祿語（菲律賓語）](../tl/README.md) | [泰米爾語](../ta/README.md) | [泰盧固語](../te/README.md) | [泰語](../th/README.md) | [土耳其語](../tr/README.md) | [烏克蘭語](../uk/README.md) | [烏爾都語](../ur/README.md) | [越南語](../vi/README.md)

> **想要本地同步克隆？**
>
> 本倉庫包含超過 50 種語言的翻譯，這會大幅增加下載大小。若要不包含翻譯下載，請使用稀疏檢出：
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
> 這樣你能夠更快速下載完成課程所需的所有東西。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## 架構

```mermaid
flowchart TB
    subgraph Local["本地開發 (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        擴充套件"]
        FoundryToolkit["Foundry 工具套件
        擴充套件"]
        Scaffold["腳手架代理程式碼
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["代理程式檢查器
        (本地測試)"]
        FE -- "建立新的
        託管代理" --> Scaffold
        Scaffold -- "F5 除錯" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure 容器
        登錄"]
        AgentService["Foundry 代理服務
        (託管代理執行階段)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry 遊樂場
        & VS Code 遊樂場"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "部署
    (Docker 建置 + 推送)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "測試提示" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**流程：** Foundry 擴充功能腳手架建立代理 → 你客製化代碼與指示 → 使用 Agent Inspector 本地測試 → 部署到 Foundry（將 Docker 映像推送到 ACR）→ 在 Playground 驗證。

---

## 你將構建什麼

| 實驗室 | 描述 | 狀態 |
|-----|-------------|--------|
| **實驗室 01 - 單一代理** | 建立 **「解釋給我，一位執行長聽得懂」代理**，本地測試並部署至 Foundry | ✅ 可用 |
| **實驗室 02 - 多代理工作流程** | 建立 **「履歷 → 工作適配評估員」** - 4 個代理合作評分履歷適配度並產生學習路線圖 | ✅ 可用 |

---

## 認識執行長代理

在本工作坊中，你將建立 **「解釋給我，一位執行長聽得懂」代理** —— 一個把複雜技術術語轉換成冷靜、適合董事會聽的摘要的 AI 代理。說實話，高階主管誰想聽什麼「v3.2 版本引入同步呼叫導致執行緒池耗盡」這種技術細節呢？

我在經歷太多次我的完美事後檢討文章得到的回覆是：「所以……網站到底掛了沒？」之後建立了這個代理。

### 它是如何運作的

你給它技術更新內容，它回應一個執行長摘要 —— 三點精簡內容，沒有術語、沒有堆疊追蹤、沒有存在主義的恐懼感。只有 <strong>發生了什麼事</strong>，<strong>業務影響</strong>，和 <strong>下一步</strong>。

### 實際示範

**你說：**
> 「API 延遲增加是因為 v3.2 版本引入的同步呼叫導致執行緒池耗盡。」

**代理回覆：**

> **執行長摘要：**
> - **發生了什麼事：** 在最新版本釋出後，系統變慢了。
> - **業務影響：** 部分用戶在使用服務時遇到延遲。
> - **下一步：** 已將更改回滾，並正在準備修補後重新部署。

### 為什麼選這個代理？

它是個非常簡單、單一目的代理 —— 非常適合全程學習 Hosted Agent 工作流程而不會陷入複雜的工具鏈中。老實說，每個工程團隊都該有一個。

---

## 工作坊結構

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
├── 📂 ExecutiveAgent/                ← Standalone hosted agent project
│   ├── agent.yaml
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-install-foundry-toolkit.md
    │   │   ├── 02-create-foundry-project.md
    │   │   ├── 03-create-hosted-agent.md
    │   │   ├── 04-configure-and-code.md
    │   │   ├── 05-test-locally.md
    │   │   ├── 06-deploy-to-foundry.md
    │   │   ├── 07-verify-in-playground.md
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

> **注意：** 每個實驗室裏的 `agent/` 資料夾是你從命令面板執行 `Microsoft Foundry: Create a New Hosted Agent` 時，**Microsoft Foundry 擴充功能** 自動產生的。檔案隨後按照你的代理指令、工具和設定進行定制。實驗室 01 將會引導你從零開始重建此代理。

---

## 開始

### 1. 克隆此倉庫

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. 設定 Python 虛擬環境

```bash
python -m venv venv
```

啟用它：

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. 安裝相依套件

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. 設定環境變數

複製 agent 資料夾中的範例 `.env` 檔案，並填入你的值：

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

編輯 `workshop/lab01-single-agent/agent/.env`：

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. 跟隨工作坊實驗室練習

每個實驗室都是自包含的模組。從 **實驗室 01** 開始學習基礎，接著前進到 **實驗室 02** 進行多代理工作流程。

#### 實驗室 01 - 單一代理 ([完整說明](workshop/lab01-single-agent/README.md))

| # | 模組 | 連結 |
|---|--------|------|
| 1 | 閱讀先決條件 | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | 安裝 Foundry Toolkit & Foundry 擴充功能 | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | 建立 Foundry 專案 | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | 建立 Hosted Agent | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | 配置指示與環境 | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | 本地測試 | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | 部署到 Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | 在 Playground 驗證 | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | 疑難排解 | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### 實驗室 02 - 多代理工作流程 ([完整說明](workshop/lab02-multi-agent/README.md))

| # | 模組 | 連結 |
|---|--------|------|
| 1 | 先決條件（實驗室 02） | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | 了解多代理架構 | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | 腳手架多代理專案 | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | 配置代理與環境 | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | 編排模式 | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | 本地測試（多代理） | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | 部署到 Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | 在 playground 中驗證 | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | 疑難排解（多代理） | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## 維護者

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

## 所需權限（快速參考）

| 場景 | 所需角色 |
|----------|---------------|
| 建立新的 Foundry 專案 | Foundry 資源上的 **Azure AI 擁有者** |
| 部署到現有專案（新資源） | 訂閱上的 **Azure AI 擁有者** + <strong>貢獻者</strong> |
| 部署至完全配置的專案 | 帳戶上的 <strong>讀者</strong> + 專案上的 **Azure AI 使用者** |

> **重要:** Azure 的 `擁有者` 和 `貢獻者` 角色僅包含 <em>管理</em> 權限，不包括 <em>開發</em>（資料操作）權限。您需要 **Azure AI 使用者** 或 **Azure AI 擁有者** 來建立和部署代理。

---

## 參考資料

- [快速入門：部署您的第一個託管代理 (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [什麼是託管代理？](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [在 VS Code 中建立託管代理工作流程](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [部署託管代理](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry 的 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [架構審查代理範例](https://github.com/Azure-Samples/agent-architecture-review-sample) - 具有 MCP 工具、Excalidraw 圖表和雙重部署的實務託管代理

---

## 授權條款

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件之母語版本應視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯所引起之任何誤解或曲解負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->