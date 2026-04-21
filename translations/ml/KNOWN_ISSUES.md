# അറിയപ്പെടുന്ന പ്രശ്നങ്ങൾ

ഈ പ്രമാണം നിലവിലുള്ള റിപ്പോസിറ്ററിയുടെ അവസ്ഥയിലുള്ള അറിയപ്പെടുന്ന പ്രശ്നങ്ങളെ പിന്തുടരുന്നു.

> അവസാനമായുള്ള അപ്ഡേറ്റ്: 2026-04-15. Python 3.13 / Windows-ൽ `.venv_ga_test`-ന്റെ എതിരെ ടെസ്റ്റ് ചെയ്‌തത്.

---

## നിലവിലുള്ള പാക്കേജ് പിന്‍സ് (മൂന്നു ഏജന്റുകളും)

| പാക്കേജ് | നിലവിലെ പതിപ്പ് |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(സ്ഥിരീകരിക്കപ്പെട്ടു — KI-003 നോക്കുക)* |

---

## KI-001 — GA 1.0.0 അപ്ഡേറ്റ് തടയപ്പെട്ടു: `agent-framework-azure-ai` നീക്കംചെയ്‌തിരുന്നു

**അവസ്ഥ:** തുറന്നു | **തീവ്രത:** 🔴 ഉയർന്നത് | **തരം:** വിഘടിപ്പിക്കൽ

### വിവരണം

`agent-framework-azure-ai` പാക്കേജ് (`1.0.0rc3`-ൽ പിന് ചെയ്തു) GA വിപണി రిలీజ్ (1.0.0, 2026-04-02-ന് പുറത്തിറങ്ങി) ൽ **നീക്കംചെയ്‌തിരിക്കുന്നു/ഡിപ്പ്രീക്കേറ്റ്** ചെയ്തു.
അത് താഴെപ്പറയുന്നവ കൊണ്ട് മാറ്റിവച്ചിരിക്കുന്നു:

- `agent-framework-foundry==1.0.0` — ഫൗണ്ടറി-ഹോസ്റ്റുചെയ്ത ഏജന്റ് പാറ്റേൺ
- `agent-framework-openai==1.0.0` — ഓപ്പൺഎഐ പിന്തുടർന്ന ഏജന്റ് പാറ്റേൺ

മൂന്ന് `main.py` ഫയലുകളും `agent_framework.azure`-ൽ നിന്നും `AzureAIAgentClient` ഇറക്കുമതി ചെയ്യുന്നു, ഇത് GA പാക്കേജുകളിൽ `ImportError` ഉണ്ടാക്കുന്നു. GA-യിൽ `agent_framework.azure` namespaces ഇപ്പോഴും നിലനിൽക്കുന്നു, പക്ഷേ ഇപ്പോൾ Azure Functions ക്ലാസ്സുകൾ മാത്രമേ അടങ്ങിയിട്ടുള്ളൂ (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ഫൗണ്ടറി ഏജന്റുകൾ അല്ല.

### സ്ഥിരീകരിച്ച പിഴവ് (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### ബാധിച്ച ഫയലുകൾ

| ഫയൽ | ലൈൻ |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core`-നോടു പൊരുത്തക്കേടാണ്

**അവസ്ഥ:** തുറന്നു | **തീവ്രത:** 🔴 ഉയർന്നത് | **തരം:** വിഘടിപ്പിക്കൽ (അപ്പ്സ്ട്രീം ബ്ലോക്ക്)

### വിവരണം

`azure-ai-agentserver-agentframework==1.0.0b17` (പുതിയത്) `agent-framework-core<=1.0.0rc3` ആയി കർശനമായും പിന് ചെയ്തു.
ഇത് GA യിലുള്ള `agent-framework-core==1.0.0` ഒപ്പം ഇൻസ്റ്റാൾ ചെയ്യുമ്പോൾ, pip `agent-framework-core`-നെ ഞെട്ടിച്ച് `rc3`-ല് തന്നെ മടങ്ങിപ്പോകാൻ നിർബന്ധിക്കുന്നു, ഇത് പിന്നീട് `agent-framework-foundry==1.0.0`-നും `agent-framework-openai==1.0.0`-നും തകരാറു വരുത്തുന്നു.

എല്ലാ ഏജന്റുകളും HTTP സർവറുമായി ബൈൻഡിംഗ് നടത്താൻ ഉപയോഗിക്കുന്ന `from azure.ai.agentserver.agentframework import from_agent_framework` വിളി അതിനാൽ തടസപ്പെടുന്നു.

### സ്ഥിരീകരിച്ച ആശ്രിത സംഘർഷം (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### ബാധിച്ച ഫയലുകൾ

മൂന്നു `main.py` ഫയലുകളും — ടോപ്പ്-ലെവൽ ഇറക്കുമതിയും `main()`-ൽ ഫംഗ്ഷനു ഉള്ളിൽ ഇറക്കുമതിയും.

---

## KI-003 — `agent-dev-cli --pre` ഫ്ലാഗ് ഇനി ആവശ്യമില്ല

**അവസ്ഥ:** ✅ പരിഹരിച്ചു (വ്യവധിയില്ലാത്തത്) | **തീവ്രത:** 🟢 കുറഞ്ഞത്

### വിവരണം

മുൻപ് എല്ലാ `requirements.txt` ഫയലുകളിലും മുൻ റിലീസ് CLI ഓഫ്‌ചെയ്യാൻ `agent-dev-cli --pre` ഉൾപ്പെടുത്തിയിരുന്നു. GA 1.0.0 പുറത്തിറങ്ങിയ 2026-04-02 മുതൽ, `agent-dev-cli`-ന്റെ സ്ഥിരതയുള്ള റിലീസ് ഇപ്പോൾ `--pre` ഫ്ലാഗ് കൂടാതെ ലഭ്യമാണ്.

**പരിഹാരം:** എല്ലാ മൂന്ന് `requirements.txt` ഫയലുകളിലും നിന്നും `--pre` ഫ്ലാഗ് നീക്കംചെയ്‌തു.

---

## KI-004 — Dockerfiles `python:3.14-slim` ഉപയോഗിക്കുന്നു ( മുൻ റിലീസ് അടിസ്ഥാന ഇമേജ്)

**അവസ്ഥ:** തുറന്നു | **തീവ്രത:** 🟡 കുറഞ്ഞത്

### വിവരണം

എല്ലാ `Dockerfile`കൾക്കും `FROM python:3.14-slim` ഉണ്ട്, ഇത് മുൻ റിലീസ് പൈതൺ ഘടനയെ സൂചിപ്പിക്കുന്നു.
പ്രൊഡക്ഷൻ വിന്യാസങ്ങൾക്ക് ഇത് സ്ഥിരതയുള്ള റിലീസിനെ (ഉദാ., `python:3.12-slim`) പിന്‍ൻചെയ്യുക.

### ബാധിച്ച ഫയലുകൾ

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## റഫറന്റ്സുകൾ

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**വ്യക്തിഗത ഉത്തരവാദിത്വ മുൻകൂർ**:  
ഈ ഡോക്യുമെന്റ് AI വിവർത്തന സേവനം [Co-op Translator](https://github.com/Azure/co-op-translator) ഉപയോഗിച്ച് വിവർത്തനം ചെയ്യപ്പെട്ടതാണ്. നാം ശരിയായ വിവർത്തനത്തിനായി പരിശ്രമിക്കുകയാണെങ്കിലും, ഓട്ടോമേറ്റഡ് വിവർത്തനങ്ങളിൽ പിഴവുകൾ അല്ലെങ്കിൽ തെറ്റുകൾ ഉണ്ടാകാമെന്നും ദയവായി ശ്രദ്ധിക്കുക. അതിന്റെ സ്വഭാവഭാഷയിൽ ഉള്ള ഓറിജിനൽ ഡോക്യുമെന്റിനെ പരമാധികാര ഉറവിടമായി പരിഗണിക്കണം. നിർണായകമായ വിവരങ്ങൾക്ക്, പ്രൊഫഷണൽ മാനവ വിവർത്തനം നിർദേശിക്കുന്നു. ഈ വിവർത്തനത്തിന്റെ ഉപയോഗത്തിൽ നിന്നുണ്ടാകുന്ന ഏതെങ്കിലും തെറ്റായ ധാരണകൾക്കും തെറ്റായ വ്യാഖ്യാനങ്ങൾക്കും ഞങ്ങൾ ഉത്തരവാദികളല്ല.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->