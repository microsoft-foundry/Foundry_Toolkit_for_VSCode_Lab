# Lab 02 - Multi-Agent Workflow: Resume → Job Fit Evaluator

## Fuld Læringssti

Denne dokumentation guider dig gennem opbygning, test og implementering af en **multi-agent workflow**, der vurderer hvor godt et CV passer til et job ved hjælp af fire specialiserede agenter orkestreret via **WorkflowBuilder**.

> **Forudsætning:** Fuldfør [Lab 01 - Single Agent](../../lab01-single-agent/README.md) inden du starter Lab 02.

---

## Moduler

| # | Modul | Hvad du skal gøre |
|---|--------|-------------------|
| 0 | [Forudsætninger](00-prerequisites.md) | Verificer færdiggørelse af Lab 01, forstå multi-agent koncepter |
| 1 | [Forstå Multi-Agent Arkitektur](01-understand-multi-agent.md) | Lær WorkflowBuilder, agentroller, orkestreringsgraf |
| 2 | [Opsæt Multi-Agent Projekt](02-scaffold-multi-agent.md) | Brug Foundry-udvidelsen til at opsætte en multi-agent workflow |
| 3 | [Konfigurer Agenter & Miljø](03-configure-agents.md) | Skriv instruktioner til 4 agenter, konfigurer MCP værktøj, sæt miljøvariabler |
| 4 | [Orkestreringsmønstre](04-orchestration-patterns.md) | Udforsk parallel fan-out, sekventiel aggregering og alternative mønstre |
| 5 | [Test Lokalt](05-test-locally.md) | F5 fejlret med Agent Inspector, kør rygetests med CV + jobbeskrivelse |
| 6 | [Deploy til Foundry](06-deploy-to-foundry.md) | Byg container, push til ACR, registrer hostet agent |
| 7 | [Verificer i Playground](07-verify-in-playground.md) | Test implementeret agent i VS Code og Foundry Portal playgrounds |
| 8 | [Fejlfinding](08-troubleshooting.md) | Løs almindelige multi-agent problemer (MCP-fejl, afkortet output, pakkeversioner) |

---

## Anslået tid

| Erfaring | Tid |
|-----------|-----|
| Har for nyligt gennemført Lab 01 | 45-60 minutter |
| Nogen erfaring med Azure AI | 60-90 minutter |
| Første gang med multi-agent | 90-120 minutter |

---

## Arkitektur ved et øjekast

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

**Tilbage til:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det oprindelige dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->