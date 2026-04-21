# Modulo 8 - Risoluzione dei problemi (Multi-Agente)

Questo modulo copre errori comuni, correzioni e strategie di debug specifiche per il flusso di lavoro multi-agente. Per problemi generali di distribuzione di Foundry, fare anche riferimento alla [guida alla risoluzione dei problemi del Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Riferimento rapido: Errore → Correzione

| Errore / Sintomo | Causa Probabile | Correzione |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | File `.env` mancante o valori non impostati | Creare `.env` con `PROJECT_ENDPOINT=<your-endpoint>` e `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Ambiente virtuale non attivato o dipendenze non installate | Eseguire `.\.venv\Scripts\Activate.ps1` poi `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Pacchetto MCP non installato (mancante nei requisiti) | Eseguire `pip install mcp` o verificare che `requirements.txt` lo includa come dipendenza transitiva |
| L'agente parte ma restituisce risposta vuota | `output_executors` non corrispondente o mancano archi | Verificare `output_executors=[gap_analyzer]` e che tutti gli archi esistano in `create_workflow()` |
| Solo 1 scheda gap (le altre mancanti) | Istruzioni GapAnalyzer incomplete | Aggiungere il paragrafo `CRITICAL:` a `GAP_ANALYZER_INSTRUCTIONS` - vedi [Modulo 3](03-configure-agents.md) |
| Il punteggio Fit è 0 o assente | MatchingAgent non ha ricevuto dati a monte | Verificare che esistano sia `add_edge(resume_parser, matching_agent)` che `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Server MCP ha respinto la chiamata tool | Controllare la connettività internet. Provare ad aprire `https://learn.microsoft.com/api/mcp` nel browser. Riprova |
| Nessun URL Microsoft Learn nell'output | Tool MCP non registrato o endpoint errato | Verificare `tools=[search_microsoft_learn_for_plan]` su GapAnalyzer e che `MICROSOFT_LEARN_MCP_ENDPOINT` sia corretto |
| `Address already in use: port 8088` | Un altro processo usa la porta 8088 | Eseguire `netstat -ano \| findstr :8088` (Windows) o `lsof -i :8088` (macOS/Linux) e terminare processo in conflitto |
| `Address already in use: port 5679` | Conflitto porta Debugpy | Terminare altre sessioni di debug. Eseguire `netstat -ano \| findstr :5679` per trovare e chiudere il processo |
| Agent Inspector non si apre | Server non completamente avviato o conflitto di porta | Attendere il log "Server running". Verificare che la porta 5679 sia libera |
| `azure.identity.CredentialUnavailableError` | Non connesso a Azure CLI | Eseguire `az login` poi riavviare il server |
| `azure.core.exceptions.ResourceNotFoundError` | Distribuzione modello inesistente | Verificare che `MODEL_DEPLOYMENT_NAME` corrisponda a un modello distribuito nel progetto Foundry |
| Stato container "Failed" dopo la distribuzione | Crash del container all'avvio | Controllare i log del container nel pannello laterale Foundry. Comune: variabile env mancante o errore di import |
| La distribuzione mostra "Pending" per > 5 minuti | Container impiega troppo per avviarsi o limiti risorse | Attendere fino a 5 minuti per multi-agente (crea 4 istanze agente). Se ancora pending, controllare i log |
| `ValueError` da `WorkflowBuilder` | Configurazione del grafo non valida | Assicurarsi che `start_executor` sia impostato, `output_executors` sia una lista, e non ci siano archi circolari |

---

## Problemi di ambiente e configurazione

### Valori `.env` mancanti o errati

Il file `.env` deve trovarsi nella directory `PersonalCareerCopilot/` (stesso livello di `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Contenuto `.env` atteso:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Trovare il tuo PROJECT_ENDPOINT:** 
- Apri la barra laterale **Microsoft Foundry** in VS Code → clic destro sul progetto → **Copia Project Endpoint**. 
- Oppure vai su [Azure Portal](https://portal.azure.com) → progetto Foundry → **Panoramica** → **Project endpoint**.

> **Trovare il tuo MODEL_DEPLOYMENT_NAME:** Nella barra laterale di Foundry, espandi il progetto → **Models** → trova il nome del modello distribuito (es. `gpt-4.1-mini`).

### Precedenza variabili Env

`main.py` usa `load_dotenv(override=False)`, cioè:

| Priorità | Fonte | Vince se entrambi sono impostati? |
|----------|--------|------------------------|
| 1 (massima) | Variabile ambiente shell | Sì |
| 2 | File `.env` | Solo se la variabile shell non è impostata |

Questo significa che le variabili d'ambiente runtime di Foundry (impostate tramite `agent.yaml`) hanno precedenza sui valori `.env` durante la distribuzione ospitata.

---

## Compatibilità versioni

### Matrice versioni pacchetti

Il flusso di lavoro multi-agente richiede versioni pacchetto specifiche. Versioni non corrispondenti causano errori a runtime.

| Pacchetto | Versione richiesta | Comando controllo |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | ultima pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Errori comuni di versione

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Correzione: aggiornamento a rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` non trovato o Inspector incompatibile:**

```powershell
# Correzione: installare con il flag --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Correzione: aggiornare il pacchetto mcp
pip install mcp --upgrade
```

### Verifica tutte le versioni in una volta

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Output atteso:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Problemi con lo strumento MCP

### Lo strumento MCP non restituisce risultati

**Sintomo:** Le schede gap dicono "No results returned from Microsoft Learn MCP" o "No direct Microsoft Learn results found".

**Possibili cause:**

1. **Problema di rete** - L'endpoint MCP (`https://learn.microsoft.com/api/mcp`) non è raggiungibile.
   ```powershell
   # Verifica la connettività
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Se questo restituisce `200`, l'endpoint è raggiungibile.

2. **Query troppo specifica** - Il nome della competenza è troppo di nicchia per la ricerca Microsoft Learn.
   - Questo è previsto per competenze molto specializzate. Lo strumento ha un URL di fallback nella risposta.

3. **Timeout sessione MCP** - La connessione Streamable HTTP è scaduta.
   - Riprova la richiesta. Le sessioni MCP sono effimere e possono necessitare di riconnessione.

### Log MCP spiegati

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Significato | Azione |
|-----|---------|--------|
| `GET → 405` | Sondaggio client MCP durante inizializzazione | Normale - ignorare |
| `POST → 200` | Chiamata tool riuscita | Previsto |
| `DELETE → 405` | Sondaggio client MCP durante pulizia | Normale - ignorare |
| `POST → 400` | Richiesta errata (query malformata) | Controllare il parametro `query` in `search_microsoft_learn_for_plan()` |
| `POST → 429` | Limite di richieste superato | Attendere e riprovare. Ridurre parametro `max_results` |
| `POST → 500` | Errore server MCP | Transitorio - riprovare. Se persiste, l’API Microsoft Learn MCP può essere down |
| Timeout connessione | Problema rete o server MCP non disponibile | Controllare internet. Provare `curl https://learn.microsoft.com/api/mcp` |

---

## Problemi di distribuzione

### Il container non si avvia dopo la distribuzione

1. **Controlla i log del container:**
   - Apri la barra laterale **Microsoft Foundry** → espandi **Hosted Agents (Preview)** → clicca il tuo agente → espandi la versione → **Container Details** → **Logs**.
   - Cerca tracce di errori Python o moduli mancanti.

2. **Guasti comuni all'avvio del container:**

   | Errore nei log | Causa | Correzione |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` manca un pacchetto | Aggiungere il pacchetto, ridistribuire |
   | `RuntimeError: Missing required environment variable` | Variabili env in `agent.yaml` non impostate | Aggiornare `agent.yaml` → sezione `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity non configurata | Foundry lo imposta automaticamente - assicurarsi di distribuire via estensione |
   | `OSError: port 8088 already in use` | Dockerfile espone porta errata o conflitto porta | Verificare `EXPOSE 8088` in Dockerfile e `CMD ["python", "main.py"]` |
   | Il container esce con codice 1 | Eccezione non gestita in `main()` | Testare localmente prima ([Modulo 5](05-test-locally.md)) per intercettare errori prima di distribuire |

3. **Ridispiegare dopo correzione:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → seleziona lo stesso agente → distribuisci nuova versione.

### La distribuzione impiega troppo tempo

I container multi-agente impiegano più tempo ad avviarsi perché creano 4 istanze agente all'avvio. Tempi normali di avvio:

| Fase | Durata prevista |
|-------|------------------|
| Build immagine container | 1-3 minuti |
| Push immagine su ACR | 30-60 secondi |
| Avvio container (agente singolo) | 15-30 secondi |
| Avvio container (multi-agente) | 30-120 secondi |
| Agente disponibile in Playground | 1-2 minuti dopo "Started" |

> Se lo stato "Pending" persiste oltre 5 minuti, controllare i log container per errori.

---

## Problemi RBAC e permessi

### `403 Forbidden` o `AuthorizationFailed`

Serve il ruolo **[Azure AI User](https://aka.ms/foundry-ext-project-role)** sul progetto Foundry:

1. Vai su [Azure Portal](https://portal.azure.com) → risorsa **progetto** Foundry.
2. Clicca su **Controllo accessi (IAM)** → **Assegnazioni ruoli**.
3. Cerca il tuo nome → conferma che **Azure AI User** sia presente.
4. Se manca: **Aggiungi** → **Aggiungi assegnazione ruolo** → cerca **Azure AI User** → assegna al tuo account.

Consultare la documentazione [RBAC per Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) per dettagli.

### Distribuzione modello non accessibile

Se l'agente restituisce errori relativi al modello:

1. Verificare che il modello sia distribuito: barra laterale Foundry → espandi progetto → **Models** → controlla `gpt-4.1-mini` (o tuo modello) con stato **Succeeded**.
2. Verificare che il nome distribuzione corrisponda: confronta `MODEL_DEPLOYMENT_NAME` in `.env` (o `agent.yaml`) con nome distribuzione effettiva nella barra laterale.
3. Se la distribuzione è scaduta (tier gratuito): ridistribuire dal [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problemi Agent Inspector

### Inspector si apre ma mostra "Disconnected"

1. Verificare che il server sia in esecuzione: cercare "Server running on http://localhost:8088" nel terminale.
2. Controllare porta `5679`: Inspector si connette via debugpy sulla porta 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Riavviare il server e riaprire l’Inspector.

### Inspector mostra risposta parziale

Le risposte multi-agente sono lunghe e si trasmettono progressivamente. Attendere il completamento della risposta completa (può richiedere 30-60 secondi a seconda del numero di schede gap e chiamate MCP).

Se la risposta è costantemente troncata:
- Verificare che le istruzioni GapAnalyzer contengano il blocco `CRITICAL:` che impedisce di combinare le schede gap.
- Controllare il limite token del modello - `gpt-4.1-mini` supporta fino a 32K token in uscita, dovrebbero essere sufficienti.

---

## Consigli sulle prestazioni

### Risposte lente

I flussi di lavoro multi-agente sono intrinsecamente più lenti dei singoli agenti a causa di dipendenze sequenziali e chiamate allo strumento MCP.

| Ottimizzazione | Come | Impatto |
|-------------|-----|--------|
| Ridurre chiamate MCP | Abbassare il parametro `max_results` nello strumento | Meno round-trip HTTP |
| Semplificare istruzioni | Prompt agente più brevi e focalizzati | Inferenza LLM più veloce |
| Usare `gpt-4.1-mini` | Più veloce di `gpt-4.1` per sviluppo | ~2x miglioramento velocità |
| Ridurre dettaglio schede gap | Semplificare il formato delle schede gap nelle istruzioni GapAnalyzer | Meno output da generare |

### Tempi tipici di risposta (locale)

| Configurazione | Tempo previsto |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 schede gap | 30-60 secondi |
| `gpt-4.1-mini`, 8+ schede gap | 60-120 secondi |
| `gpt-4.1`, 3-5 schede gap | 60-120 secondi |
---

## Ottenere aiuto

Se sei bloccato dopo aver provato le correzioni sopra:

1. **Controlla i log del server** - La maggior parte degli errori produce una traccia dello stack Python nel terminale. Leggi l'intero traceback.
2. **Cerca il messaggio di errore** - Copia il testo dell'errore e cerca in [Microsoft Q&A per Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Apri un problema** - Inoltra un problema nel [repository del workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) con:
   - Il messaggio di errore o uno screenshot
   - Le versioni dei tuoi pacchetti (`pip list | Select-String "agent-framework"`)
   - La tua versione di Python (`python --version`)
   - Se il problema è locale o dopo il deployment

---

### Checkpoint

- [ ] Puoi identificare e correggere gli errori multi-agente più comuni utilizzando la tabella di riferimento rapido
- [ ] Sai come controllare e correggere problemi di configurazione `.env`
- [ ] Puoi verificare che le versioni dei pacchetti corrispondano alla matrice richiesta
- [ ] Comprendi le voci di log MCP e puoi diagnosticare i guasti degli strumenti
- [ ] Sai come controllare i log dei container per i fallimenti di deployment
- [ ] Puoi verificare i ruoli RBAC nel Portale Azure

---

**Precedente:** [07 - Verifica nel Playground](07-verify-in-playground.md) · **Home:** [Lab 02 README](../README.md) · [Home del Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Pur impegnandoci per garantire l’accuratezza, si prega di tenere presente che le traduzioni automatiche possono contenere errori o inesattezze. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche si raccomanda una traduzione professionale effettuata da un essere umano. Non ci assumiamo alcuna responsabilità per eventuali incomprensioni o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->