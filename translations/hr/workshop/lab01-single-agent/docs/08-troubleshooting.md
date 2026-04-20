# Modul 8 - Rješavanje problema

Ovaj modul je referentni vodič za svaki česti problem na koji možete naići tijekom radionice. Dodajte ga u favorite - vratit ćete mu se kad god nešto pođe po zlu.

---

## 1. Pogreške vezane uz dozvole

### 1.1 `agents/write` dozvola odbijena

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Uzrok:** Nemate ulogu `Azure AI User` na razini **projekta**. Ovo je najčešća pogreška u radionici.

**Popravak - korak po korak:**

1. Otvorite [https://portal.azure.com](https://portal.azure.com).
2. U gornji tražilicu upišite ime vašeg **Foundry projekta** (npr. `workshop-agents`).
3. **Važno:** Kliknite na rezultat koji prikazuje tip **"Microsoft Foundry project"**, a NE na roditeljski račun/hub resurs. To su različiti resursi s različitim RBAC rasponima.
4. U lijevom izborniku na stranici projekta kliknite **Access control (IAM)**.
5. Kliknite karticu **Role assignments** da provjerite imate li već ulogu:
   - Potražite svoje ime ili email.
   - Ako je `Azure AI User` već naveden → pogreška ima drugi uzrok (provjerite korak 8 dolje).
   - Ako nije naveden → nastavite s dodavanjem.
6. Kliknite **+ Add** → **Add role assignment**.
7. Na kartici **Role**:
   - Potražite [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Odaberite ga s rezultata.
   - Kliknite **Next**.
8. Na kartici **Members**:
   - Odaberite **User, group, or service principal**.
   - Kliknite **+ Select members**.
   - Potražite svoje ime ili email adresu.
   - Odaberite sebe s rezultata.
   - Kliknite **Select**.
9. Kliknite **Review + assign** → ponovo **Review + assign**.
10. **Pričekajte 1-2 minute** - RBAC promjene trebaju vremena da se primijene.
11. Ponovno pokušajte izvršiti operaciju koja je prethodno neuspjela.

> **Zašto vlasnik/kontributor nije dovoljan:** Azure RBAC ima dvije vrste dozvola - *akcije upravljanja* i *akcije podataka*. Vlasnik i Kontributor dozvoljavaju akcije upravljanja (kreiranje resursa, uređivanje postavki), ali agent operacije zahtijevaju `agents/write` **akciju podataka**, što je uključeno samo u ulogama `Azure AI User`, `Azure AI Developer` ili `Azure AI Owner`. Pogledajte [Foundry RBAC dokumentaciju](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` tijekom kreiranja resursa

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Uzrok:** Nemate dozvolu za kreiranje ili izmjenu Azure resursa u ovom pretplati/grupi resursa.

**Popravak:**
1. Zamolite administratora pretplate da vam dodijeli ulogu **Contributor** na grupi resursa gdje je vaš Foundry projekt.
2. Alternativno, zamolite da oni kreiraju Foundry projekt za vas i dodijele vam **Azure AI User** ulogu na projektu.

### 1.3 `SubscriptionNotRegistered` za [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Uzrok:** Azure pretplata nije registrirala davatelja resursa potreban za Foundry.

**Popravak:**

1. Otvorite terminal i pokrenite:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Pričekajte da registracija bude dovršena (može potrajati 1-5 minuta):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Očekivani ispis: `"Registered"`
3. Ponovno pokušajte operaciju.

---

## 2. Docker greške (samo ako je Docker instaliran)

> Docker je **opcionalan** za ovu radionicu. Ove greške se odnose samo ako imate instaliran Docker Desktop i Foundry proširenje pokušava lokalno graditi kontejner.

### 2.1 Docker daemon ne radi

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Popravak - korak po korak:**

1. Pronađite Docker Desktop u izborniku Start (Windows) ili Aplikacijama (macOS) i pokrenite ga.
2. Pričekajte da prozor Docker Desktop pokaže **"Docker Desktop is running"** - to obično traje 30-60 sekundi.
3. Potražite ikonu Docker kita u sistemskoj traci (Windows) ili traci izbornika (macOS). Postavite kursor na nju za potvrdu statusa.
4. Provjerite u terminalu:
   ```powershell
   docker info
   ```
   Ako ovo ispisuje informacije o Docker sustavu (Server Verzija, Storage Driver itd.), Docker radi.
5. **Specifično za Windows:** ako Docker i dalje ne želi startati:
   - Otvorite Docker Desktop → **Settings** (ikonica zupčanika) → **General**.
   - Provjerite je li označeno **Use the WSL 2 based engine**.
   - Kliknite **Apply & restart**.
   - Ako WSL 2 nije instaliran, pokrenite `wsl --install` u povišenom PowerShellu i restartajte računalo.
6. Ponovno pokušajte s implementacijom.

### 2.2 Docker build ne uspijeva zbog grešaka ovisnosti

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Popravak:**
1. Otvorite `requirements.txt` i provjerite jesu li imena svih paketa ispravno napisana.
2. Provjerite ispravnost verzija:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Najprije testirajte lokalnu instalaciju:
   ```bash
   pip install -r requirements.txt
   ```
4. Ako koristite privatni paketni indeks, pobrinite se da Docker ima mrežni pristup do njega.

### 2.3 Neusklađenost platforme kontejnera (Apple Silicon)

Ako implementirate s Apple Silicon Mac računala (M1/M2/M3/M4), kontejner mora biti izgrađen za `linux/amd64` jer Foundry runtime koristi AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Deploy naredba Foundry proširenja automatizira ovo u većini slučajeva. Ako naiđete na greške povezane s arhitekturom, izgradite ručno s `--platform` opcijom i kontaktirajte Foundry tim.

---

## 3. Greške autentikacije

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ne uspijeva dohvatiti token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Uzrok:** Nijedan od credential izvora u `DefaultAzureCredential` lancu nema valjani token.

**Popravak - pokušajte svaki korak redom:**

1. **Ponovno prijavite se preko Azure CLI** (najčešći popravak):
   ```bash
   az login
   ```
   Otvara se prozor preglednika. Prijavite se, zatim se vratite u VS Code.

2. **Postavite ispravnu pretplatu:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Ako ovo nije prava pretplata:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Ponovno prijavite se preko VS Code:**
   - Kliknite ikonu **Accounts** (ikona osobe) u donjem lijevom kutu VS Code.
   - Kliknite svoje ime → **Sign Out**.
   - Ponovo kliknite Accounts ikonu → **Sign in to Microsoft**.
   - Dovršite prijavu u pregledniku.

4. **Service principal (samo CI/CD scenariji):**
   - Postavite ove environment varijable u `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Zatim restartajte agent proces.

5. **Provjerite cache tokena:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Ako ovo ne uspije, vaš CLI token je istekao. Pokrenite `az login` ponovno.

### 3.2 Token radi lokalno, ali ne i na hostiranoj implementaciji

**Uzrok:** Hostirani agent koristi sistemski upravljan identitet, koji je različit od vašeg osobnog credentiala.

**Popravak:** Ovo je očekivano ponašanje - upravljani identitet se automatski priprema prilikom implementacije. Ako hostirani agent i dalje dobiva greške autentikacije:
1. Provjerite ima li upravljani identitet Foundry projekta pristup Azure OpenAI resursu.
2. Provjerite je li `PROJECT_ENDPOINT` u `agent.yaml` ispravan.

---

## 4. Greške modela

### 4.1 Model deployment nije pronađen

```
Error: Model deployment not found / The specified deployment does not exist
```

**Popravak - korak po korak:**

1. Otvorite `.env` datoteku i zabilježite vrijednost `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Otvorite **Microsoft Foundry** bočnu traku u VS Code.
3. Proširite svoj projekt → **Model Deployments**.
4. Usporedite ime implementacije tamo s vrijednošću u `.env`.
5. Ime je **osjetljivo na velika/mala slova** - `gpt-4o` nije isto što i `GPT-4o`.
6. Ako se ne podudaraju, ažurirajte `.env` da koristi točno ime prikazano u bočnoj traci.
7. Za hostiranu implementaciju, također ažurirajte `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model daje neočekivani odgovor

**Popravak:**
1. Pregledajte konstantu `EXECUTIVE_AGENT_INSTRUCTIONS` u `main.py`. Provjerite nije li skraćena ili oštećena.
2. Provjerite temperatura modela (ako je konfigurabilno) - niže vrijednosti daju determinističkije rezultate.
3. Usporedite koji je model implementiran (npr. `gpt-4o` naspram `gpt-4o-mini`) - različiti modeli imaju različite mogućnosti.

---

## 5. Greške implementacije

### 5.1 ACR autorizacija za preuzimanje

```
Error: AcrPullUnauthorized
```

**Uzrok:** Upravljani identitet Foundry projekta ne može povući sliku kontejnera iz Azure Container Registry.

**Popravak - korak po korak:**

1. Otvorite [https://portal.azure.com](https://portal.azure.com).
2. Potražite **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** u vrhu pretraživača.
3. Kliknite na registar povezan s vašim Foundry projektom (obično je u istoj grupi resursa).
4. U lijevom izborniku kliknite **Access control (IAM)**.
5. Kliknite **+ Add** → **Add role assignment**.
6. Potražite i odaberite **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Kliknite **Next**.
7. Odaberite **Managed identity** → kliknite **+ Select members**.
8. Pronađite i odaberite upravljani identitet Foundry projekta.
9. Kliknite **Select** → **Review + assign** → **Review + assign**.

> Ova uloga se obično postavlja automatski preko Foundry proširenja. Ako vidite ovu grešku, automatska konfiguracija možda nije uspjela. Možete pokušati ponovno implementirati - proširenje može pokušati ponovno.

### 5.2 Agent ne uspije pokrenuti se nakon implementacije

**Simptomi:** Status kontejnera ostaje na "Pending" duže od 5 minuta ili prikazuje "Failed".

**Popravak - korak po korak:**

1. Otvorite **Microsoft Foundry** bočnu traku u VS Code.
2. Kliknite na svoj hostirani agent → odaberite verziju.
3. U panelu detalja provjerite **Container Details** → potražite odjeljak ili link **Logs**.
4. Pročitajte početne dnevničke zapise kontejnera. Najčešći uzroci:

| Poruka zapisa | Uzrok | Popravak |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Nedostaje ovisnost | Dodajte u `requirements.txt` i ponovo implementirajte |
| `KeyError: 'PROJECT_ENDPOINT'` | Nedostaje environment varijabla | Dodajte varijablu u `agent.yaml` pod `env:` |
| `OSError: [Errno 98] Address already in use` | Sukob porta | Provjerite da `agent.yaml` ima `port: 8088` i da samo jedan proces veže taj port |
| `ConnectionRefusedError` | Agent se nije počeo slušati | Provjerite `main.py` - poziv `from_agent_framework()` mora se izvršiti pri startu |

5. Ispravite problem, zatim ponovo implementirajte iz [Modula 6](06-deploy-to-foundry.md).

### 5.3 Implementacija istječe

**Popravak:**
1. Provjerite internet vezu - Docker push može biti velik (>100MB za prvu implementaciju).
2. Ako ste iza korporacijskog proxyja, pobrinite se da su proxy postavke u Docker Desktop konfigurirane: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Pokušajte ponovno - mrežni problemi mogu uzrokovati prolazne greške.

---

## 6. Brzi pregled: RBAC uloge

| Uloga | Tipični opseg | Što dozvoljava |
|------|---------------|----------------|
| **Azure AI User** | Projekt | Akcije podataka: izgradnja, implementacija i pozivanje agenata (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt ili račun | Akcije podataka + kreiranje projekata |
| **Azure AI Owner** | Račun | Potpun pristup + upravljanje dodjelama uloga |
| **Azure AI Project Manager** | Projekt | Akcije podataka + može dodijeliti Azure AI User drugima |
| **Contributor** | Pretplata/RG | Akcije upravljanja (kreiranje/brisanje resursa). **Ne uključuje akcije podataka** |
| **Owner** | Pretplata/RG | Akcije upravljanja + upravljanje ulogama. **Ne uključuje akcije podataka** |
| **Reader** | Bilo koji | Samo za čitanje upravljanja |

> **Ključni zaključak:** `Owner` i `Contributor` ne uključuju akcije podataka. Za agent operacije uvijek trebate `Azure AI *` ulogu. Minimalna uloga za ovu radionicu je **Azure AI User** na **projektnom** opsegu.

---

## 7. Kontrolna lista za završetak radionice

Koristite ovo kao završni potpis da ste završili sve:

| # | Stavka | Modul | Prošao? |
|---|------|--------|---|
| 1 | Svi preduvjeti instalirani i provjereni | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit i Foundry proširenja instalirani | [01](01-install-foundry-toolkit.md) | |
| 3 | Kreiran Foundry projekt (ili odabran postojeći) | [02](02-create-foundry-project.md) | |
| 4 | Model implementiran (npr. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Dodijeljena uloga Azure AI korisnika na razini projekta | [02](02-create-foundry-project.md) | |
| 6 | Postavljen projekt hostiranog agenta (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfiguriran s PROJECT_ENDPOINT i MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Upute za agenta prilagođene u main.py | [04](04-configure-and-code.md) | |
| 9 | Kreirano virtualno okruženje i instalirane ovisnosti | [04](04-configure-and-code.md) | |
| 10 | Agent testiran lokalno pomoću F5 ili terminala (uspješno 4 temeljna testa) | [05](05-test-locally.md) | |
| 11 | Implementirano u Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Status kontejnera prikazuje "Started" ili "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Provjereno u VS Code Playground (uspješno 4 temeljna testa) | [07](07-verify-in-playground.md) | |
| 14 | Provjereno u Foundry Portal Playground (uspješno 4 temeljna testa) | [07](07-verify-in-playground.md) | |

> **Čestitamo!** Ako su svi stavke označene, dovršili ste cijelu radionicu. Izgradili ste hostiranog agenta od nule, testirali ga lokalno, implementirali u Microsoft Foundry i potvrdili u produkciji.

---

**Prethodno:** [07 - Verify in Playground](07-verify-in-playground.md) · **Početna:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Odricanje od odgovornosti**:  
Ovaj dokument preveden je korištenjem AI usluge prevođenja [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo postići točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba se smatrati autoritativnim izvorom. Za kritične informacije preporučuje se profesionalni ljudski prijevod. Ne odgovaramo za bilo kakve nesporazume ili kriva tumačenja koja proizlaze iz upotrebe ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->