# ഫൗണ്ട്രി ടൂൾകിറ്റ് + ഫൗണ്ട്രി ഹോസ്റ്റഡ് ഏജന്റ്സ് വർക്‌ഷോപ്പ്

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

എ.ഐ. ഏജന്റുകൾ **Microsoft Foundry Agent Service** ലേക്ക് **Hosted Agents** ആയി നിർമ്മിക്കുക, പരീക്ഷിക്കുക, വിന്യസിപ്പിക്കുക — പൂര്‍ണമായും VS കോഡ് ഉപയോഗിച്ച് **Microsoft Foundry extension**-ഉം **Foundry Toolkit**-ഉം ഉപയോഗിച്ച്.

> **Hosted Agents എപ്പോഴും പ്രിവ്യൂയിൽ ആണ്.** പിന്തുണയുള്ള മേഖലയെ കുറിച്ചുള്ള വിശദാംശങ്ങൾക്കായി [region availability](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) കാണുക.

> ഓരോ ലാബിനും ഉള്ള `agent/` ഫോൾഡർ **Foundry extension** ഉപയോഗിച്ച് **സ്വയം സ്കാഫോൾഡ്** ചെയ്യുന്നു - പിന്നീട് നിങ്ങൾ കോഡ് തിരുത്തി, ലൊക്കലായി പരിശോധന നടത്തി, വിന്യസിപ്പിക്കാം.

### 🌐 ബഹു-ഭാഷാ പിന്തുണ

#### GitHub ആക്ഷൻ വഴി പിന്തുണ (സ്വയംകരിച്ചും എപ്പോഴുമുള്ള അപ്‌ഡേറ്റുമായും)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](./README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **സ്റ്റോറേജ് ലൊക്കലായി ക്ലോൺ ചെയ്യാൻ ആഗ്രഹിക്കുന്നോ?**
>
> ഈ റിപ്പോസിറ്ററിയിൽ 50-ത്തിലധികം ഭാഷാ വിവർത്തനങ്ങൾ ഉൾക്കൊള്ളുന്നു, ഇത് ഡൗൺലോഡ് വലുപ്പം ഏറെ വർധിപ്പിക്കുന്നു. വിവർത്തനങ്ങൾ കൂടാതെ ക്ലോൺ ചെയ്യാൻ, sparse checkout ഉപയോഗിക്കുക:
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
> ഇത് കോഴ്സ് പൂർത്തിയാക്കാൻ ആവശ്യമായ എല്ലാ ഫയലുകളും വേഗത്തിൽ ഡൗൺലോഡ് ചെയ്യാൻ സഹായിക്കുന്നു.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## ആർക്കിടെക്ചർ

```mermaid
flowchart TB
    subgraph Local["പ്രാദേശിക ഡെവലപ്പ്മെന്റ് (VS കോഡ്)"]
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
        Scaffold -- "F5 ഡീബഗ്" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["മൈക്രോസോഫ്റ്റ് ഫൗണ്ട്‌റി"]
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
    (localhost:8088)" --> സ്‌കാഫോൾഡ്
    Playground -- "ടെസ്റ്റ് പ്രോംപ്റ്റുകൾ" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**പ്രവാഹം:** ഫൗണ്ട്രി എക്സ്റ്റൻഷൻ ഏജന്റ് സ്കാഫോൾഡ് ചെയ്യുന്നു → നിങ്ങൾ കോഡ് & നിർദ്ദേശങ്ങൾ ഇഷ്ടാനുസൃതമാക്കുന്നു → Agent Inspector ഉപയോഗിച്ച് നീക്കം പരിശോധിക്കുന്നു → ഫൗണ്ട്രിയിലേക്ക് വിന്യസിക്കുന്നു (Docker ഇമേജ് ACR-ലേക്ക് പുഷ് ചെയ്യുന്നു) → പ്ലേഗ്രൗണ്ടിൽ സ്ഥിരീകരിക്കുന്നു.

---

## നിങ്ങൾ നിർമ്മിക്കാനുള്ളത്

| ലാബ് | വിശദവിവരം | നില |
|-----|-------------|--------|
| **ലാബ് 01 - സിംഗിൾ ഏജന്റ്** | **"Explain Like I'm an Executive" Agent** നിർമ്മിക്കുക, ലൊക്കലായി പരീക്ഷിച്ച് ഫൗണ്ട്രിയിലേക്ക് വിന്യസിക്കുക | ✅ ലഭ്യമാണ് |
| **ലാബ് 02 - മൾട്ടി-ഏജന്റ് വർക്ക്‌ഫ്ലോ** | **"Resume → Job Fit Evaluator"** - 4 ഏജന്റുകൾ ചേർന്ന് റിസ്യൂമെയുടെ യോജ്യത സ്കോർ ചെയ്ത് പഠന പദ്ധതിയുടെ റോഡ്‌మാപ്പ് സൃഷ്ടിക്കും | ✅ ലഭ്യമാണ് |

---

## എക്സിക്യൂട്ടീവ് ഏജന്റിനെ പരിചയപ്പെടുക

ഈ വർക്‌ഷോപ്പിൽ നിങ്ങൾ നിർമ്മിക്കുന്നതാണ് **"Explain Like I'm an Executive" Agent** — നിഴലുള്ള സാങ്കേതിക പദങ്ങൾ ശാന്തമായ, ബോർഡ്‌റൂം-സജ്ജമായ സർവിണികളുടെ രൂപത്തിൽ വിവർത്തനം ചെയ്യുന്നത്. സത്യം പറയുമ്പോൾ, C-സ്‌യൂടിൽ ആരും "തന്തു പൂളിന്റെ ക്ഷീണം മൂലം API ലാറ്റൻസി വർദ്ധിച്ചു" എന്ന് കേൾക്കാൻ ആഗ്രഹിക്കുന്നില്ല.

ഒരു പകൃതിയായി ഞാൻ ഈ ഏജന്റ് നിർമ്മിച്ചു, എപ്പോൾ എങ്കിലും എന്റെ നന്നായി തയ്യാറാക്കിയ പോസ്റ്റ്-മോർട്ടം കിട്ടിയത് അതുപോലെയുള്ള പ്രതികരണമായി: *"അതായത്... വെബ്സൈറ്റ് താഴെയോ അല്ലയോ?"*

### ഇത് എങ്ങനെ പ്രവർത്തിക്കുന്നു

നിങ്ങൾക്ക് സാങ്കേതിക അപ്‌ഡേറ്റ് നൽകുക. അത് നിങ്ങളെക്കായി ഒരു എക്സിക്യൂട്ടീവ് സാരാംശം നൽകും - മൂന്ന് ബുള്ളറ്റ് പോയിന്റുകൾ, jargon ഇല്ല, സ്റ്റാക്ക് ട്രേസുകൾ ഇല്ല, ഭയം ഇല്ല. വെറും **കുറ്റം സംഭവിച്ചത്**, **ബിസിനസ് സ്വാധീനം**, **അടുത്ത പടി**.

### പ്രവർത്തനത്തിൽ കാണുക

**നിങ്ങൾ പറയുന്നു:**
> "The API latency increased due to thread pool exhaustion caused by synchronous calls introduced in v3.2."

**ഏജന്റ് മറുപടി:**

> **എക്സിക്യൂട്ടീവ് സാരാംശം:**
> - **എന്ത് സംഭവിച്ചു:** ഏറ്റവും പുതിയ റിലീസ് ശേഷം, സിസ്റ്റം മന്ദഗതിയിൽ ആയി.
> - **ബിസിനസ് സ്വാധീനം:** ചില ഉപയോക്താക്കൾ സേവനം ഉപയോഗിക്കുന്ന സമയത്ത് വൈകിപ്പോവുകൾ അനുഭവപ്പെട്ടു.
> - **അടുത്ത പടി:** മാറ്റം റോള്ബാക്ക് ചെയ്തു, പുതുക്കലിനുമുമ്പായി പരിഹാരമൊരുങ്ങുകയാണ്.

### ഈ ഏജന്റ് എന്തിനായി?

ഇത് ഒരുപാട് ലളിതമായ, ഒറ്റ ശ്രമ-Agent ആണ് — ഹോസ്റ്റഡ് ഏജന്റ് വർക്ക്‌ഫ്ലോ പൂർണമായി പഠിക്കാൻ ഉചിതം, സങ്കീർണമായ ടൂൾ ചെയിൻസിൽ കുടുങ്ങാതെ. സത്യമായി, ഓരോ എഞ്ചിനീയറിങ്ങ് ടീമും ഇതിൽ ഒന്ന് ഉപയോഗിക്കണം.

---

## വർക്‌ഷോപ്പ് ഘടന

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

> **Note:** ഓരോ ലാബിനും ഉള്ള `agent/` ഫോൾഡർ **Microsoft Foundry extension** ഉപയോഗിച്ച് നിങ്ങൾ കമാൻഡ് പാറലെറ്റ് വഴി `Microsoft Foundry: Create a New Hosted Agent` ഓടിക്കുമ്പോൾ സൃഷ്ടിക്കുന്നതാണ്. തുടർന്ന് വാഹകത്തിന്റെ നിർദ്ദേശങ്ങൾ, ടൂളുകൾ, കോൺഫിഗറേഷൻ എന്നിവ ഉൾപ്പെടുത്തി ഫയലുകൾ ഇഷ്ടാനുസൃതമാക്കും. ലാബ് 01 നിങ്ങൾക്ക് ഇത് ശൂന്യം മുതൽ സൃഷ്ടിക്കാനായി നടപടിക്രമങ്ങൾ നൽകുന്നു.

---

## തുടങ്ങൽ

### 1. റിപ്പോസിറ്ററി ക്ലോൺ ചെയ്യുക

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Python വിർച്വൽ എൻവയിർമെന്റ് സജ്ജമാക്കുക

```bash
python -m venv venv
```

ആക്റ്റിവേറ്റ് ചെയ്യുക:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. ഡിപ്പെൻഡൻസികൾ ഇൻസ്റ്റാൾ ചെയ്യുക

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. എൻവയിർമെന്റ് വെറിയബിൾസ് കോൺഫിഗർ ചെയ്യുക

ഏജന്റ് ഫോൾഡറിൽ ഉള്ള ഉദാഹരണമായ `.env` ഫയൽ നൽകും, നിങ്ങളുടെ മൂല്യങ്ങൾ അവിടെ ഫിൽ ചെയ്യുക:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` എഡിറ്റ് ചെയ്യുക:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. വർക്‌ഷോപ്പ് ലാബുകൾ പിന്തുടരുക

ഓരോ ലാബും സ്വതന്ത്രമായ മൊഡ്യൂളുകളോടെയാണ്. അടിസ്ഥാനങ്ങൾ പഠിക്കാൻ ആദ്യം **Lab 01** ആരംഭിക്കുക, പിന്നീട് മൾട്ടി-ഏജന്റ് വർക്ക്‌ഫ്ലോകളെക്കുറിച്ച് **Lab 02** ആശയങ്ങൾ നൽകുന്നു.

#### Lab 01 - Single Agent ([പൂർണ്ണ നിർദ്ദേശങ്ങൾ](workshop/lab01-single-agent/README.md))

| # | മോഡ്യൂൾ | ലിങ്ക് |
|---|--------|------|
| 1 | മുൻ‌കൂട്ടി പോരായ്മകൾ വായിക്കുക | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry extension ഇൻസ്റ്റാൾ ചെയ്യുക | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry പ്രൊജക്ട് സൃഷ്ടിക്കുക | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | ഹോസ്റ്റഡ് ഏജന്റ് സൃഷ്ടിക്കുക | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | നിർദ്ദേശങ്ങൾ & എൻവയിർമെന്റ് കോൺഫിഗർ ചെയ്യുക | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | ലൊക്കലായി ടെസ്റ്റ് ചെയ്യുക | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | ഫൗണ്ട്രിയിലേക്ക് വിന്യസിക്കുക | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | പ്ലേഗ്രൗണ്ടിൽ പരിശോധന നടത്തുക | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | പ്രശ്നപരിഹാരം | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Multi-Agent Workflow ([പൂർണ്ണ നിർദ്ദേശങ്ങൾ](workshop/lab02-multi-agent/README.md))

| # | മോഡ്യൂൾ | ലിങ്ക് |
|---|--------|------|
| 1 | മുൻ‌കൂട്ടി പരി‌ശോധനകൾ (ലാബ് 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | മൾട്ടി-ഏജന്റ് ആർക്കിടെക്ചർ മനസ്സിലാക്കുക | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | മൾട്ടി-ഏജന്റ് പ്രൊജക്ട് സ്കാഫോൾഡ് ചെയ്യുക | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | ഏജന്റുകളും എൻവയിർമെന്റും കോൺഫിഗർ ചെയ്യുക | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | ഓർക്കസ്ട്രേഷൻ പാറ്റേണുകൾ | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | ലൊക്കലായി പരീക്ഷിക്കുക (മൾട്ടി-ഏജന്റ്) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | ഫൗണ്ടറിയിലേക്ക് വിന്യസിക്കുക | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | പ്ലേഗ്രൗണ്ടിൽ പരിശോദിക്കുക | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | പ്രശ്നപരിഹാരം (മൾටි-ഏജന്റ്) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## പരിപാലകൻ

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>ശിവം ഗോയൽ</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## ആവശ്യമുള്ള അവകാശങ്ങൾ (വേഗം കാണുവാനുള്ള സംവരണം)

| സ്ഥിതിവിവരം | ആവശ്യമായ പങ്കുവകാശങ്ങൾ |
|----------|---------------|
| പുതിയ ഫൗണ്ടറി പ്രോജക്ട് സൃഷ്ടിക്കുക | ഫൗണ്ടറി റിസോഴ്‌സിലെ **Azure AI მാലിക** |
| നിലവിലുള്ള പ്രോജക്ടിലേക്ക് വിന്യസിക്കുക (പുതിയ റിസോഴ്‌സുകൾ) | സബ്സ്ക്രിപ്ഷനിൽ **Azure AI მാലിക** + **സംഭാവനദാതാവ്** |
| പൂർണ്ണമായും ക്രമീകരിച്ച പ്രോജക്ടിലേക്ക് വിന്യസിക്കുക | അക്കൗണ്ടിലെ **വായനക്കാരൻ** + പ്രോജക്ടിലെ **Azure AI ഉപയോക്താവ്** |

> **പ്രധാനമാണ്:** Azure ൽ `മാൽിക`യും `സംഭാവനദാതാവ്`കളും *നിർമാണ* അവകാശങ്ങൾ മാത്രമേ ഉൾക്കൊള്ളൂ, *വികസന* (ഡാറ്റ പ്രവർത്തന) അവകാശങ്ങൾ അല്ല. ഏജന്റുകൾ നിർമ്മിച്ചു വിന്യസിക്കാൻ നിങ്ങൾക്ക് **Azure AI ഉപയോക്താവ്** അല്ലെങ്കിൽ **Azure AI മാലിക** ആവശ്യമുണ്ട്.

---

## സൂചനകൾ

- [ക്വിക്‌സ്റ്റാർട്ട്: നിങ്ങളുടെ ആദ്യ ഹോസ്റ്റ് ചെയ്‌തിരിക്കുന്ന ഏജന്റ് വിന്യസിക്കുക (VS കോഡ്)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [ഹോസ്റ്റ് ചെയ്‌തിരിക്കുന്ന ഏജന്റുകൾ എന്താണ്?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS കോഡിൽ ഹോസ്റ്റ് ചെയ്‌തിരിക്കുന്ന ഏജന്റ് പ്രവാഹങ്ങൾ സൃഷ്ടിക്കുക](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [ഹോസ്റ്റ് ചെയ്‌തിരിക്കുന്ന ഏജന്റ് വിന്യസിക്കുക](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry ന്റെ RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [ആർക്കിടെക്ചർ റിവ്യൂ ഏജന്റ് സാമ്പിൾ](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP ടൂൾസുകൾ, എക്സ്കാലിഡ്രോ ഡയഗ്രാമുകൾ, ഇരട്ട വിന്യാസം എന്നിവയുള്ള യഥാർത്ഥ ലോക ഹോസ്റ്റ് ചെയ്‌തിരിക്കുന്ന ഏജന്റ്

---


## ലൈസൻസ്

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**അറിയിപ്പ്**:
ഈ രേഖ AI പരിഭാഷാ സേവനം [Co-op Translator](https://github.com/Azure/co-op-translator) ഉപയോഗിച്ച് പരിഭാഷപ്പെടുത്തിയതാണ്. ഞങ്ങൾ കൃത്യതയ്ക്കായി ശ്രമിക്കുന്നുവെങ്കിലും, ഓട്ടോമേറ്റഡ് പരിഭാഷകളിൽ പിഴവുകൾ അല്ലെങ്കിൽ തെറ്റായ വിവരങ്ങൾ ഉണ്ടാകാൻ സാധ്യതയുണ്ട്. അതിന്റെ സ്വാഭാവിക ഭാഷയിലുള്ള അസൽ രേഖയാണ് പ്രാമാണികമായ ഉറവിടമായി പരിഗണിക്കേണ്ടത്. നിർണായകമായ വിവരങ്ങൾക്ക്, പ്രൊഫഷണൽ മനുഷ്യ പരിഭാഷ ശുപാർശ ചെയ്യുന്നു. ഈ പരിഭാഷ ഉപയോഗിച്ച് ഉണ്ടാകുന്ന തെറ്റിദ്ധാരണകൾ അല്ലെങ്കിൽ തെറ്റായ വ്യാഖ്യാനങ്ങൾക്കായി ഞങ്ങൾ ഉത്തരവാദികളല്ല.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->