# Znane težave

Ta dokument sledi znanim težavam v trenutnem stanju repozitorija.

> Zadnja posodobitev: 2026-04-15. Testirano z Python 3.13 / Windows v `.venv_ga_test`.

---

## Trenutne zaklenitve paketov (vsi trije agenti)

| Paket | Trenutna različica |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(popravljeno — glej KI-003)* |

---

## KI-001 — Nadgradnja GA 1.0.0 blokirana: `agent-framework-azure-ai` odstranjen

**Status:** Odprto | **Resnost:** 🔴 Visoka | **Tip:** Prelomna

### Opis

Paket `agent-framework-azure-ai` (zaklenjen na `1.0.0rc3`) je bil **odstranjen/opuščen**
v izdaji GA (1.0.0, izdano 2026-04-02). Nadomeščen je z:

- `agent-framework-foundry==1.0.0` — agent vzorec gostovan v Foundryju
- `agent-framework-openai==1.0.0` — agent vzorec, ki ga podpira OpenAI

Vse tri datoteke `main.py` uvažajo `AzureAIAgentClient` iz `agent_framework.azure`, kar
pri GA paketih sproži `ImportError`. Ime prostora `agent_framework.azure` še obstaja
v GA, a sedaj vsebuje le Azure Functions razrede (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ne Foundry agente.

### Potrjena napaka (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Vplivane datoteke

| Datoteka | Vrstica |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` ni združljiv z GA `agent-framework-core`

**Status:** Odprto | **Resnost:** 🔴 Visoka | **Tip:** Prelomna (bloki na podlagi zunanjega vira)

### Opis

`azure-ai-agentserver-agentframework==1.0.0b17` (najnovejši) strogo zaklene
`agent-framework-core<=1.0.0rc3`. Namestitev skupaj z `agent-framework-core==1.0.0` (GA)
prisili pip, da **zaznamuje** `agent-framework-core` nazaj na `rc3`, kar nato povzroči,
da `agent-framework-foundry==1.0.0` in `agent-framework-openai==1.0.0` ne delujeta.

Klic `from azure.ai.agentserver.agentframework import from_agent_framework`, ki ga vsi
agenti uporabljajo za povezavo HTTP strežnika, je zato prav tako blokiran.

### Potrjen konflikt odvisnosti (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Vplivane datoteke

Vse tri datoteke `main.py` — tako zgornji uvoz kot uvoz znotraj funkcije v `main()`.

---

## KI-003 — `agent-dev-cli --pre` zastavica ni več potrebna

**Status:** ✅ Popravljeno (neprelomno) | **Resnost:** 🟢 Nizka

### Opis

Vse datoteke `requirements.txt` so prej vključevale `agent-dev-cli --pre` za pridobitev
predizdaje CLI. Odkar je GA 1.0.0 izdan 2026-04-02, je stabilna izdaja
`agent-dev-cli` zdaj na voljo brez zastavice `--pre`.

**Popravek:** Zastavica `--pre` je bila odstranjena iz vseh treh `requirements.txt` datotek.

---

## KI-004 — Dockerfile uporabljajo `python:3.14-slim` (predizhodna osnovna slika)

**Status:** Odprto | **Resnost:** 🟡 Nizka

### Opis

Vsi `Dockerfile` uporabljajo `FROM python:3.14-slim`, kar je predizhodna Python različica.
Za produkcijske nameščanja bi bilo smiselno zakleniti na stabilno izdajo (npr. `python:3.12-slim`).

### Vplivane datoteke

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Viri

- [agent-framework-core na PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry na PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Opozorilo**:
Ta dokument je bil preveden z uporabo storitve AI prevajanja [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da lahko avtomatizirani prevodi vsebujejo napake ali netočnosti. Izvirni dokument v njegovem maternem jeziku velja za avtoritativni vir. Za kritične informacije je priporočljivo uporabiti strokovni človeški prevod. Za kakršne koli nesporazume ali napačne interpretacije, nastale zaradi uporabe tega prevoda, ne prevzemamo odgovornosti.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->