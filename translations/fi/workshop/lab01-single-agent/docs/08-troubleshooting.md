# Moduuli 8 - Vianmääritys

Tämä moduuli on viiteopas yleisimpiin ongelmiin. Tallenna se kirjanmerkkeihin ja palaa siihen, kun jokin menee vikaan.

---

## 1. Käyttöoikeusvirheet

### 1.1 `agents/write` käyttö estetty

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Juuri:** `Azure AI User` -rooli puuttuu **projektin** tasolla. Tämä on työpajan yleisin virhe.

**Korjaus:**
1. Avaa [portal.azure.com](https://portal.azure.com).
2. Etsi Foundryn **projektin** nimi → napsauta tulosta, jonka tyyppi on **"Microsoft Foundry project"** (EI yläkäyttäjätiliä).
3. **Käyttöoikeuden hallinta (IAM)** → **+ Lisää** → **Lisää roolimääritys**.
4. Rooli: **Azure AI User** → Seuraava.
5. Jäsenet: Valitse itsesi → Tarkista + määritä → Tarkista + määritä.
6. **Odota 1–2 minuuttia** → kokeile uudelleen.

> **Miksi Owner/Contributor ei riitä:** Nämä roolit myöntävät *hallintatoimet* vain. Agentin toiminnot vaativat `agents/write` *data-toiminnon*, joka löytyy vain `Azure AI User`, `Azure AI Developer` tai `Azure AI Owner`. Katso [Foundryn RBAC-dokumentaatio](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` provisioinnin aikana

**Korjaus:** Pyydä ylläpitäjääsi antamaan **Contributor** resurssiryhmälle tai luomaan projekti puolestasi ja myöntämään sinulle **Azure AI User** -rooli siihen.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker-virheet

> Docker on **valinnainen**. Nämä virheet koskevat vain, jos Docker Desktop on asennettu ja laajennus yrittää paikallista rakennusta.

### 2.1 Docker daemon ei ole käynnissä

**Korjaus:** Käynnistä Docker Desktop → odota "käynnissä"-tila → varmista `docker info` → yritä uudelleen.

### 2.2 Rakennus epäonnistuu riippuvuuksien vuoksi

**Korjaus:** Varmista `requirements.txt` oikeinkirjoitus, testaa ensin paikallisesti: `pip install -r requirements.txt`.

### 2.3 Alustayhteensopimattomuus (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Todennusvirheet

### 3.1 `DefaultAzureCredential` epäonnistuu

**Korjaus (yritä järjestyksessä):**
1. `az login` (kirjaudu uudelleen)
2. `az account set --subscription "<id>"` (oikea tilaus)
3. VS Code → Tilit → Kirjaudu ulos → Kirjaudu sisään uudelleen
4. Varmista: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token toimii paikallisesti, mutta ei isännöitynä

**Odotettu:** Isännöidyt agentit käyttävät järjestelmän hallinnoimaa identiteettiä, eivät sinun tunnistettasi. Jos isännöity agentti saa todennusvirheitä:
- Varmista, että `AZURE_AI_MODEL_DEPLOYMENT_NAME` `agent.yaml` osoittaa mallin käyttöönoton nimeen (`FOUNDRY_PROJECT_ENDPOINT` lisätään Foundryn toimesta ajonaikaisesti - älä määritä sitä `agent.yaml`)
- Tarkista, että projektin hallinnoidulla identiteetillä on malli käyttöoikeudet

---

## 4. Mallivirheet

### 4.1 Mallin käyttöönottoa ei löydy

**Korjaus:** Nimi on **herkkä kirjainko'oille**. Vertaa `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` täsmälliseen nimeen Foundryn sivupalkissa → Models.

### 4.2 Odottamaton mallin tulos

**Korjaus:** Tarkista `AGENT_INSTRUCTIONS` `main.py` (leikattu?). Kokeile eri mallia (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Käyttöönotto-ongelmat

### 5.1 ACR-pullointioikeus puuttuu

**Korjaus:** Azure-portaali → Container Registry → Käyttöoikeuden hallinta (IAM) → Lisää **AcrPull** rooli Foundry-projektin hallinnoidulle identiteetille.

### 5.2 Agentti ei käynnisty (jää tilaan "Pending" tai "Failed")

Tarkista konttilokit sivupalkista. Yleisiä syitä:

| Lokiviesti | Korjaus |
|-------------|-----|
| `ModuleNotFoundError` | Lisää puuttuva paketti `requirements.txt`, ota käyttöön uudelleen |
| `ValueError: Missing required environment variables` | Varmista, että `AZURE_AI_MODEL_DEPLOYMENT_NAME` on määritelty `agent.yaml` alla `environment_variables` ja sillä on arvo, sitten ota käyttöön uudelleen. `FOUNDRY_PROJECT_ENDPOINT` lisätään Foundryn toimesta ajonaikaisesti |
| `Address already in use` | Varmista, että vain yksi prosessi käyttää porttia 8088 |

### 5.3 Käyttöönotto aikakatkaisee

**Korjaus:** Tarkista internet-yhteys. Ensimmäinen käyttöönotto siirtää >100 Mt. Käytätkö välityspalvelinta? Konfiguroi Docker Desktopin välityspalvelinasetukset.

---

## 6. Polku B - Foundry Local

### 6.1 Foundry Local ei käynnisty

| Ongelma | Korjaus |
|-------|-----|
| `foundry: command not found` | Asenna uudelleen: `winget install Microsoft.FoundryLocal` |
| Riittämättömät resurssit | Foundry Local tarvitsee ~4 Gt RAM vapaana. Sulje muut sovellukset. |
| Mallin lataus epäonnistuu | Tarkista levytila (mallit ovat 2–8 Gt). Yritä uudelleen: `foundry local models pull <name>` |

### 6.2 Foundry Localin mallivirheet

| Ongelma | Korjaus |
|-------|-----|
| Hitaat vastaukset | Odotettu - paikalliset mallit toimivat CPU:lla, ellei sinulla ole GPU:ta. Ole kärsivällinen. |
| Huono laatuinen tulos | Kokeile suurempaa mallia, jos laitteistosi sallii. `phi-4-mini` on hyvä tasapaino. |
| Yhteys evätty | Varmista, että Foundry Local toimii: `foundry local status`. Käynnistä uudelleen tarvittaessa. |

---

## 7. Pikatarkistus: RBAC-roolit

| Rooli | Laajuus | Oikeudet |
|------|-------|--------|
| **Azure AI User** | Projekti | Data-toiminnot: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekti/Tili | Data-toiminnot + projektin luonti |
| **Azure AI Owner** | Tili | Täysi käyttö + roolien hallinta |
| **Contributor** | Tilaus/Resurssiryhmä | Vain hallintatoimet (**ei** data-toimintoja) |
| **Owner** | Tilaus/Resurssiryhmä | Hallinta + roolien määrittely (**ei** data-toimintoja) |

---

## 8. Työpajan valmistumisen tarkistuslista

| # | Kohta | Moduuli |
|---|------|--------|
| 1 | Esivaatimusten asennus ja varmistus | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit -laajennus asennettu, projekti liitetty (tai Polku B määritetty) | [01](01-setup.md) |
| 3 | Isännöity agentti luotu | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfiguroitu, ohjeet kirjoitettu, riippuvuudet asennettu | [03](03-configure-and-code.md) |
| 5 | Agentti testattu paikallisesti - 3 toimivaa skenaariota läpäisty | [04](04-test-locally.md) |
| 6 | Käyttöönotto Foundryssa (vain Polku A) | [05](05-deploy-to-foundry.md) |
| 7 | Erikoistilanne-/turvatestit läpäisty pilvessä (vain Polku A) | [06](06-verify-in-playground.md) |
| 8 | Yhteenveto tarkistettu, seuraavat askeleet määritetty | [07](07-summary.md) |

---

**Edellinen:** [07 - Yhteenveto](07-summary.md) · **Koti:** [Työpajan README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->