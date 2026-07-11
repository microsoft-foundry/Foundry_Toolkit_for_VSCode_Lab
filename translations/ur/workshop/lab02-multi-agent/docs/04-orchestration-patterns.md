# ماڈیول 4 - آرکیسٹریشن پیٹرن

⏱️ ~10 منٹ

اس ماڈیول میں، آپ Resume Job Fit Evaluator میں استعمال ہونے والے آرکیسٹریشن پیٹرنز کو تلاش کرتے ہیں اور سیکھتے ہیں کہ ورک فلو گراف کو کیسے پڑھا جائے، ترمیم کی جائے، اور بڑھایا جائے۔ ان پیٹرنز کو سمجھنا ڈیٹا فلو مسائل کو ڈی بگ کرنے اور اپنے [ملٹی ایجنٹ ورک فلو](https://learn.microsoft.com/agent-framework/workflows/) بنانے کے لیے ضروری ہے۔

---

## پیٹرن 1: تسلسل وار چین

ورک فلو میں بنیادی پیٹرن ایک **تسلسل وار چین** ہے - ہر ایجنٹ کی آؤٹ پٹ سیدھے اگلے میں جاتی ہے۔

```mermaid
flowchart LR
    RP[ریزیومے پارسر] --> JD[جے ڈی ایجنٹ]
    JD --> MA[میچنگ ایجنٹ]
    MA --> GA[گیپ اینالائزر]
```

کوڈ میں، ہر `add_edge()` کال چین میں ایک قدم بناتی ہے:

```python
.add_edge(resume_executor, jd_executor)       # ResumeParser کا آؤٹ پٹ → JD ایجنٹ
.add_edge(jd_executor, matching_executor)     # JD ایجنٹ کا آؤٹ پٹ → MatchingAgent
.add_edge(matching_executor, gap_executor)    # MatchingAgent کا آؤٹ پٹ → GapAnalyzer
```

> **تسلسل کیوں، نہ کہ fan-out/fan-in؟** `WorkflowBuilder` آنے والے ایجز کے لیے **OR-semantics** استعمال کرتا ہے: ایک نیچے والا ایگزیکیوٹر چلتا ہے جیسے ہی **کوئی بھی** پچھلا ایگزیکیوٹر مکمل ہو جائے۔ اگر `matching_executor` کے دو آنے والے ایجز ہوتے (دونوں `resume_executor` اور `jd_executor` سے)، تو یہ دو بار ٹرگر ہوتا - ایک بار جب ResumeParser ختم ہوتا ہے اور دوبارہ جب JD Agent ختم ہوتا ہے - اس سے GapAnalyzer بھی دو بار چلے گا اور آؤٹ پٹ دو بار ظاہر ہوگی۔ تسلسل والی پائپ لائن اس سے مکمل بچتی ہے۔

## پیٹرن 2: مواد کی ریلے

چونکہ `context_mode="last_agent"` کا مطلب ہے کہ ہر ایگزیکیوٹر صرف اپنے **براہ راست پچھلے ایجنٹ کی آؤٹ پٹ** دیکھتا ہے، تسلسل وار چین میں ایجنٹس کو واضح طور پر وہ ڈیٹا آگے بھیجنا ہوتا ہے جو نیچے والے ایجنٹس کو چاہیے۔

اس ورک فلو میں:
- **ResumeParser** JD کو ویربیٹم `[JOB DESCRIPTION PASS-THROUGH]` میں کاپی کرتا ہے (تاکہ JD Agent اسے تلاش کر سکے)۔
- **JD Agent** `[PARSED RESUME]` کو ویربیٹم `[PARSED RESUME PASS-THROUGH]` میں کاپی کرتا ہے (تاکہ MatchingAgent دونوں پروفائلز کا موازنہ کر سکے)۔

```
ResumeParser output
└─ [PARSED RESUME]               ← extracted by JD Agent
└─ [JOB DESCRIPTION PASS-THROUGH] ← extracted by JD Agent

JD Agent output
└─ [JD REQUIREMENTS]             ← extracted by MatchingAgent
└─ [PARSED RESUME PASS-THROUGH]  ← extracted by MatchingAgent
```

ہر ریلے سیکشن کو **ویربیٹم** کاپی کرنا چاہیے - خلاصہ کرنا یا پیرافریسنگ وہ نیچے والے ایجنٹ کو خراب کر دیتا ہے جو اس پر انحصار کرتا ہے۔

---

## مکمل گراف

تسلسل وار چین اور مواد کی ریلے پیٹرنز کو ملانے سے مکمل ورک فلو بنتا ہے:

```mermaid
flowchart LR
    U[صارف کا انپٹ] --> RP[ریزیومے پارسر]
    RP --> JD[جے ڈی ایجنٹ]
    JD --> MA[مماثلت کا ایجنٹ]
    MA --> GA[فرق تجزیہ کار + MCP]
    GA --> O[حتمی نتیجہ]
```

ایجنٹ انسپکٹر وہی گراف ڈھانچہ دکھاتا ہے جب ایجنٹ مقامی طور پر چل رہا ہو۔ اسکرین شاٹس کے لیے [ماڈیول 5 - مقامی طور پر ٹیسٹ کریں](05-test-locally.md) دیکھیں۔

---

## WorkflowBuilder کوڈ پڑھنا

مکمل `create_workflow()` فنکشن [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) میں ہے۔ تین `add_edge()` کالز تسلسل وار پائپ لائن بناتی ہیں:

| # | ایج | اثر |
|---|------|--------|
| 1 | `resume_executor → jd_executor` | JD Agent `[PARSED RESUME]` + `[JOB DESCRIPTION PASS-THROUGH]` وصول کرتا ہے |
| 2 | `jd_executor → matching_executor` | MatchingAgent `[JD REQUIREMENTS]` + `[PARSED RESUME PASS-THROUGH]` وصول کرتا ہے |
| 3 | `matching_executor → gap_executor` | GapAnalyzer فٹ رپورٹ + گیپ لسٹ وصول کرتا ہے |

---

## گراف میں ترمیم کرنا

### نیا ایجنٹ شامل کرنا

پانچواں ایجنٹ شامل کرنے کے لیے (مثلاً **InterviewPrepAgent** GapAnalyzer کے بعد):

1. `INTERVIEW_PREP_INSTRUCTIONS` مستقل مقدار تعریف کریں۔
2. `Agent` + `AgentExecutor` آبجیکٹس بنائیں (موجودہ چار کے جیسا پیٹرن)۔
3. `WorkflowBuilder` میں `.add_edge(gap_executor, interview_exec)` شامل کریں۔
4. `output_executors=[interview_exec]` کو اپڈیٹ کریں۔

> **اہم:** `start_executor` وہ واحد ایجنٹ ہے جو خام صارف ان پٹ حاصل کرتا ہے۔ باقی تمام ایجنٹس اپنے اپ اسٹریم ایج سے آؤٹ پٹ وصول کرتے ہیں۔

---

## عام گراف کی غلطیاں

| غلطی | علامت | حل |
|---------|---------|-----|
| `output_executors` کو ایج کا فقدان | ایجنٹ چلتا ہے مگر آؤٹ پٹ خالی ہے | یقین دہانی کریں کہ `start_executor` سے ہر ایجنٹ تک راستہ موجود ہے جو `output_executors` میں ہیں |
| سرکلر انحصار | لامتناہی لوپ یا ٹائم آؤٹ | چیک کریں کہ کوئی ایجنٹ اپنے اپ اسٹریم ایجنٹ میں واپس فیڈ نہ کر رہا ہو |
| `output_executors` میں ایجنٹ بغیر آنے والے ایج کے | آؤٹ پٹ خالی | کم از کم ایک `add_edge(source, that_agent)` شامل کریں |
| متعدد `output_executors` بغیر fan-in کے | آؤٹ پٹ صرف ایک ایجنٹ کی جواب پر مشتمل ہے | ایک واحد آؤٹ پٹ ایجنٹ استعمال کریں جو ان کا مجموعہ بنائے، یا متعدد آؤٹ پٹس قبول کریں |
| `start_executor` نہیں دیا گیا | تعمیر کے وقت `ValueError` | ہمیشہ `WorkflowBuilder()` میں `start_executor` کی وضاحت کریں |

---

## گراف کی ڈی بگنگ

### ایجنٹ انسپکٹر استعمال کرنا

1. F5 کے ساتھ ایجنٹ مقامی طور پر شروع کریں۔
2. ایجنٹ انسپکٹر کھولیں (`Ctrl+Shift+P` → **Foundry Toolkit: Open Agent Inspector**)۔
3. ٹیسٹ پیغام بھیجیں۔
4. انسپکٹر کی ردعمل پینل میں **streaming output** دیکھیں - یہ ہر ایجنٹ کے حصے کو تسلسل میں دکھاتا ہے۔


### لاگنگ استعمال کرنا

`main.py` میں لاگنگ شامل کریں تاکہ ڈیٹا فلو کا پتہ چل سکے:

```python
import logging
logger = logging.getLogger("resume-job-fit")

# مین() میں، ورک فلو بنانے کے بعد:
logger.info("Workflow graph built with edges: RP→JD, JD→MA, MA→GA")
```

سرور کے لاگز ایجنٹ کی عملدرآمد کی ترتیب اور MCP ٹول کالز دکھاتے ہیں:

```
INFO:agent_framework:Executing agent: ResumeParser
INFO:agent_framework:Executing agent: JobDescriptionAgent
INFO:agent_framework:Executing agent: MatchingAgent
INFO:agent_framework:Executing agent: GapAnalyzer
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Kubernetes")
POST https://learn.microsoft.com/api/mcp → 200
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Terraform")
POST https://learn.microsoft.com/api/mcp → 200
```

---

### چیک پوائنٹ

- [ ] آپ ورک فلو میں دو آرکیسٹریشن پیٹرنز کی نشاندہی کر سکتے ہیں: تسلسل وار چین اور مواد کی ریلے
- [ ] آپ سمجھتے ہیں کہ کیوں `context_mode="last_agent"` ایجنٹس کے درمیان واضح ڈیٹا ریلے کا تقاضا کرتا ہے
- [ ] آپ `WorkflowBuilder` کوڈ پڑھ سکتے ہیں اور ہر `add_edge()` کو کال کو بصری گراف سے جوڑ سکتے ہیں
- [ ] آپ جانتے ہیں کہ پائپ لائن کے آخر میں نیا ایجنٹ کیسے شامل کریں
- [ ] آپ عام گراف کی غلطیاں اور ان کی علامات کی شناخت کر سکتے ہیں

---

**پچھلا:** [03 - ایجنٹس اور ماحول ترتیب دیں](03-configure-agents.md) · **اگلا:** [05 - مقامی طور پر ٹیسٹ کریں →](05-test-locally.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->