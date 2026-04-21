# Module 0 - 先決條件

在開始 Lab 02 之前，請確認您已完成以下事項。本實驗室直接建立在 Lab 01 之上，請勿跳過。

---

## 1. 完成 Lab 01

Lab 02 假設您已經：

- [x] 完成所有 8 個模組的 [Lab 01 - 單一代理人](../../lab01-single-agent/README.md)
- [x] 成功部署單一代理人至 Foundry 代理人服務
- [x] 確認代理人在本地 Agent Inspector 和 Foundry Playground 中均能運作

如果您尚未完成 Lab 01，請返回並立即完成：[Lab 01 文件](../../lab01-single-agent/docs/00-prerequisites.md)

---

## 2. 驗證現有設定

Lab 01 中的所有工具應仍已安裝並能正常運作。請執行以下快速檢查：

### 2.1 Azure CLI

```powershell
az account show --query "{name:name, id:id}" --output table
```

預期結果：顯示您的訂閱名稱和 ID。如果失敗，請執行 [`az login`](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)。

### 2.2 VS Code 擴充功能

1. 按 `Ctrl+Shift+P` → 輸入 **"Microsoft Foundry"** → 確認您能看到命令 (例如 `Microsoft Foundry: Create a New Hosted Agent`)。
2. 按 `Ctrl+Shift+P` → 輸入 **"Foundry Toolkit"** → 確認您能看到命令 (例如 `Foundry Toolkit: Open Agent Inspector`)。

### 2.3 Foundry 專案與模型

1. 按一下 VS Code 活動列中的 **Microsoft Foundry** 圖示。
2. 確認您的專案有列出（如 `workshop-agents`）。
3. 展開專案 → 驗證存在部署成功的模型（例如 `gpt-4.1-mini`）且狀態為 **Succeeded**。

> **如果您的模型部署已過期：** 部分免費層級的部署會自動過期。請從 [模型目錄](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**）。

![Foundry sidebar showing project and deployed model with Succeeded status](../../../../../translated_images/zh-TW/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

### 2.4 RBAC 角色

確認您在 Foundry 專案中擁有 **Azure AI User** 角色：

1. 前往 [Azure 入口網站](https://portal.azure.com) → 您的 Foundry <strong>專案</strong> 資源 → **存取控制 (IAM)** → **[角色指派](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)** 分頁。
2. 搜尋您的名稱 → 確認列出 **[Azure AI User](https://aka.ms/foundry-ext-project-role)**。

---

## 3. 了解多代理人概念（Lab 02 新增）

Lab 02 引入 Lab 01 未涵蓋的概念。請在繼續前閱讀以下內容：

### 3.1 甚麼是多代理人工作流程？

多代理人工作流程將工作分散給多個專門代理人，而非由單一代理人承擔所有任務。每個代理人皆有：

- 自己的 <strong>指令</strong>（系統提示）
- 自己的 <strong>角色</strong>（負責的任務）
- 可選的 <strong>工具</strong>（可呼叫的函式）

這些代理人透過一個定義資料流的 <strong>編排圖</strong> 進行溝通。

### 3.2 WorkflowBuilder

來自 `agent_framework` 的 [`WorkflowBuilder`](https://learn.microsoft.com/agent-framework/workflows/agents-in-workflows) 類別是負責將代理人串接起來的 SDK 元件：

```python
from agent_framework import WorkflowBuilder

workflow = (
    WorkflowBuilder(
        name="MyWorkflow",
        start_executor=agent_a,
        output_executors=[agent_d],
    )
    .add_edge(agent_a, agent_b)
    .add_edge(agent_a, agent_c)
    .add_edge(agent_b, agent_d)
    .add_edge(agent_c, agent_d)
    .build()
)
```

- **`start_executor`** - 接收使用者輸入的第一個代理人
- **`output_executors`** - 輸出成為最終回應的代理人們
- **`add_edge(source, target)`** - 定義 `target` 接收 `source` 的輸出

### 3.3 MCP（模型上下文協議）工具

Lab 02 使用一個 **MCP 工具**，它會呼叫 Microsoft Learn API 以取得學習資源。[MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction) 是一種用於連接 AI 模型與外部資料來源及工具的標準化協議。

| 詞彙 | 定義 |
|------|-----------|
| **MCP 伺服器** | 透過 [MCP 協議](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol) 提供工具/資源的服務 |
| **MCP 用戶端** | 您的代理人程式碼，連接並呼叫 MCP 伺服器的工具 |
| **[可串流 HTTP](https://learn.microsoft.com/agent-framework/agents/tools/hosted-mcp-tools)** | 與 MCP 伺服器通訊所使用的傳輸方法 |

### 3.4 Lab 02 與 Lab 01 的差異

| 方面 | Lab 01（單一代理人） | Lab 02（多代理人） |
|--------|----------------------|---------------------|
| 代理人數量 | 1 | 4（專門角色） |
| 編排 | 無 | WorkflowBuilder（平行＋序列） |
| 工具 | 可選的 `@tool` 函式 | MCP 工具（呼叫外部 API） |
| 複雜度 | 簡單提示 → 回應 | 履歷＋職務說明 → 適配分數 → 路線圖 |
| 上下文流 | 直接 | 代理人間交接 |

---

## 4. Lab 02 的工作坊存放庫結構

請確認您知道 Lab 02 的檔案位置：

```
workshop/
└── lab02-multi-agent/
    ├── README.md                       ← Lab overview
    ├── docs/                           ← You are here
    │   ├── README.md                   ← Learning path index
    │   ├── 00-prerequisites.md         ← This file
    │   ├── 01-understand-multi-agent.md
    │   ├── ...
    │   └── 08-troubleshooting.md
    └── PersonalCareerCopilot/          ← The agent project
        ├── agent.yaml                  ← Agent definition
        ├── main.py                     ← 4-agent workflow code
        ├── Dockerfile                  ← Container configuration
        └── requirements.txt            ← Python dependencies
```

---

### 檢查清單

- [ ] 已完整完成 Lab 01（所有 8 個模組，代理人部署並驗證）
- [ ] `az account show` 能回傳您的訂閱資訊
- [ ] 已安裝且可反應的 Microsoft Foundry 及 Foundry Toolkit 擴充功能
- [ ] Foundry 專案中有部署的模型（例如 `gpt-4.1-mini`）
- [ ] 您在該專案擁有 **Azure AI User** 角色
- [ ] 您已閱讀上述多代理人概念章節，且理解 WorkflowBuilder、MCP 及代理人編排

---

**下一步：** [01 - 了解多代理人架構 →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤譯負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->