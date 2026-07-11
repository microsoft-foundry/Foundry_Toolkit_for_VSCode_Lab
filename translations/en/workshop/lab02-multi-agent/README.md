# Lab 02 - Multi-Agent Workflow: Resume → Job Fit Evaluator

## Overview

In this hands-on lab, you'll build a **workflow-first multi-agent app** using Foundry Toolkit in VS Code and deploy it to Microsoft Foundry Agent Service.

**What you'll build:** a Resume → Job Fit Evaluator that parses a resume and job description, scores the match, and produces a personalized learning roadmap using Microsoft Learn resources.

---

## Architecture

```mermaid
flowchart TD
    A["User Input"] --> B["Resume Parser"]
    B -->|"[PARSED RESUME] + [JOB DESCRIPTION PASS-THROUGH]"| C["Job Description Agent"]
    C -->|"[JD REQUIREMENTS] + [PARSED RESUME PASS-THROUGH]"| D["Matching Agent"]
    D -->|fit report + gaps| E["Gap Analyzer + Microsoft Learn MCP"]
    E -->|fit score + roadmap| F["Output"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

**How it works:**
1. The user pastes a resume and job description.
2. **ResumeParser** parses the resume and copies the JD verbatim into a `[JOB DESCRIPTION PASS-THROUGH]` section.
3. **JD Agent** extracts structured requirements from the pass-through, then relays the `[PARSED RESUME]` forward as `[PARSED RESUME PASS-THROUGH]`.
4. **MatchingAgent** compares `[PARSED RESUME PASS-THROUGH]` vs `[JD REQUIREMENTS]` and produces a fit score.
5. **GapAnalyzer** turns the gaps into a practical roadmap and fetches real Microsoft Learn links via MCP.

---

## Prerequisites

Complete Lab 01 first:

- [Lab 01 - Single Agent](../lab01-single-agent/README.md)

---

## Part 1: Read the modules in order

See the full learning path in:

- [Lab 2 Docs - Prerequisites](docs/00-prerequisites.md)
- [Lab 2 Docs - Full Learning Path](docs/README.md)
- [PersonalCareerCopilot run guide](PersonalCareerCopilot/README.md)

---

## Part 2: Build and test the workflow

1. Use the Foundry Toolkit wizard to scaffold the workflow-based project.
2. Copy the prompt blocks and workflow graph from `PersonalCareerCopilot/main.py` into your workspace.
3. Run locally with the Agent Inspector and verify all four agents plus the MCP tool.
4. Deploy the hosted agent to Foundry when local testing passes.

---

## Orchestration patterns

Lab 02 includes the default **fan-out → fan-in → sequential** flow, and the docs also describe alternative orchestration patterns for experimentation.

- **Fan-out/Fan-in with weighted consensus**
- **Reviewer/critic pass before final roadmap**
- **Conditional router** based on fit score and missing skills

See [docs/04-orchestration-patterns.md](docs/04-orchestration-patterns.md).

---

**Previous:** [Lab 01 - Single Agent](../lab01-single-agent/README.md) · **Back to:** [Workshop Home](../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
This document has been translated using AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). While we strive for accuracy, please be aware that automated translations may contain errors or inaccuracies. The original document in its native language should be considered the authoritative source. For critical information, professional human translation is recommended. We are not liable for any misunderstandings or misinterpretations arising from the use of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->