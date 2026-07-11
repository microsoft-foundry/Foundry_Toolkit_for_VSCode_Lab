# ماڈیول 8 - مسائل کا حل

یہ ماڈیول عام غلطیوں، اصلاحات، اور ملٹی ایجنٹ ورک فلو سے متعلق خاص ڈیبگنگ حکمت عملیوں کا احاطہ کرتا ہے۔

## ایجنٹ کے آؤٹ پٹ کے مسائل

### GapAnalyzer کہتا ہے "میرے پاس ابھی تک میچنگ رپورٹ نہیں ہے"

**علامت:** GapAnalyzer کا جواب آپ کو "غیر موجود مہارتیں" اور "سرٹیفیکیشن خلا" والی میچنگ رپورٹ چسپاں کرنے کو کہتا ہے۔ یہ اس وقت بھی ہوتا ہے جب آپ نے ریزیومے اور جاب کی تفصیل دونوں بھیجی ہوں۔

**سبب:** JD متن کو JD ایجنٹ کو نیچے نہیں بھیجا گیا۔ `context_mode="last_agent"` کے ساتھ، `resume_executor` واحد ایگزیکیوٹر ہے جو صارف کا اصل پیغام دیکھتا ہے۔ اگر `RESUME_PARSER_INSTRUCTIONS` اپنی آؤٹ پٹ میں JD متن شامل نہیں کرتا تو JD ایجنٹ کے پاس تجزیہ کرنے کے لئے JD نہیں ہوتا، MatchingAgent فٹ اسکور حساب نہیں کر سکتا، اور GapAnalyzer کو بے معنی ان پٹ ملتا ہے۔

**تشخیص:**

سرور لاگز میں MatchingAgent اسپین کو تلاش کریں۔ اگر اس میں:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
پاس-تھرو غائب یا خراب ہے۔

**اصلاح:** تصدیق کریں کہ `main.py` میں `RESUME_PARSER_INSTRUCTIONS` میں `[JOB DESCRIPTION PASS-THROUGH]` سیکشن اور قاعدہ موجود ہے:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
اسی طرح تصدیق کریں کہ `JOB_DESCRIPTION_INSTRUCTIONS` میں `[PARSED RESUME PASS-THROUGH]` ریلے قاعدہ موجود ہے:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
اگر کوئی بھی ہدایت بلاک سکہ ساز جادوگر سے نکلا ہوا اسٹب ہے، تو اسے [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) سے مکمل ورژن سے بدل دیں۔

### MatchingAgent آؤٹ پٹ دیتا ہے "fit score حساب نہیں کر سکتا - کوئی JD فراہم نہیں کیا گیا"

یہ اوپر والے ہی بنیادی سبب کا نتیجہ ہے۔ MatchingAgent کو JD Agent کی آؤٹ پٹ موصول ہوئی لیکن `[PARSED RESUME PASS-THROUGH]` سیکشن غائب یا خالی تھا، اس لئے وہ دونوں پروفائلز کا موازنہ نہیں کر سکا۔ تصدیق کریں:
1. `JOB_DESCRIPTION_INSTRUCTIONS` میں ریلے قاعدہ شامل ہے: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` ایجنٹ کو `[JD REQUIREMENTS]` اور `[PARSED RESUME PASS-THROUGH]` سیکشنز کو تلاش کرنے کو کہتا ہے۔

دونوں ہدایت بلاکس کو [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) سے مکمل ورژنز سے بدل دیں۔

### جواب دو بار ظاہر ہوتا ہے

**علامت:** Agent Inspector کے جواب میں GapAnalyzer کا آؤٹ پٹ (یا پورا پائپ لائن آؤٹ پٹ) دو بار ظاہر ہوتا ہے۔

**سبب:** `WorkflowBuilder` ان پٹ ایجز کے لیے OR-سیمانٹکس استعمال کرتا ہے - ایک نیچے والا ایگزیکیوٹر اس وقت چل پڑتا ہے جب **کوئی بھی** پریڈیسیسر مکمل ہو جائے۔ اگر `matching_executor` کے دو ان پٹ ایجز ہوں (ایک `resume_executor` سے اور ایک `jd_executor` سے)، تو یہ دو بار چلتا ہے: ایک بار جب ResumeParser مکمل ہو اور دوسری بار جب JD ایجنٹ مکمل ہو۔ پھر GapAnalyzer بھی دو بار چلتا ہے۔

**اصلاح:** اس بات کو یقینی بنائیں کہ `WorkflowBuilder` گراف صرف یک بعدی پائپ لائن ہو بغیر فین-ان کے:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # ریزیومے ایگزیکییوٹر سے نہیں
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

اگر آپ کے پاس کوئی غیر ضروری `.add_edge(resume_executor, matching_executor)` لائن ہے، تو اسے ہٹا دیں۔ JD ایجنٹ کے آؤٹ پٹ میں `[PARSED RESUME PASS-THROUGH]` ریلے پہلے ہی MatchingAgent کو ریزیومے تک رسائی دیتا ہے۔

---

## ماحول اور کنفیگریشن مسائل

### غائب یا غلط `.env` ویلیوز

`.env` فائل `PersonalCareerCopilot/` ڈائریکٹری میں ہونی چاہیے (وہی سطح جہاں `main.py` ہے):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

متوقع `.env` مواد:

**راستہ A - Foundry کلاؤڈ:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**راستہ B - Foundry لوکل:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> دونوں راستے `FOUNDRY_PROJECT_ENDPOINT` استعمال کرتے ہیں۔ ویلیو مختلف ہے: کلاؤڈ میں `https://` Foundry اینڈ پوائنٹ ہے؛ لوکل میں `http://localhost:5273/v1` ہے۔ Path B کے لئے درست ماڈل علیاس کی تصدیق کے لئے `foundry model list` چلائیں۔

> **اپنے `FOUNDRY_PROJECT_ENDPOINT` کو تلاش کرنا:** 
- VS Code میں **Foundry Toolkit** سائڈ بار کھولیں → اپنے پروجیکٹ پر رائٹ کلک کریں → **Copy Project Endpoint**۔ 
- یا [Azure پورٹل](https://portal.azure.com) پر جائیں → اپنا Foundry پروجیکٹ → **Overview** → **Project endpoint**۔

> **اپنے `AZURE_AI_MODEL_DEPLOYMENT_NAME` کو تلاش کرنا:** Foundry Toolkit سائڈبار میں، اپنے پروجیکٹ کو پھیلائیں → **Models** → اپنا تعینات کردہ ماڈل نام تلاش کریں (مثلاً `gpt-4.1-mini`)۔

### Env ویری ایبل کی ترجیح

`main.py` میں `load_dotenv(override=True)` استعمال ہوتا ہے، جس کا مطلب ہے:

| ترجیح | ماخذ | جب دونوں سیٹ ہوں تو کون جیتے گا؟ |
|----------|--------|------------------------|
| 1 (سب سے زیادہ) | `.env` فائل | ہاں |
| 2 | شیل / کنٹینر ماحول متغیر | جب اسی کلید کی `.env` میں موجودگی نہ ہو تب استعمال ہوتا ہے |

مقامی ترقی میں، اس کا مطلب ہے کہ `.env` حقائق کا ماخذ ہے (`.env` کی تبدیلیاں فوری طور پر رنز پر اثر انداز ہوتی ہیں)۔ ہوسٹڈ تعیناتی میں، Foundry کنٹینر سطح پر ماحول کے متغیرات ڈالتی ہے؛ چونکہ `.env` اس لیب سیٹ اپ کے لیے تعینات تصویر کا حصہ نہیں ہے، اس لئے ڈالے گئے کنٹینر ویلیوز استعمال ہوتے ہیں۔

---

## ورژن مطابقت

### پیکج ورژن میٹرکس

ملٹی ایجنٹ ورک فلو مخصوص پیکج ورژنز کا تقاضا کرتا ہے۔ مختلف ورژنز رن ٹائم غلطیاں پیدا کرتے ہیں۔

| پیکج | مطلوبہ ورژن | چیک کرنے کا حکم |
|---------|-----------------|---------------|
| `agent-framework-foundry` | تازہ ترین | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | تازہ ترین | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | تازہ ترین | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### عام ورژن کی غلطیاں

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# حل: ایجنٹ-فریم ورک-فاؤنڈری دوبارہ انسٹال کریں
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# درست کریں: mcp پیکیج کو اپ گریڈ کریں
pip install mcp --upgrade
```

### تمام ورژنز کی ایک ساتھ تصدیق کریں

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

متوقع آؤٹ پٹ:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## تعیناتی کے مسائل

### تعیناتی کے بعد کنٹینر شروع نہیں ہوتا

1. **کنٹینر لاگز چیک کریں:**
   - **Foundry Toolkit** سائڈبار کھولیں → **Hosted Agents (Preview)** کو پھیلائیں → اپنے ایجنٹ پر کلک کریں → ورژن کو پھیلائیں → **Container Details** → **Logs**۔
   - Python اسٹیک ٹریس یا غائب ماڈیول کی غلطیاں تلاش کریں۔

2. **عام کنٹینر اسٹارٹ اپ کی ناکامیاں:**

   | لاگز میں خرابی | سبب | اصلاح |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` میں پیکج غائب | پیکج شامل کریں، دوبارہ تعینات کریں |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` یا `.env` کے env ویری ایبل سیٹ نہیں | `agent.yaml` میں **environment_variables** سیکشن (ہوسٹڈ) یا `.env` (لوکل) اپڈیٹ کریں |
   | `azure.identity.CredentialUnavailableError` | مینیجڈ شناخت مرتب نہیں ہوئی | Foundry خودکار طریقے سے سیٹ کرتا ہے - توسیع کے ذریعے تعیناتی یقینی بنائیں |
   | `OSError: port 8088 already in use` | Dockerfile میں غلط پورٹ یا پورٹ تنازعہ | Dockerfile میں `EXPOSE 8088` اور `CMD ["python", "main.py"]` چیک کریں |
   | کنٹینر کوڈ 1 کے ساتھ بند ہوتا ہے | `main()` میں ناتحمل شدہ استثناء | پہلے مقامی طور پر جانچیں ([Module 5](05-test-locally.md)) تاکہ تعیناتی سے پہلے غلطیاں پکڑی جا سکیں |

3. **اصلاح کے بعد دوبارہ تعینات کریں:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → وہی ایجنٹ منتخب کریں → نیا ورژن تعینات کریں۔

### تعیناتی میں بہت وقت لگنا

ملٹی ایجنٹ کنٹینرز اس لئے زیادہ وقت لیتے ہیں کیونکہ وہ اسٹارٹ اپ پر 4 ایجنٹ انسٹینسز بناتے ہیں۔ معمول کے اسٹارٹ اپ اوقات:

| مرحلہ | متوقع دورانیہ |
|-------|------------------|
| کنٹینر امیج بنانا | 1-3 منٹ |
| ACR کو امیج پش کرنا | 30-60 سیکنڈ |
| کنٹینر اسٹارٹ (سنگل ایجنٹ) | 15-30 سیکنڈ |
| کنٹینر اسٹارٹ (ملٹی ایجنٹ) | 30-120 سیکنڈ |
| ایجنٹ کھیل کے میدان میں دستیاب | "شروع ہو گیا" کے 1-2 منٹ بعد |

> اگر "منتظر" کی حالت 5 منٹ سے زیادہ برقرار رہے، تو کنٹینر لاگز میں خرابیوں کو چیک کریں۔

---

## RBAC اور اجازت کے مسائل

### `403 Forbidden` یا `AuthorizationFailed`

آپ کو اپنے Foundry پروجیکٹ پر **[Foundry User](https://aka.ms/foundry-ext-project-role)** رول کی ضرورت ہے (جو پہلے **Azure AI User** کہلاتا تھا - رول ID تبدیل نہیں ہوا):

1. [Azure پورٹل](https://portal.azure.com) پر جائیں → اپنا Foundry **پروجیکٹ** ریسورس۔
2. **Access control (IAM)** → **Role assignments** پر کلک کریں۔
3. اپنا نام تلاش کریں → تصدیق کریں کہ **Foundry User** (یا پرانا نام **Azure AI User**) فہرست میں ہے۔
4. اگر موجود نہیں ہے: **Add** → **Add role assignment** → **Foundry User** تلاش کریں → اپنے اکاؤنٹ کو تفویض کریں۔

تفصیلات کے لیے [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) دستاویزات دیکھیں۔

### ماڈل کی تعیناتی قابل رسائی نہیں

اگر ایجنٹ ماڈل سے متعلق غلطیاں دیتا ہے:

1. تصدیق کریں کہ ماڈل تعینات شدہ ہے: Foundry سائڈبار → پروجیکٹ پھیلائیں → **Models** → `gpt-4.1-mini` (یا آپ کا ماڈل) کی حیثیت **Succeeded** ہو۔
2. تعیناتی نام کا موازنہ کریں: `.env` (یا `agent.yaml`) میں `AZURE_AI_MODEL_DEPLOYMENT_NAME` اور سائڈبار میں اصل تعیناتی نام کو موازنہ کریں۔
3. اگر تعیناتی کی میعاد ختم ہو گئی (مفت سطح): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) سے دوبارہ تعینات کریں (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)۔

---

## Foundry لوکل کے مسائل (راستہ B)

### Foundry لوکل سروس نہیں چل رہی

```powershell
# حیثیت چیک کریں
foundry local status

# اگر سروس بند ہو تو اسے شروع کریں
foundry local start
```

| علامت | سبب | اصلاح |
|---------|-------|-----|
| ہیلتھ چیک `503` دیتا ہے | سروس شروع نہیں ہوئی | `foundry local start` چلائیں یا Foundry Toolkit سائڈبار میں **Start** پر کلک کریں |
| ہیلتھ چیک ٹائم آؤٹ ہوتا ہے | ماڈل ابھی لوڈ ہو رہا ہے | شروع کرنے کے بعد 30–60 سیکنڈ انتظار کریں؛ بڑے ماڈلز کو زیادہ وقت لگتا ہے |
| `/v1/health` پر `StatusCode: 404` | غلط پورٹ | ڈیفالٹ `5273` ہے۔ اصل پورٹ کے لیے `foundry local status` چیک کریں |
| وسائل ناکافی ہیں | Foundry لوکل کو تقریباً 4 GB RAM خالی چاہیے | دوسری ایپلیکیشنز بند کریں |
| ماڈل ڈاؤن لوڈ ناکام | کم ڈسک اسپیس | ماڈلز 2–8 GB کے ہوتے ہیں۔ جگہ خالی کریں، پھر `foundry model pull <name>` چلائیں |

### ماڈل کا نام میل نہیں کھاتا

```powershell
# ڈاؤن لوڈ کردہ ماڈلز اور ان کے درست القابات کی فہرست بنائیں
foundry model list
```

`.env` میں `AZURE_AI_MODEL_DEPLOYMENT_NAME` کو وہی علیاس سیٹ کریں جو دکھایا گیا ہے (مثلاً `phi-4-mini`, نہ کہ `Phi-4-mini`)۔

### لوکل رن پر `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (راستہ B)

لیب کا `main.py` `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` استعمال کرتا ہے۔ Foundry لوکل کو یہ ویری ایبل لوکل سروس کی طرف اشارہ کرنا چاہیے - **نہ کہ** `AZURE_AI_PROJECT_ENDPOINT`۔ یقینی بنائیں کہ آپ کا `.env` یہ رکھتا ہو:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP ٹول اب بھی ایک خارجہ کال بناتا ہے (راستہ B)

یہ متوقع ہے۔ `search_microsoft_learn_for_plan` ٹول `https://learn.microsoft.com/api/mcp` سے لرننگ ریسورسز حاصل کرتا ہے۔ **صرف مہارت کے نام کی تلاش کا سوال** نیٹ ورک پر جاتا ہے - ریزیومے اور JD متن مکمل طور پر آپ کے ڈیوائس پر پروسیس ہوتے ہیں اور کبھی منتقل نہیں ہوتے۔ اگر مکمل آف لائن آپریشن ضروری ہو تو ٹول میں ایک `try/except` فول بیک شامل کریں جو جب اینڈپوائنٹ دستیاب نہ ہو تو ایک ساکن `learn.microsoft.com` URL واپس کرے۔

---

## مدد حاصل کرنا

اگر آپ اوپر دی گئی اصلاحات آزمانے کے بعد پھنس گئے ہیں:

1. **سرور لاگز چیک کریں** - اکثر غلطیاں ٹرمینل میں Python اسٹیک ٹریس فراہم کرتی ہیں۔ پوری ٹریس کو پڑھیں۔
2. **غلطی کا پیغام تلاش کریں** - غلطی کا متن کاپی کریں اور [Microsoft Q&A برائے Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) میں تلاش کریں۔
3. **مسئلہ کھولیں** - ورکشاپ ریپوزیٹری پر مسئلہ کھولیں: [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) درج ذیل کے ساتھ:
   - غلطی کا پیغام یا اسکرین شاٹ
   - آپ کے پیکج ورژنز (`pip list | Select-String "agent-framework"`)
   - آپ کا Python ورژن (`python --version`)
   - یہ مسئلہ لوکل ہے یا تعیناتی کے بعد

---

### چیک پوائنٹ

- [ ] آپ جانتے ہیں کہ `.env` کنفیگریشن کے مسائل کو کیسے چیک اور درست کیا جائے
- [ ] آپ مطلوبہ میٹرکس کے مطابق پیکج ورژنز کی تصدیق کر سکتے ہیں
- [ ] آپ تعیناتی کی ناکامیوں کے لئے کنٹینر لاگز چیک کرنا جانتے ہیں
- [ ] آپ Azure پورٹل میں RBAC رولز کی تصدیق کر سکتے ہیں

---

**پچھلا:** [07 - Verify in Playground](07-verify-in-playground.md) · **اگلا:** [09 - Summary →](09-summary.md) · **ہوم:** [Lab 02 README](../README.md) · [ورکشاپ ہوم](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->