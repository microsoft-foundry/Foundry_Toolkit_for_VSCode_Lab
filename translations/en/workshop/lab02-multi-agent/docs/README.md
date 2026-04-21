# Lab 02 - Multi-Agent Workflow: Resume → Job Fit Evaluator

## Full Learning Path

This documentation walks you through building, testing, and deploying a **multi-agent workflow** that evaluates resume-to-job fit using four specialized agents orchestrated via **WorkflowBuilder**.

> **Prerequisite:** Complete [Lab 01 - Single Agent](../../lab01-single-agent/README.md) before starting Lab 02.

---

## Modules

| # | Module | What you'll do |
|---|--------|---------------|
| 0 | [Prerequisites](00-prerequisites.md) | Verify Lab 01 completion, understand multi-agent concepts |
| 1 | [Understand Multi-Agent Architecture](01-understand-multi-agent.md) | Learn WorkflowBuilder, agent roles, orchestration graph |
| 2 | [Scaffold the Multi-Agent Project](02-scaffold-multi-agent.md) | Use the Foundry extension to scaffold a multi-agent workflow |
| 3 | [Configure Agents & Environment](03-configure-agents.md) | Write instructions for 4 agents, configure MCP tool, set env vars |
| 4 | [Orchestration Patterns](04-orchestration-patterns.md) | Explore parallel fan-out, sequential aggregation, and alternative patterns |
| 5 | [Test Locally](05-test-locally.md) | F5 debug with Agent Inspector, run smoke tests with resume + JD |
| 6 | [Deploy to Foundry](06-deploy-to-foundry.md) | Build container, push to ACR, register hosted agent |
| 7 | [Verify in Playground](07-verify-in-playground.md) | Test deployed agent in VS Code and Foundry Portal playgrounds |
| 8 | [Troubleshooting](08-troubleshooting.md) | Fix common multi-agent issues (MCP errors, truncated output, package versions) |

---

## Estimated time

| Experience level | Time |
|-----------------|------|
| Completed Lab 01 recently | 45-60 minutes |
| Some Azure AI experience | 60-90 minutes |
| First time with multi-agent | 90-120 minutes |

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
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->