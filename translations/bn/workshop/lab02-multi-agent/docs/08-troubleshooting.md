# মডিউল ৮ - সমস্যার সমাধান

এই মডিউলটি মাল্টি-অ্যাজেন্ট ওয়ার্কফ্লো সংক্রান্ত সাধারণ ত্রুটি, সমাধান এবং ডিবাগিং কৌশলগুলি আচ্ছাদিত করে।

## এজেন্ট আউটপুট সমস্যাগুলো

### GapAnalyzer বলে "আমার কাছে এখনও ম্যাচিং রিপোর্ট নেই"

**লক্ষণ:** GapAnalyzer এর প্রতিক্রিয়া আপনাকে “Missing Skills” এবং “Certification Gaps” সহ একটি ম্যাচিং রিপোর্ট পেস্ট করতে বলছে। এমনকি যখন আপনি একটি রিজিউম এবং একটি চাকরির বিবরণ পাঠিয়েছিলেন তখনও এটি হয়।

**কারণ:** JD Agent এ JD টেক্সট ডাউনস্ট্রিমে পাঠানো হয়নি। `context_mode="last_agent"` এর সাথে, `resume_executor` হল একমাত্র executor যিনি ব্যবহারকারীর মূল বার্তা পায়। যদি `RESUME_PARSER_INSTRUCTIONS` এর আউটপুটে JD টেক্সট না থাকে, JD Agent এর কাছে বিশ্লেষণের জন্য JD থাকে না, MatchingAgent ফিট স্কোর গণনা করতে পারে না, এবং GapAnalyzer অর্থহীন ইনপুট পায়।

**নির্ণয়:**

সার্ভার লগে MatchingAgent স্প্যান খুঁজুন। যদি এতে থাকে:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
পাস-থ্রু অনুপস্থিত বা ভাঙা।

**সমাধান:** নিশ্চিত করুন `main.py` তে `RESUME_PARSER_INSTRUCTIONS` এর মধ্যে একটি `[JOB DESCRIPTION PASS-THROUGH]` অংশ এবং নিম্নলিখিত নিয়ম আছে:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
এছাড়াও নিশ্চিত করুন `JOB_DESCRIPTION_INSTRUCTIONS` তে একটি `[PARSED RESUME PASS-THROUGH]` রিলে নিয়ম আছে:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
যদি কোনও নির্দেশনা ব্লক স্ক্যাফোল্ড উইজার্ড থেকে একটি স্টাব হয়, তবে এটি পূর্ণ সংস্করণ দিয়ে প্রতিস্থাপন করুন [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) থেকে।

### MatchingAgent আউটপুট দেয় "Cannot compute fit score - no JD provided"

এটি উপরোক্ত একই মূল কারণ। MatchingAgent JD Agent এর আউটপুট পেয়েছে কিন্তু `[PARSED RESUME PASS-THROUGH]` অংশ অনুপস্থিত বা খালি ছিল, তাই এটি দুটি প্রোফাইল তুলনা করতে পারেনি। নিশ্চিত করুন:
১. `JOB_DESCRIPTION_INSTRUCTIONS` রিলে নিয়ম অন্তর্ভুক্ত করে: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
২. `MATCHING_AGENT_INSTRUCTIONS` এজেন্টকে বলে যে `[JD REQUIREMENTS]` এবং `[PARSED RESUME PASS-THROUGH]` অংশগুলি খোঁজার জন্য।

উভয় নির্দেশনা ব্লক পূর্ণ সংস্করণ দিয়ে প্রতিস্থাপন করুন [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) থেকে।

### উত্তরটি দুইবার প্রদর্শিত হচ্ছে

**লক্ষণ:** Agent Inspector প্রতিক্রিয়ায় GapAnalyzer আউটপুট (অথবা পুরো পাইপলাইন আউটপুট) দুইবার দেখা যাচ্ছে।

**কারণ:** `WorkflowBuilder` ইনকামিং এজগুলোর জন্য OR-অর্থনৈতিক তত্ত্ব ব্যবহার করে - ডাউনস্ট্রিম এক্সেকিউটর যেকোনো পূর্বসূরি সম্পন্ন হওয়ার সাথে সাথে কাজ শুরু করে। যদি `matching_executor` এর দুইটি ইনকামিং এজ থাকে (একটি `resume_executor` থেকে এবং একটি `jd_executor` থেকে), এটি দুইবার চালু হয়: একবার যখন ResumeParser শেষ হয় এবং আরেকবার যখন JD Agent শেষ হয়। ফলে GapAnalyzer ও দুইবার চলে।

**সমাধান:** নিশ্চিত করুন `WorkflowBuilder` গ্রাফ একটি কঠোরভাবে ক্রমাগত পাইপলাইন, কোনো ফ্যান-ইন নেই:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # রিজিউম_এক্সিকিউটর থেকে নয়
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

যদি আপনার কাছে একটি ভুল `.add_edge(resume_executor, matching_executor)` লাইন থাকে, এটি সরিয়ে দিন। JD Agent এর আউটপুটে `[PARSED RESUME PASS-THROUGH]` রিলে ইতিমধ্যেই MatchingAgent কে রিজিউম অ্যাক্সেস দেয়।

---

## পরিবেশ এবং কনফিগারেশন সমস্যা

### .env মান অনুপস্থিত বা ভুল

`.env` ফাইলটি অবশ্যই `PersonalCareerCopilot/` ডিরেক্টরিতে থাকতে হবে (`main.py` এর সমতল):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

প্রত্যাশিত `.env` বিষয়বস্তু:

**পাথ A - Foundry ক্লাউড:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**পাথ B - Foundry লোকাল:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> দুইটি পাথই `FOUNDRY_PROJECT_ENDPOINT` ব্যবহার করে। মান ভিন্ন: ক্লাউড uses একটি `https://` Foundry এন্ডপয়েন্ট; লোকাল uses `http://localhost:5273/v1`। সঠিক মডেল এ্যালায়াস নিশ্চিত করতে `foundry model list` চালান Path B এর জন্য।

> **আপনার `FOUNDRY_PROJECT_ENDPOINT` খোঁজার উপায়:** 
- VS Code এর **Foundry Toolkit** সাইডবার খুলুন → আপনার প্রকল্পের উপর রাইট-ক্লিক করুন → **Copy Project Endpoint**। 
- অথবা যান [Azure Portal](https://portal.azure.com) → আপনার Foundry প্রকল্প → **ওভারভিউ** → **Project endpoint**।

> **আপনার `AZURE_AI_MODEL_DEPLOYMENT_NAME` খোঁজার উপায়:** Foundry Toolkit সাইডবারে আপনার প্রকল্প সম্প্রসারণ করুন → **Models** → আপনার ডিপ্লয় করা মডেল নাম (যেমন `gpt-4.1-mini`) খুঁজুন।

### পরিবেশ ভেরিয়েবল অগ্রাধিকার

`main.py` এ `load_dotenv(override=True)` ব্যবহৃত হয়েছে, যার মানে:

| অগ্রাধিকার | উৎস | উভয় সেট থাকলে কোনটি জয়ী? |
|----------|--------|------------------------|
| ১ (সর্বোচ্চ) | `.env` ফাইল | হ্যাঁ |
| ২ | শেল / কনটেইনার পরিবেশ ভেরিয়েবল | ব্যবহৃত হয় যখন একই কী `.env` এ নেই |

স্থানীয় উন্নয়নে, এটি `.env` কে সত্যের উৎস বানায় (`.env` সম্পাদনা করলে চলতি রান উঠে আসে)। হোস্টেড ডিপ্লয়মেন্টে, Foundry কনটেইনার স্তরে পরিবেশ ভেরিয়েবল ইনজেক্ট করে; যেহেতু `.env` এই ল্যাব সেটআপে ডিপ্লয় করা ইমেজের অংশ নয়, ইনজেক্ট করা কনটেইনার মান ব্যবহার করা হয়।

---

## সংস্করণ সামঞ্জস্যতা

### প্যাকেজ সংস্করণ ম্যাট্রিক্স

মাল্টি-অ্যাজেন্ট ওয়ার্কফ্লো নির্দিষ্ট প্যাকেজ সংস্করণ প্রয়োজন। সংস্করণ মেলেনি ভুল ঘটায় রানটাইম ত্রুটি।

| প্যাকেজ | প্রয়োজনীয় সংস্করণ | পরীক্ষা কমান্ড |
|---------|-----------------|---------------|
| `agent-framework-foundry` | সর্বশেষ | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | সর্বশেষ | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | সর্বশেষ | `pip show debugpy` |
| পাইথন | ৩.১২+ | `python --version` |

### সাধারণ সংস্করণ ত্রুটি

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ঠিক করুন: এজেন্ট-ফ্রেমওয়ার্ক-ফাউন্ড্রি পুনরায় ইনস্টল করুন
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# সমাধান: mcp প্যাকেজ আপগ্রেড করুন
pip install mcp --upgrade
```

### একসাথে সব সংস্করণ যাচাই করুন

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

প্রত্যাশিত আউটপুট:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## ডিপ্লয়মেন্ট সমস্যা

### ডিপ্লয়মেন্টের পরে কনটেইনার শুরু হয় না

১. **কনটেইনার লগ দেখুন:**
   - **Foundry Toolkit** সাইডবার খুলুন → **Hosted Agents (Preview)** সম্প্রসারণ করুন → আপনার এজেন্ট ক্লিক করুন → সংস্করণ সম্প্রসারণ করুন → **Container Details** → **Logs**।
   - পাইথন স্ট্যাক ট্রেস বা অনুপস্থিত মডিউল ত্রুটি খুঁজুন।

২. **সাধারণ কনটেইনার স্টার্টআপ বিফলতা:**

   | লগে ত্রুটি | কারণ | সমাধান |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` তে একটি প্যাকেজ অনুপস্থিত | প্যাকেজ যোগ করুন, পুনরায় ডিপ্লয় করুন |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` বা `.env` এ env vars সেট নেই | `agent.yaml` → `environment_variables` সেকশন (হোস্টেড) অথবা `.env` (লোকাল) আপডেট করুন |
   | `azure.identity.CredentialUnavailableError` | Managed Identity কনফিগার করা হয়নি | Foundry স্বয়ংক্রিয়ভাবে সেট করে - নিশ্চিত করুন এক্সটেনশন থেকে ডিপ্লয় করছেন |
   | `OSError: port 8088 already in use` | Dockerfile ভুল পোর্ট এক্সপোজ করছে বা পোর্ট সংঘর্ষ আছে | Dockerfile এ `EXPOSE 8088` এবং `CMD ["python", "main.py"]` যাচাই করুন |
   | কনটেইনার কোড ১ সহ বের হয় | `main()` এ হ্যান্ডেল করা হয়নি এমন ব্যতিক্রম | প্রথমে স্থানীয়ভাবে পরীক্ষা করুন ([মডিউল ৫](05-test-locally.md)) ভুল ধরা পড়ার জন্য |

৩. **সমস্যা সমাধানের পর পুনরায় ডিপ্লয় করুন:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → একই এজেন্ট নির্বাচন করুন → নতুন সংস্করণ ডিপ্লয় করুন।

### ডিপ্লয়মেন্ট অনেক সময় নিচ্ছে

মাল্টি-অ্যাজেন্ট কনটেইনার শুরু হতে বেশি সময় নেয় কারণ তারা স্টার্টআপে ৪টি এজেন্ট ইনস্ট্যান্স তৈরি করে। স্বাভাবিক স্টার্টআপ সময়:

| ধাপ | প্রত্যাশিত সময় |
|-------|------------------|
| কনটেইনার ইমেজ বিল্ড | ১-৩ মিনিট |
| ইমেজ পুশ টু ACR | ৩০-৬০ সেকেন্ড |
| কনটেইনার স্টার্ট (একক এজেন্ট) | ১৫-৩০ সেকেন্ড |
| কনটেইনার স্টার্ট (মাল্টি-অ্যাজেন্ট) | ৩০-১২০ সেকেন্ড |
| এজেন্ট প্লেগ্রাউন্ডে উপলব্ধ | "Started" হওয়ার ১-২ মিনিট পরে |

> যদি "Pending" অবস্থা ৫ মিনিটের বেশি থাকে, কনটেইনার লগে ত্রুটি পরীক্ষা করুন।

---

## আরবিএসি এবং অনুমতি সমস্যা

### `403 Forbidden` অথবা `AuthorizationFailed`

আপনার Foundry প্রকল্পে **[Foundry User](https://aka.ms/foundry-ext-project-role)** ভূমিকা প্রয়োজন (আগে নাম ছিল **Azure AI User** - ভূমিকা আইডি অপরিবর্তিত):

১. যান [Azure Portal](https://portal.azure.com) → আপনার Foundry **প্রকল্প** রিসোর্স।
২. ক্লিক করুন **Access control (IAM)** → **Role assignments**।
৩. আপনার নাম অনুসন্ধান করুন → নিশ্চিত করুন **Foundry User** (অথবা পুরাতন লেবেল **Azure AI User**) তালিকাভুক্ত।
৪. যদি না থাকে: **Add** → **Add role assignment** → **Foundry User** অনুসন্ধান → আপনার অ্যাকাউন্টে নিয়োগ করুন।

বিস্তারিত জানার জন্য দেখুন [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ডকুমেন্টেশন।

### মডেল ডিপ্লয়মেন্ট অ্যাক্সেসযোগ্য নয়

যদি এজেন্ট মডেল-সম্পর্কিত ত্রুটি ফিরিয়ে দেয়:

১. যাচাই করুন মডেলটি ডিপ্লয় হয়েছে: Foundry সাইডবার → প্রকল্প সম্প্রসারণ করুন → **Models** → `gpt-4.1-mini` (অথবা আপনার মডেল) এবং স্ট্যাটাস **Succeeded** আছে কিনা দেখুন।
২. যাচাই করুন ডিপ্লয়মেন্ট নাম মিলে: `.env` (অথবা `agent.yaml`) এ `AZURE_AI_MODEL_DEPLOYMENT_NAME` প্রকৃত ডিপ্লয়মেন্ট নামের সাথে মেলে কিনা।
৩. যদি ডিপ্লয়মেন্ট মেয়াদ উত্তীর্ণ হয়েছে (ফ্রি টিয়ার): পুনরায় ডিপ্লয় করুন [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) থেকে (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)।

---

## Foundry লোকাল সমস্যা (পাথ B)

### Foundry লোকাল সার্ভিস চলছে না

```powershell
# অবস্থা পরীক্ষা করুন
foundry local status

# সার্ভিস বন্ধ থাকলে শুরু করুন
foundry local start
```

| লক্ষণ | কারণ | সমাধান |
|---------|-------|-----|
| স্বাস্থ্য পরীক্ষা `503` ফেরত দেয় | সার্ভিস শুরু হয়নি | `foundry local start` অথবা Foundry Toolkit সাইডবারে **Start** ক্লিক করুন |
| স্বাস্থ্য পরীক্ষা টাইমআউট হয় | মডেল এখনও লোড হচ্ছে | শুরু করার ৩০-৬০ সেকেন্ড পরে অপেক্ষা করুন; বড় মডেল বেশি সময় নেয় |
| `/v1/health` এ `StatusCode: 404` | ভুল পোর্ট | ডিফল্ট `5273`। প্রকৃত পোর্ট দেখতে `foundry local status` চালান |
| সম্পদ কম | Foundry Local সাধারণত ~৪ জিবি RAM ফ্রি প্রয়োজন | অন্যান্য অ্যাপ্লিকেশন বন্ধ করুন |
| মডেল ডাউনলোড ব্যর্থ | ডিস্ক স্পেস কম | মডেল ২-৮ জিবি। স্পেস ফ্রী করুন, তারপর `foundry model pull <name>` চালান |

### মডেল নাম মেলেনি

```powershell
# ডাউনলোড করা মডেলগুলির তালিকা এবং তাদের সঠিক উপনামগুলি
foundry model list
```

`.env` এ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ঠিক মডেল নামে সেট করুন (যেমন `phi-4-mini`, না `Phi-4-mini`)।

### লোকাল রান এ `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (পাথ B)

ল্যাবের `main.py` এ `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` ব্যবহার করা হয়েছে। Foundry Local এ এই ভেরিয়েবল লোকাল সার্ভিসের দিকে নির্দেশ করবে - **না** `AZURE_AI_PROJECT_ENDPOINT`। নিশ্চিত করুন আপনার `.env` এ আছে:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP টুল এখনও একটি আউটবাউন্ড কল করে (পাথ B)

এটি আশা করা যায়। `search_microsoft_learn_for_plan` টুল `https://learn.microsoft.com/api/mcp` থেকে শেখার সংস্থান নিয়ে আসে। **শুধুমাত্র স্কিল-নাম ক্যোয়ারি** নেটওয়ার্কে যায় - রিজিউম এবং JD টেক্সট সম্পূর্ণরূপে আপনার ডিভাইসে প্রক্রিয়াজাত হয় এবং কখনও প্রেরিত হয় না। সম্পূর্ণ অফলাইন অপারেশন প্রয়োজন হলে, টুলে একটি `try/except` ফ্যালব্যাক যোগ করুন যা এন্ডপয়েন্ট পৌঁছাতে না পারলে একটি স্থির `learn.microsoft.com` URL ফেরত দেয়।

---

## সাহায্য নেওয়া

উপরের ফিক্সগুলি চেষ্টা করার পরে আটকে গেলে:

১. **সার্ভার লগ চেক করুন** - বেশিরভাগ ত্রুটি পাইথন স্ট্যাক ট্রেস তৈরি করে টার্মিনালে। সম্পূর্ণ ট্রেসব্যাক পড়ুন।
২. **ত্রুটি বার্তা খুঁজুন** - ত্রুটির টেক্সট কপি করুন এবং [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) তে অনুসন্ধান করুন।
৩. **ইস্যু খুলুন** - [ওয়ার্কশপ রিপোজিটরি](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) এ একটি ইস্যু ফাইল করুন:
   - ত্রুটি বার্তা বা স্ক্রিনশট
   - আপনার প্যাকেজ সংস্করণ (`pip list | Select-String "agent-framework"`)
   - আপনার পাইথন সংস্করণ (`python --version`)
   - সমস্যা স্থানীয় নাকি ডিপ্লয়মেন্ট পরবর্তী

---

### চেকপয়েন্ট

- [ ] আপনি জানেন কিভাবে `.env` কনফিগারেশন সমস্যা পরীক্ষা ও সমাধান করবেন
- [ ] আপনি যাচাই করতে পারেন প্যাকেজ সংস্করণ প্রয়োজনীয় ম্যাট্রিক্সের সাথে মেলে
- [ ] আপনি জানেন কনটেইনার লগে ডিপ্লয়মেন্ট ব্যর্থতা কিভাবে পরীক্ষা করবেন
- [ ] আপনি যাচাই করতে পারেন Azure পোর্টালে RBAC ভূমিকা

---

**পূর্ববর্তী:** [07 - Verify in Playground](07-verify-in-playground.md) · **পরবর্তী:** [09 - Summary →](09-summary.md) · **মূখ্য:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা শুদ্ধতার জন্য চেষ্টা করি, অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার স্বভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে প্রয়োজনীয় ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়বদ্ধ নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->