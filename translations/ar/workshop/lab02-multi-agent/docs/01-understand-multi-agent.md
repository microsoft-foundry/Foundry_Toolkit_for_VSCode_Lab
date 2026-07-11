# الوحدة 1 - فهم البنية

⏱️ ~5 دقائق

قبل كتابة أي كود، إليك نظرة سريعة على ما تقوم ببنائه وكيف يعمل.

---

## ما تبنيه

تقوم بلصق **السيرة الذاتية** و **الوصف الوظيفي**. يعيد سير العمل:

- درجة الملاءمة (0–100 مع تفصيل)
- قائمة بالفجوات في المهارات والشهادات
- خريطة تعلم شخصية مع روابط Microsoft Learn لكل فجوة

---

## الوكلاء الأربعة

الوكيل الواحد الذي يحاول التحليل والتقييم والتخطيط في آنٍ واحد يميل إلى العجلة وإنتاج مخرجات سطحية. تقسيم العمل إلى أربعة وكلاء متخصصين يعطي نتائج أفضل:

| الوكيل | ما يقوم به |
|-------|-------------|
| **ResumeParser** | يحلل السيرة الذاتية؛ ينسخ الوصف الوظيفي حرفيًا إلى `[JOB DESCRIPTION PASS-THROUGH]` للوكلاء التاليين |
| **JobDescriptionAgent** | يستخرج متطلبات الوصف الوظيفي من المار السابق؛ يرسل `[PARSED RESUME]` للأمام كـ `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | يقارن الأقسام الموسومة؛ ينتج درجة ملاءمة من 0–100 وقائمة بالفجوات |
| **GapAnalyzer** | يبني خريطة تعلم؛ يبحث في Microsoft Learn عن كل فجوة |

---

## مخطط التنسيق

سير العمل هو **خط أنابيب تسلسلي** - كل وكيل يمرر مخرجاته إلى التالي:

```mermaid
flowchart LR
    A["مدخلات المستخدم"] --> B["محلل السيرة الذاتية"]
    B -- "السيرة الذاتية المحللة + نقل وصف الوظيفة" --> C["وكيل وصف الوظيفة"]
    C -- "متطلبات وصف الوظيفة + نقل السيرة الذاتية" --> D["وكيل المطابقة"]
    D -- "تقرير التوافق + الفجوات" --> E["محلل الفجوات + MCP"]
    E --> F["المخرجات النهائية"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** يستقبل إدخال المستخدم، يحلل السيرة الذاتية، وينسخ الوصف الوظيفي إلى `[JOB DESCRIPTION PASS-THROUGH]`.
2. **JD Agent** يستخرج المتطلبات المهيكلة ويرسل `[PARSED RESUME PASS-THROUGH]` للأمام.
3. **MatchingAgent** يقارن كلا الجزأين وينتج درجة ملاءمة وقائمة فجوات.
4. **GapAnalyzer** يبني الخريطة وينادي أداة MCP من Microsoft Learn لكل فجوة.

---

## كيف يتم ربط هذا بالكود

في `main.py`، تصف هذا المخطط باستخدام `WorkflowBuilder`:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # الوكيل الأول لتلقي إدخال المستخدم
        output_executors=[gap_executor],      # الوكيل الأخير - مخرجه هو الرد
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → وكيل الوصف الوظيفي
    .add_edge(jd_executor, matching_executor)     # وكيل الوصف الوظيفي → وكيل المطابقة
    .add_edge(matching_executor, gap_executor)    # وكيل المطابقة → محلل الفجوات
    .build()
    .as_agent()
)
```

كل `Agent` ملفوف في `AgentExecutor`. استدعاءات `add_edge()` تحدد خط أنابيب تسلسلي صارم - كل وكيل يستقبل فقط مخرجات الوكيل السابق المباشر.

> `context_mode="last_agent"` يعني أن كل منفذ يرى فقط مخرجات الوكيل السابق المباشر له. يقوم كل من ResumeParser و JD Agent بتمرير البيانات للأمام في أقسام معنونة حتى يكون لدى كل وكيل لاحق ما يحتاجه تحديدًا.

---

## أداة MCP

لدى GapAnalyzer أداة واحدة: `search_microsoft_learn_for_plan`. تتصل بـ `https://learn.microsoft.com/api/mcp` وتُرجع روابط Microsoft Learn الحقيقية لكل فجوة مهارية.

عندما تعمل الأداة سترى هذه السجلات - كلها متوقعة:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

لا تقلق إلا إذا أعاد `POST` خطأ.

---

**السابق:** [00 - Prerequisites](00-prerequisites.md) · **التالي:** [02 - Scaffold the Project →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**تنويه**:
تمت ترجمة هذا المستند باستخدام خدمة الترجمة بالذكاء الاصطناعي [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والمعتمد. للمعلومات الهامة، يُنصح بالاستعانة بترجمة بشرية محترفة. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->