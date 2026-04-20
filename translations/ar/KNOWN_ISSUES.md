# المشكلات المعروفة

يتتبع هذا المستند المشكلات المعروفة في حالة المستودع الحالية.

> آخر تحديث: 2026-04-15. تم الاختبار مقابل Python 3.13 / Windows في `.venv_ga_test`.

---

## تثبيتات الحزم الحالية (جميع الوكلاء الثلاثة)

| الحزمة | الإصدار الحالي |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(ثابت — انظر KI-003)* |

---

## KI-001 — ترقية GA 1.0.0 محجوبة: تم إزالة `agent-framework-azure-ai`

**الحالة:** مفتوحة | **شدة:** 🔴 عالية | **النوع:** كسر

### الوصف

تم **إزالة / إيقاف** حزمة `agent-framework-azure-ai` (مثبتة عند `1.0.0rc3`)
في إصدار GA (1.0.0، تاريخ الإصدار 2026-04-02). وتم استبدالها بـ:

- `agent-framework-foundry==1.0.0` — نمط الوكيل المستضاف على Foundry
- `agent-framework-openai==1.0.0` — نمط الوكيل المدعوم من OpenAI

جميع ملفات `main.py` الثلاثة تستورد `AzureAIAgentClient` من `agent_framework.azure`، والذي
يرمي `ImportError` عند استخدام حزم GA. مساحة الاسم `agent_framework.azure` لا تزال موجودة
في GA ولكنها تحتوي الآن فقط على فئات وظائف Azure (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — وليست وكلاء Foundry.

### الخطأ المؤكد (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### الملفات المتأثرة

| الملف | السطر |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` غير متوافق مع GA `agent-framework-core`

**الحالة:** مفتوحة | **شدة:** 🔴 عالية | **النوع:** كسر (محجوب على المصدر الأعلى)

### الوصف

تثبت `azure-ai-agentserver-agentframework==1.0.0b17` (الأحدث) بشكل صارم
`agent-framework-core<=1.0.0rc3`. تثبيتها جنبًا إلى جنب مع `agent-framework-core==1.0.0` (GA)
يجبر pip على **تخفيض** إصدار `agent-framework-core` مرة أخرى إلى `rc3`، مما يؤدي إلى تعطل
`agent-framework-foundry==1.0.0` و `agent-framework-openai==1.0.0`.

لذلك، النداء `from azure.ai.agentserver.agentframework import from_agent_framework` 
الذي يستخدمه جميع الوكلاء لربط خادم HTTP محجوب أيضًا.

### تعارض الاعتماد المؤكد (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### الملفات المتأثرة

جميع ملفات `main.py` الثلاثة — كل من الاستيراد في المستوى الأعلى والاستيراد داخل الدالة في `main()`.

---

## KI-003 — لم يعد مطلوبًا علم `agent-dev-cli --pre`

**الحالة:** ✅ تم الإصلاح (غير مسبب للكسر) | **الشدة:** 🟢 منخفضة

### الوصف

كانت جميع ملفات `requirements.txt` سابقًا تتضمن `agent-dev-cli --pre` لجلب
نسخة CLI ما قبل الإصدار. منذ إصدار GA 1.0.0 بتاريخ 2026-04-02، أصبح الإصدار المستقر من
`agent-dev-cli` متاحًا الآن بدون علم `--pre`.

**الإصلاح المطبق:** تمت إزالة علم `--pre` من جميع ملفات `requirements.txt` الثلاثة.

---

## KI-004 — ملفات Docker تستخدم `python:3.14-slim` (صورة أساسية ما قبل الإصدار)

**الحالة:** مفتوحة | **الشدة:** 🟡 منخفضة

### الوصف

جميع ملفات `Dockerfile` تستخدم `FROM python:3.14-slim` التي تتبع إصدار Python ما قبل الإصدار.
للنشر الإنتاجي يجب تثبيتها على إصدار مستقر (مثلًا `python:3.12-slim`).

### الملفات المتأثرة

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## المراجع

- [agent-framework-core على PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry على PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**إخلاء مسؤولية**:
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق. للمعلومات الحرجة، يُنصح بالاعتماد على ترجمة بشرية محترفة. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->