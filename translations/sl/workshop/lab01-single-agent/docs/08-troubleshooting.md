# Modul 8 - Odpravljanje težav

Ta modul je referenčni vodič za vsako pogosto težavo, s katero se srečate med delavnico. Dodajte ga med zaznamke - vrnili se boste nanj vsakokrat, ko bo nekaj narobe.

---

## 1. Napake s pravicami

### 1.1 Zavrnjen dostop `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Glavni vzrok:** Nimate vloge `Azure AI User` na **ravni projekta**. To je najpogostejša napaka v delavnici.

**Popravek - korak za korakom:**

1. Odprite [https://portal.azure.com](https://portal.azure.com).
2. V zgornjem iskalnem polju vtipkajte ime svojega **Foundry projekta** (npr. `workshop-agents`).
3. **Ključno:** Kliknite rezultat, ki prikazuje tip **"Microsoft Foundry project"**, NE starševski račun/hub vir. To so različni viri z različnimi obsegih RBAC.
4. Na levi navigaciji strani projekta kliknite **Access control (IAM)**.
5. Kliknite zavihek **Role assignments**, da preverite, ali že imate vlogo:
   - Poiščite svoje ime ali e-poštni naslov.
   - Če je `Azure AI User` že na seznamu → ima napaka drug vzrok (glejte korak 8 spodaj).
   - Če ni na seznamu → nadaljujte z dodajanjem.
6. Kliknite **+ Add** → **Add role assignment**.
7. V zavihku **Role**:
   - Poiščite [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Izberite jo med rezultati.
   - Kliknite **Next**.
8. V zavihku **Members**:
   - Izberite **User, group, or service principal**.
   - Kliknite **+ Select members**.
   - Poiščite svoje ime ali e-poštni naslov.
   - Izberite sebe med rezultati.
   - Kliknite **Select**.
9. Kliknite **Review + assign** → ponovno **Review + assign**.
10. **Počakajte 1-2 minuti** - spremembe RBAC potrebujejo čas za uveljavitev.
11. Poskusite operacijo, ki je prej spodletela.

> **Zakaj lastnik/prispevalec ni dovolj:** Azure RBAC ima dve vrsti dovoljenj - *upravljalske ukrepe* in *dovoljenja za podatke*. Lastnik in prispevalec imata upravljalska dovoljenja (ustvarjanje virov, urejanje nastavitev), vendar operacije agentov zahtevajo pravico `agents/write`, ki je tip dovoljenja za podatke in je vključena samo v vlogah `Azure AI User`, `Azure AI Developer` ali `Azure AI Owner`. Oglejte si [Foundry RBAC dokumentacijo](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` med ustvarjanjem vira

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Glavni vzrok:** Nimate dovoljenja za ustvarjanje ali spreminjanje Azure virov v tem naročniškem računu/skupini virov.

**Popravek:**
1. Prosite skrbnika naročnine, naj vam dodeli vlogo **Contributor** na skupini virov, kjer je vaš Foundry projekt.
2. Alternativno naj za vas ustvari Foundry projekt in vam dodeli vlogo **Azure AI User** na projektu.

### 1.3 `SubscriptionNotRegistered` za [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Glavni vzrok:** Azure naročnina ni registrirala ponudnika virov, potrebnega za Foundry.

**Popravek:**

1. Odprite terminal in zaženite:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Počakajte, da se registracija zaključi (lahko traja 1-5 minut):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Pričakovani izhod: `"Registered"`
3. Ponovno poizkusite operacijo.

---

## 2. Docker napake (samo če je Docker nameščen)

> Docker je za to delavnico **neobvezen**. Te napake veljajo samo, če imate nameščen Docker Desktop in razširitev Foundry poskuša lokalno zgraditi vsebnik.

### 2.1 Docker demon ne teče

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Popravek - korak za korakom:**

1. **Poiščite Docker Desktop** v Start meniju (Windows) ali v Aplikacijah (macOS) in ga zaženite.
2. Počakajte, da se okno Docker Desktop prikaže z napisom **"Docker Desktop is running"** - to običajno traja 30-60 sekund.
3. Poglejte za ikono Docker kita v sistemski vrstici (Windows) ali menijski vrstici (macOS). Premaknite kurzor nanjo, da preverite status.
4. Preverite v terminalu:
   ```powershell
   docker info
   ```
   Če to izpiše sistemske podatke o Dockerju (Server Version, Storage Driver itd.), Docker teče.
5. **Posebno za Windows:** Če Docker še vedno ne zažene:
   - Odprite Docker Desktop → **Settings** (ikona zobnika) → **General**.
   - Prepričajte se, da je označeno **Use the WSL 2 based engine**.
   - Kliknite **Apply & restart**.
   - Če WSL 2 ni nameščen, zaženite `wsl --install` v povišanem PowerShellu in nato znova zaženite računalnik.
6. Ponovno poskusite razmestitev.

### 2.2 Docker build spodleti zaradi napak pri odvisnostih

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Popravek:**
1. Odprite datoteko `requirements.txt` in preverite, da so imena paketov pravilno črkovana.
2. Preverite, da je verzija pravilno določena:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Najprej preizkusite lokalno namestitev:
   ```bash
   pip install -r requirements.txt
   ```
4. Če uporabljate zasebni paketni indeks, se prepričajte, da ima Docker omrežni dostop do njega.

### 2.3 Neujemanje platforme vsebnika (Apple Silicon)

Če razmestite iz Apple Silicon Mac-a (M1/M2/M3/M4), mora biti vsebnik zgrajen za `linux/amd64`, ker Foundry runtime uporablja AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Ukaz za razmestitev, ki ga izvaja razširitev Foundry, to večinoma samodejno uredi. Če vidite napake, povezane z arhitekturo, zgradite ročno z zastavico `--platform` in se obrnite na ekipo Foundry.

---

## 3. Napake pri avtentikaciji

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ne uspe pridobiti žetona

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Glavni vzrok:** Noben izmed virov poverilnic v verigi `DefaultAzureCredential` nima veljavnega žetona.

**Popravek - poskusite vsako možnost po vrsti:**

1. **Ponovno prijavite preko Azure CLI** (najpogostejša rešitev):
   ```bash
   az login
   ```
   Odpre se okno brskalnika. Prijavite se in se nato vrnite v VS Code.

2. **Nastavite pravo naročnino:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Če to ni prava naročnina:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Ponovno prijavite preko VS Code:**
   - Kliknite ikono **Računi** (ikona osebe) spodaj levo v VS Code.
   - Kliknite svoje uporabniško ime → **Odjava**.
   - Kliknite ikono računa ponovno → **Prijava v Microsoft**.
   - Dokončajte postopek prijave v brskalniku.

4. **Service principal (samo za scenarije CI/CD):**
   - Nastavite naslednje spremenljivke okolja v datoteki `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Nato ponovno zaženite agentov proces.

5. **Preverite predpomnilnik žetonov:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Če to spodleti, je vaš CLI žeton potekel. Ponovno zaženite `az login`.

### 3.2 Žeton deluje lokalno, a ne v gostovani razmestitvi

**Glavni vzrok:** Gostovani agent uporablja sistemsko upravljano identiteto, ki je drugačna od vaših osebnih poverilnic.

**Popravek:** To je pričakovano obnašanje - upravljana identiteta se samodejno ustvari med razmestitvijo. Če gostovani agent še vedno dobi napake avtentikacije:
1. Preverite, ali ima upravljana identiteta Foundry projekta dostop do Azure OpenAI vira.
2. Preverite, da je `PROJECT_ENDPOINT` v `agent.yaml` pravilno nastavljen.

---

## 4. Napake modela

### 4.1 Namestitev modela ni najdena

```
Error: Model deployment not found / The specified deployment does not exist
```

**Popravek - korak za korakom:**

1. Odprite svojo datoteko `.env` in si zapišite vrednost `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Odprite stransko vrstico **Microsoft Foundry** v VS Code.
3. Razširite svoj projekt → **Model Deployments**.
4. Primerjajte ime namestitve tukaj z vrednostjo v `.env`.
5. Imena so **občutljiva na velike in male črke** - `gpt-4o` ni isto kot `GPT-4o`.
6. Če se ne ujemata, popravite `.env` z natančnim imenom iz stranske vrstice.
7. Za gostovano razmestitev posodobite tudi `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model odgovori z nepričakovano vsebino

**Popravek:**
1. Preglejte konstanto `EXECUTIVE_AGENT_INSTRUCTIONS` v `main.py`. Prepričajte se, da ni obrezana ali poškodovana.
2. Preverite nastavitev temperature modela (če je nastavljiva) - nižje vrednosti dajejo bolj deterministične rezultate.
3. Primerjajte nameščen model (npr. `gpt-4o` proti `gpt-4o-mini`) - različni modeli imajo različne zmožnosti.

---

## 5. Napake pri razmestitvi

### 5.1 Avtorizacija za ACR prenos

```
Error: AcrPullUnauthorized
```

**Glavni vzrok:** Upravljana identiteta Foundry projekta ne more prenesti slike vsebnika iz Azure Container Registry.

**Popravek - korak za korakom:**

1. Odprite [https://portal.azure.com](https://portal.azure.com).
2. V zgornjem iskalnem polju poiščite **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Kliknite na register, ki je povezan z vašim Foundry projektom (ponavadi v isti skupini virov).
4. Na levi navigaciji kliknite **Access control (IAM)**.
5. Kliknite **+ Add** → **Add role assignment**.
6. Poiščite **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** in jo izberite. Kliknite **Next**.
7. Izberite **Managed identity** → kliknite **+ Select members**.
8. Poiščite in izberite upravljano identiteto Foundry projekta.
9. Kliknite **Select** → **Review + assign** → **Review + assign**.

> Ta dodelitev vloge običajno samodejno nastavi razširitev Foundry. Če vidite to napako, je lahko avtomatska nastavitev spodletela. Poskusite ponovno razmestiti - razširitev lahko poskusi nastavitev znova.

### 5.2 Agent se ne zažene po razmestitvi

**Simptomi:** Status vsebnika ostane "Pending" več kot 5 minut ali kaže "Failed".

**Popravek - korak za korakom:**

1. Odprite stransko vrstico **Microsoft Foundry** v VS Code.
2. Kliknite na svoj gostovani agent → izberite različico.
3. V podrobnostih preverite **Container Details** → poiščite razdelek ali povezavo **Logs**.
4. Preberite dnevnik zagona vsebnika. Pogosti vzroki:

| Sporočilo iz dnevnika | Vzrok | Popravek |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Manjkajoča odvisnost | Dodajte jo v `requirements.txt` in ponovno razmestite |
| `KeyError: 'PROJECT_ENDPOINT'` | Manjkajoča okoljska spremenljivka | Dodajte spremenljivko v `agent.yaml` pod `env:` |
| `OSError: [Errno 98] Address already in use` | Konflikt vrat | Prepričajte se, da ima `agent.yaml` `port: 8088` in da se nanj prijavlja samo en proces |
| `ConnectionRefusedError` | Agent ni začel poslušati | Preverite `main.py` - klic `from_agent_framework()` mora teči ob zagonu |

5. Odpravite težavo in nato ponovno razmestite iz [Modula 6](06-deploy-to-foundry.md).

### 5.3 Čas razmestitve poteče

**Popravek:**
1. Preverite svojo internetno povezavo - Docker push lahko nosi veliko podatkov (>100MB za prvo razmestitev).
2. Če ste za korporativnim proxyjem, zagotovite, da so nastavitve proxyja v Docker Desktop pravilno nastavljene: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Poskusite znova - omrežni izpadi lahko povzročijo začasne napake.

---

## 6. Hiter pregled: RBAC vloge

| Vloga | Obseg | Kaj omogoča |
|------|-------|-------------|
| **Azure AI User** | Projekt | Dovoljenja za podatke: gradnja, razmestitev in klic agentov (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt ali račun | Dovoljenja za podatke + ustvarjanje projektov |
| **Azure AI Owner** | Račun | Poln dostop + upravljanje dodelitev vlog |
| **Azure AI Project Manager** | Projekt | Dovoljenja za podatke + lahko dodeljuje Azure AI User drugim |
| **Contributor** | Naročnina/skupina virov | Upravljalska dovoljenja (ustvarjanje/brisanje virov). **NE VKLJUČUJE podatkovnih dovoljenj** |
| **Owner** | Naročnina/skupina virov | Upravljalska dovoljenja + dodeljevanje vlog. **NE VKLJUČUJE podatkovnih dovoljenj** |
| **Reader** | Karkoli | Samo bralni dostop do upravljanja |

> **Ključna ugotovitev:** `Owner` in `Contributor` ne vključujeta dovoljenj za podatke. Za operacije agentov vedno potrebujete vlogo `Azure AI *`. Najmanjša vloga za to delavnico je **Azure AI User** na **ravni projekta**.

---

## 7. Kontrolni seznam za dokončanje delavnice

Uporabite ga kot končno potrditev, da ste opravili vse:

| # | Postavka | Modul | Preverjeno? |
|---|----------|-------|-------------|
| 1 | Vse predpogoje nameščene in preverjene | [00](00-prerequisites.md) | |
| 2 | Nameščeni Foundry Toolkit in razširitve Foundry | [01](01-install-foundry-toolkit.md) | |
| 3 | Ustvarjen Foundry projekt (ali izbran obstoječ projekt) | [02](02-create-foundry-project.md) | |
| 4 | Model nameščen (npr. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Vloga uporabnika Azure AI dodeljena na obsegu projekta | [02](02-create-foundry-project.md) | |
| 6 | Projekt gostovanega agenta pripravljen (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfiguriran z PROJECT_ENDPOINT in MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Navodila agenta prilagojena v main.py | [04](04-configure-and-code.md) | |
| 9 | Ustvarjeno virtualno okolje in nameščene odvisnosti | [04](04-configure-and-code.md) | |
| 10 | Agent preizkušen lokalno z F5 ali terminalom (4 narejeni osnovni testi) | [05](05-test-locally.md) | |
| 11 | Nameščen v Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Status kontejnerja prikazuje "Started" ali "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Preverjeno v VS Code Playground (4 narejeni osnovni testi) | [07](07-verify-in-playground.md) | |
| 14 | Preverjeno v Foundry Portal Playground (4 narejeni osnovni testi) | [07](07-verify-in-playground.md) | |

> **Čestitamo!** Če so vsi elementi označeni, ste zaključili cel delavnico. Ustvarili ste gostovanega agenta iz nič, preizkusili ga lokalno, ga namestili v Microsoft Foundry in preverili v produkcijskem okolju.

---

**Prejšnje:** [07 - Preveri v igralnem okolju](07-verify-in-playground.md) · **Domov:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo storitve za prevajanje z umetno inteligenco [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da lahko avtomatizirani prevodi vsebujejo napake ali netočnosti. Izvirni dokument v maternem jeziku se šteje za avtoritativni vir. Za ključne informacije priporočamo strokovni človeški prevod. Za kakršne koli nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda, nismo odgovorni.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->