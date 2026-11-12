# Warsztat Foundry Toolkit + Foundry Hosted Agents

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../../LICENSE)

Buduj, testuj i wdrażaj agentów AI do **Microsoft Foundry Agent Service** jako **Hosted Agents** - całkowicie z VS Code przy użyciu rozszerzenia **Microsoft Foundry** i **Foundry Toolkit**.

> **Hosted Agents are currently in preview.** Supported regions are limited - see [region availability](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> The `agent/` folder inside each lab is **automatically scaffolded** by the Foundry extension - you then customize the code, test locally, and deploy.

### 🌐 Obsługa wielu języków

#### Wspierane przez GitHub Action (automatyczne i zawsze aktualne)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabski](../ar/README.md) | [Bengalski](../bn/README.md) | [Bułgarski](../bg/README.md) | [Birmański (Myanmar)](../my/README.md) | [Chiński (uproszczony)](../zh-CN/README.md) | [Chiński (tradycyjny, Hong Kong)](../zh-HK/README.md) | [Chiński (tradycyjny, Macau)](../zh-MO/README.md) | [Chiński (tradycyjny, Taiwan)](../zh-TW/README.md) | [Chorwacki](../hr/README.md) | [Czeski](../cs/README.md) | [Duński](../da/README.md) | [Niderlandzki](../nl/README.md) | [Estoński](../et/README.md) | [Fiński](../fi/README.md) | [Francuski](../fr/README.md) | [Niemiecki](../de/README.md) | [Grecki](../el/README.md) | [Hebrajski](../he/README.md) | [Hindi](../hi/README.md) | [Węgierski](../hu/README.md) | [Indonezyjski](../id/README.md) | [Włoski](../it/README.md) | [Japoński](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreański](../ko/README.md) | [Litewski](../lt/README.md) | [Malajski](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalski](../ne/README.md) | [Pidgin nigeryjski](../pcm/README.md) | [Norweski](../no/README.md) | [Perski (Farsi)](../fa/README.md) | [Polski](./README.md) | [Portugalski (Brazylia)](../pt-BR/README.md) | [Portugalski (Portugalia)](../pt-PT/README.md) | [Pendżabski (Gurmukhi)](../pa/README.md) | [Rumuński](../ro/README.md) | [Rosyjski](../ru/README.md) | [Serbski (cyrylica)](../sr/README.md) | [Słowacki](../sk/README.md) | [Słoweński](../sl/README.md) | [Hiszpański](../es/README.md) | [Suahili](../sw/README.md) | [Szwedzki](../sv/README.md) | [Tagalog (filipiński)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tajski](../th/README.md) | [Turecki](../tr/README.md) | [Ukraiński](../uk/README.md) | [Urdu](../ur/README.md) | [Wietnamski](../vi/README.md)

> **Wolisz klonować lokalnie?**
>
> To repozytorium zawiera tłumaczenia na ponad 50 języków, co znacząco zwiększa rozmiar pobierania. Aby sklonować bez tłumaczeń, użyj sparse checkout:
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
> To daje wszystko, czego potrzebujesz, aby ukończyć kurs, przy znacznie szybszym pobieraniu.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Architektura

```mermaid
flowchart TB
    subgraph Local["Local Development (VS Code)"]
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
        Scaffold -- "F5 Debug" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
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
    (localhost:8088)" --> Scaffold
    Playground -- "Test prompts" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Przebieg:** Rozszerzenie Foundry tworzy szkielet agenta → dostosowujesz kod i instrukcje → testujesz lokalnie za pomocą Agent Inspector → wdrażasz do Foundry (obraz Dockera przesyłany do ACR) → weryfikujesz w Playground.

---

## Co zbudujesz

| Laboratorium | Opis | Status |
|-----|-------------|--------|
| **Lab 01 - Single Agent** | Zbuduj agenta **"Explain Like I'm an Executive"**, przetestuj go lokalnie i wdroż do Foundry | ✅ Dostępne |
| **Lab 02 - Multi-Agent Workflow** | Zbuduj **"Resume → Job Fit Evaluator"** - 4 agenci współpracują, aby ocenić dopasowanie CV i wygenerować plan nauki | ✅ Dostępne |

---

## Poznaj Agenta Executive

W tym warsztacie zbudujesz agenta **"Explain Like I'm an Executive"** - agenta AI, który bierze skomplikowany żargon techniczny i tłumaczy go na spokojne, gotowe na spotkanie zarządu podsumowania. Bądźmy szczerzy, nikt w kadrze kierowniczej nie chce słyszeć o "thread pool exhaustion caused by synchronous calls introduced in v3.2."

Zbudowałem tego agenta po zbyt wielu sytuacjach, w których moje perfekcyjnie przygotowane post-mortem spotykało się z odpowiedzią: *"So... is the website down or not?"*

### Jak to działa

Podajesz mu aktualizację techniczną. Zwraca streszczenie dla kadry zarządzającej - trzy punkty, bez żargonu, bez stack trace'ów, bez egzystencjalnego niepokoju. Tylko **co się stało**, **wpływ na biznes**, i **kolejny krok**.

### Zobacz w akcji

**Ty mówisz:**
> "Opóźnienie API wzrosło z powodu wyczerpania puli wątków spowodowanego synchronicznymi wywołaniami wprowadzonymi w v3.2."

**Agent odpowiada:**

> **Streszczenie wykonawcze:**
> - **Co się stało:** Po ostatnim wydaniu system zwolnił.
> - **Wpływ na biznes:** Niektórzy użytkownicy doświadczyli opóźnień podczas korzystania z usługi.
> - **Kolejny krok:** Zmiana została wycofana, a poprawka jest przygotowywana przed ponownym wdrożeniem.

### Dlaczego ten agent?

To prosty, jednozadaniowy agent - idealny do nauki pełnego procesu pracy z hosted agentami bez ugrzęźnięcia w złożonych łańcuchach narzędzi. I szczerze? Każdy zespół inżynierski mógłby mieć takiego.

---

## Struktura warsztatu

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

> **Uwaga:** Folder `agent/` w każdym laboratorium to to, co generuje rozszerzenie **Microsoft Foundry** po uruchomieniu `Microsoft Foundry: Create a New Hosted Agent` z palety poleceń. Pliki są następnie dostosowywane z instrukcjami, narzędziami i konfiguracją twojego agenta. Lab 01 przeprowadza cię przez odtworzenie tego od podstaw.

---

## Rozpoczęcie

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Skonfiguruj wirtualne środowisko Pythona

```bash
python -m venv venv
```

Aktywuj je:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Zainstaluj zależności

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Skonfiguruj zmienne środowiskowe

Skopiuj przykładowy plik `.env` do folderu agenta i wypełnij swoje wartości:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Edytuj `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Przejdź przez laboratoria warsztatu

Każde laboratorium jest samodzielne i ma własne moduły. Zacznij od **Lab 01**, aby poznać podstawy, a następnie przejdź do **Lab 02** dla wieloagentowych przepływów pracy.

#### Lab 01 - Single Agent ([pełne instrukcje](workshop/lab01-single-agent/README.md))

| # | Moduł | Link |
|---|--------|------|
| 1 | Przeczytaj wymagania wstępne | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Zainstaluj Foundry Toolkit i rozszerzenie Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Utwórz projekt Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Utwórz hosted agenta | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Skonfiguruj instrukcje i środowisko | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Przetestuj lokalnie | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Wdróż do Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Zweryfikuj w playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Rozwiązywanie problemów | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Multi-Agent Workflow ([pełne instrukcje](workshop/lab02-multi-agent/README.md))

| # | Moduł | Link |
|---|--------|------|
| 1 | Wymagania wstępne (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Zrozum architekturę wieloagentową | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Stwórz szkielet projektu wieloagentowego | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Skonfiguruj agentów i środowisko | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Wzorce orkiestracji | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testuj lokalnie (wieloagentowo) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Wdróż do Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Zweryfikuj w playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Rozwiązywanie problemów (wieloagentowe) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Opiekun

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## Wymagane uprawnienia (szybkie odniesienie)

| Scenariusz | Wymagane role |
|----------|---------------|
| Utwórz nowy projekt Foundry | **Azure AI Owner** na zasobie Foundry |
| Wdróż do istniejącego projektu (nowe zasoby) | **Azure AI Owner** + **Contributor** na subskrypcji |
| Wdróż do w pełni skonfigurowanego projektu | **Reader** na koncie + **Azure AI User** w projekcie |

> **Ważne:** Azure `Owner` i `Contributor` role only include *management* permissions, not *development* (data action) permissions. You need **Azure AI User** or **Azure AI Owner** to build and deploy agents.

---

## Odniesienia

- [Szybki start: Wdróż swojego pierwszego hostowanego agenta (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Czym są hostowani agenci?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Utwórz przepływy pracy hostowanych agentów w VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Wdróż hostowanego agenta](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC dla Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Przykład agenta przeglądu architektury](https://github.com/Azure-Samples/agent-architecture-review-sample) - Hostowany agent z prawdziwego świata z narzędziami MCP, diagramami Excalidraw i podwójnym wdrożeniem

---


## Licencja

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->
