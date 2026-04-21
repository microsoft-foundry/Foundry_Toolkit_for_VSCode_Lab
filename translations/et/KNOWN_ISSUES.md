# Tuntud probleemid

See dokument jälgib teadaolevaid probleeme praeguse hoidla olekuga.

> Viimati uuendatud: 2026-04-15. Testitud Python 3.13 / Windows keskkonnas `.venv_ga_test`.

---

## Praegused pakettide lukustused (kõik kolm agendi)

| Pakett | Praegune versioon |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fikseeritud — vt KI-003)* |

---

## KI-001 — GA 1.0.0 uuendus blokeeritud: `agent-framework-azure-ai` eemaldatud

**Staatus:** Avatud | **Tõsidus:** 🔴 Kõrge | **Tüüp:** Katkestav

### Kirjeldus

`agent-framework-azure-ai` pakett (lukustatud versioonile `1.0.0rc3`) **eemaldati/ära kasutusele võetud**  
GA väljalaskes (1.0.0, välja antud 2026-04-02). See on asendatud järgmistega:

- `agent-framework-foundry==1.0.0` — Foundry majutatud agendi muster
- `agent-framework-openai==1.0.0` — OpenAI toetatud agendi muster

Kõik kolm `main.py` faili impordivad `AzureAIAgentClient` kui `agent_framework.azure` moodulist, mis  
tekitab GA pakettide all `ImportError` vea. `agent_framework.azure` nimi on GA-s endiselt olemas,  
kuid sisaldab nüüd ainult Azure Funktsioonide klasse (`DurableAIAgent`,  
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — mitte Foundry agente.

### Kinnitatud viga (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Mõjutatud failid

| Fail | Rida |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` ei ühildu GA `agent-framework-core`-ga

**Staatus:** Avatud | **Tõsidus:** 🔴 Kõrge | **Tüüp:** Katkestav (ülesvoogu ootel)

### Kirjeldus

`azure-ai-agentserver-agentframework==1.0.0b17` (viimane) lukustab  
`agent-framework-core<=1.0.0rc3`. Selle paigaldamine koos `agent-framework-core==1.0.0` (GA) versiooniga sunnib pipi  
**langetama** `agent-framework-core` tagasi `rc3` versioonile, mis omakorda rikub  
`agent-framework-foundry==1.0.0` ja `agent-framework-openai==1.0.0` paigalduse.

`from azure.ai.agentserver.agentframework import from_agent_framework` import, mida kõik agendid  
kasutavad HTTP serveri sidumiseks, on seetõttu samuti blokeeritud.

### Kinnitatud sõltuvuskonflikt (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Mõjutatud failid

Kõikide kolme `main.py` failid — nii peamine ülemine import kui ka `main()` funktsiooni sees tehtud import.

---

## KI-003 — `agent-dev-cli --pre` lipp enam vajalik

**Staatus:** ✅ Fikseeritud (mittekatkestav) | **Tõsidus:** 🟢 Madal

### Kirjeldus

Kõik `requirements.txt` failid sisaldasid varem `agent-dev-cli --pre` käsu, et saada  
eelvabastuse CLI versioon. Alates GA 1.0.0 väljalaske kuupäevast 2026-04-02 on  
`agent-dev-cli` stabiilne vabastus saadaval ilma `--pre` liputa.

**Rakendatud parandus:** Kõikidest kolmest `requirements.txt` failist on `--pre` lipp eemaldatud.

---

## KI-004 — Dockerfile’id kasutavad `python:3.14-slim` (eelvabastuse baaspilt)

**Staatus:** Avatud | **Tõsidus:** 🟡 Madal

### Kirjeldus

Kõik `Dockerfile` failid kasutavad `FROM python:3.14-slim`, mis põhineb eelvabastuse Python ehitusel.  
Tootmiskeskkonnas peaks see olema lukustatud stabiilsele versioonile (nt `python:3.12-slim`).

### Mõjutatud failid

- `ExecutiveAgent/Dockerfile`  
- `workshop/lab01-single-agent/agent/Dockerfile`  
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Viited

- [agent-framework-core PyPI-s](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry PyPI-s](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Väljavõte**:
See dokument on tõlgitud tehisintellekti tõlketeenuse [Co-op Translator](https://github.com/Azure/co-op-translator) abil. Kuigi püüame tagada täpsust, olge teadlikud, et automaatsed tõlked võivad sisaldada vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Kriitilise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlke kasutamisest tulenevate arusaamatuste või väärarusaamade eest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->