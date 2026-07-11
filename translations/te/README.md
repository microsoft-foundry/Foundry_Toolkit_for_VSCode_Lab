# Foundry Toolkit + Foundry Hosted Agents కార్యశాల

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

**Microsoft Foundry Agent Service**‌కి **Hosted Agents**గా AI ఏజెంట్లను సృష్టించండి, పరీక్షించండి మరియు పంపండి - **Microsoft Foundry ఎక్స్‌టెన్షన్** మరియు **Foundry Toolkit** ఉపయోగించి పూర్తిగా VS Code నుండి.

> **Hosted Agents ప్రస్తుతానికి ప్రీవ్యూ‌లో ఉన్నాయి.** మద్దతు పొందిన ప్రాంతాలు పరిమితంగా ఉన్నాయి - [ప్రాంత అందుబాటు](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) చూడండి.

> ప్రతి ల్యాబ్‌లోని `agent/` ఫోల్డర్ **Foundry ఎక్స్‌టెన్షన్ ద్వారా ఆటోమేటిక్‌గా నిర్మించబడుతుంది** - మీరు ఆపై కోడ్‌ను అనుకూలీకరించండి, స్థానికంగా పరీక్షించండి, మరియు పంపండి.

### 🌐 బహుళ-భాషా మద్దతు

#### గిట్‌హబ్ యాక్షన్ ద్వారా మద్దతు ([ఆటోమేటెడ్ & ఎప్పుడూ నవీకరణಗೊಂಡది](https://github.com))

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](./README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **స్థానికంగా క్లోన్ చేయాలని ఇష్టమా?**
>
> ఈ రిపోజిటరీ 50+ భాషా అనువాదాలను కలిగి ఉందని దాని డౌన్‌లోడ్ పరిమాణాన్ని గణనీయంగా పెంచుతుంది. అనువాదాలు లేకుండా క్లోన్ చేయాలంటే, స్పార్స్ చెకౌట్ను ఉపయోగించండి:
>
> **బాష్ / మాక్‌ఓఎస్ / లినక్స్:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **సీఎండీ (విండోస్):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> దీని ద్వారా మీరు కోర్సును పూర్తి చేయడానికి అవసరమైన అన్ని విషయాలను తక్కువ డౌన్లోడ్ వేగంతో పొందుతారు.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## నిర్మాణ శాస్త్రం

```mermaid
flowchart TB
    subgraph Local["స్థానిక అభివృద్ధి (VS కోడ్)"]
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
        Scaffold -- "F5 డీబగ్" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["మైక్రోసాఫ్ట్ ఫౌండ్రీ"]
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
    (localhost:8088)" --> స్కాఫోల్
    Playground -- "టెస్ట్ ప్రాంప్ట్స్" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**ఫ్లో:** Foundry ఎక్స్‌టెన్షన్ ఏజెంట్‌ను స్కాఫోల్డ్ చేస్తుంది → మీరు కోడ్ & సూచనలను అనుకూలం చేస్తారు → Agent Inspectorతో స్థానికంగా పరీక్షించండి → Foundryకి పంపండి (డాకర్ ఇమేజ్ ACRకి పుష్ చేయబడుతుంది) → ప్లేగ్రౌండ్‌లో ధృవీకరించండి.

---

## మీరు ఏది నిర్మించబోతున్నారు

| ల్యాబ్ | వివరణ | స్థితి |
|-----|-------------|--------|
| **ల్యాబ్ 01 - సింగిల్ ఏజెంట్** | **"Explain Like I'm an Executive" ఏజెంట్**ను నిర్మించి, స్థానికంగా పరీక్షించి, Foundryకి పంపండి | ✅ అందుబాటులో ఉంది |
| **ల్యాబ్ 02 - మల్టీ-ఏజెంట్ వర్క్‌ఫ్లో** | **"Resume → Job Fit Evaluator"** నిర్మించండి - 4 ఏజెంట్లు కలిసి రిజ్యూమ్ ఫిట్‌ను స్కోర్ చేసి, లెర్నింగ్ రోడ్‌మాప్‌ను రూపొందిస్తారు | ✅ అందుబాటులో ఉంది |

---

## ఎగ్జిక్యూటివ్ ఏజెంట్‌తో పరిచయం

ఈ కార్యశాలలో మీరు **"Explain Like I'm an Executive" ఏజెంట్**ను నిర్మిస్తారు - ఒక AI ఏజెంట్ ఇది క్లిష్టమైన సాంకేతిక పదజాలాన్ని తీసుకుని, శాంతమైన, బోర్డ్రూమ్-తయారైన సారాంశాలుగా అనువదిస్తుంది. నిజం చెప్పాలంటే, C-సూట్‌లో ఎవరికీ "v3.2లో పరిచయం చేసిన సమకలిత కాల్స్ కారణంగా థ్రెడ్ పూల్ ఎగ్జాస్ట్‌షన్" గురించి వినడం ఇష్టం ఉండదు.

నేను ఈ ఏజెంట్‌ని సృష్టించాను ఎందుకంటే నా బాగా రూపొందించిన పోస్ట్‌మార్టెమ్‌కు చాల సార్లు ప్రతిస్పందన *"అంటే... వెబ్‌సైట్ డౌన్ అయిందా లేదా?"* వచ్చింది.

### ఇది ఎలా పనిచేస్తుంది

మీరు ఒక సాంకేతిక అప్డేట్ ఇస్తారు. ఇది మూడు బుల్లెట్ పాయింట్లలో ఎగ్జిక్యూటివ్ సారాంశాన్ని ఇస్తుంది - చర్చాత్మక పదాలు లేవు, స్టాక్ ట్రేస్‌లు లేవు, ఎగ్జిస్టెన్షియల్ భయాలు లేవు. కేవలం **ఏమి జరిగింది**, **వ్యాపార ప్రభావం**, మరియు **తదుపరి చర్య**.

### దాని కార్యకలాపం చూడండి

**మీరు అంటారు:**
> "API లాటెన్సీ v3.2లో పరిచయం చేసిన సమకలిత కాల్స్ కారణంగా థ్రెడ్ పూల్ ఎగ్జాస్ట్‌షన్ వల్ల పెరిగింది."

**ఏజెంట్ స్పందిస్తుంది:**

> **ఎగ్జిక్యూటివ్ సారాంశం:**
> - **ఏమి జరిగింది:** తాజా విడుదల తరువాత, సిస్టమ్ నిబంధించబడింది.
> - **వ్యాపార ప్రభావం:** కొంతమంది వినియోగదారులు సేవ వినియోగ సమయంలో ఆలస్యం అనుభవించారు.
> - **తదుపరి చర్య:** మార్పు రద్దు చేయబడింది మరియు మరోసారి పంపే ముందు ఫిక్స్ సిద్ధం అవుతుంది.

### ఈ ఏజెంట్ ఎందుకు?

ఇది ఒక చిత్తశుద్ధితో నింపబడిన, ఒకే ఉపయోగం గల ఏజెంట్ - Hosted Agent వర్క్‌ఫ్లోను పూర్తిగా అర్థం చేసుకోవడానికి మంచి. నిజం చెప్పాలంటే? ప్రతి ఇంజనీరింగ్ జట్టు ఇలాంటి ఏజెంట్ అవసరం.

---

## కార్యశాల నిర్మాణం

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

> **గమనిక:** ప్రతి ల్యాబ్‌లోని `agent/` ఫోల్డర్ **Microsoft Foundry ఎక్స్‌టెన్షన్** ద్వారా పుట్టించబడుతుంది, మీరు కمان్డ్ పలెట్ నుండి `Microsoft Foundry: Create a New Hosted Agent`ని నడిపినపుడు. ఫైళ్లను తరువాత మీరు ఏజెంట్ సూచనలు, టూల్స్ మరియు సంఘటనతో అనుకూలం చేస్తారు. ల్యాబ్ 01 ఈ ప్రక్రియను తొలుత ప్రారంభ తెలుపుతుంది.

---

## ప్రారంభించండి

### 1. రిపోజిటరీని క్లోన్ చేయండి

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. పైథాన్ వర్చువల్ వాతావరణం సెటప్ చేయండి

```bash
python -m venv venv
```

యాక్టివేట్ చేయండి:

- **విండోస్ (పవర్‌షెల్):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **మాక్‌ఓఎస్ / లినక్స్:**
  ```bash
  source venv/bin/activate
  ```

### 3. ఆధారాలు ఇన్‌స్టాల్ చేయండి

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. వాతావరణ చట్రాలు కాఫీగా సెట్ చేయండి

ఏజెంట్ ఫోల్డర్లోనుండి ఉదాహరణ `.env` ఫైల్‌ని కాపీ చేసి మీ విలువలను పూరించండి:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env`ను ఎడిట్ చేయండి:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. కార్యశాల ల్యాబ్‌లను అనుసరించండి

ప్రతి ల్యాబ్ స్వయంపరిపూర్ణంగా మాడ్యూల్లతో ఉంటుంది. ప్రాథమికాలు నేర్చుకోవడానికి **ల్యాబ్ 01**తో ప్రారంభించి, తరువాత బహుళ-ఏజెంట్ వర్క్‌ఫ్లో కోసం **ల్యాబ్ 02**కి వెళ్లండి.

#### ల్యాబ్ 01 - సింగిల్ ఏజెంట్ ([సంపూర్ణ సూచనలు](workshop/lab01-single-agent/README.md))

| # | మాడ్యూల్ | లింక్ |
|---|--------|------|
| 1 | అవసరాలు చదవండి | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry ఎక్స్‌టెన్షన్ ఇన్‌స్టాల్ చేయండి | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry ప్రాజెక్ట్ సృష్టించండి | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Hosted Agent సృష్టించండి | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | సూచనలు & వాతావరణం కాన్ఫిగర్ చేయండి | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | స్థానికంగా పరీక్షించండి | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundryకి పంపండి | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | ప్లేగ్రౌండ్‌లో ధృవీకరించండి | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | సమస్యలు పరిష్కరించు | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### ల్యాబ్ 02 - మల్టీ-ఏజెంట్ వర్క్‌ఫ్లో ([సంపూర్ణ సూచనలు](workshop/lab02-multi-agent/README.md))

| # | మాడ్యూల్ | లింక్ |
|---|--------|------|
| 1 | అవసరాలు (ల్యాబ్ 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | బహుళ-ఏజెంట్ నిర్మాణం అర్థం చేసుకోండి | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | బహుళ-ఏజెంట్ ప్రాజెక్ట్ స్కాఫోల్డ్ చేయండి | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | ఏజెంట్లు & వాతావరణం కాన్ఫిగర్ చేయండి | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | ఆర్కెస్ట్రేషన్ తేడాలు | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | స్థానికంగా పరీక్షించండి (బహుళ-ఏజెంట్) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Foundryకి పంపండి | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | ప్లేగ్రౌండ్‌లో గుర్తించండి | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | సమస్య పరిష్కారం (బహుళ ఏజెంట్లు) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## నిర్వహకుడు

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>శివం గోయెల్</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## అవసరమైన అనుమతులు (త్వరిత సూచన)

| సన్నివేశం | అవసరమైన పాత్రలు |
|----------|---------------|
| కొత్త Foundry ప్రాజెక్ట్ సృష్టించండి | Foundry వనరుపై **Azure AI యజమాని** |
| ఉన్న ప్రాజెక్ట్‌కు పంపండి (కొత్త వనరులు) | సబ్‌స్క్రిప్షన్‌పై **Azure AI యజమాని** + **కాంట్రిబ్యూటర్** |
| పూర్తిగా అమర్చిన ప్రాజెక్ట్‌కు పంపండి | ఖాతాపై **Reader** + ప్రాజెక్ట్‌పై **Azure AI వినియోగదారు** |

> **గమనిక:** Azure `Owner` మరియు `Contributor` పాత్రలు *నిర్వాహణ* అనుమతులను మాత్రమే కలిగి ఉంటాయి, *వికాసం* (డేటా చర్య) అనుమతులు కలిగి ఉండవు. ఏజెంట్లను నిర్మించడానికి మరియు పంపిణీ చేయడానికి **Azure AI వినియోగదారు** లేదా **Azure AI యజమాని** ఆవশ্যకం.

---

## సూచనలు

- [త్వరిత ప్రారంభం: మీ మొదటి హోస్టెడ్ ఏజెంట్‌ను పంపండి (VS కోడ్)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [హోస్టెడ్ ఏజెంట్లు ఏమిటి?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS కోడ్‌లో హోస్టెడ్ ఏజెంట్ వర్క్‌ఫ్లోలను సృష్టించండి](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [హోస్టెడ్ ఏజెంట్‌ను పంపండి](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry కోసం RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [ఆర్కిటెక్చర్ రివ్యూ ఏజెంట్ నమూనా](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP పరికరాలు, Excalidraw చిత్రాలు, మరియు ద్విభాగ పంపకం కలిగిన వాస్తవ ప్రపంచ హోస్టెడ్ ఏజెంట్

---


## లైసెన్స్

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్వీకరణ**:
ఈ పత్రం AI అనువాద సేవ [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నిస్తున్నప్పటికీ, ఆటోమేటెడ్ అనువాదాలు తప్పులు లేదా అసమగ్రతలను కలిగి ఉండవచ్చు. దాని స్వదేశ భాషలో ఉన్న అసలు పత్రాన్ని అధికారం కలిగిన మూలంగా పరిగణించాలి. కీలకమైన సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదాన్ని సిఫారసు చేస్తాము. ఈ అనువాదం ఉపయోగం వల్ల కలిగే ఏవైనా అపార్థాలు లేదా తప్పుదారులు కోసం మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->