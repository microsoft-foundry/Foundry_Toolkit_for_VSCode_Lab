# ماژول ۸ - عیب‌یابی

این ماژول به خطاهای رایج، رفع مشکلات، و استراتژی‌های عیب‌یابی خاص روند کاری چندعامله می‌پردازد.

## مشکلات خروجی عامل

### GapAnalyzer می‌گوید «من هنوز گزارش مطابقت را ندارم»

**نشانه:** پاسخ GapAnalyzer از شما می‌خواهد تا گزارشی با معیارهای «مهارت‌های گمشده» و «شکاف‌های گواهی‌نامه» ارائه دهید. این اتفاق حتی وقتی می‌فرستید هر دو رزومه و توصیف شغل رخ می‌دهد.

**علت:** متن JD (توصیف شغل) به JD Agent منتقل نشده است. با `context_mode="last_agent"`، `resume_executor` تنها اجرایی است که پیام اصلی کاربر را می‌بیند. اگر `RESUME_PARSER_INSTRUCTIONS` شامل متن JD در خروجی خود نباشد، JD Agent چیزی برای تجزیه ندارد، MatchingAgent نمی‌تواند امتیاز تطابق محاسبه کند، و GapAnalyzer ورودی بی‌معنی دریافت می‌کند.

**تشخیص:**

در لاگ‌های سرور، به بازه MatchingAgent نگاه کنید. اگر شامل:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
 گذر انتقال ناقص یا خراب است.

**رفع:** تأیید کنید که `RESUME_PARSER_INSTRUCTIONS` در `main.py` شامل بخشی به نام `[JOB DESCRIPTION PASS-THROUGH]` و قانون زیر باشد:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
 همچنین مطمئن شوید که `JOB_DESCRIPTION_INSTRUCTIONS` شامل یک قانون واسط `[PARSED RESUME PASS-THROUGH]` است:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
 اگر هر کدام از بلوک‌های دستورات stub از جادوگر اسکافولد باشد، آن را با نسخه کامل از [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) جایگزین کنید.

### MatchingAgent خروجی «نمی‌توان امتیاز تطابق را محاسبه کرد - JD ارائه نشده» می‌دهد

این همان علت ریشه‌ای بالاست. MatchingAgent خروجی JD Agent را دریافت کرده اما بخش `[PARSED RESUME PASS-THROUGH]` از دست رفته یا خالی بوده و نمی‌توانسته دو پروفایل را مقایسه کند. تأیید کنید:
1. `JOB_DESCRIPTION_INSTRUCTIONS` شامل قانون واسط: `کپی [PARSED RESUME] عیناً - Matching Agent آن را در پایین‌دست نیاز دارد.` باشد.
2. `MATCHING_AGENT_INSTRUCTIONS` به عامل می‌گوید به دنبال بخش‌های `[JD REQUIREMENTS]` و `[PARSED RESUME PASS-THROUGH]` باشد.

هر دو بلوک دستورات را با نسخه‌های کامل از [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) جایگزین کنید.

### پاسخ دو بار ظاهر می‌شود

**نشانه:** خروجی GapAnalyzer (یا کل خروجی خط لوله) دو بار در پاسخ Agent Inspector ظاهر می‌شود.

**علت:** `WorkflowBuilder` از منطق OR برای یال‌های ورودی استفاده می‌کند - یک مجری پایین‌دست به محض تکمیل شدن هر یک از پیش‌نیازها اجرا می‌شود. اگر `matching_executor` دو یال ورودی داشته باشد (یکی از `resume_executor` و دیگری از `jd_executor`)، دو بار اجرا می‌شود: یک‌بار هنگام پایان ResumeParser و بار دیگر هنگام پایان JD Agent. سپس GapAnalyzer نیز دوبار اجرا می‌شود.

**رفع:** اطمینان حاصل کنید که گراف `WorkflowBuilder` یک خط لوله کاملاً متوالی و بدون پرش ورودی (fan-in) است:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # نه از resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

اگر خط `.add_edge(resume_executor, matching_executor)` اضافی دارید، آن را حذف کنید. واسطه `[PARSED RESUME PASS-THROUGH]` در خروجی JD Agent دسترسی MatchingAgent به رزومه را فراهم می‌کند.

---

## مشکلات محیط و پیکربندی

### مقادیر `.env` از دست رفته یا نادرست

فایل `.env` باید در دایرکتوری `PersonalCareerCopilot/` باشد (در همان سطح با `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

محتوای مورد انتظار `.env`:

**مسیر A - کلاود فوندری:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**مسیر B - فوندری محلی:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> هر دو مسیر از `FOUNDRY_PROJECT_ENDPOINT` استفاده می‌کنند. مقدار متفاوت است: کلاود از نقطه انتهایی `https://` فوندری استفاده می‌کند؛ محلی از `http://localhost:5273/v1`. برای تأیید نام مستعار مدل دقیق مسیر B فرمان `foundry model list` را اجرا کنید.

> **چگونه `FOUNDRY_PROJECT_ENDPOINT` خود را پیدا کنیم:** 
- در نوار کناری **Foundry Toolkit** در VS Code → روی پروژه خود راست کلیک کنید → **کپی نقطه انتهایی پروژه**. 
- یا به [Azure Portal](https://portal.azure.com) بروید → پروژه فوندری خود → **نمای کلی** → **نقطه انتهایی پروژه**.

> **چگونه `AZURE_AI_MODEL_DEPLOYMENT_NAME` را پیدا کنیم:** در نوار کناری Foundry Toolkit، پروژه خود را گسترش دهید → **مدل‌ها** → نام مدل مستقر شده خود را بیابید (مثلاً `gpt-4.1-mini`).

### تقدم متغیرهای محیطی

`main.py` از `load_dotenv(override=True)` استفاده می‌کند، که بدان معنی است:

| اولویت | منبع | برنده هنگام تنظیم هر دو؟ |
|----------|--------|------------------------|
| ۱ (بالاترین) | فایل `.env` | بله |
| ۲ | پوسته / متغیر محیطی کانتینر | زمانی استفاده می‌شود که همان کلید در `.env` نباشد |

در توسعه محلی، این باعث می‌شود `.env` منبع حقیقت باشد (ویرایش `.env` بلافاصله روی اجراها تأثیر می‌گذارد). در استقرار میزبانی شده، فوندری متغیرهای محیطی را در سطح کانتینر تزریق می‌کند؛ چون `.env` بخشی از تصویر مستقر شده برای این تنظیم آزمایشگاه نیست، مقادیر تزریق شده کانتینر استفاده می‌شوند.

---

## سازگاری نسخه

### ماتریس نسخه بسته‌ها

روند کاری چندعامله به نسخه‌های خاص بسته‌ها نیاز دارد. نسخه‌های ناسازگار باعث خطاهای زمان اجرا می‌شوند.

| بسته | نسخه مورد نیاز | فرمان بررسی |
|---------|-----------------|---------------|
| `agent-framework-foundry` | جدیدترین | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | جدیدترین | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | جدیدترین | `pip show debugpy` |
| پایتون | ۳.۱۲+ | `python --version` |

### خطاهای رایج نسخه

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# رفع مشکل: نصب مجدد agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# اصلاح: ارتقاء بسته mcp
pip install mcp --upgrade
```

### بررسی همه نسخه‌ها به صورت همزمان

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

خروجی مورد انتظار:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## مشکلات استقرار

### کانتینر پس از استقرار شروع نمی‌شود

۱. **لاگ‌های کانتینر را بررسی کنید:**
   - نوار کناری **Foundry Toolkit** را باز کنید → بخش **Hosted Agents (Preview)** را باز کنید → روی عامل خود کلیک کنید → نسخه را باز کنید → **جزئیات کانتینر** → **لاگ‌ها**.
   - به دنبال تراس استک پایتون یا خطاهای ماژول گمشده بگردید.

۲. **شکست‌های رایج شروع کانتینر:**

   | خطا در لاگ‌ها | علت | رفع |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | فایل `requirements.txt` فاقد بسته‌ای است | بسته را اضافه کرده و مجدداً استقرار دهید |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | متغیرهای محیطی `agent.yaml` یا `.env` تنظیم نشده‌اند | بخش `environment_variables` در `agent.yaml` (میزبانی شده) یا `.env` (محلی) را به‌روزرسانی کنید |
   | `azure.identity.CredentialUnavailableError` | شناسه مدیریت تنظیم نشده | فوندری این را خودکار تنظیم می‌کند - اطمینان حاصل کنید که از طریق افزونه استقرار می‌دهید |
   | `OSError: port 8088 already in use` | Dockerfile پورت اشتباه را باز کرده یا تداخل پورت وجود دارد | `EXPOSE 8088` در Dockerfile و `CMD ["python", "main.py"]` را بررسی کنید |
   | خروجی کانتینر با کد ۱ | استثنای رسیدگی نشده در `main()` | ابتدا در محلی ([ماژول ۵](05-test-locally.md)) تست کنید تا خطاها قبل از استقرار شناسایی شوند |

۳. **پس از رفع:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → همان عامل را انتخاب کنید → نسخه جدید را مستقر کنید.

### استقرار زمان زیادی می‌برد

کانتینرهای چندعامله به دلیل ایجاد ۴ نمونه عامل هنگام شروع، زمان بیشتری برای شروع دارند. زمان‌های معمول شروع:

| مرحله | مدت زمان مورد انتظار |
|-------|------------------|
| ساخت تصویر کانتینر | ۱-۳ دقیقه |
| ارسال تصویر به ACR | ۳۰-۶۰ ثانیه |
| شروع کانتینر (عامل واحد) | ۱۵-۳۰ ثانیه |
| شروع کانتینر (چندعامله) | ۳۰-۱۲۰ ثانیه |
| عامل در Playground قابل دسترسی است | ۱-۲ دقیقه پس از «شروع شده» |

> اگر وضعیت «در انتظار» بیش از ۵ دقیقه باقی ماند، لاگ‌های کانتینر را برای خطاها بررسی کنید.

---

## مشکلات RBAC و مجوزها

### خطای `403 Forbidden` یا `AuthorizationFailed`

شما نیاز به نقش **[Foundry User](https://aka.ms/foundry-ext-project-role)** در پروژه فوندری خود دارید (قبلاً با نام **Azure AI User** شناخته می‌شد - شناسه نقش تغییر نکرده):

۱. به [Azure Portal](https://portal.azure.com) → منبع **پروژه** فوندری خود بروید.
۲. کلیک کنید روی **کنترل دسترسی (IAM)** → **تخصیص نقش‌ها**.
۳. نام خود را جستجو کنید → تأیید کنید **Foundry User** (یا برچسب قدیمی **Azure AI User**) در لیست باشد.
۴. اگر نیست: **افزودن** → **افزودن تخصیص نقش** → جستجو کنید برای **Foundry User** → به حساب خود اختصاص دهید.

برای جزئیات بیشتر به مستندات [RBAC برای Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) مراجعه کنید.

### استقرار مدل قابل دسترسی نیست

اگر عامل خطاهای مربوط به مدل برمی‌گرداند:

۱. تأیید کنید مدل مستقر شده: نوار کنار فوندری → پروژه را گسترش دهید → **مدل‌ها** → ببیند مدل `gpt-4.1-mini` (یا مدل شما) با وضعیت **موفق** وجود دارد.
۲. تأیید کنید نام استقرار مطابقت دارد: `AZURE_AI_MODEL_DEPLOYMENT_NAME` در `.env` (یا `agent.yaml`) را با نام واقعی استقرار در نوار کنار مقایسه کنید.
۳. اگر استقرار منقضی شده (طبقه رایگان): از [کاتالوگ مدل](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) مجدداً استقرار دهید (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## مشکلات Foundry Local (مسیر B)

### سرویس Foundry Local اجرا نمی‌شود

```powershell
# بررسی وضعیت
foundry local status

# اگر سرویس متوقف شده بود، آن را شروع کنید
foundry local start
```

| نشانه | علت | رفع |
|---------|-------|-----|
| برگشت چک سلامت `503` | سرویس شروع نشده | اجرای `foundry local start` یا کلیک روی **شروع** در نوار کناری Foundry Toolkit |
| تایم‌اوت در چک سلامت | مدل هنوز بارگذاری می‌شود | ۳۰–۶۰ ثانیه پس از شروع صبر کنید؛ مدل‌های بزرگ‌تر زمان بیشتری می‌برند |
| `StatusCode: 404` در `/v1/health` | پورت اشتباه | پیش‌فرض `5273` است. پورت واقعی را با `foundry local status` بررسی کنید |
| منابع ناکافی | Foundry Local به ~4 گیگابایت رم آزاد نیاز دارد | برنامه‌های دیگر را ببندید |
| دانلود مدل با شکست مواجه می‌شود | فضای دیسک کم است | مدل‌ها ۲–۸ گیگابایت هستند. فضا آزاد کنید، سپس `foundry model pull <name>` را اجرا کنید |

### عدم تطابق نام مدل

```powershell
# مدل‌های دانلود شده و نام‌های مستعاری دقیق آن‌ها را فهرست کنید
foundry model list
```

مقدار `AZURE_AI_MODEL_DEPLOYMENT_NAME` در `.env` را دقیقاً به همان شکلی که نشان داده شده تنظیم کنید (مثلاً `phi-4-mini`، نه `Phi-4-mini`).

### خطای `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` هنگام اجرای محلی (مسیر B)

`main.py` آزمایشگاه از `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` استفاده می‌کند. Foundry Local نیاز دارد این متغیر به سرویس محلی اشاره کند - **نه** به `AZURE_AI_PROJECT_ENDPOINT`. اطمینان حاصل کنید `.env` شما شامل موارد زیر است:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### ابزار MCP هنوز فراخوانی بیرون‌روندی انجام می‌دهد (مسیر B)

این انتظار می‌رود. ابزار `search_microsoft_learn_for_plan` منابع آموزشی را از `https://learn.microsoft.com/api/mcp` واکشی می‌کند. **فقط کوئری نام مهارت** بر روی شبکه ارسال می‌شود - رزومه و متن JD کاملاً روی دستگاه شما پردازش می‌شوند و هرگز منتقل نمی‌شوند. اگر عملیات کاملاً آفلاین مورد نیاز است، یک fallback در ابزار اضافه کنید که در صورت عدم دسترسی به نقطه انتهایی، یک URL ثابت `learn.microsoft.com` را بازگرداند.

---

## گرفتن کمک

اگر پس از تلاش برای رفع مشکلات بالا هنوز گیر کرده‌اید:

۱. **لاگ‌های سرور را چک کنید** - بیشتر خطاها در ترمینال یک ردیابی استک پایتون تولید می‌کنند. کل traceback را مطالعه کنید.
۲. **متن خطا را جستجو کنید** - متن خطا را کپی کرده و در [Microsoft Q&A برای Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) جستجو کنید.
۳. **یک مسئله باز کنید** - در [مخزن ورکشاپ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) یک issue باز کنید که شامل موارد زیر باشد:
   - پیام خطا یا اسکرین‌شات
   - نسخه‌های بسته شما (`pip list | Select-String "agent-framework"`)
   - نسخه پایتون شما (`python --version`)
   - آیا مشکل محلی است یا پس از استقرار

---

### نقطه بررسی

- [ ] می‌دانید چگونه مسائل پیکربندی `.env` را بررسی و رفع کنید
- [ ] می‌توانید نسخه‌های بسته‌ها را با ماتریس مورد نیاز تطبیق دهید
- [ ] می‌دانید چگونه لاگ‌های کانتینر را برای شکست‌های استقرار بررسی کنید
- [ ] می‌توانید نقش‌های RBAC را در پرتال Azure تأیید کنید

---

**قبلی:** [۰۷ - بررسی در Playground](07-verify-in-playground.md) · **بعدی:** [۰۹ - خلاصه →](09-summary.md) · **خانه:** [Lab 02 README](../README.md) · [خانه ورکشاپ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان مادری خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما در قبال هرگونه سوء تفاهم یا برداشت نادرست ناشی از استفاده از این ترجمه مسئولیتی نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->