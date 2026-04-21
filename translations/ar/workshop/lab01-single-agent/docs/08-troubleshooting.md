# الوحدة 8 - استكشاف الأخطاء وإصلاحها

تعد هذه الوحدة دليل مرجعي لكل مشكلة شائعة يتم مواجهتها خلال الورشة. قم بإضافتها للمفضلة - ستعود إليها كلما حدث خطأ ما.

---

## 1. أخطاء الأذونات

### 1.1 تم رفض إذن `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**السبب الجذري:** ليس لديك دور `Azure AI User` على مستوى **المشروع**. هذا هو الخطأ الأكثر شيوعًا في الورشة.

**الإصلاح - خطوة بخطوة:**

1. افتح [https://portal.azure.com](https://portal.azure.com).
2. في شريط البحث العلوي، اكتب اسم **مشروع Foundry** الخاص بك (مثلاً، `workshop-agents`).
3. **مهم:** انقر على النتيجة التي تظهر نوع **"مشروع Microsoft Foundry"**، وليس المورد الحساب/المحور الرئيسي. هذه موارد مختلفة بنطاقات RBAC مختلفة.
4. في التنقل الأيسر لصفحة المشروع، انقر على **التحكم في الوصول (IAM)**.
5. انقر على تبويب **تعيينات الأدوار** للتحقق مما إذا كان لديك الدور بالفعل:
   - ابحث عن اسمك أو بريدك الإلكتروني.
   - إذا كان `Azure AI User` مدرجًا بالفعل → يكون الخطأ بسبب مختلف (تحقق من الخطوة 8 أدناه).
   - إذا لم يكن مدرجًا → تابع لإضافته.
6. انقر على **+ إضافة** → **إضافة تعيين دور**.
7. في تبويب **الدور**:
   - ابحث عن [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - اختره من النتائج.
   - انقر على **التالي**.
8. في تبويب **الأعضاء**:
   - اختر **مستخدم، مجموعة، أو كيان خدمة**.
   - انقر على **+ اختيار الأعضاء**.
   - ابحث عن اسمك أو بريدك الإلكتروني.
   - اختر نفسك من النتائج.
   - انقر على **اختيار**.
9. انقر على **مراجعة + تعيين** → ثم **مراجعة + تعيين** مرة أخرى.
10. **انتظر 1-2 دقيقة** - تستغرق تغييرات RBAC وقتًا للتطبيق.
11. أعد محاولة العملية التي فشلت.

> **لماذا دور Owner/Contributor غير كافٍ:** لدى Azure RBAC نوعان من الأذونات - *إجراءات الإدارة* و*إجراءات البيانات*. يمنح Owner وContributor إجراءات الإدارة (إنشاء الموارد، تحرير الإعدادات)، لكن عمليات الوكيل تتطلب إذن `agents/write` وهو **إجراء بيانات** ضمن أدوار `Azure AI User` أو `Azure AI Developer` أو `Azure AI Owner` فقط. راجع [مستندات Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` أثناء توفير المورد

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**السبب الجذري:** ليس لديك إذن لإنشاء أو تعديل موارد Azure في هذه الاشتراك/مجموعة الموارد.

**الإصلاح:**
1. اطلب من مسؤول الاشتراك تعيين دور **المساهم** لك على مجموعة الموارد التي يعيش فيها مشروع Foundry الخاص بك.
2. بدلاً من ذلك، اطلب منهم إنشاء مشروع Foundry لك ومنحك دور **Azure AI User** على المشروع.

### 1.3 `SubscriptionNotRegistered` لـ [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**السبب الجذري:** لم يتم تسجيل مزود المورد اللازم لـ Foundry في اشتراك Azure.

**الإصلاح:**

1. افتح محطة أوامر وشغّل:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. انتظر حتى تكتمل عملية التسجيل (قد تستغرق من 1 إلى 5 دقائق):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   الناتج المتوقع: `"Registered"`
3. أعد محاولة العملية.

---

## 2. أخطاء Docker (فقط إذا تم تثبيت Docker)

> Docker **اختياري** لهذه الورشة. تنطبق هذه الأخطاء فقط إذا كان لديك Docker Desktop مثبتًا وحاول امتداد Foundry بناء الحاوية محليًا.

### 2.1 خدمة Docker daemon غير مشغلة

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**الإصلاح - خطوة بخطوة:**

1. **ابحث عن Docker Desktop** في قائمة ابدأ (ويندوز) أو التطبيقات (macOS) وشغِّله.
2. انتظر حتى تظهر نافذة Docker Desktop مع الرسالة **"Docker Desktop is running"** - عادة ما تستغرق 30-60 ثانية.
3. ابحث عن أيقونة الحوت الخاصة بـ Docker في علبة النظام (ويندوز) أو شريط القوائم (macOS). مرّر المؤشر فوقها للتحقق من حالتها.
4. تحقق من خلال الطرفية:
   ```powershell
   docker info
   ```
   إذا طُبعت معلومات نظام Docker (إصدار الخادم، برنامج التخزين، إلخ)، فهذا يعني أن Docker يعمل.
5. **لنظام ويندوز فقط:** إذا لم يبدأ Docker:
   - افتح Docker Desktop → **الإعدادات** (رمز الترس) → **عام**.
   - تأكد من تفعيل **Use the WSL 2 based engine**.
   - انقر **تطبيق وإعادة تشغيل**.
   - إذا لم يكن WSL 2 مثبتًا، شغّل `wsl --install` في PowerShell بصلاحيات مرتفعة وأعد تشغيل الكمبيوتر.
6. أعد محاولة النشر.

### 2.2 فشل بناء Docker بأخطاء تبعيات

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**الإصلاح:**
1. افتح ملف `requirements.txt` وتحقق من صحة أسماء الحزم.
2. تأكد من صحة تحديد الإصدارات:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. اختبر التثبيت محليًا أولاً:
   ```bash
   pip install -r requirements.txt
   ```
4. إذا كنت تستخدم مستودع حزم خاص، فتأكد من أن Docker لديه وصول إلى الشبكة الخاصة به.

### 2.3 تعارض منصة الحاوية (Apple Silicon)

إذا كنت تنشر من جهاز Mac بمعالج Apple Silicon (M1/M2/M3/M4)، يجب بناء الحاوية لمنصة `linux/amd64` لأن وقت تشغيل الحاوية في Foundry يستخدم AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> أمر النشر الخاص بامتداد Foundry يدير هذا تلقائيًا في معظم الحالات. إذا رأيت أخطاء مرتبطة بالمعمارية، قم بالبناء يدويًا باستخدام العلم `--platform` واتصل بفريق Foundry.

---

## 3. أخطاء المصادقة

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) تفشل في استرداد رمز

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**السبب الجذري:** لا يوجد مصدر تصريح في سلسلة `DefaultAzureCredential` يمتلك رمزًا صالحًا.

**الإصلاح - جرب كل خطوة بالترتيب:**

1. **إعادة تسجيل الدخول عبر Azure CLI** (الإصلاح الأكثر شيوعًا):
   ```bash
   az login
   ```
   تفتح نافذة متصفح. سجل دخولك ثم عد إلى VS Code.

2. **تعيين الاشتراك الصحيح:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   إذا لم يكن هذا الاشتراك هو الصحيح:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **إعادة تسجيل الدخول عبر VS Code:**
   - انقر على أيقونة **الحسابات** (رمز الشخص) في أسفل يسار VS Code.
   - انقر على اسم حسابك → **تسجيل الخروج**.
   - انقر مرة أخرى على أيقونة الحسابات → **تسجيل الدخول إلى Microsoft**.
   - أكمل تدفق تسجيل الدخول في المتصفح.

4. **كيان الخدمة (لحالات CI/CD فقط):**
   - عيّن متغيرات البيئة هذه في `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - ثم أعد تشغيل عملية الوكيل.

5. **تحقق من ذاكرة التخزين المؤقت للرمز:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   إذا فشل هذا، فإن رمز CLI الخاص بك قد انتهت صلاحيته. نفذ `az login` مرة أخرى.

### 3.2 يعمل الرمز محليًا لكن ليس في النشر المستضاف

**السبب الجذري:** يستخدم الوكيل المستضاف هوية مُدارة من النظام، مختلفة عن بيانات اعتمادك الشخصية.

**الإصلاح:** هذا سلوك متوقع - يتم تجهيز الهوية المُدارة تلقائيًا أثناء النشر. إذا استمر حصول الوكيل المستضاف على أخطاء مصادقة:
1. تحقق من أن هوية المشروع المُدارة في Foundry تمتلك حق الوصول إلى مورد Azure OpenAI.
2. تحقق من أن `PROJECT_ENDPOINT` في `agent.yaml` صحيح.

---

## 4. أخطاء النموذج

### 4.1 لم يتم العثور على نشر النموذج

```
Error: Model deployment not found / The specified deployment does not exist
```

**الإصلاح - خطوة بخطوة:**

1. افتح ملف `.env` ولاحظ قيمة `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. افتح الشريط الجانبي لـ **Microsoft Foundry** في VS Code.
3. وسّع مشروعك → **نشرات النموذج**.
4. قارن اسم النشر المدرج هناك مع القيمة في `.env`.
5. الاسم **حساس لحالة الأحرف** - `gpt-4o` مختلف عن `GPT-4o`.
6. إذا لم يطابقا، حدّث `.env` لاستخدام الاسم الدقيق المعروض في الشريط الجانبي.
7. للنشر المستضاف، حدّث أيضًا `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 استجابة النموذج بمحتوى غير متوقع

**الإصلاح:**
1. راجع الثابت `EXECUTIVE_AGENT_INSTRUCTIONS` في `main.py`. تأكد من عدم قطعه أو تلفه.
2. تحقق من إعداد درجة حرارة النموذج (إن كانت قابلة للتعديل) - القيم الأقل تقدم مخرجات أكثر حتمية.
3. قارن بين النموذج المنشور (مثلاً `gpt-4o` مقابل `gpt-4o-mini`) - النماذج المختلفة لديها قدرات مختلفة.

---

## 5. أخطاء النشر

### 5.1 تفويض سحب ACR

```
Error: AcrPullUnauthorized
```

**السبب الجذري:** لا تستطيع الهوية المُدارة لمشروع Foundry سحب صورة الحاوية من سجل Azure Container Registry.

**الإصلاح - خطوة بخطوة:**

1. افتح [https://portal.azure.com](https://portal.azure.com).
2. ابحث عن **[سجلات الحاويات](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** في شريط البحث الأعلى.
3. انقر على السجل المرتبط بمشروع Foundry الخاص بك (عادة ما يكون في نفس مجموعة الموارد).
4. في التنقل الأيسر، انقر على **التحكم في الوصول (IAM)**.
5. انقر على **+ إضافة** → **إضافة تعيين دور**.
6. ابحث عن **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** واختره. انقر على **التالي**.
7. اختر **الهوية المُدارة** → انقر على **+ اختيار الأعضاء**.
8. ابحث وحدد هوية المشروع المُدارة في Foundry.
9. انقر على **اختيار** → **مراجعة + تعيين** → **مراجعة + تعيين**.

> يتم عادة إعداد هذا التعيين تلقائيًا بواسطة امتداد Foundry. إذا رأيت هذا الخطأ، قد يكون الإعداد التلقائي قد فشل. يمكنك أيضًا محاولة إعادة النشر - قد يعيد الامتداد محاولة الإعداد.

### 5.2 فشل الوكيل في البدء بعد النشر

**الأعراض:** يبقى حالة الحاوية "قيد الانتظار" لأكثر من 5 دقائق أو تظهر "فشل".

**الإصلاح - خطوة بخطوة:**

1. افتح الشريط الجانبي لـ **Microsoft Foundry** في VS Code.
2. انقر على الوكيل المستضاف الخاص بك → اختر الإصدار.
3. في لوحة التفاصيل، تحقق من **تفاصيل الحاوية** → ابحث عن قسم أو رابط **السجلات**.
4. اقرأ سجلات بدء الحاوية. الأسباب الشائعة:

| رسالة السجل | السبب | الإصلاح |
|-------------|-------|---------|
| `ModuleNotFoundError: No module named 'xxx'` | تبعية مفقودة | أضفها إلى `requirements.txt` وأعد النشر |
| `KeyError: 'PROJECT_ENDPOINT'` | متغير بيئة مفقود | أضف متغير البيئة إلى `agent.yaml` ضمن `env:` |
| `OSError: [Errno 98] Address already in use` | تعارض المنفذ | تأكد أن `agent.yaml` يحتوي `port: 8088` ويكون هناك عملية واحدة فقط تستخدمه |
| `ConnectionRefusedError` | الوكيل لم يبدأ بالاستماع | تحقق من `main.py` - يجب أن يتم استدعاء `from_agent_framework()` عند بدء التشغيل |

5. أصلح المشكلة، ثم أعد النشر من [الوحدة 6](06-deploy-to-foundry.md).

### 5.3 انتهاء مهلة النشر

**الإصلاح:**
1. تحقق من اتصال الإنترنت - دفع Docker قد يكون كبيرًا (>100 ميجابايت للنشر الأول).
2. إذا كنت خلف وكيل شركي، تأكد من إعدادات وكيل Docker Desktop: **Docker Desktop** → **الإعدادات** → **الموارد** → **الوكلاء**.
3. حاول مجددًا - قد تتسبب مشاكل الشبكة العابرة في فشل مؤقت.

---

## 6. مرجع سريع: أدوار RBAC

| الدور | النطاق النموذجي | ما يمنحه |
|------|-----------------|-----------|
| **Azure AI User** | المشروع | إجراءات البيانات: بناء، نشر، واستدعاء الوكلاء (`agents/write`, `agents/read`) |
| **Azure AI Developer** | المشروع أو الحساب | إجراءات البيانات + إنشاء المشاريع |
| **Azure AI Owner** | الحساب | الوصول الكامل + إدارة تعيين الأدوار |
| **Azure AI Project Manager** | المشروع | إجراءات البيانات + يمكنه تعيين دور Azure AI User للآخرين |
| **Contributor** | الاشتراك/مجموعة الموارد | إجراءات الإدارة (إنشاء/حذف الموارد). **لا يشمل إجراءات البيانات** |
| **Owner** | الاشتراك/مجموعة الموارد | إجراءات الإدارة + تعيين الأدوار. **لا يشمل إجراءات البيانات** |
| **Reader** | أي | وصول إدارة قراءة فقط |

> **النقطة الأساسية:** لا يشمل دور `Owner` و `Contributor` إجراءات البيانات. تحتاج دائمًا إلى دور `Azure AI *` لعمليات الوكيل. الحد الأدنى للدور لهذه الورشة هو **Azure AI User** على مستوى **المشروع**.

---

## 7. قائمة مراجعة إكمال الورشة

استخدم هذه كعلامة نهائية على أنك أكملت كل شيء:

| # | العنصر | الوحدة | اجتياز؟ |
|---|---------|---------|---------|
| 1 | تثبيت والتحقق من كل المتطلبات المسبقة | [00](00-prerequisites.md) | |
| 2 | تثبيت Toolkit وامتدادات Foundry | [01](01-install-foundry-toolkit.md) | |
| 3 | إنشاء مشروع Foundry (أو اختيار مشروع موجود) | [02](02-create-foundry-project.md) | |
| 4 | تم نشر النموذج (مثل gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | تم تعيين دور مستخدم Azure AI على نطاق المشروع | [02](02-create-foundry-project.md) | |
| 6 | تم إعداد مشروع العميل المستضاف (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | تم تكوين `.env` مع PROJECT_ENDPOINT و MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | تم تخصيص تعليمات العميل في main.py | [04](04-configure-and-code.md) | |
| 9 | تم إنشاء البيئة الافتراضية وتثبيت التبعيات | [04](04-configure-and-code.md) | |
| 10 | تم اختبار العميل محليًا باستخدام F5 أو الطرفية (تم اجتياز 4 اختبارات أولية) | [05](05-test-locally.md) | |
| 11 | تم النشر في خدمة Foundry Agent | [06](06-deploy-to-foundry.md) | |
| 12 | حالة الحاوية تظهر "Started" أو "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | تم التحقق في VS Code Playground (تم اجتياز 4 اختبارات أولية) | [07](07-verify-in-playground.md) | |
| 14 | تم التحقق في Foundry Portal Playground (تم اجتياز 4 اختبارات أولية) | [07](07-verify-in-playground.md) | |

> **تهانينا!** إذا تم التحقق من جميع العناصر، فقد أكملت ورشة العمل بأكملها. لقد أنشأت عميلًا مستضافًا من الصفر، وقمت باختباره محليًا، ونشرته على Microsoft Foundry، وتحققته في الإنتاج.

---

**السابق:** [07 - التحقق في ساحة اللعب](07-verify-in-playground.md) · **الرئيسية:** [ورشة العمل README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**إخلاء المسؤولية**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى للدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والموثوق. بالنسبة للمعلومات الهامة، يُوصى بالاستعانة بالترجمة البشرية المهنية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناجم عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->