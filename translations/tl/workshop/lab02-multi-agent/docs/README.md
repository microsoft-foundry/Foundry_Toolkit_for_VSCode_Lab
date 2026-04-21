# Lab 02 - Multi-Agent Workflow: Resume → Job Fit Evaluator

## Buong Landas ng Pagkatuto

Ang dokumentasyong ito ay gagabay sa iyo sa pagbuo, pagsubok, at pag-deploy ng isang **multi-agent workflow** na sumusuri sa tugma ng resume sa trabaho gamit ang apat na espesyal na ahente na pinamamahalaan sa pamamagitan ng **WorkflowBuilder**.

> **Kinakailangan:** Kumpletuhin ang [Lab 01 - Single Agent](../../lab01-single-agent/README.md) bago simulan ang Lab 02.

---

## Mga Module

| # | Module | Ano ang gagawin mo |
|---|--------|--------------------|
| 0 | [Prerequisites](00-prerequisites.md) | Beripikahin ang pagkakumpleto ng Lab 01, unawain ang mga konsepto ng multi-agent |
| 1 | [Understand Multi-Agent Architecture](01-understand-multi-agent.md) | Matutunan ang WorkflowBuilder, mga tungkulin ng ahente, orchestration graph |
| 2 | [Scaffold the Multi-Agent Project](02-scaffold-multi-agent.md) | Gamitin ang Foundry extension para mag-scaffold ng multi-agent workflow |
| 3 | [Configure Agents & Environment](03-configure-agents.md) | Isulat ang mga instruksyon para sa 4 na ahente, i-configure ang MCP tool, itakda ang mga env vars |
| 4 | [Orchestration Patterns](04-orchestration-patterns.md) | Tuklasin ang parallel fan-out, sequential aggregation, at mga alternatibong pattern |
| 5 | [Test Locally](05-test-locally.md) | Debug gamit ang F5 sa Agent Inspector, patakbuhin ang smoke tests gamit ang resume + JD |
| 6 | [Deploy to Foundry](06-deploy-to-foundry.md) | Bumuo ng container, i-push sa ACR, irehistro ang hosted agent |
| 7 | [Verify in Playground](07-verify-in-playground.md) | Subukan ang na-deploy na ahente sa VS Code at Foundry Portal playgrounds |
| 8 | [Troubleshooting](08-troubleshooting.md) | Ayusin ang mga karaniwang problema sa multi-agent (MCP errors, truncated output, package versions) |

---

## Tinatayang Oras

| Antas ng Karanasan | Oras |
|--------------------|------|
| Kamakailang nakatapos ng Lab 01 | 45-60 minuto |
| May ilang karanasan sa Azure AI | 60-90 minuto |
| Unang beses sa multi-agent | 90-120 minuto |

---

## Arkitektura sa isang sulyap

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

**Bumalik sa:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Paunawa**:
Ang dokumentong ito ay isinalin gamit ang serbisyong AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagamat nagsisikap kami para sa kawastuhan, pakatandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o maling interpretasyon. Ang orihinal na dokumento sa kanyang likas na wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na nagmumula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->