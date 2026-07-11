# מודול 8 - פתרון תקלות

מודול זה עוסק בשגיאות נפוצות, תיקונים ואסטרטגיות ניפוי שגיאות ספציפיות לזרימת עבודה מרובת סוכנים.

## בעיות ביציאות הסוכן

### GapAnalyzer אומר "עדיין אין לי את דוח ההתאמה"

**תסמין:** תגובת GapAnalyzer מבקשת ממך להדביק דוח התאמה הכולל "כישורים חסרים" ו"פערי הסמכה". זה קורה גם כאשר שלחת גם קורות חיים וגם תיאור משרה.

**סיבה:** הטקסט של JD לא הועבר הלאה לסוכן JD. עם `context_mode="last_agent"`, `resume_executor` הוא המבצע היחיד שרואה את ההודעה המקורית של המשתמש. אם `RESUME_PARSER_INSTRUCTIONS` אינו כולל את טקסט JD ביציאה שלו, לסוכן JD אין JD לפרש, MatchingAgent לא יכול לחשב ציון התאמה, ו-GapAnalyzer מקבל קלט חסר משמעות.

**אבחנה:**

ביומני השרת, חפש את הטווח של MatchingAgent. אם הוא מכיל:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
העברה-ישירה חסרה או שבורה.

**תיקון:** ודא ש־`RESUME_PARSER_INSTRUCTIONS` בקובץ `main.py` מכיל קטע `[JOB DESCRIPTION PASS-THROUGH]` וכלל:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
כמו כן ודא ש־`JOB_DESCRIPTION_INSTRUCTIONS` כולל כלל העברה `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
אם אחד מחסימות ההוראות הוא תבנית מהאשף, החלף את זה בגרסה המלאה מ־[`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent מחזיר "לא ניתן לחשב ציון התאמה - לא סופק JD"

זוהי אותה סיבה שורשית כמו למעלה. MatchingAgent קיבל את פלט סוכן JD אך קטע `[PARSED RESUME PASS-THROUGH]` היה חסר או ריק, ולכן לא יכול היה להשוות בין שני הפרופילים. ודא:
1. `JOB_DESCRIPTION_INSTRUCTIONS` כולל את כלל ההעברה: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` מורה לסוכן לחפש קטעים `[JD REQUIREMENTS]` ו־`[PARSED RESUME PASS-THROUGH]`.

החלף את שתי חסימות ההוראות בגרסאות המלאות מ־[`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### התגובה מופיעה פעמיים

**תסמין:** הפלט של GapAnalyzer (או הפלט המלא של הצנרת) מופיע פעמיים בתגובת Agent Inspector.

**סיבה:** `WorkflowBuilder` משתמש בסמנטיקה של OR עבור צמתים נכנסים - מבצע המשכי ירוץ ברגע ש**אחד** מהקודמים מסתיים. אם ל־`matching_executor` יש שני קצוות נכנסים (אחד מ־`resume_executor` ואחד מ־`jd_executor`), הוא ירוץ פעמיים: פעם אחת עם סיום ResumeParser ופעם שנייה עם סיום סוכן JD. GapAnalyzer אז ירוץ פעמיים גם כן.

**תיקון:** וודא שגראף `WorkflowBuilder` הוא צנרת רציפה לחלוטין ללא צמתים עם מספר כניסות:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # לא מ- resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

אם יש לך שורת `.add_edge(resume_executor, matching_executor)` מיותרת, הסר אותה. ההעברה `[PARSED RESUME PASS-THROUGH]` בפלט סוכן JD כבר מעניקה ל־MatchingAgent גישה לקורות החיים.

---

## בעיות סביבה וקונפיגורציה

### ערכי `.env` חסרים או שגויים

קובץ `.env` חייב להיות בתיקיית `PersonalCareerCopilot/` (באותו רמה עם `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

תוכן `.env` צפוי:

**נתיב A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**נתיב B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> שני הנתיבים משתמשים ב־`FOUNDRY_PROJECT_ENDPOINT`. הערך שונה: ענן משתמש בנקודת קצה Foundry עם `https://`; מקומי משתמש ב־`http://localhost:5273/v1`. הרץ `foundry model list` כדי לאשר את כינוי הדגם המדויק עבור נתיב B.

> **כיצד למצוא את `FOUNDRY_PROJECT_ENDPOINT`:** 
- פתח את סרגל הכלים Foundry Toolkit ב־VS Code → לחץ ימני על הפרויקט שלך → **Copy Project Endpoint**. 
- או עבור ל־[Azure Portal](https://portal.azure.com) → פרויקט Foundry שלך → **Overview** → **Project endpoint**.

> **כיצד למצוא את `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** בסרגל Foundry Toolkit הרחב את הפרויקט שלך → **Models** → מצא את שם הדגם שפורש (למשל, `gpt-4.1-mini`).

### עדיפות משתני סביבה

`main.py` משתמש ב־`load_dotenv(override=True)`, כלומר:

| עדיפות | מקור | מנצח כשהשניים מוגדרים? |
|----------|--------|------------------------|
| 1 (הגבוהה ביותר) | קובץ `.env` | כן |
| 2 | משתנה סביבה של shell/מכולה | משמש כאשר אותו מפתח אינו קיים ב־`.env` |

בפיתוח מקומי, זה הופך את `.env` למקור האמת (עריכת `.env` משפיעה מיידית על הריצות). בפריסה מתארחת, Foundry מזריקה משתני סביבה ברמת המכולה; מאחר ש־`.env` אינו חלק מהתמונה המתפרסת עבור תצורת המעבדה הזו, ערכי המכולה המוזרקים משמשים.

---

## תאימות גרסאות

### מטריצת גרסאות חבילות

זרימת העבודה מרובת הסוכנים דורשת גרסאות חבילות ספציפיות. גרסאות שאינן תואמות גורמות לשגיאות בזמן ריצה.

| חבילה | גרסה דרושה | פקודת בדיקה |
|---------|-----------------|---------------|
| `agent-framework-foundry` | העדכנית ביותר | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | העדכנית ביותר | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | העדכנית ביותר | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### שגיאות גרסה נפוצות

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# תיקון: התקן מחדש את agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# תיקון: שדרג את חבילת mcp
pip install mcp --upgrade
```

### אמת את כל הגרסאות בבת אחת

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

פלט צפוי:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## בעיות בפריסה

### המכולה נכשלת בהפעלה לאחר הפריסה

1. **בדוק יומני מכולה:**
   - פתח את סרגל הכלים Foundry Toolkit → הרחב **Hosted Agents (Preview)** → לחץ על הסוכן שלך → הרחב את הגרסה → **Container Details** → **Logs**.
   - חפש עקבות שגיאות פייתון או שגיאות מודול חסר.

2. **כשלי הפעלה נפוצים במכולה:**

   | שגיאה ביומנים | סיבה | תיקון |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | חסר חבילה ב־`requirements.txt` | הוסף את החבילה, פרוס מחדש |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | משתני סביבה ב־`agent.yaml` או `.env` לא מוגדרים | עדכן ב־`agent.yaml` → קטע `environment_variables` (מתארח) או `.env` (מקומי) |
   | `azure.identity.CredentialUnavailableError` | זיהוי מנוהל לא מוגדר | Foundry מגדיר זאת אוטומטית - ודא שאתה מפרוס דרך התוסף |
   | `OSError: port 8088 already in use` | Dockerfile חושף פורט שגוי או קונפליקט פורטים | אמת ש־`EXPOSE 8088` ב־Dockerfile ו־`CMD ["python", "main.py"]` |
   | יציאת מכולה עם קוד 1 | חריגה לא מטופלת ב־`main()` | בדוק מקומית תחילה ([מודול 5](05-test-locally.md)) כדי לתפוס שגיאות לפני הפריסה |

3. **פרוס מחדש לאחר תיקון:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → בחר את אותו סוכן → פרוס גרסה חדשה.

### הפריסה לוקחת יותר מדי זמן

מכולות של סוכנים מרובים לוקחות זמן הארכה להפעלה מאחר שהן יוצרות 4 מופעי סוכן בעת ההפעלה. זמני הפעלה רגילים:

| שלב | משך צפוי |
|-------|------------------|
| בניית תמונת מכולה | 1-3 דקות |
| דחיפת תמונה ל-ACR | 30-60 שניות |
| הפעלת מכולה (סוכן יחיד) | 15-30 שניות |
| הפעלת מכולה (מספר סוכנים) | 30-120 שניות |
| סוכן זמין ב-Playground | 1-2 דקות לאחר "התחלה" |

> אם מצב "Pending" נמשך מעבר ל-5 דקות, בדוק יומני מכולה לשגיאות.

---

## בעיות הרשאות ו-RBAC

### `403 Forbidden` או `AuthorizationFailed`

עליך להיות עם תפקיד **[Foundry User](https://aka.ms/foundry-ext-project-role)** בפרויקט Foundry שלך (שנקרא בעבר **Azure AI User** - מזהה התפקיד לא השתנה):

1. עבור ל־[Azure Portal](https://portal.azure.com) → המשאב **project** של Foundry שלך.
2. לחץ על **Access control (IAM)** → **Role assignments**.
3. חפש את שמך → אמת שכהוגדר **Foundry User** (או התווית הישנה **Azure AI User**).
4. אם חסר: **הוסף** → **Add role assignment** → חפש **Foundry User** → הקצה לחשבונך.

עיין בתיעוד [RBAC ל-Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) לפרטים.

### דגם פרוס אינו נגיש

אם הסוכן מחזיר שגיאות הקשורות לדגם:

1. אמת שהדגם פרוס: סרגל Foundry → הרחב את הפרויקט → **Models** → בדוק את `gpt-4.1-mini` (או מודל אחר) עם מצב **Succeeded**.
2. אמת ששמו של הפריסה תואם: השווה את `AZURE_AI_MODEL_DEPLOYMENT_NAME` ב־`.env` (או `agent.yaml`) לשם הפריסה בפועל בסרגל הכלים.
3. אם הפריסה פגה (שכבת חינם): פרוס מחדש מ-[Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## בעיות Foundry Local (נתיב B)

### שירות Foundry Local לא רץ

```powershell
# בדוק מצב
foundry local status

# הפעל את השירות אם הוא נעצר
foundry local start
```

| תסמין | סיבה | תיקון |
|---------|-------|-----|
| בדיקת בריאות מחזירה `503` | השירות לא הופעל | הפעל `foundry local start` או לחץ על **Start** בסרגל Foundry Toolkit |
| בדיקת בריאות נגמרת בזמן | הדגם עדיין נטען | המתן 30–60 שניות לאחר ההפעלה; דגמים גדולים יותר לוקחים יותר זמן |
| `StatusCode: 404` ב-/v1/health | פורט שגוי | ברירת המחדל היא `5273`. בדוק עם `foundry local status` את הפורט הנכון |
| משאבים לא מספיקים | Foundry Local זקוק לכ-4 GB RAM פנויים | סגור יישומים אחרים |
| כשלון בהורדת דגם | מקום אחסון נמוך בדיסק | הדגמים הם בגודל 2–8 ג"ב. פנה מקום ואז הרץ `foundry model pull <name>` |

### חוסר התאמה בשם הדגם

```powershell
# רשום דגמים שהורדו ואת הכינויים המדויקים שלהם
foundry model list
```

הגדר את `AZURE_AI_MODEL_DEPLOYMENT_NAME` ב־`.env` לכינוי המדויק שמופיע (למשל, `phi-4-mini` ולא `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` בהרצה מקומית (נתיב B)

`main.py` של המעבדה משתמש ב־`os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local דורש שמשתנה זה יפנה אל השירות המקומי - **לא** ל־`AZURE_AI_PROJECT_ENDPOINT`. ודא שקובץ `.env` שלך מכיל:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### כלי MCP עדיין מבצע קריאת רשת יוצאת (נתיב B)

זה צפוי. הכלי `search_microsoft_learn_for_plan` מושך משאבי למידה מ־`https://learn.microsoft.com/api/mcp`. **רק שאילתת שם הכישור** נעשית ברשת - קורות החיים וטקסט תיאור המשרה מעובדים באופן מלא במכשיר שלך ולעולם לא משודרים. אם נדרשת הפעלה במצב לא מקוון לגמרי, הוסף בלוק `try/except` בכלי שיחזיר כתובת URL סטטית של `learn.microsoft.com` כשנקודת הקצה אינה נגישה.

---

## קבלת עזרה

אם אתה תקוע לאחר שניסית את התיקונים שלמעלה:

1. **בדוק את יומני השרת** - רוב השגיאות מייצרות עקבות סטאק פייתון בטורמינל. קרא את כל עקבת השגיאה.
2. **חפש את הודעת השגיאה** - העתק את טקסט השגיאה וחפש ב־[Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **פתח נושא** - פתור נושא ב־[מאגר הסדנה](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) עם:
   - הודעת השגיאה או צילום מסך
   - גרסאות החבילות שלך (`pip list | Select-String "agent-framework"`)
   - גרסת הפייתון שלך (`python --version`)
   - האם הבעיה מקומית או לאחר פריסה

---

### נקודת בדיקה

- [ ] אתה יודע כיצד לבדוק ולתקן בעיות קונפיגורציית `.env`
- [ ] אתה יכול לוודא שגרסאות החבילות מתאימות למטריצה הדרושה
- [ ] אתה יודע כיצד לבדוק יומני מכולה לכשלי פריסה
- [ ] אתה יכול לוודא תפקידי RBAC בפורטל Azure

---

**קודם:** [07 - Verify in Playground](07-verify-in-playground.md) · **הבא:** [09 - Summary →](09-summary.md) · **בית:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->