# 8 skyrius - trikčių šalinimas

Šiame skyriuje aptariamos dažnos klaidos, pataisymai ir derinimo strategijos, specifinės daugiaagentiniam darbo eigai.

## Agentų išvesties problemos

### GapAnalyzer sako „Aš vis dar neturiu atitinkančio pranešimo“

**Simptomas:** GapAnalyzer atsakymas prašo įklijuoti atitinkantį pranešimą su „Trūkstamais įgūdžiais“ ir „Sertifikavimo spragomis“. Tai vyksta net kai pateikėte tiek gyvenimo aprašymą, tiek darbo aprašymą.

**Priežastis:** Darbo aprašymo tekstas nebuvo perduotas žemyn JD agentui. Naudojant `context_mode="last_agent"`, `resume_executor` yra vienintelis vykdytojas, kuris mato vartotojo pradinį pranešimą. Jei `RESUME_PARSER_INSTRUCTIONS` neįtraukia darbo aprašymo teksto į išvestį, JD agentas neturi darbo aprašymo parsinti, MatchingAgent negali apskaičiuoti atitikimo balo, o GapAnalyzer gauna beprasmį įvestį.

**Diagnostika:**

Serverio žurnaluose ieškokite MatchingAgent sekos. Jei joje yra:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pralaidumas yra praleistas arba sugadintas.

**Pataisa:** Patikrinkite, ar `RESUME_PARSER_INSTRUCTIONS` faile `main.py` yra `[JOB DESCRIPTION PASS-THROUGH]` skyrius ir taisyklė:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Taip pat patikrinkite, ar `JOB_DESCRIPTION_INSTRUCTIONS` turi `[PARSED RESUME PASS-THROUGH]` perdavimo taisyklę:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jei kuris nors instrukcijų blokas yra šablonas iš karkaso vedlio, pakeiskite jį pilna versija iš [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent išveda „Negali apskaičiuoti atitikimo balo - darbo aprašymas nepateiktas“

Tai ta pati pagrindinė priežastis kaip aukščiau. MatchingAgent gavo JD agento išvestį, bet `[PARSED RESUME PASS-THROUGH]` skyrius trūko arba buvo tuščias, todėl jis negalėjo palyginti abiejų profilių. Patikrinkite:
1. `JOB_DESCRIPTION_INSTRUCTIONS` apima perdavimo taisyklę: `Nukopijuokite [PARSED RESUME] žodžiu žodin - Matching Agent remiasi tuo žemyninis.`
2. `MATCHING_AGENT_INSTRUCTIONS` nurodo agentui ieškoti `[JD REQUIREMENTS]` ir `[PARSED RESUME PASS-THROUGH]` skyrių.

Pakeiskite abu instrukcijų blokus su pilnomis versijomis iš [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Atsakymas pasirodo du kartus

**Simptomas:** GapAnalyzer išvestis (arba visa kanalo išvestis) Agent Inspector atsakyme pasirodo du kartus.

**Priežastis:** `WorkflowBuilder` naudoja ARBA semantiką įeinančioms jungtims - žemyninis vykdytojas įsijungia, kai tik bet kuris priešininkas baigiasi. Jei `matching_executor` turi dvi įeinančias jungtis (viena iš `resume_executor` ir kita iš `jd_executor`), jis paleidžiamas du kartus: vieną kartą kai ResumeParser baigia ir dar kartą kai JD agentas baigia. Tada ir GapAnalyzer taip pat paleidžiamas du kartus.

**Pataisa:** Užtikrinkite, kad `WorkflowBuilder` grafikas būtų griežtai sekvencinis kanalas be konvergencijos:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NE iš resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jei turite klaidžiojančią `.add_edge(resume_executor, matching_executor)` eilutę, pašalinkite ją. `[PARSED RESUME PASS-THROUGH]` perdavimas JD agento išvestyje jau suteikia MatchingAgent priėjimą prie gyvenimo aprašymo.

---

## Aplinkos ir konfigūracijos problemos

### Trūkstamos arba netinkamos `.env` reikšmės

`.env` failas turi būti `PersonalCareerCopilot/` kataloge (tame pačiame lygyje kaip `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Laukiamas `.env` turinys:

**A variantas - Foundry debesyje:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**B variantas - Foundry vietinis:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Abu keliai naudoja `FOUNDRY_PROJECT_ENDPOINT`. Vertė skiriasi: debesyje naudojamas `https://` Foundry galinis taškas; vietiniame naudojamas `http://localhost:5273/v1`. Paleiskite komandą `foundry model list`, kad patvirtintumėte tikslią modelio slapyvardį B keliui.

> **Kaip rasti savo `FOUNDRY_PROJECT_ENDPOINT`:** 
- Atidarykite **Foundry Toolkit** šoninę juostą VS Code → dešiniuoju pelės mygtuku spustelėkite savo projektą → **Copy Project Endpoint**. 
- Arba eikite į [Azure Portal](https://portal.azure.com) → savo Foundry projektą → **Overview** → **Project endpoint**.

> **Kaip rasti `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Foundry Toolkit šoninėje juostoje išplėskite projektą → **Models** → raskite savo diegto modelio pavadinimą (pvz., `gpt-4.1-mini`).

### Aplinkos kintamųjų prioriteto tvarka

`main.py` naudoja `load_dotenv(override=True)`, kas reiškia:

| Prioritetas | Šaltinis | Laimi, kai abu nustatyti? |
|------------|----------|---------------------------|
| 1 (aukščiausias) | `.env` failas | Taip |
| 2 | Korpuso / konteinerio aplinkos kintamasis | Naudojamas, kai to paties rakto nėra `.env` |

Vietinėje kūrimo aplinkoje tai reiškia, kad `.env` yra tikrasis šaltinis (redaguojant `.env` iš karto paveikiamos vykdymo kartos). Talpinant serveriuose, Foundry įpurškia aplinkos kintamuosius konteinerio lygyje; kadangi `.env` nėra diegiamo paveikslo dalis šioje laboratorijoje, naudojamos įpurškintos konteinerio reikšmės.

---

## Versijų suderinamumas

### Paketų versijų matrica

Daugiaagentė darbo eiga reikalauja tam tikrų paketų versijų. Nesuderintos versijos sukelia vykdymo klaidas.

| Paketas | Reikalinga versija | Patikros komanda |
|---------|-------------------|------------------|
| `agent-framework-foundry` | naujausia | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | naujausia | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | naujausia | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Dažnos versijų klaidos

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Pataisyti: iš naujo įdiegti agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Ištaisyti: atnaujinti mcp paketą
pip install mcp --upgrade
```

### Patikrinkite visas versijas vienu metu

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Laukiamas išvestis:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Diegimo problemos

### Konteineris nepavyksta paleisti po diegimo

1. **Patikrinkite konteinerio žurnalus:**
   - Atidarykite **Foundry Toolkit** šoninę juostą → išplėskite **Hosted Agents (Preview)** → spustelėkite savo agentą → išplėskite versiją → **Container Details** → **Logs**.
   - Ieškokite Python klaidų aprašų arba trūkstamų modulių klaidų.

2. **Dažnos konteinerio paleidimo klaidos:**

   | Klaida žurnaluose | Priežastis | Pataisa |
   |------------------|------------|----------|
   | `ModuleNotFoundError` | `requirements.txt` trūksta paketo | Pridėkite paketą, įdiekite iš naujo |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` arba `.env` aplinkos kintamieji nenustatyti | Atnaujinkite `agent.yaml` → `environment_variables` skyrių (hosted) arba `.env` (vietinis) |
   | `azure.identity.CredentialUnavailableError` | Nesuinstaliuota Managed Identity | Foundry tai kuriama automatiškai - įsitikinkite, kad diegiate per plėtinį |
   | `OSError: port 8088 already in use` | Dockerfile atskleidžia netinkamą uostą arba kyla uosto konfliktas | Patikrinkite `EXPOSE 8088` Dockerfile ir `CMD ["python", "main.py"]` |
   | Konteineris išeina su kodu 1 | Nepažymėta išimtis `main()` | Patikrinkite vietoje pirmiausia ([5 skyrius](05-test-locally.md)) klaidų sugavimui prieš diegimą |

3. **Paleiskite diegimą iš naujo pataisę:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → pasirinkite tą patį agentą → įdiekite naują versiją.

### Diegimo užtrukimas per ilgai

Daugiaagentiški konteineriai užtrunka ilgiau paleisti, nes paleidimo metu sukuria 4 agentų egzempliorius. Įprasti paleidimo laikai:

| Etapas | Laukiamas trukmė |
|--------|------------------|
| Konteinerio vaizdo kūrimas | 1-3 minutės |
| Vaizdo nusiuntimas į ACR | 30-60 sekundžių |
| Konteinerio paleidimas (vienas agentas) | 15-30 sekundžių |
| Konteinerio paleidimas (daugiaagentis) | 30-120 sekundžių |
| Agentas pasiekiamas Playground | 1-2 minutės po „Started“ pranešimo |

> Jei „Pending“ būsena trunka ilgiau nei 5 minutes, patikrinkite konteinerio žurnalus klaidoms.

---

## RBAC ir leidimų problemos

### `403 Forbidden` arba `AuthorizationFailed`

Jums reikalinga **[Foundry vartotojo](https://aka.ms/foundry-ext-project-role)** rolė jūsų Foundry projekte (anksčiau vadinosi **Azure AI vartotojas** - rolės ID nepasikeitė):

1. Eikite į [Azure Portal](https://portal.azure.com) → savo Foundry **projekto** išteklių.
2. Spustelėkite **Prieigos valdymas (IAM)** → **Rolės priskyrimai**.
3. Ieškokite savo vardo → patikrinkite, ar nurodyta **Foundry vartotojas** (arba senoji žyma **Azure AI vartotojas**).
4. Jei trūksta: spustelėkite **Pridėti** → **Pridėti rolės priskyrimą** → ieškokite **Foundry vartotojas** → priskirkite savo paskyrai.

Daugiau informacijos ieškokite [RBAC dokumentacijoje Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Modelio diegimas neprieinamas

Jei agentas grąžina su modeliu susijusias klaidas:

1. Patikrinkite, ar modelis įdiegtas: Foundry šoninėje juostoje išplėskite projektą → **Models** → ieškokite `gpt-4.1-mini` (ar jūsų modelio) su statusu **Succeeded**.
2. Patikrinkite, ar diegimo pavadinimas sutampa: palyginkite `AZURE_AI_MODEL_DEPLOYMENT_NAME` `.env` faile (arba `agent.yaml`) su faktiniu diegimo vardu šoninėje juostoje.
3. Jei diegimas pasibaigė (nemokama versija): įdiekite iš naujo iš [Modelų katalogo](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problemos (B variantas)

### Foundry Local paslauga neveikia

```powershell
# Patikrinti būseną
foundry local status

# Paleisti paslaugą, jei ji sustabdyta
foundry local start
```

| Simptomas | Priežastis | Pataisa |
|---------|------------|----------|
| Sveikatos patikra grąžina `503` | Paslauga neįjungta | Paleiskite `foundry local start` arba spustelėkite **Start** Foundry Toolkit šoninėje juostoje |
| Sveikatos patikra baigiasi laiko limitu | Modelis dar kraunasi | Palaukite 30–60 sek. po paleidimo; didesni modeliai užtrunka ilgiau |
| `StatusCode: 404` adresu `/v1/health` | Netinkamas uostas | Numatyta `5273`. Patikrinkite `foundry local status`, kad sužinotumėte faktinį uostą |
| Nepakanka resursų | Foundry Local reikalauja ~4 GB laisvos RAM | Uždarykite kitas programas |
| Modelio atsisiuntimas nepavyksta | Mažai disko vietos | Modeliai užima 2–8 GB. Atlaisvinkite vietos ir tada paleiskite `foundry model pull <name>` |

### Modelio pavadinimo neatitikimas

```powershell
# Išvardinkite atsisiųstus modelius ir jų tikrus aliasus
foundry model list
```

Nustatykite `AZURE_AI_MODEL_DEPLOYMENT_NAME` `.env` faile tiksliai pagal rodomą slapyvardį (pvz., `phi-4-mini`, ne `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` vietiniam paleidimui (B variantas)

Laboratorijos `main.py` naudoja `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local reikalauja, kad šis kintamasis nurodytų vietinę paslaugą - **ne** `AZURE_AI_PROJECT_ENDPOINT`. Užtikrinkite, kad jūsų `.env` failas turi:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP įrankis vis dar siunčia išorinį kvietimą (B variantas)

Tai tikėtina. Įrankis `search_microsoft_learn_for_plan` gauna mokymosi išteklius iš `https://learn.microsoft.com/api/mcp`. **Tik įgūdžių pavadinimo užklausa** keliauja tinklu - gyvenimo aprašymas ir darbo aprašymas apdorojami visiškai jūsų įrenginyje ir niekada nepasiunčiami tinklu. Jei reikalinga visiškai offline veikla, pridėkite `try/except` rezervinį variantą į įrankį, kuris, jei endpointas nepasiekiamas, grąžina statinį `learn.microsoft.com` URL.

---

## Pagalbos gavimas

Jei likote įstrigę net ir išbandę aukščiau pateiktus pataisymus:

1. **Patikrinkite serverio žurnalus** - dauguma klaidų pateikia Python klaidų aprašą terminale. Perskaitykite visą klaidos grandinę.
2. **Ieškokite klaidos pranešimo** - Nukopijuokite klaidos tekstą ir ieškokite [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Atidarykite problemą** - Pateikite klausimą [workshop saugykloje](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) su:
   - Klaidos pranešimu arba ekrano nuotrauka
   - Jūsų paketų versijomis (`pip list | Select-String "agent-framework"`)
   - Jūsų Python versija (`python --version`)
   - Ar problema vietinė, ar po diegimo

---

### Tikrinimo taškas

- [ ] Mokate patikrinti ir išspręsti `.env` konfigūracijos problemas
- [ ] Galite patikrinti, kad paketų versijos atitiktų reikalaujamą matricą
- [ ] Mokate tikrinti konteinerio žurnalus diegimo nesėkmėms
- [ ] Galite patikrinti RBAC roles Azure portale

---

**Ankstesnis:** [07 - Tikrinimas Playground](07-verify-in-playground.md) · **Kitas:** [09 - Santrauka →](09-summary.md) · **Pradžia:** [Laboratorija 02 README](../README.md) · [Dirbtuvės pradžia](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->