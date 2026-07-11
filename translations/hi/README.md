# Foundry Toolkit + Foundry Hosted Agents कार्यशाला

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

AI एजेंट्स को **Microsoft Foundry Agent Service** पर **Hosted Agents** के रूप में बनाएं, परीक्षण करें, और परिनियोजित करें - पूरी तरह से VS Code से **Microsoft Foundry एक्सटेंशन** और **Foundry Toolkit** का उपयोग करके।

> **Hosted Agents वर्तमान में पूर्वावलोकन में हैं।** समर्थित क्षेत्र सीमित हैं - देखें [क्षेत्र उपलब्धता](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)।

> प्रत्येक प्रयोगशाला के अंदर `agent/` फ़ोल्डर **स्वचालित रूप से Foundry एक्सटेंशन द्वारा स्कैफोल्ड किया जाता है** - आप फिर कोड को अनुकूलित करते हैं, स्थानीय रूप से परीक्षण करते हैं, और परिनियोजित करते हैं।

### 🌐 बहुभाषी समर्थन

#### GitHub Action के माध्यम से समर्थित (स्वचालित और हमेशा अद्यतित)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](./README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानीय रूप से क्लोन करना पसंद है?**
>
> इस रिपॉजिटरी में 50+ भाषा अनुवाद शामिल हैं जो डाउनलोड आकार को काफी बढ़ाते हैं। बिना अनुवाद के क्लोन करने के लिए, sparse checkout का उपयोग करें:
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
> यह आपको कोर्स पूरा करने के लिए आवश्यक सब कुछ बहुत तेज़ डाउनलोड के साथ देता है।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## वास्तुकला

```mermaid
flowchart TB
    subgraph Local["स्थानीय विकास (VS कोड)"]
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
        Scaffold -- "F5 डिबग" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["माइक्रोसॉफ्ट फाउंड्री"]
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
    (localhost:8088)" --> ढांचा तैयार करें
    Playground -- "परीक्षण संकेत" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**प्रवाह:** Foundry एक्सटेंशन एजेंट को स्कैफोल्ड करता है → आप कोड और निर्देश अनुकूलित करते हैं → Agent Inspector के साथ स्थानीय रूप से परीक्षण करते हैं → Foundry पर परिनियोजित करते हैं (Docker इमेज ACR में पुश की जाती है) → Playground में सत्यापित करते हैं।

---

## आप क्या बनाएंगे

| प्रयोगशाला | विवरण | स्थिति |
|-----|-------------|--------|
| **प्रयोगशाला 01 - एकल एजेंट** | **"Explain Like I'm an Executive" एजेंट** बनाएं, स्थानीय रूप से परीक्षण करें, और Foundry पर परिनियोजित करें | ✅ उपलब्ध |
| **प्रयोगशाला 02 - मल्टी-एजेंट वर्कफ़्लो** | **"Resume → Job Fit Evaluator"** बनाएं - 4 एजेंट मिलकर रिज्यूमे फिट स्कोर करते हैं और एक शिक्षण रोडमैप तैयार करते हैं | ✅ उपलब्ध |

---

## Executive Agent से मिलें

इस कार्यशाला में आप **"Explain Like I'm an Executive" Agent** बनाएंगे - एक AI एजेंट जो जटिल तकनीकी शब्दजाल को शांत, बोर्डरूम-तैयार सारांशों में अनुवाद करता है। क्योंकि ईमानदारी से कहें, C-suite में कोई यह सुनना नहीं चाहता कि "v3.2 में पेश किए गए सिंक्रोनस कॉल्स के कारण थ्रेड पूल समाप्ति हो गई।"

मैंने यह एजेंट तब बनाया जब मेरी अच्छी तरह से तैयार पोस्ट-मॉर्टम पर प्रतिक्रिया थी: *"तो... क्या वेबसाइट डाउन है या नहीं?"*

### यह कैसे काम करता है

आप इसे एक तकनीकी अपडेट देते हैं। यह एक कार्यकारी सारांश देता है - तीन बिंदु, कोई शब्दजाल नहीं, कोई स्टैक ट्रेस नहीं, कोई अस्तित्व संबंधी डर नहीं। सिर्फ़ **क्या हुआ**, **व्यवसाय पर प्रभाव**, और **अगला कदम**।

### इसे क्रियाशील देखें

**आप कहते हैं:**
> "API लैटेंसी v3.2 में पेश किए गए सिंक्रोनस कॉल्स के कारण थ्रेड पूल समाप्ति की वजह से बढ़ गई।"

**एजेंट जवाब देता है:**

> **कार्यकारी सारांश:**
> - **क्या हुआ:** नवीनतम रिलीज के बाद सिस्टम धीमा हो गया।
> - **व्यवसाय पर प्रभाव:** कुछ उपयोगकर्ताओं को सेवा उपयोग में देरी का सामना करना पड़ा।
> - **अगला कदम:** परिवर्तन वापस ले लिया गया है और पुनः तैनाती से पहले एक सुधार तैयार किया जा रहा है।

### यह एजेंट क्यों?

यह एक बहुत ही सरल, अकेले उद्देश्य वाला एजेंट है - होस्टेड एजेंट वर्कफ़्लो को अंत तक सीखने के लिए बिल्कुल उपयुक्त, बिना जटिल टूल चेन में उलझे। और सच कहूँ? हर इंजीनियरिंग टीम को इनमे से एक की जरूरत होती है।

---

## कार्यशाला संरचना

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

> **टिप्पणी:** प्रत्येक प्रयोगशाला के अंदर `agent/` फ़ोल्डर वह है जो आप कमांड पैलेट से `Microsoft Foundry: Create a New Hosted Agent` चलाने पर **Microsoft Foundry एक्सटेंशन** उत्पन्न करता है। फिर फाइलें आपके एजेंट के निर्देशों, उपकरणों, और विन्यास के साथ अनुकूलित की जाती हैं। प्रयोगशाला 01 आपको इसे शुरू से फिर से बनाने में मार्गदर्शन देती है।

---

## आरंभ करना

### 1. रिपॉजिटरी क्लोन करें

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Python वर्चुअल एनवायरनमेंट सेटअप करें

```bash
python -m venv venv
```

इसे सक्रिय करें:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. निर्भरता स्थापित करें

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. पर्यावरण चर कॉन्फ़िगर करें

एजेंट फ़ोल्डर के अंदर उदाहरण `.env` फ़ाइल कॉपी करें और अपने मान भरें:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` संपादित करें:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. कार्यशाला प्रयोगशालाओं का पालन करें

प्रत्येक प्रयोगशाला अपने मॉड्यूल के साथ स्वावलंबी है। मौलिक जानने के लिए **प्रयोगशाला 01** से शुरू करें, फिर मल्टी-एजेंट वर्कफ़्लो के लिए **प्रयोगशाला 02** पर जाएं।

#### प्रयोगशाला 01 - एकल एजेंट ([पूर्ण निर्देश](workshop/lab01-single-agent/README.md))

| # | मॉड्यूल | लिंक |
|---|--------|------|
| 1 | पूर्वापेक्षाएँ पढ़ें | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry एक्सटेंशन स्थापित करें | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry परियोजना बनाएँ | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | एक होस्टेड एजेंट बनाएं | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | निर्देश और पर्यावरण कॉन्फ़िगर करें | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | स्थानीय रूप से परीक्षण करें | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundry पर परिनियोजित करें | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | प्लेग्राउंड में सत्यापित करें | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | समस्या निवारण | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### प्रयोगशाला 02 - मल्टी-एजेंट वर्कफ़्लो ([पूर्ण निर्देश](workshop/lab02-multi-agent/README.md))

| # | मॉड्यूल | लिंक |
|---|--------|------|
| 1 | पूर्वापेक्षाएँ (प्रयोगशाला 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | मल्टी-एजेंट आर्किटेक्चर समझें | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | मल्टी-एजेंट परियोजना स्कैफोल्ड करें | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | एजेंट्स और पर्यावरण कॉन्फ़िगर करें | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | ऑर्केस्ट्रेशन पैटर्न्स | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | स्थानीय रूप से परीक्षण करें (मल्टी-एजेंट) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | फाउंडरी पर तैनात करें | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | प्लेग्राउंड में सत्यापित करें | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | समस्या समाधान (मल्टी-एजेंट) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## मेन्टेनर

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>शिवम गोयल</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## आवश्यक अनुमतियां (त्वरित संदर्भ)

| परिदृश्य | आवश्यक भूमिकाएँ |
|----------|---------------|
| नया फाउंडरी प्रोजेक्ट बनाएं | फाउंडरी संसाधन पर **Azure AI Owner** |
| मौजूदा प्रोजेक्ट में तैनात करें (नए संसाधन) | सदस्यता पर **Azure AI Owner** + **Contributor** |
| पूरी तरह से कॉन्फ़िगर किए गए प्रोजेक्ट में तैनात करें | खाते पर **Reader** + प्रोजेक्ट पर **Azure AI User** |

> **महत्वपूर्ण:** Azure `Owner` और `Contributor` भूमिकाओं में केवल *प्रबंधन* अनुमतियां शामिल हैं, *विकास* (डेटा क्रिया) अनुमतियां नहीं। एजेंट बनाने और तैनात करने के लिए आपको **Azure AI User** या **Azure AI Owner** चाहिए।

---

## संदर्भ

- [त्वरित शुरुआत: अपना पहला होस्टेड एजेंट तैनात करें (VS कोड)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [होस्टेड एजेंट क्या हैं?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS कोड में होस्टेड एजेंट वर्कफ़्लोज़ बनाएं](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [होस्टेड एजेंट तैनात करें](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry के लिए RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [आर्किटेक्चर समीक्षा एजेंट नमूना](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP टूल्स, Excalidraw आरेखों, और द्वैध तैनाती के साथ वास्तविक दुनिया का होस्टेड एजेंट

---


## लाइसेंस

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
इस दस्तावेज़ का अनुवाद AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->