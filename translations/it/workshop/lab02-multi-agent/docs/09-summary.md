# Modulo 9 - Riepilogo e Passi Successivi

⏱️ ~5 min

**Congratulazioni!** Hai costruito, testato e (se sul Percorso A) distribuito un workflow multi-agente utilizzando Microsoft Foundry e il Foundry Toolkit per VS Code.

---

## Cosa hai costruito

Il **Resume → Job Fit Evaluator** - un workflow multi-agente ospitato che:
- Riceve un curriculum + descrizione del lavoro via HTTP (`POST /responses`)
- Esegue quattro agenti specializzati in una pipeline sequenziale - ogni agente trasmette i dati che il suo successore necessita
- Restituisce un punteggio di adattamento (0–100 con dettaglio), una lista delle lacune in competenze e certificazioni, e una roadmap di apprendimento personalizzata con link reali a Microsoft Learn per ogni lacuna
- Chiama il server Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) per recuperare risorse ufficiali di apprendimento per ogni lacuna identificata
- Funziona come un unico agente ospitato containerizzato nel Microsoft Foundry Agent Service

---

## Concetti chiave appresi

| Concetto | Cosa hai messo in pratica |
|---------|-------------------------|
| **Orchestrazione multi-agente** | Pipeline sequenziale `WorkflowBuilder` con `add_edge()` |
| **Specializzazione degli agenti** | Quattro agenti focalizzati superano un agente generico |
| **Pattern Content Router** | ResumeParser funge anche da router - conserva il testo JD in una sezione `[JOB DESCRIPTION PASS-THROUGH]` così gli agenti a valle possono accedervi (necessario perché `context_mode="last_agent"` significa che solo `start_executor` vede il messaggio utente grezzo) |
| **Pattern Content Relay** | JD Agent trasmette avanti `[PARSED RESUME PASS-THROUGH]` così MatchingAgent ha entrambi i profili; evita il doppio trigger a semantica OR che i grafi di fan-in causano |
| **Integrazione tool MCP** | `@tool` + `streamable_http_client` che chiama un server MCP esterno |
| **Ciclo di vita Hosted Agent** | Scaffold → Configurazione → Test locale → Distribuzione → Verifica in cloud |
| **`context_mode="last_agent"`** | Ogni executor vede solo l'output del predecessore diretto |
| **Workflow Foundry Toolkit** | Wizard di scaffold, Agent Inspector, Workflow Visualizer, deploy con un click |

---

## Cosa hai completato

<details open>
<summary><strong>🅰️ Percorso A - Abbonamento Foundry</strong></summary>

- [x] Verificata configurazione Lab 01: progetto, modello e RBAC ancora attivi
- [x] Scaffold di un progetto multi-agente usando il template Workflows
- [x] Scritti quattro set di istruzioni agenti (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrato lo strumento Microsoft Learn MCP con `streamable_http_client`
- [x] Collegato il grafo workflow con `WorkflowBuilder` (pipeline sequenziale con content relay)
- [x] Testato localmente con 3 test smoke (Agent Inspector) - punteggio di adattamento, schede gap, e URL MCP
- [x] Distribuito su Foundry Agent Service (containerizzato, managed identity)
- [x] Verificato nel playground cloud - coerenza strutturale con risultati locali

</details>

<details open>
<summary><strong>🅱️ Percorso B - Foundry Local</strong></summary>

- [x] Verificata configurazione Lab 01: Foundry Local in esecuzione con modello locale
- [x] Scaffold di un progetto multi-agente usando il template Workflows
- [x] Scritti quattro set di istruzioni agenti e collegato il grafo workflow
- [x] Integrato lo strumento Microsoft Learn MCP
- [x] Testato localmente con 3 test smoke
- [x] Validato il comportamento multi-agente senza necessità di risorse cloud

</details>

---

## Passi successivi

### Continua ad imparare

| Risorsa | Descrizione |
|----------|-------------|
| **[Riferimento Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentazione API per `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catalogo tool MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Connetti agenti a altri server MCP (Bing, GitHub, personalizzati) |
| **[Aggiungi conoscenza (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Supporta agenti con documenti, archivi vettoriali o ricerca Bing |
| **[Valutazioni Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Misura la qualità degli agenti su larga scala con valutatori automatizzati |
| **[Documentazione Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Riferimento completo alla piattaforma |
| **[Foundry Toolkit - Novità](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Note di rilascio e changelog estensione |

### Idee per estendere questo workflow

- **Aggiungi un quinto agente** - Un coach per colloqui che produce probabili domande basate sul report delle lacune
- **Aggiungi uno strumento di grounding Bing** - Permetti all’agente JD di cercare offerte di lavoro simili per arricchire i requisiti
- **Connetti a un database di curricula** - Recupera profili candidati da un database tramite un `@tool` personalizzato
- **Prova modelli diversi** - Confronta qualità e latenza dell’output di `gpt-4.1` vs. `gpt-4.1-mini`
- **Valuta con Foundry** - Usa la funzionalità Evaluations per valutare report di adattamento contro un set di dati gold standard

### Per utenti Percorso B: aggiorna a distribuzione cloud

Quando sei pronto a distribuire sul cloud:
1. Ottieni una sottoscrizione Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Completa [Lab 01, Modulo 01](../../lab01-single-agent/docs/01-setup.md) (crea progetto, distribuisci modello, assegna RBAC)
3. Aggiorna il tuo `.env` con l’endpoint progetto Foundry e il nome distribuzione modello
4. Continua da [Modulo 06 - Distribuisci su Foundry](06-deploy-to-foundry.md)

---

## Pulizia risorse (opzionale)

Se vuoi rimuovere le risorse Azure create durante questo workshop:

### Opzione 1: Elimina il gruppo di risorse (rimuove tutto)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opzione 2: Elimina solo l’agente ospitato

1. Apri [ai.azure.com](https://ai.azure.com) → il tuo progetto → **Build** → **Agents**.
2. Trova **PersonalCareerCopilot** → clicca **Elimina**.

### Opzione 3: Elimina la distribuzione modello

1. Nella sidebar di Foundry, espandi il tuo progetto → **Models**.
2. Clic destro sulla distribuzione modello → **Elimina**.

> **Nota sui costi:** Gli agenti ospitati generano costi solo quando sono in esecuzione. Se fermi o elimini l’agente, non ci sono costi continui. La distribuzione modello può generare un piccolo costo per la capacità riservata - eliminala se hai finito.

---

**Precedente:** [08 - Risoluzione Problemi](08-troubleshooting.md) · **Home:** [Lab 02 README](../README.md) · [Home Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->