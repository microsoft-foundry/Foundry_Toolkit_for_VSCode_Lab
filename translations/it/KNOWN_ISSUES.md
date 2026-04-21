# Problemi Noti

Questo documento traccia i problemi noti con lo stato corrente del repository.

> Ultimo aggiornamento: 2026-04-15. Testato con Python 3.13 / Windows in `.venv_ga_test`.

---

## Blocchi correnti del pacchetto (tutti e tre gli agenti)

| Pacchetto | Versione attuale |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fissato — vedi KI-003)* |

---

## KI-001 — Aggiornamento GA 1.0.0 Bloccato: `agent-framework-azure-ai` Rimosso

**Stato:** Aperto | **Gravità:** 🔴 Alta | **Tipo:** Breaking

### Descrizione

Il pacchetto `agent-framework-azure-ai` (bloccato a `1.0.0rc3`) è stato **rimosso/deprezzato**  
nella release GA (1.0.0, rilasciata 2026-04-02). È sostituito da:

- `agent-framework-foundry==1.0.0` — pattern di agente ospitato da Foundry  
- `agent-framework-openai==1.0.0` — pattern di agente supportato da OpenAI

Tutti e tre i file `main.py` importano `AzureAIAgentClient` da `agent_framework.azure`, che  
solleva `ImportError` con i pacchetti GA. Il namespace `agent_framework.azure` esiste ancora  
in GA ma ora contiene solo classi di Azure Functions (`DurableAIAgent`,  
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — non agenti Foundry.

### Errore confermato (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### File interessati

| File | Riga |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Incompatibile con GA `agent-framework-core`

**Stato:** Aperto | **Gravità:** 🔴 Alta | **Tipo:** Breaking (bloccato a monte)

### Descrizione

`azure-ai-agentserver-agentframework==1.0.0b17` (ultima versione) blocca rigidamente  
`agent-framework-core<=1.0.0rc3`. Installarlo insieme a `agent-framework-core==1.0.0` (GA)  
costringe pip a **downgradare** `agent-framework-core` di nuovo a `rc3`, cosa che rompe  
`agent-framework-foundry==1.0.0` e `agent-framework-openai==1.0.0`.

Quindi la chiamata `from azure.ai.agentserver.agentframework import from_agent_framework` usata da tutti  
gli agenti per collegare il server HTTP è anch’essa bloccata.

### Conflitto di dipendenze confermato (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### File interessati

Tutti e tre i file `main.py` — sia l’import principale a livello superiore che l’import all’interno della funzione `main()`.

---

## KI-003 — Flag `agent-dev-cli --pre` Non Più Necessario

**Stato:** ✅ Risolto (non breaking) | **Gravità:** 🟢 Bassa

### Descrizione

Tutti i file `requirements.txt` includevano precedentemente `agent-dev-cli --pre` per scaricare la  
CLI in pre-release. Dal rilascio GA 1.0.0 del 2026-04-02, la versione stabile di  
`agent-dev-cli` è ora disponibile senza il flag `--pre`.

**Fix applicato:** Il flag `--pre` è stato rimosso da tutti e tre i file `requirements.txt`.

---

## KI-004 — Dockerfile Usano `python:3.14-slim` (Immagine base Pre-release)

**Stato:** Aperto | **Gravità:** 🟡 Bassa

### Descrizione

Tutti i `Dockerfile` usano `FROM python:3.14-slim` che segue una build Python in pre-release.  
Per le distribuzioni in produzione dovrebbe essere bloccato a una versione stabile (es. `python:3.12-slim`).

### File interessati

- `ExecutiveAgent/Dockerfile`  
- `workshop/lab01-single-agent/agent/Dockerfile`  
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`  

---

## Riferimenti

- [agent-framework-core su PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry su PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Pur impegnandoci per l’accuratezza, si prega di considerare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua madre deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un umano. Non siamo responsabili per eventuali incomprensioni o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->