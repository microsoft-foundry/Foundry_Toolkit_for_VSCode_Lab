# Known Issues

This document tracks known issues with the current repository state.

> Last updated: 2026-04-15. Tested against Python 3.13 / Windows in `.venv_ga_test`.

---

## Current Package Pins (all three agents)

| Package | Current Version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fixed — see KI-003)* |

---

## KI-001 — GA 1.0.0 Upgrade Blocked: `agent-framework-azure-ai` Removed

**Status:** Open | **Severity:** 🔴 High | **Type:** Breaking

### Description

The `agent-framework-azure-ai` package (pinned at `1.0.0rc3`) was **removed/deprecated**
in the GA release (1.0.0, released 2026-04-02). It is replaced by:

- `agent-framework-foundry==1.0.0` — Foundry-hosted agent pattern
- `agent-framework-openai==1.0.0` — OpenAI-backed agent pattern

All three `main.py` files import `AzureAIAgentClient` from `agent_framework.azure`, which
raises `ImportError` under GA packages. The `agent_framework.azure` namespace still exists
in GA but now contains only Azure Functions classes (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — not Foundry agents.

### Confirmed error (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Files affected

| File | Line |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Incompatible with GA `agent-framework-core`

**Status:** Open | **Severity:** 🔴 High | **Type:** Breaking (blocked on upstream)

### Description

`azure-ai-agentserver-agentframework==1.0.0b17` (latest) hard-pins
`agent-framework-core<=1.0.0rc3`. Installing it alongside `agent-framework-core==1.0.0` (GA)
forces pip to **downgrade** `agent-framework-core` back to `rc3`, which then breaks
`agent-framework-foundry==1.0.0` and `agent-framework-openai==1.0.0`.

The `from azure.ai.agentserver.agentframework import from_agent_framework` call used by all
agents to bind the HTTP server is therefore also blocked.

### Confirmed dependency conflict (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Files affected

All three `main.py` files — both the top-level import and the in-function import in `main()`.

---

## KI-003 — `agent-dev-cli --pre` Flag No Longer Needed

**Status:** ✅ Fixed (non-breaking) | **Severity:** 🟢 Low

### Description

All `requirements.txt` files previously included `agent-dev-cli --pre` to pull the
pre-release CLI. Since GA 1.0.0 was released on 2026-04-02, the stable release of
`agent-dev-cli` is now available without the `--pre` flag.

**Fix applied:** The `--pre` flag has been removed from all three `requirements.txt` files.

---

## KI-004 — Dockerfiles Use `python:3.14-slim` (Pre-release Base Image)

**Status:** Open | **Severity:** 🟡 Low

### Description

All `Dockerfile`s use `FROM python:3.14-slim` which tracks a pre-release Python build.
For production deployments this should be pinned to a stable release (e.g., `python:3.12-slim`).

### Files affected

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## References

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->