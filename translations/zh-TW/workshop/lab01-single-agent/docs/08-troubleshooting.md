# Module 8 - 疑難排解

本模組是作坊期間遇到的每個常見問題的參考指南。請加書籤——當出現問題時，你會回來查看。

---

## 1. 權限錯誤

### 1.1 `agents/write` 權限被拒絕

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**根本原因：** 你在 <strong>專案</strong> 層級沒有 `Azure AI User` 角色。這是作坊中最常見的錯誤。

**修復步驟：**

1. 開啟 [https://portal.azure.com](https://portal.azure.com)。
2. 在頂部搜尋欄，輸入你的 **Foundry 專案** 名稱（例如：`workshop-agents`）。
3. **關鍵：** 點選結果中顯示類型為 **"Microsoft Foundry project"** 的項目，而不是其父帳戶或樞紐資源。這些是不同的資源，具有不同的 RBAC 範圍。
4. 在專案頁面的左側導航中，點選 **Access control (IAM)**。
5. 點選 **Role assignments** 分頁以檢查是否已有此角色：
   - 搜尋你的姓名或電子郵件。
   - 如果已顯示 `Azure AI User` → 表示錯誤另有原因（請參考下面第 8 步驟）。
   - 如果未顯示 → 繼續新增。
6. 點選 **+ Add** → **Add role assignment**。
7. 於 **Role** 分頁：
   - 搜尋 [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles)。
   - 從結果中選取它。
   - 點選 **Next**。
8. 於 **Members** 分頁：
   - 選擇 **User, group, or service principal**。
   - 點選 **+ Select members**。
   - 搜尋你的姓名或電子郵件地址。
   - 從結果中選取你自己。
   - 點選 **Select**。
9. 點選 **Review + assign** → 再次點選 **Review + assign**。
10. **等待 1-2 分鐘** - RBAC 變更需要時間傳播。
11. 重試之前失敗的操作。

> **為何 Owner/Contributor 不足夠：** Azure RBAC 有兩種權限 - <em>管理操作</em> 和 <em>資料操作</em>。Owner 和 Contributor 授予管理操作（建置資源、編輯設定），但代理操作需要 `agents/write` <strong>資料操作</strong>，此權限僅包含在 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner` 角色中。請參閱 [Foundry RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 資源部署時出現 `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**根本原因：** 你在此訂閱/資源群組中沒有建立或修改 Azure 資源的權限。

**修復方法：**
1. 請訂閱管理員將 **Contributor** 角色指派給你，範圍是 Foundry 專案所在的資源群組。
2. 或請管理員為你建立 Foundry 專案並授予你專案層級的 **Azure AI User**。

### 1.3 在 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) 中出現 `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**根本原因：** 該 Azure 訂閱未註冊 Foundry 所需的資源提供者。

**修復方法：**

1. 開啟終端機並執行：
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```

2. 等待註冊完成（可能需 1 到 5 分鐘）：
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   預期輸出：`"Registered"`
3. 重試操作。

---

## 2. Docker 錯誤（僅限已安裝 Docker）

> Docker 對此作坊為 <strong>可選</strong>。下列錯誤僅在你安裝 Docker Desktop 且 Foundry 擴充套件嘗試本地容器建置時才適用。

### 2.1 Docker daemon 未啟動

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**修復步驟：**

1. 在開始功能表（Windows）或應用程式資料夾（macOS）找到並啟動 Docker Desktop。
2. 等待 Docker Desktop 視窗顯示 **"Docker Desktop is running"** — 通常需 30-60 秒。
3. 在系統列（Windows）或選單列（macOS）看到 Docker 鯨魚圖示，滑鼠懸停檢查狀態。
4. 在終端驗證：
   ```powershell
   docker info
   ```
   如果這列出了 Docker 系統資訊（伺服器版本、存儲驅動等），則表示 Docker 正在執行。
5. **Windows 專用：** 若 Docker 仍無法啟動：
   - 開啟 Docker Desktop → 點選 **Settings**（齒輪圖示）→ **General**。
   - 確認勾選了 **Use the WSL 2 based engine**。
   - 點選 **Apply & restart**。
   - 如果未安裝 WSL 2，請在提升權限的 PowerShell 執行 `wsl --install` 並重新啟動電腦。
6. 重新嘗試部署。

### 2.2 Docker 建置因依賴錯誤失敗

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**修復方法：**
1. 打開 `requirements.txt`，確認所有套件名稱拼寫正確無誤。
2. 確認版本限定（pinning）符合預期：
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```

3. 先嘗試本地安裝測試：
   ```bash
   pip install -r requirements.txt
   ```

4. 若使用私有套件索引，確保 Docker 有網路連線權限。

### 2.3 容器平台不匹配（Apple Silicon）

若從 Apple Silicon Mac（M1/M2/M3/M4）部署，容器必須建置為 `linux/amd64`，因為 Foundry 的容器執行時使用 AMD64 架構。

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry 擴充套件的部署指令在大多數情況下自動處理此問題。若出現與架構相關的錯誤，請使用 `--platform` 標誌手動建置，並聯絡 Foundry 團隊。

---

## 3. 身份驗證錯誤

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) 無法取得 token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**根本原因：** `DefaultAzureCredential` 鏈中的任何憑證來源都沒有有效的 token。

**修復步驟，依序嘗試：**

1. **透過 Azure CLI 重新登入**（最常見的修復）：
   ```bash
   az login
   ```
   會開啟瀏覽器視窗，登入後回到 VS Code。

2. **設定正確的訂閱：**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   若非正確訂閱：
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **透過 VS Code 重新登入：**
   - 點選 VS Code 左下角的 **Accounts** 圖示（人像圖示）。
   - 點選你的帳戶名稱 → **Sign Out**。
   - 再次點選 Accounts 圖示 → **Sign in to Microsoft**。
   - 完成瀏覽器登入流程。

4. **服務主體（僅 CI/CD 場景）：**
   - 在 `.env` 中設定以下環境變數：
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - 然後重啟代理程序。

5. **檢查 token 快取：**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   若失敗，表示 CLI token 已過期。請重新執行 `az login`。

### 3.2 token 本地有效但託管部署失敗

**根本原因：** 託管代理使用系統管理身分識別，與你的個人憑證不同。

**修復：** 這是預期行為 - 管理身分識別會在部署時自動佈建。若託管代理仍遇到認證錯誤：
1. 確認 Foundry 專案的系統管理身分識別已被授權存取 Azure OpenAI 資源。
2. 驗證 `agent.yaml` 中的 `PROJECT_ENDPOINT` 是否正確。

---

## 4. 模型錯誤

### 4.1 找不到模型部署

```
Error: Model deployment not found / The specified deployment does not exist
```

**修復步驟：**

1. 開啟 `.env` 檔，記下 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 的值。
2. 在 VS Code 中打開 **Microsoft Foundry** 側邊欄。
3. 展開你的專案 → **Model Deployments**。
4. 比對側邊欄中顯示的部署名稱與 `.env` 中的值。
5. 名稱 <strong>區分大小寫</strong> — `gpt-4o` 與 `GPT-4o` 是不同的。
6. 若不符，請更新 `.env` 使用側邊欄顯示的精確名稱。
7. 託管部署時，請同時更新 `agent.yaml`：
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 模型回應內容異常

**修復方法：**
1. 查看 `main.py` 中的 `EXECUTIVE_AGENT_INSTRUCTIONS` 常數。確保指令未被截斷或損壞。
2. 檢查模型溫度設定（如果可配置）— 較低值會提供更確定性的輸出。
3. 比較所部署的模型（例如 `gpt-4o` 與 `gpt-4o-mini`），不同模型能力不同。

---

## 5. 部署錯誤

### 5.1 ACR 拉取授權失敗

```
Error: AcrPullUnauthorized
```

**根本原因：** Foundry 專案的系統管理身分識別無法從 Azure Container Registry 拉取容器映像檔。

**修復步驟：**

1. 開啟 [https://portal.azure.com](https://portal.azure.com)。
2. 在頂部搜尋欄搜尋 **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**。
3. 點擊與你的 Foundry 專案相關的容器註冊表（通常與專案位於同一資源群組）。
4. 在左側導航中點選 **Access control (IAM)**。
5. 點選 **+ Add** → **Add role assignment**。
6. 搜尋並選擇 **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** 角色。點選 **Next**。
7. 選擇 **Managed identity** → 點選 **+ Select members**。
8. 找到並選擇 Foundry 專案的系統管理身分識別。
9. 點選 **Select** → **Review + assign** → 再次點選 **Review + assign**。

> 此角色指派通常由 Foundry 擴充套件自動完成。若發生此錯誤，表示自動設置失敗。你也可嘗試重新部署，擴充套件可能會重試設置。

### 5.2 代理部署後無法啟動

**症狀：** 容器狀態維持「Pending」超過 5 分鐘或顯示「Failed」。

**修復步驟：**

1. 在 VS Code 開啟 **Microsoft Foundry** 側邊欄。
2. 點選你的託管代理 → 選擇版本。
3. 在詳細面板檢查 **Container Details** → 查找 **Logs** 區域或連結。
4. 閱讀容器啟動日誌。常見原因：

| 日誌訊息 | 原因 | 修復方法 |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | 缺少依賴 | 將其加入 `requirements.txt` 並重新部署 |
| `KeyError: 'PROJECT_ENDPOINT'` | 缺少環境變數 | 在 `agent.yaml` 的 `env:` 區塊新增該變數 |
| `OSError: [Errno 98] Address already in use` | 埠衝突 | 確認 `agent.yaml` 的 `port: 8088`，且只有一個程序綁定該埠 |
| `ConnectionRefusedError` | 代理未開始監聽 | 檢查 `main.py` - `from_agent_framework()` 需要在啟動時執行 |

5. 修正問題後，參考 [Module 6](06-deploy-to-foundry.md) 重新部署。

### 5.3 部署逾時

**修復方法：**
1. 檢查你的網路連線 — Docker 推送可能檔案很大（首次部署超過 100MB）。
2. 若處於企業代理後方，請確保 Docker Desktop 已設定代理：**Docker Desktop** → **Settings** → **Resources** → **Proxies**。
3. 再次嘗試，網路波動可能造成暫時失敗。

---

## 6. 快速參考：RBAC 角色

| 角色 | 典型範圍 | 授予權限 |
|------|---------------|----------------|
| **Azure AI User** | 專案 | 資料操作：建立、部署和調用代理 (`agents/write`, `agents/read`) |
| **Azure AI Developer** | 專案或帳戶 | 資料操作 + 專案建立 |
| **Azure AI Owner** | 帳戶 | 完全存取 + 角色指派管理 |
| **Azure AI Project Manager** | 專案 | 資料操作 + 可以指派 Azure AI User 給他人 |
| **Contributor** | 訂閱/資源群組 | 管理操作（建立/刪除資源）。<strong>不包含資料操作</strong> |
| **Owner** | 訂閱/資源群組 | 管理操作 + 角色指派。<strong>不包含資料操作</strong> |
| **Reader** | 任何 | 只讀管理存取 |

> **重點提醒：** `Owner` 和 `Contributor` <strong>不包括</strong>資料操作。代理操作必須擁有 `Azure AI *` 角色。本作坊最低需求為專案範圍的 **Azure AI User**。

---

## 7. 作坊完成核對清單

用以最後核對所有任務是否完成：

| 編號 | 項目 | 模組 | 通過？ |
|---|------|--------|---|
| 1 | 所有先決條件已安裝並驗證 | [00](00-prerequisites.md) | |
| 2 | 安裝 Foundry Toolkit 與 Foundry 擴充套件 | [01](01-install-foundry-toolkit.md) | |
| 3 | 建立 Foundry 專案（或選擇已存在專案） | [02](02-create-foundry-project.md) | |
| 4 | 已部署模型（例如 gpt-4o） | [02](02-create-foundry-project.md) | |
| 5 | 在專案範圍內指派 Azure AI 使用者角色 | [02](02-create-foundry-project.md) | |
| 6 | 建立主機代理專案骨架（agent/） | [03](03-create-hosted-agent.md) | |
| 7 | `.env` 配置了 PROJECT_ENDPOINT 和 MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | 在 main.py 自訂代理指令 | [04](04-configure-and-code.md) | |
| 9 | 已建立虛擬環境並安裝相依性 | [04](04-configure-and-code.md) | |
| 10 | 使用 F5 或終端機本地測試代理（4 項冒煙測試通過） | [05](05-test-locally.md) | |
| 11 | 部署至 Foundry 代理服務 | [06](06-deploy-to-foundry.md) | |
| 12 | 容器狀態顯示「已啟動」或「執行中」 | [06](06-deploy-to-foundry.md) | |
| 13 | 在 VS Code Playground 驗證（4 項冒煙測試通過） | [07](07-verify-in-playground.md) | |
| 14 | 在 Foundry Portal Playground 驗證（4 項冒煙測試通過） | [07](07-verify-in-playground.md) | |

> **恭喜！** 如果所有項目都打勾，表示你已完成整個工作坊。你已從零開始建立主機代理、本地測試、部署到 Microsoft Foundry，並在生產環境中進行驗證。

---

**上一頁：** [07 - 在 Playground 驗證](07-verify-in-playground.md) · **首頁：** [工作坊 README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的原文版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用此翻譯而產生的任何誤解或誤釋負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->