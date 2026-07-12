# Foundry Toolkit + Foundry Hosted Agents कार्यशाळा

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

एआय एजंट्स तयार करा, चाचणी करा, आणि **Microsoft Foundry Agent Service** मध्ये **Hosted Agents** म्हणून तैनात करा - पूर्णपणे VS Code वापरून **Microsoft Foundry विस्तार** आणि **Foundry Toolkit** वापरुन.

> **Hosted Agents सध्या पूर्वावलोकनात आहेत.** समर्थित प्रदेश मर्यादित आहेत - पाहा [प्रदेश उपलब्धता](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> प्रत्येक लॅबमधील `agent/` फोल्डर **Foundry विस्ताराद्वारे स्वयंचलितपणे तयार केला जातो** - नंतर आपण कोड सानुकूलित करता, स्थानिक चाचणी करता, आणि तैनात करता.

### 🌐 बहुभाषिक समर्थन

#### GitHub Action द्वारे समर्थित (स्वयंचलित आणि सदैव अद्ययावत)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](./README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानिक क्लोन करणे प्राधान्य द्यायचे का?**
>
> या रिपॉझिटरीमध्ये ५०+ भाषा अनुवाद आहेत, ज्यामुळे डाउनलोड आकार खूप वाढतो. अनुवादांशिवाय क्लोन करण्यासाठी sparse checkout वापरा:
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
> हे आपल्याला कोर्स पूर्ण करण्यासाठी आवश्यक असलेले सर्व काही जलद डाउनलोडसह देते.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## आर्किटेक्चर

```mermaid
flowchart TB
    subgraph Local["स्थानिक विकास (VS कोड)"]
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
        Scaffold -- "F5 डीबग" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["मायक्रोसॉफ्ट फाउंड्री"]
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
    (localhost:8088)" --> ढाँचा तयार करा
    Playground -- "चाचणी प्रवर्तक" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**प्रवाह:** Foundry विस्तार एजंट तयार करतो → आपण कोड आणि सूचना सानुकूलित करता → Agent Inspector सह स्थानिक चाचणी → Foundry मध्ये तैनात करा (Docker इमेज ACR कडे ढकलले जाते) → प्लेग्राऊंड मध्ये तपासा.

---

## आपण काय तयार कराल

| लॅब | वर्णन | स्थिती |
|-----|-------------|--------|
| **Lab 01 - Single Agent** | **"Explain Like I'm an Executive" एजंट** तयार करा, स्थानिक चाचणी करा, आणि Foundry मध्ये तैनात करा | ✅ उपलब्ध |
| **Lab 02 - Multi-Agent Workflow** | **"Resume → Job Fit Evaluator"** तयार करा - ४ एजंट्स एकत्र येऊन रिज्युमे फिट स्कोअर करतात आणि शिकण्याचा रोडमॅप तयार करतात | ✅ उपलब्ध |

---

## Executive Agent ची ओळख

या कार्यशाळेत आपण **"Explain Like I'm an Executive" एजंट** तयार कराल - एक एआय एजंट जो गुंतागुंतीची तांत्रिक भाषाशैली घेतो आणि शांत, बोर्डरूम-तयार सारांशात अनुवादित करतो. खरी गोष्ट म्हणजे, C-suite मधील कोणीही "thread pool exhaustion caused by synchronous calls introduced in v3.2." ऐकू इच्छित नाही.

मी हा एजंट तयार केला कारण अनेक वेळा माझा परिपूर्ण पोस्ट-मॉर्टम उत्तर मिळाले: *"मग... वेबसाइट चालू आहे की नाही?"*

### हे कसे काम करते

आपण त्याला तांत्रिक अपडेट देता. तो आपल्याला कार्यकारी सारांश देतो - तीन बुलेट पॉइंट्स, कोणताही जार्गन नाही, कोणतेही स्टॅक ट्रेस नाही, कोणतीही अस्वस्थता नाही. फक्त **काय झाले**, **व्यवसायावर परिणाम**, आणि **पुढचा टप्पा**.

### क्रियेत पहा

**आपण म्हणता:**
> "API लॅटन्सी वाढली कारण synchronous calls मुळे v3.2 मध्ये thread pool exhaustion झाला."

**एजंट उत्तर देतो:**

> **कार्यकारी सारांश:**
> - **काय झाले:** नवीनतम रिलीझ नंतर सिस्टम हळू झाले.
> - **व्यवसायावर परिणाम:** काही वापरकर्त्यांना सेवा वापरताना विलंब अनुभवावा लागला.
> - **पुढचा टप्पा:** बदल मागे घेतला गेला आहे आणि पुन्हा तैनात करण्याआधी दुरुस्ती तयार केली जात आहे.

### हा एजंट का?

हा एक सोपा, एकल-उद्देशाचा एजंट आहे - होस्टेड एजंट कार्यप्रवाह संपूर्ण शिकण्यासाठी परिपूर्ण, ज्यामुळे जटिल टूल चेनमध्ये अडकणे टळते. आणि प्रामाणिकपणे? प्रत्येक अभियांत्रिकी टीमला यापैकी एक हवेच आहे.

---

## कार्यशाळा संरचना

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

> **टीप:** प्रत्येक लॅबमध्ये `agent/` फोल्डर हा **Microsoft Foundry विस्ताराद्वारे** तयार केला जातो जेव्हा आपण Command Palette मधून `Microsoft Foundry: Create a New Hosted Agent` चालवता. नंतर त्या फाइल्स एजंटच्या सूचना, टूल्स, आणि कॉन्फिगरेशन नुसार सानुकूलित केल्या जातात. Lab 01 मध्ये आपण ह्याचा आरंभापासून पुनर्निर्माण कसा करायचा ते पाहाल.

---

## सुरुवात कशी करावी

### 1. रिपॉझिटरी क्लोन करा

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Python व्हर्च्युअल एन्व्हायर्नमेंट सेट करा

```bash
python -m venv venv
```

ते सक्रिय करा:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. अवलंबित्व स्थापित करा

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. एन्व्हायर्नमेंट व्हेरिएबल कॉन्फिगर करा

एजंट फोल्डरमधील उदाहरण `.env` फाइल कॉपी करा आणि आपली मूल्ये भरा:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` संपादित करा:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. कार्यशाळेतील लॅब्सचा पाठपुरावा करा

प्रत्येक लॅब स्वतःच्या मॉड्यूलसह स्वतंत्र आहे. मूळ गोष्टी शिकण्यासाठी **Lab 01** पासून प्रारंभ करा, नंतर बहु-एजंट कार्यप्रवाहासाठी **Lab 02** कडे जा.

#### Lab 01 - Single Agent ([संपूर्ण सूचना](workshop/lab01-single-agent/README.md))

| # | मॉड्यूल | दुवा |
|---|--------|------|
| 1 | आवश्यक गोष्टी वाचा | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry विस्तार स्थापित करा | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry प्रोजेक्ट तयार करा | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Hosted Agent तयार करा | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | सूचना आणि पर्यावरण कॉन्फिगर करा | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | स्थानिक चाचणी करा | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundry मध्ये तैनात करा | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | प्लेग्राऊंड मध्ये सत्यापित करा | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | समस्या निवारण | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Multi-Agent Workflow ([संपूर्ण सूचना](workshop/lab02-multi-agent/README.md))

| # | मॉड्यूल | दुवा |
|---|--------|------|
| 1 | आवश्यकताएँ (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | बहु-एजंट आर्किटेक्चर समजून घ्या | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | बहु-एजंट प्रोजेक्ट तयार करा | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | एजंट्स आणि पर्यावरण कॉन्फिगर करा | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | आर्कष्ट्रेशन पॅटर्न | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | स्थानिक चाचणी (बहु-एजंट) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | फाउंड्रीवर तैनात करा | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | प्लेग्राउंडमध्ये पडताळणी करा | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | त्रुटी निराकरण (मल्टि-एजंट) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## देखभाल करणारा

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

## आवश्यक परवानग्या (जलद संदर्भ)

| परिस्थिती | आवश्यक भूमिका |
|----------|---------------|
| नवीन फाउंड्री प्रकल्प तयार करा | फाउंड्री संसाधनावर **Azure AI Owner** |
| विद्यमान प्रकल्पात तैनात करा (नवीन संसाधने) | सदस्यत्वावर **Azure AI Owner** + **Contributor** |
| पूर्णपणे संरचीत प्रकल्पात तैनात करा | खात्यावर **Reader** + प्रकल्पावर **Azure AI User** |

> **महत्त्वाचे:** Azure `Owner` आणि `Contributor` भूमिका फक्त *व्यवस्थापन* परवानग्या समाविष्ट करतात, *विकास* (डेटा क्रिया) परवानग्या नाहीत. एजंट तयार करण्यासाठी आणि तैनात करण्यासाठी तुम्हाला **Azure AI User** किंवा **Azure AI Owner** आवश्यक आहे.

---

## संदर्भ

- [जलद प्रारंभ: तुमचा पहिला होस्टेड एजंट तैनात करा (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [होस्टेड एजंट म्हणजे काय?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS Code मध्ये होस्टेड एजंट वर्कफ्लो तयार करा](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [होस्टेड एजंट तैनात करा](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry साठी RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [आर्किटेक्चर रिव्यू एजंट सॅम्पल](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP टूल्स, Excalidraw आकृत्या आणि द्वैतीय तैनातीसह वास्तविक होस्टेड एजंट

---


## परवाना

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून अनुवादित केला आहे. जरी आम्ही अचूकतेसाठी प्रयत्न करतो, तरी कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या मूळ भाषेत अधिकृत स्रोत मानला पाहिजे. महत्त्वाची माहिती असल्यास, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थलावणीसाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->