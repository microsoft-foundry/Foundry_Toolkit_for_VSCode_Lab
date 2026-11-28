# មេហ្ស៊ូល 8 - ការដោះស្រាយបញ្ហា

មេហ្ស៊ូលនេះគ្របដណ្តប់ពីកំហុសទូទៅ ការជួសជុល និងយុទ្ធសាស្រ្តដំណោះស្រាយកំហុសជាក់លាក់សម្រាប់កម្មវិធីចល័តច្រើនភ្នាក់ងារ។

## បញ្ហាចេញលទ្ធផលពីភ្នាក់ងារ

### GapAnalyzer និយាយថា “ខ្ញុំនៅតែមិនមានរបាយការណ៏ត្រូវគ្នា”

**រោគសញ្ញា៖** ឆ្លើយតបរបស់ GapAnalyzer សុំឱ្យអ្នកបិទបញ្ចូលរបាយការណ៏ដែលមាន “ជំនាញខ្វះ” និង “របួសសញ្ញាបត្រ”។ វាធ្វើឡើងទោះបីអ្នកបានផ្ញើទាំងប្រវត្តិរូប និងបរិយាយការងារទាំងសោះក៏ដោយ។

**មូលហេតុ៖** អត្ថបទ JD មិនត្រូវបានផ្ញើទៅខាងក្រោមទៅ JD Agent ទេ។ ជាមួយ `context_mode="last_agent"`, `resume_executor` គឺជាអ្នកអនុវត្តតែម្នាក់ដែលធ្លាប់ឃើញសារដើមរបស់អ្នកប្រើ។ ប្រសិនបើ `RESUME_PARSER_INSTRUCTIONS` មិនរួមបញ្ចូលអត្ថបទ JD នៅលទ្ធផលរបស់វានោះ JD Agent គ្មាន JD ឲ្យបកប្រែ, MatchingAgent មិនអាចគណនារង្វាស់សម្របសម្រួល, ហើយ GapAnalyzer ទទួលបានការបញ្ចូលមិនមានអត្ថន័យ។

**ការវិភាគ៖**

នៅក្នុងកំណត់ហេតុម៉ាស៊ីនមេ សូមស្វែងរកផ្នែក MatchingAgent។ ប្រសិនបើវាមាន:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
ការផ្ញើបន្តត្រូវបានខ្វះឬខូច។

**ការជួសជុល៖** បញ្ជាក់ថា `RESUME_PARSER_INSTRUCTIONS` នៅក្នុង `main.py` មានផ្នែក `[JOB DESCRIPTION PASS-THROUGH]` និងច្បាប់៖
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
បញ្ជាក់ថា `JOB_DESCRIPTION_INSTRUCTIONS` មានច្បាប់បញ្ជូនបន្ត `[PARSED RESUME PASS-THROUGH]` ខាងក្រោម៖
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
ប្រសិនបើប្លុកសេចក្តីណែនាំណាមួយគឺជាកំណត់ត្រាផ្លូវភេទពីវិលហ្វារ យកវាបម្លែងជាទំព័រពេញពី [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)។

### MatchingAgent បញ្ចេញ “មិនអាចគណនារង្វាស់សម្របសម្រួល - មិនមាន JD”

នេះជាមូលហេតុដូចជាលើកទីមុន។ MatchingAgent ទទួលបានលទ្ធផលពី JD Agent ប៉ុន្តែផ្នែក `[PARSED RESUME PASS-THROUGH]` ត្រូវបានខ្វះឬទទេ ដូច្នេះវាមិនអាចប្រៀបធៀបទាំងពីរប្រវត្តិរូបទេ។ សូមបញ្ជាក់៖
1. `JOB_DESCRIPTION_INSTRUCTIONS` រួមបញ្ចូលច្បាប់បញ្ជូនបន្ត៖ `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` ប្រាប់ភ្នាក់ងារឲ្យស្វែងរកផ្នែក `[JD REQUIREMENTS]` និង `[PARSED RESUME PASS-THROUGH]` ។

ប្ដូរប្លុកសេចក្តីណែនាំទាំងពីរជាមួយគំរូពេញពី [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)។

### ចម្លើយបង្ហាញពីរដង

**រោគសញ្ញា៖** លទ្ធផល GapAnalyzer (ឬលទ្ធផលបណ្តុំទាំងមូល) បង្ហាញពីរដងក្នុងចម្លើយ Agent Inspector ។

**មូលហេតុ៖** `WorkflowBuilder` ប្រើការស្នើសុំ OR សម្រាប់ច្រកចូល - អ្នកអនុវត្តខាងក្រោមបើកធ្វើការបន្ទាន់បន្ទាប់ពី **ណាមួយ** រហូតបញ្ចប់។ ប្រសិនបើ `matching_executor` មានច្រកចូលពីរដង (មួយពី `resume_executor` និងមួយពី `jd_executor`) វាចាប់ផ្តើមធ្វើការពីរដង៖ មួយពេល ResumeParser បញ្ចប់ និងមួយពេល JD Agent បញ្ចប់។ បន្ទាប់មក GapAnalyzer ក៏ដំណើរការបីដងដែរ។

**ការជួសជុល៖** ប្រាកដថា `WorkflowBuilder` គឺជាខ្សែការដំណើរការដែលជាប្រព័ន្ធថ្នាលតែមួយគ្មានការចូលលើសពីមួយ៖

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

ប្រសិនបើអ្នកមានបន្ទាត់ `.add_edge(resume_executor, matching_executor)` ហួសដិត ត្រូវយកវាចេញ។ ច្បាប់បញ្ជូន `[PARSED RESUME PASS-THROUGH]` ក្នុងលទ្ធផល JD Agent បានផ្តល់ឱ្យ MatchingAgent មានសិទ្ធិចូលប្រវត្តិរូបរួចហើយ។

---

## បរិការណ៍ និងបំលែងរចនាសម្ព័ន្ធ

### តម្លៃ `.env` ខ្វះឬខុស

ឯកសារ `.env` ត្រូវតែធ្លាប់មាននៅក្នុងថត `PersonalCareerCopilot/` (ជាតម្លៃដូចគ្នានឹង `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

ខ្លឹមសារ `.env` ដែលរំពឹងទុក៖

**ផ្លូវ A - ម៉េฆ Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**ផ្លូវ B - Foundry តំបន់មូលដ្ឋាន:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> ទាំងពីរផ្លូវប្រើ `FOUNDRY_PROJECT_ENDPOINT` ។ តម្លៃខុសគ្នា៖ ម៉េฆប្រើចុងផ្លូវ Foundry `https://`; តំបន់មូលដ្ឋានប្រើ `http://localhost:5273/v1` ។ ដំណើរការ `foundry model list` ដើម្បីបញ្ជាក់ឈ្មោះម៉ូឌែលដែលត្រូវការសម្រាប់ផ្លូវ B។

> **រកឃើញ `FOUNDRY_PROJECT_ENDPOINT` របស់អ្នកៈ** 
- បើកផ្ទាំង Foundry Toolkit នៅ VS Code → ចុចស្ដាំលើគំរោងរបស់អ្នក → **ចម្លងចុងផ្លូវគំរោង**។
- ឬទៅកាន់ [Azure Portal](https://portal.azure.com) → គំរោង Foundry របស់អ្នក → **ការមើលទូទៅ** → **ចុងផ្លូវគំរោង**។

> **រកឃើញ `AZURE_AI_MODEL_DEPLOYMENT_NAME` របស់អ្នក:** នៅក្នុងផ្ទាំង Foundry Toolkit លាយបន្តិចគំរោងរបស់អ្នក → **ម៉ូឌែល** → រកឈ្មោះម៉ូឌែលដែលបានឱ្យដំណើរការ (ឧ. `gpt-4.1-mini`)។

### លំដាប់អាទិភាព Env var

`main.py` ប្រើ `load_dotenv(override=True)` ដែលមានន័យថា:

| អាទិភាព | ប្រភព | ឈ្នះពេលទាំងពីរត្រូវបានកំណត់? |
|----------|--------|------------------------|
| 1 (ខ្ពស់បំផុត) | ឯកសារ `.env` | បាទ/ចាស |
| 2 | តួបញ្ជា / ពហុកោណបរិស្ថាន | ប្រើនៅពេលកូនសោមួយដូចគ្នាមិនមាននៅក្នុង `.env` |

នៅក្នុងការអភិវឌ្ឍន៍តំបន់មូលដ្ឋាន នេះធ្វើឱ្យ `.env` ជាមូលដ្ឋានពិតប្រាកដ (ការកែប្រែ `.env` មានប្រសិទ្ធភាពភ្លាមៗក្នុងការរត់)។ នៅក្នុងការបង្ហោះម៉ាស៊ីនមេ Foundry ចាក់ Env var នៅកម្រិតតួបញ្ជាមួយ; ព្រោះ `.env` មិនជាផ្នែកមួយនៃរូបភាពបានបង្ហោះសម្រាប់ការរៀបចំមេរៀននេះទេ តម្លៃ Env ដែលបានចាក់បញ្ចូលត្រូវបានប្រើ។

---

## សម រម្យកម្មកំណែ

### ម៉ាទ្រីកកំណែបញ្ចី

ដំណើរការចល័តច្រើនភ្នាក់ងារពាក់ព័ន្ធនឹងកំណែបញ្ចីជាក់លាក់។ កំណែអតិផរណាអាចបណ្តាលឲ្យកំហុសពេលរត់។

| កញ្ចប់ | កំណែដែលទាមទារ | ពាក្យបញ្ជារត្រួតពិនិត្យ |
|---------|-----------------|---------------|
| `agent-framework-foundry` | ថ្មីជាងគេ | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ថ្មីជាងគេ | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ថ្មីជាងគេ | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### កំហុសកំណែទូទៅ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### ពិនិត្យកំណែទាំងអស់ភ្លាមៗ

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

លទ្ធផលដែលរំពឹងទុក៖

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## បញ្ហាបង្ហោះ

### ធុងគ្មានរក្សារភាពចាប់ផ្តើមបន្ទាប់ពីបង្ហោះ

1. **ពិនិត្យកំណត់ហេតុធុង៖**
   - បើកផ្ទាំង Foundry Toolkit → នៅក្រោមគំរោងរបស់អ្នក ចុច **Agents** → ផ្ទាំង **Hosted Agent** → ចុចភ្នាក់ងាររបស់អ្នក។ ពិនិត្យ **ស្ថានភាព** នៅផ្ទាំង **ព័ត៌មានលម្អិត** បន្ទាប់មកបើកផ្ទាំង **Playground** ហើយប្រើផ្ទាំង **កំណត់ហេតុ** ក្នុងផ្ទាំង **ព័ត៌មានលម្អិតសម័យ** ដើម្បីមើលលទ្ធផលធុង។
   - ស្វែងរកស្ទាតរម៉ាស៊ីន Python ឬកំហុសផ្នែកមូឌុលខ្វះ។

2. **កំហុសចាប់ផ្តើមធូងទូទៅ៖**

   | កំហុសនៅកំណត់ហេតុ | មូលហេតុ | ដោះស្រាយ |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` មិនមានកញ្ចប់ | បន្ថែមកញ្ចប់ ហើយធ្វើការ deploy ម្ដងទៀត |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` ឬ `.env` env vars មិនបានកំណត់ | បន្ទាន់សម័យ `agent.yaml` → `environment_variables` ផ្នែក (hosted) ឬ `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | មិនបានកំណត់ Managed Identity | Foundry កំណត់នេះដោយស្វ័យប្រវត្តិ - សូមធ្វើការត្រួតពិនិត្យថាអ្នកកំពុង deploy តាមរយៈ extension |
   | `OSError: port 8088 already in use` | Dockerfile បង្ហាញច្រកខុសឬមានការប្រឆាំងច្រក | ពិនិត្យ `EXPOSE 8088` ក្នុង Dockerfile និង `CMD ["python", "main.py"]` |
   | Container ឈប់ with code 1 | កំហុសដែលមិនបានចាត់ទុកក្នុង `main()` | សាកល្បង locally ជាជំហានដំបូង ([Module 5](05-test-locally.md)) ដើម្បីចាប់កំហុសមុន deploy |

3. **ធ្វើការបញ្ចូនម្ដងទៀតបន្ទាប់ពីជួសជុល៖**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → ជ្រើសជាអេជិនដដែល → deploy ជំនាន់ថ្មី។

### ការដាក់ចេញយឺតពេក

ពីភ្នាក់ងារច្រើនកុងតឺន័រនឹងចាប់ផ្តើមយឺតព្រោះពួកវាបង្កើត instance អេជិនចំនួន ៤ នៅពេលចាប់ផ្តើម។ រយៈពេលចាប់ផ្តើមធម្មតា៖

| ជំហាន | រយៈពេលរំពឹងទុក |
|-------|------------------|
| ការបង្កើតរូបភាព container | ១-៣ នាទី |
| ការបញ្ជូនរូបភាពទៅ ACR | ៣០-៦០ វិនាទី |
| ចាប់ផ្តើម container (អេជិនតែមួយ) | ១៥-៣០ វិនាទី |
| ចាប់ផ្តើម container (ភ្នាក់ងារច្រើន) | ៣០-១២០ វិនាទី |
| អេជិនមាននៅក្នុង Playground | ១-២ នាទី បន្ទាប់ពី "Started" |

> ប្រសិនបើស្ថានភាព "Pending" ប្រើប្រាស់ជាង ៥ នាទី សូមពិនិត្យកំណត់ត្រាហៅ container សម្រាប់កំហុស។

---

## បញ្ហា RBAC និង សិទ្ធិ

### `403 Forbidden` ឬ `AuthorizationFailed`

អ្នកត្រូវការ តួនាទី **[Foundry User](https://aka.ms/foundry-ext-project-role)** នៅលើគម្រោង Foundry របស់អ្នក (ដែលមានឈ្មោះពីមុនថា **Azure AI User** - តួនាទី ID មិនបានផ្លាស់ប្តូរ):

1. ចូលទៅ [Azure Portal](https://portal.azure.com) → តំណធនធាន **គម្រោង** Foundry របស់អ្នក។
2. ចុច **Access control (IAM)** → **Role assignments**។
3. ស្វែងរកឈ្មោះរបស់អ្នក → បញ្ជាក់ថា **Foundry User** (ឬស្លាកបុរាណ **Azure AI User**) មានបញ្ជី។
4. ប្រសិនបើបាត់បង់៖ **បន្ថែម** → **Add role assignment** → ស្វែងរក **Foundry User** → ផ្ដល់តួនាទីទៅគណនីរបស់អ្នក។

មើលឯកសារ [RBAC សម្រាប់ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) សម្រាប់ព័ត៌មានលម្អិត។

### មិនអាចចូលដំណើរការការដាក់ម៉ូដែល

ប្រសិនបើអេជិនបង្ហាញកំហុសពាក់ព័ន្ធម៉ូដែល៖

1. ពិនិត្យថាម៉ូដែលបានដាក់ចេញ: ផ្នែក Foundry sidebar → ពង្រីកគម្រោង → **Models** → ពិនិត្យស្ថានភាព `gpt-4.1-mini` (ឬម៉ូដែលរបស់អ្នក) ជា **Succeeded**។
2. ពិនិត្យឈ្មោះការដាក់ចេញផ្គូផ្គង: ប្រៀបធៀប `AZURE_AI_MODEL_DEPLOYMENT_NAME` នៅក្នុង `.env` (ឬ `agent.yaml`) ជាមួយឈ្មោះការដាក់ចេញពិត នៅ sidebar។
3. ប្រសិនបើការដាក់ចេញផុតកំណត់ (ជាន់ឥតគិតថ្លៃ): deploy ម្ដងទៀតពី [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)។

---

## បញ្ហា Foundry Local (ផ្លូវ B)

### សេវាកម្ម Foundry Local មិនដំណើរការ

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| អញ្ញត្តិ | មូលហេតុ | ជាដំណោះស្រាយ |
|---------|-------|-----|
| ការត្រួតពិនិត្យសុខភាពបង្ហាញ `503` | សេវាកម្មមិនបានចាប់ផ្តើម | `foundry local start` ឬចុច **Start** នៅក្នុង Foundry Toolkit sidebar |
| ការត្រួតពិនិត្យសុខភាពពន្យារពេល | ម៉ូដែលកំពុងផ្ទុក | រង់ចាំ ៣០–៦០ វិនាទី បន្ទាប់ពីចាប់ផ្តើម; ម៉ូដែលធំប៉ុន្មានវេលាខ្លះយូរ |
| `StatusCode: 404` នៅលើ `/v1/health` | ច្រកខុស | ហេតុដើមគឺ `5273`។ ពិនិត្យ `foundry local status` សម្រាប់ច្រកពិតប្រាកដ |
| ធនធានមិនគ្រប់គ្រាន់ | Foundry Local ត្រូវការចន្លោះ RAM ប្រហែល ៤ GB មិនប្រើ | បិទកម្មវិធីផ្សេងទៀត |
| ការទាញយកម៉ូដែលបរាជ័យ | ទំហំដំបូលតិច | ម៉ូដែលមានទំហំ ២–៨ GB។ បើកទំហំចន្លោះ ចុះក្រោម បន្ទាប់មក `foundry model pull <name>` |

### ឈ្មោះម៉ូដែលមិនផ្គូផ្គង

```powershell
# List downloaded models and their exact aliases
foundry model list
```

កំណត់ `AZURE_AI_MODEL_DEPLOYMENT_NAME` នៅក្នុង `.env` ជាឈ្មោះរ alias ពិតប្រាកដដែលបង្ហាញ (ឧ. `phi-4-mini` មិនមែន `Phi-4-mini`) ។

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` នៅក្នុងការរត់ក្នុងស្រុក (ផ្លូវ B)

លាបនៃ `main.py` ប្រើ `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` ។ Foundry Local ត្រូវការអោយការបញ្ជូនមួយនេះចុះទៅសេវាកម្មក្នុងស្រុក - **មិនមែន** `AZURE_AI_PROJECT_ENDPOINT` ។ សូមប្រាកដថា `.env` របស់អ្នកមានៈ

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### ឧបករណ៍ MCP នៅតែធ្វើការហៅបណ្តាញក្រៅ (ផ្លូវ B)

នេះគឺជាការរំពឹងទុក។ ឧបករណ៍ `search_microsoft_learn_for_plan` ទាញធនធានការរៀនពី `https://learn.microsoft.com/api/mcp`។ **តែសំនួរឈ្មោះជំនាញ** ផ្ញើតាមបណ្ដាញ - ពត៌មានប្រវត្តិ និងអត្ថបទ JD ត្រូវបានកែសម្រួលពេញលេញលើឧបករណ៍របស់អ្នកហើយមិនដែលផ្ញើចេញ។ ប្រសិនបើអាចដំណើរការជាលក្ខណៈផ្តាច់មុខ ត្រូវបន្ថែម `try/except` ជំនួសក្នុងឧបករណ៍ ដើម្បីផ្តប់ URL `learn.microsoft.com` ស្ថិតិពេលផ្ទៃមិនអាចទាក់ទងបាន។

---

## ស្វែងរកជំនួយ

ប្រសិនបើអ្នកជាប់គុកបន្ទាប់ពីព្យាយាមជួសជុលខាងលើ៖

1. **ពិនិត្យកំណត់ត្រាសេវា** - កំហុសភាគច្រើនបង្កើត Python stack trace នៅក្នុង terminal។ សូមអានការតាមដានកំហុសពេញលេញ។
2. **ស្វែងរកសារកំហុស** - ចម្លងអត្ថបទកំហុស ហើយស្វែងរកនៅក្នុង [Microsoft Q&A សម្រាប់ Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service)។
3. **បើកបញ្ហា** - បញ្ចូលបញ្ហានៅលើ [កន្លែងផ្ទុកកូដ workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) ជាមួយ៖
   - សារកំហុស ឬរូបថតមុខម្ខាង
   - កំណែ package របស់អ្នក (`pip list | Select-String "agent-framework"`)
   - កំណែ Python របស់អ្នក (`python --version`)
   - ថាតើបញ្ហានេះនៅក្នុងស្រុក ឬបន្ទាប់ពី deploy

---

### ចំណុចត្រួតពិនិត្យ

- [ ] អ្នកដឹងរបៀបត្រួតពិនិត្យ និងជួសជុលបញ្ហាកំណត់រចនាសម្ព័ន្ធ `.env`
- [ ] អ្នកអាចផ្ទៀងផ្ទាត់កំណែ package ទៅកាន់ម៉ាទ្រីសត្រូវការ
- [ ] អ្នកដឹងរបៀបពិនិត្យកំណត់ត្រាកុងតឺន័រនៃការអស់ស្តុក
- [ ] អ្នកអាចត្រួតពិនិត្យតួនាទី RBAC នៅក្នុង Azure Portal

---

**មុន៖** [07 - Verify in Playground](07-verify-in-playground.md) · **បន្ទាប់៖** [09 - Summary →](09-summary.md) · **ទំព័រដើម:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**:
ឯកសារនេះត្រូវបានបម្លែងភាសា ដោយប្រើសេវាបម្លែងភាសា AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ទោះយើងខ្ញុំមានក្តីប្រាថ្នាឱ្យបានច្បាស់លាស់ តែសូមយល់ដឹងថាការបម្លែងដោយស្វ័យប្រវត្តិក៏អាចមានកំហុសឬភាពមិនត្រឹមត្រូវ។ ឯកសារដើមជាភាសាទីតាំងគួរត្រូវបានគេប្រើជាប្រភពច្បាស់លាស់។ សម្រាប់ព័ត៌មានសំខាន់ៗ សូមណែនាំឱ្យប្រើប្រាស់ការប្រែដោយមនុស្សជំនាញ។ យើងខ្ញុំមិនទទួលខុសត្រូវចំពោះការយល់ច្រឡំ ឬការបកស្រាយខុសបន្ទាប់ពីការប្រើប្រាស់ការបម្លែងនេះនោះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->