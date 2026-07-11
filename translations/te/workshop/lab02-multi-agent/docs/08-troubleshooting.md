# మాడ్యూల్ 8 - సమస్య పరిష్కారం

ఈ మాడ్యూల్ మల్టీ ఏజెంట్ వర్క్‌ఫ్లోకి ప్రత్యేకమైన సాధారణ లోపాలు, పరిష్కారాలు మరియు డీబగ్గింగ్ వ్యూహాలను కవర్ చేస్తుంది.

## ఏజెంట్ అవుట్‌పుట్ సమస్యలు

### GapAnalyzer “నేను ఇంకా సరిసాటి నివేదిక కలిగి లేను” అనుగుంటుంది

**లక్షణం:** GapAnalyzer స్పందన “మిస్సింగ్ స్కిల్స్” మరియు “సర్టిఫికేషన్ గ్యాప్స్” ఉన్న ఒక సరిపోయే నివేదిక పేస్ట్ చేయమని అడుగుతుంది. మీరు రెండింటినీ - రిజ్యూమ్ మరియు ఉద్యోగ వివరణ - పంపినప్పటికీ ఇది జరుగుతుంది.

**కారణం:** JD Agent కు JD పాఠ్యం డౌన్‌స్ట్రీమ్‌కు పంపబడలేదు. `context_mode="last_agent"` తో `resume_executor` మాత్రమే యూజర్ యొక్క అసలు సందేశాన్ని చూస్తుంది. `RESUME_PARSER_INSTRUCTIONS` దాని అవుట్‌పుట్‌లో JD పాఠ్యం చేర్చకపోతే, JD Agent కు पार్స్ చేయడానికి JD ఉంటుంది కాదని, MatchingAgent ఫిట్ స్కోర్ ను లెక్కించలేడు, మరియు GapAnalyzer కు అర్థరహిత ఇన్పుట్ అందుతుంది.

**నిర్ధారణ:**

సర్వర్ లాగ్లలో MatchingAgent స్పాన్ కోసం చూడండి. ఇది ఉంటే:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
పాస్-త్రూజ్ లేకపోవటం లేదా చల్లబడటం జరుగుతుంది.

**పరిష్కారం:** `main.py` యందు `RESUME_PARSER_INSTRUCTIONS` లో `[JOB DESCRIPTION PASS-THROUGH]` సెక్షన్ మరియు క్రింది నియమం ఉందని నిర్ధారించుకోండి:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
అలాగే `JOB_DESCRIPTION_INSTRUCTIONS` లో `[PARSED RESUME PASS-THROUGH]` రీలే నియమం ఉందని నిర్ధారించుకోండి:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
స్కాఫోల్డ్ విజార్ నుండి ఏదైనా ఇన్‌స్ట్రక్షన్ బ్లాక్ ఒక స్టబ్ అయితే, దానిని [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) నుండి సంపూర్న సంస్కరణతో మార్చండి.

### MatchingAgent “Cannot compute fit score - no JD provided” అని అవుట్‌పుట్ చేస్తుంది

ఇది పై కారణమే. MatchingAgent JD Agent యొక్క అవుట్‌పుట్ స్వీకరించింది కానీ `[PARSED RESUME PASS-THROUGH]` సెక్షన్ దొరకలేదు లేదా ఖాళీగా ఉండడంతో రెండు ప్రొఫైల్స్ పోల్చలేకపోయింది. నిర్ధారించుకోండి:
1. `JOB_DESCRIPTION_INSTRUCTIONS` లో రీలే నియమం ఉంది: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` ఏజెంట్ కు `[JD REQUIREMENTS]` మరియు `[PARSED RESUME PASS-THROUGH]` సెక్షన్లు కోసం చూస్తున్నట్లు చెప్పబడింది.

ఇరువురు ఇన్‌స్ట్రక్షన్ బ్లాక్స్‌ని [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) నుండి సంపూర్ణ సంస్కరణలతో మార్చండి.

### స్పందన రెండు సార్లు కనిపిస్తుంది

**లక్షణం:** GapAnalyzer అవుట్‌పుట్ (లేదా మొత్తం పైప్‌లైన్ అవుట్‌పుట్) ఏజెంట్ ఇన్‌స్పెక్టర్ స్పందనలో రెండు సార్లు కనిపిస్తుంది.

**కారణం:** `WorkflowBuilder` ఇన్కమింగ్ ఎడ్జ్లకు OR-అర్థాన్ని ఉపయోగిస్తుంది - డౌన్‌స్ట్రీమ్ ఎగ్జిక్యూటర్ ఏదైనా ముందస్తు ప్రాసెస్ పూర్తయిన తర్వాత ఫైర్ అవుతుంది. `matching_executor` రెండు ఇన్కమింగ్ ఎడ్జ్‌లు కలిగి ఉంటే (ఒకటి `resume_executor` నుండి మరియు ఒకటి `jd_executor` నుండి), ఇది రెండుసార్లు ఫైర్ అవుతుంది: ఒకసారి ResumeParser ముగిసినప్పుడు మరియు మరొకసారి JD Agent ముగిసినప్పుడు. GapAnalyzer కూడా రెండు సార్లు నడుస్తుంది.

**పరిష్కారం:** `WorkflowBuilder` గ్రాఫ్ కఠినంగా వరుస పైప్‌లైన్ గా ఉండేలా మరియు ఫ్యాన్- ఇన్ లేకుండా చూడండి:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # రిజ్యూమ్ ఎగ్జిక్యూటర్ నుండి కాదు
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

మీరు ఎక్కడైనా `.add_edge(resume_executor, matching_executor)` లైన్ ఉంటే, దాన్ని తీసేయండి. JD Agent అవుట్‌పుట్ నుండి `[PARSED RESUME PASS-THROUGH]` రీలే ఇప్పటికే MatchingAgent కు రిజ్యూమ్ యాక్సెస్ ఇస్తుంది.

---

## పరిసరాలు మరియు కాన్ఫిగరేషన్ సమస్యలు

### మిస్సింగ్ లేదా తప్పు `.env` విలువలు

`.env` ఫైల్ `PersonalCareerCopilot/` డైరెక్టరీలో ఉండాలి (అటువంటి స్థాయిలో `main.py` లాగా):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

అంచనా `.env` కంటెంట్:

**పాత్ ఎ - Foundry క్లౌడ్:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**పాత్ బి - Foundry లోకల్:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> రెండూ `FOUNDRY_PROJECT_ENDPOINT` వాడతాయి. విలువ భిన్నమే: క్లౌడ్ `https://` Foundry ఎండ్‌పాయింట్ వాడుతుంది; లోకల్ `http://localhost:5273/v1` వాడుతుంది. పాత్ బి కోసం ఖచ్చితమైన మodel అలియాస్ తెలుసుకోవడానికి `foundry model list` నడిపించండి.

> **మీ `FOUNDRY_PROJECT_ENDPOINT` ఎలా గుర్తించాలి:**
- VS Code లో **Foundry Toolkit** సైడ్‌బార్ తెరవండి → మీ ప్రాజెక్ట్ పై రైట్ క్లిక్ → **Copy Project Endpoint**.
- లేదా [Azure Portal](https://portal.azure.com) → మీ Foundry ప్రాజెక్ట్ → **Overview** → **Project endpoint**.

> **మీ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ఎలా కనుగొనాలి:** Foundry Toolkit sidebar లో మీ ప్రాజెక్ట్ విస్తరించండి → **Models** → మీ డిప్లాయ్ అయిన మోడల్ పేరు కనుగొనండి (ఉదా. `gpt-4.1-mini`).

### Env var ప్రాధాన్యత

`main.py` లో `load_dotenv(override=True)` వాడతారు, దీని అర్థం:

| ప్రాధాన్యత | మూలం | ఇద్దరూ సెట్ చేసినపుడు ఏది గెలుస్తుంది? |
|----------|--------|------------------------|
| 1 (అత్యధిక) | `.env` ఫైల్ | అవును |
| 2 | షెల్ / కంటైనర్ ఎన్విరాన్‌మెంట్ వేరియబుల్ | అదే కీ `.env` లో లేదంటే వాడుతుంది |

లోకల్ డెవలప్మెంట్‌లో, ఇది `.env` ని నిజ స్రోతస్గా చేస్తుంది (`.env` ను ఎడిట్ చేయగానే నడుపుతుండటానికి ప్రభావితం చేస్తుంది). హోస్టెడ్ డిప్లాయ్మెంట్‌లో, Foundry కంటైనర్ స్థాయిలో ఎన్విరాన్‌మెంట్ వేరియబుల్స్ ఇంజెక్ట్ చేస్తుంది; ఈ ల్యాబ్ సెటప్ కోసం `.env` కలిగి ఉండకపోవడంతో, ఇంజెక్ట్ చేసిన కంటైనర్ విలువలు వాడతారు.

---

## వెర్షన్ సరిపోలిక

### ప్యాకేజ్ వెర్షన్ మేట్రిక్స్

మల్టీ-ఏజెంట్ వర్క్‌ఫ్లోకు నిర్దిష్ట ప్యాకేజ్ వెర్షన్లు అవసరం. వెర్షన్‌ ల విలువల తేడా రన్‌టైమ్ లోపాలను కలిగిస్తుంది.

| ప్యాకేజ్ | అవసరమైన వెర్షన్ | చెక్ కమాండ్ |
|---------|-----------------|---------------|
| `agent-framework-foundry` | తాజా | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | తాజా | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | తాజా | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### సాధారణ వెర్షన్ లోపాలు

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# సరిచూడండి: ఎజెంట్-ఫ్రేమ్‌వర్క్-ఫౌండ్రీని మళ్లీ ఇన్‌స్టాల్ చేయండి
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# సవరణ: mcp ప్యాకేజీని అప్డేట్ చేయండి
pip install mcp --upgrade
```

### అన్ని వెర్షన్లను ఒకేసారి ధృవీకరించండి

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

అంచనా అవుట్‌పుట్:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## డిప్లాయ్‌మెంట్ సమస్యలు

### డిప్లాయ్‌మెంట్ తర్వాత కంటైనర్ స్టార్ట్ కావడం లేదు

1. **కంటైనర్ లాగ్‌లను చూడండి:**
   - **Foundry Toolkit** సైడ్‌బార్ తెరవండి → **Hosted Agents (Preview)** విస్తరించండి → మీ ఏజెంట్ పై క్లిక్ చేయండి → వెర్షన్ విస్తరించండి → **Container Details** → **Logs**.
   - Python స్టాక్ ట్రేస్‌లు లేదా మిస్సింగ్ మాడ్యూల్ లోపాలు కోసం చూడండి.

2. **సాధారణ కంటైనర్ స్టార్టప్ లోపాలు:**

   | లాగ్ లో లోపం | కారణం | పరిష్కారం |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` లో ప్యాకేజ్ లేదు | ప్యాకేజ్ జోడించి రీడిప్లాయ్ చేయండి |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` లేదా `.env` ఎన్విరాన్‌మెంట్ వేరియబుల్స్ సెటైయలేదు | `agent.yaml` → `environment_variables` సెక్షన్ (హోస్టెడ్) లేదా `.env` (లోకల్) అప్డేట్ చేయండి |
   | `azure.identity.CredentialUnavailableError` | మేనేజ్డ్ ఐడెంటిటీ కాన్ఫిగర్ చేయలేదు | Foundry స్వయంచాలకంగా సెట్ చేస్తుంది - ఎక్స్‌టెన్షన్ ద్వారా డిప్లాయ్ చేస్తున్నారనే నిర్ధారించుకోండి |
   | `OSError: port 8088 already in use` | Dockerfile తప్పు పోర్ట్ ను ఎక్స్‌పోజ్ చేసి ఉండటం లేదా పోర్ట్ విభేదం | Dockerfile లో `EXPOSE 8088` మరియు `CMD ["python", "main.py"]` ని నిర్ధారించండి |
   | కంటైనర్ కోడ్ 1తో నిష్క్రమణ | `main()` లో నియంత్రించని ఎక్సెప్షన్ | ముందుగా లోకల్‌లో పరీక్షించండి ([Module 5](05-test-locally.md)) లోపాలు పట్టుకోవడానికి |

3. **పరిష్కారం తర్వాత తిరిగి డిప్లాయ్ చేయండి:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → అదే ఏజెంట్ ఎంచుకొని → కొత్త వెర్షన్ డిప్లాయ్ చేయండి.

### డిప్లాయ్‌మెంట్ ఎక్కువసేపు పడుతుంది

మల్టీ-ఏజెంట్ కంటైనర్లు స్టార్ట్ కావడంలో ఎక్కువ సమయం పడతాయి ఎందుకంటే స్టార్ట్‌పై 4 ఏజెంట్ ఇన్‌స్టాన్స్‌లను సృష్టిస్తారు. సాధారణ స్టార్ట్ టైమ్స్:

| దశ | అంచనా వ్యవధి |
|-------|------------------|
| కంటైనర్ ఇమేజ్ బిల్డ్ | 1-3 నిమిషాలు |
| ఇమేజ్‌ను ACR కు పుష్ చేయడం | 30-60 సెలవులు |
| కంటైనర్ స్టార్ట్ (ఒకే ఏజెంట్) | 15-30 సెకన్లు |
| కంటైనర్ స్టార్ట్ (మల్టీ-ఏజెంట్) | 30-120 సెకన్లు |
| ఏజెంట్ ప్లేగ్రౌండ్ లో అందుబాటులో | "Started" తర్వాత 1-2 నిమిషాలు |

> "Pending" స్థితి 5 నిమిషాలను దాటితే, లోపాల కోసం కంటైనర్ లాగ్లను చూడండి.

---

## RBAC మరియు అనుమతి సమస్యలు

### `403 Forbidden` లేదా `AuthorizationFailed`

మీరు మీ Foundry ప్రాజెక్ట్ పై **[Foundry User](https://aka.ms/foundry-ext-project-role)** పాత్ర అవసరం (మునుపటి పేరు **Azure AI User** - రోల్ ID మారలేదు):

1. [Azure Portal](https://portal.azure.com) కు వెళ్ళండి → మీ Foundry **ప్రాజెక్ట్** వనరు.
2. **Access control (IAM)** → **Role assignments** క్లిక్ చేయండి.
3. మీ పేరు కోసం శోధించి → **Foundry User** (లేదా పాత లేబుల్ **Azure AI User**) ఉన్నదని ధృవీకరించండి.
4. లేనిపక్షంలో: **Add** → **Add role assignment** → **Foundry User** శోధించి → మీ ఖాతాకు అప్పగించండి.

వివరాల కోసం [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) డాక్యుమెంటేషన్ చూడండి.

### మోడల్ డిప్లాయ్‌మెంట్ అందుబాటులో లేదు

ఏజెంట్ మోడల్ సంబంధిత లోపాలను తిరిగి ఇచ్చినట్లయితే:

1. మోడల్ డిప్లాయ్ అయిందా అని నిర్ధారించుకోండి: Foundry సైడ్‌బార్ → ప్రాజెక్ట్ విస్తరించండి → **Models** → `gpt-4.1-mini` (లేదా మీ మోడల్) **Succeeded** స్థితితో ఉందో చూసుకోండి.
2. డిప్లాయ్‌మెంట్ పేరు సరిపోతుందా అని నిర్ధారించుకోండి: `.env` (లేదా `agent.yaml`) లో `AZURE_AI_MODEL_DEPLOYMENT_NAME` ని సైడ్‌బార్ లో అసలు డిప్లాయ్‌మెంట్ పేరుతో సరాసరి పోల్చండి.
3. డిప్లాయ్‌మెంట్ గడువు ముగిసిందా (ఫ్రీ టియర్): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) నుండి తిరిగి డిప్లాయ్ చేయండి (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry లోకల్ సమస్యలు (పాత్ బి)

### Foundry లోకల్ సర్వీస్ నడవడం లేదు

```powershell
# స్థితి తనిఖీ చేయండి
foundry local status

# సేవ ఆపబడినట్లయితే ప్రారంభించండి
foundry local start
```

| లక్షణం | కారణం | పరిష్కారం |
|---------|-------|-----|
| హెల్త్ చెక్ `503` తిరిగి ఇస్తుంది | సర్వీస్ స్టార్ట్ కాలేదు | `foundry local start` లేదా Foundry Toolkitsidebarలో **Start** క్లిక్ చేయండి |
| హెల్త్ చెక్ టైమ్ అవుట్ అవుతుంది | మోడల్ లోడవుతోంది | స్టార్ట్ చేసిన తర్వాత 30–60 సెకన్లు వేచి ఉండండి; పెద్ద మోడల్స్ ఎక్కువ సమయం పడతాయి |
| `/v1/health` పై `StatusCode: 404` | తప్పు పోర్ట్ | డిఫాల్ట్ `5273`. నిజమైన పోర్ట్ కోసం `foundry local status` చూడండి |
| సరిపోని వనరులు | Foundry Local కు ~4 GB RAM ఖాళీ అవసరం | ఇతర యాప్లను మూసేయండి |
| మోడల్ డౌన్లోడ్ విఫలం | తక్కువ డిస్క్ స్పేస్ | మోడల్స్ 2–8 GB. స్థలం ఖాళీ చేయండి, ఆపై `foundry model pull <name>` నడిపించండి |

### మోడల్ పేరు సరిపోకుండా ఉంది

```powershell
# డౌన్లోడ్ చేసిన మోడళ్లు మరియు వాటి కనిష్ట ప్రత్యామ్నాయ పేర్లను జాబితా చేయండి
foundry model list
```

`.env` లో `AZURE_AI_MODEL_DEPLOYMENT_NAME` ను ఖచ్చితంగా చూపిన అలియాస్ గా సెట్ చేయండి (ఉదా., `phi-4-mini` అనగా `Phi-4-mini` కాదు).

### లోకల్ నడపుటలో `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (పాత్ బి)

ల్యాబ్ యొక్క `main.py` `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` వాడుతుంది. Foundry లోకల్ ఈ వేరియబుల్ స్థానిక సర్వీస్ వైపు సూచించాలి - `AZURE_AI_PROJECT_ENDPOINT` కాదు. మీ `.env` లో ఇలా ఉండాలి:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP టూల్ ఇంకా అవుట్‌బౌండ్ కాల్ చేస్తోంది (పాత్ బి)

ఇది ఆశించదగినది. `search_microsoft_learn_for_plan` టూల్ `https://learn.microsoft.com/api/mcp` నుండి లెర్నింగ్ వనరులు తీసివ్వటానికి ఉపయోగపడుతుంది. **మాత్రమే స్కిల్-నేమ్ క్వెరీ** నెట్‌వర్క్‌ పై ప్రయాణిస్తుంది - రిజ్యూమే మరియు JD టెక్స్ట్ పూర్తిగా మీ పరికరం లోనే ప్రాసెస్ అవుతుంది మరియు ఎప్పుడూ ప్రసారం కాదు. పూర్తిగా ఆఫ్‌లైన్ ఆపరేషన్ అవసరం అయితే, టూల్ లో ఒక `try/except` fallback జోడించి ఎండ్‌పాయింట్ అందుబాటులో లేకపోతే స్థిరంగా `learn.microsoft.com` URL ను తిరిగిచ్చేలా చేయండి.

---

## సహాయం పొందడం

మీరు పై పరిష్కారాలను ప్రయత్నించిన తర్వాత ఇప్పటికైనా సమస్యలో ఉంటే:

1. **సర్వర్ లాగ్‌లను తనిఖీ చెయ్యండి** - చాలా లోపాలు టెర్మినల్ లో Python స్టాక్ ట్రేస్ ను ఉత్పత్తి చేస్తాయి. పూర్తి traceback చదవండి.
2. **లోపం సందేశం కోసం శోధించండి** - లోపం వచనాన్ని కాపీ చేసుకుని [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) లో శోధించండి.
3. **ఇష్యూ ఓపెన్ చేయండి** - [workshop రిపోజిటరీ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) లో ఇష్యూ ఫైలు చేయండి:
   - లోపం సందేశం లేదా స్క్రీన్‌షాట్
   - మీ ప్యాకేజ్ వెర్షన్లు (`pip list | Select-String "agent-framework"`)
   - మీ Python వెర్షన్ (`python --version`)
   - లోపం స్థానికంగా లేదా డిప్లాయ్‌మెంట్ తర్వాత వచ్చినదా

---

### చెక్‌పాయింట్

- [ ] మీరు `.env` కాన్ఫిగరేషన్ సమస్యలను ఎలా తనిఖీ చేసి పరిష్కరించాలో తెలుసుకున్నారు
- [ ] మీరు ప్యాకేజ్ వెర్షన్లను అవసరమైన మేట్రిక్స్‌తో సరిపోల్చగలుగుతారు
- [ ] మీరు డిప్లాయ్‌మెంట్ వైఫల్యాల కోసం కంటైనర్ లాగ్‌లను ఎలా తనిఖీ చేయాలో తెలుసుకున్నారు
- [ ] మీరు Azure పోర్టల్‌లో RBAC రోల్స్‌ను ధృవీకరించగలుగుతారు

---

**మునుపటి:** [07 - Verify in Playground](07-verify-in-playground.md) · **తరువాత:** [09 - Summary →](09-summary.md) · **హోమ్:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్వీకరణ**:
ఈ పత్రం AI అనువాద సేవ [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నిస్తున్నప్పటికీ, ఆటోమేటెడ్ అనువాదాలు తప్పులు లేదా అసమగ్రతలను కలిగి ఉండవచ్చు. దాని స్వదేశ భాషలో ఉన్న అసలు పత్రాన్ని అధికారం కలిగిన మూలంగా పరిగణించాలి. కీలకమైన సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదాన్ని సిఫారసు చేస్తాము. ఈ అనువాదం ఉపయోగం వల్ల కలిగే ఏవైనా అపార్థాలు లేదా తప్పుదారులు కోసం మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->