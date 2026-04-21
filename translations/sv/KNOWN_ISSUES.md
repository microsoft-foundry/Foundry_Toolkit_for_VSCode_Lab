# Kända problem

Detta dokument spårar kända problem med det aktuella tillståndet i förvaret.

> Senast uppdaterat: 2026-04-15. Testad mot Python 3.13 / Windows i `.venv_ga_test`.

---

## Nuvarande paketversioner (alla tre agenter)

| Paket | Nuvarande version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fixad — se KI-003)* |

---

## KI-001 — GA 1.0.0 Uppgradering blockerad: `agent-framework-azure-ai` borttagen

**Status:** Öppen | **Allvar:** 🔴 Hög | **Typ:** Brytande förändring

### Beskrivning

`agent-framework-azure-ai` paketet (fastlåst vid `1.0.0rc3`) har **tagits bort/avvecklats**
i GA-utgåvan (1.0.0, släppt 2026-04-02). Det ersätts av:

- `agent-framework-foundry==1.0.0` — Foundry-hostad agentmönster
- `agent-framework-openai==1.0.0` — OpenAI-baserat agentmönster

Alla tre `main.py` filer importerar `AzureAIAgentClient` från `agent_framework.azure`, vilket
orsakar `ImportError` under GA-paketen. `agent_framework.azure` namnrymden finns fortfarande
i GA men innehåller nu endast Azure Functions-klasser (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — inte Foundry-agenter.

### Bekräftat fel (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Påverkade filer

| Fil | Rad |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` inkompatibelt med GA `agent-framework-core`

**Status:** Öppen | **Allvar:** 🔴 Hög | **Typ:** Brytande (blockerad av upstream)

### Beskrivning

`azure-ai-agentserver-agentframework==1.0.0b17` (senaste) fastlåser  
`agent-framework-core<=1.0.0rc3`. Att installera den tillsammans med `agent-framework-core==1.0.0` (GA)  
tvingar pip att **nedgradera** `agent-framework-core` tillbaka till `rc3`, vilket sedan bryter  
`agent-framework-foundry==1.0.0` och `agent-framework-openai==1.0.0`.

Anropet `from azure.ai.agentserver.agentframework import from_agent_framework` som alla  
agenter använder för att binda HTTP-servern är därför också blockerat.

### Bekräftad beroendekonflikt (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Påverkade filer

Alla tre `main.py` filer — både toppnivåimporten och infunktionimporten i `main()`.

---

## KI-003 — `agent-dev-cli --pre` flagga behövs inte längre

**Status:** ✅ Fixad (icke-brytande) | **Allvar:** 🟢 Låg

### Beskrivning

Alla `requirements.txt`-filer innehöll tidigare `agent-dev-cli --pre` för att hämta  
pre-release CLI. Sedan GA 1.0.0 släpptes den 2026-04-02 är den stabila versionen av  
`agent-dev-cli` nu tillgänglig utan `--pre` flaggan.

**Åtgärd utförd:** `--pre` flaggan har tagits bort från alla tre `requirements.txt`-filer.

---

## KI-004 — Dockerfiler använder `python:3.14-slim` (pre-release basbild)

**Status:** Öppen | **Allvar:** 🟡 Låg

### Beskrivning

Alla `Dockerfile`s använder `FROM python:3.14-slim` som spårar en pre-release Python-build.  
För produktionsdistributioner bör detta låsas till en stabil release (t.ex. `python:3.12-slim`).

### Påverkade filer

- `ExecutiveAgent/Dockerfile`  
- `workshop/lab01-single-agent/agent/Dockerfile`  
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referenser

- [agent-framework-core på PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry på PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, vänligen observera att automatiska översättningar kan innehålla fel eller felaktigheter. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår från användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->