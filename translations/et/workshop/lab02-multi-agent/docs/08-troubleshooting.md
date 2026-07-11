# Moodul 8 - Tõrkeotsing

See moodul käsitleb mitme agendi töövoole iseloomulikke tavalisi vigu, parandusi ja silumisstrateegiaid.

## Agendi väljundi probleemid

### GapAnalyzer ütleb “Mul pole ikka sobivat raportit”

**Sümptom:** GapAnalyzer'i vastus palub kleepida sobiv raport koos "Puuduvate oskuste" ja "Sertifitseerimise lünkadega". See juhtub isegi siis, kui saatsite nii CV kui töökuulutuse tekst.

**Põhjus:** Töökuulutuse tekst ei kandunud allavoolu JD agendile. `context_mode="last_agent"` puhul näeb kasutaja algset sõnumit ainult `resume_executor`. Kui `RESUME_PARSER_INSTRUCTIONS` ei sisalda oma väljundis töökuulutuse teksti, ei ole JD agendil midagi parsida, MatchingAgent ei saa arvutada sobivuskoefitsienti ja GapAnalyzer saab mõttetut sisendit.

**Diagnoos:**

Serveri logidest otsi MatchingAgent'i spaani. Kui seal on:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
läbipääs puudub või on katki.

**Parandus:** Kinnita, et `main.py` failis `RESUME_PARSER_INSTRUCTIONS` sisaldab `[JOB DESCRIPTION PASS-THROUGH]` sektsiooni ja reeglit:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Samuti veendu, et `JOB_DESCRIPTION_INSTRUCTIONS` sisaldab `[PARSED RESUME PASS-THROUGH]` edastamise reeglit:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Kui ükskõik milline juhiste plokk on tühimik scaffolding’i assistendist, asenda see täieliku versiooniga failist [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent väljastab “Ei saa arvutada sobivuskoefitsienti - töökuulutust ei ole esitatud”

See viga tuleneb samast põhjusest kui eespool. MatchingAgent sai JD agendi väljundi, kuid `[PARSED RESUME PASS-THROUGH]` sektsioon puudus või oli tühi, seega ei saanud neid profiile võrrelda. Kontrolli:
1. `JOB_DESCRIPTION_INSTRUCTIONS` sisaldab edastusreeglit: `Kopeeri [PARSED RESUME] täpselt edasi - Matching Agent sõltub sellest allavoolu.`
2. `MATCHING_AGENT_INSTRUCTIONS` ütleb agendile otsida `[JD REQUIREMENTS]` ja `[PARSED RESUME PASS-THROUGH]` sektsioone.

Asenda mõlemad juhiste plokid täielike versioonidega failist [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Vastus kuvatakse kaks korda

**Sümptom:** GapAnalyzer väljund (või kogu torujuhtme väljund) kuvatakse Agent Inspector'i vastuses kaks korda.

**Põhjus:** `WorkflowBuilder` kasutab saabuvatele servadele VÕI-semantikat - allavoolu täideviija käivitub kohe, kui **ükski** eelkäija lõpetab. Kui `matching_executor`il on kaks saabuvat serva (üks `resume_executor'ilt` ja teine `jd_executor'ilt`), käivitub ta kaks korda: üks kord, kui ResumeParser lõpeb ja teine kord, kui JD Agent lõpetab. GapAnalyzer jookseb siis ka kaks korda.

**Parandus:** Veendu, et `WorkflowBuilder` graafik on rangelt järjestikune torujuhe ilma fännisisendita:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # EI ole pärit resume_executor-ist
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Kui sul on lisarida `.add_edge(resume_executor, matching_executor)`, eemalda see. JD Agendi väljundis olev `[PARSED RESUME PASS-THROUGH]` edastamine annab juba MatchingAgent'ile CV juurdepääsu.

---

## Keskkonna- ja konfiguratsiooniprobleemid

### Puuduvad või valed `.env` väärtused

`.env` fail peab olema kaustas `PersonalCareerCopilot/` (samal tasemel `main.py` failiga):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Oodatud `.env` sisu:

**Võimalus A - Foundry pilv:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Võimalus B - Foundry lokaalne:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Mõlemad võimalused kasutavad `FOUNDRY_PROJECT_ENDPOINT`. Väärtus erineb: pilv kasutab `https://` Foundry lõpp-punkti; lokaalne kasutab `http://localhost:5273/v1`. Käivita `foundry model list`, et kinnitada täpne mudeli alias Võimalus B jaoks.

> **Kuidas leida oma `FOUNDRY_PROJECT_ENDPOINT`:** 
- Ava VS Code'is **Foundry Toolkit** külgriba → paremklõps oma projektil → **Copy Project Endpoint**. 
- Või mine [Azure portaal](https://portal.azure.com) → oma Foundry projekt → **Ülevaade** → **Projektipunkt**.

> **Kuidas leida oma `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Foundry Toolkit külgribal laienda projekt → **Mudelite** sektsioon → leia oma juurutatud mudeli nimi (nt `gpt-4.1-mini`).

### Keskkonnamuutuja eelisjärjekord

`main.py` kasutab `load_dotenv(override=True)`, mis tähendab:

| Prioriteet | Allikas | Kas võidab, kui mõlemad on määratud? |
|----------|--------|------------------------------|
| 1 (kõrgeim) | `.env` fail | Jah |
| 2 | Shelli/konteineri keskkonnamuutuja | Kasutatakse, kui sama võtme kohta `.env`-failis pole väärtust |

Kohalikus arenduses tähendab see, et `.env` on tõeallikas (selle muutmine mõjutab jooksvaid käske kohe). Hostitud juurutuses süstib Foundry konteineri tasandil keskkonnamuutujad; kuna `.env` ei ole selle laboris kasutatavas kujutises, kasutatakse konteinerisse süstitud muutujate väärtusi.

---

## Versioonide ühilduvus

### Paketiversioonide tabel

Mitme agendi töövoog nõuab kindlaid paketiversioone. Versioonide sobimatus põhjustab jooksutõrkeid.

| Pakett | Nõutav versioon | Kontrollkäsk |
|---------|-----------------|-------------|
| `agent-framework-foundry` | uuem | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | uuem | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | uuem | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Levinud versioonivead

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Parandus: paigalda agent-framework-foundry uuesti
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Parandus: uuenda mcp paketti
pip install mcp --upgrade
```

### Kontrolli kõiki versioone korraga

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Oodatud väljund:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Juurutusprobleemid

### Konteiner ei käivitu pärast juurutust

1. **Kontrolli konteineri logisid:**
   - Ava **Foundry Toolkit** külgriba → laienda **Hosted Agents (Preview)** → klõpsa oma agendil → laienda versiooni → **Container Details** → **Logs**.
   - Otsi Python'i virnade jälgi või moodulite puudumise teateid.

2. **Levinumad konteineri käivituse vead:**

   | Viga logides | Põhjus | Parandus |
   |--------------|---------|----------|
   | `ModuleNotFoundError` | `requirements.txt`-st pakett puudu | Lisa pakett, juuruta uuesti |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` või `.env` keskkonnamuutujad puuduvad | Uuenda `agent.yaml` → `environment_variables` sektsiooni (hostitud) või `.env` (kohalik) |
   | `azure.identity.CredentialUnavailableError` | Hallatav identiteet pole konfigureeritud | Foundry teeb selle automaatselt - veendu, et kasutad laiendust juurutamiseks |
   | `OSError: port 8088 already in use` | Dockerfile eksposeerib vale pordi või portide konflikt | Kontrolli Dockerfile's `EXPOSE 8088` ja CMD rida `CMD ["python", "main.py"]` |
   | Konteiner väljub koodiga 1 | Käitlemata erand funktsioonis `main()` | Testi esmalt kohalikult ([Moodul 5](05-test-locally.md)) vigade püüdmiseks enne juurutust |

3. **Juuruta paranduse järel uuesti:**
   - Vajuta `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → vali sama agent → juuruta uus versioon.

### Juurutamine võtab liiga kaua aega

Mitme agendi konteinerid käivituvad kauem, sest nad loovad käivitamisel 4 agendi eksemplari. Tavalised käivituse ajad:

| Etapp | Oodatav kestus |
|-------|----------------|
| Konteineri kujutise loomine | 1-3 minutit |
| Kujutise tõstmine ACR-i | 30-60 sekundit |
| Konteineri käivitamine (ühe agendi puhul) | 15-30 sekundit |
| Konteineri käivitamine (mitme agendi puhul) | 30-120 sekundit |
| Agent kättesaadav mänguväljakus | 1-2 minutit pärast “Käivitati” teateid |

> Kui “Ootel” olek kestab kauem kui 5 minutit, kontrolli konteineri logisid vigade leidmiseks.

---

## RBAC ja õiguste probleemid

### `403 Keelatud` või `AuthorizationFailed`

Sul peab olema **[Foundry kasutaja](https://aka.ms/foundry-ext-project-role)** roll oma Foundry projektis (varem nimetatud **Azure AI kasutajaks** - rolli ID ei ole muutunud):

1. Mine [Azure portaalile](https://portal.azure.com) → oma Foundry **projekti** ressurss.
2. Klõpsa **Juurdepääsu juhtimine (IAM)** → **Rolli määramised**.
3. Otsi oma nime → kinnita, et on olemas **Foundry kasutaja** (või vana nimetus **Azure AI kasutaja**).
4. Kui puudub: **Lisa** → **Lisa rolli määramine** → otsi **Foundry kasutaja** → määra see oma kontole.

Vaata [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokumentatsiooni lisateabe saamiseks.

### Mudeli juurutus ei ole ligipääsetav

Kui agent tagastab mudeliga seotud vigu:

1. Kontrolli, kas mudel on juurutatud: Foundry külgriba → laienda projekt → **Mudelite** sektsioon → kontrolli, et `gpt-4.1-mini` (või sinu mudel) on olekus **Succeeded**.
2. Kontrolli, et juurutamisnimega klapib: võrdle `.env`-failis (või `agent.yaml`-is) olevat `AZURE_AI_MODEL_DEPLOYMENT_NAME` tegeliku nimega külgribal.
3. Kui juurutuse aeg on lõppenud (tasuta tase): juuruta uuesti [Mudelite kataloogist](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry lokaalsed probleemid (võimalus B)

### Foundry Local teenus ei tööta

```powershell
# Kontrolli staatust
foundry local status

# Käivita teenus, kui see on peatatud
foundry local start
```

| Sümptom | Põhjus | Parandus |
|---------|-------|----------|
| Tervisekontroll tagastab `503` | Teenus pole käivitatud | Käivita `foundry local start` või vajuta Foundry Toolkit külgribal **Start** |
| Tervisekontroll lõppes ajapiiranguga | Mudel on veel laadimisel | Oota 30–60 sekundit peale käivitamist; suuremad mudelid vajavad rohkem aega |
| `StatusCode: 404` aadressil `/v1/health` | Vale pordinumber | Vaikimisi on `5273`. Kontrolli reaalset porti käsuga `foundry local status` |
| Ebapiisavad ressursid | Foundry Local vajab ~4 GB vaba RAM-i | Sulge teised programmid |
| Mudeli allalaadimine ebaõnnestub | Vähe kettaruumi | Mudelid on 2–8 GB suured. Tee kettaruumi vabaks, seejärel käivita `foundry model pull <name>` |

### Mudelinime sobimatus

```powershell
# Loetle alla laaditud mudelid ja nende täpsed aliased
foundry model list
```

Sea `.env` failis `AZURE_AI_MODEL_DEPLOYMENT_NAME` täpselt samaks kui ekraanile kuvatud alias (nt `phi-4-mini`, mitte `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` lokaalsel ajal (võimalus B)

Labori `main.py` kasutab `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local eeldab, et see viitab kohaliku teenuse aadressile - **mitte** `AZURE_AI_PROJECT_ENDPOINT`-le. Veendu, et sinu `.env` fail sisaldab:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP tööriist teeb siiski väljamineva päringu (võimalus B)

See on ootuspärane. `search_microsoft_learn_for_plan` tööriist tõmbab õppematerjale aadressilt `https://learn.microsoft.com/api/mcp`. **Ainult oskuste nime päring** läbib võrku - CV ja töökuulutuse tekst töödeldakse täielikult sinu seadmes ega saadeta kunagi edasi. Kui on vaja täielikku võrguühenduseta toimimist, lisa tööriista `try/except` erihaldus, mis tagastab staatilise `learn.microsoft.com` URL-i, kui lõpp-punkt on kättesaamatu.

---

## Abi saamine

Kui sa takerdud pärast ülaltoodud paranduste proovimist:

1. **Kontrolli serveri logisid** - Enamik veateateid genereerib Python'i virnade jälgede terminalis. Loe kogu väljund läbi.
2. **Otsi veateadet** - Kopeeri veateade ja otsi [Microsoft Q&A Azure AI teemade lõimes](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Loo probleemiteade** - Sissekanne selle [workshopi repotiilöös](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues):
   - Veateade või ekraanipilt
   - Sinu paketiversioonid (`pip list | Select-String "agent-framework"`)
   - Sinu Python versioon (`python --version`)
   - Kas probleem on lokaalne või pärast juurutust

---

### Kontrollpunkt

- [ ] Sa tead, kuidas kontrollida ja parandada `.env` konfiguratsiooni probleeme
- [ ] Sa suudad kontrollida, et paketiversioonid vastavad nõutud tabelile
- [ ] Sa tead, kuidas kontrollida konteinerilogi juurutuse vigade jaoks
- [ ] Sa oskad kontrollida RBAC rolle Azure Portaalis

---

**Eelmine:** [07 - Kontrollimänguväljakus](07-verify-in-playground.md) · **Järgmine:** [09 - Kokkuvõte →](09-summary.md) · **Esileht:** [Labor 02 README](../README.md) · [Workshopsi esileht](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->