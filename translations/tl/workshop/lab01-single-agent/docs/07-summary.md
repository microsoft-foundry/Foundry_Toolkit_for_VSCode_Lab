# Module 7 - Buod at Susunod na Mga Hakbang

⏱️ ~5 minuto

**Pagbati!** Nakabuo ka, nakapagsuri, at (kung nasa Path A) nakapag-deploy ng isang hosted AI agent gamit ang Microsoft Foundry at ang Foundry Toolkit para sa VS Code.

---

## Ano ang iyong nabuo

Isang **"Ipaliwanag Para Akong Isang Ehekutibo"** agent na:
- Tumanggap ng mga teknikal na ulat ng insidente o mga operational update sa pamamagitan ng HTTP (`POST /responses`)
- Isinasaalang-alang ang mga ito sa plain-language na mga executive summary
- Sumusunod sa isang istrakturadong output format (Ano ang nangyari / Epekto sa negosyo / Susunod na hakbang)
- Tinatanggihan ang mga off-topic na kahilingan at mga pagtatangka ng prompt injection
- Tumatakbo bilang containerized hosted agent sa Microsoft Foundry Agent Service

---

## Mga Mahahalagang Konsepto na Natutunan

| Konsepto | Iyong Pinagsanayan |
|---------|-------------------|
| **Arkitektura ng Agent Framework** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Lifecycle ng Hosted Agent** | Scaffold → I-configure → Mag-test locally → Mag-deploy → Beripikahin sa cloud |
| **System prompt engineering** | Role, audience, output format, mga patakaran, mga safety constraint, at mga halimbawa |
| **Mga pagkakaiba ng local kumpara sa hosted** | Identidad (personal na kredensyal kumpara sa managed identity), endpoint, network path |
| **Mga safety boundary** | Depensa sa prompt injection, pagsunod sa role, maayos na paghawak ng mga edge case |
| **Foundry Toolkit workflow** | Paggawa ng proyekto, pag-deploy ng modelo, pag-scaffold ng agent, Agent Inspector, one-click deploy |

---

## Ano ang iyong natapos

### Path A (Foundry subscription)

- [x] Nai-set up ang Foundry Toolkit at nakagawa ng Foundry project na may deployed model
- [x] Na-scaffold ang hosted agent na may auto-generated na istraktura ng proyekto
- [x] Nakasulat ng istrakturadong mga tagubilin para sa agent na may mga patakarang panseguridad
- [x] Nasubukan locally gamit ang 3 functional na scenario (Agent Inspector)
- [x] Na-deploy sa Foundry Agent Service (containerized)
- [x] Na-beripika sa cloud playground gamit ang 4 na edge-case at safety tests

### Path B (Foundry Local)

- [x] Nai-set up ang Foundry Toolkit na may local model endpoint
- [x] Na-scaffold ang hosted agent project
- [x] Nakasulat ng istrakturadong mga tagubilin para sa agent na may mga patakarang panseguridad
- [x] Nasubukan locally gamit ang 3 functional na scenario
- [x] Na-validate ang ugali ng agent nang hindi nangangailangan ng cloud resources

---

## Susunod na mga hakbang

### Magpatuloy sa pag-aaral

| Resource | Deskripsyon |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Gumawa ng 4-agent workflow (Resume → Job Fit Evaluator) gamit ang orchestration patterns |
| **[Magdagdag ng mga tool sa iyong agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Ikonekta ang mga API, database, o custom na function sa pamamagitan ng Tool Catalog |
| **[Magdagdag ng kaalaman (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Pag-ugatan ang iyong agent gamit ang mga dokumento, vector stores, o Bing search |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Kumpletong platform reference |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API docs para sa `agent-framework` package |
| **[Foundry Toolkit - Ano ang Bago](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Mga tala ng release ng extension at changelog |

### Mga ideya para palawakin ang iyong agent

- **Magdagdag ng date tool** - Payagan ang agent na isama ang "as of today" na konteksto sa mga summary
- **Ikonekta sa isang incident database** - Kunin ang totoong detalye ng insidente gamit ang tool na function
- **Magdagdag ng Bing grounding tool** - Payagan ang agent na maghanap ng mga kamakailang balita para sa karagdagang konteksto
- **Subukan ang iba't ibang modelo** - Ihambing ang kalidad ng output ng `gpt-4.1` kumpara sa `gpt-4.1-mini`
- **Suriin gamit ang Foundry** - Gamitin ang Evaluations feature upang masukat ang kalidad ng agent sa malawakang paraan

### Para sa mga gumagamit ng Path B: I-upgrade sa cloud deployment

Kapag handa ka nang mag-deploy sa cloud:
1. Kumuha ng Azure subscription ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Kumpletuhin ang [Module 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (gumawa ng proyekto, mag-deploy ng modelo, magtalaga ng RBAC)
3. I-update ang iyong `.env` gamit ang Foundry project endpoint at pangalan ng model deployment
4. Magpatuloy mula sa [Module 05 - Deploy to Foundry](05-deploy-to-foundry.md)

---

## Linisin ang mga resources (opsyonal)

Kung nais mong alisin ang mga Azure resources na nilikha sa panahon ng workshop na ito:

### Opsyon 1: Burahin ang resource group (aalis ng lahat)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opsyon 2: Burahin lang ang hosted agent

1. Buksan ang [ai.azure.com](https://ai.azure.com) → ang iyong proyekto → **Build** → **Agents**.
2. I-click ang iyong agent → i-click ang **Delete**.

### Opsyon 3: Burahin ang model deployment

1. Sa Foundry sidebar, i-expand ang iyong proyekto → **Models**.
2. I-right-click ang model deployment → **Delete**.

> **Tala sa gastos:** Nagkakaroon ng gastos ang hosted agents kapag tumatakbo lamang. Kung ihihinto o buburahin mo ang agent, walang tuloy-tuloy na singil. Maaaring magkaroon ng maliit na singil sa model deployment para sa reserved capacity - burahin ito kung tapos ka na.

---

**Nakaraan:** [06 - Verify in Playground](06-verify-in-playground.md) · **Susunod:** [08 - Troubleshooting (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->