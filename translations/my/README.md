# Foundry Toolkit + Foundry Hosted Agents Workshop

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

**Microsoft Foundry Agent Service** သို့ **Hosted Agents** အဖြစ် AI Agent များကို VS Code မှတဆင့် **Microsoft Foundry extension** နှင့် **Foundry Toolkit** အသုံးပြုကာ ဆောက်လုပ်၊ စမ်းသပ်၊ ပြရန်။

> **Hosted Agents သည် ယခုအခါ မကြာသေးမီက စမ်းသပ်ဆောင်ရွက်နေဆဲဖြစ်သည်။** ပံ့ပိုးပေးသော ဒေသများကန့်သတ်ချက်ရှိပါသည် - [ဒေသရနိုင်မှု](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ကိုကြည့်ပါ။

> Lab တစ်ခုချင်းစီ၏ `agent/` ဖိုင်တွဲသည် Foundry extension မှ **အလိုအလျောက် တည်ဆောက်ခံထားခြင်း**ဖြစ်ပြီး၊ သင်သည် ကုဒ်ကို ကိုယ်တိုင်ပြင်ဆင်၊ ဒေသတွင်း စမ်းသပ်ပြီး တင်ပို့နိုင်ပါသည်။

### 🌐 ဘာသာစကားများစွာ ထောက်ပံ့မှု

#### GitHub Action ဖြင့် ထောက်ပံ့သည် (အလိုအလျောက် ပြုလုပ်ပြီး နေ့စဉ်မွမ်းမံနေသည်)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](./README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ဒေသတွင်းကို ကလုတ်လုပ်ချင်ပါသလား?**
>
> ဤ repository သည် ၅၀ ကျော် ဘာသာစကားအတွက် ဘာသာပြန်ချက်များပါဝင်သောကြောင့် အာရုံစိုက်မှု အရွယ်အစား တိုးမြှင့်ပါသည်။ ဘာသာပြန်ချက်များမပါဘဲ ကလုတ်လုပ်ရန် sparse checkout ကိုအသုံးပြုပါ။
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
> ၎င်းသည် သင်အား သင်တန်းကို မြန်ဆန်စွာပြီးစီးနိုင်ရန်လိုအပ်သည့် အရာအားလုံးကို ပေးပါသည်။
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## ပုံသဏ္ဌာန်

```mermaid
flowchart TB
    subgraph Local["ဒေသীয় ဖွံ့ဖြိုးတိုးတက်မှု (VS Code)"]
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
        Scaffold -- "F5 ဒီဘတ်" --> Inspector
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
    (localhost:8088)" --> သင်္ချာစနစ်
    Playground -- "စမ်းသပ်မှု အကြံပြုချက်များ" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**စီးဆင်းပုံ:** Foundry extension မှ agent ကို scaffolding ပြုလုပ် → သင်သည် ကုဒ်နှင့် ညွှန်ကြားချက်များကိုပြင်ဆင် → Agent Inspector ဖြင့် ဒေသတွင်းစမ်းသပ် → Foundry သို့ ပို့ခြင်း (Docker အိုင်မေ့ခ်ကို ACR သို့ တင်ပို့) → Playground တွင် အတည်ပြုသည်။

---

## သင် တည်ဆောက်မည့် အရာများ

| Lab | ဖော်ပြချက် | နေ့စဉ်အခြေအနေ |
|-----|-------------|--------|
| **Lab 01 - Single Agent** | **"Explain Like I'm an Executive" Agent** ကို တည်ဆောက်၊ ဒေသတွင်းစမ်းသပ်ပြီး Foundry သို့ တင်ပို့မည် | ✅ ရနိုင်ပါပြီ |
| **Lab 02 - Multi-Agent Workflow** | **"Resume → Job Fit Evaluator"** ကို တည်ဆောက်မည် - Agent ၄ ခုသည် အသင်းလိုက် Resume ကိုမှတ်ချက်ပေးခြင်းနှင့် သင်ယူမှု ပြမတ်ပုံ များဖန်တီးခြင်းနှင့် ပူးပေါင်းဆောင်ရွက်မည် | ✅ ရနိုင်ပါပြီ |

---

## Executive Agent ကို တွေ့ဆုံခြင်း

ဤ workshop တွင် သင်သည် **"Explain Like I'm an Executive" Agent** ကို တည်ဆောက်မည် - စိတ်ညစ်စရာနည်းပညာစကားများကို စာပိုဒ်သက်သောင့်သက်သာရှိသော ဌာနခန်းမအဆင့် စာချုပ်များသို့ ဘာသာပြန်ပေးသော AI Agent ဖြစ်သည်။ C-suite တွင် "v3.2 တွင် မူကွဲဖို့ synchronous call များကြောင့် thread pool ကို သုံးလို့ နောက်ကျခြင်း" ဆိုသည့်အကြောင်း တစ်ဦးတည်းမကြားချင်ကြပါ။

ဤ agent ကို ငါ့ရဲ့တိကျပြီး မွမ်းမံထားသော post-mortem ကို "ဆိုလိုတာ website ကပိတ်သွားပြီလား?" ဆိုပြီး အကြောင်းပြန်ခဲ့သော နောက် စိတ်ပေးခြင်း မကြာခဏကြုံရမိ၍ တည်ဆောက်ခဲ့ပါသည်။

### ၎င်း၏ လည်ပတ်ပုံ

သင်သည် နည်းပညာဆိုင်ရာ အပ်ဒိတ်ကို ထည့်သွင်းပေးသည်။ ၎င်းသည် executive summary ကို ပြန်ပြီးဖြေနိုင်သည် - သုံးချက် bullet point ဖြစ်ပြီး စကားလုံးရှုပ်ထွေးမှု၊ stack trace များ၊ စိတ်မကောင်းမှု မပါဝင်ပါ။ သာ **ဖြစ်ပျက်สิ่ง**, **လုပ်ငန်းထိခိုက်မှု**, နှင့် **နောက်တစ်ဆင့်**။

### လည်ပတ်သည့် ပုံကို ကြည့်ရှုရန်

**သင်ပြောသည်:**
> "API latency သည် v3.2 မှ synchronous call များကြောင့် thread pool သုံးလွတ်မှုကြောင့် တိုးတက်ခဲ့သည်။"

**Agent မှ ပြန်ကြားသည်:**

> **Executive စာစုအကျဉ်း:**
> - **ဖြစ်ခဲ့သည့်အချက်:** နောက်ဆုံးထုတ်လုပ်မှုနောက်ပိုင်း စနစ်မှန်မြည်သွားပါသည်။
> - **လုပ်ငန်းထိခိုက်မှု:** အသုံးပြုသူအချို့သည် ဝန်ဆောင်မှုကို သုံးစဉ် အချိန်နှောင့်နှေးမှု ခံစားခဲ့ရသည်။
> - **နောက်တစ်ဆင့်:** ပြောင်းလဲမှုကို ရှေ့ပြေး ပြန်ဆုတ်ပြီး ပြင်ဆင်ရေး အစီအစဉ်တင်မြှောက်နေပြီး ပြန်တင်ဆော့ရန် ကြိုတင်ပြင်ဆင်ထားသည်။

### ၎င်း agent ကို ဘာကြောင့် သုံးသင့်သလဲ?

၎င်းကို အသုံးပြုရလွယ်ကူပြီး တစ်ဦးတည်းအတွက်သာ ရည်ရွယ်ထားသည့် agent ဖြစ်သည် - hosted agent workflow ကို စတင်သင်ယူလိုသူများအတွက် ပြတ်သားစွာ လေ့လာနိုင်ရန်အတွက် အထူးသင့်တော်သည်။ ထို့အပြင်? အင်ဂျင်နီယာအသင်းတိုင်းတွင် ၎င်းလို agent တစ်ခုလိုအပ်သည်ဟု ယူဆပါသည်။

---

## Workshop ဖွဲ့စည်းပုံ

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

> **မှတ်ချက်:** Lab တစ်ခုလုံးမှ `agent/` ဖိုင်တွဲမှာ သင်က Command Palette မှ `Microsoft Foundry: Create a New Hosted Agent` ကိုrun လုပ်သည့်အခါ **Microsoft Foundry extension** က ဤဖိုင်များကို ပေါ်လာစေသည်။ ထို့နောက် သင့်၏ agent ညွှန်ကြားချက်များ၊ ကိရိယာများနှင့် ဖော်ပြချက်များဖြင့် ပြင်ဆင်သည်။ Lab 01 တွင် မူလမှစပြီး ၎င်းကို ပြန်လည်ဖန်တီးရန် လမ်းညွှန်ထားသည်။

---

## စတင်ရန်

### ၁။ Repository ကို ကလုတ်လုပ်ပါ

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### ၂။ Python virtual environment တစ်ခု တပ်ဆင်ပါ

```bash
python -m venv venv
```

လှုပ်ရှားပေးပါ:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### ၃။ လိုအပ်သော dependency များ ထည့်သွင်းပါ

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### ၄။ ပတ်ဝန်းကျင် မူလတိုင်များ configuration ပြုလုပ်ပါ

agent ဖိုင်တွဲအတွင်းရှိ နမူနာ `.env` ဖိုင်ကို ကူးယူပြီး သင့်တန်ဖိုးများဖြည့်စွက်ပါ။

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` ကို ပြင်ဆင်ပါ။

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### ၅။ Workshop labs များ နောက်တက်ပါ

Lab တစ်ခုချင်းစီသည် သူ၏ module များဖြင့် ကိုယ်စားပြု၎င်းပါ။ အဓိကအားဖြင့် **Lab 01** တွင် အခြေခံ အကြောင်းအရာများ သင်ယူပြီး နောက်ပိုင်း **Lab 02** သို့ ဆက်သွားကာ multi-agent workflows ကို ကျွမ်းကျင်ပါ။

#### Lab 01 - Single Agent ([အပြည့်အစုံ ညွှန်ကြားမှုများ](workshop/lab01-single-agent/README.md))

| # | Module | Link |
|---|--------|------|
| 1 | ရှေ့ပြေးလိုအပ်ချက်များ ဖတ်ရှုပါ | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry extension ထည့်သွင်းပါ | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry project တစ်ခုဖန်တီးပါ | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Hosted agent တစ်ခု ဖန်တီးပါ | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | ညွှန်ကြားချက်များနှင့် ပတ်ဝန်းကျင် စီမံချက်များ ပြင်ဆင်ပါ | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | ဒေသတွင်း စမ်းသပ်ပါ | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundry သို့ တင်ပို့ပါ | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Playground တွင် အတည်ပြုပါ | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | ပြဿနာဖြေရှင်းခြင်း | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Multi-Agent Workflow ([အပြည့်အစုံ ညွှန်ကြားမှုများ](workshop/lab02-multi-agent/README.md))

| # | Module | Link |
|---|--------|------|
| 1 | ရှေ့ပြေးလိုအပ်ချက်များ (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | multi-agent ပုံစံကို နားလည်ပါ | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | multi-agent project ကို scaffold လုပ်ပါ | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | agents များနှင့် ပတ်ဝန်းကျင် မူလတိုင်များကို စီမံပေးပါ | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Orchestration ပုံစံများ | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | ဒေသတွင်း စမ်းသပ်ပါ (multi-agent) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Foundry သို့ တင်သွင်းခြင်း | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | playground တွင် စစ်ဆေးခြင်း | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | ပြဿနာဖြေရှင်းခြင်း (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## ထိန်းသိမ်းသူ

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

## လိုအပ်သော အခွင့်အရေးများ (အမြန်ပြန်ကြားမှု)

| ဇာတ်ကောင် | လိုအပ်သော တာဝန်များ |
|----------|---------------|
| Foundry ပရောဂျက် အသစ် ဖန်တီးခြင်း | Foundry အရင်းအမြစ်ပေါ်တွင် **Azure AI Owner** |
| ရှိပြီးသားပရောဂျက် သို့ တင်သွင်းခြင်း (အရင်းအမြစ်အသစ်များ) | စာရင်းသွင်းမှုပေါ်တွင် **Azure AI Owner** + **Contributor** |
| ပြီးပြည့်စုံစွာ ပြင်ဆင်ထားသော ပရောဂျက် သို့ တင်သွင်းခြင်း | အကောင့်ပေါ်တွင် **Reader** + ပရောဂျက်ပေါ်တွင် **Azure AI User** |

> **အရေးကြီးချက်:** Azure `Owner` နှင့် `Contributor` တာဝန်များတွင် *စီမံခန့်ခွဲမှု* အခွင့်အရေးများသာ ပါဝင်၍ *ဖွံ့ဖြိုးရေး* (ဒေတာ လုပ်ဆောင်ချက်) အခွင့်အရေး မပါဝင်ပါ။ Agent များ တည်ဆောက်ပြီး တင်သွင်းရန်အတွက် **Azure AI User** သို့မဟုတ် **Azure AI Owner** လိုအပ်ပါသည်။

---

## ကိုးကားချက်များ

- [Quickstart: သင့်ပထမဆုံး hosted agent တင်သွင်းခြင်း (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [hosted agents ဆိုသည်မှာ?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS Code တွင် hosted agent workflow ဖန်တီးခြင်း](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [hosted agent တင်သွင်းခြင်း](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry အတွက် RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Architecture Review Agent နမူနာ](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP tools, Excalidraw diagrams နှင့် နှစ်ထပ်တင်သွင်းမှု ပါဝင်သည့် လက်တွေ့ hosted agent

---


## အာမခံချက်

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ပြောကြားချက်**
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းနေသော်လည်း၊ စက်ကိရိယာဘာသာပြန်ခြင်းများတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် လိုအပ်ပါသည်။ မူလစာတမ်းကို မူရင်းဘာသာဖြင့်သာ ယုံကြည်စိတ်ချရသော အချက်အလက်အဖြစ် သတ်မှတ်သင့်သည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုကွာခြားမှုများ သို့မဟုတ် မမှန်ကန်သော အသုံးပြုမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မခံပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->