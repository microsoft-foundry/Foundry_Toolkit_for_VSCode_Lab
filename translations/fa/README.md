# کارگاه Foundry Toolkit + نمایندگان میزبانی شده Foundry

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

ساخت، آزمایش و استقرار نمایندگان هوش مصنوعی به **Microsoft Foundry Agent Service** به‌عنوان **نمایندگان میزبانی شده** - کاملاً از طریق VS Code با استفاده از **افزونه Microsoft Foundry** و **Foundry Toolkit**.

> **نمایندگان میزبانی شده در حال حاضر در پیش نمایش هستند.** مناطق پشتیبانی شده محدود هستند - به [دسترس‌پذیری منطقه‌ای](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) مراجعه کنید.

> پوشه `agent/` در داخل هر آزمایشگاه به صورت **خودکار توسط افزونه Foundry ایجاد می‌شود** - سپس می‌توانید کد را سفارشی کنید، به صورت محلی تست کنید و مستقر نمایید.

### 🌐 پشتیبانی چندزبانه

#### پشتیبانی از طریق GitHub Action (خودکار و همیشه به‌روز)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](./README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ترجیح می‌دهید به صورت محلی کلون کنید؟**
>
> این مخزن بیش از ۵۰ ترجمه زبان را شامل می‌شود که اندازه دانلود را به طور قابل توجهی افزایش می‌دهد. برای کلون کردن بدون ترجمه‌ها از روش sparse checkout استفاده کنید:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (ویندوز):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> این کار همه چیز لازم برای اتمام دوره را با سرعت دانلود بسیار سریع‌تر به شما می‌دهد.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## معماری

```mermaid
flowchart TB
    subgraph Local["توسعه محلی (VS Code)"]
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
        Scaffold -- "اشکال‌زدایی F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["مایکروسافت فاندری"]
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
    (localhost:8088)" --> ساختار اسکلتی
    Playground -- "آزمایش پرامپت‌ها" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**روند:** افزونه Foundry نماینده را ایجاد می‌کند → شما کد و دستورالعمل‌ها را سفارشی می‌کنید → با Agent Inspector محلی تست می‌کنید → به Foundry مستقر می‌کنید (تصویر Docker به ACR ارسال می‌شود) → در Playground تایید می‌کنید.

---

## آنچه خواهید ساخت

| آزمایشگاه | توضیحات | وضعیت |
|-----|-------------|--------|
| **آزمایشگاه ۰۱ - نماینده تک‌نفره** | ساخت **نماینده "توضیح مانند یک مدیر اجرایی"**، تست محلی و استقرار در Foundry | ✅ موجود |
| **آزمایشگاه ۰۲ - جریان کار چند نماینده‌ای** | ساخت **"ارزیاب تناسب رزومه به شغل"** - همکاری ۴ نماینده برای امتیازدهی رزومه و تولید نقشه راه یادگیری | ✅ موجود |

---

## آشنایی با نماینده اجرایی

در این کارگاه، نماینده **"توضیح مانند یک مدیر اجرایی"** را خواهید ساخت - نماینده هوش مصنوعی که اصطلاحات فنی پیچیده را به خلاصه‌های آرام، مناسب جلسات هیئت مدیره ترجمه می‌کند. چون صادقانه بگوییم، هیچ‌کس در C-suite نمی‌خواهد درباره «اتمام استخر نخ به دلیل تماس‌های همزمان معرفی شده در نسخه ۳.۲» بشنود.

این نماینده را پس از چندین مورد که گزارش کامل من پاسخ دریافت کرد: *«پس… آیا سایت پایین است یا نه؟»* ساختم.

### چگونه کار می‌کند

شما یک به‌روزرسانی فنی به آن می‌دهید. یک خلاصه اجرایی برمی‌گرداند - سه نکته گلوله‌ای، بدون اصطلاحات فنی، بدون ردپای استک، بدون ترس وجودی. فقط **چه اتفاقی افتاده**، **تاثیر کسب‌وکار** و **گام بعدی**.

### مشاهده عملکرد آن

**شما می‌گویید:**
> "زمان پاسخ API به دلیل اتمام استخر نخ ایجاد شده توسط تماس‌های همزمان معرفی شده در نسخه ۳.۲ افزایش یافته است."

**نماینده پاسخ می‌دهد:**

> **خلاصه اجرایی:**
> - **چه اتفاقی افتاده:** پس از آخرین انتشار، سیستم کند شد.
> - **تاثیر کسب‌وکار:** برخی کاربران تأخیرهایی در استفاده از سرویس تجربه کردند.
> - **گام بعدی:** تغییرات برگشت داده شده و رفع مشکل در حال آماده‌سازی پیش از استقرار مجدد است.

### چرا این نماینده؟

این یک نماینده ساده و تک‌منظوره است - مناسب برای یادگیری کامل جریان کار نماینده میزبانی شده بدون گرفتار شدن در زنجیره ابزارهای پیچیده. و صادقانه؟ هر تیم مهندسی می‌تواند یکی از این‌ها داشته باشد.

---

## ساختار کارگاه

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

> **توجه:** پوشه `agent/` در داخل هر آزمایشگاه همان چیزی است که **افزونه Microsoft Foundry** هنگام اجرای فرمان `Microsoft Foundry: Create a New Hosted Agent` در Command Palette تولید می‌کند. سپس فایل‌ها با دستورالعمل‌ها، ابزارها و پیکربندی نماینده شما سفارشی می‌شوند. آزمایشگاه ۰۱ شما را قدم به قدم با ساخت این از ابتدا همراهی می‌کند.

---

## شروع به کار

### ۱. مخزن را کلون کنید

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### ۲. ایجاد محیط مجازی پایتون

```bash
python -m venv venv
```

آن را فعال کنید:

- **ویندوز (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / لینوکس:**
  ```bash
  source venv/bin/activate
  ```

### ۳. نصب وابستگی‌ها

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### ۴. پیکربندی متغیرهای محیطی

فایل نمونه `.env` را در پوشه نماینده کپی کرده و مقادیر خود را وارد کنید:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

فایل `workshop/lab01-single-agent/agent/.env` را ویرایش کنید:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### ۵. دنبال کردن آزمایشگاه‌های کارگاه

هر آزمایشگاه مستقل با ماژول‌های خود است. با **آزمایشگاه ۰۱** برای یادگیری مبانی شروع کنید، سپس به **آزمایشگاه ۰۲** برای جریان‌های کاری چند نماینده‌ای بروید.

#### آزمایشگاه ۰۱ - نماینده تک‌نفره ([دستورالعمل کامل](workshop/lab01-single-agent/README.md))

| شماره | ماژول | لینک |
|---|--------|------|
| 1 | خواندن پیش‌نیازها | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | نصب Foundry Toolkit و افزونه Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | ایجاد پروژه Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | ایجاد نماینده میزبانی شده | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | پیکربندی دستورالعمل‌ها و محیط | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | تست به صورت محلی | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | استقرار در Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | تایید در Playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | عیب‌یابی | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### آزمایشگاه ۰۲ - جریان کار چند نماینده‌ای ([دستورالعمل کامل](workshop/lab02-multi-agent/README.md))

| شماره | ماژول | لینک |
|---|--------|------|
| 1 | پیش‌نیازها (آزمایشگاه ۰۲) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | درک معماری چند نماینده‌ای | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | ایجاد چارچوب پروژه چند نماینده‌ای | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | پیکربندی نمایندگان و محیط | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | الگوهای هماهنگی | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | تست محلی (چند نماینده‌ای) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | استقرار در Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | تأیید در محیط بازی | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | رفع اشکال (چندعامله) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## نگهدارنده

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>شیوام گویال</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## مجوزهای مورد نیاز (مرجع سریع)

| سناریو | نقش‌های مورد نیاز |
|----------|---------------|
| ایجاد پروژه جدید Foundry | **مالک Azure AI** بر روی منبع Foundry |
| استقرار در پروژه موجود (منابع جدید) | **مالک Azure AI** + **مشارکت‌کننده** بر روی اشتراک |
| استقرار در پروژه کاملاً پیکربندی شده | **خواننده** بر روی حساب + **کاربر Azure AI** بر روی پروژه |

> **مهم:** نقش‌های `مالک` و `مشارکت‌کننده` در Azure تنها شامل مجوزهای *مدیریت* هستند، نه مجوزهای *توسعه* (عملیات داده). برای ساخت و استقرار نمایندگان به **کاربر Azure AI** یا **مالک Azure AI** نیاز دارید.

---

## منابع

- [شروع سریع: استقرار اولین نماینده میزبانی شده شما (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [نمایندگان میزبانی شده چیستند؟](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [ایجاد گردش‌های کاری نمایندگان میزبانی شده در VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [استقرار یک نماینده میزبانی شده](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [مدیریت دسترسی مبتنی بر نقش برای Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [نمونه نماینده بازبینی معماری](https://github.com/Azure-Samples/agent-architecture-review-sample) - نماینده واقعی میزبانی شده با ابزارهای MCP، نمودارهای Excalidraw، و استقرار دوگانه

---


## مجوز

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان مادری خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما در قبال هرگونه سوء تفاهم یا برداشت نادرست ناشی از استفاده از این ترجمه مسئولیتی نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->