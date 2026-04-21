# Foundry Toolkit + Foundry Hosted Agents -työpaja

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

Rakenna, testaa ja ota käyttöön tekoälyagentteja **Microsoft Foundry Agent Service** -palveluun **Hosted Agents** -muodossa - kokonaan VS Codesta käyttäen **Microsoft Foundry -laajennusta** ja **Foundry Toolkitia**.

> **Hosted Agents ovat tällä hetkellä esikatseluvaiheessa.** Tuetut alueet ovat rajalliset – katso [alueiden saatavuus](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Jokaisen työpajan `agent/`-kansio on **Foundry-laajennuksen automaattisesti luoma** - muokkaat sitten koodia, testaat paikallisesti ja otat käyttöön.

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](./README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Haluatko mieluummin kloonata paikallisesti?**
>
> Tämä repositorio sisältää yli 50 käännöstä, mikä lisää merkittävästi latausmäärää. Jos haluat kloonata ilman kielitiedostoja, käytä sparse-checkoutia:
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
> Saat kaikki tarpeelliset tiedostot kurssin suorittamiseen paljon nopeammalla latauksella.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arkkitehtuuri

```mermaid
flowchart TB
    subgraph Local["Paikallinen kehitys (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Laajennus"]
        FoundryToolkit["Foundry Työkalupakki
        Laajennus"]
        Scaffold["Rakennettu Agenttikoodi
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agentin tarkastaja
        (Paikallinen testaus)"]
        FE -- "Luo uusi
        Isännöity agentti" --> Scaffold
        Scaffold -- "F5 Virheenkorjaus" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Scr Container
        Rekisteri"]
        AgentService["Foundry Agenttipalvelu
        (Isännöity agentin suoritusaika)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Leikkikenttä
        & VS Code Leikkikenttä"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Ota käyttöön
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Testaa kehotteita" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**Virtaus:** Foundry-laajennus luo agentin rungon → muokkaat koodia ja ohjeita → testaat paikallisesti Agent Inspectorilla → otat käyttöön Foundryyn (Docker-kuva pusketaan ACR:ään) → tarkistat Playgroundissa.

---

## Mitä rakennat

| Työpaja | Kuvaus | Tila |
|-----|-------------|--------|
| **Työpaja 01 - Yksittäinen agentti** | Rakenna **"Explain Like I'm an Executive" -agentti**, testaa paikallisesti ja ota käyttöön Foundryssa | ✅ Saatavilla |
| **Työpaja 02 - Moniagenttityönkulku** | Rakenna **"Resume → Job Fit Evaluator"** - 4 agenttia työskentelee yhdessä arvioiden CV:n sopivuutta ja luoden oppimissuunnitelman | ✅ Saatavilla |

---

## Tutustu Executive-agenttiin

Tässä työpajassa rakennat **"Explain Like I'm an Executive" -agentin** – tekoälyagentin, joka ottaa monimutkaisen teknisen kielen ja muuntaa sen rauhallisiksi, hallitustason yhteenvetoiksi. Rehellisesti sanottuna, C-tason johdossa kukaan ei halua kuulla "v1.3:n synkronisten kutsujen aiheuttamasta säikeiden paljun loppumisesta".

Rakensin tämän agentin yhden liian monta kertaa sattuneen tilanteen jälkeen, jossa huolellisesti kirjoitettu jälkiarvio sai vastaukseksi: *"Eli... onko verkkosivu alhaalla vai ei?"*

### Miten se toimii

Syötät teknisen päivityksen. Se palauttaa johtoryhmälle tarkoitetun yhteenvedon – kolme pääkohtaa, ei ammattislangia, ei pinon jäljitysjälkiä, ei eksistentiaalista ahdistusta. Vain **mitä tapahtui**, **liiketoiminnan vaikutus** ja **seuraava askel**.

### Näe miten se toimii

**Sanot:**
> "API-viive kasvoi säikeiden paljun loppumisen vuoksi, joka johtui v3.2:een lisätyistä synkronisista kutsuista."

**Agentti vastaa:**

> **Johtoryhmän yhteenveto:**
> - **Mitä tapahtui:** Viimeisimmän julkaisun jälkeen järjestelmä hidastui.
> - **Liiketoiminnan vaikutus:** Jotkut käyttäjät kokivat viiveitä palvelun käytössä.
> - **Seuraava askel:** Muutos peruttiin ja korjaus on valmisteilla ennen uudelleen käyttöönottoa.

### Miksi tämä agentti?

Se on yksinkertainen, yhteen tarkoitukseen rakennettu agentti – täydellinen tapa oppia hosted agent -työnkulku kokonaisuudessaan ilman monimutkaisia työkaluketjuja. Rehellisesti? Jokainen insinööriryhmä voisi hyötyä tällaisesta.

---

## Työpajan rakenne

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

> **Huom:** Jokaisen työpajan `agent/` -kansio on se, jonka **Microsoft Foundry -laajennus** luo, kun suoritat komentopalettista komennon `Microsoft Foundry: Create a New Hosted Agent`. Tiedostot muokataan sen jälkeen agenttisi ohjeilla, työkaluilla ja määrityksillä. Työpaja 01 vie sinut läpi tämän prosessin alusta asti.

---

## Aloittaminen

### 1. Kloonaa varasto

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Luo Python-virtuaaliympäristö

```bash
python -m venv venv
```

Aktivoi se:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Asenna riippuvuudet

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Määritä ympäristömuuttujat

Kopioi agentin kansion sisällä oleva esimerkkitiedosto `.env` ja täytä omat arvosi:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Muokkaa tiedostoa `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Seuraa työpajan harjoituksia

Jokainen työpaja on itsenäinen omine moduuleineen. Aloita **työpajasta 01** oppiaksesi perusteet, siirry sitten **työpajaan 02** oppiaksesi moniagenttityönkulkuja.

#### Työpaja 01 - Yksittäinen agentti ([täydelliset ohjeet](workshop/lab01-single-agent/README.md))

| # | Moduuli | Linkki |
|---|--------|------|
| 1 | Lue ennakkoedellytykset | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Asenna Foundry Toolkit & Foundry-laajennus | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Luo Foundry-projekti | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | Luo hosted agent | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | Määritä ohjeet & ympäristö | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | Testaa paikallisesti | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Ota käyttöön Foundryssa | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Tarkista playgroundissa | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | Vianmääritys | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Työpaja 02 - Moniagenttityönkulku ([täydelliset ohjeet](workshop/lab02-multi-agent/README.md))

| # | Moduuli | Linkki |
|---|--------|------|
| 1 | Ennakkoedellytykset (Työpaja 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Ymmärrä moniagenttien arkkitehtuuri | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Luo moniagenttiprojekti | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Määritä agentit & ympäristö | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Orkestrointimallit | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Testaa paikallisesti (moniagentti) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Julkaise Foundryyn | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Vahvista leikkikentässä | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Vianetsintä (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Ylläpitäjä

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

## Vaaditut oikeudet (nopea viite)

| Tilanne | Vaaditut roolit |
|----------|---------------|
| Luo uusi Foundry-projekti | **Azure AI Owner** Foundryn resurssissa |
| Julkaise olemassa olevaan projektiin (uudet resurssit) | **Azure AI Owner** + **Contributor** tilauksessa |
| Julkaise täysin konfiguroituun projektiin | **Reader** tilillä + **Azure AI User** projektissa |

> **Tärkeää:** Azure `Owner`- ja `Contributor`-roolit sisältävät vain *hallintaoikeudet*, eivät *kehitysoikeuksia* (data-toimintoja). Tarvitset **Azure AI User**- tai **Azure AI Owner** -oikeudet agenttien rakentamiseen ja julkaisuun.

---

## Viitteet

- [Pikaopas: Julkaise ensimmäinen isännöity agentti (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Mitkä ovat isännöidyt agentit?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Luo isännöityjen agenttien työnkulkuja VS Codessa](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Julkaise isännöity agentti](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC Microsoft Foundrylle](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Arkkitehtuurin tarkistusagentin esimerkki](https://github.com/Azure-Samples/agent-architecture-review-sample) - Käytännön isännöity agentti MCP-työkaluilla, Excalidraw-kaavioilla ja kaksinkertaisella julkaisulla

---


## Lisenssi

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty tekoälykäännöspalvelu [Co-op Translator](https://github.com/Azure/co-op-translator) avulla. Vaikka pyrimme tarkkuuteen, huomioithan, että automaattikäännöksissä saattaa esiintyä virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäisellä kielellä tulisi pitää auktoritatiivisena lähteenä. Tärkeiden tietojen osalta suositellaan ammattilaisten tekemää käännöstä. Emme ole vastuussa tästä käännöksestä johtuvista väärinymmärryksistä tai virhetulkinnasta.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->