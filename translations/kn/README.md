# ಫೌಂಡ್ರಿ ಟೂಲ್‌ಕಿಟ್ + ಫೌಂಡ್ರಿ ಹೋಸ್ಟ್ ಆಗಂಟ್‌ಗಳ ಕಾರ್ಯಾಗារ

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

**Microsoft Foundry Agent Service** ಗೆ **Hosted Agents** ಆಗಿ AI ಆಗಂಟ್‌ಗಳನ್ನು ನಿರ್ಮಿಸಿ, ಪರೀಕ್ಷಿಸಿ, ಮತ್ತು ನಿಯೋಜಿಸಿ - ಸಂಪೂರ್ಣವಾಗಿ VS ಕೋಡ್‌ನಿಂದ **Microsoft Foundry ಎಕ್ಸ್ಟೆನ್ಷನ್** ಮತ್ತು **Foundry Toolkit** ಬಳಸಿ.

> **Hosted Agents ಪ್ರಸ್ತುತ ಪೂರ್ವದೃಶ್ಯದಲ್ಲಿ ಇದೆ.** ಬೆಂಬಲಿತ ಪ್ರದೇಶಗಳು ಮಿತವಾಗಿವೆ - [ಪ್ರದೇಶ ಲಭ್ಯತೆ](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ಅನ್ನು ನೋಡಿ.

> ಪ್ರತಿಯೊಂದು ಪ್ರಯೋಗಾಲಯದಲ್ಲಿಯೂ `agent/` ಫೋಲ್ಡರ್ **Foundry ಎಕ್ಸ್ಟೆನ್ಷನ್** ಮೂಲಕ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಸೃಷ್ಟಿಯಾಗುತ್ತದೆ - ನಂತರ ನೀವು ಕೋಡ್ ಅನ್ನು ಕಸ್ಟಮೈಸ್ ಮಾಡಿ, ಸ್ಥಳೀಯವಾಗಿ ಪರೀಕ್ಷಿಸಿ, ಮತ್ತು ನಿಯೋಜನೆಯನ್ನು ಮಾಡಬಹುದು.

### 🌐 ಬಹುಭಾಷಾ ಬೆಂಬಲ

#### ಗಿತ್ಹಬ್ ಕ್ರಿಯೆ ಮೂಲಕ ಬೆಂಬಲಿಸಲಾಗಿದೆ (ಆಟೋಮೇಟೆಡ್ & ಸದಾ ಅಪ್ಟುಡೇಟ್)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](./README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ಸ್ಥಳೀಯ ಎಂದನ್ನೂ ಕ್ಲೋನ್ ಮಾಡಬೇಕೆ?**
>
> ಈ ರೆಪೊಜಿಟರಿ 50+ ಭಾಷಾ ಅನುವಾದಗಳನ್ನು ಹೊಂದಿದ್ದು, ಡೌನ್‌ಲೋಡ್ ಗಾತ್ರವನ್ನು ಬಹಳ ಹೆಚ್ಚಿಸುತ್ತದೆ. ಅನುವಾದಗಳಿಲ್ಲದೆ ಕ್ಲೋನ್ ಮಾಡಲು, ಸ್ಫಾರ್ಸ್ ಚೆಕ್‌ಔಟ್ ಬಳಸಿ:
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
> ಇದರಿಂದ ನೀವು ಕೋರ್ಸ್ ಪೂರ್ಣಗೊಳಿಸಲು ಅಗತ್ಯವಿರುವ ಎಲ್ಲವನ್ನೂ ನೋಂದಣಿ ವೇಗವರ್ಧಿತವಾಗಿ ಪಡೆಯಬಹುದು.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## ವಾಸ್ತುಶಿಲ್ಪ

```mermaid
flowchart TB
    subgraph Local["ಸ್ಥಳೀಯ ಅಭಿವೃದ್ಧಿ (VS ಕೋಡ್)"]
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
        Scaffold -- "F5 ಡಿಬಗ್" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["ಮೈಕ್ರೋಸಾಫ್ಟ್ ಫೌಂಡ್ರಿ"]
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
    (localhost:8088)" --> ಮಾದರಿ ರಚನೆ
    Playground -- "ಪರೀಕ್ಷಾ ಪ್ರಾಂಪ್ಟ್‌ಗಳು" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**ಪ್ರವಾಹ:** Foundry ಎಕ್ಸ್ಟೆನ್ಷನ್ ಆಗಂಟ್ ಅನ್ನು ನಿರ್ಮಿಸುತ್ತದೆ → ನೀವು ಕೋಡ್ ಮತ್ತು ಸೂಚನೆಗಳನ್ನು ಕಸ್ಟಮೈಸ್ ಮಾಡುತ್ತೀರಿ → Agent Inspector ಜೊತೆ ಸ್ಥಳೀಯವಾಗಿ ಪರೀಕ್ಷಿಸಿ → Foundry ಗೆ ನಿಯೋಜಿಸಿ (Docker ಇಮೇಜ್ ಅನ್ನು ACR ಗೆ पुಷ್ ಮಾಡುತ್ತದೆ) → Playground ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ.

---

## ನೀವು ನಿರ್ಮಿಸುವುದು

| ಪ್ರಯೋಗಾಲಯ | ವಿವರಣೆ | ಸ್ಥಿತಿ |
|-----|-------------|--------|
| **Prayog 01 - Single Agent** | **"ನಾನು ಕಾರ್ಯನಿರ್ವಾಹಕನಾಗಿದ್ದೇನೆ" ಅಂತದಾಗಿಸಿ** ಆಗಂಟ್ ನಿರ್ಮಿಸಿ, ಸ್ಥಳೀಯವಾಗಿ ಪರೀಕ್ಷಿಸಿ, ಮತ್ತು Foundry ಗೆ ನಿಯೋಜಿಸಿ | ✅ ಲಭ್ಯವಿದೆ |
| **Prayog 02 - ಬಹು ಆಗಂಟ್ ಕಾರ್ಯಪ್ರವಾಹ** | **"ರೆಸ್ಯುಮೆ → ಕೆಲಸದ ಹೊಂದಾಣಿಕೆಯ ಮೌಲ್ಯಮಾಪನ"** - 4 ಆಗಂಟ್ಸ್ ರೆಸ್ಯುಮೆ ಹೊಂದಾಣಿಕೆಯ ಅಂಕಗಳನ್ನು ನೀಡಲು ಮತ್ತು ಕಲಿಕಾ ರಸ್ತೆ ನಕ್ಷೆಯನ್ನು ರಚಿಸಲು ಸಹಕರಿಸುತ್ತವೆ | ✅ ಲಭ್ಯವಿದೆ |

---

## ಕಾರ್ಯನಿರ್ವಾಹಕ ಆಗಂಟ್ ಅನ್ನು ಭೇಟಿಗೊಳ್ಳಿ

ಈ ಕಾರ್ಯಾಗಾರದಲ್ಲಿ ನೀವು **"ನಾನು ಕಾರ್ಯನಿರ್ವಾಹಕನಾಗಿದ್ದೇನೆ" ಅಂತದಾಗಿಸಿ** ಆಗಂಟ್ ಅನ್ನು ನಿರ್ಮಿಸುವಿರಿ - ತಂತ್ರಜ್ಞಾನಿ ಜಾರ್ಗಾನ್ ಅನ್ನು ಬೋರ್ಡ್‌ರೂಮ್‌ಗೆ ತಯಾರಾದ ಸಂಕ್ಷಿಪ್ತಗಳಲ್ಲಿ ಪರಿವರ್ತಿಸುವ AI ಆಗಂಟ್. ಏಕೆಂದರೆ ನಿಜವಾಗಲಿ, C- ಸೀಟ್ ನಲ್ಲಿ ಯಾರೂ "v3.2 ನಲ್ಲಿ ಪರಿಚಯಿಸಿದ ಸಮಕಾಲಿಕ ಕರೆಗಳಿಂದ ಉಂಟಾದ ಥ್ರೆಡ್ ಪೂಲ್ ಕೊನಸು" ಕುರಿತು ಕೇಳಲು ಇಚ್ಛಿಸುವುದಿಲ್ಲ.

ನಾನು ಈ ಆಗಂಟ್ ಅನ್ನು ಅನೇಕ ಘಟನೆಗಳ ನಂತರ ನಿರ್ಮಿಸಿದೆ, ನನ್ನ ಪರಿಪೂರ್ಣವಾಗಿ ರচিত ಪೋಸ್ಟ್-ಮೊರ್ಟಮ್‌ಗೆ ಉತ್ತರವಾಗಿ: *"ಹೌದು... ವೆಬ್‌ಸೈಟ್ ಕೆಲಸ ಮಾಡುತ್ತಿದೆಯೇ ಇಲ್ಲವೆ?"*

### ಅದು ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ

ನೀವು 技术 ಸುಧಾರಣೆಯನ್ನು ನೀಡುತ್ತೀರಿ. ಇದು ಮೂರು ಸುಲಭ ಬಿಂದುಗಳಾದ ಕಾರ್ಯನಿರ್ವಾಹಕ ಸಾರಾಂಶವನ್ನು ಹಿಂತಿರುಗಿಸುತ್ತದೆ - ಯಾರಾದರೂ ತುಮುಕತಟ್ಯದಿಲ್ಲ, ಸ್ಟ್ಯಾಕ್ ಟ್ರೇಸ್ ಇಲ್ಲ, ಅಸ್ತಿತ್ವಭೀತಿಯಿಲ್ಲ. ಕೇವಲ **ಏನಾಯಿತು**, **ವ್ಯವಹಾರ ಪ್ರಭಾವ**, ಮತ್ತು **ಮುಂದಿನ ಹಂತ**.

### ಇದನ್ನು ಪ್ರಾಯೋಗಿಕವಾಗಿ ನೋಡಿರಿ

**ನೀವು ಹೇಳುತ್ತೀರಿ:**
> "API ವಿಳಂಬವು v3.2 ನಲ್ಲಿ ಪರಿಚಯಿಸಿದ ಸಮಕಾಲಿಕ ಕರೆಗಳಿಂದ ಉಂಟಾದ ಥ್ರೆಡ್ ಪೂಲ್ ಕೊನಸು ಕಾರಣ ಬಲಪಟ್ಟಿತು."

**ಆಗಂಟ್ ಪ್ರತಿಕ್ರಿಯಿಸುತ್ತದೆ:**

> **ಕಾರ್ಯನಿರ್ವಾಹಕ ಸಾರಾಂಶ:**
> - **ಏನಾಯಿತು:** ಇತ್ತೀಚಿನ ಬಿಡುಗಡೆಯಾದ ನಂತರ ವ್ಯವಸ್ಥೆ ನಿಧಾನವಾಯಿತು.
> - **ವ್ಯವಹಾರ ಪ್ರಭಾವ:** ಕೆಲವು ಬಳಕೆದಾರರು ಸೇವೆ ಬಳಸುವಾಗ ವಿಳಂಬಗಳನ್ನು ಅನುಭವಿಸಿದರು.
> - **ಮುಂದಿನ ಹಂತ:** ಬದಲಾವಣೆ ಹಿಂದಕ್ಕೆ ತರುವುದಾಗಿ ಮಾಡಲಾಗಿದೆ ಮತ್ತು ಪುನರ್ನಿಯೋಜನೆಯ ಮೊದಲು ದುರಸ್ತಿ ಪ್ರಸ್ತುತವಾಗುತ್ತಿದೆ.

### ಈ ಆಗಂಟ್ ಏಕೆ?

ಇದು ಸರಳ, ಏಕ ಉದ್ಯೇಶಿ ಆಗಂಟ್ - ಸಮಗ್ರವಾಗಿ ಹೋಸ್ಟ್ ಆಗಂಟ್ ಕಾರ್ಯಪ್ರವಾಹವನ್ನು ಕಲಿಯಲು ಪರಿಪೂರ್ಣ. ಮತ್ತು ನಿಜವಾಗಿಯೂ, ಪ್ರತಿ ಎಂಜಿನಿಯರಿಂಗ್ ತಂಡಕ್ಕೆ ಇಂತಹ ಒಂದು ಅಗತ್ಯವೇ.

---

## ಕಾರ್ಯಾಗಾರದ ರಚನೆ

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

> **ಟಿಪ್ಪಣಿ:** ಪ್ರತಿಯೊಂದು ಪ್ರಯೋಗಾಲಯದೊಳಗಿನ `agent/` ಫೋಲ್ಡರ್ ಅನ್ನು **Microsoft Foundry ಎಕ್ಸ್ಟೆನ್ಷನ್** ನೀವು ಕಮಾನ್ ಪ್ಯಾಲೆಟ್ನಿಂದ `Microsoft Foundry: Create a New Hosted Agent` ರನ್ ಮಾಡಿದಾಗ ಉತ್ಪಾದಿಸುತ್ತದೆ. ಫೈಲ್‌ಗಳನ್ನು ನಂತರ ನಿಮ್ಮ ಆಗಂಟ್ ಸೂಚನೆಗಳು, ಸಾಧನಗಳು ಮತ್ತು ಸಂರಚನೆಗಳೊಂದಿಗೆ ಕಸ್ಟಮೈಸ್ ಮಾಡಲಾಗುತ್ತದೆ. ಪ್ರಯೋಗಾಲಯ 01 ನಿಮಗೆ ಇದನ್ನು ಮೊದಲಿನಿಂದಲೇ ಸೃಷ್ಟಿಸುವುದನ್ನು ಕಲಿಸುತ್ತದೆ.

---

## ಪ್ರಾರಂಭಿಸುವುದು

### 1. ರೆಪೊಜಿಟರಿ ಕ್ಲೋನ್ ಮಾಡಿ

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. ಪೈಥಾನ್ ವರ್ಚುವಲ್ ಪರಿಸರವನ್ನು ಸಜ್ಜುಗೊಳಿಸಿ

```bash
python -m venv venv
```

ಅದನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. ಅವಲಂಬನೆಗಳನ್ನು ಸ್ಥಾಪಿಸಿ

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. ಪರಿಸರ ಬದಲಾವಣೆಗಳನ್ನು ಸಂರಚಿಸಿ

ಆಗಂಟ್ ಫೋಲ್ಡರ್ ಒಳಗಿನ `.env` ಉದಾಹರಣೆಯನ್ನು ನಕಲಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಮೌಲ್ಯಗಳನ್ನು ಪೂರೈಸಿ:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` ಅನ್ನು ಸಂಪಾದಿಸಿ:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. ಕಾರ್ಯಾಗಾರದ ಪ್ರಯೋಗಾಲಯಗಳನ್ನು ಅನುಸರಿಸಿ

ಪ್ರತಿ ಪ್ರಯೋಗಾಲಯವು ಸ್ವಂತ ಮಾಯಾಜಾಲಗಳೊಂದಿಗೆ ಸ್ವತಂತ್ರವಾಗಿದೆ. ಮೂಲಭೂತಗಳನ್ನು ಕಲಿಯಲು **Lab 01**ರಿಂದ ಪ್ರಾರಂಭಿಸಿ, ನಂತರ ಬಹು-ಆಗಂಟ್ ಕಾರ್ಯಪ್ರವಾಹಗಳಿಗೆ **Lab 02**ಗೆ ತೆರಳಿರಿ.

#### Lab 01 - Single Agent ([ಪೂರ್ಣ ಸೂಚನೆಗಳು](workshop/lab01-single-agent/README.md))

| # | ಮಾಯಾಜಾಲ | ಲಿಂಕ್ |
|---|--------|------|
| 1 | ಪೂರ್ವಾಪೇಕ್ಷತೆಗಳನ್ನು ಓದಿ | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry ಎಕ್ಸ್ಟೆನ್ಷನ್ ಅನ್ನು ಸ್ಥಾಪಿಸಿ | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Foundry ಪ್ರಾಜೆಕ್ಟ್ ಅನ್ನು ಸೃಷ್ಟಿಸಿ | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | ஹೋಸ್ಟ್ ಆಗಂಟ್ ಸೃಷ್ಟಿಸಿ | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | ಸೂಚನೆಗಳು ಮತ್ತು ಪರಿಸರವನ್ನು ಸಂರಚಿಸಿ | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | ಸ್ಥಳೀಯವಾಗಿ ಪರೀಕ್ಷಿಸಿ | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundry ಗೆ ನಿಯೋಜಿಸಿ | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | ಪ್ಲೆಗಳಾತ್ ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | ಸಮಸ್ಯಾ ಪರಿಹಾರ | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - ಬಹು-ಆಗಂಟ್ ಕಾರ್ಯಪ್ರವಾಹ ([ಪೂರ್ಣ ಸೂಚನೆಗಳು](workshop/lab02-multi-agent/README.md))

| # | ಮಾಯಾಜಾಲ | ಲಿಂಕ್ |
|---|--------|------|
| 1 | ಪೂರ್ವಾಪೇಕ್ಷತೆಗಳು (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | ಬಹು-ಆಗಂಟ್ ವಾಸ್ತುಶಿಲ್ಪವನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | ಬಹು-ಆಗಂಟ್ ಪ್ರಾಜೆಕ್ಟ್ ಅನ್ನು ನಿರ್ಮಿಸಿ | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | ಆಗಂಟ್‌ಗಳು ಮತ್ತು ಪರಿಸರವನ್ನು ಸಂರಚಿಸಿ | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | ಸಂಯೋಜನಾ ಮಾದರಿಗಳು | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | ಸ್ಥಳೀಯವಾಗಿ ಪರೀಕ್ಷಿಸಿ (ಬಹು-ಆಗಂಟ್) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | ಫೌಂಡ್‌ರಿಯಲ್ಲಿ ನಿಯೋಜಿಸಿ | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | ಪ್ಲೇಗ್ರೌಂಡ್‌ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | ಸಮಸ್ಯೆ ಪರಿಹಾರ (ಬಹು-ಏಜೆಂಟ್) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## ನಿರ್ವಹಣೆಗಾರ

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="ಶಿವಮ್ ಗೋಯಲ್"/><br />
        <sub><b>ಶಿವಮ್ ಗೋಯಲ್</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## ಅಗತ್ಯ ಅನುಮತಿಗಳು (ತ್ವರಿತ ಉಲ್ಲೇಖ)

| ಸನ್ನಿವೇಶ | ಅಗತ್ಯ ಪಾತ್ರಗಳು |
|----------|---------------|
| ಹೊಸ ಫೌಂಡ್‌ರಿಯಾ ಯೋಜನೆ ಸೃಷ್ಟಿಸಿ | ಫೌಂಡ್‌ರಿ ಸಂಪನ್ಮೂಲದಲ್ಲಿ **ಅಜೂರ್ ಏಐ ಮಾಲೀಕ** |
| υπάρχουσα ಯೋಜನೆಗೆ ನಿಯೋಜನೆ (ಹೊಸ ಸಂಪನ್ಮೂಲಗಳು) | ಚಂದಾದಾರಿಕೆಯಲ್ಲಿ **ಅಜೂರ್ ಏಐ ಮಾಲೀಕ** + **ದೇಣಿಗೆದಾರ** |
| ಸಂಪೂರ್ಣವಾಗಿ ಸಂರಚಿಸಲಾದ ಯೋಜನೆಗೆ ನಿಯೋಜನೆ | ಖಾತೆಯಲ್ಲಿ **ವಾಚಕ** + ಯೋಜನೆಯಲ್ಲಿ **ಅಜೂರ್ ಏಐ ಬಳಕೆದಾರ** |

> **ಮುಖ್ಯ:** ಅಜೂರ್ `ಮಾಲೀಕ` ಮತ್ತು `ದೇಣಿಗೆದಾರ` ಪಾತ್ರಗಳು ಕೇವಲ *ನಿರ್ವಹಣಾ* ಅನುವಾಗಿಗಳನ್ನು ಒಳಗೊಂಡಿವೆ, *ಅಭಿವೃದ್ದಿ* (ಡೇಟಾ ಕ್ರಿಯೆ) ಅನುಮತಿಗಳನ್ನು ಅಲ್ಲ. ಏಜೆಂಟ್‌ಗಳನ್ನು ನಿರ್ಮಿಸಲು ಮತ್ತು ನಿಯೋಜಿಸಲು ನಿಮಗೆ **ಅಜೂರ್ ಏಐ ಬಳಕೆದಾರ** ಅಥವಾ **ಅಜೂರ್ ಏಐ ಮಾಲೀಕ** ಅಗತ್ಯವಿದೆ.

---

## ಉಲ್ಲೇಖಗಳು

- [Quickstart: Deploy your first hosted agent (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [ಹೋಸ್ಟೆಡ್ ಏಜೆಂಟ್‌ಗಳೇನು?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS ಕೋಡ್‌ನಲ್ಲಿ ಹೋಸ್ಟೆಡ್ ಏಜೆಂಟ್ ಕಾರ್ಯಪ್ರವಾಹಗಳನ್ನು ರಚಿಸಿ](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [ಹೋಸ್ಟೆಡ್ ಏಜೆಂಟ್ ನಿಯೋಜಿಸಿ](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [ಮೈಕ್ರೋಸಾಫ್ಟ್ ಫೌಂಡ್‌ರಿಗಾಗಿ RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [ವಾಸ್ತವಿಕ ಲೋಕ ಹೋಸ್ಟೆಡ್ ಏಜೆಂಟ್ ಮಾದರಿ](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP ಸಾಧನಗಳು, ಎಕ್ಸ್ಕ್ಯಾಲಿಡ್ರಾ ಡಾಯಾಗ್ರಾಮ್‌ಗಳು ಮತ್ತು ಡುಯಲ್ ನಿಯೋಜನೆಯೊಂದಿಗೆ

---


## ಪರವಾನಗೆ

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ಅಸ್ವೀಕಾರ**:
ಈ ದಸ್ತಾವೇಜು AI ಅನುವಾದ ಸೇವೆ [Co-op Translator](https://github.com/Azure/co-op-translator) ಬಳಸಿ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ನಿಖರತೆಯನ್ನು ಸಾಧಿಸಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದರೂ, ದಯವಿಟ್ಟು ಗಮನಿಸಿ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ದೋಷಗಳು ಅಥವಾ ಅಸಡ್ಡೆಗಳು ಇರಬಹುದು. ಮೂಲ ಭಾಷೆಯಲ್ಲಿರುವ ಮೂಲ ದಸ್ತಾವೇಜು ಪ್ರಾಮಾಣಿಕ ಮೂಲವೆಂದು ಪರಿಗಣಿಸಬೇಕು. ಪ್ರಮುಖ ಮಾಹಿತಿಗಾಗಿ, ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ. ಈ ಅನುವಾದವನ್ನು ಬಳಸುವ ಮೂಲಕ ಉಂಟಾಗುವ ಯಾವುದೇ ತಪ್ಪು ಅರ್ಥಗಳ ಅಥವಾ ತಪ್ಪು ವ್ಯಾಖ್ಯಾನಗಳ ಬಗ್ಗೆ ನಾವು ಹೊಣೆಗಾರರಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->