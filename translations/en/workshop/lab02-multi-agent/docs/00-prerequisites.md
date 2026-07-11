# Module 0 - Introduction

⏱️ ~10 min

> [!WARNING]
> **Preview & Limitations:** [Hosted Agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) are currently in **public preview** - not recommended for production workloads. Some features shown in this workshop may change as the service moves toward GA.

## What you'll build

In this lab, you extend the single-agent skills from Lab 01 to build a **multi-agent workflow** - the Resume → Job Fit Evaluator.

You paste in a **resume** and a **job description**. Four specialized agents process the input sequentially, then return:
- A fit score (0–100 with a scoring breakdown)
- A skill and certification gap list
- A personalized learning roadmap with real Microsoft Learn links for each gap

**The workflow uses:**
- **Microsoft Agent Framework** - `WorkflowBuilder` for sequential pipeline orchestration
- **Foundry Toolkit for VS Code** - scaffold, test locally, deploy
- **An AI model** (e.g., `gpt-4.1-mini`) - used by all four agents
- **Microsoft Learn MCP server** - provides real learning resource links for each skill gap

---

## Choose your path

> ⚠️ **Continue with the same path you used in Lab 01.**

<details open>
<summary><strong>🅰️ Path A - Azure cloud (requires Azure subscription)</strong></summary>

| | Details |
|---|---|
| **Who is this for?** | You completed Lab 01 using an Azure subscription |
| **Model** | Azure OpenAI via Foundry (e.g., `gpt-4.1-mini`) |
| **Modules covered** | All modules (00–09) |
| **Deploy to cloud?** | ✅ Yes - full end-to-end deployment |

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local (no Azure subscription needed)</strong></summary>

| | Details |
|---|---|
| **Who is this for?** | You completed Lab 01 using Foundry Local |
| **Model** | Foundry Local (free, runs on your machine) |
| **Modules covered** | Modules 00–05 (skip 06–07 - deploy & cloud verify) |
| **Deploy to cloud?** | ❌ No - local testing only via Agent Inspector |

</details>

---

## Lab 01 check

Lab 02 builds directly on Lab 01. Complete Lab 01 first before starting here.

Haven't done Lab 01 yet? Start here: [Lab 01 - Introduction](../../lab01-single-agent/docs/00-prerequisites.md)

<details open>
<summary><strong>🅰️ Path A - Azure cloud</strong></summary>

```powershell
az account show --query "{name:name, id:id}" --output table
```

If this fails, run `az login`. Then verify in VS Code:

1. `Ctrl+Shift+P` → type **Foundry Toolkit** → confirm commands appear.
2. Click the **Foundry Toolkit** icon → your project and deployed model show **Succeeded**.

![Foundry Toolkit sidebar showing MY RESOURCES section with the project switcher modal open](../../../../../translated_images/en/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

> **RBAC:** You assigned **Foundry User** in Lab 01. If you need to re-assign it, see [Lab 01, Module 1](../../lab01-single-agent/docs/01-setup.md#deploy-a-model--assign-rbac). The role was previously named **Azure AI User** - same permissions.

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local</strong></summary>

```powershell
Invoke-WebRequest -Uri "http://localhost:5273/v1/health" -UseBasicParsing | Select-Object StatusCode
```

Expected: `StatusCode: 200`. If not, restart Foundry Local from the Foundry Toolkit sidebar.

> All inference runs on your machine. The only outbound call is the MCP tool to `https://learn.microsoft.com/api/mcp`.

</details>

---

## What's new in Lab 02

| | Lab 01 | Lab 02 |
|--|--------|--------|
| Agents | 1 | 4 (chained with WorkflowBuilder) |
| Scaffold template | Basic - Agent Framework | Workflows - Agent Framework |
| New package | - | `mcp` |
| Orchestration | Single conversational agent | Sequential pipeline (WorkflowBuilder) |
| New tool | - | `search_microsoft_learn_for_plan` (MCP) |

---

**Next:** [01 - Understand the Architecture →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->