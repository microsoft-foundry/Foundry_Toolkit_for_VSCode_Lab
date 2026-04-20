# PersonalCareerCopilot - 履歷 → 工作適配評估器

一個多智能代理工作流程，用以評估履歷與職位描述的匹配程度，然後生成個人化學習路線圖以彌補差距。

---

## 代理

| 代理 | 角色 | 工具 |
|-------|------|-------|
| **ResumeParser** | 從履歷文字中提取結構化的技能、經驗、證書 | - |
| **JobDescriptionAgent** | 從職位描述中提取所需/優先技能、經驗、證書 | - |
| **MatchingAgent** | 比較個人資料與要求 → 適配分數 (0-100) + 匹配/缺失技能 | - |
| **GapAnalyzer** | 使用 Microsoft Learn 資源建立個人化學習路線圖 | `search_microsoft_learn_for_plan` (MCP) |

## 工作流程

```mermaid
flowchart TD
    UserInput["用戶輸入：履歷 + 工作描述"] --> ResumeParser
    UserInput --> JobDescriptionAgent
    ResumeParser --> MatchingAgent
    JobDescriptionAgent --> MatchingAgent
    MatchingAgent --> GapAnalyzerMCP["差距分析器 &
    Microsoft Learn 文件 MCP"]
    GapAnalyzerMCP --> FinalOutput["最終輸出：
     適合度得分 + 路線圖"]
```
---

## 快速開始

### 1. 設定環境

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. 配置認證

複製範例環境檔，並填寫您的 Foundry 專案詳情：

```powershell
cp .env.example .env
```

編輯 `.env`：

```env
PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| 值 | 位置 |
|-------|-----------------|
| `PROJECT_ENDPOINT` | Microsoft Foundry 側邊欄於 VS Code → 右鍵點選您的專案 → <strong>複製專案端點</strong> |
| `MODEL_DEPLOYMENT_NAME` | Foundry 側邊欄 → 展開專案 → **模型 + 端點** → 部署名稱 |

### 3. 本地運行

```powershell
python -m debugpy --listen 127.0.0.1:5679 -m agentdev run main.py --verbose --port 8088
```

或使用 VS Code 任務：`Ctrl+Shift+P` → **任務: 執行任務** → **執行 Lab02 HTTP 伺服器**。

### 4. 使用 Agent Inspector 測試

打開 Agent Inspector：`Ctrl+Shift+P` → **Foundry 工具組: 開啟 Agent Inspector**。

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

**預期：** 一個適配分數（0-100）、匹配/缺失技能，及含有 Microsoft Learn URL 的個人化學習路線圖。

### 5. 部署至 Foundry

`Ctrl+Shift+P` → **Microsoft Foundry: 部署託管代理** → 選擇您的專案 → 確認。

---

## 專案結構

```
PersonalCareerCopilot/
├── .env.example        ← Template for environment variables
├── .env                ← Your credentials (git-ignored)
├── agent.yaml          ← Hosted agent definition (name, resources, env vars)
├── Dockerfile          ← Container image for Foundry deployment
├── main.py             ← 4-agent workflow (instructions, MCP tool, WorkflowBuilder)
└── requirements.txt    ← Python dependencies
```

## 主要檔案

### `agent.yaml`

定義 Foundry Agent 服務的託管代理：
- `kind: hosted` - 以管理容器型態運行
- `protocols: [responses v1]` - 暴露 `/responses` HTTP 端點
- `environment_variables` - 部署時注入 `PROJECT_ENDPOINT` 與 `MODEL_DEPLOYMENT_NAME`

### `main.py`

包含：
- <strong>代理指令</strong> - 四個 `*_INSTRUCTIONS` 常數，每個代理一個
- **MCP 工具** - `search_microsoft_learn_for_plan()` 通過 Streamable HTTP 調用 `https://learn.microsoft.com/api/mcp`
- <strong>代理建立</strong> - 使用 `AzureAIAgentClient.as_agent()` 的 `create_agents()` 上下文管理器
- <strong>工作流程圖</strong> - `create_workflow()` 利用 `WorkflowBuilder` 以分支/匯合/序列模式連接代理
- <strong>伺服器啟動</strong> - `from_agent_framework(agent).run_async()` 在 8088 埠運行

### `requirements.txt`

| 套件 | 版本 | 用途 |
|---------|---------|---------|
| `agent-framework-azure-ai` | `1.0.0rc3` | 微軟代理框架的 Azure AI 整合 |
| `agent-framework-core` | `1.0.0rc3` | 核心執行環境（含 WorkflowBuilder） |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | 託管代理服務執行環境 |
| `azure-ai-agentserver-core` | `1.0.0b16` | 核心代理服務抽象層 |
| `debugpy` | 最新版 | Python 除錯（VS Code 中 F5） |
| `agent-dev-cli` | `--pre` | 本地開發 CLI + Agent Inspector 後端 |

---

## 疑難排解

| 問題 | 解決方法 |
|-------|-----|
| `RuntimeError: Missing required environment variable(s)` | 建立 `.env`，包含 `PROJECT_ENDPOINT` 與 `MODEL_DEPLOYMENT_NAME` |
| `ModuleNotFoundError: No module named 'agent_framework'` | 啟用虛擬環境並執行 `pip install -r requirements.txt` |
| 輸出中沒有 Microsoft Learn URL | 檢查與 `https://learn.microsoft.com/api/mcp` 的網路連線 |
| 只有 1 張差距卡（顯示截斷） | 確認 `GAP_ANALYZER_INSTRUCTIONS` 包含 `CRITICAL:` 區塊 |
| 埠 8088 被佔用 | 停止其他伺服器：`netstat -ano \| findstr :8088` |

詳細疑難排解，請參閱 [Module 8 - 疑難排解](../docs/08-troubleshooting.md)。

---

**完整操作指南：** [Lab 02 文件](../docs/README.md) · **返回：** [Lab 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件是使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 所翻譯。雖然我們力求準確，但請注意自動翻譯可能包含錯誤或不準確之處。原文件的母語版本應視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對使用此翻譯所引起的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->