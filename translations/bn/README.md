# Foundry Toolkit + Foundry Hosted Agents কর্মশালা

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Microsoft Foundry Agent Service**-এ AI এজেন্ট তৈরি, পরীক্ষা এবং মোতায়েন করুন **Hosted Agents** হিসেবে — সম্পূর্ণরূপে VS Code ব্যবহার করে **Microsoft Foundry এক্সটেনশন** এবং **Foundry Toolkit** এর মাধ্যমে।

> **Hosted Agents বর্তমানে প্রিভিউ মোডে আছে।** সমর্থিত অঞ্চলগুলি সীমিত - দেখুন [অঞ্চল উপলব্ধতা](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)।

> প্রতিটি ল্যাবে `agent/` ফোল্ডারটি Foundry এক্সটেনশন দ্বারা **স্বয়ংক্রিয়ভাবে তৈরি** হয় — তারপর আপনি কোড কাস্টমাইজ করেন, স্থানীয়ভাবে পরীক্ষা করেন, এবং মোতায়েন করেন।

### 🌐 বহু-ভাষার সমর্থন

#### GitHub Action এর মাধ্যমে সমর্থিত (অটোমেটেড ও সবসময় আপ-টু-ডেট)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](./README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **স্থানীয়ভাবে ক্লোন করতে চান?**
>
> এই রিপোজিটরিতে ৫০+ ভাষার অনুবাদ অন্তর্ভুক্ত, যা ডাউনলোড সাইজ অনেক বাড়িয়ে দেয়। অনুবাদ ছাড়া ক্লোন করতে স্পার্স চেকআউট ব্যবহার করুন:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> এটি দ্রুত ডাউনলোডের মাধ্যমে কোর্স শেষ করার জন্য আপনার প্রয়োজনীয় সবকিছু দেয়।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## স্থাপত্য

```mermaid
flowchart TB
    subgraph Local["স্থানীয় উন্নয়ন (VS কোড)"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "F5 ডিবাগ" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["মাইক্রোসফট ফাউন্ডরি"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> স্ক্যাফোল্ড
    Playground -- "টেস্ট প্রম্পটসমূহ" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**প্রবাহ:** Foundry এক্সটেনশন এজেন্ট তৈরি করে → আপনি কোড এবং নির্দেশাবলী কাস্টমাইজ করেন → Agent Inspector দিয়ে স্থানীয়ভাবে পরীক্ষা করেন → Foundry-তে মোতায়েন (Docker ইমেজ ACR তে পাঠানো) → Playground-এ যাচাই করেন।

---

## আপনি যা তৈরি করবেন

| ল্যাব | বিবরণ | অবস্থা |
|-----|-------------|--------|
| **ল্যাব ০১ - একক এজেন্ট** | **"Explain Like I'm an Executive" এজেন্টটি** তৈরি করুন, স্থানীয়ভাবে পরীক্ষা করুন, এবং Foundry-তে মোতায়েন করুন | ✅ উপলব্ধ |
| **ল্যাব ০২ - বহু-এজেন্ট ওয়ার্কফ্লো** | **"Resume → Job Fit Evaluator"** - ৪টি এজেন্ট একসাথে কাজ করে রেজিউমের উপযোগিতা স্কোর করে এবং শেখার রোডম্যাপ তৈরি করে | ✅ উপলব্ধ |

---

## Executive Agent এর সাথে পরিচিতি

এই কর্মশালায় আপনি **"Explain Like I'm an Executive" এজেন্ট** তৈরি করবেন - একটি AI এজেন্ট যা জটিল প্রযুক্তিগত ভাষা নিয়ে সেটিকে শান্ত ও বোর্ডরুম-উপযোগী সারাংশে অনুবাদ করে। কারণ সত্ত্বেও, সি-সুইটে কেউ "v3.2-এ সিঙ্ক্রোনাস কল দ্বারা তৈরি থ্রেড পুল ক্ষয়জনিত ডিলে" শুনতে চায় না।

আমি এই এজেন্টটি তৈরি করেছিলাম একাধিক ঘটনার পর যখন আমার নিখুঁত পোস্ট-মর্টেম পেয়ে উত্তর পাওয়া গেল: *"তাহলে... ওয়েবসাইট ডাউন কি না?"*

### এটি কীভাবে কাজ করে

আপনি একটি প্রযুক্তিগত আপডেট দেবেন। এটি তিনটি পয়েন্টে একটি নির্বাহী সারাংশ ফিরিয়ে দেয় - কোন জটিল ভাষা নয়, না স্ট্যাক ট্রেস, না আতঙ্কজনক ব্যাখ্যা। শুধু **কি ঘটেছে**, **ব্যবসায়িক প্রভাব**, এবং **পরবর্তী পদক্ষেপ**।

### এটি কার্যকরীভাবে দেখুন

**আপনি বলুন:**
> "API বিলম্বতা বৃদ্ধি পেয়েছে v3.2 এ সিঙ্ক্রোনাস কল দ্বারা তৈরি থ্রেড পুল ক্ষয়ের কারণে।"

**এজেন্ট উত্তর দেয়:**

> **নির্বাহী সারাংশ:**
> - **কি ঘটেছে:** সর্বশেষ রিলিজের পর সিস্টেম ধীরে চলে।
> - **ব্যবসায়িক প্রভাব:** কিছু ব্যবহারকারী সেবাটি ব্যবহার করতে দেরি অনুভব করেছে।
> - **পরবর্তী পদক্ষেপ:** পরিবর্তনটি পূর্বাবস্থায় ফিরিয়ে আনা হয়েছে এবং পুনরায় মোতায়েনের আগে সমাধান প্রস্তুত করা হচ্ছে।

### কেন এই এজেন্ট?

এটি খুব সহজ, একক উদ্দেশ্যের এজেন্ট - হোস্টেড এজেন্ট ওয়ার্কফ্লো শুরু থেকে শেষ পর্যন্ত শেখার জন্য পারফেক্ট, জটিল সরঞ্জাম চেইন ছাড়া। সত্যি বলতে? প্রতিটি ইঞ্জিনিয়ারিং দল এরকম একটি ব্যবহার করতে পারে।

---

## কর্মশালা কাঠামো

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **দ্রষ্টব্য:** প্রতিটি ল্যাবের `agent/` ফোল্ডারটি **Microsoft Foundry এক্সটেনশন** দ্বারা তৈরি হয় যখন আপনি কমান্ড প্যালেট থেকে `Microsoft Foundry: Create a New Hosted Agent` রান করেন। এরপর ফাইলগুলো আপনার এজেন্টের নির্দেশাবলী, টুলস এবং কনফিগারেশন দিয়ে কাস্টমাইজ করা হয়। ল্যাব ০১ আপনাকে আবার থেকে তৈরি করার মাধ্যমে ধাপে ধাপে দেখায়।

---

## শুরু করা

### ১. রিপোজিটরি ক্লোন করুন

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### ২. একটি Python ভার্চুয়াল এনভায়রনমেন্ট সেট আপ করুন

```bash
python -m venv venv
```

এটি সক্রিয় করুন:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### ৩. নির্ভরতা ইনস্টল করুন

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### ৪. পরিবেশ ভেরিয়েবল কনফিগার করুন

এজেন্ট ফোল্ডারের ভিতরে উদাহরণ `.env` ফাইলটি কপি করুন এবং আপনার মানগুলি পূরণ করুন:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` সম্পাদনা করুন:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### ৫. কর্মশালা ল্যাব অনুসরণ করুন

প্রতিটি ল্যাব নিজস্ব মডিউল সহ স্বয়ংসম্পূর্ণ। মৌলিক বিষয়গুলি শেখার জন্য প্রথমে **ল্যাব ০১** শুরু করুন, তারপর বহু-এজেন্ট ওয়ার্কফ্লোর জন্য **ল্যাব ০২** এ যান।

#### ল্যাব ০১ - একক এজেন্ট ([সম্পূর্ণ নির্দেশাবলী](workshop/lab01-single-agent/README.md))

| # | মডিউল | লিঙ্ক |
|---|--------|------|
| ১ | প্রাক-শর্ত পড়ুন | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| ২ | Foundry Toolkit ও Foundry এক্সটেনশন ইনস্টল করুন | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| ৩ | একটি Foundry প্রকল্প তৈরি করুন | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| ৪ | একটি হোস্টেড এজেন্ট তৈরি করুন | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| ৫ | নির্দেশাবলী ও পরিবেশ কনফিগার করুন | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| ৬ | স্থানীয়ভাবে পরীক্ষা করুন | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| ৭ | Foundry-তে মোতায়েন করুন | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| ৮ | প্লেগ্রাউন্ডে যাচাই করুন | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| ৯ | সমস্যার সমাধান | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### ল্যাব ০২ - বহু-এজেন্ট ওয়ার্কফ্লো ([সম্পূর্ণ নির্দেশাবলী](workshop/lab02-multi-agent/README.md))

| # | মডিউল | লিঙ্ক |
|---|--------|------|
| ১ | প্রাক-শর্ত (ল্যাব ০২) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| ২ | বহু-এজেন্ট স্থাপত্য বোঝা | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| ৩ | বহু-এজেন্ট প্রকল্প স্ক্যাফোল্ড করা | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| ৪ | এজেন্ট ও পরিবেশ কনফিগার করা | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| ৫ | অর্কেস্ট্রেশন প্যাটার্ন | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| ৬ | স্থানীয়ভাবে পরীক্ষা করা (বহু-এজেন্ট) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Foundry তে স্থাপন করুন | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | প্লেগ্রাউন্ডে যাচাই করুন | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | সমস্যা সমাধান (মাল্টি-এজেন্ট) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## রক্ষণাবেক্ষক

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>শিবম গয়াল</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## প্রয়োজনীয় অনুমতিসমূহ (দ্রুত রেফারেন্স)

| পরিস্থিতি | প্রয়োজনীয় ভূমিকা |
|----------|---------------|
| নতুন Foundry প্রকল্প তৈরি করুন | Foundry রিসোর্সে **Azure AI Owner** |
| বিদ্যমান প্রকল্পে স্থাপন করুন (নতুন রিসোর্স) | সাবস্ক্রিপশনে **Azure AI Owner** + **Contributor** |
| সম্পূর্ণ কনফিগার্ড প্রকল্পে স্থাপন করুন | অ্যাকাউন্টে **Reader** + প্রকল্পে **Azure AI User** |

> **গুরুত্বপূর্ণ:** Azure `Owner` এবং `Contributor` ভূমিকা শুধুমাত্র *ম্যানেজমেন্ট* অনুমতি অন্তর্ভুক্ত করে, *ডেভেলপমেন্ট* (ডেটা অ্যাকশন) অনুমতি নয়। এজেন্ট তৈরি ও স্থাপনের জন্য আপনার **Azure AI User** বা **Azure AI Owner** প্রয়োজন।

---

## রেফারেন্সসমূহ

- [দ্রুত শুরু: আপনার প্রথম হোস্টেড এজেন্ট স্থাপন করুন (VS কোড)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [হোস্টেড এজেন্ট কী?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS কোডে হোস্টেড এজেন্ট ওয়ার্কফ্লো তৈরি করুন](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [হোস্টেড এজেন্ট স্থাপন করুন](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry এর জন্য RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [আর্কিটেকচার রিভিউ এজেন্ট নমুনা](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP টুলস, Excalidraw ডায়াগ্রাম এবং ডুয়াল ডিপ্লয়মেন্ট সহ বাস্তব হোস্টেড এজেন্ট

---


## লাইসেন্স

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:
এই নথিটি AI অনুবাদ পরিষেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। যদিও আমরা শুদ্ধতার জন্য চেষ্টা করি, অনুগ্রহ করে মনে রাখবেন যে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার স্বভাষায় কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ সুপারিশ করা হয়। এই অনুবাদের ব্যবহারে প্রয়োজনীয় ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়বদ্ধ নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->