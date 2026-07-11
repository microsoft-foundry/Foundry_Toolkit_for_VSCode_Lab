# Paano ihatid ang sesyon na ito

Salamat sa paghahatid ng sesyon na ito!

Bago ihatid ang workshop, pakiusap:

1. Basahin nang buo ang dokumentong ito at lahat ng kalakip nitong mga resources.
2. Panoorin ang recording ng paghahatid ng sesyon at ang workshop end-to-end walkthrough.
3. Isagawa ang parehong hands-on labs nang buo sa iyong sariling makina **kahit isang beses** bago ang event.
4. I-validate ang iyong Microsoft Foundry project, mga deployment ng modelo, at quota.
5. Makipag-ugnayan sa maintainer kung may mga hindi malinaw.

---

## Buod ng mga file

| Resource                      | Link                                                                             | Deskripsyon                                                                                 |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop slide deck           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Mga presentasyon na slide para sa workshop na ito kasama ang mga tala ng presenter at naka-embed na mga demo video    |
| Session delivery recording    | _Ibibigay ng maintainer_                                                          | Intro ng workshop at recording ng walkthrough ng mga slide                                  |
| Workshop end-to-end recording | _Ibibigay ng maintainer_                                                          | End-to-end recording ng parehong labs mula sa perspektibo ng isang learner                   |
| Workshop documentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Source repository, mga lab README, mga hakbang-hakbang na modules                          |
| Lab 01 - single agent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Hands-on lab: gumawa, subukan, at i-deploy ang *Explain Like I'm an Executive* hosted agent  |
| Lab 02 - multi-agent workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Hands-on lab: bumuo ng 4-agent *Resume to Job Fit Evaluator* workflow                       |
| Demo 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Demo ng Lab 01: isalin ang teknikal na jargon sa executive summary                          |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demo ng Lab 02: 4-agent workflow na nagsusuri ng resume-job fit at bumubuo ng mga rekomendasyon |

> **Note para sa mga tagapagsanay:** Idadagdag ang mga slide deck at link sa video kapag nailathala na ang mga recording. Hanggang noon, kontakin ang maintainer (tingnan ang [Contacts](#mga-kontak)) para sa pinakabagong mga assets.

---

## Magsimula

Itinuturo ng workshop na ito sa mga developer kung paano bumuo, mag-test, at mag-deploy ng mga AI agent sa **Microsoft Foundry Agent Service** bilang **Hosted Agents** nang buong buo mula sa VS Code gamit ang **Microsoft Foundry Toolkit** extension.

Nahahati ang workshop sa ilang mga bahagi kabilang ang mga slide, **2 live demo**, at **2 hands-on labs**.

### Oras

#### Buong paghahatid (mga 2 oras)

| Oras           | Deskripsyon                                                         |
|-----------------|--------------------------------------------------------------------|
| 0:00 - 10:00    | Introduksyon: hosted agents, Foundry Agent Service, at toolkit     |
| 10:00 - 20:00   | Demo: Executive Agent mula simula hanggang dulo                    |
| 20:00 - 60:00   | Lab 01 - single agent (bumuo, test locally, deploy, playground)   |
| 60:00 - 110:00  | Lab 02 - multi-agent workflow (Resume to Job Fit Evaluator)       |
| 110:00 - 120:00 | Pagtatapos, Q&A, at mga resources para sa patuloy na pag-aaral    |

#### Maikling paghahatid (mga 75 minuto)

| Oras          | Deskripsyon                                                |
|---------------|------------------------------------------------------------|
| 0:00 - 10:00  | Introduksyon at pangkalahatang-ideya                      |
| 10:00 - 20:00 | Demo: Executive Agent                                     |
| 20:00 - 70:00 | Lab 01 lamang (ipakita sa mga kalahok ang Lab 02 bilang self-paced) |
| 70:00 - 75:00 | Pagtatapos at Q&A                                         |

### Paghahanda

| Resource                       | Link                                                                                          | Deskripsyon                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Dokumentasyon ng workshop      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Dokumentasyon ng workshop at source                 |
| Mga tagubilin sa Lab 01        | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Hands-on lab: single hosted agent                 |
| Mga tagubilin sa Lab 02        | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Hands-on lab: multi-agent workflow                |
| Checklist ng mga kinakailangan | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Mga tools, accounts, at Azure access na kailangan   |
| Hosted agents quickstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Opisyal na quickstart para sa pag-deploy ng hosted agent gamit ang `azd` |
| Availability ng hosted agents sa rehiyon | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Mga suportadong rehiyon para sa hosted agents (preview)     |

### Mga kinakailangan para sa tagapagsanay

Bago maghatid, tiyakin na mayroon ka:

- Isang **Azure subscription** na may permiso na gumawa ng resources (Owner o Contributor sa isang resource group).
- Access sa **Microsoft Foundry project** sa [rehiyong sumusuporta sa hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota para sa **gpt-4.1** (o **gpt-4.1-mini**) sa iyong Foundry project.
- Ang mga sumusunod na tools na naka-install:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opsyonal)
  - Python 3.10 o mas bago

Patakbuhin ang [Hosted agents quickstart with `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) kahit isang beses bago ang paghahatid para may kilalang-mahusay kang Foundry project, deployment ng modelo, at Azure Container Registry na mababanggit kung may mahirapang learner.

---

## Walkthrough ng slide

Ang deck ay sumusunod sa parehong daloy tulad ng mga labs. Mga mungkahing punto sa pagsasalita para sa bawat seksyon:

| Seksiyon                      | Pangunahing mensahe                                                                                                |
|-----------------------------|------------------------------------------------------------------------------------------------------------------|
| Pamagat at agenda            | I-frame ang workshop bilang *VS Code to Foundry* na walang kailangang magpalipat ng portal.                      |
| Bakit hosted agents?         | Managed runtime, ACR-based deployment, OpenAI-compatible `/responses` API, naka-scope sa mga Foundry projects.   |
| Arkitekturang diagram        | I-walkthrough ang [README architecture](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.     |
| Anyo ng hosted agent         | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - ano ang ginagawa ng bawat file.                        |
| Live demo: Executive Agent   | Lumipat sa VS Code at patakbuhin ang [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo mula simula hanggang dulo (tingnan ang [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Lumipat sa VS Code at patakbuhin ang [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo (tingnan ang [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Maikling paliwanag sa Lab 01 | I-turnover sa mga learners. Ituro ang [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Mga pattern ng multi-agent   | Sequential vs concurrent vs handoff - preview bago magsimula ang Lab 02.                                         |
| Maikling paliwanag sa Lab 02 | I-turnover sa mga learners. Ituro ang [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Pagtatapos at mga resources  | Mga link para sa patuloy na pag-aaral mula sa seksyon ng [Additional resources](#karagdagang-mga-mapagkukunan).           |

---

## Mga Demo

Dalawang live demo ang kasama sa paghahatid. Maglaan ng 10 minuto para sa bawat isa.

| Demo | Lab | Mga File | Ano ang ipapakita |
|------|-----|---------|-------------------|
| Executive Agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Isang hosted agent; isalin ang teknikal na jargon sa isang executive summary |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orchestration; markahan ang resume-job fit at bumuo ng rekomendasyon |

### Demo 1: Executive Agent

Isang standalone agent sa [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Gamitin ito bilang 10-minutong demo bago ang Lab 01.

1. Buksan ang [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) at suriin ang agent definition (system prompt, model, framework).
2. Pindutin ang `F5` upang ilunsad ang **Agent Inspector** nang lokal.
3. I-paste ang sample prompt mula sa [README](../README.md#see-it-in-action) at ipakita ang tugon ng executive summary.
4. Ipakita ang [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) at [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) para ipaliwanag ang mga deployment artefacts.
5. Ipakita ang daloy ng deployment (Docker build, ACR push, hosted agent create) nang hindi naghihintay ng katapusan.

### Demo 2: Resume to Job Fit Evaluator

Isang 4-agent workflow sa [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Gamitin ito bilang 10-minutong demo bago ang Lab 02.

1. Buksan ang [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) at ipakita kung paano naka-wiring ang apat na agents sa isang sequential orchestration.
2. Pindutin ang `F5` upang ilunsad ang **Agent Inspector** para sa multi-agent workflow.
3. I-paste ang maikling job description at isang sample resume sa Inspector chat.
4. Suriin ang four-agent pipeline: resume parser, job requirement extractor, fit scorer, at recommendation writer.
5. Ituro kung paano ang output ng bawat sub-agent ay nagiging konteksto ng susunod na agent, binibigyang-diin ang handoff pattern.
6. Ipakita ang [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) para ihambing sa single-agent na katumbas mula sa Demo 1.

---

## Mga tip sa paghahatid

- **Itakda ang mga inaasahan nang maaga.** Ang hosted agents ay nasa preview - ipaalam ang mga limitasyon ng rehiyon at quota agad para hindi mabigla ang mga kalahok habang nasa gitna ng lab.
- **Patakbuhin muna ang prerequisites task.** Parehong labs ay may `Validate prerequisites` na VS Code task - ipagawa ito sa mga kalahok bago magsulat ng kahit anong code.
- **Panatilihing nakikita ang Agent Inspector.** Karamihan sa mga "aha" na sandali ay nangyayari kapag nakikita ng mga learner na umiilaw ang local `/responses` round-trip.
- **Magkaroon ng backup na proyekto.** Kung maabot ng Foundry project ng isang learner ang quota wall, ibahagi ang isang pre-provisioned na proyekto para sa deployment step kaysa hadlangan ang buong kwarto.
- **Pair-in ang mga kalahok.** Ang Lab 02 (multi-agent) ay mas madali kapag nakakapag-usap ang mga learner tungkol sa orchestration kasama ang isang partner.
- **Gamitin ang mga modules ng docs bilang mga checkpoint.** Ang bawat lab `docs/` folder ay hinati sa 8 numbered modules - gamitin ito bilang mga natural na pahinga.
- **Pre-pull ang base Docker image** sa mga shared lab machines upang maiwasan ang registry rate limits.

---

## Pag-troubleshoot habang naghahatid

| Sintomas                                     | Unang subukang gawin                                                                                   |
|----------------------------------------------|---------------------------------------------------------------------------------------------------------|
| Hindi makakonekta ang Agent Inspector         | Tiyaking libre ang port `8088` at tumatakbo ang task na `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server`. |
| Nabibigo ang debugger na mag-attach           | Suriin kung libre ang port `5679`; i-restart ang VS Code kung ang `debugpy` ay naka-bind na.              |
| Nabibigo ang `azd up` dahil sa auth error     | Patakbuhin ang `az login` at `azd auth login`, tiyaking napili ang tamang tenant.                       |
| Nakabitin ang deployment sa ACR push           | Siguraduhing tumatakbo ang Docker Desktop at may pahintulot ang user na `AcrPush` sa registry.          |
| Nagbabalik ang model ng 404 / deployment-not-found | Dapat magtugma ang pangalan ng model deployment sa `agent.yaml` sa deployment sa Foundry project.        |

| Naka-host na ahente na natigil sa `Provisioning`         | Siguraduhing sinusuportahan ng rehiyon ng proyekto ang [mga naka-host na ahente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) at may available na quota. |
| Nagbabalik ang Playground ng 401                       | Muling i-authenticate ang Foundry extension mula sa VS Code activity bar.                                     |

Para sa mas malalim na gabay, bawat lab ay may sariling `08-troubleshooting.md` na dokumento - i-link ang mga learner dito:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Pag-customize ng sesyon na ito

Malugod kang maaaring iakma ang workshop para sa iyong mga tagapakinig. Mga karaniwang pagbabago:

- **Para sa mga backend audience:** maglaan ng mas maraming oras sa `agent.yaml`, Docker, at ACR; paikliin ang demo ng playground.
- **Para sa citizen-developer audience:** manatili sa Foundry extension UI para sa scaffolding; bawasan ang mga hakbang sa CLI.
- **Isang 60-minutong single-track na slot:** ihatid ang intro, demo, at Lab 01 lamang.
- **Workshop-only (walang slides) na format:** buksan ang parehong mga README ng lab at gamitin ito bilang pangunahing script.

Kung palalawakin mo ang mga lab, mangyaring ibahagi ang mga pagbabago pabalik sa pamamagitan ng PR para makinabang ang ibang mga tagapagsanay.

---

## Karagdagang mga mapagkukunan

- [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Pangkalahatang-ideya ng mga naka-host na ahente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Quickstart: i-deploy ang iyong unang naka-host na ahente (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [I-deploy ang isang naka-host na ahente (paano gawin)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit para sa VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Mga Kontak

Kung mayroon kang mga tanong tungkol sa paghahatid ng sesyon na ito, mangyaring magbukas ng isyu sa [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) at i-tag ang tagapangalaga.

| Papel                | Pangalan           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Tagapangalaga / kontak| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->