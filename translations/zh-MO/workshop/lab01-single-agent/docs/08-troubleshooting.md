# 模組 8 - 疑難排解

此模組為常見問題參考指南。請加書籤並於發生問題時回來查看。

---

## 1. 權限錯誤

### 1.1 拒絕 `agents/write` 權限

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**根本原因：** 缺少在 <strong>專案</strong> 級別的 `Azure AI User` 角色。這是工作坊最常見的錯誤。

**解決方法：**
1. 開啟 [portal.azure.com](https://portal.azure.com)。
2. 搜尋您的 Foundry <strong>專案</strong> 名稱 → 點擊類型為 **「Microsoft Foundry project」** 的結果（非上層帳戶）。
3. **存取控制 (IAM)** → **+ 新增** → <strong>新增角色指派</strong>。
4. 角色：**Azure AI User** → 下一步。
5. 成員：選取自己 → 審查 + 指派 → 審查 + 指派。
6. **等待 1-2 分鐘** → 再試一次。

> **為何擁有者/貢獻者角色不夠：** 這些角色只授予<em>管理</em>操作。代理程序作業需要 `agents/write` <em>資料操作</em>，此操作僅包含於 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner`。詳見 [Foundry RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 佈建時出現 `AuthorizationFailed`

**解決方法：** 請管理員在資源群組上指派 **Contributor** 角色，或由他們建立專案並授予您 **Azure AI User** 角色。

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# 等待直到：「已登記」
```

---

## 2. Docker 錯誤

> Docker 為<strong>選用</strong>。以下僅適用於已安裝 Docker Desktop 且擴充功能嘗試本地構建的情況。

### 2.1 Docker 服務未運行

**解決方法：** 啟動 Docker Desktop → 等待顯示「運行中」狀態 → 用 `docker info` 驗證 → 重試。

### 2.2 依賴錯誤導致建置失敗

**解決方法：** 驗證 `requirements.txt` 拼寫，先在本地測試：`pip install -r requirements.txt`。

### 2.3 平台不符（Apple Silicon）

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. 認證錯誤

### 3.1 `DefaultAzureCredential` 失敗

**解決方法（依序嘗試）：**
1. `az login`（重新認證）
2. `az account set --subscription "<id>"`（設定正確訂閱）
3. VS Code → 帳戶 → 登出 → 再登入
4. 驗證：`az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 本地 Token 有效，託管時無效

**預期行為：** 託管代理使用系統管理的身分識別，而非您的憑證。若託管代理收到認證錯誤：
- 驗證 `agent.yaml` 內的 `AZURE_AI_PROJECT_ENDPOINT` 是否正確
- 確認專案的管理身分識別已獲得模型存取權

---

## 4. 模型錯誤

### 4.1 找不到模型部署

**解決方法：** 名稱<strong>大小寫敏感</strong>。比對 `.env` 中 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 與 Foundry 側欄 → 模型中的確切名稱。

### 4.2 模型輸出異常

**解決方法：** 檢查 `main.py` 中的 `AGENT_INSTRUCTIONS`（是否被截斷？）。嘗試不同模型（如 `gpt-4.1` 與 `gpt-4.1-mini`）。

---

## 5. 部署錯誤

### 5.1 ACR 拉取未授權

**解決方法：** Azure 入口網站 → 容器登錄 → 存取控制 (IAM) → 新增 **AcrPull** 角色給 Foundry 專案的管理身分識別。

### 5.2 代理無法啟動（持續顯示「待命」或「失敗」）

檢查側欄中的容器日誌。常見原因：

| 日誌訊息 | 解決方法 |
|-------------|-----|
| `ModuleNotFoundError` | 將缺少的套件加入 `requirements.txt`，重新部署 |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | 在 `agent.yaml` 的 `environment_variables` 中新增環境變數 |
| `Address already in use` | 確保只有一個進程綁定埠號 8088 |

### 5.3 部署逾時

**解決方法：** 檢查網路連線。第一次部署會推送超過 100MB。若位於代理伺服器後方，請設定 Docker Desktop 代理設定。

---

## 6. 路徑 B - Foundry Local

### 6.1 Foundry Local 無法啟動

| 問題 | 解決方法 |
|-------|-----|
| `foundry: command not found` | 重新安裝：`winget install Microsoft.FoundryLocal` |
| 資源不足 | Foundry Local 需要約 4GB 可用記憶體。關閉其他應用程式。 |
| 模型下載失敗 | 檢查磁碟空間（模型大小為 2–8 GB）。重試：`foundry local models pull <name>` |

### 6.2 Foundry Local 模型錯誤

| 問題 | 解決方法 |
|-------|-----|
| 回應緩慢 | 預期內 - 本地模型在 CPU 上運行，除非您有 GPU。請耐心等待。 |
| 輸出品質差 | 若硬體允許，嘗試較大型模型。`phi-4-mini` 是良好平衡選擇。 |
| 連線被拒 | 驗證 Foundry Local 正在運行：`foundry local status`。若需要，重新啟動。 |

---

## 7. 快速參考：RBAC 角色

| 角色 | 範圍 | 授權內容 |
|------|-------|--------|
| **Azure AI User** | 專案 | 資料操作：`agents/write`、`agents/read` |
| **Azure AI Developer** | 專案/帳戶 | 資料操作 + 創建專案 |
| **Azure AI Owner** | 帳戶 | 完全存取 + 角色管理 |
| **Contributor** | 訂閱/資源群組 | 僅管理操作（<strong>無</strong>資料操作） |
| **Owner** | 訂閱/資源群組 | 管理 + 角色指派（<strong>無</strong>資料操作） |

---

## 8. 工作坊完成檢查清單

| 編號 | 項目 | 模組 |
|---|------|--------|
| 1 | 安裝並驗證先決條件 | [00](00-prerequisites.md) |
| 2 | 安裝 Foundry Toolkit 擴充功能，連接專案（或設定路徑 B） | [01](01-setup.md) |
| 3 | 託管代理腳手架完成 | [02](02-create-hosted-agent.md) |
| 4 | 已設定 `.env`，撰寫指令，安裝相依性 | [03](03-configure-and-code.md) |
| 5 | 本地代理測試完成 - 三個功能場景通過 | [04](04-test-locally.md) |
| 6 | 部署到 Foundry（僅路徑 A） | [05](05-deploy-to-foundry.md) |
| 7 | 雲端邊緣狀況/安全性測試通過（僅路徑 A） | [06](06-verify-in-playground.md) |
| 8 | 檢視摘要，確認後續步驟 | [07](07-summary.md) |

---

**上一頁：** [07 - 摘要](07-summary.md) · **首頁：** [工作坊 README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->