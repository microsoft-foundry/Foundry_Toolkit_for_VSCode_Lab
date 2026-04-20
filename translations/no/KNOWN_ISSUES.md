# Kjente Problemer

Dette dokumentet sporer kjente problemer med den nåværende tilstanden i depotet.

> Sist oppdatert: 2026-04-15. Testet mot Python 3.13 / Windows i `.venv_ga_test`.

---

## Nåværende Pakkeversjoner (alle tre agenter)

| Pakke | Nåværende Versjon |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fikset — se KI-003)* |

---

## KI-001 — GA 1.0.0 Oppgradering Blokkert: `agent-framework-azure-ai` Fjernet

**Status:** Åpen | **Alvorlighetsgrad:** 🔴 Høy | **Type:** Brytende

### Beskrivelse

`agent-framework-azure-ai` pakken (fastsatt til `1.0.0rc3`) ble **fjernet/utgått**
i GA-utgivelsen (1.0.0, utgitt 2026-04-02). Den er erstattet med:

- `agent-framework-foundry==1.0.0` — Foundry-hostet agentmønster
- `agent-framework-openai==1.0.0` — OpenAI-basert agentmønster

Alle tre `main.py` filene importerer `AzureAIAgentClient` fra `agent_framework.azure`, som
gir `ImportError` under GA-pakker. `agent_framework.azure`-navneområdet eksisterer fortsatt
i GA, men inneholder nå kun Azure Functions-klasser (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ikke Foundry-agenter.

### Bekreftet feil (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Berørte filer

| Fil | Linje |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Uforenlig med GA `agent-framework-core`

**Status:** Åpen | **Alvorlighetsgrad:** 🔴 Høy | **Type:** Brytende (blokkert av oppstrøms)

### Beskrivelse

`azure-ai-agentserver-agentframework==1.0.0b17` (siste) har streng versjonsbinding til
`agent-framework-core<=1.0.0rc3`. Installering sammen med `agent-framework-core==1.0.0` (GA)
tvinger pip til å **nedgradere** `agent-framework-core` tilbake til `rc3`, hvilket bryter
`agent-framework-foundry==1.0.0` og `agent-framework-openai==1.0.0`.

`from azure.ai.agentserver.agentframework import from_agent_framework`-kallet som alle
agenter bruker for å binde HTTP-serveren er derfor også blokkert.

### Bekreftet avhengighetskonflikt (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Berørte filer

Alle tre `main.py` filer — både toppnivå import og import inne i funksjonen `main()`.

---

## KI-003 — `agent-dev-cli --pre` Flagget Ikke Lenger Nødvendig

**Status:** ✅ Fikset (ikke-brytende) | **Alvorlighetsgrad:** 🟢 Lav

### Beskrivelse

Alle `requirements.txt` filer inkluderte tidligere `agent-dev-cli --pre` for å hente
pre-release CLI. Siden GA 1.0.0 ble utgitt 2026-04-02, er den stabile utgivelsen av
`agent-dev-cli` nå tilgjengelig uten `--pre` flagget.

**Fiks utført:** `--pre` flagget er fjernet fra alle tre `requirements.txt` filer.

---

## KI-004 — Dockerfiler Bruker `python:3.14-slim` (Pre-release Base Image)

**Status:** Åpen | **Alvorlighetsgrad:** 🟡 Lav

### Beskrivelse

Alle `Dockerfile` bruker `FROM python:3.14-slim` som følger en pre-release Python-versjon.
For produksjonsdistribusjoner bør dette låses til en stabil utgivelse (f.eks. `python:3.12-slim`).

### Berørte filer

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referanser

- [agent-framework-core på PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry på PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vennligst vær oppmerksom på at automatiserte oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på sitt opprinnelige språk skal anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for noen misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->