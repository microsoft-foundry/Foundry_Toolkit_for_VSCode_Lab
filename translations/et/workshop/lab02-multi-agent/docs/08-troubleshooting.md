# Moodul 8 - Tõrkeotsing

See moodul käsitleb mitme agendi töövoo puhul levinud vigu, parandusi ja silumisstrateegiaid.

## Agendi väljundi probleemid

### GapAnalyzer ütleb: „Mul ei ole ikka veel sobivat raportit”

**Sümptom:** GapAnalyzer’i vastus palub teil kleepida sobiv raport koos „Puuduvad oskused” ja „Sertifitseerimise puudujäägid.” See juhtub isegi siis, kui te saatsite nii CV kui ka töökuulutuse.

**Põhjus:** JD teksti ei edastatud allavoolu JD Agendile. `context_mode="last_agent"` puhul näeb `resume_executor` ainuisikuliselt kasutaja originaalset sõnumit. Kui `RESUME_PARSER_INSTRUCTIONS` ei sisalda töökuulutuse teksti väljundis, siis JD Agentil puudub töökuulutus, mille põhjal analüüsida, MatchingAgent ei saa sobivusskoori arvutada ja GapAnalyzer saab mõttetut sisendit.

**Diagnoos:**

Serverilogides otsige MatchingAgent span’i. Kui see sisaldab:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
siis on edastamisprotsess kadunud või katkine.

**Parandus:** Kinnitage, et `RESUME_PARSER_INSTRUCTIONS` sees `main.py` sisaldab `[JOB DESCRIPTION PASS-THROUGH]` osa ja reeglit:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Samuti kinnitage, et `JOB_DESCRIPTION_INSTRUCTIONS` sisaldab `[PARSED RESUME PASS-THROUGH]` edastusreeglit:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Kui ükski neist juhisplokkidest on scaffolding-võluri näidis, asendage see täieliku versiooniga [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent väljastab „Ei saa sobivusskoori arvutada – töökuulutus puudub”

See on sama juurpõhjus nagu eelnevalt. MatchingAgent sai kätte JD Agendi väljundi, kuid `[PARSED RESUME PASS-THROUGH]` osa puudus või oli tühi, seega ei saanud ta neid kahte profiili võrrelda. Kontrollige:
1. `JOB_DESCRIPTION_INSTRUCTIONS` sisaldab edastusreeglit: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` annab agendile juhise otsida `[JD REQUIREMENTS]` ja `[PARSED RESUME PASS-THROUGH]` osi.

Asendage mõlemad juhisplokid täielike versioonidega [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Vastus kuvatakse kaks korda

**Sümptom:** GapAnalyzer väljund (või kogu torujuhtme väljund) kuvatakse Agent Inspector vastuses kaks korda.

**Põhjus:** `WorkflowBuilder` kasutab VÕI-semantikat sisenevate linkide puhul – allavoolu täitja käivitub kohe, kui **ükskõik milline** eelkäija lõpetab. Kui `matching_executor`-l on kaks sisenevat linki (üks `resume_executor`-st ja üks `jd_executor`-st), siis see käivitub kaks korda: ühe korra, kui ResumeParser lõpetab ja teist korda, kui JD Agent lõpetab. Seejärel töötab GapAnalyzer samuti kaks korda.

**Parandus:** Veenduge, et `WorkflowBuilder` graafik on rangelt järjestikune torujuhe ilma fänn-in ühenduseta:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Kui teil on üksik `.add_edge(resume_executor, matching_executor)` rida, eemaldage see. JD Agendi väljundi `[PARSED RESUME PASS-THROUGH]` edastus annab juba MatchingAgentile ligipääsu CV-le.

---

## Keskkonna ja konfiguratsiooni probleemid

### Puuduvad või valed `.env` väärtused

`.env` fail peab olema `PersonalCareerCopilot/` kataloogis (samal tasemel kui `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Oodatud `.env` sisu:

**A variant – Foundry pilv:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**B variant – Foundry kohalik:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Mõlemad variandid kasutavad `FOUNDRY_PROJECT_ENDPOINT`. Väärtus erineb: pilv kasutab `https://` Foundry liidest; kohalik versioon kasutab `http://localhost:5273/v1`. Käivitage `foundry model list`, et kinnitada täpne mudeli alias B variandi jaoks.

> **Kuidas leida oma `FOUNDRY_PROJECT_ENDPOINT`:** 
- Avage VS Code’is **Foundry Toolkit** külgriba → paremklõpsake oma projektil → valige **Copy Project Endpoint**. 
- Või minge [Azure Portaali](https://portal.azure.com) → oma Foundry projekti → **Ülevaade** → **Project endpoint**.

> **Kuidas leida oma `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Foundry Toolkit külgribas laiendage oma projekt → **Models** → leidke oma kasutusel olev mudeli nimi (nt `gpt-4.1-mini`).

### Keskkonnamuutuja prioriteet

`main.py` kasutab `load_dotenv(override=True)`, mis tähendab:

| Prioriteet | Allikas | Kas võidab, kui mõlemad on määratud? |
|----------|--------|-------------------------------|
| 1 (kõrgeim) | `.env` fail | Jah |
| 2 | Shell / konteineri keskkonnamuutuja | Kasutatakse, kui sama võti puudub `.env` |

Kohalikus arenduses tähendab see, et `.env` on tõe allikas (`.env` muutmine mõjutab jooksvaid protsesse koheselt). Majutatud versioonis süstib Foundry keskkonnamuutujaid konteineri tasandil; kuna `.env` ei ole selle laborisüsteemi paigutatud kujutise osa, kasutatakse konteinerisse süstitud väärtusi.

---

## Versioonide ühilduvus

### Paketi versioonide maatriks

Mitme agendi töövoog nõuab spetsiifilisi pakettide versioone. Erinevad versioonid põhjustavad jooksu ajal vigu.

| Pakett | Nõutav versioon | Kontrollkäsk |
|---------|-----------------|--------------|
| `agent-framework-foundry` | viimane | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | viimane | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | viimane | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Levinud versioonivead

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

## Paigaldamisprobleemid

### Konteiner ei käivitu pärast paigaldust

1. **Vaadake konteineri logisid:**
   - Avage **Foundry Toolkit** külgriba → oma projekti alt klõpsake **Agents** → vahekaart **Hosted Agent** → valige oma agent. Kontrollige **Status** vahekaardil **Details**, seejärel avage vahekaart **Playground** ja kasutage **Logs** sektsiooni paneelis **Session Details**, et näha konteineri väljundit.
   - Otsige Python veateateid või puuduvate moodulite vigu.

2. **Levinumad konteineri käivituse vead:**

   | Viga logides | Põhjus | Parandus |
   |--------------|--------|----------|
   | `ModuleNotFoundError` | Pakett `requirements.txt` puudub | Lisage pakett, paigaldage uuesti |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Keskkonnamuutujad `agent.yaml` või `.env` ei ole määratud | Uuendage `agent.yaml` → `environment_variables` osa (hostitud) või `.env` (kohalik) |
   | `azure.identity.CredentialUnavailableError` | Haldatud identiteeti ei ole konfigureeritud | Foundry seab selle automaatselt - veendu, et kasutad laienduse kaudu juurutamist |
   | `OSError: port 8088 already in use` | Dockerfile avaldab vale pordi või ports on konfliktis | Kontrolli `EXPOSE 8088` Dockerfile’is ja `CMD ["python", "main.py"]` |
   | Konteiner väljub koodi 1-ga | Käitlemata erand `main()` | Testi esmalt lokaalselt ([Moodul 5](05-test-locally.md)), et tabada vead enne juurutamist |

3. **Juuruta uuesti pärast parandamist:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → vali sama agent → juuruta uus versioon.

### Juurutamine võtab liiga kaua aega

Mitme agendiga konteinerite käivitamine võtab kauem aega, kuna käivitamisel luuakse 4 agendi eksemplari. Tavalised käivitamisajad:

| Etapp | Eeldatav kestus |
|-------|------------------|
| Konteineri pildi ehitus | 1-3 minutit |
| Pildi edastamine ACR-i | 30-60 sekundit |
| Konteineri käivitamine (üks agent) | 15-30 sekundit |
| Konteineri käivitamine (mitme agendiga) | 30-120 sekundit |
| Agent Playgroundis kättesaadav | 1-2 minutit pärast "Käivitamist" |

> Kui olek "Ootel" püsib kauem kui 5 minutit, kontrolli konteineri logisid vigade suhtes.

---

## RBAC ja õiguste probleemid

### `403 Forbidden` või `AuthorizationFailed`

Sul peab olema **[Foundry User](https://aka.ms/foundry-ext-project-role)** roll oma Foundry projektis (varem nimetatud **Azure AI User** - rolli ID muutmata):

1. Mine [Azure Portaalile](https://portal.azure.com) → oma Foundry **projekti** ressursile.
2. Klõpsa **Juurdepääsu kontroll (IAM)** → **Rolli määramised**.
3. Otsi oma nime → kinnita, et **Foundry User** (või vana nimetus **Azure AI User**) on nimekirjas.
4. Kui puudub: **Lisa** → **Lisa rolli määramine** → otsi **Foundry kasutaja** → määra oma kontole.

Lisateabe saamiseks vaata dokumentatsiooni [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Mudeli juurutus pole ligipääsetav

Kui agent tagastab mudeliga seotud veateateid:

1. Kontrolli, kas mudel on juurutatud: Foundry külgriba → laienda projekt → **Mudlid** → otsi `gpt-4.1-mini` (või oma mudel), mille olek on **Õnnestunud**.
2. Kontrolli, kas juurutuse nimi vastab: võrdle `AZURE_AI_MODEL_DEPLOYMENT_NAME` failis `.env` (või `agent.yaml`) tegeliku juurutuse nimega külgribal.
3. Kui juurutamine aegus (tasuta kiht): juuruta uuesti [Mudeli kataloogist](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry tööriistakomplekt: Avatud mudelikataloog**).

---

## Foundry Local probleemid (rada B)

### Foundry Local teenus ei tööta

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Sümptom | Põhjus | Parandus |
|---------|-------|-----|
| Tervisekontroll tagastab `503` | Teenus ei ole käivitatud | `foundry local start` või klõpsa **Alusta** Foundry Tööriistakomplekti külgribal |
| Tervisekontroll aegub | Mudel laeb endiselt | Oota 30–60 sekundit pärast käivitamist; suuremad mudelid võtavad kauem aega |
| `StatusCode: 404` aadressil `/v1/health` | Vale port | Vaikimisi on `5273`. Kontrolli tegelikku porti `foundry local status` |
| Ebapiisavad ressursid | Foundry Local vajab ~4 GB RAM-i vaba | Sule teised rakendused |
| Mudeli allalaadimine ebaõnnestub | Vähe vaba kettaruumi | Mudelid on 2–8 GB suured. Vabastage ruumi, seejärel `foundry model pull <name>` |

### Mudeli nime sobimatus

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Seadistage `AZURE_AI_MODEL_DEPLOYMENT_NAME` failis `.env` täpselt vastavaks näidatud alias'ega (nt `phi-4-mini`, mitte `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` kohaliku käivitamise puhul (Path B)

Labori `main.py` kasutab `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local nõuab, et see muutuj viitaks kohaliku teenuse aadressile - **mitte** `AZURE_AI_PROJECT_ENDPOINT`. Veenduge, et teie `.env` sisaldab:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP tööriist teeb endiselt väljuva kõne (Path B)

See on oodatud. `search_microsoft_learn_for_plan` tööriist hangib õppematerjale aadressilt `https://learn.microsoft.com/api/mcp`. **Ainult oskuse nime päring** liigub võrgus – CV ja töökirjelduse tekst töödeldakse täielikult teie seadmes ega saadeta kunagi edasi. Kui on vaja täielikku võrguühenduseta toimimist, lisage tööriista `try/except` tagasipöördumine, mis tagastab staatilise `learn.microsoft.com` URL-i, kui lõpp-punkt on kättesaamatu.

---

## Abi saamine

Kui olete ülaltoodud parandustega ummikus:

1. **Kontrollige serveri logisid** – Enamik vigu annab terminalis Python'i stack trace'i. Loe täielik vea tagasijälg.
2. **Otsige veateadet** – Kopeerige veatekst ja otsige seda [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Ava probleem** - Esita probleem [töötoa hoidlas](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) koos:
   - Veateate või ekraanipildiga
   - Oma pakettide versioonidega (`pip list | Select-String "agent-framework"`)
   - Oma Pythoni versiooniga (`python --version`)
   - Kas probleem on lokaalne või pärast juurutamist

---

### Kontrollpunkt

- [ ] Sa tead, kuidas kontrollida ja parandada `.env` seadistusvigu
- [ ] Sa oskad kontrollida, et pakettide versioonid vastaksid nõutud maatriksile
- [ ] Sa tead, kuidas kontrollida konteineri logisid juurutamise vigade jaoks
- [ ] Sa oskad kontrollida RBAC rolle Azure portaalis

---

**Eelmine:** [07 - Kontrolli mänguväljakus](07-verify-in-playground.md) · **Järgmine:** [09 - Kokkuvõte →](09-summary.md) · **Avaleht:** [Labor 02 README](../README.md) · [Töötoa avaleht](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->