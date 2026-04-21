# Module 8 - Troubleshooting (Multi-Agent)

ਇਹ ਮੋਡਿਊਲ ਮਲਟੀ-ਏਜੰਟ ਵਰਕਫਲੋ ਲਈ ਆਮ ਗਲਤੀਆਂ, ਸੁਧਾਰ ਅਤੇ ਡੀਬੱਗਿੰਗ ਰਣਨੀਤੀਆਂ ਨੂੰ ਕਵਰ ਕਰਦਾ ਹੈ। ਆਮ ਫਾਊਂਡਰੀ ਡਿਪਲੌਇਮੈਂਟ ਮੁੱਦਿਆਂ ਲਈ, [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md) ਨੂੰ ਵੀ ਵੇਖੋ।

---

## Quick reference: Error → Fix

| Error / Symptom | Likely Cause | Fix |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` ਫ਼ਾਈਲ ਗੁੰਮ ਜਾਂ ਮੁੱਲ ਸੈੱਟ ਨਹੀਂ ਕੀਤੇ ਗਏ | `.env` ਬਣਾਓ ਜਿਸ ਵਿੱਚ `PROJECT_ENDPOINT=<your-endpoint>` ਅਤੇ `MODEL_DEPLOYMENT_NAME=<your-model>` ਹੋਵੇ |
| `ModuleNotFoundError: No module named 'agent_framework'` | ਵਰਚੁਅਲ ਇਨਵਾਇਰਨਮੈਂਟ ਸਰਗਰਮ ਨਹੀਂ ਹੈ ਜਾਂ ਡਿਪੈਂਡੈਂਸੀਜ਼ ਨਹੀਂ ਇੰਸਟਾਲ ਕੀਤੀਆਂ | ਚਲਾਓ `.\.venv\Scripts\Activate.ps1` ਫਿਰ `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP ਪੈਕੇਜ ਇੰਸਟਾਲ ਨਹੀਂ (requirements ਵਿੱਚ ਨਹੀਂ) | ਚਲਾਓ `pip install mcp` ਜਾਂ ਯਕੀਨੀ ਬਣਾਓ ਕਿ `requirements.txt` ਵਿੱਚ ਇਹ ਟ੍ਰਾਂਸਿਟਿਵ ਡਿਪੈਂਡੈਂਸੀ ਵਜੋਂ ਹੈ |
| ਏਜੰਟ ਸ਼ੁਰੂ ਹੁੰਦਾ ਹੈ ਪਰ ਖਾਲੀ ਜਵਾਬ ਦਿੰਦਾ ਹੈ | `output_executors` ਮਿਸਮੇਚ ਹੈ ਜਾਂ edges ਗੁੰਮ ਹਨ | `output_executors=[gap_analyzer]` ਅਤੇ ਸਾਰੇ edges `create_workflow()` ਵਿੱਚ ਮੌਜੂਦ ਹਨ ਜਾਂ ਨਹੀਂ ਸੱਚ ਕਰੋ |
| ਸਿਰਫ਼ 1 gap card (ਬਾਕੀ ਗੁੰਮ) | GapAnalyzer ਹਦਾਇਤਾਂ ਅਧੂਰੀਆਂ ਹਨ | `GAP_ANALYZER_INSTRUCTIONS` ਵਿੱਚ `CRITICAL:` ਪੈਰਾ ਜੋੜੋ - ਵੇਖੋ [Module 3](03-configure-agents.md) |
| Fit score 0 ਹੈ ਜਾਂ ਨਹੀਂ ਹੈ | MatchingAgent ਨੂੰ upstream ਡਾਟਾ ਮਿਲਿਆ ਨਹੀਂ | ਦੋਹਾਂ `add_edge(resume_parser, matching_agent)` ਅਤੇ `add_edge(jd_agent, matching_agent)` ਮੌਜੂਦ ਹਨ ਜਾਂ ਨਹੀਂ ਚੈੱਕ ਕਰੋ |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP ਸਰਵਰ ਨੇ ਟੂਲ ਕਾਲ ਰੱਦ ਕਰ ਦਿੱਤੀ | ਇੰਟਰਨੈੱਟ ਕਨੈਕਟੀਵੀਟੀ ਚੈਕ ਕਰੋ। ਬ੍ਰਾਉਜ਼ਰ ਵਿੱਚ `https://learn.microsoft.com/api/mcp` ਖੋਲ੍ਹ ਕੇ ਕੋਸ਼ਿਸ਼ ਕਰੋ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ |
| ਆਉਟਪੁੱਟ ਵਿੱਚ ਕੋਈ Microsoft Learn URL ਨਹੀਂ | MCP ਟੂਲ ਰਜਿਸਟਰਡ ਨਹੀਂ ਜਾਂ endpoint ਗਲਤ ਹੈ | GapAnalyzer ਤੇ `tools=[search_microsoft_learn_for_plan]` ਹੈ ਅਤੇ `MICROSOFT_LEARN_MCP_ENDPOINT` ਸਹੀ ਹੈ ਯਕੀਨੀ ਬਣਾਓ |
| `Address already in use: port 8088` | ਹੋਰ ਪ੍ਰਕਿਰਿਆ 8088 ਪੋਰਟ ਨੂੰ ਵਰਤ ਰਹੀ ਹੈ | ਚਲਾਓ `netstat -ano \| findstr :8088` (Windows) ਜਾਂ `lsof -i :8088` (macOS/Linux) ਅਤੇ ਟਕਰਾਅ ਕਰਨ ਵਾਲੀ ਪ੍ਰਕਿਰਿਆ ਰੋਕੋ |
| `Address already in use: port 5679` | Debugpy ਪੋਰਟ ਟਕਰਾਅ | ਹੋਰ ਡੀਬੱਗ ਸੈਸ਼ਨ ਰੋਕੋ। `netstat -ano \| findstr :5679` ਚਲਾਕੇ ਪ੍ਰਕਿਰਿਆ ਨੂੰ ਖਤਮ ਕਰੋ |
| Agent Inspector ਖੁਲਦਾ ਨਹੀਂ | ਸਰਵਰ ਪੂਰੀ ਤਰ੍ਹਾਂ ਸ਼ੁਰੂ ਨਹੀਂ ਹਾਂ ਜਾਂ ਪੋਰਟ ਟਕਰਾਅ | "Server running" ਲਾਗ ਦੀ ਉਡੀਕ ਕਰੋ। ਪੋਰਟ 5679 ਮੁਫ਼ਤ ਹੈ ਜਾਂ ਨਹੀਂ ਚੈੱਕ ਕਰੋ |
| `azure.identity.CredentialUnavailableError` | Azure CLI ਵਿੱਚ ਸਾਈਨ ਇਨ ਨਹੀਂ | `az login` ਚਲਾਓ ਫਿਰ ਸਰਵਰ ਰੀਸਟਾਰਟ ਕਰੋ |
| `azure.core.exceptions.ResourceNotFoundError` | ਮਾਡਲ ਡਿਪਲੌਇਮੈਂਟ ਮੌਜੂਦ ਨਹੀਂ | ਯਕੀਨੀ ਬਣਾਓ ਕਿ `MODEL_DEPLOYMENT_NAME` ਤੁਹਾਡੇ Foundry ਪ੍ਰੋਜੈਕਟ ਵਿੱਚ ਡਿਪਲੌਇਡ ਮਾਡਲ ਨਾਲ ਮੇਲ ਖਾਂਦਾ ਹੈ |
| ਡਿਪਲੌਇਮੈਂਟ ਮਗਰੋਂ ਕੰਟੇਨਰ ਦੀ ਸਥਿਤੀ "Failed" | ਸਟਾਰਟਅਪ 'ਤੇ ਕੰਟੇਨਰ ਕਰੈਸ਼ | Foundry ਸਾਈਡਬਾਰ ਵਿੱਚ ਕੰਟੇਨਰ ਲਾਗਜ਼ ਚੈੱਕ ਕਰੋ। ਆਮ ਤੌਰ 'ਤੇ: ਗੁੰਮ env var ਜਾਂ ਇਮਪੋਰਟ ਐਰਰ |
| ਡਿਪਲੌਇਮੈਂਟ 5 ਮਿੰਟ ਤੋਂ ਵੱਧ "Pending" ਦਿਖਾਂਦਾ ਹੈ | ਕੰਟੇਨਰ ਸ਼ੁਰੂ ਹੋਣ ਵਿੱਚ ਜ਼ਿਆਦਾ ਸਮਾਂ ਲੱਗ ਰਿਹਾ ਹੈ ਜਾਂ ਰਿਸੋਰਸ ਸੀਮਾਵਾਂ | ਮਲਟੀ-ਏਜੰਟ ਲਈ (4 ਏਜੰਟ ਇੰਸਟੈਂਸ ਬਣਾਉਂਦਾ ਹੈ) 5 ਮਿੰਟ ਤੱਕ ਉਡੀਕ ਕਰੋ। ਜੇ ਫਿਰ ਵੀ ਪੇਂਡਿੰਗ, ਤਬ ਲਾਗਜ਼ ਦੇਖੋ |
| `ValueError` from `WorkflowBuilder` | ਗਲਤ ਗ੍ਰਾਫ ਸੰਰਚਨਾ | ਯਕੀਨ ਕਰੋ ਕਿ `start_executor` ਸੈੱਟ ਹੈ, `output_executors` ਸੂਚੀ ਹੈ, ਅਤੇ ਕੋਈ ਵਰਤੀ ਗਈ ਲੂਪੇਡਜ ਨਹੀਂ ਹੈ |

---

## Environment and configuration issues

### ਗੁੰਮ ਜਾਂ ਗਲਤ `.env` ਮੁੱਲ

`.env` ਫ਼ਾਈਲ ਨੂੰ `PersonalCareerCopilot/` ਡਾਇਰੈਕਟਰੀ ਵਿੱਚ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ (ਜਿੱਥੇ ਹੀ `main.py` ਹੈ):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

ਉਮੀਦਜਦ `.env` ਵਰਤੋਂ:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **ਆਪਣਾ PROJECT_ENDPOINT ਲੱਭਣਾ:**  
- VS Code ਵਿੱਚ **Microsoft Foundry** ਸਾਈਡਬਾਰ ਖੋਲ੍ਹੋ → ਆਪਣਾ ਪ੍ਰੋਜੈਕਟ ਤੇ ਦਹਿਨ-ਕਲਿੱਕ ਕਰੋ → **Copy Project Endpoint**।  
- ਜਾਂ [Azure Portal](https://portal.azure.com) ਤੇ ਜਾਓ → ਆਪਣੇ Foundry ਪ੍ਰੋਜੈਕਟ → **Overview** → **Project endpoint**।

> **ਆਪਣਾ MODEL_DEPLOYMENT_NAME ਲੱਭਣਾ:** Foundry ਸਾਈਡਬਾਰ ਵਿੱਚ ਆਪਣਾ ਪ੍ਰੋਜੈਕਟ ਖੋਲ੍ਹੋ → **Models** → ਆਪਣਾ ਡਿਪਲੌਇਡ ਮਾਡਲ ਨਾਂ (ਜਿਵੇਂ `gpt-4.1-mini`) ਲੱਭੋ।

### Env var precedence

`main.py` `load_dotenv(override=False)` ਵਰਤਦਾ ਹੈ, ਜਿਸਦਾ ਮਤਲਬ ਹੈ:

| ਪ੍ਰਾਥਮਿਕਤਾ | ਸਰੋਤ | ਦੋਹਾਂ ਸੈੱਟ ਹੋਣ 'ਤੇ ਕਿਹੜਾ ਜਿੱਤਦਾ ਹੈ? |
|----------|--------|------------------------|
| 1 (ਸਭ ਤੋਂ ਉੱਚਾ) | Shell ਇਨਵਾਇਰਨਮੈਂਟ ਵੈਰੀਏਬਲ | ਹਾਂ |
| 2 | `.env` ਫ਼ਾਈਲ | ਸਿਰਫ ਜੇ shell var ਸੈੱਟ ਨਹੀਂ ਹੈ |

ਇਸਦਾ ਮਤਲਬ Foundry ਰਨਟਾਈਮ env vars (`agent.yaml` ਤੋਂ ਸੈੱਟ ਕੀਤੇ) ਹੋਸਟ ਡਿਪਲੌਇਮੈਂਟ ਵਿਚ `.env` ਮੁੱਲਾਂ ਨਾਲੋਂ ਉੱਚ ਪ੍ਰਾਥਮਿਕਤਾ ਰੱਖਦੇ ਹਨ।

---

## Version compatibility

### ਪੈਕੇਜ ਵਰਜਨ ਮੈਟ੍ਰਿਕਸ

ਮਲਟੀ-ਏਜੰਟ ਵਰਕਫਲੋ ਨੂੰ ਖਾਸ ਪੈਕੇਜ ਵਰਜਨਾਂ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ। ਗਲਤ ਮੈਚ ਵਰਜਨਾਂ ਨਾਲ ਰਨਟਾਈਮ ਤ੍ਰੁਟੀਆਂ ਆਉਂਦੀਆਂ ਹਨ।

| ਪੈਕੇਜ | ਲੋੜੀਂਦਾ ਵਰਜਨ | ਚੈੱਕ ਕਰਨ ਦਾ ਕਮਾਂਡ |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | ਤਾਜ਼ਾ ਪ੍ਰੀ-ਰਿਲੀਜ਼ | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### ਆਮ ਵਰਜਨ ਗਲਤੀਆਂ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ਠੀਕ ਕਰੋ: ਆਰਸੀ3 ਵਿੱਚ ਅੱਪਗਰੇਡ ਕਰੋ
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` ਨਹੀਂ ਮਿਲੀ ਜਾਂ Inspector ਅਣਕੰਪੈਟਿਬਲ:**

```powershell
# ਠੀਕ ਕਰੋ: --pre ਫਲੈਗ ਨਾਲ ਇੰਸਟਾਲ ਕਰੋ
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ਸੁਧਾਰ: mcp ਪੈਕੇਜ ਨੂੰ ਅਪਗ੍ਰੇਡ ਕਰੋ
pip install mcp --upgrade
```

### ਇੱਕ ਵਾਰੀ ਵਿੱਚ ਸਾਰੇ ਵਰਜਨ ਚੈੱਕ ਕਰੋ

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

ਉਮੀਦਜਦ ਆਉਟਪੁਟ:

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

### MCP ਟੂਲ ਕੋਈ ਨਤੀਜੇ ਵਾਪਸ ਨਹੀਂ ਦਿੰਦਾ

**ਲੱਛਣ:** Gap cards ਕਹਿੰਦੇ ਹਨ "No results returned from Microsoft Learn MCP" ਜਾਂ "No direct Microsoft Learn results found"।

**ਸੰਭਾਵਿਤ ਕਾਰਨ:**

1. **ਨੈਟਵਰਕ ਮੁੱਦਾ** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) ਪਹੁੰਚ ਤੋਂ ਬਾਹਰ ਹੈ।
   ```powershell
   # ਕਨੈਕਟਿਵਿਟੀ ਦੀ ਜਾਂਚ ਕਰੋ
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   ਜੇ ਇਹ `200` ਵਾਪਸ ਕਰਦਾ ਹੈ ਤਾਂ endpoint ਉਪਲਬਧ ਹੈ।

2. **ਬਹੁਤ ਵਿਸ਼ੇਸ਼ਤ ਪੁੱਛਗਿੱਛ** - Microsoft Learn ਸਰਚ ਲਈ ਸਖ਼ਤ ਸਕਿਲ ਨਾਂ ਹੈ।  
   - ਇਹ ਬਹੁਤ ਖਾਸ ਸਕਿਲ ਲਈ ਆਮ ਹੈ। ਟੂਲ ਵਿੱਚ ਇਸਦਾ fallback URL ਹੁੰਦਾ ਹੈ।

3. **MCP ਸੈਸ਼ਨ ਸਮਾਪਤੀ** - Streamable HTTP ਕਨੈਕਸ਼ਨ ਟਾਈਮਆਉਟ ਹੋ ਗਿਆ।  
   - ਮੰਗ ਦੁਹਰਾਓ। MCP ਸੈਸ਼ਨ ਛਣਣ ਹਨ ਅਤੇ ਮੁੜ ਜੁੜਨ ਦੀ ਲੋੜ ਹੋ ਸਕਦੀ ਹੈ।

### MCP ਲਾਗਜ਼ ਦੀ ਵਿਆਖਿਆ

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| ਲਾਗ | ਮਤਲਬ | ਕਾਰਵਾਈ |
|-----|---------|--------|
| `GET → 405` | MCP ਕਲਾਇੰਟ ਸ਼ੁਰੂਆਤੀ ਜਾਂਚਾਂ ਕਰ ਰਿਹਾ ਹੈ | ਆਮ - ਨਜ਼ਰਅੰਦਾਜ਼ ਕਰੋ |
| `POST → 200` | ਟੂਲ ਕਾਲ ਸਫਲ | ਉਮੀਦਜਦ |
| `DELETE → 405` | MCP ਕਲਾਇੰਟ ਸਾਫ਼-ਸਫਾਈ ਦੌਰਾਨ ਜਾਂਚਾਂ ਕਰ ਰਿਹਾ ਹੈ | ਆਮ - ਨਜ਼ਰਅੰਦਾਜ਼ ਕਰੋ |
| `POST → 400` | ਬੁਰਾ ਬੇਨਤੀ (ਖ਼ਰਾਬ ਪੁੱਛਗਿੱਛ) | `search_microsoft_learn_for_plan()` ਵਿੱਚ `query` ਪੈਰਾਮੀਟਰ ਚੈੱਕ ਕਰੋ |
| `POST → 429` | ਰੇਟ ਸੀਮਿਤ | ਉਡੀਕ ਕਰੋ ਅਤੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ। `max_results` ਪੈਰਾਮੀਟਰ ਘਟਾਓ |
| `POST → 500` | MCP ਸਰਵਰ ਗਲਤੀ | ਅਸਥਾਈ - ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ। ਜੇ ਲੰਬੇ ਸਮੇਂ ਲਈ ਹੈ ਤਾਂ Microsoft Learn MCP API ਬੰਦ ਹੋ ਸਕਦੀ ਹੈ |
| ਕਨੈਕਸ਼ਨ ਸਮਾਂ ਸਮਾਪਤ | ਨੈੱਟਵਰਕ ਮੁੱਦਾ ਜਾਂ MCP ਸਰਵਰ ਨੂੰ ਪਹੁੰਚ ਨਹੀਂ | ਇੰਟਰਨੈੱਟ ਚੈੱਕ ਕਰੋ। `curl https://learn.microsoft.com/api/mcp` ਕੋਸ਼ਿਸ਼ ਕਰੋ |

---

## Deployment issues

### ਡਿਪਲੌਇਮੈਂਟ ਮਗਰੋਂ ਕੰਟੇਨਰ ਸ਼ੁਰੂ ਹੋਣਾ ਨਾਕਾਮ

1. **ਕੰਟੇਨਰ ਲਾਗਜ਼ ਦੀ ਜਾਂਚ ਕਰੋ:**  
   - **Microsoft Foundry** ਸਾਈਡਬਾਰ ਖੋਲ੍ਹੋ → **Hosted Agents (Preview)** ਖੋਲ੍ਹੋ → ਆਪਣਾ ਏਜੰਟ ਕਲਿੱਕ ਕਰੋ → ਵਰਜਨ ਵਧਾਓ → **Container Details** → **Logs**।  
   - Python ਸਟੈਕ ਟਰੇਸ ਜਾਂ ਮੌਡੀਊਲ ਗੁੰਮ ਹੋਣ ਵਾਲੀਆਂ ਗਲਤੀਆਂ ਵੇਖੋ।

2. **ਆਮ ਕੰਟੇਨਰ ਸ਼ੁਰੂਆਤ ਦੀਆਂ ਅਸਫਲਤਾਵਾਂ:**

   | ਲਾਗ ਵਿੱਚ ਗਲਤੀ | ਕਾਰਨ | ਸੁਧਾਰ |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` ਵਿੱਚ ਪੈਕੇਜ ਨਹੀਂ | ਪੈਕੇਜ ਜੋੜੋ, ਮੁੜ ਡਿਪਲੌਇ ਕਰੋ |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` env vars ਨਹੀਂ | `agent.yaml` ਦਾ `environment_variables` ਹਿੱਸਾ ਅਪਡੇਟ ਕਰੋ |
   | `azure.identity.CredentialUnavailableError` | ਮੈਨੇਜਡ ਆਈਡੈਂਟਿਟੀ ਕੁਨਫ਼ਿਗਰ ਨਹੀਂ | Foundry ਆਟੋਮੈਟਿਕ ਸੈੱਟ ਕਰਦਾ ਹੈ - ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਤੁਸੀਂ ਐਕਸਟेंਸ਼ਨ ਰਾਹੀਂ ਡਿਪਲੌਇ ਕਰ ਰਹੇ ਹੋ |
   | `OSError: port 8088 already in use` | Dockerfile ਗਲਤ ਪੋਰਟ ਖੋਲ੍ਹਦਾ ਹੈ ਜਾਂ ਪੋਰਟ ਟਕਰਾਅ | Dockerfile ਵਿੱਚ `EXPOSE 8088` ਅਤੇ `CMD ["python", "main.py"]` ਸਹੀ ਹਨ ਜਾਂ ਨਹੀਂ ਵਾੈਰੀਫਾਈ ਕਰੋ |
   | Container 1 ਕੋਡ ਨਾਲ ਬੰਦ ਹੋ ਜਾਂਦਾ ਹੈ | `main()` 'ਚ ਅਨਹੈਂਡਲਡ ਇਕਸੀਪਸ਼ਨ | ਪਹਿਲਾਂ ਲੋਕਲ ([Module 5](05-test-locally.md)) 'ਤੇ ਟੈਸਟ ਕਰੋ ਤਾਂ ਜੋ ਡਿਪਲੌਇ ਤੋਂ ਪਹਿਲਾਂ ਤ੍ਰੁਟੀਆਂ ਪਕੜੀ ਜਾ ਸਕਣ |

3. **ਸੁਧਾਰ ਕਰਨ ਤੋਂ ਬਾਅਦ ਮੁੜ ਡਿਪਲੌਇ ਕਰੋ:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → ਉਹੀ ਏਜੰਟ ਚੁਣੋ → ਨਵਾਂ ਵਰਜਨ ਡਿਪਲੌਇ ਕਰੋ।

### ਡਿਪਲੌਇਮੈਂਟ ਵਿੱਚ ਜ਼ਿਆਦਾ ਸਮਾਂ ਲੱਗਣਾ

ਮਲਟੀ-ਏਜੰਟ ਕੰਟੇਨਰ ਸ਼ੁਰੂ ਹੋਣ ਵਿੱਚ ਜ਼ਿਆਦਾ ਸਮਾਂ ਲੈਂਦੇ ਹਨ ਕਿਉਂਕਿ ਇਹ ਚਾਰ ਏਜੰਟ ਇੰਸਟੈਂਸ ਬਣਾਉਂਦੇ ਹਨ। ਆਮ ਸਟਾਰਟਅਪ ਸਮਾਂ:

| ਦਰਜਾ | ਉਮੀਦੀ ਸਮਾਂ |
|-------|------------|
| ਕੰਟੇਨਰ ਇਮੇਜ਼ ਬਿਲਡ | 1-3 ਮਿੰਟ |
| ਇਮੇਜ਼ ਨੂੰ ACR 'ਤੇ ਪੁਸ਼ | 30-60 ਸੈਕੰਡ |
| ਕੰਟੇਨਰ ਸਿੰਗਲ ਏਜੰਟ ਸਟਾਰਟ | 15-30 ਸੈਕੰਡ |
| ਕੰਟੇਨਰ ਮਲਟੀ-ਏਜੰਟ ਸਟਾਰਟ | 30-120 ਸੈਕੰਡ |
| ਏਜੰਟ Playground ਵਿੱਚ ਉਪਲਬਧ | "Started" ਤੋਂ ਬਾਅਦ 1-2 ਮਿੰਟ |

> ਜੇ "Pending" ਸਥਿਤੀ 5 ਮਿੰਟ ਤੋਂ ਵੱਧ ਰਹਿੰਦੀ ਹੈ, ਕੰਟੇਨਰ ਲਾਗਜ਼ ਵਿੱਚ ਗਲਤੀਆਂ ਚੈੱਕ ਕਰੋ।

---

## RBAC and permission issues

### `403 Forbidden` ਜਾਂ `AuthorizationFailed`

ਤੁਹਾਨੂੰ ਆਪਣੇ Foundry ਪ੍ਰੋਜੈਕਟ ਉੱਤੇ **[Azure AI User](https://aka.ms/foundry-ext-project-role)** ਰੋਲ ਦੀ ਲੋੜ ਹੈ:

1. [Azure Portal](https://portal.azure.com) ਖੋਲ੍ਹੋ → ਆਪਣੇ Foundry **ਪ੍ਰੋਜੈਕਟ** ਸਰੋਤ।
2. **Access control (IAM)** → **Role assignments** ਤੇ ਕਲਿੱਕ ਕਰੋ।
3. ਆਪਣਾ ਨਾਮ ਖੋਜੋ → ਪੱਕਾ ਕਰੋ **Azure AI User** ਸੂਚੀ ਵਿੱਚ ਹੈ।
4. ਜੇ ਗੁੰਮ: **Add** → **Add role assignment** → **Azure AI User** ਖੋਜੋ → ਆਪਣੇ ਖਾਤੇ ਲਈ ਸਮਰਪਿਤ ਕਰੋ।

ਵਿਸਥਾਰ ਲਈ [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ਦਸਤਾਵੇਜ਼ ਵੇਖੋ।

### ਮਾਡਲ ਡਿਪਲੌਇਮੈਂਟ ਨਹੀਂ ਮਿਲਦਾ

ਜੇ ਏਜੰਟ ਮਾਡਲ ਸੰਬੰਧੀ ਗਲਤੀਆਂ ਵਾਪਸ ਕਰਦਾ ਹੈ:

1. ਮਾਡਲ ਡਿਪਲੌਇਡ ਹੈ ਜਾਂ ਨਹੀਂ ਵੇਰਵੇ: Foundry ਸਾਈਡਬਾਰ → ਪ੍ਰੋਜੈਕਟ ਖੋਲ੍ਹੋ → **Models** → `gpt-4.1-mini` (ਜਾਂ ਤੁਹਾਡਾ ਮਾਡਲ) ਦੀ ਵੱਧੀ ਸਥਿਤੀ **Succeeded** ਹੋਵੇ।
2. ਡਿਪਲੌਇਮੈਂਟ ਨਾਂ ਮੇਲ ਖਾਂਦਾ ਹੈ ਜਾਂ ਨਹੀਂ: `.env` (ਜਾਂ `agent.yaml`) ਵਿੱਚ `MODEL_DEPLOYMENT_NAME` ਨਾਲ ਸਾਈਡਬਾਰ ਵਿੱਚ ਅਸਲੀ ਡਿਪਲੌਇਮੈਂਟ ਨਾਂ ਤੁਲਨਾ ਕਰੋ।
3. ਜੇ ਡਿਪਲੌਇਮੈਂਟ ਖਤਮ ਹੋ ਗਿਆ (ਫ੍ਰੀ ਟੀਅਰ): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) ਤੋਂ ਮੁੜ ਡਿਪਲੌਇ ਕਰੋ (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)।

---

## Agent Inspector issues

### Inspector ਖੁਲਦਾ ਹੈ ਪਰ "Disconnected" ਦਿਖਾਉਂਦਾ ਹੈ

1. ਸਰਵਰ ਚੱਲ ਰਿਹਾ ਹੈ ਜਾਂ ਨਹੀਂ ਵੇਖੋ: ਟਰਮੀਨਲ ਵਿੱਚ "Server running on http://localhost:8088" ਦੇਖੋ।
2. ਪੋਰਟ `5679` ਚੈੱਕ ਕਰੋ: Inspector ਡੀਬੱਗਪੀ ਨਾਲ ਪੋਰਟ 5679 ਉੱਤੇ ਜੁੜਦਾ ਹੈ।
   ```powershell
   netstat -ano | findstr :5679
   ```
3. ਸਰਵਰ ਮੁੜ ਚਾਲੂ ਕਰੋ ਅਤੇ Inspector ਮੁੜ ਖੋਲ੍ਹੋ।

### Inspector ਆংশਿਕ ਜਵਾਬ ਦਿਖਾਂਦਾ ਹੈ

ਮਲਟੀ-ਏਜੰਟ ਜਵਾਬ ਲੰਬੇ ਹੁੰਦੇ ਹਨ ਅਤੇ ਸਟ੍ਰੀਮ ਰੂਪ ਵਿੱਚ ਹੁੰਦੇ ਹਨ। ਪੂਰਾ ਜਵਾਬ ਮੁਕੰਮਲ ਹੋਣ ਲਈ ਉਡੀਕ ਕਰੋ (30-60 ਸਕਿੰਟ ਜਾਂ ਵੱਧ ਵੀ ਲੱਗ ਸਕਦਾ ਹੈ, GAP ਕਾਰਡਾਂ ਅਤੇ MCP ਟੂਲ ਕਾਲਾਂ ਦੀ ਗਿਣਤੀ ਤੇ ఆధਾਰਿਤ)।

ਜੇ ਜਵਾਬ ਲਗਾਤਾਰ ਕੱਟਿਆ ਜਾਂਦਾ ਹੈ:  
- ਯਕੀਨੀ ਬਣਾਓ ਕਿ GapAnalyzer ਹਦਾਇਤਾਂ ਵਿੱਚ `CRITICAL:` ਬਲਾਕ ਹੈ ਜੋ gap cards ਨੂੰ ਇकट्ठਾ ਹੋਣ ਤੋਂ ਰੋਕਦਾ ਹੈ।  
- ਆਪਣੀ ਮਾਡਲ ਦੀ ਟੋਕਨ ਸੀਮਾ ਚੈੱਕ ਕਰੋ - `gpt-4.1-mini` 32K ਟੋਕਨਆਉਟਪੁੱਟ ਤੱਕ ਸਮਰਥਨ ਕਰਦਾ ਹੈ, ਜਿਹੜਾ ਕਾਫ਼ੀ ਹੈ।

---

## Performance tips

### ਹੌਲੀ ਜਵਾਬੀ

ਮਲਟੀ-ਏਜੰਟ ਵਰਕਫਲੋ ਇੱਕਲਿਆ ਏਜੰਟ ਨਾਲੋਂ ਆਮ ਤੌਰ 'ਤੇ ਹੌਲੇ ਹੁੰਦੇ ਹਨ ਕਿਉਂਕਿ ਇਹ ਲੜੀਵਾਰ ਨਿਰਭਰਤਾਵਾਂ ਅਤੇ MCP ਟੂਲ ਕਾਲਾਂ ਕਰਦਾ ਹੈ।

| ਸੁਧਾਰ | ਕਿਵੇਂ | ਪ੍ਰਭਾਵ |
|-------------|-----|--------|
| MCP ਕਾਲਾਂ ਘਟਾਓ | ਟੂਲ ਵਿੱਚ `max_results` ਪੈਰਾਮੀਟਰ ਘਟਾਓ | ਘੱਟ HTTP ਰਾਊਂਡ-ਟ੍ਰਿਪਸ |
| ਹਦਾਇਤਾਂ ਸਧਾਰਨ ਕਰੋ | ਛੋਟੇ, ਫੋਕਸ ਵਾਲੇ ਏਜੰਟ ਪ੍ਰੰਪਟ | ਤੇਜ਼ LLM ਇੰਫ਼ਰੈਂਸ |
| `gpt-4.1-mini` ਵਰਤੋਂ | ਸਿੰਗਲ `gpt-4.1` ਨਾਲੋਂ ਤੇਜ਼ | ਲਗਭਗ 2 ਗੁਣਾ ਤੇਜ਼ |
| gap ਕਾਰਡ ਵੇਰਵਾ ਘੱਟ ਕਰੋ | GapAnalyzer ਹਦਾਇਤਾਂ ਵਿੱਚ gap ਕਾਰਡ ਫਾਰਮੈਟ ਸਧਾਰਨ ਕਰੋ | ਘੱਟ ਆਉਟਪੁੱਟ ਤਿਆਰ ਕਰਨੀ |

### ਆਮ ਜਵਾਬ ਸਮੇਂ (ਲੋਕਲ)

| ਸੰਰਚਨਾ | ਉਮੀਦਜਦ ਸਮਾਂ |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap ਕਾਰਡ | 30-60 ਸਕਿੰਟ |
| `gpt-4.1-mini`, 8+ gap ਕਾਰਡ | 60-120 ਸਕਿੰਟ |
| `gpt-4.1`, 3-5 gap ਕਾਰਡ | 60-120 ਸਕਿੰਟ |
---

## ਸਹਾਇਤਾ ਪ੍ਰਾਪਤ ਕਰਨਾ

ਜੇ ਤੁਸੀਂ ਉਪਰ ਦਿੱਤੀਆਂ ਸੁਧਾਰਾਂ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰਨ ਤੋਂ ਬਾਅਦ ਫਸੇ ਹੋ:

1. **ਸਰਵਰ ਲਾਗਜ਼ ਦੀ ਜਾਂਚ ਕਰੋ** - ਜ਼ਿਆਦਾਤਰ ਗਲਤੀਆਂ ਟਰਮੀਨਲ ਵਿੱਚ ਪਾਇਥਨ ਸਟੈਕ ਟ੍ਰੇਸ ਪੈਦਾ ਕਰਦੀਆਂ ਹਨ। ਪੂਰਾ ਟ੍ਰੇਸਬੈਕ ਪੜ੍ਹੋ।
2. **ਗਲਤੀ ਸੁਨੇਹਾ ਖੋਜੋ** - ਗਲਤੀ ਦੇ ਟੈਕਸਟ ਨੂੰ ਕਾਪੀ ਕਰੋ ਅਤੇ [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) ਵਿੱਚ ਖੋਜੋ।
3. **ਇੱਕ ਮਾਮਲਾ ਖੋਲ੍ਹੋ** - [ਵਰਕਸ਼ਾਪ ਰਿਪੋਜ਼ੀਟਰੀ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 'ਤੇ ਇੱਕ ਮਾਮਲਾ ਦਰਜ ਕਰੋ ਜਿਸ ਵਿੱਚ ਸ਼ਾਮਲ ਹੋਵੇ:
   - ਗਲਤੀ ਸੁਨੇਹਾ ਜਾਂ ਸਕ੍ਰੀਨਸ਼ਾਟ
   - ਤੁਹਾਡੇ ਪੈਕੇਜ ਸੰਸਕਰਨ (`pip list | Select-String "agent-framework"`)
   - ਤੁਹਾਡਾ ਪਾਇਥਨ ਸੰਸਕਰਨ (`python --version`)
   - ਮਾਮਲਾ ਸਥਾਨਕ ਹੈ ਜਾਂ ਡਿਪਲੋਇਮੈਂਟ ਤੋਂ ਬਾਅਦ

---

### ਚੈਕਪੋਇੰਟ

- [ ] ਤੁਸੀਂ ਸਭ ਤੋਂ ਆਮ ਮਲਟੀ-ਏਜੰਟ ਗਲਤੀਆਂ ਨੂੰ ਜਾਂਚਕੇ ਸੁਧਾਰ ਸਕਦੇ ਹੋ ਤੇਜ਼ ਰੈਫਰੇੰਸ ਟੇਬਲ ਦੀ ਵਰਤੋਂ ਕਰਕੇ
- [ ] ਤੁਸੀਂ `.env` ਸੰਰਚਨਾ ਸਮੱਸਿਆਵਾਂ ਦੀ ਜਾਂਚ ਅਤੇ ਸੁਧਾਰ ਕਰਨਾ ਜਾਣਦੇ ਹੋ
- [ ] ਤੁਸੀਂ ਪੈਕੇਜ ਸੰਸਕਰਨ ਦੀ ਜਾਂਚ ਕਰਕੇ ਵੇਰਵਾ ਮੈਟ੍ਰਿਕਸ ਨਾਲ ਮੇਲ ਖਾਂਦੇ ਹੋ ਇਹ ਯਕੀਨੀ ਬਣਾ ਸਕਦੇ ਹੋ
- [ ] ਤੁਸੀਂ MCP ਲਾਗ ਐਨਟਰੀਜ਼ ਨੂੰ ਸਮਝਦੇ ਹੋ ਅਤੇ ਟੂਲ ਫੇਲਿਯਰਾਂ ਦੀ ਤਸ਼ਖੀਸ ਕਰ ਸਕਦੇ ਹੋ
- [ ] ਤੁਸੀਂ ਡਿਪਲੋਇਮੈਂਟ ਫੇਲਿਯਰਾਂ ਲਈ ਕੰਟੇਨਰ ਲਾਗਜ਼ ਦੀ ਜਾਂਚ ਕਰਨਾ ਜਾਣਦੇ ਹੋ
- [ ] ਤੁਸੀਂ ਐਜ਼ਯੂਰ ਪੋਰਟਲ ਵਿੱਚ RBAC ਰੋਲਾਂ ਦੀ ਜਾਂਚ ਕਰ ਸਕਦੇ ਹੋ

---

**ਪਿਛਲਾ:** [07 - ਪਲੇਗ੍ਰਾਊੰਡ ਵਿੱਚ ਸਵੀਕਾਰੋ](07-verify-in-playground.md) · **ਘਰ:** [ਲੈਬ 02 README](../README.md) · [ਵਰਕਸ਼ਾਪ ਘਰ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰਤਾ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦਿਤ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸ਼ੁੱਧਤਾ ਲਈ ਯਤਨ ਕਰਦੇ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਵਿੱਚ ਰੱਖੋ ਕਿ ਆਟੋਮੈਟਿਕ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਥਿਰਤਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਉਸ ਦੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਹੀ ਪ੍ਰਮਾਣਿਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਅਹਿਮ ਜਾਣਕਾਰੀ ਲਈ ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਹੋਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆਵਾਂ ਲਈ ਅਸੀਂ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->