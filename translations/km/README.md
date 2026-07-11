# បច្ចេកទេស Foundry Toolkit + កម្មវិធីសិក្សាសម្រាប់អ្នកតំណាង Foundry Hosted

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

សាងសង់, សាកល្បង, និងអនុវត្តប្រ៉ាក់តិសិន AI ទៅកាន់ **Microsoft Foundry Agent Service** ជា **Hosted Agents** - ពេញលេញពី VS Code ដោយប្រើ **កម្មវិធីបន្ថែម Microsoft Foundry** និង **Foundry Toolkit**។

> **Hosted Agents ឥលូវនេះនៅក្នុងជំហានសាកល្បង។** តំបន់ដែលគាំទ្រ មានកំណត់ - មើល [ភាពអាចប្រើប្រាស់តំបន់](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)។

> ថត `agent/` ក្នុងមួយមនុស្សរៀន គឺ **បានបង្កើតដោយស្វ័យប្រវត្តិ** ដោយកម្មវិធីបន្ថែម Foundry - បន្ទាប់មកអ្នកប្ដូរទំហឹងកូដ, សាកល្បងក្នុងតំបន់, ហើយអនុវត្ត។

### 🌐 គាំទ្រជាភាសាច្រើន

#### គាំទ្រតាមរយៈ GitHub Action (ស្វ័យប្រវត្តិនិងមានភាពទាន់សម័យជានិច្ច)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](./README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ចូលចិត្ត Clone ទៅក្នុងតំបន់មែនទេ?**
>
> រក្សាទុកនេះមានការប្រែសម្រួលជាភាសាច្រើនជាង ៥០ ដែលបង្កើនទំហំទាញយកយ៉ាងខ្លាំង។ ដើម្បី clone ដោយមិនមានការប្រែសម្រួល សូមប្រើ sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> វាបញ្ជូនអ្វីគ្រប់យ៉ាងដែលអ្នកត្រូវការ ដើម្បីបញ្ចប់វគ្គនេះជាមួយនឹងការទាញយកដែលលឿនជាង។
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## វិស្វត្បកម្ម

```mermaid
flowchart TB
    subgraph Local["ការអភិវឌ្ឍកន្លែង(Local Development) (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "F5 កែបញ្ហា(Debug)" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> សមាសធាតុ(Scaffold)
    Playground -- "សាកល្បងពាក្យបញ្ជា(Test prompts)" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**ចរន្ត:** កម្មវិធីបន្ថែម Foundry រៀបចំ agent → អ្នកប្ដូរកូដនិងសេចក្តីណែនាំ → សាកល្បងក្នុងតំបន់ជាមួយ Agent Inspector → អនុវត្តទៅ Foundry (រូបភាព Docker ផ្ញើទៅ ACR) → ធ្វើឱ្យប្រាកដនៅក្នុង Playground។

---

## អ្វីដែលអ្នកនឹងបង្កើត

| ឡាប់ | ការពិពណ៌នា | ស្ថានភាព |
|-----|-------------|--------|
| **ឡាប់ 01 - អ្នកតំណាងតែម្នាក់** | បង្កើត **"Explain Like I'm an Executive" Agent** សាកល្បងក្នុងតំបន់ ហើយអនុវត្តទៅ Foundry | ✅ មានស្រាប់ |
| **ឡាប់ 02 - ដំណើរការជា Multi-Agent** | បង្កើត **"Resume → Job Fit Evaluator"** - អ្នកតំណាង ៤ នាក់សហការដើម្បីវាយតម្លៃការពាក់ព័ន្ធនៃ résumé និងបង្កើតផែនទីរៀន | ✅ មានស្រាប់ |

---

## ជួបជាមួយ Executive Agent

ក្នុងកម្មវិធីសិក្សានេះ អ្នកនឹងបង្កើត **"Explain Like I'm an Executive" Agent** - អ្នកតំណាង AI ដែលយកពាក្យបច្ចេកទេសពិបាក ហើយប្រែអត្ថន័យឲ្យក្លាយជាសេចក្ដីសង្ខេបស្ងប់ស្ងាត់ និងមានត្រៀមក្នុងសន្និសីទបន្ទុកផ្ទាល់ការិយាល័យ។ ពីព្រោះមិនមាននរណាជាក្រុមគ្រប់គ្រង C-suite ត្រូវការស្តាប់អំពី "thread pool exhaustion caused by synchronous calls introduced in v3.2" ទេ។

ខ្ញុំបានបង្កើតអ្នកតំណាងនេះ បន្ទាប់ពីមានករណីមួយចំនួន ដែលខ្ញុំបានរៀបចំសេចក្តីរាយការណ៍ដល់ពេលក្រោយ តែមិនទទួលបានចម្លែកក់ល្អ ល្អ គឺ *"ដូច្នេះ... តើវែបសាយមានបញ្ហាឬអត់?"*

### វាធ្វើដូចម្តេច

អ្នកផ្តល់បច្ចេកទេសថ្មីមកវា វាសំរេចចិត្តបម្លែងជាសេចក្ដីសង្ខេបសម្រាប់អ្នកគ្រប់គ្រង - ពីរបីចំណុច, មិនមានពាក្យបច្ចេកទេស, មិនមាន stack traces, មិនមានសោកនាដកម្ម។ តែ **អ្វីដែលបានកើតឡើង**, **ផលប៉ះពលពាណិជ្ជកម្ម**, និង **ជំហានបន្ទាប់**។

### មើលវាធ្វើការជាក់ស្តែង

**អ្នកពោល៖**
> "The API latency increased due to thread pool exhaustion caused by synchronous calls introduced in v3.2."

**អ្នកតំណាងឆ្លើយតប៖**

> **សេចក្ដីសង្ខេបសម្រាប់អ្នកគ្រប់គ្រង:**
> - **អ្វីដែលបានកើតឡើង:** បន្ទាប់ពីប្រើប្រាស់ក្រោយទាំងស្រុង ប្រព័ន្ធយឺតចុះ។
> - **ផលប៉ះពលពាណិជ្ជកម្ម:** អ្នកប្រើប្រាស់មួយចំនួនបានជួបការពន្យារពេល ខណៈព្យាយាមប្រើសេវាកម្ម។
> - **ជំហានបន្ទាប់:** ការផ្លាស់ប្តូរបានត្រឡប់ក្រោយ ហើយកំពុងរៀបចំការជួសជុលមុនពេលអនុវត្តឡើងវិញ។

### ហេតុអ្វីបានជាជ្រើសរើសអ្នកតំណាងនេះ?

វាជាអ្នកតំណាងសាមញ្ញ សម្រួលមុខងារតែមួយ - សម្រាប់រៀនលំដាប់ជាកម្មវិធី hosted agent ពីដើមដល់ចប់ដោយមិនចាញ់ចិត្តប្រព័ន្ធឧបករណ៍ស្មុគស្មាញ។ ហើយតាមពិត? ក្រុមវិស្វកម្មរាល់ក្រុមអាចប្រើប្រាស់អ្នកតំណាងមួយនេះបាន។

---

## រចនាសម្ព័ន្ធកម្មវិធីសិក្សា

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **ចំណាំ៖** ថត `agent/` ក្នុងមួយមនុស្សរៀន គឺអ្វីដែលកម្មវិធីបន្ថែម **Microsoft Foundry** បង្កើតពេលអ្នករត់ `Microsoft Foundry: Create a New Hosted Agent` ពី Command Palette។ ឯកសារត្រូវបានកែប្រែនៅក្រោយជាមួយនឹងសេចក្ដីណែនាំ, ឧបករណ៍ និងកំណត់រចនាសម្ព័ន្ធរបស់អ្នកតំណាង។ ឡាប់ 01 នាំអ្នកតាមដានពីការបង្កើតនេះពីចាប់ផ្ដើម។

---

## ចាប់ផ្ដើម

### 1. Clone រក្សាទុកនេះ

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. តំឡើងបរិយាកាស Python លំនាំ Virtual

```bash
python -m venv venv
```

បើកវា:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. តំឡើង dependencies

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. កំណត់អថេរបរិយាកាស

ចម្លងឯកសារ `.env` នៃឧទាហរណ៍នៅក្នុងថត agent ហើយបញ្ចូលតម្លៃរបស់អ្នក:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

កែប្រែ `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. អនុវត្តឡាប់កម្មវិធីសិក្សា

ឡាប់រាល់ឡាប់មានម៉ូឌុលផ្ទាល់ខ្លួន។ ចាប់ផ្ដើមជាមួយ **ឡាប់ 01** ដើម្បីរៀនមូលដ្ឋាន ហើយបន្តទៅ **ឡាប់ 02** សម្រាប់ដំណើរការជា multi-agent។

#### លាប់ 01 - អ្នកតំណាងតែម្នាក់ ([សេចក្ដីណែនាំពេញលេញ](workshop/lab01-single-agent/README.md))

| # | ម៉ូឌុល | តំណរ |
|---|--------|------|
| 1 | អានលក្ខខណ្ឌមុន | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | តំឡើង Foundry Toolkit និងកម្មវិធីបន្ថែម Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | បង្កើតគម្រោង Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | បង្កើត hosted agent | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | កំណត់សេចក្ដីណែនាំ និងបរិយាកាស | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | សាកល្បងក្នុងតំបន់ | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | អនុវត្តទៅ Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | ផ្ទៀងផ្ទាត់នៅក្នុងព្រោងលែង | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | ដោះស្រាយបញ្ហា | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### លាប់ 02 - ដំណើរការជា Multi-Agent ([សេចក្ដីណែនាំពេញលេញ](workshop/lab02-multi-agent/README.md))

| # | ម៉ូឌុល | តំណរ |
|---|--------|------|
| 1 | លក្ខខណ្ឌមុន (ឡាប់ 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | យល់ដឹងអំពី វិស្វត្បកម្ម multi-agent | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | រៀបចំគម្រោង multi-agent | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | កំណត់អ្នកតំណាង និងបរិយាកាស | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | គំរូអង្គភាព | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | សាកល្បងក្នុងតំបន់ (multi-agent) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | ចែកចាយទៅ Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | បញ្ជាក់នៅក្នុងលំហសាកល្បង | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | ការដោះស្រាយបញ្ហា (ភ្នាក់ងារច្រើន) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## អ្នកថែទាំ

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## សិទ្ធិវាយតម្លៃដែលត្រូវការ (ការយោងឆាប់រហ័ស)

| វិស័យ | តួនាទីដែលត្រូវការ |
|----------|---------------|
| បង្កើតគម្រោង Foundry ថ្មី | **ម្ចាស់ Azure AI** លើធនធាន Foundry |
| ចែកចាយទៅគម្រោងដែលមានស្រាប់ (ធនធានថ្មី) | **ម្ចាស់ Azure AI** + **អ្នករួមចំណែក** លើការជាវ |
| ចែកចាយទៅគម្រោងដែលបានកំណត់រចនាសម្ព័ន្ធពេញលេញ | **អ្នកអាន** លើគណនី + **អ្នកប្រើ Azure AI** លើគម្រោង |

> **សំខាន់:** តួនាទី Azure `Owner` និង `Contributor` មានតែការអនុញ្ញាត *ការគ្រប់គ្រង* ប៉ុណ្ណោះ មិនសម្រាប់ *ការអភិវឌ្ឍន៍* (សកម្មភាពទិន្នន័យ) ទេ។ អ្នកត្រូវការ **អ្នកប្រើ Azure AI** ឬ **ម្ចាស់ Azure AI** ដើម្បីបង្កើតនិងចែកចាយភ្នាក់ងារ។

---

## ឯកសារយោង

- [Quickstart: ចែកចាយភ្នាក់ងារចាប់ផ្តើមរបស់អ្នក (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [ភ្នាក់ងារត្រូវបានផ្ទុកជាភាសាអ្វី?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [បង្កើតវេរលក្ខណៈភ្នាក់ងារផ្ទុកក្នុង VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [ចែកចាយភ្នាក់ងារផ្ទុកក្នុង](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC សម្រាប់ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [ឧទាហរណ៍ភ្នាក់ងារត្រួតពិនិត្យស្ថាបត្យកម្ម](https://github.com/Azure-Samples/agent-architecture-review-sample) - ភ្នាក់ងារផ្ទុកក្នុងពិភពពិតជាមួយឧបករណ៍ MCP, គំនូស Excalidraw, និងការចែកចាយពីរដង

---


## របបផ្សាយសិទ្ធិ

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ការបដិសេធ**:
ឯកសារនេះត្រូវបានបម្លែងភាសា ដោយប្រើសេវាបម្លែងភាសា AI [Co-op Translator](https://github.com/Azure/co-op-translator)។ ទោះយើងខ្ញុំមានក្តីប្រាថ្នាឱ្យបានច្បាស់លាស់ តែសូមយល់ដឹងថាការបម្លែងដោយស្វ័យប្រវត្តិក៏អាចមានកំហុសឬភាពមិនត្រឹមត្រូវ។ ឯកសារដើមជាភាសាទីតាំងគួរត្រូវបានគេប្រើជាប្រភពច្បាស់លាស់។ សម្រាប់ព័ត៌មានសំខាន់ៗ សូមណែនាំឱ្យប្រើប្រាស់ការប្រែដោយមនុស្សជំនាញ។ យើងខ្ញុំមិនទទួលខុសត្រូវចំពោះការយល់ច្រឡំ ឬការបកស្រាយខុសបន្ទាប់ពីការប្រើប្រាស់ការបម្លែងនេះនោះទេ។
<!-- CO-OP TRANSLATOR DISCLAIMER END -->