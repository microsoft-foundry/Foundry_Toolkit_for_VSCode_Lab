# Modulo 8 - Risoluzione dei problemi

Questo modulo è una guida di riferimento per ogni problema comune incontrato durante il workshop. Aggiungilo ai preferiti - ci tornerai ogni volta che qualcosa va storto.

---

## 1. Errori di autorizzazione

### 1.1 Permesso `agents/write` negato

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Causa principale:** Non hai il ruolo `Azure AI User` a livello di **progetto**. Questo è l'errore più comune nel workshop.

**Soluzione - passo dopo passo:**

1. Apri [https://portal.azure.com](https://portal.azure.com).
2. Nella barra di ricerca in alto, digita il nome del tuo **progetto Foundry** (es. `workshop-agents`).
3. **Critico:** Clicca il risultato che mostra il tipo **"Microsoft Foundry project"**, NON la risorsa padre account/hub. Si tratta di risorse differenti con ambiti RBAC differenti.
4. Nel menu di navigazione a sinistra della pagina del progetto, clicca **Controllo accessi (IAM)**.
5. Clicca sulla scheda **Assegnazioni ruoli** per verificare se hai già il ruolo:
   - Cerca il tuo nome o email.
   - Se `Azure AI User` è già elencato → l'errore ha una causa diversa (controlla il Passo 8 sotto).
   - Se non è elencato → procedi ad aggiungerlo.
6. Clicca **+ Aggiungi** → **Aggiungi assegnazione ruolo**.
7. Nella scheda **Ruolo**:
   - Cerca [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Selezionalo dai risultati.
   - Clicca **Avanti**.
8. Nella scheda **Membri**:
   - Seleziona **Utente, gruppo o service principal**.
   - Clicca **+ Seleziona membri**.
   - Cerca il tuo nome o indirizzo email.
   - Selezionati nei risultati.
   - Clicca **Seleziona**.
9. Clicca **Rivedi + assegna** → di nuovo **Rivedi + assegna**.
10. **Attendi 1-2 minuti** - le modifiche RBAC richiedono tempo per propagarsi.
11. Ritenta l'operazione che ha fallito.

> **Perché Owner/Contributor non basta:** Azure RBAC ha due tipi di permessi - *azioni di gestione* e *azioni dati*. Owner e Contributor concedono azioni di gestione (creare risorse, modificare impostazioni), ma le operazioni degli agenti richiedono l'**azione dati** `agents/write`, inclusa solo nei ruoli `Azure AI User`, `Azure AI Developer`, o `Azure AI Owner`. Vedi [documentazione RBAC Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante il provisioning della risorsa

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Causa principale:** Non hai permessi per creare o modificare risorse Azure in questa sottoscrizione/gruppo di risorse.

**Soluzione:**
1. Chiedi all'amministratore della sottoscrizione di assegnarti il ruolo **Contributor** sul gruppo di risorse dove vive il progetto Foundry.
2. In alternativa, chiedigli di creare il progetto Foundry per te e assegnarti **Azure AI User** sul progetto.

### 1.3 `SubscriptionNotRegistered` per [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Causa principale:** La sottoscrizione Azure non ha registrato il provider di risorse necessario per Foundry.

**Soluzione:**

1. Apri un terminale ed esegui:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Attendi che la registrazione sia completata (può richiedere 1-5 minuti):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Output atteso: `"Registered"`
3. Ritenta l'operazione.

---

## 2. Errori Docker (solo se Docker è installato)

> Docker è **opzionale** per questo workshop. Questi errori si applicano solo se hai installato Docker Desktop e l’estensione Foundry tenti una build container locale.

### 2.1 Il demone Docker non è in esecuzione

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Soluzione - passo dopo passo:**

1. **Trova Docker Desktop** nel menu Start (Windows) o nelle Applicazioni (macOS) e avvialo.
2. Attendi che la finestra di Docker Desktop mostri **"Docker Desktop is running"** - solitamente richiede 30-60 secondi.
3. Controlla l'icona della balena Docker nella system tray (Windows) o barra dei menu (macOS). Passa sopra con il mouse per confermare lo stato.
4. Verifica in un terminale:
   ```powershell
   docker info
   ```
   Se questo stampa informazioni di sistema di Docker (Server Version, Storage Driver, ecc.), Docker è in esecuzione.
5. **Solo Windows:** Se Docker non si avvia ancora:
   - Apri Docker Desktop → **Impostazioni** (icona ingranaggio) → **Generale**.
   - Assicurati che **Usa il motore basato su WSL 2** sia selezionato.
   - Clicca **Applica e riavvia**.
   - Se WSL 2 non è installato, esegui `wsl --install` da PowerShell con privilegi elevati e riavvia il pc.
6. Ritenta il deployment.

### 2.2 La build Docker fallisce con errori di dipendenze

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Soluzione:**
1. Apri `requirements.txt` e verifica che tutti i nomi dei pacchetti siano scritti correttamente.
2. Controlla che il fissaggio delle versioni sia corretto:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Testa prima l’installazione localmente:
   ```bash
   pip install -r requirements.txt
   ```
4. Se usi un indice pacchetti privato, assicurati che Docker abbia accesso di rete ad esso.

### 2.3 Incompatibilità piattaforma container (Apple Silicon)

Se esegui il deployment da un Mac Apple Silicon (M1/M2/M3/M4), il container deve essere buildato per `linux/amd64` perché il runtime container di Foundry usa AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Il comando di deploy dell’estensione Foundry gestisce automaticamente questo nella maggior parte dei casi. Se vedi errori correlati all’architettura, costruisci manualmente con il flag `--platform` e contatta il team Foundry.

---

## 3. Errori di autenticazione

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) fallisce nel recuperare un token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Causa principale:** Nessuna delle fonti di credenziali nella catena `DefaultAzureCredential` ha un token valido.

**Soluzione - prova ogni passo in ordine:**

1. **Riconnettiti via Azure CLI** (correzione più comune):
   ```bash
   az login
   ```
   Si apre una finestra del browser. Effettua l'accesso, poi torna in VS Code.

2. **Imposta la sottoscrizione corretta:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Se questa non è la sottoscrizione corretta:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Riconnettiti via VS Code:**
   - Clicca l'icona **Account** (icona persona) in basso a sinistra di VS Code.
   - Clicca il tuo nome account → **Esci**.
   - Clicca di nuovo l'icona Account → **Accedi a Microsoft**.
   - Completa il flusso di login nel browser.

4. **Service principal (solo scenari CI/CD):**
   - Imposta queste variabili d’ambiente nel tuo `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Poi riavvia il processo agente.

5. **Controlla la cache del token:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Se fallisce, il token CLI è scaduto. Esegui di nuovo `az login`.

### 3.2 Il token funziona localmente ma non nel deployment ospitato

**Causa principale:** L’agente ospitato usa un’identità gestita dal sistema, diversa dalla tua credenziale personale.

**Soluzione:** Questo comportamento è previsto - l’identità gestita viene creata automaticamente durante il deployment. Se l’agente ospitato riceve ancora errori di autenticazione:
1. Controlla che l’identità gestita del progetto Foundry abbia accesso alla risorsa Azure OpenAI.
2. Verifica che `PROJECT_ENDPOINT` in `agent.yaml` sia corretto.

---

## 4. Errori del modello

### 4.1 Deploy del modello non trovato

```
Error: Model deployment not found / The specified deployment does not exist
```

**Soluzione - passo dopo passo:**

1. Apri il file `.env` e annota il valore di `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Apri la sidebar **Microsoft Foundry** in VS Code.
3. Espandi il tuo progetto → **Model Deployments**.
4. Confronta il nome del deployment elencato con quello nel tuo `.env`.
5. Il nome è **case-sensitive** - `gpt-4o` è diverso da `GPT-4o`.
6. Se non corrispondono, aggiorna il tuo `.env` per usare il nome esatto mostrato nella sidebar.
7. Per deployment ospitato, aggiorna anche `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Il modello risponde con contenuto inatteso

**Soluzione:**
1. Rivedi la costante `EXECUTIVE_AGENT_INSTRUCTIONS` in `main.py`. Assicurati che non sia stata troncata o corrotta.
2. Controlla la temperatura del modello (se configurabile) - valori più bassi danno output più deterministici.
3. Confronta il modello deployato (es. `gpt-4o` vs `gpt-4o-mini`) - modelli diversi hanno capacità diverse.

---

## 5. Errori di deployment

### 5.1 Autorizzazione pull ACR

```
Error: AcrPullUnauthorized
```

**Causa principale:** L’identità gestita del progetto Foundry non può scaricare l’immagine container da Azure Container Registry.

**Soluzione - passo dopo passo:**

1. Apri [https://portal.azure.com](https://portal.azure.com).
2. Cerca **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** nella barra di ricerca in alto.
3. Clicca sul registro associato al tuo progetto Foundry (di solito nello stesso gruppo di risorse).
4. Nel menu a sinistra, clicca **Controllo accessi (IAM)**.
5. Clicca **+ Aggiungi** → **Aggiungi assegnazione ruolo**.
6. Cerca **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** e selezionalo. Clicca **Avanti**.
7. Seleziona **Identità gestita** → clicca **+ Seleziona membri**.
8. Trova e seleziona l’identità gestita del progetto Foundry.
9. Clicca **Seleziona** → **Rivedi + assegna** → **Rivedi + assegna**.

> Questa assegnazione ruolo viene normalmente configurata automaticamente dall’estensione Foundry. Se vedi questo errore, la configurazione automatica potrebbe essere fallita. Puoi provare anche a ridistribuire - l’estensione può ritentare la configurazione.

### 5.2 L’agente non si avvia dopo il deployment

**Sintomi:** Lo stato del container resta "Pending" per più di 5 minuti o mostra "Failed".

**Soluzione - passo dopo passo:**

1. Apri la sidebar **Microsoft Foundry** in VS Code.
2. Clicca sul tuo agente ospitato → seleziona la versione.
3. Nel pannello dettagli, controlla **Dettagli Container** → cerca una sezione o un link **Logs**.
4. Leggi i log di avvio del container. Cause comuni:

| Messaggio di log | Causa | Soluzione |
|------------------|--------|-----------|
| `ModuleNotFoundError: No module named 'xxx'` | Dipendenza mancante | Aggiungila in `requirements.txt` e ridistribuisci |
| `KeyError: 'PROJECT_ENDPOINT'` | Variabile ambiente mancante | Aggiungi la variabile in `agent.yaml` sotto `env:` |
| `OSError: [Errno 98] Address already in use` | Conflitto di porta | Assicurati che `agent.yaml` abbia `port: 8088` e che solo un processo la usi |
| `ConnectionRefusedError` | Agente non ha iniziato l’ascolto | Controlla `main.py` - la chiamata `from_agent_framework()` deve essere eseguita all’avvio |

5. Risolvi il problema, poi ridistribuisci dal [Modulo 6](06-deploy-to-foundry.md).

### 5.3 Il deployment scade

**Soluzione:**
1. Controlla la tua connessione internet - il push Docker può essere grande (>100MB per il primo deploy).
2. Se sei dietro a un proxy aziendale, assicurati che le impostazioni proxy di Docker Desktop siano configurate: **Docker Desktop** → **Impostazioni** → **Risorse** → **Proxy**.
3. Riprova - interruzioni di rete possono causare errori temporanei.

---

## 6. Riferimento rapido: ruoli RBAC

| Ruolo | Ambito tipico | Cosa concede |
|-------|---------------|--------------|
| **Azure AI User** | Progetto | Azioni dati: build, deploy e invocazione agenti (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Progetto o Account | Azioni dati + creazione progetto |
| **Azure AI Owner** | Account | Accesso completo + gestione assegnazione ruoli |
| **Azure AI Project Manager** | Progetto | Azioni dati + può assegnare Azure AI User ad altri |
| **Contributor** | Sottoscrizione/RG | Azioni gestione (crea/elimina risorse). **NON include azioni dati** |
| **Owner** | Sottoscrizione/RG | Azioni gestione + assegnazione ruoli. **NON include azioni dati** |
| **Reader** | Qualsiasi | Accesso sola lettura gestione |

> **Conclusione chiave:** `Owner` e `Contributor` non includono azioni dati. Per operazioni agenti serve sempre un ruolo `Azure AI *`. Il ruolo minimo per questo workshop è **Azure AI User** a livello **progetto**.

---

## 7. Checklist completamento workshop

Usala come conferma finale che hai completato tutto:

| # | Elemento | Modulo | Superato? |
|---|----------|--------|-----------|
| 1 | Tutti i prerequisiti installati e verificati | [00](00-prerequisites.md) | |
| 2 | Toolkit Foundry ed estensioni Foundry installati | [01](01-install-foundry-toolkit.md) | |
| 3 | Progetto Foundry creato (o progetto esistente selezionato) | [02](02-create-foundry-project.md) | |
| 4 | Modello distribuito (es. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Ruolo utente Azure AI assegnato a livello di progetto | [02](02-create-foundry-project.md) | |
| 6 | Progetto agente ospitato scaffolding (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` configurato con PROJECT_ENDPOINT e MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Istruzioni dell'agente personalizzate in main.py | [04](04-configure-and-code.md) | |
| 9 | Ambiente virtuale creato e dipendenze installate | [04](04-configure-and-code.md) | |
| 10 | Agente testato localmente con F5 o terminale (4 test di fumo superati) | [05](05-test-locally.md) | |
| 11 | Distribuito al Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Stato del contenitore mostra "Started" o "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verificato in VS Code Playground (4 test di fumo superati) | [07](07-verify-in-playground.md) | |
| 14 | Verificato in Foundry Portal Playground (4 test di fumo superati) | [07](07-verify-in-playground.md) | |

> **Congratulazioni!** Se tutti gli elementi sono spuntati, hai completato l’intero workshop. Hai creato un agente ospitato da zero, lo hai testato localmente, lo hai distribuito su Microsoft Foundry e lo hai convalidato in produzione.

---

**Precedente:** [07 - Verifica nel Playground](07-verify-in-playground.md) · **Home:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Pur impegnandoci per l'accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o inesattezze. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale umana. Non ci assumiamo alcuna responsabilità per incomprensioni o interpretazioni errate derivanti dall'uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->