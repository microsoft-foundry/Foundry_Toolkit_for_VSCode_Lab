# Module 7 - Summary & Next Steps

⏱️ ~5 min

**Congratulations!** You don build, test, and (if na Path A) deploy one hosted AI agent wey use Microsoft Foundry and di Foundry Toolkit for VS Code.

---

## Wetin you build

One **"Explain Like I'm an Executive"** agent wey:
- Dey receive technical incident reports or operational updates thru HTTP (`POST /responses`)
- Dey translate dem go plain language executive summaries
- Dey follow structured output format (Wetin happen / Business impact / Next step)
- No dey accept off-topic requests and prompt injection attempts
- Dey run as containerized hosted agent for Microsoft Foundry Agent Service

---

## Key concepts wey you learn

| Concept | Wetin you practice |
|---------|-------------------|
| **Agent Framework architecture** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hosted Agent lifecycle** | Scaffold → Configure → Test locally → Deploy → Verify for cloud |
| **System prompt engineering** | Role, audience, output format, rules, safety constraints, and examples |
| **Local vs. hosted differences** | Identity (personal credential vs. managed identity), endpoint, network path |
| **Safety boundaries** | Prompt injection defense, role adherence, graceful handling of edge cases |
| **Foundry Toolkit workflow** | Project creation, model deployment, agent scaffolding, Agent Inspector, one-click deploy |

---

## Wetin you complete

### Path A (Foundry subscription)

- [x] Set up Foundry Toolkit and create Foundry project wey get deployed model
- [x] Scaffolded one hosted agent with auto-generated project structure
- [x] Write structured agent instructions with safety rules
- [x] Test am locally with 3 functional scenarios (Agent Inspector)
- [x] Deploy am to Foundry Agent Service (containerized)
- [x] Verify for cloud playground with 4 edge-case/safety tests

### Path B (Foundry Local)

- [x] Set up Foundry Toolkit with local model endpoint
- [x] Scaffolded a hosted agent project
- [x] Write structured agent instructions with safety rules
- [x] Test am locally with 3 functional scenarios
- [x] Validate agent behavior without cloud resources

---

## Next steps

### Continue to learn

| Resource | Description |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Build 4-agent workflow (Resume → Job Fit Evaluator) with orchestration patterns |
| **[Add tools to your agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Connect APIs, databases, or custom functions thru Tool Catalog |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ground your agent with documents, vector stores, or Bing search |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Full platform reference |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs for `agent-framework` package |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extension release notes and changelog |

### Ideas to extend your agent

- **Add date tool** - Make agent fit include "as of today" context for summaries
- **Connect to incident database** - Pull real incident details via tool function
- **Add Bing grounding tool** - Make agent fit look up recent news for extra context
- **Try different models** - Compare `gpt-4.1` vs. `gpt-4.1-mini` output quality
- **Evaluate with Foundry** - Use Evaluations feature to measure agent quality for scale

### For Path B users: Upgrade go cloud deployment

When you ready to deploy go cloud:
1. Get Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Module 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (create project, deploy model, assign RBAC)
3. Update your `.env` with Foundry project endpoint and model deployment name
4. Continue from [Module 05 - Deploy to Foundry](05-deploy-to-foundry.md)

---

## Clean up resources (optional)

If you wan remove Azure resources wey dem create during this workshop:

### Option 1: Delete resource group (go wipe everything)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Delete only hosted agent

1. Open [ai.azure.com](https://ai.azure.com) → your project → **Build** → **Agents**.
2. Click your agent → click **Delete**.

### Option 3: Delete model deployment

1. For Foundry sidebar, expand your project → **Models**.
2. Right-click model deployment → **Delete**.

> **Cost note:** Hosted agents dey cost only when dem dey run. If you stop or delete agent, no cost again. Model deployment fit get small charge for reserved capacity - delete am if you finish.

---

**Previous:** [06 - Verify in Playground](06-verify-in-playground.md) · **Next:** [08 - Troubleshooting (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->