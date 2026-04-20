# Ismert problémák

Ez a dokumentum nyomon követi a tároló aktuális állapotával kapcsolatos ismert problémákat.

> Utolsó frissítés: 2026-04-15. Tesztelve Python 3.13 / Windows alatt `.venv_ga_test` környezetben.

---

## Jelenlegi csomag verziók (mindhárom ügynök esetén)

| Csomag | Jelenlegi verzió |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(rögzített — lásd KI-003)* |

---

## KI-001 — GA 1.0.0 frissítés blokkolva: `agent-framework-azure-ai` eltávolítva

**Állapot:** Nyitott | **Súlyosság:** 🔴 Magas | **Típus:** Visszamenőleges kompatibilitás törés

### Leírás

Az `agent-framework-azure-ai` csomag (rögzítve `1.0.0rc3` verzióval) **eltávolításra/megsemmisítésre került** a GA kiadásban (1.0.0, megjelent 2026-04-02). Helyette:

- `agent-framework-foundry==1.0.0` — Foundry által hosztolt ügynök minta
- `agent-framework-openai==1.0.0` — OpenAI alapú ügynök minta

Mindhárom `main.py` fájl az `AzureAIAgentClient`-et importálja az `agent_framework.azure` könyvtárból, ami GA csomagok mellett `ImportError`-t dob. Az `agent_framework.azure` névtér továbbra is létezik GA alatt, de már csak Azure Functions osztályokat tartalmaz (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — nem Foundry ügynököket.

### Megerősített hiba (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Érintett fájlok

| Fájl | Sor |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` inkompatibilis a GA `agent-framework-core`-ral

**Állapot:** Nyitott | **Súlyosság:** 🔴 Magas | **Típus:** Visszamenőleges kompatibilitás törés (felülről blokkolva)

### Leírás

Az `azure-ai-agentserver-agentframework==1.0.0b17` (legfrissebb) szigorúan rögzíti az `agent-framework-core<=1.0.0rc3` verziót. Ha ezt a `agent-framework-core==1.0.0` (GA) verzió mellé telepítjük, akkor a pip **visszaminősíti** az `agent-framework-core`-t `rc3`-ra, ami megbontja az `agent-framework-foundry==1.0.0` és `agent-framework-openai==1.0.0` működését.

Az összes ügynök által használt `from azure.ai.agentserver.agentframework import from_agent_framework` hívás, ami az HTTP szerver kötésére szolgál, ezért szintén blokkolva van.

### Megerősített függőségi konfliktus (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Érintett fájlok

Mindhárom `main.py` fájl — mind a felső szintű import, mind a `main()` függvénybeli import.

---

## KI-003 — `agent-dev-cli --pre` kapcsoló többé nem szükséges

**Állapot:** ✅ Javítva (nem visszamenőleges kompatibilitási törés) | **Súlyosság:** 🟢 Alacsony

### Leírás

Korábban minden `requirements.txt` fájl tartalmazta az `agent-dev-cli --pre` parancsot, hogy előzetes CLI verziót telepítsen. Mivel a GA 1.0.0 2026-04-02-án megjelent, a stabil verzió már elérhető az előzetes kapcsoló nélkül.

**Javítás:** Az összes három `requirements.txt` fájlból eltávolításra került a `--pre` kapcsoló.

---

## KI-004 — Dockerfile-ok `python:3.14-slim` (előzetes alap image) használata

**Állapot:** Nyitott | **Súlyosság:** 🟡 Alacsony

### Leírás

Minden `Dockerfile` a `FROM python:3.14-slim` sort használja, ami egy előzetes Python buildet követ. Éles környezetekben stabil kiadásra kellene rögzíteni (pl. `python:3.12-slim`).

### Érintett fájlok

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Hivatkozások

- [agent-framework-core a PyPI-n](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry a PyPI-n](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:  
Ez a dokumentum az AI fordító szolgáltatás [Co-op Translator](https://github.com/Azure/co-op-translator) használatával készült. Bár a pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum anyanyelvén tekintendő a hiteles forrásnak. Kritikus információk esetén professzionális emberi fordítást javaslunk. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy félreértelmezésekért.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->