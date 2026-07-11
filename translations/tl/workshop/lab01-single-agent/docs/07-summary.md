# Module 7 - Buod at Mga Susunod na Hakbang

⏱️ ~5 min

**Pananglitan!** Nakabuo, nakapagsuri, at (kung nasa Path A) nakapag-deploy ka ng isang hosted AI agent gamit ang Microsoft Foundry at Foundry Toolkit para sa VS Code.

---

## Ang Iyong Nabuo

Isang **"Ipaliwanag Para Parang Executive"** agent na:
- Tumanggap ng mga teknikal na ulat ng insidente o mga operational update sa pamamagitan ng HTTP (`POST /responses`)
- Isinalin ito sa simpleng buod na naiintindihan ng executive
- Sumusunod sa isang estrukturadong output format (Ano ang nangyari / Epekto sa negosyo / Susunod na hakbang)
- Tumangging iproseso ang mga request na wala sa paksa at pagtatangka ng prompt injection
- Tumatakbo bilang containerized hosted agent sa Microsoft Foundry Agent Service

---

## Mga Pangunahing Konsepto na Natutunan

| Konsepto | Iyong Pinraktisan |
|---------|-------------------|
| **Arkitektura ng Agent Framework** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Lifecycle ng Hosted Agent** | Scaffold → I-configure → Subukan nang lokal → I-deploy → I-verify sa cloud |
| **System prompt engineering** | Papel, tagapakinig, format ng output, mga patakaran, mga safety constraints, at mga halimbawa |
| **Mga pagkakaiba ng local vs. hosted** | Identidad (personal na kredensyal vs. managed identity), endpoint, network path |
| **Mga hangganan ng kaligtasan** | Depensa laban sa prompt injection, pagsunod sa papel, magalang na paghawak ng mga edge case |
| **Workflow ng Foundry Toolkit** | Paglikha ng proyekto, deployment ng modelo, scaffolding ng agent, Agent Inspector, one-click deploy |

---

## Mga Natapos Mo

### Path A (Foundry subscription)

- [x] Na-set up ang Foundry Toolkit at nakagawa ng Foundry project na may deployed model
- [x] Na-scaffold ang isang hosted agent na may auto-generated na istruktura ng proyekto
- [x] Nagsulat ng estrukturadong mga tagubilin para sa agent na may mga patakaran sa kaligtasan
- [x] Nasubukan nang lokal gamit ang 3 functional na scenario (Agent Inspector)
- [x] Nai-deploy sa Foundry Agent Service (containerized)
- [x] Na-verify sa cloud playground gamit ang 4 edge-case/safety tests

### Path B (Foundry Local)

- [x] Na-set up ang Foundry Toolkit na may local na model endpoint
- [x] Na-scaffold ang proyekto ng hosted agent
- [x] Nagsulat ng estrukturadong mga tagubilin para sa agent na may mga patakaran sa kaligtasan
- [x] Nasubukan nang lokal gamit ang 3 functional na scenario
- [x] Na-validate ang pag-uugali ng agent nang hindi kailangan ang mga cloud resources

---

## Mga Susunod na Hakbang

### Ipagpatuloy ang Pag-aaral

| Resource | Paglalarawan |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Bumuo ng 4-agent na workflow (Resume → Job Fit Evaluator) gamit ang mga orchestration pattern |
| **[Magdagdag ng mga tool sa iyong agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Ikonekta ang mga API, database, o custom na function gamit ang Tool Catalog |
| **[Magdagdag ng kaalaman (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Bigyang-lakas ang iyong agent gamit ang mga dokumento, vector stores, o Bing search |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Buong sanggunian ng platform |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | Mga dokumento ng API para sa `agent-framework` package |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Mga tala ng release at changelog ng extension |

### Mga Ideya para Palawakin ang Iyong Agent

- **Magdagdag ng date tool** - Hayaan ang agent na isama ang kontekstong "as of today" sa mga buod
- **Kumonekta sa isang incident database** - Kunin ang totoong detalye ng insidente gamit ang isang tool function
- **Magdagdag ng Bing grounding tool** - Pahintulutan ang agent na maghanap ng mga kamakailang balita para sa karagdagang konteksto
- **Subukan ang iba't ibang mga modelo** - Ihambing ang kalidad ng output ng `gpt-4.1` vs. `gpt-4.1-mini`
- **Suriin gamit ang Foundry** - Gamitin ang Evaluations feature para sukatin ang kalidad ng agent sa malawakang lawak

### Para sa mga gumagamit ng Path B: Mag-upgrade sa cloud deployment

Kapag handa ka nang mag-deploy sa cloud:
1. Kumuha ng Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Tapusin ang [Module 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (gumawa ng proyekto, mag-deploy ng modelo, mag-assign ng RBAC)
3. I-update ang iyong `.env` gamit ang Foundry project endpoint at pangalan ng model deployment
4. Magpatuloy mula sa [Module 05 - Deploy to Foundry](05-deploy-to-foundry.md)

---

## Linisin ang mga Resources (opsyonal)

Kung nais mong tanggalin ang mga Azure resources na nalikha sa panahon ng workshop na ito:

### Opsyon 1: I-delete ang resource group (tinanggal lahat)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opsyon 2: I-delete lang ang hosted agent

1. Buksan ang [ai.azure.com](https://ai.azure.com) → iyong proyekto → **Build** → **Agents**.
2. I-click ang iyong agent → i-click ang **Delete**.

### Opsyon 3: I-delete ang model deployment

1. Sa Foundry sidebar, palawakin ang iyong proyekto → **Models**.
2. I-right click ang model deployment → **Delete**.

> **Tala tungkol sa gastos:** Ang mga hosted agent ay may singil lamang kapag tumatakbo. Kung hihinto o tatanggalin mo ang agent, wala nang tuloy-tuloy na singil. Maaaring may maliit na singil ang model deployment para sa reserved capacity - tanggalin ito kapag tapos ka na.

---

**Nuna:** [06 - Verify in Playground](06-verify-in-playground.md) · **Susunod:** [08 - Troubleshooting (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->