# Module 9 - Summary & Next Steps

⏱️ ~5 min

**Congrats!** You don build, test, and (if you dey for Path A) deploy multi-agent workflow wey use Microsoft Foundry and Foundry Toolkit for VS Code.

---

## Wetin you build

The **Resume → Job Fit Evaluator** - na multi-agent hosted workflow wey:
- Dey receive resume + job description via HTTP (`POST /responses`)
- Dey run four specialized agents one after another - each agent dey pass the data wey the next agent need
- Dey return fit score (0–100 with breakdown), skill and certification gap list, plus personalized learning roadmap with beta Microsoft Learn links for each gap
- Dey call Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) to collect official learning resources for each skill gap we dem identify
- Dey run as one containerized hosted agent in Microsoft Foundry Agent Service

---

## Key concepts wey you learn

| Concept | Wetin you practice |
|---------|-------------------|
| **Multi-agent orchestration** | `WorkflowBuilder` pipeline wey run sequentially with `add_edge()` |
| **Agent specialization** | Four focused agents pass one general-purpose agent |
| **Content Router pattern** | ResumeParser dey work as router too - e dey keep JD text for inside `[JOB DESCRIPTION PASS-THROUGH]` section so downstream agents fit access am (e necessary because `context_mode="last_agent"` mean say only `start_executor` go fit see raw user message) |
| **Content Relay pattern** | JD Agent dey pass `[PARSED RESUME PASS-THROUGH]` go forward so MatchingAgent go get both profiles; e avoid the OR-semantics double-trigger way fan-in graphs fit cause |
| **MCP tool integration** | `@tool` + `streamable_http_client` dey call external MCP server |
| **Hosted Agent lifecycle** | Scaffold → Configure → Test locally → Deploy → Verify for cloud |
| **`context_mode="last_agent"`** | Each executor dey see only the output of the agent wey come before am |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, one-click deploy |

---

## Wetin you complete

<details open>
<summary><strong>🅰️ Path A - Foundry subscription</strong></summary>

- [x] Verify Lab 01 setup: project, model, and RBAC still dey active
- [x] Scaffolded multi-agent project using Workflows template
- [x] Write four agent instruction sets (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrate Microsoft Learn MCP tool with `streamable_http_client`
- [x] Wire workflow graph with `WorkflowBuilder` (sequential pipeline with content relay)
- [x] Test locally with 2 smoke tests (Agent Inspector) - fit score, gap cards, MCP URLs
- [x] Deploy to Foundry Agent Service (containerized, managed identity)
- [x] Verify for cloud playground - structural consistency with local results

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local</strong></summary>

- [x] Verify Lab 01 setup: Foundry Local dey run with local model
- [x] Scaffolded multi-agent project using Workflows template
- [x] Write four agent instruction sets and wire workflow graph
- [x] Integrate Microsoft Learn MCP tool
- [x] Test locally with 2 smoke tests
- [x] Validate multi-agent behavior without cloud resources

</details>

---

## Next steps

### Continue to learn

| Resource | Description |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs for `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Connect agents to other MCP servers (Bing, GitHub, custom) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ground agents with documents, vector stores, or Bing search |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Measure agent quality at scale with automated evaluators |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Full platform reference |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extension release notes and changelog |

### Ideas to extend dis workflow

- **Add one 5th agent** - Interview coach wey go produce likely interview questions based on the gap report
- **Add Bing grounding tool** - Make JD Agent fit search for similar job postings to make requirements better
- **Connect to resume database** - Pull candidate profiles from database via custom `@tool`
- **Try different models** - Compare `gpt-4.1` vs. `gpt-4.1-mini` output quality and latency
- **Evaluate with Foundry** - Use Evaluations feature to score fit reports against golden dataset

### For Path B users: Upgrade to cloud deployment

When you ready to deploy to cloud:
1. Get Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (create project, deploy model, assign RBAC)
3. Update your `.env` with Foundry project endpoint and model deployment name
4. Continue from [Module 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Clean up resources (optional)

If you want remove Azure resources wey this workshop create:

### Option 1: Delete resource group (go remove everything)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Delete just the hosted agent

1. Open [ai.azure.com](https://ai.azure.com) → your project → **Build** → **Agents**.
2. Find **PersonalCareerCopilot** → click **Delete**.

### Option 3: Delete model deployment

1. For Foundry sidebar, expand your project → **Models**.
2. Right-click model deployment → **Delete**.

> **Cost note:** Hosted agents dey only cost money when e dey run. If you stop or delete the agent, you no go dey pay again. Model deployment fit get small charge for reserved capacity - delete am if you don finish.

---

**Previous:** [08 - Troubleshooting](08-troubleshooting.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->