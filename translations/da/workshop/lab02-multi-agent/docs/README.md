# Lab 02 - Multi-Agent Workflow: CV → Job Match Evaluator

## Fuld Læringssti

Denne dokumentation guider dig gennem opbygning, test og implementering af en **multi-agent workflow**, der evaluerer CV-til-job match ved hjælp af fire specialiserede agenter orkestreret via **WorkflowBuilder**.

> **Forudsætning:** Fuldfør [Lab 01 - Single Agent](../../lab01-single-agent/README.md) før du starter Lab 02.

---

## Moduler

| # | Modul | Hvad du vil gøre |
|---|--------|---------------|
| 0 | [Introduktion](00-prerequisites.md) | Hvad du bygger, verifikation af Lab 01, sammenligning mellem Lab 02 og Lab 01 |
| 1 | [Forstå Multi-Agent Arkitektur](01-understand-multi-agent.md) | Lær WorkflowBuilder, agentroller, orkestreringsgraf |
| 2 | [Opsæt Multi-Agent Projekt](02-scaffold-multi-agent.md) | Brug Foundry extension wizard til at opsætte basisprojektet |
| 3 | [Konfigurer Agenter & Miljø](03-configure-agents.md) | Skriv instruktioner til 4 agenter, konfigurer MCP-værktøj, sæt miljøvariabler |
| 4 | [Orkestreringsmønstre](04-orchestration-patterns.md) | Sekventiel kæde, indholdsrelay og WorkflowBuilder OR-semantik |
| 5 | [Test Lokalt](05-test-locally.md) | F5 debugging med Agent Inspector, kør smoke tests med CV + jobbeskrivelse |
| 6 | [Deploy til Foundry](06-deploy-to-foundry.md) | Byg container, push til ACR, registrer hosted agent |
| 7 | [Verificer i Playground](07-verify-in-playground.md) | Test deployet agent i VS Code og Foundry Portal playgrounds |
| 8 | [Fejlfinding](08-troubleshooting.md) | Løs almindelige multi-agent problemer (MCP fejl, forkortet output, pakkerversioner) |
| 9 | [Opsummering & Næste Skridt](09-summary.md) | Hvad du byggede, nøglebegreber lært, oprydning og hvor du går hen næste gang |

---

**Tilbage til:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->