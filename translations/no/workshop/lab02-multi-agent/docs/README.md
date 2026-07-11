# Lab 02 - Multi-Agent Workflow: CV → Jobbpassform Evaluator

## Fullt Læringsløp

Denne dokumentasjonen guider deg gjennom å bygge, teste og distribuere en **multi-agent arbeidsflyt** som vurderer CV-til-jobb passform ved bruk av fire spesialiserte agenter koordinert via **WorkflowBuilder**.

> **Forutsetning:** Fullfør [Lab 01 - Enkelt Agent](../../lab01-single-agent/README.md) før du starter Lab 02.

---

## Moduler

| # | Modul | Hva du vil gjøre |
|---|--------|-----------------|
| 0 | [Introduksjon](00-prerequisites.md) | Hva du vil bygge, Lab 01 verifisering, Lab 02 vs Lab 01 sammenligning |
| 1 | [Forstå Multi-Agent Arkitektur](01-understand-multi-agent.md) | Lær WorkflowBuilder, agentroller, orkestreringsgraf |
| 2 | [Still opp Multi-Agent Prosjektet](02-scaffold-multi-agent.md) | Bruk Foundry-utvidelsesveiviseren til å stille opp grunnprosjektet |
| 3 | [Konfigurer Agenter & Miljø](03-configure-agents.md) | Skriv instruksjoner for 4 agenter, konfigurer MCP-verktøy, sett miljøvariabler |
| 4 | [Orkestreringsmønstre](04-orchestration-patterns.md) | Sekvensiell kjede, innholdsoverføring, og WorkflowBuilder OR-semantikk |
| 5 | [Test Lokalt](05-test-locally.md) | F5 feilsøk med Agent Inspector, kjør røyktester med CV + stillingsbeskrivelse |
| 6 | [Distribuer til Foundry](06-deploy-to-foundry.md) | Bygg container, push til ACR, registrer vertet agent |
| 7 | [Verifiser i Playground](07-verify-in-playground.md) | Test distribuert agent i VS Code og Foundry Portal playgrounds |
| 8 | [Feilsøking](08-troubleshooting.md) | Fiks vanlige multi-agent problemer (MCP-feil, avkortet output, pakkeversjoner) |
| 9 | [Oppsummering & Neste Steg](09-summary.md) | Hva du bygde, viktige konsepter lært, opprydding og veien videre |

---

**Tilbake til:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->