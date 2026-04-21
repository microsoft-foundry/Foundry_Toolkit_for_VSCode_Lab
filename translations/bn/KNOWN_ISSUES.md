# পরিচিত সমস্যা

এই নথিটি বর্তমানে রেপোজিটরির অবস্থার সাথে পরিচিত সমস্যাগুলি ট্র্যাক করে।

> সর্বশেষ আপডেট: ২০২৬-০৪-১৫। Python 3.13 / Windows এ `.venv_ga_test` এ পরীক্ষা করা হয়েছে।

---

## বর্তমান প্যাকেজ পিন (সমস্ত তিনটি এজেন্ট)

| প্যাকেজ | বর্তমান সংস্করণ |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(স্থির করা হয়েছে — দেখুন KI-003)* |

---

## KI-001 — GA 1.0.0 আপগ্রেড বাধাগ্রস্ত: `agent-framework-azure-ai` সরানো হয়েছে

**অবস্থা:** খোলা | **তীব্রতা:** 🔴 উচ্চ | **ধরন:** ব্রেকিং

### বিবরণ

`agent-framework-azure-ai` প্যাকেজ (পিন করা হয়েছে `1.0.0rc3`) GA রিলিজে (1.0.0, মুক্তি: ২০২৬-০৪-০২) **সরানো/বিরতিপ্রাপ্ত** হয়েছে। এটি দ্বারা প্রতিস্থাপিত হয়েছে:

- `agent-framework-foundry==1.0.0` — Foundry-হোস্টেড এজেন্ট প্যাটার্ন
- `agent-framework-openai==1.0.0` — OpenAI-সমর্থিত এজেন্ট প্যাটার্ন

সমস্ত তিনটি `main.py` ফাইল `agent_framework.azure` থেকে `AzureAIAgentClient` ইম্পোর্ট করে, যা GA প্যাকেজে `ImportError` তোলা হয়। `agent_framework.azure` নামস্থান GA তে এখনও রয়েছে তবে এখন এতে শুধুমাত্র Azure Functions ক্লাসগুলি (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) রয়েছে — Foundry এজেন্ট নয়।

### নিশ্চিত ত্রুটি (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### প্রভাবিত ফাইলগুলি

| ফাইল | লাইন |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` এর সাথে অসঙ্গতিপূর্ণ

**অবস্থা:** খোলা | **তীব্রতা:** 🔴 উচ্চ | **ধরন:** ব্রেকিং (আপস্ট্রিমে বাধাগ্রস্ত)

### বিবরণ

`azure-ai-agentserver-agentframework==1.0.0b17` (সর্বশেষ) `agent-framework-core<=1.0.0rc3` হেয়ার্ড-পিন করে। এটি `agent-framework-core==1.0.0` (GA) এর সাথে একসাথে ইনস্টল করার সময় pip কে বাধ্য করে `agent-framework-core` কে আবার `rc3` এ **ডাউনগ্রেড** করতে, যা পরে `agent-framework-foundry==1.0.0` এবং `agent-framework-openai==1.0.0` ভঙ্গ করে।

`from azure.ai.agentserver.agentframework import from_agent_framework` কল যা সমস্ত এজেন্ট দ্বারা HTTP সার্ভার বাইন্ড করার জন্য ব্যবহৃত হয়, তাই বাধাগ্রস্ত।

### নিশ্চিত ডিপেন্ডেন্সি সংঘাত (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### প্রভাবিত ফাইলগুলি

সব তিনটি `main.py` ফাইল — শীর্ষ-স্তরের ইম্পোর্ট এবং `main()` ফাংশনের ভিতরের ইম্পোর্ট উভয়।

---

## KI-003 — `agent-dev-cli --pre` ফ্ল্যাগ আর প্রয়োজন নেই

**অবস্থা:** ✅ স্থির (ব্রেকিং নয়) | **তীব্রতা:** 🟢 কম

### বিবরণ

সমস্ত `requirements.txt` ফাইল পূর্বে `agent-dev-cli --pre` অন্তর্ভুক্ত করতো প্রি-রিলিজ CLI টানার জন্য। GA 1.0.0 মুক্তির (২০২৬-০৪-০২) পর থেকে, `agent-dev-cli` এর স্থিতিশীল রিলিজ এখন `--pre` ফ্ল্যাগ ছাড়াই উপলব্ধ।

**স্থিরকরণ প্রয়োগ:** সমস্ত তিনটি `requirements.txt` ফাইল থেকে `--pre` ফ্ল্যাগ সরানো হয়েছে।

---

## KI-004 — Dockerfiles এ `python:3.14-slim` (প্রি-রিলিজ বেস ইমেজ) ব্যবহার হচ্ছে

**অবস্থা:** খোলা | **তীব্রতা:** 🟡 কম

### বিবরণ

সমস্ত `Dockerfile` এ `FROM python:3.14-slim` ব্যবহার করা হয়েছে যা একটি প্রি-রিলিজ Python বিল্ড ট্র্যাক করে। প্রোডাকশন ডিপ্লয়মেন্টের জন্য এটি একটি স্থিতিশীল রিলিজ (যেমন, `python:3.12-slim`) এ পিন করা উচিত।

### প্রভাবিত ফাইলগুলি

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## রেফারেন্স

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ সেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। আমরা যথাসাধ্য সঠিকতার জন্য চেষ্টা করি, তবে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে তা অনুগ্রহ করে লক্ষ করুন। মূল নথি এর নিজস্ব ভাষায় থাকা নথিটি প্রামাণিক উৎস হিসাবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানু্ষ অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে সৃষ্ট কোনো ভুল বুঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->