# Module 0 - Introdakshon

⏱️ ~10 min

> [!WARNING]
> **Preview & Limitations:** [Hosted Agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) de now for **public preview** - e no too beta for production work dem. Some tins wey dis workshop show fit change as service dey move go GA.

## Wetin you go build

For dis lab, you go extend the single-agent skills wey you learn for Lab 01 to build **multi-agent workflow** - di Resume → Job Fit Evaluator.

You go paste **resume** and **job description** inside. Four special agents go process di tins one by one, den return:
- Fit score (0–100 wit scoring breakdown)
- Skill and certification gap list
- Personal learning roadmap wit real Microsoft Learn links for each gap

**Di workflow dey use:**
- **Microsoft Agent Framework** - `WorkflowBuilder` for sequential pipeline orchestration
- **Foundry Toolkit for VS Code** - scaffold, test locally, deploy
- **AI model** (like `gpt-4.1-mini`) wey all four agents dey use
- **Microsoft Learn MCP server** - dey provide real learning links for every skill gap

---

## Choose your path

> ⚠️ **Continue wit di same path wey you use for Lab 01.**

<details open>
<summary><strong>🅰️ Path A - Azure cloud (you go need Azure subscription)</strong></summary>

| | Details |
|---|---|
| **Who na for dis one?** | You finish Lab 01 using Azure subscription |
| **Model** | Azure OpenAI via Foundry (like `gpt-4.1-mini`) |
| **Modules wey cover** | All modules (00–09) |
| **Deploy go cloud?** | ✅ Yes - full end-to-end deployment |

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local (no need Azure subscription)</strong></summary>

| | Details |
|---|---|
| **Who na for dis one?** | You finish Lab 01 using Foundry Local |
| **Model** | Foundry Local (free, e dey run for your machine) |
| **Modules wey cover** | Modules 00–05 (skip 06–07 - deploy & cloud verify) |
| **Deploy go cloud?** | ❌ No - na local testing only via Agent Inspector |

</details>

---

## Lab 01 check

Lab 02 na build directly on top Lab 01. Make you finish Lab 01 first before you start here.

You neva do Lab 01 yet? Start for here: [Lab 01 - Introdakshon](../../lab01-single-agent/docs/00-prerequisites.md)

<details open>
<summary><strong>🅰️ Path A - Azure cloud</strong></summary>

```powershell
az account show --query "{name:name, id:id}" --output table
```

If e fail, run `az login`. Den check for VS Code:

1. `Ctrl+Shift+P` → type **Foundry Toolkit** → confirm say commands dey show.
2. Click **Foundry Toolkit** icon → your project and deployed model go show **Succeeded**.

![Foundry Toolkit sidebar showing MY RESOURCES section with the project switcher modal open](../../../../../translated_images/pcm/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

> **RBAC:** You assign **Foundry User** for Lab 01. If you need assign again, see [Lab 01, Module 1](../../lab01-single-agent/docs/01-setup.md#deploy-a-model--assign-rbac). The role before e de call **Azure AI User** - permissions na the same.

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local</strong></summary>

```powershell
Invoke-WebRequest -Uri "http://localhost:5273/v1/health" -UseBasicParsing | Select-Object StatusCode
```

Expect: `StatusCode: 200`. If no, restart Foundry Local from Foundry Toolkit sidebar.

> All inference dey run for your machine. The only outbound call na MCP tool to `https://learn.microsoft.com/api/mcp`.

</details>

---

## Wetin new for Lab 02

| | Lab 01 | Lab 02 |
|--|--------|--------|
| Agents | 1 | 4 (chained wit WorkflowBuilder) |
| Scaffold template | Basic - Agent Framework | Workflows - Agent Framework |
| New package | - | `mcp` |
| Orchestration | Single conversational agent | Sequential pipeline (WorkflowBuilder) |
| New tool | - | `search_microsoft_learn_for_plan` (MCP) |

---

**Next:** [01 - Understand the Architecture →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->