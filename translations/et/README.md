# Foundry Toolkit + Foundry Hostitud Agentide Töötuba

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

Ehita, testi ja juuruta tehisintellekti agendid **Microsoft Foundry Agent Service**'i kui **hostitud agente** - täielikult VS Code'i kaudu kasutades **Microsoft Foundry laiendust** ja **Foundry Toolkit**i.

> **Hostitud agentid on hetkel eelvaates.** Toetatud piirkonnad on piiratud – vaata [piirkondade saadavust](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Igas töökohas olev kaust `agent/` on **automaatselt genereeritud** Foundry laienduse poolt - seejärel kohandad koodi, testid lokaalselt ja juurutad.

### 🌐 Mitmekeelne tugi

#### Toetatud GitHub Action'i kaudu (automatiseeritud ja alati ajakohane)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](./README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Manipuri (Meitei Mayek)](../mni/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Eelistad kohalikku kloonimist?**
>
> See hoidla sisaldab 50+ keele tõlget, mis suurendab allalaadimise mahtu märkimisväärselt. Kui soovid kloonida ilma tõlgeteta, kasuta sparse checkout’i:
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
> See annab sulle kõik vajaliku kursuse sooritamiseks palju kiirema allalaadimisega.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arhitektuur

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

**Voog:** Foundry laiendus loob agendi raamistiku → sina kohandad koodi ja juhiseid → testid lokaalselt Agent Inspectoriga → juurutad Foundrys (Docker pilt lükatakse ACR-i) → kontrollid Playgroundis.

---

## Mida sa ehitad

| Töökoda | Kirjeldus | Staatus |
|-----|-------------|--------|
| **Töökoda 01 – Üks agent** | Ehita **"Selgita nagu juhile" agent**, testi seda kohalikult ja juuruta Foundrys | ✅ Saadaval |
| **Töökoda 02 – Mitme agendi töövoog** | Ehita **"CV → töö sobivuse hindaja"** – 4 agenti töötavad koos CV hindamiseks ja õpitee loomiseks | ✅ Saadaval |

---

## Tutvu Juhitagajaga

Selles töötubas ehitad **"Selgita nagu juhile" agendi** – tehisintellekti agendi, kes võtab keerulise tehnilise žargooni ja tõlgendab selle rahulikeks, juhtruumiks sobivateks kokkuvõteteks. Ausalt öeldes, keegi juhtkonnas ei taha kuulda „niidipooli ammendumist sünkroonsete kõnede tõttu versioonis 3.2.”

Ehitasin selle agendi pärast liiga palju juhtumeid, kus minu hoolikalt koostatud tagasivaade sai vastuseks: *„Niisiis... kas veebisait on maas või mitte?”*

### Kuidas see töötab

Sa annad sellele tehnilise uuenduse. See annab sulle juhiraportina kolm peamist punkti, ilma žargoonita, ilma virnasoovituseta, ilma eksistentsiaalset hirmu. Lihtsalt **mis juhtus**, **äriline mõju** ja **järgmine samm**.

### Vaata seda töös

**Sa ütled:**
> „API latentsus suurenes niidipooli ammendumise tõttu, mille põhjustasid versioonis 3.2 sisse viidud sünkroonsed kõned.”

**Agent vastab:**

> **Juhtkonna kokkuvõte:**
> - **Mis juhtus:** Pärast viimast värskendust aeglustus süsteem.
> - **Äriline mõju:** Mõned kasutajad kogesid teenuse kasutamisel viivitusi.
> - **Järgmine samm:** Muudatus tühistati ja parandust valmistatakse ette enne uuesti juurutamist.

### Miks just see agent?

See on väga lihtne, ühe eesmärgiga agent – ideaalne selleks, et õppida hostitud agendi töövoogu algusest lõpuni, ilma keeruliste tööriistade kinni jäämiseta. Ja ausalt? Iga insenerimeeskond võiks sellist kasutada.

---

## Töötuba struktuur

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

> **Märkus:** Iga töökoha kaust `agent/` on see, mida **Microsoft Foundry laiendus** genereerib, kui käivitad käsuviibast `Microsoft Foundry: Create a New Hosted Agent`. Failid kohandatakse seejärel sinu agendi juhiste, tööriistade ja seadistustega. Töökoda 01 viib sind samm-sammult läbi ehk alustad nullist loomisest.

---

## Alustamine

### 1. Klooni hoidla

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Loo Python virtuaalne keskkond

```bash
python -m venv venv
```

Aktiveeri see:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Paigalda sõltuvused

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Konfigureeri keskkonnamuutujad

Kopeeri näidisfail `.env` agendi kaustast ja täida õiged väärtused:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Muuda `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Järgi töötuba juhiseid

Iga tuba on iseseisev oma moodulitega. Alusta **Töökoda 01**'st, et õppida põhialused, siis liigu edasi **Töökoda 02** juurde mitme agendi töövoogude jaoks.

#### Töökoda 01 – Üks agent ([täielikud juhised](workshop/lab01-single-agent/README.md))

| # | Moodul | Link |
|---|--------|------|
| 1 | Eeltingimuste lugemine | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Paigalda Foundry Toolkit & Foundry laiendus | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Loo Foundry projekt | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Loo hostitud agent | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Konfigureeri juhised & keskkond | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Testi lokaalselt | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Juuraota Foundrys | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Kontrolli mänguväljakul | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Veaotsing | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Töökoda 02 – Mitme agendi töövoog ([täielikud juhised](workshop/lab02-multi-agent/README.md))

| # | Moodul | Link |
|---|--------|------|
| 1 | Eeltingimused (Töökoda 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Mõista mitme agendi arhitektuuri | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Loo mitme agendi projektiraamistik | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Konfigureeri agendid & keskkond | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Orkestreerimise mustrid | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testi lokaalselt (mitme agendi) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Juuraota Foundrys | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Kontrolli mänguväljakul | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Veaotsing (mitme agendi) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Hooldaja

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

## Nõutavad õigused (kiirülevaade)

| Stsenaarium | Nõutavad rollid |
|----------|---------------|
| Uue Foundry projekti loomine | **Azure AI Owner** Foundry ressursil |
| Juuruta olemasolevasse projekti (uued ressursid) | **Azure AI Owner** + **Contributor** tellimuses |
| Juuruta täielikult konfigureeritud projekti | Konto **Reader** + projekti **Azure AI User** |

> **Tähtis:** Azure `Owner` ja `Contributor` rollid sisaldavad ainult *haldusõiguseid*, mitte *arendusõiguseid* (andmete toiminguid). Agentide ehitamiseks ja juurutamiseks vajad **Azure AI User** või **Azure AI Owner** õigust.

---

## Viited

- [Kiirkäivitus: juurutage oma esimene majutatud agent (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Mis on majutatud agendid?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Looge majutatud agendi töövood VS Code'is](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Juurutage majutatud agent](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Arhitektuuri ülevaate agendi näide](https://github.com/Azure-Samples/agent-architecture-review-sample) - Reaalne majutatud agent MCP tööriistade, Excalidraw diagrammide ja kahekordse juurutusega

---


## Litsents

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->