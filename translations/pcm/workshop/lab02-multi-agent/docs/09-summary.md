# Module 9 - Summary & Next Steps

⏱️ ~5 min

**Congratulations!** You don build, test, an (if na Path A) deploy multi-agent workflow wey use Microsoft Foundry an di Foundry Toolkit for VS Code.

---

## Wetin you build

Di **Resume → Job Fit Evaluator** - na multi-agent hosted workflow wey:
- Dey receive resume + job description via HTTP (`POST /responses`)
- Dey run four specialized agents one after di oda - each agent dey pass di data wey im successor need
- Dey return fit score (0–100 wit breakdown), skill an certification gap list, plus personalized learning roadmap wit real Microsoft Learn links for each gap
- Dey call Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) to fetch official learning resources for each skill gap wey dem find
- Dey run as one single containerized hosted agent for Microsoft Foundry Agent Service

---

## Key concepts wey you learn

| Concept | Wetin you practice |
|---------|-------------------|
| **Multi-agent orchestration** | `WorkflowBuilder` sequential pipeline wit `add_edge()` |
| **Agent specialization** | Four focused agents do pass one general-purpose agent |
| **Content Router pattern** | ResumeParser still dey act as router - e dey keep di JD text inside `[JOB DESCRIPTION PASS-THROUGH]` section so downstream agents fit access am (dis na because `context_mode="last_agent"` mean sey only di `start_executor` go see di raw user message) |
| **Content Relay pattern** | JD Agent dey relay `[PARSED RESUME PASS-THROUGH]` forward so MatchingAgent go get both profiles; e dey avoid di OR-semantics double-trigger wey fan-in graphs cause |
| **MCP tool integration** | `@tool` + `streamable_http_client` wey dey call external MCP server |
| **Hosted Agent lifecycle** | Scaffold → Configure → Test locally → Deploy → Verify for cloud |
| **`context_mode="last_agent"`** | Each executor dey see only wetin im direct predecessor output |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, one-click deploy |

---

## Wetin you complete

<details open>
<summary><strong>🅰️ Path A - Foundry subscription</strong></summary>

- [x] Verify Lab 01 setup: project, model, an RBAC still dey active
- [x] Scaffold multi-agent project wey use di Workflows template
- [x] Write four agent instruction sets (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrate Microsoft Learn MCP tool wit `streamable_http_client`
- [x] Wire di workflow graph wit `WorkflowBuilder` (sequential pipeline wit content relay)
- [x] Test locally wit 3 smoke tests (Agent Inspector) - fit score, gap cards, an MCP URLs
- [x] Deploy to Foundry Agent Service (containerized, managed identity)
- [x] Verify for cloud playground - structural consistency wit local results

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local</strong></summary>

- [x] Verify Lab 01 setup: Foundry Local dey run wit one local model
- [x] Scaffold multi-agent project wey use Workflows template
- [x] Write four agent instruction sets an wire di workflow graph
- [x] Integrate Microsoft Learn MCP tool
- [x] Test locally wit 3 smoke tests
- [x] Validate multi-agent behavior without cloud resources

</details>

---

## Next steps

### Continue to learn

| Resource | Description |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs for `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Connect agents to oda MCP servers (Bing, GitHub, custom) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ground agents wit documents, vector stores, or Bing search |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Measure agent quality at scale wit automated evaluators |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Full platform reference |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extension release notes an changelog |

### Ideas to extend dis workflow

- **Add 5th agent** - Interview coach wey go produce likely interview questions based on gap report
- **Add Bing grounding tool** - Make JD Agent fit search for similar job postings to enrich requirements
- **Connect to resume database** - Pull candidate profiles from database via custom `@tool`
- **Try different models** - Compare `gpt-4.1` vs. `gpt-4.1-mini` for output quality an latency
- **Evaluate wit Foundry** - Use Evaluations feature to score fit reports against golden dataset

### For Path B users: Upgrade go cloud deployment

When you don ready to deploy to cloud:
1. Get Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (create project, deploy model, assign RBAC)
3. Update your `.env` wit Foundry project endpoint an model deployment name
4. Continue from [Module 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Clean up resources (optional)

If you want remove di Azure resources wey you create during dis workshop:

### Option 1: Delete di resource group (e go remove everything)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Delete only di hosted agent

1. Open [ai.azure.com](https://ai.azure.com) → your project → **Build** → **Agents**.
2. Find **PersonalCareerCopilot** → click **Delete**.

### Option 3: Delete di model deployment

1. For Foundry sidebar, expand your project → **Models**.
2. Right-click di model deployment → **Delete**.

> **Cost note:** Hosted agents dey cost only when dem dey run. If you stop or delete agent, no charge go dey again. Model deployment fit get small charge for reserved capacity - delete am if you done.

---

**Previous:** [08 - Troubleshooting](08-troubleshooting.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->