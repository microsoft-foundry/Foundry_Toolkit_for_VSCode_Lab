# Modulo 8 - Risoluzione dei problemi

Questo modulo copre errori comuni, correzioni e strategie di debug specifiche per il flusso di lavoro multi-agente.

## Problemi di output dell'agente

### GapAnalyzer dice "Non ho ancora il report corrispondente"

**Sintomo:** La risposta di GapAnalyzer chiede di incollare un report corrispondente con "Competenze Mancanti" e "Lacune di Certificazione." Questo accade anche quando hai inviato sia un curriculum che una descrizione del lavoro.

**Causa:** Il testo JD non è stato passato a valle all'agente JD. Con `context_mode="last_agent"`, `resume_executor` è l'unico esecutore che vede il messaggio originale dell'utente. Se `RESUME_PARSER_INSTRUCTIONS` non include il testo JD nel suo output, l'agente JD non ha JD da analizzare, MatchingAgent non può calcolare un punteggio di corrispondenza e GapAnalyzer riceve un input senza senso.

**Diagnosi:**

Nei log del server, cerca lo span di MatchingAgent. Se contiene:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
il passaggio è mancante o rotto.

**Correzione:** Conferma che `RESUME_PARSER_INSTRUCTIONS` in `main.py` contiene una sezione `[JOB DESCRIPTION PASS-THROUGH]` e la regola:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Conferma inoltre che `JOB_DESCRIPTION_INSTRUCTIONS` contiene una regola di inoltro `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Se uno dei due blocchi di istruzioni è un segnaposto dello scaffolding wizard, sostituiscilo con la versione completa da [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent riporta "Impossibile calcolare il punteggio di corrispondenza - JD non fornito"

Questa è la stessa causa principale di cui sopra. MatchingAgent ha ricevuto l'output dell'agente JD ma la sezione `[PARSED RESUME PASS-THROUGH]` era mancante o vuota, quindi non poteva confrontare i due profili. Conferma:
1. `JOB_DESCRIPTION_INSTRUCTIONS` include la regola di inoltro: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` indica all'agente di cercare le sezioni `[JD REQUIREMENTS]` e `[PARSED RESUME PASS-THROUGH]`.

Sostituisci entrambi i blocchi di istruzioni con le versioni complete da [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### La risposta appare due volte

**Sintomo:** L'output di GapAnalyzer (o l'intero output della pipeline) appare due volte nella risposta di Agent Inspector.

**Causa:** `WorkflowBuilder` usa la semantica OR per gli edge in ingresso - un esecutore a valle si attiva non appena **qualunque** predecessore termina. Se `matching_executor` ha due edge in ingresso (uno da `resume_executor` e uno da `jd_executor`), si attiva due volte: una quando ResumeParser termina e di nuovo quando JD Agent termina. Anche GapAnalyzer quindi viene eseguito due volte.

**Correzione:** Assicurati che il grafo `WorkflowBuilder` sia una pipeline strettamente sequenziale senza fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Se hai una riga `.add_edge(resume_executor, matching_executor)` dispersa, rimuovila. Il relay `[PARSED RESUME PASS-THROUGH]` nell'output di JD Agent dà già a MatchingAgent l'accesso al curriculum.

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

Contenuto atteso di `.env`:

**Percorso A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Percorso B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Entrambi i percorsi usano `FOUNDRY_PROJECT_ENDPOINT`. Il valore differisce: il cloud usa un endpoint Foundry `https://`; il locale usa `http://localhost:5273/v1`. Esegui `foundry model list` per confermare l'alias modello esatto per il Percorso B.

> **Come trovare il tuo `FOUNDRY_PROJECT_ENDPOINT`:** 
- Apri la barra laterale **Foundry Toolkit** in VS Code → clic destro sul tuo progetto → **Copia Endpoint Progetto**. 
- Oppure vai su [Azure Portal](https://portal.azure.com) → il tuo progetto Foundry → **Panoramica** → **Endpoint progetto**.

> **Come trovare il tuo `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Nella barra laterale Foundry Toolkit, espandi il progetto → **Modelli** → trova il nome del modello distribuito (es., `gpt-4.1-mini`).

### Precedenza delle variabili d'ambiente

`main.py` usa `load_dotenv(override=True)`, il che significa:

| Priorità | Fonte | Vince quando entrambi sono impostati? |
|----------|--------|------------------------|
| 1 (massima) | file `.env` | Sì |
| 2 | Variabile ambiente shell/contenitore | Usata quando la stessa chiave non è presente in `.env` |

In sviluppo locale, questo rende `.env` la fonte di verità (modificare `.env` influisce immediatamente sulle esecuzioni). In distribuzione ospitata, Foundry inietta variabili d'ambiente a livello di contenitore; poiché `.env` non fa parte dell'immagine distribuita per questa configurazione del laboratorio, vengono usati i valori iniettati nel contenitore.

---

## Compatibilità delle versioni

### Matrice versioni pacchetti

Il flusso multi-agente richiede versioni pacchetto specifiche. Versioni non corrispondenti causano errori di runtime.

| Pacchetto | Versione richiesta | Comando di verifica |
|---------|-----------------|---------------|
| `agent-framework-foundry` | ultima | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ultima | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ultima | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Errori comuni di versione

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Verificare tutte le versioni contemporaneamente

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Output atteso:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problemi di distribuzione

### Il contenitore non si avvia dopo la distribuzione

1. **Controlla i log del contenitore:**
   - Apri la barra laterale **Foundry Toolkit** → sotto il tuo progetto, clicca **Agents** → scheda **Hosted Agent** → clicca il tuo agente. Controlla lo **Stato** nella scheda **Dettagli**, quindi apri la scheda **Playground** e utilizza la scheda **Logs** nel pannello **Dettagli sessione** per vedere l'output del contenitore.
   - Cerca tracce di errori Python o errori di moduli mancanti.

2. **Errori comuni di avvio contenitore:**

   | Errore nei log | Causa | Correzione |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` mancante un pacchetto | Aggiungi il pacchetto, ridistribuisci |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | variabili d'ambiente `agent.yaml` o `.env` non impostate | Aggiorna `agent.yaml` → sezione `environment_variables` (ospitata) o `.env` (locale) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity non configurata | Foundry la imposta automaticamente - assicurati di distribuire tramite l'estensione |
   | `OSError: port 8088 already in use` | Dockerfile espone porta sbagliata o conflitto di porta | Verifica `EXPOSE 8088` nel Dockerfile e `CMD ["python", "main.py"]` |
   | Il contenitore si chiude con codice 1 | Eccezione non gestita in `main()` | Testa localmente prima ([Modulo 5](05-test-locally.md)) per catturare errori prima della distribuzione |

3. **Ridispiega dopo la correzione:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Distribuisci Hosted Agent** → seleziona lo stesso agente → distribuisci una nuova versione.

### La distribuzione richiede troppo tempo

I contenitori multi-agente impiegano più tempo ad avviarsi perché creano 4 istanze agente all'avvio. Tempi normali di avvio:

| Fase | Durata prevista |
|-------|------------------|
| Costruzione immagine contenitore | 1-3 minuti |
| Push immagine su ACR | 30-60 secondi |
| Avvio contenitore (agente singolo) | 15-30 secondi |
| Avvio contenitore (multi-agente) | 30-120 secondi |
| Agente disponibile in Playground | 1-2 minuti dopo "Avviato" |

> Se lo stato "In attesa" persiste oltre 5 minuti, controlla i log del contenitore per errori.

---

## Problemi RBAC e permessi

### `403 Forbidden` o `AuthorizationFailed`

Hai bisogno del ruolo **[Foundry User](https://aka.ms/foundry-ext-project-role)** nel tuo progetto Foundry (precedentemente chiamato **Azure AI User** - ID ruolo invariato):

1. Vai su [Azure Portal](https://portal.azure.com) → la risorsa **progetto** Foundry.
2. Clicca **Controllo accessi (IAM)** → **Assegnazioni ruoli**.
3. Cerca il tuo nome → conferma che sia elencato **Foundry User** (o l'etichetta legacy **Azure AI User**).
4. Se manca: **Aggiungi** → **Aggiungi assegnazione ruolo** → cerca **Foundry User** → assegna al tuo account.

Consulta la documentazione [RBAC per Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) per dettagli.

### Distribuzione modello non accessibile

Se l'agente restituisce errori relativi al modello:

1. Verifica che il modello sia distribuito: barra laterale Foundry → espandi progetto → **Modelli** → controlla la presenza di `gpt-4.1-mini` (o il tuo modello) con stato **Succeeded**.
2. Verifica che il nome della distribuzione corrisponda: confronta `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` (o `agent.yaml`) con il nome effettivo nella barra laterale.
3. Se la distribuzione è scaduta (tier gratuito): ridistribuisci da [Catalogo Modelli](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Apri Catalogo Modelli**).

---

## Problemi con Foundry Local (Percorso B)

### Servizio Foundry Local non in esecuzione

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Sintomo | Causa | Correzione |
|---------|-------|-----|
| Controllo salute restituisce `503` | Servizio non avviato | `foundry local start` o clicca **Avvia** nella barra laterale Foundry Toolkit |
| Controllo salute scade | Modello ancora in caricamento | Attendi 30–60 s dopo l'avvio; modelli più grandi richiedono più tempo |
| `StatusCode: 404` su `/v1/health` | Porta errata | Default è `5273`. Verifica `foundry local status` per la porta effettiva |
| Risorse insufficienti | Foundry Local necessita di ~4 GB di RAM liberi | Chiudi altre applicazioni |
| Download modello fallito | Spazio su disco insufficiente | I modelli sono da 2 a 8 GB. Libera spazio, poi `foundry model pull <name>` |

### Incongruenza nome modello

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Imposta `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` sull'alias esatto mostrato (es., `phi-4-mini`, non `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` durante esecuzione locale (Percorso B)

Il laboratorio `main.py` usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local richiede che questa variabile punti al servizio locale - **non** a `AZURE_AI_PROJECT_ENDPOINT`. Assicurati che il tuo `.env` contenga:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Lo strumento MCP fa comunque una chiamata in uscita (Percorso B)

Questo è previsto. Lo strumento `search_microsoft_learn_for_plan` recupera risorse di apprendimento da `https://learn.microsoft.com/api/mcp`. **Solo la query del nome competenza** viaggia sulla rete - curriculum e testo JD sono processati interamente sul tuo dispositivo e mai trasmessi. Se è richiesta operatività completamente offline, aggiungi un fallback `try/except` nello strumento che ritorna un URL `learn.microsoft.com` statico quando l'endpoint è irraggiungibile.

---

## Come ottenere aiuto

Se sei bloccato dopo aver provato le correzioni sopra:

1. **Controlla i log del server** - La maggior parte degli errori produce una traccia dello stack Python nel terminale. Leggi l'intero traceback.
2. **Cerca il messaggio di errore** - Copia il testo dell'errore e cerca in [Microsoft Q&A per Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Apri una issue** - Apri una issue nel [repository del workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) con:
   - Il messaggio di errore o uno screenshot
   - Le versioni dei tuoi pacchetti (`pip list | Select-String "agent-framework"`)
   - La versione di Python (`python --version`)
   - Se il problema è locale o dopo la distribuzione

---

### Punto di controllo

- [ ] Sai come verificare e correggere problemi di configurazione `.env`
- [ ] Puoi verificare che le versioni dei pacchetti corrispondano alla matrice richiesta
- [ ] Sai come controllare i log del contenitore per errori di distribuzione
- [ ] Puoi verificare i ruoli RBAC nel portale Azure

---

**Precedente:** [07 - Verifica in Playground](07-verify-in-playground.md) · **Successivo:** [09 - Riepilogo →](09-summary.md) · **Home:** [Lab 02 README](../README.md) · [Home Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->