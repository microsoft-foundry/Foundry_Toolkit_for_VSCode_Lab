# Module 8 - Troubleshooting

Dis module na reference guide for every common wahala wey person fit face during workshop. Bookmark am - you go come back to am anytime something no work.

---

## 1. Permission errors

### 1.1 `agents/write` permission denied

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Root cause:** You no get di `Azure AI User` role for di **project** level. Dis na di most common wahala for di workshop.

**Fix - step by step:**

1. Open [https://portal.azure.com](https://portal.azure.com).
2. For di top search bar, type di name of your **Foundry project** (ex: `workshop-agents`).
3. **Critical:** Click di result wey show type **"Microsoft Foundry project"**, NO di parent account/hub resource. Dem na different resources with different RBAC scopes.
4. For left navigation of di project page, click **Access control (IAM)**.
5. Click di **Role assignments** tab to check if you don get di role before:
   - Search for your name or email.
   - If `Azure AI User` don dey there → di wahala get anoda cause (check Step 8 below).
   - If no dey there → continue to add am.
6. Click **+ Add** → **Add role assignment**.
7. For **Role** tab:
   - Search for [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Select am from di results.
   - Click **Next**.
8. For **Members** tab:
   - Select **User, group, or service principal**.
   - Click **+ Select members**.
   - Search your name or email address.
   - Select yourself from di results.
   - Click **Select**.
9. Click **Review + assign** → **Review + assign** again.
10. **Wait 1-2 minutes** - RBAC changes dey take time to reach everywhere.
11. Retry di operation wey fail.

> **Why Owner/Contributor no dey enough:** Azure RBAC get two types of permissions - *management actions* and *data actions*. Owner and Contributor dey give management actions (create resources, edit settings), but agent operations need di `agents/write` **data action**, wey only dey inside `Azure AI User`, `Azure AI Developer`, or `Azure AI Owner` roles. See [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` during resource provisioning

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Root cause:** You no get permission to create or modify Azure resources for dis subscription/resource group.

**Fix:**
1. Ask your subscription administrator make e assign you the **Contributor** role for the resource group wey your Foundry project dey.
2. Or, make dem create the Foundry project for you and give you **Azure AI User** for the project.

### 1.3 `SubscriptionNotRegistered` for [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Root cause:** Azure subscription never register the resource provider wey Foundry need.

**Fix:**

1. Open terminal run:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Wait make registration complete (fit take 1-5 minutes):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Expected output: `"Registered"`
3. Retry di operation.

---

## 2. Docker errors (only if Docker dey installed)

> Docker na **optional** for dis workshop. Dis errors dey apply only if you get Docker Desktop wey install and Foundry extension dey try build local container.

### 2.1 Docker daemon no dey run

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Fix - step by step:**

1. **Find Docker Desktop** for your Start menu (Windows) or Applications (macOS) open am.
2. Wait till Docker Desktop window talk **"Docker Desktop is running"** - usually e dey take 30-60 seconds.
3. Find Docker whale icon for your system tray (Windows) or menu bar (macOS). Hold your mouse on top to check status.
4. Verify for terminal:
   ```powershell
   docker info
   ```
   If e show Docker system info (Server Version, Storage Driver, etc.), Docker dey run.
5. **Windows special:** If Docker still no dey start:
   - Open Docker Desktop → **Settings** (gear icon) → **General**.
   - Make sure **Use the WSL 2 based engine** dey checked.
   - Click **Apply & restart**.
   - If WSL 2 never install, run `wsl --install` as admin for PowerShell then restart your PC.
6. Retry di deployment.

### 2.2 Docker build fail with dependency errors

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Fix:**
1. Open `requirements.txt` check say all package names correct.
2. Make sure version pinning correct:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Test the install locally first:
   ```bash
   pip install -r requirements.txt
   ```
4. If you dey use private package index, make sure Docker get network access to am.

### 2.3 Container platform mismatch (Apple Silicon)

If you dey deploy from Apple Silicon Mac (M1/M2/M3/M4), di container must build for `linux/amd64` because Foundry container runtime dey use AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry extension deploy command dey handle dis automatically most times. If you see architecture errors, build manually with `--platform` flag and contact Foundry team.

---

## 3. Authentication errors

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) no fit get token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Root cause:** None of di credential sources inside `DefaultAzureCredential` chain get valid token.

**Fix - try all steps one by one:**

1. **Re-login with Azure CLI** (most common fix):
   ```bash
   az login
   ```
   Browser window go open. Sign in, then come back to VS Code.

2. **Set the correct subscription:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   If na wrong subscription:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Re-login with VS Code:**
   - Click **Accounts** icon (person icon) at bottom-left for VS Code.
   - Click your account name → **Sign Out**.
   - Click Accounts icon again → **Sign in to Microsoft**.
   - Complete browser sign-in flow.

4. **Service principal (CI/CD only):**
   - Set dis environment variables inside `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Then restart your agent process.

5. **Check token cache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   If e fail, your CLI token don expire. Run `az login` again.

### 3.2 Token dey work locally but no work for hosted deployment

**Root cause:** Hosted agent dey use system-managed identity, e different from your personal credential.

**Fix:** This na expected behavior - managed identity go automatically dey provision during deployment. If hosted agent still dey get auth wahala:
1. Check say Foundry project managed identity get access to Azure OpenAI resource.
2. Verify `PROJECT_ENDPOINT` inside `agent.yaml` correct.

---

## 4. Model errors

### 4.1 Model deployment no dey found

```
Error: Model deployment not found / The specified deployment does not exist
```

**Fix - step by step:**

1. Open your `.env` file check di value of `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Open **Microsoft Foundry** sidebar for VS Code.
3. Expand your project → **Model Deployments**.
4. Compare di deployment name wey dey there with your `.env` value.
5. Di name get **case-sensitive** - `gpt-4o` no be di same as `GPT-4o`.
6. If dem no match, update your `.env` to use the exact name wey dey the sidebar.
7. For hosted deployment, also update `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model dey respond with unexpected content

**Fix:**
1. Check di `EXECUTIVE_AGENT_INSTRUCTIONS` constant inside `main.py`. Make sure e no cut or corrupt.
2. Check model temperature setting (if configurable) - lower values dey give more deterministic output.
3. Compare the model wey deploy (ex: `gpt-4o` vs `gpt-4o-mini`) - different models get different capability.

---

## 5. Deployment errors

### 5.1 ACR pull authorization

```
Error: AcrPullUnauthorized
```

**Root cause:** Foundry project managed identity no fit pull container image from Azure Container Registry.

**Fix - step by step:**

1. Open [https://portal.azure.com](https://portal.azure.com).
2. Search **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** for top search bar.
3. Click the registry wey associate with your Foundry project (usually e dey the same resource group).
4. For left navigation, click **Access control (IAM)**.
5. Click **+ Add** → **Add role assignment**.
6. Search for **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** and select am. Click **Next**.
7. Select **Managed identity** → click **+ Select members**.
8. Find and select Foundry project’s managed identity.
9. Click **Select** → **Review + assign** → **Review + assign**.

> Usually dis role assignment dey set up automatically by Foundry extension. If you see dis error, automatic setup fit fail. You fit still try redeploy - extension fit try setup again.

### 5.2 Agent no fit start after deployment

**Symptoms:** Container status still "Pending" for more than 5 minutes or e show "Failed".

**Fix - step by step:**

1. Open **Microsoft Foundry** sidebar for VS Code.
2. Click on your hosted agent → select di version.
3. For di detail panel, check **Container Details** → find **Logs** section or link.
4. Read container startup logs. Common causes:

| Log message | Cause | Fix |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Missing dependency | Add am to `requirements.txt` and redeploy |
| `KeyError: 'PROJECT_ENDPOINT'` | Missing environment variable | Add di env var to `agent.yaml` under `env:` |
| `OSError: [Errno 98] Address already in use` | Port conflict | Make sure `agent.yaml` get `port: 8088` and only one process dey bind am |
| `ConnectionRefusedError` | Agent no start to listen | Check `main.py` - di `from_agent_framework()` call must run on startup |

5. Fix di issue, then redeploy from [Module 6](06-deploy-to-foundry.md).

### 5.3 Deployment time don pass finish

**Fix:**
1. Check your internet connection - Docker push fit dey big (>100MB for first deploy).
2. If you dey behind corporate proxy, make sure Docker Desktop proxy settings set correct: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Try again - network wahala fit cause small failure wey go clear.

---

## 6. Quick reference: RBAC roles

| Role | Typical scope | Wetin e grant |
|------|---------------|----------------|
| **Azure AI User** | Project | Data actions: build, deploy, and invoke agents (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Project or Account | Data actions + project creation |
| **Azure AI Owner** | Account | Full access + role assignment management |
| **Azure AI Project Manager** | Project | Data actions + fit assign Azure AI User to oda people |
| **Contributor** | Subscription/RG | Management actions (create/delete resources). **No dey include data actions** |
| **Owner** | Subscription/RG | Management actions + role assignment. **No dey include data actions** |
| **Reader** | Any | Read-only management access |

> **Key takeaway:** `Owner` and `Contributor` no include data actions. You always need `Azure AI *` role for agent operations. Minimum role for dis workshop na **Azure AI User** for di **project** scope.

---

## 7. Workshop completion checklist

Use dis as final confirmation say you don complete everything:

| # | Item | Module | Pass? |
|---|------|--------|---|
| 1 | All prerequisites install and verified | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit and Foundry extensions install | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry project create (or existing project select) | [02](02-create-foundry-project.md) | |
| 4 | Model wey dem don deploy (e.g., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI User role don assign for project scope | [02](02-create-foundry-project.md) | |
| 6 | Hosted agent project don scaffold (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` don configure with PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agent instructions don customize for main.py | [04](04-configure-and-code.md) | |
| 9 | Virtual environment don create and dependencies don install | [04](04-configure-and-code.md) | |
| 10 | Agent don test locally with F5 or terminal (4 smoke tests don pass) | [05](05-test-locally.md) | |
| 11 | Dem don deploy am to Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Container status dey show "Started" or "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Dem don verify am for VS Code Playground (4 smoke tests don pass) | [07](07-verify-in-playground.md) | |
| 14 | Dem don verify am for Foundry Portal Playground (4 smoke tests don pass) | [07](07-verify-in-playground.md) | |

> **Congratulations!** If everytin don tick, you don finish the whole workshop. You don build hosted agent from scratch, test am locally, deploy am to Microsoft Foundry, and you check am well for production.

---

**Previous:** [07 - Verify in Playground](07-verify-in-playground.md) · **Home:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Dis dokument don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even though we dey try make am correct, abeg sabi say automated translations fit get errors or mistakes. Di original dokument for im main language na di correct source. For important mata, better make professional human translation do am. We no go responsible for any misunderstanding or wrong meaning wey fit happen from using dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->