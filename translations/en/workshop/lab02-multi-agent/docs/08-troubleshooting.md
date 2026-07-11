# Module 8 - Troubleshooting

This module covers common errors, fixes, and debugging strategies specific to the multi-agent workflow.

## Agent output issues

### GapAnalyzer says “I still don’t have the matching report”

**Symptom:** GapAnalyzer’s response asks you to paste a matching report with “Missing Skills” and “Certification Gaps.” This happens even when you sent both a resume and a job description.

**Cause:** The JD text was not passed downstream to JD Agent. With `context_mode="last_agent"`, `resume_executor` is the only executor that ever sees the user’s original message. If `RESUME_PARSER_INSTRUCTIONS` does not include the JD text in its output, JD Agent has no JD to parse, MatchingAgent cannot compute a fit score, and GapAnalyzer receives a meaningless input.

**Diagnosis:**

In the server logs, look for the MatchingAgent span. If it contains:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
the pass-through is missing or broken.

**Fix:** Confirm that `RESUME_PARSER_INSTRUCTIONS` in `main.py` contains a `[JOB DESCRIPTION PASS-THROUGH]` section and the rule:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Also confirm that `JOB_DESCRIPTION_INSTRUCTIONS` contains a `[PARSED RESUME PASS-THROUGH]` relay rule:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
If either instruction block is a stub from the scaffold wizard, replace it with the complete version from [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent outputs “Cannot compute fit score - no JD provided”

This is the same root cause as above. MatchingAgent received JD Agent’s output but the `[PARSED RESUME PASS-THROUGH]` section was missing or empty, so it couldn’t compare the two profiles. Confirm:
1. `JOB_DESCRIPTION_INSTRUCTIONS` includes the relay rule: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` tells the agent to look for `[JD REQUIREMENTS]` and `[PARSED RESUME PASS-THROUGH]` sections.

Replace both instruction blocks with the complete versions from [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### The response appears twice

**Symptom:** GapAnalyzer output (or the entire pipeline output) appears twice in the Agent Inspector response.

**Cause:** `WorkflowBuilder` uses OR-semantics for incoming edges - a downstream executor fires as soon as **any** predecessor completes. If `matching_executor` has two incoming edges (one from `resume_executor` and one from `jd_executor`), it fires twice: once when ResumeParser finishes and again when JD Agent finishes. GapAnalyzer then also runs twice.

**Fix:** Ensure the `WorkflowBuilder` graph is a strictly sequential pipeline with no fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

If you have a stray `.add_edge(resume_executor, matching_executor)` line, remove it. The `[PARSED RESUME PASS-THROUGH]` relay in JD Agent’s output already gives MatchingAgent access to the resume.

---

## Environment and configuration issues

### Missing or wrong `.env` values

The `.env` file must be in the `PersonalCareerCopilot/` directory (same level as `main.py`):

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

> Both paths use `FOUNDRY_PROJECT_ENDPOINT`. The value differs: cloud uses an `https://` Foundry endpoint; local uses `http://localhost:5273/v1`. Run `foundry model list` to confirm the exact model alias for Path B.

> **Finding your `FOUNDRY_PROJECT_ENDPOINT`:** 
- Open the **Foundry Toolkit** sidebar in VS Code → right-click your project → **Copy Project Endpoint**. 
- Or go to [Azure Portal](https://portal.azure.com) → your Foundry project → **Overview** → **Project endpoint**.

> **Finding your `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** In the Foundry Toolkit sidebar, expand your project → **Models** → find your deployed model name (e.g., `gpt-4.1-mini`).

### Env var precedence

`main.py` uses `load_dotenv(override=True)`, which means:

| Priority | Source | Wins when both are set? |
|----------|--------|------------------------|
| 1 (highest) | `.env` file | Yes |
| 2 | Shell / container environment variable | Used when the same key is not present in `.env` |

In local development, this makes `.env` the source of truth (editing `.env` immediately affects runs). In hosted deployment, Foundry injects environment variables at the container level; since `.env` is not part of the deployed image for this lab setup, the injected container values are used.

---

## Version compatibility

### Package version matrix

The multi-agent workflow requires specific package versions. Mismatched versions cause runtime errors.

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

## Deployment issues

### Container fails to start after deployment

1. **Check container logs:**
   - Open the **Foundry Toolkit** sidebar → expand **Hosted Agents (Preview)** → click your agent → expand the version → **Container Details** → **Logs**.
   - Look for Python stack traces or missing module errors.

2. **Common container startup failures:**

   | Error in logs | Cause | Fix |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` missing a package | Add the package, redeploy |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` or `.env` env vars not set | Update `agent.yaml` → `environment_variables` section (hosted) or `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity not configured | Foundry sets this automatically - ensure you're deploying via the extension |
   | `OSError: port 8088 already in use` | Dockerfile exposes wrong port or port conflict | Verify `EXPOSE 8088` in Dockerfile and `CMD ["python", "main.py"]` |
   | Container exits with code 1 | Unhandled exception in `main()` | Test locally first ([Module 5](05-test-locally.md)) to catch errors before deploying |

3. **Redeploy after fixing:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → select the same agent → deploy a new version.

### Deployment takes too long

Multi-agent containers take longer to start because they create 4 agent instances on startup. Normal startup times:

| Stage | Expected duration |
|-------|------------------|
| Container image build | 1-3 minutes |
| Image push to ACR | 30-60 seconds |
| Container start (single agent) | 15-30 seconds |
| Container start (multi-agent) | 30-120 seconds |
| Agent available in Playground | 1-2 minutes after "Started" |

> If "Pending" status persists beyond 5 minutes, check container logs for errors.

---

## RBAC and permission issues

### `403 Forbidden` or `AuthorizationFailed`

You need the **[Foundry User](https://aka.ms/foundry-ext-project-role)** role on your Foundry project (previously named **Azure AI User** - role ID unchanged):

1. Go to [Azure Portal](https://portal.azure.com) → your Foundry **project** resource.
2. Click **Access control (IAM)** → **Role assignments**.
3. Search for your name → confirm **Foundry User** (or the legacy label **Azure AI User**) is listed.
4. If missing: **Add** → **Add role assignment** → search for **Foundry User** → assign to your account.

See the [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) documentation for details.

### Model deployment not accessible

If the agent returns model-related errors:

1. Verify the model is deployed: Foundry sidebar → expand project → **Models** → check for `gpt-4.1-mini` (or your model) with status **Succeeded**.
2. Verify the deployment name matches: compare `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` (or `agent.yaml`) with the actual deployment name in the sidebar.
3. If the deployment expired (free tier): redeploy from [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local issues (Path B)

### Foundry Local service not running

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Symptom | Cause | Fix |
|---------|-------|-----|
| Health check returns `503` | Service not started | `foundry local start` or click **Start** in the Foundry Toolkit sidebar |
| Health check times out | Model still loading | Wait 30–60 s after starting; larger models take longer |
| `StatusCode: 404` on `/v1/health` | Wrong port | Default is `5273`. Check `foundry local status` for the actual port |
| Insufficient resources | Foundry Local needs ~4 GB RAM free | Close other applications |
| Model download fails | Low disk space | Models are 2–8 GB. Free up space, then `foundry model pull <name>` |

### Model name mismatch

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Set `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` to the exact alias shown (e.g., `phi-4-mini`, not `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` on local run (Path B)

The lab’s `main.py` uses `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local requires this variable to point to the local service - **not** `AZURE_AI_PROJECT_ENDPOINT`. Ensure your `.env` contains:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP tool still makes an outbound call (Path B)

This is expected. The `search_microsoft_learn_for_plan` tool fetches learning resources from `https://learn.microsoft.com/api/mcp`. **Only the skill-name query** travels over the network - resume and JD text are processed entirely on your device and never transmitted. If fully offline operation is required, add a `try/except` fallback in the tool that returns a static `learn.microsoft.com` URL when the endpoint is unreachable.

---

## Getting help

If you're stuck after trying the fixes above:

1. **Check the server logs** - Most errors produce a Python stack trace in the terminal. Read the full traceback.
2. **Search the error message** - Copy the error text and search in the [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Open an issue** - File an issue on the [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) with:
   - The error message or screenshot
   - Your package versions (`pip list | Select-String "agent-framework"`)
   - Your Python version (`python --version`)
   - Whether the issue is local or after deployment

---

### Checkpoint

- [ ] You know how to check and fix `.env` configuration issues
- [ ] You can verify package versions match the required matrix
- [ ] You know how to check container logs for deployment failures
- [ ] You can verify RBAC roles in the Azure Portal

---

**Previous:** [07 - Verify in Playground](07-verify-in-playground.md) · **Next:** [09 - Summary →](09-summary.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->