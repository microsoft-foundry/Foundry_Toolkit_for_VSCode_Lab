# الوحدة 8 - استكشاف الأخطاء وإصلاحها (متعدد الوكلاء)

تغطي هذه الوحدة الأخطاء الشائعة والإصلاحات واستراتيجيات التصحيح الخاصة بسير العمل متعدد الوكلاء. لمشكلات نشر Foundry العامة، راجع أيضًا [دليل استكشاف الأخطاء في المختبر 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## مرجع سريع: خطأ → إصلاح

| الخطأ / العرض | السبب المحتمل | الإصلاح |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | ملف `.env` مفقود أو القيم غير معينة | أنشئ `.env` بـ `PROJECT_ENDPOINT=<your-endpoint>` و `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | البيئة الافتراضية غير مفعلة أو تبعيات غير مثبتة | شغّل `.\.venv\Scripts\Activate.ps1` ثم `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | حزمة MCP غير مثبتة (مفقودة من المتطلبات) | شغّل `pip install mcp` أو تحقق من وجودها في `requirements.txt` كاعتماد انتقالي |
| يبدأ الوكيل لكنه يُرجع استجابة فارغة | عدم تطابق `output_executors` أو حواف مفقودة | تحقق من `output_executors=[gap_analyzer]` وأن جميع الحواف موجودة في `create_workflow()` |
| بطاقة فجوة واحدة فقط (الباقي مفقود) | تعليمات GapAnalyzer غير كاملة | أضف الفقرة `CRITICAL:` إلى `GAP_ANALYZER_INSTRUCTIONS` - راجع [الوحدة 3](03-configure-agents.md) |
| درجة الملاءمة 0 أو مفقودة | MatchingAgent لم يتلق بيانات من الأعلى | تحقق من وجود كل من `add_edge(resume_parser, matching_agent)` و `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | رفض خادم MCP استدعاء الأداة | تحقق من الاتصال بالإنترنت. حاول فتح `https://learn.microsoft.com/api/mcp` في المتصفح. أعد المحاولة |
| لا توجد عناوين URL لـ Microsoft Learn في المخرجات | أداة MCP غير مسجلة أو نقطة النهاية خاطئة | تحقق من `tools=[search_microsoft_learn_for_plan]` على GapAnalyzer و`MICROSOFT_LEARN_MCP_ENDPOINT` صحيح |
| `Address already in use: port 8088` | عملية أخرى تستخدم المنفذ 8088 | شغّل `netstat -ano \| findstr :8088` (ويندوز) أو `lsof -i :8088` (ماك/لينكس) وأوقف العملية المتضاربة |
| `Address already in use: port 5679` | تعارض منفذ debugpy | أوقف جلسات التصحيح الأخرى. شغّل `netstat -ano \| findstr :5679` للعثور على العملية وإنهائها |
| لا يفتح Agent Inspector | الخادم لم يبدأ بالكامل أو تعارض في المنفذ | انتظر لسجل "Server running". تحقق من أن المنفذ 5679 متاح |
| `azure.identity.CredentialUnavailableError` | لم تقم بتسجيل الدخول إلى Azure CLI | شغّل `az login` ثم أعد تشغيل الخادم |
| `azure.core.exceptions.ResourceNotFoundError` | نشر النموذج غير موجود | تحقق من أن `MODEL_DEPLOYMENT_NAME` يطابق نموذج نشر في مشروع Foundry |
| حالة الحاوية "فشلت" بعد النشر | تعطل الحاوية عند بدء التشغيل | تحقق من سجلات الحاوية في الشريط الجانبي لـ Foundry. شائع: متغير بيئي مفقود أو خطأ في الاستيراد |
| النشر يظهر "قيد الانتظار" لأكثر من 5 دقائق | الحاوية تستغرق وقت طويل للبدء أو حدود الموارد | انتظر حتى 5 دقائق للوكيل المتعدد (ينشئ 4 مثيلات). إذا استمر الانتظار، تحقق من السجلات |
| `ValueError` من `WorkflowBuilder` | تكوين الرسم البياني غير صالح | تأكد من تعيين `start_executor` وأن `output_executors` قائمة، ولا توجد حواف دائرية |

---

## مشكلات البيئة والتكوين

### قيم `.env` مفقودة أو خاطئة

يجب أن يكون ملف `.env` في دليل `PersonalCareerCopilot/` (نفس مستوى `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

محتوى `.env` المتوقع:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **كيفية العثور على PROJECT_ENDPOINT:**  
- افتح الشريط الجانبي لـ **Microsoft Foundry** في VS Code → انقر بزر الماوس الأيمن على مشروعك → **Copy Project Endpoint**.  
- أو اذهب إلى [بوابة Azure](https://portal.azure.com) → مشروع Foundry الخاص بك → **Overview** → **Project endpoint**.

> **كيفية العثور على MODEL_DEPLOYMENT_NAME:** في الشريط الجانبي لـ Foundry، وسع مشروعك → **Models** → ابحث عن اسم النموذج المنشور (مثل `gpt-4.1-mini`).

### أسبقية متغيرات البيئة

يستخدم `main.py` `load_dotenv(override=False)`، مما يعني:

| الأولوية | المصدر | يفوز عندما يكون كلاهما مضبوطًا؟ |
|----------|--------|------------------------|
| 1 (الأعلى) | متغير بيئة الصدفة | نعم |
| 2 | ملف `.env` | فقط إذا لم يتم تعيين متغير الصدفة |

هذا يعني أن متغيرات بيئة وقت التشغيل في Foundry (المضبوطة عبر `agent.yaml`) تتفوق على قيم `.env` أثناء النشر المستضاف.

---

## توافق الإصدارات

### مصفوفة إصدارات الحزم

يتطلب سير عمل الوكيل المتعدد إصدارات محددة من الحزم. يؤدّي عدم تطابق الإصدارات إلى أخطاء وقت التشغيل.

| الحزمة | الإصدار المطلوب | أمر التحقق |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | أحدث إصدار ما قبل الإصدار | `pip show agent-dev-cli` |
| بايثون | 3.10+ | `python --version` |

### أخطاء الإصدارات الشائعة

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# إصلاح: الترقية إلى rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` غير موجود أو Inspector غير متوافق:**

```powershell
# إصلاح: التثبيت مع العلم --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# إصلاح: ترقية حزمة mcp
pip install mcp --upgrade
```

### تحقق من كل الإصدارات مرة واحدة

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

المخرجات المتوقعة:

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

## مشكلات أداة MCP

### أداة MCP لا تُرجع نتائج

**العرض:** بطاقات الفجوة تقول "No results returned from Microsoft Learn MCP" أو "No direct Microsoft Learn results found".

**الأسباب المحتملة:**

1. **مشكلة شبكة** - نقطة النهاية MCP (`https://learn.microsoft.com/api/mcp`) غير متاحة.
   ```powershell
   # اختبار الاتصال
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   إذا أعاد هذا `200`، فإن نقطة النهاية متاحة.

2. **استعلام محدد جدًا** - اسم المهارة متخصص جدًا لبحث Microsoft Learn.
   - هذا متوقع للمهارات المتخصصة جداً. الأداة لديها URL بديل في الاستجابة.

3. **انتهاء جلسة MCP** - اتصال Streamable HTTP انتهى وقته.
   - أعد محاولة الطلب. جلسات MCP مؤقتة وقد تحتاج إلى إعادة الاتصال.

### شرح سجلات MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| السجل | المعنى | الإجراء |
|-----|---------|--------|
| `GET → 405` | فحص عميل MCP أثناء التهيئة | طبيعي - تجاهل |
| `POST → 200` | نجح استدعاء الأداة | متوقع |
| `DELETE → 405` | فحص عميل MCP أثناء التنظيف | طبيعي - تجاهل |
| `POST → 400` | طلب سيء (استعلام غير صالح) | تحقق من المعامل `query` في `search_microsoft_learn_for_plan()` |
| `POST → 429` | تجاوز معدل الدعوات | انتظر وأعد المحاولة. قلل من معلمة `max_results` |
| `POST → 500` | خطأ خادم MCP | مؤقت - أعد المحاولة. إذا استمر، قد يكون API MCP الخاص بـ Microsoft Learn معطلًا |
| انتهاء مهلة الاتصال | مشكلة شبكة أو خادم MCP غير متوفر | تحقق من الإنترنت. جرب `curl https://learn.microsoft.com/api/mcp` |

---

## مشكلات النشر

### فشل الحاوية في البدء بعد النشر

1. **تحقق من سجلات الحاوية:**
   - افتح الشريط الجانبي لـ **Microsoft Foundry** → وسّع **Hosted Agents (Preview)** → انقر على وكيلك → وسع الإصدار → **تفاصيل الحاوية** → **السجلات**.
   - ابحث عن تتبعات بايثون أو أخطاء وحدة مفقودة.

2. **فشلات شائعة عند بدء الحاوية:**

   | الخطأ في السجلات | السبب | الإصلاح |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` تفتقد حزمة | أضف الحزمة، أعد النشر |
   | `RuntimeError: Missing required environment variable` | متغيرات env في `agent.yaml` غير مضبوطة | حدّث قسم `environment_variables` في `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | الهوية المدارة غير مُهيأة | Foundry يعينها تلقائيًا - تأكد من النشر عبر الإضافة |
   | `OSError: port 8088 already in use` | Dockerfile يفتح منفذ خاطئ أو تعارض في المنفذ | تحقق من `EXPOSE 8088` في Dockerfile و`CMD ["python", "main.py"]` |
   | الحاوية تخرج برمز 1 | استثناء غير معالج في `main()` | اختبر محليًا أولاً ([الوحدة 5](05-test-locally.md)) لالتقاط الأخطاء قبل النشر |

3. **أعد النشر بعد الإصلاح:**
   - اضغط `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → اختر نفس الوكيل → انشر إصدارًا جديدًا.

### استغراق النشر وقتًا طويلاً

حاويات الوكيل المتعدد تستغرق وقتًا أطول للبدء لأنها تنشئ 4 مثيلات وكيل عند بدء التشغيل. أوقات البدء العادية:

| المرحلة | المدة المتوقعة |
|-------|------------------|
| بناء صورة الحاوية | 1-3 دقائق |
| دفع الصورة إلى ACR | 30-60 ثانية |
| بدء الحاوية (وكيل فردي) | 15-30 ثانية |
| بدء الحاوية (متعدد الوكلاء) | 30-120 ثانية |
| توفر الوكيل في Playground | 1-2 دقائق بعد "Started" |

> إذا استمر الوضع "قيد الانتظار" لأكثر من 5 دقائق، تحقق من سجلات الحاوية للأخطاء.

---

## مشكلات RBAC والأذونات

### `403 Forbidden` أو `AuthorizationFailed`

تحتاج إلى دور **[Azure AI User](https://aka.ms/foundry-ext-project-role)** على مشروع Foundry الخاص بك:

1. اذهب إلى [بوابة Azure](https://portal.azure.com) → مورد مشروع Foundry الخاص بك.  
2. انقر على **Access control (IAM)** → **Role assignments**.  
3. ابحث عن اسمك → تأكد من إدراج **Azure AI User**.  
4. إذا كان مفقودًا: **إضافة** → **إضافة تعيين دور** → ابحث عن **Azure AI User** → عيّنه لحسابك.

راجع وثائق [RBAC لـ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) لمزيد من التفاصيل.

### نشر النموذج غير متاح

إذا أعاد الوكيل أخطاء متعلقة بالنموذج:

1. تحقق من نشر النموذج: الشريط الجانبي لـ Foundry → وسّع المشروع → **Models** → تحقق من وجود `gpt-4.1-mini` (أو نموذك) بحالة **Succeeded**.  
2. تحقق من تطابق اسم النشر: قارن `MODEL_DEPLOYMENT_NAME` في `.env` (أو `agent.yaml`) مع اسم النشر الفعلي في الشريط الجانبي.  
3. إذا انتهت صلاحية النشر (الطبقة المجانية): أعد النشر من [فهرس النماذج](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## مشكلات Agent Inspector

### يفتح Inspector لكنه يظهر "Disconnected"

1. تحقق من تشغيل الخادم: تحقق من وجود "Server running on http://localhost:8088" في الطرفية.  
2. تحقق من المنفذ `5679`: يتصل Inspector عبر debugpy على المنفذ 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. أعد تشغيل الخادم وأعد فتح Inspector.

### يعرض Inspector استجابة جزئية

استجابات الوكلاء المتعددين طويلة وتُرسل بشكل متدفق تدريجيًا. انتظر حتى تكتمل الاستجابة بالكامل (قد تستغرق 30-60 ثانية حسب عدد بطاقات الفجوة واستدعاءات أداة MCP).

إذا كانت الاستجابة مقطوعة دائمًا:  
- تحقق من تعليمات GapAnalyzer التي تحتوي على كتلة `CRITICAL:` التي تمنع دمج بطاقات الفجوة.  
- تحقق من حد الرموز لنموذجك - حيث يدعم `gpt-4.1-mini` حتى 32 ألف رمز ناتج، وهذا يجب أن يكون كافيًا.

---

## نصائح الأداء

### الاستجابات البطيئة

سير عمل الوكلاء المتعددين أبطأ بطبيعته من الوكيل الفردي بسبب التبعيات المتسلسلة واستدعاءات أداة MCP.

| التحسين | كيف | التأثير |
|-------------|-----|--------|
| قلل استدعاءات MCP | خفّض معلمة `max_results` في الأداة | يقلل جولات HTTP |
| بسّط التعليمات | موجهات وكيل أقصر وأكثر تركيزًا | تسريع استنتاج LLM |
| استخدم `gpt-4.1-mini` | أسرع من `gpt-4.1` للتطوير | تحسن السرعة ~2x |
| قلل تفاصيل بطاقة الفجوة | بسّط تنسيق بطاقة الفجوة في تعليمات GapAnalyzer | إنتاج أقل مخرجات |

### أوقات الاستجابة النموذجية (محلياً)

| التكوين | الوقت المتوقع |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 بطاقات فجوة | 30-60 ثانية |
| `gpt-4.1-mini`, 8+ بطاقات فجوة | 60-120 ثانية |
| `gpt-4.1`, 3-5 بطاقات فجوة | 60-120 ثانية |
---

## الحصول على المساعدة

إذا كنت عالقًا بعد محاولة الإصلاحات أعلاه:

1. **تحقق من سجلات الخادم** - معظم الأخطاء تنتج أثر تتبع مكدس Python في الطرفية. اقرأ أثر التتبع الكامل.
2. **ابحث عن رسالة الخطأ** - انسخ نص الخطأ وابحث عنه في [الأسئلة والأجوبة من Microsoft لـ Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **افتح قضية** - قدم قضية في [مستودع الورشة](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) مرفقًا:
   - رسالة الخطأ أو لقطة الشاشة
   - إصدارات الحزم الخاصة بك (`pip list | Select-String "agent-framework"`)
   - إصدار Python الخاص بك (`python --version`)
   - ما إذا كانت المشكلة محلية أو بعد النشر

---

### قائمة التحقق

- [ ] يمكنك تحديد وإصلاح أكثر أخطاء الوكلاء المتعددين شيوعًا باستخدام جدول المراجعة السريعة
- [ ] تعرف كيفية التحقق من مشكلات تكوين `.env` وإصلاحها
- [ ] يمكنك التحقق من تطابق إصدارات الحزم مع المصفوفة المطلوبة
- [ ] تفهم إدخالات سجلات MCP ويمكنك تشخيص فشل الأدوات
- [ ] تعرف كيفية التحقق من سجلات الحاويات لأخطاء النشر
- [ ] يمكنك التحقق من أدوار RBAC في بوابة Azure

---

**السابق:** [07 - التحقق في الملعب](07-verify-in-playground.md) · **الرئيسية:** [قراءة الملف 02 المختبر](../README.md) · [الرئيسية الورشة](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**إخلاء المسؤولية**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات التلقائية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر المعترف به والموثوق. للمعلومات الحيوية، يُنصح باستخدام ترجمة مهنية بشرية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->