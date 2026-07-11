# 模組 8 - 疑難排解

本模組為常見問題的參考指南。請將此頁加入書籤，當出現問題時返回查閱。

---

## 1. 權限錯誤

### 1.1 `agents/write` 權限被拒

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**根本原因：** 缺少<strong>專案</strong>層級的 `Azure AI User` 角色。這是研討會中最常見的錯誤。

**解決方法：**
1. 開啟 [portal.azure.com](https://portal.azure.com)。
2. 搜尋你的 Foundry <strong>專案</strong>名稱 → 點擊類型為 **"Microsoft Foundry project"** 的結果（非父帳號）。
3. 進入 **存取控制 (IAM)** → **+ 新增** → <strong>新增角色指派</strong>。
4. 角色選擇：**Azure AI User** → 下一步。
5. 成員：選擇自己 → 審查 + 指派 → 審查 + 指派。
6. **等待 1–2 分鐘** → 重試。

> **為何 Owner/Contributor 不夠用：** 這些角色僅授予<em>管理</em>操作權限。代理程式操作需 `agents/write` <em>資料操作</em>，此權限只包含在 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner` 角色中。詳見 [Foundry RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 部署過程出現 `AuthorizationFailed`

**解決方法：** 請管理員在資源群組上指派 **Contributor** 角色，或請他們為你建立專案並授予你 **Azure AI User** 角色。

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# 等待至：「已註冊」
```

---

## 2. Docker 錯誤

> Docker 是<strong>選用項目</strong>。下列錯誤僅在安裝了 Docker Desktop 且擴充嘗試本機構建時才會出現。

### 2.1 Docker 守護程序未運行

**解決方法：** 啟動 Docker Desktop → 等候顯示「運行中」狀態 → 使用 `docker info` 驗證 → 重新嘗試。

### 2.2 建置失敗並顯示依賴錯誤

**解決方法：** 核對 `requirements.txt` 拼寫，先在本機測試：`pip install -r requirements.txt`。

### 2.3 平台不匹配（Apple Silicon）

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. 驗證錯誤

### 3.1 `DefaultAzureCredential` 認證失敗

**解決方法（依序嘗試）：**
1. 執行 `az login`（重新認證）
2. 執行 `az account set --subscription "<id>"`（設定正確訂閱）
3. VS Code → 帳戶 → 登出 → 再次登入
4. 確認：`az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 本機 token 有效但托管代理無效

**預期行為：** 托管代理使用系統管理的身份，而非你的憑證。若托管代理出現認證錯誤：
- 確認 `agent.yaml` 中的 `AZURE_AI_PROJECT_ENDPOINT` 設定正確
- 檢查專案的託管身份是否具有模型存取權限

---

## 4. 模型錯誤

### 4.1 找不到模型部署

**解決方法：** 名稱<strong>區分大小寫</strong>。比對 `.env` 中 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 與 Foundry 側邊欄 → 模型中的精確名稱。

### 4.2 模型輸出異常

**解決方法：** 檢查 `main.py` 中的 `AGENT_INSTRUCTIONS`（是否被截斷？）。試用不同模型（例如 `gpt-4.1` 對比 `gpt-4.1-mini`）。

---

## 5. 部署錯誤

### 5.1 ACR 拉取未授權

**解決方法：** 在 Azure 入口網站 → 容器註冊表 → 存取控制 (IAM) → 向 Foundry 專案的託管身份新增 **AcrPull** 角色。

### 5.2 代理啟動失敗（持續顯示「待命」或「失敗」）

在側邊欄查看容器日誌。常見原因：

| 日誌訊息 | 解決方法 |
|-------------|-----|
| `ModuleNotFoundError` | 將缺少的套件加入 `requirements.txt`，重新部署 |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | 在 `agent.yaml` 的 `environment_variables` 區段新增環境變數 |
| `Address already in use` | 確保只有一個程序綁定在 8088 埠 |

### 5.3 部署逾時

**解決方法：** 檢查網路連線。首次部署需推送 >100MB。若處於代理伺服器後方，請配置 Docker Desktop 的代理設定。

---

## 6. 路徑 B - Foundry Local

### 6.1 Foundry Local 無法啟動

| 問題 | 解決方法 |
|-------|-----|
| `foundry: command not found` | 重新安裝：`winget install Microsoft.FoundryLocal` |
| 資源不足 | Foundry Local 需要約 4GB 以上可用記憶體。關閉其他應用程式。 |
| 模型下載失敗 | 檢查磁碟空間（模型大小 2–8 GB）。重試：`foundry local models pull <name>` |

### 6.2 Foundry Local 模型錯誤

| 問題 | 解決方法 |
|-------|-----|
| 回應緩慢 | 正常 - 本機模型除非有 GPU，否則在 CPU 上執行。請耐心等候。 |
| 輸出品質差 | 若硬體允許，試用較大模型。`phi-4-mini` 是不錯的平衡選擇。 |
| 連線被拒絕 | 確認 Foundry Local 是否正在運行：`foundry local status`。必要時重新啟動。 |

---

## 7. 快速參考：RBAC 角色

| 角色 | 範圍 | 授權內容 |
|------|-------|--------|
| **Azure AI User** | 專案 | 資料操作：`agents/write`、`agents/read` |
| **Azure AI Developer** | 專案/帳號 | 資料操作 + 專案建立 |
| **Azure AI Owner** | 帳號 | 完整存取 + 角色管理 |
| **Contributor** | 訂閱/資源群組 | 僅管理操作 (<strong>無</strong>資料操作) |
| **Owner** | 訂閱/資源群組 | 管理 + 角色指派 (<strong>無</strong>資料操作) |

---

## 8. 研討會完成檢查表

| 編號 | 項目 | 模組 |
|---|------|--------|
| 1 | 先決條件已安裝並驗證 | [00](00-prerequisites.md) |
| 2 | Foundry 工具套件擴充已安裝，專案已連接（或路徑 B 已配置） | [01](01-setup.md) |
| 3 | 托管代理架構已建立 | [02](02-create-hosted-agent.md) |
| 4 | `.env` 已配置，指令編寫完畢，依賴安裝完成 | [03](03-configure-and-code.md) |
| 5 | 本機測試代理 - 3 個功能場景通過 | [04](04-test-locally.md) |
| 6 | 部署至 Foundry（僅限路徑 A） | [05](05-deploy-to-foundry.md) |
| 7 | 雲端中邊緣案例/安全測試通過（僅限路徑 A） | [06](06-verify-in-playground.md) |
| 8 | 檢閱總結，確認後續步驟 | [07](07-summary.md) |

---

**上一頁：** [07 - 總結](07-summary.md) · **首頁：** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->