# Module 9 - Buod at Mga Susunod na Hakbang

⏱️ ~5 min

**Binabati kita!** Nakabuo, nasubukan, at (kung nasa Path A) na-deploy mo ang multi-agent workflow gamit ang Microsoft Foundry at ang Foundry Toolkit para sa VS Code.

---

## Ang iyong nabuo

Ang **Resume → Job Fit Evaluator** - isang multi-agent hosted workflow na:
- Tumanggap ng resume + job description sa pamamagitan ng HTTP (`POST /responses`)
- Nagpapatakbo ng apat na specialized agents sa isang sunud-sunod na pipeline - ang bawat agent ay nagpapasa ng data na kailangan ng sumunod na agent
- Nagbabalik ng fit score (0–100 na may breakdown), listahan ng skill at certification gap, at personalized learning roadmap na may tunay na Microsoft Learn links para sa bawat gap
- Tumatawag sa Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) upang kunin ang official learning resources para sa bawat natukoy na skill gap
- Tumatakbo bilang isang single containerized hosted agent sa Microsoft Foundry Agent Service

---

## Mga mahahalagang konseptong natutunan

| Konsepto | Ang iyong pinagpraktisan |
|---------|------------------------|
| **Multi-agent orchestration** | `WorkflowBuilder` sunud-sunod na pipeline gamit ang `add_edge()` |
| **Agent specialization** | Apat na pokus na ahente na mas magaling kaysa sa isang general-purpose na ahente |
| **Content Router pattern** | Gumagana bilang router ang ResumeParser - pinapanatili nito ang teksto ng JD sa isang `[JOB DESCRIPTION PASS-THROUGH]` na seksyon para ma-access ito ng mga downstream agents (kailangan ito dahil ang `context_mode="last_agent"` ay nangangahulugan na tanging ang `start_executor` lang ang nakikita ang raw user message) |
| **Content Relay pattern** | Pinapasa ng JD Agent ang `[PARSED RESUME PASS-THROUGH]` pasulong upang makuha ng MatchingAgent ang parehong profile; iniiwasan ang OR-semantics double-trigger na sanhi ng fan-in graphs |
| **MCP tool integration** | `@tool` + `streamable_http_client` na tumatawag sa external MCP server |
| **Hosted Agent lifecycle** | Scaffold → I-configure → Subukan nang lokal → I-deploy → I-verify sa cloud |
| **`context_mode="last_agent"`** | Nakikita ng bawat executor ang output lamang ng direktang nauna sa kanya |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, one-click deploy |

---

## Ang iyong natapos

<details open>
<summary><strong>🅰️ Path A - Foundry subscription</strong></summary>

- [x] Nakumpirma ang Lab 01 setup: proyekto, modelo, at RBAC ay aktibo pa rin
- [x] Naka-scaffold ng multi-agent na proyekto gamit ang Workflows template
- [x] Nakasulat ng apat na set ng instruksyon para sa mga ahente (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Na-integrate ang Microsoft Learn MCP tool gamit ang `streamable_http_client`
- [x] Na-wired ang workflow graph gamit ang `WorkflowBuilder` (sunud-sunod na pipeline na may content relay)
- [x] Nasubukan nang lokal gamit ang 2 smoke tests (Agent Inspector) - fit score, gap cards, at MCP URLs
- [x] Na-deploy sa Foundry Agent Service (containerized, managed identity)
- [x] Nakumpirma sa cloud playground - structural consistency sa lokal na resulta

</details>

<details open>
<summary><strong>🅱️ Path B - Foundry Local</strong></summary>

- [x] Nakumpirma ang Lab 01 setup: Foundry Local na tumatakbo gamit ang lokal na modelo
- [x] Naka-scaffold ng multi-agent na proyekto gamit ang Workflows template
- [x] Nakasulat ng apat na set ng instruksyon para sa mga ahente at na-wired ang workflow graph
- [x] Na-integrate ang Microsoft Learn MCP tool
- [x] Nasubukan nang lokal gamit ang 2 smoke tests
- [x] Napatunayan ang multi-agent na pagkilos nang hindi nangangailangan ng cloud resources

</details>

---

## Mga susunod na hakbang

### Ipagpatuloy ang pag-aaral

| Resource | Deskripsyon |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs para sa `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Ikonekta ang mga ahente sa ibang MCP servers (Bing, GitHub, custom) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Bigyang pundasyon ang mga ahente gamit ang mga dokumento, vector stores, o Bing search |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Sukatin ang kalidad ng ahente sa malaking saklaw gamit ang automated evaluators |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Buong platform reference |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Mga tala ng bersyon at changelog ng extension |

### Mga ideya para palawakin ang workflow na ito

- **Magdagdag ng ika-5 ahente** - Isang interview coach na gumagawa ng mga posibleng tanong sa interbyu base sa gap report
- **Magdagdag ng Bing grounding tool** - Hayaan ang JD Agent na maghanap ng mga katulad na job postings upang mapayaman ang mga requirements
- **Ikonekta sa isang resume database** - Kunin ang mga profile ng kandidato mula sa database gamit ang custom na `@tool`
- **Subukan ang iba't ibang mga modelo** - Ihambing ang kalidad at latency ng output ng `gpt-4.1` laban sa `gpt-4.1-mini`
- **Suriin gamit ang Foundry** - Gamitin ang Evaluations feature upang bigyan ng score ang mga fit reports laban sa golden dataset

### Para sa mga gumagamit ng Path B: Mag-upgrade sa deployment sa cloud

Kapag handa ka nang mag-deploy sa cloud:
1. Kumuha ng Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Kumpletuhin ang [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (gumawa ng proyekto, i-deploy ang modelo, magtalaga ng RBAC)
3. I-update ang iyong `.env` gamit ang Foundry project endpoint at pangalan ng model deployment
4. Magpatuloy mula sa [Module 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Linisin ang mga resources (opsyonal)

Kung nais mong alisin ang mga Azure resources na nilikha sa workshop na ito:

### Opsyon 1: I-delete ang resource group (tatanggal lahat)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opsyon 2: I-delete lamang ang hosted agent

1. Buksan ang [ai.azure.com](https://ai.azure.com) → iyong proyekto → **Build** → **Agents**.
2. Hanapin ang **PersonalCareerCopilot** → i-click ang **Delete**.

### Opsyon 3: I-delete ang model deployment

1. Sa Foundry sidebar, i-expand ang iyong proyekto → **Models**.
2. Right-click ang model deployment → **Delete**.

> **Tala sa gastos:** Ang mga hosted agents ay naniningil lamang kapag tumatakbo. Kung hihinto o ide-delete mo ang agent, wala nang patuloy na singil. Maaaring magkaroon ng maliit na singil para sa reserved capacity ang model deployment - i-delete ito kung tapos ka na.

---

**Nakaraan:** [08 - Troubleshooting](08-troubleshooting.md) · **Bahay:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->