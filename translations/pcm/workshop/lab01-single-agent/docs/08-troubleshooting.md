# Module 8 - Troubleshooting

Dis module na reference guide for common palava dem. Bookmark am come back when sometin no dey work.

---

## 1. Permission errors

### 1.1 `agents/write` permission denied

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Root cause:** No `Azure AI User` role for the **project** level. Na dis one be the #1 workshop mistake.

**Fix:**
1. Open [portal.azure.com](https://portal.azure.com).
2. Search your Foundry **project** name → click the result wey be **"Microsoft Foundry project"** (NO be parent account).
3. **Access control (IAM)** → **+ Add** → **Add role assignment**.
4. Role: **Azure AI User** → Next.
5. Members: Choose yourself → Review + assign → Review + assign.
6. **Wait 1–2 minutes** → try again.

> **Why Owner/Contributor no too enough:** Dis roles only dey give *management* actions. Agent operations need `agents/write` *data action*, wey dey only for `Azure AI User`, `Azure AI Developer`, or `Azure AI Owner`. Check [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` during provisioning

**Fix:** Ask your admin to add you **Contributor** for the resource group, or make dem create the project for you and give you **Azure AI User** on top am.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker errors

> Docker na **optional**. Dis tins dey only happen if Docker Desktop don install and the extension try to build locally.

### 2.1 Docker daemon no dey run

**Fix:** Start Docker Desktop → wait till e say "running" → check with `docker info` → try again.

### 2.2 Build fail with dependency palava

**Fix:** Check spelling for `requirements.txt`, test am local first: `pip install -r requirements.txt`.

### 2.3 Platform mismatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Authentication errors

### 3.1 `DefaultAzureCredential` fail

**Fix (try am one by one):**
1. `az login` (login again)
2. `az account set --subscription "<id>"` (set correct subscription)
3. VS Code → Accounts → Sign Out → Sign In again
4. Check: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token dey work local but no work for hosted

**Wetin suppose happen:** Hosted agents dey use system-managed identity, no be your credential. If hosted agent get auth palava:
- Check say `AZURE_AI_PROJECT_ENDPOINT` for `agent.yaml` correct
- Check say project managed identity get model access

---

## 4. Model errors

### 4.1 Model deployment no dey find

**Fix:** Name dey **case-sensitive**. Check `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` with correct name for Foundry sidebar → Models.

### 4.2 Model output no be wetin you expect

**Fix:** Check `AGENT_INSTRUCTIONS` inside `main.py` (no truncate?). Try another model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Deployment errors

### 5.1 ACR pull no authorize

**Fix:** Go Azure Portal → Container Registry → Access control (IAM) → Add **AcrPull** role give Foundry project managed identity.

### 5.2 Agent no fit start (still "Pending" or "Failed")

Check container logs for sidebar. Common cause be:

| Log message | Fix |
|-------------|-----|
| `ModuleNotFoundError` | Add missing package to `requirements.txt`, deploy again |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Add env var to `agent.yaml` under `environment_variables` |
| `Address already in use` | Make sure say only one process dey bind port 8088 |

### 5.3 Deployment time don finish before e ready

**Fix:** Check your internet connection. First deploy dey push >100MB. You dey behind proxy? Setup your Docker Desktop proxy settings.

---

## 6. Path B - Foundry Local

### 6.1 Foundry Local no fit start

| Palava | Fix |
|-------|-----|
| `foundry: command not found` | Reinstall: `winget install Microsoft.FoundryLocal` |
| Not enough resources | Foundry Local need about 4GB RAM free. Close other programs. |
| Model download no fit complete | Check disk space (models get 2–8 GB). Try again: `foundry local models pull <name>` |

### 6.2 Foundry Local model errors

| Palava | Fix |
|-------|-----|
| Slow response | Na normal - local models go run on CPU unless you get GPU. Make you patient. |
| Output quality bad | Try bigger model if your hardware fit handle am. `phi-4-mini` na good balance. |
| Connection refuse | Check say Foundry Local dey run: `foundry local status`. Restart am if you need. |

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
| 1 | Prerequisites install and confirm | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit extension install, project connect (or Path B configure) | [01](01-setup.md) |
| 3 | Hosted agent setup | [02](02-create-hosted-agent.md) |
| 4 | `.env` configure, instructions write, dependencies install | [03](03-configure-and-code.md) |
| 5 | Agent test local - 3 working scenarios pass | [04](04-test-locally.md) |
| 6 | Deploy to Foundry (Path A only) | [05](05-deploy-to-foundry.md) |
| 7 | Edge-case/safety tests pass for cloud (Path A only) | [06](06-verify-in-playground.md) |
| 8 | Summary check, next steps find | [07](07-summary.md) |

---

**Previous:** [07 - Summary](07-summary.md) · **Home:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->