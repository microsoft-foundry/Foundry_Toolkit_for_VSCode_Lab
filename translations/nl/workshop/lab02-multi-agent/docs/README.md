# Lab 02 - Multi-Agent Workflow: Cv → Functiegeschiktheid Evaluator

## Volledige Leertraject

Deze documentatie begeleidt je bij het bouwen, testen en implementeren van een **multi-agent workflow** die de geschiktheid van een cv voor een functie evalueert met behulp van vier gespecialiseerde agenten die worden gecoördineerd via **WorkflowBuilder**.

> **Vereiste:** Voltooi [Lab 01 - Enkele Agent](../../lab01-single-agent/README.md) voordat je begint met Lab 02.

---

## Modules

| # | Module | Wat je gaat doen |
|---|--------|------------------|
| 0 | [Vereisten](00-prerequisites.md) | Controleer voltooiing Lab 01, begrijp multi-agent concepten |
| 1 | [Begrijp Multi-Agent Architectuur](01-understand-multi-agent.md) | Leer WorkflowBuilder, agentrollen, orkestratiegrafiek |
| 2 | [Scaffold het Multi-Agent Project](02-scaffold-multi-agent.md) | Gebruik de Foundry extensie om een multi-agent workflow op te zetten |
| 3 | [Configureer Agenten & Omgeving](03-configure-agents.md) | Schrijf instructies voor 4 agenten, configureer MCP-tool, stel omgevingsvariabelen in |
| 4 | [Orkestratiepatronen](04-orchestration-patterns.md) | Verken parallelle fan-out, sequentiële aggregatie en alternatieve patronen |
| 5 | [Test Lokaal](05-test-locally.md) | F5 debug met Agent Inspector, voer smoke tests uit met cv + functiebeschrijving |
| 6 | [Implementeer naar Foundry](06-deploy-to-foundry.md) | Bouw container, push naar ACR, registreer gehoste agent |
| 7 | [Verifieer in Playground](07-verify-in-playground.md) | Test geïmplementeerde agent in VS Code en Foundry Portal playgrounds |
| 8 | [Probleemoplossing](08-troubleshooting.md) | Los veelvoorkomende multi-agent problemen op (MCP-fouten, afgebroken output, pakketversies) |

---

## Geschatte tijd

| Ervaringsniveau | Tijd |
|-----------------|------|
| Onlangs Lab 01 voltooid | 45-60 minuten |
| Enige Azure AI ervaring | 60-90 minuten |
| Eerste keer met multi-agent | 90-120 minuten |

---

## Architectuur in één oogopslag

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

**Terug naar:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat automatische vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet als de gezaghebbende bron worden beschouwd. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor enige misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->