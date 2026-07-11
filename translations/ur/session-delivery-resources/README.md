# اس سیشن کو کیسے پہنچانا ہے

اس سیشن کو پہنچانے کا شکریہ!

ورکشاپ پہنچانے سے پہلے، براہ کرم:

1. اس دستاویز اور شامل تمام وسائل کو مکمل طور پر پڑھیں۔
2. سیشن کی ڈیلیوری ریکارڈنگ اور ورکشاپ کے شروع سے آخر تک واک تھرو کو دیکھیں۔
3. دونوں ہینڈز-آن لیبز کو اپنی مشین پر **کم از کم ایک بار** پورے طور پر مکمل کریں۔
4. اپنے Microsoft Foundry پروجیکٹ، ماڈل ڈیپلائمنٹس، اور کوٹاز کی توثیق کریں۔
5. اگر کچھ سمجھ نہ آئے تو مینٹینر سے رابطہ کریں۔

---

## فائل کا خلاصہ

| وسیلہ                         | لنک                                                                             | وضاحت                                                                                     |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| ورکشاپ سلائیڈ ڈیک            | [ورکشاپ ڈیک](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | اس ورکشاپ کے پریزنٹیشن سلائیڈز، پریزنٹر کے نوٹس اور شامل ڈیمو ویڈیوز                            |
| سیشن کی ڈیلیوری ریکارڈنگ      | _مینٹینر کی طرف سے فراہم کی جائے گی_                                               | ورکشاپ کا تعارف اور سلائیڈ واک تھرو ریکارڈنگ                                                 |
| ورکشاپ کا شروع سے آخر تک ریکارڈنگ | _مینٹینر کی طرف سے فراہم کی جائے گی_                                               | دونوں لیبز کی شروع سے آخر تک ریکارڈنگ، سیکھنے والے کے نقطہ نظر سے                                |
| ورکشاپ دستاویزات             | [ریپوزیٹری](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | ماخذ ریپوزیٹری، لیب کے ریڈمز، مرحلہ وار ماڈیولز                                              |
| لیب 01 - سنگل ایجنٹ           | [لیب 01](../workshop/lab01-single-agent/README.md)                               | ہینڈز-آن لیب: *Explain Like I'm an Executive* میزبانی شدہ ایجنٹ تیار کریں، ٹیسٹ اور ڈیپلائے کریں    |
| لیب 02 - ملٹی ایجنٹ ورک فلو    | [لیب 02](../workshop/lab02-multi-agent/README.md)                                | ہینڈز-آن لیب: 4 ایجنٹ *Resume to Job Fit Evaluator* ورک فلو تیار کریں                          |
| ڈیمو 1: ایگزیکٹو ایجنٹ           | [لیب01 ایجنٹ](../../../workshop/lab01-single-agent/agent)                                              | لیب 01 ڈیمو: تکنیکی اصطلاحات کو ایگزیکٹو خلاصہ میں ترجمہ کریں                                   |
| ڈیمو 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | لیب 02 ڈیمو: 4-ایجنٹ ورک فلو جو ریزیومے-جاب فٹ کی درجہ بندی کرتا ہے اور سفارشات جنریٹ کرتا ہے   |

> **تربیت دہندگان کے لیے نوٹ:** جب ریکارڈنگز شائع ہو جائیں گی تو سلائیڈ ڈیک اور ویڈیو کے لنکس شامل کیے جائیں گے۔ تب تک تازہ ترین مواد کے لیے مینٹینر سے رابطہ کریں (دیکھیں [Contacts](#رابطے))۔

---

## شروع کریں

یہ ورکشاپ ڈیولپرز کو سکھاتی ہے کہ کس طرح AI ایجنٹس کو **Microsoft Foundry Agent Service** میں **Hosted Agents** کے طور پر مکمل طور پر VS Code سے بنا، ٹیسٹ، اور ڈیپلائے کریں، **Microsoft Foundry Toolkit** ایکسٹینشن کا استعمال کرتے ہوئے۔

ورکشاپ متعدد حصوں میں تقسیم ہے جن میں سلائیڈز، **2 لائیو ڈیموز**، اور **2 ہینڈز-آن لیبز** شامل ہیں۔

### وقت کا تعین

#### مکمل ڈیلیوری (تقریباً 2 گھنٹے)

| وقت             | وضاحت                                                            |
|-----------------|-----------------------------------------------------------------|
| 0:00 - 10:00    | تعارف: hosted agents، Foundry Agent Service، اور ٹول کٹ          |
| 10:00 - 20:00   | ڈیمو: ایگزیکٹو ایجنٹ شروع سے آخر تک                              |
| 20:00 - 60:00   | لیب 01 - سنگل ایجنٹ (بنائیں، لوکل ٹیسٹ کریں، ڈیپلائے کریں، پلے گراونڈ) |
| 60:00 - 110:00  | لیب 02 - ملٹی ایجنٹ ورک فلو (Resume to Job Fit Evaluator)       |
| 110:00 - 120:00 | خلاصہ، سوال و جواب، جاری رہنے والے تعلیمی وسائل                  |

#### مختصر ڈیلیوری (تقریباً 75 منٹ)

| وقت          | وضاحت                                                      |
|---------------|-------------------------------------------------------------|
| 0:00 - 10:00  | تعارف اور جائزہ                                          |
| 10:00 - 20:00 | ڈیمو: ایگزیکٹو ایجنٹ                                   |
| 20:00 - 70:00 | صرف لیب 01 (شرکاء کو لیب 02 کو خود سے مکمل کرنے کی ہدایت کریں) |
| 70:00 - 75:00 | خلاصہ اور سوال و جواب                                   |

### تیاری

| وسیلہ                           | لنک                                                                                          | وضاحت                                          |
|--------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------|
| ورکشاپ دستاویزات              | [ریپوزیٹری](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | ورکشاپ دستاویزات اور ماخذ                     |
| لیب 01 کی ہدایات               | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | ہینڈز-آن لیب: سنگل میزبانی شدہ ایجنٹ          |
| لیب 02 کی ہدایات               | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | ہینڈز-آن لیب: ملٹی ایجنٹ ورک فلو               |
| ضروریات کی چیک لسٹ            | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | درکار ٹولز، اکاؤنٹس، اور Azure رسائی          |
| Hosted agents کا تیز آغاز (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | `azd` کے ذریعے میزبانی شدہ ایجنٹ کو ڈیپلائے کرنے کا سرکاری تیز آغاز |
| Hosted agents کے خطوں کی دستیابی | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | میزبانی شدہ ایجنٹس کی حمایت یافتہ خطے (پریویو)  |

### تربیت دہندگان کے لیے ضروریات

ڈیلیوری سے پہلے، یقینی بنائیں کہ آپ کے پاس ہے:

- ایک **Azure سبسکرپشن** جسے وسائل بنانے کی اجازت ہو (Owner یا Contributor کسی resource group پر)۔
- ایک **Microsoft Foundry پروجیکٹ** جس کا تعلق [اس خطے سے ہو جو hosted agents کی حمایت کرتا ہے](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)۔
- اپنے Foundry پروجیکٹ میں **gpt-4.1** (یا **gpt-4.1-mini**) کے لیے کوٹا۔
- درج ذیل ٹولز انسٹال کیے ہوئے:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (اختیاری)
  - Python 3.10 یا بعد کا ورژن

ڈیلیوری سے پہلے کم از کم ایک بار [Hosted agents تیز آغاز `azd` کے ساتھ](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) چلائیں تاکہ آپ کے پاس ایک معروف Foundry پروجیکٹ، ماڈل ڈیپلائمنٹ، اور Azure Container Registry ہو جس کا حوالہ دیا جا سکے اگر کوئی سیکھنے والا پھنس جائے۔

---

## سلائیڈ واک تھرو

یہ ڈیک لیبز کے بہاؤ کو فالو کرتا ہے۔ ہر سیکشن کے لیے تجویز کردہ بات چیت کے نکات:

| سیکشن                    | اہم پیغام                                                                                                  |
|--------------------------|------------------------------------------------------------------------------------------------------------|
| عنوان اور ایجنڈا         | ورکشاپ کو *VS Code سے Foundry* کے طور پر فریم کریں، بغیر کسی پورٹل سوئچنگ کے۔                             |
| کیوں hosted agents؟      | مینیجڈ رن ٹائم، ACR پر مبنی ڈیپلائمنٹ، OpenAI کے ہم آہنگ `/responses` API، Foundry پروجیکٹس کے دائرہ کار میں۔    |
| فن تعمیر کا خاکہ         | [README فن تعمیر](../README.md#architecture) کا واک تھرو: اسکافولڈ، انسپیکٹر، ACR، ایجنٹ سروس۔              |
| میزبانی شدہ ایجنٹ کی بناوٹ | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - ہر فائل کا کام۔                               |
| لائیو ڈیمو: ایگزیکٹو ایجنٹ | VS Code پر تبدیل ہوں اور [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) ڈیمو پورے طور پر چلائیں (دیکھیں [Demo 1](#ڈیمو-1-ایگزیکٹو-ایجنٹ))۔ |
| لائیو ڈیمو: Resume to Job Fit Evaluator | VS Code پر تبدیل ہوں اور [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-ایجنٹ ڈیمو چلائیں (دیکھیں [Demo 2](#ڈیمو-2-resume-to-job-fit-evaluator))۔ |
| لیب 01 کا مختصر تعارف    | شرکاء کو حوالے کریں۔ [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md) کی جانب اشارہ کریں۔ |
| ملٹی ایجنٹ پیٹرنز         | ترتیب وار بمقابلہ متوازی بمقابلہ ہینڈ آف - لیب 02 شروع ہونے سے پہلے پیش نظر۔                                |
| لیب 02 کا مختصر تعارف    | شرکاء کو حوالے کریں۔ [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md) کی جانب اشارہ کریں۔ |
| اختتام اور وسائل          | [اضافی وسائل](#اضافی-وسائل) سیکشن سے جاری تعلیمی لنکس۔                                         |

---

## ڈیموز

دو لائیو ڈیموز ڈیلیوری میں شامل ہیں۔ ہر ایک کو 10 منٹ دیں۔

| ڈیمو                  | لیب  | فائلز                                                                                     | کیا دکھانا ہے                                           |
|-----------------------|-------|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| ایگزیکٹو ایجنٹ         | لیب 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)                | واحد میزبانی شدہ ایجنٹ؛ تکنیکی اصطلاحات کو ایگزیکٹو خلاصہ میں ترجمہ کریں |
| Resume to Job Fit Evaluator | لیب 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-ایجنٹ آرکسیسٹریشن؛ ریزیومے-جاب فٹ کی درجہ بندی کریں اور سفارش جنریٹ کریں |

### ڈیمو 1: ایگزیکٹو ایجنٹ

ایک خود مختار ایجنٹ [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) میں۔ یہ لیب 01 سے پہلے 10 منٹ کا ڈیمو کے طور پر استعمال کریں۔

1. [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) کھولیں اور ایجنٹ کی تعریف (سسٹم پرامپٹ، ماڈل، فریم ورک) کا جائزہ لیں۔
2. `F5` دبائیں تاکہ **Agent Inspector** لوکل طور پر چلایا جا سکے۔
3. [README](../README.md#see-it-in-action) سے نمونہ پرامپٹ پیسٹ کریں اور ایگزیکٹو خلاصہ کا جواب دکھائیں۔
4. [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) اور [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) دکھائیں اور تعیناتی کے آرٹیفیکٹس کی وضاحت کریں۔
5. تعیناتی کے بہاؤ (Docker build، ACR push، hosted agent create) کا مظاہرہ کریں بغیر مکمل ہونے کا انتظار کیے۔

### ڈیمو 2: Resume to Job Fit Evaluator

[`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) میں 4-ایجنٹ ورک فلو۔ یہ لیب 02 سے پہلے 10 منٹ کا ڈیمو کے طور پر استعمال کریں۔

1. [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) کھولیں اور دکھائیں کہ چار ایجنٹس ایک ترتیب وار آرکسیسٹریشن میں کیسے منسلک ہیں۔
2. ملٹی-ایجنٹ ورک فلو کے لیے **Agent Inspector** چلانے کے لیے `F5` دبائیں۔
3. انسپیکٹر چیٹ میں ایک مختصر ملازمت کی تفصیل اور ایک نمونہ ریزیومے پیسٹ کریں۔
4. چار ایجنٹ کی پائپ لائن کا جائزہ لیں: ریزیومے پارسر، جاب ریکوائرمنٹ ایکسٹریکٹر، فٹ سکورر، اور ریکمینڈیشن رائٹر۔
5. بتائیں کہ ہر ذیلی ایجنٹ کا آؤٹ پٹ اگلے ایجنٹ کے سیاق و سباق میں کیسے بدلتا ہے، ہینڈ آف پیٹرن کو اجاگر کریں۔
6. [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) دکھائیں اور اسے ڈیمو 1 کے سنگل ایجنٹ کے مقابلہ میں رکھیں۔

---

## ڈیلیوری کے نکات

- **امیدیں پہلے ہی طے کریں۔** Hosted agents پریویو میں ہیں - خطے کی حدود اور کوٹا شروع میں بتائیں تاکہ شرکاء کو لیب کے دوران حیرت نہ ہو۔
- **ضروریات کا کام پہلے چلائیں۔** دونوں لیبز `Validate prerequisites` VS Code ٹاسک فراہم کرتی ہیں - شرکاء کو کہیں کہ یہ کوڈ لکھنے سے پہلے چلائیں۔
- **Agent Inspector کو نظر میں رکھیں۔** زیادہ تر "آہا" لمحات اس وقت ہوتے ہیں جب سیکھنے والے لوکل `/responses` راؤنڈ-ٹرپ کو روشن دیکھتے ہیں۔
- **ایک بیک اپ پروجیکٹ رکھیں۔** اگر کسی سیکھنے والے کا Foundry پروجیکٹ کوٹا کی حد پر پہنچ جائے، تو ڈیپلائمنٹ کے مرحلے کے لیے پری-پروویژند پروجیکٹ شئیر کریں تاکہ کلاس بلاک نہ ہو۔
- **شرکاء کو جوڑوں میں بٹھائیں۔** لیب 02 (ملٹی ایجنٹ) تب زیادہ آسان ہوتی ہے جب سیکھنے والے کسی ساتھی کے ساتھ آرکسیسٹریشن پر بات کر سکیں۔
- **دستاویزات کے ماڈیولز کو چیک پوائنٹس کے طور پر استعمال کریں۔** ہر لیب کا `docs/` فولڈر 8 عددی ماڈیولز میں تقسیم ہے - انہیں قدرتی وقفہ پوائنٹس کے طور پر استعمال کریں۔
- **بنیادی Docker امیج کو پہلے سے کھینچ لیں** تاکہ شیئرڈ لیب مشینوں پر ریجسٹری ریٹ لمیٹس سے بچا جا سکے۔

---

## ڈیلیوری کے دوران مسائل کا حل

| علامت                                      | سب سے پہلی کوشش                                                                                      |
|----------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Agent Inspector کنیکٹ نہیں کر سکتا          | تصدیق کریں کہ پورٹ `8088` خالی ہے اور `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` ٹاسک چل رہا ہے۔|
| ڈی بگر منسلک نہیں ہوتا                      | چیک کریں کہ پورٹ `5679` خالی ہے؛ اگر `debugpy` پہلے سے منسلک ہے تو VS Code کو ری اسٹارٹ کریں۔           |
| `azd up` مصدقہ غلطی دیتا ہے                 | `az login` اور `azd auth login` چلائیں، یقینی بنائیں کہ درست ٹینینٹ منتخب کیا گیا ہے۔                 |
| تعیناتی ACR پش پر رک جاتی ہے                  | چیک کریں کہ Docker Desktop چل رہا ہے اور صارف کے پاس ریجسٹری پر `AcrPush` کی اجازت ہے۔               |
| ماڈل 404 / deployment-not-found دیتا ہے      | `agent.yaml` میں ماڈل تعیناتی کا نام Foundry پروجیکٹ میں تعیناتی کے نام سے میل کھانا چاہیے۔             |

| ہوستڈ ایجنٹ `Provisioning` میں پھنس گیا ہے         | تصدیق کریں کہ پراجیکٹ کا علاقہ [ہوسٹڈ ایجنٹس کی حمایت کرتا ہے](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) اور کوٹہ دستیاب ہے۔ |
| پلے گراؤنڈ 401 واپس کرتا ہے                       | VS کوڈ ایکٹیویٹی بار سے Foundry ایکسٹینشن کو دوبارہ توثیق کریں۔                                   |

مزید گہرائی میں رہنمائی کے لیے، ہر لیب اپنی `08-troubleshooting.md` دستاویز فراہم کرتی ہے - سیکھنے والوں کو وہاں لنک کریں:

- لیب 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- لیب 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## اس نشست کو حسبِ منشا بنانا

آپ ورکشاپ کو اپنے ناظرین کے مطابق ڈھال سکتے ہیں۔ عام تبدیلیاں:

- **بیک اینڈ ناظرین:** `agent.yaml`، ڈوکر، اور ACR پر زیادہ وقت دیں؛ پلے گراؤنڈ ڈیمو کو کم کریں۔
- **سِٹیزن ڈیولپر ناظرین:** سکیفولڈنگ کے لیے Foundry ایکسٹینشن UI میں رہیں؛ CLI اقدامات کو کم کریں۔
- **سنگل ٹریک 60 منٹ کا سیشن:** صرف تعارف، ڈیمو، اور لیب 01 فراہم کریں۔
- **صرف ورکشاپ (بغیر سلائیڈز) فارمیٹ:** دونوں لیب کے README کھولیں اور انہیں بنیادی اسکرپٹ کے طور پر استعمال کریں۔

اگر آپ لیبز کو بڑھاتے ہیں، تو براہ کرم تبدیلیاں PR کے ذریعے واپس جمع کریں تاکہ دوسرے ٹرینرز کو فائدہ ہو۔

---

## اضافی وسائل

- [Microsoft Foundry دستاویزات](https://learn.microsoft.com/azure/ai-foundry/)
- [ہوسٹڈ ایجنٹس کا جائزہ](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [فوری آغاز: اپنا پہلا ہوسٹڈ ایجنٹ تعینات کریں (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [ہوسٹڈ ایجنٹ تعینات کریں (کیسے)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent فریم ورک](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit برائے VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## رابطے

اگر آپ کو اس نشست کی فراہمی کے بارے میں سوالات ہیں، تو براہ کرم [ورکشاپ ریپوزیٹری](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) پر ایک مسئلہ کھولیں اور مینٹینر کو ٹیگ کریں۔

| کردار                | نام           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| مینٹینر / رابطہ| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ڈس کلیمر**:
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ جبکہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم اس بات سے آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنے مادری زبان میں مستند ماخذ سمجھی جائے گی۔ حساس معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم قبول نہیں کرتے۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->