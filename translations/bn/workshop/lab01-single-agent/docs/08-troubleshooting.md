# মডিউল ৮ - সমস্যার সমাধান

এই মডিউলটি সাধারণ সমস্যাগুলির জন্য একটি রেফারেন্স গাইড। এটিকে বুকমার্ক করুন এবং কিছু ভুল হলে ফিরে আসুন।

---

## ১. অনুমতি ত্রুটি

### ১.১ `agents/write` অনুমতি প্রত্যাখ্যাত

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**মূল কারণ:** **প্রজেক্ট** স্তরে `Azure AI User` ভূমিকা অনুপস্থিত। এটি #1 কর্মশালা ত্রুটি।

**সমাধান:**
১. [portal.azure.com](https://portal.azure.com) খুলুন।
২. আপনার Foundry **প্রজেক্ট** নাম অনুসন্ধান করুন → **"Microsoft Foundry project"** টাইপের ফলাফলের উপর ক্লিক করুন (parent account নয়)।
৩. **Access control (IAM)** → **+ Add** → **Add role assignment**।
৪. ভূমিকা: **Azure AI User** → Next।
৫. সদস্যরা: নিজেকে নির্বাচন করুন → Review + assign → Review + assign।
৬. **১–২ মিনিট অপেক্ষা করুন** → পুনরায় চেষ্টা করুন।

> **কেন Owner/Contributor যথেষ্ট নয়:** এই ভূমিকাগুলি কেবল *management* ক্রিয়াকলাপের অনুমতি দেয়। এজেন্ট অপারেশনগুলি `agents/write` *data action* প্রয়োজন, যা শুধুমাত্র `Azure AI User`, `Azure AI Developer`, বা `Azure AI Owner` তে থাকে। দেখুন [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)।

### ১.২ Provisioning সময় `AuthorizationFailed`

**সমাধান:** আপনার অ্যাডমিনকে রিসোর্স গ্রুপে **Contributor** অ্যাসাইন করতে বলুন, অথবা তারা আপনার জন্য প্রজেক্ট তৈরি করে আপনারকে তাতে **Azure AI User** দিয়ে দিন।

### ১.৩ `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# পর্যন্ত অপেক্ষা করুন: "নিবন্ধিত"
```

---

## ২. ডকার ত্রুটি

> ডকার **বিকল্প**। এগুলি কেবল তখনই প্রযোজ্য যখন Docker Desktop ইনস্টল করা থাকে এবং এক্সটেনশন একটি লোকাল বিল্ড চেষ্টা করে।

### ২.১ Docker daemon চালু নেই

**সমাধান:** Docker Desktop চালু করুন → "running" অবস্থা পর্যন্ত অপেক্ষা করুন → `docker info` দিয়ে যাচাই করুন → পুনরায় চেষ্টা করুন।

### ২.২ নির্ভরশীলতা ত্রুটিতে বিল্ড ব্যর্থ

**সমাধান:** `requirements.txt` এর বানান যাচাই করুন, প্রথমে লোকালি পরীক্ষা করুন: `pip install -r requirements.txt`।

### ২.৩ প্ল্যাটফর্ম মিল নেই (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## ৩. প্রমাণীকরণ ত্রুটি

### ৩.১ `DefaultAzureCredential` ব্যর্থ

**সমাধান (ক্রমে চেষ্টা করুন):**
১. `az login` (পুনরায় প্রমাণীকরণ)
২. `az account set --subscription "<id>"` (সঠিক সাবস্ক্রিপশন)
৩. VS Code → Accounts → Sign Out → আবার Sign In
৪. যাচাই করুন: `az account get-access-token --resource https://cognitiveservices.azure.com`

### ৩.২ টোকেন লোকাল কাজ করে কিন্তু হোস্টেড নয়

**প্রত্যাশিত:** হোস্টেড এজেন্টগুলি সিস্টেম-ব্যবস্থাপিত পরিচয় ব্যবহার করে, আপনার ক্রেডেনশিয়াল নয়। যদি হোস্টেড এজেন্ট auth ত্রুটি পায়:
- `agent.yaml` এ `AZURE_AI_PROJECT_ENDPOINT` সঠিক কিনা যাচাই করুন
- প্রজেক্টের ব্যবস্থাপিত পরিচয় মডেলের অ্যাক্সেস আছে কিনা চেক করুন

---

## ৪. মডেল ত্রুটি

### ৪.১ মডেল ডিপ্লয়মেন্ট পাওয়া যায়নি

**সমাধান:** নাম **কেস-সেনসিটিভ**। `.env` এ `AZURE_AI_MODEL_DEPLOYMENT_NAME` এবং ফাউন্ডরি সাইডবারে → Models এ সঠিক নাম তুলনা করুন।

### ৪.২ অপ্রত্যাশিত মডেল আউটপুট

**সমাধান:** `main.py` তে `AGENT_INSTRUCTIONS` পর্যালোচনা করুন (কোন অংশ কাটা পড়েনি কিনা)। একটি ভিন্ন মডেল চেষ্টা করুন (`gpt-4.1` বনাম `gpt-4.1-mini`)।

---

## ৫. ডিপ্লয়মেন্ট ত্রুটি

### ৫.১ ACR pull অনুমোদিত নয়

**সমাধান:** Azure Portal → Container Registry → Access control (IAM) → Foundry প্রকল্পের ব্যবস্থাপিত পরিচয়ে **AcrPull** ভূমিকা যোগ করুন।

### ৫.২ এজেন্ট শুরু করতে ব্যর্থ (থাকে "Pending" অথবা "Failed")

সাইডবারে কন্টেইনার লগ পরীক্ষা করুন। সাধারণ কারণ:

| লগ বার্তা | সমাধান |
|-------------|-----|
| `ModuleNotFoundError` | `requirements.txt` এ অনুপস্থিত প্যাকেজ যোগ করুন, পুনরায় ডিপ্লয় করুন |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | `agent.yaml` এর `environment_variables` এর জন্য env var যোগ করুন |
| `Address already in use` | নিশ্চিত করুন যে শুধু এক শতাংশ ৮০৮৮ পোর্টে বাঁধা দিচ্ছে |

### ৫.৩ ডিপ্লয়মেন্ট সময়সীমা শেষ

**সমাধান:** ইন্টারনেট সংযোগ চেক করুন। প্রথম ডিপ্লয়মেন্টে >১০০এমবি ডেটা পাঠানো হয়। প্রোক্সির পিছনে? Docker Desktop এর প্রোক্সি সেটিংস কনফিগার করুন।

---

## ৬. পাথ বি - Foundry Local

### ৬.১ Foundry Local চালু হয় না

| সমস্যা | সমাধান |
|-------|-----|
| `foundry: command not found` | পুনরায় ইনস্টল করুন: `winget install Microsoft.FoundryLocal` |
| অপর্যাপ্ত রিসোর্স | Foundry Local এর জন্য ~৪জিবি র‍্যাম খালি থাকতে হবে। অন্যান্য অ্যাপ বন্ধ করুন। |
| মডেল ডাউনলোড ব্যর্থ | ডিস্ক স্পেস চেক করুন (মডেল ২–৮ জিবি)। পুনরায় চেষ্টা করুন: `foundry local models pull <name>` |

### ৬.২ Foundry Local মডেল ত্রুটি

| সমস্যা | সমাধান |
|-------|-----|
| ধীর প্রতিক্রিয়া | প্রত্যাশিত - লোকাল মডেল CPU তে চলে যদি GPU না থাকে। ধৈর্য ধরুন। |
| কম মানের আউটপুট | আপনার হার্ডওয়্যার সামর্থ্য অনুযায়ী বড় মডেল চেষ্টা করুন। `phi-4-mini` ভালো সামঞ্জস্য। |
| সংযোগ প্রত্যাখ্যান | যাচাই করুন Foundry Local চলছে: `foundry local status`। প্রয়োজনে পুনরায় চালু করুন। |

---

## ৭. দ্রুত রেফারেন্স: RBAC ভূমিকা

| ভূমিকা | স্কোপ | অনুমতি |
|------|-------|--------|
| **Azure AI User** | প্রজেক্ট | ডেটা অ্যাকশন: `agents/write`, `agents/read` |
| **Azure AI Developer** | প্রজেক্ট/অ্যাকাউন্ট | ডেটা অ্যাকশন + প্রজেক্ট তৈরি |
| **Azure AI Owner** | অ্যাকাউন্ট | পূর্ণ অ্যাক্সেস + ভূমিকা পরিচালনা |
| **Contributor** | সাবস্ক্রিপশন/আরজি | শুধুমাত্র ব্যবস্থাপনা ক্রিয়া (**কোনো** ডেটা অ্যাকশন নয়) |
| **Owner** | সাবস্ক্রিপশন/আরজি | ব্যবস্থাপনা + ভূমিকা নির্ধারণ (**কোনো** ডেটা অ্যাকশন নয়) |

---

## ৮. কর্মশালা সম্পাদনার চেকলিস্ট

| # | আইটেম | মডিউল |
|---|------|--------|
| ১ | প্রয়োজনীয়তা ইনস্টল ও যাচাই | [00](00-prerequisites.md) |
| ২ | Foundry Toolkit এক্সটেনশন ইনস্টল, প্রজেক্ট সংযুক্ত (অথবা পাথ বি কনফিগার করা) | [01](01-setup.md) |
| ৩ | হোস্টেড এজেন্ট তৈরি | [02](02-create-hosted-agent.md) |
| ৪ | `.env` কনফিগার, নির্দেশনা লেখা, নির্ভরশীলতা ইনস্টল | [03](03-configure-and-code.md) |
| ৫ | এজেন্ট লোকালি পরীক্ষা - ৩টি কার্যকরী পরিস্থিতি পাস | [04](04-test-locally.md) |
| ৬ | Foundry তে ডিপ্লয় (শুধুমাত্র পাথ এ) | [05](05-deploy-to-foundry.md) |
| ৭ | ক্লাউডে এজ অফ কেস/সুরক্ষা পরীক্ষা পাস (শুধুমাত্র পাথ এ) | [06](06-verify-in-playground.md) |
| ৮ | সারাংশ পর্যালোচনা, পরবর্তী ধাপ নির্ধারণ | [07](07-summary.md) |

---

**পূর্বের:** [07 - সারাংশ](07-summary.md) · **হোম:** [কর্মশালা README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা শুদ্ধতার জন্য চেষ্টা করি, অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার স্বভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে প্রয়োজনীয় ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়বদ্ধ নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->