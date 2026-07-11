# الوحدة 8 - استكشاف الأخطاء وإصلاحها

تغطي هذه الوحدة الأخطاء الشائعة والإصلاحات واستراتيجيات التصحيح الخاصة بتدفق العمل متعدد الوكلاء.

## مشكلات مخرجات الوكيل

### GapAnalyzer يقول "ما زلت لا أمتلك تقرير المطابقة"

**العَرَض:** يطلب رد GapAnalyzer منك لصق تقرير مطابقة يحتوي على "المهارات المفقودة" و"فجوات الشهادة". يحدث هذا حتى عندما أرسلت كل من السيرة الذاتية ووصف الوظيفة.

**السبب:** لم يتم تمرير نص وصف الوظيفة (JD) إلى وكيل وصف الوظيفة. مع `context_mode="last_agent"`، يكون `resume_executor` هو المنفذ الوحيد الذي يرى رسالة المستخدم الأصلية. إذا لم يتضمن `RESUME_PARSER_INSTRUCTIONS` نص الوصف في مخرجاته، فلن يكون لدى وكيل وصف الوظيفة JD ليحلله، ولن يستطيع MatchingAgent حساب درجة الملاءمة، وسيتلقى GapAnalyzer مدخلاً بلا معنى.

**التشخيص:**

في سجلات الخادم، ابحث عن نطاق MatchingAgent. إذا احتوى على:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
التمرير المار مفقود أو تالف.

**الإصلاح:** تأكد من أن `RESUME_PARSER_INSTRUCTIONS` في `main.py` يحتوي على قسم `[JOB DESCRIPTION PASS-THROUGH]` والقانون:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
وتأكد أيضًا من أن `JOB_DESCRIPTION_INSTRUCTIONS` يحتوي على قاعدة تمرير `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
إذا كان أي من كتلو التعليمات عبارة عن نموذج من المعالج، استبدله بالإصدار الكامل من [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### ينبعث من MatchingAgent "لا يمكن حساب درجة الملاءمة - لم يتم تقديم الوصف الوظيفي"

هذا هو نفس السبب الجذري أعلاه. تلقى MatchingAgent مخرجات وكيل وصف الوظيفة ولكن قسم `[PARSED RESUME PASS-THROUGH]` كان مفقودًا أو فارغًا، لذلك لم يستطع مقارنة الملفين الشخصيين. تأكد من:
1. تتضمن `JOB_DESCRIPTION_INSTRUCTIONS` قاعدة الإرسال: `نسخ [PARSED RESUME] حرفيًا - يعتمد عليه Matching Agent في الخطوات اللاحقة.`
2. تخبر `MATCHING_AGENT_INSTRUCTIONS` الوكيل بالبحث عن أقسام `[JD REQUIREMENTS]` و `[PARSED RESUME PASS-THROUGH]`.

استبدل كلا كتلو التعليمات بالإصدارات الكاملة من [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### يظهر الرد مرتين

**العَرَض:** يظهر ناتج GapAnalyzer (أو مخرجات خط الأنابيب بالكامل) مرتين في رد مفتش الوكيل.

**السبب:** يستخدم `WorkflowBuilder` منطق OR للحواف الواردة - يتم تشغيل منفذ في الخط الأسفل بمجرد إكمال **أي** من السلفين. إذا كان لـ `matching_executor` حافتان واردتان (واحدة من `resume_executor` وواحدة من `jd_executor`)، فإنه يتم تشغيله مرتين: مرة عند انتهاء ResumeParser ومرة أخرى عند انتهاء وكيل JD. ثم يعمل GapAnalyzer أيضًا مرتين.

**الإصلاح:** تأكد من أن مخطط `WorkflowBuilder` هو خط أنابيب متسلسل صارم بدون دمج مدخلات (fan-in):

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # ليس من resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

إذا كان لديك سطر `.add_edge(resume_executor, matching_executor)` عالق، قم بحذفه. تسمح قاعدة التمرير `[PARSED RESUME PASS-THROUGH]` في مخرجات وكيل JD لوكيل المطابقة بالوصول إلى السيرة الذاتية بالفعل.

---

## مشكلات البيئة والتكوين

### قيم `.env` مفقودة أو خاطئة

يجب أن يكون ملف `.env` في دليل `PersonalCareerCopilot/` (بنفس مستوى `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

محتوى `.env` المتوقع:

**المسار أ - Foundry السحابي:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**المسار ب - Foundry المحلي:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> كلا المسارين يستخدمان `FOUNDRY_PROJECT_ENDPOINT`. تختلف القيمة: السحابة تستخدم نقطة نهاية Foundry عبر `https://`؛ المحلي يستخدم `http://localhost:5273/v1`. نفذ `foundry model list` لتأكيد الاسم المستعار الدقيق للنموذج للمسار ب.

> **طريقة العثور على `FOUNDRY_PROJECT_ENDPOINT`:** 
- افتح شريط أدوات **Foundry Toolkit** الجانبي في VS Code → انقر بزر الماوس الأيمن على مشروعك → **نسخ نقطة نهاية المشروع**. 
- أو انتقل إلى [بوابة Azure](https://portal.azure.com) → مشروع Foundry الخاص بك → **نظرة عامة** → **نقطة نهاية المشروع**.

> **طريقة العثور على `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** في شريط أدوات Foundry Toolkit الجانبي، وسع مشروعك → **النماذج** → ابحث عن اسم النموذج المنشور (مثل `gpt-4.1-mini`).

### أولوية متغيرات البيئة

يستخدم `main.py` `load_dotenv(override=True)`، مما يعني:

| الأولوية | المصدر | يفوز إذا تم تعيين كلاهما؟ |
|----------|--------|--------------------|
| 1 (الأعلى) | ملف `.env` | نعم |
| 2 | متغير بيئة الصدفة / الحاوية | يُستخدم عندما لا يكون نفس المفتاح موجودًا في `.env` |

في التطوير المحلي، يجعل هذا `.env` مصدر الحقيقة (تحرير `.env` يؤثر على التشغيل فورًا). في النشر المستضاف، يقوم Foundry بحقن متغيرات البيئة على مستوى الحاوية؛ نظرًا لأن `.env` ليس جزءًا من الصورة المنشورة لإعداد المعمل هذا، تُستخدم القيم المحقونة في الحاوية.

---

## توافق الإصدارات

### مصفوفة إصدارات الحزم

يتطلب تدفق العمل متعدد الوكلاء إصدارات محددة من الحزم. تؤدي الإصدارات غير المطابقة لأخطاء وقت التشغيل.

| الحزمة | الإصدار المطلوب | أمر الفحص |
|---------|-----------------|------------|
| `agent-framework-foundry` | الأحدث | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | الأحدث | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | الأحدث | `pip show debugpy` |
| بايثون | 3.12+ | `python --version` |

### أخطاء الإصدارات الشائعة

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# إصلاح: أعد تثبيت agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# إصلاح: ترقية حزمة mcp
pip install mcp --upgrade
```

### تحقق من كل الإصدارات دفعة واحدة

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

المخرجات المتوقعة:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## مشكلات النشر

### فشل الحاوية في البدء بعد النشر

1. **تحقق من سجلات الحاوية:**
   - افتح شريط أدوات **Foundry Toolkit** → وسع **الوكلاء المستضافين (معاينة)** → انقر على وكيلك → وسع الإصدار → **تفاصيل الحاوية** → **السجلات**.
   - ابحث عن تتبعات أخطاء بايثون أو أخطاء وحدات مفقودة.

2. **أخطاء بدء تشغيل الحاوية الشائعة:**

   | خطأ في السجلات | السبب | الإصلاح |
   |-----------------|-------|--------|
   | `ModuleNotFoundError` | حزمة مفقودة في `requirements.txt` | أضف الحزمة وأعد النشر |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | متغيرات البيئة في `agent.yaml` أو `.env` غير مضبوطة | حدِّث قسم `environment_variables` في `agent.yaml` (مستضاف) أو `.env` (محلي) |
   | `azure.identity.CredentialUnavailableError` | الهوية المُدارة غير مُكوَّنة | يقوم Foundry بضبطها تلقائيًا - تأكد من نشرك عبر الامتداد |
   | `OSError: port 8088 already in use` | Dockerfile يفتح منفذ خاطئ أو تعارض في المنفذ | تحقق من `EXPOSE 8088` في Dockerfile و `CMD ["python", "main.py"]` |
   | تنهي الحاوية برمز 1 | استثناء غير معالج في `main()` | اختبر محليًا أولاً ([الوحدة 5](05-test-locally.md)) لالتقاط الأخطاء قبل النشر |

3. **أعد النشر بعد الإصلاح:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → اختر نفس الوكيل → انشر إصدارًا جديدًا.

### تستغرق عملية النشر وقتًا طويلاً

تستغرق حاويات الوكلاء المتعددين وقتًا أطول للبدء لأنها تنشئ 4 مثيلات للوكلاء عند التشغيل. أوقات البدء المعتادة:

| المرحلة | المدة المتوقعة |
|-------|---------------|
| بناء صورة الحاوية | 1-3 دقائق |
| دفع الصورة إلى ACR | 30-60 ثانية |
| بدء الحاوية (وكيل واحد) | 15-30 ثانية |
| بدء الحاوية (وكلاء متعددون) | 30-120 ثانية |
| الوكيل متاح في Playground | 1-2 دقيقة بعد "تم البدء" |

> إذا استمر وضع "قيد الانتظار" لأكثر من 5 دقائق، تحقق من سجلات الحاوية بحثًا عن الأخطاء.

---

## مشكلات RBAC والأذونات

### `403 ممنوع` أو `AuthorizationFailed`

تحتاج إلى دور **[مستخدم Foundry](https://aka.ms/foundry-ext-project-role)** على مشروع Foundry الخاص بك (كان يُسمى سابقًا **مستخدم Azure AI** - ورمز الدور لم يتغير):

1. اذهب إلى [بوابة Azure](https://portal.azure.com) → مورد مشروع Foundry الخاص بك.
2. انقر على **التحكم بالوصول (IAM)** → **تعيينات الدور**.
3. ابحث عن اسمك → تأكد من وجود **مستخدم Foundry** (أو التسمية القديمة **مستخدم Azure AI**).
4. إذا كان مفقودًا: **إضافة** → **إضافة تعيين دور** → ابحث عن **مستخدم Foundry** → عين الدور لحسابك.

راجع توثيق [RBAC لـ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) للتفاصيل.

### عدم إمكانية الوصول إلى نشر النموذج

إذا أعاد الوكيل أخطاء متعلقة بالنموذج:

1. تحقق من نشر النموذج: شريط Foundry الجانبي → وسع المشروع → **النماذج** → تحقق من وجود `gpt-4.1-mini` (أو نموذجك) مع الحالة **تم بنجاح**.
2. تحقق من تطابق اسم النشر: قارن `AZURE_AI_MODEL_DEPLOYMENT_NAME` في `.env` (أو `agent.yaml`) مع اسم النشر الفعلي في الشريط الجانبي.
3. إذا انتهت صلاحية النشر (الطبقة المجانية): أعد النشر من [كتالوج النماذج](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## مشكلات Foundry Local (المسار ب)

### خدمة Foundry Local غير تعمل

```powershell
# تحقق من الحالة
foundry local status

# ابدأ الخدمة إذا كانت متوقفة
foundry local start
```

| العَرَض | السبب | الإصلاح |
|---------|-------|--------|
| تحقق الصحة يعيد `503` | الخدمة لم تبدأ | نفذ `foundry local start` أو اضغط **ابدأ** في شريط أدوات Foundry Toolkit الجانبي |
| تحقق الصحة تنتهي المهلة | النموذج لا يزال يُحمّل | انتظر 30–60 ثانية بعد البدء؛ النماذج الأكبر تستغرق وقتًا أطول |
| `StatusCode: 404` على `/v1/health` | المنفذ خاطئ | الافتراضي هو `5273`. تحقق من `foundry local status` للمنفذ الفعلي |
| موارد غير كافية | يحتاج Foundry Local لـ ~4 جيجابايت رام متاحة | أغلق التطبيقات الأخرى |
| فشل تحميل النموذج | مساحة القرص منخفضة | النماذج بحجم 2-8 جيجابايت. حرر مساحة، ثم نفذ `foundry model pull <name>` |

### عدم تطابق اسم النموذج

```powershell
# قائمة النماذج المحملة وأسماؤها المستعارة الدقيقة
foundry model list
```

عيّن `AZURE_AI_MODEL_DEPLOYMENT_NAME` في `.env` إلى الاسم المستعار الدقيق المعروض (مثلًا `phi-4-mini` وليس `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` عند التشغيل محليًا (المسار ب)

يستخدم `main.py` في المعمل `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. يتطلب Foundry Local أن يشير هذا المتغير إلى الخدمة المحلية - **ليس** `AZURE_AI_PROJECT_ENDPOINT`. تأكد من أن `.env` يحتوي على:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### أداة MCP لا تزال تصدر طلبًا خارجيًا (المسار ب)

هذا متوقع. تستخرج أداة `search_microsoft_learn_for_plan` موارد التعلم من `https://learn.microsoft.com/api/mcp`. **يتم إرسال استعلام اسم المهارة فقط** عبر الشبكة - تتم معالجة السيرة الذاتية ونص الوصف الوظيفي بالكامل على جهازك ولا تُرسَل أبدًا. إذا كان التشغيل دون اتصال كلي مطلوبًا، أضف تعبير `try/except` في الأداة يعيد عنوان URL ثابت لـ `learn.microsoft.com` عند تعذر الوصول إلى نقطة النهاية.

---

## طلب المساعدة

إذا علقت بعد تجربة الإصلاحات أعلاه:

1. **تحقق من سجلات الخادم** - معظم الأخطاء تنتج تتبع سترق بايثون في الطرفية. اقرأ التتبع بالكامل.
2. **ابحث عن رسالة الخطأ** - انسخ نص الخطأ وابحث في [Microsoft Q&A لخدمات Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **افتح تقرير مشكلة** - قدّم قضية في [مستودع ورشة العمل](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) مع:
   - رسالة الخطأ أو لقطة شاشة
   - إصدارات الحزم لديك (`pip list | Select-String "agent-framework"`)
   - إصدار بايثون لديك (`python --version`)
   - ما إذا كانت المشكلة محلية أو بعد النشر

---

### نقطة التحقق

- [ ] تعرف كيفية التحقق من مشكلات تكوين `.env` وإصلاحها
- [ ] يمكنك التحقق من تطابق إصدارات الحزم مع المصفوفة المطلوبة
- [ ] تعرف كيفية التحقق من سجلات الحاوية لرسائل فشل النشر
- [ ] تستطيع التحقق من أدوار RBAC في بوابة Azure

---

**السابق:** [07 - التحقق في Playground](07-verify-in-playground.md) · **التالي:** [09 - الملخص →](09-summary.md) · **الرئيسية:** [README معمل 02](../README.md) · [الصفحة الرئيسية لورشة العمل](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**تنويه**:
تمت ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والمعتمد. للمعلومات الهامة، يُنصح بالاستعانة بترجمة بشرية محترفة. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->