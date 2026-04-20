# Známé problémy

Tento dokument sleduje známé problémy se současným stavem repozitáře.

> Poslední aktualizace: 2026-04-15. Testováno s Python 3.13 / Windows v `.venv_ga_test`.

---

## Aktuální pevné verze balíčků (všechny tři agenty)

| Balíček | Aktuální verze |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(opraveno — viz KI-003)* |

---

## KI-001 — GA 1.0.0 Aktualizace zablokována: `agent-framework-azure-ai` odstraněn

**Stav:** Otevřeno | **Závažnost:** 🔴 Vysoká | **Typ:** Zlomová změna

### Popis

Balíček `agent-framework-azure-ai` (přenastavený na `1.0.0rc3`) byl **odstraněn/zaniknut**
v GA vydání (1.0.0, vydáno 2026-04-02). Je nahrazen:

- `agent-framework-foundry==1.0.0` — agentní vzor hostovaný ve Foundry
- `agent-framework-openai==1.0.0` — agentní vzor pod OpenAI

Všechny tři soubory `main.py` importují `AzureAIAgentClient` z `agent_framework.azure`, což
vyvolává `ImportError` pod GA balíčky. Jmenný prostor `agent_framework.azure` v GA stále existuje,
ale nyní obsahuje pouze třídy Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — nikoliv Foundry agenty.

### Potvrzená chyba (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Ovlivněné soubory

| Soubor | Řádek |
|--------|--------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` nekompatibilní s GA `agent-framework-core`

**Stav:** Otevřeno | **Závažnost:** 🔴 Vysoká | **Typ:** Zlomová změna (zablokováno upstream)

### Popis

`azure-ai-agentserver-agentframework==1.0.0b17` (nejnovější) pevně nastavuje
`agent-framework-core<=1.0.0rc3`. Instalace společně s `agent-framework-core==1.0.0` (GA)
nutí pip **downgradovat** `agent-framework-core` zpět na `rc3`, což následně rozbíjí
`agent-framework-foundry==1.0.0` a `agent-framework-openai==1.0.0`.

Volání `from azure.ai.agentserver.agentframework import from_agent_framework`, používané všemi
agenty k navázání HTTP serveru, je tedy také zablokováno.

### Potvrzený konflikt závislostí (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Ovlivněné soubory

Všechny tři soubory `main.py` — jak import na úrovni souboru, tak import uvnitř funkce `main()`.

---

## KI-003 — Přepínač `agent-dev-cli --pre` již není potřeba

**Stav:** ✅ Opraveno (nezlomová změna) | **Závažnost:** 🟢 Nízká

### Popis

Všechny soubory `requirements.txt` dříve obsahovaly `agent-dev-cli --pre` pro stažení
předběžné verze CLI. Od vydání GA 1.0.0 dne 2026-04-02 je stabilní verze
`agent-dev-cli` nyní dostupná bez přepínače `--pre`.

**Uplatněná oprava:** Přepínač `--pre` byl odstraněn ze všech tří souborů `requirements.txt`.

---

## KI-004 — Dockerfiles používají `python:3.14-slim` (předběžný základní obraz)

**Stav:** Otevřeno | **Závažnost:** 🟡 Nízká

### Popis

Všechny `Dockerfile` používají `FROM python:3.14-slim`, který sleduje předběžné vydání Pythonu.
Pro produkční nasazení by měl být pevně nastaven na stabilní verzi (např. `python:3.12-slim`).

### Ovlivněné soubory

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Reference

- [agent-framework-core na PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry na PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Upozornění**:  
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho rodném jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoliv nedorozumění nebo nesprávné výklady vyplývající z použití tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->