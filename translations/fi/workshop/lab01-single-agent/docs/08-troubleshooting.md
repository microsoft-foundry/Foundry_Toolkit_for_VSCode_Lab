# Moduuli 8 - Vianmääritys

Tämä moduuli on viiteopas yleisiin ongelmiin. Kirjanmerkit se ja palaa, kun jokin menee pieleen.

---

## 1. Oikeusvirheet

### 1.1 `agents/write` -oikeus evätty

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Juuri syy:** Puuttuva `Azure AI User` -rooli **projektin** tasolla. Tämä on yleisin työpajaongelma.

**Korjaus:**
1. Avaa [portal.azure.com](https://portal.azure.com).
2. Etsi Foundry-projektisi nimi → napsauta **"Microsoft Foundry project"** -tyyppistä tulosta (EI päätiliä).
3. **Access control (IAM)** → **+ Lisää** → **Lisää roolimääritys**.
4. Rooli: **Azure AI User** → Seuraava.
5. Jäsenet: Valitse itsesi → Tarkista + myönnä → Tarkista + myönnä.
6. **Odottele 1–2 minuuttia** → yritä uudelleen.

> **Miksi Owner/Contributor ei riitä:** Nämä roolit antavat vain *hallintaoikeudet*. Agentin toiminnot vaativat `agents/write` - *data-toiminnon*, joka löytyy vain `Azure AI User`-, `Azure AI Developer`- tai `Azure AI Owner` -rooleista. Katso [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` käyttöönottovaiheessa

**Korjaus:** Pyydä ylläpitäjääsi määrittämään **Contributor** resurssiryhmään tai antamaan sinulle **Azure AI User** projektissa luomisen yhteydessä.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Odota, kunnes: "Rekisteröity"
```

---

## 2. Docker-virheet

> Docker on **valinnainen**. Nämä koskevat vain, jos Docker Desktop on asennettu ja laajennus yrittää paikallista käännöstä.

### 2.1 Docker daemon ei käynnissä

**Korjaus:** Käynnistä Docker Desktop → odota "running"-tila → varmista `docker info` -komennolla → yritä uudelleen.

### 2.2 Käännös epäonnistuu riippuvuusvirheisiin

**Korjaus:** Tarkista `requirements.txt` oikeinkirjoitus, testaa ensin paikallisesti: `pip install -r requirements.txt`.

### 2.3 Alusta ei vastaa (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentikointivirheet

### 3.1 `DefaultAzureCredential` epäonnistuu

**Korjaus (kokeile järjestyksessä):**
1. `az login` (kirjaudu uudelleen)
2. `az account set --subscription "<id>"` (oikea tilaus)
3. VS Code → Tilit → Kirjaudu ulos → Kirjaudu sisään uudelleen
4. Varmista: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token toimii paikallisesti, mutta ei isännöidyssä

**Odotettu:** Isännöidyt agentit käyttävät järjestelmän hallitsemaa identiteettiä, eivät sinun tunnuksiasi. Jos isännöity agentti saa todennusvirheitä:
- Varmista, että `AZURE_AI_PROJECT_ENDPOINT` agent.yamlissa on oikein
- Tarkista, että projektin hallittu identiteetti pääsee malliin

---

## 4. Mallivirheet

### 4.1 Mallin käyttöönottoa ei löytynyt

**Korjaus:** Nimi on **kokonaan kirjainkoolla erotteleva**. Vertaa `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` täsmälleen Foundry-sivupalkin mallien nimiin.

### 4.2 Odottamaton mallin tulos

**Korjaus:** Tarkista `AGENT_INSTRUCTIONS` main.pyssä (ei olekatkaistu?). Kokeile eri mallia (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Käyttöönotto-ongelmat

### 5.1 ACR pull ei valtuutettu

**Korjaus:** Azure Portal → Container Registry → Access control (IAM) → Lisää **AcrPull** rooli Foundry-projektin hallitulle identiteetille.

### 5.2 Agentti ei käynnisty (jää "Pending" tai "Failed" tilaan)

Tarkista säilön lokit sivupalkista. Yleisiä syitä:

| Lokiviesti | Korjaus |
|-------------|-----|
| `ModuleNotFoundError` | Lisää puuttuva paketti `requirements.txt` tiedostoon, ota käyttöön uudelleen |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Lisää ympäristömuuttuja `agent.yaml` tiedostoon `environment_variables` alle |
| `Address already in use` | Varmista, että vain yksi prosessi kuuntelee porttia 8088 |

### 5.3 Käyttöönoton aikakatkaisu

**Korjaus:** Tarkista internet-yhteys. Ensimmäinen käyttöönotto siirtää >100MB. Käytätkö proxyä? Määritä Docker Desktopin proxy-asetukset.

---

## 6. Reitti B - Foundry Local

### 6.1 Foundry Local ei käynnisty

| Ongelmia | Korjaus |
|-------|-----|
| `foundry: command not found` | Asenna uudelleen: `winget install Microsoft.FoundryLocal` |
| Riittämättömät resurssit | Foundry Local tarvitsee noin 4GB vapaata RAM-muistia. Sulje muut sovellukset. |
| Mallin lataus epäonnistuu | Tarkista levytila (mallit ovat 2–8 GB). Yritä uudelleen: `foundry local models pull <name>` |

### 6.2 Foundry Local mallivirheet

| Ongelmia | Korjaus |
|-------|-----|
| Hitaat vastaukset | Odotettua - paikalliset mallit käyttävät CPU:ta ellei GPU:ta ole. Ole kärsivällinen. |
| Huono laatutulos | Kokeile isompaa mallia, jos laitteistosi sallii. `phi-4-mini` on hyvä tasapaino. |
| Yhteys evätty | Varmista että Foundry Local on käynnissä: `foundry local status`. Käynnistä uudelleen tarvittaessa. |

---

## 7. Pikaviite: RBAC-roolit

| Rooli | Kohde | Myöntää |
|------|-------|--------|
| **Azure AI User** | Projekti | Data-toiminnot: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekti/Tili | Data-toiminnot + projektin luonti |
| **Azure AI Owner** | Tili | Täysi pääsy + roolinhallinta |
| **Contributor** | Tilaus/RG | Vain hallintatoiminnot (**ei** data-toimintoja) |
| **Owner** | Tilaus/RG | Hallinnointi + roolimääritykset (**ei** data-toimintoja) |

---

## 8. Työpajan valmistumislista

| # | Kohta | Moduuli |
|---|------|--------|
| 1 | Esivaatimukset asennettu ja tarkistettu | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit -laajennus asennettu, projekti yhdistetty (tai Reitti B konfiguroitu) | [01](01-setup.md) |
| 3 | Isännöity agentti luotu | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfiguroitu, ohjeet kirjoitettu, riippuvuudet asennettu | [03](03-configure-and-code.md) |
| 5 | Agentti testattu paikallisesti - kolme toimivaa skenaariota läpäisty | [04](04-test-locally.md) |
| 6 | Otettu käyttöön Foundryssä (vain Reitti A) | [05](05-deploy-to-foundry.md) |
| 7 | Reunaehdot/turvallisuustestit läpäisty pilvessä (vain Reitti A) | [06](06-verify-in-playground.md) |
| 8 | Yhteenveto käyty läpi, seuraavat askeleet tunnistettu | [07](07-summary.md) |

---

**Edellinen:** [07 - Yhteenveto](07-summary.md) · **Koti:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->