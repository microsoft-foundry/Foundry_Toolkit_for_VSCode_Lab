# Module 8 - Troubleshooting

This module is a reference guide for every common issue encountered during the workshop. Bookmark it - you'll come back to it whenever something goes wrong.

---

## 1. Permission errors

### 1.1 `agents/write` permission denied

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Root cause:** You don't have the `Azure AI User` role at the **project** level. This is the single most common error in the workshop.

**Fix - step by step:**

1. Open [https://portal.azure.com](https://portal.azure.com).
2. In the top search bar, type the name of your **Foundry project** (e.g., `workshop-agents`).
3. **Critical:** Click the result that shows type **"Microsoft Foundry project"**, NOT the parent account/hub resource. These are different resources with different RBAC scopes.
4. In the left navigation of the project page, click **Access control (IAM)**.
5. Click the **Role assignments** tab to check if you already have the role:
   - Search for your name or email.
   - If `Azure AI User` is already listed → the error has a different cause (check Step 8 below).
   - If not listed → proceed to add it.
6. Click **+ Add** → **Add role assignment**.
7. In the **Role** tab:
   - Search for [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Select it from the results.
   - Click **Next**.
8. In the **Members** tab:
   - Select **User, group, or service principal**.
   - Click **+ Select members**.
   - Search for your name or email address.
   - Select yourself from the results.
   - Click **Select**.
9. Click **Review + assign** → **Review + assign** again.
10. **Wait 1-2 minutes** - RBAC changes take time to propagate.
11. Retry the operation that failed.

> **Why Owner/Contributor isn't enough:** Azure RBAC has two types of permissions - *management actions* and *data actions*. Owner and Contributor grant management actions (create resources, edit settings), but agent operations require the `agents/write` **data action**, which is only included in `Azure AI User`, `Azure AI Developer`, or `Azure AI Owner` roles. See [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` during resource provisioning

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Root cause:** You don't have permission to create or modify Azure resources in this subscription/resource group.

**Fix:**
1. Ask your subscription administrator to assign you the **Contributor** role on the resource group where your Foundry project lives.
2. Alternatively, ask them to create the Foundry project for you and grant you **Azure AI User** on the project.

### 1.3 `SubscriptionNotRegistered` for [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Root cause:** The Azure subscription hasn't registered the resource provider needed for Foundry.

**Fix:**

1. Open a terminal and run:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Wait for registration to complete (can take 1-5 minutes):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Expected output: `"Registered"`
3. Retry the operation.

---

## 2. Docker errors (only if Docker is installed)

> Docker is **optional** for this workshop. These errors only apply if you have Docker Desktop installed and the Foundry extension attempts a local container build.

### 2.1 Docker daemon not running

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Fix - step by step:**

1. **Find Docker Desktop** in your Start menu (Windows) or Applications (macOS) and launch it.
2. Wait for the Docker Desktop window to show **"Docker Desktop is running"** - this typically takes 30-60 seconds.
3. Look for the Docker whale icon in your system tray (Windows) or menu bar (macOS). Hover over it to confirm status.
4. Verify in a terminal:
   ```powershell
   docker info
   ```
   If this prints Docker system information (Server Version, Storage Driver, etc.), Docker is running.
5. **Windows specific:** If Docker still won't start:
   - Open Docker Desktop → **Settings** (gear icon) → **General**.
   - Ensure **Use the WSL 2 based engine** is checked.
   - Click **Apply & restart**.
   - If WSL 2 isn't installed, run `wsl --install` in an elevated PowerShell and restart your computer.
6. Retry the deployment.

### 2.2 Docker build fails with dependency errors

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Fix:**
1. Open `requirements.txt` and verify all package names are spelled correctly.
2. Ensure the version pinning is correct:
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
4. If using a private package index, ensure Docker has network access to it.

### 2.3 Container platform mismatch (Apple Silicon)

If deploying from an Apple Silicon Mac (M1/M2/M3/M4), the container must be built for `linux/amd64` because Foundry's container runtime uses AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> The Foundry extension's deploy command handles this automatically in most cases. If you see architecture-related errors, build manually with the `--platform` flag and contact the Foundry team.

---

## 3. Authentication errors

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) fails to retrieve a token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Root cause:** None of the credential sources in the `DefaultAzureCredential` chain have a valid token.

**Fix - try each step in order:**

1. **Re-login via Azure CLI** (most common fix):
   ```bash
   az login
   ```
   A browser window opens. Sign in, then return to VS Code.

2. **Set the correct subscription:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   If this isn't the right subscription:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Re-login via VS Code:**
   - Click the **Accounts** icon (person icon) in the bottom-left of VS Code.
   - Click your account name → **Sign Out**.
   - Click the Accounts icon again → **Sign in to Microsoft**.
   - Complete the browser sign-in flow.

4. **Service principal (CI/CD scenarios only):**
   - Set these environment variables in your `.env`:
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
   If this fails, your CLI token has expired. Run `az login` again.

### 3.2 Token works locally but not in hosted deployment

**Root cause:** The hosted agent uses a system-managed identity, which is different from your personal credential.

**Fix:** This is expected behavior - the managed identity is automatically provisioned during deployment. If the hosted agent still gets auth errors:
1. Check that the Foundry project's managed identity has access to the Azure OpenAI resource.
2. Verify `PROJECT_ENDPOINT` in `agent.yaml` is correct.

---

## 4. Model errors

### 4.1 Model deployment not found

```
Error: Model deployment not found / The specified deployment does not exist
```

**Fix - step by step:**

1. Open your `.env` file and note the value of `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Open the **Microsoft Foundry** sidebar in VS Code.
3. Expand your project → **Model Deployments**.
4. Compare the deployment name listed there with your `.env` value.
5. The name is **case-sensitive** - `gpt-4o` is different from `GPT-4o`.
6. If they don't match, update your `.env` to use the exact name shown in the sidebar.
7. For hosted deployment, also update `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model responds with unexpected content

**Fix:**
1. Review the `EXECUTIVE_AGENT_INSTRUCTIONS` constant in `main.py`. Make sure it hasn't been truncated or corrupted.
2. Check the model temperature setting (if configurable) - lower values give more deterministic outputs.
3. Compare the model deployed (e.g., `gpt-4o` vs `gpt-4o-mini`) - different models have different capabilities.

---

## 5. Deployment errors

### 5.1 ACR pull authorization

```
Error: AcrPullUnauthorized
```

**Root cause:** The Foundry project's managed identity can't pull the container image from Azure Container Registry.

**Fix - step by step:**

1. Open [https://portal.azure.com](https://portal.azure.com).
2. Search for **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** in the top search bar.
3. Click on the registry associated with your Foundry project (it's typically in the same resource group).
4. In the left navigation, click **Access control (IAM)**.
5. Click **+ Add** → **Add role assignment**.
6. Search for **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** and select it. Click **Next**.
7. Select **Managed identity** → click **+ Select members**.
8. Find and select the Foundry project's managed identity.
9. Click **Select** → **Review + assign** → **Review + assign**.

> This role assignment is normally set up automatically by the Foundry extension. If you see this error, the automatic setup may have failed. You can also try redeploying - the extension may retry the setup.

### 5.2 Agent fails to start after deployment

**Symptoms:** Container status stays "Pending" for more than 5 minutes or shows "Failed".

**Fix - step by step:**

1. Open the **Microsoft Foundry** sidebar in VS Code.
2. Click on your hosted agent → select the version.
3. In the detail panel, check **Container Details** → look for a **Logs** section or link.
4. Read the container startup logs. Common causes:

| Log message | Cause | Fix |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Missing dependency | Add it to `requirements.txt` and redeploy |
| `KeyError: 'PROJECT_ENDPOINT'` | Missing environment variable | Add the env var to `agent.yaml` under `env:` |
| `OSError: [Errno 98] Address already in use` | Port conflict | Ensure `agent.yaml` has `port: 8088` and only one process binds to it |
| `ConnectionRefusedError` | Agent didn't start listening | Check `main.py` - the `from_agent_framework()` call must run on startup |

5. Fix the issue, then redeploy from [Module 6](06-deploy-to-foundry.md).

### 5.3 Deployment times out

**Fix:**
1. Check your internet connection - the Docker push can be large (>100MB for the first deploy).
2. If behind a corporate proxy, ensure Docker Desktop proxy settings are configured: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Try again - network hiccups can cause transient failures.

---

## 6. Quick reference: RBAC roles

| Role | Typical scope | What it grants |
|------|---------------|----------------|
| **Azure AI User** | Project | Data actions: build, deploy, and invoke agents (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Project or Account | Data actions + project creation |
| **Azure AI Owner** | Account | Full access + role assignment management |
| **Azure AI Project Manager** | Project | Data actions + can assign Azure AI User to others |
| **Contributor** | Subscription/RG | Management actions (create/delete resources). **Does NOT include data actions** |
| **Owner** | Subscription/RG | Management actions + role assignment. **Does NOT include data actions** |
| **Reader** | Any | Read-only management access |

> **Key takeaway:** `Owner` and `Contributor` do **NOT** include data actions. You always need an `Azure AI *` role for agent operations. The minimum role for this workshop is **Azure AI User** at the **project** scope.

---

## 7. Workshop completion checklist

Use this as a final sign-off that you've completed everything:

| # | Item | Module | Pass? |
|---|------|--------|---|
| 1 | All prerequisites installed and verified | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit and Foundry extensions installed | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry project created (or existing project selected) | [02](02-create-foundry-project.md) | |
| 4 | Model deployed (e.g., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI User role assigned at project scope | [02](02-create-foundry-project.md) | |
| 6 | Hosted agent project scaffolded (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` configured with PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agent instructions customized in main.py | [04](04-configure-and-code.md) | |
| 9 | Virtual environment created and dependencies installed | [04](04-configure-and-code.md) | |
| 10 | Agent tested locally with F5 or terminal (4 smoke tests passed) | [05](05-test-locally.md) | |
| 11 | Deployed to Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Container status shows "Started" or "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verified in VS Code Playground (4 smoke tests passed) | [07](07-verify-in-playground.md) | |
| 14 | Verified in Foundry Portal Playground (4 smoke tests passed) | [07](07-verify-in-playground.md) | |

> **Congratulations!** If all items are checked, you've completed the entire workshop. You've built a hosted agent from scratch, tested it locally, deployed it to Microsoft Foundry, and validated it in production.

---

**Previous:** [07 - Verify in Playground](07-verify-in-playground.md) · **Home:** [Workshop README](../../../README.md)