# Kilalang Mga Isyu

Sinusubaybayan ng dokumentong ito ang mga kilalang isyu sa kasalukuyang estado ng repositoryo.

> Huling inayos: 2026-04-15. Sinubukan laban sa Python 3.13 / Windows sa `.venv_ga_test`.

---

## Kasalukuyang Package Pins (lahat ng tatlong ahente)

| Package | Kasalukuyang Bersyon |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(naayos — tingnan ang KI-003)* |

---

## KI-001 — NAHARANGAN ang GA 1.0.0 Upgrade: Tinanggal ang `agent-framework-azure-ai`

**Status:** Bukas | **Kalubhaan:** 🔴 Mataas | **Uri:** Nakakapinsala

### Paglalarawan

Ang package na `agent-framework-azure-ai` (na naka-pin sa `1.0.0rc3`) ay **tinanggal/iniretiro**
sa GA release (1.0.0, inilabas 2026-04-02). Pinalitan ito ng:

- `agent-framework-foundry==1.0.0` — Foundry-hosted na pattern ng ahente
- `agent-framework-openai==1.0.0` — OpenAI-lamang na pattern ng ahente

Ang lahat ng tatlong `main.py` files ay nag-i-import ng `AzureAIAgentClient` mula sa `agent_framework.azure`, na
nagbubunga ng `ImportError` sa ilalim ng GA packages. Ang namespace na `agent_framework.azure` ay nananatili sa GA ngunit ngayon ay naglalaman lamang ng mga klase para sa Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — hindi mga Foundry agents.

### Nakumpirmang error (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Mga apektadong file

| File | Linya |
|------|-------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — Hindi Tugma ang `azure-ai-agentserver` sa GA `agent-framework-core`

**Status:** Bukas | **Kalubhaan:** 🔴 Mataas | **Uri:** Nakakapinsala (nakaharang sa upstream)

### Paglalarawan

Ang `azure-ai-agentserver-agentframework==1.0.0b17` (pinakabago) ay mahigpit na nagpi-pin
ng `agent-framework-core<=1.0.0rc3`. Ang pag-install nito kasabay ng `agent-framework-core==1.0.0` (GA)
ay nagpipilit sa pip na **ibaba ang bersyon** ng `agent-framework-core` pabalik sa `rc3`, na dahilan ng pagkasira ng
`agent-framework-foundry==1.0.0` at `agent-framework-openai==1.0.0`.

Ang tawag na `from azure.ai.agentserver.agentframework import from_agent_framework` na ginagamit ng lahat
ng ahente para i-bind ang HTTP server ay nakaharang din.

### Nakumpirmang dependency conflict (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Mga apektadong file

Lahat ng tatlong `main.py` files — kapwa ang top-level na import at ang in-function na import sa `main()`.

---

## KI-003 — Hindi Na Kailangan ang `agent-dev-cli --pre` Flag

**Status:** ✅ Naayos (hindi nakakasira) | **Kalubhaan:** 🟢 Mababa

### Paglalarawan

Lahat ng `requirements.txt` files ay dati nang mayroong `agent-dev-cli --pre` para kunin ang
pre-release na CLI. Simula nang inilabas ang GA 1.0.0 noong 2026-04-02, ang stable release ng
`agent-dev-cli` ay available na nang walang `--pre` flag.

**Inayos:** Tinanggal na ang `--pre` flag sa lahat ng tatlong `requirements.txt` files.

---

## KI-004 — Gumagamit ang Dockerfiles ng `python:3.14-slim` (Pre-release Base Image)

**Status:** Bukas | **Kalubhaan:** 🟡 Mababa

### Paglalarawan

Lahat ng `Dockerfile`s ay gumagamit ng `FROM python:3.14-slim` na sumusubaybay sa pre-release na Python build.
Para sa produksyon na deployment, ito ay dapat naka-pin sa stable release (halimbawa, `python:3.12-slim`).

### Mga apektadong file

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Mga Sanggunian

- [agent-framework-core sa PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry sa PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kaming maging tumpak, mangyaring tandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga error o pagkakamali. Ang orihinal na dokumento sa kanyang likas na wika ang dapat ituring na opisyal na sanggunian. Para sa mga mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasaling pang-tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->