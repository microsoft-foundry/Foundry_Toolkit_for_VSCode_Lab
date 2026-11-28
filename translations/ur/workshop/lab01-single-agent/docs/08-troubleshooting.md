# ماڈیول 8 - مسئلہ حل کرنا

یہ ماڈیول عام مسائل کے لیے ایک حوالہ گائیڈ ہے۔ اسے محفوظ کریں اور جب کچھ خراب ہو جائے تو واپس آئیں۔

---

## 1. اجازت کی غلطیاں

### 1.1 `agents/write` اجازت نہیں دی گئی

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**بنیادی وجہ:** `Azure AI User` کی کمی **پروجیکٹ** سطح پر۔ یہ ورکشاپ کی سب سے عام غلطی ہے۔

**حل:**
1. کھولیں [portal.azure.com](https://portal.azure.com).
2. اپنے Foundry **پروجیکٹ** کا نام تلاش کریں → اس نتیجے پر کلک کریں جو **"Microsoft Foundry project"** قسم کا ہو (والد اکاؤنٹ نہیں)۔
3. **Access control (IAM)** → **+ Add** → **Add role assignment**۔
4. رول: **Azure AI User** → آگے بڑھیں۔
5. اراکین: خود کو منتخب کریں → جائزہ لیں + تفویض کریں → جائزہ لیں + تفویض کریں۔
6. **1–2 منٹ انتظار کریں** → دوبارہ کوشش کریں۔

> **کیوں Owner/Contributor کافی نہیں ہیں:** یہ رولز صرف *انتظامی* کارروائیاں دیتے ہیں۔ ایجنٹ کے عملیات کو `agents/write` *ڈیٹا ایکشن* کی ضرورت ہوتی ہے، جو صرف `Azure AI User`، `Azure AI Developer`، یا `Azure AI Owner` میں ہوتا ہے۔ دیکھیں [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)۔

### 1.2 `AuthorizationFailed` پروویژنگ کے دوران

**حل:** اپنے ایڈمن سے کہیں کہ resource group پر **Contributor** تفویض کریں، یا وہ آپ کے لیے پروجیکٹ بنائیں اور آپ کو اس پر **Azure AI User** دیں۔

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker کی غلطیاں

> Docker **اختیاری** ہے۔ یہ صرف اس صورت میں لاگو ہوتے ہیں جب Docker Desktop انسٹال ہو اور ایکسٹینشن مقامی تعمیر کی کوشش کر رہا ہو۔

### 2.1 Docker daemon کام نہیں کر رہا

**حل:** Docker Desktop شروع کریں → "running" کی حیثیت کا انتظار کریں → `docker info` کے ساتھ تصدیق کریں → دوبارہ کوشش کریں۔

### 2.2 انحصار کی غلطیوں کے ساتھ تعمیر ناکام

**حل:** `requirements.txt` کی ہجے کی درستگی چیک کریں، پہلے مقامی طور پر ٹیسٹ کریں: `pip install -r requirements.txt`۔

### 2.3 پلیٹ فارم کا عدم مطابقت (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. تصدیقی غلطیاں

### 3.1 `DefaultAzureCredential` ناکام ہوتا ہے

**حل (ترتیب سے کوشش کریں):**
1. `az login` (دوبارہ تصدیق کریں)
2. `az account set --subscription "<id>"` (صحیح سبسکرپشن)
3. VS Code → Accounts → سائن آؤٹ → دوبارہ سائن ان کریں
4. تصدیق کریں: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 ٹوکن مقامی طور پر کام کرتا ہے لیکن ہوسٹڈ نہیں

**متوقع:** ہوسٹڈ ایجنٹ سسٹم مینجڈ شناخت کا استعمال کرتے ہیں، آپ کی اسناد نہیں۔ اگر ہوسٹڈ ایجنٹ کو تصدیقی غلطیاں ملیں:
- یقینی بنائیں کہ `AZURE_AI_MODEL_DEPLOYMENT_NAME` میں `agent.yaml` آپ کے ماڈل کی تعیناتی کے نام پر حل ہوتا ہے (`FOUNDRY_PROJECT_ENDPOINT` Foundry کی طرف سے رن ٹائم پر شامل کیا جاتا ہے - اسے `agent.yaml` میں مت ظاہر کریں)
- چیک کریں کہ پروجیکٹ کی مینجڈ شناخت کے پاس ماڈل تک رسائی ہے

---

## 4. ماڈل کی غلطیاں

### 4.1 ماڈل کی تعیناتی نہیں ملی

**حل:** نام **حساسیت بڑے اور چھوٹے حروف کی** ہے۔ `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` کی اصل نام سے Foundry سائڈبار → ماڈلز میں موازنہ کریں۔

### 4.2 غیر متوقع ماڈل کا آؤٹ پٹ

**حل:** `AGENT_INSTRUCTIONS` کو `main.py` میں جائزہ لیں (کیا کٹا ہوا نہیں؟). کوئی مختلف ماڈل آزمائیں (`gpt-4.1` بمقابلہ `gpt-4.1-mini`)۔

---

## 5. تعیناتی کی غلطیاں

### 5.1 ACR پل کی اجازت نہیں

**حل:** Azure پورٹل → کنٹینر رجسٹری → Access control (IAM) → Foundry پروجیکٹ کی مینجڈ شناخت کو **AcrPull** رول تفویض کریں۔

### 5.2 ایجنٹ شروع ہونے میں ناکام (ہمیشہ "Pending" یا "Failed" رہتا ہے)

سائڈبار میں کنٹینر لاگز چیک کریں۔ عام وجوہات:

| لاگ پیغام | حل |
|-------------|-----|
| `ModuleNotFoundError` | کھویا ہوا پیکیج `requirements.txt` میں شامل کریں، دوبارہ تعینات کریں |
| `ValueError: Missing required environment variables` | تصدیق کریں `AZURE_AI_MODEL_DEPLOYMENT_NAME` `agent.yaml` میں `environment_variables` کے تحت ظاہر ہے اور اس کی کوئی قیمت ہے، پھر دوبارہ تعینات کریں۔ `FOUNDRY_PROJECT_ENDPOINT` Foundry کی طرف سے رن ٹائم پر شامل کیا جاتا ہے |
| `Address already in use` | یقینی بنائیں کہ صرف ایک عمل پورٹ 8088 پر باندھا ہوا ہے |

### 5.3 تعیناتی کا وقت ختم ہو گیا

**حل:** انٹرنیٹ کنکشن چیک کریں۔ پہلی تعیناتی 100MB سے زیادہ ڈیٹا بھیجتی ہے۔ کیا آپ پراکسی کے پیچھے ہیں؟ Docker Desktop پراکسی سیٹنگز تشکیل دیں۔

---

## 6. راستہ ب - Foundry مقامی

### 6.1 Foundry مقامی شروع نہیں ہو رہا

| مسئلہ | حل |
|-------|-----|
| `foundry: command not found` | دوبارہ تنصیب کریں: `winget install Microsoft.FoundryLocal` |
| وسائل ناکافی ہیں | Foundry مقامی کو تقریباً 4GB RAM خالی چاہیے۔ دیگر ایپس بند کریں۔ |
| ماڈل ڈاؤن لوڈ ناکام | ڈسک کی جگہ چیک کریں (ماڈلز 2–8 GB کے ہوتے ہیں). دوبارہ کوشش کریں: `foundry local models pull <name>` |

### 6.2 Foundry مقامی ماڈل کی غلطیاں

| مسئلہ | حل |
|-------|-----|
| سست جوابات | متوقع ہے - مقامی ماڈلز CPU پر چلتے ہیں جب تک کہ آپ کے پاس GPU نہ ہو۔ صبر کریں۔ |
| خراب معیار کا آؤٹ پٹ | اگر آپ کے ہارڈویئر کی اجازت ہو تو بڑے ماڈل کی کوشش کریں۔ `phi-4-mini` اچھا توازن ہے۔ |
| کنکشن مسترد شدہ | تصدیق کریں کہ Foundry مقامی چل رہا ہے: `foundry local status`۔ ضرورت پڑنے پر دوبارہ شروع کریں۔ |

---

## 7. فوری حوالہ: RBAC رولز

| رول | دائرہ کار | اجازتیں |
|------|-------|--------|
| **Azure AI User** | پروجیکٹ | ڈیٹا ایکشنز: `agents/write`، `agents/read` |
| **Azure AI Developer** | پروجیکٹ/اکاؤنٹ | ڈیٹا ایکشنز + پروجیکٹ تخلیق |
| **Azure AI Owner** | اکاؤنٹ | مکمل رسائی + رول انتظام |
| **Contributor** | سبسکرپشن/آر جی | صرف انتظامی کارروائیاں (**کوئی** ڈیٹا ایکشنز نہیں) |
| **Owner** | سبسکرپشن/آر جی | انتظام + رول تفویض (**کوئی** ڈیٹا ایکشنز نہیں) |

---

## 8. ورکشاپ مکمل کرنے کی چیک لسٹ

| # | آئٹم | ماڈیول |
|---|------|--------|
| 1 | پری ریکوزیٹس انسٹال ہو چکے اور تصدیق شدہ | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit ایکسٹینشن انسٹال، پروجیکٹ منسلک (یا راستہ ب ترتیب دیا گیا) | [01](01-setup.md) |
| 3 | ہوسٹڈ ایجنٹ تیار کیا گیا | [02](02-create-hosted-agent.md) |
| 4 | `.env` ترتیب دیا گیا، ہدایات لکھی گئی، انحصارات انسٹال کیے گئے | [03](03-configure-and-code.md) |
| 5 | ایجنٹ مقامی طور پر ٹیسٹ کیا گیا - 3 فعالیتی منظرنامے پاس ہوئے | [04](04-test-locally.md) |
| 6 | Foundry میں تعینات کیا گیا (صرف راستہ A) | [05](05-deploy-to-foundry.md) |
| 7 | ایج-کیس/حفاظتی ٹیسٹ کلاؤڈ میں پاس ہوئے (صرف راستہ A) | [06](06-verify-in-playground.md) |
| 8 | خلاصہ کا جائزہ لیا، اگلے اقدامات کی شناخت کی | [07](07-summary.md) |

---

**پچھلا:** [07 - خلاصہ](07-summary.md) · **گھر:** [ورکشاپ README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->