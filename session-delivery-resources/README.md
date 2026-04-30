# How to deliver this session

Thanks for delivering this session!

Prior to delivering the workshop, please:

1. Read this document and all included resources in their entirety.
2. Watch the session delivery recording and the workshop end-to-end walkthrough.
3. Walk through both hands-on labs end-to-end on your own machine **at least once** before the event.
4. Validate your Microsoft Foundry project, model deployments, and quotas.
5. Reach out to the maintainer if anything is unclear.

---

## File summary

| Resource                      | Link                                                                             | Description                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop slide deck           | _To be provided by the maintainer_                                               | Presentation slides for this workshop with presenter notes and embedded demo videos        |
| Session delivery recording    | _To be provided by the maintainer_                                               | Workshop intro and slide walkthrough recording                                              |
| Workshop end-to-end recording | _To be provided by the maintainer_                                               | End-to-end recording of both labs from a learner's perspective                              |
| Workshop documentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Source repository, lab READMEs, step-by-step modules                                       |
| Lab 01 - single agent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Hands-on lab: build, test, and deploy the *Explain Like I'm an Executive* hosted agent     |
| Lab 02 - multi-agent workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Hands-on lab: build the 4-agent *Resume to Job Fit Evaluator* workflow                     |
| Demo 1: Executive Agent             | [ExecutiveAgent](../ExecutiveAgent/)                                                              | Lab 01 demo: translate technical jargon into an executive summary                          |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../workshop/lab02-multi-agent/PersonalCareerCopilot/)                     | Lab 02 demo: 4-agent workflow that scores resume-job fit and generates recommendations     |
| Known issues                  | [KNOWN_ISSUES.md](../KNOWN_ISSUES.md)                                            | Workarounds for known issues you may hit during delivery                                   |

> **Note for trainers:** Slide deck and video links will be added once the recordings are published. Until then, ping the maintainer (see [Contacts](#contacts)) for the latest assets.

---

## Get started

This workshop teaches developers how to build, test, and deploy AI agents to **Microsoft Foundry Agent Service** as **Hosted Agents** entirely from VS Code, using the **Microsoft Foundry Toolkit** extension.

The workshop is divided into multiple sections including slides, **2 live demos**, and **2 hands-on labs**.

### Timing

#### Full delivery (about 2 hours)

| Time            | Description                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Intro: hosted agents, Foundry Agent Service, and the toolkit         |
| 10:00 - 20:00   | Demo: Executive Agent end-to-end                                     |
| 20:00 - 60:00   | Lab 01 - single agent (build, test locally, deploy, playground)     |
| 60:00 - 110:00  | Lab 02 - multi-agent workflow (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00 | Wrap-up, Q&A, and continued-learning resources                       |

#### Short delivery (about 75 minutes)

| Time          | Description                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Intro and overview                                           |
| 10:00 - 20:00 | Demo: Executive Agent                                        |
| 20:00 - 70:00 | Lab 01 only (point attendees at Lab 02 as self-paced)        |
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
| Known issues                   | [KNOWN_ISSUES.md](../KNOWN_ISSUES.md)                                                         | Workarounds for known issues                      |

### Trainer prerequisites

Before you deliver, make sure you have:

- An **Azure subscription** with permission to create resources (Owner or Contributor on a resource group).
- Access to a **Microsoft Foundry project** in a [region that supports hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota for **gpt-4.1** (or **gpt-4.1-mini**) in your Foundry project.
- The following tools installed:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Optional)
  - Python 3.10 or later

Run the [Hosted agents quickstart with `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) at least once before delivery so you have a known-good Foundry project, model deployment, and Azure Container Registry to reference if a learner gets stuck.

---

## Slide walkthrough

The deck follows the same flow as the labs. Suggested talking points for each section:

| Section                     | Key message                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Title and agenda            | Frame the workshop as *VS Code to Foundry* with no portal switching required.                                |
| Why hosted agents?          | Managed runtime, ACR-based deployment, OpenAI-compatible `/responses` API, scoped to Foundry projects.        |
| Architecture diagram        | Walk through the [README architecture](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.   |
| Anatomy of a hosted agent   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - what each file does.                              |
| Live demo: Executive Agent  | Switch to VS Code and run the [`ExecutiveAgent/`](../ExecutiveAgent/) demo end-to-end (see [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Switch to VS Code and run the [`PersonalCareerCopilot/`](../workshop/lab02-multi-agent/PersonalCareerCopilot/) 4-agent demo (see [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 brief                | Hand off to learners. Point at [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Multi-agent patterns        | Sequential vs concurrent vs handoff - preview before Lab 02 starts.                                           |
| Lab 02 brief                | Hand off to learners. Point at [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Wrap-up and resources       | Continued-learning links from the [Additional resources](#additional-resources) section.                      |

---

## Demos

Two live demos are included in the delivery. Allocate 10 minutes to each.

| Demo | Lab | Files | What to show |
|------|-----|-------|--------------|
| Executive Agent | Lab 01 | [`ExecutiveAgent/`](../ExecutiveAgent/) | Single hosted agent; translate technical jargon into an executive summary |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../workshop/lab02-multi-agent/PersonalCareerCopilot/) | 4-agent orchestration; score resume-job fit and generate a recommendation |

### Demo 1: Executive Agent

A standalone agent in [`ExecutiveAgent/`](../ExecutiveAgent/). Use this as a 10-minute demo before Lab 01.

1. Open [`ExecutiveAgent/main.py`](../ExecutiveAgent/main.py) and walk through the agent definition (system prompt, model, framework).
2. Press `F5` to launch the **Agent Inspector** locally.
3. Paste the sample prompt from the [README](../README.md#see-it-in-action) and show the executive-summary response.
4. Show [`ExecutiveAgent/agent.yaml`](../ExecutiveAgent/agent.yaml) and [`ExecutiveAgent/Dockerfile`](../ExecutiveAgent/Dockerfile) to explain the deployment artefacts.
5. Demonstrate the deployment flow (Docker build, ACR push, hosted agent create) without waiting for completion.

### Demo 2: Resume to Job Fit Evaluator

A 4-agent workflow in [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../workshop/lab02-multi-agent/PersonalCareerCopilot/). Use this as a 10-minute demo before Lab 02.

1. Open [`PersonalCareerCopilot/main.py`](../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) and show how the four agents are wired together in a sequential orchestration.
2. Press `F5` to launch the **Agent Inspector** for the multi-agent workflow.
3. Paste a short job description and a sample resume in the Inspector chat.
4. Walk through the four-agent pipeline: resume parser, job requirement extractor, fit scorer, and recommendation writer.
5. Point out how each sub-agent's output becomes the next agent's context, highlighting the handoff pattern.
6. Show [`PersonalCareerCopilot/agent.yaml`](../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) to compare with the single-agent equivalent from Demo 1.

---

## Delivery tips

- **Set expectations early.** Hosted agents are in preview - call out region limits and quota up front so attendees do not get surprised mid-lab.
- **Run the prerequisites task first.** Both labs ship a `Validate prerequisites` VS Code task - have attendees run it before any code is written.
- **Keep the Agent Inspector visible.** Most "aha" moments happen when learners see the local `/responses` round-trip light up.
- **Have a backup project.** If a learner's Foundry project hits a quota wall, share a pre-provisioned project for the deployment step rather than blocking the room.
- **Pair attendees.** Lab 02 (multi-agent) is meaningfully easier when learners can talk through the orchestration with a partner.
- **Use the docs modules as checkpoints.** Each lab's `docs/` folder is split into 8 numbered modules - use those as natural pause points.
- **Pre-pull the base Docker image** on shared lab machines to avoid registry rate limits.

---

## Troubleshooting during delivery

| Symptom                                      | First thing to try                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector cannot connect               | Confirm port `8088` is free and the `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` task is running.   |
| Debugger fails to attach                     | Check that port `5679` is free; restart VS Code if `debugpy` is already bound.                           |
| `azd up` fails with auth error               | Run `az login` and `azd auth login`, ensure the correct tenant is selected.                              |
| Deployment hangs at ACR push                 | Check Docker Desktop is running and the user has `AcrPush` on the registry.                              |
| Model returns 404 / deployment-not-found     | The model deployment name in `agent.yaml` must match the deployment in the Foundry project.              |
| Hosted agent stuck in `Provisioning`         | Verify the project region [supports hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) and that quota is available. |
| Playground returns 401                       | Re-authenticate the Foundry extension from the VS Code activity bar.                                     |

For deeper guidance, every lab ships its own `08-troubleshooting.md` doc - link learners there:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Customizing this session

You are welcome to adapt the workshop for your audience. Common variations:

- **Backend audiences:** spend more time on `agent.yaml`, Docker, and ACR; trim the playground demo.
- **Citizen-developer audiences:** stay in the Foundry extension UI for scaffolding; reduce CLI steps.
- **Single-track 60-minute slot:** deliver intro, demo, and Lab 01 only.
- **Workshop-only (no slides) format:** open both lab READMEs and use them as the primary script.

If you extend the labs, please contribute the changes back via PR so other trainers benefit.

---

## Additional resources

- [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Hosted agents overview](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Quickstart: deploy your first hosted agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Deploy a hosted agent (how-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contacts

If you have questions about delivering this session, please open an issue on the [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) and tag the maintainer.

| Role                | Name           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Maintainer / contact| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |
