# Module 7 - Samenvatting & Volgende Stappen

⏱️ ~5 min

**Gefeliciteerd!** Je hebt een gehoste AI-agent gebouwd, getest en (indien op Pad A) ingezet met Microsoft Foundry en de Foundry Toolkit voor VS Code.

---

## Wat je hebt gebouwd

Een **"Leg uit alsof ik een bestuurder ben"** agent die:
- Technische incidentrapporten of operationele updates ontvangt via HTTP (`POST /responses`)
- Deze vertaalt naar eenvoudige samenvattingen voor bestuurders
- Een gestructureerd uitvoerformaat volgt (Wat is er gebeurd / Zakelijke impact / Volgende stap)
- Off-topic verzoeken en pogingen tot prompt injectie weigert
- Draait als een container-gehoste agent in de Microsoft Foundry Agent Service

---

## Belangrijke concepten geleerd

| Concept | Wat je geoefend hebt |
|---------|-------------------|
| **Agent Framework architectuur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pijplijn |
| **Levenscyclus van gehoste agent** | Scaffold → Configureren → Lokaal testen → Deployen → Verifiëren in de cloud |
| **System prompt engineering** | Rol, doelgroep, uitvoerformaat, regels, veiligheidsbeperkingen en voorbeelden |
| **Verschillen lokaal vs. gehost** | Identiteit (persoonlijk referentie versus beheerde identiteit), eindpunt, netwerkpad |
| **Veiligheidsgrenzen** | Defensie tegen prompt injectie, rolintegriteit, correcte afhandeling van randgevallen |
| **Foundry Toolkit workflow** | Projectcreatie, modeldeploy, agent scaffolding, Agent Inspector, one-click deploy |

---

## Wat je voltooid hebt

### Pad A (Foundry abonnement)

- [x] Foundry Toolkit opgezet en een Foundry project gemaakt met een gedeployed model
- [x] Een gehoste agent gescaffold met automatisch gegenereerde projectstructuur
- [x] Gestructureerde agent instructies geschreven met veiligheidsregels
- [x] Lokaal getest met 3 functionele scenario's (Agent Inspector)
- [x] Gedeployed naar Foundry Agent Service (gecontaineriseerd)
- [x] Gecontroleerd in cloud playground met 4 randgeval-/veiligheidstests

### Pad B (Foundry Lokaal)

- [x] Foundry Toolkit opgezet met een lokaal model eindpunt
- [x] Gehoste agent project gescaffold
- [x] Gestructureerde agent instructies geschreven met veiligheidsregels
- [x] Lokaal getest met 3 functionele scenario's
- [x] Agentgedrag gevalideerd zonder cloud resources nodig te hebben

---

## Volgende stappen

### Blijf leren

| Bron | Beschrijving |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orkestratie](../../lab02-multi-agent/docs/README.md)** | Bouw een workflow met 4 agents (CV → Job Fit Evaluator) met orkestratiepatronen |
| **[Voeg tools toe aan je agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Verbind API's, databases of aangepaste functies via de Tool Catalog |
| **[Voeg kennis toe (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Grond je agent met documenten, vector stores of Bing-zoekopdrachten |
| **[Microsoft Foundry documentatie](https://learn.microsoft.com/azure/foundry/)** | Volledige platformreferentie |
| **[Agent Framework SDK referentie](https://learn.microsoft.com/agent-framework/)** | API-documentatie voor het `agent-framework` pakket |
| **[Foundry Toolkit - Wat is nieuw](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extensie release-opmerkingen en changelog |

### Ideeën om je agent uit te breiden

- **Voeg een datumtool toe** - Laat de agent "per vandaag" context in samenvattingen opnemen
- **Verbind met een incidentendatabase** - Haal echte incidentdetails op via een toolfunctie
- **Voeg een Bing-gronding tool toe** - Laat de agent recente nieuwsberichten opzoeken voor extra context
- **Probeer verschillende modellen** - Vergelijk outputkwaliteit van `gpt-4.1` vs. `gpt-4.1-mini`
- **Evalueer met Foundry** - Gebruik de Evaluaties-functie om agentkwaliteit op schaal te meten

### Voor Pad B gebruikers: upgrade naar cloud deployment

Wanneer je klaar bent om in de cloud te implementeren:
1. Verkrijg een Azure-abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Voltooi [Module 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (maak project, deploy model, wijs RBAC toe)
3. Werk je `.env` bij met het Foundry project-eindpunt en de model deployment naam
4. Ga verder vanaf [Module 05 - Deployen naar Foundry](05-deploy-to-foundry.md)

---

## Opruimen van resources (optioneel)

Als je de tijdens deze workshop aangemaakte Azure-resources wilt verwijderen:

### Optie 1: Verwijder de resourcegroep (verwijdert alles)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Optie 2: Verwijder alleen de gehoste agent

1. Open [ai.azure.com](https://ai.azure.com) → je project → **Build** → **Agents**.
2. Klik je agent aan → klik **Verwijderen**.

### Optie 3: Verwijder de model deployment

1. Vouw in de Foundry zijbalk je project uit → **Models**.
2. Rechtsklik de model deployment → **Verwijderen**.

> **Kostenopmerking:** Gehoste agents veroorzaken alleen kosten tijdens het draaien. Als je de agent stopt of verwijdert, zijn er geen doorlopende kosten. De model deployment kan een kleine vergoeding veroorzaken voor gereserveerde capaciteit - verwijder deze als je klaar bent.

---

**Vorige:** [06 - Verifiëren in Playground](06-verify-in-playground.md) · **Volgende:** [08 - Probleemoplossing (Referentie) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->