# ماژول ۸ - عیب‌یابی (چندعامل‌گی)

این ماژول پوشش‌دهنده خطاهای رایج، رفع مشکل‌ها و استراتژی‌های اشکال‌زدایی خاص برای جریان کاری چندعامل است. برای مشکلات کلی استقرار Foundry، به [راهنمای عیب‌یابی آزمایشگاه ۰۱](../../lab01-single-agent/docs/08-troubleshooting.md) نیز مراجعه کنید.

---

## مرجع سریع: خطا → رفع

| خطا / نشانه | علت محتمل | رفع |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | فایل `.env` ناقص است یا مقادیری تنظیم نشده‌اند | ایجاد فایل `.env` با `PROJECT_ENDPOINT=<your-endpoint>` و `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | محیط مجازی فعال نشده یا وابستگی‌ها نصب نشده | اجرای `.\.venv\Scripts\Activate.ps1` سپس `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | بسته MCP نصب نشده (در requirements نیست) | اجرای `pip install mcp` یا اطمینان از وجود آن به عنوان وابستگی گذرا در `requirements.txt` |
| عامل شروع می‌شود اما پاسخ خالی برمی‌گرداند | عدم تطابق `output_executors` یا یال‌های گمشده | اطمینان از `output_executors=[gap_analyzer]` و وجود تمام یال‌ها در `create_workflow()` |
| فقط ۱ کارت گپ (باقی گم شده‌اند) | دستورالعمل‌های GapAnalyzer ناقص است | افزودن پاراگراف `CRITICAL:` به `GAP_ANALYZER_INSTRUCTIONS` - مراجعه به [ماژول ۳](03-configure-agents.md) |
| امتیاز برازش ۰ یا غایب است | MatchingAgent داده‌های بالادستی دریافت نکرده | اطمینان از وجود هردو `add_edge(resume_parser, matching_agent)` و `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | سرور MCP فراخوانی ابزار را رد کرده | اتصال اینترنت را بررسی کنید. تلاش برای باز کردن `https://learn.microsoft.com/api/mcp` در مرورگر. دوباره امتحان کنید |
| هیچ آدرس Microsoft Learn در خروجی نیست | ابزار MCP ثبت نشده یا نقطه انتهایی اشتباه است | اطمینان از `tools=[search_microsoft_learn_for_plan]` در GapAnalyzer و صحت `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | فرآیند دیگری در حال استفاده از پورت ۸۰۸۸ است | اجرای `netstat -ano \| findstr :8088` (ویندوز) یا `lsof -i :8088` (macOS/Linux) و قطع فرآیند متعارض |
| `Address already in use: port 5679` | تداخل پورت Debugpy | خاتمه جلسات دیباگ دیگر. اجرای `netstat -ano \| findstr :5679` برای پیدا کردن و اتمام فرآیند |
| Agent Inspector باز نمی‌شود | سرور کامل راه‌اندازی نشده یا تداخل پورت وجود دارد | منتظر بمانید تا پیام "Server running" ظاهر شود. بررسی آزاد بودن پورت ۵۶۷۹ |
| `azure.identity.CredentialUnavailableError` | وارد Azure CLI نشده‌اید | اجرای `az login` سپس ری‌استارت سرور |
| `azure.core.exceptions.ResourceNotFoundError` | استقرار مدل وجود ندارد | بررسی کنید `MODEL_DEPLOYMENT_NAME` با مدل مستقر شده در پروژه Foundry شما مطابقت دارد |
| وضعیت کانتینر "Failed" پس از استقرار | کرش کانتینر در شروع | لاگ‌های کانتینر در پنل کناری Foundry را بررسی کنید. معمولاً متغیر محیطی یا خطای وارد کردن حذف شده |
| استقرار بیش از ۵ دقیقه "Pending" نشان می‌دهد | زمان‌بری طولانی کانتینر برای شروع یا محدودیت منابع | تا ۵ دقیقه منتظر بمانید برای چندعامل (۴ نمونه عامل ایجاد می‌کند). اگر هنوز معلق است، لاگ‌ها را چک کنید |
| `ValueError` از `WorkflowBuilder` | پیکربندی گراف نامعتبر است | اطمینان از تنظیم `start_executor`، اینکه `output_executors` لیست است و هیچ یال مدور وجود ندارد |

---

## مشکلات محیطی و پیکربندی

### مقادیر `.env` ناقص یا اشتباه

فایل `.env` باید در دایرکتوری `PersonalCareerCopilot/` قرار داشته باشد (همسطح با `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

محتوای مورد انتظار `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **یافتن PROJECT_ENDPOINT:**  
- پنل کناری **Microsoft Foundry** را در VS Code باز کنید → روی پروژه‌تان راست‌کلیک کنید → **Copy Project Endpoint** را بزنید.  
- یا به [Azure Portal](https://portal.azure.com) بروید → پروژه Foundry شما → **Overview** → **Project endpoint**.

> **یافتن MODEL_DEPLOYMENT_NAME:** در پنل کناری Foundry، پروژه‌تان را گسترش دهید → **Models** → نام مدل مستقر شده را بیابید (مثلاً `gpt-4.1-mini`).

### تقدم متغیرهای محیطی

`main.py` از `load_dotenv(override=False)` استفاده می‌کند، یعنی:

| اولویت | منبع | آیا بر هر دو تنظیم شده اعمال می‌شود؟ |
|----------|--------|------------------------|
| ۱ (بالاترین) | متغیر محیطی shell | بله |
| ۲ | فایل `.env` | فقط اگر متغیر shell تنظیم نشده باشد |

این یعنی متغیرهای محیطی زمان اجرا Foundry (تنظیم شده از طریق `agent.yaml`) در استقرار میزبانی‌شده، بر مقادیر `.env` اولویت دارند.

---

## سازگاری نسخه‌ها

### ماتریس نسخه بسته‌ها

جریان کاری چندعامل به نسخه‌های خاص بسته‌ها نیاز دارد. ناسازگاری نسخه‌ها موجب خطاهای زمان اجرا می‌شود.

| بسته | نسخه مورد نیاز | فرمان بررسی |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | نسخه پیش‌انتشار آخر | `pip show agent-dev-cli` |
| پایتون | نسخه 3.10 به بالا | `python --version` |

### خطاهای رایج نسخه

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# اصلاح شده: ارتقا به نسخه rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**عدم یافتن `agent-dev-cli` یا ناسازگاری Inspector:**

```powershell
# رفع: نصب با گزینه --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# اصلاح: ارتقاء بسته mcp
pip install mcp --upgrade
```

### بررسی همه نسخه‌ها همزمان

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

خروجی مورد انتظار:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## مشکلات ابزار MCP

### ابزار MCP هیچ نتیجه‌ای بازنمی‌گرداند

**نشانه:** کارت‌های گپ می‌گویند "No results returned from Microsoft Learn MCP" یا "No direct Microsoft Learn results found".

**دلایل ممکن:**

1. **مشکل شبکه** - نقطه انتهایی MCP (`https://learn.microsoft.com/api/mcp`) غیرقابل دسترس است.
   ```powershell
   # آزمون اتصال
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
  
اگر این `۲۰۰` برگرداند، نقطه انتهایی قابل دسترسی است.

2. **پرسش خیلی خاص است** - نام مهارت بیش از حد تخصصی برای جستجوی Microsoft Learn است.  
   - این موضوع برای مهارت‌های بسیار تخصصی طبیعی است. ابزار URL جایگزین در پاسخ دارد.

3. **زمان جلسه MCP منقضی شده** - اتصال Streamable HTTP به‌خاطر زمان منقضی شده قطع شده است.  
   - درخواست را دوباره بفرستید. جلسات MCP زودگذر هستند و ممکن است نیاز به اتصال مجدد داشته باشند.

### توضیح لاگ‌های MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| لاگ | معنی | اقدام |
|-----|---------|--------|
| `GET → 405` | بررسی‌های کلاینت MCP هنگام راه‌اندازی | عادی - نادیده بگیرید |
| `POST → 200` | فراخوانی ابزار موفق | انتظار می‌رود |
| `DELETE → 405` | بررسی‌های کلاینت MCP هنگام پاکسازی | عادی - نادیده بگیرید |
| `POST → 400` | درخواست بد (پرسش بدفرم) | پارامتر `query` در `search_microsoft_learn_for_plan()` را بررسی کنید |
| `POST → 429` | محدودیت نرخ | صبر کنید و دوباره تلاش کنید. پارامتر `max_results` را کاهش دهید |
| `POST → 500` | خطای سرور MCP | موقتی - دوباره تلاش کنید. اگر مداوم بود، API MCP مایکروسافت ممکن است قطع باشد |
| قطع اتصال | مشکل شبکه یا سرور MCP در دسترس نیست | اینترنت را بررسی کنید. تلاش کنید با `curl https://learn.microsoft.com/api/mcp` |

---

## مشکلات استقرار

### کانتینر پس از استقرار شروع نمی‌شود

1. **بررسی لاگ‌های کانتینر:**  
   - پنل کناری **Microsoft Foundry** را باز کنید → گسترش **Hosted Agents (Preview)** → روی عامل خود کلیک کنید → نسخه را گسترش دهید → **Container Details** → **Logs**.  
   - به دنبال استک‌تریس پایتون یا خطاهای ماژول‌های از دست رفته باشید.

2. **اشکالات متداول شروع کانتینر:**

   | خطا در لاگ‌ها | علت | رفع |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | بسته‌ای در `requirements.txt` فراموش شده | افزودن بسته و استقرار مجدد |
   | `RuntimeError: Missing required environment variable` | متغیرهای محیطی در `agent.yaml` تنظیم نشده‌اند | به‌روزرسانی بخش `environment_variables` در `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity پیکربندی نشده | Foundry این کار را خودکار انجام می‌دهد - اطمینان حاصل کنید با افزونه استقرار می‌دهید |
   | `OSError: port 8088 already in use` | فایل Docker پورت اشتباه اعلام کرده یا تداخل پورت وجود دارد | بررسی `EXPOSE 8088` در Dockerfile و `CMD ["python", "main.py"]` |
   | خروج کانتینر با کد ۱ | استثناء کنترل نشده در `main()` | ابتدا به صورت محلی تست کنید ([ماژول ۵](05-test-locally.md)) تا خطاها قبل از استقرار گرفته شوند |

3. **پس از رفع مشکل دوباره استقرار دهید:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → انتخاب همان عامل → استقرار نسخه جدید.

### زمان استقرار طولانی است

کانتینرهای چندعامل زمان بیشتری برای شروع نیاز دارند زیرا ۴ نمونه عامل ایجاد می‌کنند. مدت زمان‌های معمول راه‌اندازی:

| مرحله | زمان مورد انتظار |
|-------|------------------|
| ساخت ایمیج کانتینر | ۱-۳ دقیقه |
| پوش ایمیج به ACR | ۳۰-۶۰ ثانیه |
| شروع کانتینر (عامل تک) | ۱۵-۳۰ ثانیه |
| شروع کانتینر (چندعامل) | ۳۰-۱۲۰ ثانیه |
| دسترسی عامل در Playground | ۱-۲ دقیقه بعد از "Started" |

> اگر وضعیت "Pending" بیش از ۵ دقیقه باقی ماند، لاگ‌های کانتینر را برای خطاها بررسی کنید.

---

## مشکلات RBAC و دسترسی‌ها

### `403 Forbidden` یا `AuthorizationFailed`

برای پروژه Foundry خود به نقش **[Azure AI User](https://aka.ms/foundry-ext-project-role)** نیاز دارید:

1. وارد [Azure Portal](https://portal.azure.com) شوید → منبع **پروژه** Foundry خود را انتخاب کنید.  
2. روی **Access control (IAM)** کلیک کنید → **Role assignments**.  
3. نام خود را جستجو کنید → اطمینان حاصل کنید **Azure AI User** فهرست شده باشد.  
4. اگر نبود: **Add** → **Add role assignment** → جستجو برای **Azure AI User** → انتساب به حساب کاربری خود.

برای جزئیات بیشتر به مستندات [RBAC برای Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) مراجعه کنید.

### عدم دسترسی به استقرار مدل

اگر عامل خطاهای مربوط به مدل برمی‌گرداند:

1. اطمینان حاصل کنید مدل مستقر شده است: پنل کناری Foundry → گسترش پروژه → **Models** → بررسی وضعیت `gpt-4.1-mini` (یا مدل شما) با وضعیت **Succeeded**.  
2. مطابقت نام استقرار: مقایسه `MODEL_DEPLOYMENT_NAME` در `.env` (یا `agent.yaml`) با نام استقرار واقعی در پنل جانبی.  
3. اگر استقرار منقضی شده (در سطح رایگان): دوباره استقرار دهید از [کاتالوگ مدل](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## مشکلات Agent Inspector

### Inspector باز می‌شود اما "Disconnected" نشان می‌دهد

1. اطمینان از اجرای سرور: در ترمینال پیام "Server running on http://localhost:8088" را بررسی کنید.  
2. بررسی پورت `5679`: Inspector از طریق debugpy روی پورت ۵۶۷۹ متصل می‌شود.  
   ```powershell
   netstat -ano | findstr :5679
   ```
  
3. سرور را ری‌استارت کنید و Inspector را دوباره باز کنید.

### Inspector پاسخ ناقص نشان می‌دهد

پاسخ‌های چندعامل طولانی هستند و به صورت جریان افزایشی (stream) می‌آیند. منتظر اتمام پاسخ کامل باشید (ممکن است ۳۰-۶۰ ثانیه بسته به تعداد کارت‌های گپ و فراخوانی‌های MCP طول بکشد).

اگر پاسخ مدام ناقص بود:  
- بررسی کنید دستورالعمل‌های GapAnalyzer بلوک `CRITICAL:` را دارند که جلوی ترکیب کارت‌های گپ می‌شود.  
- محدودیت توکن مدل خود را بررسی کنید - `gpt-4.1-mini` تا ۳۲ هزار توکن خروجی را پشتیبانی می‌کند که کافی است.

---

## نکات بهبود عملکرد

### پاسخ‌های کند

جریان‌های کاری چندعامل ذاتاً کندتر از تک‌عامل هستند به خاطر وابستگی‌های ترتیبی و فراخوانی‌های ابزار MCP.

| بهینه‌سازی | چگونه | تاثیر |
|-------------|-----|--------|
| کاهش فراخوانی‌های MCP | کاهش پارامتر `max_results` در ابزار | کاهش رفت‌وآمدهای HTTP |
| ساده کردن دستورالعمل‌ها | پرسش‌های کوتاه‌تر و متمرکزتر عامل | پیش‌بینی سریع‌تر LLM |
| استفاده از `gpt-4.1-mini` | نسبت به `gpt-4.1` سریع‌تر برای توسعه | حدود ۲ برابر سرعت بیشتر |
| کاهش جزئیات کارت گپ | ساده‌تر کردن فرمت کارت گپ در دستورالعمل GapAnalyzer | خروجی کمتر برای تولید |

### زمان پاسخ معمولی (لوکال)

| پیکربندی | زمان مورد انتظار |
|--------------|---------------|
| `gpt-4.1-mini`، ۳-۵ کارت گپ | ۳۰-۶۰ ثانیه |
| `gpt-4.1-mini`، ۸+ کارت گپ | ۶۰-۱۲۰ ثانیه |
| `gpt-4.1`، ۳-۵ کارت گپ | ۶۰-۱۲۰ ثانیه |
---

## دریافت کمک

اگر پس از تلاش برای رفع مشکلات بالا هنوز گیر کرده‌اید:

1. **لاگ‌های سرور را بررسی کنید** - بیشتر خطاها در ترمینال یک traceback پایتون تولید می‌کنند. کل traceback را بخوانید.
2. **پیام خطا را جستجو کنید** - متن خطا را کپی کنید و در [Microsoft Q&A برای Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) جستجو کنید.
3. **یک مسئله باز کنید** - یک issue در [مخزن ورکشاپ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) با موارد زیر ثبت کنید:
   - پیام خطا یا تصویر صفحه
   - نسخه‌های بسته‌های شما (`pip list | Select-String "agent-framework"`)
   - نسخه پایتون شما (`python --version`)
   - اینکه مشکل محلی است یا پس از استقرار رخ داده است

---

### بررسی نهایی

- [ ] شما می‌توانید رایج‌ترین خطاهای چندعامله را با استفاده از جدول مرجع سریع شناسایی و رفع کنید
- [ ] می‌دانید چگونه مشکلات پیکربندی `.env` را بررسی و اصلاح کنید
- [ ] می‌توانید نسخه‌های بسته‌ها را با ماتریس مورد نیاز تطابق دهید
- [ ] ورودی‌های لاگ MCP را می‌فهمید و می‌توانید شکست‌های ابزار را تشخیص دهید
- [ ] می‌دانید چگونه لاگ‌های کانتینر را برای شکست‌های استقرار بررسی کنید
- [ ] می‌توانید نقش‌های RBAC را در پرتال Azure تأیید کنید

---

**قبلی:** [07 - تأیید در محیط بازی](07-verify-in-playground.md) · **خانه:** [راهنمای آزمایشگاه ۰۲](../README.md) · [خانه ورکشاپ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است حاوی خطاها یا نواقصی باشند. سند اصلی به زبان بومی آن باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما مسئولیتی در قبال سوءتفاهم‌ها یا تفسیرهای نادرست ناشی از استفاده از این ترجمه نداریم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->