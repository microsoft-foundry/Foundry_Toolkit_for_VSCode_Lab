# បញ្ហាដែលបានស្គាល់

ឯកសារនេះតាមដានបញ្ហាដែលបានស្គាល់ជាមួយស្ថានភាពទំនិញបច្ចុប្បន្ន។

> បានបំពានចុងក្រោយ៖ ២០២៦-០៤-១៥។ បានសាកល្បងប្រឆាំង Python 3.13 / Windows ក្នុង `.venv_ga_test`។

---

## Package Pins បច្ចុប្បន្ន (ភ្នាក់ងារទាំងបី)

| Package | បន្ទុកបច្ចុប្បន្ន |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(កន្លែងកំណត់ — មើល KI-003)* |

---

## KI-001 — ពិរុទ្ធ GA 1.0.0 ការអាប់ដេតបានឧបសគ្គ៖ `agent-framework-azure-ai` បានដកចេញ

**ស្ថានភាព:** បើក | **ភាពធ្ងន់ធ្ងរ:** 🔴 ខ្ពស់ | **ប្រភេទ៖** បែកបាក់

### សេចក្ដីពិពណ៌នា

បណ្ណៈ `agent-framework-azure-ai` (បានចាក់តែ `1.0.0rc3`) បាន **ដកចេញ / មិនគាំទ្រ** 
នៅក្នុងការចេញផ្សាយ GA (1.0.0, ចេញផ្សាយ ២០២៦-០៤-០២)។ វាត្រូវបានជំនួសដោយ៖

- `agent-framework-foundry==1.0.0` — ទ្រង់ទ្រាយភ្នាក់ងារតាម Foundry
- `agent-framework-openai==1.0.0` — ទ្រង់ទ្រាយភ្នាក់ងារប្រាក់ខាង OpenAI

ឯកសារ `main.py` ទាំងបីនាំចូល `AzureAIAgentClient` ពី `agent_framework.azure` ដែលបង្កើត
កំហុស `ImportError` នៅក្រោម package GA។ ឈ្មេាះ namespace `agent_framework.azure` នៅ GA 
មែនប៉ុន្តែនៅតែមិនមានទេថោកតែថ្នាក់ Azure Functions ទេ (`DurableAIAgent`, 
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — មិនមែនគឺភ្នាក់ងារ Foundry ទេ។

### កំហុសដែលបានបញ្ជាក់ (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### ឯកសារដែលទាក់ទង

| ឯកសារ | បន្ទាត់ |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` មិនត្រូវគ្នាជាមួយ GA `agent-framework-core`

**ស្ថានភាព:** បើក | **ភាពធ្ងន់ធ្ងរ៖** 🔴 ខ្ពស់ | **ប្រភេទ៖** បែកបាក់ (ឧបសគ្គនៅ upstream)

### សេចក្ដីពិពណ៌នា

`azure-ai-agentserver-agentframework==1.0.0b17` (ថ្មីបំផុត) ធ្វើការចាក់តែ
`agent-framework-core<=1.0.0rc3`។ ការដំឡើងវាភ្ជាប់ជាមួយ `agent-framework-core==1.0.0` (GA)
បង្ខំឱ្យ pip **ធ្វើចុះកម្តៅ** `agent-framework-core` ទៅកាន់ `rc3` ដែលបង្កហានការខូច
`agent-framework-foundry==1.0.0` និង `agent-framework-openai==1.0.0`។

ការហៅ `from azure.ai.agentserver.agentframework import from_agent_framework` ដែល
ត្រូវបានប្រើដោយភ្នាក់ងារទាំងអស់សម្រាប់ភ្ជាប់ HTTP server ក៏ត្រូវបានឧបសគ្គដែរ។

### បញ្ហាគ្នាដែលបានបញ្ជាក់ (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### ឯកសារដែលទាក់ទង

ឯកសារ `main.py` ទាំងបី — ទាំងការនាំចូលពីកំពូល និងការនាំចូលក្នុងមុខងារ `main()`។

---

## KI-003 — ទង់ `agent-dev-cli --pre` មិនចាំបាច់ប្រើបន្ថែមទៀត

**ស្ថានភាព:** ✅ បានជួសជុល (មិនបែកបាក់) | **ភាពធ្ងន់ធ្ងរ៖** 🟢 ទាប

### សេចក្ដីពិពណ៌នា

ឯកសារ `requirements.txt` ទាំងអស់ មានការរួមបញ្ចូល `agent-dev-cli --pre` សម្រាប់ទាញយក
CLI ពន្លឿនមុន។ តាំងពី GA 1.0.0 ត្រូវបានចេញផ្សាយនៅ ២០២៦-០៤-០២ ការចេញផ្សាយដែល
មានស្ថេរភាពនៃ `agent-dev-cli` ពេលនេះទំនងទៅអាចប្រើបានដោយគ្មានទង់ `--pre`។

**បានបញ្ចូលជួសជុល៖** ទង់ `--pre` ត្រូវបានដកចេញពីឯកសារ `requirements.txt` ទាំងបី។

---

## KI-004 — Dockerfiles ប្រើ `python:3.14-slim` (រូបភាពមូលដ្ឋានមុនចេញផ្សាយ)

**ស្ថានភាព:** បើក | **ភាពធ្ងន់ធ្ងរ៖** 🟡 ទាប

### សេចក្ដីពិពណ៌នា

Dockerfile ទាំងអស់ប្រើ `FROM python:3.14-slim` ដែលតាមដានកំណែ Python មុនចេញផ្សាយ។
សម្រាប់ការដាក់ប្រេីបច្ចុប្បន្នគួរតែចាក់តែកំណែដែលមានស្ថេរភាព (ឧទាហរណ៍ `python:3.12-slim`)។

### ឯកសារដែលទាក់ទង

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## ការយោង

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**៖  
ឯកសារ​នេះ​ត្រូវ​បាន​ប្រែ​ប្រើ​សេវាកម្ម​ប្រែ​សម្រួល AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ខណៈ​ពេល​យើង​ព្យាយាម​រក្សា​ការត្រឹមត្រូវ សូម​យកចិត្តទុកដាក់​ថា​ការ​ប្រែ​សម្រួល​ស្វ័យប្រវត្តិ​អាច​មាន​កំហុស ឬ​ការខ្វះខាត។ ឯកសារ​ដើម​នៅក្នុង​ភាសា​ដើម​គួរត្រូវបាន​ស្គាល់​ជា​ប្រភព​ដែល​មាន​សក្តានុពល។ សម្រាប់​ព័ត៌មាន​សំខាន់ គួរ​ឲ្យ​ប្រើ​ប្រែ​ដោយ​មនុស្ស​ជំនាញ។ យើងមិនទទួលខុសត្រូវ​ចំពោះ​ការ​យល់ខុស ឬ​ការ​ពន្យល់ខុស​ដែល​កើត​ពី​ការ​ប្រើប្រាស់​ការ​ប្រែនេះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->