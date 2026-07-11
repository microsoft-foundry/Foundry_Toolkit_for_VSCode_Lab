# Lab 02 - Multi-Agent Arbetsflöde: CV → Jobbmatchningsutvärderare

## Fullständig Lärandestig

Denna dokumentation guidar dig genom att bygga, testa och distribuera ett **multi-agent arbetsflöde** som utvärderar CV till jobb-matchning med fyra specialiserade agenter orkestrerade via **WorkflowBuilder**.

> **Förutsättning:** Slutför [Lab 01 - Enskild Agent](../../lab01-single-agent/README.md) innan du börjar med Lab 02.

---

## Moduler

| # | Modul | Vad du kommer göra |
|---|--------|---------------|
| 0 | [Introduktion](00-prerequisites.md) | Vad du bygger, verifiering av Lab 01, jämförelse Lab 02 vs Lab 01 |
| 1 | [Förstå Multi-Agent Arkitektur](01-understand-multi-agent.md) | Lära dig WorkflowBuilder, agentroller, orkestreringsgraf |
| 2 | [Skapa Multi-Agent Projekt](02-scaffold-multi-agent.md) | Använd Foundry extension wizard för att skapa basprojektet |
| 3 | [Konfigurera Agenter & Miljö](03-configure-agents.md) | Skriv instruktioner för 4 agenter, konfigurera MCP-verktyg, sätt miljövariabler |
| 4 | [Orkestreringsmönster](04-orchestration-patterns.md) | Sekventiell kedja, innehållsrelay, och WorkflowBuilder OR-semantik |
| 5 | [Testa Lokalt](05-test-locally.md) | F5-debugga med Agent Inspector, kör röktester med CV + JD |
| 6 | [Distribuera till Foundry](06-deploy-to-foundry.md) | Bygg container, pusha till ACR, registrera hostad agent |
| 7 | [Verifiera i Playground](07-verify-in-playground.md) | Testa distribuerad agent i VS Code och Foundry Portal playgrounds |
| 8 | [Felsökning](08-troubleshooting.md) | Åtgärda vanliga multi-agent problem (MCP-fel, avklippt utdata, paketversioner) |
| 9 | [Sammanfattning & Nästa Steg](09-summary.md) | Vad du byggt, viktiga koncept, uppstädning och vart du går härnäst |

---

**Tillbaka till:** [Lab 02 README](../README.md) · [Workshop Hem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->