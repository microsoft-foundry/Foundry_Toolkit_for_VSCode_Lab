# Foundry Toolkit + Foundry Hosted Agents ਵਰਕਸ਼ਾਪ

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

ਮਾਇਕਰੋਸੌਫਟ ਫਊਂਡਰੀ ਏਜੰਟ ਸੇਵਾ 'ਚ AI ਏਜੰਟਾਂ ਨੂੰ ਬਿਲਡ, ਟੈਸਟ ਅਤੇ ਡਿਪਲੌ ਕਰੋਂ **ਹੋਸਟਡ ਏਜੰਟਾਂ** ਵਜੋਂ - ਪੂਰੀ ਤਰ੍ਹਾਂ VS ਕੋਡ 'ਚੋਂ **ਮਾਇਕਰੋਸੌਫਟ ਫਊਂਡਰੀ ਇਕਸਟੈਂਸ਼ਨ** ਅਤੇ **ਫਊਂਡਰੀ ਟੂਲਕਿਟ** ਦੀ ਵਰਤੋਂ ਕਰਕੇ।

> **ਹੋਸਟਡ ਏਜੰਟ ਇਸ ਸਮੇਂ ਪ੍ਰੀਵਿਊ ਵਿੱਚ ਹਨ।** ਸਹਾਇਤਾ ਪ੍ਰਾਪਤ ਖੇਤਰ ਸੀਮਤ ਹਨ - ਵੇਖੋ [ਖੇਤਰ ਉਪਲਬਧਤਾ](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)।

> ਹਰ ਲੈਬ ਵਿੱਚ `agent/` ਫੋਲਡਰ **ਆਟੋਮੈਟਿਕਲੀ ਸਕੈਫੋਲਡਿਸ਼ਦ** ਹੁੰਦਾ ਹੈ ਫਊਂਡਰੀ ਇਕਸਟੈਂਸ਼ਨ ਵੱਲੋਂ - ਤੁਸੀਂ ਫਿਰ ਕੋਡ ਨੂੰ ਕਸਟਮਾਈਜ਼ ਕਰਦੇ ਹੋ, ਸਥਾਨਕ ਟੈਸਟ ਕਰਦੇ ਹੋ ਅਤੇ ਡਿਪਲੌ ਕਰਦੇ ਹੋ।

### 🌐 ਬਹੁ-ਭਾਸ਼ਾਈ ਸਹਾਇਤਾ

#### GitHub ਐਕਸ਼ਨ ਰਾਹੀਂ ਸਹਾਇਤਾ (ਆਟੋਮੈਟਿਕ ਅਤੇ ਹਮੇਸ਼ਾ ਅਪ-ਟੂ-ਡੇਟ)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](./README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ਕੀ ਤੁਸੀਂ ਆਪਣੇ ਸਥਾਨਕ ਕਮੇਪਿਊਟਰ 'ਤੇ ਕਲੋਨ ਕਰਨਾ ਪਸੰਦ ਕਰੋਗੇ?**
>
> ਇਸ ਰਿਪੋਜ਼ਿਟਰੀ ਵਿੱਚ 50+ ਭਾਸ਼ਾ ਅਨੁਵਾਦ ਸ਼ਾਮਲ ਹਨ ਜੋ ਡਾਊਨਲੋਡ ਸਾਈਜ਼ ਨੂੰ ਕਾਫੀ ਵਧਾਉਂਦੇ ਹਨ। ਬਿਨਾਂ ਅਨੁਵਾਦਾਂ ਦੇ ਕਲੋਨ ਕਰਨ ਲਈ, ਸਪਾਰਸ ਚੈਕਆਉਟ ਵਰਤੋ:
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
> ਇਸ ਨਾਲ ਤੁਹਾਨੂੰ ਟੂਰਨੈੜ ਕੋਰਸ ਪੂਰਾ ਕਰਨ ਲਈ ਸਾਰਾ ਕੁੱਝ ਬਹੁਤ ਤੇਜ਼ ਡਾਊਨਲੋਡ ਨਾਲ ਮਿਲ ਜਾਵੇਗਾ।
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## ਸਰંચਨਾ

```mermaid
flowchart TB
    subgraph Local["ਸਥਾਨਕ ਵਿਕਾਸ (VS ਕੋਡ)"]
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
        Scaffold -- "F5 ਡਿਬੱਗ" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["ਮਾਈਕ੍ਰੋਸੌਫਟ ਫਾਊਂਡਰੀ"]
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
    (localhost:8088)" --> ਸਕੈਫੋਲਡ
    Playground -- "ਟੈਸਟ ਪ੍ਰਾਂਪਟਸ" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**ਪ੍ਰਵਾਹ:** ਫਊਂਡਰੀ ਇਕਸਟੈਂਸ਼ਨ ਏਜੰਟ ਨੂੰ ਸਕੈਫੋਲਡ ਕਰਦਾ ਹੈ → ਤੁਸੀਂ ਕੋਡ ਅਤੇ ਦਿਸ਼ਾ ਨਿਰਦੇਸ਼ ਕਸਟਮਾਈਜ਼ ਕਰਦੇ ਹੋ → ਏਜੰਟ ਇੰਸਪੈਕਟਰ ਨਾਲ ਸਥਾਨਕ ਟੈਸਟ → ਫਊਂਡਰੀ 'ਤੇ ਡਿਪਲੌ (ਡੋਕਰ ਇਮੇਜ ACR 'ਤੇ ਪੁਸ਼ ਕੀਤਾ ਜਾਂਦਾ ਹੈ) → ਪਲੇਗ੍ਰਾਊਂਡ ਵਿੱਚ ਜਾਂਚ।

---

## ਤੁਸੀਂ ਕੀ ਬਣਾਉਗੇ

| ਲੈਬ | ਵੇਰਵਾ | ਸਥਿਤੀ |
|-----|-------------|--------|
| **ਲੈਬ 01 - ਸਿੰਗਲ ਏਜੰਟ** | **"Explain Like I'm an Executive" Agent** ਬਣਾਓ, ਸਥਾਨਕ ਟੈਸਟ ਕਰੋ ਅਤੇ ਫਊਂਡਰੀ ਵਿੱਚ ਡਿਪਲੌ ਕਰੋ | ✅ ਉਪਲਬਧ |
| **ਲੈਬ 02 - ਮਲਟੀ-ਏਜੰਟ ਵਰਕਫਲੋ** | **"Resume → Job Fit Evaluator"** ਬਣਾਓ - 4 ਏਜੰਟ ਰੀਜ਼ਿਊਮੇ ਦੀ ਮਾਪ ਅਤੇ ਸਿਖਲਾਈ ਰੋਡਮੈਪ ਬਣਾਉਂਦੇ ਹਨ | ✅ ਉਪਲਬਧ |

---

## ਕਾਰਜਕਾਰੀ ਏਜੰਟ ਨਾਲ ਮਿਲੋ

ਇਸ ਵਰਕਸ਼ਾਪ ਵਿੱਚ ਤੁਸੀਂ **"Explain Like I'm an Executive" Agent** ਬਣਾਓਗੇ - ਇੱਕ AI ਏਜੰਟ ਜੋ ਜਟਿਲ ਟੈਕਨਿਕਲ ਭਾਸ਼ਾ ਨੂੰ ਸ਼ਾਂਤ, ਬੋਰਡਰੂਮ-ਤਿਆਰ ਸੰਖੇਪਾਂ ਵਿੱਚ ਅਨੁਵਾਦ ਕਰਦਾ ਹੈ। ਸੱਚ ਪੁੱਛੋ ਤਾਂ C-suite ਵਿੱਚ ਕੋਈ ਵੀ "ਥ੍ਰੈਡ ਪੂਲ ਖਤਮ ਹੋਣ ਕਾਰਨ ਸਮਕਾਲੀ ਕਾਲਾਂ ਜੋ v3.2 ਵਿੱਚ ਸ਼ਾਮਲ ਕੀਤੀਆਂ ਗਈਆਂ" ਦੀ ਗੱਲ ਸੁਣਨਾ ਨਹੀਂ ਚਾਹੁੰਦਾ।

ਮੈਂ ਇਹ ਏਜੰਟ ਤਾਂ ਬਣਾਇਆ ਸੀ ਕਿਉਂਕਿ ਬਹੁਤ ਸਾਰੀਆਂ ਵਾਰ ਮੇਰੇ ਬਹੁਤ ਸਧਰੇ ਪੋਸਟ-ਮਾਰਟਮ ਨੂੰ ਇਹ ਜਵਾਬ ਮਿਲਿਆ: *"ਤਾਂ... ਕੀ ਵੈੱਬਸਾਈਟ ਡਾਊਨ ਹੈ ਜਾਂ ਨਹੀਂ?"*

### ਇਹ ਕਿਵੇਂ ਕੰਮ ਕਰਦਾ ਹੈ

ਤੁਸੀਂ ਇਸਨੂੰ ਇੱਕ ਟੈਕਨੀਕੀ ਅਪਡੇਟ ਦਿੰਦੇ ਹੋ। ਇਹ ਇੱਕ ਕਾਰਜਕਾਰੀ ਸੰਖੇਪ ਦਿੰਦਾ ਹੈ - ਤਿੰਨ ਬੁਲੇਟ ਪੁਆਇੰਟ, ਕੋਈ ਜਰਗਨ ਨਹੀਂ, ਕੋਈ ਸਟੈਕ ਟਰੇਸ ਨਹੀਂ, ਕੋਈ ਡਰ ਨਹੀਂ। ਸਿਰਫ਼ **ਕੀ ਵਾਪਰਿਆ**, **ਕਾਰੋਬਾਰੀ ਪ੍ਰਭਾਵ**, ਅਤੇ **ਅਗਲਾ ਕਦਮ**।

### ਇਸਨੂੰ ਕਾਰਜ ਵਿੱਚ ਦੇਖੋ

**ਤੁਸੀਂ ਕਹਿੰਦੇ ਹੋ:**
> "API ਦੀ ਲੇਟेंसी ਵਧ ਗਈ ਕਿਉਂਕਿ ਸਮਕਾਲੀ ਕਾਲਾਂ ਕਰਕੇ ਥ੍ਰੈਡ ਪੂਲ ਖਤਮ ਹੋ ਗਿਆ ਜੋ v3.2 ਵਿੱਚ ਸ਼ਾਮਲ ਕੀਤੀਆਂ ਗਈਆਂ।"

**ਏਜੰਟ ਜਵਾਬ ਦਿੰਦਾ ਹੈ:**

> **ਕਾਰਜਕਾਰੀ ਸੰਖੇਪ:**
> - **ਕੀ ਵਾਪਰਿਆ:** ਤਾਜ਼ਾ ਰਿਲੀਜ਼ ਦੇ ਬਾਅਦ ਸਿਸਟਮ ਸੁਸਤ ਹੋ ਗਿਆ।
> - **ਕਾਰੋਬਾਰੀ ਪ੍ਰਭਾਵ:** ਕੁਝ ਯੂਜ਼ਰਾਂ ਨੂੰ ਸੇਵਾ ਦੇ ਉਪਯੋਗ ਦੌਰਾਨ ਦੇਰੀ ਦਾ ਅਨੁਭਵ ਹੋਇਆ।
> - **ਅਗਲਾ ਕਦਮ:** ਬਦਲਾਵ ਵਾਪਸ ਲਿਆ ਜਾ ਚੁੱਕਾ ਹੈ ਅਤੇ ਡਿਪਲੌਮੈਂਟ ਤੋਂ ਪਹਿਲਾਂ ਇੱਕ ਫਿਕਸ ਤਿਆਰ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ।

### ਇਹ ਏਜੰਟ ਕਿਉਂ?

ਇਹ ਇਕ ਸਧਾਰਣ, ਇੱਕ ਹੀ ਮਕਸਦ ਵਾਲਾ ਏਜੰਟ ਹੈ - ਜੋ ਹੋਸਟਡ ਏਜੰਟ ਵਰਕਫਲੋ ਨੂੰ ਅੰਤ ਤੋਂ ਅੰਤ ਤੱਕ ਸਿੱਖਣ ਲਈ ਬਿਲਕੁਲ ਠੀਕ ਹੈ ਬਿਨਾ ਜਟਿਲ ਉਦਯੋਗਾਂ ਵਿੱਚ ਲੱਪੇ ਪਏ। ਅਤੇ ਇਮਾਨਦਾਰੀ ਨਾਲ ਕਹਿਣਾ ਹੈ? ਹਰ ਏਂਜੀਨੀਅਰਿੰਗ ਟੀਮ ਨੂੰ ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਇੱਕ ਦੀ ਲੋੜ ਹੈ।

---

## ਵਰਕਸ਼ਾਪ ਦੀ ਬਣਤਰ

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

> **ਨੋਟ:** ਹਰ ਲੈਬ ਵਿਚਕਾਰ `agent/` ਫੋਲਡਰ ਉਹ ਹੈ ਜੋ **ਮਾਇਕਰੋਸੌਫਟ ਫਊਂਡਰੀ ਇਕਸਟੈਂਸ਼ਨ** ਜਨਰੇਟ ਕਰਦਾ ਹੈ ਜਦੋਂ ਤੁਸੀਂ ਕਮਾਂਡ ਪੈਲੇਟ ਤੋਂ `Microsoft Foundry: Create a New Hosted Agent` ਚਲਾਉਂਦੇ ਹੋ। ਫਾਇਲਾਂ ਫਿਰ ਤੁਹਾਡੇ ਏਜੰਟ ਦੇ ਨਿਰਦੇਸ਼ਾਂ, ਟੂਲ ਅਤੇ ਕਾਨਫਿਗਰੇਸ਼ਨ ਨਾਲ ਕਸਟਮਾਈਜ਼ ਕੀਤੀਆਂ ਜਾਂਦੀਆਂ ਹਨ। ਲੈਬ 01 ਤੁਸੀਂ ਇਸਨੂੰ ਜ਼ੀਰੋ ਤੋਂ ਤੇਆਰ ਕਰਨਾ ਸਿਖਾਉਂਦਾ ਹੈ।

---

## ਸ਼ੁਰੂਆਤ

### 1. ਰਿਪੋਜ਼ਿਟਰੀ ਕਲੋਨ ਕਰੋ

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. ਪਾਇਥਨ ਵਰਚੁਅਲ ਵਾਤਾਵਰਣ ਸੈੱਟ ਕਰੋ

```bash
python -m venv venv
```

ਇਸਨੂੰ ਐਕਟਿਵ ਕਰੋ:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. ਨਿਰਭਰਤਾਵਾਂ ਇੰਸਟਾਲ ਕਰੋ

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. ਵਾਤਾਵਰਣ ਚਰ (Environment Variables) ਸੈੱਟ ਕਰੋ

ਏਜੰਟ ਫੋਲਡਰ ਦੇ ਅੰਦਰ `.env` ਫਾਈਲ ਦੀ ਨਕਲ ਕਰੋ ਅਤੇ ਆਪਣੇ ਮੁੱਲ ਭਰੋ:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` ਫਾਈਲ ਸੰਪਾਦਿਤ ਕਰੋ:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. ਵਰਕਸ਼ਾਪ ਲੈਬਾਂ ਦੀ ਪਾਲਣਾ ਕਰੋ

ਹਰ ਲੈਬ ਆਪਣੇ ਮੋਡੀਊਲਾਂ ਨਾਲ ਸਵੈ-ਨਿਰਭਰ ਹੈ। ਪ੍ਰਾਰੰਭ ਕਰਨ ਲਈ **ਲੈਬ 01** ਨੂੰ ਕਰੋ, ਫਿਰ ਮਲਟੀ-ਏਜੰਟ ਵਰਕਫਲੋ ਲਈ **ਲੈਬ 02** 'ਤੇ ਜਾਓ।

#### ਲੈਬ 01 - ਸਿੰਗਲ ਏਜੰਟ ([ਪੂਰੀ ਹਦਾਇਤਾਂ](workshop/lab01-single-agent/README.md))

| # | ਮੋਡੀਊਲ | ਲਿੰਕ |
|---|--------|------|
| 1 | ਜਰੂਰੀਆਂ ਪੜ੍ਹੋ | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | ਫਊਂਡਰੀ ਟੂਲਕਿਟ ਅਤੇ ਫਊਂਡਰੀ ਇਕਸਟੈਂਸ਼ਨ ਇੰਸਟਾਲ ਕਰੋ | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | ਫਊਂਡਰੀ ਪ੍ਰਾਜੈਕਟ ਬਣਾਓ | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | ਇੱਕ ਹੋਸਟਡ ਏਜੰਟ ਬਣਾਓ | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | ਦਿਸ਼ਾ-ਨਿਰਦੇਸ਼ਾਂ ਅਤੇ ਵਾਤਾਵਰਣ ਦੀ ਕਾਨਫਿਗਰੇਸ਼ਨ ਕਰੋ | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | ਸਥਾਨਕ ਟੈਸਟ ਕਰੋ | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | ਫਊਂਡਰੀ ਤੇ ਡਿਪਲੌ ਕਰੋ | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | ਪਲੇਗ੍ਰਾਊਂਡ ਵਿੱਚ ਜਾਂਚ ਕਰੋ | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | ਸਮੱਸਿਆ ਹੱਲ | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### ਲੈਬ 02 - ਮਲਟੀ-ਏਜੰਟ ਵਰਕਫਲੋ ([ਪੂਰੀ ਹਦਾਇਤਾਂ](workshop/lab02-multi-agent/README.md))

| # | ਮੋਡੀਊਲ | ਲਿੰਕ |
|---|--------|------|
| 1 | ਜਰੂਰੀਆਂ (ਲੈਬ 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | ਮਲਟੀ-ਏਜੰਟ ਸਰੰਜਾਮ ਨੂੰ ਸਮਝੋ | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | ਮਲਟੀ-ਏਜੰਟ ਪ੍ਰਾਜੈਕਟ ਨੂੰ ਸਕੈਫੋਲਡ ਕਰੋ | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | ਏਜੰਟ ਅਤੇ ਵਾਤਾਵਰਣ ਦੀ ਕਾਨਫਿਗਰੇਸ਼ਨ ਕਰੋ | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | ਆਰਕੇਸਟਰੈਸ਼ਨ ਪੈਟਰਨ | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | ਸਥਾਨਕ ਟੈਸਟ (ਮਲਟੀ-ਏਜੰਟ) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | ਫਾਊਂਡਰੀ 'ਤੇ ਤਾਇਨਾਤ ਕਰੋ | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | ਪਲੇਗ੍ਰਾਊਂਡ ਵਿੱਚ ਜਾਂਚੋ | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | ਸਮੱਸਿਆ ਨਿਵਾਰਨ (ਮਲਟੀ ਏਜਂਟ) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## ਮੈਨਟੇਨਰ

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>ਸ਼ਿਵਮ ਗੋਯਲ</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## ਲੋੜੀਂਦੇ ਅਧਿਕਾਰ (ਤੁਰੰਤ ਹਵਾਲਾ)

| ਸਥਿਤੀ | ਲੋੜੀਂਦੇ ਭੂਮਿਕਾਵਾਂ |
|----------|---------------|
| ਨਵਾਂ ਫਾਊਂਡਰੀ ਪ੍ਰੋਜੈਕਟ ਬਣਾਓ | ਫਾਊਂਡਰੀ ਸਰੋਤ 'ਤੇ **ਅਜ਼ੂਰ ਏਆਈ ਮਾਲਕ** |
| ਮੌਜੂਦਾ ਪ੍ਰੋਜੈਕਟ ਵਿੱਚ ਤਾਇਨਾਤ ਕਰੋ (ਨਵੇਂ ਸਰੋਤ) | ਸਬਸਕ੍ਰਿਪਸ਼ਨ 'ਤੇ **ਅਜ਼ੂਰ ਏਆਈ ਮਾਲਕ** + **ਯੋਗਦਾਨਕਾਰ** |
| ਪੂਰੀ ਤਰ੍ਹਾਂ ਸੰਰਚਿਤ ਪ੍ਰੋਜੈਕਟ ਵਿੱਚ ਤਾਇਨਾਤ ਕਰੋ | ਖਾਤੇ 'ਤੇ **ਰੀਡਰ** + ਪ੍ਰੋਜੈਕਟ 'ਤੇ **ਅਜ਼ੂਰ ਏਆਈ ਯੂਜ਼ਰ** |

> **ਮਹੱਤਵਪੂਰਨ:** ਅਜ਼ੂਰ `ਮਾਲਿਕ` ਅਤੇ `ਯੋਗਦਾਨਕਾਰ` ਭੂਮਿਕਾਵਾਂ ਸਿਰਫ਼ *ਪ੍ਰਬੰਧਨ* ਅਧਿਕਾਰ ਸ਼ਾਮਲ ਕਰਦੀਆਂ ਹਨ, ਨਾ ਕਿ *ਵਿਕਾਸ* (ਡਾਟਾ ਐਕਸ਼ਨ) ਅਧਿਕਾਰ। ਤੁਹਾਨੂੰ ਏਜੰਟ ਬਣਾਉਣ ਅਤੇ ਤਾਇਨਾਤ ਕਰਨ ਲਈ **ਅਜ਼ੂਰ ਏਆਈ ਯੂਜ਼ਰ** ਜਾਂ **ਅਜ਼ੂਰ ਏਆਈ ਮਾਲਕ** ਦੀ ਲੋੜ ਹੈ।

---

## ਸੰਦਰਭ

- [ਤੀਬਰ ਸ਼ੁਰੂਆਤ: ਆਪਣਾ ਪਹਿਲਾ ਹੋਸਟਡ ਏਜੰਟ ਤਾਇਨਾਤ ਕਰੋ (VS ਕੋਡ)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [ਹੋਸਟਡ ਏਜੰਟ ਕੀ ਹਨ?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS ਕੋਡ ਵਿੱਚ ਹੋਸਟਡ ਏਜੰਟ ਵਰਕਫਲੋ ਬਣਾਓ](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [ਹੋਸਟਡ ਏਜੰਟ ਤਾਇਨਾਤ ਕਰੋ](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [ਮਾਈਕਰੋਸਾਫਟ ਫਾਊਂਡਰੀ ਲਈ RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [ਆਰਕੀਟੈਕਚਰ ਰਿਵਿਊ ਏਜੰਟ ਨਮੂਨਾ](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP ਟੂਲਾਂ, ਐਕਸਕੈਲੀਡਰਾਵ ਡਾਇਗ੍ਰਾਮਾਂ ਅਤੇ ਦੁਹਰਾ ਤਾਇਨਾਤੀਕਰਨ ਨਾਲ ਹਕੀਕਤੀ ਦੁਨੀਆ ਦਾ ਹੋਸਟਡ ਏਜੰਟ

---


## ਲਾਇਸੰਸ

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਪਣ**:
ਇਸ ਦਸਤਾਵੇਜ਼ ਦਾ ਅਨੁਵਾਦ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾਵਾਂ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮੱਤਿਆਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੇ ਉਪਯੋਗ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆਵਾਂ ਲਈ ਜਵਾਬਦੇਹ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->