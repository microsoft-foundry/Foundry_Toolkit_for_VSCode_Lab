# Modulul 8 - Depanare

Acest modul este un ghid de referință pentru fiecare problemă comună întâlnită în timpul atelierului. Adaugă-l la favorite - te vei întoarce la el ori de câte ori ceva nu merge bine.

---

## 1. Erori de permisiuni

### 1.1 Permisiunea `agents/write` negată

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Cauza principală:** Nu ai rolul `Azure AI User` la nivelul **proiectului**. Aceasta este cea mai frecventă eroare întâlnită în atelier.

**Remediere - pas cu pas:**

1. Deschide [https://portal.azure.com](https://portal.azure.com).
2. În bara de căutare din partea de sus, tastează numele **proiectului Foundry** (de exemplu, `workshop-agents`).
3. **Critic:** Apasă pe rezultatul care arată tipul **"Microsoft Foundry project"**, NU contul/punctul central parental. Acestea sunt resurse diferite cu domenii RBAC diferite.
4. În navigarea din stânga a paginii proiectului, apasă pe **Control acces (IAM)**.
5. Apasă pe fila **Atribuiri rol** pentru a verifica dacă ai deja rolul:
   - Caută-ți numele sau adresa de email.
   - Dacă `Azure AI User` este deja listat → eroarea are o cauză diferită (verifică Pasul 8 mai jos).
   - Dacă nu este listat → continuă pentru a-l adăuga.
6. Apasă **+ Adaugă** → **Adaugă atribuire de rol**.
7. În fila **Rol**:
   - Caută [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Selectează-l din rezultate.
   - Apasă **Următorul**.
8. În fila **Membri**:
   - Selectează **Utilizator, grup sau principal de serviciu**.
   - Apasă **+ Selectează membri**.
   - Caută-ți numele sau adresa de email.
   - Selectează-te din rezultate.
   - Apasă **Selectează**.
9. Apasă **Revizuiește + atribuie** → **Revizuiește + atribuie** din nou.
10. **Așteaptă 1-2 minute** - modificările RBAC necesită timp pentru propagare.
11. Încearcă din nou operația care a eșuat.

> **De ce Owner/Contributor nu este suficient:** Azure RBAC are două tipuri de permisiuni - *acțiuni de management* și *acțiuni de date*. Owner și Contributor acordă acțiuni de management (creare resurse, editare setări), dar operațiunile agentului cer acțiunea de date `agents/write`, care este inclusă doar în rolurile `Azure AI User`, `Azure AI Developer` sau `Azure AI Owner`. Vezi [documentația Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` în timpul aprovizionării resursei

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Cauza principală:** Nu ai permisiunea să creezi sau să modifici resurse Azure în acest abonament/grup de resurse.

**Remediere:**
1. Cere administratorului abonamentului să-ți atribuie rolul **Contributor** pe grupul de resurse unde se află proiectul Foundry.
2. Alternativ, cere să creeze proiectul Foundry pentru tine și să-ți acorde rolul **Azure AI User** pe proiect.

### 1.3 `SubscriptionNotRegistered` pentru [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Cauza principală:** Abonamentul Azure nu s-a înregistrat la furnizorul de resurse necesar pentru Foundry.

**Remediere:**

1. Deschide un terminal și execută:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Așteaptă finalizarea înregistrării (poate dura 1-5 minute):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Output-ul așteptat: `"Registered"`
3. Încearcă din nou operația.

---

## 2. Erori Docker (doar dacă Docker este instalat)

> Docker este **opțional** pentru acest atelier. Aceste erori se aplică doar dacă ai instalat Docker Desktop și extensia Foundry încearcă o construire locală a containerului.

### 2.1 Demonul Docker nu rulează

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Remediere - pas cu pas:**

1. **Găsește Docker Desktop** în meniul Start (Windows) sau în Aplicații (macOS) și deschide-l.
2. Așteaptă ca fereastra Docker Desktop să afișeze **"Docker Desktop este în funcțiune"** - de obicei durează 30-60 secunde.
3. Caută iconița balenă Docker în bara de sistem (Windows) sau bara de meniu (macOS). Plasează cursorul deasupra pentru a confirma statusul.
4. Verifică într-un terminal:
   ```powershell
   docker info
   ```
   Dacă afișează informații despre sistemul Docker (versiune server, driver stocare etc.), Docker este pornit.
5. **Specific Windows:** Dacă Docker tot nu pornește:
   - Deschide Docker Desktop → **Setări** (iconiță rotiță) → **General**.
   - Asigură-te că este bifată opțiunea **Use the WSL 2 based engine**.
   - Apasă **Aplică & repornește**.
   - Dacă WSL 2 nu este instalat, execută `wsl --install` într-un PowerShell cu drepturi de admin și repornește calculatorul.
6. Încearcă din nou să faci deploy.

### 2.2 Construirea Docker eșuează cu erori de dependențe

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Remediere:**
1. Deschide `requirements.txt` și verifică dacă toate numele pachetelor sunt corect scrise.
2. Asigură-te că versiunea fixată este corectă:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Testează instalarea local:
   ```bash
   pip install -r requirements.txt
   ```
4. Dacă folosești un index privat de pachete, asigură-te că Docker are acces la rețea către acesta.

### 2.3 Neconcordanța platformei containerului (Apple Silicon)

Dacă faci deploy de pe un Mac Apple Silicon (M1/M2/M3/M4), containerul trebuie să fie construit pentru `linux/amd64` deoarece runtime-ul container al Foundry folosește AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Comanda de deploy a extensiei Foundry gestionează asta automat în majoritatea cazurilor. Dacă vezi erori legate de arhitectură, construiește manual cu flag-ul `--platform` și contactează echipa Foundry.

---

## 3. Erori de autentificare

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) nu reușește să recupereze un token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Cauza principală:** Niciuna dintre sursele de acreditări din lanțul `DefaultAzureCredential` nu are un token valid.

**Remediere - încearcă fiecare pas în ordine:**

1. **Reautentificare prin Azure CLI** (cea mai comună soluție):
   ```bash
   az login
   ```
   Se va deschide o fereastră de browser. Autentifică-te, apoi revino în VS Code.

2. **Setează abonamentul corect:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Dacă nu este abonamentul dorit:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Reautentificare prin VS Code:**
   - Apasă iconița **Accounts** (persoană) din colțul stânga-jos al VS Code.
   - Apasă pe numele contului → **Deconectare**.
   - Apasă din nou pe iconița Accounts → **Autentificare la Microsoft**.
   - Urmează fluxul de autentificare în browser.

4. **Principal de serviciu (doar pentru scenarii CI/CD):**
   - Setează variabilele de mediu în `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Apoi repornește procesul agentului.

5. **Verifică cache-ul de tokenuri:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Dacă eșuează, tokenul CLI a expirat. Rulează din nou `az login`.

### 3.2 Tokenul funcționează local, dar nu în mediul găzduit

**Cauza principală:** Agentul găzduit folosește o identitate gestionată de sistem, care este diferită de acreditarea ta personală.

**Remediere:** Acest comportament este așteptat - identitatea gestionată este aprovizionată automat în timpul deploy-ului. Dacă agentul găzduit primește în continuare erori de autentificare:
1. Verifică dacă identitatea gestionată a proiectului Foundry are acces la resursa Azure OpenAI.
2. Verifică că `PROJECT_ENDPOINT` din `agent.yaml` este corect.

---

## 4. Erori ale modelului

### 4.1 Implementarea modelului nu este găsită

```
Error: Model deployment not found / The specified deployment does not exist
```

**Remediere - pas cu pas:**

1. Deschide fișierul `.env` și notează valoarea lui `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Deschide panoul lateral **Microsoft Foundry** în VS Code.
3. Extinde proiectul → **Implementări Model**.
4. Compară numele implementării listat acolo cu valoarea din `.env`.
5. Numele este **sensibil la majuscule/minuscule** - `gpt-4o` este diferit de `GPT-4o`.
6. Dacă nu se potrivesc, actualizează `.env` pentru a folosi exact numele afișat în sidebar.
7. Pentru deploy găzduit, actualizează și `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modelul răspunde cu conținut neașteptat

**Remediere:**
1. Revizuiește constanta `EXECUTIVE_AGENT_INSTRUCTIONS` din `main.py`. Asigură-te că nu este trunchiată sau coruptă.
2. Verifică setarea temperaturii modelului (dacă este configurabilă) - valori mai mici dau outputuri mai deterministe.
3. Compară modelul implementat (ex. `gpt-4o` vs `gpt-4o-mini`) - modelele diferite au capabilități diferite.

---

## 5. Erori la implementare

### 5.1 Autorizare la extragerea imaginii din ACR

```
Error: AcrPullUnauthorized
```

**Cauza principală:** Identitatea gestionată a proiectului Foundry nu poate extrage imaginea container din Azure Container Registry.

**Remediere - pas cu pas:**

1. Deschide [https://portal.azure.com](https://portal.azure.com).
2. Caută **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** în bara de căutare de sus.
3. Apasă pe registrul asociat proiectului Foundry (de obicei în același grup de resurse).
4. În navigarea din stânga, apasă **Control acces (IAM)**.
5. Apasă **+ Adaugă** → **Adaugă atribuire de rol**.
6. Caută și selectează **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Apasă **Următorul**.
7. Selectează **Identitate gestionată** → apasă **+ Selectează membri**.
8. Găsește și selectează identitatea gestionată a proiectului Foundry.
9. Apasă **Selectează** → **Revizuiește + atribuie** → **Revizuiește + atribuie**.

> Această atribuție de rol este de obicei configurată automat de extensia Foundry. Dacă vezi această eroare, configurarea automată a eșuat. Poți încerca să redeploiezi - extensia poate încerca din nou configurarea.

### 5.2 Agentul nu pornește după implementare

**Simptome:** Starea containerului rămâne "Pending" mai mult de 5 minute sau afișează "Failed".

**Remediere - pas cu pas:**

1. Deschide panoul lateral **Microsoft Foundry** în VS Code.
2. Apasă pe agentul găzduit → selectează versiunea.
3. În panoul de detalii, verifică **Detalii Container** → caută o secțiune sau link către **Jurnale**.
4. Citește jurnalele de pornire ale containerului. Cauze comune:

| Mesaj din jurnal | Cauză | Remediere |
|------------------|-------|-----------|
| `ModuleNotFoundError: No module named 'xxx'` | Dependență lipsă | Adaugă în `requirements.txt` și redeploiează |
| `KeyError: 'PROJECT_ENDPOINT'` | Variabilă de mediu lipsă | Adaugă variabila de mediu în `agent.yaml` sub `env:` |
| `OSError: [Errno 98] Address already in use` | Conflict port | Asigură-te că în `agent.yaml` este `port: 8088` și numai un proces ascultă pe acest port |
| `ConnectionRefusedError` | Agentul nu a început să asculte | Verifică în `main.py` - apelul `from_agent_framework()` trebuie să ruleze la pornire |

5. Remediază problema, apoi redeploiează folosind [Modulul 6](06-deploy-to-foundry.md).

### 5.3 Deploy-ul expiră ca timp

**Remediere:**
1. Verifică conexiunea ta la internet - push-ul Docker poate fi mare (>100MB la primul deploy).
2. Dacă ești în spatele unui proxy corporate, asigură-te că setările proxy din Docker Desktop sunt configurate: **Docker Desktop** → **Setări** → **Resurse** → **Proxy-uri**.
3. Încearcă din nou - întreruperile de rețea pot cauza eșecuri temporare.

---

## 6. Referință rapidă: roluri RBAC

| Rol | Domeniu tipic | Ce oferă |
|------|---------------|----------|
| **Azure AI User** | Proiect | Acțiuni de date: construire, deploy și invocare agenți (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Proiect sau Cont | Acțiuni de date + creare proiect |
| **Azure AI Owner** | Cont | Acces complet + management atribuiri rol |
| **Azure AI Project Manager** | Proiect | Acțiuni de date + poate atribui rolul Azure AI User altora |
| **Contributor** | Abonament/GR | Acțiuni de management (creare/ștergere resurse). **Nu include acțiuni de date** |
| **Owner** | Abonament/GR | Acțiuni de management + atribuiri roluri. **Nu include acțiuni de date** |
| **Reader** | Orice | Acces doar în citire la management |

> **Concluzie cheie:** `Owner` și `Contributor` NU includ acțiuni de date. Ai nevoie întotdeauna de un rol `Azure AI *` pentru operațiuni agent. Rolul minim pentru acest atelier este **Azure AI User** la domeniul **proiect**.

---

## 7. Checklist finală atelier

Folosește asta ca semn de confirmare finală că ai terminat totul:

| # | Element | Modul | Validat? |
|---|---------|-------|----------|
| 1 | Toate prerechizitele instalate și verificate | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit și extensiile Foundry instalate | [01](01-install-foundry-toolkit.md) | |
| 3 | Proiect Foundry creat (sau proiect existent selectat) | [02](02-create-foundry-project.md) | |
| 4 | Model implementat (de exemplu, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Rolul de utilizator Azure AI atribuit la nivel de proiect | [02](02-create-foundry-project.md) | |
| 6 | Proiectul agentului găzduit a fost schițat (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` configurat cu PROJECT_ENDPOINT și MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instrucțiunile agentului personalizate în main.py | [04](04-configure-and-code.md) | |
| 9 | Mediu virtual creat și dependențele instalate | [04](04-configure-and-code.md) | |
| 10 | Agent testat local cu F5 sau terminal (4 teste inițiale trecute) | [05](05-test-locally.md) | |
| 11 | Implementat în Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Starea containerului afișează "Started" sau "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verificat în VS Code Playground (4 teste inițiale trecute) | [07](07-verify-in-playground.md) | |
| 14 | Verificat în Foundry Portal Playground (4 teste inițiale trecute) | [07](07-verify-in-playground.md) | |

> **Felicitări!** Dacă toate elementele sunt bifate, ai finalizat întregul atelier. Ai construit un agent găzduit de la zero, l-ai testat local, l-ai implementat în Microsoft Foundry și l-ai validat în producție.

---

**Anterior:** [07 - Verificare în Playground](07-verify-in-playground.md) · **Acasă:** [README atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm răspunderea pentru eventualele neînțelegeri sau interpretări greșite rezultate din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->