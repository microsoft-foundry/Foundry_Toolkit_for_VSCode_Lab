# Foundry Toolkit + Workshop hostovaných agentů Foundry

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

Vytvářejte, testujte a nasazujte AI agenty do **Microsoft Foundry Agent Service** jako **hostované agenty** – vše přímo z VS Code pomocí **rozšíření Microsoft Foundry** a **Foundry Toolkit**.

> **Hostovaní agenti jsou momentálně v režimu preview.** Podporované oblasti jsou omezené – viz [dostupnost oblastí](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Složka `agent/` v každé laboratoři je **automaticky vytvořena** rozšířením Foundry – potom upravujete kód, testujete lokálně a nasazujete.

### 🌐 Podpora více jazyků

#### Podporováno přes GitHub Action (automatizováno a vždy aktuální)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabština](../ar/README.md) | [Bengálština](../bn/README.md) | [Bulharština](../bg/README.md) | [Barmština (Myanmar)](../my/README.md) | [Čínština (zjednodušená)](../zh-CN/README.md) | [Čínština (tradiční, Hong Kong)](../zh-HK/README.md) | [Čínština (tradiční, Macau)](../zh-MO/README.md) | [Čínština (tradiční, Taiwan)](../zh-TW/README.md) | [Chorvatština](../hr/README.md) | [Čeština](./README.md) | [Dánština](../da/README.md) | [Nizozemština](../nl/README.md) | [Estonština](../et/README.md) | [Finština](../fi/README.md) | [Francouzština](../fr/README.md) | [Němčina](../de/README.md) | [Řečtina](../el/README.md) | [Hebrejština](../he/README.md) | [Hindština](../hi/README.md) | [Maďarština](../hu/README.md) | [Indonéština](../id/README.md) | [Italština](../it/README.md) | [Japonština](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korejština](../ko/README.md) | [Litevština](../lt/README.md) | [Malajština](../ms/README.md) | [Malajalámština](../ml/README.md) | [Maráthština](../mr/README.md) | [Nepálština](../ne/README.md) | [Nigerijská pidžinština](../pcm/README.md) | [Norština](../no/README.md) | [Perština (Fársí)](../fa/README.md) | [Polština](../pl/README.md) | [Portugalština (Brazílie)](../pt-BR/README.md) | [Portugalština (Portugalsko)](../pt-PT/README.md) | [Punjábština (Gurmukhí)](../pa/README.md) | [Rumunština](../ro/README.md) | [Ruština](../ru/README.md) | [Srbština (cyrilice)](../sr/README.md) | [Slovenština](../sk/README.md) | [Slovinština](../sl/README.md) | [Španělština](../es/README.md) | [Suahelština](../sw/README.md) | [Švédština](../sv/README.md) | [Tagalog (filipínština)](../tl/README.md) | [Tamilština](../ta/README.md) | [Telugu](../te/README.md) | [Thajština](../th/README.md) | [Turečtina](../tr/README.md) | [Ukrajinština](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamština](../vi/README.md)

> **Chcete raději klonovat lokálně?**
>
> Toto repo obsahuje více než 50 jazykových překladů, což výrazně zvyšuje velikost stahování. Pro klonování bez překladů použijte sparse checkout:
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
> Toto vám poskytne vše potřebné ke zvládnutí kurzu s podstatně rychlejším stažením.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Architektura

```mermaid
flowchart TB
    subgraph Local["Místní Vývoj (VS Code)"]
        direction TB
        FE["Rozšíření Microsoft Foundry"]
        FoundryToolkit["Rozšíření Foundry Toolkit"]
        Scaffold["Vygenerovaný Kód Agenta
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Inspektor Agenta
        (Místní Testování)"]
        FE -- "Vytvořit Nového
        Hostovaného Agenta" --> Scaffold
        Scaffold -- "Ladění F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Kontejnerový
        Registr"]
        AgentService["Služba Agenta Foundry
        (Runtime Hostovaného Agenta)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Hřiště
        & VS Code Hřiště"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Nasadit
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Testovat výzvy" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**Tok:** Rozšíření Foundry vytváří kostru agenta → upravujete kód a instrukce → lokálně testujete s Agent Inspector → nasazujete do Foundry (Docker image je nahrán do ACR) → ověřujete ve Playgroundu.

---

## Co postavíte

| Laboratoř | Popis | Stav |
|-----------|--------|------|
| **Laboratoř 01 - Jendotlivý agent** | Vytvořte **agent "Vysvětli to jako vedoucímu"**, vyzkoušejte ho lokálně a nasazujte do Foundry | ✅ K dispozici |
| **Laboratoř 02 - Víceagentový pracovní postup** | Vytvořte **"Hodnocení životopisu → shoda s pozicí"** - 4 agenti spolupracují na hodnocení životopisu a generují vzdělávací plán | ✅ K dispozici |

---

## Seznamte se s agentem pro vedoucí

V tomto workshopu vytvoříte **agenta "Vysvětli to jako vedoucímu"** – AI agenta, který vezme složitý technický žargon a přeloží jej do klidných, připravených boardroomových souhrnů. Protože buďme upřímní, nikdo v C-suite nechce slyšet o „vyčerpání thread poolu způsobeném synchronními voláními zavedenými ve verzi 3.2.“

Tento agent vznikl po příliš mnoha případech, kdy moje dokonale připravená post-mortem zpráva byla přijata odpovědí: *„Takže… web je mimo provoz, nebo ne?“*

### Jak to funguje

Dáte mu technickou zprávu. On vám vrátí výkonný souhrn – tři odrážky, žádný žargon, žádné stack trace, žádnou existenciální úzkost. Jen **co se stalo**, **dopad na byznys** a **další krok**.

### Uvidíte ho v akci

**Řeknete:**
> „Latence API se zvýšila kvůli vyčerpání thread poolu způsobenému synchronními voláními zavedenými ve verzi 3.2.“

**Agent odpoví:**

> **Výkonný souhrn:**
> - **Co se stalo:** Po posledním vydání se systém zpomalil.
> - **Dopad na byznys:** Někteří uživatelé zažili zpoždění při používání služby.
> - **Další krok:** Změna byla vrácena zpět a připravuje se oprava před opětovným nasazením.

### Proč tento agent?

Je to velmi jednoduchý, jednoprofilový agent – ideální pro osvojení workflow hostovaných agentů od začátku do konce bez zbytečného složitého řetězce nástrojů. A upřímně? Každý tým vývojářů by mohl takového agenta využít.

---

## Struktura workshopu

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

> **Poznámka:** Složka `agent/` v každé laboratoři je to, co **rozšíření Microsoft Foundry** vygeneruje, když spustíte `Microsoft Foundry: Create a New Hosted Agent` z příkazové palety. Soubory se pak upravují s instrukcemi, nástroji a konfigurací vašeho agenta. Laboratoř 01 vás provede vytvořením od začátku.

---

## Začínáme

### 1. Klonujte repozitář

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Nastavte Python virtuální prostředí

```bash
python -m venv venv
```

Aktivujte ho:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Nainstalujte závislosti

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Nakonfigurujte proměnné prostředí

Zkopírujte ukázkový soubor `.env` ve složce agenta a vyplňte své hodnoty:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Upravte `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Sledujte laboratoře workshopu

Každá laboratoř je samostatná s vlastním modulem. Začněte s **Laboratoří 01**, naučte se základy, pak pokračujte do **Laboratoře 02** pro vícero agentů.

#### Laboratoř 01 - Jednotlivý agent ([plný návod](workshop/lab01-single-agent/README.md))

| # | Modul | Odkaz |
|---|--------|-------|
| 1 | Přečtěte si předpoklady | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Nainstalujte Foundry Toolkit & Foundry extension | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Vytvořte Foundry projekt | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | Vytvořte hostovaného agenta | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | Nakonfigurujte instrukce & prostředí | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | Testujte lokálně | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Nasazujte do Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Ověřte ve playgroundu | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | Řešení problémů | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Laboratoř 02 - Víceagentový pracovní postup ([plný návod](workshop/lab02-multi-agent/README.md))

| # | Modul | Odkaz |
|---|--------|-------|
| 1 | Předpoklady (Laboratoř 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Pochopení architektury více agentů | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Vytvoření víceagentového projektu | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Konfigurace agentů & prostředí | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Vzory orchestrací | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testování lokálně (více agentů) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Nasazení do Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Ověření v playgroundu | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Řešení problémů (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Správce

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

## Požadovaná oprávnění (rychlá reference)

| Scénář | Požadované role |
|----------|---------------|
| Vytvoření nového projektu Foundry | **Azure AI Owner** u Foundry zdroje |
| Nasazení do existujícího projektu (nové zdroje) | **Azure AI Owner** + **Contributor** u předplatného |
| Nasazení do plně nakonfigurovaného projektu | **Reader** na účtu + **Azure AI User** v projektu |

> **Důležité:** Role Azure `Owner` a `Contributor` zahrnují pouze *správcovská* oprávnění, nikoli *vývojová* (akcí s daty). K vytváření a nasazení agentů potřebujete **Azure AI User** nebo **Azure AI Owner**.

---

## Odkazy

- [Rychlý start: Nasazení vašeho prvního hostovaného agenta (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Co jsou hostovaní agenti?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Vytváření workflow hostovaných agentů ve VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Nasazení hostovaného agenta](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC pro Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Ukázkový agent pro revizi architektury](https://github.com/Azure-Samples/agent-architecture-review-sample) - Skutečný hostovaný agent s nástroji MCP, diagramy Excalidraw a dvojím nasazením

---


## Licence

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o vyloučení odpovědnosti**:
Tento dokument byl přeložen pomocí automatického překladatelského nástroje [Co-op Translator](https://github.com/Azure/co-op-translator). I když usilujeme o přesnost, mějte prosím na paměti, že automatické překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakákoliv nedorozumění nebo nesprávné výklady vyplývající z použití tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->