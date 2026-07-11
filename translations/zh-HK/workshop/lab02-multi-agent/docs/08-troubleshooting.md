# 模組 8 - 疑難排解

本模組涵蓋多代理工作流程中常見錯誤、修復方法及除錯策略。

## 代理輸出問題

### GapAnalyzer 顯示「我仍然沒有匹配的報告」

**症狀：** GapAnalyzer 的回應要求您貼上包含「缺失技能」和「證書缺口」的匹配報告，即使您同時傳送了履歷和職務描述。

**原因：** JD 文字未傳遞到 JD 代理。使用 `context_mode="last_agent"` 時，`resume_executor` 是唯一看到使用者原始訊息的執行者。如果 `RESUME_PARSER_INSTRUCTIONS` 的輸出中未包含 JD 文字，JD 代理無法解析 JD，MatchingAgent 無法計算匹配分數，而 GapAnalyzer 收到的輸入沒有意義。

**診斷：**

在伺服器日誌中查看 MatchingAgent 範圍。若其中：
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
代表傳遞缺失或中斷。

**修復：** 確認 `main.py` 中的 `RESUME_PARSER_INSTRUCTIONS` 包含 `[JOB DESCRIPTION PASS-THROUGH]` 節和規則：
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
也確認 `JOB_DESCRIPTION_INSTRUCTIONS` 包含 `[PARSED RESUME PASS-THROUGH]` 的轉發規則：
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
如其中任一指令區塊為腳手架嚮導的預設範本，請以 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 中的完整版本替換。

### MatchingAgent 輸出「無法計算匹配分數 - 沒有提供 JD」

根本原因同上。MatchingAgent 收到 JD 代理的輸出，但 `[PARSED RESUME PASS-THROUGH]` 區塊缺失或為空，因此無法比較兩個檔案。請確認：
1. `JOB_DESCRIPTION_INSTRUCTIONS` 包含轉發規則：`Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` 告知代理尋找 `[JD REQUIREMENTS]` 和 `[PARSED RESUME PASS-THROUGH]` 區塊。

將兩個指令區塊替換為 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 的完整版本。

### 回應出現兩次

**症狀：** GapAnalyzer 輸出（或整條管線輸出）在代理檢視器回應中重複出現兩次。

**原因：** `WorkflowBuilder` 使用 OR 邏輯語意來處理輸入，任何前驅執行者完成後，下游執行者就會觸發。如果 `matching_executor` 有兩個輸入邊（分別來自 `resume_executor` 和 `jd_executor`），它會觸發兩次：一次是 ResumeParser 結束後，另一次是 JD 代理結束後。接著 GapAnalyzer 也執行兩次。

**修復：** 確保 `WorkflowBuilder` 圖形為嚴格的順序管線，且無合併輸入（fan-in）：

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # 非來自 resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

若有多餘的 `.add_edge(resume_executor, matching_executor)` 代碼行，請刪除。JD 代理輸出中的 `[PARSED RESUME PASS-THROUGH]` 轉發已讓 MatchingAgent 取得履歷。

---

## 環境與配置問題

### 缺失或錯誤的 `.env` 值

`.env` 檔必須位於 `PersonalCareerCopilot/` 目錄中（與 `main.py` 同層）：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

預期的 `.env` 內容：

**路徑 A - Foundry 雲端版：**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**路徑 B - Foundry 本地版：**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> 兩條路徑皆使用 `FOUNDRY_PROJECT_ENDPOINT`，但數值不同：雲端路徑使用帶 `https://` 的 Foundry 端點；本地路徑使用 `http://localhost:5273/v1`。執行 `foundry model list` 確認路徑 B 的精確模型別名。

> **尋找你的 `FOUNDRY_PROJECT_ENDPOINT`：** 
- 在 VS Code 的 **Foundry Toolkit** 側邊欄 → 專案點右鍵 → <strong>複製專案端點</strong>。
- 或至 [Azure Portal](https://portal.azure.com) → 你的 Foundry 專案 → <strong>總覽</strong> → <strong>專案端點</strong>。

> **尋找你的 `AZURE_AI_MODEL_DEPLOYMENT_NAME`：** 在 Foundry Toolkit 側邊欄展開專案 → **Models** → 找出已部署的模型名稱（例如 `gpt-4.1-mini`）。

### 環境變數優先權

`main.py` 使用 `load_dotenv(override=True)`，代表：

| 優先順序 | 來源 | 兩者均設時採用？ |
|----------|--------|-------------------|
| 1 (最高) | `.env` 檔 | 是 |
| 2 | Shell / 容器環境變數 | 當 `.env` 中無相同鍵時使用 |

在本地開發中，這使 `.env` 成為真理來源（編輯 `.env` 立即生效）。託管部署時，Foundry 在容器層注入環境變數；因為此實驗室設定中 `.env` 不包含於映像檔，故以容器注入值為準。

---

## 版本相容性

### 套件版本矩陣

多代理工作流程需要特定套件版本，版本不符會導致運行時錯誤。

| 套件 | 需求版本 | 檢查指令 |
|---------|-------------|-------------|
| `agent-framework-foundry` | 最新版 | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | 最新版 | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | 最新版 | `pip show debugpy` |
| Python | 3.12 以上 | `python --version` |

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

### 部署後容器無法啟動

1. **檢查容器日誌：**
   - 打開 **Foundry Toolkit** 側邊欄 → 展開 **Hosted Agents (Preview)** → 點選你的代理 → 展開版本 → <strong>容器細節</strong> → <strong>日誌</strong>。
   - 尋找 Python 堆疊追蹤或缺少模組錯誤。

2. **常見容器啟動失敗：**

   | 日誌錯誤 | 原因 | 修復方法 |
   |----------|-------|----------|
   | `ModuleNotFoundError` | `requirements.txt` 缺少套件 | 新增套件，重新部署 |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` 或 `.env` 未設定環境變數 | 更新 `agent.yaml` → `environment_variables` 部分（託管）或 `.env`（本地） |
   | `azure.identity.CredentialUnavailableError` | 未設定受管身分 | Foundry 自動設定 - 確保您透過擴充功能部署 |
   | `OSError: port 8088 already in use` | Dockerfile 暴露錯誤端口或端口衝突 | 確認 Dockerfile 中的 `EXPOSE 8088` 與 `CMD ["python", "main.py"]` |
   | 容器以代碼 1 退出 | `main()` 中有未處理例外 | 本地先測試 ([模組 5](05-test-locally.md)) 捕捉錯誤後再部署 |

3. **修正後重新部署：**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → 選擇同一代理 → 部署新版本。

### 部署時間過長

多代理容器啟動較慢，因為啟動時會建立 4 個代理實例。正常啟動時間：

| 階段 | 預期耗時 |
|-------|---------|
| 容器映像建置 | 1-3 分鐘 |
| 映像推送到 ACR | 30-60 秒 |
| 單代理容器啟動 | 15-30 秒 |
| 多代理容器啟動 | 30-120 秒 |
| Playground 中代理可用 | 「啟動完成」後 1-2 分鐘 |

> 若「等待中」狀態持續超過 5 分鐘，請檢查容器日誌是否有錯誤。

---

## RBAC 和權限問題

### `403 Forbidden` 或 `AuthorizationFailed`

你需要在 Foundry 專案中具備 **[Foundry User](https://aka.ms/foundry-ext-project-role)** 角色（先前名為 **Azure AI User**，角色 ID 未變）：

1. 前往 [Azure Portal](https://portal.azure.com) → 你的 Foundry <strong>專案</strong> 資源。
2. 點選 **存取控制 (IAM)** → <strong>角色指派</strong>。
3. 搜尋你的使用者名稱 → 確認有列出 **Foundry User**（或舊版標籤 **Azure AI User**）。
4. 若缺失：點 <strong>新增</strong> → <strong>新增角色指派</strong> → 搜尋 **Foundry User** → 指派給你的帳號。

詳細資訊請參閱 [Microsoft Foundry RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 模型部署無法存取

若代理回傳模型相關錯誤：

1. 驗證模型已部署：Foundry 側邊欄 → 展開專案 → **Models** → 檢查 `gpt-4.1-mini`（或你的模型）狀態為 **Succeeded**。
2. 驗證部署名稱相符：比較 `.env`（或 `agent.yaml`）中 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 與側邊欄中的實際名稱。
3. 若部署過期（免費方案）：從 [模型目錄](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**）。

---

## Foundry 本地版問題（路徑 B）

### Foundry 本地服務未啟動

```powershell
# 檢查狀態
foundry local status

# 如果服務停止，則啟動服務
foundry local start
```

| 症狀 | 原因 | 修復 |
|---------|-------|-----|
| 健康檢查回傳 `503` | 服務未啟動 | 執行 `foundry local start` 或點選 Foundry Toolkit 側邊欄的 **Start** |
| 健康檢查逾時 | 模型尚在載入 | 啟動後等候 30–60 秒；大型模型時間更長 |
| 在 `/v1/health` 回傳 `StatusCode: 404` | 端口錯誤 | 預設為 `5273`。執行 `foundry local status` 查看實際端口 |
| 資源不足 | Foundry Local 需約 4 GB 空閒 RAM | 關閉其他應用程式 |
| 模型下載失敗 | 磁碟空間不足 | 模型大小 2–8 GB。釋放空間後執行 `foundry model pull <name>` |

### 模型名稱不符

```powershell
# 列出已下載的模型及其精確別名
foundry model list
```

將 `.env` 中的 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 設為完全相符的別名（例如 `phi-4-mini`，非 `Phi-4-mini`）。

### 本地運行出現 `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'`（路徑 B）

實驗室的 `main.py` 使用 `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`。Foundry Local 需要該變數指向本地服務，<strong>不可用</strong> `AZURE_AI_PROJECT_ENDPOINT`。請確保 `.env` 含有：

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP 工具仍會發出外部請求（路徑 B）

這是預期的。工具 `search_microsoft_learn_for_plan` 從 `https://learn.microsoft.com/api/mcp` 取得學習資源。<strong>只有技能名稱查詢</strong>會透過網路傳輸—履歷與 JD 文字完全在本地處理，不會傳送出去。若需完整離線操作，請在該工具中加入 `try/except` 例外處理，遇無法到達端點時回傳靜態的 `learn.microsoft.com` URL。

---

## 尋求幫助

若上述修復嘗試後仍卡住：

1. <strong>查看伺服器日誌</strong> - 多數錯誤會在終端機產生 Python 堆疊追蹤。請閱讀完整追蹤。
2. <strong>搜尋錯誤訊息</strong> - 複製錯誤文字並於 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 搜尋。
3. **開啟 Issue** - 在 [workshop 倉庫](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 建立問題，並提供：
   - 錯誤訊息或截圖
   - 你的套件版本（`pip list | Select-String "agent-framework"`）
   - 你的 Python 版本（`python --version`）
   - 問題發生在本地或部署後

---

### 檢查點

- [ ] 你知道如何檢查和修正 `.env` 配置問題
- [ ] 你可以驗證套件版本是否符合需求矩陣
- [ ] 你知道如何檢視容器日誌來排查部署失敗
- [ ] 你能確認 Azure 入口網站中 RBAC 角色設定

---

**上一章：** [07 - 在 Playground 驗證](07-verify-in-playground.md) · **下一章：** [09 - 總結 →](09-summary.md) · **首頁：** [Lab 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->