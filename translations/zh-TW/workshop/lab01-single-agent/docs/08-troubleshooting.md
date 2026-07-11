# 模組 8 - 疑難排解

本模組是常見問題的參考指南。請將它加入書籤，當發生問題時再回來查閱。

---

## 1. 權限錯誤

### 1.1 拒絕存取 `agents/write` 權限

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**根本原因：** 在 <strong>專案</strong> 級別缺少 `Azure AI User` 角色。這是工作坊中最常見的錯誤。

**解決方法：**
1. 開啟 [portal.azure.com](https://portal.azure.com)。
2. 搜尋您的 Foundry <strong>專案</strong> 名稱 → 點選類型為 **"Microsoft Foundry project"** 的結果（不是父帳戶）。
3. **存取控制 (IAM)** → **+ 新增** → <strong>新增角色指派</strong>。
4. 角色：選擇 **Azure AI User** → 下一步。
5. 成員：選擇您自己 → 檢閱並指派 → 檢閱並指派。
6. **等待 1–2 分鐘** → 重試。

> **為何擁有者/參與者角色不足：** 這些角色僅授予<em>管理</em>操作。代理人操作需要 `agents/write` <em>資料動作</em>，此權限只包含在 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner` 角色中。詳見 [Foundry RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 佈建期間出現 `AuthorizationFailed`

**解決方法：** 請管理員在資源群組指派 **Contributor** 角色，或者請他們為您建立專案並授予您該專案的 **Azure AI User** 角色。

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# 等待直到：“已註冊”
```

---

## 2. Docker 錯誤

> Docker 是<strong>選用的</strong>。以下錯誤僅在安裝 Docker Desktop 且擴充功能嘗試本機建置時適用。

### 2.1 Docker 守護程序未運行

**解決方法：** 啟動 Docker Desktop → 等待顯示「執行中」狀態 → 使用 `docker info` 驗證 → 重試。

### 2.2 建置失敗，出現依賴錯誤

**解決方法：** 確認 `requirements.txt` 拼寫正確，先在本機測試：`pip install -r requirements.txt`。

### 2.3 平台不匹配（Apple Silicon）

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. 認證錯誤

### 3.1 `DefaultAzureCredential` 失敗

**解決方法（依序嘗試）：**
1. `az login`（重新驗證）
2. `az account set --subscription "<id>"`（設定正確訂閱）
3. VS Code → 帳戶 → 登出 → 再登入
4. 驗證：`az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token 在本機有效但在託管環境無效

**預期情況：** 託管代理使用系統管理的識別，而非您的認證。如託管代理出現認證錯誤：
- 驗證 `agent.yaml` 中的 `AZURE_AI_PROJECT_ENDPOINT` 是否正確
- 確認專案的管理識別具有模型存取權

---

## 4. 模型錯誤

### 4.1 找不到模型部署

**解決方法：** 名稱是<strong>大小寫敏感</strong>的。比較 `.env` 中的 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 和 Foundry 側邊欄 → 模型中的精確名稱。

### 4.2 模型輸出異常

**解決方法：** 檢查 `main.py` 中的 `AGENT_INSTRUCTIONS`（是否截斷？）。嘗試不同模型（`gpt-4.1` vs `gpt-4.1-mini`）。

---

## 5. 佈署錯誤

### 5.1 ACR 拉取未授權

**解決方法：** 在 Azure 管理入口網站 → Container Registry → 存取控制 (IAM) → 新增 **AcrPull** 角色給 Foundry 專案的管理識別。

### 5.2 代理啟動失敗（停留在「等待中」或「失敗」）

在側邊欄查看容器日誌。常見原因：

| 日誌訊息 | 解決方法 |
|-------------|-----|
| `ModuleNotFoundError` | 將缺少的套件加入 `requirements.txt`，重新佈署 |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | 在 `agent.yaml` 的 `environment_variables` 中加入環境變數 |
| `Address already in use` | 確認只有一個程序綁定在 8088 埠口 |

### 5.3 佈署逾時

**解決方法：** 檢查網路連線。初次佈署會推送超過 100MB。若處於代理伺服器後，請設定 Docker Desktop 的代理設定。

---

## 6. 路徑 B - Foundry Local

### 6.1 Foundry Local 無法啟動

| 問題 | 解決方法 |
|-------|-----|
| `foundry: command not found` | 重新安裝：`winget install Microsoft.FoundryLocal` |
| 資源不足 | Foundry Local 需要約 4GB 可用記憶體。請關閉其他應用程式。 |
| 模型下載失敗 | 檢查磁碟空間（模型大小約 2–8 GB）。重試指令：`foundry local models pull <name>` |

### 6.2 Foundry Local 模型錯誤

| 問題 | 解決方法 |
|-------|-----|
| 回應速度緩慢 | 預期情況 - 本地模型在 CPU 運行，除非有 GPU。請耐心等待。 |
| 輸出品質差 | 如果硬體允許，嘗試使用更大型模型。`phi-4-mini` 是良好的平衡選擇。 |
| 連線被拒絕 | 確認 Foundry Local 正在運行：`foundry local status`。需要可重新啟動。 |

---

## 7. 快速參考：RBAC 角色

| 角色 | 範圍 | 授權內容 |
|------|-------|--------|
| **Azure AI User** | 專案 | 資料動作：`agents/write`、`agents/read` |
| **Azure AI Developer** | 專案/帳戶 | 資料動作 + 專案建立 |
| **Azure AI Owner** | 帳戶 | 完整存取 + 角色管理 |
| **Contributor** | 訂閱/資源群組 | 僅管理操作（<strong>無</strong>資料動作） |
| **Owner** | 訂閱/資源群組 | 管理 + 角色指派（<strong>無</strong>資料動作） |

---

## 8. 工作坊完成檢查清單

| # | 項目 | 模組 |
|---|------|--------|
| 1 | 安裝並驗證先決條件 | [00](00-prerequisites.md) |
| 2 | 安裝 Foundry Toolkit 擴充功能，連接專案（或完成路徑 B 配置） | [01](01-setup.md) |
| 3 | 已建立託管代理 | [02](02-create-hosted-agent.md) |
| 4 | 已配置 `.env`、撰寫指令、安裝依賴 | [03](03-configure-and-code.md) |
| 5 | 在本機測試代理 - 3 個功能場景通過 | [04](04-test-locally.md) |
| 6 | 已部署至 Foundry（僅路徑 A） | [05](05-deploy-to-foundry.md) |
| 7 | 雲端邊緣案例/安全測試通過（僅路徑 A） | [06](06-verify-in-playground.md) |
| 8 | 檢閱摘要，確定後續步驟 | [07](07-summary.md) |

---

**前一節：** [07 - 摘要](07-summary.md) · **首頁：** [工作坊 README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->