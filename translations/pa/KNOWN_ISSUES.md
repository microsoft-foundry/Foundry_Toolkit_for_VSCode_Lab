# ਜਾਣੀਆਂ ਸਮੱਸਿਆਵਾਂ

ਇਹ ਦਸਤਾਵੇਜ਼ ਮੌਜੂਦਾ ਰਿਪੋਜ਼ਟਰੀ ਦੀ ਸਥਿਤੀ ਨਾਲ ਸਬੰਧਿਤ ਜਾਣੀਆਂ ਸਮੱਸਿਆਵਾਂ ਨੂੰ ਟ੍ਰੈਕ ਕਰਦਾ ਹੈ।

> ਆਖਰੀ ਵਾਰੀ ਅੱਪਡੇਟ ਕੀਤਾ: 2026-04-15। Python 3.13 / Windows ਵਿੱਚ `.venv_ga_test` ਵਿੱਚ ਟੈਸਟ ਕੀਤਾ ਗਿਆ।

---

## ਮੌਜੂਦਾ ਪੈਕੇਜ ਪਿਨ (ਤਿੰਨੋ ਏਜੰਟਸ ਲਈ)

| Package | Current Version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(ਸੁਧਾਰਿਆ — ਦੇਖੋ KI-003)* |

---

## KI-001 — GA 1.0.0 ਅਪਗ੍ਰੇਡ ਰੋਕਿਆ ਗਿਆ: `agent-framework-azure-ai` ਹਟਾ ਦਿੱਤਾ ਗਿਆ

**ਸਤਿਤੀ:** ਖੁੱਲ੍ਹਾ | **ਗੰਭੀਰਤਾ:** 🔴 ਉੱਚ | **ਕਿਸਮ:** ਤੋੜਨ ਵਾਲਾ

### ਵਰਣਨ

`agent-framework-azure-ai` ਪੈਕੇਜ (ਜੋ `1.0.0rc3` ਤੇ ਪਿੰਨ ਕੀਤਾ ਗਿਆ ਸੀ) GA ਰਿਲੀਜ਼ (1.0.0, 2026-04-02 ਨੂੰ ਜਾਰੀ ਕੀਤੀ ਗਈ) ਵਿੱਚ **ਹਟਾ ਦਿੱਤਾ/ਡਿਪ੍ਰੀਕੇਟ ਕਰ ਦਿੱਤਾ ਗਿਆ** ਹੈ। ਇਹ ਇਸ ਨਾਲ ਬਦਲਿਆ ਗਿਆ ਹੈ:

- `agent-framework-foundry==1.0.0` — ਫਾਊਂਡਰੀ-ਹੋਸਟਿਡ ਏਜੰਟ ਪੈਟਰਨ
- `agent-framework-openai==1.0.0` — OpenAI-ਅਧਾਰਿਤ ਏਜੰਟ ਪੈਟਰਨ

ਤਿੰਨੋ `main.py` ਫਾਈਲਾਂ `agent_framework.azure` ਤੋਂ `AzureAIAgentClient` ਨੂੰ ਇੰਪੋਰਟ ਕਰਦੀਆਂ ਹਨ, ਜੋ GA ਪੈਕੇਜਾਂ ਹੇਠਾਂ `ImportError` ਉਠਾਉਂਦਾ ਹੈ। GA ਵਿੱਚ `agent_framework.azure` ਨੇਮਸਪੇਸ ਹਾਲੇ ਵੀ ਮੌਜੂਦ ਹੈ, ਪਰ ਹੁਣ ਇਸ ਵਿੱਚ ਸਿਰਫ Azure Functions ਕਲਾਸਜ਼ ਹਨ (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ਫਾਊਂਡਰੀ ਏਜੰਟ ਨਹੀਂ।

### ਪੱਕੀ ਕੀਤੀ ਗਈ ਗਲਤੀ (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### ਪ੍ਰਭਾਵਿਤ ਫਾਈਲਾਂ

| ਫਾਈਲ | ਲਾਈਨ |
|-------|-------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` ਨਾਲ ਅਣਅਨੁਕੂਲ

**ਸਤਿਤੀ:** ਖੁੱਲ੍ਹਾ | **ਗੰਭੀਰਤਾ:** 🔴 ਉੱਚ | **ਕਿਸਮ:** ਤੋੜਨ ਵਾਲਾ (ਅਪਸਟਰੀਮ 'ਤੇ ਰੁਕਿਆ)

### ਵਰਣਨ

`azure-ai-agentserver-agentframework==1.0.0b17` (ਤਾਜ਼ਾ) ਸਖਤ ਪਿੰਨ ਕਰਦਾ ਹੈ
`agent-framework-core<=1.0.0rc3`। ਇਸਨੂੰ `agent-framework-core==1.0.0` (GA) ਨਾਲ ਇੰਸਟਾਲ ਕਰਨ ਨਾਲ pip ਨੂੰ
ਮਜ਼ਬੂਰ ਕਰਦਾ ਹੈ ਕਿ ਉਹ `agent-framework-core` ਨੂੰ ਮੁੜ `rc3` ਤੇ ਡਾਊਨਗ੍ਰੇਡ ਕਰੇ, ਜੋ `agent-framework-foundry==1.0.0` ਅਤੇ `agent-framework-openai==1.0.0` ਨੂੰ ਤੋੜਦਾ ਹੈ।

ਇਸ ਲਈ ਸਾਰੇ ਏਜੰਟਾਂ ਵੱਲੋਂ HTTP ਸਰਵਰ ਬਾਈਂਡ ਕਰਨ ਲਈ ਵਰਤੀ ਜਾਣ ਵਾਲੀ ਕਾਲ `from azure.ai.agentserver.agentframework import from_agent_framework` ਵੀ ਰੁਕੀ ਰਹਿੰਦੀ ਹੈ।

### ਪੱਕੀ dependency ਸੰਘਰਸ਼ (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### ਪ੍ਰਭਾਵਿਤ ਫਾਈਲਾਂ

ਸਾਰੇ ਤਿੰਨ `main.py` ਫਾਈਲਾਂ — ਇਮਪੋਰਟ ਦੇ ਸਿਖਰਲੇ ਪੱਧਰ ‘ਤੇ ਅਤੇ `main()` ਵਿੱਚ ਫੰਕਸ਼ਨ ਆਵਾਜਾਈ ਵਿੱਚ ਦੋਹਾਂ।

---

## KI-003 — `agent-dev-cli --pre` ਫਲੈਗ ਹੁਣ ਲੋੜੀਂਦਾ ਨਹੀਂ

**ਸਤਿਤੀ:** ✅ ਸੁਧਾਰਿਆ (ਨਾ-ਤੋੜਨ ਵਾਲਾ) | **ਗੰਭੀਰਤਾ:** 🟢 ਘੱਟ

### ਵਰਣਨ

ਸਾਰੇ `requirements.txt` ਫਾਈਲਾਂ ਪਹਿਲਾਂ `agent-dev-cli --pre` ਸ਼ਾਮਲ ਕਰਦੀਆਂ ਸੀ ਤਾਂ ਜੋ
ਪ੍ਰੀ-ਰਿਲੀਜ਼ CLI ਖਿੱਚਿਆ ਜਾ ਸਕੇ। GA 1.0.0 2026-04-02 ਨੂੰ ਜਾਰੀ ਹੋਣ ਤੋਂ ਬਾਅਦ,
`agent-dev-cli` ਦਾ ਸਥਿਰ ਰਿਲੀਜ਼ ਹੁਣ `--pre` ਫਲੈਗ ਬਿਨਾਂ ਉਪਲੱਬਧ ਹੈ।

**ਲਾਗੂ ਕੀਤਾ ਸੁਧਾਰ:** ਤਿੰਨੋ `requirements.txt` ਫਾਈਲਾਂ ਵਿੱਚੋਂ `--pre` ਫਲੈਗ ਹਟਾ ਦਿੱਤਾ ਗਿਆ ਹੈ।

---

## KI-004 — Dockerfiles `python:3.14-slim` (ਪ੍ਰੀ-ਰਿਲੀਜ਼ ਬੇਸ ਇਮੇਜ) ਵਰਤਦੇ ਹਨ

**ਸਤਿਤੀ:** ਖੁੱਲ੍ਹਾ | **ਗੰਭੀਰਤਾ:** 🟡 ਘੱਟ

### ਵਰਣਨ

ਸਾਰੇ `Dockerfile`s `FROM python:3.14-slim` ਵਰਤਦੇ ਹਨ ਜੋ ਕਿ ਪ੍ਰੀ-ਰਿਲੀਜ਼ Python ਬਨਾਵਟ ਨੂੰ ਟ੍ਰੈਕ ਕਰਦਾ ਹੈ।
ਉਤਪਾਦਨ ਵਿਕਾਸ ਲਈ ਇਸਨੂੰ ਸਥਿਰ ਰਿਲੀਜ਼ (ਜਿਵੇਂ `python:3.12-slim`) 'ਤੇ ਪਿੰਨ ਕੀਤਾ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ।

### ਪ੍ਰਭਾਵਿਤ ਫਾਈਲਾਂ

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## ਸੰਦਰਭ

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਕਤ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾ ਲਈ ਯਤਨ ਕਰਦੇ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਵਿੱਚ ਰੱਖੋ ਕਿ ਆਟੋਮੈਟਿਕ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸੁਚਿਤਤਾ ਹੋ ਸਕਦੀ ਹੈ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੇ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਪ੍ਰਮਾਣਿਤ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ਾਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਿਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਉਪਜੀਆਂ ਕੋਈ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਭੇੜਭਾੜ ਲਈ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->