# Module 8 - সমস্যা নির্ণয়

এই মডিউলটি ওয়ার্কশপ চলাকালীন সবচেয়ে সাধারণ প্রতিটি সমস্যার জন্য একটি রেফারেন্স গাইড। এটি বুকমার্ক করুন - কিছু ভুল হলে আপনি এটি আবার দেখতে পারবেন।

---

## 1. অনুমতি ত্রুটি

### 1.1 `agents/write` অনুমতি অস্বীকার

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**মূল কারণ:** আপনার কাছে **প্রকল্প** স্তরে `Azure AI User` ভূমিকা নেই। এটি ওয়ার্কশপে সবচেয়ে সাধারণ ত্রুটি।

**সমাধান - ধাপে ধাপে:**

1. [https://portal.azure.com](https://portal.azure.com) খুলুন।
2. উপরের অনুসন্ধান বারে আপনার **Foundry প্রকল্প** এর নাম লিখুন (যেমন, `workshop-agents`)।
3. **গুরুত্বপূর্ণ:** "Microsoft Foundry project" ধরণের ফলাফলটি ক্লিক করুন, পিতামাতা অ্যাকাউন্ট/হাব রিসোর্স নয়। এগুলো বিভিন্ন RBAC স্কোপ সহ ভিন্ন রিসোর্স।
4. প্রকল্প পৃষ্ঠার বাম দিকের নেভিগেশনে **Access control (IAM)** ক্লিক করুন।
5. **Role assignments** ট্যাবে ক্লিক করে দেখুন আপনি ইতিমধ্যেই ভূমিকা পেয়েছেন কি না:
   - আপনার নাম বা ইমেল অনুসন্ধান করুন।
   - যদি `Azure AI User` তালিকাভুক্ত থাকে → ত্রুটির অন্য কারণ আছে (নীচের ধাপে পরীক্ষা করুন)।
   - না থাকলে → এটি যোগ করার জন্য এগিয়ে যান।
6. **+ Add** → **Add role assignment** ক্লিক করুন।
7. **Role** ট্যাবে:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) অনুসন্ধান করুন।
   - ফলাফলে এটি নির্বাচন করুন।
   - **Next** ক্লিক করুন।
8. **Members** ট্যাবে:
   - **User, group, or service principal** নির্বাচন করুন।
   - **+ Select members** ক্লিক করুন।
   - আপনার নাম বা ইমেল ঠিকানা অনুসন্ধান করুন।
   - ফলাফল থেকে নিজেকে নির্বাচন করুন।
   - **Select** ক্লিক করুন।
9. **Review + assign** → আবার **Review + assign** ক্লিক করুন।
10. **১-২ মিনিট অপেক্ষা করুন** - RBAC পরিবর্তনগুলি ছড়াতে সময় লাগে।
11. যে অপারেশনটি ব্যর্থ হয়েছে এটি পুনরায় চেষ্টা করুন।

> **কেন Owner/Contributor যথেষ্ট নয়:** Azure RBAC এর দুটি অনুমতির ধরণ থাকে - *management actions* এবং *data actions*। Owner ও Contributor ম্যানেজমেন্ট অ্যাকশন দেয় (রিসোর্স তৈরি, সেটিংস সম্পাদনা), কিন্তু agent অপারেশনগুলি `agents/write` **ডেটা অ্যাকশন** প্রয়োজন, যা শুধুমাত্র `Azure AI User`, `Azure AI Developer`, বা `Azure AI Owner` রোলে রয়েছে। দেখুন [Foundry RBAC ডকুমেন্টেশন](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)।

### 1.2 রিসোর্স প্রোভিশনিং সময় `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**মূল কারণ:** আপনার কাছে এই সাবস্ক্রিপশন/রিসোর্স গ্রুপে Azure রিসোর্স তৈরি বা পরিবর্তনের অনুমতি নেই।

**সমাধান:**
1. আপনার সাবস্ক্রিপশন প্রশাসককে অনুরোধ করুন যে তারা রিসোর্স গ্রুপের উপর আপনাকে **Contributor** ভূমিকা দিন যেখানে Foundry প্রকল্প অবস্থিত।
2. বিকল্পভাবে, তাদের দ্বারা Foundry প্রকল্প তৈরি করে আপনাকে প্রকল্পে **Azure AI User** ভূমিকা প্রদান করতে বলুন।

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) এর জন্য `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**মূল কারণ:** Azure সাবস্ক্রিপশনটি Foundry এর জন্য প্রয়োজনীয় রিসোর্স প্রদানকারী নিবন্ধিত হয়নি।

**সমাধান:**

1. একটি টার্মিনাল খুলুন এবং চালান:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. নিবন্ধন সম্পন্ন হওয়ার জন্য অপেক্ষা করুন (১-৫ মিনিট লাগতে পারে):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   প্রত্যাশিত আউটপুট: `"Registered"`
3. অপারেশনটি পুনরায় চেষ্টা করুন।

---

## 2. Docker ত্রুটি (শুধু Docker ইনস্টল করা থাকলে)

> Docker এই ওয়ার্কশপের জন্য **বিকল্প**। এই ত্রুটিগুলো শুধুমাত্র তখনই প্রযোজ্য যখন আপনার Docker Desktop ইনস্টল করা থাকে এবং Foundry এক্সটেনশন একটি স্থানীয় কনটেইনার বিল্ড করার চেষ্টা করে।

### 2.1 Docker daemon চলছে না

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**সমাধান - ধাপে ধাপে:**

1. আপনার Start মেনু (Windows) বা Applications (macOS) থেকে **Docker Desktop** খুঁজে চালু করুন।
2. অপেক্ষা করুন Docker Desktop উইন্ডোতে **"Docker Desktop is running"** দেখাতে - সাধারণত ৩০-৬০ সেকেন্ড সময় লাগে।
3. আপনার সিস্টেম ট্রে (Windows) বা মেনু বার (macOS) এ Docker হোয়েল আইকন খুঁজুন। এর উপর কারসর রেখে অবস্থা যাচাই করুন।
4. একটি টার্মিনালে যাচাই করুন:
   ```powershell
   docker info
   ```
   যদি এটি Docker সিস্টেম তথ্য (Server Version, Storage Driver, ইত্যাদি) প্রদর্শন করে, Docker চলছে।
5. **Windows বিশেষ:** যদি Docker এখনও শুরু না হয়:
   - Docker Desktop → **Settings** (গিয়ার আইকন) → **General** খুলুন।
   - নিশ্চিত করুন **Use the WSL 2 based engine** নির্বাচিত আছে।
   - **Apply & restart** ক্লিক করুন।
   - যদি WSL 2 ইনস্টল না থাকে, একটি প্রশাসনিক PowerShell এ `wsl --install` চালান এবং আপনার কম্পিউটার রিস্টার্ট করুন।
6. ডিপ্লয়মেন্ট পুনরায় চেষ্টা করুন।

### 2.2 Docker বিল্ড নির্ভরতা ত্রুটি নিয়ে ব্যর্থ

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**সমাধান:**
1. `requirements.txt` খুলে নিশ্চিত করুন সব প্যাকেজ নাম সঠিক বানানে আছে।
2. ভার্সন পিনিং সঠিক কিনা দেখুন:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. প্রথমে লোকালি ইনস্টলেশন পরীক্ষা করুন:
   ```bash
   pip install -r requirements.txt
   ```
4. যদি প্রাইভেট প্যাকেজ ইনডেক্স ব্যবহার করেন, নিশ্চিত করুন Docker এর কাছে তার নেটওয়ার্ক অ্যাক্সেস আছে।

### 2.3 কনটেইনার প্ল্যাটফর্ম অসঙ্গতি (Apple Silicon)

যদি Apple Silicon Mac (M1/M2/M3/M4) থেকে ডিপ্লয় করছেন, কনটেইনার অবশ্যই `linux/amd64` এর জন্য তৈরি হতে হবে কারণ Foundry এর কনটেইনার রানটাইম AMD64 ব্যবহার করে।

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry এক্সটেনশনের deploy কমান্ড অধিকাংশ ক্ষেত্রে এটি স্বয়ংক্রিয়ভাবে পরিচালনা করে। যদি স্থাপত্য-সংক্রান্ত ত্রুটি আসে, তাহলে ম্যানুয়ালি `--platform` ফ্ল্যাগ দিয়ে বিল্ড করুন এবং Foundry টিমের সাথে যোগাযোগ করুন।

---

## 3. প্রমাণীকরণ ত্রুটি

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) টোকেন পেতে ব্যর্থ

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**মূল কারণ:** `DefaultAzureCredential` চেইনের কোনো ক্রেডেনশিয়াল সোর্সের বৈধ টোকেন নেই।

**সমাধান - প্রতিটি ধাপ চেষ্টা করুন:**

1. **Azure CLI দিয়ে পুনরায় লগইন করুন** (সবচেয়ে সাধারণ সমাধান):
   ```bash
   az login
   ```
   একটি ব্রাউজার উইন্ডো খুলবে। সাইন ইন করুন, তারপর VS Code এ ফিরে আসুন।

2. **সঠিক সাবস্ক্রিপশন সিলেক্ট করুন:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   যদি এটি সঠিক সাবস্ক্রিপশন না হয়:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code থেকে পুনরায় লগইন করুন:**
   - VS Code এর নিচের বাম কোণের **Accounts** আইকনে ক্লিক করুন।
   - আপনার একাউন্ট নাম ক্লিক করে → **Sign Out** করুন।
   - আবার Accounts আইকনে ক্লিক করে → **Sign in to Microsoft**।
   - ব্রাউজার সাইন-ইন সম্পন্ন করুন।

4. **সার্ভিস প্রিন্সিপাল (শুধু CI/CD ক্ষেত্রে):**
   - আপনার `.env` ফাইলে এই পরিবেশ চলকগুলো সেট করুন:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - তারপর আপনার এজেন্ট প্রসেস রিস্টার্ট করুন।

5. **টোকেন ক্যাশ পরীক্ষা করুন:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   যদি ব্যর্থ হয়, আপনার CLI টোকেনের মেয়াদ উত্তীর্ণ হয়েছে। আবার `az login` চালান।

### 3.2 টোকেন লোকালি কাজ করে কিন্তু হোস্টেড ডিপ্লয়মেন্টে নয়

**মূল কারণ:** হোস্টেড এজেন্ট একটি সিস্টেম-পরিচালিত আইডেন্টিটি ব্যবহার করে, যা আপনার ব্যক্তিগত ক্রেডেনশিয়াল থেকে আলাদা।

**সমাধান:** এটি প্রত্যাশিত আচরণ - ব্যবস্থাপিত আইডেন্টিটি ডিপ্লয়মেন্টের সময় স্বয়ংক্রিয়ভাবে উত্পাদিত হয়। হোস্টেড এজেন্ট যদি এখনো অথ ত্রুটি পায়:
1. Foundry প্রকল্পের ব্যবস্থাপিত আইডেন্টিটি Azure OpenAI রিসোর্স অ্যাক্সেস আছে কিনা যাচাই করুন।
2. `agent.yaml`-এ `PROJECT_ENDPOINT` সঠিক কিনা নিশ্চিত করুন।

---

## 4. মডেল ত্রুটি

### 4.1 মডেল ডিপ্লয়মেন্ট পাওয়া যায়নি

```
Error: Model deployment not found / The specified deployment does not exist
```

**সমাধান - ধাপে ধাপে:**

1. আপনার `.env` ফাইলটি খুলে `AZURE_AI_MODEL_DEPLOYMENT_NAME` এর মান নোট করুন।
2. VS Code এ **Microsoft Foundry** সাইডবার খুলুন।
3. আপনার প্রকল্প বিস্তৃত করুন → **Model Deployments** এ প্রবেশ করুন।
4. অন্যান্য ডিপ্লয়মেন্ট নাম আপনার `.env`-এর সাথে মিলিয়ে দেখুন।
5. নাম **কেস সংবেদনশীল** - `gpt-4o` এবং `GPT-4o` আলাদা।
6. যদি তারা মেলেনা, আপনার `.env` ফাইলে সাইডবারে প্রদর্শিত সঠিক নাম লিখুন।
7. হোস্টেড ডিপ্লয়মেন্টের জন্য, `agent.yaml` আপডেট করুন:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 মডেল অনাকাঙ্ক্ষিত বিষয়বস্তু দিয়ে প্রতিক্রিয়া দেয়

**সমাধান:**
1. `main.py` এ `EXECUTIVE_AGENT_INSTRUCTIONS` ধ্রুবকটি পর্যালোচনা করুন। নিশ্চিত করুন এটি সংক্ষিপ্তকৃত বা ক্ষতিগ্রস্থ হয়নি।
2. মডেল টেম্পারেচার সেটিং পরীক্ষা করুন (যদি কনফিগারেবল হয়) - নিম্ন মান বেশি নির্ধারিত আউটপুট দেয়।
3. ডিপ্লয় করা মডেল তুলনা করুন (যেমন `gpt-4o` বনাম `gpt-4o-mini`) - বিভিন্ন মডেলের ক্ষমতা ভিন্ন।

---

## 5. ডিপ্লয়মেন্ট ত্রুটি

### 5.1 ACR পুল অনুমোদন

```
Error: AcrPullUnauthorized
```

**মূল কারণ:** Foundry প্রকল্পের ব্যবস্থাপিত আইডেন্টিটি Azure Container Registry থেকে কনটেইনার ইমেজ টেনে নিতে পারে না।

**সমাধান - ধাপে ধাপে:**

1. [https://portal.azure.com](https://portal.azure.com) খুলুন।
2. উপরের অনুসন্ধান বারে **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** অনুসন্ধান করুন।
3. আপনার Foundry প্রকল্পের সাথে সংযুক্ত রেজিস্ট্রি ক্লিক করুন (সাধারণত একই রিসোর্স গ্রুপে অবস্থিত)।
4. বাম নেভিগেশনে **Access control (IAM)** ক্লিক করুন।
5. **+ Add** → **Add role assignment** ক্লিক করুন।
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** অনুসন্ধান করে নির্বাচন করুন। **Next** ক্লিক করুন।
7. **Managed identity** নির্বাচন করুন → **+ Select members** ক্লিক করুন।
8. Foundry প্রকল্পের ব্যবস্থাপিত আইডেন্টিটি খুঁজে নির্বাচন করুন।
9. **Select** → **Review + assign** → আরেকবার **Review + assign** করুন।

> এই ভূমিকা স্বয়ংক্রিয়ভাবে Foundry এক্সটেনশন দ্বারা গঠন করা হয়ে থাকে। যদি এই ত্রুটি আসে, স্বয়ংক্রিয় সেটআপ ব্যর্থ হয়েছে। পুনরায় ডিপ্লয় করার চেষ্টা করুন - এক্সটেনশন সেটআপটি পুনরায় চেষ্টা করতে পারে।

### 5.2 ডিপ্লয়মেন্টের পর এজেন্ট শুরু হয় না

**লক্ষণ:** কনটেইনারের অবস্থা "Pending" ৫ মিনিটের বেশি থাকে বা "Failed" দেখায়।

**সমাধান - ধাপে ধাপে:**

1. VS Code এ **Microsoft Foundry** সাইডবার খুলুন।
2. আপনার হোস্টেড এজেন্ট ক্লিক করুন → সংস্করণ নির্বাচন করুন।
3. বিস্তারিত প্যানেলে **Container Details** দেখুন → **Logs** সেকশন বা লিঙ্ক খুঁজুন।
4. কনটেইনার স্টার্টআপ লগ পড়ুন। সাধারণ কারণসমূহ:

| লগ বার্তা | কারণ | সমাধান |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | নির্ভরতা অনুপস্থিত | `requirements.txt`-এ যোগ করুন এবং পুনরায় ডিপ্লয় করুন |
| `KeyError: 'PROJECT_ENDPOINT'` | পরিবেশ চলক অনুপস্থিত | `agent.yaml`-এ `env:` এর নিচে env var যোগ করুন |
| `OSError: [Errno 98] Address already in use` | পোর্ট সংঘাত | নিশ্চিত করুন `agent.yaml`-এ `port: 8088` আছে এবং শুধু একটি প্রসেস এটি ব্যবহার করছে |
| `ConnectionRefusedError` | এজেন্ট শোনা শুরু করেনি | `main.py` পরীক্ষা করুন - `from_agent_framework()` কল শুরুতেই 실행 হওয়া উচিত |

5. সমস্যা সমাধান করুন, তারপরে [Module 6](06-deploy-to-foundry.md) থেকে পুনরায় ডিপ্লয় করুন।

### 5.3 ডিপ্লয়মেন্ট টাইমআউট

**সমাধান:**
1. আপনার ইন্টারনেট সংযোগ পরীক্ষা করুন - Docker push বড় হতে পারে (>১০০ এমবি প্রথম ডিপ্লয়ের জন্য)।
2. যদি কর্পোরেট প্রক্সি ব্যবহার করেন, নিশ্চিত করুন Docker Desktop প্রক্সি সেটিংস সেট আছে: **Docker Desktop** → **Settings** → **Resources** → **Proxies**।
3. আবার চেষ্টা করুন - নেটওয়ার্ক সমস্যা সাময়িক ব্যর্থতার কারণ হতে পারে।

---

## 6. দ্রুত রেফারেন্স: RBAC রোল

| ভূমিকা | সাধারণ স্কোপ | কী অনুমতি দেয় |
|------|---------------|----------------|
| **Azure AI User** | প্রকল্প | ডেটা অ্যাকশন: এজেন্ট তৈরি, ডিপ্লয় ও আহ্বান (`agents/write`, `agents/read`) |
| **Azure AI Developer** | প্রকল্প বা অ্যাকাউন্ট | ডেটা অ্যাকশন + প্রকল্প তৈরি |
| **Azure AI Owner** | অ্যাকাউন্ট | পূর্ণ প্রবেশাধিকার + রোল নিয়ন্ত্রণ |
| **Azure AI Project Manager** | প্রকল্প | ডেটা অ্যাকশন + অন্যদের Azure AI User দিতে পারে |
| **Contributor** | সাবস্ক্রিপশন/আরজি | ব্যবস্থাপনা অ্যাকশন (রিসোর্স তৈরি/মুছে ফেলা)। **ডেটা অ্যাকশন নেই** |
| **Owner** | সাবস্ক্রিপশন/আরজি | ব্যবস্থাপনা + রোল নিয়ন্ত্রণ। **ডেটা অ্যাকশন নেই** |
| **Reader** | যেকোনো | পড়ার অনুমতি মাত্র |

> **কী কথা:** `Owner` ও `Contributor` ডেটা অ্যাকশন অন্তর্ভুক্ত করে না। এজেন্ট অপারেশনের জন্য সর্বদা একটি `Azure AI *` ভূমিকা প্রয়োজন। এই ওয়ার্কশপের জন্য সর্বনিম্ন ভূমিকা হল প্রকল্প স্কোপের মধ্যে **Azure AI User**।

---

## 7. ওয়ার্কশপ সম্পন্ন চেকলিস্ট

সবকিছু সম্পন্ন করার চূড়ান্ত স্বীকৃতির জন্য এটি ব্যবহার করুন:

| # | আইটেম | মডিউল | পাশ? |
|---|------|--------|---|
| 1 | সমস্ত প্রাকশর্ত ইনস্টল ও যাচাই করা হয়েছে | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit এবং Foundry এক্সটেনশন ইনস্টল করা হয়েছে | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry প্রকল্প তৈরি করা হয়েছে (অথবা বিদ্যমান প্রকল্প নির্বাচন করা হয়েছে) | [02](02-create-foundry-project.md) | |
| 4 | মডেল স্থাপিত (যেমন, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | প্রকল্প সীমায় Azure AI ব্যবহারকারী ভূমিকা বরাদ্দ | [02](02-create-foundry-project.md) | |
| 6 | হোস্টেড এজেন্ট প্রকল্প স্ক্যাফোল্ড করা হয়েছে (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` কনফিগার করা হয়েছে PROJECT_ENDPOINT এবং MODEL_DEPLOYMENT_NAME সহ | [04](04-configure-and-code.md) | |
| 8 | Agent নির্দেশাবলী main.py তে কাস্টমাইজ করা হয়েছে | [04](04-configure-and-code.md) | |
| 9 | ভার্চুয়াল পরিবেশ তৈরি হয়েছে এবং ডিপেন্ডেন্সি ইনস্টল করা হয়েছে | [04](04-configure-and-code.md) | |
| 10 | Agent স্থানীয়ভাবে F5 বা টার্মিনাল দিয়ে পরীক্ষা করা হয়েছে (4 ধূমপান পরীক্ষা passed) | [05](05-test-locally.md) | |
| 11 | Foundry Agent সার্ভিসে স্থাপিত | [06](06-deploy-to-foundry.md) | |
| 12 | কন্টেইনারের অবস্থা "Started" অথবা "Running" দেখায় | [06](06-deploy-to-foundry.md) | |
| 13 | VS Code প্লেগ্রাউন্ডে যাচাই করা হয়েছে (4 ধূমপান পরীক্ষা passed) | [07](07-verify-in-playground.md) | |
| 14 | Foundry পোর্টাল প্লেগ্রাউন্ডে যাচাই করা হয়েছে (4 ধূমপান পরীক্ষা passed) | [07](07-verify-in-playground.md) | |

> **অভিনন্দন!** যদি সমস্ত আইটেম চিহ্নিত থাকে, তবে আপনি পুরো কর্মশালা সম্পন্ন করেছেন। আপনি স্ক্র্যাচ থেকে একটি হোস্টেড এজেন্ট তৈরি করেছেন, স্থানীয়ভাবে এটি পরীক্ষা করেছেন, Microsoft Foundry এ স্থাপন করেছেন, এবং প্রোডাকশনে যাচাই করেছেন।

---

**পূর্ববর্তী:** [07 - Verify in Playground](07-verify-in-playground.md) · **হোম:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকারোক্তি**:  
এই নথিটি AI অনুবাদ সেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। আমরা সঠিকতার জন্য চেষ্টা করি, তবে অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার নিজভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গভীর গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ প্রয়োজন। এই অনুবাদের ব্যবহারে কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->