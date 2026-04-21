# מודול 8 - פתרון בעיות (רב-סוכנים)

מודול זה מכסה שגיאות נפוצות, תיקונים ואסטרטגיות דיבוג ספציפיות לזרימת עבודה רב-סוכנים. בנושאי פריסת Foundry כלליים, יש להתייעץ גם עם [מדריך פתרון בעיות למעבדה 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## התייחסות מהירה: שגיאה → תיקון

| שגיאה / תסמין | סיבה סבירה | תיקון |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | חסר קובץ `.env` או הערכים לא הוגדרו | צור `.env` עם `PROJECT_ENDPOINT=<your-endpoint>` ו-`MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | סביבת וירטואלית לא הופעלה או התלויות לא הותקנו | הרץ `.\.venv\Scripts\Activate.ps1` ואז `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | חבילת MCP לא מותקנת (חסרה ב-requirements) | הרץ `pip install mcp` או בדוק ש־`requirements.txt` כוללת אותה כתלות עקיפה |
| הסוכן מתחיל אך מחזיר תגובה ריקה | אי התאמה ב-`output_executors` או חסרים קשתות | ודא ש-`output_executors=[gap_analyzer]` ושהכל הקשתות קיימות ב-`create_workflow()` |
| יש רק כרטיס פער אחד (שאר חסרים) | הוראות GapAnalyzer לא שלמות | הוסף את הפסקה `CRITICAL:` ל-`GAP_ANALYZER_INSTRUCTIONS` - ראה [מודול 3](03-configure-agents.md) |
| ניקוד Fit הוא 0 או חסר | ה-MatchingAgent לא קיבל נתונים מקדימה | ודא ש-`add_edge(resume_parser, matching_agent)` וגם `add_edge(jd_agent, matching_agent)` קיימות |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | שרת MCP דחה את קריאת הכלי | בדוק חיבור לאינטרנט. נסה לפתוח `https://learn.microsoft.com/api/mcp` בדפדפן. נסה שוב |
| אין כתובות Microsoft Learn ביציאה | כלי MCP לא רשום או נקודת קצה שגויה | ודא ש-`tools=[search_microsoft_learn_for_plan]` ב-GapAnalyzer ו-`MICROSOFT_LEARN_MCP_ENDPOINT` נכונים |
| `Address already in use: port 8088` | תהליך אחר משתמש בפורט 8088 | הרץ `netstat -ano \| findstr :8088` (Windows) או `lsof -i :8088` (macOS/Linux) ועצור את התהליך המתנגש |
| `Address already in use: port 5679` | התנגשות פורט Debugpy | עצור סשנים אחרים של דיבוג. הרץ `netstat -ano \| findstr :5679` למציאת התהליך והרג אותו |
| Agent Inspector לא נפתח | השרת לא התחיל במלואו או התנגשות פורטים | המתן ל"Server running" בלוג. בדוק שפורט 5679 חופשי |
| `azure.identity.CredentialUnavailableError` | לא חתום ל-Azure CLI | הרץ `az login` ואז הפעל מחדש את השרת |
| `azure.core.exceptions.ResourceNotFoundError` | פריסת המודל לא קיימת | בדוק ש-`MODEL_DEPLOYMENT_NAME` תואם למודל פרוס בפרויקט Foundry שלך |
| סטטוס הקונטיינר "Failed" אחרי פריסה | הקונטיינר קרס בהפעלה | בדוק לוגי קונטיינר בפאנל הצדדי של Foundry. נפוץ: משתנה סביבה חסר או שגיאת ייבוא |
| הפריסה מציגה "Pending" יותר מ־5 דקות | הקונטיינר מתעכב באתחול או מגבלות משאבים | המתן עד 5 דקות עבור רב-סוכן (יוצר 4 מופעי סוכן). אם עדיין תלוי, בדוק לוגים |
| `ValueError` מ־`WorkflowBuilder` | תצורת גרף לא תקינה | ודא ש-`start_executor` מוגדר, `output_executors` הוא רשימה, ואין קשתות מעגליות |

---

## בעיות סביבה ולקונפיגורציה

### ערכי `.env` חסרים או שגויים

קובץ `.env` חייב להיות בתיקיית `PersonalCareerCopilot/` (אותו רמה שבה נמצא `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

תוכן צפוי של `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **איך למצוא את PROJECT_ENDPOINT שלך:**  
- פתח את סרגל הצד של **Microsoft Foundry** ב-VS Code → קליק ימני על הפרויקט שלך → **Copy Project Endpoint**.  
- או עבור ל-[Azure Portal](https://portal.azure.com) → הפרויקט שלך ב-Foundry → **Overview** → **Project endpoint**.

> **איך למצוא את MODEL_DEPLOYMENT_NAME שלך:** בסרגל הצד של Foundry, פתח את הפרויקט שלך → **Models** → מצא את שם המודל שפרסת (לדוגמה, `gpt-4.1-mini`).

### קדימות משתני סביבה

`main.py` משתמש ב-`load_dotenv(override=False)`, כלומר:

| עדיפות | מקור | מנצח כאשר שניהם מוגדרים? |
|----------|--------|------------------------|
| 1 (הגבוהה ביותר) | משתנה סביבת shell | כן |
| 2 | קובץ `.env` | רק אם משתנה shell לא מוגדר |

משמעות הדבר היא שמשתני סביבת הריצה של Foundry (המוגדרים ב-`agent.yaml`) גוברים על ערכי `.env` במהלך פריסה מתארחת.

---

## תאימות גרסאות

### מטריצת גרסאות חבילות

זרימת העבודה רב-הסוכנים דורשת גרסאות חבילות ספציפיות. גרסאות לא תואמות גורמות לשגיאות ריצה.

| חבילה | גרסה נדרשת | פקודת בדיקה |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | גרסת טרום-שחרור אחרונה | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### שגיאות גרסה נפוצות

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# תיקון: שדרוג ל-rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` לא נמצא או Inspector לא תואם:**

```powershell
# תיקון: התקנה עם הדגל --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# תיקון: שדרג חבילת mcp
pip install mcp --upgrade
```

### וודא את כל הגרסאות בבת אחת

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

תוצאה צפויה:

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

## בעיות בכלי MCP

### כלי MCP מחזיר ללא תוצאות

**תסמין:** כרטיסי הפער מציגים "No results returned from Microsoft Learn MCP" או "No direct Microsoft Learn results found".

**סיבות אפשריות:**

1. **בעיה ברשת** - נקודת הקצה של MCP (`https://learn.microsoft.com/api/mcp`) לא נגישה.  
   ```powershell
   # בדוק חיבוריות
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
 אם זה מחזיר `200`, הנקודה נגישה.

2. **שאילתא ספציפית מדי** - שם הכישור מדויק מדי לחיפוש Microsoft Learn.  
   - זה צפוי לכישורים מאוד מתמחים. לכלי יש URL גיבוי בתגובה.

3. **פסק זמן של סשן MCP** - חיבור HTTP זרם זמן אתחול.  
   - נסה לבצע שוב את הבקשה. סשני MCP הם זמניים ועלולים לדרוש חיבור מחדש.

### הסברים ללוגים של MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| לוג | משמעות | פעולה |
|-----|---------|--------|
| `GET → 405` | בדיקות לקוח MCP במהלך אתחול | נורמלי - התעלם |
| `POST → 200` | קריאת כלי הצליחה | צפוי |
| `DELETE → 405` | בדיקות לקוח MCP במהלך ניקוי | נורמלי - התעלם |
| `POST → 400` | בקשה גרועה (שאילתה שגויה) | בדוק את הפרמטר `query` ב-`search_microsoft_learn_for_plan()` |
| `POST → 429` | מוגבל קצב | המתן ונסה שוב. הקטן את פרמטר `max_results` |
| `POST → 500` | שגיאת שרת MCP | מצב זמני - נסה שוב. אם מתמיד, ייתכן ש-API של Microsoft Learn MCP למטה |
| פסק זמן חיבור | בעיית רשת או שרת MCP לא זמין | בדוק אינטרנט. נסה `curl https://learn.microsoft.com/api/mcp` |

---

## בעיות פריסה

### הקונטיינר נכשל להפעיל אחרי פריסה

1. **בדוק לוגים של הקונטיינר:**  
   - פתח את סרגל הצד של **Microsoft Foundry** → פתח **Hosted Agents (Preview)** → לחץ על הסוכן שלך → פתח את הגרסה → **Container Details** → **Logs**.  
   - חפש עקבות שגיאות של Python או שגיאות מודול חסר.

2. **כשלונות אתחול נפוצים בקונטיינר:**

   | שגיאה בלוג | סיבה | תיקון |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | חסר חבילה ב־`requirements.txt` | הוסף את החבילה, בצע פריסה מחדש |
   | `RuntimeError: Missing required environment variable` | משתני סביבה ב-`agent.yaml` לא הוגדרו | עדכן את `agent.yaml` → סעיף `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | זהות מנוהלת לא מוגדרת | Foundry מגדיר אוטומטית - ודא שאתה מפרסם דרך התוסף |
   | `OSError: port 8088 already in use` | Dockerfile חושף פורט לא נכון או התנגשות פורטים | ודא ש-`EXPOSE 8088` ב-Dockerfile ו-`CMD ["python", "main.py"]` נכונים |
   | יציאת קוד 1 מהקונטיינר | יוצא מן הכלל לא מטופל ב-`main()` | הרץ בדיקה מקומית קודם ([מודול 5](05-test-locally.md)) כדי לתפוס שגיאות לפני פריסה |

3. **פריסה מחדש אחרי תיקון:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → בחר את אותו סוכן → פרוס גרסה חדשה.

### פריסה אורכת זמן רב מדי

קונטיינרים רב-סוכנים לוקחים יותר זמן אתחול כי הם יוצרים 4 מופעי סוכן באתחול. זמני אתחול רגילים:

| שלב | משך צפוי |
|-------|------------------|
| בניית תמונת קונטיינר | 1-3 דקות |
| דחיפת תמונה ל-ACR | 30-60 שניות |
| התחלת קונטיינר (סוכן יחיד) | 15-30 שניות |
| התחלת קונטיינר (רב-סוכנים) | 30-120 שניות |
| סוכן זמין ב-Playground | 1-2 דקות אחרי "Started" |

> אם הסטטוס "Pending" נמשך יותר מ-5 דקות, בדוק את לוג הקונטיינר לשגיאות.

---

## בעיות RBAC והרשאות

### `403 Forbidden` או `AuthorizationFailed`

אתה צריך את התפקיד **[Azure AI User](https://aka.ms/foundry-ext-project-role)** בפרויקט Foundry שלך:

1. עבור ל-[Azure Portal](https://portal.azure.com) → למשאב **הפרויקט** של Foundry שלך.  
2. לחץ על **Access control (IAM)** → **Role assignments**.  
3. חפש את שמך → ודא ש-**Azure AI User** מופיע.  
4. אם חסר: **Add** → **Add role assignment** → חפש **Azure AI User** → הקצה לחשבון שלך.

ראה את תיעוד [RBAC ל-Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) לפרטים.

### פריסת מודל לא נגישה

אם הסוכן מחזיר שגיאות הקשורות למודל:

1. ודא שהמודל פרוס: בפאנל הצדדי של Foundry → פתח את הפרויקט → **Models** → בדוק אם `gpt-4.1-mini` (או המודל שלך) עם סטטוס **Succeeded**.  
2. ודא ששם הפריסה תואם: השווה בין `MODEL_DEPLOYMENT_NAME` ב-`.env` (או `agent.yaml`) לבין שם הפריסה בפאנל הצדדי.  
3. אם הפריסה פגה (שכבת חינם): פרוס מחדש מ-[Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## בעיות ב-Agent Inspector

### Inspector נפתח אך מציג "Disconnected"

1. ודא שהשרת רץ: בדוק לוג עם "Server running on http://localhost:8088" במסוף.  
2. בדוק את פורט `5679`: Inspector מתחבר דרך debugpy על פורט 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. הפעל מחדש את השרת ופתח שוב את Inspector.

### Inspector מציג תגובה חלקית

תגובות רב-סוכנים ארוכות וזורמות בהדרגה. המתן לסיום התגובה המלאה (יכול לקחת 30-60 שניות בהתאם למספר כרטיסי הפער וקריאות כלי MCP).

אם התגובה נחתכת באופן עקבי:  
- בדוק שהוראות GapAnalyzer כוללות את בלוק `CRITICAL:` שמונע איחוד של כרטיסי פער.  
- בדוק את מגבלת הטוקנים של המודל שלך - `gpt-4.1-mini` תומך עד 32K טוקנים ביציאה, דבר שצריך להספיק.

---

## טיפים לביצועים

### תגובות איטיות

זרימות עבודה רב-סוכנים איטיות מטבען מפני שיש תלות סדרתית וקריאות לכלי MCP.

| אופטימיזציה | איך | השפעה |
|-------------|-----|--------|
| הקטן את קריאות MCP | הורד את פרמטר `max_results` בכלי | פחות סבבי HTTP |
| פשט את ההוראות | שפרומפטים קצרים וממוקדים יותר לסוכן | זיהוי מהיר יותר של LLM |
| השתמש ב-`gpt-4.1-mini` | מהיר יותר מ-`gpt-4.1` לפיתוח | שיפור מהירות כ-2x |
| הקטן את פירוט כרטיסי הפער | פשט את פורמט כרטיסי הפער בהוראות GapAnalyzer | פחות פלט ליצירה |

### זמנים טיפוסיים לתגובה (מקומי)

| תצורה | זמן צפוי |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 כרטיסי פער | 30-60 שניות |
| `gpt-4.1-mini`, 8+ כרטיסי פער | 60-120 שניות |
| `gpt-4.1`, 3-5 כרטיסי פער | 60-120 שניות |
---

## קבלת עזרה

אם נתקעת לאחר שניסית את התיקונים למעלה:

1. **בדוק את יומני השרת** - רוב השגיאות מייצרות עקבת מחסנית של פייתון במסוף. קרא את שאר העקבות.
2. **חפש את הודעת השגיאה** - העתק את טקסט השגיאה וחפש ב-[Microsoft Q&A עבור Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **פתח תקלה** - הגש תקלה ב-[מאגר הסדנה](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) עם:
   - הודעת השגיאה או צילום מסך
   - גרסאות החבילות שלך (`pip list | Select-String "agent-framework"`)
   - גרסת הפייתון שלך (`python --version`)
   - האם הבעיה מקומית או לאחר פריסה

---

### נקודת ביקורת

- [ ] אתה יכול לזהות ולתקן את השגיאות הנפוצות ביותר של סוכנים מרובים באמצעות טבלת ההתייחסות המהירה
- [ ] אתה יודע כיצד לבדוק ולתקן בעיות תצורת `.env`
- [ ] אתה יכול לוודא שגרסאות החבילות תואמות למטריצה הדרושה
- [ ] אתה מבין את רשומות היומן של MCP ויכול לאבחן תקלות בכלים
- [ ] אתה יודע כיצד לבדוק יומני קונטיינר לתקלות פריסה
- [ ] אתה יכול לוודא תפקידי RBAC בפורטל Azure

---

**קודם:** [07 - אימות ב-Playground](07-verify-in-playground.md) · **בית:** [Lab 02 README](../README.md) · [בית הסדנה](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש להבין כי תרגומים ממוחשבים עלולים להכיל שגיאות או אי-דיוקים. יש להסתמך על המסמך המקורי בשפתו המקורית כמקור הסמכות. למידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. אנו לא נושאיים באחריות לכל אי-הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->