# בעיות ידועות

מסמך זה עוקב אחר בעיות ידועות במצב הנוכחי של המאגר.

> עודכן לאחרונה: 2026-04-15. נבדק מול Python 3.13 / Windows ב-`.venv_ga_test`.

---

## גרסאות הנוכחיות של החבילות (כל שלושת הסוכנים)

| חבילה | גרסה נוכחית |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(תוקן — ראה KI-003)* |

---

## KI-001 — שדרוג GA 1.0.0 נחסם: `agent-framework-azure-ai` הוסר

**סטטוס:** פתוח | **חומרה:** 🔴 גבוהה | **סוג:** משבית

### תיאור

חבילת `agent-framework-azure-ai` (נעולה ב-`1.0.0rc3`) **הוסרה/הועמסה** בגרסת GA (1.0.0, יצאה 2026-04-02). היא הוחלפה ב:

- `agent-framework-foundry==1.0.0` — תבנית סוכן מתארחת בפאונדרי
- `agent-framework-openai==1.0.0` — תבנית סוכן מבוססת OpenAI

כל שלושת קבצי `main.py` מייבאים `AzureAIAgentClient` מ-`agent_framework.azure`, דבר
המוביל ל-`ImportError` תחת חבילות GA. המרחב שמות `agent_framework.azure` עדיין קיים ב-GA
אך כעת מכיל רק מחלקות Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — לא סוכני Foundry.

### שגיאה מאומתת (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### קבצים מושפעים

| קובץ | שורה |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` לא תואם ל-GA `agent-framework-core`

**סטטוס:** פתוח | **חומרה:** 🔴 גבוהה | **סוג:** משבית (חסום על ידי מעלה)

### תיאור

`azure-ai-agentserver-agentframework==1.0.0b17` (העדכנית ביותר) נעילה למחסום
`agent-framework-core<=1.0.0rc3`. התקנתה לצד `agent-framework-core==1.0.0` (GA)
כופה על pip **הורדה בחזרה** של `agent-framework-core` לגרסת rc3, מה שמפסיק את
`agent-framework-foundry==1.0.0` ו-`agent-framework-openai==1.0.0`.

קריאת `from azure.ai.agentserver.agentframework import from_agent_framework` המשמשת את כל
הסוכנים לקישור שרת HTTP גם כן חסומה.

### קונפליקט תלות מאומת (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### קבצים מושפעים

כל שלושת קבצי `main.py` — הן הייבוא העל-רמה והן הייבוא בתוך הפונקציה ב-`main()`.

---

## KI-003 — דגל `agent-dev-cli --pre` אינו נדרש יותר

**סטטוס:** ✅ תוקן (לא משבית) | **חומרה:** 🟢 נמוכה

### תיאור

כל קבצי `requirements.txt` כללו קודם `agent-dev-cli --pre` כדי למשוך את
גרסת CLI לפני-שחרור. מאז צאת GA 1.0.0 ב-2026-04-02, גרסת הייצור היציבה של
`agent-dev-cli` זמינה כעת ללא דגל `--pre`.

**תיקון יושם:** דגל `--pre` הוסר מכל שלושת קבצי `requirements.txt`.

---

## KI-004 — קבצי Docker משתמשים ב-`python:3.14-slim` (תמונה בסיסית לפני שחרור)

**סטטוס:** פתוח | **חומרה:** 🟡 נמוכה

### תיאור

כל קבצי `Dockerfile` משתמשים ב-`FROM python:3.14-slim` אשר עוקב אחרי בניית Python לפני השחרור.
לפריסות בייצור מומלץ לנעול לגרסה יציבה (למשל, `python:3.12-slim`).

### קבצים מושפעים

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## הפניות

- [agent-framework-core ב-PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry ב-PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב免责声明**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים לכלול שגיאות או אי-דיוקים. המסמך המקורי בשפת המקור שלו הוא המקור הסמכותי. למידע חשוב או קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אנושי. אנו לא נושאים באחריות לכל אי הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->