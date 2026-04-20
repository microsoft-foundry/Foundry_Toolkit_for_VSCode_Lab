# Moduuli 8 - Vianmääritys (Moni-agenttijärjestelmä)

Tämä moduuli käsittelee yleisiä virheitä, korjauksia ja virheenkorjausstrategioita, jotka liittyvät moni-agenttiprosessiin. Yleisiin Foundry-julkaisuongelmiin viitataan myös [Lab 01 vianmääritysohjeisiin](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Pikaviite: Virhe → Korjaus

| Virhe / Oire | Todennäköinen syy | Korjaus |
|--------------|-------------------|---------|
| `RuntimeError: Missing required environment variable(s)` | `.env`-tiedosto puuttuu tai arvot asettamatta | Luo `.env` sisältäen `PROJECT_ENDPOINT=<your-endpoint>` ja `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuaaliympäristö ei ole aktivoitu tai riippuvuuksia ei ole asennettu | Aja `.\.venv\Scripts\Activate.ps1` sitten `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP-pakettia ei ole asennettu (puuttuu requirements.txt:stä) | Aja `pip install mcp` tai tarkista, että `requirements.txt` sisältää sen välillisenä riippuvuutena |
| Agentti käynnistyy mutta palauttaa tyhjän vastauksen | `output_executors` ei täsmää tai reunat puuttuvat | Varmista, että `output_executors=[gap_analyzer]` ja kaikki reunat ovat olemassa `create_workflow()`-funktiossa |
| Vain 1 gap-kortti (muut puuttuvat) | GapAnalyzerin ohjeet puutteelliset | Lisää `CRITICAL:`-kappale `GAP_ANALYZER_INSTRUCTIONS`-muuttujaan - katso [Moduuli 3](03-configure-agents.md) |
| Fit-pistemäärä on 0 tai puuttuu | MatchingAgent ei saanut ylävirran dataa | Varmista, että molemmat `add_edge(resume_parser, matching_agent)` ja `add_edge(jd_agent, matching_agent)` ovat olemassa |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP-palvelin hylkäsi työkalupyynnön | Tarkista verkkoyhteys. Yritä avata `https://learn.microsoft.com/api/mcp` selaimessa. Yritä uudelleen |
| Ei Microsoft Learn -URL-osoitteita tulosteessa | MCP-työkalu ei rekisteröity tai päätepiste on väärä | Varmista, että `tools=[search_microsoft_learn_for_plan]` on GapAnalyzerissa ja `MICROSOFT_LEARN_MCP_ENDPOINT` on oikea |
| `Address already in use: port 8088` | Toinen prosessi käyttää porttia 8088 | Aja `netstat -ano \| findstr :8088` (Windows) tai `lsof -i :8088` (macOS/Linux) ja pysäytä ristiriitainen prosessi |
| `Address already in use: port 5679` | Debugpy-porttikonflikti | Lopeta muut debug-istunnot. Aja `netstat -ano \| findstr :5679` löytääksesi ja tappaksesi prosessi |
| Agent Inspector ei aukea | Palvelin ei ole kokonaan käynnistynyt tai porttikonflikti | Odota "Server running" -lokia. Tarkista, että portti 5679 on vapaa |
| `azure.identity.CredentialUnavailableError` | Ei ole kirjautunut Azure CLI:hin | Suorita `az login` ja käynnistä palvelin uudelleen |
| `azure.core.exceptions.ResourceNotFoundError` | Mallin julkaisu ei ole olemassa | Tarkista, että `MODEL_DEPLOYMENT_NAME` vastaa projektissasi julkaistua mallia |
| Kontin tila "Failed" julkaisun jälkeen | Kontti kaatui käynnistyksessä | Tarkista kontin lokit Foundryn sivupalkista. Tavallisia syitä: puuttuva ympäristömuuttuja tai import-virhe |
| Julkaisu näkyy "Pending" yli 5 minuuttia | Kontti käynnistyy liian hitaasti tai resurssirajoitteet | Odota jopa 5 minuuttia moniajagentille (luo 4 agentti-instanssia). Jos edelleen odottaa, tarkista lokit |
| `ValueError` `WorkflowBuilder`:sta | Virheellinen graafin määritys | Varmista, että `start_executor` on asetettu, `output_executors` on lista, eikä ole silmukkareunoja |

---

## Ympäristö- ja määritysongelmat

### Puuttuvat tai virheelliset `.env`-arvot

`.env`-tiedoston tulee olla `PersonalCareerCopilot/`-hakemistossa (saman tasoisena kuin `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Odotettu `.env`-sisältö:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Miten löydät PROJECT_ENDPOINTin:**  
- Avaa **Microsoft Foundry** -sivupalkki VS Codessa → oikea klikkaa projektiasi → **Copy Project Endpoint**.  
- Tai siirry [Azure-portaaliin](https://portal.azure.com) → projektisi Foundry → **Yleiskatsaus** → **Project endpoint**.

> **Miten löydät MODEL_DEPLOYMENT_NAMEin:** Laajenna projektia Foundryn sivupalkissa → **Models** → etsi julkaistun mallisi nimi (esim. `gpt-4.1-mini`).

### Env-muuttujien prioriteetti

`main.py` käyttää `load_dotenv(override=False)`, mikä tarkoittaa:

| Prioriteetti | Lähde | Voittaa, jos molemmat asetettu? |
|--------------|-------|----------------------------------|
| 1 (korkein)  | Shell-ympäristömuuttuja | Kyllä |
| 2            | `.env`-tiedosto | Vain jos shell-muuttuja ei ole asetettu |

Tämä tarkoittaa, että Foundryn runtime-ympäristömuuttujat (`agent.yaml`-asetuksista) syrjäyttävät `.env`:n arvot hosting-julkaisussa.

---

## Versiokelpoisuus

### Pakettiversiotaulukko

Moni-agenttiprosessi vaatii tiettyjä pakettiversioita. Versioiden yhteensopimattomuudet aiheuttavat virheitä ajossa.

| Paketti | Vaadittu versio | Tarkistuskomento |
|---------|-----------------|------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | uusin esiversio | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Yleiset versiovirheet

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Korjaus: päivitä rc3-versioon
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` puuttuu tai Inspector on yhteensopimaton:**

```powershell
# Korjaa: asenna --pre-lipulla
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Korjaus: päivitä mcp-paketti
pip install mcp --upgrade
```

### Tarkista kaikki versiot yhdellä kertaa

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Odotettu tuloste:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## MCP-työkalun ongelmat

### MCP-työkalu ei palauta tuloksia

**Oire:** Gap-korteissa lukee "No results returned from Microsoft Learn MCP" tai "No direct Microsoft Learn results found".

**Mahdolliset syyt:**

1. **Verkkoyhteysongelma** - MCP-päätepistettä (`https://learn.microsoft.com/api/mcp`) ei tavoiteta.
   ```powershell
   # Testaa yhteys
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Jos vastauksena on `200`, päätepiste on saavutettavissa.

2. **Kysely on liian tarkka** - Taitonimi on liian erikoistunut Microsoft Learn -haulle.  
   - Tämä on odotettu hyvin erikoistuneiden taitojen kohdalla. Työkalu tarjoaa vastausobjektissa vararatkaisulinkin.

3. **MCP-istunnon aikakatkaisu** - Streamable HTTP -yhteys aikakatkaistiin.  
   - Yritä pyyntö uudelleen. MCP-istunnot ovat tilapäisiä ja vaativat uudelleenyhdistämisen.

### MCP-lokit selitettynä

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Lokimerkintä | Merkitys | Toimenpide |
|--------------|----------|------------|
| `GET → 405` | MCP-asiakkaan kyselyt alustuksen aikana | Normaalia - ohita |
| `POST → 200` | Työkalukutsu onnistui | Odotettu |
| `DELETE → 405` | MCP-asiakkaan kyselyt puhdistuksen aikana | Normaalia - ohita |
| `POST → 400` | Virheellinen pyyntö (muodoton kysely) | Tarkista `query`-parametri `search_microsoft_learn_for_plan()` -funktiossa |
| `POST → 429` | Kutsujen rajoitus ylittynyt | Odota ja yritä uudelleen. Vähennä `max_results`-parametria |
| `POST → 500` | MCP-palvelinvirhe | Tilapäinen - yritä uudelleen. Jos jatkuva, Microsoft Learn MCP API voi olla poissa käytöstä |
| Yhteyden aikakatkaisu | Verkkoyhteysongelma tai MCP-palvelin ei saatavilla | Tarkista nettiyhteys. Kokeile `curl https://learn.microsoft.com/api/mcp` |

---

## Julkaisun ongelmat

### Kontti ei käynnisty julkaisun jälkeen

1. **Tarkista kontin lokit:**
   - Avaa **Microsoft Foundry** -sivupalkki → laajenna **Hosted Agents (Preview)** → klikkaa agenttiasi → laajenna versio → **Container Details** → **Logs**.
   - Etsi Pythonin pinon jälkiä tai puuttuvia moduulivirheitä.

2. **Yleiset kontin käynnistysvirheet:**

   | Virhe lokeissa | Syy | Korjaus |
   |----------------|-----|---------|
   | `ModuleNotFoundError` | `requirements.txt`stä puuttuu paketti | Lisää paketti ja julkaise uudelleen |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` ympäristömuuttujat eivät ole asetettu | Päivitä `agent.yaml` → `environment_variables`-osio |
   | `azure.identity.CredentialUnavailableError` | Hallittu identiteetti ei ole määritetty | Foundry määrittää automaattisesti - varmista, että julkaiset laajennuksen kautta |
   | `OSError: port 8088 already in use` | Dockerfile paljastaa väärän portin tai porttikonflikti | Varmista `EXPOSE 8088` Dockerfilessä ja `CMD ["python", "main.py"]` |
   | Kontti lopettaa koodilla 1 | Käsittelemätön poikkeus `main()`-funktiossa | Testaa ensin paikallisesti ([Moduuli 5](05-test-locally.md)) virheiden havaitsemiseksi ennen julkaisua |

3. **Julkaise uudelleen korjauksen jälkeen:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → valitse sama agentti → julkaise uusi versio.

### Julkaisu kestää liian kauan

Moni-agenttikontit käynnistyvät hitaammin, koska ne luovat käynnistyksessä 4 agentti-instanssia. Tyypilliset käynnistysajat:

| Vaihe | Odotettu kesto |
|-------|----------------|
| Konttikuvan rakentaminen | 1-3 minuuttia |
| Kuvan lähetys ACR:ään | 30-60 sekuntia |
| Kontin käynnistys (yksittäinen agentti) | 15-30 sekuntia |
| Kontin käynnistys (moni-agentti) | 30-120 sekuntia |
| Agentti käytettävissä PlayGroundissa | 1-2 minuuttia "Started" jälkeen |

> Jos “Pending” -tila kestää yli 5 minuuttia, tarkista kontin lokit virheiden varalta.

---

## RBAC- ja oikeusongelmat

### `403 Forbidden` tai `AuthorizationFailed`

Tarvitset **[Azure AI User](https://aka.ms/foundry-ext-project-role)** -roolin Foundry-projektiisi:

1. Mene [Azure-portaaliin](https://portal.azure.com) → projektisi **Foundry**-resurssiin.
2. Valitse **Access control (IAM)** → **Role assignments**.
3. Etsi nimesi → varmista, että **Azure AI User** on listattuna.
4. Jos puuttuu: valitse **Add** → **Add role assignment** → etsi **Azure AI User** → määritä tilillesi.

Lisätietoja löytyy [RBAC Microsoft Foundryssä](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) -dokumentaatiosta.

### Mallin julkaisu ei ole käytettävissä

Jos agentti palauttaa malli- tai julkaisuvirheitä:

1. Varmista, että malli on julkaistu: Foundryn sivupalkissa laajenna projekti → **Models** → tarkista, että `gpt-4.1-mini` (tai oma mallisi) näkyy tilassa **Succeeded**.  
2. Varmista, että julkaisun nimi täsmää: vertaa `.env`in (tai `agent.yaml`n) `MODEL_DEPLOYMENT_NAME` julkaisun nimeen sivupalkissa.  
3. Jos julkaisu on vanhentunut (ilmainen taso): julkaise uudelleen [Model Catalogista](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspectorin ongelmat

### Inspector aukeaa mutta näyttää "Disconnected"

1. Varmista, että palvelin on käynnissä: etsi terminaalista "Server running on http://localhost:8088".  
2. Tarkista portti `5679`: Inspector yhdistää debugpy:n kautta porttiin 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Käynnistä palvelin uudelleen ja avaa Inspector uudelleen.

### Inspector näyttää osittaisen vastauksen

Moni-agentin vastaukset ovat pitkiä ja virtautuvat vaiheittain. Odota koko vastauksen valmistumista (voi kestää 30-60 sekuntia riippuen gap-korttien määrästä ja MCP-työkalupyyntöjen lukumäärästä).

Jos vastaus on jatkuvasti katkaistu:  
- Tarkista, että GapAnalyzerin ohjeissa on `CRITICAL:`-lohko, joka estää gap-korttien yhdistämisen.  
- Tarkista mallisi token-raja – `gpt-4.1-mini` tukee jopa 32 000 output-tokenia, mikä riittää yleensä.

---

## Suorituskykyvinkit

### Hitaat vastaukset

Moni-agenttiprosessit ovat luontaisesti hitaampia kuin yksittäisagenttikorvaukset, koska ne vaativat peräkkäisiä riippuvuuksia ja MCP-työkalukutsuja.

| Optimointi | Miten | Vaikutus |
|------------|--------|----------|
| Vähennä MCP-kutsuja | Laske työkalun `max_results`-parametria | Vähemmän HTTP-kierroksia |
| Yksinkertaista ohjeita | Lyhyemmät, täsmällisemmät agenttipyynnöt | Nopeampi LLM-päätteleminen |
| Käytä `gpt-4.1-mini` | Nopeampi kuin `gpt-4.1` kehityksessä | Noin 2x nopeampi |
| Vähennä gap-korttien yksityiskohtia | Siisti gap-korttien formaatti GapAnalyzerin ohjeissa | Vähemmän tulostettavaa |

### Tyypilliset vasteajat (paikallinen)

| Määritys | Odotettu aika |
|----------|---------------|
| `gpt-4.1-mini`, 3-5 gap-korttia | 30-60 sekuntia |
| `gpt-4.1-mini`, 8+ gap-korttia | 60-120 sekuntia |
| `gpt-4.1`, 3-5 gap-korttia | 60-120 sekuntia |
---

## Avun hakeminen

Jos olet jumissa yllä olevien korjausten jälkeen:

1. **Tarkista palvelimen lokit** - Useimmat virheet tuottavat Pythonin pinon jäljityksen terminaaliin. Lue koko jäljitys.
2. **Hae virheilmoitusta** - Kopioi virheteksti ja etsi sitä [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) -sivustolta.
3. **Avaa ongelma** - Tee ongelmailmoitus [workshopin varastoon](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues), jossa on:
   - Virheilmoitus tai kuvakaappaus
   - Pakettiversiosi (`pip list | Select-String "agent-framework"`)
   - Python-versiosi (`python --version`)
   - Onko ongelma paikallinen vai käyttöönottamisen jälkeinen

---

### Tarkistuslista

- [ ] Osaat tunnistaa ja korjata yleisimmät moniagenttivirheet pikaviitetaulukon avulla
- [ ] Osaat tarkistaa ja korjata `.env`-asetusten ongelmia
- [ ] Osaat varmistaa, että pakettiversiot vastaavat vaadittua matriisia
- [ ] Ymmärrät MCP-lokimerkinnät ja voit diagnosoida työkalujen epäonnistumisia
- [ ] Osaat tarkistaa säiliölokit käyttöönoton epäonnistumisia varten
- [ ] Osaat varmistaa RBAC-roolit Azure-portaalissa

---

**Edellinen:** [07 - Verify in Playground](07-verify-in-playground.md) · **Koti:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vapaamuotoinen vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Pyrimme tarkkuuteen, mutta ole hyvä ja ota huomioon, että automaattiset käännökset voivat sisältää virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulee pitää virallisena lähteenä. Tärkeissä tiedoissa suositellaan ammattimaisesti tehtyä ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinkäsityksistä tai virhetulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->