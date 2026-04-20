# Module 8 - 疑難排解

本模組為工作坊中遇到的各種常見問題提供參考指南。請將此頁面加入書籤 — 當有問題時，你會隨時回來查看。

---

## 1. 權限錯誤

### 1.1 `agents/write` 權限被拒

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**根本原因：** 你在 <strong>專案</strong> 層級上沒有 `Azure AI User` 角色。這是工作坊中最常見的錯誤。

**解決步驟：**

1. 開啟 [https://portal.azure.com](https://portal.azure.com)。
2. 在頂部搜尋列輸入你的 **Foundry 專案** 名稱（例如 `workshop-agents`）。
3. **關鍵步驟：** 點擊結果中顯示類型為 **"Microsoft Foundry project"** 的項目，而非父層帳戶/集線器資源。這些是不同的資源，具有不同的 RBAC 範圍。
4. 在專案頁面的左側導航，點擊 **Access control (IAM)**。
5. 點擊 **Role assignments** 索引標籤，檢查是否已有該角色：
   - 搜尋你的名字或電子郵件。
   - 若已列出 `Azure AI User` → 錯誤可能有其他原因（請查看第8步）。
   - 若未列出 → 繼續新增。
6. 點擊 **+ Add** → **Add role assignment**。
7. 在 **Role** 索引標籤：
   - 搜尋 [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles)。
   - 從結果中選取它。
   - 點擊 **Next**。
8. 在 **Members** 索引標籤：
   - 選擇 **User, group, or service principal**。
   - 點擊 **+ Select members**。
   - 搜尋你的名字或電子郵件地址。
   - 從結果中選擇你自己。
   - 點擊 **Select**。
9. 點擊 **Review + assign** → 再次點擊 **Review + assign**。
10. **等待 1-2 分鐘** — RBAC 變更需要一些時間傳播。
11. 重試失敗的操作。

> **為何 Owner/Contributor 不足夠：** Azure RBAC 有兩種權限類型 — <em>管理動作</em> 與 <em>資料動作</em>。Owner 和 Contributor 允許管理動作（建立資源、編輯設定），但代理程式運行需要 `agents/write` <strong>資料動作</strong>，該權限僅包含在 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner` 角色中。詳見 [Foundry RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 資源部署時出現 `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**根本原因：** 你沒有在此訂閱/資源群組中建立或修改 Azure 資源的權限。

**修正方法：**
1. 請你的訂閱管理員將你指派為 Foundry 專案所在資源群組的 **Contributor**。
2. 或請他們為你建立 Foundry 專案，並授予專案的 **Azure AI User** 角色。

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) 顯示 `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**根本原因：** Azure 訂閱尚未註冊 Foundry 需要的資源提供者。

**修正方法：**

1. 開啟終端機並執行：
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. 等待註冊完成（可能需 1-5 分鐘）：
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   預期輸出：`"Registered"`
3. 重試操作。

---

## 2. Docker 錯誤（僅限安裝 Docker 時）

> Docker 是本工作坊的 <strong>選用項目</strong>。以下錯誤僅在你安裝 Docker Desktop 且 Foundry 擴充嘗試本地容器建置時適用。

### 2.1 Docker Daemon 未執行

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**解決步驟：**

1. 在開始選單（Windows）或應用程式（macOS）中找到並啟動 Docker Desktop。
2. 等待 Docker Desktop 視窗顯示 **「Docker Desktop is running」**，通常需要 30-60 秒。
3. 查看系統列（Windows）或選單列（macOS）中的 Docker 鯨魚圖示，將滑鼠移至該圖示以確認狀態。
4. 在終端機確認：
   ```powershell
   docker info
   ```
   如果此指令列出 Docker 系統資訊（Server Version、Storage Driver 等）即表示 Docker 正在運行。
5. **Windows 專用：** 若 Docker 仍無法啟動：
   - 開啟 Docker Desktop → **Settings**（齒輪圖示）→ **General**。
   - 確認勾選 **Use the WSL 2 based engine**。
   - 點擊 **Apply & restart**。
   - 若系統尚未安裝 WSL 2，請在提升權限的 PowerShell 中執行 `wsl --install` 並重新啟動電腦。
6. 重試部署。

### 2.2 Docker 建置失敗並出現依賴錯誤

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**修正方法：**
1. 打開 `requirements.txt`，確認所有套件名稱拼寫正確。
2. 確認版本鎖定設定正確：
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. 本地先測試安裝：
   ```bash
   pip install -r requirements.txt
   ```
4. 若使用私有套件索引，確保 Docker 有網路權限存取。

### 2.3 容器平台不匹配（Apple Silicon）

若從 Apple Silicon Mac（M1/M2/M3/M4）部署，容器必須針對 `linux/amd64` 建置，因為 Foundry 的容器運行時使用 AMD64 架構。

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry 擴充的 deploy 指令多數情況會自動處理此事。如遇架構相關錯誤，請手動加上 `--platform` 標誌建置，並聯絡 Foundry 團隊。

---

## 3. 認證錯誤

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) 無法取得憑證代幣

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**根本原因：** `DefaultAzureCredential` 鏈中的任何認證來源都沒有有效代幣。

**逐步嘗試解決方法：**

1. **透過 Azure CLI 重新登入**（最常見解決方式）：
   ```bash
   az login
   ```
   將開啟瀏覽器視窗，登入後返回 VS Code。

2. **設置正確的訂閱：**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   若不是正確的訂閱：
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **透過 VS Code 重新登入：**
   - 點擊左下角的 **Accounts**（人物圖示）。
   - 點選帳戶名稱 → **Sign Out**（登出）。
   - 再點一次帳戶圖示 → **Sign in to Microsoft**（登入 Microsoft）。
   - 完成瀏覽器中的登入流程。

4. **服務主體（僅 CI/CD 使用場景）：**
   - 在 `.env` 檔案中設定以下環境變數：
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - 之後重新啟動代理程式。

5. **檢查代幣快取：**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   若失敗，表示 CLI 代幣已過期。再次執行 `az login`。

### 3.2 代幣在本機有效，托管部署失敗

**根本原因：** 托管代理使用系統管理身分，與個人憑證不同。

**解決方法：** 此為預期行為 — 系統管理身分會在部署時自動建立。若托管代理仍出現認證錯誤：
1. 確認 Foundry 專案的系統管理身分已有權限存取 Azure OpenAI 資源。
2. 驗證 `agent.yaml` 裡的 `PROJECT_ENDPOINT` 是否正確。

---

## 4. 模型錯誤

### 4.1 找不到模型部署

```
Error: Model deployment not found / The specified deployment does not exist
```

**修正步驟：**

1. 開啟 `.env` 檔案，記下 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 的值。
2. 在 VS Code 中打開 **Microsoft Foundry** 側邊欄。
3. 展開你的專案 → **Model Deployments**。
4. 比對側邊欄中列出的部署名稱與 `.env` 中的值。
5. 名稱 <strong>區分大小寫</strong> — `gpt-4o` 與 `GPT-4o` 不同。
6. 若不一致，更新 `.env` 以使用側邊欄顯示的正確名稱。
7. 若為托管部署，也更新 `agent.yaml`：
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 模型回應內容異常

**解決方法：**
1. 檢查 `main.py` 中的常數 `EXECUTIVE_AGENT_INSTRUCTIONS`，確認其未被截斷或損壞。
2. 檢查模型溫度設定（如果可設定）— 較低溫度會產生較確定性的輸出。
3. 比較使用的模型（例如 `gpt-4o` vs `gpt-4o-mini`）— 不同模型能力不同。

---

## 5. 部署錯誤

### 5.1 ACR 拉取授權失敗

```
Error: AcrPullUnauthorized
```

**根本原因：** Foundry 專案的系統管理身分無法從 Azure Container Registry 拉取容器映像檔。

**解決步驟：**

1. 開啟 [https://portal.azure.com](https://portal.azure.com)。
2. 在頂部搜尋列輸入 **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**。
3. 點選與你的 Foundry 專案關聯的註冊表（通常與專案同資源群組）。
4. 在左側導航點選 **Access control (IAM)**。
5. 點擊 **+ Add** → **Add role assignment**。
6. 搜尋並選擇 **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**，點擊 **Next**。
7. 選擇 **Managed identity** → 點擊 **+ Select members**。
8. 找到並選擇 Foundry 專案的系統管理身分。
9. 點擊 **Select** → **Review + assign** → 再點擊 **Review + assign**。

> 此角色指派通常由 Foundry 擴充自動設置。若出現此錯誤，可能是自動設置失敗。你可嘗試重新部署，擴充可能會重新嘗試設定。

### 5.2 代理部署後無法啟動

**現象：** 容器狀態停留在「Pending」超過5分鐘或顯示「Failed」。

**解決步驟：**

1. 打開 VS Code 的 **Microsoft Foundry** 側邊欄。
2. 點選你的托管代理 → 選擇版本。
3. 在詳細面板中，查看 **Container Details** → 找尋 **Logs** 區段或連結。
4. 閱讀容器啟動日誌。常見原因：

| 日誌訊息 | 原因 | 解決方法 |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | 缺少依賴套件 | 將該套件加至 `requirements.txt` 並重新部署 |
| `KeyError: 'PROJECT_ENDPOINT'` | 環境變數缺失 | 在 `agent.yaml` 的 `env:` 區段新增該環境變數 |
| `OSError: [Errno 98] Address already in use` | 埠衝突 | 確認 `agent.yaml` 設定 `port: 8088` 且僅有一個程序綁定此埠 |
| `ConnectionRefusedError` | 代理未啟動監聽 | 檢查 `main.py`，確認 `from_agent_framework()` 呼叫於啟動時執行 |

5. 解決問題後，從第 [Module 6](06-deploy-to-foundry.md) 重新部署。

### 5.3 部署逾時

**修正建議：**
1. 檢查網路連線 — Docker 推送的大小可能很大（首次部署可超過 100MB）。
2. 若處於企業代理 (Proxy) 後方，確保 Docker Desktop 設定有 Proxy 配置：**Docker Desktop** → **Settings** → **Resources** → **Proxies**。
3. 再次嘗試 — 網路不穩可能導致臨時錯誤。

---

## 6. 快速參考：RBAC 角色

| 角色 | 典型範圍 | 授權內容 |
|------|---------------|----------------|
| **Azure AI User** | 專案 | 資料動作：建置、部署並調用代理 (`agents/write`, `agents/read`) |
| **Azure AI Developer** | 專案或帳戶 | 資料動作 + 專案建立 |
| **Azure AI Owner** | 帳戶 | 完整存取 + 角色指派管理 |
| **Azure AI Project Manager** | 專案 | 資料動作 + 可指派 Azure AI User 給他人 |
| **Contributor** | 訂閱/資源群組 | 管理動作（建立/刪除資源）。<strong>不包含資料動作</strong> |
| **Owner** | 訂閱/資源群組 | 管理動作 + 角色指派。<strong>不包含資料動作</strong> |
| **Reader** | 任意 | 唯讀管理存取 |

> **重點：** `Owner` 與 `Contributor` 不包含資料動作。代理操作始終需要 `Azure AI *` 角色。工作坊最低需求是 **Azure AI User**，範圍為 <strong>專案</strong>。

---

## 7. 工作坊完成檢查清單

作為完成所有步驟的最終確認：

| # | 項目 | 模組 | 是否通過？ |
|---|------|--------|---|
| 1 | 安裝並驗證所有先決條件 | [00](00-prerequisites.md) | |
| 2 | 安裝 Foundry Toolkit 與 Foundry 擴充功能 | [01](01-install-foundry-toolkit.md) | |
| 3 | 已建立 Foundry 專案（或選擇現有專案） | [02](02-create-foundry-project.md) | |
| 4 | 已部署模型（例如 gpt-4o） | [02](02-create-foundry-project.md) | |
| 5 | 已在專案範圍內分配 Azure AI 使用者角色 | [02](02-create-foundry-project.md) | |
| 6 | 已架構託管代理專案 (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | 使用 PROJECT_ENDPOINT 和 MODEL_DEPLOYMENT_NAME 設定 `.env` | [04](04-configure-and-code.md) | |
| 8 | 在 main.py 中自訂代理指令 | [04](04-configure-and-code.md) | |
| 9 | 已建立虛擬環境並安裝相依套件 | [04](04-configure-and-code.md) | |
| 10 | 已在本地使用 F5 或終端機測試代理（通過 4 項煙霧測試） | [05](05-test-locally.md) | |
| 11 | 已部署至 Foundry Agent 服務 | [06](06-deploy-to-foundry.md) | |
| 12 | 容器狀態顯示「已啟動」或「執行中」 | [06](06-deploy-to-foundry.md) | |
| 13 | 已在 VS Code Playground 驗證（通過 4 項煙霧測試） | [07](07-verify-in-playground.md) | |
| 14 | 已在 Foundry Portal Playground 驗證（通過 4 項煙霧測試） | [07](07-verify-in-playground.md) | |

> **恭喜！** 如果所有項目都已勾選，您已完成整個工作坊。您已從零開始建立託管代理，並在本地測試，將其部署至 Microsoft Foundry，並在生產環境中驗證。

---

**上一步：** [07 - 在 Playground 中驗證](07-verify-in-playground.md) · **首頁：** [工作坊 README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力確保準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始語言的文件應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯所引起的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->