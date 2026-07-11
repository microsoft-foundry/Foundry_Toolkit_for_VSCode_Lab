# Module 7 - Summary & Next Steps

⏱️ ~5 min

**Congratulations!** You've built, tested, and (if on Path A) deployed a hosted AI agent using Microsoft Foundry and the Foundry Toolkit for VS Code.

---

## What you built

An **"Explain Like I'm an Executive"** agent that:
- Receives technical incident reports or operational updates via HTTP (`POST /responses`)
- Translates them into plain-language executive summaries
- Follows a structured output format (What happened / Business impact / Next step)
- Refuses off-topic requests and prompt injection attempts
- Runs as a containerized hosted agent in Microsoft Foundry Agent Service

---

## Key concepts learned

| Concept | What you practiced |
|---------|-------------------|
| **Agent Framework architecture** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hosted Agent lifecycle** | Scaffold → Configure → Test locally → Deploy → Verify in cloud |
| **System prompt engineering** | Role, audience, output format, rules, safety constraints, and examples |
| **Local vs. hosted differences** | Identity (personal credential vs. managed identity), endpoint, network path |
| **Safety boundaries** | Prompt injection defense, role adherence, graceful handling of edge cases |
| **Foundry Toolkit workflow** | Project creation, model deployment, agent scaffolding, Agent Inspector, one-click deploy |

---

## What you completed

### Path A (Foundry subscription)

- [x] Set up Foundry Toolkit and created a Foundry project with a deployed model
- [x] Scaffolded a hosted agent with auto-generated project structure
- [x] Wrote structured agent instructions with safety rules
- [x] Tested locally with 3 functional scenarios (Agent Inspector)
- [x] Deployed to Foundry Agent Service (containerized)
- [x] Verified in cloud playground with 4 edge-case/safety tests

### Path B (Foundry Local)

- [x] Set up Foundry Toolkit with a local model endpoint
- [x] Scaffolded a hosted agent project
- [x] Wrote structured agent instructions with safety rules
- [x] Tested locally with 3 functional scenarios
- [x] Validated agent behavior without needing cloud resources

---

## Next steps

### Continue learning

| Resource | Description |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Build a 4-agent workflow (Resume → Job Fit Evaluator) with orchestration patterns |
| **[Add tools to your agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Connect APIs, databases, or custom functions via the Tool Catalog |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ground your agent with documents, vector stores, or Bing search |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Full platform reference |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs for `agent-framework` package |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extension release notes and changelog |

### Ideas to extend your agent

- **Add a date tool** - Let the agent include "as of today" context in summaries
- **Connect to an incident database** - Pull real incident details via a tool function
- **Add a Bing grounding tool** - Let the agent look up recent news for additional context
- **Try different models** - Compare `gpt-4.1` vs. `gpt-4.1-mini` output quality
- **Evaluate with Foundry** - Use the Evaluations feature to measure agent quality at scale

### For Path B users: Upgrade to cloud deployment

When you're ready to deploy to the cloud:
1. Get an Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Module 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (create project, deploy model, assign RBAC)
3. Update your `.env` with the Foundry project endpoint and model deployment name
4. Continue from [Module 05 - Deploy to Foundry](05-deploy-to-foundry.md)

---

## Clean up resources (optional)

If you want to remove the Azure resources created during this workshop:

### Option 1: Delete the resource group (removes everything)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Delete just the hosted agent

1. Open [ai.azure.com](https://ai.azure.com) → your project → **Build** → **Agents**.
2. Click your agent → click **Delete**.

### Option 3: Delete the model deployment

1. In the Foundry sidebar, expand your project → **Models**.
2. Right-click the model deployment → **Delete**.

> **Cost note:** Hosted agents only incur cost when running. If you stop or delete the agent, there's no ongoing charge. The model deployment may incur a small charge for reserved capacity - delete it if you're done.

---

**Previous:** [06 - Verify in Playground](06-verify-in-playground.md) · **Next:** [08 - Troubleshooting (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->