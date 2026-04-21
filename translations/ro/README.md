# Foundry Toolkit + Atelierul Agenților Găzduiți Foundry

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

Construiește, testează și implementează agenți AI în **Microsoft Foundry Agent Service** ca **Agenți Găzduiți** - integral din VS Code folosind **extensia Microsoft Foundry** și **Foundry Toolkit**.

> **Agenții Găzduiți sunt momentan în versiune preview.** Regiunile suportate sunt limitate - vezi [disponibilitatea pe regiuni](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Folderul `agent/` din fiecare laborator este **generat automat** de extensia Foundry - apoi personalizezi codul, testezi local și implementezi.

### 🌐 Suport Multi-Limbaj

#### Suportat prin GitHub Action (Automatizat & Întotdeauna Actualizat)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](./README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Preferi să clonezi local?**
>
> Acest depozit conține peste 50 de traduceri în limbi diferite, ceea ce crește semnificativ dimensiunea descărcării. Pentru a clona fără traduceri, folosește sparse checkout:
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
> Aceasta îți oferă tot ce ai nevoie pentru a finaliza cursul cu o descărcare mult mai rapidă.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arhitectură

```mermaid
flowchart TB
    subgraph Local["Dezvoltare locală (VS Code)"]
        direction TB
        FE["Extensie Microsoft Foundry"]
        FoundryToolkit["Extensie Foundry Toolkit"]
        Scaffold["Cod Agent Șablon
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Inspector Agent
        (Testare Locală)"]
        FE -- "Creează Agent Gazduit Nou" --> Scaffold
        Scaffold -- "Debug F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Registru Container Azure"]
        AgentService["Serviciu Agent Foundry
        (Execuție Agent Gazduit)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Implementare
    (Construire + push Docker)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Testează prompturi" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**Flux:** Extensia Foundry generează scheletul agentului → tu personalizezi codul și instrucțiunile → testezi local cu Agent Inspector → implementezi în Foundry (imaginea Docker este împinsă în ACR) → verifici în Playground.

---

## Ce vei construi

| Laborator | Descriere | Stare |
|-----|-------------|--------|
| **Laborator 01 - Agent Simplu** | Construiește agentul **"Explică-mi ca unui Director Executiv"**, testează-l local și implementează-l în Foundry | ✅ Disponibil |
| **Laborator 02 - Flux Multi-Agent** | Construiește evaluatorul **"CV → Potrivire Job"** - 4 agenți colaborează pentru a evalua potrivirea CV-ului și a genera un plan de învățare | ✅ Disponibil |

---

## Cunoaște Agentul Executiv

În acest atelier vei construi agentul **"Explică-mi ca unui Director Executiv"** - un agent AI care preia jargon tehnic dificil și îl traduce în rezumate calme, gata pentru sala de ședințe. Pentru că, să fim sinceri, nimeni din echipa de conducere nu vrea să audă despre „exhaustarea thread pool-ului cauzată de apeluri sincronizate introduse în v3.2.”

Am creat acest agent după prea multe situații în care postul meu post-mortem perfect redactat a primit răspunsul: *„Deci... site-ul este jos sau nu?”*

### Cum funcționează

Îi dai o actualizare tehnică. El îți oferă un rezumat executiv - trei puncte esențiale, fără jargon, fără trasee de stivă, fără teamă existențială. Doar **ce s-a întâmplat**, **impactul asupra afacerii** și **următorul pas**.

### Vezi-l în acțiune

**Spui tu:**
> „Latenta API a crescut din cauza exhaustării thread pool-ului cauzate de apeluri sincronizate introduse în v3.2.”

**Agentul răspunde:**

> **Rezumat Executiv:**
> - **Ce s-a întâmplat:** După ultima actualizare, sistemul a încetinit.
> - **Impact asupra afacerii:** Unii utilizatori au întâmpinat întârzieri în utilizarea serviciului.
> - **Următorul pas:** Modificarea a fost anulată și se pregătește o remediere înainte de implementare.

### De ce acest agent?

Este un agent foarte simplu, cu un singur scop - perfect pentru a învăța fluxul de lucru pentru agenți găzduiți de la cap la coadă fără a fi copleșit de lanțuri complexe de instrumente. Și sincer? Orice echipă de inginerie ar putea folosi unul ca acesta.

---

## Structura atelierului

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

> **Notă:** Folderul `agent/` din fiecare laborator este ceea ce generează **extensia Microsoft Foundry** când rulezi `Microsoft Foundry: Create a New Hosted Agent` din Command Palette. Fișierele sunt apoi personalizate cu instrucțiunile, uneltele și configurația pentru agentul tău. Laboratorul 01 te ghidează să recreezi acest proces de la zero.

---

## Începutul

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

Copiază fișierul exemplu `.env` din folderul agent și completează valorile tale:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Editează `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Urmează laboratoarele atelierului

Fiecare laborator este autonom cu propriile module. Începe cu **Laborator 01** pentru a învăța elementele de bază, apoi treci la **Laborator 02** pentru fluxuri multi-agent.

#### Laborator 01 - Agent Simplu ([instrucțiuni complete](workshop/lab01-single-agent/README.md))

| # | Modul | Link |
|---|--------|------|
| 1 | Citește precondițiile | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Instalează Foundry Toolkit & extensia Foundry | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Creează un proiect Foundry | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | Creează un agent găzduit | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | Configurează instrucțiunile și mediul | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | Testează local | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Implementează în Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verifică în playground | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | Depanare | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Laborator 02 - Flux Multi-Agent ([instrucțiuni complete](workshop/lab02-multi-agent/README.md))

| # | Modul | Link |
|---|--------|------|
| 1 | Precondiții (Laborator 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Înțelege arhitectura multi-agent | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Generează proiectul multi-agent | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Configurează agenții și mediul | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Modele de orchestrare | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testează local (multi-agent) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Implementare în Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verificare în playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Depanare (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

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
|----------|-----------------|
| Crearea unui nou proiect Foundry | **Azure AI Owner** pe resursa Foundry |
| Implementare în proiect existent (resurse noi) | **Azure AI Owner** + **Contributor** pe abonament |
| Implementare în proiect complet configurat | **Reader** pe cont + **Azure AI User** pe proiect |

> **Important:** Rolurile `Owner` și `Contributor` din Azure includ doar permisiuni de *gestionare*, nu permisiuni de *dezvoltare* (acțiuni de date). Ai nevoie de **Azure AI User** sau **Azure AI Owner** pentru a construi și implementa agenți.

---

## Referințe

- [Pornire rapidă: Implementați primul agent gazduit (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Ce sunt agenții găzduiți?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Crearea workflow-urilor pentru agenți găzduiți în VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Implementarea unui agent găzduit](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC pentru Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Exemplu Agent de Revizuire a Arhitecturii](https://github.com/Azure-Samples/agent-architecture-review-sample) - Agent găzduit real cu instrumente MCP, diagrame Excalidraw și implementare duală

---

## Licență

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim pentru acuratețe, vă rugăm să aveți în vedere că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite rezultate din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->