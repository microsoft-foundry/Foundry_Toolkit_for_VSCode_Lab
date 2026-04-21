# Poznati problemi

Ovaj dokument prati poznate probleme s trenutnim stanjem repozitorija.

> Zadnje ažurirano: 2026-04-15. Testirano na Python 3.13 / Windows u `.venv_ga_test`.

---

## Trenutne verzije paketa (sva tri agenta)

| Paket | Trenutna verzija |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(riješeno — vidi KI-003)* |

---

## KI-001 — Nadogradnja na GA 1.0.0 Blokirana: `agent-framework-azure-ai` Uklonjen

**Status:** Otvoreno | **Ozbiljnost:** 🔴 Visoka | **Tip:** Kritični prekid

### Opis

Paket `agent-framework-azure-ai` (fiksiran na `1.0.0rc3`) je **uklonjen/prekida podrška**
u GA izdanju (1.0.0, izdano 2026-04-02). Zamijenjen je sa:

- `agent-framework-foundry==1.0.0` — agent obrazac baziran na Foundry
- `agent-framework-openai==1.0.0` — agent obrazac baziran na OpenAI

Sva tri `main.py` datoteke uvoze `AzureAIAgentClient` iz `agent_framework.azure`, što
izaziva `ImportError` pod GA paketima. `agent_framework.azure` namespace još uvijek postoji
u GA, ali sada sadrži samo Azure Functions klase (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ne Foundry agente.

### Potvrđena greška (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Datoteke koje su pogođene

| Datoteka | Linija |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Nekompatibilan s GA `agent-framework-core`

**Status:** Otvoreno | **Ozbiljnost:** 🔴 Visoka | **Tip:** Kritični prekid (blokira se na upstreamu)

### Opis

`azure-ai-agentserver-agentframework==1.0.0b17` (najnoviji) strogo fiksira
`agent-framework-core<=1.0.0rc3`. Instaliranje zajedno s `agent-framework-core==1.0.0` (GA)
prisiljava pip da **sniži** `agent-framework-core` nazad na `rc3`, što tada kvari
`agent-framework-foundry==1.0.0` i `agent-framework-openai==1.0.0`.

Poziv `from azure.ai.agentserver.agentframework import from_agent_framework` koji koriste svi
agenti za spajanje HTTP servera je također blokiran.

### Potvrđeni konflikt ovisnosti (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Datoteke koje su pogođene

Sva tri `main.py` datoteke — i vršni import i import unutar funkcije `main()`.

---

## KI-003 — Zastavica `agent-dev-cli --pre` Više Nije Potrebna

**Status:** ✅ Riješeno (nekritično) | **Ozbiljnost:** 🟢 Niska

### Opis

Sve `requirements.txt` datoteke su prije uključivale `agent-dev-cli --pre` kako bi povukle
pre-izdanje CLI-ja. Od izdavanja GA 1.0.0 2026-04-02, stabilno izdanje
`agent-dev-cli` je sada dostupno bez `--pre` zastavice.

**Primijenjeno rješenje:** Zastavica `--pre` je uklonjena iz sve tri `requirements.txt` datoteke.

---

## KI-004 — Dockerfile koristi `python:3.14-slim` (Pre-izdanje Bazne Slike)

**Status:** Otvoreno | **Ozbiljnost:** 🟡 Niska

### Opis

Svi `Dockerfile` koriste `FROM python:3.14-slim` što prati pre-izdanje Python builda.
Za produkcijske deploymente ovo treba biti fiksirano na stabilno izdanje (npr. `python:3.12-slim`).

### Datoteke koje su pogođene

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Reference

- [agent-framework-core na PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry na PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Izjava o odricanju od odgovornosti**:
Ovaj je dokument preveden pomoću AI usluge prijevoda [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo postići točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba se smatrati autoritativnim izvorom. Za važne informacije preporučuje se profesionalni ljudski prijevod. Ne snosimo odgovornost za bilo kakva nesporazuma ili pogrešne tumačenja proizašla iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->