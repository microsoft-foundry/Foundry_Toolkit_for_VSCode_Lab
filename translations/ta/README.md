# Foundry டூல்கிட் + Foundry ஹோஸ்டட் ஏஜென்டுகள் வேலைக்கூடு

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

**Microsoft Foundry Agent Service**-ல் **Hosted Agents** ஆக AI ஏஜென்டுகளை கட்டமைக்கவும், சோதிக்கவும், வெளியிடவும் - முழுகாக VS Code பயன்படுத்தி **Microsoft Foundry நீட்டிப்பு** மற்றும் **Foundry டூல்கிட்** மூலம்.

> **Hosted Agents இப்போது முன்னோட்ட நிலையில் உள்ளன.** ஆதரவு பெற்ற பிராந்தியங்கள் সীমितம் - பார்க்கவும் [region availability](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> ஒவ்வொரு ஆய்வகத்திலும் உள்ள `agent/` கோப்புறை Foundry நீட்டிப்பு மூலம் **தானாக உருவாக்கப்படுகிறது** - பின்னர் நீங்கள் குறியீட்டை தனிப்பயனாக்கி, உள்ளூர் சோதனை செய்து, வெளியிடலாம்.

### 🌐 பல மொழி ஆதரவு

#### GitHub செயல்பாட்டின் மூலம் ஆதரவு (தானியங்கி மற்றும் எப்போதும் புதுமையாக இருக்கும்)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](./README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **உள்ளூரில் கிளோன் செய்ய விரும்புமா?**
>
> இந்த சேமிப்பகத்தில் 50+ மொழி மொழிபெயர்ப்புகள் உள்ளன, இது பதிவிறக்கும் அளவை பெருக்குகிறது. மொழிபெயர்ப்புகள் இல்லாமல் கிளோன் செய்வதற்கு sparse checkout பயன்படுத்தவும்:
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
> இதனால் நீங்கள் வேகம் அதிகமான பதிவிறக்கத்தில் முழு பாடத்திட்டத்தையும் முடிக்க முடியும்.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## கட்டமைப்பு

```mermaid
flowchart TB
    subgraph Local["உள்ளூர்க் கலைவள மேம்பாடு (VS Code)"]
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
        Scaffold -- "F5 பிழைத்திருத்தம்" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["மைக்ரோசொஃப்ட் ஃபவுண்ட்ரி"]
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
    (localhost:8088)" --> அடித்தளம்
    Playground -- "சோதனை உத்தரவுகள்" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**போர்:** Foundry நீட்டிப்பு ஏஜெண்டை உருவாக்குகிறது → நீங்கள் குறியீடு மற்றும் வழிமுறைகளை தனிப்பயனாக்கும் → Agent Inspector மூலம் உள்ளூரில் சோதனை செய்கிறீர்கள் → Foundry க்கு வெளியிடுவது (Docker படம் ACR க்கு அழுத்தப்படுகிறது) → Playground ல் சரிபார்க்கவும்.

---

## நீங்கள் உருவாக்கப்போகும் விஷயம்

| ஆய்வகம் | விளக்கம் | நிலை |
|-----|-------------|--------|
| **ஆய்வகம் 01 - ஒற்றை ஏஜென்ட்** | **"எவ்வாறு தெரிவிக்கும்" தலைவர் ஏஜென்ட்** உருவாக்கி, உள்ளூர் சோதனை செய்து, Foundryக்கு வெளியிடவும் | ✅ கிடைக்கிறது |
| **ஆய்வகம் 02 - பல-ஏஜென்ட் வேலைநடை** | **"Resume → வேலை பொருத்த மதிப்பீடு"** - 4 ஏஜென்ட்கள் Resume பொருத்தத்தை மதிப்பிட்டும் கற்றல் திட்டத்தை உருவாக்கும் | ✅ கிடைக்கிறது |

---

## தலைவர் ஏஜென்டை சந்திக்கவும்

இந்நிகழ்ச்சியில் நீங்கள் **"எவ்வாறு தெரிவிக்கும்" தலைவர் ஏஜென்டை** உருவாக்கப்போகிறீர்கள் - இது திறமையான தொழில்நுட்ப சொற்றொடரை எடுக்கி, அமைதியான, வாராந்திர அறிக்கைகளுக்கு உரிய சுருக்கமாக மாற்றும் AI ஏஜென்ட். ஏனெனில் நிஜம் என்னவென்றால், C-சூட்டில் ஒருவரும் "v3.2ல் அறிமுகப்படுத்தப்பட்ட சமகால அழைப்புகளால் ஏற்பட்ட thread pool exhaustion" பற்றி கேட்க விரும்ப மாட்டார்கள்.

நான் இந்த ஏஜென்டை உருவாக்கியது என் மிகச்சிறந்த post-mortemக்கு பதில் வந்தபோது: *"எனவே... இணையதளம் பணி நிறுத்தம் ஆனதா இல்லையா?"* என்ற கேள்வியை பலமுறைகள் பெற்றுவிட்டேன்.

### அது எப்படி செயல்படுகிறது

நீங்கள் அதற்கு ஒரு தொழில்நுட்ப புதுப்பிப்பை காலி செய்கிறீர்கள். அது ஒரு தலைவர் சுருக்கத்தை வெளி கொண்டுவரும் - மூன்று புள்ளிகள், சொற்றொடர்கள் இல்லை, வழுக்கைத் திரை எதுவும் இல்லை, கவலை இல்லாமல். வெறும் **என்ன జరిగியது**, **வணிக பாதிப்பு**, மற்றும் **அடுத்த படி**.

### செயலில் காணவும்

**நீங்கள் கூறுகிறீர்கள்:**
> "API லேட்டன்சி v3.2ல் அறிமுகப்படுத்தப்பட்ட சமகால அழைப்புகளால் thread pool exhaustionஉடன் அதிகரித்தது."

**ஏஜென்ட் பதிலளிக்கிறது:**

> **தலைவர் சுருக்கம்:**
> - **என்ன நடந்தது:** சமீபத்திய வெளியீட்டுக்குப் பிறகு, அமைப்பு மெதுவாகியது.
> - **வணிக பாதிப்பு:** சில பயனர் சேவையைப் பயன்படுத்தும் போது தாமதம் ஏற்பட்டது.
> - **அடுத்த படி:** மாற்றம் திரும்பி வைப்பு செய்யப்பட்டது மற்றும் திருத்தம் தயாராகி மீண்டும் வெளியிடப்பட உள்ளது.

### இந்த ஏஜென்ட் ஏன்?

இது மிக எளிமையான, ஒரே நோக்குடைய ஏஜென்ட் - hosted agent வேலைநடையை முழுமையாகக் கற்றுக்கொள்ள மிகவும் சிறந்தது, அசிங்கமான கருவி சங்கிலிகளில் அடைக்காமல். உண்மை சொல்வதானால்? ஒவ்வொரு பொறியியல் குழுவுக்கும் இதுபோன்ற ஒன்றை வேண்டியிருக்கும்.

---

## வேலைக்கூடு அமைப்பு

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

> **குறிப்பு:** ஒவ்வொரு ஆய்வகத்திலும் உள்ள `agent/` கோப்புறை **Microsoft Foundry நீட்டிப்பு** மூலம் `Microsoft Foundry: Create a New Hosted Agent` என்பதைக் கட்டளை பட்டியலில் இயக்கு போது உருவாக்கப்படுகிறது. பின்னர் கோப்புகள் உங்கள் ஏஜென்டின் வழிமுறைகள், கருவிகள் மற்றும் அமைப்புகளுடன் தனிப்பயனாக்கப்படுகின்றன. ஆய்வகம் 01 இல் இதை முற்றிலும் மீண்டும் உருவாக்குவது எப்படி என்று காட்டப்படும்.

---

## துவக்கம்

### 1. சேமிப்புகையை கிளோன் செய்யவும்

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Python மெய்நிகர் சுற்றுப்பாதையை அமைக்கவும்

```bash
python -m venv venv
```

செயல்படுத்தவும்:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. சார்பு பொருட்களை நிறுவவும்

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. சுற்றுப்பாதை மாறிலிகளை அமைக்கவும்

உதாரண `.env` கோப்பை agent கோப்புறையில் நகல் செய்து, உங்கள் மதிப்புகளை நிரப்பவும்:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` ஐத் திருத்தவும்:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. வேலைக்கூடு ஆய்வகங்களை பின்பற்றவும்

ஒவ்வொரு ஆய்வகமும் தனித்தனிப் பொருள்களுடன் முழுமையாக உள்ளது. அடிப்படைகளை கற்றுக்கொள்ள **ஆய்வகம் 01** ஆரம்பிக்கவும், பிறகு **ஆய்வகம் 02**-க்கு மாறி பல-ஏஜென்ட் வேலைநடையை கற்றுக்கொள்ளவும்.

#### ஆய்வகம் 01 - ஒற்றை ஏஜென்ட் ([முழு வழிமுறைகள்](workshop/lab01-single-agent/README.md))

| # | பொருள் | இணைப்பு |
|---|--------|------|
| 1 | முன்னோடிய வாசல் படிக்கவும் | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry டூல்கிட் & Foundry நீட்டிப்பை நிறுவவும் | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry திட்டத்தை உருவாக்கவும் | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | ஒரு ஹோஸ்டட் ஏஜென்டை உருவாக்கவும் | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | வழிமுறைகள் & சுற்றுப்பாதைகளை அமைக்கவும் | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | உள்ளூரில் சோதனை செய்யவும் | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundryக்கு வெளியிடவும் | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | விளையாட்டு மைதானத்தில் சரிபார்க்கவும் | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | சிக்கல் நீக்குதல் | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### ஆய்வகம் 02 - பல-ஏஜென்ட் வேலைநடை ([முழு வழிமுறைகள்](workshop/lab02-multi-agent/README.md))

| # | பொருள் | இணைப்பு |
|---|--------|------|
| 1 | முன்னோடியங்கள் (ஆய்வகம் 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | பல-ஏஜென்ட் கட்டமைப்பை புரிந்து கொள்வது | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | பல-ஏஜென்ட் திட்டத்திற்கான மாடலை உருவாக்கவும் | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | ஏஜென்டுகள் & சுற்றுப்பாதைகளை அமைக்கவும் | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | ஒருங்கிணைப்பு எடுத்துக்காட்டுகள் | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | உள்ளூரில் சோதனை (பல-ஏஜென்ட்) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Foundry-க்கு வெளியிடவும் | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | விளையாட்டுத்துலையில் சரிபார்க்கவும் | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | பிழைத் திருத்தம் (பல-எஜெந்த்) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## பராமரிப்பாளர்

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>ஷிவம் கோயல்</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## தேவையான அனுமதிகள் (துரிதக் குறிப்புகள்)

| சூழல் | தேவையான பங்கு வகிகள் |
|----------|---------------|
| புதிய Foundry திட்டம் உருவாக்கவும் | Foundry வளத்தில் **Azure AI உரிமையாளர்** |
| எ_existing_ திட்டத்தில் வெளியிடவும் (புதிய வளங்கள்) | சந்தாவில் **Azure AI உரிமையாளர்** + **கொணர்பனியாளர்** |
| முழுமையாக அமைக்கப்பட்ட திட்டத்தில் வெளியிடவும் | கணக்கில் **பருகுனரா** + திட்டத்தில் **Azure AI பயனர்** |

> **முக்கியம்:** Azure `உரிமையாளர்` மற்றும் `கொணர்பனியாளர்` பங்குகள் *மேலாண்மை* அனுமதிகள் மட்டுமே உள்ளடக்கியவை, *வளர்ச்சி* (தரவு செயல்பாட்டு) அனுமதிகள் அல்ல. எஜெந்த்களை உருவாக்கவும் வெளியிடவும் **Azure AI பயனர்** அல்லது **Azure AI உரிமையாளர்** தேவை.

---

## குறிப்பு ஆதாரங்கள்

- [விரைவாண்மை: உங்கள் முதல் ஹோஸ்டட் எஜெந்தை வெளியிடவும் (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [ஹோஸ்டட் எஜெந்த்கள் என்ன?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS Code-ல் ஹோஸ்டட் எஜெந்த் பண்படுத்தல்கள் உருவாக்கவும்](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [ஹோஸ்டட் எஜெந்தை வெளியிடவும்](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundryக்கு RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [கட்டமைப்பு மதிப்பாய்வு எஜெந்த் மாதிரி](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP கருவிகள், Excalidraw வரைபடங்கள் மற்றும் இரட்டைத்தளவீடு கொண்ட உண்மையான உலக ஹோஸ்டட் எஜெந்த்

---


## உரிமம்

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**மறுப்பு**:
இந்த ஆவணம் AI மொழிபெயர்ப்பு சேவை [Co-op Translator](https://github.com/Azure/co-op-translator) பயன்படுத்தி மொழிபெயர்க்கப்பட்டுள்ளது. நாங்கள் துல்லியத்திற்காக முயற்சி செய்துள்ளோம், ஆனால் தானாக செய்யப்படும் மொழிபெயர்ப்புகளில் பிழைகள் அல்லது தவறுகள் இருக்கலாம் என்பதை கவனத்தில் கொள்ளவும். அசல் ஆவணம் அதன் தாய்மொழியில் அதிகாரப்பூர்வ ஆதாரமாக கருதப்பட வேண்டும். முக்கியமான தகவல்களுக்கு, தொழில்நுட்பமான மனித மொழிபெயர்ப்பு பரிந்துரைக்கப்படுகிறது. இந்த மொழிபெயர்ப்பைப் பயன்படுத்துவதால் ஏற்படும் எந்த தவறான புரிதல்கள் அல்லது தவறான விளக்கத்திற்கும் நாங்கள் பொறுப்பில்வில்லை.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->