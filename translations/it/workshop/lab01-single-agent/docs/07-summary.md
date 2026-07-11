# Modulo 7 - Riepilogo e Passi Successivi

⏱️ ~5 min

**Congratulazioni!** Hai creato, testato e (se nel Percorso A) distribuito un agente AI ospitato utilizzando Microsoft Foundry e il Foundry Toolkit per VS Code.

---

## Cosa hai creato

Un agente **"Spiega come se fossi un Dirigente"** che:
- Riceve rapporti tecnici di incidenti o aggiornamenti operativi tramite HTTP (`POST /responses`)
- Li traduce in riassunti esecutivi in linguaggio semplice
- Segue un formato di output strutturato (Cosa è successo / Impatto sul business / Passo successivo)
- Rifiuta richieste fuori tema e tentativi di prompt injection
- Funziona come agente ospitato containerizzato nel Microsoft Foundry Agent Service

---

## Concetti chiave appresi

| Concetto | Cosa hai praticato |
|---------|-------------------|
| **Architettura Agent Framework** | pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Ciclo di vita dell'agente ospitato** | Scaffold → Configura → Test locale → Distribuisci → Verifica sul cloud |
| **Progettazione prompt di sistema** | Ruolo, pubblico, formato output, regole, vincoli di sicurezza ed esempi |
| **Differenze locale vs ospitato** | Identità (credenziale personale vs identità gestita), endpoint, percorso di rete |
| **Confini di sicurezza** | Difesa da prompt injection, rispetto del ruolo, gestione elegante di casi limite |
| **Workflow Foundry Toolkit** | Creazione progetto, deployment modello, scaffolding agente, Agent Inspector, deploy con un clic |

---

## Cosa hai completato

### Percorso A (Sottoscrizione Foundry)

- [x] Configurato Foundry Toolkit e creato un progetto Foundry con un modello distribuito
- [x] Scaffolded un agente ospitato con struttura progetto auto-generata
- [x] Scritto istruzioni strutturate per l'agente con regole di sicurezza
- [x] Testato localmente con 3 scenari funzionali (Agent Inspector)
- [x] Distribuito su Foundry Agent Service (containerizzato)
- [x] Verificato nel playground cloud con 4 test di casi limite/sicurezza

### Percorso B (Foundry Locale)

- [x] Configurato Foundry Toolkit con endpoint modello locale
- [x] Scaffolded un progetto agente ospitato
- [x] Scritto istruzioni strutturate per l'agente con regole di sicurezza
- [x] Testato localmente con 3 scenari funzionali
- [x] Validato comportamento dell'agente senza bisogno di risorse cloud

---

## Passi successivi

### Continua ad imparare

| Risorsa | Descrizione |
|----------|-------------|
| **[Lab 02 - Orchestrazione Multi-Agente](../../lab02-multi-agent/docs/README.md)** | Costruisci un workflow a 4 agenti (Resume → Valutatore di Fit Lavorativo) con pattern di orchestrazione |
| **[Aggiungi strumenti al tuo agente](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Connetti API, database o funzioni personalizzate tramite il Catalogo Strumenti |
| **[Aggiungi conoscenza (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Fondamenta il tuo agente con documenti, archivi vettoriali o ricerca Bing |
| **[Documentazione Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Riferimento completo della piattaforma |
| **[Riferimento Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentazione API per il pacchetto `agent-framework` |
| **[Foundry Toolkit - Novità](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Note di rilascio ed elenco modifiche dell'estensione |

### Idee per estendere il tuo agente

- **Aggiungi uno strumento per la data** - Permetti all'agente di includere il contesto "a oggi" nei riassunti
- **Connettiti a un database degli incidenti** - Estrai dettagli reali degli incidenti tramite una funzione strumento
- **Aggiungi uno strumento di grounding Bing** - Permetti all'agente di cercare notizie recenti per contesto aggiuntivo
- **Prova modelli diversi** - Confronta la qualità di output di `gpt-4.1` vs. `gpt-4.1-mini`
- **Valuta con Foundry** - Usa la funzione Valutazioni per misurare la qualità dell'agente su larga scala

### Per utenti del Percorso B: Aggiorna al deployment cloud

Quando sei pronto a distribuire sul cloud:
1. Ottieni una sottoscrizione Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Completa [Modulo 01, Configurazione](01-setup.md#step-2-set-up-based-on-your-access) (crea progetto, distribuisci modello, assegna RBAC)
3. Aggiorna il tuo `.env` con l'endpoint del progetto Foundry e il nome del deployment del modello
4. Continua da [Modulo 05 - Deploy su Foundry](05-deploy-to-foundry.md)

---

## Pulisci le risorse (opzionale)

Se vuoi rimuovere le risorse Azure create durante questo workshop:

### Opzione 1: Elimina il gruppo di risorse (rimuove tutto)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opzione 2: Elimina solo l'agente ospitato

1. Apri [ai.azure.com](https://ai.azure.com) → il tuo progetto → **Build** → **Agents**.
2. Clicca sul tuo agente → clicca **Elimina**.

### Opzione 3: Elimina il deployment del modello

1. Nella sidebar di Foundry, espandi il tuo progetto → **Models**.
2. Click destro sul deployment del modello → **Elimina**.

> **Nota sui costi:** Gli agenti ospitati generano costi solo mentre sono attivi. Se fermi o elimini l'agente, non ci sono costi continui. Il deployment del modello può generare un piccolo costo per la capacità riservata - eliminalo se hai terminato.

---

**Precedente:** [06 - Verifica nel Playground](06-verify-in-playground.md) · **Successivo:** [08 - Risoluzione problemi (Riferimento) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->