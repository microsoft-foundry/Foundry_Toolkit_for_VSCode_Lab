# Foundry Toolkit + Foundry Hosted Agents Workshop

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/agent-framework/)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Bumuo, subukan, at i-deploy ang mga AI agent sa **Microsoft Foundry Agent Service** bilang **Hosted Agents** - nang buo mula sa VS Code gamit ang **Microsoft Foundry extension** at **Foundry Toolkit**.

> **Ang Hosted Agents ay kasalukuyang nasa preview.** Limitado ang mga suportadong rehiyon - tingnan ang [region availability](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Ang folder na `agent/` sa bawat lab ay **awtomatikong ginagawa** ng Foundry extension - pagkatapos ay i-customize mo ang code, subukan lokal, at i-deploy.

### 🌐 Suporta sa Iba't Ibang Wika

#### Sinusuportahan sa pamamagitan ng GitHub Action (Automated at Palaging Napapanahon)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](./README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Mas gustong mag-clone nang lokal?**
>
> Kasama sa repository na ito ang 50+ na salin sa mga wika na malaki ang dagdag sa laki ng pag-download. Para mag-clone nang wala ang mga salin, gamitin ang sparse checkout:
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
> Ito ang magbibigay sa iyo ng lahat ng kailangan para matapos ang kurso nang mas mabilis ang pag-download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arkitektura

```mermaid
flowchart TB
    subgraph Local["Local Development (VS Code)"]
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
        Scaffold -- "F5 Debug" --> Inspector
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
    (localhost:8088)" --> Scaffold
    Playground -- "Test prompts" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Daloy:** Ginagawa ng Foundry extension ang scaffolding ng agent → i-customize mo ang code at mga tagubilin → subukan lokal gamit ang Agent Inspector → i-deploy sa Foundry (Docker image naipush sa ACR) → beripikahin sa Playground.

---

## Ano ang iyong bubuuin

| Lab | Paglalarawan | Katayuan |
|-----|-------------|--------|
| **Lab 01 - Isang Agent** | Bumuo ng **"Explain Like I'm an Executive" Agent**, subukan ito lokal, at i-deploy sa Foundry | ✅ Available |
| **Lab 02 - Multi-Agent Workflow** | Bumuo ng **"Resume → Job Fit Evaluator"** - nagtutulungan ang 4 na agent para i-score ang resume fit at gumawa ng learning roadmap | ✅ Available |

---

## Kilalanin ang Executive Agent

Sa workshop na ito bibuuin mo ang **"Explain Like I'm an Executive" Agent** - isang AI agent na kinukuha ang mahirap na teknikal na jargon at isinasalin ito sa malinaw, handang ipresentang mga buod para sa boardroom. Kasi sa totoo lang, walang gustong makinig sa C-suite tungkol sa "thread pool exhaustion caused by synchronous calls introduced in v3.2."

Binuo ko ang agent na ito matapos ang ilang insidente kung saan ang aking maayos na post-mortem ay tinugon ng: *"So... website ba ay down o hindi?"*

### Paano ito gumagana

Bibigyan mo ito ng teknikal na update. Babalik ito ng executive summary - tatlong punto lang, walang jargon, walang stack traces, walang nakakakilabot na pakiramdam. Ang sagot lang ay **ano ang nangyari**, **epekto sa negosyo**, at **susunod na hakbang**.

### Tingnan ito na kumikilos

**Sinasabi mo:**
> "The API latency increased due to thread pool exhaustion caused by synchronous calls introduced in v3.2."

**Sagot ng agent:**

> **Executive Summary:**
> - **Ano ang nangyari:** Pagkatapos ng pinakabagong release, bumagal ang sistema.
> - **Epekto sa negosyo:** Ang ilang mga user ay nakaranas ng pagkaantala habang ginagamit ang serbisyo.
> - **Susunod na hakbang:** Ang pagbabago ay na-rollback na at naghahanda ng ayos bago muling i-deploy.

### Bakit ang agent na ito?

Isa itong napakadaling, single-purpose na agent - perpekto para matutunan ang hosted agent workflow mula simula hanggang dulo nang hindi nahihirapan sa komplikadong tool chains. At sa totoo lang? Bawat engineering team ay pwedeng magkaroon nito.

---

## Istruktura ng Workshop

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
        │   ├── 08-troubleshooting.md
        │   └── 09-summary.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **Tandaan:** Ang `agent/` folder sa bawat lab ay ginagawa ng **Microsoft Foundry extension** kapag pinatakbo mo ang `Microsoft Foundry: Create a New Hosted Agent` mula sa Command Palette. Ang mga file dito ay sine-customize gamit ang mga tagubilin, mga tool, at config ng iyong agent. Tinatahak ng Lab 01 ang pagbuo nito mula sa simula.

---

## Pagsisimula

### 1. I-clone ang repository

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Mag-setup ng Python virtual environment

```bash
python -m venv venv
```

I-activate ito:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Mag-install ng mga dependency

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. I-configure ang mga environment variables

Kopyahin ang halimbawa ng `.env` file sa loob ng agent folder at punan ang mga halaga:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

I-edit ang `workshop/lab01-single-agent/agent/.env`:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Sundin ang mga workshop lab

Bawat lab ay may sariling mga module. Magsimula sa **Lab 01** para matutunan ang mga pundasyon, pagkatapos ay pumunta sa **Lab 02** para sa multi-agent workflows.

#### Lab 01 - Isang Agent ([full instructions](workshop/lab01-single-agent/README.md))

| # | Module | Link |
|---|--------|------|
| 1 | Basahin ang mga prerequisites | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | I-install ang Foundry Toolkit & Foundry extension | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Gumawa ng Foundry project | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Gumawa ng hosted agent | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | I-configure ang mga tagubilin & environment | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Subukan lokal | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | I-deploy sa Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Beripikahin sa playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Buod & susunod na mga hakbang | [07-summary.md](workshop/lab01-single-agent/docs/07-summary.md) |
| 10 | Pag-troubleshoot | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Multi-Agent Workflow ([full instructions](workshop/lab02-multi-agent/README.md))

| # | Module | Link |
|---|--------|------|
| 1 | Mga Panimulang Kaalaman (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Unawain ang multi-agent architecture | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Gumawa ng scaffold para sa multi-agent project | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | I-configure ang mga agent & environment | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Mga pattern ng orchestration | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Subukan lokal (multi-agent) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | I-deploy sa Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Beripikahin sa playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Pag-troubleshoot (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |
| 10 | Buod & susunod na mga hakbang | [09-summary.md](workshop/lab02-multi-agent/docs/09-summary.md) |

---

## Tagapangalaga

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

## Kinakailangang permiso (mabilisang sanggunian)

| Senaryo | Kinakailangang mga tungkulin |
|----------|---------------|
| Gumawa ng bagong Foundry project | **Azure AI Owner** sa Foundry resource |
| Mag-deploy sa umiiral na proyekto (mga bagong resources) | **Azure AI Owner** + **Contributor** sa subscription |
| Mag-deploy sa ganap na naka-configure na proyekto | **Reader** sa account + **Azure AI User** sa proyekto |

> **Mahalaga:** Ang mga Azure `Owner` at `Contributor` na mga papel ay naglalaman lamang ng mga *pamamahala* na pahintulot, hindi *pag-unlad* (data action) na mga pahintulot. Kailangan mo ng **Azure AI User** o **Azure AI Owner** upang makabuo at makapag-deploy ng mga ahente.

---

## Mga Sanggunian

- [Mabilisang Simula: I-deploy ang iyong unang hosted agent (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Ano ang mga hosted agent?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Lumikha ng mga workflow ng hosted agent sa VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [I-deploy ang isang hosted agent](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC para sa Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Architecture Review Agent Sample](https://github.com/Azure-Samples/agent-architecture-review-sample) - Totoong hosted agent na may MCP tools, Excalidraw diagrams, at dobleng deployment

---


## Lisensya

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->