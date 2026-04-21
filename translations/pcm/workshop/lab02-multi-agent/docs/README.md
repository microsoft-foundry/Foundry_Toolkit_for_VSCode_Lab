# Lab 02 - Multi-Agent Workflow: Resume → Job Fit Evaluator

## Full Learning Path

Dis documentation go waka you through how to build, test, and deploy **multi-agent workflow** wey dey evaluate resume-to-job fit using four special agents wey WorkflowBuilder dey control.

> **Prerequisite:** Complete [Lab 01 - Single Agent](../../lab01-single-agent/README.md) before you start Lab 02.

---

## Modules

| # | Module | Wetin you go do |
|---|--------|-----------------|
| 0 | [Prerequisites](00-prerequisites.md) | Check say you don finish Lab 01, understand multi-agent concepts |
| 1 | [Understand Multi-Agent Architecture](01-understand-multi-agent.md) | Learn WorkflowBuilder, agent roles, orchestration graph |
| 2 | [Scaffold the Multi-Agent Project](02-scaffold-multi-agent.md) | Use the Foundry extension to scaffold multi-agent workflow |
| 3 | [Configure Agents & Environment](03-configure-agents.md) | Write instructions for 4 agents, set up MCP tool, arrange env vars |
| 4 | [Orchestration Patterns](04-orchestration-patterns.md) | Explore parallel fan-out, sequential aggregation, and alternative patterns |
| 5 | [Test Locally](05-test-locally.md) | F5 debug with Agent Inspector, run smoke tests with resume + JD |
| 6 | [Deploy to Foundry](06-deploy-to-foundry.md) | Build container, push am to ACR, register hosted agent |
| 7 | [Verify in Playground](07-verify-in-playground.md) | Test the deployed agent for VS Code and Foundry Portal playgrounds |
| 8 | [Troubleshooting](08-troubleshooting.md) | Fix common multi-agent wahala (MCP errors, truncated output, package versions) |

---

## Estimated time

| Experience level | Time |
|-----------------|------|
| Recently finish Lab 01 | 45-60 minutes |
| Get some Azure AI experience | 60-90 minutes |
| First time for multi-agent | 90-120 minutes |

---

## Architecture at a glance

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Back to:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you sabi say automated translations fit get errors or wrong tins. Di original document wey dey im own language na di real correct source. For important matter dem, e good make professional human translation do am. We no go responsible for any misunderstanding or wrong meaning wey fit come from dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->