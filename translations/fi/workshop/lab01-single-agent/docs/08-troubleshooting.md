# Module 8 - Vianetsintä

Tämä moduuli on viiteopas yleisimpiin työpajan aikana esiintyviin ongelmiin. Lisää se kirjanmerkkeihin – tulet palaamaan siihen aina, kun jokin menee vikaan.

---

## 1. Käyttöoikeusvirheet

### 1.1 `agents/write` käyttöoikeus evätty

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Juuri:** Sinulla ei ole `Azure AI User` -roolia **projektin** tasolla. Tämä on yleisin virhe työpajassa.

**Korjaus vaihe vaiheelta:**

1. Avaa [https://portal.azure.com](https://portal.azure.com).
2. Ylimmässä hakupalkissa kirjoita **Foundry-projektisi** nimi (esim. `workshop-agents`).
3. **Tärkeää:** Klikkaa tulosta, joka näyttää tyypin **"Microsoft Foundry project"**, EI päätiliä/hub-resurssia. Nämä ovat eri resursseja eri RBAC-laajuuksilla.
4. Projektisivun vasemman reunan valikossa klikkaa **Access control (IAM)**.
5. Tarkista **Role assignments** -välilehdeltä, onko sinulla jo rooli:
   - Etsi nimesi tai sähköpostiosoitteesi.
   - Jos `Azure AI User` on jo listalla → virheen syy on muualla (katso Vaihe 8 alla).
   - Jos ei ole listalla → jatka roolin lisäämistä.
6. Klikkaa **+ Add** → **Add role assignment**.
7. **Role**-välilehdellä:
   - Etsi [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Valitse se tuloksista.
   - Klikkaa **Next**.
8. **Members**-välilehdellä:
   - Valitse **User, group, or service principal**.
   - Klikkaa **+ Select members**.
   - Etsi nimesi tai sähköpostiosoitteesi.
   - Valitse itsesi tuloksista.
   - Klikkaa **Select**.
9. Klikkaa **Review + assign** → uudelleen **Review + assign**.
10. **Odota 1-2 minuuttia** – RBAC-muutokset vaativat aikaa levitäkseen.
11. Yritä suorittaa virheellinen operaatio uudelleen.

> **Miksi Owner/Contributor ei riitä:** Azure RBAC:lla on kaksi käyttöoikeustyyppiä – *hallintatoiminnot* ja *data-toiminnot*. Owner ja Contributor myöntävät hallintatoimet (resurssien luonti, asetusten muokkaus), mutta agenttien toiminnot vaativat `agents/write` **data-toiminnon**, joka kuuluu vain rooleihin `Azure AI User`, `Azure AI Developer` tai `Azure AI Owner`. Katso [Foundry RBAC -dokumentaatio](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` resurssin provisioinnissa

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Juuri:** Sinulla ei ole oikeutta luoda tai muokata Azure-resursseja tässä tilauksessa/resurssiryhmässä.

**Korjaus:**
1. Pyydä tilauksen ylläpitäjää antamaan sinulle **Contributor**-rooli resurssiryhmään, jossa Foundry-projektisi sijaitsee.
2. Vaihtoehtoisesti pyydä heitä luomaan Foundry-projekti puolestasi ja myöntämään sinulle **Azure AI User** -käyttöoikeus projektille.

### 1.3 `SubscriptionNotRegistered` Microsoft.CognitiveServicesille

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Juuri:** Azure-tilaus ei ole rekisteröinyt resurssin tarjoajaa, jota Foundry tarvitsee.

**Korjaus:**

1. Avaa terminaali ja suorita:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Odota rekisteröinnin valmistumista (kestää 1-5 minuuttia):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Odotettu tulos: `"Registered"`
3. Yritä operaatio uudelleen.

---

## 2. Docker-virheet (vain jos Docker on asennettu)

> Docker on **valinnainen** tähän työpajaan. Näitä virheitä ilmenee vain, jos sinulla on Docker Desktop asennettuna ja Foundry-laajennus yrittää rakentaa paikallista konttia.

### 2.1 Docker daemon ei käynnissä

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Korjaus vaihe vaiheelta:**

1. Löydä Docker Desktop Käynnistä-valikosta (Windows) tai Sovelluksista (macOS) ja avaa se.
2. Odota, että Docker Desktop -ikkuna näyttää **"Docker Desktop is running"** -tyyppisen viestin – yleensä kestää 30-60 sekuntia.
3. Etsi Docker-maijalogo ilmoitusalueelta (Windows) tai valikkoriviltä (macOS). Vie hiiri ikonien päälle statusin näkemiseksi.
4. Tarkista terminaalissa:
   ```powershell
   docker info
   ```
   Jos tämä tulostaa Docker-järjestelmätietoja (Server Version, Storage Driver jne.), Docker on käynnissä.
5. **Windows-erikoisohje:** Jos Docker ei vieläkään käynnisty:
   - Avaa Docker Desktop → **Settings** (hammasrataskuvake) → **General**.
   - Varmista, että **Use the WSL 2 based engine** on valittuna.
   - Klikkaa **Apply & restart**.
   - Jos WSL 2 ei ole asennettu, suorita `wsl --install` korotetussa PowerShellissä ja käynnistä tietokone uudelleen.
6. Yritä käyttöönotto uudelleen.

### 2.2 Docker build epäonnistuu riippuvuusvirheiden takia

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Korjaus:**
1. Avaa `requirements.txt` ja varmista, että kaikki paketit on kirjoitettu oikein.
2. Varmista, että versioiden lukitus on oikea:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Testaa asennus ensin paikallisesti:
   ```bash
   pip install -r requirements.txt
   ```
4. Jos käytät yksityistä pakettivarastoa, varmista että Dockerilla on verkkoyhteys siihen.

### 2.3 Konttialustan yhteensopimattomuus (Apple Silicon)

Jos otat käyttöön Apple Silicon -Macilta (M1/M2/M3/M4), kontti on rakennettava `linux/amd64` -alustalle, koska Foundryn konttiajuri käyttää AMD64:ää.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry-laajennuksen deploy-komento hoitaa tämän automaattisesti useimmissa tapauksissa. Jos näet arkkitehtuurivirheitä, rakenna manuaalisesti `--platform`-lipulla ja ota yhteyttä Foundryn tiimiin.

---

## 3. Todennusvirheet

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ei saa tokenia

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Juuri:** Mikään `DefaultAzureCredential`-ketjun todennustavoista ei tuota voimassa olevaa tokenia.

**Korjaus - kokeile jokainen vaihe järjestyksessä:**

1. **Kirjaudu uudelleen Azure CLI:llä** (yleisin korjaus):
   ```bash
   az login
   ```
   Selainikkuna aukeaa. Kirjaudu sisään ja palaa sitten VS Codeen.

2. **Aseta oikea tilaus:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Jos tämä ei ole oikea tilaus:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Kirjaudu uudelleen VS Codessa:**
   - Klikkaa vasemmasta alakulmasta **Accounts**-kuvaketta (henkilöhahmo).
   - Klikkaa tilisi nimeä → **Sign Out**.
   - Klikkaa Accounts-kuvaketta uudelleen → **Sign in to Microsoft**.
   - Suorita selainkirjautuminen loppuun.

4. **Service principal -tilanteissa (CI/CD):**
   - Määritä nämä ympäristömuuttujat `.env`-tiedostoon:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Käynnistä agenttiprosessi uudelleen.

5. **Tarkista tokenin välimuisti:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Jos epäonnistuu, CLI-tokenisi on vanhentunut. Suorita `az login` uudelleen.

### 3.2 Token toimii paikallisesti, mutta ei isännöidyssä käyttöönotossa

**Juuri:** Isännöity agentti käyttää järjestelmän hallitsemaa identiteettiä, joka on eri kuin henkilökohtainen todentamisesi.

**Korjaus:** Tämä on odotettua – hallittu identiteetti provisioidaan automaattisesti käyttöönoton aikana. Jos isännöity agentti saa silti todennusvirheitä:
1. Varmista, että Foundry-projektin hallittu identiteetti pääsee Azure OpenAI -resurssille.
2. Tarkista, että `PROJECT_ENDPOINT` agent.yaml:ssa on oikein.

---

## 4. Mallivirheet

### 4.1 Mallin käyttöönottoa ei löydy

```
Error: Model deployment not found / The specified deployment does not exist
```

**Korjaus vaihe vaiheelta:**

1. Avaa `.env`-tiedosto ja merkitse ylös `AZURE_AI_MODEL_DEPLOYMENT_NAME` -arvo.
2. Avaa VS Codessa **Microsoft Foundry** -sivupalkki.
3. Laajenna projektisi → **Model Deployments**.
4. Vertaa siellä olevaa käyttöönoton nimeä `.env`:in arvoon.
5. Nimi on **kirjainkokoriippuvainen** – `gpt-4o` ei ole sama kuin `GPT-4o`.
6. Jos nimet eivät täsmää, päivitä `.env` käyttämään täsmällistä nimeä, joka näkyy sivupalkissa.
7. Hallinnoidussa käyttöönotossa päivitä myös `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Malli vastaa odottamattomasti

**Korjaus:**
1. Tarkista `EXECUTIVE_AGENT_INSTRUCTIONS` -vakio `main.py`:ssä. Varmista, ettei se ole katkennut tai korruptoitunut.
2. Tarkista mallin lämpötilan asetus (jos konfiguroitavissa) – matalammat arvot antavat deterministisempiä vastauksia.
3. Vertaile käyttöönotettua mallia (esim. `gpt-4o` vs `gpt-4o-mini`) – eri mallit tarjoavat erilaisia ominaisuuksia.

---

## 5. Käyttöönotto-ongelmat

### 5.1 ACR:n nouto-oikeus

```
Error: AcrPullUnauthorized
```

**Juuri:** Foundry-projektin hallittu identiteetti ei pääse hakemaan konttikuvajaa Azure Container Registry -palvelusta.

**Korjaus vaihe vaiheelta:**

1. Avaa [https://portal.azure.com](https://portal.azure.com).
2. Etsi ylähaussa **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Klikkaa rekisteriä, joka liittyy Foundry-projektiisi (yleensä sama resurssiryhmä).
4. Vasemman reunan valikossa klikkaa **Access control (IAM)**.
5. Klikkaa **+ Add** → **Add role assignment**.
6. Etsi ja valitse **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Klikkaa **Next**.
7. Valitse **Managed identity** → klikkaa **+ Select members**.
8. Etsi ja valitse Foundry-projektin hallittu identiteetti.
9. Klikkaa **Select** → **Review + assign** → **Review + assign**.

> Tämä rooliajo yleensä hoidetaan automaattisesti Foundry-laajennuksen toimesta. Jos näet tämän virheen, automaattinen asennus saattaa olla epäonnistunut. Voit myös yrittää uudelleenottamista - laajennus voi yrittää asennusta uudelleen.

### 5.2 Agentti ei käynnisty käyttöönoton jälkeen

**Oireet:** Kontin tila pysyy "Pending" yli 5 minuuttia tai näyttää "Failed".

**Korjaus vaihe vaiheelta:**

1. Avaa VS Codessa **Microsoft Foundry** -sivupalkki.
2. Klikkaa isännöityä agenttiasi → valitse versio.
3. Tarkastelupaneelissa katso **Container Details** → etsi **Logs**-osio tai linkki.
4. Lue kontin käynnistyslokit. Yleisiä syitä:

| Lokiviesti | Syy | Korjaus |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Puuttuva riippuvuus | Lisää se `requirements.txt`:iin ja ota käyttöön uudelleen |
| `KeyError: 'PROJECT_ENDPOINT'` | Puuttuva ympäristömuuttuja | Lisää ympäristömuuttuja `agent.yaml`:in `env:`-kohtaan |
| `OSError: [Errno 98] Address already in use` | Porttikonflikti | Varmista, että `agent.yaml` sisältää `port: 8088` ja vain yksi prosessi kuuntelee porttia |
| `ConnectionRefusedError` | Agentti ei aloittanut kuuntelua | Tarkista `main.py`:n `from_agent_framework()`-kutsu suoritetaan käynnistyksessä |

5. Korjaa ongelma ja ota käyttöön uudelleen [Moduuli 6](06-deploy-to-foundry.md).

### 5.3 Käyttöönotto aikakatkaistaan

**Korjaus:**
1. Tarkista internet-yhteytesi – Docker-push voi olla suuri (>100Mt ensimmäisellä käyttöönotolla).
2. Jos olet yritysverkon takana, varmista että Docker Desktopin proxy-asetukset ovat oikein: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Kokeile uudelleen – verkkohäiriöt voivat aiheuttaa tilapäisiä virheitä.

---

## 6. Pikamuistilista: RBAC-roolit

| Rooli | Tyypillinen laajuus | Mitä rooli antaa |
|------|---------------|----------------|
| **Azure AI User** | Projekti | Data-toiminnot: agenttien rakentaminen, käyttöönotto ja kutsuminen (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekti tai Tili | Data-toiminnot + projektin luonti |
| **Azure AI Owner** | Tili | Täysi pääsy + roolijakojen hallinta |
| **Azure AI Project Manager** | Projekti | Data-toiminnot + voi myöntää Azure AI User -roolin muille |
| **Contributor** | Tilauksen/Resurssiryhmän | Hallintatoiminnot (resurssien luonti/poisto). **EI sisällä data-toimintoja** |
| **Owner** | Tilauksen/Resurssiryhmän | Hallintatoiminnot + roolijakojen hallinta. **EI sisällä data-toimintoja** |
| **Reader** | Mikä tahansa | Vain luku hallintaan |

> **Tärkeä huomio:** `Owner` ja `Contributor` eivät sisällä data-toimintoja. Agenttien toimintaan tarvitset aina `Azure AI *` -roolin. Tämän työpajan minimirooli on **Azure AI User** **projektin** tasolla.

---

## 7. Työpajan suorituslista

Käytä tätä lopullisena tarkistuslistana, että kaikki on tehty:

| # | Asia | Moduuli | Hyväksytty? |
|---|------|--------|---|
| 1 | Kaikki esivaatimukset asennettu ja tarkistettu | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit ja Foundry-laajennukset asennettu | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry-projekti luotu (tai olemassa oleva valittu) | [02](02-create-foundry-project.md) | |
| 4 | Malli otettu käyttöön (esim. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI -käyttäjärooli määritetty projektin laajuudessa | [02](02-create-foundry-project.md) | |
| 6 | Isännöity agenttiprojekti alustettu (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfiguroitu PROJECT_ENDPOINT- ja MODEL_DEPLOYMENT_NAME-arvoilla | [04](04-configure-and-code.md) | |
| 8 | Agentin ohjeet muokattu tiedostossa main.py | [04](04-configure-and-code.md) | |
| 9 | Virtuaaliympäristö luotu ja riippuvuudet asennettu | [04](04-configure-and-code.md) | |
| 10 | Agentti testattu paikallisesti F5:llä tai terminaalissa (4 savutestiä läpäisty) | [05](05-test-locally.md) | |
| 11 | Otettu käyttöön Foundry Agent Service -palvelussa | [06](06-deploy-to-foundry.md) | |
| 12 | Kontin tila näyttää "Started" tai "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Varmistus VS Code Playgroundissa (4 savutestiä läpäisty) | [07](07-verify-in-playground.md) | |
| 14 | Varmistus Foundry Portalin Playgroundissa (4 savutestiä läpäisty) | [07](07-verify-in-playground.md) | |

> **Onnittelut!** Jos kaikki kohdat on ruksetettu, olet suorittanut koko työpajan. Olet rakentanut isännöidyn agentin alusta alkaen, testannut sen paikallisesti, ottanut sen käyttöön Microsoft Foundryssa ja varmistanut sen toimivuuden tuotantoympäristössä.

---

**Edellinen:** [07 - Varmista Playgroundissa](07-verify-in-playground.md) · **Koti:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttäen tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulisi pitää virallisena lähteenä. Tärkeissä asioissa suositellaan ammattimaisen ihmiskääntäjän käyttöä. Emme ole vastuussa mahdollisista väärinymmärryksistä tai virhetulkinnoista, jotka johtuvat tämän käännöksen käytöstä.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->