# Zestaw narzędzi Foundry + Warsztat Agentów Hostowanych Foundry

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

Buduj, testuj i wdrażaj agentów AI do **Microsoft Foundry Agent Service** jako **Hostowanych Agentów** – całkowicie z VS Code przy użyciu **rozszerzenia Microsoft Foundry** i **Zestawu narzędzi Foundry**.

> **Hostowani Agenci są obecnie w wersji zapoznawczej.** Obsługiwane regiony są ograniczone – zobacz [dostępność regionów](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Folder `agent/` w każdym laboratorium jest **automatycznie generowany** przez rozszerzenie Foundry – następnie dostosowujesz kod, testujesz lokalnie i wdrażasz.

### 🌐 Obsługa wielu języków

#### Obsługiwane poprzez GitHub Action (Automatyczne i zawsze aktualne)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabski](../ar/README.md) | [Bengalski](../bn/README.md) | [Bułgarski](../bg/README.md) | [Birmański (Myanmar)](../my/README.md) | [Chiński (uproszczony)](../zh-CN/README.md) | [Chiński (tradycyjny, Hongkong)](../zh-HK/README.md) | [Chiński (tradycyjny, Makau)](../zh-MO/README.md) | [Chiński (tradycyjny, Tajwan)](../zh-TW/README.md) | [Chorwacki](../hr/README.md) | [Czeski](../cs/README.md) | [Duński](../da/README.md) | [Holenderski](../nl/README.md) | [Estoński](../et/README.md) | [Fiński](../fi/README.md) | [Francuski](../fr/README.md) | [Niemiecki](../de/README.md) | [Grecki](../el/README.md) | [Hebrajski](../he/README.md) | [Hindi](../hi/README.md) | [Węgierski](../hu/README.md) | [Indonezyjski](../id/README.md) | [Włoski](../it/README.md) | [Japoński](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreański](../ko/README.md) | [Litewski](../lt/README.md) | [Malajski](../ms/README.md) | [Malajalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalski](../ne/README.md) | [Nigeryjski pidżyn](../pcm/README.md) | [Norweski](../no/README.md) | [Perski (farsi)](../fa/README.md) | [Polski](./README.md) | [Portugalski (Brazylia)](../pt-BR/README.md) | [Portugalski (Portugalia)](../pt-PT/README.md) | [Pendżabski (gurmukhi)](../pa/README.md) | [Rumuński](../ro/README.md) | [Rosyjski](../ru/README.md) | [Serbski (cyrylica)](../sr/README.md) | [Słowacki](../sk/README.md) | [Słoweński](../sl/README.md) | [Hiszpański](../es/README.md) | [Suahili](../sw/README.md) | [Szwedzki](../sv/README.md) | [Tagalog (filipiński)](../tl/README.md) | [Tami'lski](../ta/README.md) | [Telugu](../te/README.md) | [Tajski](../th/README.md) | [Turecki](../tr/README.md) | [Ukraiński](../uk/README.md) | [Urdu](../ur/README.md) | [Wietnamski](../vi/README.md)

> **Wolisz klonować lokalnie?**
>
> To repozytorium zawiera ponad 50 tłumaczeń językowych, co znacznie zwiększa rozmiar pobierania. Aby sklonować bez tłumaczeń, użyj sparse checkout:
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
> To zapewnia wszystko, czego potrzebujesz do ukończenia kursu, z dużo szybszym pobieraniem.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Architektura

```mermaid
flowchart TB
    subgraph Local["Lokalny rozwój (VS Code)"]
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
        Scaffold -- "Debugowanie F5" --> Inspector
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
    (localhost:8088)" --> Szkielet
    Playground -- "Testuj podpowiedzi" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Przepływ:** rozszerzenie Foundry generuje szkic agenta → dostosowujesz kod i instrukcje → testujesz lokalnie za pomocą Agent Inspector → wdrażasz do Foundry (obraz Dockera pushowany do ACR) → weryfikujesz na placu zabaw.

---

## Co zbudujesz

| Laboratorium | Opis | Status |
|-----|-------------|--------|
| **Laboratorium 01 - Pojedynczy Agent** | Zbuduj agenta **"Wyjaśnij jak dla Dyrektora"**, przetestuj lokalnie i wdroż do Foundry | ✅ Dostępne |
| **Laboratorium 02 - Przepływ wieloagentowy** | Zbuduj **"Oceniacz dopasowania CV → stanowiska"** - 4 agenci współpracują, aby ocenić dopasowanie CV i wygenerować plan nauki | ✅ Dostępne |

---

## Poznaj agenta dyrektora

W tym warsztacie zbudujesz agenta **"Wyjaśnij jak dla Dyrektora"** - agenta AI, który przetwarza skomplikowany żargon techniczny i tłumaczy go na spokojne, gotowe na zebranie streszczenia. Bo bądźmy szczerzy, nikt w zarządzie nie chce słuchać o „wyczerpaniu puli wątków spowodowanym synchronicznymi wywołaniami wprowadzonymi w wersji 3.2.”

Zbudowałem tego agenta po zbyt wielu sytuacjach, gdy moje perfekcyjnie przygotowane post-mortem zostało przyjęte odpowiedzią: *"To... strona jest nieaktywna czy nie?"*

### Jak to działa

Wprowadzasz aktualizację techniczną. Agent odsyła streszczenie dla zarządu – trzy punkty, bez żargonu, bez śladów stosu, bez egzystencjalnego przerażenia. Tylko **co się stało**, **wpływ na biznes** i **kolejny krok**.

### Zobacz to w akcji

**Mówisz:**
> "Opóźnienie API wzrosło z powodu wyczerpania puli wątków spowodowanego synchronicznymi wywołaniami wprowadzonymi w wersji 3.2."

**Agent odpowiada:**

> **Streszczenie dla zarządu:**
> - **Co się stało:** Po ostatniej aktualizacji system spowolnił.
> - **Wpływ na biznes:** Niektórzy użytkownicy doświadczyli opóźnień przy korzystaniu z usługi.
> - **Kolejny krok:** Zmiana została wycofana, a naprawa jest przygotowywana przed ponownym wdrożeniem.

### Dlaczego ten agent?

To prosty, jednofunkcyjny agent – idealny do nauki przepływu pracy hostowanego agenta od początku do końca bez zagłębiania się w skomplikowane narzędzia. I szczerze? Każdy zespół inżynierów mógłby takiego potrzebować.

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

> **Uwaga:** Folder `agent/` w każdym laboratorium jest tym, co generuje **rozszerzenie Microsoft Foundry**, gdy uruchamiasz `Microsoft Foundry: Create a New Hosted Agent` z palety poleceń. Pliki są następnie dostosowywane za pomocą instrukcji, narzędzi i konfiguracji twojego agenta. Laboratorium 01 przeprowadzi cię krok po kroku przez odtworzenie tego od zera.

---

## Zacznijmy

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

Skopiuj przykładowy plik `.env` do folderu agenta i uzupełnij swoje wartości:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Edytuj `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Postępuj zgodnie z laboratoriami warsztatu

Każde laboratorium jest samodzielne z własnymi modułami. Zacznij od **Laboratorium 01**, aby poznać podstawy, a następnie przejdź do **Laboratorium 02** dla przepływów wieloagentowych.

#### Laboratorium 01 - Pojedynczy Agent ([pełne instrukcje](workshop/lab01-single-agent/README.md))

| # | Moduł | Link |
|---|--------|------|
| 1 | Przeczytaj wymagania wstępne | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Zainstaluj Foundry Toolkit i rozszerzenie Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Utwórz projekt Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Utwórz hostowanego agenta | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Skonfiguruj instrukcje i środowisko | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Testuj lokalnie | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Wdróż do Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Sprawdź w placu zabaw | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Rozwiązywanie problemów | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Laboratorium 02 - Przepływ wieloagentowy ([pełne instrukcje](workshop/lab02-multi-agent/README.md))

| # | Moduł | Link |
|---|--------|------|
| 1 | Wymagania wstępne (Laboratorium 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Zrozum architekturę wieloagentową | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Utwórz szkic projektu wieloagentowego | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Skonfiguruj agentów i środowisko | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Wzorce orkiestracji | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testuj lokalnie (wieloagentowo) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Wdróż do Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Sprawdź na placu zabaw | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Rozwiązywanie problemów (wielu agentów) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

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
| Utwórz nowy projekt Foundry | **Azure AI Owner** w zasobie Foundry |
| Wdróż do istniejącego projektu (nowe zasoby) | **Azure AI Owner** + **Contributor** w subskrypcji |
| Wdróż do w pełni skonfigurowanego projektu | **Czytelnik** na koncie + **Azure AI User** w projekcie |

> **Ważne:** Role `Owner` i `Contributor` w Azure obejmują tylko uprawnienia *zarządcze*, nie *deweloperskie* (akcje na danych). Do budowy i wdrażania agentów potrzebujesz **Azure AI User** lub **Azure AI Owner**.

---

## Odniesienia

- [Szybki start: Wdróż swojego pierwszego hostowanego agenta (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Czym są hostowani agenci?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Twórz workflow dla hostowanych agentów w VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Wdróż hostowanego agenta](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC dla Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Przykład agenta do przeglądu architektury](https://github.com/Azure-Samples/agent-architecture-review-sample) - Hostowany agent z narzędziami MCP, diagramami Excalidraw i podwójnym wdrożeniem

---


## Licencja

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->