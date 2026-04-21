# مشکلات شناخته شده

این سند مشکلات شناخته شده با وضعیت فعلی مخزن را ردیابی می‌کند.

> آخرین به‌روزرسانی: 2026-04-15. آزمایش شده بر روی Python 3.13 / Windows در `.venv_ga_test`.

---

## ورژن‌های فعلی پکیج‌ها (هر سه عامل)

| پکیج | نسخه فعلی |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(اصلاح شده — به KI-003 نگاه کنید)* |

---

## KI-001 — ارتقاء GA 1.0.0 مسدود شده: حذف `agent-framework-azure-ai`

**وضعیت:** باز | **شدت:** 🔴 بالا | **نوع:** شکست‌خورنده

### توضیحات

پکیج `agent-framework-azure-ai` (سنجاق شده روی `1.0.0rc3`) در نسخه GA (1.0.0، منتشر شده در 2026-04-02) **حذف/منسوخ شده** است.
این پکیج جایگزین شده با:

- `agent-framework-foundry==1.0.0` — الگوی عامل میزبانی شده توسط Foundry
- `agent-framework-openai==1.0.0` — الگوی عامل پشتیبانی شده توسط OpenAI

هر سه فایل `main.py` کلاسی به نام `AzureAIAgentClient` را از `agent_framework.azure` وارد می‌کنند، که در نسخه‌های GA باعث ایجاد خطای `ImportError` می‌شود. فضای نام `agent_framework.azure` هنوز در GA وجود دارد
اما اکنون فقط شامل کلاس‌های Azure Functions است (`DurableAIAgent`، `AzureAISearchContextProvider`، `CosmosHistoryProvider`) — نه عوامل Foundry.

### خطای تأیید شده (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### فایل‌های متاثر

| فایل | خط |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — ناسازگاری `azure-ai-agentserver` با `agent-framework-core` نسخه GA

**وضعیت:** باز | **شدت:** 🔴 بالا | **نوع:** شکست‌خورنده (مسدود شده توسط upstream)

### توضیحات

نسخه `azure-ai-agentserver-agentframework==1.0.0b17` (آخرین نسخه) به شدت سنجاق شده است به
`agent-framework-core<=1.0.0rc3`. نصب آن در کنار `agent-framework-core==1.0.0` (GA)
باعث می‌شود pip نسخه `agent-framework-core` را به `rc3` **تنزیل دهد**، که سپس باعث خرابی
`agent-framework-foundry==1.0.0` و `agent-framework-openai==1.0.0` می‌شود.

در نتیجه تماس `from azure.ai.agentserver.agentframework import from_agent_framework` که توسط همه
عوامل برای اتصال سرور HTTP استفاده می‌شود نیز مسدود شده است.

### تداخل وابستگی تأیید شده (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### فایل‌های متاثر

هر سه فایل `main.py` — هم واردات سطح بالایی و هم واردات داخل تابع `main()`.

---

## KI-003 — دیگر نیازی به فلگ `agent-dev-cli --pre` نیست

**وضعیت:** ✅ اصلاح شده (غیر شکست‌خورنده) | **شدت:** 🟢 کم

### توضیحات

تمام فایل‌های `requirements.txt` قبلاً شامل `agent-dev-cli --pre` بودند تا نسخه پیش‌انتشار CLI را بگیرند.
از زمان انتشار GA 1.0.0 در 2026-04-02، نسخه پایدار `agent-dev-cli` بدون فلگ `--pre` اکنون در دسترس است.

**اصلاح اعمال شده:** فلگ `--pre` از هر سه فایل `requirements.txt` حذف شده است.

---

## KI-004 — فایل‌های Docker از `python:3.14-slim` (تصویر پایه پیش‌انتشار) استفاده می‌کنند

**وضعیت:** باز | **شدت:** 🟡 کم

### توضیحات

تمام فایل‌های `Dockerfile` از تصویر پایه `FROM python:3.14-slim` استفاده می‌کنند که مربوط به ساخت پیش‌انتشار Python است.
برای استقرار در محیط تولید باید به نسخه پایدار سنجاق شود (مثلاً `python:3.12-slim`).

### فایل‌های متاثر

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## مراجع

- [agent-framework-core در PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry در PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه ماشینی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما برای دقت تلاش می‌کنیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است شامل خطاها یا نادقتی‌هایی باشند. سند اصلی به زبان بومی خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حساس، ترجمه انسانی حرفه‌ای توصیه می‌شود. ما مسئول هیچ گونه سوءتفاهم یا تفسیر نادرست ناشی از استفاده از این ترجمه نیستیم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->