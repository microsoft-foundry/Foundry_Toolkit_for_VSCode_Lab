# איך להעביר את המפגש הזה

תודה על העברת המפגש הזה!

לפני העברת הסדנה, אנא:

1. קרא את המסמך הזה וכל המשאבים הכלולים במלואם.
2. צפה בהקלטת העברת המפגש ובהדגמה מקצה לקצה של הסדנה.
3. עשה את שני המעבדות המעשיות מקצה לקצה במחשב שלך **לפחות פעם אחת** לפני האירוע.
4. אמת את פרויקט Microsoft Foundry שלך, פריסות המודלים והמכסים.
5. פנה למתחזק במקרה שמשהו לא ברור.

---

## סיכום קבצים

| משאב                        | קישור                                                                             | תיאור                                                                                       |
|-----------------------------|----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| מצגת הסדנה                  | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                   | שקופיות הצגה לסדנה זו עם הערות למרצה וסרטוני הדגמה משולבים                                 |
| הקלטת העברת הסדנה          | _תקבלו מהמתחזק_                                                                | הקלטת מבוא הסדנה והליכה על השקופיות                                                        |
| הקלטת הסדנה מקצה לקצה      | _תקבלו מהמתחזק_                                                                | הקלטת מקצה לקצה של שתי המעבדות מנקודת מבט של הלומד                                       |
| תיעוד הסדנה                | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | מאגר הקוד, קבצי README של המעבדות, מודולים צעד-אחר-צעד                                   |
| מעבדה 01 - סוכן יחיד       | [Lab 01](../workshop/lab01-single-agent/README.md)                             | מעבדה מעשית: בנייה, בדיקה ופריסה של סוכן *Explain Like I'm an Executive* מאוחסן             |
| מעבדה 02 - זרימת עבודה מרובת סוכנים | [Lab 02](../workshop/lab02-multi-agent/README.md)                             | מעבדה מעשית: בניית זרימת עבודה עם 4 סוכנים *Resume to Job Fit Evaluator*                 |
| הדגמה 1: סוכן ביצועי          | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                           | הדגמה של מעבדה 01: תרגום מונחים טכניים לסיכום ביצועי                                    |
| הדגמה 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | הדגמה של מעבדה 02: זרימת עבודה עם 4 סוכנים שמדרגת התאמת קורות חיים לעבודה ומייצרת המלצות |

> **הערה למרצים:** מצגת הסדנה וקישורי הווידאו יתווספו כאשר ההקלטות יפורסמו. עד אז, פנו למתחזק (ראו [צור קשר](#אנשי-קשר)) לקבלת הנכסים המעודכנים.

---

## התחלת עבודה

סדנה זו מלמדת מפתחים כיצד לבנות, לבדוק ולפרוס סוכני AI ל**Microsoft Foundry Agent Service** כסוכנים **מאוחסנים** כולו מתוך VS Code, באמצעות התוסף **Microsoft Foundry Toolkit**.

הסדנה מחולקת למספר חלקים הכוללים שקופיות, **2 הדגמות חיות**, ו-**2 מעבדות מעשיות**.

### זמן

#### העברה מלאה (כ-שעתיים)

| זמן           | תיאור                                                                |
|----------------|----------------------------------------------------------------------|
| 0:00 - 10:00   | מבוא: סוכנים מאוחסנים, Foundry Agent Service, והערכת הכלים          |
| 10:00 - 20:00  | הדגמה: סוכן ביצועי מקצה לקצה                                        |
| 20:00 - 60:00  | מעבדה 01 - סוכן יחיד (בנייה, בדיקה מקומית, פריסה, מגרש משחקים)     |
| 60:00 - 110:00 | מעבדה 02 - זרימת עבודה מרובת סוכנים (Resume to Job Fit Evaluator)   |
| 110:00 - 120:00| סיכום, שאלות ותשובות, ומשאבי למידה מתמשכת                         |

#### העברה מקוצרת (כ-75 דקות)

| זמן          | תיאור                                                      |
|--------------|------------------------------------------------------------|
| 0:00 - 10:00 | מבוא וסיכום                                                |
| 10:00 - 20:00| הדגמה: סוכן ביצועי                                       |
| 20:00 - 70:00| רק מעבדה 01 (הפנה את המשתתפים למעבדה 02 בקצב עצמי)     |
| 70:00 - 75:00| סיכום ושאלות ותשובות                                    |

### הכנה

| משאב                         | קישור                                                                                         | תיאור                                               |
|------------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------------|
| תיעוד הסדנה                 | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)            | תיעוד הסדנה והמקור                                  |
| הוראות מעבדה 01             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                               | מעבדה מעשית: סוכן מאוחסן יחיד                      |
| הוראות מעבדה 02             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                 | מעבדה מעשית: זרימת עבודה מרובת סוכנים             |
| רשימת דרישות קדם           | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)               | כלים, חשבונות, וגישה לאזור Azure דרושים          |
| התחלת מהירה לסוכנים מאוחסנים (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | התחלת מהירה רשמית לפריסת סוכן מאוחסן עם `azd`     |
| זמינות אזורי סוכנים מאוחסנים | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | אזורים נתמכים לסוכנים מאוחסנים (במצב תצוגה מקדימה) |

### דרישות קדם למרצים

לפני ההעברה, ודא שיש לך:

- **מנוי Azure** עם הרשאה ליצירת משאבים (Owner או Contributor על קבוצת משאבים).
- גישה לפרויקט **Microsoft Foundry** ב[אזור התומך בסוכנים מאוחסנים](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- מכסה ל**gpt-4.1** (או **gpt-4.1-mini**) בפרויקט Foundry שלך.
- כלים מותקנים הבאים:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [תוסף Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (אופציונלי)
  - Python 3.10 או מאוחר יותר

הרץ את [התחלת הסוכנים המאוחסנים עם `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) לפחות פעם אחת לפני ההעברה כדי שיהיה לך פרויקט Foundry תקין, פריסת מודל ו-Azure Container Registry מוכרזים שאליהם ניתן לפנות אם לומד יתקל בקושי.

---

## הליכה על השקופיות

המצגת עוקבת אחרי אותה זרימה כמו המעבדות. נקודות שיחה מוצעות לכל חלק:

| חלק                        | מסר מרכזי                                                                                                  |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| כותרת וסדר יום             | הצג את הסדנה כ*VS Code ל-Foundry* ללא צורך במעבר בין פורטלים.                                           |
| מדוע סוכנים מאוחסנים?     | ריצה מנוהלת, פריסה מבוססת ACR, API `/responses` תואם OpenAI, מותאם לפרויקטים ב-Foundry.                |
| תרשים ארכיטקטורה          | הסבר את [ארכיטקטורת README](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.         |
| אנטומיה של סוכן מאוחסן     | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - מה עושה כל קובץ.                              |
| הדגמה חיה: סוכן ביצועי     | עבור ל-VS Code והרץ את הדגמת  [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) מקצה לקצה (ראה [Demo 1](#הדגמה-1-סוכן-ביצועי)). |
| הדגמה חיה: Resume to Job Fit Evaluator | עבור ל-VS Code והרץ את הדגמת 4 סוכנים [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (ראה [Demo 2](#הדגמה-2-resume-to-job-fit-evaluator)). |
| סיכום מעבדה 01             | העבר ללומדים. הפנה אל [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| דפוסי סוכנים מרובים       | רציף לעומת מקביל לעומת handoff - תצוגה מקדימה לפני התחלת מעבדה 02.                                    |
| סיכום מעבדה 02             | העבר ללומדים. הפנה אל [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| סיכום ומשאבים              | קישורים ללמידה נוספת מתוך סעיף [Additional resources](#משאבים-נוספים).                            |

---

## הדגמות

שתי הדגמות חיות כלולות בהעברה. הקצה 10 דקות לכל אחת.

| הדגמה  | מעבדה | קבצים                                                        | מה להראות                                                         |
|---------|-------|---------------------------------------------------------------|------------------------------------------------------------------|
| סוכן ביצועי | מעבדה 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | סוכן מאוחסן יחיד; תרגום מונחים טכניים לסיכום ביצועי              |
| Resume to Job Fit Evaluator | מעבדה 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | תזמור 4 סוכנים; דירוג התאמת קורות חיים לעבודה ויצירת המלצה       |

### הדגמה 1: סוכן ביצועי

סוכן עצמאי ב-[`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). השתמש בזה כהדגמה של 10 דקות לפני מעבדה 01.

1. פתח את [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) ועבור על הגדרת הסוכן (הנחיית מערכת, מודל, מסגרת עבודה).
2. לחץ על `F5` כדי להפעיל את **Agent Inspector** באופן מקומי.
3. הדבק את הדוגמת ההנחיה מתוך ה-[README](../README.md#see-it-in-action) והצג את תגובת הסיכום הביצועי.
4. הצג את [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) ואת [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) להסבר על ארטיפקטי הפריסה.
5. הדגם את זרם הפריסה (Docker build, ACR push, יצירת סוכן מאוחסן) מבלי להמתין להשלמה.

### הדגמה 2: Resume to Job Fit Evaluator

זרימת עבודה עם 4 סוכנים ב-[`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). השתמש בזה כהדגמה של 10 דקות לפני מעבדה 02.

1. פתח את [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) והראה כיצד ארבעת הסוכנים מקושרים יחד בתזמור רציף.
2. לחץ על `F5` כדי להפעיל את **Agent Inspector** לזרימת העבודה המרובת סוכנים.
3. הדבק תיאור קצר של משרה וקורות חיים לדוגמא בצ'אט של ה-Inspector.
4. עבור על צינור הארבעה סוכנים: מנתח קורות חיים, מחלץ דרישות תפקיד, מדרג התאמה, וכותב המלצות.
5. הצבע כיצד הפלט של כל תת-סוכן הופך להקשר עבור הסוכן הבא, תוך הדגשת דפוס ה-handoff.
6. הצג את [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) להשוואה עם המקבילה לסוכן יחיד מהדגמה 1.

---

## טיפים להובלה

- **הגדר ציפיות מוקדם.** סוכנים מאוחסנים נמצאים בתצוגה מקדימה - ציין מראש מגבלות אזור ומכסה כדי שמשתתפים לא יופתעו באמצע המעבדה.
- **הרץ קודם את משימת דרישות הקדם.** שתי המעבדות כוללות משימת VS Code בשם `Validate prerequisites` - דאג שמשתתפים יריצו אותה לפני כל כתיבת קוד.
- **שמור את Agent Inspector גלוי.** רוב רגעי ה"אחה" מתרחשים כאשר הלומדים רואים את הנורות של סבב ה-/responses המקומי נדלקות.
- **הכנס פרויקט גיבוי.** אם לפרויקט Foundry של לומד חסרה מכסה, שתף פרויקט מוכן לשלב הפריסה במקום לחסום את החדר.
- **צרף משתתפים זוגות.** מעבדה 02 (מרובת סוכנים) קלה משמעותית כאשר הלומדים יכולים לדון בתזמור עם שותף.
- **השתמש במודולים שבמסמכים כנקודות עצירה.** כל תיקיית `docs/` במעבדה מחולקת ל-8 מודולים ממוספרים - השתמש בהם כנקודות עצירה טבעיות.
- **משוך מראש את תצורת הבסיס של Docker** במחשבי המעבדה המשותפים כדי להימנע ממגבלות קצב הרישום.

---

## פתרון תקלות במהלך ההעברה

| תסמין                                      | הדבר הראשון לנסות                                                                                   |
|--------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Agent Inspector לא מצליח להתחבר            | אמת שפורט `8088` פנוי ושהמשימה `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` רצים.            |
| הנתקע הניפוי מחבר                               | בדוק שפורט `5679` פנוי; הפעל מחדש את VS Code אם `debugpy` כבר קשור.                              |
| `azd up` נכשל בשגיאת אימות                   | הרץ `az login` ואת `azd auth login`, וודא שהשוכר הנכון נבחר.                                      |
| הפריסה תקועה בשלב ה-ACR push               | בדוק ש-Docker Desktop רץ ולמשתמש יש הרשאת `AcrPush` על הרגיסטרי.                                |
| המודל מחזיר 404 / deployment-not-found      | שם פריסת המודל ב-`agent.yaml` חייב להתאים לפריסה בפרויקט Foundry.                                |

| סוכן מאוחסן תקוע ב־`Provisioning`            | ודא שהאזור של הפרויקט [תומך בסוכנים מאוחסנים](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ושהקווטה זמינה. |
| Playground מחזיר 401                         | התחבר מחדש להרחבת Foundry מתוך סרגל הפעילויות של VS Code.                                      |

להדרכה מעמיקה יותר, לכל מעבדה מצורף מסמך `08-troubleshooting.md` משלה - הפנה את הלומדים לשם:

- מעבדה 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- מעבדה 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## התאמת המפגש הזה

אתם מוזמנים להתאים את הסדנה לקהל שלכם. וריאציות נפוצות:

- **קהל Backend:** השקיעו יותר זמן ב־`agent.yaml`, Docker ו־ACR; קצצו את הדמו ב־playground.
- **קהל מפתחי אזרחים:** השארו ב־UI של הרחבת Foundry לבניית התשתית; הפחיתו שלבים ב־CLI.
- **מפגש בודד של 60 דקות:** ספקו רק מבוא, דמו ומעבדה 01.
- **פורמט רק סדנה (ללא שקופיות):** פתחו את שני קבצי ה־README של המעבדות והשתמשו בהם כסקריפט ראשי.

אם תרחיבו את המעבדות, אנא תרמו את השינויים בחזרה באמצעות PR כדי שמדריכים אחרים יהנו.

---

## משאבים נוספים

- [תיעוד Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [סקירה על סוכנים מאוחסנים](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [התחלה מהירה: פריסת הסוכן המאוחסן הראשון שלך (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [פריסת סוכן מאוחסן (כיצד לעשות)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit עבור VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## אנשי קשר

אם יש לכם שאלות בנוגע למתן מפגש זה, אנא פתחו נושא ב־[מאגר הסדנה](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) ותגו את האחראי.

| תפקיד                | שם             | GitHub                                                 |
|---------------------|----------------|---------------------------------------------------------|
| אחראי / איש קשר    | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->