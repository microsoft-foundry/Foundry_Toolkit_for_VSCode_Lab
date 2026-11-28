# Module 8 - Troubleshooting

Dis module dey cover common error, how to fix dem, and debugging strategies wey concern di multi-agent workflow.

## Agent output wahala dem

### GapAnalyzer talk say “I still no get di matching report”

**Symptom:** GapAnalyzer answer dey ask you to put matching report wey get “Missing Skills” and “Certification Gaps.” Dis dey happen even when you don send both resume and job description.

**Cause:** Di JD text no pass go JD Agent. Wit `context_mode="last_agent"`, `resume_executor` na di only executor wey ever see di original user message. If `RESUME_PARSER_INSTRUCTIONS` no put di JD text for im output, JD Agent no get JD to parse, MatchingAgent no fit calculate fit score, and GapAnalyzer go get nonsense input.

**Diagnosis:**

For server logs, find MatchingAgent span. If e get:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
 di pass-through dey miss or e spoil.

**Fix:** Make sure say `RESUME_PARSER_INSTRUCTIONS` for `main.py` get `[JOB DESCRIPTION PASS-THROUGH]` section and di rule:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Also make sure say `JOB_DESCRIPTION_INSTRUCTIONS` get `[PARSED RESUME PASS-THROUGH]` relay rule:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
If any of dem na stub from di scaffold wizard, replace am wit full one from [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent talk “Cannot compute fit score - no JD provided”

Dis na di same root cause as above. MatchingAgent receive JD Agent output but di `[PARSED RESUME PASS-THROUGH]` section no dey or e empty, so e no fit compare di two profiles. Confirm:
1. `JOB_DESCRIPTION_INSTRUCTIONS` get di relay rule: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` tell di agent make e find `[JD REQUIREMENTS]` and `[PARSED RESUME PASS-THROUGH]` sections.

Replace both instruction blocks wit di full ones from [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Di response dey show two times

**Symptom:** GapAnalyzer output (or di whole pipeline output) dey appear two times for Agent Inspector response.

**Cause:** `WorkflowBuilder` dey use OR-semantics for incoming edges - downstream executor go fire as soon as **any** predecessor complete. If `matching_executor` get two incoming edges (one from `resume_executor` and one from `jd_executor`), e go fire two times: once wen ResumeParser finish and another wen JD Agent finish. GapAnalyzer go run two times too.

**Fix:** Make sure say di `WorkflowBuilder` graph na strictly sequential pipeline wey no get fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

If you see any stray `.add_edge(resume_executor, matching_executor)` line, remove am. Di `[PARSED RESUME PASS-THROUGH]` relay for JD Agent output don already give MatchingAgent access to di resume.

---

## Environment and configuration wahala dem

### Missing or wrong `.env` values

Di `.env` file must dey inside di `PersonalCareerCopilot/` directory (same level wit `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Expected `.env` content:

**Path A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Path B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Both paths dey use `FOUNDRY_PROJECT_ENDPOINT`. Di value different: cloud dey use `https://` Foundry endpoint; local dey use `http://localhost:5273/v1`. Run `foundry model list` to confirm di exact model alias for Path B.

> **How to find your `FOUNDRY_PROJECT_ENDPOINT`:** 
- Open di **Foundry Toolkit** sidebar for VS Code → right-click your project → **Copy Project Endpoint**. 
- Or waka go [Azure Portal](https://portal.azure.com) → your Foundry project → **Overview** → **Project endpoint**.

> **How to find your `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** For di Foundry Toolkit sidebar, expand your project → **Models** → find your deployed model name (e.g., `gpt-4.1-mini`).

### Env var precedence

`main.py` dey use `load_dotenv(override=True)`, wey mean:

| Priority | Source | Which one win if both set? |
|----------|--------|---------------------------|
| 1 (highest) | `.env` file | Yes |
| 2 | Shell / container environment variable | Na dis one if `.env` no get di same key |

For local development, dis one mean say `.env` na di source of truth (if you edit `.env` e go affect runs immediately). For hosted deployment, Foundry dey inject environment variables for container level; since `.env` no dey part of di deployed image for dis lab setup, di container injected values na dem dey use.

---

## Version compatibility

### Package version matrix

Di multi-agent workflow need specific package versions. Versions wey no match dey cause runtime errors.

| Package | Required Version | Check Command |
|---------|-----------------|---------------|
| `agent-framework-foundry` | latest | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | latest | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | latest | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Common version errors

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Verify all versions at once

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Expected output:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Deployment wahala dem

### Container no fit start after deployment

1. **Check container logs:**
   - Open di **Foundry Toolkit** sidebar → under your project, click **Agents** → **Hosted Agent** tab → click your agent. Check **Status** for di **Details** tab, then open di **Playground** tab and use di **Logs** tab inside **Session Details** panel to see di container output.
   - Look for Python stack traces or missing module errors.

2. **Common container startup failures:**

   | Error for logs | Cause | How to fix am |
   |---------------|-------|---------------|
   | `ModuleNotFoundError` | `requirements.txt` package miss | Add di package, then redeploy |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` or `.env` env vars no set | Update `agent.yaml` → `environment_variables` section (hosted) or `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity no configure | Foundry dey set am automatically - make sure you dey deploy wit extension |
   | `OSError: port 8088 already in use` | Dockerfile dey expose wrong port or port conflict | Check `EXPOSE 8088` for Dockerfile and `CMD ["python", "main.py"]` |
   | Container exit wit code 1 | Unhandled exception for `main()` | Test am locally first ([Module 5](05-test-locally.md)) to catch error before you deploy |

3. **Redeploy after you fix am:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → select di same agent → deploy new version.

### Deployment dey take long

Multi-agent containers dey take longer to start because dem dey create 4 agent instances on startup. Normal startup time dem:

| Stage | Expected duration |
|-------|------------------|
| Container image build | 1-3 minutes |
| Image push to ACR | 30-60 seconds |
| Container start (single agent) | 15-30 seconds |
| Container start (multi-agent) | 30-120 seconds |
| Agent available in Playground | 1-2 minutes after "Started" |

> If "Pending" status dey pass 5 minutes, check container logs for error.

---

## RBAC and permission wahala dem

### `403 Forbidden` or `AuthorizationFailed`

You need di **[Foundry User](https://aka.ms/foundry-ext-project-role)** role for your Foundry project (wey before dem dey call am **Azure AI User** - di role ID no change):

1. Go [Azure Portal](https://portal.azure.com) → your Foundry **project** resource.
2. Click **Access control (IAM)** → **Role assignments**.
3. Search your name → confirm say **Foundry User** (or old name **Azure AI User**) dey listed.
4. If e miss: **Add** → **Add role assignment** → find **Foundry User** → assign am to your account.

See di [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) docs for details.

### Model deployment no fit access

If di agent show model-related error:

1. Confirm say model deploy: Foundry sidebar → expand project → **Models** → look for `gpt-4.1-mini` (or your model) wit status **Succeeded**.
2. Confirm say deployment name match: compare `AZURE_AI_MODEL_DEPLOYMENT_NAME` inside `.env` (or `agent.yaml`) with di real deployment name in di sidebar.
3. If deployment don expire (free tier): redeploy from [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local wahala dem (Path B)

### Foundry Local service no dey run

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Symptom | Cause | Fix |
|---------|-------|-----|
| Health check dey return `503` | Service never start | `foundry local start` or click **Start** for Foundry Toolkit sidebar |
| Health check time out | Model still dey load | Wait 30–60 seconds after you start; big models dey take more time |
| `StatusCode: 404` on `/v1/health` | Wrong port | Default na `5273`. Check `foundry local status` for di correct port |
| Not enough resources | Foundry Local need ~4 GB RAM free | Close other apps |
| Model download fail | Disk space low | Models be 2–8 GB. Free space then `foundry model pull <name>` |

### Model name no match

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Set `AZURE_AI_MODEL_DEPLOYMENT_NAME` inside `.env` to di exact alias wey dem show (e.g., `phi-4-mini`, no be `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` on local run (Path B)

Di lab's `main.py` dey use `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local need this variable make e point to di local service - **no be** `AZURE_AI_PROJECT_ENDPOINT`. Make sure say your `.env` get:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP tool still dey make outbound call (Path B)

Dis one wey suppose happen. Di `search_microsoft_learn_for_plan` tool dey fetch learning resources from `https://learn.microsoft.com/api/mcp`. **Only di skill-name query** dey travel for network - resume and JD text dey process for your device only and dem no dey transmit. If you want full offline operation, add `try/except` fallback for di tool wey go give static `learn.microsoft.com` URL when endpoint no dey reachable.

---

## How to get help

If you jam wahala after you try di fixes above:

1. **Check server logs** - Most error go get Python stack trace for terminal. Read all di traceback well.
2. **Search di error message** - Copy di error text and search am for [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Open issue** - File issue for [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) with:
   - Di error message or screenshot
   - Your package versions (`pip list | Select-String "agent-framework"`)
   - Your Python version (`python --version`)
   - Whether di issue dey local or na after deployment

---

### Checkpoint

- [ ] You sabi how to check and fix `.env` configuration wahala dem
- [ ] You fit verify package versions match the required matrix
- [ ] You sabi how to check container logs for deployment failure
- [ ] You fit verify RBAC roles for Azure Portal

---

**Previous:** [07 - Verify in Playground](07-verify-in-playground.md) · **Next:** [09 - Summary →](09-summary.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->