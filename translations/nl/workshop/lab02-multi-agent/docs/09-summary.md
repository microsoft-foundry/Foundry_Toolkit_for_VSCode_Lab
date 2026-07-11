# Module 9 - Samenvatting & Volgende Stappen

⏱️ ~5 min

**Gefeliciteerd!** Je hebt een multi-agent workflow gebouwd, getest en (indien op Pad A) ingezet met Microsoft Foundry en de Foundry Toolkit voor VS Code.

---

## Wat je hebt gebouwd

De **Resume → Job Fit Evaluator** - een multi-agent gehoste workflow die:
- Een cv + functiebeschrijving ontvangt via HTTP (`POST /responses`)
- Vier gespecialiseerde agents uitvoert in een sequentiële pijplijn - elke agent geeft de gegevens door die de opvolger nodig heeft
- Een fit score teruggeeft (0–100 met een uitsplitsing), een lijst met vaardigheids- en certificeringslacunes, en een gepersonaliseerd leertraject met echte Microsoft Learn-links voor elke lacune
- De Microsoft Learn MCP-server aanroept (`https://learn.microsoft.com/api/mcp`) om officiële leerbronnen op te halen voor elke geïdentificeerde vaardigheidslacune
- Draait als een enkele containerized gehoste agent in Microsoft Foundry Agent Service

---

## Belangrijke concepten geleerd

| Concept | Wat je geoefend hebt |
|---------|-------------------|
| **Multi-agent orkestratie** | `WorkflowBuilder` sequentiële pijplijn met `add_edge()` |
| **Agent specialisatie** | Vier gerichte agents presteren beter dan één algemene agent |
| **Content Router patroon** | ResumeParser fungeert ook als router - het behoudt de functiebeschrijvingtekst in een `[JOB DESCRIPTION PASS-THROUGH]` sectie zodat downstream agents er toegang toe hebben (vereist omdat `context_mode="last_agent"` betekent dat alleen de `start_executor` het ruwe gebruikersbericht ziet) |
| **Content Relay patroon** | JD Agent geeft `[PARSED RESUME PASS-THROUGH]` door zodat MatchingAgent beide profielen krijgt; voorkomt de OR-semantiek dubbele trigger die fan-in grafieken veroorzaken |
| **MCP tool integratie** | `@tool` + `streamable_http_client` die een externe MCP-server aanroept |
| **Hosted Agent lifecycle** | Scaffold → Configureren → Lokaal testen → Deployen → Verifiëren in de cloud |
| **`context_mode="last_agent"`** | Elke executor ziet alleen de output van zijn directe voorganger |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, één-klik deployment |

---

## Wat je hebt voltooid

<details open>
<summary><strong>🅰️ Pad A - Foundry abonnement</strong></summary>

- [x] Lab 01 setup geverifieerd: project, model en RBAC nog actief
- [x] Een multi-agent project gescaffold met de Workflows template
- [x] Vier agent instructiesets geschreven (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] De Microsoft Learn MCP tool geïntegreerd met `streamable_http_client`
- [x] De workflow grafiek verbonden met `WorkflowBuilder` (sequentiële pijplijn met content relay)
- [x] Lokaal getest met 3 smoke tests (Agent Inspector) - fit score, gap kaarten, en MCP URLs
- [x] Geplaatst naar Foundry Agent Service (gecontaineriseerd, managed identity)
- [x] Gecontroleerd in cloud playground - structurele consistentie met lokale resultaten

</details>

<details open>
<summary><strong>🅱️ Pad B - Foundry Local</strong></summary>

- [x] Lab 01 setup geverifieerd: Foundry Local draait met een lokaal model
- [x] Een multi-agent project gescaffold met de Workflows template
- [x] Vier agent instructiesets geschreven en de workflow grafiek verbonden
- [x] De Microsoft Learn MCP tool geïntegreerd
- [x] Lokaal getest met 3 smoke tests
- [x] Multi-agent gedrag gevalideerd zonder cloud resources

</details>

---

## Volgende stappen

### Blijf leren

| Bron | Beschrijving |
|----------|-------------|
| **[Agent Framework SDK referentie](https://learn.microsoft.com/agent-framework/)** | API documentatie voor `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalogus](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Verbind agents met andere MCP servers (Bing, GitHub, maatwerk) |
| **[Kennis toevoegen (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Veranker agents met documenten, vector stores of Bing zoekopdrachten |
| **[Foundry Evaluaties](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Meet agent kwaliteit op schaal met geautomatiseerde evaluators |
| **[Microsoft Foundry documentatie](https://learn.microsoft.com/azure/foundry/)** | Volledige platformreferentie |
| **[Foundry Toolkit - Wat is nieuw](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extensie release notes en changelog |

### Ideeën om deze workflow uit te breiden

- **Voeg een 5e agent toe** - Een interview coach die waarschijnlijke interviewvragen genereert op basis van het gap rapport
- **Voeg een Bing verankerings-tool toe** - Laat de JD Agent zoeken naar vergelijkbare vacatures om de eisen te verrijken
- **Verbind met een cv database** - Haal kandidatenprofielen op uit een database via een maatwerk `@tool`
- **Probeer verschillende modellen** - Vergelijk `gpt-4.1` vs. `gpt-4.1-mini` output kwaliteit en latentie
- **Evalueer met Foundry** - Gebruik de Evaluations functie om fit rapporten te scoren tegen een gouden dataset

### Voor Pad B gebruikers: Upgrade naar clouddeployment

Wanneer je klaar bent om naar de cloud te deployen:
1. Neem een Azure abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Voltooi [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (maak project aan, deploy model, wijs RBAC toe)
3. Werk je `.env` bij met het Foundry project endpoint en model deployment naam
4. Ga verder vanaf [Module 06 - Deploy naar Foundry](06-deploy-to-foundry.md)

---

## Opruimen van resources (optioneel)

Als je de Azure resources die tijdens deze workshop zijn gecreëerd wilt verwijderen:

### Optie 1: Verwijder de resourcegroep (verwijdert alles)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Optie 2: Verwijder alleen de gehoste agent

1. Open [ai.azure.com](https://ai.azure.com) → jouw project → **Build** → **Agents**.
2. Zoek **PersonalCareerCopilot** → klik op **Delete**.

### Optie 3: Verwijder de model deployment

1. Vouw in de Foundry sidebar je project uit → **Models**.
2. Rechtsklik de model deployment → **Delete**.

> **Kostennota:** Gehoste agents brengen alleen kosten met zich mee tijdens het draaien. Als je de agent stopt of verwijdert, zijn er geen doorlopende kosten. De model deployment kan een kleine vergoeding voor gereserveerde capaciteit veroorzaken - verwijder deze als je klaar bent.

---

**Vorige:** [08 - Troubleshooting](08-troubleshooting.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->