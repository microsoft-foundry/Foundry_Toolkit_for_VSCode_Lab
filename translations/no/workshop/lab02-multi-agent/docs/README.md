# Lab 02 - Multi-Agent Arbeidsflyt: CV → Jobbtilpasning Evaluator

## Fullt Læringsløp

Denne dokumentasjonen guider deg gjennom å bygge, teste og distribuere en **multi-agent arbeidsflyt** som vurderer CV-til-jobb tilpasning ved bruk av fire spesialiserte agenter orkestrert via **WorkflowBuilder**.

> **Forutsetning:** Fullfør [Lab 01 - Enkel Agent](../../lab01-single-agent/README.md) før du starter Lab 02.

---

## Moduler

| # | Modul | Hva du skal gjøre |
|---|--------|------------------|
| 0 | [Forutsetninger](00-prerequisites.md) | Verifisere fullføring av Lab 01, forstå multi-agent konsepter |
| 1 | [Forstå Multi-Agent Arkitektur](01-understand-multi-agent.md) | Lære WorkflowBuilder, agentroller, orkestreringsgraf |
| 2 | [Bygg opp Multi-Agent Prosjektet](02-scaffold-multi-agent.md) | Bruke Foundry-utvidelsen til å bygge opp en multi-agent arbeidsflyt |
| 3 | [Konfigurer Agenter & Miljø](03-configure-agents.md) | Skriv instruksjoner for 4 agenter, konfigurer MCP-verktøy, sett miljøvariabler |
| 4 | [Orkestreringsmønstre](04-orchestration-patterns.md) | Utforsk parallell forgrening, sekvensiell aggregering og alternative mønstre |
| 5 | [Test Lokalt](05-test-locally.md) | F5 debug med Agent Inspector, kjør røyktester med CV + stillingsbeskrivelse |
| 6 | [Distribuer til Foundry](06-deploy-to-foundry.md) | Bygg container, push til ACR, registrer hostet agent |
| 7 | [Verifiser i Playground](07-verify-in-playground.md) | Test distribuert agent i VS Code og Foundry Portal playgrounds |
| 8 | [Feilsøking](08-troubleshooting.md) | Løs vanlige multi-agent problemer (MCP feil, trunkert output, pakkversjoner) |

---

## Estimert tid

| Erfaring | Tid |
|-----------------|------|
| Fullførte Lab 01 nylig | 45-60 minutter |
| Litt erfaring med Azure AI | 60-90 minutter |
| Første gang med multi-agent | 90-120 minutter |

---

## Arkitektur ved første øyekast

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

**Tilbake til:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vennligst vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på det opprinnelige språket skal anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->