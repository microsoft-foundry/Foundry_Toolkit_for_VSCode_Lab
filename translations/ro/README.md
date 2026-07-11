# Foundry Toolkit + Atelierul Agenților Găzduiți Foundry

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

Construiește, testează și implementează agenți AI în **Microsoft Foundry Agent Service** ca **Agenți Găzduiți** - totul din VS Code folosind extensia **Microsoft Foundry** și **Foundry Toolkit**.

> **Agenții Găzduiți sunt în prezent în previzualizare.** Regiunile suportate sunt limitate - vezi [disponibilitatea regiunilor](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Folderul `agent/` din fiecare laborator este **generat automat** de extensia Foundry - apoi personalizezi codul, testezi local și implementezi.

### 🌐 Suport Multi-Limbaj

#### Suportat prin GitHub Action (automatizat și mereu actualizat)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](./README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Preferi să clonezi local?**
>
> Acest depozit include peste 50 de traduceri de limbaje, ceea ce mărește semnificativ mărimea descărcării. Pentru a clona fără traduceri, folosește sparse checkout:
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
> Acest lucru îți oferă tot ce ai nevoie pentru a finaliza cursul cu o descărcare mult mai rapidă.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arhitectură

```mermaid
flowchart TB
    subgraph Local["Dezvoltare Locală (VS Code)"]
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
        Scaffold -- "Depanare F5" --> Inspector
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
    (localhost:8088)" --> Schelet
    Playground -- "Testează prompturi" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Flux:** Extensia Foundry generează schema agentului → personalizezi codul și instrucțiunile → testezi local cu Agent Inspector → implementezi în Foundry (imagine Docker împinsă în ACR) → verifici în Playground.

---

## Ce vei construi

| Laborator | Descriere | Stare |
|-----|-------------|--------|
| **Laborator 01 - Agent Unic** | Construieste agentul **"Explică ca și cum aș fi un director executiv"**, testează-l local și implementează-l în Foundry | ✅ Disponibil |
| **Laborator 02 - Flux Multi-Agent** | Construiește **"Evaluatorul de potrivire CV → Job"** - 4 agenți colaborează pentru a evalua potrivirea CV-ului și a genera un plan de învățare | ✅ Disponibil |

---

## Cunoaște Agentul Executiv

În acest atelier vei construi agentul **"Explică ca și cum aș fi un director executiv"** - un agent AI care ia jargonul tehnic complicat și îl traduce în rezumate calme, gata pentru sala de consiliu. Pentru că să fim cinstiți, nimeni din C-suite nu vrea să audă despre „exhaustarea pool-ului de fire cauzată de apeluri sincrone introduse în v3.2.”

Am construit acest agent după prea multe incidente în care raportul meu post-mortem perfect elaborat a primit răspunsul: *„Deci... site-ul e jos sau nu?”*

### Cum funcționează

Îi dai o actualizare tehnică. Îți returnează un rezumat executiv - trei puncte esențiale, fără jargon, fără urme de cod, fără teamă existențială. Doar **ce s-a întâmplat**, **impactul asupra afacerii** și **următorul pas**.

### Vezi-l în acțiune

**Tu spui:**
> "Latenta API a crescut din cauza epuizării pool-ului de fire cauzată de apeluri sincrone introduse în v3.2."

**Agentul răspunde:**

> **Rezumat executiv:**
> - **Ce s-a întâmplat:** După ultima lansare, sistemul a încetinit.
> - **Impact asupra afacerii:** Unii utilizatori au avut întârzieri în folosirea serviciului.
> - **Următorul pas:** Schimbarea a fost anulată și se pregătește o soluție înainte de relansare.

### De ce acest agent?

Este un agent simplu, cu un singur scop - perfect pentru a învăța fluxul de lucru al agenților găzduiți de la început până la sfârșit fără a fi copleșit de lanțuri de unelte complexe. Și sincer? Fiecare echipă de ingineri ar putea folosi unul ca acesta.

---

## Structura atelierului

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

> **Notă:** Folderul `agent/` din fiecare laborator este ceea ce generează **extensia Microsoft Foundry** când rulezi `Microsoft Foundry: Create a New Hosted Agent` din Command Palette. Fișierele sunt apoi personalizate cu instrucțiunile, uneltele și configurația agentului tău. Laboratorul 01 te ghidează să recreezi acest lucru de la zero.

---

## Începutul lucrului

### 1. Clonează depozitul

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Configurează un mediu virtual Python

```bash
python -m venv venv
```

Activează-l:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalează dependențele

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Configurează variabilele de mediu

Copiază fișierul exemplar `.env` din folderul agent și completează valorile tale:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Editează `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Urmează laboratoarele atelierului

Fiecare laborator este autonom cu propriile module. Începe cu **Laboratorul 01** pentru a învăța elementele fundamentale, apoi continuă cu **Laboratorul 02** pentru fluxuri multi-agent.

#### Laborator 01 - Agent Unic ([instrucțiuni complete](workshop/lab01-single-agent/README.md))

| # | Modul | Link |
|---|--------|------|
| 1 | Citește prerechizitele | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Instalează Foundry Toolkit & extensia Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Creează un proiect Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Creează un agent găzduit | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Configurează instrucțiunile & mediul | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Testează local | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Implementează în Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Verifică în playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Depanare | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Laborator 02 - Flux Multi-Agent ([instrucțiuni complete](workshop/lab02-multi-agent/README.md))

| # | Modul | Link |
|---|--------|------|
| 1 | Prerechizite (Laborator 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Înțelege arhitectura multi-agent | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Generează structura proiectului multi-agent | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Configurează agenții și mediul | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Modele de orchestrare | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testează local (multi-agent) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Implementare în Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verificare în playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Rezolvarea problemelor (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Administrator

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

## Permisiuni necesare (referință rapidă)

| Scenariu | Roluri necesare |
|----------|---------------|
| Crearea unui nou proiect Foundry | **Azure AI Owner** pe resursa Foundry |
| Implementare în proiect existent (resurse noi) | **Azure AI Owner** + **Contributor** pe abonament |
| Implementare în proiect complet configurat | **Reader** pe cont + **Azure AI User** pe proiect |

> **Important:** Rolurile Azure `Owner` și `Contributor` includ doar permisiuni de *management*, nu permisiuni de *dezvoltare* (acțiuni pe date). Ai nevoie de **Azure AI User** sau **Azure AI Owner** pentru a construi și implementa agenți.

---

## Referințe

- [Start rapid: Implementează primul tău agent găzduit (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Ce sunt agenții găzduiți?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Creează fluxuri de lucru pentru agenți găzduiți în VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Implementează un agent găzduit](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC pentru Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Exemplu Agent Review Arhitectură](https://github.com/Azure-Samples/agent-architecture-review-sample) - Agent găzduit din lumea reală cu instrumente MCP, diagrame Excalidraw și implementare duală

---


## Licență

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->