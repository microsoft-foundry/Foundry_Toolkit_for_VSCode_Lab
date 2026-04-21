# Foundry Toolkit + Workshop Agenti Hosted Foundry

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

Costruisci, testa e distribuisci agenti AI su **Microsoft Foundry Agent Service** come **Agenti Hosted** - interamente da VS Code usando l'**estensione Microsoft Foundry** e il **Foundry Toolkit**.

> **Gli Agenti Hosted sono attualmente in anteprima.** Le regioni supportate sono limitate - vedi [disponibilità delle regioni](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> La cartella `agent/` all'interno di ogni laboratorio è **automaticamente generata** dall’estensione Foundry - poi personalizzi il codice, testi localmente e distribuisci.

### 🌐 Supporto Multilingue

#### Supportato tramite GitHub Action (Automatizzato & Sempre Aggiornato)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabo](../ar/README.md) | [Bengalese](../bn/README.md) | [Bulgaro](../bg/README.md) | [Birmano (Myanmar)](../my/README.md) | [Cinese (Semplificato)](../zh-CN/README.md) | [Cinese (Tradizionale, Hong Kong)](../zh-HK/README.md) | [Cinese (Tradizionale, Macao)](../zh-MO/README.md) | [Cinese (Tradizionale, Taiwan)](../zh-TW/README.md) | [Croato](../hr/README.md) | [Ceco](../cs/README.md) | [Danese](../da/README.md) | [Olandese](../nl/README.md) | [Estone](../et/README.md) | [Finlandese](../fi/README.md) | [Francese](../fr/README.md) | [Tedesco](../de/README.md) | [Greco](../el/README.md) | [Ebraico](../he/README.md) | [Hindi](../hi/README.md) | [Ungherese](../hu/README.md) | [Indonesiano](../id/README.md) | [Italiano](./README.md) | [Giapponese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malese](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalese](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Norvegese](../no/README.md) | [Persiano (Farsi)](../fa/README.md) | [Polacco](../pl/README.md) | [Portoghese (Brasile)](../pt-BR/README.md) | [Portoghese (Portogallo)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumeno](../ro/README.md) | [Russo](../ru/README.md) | [Serbo (Cirillico)](../sr/README.md) | [Slovacco](../sk/README.md) | [Sloveno](../sl/README.md) | [Spagnolo](../es/README.md) | [Swahili](../sw/README.md) | [Svedese](../sv/README.md) | [Tagalog (Filippino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tailandese](../th/README.md) | [Turco](../tr/README.md) | [Ucraino](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **Preferisci Clonare Localmente?**
>
> Questo repository include oltre 50 traduzioni linguistiche che aumentano significativamente la dimensione del download. Per clonare senza traduzioni, usa sparse checkout:
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
> Questo ti dà tutto il necessario per completare il corso con un download molto più veloce.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Architettura

```mermaid
flowchart TB
    subgraph Local["Sviluppo Locale (VS Code)"]
        direction TB
        FE["Estensione Microsoft Foundry"]
        FoundryToolkit["Estensione Foundry Toolkit"]
        Scaffold["Codice Agente Scaffoldato
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Inspector Agente
        (Test Locale)"]
        FE -- "Crea Nuovo
        Agente Ospitato" --> Scaffold
        Scaffold -- "Debug F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Registro Contenitori Azure"]
        AgentService["Servizio Agente Foundry
        (Runtime Agente Ospitato)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (build + push Docker)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Testa prompt" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**Flusso:** L'estensione Foundry genera lo scheletro dell'agente → personalizzi codice e istruzioni → testi localmente con Agent Inspector → distribuisci su Foundry (immagine Docker inviata su ACR) → verifichi nel Playground.

---

## Cosa costruirai

| Laboratorio | Descrizione | Stato |
|-------------|-------------|-------|
| **Lab 01 - Agente Singolo** | Costruisci l'**Agente "Spiega come se fossi un dirigente"**, testalo localmente e distribuiscilo su Foundry | ✅ Disponibile |
| **Lab 02 - Flusso di lavoro Multi-Agente** | Costruisci il **"Valutatore Curriculum → Adattamento al Lavoro"** - 4 agenti collaborano per valutare l'idoneità del curriculum e generare una roadmap di apprendimento | ✅ Disponibile |

---

## Incontra l'Agente Executive

In questo workshop costruirai l'**Agente "Spiega come se fossi un dirigente"** - un agente AI che prende gergo tecnico complicato e lo traduce in riassunti calmi, pronti per la sala del consiglio. Perché diciamolo, nessuno nel C-suite vuole sentire parlare di "esaurimento del thread pool causato da chiamate sincrone introdotte in v3.2."

Ho costruito questo agente dopo troppi incidenti in cui il mio post-mortem perfettamente elaborato riceveva la risposta: *"Quindi... il sito è giù o no?"*

### Come funziona

Gli fornisci un aggiornamento tecnico. Lui restituisce un sommario esecutivo - tre punti chiave, niente gergo, niente tracce dello stack, niente angoscia esistenziale. Solo **cosa è successo**, **impatto sul business**, e **prossimo passo**.

### Vedi in azione

**Tu dici:**
> "La latenza dell'API è aumentata a causa dell'esaurimento del thread pool causato da chiamate sincrone introdotte in v3.2."

**L'agente risponde:**

> **Sommario esecutivo:**
> - **Cosa è successo:** Dopo l'ultimo rilascio, il sistema ha rallentato.
> - **Impatto sul business:** Alcuni utenti hanno riscontrato ritardi nell'uso del servizio.
> - **Prossimo passo:** La modifica è stata annullata e si sta preparando una correzione prima della nuova distribuzione.

### Perché questo agente?

È un agente semplice, con uno scopo unico - perfetto per imparare il flusso di lavoro dell'agente hosted da cima a fondo senza complicarsi con catene di strumenti complesse. E onestamente? Ogni team di ingegneri potrebbe usarne uno così.

---

## Struttura del workshop

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

> **Nota:** La cartella `agent/` all’interno di ogni laboratorio è ciò che genera l’**estensione Microsoft Foundry** quando esegui `Microsoft Foundry: Create a New Hosted Agent` dalla Command Palette. I file sono quindi personalizzati con le istruzioni, gli strumenti e la configurazione dell'agente. Il Lab 01 ti guida a ricreare questo da zero.

---

## Primo avvio

### 1. Clona il repository

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Configura un ambiente virtuale Python

```bash
python -m venv venv
```

Attivalo:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Installa le dipendenze

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Configura le variabili d’ambiente

Copia il file `.env` di esempio dentro la cartella agente e inserisci i tuoi valori:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Modifica `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Segui i laboratori del workshop

Ogni laboratorio è autonomo con i suoi moduli. Inizia con **Lab 01** per apprendere le basi, poi passa a **Lab 02** per i flussi multi-agente.

#### Lab 01 - Agente Singolo ([istruzioni complete](workshop/lab01-single-agent/README.md))

| # | Modulo | Link |
|---|--------|------|
| 1 | Leggi i prerequisiti | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Installa Foundry Toolkit & estensione Foundry | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Crea un progetto Foundry | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | Crea un agente hosted | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | Configura istruzioni & ambiente | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | Testa localmente | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Distribuisci su Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verifica nel playground | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | Risoluzione problemi | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Flusso di lavoro Multi-Agente ([istruzioni complete](workshop/lab02-multi-agent/README.md))

| # | Modulo | Link |
|---|--------|------|
| 1 | Prerequisiti (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Comprendere l’architettura multi-agente | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Genera lo scheletro del progetto multi-agente | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Configura agenti & ambiente | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Pattern di orchestrazione | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testa localmente (multi-agente) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Distribuire su Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verifica nel playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Risoluzione problemi (multi-agente) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Responsabile

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

## Permessi richiesti (riferimento rapido)

| Scenario | Ruoli richiesti |
|----------|-----------------|
| Creare un nuovo progetto Foundry | **Proprietario Azure AI** sulla risorsa Foundry |
| Distribuire su progetto esistente (nuove risorse) | **Proprietario Azure AI** + **Collaboratore** sulla sottoscrizione |
| Distribuire su progetto completamente configurato | **Lettore** sull'account + **Utente Azure AI** sul progetto |

> **Importante:** I ruoli Azure `Proprietario` e `Collaboratore` includono solo permessi di *gestione*, non permessi di *sviluppo* (azione dati). Hai bisogno di **Utente Azure AI** o **Proprietario Azure AI** per costruire e distribuire agenti.

---

## Riferimenti

- [Avvio rapido: Distribuisci il tuo primo agente ospitato (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Cosa sono gli agenti ospitati?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Crea flussi di lavoro per agenti ospitati in VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Distribuisci un agente ospitato](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC per Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Esempio agente revisione architettura](https://github.com/Azure-Samples/agent-architecture-review-sample) - Agente ospitato reale con strumenti MCP, diagrammi Excalidraw e doppia distribuzione

---

## Licenza

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avvertenza**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per l'accuratezza, ti preghiamo di considerare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda la traduzione professionale umana. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall'uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->