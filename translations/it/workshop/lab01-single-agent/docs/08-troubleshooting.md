# Modulo 8 - Risoluzione dei problemi

Questo modulo è una guida di riferimento per problemi comuni. Aggiungilo ai preferiti e torna quando qualcosa va storto.

---

## 1. Errori di autorizzazione

### 1.1 `agents/write` permesso negato

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Causa principale:** Ruolo `Azure AI User` mancante a livello del **progetto**. Questo è l'errore più frequente nei workshop.

**Soluzione:**
1. Apri [portal.azure.com](https://portal.azure.com).
2. Cerca il nome del tuo **progetto** Foundry → clicca il risultato di tipo **"Microsoft Foundry project"** (NON l'account principale).
3. **Controllo accessi (IAM)** → **+ Aggiungi** → **Aggiungi assegnazione ruolo**.
4. Ruolo: **Azure AI User** → Avanti.
5. Membri: Selezionati te stesso → Rivedi + assegna → Rivedi + assegna.
6. **Attendi 1–2 minuti** → riprova.

> **Perché Owner/Contributor non basta:** Questi ruoli concedono solo azioni di *gestione*. Le operazioni dell'agente richiedono `agents/write` *azione dati*, presente solo in `Azure AI User`, `Azure AI Developer` o `Azure AI Owner`. Vedi [documentazione RBAC Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante il provisioning

**Soluzione:** Chiedi al tuo amministratore di assegnarti il ruolo **Contributor** sul gruppo di risorse, oppure di creare il progetto per te e concederti il ruolo **Azure AI User** su di esso.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Errori Docker

> Docker è **opzionale**. Questi errori si applicano solo se Docker Desktop è installato e l'estensione tenta una build locale.

### 2.1 Demone Docker non in esecuzione

**Soluzione:** Avvia Docker Desktop → attendi lo stato "in esecuzione" → verifica con `docker info` → riprova.

### 2.2 La build fallisce con errori di dipendenze

**Soluzione:** Verifica l'ortografia di `requirements.txt`, testa prima in locale: `pip install -r requirements.txt`.

### 2.3 Incompatibilità piattaforma (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Errori di autenticazione

### 3.1 `DefaultAzureCredential` fallisce

**Soluzione (prova in ordine):**
1. `az login` (ri-autenticarsi)
2. `az account set --subscription "<id>"` (sottoscrizione corretta)
3. VS Code → Account → Disconnetti → Riconnettiti
4. Verifica: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Il token funziona in locale ma non in hosting

**Aspettativa:** Gli agenti ospitati usano un'identità gestita di sistema, non la tua credenziale. Se l'agente ospitato riceve errori di autenticazione:
- Verifica che `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `agent.yaml` corrisponda al nome del tuo modello distribuito (`FOUNDRY_PROJECT_ENDPOINT` è inserito da Foundry a runtime - non dichiararlo in `agent.yaml`)
- Controlla che l'identità gestita del progetto abbia accesso al modello

---

## 4. Errori del modello

### 4.1 Distribuzione del modello non trovata

**Soluzione:** Il nome è **case-sensitive**. Confronta `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` con il nome esatto nella barra laterale di Foundry → Modelli.

### 4.2 Output imprevisto del modello

**Soluzione:** Controlla `AGENT_INSTRUCTIONS` in `main.py` (non è troncato?). Prova un modello differente (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Errori di distribuzione

### 5.1 Autorizzazione ACR negata

**Soluzione:** Azure Portal → Container Registry → Controllo accessi (IAM) → Aggiungi ruolo **AcrPull** all'identità gestita del progetto Foundry.

### 5.2 L'agente fallisce l'avvio (rimane in "Pending" o "Failed")

Controlla i log del container nella barra laterale. Cause comuni:

| Messaggio di log | Soluzione |
|-------------|-----|
| `ModuleNotFoundError` | Aggiungi il pacchetto mancante a `requirements.txt`, ridistribuisci |
| `ValueError: Missing required environment variables` | Conferma che `AZURE_AI_MODEL_DEPLOYMENT_NAME` sia dichiarato in `agent.yaml` sotto `environment_variables` e abbia un valore, poi ridistribuisci. `FOUNDRY_PROJECT_ENDPOINT` è inserito da Foundry a runtime |
| `Address already in use` | Assicurati che solo un processo si leghi alla porta 8088 |

### 5.3 Timeout durante la distribuzione

**Soluzione:** Verifica la connessione internet. Il primo deploy trasferisce >100MB. Sei dietro un proxy? Configura le impostazioni proxy di Docker Desktop.

---

## 6. Percorso B - Foundry Local

### 6.1 Foundry Local non parte

| Problema | Soluzione |
|-------|-----|
| `foundry: command not found` | Reinstalla: `winget install Microsoft.FoundryLocal` |
| Risorse insufficienti | Foundry Local richiede ~4GB di RAM libera. Chiudi altre app. |
| Download modello fallito | Controlla spazio su disco (i modelli sono da 2 a 8 GB). Riprova: `foundry local models pull <name>` |

### 6.2 Errori modello in Foundry Local

| Problema | Soluzione |
|-------|-----|
| Risposte lente | Normale - i modelli locali girano su CPU a meno che non hai una GPU. Abbi pazienza. |
| Output di scarsa qualità | Prova un modello più grande se il tuo hardware lo consente. `phi-4-mini` è un buon compromesso. |
| Connessione rifiutata | Verifica che Foundry Local sia attivo: `foundry local status`. Riavvia se necessario. |

---

## 7. Riferimento rapido: ruoli RBAC

| Ruolo | Ambito | Concede |
|------|-------|--------|
| **Azure AI User** | Progetto | Azioni dati: `agents/write`, `agents/read` |
| **Azure AI Developer** | Progetto/Account | Azioni dati + creazione progetto |
| **Azure AI Owner** | Account | Accesso completo + gestione ruoli |
| **Contributor** | Sottoscrizione/Gruppo risorse | Solo azioni di gestione (**no** azioni dati) |
| **Owner** | Sottoscrizione/Gruppo risorse | Gestione + assegnazione ruoli (**no** azioni dati) |

---

## 8. Checklist di completamento workshop

| # | Elemento | Modulo |
|---|------|--------|
| 1 | Prerequisiti installati e verificati | [00](00-prerequisites.md) |
| 2 | Estensione Foundry Toolkit installata, progetto collegato (o Percorso B configurato) | [01](01-setup.md) |
| 3 | Agente ospitato strutturato | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurato, istruzioni scritte, dipendenze installate | [03](03-configure-and-code.md) |
| 5 | Agente testato localmente - 3 scenari funzionali superati | [04](04-test-locally.md) |
| 6 | Distribuito in Foundry (solo Percorso A) | [05](05-deploy-to-foundry.md) |
| 7 | Test edge-case/sicurezza superati nel cloud (solo Percorso A) | [06](06-verify-in-playground.md) |
| 8 | Riepilogo esaminato, prossimi passi identificati | [07](07-summary.md) |

---

**Precedente:** [07 - Riepilogo](07-summary.md) · **Home:** [README Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->