# Lab 02 - Multi-Agent Arbetsflöde: CV → Jobbmatchningsutvärderare

## Fullständig lärandebana

Denna dokumentation guidar dig igenom att bygga, testa och driftsätta ett **multi-agent arbetsflöde** som utvärderar matchning mellan CV och jobb med hjälp av fyra specialiserade agenter orkestrerade via **WorkflowBuilder**.

> **Förkunskapskrav:** Slutför [Lab 01 - Single Agent](../../lab01-single-agent/README.md) innan du påbörjar Lab 02.

---

## Moduler

| # | Modul | Vad du kommer göra |
|---|--------|-------------------|
| 0 | [Förkunskaper](00-prerequisites.md) | Verifiera slutförandet av Lab 01, förstå multi-agent koncept |
| 1 | [Förstå Multi-Agent Arkitektur](01-understand-multi-agent.md) | Lär dig WorkflowBuilder, agentroller, orkestreringsgraf |
| 2 | [Skaffa Grunden för Multi-Agent Projekt](02-scaffold-multi-agent.md) | Använd Foundry-tillägget för att skapa ett multi-agent arbetsflöde |
| 3 | [Konfigurera Agenter & Miljö](03-configure-agents.md) | Skriv instruktioner för 4 agenter, konfigurera MCP-verktyg, ställ in miljövariabler |
| 4 | [Orkestreringsmönster](04-orchestration-patterns.md) | Utforska parallell fan-out, sekventiell aggregering och alternativa mönster |
| 5 | [Testa Lokalt](05-test-locally.md) | F5-debugga med Agent Inspector, kör röktester med CV + JD |
| 6 | [Driftsätt till Foundry](06-deploy-to-foundry.md) | Bygg container, pusha till ACR, registrera hostad agent |
| 7 | [Verifiera i Playground](07-verify-in-playground.md) | Testa driftsatt agent i VS Code och Foundry Portals playgrounds |
| 8 | [Felsökning](08-troubleshooting.md) | Åtgärda vanliga multi-agent problem (MCP-fel, trunkerad output, paketversioner) |

---

## Uppskattad tid

| Erfarenhetsnivå | Tid |
|-----------------|------|
| Nyligen slutfört Lab 01 | 45-60 minuter |
| Viss erfarenhet av Azure AI | 60-90 minuter |
| Första gången med multi-agent | 90-120 minuter |

---

## Arkitektur i korthet

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

**Tillbaka till:** [Lab 02 README](../README.md) · [Workshop Hem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, vänligen notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för missförstånd eller feltolkningar som uppstår vid användning av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->