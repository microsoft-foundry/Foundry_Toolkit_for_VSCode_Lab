# מודול 8 - פתרון בעיות

מודול זה הוא מדריך לפתרון בעיות נפוצות. ערוך סימנייה וחזור אליו כאשר משהו משתבש.

---

## 1. שגיאות הרשאה

### 1.1 `agents/write` הרשאה נדחתה

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**סיבת השורש:** חסר תפקיד `Azure AI User` ברמת **הפרויקט**. זו השגיאה מספר 1 בסדנה.

**תיקון:**
1. פתח את [portal.azure.com](https://portal.azure.com).
2. חפש את שם **הפרויקט** שלך ב-Foundry → לחץ על התוצאה מסוג **"Microsoft Foundry project"** (לא חשבון הורה).
3. **Access control (IAM)** → **+ Add** → **Add role assignment**.
4. תפקיד: **Azure AI User** → הבא.
5. חברים: בחר את עצמך → סקור + הקצה → סקור + הקצה.
6. **המתן 1–2 דקות** → נסה שוב.

> **מדוע Owner/Contributor לא מספיק:** תפקידים אלה מעניקים רק פעולות *ניהול*. פעולות סוכן דורשות `agents/write` *פעולת נתונים*, שנמצאת רק ב-`Azure AI User`, `Azure AI Developer`, או `Azure AI Owner`. ראה [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` במהלך הפריסה

**תיקון:** בקש מהמנהל שלך להקצות **Contributor** על קבוצת המשאבים, או שיבצע עבורך את יצירת הפרויקט וייתן לך **Azure AI User** עליו.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# המתן עד: "נרשם"
```

---

## 2. שגיאות Docker

> Docker הוא **אופציונלי**. אלה חלים רק אם Docker Desktop מותקן וההרחבה מנסה קומפילציה מקומית.

### 2.1 Docker daemon לא רץ

**תיקון:** הפעל את Docker Desktop → המתן לסטטוס "running" → אמת עם `docker info` → נסה שוב.

### 2.2 בנייה נכשלה עם שגיאות תלות

**תיקון:** אמת את האיות בקובץ `requirements.txt`, בדוק מקומית ראשונה: `pip install -r requirements.txt`.

### 2.3 אי התאמת פלטפורמה (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. שגיאות אימות

### 3.1 `DefaultAzureCredential` נכשל

**תיקון (נסה לפי הסדר):**
1. `az login` (הרשמה מחדש)
2. `az account set --subscription "<id>"` (מנוי נכון)
3. VS Code → חשבונות → התנתק → התחבר שוב
4. אמת: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 הטוקן עובד מקומית אך לא באירוח

**צפוי:** סוכנים מתארחים משתמשים בזהות מנוהלת על ידי המערכת, לא באישורך. אם הסוכן המתארח מקבל שגיאות אימות:
- אמת ש-`AZURE_AI_PROJECT_ENDPOINT` ב-`agent.yaml` נכון
- בדוק שלזהות המנוהלת של הפרויקט יש גישה למודל

---

## 4. שגיאות מודל

### 4.1 פריסת מודל לא נמצאה

**תיקון:** השם רגיש לאותיות גדולות/קטנות. השווה `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` עם השם המדויק בפאנל הצידי של Foundry → Models.

### 4.2 פלט מודל לא צפוי

**תיקון:** סקור את `AGENT_INSTRUCTIONS` ב-`main.py` (האם לא קוצץ?). נסה מודל אחר (`gpt-4.1` לעומת `gpt-4.1-mini`).

---

## 5. שגיאות פריסה

### 5.1 הרשאה למשיכת ACR נדחתה

**תיקון:** פורטל Azure → Container Registry → Access control (IAM) → הוסף תפקיד **AcrPull** לזהות המנוהלת של פרויקט Foundry.

### 5.2 הסוכן נכשל להתחיל (נשאר ב-"Pending" או "Failed")

בדוק יומני המכולה בפאנל הצידי. סיבות נפוצות:

| הודעת לוג | תיקון |
|-------------|-----|
| `ModuleNotFoundError` | הוסף חבילה חסרה ל-`requirements.txt`, פרוס מחדש |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | הוסף משתנה סביבה ל-`agent.yaml` תחת `environment_variables` |
| `Address already in use` | ודא שתהליך אחד בלבד קשור ל-port 8088 |

### 5.3 פריסת המודל נדחתה

**תיקון:** בדוק חיבור לאינטרנט. פריסה ראשונה דוחפת >100MB. מאחורי פרוקסי? הגדר הגדרות פרוקסי ב-Docker Desktop.

---

## 6. מסלול B - Foundry Local

### 6.1 Foundry Local לא מתחיל

| בעיה | תיקון |
|-------|-----|
| `foundry: command not found` | התקן מחדש: `winget install Microsoft.FoundryLocal` |
| משאבים לא מספקים | Foundry Local דורש כ-4GB RAM פנוי. סגור תוכניות אחרות. |
| הורדת המודל נכשלה | בדוק מקום בדיסק (המודלים הם 2–8 GB). נסה שוב: `foundry local models pull <name>` |

### 6.2 שגיאות מודל ב-Foundry Local

| בעיה | תיקון |
|-------|-----|
| תגובות איטיות | צפוי - מודלים מקומיים רצים על CPU אלא אם יש לך GPU. סבלנות. |
| פלט באיכות ירודה | נסה מודל גדול יותר אם החומרה שלך מאפשרת. `phi-4-mini` הוא איזון טוב. |
| חיבור נדחה | אמת ש-Foundry Local רץ: `foundry local status`. הפעל מחדש במידת הצורך. |

---

## 7. הפניה מהירה: תפקידי RBAC

| תפקיד | היקף | מעניק |
|------|-------|--------|
| **Azure AI User** | פרויקט | פעולות נתונים: `agents/write`, `agents/read` |
| **Azure AI Developer** | פרויקט/חשבון | פעולות נתונים + יצירת פרויקט |
| **Azure AI Owner** | חשבון | גישה מלאה + ניהול תפקידים |
| **Contributor** | מנוי/קבוצת משאבים | פעולות ניהול בלבד (**ללא** פעולות נתונים) |
| **Owner** | מנוי/קבוצת משאבים | ניהול + הקצאת תפקידים (**ללא** פעולות נתונים) |

---

## 8. רשימת בדיקה להשלמת הסדנה

| # | פריט | מודול |
|---|------|--------|
| 1 | דרישות מקדימות מותקנות ומאומתות | [00](00-prerequisites.md) |
| 2 | הרחבת Foundry Toolkit מותקנת, פרויקט מחובר (או מסלול B מוגדר) | [01](01-setup.md) |
| 3 | סוכן מתארח נוצר | [02](02-create-hosted-agent.md) |
| 4 | `.env` מוגדר, הוראות כתובות, תלותות מותקנות | [03](03-configure-and-code.md) |
| 5 | סוכן נבדק מקומית - 3 תרחישים פונקציונליים עוברים | [04](04-test-locally.md) |
| 6 | פרוס ל-Foundry (רק מסלול A) | [05](05-deploy-to-foundry.md) |
| 7 | מבחני קצה/בטיחות עוברים בענן (רק מסלול A) | [06](06-verify-in-playground.md) |
| 8 | סיכום סוקרן, צעדים הבאים זוהו | [07](07-summary.md) |

---

**הקודם:** [07 - סיכום](07-summary.md) · **בית:** [README של הסדנה](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:
מסמך זה תורגם באמצעות שירות תרגום אוטומטי [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון שתרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להחשיב את המסמך המקורי בשפתו הטבעית כמקור הסמכות. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אדם. אנו לא אחראים לכל אי-הבנה או פירוש שגוי הנובע מהשימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->