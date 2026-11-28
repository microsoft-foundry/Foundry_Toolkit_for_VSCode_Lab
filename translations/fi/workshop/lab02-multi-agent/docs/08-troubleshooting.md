# Moduuli 8 - Vianmääritys

Tämä moduuli kattaa yleiset virheet, korjaukset ja virheenetsintästrategiat, jotka ovat spesifisiä moniedustajan työnkululle.

## Agentin tulostusongelmat

### GapAnalyzer sanoo ”Minulla ei vieläkään ole vastaavaa raporttia”

**Oire:** GapAnalyzerin vastaus pyytää sinua liittämään vastaavan raportin, jossa on ”Puuttuvat taidot” ja ”Sertifiointivajaukset.” Tämä tapahtuu, vaikka olisit lähettänyt sekä ansioluettelon että työkuvauksen.

**Syy:** Työkuvauksen tekstiä ei siirretty eteenpäin JD Agentille. `context_mode="last_agent"`:ssa `resume_executor` on ainoa suoritin, joka näkee käyttäjän alkuperäisen viestin. Jos `RESUME_PARSER_INSTRUCTIONS` ei sisällytä työkuvauksen tekstiä tulosteeseensa, JD Agentilla ei ole työkuvausta analysoitavaksi, MatchingAgent ei pysty laskemaan sopivuuspistettä ja GapAnalyzer saa merkityksettömän syötteen.

**Diagnoosi:**

Palvelimen lokeista etsi MatchingAgentin span. Jos se sisältää:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
välitys puuttuu tai on rikki.

**Korjaus:** Varmista, että `RESUME_PARSER_INSTRUCTIONS` `main.py` sisältää `[JOB DESCRIPTION PASS-THROUGH]`-osion ja säännön:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Varmista myös, että `JOB_DESCRIPTION_INSTRUCTIONS` sisältää `[PARSED RESUME PASS-THROUGH]`-välityssäännön:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jos jompikumpi ohjeistuslohko on erityinen ja alustettu wizardilla, korvaa se täydellisellä versiolla osoitteesta [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent tulostaa ”Ei voida laskea sopivuuspistettä - työkuvausta ei toimitettu”

Sama perimmäinen syy kuin yllä. MatchingAgent sai JD Agentin tulosteen, mutta `[PARSED RESUME PASS-THROUGH]`-osio puuttui tai oli tyhjä, joten se ei voinut verrata kahta profiilia. Varmista:
1. `JOB_DESCRIPTION_INSTRUCTIONS` sisältää välityssäännön: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` kertoo agentille, että sen tulee etsiä `[JD REQUIREMENTS]` ja `[PARSED RESUME PASS-THROUGH]`-osioita.

Korvaa molemmat ohjeistukset täydellisillä versioilla osoitteesta [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Vastaus näkyy kahdesti

**Oire:** GapAnalyzerin tuloste (tai koko putken tulos) näkyy kahdesti Agentin tarkastelijan vastauksessa.

**Syy:** `WorkflowBuilder` käyttää TAI-semantikkaa sisään tuleville reunoille - alavirran suoritin käynnistyy heti, kun **minkä tahansa** edeltäjän suoritus on valmis. Jos `matching_executor`:lla on kaksi sisään tulevaa reunaa (yksi `resume_executor`:sta ja yksi `jd_executor`:sta), se aktivoituu kahdesti: kerran ResumeParserin päätyttyä ja uudelleen JD Agentin päätyttyä. GapAnalyzer puolestaan suorittuu silloin myös kahdesti.

**Korjaus:** Varmista, että `WorkflowBuilder`-kaavio on ehdottoman peräkkäinen putkisto ilman fan-in:tä:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jos löydät ylimääräisen `.add_edge(resume_executor, matching_executor)`-rivin, poista se. `[PARSED RESUME PASS-THROUGH]`-välitys JD Agentin tulosteessa antaa jo MatchingAgentille pääsyn ansioluetteloon.

---

## Ympäristö- ja konfigurointi-ongelmat

### Puuttuvat tai väärät `.env` arvot

`.env`-tiedoston tulee olla `PersonalCareerCopilot/`-hakemistossa (saman tason kansio kuin `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Odotettu `.env`-sisältö:

**Polku A - Foundryn pilvi:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Polku B - Foundry paikallinen:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Molemmat polut käyttävät `FOUNDRY_PROJECT_ENDPOINT`:a. Arvo eroaa: pilvi käyttää `https://` Foundry-päätettä; paikallinen käyttää `http://localhost:5273/v1`. Suorita `foundry model list` varmistaaksesi tarkan mallin aliaksen polulle B.

> **Miten löydät `FOUNDRY_PROJECT_ENDPOINT`-arvosi:** 
- Avaa **Foundry Toolkit** -sivupalkki VS Codessa → napsauta projektiasi hiiren oikealla → **Copy Project Endpoint**. 
- Tai mene [Azure Portal](https://portal.azure.com) → oma Foundry-projektisi → **Yleiskatsaus** → **Project endpoint**.

> **Miten löydät `AZURE_AI_MODEL_DEPLOYMENT_NAME`-arvosi:** Foundry Toolkit -sivupalkissa laajenna projektisi → **Models** → etsi käyttämäsi malli (esim. `gpt-4.1-mini`).

### Ympäristömuuttujien prioriteetti

`main.py` käyttää `load_dotenv(override=True)`-järjestelmää, mikä tarkoittaa:

| Prioriteetti | Lähde | Voittaa molemmat asetettuna? |
|-------------|--------|---------------------------|
| 1 (korkein) | `.env` tiedosto | Kyllä |
| 2 | Shell / säiliöympäristömuuttuja | Käytetään, kun samaa avainta ei ole `.env`:ssa |

Paikallisessa kehityksessä tämä tekee `.env` totuuden lähteeksi (muutokset `.env`:ssa vaikuttavat välittömästi ajoihin). Hostatussa käyttöönotossa Foundry injektoi ympäristömuuttujat säiliötasolla; koska `.env` ei ole osa otettua kuvaa tässä lab-asetuksessa, käytetään arvoja, jotka on injektoitu säiliölle.

---

## Versioyhteensopivuus

### Paketiversiomatriisi

Moniedustajan työnkulku vaatii tiettyjä pakettiversioita. Versioiden yhteensopimattomuus aiheuttaa suoritusaikavirheitä.

| Paketti | Vaadittu versio | Tarkastuskomento |
|---------|-----------------|------------------|
| `agent-framework-foundry` | uusin | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | uusin | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | uusin | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Yleisiä versiovirheitä

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Tarkista kaikki versiot kerralla

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Odotettu tuloste:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Käyttöönotto-ongelmat

### Säiliö ei käynnisty käyttöönoton jälkeen

1. **Tarkista säiliön lokit:**
   - Avaa **Foundry Toolkit** -sivupalkki → projektisi alta klikkaa **Agents** → **Hosted Agent** -välilehti → klikkaa agenttiasi. Tarkista **Tila** -välilehdeltä ja avaa sitten **Playground** -välilehti sekä käytä **Lokit** -välilehteä **Istuntojen tiedoissa** nähdäksesi säiliön tulosteen.
   - Etsi Pythonin pinon jälkiä tai puuttuvien moduulien virheilmoituksia.

2. **Yleiset säiliön käynnistysvirheet:**

   | Virhe lokissa | Syy | Korjaus |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` puuttuu paketti | Lisää paketti, ota käyttöön uudelleen |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` tai `.env` ympäristömuuttujat puuttuvat | Päivitä `agent.yaml` → `environment_variables` osio (hostattu) tai `.env` (paikallinen) |
   | `azure.identity.CredentialUnavailableError` | Hallittu identiteetti ei määritetty | Foundry määrittää tämän automaattisesti - varmista, että otat käyttöön laajennuksen kautta |
   | `OSError: port 8088 already in use` | Dockerfile paljastaa väärän portin tai porttikonflikti | Tarkista `EXPOSE 8088` Dockerfilessä ja `CMD ["python", "main.py"]` |
   | Säiliö poistuu koodilla 1 | Käsittelemätön poikkeus `main()` | Testaa paikallisesti ensin ([Moduuli 5](05-test-locally.md)) löytääksesi virheet ennen käyttöönottoa |

3. **Ota käyttöön uudelleen korjauksen jälkeen:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → valitse sama agentti → ota käyttöön uusi versio.

### Käyttöönotto kestää liian kauan

Moniedustajan säiliöt käynnistyvät hitaammin, koska ne luovat 4 agentti-instanssia käynnistyessään. Normaalit käynnistysajat:

| Vaihe | Odotettu kesto |
|-------|-----------------|
| Säiliökuvan rakentaminen | 1–3 minuuttia |
| Kuvan työntö ACR:ään | 30–60 sekuntia |
| Säiliön käynnistys (yksittäinen agentti) | 15–30 sekuntia |
| Säiliön käynnistys (moniedustaja) | 30–120 sekuntia |
| Agentti käytettävissä Playgroundsissa | 1–2 minuuttia ”Started”-viestin jälkeen |

> Jos ”Pending” -tila jatkuu yli 5 minuuttia, tarkista säiliön lokit virheiden varalta.

---

## RBAC- ja käyttöoikeusongelmat

### `403 Forbidden` tai `AuthorizationFailed`

Tarvitset **[Foundry User](https://aka.ms/foundry-ext-project-role)** -roolin Foundry-projektissasi (aiemmin nimeltään **Azure AI User** - roolin ID ei muuttunut):

1. Siirry osoitteeseen [Azure Portal](https://portal.azure.com) → oman Foundry **projektisi** resurssi.
2. Napsauta **Access control (IAM)** → **Role assignments**.
3. Etsi oma nimesi → varmista, että **Foundry User** (tai vanhempi nimike **Azure AI User**) on listattu.
4. Jos puuttuu: **Add** → **Add role assignment** → etsi **Foundry User** → määritä tilillesi.

Katso lisätietoja [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) -dokumentaatiosta.

### Mallin käyttöönotto ei ole käytettävissä

Jos agentti palauttaa mallin liittyviä virheitä:

1. Varmista, että malli on otettu käyttöön: Foundry sivuvalikko → avaa projekti → **Models** → tarkista `gpt-4.1-mini` (tai oma mallisi) tilassa **Succeeded**.
2. Varmista, että käyttöönoton nimi vastaa: vertaa `AZURE_AI_MODEL_DEPLOYMENT_NAME` kohdassa `.env` (tai `agent.yaml`) todelliseen käyttöönoton nimeen sivuvalikossa.
3. Jos käyttöönotto on vanhentunut (ilmainen taso): ota uudelleen käyttöön [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local -ongelmat (Polku B)

### Foundry Local -palvelu ei käynnisty

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Oire | Syy | Korjaus |
|---------|-------|-----|
| Health check palauttaa `503` | Palvelu ei käynnissä | `foundry local start` tai napsauta **Start** Foundry Toolkit -sivupalkissa |
| Health check aikakatkaisu | Malli latautuu vielä | Odota 30–60 s käynnistyksen jälkeen; suuremmat mallit vievät enemmän aikaa |
| `StatusCode: 404` kohdassa `/v1/health` | Väärä portti | Oletus on `5273`. Tarkista todellinen portti `foundry local status` |
| Riittämättömät resurssit | Foundry Local tarvitsee ~4 GB RAM-vapautta | Sulje muut sovellukset |
| Mallin lataus epäonnistuu | Vähän levytilaa | Mallit ovat 2–8 GB. Vapauta tilaa ja sitten `foundry model pull <name>` |

### Mallin nimen ristiriita

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Aseta `AZURE_AI_MODEL_DEPLOYMENT_NAME` tiedostossa `.env` täsmälleen samalla aliasilla kuin näkyy (esim. `phi-4-mini`, ei `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` paikallisessa suorituksessa (Polku B)

Labin `main.py` käyttää `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local vaatii, että tämä muuttuja osoittaa paikalliseen palveluun - **ei** `AZURE_AI_PROJECT_ENDPOINT`. Varmista, että `.env` sisältää:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-työkalu tekee silti ulkopuolisen kutsun (Polku B)

Tämä on odotettua. `search_microsoft_learn_for_plan`-työkalu hakee oppimateriaalia osoitteesta `https://learn.microsoft.com/api/mcp`. **Vain taitonimi-kysely** liikkuu verkon kautta – ansioluettelo ja työpaikkakuvaus käsitellään kokonaan laitteellasi eivätkä koskaan lähetetä. Jos täysin offline-toiminto vaaditaan, lisää työkaluun `try/except`-varayhteys, joka palauttaa staattisen `learn.microsoft.com` URL-osoitteen, kun palvelupistettä ei ole saavutettavissa.

---

## Apua saadaksesi

Jos olet jumissa yllä olevien korjausten jälkeen:

1. **Tarkista palvelimen lokit** - Useimmat virheet tuottavat Python-pinon jäljen terminaaliin. Lue koko jälki.
2. **Etsi virheilmoitusta** - Kopioi virheteksti ja etsi [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Avaa ongelma** - Luo ongelma [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) -varastoon:
   - Virheilmoitus tai näyttökuva
   - Pakettiversiot (`pip list | Select-String "agent-framework"`)
   - Python-versio (`python --version`)
   - Onko ongelma paikallinen vai käyttöönoton jälkeen

---

### Välitarkistus

- [ ] Osaat tarkistaa ja korjata `.env` konfiguraatio-ongelmat
- [ ] Osaat varmistaa, että pakettiversiot vastaavat vaadittua matriisia
- [ ] Osaat tarkistaa konttien lokit käyttöönoton epäonnistumisten varalta
- [ ] Osaat varmistaa RBAC-roolit Azure Portalissa

---

**Edellinen:** [07 - Tarkista Playgroundissa](07-verify-in-playground.md) · **Seuraava:** [09 - Yhteenveto →](09-summary.md) · **Koti:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->