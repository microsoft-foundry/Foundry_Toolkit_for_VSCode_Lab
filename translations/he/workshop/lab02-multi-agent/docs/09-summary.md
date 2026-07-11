# מודול 9 - סיכום והשלבים הבאים

⏱️ ~5 דקות

**מברוכים!** בניתם, בדקתם, ואם במסלול א', פרסמתם תהליך עבודה רב-סוכנים באמצעות Microsoft Foundry ו-Foundry Toolkit עבור VS Code.

---

## מה שבניתם

**Resume → Job Fit Evaluator** - תהליך עבודה רב-סוכנים מאוחסן ש:
- מקבל קורות חיים + תיאור משרה דרך HTTP (`POST /responses`)
- מריץ ארבעה סוכנים ייעודיים בצינור רציף - כל סוכן מעביר את הנתונים שהבא אחריו צריך
- מחזיר ציון התאמה (0–100 עם פירוט), רשימת פערי מיומנויות והסמכות, ומפת דרכים מותאמת ללמידה עם קישורים אמיתיים למיקרוסופט Learn לכל פער
- קורא לשרת Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) כדי להביא משאבי למידה רשמיים לכל פער מיומנות מזוהה
- רץ כסוכן מאוחסן מכולתי יחיד ב-Microsoft Foundry Agent Service

---

## מושגים מרכזיים שלמדתם

| מושג | מה שתרגלתם |
|---------|-------------------|
| **תזמור רב-סוכנים** | צינור רציף של `WorkflowBuilder` עם `add_edge()` |
| **התמחות סוכן** | ארבעה סוכנים ממוקדים מתעלים על סוכן כללי אחד |
| **תבנית ניתוב תוכן** | ResumeParser משמש גם כאמצעי ניתוב - משמר את טקסט ה-JD במדור `[JOB DESCRIPTION PASS-THROUGH]` כדי שסוכנים בדרג יורד יוכלו לגשת אליו (נדרש כי `context_mode="last_agent"` אומר שרק ה-start_executor רואה את ההודעה הגולמית של המשתמש) |
| **תבנית העברת תוכן** | סוכן JD מעביר את `[PARSED RESUME PASS-THROUGH]` קדימה כך ש-MatchingAgent מקבל את שני הפרופילים; מונע את טריגר OR כהכפלה בגרפים עם כניסות מרובות |
| **שילוב כלי MCP** | `@tool` + `streamable_http_client` שקורא לשרת MCP חיצוני |
| **מחזור חיי סוכן מאוחסן** | Scaffold → קונפיגורציה → בדיקה מקומית → פריסה → אימות בענן |
| **`context_mode="last_agent"`** | כל מבצע רואה רק את הפלט הישיר של קודמו |
| **תהליך עבודה ב-Foundry Toolkit** | אשף Scaffold, Agent Inspector, Workflow Visualizer, פריסה בלחיצה אחת |

---

## מה שסיימתם

<details open>
<summary><strong>🅰️ מסלול א' - Foundry במנוי</strong></summary>

- [x] אימתתם את ההתקנה של מעבדה 01: פרויקט, מודל, ו-RBAC עדיין פעילים
- [x] בניתם פרויקט רב-סוכנים באמצעות תבנית Workflows
- [x] כתבתם ארבעה סטים של הוראות סוכן (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] שילבתם את כלי Microsoft Learn MCP עם `streamable_http_client`
- [x] חיברתם את גרף תהליך העבודה עם `WorkflowBuilder` (צינור רציף עם העברת תוכן)
- [x] בדקתם מקומית עם 3 בדיקות בסיס (Agent Inspector) - ציון התאמה, כרטיסי פערים, וכתובות URL של MCP
- [x] פרסתם לשירות סוכני Foundry (מכולה, זהות מנוהלת)
- [x] אימתתם בפורטל ענן - עקביות מבנית מול התוצאות המקומיות

</details>

<details open>
<summary><strong>🅱️ מסלול ב' - Foundry מקומי</strong></summary>

- [x] אימתתם את ההתקנה של מעבדה 01: Foundry מקומי רץ עם מודל מקומי
- [x] בניתם פרויקט רב-סוכנים באמצעות תבנית Workflows
- [x] כתבתם ארבעה סטים של הוראות סוכן וחיברתם את גרף תהליך העבודה
- [x] שילבתם את כלי Microsoft Learn MCP
- [x] בדקתם מקומית עם 3 בדיקות בסיס
- [x] אימתתם התנהגות רב-סוכנים ללא צורך במשאבי ענן

</details>

---

## השלבים הבאים

### המשיכו ללמוד

| משאב | תיאור |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | מסמכי API עבור `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | חיבור סוכנים לשרתים אחרים של MCP (Bing, GitHub, מותאם אישית) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | העמקת הסוכנים עם מסמכים, מאגרי וקטורים, או חיפוש ב-Bing |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | מדידת איכות הסוכן בקנה מידה עם מעריכים אוטומטיים |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | תיעוד מלא לפלטפורמה |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | הערות שחרור של התוסף ורשימת שינויים |

### רעיונות להרחבת תהליך העבודה הזה

- **הוספת סוכן חמישי** - מאמן לראיונות שיוצר שאלות ראיון סבירות בהתבסס על דוח הפערים
- **הוספת כלי עיגון Bing** - לתת לסוכן JD לחפש משרות דומות להעשיר דרישות
- **קישור למסד נתונים לקורות חיים** - למשוך פרופילים דרך `@tool` מותאם אישית
- **נסו מודלים שונים** - השוו בין איכות ופיגור יציאה של `gpt-4.1` מול `gpt-4.1-mini`
- **הערכה עם Foundry** - השתמשו בתכונת ההערכות כדי לדרג דוחות התאמה מול מערך זהב

### למשתמשי מסלול ב': שדרגו לפריסת ענן

כאשר תהיו מוכנים לפרוס לענן:
1. השיגו מנוי Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. השלימו את [מעבדה 01, מודול 01](../../lab01-single-agent/docs/01-setup.md) (יצירת פרויקט, פריסת מודל, הקצאת RBAC)
3. עדכנו את `.env` עם נקודת הקצה של פרויקט Foundry ושם פריסת המודל
4. המשיכו מ-[מודול 06 - פריסה ל-Foundry](06-deploy-to-foundry.md)

---

## ניקוי משאבים (אופציונלי)

אם ברצונכם להסיר את משאבי Azure שנוצרו במהלך הסדנה הזאת:

### אפשרות 1: מחיקת קבוצת המשאבים (מסיר הכל)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### אפשרות 2: מחיקת הסוכן המאוחסן בלבד

1. פתחו [ai.azure.com](https://ai.azure.com) → הפרויקט שלכם → **בנה** → **סוכנים**.
2. מצאו את **PersonalCareerCopilot** → לחצו על **מחיקה**.

### אפשרות 3: מחיקת פריסת המודל

1. בסרגל הצד של Foundry, הרחיבו את הפרויקט שלכם → **מודלים**.
2. לחצו ימני על פריסת המודל → **מחיקה**.

> **הערת עלות:** סוכנים מאוחסנים גורמים לעלות רק בעת הרצה. אם תעצור או תמחק את הסוכן, אין חיוב מתמשך. לפריסת המודל עשוי לחול חיוב קטן על קיבולת שמורה - מחקו אותו אם סיימתם.

---

**קודם:** [08 - פתרון תקלות](08-troubleshooting.md) · **בית:** [Lab 02 README](../README.md) · [דף הבית של הסדנה](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->