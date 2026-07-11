# Module 8 - Troubleshooting

Dis module dey cover common wahala, how to fix dem, and debugging strategies specific to the multi-agent workflow.

## Agent output issues

### GapAnalyzer talk “I still no get the matching report”

**Symptom:** GapAnalyzer response dey tell you to paste matching report wey get “Missing Skills” and “Certification Gaps.” E dey happen even if you don send both resume and job description.

**Cause:** The JD text no pass go JD Agent. With `context_mode="last_agent"`, `resume_executor` na only executor wey see di user original message. If `RESUME_PARSER_INSTRUCTIONS` no put the JD text inside the output, JD Agent no get JD to parse, MatchingAgent no fit compute fit score, and GapAnalyzer go get useless input.

**Diagnosis:**

For the server logs, look for the MatchingAgent span. If e get:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
di pass-through dey miss or broken.

**Fix:** Confirm sey `RESUME_PARSER_INSTRUCTIONS` for `main.py` get the `[JOB DESCRIPTION PASS-THROUGH]` section and the rule:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Also confirm sey `JOB_DESCRIPTION_INSTRUCTIONS` get `[PARSED RESUME PASS-THROUGH]` relay rule:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
If either instruction block na stub from the scaffold wizard, make you change am with the full version from [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent talk “Cannot compute fit score - no JD provided”

Dis na di same root cause as before. MatchingAgent receive JD Agent output but the `[PARSED RESUME PASS-THROUGH]` section no dey or e empty, so e no fit compare the two profiles. Confirm:
1. `JOB_DESCRIPTION_INSTRUCTIONS` get the relay rule: `Copy [PARSED RESUME] verbatim - the Matching Agent depend on am downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` tell the agent make e look for `[JD REQUIREMENTS]` and `[PARSED RESUME PASS-THROUGH]` sections.

Change both instruction blocks with the full versions from [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### The response show two times

**Symptom:** GapAnalyzer output (or whole pipeline output) dey show two times for the Agent Inspector response.

**Cause:** `WorkflowBuilder` dey use OR-semantics for incoming edges - downstream executor go fire as soon as **any** predecessor finish. If `matching_executor` get two incoming edges (one from `resume_executor` and one from `jd_executor`), e go fire two times: once when ResumeParser finish and again when JD Agent finish. GapAnalyzer then go run two times too.

**Fix:** Make sure sey the `WorkflowBuilder` graph na strictly sequential pipeline with no fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NO be from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

If you see stray `.add_edge(resume_executor, matching_executor)` line, make you remove am. The `[PARSED RESUME PASS-THROUGH]` relay inside JD Agent output don already give MatchingAgent access to the resume.

---

## Environment and configuration issues

### Missing or wrong `.env` values

The `.env` file must dey for `PersonalCareerCopilot/` directory (the same level as `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Wetin `.env` suppose get:

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
- Open the **Foundry Toolkit** sidebar for VS Code → right-click your project → **Copy Project Endpoint**. 
- Or waka go [Azure Portal](https://portal.azure.com) → your Foundry project → **Overview** → **Project endpoint**.

> **How to find your `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** For the Foundry Toolkit sidebar, expand your project → **Models** → find your deployed model name (e.g., `gpt-4.1-mini`).

### Env var precedence

`main.py` dey use `load_dotenv(override=True)`, wey mean:

| Priority | Source | E win if both dey set? |
|----------|--------|------------------------|
| 1 (highest) | `.env` file | Yes |
| 2 | Shell / container environment variable | E use am if the same key no dey inside `.env` |

For local development, dis one make `.env` be di source of truth (editing `.env` dey immediately affect runs). For hosted deployment, Foundry go inject environment variables for container level; since `.env` no dey as part of di deployed image for dis lab setup, the injected container values na dem go use.

---

## Version compatibility

### Package version matrix

Di multi-agent workflow need specific package versions. If versions no match, e go cause runtime errors.

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

**`AttributeError: module 'mcp.client' no get attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Check all versions at once

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

## Deployment issues

### Container no fit start after deployment

1. **Look container logs:**
   - Open the **Foundry Toolkit** sidebar → expand **Hosted Agents (Preview)** → click your agent → expand the version → **Container Details** → **Logs**.
   - Check for Python stack traces or missing module errors.

2. **Common container startup wahala:**

   | Error for logs | Cause | Fix |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` no get package | Add the package, unlock deploy again |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` or `.env` env vars no set | Update `agent.yaml` → `environment_variables` section (hosted) or `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity no configure | Foundry dey set am automatically - make sure say you deploy am via extension |
   | `OSError: port 8088 already in use` | Dockerfile expose wrong port or port conflict | Confirm `EXPOSE 8088` for Dockerfile and `CMD ["python", "main.py"]` |
   | Container exit with code 1 | Exception no handle inside `main()` | Test am for local first ([Module 5](05-test-locally.md)) to catch wahala before deploying |

3. **Deploy again after fixing:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → pick the same agent → deploy new version.

### Deployment dey take long

Multi-agent containers dey take longer to start because dem dey create 4 agent instances on startup. Normal startup time:

| Stage | Expected duration |
|-------|------------------|
| Container image build | 1-3 minutes |
| Image push to ACR | 30-60 seconds |
| Container start (single agent) | 15-30 seconds |
| Container start (multi-agent) | 30-120 seconds |
| Agent available inside Playground | 1-2 minutes after "Started" |

> If "Pending" status still dey pass 5 minutes, check container logs for errors.

---

## RBAC and permission wahala

### `403 Forbidden` or `AuthorizationFailed`

You need the **[Foundry User](https://aka.ms/foundry-ext-project-role)** role for your Foundry project (formerly called **Azure AI User** - role ID no change):

1. Go to [Azure Portal](https://portal.azure.com) → your Foundry **project** resource.
2. Click **Access control (IAM)** → **Role assignments**.
3. Search for your name → confirm **Foundry User** (or old name **Azure AI User**) dey there.
4. If e no dey: **Add** → **Add role assignment** → search for **Foundry User** → assign am to your account.

See the [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) docs for more info.

### Model deployment no dey accessible

If the agent dey show model-related errors:

1. Confirm the model deploy: Foundry sidebar → open project → **Models** → check if `gpt-4.1-mini` (or your model) status na **Succeeded**.
2. Confirm the deployment name dey match: compare `AZURE_AI_MODEL_DEPLOYMENT_NAME` inside `.env` (or `agent.yaml`) with the deployment name for the sidebar.
3. If deployment don expire (free tier): redeploy from [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local wahala (Path B)

### Foundry Local service no dey run

```powershell
# Make you check di status
foundry local status

# Start di service if e don stop already
foundry local start
```

| Symptom | Cause | Fix |
|---------|-------|-----|
| Health check return `503` | Service no start | `foundry local start` or click **Start** for Foundry Toolkit sidebar |
| Health check timeout | Model still dey load | Wait 30–60 seconds after start; big models go take more time |
| `StatusCode: 404` on `/v1/health` | Wrong port | Default na `5273`. Check `foundry local status` for real port |
| Insufficient resources | Foundry Local need ~4 GB RAM free | Close other apps |
| Model download fail | Low disk space | Models big pass 2–8 GB. Free space, then run `foundry model pull <name>` |

### Model name no match

```powershell
# List di downloaded model dem and dia correct alias dem
foundry model list
```

Set `AZURE_AI_MODEL_DEPLOYMENT_NAME` inside `.env` to exactly the alias wey show (e.g., `phi-4-mini`, no be `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` on local run (Path B)

The lab `main.py` use `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local need dis variable point to local service - **no be** `AZURE_AI_PROJECT_ENDPOINT`. Make sure your `.env` get:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP tool still dey make outbound call (Path B)

Dis one na normal. The `search_microsoft_learn_for_plan` tool dey fetch learning resources from `https://learn.microsoft.com/api/mcp`. **Only skill-name query** dey travel on network - resume and JD text dey processed fully for your device, e no ever transmit. If fully offline mode dey needed, add `try/except` fallback inside tool wey dey return static `learn.microsoft.com` URL if endpoint no reach.

---

## How to get help

If you jam wahala after you try all di fixes above:

1. **Check server logs** - Most errors go get Python stack trace for terminal. Read all the traceback.
2. **Search error message** - Copy the error text and search inside [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Open issue** - File issue on the [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) with:
   - Error message or screenshot
   - Your package versions (`pip list | Select-String "agent-framework"`)
   - Your Python version (`python --version`)
   - If di issue na local or after deployment

---

### Checkpoint

- [ ] You sabi how to check and fix `.env` configuration issues
- [ ] You fit verify package versions wey match the required matrix
- [ ] You sabi how to check container logs for deployment failures
- [ ] You fit verify RBAC roles for Azure Portal

---

**Previous:** [07 - Verify in Playground](07-verify-in-playground.md) · **Next:** [09 - Summary →](09-summary.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->