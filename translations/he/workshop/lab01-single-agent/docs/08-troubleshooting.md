# מודול 8 - פתרון בעיות

מודול זה הוא מדריך עזר לכל בעיה נפוצה שנתקלת בה במהלך הסדנא. שמור אותו כמועדף - תחזור אליו בכל פעם שמשהו משתבש.

---

## 1. שגיאות הרשאה

### 1.1 הרשאת `agents/write` נדחתה

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**סיבת הבעיה:** אין לך את התפקיד `Azure AI User` ברמת ה**פרויקט**. זו השגיאה הנפוצה ביותר בסדנא.

**תיקון - שלב אחר שלב:**

1. פתח את [https://portal.azure.com](https://portal.azure.com).
2. בסרגל החיפוש העליון, הקלד את שם **פרויקט Foundry** שלך (למשל, `workshop-agents`).
3. **חשוב:** לחץ על התוצאה שמציגה סוג **"Microsoft Foundry project"**, ולא על החשבון הראשי/המשאב הראשי. אלה משאבים שונים עם תחומי RBAC שונים.
4. בניווט השמאלי בדף הפרויקט, לחץ על **Access control (IAM)**.
5. לחץ על לשונית **Role assignments** כדי לבדוק אם יש לך כבר את התפקיד:
   - חפש את שמך או כתובת האימייל שלך.
   - אם `Azure AI User` כבר מופיע → לשגיאה יש סיבה אחרת (בדוק שלב 8 למטה).
   - אם לא מופיע → המשך להוספה.
6. לחץ **+ Add** → **Add role assignment**.
7. בלשונית **Role**:
   - חפש [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - בחר אותו מהרשימה.
   - לחץ **Next**.
8. בלשונית **Members**:
   - בחר **User, group, or service principal**.
   - לחץ **+ Select members**.
   - חפש את שמך או כתובת האימייל.
   - בחר את עצמך מהרשימה.
   - לחץ **Select**.
9. לחץ **Review + assign** → שוב **Review + assign**.
10. **המתן 1-2 דקות** - שינויים ב-RBAC לוקחים זמן להתפשט.
11. נסה שוב את הפעולה שנכשלת.

> **למה Owner/Contributor לא מספיקים:** ל-Azure RBAC יש שני סוגי הרשאות - *פעולות ניהול* ו*פעולות נתונים*. Owner ו-Contributor נותנים הרשאות ניהול (יצירת משאבים, עריכת הגדרות), אבל פעולות הסוכן דורשות את פעולת ה`agents/write` **של פעולות נתונים**, שהיא רק בתוך התפקידים `Azure AI User`, `Azure AI Developer`, או `Azure AI Owner`. ראו [מסמכי Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` במהלך הפעלת משאב

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**סיבת הבעיה:** אין לך הרשאה ליצור או לשנות משאבי Azure במנוי/קבוצת המשאבים הזו.

**תיקון:**
1. בקש ממנהל המנוי להקצות לך את תפקיד **Contributor** על קבוצת המשאבים שבה נמצא פרויקט Foundry שלך.
2. כחלופה, בקש שייצור עבורך את פרויקט Foundry וייתן לך את תפקיד **Azure AI User** על הפרויקט.

### 1.3 `SubscriptionNotRegistered` עבור [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**סיבת הבעיה:** מנוי Azure לא רשם את ספק המשאבים הנדרש ל-Foundry.

**תיקון:**

1. פתח טרמינל והרץ:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. המתן לסיום ההרשמה (יכול לקחת 1-5 דקות):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   הפלט המצופה: `"Registered"`
3. נסה שוב את הפעולה.

---

## 2. שגיאות Docker (רק אם Docker מותקן)

> Docker הוא **אופציונלי** בסדנא הזו. שגיאות אלו חלות רק אם התקנת Docker Desktop וההרחבה של Foundry מנסה לבצע בניית מכולה מקומית.

### 2.1 Docker daemon אינו פועל

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**תיקון - שלב אחר שלב:**

1. **מצא את Docker Desktop** בתפריט ההתחלה שלך (Windows) או ביישומים (macOS) והפעל אותו.
2. המתן עד שחלון Docker Desktop יציג **"Docker Desktop is running"** - זה בדרך כלל לוקח 30-60 שניות.
3. חפש את סמל הלוויתן של Docker במגש המערכת (Windows) או בסרגל התפריטים (macOS). העבר מעליו כדי לוודא את הסטטוס.
4. אמת בטרמינל:
   ```powershell
   docker info
   ```
   אם זה מדפיס מידע על מערכת Docker (גרסת שרת, Storage Driver וכו'), Docker פועל.
5. **מיוחד ל-Windows:** אם Docker עדיין לא מתחיל:
   - פתח את Docker Desktop → **Settings** (סמל גלגל שיניים) → **General**.
   - ודא שסמן **Use the WSL 2 based engine** מסומן.
   - לחץ **Apply & restart**.
   - אם WSL 2 לא מותקן, הרץ `wsl --install` ב-PowerShell במצב מנהל והפעל מחדש את המחשב.
6. נסה לפרוס שוב.

### 2.2 בניית Docker נכשלה עם שגיאות תלות

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**תיקון:**
1. פתח את `requirements.txt` וודא שכל שמות החבילות מאויתים נכון.
2. ודא שהגרסה מוגדרת נכון:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. בדוק התקנה מקומית קודם:
   ```bash
   pip install -r requirements.txt
   ```
4. אם משתמשים במדד חבילות פרטי, ודא של-Docker יש גישה רשתית אליו.

### 2.3 חוסר התאמה בפלטפורמת מכולה (Apple Silicon)

אם אתה מפרוס ממחשב Mac מבוסס Apple Silicon (M1/M2/M3/M4), המכולה חייבת להיבנות עבור `linux/amd64` כי סביבת הריצה של Foundry משתמשת ב-AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> פקודת הפריסה של הרחבת Foundry מטפלת בזה אוטומטית ברוב המקרים. אם אתה רואה שגיאות הקשורות לארכיטקטורה, בצע בנייה ידנית עם הדגל `--platform` ופנה לצוות Foundry.

---

## 3. שגיאות אימות

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) נכשל בקבלת טוקן

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**סיבת הבעיה:** אף אחד ממשאבי האימות בשרשרת `DefaultAzureCredential` לא כולל טוקן תקף.

**תיקון - נסה כל שלב לפי הסדר:**

1. **התחבר מחדש דרך Azure CLI** (תיקון נפוץ ביותר):
   ```bash
   az login
   ```
   חלון דפדפן נפתח. התחבר, ואז חזור ל-VS Code.

2. **הגדר את המנוי הנכון:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   אם זה לא המנוי הנכון:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **התחבר מחדש דרך VS Code:**
   - לחץ על סמל **Accounts** (אייקון אדם) בפינה התחתונה-שמאלית של VS Code.
   - לחץ על שם החשבון שלך → **Sign Out**.
   - לחץ שוב על סמל החשבונות → **Sign in to Microsoft**.
   - סיים את תהליך ההתחברות בדפדפן.

4. **Service principal (רק בתרחישי CI/CD):**
   - הגדר את משתני הסביבה האלו ב`.env` שלך:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - ואז הפעל מחדש את תהליך הסוכן.

5. **בדוק מטמון טוקנים:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   אם זה נכשל, הטוקן שלך ב-CLI פג תוקף. הרץ שוב `az login`.

### 3.2 הטוקן עובד מקומית אבל לא בפריסה מתארחת

**סיבת הבעיה:** הסוכן המתארח משתמש בזהות מנוהלת על ידי המערכת, שהיא שונה מאות האימות האישי שלך.

**תיקון:** זה התנהגות צפויה - הזהות המנוהלת מוקצית אוטומטית במהלך הפריסה. אם הסוכן המתארח עדיין מקבל שגיאות אימות:
1. בדוק שלזהות המנוהלת של פרויקט Foundry יש גישה למשאב Azure OpenAI.
2. אמת ש-`PROJECT_ENDPOINT` בקובץ `agent.yaml` נכון.

---

## 4. שגיאות בדגם

### 4.1 פריסת דגם לא נמצאה

```
Error: Model deployment not found / The specified deployment does not exist
```

**תיקון - שלב אחר שלב:**

1. פתח את קובץ `.env` שלך ורשום את הערך של `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. פתח את סרגל הצד של **Microsoft Foundry** ב-VS Code.
3. הרחב את הפרויקט שלך → **Model Deployments**.
4. השווה את שם הפריסה שמופיע שם לערך בקובץ `.env`.
5. השם **רגיש לאותיות רישיות** - `gpt-4o` שונה מ-`GPT-4o`.
6. אם השמות לא תואמים, עדכן את קובץ `.env` לשם המדויק שמופיע בסרגל הצד.
7. לפריסה מתארחת, עדכן גם את הקובץ `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 הדגם מגיב בתוכן לא צפוי

**תיקון:**
1. בדוק את הקבוע `EXECUTIVE_AGENT_INSTRUCTIONS` בקובץ `main.py`. וודא שהוא לא נחתך או נפגם.
2. בדוק את הגדרת הטמפרטורה של הדגם (אם ניתן להגדיר) - ערכים נמוכים יותר נותנים פלטים חד-משמעיים יותר.
3. השווה בין הדגם שפורס (למשל, `gpt-4o` לעומת `gpt-4o-mini`) - לדגמים שונים יש יכולות שונות.

---

## 5. שגיאות בפריסה

### 5.1 הרשאת משיכה מ-ACR

```
Error: AcrPullUnauthorized
```

**סיבת הבעיה:** זהות מנוהלת של פרויקט Foundry אינה יכולה למשוך את תמונת המכולה מ-Azure Container Registry.

**תיקון - שלב אחר שלב:**

1. פתח את [https://portal.azure.com](https://portal.azure.com).
2. חפש **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** בסרגל החיפוש העליון.
3. לחץ על הרישום המשויך לפרויקט Foundry שלך (בדרך כלל באותה קבוצת משאבים).
4. בניווט השמאלי, לחץ על **Access control (IAM)**.
5. לחץ **+ Add** → **Add role assignment**.
6. חפש את **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** ובחר אותו. לחץ **Next**.
7. בחר **Managed identity** → לחץ **+ Select members**.
8. מצא ובחר את הזהות המנוהלת של פרויקט Foundry.
9. לחץ **Select** → **Review + assign** → **Review + assign**.

> הקצאת תפקיד זו בדרך כלל מוגדרת אוטומטית על ידי ההרחבה של Foundry. אם אתה רואה את השגיאה הזו, ייתכן שההגדרה האוטומטית נכשלה. תוכל גם לנסות לפרוס מחדש - ההרחבה עשויה לנסות שוב את ההגדרה.

### 5.2 הסוכן נכשל להתחיל לאחר פריסה

**תסמינים:** מצב המכולה נשאר "Pending" יותר מ-5 דקות או מציג "Failed".

**תיקון - שלב אחר שלב:**

1. פתח את סרגל הצד של **Microsoft Foundry** ב-VS Code.
2. לחץ על הסוכן המתארח שלך → בחר את הגרסה.
3. בפאנל הפרטים, בדוק **Container Details** → חפש מדור או קישור ל**Logs**.
4. קרא את יומני האתחול של המכולה. סיבות נפוצות:

| הודעת יומן | סיבה | תיקון |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | תלות חסרה | הוסף ל-`requirements.txt` ופרוס מחדש |
| `KeyError: 'PROJECT_ENDPOINT'` | משתנה סביבת חסר | הוסף את משתנה הסביבה ל-`agent.yaml` תחת `env:` |
| `OSError: [Errno 98] Address already in use` | התנגשות בפורט | ודא שיש ב-`agent.yaml` את `port: 8088` ורק תהליך אחד מאזין אליו |
| `ConnectionRefusedError` | הסוכן לא התחיל להאזין | בדוק ב- `main.py` - הקריאה ל-`from_agent_framework()` חייבת להתבצע באתחול |

5. תקן את הבעיה, ואז פרוס מחדש מ-[מודול 6](06-deploy-to-foundry.md).

### 5.3 הפריסה מתנתקת

**תיקון:**
1. בדוק את חיבור האינטרנט שלך - העלאת Docker יכולה להיות גדולה (>100MB לפריסה ראשונה).
2. אם אתה מאחורי פרוקסי ארגוני, ודא שהגדרות הפרוקסי של Docker Desktop מוגדרות: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. נסה שוב - בעיות רשת זמניות עלולות לגרום לכישלונות.

---

## 6. הפניה מהירה: תפקידי RBAC

| תפקיד | תחום טיפוסי | מה הוא מעניק |
|------|---------------|----------------|
| **Azure AI User** | פרויקט | פעולות נתונים: בנייה, פריסה והפעלה של סוכנים (`agents/write`, `agents/read`) |
| **Azure AI Developer** | פרויקט או חשבון | פעולות נתונים + יצירת פרויקטים |
| **Azure AI Owner** | חשבון | גישה מלאה + ניהול הקצאת תפקידים |
| **Azure AI Project Manager** | פרויקט | פעולות נתונים + יכול להקצות תפקיד Azure AI User לאחרים |
| **Contributor** | מנוי/קבוצת משאבים | פעולות ניהול (יצירת/מחיקת משאבים). **לא כולל פעולות נתונים** |
| **Owner** | מנוי/קבוצת משאבים | פעולות ניהול + הקצאת תפקידים. **לא כולל פעולות נתונים** |
| **Reader** | כל | גישה לקריאה בלבד לניהול |

> **ניקוד מרכזי:** `Owner` ו-`Contributor` אינם כוללים פעולות נתונים. תמיד יש צורך בתפקיד `Azure AI *` עבור פעולות סוכן. התפקיד המינימלי לסדנא זו הוא **Azure AI User** ברמת **הפרויקט**.

---

## 7. רשימת בדיקה להשלמת הסדנא

השתמש בזאת כאישור סופי שסיימת הכל:

| # | פריט | מודול | עבר? |
|---|------|--------|---|
| 1 | כל התלויות הותקנו ואומתו | [00](00-prerequisites.md) | |
| 2 | כלי Foundry והרחבות Foundry הותקנו | [01](01-install-foundry-toolkit.md) | |
| 3 | פרויקט Foundry נוצר (או נבחר פרויקט קיים) | [02](02-create-foundry-project.md) | |
| 4 | המודל הושק (למשל, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | תפקיד משתמש Azure AI הוקצה בטווח הפרויקט | [02](02-create-foundry-project.md) | |
| 6 | שלד פרויקט סוכן מתארח נוצר (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` הוגדר עם PROJECT_ENDPOINT ו- MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | הוראות הסוכן מותאמות ב-main.py | [04](04-configure-and-code.md) | |
| 9 | סביבה וירטואלית נוצרה ותלויות הותקנו | [04](04-configure-and-code.md) | |
| 10 | הסוכן נבדק מקומית עם F5 או טרמינל (עבר 4 בדיקות בסיס) | [05](05-test-locally.md) | |
| 11 | הושק לשירות סוכן Foundry | [06](06-deploy-to-foundry.md) | |
| 12 | מצב המכולה מציג "הופעל" או "רץ" | [06](06-deploy-to-foundry.md) | |
| 13 | אומת ב-VS Code Playground (עבר 4 בדיקות בסיס) | [07](07-verify-in-playground.md) | |
| 14 | אומת ב-Foundry Portal Playground (עבר 4 בדיקות בסיס) | [07](07-verify-in-playground.md) | |

> **ברכות!** אם כל הפריטים מסומנים, סיימת את סדנת העבודה כולה. בנית סוכן מתארח מאפס, בדקת אותו מקומית, פרסמת אותו ב-Microsoft Foundry, ואימתת אותו בייצור.

---

**הקודם:** [07 - אמת ב-Playground](07-verify-in-playground.md) · **בית:** [סדנת עבודה README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לזכור כי תרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. יש להתייחס למסמך המקורי בשפת המקור כמקור המוסמך. למידע קריטי מומלץ תרגום מקצועי על ידי אדם. אנו לא נושאים באחריות לכל אי-הבנות או פרשנויות שגויות הנובעות משימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->