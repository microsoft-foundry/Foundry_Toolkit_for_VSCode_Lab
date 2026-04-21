# মডিউল ৮ - সমস্যা সমাধান (মাল্টি-এজেন্ট)

এই মডিউলটি মাল্টি-এজেন্ট ওয়ার্কফ্লোর নির্দিষ্ট সাধারণ ত্রুটি, সমাধান এবং ডিবাগিং কৌশলগুলি আলোচনা করে। সাধারণ Foundry ডিপ্লয়মেন্ট সমস্যা গুলোর জন্য, [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md) দেখুন।

---

## দ্রুত রেফারেন্স: ত্রুটি → সমাধান

| ত্রুটি / উপসর্গ | সম্ভাব্য কারণ | সমাধান |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` ফাইল অনুপস্থিত বা মান সেট করা হয়নি | `.env` তৈরি করুন `PROJECT_ENDPOINT=<your-endpoint>` এবং `MODEL_DEPLOYMENT_NAME=<your-model>` সহ |
| `ModuleNotFoundError: No module named 'agent_framework'` | ভার্চুয়াল পরিবেশ সক্রিয় নয় বা ডিপেন্ডেন্সি ইনস্টল হয়নি | চালান `.\.venv\Scripts\Activate.ps1` তারপর `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP প্যাকেজ ইনস্টল করা হয়নি (requirements এ অনুপস্থিত) | চালান `pip install mcp` বা নিশ্চিত করুন `requirements.txt` এ এটিকে ট্রানজিটিভ ডিপেন্ডেন্সি হিসেবে অন্তর্ভুক্ত করা হয়েছে |
| এজেন্ট শুরু হয় কিন্তু খালি রেসপন্স দেয় | `output_executors` এর মিল নেই বা এজ মিসিং | যাচাই করুন `output_executors=[gap_analyzer]` এবং সব এজ `create_workflow()` এ আছে |
| শুধুমাত্র ১টি গ্যাপ কার্ড (বাকি অনুপস্থিত) | GapAnalyzer নির্দেশনা অসম্পূর্ণ | `GAP_ANALYZER_INSTRUCTIONS` এ `CRITICAL:` প্যারাগ্রাফ যোগ করুন - দেখুন [মডিউল ৩](03-configure-agents.md) |
| Fit স্কোর ০ বা অনুপস্থিত | MatchingAgent upstream ডাটা পায়নি | নিশ্চিত করুন `add_edge(resume_parser, matching_agent)` এবং `add_edge(jd_agent, matching_agent)` উভয়ই আছে |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP সার্ভার টুল কল প্রত্যাখ্যান করেছে | ইন্টারনেট সংযোগ পরীক্ষা করুন। ব্রাউজারে `https://learn.microsoft.com/api/mcp` খুলুন। পুনরায় চেষ্টা করুন |
| আউটপুটে Microsoft Learn URL নেই | MCP টুল রেজিস্টার হয়নি বা এন্ডপয়েন্ট ভুল | যাচাই করুন `tools=[search_microsoft_learn_for_plan]` GapAnalyzer এ এবং `MICROSOFT_LEARN_MCP_ENDPOINT` সঠিক |
| `Address already in use: port 8088` | অন্য কোনো প্রসেস পোর্ট 8088 ব্যবহার করছে | চালান `netstat -ano \| findstr :8088` (Windows) বা `lsof -i :8088` (macOS/Linux), এবং বিরোধী প্রসেস বন্ধ করুন |
| `Address already in use: port 5679` | Debugpy পোর্ট সংঘর্ষ | অন্য ডিবাগ সেশন বন্ধ করুন। চালান `netstat -ano \| findstr :5679` প্রসেস খুঁজে পায় এবং হত্যা করুন |
| Agent Inspector খুলতে পারছে না | সার্ভার পুরোপুরি শুরু হয়নি বা পোর্ট সংঘর্ষ | "Server running" লগের জন্য অপেক্ষা করুন। পরীক্ষা করুন পোর্ট 5679 ফাঁকা আছে |
| `azure.identity.CredentialUnavailableError` | Azure CLI তে সাইন ইন করা নেই | চালান `az login` তারপর সার্ভার রিস্টার্ট করুন |
| `azure.core.exceptions.ResourceNotFoundError` | মডেল ডিপ্লয়মেন্ট বিদ্যমান নেই | যাচাই করুন `MODEL_DEPLOYMENT_NAME` আপনার Foundry প্রকল্পে ডিপ্লয় করা মডেলের সাথে মেলে |
| ডিপ্লয়মেন্টের পরে কন্টেইনার স্ট্যাটাস "Failed" | স্টার্টআপে কন্টেইনার ক্রাশ | Foundry সাইডবারে কন্টেইনার লগস পরীক্ষা করুন। সাধারণ: env var মিসিং বা ইমপোর্ট ত্রুটি |
| ডিপ্লয়মেন্ট "Pending" > ৫ মিনিট ধরে | কন্টেইনার শুরু হতে বেশি সময় নিচ্ছে বা রিসোর্স সীমাবদ্ধতা | মাল্টি-এজেন্ট ৪টি এজেন্ট ইন্সট্যান্স তৈরি করে, ৫ মিনিট পর্যন্ত অপেক্ষা করুন। যদি এখনও Pending থাকে, লগস চেক করুন |
| `ValueError` from `WorkflowBuilder` | অবৈধ গ্রাফ কনফিগারেশন | নিশ্চিত করুন `start_executor` সেট আছে, `output_executors` একটি তালিকা এবং কোনও সার্কুলার এজ নেই |

---

## পরিবেশ ও কনফিগারেশন সমস্যা

### .env মান অনুপস্থিত বা ভুল

`.env` ফাইল অবশ্যই `PersonalCareerCopilot/` ডিরেক্টরিতে থাকতে হবে (`main.py` এর সমতল):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

প্রত্যাশিত `.env` কনটেন্ট:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **আপনার PROJECT_ENDPOINT খুঁজে পাওয়া:**  
- VS Code এ **Microsoft Foundry** সাইডবার খুলুন → আপনার প্রজেক্টে রাইট-ক্লিক → **Copy Project Endpoint**.  
- অথবা [Azure Portal](https://portal.azure.com) → আপনার Foundry প্রকল্প → **Overview** → **Project endpoint**।

> **আপনার MODEL_DEPLOYMENT_NAME খুঁজুন:** Foundry সাইডবারে আপনার প্রোজেক্ট বাড়ান → **Models** → ডিপ্লয় করা মডেলের নাম খুঁজুন (যেমন `gpt-4.1-mini`)।

### Env var অগ্রাধিকার

`main.py` এ `load_dotenv(override=False)` ব্যবহৃত হয়েছে, যার অর্থ:

| অগ্রাধিকার | উত্স | উভয় সেট থাকলে কোনটি জিতে? |
|------------|------|------------------------------|
| ১ (সর্বোচ্চ) | শেল এনভায়রনমেন্ট ভেরিয়েবল | হ্যাঁ |
| ২ | `.env` ফাইল | শেল ভ্যারিয়েবল সেট না থাকলে মাত্র |

এর মানে Foundry রানটাইম env vars (`agent.yaml` এ সেট) হোস্টেড ডিপ্লয়মেন্ট চলাকালে `.env` মানের চেয়ে অগ্রাধিকার পায়।

---

## সংস্করণ সামঞ্জস্য

### প্যাকেজ সংস্করণ ম্যাট্রিক্স

মাল্টি-এজেন্ট ওয়ার্কফ্লোর নির্দিষ্ট প্যাকেজ সংস্করণের প্রয়োজন। অসামঞ্জস্যপূর্ণ সংস্করণগুলি রানটাইম ত্রুটি ঘটায়।

| প্যাকেজ | প্রয়োজনীয় সংস্করণ | যাচাই কমান্ড |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | সর্বশেষ প্রি-রিলিজ | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### সাধারণ সংস্করণ ত্রুটি

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ঠিক করুন: rc3 এ আপগ্রেড করুন
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` পাওয়া যাচ্ছে না বা Inspector অনুপযুক্ত:**

```powershell
# সমাধান: --pre ফ্ল্যাগ দিয়ে ইনস্টল করুন
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ফিক্স: mcp প্যাকেজ আপগ্রেড করুন
pip install mcp --upgrade
```

### একসাথে সব সংস্করণ যাচাই

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

প্রত্যাশিত আউটপুট:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## MCP টুল সমস্যা

### MCP টুল কোনো ফলাফল দেয় না

**উপসর্গ:** গ্যাপ কার্ড বলছে "No results returned from Microsoft Learn MCP" অথবা "No direct Microsoft Learn results found"।

**সম্ভাব্য কারণ:**

১. **নেটওয়ার্ক সমস্যা** - MCP এন্ডপয়েন্ট (`https://learn.microsoft.com/api/mcp`) পৌঁছা যাচ্ছে না।
   ```powershell
   # সংযোগ পরীক্ষা করুন
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   যদি এটা `200` রিটার্ন করে, এন্ডপয়েন্ট পৌঁছনযোগ্য।

২. **অনুরোধ অত্যন্ত নির্দিষ্ট** - স্কিল নাম Microsoft Learn সার্চের জন্য খুবই সংকীর্ণ।  
   - খুব বিশেষায়িত স্কিলের জন্য এটা প্রত্যাশিত। টুলটির রেসপন্সে একটি ব্যাকআপ URL থাকে।

৩. **MCP সেশন টাইমআউট** - Streamable HTTP সংযোগ টাইমআউট হয়েছে।  
   - আবার অনুরোধ করুন। MCP সেশন ক্ষণস্থায়ী এবং পুনঃসংযোগ দরকার হতে পারে।

### MCP লগ ব্যাখ্যা

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| লগ | অর্থ | পদক্ষেপ |
|-----|---------|--------|
| `GET → 405` | MCP ক্লায়েন্ট ইনিশিয়ালাইজেশনের সময় পরীক্ষা করে | স্বাভাবিক - উপেক্ষা করুন |
| `POST → 200` | টুল কল সফল হয়েছে | প্রত্যাশিত |
| `DELETE → 405` | MCP ক্লায়েন্ট ক্লিনআপে পরীক্ষা করে | স্বাভাবিক - উপেক্ষা করুন |
| `POST → 400` | ভুল অনুরোধ (ম্যালফর্মড কুয়েরি) | `search_microsoft_learn_for_plan()` এ `query` প্যারামিটার চেক করুন |
| `POST → 429` | রেট লিমিটেড | অপেক্ষা করে পুনরায় চেষ্টা করুন। `max_results` প্যারামিটার কমান |
| `POST → 500` | MCP সার্ভার ত্রুটি | অস্থায়ী - পুনরায় চেষ্টা করুন। সমস্যা থাকলে Microsoft Learn MCP API ডাউন থাকতে পারে |
| কানেকশন টাইমআউট | নেটওয়ার্ক সমস্যা বা MCP সার্ভার অনুপলব্ধ | ইন্টারনেট চেক করুন। চেষ্টা করুন `curl https://learn.microsoft.com/api/mcp` |

---

## ডিপ্লয়মেন্ট সমস্যা

### ডিপ্লয়মেন্টের পরে কন্টেইনার শুরুতে ব্যর্থ

১. **কন্টেইনার লগ পরীক্ষা করুন:**
   - **Microsoft Foundry** সাইডবার খুলুন → **Hosted Agents (Preview)** বাড়ান → আপনার এজেন্ট ক্লিক করুন → ভার্সন বাড়ান → **Container Details** → **Logs**।
   - পাইথন স্ট্যাক ট্রেস বা মিসিং মডিউল ত্রুটি দেখুন।

২. **সাধারণ কন্টেইনার স্টার্টআপ সমস্যা:**

| লগে ত্রুটি | কারণ | সমাধান |
|------------|-------|---------|
| `ModuleNotFoundError` | `requirements.txt` এ একটি প্যাকেজ অনুপস্থিত | প্যাকেজ যোগ করুন, পুনরায় ডিপ্লয় করুন |
| `RuntimeError: Missing required environment variable` | `agent.yaml` এ env vars সেট হয়নি | `agent.yaml` → `environment_variables` অংশ হালনাগাদ করুন |
| `azure.identity.CredentialUnavailableError` | Managed Identity কনফিগার করা হয়নি | Foundry স্বয়ংক্রিয় ভাবে সেট করে - নিশ্চিত করুন আপনি এক্সটেনশনের মাধ্যমে ডিপ্লয় করছেন |
| `OSError: port 8088 already in use` | Dockerfile ভুল পোর্ট প্রকাশ করেছে বা পোর্ট সংঘর্ষ | Dockerfile এ `EXPOSE 8088` এবং `CMD ["python", "main.py"]` যাচাই করুন |
| Container কোড 1 দিয়ে বন্ধ | `main()` এ হ্যান্ডেল করা হয়নি এমন এক্সসেপশন | প্রথমে লোকাল [মডিউল ৫](05-test-locally.md) এ পরীক্ষা করুন ত্রুটি ধরার জন্য |

৩. **ত্রুটি সমাধানের পর পুনঃডিপ্লয়:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → একই এজেন্ট নির্বাচন → নতুন ভার্সন ডিপ্লয় করুন।

### ডিপ্লয়মেন্ট সময় বেশি নেয়

মাল্টি-এজেন্ট কন্টেইনার শুরু হতে সময় নেয় কারণ এটি ৪টি এজেন্ট ইন্সট্যান্স তৈরি করে। স্বাভাবিক শুরু সময়:

| পর্যায় | প্রত্যাশিত সময় |
|--------|----------------|
| কন্টেইনার ইমেজ বিল্ড | ১-৩ মিনিট |
| ইমেজ ACR এ পুশ | ৩০-৬০ সেকেন্ড |
| কন্টেইনার শুরু (সিঙ্গল এজেন্ট) | ১৫-৩০ সেকেন্ড |
| কন্টেইনার শুরু (মাল্টি-এজেন্ট) | ৩০-১২০ সেকেন্ড |
| এজেন্ট প্লে গ্রাউন্ডে উপলব্ধ | "Started" থেকে ১-২ মিনিট পরে |

> যদি ৫ মিনিটের বেশি Pending থাকে, কন্টেইনার লগে ত্রুটি পরীক্ষা করুন।

---

## RBAC এবং অনুমতি সমস্যা

### `403 Forbidden` বা `AuthorizationFailed`

Foundry প্রকল্পে আপনাকে **[Azure AI User](https://aka.ms/foundry-ext-project-role)** ভূমিকা প্রদান করতে হবে:

১. [Azure Portal](https://portal.azure.com) এ যান → আপনার Foundry **প্রকল্প** রিসোর্স।  
২. ক্লিক করুন **Access control (IAM)** → **Role assignments**।  
৩. আপনার নাম খুঁজুন → নিশ্চিত করুন **Azure AI User** তালিকাভুক্ত আছে।  
৪. অনুপস্থিত হলে: **Add** → **Add role assignment** → **Azure AI User** খুঁজুন → আপনার একাউন্টে অ্যাসাইন করুন।

বিস্তারিত জন্য [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ডকুমেন্ট দেখুন।

### মডেল ডিপ্লয়মেন্ট অ্যাক্সেসযোগ্য নয়

যদি এজেন্ট মডেল সম্পর্কিত ত্রুটি দেয়:

১. যাচাই করুন মডেল ডিপ্লয় করা আছে: Foundry সাইডবার → প্রকল্প বাড়ান → **Models** → `gpt-4.1-mini` (অথবা আপনার মডেল) স্ট্যাটাস **Succeeded**।  
২. ডিপ্লয়মেন্ট নাম মিলে কিনা যাচাই করুন: `.env` (অথবা `agent.yaml`) এর `MODEL_DEPLOYMENT_NAME` এবং সাইডবারে প্রকৃত ডিপ্লয়মেন্ট নাম।  
৩. যদি ডিপ্লয়মেন্টের মেয়াদ শেষ হয় (ফ্রি টিয়ার): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) থেকে পুনঃডিপ্লয় করুন (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)।

---

## Agent Inspector সমস্যা

### Inspector খোলে কিন্তু "Disconnected" দেখায়

১. সার্ভার চলছে কিনা নিশ্চিত করুন: টার্মিনালে "Server running on http://localhost:8088" দেখুন।  
২. পোর্ট `5679` চেক করুন: Inspector debugpy মাধ্যমে এই পোর্টে কানেক্ট করে।  
   ```powershell
   netstat -ano | findstr :5679
   ```
৩. সার্ভার রিস্টার্ট করুন এবং Inspector পুনরায় খুলুন।

### Inspector আংশিক রেসপন্স দেখায়

মাল্টি-এজেন্ট রেসপন্সগুলি দীর্ঘ এবং ইনক্রিমেন্টালি স্ট্রিম হয়। সম্পূর্ণ রেসপন্সের জন্য অপেক্ষা করুন (গ্যাপ কার্ড এবং MCP টুল কলের সংখ্যা অনুসারে ৩০-৬০ সেকেন্ড লাগতে পারে)।

যদি রেসপন্স ক্রমাগত কাটা যায়:  
- যাচাই করুন GapAnalyzer নির্দেশনায় `CRITICAL:` ব্লক আছে যা গ্যাপ কার্ডগুলো একত্রিত হওয়া রোধ করে।  
- আপনার মডেলের টোকেন সীমা পরীক্ষা করুন - `gpt-4.1-mini` সর্বোচ্চ ৩২ হাজার আউটপুট টোকেন সমর্থন করে, যা যথেষ্ট হওয়া উচিত।

---

## কর্মক্ষমতা সংক্রান্ত টিপস

### ধীর প্রতিক্রিয়া

মাল্টি-এজেন্ট ওয়ার্কফ্লো স্বভাবতই স্লো কারণ এটি ক্রমানুসারে নির্ভরতাসহ MCP টুল কল করে।

| অপটিমাইজেশন | কিভাবে | প্রভাব |
|-------------|-------|--------|
| MCP কল কমান | টুলের `max_results` প্যারামিটার কমিয়ে দিন | HTTP রাউন্ড ট্রিপ কমবে |
| নির্দেশনা সহজ করুন | ছোট, বেশি ফোকাসড এজেন্ট প্রম্পট | দ্রুত LLM ইনফারেন্স |
| ব্যবহার করুন `gpt-4.1-mini` | উন্নয়নের জন্য `gpt-4.1` থেকে দ্রুত | প্রায় ২গুণ দ্রুততা |
| গ্যাপ কার্ডের বিস্তারিত কমান | GapAnalyzer নির্দেশনায় গ্যাপ কার্ড ফরম্যাট সরল করুন | কম আউটপুট জেনারেশন |

### সাধারণ রেসপন্স সময় (লোকাল)

| কনফিগারেশন | প্রত্যাশিত সময় |
|--------------|----------------|
| `gpt-4.1-mini`, ৩-৫ গ্যাপ কার্ড | ৩০-৬০ সেকেন্ড |
| `gpt-4.1-mini`, ৮+ গ্যাপ কার্ড | ৬০-১২০ সেকেন্ড |
| `gpt-4.1`, ৩-৫ গ্যাপ কার্ড | ৬০-১২০ সেকেন্ড |
---

## সাহায্য পাওয়া

উপরে উল্লেখিত সমাধানসমূহ চেষ্টা করার পরও যদি আটকে থাকেন:

1. **সার্ভারের লগ পরীক্ষা করুন** - অধিকাংশ ত্রুটি টার্মিনালে একটি পাইথন স্ট্যাক ট্রেস তৈরি করে। সম্পূর্ণ ট্রেসব্যাকটি পড়ুন।
2. **ত্রুটি বার্তাটি অনুসন্ধান করুন** - ত্রুটি পাঠ্যটি কপি করে [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) তে অনুসন্ধান করুন।
3. **একটি সমস্যা রিপোর্ট করুন** - [ওয়ার্কশপ রেপোজিটোরি](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) তে একটি ইস্যু ফাইল করুন যার মধ্যে থাকুক:
   - ত্রুটি বার্তা বা স্ক্রিনশট
   - আপনার প্যাকেজ সংস্করণসমূহ (`pip list | Select-String "agent-framework"`)
   - আপনার পাইথনের সংস্করণ (`python --version`)
   - সমস্যা কি লোকাল নাকি ডিপ্লয়মেন্টের পর হয়েছে

---

### চেকপয়েন্ট

- [ ] আপনি দ্রুত রেফারেন্স টেবিল ব্যবহার করে সবচেয়ে সাধারণ মাল্টি-এজেন্ট ত্রুটিগুলো সনাক্ত এবং ঠিক করতে পারেন
- [ ] আপনি `.env` কনফিগারেশন সমস্যাগুলো পরীক্ষা ও মেরামত করতে জানেন
- [ ] আপনি যাচাই করতে পারেন যে প্যাকেজ সংস্করণগুলো প্রয়োজনীয় ম্যাট্রিক্সের সাথে মেলে
- [ ] আপনি MCP লগ এন্ট্রিগুলো বুঝতে এবং টুলের ব্যর্থতা নির্ণয় করতে পারেন
- [ ] আপনি ডিপ্লয়মেন্ট ব্যর্থতার জন্য কন্টেইনার লগগুলি পরীক্ষা করতে জানেন
- [ ] আপনি Azure পোর্টালে RBAC রোলগুলি যাচাই করতে পারেন

---

**পূর্ববর্তী:** [07 - Verify in Playground](07-verify-in-playground.md) · **মূল পাতা:** [Lab 02 README](../README.md) · [ওয়ার্কশপ হোম](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:  
এই ডকুমেন্টটি AI অনুবাদ সেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা যথাযথতার চেষ্টা করি, তবে অনুগ্রহ করে সচেতন থাকুন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল ডকুমেন্টটি তার নিজ ভাষায়ই কর্তৃত্বপূর্ণ উৎস হিসাবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহার থেকে উদ্ভূত কোনো ভুলবোঝাবুঝি বা ভ্রান্ত ব্যাখ্যার জন্য আমরা দায় প্রকাশ করছি না।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->