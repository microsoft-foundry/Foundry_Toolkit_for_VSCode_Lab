# ماژول ۸ - عیب‌یابی

این ماژول یک راهنمای مرجع برای هر مشکل رایجی است که در طول کارگاه رخ می‌دهد. آن را نشانک کنید - هر زمان مشکلی پیش آمد دوباره به آن مراجعه خواهید کرد.

---

## ۱. خطاهای دسترسی

### ۱.۱ اجازه `agents/write` رد شده است

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**علت اصلی:** شما در سطح **پروژه** نقش `Azure AI User` را ندارید. این رایج‌ترین خطا در کارگاه است.

**رفع مشکل - مرحله به مرحله:**

1. به [https://portal.azure.com](https://portal.azure.com) بروید.
2. در نوار جستجوی بالا، نام **پروژه Foundry** خود را وارد کنید (مثلاً `workshop-agents`).
3. **مهم:** روی نتیجه‌ای که نوع آن **"Microsoft Foundry project"** است کلیک کنید، نه حساب والد/هاب. این‌ها منابع مختلفی با حوزه‌های RBAC متفاوت هستند.
4. در ناوبری سمت چپ صفحه پروژه، روی **Access control (IAM)** کلیک کنید.
5. تب **Role assignments** را باز کنید تا ببینید آیا نقش برای شما تعریف شده است یا نه:
   - نام یا ایمیل خود را جستجو کنید.
   - اگر `Azure AI User` قبلاً هست → خطا دلیل دیگری دارد (مرحله ۸ را پایین‌تر چک کنید).
   - اگر نیست → ادامه دهید برای افزودن آن.
6. روی **+ Add** → **Add role assignment** کلیک کنید.
7. در تب **Role**:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) را جستجو کنید.
   - آن را از نتایج انتخاب کنید.
   - روی **Next** کلیک کنید.
8. در تب **Members**:
   - گزینه **User, group, or service principal** را انتخاب کنید.
   - روی **+ Select members** کلیک کنید.
   - نام یا ایمیل خود را جستجو کرده و خودتان را انتخاب کنید.
   - روی **Select** کلیک کنید.
9. روی **Review + assign** → دوباره **Review + assign** کلیک کنید.
10. **۱-۲ دقیقه صبر کنید** - تغییرات RBAC زمان می‌برد تا اعمال شوند.
11. عملیات ناموفق را دوباره امتحان کنید.

> **چرا Owner/Contributor کافی نیست:** Azure RBAC دو نوع مجوز دارد - *اقدامات مدیریت* و *اقدامات داده*. Owner و Contributor فقط اجازه اقدامات مدیریت (ایجاد منابع، ویرایش تنظیمات) را می‌دهند، اما عملیات عامل‌ها نیاز به مجوز `agents/write` بعنوان **اقدام داده** دارد که فقط در نقش‌های `Azure AI User`، `Azure AI Developer` یا `Azure AI Owner` وجود دارد. برای اطلاعات بیشتر به [مستندات Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) مراجعه کنید.

### ۱.۲ خطای `AuthorizationFailed` هنگام تامین منابع

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**علت اصلی:** شما اجازه ایجاد یا تغییر منابع Azure در این اشتراک/گروه منابع را ندارید.

**رفع مشکل:**
1. از مدیر اشتراک خود بخواهید نقش **Contributor** را روی گروه منبعی که پروژه Foundry شما در آن قرار دارد به شما اختصاص دهد.
2. یا اینکه آن‌ها پروژه Foundry را بسازند و به شما نقش **Azure AI User** بر روی پروژه بدهند.

### ۱.۳ خطای `SubscriptionNotRegistered` برای [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**علت اصلی:** اشتراک Azure فراهم‌کننده مورد نیاز برای Foundry را ثبت نکرده است.

**رفع مشکل:**

1. ترمینال را باز کنید و دستور زیر را اجرا کنید:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. منتظر بمانید ثبت کامل شود (ممکن است ۱-۵ دقیقه طول بکشد):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   خروجی مورد انتظار: `"Registered"`
3. عملیات را دوباره امتحان کنید.

---

## ۲. خطاهای Docker (فقط اگر Docker نصب است)

> Docker برای این کارگاه **اختیاری** است. این خطاها فقط زمانی صادقند که Docker Desktop نصب شده و افزونه Foundry تلاش به ساخت محلی کانتینر کند.

### ۲.۱ Docker daemon اجرا نمی‌شود

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**رفع مشکل - مرحله به مرحله:**

1. **Docker Desktop** را در منوی استارت (ویندوز) یا در بخش برنامه‌ها (macOS) پیدا کنید و اجرا کنید.
2. منتظر بمانید پنجره Docker Desktop پیغام **"Docker Desktop is running"** را نشان دهد - معمولاً ۳۰-۶۰ ثانیه طول می‌کشد.
3. آیکون نهنگ Docker را در نوار وضعیت سیستم (ویندوز) یا نوار منو (macOS) پیدا کنید و روی آن نگه دارید برای دیدن وضعیت.
4. در ترمینال تایپ کنید:
   ```powershell
   docker info
   ```
   اگر اطلاعات سیستم Docker (نسخه سرور، درایور ذخیره‌سازی، و غیره) را نشان داد، یعنی Docker اجرا می‌شود.
5. **ویندوز خاص:** اگر باز هم Docker اجرا نشد:
   - وارد Docker Desktop شوید → **Settings** (آیکون چرخ‌دنده) → **General**.
   - اطمینان حاصل کنید که گزینه **Use the WSL 2 based engine** فعال است.
   - روی **Apply & restart** کلیک کنید.
   - اگر WSL 2 نصب نیست، در PowerShell با دسترسی مدیر دستور `wsl --install` را اجرا کرده و سیستم را ری‌استارت کنید.
6. دوباره استقرار را امتحان کنید.

### ۲.۲ ساخت Docker با خطاهای وابستگی مواجه می‌شود

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**رفع مشکل:**
1. فایل `requirements.txt` را باز کنید و مطمئن شوید نام همه پکیج‌ها صحیح است.
2. اطمینان حاصل کنید نسخه‌های مشخص شده درست هستند:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. ابتدا در محلی تست نصب انجام دهید:
   ```bash
   pip install -r requirements.txt
   ```
4. اگر از شاخص بسته خصوصی استفاده می‌کنید، اطمینان حاصل کنید Docker به آن دسترسی شبکه دارد.

### ۲.۳ ناسازگاری پلتفرم کانتینر (اپل سیلیکون)

اگر از مک با تراشه Apple Silicon (M1/M2/M3/M4) استفاده می‌کنید، کانتینر باید برای `linux/amd64` ساخته شود چون زمان اجرا کانتینر Foundry از AMD64 استفاده می‌کند.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> دستور استقرار افزونه Foundry معمولاً این کار را به طور خودکار انجام می‌دهد. اگر خطاهای مرتبط با معماری مشاهده کردید، به صورت دستی با پرچم `--platform` بسازید و با تیم Foundry تماس بگیرید.

---

## ۳. خطاهای احراز هویت

### ۳.۱ [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) موفق به دریافت توکن نشد

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**علت اصلی:** هیچ‌یک از منابع اعتبارسنجی در زنجیره `DefaultAzureCredential` توکن معتبر ندارد.

**رفع مشکل - هر مرحله را به ترتیب امتحان کنید:**

1. **دوباره ورود به سیستم از طریق Azure CLI** (رایج‌ترین راه حل):
   ```bash
   az login
   ```
   یک پنجره مرورگر باز می‌شود. وارد شوید و سپس به VS Code بازگردید.

2. **انتخاب اشتراک صحیح:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   اگر این اشتراک درستی نیست:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **دوباره ورود به سیستم از طریق VS Code:**
   - روی آیکون **Accounts** (شکل آدمک) در پایین-چپ VS Code کلیک کنید.
   - روی نام اکانت خود کلیک کرده و **Sign Out** را بزنید.
   - دوباره روی آیکون اکانت کلیک کرده و **Sign in to Microsoft** را بزنید.
   - فرایند ورود به سیستم مرورگر را کامل کنید.

4. **Service principal (فقط در سناریوهای CI/CD):**
   - این متغیرهای محیطی را در `.env` خود قرار دهید:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - سپس فرایند عامل را مجدداً راه‌اندازی کنید.

5. **بررسی کش توکن:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   اگر این مرحله شکست خورد، توکن CLI شما منقضی شده است. دوباره `az login` را اجرا کنید.

### ۳.۲ توکن در محلی کار می‌کند اما در استقرار میزبان نه

**علت اصلی:** عامل میزبان از هویت مدیریت‌شده سیستم استفاده می‌کند که با اعتبار شخصی شما متفاوت است.

**رفع مشکل:** این رفتار مورد انتظار است - هویت مدیریت شده به صورت خودکار در هنگام استقرار فراهم می‌شود. اگر عامل میزبان هنوز خطای احراز هویت می‌دهد:
1. بررسی کنید هویت مدیریت شده پروژه Foundry به منبع Azure OpenAI دسترسی دارد.
2. مطمئن شوید مقدار `PROJECT_ENDPOINT` در `agent.yaml` صحیح است.

---

## ۴. خطاهای مدل

### ۴.۱ استقرار مدل پیدا نشد

```
Error: Model deployment not found / The specified deployment does not exist
```

**رفع مشکل - مرحله به مرحله:**

1. فایل `.env` خود را باز کنید و مقدار `AZURE_AI_MODEL_DEPLOYMENT_NAME` را یادداشت کنید.
2. نوار کناری **Microsoft Foundry** را در VS Code باز کنید.
3. پروژه خود را باز کنید → **Model Deployments** را گسترش دهید.
4. نام استقرار نمایش داده شده را با مقدار در `.env` مقایسه کنید.
5. نام به **حساس به حروف بزرگ و کوچک** است - `gpt-4o` با `GPT-4o` متفاوت است.
6. اگر نام‌ها مطابقت ندارند، در `.env` نام دقیق نمایش داده شده را وارد کنید.
7. اگر استقرار میزبان است، همچنین در `agent.yaml` مقدار را بروز کنید:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### ۴.۲ مدل با محتوای غیرمنتظره پاسخ می‌دهد

**رفع مشکل:**
1. ثابت `EXECUTIVE_AGENT_INSTRUCTIONS` در `main.py` را بررسی کنید. مطمئن شوید بریده نشده یا خراب نشده است.
2. تنظیم دمای مدل را چک کنید (اگر قابل تنظیم است) - مقادیر پایین‌تر خروجی‌های قطعی‌تری می‌دهند.
3. مدل مستقر شده را مقایسه کنید (مثلاً `gpt-4o` مقابل `gpt-4o-mini`) - مدل‌های مختلف قابلیت‌های متفاوتی دارند.

---

## ۵. خطاهای استقرار

### ۵.۱ مجوز کشیدن تصویر ACR

```
Error: AcrPullUnauthorized
```

**علت اصلی:** هویت مدیریت شده پروژه Foundry قادر به کشیدن تصویر کانتینر از Azure Container Registry نیست.

**رفع مشکل - مرحله به مرحله:**

1. به [https://portal.azure.com](https://portal.azure.com) بروید.
2. در نوار جستجوی بالا **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** را جستجو کنید.
3. روی رجیستری مرتبط با پروژه Foundry خود کلیک کنید (معمولاً در همان گروه منابع).
4. در ناوبری سمت چپ، روی **Access control (IAM)** کلیک کنید.
5. روی **+ Add** → **Add role assignment** کلیک کنید.
6. نقش **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** را جستجو و انتخاب کنید. سپس روی **Next** کلیک کنید.
7. گزینه **Managed identity** را انتخاب و روی **+ Select members** کلیک کنید.
8. هویت مدیریت شده پروژه Foundry را پیدا و انتخاب کنید.
9. روی **Select** → **Review + assign** → **Review + assign** کلیک کنید.

> این نقش معمولاً به صورت خودکار توسط افزونه Foundry تنظیم می‌شود. اگر این خطا را دیدید، احتمالاً تنظیم خودکار با شکست مواجه شده است. می‌توانید دوباره استقرار را امتحان کنید - افزونه شاید تنظیم را مجدداً انجام دهد.

### ۵.۲ عامل پس از استقرار شروع نمی‌شود

**نشانه‌ها:** وضعیت کانتینر بیش از ۵ دقیقه روی "Pending" باقی می‌ماند یا "Failed" نمایش می‌دهد.

**رفع مشکل - مرحله به مرحله:**

1. پنل کناری **Microsoft Foundry** را در VS Code باز کنید.
2. روی عامل میزبانی خود کلیک کرده و نسخه آن را انتخاب کنید.
3. در پنل جزئیات، بخش **Container Details** را چک کنید و به دنبال بخش یا لینک **Logs** بگردید.
4. لاگ‌های شروع کانتینر را بخوانید. دلایل رایج:

| پیام لاگ | علت | رفع مشکل |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | وابستگی گم شده | آن را به `requirements.txt` اضافه کرده و مجدداً استقرار دهید |
| `KeyError: 'PROJECT_ENDPOINT'` | متغیر محیطی گم شده | متغیر env را در `agent.yaml` زیر `env:` اضافه کنید |
| `OSError: [Errno 98] Address already in use` | تداخل پورت | مطمئن شوید در `agent.yaml` مقدار `port: 8088` است و فقط یک فرایند به آن متصل است |
| `ConnectionRefusedError` | عامل شروع به گوش دادن نکرده | در `main.py` بررسی کنید که فراخوانی `from_agent_framework()` هنگام شروع اجرا شود |

5. مشکل را برطرف کرده و سپس دوباره از [ماژول ۶](06-deploy-to-foundry.md) استقرار دهید.

### ۵.۳ زمان استقرار تمام می‌شود

**رفع مشکل:**
1. اتصال اینترنت خود را بررسی کنید - ارسال Docker ممکن است حجم زیاد (>100MB برای اولین بار) داشته باشد.
2. اگر پشت پراکسی شرکت هستید، مطمئن شوید تنظیمات پراکسی Docker Desktop تنظیم شده است: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. دوباره تلاش کنید - مشکلات شبکه ممکن است باعث خطاهای موقتی شوند.

---

## ۶. مرجع سریع: نقش‌های RBAC

| نقش | دامنه معمول | چه مجوزی می‌دهد |
|------|---------------|----------------|
| **Azure AI User** | پروژه | اقدامات داده: ساخت، استقرار و فراخوانی عامل‌ها (`agents/write`, `agents/read`) |
| **Azure AI Developer** | پروژه یا حساب | اقدامات داده + ایجاد پروژه |
| **Azure AI Owner** | حساب | دسترسی کامل + مدیریت انتساب نقش |
| **Azure AI Project Manager** | پروژه | اقدامات داده + امکان انتساب Azure AI User به دیگران |
| **Contributor** | اشتراک/گروه منابع | اقدامات مدیریت (ایجاد/حذف منابع). **شامل اقدامات داده نمی‌شود** |
| **Owner** | اشتراک/گروه منابع | اقدامات مدیریت + انتساب نقش. **شامل اقدامات داده نمی‌شود** |
| **Reader** | هر جا | دسترسی فقط خواندنی مدیریت |

> **نکته کلیدی:** نقش‌های `Owner` و `Contributor` **شامل اقدامات داده نیستند**. شما همیشه برای عملیات عامل‌ها به نقش `Azure AI *` نیاز دارید. حداقل نقش برای این کارگاه **Azure AI User** در حوزه **پروژه** است.

---

## ۷. فهرست بررسی تکمیل کارگاه

از این برای تایید نهایی که همه مراحل را کامل کرده‌اید استفاده کنید:

| شماره | آیتم | ماژول | گذراندن؟ |
|---|------|--------|---|
| ۱ | تمام پیش‌نیازها نصب و تایید شده‌اند | [00](00-prerequisites.md) | |
| ۲ | Foundry Toolkit و افزونه‌های Foundry نصب شده‌اند | [01](01-install-foundry-toolkit.md) | |
| ۳ | پروژه Foundry ایجاد شده (یا پروژه موجود انتخاب شده) | [02](02-create-foundry-project.md) | |
| ۴ | مدل مستقر شده (مثلاً gpt-4o) | [۰۲](02-create-foundry-project.md) | |
| ۵ | نقش کاربر Azure AI در محدوده پروژه اختصاص داده شده | [۰۲](02-create-foundry-project.md) | |
| ۶ | چارچوب پروژه عامل میزبانی شده ساخته شده (agent/) | [۰۳](03-create-hosted-agent.md) | |
| ۷ | فایل `.env` با PROJECT_ENDPOINT و MODEL_DEPLOYMENT_NAME پیکربندی شده | [۰۴](04-configure-and-code.md) | |
| ۸ | دستورالعمل‌های عامل در main.py سفارشی شده | [۰۴](04-configure-and-code.md) | |
| ۹ | محیط مجازی ایجاد شده و وابستگی‌ها نصب شده | [۰۴](04-configure-and-code.md) | |
| ۱۰ | عامل به صورت محلی با F5 یا ترمینال آزمایش شده (۴ تست دود گذشته) | [۰۵](05-test-locally.md) | |
| ۱۱ | در سرویس Foundry Agent مستقر شده | [۰۶](06-deploy-to-foundry.md) | |
| ۱۲ | وضعیت کانتینر "شروع شده" یا "در حال اجرا" را نشان می‌دهد | [۰۶](06-deploy-to-foundry.md) | |
| ۱۳ | در VS Code Playground تأیید شده (۴ تست دود گذشته) | [۰۷](07-verify-in-playground.md) | |
| ۱۴ | در Foundry Portal Playground تأیید شده (۴ تست دود گذشته) | [۰۷](07-verify-in-playground.md) | |

> **تبریک!** اگر همه موارد علامت زده شده‌اند، کل کارگاه را به پایان رسانده‌اید. شما یک عامل میزبانی شده را از ابتدا ساخته، به صورت محلی آزمایش کرده، آن را در Microsoft Foundry مستقر کرده و در محیط تولید اعتبارسنجی کرده‌اید.

---

**قبلی:** [۰۷ - تأیید در Playground](07-verify-in-playground.md) · **خانه:** [README کارگاه](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه ماشینی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما برای دقت تلاش می‌کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است حاوی خطاها یا نادرستی‌هایی باشند. سند اصلی به زبان بومی خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حساس، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما مسئول هیچ گونه سوءتفاهم یا تفسیر نادرست ناشی از استفاده از این ترجمه نیستیم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->