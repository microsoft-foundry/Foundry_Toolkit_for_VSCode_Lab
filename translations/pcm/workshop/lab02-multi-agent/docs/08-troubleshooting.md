# Module 8 - Troubleshooting (Multi-Agent)

Dis module cover common wahala, how to fix am, and debugging strategy wey concern multi-agent workflow. For general Foundry deployment palava dem, make you still check [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Quick reference: Error → Fix

| Error / Symptom | Likely Cause | Fix |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` file no dey or values never set | Create `.env` with `PROJECT_ENDPOINT=<your-endpoint>` and `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtual environment no activate or dependencies never install | Run `.\.venv\Scripts\Activate.ps1` then `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP package never install (no dey for requirements) | Run `pip install mcp` or check `requirements.txt` say e get am as transitive dependency |
| Agent start but e return empty response | `output_executors` no match or missing edges | Confirm `output_executors=[gap_analyzer]` and all edges dey for `create_workflow()` |
| Only 1 gap card (rest missing) | GapAnalyzer instructions no complete | Add the `CRITICAL:` paragraph for `GAP_ANALYZER_INSTRUCTIONS` - see [Module 3](03-configure-agents.md) |
| Fit score na 0 or e no dey | MatchingAgent no receive upstream data | Confirm both `add_edge(resume_parser, matching_agent)` and `add_edge(jd_agent, matching_agent)` dey |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server reject the tool call | Check internet connectivity. Try open `https://learn.microsoft.com/api/mcp` for browser. Retry |
| No Microsoft Learn URLs inside output | MCP tool never register or endpoint wrong | Confirm `tools=[search_microsoft_learn_for_plan]` for GapAnalyzer and `MICROSOFT_LEARN_MCP_ENDPOINT` correct |
| `Address already in use: port 8088` | Another process dey use port 8088 | Run `netstat -ano \| findstr :8088` (Windows) or `lsof -i :8088` (macOS/Linux) and kill the process wey dey clash |
| `Address already in use: port 5679` | Debugpy port dey conflict | Stop all other debug session. Run `netstat -ano \| findstr :5679` make you find and kill the process |
| Agent Inspector no go open | Server never start finish or port conflict dey | Wait "Server running" message. Confirm say port 5679 free |
| `azure.identity.CredentialUnavailableError` | You no sign into Azure CLI | Run `az login` then restart the server |
| `azure.core.exceptions.ResourceNotFoundError` | Model deployment no dey exist | Check say `MODEL_DEPLOYMENT_NAME` match deployed model for your Foundry project |
| Container status "Failed" after deployment | Container crash for startup | Check container logs inside Foundry sidebar. Common: env var no dey or import error |
| Deployment dey show "Pending" for > 5 minutes | Container dey take too long to start or resource limit | Wait up to 5 minutes for multi-agent (e create 4 agent instances). If e still dey pending, check logs |
| `ValueError` from `WorkflowBuilder` | Wrong graph configuration | Make sure say `start_executor` dey set, `output_executors` na list, and no circular edges |

---

## Environment and configuration issues

### Missing or wrong `.env` values

The `.env` file must dey for `PersonalCareerCopilot/` directory (same level as `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Expected `.env` content:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **How to find your PROJECT_ENDPOINT:**  
- Open **Microsoft Foundry** sidebar for VS Code → right-click your project → **Copy Project Endpoint**.  
- Or go [Azure Portal](https://portal.azure.com) → your Foundry project → **Overview** → **Project endpoint**.

> **How to find your MODEL_DEPLOYMENT_NAME:** For Foundry sidebar, open your project → **Models** → find the deployed model name (e.g., `gpt-4.1-mini`).

### Env var priority

`main.py` dey use `load_dotenv(override=False)`, dat mean:

| Priority | Source | E win if both set? |
|----------|--------|--------------------|
| 1 (highest) | Shell environment variable | Yes |
| 2 | `.env` file | Only if shell var no set |

Dis one mean Foundry runtime env vars (wey set by `agent.yaml`) dey priority pass `.env` values during hosted deployment.

---

## Version compatibility

### Package version matrix

Multi-agent workflow need specific package versions. If versions no match, e go cause runtime errors.

| Package | Required Version | Check Command |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | latest pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Common version errors

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: make am beta for rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` no dey or Inspector no compatible:**

```powershell
# Fix: install wit --pre flag
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' no get attribute 'streamable_http'`**

```powershell
# Fix: make mcp package beta pass
pip install mcp --upgrade
```

### Check all versions at once

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Expected output:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## MCP tool issues

### MCP tool no return results

**Symptom:** Gap cards talk "No results returned from Microsoft Learn MCP" or "No direct Microsoft Learn results found".

**Possible causes:**

1. **Network wahala** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) no dey reachable.
   ```powershell
   # Test di connection
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   If e return `200`, then the endpoint dey reachable.

2. **Query too specific** - The skill name too niche for Microsoft Learn search.
   - Dis one normal for very specialized skills. The tool get fallback URL inside the response.

3. **MCP session timeout** - The Streamable HTTP connection time don finish.
   - Retry the request. MCP sessions dey temporary and fit need reconnect.

### MCP logs meaning

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Meaning | Action |
|-----|---------|--------|
| `GET → 405` | MCP client dey probe during startup | Normal - ignore am |
| `POST → 200` | Tool call succeed | Expected |
| `DELETE → 405` | MCP client dey probe during cleanup | Normal - ignore am |
| `POST → 400` | Bad request (query no correct) | Check the `query` parameter inside `search_microsoft_learn_for_plan()` |
| `POST → 429` | Rate limit hit | Wait small and retry. Reduce `max_results` parameter |
| `POST → 500` | MCP server error | Temporary - retry. If e no stop, Microsoft Learn MCP API fit dey down |
| Connection timeout | Network problem or MCP server no dey | Check internet. Try `curl https://learn.microsoft.com/api/mcp` |

---

## Deployment issues

### Container no fit start after deployment

1. **Check container logs:**
   - Open **Microsoft Foundry** sidebar → expand **Hosted Agents (Preview)** → click your agent → expand version → **Container Details** → **Logs**.
   - Look for Python errors or missing module wahala.

2. **Common container startup failures:**

   | Error in logs | Cause | Fix |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` no get package | Add the package, redeploy |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` env vars no set | Update `agent.yaml` → `environment_variables` section |
   | `azure.identity.CredentialUnavailableError` | Managed Identity no set | Foundry dey set am automatically - make sure you dey deploy using extension |
   | `OSError: port 8088 already in use` | Dockerfile expose wrong port or port conflict | Confirm `EXPOSE 8088` for Dockerfile and `CMD ["python", "main.py"]` |
   | Container exit with code 1 | Unhandled exception for `main()` | Test for local first ([Module 5](05-test-locally.md)) make you catch errors before deploy |

3. **Redeploy after fix:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → choose the same agent → deploy new version.

### Deployment dey take long

Multi-agent container dey take more time to start because dem dey create 4 agent instances on startup. Normal startup time be:

| Stage | Expected duration |
|-------|------------------|
| Container image build | 1-3 minutes |
| Image push to ACR | 30-60 seconds |
| Container start (single agent) | 15-30 seconds |
| Container start (multi-agent) | 30-120 seconds |
| Agent ready for Playground | 1-2 minutes after "Started" |

> If "Pending" status still dey after 5 minutes, check container logs for wahala.

---

## RBAC and permission issues

### `403 Forbidden` or `AuthorizationFailed`

You need the **[Azure AI User](https://aka.ms/foundry-ext-project-role)** role for your Foundry project:

1. Go [Azure Portal](https://portal.azure.com) → your Foundry **project** resource.
2. Click **Access control (IAM)** → **Role assignments**.
3. Search your name → confirm say **Azure AI User** dey listed.
4. If e no dey: **Add** → **Add role assignment** → search **Azure AI User** → assign am to your account.

See [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) docs for detail.

### Model deployment no dey accessible

If the agent dey return model error:

1. Confirm model dey deployed: Foundry sidebar → expand project → **Models** → check for `gpt-4.1-mini` (or your model) with status **Succeeded**.
2. Confirm deployment name match: compare `MODEL_DEPLOYMENT_NAME` inside `.env` (or `agent.yaml`) with actual deployment name for sidebar.
3. If deployment done expire (free tier): redeploy from [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector issues

### Inspector open but e show "Disconnected"

1. Confirm server dey run: check for "Server running on http://localhost:8088" for terminal.
2. Check port `5679`: Inspector connect via debugpy for port 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Restart the server and open Inspector again.

### Inspector show partial response

Multi-agent responses long and e dey stream small small. Wait till full response finish (fit take 30-60 seconds depending on gap cards and MCP tool calls).

If response dey cut every time:
- Check GapAnalyzer instructions get `CRITICAL:` block wey no allow gap cards to combine.
- Check your model token limit - `gpt-4.1-mini` fit support up to 32K output tokens, e suppose enough.

---

## Performance tips

### Slow responses

Multi-agent workflow dey slow pass single-agent because dem get sequential dependencies and MCP tool calls.

| Optimization | How | Impact |
|-------------|-----|--------|
| Reduce MCP calls | Lower `max_results` parameter for tool | Less HTTP round-trips |
| Simplify instructions | Shorter, more focused agent prompts | Faster LLM inference |
| Use `gpt-4.1-mini` | Faster than `gpt-4.1` for development | About 2x speed improvement |
| Reduce gap card detail | Simplify gap card format inside GapAnalyzer instructions | Less output to generate |

### Typical response times (local)

| Configuration | Expected time |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap cards | 30-60 seconds |
| `gpt-4.1-mini`, 8+ gap cards | 60-120 seconds |
| `gpt-4.1`, 3-5 gap cards | 60-120 seconds |
---

## Getting help

If you dey stuck afta you don try di fixes wen I talk before:

1. **Check di server logs** - Most errors go get Python stack trace for di terminal. Read di full traceback.
2. **Search di error message** - Copy di error text come search am for [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Open an issue** - File issue for di [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) wit:
   - Di error message or screenshot
   - Your package versions (`pip list | Select-String "agent-framework"`)
   - Your Python version (`python --version`)
   - Whether di issue na local or e show after deployment

---

### Checkpoint

- [ ] You fit identify and fix di most common multi-agent errors using di quick reference table
- [ ] You sabi how to check and fix `.env` configuration issues
- [ ] You fit verify package versions wey match di required matrix
- [ ] You understand MCP log entries and fit diagnose tool failures
- [ ] You sabi how to check container logs for deployment failures
- [ ] You fit verify RBAC roles for Azure Portal

---

**Previous:** [07 - Verify in Playground](07-verify-in-playground.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Although we dey try make am correct, abeg sabi say automated translations fit get some errors or mistakes. Di original document for im own language na di correct source. For important information, make person wey sabi human translation do am. We no go take responsibility if any misunderstanding or wrong interpretation happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->