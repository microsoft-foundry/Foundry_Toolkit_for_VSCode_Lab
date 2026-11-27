# How to deliver dis session

Thanks for to deliver dis session!

Before you deliver di workshop, abeg:

1. Read dis document and all di resources inside am well well.
2. Watch di session delivery recording and di workshop end-to-end walkthrough.
3. Try walk through both hands-on labs end-to-end for your own machine **at least one time** before di event.
4. Check your Microsoft Foundry project, model deployments, and quotas.
5. If anything no clear, abeg hala di maintainer.

---

## File summary

| Resource                      | Link                                                                             | Description                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop slide deck           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Presentation slides for dis workshop with presenter notes and embedded demo videos        |
| Session delivery recording    | _To be provided by di maintainer_                                               | Workshop intro and slide walkthrough recording                                              |
| Workshop end-to-end recording | _To be provided by di maintainer_                                               | End-to-end recording of both labs from di learner perspective                              |
| Workshop documentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Source repository, lab READMEs, step-by-step modules                                       |
| Lab 01 - single agent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Hands-on lab: build, test, and deploy di *Explain Like I'm an Executive* hosted agent     |
| Lab 02 - multi-agent workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Hands-on lab: build di 4-agent *Resume to Job Fit Evaluator* workflow                     |
| Demo 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Lab 01 demo: translate technical jargon into executive summary                          |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Lab 02 demo: 4-agent workflow wey scores resume-job fit and generate recommendations     |

> **Note for trainers:** Slide deck and video links go add after di recordings publish. Till then, abeg ping di maintainer (see [Contacts](#contacts)) for di latest assets.

---

## Get started

Dis workshop dey teach developers how dem go build, test, and deploy AI agents to **Microsoft Foundry Agent Service** as **Hosted Agents** direct from VS Code, using di **Microsoft Foundry Toolkit** extension.

Di workshop divide into many sections including slides, **2 live demos**, and **2 hands-on labs**.

### Timing

#### Full delivery (about 2 hours)

| Time            | Description                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Intro: hosted agents, Foundry Agent Service, and di toolkit         |
| 10:00 - 20:00   | Demo: Executive Agent end-to-end                                     |
| 20:00 - 60:00   | Lab 01 - single agent (build, test locally, deploy, playground)     |
| 60:00 - 110:00  | Lab 02 - multi-agent workflow (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00 | Wrap-up, Q&A, and continued-learning resources                       |

#### Short delivery (about 75 minutes)

| Time          | Description                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Intro and overview                                           |
| 10:00 - 20:00 | Demo: Executive Agent                                        |
| 20:00 - 70:00 | Lab 01 only (show people di way to Lab 02 for self-paced)    |
| 70:00 - 75:00 | Wrap-up and Q&A                                              |

### Preparation

| Resource                       | Link                                                                                          | Description                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Workshop documentation         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Workshop documentation and source                 |
| Lab 01 instructions            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Hands-on lab: single hosted agent                 |
| Lab 02 instructions            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Hands-on lab: multi-agent workflow                |
| Prerequisites checklist        | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Tools, accounts, and Azure access required        |
| Hosted agents quickstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Official quickstart for deploying a hosted agent with `azd` |
| Hosted agents region availability | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Supported regions for hosted agents (preview)     |

### Trainer prerequisites

Before you deliver, make sure say you get:

- An **Azure subscription** with permission to create resources (Owner or Contributor on a resource group).
- Access to a **Microsoft Foundry project** for [region wey support hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota for **gpt-4.1** (or **gpt-4.1-mini**) for your Foundry project.
- Di following tools don install for your system:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Optional)
  - Python 3.12 or later

Run di [Hosted agents quickstart with `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) at least one time before delivery make you get correct Foundry project, model deployment, and Azure Container Registry to use if learner jam.

---

## Slide walkthrough

Di deck follow di same waka as di labs. Suggested talking points for each section be:

| Section                     | Key message                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Title and agenda            | Frame di workshop as *VS Code to Foundry* with no need for portal switching.                                |
| Why hosted agents?          | Managed runtime, ACR-based deployment, OpenAI-compatible `/responses` API, scoped to Foundry projects.        |
| Architecture diagram        | Walk through di [README architecture](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.   |
| Anatomy of a hosted agent   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - wetin each file dey do.                             |
| Live demo: Executive Agent  | Change go VS Code and run di [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo end-to-end (see [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Change go VS Code and run di [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo (see [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 brief                | Hand over to learners. Show dem [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Multi-agent patterns        | Sequential vs concurrent vs handoff - preview before Lab 02 start.                                           |
| Lab 02 brief                | Hand over to learners. Show dem [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Wrap-up and resources       | Continued-learning links from di [Additional resources](#additional-resources) section.                      |

---

## Demos

Two live demos dey inside di delivery. Assign 10 minutes for each.

| Demo | Lab | Files | Wetin show |
|------|-----|-------|--------------|
| Executive Agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Single hosted agent; translate technical words into executive summary |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orchestration; score resume-job fit and generate recommendation |

### Demo 1: Executive Agent

Standalone agent for [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Use am as 10-minute demo before Lab 01.

1. Open [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) and waka through the agent definition (system prompt, model, framework).
2. Press `F5` to start di **Agent Inspector** locally.
3. Paste di sample prompt from di [README](../README.md#see-it-in-action) and show the executive-summary response.
4. Show [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) and [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) to explain di deployment artefacts.
5. Show di deployment waka (Docker build, ACR push, hosted agent create) without wait to finish.

### Demo 2: Resume to Job Fit Evaluator

4-agent workflow for [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Use am as 10-minute demo before Lab 02.

1. Open [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) and show how di four agents dem join together in sequential orchestration.
2. Press `F5` to start di **Agent Inspector** for di multi-agent workflow.
3. Paste short job description and sample resume for di Inspector chat.
4. Walk through di four-agent pipeline: resume parser, job requirement extractor, fit scorer, and recommendation writer.
5. Show how each sub-agent output become the next agent context, show di handoff pattern.
6. Show [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) to compare with di single-agent wey come from Demo 1.

---

## Delivery tips

- **Set expectations early.** Hosted agents dey preview - talk about region limits and quota upfront so people no go surprise for middle of lab.
- **Run prerequisites task first.** Both labs get `Validate prerequisites` VS Code task - make sure people run am before dem write any code.
- **Keep di Agent Inspector visible.** Most "aha" moments dey happen when learners dey see local `/responses` round-trip light up.
- **Get backup project.** If learner Foundry project jam quota wahala, share pre-provisioned project for deployment step instead make room jam.
- **Pair attendees.** Lab 02 (multi-agent) dey easier if learners fit discuss orchestration with partner.
- **Use di docs modules as checkpoints.** Each lab's `docs/` folder split into numbered modules - use dem as natural pause points.
- **Pre-pull base Docker image** on shared lab machines to avoid registry rate limits.

---

## Troubleshooting during delivery

| Symptom                                      | First thing to try                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector no fit connect               | Confirm say port `8088` free and `Run Agent HTTP Server` task dey run.               |
| Debugger no fit attach                        | Check say port `5679` free; restart VS Code if `debugpy` don bind already.                           |
| `azd up` fail with auth error               | Run `az login` and `azd auth login`, make sure correct tenant select.                              |
| Deployment hang for ACR push                 | Check Docker Desktop dey run and user get `AcrPush` for di registry.                              |
| Model dey return 404 / deployment-not-found     | Di model deployment name for `agent.yaml` must match di deployment for Foundry project.              |
| Hosted agent jam for `Provisioning`         | Confirm project region [support hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) and quota dey available. |
| Playground dey return 401                      | Re-authenticate Foundry extension from VS Code activity bar.                                     |

For deeper help, every lab get im own `08-troubleshooting.md` doc - direct learners go there:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Customizing dis session

You fit adapt di workshop for your audience. Common variations be:

- **Backend audiences:** spend more time for `agent.yaml`, Docker, and ACR; cut di playground demo.
- **Citizen-developer audiences:** stay for Foundry extension UI for scaffolding; reduce CLI steps.
- **Single-track 60-minute slot:** deliver intro, demo, and Lab 01 only.
- **Workshop-only (no slides) format:** opɛn bot lab READMEs dem an use dem as di main skript.

If you add more tins for di labs, abeg make you send di changes back through PR so oda trainers go benefit.

---

## Adidionɔl risɔs

- [Microsoft Foundry dokumenteshɔn](https://learn.microsoft.com/azure/ai-foundry/)
- [Hosted agents ovavyu](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Quickstart: deploy your first hosted agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Deploy a hosted agent (how-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contacts

If you get question about how to deliver dis session, abeg open issue for di [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) an tag di person wey dey maintain am.

| Role                | Name           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Maintainer / contact| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->