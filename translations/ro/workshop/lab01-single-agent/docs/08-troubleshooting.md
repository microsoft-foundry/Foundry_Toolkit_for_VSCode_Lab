# Modulul 8 - Depanare

Acest modul este un ghid de referință pentru probleme comune. Adaugă-l la favorite și revino când ceva nu merge bine.

---

## 1. Erori de permisiune

### 1.1 Permisiunea `agents/write` refuzată

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Cauza principală:** Lipsa rolului `Azure AI User` la nivel de **proiect**. Aceasta este eroarea #1 la atelier.

**Remediere:**
1. Deschide [portal.azure.com](https://portal.azure.com).
2. Caută numele proiectului tău Foundry → fă clic pe rezultatul de tip **"Proiect Microsoft Foundry"** (NU contul părinte).
3. **Control acces (IAM)** → **+ Adaugă** → **Adaugă atribuirea de rol**.
4. Rol: **Azure AI User** → Următorul.
5. Membri: Selectează-te pe tine → Revizuiește + atribuie → Revizuiește + atribuie.
6. **Așteaptă 1–2 minute** → încearcă din nou.

> **De ce rolurile Owner/Contributor nu sunt suficiente:** Aceste roluri acordă doar acțiuni de *management*. Operațiile agentului necesită acțiunea de *date* `agents/write`, care este prezentă doar în `Azure AI User`, `Azure AI Developer` sau `Azure AI Owner`. Vezi [documentația Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` în timpul aprovizionării

**Remediere:** Cere administratorului să-ți atribuie rolul de **Contributor** pe grupul de resurse sau să creeze el proiectul și să-ți acorde rolul **Azure AI User** pe acesta.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Așteptați până la: "Înregistrat"
```

---

## 2. Erori Docker

> Docker este **opțional**. Acestea se aplică doar dacă Docker Desktop este instalat și extensia încearcă o construire locală.

### 2.1 Daemon-ul Docker nu rulează

**Remediere:** Pornește Docker Desktop → așteaptă starea „running” → verifică cu `docker info` → încearcă din nou.

### 2.2 Construirea eșuează cu erori de dependențe

**Remediere:** Verifică scrierea corectă a `requirements.txt`, testează local mai întâi: `pip install -r requirements.txt`.

### 2.3 Neconcordanță platformă (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Erori de autentificare

### 3.1 `DefaultAzureCredential` eșuează

**Remediere (încearcă în această ordine):**
1. `az login` (reautentificare)
2. `az account set --subscription "<id>"` (setează abonamentul corect)
3. VS Code → Conturi → Deconectare → Autentificare din nou
4. Verifică: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Tokenul funcționează local, dar nu la găzduire

**Așteptat:** Agenții găzduiți folosesc identitatea administrată de sistem, nu credențialele tale. Dacă agentul găzduit primește erori de autentificare:
- Verifică dacă `AZURE_AI_PROJECT_ENDPOINT` din `agent.yaml` este corect
- Verifică că identitatea administrată a proiectului are acces la model

---

## 4. Erori model

### 4.1 Implementarea modelului nu este găsită

**Remediere:** Numele este **sensibil la majuscule/minuscule**. Compară `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` cu numele exact din bara laterală Foundry → Modele.

### 4.2 Ieșire neașteptată a modelului

**Remediere:** Revizuiește `AGENT_INSTRUCTIONS` în `main.py` (nu este trunchiat?). Încearcă un alt model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Erori de implementare

### 5.1 ACR pull neautorizat

**Remediere:** Azure Portal → Container Registry → Control acces (IAM) → Adaugă rolul **AcrPull** identității administrate a proiectului Foundry.

### 5.2 Agentul nu pornește (rămâne „Pending” sau „Failed”)

Verifică jurnalele containerului în bara laterală. Cauze comune:

| Mesaj jurnal | Remediere |
|-------------|-----------|
| `ModuleNotFoundError` | Adaugă pachetul lipsă în `requirements.txt`, reimplementează |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Adaugă variabila de mediu în `agent.yaml` sub `environment_variables` |
| `Address already in use` | Asigură-te că un singur proces folosește portul 8088 |

### 5.3 Timpul de implementare expiră

**Remediere:** Verifică conexiunea la internet. Prima implementare transferă >100MB. Ești în spatele unui proxy? Configurează setările proxy Docker Desktop.

---

## 6. Calea B - Foundry Local

### 6.1 Foundry Local nu pornește

| Problemă | Remediere |
|----------|-----------|
| `foundry: command not found` | Reinstalează: `winget install Microsoft.FoundryLocal` |
| Resurse insuficiente | Foundry Local necesită ~4GB RAM liber. Închide alte aplicații. |
| Descărcarea modelului eșuează | Verifică spațiul pe disc (modelele au 2–8 GB). Încearcă: `foundry local models pull <name>` |

### 6.2 Erori model Foundry Local

| Problemă | Remediere |
|----------|-----------|
| Răspunsuri lente | Normal - modelele locale rulează pe CPU dacă nu ai GPU. Fii răbdător. |
| Ieșire de calitate slabă | Încearcă un model mai mare dacă hardware-ul permite. `phi-4-mini` e un echilibru bun. |
| Conexiune refuzată | Verifică dacă Foundry Local rulează: `foundry local status`. Repornește dacă este nevoie. |

---

## 7. Referință rapidă: roluri RBAC

| Rol | Domeniu | Oferă |
|-----|---------|--------|
| **Azure AI User** | Proiect | Acțiuni pe date: `agents/write`, `agents/read` |
| **Azure AI Developer** | Proiect/Cont | Acțiuni pe date + creare proiect |
| **Azure AI Owner** | Cont | Acces complet + management roluri |
| **Contributor** | Abonament/GR | Doar acțiuni de management (**fără** acțiuni pe date) |
| **Owner** | Abonament/GR | Management + atribuiri roluri (**fără** acțiuni pe date) |

---

## 8. Lista de verificare a finalizării atelierului

| # | Element | Modul |
|---|---------|-------|
| 1 | Precondiții instalate și verificate | [00](00-prerequisites.md) |
| 2 | Extensia Foundry Toolkit instalată, proiect conectat (sau configurată Calea B) | [01](01-setup.md) |
| 3 | Agent găzduit creat | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurat, instrucțiuni scrise, dependențe instalate | [03](03-configure-and-code.md) |
| 5 | Agent testat local - 3 scenarii funcționale aprobate | [04](04-test-locally.md) |
| 6 | Implementat în Foundry (doar Calea A) | [05](05-deploy-to-foundry.md) |
| 7 | Teste de cazuri limită / siguranță aprobate în cloud (doar Calea A) | [06](06-verify-in-playground.md) |
| 8 | Rezumat revizuit, pași următori identificați | [07](07-summary.md) |

---

**Anterior:** [07 - Rezumat](07-summary.md) · **Acasă:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->