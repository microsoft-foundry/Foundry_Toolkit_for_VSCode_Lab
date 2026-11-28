# Modulo 9 - Riepilogo e prossimi passi

⏱️ ~5 min

**Congratulazioni!** Hai creato, testato e (se sul Percorso A) distribuito un workflow multi-agente utilizzando Microsoft Foundry e il Foundry Toolkit per VS Code.

---

## Cosa hai costruito

Il **Valutatore di corrispondenza Curriculum → Lavoro** - un workflow multi-agente ospitato che:
- Riceve un curriculum + descrizione del lavoro via HTTP (`POST /responses`)
- Esegue quattro agenti specializzati in una pipeline sequenziale - ogni agente trasmette i dati necessari al successore
- Restituisce un punteggio di corrispondenza (0–100 con dettaglio), una lista di gap di competenze e certificazioni, e una roadmap di apprendimento personalizzata con link reali a Microsoft Learn per ogni gap
- Chiama il server MCP di Microsoft Learn (`https://learn.microsoft.com/api/mcp`) per recuperare risorse di apprendimento ufficiali per ogni gap identificato
- Funziona come un singolo agente containerizzato ospitato nel Microsoft Foundry Agent Service

---

## Concetti chiave appresi

| Concetto | Cosa hai praticato |
|---------|-------------------|
| **Orchestrazione multi-agente** | pipeline sequenziale con `WorkflowBuilder` e `add_edge()` |
| **Specializzazione dell'agente** | Quattro agenti focalizzati sono più efficaci di un agente generico |
| **Pattern Content Router** | ResumeParser funge anche da router - conserva il testo JD in una sezione `[JOB DESCRIPTION PASS-THROUGH]` così gli agenti a valle possono accedervi (necessario perché `context_mode="last_agent"` significa che solo `start_executor` vede il messaggio utente grezzo) |
| **Pattern Content Relay** | L'agente JD trasmette `[PARSED RESUME PASS-THROUGH]` in avanti così MatchingAgent ottiene entrambi i profili; evita il doppio trigger con semantica OR che i grafi fan-in causano |
| **Integrazione strumento MCP** | `@tool` + `streamable_http_client` che chiamano un server MCP esterno |
| **Ciclo di vita Hosted Agent** | Scaffold → Configura → Testa localmente → Distribuisci → Verifica nel cloud |
| **`context_mode="last_agent"`** | Ogni esecutore vede solo l'output diretto del predecessore |
| **Workflow Foundry Toolkit** | Scaffold wizard, Agent Inspector, Workflow Visualizer, deploy con un click |

---

## Cosa hai completato

<details open>
<summary><strong>🅰️ Percorso A - Abbonamento Foundry</strong></summary>

- [x] Verificata configurazione Lab 01: progetto, modello e RBAC ancora attivi
- [x] Scaffold di un progetto multi-agente usando il template Workflows
- [x] Scritti quattro set di istruzioni per agenti (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrato strumento Microsoft Learn MCP con `streamable_http_client`
- [x] Collegato il grafo del workflow con `WorkflowBuilder` (pipeline sequenziale con content relay)
- [x] Testato localmente con 2 test smoke (Agent Inspector) - punteggio fit, card gap, e URL MCP
- [x] Distribuito su Foundry Agent Service (containerizzato, identità gestita)
- [x] Verificato nel playground cloud - coerenza strutturale con risultati locali

</details>

<details open>
<summary><strong>🅱️ Percorso B - Foundry Local</strong></summary>

- [x] Verificata configurazione Lab 01: Foundry Local in esecuzione con modello locale
- [x] Scaffold di un progetto multi-agente usando il template Workflows
- [x] Scritti quattro set di istruzioni per agenti e collegato il grafo del workflow
- [x] Integrato strumento Microsoft Learn MCP
- [x] Testato localmente con 2 test smoke
- [x] Validato comportamento multi-agente senza necessità di risorse cloud

</details>

---

## Prossimi passi

### Continua ad imparare

| Risorsa | Descrizione |
|----------|-------------|
| **[Riferimento Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentazione API per `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catalogo strumento MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Collega agenti ad altri server MCP (Bing, GitHub, personalizzati) |
| **[Aggiungi conoscenza (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Fornisci agli agenti documenti, archivi vettoriali o ricerca Bing |
| **[Valutazioni Foundry](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Misura la qualità dell'agente su scala con valutatori automatici |
| **[Documentazione Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Riferimento completo della piattaforma |
| **[Foundry Toolkit - Novità](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Note di rilascio dell'estensione e changelog |

### Idee per estendere questo workflow

- **Aggiungi un 5° agente** - Un coach per colloqui che genera possibili domande basate sul report gap
- **Aggiungi uno strumento di grounding Bing** - Permetti all'agente JD di cercare annunci di lavoro simili per arricchire i requisiti
- **Connettiti a un database di curriculum** - Estrai profili candidati da un database tramite un `@tool` personalizzato
- **Prova modelli diversi** - Confronta qualità e latenza di output tra `gpt-4.1` e `gpt-4.1-mini`
- **Valuta con Foundry** - Usa la funzione Valutazioni per assegnare punteggi ai report di corrispondenza rispetto a un dataset aureo

### Per gli utenti del Percorso B: Aggiorna alla distribuzione cloud

Quando sei pronto a distribuire nel cloud:
1. Ottieni un abbonamento Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Completa [Lab 01, Modulo 01](../../lab01-single-agent/docs/01-setup.md) (crea progetto, distribuisci modello, assegna RBAC)
3. Aggiorna il tuo `.env` con l'endpoint progetto Foundry e il nome della distribuzione modello
4. Continua da [Modulo 06 - Distribuisci su Foundry](06-deploy-to-foundry.md)

---

## Pulizia risorse (opzionale)

Se desideri rimuovere le risorse Azure create durante questo workshop:

### Opzione 1: Elimina il gruppo di risorse (rimuove tutto)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opzione 2: Elimina solo l'agente ospitato

1. Apri [ai.azure.com](https://ai.azure.com) → il tuo progetto → **Build** → **Agents**.
2. Trova **PersonalCareerCopilot** → clicca su **Elimina**.

### Opzione 3: Elimina la distribuzione del modello

1. Nella barra laterale di Foundry, espandi il tuo progetto → **Models**.
2. Clic destro sulla distribuzione modello → **Elimina**.

> **Nota sui costi:** Gli agenti ospitati comportano costi solo mentre sono in esecuzione. Se fermi o elimini l'agente, non ci sono addebiti in corso. La distribuzione del modello può generare un piccolo costo per capacità riservata - eliminala se hai terminato.

---

**Precedente:** [08 - Risoluzione problemi](08-troubleshooting.md) · **Home:** [Lab 02 README](../README.md) · [Home Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->