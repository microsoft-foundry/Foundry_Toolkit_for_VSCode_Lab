# Známe problémy

Tento dokument sleduje známe problémy s aktuálnym stavom repozitára.

> Posledná aktualizácia: 2026-04-15. Testované na Python 3.13 / Windows v `.venv_ga_test`.

---

## Aktuálne pevné verzie balíkov (všetci traja agenti)

| Balík | Aktuálna verzia |
|-------|-----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(opravené — pozri KI-003)* |

---

## KI-001 — GA 1.0.0 Upgrade Blokovaný: `agent-framework-azure-ai` Odstránený

**Stav:** Otvorené | **Závažnosť:** 🔴 Vysoká | **Typ:** Zlomový

### Popis

Balík `agent-framework-azure-ai` (pevne stanovený na `1.0.0rc3`) bol **odstránený/ustúpený**
v GA verzii (1.0.0, vydané 2026-04-02). Nahrádza ho:

- `agent-framework-foundry==1.0.0` — agentný vzor hostovaný cez Foundry
- `agent-framework-openai==1.0.0` — agentný vzor podporovaný OpenAI

Všetky tri súbory `main.py` importujú `AzureAIAgentClient` z `agent_framework.azure`, čo
vyvoláva `ImportError` pod GA balíkmi. Menno-priestor `agent_framework.azure` stále existuje
v GA, ale obsahuje teraz iba triedy Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — nie Foundry agentov.

### Potvrdená chyba (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Ovlplyvnené súbory

| Súbor | Riadok |
|-------|--------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Ne kompatibilný s GA `agent-framework-core`

**Stav:** Otvorené | **Závažnosť:** 🔴 Vysoká | **Typ:** Zlomový (blokované na strane upstream)

### Popis

`azure-ai-agentserver-agentframework==1.0.0b17` (najnovší) pevne stanovil
`agent-framework-core<=1.0.0rc3`. Inštalácia spolu s `agent-framework-core==1.0.0` (GA)
nutí pip **degradovať** `agent-framework-core` späť na `rc3`, čo následne rozbíja
`agent-framework-foundry==1.0.0` a `agent-framework-openai==1.0.0`.

Volanie `from azure.ai.agentserver.agentframework import from_agent_framework` používané všetkými
agentmi na naviazanie HTTP servera je preto taktiež zablokované.

### Potvrdený konflikt závislostí (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Ovplyvnené súbory

Všetky tri `main.py` súbory — import na najvyššej úrovni aj import vo funkcii `main()`.

---

## KI-003 — `agent-dev-cli --pre` Už Nie je Potrebný

**Stav:** ✅ Opravené (nezlomové) | **Závažnosť:** 🟢 Nízka

### Popis

Všetky `requirements.txt` súbory predtým obsahovali `agent-dev-cli --pre` na získanie
predvydaného CLI. Od vydania GA 1.0.0 dňa 2026-04-02 je stabilné vydanie
`agent-dev-cli` teraz dostupné bez prepínača `--pre`.

**Oprava:** Prepínač `--pre` bol odstránený zo všetkých troch `requirements.txt` súborov.

---

## KI-004 — Dockerfiles Používajú `python:3.14-slim` (Predvydanie Bazového Obrazu)

**Stav:** Otvorené | **Závažnosť:** 🟡 Nízka

### Popis

Všetky `Dockerfile` používajú `FROM python:3.14-slim`, ktorá sleduje predvydanú verziu Pythonu.
Pre produkčné nasadenia by mala byť zafixovaná na stabilnú verziu (napr. `python:3.12-slim`).

### Ovplyvnené súbory

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referencie

- [agent-framework-core na PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry na PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zrieknutie sa zodpovednosti**:
Tento dokument bol preložený pomocou služby automatického prekladu AI [Co-op Translator](https://github.com/Azure/co-op-translator). Aj keď sa snažíme o presnosť, majte prosím na pamäti, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Originálny dokument v jeho pôvodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za akékoľvek nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->