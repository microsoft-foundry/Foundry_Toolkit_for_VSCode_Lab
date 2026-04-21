# Lab 02 - Flusso di Lavoro Multi-Agente: Valutatore di Corrispondenza Curriculum → Lavoro

## Percorso di Apprendimento Completo

Questa documentazione ti guida nella creazione, nel test e nel deployment di un **flusso di lavoro multi-agente** che valuta la corrispondenza tra curriculum e lavoro usando quattro agenti specializzati orchestrati tramite **WorkflowBuilder**.

> **Prerequisito:** Completa [Lab 01 - Single Agent](../../lab01-single-agent/README.md) prima di iniziare il Lab 02.

---

## Moduli

| # | Modulo | Cosa farai |
|---|--------|------------|
| 0 | [Prerequisiti](00-prerequisites.md) | Verifica del completamento del Lab 01, comprensione dei concetti multi-agente |
| 1 | [Comprendere l'Architettura Multi-Agente](01-understand-multi-agent.md) | Impara WorkflowBuilder, ruoli degli agenti, grafo di orchestrazione |
| 2 | [Impostare il Progetto Multi-Agente](02-scaffold-multi-agent.md) | Usa l'estensione Foundry per impostare un flusso di lavoro multi-agente |
| 3 | [Configura Agenti & Ambiente](03-configure-agents.md) | Scrivi istruzioni per 4 agenti, configura lo strumento MCP, imposta variabili di ambiente |
| 4 | [Schemi di Orchestrazione](04-orchestration-patterns.md) | Esplora fan-out parallelo, aggregazione sequenziale e schemi alternativi |
| 5 | [Testa Localmente](05-test-locally.md) | Debug F5 con Agent Inspector, esegui test smoke con curriculum + JD |
| 6 | [Distribuisci su Foundry](06-deploy-to-foundry.md) | Costruisci il container, push su ACR, registra agente ospitato |
| 7 | [Verifica in Playground](07-verify-in-playground.md) | Testa l’agente distribuito negli playground di VS Code e Foundry Portal |
| 8 | [Risoluzione Problemi](08-troubleshooting.md) | Risolvi problemi comuni multi-agente (errori MCP, output troncato, versioni pacchetti) |

---

## Tempo stimato

| Livello di esperienza | Tempo |
|-----------------------|-------|
| Completato il Lab 01 di recente | 45-60 minuti |
| Un po' di esperienza con Azure AI | 60-90 minuti |
| Prima esperienza con multi-agente | 90-120 minuti |

---

## Architettura a colpo d'occhio

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

**Torna a:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Esclusione di responsabilità**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Pur impegnandoci per l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua madre deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale umana. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall'uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->