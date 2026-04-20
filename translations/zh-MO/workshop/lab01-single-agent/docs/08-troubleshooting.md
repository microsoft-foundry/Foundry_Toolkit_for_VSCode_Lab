# Module 8 - 疑難排解

此模組是本工作坊中遇到的每個常見問題的參考指南。請將它設為書籤 — 每當遇到問題時，都會回來查看。

---

## 1. 權限錯誤

### 1.1 `agents/write` 權限被拒

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**根本原因：** 您在<strong>專案</strong>層級沒有 `Azure AI User` 角色。這是工作坊中最常見的錯誤。

**修復 - 步驟說明：**

1. 開啟 [https://portal.azure.com](https://portal.azure.com)。
2. 在頂部搜尋欄輸入您的<strong>Foundry 專案</strong>名稱（例如 `workshop-agents`）。
3. **重要：** 點擊顯示類型為 **"Microsoft Foundry project"** 的結果，**不要點擊父帳戶/集線器資源**。這些是不同的資源，擁有不同的 RBAC 範圍。
4. 在專案頁面左側導覽中，點擊 **存取控制 (IAM)**。
5. 點擊 <strong>角色指派</strong> 標籤，檢查您是否已有該角色：
   - 搜尋您的名字或電子郵件。
   - 如果已列出 `Azure AI User` → 錯誤原因另有他因（請參閱下面第 8 步）。
   - 如果未列出 → 繼續新增。
6. 點擊 **+ 新增** → <strong>新增角色指派</strong>。
7. 在 <strong>角色</strong> 標籤：
   - 搜尋 [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles)。
   - 從結果中選擇。
   - 點擊 <strong>下一步</strong>。
8. 在 <strong>成員</strong> 標籤：
   - 選擇 **使用者、群組或服務主體**。
   - 點擊 **+ 選取成員**。
   - 搜尋您的名字或電子郵件地址。
   - 從結果中選擇您自己。
   - 點擊 <strong>選取</strong>。
9. 點擊 **檢閱 + 指派** → 再次點擊 **檢閱 + 指派**。
10. **等候 1-2 分鐘** - RBAC 權限變更需要時間生效。
11. 重試失敗的操作。

> **為什麼擁有者或協作者不足夠：** Azure RBAC 具有兩種類型的權限 - <em>管理操作</em> 和 <em>資料操作</em>。擁有者與協作者授予管理操作（建立資源、編輯設定），但 Agent 操作需要 `agents/write` 的 <strong>資料操作</strong> 權限，而該權限僅包含在 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner` 角色中。詳見 [Foundry RBAC 文件](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 在資源建立過程中出現 `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**根本原因：** 您沒有在此訂閱或資源群組中建立或修改 Azure 資源的權限。

**修復：**
1. 請您的訂閱管理員在 Foundry 專案所在的資源群組中，指派您 <strong>協作者</strong> 角色。
2. 或者，請他們為您建立 Foundry 專案，並在專案上指派您 **Azure AI User**。

### 1.3 訂閱未註冊 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) 導致 `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**根本原因：** Azure 訂閱尚未註冊 Foundry 需要的資源提供者。

**修復：**

1. 開啟終端機並執行：
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. 等待註冊完成（通常需 1-5 分鐘）：
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   預期輸出：`"Registered"`
3. 重試操作。

---

## 2. Docker 錯誤（僅限安裝了 Docker 時）

> Docker 是此工作坊的<strong>選用</strong>項目。以下錯誤只適用於已安裝 Docker Desktop，且 Foundry 擴充嘗試本地容器建置時。

### 2.1 Docker 服務未啟動

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**修復 - 步驟說明：**

1. 從開始功能表（Windows）或應用程式（macOS）中找到 Docker Desktop 並啟動。
2. 等待 Docker Desktop 視窗顯示 **"Docker Desktop is running"** — 通常需 30-60 秒。
3. 在系統通知區（Windows）或選單列（macOS）尋找 Docker 鯨魚圖示，滑鼠懸停確認狀態。
4. 在終端機中確認：
   ```powershell
   docker info
   ```
   如果此指令輸出 Docker 系統資訊（伺服器版本、儲存驅動等），表示 Docker 正在運行。
5. **Windows 專用：** 如果 Docker 仍無法啟動：
   - 開啟 Docker Desktop → <strong>設定</strong>（齒輪圖示）→ <strong>一般</strong>。
   - 確認勾選了 **使用基於 WSL 2 的引擎**。
   - 點擊 <strong>套用並重啟</strong>。
   - 若尚未安裝 WSL 2，請使用以系統管理員身份執行的 PowerShell 執行 `wsl --install`，然後重新啟動電腦。
6. 重試部署。

### 2.2 Docker 建置失敗，出現依賴錯誤

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**修復：**
1. 開啟 `requirements.txt`，確認所有套件名稱拼寫正確無誤。
2. 確認版本鎖定定義正確：
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. 先在本機測試安裝：
   ```bash
   pip install -r requirements.txt
   ```
4. 如使用私人套件索引，確保 Docker 有網路連線權限。

### 2.3 容器平臺不符（Apple Silicon）

若從 Apple Silicon Mac（M1/M2/M3/M4）部署，容器必須建置為 `linux/amd64`，因為 Foundry 的容器執行時使用 AMD64 架構。

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry 擴充的 deploy 指令在大多數情況下會自動處理。如有架構相關錯誤，請使用 `--platform` 標誌手動建置，並聯絡 Foundry 團隊。

---

## 3. 認證錯誤

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) 無法取得令牌

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**根本原因：** `DefaultAzureCredential` 鏈中無任何來源有有效令牌。

**修復 - 按順序嘗試每一步：**

1. **透過 Azure CLI 重新登入**（最常見辦法）：
   ```bash
   az login
   ```
   瀏覽器視窗開啟，完成登入後返回 VS Code。

2. **設定正確的訂閱：**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   若非正確訂閱：
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **透過 VS Code 重新登入：**
   - 點擊左下角的 <strong>帳戶</strong> 圖示（人形圖示）。
   - 點擊您的帳戶名稱 → <strong>登出</strong>。
   - 再點擊帳戶圖示 → **登入 Microsoft**。
   - 完成瀏覽器登入流程。

4. **服務主體（僅 CI/CD 場景）：**
   - 在 `.env` 設定以下環境變數：
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - 重新啟動您的代理程式。

5. **檢查令牌快取：**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   若失敗，表示您 CLI 令牌已過期。請重新執行 `az login`。

### 3.2 本地令牌有效但託管部署失敗

**根本原因：** 託管代理使用系統管理身分識別，與您的個人憑證不同。

**修復：** 這是預期行為 — 在部署時會自動配置管理身分識別。若託管代理仍出現認證錯誤：
1. 檢查 Foundry 專案的管理身分識別是否有權存取 Azure OpenAI 資源。
2. 確認 `agent.yaml` 中的 `PROJECT_ENDPOINT` 是否正確。

---

## 4. 模型錯誤

### 4.1 找不到模型部署

```
Error: Model deployment not found / The specified deployment does not exist
```

**修復 - 步驟說明：**

1. 開啟 `.env` 文件，記下 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 的值。
2. 在 VS Code 中開啟 **Microsoft Foundry** 側邊欄。
3. 展開您的專案 → **Model Deployments**。
4. 比對側邊欄列出的部署名稱與 `.env` 中的值。
5. 名稱<strong>區分大小寫</strong> — 例如 `gpt-4o` 與 `GPT-4o` 不相同。
6. 若不符，請更新 `.env` 使用側邊欄的確切名稱。
7. 託管部署時，亦請更新 `agent.yaml`：
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 模型回應不符合預期

**修復：**
1. 檢查 `main.py` 中的 `EXECUTIVE_AGENT_INSTRUCTIONS` 常數，確認未被截斷或破損。
2. 確認模型溫度設定（如果可配置）— 較低值提供較確定的輸出。
3. 比較所部署模型（例如 `gpt-4o` 對比 `gpt-4o-mini`）— 不同模型功能不同。

---

## 5. 部署錯誤

### 5.1 ACR 拉取授權

```
Error: AcrPullUnauthorized
```

**根本原因：** Foundry 專案的管理身分識別無法從 Azure Container Registry 拉取容器映像。

**修復 - 步驟說明：**

1. 開啟 [https://portal.azure.com](https://portal.azure.com)。
2. 在頂部搜尋欄搜尋 **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**。
3. 點擊與您的 Foundry 專案相關聯的 Container Registry（通常位於同一資源群組）。
4. 在左側導覽中點擊 **存取控制 (IAM)**。
5. 點擊 **+ 新增** → <strong>新增角色指派</strong>。
6. 搜尋並選擇 **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** 角色，點擊 <strong>下一步</strong>。
7. 選擇 <strong>管理身分識別</strong> → 點擊 **+ 選取成員**。
8. 尋找並選取 Foundry 專案的管理身分識別。
9. 點擊 <strong>選取</strong> → **檢閱 + 指派** → 再次點擊 **檢閱 + 指派**。

> 此角色指派通常由 Foundry 擴充自動設定。若看到此錯誤，可能自動設定失敗。您也可以嘗試重新部署 — 擴充會重試設定。

### 5.2 Agent 部署後無法啟動

**症狀：** 容器狀態持續顯示「待命」超過 5 分鐘或顯示「失敗」。

**修復 - 步驟說明：**

1. 開啟 VS Code 的 **Microsoft Foundry** 側邊欄。
2. 點擊您的託管代理 → 選擇版本。
3. 在詳細面板中，檢查 **Container Details** → 尋找 **Logs** 區段或連結。
4. 閱讀容器啟動日誌。常見原因：

| 日誌訊息 | 原因 | 修復方案 |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | 缺少相依套件 | 加入 `requirements.txt` 並重新部署 |
| `KeyError: 'PROJECT_ENDPOINT'` | 缺少環境變數 | 在 `agent.yaml` 的 `env:`下新增該變數 |
| `OSError: [Errno 98] Address already in use` | 連接埠衝突 | 確認 `agent.yaml` 設定 `port: 8088` 且只有一個程序監聽該端口 |
| `ConnectionRefusedError` | Agent 未開始監聽 | 檢查 `main.py` — 必須在啟動時執行 `from_agent_framework()` 呼叫 |

5. 修正問題後，參照 [Module 6](06-deploy-to-foundry.md) 重新部署。

### 5.3 部署超時

**修復：**
1. 檢查網路連線 — Docker 推送相當大（首次部署可能超過 100MB）。
2. 若您位於企業代理後方，確認 Docker Desktop 代理設定：
   **Docker Desktop** → <strong>設定</strong> → <strong>資源</strong> → <strong>代理</strong>。
3. 再試一次 — 網路偶發異常可能導致短暫失敗。

---

## 6. 快速參考：RBAC 角色

| 角色 | 典型範圍 | 授權內容 |
|------|----------|----------|
| **Azure AI User** | 專案 | 資料操作：建置、部署及調用代理 (`agents/write`, `agents/read`) |
| **Azure AI Developer** | 專案或帳戶 | 資料操作 + 專案建立權限 |
| **Azure AI Owner** | 帳戶 | 完全存取 + 角色指派管理權限 |
| **Azure AI Project Manager** | 專案 | 資料操作 + 可指派 Azure AI User 給他人 |
| **Contributor** | 訂閱/資源群組 | 管理操作（建立/刪除資源）。<strong>不包含資料操作</strong> |
| **Owner** | 訂閱/資源群組 | 管理操作 + 角色指派。<strong>不包含資料操作</strong> |
| **Reader** | 任何 | 管理只讀存取 |

> **重點說明：** `Owner` 和 `Contributor` <strong>不包含</strong>資料操作權限。Agent 操作始終需 `Azure AI *` 角色。此工作坊最低需求角色為<strong>專案層級</strong>的 **Azure AI User**。

---

## 7. 工作坊完成檢查清單

作為完成所有步驟的最終確認：

| # | 項目 | 模組 | 通過？ |
|---|------|--------|---|
| 1 | 已安裝並驗證所有先決條件 | [00](00-prerequisites.md) | |
| 2 | 已安裝 Foundry Toolkit 及 Foundry 擴充套件 | [01](01-install-foundry-toolkit.md) | |
| 3 | 已建立 Foundry 專案（或選取既有專案） | [02](02-create-foundry-project.md) | |
| 4 | 已部署模型（例如，gpt-4o） | [02](02-create-foundry-project.md) | |
| 5 | 已在專案範圍內指派 Azure AI 使用者角色 | [02](02-create-foundry-project.md) | |
| 6 | 已建立託管代理專案骨架（agent/） | [03](03-create-hosted-agent.md) | |
| 7 | 已在 `.env` 設定 PROJECT_ENDPOINT 和 MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | 代理指令已在 main.py 自訂 | [04](04-configure-and-code.md) | |
| 9 | 已建立虛擬環境並安裝依賴程式庫 | [04](04-configure-and-code.md) | |
| 10 | 使用 F5 或終端機於本機測試代理（4 項冒煙測試通過） | [05](05-test-locally.md) | |
| 11 | 已部署至 Foundry 代理服務 | [06](06-deploy-to-foundry.md) | |
| 12 | 容器狀態顯示「已啟動」或「執行中」 | [06](06-deploy-to-foundry.md) | |
| 13 | 在 VS Code Playground 驗證（4 項冒煙測試通過） | [07](07-verify-in-playground.md) | |
| 14 | 在 Foundry Portal Playground 驗證（4 項冒煙測試通過） | [07](07-verify-in-playground.md) | |

> **恭喜！** 若所有項目均已勾選，代表你已完成整個工作坊。你從零開始建置了一個託管代理，於本機測試，部署到 Microsoft Foundry，並在生產環境中驗證成功。

---

**上一篇：** [07 - 在 Playground 中驗證](07-verify-in-playground.md) · **主頁：** [工作坊 README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件是使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯的。雖然我們致力於確保準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始語言的文件應視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用此翻譯而引起的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->