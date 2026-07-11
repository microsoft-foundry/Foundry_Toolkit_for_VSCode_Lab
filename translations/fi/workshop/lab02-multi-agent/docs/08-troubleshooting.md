# Moduuli 8 – Vianmääritys

Tässä moduulissa käsitellään yleisiä virheitä, korjauksia ja vianetsintästrategioita, jotka ovat erityisiä moni-agenttityönkululle.

## Agentin tulosteongelmat

### GapAnalyzer ilmoittaa “Minulla ei vieläkään ole vastaavaa raporttia”

**Oire:** GapAnalyzer kysyy sinua liittämään vastaavan raportin, jossa on “Puuttuvat taidot” ja “Sertifiointivajeet.” Tämä tapahtuu, vaikka olisit lähettänyt sekä ansioluettelon että työkuvauksen.

**Syy:** Työkuvaustekstiä ei lähetetty eteenpäin JD Agentille. `context_mode="last_agent"` -tilassa `resume_executor` on ainoa suoritettava, joka koskaan näkee käyttäjän alkuperäisen viestin. Jos `RESUME_PARSER_INSTRUCTIONS` ei sisällä työkuvaustekstiä tulosteessaan, JD Agentilla ei ole työkkuvausta jäsennettäväksi, MatchingAgent ei voi laskea sopivuuspistettä, ja GapAnalyzer saa merkityksettömän syötteen.

**Diagnostiikka:**

Palvelimen lokeista etsi MatchingAgent-span. Jos se sisältää:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
siirto puuttuu tai on rikki.

**Korjaus:** Varmista, että `RESUME_PARSER_INSTRUCTIONS` tiedostossa `main.py` sisältää `[JOB DESCRIPTION PASS-THROUGH]` -osion ja säännön:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Varmista myös, että `JOB_DESCRIPTION_INSTRUCTIONS` sisältää `[PARSED RESUME PASS-THROUGH]` -välityssäännön:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jos jompikumpi ohjejakso on työkalupakin ohjevelhosta peräisin oleva luonnos, korvaa se täydellisellä versiolla tiedostosta [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent ilmoittaa “Sopivuuspistettä ei voida laskea – JD:tä ei annettu”

Tämä johtuu samasta pääsyystä kuin yllä. MatchingAgent sai JD Agentin tulosteen, mutta `[PARSED RESUME PASS-THROUGH]` -osio puuttui tai oli tyhjä, joten se ei voinut vertailla kahta profiilia. Varmista:
1. `JOB_DESCRIPTION_INSTRUCTIONS` sisältää välityssäännön: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` ohjeistaa agenttia etsimään `[JD REQUIREMENTS]` ja `[PARSED RESUME PASS-THROUGH]` -osiot.

Korvaa molemmat ohjejaksot täydellisillä versioilla tiedostosta [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Vastaus ilmestyy kahdesti

**Oire:** GapAnalyzerin tuloste (tai koko putken tuloste) näkyy kahdesti Agent Inspectorin vastauksessa.

**Syy:** `WorkflowBuilder` käyttää TAI-semantikkaa saapuvissa kaarissa – alaspäin tuleva suorittaja käynnistyy heti, kun **mikä tahansa** edeltäjä on valmis. Jos `matching_executor`:lla on kaksi saapuvaa kaarta (yksi `resume_executor`ilta ja yksi `jd_executor`ilta), se käynnistyy kahdesti: kerran ResumeParserin valmistumisen yhteydessä ja uudelleen JD Agentin päätyttyä. GapAnalyzer toimii tällä tavoin myös kahdesti.

**Korjaus:** Varmista, että `WorkflowBuilder`-kaavio on ehdottomasti peräkkäinen putki ilman fan-in:iä:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # EI resume_executorista
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jos sinulla on ylimääräinen `.add_edge(resume_executor, matching_executor)`-rivi, poista se. JD Agentin tulosteen `[PARSED RESUME PASS-THROUGH]` -välitys antaa jo MatchingAgentille pääsyn ansioluetteloon.

---

## Ympäristö- ja konfiguraatio-ongelmat

### Puuttuvat tai virheelliset `.env`-arvot

`.env`-tiedoston on oltava hakemistossa `PersonalCareerCopilot/` (saman tason kansio kuin `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Odotettu `.env`-sisältö:

**Polku A - Foundry pilvi:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Polku B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Molemmat polut käyttävät `FOUNDRY_PROJECT_ENDPOINT`-arvoa. Arvo eroaa: pilviversio käyttää `https://` Foundry-päätepistettä; paikallinen käyttää `http://localhost:5273/v1`. Suorita `foundry model list` varmistaaksesi tarkan mallin aliaksen Polulle B.

> **Miten löydät `FOUNDRY_PROJECT_ENDPOINT`-arvosi:** 
- Avaa **Foundry Toolkit** -sivupalkki VS Codessa → oikeaklikkaa projektiasi → **Copy Project Endpoint**. 
- Tai mene [Azure Portaalin](https://portal.azure.com) kautta projektillesi → **Yleiskatsaus** → **Projektin päätepiste**.

> **Miten löydät `AZURE_AI_MODEL_DEPLOYMENT_NAME`-arvosi:** Foundry Toolkit -sivupalkissa laajenna projektisi → **Models** → etsi käyttöönotetun mallisi nimi (esim. `gpt-4.1-mini`).

### Env-muuttujien prioriteetti

`main.py` käyttää `load_dotenv(override=True)`, mikä tarkoittaa:

| Prioriteetti | Lähde | Voittaa, jos molemmat asetettu? |
|-------------|-------|------------------------------|
| 1 (korkein) | `.env`-tiedosto | Kyllä |
| 2 | Shell / konttiympäristömuuttuja | Käytetään, kun sama avain ei ole `.env`:ssä |

Paikallisessa kehityksessä tämä tekee `.env`:stä totuuden lähteen (muutokset `.env`:ssä vaikuttavat suoraan ajoissa). Isännöidyssä käyttöönotossa Foundry lisää ympäristömuuttujat konttitasolla; koska `.env` ei kuulu käyttöön otettuun kuvaan tässä laboratoriossa, käytetään konttiin asetettuja arvoja.

---

## Versioyhteensopivuus

### Pakettiversioiden matriisi

Moni-agenttityönkulku vaatii tiettyjä pakettiversioita. Virheelliset versiot aiheuttavat ajonaikaisia virheitä.

| Paketti | Vaadittu versio | Tarkistuskomento |
|---------|-----------------|-----------------|
| `agent-framework-foundry` | uusin | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | uusin | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | uusin | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Yleiset versioviat

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Korjaus: asenna agent-framework-foundry uudelleen
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Korjaa: päivitä mcp-paketti
pip install mcp --upgrade
```

### Tarkista kaikki versiot yhdellä kertaa

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

### Kontti ei käynnisty käyttöönoton jälkeen

1. **Tarkista kontin lokit:**
   - Avaa **Foundry Toolkit** -sivupalkki → laajenna **Hosted Agents (Preview)** → klikkaa agenttiasi → laajenna versio → **Container Details** → **Logs**.
   - Etsi Python-pinojälkiä tai puuttuvia moduulivirheitä.

2. **Yleisiä kontin käynnistysvirheitä:**

   | Lokivirhe | Syy | Korjaus |
   |-----------|-----|--------|
   | `ModuleNotFoundError` | `requirements.txt` puuttuu paketti | Lisää paketti, ota uudelleen käyttöön |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml`:ssä tai `.env`:ssä ympäristömuuttujat puuttuvat | Päivitä `agent.yaml` → `environment_variables`-osa (isännöity) tai `.env` (paikallinen) |
   | `azure.identity.CredentialUnavailableError` | Managed Identityä ei ole konfiguroitu | Foundry tekee tämän automaattisesti – varmista, että otat käyttöön laajennuksen kautta |
   | `OSError: port 8088 already in use` | Dockerfile altistaa väärän portin tai porttikonflikti | Tarkista `EXPOSE 8088` Dockerfilessä ja `CMD ["python", "main.py"]` |
   | Kontti sulkeutuu koodilla 1 | Käsittelemätön poikkeus `main()`-funktiossa | Testaa ensin paikallisesti ([Moduuli 5](05-test-locally.md)) virheiden poistamiseksi ennen käyttöönottoa |

3. **Ota uudelleen käyttöön korjauksen jälkeen:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → valitse sama agentti → ota käyttöön uusi versio.

### Käyttöönotto kestää liian kauan

Moni-agenttikontit vievät pidempään käynnistyä, koska ne luovat 4 agentti-instanssia käynnistyksessä. Tavalliset käynnistysajat:

| Vaihe | Odotettu kesto |
|-------|----------------|
| Konttikuvan rakentaminen | 1-3 minuuttia |
| Kuvan työntö ACR:ään | 30-60 sekuntia |
| Kontin käynnistys (yksi agentti) | 15-30 sekuntia |
| Kontin käynnistys (moni-agentti) | 30-120 sekuntia |
| Agentti saatavilla Playgroundissa | 1-2 minuuttia “Started”-tilan jälkeen |

> Jos “Pending”-tila jatkuu yli 5 minuuttia, tarkista kontin lokit virheiden varalta.

---

## RBAC- ja käyttöoikeusongelmat

### `403 Forbidden` tai `AuthorizationFailed`

Tarvitset **[Foundry User](https://aka.ms/foundry-ext-project-role)** -roolin Foundry-projektissasi (aiemmin nimeltään **Azure AI User** – roolin tunnus on sama):

1. Mene [Azure Portaalin](https://portal.azure.com) kautta Foundry-projektisi resurssille.
2. Valitse **Access control (IAM)** → **Role assignments**.
3. Etsi nimesi → varmista, että luettelossa on **Foundry User** (tai vanha nimi **Azure AI User**).
4. Jos puuttuu: **Lisää** → **Add role assignment** → hae **Foundry User** → anna tilillesi.

Katso lisätietoja [RBAC Microsoft Foundrylle](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) -dokumentaatiosta.

### Mallin käyttöönotto ei ole käytettävissä

Jos agentti palauttaa malliin liittyviä virheitä:

1. Varmista, että malli on käyttöön otettu: Foundry-sivupalkki → laajenna projekti → **Models** → tarkista, että `gpt-4.1-mini` (tai oma mallisi) näkyy tilalla **Succeeded**.
2. Varmista, että käyttöönoton nimi vastaa: vertaa `AZURE_AI_MODEL_DEPLOYMENT_NAME`-arvoa `.env`-tiedostossa (tai `agent.yaml`:ssä) todelliseen nimeen sivupalkissa.
3. Jos käyttöönotto vanhentui (ilmainen taso): ota uudelleen käyttöön [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) -työkalusta (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local -ongelmat (Polku B)

### Foundry Local -palvelu ei ole käynnissä

```powershell
# Tarkista tila
foundry local status

# Käynnistä palvelu, jos se on pysäytetty
foundry local start
```

| Oire | Syy | Korjaus |
|------|------|--------|
| Health check palauttaa `503` | Palvelu ei käynnistynyt | Suorita `foundry local start` tai napsauta **Start** Foundry Toolkit -sivupalkissa |
| Health check aikakatkaisee | Malli latautuu vielä | Odota 30–60 sekuntia käynnistyksen jälkeen; isot mallit vievät kauemmin |
| `StatusCode: 404` osoitteessa `/v1/health` | Väärä portti | Oletus on `5273`. Tarkista `foundry local status` todellinen portti |
| Riittämättömät resurssit | Foundry Local tarvitsee ~4 Gt RAM-vapaata | Sulje muut sovellukset |
| Mallin lataus epäonnistuu | Levytila loppu | Mallit ovat 2–8 Gt. Vapauta tilaa, sitten `foundry model pull <name>` |

### Mallin nimen epäyhtenäisyys

```powershell
# Listaa ladatut mallit ja niiden tarkat aliakset
foundry model list
```

Aseta `AZURE_AI_MODEL_DEPLOYMENT_NAME` `.env`-tiedostoon täsmälleen näytetyn aliasn mukaan (esim. `phi-4-mini`, ei `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` paikallisessa ajossa (Polku B)

Labin `main.py` käyttää `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local vaatii tämän muuttujan osoittamaan paikalliseen palveluun - **ei** `AZURE_AI_PROJECT_ENDPOINT`-arvoon. Varmista, että `.env` sisältää:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-työkalu tekee silti ulospäin menevän kutsun (Polku B)

Tämä on odotettua. `search_microsoft_learn_for_plan`-työkalu hakee oppimateriaalit osoitteesta `https://learn.microsoft.com/api/mcp`. **Ainoastaan taitonimihakukysely** kulkee verkon yli – ansioluettelo ja työkuvausteksti käsitellään kokonaan laitteellasi eivätkä koskaan siirry ulos. Jos täysin offline-tila on tarpeen, lisää työkaluun try/except-rahoitus, joka palauttaa staattisen `learn.microsoft.com` -URL-osoitteen päätepisteen ollessa saavuttamattomissa.

---

## Apua saatavana

Jos jumitut kokeiltuasi ylläolevia korjauksia:

1. **Tarkista palvelimen lokit** – Useimmat virheet tuottavat Python-pinojäljen terminaaliin. Lue koko traceback.
2. **Etsi virheilmoituksella** – Kopioi virheteksti ja hae [Microsoft Q&A Azure AI:lle](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Avaa issue** – Tee virheilmoitus [työpajan repositorioon](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) sisältäen:
   - Virheilmoitus tai kuvakaappaus
   - Pakettiversiosi (`pip list | Select-String "agent-framework"`)
   - Python-versiosi (`python --version`)
   - Onko ongelma paikallinen vai käyttöönoton jälkeen

---

### Välitarkastus

- [ ] Osaat tarkistaa ja korjata `.env`-konfiguraatio-ongelmat
- [ ] Osaat varmistaa pakettiversioiden vastaavuuden vaaditun matriisin kanssa
- [ ] Osaat tarkistaa kontin lokit käyttöönotto-ongelmien varalta
- [ ] Osaat tarkistaa RBAC-roolit Azure-portaalissa

---

**Edellinen:** [07 - Tarkistus Playgroundissa](07-verify-in-playground.md) · **Seuraava:** [09 - Yhteenveto →](09-summary.md) · **Koti:** [Lab 02 README](../README.md) · [Työpajan aloitussivu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->