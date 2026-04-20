# معلوم مسائل

یہ دستاویز موجودہ ریپوزیٹری کی حالت میں معروف مسائل کا پتہ لگاتی ہے۔

> آخری تازہ کاری: 2026-04-15۔ Python 3.13 / Windows میں `.venv_ga_test` کے خلاف جانچا گیا۔

---

## موجودہ پیکیج پنز (تینوں ایجنٹس کے لیے)

| پیکیج | موجودہ ورژن |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(درست شدہ — دیکھیں KI-003)* |

---

## KI-001 — GA 1.0.0 اپ گریڈ روکا گیا: `agent-framework-azure-ai` ہٹا دیا گیا

**حالت:** کھلا | **شدت:** 🔴 زیادہ | **قسم:** بریکنگ

### تفصیل

`agent-framework-azure-ai` پیکیج (جو `1.0.0rc3` پر پن کیا گیا ہے) کو GA ریلیز (1.0.0، جاری ہوا 2026-04-02) میں **ہٹا یا مطرود** کیا گیا ہے۔ اسے درج ذیل سے بدل دیا گیا ہے:

- `agent-framework-foundry==1.0.0` — Foundry کی میزبانی والا ایجنٹ پیٹرن
- `agent-framework-openai==1.0.0` — OpenAI کی حمایت یافتہ ایجنٹ پیٹرن

تینوں `main.py` فائلیں `AzureAIAgentClient` کو `agent_framework.azure` سے درآمد کرتی ہیں، جو GA پیکیجز کے تحت `ImportError` پیدا کرتا ہے۔ `agent_framework.azure` نام جگہ GA میں ابھی بھی موجود ہے لیکن اب صرف Azure Functions کلاسز (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) پر مشتمل ہے — Foundry ایجنٹس نہیں ہیں۔

### تصدیق شدہ خرابی (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### متاثرہ فائلیں

| فائل | لائن |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` کے ساتھ غیر مطابقت رکھتا ہے

**حالت:** کھلا | **شدت:** 🔴 زیادہ | **قسم:** بریکنگ (اپ اسٹریم پر روکا ہوا)

### تفصیل

`azure-ai-agentserver-agentframework==1.0.0b17` (تازہ ترین) سختی سے `agent-framework-core<=1.0.0rc3` کو پن کرتا ہے۔ اسے `agent-framework-core==1.0.0` (GA) کے ساتھ انسٹال کرنے سے pip مجبور ہو جاتا ہے کہ `agent-framework-core` کو واپس `rc3` پر ڈاؤن گریڈ کرے، جو پھر `agent-framework-foundry==1.0.0` اور `agent-framework-openai==1.0.0` کو توڑ دیتا ہے۔

تمام ایجنٹس کے ذریعے HTTP سرور کو بائنڈ کرنے کے لیے استعمال ہونے والی `from azure.ai.agentserver.agentframework import from_agent_framework` کال بھی اس لیے بلاک کر دی گئی ہے۔

### تصدیق شدہ انحصاری تنازعہ (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### متاثرہ فائلیں

تینوں `main.py` فائلیں — اوپری سطح کی درآمد اور `main()` میں فنکشن کے اندر درآمد دونوں۔

---

## KI-003 — `agent-dev-cli --pre` فلیگ کی مزید ضرورت نہیں

**حالت:** ✅ درست شدہ (غیر بریکنگ) | **شدت:** 🟢 کم

### تفصیل

تمام `requirements.txt` فائلوں میں پہلے `agent-dev-cli --pre` شامل تھا تاکہ پری ریلیز CLI کو حاصل کیا جا سکے۔ چونکہ GA 1.0.0 2026-04-02 کو جاری ہو چکا ہے، `agent-dev-cli` کی مستحکم ریلیز اب `--pre` فلیگ کے بغیر دستیاب ہے۔

**درستگی لاگو کی گئی:** تینوں `requirements.txt` فائلوں سے `--pre` فلیگ ہٹا دیا گیا ہے۔

---

## KI-004 — Dockerfiles `python:3.14-slim` استعمال کرتے ہیں (پری ریلیز بیس امیج)

**حالت:** کھلا | **شدت:** 🟡 کم

### تفصیل

تمام `Dockerfile`s `FROM python:3.14-slim` استعمال کرتے ہیں جو کہ پری ریلیز پائتھن بلڈ کی نمائندگی کرتا ہے۔ پیداوار کی تنصیبات کے لیے اسے مستحکم ریلیز (مثلاً، `python:3.12-slim`) پر پن کیا جانا چاہیے۔

### متاثرہ فائلیں

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## حوالہ جات

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**دفاعی بیان**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کا استعمال کرتے ہوئے ترجمہ کی گئی ہے۔ جب کہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات کا خیال رکھیں کہ خودکار ترجموں میں غلطیاں یا غیر درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنی مادری زبان میں مستند ذریعہ سمجھی جانی چاہیے۔ اہم معلومات کے لیے پیشہ ور انسانی ترجمہ تجویز کیا جاتا ہے۔ ہم اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تعبیرات کے ذمہ دار نہیں ہیں۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->