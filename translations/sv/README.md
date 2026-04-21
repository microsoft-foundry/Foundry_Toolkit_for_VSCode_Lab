# Foundry Toolkit + Foundry Hosted Agents Workshop

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.0.0rc3-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents/)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Bygg, testa och distribuera AI-agenter till **Microsoft Foundry Agent Service** som **Hosted Agents** – helt från VS Code med hjälp av **Microsoft Foundry extension** och **Foundry Toolkit**.

> **Hosted Agents är för närvarande i förhandsgranskning.** Stödda regioner är begränsade – se [regiontillgänglighet](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Mappen `agent/` i varje labb skapas **automatiskt** av Foundry extension – du anpassar sedan koden, testar lokalt och distribuerar.

### 🌐 Fler språkstöd

#### Stöds via GitHub Action (Automatiserat & Alltid Uppdaterat)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](./README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Föredrar du att klona lokalt?**
>
> Detta repository inkluderar 50+ språköversättningar vilket markant ökar nedladdningsstorleken. För att klona utan översättningar, använd sparse checkout:
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
> Detta ger dig allt du behöver för att genomföra kursen med en mycket snabbare nedladdning.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arkitektur

```mermaid
flowchart TB
    subgraph Local["Lokal Utveckling (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Tillägg"]
        FoundryToolkit["Foundry Toolkit
        Tillägg"]
        Scaffold["Ramverk Agentkod
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agentinspektör
        (Lokal Testning)"]
        FE -- "Skapa Ny
        Hostad Agent" --> Scaffold
        Scaffold -- "F5 Felsök" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Register"]
        AgentService["Foundry Agenttjänst
        (Hostad Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Lekplats
        & VS Code Lekplats"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Distribuera
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Testa uppmaningar" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**Flöde:** Foundry extension skapar agenten → du anpassar koden & instruktionerna → testar lokalt med Agent Inspector → distribuerar till Foundry (Docker-image pushas till ACR) → verifierar i Playground.

---

## Vad du kommer bygga

| Labb | Beskrivning | Status |
|-----|-------------|--------|
| **Lab 01 - Enskild Agent** | Bygg **"Explain Like I'm an Executive" Agent**, testa lokalt och distribuera till Foundry | ✅ Tillgänglig |
| **Lab 02 - Multi-Agent Arbetsflöde** | Bygg **"Resume → Job Fit Evaluator"** – 4 agenter samarbetar för att poängsätta CV-passform och generera en lärande plan | ✅ Tillgänglig |

---

## Möt Executive Agent

I denna workshop bygger du **"Explain Like I'm an Executive" Agent** – en AI-agent som omvandlar svår teknisk jargong till lugna, styrelserumsfärdiga sammanfattningar. För ärligt talat, ingen i ledningsgruppen vill höra om "thread pool exhaustion orsakad av synkrona anrop införda i v3.2."

Jag skapade denna agent efter ett antal incidenter där min perfekt utformade post-mortem fick svaret: *"Så... är webbplatsen nere eller inte?"*

### Så fungerar det

Du matar in en teknisk uppdatering. Den levererar en ledningssammanfattning – tre punkter, ingen jargong, inga stacktraces, ingen existentiell ångest. Bara **vad som hände**, **affärspåverkan**, och **nästa steg**.

### Se den i aktion

**Du säger:**
> "API-latensen ökade på grund av thread pool exhaustion orsakad av synkrona anrop införda i v3.2."

**Agenten svarar:**

> **Sammanfattning för ledningen:**
> - **Vad som hände:** Efter senaste releasen blev systemet långsammare.
> - **Affärspåverkan:** Vissa användare upplevde förseningar vid användning av tjänsten.
> - **Nästa steg:** Ändringen har rullats tillbaka och en fix förbereds innan omdistribuering.

### Varför denna agent?

Den är enkel och har ett enda syfte – perfekt för att lära sig hosted agent-arbetsflödet från början till slut utan att fastna i komplexa verktygskedjor. Och ärligt talat? Varje teknikteam kan ha nytta av en sådan här.

---

## Workshopstruktur

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
├── 📂 ExecutiveAgent/                ← Standalone hosted agent project
│   ├── agent.yaml
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-install-foundry-toolkit.md
    │   │   ├── 02-create-foundry-project.md
    │   │   ├── 03-create-hosted-agent.md
    │   │   ├── 04-configure-and-code.md
    │   │   ├── 05-test-locally.md
    │   │   ├── 06-deploy-to-foundry.md
    │   │   ├── 07-verify-in-playground.md
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

> **Notera:** Mappen `agent/` i varje labb är vad **Microsoft Foundry extension** genererar när du kör `Microsoft Foundry: Create a New Hosted Agent` från Command Palette. Filernas innehåll anpassas sedan med agentens instruktioner, verktyg och konfiguration. Lab 01 visar hur du återskapar detta från grunden.

---

## Kom igång

### 1. Klona repositoryt

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Skapa en Python-virtuell miljö

```bash
python -m venv venv
```

Aktivera den:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Installera beroenden

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Konfigurera miljövariabler

Kopiera exempel `.env`-filen inuti agent-mappen och fyll i dina värden:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Redigera `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Följ workshop-labben

Varje labb är självständigt med egna moduler. Börja med **Lab 01** för att lära dig grunderna, sedan går du vidare till **Lab 02** för multi-agent arbetsflöden.

#### Lab 01 - Enskild Agent ([fullständiga instruktioner](workshop/lab01-single-agent/README.md))

| # | Modul | Länk |
|---|--------|------|
| 1 | Läs förutsättningar | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Installera Foundry Toolkit & Foundry extension | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Skapa ett Foundry-projekt | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | Skapa en hosted agent | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | Konfigurera instruktioner & miljö | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | Testa lokalt | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Distribuera till Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verifiera i playground | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | Felsökning | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Multi-Agent Arbetsflöde ([fullständiga instruktioner](workshop/lab02-multi-agent/README.md))

| # | Modul | Länk |
|---|--------|------|
| 1 | Förutsättningar (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Förstå multi-agent arkitektur | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Skapa multi-agent projekt | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Konfigurera agenter & miljö | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Orkestreringsmönster | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testa lokalt (multi-agent) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Distribuera till Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verifiera i lekplatsen | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Felsökning (fleragent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Underhållare

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

## Krävs behörigheter (snabbreferens)

| Scenario | Krävs roller |
|----------|--------------|
| Skapa nytt Foundry-projekt | **Azure AI Owner** på Foundry-resurs |
| Distribuera till befintligt projekt (nya resurser) | **Azure AI Owner** + **Contributor** på prenumerationen |
| Distribuera till fullt konfigurerat projekt | **Läsare** på konto + **Azure AI User** på projektet |

> **Viktigt:** Azure-rollerna `Owner` och `Contributor` inkluderar bara *hanterings*behörigheter, inte *utvecklings* (dataåtgärd) behörigheter. Du behöver **Azure AI User** eller **Azure AI Owner** för att bygga och distribuera agenter.

---

## Referenser

- [Snabbstart: Distribuera din första hostade agent (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Vad är hostade agenter?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Skapa arbetsflöden för hostad agent i VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Distribuera en hostad agent](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC för Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Architecture Review Agent Sample](https://github.com/Azure-Samples/agent-architecture-review-sample) - Verklighetsbaserad hostad agent med MCP-verktyg, Excalidraw-diagram och dubbel distribution

---

## Licens

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi eftersträvar noggrannhet, bör du vara medveten om att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för eventuella missförstånd eller feltolkningar som uppstår vid användning av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->