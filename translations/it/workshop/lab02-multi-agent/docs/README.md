# Laboratorio 02 - Flusso di Lavoro Multi-Agente: Valutatore di Adattamento Curriculum → Lavoro

## Percorso Completo di Apprendimento

Questa documentazione ti guida nella costruzione, nel test e nel deployment di un **flusso di lavoro multi-agente** che valuta l'adattamento tra curriculum e posizione lavorativa usando quattro agenti specializzati orchestrati tramite **WorkflowBuilder**.

> **Prerequisito:** Completa il [Laboratorio 01 - Agente Singolo](../../lab01-single-agent/README.md) prima di iniziare il Laboratorio 02.

---

## Moduli

| # | Modulo | Cosa farai |
|---|--------|------------|
| 0 | [Introduzione](00-prerequisites.md) | Cosa costruirai, verifica del Laboratorio 01, confronto Laboratorio 02 vs Laboratorio 01 |
| 1 | [Comprendere l'Architettura Multi-Agente](01-understand-multi-agent.md) | Impara WorkflowBuilder, i ruoli degli agenti, grafo di orchestrazione |
| 2 | [Prepara il Progetto Multi-Agente](02-scaffold-multi-agent.md) | Usa la procedura guidata dell'estensione Foundry per iniziare il progetto base |
| 3 | [Configura Agenti & Ambiente](03-configure-agents.md) | Scrivi le istruzioni per 4 agenti, configura lo strumento MCP, imposta le variabili d'ambiente |
| 4 | [Pattern di Orchestrazione](04-orchestration-patterns.md) | Catena sequenziale, relay di contenuti e OR-semantica di WorkflowBuilder |
| 5 | [Test Locale](05-test-locally.md) | Debug F5 con Agent Inspector, esegui test smoke con curriculum + JD |
| 6 | [Deploy su Foundry](06-deploy-to-foundry.md) | Costruisci il container, push su ACR, registra agente ospitato |
| 7 | [Verifica nel Playground](07-verify-in-playground.md) | Testa l'agente deployato in VS Code e nei playground del Foundry Portal |
| 8 | [Risoluzione Problemi](08-troubleshooting.md) | Risolvi problemi comuni multi-agente (errori MCP, output troncato, versioni pacchetto) |
| 9 | [Riepilogo & Passi Successivi](09-summary.md) | Cosa hai costruito, concetti chiave appresi, pulizia, e dove andare dopo |

---

**Torna a:** [Lab 02 README](../README.md) · [Home del Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->