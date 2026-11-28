# Module 7 - Summary & Next Steps

⏱️ ~5 min

**Congratulations!** You don build, test, and (if na Path A) deploy one hosted AI agent wey use Microsoft Foundry and the Foundry Toolkit for VS Code.

---

## Wetin you build

One **"Explain Like I'm an Executive"** agent wey:
- Dey receive technical incident reports or operational updates through HTTP (`POST /responses`)
- Dey translate dem into plain-language executive summaries
- Dey follow one structured output format (Wetin happen / Business impact / Next step)
- No dey accept off-topic requests and prompt injection try
- Dey run as containerized hosted agent for Microsoft Foundry Agent Service

---

## Main concepts wey you learn

| Concept | Wetin you practice |
|---------|-------------------|
| **Agent Framework architecture** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hosted Agent lifecycle** | Scaffold → Configure → Test locally → Deploy → Verify for cloud |
| **System prompt engineering** | Role, audience, output format, rules, safety constraints, and examples |
| **Local vs. hosted differences** | Identity (personal credential vs. managed identity), endpoint, network path |
| **Safety boundaries** | Prompt injection defense, role adherence, graceful handling of edge cases |
| **Foundry Toolkit workflow** | Project creation, model deployment, agent scaffolding, Agent Inspector, one-click deploy |

---

## Wetin you finish

### Path A (Foundry subscription)

- [x] Set up Foundry Toolkit and create one Foundry project with deployed model
- [x] Scaffold one hosted agent with auto-generated project structure
- [x] Write structured agent instructions with safety rules
- [x] Test locally with 3 functional scenarios (Agent Inspector)
- [x] Deploy for Foundry Agent Service (containerized)
- [x] Verify for cloud playground with 4 edge-case/safety tests

### Path B (Foundry Local)

- [x] Set up Foundry Toolkit with local model endpoint
- [x] Scaffold one hosted agent project
- [x] Write structured agent instructions with safety rules
- [x] Test locally with 3 functional scenarios
- [x] Validate agent behavior without needing cloud resources

---

## Next steps

### Continue to learn

| Resource | Description |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Build 4-agent workflow (Resume → Job Fit Evaluator) with orchestration patterns |
| **[Add tools to your agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Connect APIs, databases, or custom functions through the Tool Catalog |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ground your agent with documents, vector stores, or Bing search |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Full platform reference |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs for `agent-framework` package |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extension release notes and changelog |

### Ideas to make your agent better

- **Add date tool** - Make the agent include "as of today" context in summaries
- **Connect to incident database** - Pull real incident details through tool function
- **Add Bing grounding tool** - Make agent fit check recent news for more context
- **Try different models** - Compare `gpt-4.1` vs. `gpt-4.1-mini` output quality
- **Evaluate with Foundry** - Use Evaluations feature to check agent quality for scale

### For Path B users: Upgrade to cloud deployment

When you ready to deploy to cloud:
1. Get Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Finish [Module 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (create project, deploy model, assign RBAC)
3. Update your `.env` with Foundry project endpoint and model deployment name
4. Continue from [Module 05 - Deploy to Foundry](05-deploy-to-foundry.md)

---

## Clean up resources (if you want)

If you want remove the Azure resources wey you create during this workshop:

### Option 1: Delete the resource group (go kill all)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Delete just the hosted agent

1. Open [ai.azure.com](https://ai.azure.com) → your project → **Build** → **Agents**.
2. Click your agent → click **Delete**.

### Option 3: Delete the model deployment

1. For the Foundry sidebar, open your project → **Models**.
2. Right-click the model deployment → **Delete**.

> **Cost note:** Hosted agents dey only cost money when dem dey run. If you stop or delete the agent, no charge go continue. The model deployment fit get small charge for reserved capacity - delete am if you don finish.

---

**Previous:** [06 - Verify in Playground](06-verify-in-playground.md) · **Next:** [08 - Troubleshooting (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->