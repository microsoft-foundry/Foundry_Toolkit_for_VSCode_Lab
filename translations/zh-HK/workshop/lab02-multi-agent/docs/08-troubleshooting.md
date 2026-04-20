# Module 8 - 疑難排解（多代理）

本單元涵蓋多代理工作流程中特有的常見錯誤、修復方法與除錯策略。一般 Foundry 部署問題，請參考同時參考[實驗室 01 疑難排解指南](../../lab01-single-agent/docs/08-troubleshooting.md)。

---

## 快速參考：錯誤 → 修復

| 錯誤 / 症狀 | 可能原因 | 修復方法 |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` 檔案遺失或值未設定 | 建立 `.env`，內容為 `PROJECT_ENDPOINT=<your-endpoint>` 與 `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | 未啟動虛擬環境或未安裝相依項 | 執行 `.\.venv\Scripts\Activate.ps1` 後再執行 `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | 未安裝 MCP 套件（requirements 缺漏） | 執行 `pip install mcp` 或確認 `requirements.txt` 已納入該套件作為傳遞相依 |
| 代理啟動卻回傳空回應 | `output_executors` 不匹配或缺少邊 | 確認 `output_executors=[gap_analyzer]` 且所有邊均存在於 `create_workflow()` |
| 只有 1 張 gap 卡（其餘缺失） | GapAnalyzer 指令不完整 | 在 `GAP_ANALYZER_INSTRUCTIONS` 補充 `CRITICAL:` 段落 - 參見[單元 3](03-configure-agents.md) |
| 適配分數為 0 或缺失 | MatchingAgent 未收到上游資料 | 確認存在 `add_edge(resume_parser, matching_agent)` 和 `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP 伺服器拒絕工具呼叫 | 檢查網路連線。嘗試用瀏覽器開啟 `https://learn.microsoft.com/api/mcp` 並重試 |
| 輸出中無 Microsoft Learn URL | MCP 工具未註冊或端點錯誤 | 確認 GapAnalyzer 設定中有 `tools=[search_microsoft_learn_for_plan]` 且 `MICROSOFT_LEARN_MCP_ENDPOINT` 正確 |
| `Address already in use: port 8088` | 另一程序佔用 8088 埠口 | 執行 `netstat -ano \| findstr :8088`（Windows）或 `lsof -i :8088`（macOS/Linux）並終止衝突程序 |
| `Address already in use: port 5679` | Debugpy 埠口衝突 | 停止其他調試會話。執行 `netstat -ano \| findstr :5679` 查找並終止程序 |
| 代理檢視器無法開啟 | 伺服器尚未完全啟動或埠口衝突 | 等待 "Server running" 日誌訊息。檢查 5679 埠口可用 |
| `azure.identity.CredentialUnavailableError` | 未登入 Azure CLI | 執行 `az login` 並重啟伺服器 |
| `azure.core.exceptions.ResourceNotFoundError` | 模型部署不存在 | 確認 `MODEL_DEPLOYMENT_NAME` 與 Foundry 專案中的已部署模型名稱相符 |
| 部署後容器狀態顯示「失敗」 | 容器啟動時崩潰 | 檢查 Foundry 側邊欄的容器日誌。常見原因：缺少環境變數或匯入錯誤 |
| 部署顯示「待處理」超過 5 分鐘 | 容器啟動過久或資源限制 | 多代理啟動時會建立 4 個代理實例，請等待最多 5 分鐘，仍未成功請檢查日誌 |
| `ValueError` 出自 `WorkflowBuilder` | 圖配置無效 | 確保設定了 `start_executor`，`output_executors` 是列表，且無環狀邊 |

---

## 環境與設定問題

### `.env` 值缺失或錯誤

`.env` 檔案必須放置於 `PersonalCareerCopilot/` 目錄（與 `main.py` 同層）：

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
  
> **尋找 PROJECT_ENDPOINT：**  
- 在 VS Code 開啟 **Microsoft Foundry** 側邊欄 → 對你的專案點右鍵 → **Copy Project Endpoint**。  
- 或前往 [Azure Portal](https://portal.azure.com) → 你的 Foundry 專案 → **Overview** → **Project endpoint**。

> **尋找 MODEL_DEPLOYMENT_NAME：** 在 Foundry 側邊欄展開專案 → **Models** → 找到已部署的模型名稱（例如 `gpt-4.1-mini`）。

### 環境變數優先順序

`main.py` 透過 `load_dotenv(override=False)` 載入，代表：

| 優先序 | 來源 | 同時都設置時哪個優先？ |
|----------|--------|------------------------|
| 1（最高） | Shell 環境變數 | 優先 shell 變數 |
| 2 | `.env` 檔案 | 如 shell 變數未設置才生效 |

這表示在 Hosted 部署期間，以 Foundry 運行環境變數（由 `agent.yaml` 設定）優先於 `.env`。

---

## 版本相容性

### 套件版本矩陣

多代理工作流程需要特定套件版本，版本不符會造成執行錯誤。

| 套件 | 需求版本 | 檢查指令 |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | 最新預發布版 | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### 常見版本錯誤

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修正：升級到 rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```
  
**`agent-dev-cli` 未找到或 Inspector 不相容：**

```powershell
# 修正：使用 --pre 標誌安裝
pip install agent-dev-cli --pre --upgrade
```
  
**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修正：升級mcp套件
pip install mcp --upgrade
```
  
### 一次確認所有版本

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

### MCP 工具不回傳結果

**症狀：** Gap 卡顯示「No results returned from Microsoft Learn MCP」或「No direct Microsoft Learn results found」。

**可能原因：**

1. <strong>網路問題</strong> — MCP 端點（`https://learn.microsoft.com/api/mcp`）無法連線。  
   ```powershell
   # 測試連線
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
  若此返回 `200`，表示端點可達。

2. <strong>查詢過於特定</strong> — 技能名稱對 Microsoft Learn 搜尋過於冷門。  
   - 對非常專門的技能這是預期行為。工具回應中有備用 URL。

3. **MCP 會話逾時** — Streamable HTTP 連線超時。  
   - 請重試請求。MCP 會話是短暫的，可能需要重連。

### MCP 日誌解讀

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```
  
| 記錄 | 含意 | 動作 |
|-----|---------|--------|
| `GET → 405` | MCP 用戶端初始化時的探測 | 正常 - 可忽略 |
| `POST → 200` | 工具呼叫成功 | 預期行為 |
| `DELETE → 405` | MCP 用戶端清理時的探測 | 正常 - 可忽略 |
| `POST → 400` | 請求錯誤（錯誤格式查詢） | 檢查 `search_microsoft_learn_for_plan()` 中 `query` 參數 |
| `POST → 429` | 超出速率限制 | 等待後重試。可調降 `max_results` 參數 |
| `POST → 500` | MCP 伺服器錯誤 | 臨時現象，重試。若持續，可能 Microsoft Learn MCP API 當機 |
| 連線逾時 | 網路問題或 MCP 伺服器不可用 | 檢查網路。嘗試 `curl https://learn.microsoft.com/api/mcp` |

---

## 部署問題

### 部署後容器啟動失敗

1. **檢查容器日誌：**  
   - 打開 **Microsoft Foundry** 側邊欄 → 展開 **Hosted Agents (Preview)** → 點選你的代理 → 展開版本 → **Container Details** → **Logs**。  
   - 查找 Python 堆疊追蹤或缺少模組錯誤。

2. **常見容器啟動失敗原因：**

   | 日誌錯誤 | 原因 | 修正 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` 少套件 | 補充套件，重新部署 |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` 未設定所需環境變數 | 更新 `agent.yaml` → `environment_variables` 區塊 |
   | `azure.identity.CredentialUnavailableError` | 尚未配置受管身份 | Foundry 會自動設定 - 請確定用擴充功能部署 |
   | `OSError: port 8088 already in use` | Dockerfile 指定錯誤埠口或埠口衝突 | 確認 Dockerfile 中有正確 `EXPOSE 8088` 及 `CMD ["python", "main.py"]` |
   | 容器以代碼 1 退出 | `main()` 中有未捕捉例外 | 先本地測試 ([單元 5](05-test-locally.md))，部署前捕捉錯誤 |

3. **修正後重新部署：**  
   - 按 `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → 選擇同一代理 → 部署新版本。

### 部署花費過久

多代理容器啟動需花較長時間，因為會建立 4 個代理實例。正常啟動時間：

| 階段 | 預期耗時 |
|-------|------------------|
| 容器映像建立 | 1-3 分鐘 |
| 傳送映像至 ACR | 30-60 秒 |
| 容器啟動（單代理） | 15-30 秒 |
| 容器啟動（多代理） | 30-120 秒 |
| Playground 代理可用 | 於「Started」後 1-2 分鐘 |

> 若「Pending」狀態逾 5 分鐘，請檢查容器日誌是否有錯誤。

---

## RBAC 與權限問題

### `403 Forbidden` 或 `AuthorizationFailed`

你必須擁有 Foundry 專案的 **[Azure AI User](https://aka.ms/foundry-ext-project-role)** 角色：

1. 前往 [Azure Portal](https://portal.azure.com) → 找到你的 Foundry <strong>專案</strong> 資源。
2. 點選 **Access control (IAM)** → **Role assignments**。
3. 搜尋你的名稱 → 確認清單中有 **Azure AI User**。
4. 若缺少：按 **Add** → **Add role assignment** → 搜尋 **Azure AI User** → 指派給你的帳號。

詳情請參見 [Microsoft Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 文件。

### 模型部署無法存取

若代理回傳模型相關錯誤：

1. 確認模型已部署：Foundry 側邊欄 → 展開專案 → **Models** → 檢查 `gpt-4.1-mini`（或你的模型）狀態為 **Succeeded**。
2. 確認部署名稱吻合：比對 `.env`（或 `agent.yaml`）中 `MODEL_DEPLOYMENT_NAME` 與側邊欄實際部署名稱。
3. 若部署已過期（免費層）：從 [模型目錄](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**）。

---

## 代理檢視器問題

### 檢視器開啟但顯示「Disconnected」

1. 確認伺服器正在運行：檢查終端機是否有 "Server running on http://localhost:8088"。
2. 檢查 5679 埠口：Inspector 透過 debugpy 使用該埠口連線。  
   ```powershell
   netstat -ano | findstr :5679
   ```
  
3. 重啟伺服器並重新開啟 Inspector。

### 檢視器顯示部分回應

多代理回應內容龐大且會流式漸進輸出。請等待完整回應完成（依 gap 卡數量與 MCP 呼叫可能需 30-60 秒）。

若回應持續截斷：  
- 確認 GapAnalyzer 指令中有 `CRITICAL:` 區塊，用以避免合併 gap 卡。  
- 檢查模型的 Token 限制，`gpt-4.1-mini` 支援最高 32K 輸出 Token，應足夠。

---

## 效能小貼士

### 回應緩慢

多代理工作流程因順序依賴與 MCP 呼叫本質較慢，優化建議：

| 優化 | 方法 | 影響 |
|-------------|-----|--------|
| 減少 MCP 呼叫 | 降低工具中 `max_results` 參數 | 減少 HTTP 往返 |
| 精簡指令 | 縮短且聚焦代理提示 | 提升大型語言模型推論速度 |
| 使用 `gpt-4.1-mini` | 開發時較 `gpt-4.1` 快速 | 約 2 倍速度提升 |
| 減少 gap 卡細節 | 在 GapAnalyzer 指令中簡化 gap 卡格式 | 輸出量減少 |

### 典型回應時間（本機）

| 設定 | 預期耗時 |
|--------------|---------------|
| `gpt-4.1-mini`，3-5 張 gap 卡 | 30-60 秒 |
| `gpt-4.1-mini`，8 張以上 gap 卡 | 60-120 秒 |
| `gpt-4.1`，3-5 張 gap 卡 | 60-120 秒 |
---

## 尋求協助

如果你嘗試上述修正後仍然卡住：

1. <strong>檢查伺服器日誌</strong> - 大多數錯誤會在終端機中產生 Python 堆疊追蹤。請閱讀完整追蹤紀錄。
2. <strong>搜尋錯誤訊息</strong> - 複製錯誤文字並在 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 搜尋。
3. <strong>開啟議題</strong> - 在[工作坊倉庫](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues)提交議題，內容包括：
   - 錯誤訊息或截圖
   - 你的套件版本 (`pip list | Select-String "agent-framework"`)
   - 你的 Python 版本 (`python --version`)
   - 問題是本地還是部署後發生

---

### 核心檢查點

- [ ] 你可以使用快速參考表識別並修復最常見的多代理錯誤
- [ ] 你知道如何檢查並修復 `.env` 配置問題
- [ ] 你可以驗證套件版本是否符合需求矩陣
- [ ] 你了解 MCP 日誌條目，並能診斷工具故障
- [ ] 你知道如何檢查容器日誌以確認部署失敗原因
- [ ] 你可以在 Azure 入口網站驗證 RBAC 角色

---

**上一單元：** [07 - Playground 驗證](07-verify-in-playground.md) · **首頁：** [實驗室 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於翻譯的準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->