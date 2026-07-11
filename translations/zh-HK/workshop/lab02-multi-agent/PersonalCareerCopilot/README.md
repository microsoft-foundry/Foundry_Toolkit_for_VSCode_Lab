# PersonalCareerCopilot - 履歷 → 工作匹配評估器

一款以工作流程為先的多代理程式，評估履歷與工作描述的匹配度，並生成個人化的學習路線圖以填補差距。

---

## 代理

| 代理 | 角色 | 工具 |
|-------|------|-------|
| **ResumeParser** | 從履歷文本中提取結構化技能、經驗、認證 | - |
| **JobDescriptionAgent** | 從職務說明中提取必需/優先技能、經驗、認證 | - |
| **MatchingAgent** | 比較履歷與需求 → 匹配分數 (0-100) + 匹配與缺失技能 | - |
| **GapAnalyzer** | 建立個人化學習路線圖，搭配 Microsoft Learn 資源 | `search_microsoft_learn_for_plan` (MCP) |

## 工作流程

```mermaid
flowchart LR
    UserInput["User Input: 簡歷 + 職位描述"] --> ResumeParser
    ResumeParser -- "已解析簡歷 + 職位描述轉發" --> JobDescriptionAgent
    JobDescriptionAgent -- "職位需求 + 簡歷轉發" --> MatchingAgent
    MatchingAgent -- "適配報告 + 差距" --> GapAnalyzerMCP["差距分析器 +\nMicrosoft Learn MCP"]
    GapAnalyzerMCP --> FinalOutput["Final Output:\n適配分數 + 路線圖"]
```

---

## 快速開始

### 1. 設定環境

此資料夾是基於工作流程的 Lab 02 脈絡參考實作。其 `main.py` 使用現有提示塊及 `WorkflowBuilder` 將四個代理連接起來。

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. 配置憑證

在此資料夾建立 `.env` 檔案：

```powershell
copy .env .env.bak 2>$null; echo $null > .env
```

編輯 `.env`：

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| 值 | 尋找位置 |
|-------|------------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Foundry Toolkit 側邊欄 → 右鍵點選專案 → <strong>複製專案端點</strong> |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Foundry 側邊欄 → 展開專案 → **模型 + 端點** → 部署名稱 |

### 3. 本地執行

```powershell
python -m debugpy --listen 127.0.0.1:5679 main.py --port 8088
```

或使用 VS Code 任務：`Ctrl+Shift+P` → **Tasks: Run Task** → **Run Agent HTTP Server**。

若要 F5 除錯，使用 **Debug Local Agent HTTP Server**。

### 4. 使用 Agent Inspector 測試

開啟 Agent Inspector：`Ctrl+Shift+P` → **Foundry Toolkit: Open Agent Inspector**。

貼上此測試提示：

```
Resume:
Jane Doe
Senior Software Engineer with 5 years of experience in Python, Django, and AWS.
Built microservices handling 10K+ requests/second. Led a team of 4 developers.
Certifications: AWS Solutions Architect Associate.
Education: B.S. Computer Science, State University.

Job Description:
Senior Cloud Engineer at Contoso Ltd.
Required: Python, Azure, Kubernetes, Terraform, CI/CD pipelines.
Preferred: Go, monitoring (Prometheus/Grafana), cost optimization.
Experience: 5+ years in cloud infrastructure.
Certifications: Azure Solutions Architect Expert preferred.
```

**預期結果：** 匹配分數 (0-100)、匹配與缺失技能，以及包含 Microsoft Learn 連結的個人化學習路線圖。

### 5. 部署到 Foundry

`Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → 選擇您的專案 → 確認。

---

## 專案結構

```
PersonalCareerCopilot/
├── .env                ← Your credentials (git-ignored)
├── agent.yaml          ← Hosted agent definition (name, resources, env vars)
├── Dockerfile          ← Container image for Foundry deployment
├── main.py             ← 4-agent workflow (instructions, MCP tool, WorkflowBuilder)
└── requirements.txt    ← Python dependencies
```

## 主要檔案

### `agent.yaml`

定義 Foundry Agent Service 的託管代理：
- `kind: hosted` - 作為受管容器執行
- `protocols` - `responses` 通訊協定，版本號 `1.0.0`，公開 `/responses` HTTP 端點
- `environment_variables` - 宣告 `AZURE_AI_MODEL_DEPLOYMENT_NAME`；`FOUNDRY_PROJECT_ENDPOINT` 於部署時自動注入

### `main.py`

包含：
- <strong>代理指令</strong> - 四個 `*_INSTRUCTIONS` 常數，每個代理各一
- **MCP 工具** - `search_microsoft_learn_for_plan()` 透過 Streamable HTTP 呼叫 `https://learn.microsoft.com/api/mcp`
- <strong>代理建立</strong> - 四個 `Agent()` + `AgentExecutor()` 實例共用一個 `FoundryChatClient`
- <strong>工作流程圖</strong> - `WorkflowBuilder` 將代理串成順序管線：ResumeParser → JD Agent → MatchingAgent → GapAnalyzer
- <strong>伺服器啟動</strong> - `ResponsesHostServer` 監聽 8088 埠口

### `requirements.txt`

| 套件 | 功能 |
|---------|----------|
| `agent-framework-foundry` | 核心執行時：`Agent`、`AgentExecutor`、`WorkflowBuilder`、`@tool`、`FoundryChatClient` |
| `agent-framework-foundry-hosting` | `ResponsesHostServer` + Foundry 託管整合 |
| `mcp<2,>=1.24.0` | GapAnalyzer 的 MCP 用戶端 (`streamable_http_client`) |
| `debugpy` | Python 除錯工具（VS Code F5） |

---

## 疑難排解

| 問題 | 解決方法 |
|-------|-----|
| `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` 或 `KeyError: 'AZURE_AI_MODEL_DEPLOYMENT_NAME'` | 建立 `.env`，並設定 `FOUNDRY_PROJECT_ENDPOINT` 與 `AZURE_AI_MODEL_DEPLOYMENT_NAME` |
| `ModuleNotFoundError: No module named 'agent_framework'` | 啟用虛擬環境並執行 `pip install -r requirements.txt` |
| 輸出缺少 Microsoft Learn 連結 | 檢查是否有網路連線至 `https://learn.microsoft.com/api/mcp` |
| 只有一張差距卡（被截斷） | 確認 `GAP_ANALYZER_INSTRUCTIONS` 中包含 `CRITICAL:` 模塊 |
| 埠口 8088 被佔用 | 停用其他服務：`netstat -ano \| findstr :8088` |

詳細疑難排解，請參考 [第 8 單元 - 疑難排解](../docs/08-troubleshooting.md)。

---

**完整導覽：** [Lab 02 文件](../docs/README.md) · **返回：** [Lab 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->