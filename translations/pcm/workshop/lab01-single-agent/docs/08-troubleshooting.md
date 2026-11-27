# Module 8 - Troubleshooting

Dis module na guide for common wahala dem. Bookmark am make you fit come back if something go wrong.

---

## 1. Permission errors

### 1.1 `agents/write` permission denied

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Root cause:** Dem never give `Azure AI User` role for **project** level. Na di commonest workshop error be dis.

**How to fix am:**
1. Open [portal.azure.com](https://portal.azure.com).
2. Search for your Foundry **project** name → click di result wey be **"Microsoft Foundry project"** (NO be parent account).
3. **Access control (IAM)** → **+ Add** → **Add role assignment**.
4. Role: **Azure AI User** → Next.
5. Members: Choose yourself → Review + assign → Review + assign.
6. **Wait 1–2 minutes** → try again.

> **Why Owner/Contributor no still enough:** Dis roles na only *management* actions dem de give. Agent operations need `agents/write` *data action*, wey dey only for `Azure AI User`, `Azure AI Developer`, or `Azure AI Owner`. See [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` during provisioning

**How to fix:** Make your admin assign **Contributor** for resource group, or make dem create di project for you and give you **Azure AI User** role for am.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker errors

> Docker na **optional**. Dis dem only go apply if Docker Desktop dey installed and di extension dey try local build.

### 2.1 Docker daemon no dey run

**How to fix:** Start Docker Desktop → wait make e show "running" status → check with `docker info` → try again.

### 2.2 Build fail with dependency errors

**How to fix:** Check `requirements.txt` spelling well, test am locally first: `pip install -r requirements.txt`.

### 2.3 Platform mismatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Authentication errors

### 3.1 `DefaultAzureCredential` fail

**How to fix am (try am one one):**
1. `az login` (login again)
2. `az account set --subscription "<id>"` (correct subscription)
3. VS Code → Accounts → Sign Out → Sign In again
4. Check: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token dey work locally but no dey work for hosted

**Wetin expect:** Hosted agents dey use system-managed identity, no be your credentials. If hosted agent dey get auth errors:
- Confirm `AZURE_AI_MODEL_DEPLOYMENT_NAME` for `agent.yaml` dey match your model deployment name (`FOUNDRY_PROJECT_ENDPOINT` na Foundry inject am during runtime - no make you declare am for `agent.yaml`)
- Make sure say di project's managed identity get access to model

---

## 4. Model errors

### 4.1 Model deployment no found

**How to fix:** Di name dey **case-sensitive**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` to di exact name for Foundry sidebar → Models.

### 4.2 Unexpected model output

**How to fix:** Check `AGENT_INSTRUCTIONS` for `main.py` (no cut short?). Try different model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Deployment errors

### 5.1 ACR pull no authorized

**How to fix:** Go Azure Portal → Container Registry → Access control (IAM) → Add **AcrPull** role to Foundry project's managed identity.

### 5.2 Agent no fit start (e just dey "Pending" or "Failed")

Check container logs for sidebar. Common causes:

| Log message | How to fix |
|-------------|----------|
| `ModuleNotFoundError` | Add missing package to `requirements.txt`, deploy again |
| `ValueError: Missing required environment variables` | Confirm `AZURE_AI_MODEL_DEPLOYMENT_NAME` dey declared in `agent.yaml` under `environment_variables` and get value, then deploy again. `FOUNDRY_PROJECT_ENDPOINT` na Foundry inject am during runtime |
| `Address already in use` | Make sure only one process dey bind to port 8088 |

### 5.3 Deployment time don finish before e complete

**How to fix:** Check your internet connection. First deploy dey push pass 100MB. You dey behind proxy? Configure Docker Desktop proxy settings.

---

## 6. Path B - Foundry Local

### 6.1 Foundry Local no fit start

| Wahala | How to fix |
|-------|----------|
| `foundry: command not found` | Reinstall: `winget install Microsoft.FoundryLocal` |
| No enough resources | Foundry Local need ~4GB RAM free. Close other apps. |
| Model download fail | Check disk space (models be 2–8 GB). Try again: `foundry local models pull <name>` |

### 6.2 Foundry Local model errors

| Wahala | How to fix |
|-------|----------|
| Slow responses | Na expected - local models dey run on CPU unless you get GPU. Make you patient. |
| Output quality bad | Try bigger model if your hardware fit handle am. `phi-4-mini` na better balance. |
| Connection refuse | Check say Foundry Local dey run: `foundry local status`. Restart if you need am. |

---

## 7. Quick reference: RBAC roles

| Role | Scope | Wetin e grant |
|------|-------|-------------|
| **Azure AI User** | Project | Data actions: `agents/write`, `agents/read` |
| **Azure AI Developer** | Project/Account | Data actions + project creation |
| **Azure AI Owner** | Account | Full access + role management |
| **Contributor** | Subscription/RG | Management actions only (**no** data actions) |
| **Owner** | Subscription/RG | Management + role assignment (**no** data actions) |

---

## 8. Workshop completion checklist

| # | Thing | Module |
|---|-------|--------|
| 1 | Prerequisites install and check | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit extension install, project connect (or Path B set up) | [01](01-setup.md) |
| 3 | Hosted agent scaffolded | [02](02-create-hosted-agent.md) |
| 4 | `.env` set up, instructions write, dependencies install | [03](03-configure-and-code.md) |
| 5 | Agent test locally - 3 functional scenarios pass | [04](04-test-locally.md) |
| 6 | Deploy go Foundry (Path A only) | [05](05-deploy-to-foundry.md) |
| 7 | Edge-case/safety tests pass for cloud (Path A only) | [06](06-verify-in-playground.md) |
| 8 | Summary check, next steps identify | [07](07-summary.md) |

---

**Previous:** [07 - Summary](07-summary.md) · **Home:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->