# کارگاه Foundry Toolkit + نمایندگان میزبانی شده Foundry

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

ساخت، تست و استقرار نمایندگان هوش مصنوعی به **خدمات نماینده Microsoft Foundry** به‌عنوان **نمایندگان میزبانی شده** - کاملاً از VS Code با استفاده از **افزونه Microsoft Foundry** و **Foundry Toolkit**.

> **نمایندگان میزبانی شده در حال حاضر در پیش‌نمایش هستند.** مناطق پشتیبانی شده محدود هستند - به [دسترسی منطقه‌ای](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) مراجعه کنید.

> پوشه `agent/` درون هر آزمایشگاه توسط افزونه Foundry به‌صورت **خودکار ساخته می‌شود** - سپس کد را سفارشی می‌کنید، به صورت محلی تست می‌کنید و مستقر می‌نمایید.

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](./README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ترجیح می‌دهید به صورت محلی کلون کنید؟**
>
> این مخزن شامل بیش از ۵۰ ترجمه زبانی است که به طور قابل توجهی اندازه دانلود را افزایش می‌دهد. برای کلون کردن بدون ترجمه‌ها، از sparse checkout استفاده کنید:
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
> این به شما همه چیز لازم برای تکمیل دوره با دانلود بسیار سریع‌تر را می‌دهد.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## معماری

```mermaid
flowchart TB
    subgraph Local["توسعه محلی (VS Code)"]
        direction TB
        FE["افزونه Microsoft Foundry"]
        FoundryToolkit["افزونه Foundry Toolkit"]
        Scaffold["کد عامل اسکافولد شده
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["بازرس عامل
        (آزمایش محلی)"]
        FE -- "ایجاد عامل میزبانی شده جدید" --> Scaffold
        Scaffold -- "اشکال‌زدایی F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["ثبت کانتینر Azure"]
        AgentService["سرویس عامل Foundry
        (زمان اجرای عامل میزبانی شده)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["زمین بازی Foundry
        و زمین بازی VS Code"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "استقرار
    (ساخت و ارسال داکر)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "آزمایش درخواست‌ها" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**روند:** افزونه Foundry نماینده را تولید می‌کند → شما کد و دستورالعمل‌ها را سفارشی می‌کنید → به صورت محلی با Agent Inspector آزمایش می‌کنید → به Foundry مستقر می‌کنید (تصویر داکر به ACR ارسال می‌شود) → در Playground بررسی می‌کنید.

---

## آنچه خواهید ساخت

| آزمایشگاه | شرح | وضعیت |
|-----|-------------|--------|
| **آزمایشگاه ۰۱ - نماینده تک‌نفره** | ساخت **نماینده "توضیح دهید انگار من یک مدیر ارشد هستم"**، تست محلی و استقرار در Foundry | ✅ موجود |
| **آزمایشگاه ۰۲ - جریان کاری چند نماینده‌ای** | ساخت **"ارزیاب تناسب رزومه → شغل"** - همکاری ۴ نماینده برای امتیازدهی تناسب رزومه و ایجاد نقشه راه یادگیری | ✅ موجود |

---

## معرفی نماینده مدیر ارشد

در این کارگاه، شما نماینده **"توضیح دهید انگار من یک مدیر ارشد هستم"** را خواهید ساخت - نماینده هوش مصنوعی که اصطلاحات فنی پیچیده را گرفته و به خلاصه‌هایی آرام و آماده ارائه در جلسات هیئت مدیره تبدیل می‌کند. چون بیایید صادق باشیم، هیچ‌کس در سطح مدیران عالی نمی‌خواهد درباره «اتمام استخر رشته‌ها به خاطر تماس‌های همزمان معرفی شده در نسخه ۳.۲» بشنود.

من این نماینده را پس از چندین بار که گزارش پس از حادثه من به این پاسخ رسید: *«پس... وبسایت بالا است یا نه؟»* ساختم.

### چطور کار می‌کند

شما یک بروزرسانی فنی به آن می‌دهید. آن یک خلاصه اجرایی برمی‌گرداند - سه نکته اصلی، بدون اصطلاحات فنی، بدون ردپای پشته، بدون نگرانی‌های وجودی. فقط **چه اتفاقی افتاده**، **تأثیر کسب‌وکار** و **گام بعدی**.

### نمونه عملکرد

**شما می‌گویید:**
> «تاخیر API به دلیل اتمام استخر رشته‌ها به خاطر تماس‌های همزمان معرفی شده در نسخه ۳.۲ افزایش یافته است.»

**نماینده پاسخ می‌دهد:**

> **خلاصه اجرایی:**
> - **چه اتفاقی افتاد:** پس از آخرین انتشار، سیستم کند شد.
> - **تأثیر کسب‌وکار:** برخی کاربران طی استفاده از سرویس با تأخیر مواجه شدند.
> - **گام بعدی:** تغییر معکوس شده و اصلاحی قبل از مستقرسازی مجدد آماده می‌شود.

### چرا این نماینده؟

این یک نماینده بسیار ساده با هدف واحد است - مناسب برای یادگیری کامل جریان کاری نمایندگان میزبانی شده بدون گیر کردن در زنجیره‌های ابزار پیچیده. و صادقانه؟ هر تیم مهندسی می‌تواند یکی از این‌ها را داشته باشد.

---

## ساختار کارگاه

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

> **توجه:** پوشه `agent/` درون هر آزمایشگاه همان چیزی است که **افزونه Microsoft Foundry** هنگام اجرای `Microsoft Foundry: Create a New Hosted Agent` از Command Palette تولید می‌کند. سپس فایل‌ها با دستورالعمل‌ها، ابزارها و پیکربندی نماینده شما سفارشی می‌شوند. آزمایشگاه ۰۱ به شما نحوه ساخت این از ابتدا را آموزش می‌دهد.

---

## شروع کار

### ۱. کلون کردن مخزن

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### ۲. ایجاد محیط مجازی پایتون

```bash
python -m venv venv
```

فعال‌سازی آن:

- **ویندوز (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / لینوکس:**
  ```bash
  source venv/bin/activate
  ```

### ۳. نصب پیش‌نیازها

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### ۴. پیکربندی متغیرهای محیطی

فایل نمونه `.env` داخل پوشه نماینده را کپی کرده و مقادیر خود را وارد کنید:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

فایل `workshop/lab01-single-agent/agent/.env` را ویرایش کنید:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### ۵. دنبال کردن آزمایشگاه‌های کارگاه

هر آزمایشگاه مستقل با ماژول‌های خود است. با **آزمایشگاه ۰۱** شروع کنید تا اصول اولیه را یاد بگیرید، سپس به **آزمایشگاه ۰۲** برای جریان‌های کاری چند نماینده‌ای بروید.

#### آزمایشگاه ۰۱ - نماینده تک‌نفره ([دستورالعمل کامل](workshop/lab01-single-agent/README.md))

| # | ماژول | لینک |
|---|--------|------|
| 1 | خواندن پیش‌نیازها | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | نصب Foundry Toolkit و افزونه Foundry | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | ایجاد پروژه Foundry | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | ایجاد نماینده میزبانی شده | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | پیکربندی دستورالعمل‌ها و محیط | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | تست محلی | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | استقرار در Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | تایید در playground | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | عیب‌یابی | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### آزمایشگاه ۰۲ - جریان کاری چند نماینده‌ای ([دستورالعمل کامل](workshop/lab02-multi-agent/README.md))

| # | ماژول | لینک |
|---|--------|------|
| 1 | پیش‌نیازها (آزمایشگاه ۰۲) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | آشنایی با معماری چند نماینده‌ای | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | ساختاردهی پروژه چند نماینده‌ای | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | پیکربندی نمایندگان و محیط | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | الگوهای هماهنگی | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | تست محلی (چند نماینده‌ای) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | استقرار در Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | تأیید در محیط آزمایش | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | رفع اشکال (چند عاملی) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

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
| ایجاد پروژه جدید Foundry | **مالک Azure AI** در منبع Foundry |
| استقرار در پروژه موجود (منابع جدید) | **مالک Azure AI** + **همکار** در اشتراک |
| استقرار در پروژه کاملاً پیکربندی شده | **خواننده** در حساب + **کاربر Azure AI** در پروژه |

> **مهم:** نقش‌های Azure `مالک` و `همکار` فقط شامل مجوزهای *مدیریتی* می‌شوند و نه مجوزهای *توسعه* (عملیات داده). برای ساخت و استقرار عامل‌ها نیاز به **کاربر Azure AI** یا **مالک Azure AI** دارید.

---

## مراجع

- [شروع سریع: استقرار اولین عامل میزبانی شده (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [عامل‌های میزبانی شده چیستند؟](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [ایجاد گردش کار عامل میزبانی شده در VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [استقرار یک عامل میزبانی شده](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC برای Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [نمونه عامل بازبینی معماری](https://github.com/Azure-Samples/agent-architecture-review-sample) - عامل میزبانی شده در دنیای واقعی با ابزارهای MCP، نمودارهای Excalidraw و استقرار دوگانه

---

## مجوز

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**توجه**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما برای دقت تلاش می‌کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان مبدأ باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما در قبال هرگونه سو تفاهم یا تفسیر نادرست ناشی از استفاده از این ترجمه مسئولیتی نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->