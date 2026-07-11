# Lab 02 - Multi-Agent Workflow: Resume → Job Fit Evaluator

## Buong Landas ng Pagkatuto

Ang dokumentasyong ito ay gagabay sa iyo sa paggawa, pagsubok, at pag-deploy ng isang **multi-agent workflow** na sumusuri ng resume-to-job fit gamit ang apat na espesyalisadong ahente na pinamamahalaan sa pamamagitan ng **WorkflowBuilder**.

> **Kailangang Kaalaman:** Tapusin ang [Lab 01 - Single Agent](../../lab01-single-agent/README.md) bago simulan ang Lab 02.

---

## Mga Module

| # | Module | Ano ang gagawin mo |
|---|--------|------------------|
| 0 | [Panimula](00-prerequisites.md) | Ano ang itatayo mo, beripikasyon ng Lab 01, paghahambing ng Lab 02 vs Lab 01 |
| 1 | [Unawain ang Multi-Agent Architecture](01-understand-multi-agent.md) | Alamin ang WorkflowBuilder, papel ng mga ahente, orchestration graph |
| 2 | [Gawing Scaffold ang Multi-Agent Project](02-scaffold-multi-agent.md) | Gamitin ang Foundry extension wizard para gawing scaffold ang base project |
| 3 | [I-configure ang mga Ahente at Kapaligiran](03-configure-agents.md) | Isulat ang mga instruksyon para sa 4 na ahente, i-configure ang MCP tool, itakda ang env vars |
| 4 | [Mga Pattern ng Orchestration](04-orchestration-patterns.md) | Sunud-sunod na chain, content relay, at WorkflowBuilder OR-semantics |
| 5 | [Subukan Nang Lokal](05-test-locally.md) | F5 debug gamit ang Agent Inspector, patakbuhin ang smoke tests gamit ang resume + JD |
| 6 | [I-deploy sa Foundry](06-deploy-to-foundry.md) | Bumuo ng container, i-push sa ACR, irehistro ang hosted agent |
| 7 | [Beripikahin sa Playground](07-verify-in-playground.md) | Subukan ang na-deploy na ahente sa VS Code at Foundry Portal playgrounds |
| 8 | [Pag-troubleshoot](08-troubleshooting.md) | Ayusin ang karaniwang isyu sa multi-agent (MCP errors, pinutol na output, package versions) |
| 9 | [Buod at Susunod na Hakbang](09-summary.md) | Ano ang itinayo mo, mga pangunahing konseptong natutunan, paglilinis, at saan pupunta pagkatapos |

---

**Bumalik sa:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->