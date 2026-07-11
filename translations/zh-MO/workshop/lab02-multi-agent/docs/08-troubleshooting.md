# 模組 8 - 疑難排解

本模組涵蓋多代理工作流程中特定的常見錯誤、修正方法與除錯策略。

## 代理輸出問題

### GapAnalyzer 顯示「我仍未收到匹配報告」

**症狀：** GapAnalyzer 的回應要求你貼上包含「缺少技能」與「認證差距」的匹配報告。即使你同時發送了履歷和職位描述，也會出現此情況。

**原因：** 職位描述（JD）文字未傳遞給 JD Agent。使用 `context_mode="last_agent"` 時，`resume_executor` 是唯一看的到使用者原始訊息的執行器。如果 `RESUME_PARSER_INSTRUCTIONS` 沒有在輸出中包含 JD 文字，JD Agent 沒有 JD 可解析，MatchingAgent 無法計算配適分數，GapAnalyzer 收到的是無意義輸入。

**診斷：**

在伺服器日誌中，尋找 MatchingAgent span。若其中包含：
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
傳遞資料遺失或故障。

**修正：** 確認 `main.py` 的 `RESUME_PARSER_INSTRUCTIONS` 內有包含 `[JOB DESCRIPTION PASS-THROUGH]` 區段及規則：
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
同時確認 `JOB_DESCRIPTION_INSTRUCTIONS` 包含 `[PARSED RESUME PASS-THROUGH]` 中繼規則：
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
如果任一指令區塊是從腳手架嚮導產生的占位程式，請將其換成 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 中的完整版本。

### MatchingAgent 輸出「無法計算配適分數 - 未提供職位描述」

此問題與上述相同根因。MatchingAgent 收到了 JD Agent 的輸出，但 `[PARSED RESUME PASS-THROUGH]` 區段遺失或為空，導致無法比對兩個檔案。請確認：
1. `JOB_DESCRIPTION_INSTRUCTIONS` 包含中繼規則：`Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` 指示代理尋找 `[JD REQUIREMENTS]` 與 `[PARSED RESUME PASS-THROUGH]` 區段。

將兩個指令區塊替換成 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 中的完整版本。

### 回應重複出現

**症狀：** GapAnalyzer 輸出（或整個管線輸出）在代理檢查員反應中出現兩次。

**原因：** `WorkflowBuilder` 對進入邊採用 OR 語意 —— 下游執行器一旦有 <strong>任一</strong> 前置任務完成即觸發。如果 `matching_executor` 有兩條進入邊（一條來自 `resume_executor`，一條來自 `jd_executor`），它會觸發兩次：履歷解析完成時一次，JD Agent 完成時一次。GapAnalyzer 也因此執行兩次。

**修正：** 確保 `WorkflowBuilder` 圖形為嚴格順序的管線，且無多重會聚 (fan-in)：

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # 非來自 resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

如果你有多餘的 `.add_edge(resume_executor, matching_executor)` 行，請移除。JD Agent 輸出的 `[PARSED RESUME PASS-THROUGH]` 中繼已經讓 MatchingAgent 能取得履歷。

---

## 環境與設定問題

### 缺少或錯誤的 `.env` 值

`.env` 檔必須放在 `PersonalCareerCopilot/` 目錄 （與 `main.py` 同層）：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

預期 `.env` 內容：

**路徑 A - Foundry 雲端：**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**路徑 B - Foundry 本地端：**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> 兩者皆使用 `FOUNDRY_PROJECT_ENDPOINT`。值不同：雲端使用 `https://` 開頭的 Foundry 端點；本地則用 `http://localhost:5273/v1`。執行 `foundry model list` 來確認路徑 B 的精確模型別名。

> **尋找你的 `FOUNDRY_PROJECT_ENDPOINT`：** 
- 在 VS Code 的 **Foundry Toolkit** 側邊欄 → 右鍵你的專案 → <strong>複製專案端點</strong>。 
- 或前往 [Azure 入口網站](https://portal.azure.com) → 你的 Foundry 專案 → <strong>總覽</strong> → <strong>專案端點</strong>。

> **尋找你的 `AZURE_AI_MODEL_DEPLOYMENT_NAME`：<strong> 在 Foundry Toolkit 側邊欄展開你的專案 → </strong>模型** → 找出已部署的模型名稱（例：`gpt-4.1-mini`）。

### 環境變數優先權

`main.py` 使用 `load_dotenv(override=True)`，代表：

| 優先順序 | 來源 | 兩者皆設時採用？ |
|----------|--------|----------------|
| 1（最高） | `.env` 檔 | 是 |
| 2 | Shell / 容器環境變數 | 當 `.env` 沒有該鍵時使用 |

在本地開發時，設定 `.env` 為真實來源（修改 `.env` 會立即影響執行）。在託管部署時，Foundry 會在容器層注入環境變數；由於 `.env` 不包含於此實驗的部署映像中，因此會使用容器注入的值。

---

## 版本相容性

### 套件版本矩陣

多代理工作流程需要特定版本的套件。版本錯配會造成執行時錯誤。

| 套件 | 需求版本 | 檢查指令 |
|---------|-----------------|---------------|
| `agent-framework-foundry` | 最新版 | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | 最新版 | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | 最新版 | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### 常見版本錯誤

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修正：重新安裝 agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修正：升級 mcp 套件
pip install mcp --upgrade
```

### 一次驗證所有版本

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

預期輸出：

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## 部署問題

### 容器部署後無法啟動

1. **檢查容器日誌：**
   - 開啟 **Foundry Toolkit** 側邊欄 → 展開 **Hosted Agents (Preview)** → 點擊你的代理 → 展開版本 → **Container Details** → **Logs**。
   - 搜尋 Python 堆疊追蹤或缺少模組錯誤。

2. **常見容器啟動失敗原因：**

   | 日誌錯誤 | 原因 | 修正 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` 缺少套件 | 加入該套件，重新部署 |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` 或 `.env` 未設定環境變數 | 更新 `agent.yaml` → `environment_variables` 區段（託管）或 `.env`（本地） |
   | `azure.identity.CredentialUnavailableError` | 未設定 Managed Identity | Foundry 自動設定－確保透過擴充功能部署 |
   | `OSError: port 8088 already in use` | Dockerfile 曝露錯誤埠號或埠號衝突 | 檢查 Dockerfile `EXPOSE 8088` 與 `CMD ["python", "main.py"]` |
   | 容器退出碼 1 | `main()` 中未處理例外 | 先於本地測試（[模組 5](05-test-locally.md)）捕捉錯誤後再部署 |

3. **修正後重新部署：**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → 選擇同一代理 → 部署新版本。

### 部署時間過長

多代理容器啟動時間較長，因為它啟動時會建立 4 個代理實例。一般啟動時間：

| 階段 | 預期持續時間 |
|-------|------------------|
| 容器映像建置 | 1-3 分鐘 |
| 映像推送至 ACR | 30-60 秒 |
| 容器啟動（單一代理） | 15-30 秒 |
| 容器啟動（多代理） | 30-120 秒 |
| Playground 中代理可用 | 「已啟動」後 1-2 分鐘 |

> 若「待命」狀態持續超過 5 分鐘，請檢查容器日誌中的錯誤。

---

## RBAC 與權限問題

### `403 Forbidden` 或 `AuthorizationFailed`

你需要在你的 Foundry 專案上擁有 **[Foundry User](https://aka.ms/foundry-ext-project-role)** 角色（之前稱作 **Azure AI User** — 角色 ID 未變動）：

1. 前往 [Azure 入口網站](https://portal.azure.com) → 你的 Foundry <strong>專案</strong> 資源。
2. 點擊 **存取控制 (IAM)** → <strong>角色分派</strong>。
3. 搜尋你的名字 → 確認已列出 **Foundry User**（或舊稱 **Azure AI User**）。
4. 若缺少：點選 <strong>新增</strong> → <strong>新增角色分派</strong> → 搜尋 **Foundry User** → 指派給你的帳號。

詳情請參閱 [Microsoft Foundry 的 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 文件。

### 模型部署無法存取

若代理回傳模型相關錯誤：

1. 確認模型已部署：Foundry 側邊欄 → 展開專案 → <strong>模型</strong> → 檢查 `gpt-4.1-mini`（或你的模型）狀態為 **Succeeded**。
2. 確認部署名稱匹配：核對 `.env`（或 `agent.yaml`）中的 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 與側邊欄實際部署名稱。
3. 若部署已過期（免費層）：從 [模型目錄](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**）。

---

## Foundry 本地端問題（路徑 B）

### Foundry 本地服務未運行

```powershell
# 檢查狀態
foundry local status

# 如果服務已停止，啟動服務
foundry local start
```

| 症狀 | 原因 | 修正 |
|---------|-------|-----|
| 健康檢查回傳 `503` | 服務未啟動 | 執行 `foundry local start` 或在 Foundry Toolkit 側邊欄點擊 **Start** |
| 健康檢查逾時 | 模型尚在載入 | 啟動後等候 30–60 秒；較大模型需更久 |
| `/v1/health` 回傳 `StatusCode: 404` | 埠號錯誤 | 預設為 `5273`。使用 `foundry local status` 確認實際埠號 |
| 資源不足 | Foundry Local 需約 4 GB 以上空閒 RAM | 關閉其他應用程式 |
| 模型下載失敗 | 磁碟空間不足 | 模型大小 2–8 GB。清理後執行 `foundry model pull <name>` |

### 模型名稱不匹配

```powershell
# 列出已下載的模型及其精確別名
foundry model list
```

在 `.env` 中設定 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 為顯示的精確別名（例：`phi-4-mini`，非 `Phi-4-mini`）。

### 本地執行出現 `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'`（路徑 B）

實驗的 `main.py` 使用 `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`。Foundry Local 需此變數指向本地服務，<strong>不是</strong> `AZURE_AI_PROJECT_ENDPOINT`。請確保你的 `.env` 包含：

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP 工具仍會向外部呼叫（路徑 B）

這是預期行為。`search_microsoft_learn_for_plan` 工具會從 `https://learn.microsoft.com/api/mcp` 取得學習資源。<strong>只有技能名稱的查詢會經網路傳輸</strong>——履歷和 JD 文字完全在你的裝置上處理，且不會被傳輸。若需完全離線使用，請在工具中加入 `try/except` 備援，當端點無法連線時回傳靜態 `learn.microsoft.com` URL。

---

## 尋求協助

若嘗試以上修正後仍卡住：

1. <strong>檢查伺服器日誌</strong> - 大多數錯誤會在終端顯示 Python 堆疊追蹤。詳讀完整追蹤訊息。
2. <strong>搜尋錯誤訊息</strong> - 複製錯誤文字並在 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 搜尋。
3. **開啟 issue** - 在 [工作坊倉庫](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 發起 issue，並提供：
   - 錯誤訊息或截圖
   - 你的套件版本 (`pip list | Select-String "agent-framework"`)
   - 你的 Python 版本 (`python --version`)
   - 問題發生於本地還是部署後

---

### 檢查點

- [ ] 你知道如何檢查與修正 `.env` 配置問題
- [ ] 你能驗證套件版本是否符合需求矩陣
- [ ] 你知道如何檢查容器日誌以找到部署失敗原因
- [ ] 你可以在 Azure 入口網站核對 RBAC 角色設定

---

**上一步：** [07 - 在 Playground 驗證](07-verify-in-playground.md) · **下一步：** [09 - 總結 →](09-summary.md) · **首頁：** [實驗 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->