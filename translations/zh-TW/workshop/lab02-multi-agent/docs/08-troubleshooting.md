# 模組 8 - 疑難排解

本模組涵蓋多代理工作流程中特有的常見錯誤、修正方法與除錯策略。

## 代理輸出問題

### GapAnalyzer 顯示「我仍然沒有匹配的報告」

**症狀：** GapAnalyzer 的回應要求你貼上一份包含「缺少技能」和「認證差距」的匹配報告。即使你已經傳送了履歷和工作描述，仍會發生此狀況。

**原因：** JD 文字未傳遞給 JD 代理。在 `context_mode="last_agent"` 模式下，只有 `resume_executor` 能看到使用者的原始訊息。如果 `RESUME_PARSER_INSTRUCTIONS` 沒有在輸出中包含 JD 文字，JD 代理就沒有工作描述可解析，MatchingAgent 無法計算配合度分數，GapAnalyzer 收到的則是無意義的輸入。

**診斷：**

在伺服器日誌中，尋找 MatchingAgent 的 span。如果它包含：
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
 傳遞中斷或遺失。

**修正：** 確認 `main.py` 中的 `RESUME_PARSER_INSTRUCTIONS` 包含 `[JOB DESCRIPTION PASS-THROUGH]` 區段及以下規則：
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
 並確認 `JOB_DESCRIPTION_INSTRUCTIONS` 包含 `[PARSED RESUME PASS-THROUGH]` 的轉送規則：
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
 若任一指令區段為腳手架精靈提供的樣板，請用 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 中的完整版本替換。

### MatchingAgent 輸出「無法計算配合度 - 未提供工作描述」

原因與前述相同。MatchingAgent 收到 JD 代理的輸出，但 `[PARSED RESUME PASS-THROUGH]` 區段缺失或為空，無法比較兩個履歷。請確認：
1. `JOB_DESCRIPTION_INSTRUCTIONS` 包含轉送規則：`逐字複製 [PARSED RESUME] - Matching Agent 下游依賴此規則。`
2. `MATCHING_AGENT_INSTRUCTIONS` 指示代理尋找 `[JD REQUIREMENTS]` 和 `[PARSED RESUME PASS-THROUGH]` 區段。

以 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 中的完整版本替換兩個指令區段。

### 回應出現兩次

**症狀：** GapAnalyzer 的輸出（或整個流程輸出）在 Agent Inspector 回應中顯示兩次。

**原因：** `WorkflowBuilder` 對輸入邊使用 OR 語義——只要有<strong>任意一個</strong>前置節點完成，下游執行器即觸發。如果 `matching_executor` 有兩個輸入邊（來自 `resume_executor` 和 `jd_executor`），它會被觸發兩次：一次是 ResumeParser 完成後，另一次是 JD 代理完成後。GapAnalyzer 也因此執行兩次。

**修正：** 確保 `WorkflowBuilder` 的圖是嚴格序列化的管線，且無匯合（fan-in）：

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # 不是來自 resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

如果有多餘的 `.add_edge(resume_executor, matching_executor)` 行，將其刪除。JD 代理輸出的 `[PARSED RESUME PASS-THROUGH]` 轉送已經讓 MatchingAgent 能訪問履歷。

---

## 環境與設定問題

### 缺少或錯誤的 `.env` 變數

`.env` 檔必須位於 `PersonalCareerCopilot/` 目錄（與 `main.py` 同級）：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

預期的 `.env` 內容：

**路徑 A - Foundry 雲端：**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**路徑 B - Foundry 本地：**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> 兩種路徑皆使用 `FOUNDRY_PROJECT_ENDPOINT`，值不同：雲端使用 `https://` 的 Foundry 端點；本地使用 `http://localhost:5273/v1`。執行 `foundry model list` 以確認路徑 B 的模型別名。

> **如何取得你的 `FOUNDRY_PROJECT_ENDPOINT`：** 
- 在 VS Code 的 **Foundry Toolkit** 側邊欄 → 右鍵點擊你的專案 → <strong>複製專案端點</strong>。 
- 或前往 [Azure Portal](https://portal.azure.com) → 你的 Foundry 專案 → <strong>總覽</strong> → <strong>專案端點</strong>。

> **如何取得你的 `AZURE_AI_MODEL_DEPLOYMENT_NAME`：<strong> 在 Foundry Toolkit 側邊欄展開你的專案 → </strong>模型** → 查找已部署的模型名稱（例如 `gpt-4.1-mini`）。

### 環境變數優先順序

`main.py` 使用 `load_dotenv(override=True)`，意即：

| 優先級 | 來源 | 兩者皆設時哪個生效？ |
|-------|------|---------------------|
| 1 (最高) | `.env` 檔案 | 是 |
| 2 | Shell / 容器環境變數 | 當 `.env` 中無相同鍵時使用 |

在本地開發時，`.env` 是唯一真相來源（編輯 `.env` 會立即生效）。在託管部署時，Foundry 會在容器級別注入環境變數；由於 `.env` 未包含於部署映像中，因此採用注入的容器值。

---

## 版本相容性

### 套件版本矩陣

多代理工作流程要求特定套件版本。版本不匹配會導致執行時錯誤。

| 套件 | 需用版本 | 檢查指令 |
|------|---------|-----------|
| `agent-framework-foundry` | 最新版 | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | 最新版 | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | 最新版 | `pip show debugpy` |
| Python | 3.12 以上 | `python --version` |

### 常見版本錯誤

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修復：重新安裝 agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修正：升級 mcp 套件
pip install mcp --upgrade
```

### 一次檢查所有版本

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
   - 打開 **Foundry Toolkit** 側邊欄 → 展開 **Hosted Agents (Preview)** → 點選你的代理 → 展開版本 → <strong>容器詳細資料</strong> → <strong>日誌</strong>。
   - 查找 Python 堆疊追蹤或缺少模組錯誤。

2. **常見容器啟動失敗原因：**

   | 日誌錯誤 | 原因 | 解決方法 |
   |---------|------|----------|
   | `ModuleNotFoundError` | `requirements.txt` 缺少套件 | 新增套件並重新部署 |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` 或 `.env` 缺少環境變數 | 更新 `agent.yaml` → `environment_variables` (託管) 或 `.env` (本地) |
   | `azure.identity.CredentialUnavailableError` | 未設定 Managed Identity | Foundry 會自動設置 - 確認是透過擴充功能部署 |
   | `OSError: port 8088 already in use` | Dockerfile 暴露錯誤端口或端口衝突 | 確認 Dockerfile 中 `EXPOSE 8088` 及 `CMD ["python", "main.py"]` |
   | 容器以代碼 1 退出 | `main()` 未處理例外 | 先在本地測試（參見 [模組 5](05-test-locally.md)）以捕捉錯誤 |

3. **修復後重新部署：**
   - 按下 `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → 選擇相同代理 → 部署新版本。

### 部署耗時過久

多代理容器啟動時間較長，因為它在啟動時會建立 4 個代理實例。一般啟動時間：

| 階段 | 預期耗時 |
|------|----------|
| 容器映像建置 | 1-3 分鐘 |
| 映像推送至 ACR | 30-60 秒 |
| 容器啟動（單一代理） | 15-30 秒 |
| 容器啟動（多代理） | 30-120 秒 |
| 代理在 Playground 可用 | 在「Started」後 1-2 分鐘 |

> 若「待處理」狀態超過 5 分鐘，請檢查容器日誌是否有錯誤。

---

## RBAC 與權限問題

### `403 Forbidden` 或 `AuthorizationFailed`

你需要在 Foundry 專案上具有 **[Foundry User](https://aka.ms/foundry-ext-project-role)** 角色（先前稱為 **Azure AI User** - 角色 ID 不變）：

1. 前往 [Azure Portal](https://portal.azure.com) → 專案資源。
2. 點選 **存取控制 (IAM)** → <strong>角色分配</strong>。
3. 搜尋你的名字 → 確認列有 **Foundry User**（或舊稱 **Azure AI User**）。
4. 若缺失：點選 <strong>新增</strong> → <strong>新增角色分派</strong> → 搜尋 **Foundry User** → 指派給你的帳戶。

詳情請參見 [Microsoft Foundry 的 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 文件。

### 模型部署無法存取

若代理回傳模型相關錯誤：

1. 確認模型已部署：Foundry 側邊欄 → 展開專案 → <strong>模型</strong> → 檢查 `gpt-4.1-mini`（或你的模型）狀態為 **Succeeded**。
2. 確認部署名稱匹配：比對 `.env`（或 `agent.yaml`）中 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 與實際側邊欄中的部署名稱。
3. 如部署過期（免費方案）：從 [模型目錄](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（按 `Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**）。

---

## Foundry 本地問題（路徑 B）

### Foundry 本地服務未啟動

```powershell
# 檢查狀態
foundry local status

# 如果服務已停止，則啟動服務
foundry local start
```

| 症狀 | 原因 | 解決方法 |
|------|------|----------|
| 健康檢查回傳 `503` | 服務未啟動 | 執行 `foundry local start` 或在 Foundry Toolkit 側邊欄點選 **Start** |
| 健康檢查超時 | 模型仍在載入 | 啟動後等待 30-60 秒；較大模型需要較久時間 |
| `/v1/health` 顯示 `StatusCode: 404` | 端口錯誤 | 預設為 `5273`。執行 `foundry local status` 查詢實際端口 |
| 資源不足 | Foundry Local 需約 4 GB RAM 空閒 | 關閉其他程式 |
| 模型下載失敗 | 磁碟空間不足 | 模型大小 2–8 GB。釋放空間後執行 `foundry model pull <name>` |

### 模型名稱不匹配

```powershell
# 列出已下載的模型及其精確別名
foundry model list
```

將 `.env` 中的 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 設為顯示的正確別名（如 `phi-4-mini`，注意大小寫須一致，不是 `Phi-4-mini`）。

### 本地執行時出現 `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` （路徑 B）

實驗室的 `main.py` 使用 `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`。Foundry Local 需要此變數指向本地服務，而非 `AZURE_AI_PROJECT_ENDPOINT`。請確保你的 `.env` 包含：

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP 工具仍進行外部呼叫（路徑 B）

此為預期行為。`search_microsoft_learn_for_plan` 工具會從 `https://learn.microsoft.com/api/mcp` 抓取學習資源。<strong>只有技能名稱查詢會透過網路傳送</strong>—履歷與工作描述文字完全在本機處理，絕不傳輸。如需完全離線操作，可在該工具加入 `try/except` 附加機制，當端點無法存取時回傳靜態的 `learn.microsoft.com` URL。

---

## 尋求幫助

若嘗試上述修正後仍遇困難：

1. <strong>檢查伺服器日誌</strong> - 多數錯誤會在終端機產生 Python 堆疊追蹤。詳細閱讀堆疊資訊。
2. <strong>搜尋錯誤訊息</strong> - 複製錯誤文本，至 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 搜尋。
3. **開啟 Issue** - 在 [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 提交問題，附上：
   - 錯誤訊息或截圖
   - 你的套件版本 (`pip list | Select-String "agent-framework"`)
   - 你的 Python 版本 (`python --version`)
   - 問題發生於本地或部署後

---

### 檢查點

- [ ] 你知道如何檢查與修正 `.env` 設定問題
- [ ] 你能驗證套件版本符合需求矩陣
- [ ] 你知道如何查看容器日誌以排查部署失敗
- [ ] 你能在 Azure Portal 核對 RBAC 角色設定

---

**上一章：** [07 - 在 Playground 驗證](07-verify-in-playground.md) · **下一章：** [09 - 總結 →](09-summary.md) · **首頁：** [實驗室 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->