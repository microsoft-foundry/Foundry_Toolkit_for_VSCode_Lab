# Bekende Problemen

Dit document houdt bekende problemen bij met de huidige staat van de repository.

> Laatst bijgewerkt: 2026-04-15. Getest met Python 3.13 / Windows in `.venv_ga_test`.

---

## Huidige Package-versies (alle drie agents)

| Package | Huidige Versie |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(gerepareerd — zie KI-003)* |

---

## KI-001 — GA 1.0.0 Upgrade Geblokkeerd: `agent-framework-azure-ai` Verwijderd

**Status:** Open | **Ernst:** 🔴 Hoog | **Type:** Brekend

### Beschrijving

Het pakket `agent-framework-azure-ai` (gevangen op `1.0.0rc3`) is **verwijderd/verouderd**
in de GA-release (1.0.0, uitgebracht 2026-04-02). Het is vervangen door:

- `agent-framework-foundry==1.0.0` — Foundry-gehost patroon voor agenten
- `agent-framework-openai==1.0.0` — OpenAI-ondersteund patroon voor agenten

Alledrie de `main.py` bestanden importeren `AzureAIAgentClient` uit `agent_framework.azure`, wat
`ImportError` veroorzaakt onder GA-pakketten. De namespace `agent_framework.azure` bestaat nog steeds
in GA maar bevat nu alleen Azure Functions-klassen (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — geen Foundry-agenten.

### Bevestigde fout (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Bestanden getroffen

| Bestand | Regel |
|---------|-------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Niet Compatibel met GA `agent-framework-core`

**Status:** Open | **Ernst:** 🔴 Hoog | **Type:** Brekend (geblokkeerd door upstream)

### Beschrijving

`azure-ai-agentserver-agentframework==1.0.0b17` (laatste versie) fixeert
`agent-framework-core<=1.0.0rc3`. Installatie samen met `agent-framework-core==1.0.0` (GA)
dwingt pip om `agent-framework-core` terug te **downgraden** naar `rc3`, wat dan `agent-framework-foundry==1.0.0` en `agent-framework-openai==1.0.0` breekt.

De `from azure.ai.agentserver.agentframework import from_agent_framework` oproep die door alle
agenten wordt gebruikt om de HTTP-server te binden, is daardoor ook geblokkeerd.

### Bevestigd afhankelijkheidsconflict (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Bestanden getroffen

Alle drie de `main.py` bestanden — zowel de top-level import als de import binnen de functie in `main()`.

---

## KI-003 — `agent-dev-cli --pre` Vlag Niet Meer Nodig

**Status:** ✅ Gerepareerd (niet-brekend) | **Ernst:** 🟢 Laag

### Beschrijving

Alle `requirements.txt` bestanden bevatten voorheen `agent-dev-cli --pre` om de
pre-release CLI te installeren. Sinds GA 1.0.0 uitgebracht op 2026-04-02, is de stabiele release van
`agent-dev-cli` nu beschikbaar zonder de `--pre` vlag.

**Opgelost:** De `--pre` vlag is verwijderd uit alle drie `requirements.txt` bestanden.

---

## KI-004 — Dockerfiles Gebruiken `python:3.14-slim` (Pre-release Basisimage)

**Status:** Open | **Ernst:** 🟡 Laag

### Beschrijving

Alle `Dockerfile`s gebruiken `FROM python:3.14-slim` wat een pre-release Python-build volgt.
Voor productie-implementaties zou dit moeten worden vastgezet op een stabiele release (bijv. `python:3.12-slim`).

### Bestanden getroffen

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referenties

- [agent-framework-core op PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry op PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u zich ervan bewust te zijn dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->