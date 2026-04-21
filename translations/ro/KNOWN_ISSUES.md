# Probleme cunoscute

Acest document urmărește problemele cunoscute în stadiul actual al depozitului.

> Ultima actualizare: 2026-04-15. Testat cu Python 3.13 / Windows în `.venv_ga_test`.

---

## Blocări curente ale pachetelor (toți cei trei agenți)

| Pachet | Versiune curentă |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fixat — vezi KI-003)* |

---

## KI-001 — Blocarea Upgrade-ului GA 1.0.0: `agent-framework-azure-ai` Eliminat

**Status:** Deschis | **Gravitate:** 🔴 Ridicată | **Tip:** Breaking

### Descriere

Pachetul `agent-framework-azure-ai` (fixat la `1.0.0rc3`) a fost **eliminat/depreciat**
în lansarea GA (1.0.0, lansat 2026-04-02). Este înlocuit de:

- `agent-framework-foundry==1.0.0` — modelul agent găzduit în Foundry
- `agent-framework-openai==1.0.0` — modelul agent susținut de OpenAI

Toate cele trei fișiere `main.py` importă `AzureAIAgentClient` din `agent_framework.azure`, ceea ce
a generează `ImportError` în cadrul pachetelor GA. Numele de spațiu `agent_framework.azure` există încă în GA, dar conține acum doar clase pentru Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — nu agenți Foundry.

### Eroare confirmată (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Fișiere afectate

| Fișier | Linie |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Incompatibil cu GA `agent-framework-core`

**Status:** Deschis | **Gravitate:** 🔴 Ridicată | **Tip:** Breaking (blocată de la upstream)

### Descriere

`azure-ai-agentserver-agentframework==1.0.0b17` (ultima versiune) fixează strict
`agent-framework-core<=1.0.0rc3`. Instalarea acestuia împreună cu `agent-framework-core==1.0.0` (GA)
forțează pip să **retrogradeze** `agent-framework-core` la `rc3`, ceea ce apoi strică
`agent-framework-foundry==1.0.0` și `agent-framework-openai==1.0.0`.

Apelul `from azure.ai.agentserver.agentframework import from_agent_framework` folosit de toți
agenții pentru a lega serverul HTTP este și el blocat.

### Conflict de dependență confirmat (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Fișiere afectate

Toate cele trei fișiere `main.py` — atât importul de la nivel superior, cât și importul din funcția `main()`.

---

## KI-003 — Flag-ul `agent-dev-cli --pre` Nu Mai Este Necesitar

**Status:** ✅ Remediat (fără impact de rupere) | **Gravitate:** 🟢 Scăzută

### Descriere

Toate fișierele `requirements.txt` includeau anterior `agent-dev-cli --pre` pentru a trage
CLI-ul în versiune pre-lansare. Din moment ce GA 1.0.0 a fost lansat pe 2026-04-02, versiunea stabilă a
`agent-dev-cli` este acum disponibilă fără flag-ul `--pre`.

**Remediere aplicată:** Flag-ul `--pre` a fost eliminat din toate cele trei fișiere `requirements.txt`.

---

## KI-004 — Dockerfile-urile Utilizează `python:3.14-slim` (Imagine Bază Pre-lansare)

**Status:** Deschis | **Gravitate:** 🟡 Scăzută

### Descriere

Toate `Dockerfile`-urile folosesc `FROM python:3.14-slim`, care urmărește o construcție Python pre-lansare.
Pentru implementări de producție acesta ar trebui blocat pe o versiune stabilă (de exemplu, `python:3.12-slim`).

### Fișiere afectate

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referințe

- [agent-framework-core pe PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry pe PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un uman. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite rezultate din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->