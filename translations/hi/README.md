# Foundry Toolkit + Foundry Hosted Agents कार्यशाला

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.0.0rc3-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents/)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Microsoft Foundry Agent Service** में **Hosted Agents** के रूप में AI एजेंट बनाएँ, परीक्षण करें, और तैनात करें - पूरी तरह से VS Code से **Microsoft Foundry एक्सटेंशन** और **Foundry Toolkit** का उपयोग करके।

> **Hosted Agents वर्तमान में प्रीव्यू में हैं।** समर्थित क्षेत्र सीमित हैं - देखें [क्षेत्र उपलब्धता](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)।

> प्रत्येक लैब के अंदर `agent/` फ़ोल्डर **स्वचालित रूप से Foundry एक्सटेंशन द्वारा स्कैफ़ोल्ड किया जाता है** - आप फिर कोड को अनुकूलित करते हैं, स्थानीय रूप से परीक्षण करते हैं, और तैनात करते हैं।

### 🌐 बहुभाषी समर्थन

#### GitHub Action के माध्यम से समर्थित (स्वचालित और हमेशा अद्यतन)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](./README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानीय रूप से क्लोन करना पसंद करते हैं?**
>
> यह रिपॉजिटरी 50+ भाषा अनुवादों को शामिल करता है जो डाउनलोड आकार को काफी बढ़ाते हैं। बिना अनुवाद के क्लोन करने के लिए sparse checkout का उपयोग करें:
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
> यह आपको तेज़ डाउनलोड के साथ कोर्स पूरा करने के लिए सब कुछ देता है।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## आर्किटेक्चर

```mermaid
flowchart TB
    subgraph Local["स्थानीय विकास (VS कोड)"]
        direction TB
        FE["Microsoft Foundry
        एक्सटेंशन"]
        FoundryToolkit["Foundry टूलकिट
        एक्सटेंशन"]
        Scaffold["स्कैफ़ोल्ड किया एजेंट कोड
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["एजेंट निरीक्षक
        (स्थानीय परीक्षण)"]
        FE -- "नया बनाएं
        होस्टेड एजेंट" --> Scaffold
        Scaffold -- "F5 डीबग" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure कंटेनर
        रजिस्ट्री"]
        AgentService["Foundry एजेंट सेवा
        (होस्टेड एजेंट रनटाइम)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry प्लेग्राउंड
        & VS कोड प्लेग्राउंड"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "परिनियोजित करें
    (Docker बिल्ड + पुश)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "प्रॉम्प्ट परीक्षण करें" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**प्रवाह:** Foundry एक्सटेंशन एजेंट को स्कैफ़ोल्ड करता है → आप कोड और निर्देश अनुकूलित करते हैं → Agent Inspector के साथ स्थानीय रूप से परीक्षण करते हैं → Foundry पर तैनात करते हैं (Docker इमेज ACR में पुश की जाती है) → Playground में सत्यापित करते हैं।

---

## आप क्या बनाएंगे

| लैब | विवरण | स्थिति |
|-----|-------------|--------|
| **लैब 01 - सिंगल एजेंट** | **"Explain Like I'm an Executive" Agent** बनाएँ, स्थानीय रूप से परीक्षण करें, और Foundry में तैनात करें | ✅ उपलब्ध |
| **लैब 02 - मल्टी-एजेंट वर्कफ़्लो** | **"Resume → Job Fit Evaluator"** बनाएं - 4 एजेंट मिलकर रिज्यूमे फ़िट का स्कोरिंग और एक शिक्षण रोडमैप तैयार करते हैं | ✅ उपलब्ध |

---

## Executive Agent से मिलें

इस कार्यशाला में आप **"Explain Like I'm an Executive" Agent** बनाएंगे - एक AI एजेंट जो जटिल तकनीकी शब्दजाल को शांति से, बोर्डरूम-प्रस्तुत सारांशों में अनुवादित करता है। क्योंकि ईमानदारी से कहें तो, C-सीट में कोई भी "v3.2 में परिचय किए गए synchronous कॉल्स के कारण थ्रेड पूल एक्सहॉस्टन" की बात सुनना नहीं चाहता।

मैंने यह एजेंट कई बार इस स्थिति के बाद बनाया जहां मेरी पूरी तरह से तैयार पोस्टमॉर्टम को जवाब मिला: *"तो... क्या वेबसाइट डाउन है या नहीं?"*

### यह कैसे काम करता है

आप इसे एक तकनीकी अपडेट देते हैं। यह एक executive सारांश देता है - तीन बुलेट पॉइंट, बिना जर्गन, बिना स्टैक ट्रेसेस, बिना किसी existential डर के। बस **क्या हुआ**, **कारोबार पर प्रभाव**, और **अगला कदम**।

### इसे क्रिया में देखें

**आप कहते हैं:**
> "API लैटेंसी v3.2 में परिचय किए गए synchronous कॉल्स के कारण थ्रेड पूल एक्सहॉस्टन के कारण बढ़ गई।"

**एजेंट जवाब देता है:**

> **Executive सारांश:**
> - **क्या हुआ:** नवीनतम रिलीज़ के बाद, सिस्टम धीमा हो गया।
> - **कारोबार पर प्रभाव:** कुछ उपयोगकर्ताओं ने सेवा का उपयोग करते समय देरी महसूस की।
> - **अगला कदम:** परिवर्तन वापस ले लिया गया है और पुनः तैनाती से पहले एक फिक्स तैयार किया जा रहा है।

### यह एजेंट क्यों?

यह एक सरल, एकल-उद्देश्य एजेंट है - होस्टेड एजेंट वर्कफ़्लो को शुरुआत से अंत तक सीखने के लिए बिल्कुल सही, बिना जटिल टूल चेन में उलझने के। और सच कहूं? हर इंजीनियरिंग टीम को ऐसे एक एजेंट की जरूरत हो सकती है।

---

## कार्यशाला संरचना

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
├── 📂 ExecutiveAgent/                ← Standalone hosted agent project
│   ├── agent.yaml
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-install-foundry-toolkit.md
    │   │   ├── 02-create-foundry-project.md
    │   │   ├── 03-create-hosted-agent.md
    │   │   ├── 04-configure-and-code.md
    │   │   ├── 05-test-locally.md
    │   │   ├── 06-deploy-to-foundry.md
    │   │   ├── 07-verify-in-playground.md
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

> **टिप्पणी:** प्रत्येक लैब के अंदर `agent/` फ़ोल्डर वही है जो **Microsoft Foundry एक्सटेंशन** तब बनाता है जब आप कमांड पैलेट से `Microsoft Foundry: Create a New Hosted Agent` चलाते हैं। फिर फ़ाइलों को आपके एजेंट के निर्देशों, उपकरणों, और कॉन्फ़िगरेशन के साथ अनुकूलित किया जाता है। लैब 01 आपको इसे स्क्रैच से फिर से बनाने में मार्गदर्शन करता है।

---

## प्रारंभ करना

### 1. रिपॉजिटरी क्लोन करें

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Python वर्चुअल एन्वायरनमेंट सेट करें

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

### 3. निर्भरताएँ इंस्टॉल करें

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. एन्वायरनमेंट वेरिएबल सेट करें

एजेंट फ़ोल्डर के अंदर `.env` उदाहरण फ़ाइल कॉपी करें और अपनी वैल्यू भरें:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` को संपादित करें:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. कार्यशाला लैब का पालन करें

प्रत्येक लैब अपने मॉड्यूल के साथ स्व-निहित है। मूल बातें सीखने के लिए **लैब 01** से शुरू करें, फिर मल्टी-एजेंट वर्कफ़्लो के लिए **लैब 02** पर जाएँ।

#### लैब 01 - सिंगल एजेंट ([पूर्ण निर्देश](workshop/lab01-single-agent/README.md))

| # | मॉड्यूल | लिंक |
|---|--------|------|
| 1 | आवश्यकताएँ पढ़ें | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry एक्सटेंशन इंस्टॉल करें | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Foundry प्रोजेक्ट बनाएँ | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | एक होस्टेड एजेंट बनाएँ | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | निर्देश और पर्यावरण कॉन्फ़िगर करें | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | स्थानीय रूप से परीक्षण करें | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Foundry में तैनात करें | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | प्लेग्राउंड में सत्यापन करें | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | समस्या निवारण | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### लैब 02 - मल्टी-एजेंट वर्कफ़्लो ([पूर्ण निर्देश](workshop/lab02-multi-agent/README.md))

| # | मॉड्यूल | लिंक |
|---|--------|------|
| 1 | आवश्यकताएँ (लैब 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | मल्टी-एजेंट आर्किटेक्चर समझें | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | मल्टी-एजेंट प्रोजेक्ट स्कैफ़ोल्ड करें | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | एजेंट्स और पर्यावरण कॉन्फ़िगर करें | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | ऑर्केस्ट्रेशन पैटर्न्स | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | स्थानीय रूप से परीक्षण करें (मल्टी-एजेंट) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Foundry में तैनात करें | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | प्लेग्राउंड में सत्यापित करें | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | समस्या निवारण (मल्टी-एजेंट) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## मेंटेनर

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

## आवश्यक अनुमतियाँ (त्वरित संदर्भ)

| परिदृश्य | आवश्यक भूमिकाएँ |
|----------|---------------|
| नया Foundry प्रोजेक्ट बनाएं | Foundry संसाधन पर **Azure AI Owner** |
| मौजूदा प्रोजेक्ट में तैनात करें (नए संसाधन) | सदस्यता पर **Azure AI Owner** + **Contributor** |
| पूरी तरह से कॉन्फ़िगर किए गए प्रोजेक्ट में तैनात करें | खाते पर **Reader** + प्रोजेक्ट पर **Azure AI User** |

> **महत्वपूर्ण:** Azure `Owner` और `Contributor` भूमिकाओं में केवल *प्रबंधन* अनुमतियाँ शामिल हैं, *विकास* (डेटा क्रिया) अनुमतियाँ नहीं। एजेंट बनाने और तैनात करने के लिए आपको **Azure AI User** या **Azure AI Owner** की आवश्यकता है।

---

## संदर्भ

- [त्वरित प्रारंभ: अपना पहला होस्टेड एजेंट तैनात करें (VS कोड)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [होस्टेड एजेंट क्या हैं?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS कोड में होस्टेड एजेंट वर्कफ़्लोज़ बनाएं](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [होस्टेड एजेंट तैनात करें](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry के लिए RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [आर्किटेक्चर रिव्यू एजेंट सैंप्ल](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP टूल्स, एक्स्केलिड्रॉ आरेख, और दोहरी तैनाती के साथ वास्तविक दुनिया का होस्टेड एजेंट

---

## लाइसेंस

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:  
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियां या गलतियां हो सकती हैं। मूल दस्तावेज़ अपनी मातृ भाषा में प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->