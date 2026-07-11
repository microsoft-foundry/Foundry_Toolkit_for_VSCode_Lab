# Module 9 - Buod at Mga Susunod na Hakbang

⏱️ ~5 min

**Binabati kita!** Nakabuo, nasubukan, at (kung nasa Path A) na-deploy mo ang isang multi-agent workflow gamit ang Microsoft Foundry at ang Foundry Toolkit para sa VS Code.

---

## Ang Iyong Naitayo

Ang **Resume → Job Fit Evaluator** - isang multi-agent na naka-host na workflow na:
- Tumanggap ng resume + job description sa pamamagitan ng HTTP (`POST /responses`)
- Nagpapatakbo ng apat na specialized agents sa isang sequential pipeline - bawat agent ay nagpapasa ng data na kailangan ng kasunod nito
- Nagbabalik ng fit score (0–100 na may breakdown), listahan ng skill at certification gaps, at isang personalized learning roadmap na may mga tunay na link ng Microsoft Learn para sa bawat gap
- Tumatawag sa Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) upang kunin ang opisyal na mga learning resource para sa bawat natukoy na skill gap
- Tumatakbo bilang isang containerized na hosted agent sa Microsoft Foundry Agent Service

---

## Mga Pangunahing Konsepto na Natutunan

| Konsepto | Ano ang iyong na-praktis |
|---------|--------------------------|
| **Multi-agent orchestration** | `WorkflowBuilder` sequential pipeline gamit ang `add_edge()` |
| **Agent specialization** | Apat na nakatutok na agents ay mas mahusay kaysa sa isang general-purpose agent |
| **Content Router pattern** | Ang ResumeParser ay gumagana bilang router - pinapanatili nito ang text ng JD sa section na `[JOB DESCRIPTION PASS-THROUGH]` para ma-access ito ng downstream agents (kailangan dahil ang `context_mode="last_agent"` ay nangangahulugang tanging `start_executor` lang ang nakakakita ng raw user message) |
| **Content Relay pattern** | Ang JD Agent ay nagpasa ng `[PARSED RESUME PASS-THROUGH]` pasulong para makuha ng MatchingAgent ang parehong profile; iniiwasan ang OR-semantics double-trigger na sanhi ng fan-in graphs |
| **MCP tool integration** | `@tool` + `streamable_http_client` na tumatawag sa external MCP server |
| **Hosted Agent lifecycle** | Scaffold → I-configure → Subukan lokal → I-deploy → Siguraduhin sa cloud |
| **`context_mode="last_agent"`** | Bawat executor ay nakakakita lamang ng output ng direktang predecessor nito |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, one-click deploy |

---

## Mga Natapos Mo

<details open>
<summary><strong>🅰️ Path A - Foundry subscription</strong></summary>

- [x] Na-verify ang Lab 01 setup: project, model, at RBAC ay aktibo pa rin
- [x] Nakapag-scaffold ng multi-agent project gamit ang Workflows template
- [x] Nakasulat ng apat na agent instruction sets (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Na-integrate ang Microsoft Learn MCP tool gamit ang `streamable_http_client`
- [x] Na-wire ang workflow graph gamit ang `WorkflowBuilder` (sequential pipeline na may content relay)
- [x] Nasubukan lokal gamit ang 3 smoke tests (Agent Inspector) - fit score, gap cards, at MCP URLs
- [x] Na-deploy sa Foundry Agent Service (containerized, managed identity)
- [x] Na-verify sa cloud playground - structural consistency sa lokal na resulta

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local</strong></summary>

- [x] Na-verify ang Lab 01 setup: Foundry Local na tumatakbo gamit ang lokal na model
- [x] Nakapag-scaffold ng multi-agent project gamit ang Workflows template
- [x] Nakasulat ng apat na agent instruction sets at na-wire ang workflow graph
- [x] Na-integrate ang Microsoft Learn MCP tool
- [x] Nasubukan lokal gamit ang 3 smoke tests
- [x] Na-validate ang multi-agent behavior nang hindi kailangan ang cloud resources

</details>

---

## Mga Susunod na Hakbang

### Ipagsulong ang iyong pag-aaral

| Resource | Deskripsyon |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs para sa `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Ikonekta ang mga agents sa iba pang MCP servers (Bing, GitHub, custom) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Bigyan ng pundasyon ang mga agents gamit ang mga dokumento, vector stores, o Bing search |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Sukatin ang kalidad ng agent sa malaking sukat gamit ang automated evaluators |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Buong platform reference |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Mga tala sa pag-release at changelog ng extension |

### Mga Ideya upang palawakin ang workflow na ito

- **Magdagdag ng ika-5 na agent** - Isang interview coach na gumagawa ng mga posibleng interview questions base sa gap report
- **Magdagdag ng Bing grounding tool** - Hayaan ang JD Agent na maghanap ng mga katulad na job postings upang payamanin ang mga requirements
- **Ikonekta sa resume database** - Kunin ang mga profile ng kandidato mula sa database gamit ang custom na `@tool`
- **Subukan ang iba't ibang mga modelo** - Ihambing ang kalidad at latency ng output ng `gpt-4.1` vs. `gpt-4.1-mini`
- **Suriin gamit ang Foundry** - Gamitin ang Evaluations feature upang markahan ang fit reports laban sa isang golden dataset

### Para sa mga gumagamit ng Path B: Mag-upgrade sa cloud deployment

Kapag handa ka nang i-deploy sa cloud:
1. Kumuha ng Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Kumpletuhin ang [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (gumawa ng project, i-deploy ang model, magtakda ng RBAC)
3. I-update ang iyong `.env` gamit ang Foundry project endpoint at pangalan ng model deployment
4. Magpatuloy mula sa [Module 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Linisin ang mga resources (opsyonal)

Kung nais mong alisin ang mga Azure resources na ginawa sa panahon ng workshop na ito:

### Opsyon 1: I-delete ang resource group (tinanggal lahat)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opsyon 2: I-delete lang ang hosted agent

1. Buksan ang [ai.azure.com](https://ai.azure.com) → ang iyong project → **Build** → **Agents**.
2. Hanapin ang **PersonalCareerCopilot** → i-click ang **Delete**.

### Opsyon 3: I-delete ang model deployment

1. Sa Foundry sidebar, palawakin ang iyong project → **Models**.
2. I-right-click ang model deployment → **Delete**.

> **Tala sa gastos:** Ang mga hosted agents ay naniningil lamang kapag tumatakbo. Kung ititigil o ide-delete mo ang agent, wala nang patuloy na singil. Maaaring magkaroon ng maliit na singil ang model deployment para sa reserved capacity - i-delete ito kung tapos ka na.

---

**Nakaraan:** [08 - Troubleshooting](08-troubleshooting.md) · **Bahay:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->