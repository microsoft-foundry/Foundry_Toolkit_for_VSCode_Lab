# فاؤنڈری ٹول کٹ + فاؤنڈری ہوسٹڈ ایجنٹس ورکشاپ

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

AI ایجنٹس کو **Microsoft Foundry Agent Service** پر **Hosted Agents** کے طور پر تعمیر، جانچ اور تعینات کریں — مکمل طور پر VS Code سے **Microsoft Foundry extension** اور **Foundry Toolkit** استعمال کرتے ہوئے۔

> **Hosted Agents اس وقت پیش نظارہ میں ہیں۔** معاونت یافتہ خطے محدود ہیں — دیکھیں [region availability](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)۔

> ہر لیب کے اندر `agent/` فولڈر کو Foundry ایکسٹینشن کی طرف سے **خودکار طور پر تیار کیا جاتا ہے** — پھر آپ کوڈ کو حسبِ ضرورت بناتے ہیں، مقامی طور پر ٹیسٹ کرتے ہیں، اور تعینات کرتے ہیں۔

### 🌐 کثیرالزبان معاونت

#### GitHub Action کے ذریعے معاونت یافتہ (خودکار اور ہمیشہ تازہ ترین)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](./README.md) | [Vietnamese](../vi/README.md)

> **مقامی کلون کرنا پسند کریں گے؟**
>
> یہ ذخیرہ 50+ زبانوں کے تراجم شامل کرتا ہے جو ڈاؤن لوڈ کے سائز کو نمایاں طور پر بڑھا دیتے ہیں۔ بغیر تراجم کے کلون کرنے کے لیے sparse checkout استعمال کریں:
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
> اس سے آپ کو کورس مکمل کرنے کے لیے سب کچھ ملتا ہے اور ڈاؤن لوڈ بہت تیز ہوتا ہے۔
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## فن تعمیر

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

**فلو:** Foundry ایکسٹینشن ایجنٹ کی اسکافولڈنگ کرتا ہے → آپ کوڈ اور ہدایات حسب ضرورت بناتے ہیں → Agent Inspector کے ساتھ مقامی طور پر ٹیسٹ کرتے ہیں → Foundry پر تعینات کرتے ہیں (Docker امیج ACR کو بھیجا جاتا ہے) → Playground میں تصدیق کرتے ہیں۔

---

## آپ کیا بنائیں گے

| لیب | وضاحت | حیثیت |
|-----|-------------|--------|
| **لیب 01 - سنگل ایجنٹ** | **"Explain Like I'm an Executive" ایجنٹ** بنائیں، مقامی طور پر ٹیسٹ کریں، اور Foundry پر تعینات کریں | ✅ دستیاب |
| **لیب 02 - ملٹی ایجنٹ ورک فلو** | **"Resume → Job Fit Evaluator"** بنائیں — 4 ایجنٹس مل کر ریزیومے کے موافق ہونے کی درجہ بندی کرتے ہیں اور تعلیمی روڈ میپ تیار کرتے ہیں | ✅ دستیاب |

---

## ایگزیکٹو ایجنٹ سے ملاقات

اس ورکشاپ میں آپ **"Explain Like I'm an Executive" ایجنٹ** بنائیں گے — ایک AI ایجنٹ جو پیچیدہ تکنیکی اصطلاحات کو پرسکون، بورڈروم کے لیے تیار خلاصوں میں ترجمہ کرتا ہے۔ کیونکہ ایمانداری سے بات کریں تو، C-suite میں کوئی بھی "thread pool exhaustion caused by synchronous calls introduced in v3.2." کے بارے میں سننا نہیں چاہتا۔

میں نے یہ ایجنٹ اس وقت بنایا جب میرے بے عیب پوسٹ مارٹم پر جواب ملا: *"تو... کیا ویب سائٹ بند ہے یا نہیں؟"*

### یہ کیسے کام کرتا ہے

آپ اسے تکنیکی اپ ڈیٹ دیتے ہیں۔ یہ ایک ایگزیکٹو خلاصہ دیتا ہے — تین بلٹ پوائنٹس، بغیر اصطلاحات، بغیر اسٹیک ٹریس، بغیر کسی وجودی خوف کے۔ صرف **کیا ہوا،** **کاروباری اثر،** اور **اگلا قدم**۔

### اسے عمل میں دیکھیں

**آپ کہتے ہیں:**
> "API کی تاخیر میں اضافہ ہوا کیونکہ thread pool exhaustion synchronous calls کی وجہ سے ہوئی جو v3.2 میں متعارف کرائے گئے۔"

**ایجنٹ جواب دیتا ہے:**

> **ایگزیکٹو خلاصہ:**
> - **کیا ہوا:** تازہ ترین ریلیز کے بعد، نظام سست ہو گیا۔
> - **کاروباری اثر:** کچھ صارفین کو سروس استعمال کرنے میں تاخیر کا سامنا کرنا پڑا۔
> - **اگلا قدم:** تبدیلی کو واپس لے لیا گیا ہے اور دوبارہ تعیناتی سے پہلے فکس تیار کیا جا رہا ہے۔

### یہ ایجنٹ کیوں؟

یہ ایک سادہ، مخصوص مقصد کا ایجنٹ ہے — ہوسٹڈ ایجنٹ ورک فلو کو شروع سے آخر تک سیکھنے کے لیے بہترین۔ اور ایمانداری سے؟ ہر انجینئرنگ ٹیم کو اس میں سے ایک کی ضرورت ہو سکتی ہے۔

---

## ورکشاپ کا ڈھانچہ

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

> **نوٹ:** ہر لیب کے اندر موجود `agent/` فولڈر وہ ہے جو **Microsoft Foundry extension** تب بناتا ہے جب آپ Command Palette سے `Microsoft Foundry: Create a New Hosted Agent` چلاتے ہیں۔ فائلیں پھر آپ کے ایجنٹ کی ہدایات، اوزار، اور کنفیگریشن کے ساتھ حسب ضرورت بنائی جاتی ہیں۔ لیب 01 آپ کو اس کو شروع سے دوبارہ بنانے کی رہنمائی کرتا ہے۔

---

## شروعات

### 1. ذخیرہ کو کلون کریں

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Python ورچوئل ماحول قائم کریں

```bash
python -m venv venv
```

اسے فعال کریں:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. انحصارات انسٹال کریں

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. ماحولیاتی متغیرات ترتیب دیں

ایجنٹ فولڈر کے اندر موجود مثال `.env` فائل کو کاپی کریں اور اپنی قدریں ڈالیں:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` میں ترمیم کریں:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. ورکشاپ کی لیبز پر عمل کریں

ہر لیب اپنے ماڈیولز کے ساتھ خودمختار ہے۔ بنیادیات سیکھنے کے لیے **لیب 01** سے شروع کریں، پھر ملٹی ایجنٹ ورک فلو کے لیے **لیب 02** پر جائیں۔

#### لیب 01 - سنگل ایجنٹ ([مکمل ہدایات](workshop/lab01-single-agent/README.md))

| # | ماڈیول | لنک |
|---|--------|------|
| 1 | ضروریات پڑھیں | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit اور Foundry ایکسٹینشن انسٹال کریں | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry پروجیکٹ بنائیں | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | ایک ہوسٹڈ ایجنٹ بنائیں | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | ہدایات اور ماحولیاتی ترتیبات کریں | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | مقامی طور پر ٹیسٹ کریں | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundry پر تعینات کریں | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | PlayGround میں تصدیق کریں | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | خلاصہ اور اگلے اقدامات | [07-summary.md](workshop/lab01-single-agent/docs/07-summary.md) |
| 10 | مسائل کا حل | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### لیب 02 - ملٹی ایجنٹ ورک فلو ([مکمل ہدایات](workshop/lab02-multi-agent/README.md))

| # | ماڈیول | لنک |
|---|--------|------|
| 1 | ضروریات (لیب 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | ملٹی ایجنٹ فن تعمیر کو سمجھیں | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | ملٹی ایجنٹ پروجیکٹ کی اسکافولڈنگ کریں | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | ایجنٹس اور ماحول کی ترتیب دیں | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | اورچیسٹریشن نمونے | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | مقامی طور پر جانچیں (کثیر ایجنٹ) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | فاؤنڈری پر تعینات کریں | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | پلے گراؤنڈ میں تصدیق کریں | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | مسئلہ حل کرنا (کثیر ایجنٹ) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |
| 10 | خلاصہ اور اگلے اقدامات | [09-summary.md](workshop/lab02-multi-agent/docs/09-summary.md) |

---

## مینٹینر

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>شیوام گوئل</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## مطلوبہ اجازتیں (جلدی حوالہ)

| منظر نامہ | مطلوبہ کردار |
|----------|---------------|
| نیا فاؤنڈری پروجیکٹ بنائیں | فاؤنڈری وسیلہ پر **Azure AI Owner** |
| موجودہ پروجیکٹ میں تعیناتی (نئے وسائل) | سبسکرپشن پر **Azure AI Owner** + **Contributor** |
| مکمل ترتیب شدہ پروجیکٹ میں تعیناتی | اکاؤنٹ پر **Reader** + پروجیکٹ پر **Azure AI User** |

> **اہم:** Azure `Owner` اور `Contributor` کے کردار صرف *انتظامی* اجازتیں شامل کرتے ہیں، *ترقیاتی* (ڈیٹا ایکشن) اجازتیں نہیں۔ ایجنٹس بنانے اور تعینات کرنے کے لئے آپ کو **Azure AI User** یا **Azure AI Owner** کی ضرورت ہے۔

---

## حوالہ جات

- [جلدی آغاز: اپنا پہلا ہوسٹ شدہ ایجنٹ تعینات کریں (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [ہوسٹ شدہ ایجنٹس کیا ہیں؟](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS Code میں ہوسٹ شدہ ایجنٹ ورک فلو تیار کریں](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [ایک ہوسٹ شدہ ایجنٹ تعینات کریں](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry کے لیے RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [آرکیٹیکچر کا جائزہ ایجنٹ نمونہ](https://github.com/Azure-Samples/agent-architecture-review-sample) - حقیقی دنیا کا ہوسٹ شدہ ایجنٹ MCP ٹولز، Excalidraw ڈایاگرامز، اور دوہری تعیناتی کے ساتھ

---


## لائسنس

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->