# 8 modulis - Trikčių šalinimas

Šiame modulyje aptariamos dažniausios klaidos, jų taisymai ir derinimo strategijos, būdingos daugiaagentiniam darbo eigai.

## Agentų išvesties problemos

### GapAnalyzer sako „Aš vis dar neturiu atitinkančio ataskaitos“

**Simptomai:** GapAnalyzer atsakymas prašo įklijuoti atitinkančią ataskaitą su „Trūkstamais įgūdžiais“ ir „Sertifikavimo spragomis“. Tai vyksta net jei jūs išsiuntėte tiek gyvenimo aprašymą, tiek darbo aprašymą.

**Priežastis:** JD tekstas nebuvo perduotas žemyn JD agentui. Su `context_mode="last_agent"`, `resume_executor` yra vienintelis vykdytojas, kuris kada nors mato vartotojo pradinį pranešimą. Jei `RESUME_PARSER_INSTRUCTIONS` neįtraukia JD teksto į savo išvestį, JD agentas neturi JD, kurį galėtų analizuoti, MatchingAgent negali apskaičiuoti tinkamumo įvertinimo, o GapAnalyzer gauna beprasmę įvestį.

**Diagnozė:**

Serverio žurnaluose ieškokite MatchingAgent ploto. Jei jame yra:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
tada perdavimas trūksta arba yra sugadintas.

**Taisymas:** Patvirtinkite, kad `RESUME_PARSER_INSTRUCTIONS` faile `main.py` yra `[JOB DESCRIPTION PASS-THROUGH]` skyrius ir taisyklė:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Taip pat patvirtinkite, kad `JOB_DESCRIPTION_INSTRUCTIONS` turi `[PARSED RESUME PASS-THROUGH]` perdavimo taisyklę:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jei kuri nors instrukcijų dalis yra šablonas iš ramstinio vedlio, pakeiskite ją pilna versija iš [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent išveda „Negalima apskaičiuoti tinkamumo įvertinimo - JD nepateiktas“

Tai ta pati pagrindinė priežastis kaip aukščiau. MatchingAgent gavo JD agento išvestį, bet `[PARSED RESUME PASS-THROUGH]` skyrius trūko arba buvo tuščias, todėl negalėjo palyginti dviejų profilių. Patvirtinkite:
1. `JOB_DESCRIPTION_INSTRUCTIONS` įtraukia perdavimo taisyklę: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` nurodo agentui ieškoti `[JD REQUIREMENTS]` ir `[PARSED RESUME PASS-THROUGH]` skyrių.

Pakeiskite abu instrukcijų blokus pilnomis versijomis iš [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Atsakymas pasirodo du kartus

**Simptomai:** GapAnalyzer išvestis (arba visas darbo eigos išvestis) pasirodo du kartus Agent Inspector atsakyme.

**Priežastis:** `WorkflowBuilder` naudoja OR-semantiką atėjimo kraštinėms – pakopinį vykdytoją paleidžia vos tik baigiasi **bet kuris** tiesioginis pirmtakas. Jei `matching_executor` turi dvi atėjimo kraštines (vieną iš `resume_executor` ir kitą iš `jd_executor`), jis paleidžiamas du kartus: kartą kai baigia ResumeParser ir dar kartą kai baigia JD Agent. Tada GapAnalyzer taip pat veikia du kartus.

**Sprendimas:** Užtikrinkite, kad `WorkflowBuilder` grafas būtų griežtai sekanti linija be susijungimų:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jei turite klaidžiojančią `.add_edge(resume_executor, matching_executor)` eilutę, ją pašalinkite. `[PARSED RESUME PASS-THROUGH]` perdavimas JD Agent išvestyje jau suteikia MatchingAgent prieigą prie CV.

---

## Aplinkos ir konfigūracijos problemos

### Trūksta arba neteisingos `.env` reikšmės

`.env` failas turi būti `PersonalCareerCopilot/` kataloge (toje pačioje lygyje kaip ir `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Tikėtinas `.env` turinys:

**1 kelias - Foundry debesyje:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**2 kelias - Foundry lokaliai:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Abu keliai naudoja `FOUNDRY_PROJECT_ENDPOINT`. Vertė skiriasi: debesyje naudojamas `https://` Foundry galinis taškas; lokaliai - `http://localhost:5273/v1`. Vykdykite `foundry model list`, kad patvirtintumėte tikslią modelio pravardę 2 keliui.

> **Kaip rasti savo `FOUNDRY_PROJECT_ENDPOINT`:** 
- Atidarykite **Foundry Toolkit** šoninę juostą VS Code → dešiniuoju pelės klavišu spauskite projektą → **Copy Project Endpoint**. 
- Arba eikite į [Azure Portal](https://portal.azure.com) → savo Foundry projektą → **Overview** → **Project endpoint**.

> **Kaip rasti savo `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Foundry Toolkit šoninėje juostoje išplėskite projektą → **Models** → raskite diegiamo modelio pavadinimą (pvz., `gpt-4.1-mini`).

### Aplinkos kintamųjų prioritetas

`main.py` naudoja `load_dotenv(override=True)`, tai reiškia:

| Prioritetas | Šaltinis | Kuris laimi, jei abu nustatyti? |
|----------|--------|-------------------------------|
| 1 (aukščiausias) | `.env` failas | Taip |
| 2 | Shell / konteinerio aplinkos kintamasis | Naudojamas, jei to paties rakto nėra `.env` |

Vietinėje plėtroje tai reiškia, kad `.env` yra tiesos šaltinis (redaguojant `.env` iš karto paveikiami vykdymai). Hostinamo diegimo metu Foundry injekuoja aplinkos kintamuosius konteinerio lygiu; kadangi `.env` nėra įtrauktas į šio laboratorinio rinkinio diegimo atvaizdą, naudojamos injekuotos konteinerio reikšmės.

---

## Versijų suderinamumas

### Paketo versijų matrica

Multi-agent darbo eiga reikalauja specifinių paketų versijų. Nesuderinamos versijos sukelia vykdymo klaidas.

| Paketas | Reikalaujama versija | Patikrinimo komanda |
|---------|---------------------|---------------------|
| `agent-framework-foundry` | latest | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | latest | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | latest | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Dažnos versijų klaidos

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

### Patikrinkite visas versijas vienu metu

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Tikėtinas rezultatas:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Diegimo problemos

### Konteineris nepaleidžiamas po diegimo

1. **Patikrinkite konteinerio žurnalus:**
   - Atidarykite **Foundry Toolkit** šoninę juostą → po savo projektu spauskite **Agents** → **Hosted Agent** skirtuką → spauskite savo agentą. Patikrinkite **Status** skiltyje **Details**, tuomet atidarykite skirtuką **Playground** ir naudokite **Logs** kortelę **Session Details** panele pamatyti konteinerio išvestį.
   - Ieškokite Python išimtinių sekų arba trūkstamų modulių klaidų.

2. **Dažnos konteinerio paleidimo klaidos:**

   | Klaidų žurnaluose | Priežastis | Sprendimas |
   |-------------------|-----------|------------|
   | `ModuleNotFoundError` | Trūksta `requirements.txt` paketo | Įdiekite paketą, iš naujo diegkite |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Nepakankami `agent.yaml` ar `.env` aplinkos kintamieji | Atnaujinkite `agent.yaml` → `environment_variables` skyrių (hostinimas) arba `.env` (lokaliai) |
   | `azure.identity.CredentialUnavailableError` | Valdomas identitetas nekonfigūruotas | Foundry nustato automatiškai – įsitikinkite diegiant per plėtinį |
   | `OSError: port 8088 already in use` | Dockerfile atskleidžia netinkamą prievadą arba prievadų konfliktas | Patikrinkite `EXPOSE 8088` Dockerfile ir `CMD ["python", "main.py"]` |
   | Konteineris išeina su 1 kodu | Nepavaduota išimtis `main()` | Pirmiausia testuokite lokaliai ([5 modulis](05-test-locally.md)) klaidoms sužinoti prieš diegiant |

3. **Iš naujo įdiekite ištaisę:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → pasirinkite tą patį agentą → įdiekite naują versiją.

### Diegimas užtrunka per ilgai

Daugiagentiniai konteineriai užtrunka ilgiau pradėti, nes sukuriami 4 agento egzemplioriai paleidimo metu. Normalūs paleidimo laikai:

| Etapas | Tikėtinas trukmė |
|-------|-------------------|
| Konteinerio vaizdo kūrimas | 1-3 minutės |
| Vaizdo įkėlimas į ACR | 30-60 sekundžių |
| Konteinerio paleidimas (vienas agentas) | 15-30 sekundžių |
| Konteinerio paleidimas (daugiaagentinis) | 30-120 sekundžių |
| Agentas pasiekiamas Playground | 1-2 minutės po "Started" |

> Jei statusas "Pending" išlieka ilgiau nei 5 minutes, patikrinkite konteinerio žurnalus klaidoms.

---

## RBAC ir leidimų problemos

### `403 Forbidden` arba `AuthorizationFailed`

Jums reikalinga **[Foundry User](https://aka.ms/foundry-ext-project-role)** rolė jūsų Foundry projekte (anksčiau pavadinta **Azure AI User** – rolės ID nepasikeitė):

1. Eikite į [Azure Portal](https://portal.azure.com) → savo Foundry **projekto** išteklių.
2. Spauskite **Access control (IAM)** → **Role assignments**.
3. Susiraskite savo vardą → patikrinkite, ar yra sąraše **Foundry User** (ar senasis pavadinimas **Azure AI User**).
4. Jei trūksta: spauskite **Add** → **Add role assignment** → ieškokite **Foundry User** → priskirkite savo paskyrai.

Daugiau informacijos rasite [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokumentacijoje.

### Modelio diegimas nepasiekiamas

Jei agentas grąžina modelio susijusias klaidas:

1. Patikrinkite, ar modelis įdiegtas: Foundry šoninėje juostoje išplėskite projektą → **Models** → patikrinkite ar yra `gpt-4.1-mini` (ar jūsų modelis) su statusu **Succeeded**.
2. Patikrinkite diegimo vardą: palyginkite `AZURE_AI_MODEL_DEPLOYMENT_NAME` faile `.env` (ar `agent.yaml`) su faktiniu diegimo vardu šoninėje juostoje.
3. Jei diegimas pasibaigęs (nemokamas sluoksnis): iš naujo įdiekite iš [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problemos (2 kelias)

### Foundry Local paslauga neveikia

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Simptomas | Priežastis | Sprendimas |
|---------|-----------|----------|
| Health check grąžina `503` | Paslauga nepaleista | `foundry local start` arba spustelėkite **Start** Foundry Toolkit šoninėje juostoje |
| Health check išeina dėl laiko | Modelis dar kraunasi | Palaukite 30–60 sek. po paleidimo; didesni modeliai kraunasi ilgiau |
| `StatusCode: 404` ant `/v1/health` | Netinkamas prievadas | Numatytoji reikšmė yra `5273`. Patikrinkite `foundry local status` dėl faktinio prievado |
| Nepakanka resursų | Foundry Local reikia maždaug 4 GB RAM laisvos | Uždarykite kitas programas |
| Modelio atsisiuntimas nepavyksta | Maža disko vieta | Modeliai užima 2–8 GB. Atlaisvinkite vietos ir tada `foundry model pull <name>` |

### Modelio pavadinimo neatitiktis

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Nustatykite `AZURE_AI_MODEL_DEPLOYMENT_NAME` faile `.env` tiksliai tokią pravardę, kaip nurodyta (pvz., `phi-4-mini`, ne `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` vietiniame paleidime (2 kelias)

Laboratorijos `main.py` naudoja `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local reikalauja, kad ši kintamoji rodytų į lokalią paslaugą - **ne** `AZURE_AI_PROJECT_ENDPOINT`. Įsitikinkite, kad jūsų `.env` turi:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP įrankis vis dar siunčia išėjimą į tinklą (2 kelias)

Tai normalu. `search_microsoft_learn_for_plan` įrankis gauna mokymosi išteklius iš `https://learn.microsoft.com/api/mcp`. **Tik užklausa dėl įgūdžio pavadinimo** keliauja per tinklą – CV ir JD tekstas apdorojamas visiškai jūsų įrenginyje ir niekada nėra perduodamas. Jei reikalinga visiškai neprisijungus veikianti operacija, pridėkite `try/except` atsarginį metodą į įrankį, kuris grąžina statinį `learn.microsoft.com` URL, kai galinis taškas nepasiekiamas.

---

## Pagalbos gavimas

Jei užstrigote po aukščiau pateiktų pataisymų bandymo:

1. **Peržiūrėkite serverio žurnalus** – dauguma klaidų pateikia Python klaidų seką terminale. Perskaitykite visą klaidų seką.
2. **Ieškokite klaidos pranešimo** – nukopijuokite klaidos tekstą ir ieškokite [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Atidarykite problemos pranešimą** – pateikite problemą [darbo sandėlyje](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) kartu su:
   - Klaidos pranešimu arba ekrano kopija
   - Jūsų paketų versijomis (`pip list | Select-String "agent-framework"`)
   - Jūsų Python versija (`python --version`)
   - Ar klaida lokali, ar po diegimo

---

### Patikrinimo taškas

- [ ] Jūs žinote, kaip patikrinti ir taisyti `.env` konfigūracijos problemas
- [ ] Galite patikrinti, kad paketų versijos atitinka reikalaujamas matricas
- [ ] Jūs žinote, kaip patikrinti konteinerio žurnalus dėl diegimo klaidų
- [ ] Galite patikrinti RBAC roles Azure Portale

---

**Ankstesnis:** [07 - Verify in Playground](07-verify-in-playground.md) · **Kitas:** [09 - Summary →](09-summary.md) · **Pradžia:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->