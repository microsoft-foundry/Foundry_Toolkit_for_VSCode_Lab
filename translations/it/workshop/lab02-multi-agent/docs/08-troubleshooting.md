# Modulo 8 - Risoluzione dei problemi

Questo modulo copre errori comuni, correzioni e strategie di debug specifiche per il flusso di lavoro multi-agente.

## Problemi di output dell'agente

### GapAnalyzer dice “Non ho ancora il report di corrispondenza”

**Sintomo:** La risposta di GapAnalyzer ti chiede di incollare un report di corrispondenza con “Competenze mancanti” e “Lacune di certificazione.” Questo accade anche quando hai inviato sia un curriculum che una descrizione del lavoro.

**Causa:** Il testo JD non è stato passato a valle all'agente JD. Con `context_mode="last_agent"`, `resume_executor` è l'unico executor che vede mai il messaggio originale dell'utente. Se `RESUME_PARSER_INSTRUCTIONS` non include il testo JD nel suo output, l'agente JD non ha un JD da analizzare, MatchingAgent non può calcolare un punteggio di corrispondenza e GapAnalyzer riceve un input insignificante.

**Diagnosi:**

Nei log del server, cerca il tratto (span) MatchingAgent. Se contiene:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
il pass-through manca o è rotto.

**Correzione:** Conferma che `RESUME_PARSER_INSTRUCTIONS` in `main.py` contenga una sezione `[JOB DESCRIPTION PASS-THROUGH]` e la regola:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Conferma anche che `JOB_DESCRIPTION_INSTRUCTIONS` contenga una regola di passaggio `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Se uno dei due blocchi di istruzioni è un esempio dal wizard di scaffold, sostituiscilo con la versione completa da [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent restituisce “Cannot compute fit score - no JD provided”

Questa è la stessa causa principale di cui sopra. MatchingAgent ha ricevuto l'output dall'agente JD ma la sezione `[PARSED RESUME PASS-THROUGH]` mancava o era vuota, quindi non poteva confrontare i due profili. Conferma:
1. `JOB_DESCRIPTION_INSTRUCTIONS` include la regola: `Copia [PARSED RESUME] letteralmente - Matching Agent ne dipende in downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` dice all’agente di cercare le sezioni `[JD REQUIREMENTS]` e `[PARSED RESUME PASS-THROUGH]`.

Sostituisci entrambi i blocchi di istruzioni con le versioni complete da [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### La risposta appare due volte

**Sintomo:** L'output di GapAnalyzer (o l'intero output della pipeline) appare due volte nella risposta dell'Inspector Agente.

**Causa:** `WorkflowBuilder` usa una semantica OR per gli archi in ingresso - un executor a valle si attiva non appena **qualsiasi** predecessore termina. Se `matching_executor` ha due archi in ingresso (uno da `resume_executor` e uno da `jd_executor`), si attiva due volte: una volta quando ResumeParser termina e un'altra quando l'agente JD termina. Anche GapAnalyzer si esegue quindi due volte.

**Correzione:** Assicurati che il grafo `WorkflowBuilder` sia una pipeline rigorosamente sequenziale senza fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NON da resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Se hai una linea `.add_edge(resume_executor, matching_executor)` errante, rimuovila. Il relay `[PARSED RESUME PASS-THROUGH]` nell'output dell'agente JD dà già a MatchingAgent l'accesso al curriculum.

---

## Problemi di ambiente e configurazione

### Valori `.env` mancanti o errati

Il file `.env` deve essere nella directory `PersonalCareerCopilot/` (stesso livello di `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Contenuto `.env` previsto:

**Percorso A - cloud Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Percorso B - Foundry Locale:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Entrambi i percorsi usano `FOUNDRY_PROJECT_ENDPOINT`. Il valore differisce: il cloud usa un endpoint Foundry `https://`; il locale usa `http://localhost:5273/v1`. Esegui `foundry model list` per confermare l’alias modello esatto per il Percorso B.

> **Trovare il tuo `FOUNDRY_PROJECT_ENDPOINT`:**
- Apri la barra laterale **Foundry Toolkit** in VS Code → clic destro sul progetto → **Copy Project Endpoint**.
- Oppure vai su [Azure Portal](https://portal.azure.com) → il tuo progetto Foundry → **Overview** → **Project endpoint**.

> **Trovare il tuo `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Nella barra laterale Foundry Toolkit, espandi il progetto → **Models** → trova il nome del modello distribuito (es. `gpt-4.1-mini`).

### Precedenza variabili ambiente

`main.py` usa `load_dotenv(override=True)`, il che significa:

| Priorità | Fonte | Vence quando entrambi sono impostati? |
|----------|--------|------------------------------------|
| 1 (più alta) | file `.env` | Sì |
| 2 | Variabile ambiente shell / container | Usata se la stessa chiave non è presente in `.env` |

In sviluppo locale, questo fa sì che `.env` sia la fonte di verità (modificando `.env` si influenzano immediatamente le esecuzioni). In deployment ospitato, Foundry inietta le variabili ambiente a livello container; dato che `.env` non fa parte dell'immagine distribuita per questo laboratorio, vengono usati i valori iniettati dal container.

---

## Compatibilità delle versioni

### Matrice versione pacchetti

Il flusso di lavoro multi-agente richiede versioni specifiche dei pacchetti. Versioni non corrispondenti causano errori di runtime.

| Pacchetto | Versione richiesta | Comando di verifica |
|---------|-----------------|--------------------|
| `agent-framework-foundry` | ultima | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ultima | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ultima | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Errori comuni di versione

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Correzione: reinstallare agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Correzione: aggiornare il pacchetto mcp
pip install mcp --upgrade
```

### Verifica tutte le versioni contemporaneamente

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Output previsto:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problemi di distribuzione

### Il container non parte dopo la distribuzione

1. **Controlla i log del container:**
   - Apri la barra laterale **Foundry Toolkit** → espandi **Hosted Agents (Preview)** → clicca sul tuo agente → espandi la versione → **Container Details** → **Logs**.
   - Cerca tracce di stack Python o errori di moduli mancanti.

2. **Errori comuni di avvio container:**

   | Errore nei log | Causa | Correzione |
   |--------------|-------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` manca un pacchetto | Aggiungi il pacchetto, ridistribuisci |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variabili ambiente `agent.yaml` o `.env` non impostate | Aggiorna la sezione `environment_variables` di `agent.yaml` (ospitato) o `.env` (locale) |
   | `azure.identity.CredentialUnavailableError` | Identità gestita non configurata | Foundry lo imposta automaticamente - assicurati di distribuire tramite l’estensione |
   | `OSError: port 8088 already in use` | Dockerfile espone porta errata o conflitto porte | Verifica `EXPOSE 8088` in Dockerfile e `CMD ["python", "main.py"]` |
   | Il container esce con codice 1 | Eccezione non gestita in `main()` | Testa prima localmente ([Modulo 5](05-test-locally.md)) per intercettare errori prima della distribuzione |

3. **Ridispiega dopo aver corretto:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → seleziona lo stesso agente → distribuisci una nuova versione.

### La distribuzione impiega troppo tempo

I container multi-agente impiegano più tempo ad avviarsi perché creano 4 istanze di agente all’avvio. Tempi di avvio normali:

| Fase | Durata prevista |
|-------|----------------|
| Build immagine container | 1-3 minuti |
| Push immagine su ACR | 30-60 secondi |
| Avvio container (singolo agente) | 15-30 secondi |
| Avvio container (multi-agente) | 30-120 secondi |
| Agente disponibile nel Playground | 1-2 minuti dopo “Started” |

> Se lo stato "Pending" persiste oltre 5 minuti, controlla i log del container per errori.

---

## Problemi RBAC e autorizzazioni

### `403 Forbidden` o `AuthorizationFailed`

Hai bisogno del ruolo **[Foundry User](https://aka.ms/foundry-ext-project-role)** sul tuo progetto Foundry (precedentemente chiamato **Azure AI User** - ID ruolo invariato):

1. Vai su [Azure Portal](https://portal.azure.com) → la risorsa **project** del tuo progetto Foundry.
2. Clicca su **Access control (IAM)** → **Role assignments**.
3. Cerca il tuo nome → conferma che sia elencato **Foundry User** (o l'etichetta legacy **Azure AI User**).
4. Se manca: **Aggiungi** → **Add role assignment** → cerca **Foundry User** → assegna al tuo account.

Consulta la documentazione su [RBAC per Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) per i dettagli.

### Distribuzione modello non accessibile

Se l'agente restituisce errori relativi al modello:

1. Verifica che il modello sia distribuito: barra laterale Foundry → espandi progetto → **Models** → verifica `gpt-4.1-mini` (o il tuo modello) con stato **Succeeded**.
2. Verifica che il nome distribuito corrisponda: confronta `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` (o `agent.yaml`) con il nome effettivo della distribuzione nella barra laterale.
3. Se la distribuzione è scaduta (livello gratuito): ridistribuisci da [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemi con Foundry Local (Percorso B)

### Servizio Foundry Local non in esecuzione

```powershell
# Controlla lo stato
foundry local status

# Avvia il servizio se è fermo
foundry local start
```

| Sintomo | Causa | Correzione |
|---------|-------|-----------|
| Health check ritorna `503` | Servizio non avviato | `foundry local start` o clicca **Start** nella barra laterale Foundry Toolkit |
| Health check scade | Modello ancora in caricamento | Attendi 30–60 s dopo l’avvio; modelli più grandi richiedono più tempo |
| `StatusCode: 404` su `/v1/health` | Porta errata | Di default è `5273`. Controlla con `foundry local status` la porta effettiva |
| Risorse insufficienti | Foundry Local richiede ~4 GB di RAM libera | Chiudi altre applicazioni |
| Download modello fallito | Spazio su disco insufficiente | I modelli pesano 2–8 GB. Libera spazio, poi esegui `foundry model pull <name>` |

### Disallineamento nome modello

```powershell
# Elenca i modelli scaricati e i loro alias esatti
foundry model list
```

Imposta `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` con l’alias esatto mostrato (es. `phi-4-mini`, non `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` su esecuzione locale (Percorso B)

Il `main.py` del laboratorio usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local richiede che questa variabile punti al servizio locale - **non** a `AZURE_AI_PROJECT_ENDPOINT`. Assicurati che il tuo `.env` contenga:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Lo strumento MCP fa ancora una chiamata in uscita (Percorso B)

Questo è previsto. Lo strumento `search_microsoft_learn_for_plan` recupera risorse di apprendimento da `https://learn.microsoft.com/api/mcp`. **Solo la query del nome della competenza** viaggia in rete - il curriculum e il testo JD sono elaborati interamente sul tuo dispositivo e mai trasmessi. Se è richiesta un'operazione completamente offline, aggiungi un fallback `try/except` nello strumento che restituisce un URL statico `learn.microsoft.com` quando l'endpoint non è raggiungibile.

---

## Ottenere aiuto

Se sei bloccato dopo aver provato le correzioni sopra:

1. **Controlla i log del server** - La maggior parte degli errori produce una traccia dello stack Python nel terminale. Leggi l’intero traceback.
2. **Cerca il messaggio d'errore** - Copia il testo dell'errore e cerca in [Microsoft Q&A per Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Apri un problema** - Apri una issue nel [repository del workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) con:
   - Il messaggio d'errore o uno screenshot
   - Le versioni dei pacchetti (`pip list | Select-String "agent-framework"`)
   - La versione di Python (`python --version`)
   - Se il problema è locale o dopo la distribuzione

---

### Checkpoint

- [ ] Sai come controllare e correggere problemi di configurazione `.env`
- [ ] Puoi verificare che le versioni dei pacchetti corrispondano alla matrice richiesta
- [ ] Sai come controllare i log del container per errori di distribuzione
- [ ] Puoi verificare i ruoli RBAC nel portale Azure

---

**Precedente:** [07 - Verifica nel Playground](07-verify-in-playground.md) · **Successivo:** [09 - Sommario →](09-summary.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->