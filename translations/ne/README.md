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

**Microsoft Foundry Agent Service** लाई **Hosted Agents** को रूपमा AI एजेन्टहरू निर्माण, परीक्षण, र तैनाथ गर्नुहोस् - पूर्ण रूपमा VS Code बाट **Microsoft Foundry extension** र **Foundry Toolkit** प्रयोग गरेर।

> **Hosted Agents हाल पूर्वावलोकनमा छन्।** समर्थन गरिएको क्षेत्र सीमित छ - [क्षेत्र उपलब्धता](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) हेर्नुहोस्।

> प्रत्येक प्रयोगशालाको भित्र `agent/` फोल्डर **Foundry extension द्वारा स्वचालित रूपमा निर्माण गरिएको हुन्छ** - त्यसपछि तपाईंले कोड अनुकूलन गर्नुहोस्, स्थानीय रूपमा परीक्षण गर्नुहोस्, र तैनाथ गर्नुहोस्।

### 🌐 बहुभाषी समर्थन

#### GitHub Action मार्फत समर्थन छ (स्वचालित र सँधै अपडेट हुने)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](./README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **स्थानीय रूपमा क्लोन गर्न मन छ?**
>
> यो रिपोजिटरीमा ५०+ भाषा अनुवादहरू छन् जसले डाउनलोड साइजलाई उल्लेखनीय रूपमा बढाउँछ। अनुवादहरू बिना क्लोन गर्न, sparse checkout प्रयोग गर्नुहोस्:
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
> यसले तपाईंलाई कोर्स पूरा गर्न आवश्यक सबै प्रदान गर्दछ, धेरै छिटो डाउनलोड गरेर।
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

    subgraph Cloud["माइक्रोसफ्ट फाउन्ड्री"]
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
    (localhost:8088)" --> स्क्याफोल्ड
    Playground -- "परीक्षण संकेतहरू" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**प्रवाह:** Foundry extension ले एजेन्ट स्क्याफोल्ड गर्छ → तपाईंले कोड र निर्देशनहरू अनुकूलन गर्नुहोस् → स्थानीय रूपमा Agent Inspector सँग परीक्षण गर्नुहोस् → Foundry मा तैनाथ गर्नुहोस् (Docker छवि ACR मा पठाइन्छ) → Playground मा प्रमाणीकरण गर्नुहोस्।

---

## तपाईंले के बनाउनुहुनेछ

| प्रयोगशाला | विवरण | स्थिति |
|-----|-------------|--------|
| **प्रयोगशाला ०१ - एकल एजेन्ट** | **"Examine Like I'm an Executive" Agent** बनाउनुहोस्, स्थानीय रूपमा परीक्षण गर्नुहोस्, र Foundry मा तैनाथ गर्नुहोस् | ✅ उपलब्ध |
| **प्रयोगशाला ०२ - बहु-एजेन्ट कार्यप्रवाह** | **"Resume → Job Fit Evaluator"** बनाउनुहोस् - ४ एजेन्टहरूले मिलेर रिजुमेको फिट स्कोर गर्छन् र सिकाइ रोडम्याप उत्पन्न गर्छन् | ✅ उपलब्ध |

---

## Executive Agent सँग परिचय

यस कार्यशालामा तपाईंले **"Explain Like I'm an Executive" Agent** बनाउनु हुनेछ - जुन AI एजेन्ट हो जसले जटिल प्राविधिक जार्गनलाई शान्त, बोर्डरूम-तयार सारांशमा अनुवाद गर्दछ। किनभने साँचो कुरा के हो भने, C-suite मा कसैले पनि "थ्रेड पुल इग्जोस्टसन जुन संस्करण ३.२ मा परिचालित सहक्रियात्मक कलहरूले भएको हो" सुन्न चाहँदैन।

मैले यो एजेन्ट त्यति पटक बनाएँ जब मेरो राम्रोसँग तयार गरिएको पोस्ट-मोर्टेमको जवाफ थियो: *"त्यसो भए... वेबसाइट तल छ कि छैन?"*

### यो कसरी काम गर्दछ

तपाईं यसलाई प्राविधिक अद्यावधिक दिनुहुन्छ। यसले कार्यकारी सारांश फिर्ता गर्दछ - तीन मुख्य बुँदाहरू, कुनै जार्गन छैन, कुनै स्ट्याक ट्रेस छैन, कुनै अस्तित्वगत डर छैन। केवल **के भयो**, **व्यावसायिक प्रभाव**, र **अर्को कदम**।

### प्रयोगमा हेर्नुहोस्

**तपाईं भन्नुहुन्छ:**
> "API लेटेन्सी थ्रेड पुल इग्जोस्टसन कारणले बढ्यो जुन संस्करण ३.२ मा परिचालित सहक्रियात्मक कलले भयो।"

**एजेन्ट उत्तर दिन्छ:**

> **कार्यकारी सारांश:**
> - **के भयो:** पछिल्लो रिलिज पछि, प्रणाली सुस्त भयो।
> - **व्यावसायिक प्रभाव:** केही प्रयोगकर्ताहरूले सेवा प्रयोग गर्दा ढिलाइ अनुभव गरे।
> - **अर्को कदम:** परिवर्तन फर्काइएको छ र पुन: तैनाथीकरण अघि सुधार तयारी भइरहेको छ।

### किन यो एजेन्ट?

यो एकदम सरल, एउटै उद्देश्यको एजेन्ट हो - जटिल उपकरण सञ्जालमा नअड्किएर होस्टेड एजेन्ट कार्यप्रवाह पूर्ण रूपमा सिक्न उपयुक्त। र साँचो कुरा के हो भने? प्रत्येक इन्जिनियरिङ टोलीलाई यस्ता मध्ये एउटा चाहिन्छ।

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

> **सूचना:** प्रत्येक प्रयोगशालाको भित्र `agent/` फोल्डर भनेको **Microsoft Foundry extension** द्वारा उत्पादन गरिएको हो जब तपाईंले Command Palette बाट `Microsoft Foundry: Create a New Hosted Agent` चलाउनुहुन्छ। फाइलहरू त्यसपछि तपाईंको एजेन्टका निर्देशनहरू, उपकरणहरू, र कन्फिगरेसनसँग अनुकूलित गरिन्छन्। प्रयोगशाला ०१ ले यो कसरी शून्यबाट पुनर्निर्माण गर्ने सिकाउँछ।

---

## सुरु गर्ने तरिका

### १. रिपोजिटरी क्लोन गर्नुहोस्

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### २. Python भर्चुअल वातावरण सेटअप गर्नुहोस्

```bash
python -m venv venv
```

यसलाई सक्रिय गर्नुहोस्:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### ३. निर्भरता स्थापना गर्नुहोस्

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### ४. वातावरण भेरिएबलहरू कन्फिगर गर्नुहोस्

एजेन्ट फोल्डर भित्रको `.env` फाइलको उदाहरण प्रतिलिपि गर्नुहोस् र तपाईंका मानहरू भर्नुहोस्:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` सम्पादन गर्नुहोस्:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### ५. कार्यशाला प्रयोगशालाहरू अनुसरण गर्नुहोस्

प्रत्येक प्रयोगशाला आफ्नै मोड्युलसहित आत्मनिर्भर हुन्छ। आधारहरू सिक्न **प्रयोगशाला ०१** बाट सुरु गर्नुहोस्, त्यसपछि बहु-एजेन्ट कार्यप्रवाहहरूका लागि **प्रयोगशाला ०२** मा जानुहोस्।

#### प्रयोगशाला ०१ - एकल एजेन्ट ([पूर्ण निर्देशनहरू](workshop/lab01-single-agent/README.md))

| # | मोड्युल | लिंक |
|---|--------|------|
| १ | पूर्वआवश्यकताहरू पढ्नुहोस् | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| २ | Foundry Toolkit र Foundry विस्तार स्थापना गर्नुहोस् | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| ३ | Foundry परियोजना सिर्जना गर्नुहोस् | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| ४ | होस्टेड एजेन्ट सिर्जना गर्नुहोस् | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| ५ | निर्देशनहरू र वातावरण कन्फिगर गर्नुहोस् | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| ६ | स्थानीय रूपमा परीक्षण गर्नुहोस् | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| ७ | Foundry मा तैनाथ गर्नुहोस् | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| ८ | खेल मैदानमा प्रमाणीकरण गर्नुहोस् | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| ९ | समस्या समाधान | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### प्रयोगशाला ०२ - बहु-एजेन्ट कार्यप्रवाह ([पूर्ण निर्देशनहरू](workshop/lab02-multi-agent/README.md))

| # | मोड्युल | लिंक |
|---|--------|------|
| १ | पूर्वआवश्यकताहरू (प्रयोगशाला ०२) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| २ | बहु-एजेन्ट वास्तुकलालाई बुझ्नुहोस् | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| ३ | बहु-एजेन्ट परियोजना स्क्याफोल्ड गर्नुहोस् | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| ४ | एजेन्टहरू र वातावरण कन्फिगर गर्नुहोस् | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| ५ | समन्वय नमूनाहरू | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| ६ | स्थानीय रूपमा परीक्षण गर्नुहोस् (बहु-एजेन्ट) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Foundry मा डिप्लोय गर्नुहोस् | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | प्लेग्राउन्डमा प्रमाणित गर्नुहोस् | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | समस्या समाधान (बहु-एजेन्ट) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## मर्मतकर्ता

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

## आवश्यक अनुमति (छिटो सन्दर्भ)

| परिस्थिति | आवश्यक भूमिकाहरू |
|----------|---------------|
| नयाँ Foundry परियोजना सिर्जना गर्नुहोस् | Foundry स्रोतमा **Azure AI Owner** |
| अवस्थित परियोजनामा डिप्लोय गर्नुहोस् (नयाँ स्रोतहरू) | सदस्यतामा **Azure AI Owner** + **Contributor** |
| पूर्ण रूपमा कन्फिगर गरिएको परियोजनामा डिप्लोय गर्नुहोस् | खातामा **Reader** + परियोजनामा **Azure AI User** |

> **महत्त्वपूर्ण:** Azure `Owner` र `Contributor` भूमिकाहरूले मात्र *प्रबंधन* अनुमति समावेश गर्छन्, *विकास* (डेटा क्रिया) अनुमतिहरू होइनन्। एजेन्टहरू निर्माण र डिप्लोय गर्न तपाईलाई **Azure AI User** वा **Azure AI Owner** आवश्यक पर्छ।

---

## सन्दर्भहरू

- [Quickstart: तपाईंको पहिलो होस्टेड एजेन्ट डिप्लोय गर्नुहोस् (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [होस्टेड एजेन्टहरू के हुन्?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS Code मा होस्टेड एजेन्ट कार्यप्रवाहहरू सिर्जना गर्नुहोस्](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [होस्टेड एजेन्ट डिप्लोय गर्नुहोस्](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry का लागि RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [आर्किटेक्चर समीक्षा एजेन्ट नमूना](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP उपकरणहरू, Excalidraw डायग्रामहरू, र दोहोरो डिप्लोयमेन्ट सहित वास्तविक-विश्व होस्टेड एजेन्ट

---


## लाइसेन्स

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी सही हुन प्रयास गर्छौं, तर कृपया जानकार हुनुस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छन्। मूल दस्तावेज़ यसको मूल भाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलत बुझाइ वा त्रुटिको लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->