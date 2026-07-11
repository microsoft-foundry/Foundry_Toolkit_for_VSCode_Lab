# Moduli 8 - Kusuluhisha Matatizo

Moduli hii inashughulikia makosa ya kawaida, marekebisho, na mikakati ya kutatua matatizo maalum kwa mtiririko wa kazi wa mawakala wengi.

## Masuala ya matokeo ya Wakala

### GapAnalyzer anasema “Bado sina ripoti inayolingana”

**Dalili:** Jibu la GapAnalyzer linakuomba uweke ripoti inayolingana inayojumuisha "Ujuzi Uliokosekana" na "Mapungufu ya Cheti." Hii hutokea hata wakati ulituma wasifu na maelezo ya kazi.

**Sababu:** Maandishi ya JD hayakupitishwa kwa upande wa wakala wa JD. Kwa `context_mode="last_agent"`, `resume_executor` ni mtendaji pekee anayewaona ujumbe halisi wa mtumiaji. Ikiwa `RESUME_PARSER_INSTRUCTIONS` haitajumuishi maandishi ya JD katika matokeo yake, Wakala wa JD hana JD ya kuchambua, Wakala wa Kulinganisha hawezi kukokotoa alama ya ulinganifu, na GapAnalyzer hupokea ingizo lisilo na maana.

**Uchunguzi:**

Katika rekodi za seva, tafuta sehemu ya Wakala wa Kulinganisha. Ikiwa ina:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
kupitishwa kwa mbele hukosekana au imevunjika.

**Rekebisha:** Thibitisha kuwa `RESUME_PARSER_INSTRUCTIONS` katika `main.py` ina sehemu ya `[JOB DESCRIPTION PASS-THROUGH]` na kanuni:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Pia thibitisha kuwa `JOB_DESCRIPTION_INSTRUCTIONS` ina kanuni ya kupitisha `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Kama mojawapo ya mabalozi ya maagizo ni mwanzilishi kutoka kwa wizard wa muundo, badilisha na toleo kamili kutoka [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent hutoa “Haiwezi kukokotoa alama ya ulinganifu - hakuna JD iliyotolewa”

Hii ni sababu sawa kama ilivyotajwa hapo juu. MatchingAgent alipokea matokeo ya Wakala wa JD lakini sehemu ya `[PARSED RESUME PASS-THROUGH]` ilikuwa haipo au tupu, hivyo haikuweza kulinganisha wasifu mbili. Thibitisha:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inajumuisha kanuni ya kupitisha: `Nakili [PARSED RESUME] kama ilivyo - Wakala wa Kulinganisha unategemea hili chini ya mto.`
2. `MATCHING_AGENT_INSTRUCTIONS` inaelekeza wakala kutafuta sehemu za `[JD REQUIREMENTS]` na `[PARSED RESUME PASS-THROUGH]`.

Badilisha mabalozi yote ya maagizo na matoleo kamili kutoka [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Jibu linatokea mara mbili

**Dalili:** Matokeo ya GapAnalyzer (au matokeo ya bomba zima) yanaonekana mara mbili katika jibu la Mchunguzi wa Wakala.

**Sababu:** `WorkflowBuilder` inatumia mantiki ya AU kwa mipaka inayotoka - mtendaji wa chini huchomeka mara moja mwanzo wowote kukamilika kwa mtangulizi. Ikiwa `matching_executor` ana miunganisho miwili inayoingia (moja kutoka `resume_executor` na moja kutoka `jd_executor`), huchomeka mara mbili: mara moja wakati ResumeParser anakamilisha na tena wakati Wakala wa JD anakamilisha. GapAnalyzer pia hufanya mara mbili.

**Rekebisha:** Hakikisha mchoro wa `WorkflowBuilder` ni bomba linalofuata mlolongo kwa ukali bila kupita mara nyingi:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # SI kutoka kwa resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Kama una mstari wa ziada wa `.add_edge(resume_executor, matching_executor)`, uondoe. Kupitishwa kwa `[PARSED RESUME PASS-THROUGH]` katika matokeo ya Wakala wa JD tayari kunampa Wakala wa Kulinganisha ufikiaji wa wasifu.

---

## Masuala ya Mazingira na usanidi

### Maadili ya `.env` yaliyokosekana au si sahihi

Faili la `.env` lazima liwe katika saraka ya `PersonalCareerCopilot/` (ngazi sawa na `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Yaliyotarajiwa kwenye `.env`:

**Njia A - Hali ya wingu la Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Njia B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Njia zote mbili zinatumia `FOUNDRY_PROJECT_ENDPOINT`. Thamani zinatofautiana: wingu hutumia kiungo cha Foundry `https://`; local inatumia `http://localhost:5273/v1`. Endesha `foundry model list` kuthibitisha jina sahihi la mfano kwa Njia B.

> **Kupata `FOUNDRY_PROJECT_ENDPOINT`:** 
- Fungua upau wa zana wa **Foundry Toolkit** kwenye VS Code → bonyeza kulia mradi wako → **Nakili Kiungo cha Mradi**. 
- Au nenda [Azure Portal](https://portal.azure.com) → mradi wako wa Foundry → **Muhtasari** → **Kiungo cha mradi**.

> **Kupata `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Katika upau wa zana wa Foundry Toolkit, panua mradi wako → **Models** → tafuta jina la mfano uliowekwa (mfano, `gpt-4.1-mini`).

### Kipaumbele cha mabadiliko ya mazingira

`main.py` inatumia `load_dotenv(override=True)`, ambayo ina maana:

| Kipaumbele | Chanzo | Hushinda wakati vyote vikipo? |
|----------|--------|------------------------|
| 1 (kubwa zaidi) | Faili la `.env` | Ndio |
| 2 | Kigeuzi cha shell / mazingira ya kontena | Kinatumiwa wakati ufunguo sawa haupo katika `.env` |

Katika maendeleo ya ndani, hili linafanya `.env` kuwa chanzo cha ukweli (kuhariri `.env` huathiri mara moja utekelezaji). Katika usambazaji uliowekwa mwenyeji, Foundry huingiza vigeuzi vya mazingira kwenye ngazi ya kontena; kwani `.env` si sehemu ya picha iliyowekwa kwa maabara hii, thamani za kontena zilizowekwa hutumika.

---

## Ulinganifu wa toleo

### Jedwali la matoleo ya pakiti

Mtiririko wa mawakala wengi unahitaji matoleo maalum ya pakiti. Matoleo yasiyolingana husababisha makosa wakati wa utekelezaji.

| Pakiti | Toleo Linalohitajika | Amri ya Kukagua |
|---------|-----------------|---------------|
| `agent-framework-foundry` | ya hivi karibuni | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ya hivi karibuni | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ya hivi karibuni | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Makosa ya kawaida ya matoleo

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Rekebisha: viongeze upya agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Rekebisha: boresha kifurushi cha mcp
pip install mcp --upgrade
```

### Thibitisha matoleo yote mara moja

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Matokeo yanayotarajiwa:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Masuala ya usambazaji

### Kontena haianzi baada ya usambazaji

1. **Angalia rekodi za kontena:**
   - Fungua upau wa zana wa **Foundry Toolkit** → panua **Hosted Agents (Preview)** → bonyeza wakala wako → panua toleo → **Maelezo ya Kontena** → **Rekodi**.
   - Tafuta makosa ya mfuatano wa Python au makosa ya moduli iliyokosekana.

2. **Makosa ya kawaida ya kuanzisha kontena:**

   | Makosa katika rekodi | Sababu | Rekebisho |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` haijajumuisha pakiti | Ongeza pakiti, sambaza upya |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Vigeuzi vya mazingira `agent.yaml` au `.env` havijapangwa | Sasisha `agent.yaml` → sehemu ya `environment_variables` (iliyohudumiwa) au `.env` (ya ndani) |
   | `azure.identity.CredentialUnavailableError` | Utambulisho uliosimamiwa haujapangwa | Foundry huandaa hii moja kwa moja - hakikisha unasambaza kupitia ugani |
   | `OSError: port 8088 already in use` | Dockerfile inaonyesha bandari isiyo sahihi au mgongano wa bandari | Hakikisha `EXPOSE 8088` katika Dockerfile na `CMD ["python", "main.py"]` |
   | Kontena inatoka na msimbo 1 | Hitilafu isiyoshughulikiwa katika `main()` | Jaribu ndani kwanza ([Moduli 5](05-test-locally.md)) ili kugundua makosa kabla ya kusambaza |

3. **Sambaza upya baada ya kurekebisha:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → chagua wakala ule ule → sambaza toleo jipya.

### Usambazaji huchukua muda mrefu

Kontena za mawakala wengi huchukua muda mrefu kuanzishwa kwa sababu zinaunda mifano 4 ya wakala wakati wa kuanzisha. Muda wa kawaida wa kuanzisha:

| Hatua | Muda unaotarajiwa |
|-------|------------------|
| Ujenzi wa picha ya kontena | Dakika 1-3 |
| Kuchomeka picha kwenye ACR | Sekunde 30-60 |
| Kuanzisha kontena (wakala mmoja) | Sekunde 15-30 |
| Kuanzisha kontena (mawakala wengi) | Sekunde 30-120 |
| Wakala anapatikana kwenye Playground | Dakika 1-2 baada ya "Imeanza" |

> Ikiwa hali ya "Inasubiri" inaendelea zaidi ya dakika 5, angalia rekodi za kontena kwa makosa.

---

## Masuala ya RBAC na ruhusa

### `403 Forbidden` au `AuthorizationFailed`

Unahitaji jukumu la **[Mtumiaji wa Foundry](https://aka.ms/foundry-ext-project-role)** kwenye mradi wako wa Foundry (awali lilikuwa jina **Azure AI User** - ID ya jukumu haisumbuki):

1. Nenda [Azure Portal](https://portal.azure.com) → rasilimali ya mradi wako wa Foundry.
2. Bonyeza **Udhibiti wa Upatikanaji (IAM)** → **Mteuzi wa Majukumu**.
3. Tafuta jina lako → thibitisha **Foundry User** (au lebo ya zamani **Azure AI User**) iko kwenye orodha.
4. Ikiwa haipo: **Ongeza** → **Ongeza uteuzi wa jukumu** → tafuta **Foundry User** → waipe akaunti yako.

Angalia nyaraka za [RBAC kwa Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) kwa maelezo zaidi.

### Usambazaji wa mfano haupatikani

Ikiwa wakala anarejesha makosa yanayohusiana na mfano:

1. Thibitisha mfano umewekwa: Upau wa zana wa Foundry → panua mradi → **Models** → angalia `gpt-4.1-mini` (au mfano wako) na hali ya **Imefanikiwa**.
2. Thibitisha jina la usambazaji linafanana: linganisha `AZURE_AI_MODEL_DEPLOYMENT_NAME` katika `.env` (au `agent.yaml`) na jina halisi la usambazaji kwenye upau wa zana.
3. Ikiwa usambazaji umeisha muda (kipengele cha bure): sambaza tena kutoka [Katalogi ya Mfano](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Masuala ya Foundry Local (Njia B)

### Huduma ya Foundry Local haifanyi kazi

```powershell
# Angalia hali
foundry local status

# Anza huduma ikiwa imezimwa
foundry local start
```

| Dalili | Sababu | Rekebisho |
|---------|-------|-----|
| Ukaguzi wa afya unatuma `503` | Huduma haijaanza | Endesha `foundry local start` au bonyeza **Anza** kwenye upau wa zana wa Foundry Toolkit |
| Ukaguzi wa afya unachelewa | Mfano bado unapakua | Subiri sekunde 30–60 baada ya kuanza; mifano mikubwa huchukua muda mrefu |
| `StatusCode: 404` kwenye `/v1/health` | Bandari si sahihi | Kawaida ni `5273`. Angalia `foundry local status` kwa bandari halisi |
| Rasilimali si za kutosha | Foundry Local inahitaji takriban 4 GB RAM huru | Funga programu nyingine |
| Kupakua mfano kunashindwa | Nafasi ya diski ni ndogo | Mifano ni 2–8 GB. Futa nafasi kisha endesha `foundry model pull <name>` |

### Jina la mfano halilingani

```powershell
# Orodhesha modeli zilizopakuliwa na majina yao halisi
foundry model list
```

Weka `AZURE_AI_MODEL_DEPLOYMENT_NAME` katika `.env` kwa jina halisi kama lilivyoonyeshwa (mfano, `phi-4-mini`, si `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` wakati wa kuendesha ndani (Njia B)

Maabara ya `main.py` inatumia `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local inahitaji vigeuzi hivi kuelekeza huduma ya ndani - **sio** `AZURE_AI_PROJECT_ENDPOINT`. Hakikisha `.env` yako ina:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Zana ya MCP bado inafanya mwito wa nje (Njia B)

Hili ni la kawaida. Zana ya `search_microsoft_learn_for_plan` hupokea rasilimali za kujifunza kutoka `https://learn.microsoft.com/api/mcp`. **Ni tu utafutaji wa jina la ujuzi** unaosafiri mitanoni - wasifu na maandishi ya JD hugudwi kabisa kwenye kifaa chako na hayatumiwi. Ikiwa unahitaji uendeshaji kabisa bila mtandao, ongeza zamu ya `try/except` katika zana inayorejesha anwani thabiti ya `learn.microsoft.com` wakati kiungo hakipatikani.

---

## Kupata msaada

Ikiwa umekwama baada ya kujaribu marekebisho yaliyotajwa hapo juu:

1. **Angalia rekodi za seva** - Makosa mengi huleta mfuatano wa Python kwenye terminali. Soma mfuatano mzima.
2. **Tafuta ujumbe wa kosa** - Nakili maandishi ya kosa na tafuta katika [Microsoft Q&A kwa Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Fungua tatizo** - Weka tatizo kwenye [repo ya warsha](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) zikiwa na:
   - Ujumbe wa kosa au picha ya skrini
   - Matoleo ya pakiti zako (`pip list | Select-String "agent-framework"`)
   - Toleo lako la Python (`python --version`)
   - Ikiwa tatizo ni la ndani au baada ya kusambaza

---

### Kidhibiti cha hatua

- [ ] Unajua jinsi ya kukagua na kurekebisha masuala ya usanidi wa `.env`
- [ ] Unaweza kuthibitisha matoleo ya pakiti yanalingana na jedwali lililotakiwa
- [ ] Unajua jinsi ya kukagua rekodi za kontena kwa makosa ya usambazaji
- [ ] Unaweza kuthibitisha majukumu ya RBAC kwenye Azure Portal

---

**Ya awali:** [07 - Hakiki kwenye Playground](07-verify-in-playground.md) · **Ifuatayo:** [09 - Muhtasari →](09-summary.md) · **Nyumbani:** [Lab 02 README](../README.md) · [Nyumbani Warsha](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->