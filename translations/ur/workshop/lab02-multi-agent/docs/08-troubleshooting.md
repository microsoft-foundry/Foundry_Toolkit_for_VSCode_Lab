# ماڈیول 8 - مسائل کا حل (ملٹی ایجنٹ)

یہ ماڈیول ملٹی ایجنٹ ورک فلو سے متعلق عمومی غلطیوں، اصلاحات، اور ڈیبگنگ کی حکمت عملیوں کا احاطہ کرتا ہے۔ عمومی فانڈری تعیناتی مسائل کے لیے، [لیب 01 کے مسائل کے حل کی رہنمائی](../../lab01-single-agent/docs/08-troubleshooting.md) بھی ملاحظہ کریں۔

---

## فوری حوالہ: غلطی → حل

| غلطی / علامت | ممکنہ وجہ | حل |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` فائل موجود نہیں یا اقدار سیٹ نہیں کی گئیں | `.env` بنائیں اور `PROJECT_ENDPOINT=<your-endpoint>` اور `MODEL_DEPLOYMENT_NAME=<your-model>` شامل کریں |
| `ModuleNotFoundError: No module named 'agent_framework'` | ورچوئل ماحول فعال نہیں یا dependencies انسٹال نہیں | `.\.venv\Scripts\Activate.ps1` چلائیں پھر `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP پیکیج انسٹال نہیں (requirements میں شامل نہیں) | `pip install mcp` چلائیں یا چیک کریں کہ `requirements.txt` میں اسے بطور dependency شامل کیا گیا ہو |
| ایجنٹ شروع ہوتا ہے مگر خالی جواب لوٹاتا ہے | `output_executors` میل نہیں کھاتے یا edges غائب ہیں | چیک کریں کہ `output_executors=[gap_analyzer]` اور `create_workflow()` میں تمام edges موجود ہوں |
| صرف 1 gap کارڈ (باقی غائب) | GapAnalyzer کی ہدایات نامکمل ہیں | `GAP_ANALYZER_INSTRUCTIONS` میں `CRITICAL:` پیراگراف شامل کریں - ملاحظہ کریں [Module 3](03-configure-agents.md) |
| Fit اسکور 0 یا موجود نہیں | MatchingAgent کو اپ اسٹریم ڈیٹا نہیں ملا | یقینی بنائیں کہ `add_edge(resume_parser, matching_agent)` اور `add_edge(jd_agent, matching_agent)` دونوں موجود ہوں |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP سرور نے ٹول کال مسترد کر دی | انٹرنیٹ کنکشن چیک کریں۔ `https://learn.microsoft.com/api/mcp` براؤزر میں کھولنے کی کوشش کریں۔ دوبارہ کوشش کریں |
| آؤٹ پٹ میں Microsoft Learn URLs موجود نہیں | MCP ٹول رجسٹرڈ نہیں یا endpoint غلط ہے | چیک کریں کہ GapAnalyzer پر `tools=[search_microsoft_learn_for_plan]` اور `MICROSOFT_LEARN_MCP_ENDPOINT` درست ہیں |
| `Address already in use: port 8088` | کوئی اور عمل پورٹ 8088 استعمال کر رہا ہے | `netstat -ano \| findstr :8088` (Windows) یا `lsof -i :8088` (macOS/Linux) چلائیں اور متصادم عمل کو بند کریں |
| `Address already in use: port 5679` | Debugpy پورٹ کا تصادم | دوسرے ڈیبگ سیشنز بند کریں۔ `netstat -ano \| findstr :5679` چلا کر عمل کو بند کریں |
| ایجنٹ انسپیکٹر نہیں کھلتا | سرور مکمل طور پر نہیں چلا یا پورٹ کا تصادم | "Server running" لاگ کا انتظار کریں۔ چیک کریں کہ پورٹ 5679 خالی ہے |
| `azure.identity.CredentialUnavailableError` | Azure CLI میں سائن ان نہیں | `az login` چلائیں پھر سرور کو دوبارہ شروع کریں |
| `azure.core.exceptions.ResourceNotFoundError` | ماڈل کی تعیناتی موجود نہیں | چیک کریں کہ `MODEL_DEPLOYMENT_NAME` آپ کے فانڈری پروجیکٹ میں تعینات ماڈل سے میل کھاتا ہو |
| تعیناتی کے بعد کنٹینر کی حالت "Failed" ہے | کنٹینر اسٹارٹ پر کریش ہو گیا | فانڈری سائیڈ بار میں کنٹینر لاگز چیک کریں۔ عام مسئلہ: env var غائب یا import ایرر |
| تعیناتی "Pending" زیادہ دیر تک رہتی ہے (> 5 منٹ) | کنٹینر شروع ہونے میں زیادہ وقت لے رہا ہے یا وسائل کی حدیں | ملٹی ایجنٹ 4 ایجنٹ انسٹینسز بناتا ہے، اس لیے 5 منٹ تک انتظار کریں۔ اگر پھر بھی Pending ہے تو لاگز چیک کریں |
| `ValueError` `WorkflowBuilder` سے | گراف کی ترتیب غلط ہے | یقینی بنائیں کہ `start_executor` سیٹ ہو، `output_executors` ایک فہرست ہے، اور کوئی سرکلر ایجز نہ ہوں |

---

## ماحول اور ترتیب کے مسائل

### غائب یا غلط `.env` اقدار

`.env` فائل `PersonalCareerCopilot/` ڈائریکٹری میں ہونی چاہیے (جہاں `main.py` بھی موجود ہو):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

متوقع `.env` مواد:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **اپنا PROJECT_ENDPOINT کیسے معلوم کریں:**  
- VS Code میں **Microsoft Foundry** سائیڈ بار کھولیں → اپنے پروجیکٹ پر رائٹ کلک کریں → **Copy Project Endpoint** منتخب کریں۔  
- یا [Azure Portal](https://portal.azure.com) جائیں → اپنا فانڈری پروجیکٹ → **Overview** → **Project endpoint**۔

> **اپنا MODEL_DEPLOYMENT_NAME کیسے معلوم کریں:** فانڈری سائیڈبار میں اپنا پروجیکٹ کھولیں → **Models** → تعینات کردہ ماڈل کا نام تلاش کریں (مثلاً `gpt-4.1-mini`)۔

### Env var کی ترجیحی ترتیب

`main.py` میں `load_dotenv(override=False)` استعمال ہوتا ہے، اس کا مطلب:

| ترجیح | ذریعہ | دونوں سیٹ ہوں تو کون جیتے گا؟ |
|----------|--------|------------------------|
| 1 (اعلی) | شیل ماحول متغیر | ہاں |
| 2 | `.env` فائل | صرف اگر شیل متغیر موجود نہ ہو |

اس کا مطلب ہے کہ فانڈری رن ٹائم env vars (جو `agent.yaml` میں سیٹ کی گئی ہوں) ہوسٹڈ تعیناتی میں `.env` اقدار سے زیادہ ترجیح رکھتی ہیں۔

---

## ورژن مطابقت

### پیکیج ورژن میٹرکس

ملٹی ایجنٹ ورک فلو مخصوص پیکیج ورژنز کا مطالبہ کرتا ہے۔ غلط ورژن رن ٹائم ایررز کا باعث بنتے ہیں۔

| پیکیج | مطلوبہ ورژن | چیک کمانڈ |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | تازہ ترین pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### عام ورژن کی غلطیاں

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# اصلاح: rc3 میں اپ گریڈ کریں
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` نہیں ملا یا انسپیکٹر غیر مطابقت پذیر:**

```powershell
# درست کریں: --pre فلیگ کے ساتھ انسٹال کریں
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# درست کریں: mcp پیکیج کو اپ گریڈ کریں
pip install mcp --upgrade
```

### تمام ورژنز ایک ساتھ چیک کریں

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

متوقع نتائج:

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

## MCP ٹول کے مسائل

### MCP ٹول کوئی نتائج واپس نہیں کرتا

**علامات:** Gap کارڈز پر "No results returned from Microsoft Learn MCP" یا "No direct Microsoft Learn results found" لکھا ہو۔

**ممکنہ وجوہات:**

1. **نیٹ ورک مسئلہ** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) پہنچنے کے قابل نہیں ہے۔
   ```powershell
   # کنیکٹوٹی کی جانچ کریں
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   اگر یہ `200` لوٹاتا ہے تو endpoint قابل رسائی ہے۔

2. **بہت مخصوص سوال** - skill کا نام Microsoft Learn کی تلاش کے لیے بہت niche ہے۔  
   - یہ بہت خاص مہارتوں کے لیے متوقع ہے۔ ٹول کے جواب میں fallback URL بھی ہوتا ہے۔

3. **MCP سیشن ٹائم آؤٹ** - Streamable HTTP کنکشن ٹائم آؤٹ ہو گیا ہے۔  
   - درخواست کو دوبارہ بھیجیں۔ MCP سیشنز عارضی ہوتے ہیں اور دوبارہ منسلک کرنے کی ضرورت ہو سکتی ہے۔

### MCP لاگز کی وضاحت

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| لاگ | مطلب | کارروائی |
|-----|---------|--------|
| `GET → 405` | MCP کلائنٹ چیکنگ انیشیئلائزیشن کے دوران | معمول - نظر انداز کریں |
| `POST → 200` | ٹول کال کامیاب | متوقع |
| `DELETE → 405` | MCP کلائنٹ کلین اپ کے دوران چیکنگ | معمول - نظر انداز کریں |
| `POST → 400` | خراب درخواست (غلط سوال) | `search_microsoft_learn_for_plan()` میں `query` پیرامیٹر چیک کریں |
| `POST → 429` | ریٹ لمٹ لگا دیا گیا | انتظار کریں اور دوبارہ کوشش کریں۔ `max_results` کم کریں |
| `POST → 500` | MCP سرور کی خرابی | وقتی - دوبارہ کوشش کریں۔ اگر مستقل رہے تو Microsoft Learn MCP API بند ہو سکتا ہے |
| کنکشن ٹائم آؤٹ | نیٹ ورک مسئلہ یا MCP سرور دستیاب نہیں | انٹرنیٹ چیک کریں۔ `curl https://learn.microsoft.com/api/mcp` آزمائیں |

---

## تعیناتی کے مسائل

### تعیناتی کے بعد کنٹینر شروع ہونے میں ناکام

1. **کنٹینر لاگز چیک کریں:**  
   - **Microsoft Foundry** سائیڈبار کھولیں → **Hosted Agents (Preview)** کو بڑھائیں → اپنے ایجنٹ پر کلک کریں → ورژن بڑھائیں → **Container Details** → **Logs**۔  
   - Python stack traces یا missing module errors تلاش کریں۔

2. **عام کنٹینر شروع نہ ہونے کی وجوہات:**

   | لاگز میں غلطی | وجہ | حل |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` میں پیکیج غائب ہے | پیکیج شامل کریں، دوبارہ تعینات کریں |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` env vars سیٹ نہیں ہیں | `agent.yaml` → `environment_variables` سیکشن اپ ڈیٹ کریں |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ترتیب نہیں دی گئی | فانڈری خود موجود کرتا ہے - اس بات کو یقینی بنائیں کہ آپ ایکسٹینشن کے ذریعے تعینات کر رہے ہیں |
   | `OSError: port 8088 already in use` | Dockerfile میں غلط پورٹ یا پورٹ کا تصادم | Dockerfile میں `EXPOSE 8088` اور `CMD ["python", "main.py"]` چیک کریں |
   | کنٹینر کوڈ 1 کے ساتھ بند ہو جاتا ہے | `main()` میں غیر ہینڈل شدہ استثناء | پہلے لوکل ٹیسٹ کریں ([Module 5](05-test-locally.md)) تاکہ غلطیوں کو تعیناتی سے پہلے پکڑا جا سکے |

3. **درست کرنے کے بعد دوبارہ تعینات کریں:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → وہی ایجنٹ منتخب کریں → نیا ورژن تعینات کریں۔

### تعیناتی بہت دیر لے رہی ہے

ملٹی ایجنٹ کنٹینرز شروع ہونے میں زیادہ وقت لیتے ہیں کیونکہ وہ اسٹارٹ اپ پر 4 ایجنٹ انسٹینسز بناتے ہیں۔ معمول کے مطابق شروع ہونے کا وقت:

| مرحلہ | متوقع دورانیہ |
|-------|------------------|
| کنٹینر امیج بلڈ | 1-3 منٹ |
| امیج کو ACR پر دھکیلنا | 30-60 سیکنڈ |
| کنٹینر شروع (سنگل ایجنٹ) | 15-30 سیکنڈ |
| کنٹینر شروع (ملٹی ایجنٹ) | 30-120 سیکنڈ |
| ایجنٹ پلیئر گراؤنڈ میں دستیاب | "Started" کے 1-2 منٹ بعد |

> اگر "Pending" کی حالت 5 منٹ سے زیادہ برقرار رہے تو کنٹینر لاگز میں ایرر چیک کریں۔

---

## RBAC اور اجازت کے مسائل

### `403 Forbidden` یا `AuthorizationFailed`

آپ کو اپنے فانڈری پروجیکٹ پر **[Azure AI User](https://aka.ms/foundry-ext-project-role)** رول کی ضرورت ہے:

1. [Azure Portal](https://portal.azure.com) پر جائیں → اپنا فانڈری **پروجیکٹ** ریسورس منتخب کریں۔  
2. **Access control (IAM)** → **Role assignments** منتخب کریں۔  
3. اپنا نام تلاش کریں → تصدیق کریں کہ **Azure AI User** درج ہو۔  
4. اگر نہیں ہے: **Add** → **Add role assignment** → **Azure AI User** تلاش کریں → اپنا اکاؤنٹ اس سے منسوب کریں۔

تفصیلات کے لیے [Microsoft Foundry کے RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) کی دستاویز دیکھیں۔

### ماڈل کی تعیناتی قابل رسائی نہیں ہے

اگر ایجنٹ ماڈل سے متعلق ایرر لوٹاتا ہے:

1. تصدیق کریں کہ ماڈل تعینات ہے: فانڈری سائیڈبار → پروجیکٹ بڑھائیں → **Models** → `gpt-4.1-mini` (یا آپ کا ماڈل) status **Succeeded** ہو۔  
2. تعیناتی کا نام ملاپ رکھتا ہو: `.env` یا `agent.yaml` میں `MODEL_DEPLOYMENT_NAME` اور سائیڈبار میں اصل تعیناتی کا نام موازنہ کریں۔  
3. اگر تعیناتی ختم ہو گئی (فری ٹئیر): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) سے دوبارہ تعینات کریں (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)۔

---

## ایجنٹ انسپیکٹر کے مسائل

### انسپیکٹر کھلتا ہے مگر "Disconnected" دکھاتا ہے

1. سرور چل رہا ہے یہ تصدیق کریں: ٹرمینل میں "Server running on http://localhost:8088" تلاش کریں۔  
2. پورٹ 5679 چیک کریں: انسپیکٹر debugpy کے ذریعے پورٹ 5679 سے جڑتا ہے۔  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. سرور دوبارہ شروع کریں اور انسپیکٹر دوبارہ کھولیں۔

### انسپیکٹر جزوی جواب دکھاتا ہے

ملٹی ایجنٹ جوابات طویل ہوتے ہیں اور اسٹریمنگ کے ذریعے تدریجاً مکمل ہوتے ہیں۔ مکمل جواب کے لیے انتظار کریں (gap کارڈز کی تعداد اور MCP ٹول کالز کے اعتبار سے 30-60 سیکنڈ لگ سکتے ہیں)۔

اگر جواب مستقل طور پر کٹتا ہے:  
- یقینی بنائیں کہ GapAnalyzer کی ہدایات میں `CRITICAL:` بلاک شامل ہے جو gap کارڈز کے ملاپ کو روکتا ہے۔  
- آپ کے ماڈل کی ٹوکن حد چیک کریں - `gpt-4.1-mini` 32K آؤٹ پٹ ٹوکن تک سپورٹ کرتا ہے، جو کافی ہونی چاہیے۔

---

## کارکردگی کے نکات

### آہستہ جوابات

ملٹی ایجنٹ ورک فلو انحصار کے تسلسل اور MCP ٹول کالز کی وجہ سے فطری طور پر سنگل ایجنٹ سے سست ہوتے ہیں۔

| اصلاح | طریقہ | اثر |
|-------------|-----|--------|
| MCP کالز کم کریں | ٹول میں `max_results` پیرامیٹر کم کریں | HTTP راؤنڈ-ٹریپس کی تعداد کم ہو گی |
| ہدایات آسان بنائیں | مختصر اور زیادہ مرکوز ایجنٹ پرامپٹس | LLM inference تیزی سے ہوگی |
| `gpt-4.1-mini` استعمال کریں | `gpt-4.1` کی نسبت ترقی کے لیے تیز | تقریباً 2 گنا تیز |
| gap کارڈ کی تفصیل کم کریں | GapAnalyzer ہدایات میں gap کارڈ کی سادگی | پیداوار کم ہوگی جو تیز رفتاری لاتی ہے |

### معمول کے جوابی اوقات (مقامی)

| ترتیب | متوقع وقت |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap کارڈز | 30-60 سیکنڈ |
| `gpt-4.1-mini`, 8+ gap کارڈز | 60-120 سیکنڈ |
| `gpt-4.1`, 3-5 gap کارڈز | 60-120 سیکنڈ |
---

## مدد حاصل کرنا

اگر آپ مندرجہ بالا اصلاحات آزمانے کے بعد پھنس گئے ہیں:

1. **سرور لاگز چیک کریں** - زیادہ تر غلطیاں ٹرمینل میں Python اسٹیک ٹریس پید ا کرتی ہیں۔ مکمل ٹریس بیک پڑھیں۔
2. **غلطی کے پیغام کی تلاش کریں** - غلطی کا متن کاپی کریں اور اسے [Microsoft Q&A برائے Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) میں تلاش کریں۔
3. **ایک مسئلہ کھولیں** - مسئلہ [ورکشاپ ریپوزیٹری](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) پر درج کریں جس میں شامل ہو:
   - غلطی کا پیغام یا اسکرین شاٹ
   - آپ کے پیکیج کے ورژن (`pip list | Select-String "agent-framework"`)
   - آپ کا Python ورژن (`python --version`)
   - مسئلہ لوکل ہے یا تعیناتی کے بعد

---

### چیک پوائنٹ

- [ ] آپ عام ترین ملٹی ایجنٹ غلطیوں کی شناخت اور اصلاح کے لیے تیز حوالہ جدول استعمال کر سکتے ہیں
- [ ] آپ جانتے ہیں کہ `.env` کنفیگریشن کے مسائل کیسے چیک اور ٹھیک کریں
- [ ] آپ تصدیق کر سکتے ہیں کہ پیکیج ورژنز مطلوبہ میٹرکس سے میل کھاتے ہیں
- [ ] آپ MCP لاگ اندراجات کو سمجھتے ہیں اور ٹول کی ناکامیوں کی تشخیص کر سکتے ہیں
- [ ] آپ تعیناتی کی ناکامیوں کے لیے کنٹینر لاگز چیک کرنا جانتے ہیں
- [ ] آپ Azure پورٹل میں RBAC رولز کی تصدیق کر سکتے ہیں

---

**پچھلا:** [07 - Verify in Playground](07-verify-in-playground.md) · **ہوم:** [Lab 02 README](../README.md) · [ورکشاپ ہوم](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**انتباہ**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کا استعمال کرتے ہوئے ترجمہ کی گئی ہے۔ اگرچہ ہم درستگی کی کوشش کرتے ہیں، براہ کرم نوٹ کریں کہ خودکار تراجم میں غلطیاں یا کمی بیشی ہو سکتی ہے۔ اصل دستاویز اپنی مادری زبان میں ہی معتبر ماخذ سمجھی جانی چاہئے۔ اہم معلومات کے لئے پیشہ ورانہ انسانی ترجمہ تجویز کیا جاتا ہے۔ ہم اس ترجمہ کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کے لیے ذمہ دار نہیں ہیں۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->