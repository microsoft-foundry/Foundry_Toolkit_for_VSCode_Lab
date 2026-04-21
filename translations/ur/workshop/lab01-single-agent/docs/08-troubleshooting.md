# ماڈیول 8 - مسائل کا حل

یہ ماڈیول ورکشاپ کے دوران سامنے آنے والے ہر عام مسئلے کے لیے ایک حوالہ گائیڈ ہے۔ اسے بک مارک کریں - جب بھی کچھ غلط ہوگا آپ اس کی طرف واپس آئیں گے۔

---

## 1. اجازت کے مسائل

### 1.1 `agents/write` کی اجازت مسترد

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**بنیادی وجہ:** آپ کے پاس **پروجیکٹ** سطح پر `Azure AI User` کا رول نہیں ہے۔ یہ ورکشاپ میں سب سے عام غلطی ہے۔

**حل - قدم بہ قدم:**

1. [https://portal.azure.com](https://portal.azure.com) کھولیں۔
2. اوپر سرچ بار میں اپنے **Foundry پروجیکٹ** کا نام ٹائپ کریں (مثلاً، `workshop-agents`)۔
3. **اہم:** اس نتیجے پر کلک کریں جو قسم **"Microsoft Foundry project"** دکھاتا ہے، والدین اکاؤنٹ/ہب ریسورس پر نہیں۔ یہ مختلف ریسورسز ہیں جن کے مختلف RBAC دائرہ کار ہیں۔
4. پروجیکٹ کے صفحے کی بائیں نیویگیشن میں **Access control (IAM)** پر کلک کریں۔
5. چیک کرنے کے لیے **Role assignments** ٹیب پر کلک کریں کہ کیا آپ کے پاس پہلے سے یہ رول ہے:
   - اپنا نام یا ای میل تلاش کریں۔
   - اگر `Azure AI User` پہلے سے لسٹ میں ہے → تو غلطی کی کوئی اور وجہ ہو سکتی ہے (نیچے مرحلہ 8 دیکھیں)۔
   - اگر لسٹ میں نہیں ہے → تو اسے شامل کریں۔
6. **+ Add** → **Add role assignment** پر کلک کریں۔
7. **Role** ٹیب میں:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) تلاش کریں۔
   - نتائج میں سے اسے منتخب کریں۔
   - **Next** پر کلک کریں۔
8. **Members** ٹیب میں:
   - **User, group, or service principal** منتخب کریں۔
   - **+ Select members** پر کلک کریں۔
   - اپنا نام یا ای میل تلاش کریں۔
   - خود کو نتائج میں سے منتخب کریں۔
   - **Select** پر کلک کریں۔
9. **Review + assign** پر کلک کریں → پھر سے **Review + assign** کریں۔
10. **1-2 منٹ انتظار کریں** - RBAC تبدیلیوں کو پھیلنے میں وقت لگتا ہے۔
11. وہ آپریشن دوبارہ آزما کر دیکھیں جو فیل ہوا تھا۔

> **کیوں Owner/Contributor کافی نہیں ہے:** Azure RBAC میں دو قسم کی اجازتیں ہوتی ہیں - *management actions* اور *data actions*۔ Owner اور Contributor مینجمنٹ ایکشنز (ریسورسز بنانا، سیٹنگز ایڈٹ کرنا) دیتے ہیں، لیکن ایجنٹ آپریشنز کو `agents/write` **data action** کی ضرورت ہوتی ہے، جو صرف `Azure AI User`, `Azure AI Developer`, یا `Azure AI Owner` رولز میں شامل ہے۔ دیکھیں [Foundry RBAC ڈاکومنٹیشن](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)۔

### 1.2 `AuthorizationFailed` ریسورس پروویژنگ کے دوران

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**بنیادی وجہ:** آپ کو اس سبسکرپشن/ریسورس گروپ میں Azure ریسورسز بنانے یا ترمیم کرنے کی اجازت نہیں ہے۔

**حل:**
1. اپنے سبسکرپشن ایڈمنسٹریٹر سے کہیں کہ وہ آپ کو اس ریسورس گروپ پر **Contributor** رول تفویض کرے جہاں آپ کا Foundry پروجیکٹ ہے۔
2. متبادل کے طور پر، انہیں کہیں کہ وہ آپ کے لیے Foundry پروجیکٹ بنائیں اور آپ کو پروجیکٹ پر **Azure AI User** دیں۔

### 1.3 `SubscriptionNotRegistered` for [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**بنیادی وجہ:** Azure سبسکرپشن نے Foundry کے لیے مطلوبہ ریسورس پرووائیڈر رجسٹر نہیں کیا ہے۔

**حل:**

1. ٹرمینل کھولیں اور چلائیں:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. رجسٹریشن مکمل ہونے کا انتظار کریں (1-5 منٹ لگ سکتے ہیں):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   متوقع آؤٹ پٹ: `"Registered"`
3. آپریشن دوبارہ آزمانے کی کوشش کریں۔

---

## 2. ڈاکر کی غلطیاں (صرف اگر ڈاکر انسٹال ہو)

> اس ورکشاپ کے لیے ڈاکر **اختیاری** ہے۔ یہ غلطیاں صرف اس صورت میں لگتی ہیں جب آپ کے پاس Docker Desktop انسٹال ہو اور Foundry ایکسٹینشن کسی مقامی کنٹینر بلڈ کی کوشش کرے۔

### 2.1 Docker daemon چل نہیں رہا

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**حل - قدم بہ قدم:**

1. Start مینو (Windows) یا Applications (macOS) میں **Docker Desktop** تلاش کریں اور اسے کھولیں۔
2. انتظار کریں جب تک Docker Desktop کی ونڈو پر **"Docker Desktop is running"** ظاہر نہ ہو جائے - عام طور پر 30-60 سیکنڈ لگتے ہیں۔
3. اپنے سسٹم ٹرے (Windows) یا مینو بار (macOS) میں Docker وہیل آئیکن تلاش کریں۔ اس پر ہوور کریں تاکہ اس کی حالت کی تصدیق ہو سکے۔
4. ٹرمینل میں تصدیق کریں:
   ```powershell
   docker info
   ```
   اگر یہ Docker سسٹم کی معلومات (سرور ورژن، اسٹوریج ڈرائیور، وغیرہ) دکھاتا ہے، تو Docker چل رہا ہے۔
5. **Windows مخصوص:** اگر Docker اب بھی شروع نہیں ہوتا:
   - Docker Desktop کھولیں → **Settings** (گئر آئیکن) → **General**۔
   - یقینی بنائیں کہ **Use the WSL 2 based engine** چیک ہے۔
   - **Apply & restart** پر کلک کریں۔
   - اگر WSL 2 انسٹال نہیں ہے، تو ایک ایلیویٹڈ PowerShell میں `wsl --install` چلائیں اور کمپیوٹر ری اسٹارٹ کریں۔
6. تعیناتی دوبارہ آزمائیں۔

### 2.2 Docker بلڈ انحصاری کی غلطیوں کے ساتھ فیل ہو رہا ہے

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**حل:**
1. `requirements.txt` کھولیں اور تمام پیکج کے ناموں کی درست ہجے کی تصدیق کریں۔
2. ورژن پننگ درست ہے یہ یقینی بنائیں:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. پہلے مقامی طور پر انسٹالیشن آزمائیں:
   ```bash
   pip install -r requirements.txt
   ```
4. اگر پرائیویٹ پیکج انڈیکس استعمال کر رہے ہیں، تو یقینی بنائیں کہ Docker کو اس کی نیٹ ورک رسائی حاصل ہے۔

### 2.3 کنٹینر پلیٹ فارم کا میل نہ کھانا (Apple Silicon)

اگر Apple Silicon Mac (M1/M2/M3/M4) سے تعینات کر رہے ہیں، تو کنٹینر کو `linux/amd64` کے لیے بنانا ہو گا کیونکہ Foundry کا کنٹینر رن ٹائم AMD64 استعمال کرتا ہے۔

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry ایکسٹینشن کا deploy کمانڈ زیادہ تر صورتوں میں یہ خود بخود سنبھال لیتا ہے۔ اگر آپ کو آرکیٹیکچر سے متعلق غلطیاں نظر آئیں، تو `--platform` فلیگ کے ساتھ دستی طور پر بلڈ کریں اور Foundry ٹیم سے رابطہ کریں۔

---

## 3. توثیق کی غلطیاں

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ٹوکن حاصل کرنے میں ناکام

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**بنیادی وجہ:** `DefaultAzureCredential` چین میں کوئی بھی کریڈینشل ذریعہ درست ٹوکن نہیں فراہم کر رہا۔

**حل - ہر قدم ترتیب سے آزما کر دیکھیں:**

1. **Azure CLI سے دوبارہ لاگ ان کریں** (سب سے عام حل):
   ```bash
   az login
   ```
   ایک براؤزر ونڈو کھلے گی۔ سائن ان کریں، پھر VS Code پر واپس جائیں۔

2. **درست سبسکرپشن سیٹ کریں:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   اگر یہ صحیح سبسکرپشن نہیں ہے:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code سے دوبارہ لاگ ان کریں:**
   - VS Code کے نیچے بائیں کونے میں **Accounts** آئیکن (شخص کا آئیکن) پر کلک کریں۔
   - اپنا اکاؤنٹ نام کلک کریں → **Sign Out**۔
   - دوبارہ Accounts آئیکن پر کلک کریں → **Sign in to Microsoft**۔
   - براؤزر سائن ان فلو مکمل کریں۔

4. **Service principal (صرف CI/CD معاملات میں):**
   - اپنی `.env` فائل میں یہ ماحولیاتی متغیرات سیٹ کریں:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - پھر اپنے ایجنٹ کے عمل کو ری اسٹارٹ کریں۔

5. **ٹوکن کیشے چیک کریں:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   اگر یہ ناکام ہو جائے، تو آپ کا CLI ٹوکن ختم ہو چکا ہے۔ دوبارہ `az login` چلائیں۔

### 3.2 ٹوکن مقامی طور پر کام کرتا ہے مگر ہوسٹڈ تعیناتی میں نہیں

**بنیادی وجہ:** ہوسٹڈ ایجنٹ سسٹم منیجڈ شناخت استعمال کرتا ہے، جو آپ کے ذاتی کریڈینشل سے مختلف ہوتی ہے۔

**حل:** یہ متوقع رویہ ہے - تعیناتی کے دوران منیجڈ شناخت خود بخود فراہم کی جاتی ہے۔ اگر ہوسٹڈ ایجنٹ پھر بھی auth کی غلطیاں دیتا ہے:
1. چیک کریں کہ Foundry پروجیکٹ کی منیجڈ شناخت کو Azure OpenAI ریسورس تک رسائی حاصل ہے۔
2. `agent.yaml` میں `PROJECT_ENDPOINT` کی درستگی کی تصدیق کریں۔

---

## 4. ماڈل کی غلطیاں

### 4.1 ماڈل کی تعیناتی نہیں ملی

```
Error: Model deployment not found / The specified deployment does not exist
```

**حل - قدم بہ قدم:**

1. اپنی `.env` فائل کھولیں اور `AZURE_AI_MODEL_DEPLOYMENT_NAME` کی قدر نوٹ کریں۔
2. VS Code میں **Microsoft Foundry** سائیڈبار کھولیں۔
3. اپنا پروجیکٹ بڑھائیں → **Model Deployments**۔
4. وہاں پر ماڈل کی تعیناتی کا نام اپنی `.env` کی قدر سے موازنہ کریں۔
5. نام **حساس برائے کیس** ہے - `gpt-4o` اور `GPT-4o` مختلف ہیں۔
6. اگر وہ میچ نہیں کرتے تو اپنی `.env` میں سائیڈبار میں دکھائے گئے اصل نام کو اپ ڈیٹ کریں۔
7. ہوسٹڈ تعیناتی کے لیے، `agent.yaml` بھی اپ ڈیٹ کریں:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 ماڈل غیر متوقع مواد کے ساتھ جواب دیتا ہے

**حل:**
1. `main.py` میں `EXECUTIVE_AGENT_INSTRUCTIONS` کانسٹنٹ کا جائزہ لیں۔ یقینی بنائیں کہ یہ ٹکڑا ہوا یا خراب نہیں ہوا ہے۔
2. ماڈل کا درجہ حرارت چیک کریں (اگر قابل ترتیب ہو) - کم قیمتیں زیادہ متعین نتائج دیتی ہیں۔
3. تعینات ماڈل کا موازنہ کریں (مثلاً، `gpt-4o` اور `gpt-4o-mini`) - مختلف ماڈلز کی مختلف صلاحیتیں ہوتی ہیں۔

---

## 5. تعیناتی کی غلطیاں

### 5.1 ACR پل اجازت

```
Error: AcrPullUnauthorized
```

**بنیادی وجہ:** Foundry پروجیکٹ کی منیجڈ شناخت Azure Container Registry سے کنٹینر امیج نہیں کھینچ پا رہی۔

**حل - قدم بہ قدم:**

1. [https://portal.azure.com](https://portal.azure.com) کھولیں۔
2. اوپر سرچ بار میں **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** تلاش کریں۔
3. اپنے Foundry پروجیکٹ سے منسلک ریجسٹری پر کلک کریں (عام طور پر وہی ریسورس گروپ میں ہوتا ہے)۔
4. بائیں نیویگیشن میں **Access control (IAM)** پر کلک کریں۔
5. **+ Add** → **Add role assignment** پر کلک کریں۔
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** تلاش کریں اور اسے منتخب کریں۔ **Next** پر کلک کریں۔
7. **Managed identity** منتخب کریں → **+ Select members** پر کلک کریں۔
8. Foundry پروجیکٹ کی منیجڈ شناخت تلاش کریں اور منتخب کریں۔
9. **Select** → **Review + assign** → **Review + assign** پر کلک کریں۔

> یہ رول تفویض عام طور پر Foundry ایکسٹینشن کے ذریعے خود بخود کیا جاتا ہے۔ اگر یہ غلطی نظر آتی ہے تو خودکار سیٹ اپ ناکام ہو سکتا ہے۔ آپ دوبارہ تعیناتی کی کوشش بھی کر سکتے ہیں - ایکسٹینشن سیٹ اپ دوبارہ کوشش کر سکتا ہے۔

### 5.2 تعیناتی کے بعد ایجنٹ شروع ہونے میں ناکام

**علامات:** کنٹینر کی حالت 5 منٹ یا اس سے زیادہ "Pending" رہتی ہے یا "Failed" دکھاتی ہے۔

**حل - قدم بہ قدم:**

1. VS Code میں **Microsoft Foundry** سائیڈبار کھولیں۔
2. اپنے ہوسٹڈ ایجنٹ پر کلک کریں → ورژن منتخب کریں۔
3. تفصیل والے پینل میں **Container Details** چیک کریں → **Logs** سیکشن یا لنک تلاش کریں۔
4. کنٹینر اسٹارٹ اپ لاگز پڑھیں۔ عام وجوہات:

| لاگ پیغام | وجہ | حل |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | انحصار کی کمی | اسے `requirements.txt` میں شامل کریں اور دوبارہ تعینات کریں |
| `KeyError: 'PROJECT_ENDPOINT'` | ماحولیاتی متغیر کی کمی | `agent.yaml` میں `env:` کے تحت env var شامل کریں |
| `OSError: [Errno 98] Address already in use` | پورٹ تصادم | یقینی بنائیں کہ `agent.yaml` میں `port: 8088` ہے اور صرف ایک عمل اس سے باندھا ہوا ہے |
| `ConnectionRefusedError` | ایجنٹ سننا شروع نہیں کیا | `main.py` میں چیک کریں - `from_agent_framework()` کال اسٹارٹ اپ پر چلنی چاہیے |

5. مسئلہ حل کریں، پھر [ماڈیول 6](06-deploy-to-foundry.md) سے دوبارہ تعینات کریں۔

### 5.3 تعیناتی کا وقت ختم ہو جانا

**حل:**
1. اپنے انٹرنیٹ کنکشن چیک کریں - Docker push بڑی ہو سکتی ہے (>100MB پہلی تعیناتی پر)۔
2. اگر کسی کارپوریٹ پراکسی کے پیچھے ہیں، تو یقینی بنائیں کہ Docker Desktop پراکسی سیٹنگز درست ہیں: **Docker Desktop** → **Settings** → **Resources** → **Proxies**۔
3. دوبارہ کوشش کریں - نیٹ ورک کی عارضی خرابیوں کی وجہ سے ناکام ہو سکتا ہے۔

---

## 6. فوری حوالہ: RBAC رولز

| رول | عمومی دائرہ کار | کیا فراہم کرتا ہے |
|------|---------------|----------------|
| **Azure AI User** | پروجیکٹ | ڈیٹا ایکشنز: ایجنٹس بنائیں، تعینات کریں، اور کال کریں (`agents/write`, `agents/read`) |
| **Azure AI Developer** | پروجیکٹ یا اکاؤنٹ | ڈیٹا ایکشنز + پروجیکٹ بنانا |
| **Azure AI Owner** | اکاؤنٹ | مکمل رسائی + رول تفویض کا انتظام |
| **Azure AI Project Manager** | پروجیکٹ | ڈیٹا ایکشنز + دوسروں کو Azure AI User تفویض کر سکتا ہے |
| **Contributor** | سبسکرپشن/آر جی | مینجمنٹ ایکشنز (ریسورسز بنانا/حذف کرنا)۔ **ڈیٹا ایکشنز شامل نہیں ہیں** |
| **Owner** | سبسکرپشن/آر جی | مینجمنٹ ایکشنز + رول تفویض۔ **ڈیٹا ایکشنز شامل نہیں ہیں** |
| **Reader** | کوئی بھی | صرف مینجمنٹ تک رسائی |

> **اہم نکات:** `Owner` اور `Contributor` میں ڈیٹا ایکشنز شامل نہیں ہوتے۔ ایجنٹ آپریشنز کے لیے آپ کو ہمیشہ `Azure AI *` رول کی ضرورت ہوتی ہے۔ اس ورکشاپ کے لیے کم از کم رول **Azure AI User** ہے جو **پروجیکٹ** دائرہ کار میں ہو۔

---

## 7. ورکشاپ مکمل کرنے کی چیک لسٹ

اسے سب کچھ مکمل کرنے کی آخری منظوری کے طور پر استعمال کریں:

| # | آئٹم | ماڈیول | پاس؟ |
|---|------|--------|---|
| 1 | تمام پیشگی ضروریات انسٹال اور تصدیق شدہ | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit اور Foundry ایکسٹینشنز انسٹال | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry پروجیکٹ بنایا گیا (یا موجودہ پروجیکٹ منتخب کیا گیا) | [02](02-create-foundry-project.md) | |
| 4 | ماڈل تعینات کیا گیا (مثلاً، gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI صارف کا کردار پروجیکٹ کے دائرہ کار میں تفویض کیا گیا | [02](02-create-foundry-project.md) | |
| 6 | ہوسٹڈ ایجنٹ پروجیکٹ تیار کیا گیا (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` میں PROJECT_ENDPOINT اور MODEL_DEPLOYMENT_NAME کی ترتیب دی گئی | [04](04-configure-and-code.md) | |
| 8 | ایجنٹ کی ہدایات main.py میں حسب ضرورت بنائی گئی | [04](04-configure-and-code.md) | |
| 9 | ورچوئل ماحول بنایا گیا اور درکار پیکیجز انسٹال کیے گئے | [04](04-configure-and-code.md) | |
| 10 | ایجنٹ کو مقامی طور پر F5 یا ٹرمینل کے ذریعے آزمایا گیا (4 سمoke ٹیسٹ کامیاب) | [05](05-test-locally.md) | |
| 11 | Foundry Agent سروس میں تعینات کیا گیا | [06](06-deploy-to-foundry.md) | |
| 12 | کنٹینر کی حالت "شروع" یا "چل رہا ہے" ظاہر کرتی ہے | [06](06-deploy-to-foundry.md) | |
| 13 | VS کوڈ پلے گراؤنڈ میں تصدیق کی گئی (4 سمoke ٹیسٹ کامیاب) | [07](07-verify-in-playground.md) | |
| 14 | Foundry پورٹل پلے گراؤنڈ میں تصدیق کی گئی (4 سمoke ٹیسٹ کامیاب) | [07](07-verify-in-playground.md) | |

> **مبارک ہو!** اگر تمام اشیاء چیک ہو چکی ہیں، تو آپ نے پورا ورکشاپ مکمل کر لیا ہے۔ آپ نے ایک ہوسٹڈ ایجنٹ بالکل صفر سے بنایا، اسے مقامی طور پر ٹیسٹ کیا، Microsoft Foundry پر تعینات کیا، اور پروڈکشن میں اس کی تصدیق کی ہے۔

---

**پچھلا:** [07 - پلے گراؤنڈ میں تصدیق کریں](07-verify-in-playground.md) · **ہوم:** [ورکشاپ کا README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**دستبرداری**:
اس دستاویز کا ترجمہ AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعہ کیا گیا ہے۔ اگرچہ ہم درستگی کی کوشش کرتے ہیں، براہ کرم آگاہ رہیں کہ خودکار تراجم میں غلطیاں یا عدم وضاحت ہو سکتی ہے۔ اصل دستاویز کو اس کی مادری زبان میں مستند ذریعہ سمجھا جانا چاہیے۔ اہم معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ ہم اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کے لیے ذمہ دار نہیں ہیں۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->