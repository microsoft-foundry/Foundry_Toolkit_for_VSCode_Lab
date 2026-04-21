# Moodul 8 - Tõrkeotsing

See moodul on referentsjuhend kõigi tavapäraste probleemide jaoks, millega töökoda ajal kokku puutute. Lisage see järjehoidjatesse – naasete sinna alati, kui midagi valesti läheb.

---

## 1. Lubade vead

### 1.1 Luba `agents/write` keelatud

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Põhjus:** Teil puudub roll `Azure AI User` **projekti** tasemel. See on töökoja kõige sagedasem viga.

**Parandus - samm-sammult:**

1. Avage [https://portal.azure.com](https://portal.azure.com).
2. Tippige ülaosas asuvasse otsinguribale oma **Foundry projekti** nimi (nt `workshop-agents`).
3. **Oluline:** Klõpsake tulemusel, kus tüübiks on **"Microsoft Foundry project"**, MITTE vanema konto/hub ressurss. Need on erinevad ressursid ja erinevate RBAC ulatustega.
4. Projekti lehe vasakus navigeerimises klõpsake **Access control (IAM)**.
5. Kontrollige, kas teil on juba roll:
   - Otsige oma nime või e-posti järgi.
   - Kui `Azure AI User` on juba loendis → veal on mõni muu põhjus (vaadake allpool sammu 8).
   - Kui pole loendis → jätkake rolli lisamisega.
6. Klõpsake **+ Add** → **Add role assignment**.
7. Vahekaardil **Role**:
   - Otsige rolli [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Valige see tulemustest.
   - Klõpsake **Next**.
8. Vahekaardil **Members**:
   - Valige **User, group, or service principal**.
   - Klõpsake **+ Select members**.
   - Otsige oma nime või e-posti aadressi.
   - Valige ennast.
   - Klõpsake **Select**.
9. Klõpsake **Review + assign** → uuesti **Review + assign**.
10. **Oodake 1–2 minutit** – RBAC muudatuste jõustumine võtab aega.
11. Proovige ebaõnnestunud toimingut uuesti.

> **Miks Owner/Contributor ei piisa:** Azure RBAC-is on kaks tüüpi õigusi – *haldustegevused* ja *andmepõhised tegevused*. Owner ja Contributor annavad haldustegevuste õigused (ressursside loomine, seadete muutmine), kuid agendi toimingud vajavad `agents/write` **andmepõhist tegevust**, mis on ainult rollides `Azure AI User`, `Azure AI Developer` või `Azure AI Owner`. Vaadake [Foundry RBAC dokumentatsiooni](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` ressursside loomisel

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Põhjus:** Teil puudub õigus luua või muuta Azure ressursse selles tellimuses/ressursigrupis.

**Parandus:**
1. Paluge oma tellimuse administraatoril määrata teile ressurssigrupis, kus teie Foundry projekt asub, roll **Contributor**.
2. Või laske neil luua Foundry projekt teie eest ja anda teile roll **Azure AI User** projektil.

### 1.3 `SubscriptionNotRegistered` veateade [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) jaoks

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Põhjus:** Azure tellimus ei ole registreerinud vajaliku resource provideri kasutamiseks Foundry jaoks.

**Parandus:**

1. Avage terminal ja käivitage:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Oodake registreerimise lõpetamist (võib kesta 1–5 minutit):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Oodatud väljund: `"Registered"`
3. Proovige toiming uuesti.

---

## 2. Dockeri vead (ainult kui Docker on paigaldatud)

> Docker on selle töökoja jaoks **valikuline**. Need vead kehtivad ainult, kui teil on Docker Desktop paigaldatud ja Foundry laiendus üritab kohalikku konteinerit ehitada.

### 2.1 Docker daemon ei tööta

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Parandus - samm-sammult:**

1. Leidke Start-menüüst (Windows) või Applications kaustast (macOS) Docker Desktop ja käivitage see.
2. Oodake, kuni Docker Desktop aken näitab **"Docker Desktop is running"** – tavaliselt võtab see 30–60 sekundit.
3. Otsige süsteemses salves (Windows) või menüüribal (macOS) Docker vaala ikooni. Kinnitage olek kursoriga ikooni kohal.
4. Kontrollige terminalis:
   ```powershell
   docker info
   ```
   Kui see prindib Docker süsteemiteavet (Server Version, Storage Driver jms), siis Docker töötab.
5. **Windowsi puhul spetsiifiline:** Kui Docker ikkagi ei käivitu:
   - Avage Docker Desktop → **Settings** (hammasrattakuju) → **General**.
   - Veenduge, et valik **Use the WSL 2 based engine** on märgitud.
   - Klõpsake **Apply & restart**.
   - Kui WSL 2 pole paigaldatud, käivitage kõrgendatud PowerShellis `wsl --install` ja taaskäivitage arvuti.
6. Proovige juurutust uuesti.

### 2.2 Docker build ebaõnnestub sõltuvusvigade tõttu

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Parandus:**
1. Avage `requirements.txt` ja kontrollige, et kõik pakettnimed oleksid õigesti kirjutatud.
2. Veenduge, et versiooni lukustused on õiged:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Testige esmalt kohapeal paigaldamist:
   ```bash
   pip install -r requirements.txt
   ```
4. Kui kasutate privaatset paketiregistrit, kontrollige, et Dockeril on sellele võrguühendus.

### 2.3 Konteineri platvormi sobimatus (Apple Silicon)

Kui juurutate Apple Silicon Macilt (M1/M2/M3/M4), peab konteiner olema ehitatud platvormile `linux/amd64`, sest Foundry konteineriaeg töötab AMD64 peal.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry laienduse juurutamiskäsk käsitleb seda automaatselt enamasti. Kui näete arhitektuuripõhiseid vigu, ehitage konteiner käsitsi lipuga `--platform` ja võtke ühendust Foundry meeskonnaga.

---

## 3. Autentimisvead

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ei suuda tokenit hankida

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Põhjus:** Ükski `DefaultAzureCredential` ketis olevatest volituste allikatest ei omanud kehtivat tokenit.

**Parandus - proovige samme järjekorras:**

1. **Logige uuesti sisse Azure CLI kaudu** (sagedaseim lahendus):
   ```bash
   az login
   ```
   Avaneb brauseri aken. Logige sisse ja tulge tagasi VS Code-sse.

2. **Seadistage õige tellimus:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Kui see pole õige tellimus:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Logige uuesti sisse VS Code kaudu:**
   - Klõpsake all vasakus nurgas ikooni **Accounts** (inimese ikoon).
   - Klõpsake oma konto nime → **Sign Out**.
   - Klõpsake uuesti Accounts ikooni → **Sign in to Microsoft**.
   - Täitke brauseri sisselogimisprotsess.

4. **Teenuse põhiroll (ainult CI/CD stsenaariumides):**
   - Määrake need keskkonnamuutujad oma `.env` failis:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Seejärel taaskäivitage agendi protsess.

5. **Kontrollige tokeni vahemälu:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Kui see ebaõnnestub, on teie CLI token aegunud. Käivitage uuesti `az login`.

### 3.2 Token töötab kohapeal, kuid mitte hostitud juurutuses

**Põhjus:** Hostitud agent kasutab süsteemi hallatavat identiteeti, mis erineb teie isiklikust volitusest.

**Parandus:** See on oodatud käitumine – hallatav identiteet luuakse automaatselt juurutuse käigus. Kui hostitud agent saab ikka autentimisveateateid:
1. Kontrollige, et Foundry projekti hallatav identiteet pääseks ligi Azure OpenAI ressursile.
2. Kontrollige, et `PROJECT_ENDPOINT` väärtus `agent.yaml`-is oleks õige.

---

## 4. Mudeli vead

### 4.1 Mudeli juurutus ei leitud

```
Error: Model deployment not found / The specified deployment does not exist
```

**Parandus - samm-sammult:**

1. Avage oma `.env` fail ja märkige üles `AZURE_AI_MODEL_DEPLOYMENT_NAME` väärtus.
2. Avage VS Code’s **Microsoft Foundry** küljeriba.
3. Laiendage oma projekti → **Model Deployments**.
4. Võrrelge seal nähtavat juurutuse nime oma `.env` väärtusega.
5. Nimi on **täht-tundlik** – `gpt-4o` ei ole sama mis `GPT-4o`.
6. Kui need ei ühti, uuendage `.env` nii, et see täpselt vastaks küljeribas kuvatavale nimele.
7. Hostitud juurutuse korral uuendage ka `agent.yaml` faili:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Mudel vastab ootamatule sisule

**Parandus:**
1. Kontrollige `EXECUTIVE_AGENT_INSTRUCTIONS` konstanti `main.py` failis. Veenduge, et see poleks lõigatud ega rikutud.
2. Kontrollige mudeli temperatuuri seadet (kui seadistatav) – madalamad väärtused annavad deterministlikumaid vastuseid.
3. Võrrelge kasutatavat mudelit (nt `gpt-4o` vs `gpt-4o-mini`) – erinevate mudelite võimed on erinevad.

---

## 5. Juurutamise vead

### 5.1 ACR pull autorisatsioon

```
Error: AcrPullUnauthorized
```

**Põhjus:** Foundry projekti hallatav identiteet ei saa tõmmata konteineripilti Azure Container Registryst.

**Parandus - samm-sammult:**

1. Avage [https://portal.azure.com](https://portal.azure.com).
2. Otsige ülaosas otsinguribal **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Klõpsake registril, mis on seotud teie Foundry projektiga (tavaliselt samas ressurssigrupis).
4. Vasakus navigeerimises valige **Access control (IAM)**.
5. Klõpsake **+ Add** → **Add role assignment**.
6. Otsige ja valige roll **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Klõpsake **Next**.
7. Valige **Managed identity** → klõpsake **+ Select members**.
8. Leidke ja valige Foundry projekti hallatav identiteet.
9. Klõpsake **Select** → **Review + assign** → **Review + assign**.

> See rolli määramine tehakse tavaliselt automaatselt Foundry laienduse poolt. Kui näete seda viga, võib automaatne seadistus olla ebaõnnestunud. Võite proovida ka juurutust uuesti – laiendus võib seadistuse uuesti teha.

### 5.2 Agent ei käivitu pärast juurutust

**Sümptomid:** Konteineri staatus jääb kauemaks kui 5 minutiks "Pending" või näitab "Failed".

**Parandus - samm-sammult:**

1. Avage VS Code’s küljeriba **Microsoft Foundry**.
2. Klõpsake oma hostitud agendil → valige versioon.
3. Detailide paneelis kontrollige **Container Details** → otsige **Logs** sektsiooni või linki.
4. Lugege konteineri käivitusribasid. Levinud põhjused:

| Logisõnum | Põhjus | Parandus |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Puuduv sõltuvus | Lisage see `requirements.txt` faili ja juurutage uuesti |
| `KeyError: 'PROJECT_ENDPOINT'` | Puuduv keskkonnamuutuja | Lisage keskkonnamuutuja `agent.yaml` failis `env:` alla |
| `OSError: [Errno 98] Address already in use` | Pordi konflikt | Veenduge, et `agent.yaml` sisaldab `port: 8088` ja ainult üks protsess seda kasutab |
| `ConnectionRefusedError` | Agent ei hakanud kuulama | Kontrollige `main.py` faili – `from_agent_framework()` peab jooksma käivitamisel |

5. Lahendage probleem ja juurutage uuesti alates [Moodul 6](06-deploy-to-foundry.md).

### 5.3 Juurutamise aegumine

**Parandus:**
1. Kontrollige oma internetiühendust – Docker push võib olla suur (>100MB esimesel juurutamisel).
2. Kui olete ettevõttesisese proksiga võrgu taga, seadistage Docker Desktopi proksiseaded: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Proovige uuesti – võrguprobleemid võivad põhjustada ajutisi tõrkeid.

---

## 6. Kiire viide: RBAC rollid

| Roll | Tavaliselt ulatus | Milliseid õigusi annab |
|------|-------------------|-----------------------|
| **Azure AI User** | Projekt | Andmepõhised tegevused: agendi loomine, juurutus, käivitamine (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt või Konto | Andmepõhised tegevused + projekti loomine |
| **Azure AI Owner** | Konto | Täielik juurdepääs + rollimäärajate haldus |
| **Azure AI Project Manager** | Projekt | Andmepõhised tegevused + võib anda Azure AI User rolli teistele |
| **Contributor** | Tellimus/RG | Haldustegevused (ressursside loomine/kustutamine). **EI SISALDA andmepõhiseid tegevusi** |
| **Owner** | Tellimus/RG | Haldustegevused + rollimääramine. **EI SISALDA andmepõhiseid tegevusi** |
| **Reader** | Suvaline | Ainult lugemisõigus haldusülesannete jaoks |

> **Peamine järeldus:** Rollid `Owner` ja `Contributor` EI SISALDA andmepõhiseid tegevusi. Agendi toimingute jaoks vajate alati mõnda `Azure AI *` rolli. Selle töökoja miinimumnõue on roll **Azure AI User**, projekti ulatuses.

---

## 7. Töökoja lõpetamise kontrollnimekiri

Kasutage seda viimase kinnitusena, et olete kõik lõpetanud:

| # | Punkt | Moodul | Läbinud? |
|---|--------|--------|----------|
| 1 | Kõik eeltingimused paigaldatud ja kontrollitud | [00](00-prerequisites.md) | |
| 2 | Paigaldatud Foundry Toolkit ja Foundry laiendused | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry projekt loodud (või valitud olemasolev projekt) | [02](02-create-foundry-project.md) | |
| 4 | Mudel juurutatud (nt gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI kasutaja roll määratud projekti ulatuses | [02](02-create-foundry-project.md) | |
| 6 | Hostitud agendi projekt loodud (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfigureeritud koos PROJECT_ENDPOINT ja MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agendi juhised kohandatud failis main.py | [04](04-configure-and-code.md) | |
| 9 | Virtuaalne keskkond loodud ja sõltuvused installitud | [04](04-configure-and-code.md) | |
| 10 | Agent testitud lokaalselt F5 või terminali abil (läbitud 4 kiiret testi) | [05](05-test-locally.md) | |
| 11 | Juurutatud Foundry agendi teenusesse | [06](06-deploy-to-foundry.md) | |
| 12 | Konteineri olek näitab "Started" või "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Kontrollitud VS Code mänguväljakus (läbitud 4 kiiret testi) | [07](07-verify-in-playground.md) | |
| 14 | Kontrollitud Foundry portaali mänguväljakus (läbitud 4 kiiret testi) | [07](07-verify-in-playground.md) | |

> **Palju õnne!** Kui kõik punktid on märgitud, olete lõpetanud kogu töötoa. Olete loonud hostitud agendi nullist, testinud seda lokaalselt, juurutanud Microsoft Foundrysse ja valideerinud tootmiskeskkonnas.

---

**Eelmine:** [07 - Kontroll mänguväljakus](07-verify-in-playground.md) · **Avaleht:** [Töötoa README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tähelepanek**:
See dokument on tõlgitud AI tõlketeenuse [Co-op Translator](https://github.com/Azure/co-op-translator) abil. Kuigi püüame tagada täpsust, palun arvestage, et automatiseeritud tõlked võivad sisaldada vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse professionaalset inimtõlget. Me ei vastuta selle tõlke kasutamisest tulenevate arusaamatuste või valesti mõistmiste eest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->