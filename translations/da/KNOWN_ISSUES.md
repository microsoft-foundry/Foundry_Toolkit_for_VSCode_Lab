# Kendte problemer

Dette dokument følger kendte problemer med den nuværende tilstand af repositoryet.

> Sidst opdateret: 2026-04-15. Testet mod Python 3.13 / Windows i `.venv_ga_test`.

---

## Aktuelle pakke-versioner (alle tre agenter)

| Pakke | Aktuel version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fikset — se KI-003)* |

---

## KI-001 — GA 1.0.0 Opgradering Blokeret: `agent-framework-azure-ai` Fjernet

**Status:** Åben | **Alvor:** 🔴 Høj | **Type:** Breaking

### Beskrivelse

`agent-framework-azure-ai` pakken (fastlåst ved `1.0.0rc3`) blev **fjernet/forældet**
i GA udgivelsen (1.0.0, udgivet 2026-04-02). Den er erstattet af:

- `agent-framework-foundry==1.0.0` — Foundry-hostet agentmønster
- `agent-framework-openai==1.0.0` — OpenAI-baseret agentmønster

Alle tre `main.py` filer importerer `AzureAIAgentClient` fra `agent_framework.azure`, hvilket
kaster `ImportError` under GA pakker. `agent_framework.azure` navneområdet findes stadig
i GA men indeholder nu kun Azure Functions klasser (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ikke Foundry agenter.

### Bekræftet fejl (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Påvirkede filer

| Fil | Linje |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Inkompatibel med GA `agent-framework-core`

**Status:** Åben | **Alvor:** 🔴 Høj | **Type:** Breaking (blokeret af upstream)

### Beskrivelse

`azure-ai-agentserver-agentframework==1.0.0b17` (sidste) fastlåser
`agent-framework-core<=1.0.0rc3`. At installere den sammen med `agent-framework-core==1.0.0` (GA)
tvinger pip til at **nedgradere** `agent-framework-core` tilbage til `rc3`, hvilket så bryder
`agent-framework-foundry==1.0.0` og `agent-framework-openai==1.0.0`.

Kaldet `from azure.ai.agentserver.agentframework import from_agent_framework` brugt af alle
agenter til at binde HTTP-serveren er derfor også blokeret.

### Bekræftet afhængighedskonflikt (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Påvirkede filer

Alle tre `main.py` filer — både importen i toppen og den inde i funktionen `main()`.

---

## KI-003 — `agent-dev-cli --pre` Flag Ikke Længere Nødvendigt

**Status:** ✅ Fikset (ikke-breaking) | **Alvor:** 🟢 Lav

### Beskrivelse

Alle `requirements.txt` filer inkluderede tidligere `agent-dev-cli --pre` for at hente
pre-release CLI'en. Siden GA 1.0.0 blev udgivet den 2026-04-02, er den stabile udgivelse af
`agent-dev-cli` nu tilgængelig uden `--pre` flagget.

**Fix anvendt:** `--pre` flagget er fjernet fra alle tre `requirements.txt` filer.

---

## KI-004 — Dockerfiles Bruger `python:3.14-slim` (Pre-release Base Image)

**Status:** Åben | **Alvor:** 🟡 Lav

### Beskrivelse

Alle `Dockerfile`s bruger `FROM python:3.14-slim` som følger en pre-release Python build.
Til produktionsudrulninger bør dette fastlåses til en stabil udgivelse (f.eks. `python:3.12-slim`).

### Påvirkede filer

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referencer

- [agent-framework-core på PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry på PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:  
Dette dokument er oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det oprindelige dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->