# Module 8 - 疑難排解（多代理人）

本模組涵蓋多代理人工作流程特有的常見錯誤、修復方法及除錯策略。關於一般 Foundry 部署問題，請參閱[實驗室 01 疑難排解指南](../../lab01-single-agent/docs/08-troubleshooting.md)。

---

## 快速參考：錯誤 → 修復

| 錯誤 / 症狀 | 可能原因 | 修復方法 |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` 檔案遺失或未設定值 | 建立 `.env`，內容包含 `PROJECT_ENDPOINT=<your-endpoint>` 與 `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | 未啟用虛擬環境或未安裝相依性 | 執行 `.\.venv\Scripts\Activate.ps1` 後執行 `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP 套件未安裝（requirements 缺項） | 執行 `pip install mcp` 或檢查 `requirements.txt` 是否包含該套件作為傳遞相依性 |
| 代理人啟動但回傳空白回應 | `output_executors` 不匹配或缺少邊線 | 確認 `output_executors=[gap_analyzer]` 且所有邊線存在於 `create_workflow()` 中 |
| 只顯示 1 個 gap 卡（其餘消失） | GapAnalyzer 指令不完整 | 將 `CRITICAL:` 段落加入 `GAP_ANALYZER_INSTRUCTIONS` - 詳見[模組 3](03-configure-agents.md) |
| 適配分數為 0 或不存在 | MatchingAgent 未接收到上游資料 | 確認存在 `add_edge(resume_parser, matching_agent)` 和 `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP 伺服器拒絕工具呼叫 | 檢查網路連線，嘗試在瀏覽器開啟 `https://learn.microsoft.com/api/mcp`，重試 |
| 輸出中無 Microsoft Learn URL | MCP 工具未註冊或端點錯誤 | 確認 GapAnalyzer 使用 `tools=[search_microsoft_learn_for_plan]` 且 `MICROSOFT_LEARN_MCP_ENDPOINT` 正確 |
| `Address already in use: port 8088` | 其他程序佔用 8088 埠 | 執行 `netstat -ano \| findstr :8088`（Windows）或 `lsof -i :8088`（macOS/Linux）並停止佔用程序 |
| `Address already in use: port 5679` | Debugpy 埠衝突 | 停止其他除錯工作階段。執行 `netstat -ano \| findstr :5679` 找出並結束該程序 |
| Agent Inspector 無法開啟 | 伺服器尚未完全啟動或埠衝突 | 等待「Server running」日誌訊息，檢查 5679 埠是否空閒 |
| `azure.identity.CredentialUnavailableError` | 未登入 Azure CLI | 執行 `az login` 後重新啟動伺服器 |
| `azure.core.exceptions.ResourceNotFoundError` | 模型部署不存在 | 檢查 `MODEL_DEPLOYMENT_NAME` 是否與 Foundry 專案中已部署模型相符 |
| 部署後容器狀態為「Failed」 | 容器啟動時崩潰 | 檢查 Foundry 側邊欄容器日誌。常見錯誤：缺少環境變數或匯入錯誤 |
| 部署顯示「Pending」超過 5 分鐘 | 容器啟動太久或資源限制 | 多代理會建立 4 個代理實例，等待最多 5 分鐘，若持續 Pending，請檢查日誌 |
| `ValueError` 出自 `WorkflowBuilder` | 圖形配置錯誤 | 確保設定了 `start_executor`，`output_executors` 為列表，且無循環邊線 |

---

## 環境與設定問題

### 遺失或錯誤的 `.env` 值

`.env` 檔必須放在 `PersonalCareerCopilot/` 目錄（與 `main.py` 同層級）：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

預期 `.env` 內容：

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **尋找您的 PROJECT_ENDPOINT：**  
- 在 VS Code 中開啟 **Microsoft Foundry** 側邊欄 → 對您的專案右鍵 → **Copy Project Endpoint**。  
- 或前往 [Azure 入口網站](https://portal.azure.com) → 您的 Foundry 專案 → <strong>總覽</strong> → **Project endpoint**。

> **尋找您的 MODEL_DEPLOYMENT_NAME：**  
在 Foundry 側邊欄展開專案 → **Models** → 找到您已部署的模型名稱（例如 `gpt-4.1-mini`）。

### 環境變數優先權

`main.py` 使用 `load_dotenv(override=False)`，表示：

| 優先權 | 來源 | 兩者同時設定時哪個生效？ |
|----------|--------|------------------------|
| 1（最高） | Shell 環境變數 | 生效 |
| 2 | `.env` 檔 | 只有當 shell 變數無設定時生效 |

這表示 Foundry 執行環境變數（透過 `agent.yaml` 設定）在佈署時優先於 `.env`。

---

## 版本相容性

### 套件版本矩陣

多代理人工作流程需要指定的套件版本。不匹配會導致執行時錯誤。

| 套件 | 要求版本 | 檢查指令 |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | 最新預釋出版本 | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### 常見版本錯誤

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修正：升級到 rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**找不到 `agent-dev-cli` 或 Inspector 不相容：**

```powershell
# 修正：使用 --pre 參數安裝
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

### MCP 工具未回傳結果

**症狀：** Gap 卡顯示「No results returned from Microsoft Learn MCP」或「No direct Microsoft Learn results found」。

**可能原因：**

1. <strong>網路問題</strong> - MCP 端點（`https://learn.microsoft.com/api/mcp`）無法連線。  
   ```powershell
   # 測試連線
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
  如果此命令回傳 `200`，端點可達。

2. <strong>查詢過於狹窄</strong> - 技能名稱太過專業化，Microsoft Learn 搜尋無相符。  
   - 對非常專門技能屬正常。工具會在回應附帶後備 URL。

3. **MCP 會話逾時** - Streamable HTTP 連線逾時。  
   - 請重試。MCP 會話為暫存，可能需重新連線。

### MCP 日誌說明

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| 日誌 | 含意 | 措施 |
|-----|---------|--------|
| `GET → 405` | MCP 用戶端初始化時的探測 | 正常 - 可忽略 |
| `POST → 200` | 工具呼叫成功 | 預期結果 |
| `DELETE → 405` | MCP 用戶端清理時探測 | 正常 - 可忽略 |
| `POST → 400` | 請求錯誤（語法錯誤查詢） | 檢查 `search_microsoft_learn_for_plan()` 中的 `query` 參數 |
| `POST → 429` | 過快限制 | 等待並重試。減少 `max_results` 參數 |
| `POST → 500` | MCP 伺服器錯誤 | 臨時錯誤，重試。若持續，Microsoft Learn MCP API 可能故障 |
| 連線逾時 | 網路問題或 MCP 伺服器無回應 | 檢查網路。嘗試 `curl https://learn.microsoft.com/api/mcp` |

---

## 部署問題

### 容器部署後無法啟動

1. **檢查容器日誌：**  
   - 開啟 **Microsoft Foundry** 側邊欄 → 展開 **Hosted Agents (Preview)** → 點選您的代理人 → 展開版本 → **Container Details** → **Logs**。  
   - 尋找 Python stacktrace 或缺少模組錯誤。

2. **常見容器啟動失敗：**

   | 日誌錯誤 | 原因 | 修復 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` 遺漏套件 | 新增套件並重新部署 |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` 未設定環境變數 | 更新 `agent.yaml` 的 `environment_variables` 區塊 |
   | `azure.identity.CredentialUnavailableError` | 未配置 Managed Identity | Foundry 會自動設置，確保透過擴充模組佈署 |
   | `OSError: port 8088 already in use` | Dockerfile 暴露錯誤埠或埠衝突 | 驗證 Dockerfile 的 `EXPOSE 8088` 和 `CMD ["python", "main.py"]` |
   | 容器以代碼 1 退出 | `main()` 未捕捉例外 | 先在本地測試 ([模組 5](05-test-locally.md)) 捕捉錯誤後再佈署 |

3. **修正後重新部署：**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → 選擇同一代理人 → 部署新版本。

### 部署耗時過長

多代理人容器啟動較久，因啟動時會建立 4 個代理人實例。正常啟動時間：

| 階段 | 預期時間 |
|-------|------------------|
| 容器映像建置 | 1-3 分鐘 |
| 映像推送至 ACR | 30-60 秒 |
| 容器啟動（單代理人） | 15-30 秒 |
| 容器啟動（多代理人） | 30-120 秒 |
| Playground 中代理人可用 | 「Started」訊息後 1-2 分鐘 |

> 若「Pending」狀態持續超過 5 分鐘，請檢查容器日誌錯誤。

---

## RBAC 與權限問題

### `403 Forbidden` 或 `AuthorizationFailed`

您必須具備 Foundry 專案中的 **[Azure AI User](https://aka.ms/foundry-ext-project-role)** 角色：

1. 前往 [Azure 入口網站](https://portal.azure.com) → 您的 Foundry <strong>專案</strong> 資源。  
2. 點選 **存取控制 (IAM)** → <strong>角色指派</strong>。  
3. 搜尋您的姓名 → 確認 **Azure AI User** 是否列在其中。  
4. 若缺少：點選 <strong>新增</strong> → <strong>新增角色指派</strong> → 搜尋 **Azure AI User** → 指派給您的帳號。

詳情請參閱 [Microsoft Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 文件。

### 模型部署無法存取

若代理人回傳模型相關錯誤：

1. 確認模型已部署：Foundry 側邊欄 → 展開專案 → **Models** → 確認有 `gpt-4.1-mini`（或您的模型）且狀態為 **Succeeded**。  
2. 確認部署名稱一致：比對 `.env`（或 `agent.yaml`）中的 `MODEL_DEPLOYMENT_NAME` 與側邊欄顯示部署名稱。  
3. 若部署過期（免費版）：從[模型目錄](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**）。

---

## Agent Inspector 問題

### Inspector 開啟卻顯示「Disconnected」

1. 確認伺服器已啟動：終端機中尋找「Server running on http://localhost:8088」。  
2. 檢查埠號 `5679`：Inspector 透過 debugpy 連線該埠。  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. 重新啟動伺服器並重開 Inspector。

### Inspector 顯示回應不完整

多代理人回應較長且會分段串流。請等待完整回應（視 gap 卡數量與 MCP 工具呼叫可能需 30-60 秒）。

若回應持續截斷：  
- 檢查 GapAnalyzer 指令是否包含防止合併 gap 卡的 `CRITICAL:` 區塊。  
- 檢查模型 Token 限制 — `gpt-4.1-mini` 支援最高 32K 輸出 Token，應足夠使用。

---

## 效能技巧

### 回應過慢

多代理人工作流程本質上較單代理人慢，因為有序依賴與 MCP 工具呼叫。

| 優化策略 | 作法 | 影響 |
|-------------|-----|--------|
| 減少 MCP 呼叫 | 降低工具的 `max_results` 參數 | 減少 HTTP 往返次數 |
| 簡化指令 | 簡短且聚焦的代理人提示 | 加快大型語言模型推論 |
| 使用 `gpt-4.1-mini` | 比 `gpt-4.1` 開發更快 | 約 2 倍速度提升 |
| 簡化 gap 卡細節 | 在 GapAnalyzer 指令中簡化 gap 卡格式 | 輸出較少，生成更快 |

### 典型本地回應時間

| 配置 | 預期時間 |
|--------------|---------------|
| `gpt-4.1-mini`，3-5 張 gap 卡 | 30-60 秒 |
| `gpt-4.1-mini`，8 張以上 gap 卡 | 60-120 秒 |
| `gpt-4.1`，3-5 張 gap 卡 | 60-120 秒 |
---

## 尋求協助

如果您在嘗試上述修復後仍遇到困難：

1. <strong>檢查伺服器日誌</strong> - 大多數錯誤會在終端機中產生 Python 堆疊追蹤。請閱讀完整的追蹤內容。
2. <strong>搜尋錯誤訊息</strong> - 複製錯誤文字並在 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 中搜尋。
3. <strong>開啟議題</strong> - 在 [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 中提交議題，內容包括：
   - 錯誤訊息或螢幕截圖
   - 您的套件版本 (`pip list | Select-String "agent-framework"`)
   - 您的 Python 版本 (`python --version`)
   - 問題是發生在本機還是部署後

---

### 檢查清單

- [ ] 您能使用快速參考表識別並修復最常見的多代理錯誤
- [ ] 您知道如何檢查並修復 `.env` 設定問題
- [ ] 您能驗證套件版本是否符合需求矩陣
- [ ] 您了解 MCP 日誌條目並能診斷工具失敗問題
- [ ] 您知道如何檢查容器日誌以排查部署失敗
- [ ] 您能在 Azure 入口網站中驗證 RBAC 角色

---

**前一章節：** [07 - Playground 中驗證](07-verify-in-playground.md) · **首頁：** [實驗室 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意自動翻譯可能包含錯誤或不準確的內容。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用此翻譯而產生的任何誤解或誤譯負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->