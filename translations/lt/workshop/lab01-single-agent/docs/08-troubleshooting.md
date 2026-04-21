# 8 modulis - trikčių šalinimas

Šis modulis yra nuorodų vadovas visoms dažnai pasitaikančioms problemoms dirbant su dirbtuvėmis. Įrašykite jį į žymes – sugrįšite prie jo kiekvieną kartą, kai kažkas nepavyks.

---

## 1. Leidimų klaidos

### 1.1 Leidimas `agents/write` atmestas

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Pagrindinė priežastis:** Jūs neturite `Azure AI User` vaidmens **projekto** lygyje. Tai pats dažniausias klaidos atvejis dirbtuvėse.

**Sprendimas – po žingsnį:**

1. Atidarykite [https://portal.azure.com](https://portal.azure.com).
2. Viršuje esančiame paieškos laukelyje įveskite savo **Foundry projekto** pavadinimą (pvz., `workshop-agents`).
3. **Svarbu:** Spustelėkite rezultatą, kuriame rodomas tipas **"Microsoft Foundry project"**, O NE tėvinį abonementą/arba hub išteklių. Tai yra skirtingi ištekliai su skirtingais RBAC prieigos sritimis.
4. Kairėje projekto pusėje spustelėkite **Access control (IAM)**.
5. Spustelėkite skirtuką **Role assignments**, kad patikrintumėte, ar jau turite vaidmenį:
   - Ieškokite savo vardo ar el. pašto.
   - Jei `Azure AI User` jau yra sąraše → klaidos priežastis kitokia (žiūrėkite 8 žingsnį žemiau).
   - Jei nėra sąraše → tęskite pridėjimą.
6. Spustelėkite **+ Add** → **Add role assignment**.
7. Skiltyje **Role**:
   - Ieškokite [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Pasirinkite iš rezultatų.
   - Spustelėkite **Next**.
8. Skiltyje **Members**:
   - Pasirinkite **User, group, or service principal**.
   - Spustelėkite **+ Select members**.
   - Ieškokite savo vardo arba el. pašto adreso.
   - Pasirinkite save iš rezultatų.
   - Spustelėkite **Select**.
9. Spustelėkite **Review + assign** → dar kartą **Review + assign**.
10. **Palaukite 1-2 minutes** – RBAC pakeitimams prireikia laiko išplisti.
11. Bandykite vėl atlikti nesėkmingą veiksmą.

> **Kodėl Owner/Contributor nepakanka:** Azure RBAC turi du leidimų tipus – *valdymo veiksmai* ir *duomenų veiksmai*. Owner ir Contributor suteikia valdymo veiksmus (kuriant išteklius, keičiant nustatymus), tačiau agentų operacijos reikalauja `agents/write` **duomenų veiksmo**, kuris įtrauktas tik į `Azure AI User`, `Azure AI Developer` arba `Azure AI Owner` vaidmenis. Žr. [Foundry RBAC dokumentaciją](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` klaida resursų kūrimo metu

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Pagrindinė priežastis:** Neturite leidimo kurti ar keisti Azure išteklius šioje prenumeratoje/taškinėje grupėje.

**Sprendimas:**
1. Paprašykite savo prenumeratos administratoriaus priskirti jums **Contributor** vaidmenį tam resursų grupei, kur yra jūsų Foundry projektas.
2. Arba paprašykite, kad jis sukurtų Foundry projektą už jus ir suteiktų jums **Azure AI User** rolę projekte.

### 1.3 Klaida `SubscriptionNotRegistered` dėl [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Pagrindinė priežastis:** Azure prenumerata nėra užregistravusi reikalingo Foundry išteklių tiekėjo.

**Sprendimas:**

1. Atidarykite terminalą ir vykdykite:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Palaukite registracijos užbaigimo (užtrunka apie 1–5 minutes):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Laukiama išvestis: `"Registered"`
3. Pakartokite veiksmą.

---

## 2. Docker klaidos (tik jei įdiegta Docker)

> Docker naudojimas yra **neprivalomas** šioms dirbtuvėms. Šios klaidos galioja tik jei turite įdiegtą Docker Desktop ir Foundry plėtinys bando atlikti vietinį konteinerio kūrimą.

### 2.1 Docker demonas neveikia

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Sprendimas – po žingsnį:**

1. Suraskite „Docker Desktop“ savo Start meniu (Windows) arba Applications (macOS) ir paleiskite.
2. Palaukite, kol Docker Desktop langas parodys **„Docker Desktop is running“** – tai paprastai užtrunka 30–60 sekundžių.
3. Ieškokite Docker banginio piktogramos sistemos dėkle (Windows) arba meniu juostoje (macOS). Užveskite pelę, kad patvirtintumėte statusą.
4. Patikrinkite terminale:
   ```powershell
   docker info
   ```
   Jei čia matote Docker sistemos informaciją (Server Version, Storage Driver ir kt.), Docker veikia.
5. **Tik Windows:** Jei Docker vis dar neveikia:
   - Atidarykite Docker Desktop → **Settings** (įrankio piktograma) → **General**.
   - Patikrinkite, ar pažymėta **Use the WSL 2 based engine**.
   - Spustelėkite **Apply & restart**.
   - Jei WSL 2 nėra įdiegtas, paleiskite `wsl --install` pakeltame PowerShell ir perkraukite kompiuterį.
6. Bandykite vėl diegti.

### 2.2 Docker kūrimas nepavyksta dėl priklausomybių klaidų

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Sprendimas:**
1. Atidarykite `requirements.txt` ir patikrinkite, ar visi paketų pavadinimai parašyti teisingai.
2. Įsitikinkite, kad versijų fiksavimas tinkamas:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Išbandykite diegimą vietoje pirmiausia:
   ```bash
   pip install -r requirements.txt
   ```
4. Jei naudojate privatų paketo indeksą, patikrinkite, ar Docker turi tinklo prieigą prie jo.

### 2.3 Konteinerio platformos neatitikimas (Apple Silicon)

Jei diegiate iš Apple Silicon Mac (M1/M2/M3/M4), konteineris turi būti sukurtas `linux/amd64` platformai, nes Foundry konteinerio vykdymo aplinka naudoja AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry plėtinio deploy komanda šį procesą daugeliu atvejų nustato automatiškai. Jei matote su architektūra susijusias klaidas, sukurkite konteinerį rankiniu būdu naudodami parinktį `--platform` ir susisiekite su Foundry komanda.

---

## 3. Autentifikacijos klaidos

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) nepavyksta gauti žetono

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Pagrindinė priežastis:** Nei vienas `DefaultAzureCredential` šaltinių grandinėje neturi galiojančio žetono.

**Sprendimas – bandykite kiekvieną žingsnį paeiliui:**

1. **Prisijunkite iš naujo per Azure CLI** (dažniausias sprendimas):
   ```bash
   az login
   ```
   Atsidarys naršyklės langas. Prisijunkite, tada grįžkite į VS Code.

2. **Nustatykite teisingą prenumeratą:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Jei tai ne ta prenumerata:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Prisijunkite iš naujo per VS Code:**
   - Spustelėkite apatiniame kairiajame kampe esantį **Accounts** ikoną (žmogaus figūrėlę).
   - Spustelėkite savo paskyros vardą → **Sign Out**.
   - Vėl spustelėkite Accounts ikoną → **Sign in to Microsoft**.
   - Užbaikite naršyklės prisijungimo procesą.

4. **Service principal (tik CI/CD scenarijuose):**
   - Nustatykite šiuos aplinkos kintamuosius savo `.env` faile:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Tada paleiskite savo agentą iš naujo.

5. **Patikrinkite žetono talpyklą:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Jei tai nepavyksta, jūsų CLI žetonas pasibaigęs. Vėl paleiskite `az login`.

### 3.2 Žetonas veikia vietoje, bet ne talpinamame diegime

**Pagrindinė priežastis:** Talpinamas agentas naudoja sisteminį valdomą identitetą, kuris skiriasi nuo jūsų asmeninių kredencialų.

**Sprendimas:** Tai yra numatytas elgesys – valdomas identitetas automatiškai sukuriamas diegimo metu. Jei talpinamas agentas vis dar gauna autentifikacijos klaidų:
1. Patikrinkite, ar Foundry projekto valdomas identitetas turi prieigą prie Azure OpenAI ištekliaus.
2. Patikrinkite, ar `PROJECT_ENDPOINT` reikšmė `agent.yaml` faile yra teisinga.

---

## 4. Modelio klaidos

### 4.1 Modelio diegimas nerastas

```
Error: Model deployment not found / The specified deployment does not exist
```

**Sprendimas – po žingsnį:**

1. Atidarykite `.env` failą ir atkreipkite dėmesį į `AZURE_AI_MODEL_DEPLOYMENT_NAME` reikšmę.
2. Atidarykite **Microsoft Foundry** šoninę juostą VS Code.
3. Išplėskite savo projektą → **Model Deployments**.
4. Palyginkite ten nurodytą diegimo pavadinimą su `.env` reikšme.
5. Pavadinimas yra **jautrus didžiosioms raidėms** – `gpt-4o` yra skirtinga nuo `GPT-4o`.
6. Jei nesutampa, atnaujinkite `.env` naudodami tikslų pavadinimą iš šoninės juostos.
7. Talpintame diegime taip pat atnaujinkite `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modelio atsakymas nesutampa su lūkesčiais

**Sprendimas:**
1. Peržiūrėkite `EXECUTIVE_AGENT_INSTRUCTIONS` konstantą faile `main.py`. Įsitikinkite, kad ji nėra sutrumpinta ar pažeista.
2. Patikrinkite modelio temperatūros nustatymą (jei galima konfigūruoti) – mažesnės reikšmės suteikia labiau deterministinį rezultatą.
3. Palyginkite, koks modelis yra diegiamas (pvz., `gpt-4o` prieš `gpt-4o-mini`) – skirtingi modeliai turi skirtingas galimybes.

---

## 5. Diegimo klaidos

### 5.1 Leidimas traukti iš ACR

```
Error: AcrPullUnauthorized
```

**Pagrindinė priežastis:** Foundry projekto valdomas identitetas negali patekti į konteinerio atvaizdą Azure Container Registry.

**Sprendimas – po žingsnį:**

1. Atidarykite [https://portal.azure.com](https://portal.azure.com).
2. Viršuje esančiame paieškos laukelyje įveskite **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Spustelėkite registrą, susietą su jūsų Foundry projektu (dažniausiai tame pačiame resursų grupėje).
4. Kairėje spustelėkite **Access control (IAM)**.
5. Spustelėkite **+ Add** → **Add role assignment**.
6. Ieškokite ir pasirinkite **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Spustelėkite **Next**.
7. Pasirinkite **Managed identity** → spustelėkite **+ Select members**.
8. Suraskite ir pasirinkite Foundry projekto valdomą identitetą.
9. Spustelėkite **Select** → **Review + assign** → **Review + assign**.

> Šis vaidmens priskyrimas paprastai vyksta automatiškai naudojant Foundry plėtinį. Jei matote šią klaidą, automatinis priskyrimas galėjo nepavykti. Galite pabandyti diegimą pakartoti – plėtinys gali mėginti atlikti priskyrimą iš naujo.

### 5.2 Agentas nesikrauna po diegimo

**Simptomai:** Konteinerio būsena "Pending" trunka ilgiau nei 5 minutes arba rodo "Failed".

**Sprendimas – po žingsnį:**

1. Atidarykite **Microsoft Foundry** šoninę juostą VS Code.
2. Spustelėkite savo talpinamą agentą → pasirinkite versiją.
3. Išsamios informacijos lange patikrinkite **Container Details** → ieškokite **Logs** skyriaus ar nuorodos.
4. Perskaitykite konteinerio paleidimo žurnalus. Dažniausios priežastys:

| Žurnalo pranešimas | Priežastis | Sprendimas |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Trūksta priklausomybės | Pridėkite ją į `requirements.txt` ir vėl diegkite |
| `KeyError: 'PROJECT_ENDPOINT'` | Trūksta aplinkos kintamojo | Įdėkite šį kintamąjį į `agent.yaml` po `env:` |
| `OSError: [Errno 98] Address already in use` | Prievado konfliktas | Įsitikinkite, kad `agent.yaml` yra `port: 8088` ir tik vienas procesas jį naudoja |
| `ConnectionRefusedError` | Agentas nesiklausė | Peržiūrėkite `main.py` - `from_agent_framework()` kvietimas turi vykti paleidimo metu |

5. Ištaisykite problemą ir vėl diegkite naudodami [6 modulį](06-deploy-to-foundry.md).

### 5.3 Diegimo laikas viršytas

**Sprendimas:**
1. Patikrinkite interneto ryšį – Docker atvaizdo įkėlimas gali būti didelis (>100MB pirmojo diegimo metu).
2. Jei esate už korporatyvinio proxy, patikrinkite, ar Docker Desktop proxy nustatymai sukonfigūruoti: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Bandykite dar kartą – tinklo trikdžiai gali sukelti laikinas klaidas.

---

## 6. Greita RBAC vaidmenų santrauka

| Vaidmuo | Dažniausia taikymo sritis | Ką suteikia |
|------|---------------|----------------|
| **Azure AI User** | Projektas | Duomenų veiksmai: kurti, diegti ir naudoti agentus (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projektas arba Abonementas | Duomenų veiksmai + projektų kūrimas |
| **Azure AI Owner** | Abonementas | Pilnas priėjimas + vaidmenų priskyrimas |
| **Azure AI Project Manager** | Projektas | Duomenų veiksmai + gali priskirti Azure AI User vaidmenis |
| **Contributor** | Prenumerata/RG | Valdymo veiksmai (kurti/trinti išteklius). **NĖRA duomenų veiksmų** |
| **Owner** | Prenumerata/RG | Valdymo veiksmai + vaidmenų priskyrimas. **NĖRA duomenų veiksmų** |
| **Reader** | Bet kuri | Tik skaitymo teisė valdymo srityje |

> **Pagrindinė išvada:** `Owner` ir `Contributor` NETURI duomenų veiksmų. Agentų operacijoms visuomet reikalingas `Azure AI *` vaidmuo. Minimalus vaidmuo šioms dirbtuvėms yra **Azure AI User** **projekto** lygmenyje.

---

## 7. Dirbtuvių užbaigimo kontrolinis sąrašas

Naudokite tai kaip galutinį patvirtinimą, kad viską įvykdėte:

| # | Punktas | Modulis | Atlikta? |
|---|------|--------|---|
| 1 | Visi reikalavimai įdiegti ir patikrinti | [00](00-prerequisites.md) | |
| 2 | Įdiegtas Foundry Toolkit ir Foundry plėtiniai | [01](01-install-foundry-toolkit.md) | |
| 3 | Sukurtas Foundry projektas (arba pasirinktas esamas) | [02](02-create-foundry-project.md) | |
| 4 | Modelis įdiegtas (pvz., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI naudotojo vaidmuo priskirtas projekto ribose | [02](02-create-foundry-project.md) | |
| 6 | Sukurtas talpinamo agento projektas (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` sukonfigūruotas su PROJECT_ENDPOINT ir MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agentų instrukcijos pritaikytos main.py faile | [04](04-configure-and-code.md) | |
| 9 | Sukurtos virtualioji aplinka ir įdiegtos priklausomybės | [04](04-configure-and-code.md) | |
| 10 | Agentas išbandytas lokaliai su F5 arba terminalu (praėjo 4 pagrindiniai testai) | [05](05-test-locally.md) | |
| 11 | Įdiegtas Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Dėžutės būklė rodo "Started" arba "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Patikrinta VS Code Playground aplinkoje (praėjo 4 pagrindiniai testai) | [07](07-verify-in-playground.md) | |
| 14 | Patikrinta Foundry Portal Playground aplinkoje (praėjo 4 pagrindiniai testai) | [07](07-verify-in-playground.md) | |

> **Sveikiname!** Jei visi punktai pažymėti, jūs baigėte visą dirbtuvių seriją. Jūs sukūrėte talpinamą agentą nuo nulio, išbandėte jį lokaliai, įdiegėte Microsoft Foundry aplinkoje ir patvirtinote jo veikimą gamyboje.

---

**Ankstesnis:** [07 - Patikrinkite Playground aplinkoje](07-verify-in-playground.md) · **Pagrindinis puslapis:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors stengiamės užtikrinti tikslumą, prašome atkreipti dėmesį, kad automatizuoti vertimai gali turėti klaidų arba netikslumų. Pirminis dokumentas gimtąja kalba turi būti laikomas autoritetingu šaltiniu. Esant kritinei informacijai, rekomenduojamas profesionalus žmogaus vertimas. Mes neatsakome už bet kokius nesusipratimus ar klaidingas interpretacijas, kilusias naudojant šį vertimą.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->