# Known Issues

This document tracks known issues with the current repository state.

> Last updated: 2026-05-18. Tested against Python 3.13 / Windows in `.venv_ga_test`. Foundry Toolkit v1.2.1.

---

## Current Package Pins (all three agents)

| Package | Current Version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fixed - see KI-003)* |

---

## KI-001 - GA 1.0.0 Upgrade Blocked: `agent-framework-azure-ai` Removed

**Status:** Open | **Severity:** 🔴 High | **Type:** Breaking

### Description

The `agent-framework-azure-ai` package (pinned at `1.0.0rc3`) was **removed/deprecated**
in the GA release (1.0.x; latest GA 1.0.1, released 2026-04-10). It is replaced by:

- `agent-framework-foundry==1.0.1` - Foundry-hosted agent pattern
- `agent-framework-openai==1.0.1` - OpenAI-backed agent pattern

All three `main.py` files import `AzureAIAgentClient` from `agent_framework.azure`, which
raises `ImportError` under GA packages. The `agent_framework.azure` namespace still exists
in GA but now contains only Azure Functions classes (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) - not Foundry agents.

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

## KI-002 - `azure-ai-agentserver` Incompatible with GA `agent-framework-core`

**Status:** Open (fix pending SDK release) | **Severity:** 🔴 High | **Type:** Breaking (blocked on upstream)

### Description

`azure-ai-agentserver-agentframework==1.0.0b17` (latest) hard-pins
`agent-framework-core<=1.0.0rc3`. Installing it alongside `agent-framework-core==1.0.1` (latest GA)
forces pip to **downgrade** `agent-framework-core` back to `rc3`, which then breaks
`agent-framework-foundry==1.0.1` and `agent-framework-openai==1.0.1`.

The `from azure.ai.agentserver.agentframework import from_agent_framework` call used by all
agents to bind the HTTP server is therefore also blocked.

### Upstream tracking

| Repo | Issue | Status |
|------|-------|--------|
| microsoft/agent-framework | [#5273](https://github.com/microsoft/agent-framework/issues/5273) | ✅ Closed 2026-04-21 - fix submitted to azure-sdk-for-python |
| Azure/azure-sdk-for-python | [#46324](https://github.com/Azure/azure-sdk-for-python/issues/46324) | 🔴 Open - new `azure-ai-agentserver-agentframework` release pending |

Workshop stays pinned at rc3 until azure-sdk-for-python#46324 ships.

### Confirmed dependency conflict (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.1 requires agent-framework-core<2,>=1.0.1,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.1 requires agent-framework-core<2,>=1.0.1,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Files affected

All three `main.py` files - both the top-level import and the in-function import in `main()`.

---

## KI-003 - `agent-dev-cli --pre` Flag No Longer Needed

**Status:** ✅ Fixed (non-breaking) | **Severity:** 🟢 Low

### Description

All `requirements.txt` files previously included `agent-dev-cli --pre` to pull the
pre-release CLI. Since GA 1.0.0 was released on 2026-04-02, the stable release of
`agent-dev-cli` is now available without the `--pre` flag.

**Fix applied:** The `--pre` flag has been removed from all three `requirements.txt` files.

---

## KI-004 - Dockerfiles Use `python:3.14-slim` (Pre-release Base Image)

**Status:** Open | **Severity:** 🟡 Low

### Description

All `Dockerfile`s use `FROM python:3.14-slim` which tracks a pre-release Python build.
For production deployments this should be pinned to a stable release (e.g., `python:3.12-slim`).

### Files affected

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## KI-005 - Teams/M365 Publish Succeeds but Agent Unreachable (BotId/ClientId Mismatch)

**Status:** Open | **Severity:** 🔴 High | **Type:** Integration bug | **Ref:** [vscode-ai-toolkit#381](https://github.com/microsoft/vscode-ai-toolkit/issues/381)

### Description

Publishing a Hosted Agent to Teams/M365 Copilot via Foundry Toolkit completes successfully but the agent is **not reachable** on those channel surfaces.

Root cause: **Publish** (registers bot channel artifacts) and **Deploy** (starts live hosted runtime) are two separate operations. Without Deploy, no running backend exists behind the endpoint.

Error observed when Bot Service attempts to route traffic:

```
Failed to publish agent BotId '<id>' does not match the application's default instance identity ClientId '<id>'.
[Status: 400, Code: UserError]
```

Azure Bot Service sends Bot Framework JWTs (`iss=https://api.botframework.com`). The current Foundry gateway auth path does not fully accept this token shape in this configuration.

**Deploy blocker:** Deploy Hosted Agent requires a local Docker build. No cloud-side build fallback is currently offered.

### Workaround

Test using the **web chat** channel in Azure Bot Service - this path works correctly. Teams/M365 channel integration is blocked until upstream auth and UX issues are resolved.

---

## KI-006 - No Multi-Agent Wizard Template in AITK v1.2.1

**Status:** Open | **Severity:** 🟡 Medium | **Type:** Feature gap

### Description

The AITK wizard (Foundry Toolkit v1.2.1) provides the following templates under the **Response API** path:

- Echo (Streaming)
- Multi-Turn Chat
- Note Taking
- **Basic - Agent Framework** ← used in Lab 01

There is no **Multi-Agent Workflow** template. Lab 02 uses the pre-built **`PersonalCareerCopilot/`** folder rather than a wizard-generated scaffold.

### Workshop impact

Learners cannot use the wizard to scaffold a new multi-agent project using MAF GA. Lab 02 proceeds using the pre-existing example code directly.

---

## References

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)
- [microsoft/agent-framework#5273](https://github.com/microsoft/agent-framework/issues/5273) - agentserver incompatibility with MAF GA (closed)
- [Azure/azure-sdk-for-python#46324](https://github.com/Azure/azure-sdk-for-python/issues/46324) - SDK fix pending (open)
- [microsoft/vscode-ai-toolkit#381](https://github.com/microsoft/vscode-ai-toolkit/issues/381) - Teams/M365 publish + auth (open)
