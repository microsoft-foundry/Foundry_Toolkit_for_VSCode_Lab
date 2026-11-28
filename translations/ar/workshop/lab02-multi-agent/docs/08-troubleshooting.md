# الوحدة 8 - استكشاف الأخطاء وإصلاحها

تغطي هذه الوحدة الأخطاء الشائعة، والإصلاحات، واستراتيجيات تصحيح الأخطاء الخاصة بسير العمل متعدد الوكلاء.

## مشكلات مخرجات الوكيل

### GapAnalyzer يقول "لا يزال ليس لدي تقرير مطابق"

**العَرَض:** رد GapAnalyzer يطلب منك لصق تقرير مطابق يحتوي على "المهارات المفقودة" و"فجوات الشهادة". يحدث هذا حتى عندما أرسلت كلًا من السيرة الذاتية ووصف الوظيفة.

**السبب:** لم يتم تمرير نص JD لأسفل إلى وكيل JD. مع `context_mode="last_agent"`، `resume_executor` هو المنفذ الوحيد الذي يرى رسالة المستخدم الأصلية. إذا لم يتضمن `RESUME_PARSER_INSTRUCTIONS` نص JD في مخرجاته، فلن يمتلك وكيل JD أي JD لتحليله، ولن يتمكن MatchingAgent من حساب درجة التطابق، ويستلم GapAnalyzer مدخلاً بلا معنى.

**التشخيص:**

في سجلات الخادم، ابحث عن نطاق MatchingAgent. إذا احتوى على:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
التمرير مفقود أو معطل.

**الإصلاح:** تأكد من أن `RESUME_PARSER_INSTRUCTIONS` في `main.py` يحتوي على قسم `[JOB DESCRIPTION PASS-THROUGH]` والقانون:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
وتأكد أيضًا أن `JOB_DESCRIPTION_INSTRUCTIONS` يحتوي على قاعدة تمرير `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
إذا كان أي من كتلي التعليمات عبارة عن نموذج من معالج الهيكل، استبدله بالإصدار الكامل من [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### تصدر MatchingAgent "لا يمكن حساب درجة التطابق - لم يتم توفير JD"

هذا هو نفس السبب الجذري أعلاه. استلم MatchingAgent مخرجات وكيل JD لكن قسم `[PARSED RESUME PASS-THROUGH]` كان مفقودًا أو فارغًا، لذا لم يستطع مقارنة الملفين الشخصيين. تأكد من:
1. يتضمن `JOB_DESCRIPTION_INSTRUCTIONS` قاعدة التمرير: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` يخبر الوكيل بالبحث عن قسمي `[JD REQUIREMENTS]` و`[PARSED RESUME PASS-THROUGH]`.

استبدل كلا كتلي التعليمات بالإصدارات الكاملة من [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### يظهر الرد مرتين

**العَرَض:** يظهر مخرج GapAnalyzer (أو مخرج خط الأنابيب الكامل) مرتين في رد Agent Inspector.

**السبب:** يستخدم `WorkflowBuilder` منطق OR للروابط الواردة - يتم تشغيل منفذ أسفل الخط بمجرد إكمال **أي** من السابقين. إذا كان `matching_executor` لديه رابطان واردان (واحد من `resume_executor` وآخر من `jd_executor`)، فسيتم تشغيله مرتين: مرة عند اكتمال ResumeParser ومرة أخرى عند اكتمال وكيل JD. ثم يتم تشغيل GapAnalyzer مرتين أيضًا.

**الإصلاح:** تأكد من أن رسم `WorkflowBuilder` هو خط أنابيب تسلسلي صارم بدون دمج في نقطة واحدة:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

إذا كان لديك سطر `.add_edge(resume_executor, matching_executor)` زائد، فقم بإزالته. تمرير `[PARSED RESUME PASS-THROUGH]` في مخرجات وكيل JD يمنح بالفعل الوصول لـ MatchingAgent إلى السيرة الذاتية.

---

## مشكلات البيئة والتكوين

### قيم `.env` مفقودة أو خاطئة

يجب أن يكون ملف `.env` في دليل `PersonalCareerCopilot/` (على نفس المستوى مع `main.py`):

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

> كلا المسارين يستخدمان `FOUNDRY_PROJECT_ENDPOINT`. تختلف القيمة: يستخدم السحابة نقطة نهاية Foundry `https://`؛ يستخدم المحلي `http://localhost:5273/v1`. شغّل `foundry model list` لتأكيد الاسم المستعار الدقيق للنموذج للمسار ب.

> **كيفية العثور على `FOUNDRY_PROJECT_ENDPOINT` الخاص بك:** 
- افتح الشريط الجانبي **Foundry Toolkit** في VS Code → انقر بزر الماوس الأيمن على مشروعك → **نسخ نقطة نهاية المشروع**. 
- أو اذهب إلى [Azure Portal](https://portal.azure.com) → مشروع Foundry الخاص بك → **نظرة عامة** → **نقطة نهاية المشروع**.

> **كيفية العثور على `AZURE_AI_MODEL_DEPLOYMENT_NAME` الخاص بك:** في الشريط الجانبي Foundry Toolkit، وسع مشروعك → **النماذج** → ابحث عن اسم النموذج المنشور الخاص بك (مثل `gpt-4.1-mini`).

### أولوية متغيرات البيئة

يستخدم `main.py` `load_dotenv(override=True)`، والذي يعني:

| الأولوية | المصدر | ينتصر عندما يتم تعيين كلاهما؟ |
|----------|--------|------------------------|
| 1 (الأعلى) | ملف `.env` | نعم |
| 2 | متغير بيئة القشرة / الحاوية | يستخدم عندما لا يكون المفتاح نفسه موجودًا في `.env` |

في التطوير المحلي، يجعل هذا من `.env` المصدر الحقيقي (تعديل `.env` يؤثر على الجلسات فورًا). في النشر المستضاف، يقوم Foundry بحقن متغيرات البيئة على مستوى الحاوية؛ نظرًا لأن `.env` ليس جزءًا من الصورة المنشورة لإعداد المختبر هذا، تُستخدم قيم الحاوية المحقونة.

---

## التوافق مع النسخة

### مصفوفة إصدارات الحزمة

يتطلب سير عمل الوكلاء المتعددين إصدارات محددة من الحزم. تؤدي الإصدارات غير المتطابقة إلى أخطاء وقت التشغيل.

| الحزمة | النسخة المطلوبة | أمر التحقق |
|---------|-----------------|---------------|
| `agent-framework-foundry` | الأحدث | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | الأحدث | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | الأحدث | `pip show debugpy` |
| بايثون | 3.12+ | `python --version` |

### أخطاء الإصدارات الشائعة

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### تحقق من جميع الإصدارات دفعة واحدة

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
   - افتح الشريط الجانبي **Foundry Toolkit** → ضمن مشروعك، انقر **Agents** → تبويب **Hosted Agent** → انقر على وكيلك. تحقق من **الحالة** في تبويب **التفاصيل**، ثم افتح تبويب **Playground** واستخدم تبويب **Logs** في لوحة **تفاصيل الجلسة** لرؤية مخرجات الحاوية.
   - ابحث عن تتبع مكدس بايثون أو أخطاء مفقودة في الوحدة.

2. **أعطال بدء الحاوية الشائعة:**

   | الخطأ في السجلات | السبب | الإصلاح |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` مفقودة حزمة | أضف الحزمة، وأعد النشر |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | لم يتم تعيين متغيرات بيئة `agent.yaml` أو `.env` | حدّث قسم `agent.yaml` → `environment_variables` (مستضاف) أو `.env` (محلي) |
   | `azure.identity.CredentialUnavailableError` | لم يتم تكوين الهوية المُدارة | يقوم Foundry بضبط هذا تلقائيًا - تأكد من أنك تنشر عبر الامتداد |
   | `OSError: port 8088 already in use` | يعرف Dockerfile المنفذ الخطأ أو تعارض منفذ | تحقق من `EXPOSE 8088` في Dockerfile و`CMD ["python", "main.py"]` |
   | الحاوية تخرج برمز 1 | استثناء غير معالج في `main()` | اختبر محليًا أولًا ([الوحدة 5](05-test-locally.md)) لالتقاط الأخطاء قبل النشر |

3. **أعد النشر بعد الإصلاح:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → اختر نفس الوكيل → انشر نسخة جديدة.

### يستغرق النشر وقتًا طويلاً جدًا

تستغرق حاويات الوكلاء المتعددين وقتًا أطول للبدء لأنها تنشئ 4 حالات وكيل عند بدء التشغيل. أوقات بدء التشغيل الطبيعية:

| المرحلة | المدة المتوقعة |
|-------|------------------|
| بناء صورة الحاوية | 1-3 دقائق |
| دفع الصورة إلى ACR | 30-60 ثانية |
| بدء الحاوية (وكيل واحد) | 15-30 ثانية |
| بدء الحاوية (متعدد الوكلاء) | 30-120 ثانية |
| الوكيل متاح في Playground | 1-2 دقائق بعد "بدأ" |

> إذا استمرت الحالة "قيد الانتظار" لأكثر من 5 دقائق، تحقق من سجلات الحاوية للأخطاء.

---

## مشكلات RBAC والأذونات

### `403 Forbidden` أو `AuthorizationFailed`

تحتاج إلى دور **[Foundry User](https://aka.ms/foundry-ext-project-role)** في مشروع Foundry الخاص بك (الذي كان يُسمى سابقًا **Azure AI User** - معرف الدور لم يتغير):

1. اذهب إلى [Azure Portal](https://portal.azure.com) → مورد **مشروع** Foundry الخاص بك.
2. انقر على **التحكم في الوصول (IAM)** → **تعيينات الأدوار**.
3. ابحث عن اسمك → تأكد أن **Foundry User** (أو التسمية القديمة **Azure AI User**) مدرجة.
4. إذا كانت مفقودة: **إضافة** → **إضافة تعيين دور** → ابحث عن **Foundry User** → عيّنها لحسابك.

راجع توثيق [RBAC لـ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) للتفاصيل.

### نشر النموذج غير متاح

إذا أعاد الوكيل أخطاء متعلقة بالنموذج:

1. تحقق من نشر النموذج: الشريط الجانبي Foundry → وسّع المشروع → **النماذج** → تحقق من `gpt-4.1-mini` (أو النموذج الخاص بك) بحالة **نجح**.
2. تحقق من تطابق اسم النشر: قارن `AZURE_AI_MODEL_DEPLOYMENT_NAME` في `.env` (أو `agent.yaml`) مع اسم النشر الفعلي في الشريط الجانبي.
3. إذا انتهت صلاحية النشر (الطبقة المجانية): أعد النشر من [كتالوج النموذج](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## مشكلات Foundry المحلي (المسار ب)

### خدمة Foundry المحلي غير قيد التشغيل

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| العَرَض | السبب | الإصلاح |
|---------|-------|-----|
| تحقق الصحة يعود `503` | الخدمة غير مشغلة | شغّل `foundry local start` أو انقر **Start** في الشريط الجانبي Foundry Toolkit |
| تحقق الصحة انتهى الوقت | النموذج لا يزال يُحمّل | انتظر 30-60 ثانية بعد البدء؛ النماذج الأكبر تحتاج وقتًا أطول |
| `StatusCode: 404` على `/v1/health` | منفذ خاطئ | المنفذ الافتراضي هو `5273`. تحقق من `foundry local status` للمنفذ الفعلي |
| موارد غير كافية | Foundry المحلي يحتاج إلى حوالي 4 غيغابايت ذاكرة RAM متاحة | أغلق التطبيقات الأخرى |
| فشل تنزيل النموذج | مساحة قرص منخفضة | النماذج حجمها 2-8 غيغابايت. حرر مساحة، ثم `foundry model pull <name>` |

### عدم تطابق اسم النموذج

```powershell
# List downloaded models and their exact aliases
foundry model list
```

اضبط `AZURE_AI_MODEL_DEPLOYMENT_NAME` في `.env` على الاسم المستعار الدقيق المعروض (مثل `phi-4-mini`، وليس `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` في تشغيل محلي (المسار ب)

يستخدم مختبر `main.py` `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. يتطلب Foundry المحلي أن يشير هذا المتغير إلى الخدمة المحلية - **ليس** `AZURE_AI_PROJECT_ENDPOINT`. تأكد من أن `.env` يحتوي على:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### أداة MCP لا تزال تجري اتصالاً صادرًا (المسار ب)

هذا متوقع. تجلب أداة `search_microsoft_learn_for_plan` الموارد التعليمية من `https://learn.microsoft.com/api/mcp`. **فقط استعلام اسم المهارة** يمر عبر الشبكة - تتم معالجة السيرة الذاتية ونص وصف الوظيفة بالكامل على جهازك ولا يتم إرساله أبدًا. إذا كان مطلوبًا التشغيل الكامل دون اتصال، أضف `try/except` احتياطي في الأداة يعيد عنوان URL `learn.microsoft.com` ثابت عندما لا يكون نقطة النهاية متاحة.

---

## الحصول على المساعدة

إذا كنت عالقًا بعد تجربة الإصلاحات أعلاه:

1. **تحقق من سجلات الخادم** - معظم الأخطاء تنتج تتبع مكدس بايثون في الطرفية. اقرأ التتبع بالكامل.
2. **ابحث عن رسالة الخطأ** - انسخ نص الخطأ وابحث في [Microsoft Q&A لخدمة Foundry Agent](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **افتح مشكلة** - قدِّم مشكلة في [مستودع الورشة](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) مع:
   - رسالة الخطأ أو لقطة شاشة
   - إصدارات الحزم الخاصة بك (`pip list | Select-String "agent-framework"`)
   - إصدار بايثون الخاص بك (`python --version`)
   - ما إذا كانت المشكلة محلية أو بعد النشر

---

### نقطة التحقق

- [ ] تعرف كيف تتحقق وتصلح مشكلات تكوين `.env`
- [ ] يمكنك التحقق من تطابق إصدارات الحزمة مع المصفوفة المطلوبة
- [ ] تعرف كيف تتحقق من سجلات الحاوية لأخطاء النشر
- [ ] يمكنك التحقق من أدوار RBAC في بوابة أزور

---

**السابق:** [07 - تحقق في Playground](07-verify-in-playground.md) · **التالي:** [09 - الملخص →](09-summary.md) · **الصفحة الرئيسية:** [README مختبر 02](../README.md) · [الصفحة الرئيسية للورشة](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**تنويه**:
تمت ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والمعتمد. للمعلومات الهامة، يُنصح بالاستعانة بترجمة بشرية محترفة. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->