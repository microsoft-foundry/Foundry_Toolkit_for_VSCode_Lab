# ਮੋਡੀਊਲ 8 - ਸਮੱਸਿਆ ਹਲ ਕਰਨਾ

ਇਹ ਮੋਡੀਊਲ ਬਹੁ-ਏਜੰਟ ਵਰਕਫਲੋ ਲਈ ਆਮ ਗਲਤੀਆਂ, ਠੀਕ ਕਰਨ ਦੇ ਤਰੀਕੇ ਅਤੇ ਡੀਬੱਗਿੰਗ ਰਣਨੀਤੀਆਂ ਨੂੰ ਕਵਰ ਕਰਦਾ ਹੈ।

## ਏਜੰਟ ਆਉਟਪੁਟ ਸਮੱਸਿਆਵਾਂ

### GapAnalyzer ਕਹਿੰਦਾ ਹੈ "ਮੇਰੇ ਕੋਲ ਅਜੇ ਵੀ ਮਿਲਦਾ-जੁਲਦਾ ਰਿਪੋਰਟ ਨਹੀਂ ਹੈ"

**ਲੱਛਣ:** GapAnalyzer ਦਾ ਜਵਾਬ ਤੁਹਾਨੂੰ ਮਿਲਦਾ-जੁਲਦਾ ਰਿਪੋਰਟ "ਗੁਆਂਢੀ ਕੌਸ਼ਲ" ਅਤੇ "ਸਰਟੀਫਿਕੇਸ਼ਨ ਗੈਪ" ਨਾਲ ਚਿਪਕਾਉਣ ਲਈ ਕਹਿੰਦਾ ਹੈ। ਇਹ ਉਸ ਵੇਲੇ ਵੀ ਹੁੰਦਾ ਹੈ ਜਦੋਂ ਤੁਸੀਂ ਦੋਹਾਂ ਰੈਜ਼ੂਮ ਅਤੇ ਨੌਕਰੀ ਦਾ ਵੇਰਵਾ ਭੇਜਿਆ ਹੋਵੇ।

**ਕਾਰਨ:** JD ਟੈਕਸਟ JD ਏਜੰਟ ਨੂੰ ਅੱਗੇ ਨਹੀਂ ਭੇਜਿਆ ਗਿਆ ਸੀ। `context_mode="last_agent"` ਨਾਲ, `resume_executor` ਇੱਕੋexecutor ਹੈ ਜੋ ਵਰਤੋਂਕਾਰ ਦਾ ਮੂਲ ਸੁਨੇਹਾ ਵੇਖਦਾ ਹੈ। ਜੇ `RESUME_PARSER_INSTRUCTIONS` ਆਪਣੇ ਆਉਟਪੁਟ ਵਿੱਚ JD ਟੈਕਸਟ ਨਹੀਂ ਸ਼ਾਮਲ ਕਰਦਾ, ਤਾਂ JD ਏਜੰਟ ਕੋਲ ਕੋਈ JD ਨਹੀਂ ਹੁੰਦਾ, MatchingAgent ਫਿਟ ਸਕੋਰ ਕੈਲਕੁਲੇਟ ਨਹੀਂ ਕਰ ਸਕਦਾ, ਅਤੇ GapAnalyzer ਨੂੰ ਬੇਮਤਲਬ ਇਨਪੁਟ ਮਿਲਦੀ ਹੈ।

**ਨਿਧਾਨ:**

ਸਰਵਰ ਲਾਗ ਵਿਚ, MatchingAgent ਸਪੈਨ ਦੀ ਜਾਂਚ ਕਰੋ। ਜੇ ਇਸ ਵਿੱਚ:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
ਪਾਸ-ਥਰੂ ਗੁੰਮ ਜਾਂ ਟੁੱਟ ਗਿਆ ਹੈ।

**ਠੀਕ ਕਰਨ:** ਇਹ ਪੁਸ਼ਟੀ ਕਰੋ ਕਿ `main.py` ਵਿੱਚ `RESUME_PARSER_INSTRUCTIONS` ਵਿੱਚ `[JOB DESCRIPTION PASS-THROUGH]` ਸੈਕਸ਼ਨ ਅਤੇ ਨਿਯਮ ਸ਼ਾਮਲ ਹਨ:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
ਇਸਦੇ ਨਾਲ ਇਹ ਵੀ ਪੱਕਾ ਕਰੋ ਕਿ `JOB_DESCRIPTION_INSTRUCTIONS` ਵਿੱਚ `[PARSED RESUME PASS-THROUGH]` ਰੀਲੇ ਨਿਯਮ ਹੈ:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
ਜੇ ਕਿਸੇ ਵੀ ਨਿਦੇਸ਼ ਬਲਾਕ ਦੀ ਬਣਤਰ ਵੇਜਾਰਡ ਤੋਂ ਸਟੱਬ ਹੈ, ਤਾਂ ਇਸ ਨੂੰ ਸਪੂਰਨ ਵਰਜਨ ਨਾਲ ਬਦਲੋ ਜੋ [PersonalCareerCopilot/main.py](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ਵਿੱਚ ਹੈ।

### MatchingAgent "Cannot compute fit score - no JD provided" ਆਉਟਪੁਟ ਕਰਦਾ ਹੈ

ਇਹ ਮੁੱਖ ਕਾਰਨ ਉਪਰ ਦਿੱਤਾ ਗਿਆ ਸਮਾਨ ਹੈ। MatchingAgent ਨੂੰ JD ਏਜੰਟ ਦੇ ਆਉਟਪੁਟ ਮਿਲੇ ਪਰ `[PARSED RESUME PASS-THROUGH]` ਸੈਕਸ਼ਨ ਗੁੰਮ ਜਾਂ ਖਾਲੀ ਸੀ, ਇਸ ਲਈ ਉਹ ਦੋ ਪ੍ਰੋਫਾਈਲਾਂ ਦੀ ਤੁਲਨਾ ਨਹੀਂ ਕਰ ਸਕਿਆ। ਪੁਸ਼ਟੀ ਕਰੋ:
1. `JOB_DESCRIPTION_INSTRUCTIONS` ਵਿੱਚ ਰੀਲੇ ਨਿਯਮ ਹੈ: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` ਏਜੰਟ ਨੂੰ `[JD REQUIREMENTS]` ਅਤੇ `[PARSED RESUME PASS-THROUGH]` ਸੈਕਸ਼ਨਾਂ ਲਈ ਵੇਖਣ ਲਈ ਕਹਿੰਦਾ ਹੈ।

ਦੋਹਾਂ ਨਿਰਦੇਸ਼ ਬਲਾਕਾਂ ਨੂੰ [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ਤੋਂ ਸੰਪੂਰਨ ਵਰਜਨਾਂ ਨਾਲ ਬਦਲੋ।

### ਜਵਾਬ ਦੋ ਵਾਰ ਦਿਖਾਈ ਦੇਂਦਾ ਹੈ

**ਲੱਛਣ:** GapAnalyzer ਦਾ ਆਉਟਪੁਟ (ਜਾਂ ਪੂਰਾ ਪਾਈਪਲਾਈਨ ਆਉਟਪੁਟ) ਏਜੰਟ ਇੰਸਪੈਕਟਰ ਜਵਾਬ ਵਿੱਚ ਦੋ ਵਾਰੀ ਦਿਖਾਈ ਦਿੰਦਾ ਹੈ।

**ਕਾਰਨ:** `WorkflowBuilder` ਆਉਂਦੇ ਐਜਾਂ ਲਈ OR-ਸਮਾਂਟਿਕਸ ਵਰਤਦਾ ਹੈ - ਜਦੋਂ ਕੋਈ ਵੀ ਪਿਛੋਕੜ ਮੁਕੰਮਲ ਹੋ ਜਾਂਦਾ ਹੈ ਤਾਂ ਨਵੀਨ executor ਟਰਿੱਗਰ ਹੁੰਦਾ ਹੈ। ਜੇ `matching_executor` ਦੇ ਦੋ ਆਉਣ ਵਾਲੇ ਐਜ ਹਨ (`resume_executor` ਅਤੇ `jd_executor` ਤੋਂ), ਤਾਂ ਉਹ ਦੋ ਵਾਰੀ ਚਲਦਾ ਹੈ: ਇੱਕ ਵਾਰੀ ResumeParser ਖਤਮ ਹੋਣ ਤੇ ਅਤੇ ਦੂਜਾ ਵਾਰੀ JD Agent ਖਤਮ ਹੋਣ ਤੇ। ਫਿਰ GapAnalyzer ਵੀ ਦੋ ਵਾਰੀ ਚਲਦਾ ਹੈ।

**ਠੀਕ ਕਰਨ:** ਯਕੀਨੀ ਬਣਾਓ ਕਿ `WorkflowBuilder` ਗ੍ਰਾਫ ਸਖਤ ਤੌਰ ਤੇ ਕੁੜੀ ਹੁੰਦੇ ਆ ਪਾਈਪਲਾਈਨ ਹੈ ਜਿਸ ਵਿੱਚ ਕੋਈ ਫੈਨ-ਇਨ ਨਾ ਹੋਵੇ:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # ਰਿਜ਼ੂਮੇ_ਐਗਜ਼ੀਕਿਊਟਰ ਤੋਂ ਨਹੀਂ
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

ਜੇ ਤੁਹਾਡੇ ਕੋਲ ਕੋਈ ਅਜਿਹਾ `.add_edge(resume_executor, matching_executor)` ਲਾਈਨ ਹੈ, ਤਾਂ ਇਸ ਨੂੰ ਹਟਾ ਦਿਓ। JD ਏਜੰਟ ਦੇ ਆਉਟਪੁਟ ਵਿੱਚ `[PARSED RESUME PASS-THROUGH]` ਰੀਲੇ ਪਹਿਲਾਂ ਹੀ MatchingAgent ਨੂੰ ਰੈਜ਼ੂਮ ਤੱਕ ਪਹੁੰਚ ਦਿੰਦਾ ਹੈ।

---

## ਵਾਤਾਵਰਣ ਅਤੇ ਸੰਰਚਨਾ ਸਮੱਸਿਆਵਾਂ

### ਗੁੰਮ ਜਾਂ ਗਲਤ `.env` ਮੁੱਲ

`.env` ਫਾਇਲ ਨੂੰ `PersonalCareerCopilot/` ਡਾਇਰੈਕਟਰੀ ਵਿੱਚ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ (ਉਹੀ ਪੱਧਰ ਜਿੱਥੇ `main.py` ਹੈ):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

ਉਮੀਦਵਾਰ `.env` ਸਮੱਗਰੀ:

**ਮਾਰਗ A - Foundry ਕਲਾਉਡ:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**ਮਾਰਗ B - Foundry ਲੋਕਲ:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> ਦੋਹਾਂ ਮਾਰਗਾਂ ਵਿੱਚ `FOUNDRY_PROJECT_ENDPOINT` ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ। ਕਦਰ ਵੱਖਰੀ ਹੈ: ਕਲਾਉਡ ਇੱਕ `https://` ਫਾਊਂਡਰੀ ਐਂਡਪੁਇੰਟ ਵਰਤਦਾ ਹੈ; ਲੋਕਲ `http://localhost:5273/v1` ਵਰਤਦਾ ਹੈ। ਮਾਰਗ B ਲਈ ਸਹੀ ਮਾਡਲ ਉਪਨਾਮ ਪੁਸ਼ਟੀ ਕਰਨ ਲਈ `foundry model list` ਚਲਾਓ।

> **ਤੁਹਾਡਾ `FOUNDRY_PROJECT_ENDPOINT` ਲੱਭਣ ਲਈ:** 
- VS ਕੋਡ ਵਿੱਚ **Foundry Toolkit** ਸਾਈਡਬਾਰ ਖੋਲ੍ਹੋ → ਆਪਣੇ ਪ੍ਰੋਜੈਕਟ 'ਤੇ ਰਾਈਟ-ਕਲਿੱਕ ਕਰੋ → **Copy Project Endpoint**। 
- ਜਾਂ [Azure Portal](https://portal.azure.com) 'ਤੇ ਜਾਓ → ਆਪਣਾ Foundry ਪ੍ਰੋਜੈਕਟ → **Overview** → **Project endpoint**।

> **ਤੁਹਾਡਾ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ਲੱਭਣ ਲਈ:** Foundry Toolkit ਸਾਈਡਬਾਰ ਵਿੱਚ ਆਪਣੇ ਪ੍ਰੋਜੈਕਟ ਨੂੰ ਵਡਾਓ → **Models** → ਆਪਣੀ ਡਿਪਲੌਏ ਕੀਤੀ ਮਾਡਲ ਨਾਮ ਲੱਭੋ (ਜਿਵੇਂ `gpt-4.1-mini`)।

### Env ਵਰ ਤਰਜੀਹ

`main.py` `load_dotenv(override=True)` ਵਰਤਦਾ ਹੈ, ਜਿਸਦਾ ਮਤਲਬ:

| ਤਰਜੀਹ | ਸਰੋਤ | ਦੋਹਾਂ ਸੈੱਟ ਹੋਣ 'ਤੇ ਕਿਹੜਾ ਜਿੱਤਦਾ ਹੈ? |
|----------|--------|------------------------|
| 1 (ਸਭ ਤੋਂ ਉੱਚਾ) | `.env` ਫਾਇਲ | ਹਾਂ |
| 2 | ਸ਼ੈੱਲ / ਕੰਟੇਨਰ ਵਾਤਾਵਰਣ ਪਰਿਵਰਤਨਸ਼ੀਲ | ਉਹਦੇ ਲਈ ਵਰਤੀ ਜਾਂਦੀ ਹੈ ਜਦ `.env` ਵਿੱਚ ਤੇ ਕਿਸੇ ਹੋਰ ਚਾਬੀ ਮੌਜੂਦ ਨਾ ਹੋਵੇ |

ਲੋਕਲ ਵਿਕਾਸ ਵਿੱਚ, ਇਸ ਦਾ ਮਤਲਬ `.env` ਸੱਚਾਈ ਦਾ ਸਰੋਤ ਹੈ (`.env` ਸੰਪਾਦਨ ਨਾਲ ਇੱਕ ਦਮ ਰੱਨ ਪ੍ਰਭਾਵਿਤ ਹੁੰਦੇ ਹਨ)। ਹੋਸਟ ਕੀਤੇ ਡਿਪਲੌਇਮੈਂਟ ਵਿੱਚ, Foundry ਵਾਤਾਵਰਣ ਪਰਿਵਰਤਨਸ਼ੀਲਾਂ ਨੂੰ ਕੰਟੇਨਰ ਪੱਧਰ ਤੇ ਦਾਖਲ ਕਰਦਾ ਹੈ; ਕਿਉਂਕਿ `.env` ਇਸ ਲੈਬ ਸੈਟਅਪ ਲਈ ਤਸਵੀਰ ਦਾ ਹਿੱਸਾ ਨਹੀਂ ਹੈ, ਇਸ ਲਈ ਦਾਖਲ ਕੀਤੇ ਗਏ ਕੰਟੇਨਰ ਮੁੱਲ ਵਰਤੇ ਜਾਂਦੇ ਹਨ।

---

## ਵਰਜਨ ਅਨੁਕੂਲਤਾ

### ਪੈਕੇਜ ਵਰਜਨ ਮੈਟ੍ਰਿਕਸ

ਬਹੁ-ਏਜੰਟ ਵਰਕਫਲੋ ਨੂੰ ਖਾਸ ਪੈਕੇਜ ਵਰਜਨਾਂ ਦੀ ਲੋੜ ਹੈ। ਗਲਤ ਮਿਲਦੇ-ਜੁਲਦੇ ਵਰਜਨ ਰੰਟਾਈਮ ਗਲਤੀਆਂ ਦਾ ਕਾਰਨ ਹੁੰਦੇ ਹਨ।

| ਪੈਕੇਜ | ਲੋੜੀਂਦਾ ਵਰਜਨ | ਜਾਂਚ ਕਮਾਂਡ |
|---------|-----------------|---------------|
| `agent-framework-foundry` | تازہ ترین | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | تازہ ترین | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | تازہ ترین | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### ਆਮ ਵਰਜਨ ਦੀਆਂ ਗਲਤੀਆਂ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ਸਹੀ ਕਰੋ: agent-framework-foundry ਨੂੰ ਮੁੜ ਇੰਸਟਾਲ ਕਰੋ
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ਠੀਕ ਕਰੋ: mcp ਪੈਕੇਜ ਨੂੰ ਅਪਗ੍ਰੇਡ ਕਰੋ
pip install mcp --upgrade
```

### ਸਾਰੇ ਵਰਜਨ ਇੱਕ ਵਾਰੀ ਫਿਰ ਜਾਂਚੋ

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

ਉਮੀਦਵਾਰ ਆਉਟਪੁਟ:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## ਤਾਇਨਾਤੀ ਸਮੱਸਿਆਵਾਂ

### ਤਾਇਨਾਤੀ ਤੋਂ ਬਾਅਦ ਕੰਟੇਨਰ ਸ਼ੁਰੂ ਨਹੀਂ ਹੁੰਦਾ

1. **ਕੰਟੇਨਰ ਲਾਗ ਚੈੱਕ ਕਰੋ:**
   - **Foundry Toolkit** ਸਾਈਡਬਾਰ ਖੋਲ੍ਹੋ → **Hosted Agents (Preview)** ਵਧਾਓ → ਆਪਣਾ ਏਜੰਟ ਕਲਿੱਕ ਕਰੋ → ਵਰਜਨ ਵਧਾਓ → **Container Details** → **Logs**।
   - ਪਾਇਥਨ ਸਟੈਕ ਟ੍ਰੇਸ ਜਾ ਮਾਡਿਊਲ ਗੁੰਮ ਹੋਣ ਵਾਲੀਆਂ ਗਲਤੀਆਂ ਖੋਜੋ।

2. **ਆਮ ਕੰਟੇਨਰ ਸ਼ੁਰੂਆਤੀ ਨਾਕਾਮੀਆਂ:**

   | ਲਾਗ ਵਿੱਚ ਗਲਤੀ | ਕਾਰਨ | ਠੀਕ ਕਰੋ |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` ਵਿੱਚ ਪੈਕੇਜ ਨਹੀਂ | ਪੈਕੇਜ ਸ਼ਾਮਲ ਕਰੋ, ਦੁਬਾਰਾ ਤਾਇਨਾਤੀ ਕਰੋ |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` ਜਾਂ `.env` env ਵਰ ਨਾ ਸੈੱਟ | `agent.yaml` → `environment_variables` ਡਿੱਠਾ (ਹੋਸਟ ਕੀਤਾ) ਜਾਂ `.env` (ਲੋਕਲ) ਅਪਡੇਟ ਕਰੋ |
   | `azure.identity.CredentialUnavailableError` | ਮੈਨੇਜ ਕੀਤੀ ਵਿਅਕਤੀਗਤ ਪਛਾਣ ਨਹੀਂ ਸੈੱਟ | Foundry ਆਪਣੇ ਆਪ ਸੈੱਟ ਕਰਦਾ ਹੈ - ਯਕੀਨੀ ਬਣਾਓ ਤੁਸੀਂ ਐਕਸਟੇਂਸ਼ਨ ਰਾਹੀਂ ਤਾਇਨਾਤੀ ਕਰ ਰਹੇ ਹੋ |
   | `OSError: port 8088 already in use` | Dockerfile ਗਲਤ ਪੋਰਟ ਖੋਲ੍ਹਦਾ ਜਾਂ ਪੋਰਟ ਟਕਰਾਅ | Dockerfile ਵਿੱਚ `EXPOSE 8088` ਜਾਂ `CMD ["python", "main.py"]` ਦੀ ਪੜਤਾਲ ਕਰੋ |
   | ਕੰਟੇਨਰ ਕੋਡ 1 ਨਾਲ ਬੰਦ | `main()` ਵਿੱਚ ਅਣਹੈਂਡਲਡ ਐਕਸਪਸ਼ਨ | ਪਹਿਲਾਂ ਲੋਕਲ [ਮੋਡੀਊਲ 5](05-test-locally.md) ਵਿੱਚ ਜाँच ਕਰੋ |

3. **ਠੀਕ ਕਰਨ ਤੋਂ ਬਾਅਦ ਦੁਬਾਰਾ ਤਾਇਨਾਤੀ ਕਰੋ:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → ਉਹੀ ਏਜੰਟ ਚੁਣੋ → ਨਵੀਂ ਵਰਜਨ ਤਾਇਨਾਤੀ ਕਰੋ।

### ਤਾਇਨਾਤੀ ਨੂੰ ਜ਼ਿਆਦਾ ਸਮਾਂ ਲੱਗਣ

ਬਹੁ-ਏਜੰਟ ਕੰਟੇਨਰ ਸਟਾਰਟ ਹੋਣ ਵਿੱਚ ਜ਼ਿਆਦਾ ਸਮਾਂ ਲੈਂਦੇ ਹਨ ਕਿਉਂਕਿ ਸ਼ੁਰੂਆਤ 'ਤੇ 4 ਏਜੰਟ ਉਦਾਹਰਣ ਬਣਦੇ ਹਨ। ਆਮ ਸ਼ੁਰੂਆਤੀ ਸਮਾਂ:

| ਦੌਰਾਨਾ | ਉਮੀਦਵਾਰ ਸਮਾਂ |
|-------|------------------|
| ਕੰਟੇਨਰ ਇਮੇਜ ਬਿਲਡ | 1-3 ਮਿੰਟ |
| ਇਮੇਜ ਨੂੰ ACR ਤੇ ਧਕਾ | 30-60 ਸੈਕਿੰਡ |
| ਕੰਟੇਨਰ ਸਟਾਰਟ (ਇੱਕ ਏਜੰਟ) | 15-30 ਸੈਕਿੰਡ |
| ਕੰਟੇਨਰ ਸਟਾਰਟ (ਬਹੁ ਏਜੰਟ) | 30-120 ਸੈਕਿੰਡ |
| ਅਜੇੰਟ ਖੇਡ ਸਥਲ 'ਚ ਉਪਲਬਧ | "ਸ਼ੁਰੂ ਹੋਇਆ" ਤੋਂ 1-2 ਮਿੰਟ ਬਾਅਦ |

> ਜੇ "Pending" 5 ਮਿੰਟ ਤੋਂ ਵੱਧ ਰਹਿੰਦਾ ਹੈ ਤਾਂ ਕੰਟੇਨਰ ਲਾਗਾਂ ਖ਼ਤਾਰਨਾ।

---

## RBAC ਅਤੇ ਅਧਿਕਾਰ ਸਮੱਸਿਆਵਾਂ

### `403 Forbidden` ਜਾਂ `AuthorizationFailed`

ਤੁਹਾਨੂੰ ਆਪਣੇ Foundry ਪ੍ਰੋਜੈਕਟ 'ਤੇ **[Foundry User](https://aka.ms/foundry-ext-project-role)** ਭੂਮਿਕਾ ਚਾਹੀਦੀ ਹੈ (ਪਹਿਲਾਂ **Azure AI User** ਕਿਹਾ ਜਾਂਦਾ ਸੀ - ਭੂਮਿਕਾ ID ਅਟੱਲ ਹੈ):

1. [Azure Portal](https://portal.azure.com) 'ਤੇ ਜਾਓ → ਆਪਣਾ Foundry **ਪ੍ਰੋਜੈਕਟ** ਸਾਧਨ।
2. **Access control (IAM)** → **Role assignments** ਤੇ ਕਲਿੱਕ ਕਰੋ।
3. ਆਪਣਾ ਨਾਮ ਖੋਜੋ → ਯਕੀਨ ਕਰੋ **Foundry User** (ਜਾਂ ਪੁਰਾਣਾ ਨਾਮ **Azure AI User**) ਲਿਸਟ ਵਿੱਚ ਹੈ।
4. ਜੇ ਮੌਜੂਦ ਨਹੀਂ: **Add** → **Add role assignment** → **Foundry User** ਖੋਜੋ → ਆਪਣੇ ਖਾਤੇ ਨੂੰ ਨਿਰਧਾਰਿਤ ਕਰੋ।

ਵਿਸਥਾਰ ਲਈ [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ਦਸਤਾਵੇਜ਼ ਵੇਖੋ।

### ਮਾਡਲ ਡਿਪਲੌਇਮੈਂਟ ਉਪਲੱਬਧ ਨਹੀਂ

ਜੇ ਏਜੰਟ ਮਾਡਲ ਸਬੰਧੀ ਗਲਤੀਆਂ ਵਾਪਰਦਾ ਹੈ:

1. ਪੁਸ਼ਟੀ ਕਰੋ ਕਿ ਮਾਡਲ ਡਿਪਲੌਏਡ ਹੈ: Foundry ਸਾਈਡਬਾਰ → ਪ੍ਰੋਜੈਕਟ ਵਧਾਓ → **Models** → `gpt-4.1-mini` (ਜਾਂ ਆਪਣਾ ਮਾਡਲ) ਦੇ ਨਾਲ ਸਥਿਤੀ **Succeeded** ਨੂੰ ਜਾਂਚੋ।
2. ਡਿਪਲੌਇਮੈਂਟ ਨਾਮ ਮੈਚ ਕਰਦਾ ਹੈ: `.env` (ਜਾਂ `agent.yaml`) ਵਿੱਚ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ਨਾਲ ਸਾਈਡਬਾਰ ਵਿਚਲਾ ਅਸਲੀ ਡਿਪਲੌਇਮੈਂਟ ਨਾਮ ਤુલਨਾ ਕਰੋ।
3. ਜੇ ਡਿਪਲੌਇਮੈਂਟ ਮਿਆਦ ਮੁਕੰਮਲ ਹੋ ਚੁੱਕੀ (ਮੁਫਤ ਟੀਅਰ): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) ਤੋਂ ਦੁਬਾਰਾ ਡਿਪਲੌਇ ਕਰੋ (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)।

---

## Foundry ਲੋਕਲ ਸਮੱਸਿਆਵਾਂ (ਮਾਰਗ B)

### Foundry ਲੋਕਲ ਸੇਵਾ ਚੱਲ ਰਹੀ ਨਹੀਂ

```powershell
# ਸਥਿਤੀ ਦੀ ਜਾਂਚ ਕਰੋ
foundry local status

# ਜੇ ਸੇਵਾ ਰੁਕੀ ਹੋਈ ਹੈ ਤਾਂ ਇਸ ਨੂੰ ਸ਼ੁਰੂ ਕਰੋ
foundry local start
```

| ਲੱਛਣ | ਕਾਰਨ | ਠੀਕ ਕਰੋ |
|---------|-------|-----|
| ਹੈਲਥ ਚੈੱਕ `503` ਦਿੰਦਾ ਹੈ | ਸੇਵਾ ਸ਼ੁਰੂ ਨਹੀਂ ਹੋਈ | `foundry local start` ਚਲਾਓ ਜਾਂ Foundry Toolkit ਸਾਈਡਬਾਰ ਵਿੱਚ **Start** 'ਤੇ ਕਲਿੱਕ ਕਰੋ |
| ਹੈਲਥ ਚੈੱਕ ਸਮਾਂ ਸਮਾਪਤ ਹੋ ਜਾਂਦਾ ਹੈ | ਮਾਡਲ ਅਜੇ ਵੀ ਲੋਡ ਹੋ ਰਿਹਾ ਹੈ | ਸ਼ੁਰੂਆਤ ਤੋਂ ਬਾਅਦ 30–60 ਸਕਿੰਟ ਉਡੀਕੋ; ਵੱਡੇ ਮਾਡਲ ਜ਼ਿਆਦਾ ਸਮਾਂ ਲੈਂਦੇ ਹਨ |
| `/v1/health` 'ਤੇ `StatusCode: 404` | ਗਲਤ ਪੋਰਟ | ਡਿਫਾਲਟ `5273` ਹੈ। ਅਸਲੀ ਪੋਰਟ ਲਈ `foundry local status` ਦੇਖੋ |
| ਅਪਰੇਸ਼ਨ ਲਈ ਕਮ ਸਰੋਤ | Foundry ਲੋਕਲ ਨੂੰ ~4 GB RAM ਖ਼ਾਲੀ ਚਾਹੀਦੀ ਹੈ | ਹੋਰ ਐਪਲੀਕੇਸ਼ਨ ਬੰਦ ਕਰੋ |
| ਮਾਡਲ ਡਾਊਨਲੋਡ ਫੇਲ | ਡਿਸਕ ਸਥਾਨ ਘੱਟ | ਮਾਡਲ 2–8 GB ਦੇ ਹਨ। ਸਥਾਨ ਖ਼ਾਲੀ ਕਰੋ, ਫੇਰ `foundry model pull <name>` ਚਲਾਓ |

### ਮਾਡਲ ਨਾਮ ਅਣ-ਮੈਚ

```powershell
# ਡਾਊਨਲੋਡ ਕੀਤੇ ਮਾਡਲਾਂ ਅਤੇ ਉਨ੍ਹਾਂ ਦੇ ਸਹੀ ਖਿਤਾਬਾਂ ਦੀ ਸੂਚੀ ਬਣਾਓ
foundry model list
```

`.env` ਵਿੱਚ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ਨੂੰ ਉਹੀ ਸਹੀ ਉਪਨਾਮ (ਉਦਾਹਰਣ `phi-4-mini`, ਨਾ ਕਿ `Phi-4-mini`) ਸੈੱਟ ਕਰੋ ਜੋ ਦਿਖਾਇਆ ਗਿਆ ਹੈ।

### ਲੋਕਲ ਚਲਾਉਣ 'ਤੇ `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (ਮਾਰਗ B)

ਲੈਬ ਦਾ `main.py` `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` ਵਰਤਦਾ ਹੈ। Foundry ਲੋਕਲ ਨੂੰ ਇਹ ਵੈਰੀਏਬਲ ਸਥਾਨਕ ਸੇਵਾ ਨੂੰ ਤਰਜੀਹ ਦੇਣ ਲਈ ਲੋੜ ਹੈ - **ਨਹੀਂ** `AZURE_AI_PROJECT_ENDPOINT` ਨੂੰ। ਇਹ ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਤੁਹਾਡੀ `.env` ਵਿੱਚ ਹੈ:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP ਟੂਲ ਫਿਰ ਵੀ ਬਾਹਰੀ ਕਾਲ ਕਰਦਾ ਹੈ (ਮਾਰਗ B)

ਇਹ ਉਮੀਦ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। `search_microsoft_learn_for_plan` ਟੂਲ `https://learn.microsoft.com/api/mcp` ਤੋਂ ਸਿੱਖਣ ਵਾਲੇ ਸੰਸਾਧਨ ਲਿਆਉਂਦਾ ਹੈ। **ਸਿਰਫ਼ ਕੌਸ਼ਲ-ਨਾਮ ਕਵੈਰੀ** ਨੈੱਟਵਰਕ 'ਤੇ ਭੇਜੀ ਜਾਂਦੀ ਹੈ - ਰੈਜ਼ੂਮੇ ਅਤੇ JD ਟੈਕਸਟ ਪੂਰੀ ਤਰ੍ਹਾਂ ਤੁਹਾਡੇ ਡਿਵਾਈਸ 'ਤੇ ਪ੍ਰਕਿਰਿਆਵਾਂ ਹਨ ਅਤੇ ਕਦੇ ਭੇਜਿਆਂ ਨਹੀਂ ਜਾਂਦੇ। ਜੇ ਪੂਰੀ ਤਰ੍ਹਾਂ ਆਫਲਾਈਨ ਕਾਰਵਾਈ ਚਾਹੀਦੀ ਹੈ, ਤਾਂ ਟੂਲ ਵਿੱਚ ਇੱਕ `try/except` ਫਾਲਬੈਕ ਸ਼ਾਮਲ ਕਰੋ ਜੋ endpoint ਅਣਪਹੁੰਚ ਰਹਿਣ 'ਤੇ static `learn.microsoft.com` URL ਵਾਪਸ ਕਰਦਾ ਹੈ।

---

## ਮਦਦ ਪ੍ਰਾਪਤ ਕਰਨਾ

ਜੇ ਤੁਸੀਂ ਉਪਰ ਦਿੱਤੇ ਠੀਕ ਕਰਨ ਦੇ ਤਰੀਕੇ ਅਪਣਾਉਣ ਤੋਂ ਬਾਅਦ ਫਸੇ ਹੋ:

1. **ਸਰਵਰ ਲਾਗ ਚੈੱਕ ਕਰੋ** - ਵੱਧਤਰ ਗਲਤੀਆਂ ਟਰਮੀਨਲ ਵਿੱਚ ਪਾਇਥਨ ਸਟੈਕ ਟਰੇਸ ਬਣਾਉਂਦੀਆਂ ਹਨ। ਪੂਰਾ ਟਰੇਸ ਪੜ੍ਹੋ।
2. **ਗਲਤੀ ਸੁਨੇਹਾ ਖੋਜੋ** - ਗਲਤੀ ਦੇ ਪਾਠ ਨੂੰ ਕਾਪੀ ਕਰੋ ਅਤੇ [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) ਵਿੱਚ ਖੋਜ ਕਰੋ।
3. **ਇੱਕ ਇਸ਼ੂ ਖੋਲ੍ਹੋ** - [ਵਰਕਸ਼ਾਪ ਰਿਪੋਜ਼ਟਰੀ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) ਤੇ ਇੱਕ ਇਸ਼ੂ ਦਾਖਲ ਕਰੋ:
   - ਗਲਤੀ ਸੁਨੇਹਾ ਜਾਂ ਸਕਰੀਨਸ਼ਾਟ
   - ਤੁਹਾਡੇ ਪੈਕੇਜ ਵਰਜਨ (`pip list | Select-String "agent-framework"`)
   - ਤੁਹਾਡੀ ਪਾਇਥਨ ਵਰਜਨ (`python --version`)
   - ਸਮੱਸਿਆ ਲੋਕਲ ਹੈ ਜਾਂ ਤਾਇਨਾਤੀ ਤੋਂ ਬਾਅਦ

---

### ਚੈਕਪੌਇੰਟ

- [ ] ਤੁਸੀਂ `.env` ਸੰਰਚਨਾ ਸਮੱਸਿਆਵਾਂ ਚੈੱਕ ਅਤੇ ਠੀਕ ਕਰਨਾ ਜਾਣਦੇ ਹੋ
- [ ] ਤੁਸੀਂ ਪੈਕੇਜ ਵਰਜਨਾਂ ਨੂੰ ਲੋੜੀਂਦੇ ਮੈਟ੍ਰਿਕਸ ਨਾਲ ਮੇਲ ਖਾਣ ਦੀ ਪੁਸ਼ਟੀ ਕਰ ਸਕਦੇ ਹੋ
- [ ] ਤੁਸੀਂ ਤਾਇਨਾਤੀ ਫੇਲਯਤਾਂ ਲਈ ਕੰਟੇਨਰ ਲਾਗਾਂ ਚੈੱਕ ਕਰਨਾ ਜਾਣਦੇ ਹੋ
- [ ] ਤੁਸੀਂ ਅਜ਼ੂਰ ਪੋਰਟਲ ਵਿੱਚ RBAC ਰੋਲਾਂ ਦੀ ਪੁਸ਼ਟੀ ਕਰ ਸਕਦੇ ਹੋ

---

**ਪਿਛਲਾ:** [07 - Verify in Playground](07-verify-in-playground.md) · **ਅਗਲਾ:** [09 - Summary →](09-summary.md) · **ਘਰ:** [Lab 02 README](../README.md) · [ਵਰਕਸ਼ਾਪ ਘਰ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਪਣ**:
ਇਸ ਦਸਤਾਵੇਜ਼ ਦਾ ਅਨੁਵਾਦ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾਵਾਂ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮੱਤਿਆਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੇ ਉਪਯੋਗ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆਵਾਂ ਲਈ ਜਵਾਬਦੇਹ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->