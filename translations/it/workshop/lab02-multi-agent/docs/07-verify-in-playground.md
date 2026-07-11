# Modulo 7 - Verifica nel Playground

⏱️ ~10 min

In questo modulo, testerai il tuo flusso di lavoro multi-agente distribuito in VS Code e nel Foundry Portal, confermando che l'agente si comporta allo stesso modo dei test locali.

---

## Perché testare di nuovo dopo il deployment?

L'ambiente ospitato differisce da quello locale in alcuni aspetti importanti:

| | Locale | Ospitato |
|--|-------|--------|
| **Identità** | Il tuo accesso personale (`DefaultAzureCredential`) | Identità Entra dedicata per agente (auto-provisionata al momento del deployment) |
| **Endpoint** | `http://localhost:8088/responses` | URL gestito dal Foundry Agent Service |
| **Rete** | La tua macchina → Azure OpenAI + MCP | Backbone Azure (minore latenza) |

Una variabile d'ambiente mal configurata, un problema RBAC, o una chiamata MCP in uscita bloccata si manifesterebbero qui per primi.

---

## Opzione A: Test nel Playground di VS Code (consigliato come primo)

### Passo 1: Naviga al tuo agente ospitato

1. Clicca sull'icona **Foundry Toolkit** nella Barra delle Attività.
2. Espandi il tuo progetto → **Hosted Agents (Preview)** → trova il tuo agente.

![Barra laterale Foundry Toolkit che mostra Hosted Agents (Preview) con resume-job-fit-evaluator e le sue versioni distribuite](../../../../../translated_images/it/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Passo 2: Seleziona una versione

1. Clicca sull'agente per espandere le sue versioni.
2. Clicca su `v1` → verifica che lo stato sia **attivo** (la barra laterale potrebbe mostrare "Running" o "Started" - entrambi indicano lo stato pronto).

### Passo 3: Apri il Playground

1. Clicca **Playground** (oppure clic destro sulla versione → **Open in Playground**).
2. Si apre una finestra di chat in una scheda di VS Code.

### Passo 4: Esegui i test di base

Usa gli stessi 3 test del [Modulo 5](05-test-locally.md). Digita ogni messaggio nella casella di input del Playground e premi **Invia** (o **Enter**).

#### Test 1 - Resume completo + JD (flusso standard)

Incolla il prompt completo resume + JD dal Modulo 5, Test 1 (Jane Doe + Senior Cloud Engineer presso Contoso Ltd).

**Atteso:**
- Punteggio di idoneità con calcolo dettagliato (scala di 100 punti)
- Sezione Competenze abbinate
- Sezione Competenze mancanti
- **Una scheda gap per ogni competenza mancante** con URL di Microsoft Learn
- Roadmap di apprendimento con timeline

#### Test 2 - Test breve rapido (input minimo)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Atteso:**
- Punteggio di idoneità più basso (< 40)
- Valutazione onesta con percorso di apprendimento graduale
- Multiple schede gap (AWS, Kubernetes, Terraform, CI/CD, gap di esperienza)

#### Test 3 - Candidato con alta idoneità

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Atteso:**
- Punteggio di idoneità alto (≥ 80)
- Focus sulla preparazione al colloquio e affinamento
- Poche o nessuna scheda gap
- Timeline breve concentrata sulla preparazione

### Passo 5: Confronta con i risultati locali

Apri le tue note o la scheda del browser dal Modulo 5 dove hai salvato le risposte locali. Per ogni test:

- La risposta ha la **stessa struttura** (punteggio di idoneità, schede gap, roadmap)?
- Segue la **lista di criteri di valutazione identica** (scomposizione su scala di 100)?
- Sono ancora presenti gli **URL di Microsoft Learn** nelle schede gap?
- C'è **una scheda gap per ogni competenza mancante** (non troncata)?

> **Differenze minori nella formulazione sono normali** - il modello è non deterministico. Concentrati sulla struttura, coerenza della punteggiatura e uso dello strumento MCP.

---

## Opzione B: Test nel Foundry Portal

Il [Foundry Portal](https://ai.azure.com) offre un playground basato sul web utile per condividere con colleghi o stakeholder.

### Passo 1: Apri il Foundry Portal

1. Apri il browser e vai su [https://ai.azure.com](https://ai.azure.com).
2. Accedi con lo stesso account Azure che hai usato durante tutto il workshop.

### Passo 2: Naviga al tuo progetto

1. Nella home page, cerca **Progetti recenti** nella barra laterale sinistra.
2. Clicca il nome del tuo progetto (ad esempio, `workshop-agents`).
3. Se non lo vedi, clicca **Tutti i progetti** e cercalo.

### Passo 3: Trova il tuo agente distribuito

1. Nel menu di navigazione sinistro del progetto, clicca **Build** → **Agents** (o cerca la sezione **Agents**).
2. Dovresti vedere una lista di agenti. Trova il tuo agente distribuito (es. `resume-job-fit-evaluator`).
3. Clicca sul nome dell'agente per aprire la pagina di dettaglio.

### Passo 4: Apri il Playground

1. Nella pagina di dettaglio dell'agente, guarda la barra degli strumenti in alto.
2. Clicca **Apri nel playground** (o **Prova nel playground**).
3. Si apre un'interfaccia di chat.

### Passo 5: Esegui gli stessi test di base

Ripeti tutti e 3 i test dalla sezione Playground di VS Code sopra. Confronta ogni risposta con i risultati locali (Modulo 5) e quelli nel Playground di VS Code (Opzione A sopra).

---

## Verifica specifica per multi-agente

Oltre alla correttezza di base, verifica questi comportamenti specifici multi-agente:

### Esecuzione dello strumento MCP

| Controllo | Come verificare | Condizione di passaggio |
|-------|---------------|----------------|
| Le chiamate MCP riescono | Le schede gap contengono URL `learn.microsoft.com` | URL reali, non messaggi di fallback |
| Multiple chiamate MCP | Ogni gap a Priorità Alta/Media ha risorse | Non solo la prima scheda gap |
| Fallback MCP funziona | Se mancano URL, verificare testo fallback | L'agente produce comunque schede gap (con o senza URL) |

### Coordinamento degli agenti

| Controllo | Come verificare | Condizione di passaggio |
|-------|---------------|----------------|
| Tutti e 4 gli agenti sono stati eseguiti | L'output contiene punteggio di idoneità E schede gap | Il punteggio viene da MatchingAgent, le schede da GapAnalyzer |
| Esecuzione sequenziale | Il tempo di risposta è ragionevole (< 2 min) | Se > 3 min, controllare errori nel log terminale |
| Integrità del flusso dati | Le schede gap fanno riferimento a competenze nel report di matching | Nessuna competenza inventata che non sia nel JD |

---

## Rubrica di validazione

Usa questa rubrica per valutare il comportamento ospitato del tuo flusso di lavoro multi-agente:

| # | Criteri | Condizione di passaggio | Passato? |
|---|----------|---------------|-------|
| 1 | **Correttezza funzionale** | L'agente risponde a resume + JD con punteggio di idoneità e analisi gap | |
| 2 | **Coerenza della punteggiatura** | Il punteggio usa scala a 100 punti con calcolo dettagliato | |
| 3 | **Completezza schede gap** | Una scheda per ogni competenza mancante (non troncata o combinata) | |
| 4 | **Integrazione strumento MCP** | Le schede gap includono URL reali di Microsoft Learn | |
| 5 | **Coerenza strutturale** | La struttura dell'output corrisponde tra esecuzioni locali e ospitate | |
| 6 | **Tempo di risposta** | L'agente ospitato risponde entro 2 minuti per la valutazione completa | |
| 7 | **Nessun errore** | Nessun errore HTTP 500, timeout o risposte vuote | |

> Un "pass" significa che tutti e 7 i criteri sono soddisfatti per tutti e 3 i test di base in almeno un playground (VS Code o Portal).

---

## Risoluzione problemi nel playground

| Sintomo | Probabile causa | Soluzione |
|---------|-------------|-----|
| Il playground non si carica | Il container non è in stato `active` | Torna al [Modulo 6](06-deploy-to-foundry.md), verifica lo stato del deployment. Attendi se è in stato `creating` |
| L'agente restituisce risposta vuota | Nome del deployment del modello non corrispondente | Controlla `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` corrisponde al modello distribuito |
| L'agente restituisce messaggio di errore | Mancano permessi [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Assegna **[Foundry User](https://aka.ms/foundry-ext-project-role)** (precedentemente Azure AI User) nell'ambito del progetto |
| Assenza di URL Microsoft Learn nelle schede gap | MCP in uscita bloccato o server MCP non disponibile | Controlla se il container può raggiungere `learn.microsoft.com`. Vedi [Modulo 8](08-troubleshooting.md) |
| Solo 1 scheda gap (troncata) | Istruzioni GapAnalyzer mancano del blocco "CRITICAL" | Rivedi [Modulo 3, Passo 2.4](03-configure-agents.md) |
| Il punteggio di idoneità è molto diverso dal locale | Modello o istruzioni diversi distribuiti | Confronta le variabili d'ambiente in `agent.yaml` con il locale `.env`. Ridistribuisci se necessario |
| "Agente non trovato" nel Portal | Il deployment è ancora in propagazione o è fallito | Attendi 2 minuti, aggiorna. Se manca ancora, ridistribuisci dal [Modulo 6](06-deploy-to-foundry.md) |

---

### Checkpoint

- [ ] Testato l'agente nel Playground di VS Code - tutti e 3 i test di base superati
- [ ] Testato l'agente nel Playground del [Foundry Portal](https://ai.azure.com) - tutti e 3 i test di base superati
- [ ] Le risposte sono strutturalmente coerenti con i test locali (punteggio di idoneità, schede gap, roadmap)
- [ ] Gli URL Microsoft Learn sono presenti nelle schede gap (funzionamento dello strumento MCP in ambiente ospitato)
- [ ] Una scheda gap per ogni competenza mancante (nessuna troncatura)
- [ ] Nessun errore o timeout durante i test
- [ ] Rubrica di validazione completata (tutti e 7 i criteri superati)

---

**Precedente:** [06 - Deploy to Foundry](06-deploy-to-foundry.md) · **Successivo:** [08 - Risoluzione problemi →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->