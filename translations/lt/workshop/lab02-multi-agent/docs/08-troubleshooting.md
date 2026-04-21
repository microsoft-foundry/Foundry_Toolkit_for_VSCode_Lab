# Modulis 8 - Gedimų šalinimas (Multi-agentų)

Šis modulis apima įprastas klaidas, pataisas ir derinimo strategijas, specifines daugiaagentių darbo eigų atvejams. Bendrų Foundry diegimo problemų atvejais taip pat žr. [Laboratorija 01 gedimų šalinimo vadovą](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Greita nuoroda: Klaida → Ši klaida ištaisoma taip

| Klaida / Simptomas | Tikėtina priežastis | Pataisa |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Trūksta `.env` failo arba reikšmės nėra nustatytos | Sukurkite `.env` su `PROJECT_ENDPOINT=<jūsų-endpoint>` ir `MODEL_DEPLOYMENT_NAME=<jūsų-modelis>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuali aplinka nėra aktyvuota arba priklausomybės neįdiegtos | Vykdykite `.\.venv\Scripts\Activate.ps1`, tada `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP paketas neįdiegtas (trūksta reikalavimuose) | Vykdykite `pip install mcp` arba patikrinkite, ar `requirements.txt` įtraukia jį kaip pereinamą priklausomybę |
| Agentas paleidžiamas, tačiau grąžina tuščią atsakymą | `output_executors` neatitinka arba trūksta ryšių | Patikrinkite, kad `output_executors=[gap_analyzer]` ir visi ryšiai yra `create_workflow()` |
| Tik 1 gap kortelė (likusios trūksta) | GapAnalyzer nurodymai nebaigti | Pridėkite `CRITICAL:` paragrafą prie `GAP_ANALYZER_INSTRUCTIONS` - žr. [Modulis 3](03-configure-agents.md) |
| Fit rezultatas yra 0 arba neegzistuoja | MatchingAgent negavo įvesties iš aukštesnio lygmens | Patikrinkite, ar egzistuoja `add_edge(resume_parser, matching_agent)` ir `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP serveris atmetė įrankio kvietimą | Patikrinkite interneto ryšį. Bandykite atidaryti `https://learn.microsoft.com/api/mcp` naršyklėje. Bandykite dar kartą |
| Rezultatuose nėra Microsoft Learn URL | MCP įrankis neregistruotas arba neteisingas endpoint | Patikrinkite, ar `tools=[search_microsoft_learn_for_plan]` GapAnalyzer ir `MICROSOFT_LEARN_MCP_ENDPOINT` yra teisingi |
| `Address already in use: port 8088` | Kitas procesas naudoja 8088 prievadą | Vykdykite `netstat -ano \| findstr :8088` (Windows) arba `lsof -i :8088` (macOS/Linux) ir sustabdykite konfliktuojantį procesą |
| `Address already in use: port 5679` | Debugpy uosto konfliktas | Sustabdykite kitas derinimo sesijas. Vykdykite `netstat -ano \| findstr :5679` ir užmuškite procesą |
| Agent Inspector neatsidaro | Serveris nevisiškai paleistas arba uosto konfliktas | Palaukite iki "Server running" žurnalo. Patikrinkite, ar uostas 5679 laisvas |
| `azure.identity.CredentialUnavailableError` | Neprisijungta prie Azure CLI | Vykdykite `az login` ir paleiskite serverį iš naujo |
| `azure.core.exceptions.ResourceNotFoundError` | Modelio diegimas neegzistuoja | Patikrinkite, ar `MODEL_DEPLOYMENT_NAME` atitinka diegtą modelį jūsų Foundry projekte |
| Konteinerio būsena "Failed" po diegimo | Konteinerio gedimas paleidimo metu | Peržiūrėkite konteinerio žurnalus Foundry šoninėje juostoje. Dažnas atvejis: trūksta aplinkos kintamojo arba importo klaida |
| Diegimas rodo "Pending" > 5 minučių | Konteinerio paleidimas užtrunka arba yra resursų ribojimai | Palaukite iki 5 minučių daugiaagentėms (kuriamos 4 agentų instancijos). Jei vis dar laukiate, patikrinkite žurnalus |
| `ValueError` iš `WorkflowBuilder` | Neteisinga grafiko konfigūracija | Užtikrinkite, kad `start_executor` yra nustatytas, `output_executors` yra sąrašas, ir nėra ciklinių ryšių |

---

## Aplinkos ir konfigūracijos problemos

### Trūksta arba neteisingi `.env` reikšmės

`.env` failas turi būti `PersonalCareerCopilot/` kataloge (toje pačioje vietoje kaip `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Tikėtinas `.env` turinys:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Kur rasti PROJECT_ENDPOINT:**  
- Atidarykite **Microsoft Foundry** šoninę juostą VS Code → dešiniu pelės klavišu paspauskite jūsų projektą → **Copy Project Endpoint**.  
- Arba eikite į [Azure Portal](https://portal.azure.com) → jūsų Foundry projektą → **Overview** → **Project endpoint**.

> **Kur rasti MODEL_DEPLOYMENT_NAME:** Foundry šoninėje juostoje išplėskite projektą → **Models** → raskite savo diegtą modelio pavadinimą (pvz., `gpt-4.1-mini`).

### Aplinkos kintamųjų prioritetas

`main.py` naudoja `load_dotenv(override=False)`, tai reiškia:

| Prioritetas | Šaltinis | Laimi, jei abu nustatyti? |
|----------|--------|------------------------|
| 1 (aukščiausias) | Terminalo aplinkos kintamasis | Taip |
| 2 | `.env` failas | Tik jei terminalo kintamasis nenustatytas |

Tai reiškia, kad Foundry vykdymo aplinkos kintamieji (`agent.yaml` nustatyti) viršija `.env` reikšmes talpinamame diegime.

---

## Versijų suderinamumas

### Paketų versijų matrica

Daugiaagentinė darbo eiga reikalauja konkrečių paketo versijų. Nesuderintos versijos sukelia vykdymo klaidas.

| Paketas | Reikalinga versija | Tikrinimo komanda |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | naujausia priešpaskutinė | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Dažnos versijų klaidos

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Pataisyti: atnaujinti į rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nerastas arba Inspector nesuderinamas:**

```powershell
# Pataisymas: diegimas naudojant --pre vėliavą
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Ištaisyta: atnaujinti mcp paketą
pip install mcp --upgrade
```

### Patikrinkite visas versijas vienu metu

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Tikėtinas rezultatas:

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

## MCP įrankio problemos

### MCP įrankis negrąžina rezultatų

**Simptomas:** Gap kortelės rodo "No results returned from Microsoft Learn MCP" arba "No direct Microsoft Learn results found".

**Galimos priežastys:**

1. **Tinklo problema** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) nepasiekiamas.
   ```powershell
   # Patikrinti ryšį
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
 Jei čia grąžina `200`, endpoint yra pasiekiamas.

2. **Užklausa per daug specifinė** - Įgūdžių pavadinimas per siauras Microsoft Learn paieškai.
   - Tai įprasta labai specializuotiems įgūdžiams. Įrankis turi rezervo URL atsakyme.

3. **MCP sesijos laiko limitas baigtas** - Streamable HTTP ryšys nutrūko.
   - Bandykite dar kartą. MCP sesijos yra laikinos ir reikalauja pakartotinio prisijungimo.

### MCP žurnalų aiškinimas

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Žurnalas | Prasmė | Veiksmas |
|-----|---------|--------|
| `GET → 405` | MCP klientas tikrina inicializacijos metu | Normalu - ignoruokite |
| `POST → 200` | Įrankio kvietimas sėkmingas | Laukiama |
| `DELETE → 405` | MCP klientas tikrina valymo metu | Normalu - ignoruokite |
| `POST → 400` | Bloga užklausa (neteisinga užklausa) | Patikrinkite `query` parametrą `search_microsoft_learn_for_plan()` |
| `POST → 429` | Ribojami kvietimai | Palaukite ir bandykite vėl. Sumažinkite `max_results` parametrą |
| `POST → 500` | MCP serverio klaida | Laikina - bandykite dar kartą. Jei tęsiama, Microsoft Learn MCP API gali būti neprieinamas |
| Laikino ryšio klaida | Tinklo problema arba MCP serveris neprieinamas | Patikrinkite internetą. Bandykite `curl https://learn.microsoft.com/api/mcp` |

---

## Diegimo problemos

### Konteineris nepaleidžiamas po diegimo

1. **Patikrinkite konteinerio žurnalus:**
   - Atidarykite **Microsoft Foundry** šoninę juostą → išplėskite **Hosted Agents (Preview)** → spustelėkite savo agentą → išplėskite versiją → **Container Details** → **Logs**.
   - Ieškokite Python klaidų arba trūkstamų modulių klaidų.

2. **Dažniausios konteinerio paleidimo klaidos:**

   | Klaida žurnale | Priežastis | Pataisa |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` trūksta paketo | Pridėkite paketą, diegkite iš naujo |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` aplinkos kintamieji nenurodyti | Atnaujinkite `agent.yaml` → `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | Nesuveikė Managed Identity | Foundry nustato automatiškai - įsitikinkite, kad diegiate per plėtinį |
   | `OSError: port 8088 already in use` | Dockerfile nurodo netinkamą prievadą arba prievadų konfliktas | Patikrinkite `EXPOSE 8088` Dockerfile ir `CMD ["python", "main.py"]` |
   | Konteineris baigiasi su kodu 1 | Nepagaunama išimtis `main()` | Išbandykite vietoje pirmiausia ([Modulis 5](05-test-locally.md)) prieš diegiant |

3. **Diekite iš naujo po pataisų:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → pasirinkite tą patį agentą → įdiekite naują versiją.

### Diegimas trunka per ilgai

Daugiaagentiniai konteineriai paleidžiami ilgiau, nes kuriamos 4 agentų instancijos paleidimo metu. Įprasti paleidimo laikai:

| Etapas | Tikėtinas laikas |
|-------|------------------|
| Konteinerio vaizdo kūrimas | 1-3 minutės |
| Vaizdo įkėlimas į ACR | 30-60 sekundžių |
| Konteinerio paleidimas (vienas agentas) | 15-30 sekundžių |
| Konteinerio paleidimas (daugiaagentis) | 30-120 sekundžių |
| Agentas pasiekiamas paleidimo aikštelėje | 1-2 minutės po "Started" |

> Jei būsena "Pending" išlieka ilgiau nei 5 minutes, patikrinkite konteinerio žurnalus klaidoms.

---

## RBAC ir leidimų problemos

### `403 Forbidden` arba `AuthorizationFailed`

Jums reikalinga **[Azure AI User](https://aka.ms/foundry-ext-project-role)** rolė jūsų Foundry projekte:

1. Eikite į [Azure Portal](https://portal.azure.com) → savo Foundry **projekto** resursą.
2. Spustelėkite **Access control (IAM)** → **Role assignments**.
3. Ieškokite savo vardo → patikrinkite, ar yra **Azure AI User**.
4. Jei nėra: spustelėkite **Add** → **Add role assignment** → ieškokite **Azure AI User** → priskirkite savo paskyrai.

Daugiau informacijos rasite [RBAC Microsoft Foundry dokumentacijoje](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Modelio diegimas neprieinamas

Jei agentas grąžina modelio klaidas:

1. Įsitikinkite, kad modelis yra diegtas: Foundry šoninėje juostoje išplėskite projektą → **Models** → patikrinkite, ar `gpt-4.1-mini` (ar jūsų modelis) turi statusą **Succeeded**.
2. Patikrinkite, ar diegimo pavadinimas atitinka: palyginkite `MODEL_DEPLOYMENT_NAME` `.env` (arba `agent.yaml`) su faktiniu pavadinimu šoninėje juostoje.
3. Jei diegimas pasibaigė (nemokamas sluoksnis): atnaujinkite diegimą iš [Modelių katalogo](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector problemos

### Inspector atsidaro, bet rodo "Disconnected"

1. Patikrinkite, ar serveris veikia: terminale ieškokite pranešimo "Server running on http://localhost:8088".
2. Patikrinkite uostą `5679`: Inspector jungiasi per debugpy per uostą 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Paleiskite serverį iš naujo ir dar kartą atidarykite Inspector.

### Inspector rodo dalinį atsakymą

Daugiaagentiniai atsakymai yra ilgi ir srautiniai, jie pateikiami palaipsniui. Palaukite, kol visas atsakymas bus baigtas (tai gali užtrukti 30-60 sekundžių, priklausomai nuo gap kortelių skaičiaus ir MCP įrankių kvietimų).

Jei atsakymas nuolat trūksta:
- Patikrinkite, ar GapAnalyzer nurodymuose yra `CRITICAL:` blokas, neleidžiantis kombinuoti gap kortelių.
- Patikrinkite savo modelio tokenų limitą - `gpt-4.1-mini` palaiko iki 32K išvesties tokenų, tai turėtų būti pakankama.

---

## Veikimo patarimai

### Lėtas atsakas

Daugiaagentiniai darbo procesai yra lėtesni nei vieno agente, dėl nuoseklių priklausomybių ir MCP įrankių kvietimų.

| Optimizavimas | Kaip | Efektas |
|-------------|-----|--------|
| Sumažinkite MCP kvietimų skaičių | Sumažinkite `max_results` parametrą įrankyje | Mažiau HTTP užklausų |
| Supaprastinkite nurodymus | Trumpesni, labiau fokusuoti agento prašymai | Greitesnis LLM apdorojimas |
| Naudokite `gpt-4.1-mini` | Greitesnis už `gpt-4.1` kūrimui | Apie 2 kartus greičiau |
| Sumažinkite gap kortelės detalumą | Supaprastinkite gap kortelės formatą GapAnalyzer nurodymuose | Mažiau generuojamo turinio |

### Tipiniai atsako laikai (vietiniai)

| Konfigūracija | Laukiama trukmė |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap kortelės | 30-60 sekundžių |
| `gpt-4.1-mini`, 8+ gap kortelės | 60-120 sekundžių |
| `gpt-4.1`, 3-5 gap kortelės | 60-120 sekundžių |
---

## Pagalbos gavimas

Jei užstrigote po bandymų ištaisyti klaidas aukščiau:

1. **Patikrinkite serverio žurnalus** – Dauguma klaidų terminale pateikia Python steko seką. Perskaitykite visą steko seką.
2. **Ieškokite klaidos pranešimo** – Nukopijuokite klaidos tekstą ir ieškokite [Microsoft Q&A apie Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Atidarykite problemos pranešimą** – Užregistruokite problemą [workshop repozitorijoje](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) su:
   - Klaidos pranešimu arba ekrano kopija
   - Jūsų paketų versijomis (`pip list | Select-String "agent-framework"`)
   - Jūsų Python versija (`python --version`)
   - Ar problema yra vietinė ar po diegimo

---

### Kontrolinis punktas

- [ ] Galite identifikuoti ir ištaisyti dažniausias kelių agentų klaidas naudodami greitosios nuorodos lentelę
- [ ] Žinote, kaip patikrinti ir ištaisyti `.env` konfigūracijos problemas
- [ ] Galite patikrinti, ar paketų versijos atitinka reikalaujamą matricą
- [ ] Suprantate MCP žurnalų įrašus ir galite diagnozuoti įrankių klaidas
- [ ] Žinote, kaip patikrinti konteinerio žurnalus dėl diegimo klaidų
- [ ] Galite patikrinti RBAC rolės Azure portale

---

**Ankstesnis:** [07 - Patikrinimas Playground](07-verify-in-playground.md) · **Pradžia:** [Lab 02 README](../README.md) · [Darbo suvestinė](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:  
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors stengiamės užtikrinti tikslumą, atkreipkite dėmesį, kad automatizuoti vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas gimtąja kalba turi būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojamas profesionalus žmogaus vertimas. Mes neatsakome už bet kokius nesusipratimus ar klaidingus interpretavimus, kilusius naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->