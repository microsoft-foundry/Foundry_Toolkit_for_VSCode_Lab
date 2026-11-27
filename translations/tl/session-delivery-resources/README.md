# Paano ihatid ang sesyon na ito

Salamat sa paghatid ng sesyon na ito!

Bago ihatid ang workshop, pakiusap:

1. Basahin ang dokumentong ito at lahat ng kasama nitong mga sanggunian nang buo.
2. Panoorin ang recording ng paghatid ng sesyon at ang walkthrough ng workshop mula simula hanggang katapusan.
3. Isagawa ang parehong hands-on lab mula simula hanggang katapusan sa iyong sariling makina **minsan lang** bago ang event.
4. I-validate ang iyong Microsoft Foundry project, deployments ng modelo, at mga quota.
5. Makipag-ugnayan sa tagapangalaga kung may hindi malinaw.

---

## Buod ng mga file

| Resource                      | Link                                                                             | Paglalarawan                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop slide deck           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Mga slide ng presentasyon para sa workshop na ito na may mga tala ng tagapagsalita at naka-embed na demo na mga video        |
| Session delivery recording    | _Ibibigay ng tagapangalaga_                                               | Recording ng panimula ng workshop at walkthrough ng slide                                              |
| Workshop end-to-end recording | _Ibibigay ng tagapangalaga_                                               | End-to-end recording ng parehong labs mula sa perspektibo ng isang learner                              |
| Workshop documentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repository ng pinagmulan, mga lab README, mga hakbang-hakbang na modules                                       |
| Lab 01 - single agent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Hands-on lab: bumuo, subukan, at i-deploy ang *Explain Like I'm an Executive* na hosted agent     |
| Lab 02 - multi-agent workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Hands-on lab: bumuo ng 4-agent *Resume to Job Fit Evaluator* workflow                     |
| Demo 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Demo ng Lab 01: isalin ang teknikal na jargon sa isang executive summary                          |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demo ng Lab 02: 4-agent workflow na nagtuturing ng resume-job fit at bumubuo ng mga rekomendasyon     |

> **Tandaan para sa mga tagapagsanay:** Idadagdag ang slide deck at mga link ng video pagkalabas ng mga recording. Hanggang doon, kontakin ang tagapangalaga (tingnan ang [Contacts](#contacts)) para sa pinakabagong mga asset.

---

## Magsimula

Tinuturuan ng workshop na ito ang mga developer kung paano bumuo, subukan, at i-deploy ang mga AI agent sa **Microsoft Foundry Agent Service** bilang **Hosted Agents** nang buong-buo mula sa VS Code, gamit ang extension na **Microsoft Foundry Toolkit**.

Nahahati ang workshop sa maraming bahagi kabilang ang mga slide, **2 live demo**, at **2 hands-on lab**.

### Oras

#### Buong paghatid (mga 2 oras)

| Oras           | Paglalarawan                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Panimula: hosted agents, Foundry Agent Service, at ang toolkit         |
| 10:00 - 20:00   | Demo: Executive Agent mula simula hanggang katapusan                                     |
| 20:00 - 60:00   | Lab 01 - single agent (buuin, subukan lokal, i-deploy, playground)     |
| 60:00 - 110:00  | Lab 02 - multi-agent workflow (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00 | Pagsasara, Q&A, at mga resource para sa patuloy na pag-aaral                       |

#### Maikling paghatid (mga 75 minuto)

| Oras           | Paglalarawan                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Panimula at overview                                           |
| 10:00 - 20:00 | Demo: Executive Agent                                        |
| 20:00 - 70:00 | Lab 01 lamang (ituro ang mga dumalo sa Lab 02 bilang self-paced)        |
| 70:00 - 75:00 | Pagsasara at Q&A                                              |

### Paghahanda

| Resource                       | Link                                                                                          | Paglalarawan                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Dokumentasyon ng workshop         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Dokumentasyon ng workshop at pinagmulan                 |
| Mga tagubilin para sa Lab 01            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Hands-on lab: single hosted agent                 |
| Mga tagubilin para sa Lab 02            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Hands-on lab: multi-agent workflow                |
| Checklist ng mga kinakailangan        | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Mga tools, account, at access sa Azure na kinakailangan        |
| Hosted agents quickstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Opisyal na quickstart para sa pag-deploy ng hosted agent gamit ang `azd` |
| Hosted agents region availability | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Mga suportadong rehiyon para sa hosted agents (preview)     |

### Mga kinakailangan para sa tagapagsanay

Bago ka maghatid, siguraduhing mayroon kang:

- Isang **Azure subscription** na may pahintulot na gumawa ng mga resource (Owner o Contributor sa isang resource group).
- Access sa isang **Microsoft Foundry project** sa [rehiyon na sumusuporta sa hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota para sa **gpt-4.1** (o **gpt-4.1-mini**) sa iyong Foundry project.
- Ang mga sumusunod na tools ay naka-install:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opsyonal)
  - Python 3.12 o mas bago

Patakbuhin ang [Hosted agents quickstart gamit ang `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) kahit isang beses bago ang paghatid upang magkaroon ka ng kilalang-good Foundry project, deployment ng modelo, at Azure Container Registry bilang sanggunian kung magkakaproblema ang isang learner.

---

## Walkthrough ng slide

Sinusundan ng deck ang parehong daloy ng mga lab. Mga mungkahing puntos na pag-usapan para sa bawat seksyon:

| Seksyon                     | Pangunahing mensahe                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Pamagat at agenda            | I-frame ang workshop bilang *VS Code to Foundry* na walang kailangang pagbabago ng portal.                                |
| Bakit hosted agents?          | Managed runtime, deployment gamit ang ACR, OpenAI-compatible `/responses` API, naka-scope sa Foundry projects.        |
| Diagram ng arkitektura        | I-walkthrough ang [README architecture](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.   |
| Anatomy ng isang hosted agent   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - ano ang ginagawa ng bawat file.                              |
| Live demo: Executive Agent  | Lumipat sa VS Code at patakbuhin ang [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo mula simula hanggang katapusan (tingnan ang [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Lumipat sa VS Code at patakbuhin ang [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo (tingnan ang [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Maikling paliwanag sa Lab 01                | Ibigay sa mga learner. Ituro ang [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Mga pattern ng multi-agent        | Sequential vs concurrent vs handoff - preview bago magsimula ang Lab 02.                                           |
| Maikling paliwanag sa Lab 02                | Ibigay sa mga learner. Ituro ang [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Pagsasara at mga resource       | Mga link para sa patuloy na pag-aaral mula sa seksyon ng [Additional resources](#additional-resources).                      |

---

## Mga Demos

May dalawang live na demo na kasama sa paghatid. Maglaan ng 10 minuto sa bawat isa.

| Demo | Lab | Mga File | Ano ang ipapakita |
|------|-----|-------|--------------|
| Executive Agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Isang hosted agent lamang; isalin ang teknikal na jargon sa isang executive summary |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orchestration; bigyang puntos ang resume-job fit at bumuo ng rekomendasyon |

### Demo 1: Executive Agent

Isang standalone agent sa [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Gamitin ito bilang 10-minutong demo bago ang Lab 01.

1. Buksan ang [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) at lakbayin ang agent definition (system prompt, modelo, framework).
2. Pindutin ang `F5` upang ilunsad ang **Agent Inspector** lokal.
3. I-paste ang sample prompt mula sa [README](../README.md#see-it-in-action) at ipakita ang tugon ng executive-summary.
4. Ipakita ang [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) at [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) upang ipaliwanag ang mga deployment artefact.
5. Ipakita ang daloy ng deployment (Docker build, ACR push, hosted agent create) nang hindi naghihintay ng pagkumpleto.

### Demo 2: Resume to Job Fit Evaluator

Isang 4-agent workflow sa [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Gamitin ito bilang 10-minutong demo bago ang Lab 02.

1. Buksan ang [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) at ipakita kung paano pinagsama-sama ang apat na agent sa isang sequential orchestration.
2. Pindutin ang `F5` upang ilunsad ang **Agent Inspector** para sa multi-agent workflow.
3. I-paste ang maikling paglalarawan ng trabaho at sample na resume sa Inspector chat.
4. Lakbayin ang pipeline ng apat na agent: resume parser, job requirement extractor, fit scorer, at recommendation writer.
5. Ituro kung paano ang output ng bawat sub-agent ay nagiging context ng susunod na agent, na binibigyang-diin ang handoff pattern.
6. Ipakita ang [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) upang ihambing sa katumbas na single-agent mula Demo 1.

---

## Mga tip sa paghatid

- **Itakda ang mga inaasahan nang maaga.** Ang hosted agents ay preview pa lamang - ipaalam agad ang limitasyon ng rehiyon at quota upang hindi magulat ang mga dumalo sa gitna ng lab.
- **Patakbuhin muna ang prerequisites na gawain.** Ang parehong mga lab ay may kasamang `Validate prerequisites` VS Code na gawain - ipagawa ito sa mga dumalo bago sumulat ng anumang code.
- **Panatilihing nakikita ang Agent Inspector.** Karamihan sa mga "aha" na sandali ay nangyayari kapag nakita ng mga learner ang local `/responses` round-trip na nag-iilaw.
- **Maghanda ng backup na proyekto.** Kapag nagka-quota wall ang Foundry project ng learner, magbahagi ng pre-provisioned na proyekto para sa deployment na hakbang sa halip na hadlangan ang buong silid.
- **Ipagsanib ang mga dumalo.** Mas madali ang Lab 02 (multi-agent) kapag ang mga learner ay pweding mag-usap tungkol sa orchestration kasama ng isa.
- **Gamitin ang mga doks module bilang mga checkpoint.** Ang bawat folder na `docs/` ng lab ay hinati sa mga numbered na module - gamitin ito bilang natural na mga punto para magpahinga.
- **I-pre-pull ang base Docker image** sa mga shared lab machine upang maiwasan ang mga limitasyon sa registry.

---

## Pagsasaayos ng mga problema habang naghahatid

| Sintomas                                      | Unang subukang hakbang                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Hindi makakonekta ang Agent Inspector               | Siguraduhing libre ang port `8088` at tumatakbo ang `Run Agent HTTP Server` task.               |
| Pasimulang tagasuri ay hindi makakadikit                     | Suriin na libre ang port `5679`; i-restart ang VS Code kung ang `debugpy` ay naka-bind na.                           |
| `azd up` nabibigo dahil sa auth error               | Patakbuhin ang `az login` at `azd auth login`, siguraduhing tamang tenant ang napili.                              |
| Nagka-hang ang deployment sa ACR push                 | Siguraduhing tumatakbo ang Docker Desktop at ang user ay may `AcrPush` sa registry.                              |
| Nagbibigay ang modelo ng 404 / deployment-not-found     | Ang pangalan ng deployment ng modelo sa `agent.yaml` ay dapat tumugma sa deployment sa Foundry project.              |
| Naka-stuck ang hosted agent sa `Provisioning`         | Siguraduhin na suportado ng rehiyon ng proyekto ang [hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) at may available na quota. |
| Nagbibigay ang Playground ng 401                       | Muling mag-authenticate ng Foundry extension mula sa VS Code activity bar.                                     |

Para sa mas malalim na gabay, bawat lab ay may sariling dokumento ng `08-troubleshooting.md` - ituro ang mga learner doon:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Pagsasaayos ng sesyon na ito

Malugod kang malayang ayusin ang workshop para sa iyong mga tagapakinig. Mga karaniwang pagbabago:

- **Para sa mga backend na tagapakinig:** mas maglaan ng oras sa `agent.yaml`, Docker, at ACR; paikliin ang demo ng playground.
- **Para sa mga citizen-developer na tagapakinig:** manatili sa UI ng Foundry extension para sa scaffolding; bawasan ang mga hakbang sa CLI.
- **Single-track 60-minutong slot:** ihatid lamang ang panimula, demo, at Lab 01.
- **Para sa Workshop lamang (walang slides) format:** buksan ang parehong lab READMEs at gamitin ito bilang pangunahing script.

Kung palawigin mo ang mga labs, paki-ambag ang mga pagbabago pabalik sa pamamagitan ng PR upang makinabang ang ibang mga tagapagsanay.

---

## Karagdagang mga mapagkukunan

- [Dokumentasyon ng Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Pangkalahatang-ideya ng mga hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Quickstart: i-deploy ang iyong unang hosted agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Pag-deploy ng hosted agent (paano gagawin)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry Toolkit para sa VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Mga Contact

Kung may mga katanungan ka tungkol sa paghatid ng session na ito, mangyaring magbukas ng isyu sa [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) at i-tag ang tagapangasiwa.

| Papel                | Pangalan           | GitHub                                                  |
|---------------------|--------------------|---------------------------------------------------------|
| Tagapangasiwa / contact| Shivam Goyal    | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->