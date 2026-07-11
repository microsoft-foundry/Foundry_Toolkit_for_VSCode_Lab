# Module 8 - പ്രശ്നപരിഹാരം

ഈ മോഡ്യൂൾ മൾട്ടി-ഏജന്റ് വർക്ക്‌ഫ്ലോയ്ക്ക് പ്രത്യേകമായ സാധാരണ പിശകുകൾ, പരിഹാരങ്ങൾ, ഡീബഗിംഗ് തന്ത്രങ്ങൾ എന്നിവയെക്കുറിച്ച് കൈകാര്യം ചെയ്യുന്നു.

## ഏജന്റ് പുറപ്പെടുവിക്കൽ പ്രശ്നങ്ങൾ

### GapAnalyzer “എനിക്ക് ഇപ്പോഴും പൊരുത്തപ്പെട്ട റിപ്പോർട്ട് ലഭിച്ചിട്ടില്ല” എന്ന് പറയുന്നു

**രോഗലക്ഷണം:** GapAnalyzer ന്റെ പ്രതികരണം നിങ്ങൾക്കു “കഴിവുകൾ ലഭിക്കാത്തവ” “സഹിതമുള്ള പൊരുത്തം കണ്ടെത്തേണ്ട റിപ്പോർട്ട്” പേസ്റ്റ് ചെയ്യണമെന്ന് പറയുന്നു. നിങ്ങൾ ഒരു റിസ്യൂമെയും ജോബ് വിവരണവുമെല്ലാം അയച്ചിട്ടുമാണ് ഇത് സംഭവിക്കുന്നത്.

**കാരണം:** JD പാഠം JD ഏജന്റിനായി നീർച്ചുവാച്ചിലിറ്റിയിലേക്ക് കൈമാറപ്പെട്ടിട്ടില്ല. `context_mode="last_agent"` എന്നതിനുശേഷം, `resume_executor` മാത്രമാണ് ഉപയോക്താവിന്റെ യഥാർത്ഥ സന്ദേശം കാണുന്നത്. `RESUME_PARSER_INSTRUCTIONS` അതിന്റെ ഔട്ട്പുട്ടിൽ JD പാഠം ഉൾപ്പെടുത്തിയിട്ടില്ലെങ്കിൽ, JD ഏജന്റിനു JD പാഴ്‌സുചെയ്യാനാകില്ല, MatchingAgent പൊരുത്തമില്ലാതെ സ്കോർ കണക്കാക്കുകയില്ല, GapAnalyzer അർത്ഥരഹിതമായ ഇൻപുട്ട് സ്വീകരിക്കുന്നു.

**രോഗനിർണ്ണയം:**

സേർവർ ലോഗുകളിൽ MatchingAgent സ്പാൻ നോക്കുക. ഇതിൽ:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
സംക്രമണം സംബന്ധിച്ച പള്ള വകഭേദവും ഇല്ലാതെയോ തകരാറുണ്ടോ എന്ന കാര്യമാണു.

**പരിഹാരം:** `main.py`-ൽ `RESUME_PARSER_INSTRUCTIONS`-ൽ `[JOB DESCRIPTION PASS-THROUGH]` വിഭാഗവും നിയമവും ഉണ്ടെന്ന് സ്ഥിരീകരിക്കുക:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
`JOB_DESCRIPTION_INSTRUCTIONS`-ൽ `[PARSED RESUME PASS-THROUGH]` റീലേ നിയമവും ഉണ്ടെന്ന് ഉറപ്പുവരുത്തുക:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
ഈ നിർദ്ദേശ ബ്ലോക്ക് സ്കാഫോൾഡ് വിസാർഡിൽ നിന്ന് സ്റ്റെബ് ആയിരുന്നുവെങ്കിൽ, [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ലെ പൂർണ്ണ പതിപ്പ് ഉപയോഗിക്കുക.

### MatchingAgent “Cannot compute fit score - no JD provided” 출력 ചെയ്യുന്നുണ്ട്

ഇത് മുകളിൽ പറയുന്ന കാരണത്തിന്റെ സമാനമാണ്. MatchingAgent JD ഏജന്റിന്റെ ഔട്ട്പുട്ട് സ്വീകരിച്ചെങ്കിലും `[PARSED RESUME PASS-THROUGH]` വിഭാഗം ഇല്ലാതെയോ ശൂന്യമായിട്ടോ ഉള്ളതിനാൽ, രണ്ട് പ്രൊഫൈലുകളുടെയും താരതമ്യം ചെയ്‌തില്ല. സ്ഥിരീകരിക്കുക:
1. `JOB_DESCRIPTION_INSTRUCTIONS`-ൽ റീലേ നിയമം ഉൾപ്പെടുന്നു: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` ഏജന്റിന് `[JD REQUIREMENTS]` മായി `[PARSED RESUME PASS-THROUGH]` വിഭാഗങ്ങൾ തിരയാൻ പറയുന്നു.

ഇരുവിധ നിർദ്ദേശ ബ്ലോക്കുകളും [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ലെ പൂർണ്ണ പതിപ്പുകളും മാറ്റി ഉപയോഗിക്കുക.

### പ്രതികരണം രണ്ടുതവണ കാണപ്പെടുന്നു

**രോഗലക്ഷണം:** GapAnalyzer ഔട്ട്പുട്ട് (അല്ലെങ്കിൽ മുഴുവൻ പൈപ്പ്‌ലൈൻ ഔട്ട്പുട്ട്) ഏജന്റ് ഇൻസ്പെക്ടർ പ്രതികരണത്തിൽ രണ്ടുതവണ പ്രത്യക്ഷപ്പെടുന്നു.

**കാരണം:** `WorkflowBuilder` ലഭിക്കുന്ന എഡ്ജുകൾക്കായി OR-സെമാന്റിക്സ് ഉപയോഗിക്കുന്നു - ഒരു മുൻഗാമി പൂർത്തിയാക്കുമ്പോൾ താഴെയുള്ള എക്സിക്യൂട്ടർ പ്രവർത്തിക്കുന്നു. `matching_executor` എന്നതിന് രണ്ട് ഇടപെടലുകൾ ഉണ്ടെങ്കിൽ (`resume_executor` -ൽ നിന്നോ `jd_executor` -ൽ നിന്നോ), അത് രണ്ടുതവണ പ്രവർത്തിക്കും: ഒരിക്കൽ ResumeParser പൂർത്തിയായപ്പോൾ, മറ്റൊന്ന് JD ഏജന്റ് പൂർത്തിയായപ്പോൾ. GapAnalyzerയും രണ്ടുതവണ പ്രവർത്തിക്കും.

**പരിഹാരം:** `WorkflowBuilder` ഗ്രാഫ് സStrict കൂട്ടിച്ചേർക്കൽ ഇല്ലാതെ കൃത്യമായ പരമ്പരാഗത പൈപ്പ്‌ലൈൻ ആകണമെന്ന് ഉറപ്പുവരുത്തുക:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # റിസ്യൂം_എക്സിക്യൂട്ടർ നിന്നല്ല
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

നീക്കേണ്ട .add_edge(resume_executor, matching_executor) എന്ന stray ലൈനുണ്ടെങ്കിൽ അത് നീക്കുക. JD ഏജന്റ് ഔട്ട്ഫുട്ടിൽ ഉള്ള `[PARSED RESUME PASS-THROUGH]` റീലേ ഇതിനകം പൂർത്തിയായി MatchingAgent-ന് റിസ്യൂം ആക്‌സസ് നൽകുന്നു.

---

## പരിസ്ഥിതി ക്രമീകരണ പ്രശ്നങ്ങൾ

### ഇല്ലാത്ത അല്ലെങ്കിൽ തെറ്റായ `.env` മൂല്യങ്ങൾ

`.env` ഫയൽ `PersonalCareerCopilot/` ഡയറക്ടറിയിൽ (main.py-നൊപ്പം നിലയിൽ) ഉണ്ടായിരിക്കണം:

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

പ്രതീക്ഷിക്കുന്ന `.env` ഉള്ളടക്കം:

**പാത A - Foundry ക്ലൗഡ്:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**പാത B - Foundry ലൊക്കൽ:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> രണ്ട് പാതകളും `FOUNDRY_PROJECT_ENDPOINT` ഉപയോഗിക്കുന്നു. മൂല്യം വ്യത്യസ്തമാണ്: ക്ലൗഡ് `https://` Foundry എൻഡ്‌പോയിന്റ്; ലൊക്കൽ `http://localhost:5273/v1` ഉപയോഗിക്കുന്നു. പാത B യിലെ മോഡൽ ആലിയസ് ഉറപ്പാക്കാൻ `foundry model list` ഓടിക്കുക.

> **നിങ്ങളുടെ `FOUNDRY_PROJECT_ENDPOINT` കണ്ടെത്താൻ:**
- VS കോഡിൽ **Foundry Toolkit** സൈഡ്ബാർ തുറന്ന് → നിങ്ങളുടെ പ്രോജക്ടിൽ റൈറ്റ് ക്ലിക്ക് → **Copy Project Endpoint**.
- അല്ലെങ്കിൽ [Azure Portal](https://portal.azure.com) → നിങ്ങളുടെ Foundry പ്രോജക്ട് → **Overview** → **Project endpoint** സന്ദർശിക്കുക.

> **നിങ്ങളുടെ `AZURE_AI_MODEL_DEPLOYMENT_NAME` കണ്ടെത്താൻ:** Foundry Toolkit സൈഡ്ബാറിൽ നിങ്ങളുടെ പ്രോജക്ട് വികസിപ്പിച്ച് → **Models** → എൻറോൾ ചെയ്ത മോഡൽ പേര് കണ്ടെത്തുക (ഉദാഹരണത്തിന്, `gpt-4.1-mini`).

### Env var മുൻഗണന

`main.py`-ൽ `load_dotenv(override=True)` ഉപയോഗിക്കപ്പെടുന്നതിനാൽ:

| മുൻഗണന | സ്രോതസ്സ് | രണ്ടു നിന്നും ഒരേ സമയം സജ്ജീകരിച്ചാൽ ആരാണ് ലഭിക്കുന്നത്? |
|----------|--------|------------------------|
| 1 (ഉയർന്നത്) | `.env` ഫയൽ | അതിനെയാണ് നേടുന്നത് |
| 2 | ഷെൽ / കണ്ടെയിനർ പരിസ്ഥിതി വ്യത്യാസം | `.env`-ൽ ആ തിരിച്ചുകൽ ഇല്ലെങ്കിൽ ഉപയോഗിക്കുന്നു |

ഒന്നിച്ച്, പ്രാദേശിക വികസനത്തിൽ `.env` സത്യം ഉറപ്പാക്കുന്നു (എഡിറ്റ് ചെയ്തപ്പോൾ ഉടനെ പ്രവർത്തനം ബാധിക്കും). ഹോസ്റ്റുചെയ്ത പവർ സംവിധാനങ്ങളിൽ, Foundry കണ്ടെയിനർ തലത്തിൽ വ്യത്യാസങ്ങൾ ചേർക്കുന്നു; ഈ ലാബ് ക്രമീകരണത്തിന്റെ ഭാഗമല്ലാത്തതു കൊണ്ടു, ഇജക്ട് ചെയ്ത കണ്ടെയിനർ മൂല്യങ്ങൾ ഉപയോഗിക്കപ്പെടുന്നു.

---

## പതിപ്പുകൾ തമ്മിലുള്ള പൊരുത്തക്കേടുകൾ

### പാക്കേജ് പതിപ്പ് മാട്രിക്സ്

മൾട്ടി-ഏജന്റ് വർക്ക്‌ഫ്ലോയ്ക്ക് പ്രത്യേക പാക്കേജ് പതിപ്പുകൾ ആവശ്യമാണ്. പൊരുത്തക്കേടുകൾ റൺടൈം പിശകുകൾ ഉണ്ടാക്കും.

| പാക്കേജ് | ആവശ്യമായ പതിപ്പ് | പരിശോധിക്കൽ കമാൻഡ് |
|---------|-----------------|---------------|
| `agent-framework-foundry` | ഏറ്റവും പുതിയ | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ഏറ്റവും പുതിയ | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ഏറ്റവും പുതിയ | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### സാധാരണ പതിപ്പ് പിശകുകൾ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# പരിഹാരം: എജന്റ്-ഫ്രെയിംവർക്ക്-ഫൌണ്ട്‌റി പുനഃസ്ഥാപിക്കുക
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# പരിഹാരം: mcp പാക്കേജ് അപ്ഗ്രേഡ് ചെയ്യുക
pip install mcp --upgrade
```

### എല്ലാ പതിപ്പുകളും ഒരുമിച്ച് പരിശോധിക്കുക

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

പ്രതീക്ഷിക്കുന്ന ഔട്ട്പുട്ട്:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## വിന്യാസ പ്രശ്നങ്ങൾ

### വിന്യാസം കഴിഞ്ഞ് കണ്ടെയിനർ ആരംഭിക്കാതെ പരാജയപ്പെടുന്നു

1. **കണ്ടെയിനർ ലോഗുകൾ പരിശോധിക്കുക:**
   - **Foundry Toolkit** സൈഡ്ബാർ → **Hosted Agents (Preview)** വಿಸ್ತരിച്ചു → നിങ്ങളുടെ ഏജന്റ് തിരഞ്ഞെടുക്കുക → പതിപ്പ് വികസിപ്പിച്ച് → **Container Details** → **Logs**.
   - Python സ്റ്റാക്ക് ട്രേസുകൾ അല്ലെങ്കിൽ മോഡ്യൂൾ ഇല്ല എന്ന പിശകുകൾ അന്വേഷിക്കുക.

2. **സാധാരണ കണ്ടെയിനർ സ്റ്റാർട്ട് പരാജയങ്ങൾ:**

   | ലോഗിലെ പിശക് | കാരണം | പരിഹാരം |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` പാക്കേജ് കാണാറില്ല | പാക്കേജ് ചേർക്കുക, പുനഃസ്ഥാപിക്കുക |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` അല്ലെങ്കിൽ `.env` എൻവ്വൈറൺമെന്റ് വ്യത്യാസങ്ങൾ സജ്ജീകരിച്ചിട്ടില്ല | `agent.yaml`-ല്‍ → `environment_variables` വിഭാഗം (ഹോസ്റ്റുചെയ്യുന്ന) അല്ലെങ്കിൽ `.env` (പ്രാദേശിക) വായന പുതുക്കുക |
   | `azure.identity.CredentialUnavailableError` | മാനേജ്ഡ് ഐഡന്റിറ്റി സജ്ജമാക്കിയിട്ടില്ല | Foundry ഇത് സ്വയം സജ്ജമാക്കുന്നു - വീലെയായി എക്സ്റ്റൻഷൻ വഴി വിന്യാസം ചെയ്യുക |
   | `OSError: port 8088 already in use` | Dockerfile തെറ്റായ പോർട്ട് തുറന്നിരിക്കുന്നു അല്ലെങ്കിൽ പോർട്ട് തർക്കം | Dockerfile-ലെ `EXPOSE 8088` പരിശോധിക്കുക, `CMD ["python", "main.py"]`Confirm ചെയ്യുക |
   | കണ്ടെയിനർ കോഡ് 1-നു പുറത്ത് | `main()` ൽ കൈകാര്യമറ്റാപ്പം | പ്രഥമമായി പ്രാദേശികമായി പരിശോദിക്കുക ([Module 5](05-test-locally.md)) പിശകുകൾ പിടിക്കാൻ|

3. **പരിഹാരത്തിനു ശേഷം പുനഃസ്ഥാപിക്കുക:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → ഒരേ ഏജന്റ് തിരഞ്ഞെടുക്കുക → പുതിയ പതിപ്പ് വിന്യസിക്കുക.

### വിന്യാസം വളരെ നാളം എടുക്കുന്നു

മൾട്ടി-ഏജന്റ് കണ്ടെയിനറുകൾ തുടങ്ങാൻ കൂടുതൽ സമയം എടുക്കുന്നു കാരണം സ്റ്റാർട്ടപ്പിൽ 4 ഏജന്റ് ഇൻസ്റ്റൻസുകൾ ഉണ്ടാക്കുന്നു. സാധാരണ സ്റ്റാർട്ട് സമയം:

| ഘട്ടം | പ്രതീക്ഷിച്ച ദൈർഘ്യം |
|-------|------------------|
| കണ്ടെയിനർ ചിത്രം നിർമ്മാണം | 1-3 മിനിറ്റ് |
| ചിത്രങ്ങൾ ACR-യിലേക്ക് പുഷ് ചെയ്യൽ | 30-60 സെക്കൻഡ് |
| കണ്ടെയിനർ തുടങ്ങൽ (ഏക ഏജന്റ്) | 15-30 സെക്കൻഡ് |
| കണ്ടെയിനർ തുടങ്ങൽ (മൾട്ടി-ഏജന്റ്) | 30-120 സെക്കൻഡ് |
| പ്ലേഗ്രൗണ്ടിൽ ഏജന്റ് ലഭ്യമായത് | "Started" കഴിഞ്ഞ് 1-2 മിനിറ്റ് |

> "Pending" നില സ്ഥിതി 5 മിനിറ്റിൽ അധികം തുടരുകയാണെങ്കിൽ, കണ്ടെയിനർ ലോഗുകൾ പരിശോധിക്കുക.

---

## RBAC, അനുമതി പ്രശ്നങ്ങൾ

### `403 Forbidden` അല്ലെങ്കിൽ `AuthorizationFailed`

നിങ്ങൾക്ക് നിങ്ങളുടെ Foundry പ്രോജക്ടിൽ **[Foundry User](https://aka.ms/foundry-ext-project-role)** റോളിന്റെ അവകാശം വേണം (മുൻപ് **Azure AI User** എന്നായിരുന്നു - റോളിന്റെ ഐഡി മാറ്റമില്ല):

1. [Azure Portal](https://portal.azure.com) → നിങ്ങളുടെ Foundry **പ്രോജക്ട്** റിസോഴ്‌സ് സന്ദർശിക്കുക.
2. **Access control (IAM)** → **Role assignments** തിരഞ്ഞെടുക്കുക.
3. നിങ്ങളുടെ പേര് തിരയുക → **Foundry User** (അല്ലെങ്കിൽ പഴയ പിൻവിലിപ്പുള്ള ലേബൽ **Azure AI User**) ഉറപ്പാക്കുക.
4. കാണാത്ത പക്ഷം: **Add** → **Add role assignment** → **Foundry User** തിരയുക → നിങ്ങളുടെ അക്കൗണ്ടിന് നിയോഗിക്കുക.

വിശദാംശങ്ങൾക്ക് [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ഡോകുമെന്റേഷൻ കാണുക.

### മോഡൽ വിന്യാസം എന്നിവയിലെ പ്രവേശനം ലഭ്യമല്ല

ഏജന്റ് മോഡലുമായി ബന്ധമായ പിശകുകൾ നൽകുന്നുവെങ്കിൽ:

1. മോഡൽ വിന്യാസം പൂർത്തിയാണെന്ന് ഉറപ്പാക്കുക: Foundry സൈഡ്ബാർ → പ്രോജക്റ്റ് വികസിപ്പിച്ച് → **Models** → `gpt-4.1-mini` (അല്ലെങ്കിൽ നിങ്ങളുടെ മോഡൽ) ഉള്ളത് സ്ഥതി **Succeeded** നോക്കുക.
2. വിന്യാസത്തിന്റെ പേര് ശരിയാണ് എന്ന് ഉറപ്പാക്കുക: `.env` അല്ലെങ്കിൽ `agent.yaml` -ൽ ഉള്ള `AZURE_AI_MODEL_DEPLOYMENT_NAME` വേതകരില്ലാതെ സൈഡ്ബാറിൽ ഉള്ളവനൊപ്പം താരതമ്യം ചെയ്യുക.
3. വിന്യാസം കാലഹരണപ്പെട്ടു (ഫ്രീ ടിയർ): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) -നുന, `Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**-ൽ നിന്നും പുനഃസ്ഥാപിക്കുക.

---

## Foundry Local പ്രശ്നങ്ങൾ (പാത B)

### Foundry Local സേവനം പ്രവർത്തിക്കുന്നില്ല

```powershell
# സ്ഥിതി പരിശോധിക്കുക
foundry local status

# സേവനം നിർത്തിയിരിക്കുന്നുവെങ്കിൽ ആരംഭിക്കുക
foundry local start
```

| രോഗലക്ഷണം | കാരണം | പരിഹാരം |
|---------|-------|-----|
| ഹെൽത്ത് ചെക്ക് `503` നൽകുന്നു | സേവനം ആരംഭിച്ചിട്ടില്ല | `foundry local start` ഓടിക്കുക അല്ലെങ്കിൽ Foundry Toolkit സൈഡ്ബാറിൽ **Start** ക്ലിക്ക് ചെയ്യുക |
| ഹെൽത്ത് ചെക്ക് സമയപരിധി പിന്നിട്ടു | മോഡൽ ഇപ്പോഴും ലോഡിങ്ങ് സഹായിക്കുന്നു | തുടങ്ങിയതിനു ശേഷം 30–60 സെക്കൻഡ് കാത്തിരിക്കുക; വലിയ മോഡലുകൾക്ക് കൂടുതൽ സമയമെടുക്കും |
| `/v1/health`-ൽ `StatusCode: 404` | തെറ്റായ പോർട്ട് | ഡീഫാൾട്ട് `5273`. യഥാർത്ഥ പോർട്ട് അറിയാൻ `foundry local status` പരിശോധിക്കുക |
| അപര്യാപ്തമായ വിഭവങ്ങൾ | Foundry Localക്ക് ഏകദേശം 4 GB രാം ഒന്നും ഉപയോഗിക്കാൻ വേണ്ടത് | മറ്റ് ആപ്ലിക്കേഷനുകൾ അടക്കുക |
| മോഡൽ ഡൗൺലോഡ് പരാജയം | ഡിസ്ക് സ്ഥലമറ്റത്ത് | മോഡലുകൾ 2–8 GB ആകുന്നു; സ്ഥലം ശൂന്യമാക്കി, ശേഷം `foundry model pull <name>` ഓടിക്കുക |

### മോഡൽ പേരിന്റെ പൊരുത്തക്കേടുകൾ

```powershell
# ഡൗൺലോഡ് ചെയ്ത മോഡലുകളും അവയുടെ കൃത്യമായ ഉദ്ദേശപ്പേരുകളും പട്ടികപ്പെടുത്തുക
foundry model list
```

`.env`-ൽ `AZURE_AI_MODEL_DEPLOYMENT_NAME` യഥാർത്ഥ ആലിയസ് ആക്കുക (ഉദാ: `phi-4-mini`, `Phi-4-mini` അല്ല).

### പ്രാദേശിക ഓട്ടത്തിൽ `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (പാത B)

ലാബ് `main.py`-ൽ `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` ഉപയോഗിക്കുന്നു. Foundry Local ഇന്റർനൽ സർവീസിലേക്ക് ഈ വ്യത്യാസം പോയിന്റ് ചെയ്യണം - **`AZURE_AI_PROJECT_ENDPOINT` അല്ല**. ഉറപ്പാക്കുക `.env`-ൽ:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP ഉപകരണത്തിൽ പുറത്തേക്കുള്ള കോൾ ഇപ്പോഴും ഉണ്ടാകുന്നു (പാത B)

ഇത് പ്രതീക്ഷിക്കുന്നതാണ്. `search_microsoft_learn_for_plan` ഉപകരണം `https://learn.microsoft.com/api/mcp`-ലെ പഠന വിഭവങ്ങൾ തിരയുന്നു. **മാത്രം കഴിവ് പേര് ക്വറി** നെറ്റ്‌വർക്ക് വഴി പോകുന്നു - റിസ്യൂം, JD പാഠം മുഴുവൻ നിങ്ങളുടെ ഉപകരണത്തിൽ പ്രക്രിയ ചെയ്യപ്പെടുന്നു, അയയ്ക്കപ്പെടുന്നില്ല. പൂർണ്ണമായും ഓഫ്ലൈൻ ഓപ്പറേഷൻ ആവശ്യമെങ്കിൽ, എങ്കിൽ ഉപകരണം `try/except` ഫാൾബാക്ക് ചേർക്കുക ഒപ്പം എപ്പോഴെങ്കിലും നെറ്റ്‌വർക്ക് ലഭ്യമല്ലെങ്കിൽ സജ്ജീകരിച്ചത് `learn.microsoft.com` URL മുറിച്ചു നൽകുക.

---

## സഹായം നേടുക

മുകളിൽ പറയുന്ന പരിഹാരങ്ങൾ ശ്രമിച്ചതിനു ശേഷം തടഞ്ഞുപോയാൽ:

1. **സേർവർ ലോഗുകൾ പരിശോധിക്കുക** - ഭീതിമൂലക പിശകുകൾ പലതും ടെർമിനലിൽ Python സ്റ്റാക്ക് ട്രേസ് നൽകും. പൂർണ്ണ ട്രേയ്‌സ് വായിക്കുക.
2. **പിശകിന്റെ സന്ദേശം തിരയുക** - പിശക് ഉള്ളടക്കം പകർത്തി [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) ൽ തിരയുക.
3. **ഇഷ്യൂ തുറക്കുക** - [വർക്ക്ഷോപ്പ് റിപോസിറ്ററിയിൽ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) ഇഷ്യൂ ഓപ്പൺ ചെയ്യുക:
   - പിശക് സന്ദേശം അല്ലെങ്കിൽ സ്ക്രീൻഷോട്ട്
   - നിങ്ങളുടെ പാക്കേജ് പതിപ്പുകൾ (`pip list | Select-String "agent-framework"`)
   - നിങ്ങളുടെ Python പതിപ്പ് (`python --version`)
   - പ്രശ്നം പ്രാദേശികമാണോ വിന്യാസത്തിനു ശേഷം ആണോ എന്നും

---

### ചെക്ക്പോയിന്റ്

- [ ] `.env` ക്രമീകരണ പ്രശ്നങ്ങൾ പരിശോധിച്ച് പരിഹരിക്കാൻ അറിയാം
- [ ] ആവശ്യമായ പാക്കേജ് പതിപ്പുകൾക്ക് പൊരുത്തം ഉറപ്പാക്കാൻ കഴിയും
- [ ] വിന്യാസ പരാജയങ്ങൾക്കായി കണ്ടെയിനർ ലോഗുകൾ പരിശോധിക്കാൻ അറിയാം
- [ ] Azure Portal-ൽ RBAC റോളുകൾ പരിശോധിക്കാൻ കഴിയും

---

**മുൻ:** [07 - Verify in Playground](07-verify-in-playground.md) · **അടുത്തത്:** [09 - Summary →](09-summary.md) · **പ്രധാന:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**അറിയിപ്പ്**:
ഈ രേഖ AI പരിഭാഷാ സേവനം [Co-op Translator](https://github.com/Azure/co-op-translator) ഉപയോഗിച്ച് പരിഭാഷപ്പെടുത്തിയതാണ്. ഞങ്ങൾ കൃത്യതയ്ക്കായി ശ്രമിക്കുന്നുവെങ്കിലും, ഓട്ടോമേറ്റഡ് പരിഭാഷകളിൽ പിഴവുകൾ അല്ലെങ്കിൽ തെറ്റായ വിവരങ്ങൾ ഉണ്ടാകാൻ സാധ്യതയുണ്ട്. അതിന്റെ സ്വാഭാവിക ഭാഷയിലുള്ള അസൽ രേഖയാണ് പ്രാമാണികമായ ഉറവിടമായി പരിഗണിക്കേണ്ടത്. നിർണായകമായ വിവരങ്ങൾക്ക്, പ്രൊഫഷണൽ മനുഷ്യ പരിഭാഷ ശുപാർശ ചെയ്യുന്നു. ഈ പരിഭാഷ ഉപയോഗിച്ച് ഉണ്ടാകുന്ന തെറ്റിദ്ധാരണകൾ അല്ലെങ്കിൽ തെറ്റായ വ്യാഖ്യാനങ്ങൾക്കായി ഞങ്ങൾ ഉത്തരവാദികളല്ല.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->