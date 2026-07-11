# Module 9 - Summary & Next Steps

⏱️ ~5 min

**Congratulations!** You've built, tested, and (if on Path A) deployed a multi-agent workflow using Microsoft Foundry and the Foundry Toolkit for VS Code.

---

## What you built

The **Resume → Job Fit Evaluator** - a multi-agent hosted workflow that:
- Receives a resume + job description via HTTP (`POST /responses`)
- Runs four specialized agents in a sequential pipeline - each agent relays the data its successor needs
- Returns a fit score (0–100 with a breakdown), a skill and certification gap list, and a personalized learning roadmap with real Microsoft Learn links for each gap
- Calls the Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) to fetch official learning resources for each identified skill gap
- Runs as a single containerized hosted agent in Microsoft Foundry Agent Service

---

## Key concepts learned

| Concept | What you practiced |
|---------|-------------------|
| **Multi-agent orchestration** | `WorkflowBuilder` sequential pipeline with `add_edge()` |
| **Agent specialization** | Four focused agents outperform one general-purpose agent |
| **Content Router pattern** | ResumeParser doubles as a router - it preserves the JD text in a `[JOB DESCRIPTION PASS-THROUGH]` section so downstream agents can access it (required because `context_mode="last_agent"` means only the `start_executor` sees the raw user message) |
| **Content Relay pattern** | JD Agent relays `[PARSED RESUME PASS-THROUGH]` forward so MatchingAgent gets both profiles; avoids the OR-semantics double-trigger that fan-in graphs cause |
| **MCP tool integration** | `@tool` + `streamable_http_client` calling an external MCP server |
| **Hosted Agent lifecycle** | Scaffold → Configure → Test locally → Deploy → Verify in cloud |
| **`context_mode="last_agent"`** | Each executor sees only its direct predecessor's output |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, one-click deploy |

---

## What you completed

<details open>
<summary><strong>🅰️ Path A - Foundry subscription</strong></summary>

- [x] Verified Lab 01 setup: project, model, and RBAC still active
- [x] Scaffolded a multi-agent project using the Workflows template
- [x] Wrote four agent instruction sets (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrated the Microsoft Learn MCP tool with `streamable_http_client`
- [x] Wired the workflow graph with `WorkflowBuilder` (sequential pipeline with content relay)
- [x] Tested locally with 3 smoke tests (Agent Inspector) - fit score, gap cards, and MCP URLs
- [x] Deployed to Foundry Agent Service (containerized, managed identity)
- [x] Verified in cloud playground - structural consistency with local results

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local</strong></summary>

- [x] Verified Lab 01 setup: Foundry Local running with a local model
- [x] Scaffolded a multi-agent project using the Workflows template
- [x] Wrote four agent instruction sets and wired the workflow graph
- [x] Integrated the Microsoft Learn MCP tool
- [x] Tested locally with 3 smoke tests
- [x] Validated multi-agent behavior without needing cloud resources

</details>

---

## Next steps

### Continue learning

| Resource | Description |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs for `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Connect agents to other MCP servers (Bing, GitHub, custom) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ground agents with documents, vector stores, or Bing search |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Measure agent quality at scale with automated evaluators |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Full platform reference |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extension release notes and changelog |

### Ideas to extend this workflow

- **Add a 5th agent** - An interview coach that produces likely interview questions based on the gap report
- **Add a Bing grounding tool** - Let the JD Agent search for similar job postings to enrich requirements
- **Connect to a resume database** - Pull candidate profiles from a database via a custom `@tool`
- **Try different models** - Compare `gpt-4.1` vs. `gpt-4.1-mini` output quality and latency
- **Evaluate with Foundry** - Use the Evaluations feature to score fit reports against a golden dataset

### For Path B users: Upgrade to cloud deployment

When you're ready to deploy to the cloud:
1. Get an Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (create project, deploy model, assign RBAC)
3. Update your `.env` with the Foundry project endpoint and model deployment name
4. Continue from [Module 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Clean up resources (optional)

If you want to remove the Azure resources created during this workshop:

### Option 1: Delete the resource group (removes everything)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Delete just the hosted agent

1. Open [ai.azure.com](https://ai.azure.com) → your project → **Build** → **Agents**.
2. Find **PersonalCareerCopilot** → click **Delete**.

### Option 3: Delete the model deployment

1. In the Foundry sidebar, expand your project → **Models**.
2. Right-click the model deployment → **Delete**.

> **Cost note:** Hosted agents only incur cost when running. If you stop or delete the agent, there's no ongoing charge. The model deployment may incur a small charge for reserved capacity - delete it if you're done.

---

**Previous:** [08 - Troubleshooting](08-troubleshooting.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->