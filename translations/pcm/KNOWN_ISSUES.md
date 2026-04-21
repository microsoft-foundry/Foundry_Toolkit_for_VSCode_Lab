# Known Issues

Dis document dey track known palava wey dey for di current repository state.

> Last updated: 2026-04-15. Tested against Python 3.13 / Windows for `.venv_ga_test`.

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

Di `agent-framework-azure-ai` package (wey dey pinned at `1.0.0rc3`) **dem remove/stop e**
for di GA release (1.0.0, wey dem release for 2026-04-02). E don change to:

- `agent-framework-foundry==1.0.0` — Foundry-hosted agent pattern
- `agent-framework-openai==1.0.0` — OpenAI-backed agent pattern

All di three `main.py` files dey import `AzureAIAgentClient` from `agent_framework.azure`, wey
go cause `ImportError` under GA packages. Di `agent_framework.azure` namespace still dey
inside GA but e now get only Azure Functions classes (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — no be Foundry agents again.

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

`azure-ai-agentserver-agentframework==1.0.0b17` (wey be di latest) hard-pins
`agent-framework-core<=1.0.0rc3`. If you try install am along with `agent-framework-core==1.0.0` (wey be GA)
e go force pip to **downgrade** `agent-framework-core` go back to `rc3`, and this go break
`agent-framework-foundry==1.0.0` and `agent-framework-openai==1.0.0`.

Di `from azure.ai.agentserver.agentframework import from_agent_framework` call wey all
di agents dey use to bind di HTTP server sef dey blocked.

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

All di three `main.py` files — both di top-level import and di in-function import inside `main()`.

---

## KI-003 — `agent-dev-cli --pre` Flag No Longer Needed

**Status:** ✅ Fixed (non-breaking) | **Severity:** 🟢 Low

### Description

All di `requirements.txt` files before dey inside `agent-dev-cli --pre` to pull di
pre-release CLI. Since GA 1.0.0 release on 2026-04-02, di stable release of
`agent-dev-cli` don available without di `--pre` flag.

**Fix wey dem apply:** Dem remove di `--pre` flag from all di three `requirements.txt` files.

---

## KI-004 — Dockerfiles Use `python:3.14-slim` (Pre-release Base Image)

**Status:** Open | **Severity:** 🟡 Low

### Description

All di `Dockerfile`s dey use `FROM python:3.14-slim` wey dey track pre-release Python build.
For production deployment, e better make e dey pinned to stable release (like `python:3.12-slim`).

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
Dis dokument don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg no forget say automated translations fit get errors or mistakes. Di original dokument for dia own language na di correct and trusted source. For important tin dem, make person wey sabi human translation do am. We no go responsible for any wrong understanding or confusion wey fit come from dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->