# Lab 02 - Multi-Agent Workflow: CV → Job Fit Evaluator

## Volledig Leerpad

Deze documentatie leidt je door het bouwen, testen en implementeren van een **multi-agent workflow** die de match tussen CV en baan beoordeelt met behulp van vier gespecialiseerde agenten die worden georkestreerd via **WorkflowBuilder**.

> **Vereiste:** Voltooi [Lab 01 - Enkele Agent](../../lab01-single-agent/README.md) voordat je begint met Lab 02.

---

## Modules

| # | Module | Wat je gaat doen |
|---|--------|------------------|
| 0 | [Introductie](00-prerequisites.md) | Wat je gaat bouwen, Lab 01 verificatie, Lab 02 vs Lab 01 vergelijking |
| 1 | [Begrijp Multi-Agent Architectuur](01-understand-multi-agent.md) | Leer WorkflowBuilder kennen, agentrollen, orkestratiegrafiek |
| 2 | [Scaffold het Multi-Agent Project](02-scaffold-multi-agent.md) | Gebruik de Foundry extensie wizard om het basisproject op te zetten |
| 3 | [Configureer Agenten & Omgeving](03-configure-agents.md) | Schrijf instructies voor 4 agenten, configureer MCP-tool, stel omgevingsvariabelen in |
| 4 | [Orkestratiepatronen](04-orchestration-patterns.md) | Sequentiële keten, inhoudsrelay, en WorkflowBuilder OR-semantiek |
| 5 | [Test Lokaal](05-test-locally.md) | F5 debuggen met Agent Inspector, voer smoketests uit met CV + JD |
| 6 | [Implementeer naar Foundry](06-deploy-to-foundry.md) | Container bouwen, push naar ACR, registreer gehoste agent |
| 7 | [Verifieer in Playground](07-verify-in-playground.md) | Test geïmplementeerde agent in VS Code en Foundry Portal playgrounds |
| 8 | [Probleemoplossing](08-troubleshooting.md) | Los veelvoorkomende multi-agent problemen op (MCP-fouten, afgekapt resultaat, pakketversies) |
| 9 | [Samenvatting & Volgende Stappen](09-summary.md) | Wat je hebt gebouwd, belangrijke concepten geleerd, opruimen, en waar je hierna heen gaat |

---

**Terug naar:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->