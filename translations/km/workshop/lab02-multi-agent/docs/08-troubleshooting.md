# ម៉ូឌុល 8 - ការដោះស្រាយបញ្ហា

ម៉ូឌុលនេះគ្របដណ្តប់ពីកំហុសទូទៅ ការជួសជុល និងយុទ្ធសាស្ត្របំបែកប្រាប់កំហុសដែលពិសេសសម្រាប់លំហូរតំណើរពហុភ្នាក់ងារ។

## បញ្ហាផលិតផលភ្នាក់ងារ

### GapAnalyzer ថ្មី “ខ្ញុំមិនទាន់មានរបាយការណ៍ផ្គូផ្គង”

**រោគសញ្ញា:** ចម្លើយរបស់ GapAnalyzer សុំឲ្យអ្នកបិទបញ្ចូលរបាយការណ៍ផ្គូផ្គងដែលមាន “ជំនាញខ្វះ” និង “ចន្លោះវិញ្ញាបនបត្រ”។ នេះកើតឡើងទោះបីអ្នកបានផ្ញើប្រវត្តិរូប និងការពិពណ៌នាការងារជារួម។

**មូលហេតុ:** អត្ថបទ JD មិនត្រូវបានផ្ញើទៅ JD Agent តាមหลัง។ ជាមួយ `context_mode="last_agent"` អ្នកប្រតិបត្តិ resume_executor តែម្ដងគឺគឺជាអ្នកដែលបានឃើញសារដើមរបស់អ្នកប្រើប្រាស់។ ប្រសិនបើ `RESUME_PARSER_INSTRUCTIONS` មិនបានរួមបញ្ចូលអត្ថបទ JD ក្នុងការផលិតរបស់វា JD Agent នឹងមិនមាន JD ដើម្បីបំបែកនោះទេ MatchingAgent មិនអាចគណនាគុណភាពបាន ហើយ GapAnalyzer ទទួលបានទិន្នន័យគ្មានអត្ថន័យ។

**ការពិនិត្យ:**

នៅក្នុងកំណត់ហេតុម៉ាស៊ីនបម្រើ សូមស្វែងរកស្វាន MatchingAgent។ ប្រសិនបើវាផ្ទុក:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
ការផ្ទេរត្រឡប់បានខ្វះឬខូចខាត។

**ការជួសជុល:** បញ្ជាក់ថា `RESUME_PARSER_INSTRUCTIONS` ក្នុង `main.py` មានផ្នែក `[JOB DESCRIPTION PASS-THROUGH]` និងច្បាប់៖
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
បញ្ជាក់ផងដែរថា `JOB_DESCRIPTION_INSTRUCTIONS` មានច្បាប់ផ្ទេរ `[PARSED RESUME PASS-THROUGH]`៖
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
ប្រសិនបើប្លុកការណែនាំណាមួយជាប្លុកខ្មៅពីកម្មវិធីសូហ្វកាល់ ដូររវាងវាជាមួយកំណែពេញពី [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)។

### MatchingAgent បង្ហាញ “មិនអាចគណនាគុណភាពបាន - គ្មាន JD ផ្តល់”

នេះជាមូលហេតុដើមដូចខាងលើ MatchingAgent បានទទួលផលលទ្ធផលពី JD Agent ប៉ុន្តែផ្នែក `[PARSED RESUME PASS-THROUGH]` ខ្វះឬទទេ ដូច្នេះវាមិនអាចប្រៀបធៀបទាំងពីរប្រវត្តិបាន។ សូមបញ្ជាក់៖
1. `JOB_DESCRIPTION_INSTRUCTIONS` រួមបញ្ចូលច្បាប់ផ្ទេរ៖ `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` សូមបញ្ជាក់ឱ្យភ្នាក់ងារស្វែងរកផ្នែក `[JD REQUIREMENTS]` និង `[PARSED RESUME PASS-THROUGH]`។

ប្តូរប្លុកណែនាំទាំងពីរជាមួយកំណែពេញពី [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)។

### ចម្លើយបង្ហាញពីរដង

**រោគសញ្ញា:** ផលបង្ហាញរបស់ GapAnalyzer (ឬផលបង្ហាញលូតលាស់ទាំងមូល) បង្ហាញពីរដងក្នុងចម្លើយ Agent Inspector។

**មូលហេតុ:** `WorkflowBuilder` ប្រើ OR-semantics សម្រាប់ផ្សារចូល — អ្នកប្រតិបត្តិដែលនៅក្រោមផ្លាស់ទីភ្លាមៗពេលដែលអ្នកមួយលើកបានបញ្ចប់។ ប្រសិនបើ `matching_executor` មានច្រកចូលពីរ (មួយពី `resume_executor` និងមួយពី `jd_executor`) វាស្បែកពីរដង៖ នៅពេល ResumeParser បញ្ចប់ និងនៅពេល JD Agent បញ្ចប់។ GapAnalyzer ក៏រត់ពីរដងផងដែរ។

**ការជួសជុល:** ត្រូវប្រាកដថាគ្រោង `WorkflowBuilder` ជាការដំណើរការតាមលំដាប់ត្បិតៗដោយគ្មាន fan-in៖

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # មិនមកពី resume_executor ឡើយ
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

ប្រសិនបើអ្នកមានបន្ទាត់ `.add_edge(resume_executor, matching_executor)` ដែលមិនបានប្រើ សូមដកវា។ ផ្នែកផ្ទេរ `[PARSED RESUME PASS-THROUGH]` ក្នុងលទ្ធផល JD Agent បានផ្តល់ឱ្យ MatchingAgent ទទួលបានប្រវត្តិរូបហើយ។

---

## បញ្ហាសម្បុរស្ថានភាព និងការកំណត់រចនាសម្ព័ន្ធ

### តម្លៃ `.env` ខ្វះឬខុស

ភိုင်ល៍ `.env` ត្រូវមាននៅក្នុងថត `PersonalCareerCopilot/` (កម្រិតដូច `main.py`)៖

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

មាតិកា `.env` ដែលរំពឹងទុក៖

**ផ្លូវ A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**ផ្លូវ B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> ទាំងពីរផ្លូវប្រើ `FOUNDRY_PROJECT_ENDPOINT`។ តម្លៃខុសគ្នា៖ cloud ប្រើចំណុចបញ្ចប់ Foundry `https://` ខណៈ local ប្រើ `http://localhost:5273/v1`។ ប្រតិបត្តិបញ្ជា `foundry model list` ដើម្បីបញ្ជាក់អត្តសញ្ញាណនៃម៉ូដែលសម្រាប់ផ្លូវ B។

> **នាំឱ្យដឹង `FOUNDRY_PROJECT_ENDPOINT` របស់អ្នក៖** 
- បើកផ្ទាំងប៊ុកទូល Foundry Toolkit នៅក្នុង VS Code → ចុចស្តាំលើគម្រោងរបស់អ្នក → **Copy Project Endpoint**។ 
- ឬចូលទៅកាន់ [Azure Portal](https://portal.azure.com) → គម្រោង Foundry របស់អ្នក → **Overview** → **Project endpoint**។

> **នាំឱ្យដឹង `AZURE_AI_MODEL_DEPLOYMENT_NAME` របស់អ្នក៖** នៅក្នុងផ្នែក Foundry Toolkit sidebar ពង្រីកគម្រោងរបស់អ្នក → **Models** → ប្រមូលមើលឈ្មោះម៉ូដែលដែលបានដាក់ (ឧ. `gpt-4.1-mini`)។

### អាទិភាពអថេរ Env

`main.py` ប្រើ `load_dotenv(override=True)` ដែលមានន័យថា:

| អាទិភាព | ប្រភព | អ្នកឈ្នះនៅពេលទាំងពីរត្រូវបានកំណត់? |
|----------|--------|------------------------|
| 1 (ខ្ពស់បំផុត) | ភိုင်ល៍ `.env` | បាទ/ចាស |
| 2 | អថេរ បរិវេណ shell / ធុងកុងតឺន័រ | ប្រើនៅពេលគន្លឹះដូចគ្នាមិនមានក្នុង `.env` |

នៅក្នុងការអភិវឌ្ឍក្នុងស្រុក វាធ្វើឲ្យ `.env` ជាផ្ទុកពិត (កែប្រែ `.env` ភ្លាមៗមានឥទ្ធិពលចំពោះការប្រតិបត្តិ)។ នៅក្នុងការដាក់ពាក្យផ្នែកចែកចាយ Foundry ផ្ដល់អថេរបរិវេណនៅកម្រិត container មុននេះទេ ព្រោះ `.env` មិនមានក្នុងរូបភាពដែលបានដាក់សម្រាប់លាបរ lab នេះ តម្លៃ container injected ត្រូវបានប្រើ។

---

## ភាពត្រូវគ្នានៃកំណែ

### ប៉ារ៉ាម៉ែត្រកំណែ package

លំហូរពហុភ្នាក់ងារតម្រូវឲ្យមានកំណែ package ជាក់លាក់។ កំណែខុសគ្នាបង្កើតកំហុសនៅពេលរត់។

| Package | កំណែតម្រូវការ | ពាក្យបញ្ជាសម្រាប់ពិនិត្យ |
|---------|-----------------|---------------|
| `agent-framework-foundry` | ថ្មីបំផុត | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ថ្មីបំផុត | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ថ្មីបំផុត | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### កំហុសកំណែទូទៅ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# កែសម្រួល៖ ដំឡើង agent-framework-foundry ឡើងវិញ
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ជួសជុល៖ ធ្វើបច្ចុប្បន្នកម្មការ mcp package
pip install mcp --upgrade
```

### ផ្ទៀងផ្ទាត់កំណែទាំងអស់ម្តងឯង

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

## បញ្ហាក្នុងការដាក់ពាក្យ

### កុងតឺន័រស្ទាតហ្វេចបរាជ័យបន្ទាប់ពីដាក់ពាក្យ

1. **ពិនិត្យកំណត់ហេតុកុងតឺន័រ៖**
   - បើកផ្ទាំងប៊ុកទូល Foundry Toolkit → ពង្រីក **Hosted Agents (Preview)** → ចុចលើភ្នាក់ងាររបស់អ្នក → ពង្រីកកំណែ → **Container Details** → **Logs**។
   - ស្វែងរកនូវ Python stack traces ឬកំហុសខ្វះ module។

2. **កំហុសធម្មតាក្នុងចាប់ផ្តើម container:**

   | កំហុសក្នុងកំណត់ហេតុ | មូលហេតុ | ការជួសជុល |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | ភាគតូចនៅក្នុង `requirements.txt` ខ្វះ | បន្ថែមភាគតូចនោះ ទាន់កំណត់ពាក្យផ្សព្វផ្សាយជាថ្មី |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | អថេរបរិវេណក្នុង `agent.yaml` ឬ `.env` មិនបានកំណត់ | ធ្វើបច្ចុប្បន្នភាព `agent.yaml` → ផ្នែក `environment_variables` (hosted) ឬ `.env` (រក្សាជាលក្ខណៈផ្ទាល់) |
   | `azure.identity.CredentialUnavailableError` | មិនបានកំណត់ Managed Identity | Foundry សង្កេតថាបានប្រើដោយស្វ័យប្រវត្តិ - សូមធ្វើការដាក់ពាក្យតាមរយៈបន្ថែម |
   | `OSError: port 8088 already in use` | Dockerfile បង្ហាញច្រកខុសឬច្រកម៉ូដជួបប្រទះ | សូមពិនិត្យ `EXPOSE 8088` នៅក្នុង Dockerfile និង `CMD ["python", "main.py"]` |
   | Container ចេញដោយកូដ 1 | ករណីរបាំងក្នុង `main()` | សាកល្បងក្នុងស្រុកជាដំបូង ([ម៉ូឌុល 5](05-test-locally.md)) ដើម្បីកាន់កាប់កំហុសមុនបញ្ចូន |

3. **ដាក់ពាក្យឡើងវិញបន្ទាប់ពីជួសជុល:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → ជ្រើសភ្នាក់ងារដដែល → ដាក់ពាក្យកំណែថ្មី។

### ដំណាក់កាលដាក់ពាក្យយឺតពេក

កុងតឺន័រ multi-agent ត្រូវការពេលចាប់ផ្តើមយូរជាងគេព្រោះពួកវាបង្កើតអ_instanceភ្នាក់ងារពហុជាលើកមួយនៅពេលចាប់ផ្តើម។ ពេលចាប់ផ្តើមធម្មតា៖

| ដំណាក់កាល | រយៈពេលរំពឹងទុក |
|-------|------------------|
| បង្កើតរូបភាព container | 1-3 នាទី |
| ផ្ញើរូបភាពទៅ ACR | 30-60 វិនាទី |
| ចាប់ផ្តើម container (ភ្នាក់ងារតែមួយ) | 15-30 វិនាទី |
| ចាប់ផ្តើម container (multi-agent) | 30-120 វិនាទី |
| ភ្នាក់ងារត្រូវបានអាចប្រើនៅ Playground | 1-2 នាទីបន្ទាប់ពី "Started" |

> ប្រសិនបើស្ថានភាព "Pending" នៅជាមួយលើស 5 នាទី សូមពិនិត្យកំណត់ហេតុកុងតឺន័រពីកំហុស។

---

## បញ្ហា RBAC និងសិទ្ធិ

### `403 Forbidden` ឬ `AuthorizationFailed`

អ្នកត្រូវការផលិតផល **[Foundry User](https://aka.ms/foundry-ext-project-role)** នៅលើគម្រោង Foundry របស់អ្នក (ឈ្មោះពីមុនជាផលិតផល **Azure AI User** - របាយការណ៍ ID មិនបានផ្លាស់ប្តូរ):

1. ចូលទៅ [Azure Portal](https://portal.azure.com) → ចូលទៅធនធានគម្រោង Foundry របស់អ្នក។
2. ចុច **Access control (IAM)** → **Role assignments**។
3. ស្វែងរកឈ្មោះអ្នក → បញ្ជាក់ថា **Foundry User** (ឬស្លាកចាស់ **Azure AI User**) មានក្នុងបញ្ជី។
4. ប្រសិនបើខ្វះ៖ **បន្ថែម** → **Add role assignment** → ស្វែងរក **Foundry User** → ប្ដូរទៅគណនីរបស់អ្នក។

សូមមើលឯកសារ [RBAC សម្រាប់ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) សម្រាប់ព័ត៌មានលម្អិត។

### ការដាក់ម៉ូដែលមិនអាចចូលប្រើបាន

ប្រសិនបើភ្នាក់ងារផ្តល់កំហុសពាក់ព័ន្ធម៉ូដែល៖

1. ផ្ទៀងផ្ទាត់ថាម៉ូដែលបានដាក់: ផ្ទាំង Foundry sidebar → ពង្រីកគម្រោង → **Models** → ពិនិត្យសម្រាប់ `gpt-4.1-mini` (ឬម៉ូដែលរបស់អ្នក) ជាមួយស្ថានភាព **Succeeded**។
2. ផ្ទៀងផ្ទាត់ឈ្មោះការដាក់បញ្ចូលស្រប៖ ប្រៀប `AZURE_AI_MODEL_DEPLOYMENT_NAME` នៅក្នុង `.env` (ឬ `agent.yaml`) ជាមួយឈ្មោះការដាក់បញ្ចូលពិតប្រាកដនៅក្នុងផ្នែក sidebar។
3. ប្រសិនបើការដាក់បញ្ចូលផុតកំណត់ (កម្រិតមិនគិតថ្លៃ): ដាក់បញ្ចូលឡើងវិញពី [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)។

---

## បញ្ហា Foundry Local (ផ្លូវ B)

### សេវាកម្ម Foundry Local មិនដំណើរការ

```powershell
# រក្សាស្ថានភាព
foundry local status

# ចាប់ផ្តើមសេវាកម្ម បើវា​បានឈប់ហើយ
foundry local start
```

| រោគសញ្ញា | មូលហេតុ | ការជួសជុល |
|---------|-------|-----|
| ការត្រួតពិនិត្យសុខភាពតប \(Status code\) `503` | សេវាកម្មមិនដំណើរការ | បញ្ជា `foundry local start` ឬចុច **Start** នៅក្នុងផ្នែក Foundry Toolkit sidebar |
| ការត្រួតពិនិត្យសុខភាពភ្លេចពេល | ម៉ូដែលនៅកំពុងផ្ទុក | រង់ចាំ 30–60 វិនាទីបន្ទាប់ពីចាប់ផ្តើម; ម៉ូដែលធំជាងនឹងយូរពេលបន្ថែម |
| `StatusCode: 404` លើ `/v1/health` | ច្រកខុស | ច្រកលំនាំដើមគឺ `5273`។ ពិនិត្យ `foundry local status` សម្រាប់ច្រកពិតប្រាកដ |
| មានធនធានមិនគ្រប់គ្រាន់ | Foundry Local ត្រូវការមានម៉េម៉ូរី RAM គ្មានប្រើ ~4 GB | បិទកម្មវិធីផ្សេងទៀត |
| ការទាញយកម៉ូដែលបរាជ័យ | ទំហំថតទិន្នន័យទាប | ម៉ូដែលមានទំហំ 2–8 GB។ សម្អាតទំហំ ធ្វើបន្ទាប់ `foundry model pull <name>` |

### ការផ្ទៀងផ្ទាត់ឈ្មោះម៉ូដែលមិនត្រូវ

```powershell
# បញ្ជីម៉ូដែលដែលបានទាញយក និងឈ្មោះប្រើប្រាស់ច្បាស់លាស់របស់ពួកវា
foundry model list
```

កំណត់ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ក្នុង `.env` ទៅឱ្យនាម_alias ត្រឹមត្រូវ (ឧ. `phi-4-mini`, មិនមែន `Phi-4-mini`)។

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` នៅពេលរត់ក្នុងស្រុក (ផ្លូវ B)

`main.py` របស់លាបនេះប្រើ `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`។ Foundry Local តម្រូវឲ្យអថេរនេះបញ្ជាក់ទៅសេវាកម្មក្នុងស្រុក - **មិន**មែន `AZURE_AI_PROJECT_ENDPOINT`។ សូមធ្វើឲ្យ `.env` របស់អ្នកមាន៖

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### ឧបករណ៍ MCP នៅតែធ្វើការហៅក្រៅ (ផ្លូវ B)

នេះគឺជាការរំពឹងទុក។ ឧបករណ៍ `search_microsoft_learn_for_plan` ទាញយកធនធានសិក្សាពី `https://learn.microsoft.com/api/mcp`។ **សំណួរឈ្មោះជំនាញតែប៉ុណ្ណោះ** ដែលផ្លាស់ទៅលើបណ្តាញ - ប្រវត្តិរូប និងអត្ថបទ JD ត្រូវបានដំណើរការទាំងមូលលើឧបករណ៍របស់អ្នក ហើយមិនដែលផ្ញើឆ្លង។ ប្រសិនបើតម្រូវដំណើរការស្វែងប្រព័ន្ធលើបណ្តាញ ដាក់ `try/except` ប្រើប្រាស់ជំនួសក្នុងឧបករណ៍ដែលត្រឡប់ URL ស្ទាតិក `learn.microsoft.com` នៅពេលមិនអាចទាក់ទងបាន។

---

## ដើម្បីទទួលបានជំនួយ

ប្រសិនបើអ្នកមានបញ្ហាបន្ទាប់ពីព្យាយាមជួសជុលខាងលើ៖

1. **ពិនិត្យកំណត់ហេតុម៉ាស៊ីនបម្រើ** - កំហុសច្រើនបង្កើត Python stack trace នៅលើ terminal។ អាន traceback ពេញលេញ។
2. **ស្វែងរកសារកំហុស** - ចម្លងអត្ថបទកំហុស និងស្វែងរកនៅក្នុង [Microsoft Q&A សម្រាប់ Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)។
3. **បើកបញ្ហា** - បញ្ចូលបញ្ហានៅលើ [ស្ពានការាកម្មវិធី](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) ជាមួយ៖
   - សារកំហុសឬរូបថតអេក្រង់
   - កំណែ package របស់អ្នក (`pip list | Select-String "agent-framework"`)
   - កំណែ Python របស់អ្នក (`python --version`)
   - ថាតើបញ្ហាត្រូវបានគេរកឃើញក្នុងស្រុកឬបន្ទាប់ពីដាក់ពាក្យ

---

### ចំណុចត្រួតពិនិត្យ

- [ ] អ្នកដឹងវិធីពិនិត្យ និងជួសជុលបញ្ហាកំណត់រចនាសម្ព័ន្ធ `.env`
- [ ] អ្នកអាចផ្ទៀងផ្ទាត់កំណែ package ត្រូវគ្នានឹងម៉ាទ្រីកត្រូវការ
- [ ] អ្នកដឹងវិធីពិនិត្យកំណត់ហេតុ container សម្រាប់ករណីបរាជ័យក្នុងការដាក់ពាក្យ
- [ ] អ្នកអាចផ្ទៀងផ្ទាត់តួនាទី RBAC នៅក្នុង Azure Portal

---

**មុននេះ:** [07 - ផ្ទៀងផ្ទាត់នៅក្នុង Playground](07-verify-in-playground.md) · **បន្ទាប់:** [09 - សេចក្ដីសង្ខេប →](09-summary.md) · **ផ្ទះ:** [Lab 02 README](../README.md) · [Workshop ផ្ទះ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**:
ឯកសារនេះត្រូវបានបម្លែងភាសា ដោយប្រើសេវាបម្លែងភាសា AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ទោះយើងខ្ញុំមានក្តីប្រាថ្នាឱ្យបានច្បាស់លាស់ តែសូមយល់ដឹងថាការបម្លែងដោយស្វ័យប្រវត្តិក៏អាចមានកំហុសឬភាពមិនត្រឹមត្រូវ។ ឯកសារដើមជាភាសាទីតាំងគួរត្រូវបានគេប្រើជាប្រភពច្បាស់លាស់។ សម្រាប់ព័ត៌មានសំខាន់ៗ សូមណែនាំឱ្យប្រើប្រាស់ការប្រែដោយមនុស្សជំនាញ។ យើងខ្ញុំមិនទទួលខុសត្រូវចំពោះការយល់ច្រឡំ ឬការបកស្រាយខុសបន្ទាប់ពីការប្រើប្រាស់ការបម្លែងនេះនោះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->