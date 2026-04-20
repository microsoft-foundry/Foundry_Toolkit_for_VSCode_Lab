# Module 8 - 故障排除（多代理）

本模組涵蓋多代理工作流程中特有的常見錯誤、修復方法與除錯策略。針對一般 Foundry 部署問題，亦可參考 [Lab 01 故障排除指南](../../lab01-single-agent/docs/08-troubleshooting.md)。

---

## 快速參考：錯誤 → 修復

| 錯誤 / 症狀 | 可能原因 | 修復 |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | 缺少 `.env` 檔案或變數未設定 | 建立 `.env`，內容為 `PROJECT_ENDPOINT=<your-endpoint>` 和 `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | 虛擬環境未啟用或依賴未安裝 | 執行 `.\.venv\Scripts\Activate.ps1`，接著執行 `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | 未安裝 MCP 套件（`requirements.txt` 缺少） | 執行 `pip install mcp` 或檢查 `requirements.txt` 是否包含作為傳遞依賴 |
| 代理啟動但回應空白 | `output_executors` 不匹配或缺少連接邊 | 確認 `output_executors=[gap_analyzer]` 且所有連接邊均存在於 `create_workflow()` |
| 只有 1 張 gap 卡（其餘缺失） | GapAnalyzer 指示不完整 | 將 `CRITICAL:` 段落加入 `GAP_ANALYZER_INSTRUCTIONS` - 參考 [Module 3](03-configure-agents.md) |
| 適配度（Fit score）為 0 或缺失 | MatchingAgent 未接收到上游資料 | 確認同時存在 `add_edge(resume_parser, matching_agent)` 及 `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP 伺服器拒絕工具呼叫 | 檢查網絡連線。嘗試在瀏覽器開啟 `https://learn.microsoft.com/api/mcp`。重新嘗試 |
| 輸出無 Microsoft Learn URL | MCP 工具未註冊或端點錯誤 | 確認 GapAnalyzer 設定 `tools=[search_microsoft_learn_for_plan]` 及 `MICROSOFT_LEARN_MCP_ENDPOINT` 正確 |
| `Address already in use: port 8088` | 端口 8088 被其他程序佔用 | 執行 `netstat -ano \| findstr :8088`（Windows）或 `lsof -i :8088`（macOS/Linux）並停止衝突程序 |
| `Address already in use: port 5679` | Debugpy 端口衝突 | 停止其他除錯會話。執行 `netstat -ano \| findstr :5679` 找出並終止該程序 |
| Agent Inspector 無法開啟 | 伺服器未完全啟動或端口衝突 | 等待「Server running」日誌。確認端口 5679 空閒 |
| `azure.identity.CredentialUnavailableError` | 未登入 Azure CLI | 執行 `az login` 後重啟伺服器 |
| `azure.core.exceptions.ResourceNotFoundError` | 模型部署不存在 | 檢查 `MODEL_DEPLOYMENT_NAME` 是否與你 Foundry 專案中已部署模型一致 |
| 部署後容器狀態為「Failed」 | 容器啟動時崩潰 | 查看 Foundry 側邊欄容器日誌。常見原因：缺少環境變數或匯入錯誤 |
| 部署狀態顯示「Pending」超過 5 分鐘 | 容器啟動過慢或資源限制 | 多代理建立 4 個 agent 實例，可能要等 5 分鐘。若仍待命，檢查日誌 |
| `ValueError` 來自 `WorkflowBuilder` | 圖形配置無效 | 確保設定了 `start_executor`，`output_executors` 是列表且無循環邊 |

---

## 環境與設定問題

### 缺少或錯誤的 `.env` 變數

`.env` 檔案必須放在 `PersonalCareerCopilot/` 目錄（與 `main.py` 同層）：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

預期的 `.env` 內容：

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **查找你的 PROJECT_ENDPOINT：**  
- 開啟 VS Code 中的 **Microsoft Foundry** 側邊欄 → 右鍵點擊你的專案 → 選擇 **Copy Project Endpoint**。  
- 或連至 [Azure Portal](https://portal.azure.com) → 你的 Foundry 專案 → <strong>總覽</strong> → **Project endpoint**。

> **查找你的 MODEL_DEPLOYMENT_NAME：** 在 Foundry 側邊欄展開專案 → **Models** → 找到已部署的模型名稱（如 `gpt-4.1-mini`）。

### 環境變數優先順序

`main.py` 使用 `load_dotenv(override=False)`，代表：

| 優先級 | 來源 | 兩者均設置時誰優先？ |
|----------|--------|------------------------|
| 1（最高） | Shell 環境變數 | 優先使用 |
| 2 | `.env` 檔案 | 僅 shell 變數未設時使用 |

這表示在託管部署時，Foundry 運行時的環境變數（透過 `agent.yaml` 設定）優先於 `.env`。

---

## 版本相容性

### 套件版本矩陣

多代理工作流程要求特定版本的套件。版本不符會導致執行時錯誤。

| 套件 | 需求版本 | 檢查指令 |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | 最新預發版 | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### 常見版本錯誤

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修正：升級到 rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**找不到 `agent-dev-cli` 或 Inspector 不相容：**

```powershell
# 修正：使用 --pre 標誌安裝
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修正：升級 mcp 套件
pip install mcp --upgrade
```

### 一次驗證所有版本

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

預期輸出：

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## MCP 工具問題

### MCP 工具無回傳結果

**症狀：** Gap 卡顯示「No results returned from Microsoft Learn MCP」或「No direct Microsoft Learn results found」。

**可能原因：**

1. <strong>網路問題</strong> - MCP 端點 (`https://learn.microsoft.com/api/mcp`) 無法連線。  
   ```powershell
   # 測試連接性
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   若回傳 `200`，代表端點可連。

2. <strong>查詢過於特定</strong> - 技能名稱太專門，Microsoft Learn 搜尋無結果。  
   - 對非常專門技能屬預期行為，工具回應中含有後備 URL。

3. **MCP 連線逾時** - Streamable HTTP 連接超時。  
   - 重試請求。MCP 連線是短暫會話，可能需重連。

### MCP 日誌說明

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| 日誌 | 含意 | 措施 |
|-----|---------|--------|
| `GET → 405` | MCP 用戶端初始化探測 | 正常 - 忽略 |
| `POST → 200` | 工具呼叫成功 | 預期 |
| `DELETE → 405` | MCP 用戶端清理探測 | 正常 - 忽略 |
| `POST → 400` | 錯誤請求（查詢格式錯誤） | 檢查 `search_microsoft_learn_for_plan()` 中 `query` 參數 |
| `POST → 429` | 請求被限制 | 等待並重試。減少 `max_results` 參數 |
| `POST → 500` | MCP 伺服器錯誤 | 暫時性錯誤 - 重試。若持續，Microsoft Learn MCP API 可能當機 |
| 連線逾時 | 網路問題或 MCP 伺服器無法使用 | 檢查網路，嘗試 `curl https://learn.microsoft.com/api/mcp` |

---

## 部署問題

### 部署後容器無法啟動

1. **查看容器日誌：**  
   - 開啟 **Microsoft Foundry** 側邊欄 → 展開 **Hosted Agents (Preview)** → 點擊你的代理 → 展開版本 → **Container Details** → **Logs**。  
   - 尋找 Python 堆疊追蹤或缺少模組錯誤。

2. **常見容器啟動失敗：**

   | 日誌錯誤 | 原因 | 修復 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` 缺少套件 | 加入套件並重新部署 |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` 未設定環境變數 | 更新 `agent.yaml` → `environment_variables` 欄位 |
   | `azure.identity.CredentialUnavailableError` | 沒有配置 Managed Identity | Foundry 自動設定，確保透過擴充套件部署 |
   | `OSError: port 8088 already in use` | Dockerfile 曝露錯誤端口或端口衝突 | 確認 Dockerfile 中 `EXPOSE 8088` 和 `CMD ["python", "main.py"]` |
   | 容器以代碼 1 結束 | `main()` 有未處理例外 | 本地先測試（[Module 5](05-test-locally.md)），及早捕捉錯誤 |

3. **修正後重新部署：**  
   - 按下 `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → 選擇同一代理 → 部署新版本。

### 部署時間過長

多代理容器啟動時間較長，因為啟動時會建立 4 個代理實例。正常啟動時間：

| 階段 | 預期時間 |
|-------|------------------|
| 容器映像建構 | 1-3 分鐘 |
| 映像推送至 ACR | 30-60 秒 |
| 容器啟動（單代理） | 15-30 秒 |
| 容器啟動（多代理） | 30-120 秒 |
| Playground 中代理可用 | 「Started」後 1-2 分鐘 |

> 若「Pending」狀態超過 5 分鐘，請查看容器日誌確認錯誤。

---

## RBAC 與權限問題

### `403 Forbidden` 或 `AuthorizationFailed`

你需要在 Foundry 專案中擁有 **[Azure AI 使用者](https://aka.ms/foundry-ext-project-role)** 角色：

1. 前往 [Azure Portal](https://portal.azure.com) → 找到你的 Foundry <strong>專案</strong> 資源。  
2. 點選 **Access control (IAM)** → **角色指派（Role assignments）**。  
3. 搜尋你的名稱 → 確認有列出 **Azure AI User**。  
4. 若沒有：點選 <strong>新增</strong> → <strong>新增角色指派</strong> → 搜尋 **Azure AI User** → 指派到你的帳號。

詳見 [Microsoft Foundry 的 RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 模型部署無法訪問

若代理回報模型相關錯誤：

1. 確認模型已部署：Foundry 側邊欄 → 展開專案 → **Models** → 查看 `gpt-4.1-mini`（或你的模型）狀態為 **Succeeded**。  
2. 確認部署名稱相符：比對 `.env`（或 `agent.yaml`）中的 `MODEL_DEPLOYMENT_NAME` 與側邊欄的實際部署名稱。  
3. 若部署過期（免費層）：從 [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**）。

---

## Agent Inspector 問題

### Inspector 開啟但顯示「Disconnected」

1. 確認伺服器正在運行：終端機中尋找「Server running on http://localhost:8088」。  
2. 檢查端口 `5679`：Inspector 透過 debugpy 連接此端口。  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. 重啟伺服器並重新開啟 Inspector。

### Inspector 顯示不完整回應

多代理回應長且會逐步串流產生。請等待完整回應結束（視 gap 卡與 MCP 工具呼叫數量，需 30-60 秒）。

若回應持續截斷：  
- 確認 GapAnalyzer 指示包含阻止合併 gap 卡的 `CRITICAL:` 區塊。  
- 檢查模型 Token 限制 —— `gpt-4.1-mini` 支援最高 32K 輸出 Tokens，通常足夠。

---

## 效能建議

### 回應速度慢

多代理工作流程因多階段依賴與 MCP 工具呼叫，本質上比單代理慢。

| 優化 | 說明 | 效果 |
|-------------|-----|--------|
| 減少 MCP 呼叫次數 | 降低工具中的 `max_results` 參數 | 減少 HTTP 網路往返次數 |
| 簡化指示 | 縮短且聚焦代理提示詞 | 提升 LLM 推理速率 |
| 使用 `gpt-4.1-mini` | 研發階段比 `gpt-4.1` 快 | 約 2 倍速度提升 |
| 減少 gap 卡細節 | 在 GapAnalyzer 指示中簡化 gap 卡格式 | 產出負擔減輕 |

### 典型回應時間（本地）

| 配置 | 預期時間 |
|--------------|---------------|
| `gpt-4.1-mini`，3-5 張 gap 卡 | 30-60 秒 |
| `gpt-4.1-mini`，8 張以上 gap 卡 | 60-120 秒 |
| `gpt-4.1`，3-5 張 gap 卡 | 60-120 秒 |
---

## 尋求協助

如果您在嘗試上述修復後仍然遇到問題：

1. <strong>檢查伺服器日誌</strong> - 大部分錯誤會在終端機產生 Python 堆疊追蹤。請詳讀完整追蹤內容。
2. <strong>搜尋錯誤訊息</strong> - 複製錯誤文字並在 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 搜尋。
3. <strong>開啟問題回報</strong> - 在 [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 提交問題，並附上：
   - 錯誤訊息或截圖
   - 您的套件版本 (`pip list | Select-String "agent-framework"`)
   - 您的 Python 版本 (`python --version`)
   - 問題是發生在本地還是部署後

---

### 核對清單

- [ ] 您能使用快速參考表識別並修正最常見的多代理錯誤
- [ ] 您知道如何檢查及修正 `.env` 配置問題
- [ ] 您能確認套件版本符合需求矩陣
- [ ] 您了解 MCP 日誌紀錄，並能診斷工具故障原因
- [ ] 您知道如何檢查容器日誌以找出部署失敗原因
- [ ] 您能在 Azure 入口網站驗證 RBAC 角色設定

---

**上一節：** [07 - 在 Playground 驗證](07-verify-in-playground.md) · **首頁：** [實驗室 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力確保準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原文文件的母語版本應被視為權威來源。對於重要資訊，建議由專業人工翻譯完成。我們不對因使用此翻譯而產生的任何誤解或誤譯負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->