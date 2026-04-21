# Module 2 - 架構多代理專案

在本模組中，您將使用 [Microsoft Foundry extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) <strong>架構多代理工作流程專案</strong>。此擴充套件會產生整個專案結構──`agent.yaml`、`main.py`、`Dockerfile`、`requirements.txt`、`.env` 以及除錯設定。接著，您會在模組 3 和 4 中自訂這些檔案。

> **注意：** 本實驗室中的 `PersonalCareerCopilot/` 資料夾是已完成且可運作的自訂多代理專案範例。您可以自行架構全新專案（建議用於學習）或直接研究現有程式碼。

---

## 步驟 1：開啟建立託管代理精靈

```mermaid
flowchart LR
    S1["開啟嚮導
    Ctrl+Shift+P"]
    S2["選擇範本
    多代理工作流程"]
    S3["語言
    Python"]
    S4["模型
    gpt-4.1-mini"]
    S5["資料夾及名稱
    resume-job-fit-evaluator"]
    S6["腳手架
    檔案已生成"]

    S1 --> S2 --> S3 --> S4 --> S5 --> S6

    style S1 fill:#3498DB,stroke:#2C3E50,color:#fff
    style S2 fill:#7B68EE,stroke:#2C3E50,color:#fff
    style S3 fill:#9B59B6,stroke:#2C3E50,color:#fff
    style S4 fill:#E67E22,stroke:#2C3E50,color:#fff
    style S5 fill:#F39C12,stroke:#2C3E50,color:#fff
    style S6 fill:#27AE60,stroke:#2C3E50,color:#fff
```
1. 按下 `Ctrl+Shift+P` 開啟 <strong>指令選擇器</strong>。
2. 輸入：**Microsoft Foundry: Create a New Hosted Agent** 並選取它。
3. 託管代理建立精靈隨即開啟。

> **替代方法：** 點擊活動列中的 **Microsoft Foundry** 圖示 → 點擊 **Agents** 旁的 **+** 圖示 → **Create New Hosted Agent**。

---

## 步驟 2：選擇多代理工作流程範本

精靈會讓您選擇範本：

| 範本 | 說明 | 適用時機 |
|----------|-------------|-------------|
| 單一代理 | 一個代理帶有指令及可選工具 | 實驗室 01 |
| <strong>多代理工作流程</strong> | 多個代理透過 WorkflowBuilder 協作 | **本實驗室 (實驗室 02)** |

1. 選擇 <strong>多代理工作流程</strong>。
2. 點擊 <strong>下一步</strong>。

![Wizard template selection showing Multi-Agent Workflow option highlighted](../../../../../translated_images/zh-MO/02-wizard-template-selection.b781f67331789bed.webp)

---

## 步驟 3：選擇程式語言

1. 選擇 **Python**。
2. 點擊 <strong>下一步</strong>。

---

## 步驟 4：選擇您的模型

1. 精靈會顯示您 Foundry 專案中部署的模型。
2. 選擇您在實驗室 01 中使用的相同模型（例如 **gpt-4.1-mini**）。
3. 點擊 <strong>下一步</strong>。

> **小提示：** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series) 是建議用於開發的模型──速度快、成本低，且適合多代理工作流程。若要獲得較高品質輸出，可於最終正式部署時切換到 `gpt-4.1`。

---

## 步驟 5：選擇資料夾位置及代理名稱

1. 會跳出檔案對話方塊。選擇目標資料夾：
   - 若跟著工作坊儲存庫操作：前往 `workshop/lab02-multi-agent/` 並建立新子資料夾
   - 若從頭開始：選擇任意資料夾
2. 輸入託管代理的 <strong>名稱</strong>（例如 `resume-job-fit-evaluator`）。
3. 點擊 <strong>建立</strong>。

---

## 步驟 6：等待架構完成

1. VS Code 會開啟新視窗（或更新現有視窗），顯示已架構的專案。
2. 您應該會看到此檔案結構：

```
resume-job-fit-evaluator/
├── .env                ← Environment variables (placeholders)
├── .vscode/
│   └── launch.json     ← Debug configuration
├── agent.yaml          ← Agent definition (kind: hosted)
├── Dockerfile          ← Container configuration
├── main.py             ← Multi-agent workflow code (scaffold)
└── requirements.txt    ← Python dependencies
```

> **工作坊提示：** 工作坊儲存庫的 `.vscode/` 資料夾位於 <strong>工作區根目錄</strong>，並包含共用的 `launch.json` 和 `tasks.json`。實驗室 01 與實驗室 02 都包含除錯設定。按下 F5 時，從下拉選單中選擇 **"Lab02 - Multi-Agent"**。

---

## 步驟 7：了解架構檔案（多代理特有）

多代理架構與單一代理架構在幾個重要方面有所不同：

### 7.1 `agent.yaml` - 代理定義

```yaml
kind: hosted
name: resume-job-fit-evaluator
description: >
  A multi-agent workflow that evaluates resume-to-job fit.
metadata:
  authors:
    - Microsoft
  tags:
    - Multi-Agent Workflow
    - Resume Evaluator
protocols:
  - protocol: responses
    version: v1
environment_variables:
  - name: PROJECT_ENDPOINT
    value: ${PROJECT_ENDPOINT}
  - name: MODEL_DEPLOYMENT_NAME
    value: ${MODEL_DEPLOYMENT_NAME}
```

**與實驗室 01 主要差異：** `environment_variables` 區塊可能包含額外的 MCP 端點或其他工具設定變數。`name` 及 `description` 反映多代理使用案例。

### 7.2 `main.py` - 多代理工作流程程式碼

此架構檔包括：
- <strong>多個代理操作說明字串</strong>（每個代理一個常數）
- **多個 [`AzureAIAgentClient.as_agent()`](https://learn.microsoft.com/python/api/overview/azure/ai-agents-readme) 區塊管理器**（每個代理一個）
- **[`WorkflowBuilder`](https://learn.microsoft.com/agent-framework/workflows/agents-in-workflows)** 用以串接代理
- **`from_agent_framework()`** 用來作為 HTTP 端點提供工作流程服務

```python
from agent_framework import WorkflowBuilder, tool
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
```

相較於實驗室 01，多了導入 [`WorkflowBuilder`](https://learn.microsoft.com/agent-framework/workflows/agents-in-workflows)。

### 7.3 `requirements.txt` - 額外相依套件

多代理專案使用與實驗室 01 相同基底套件，另加 MCP 相關套件：

```
agent-framework-azure-ai==1.0.0rc3
agent-framework-core==1.0.0rc3
azure-ai-agentserver-agentframework==1.0.0b16
azure-ai-agentserver-core==1.0.0b16
debugpy
agent-dev-cli --pre
```

> **重要版本注意：** `agent-dev-cli` 套件在 `requirements.txt` 內需使用 `--pre` 旗標以安裝最新版預覽版本。此作法為確保 Agent Inspector 與 `agent-framework-core==1.0.0rc3` 兼容。版本詳情請參考 [模組 8 - 疑難排解](08-troubleshooting.md)。

| 套件 | 版本 | 作用 |
|---------|---------|---------|
| [`agent-framework-azure-ai`](https://learn.microsoft.com/agent-framework/overview/) | `1.0.0rc3` | Microsoft Agent Framework 的 Azure AI 整合 |
| [`agent-framework-core`](https://learn.microsoft.com/agent-framework/overview/) | `1.0.0rc3` | 核心執行環境（含 WorkflowBuilder） |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | 託管代理伺服器執行環境 |
| `azure-ai-agentserver-core` | `1.0.0b16` | 代理伺服器核心抽象層 |
| `debugpy` | 最新版 | Python 除錯工具（VS Code F5 使用） |
| `agent-dev-cli` | `--pre` | 本地開發 CLI 及 Agent Inspector 後端 |

### 7.4 `Dockerfile` - 與實驗室 01 相同

Dockerfile 與實驗室 01 完全相同──複製檔案、安裝 `requirements.txt` 中依賴、開放 8088 埠口、執行 `python main.py`。

```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY ./ .
RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    else \
      echo "No requirements.txt found" >&2; exit 1; \
    fi
EXPOSE 8088
CMD ["python", "main.py"]
```

---

### 檢查點

- [ ] 完成架構精靈 → 新專案結構顯示
- [ ] 可以看到所有檔案：`agent.yaml`、`main.py`、`Dockerfile`、`requirements.txt`、`.env`
- [ ] `main.py` 中有導入 `WorkflowBuilder`（確認選擇多代理範本）
- [ ] `requirements.txt` 中包含 `agent-framework-core` 和 `agent-framework-azure-ai`
- [ ] 理解多代理架構與單代理架構異同（多代理、WorkflowBuilder、MCP 工具）

---

**上一節：** [01 - 了解多代理架構](01-understand-multi-agent.md) · **下一節：** [03 - 配置代理及環境 →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件經由人工智能翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原文之母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->