# Module 8 - Troubleshooting

This module is a reference guide for common issues. Bookmark it and return when something goes wrong.

---

## 1. Permission errors

### 1.1 `agents/write` permission denied

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Root cause:** Missing `Azure AI User` role at the **project** level. This is the #1 workshop error.

**Fix:**
1. Open [portal.azure.com](https://portal.azure.com).
2. Search for your Foundry **project** name → click the result of type **"Microsoft Foundry project"** (NOT parent account).
3. **Access control (IAM)** → **+ Add** → **Add role assignment**.
4. Role: **Azure AI User** → Next.
5. Members: Select yourself → Review + assign → Review + assign.
6. **Wait 1–2 minutes** → retry.

> **Why Owner/Contributor isn't enough:** These roles grant *management* actions only. Agent operations require the `agents/write` *data action*, which is only in `Azure AI User`, `Azure AI Developer`, or `Azure AI Owner`. See [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` during provisioning

**Fix:** Ask your admin to assign **Contributor** on the resource group, or have them create the project for you and grant you **Azure AI User** on it.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker errors

> Docker is **optional**. These only apply if Docker Desktop is installed and the extension attempts a local build.

### 2.1 Docker daemon not running

**Fix:** Start Docker Desktop → wait for "running" status → verify with `docker info` → retry.

### 2.2 Build fails with dependency errors

**Fix:** Verify `requirements.txt` spelling, test locally first: `pip install -r requirements.txt`.

### 2.3 Platform mismatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Authentication errors

### 3.1 `DefaultAzureCredential` fails

**Fix (try in order):**
1. `az login` (re-authenticate)
2. `az account set --subscription "<id>"` (correct subscription)
3. VS Code → Accounts → Sign Out → Sign In again
4. Verify: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token works locally but not hosted

**Expected:** Hosted agents use system-managed identity, not your credential. If the hosted agent gets auth errors:
- Verify `AZURE_AI_PROJECT_ENDPOINT` in `agent.yaml` is correct
- Check that the project's managed identity has model access

---

## 4. Model errors

### 4.1 Model deployment not found

**Fix:** The name is **case-sensitive**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` with the exact name in the Foundry sidebar → Models.

### 4.2 Unexpected model output

**Fix:** Review `AGENT_INSTRUCTIONS` in `main.py` (not truncated?). Try a different model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Deployment errors

### 5.1 ACR pull unauthorized

**Fix:** Azure Portal → Container Registry → Access control (IAM) → Add **AcrPull** role to the Foundry project's managed identity.

### 5.2 Agent fails to start (stays "Pending" or "Failed")

Check container logs in the sidebar. Common causes:

| Log message | Fix |
|-------------|-----|
| `ModuleNotFoundError` | Add missing package to `requirements.txt`, redeploy |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Add env var to `agent.yaml` under `environment_variables` |
| `Address already in use` | Ensure only one process binds to port 8088 |

### 5.3 Deployment times out

**Fix:** Check internet connection. First deploy pushes >100MB. Behind a proxy? Configure Docker Desktop proxy settings.

---

## 6. Path B - Foundry Local

### 6.1 Foundry Local won't start

| Issue | Fix |
|-------|-----|
| `foundry: command not found` | Reinstall: `winget install Microsoft.FoundryLocal` |
| Insufficient resources | Foundry Local needs ~4GB RAM free. Close other apps. |
| Model download fails | Check disk space (models are 2–8 GB). Retry: `foundry local models pull <name>` |

### 6.2 Foundry Local model errors

| Issue | Fix |
|-------|-----|
| Slow responses | Expected - local models run on CPU unless you have a GPU. Be patient. |
| Poor quality output | Try a larger model if your hardware allows. `phi-4-mini` is a good balance. |
| Connection refused | Verify Foundry Local is running: `foundry local status`. Restart if needed. |

---

## 7. Quick reference: RBAC roles

| Role | Scope | Grants |
|------|-------|--------|
| **Azure AI User** | Project | Data actions: `agents/write`, `agents/read` |
| **Azure AI Developer** | Project/Account | Data actions + project creation |
| **Azure AI Owner** | Account | Full access + role management |
| **Contributor** | Subscription/RG | Management actions only (**no** data actions) |
| **Owner** | Subscription/RG | Management + role assignment (**no** data actions) |

---

## 8. Workshop completion checklist

| # | Item | Module |
|---|------|--------|
| 1 | Prerequisites installed and verified | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit extension installed, project connected (or Path B configured) | [01](01-setup.md) |
| 3 | Hosted agent scaffolded | [02](02-create-hosted-agent.md) |
| 4 | `.env` configured, instructions written, dependencies installed | [03](03-configure-and-code.md) |
| 5 | Agent tested locally - 3 functional scenarios pass | [04](04-test-locally.md) |
| 6 | Deployed to Foundry (Path A only) | [05](05-deploy-to-foundry.md) |
| 7 | Edge-case/safety tests pass in cloud (Path A only) | [06](06-verify-in-playground.md) |
| 8 | Summary reviewed, next steps identified | [07](07-summary.md) |

---

**Previous:** [07 - Summary](07-summary.md) · **Home:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->