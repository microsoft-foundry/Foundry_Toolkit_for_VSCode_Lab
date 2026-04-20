# Moduli 8 - Kutatua Matatizo (Wakala Wengi)

Moduli hii inashughulikia makosa ya kawaida, marekebisho, na mikakati ya kuboresha maambukizi maalum kwa mtiririko wa kazi wa wakala wengi. Kwa matatizo ya jumla ya utoaji wa Foundry, rejelea pia [mwongozo wa kutatua matatizo wa Kiworoko 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Marejeleo ya haraka: Hitilafu → Marekebisho

| Hitilafu / Dalili | Sababu Inayowezekana | Marekebisho |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Faili la `.env` halipo au thamani hazijawekwa | Tengeneza `.env` na `PROJECT_ENDPOINT=<your-endpoint>` na `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Mazingira pepe hayajafunguliwa au utegemezi haujafungwa | Endesha `.\.venv\Scripts\Activate.ps1` kisha `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Pakiti ya MCP haijafungwa (haipo kwenye mahitaji) | Endesha `pip install mcp` au angalia kama `requirements.txt` inajumuisha kama utegemezi wa upitifu |
| Wakala huanza lakini hurudisha jibu tupu | `output_executors` haifanani au ukanda haupo | Thibitisha `output_executors=[gap_analyzer]` na ukanda wote upo katika `create_workflow()` |
| Kadi 1 tu ya pengo (zaidi hazipo) | Maelekezo ya GapAnalyzer hayakamilika | Ongeza aya ya `CRITICAL:` kwenye `GAP_ANALYZER_INSTRUCTIONS` - angalia [Moduli 3](03-configure-agents.md) |
| Alama ya kufaa ni 0 au haipo | MatchingAgent hakupokea data ya juu | Thibitisha `add_edge(resume_parser, matching_agent)` na `add_edge(jd_agent, matching_agent)` zipo |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Seva ya MCP iliyakataza simu ya chombo | Angalia muunganisho wa mtandao. Jaribu kufungua `https://learn.microsoft.com/api/mcp` kwenye kivinjari. Jaribu tena |
| Hakuna anuani za Microsoft Learn kwenye matokeo | Chombo cha MCP hakijasajiliwa au mwisho si sahihi | Thibitisha `tools=[search_microsoft_learn_for_plan]` kwenye GapAnalyzer na `MICROSOFT_LEARN_MCP_ENDPOINT` ni sahihi |
| `Address already in use: port 8088` | Mchakato mwingine unatumia bandari 8088 | Endesha `netstat -ano \| findstr :8088` (Windows) au `lsof -i :8088` (macOS/Linux) na zuia mchakato unaopingana |
| `Address already in use: port 5679` | Mgongano wa bandari ya Debugpy | Zuia vikao vingine vya urekebishaji. Endesha `netstat -ano \| findstr :5679` kutambua na kuua mchakato |
| Jinsia Mhakiki haifunguki | Seva haijaanza kikamilifu au mgongano wa bandari | Subiri kumbukumbu ya "Server running". Angalia bandari 5679 ni huru |
| `azure.identity.CredentialUnavailableError` | Hujasaini ndani ya CLI ya Azure | Endesha `az login` kisha anza tena seva |
| `azure.core.exceptions.ResourceNotFoundError` | Uwekaji mfano haupo | Angalia `MODEL_DEPLOYMENT_NAME` inalingana na mfano uliowekwa kwenye mradi wako wa Foundry |
| Hali ya kontena "Imeshindwa" baada ya utoaji | Kontena imeshindwa kuanzisha | Angalia kumbukumbu za kontena upande wa Foundry. Mara nyingi: env var haipo au kosa la kuingiza |
| Utoaji unaonyesha "Inangojea" kwa zaidi ya dakika 5 | Kontena inachukua muda mrefu kuanzisha au mipaka ya rasilimali | Subiri hadi dakika 5 kwa wakala wengi (huwatengeneza wakala 4). Ikiwa bado inangojea, angalia kumbukumbu |
| `ValueError` kutoka `WorkflowBuilder` | Mpangilio wa mchoro si sahihi | Hakikisha `start_executor` imewekwa, `output_executors` ni orodha, na hakuna ukanda wa mduara |

---

## Masuala ya mazingira na usanidi

### Thamani za `.env` zinazokosekana au zisizo sahihi

Faili la `.env` lazima likuwe katika saraka ya `PersonalCareerCopilot/` (kielekezi sawa na `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Yaliyotarajiwa kwenye `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Kupata PROJECT_ENDPOINT yako:**  
- Fungua upande wa **Microsoft Foundry** katika VS Code → bonyeza kulia mradi wako → **Copy Project Endpoint**.  
- Au nenda kwenye [Azure Portal](https://portal.azure.com) → mradi wako wa Foundry → **Overview** → **Project endpoint**.

> **Kupata MODEL_DEPLOYMENT_NAME yako:** Katika rubani ya Foundry, panua mradi wako → **Models** → tafuta jina la mfano uliowekwa (mfano, `gpt-4.1-mini`).

### Umuhimu wa env var

`main.py` kutumia `load_dotenv(override=False)`, maana yake:

| Kipaumbele | Chanzo | Hushinda wakati vyote vinawekwa? |
|------------|--------|----------------------------------|
| 1 (juu kabisa) | Hali ya shell | Ndiyo |
| 2 | Faili `.env` | Iwapo hali ya shell haijawaweka |

Hii ina maana vari za mazingira za Foundry runtime (zilizo kwenye `agent.yaml`) zina kipaumbele juu ya thamani za `.env` wakati wa utoaji uliohifadhiwa.

---

## Mduara wa toleo

### Msururu wa toleo la pakiti

Mtiririko wa wakala wengi unahitaji matoleo maalum ya pakiti. Toleo lisilolingana husababisha makosa wakati wa utekelezaji.

| Pakiti | Toleo Linalohitajika | Amri ya Kukagua |
|--------|---------------------|-----------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | toleo la kabla ya mwisho | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Makosa ya kawaida ya toleo

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Rekebisha: sasisha hadi rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` haipatikani au Inspector haifanyi kazi:**

```powershell
# Rekebisha: sakinisha kwa bendera ya --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Rekebisha: boresha kifurushi cha mcp
pip install mcp --upgrade
```

### Thibitisha matoleo yote mara moja

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Matokeo yanayotarajiwa:

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

## Masuala ya zana ya MCP

### Zana ya MCP hairudishi matokeo

**Dalili:** Kadi za pengo zinaonyesha "No results returned from Microsoft Learn MCP" au "No direct Microsoft Learn results found".

**Sababu zinazowezekana:**

1. **Tatizo la mtandao** - Mwisho wa MCP (`https://learn.microsoft.com/api/mcp`) haupatikani.
   ```powershell
   # Jaribu muunganisho
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Ikiwa hii irudisha `200`, mwisho upo mtandao.

2. **Ugonjwa wa swali maalum mno** - Jina la ujuzi ni dhaifu sana kwa utafutaji wa Microsoft Learn.  
   - Hii ni kawaida kwa ujuzi maalum sana. Chombo kina URL ya zana mbadala kwenye majibu.

3. **Vipindi vya MCP vimekatika** - Muunganisho wa HTTP wa Streamable umekwisha muda.
   - Jaribu tena ombi. Vipindi vya MCP ni virefu na vinaweza kuhitaji muunganisho mpya.

### Maelezo ya kumbukumbu za MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Kumbukumbu | Maana | Hatua |
|------------|--------|-------|
| `GET → 405` | MCP mteja anajaribu wakati wa kuanzisha | Zaidi - puuza |
| `POST → 200` | Simu ya zana imefanikiwa | Inatarajiwa |
| `DELETE → 405` | MCP mteja anajaribu wakati wa usafishaji | Zaidi - puuza |
| `POST → 400` | Ombi la mbaya (swali lililoandikwa vibaya) | Angalia kigezo cha `query` katika `search_microsoft_learn_for_plan()` |
| `POST → 429` | Mipaka ya kiwango | Subiri na jaribu tena. Punguza kigezo cha `max_results` |
| `POST → 500` | Kosa la seva ya MCP | La muda mfupi - jaribu tena. Ikiwa inakaa, API ya Microsoft Learn MCP inaweza kuwa imezimwa |
| Muda wa muunganisho umepita | Tatizo la mtandao au seva ya MCP haipo | Angalia mtandao. Jaribu `curl https://learn.microsoft.com/api/mcp` |

---

## Masuala ya utoaji

### Kontena haianzi baada ya utoaji

1. **Angalia kumbukumbu za kontena:**  
   - Fungua upande wa **Microsoft Foundry** → panua **Hosted Agents (Preview)** → bonyeza wakala wako → panua toleo → **Container Details** → **Logs**.  
   - Tafuta alama za Python au makosa ya moduli isiyopatikana.

2. **Sababu za kawaida za kushindwa kuanzisha kontena:**

   | Kosa kwenye kumbukumbu | Sababu | Marekebisho |
   |------------------------|---------|-------------|
   | `ModuleNotFoundError` | `requirements.txt` haijajumuisha pakiti | Ongeza pakiti, toa tena |
   | `RuntimeError: Missing required environment variable` | env vars za `agent.yaml` hazijawekwa | Sasisha sehemu ya `environment_variables` kwenye `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity haijasanidiwa | Foundry hujitoa moja kwa moja - hakikisha unatoa kupitia upanuzi |
   | `OSError: port 8088 already in use` | Dockerfile inaonesha bandari isiyo sahihi au mgongano wa bandari | Thibitisha `EXPOSE 8088` katika Dockerfile na `CMD ["python", "main.py"]` |
   | Kontena imetoka na msimbo 1 | Kosa lisilotibiwa ndani kazi ya `main()` | Jaribu ndani ya eneo la ndani kwanza ([Moduli 5](05-test-locally.md)) ili kugundua makosa kabla ya kutoa |

3. **Toa tena baada ya kurekebisha:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → chagua wakala uleule → toa toleo jipya.

### Utoaji unachukua muda mrefu

Makontena ya wakala wengi huchukua muda zaidi kuanza kwa sababu hutengeneza mawakala 4 wakati wa kuanzisha. Muda wa kuanzisha wa kawaida:

| Hatua | Muda Unaotarajiwa |
|-------|------------------|
| Kujenga picha ya kontena | Dakika 1-3 |
| Kutuma picha kwa ACR | Sekunde 30-60 |
| Kuanzisha kontena (wakala mmoja) | Sekunde 15-30 |
| Kuanzisha kontena (wakala wengi) | Sekunde 30-120 |
| Wakala upatikana kwenye Playground | Dakika 1-2 baada ya "Started" |

> Ikiwa hali ya "Pending" inaendelea zaidi ya dakika 5, angalia kumbukumbu za kontena kwa makosa.

---

## Masuala ya RBAC na ruhusa

### `403 Forbidden` au `AuthorizationFailed`

Unahitaji jukumu la **[Mtumiaji wa Azure AI](https://aka.ms/foundry-ext-project-role)** kwenye mradi wako wa Foundry:

1. Nenda kwenye [Azure Portal](https://portal.azure.com) → rasilimali ya **mradi** wa Foundry wako.  
2. Bonyeza **Access control (IAM)** → **Role assignments**.  
3. Tafuta jina lako → thibitisha **Azure AI User** ipo kwenye orodha.  
4. Ikiwa haipo: **Ongeza** → **Add role assignment** → tafuta **Azure AI User** → mpa akaunti yako.

Angalia hati ya [RBAC kwa Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) kwa maelezo zaidi.

### Uwekaji mfano haupatikani

Ikiwa wakala anarejesha makosa yanayohusiana na mfano:

1. Thibitisha mfano umezinduliwa: Rubani wa Foundry → panua mradi → **Models** → angalia `gpt-4.1-mini` (au mfano wako) na hali ni **Succeeded**.  
2. Thibitisha jina la uwekaji linalingana: linganisha `MODEL_DEPLOYMENT_NAME` kwenye `.env` (au `agent.yaml`) na jina halisi la uwekaji kwenye rubani.  
3. Ikiwa uwekaji umekwisha muda (daraja la bure): toa tena kutoka [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Maswala ya Agent Inspector

### Inspector hufunguka lakini inaonyesha "Disconnected"

1. Thibitisha seva inakimbia: angalia "Server running on http://localhost:8088" kwenye terminal.  
2. Angalia bandari `5679`: Inspector huunganishwa kupitia debugpy kwenye bandari 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Washa tena seva na fungua Inspector tena.

### Inspector inaonyesha jibu la sehemu

Majibu kutoka kwa wakala wengi huwa marefu na hutiririka kwa sehemu. Subiri jibu kamili kukamilika (inaweza kuchukua sekunde 30-60 kulingana na idadi ya kadi za pengo na simu za zana ya MCP).

Ikiwa jibu huharibika mara kwa mara:  
- Hakikisha maelekezo ya GapAnalyzer yana kipengele cha `CRITICAL:` kinachozuia kuunganisha kadi za pengo.  
- Kagua kikomo cha token cha mfano wako - `gpt-4.1-mini` inaunga mkono hadi token 32K zilizotolewa, ambazo zinapaswa kutosha.

---

## Vidokezo vya utendaji

### Majibu polepole

Mtiririko wa kazi wa wakala wengi ni polepole zaidi ikilinganishwa na wakala mmoja kwa sababu ya utegemezi wa mfuatano na simu za zana za MCP.

| Uboreshaji | Jinsi | Athari |
|------------|-------|--------|
| Punguza simu za MCP | Punguza kigezo cha `max_results` kwenye zana | Kuruhusu mizunguko michache ya HTTP |
| Fupisha maelekezo | Maelekezo mafupi na yenye malengo kwa wakala | Upelekaji wa LLM kwa haraka |
| Tumia `gpt-4.1-mini` | Kasi zaidi kuliko `gpt-4.1` kwa maendeleo | Kuboresha kasi kwa karibu mara 2 |
| Punguza maelezo ya kadi ya pengo | Rahisisha muundo wa kadi ya pengo katika maelekezo ya GapAnalyzer | Matokeo kidogo ya kuzalisha |

### Muda wa majibu kawaida (mkoa wa ndani)

| Usanidi | Muda Unaotarajiwa |
|---------|-------------------|
| `gpt-4.1-mini`, kadi 3-5 za pengo | Sekunde 30-60 |
| `gpt-4.1-mini`, kadi 8+ za pengo | Sekunde 60-120 |
| `gpt-4.1`, kadi 3-5 za pengo | Sekunde 60-120 |
---

## Kupata msaada

Ikiwa umekwama baada ya kujaribu marekebisho yaliyo hapo juu:

1. **Angalia kumbukumbu za seva** - Makosa mengi huleta mstari wa mfuatano wa Python kwenye terminali. Soma mfuatano wote wa makosa.
2. **Tafuta ujumbe wa kosa** - Nakili maandishi ya kosa na utafute katika [Microsoft Q&A kwa Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Fungua tatizo** - Weka tatizo kwenye [hifadhidata ya warsha](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) na:
   - Ujumbe wa kosa au picha ya skrini
   - Toleo la vifurushi vyako (`pip list | Select-String "agent-framework"`)
   - Toleo lako la Python (`python --version`)
   - Ikiwa tatizo ni la ndani au baada ya usambazaji

---

### Alama ya uhakiki

- [ ] Unaweza kubaini na kurekebisha makosa ya kawaida ya maajenti wengi kwa kutumia jedwali la marejeleo ya haraka
- [ ] Unajua jinsi ya kuangalia na kurekebisha matatizo ya usanidi wa `.env`
- [ ] Unaweza kuhakiki toleo la vifurushi linakutana na jedwali la mahitaji
- [ ] Unaelewa makala za kumbukumbu za MCP na unaweza kuchunguza kushindwa kwa zana
- [ ] Unajua jinsi ya kuangalia kumbukumbu za kontena kwa kushindwa kwa usambazaji
- [ ] Unaweza kuhakiki majukumu ya RBAC katika Azure Portal

---

**Iliyopita:** [07 - Thibitisha katika Playground](07-verify-in-playground.md) · **Mwanzo:** [Lab 02 README](../README.md) · [Mwanzo wa Warsha](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kanikumka**:  
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kwa usahihi, tafadhali fahamu kuwa tafsiri za kiotomatiki zinaweza kuwa na makosa au upotoshaji. Hati ya asili katika lugha yake ya asili inapaswa kuchukuliwa kama chanzo halali. Kwa taarifa muhimu, tafsiri ya kitaalamu ya binadamu inapendekezwa. Hatuwajibiki kwa kutoelewana au tafsiri potofu zinazotokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->