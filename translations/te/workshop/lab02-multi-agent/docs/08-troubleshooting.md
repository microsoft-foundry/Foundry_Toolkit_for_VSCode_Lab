# మాడ్యూల్ 8 - సమస్య పరిష్కరణ (బహు-ఏజెంట్)

ఈ మాడ్యూల్ బహు-ఏజెంట్ వర్క్‌ఫ్లోకు సంబంధించిన సాధారణ లోపాలు, పరిష్కారాలు, మరియు డీబగ్గింగ్ వ్యూహాలను కవర్ చేస్తుంది. సాధారణ Foundry డిప్లాయ్‌మెంట్ సమస్యల కోసం, [ల్యాబ్ 01 సమస్య పరిష్కరణ గైడ్](../../lab01-single-agent/docs/08-troubleshooting.md) ను కూడా చూడండి.

---

## తక్షణ సూచిక: లోపం → పరిష్కారం

| లోపం / లక్షణం | సంభవించే కారణం | పరిష్కారం |
|----------------|-----------------|-----------|
| `RuntimeError: Missing required environment variable(s)` | `.env` ఫైల్ లేదు లేదా విలువలు సెట్ కాలేదు | `.env` లో `PROJECT_ENDPOINT=<your-endpoint>` మరియు `MODEL_DEPLOYMENT_NAME=<your-model>` కలిగినదిగా రూపొందించండి |
| `ModuleNotFoundError: No module named 'agent_framework'` | వర్చువల్ ఎన్విరాన్‌మెంట్ సක්‍රීయీకరించడం లేదా డిపెండెన్సీలు ఇన్‌స్టాల్ చేయలేదు | `.\.venv\Scripts\Activate.ps1` ను రన్ చేసి తర్వాత `pip install -r requirements.txt` చేయండి |
| `ModuleNotFoundError: No module named 'mcp'` | MCP ప్యాకేజ్ ఇన్‌స్టాల్ కాలేదు (requirements లో లేదు) | `pip install mcp` లేదా `requirements.txt` లో ట్రాన్సిటివ్ డిపెండెన్సీగా ఉందా అని తనిఖీ చేయండి |
| ఏజెంట్ ప్రారంభమవుతుంది కానీ ఖాళీ స్పందన ఇస్తుంది | `output_executors` సరిపోరు లేదా ఎడ్జులు లేవు | `output_executors=[gap_analyzer]` అని ధృవపరచండి మరియు అన్ని ఎడ్జులు `create_workflow()` లో ఉన్నాయో చూడండి |
| ఒక్క 1 గ్యాప్ కార్డ్ మాత్రమే (మిగిలినవి లేవు) | GapAnalyzer సూచనలు పూర్తి కావు | `GAP_ANALYZER_INSTRUCTIONS` లో `CRITICAL:` పేరాగ్రాఫ్ చేర్చండి - [మాడ్యూల్ 3](03-configure-agents.md) చూడండి |
| ఫిట్ స్కోరు 0 లేదా లేదు | MatchingAgent పైభాగం డేటా పొందలేదు | `add_edge(resume_parser, matching_agent)` మరియు `add_edge(jd_agent, matching_agent)` రెండూ ఉందా చూసుకోండి |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP సర్వర్ టూల్ కాల్‌ను తిరస్కరించింది | ఇంటర్నెట్ కనెక్టివిటీ తనిఖీ చేసుకోండి. బ్రౌజర్లో `https://learn.microsoft.com/api/mcp` ని ఓపెన్ చేయండి. మళ్లీ ప్రయత్నించండి |
| అవుట్పుట్‌లో Microsoft Learn URLs లేవు | MCP టూల్ రిజిస్టర్ కాలేదు లేదా ఎండ్‌పాయింట్ తప్పు | GapAnalyzer లో `tools=[search_microsoft_learn_for_plan]` మరియు `MICROSOFT_LEARN_MCP_ENDPOINT` సరైనదిగా ఉన్నదా తెలుసుకోండి |
| `Address already in use: port 8088` | మరో ప్రాసెస్ 8088 పోర్ట్ ఉపయోగిస్తోంది | Windows లో `netstat -ano \| findstr :8088` లేదా macOS/Linux లో `lsof -i :8088` రన్ చేసి అంతరాయం ఉన్న ప్రాసెస్ ఆపు |
| `Address already in use: port 5679` | Debugpy పోర్ట్ 5679 లో ఘర్షణ | ఇతర డీబగ్ సెషన్లు ఆపు. `netstat -ano \| findstr :5679` రన్ చేసి ప్రాసెస్ కనుగొని చంపండి |
| ఏజెంట్ ఇన్‌స్పెక్టర్ తెరవం | సర్వర్ పూర్తి స్థాయిలో మొదలైలేదో లేదా పోర్ట్ ఘర్షణ | "Server running" లాగ్ కోసం వేచి ఉండండి. పోర్ట్ 5679 ఫ్రీగా ఉన్నదా చూసుకోండి |
| `azure.identity.CredentialUnavailableError` | Azure CLI లో సైన్-ఇన్ కాలేదు | `az login` రన్ చేసి సర్వర్ మళ్లీ స్టార్ట్ చేయండి |
| `azure.core.exceptions.ResourceNotFoundError` | మోడల్ డిప్లాయ్‌మెంట్ లేదు | `MODEL_DEPLOYMENT_NAME` మీరు డిప్లాయ్ చేసిన మోడల్‌కు సరిపోతుందో చూసుకోండి |
| డిప్లాయ్‌మెంట్ తర్వాత కంటెయినర్ స్థితి "Failed" | కంటెయినర్ ప్రారంభంలో క్రాష్ | Foundry సైడ్‌బార్‌లో కంటెయినర్ లాగ్స్ తనిఖీ చేయండి. సాధారణంగా: env var గాయమై ఉండటం లేదా ఇంపోర్ట్ లోపం |
| డిప్లాయ్‌మెంట్ > 5 నిమిషాలు "Pending" గా ఉంటుంది | కంటెయినర్ ప్రారంభానికి ఎక్కువ సమయం పడడం లేదా రిసోర్సుల పరిమితులు | బహుఏజెంట్ నాలుగు ఏజెంట్ ఇన్స్టాన్సులు సృష్టిస్తుంటే 5 నిమిషాలు వరకు వేచి ఉండండి. ఇంకా Pending అయితే లాగ్స్ చూసుకోండి |
| `ValueError` `WorkflowBuilder` నుండి | చెల్లని గ్రాఫ్ కాన్ఫిగరేషన్ | `start_executor` సెట్ ఉందా, `output_executors` లిస్ట్ అయిందా, సర్క్యులర్ ఎడ్జులు లేవా అని నిర్ధారించుకోండి |

---

## ఎన్విరాన్‌మెంట్ మరియు కాన్ఫిగరేషన్ సమస్యలు

### మిస్సింగ్ లేదా తప్పు `.env` విలువలు

`.env` ఫైల్ `PersonalCareerCopilot/` డైరెక్టరీలో ఉండాలి (అది `main.py` తో ఒకే లెవెల్):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```
  
అంచనా `.env` కంటెంట్:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```
  
> **మీ PROJECT_ENDPOINT ఎలా కనుగొనాలి:**  
- VS Code లో **Microsoft Foundry** సైడ్‌బార్ ఓపెన్ చేసి → ప్రాజెక్ట్ పై రైట్-క్లిక్ → **Copy Project Endpoint** చేసుకోండి.  
- లేక అయితే [Azure Portal](https://portal.azure.com) → మీ Foundry ప్రాజెక్ట్ → **Overview** → **Project endpoint** చూడండి.

> **మీ MODEL_DEPLOYMENT_NAME ఎలా కనుగొనాలి:** Foundry సైడ్‌బార్‌లో మీ ప్రాజెక్ట్‌ను విస్తరించి → **Models** → మీరు డిప్లాయ్ చేసిన మోడల్ పేరు (ఉదా: `gpt-4.1-mini`) గమనించండి.

### Env var ప్రాధాన్యం

`main.py` లో `load_dotenv(override=False)` వాడటం అంటే:

| ప్రాధాన్యం | మూలం | బొమ్మగా ఉన్నా ఏది గెలుస్తుంది? |
|------------|--------|----------------------------|
| 1 (అత్యున్నత) | షెల్ ఎన్విరాన్‌మెంట్ వేరియబుల్ | అవును |
| 2 | `.env` ఫైల్ | షెల్ వేరియబుల్ లేకపోతే మాత్రమే |

దీంతో, హోస్ట్ చేయబడిన డిప్లాయ్‌మెంట్‌లో Foundry రన్‌టైమ్ env vars (`agent.yaml` ద్వారా సెట్ చేసినవి) `.env` విలువలకిపైగా ప్రాధాన్యం కలిగివుంటాయి.

---

## వెర్షన్ సరిపోలిక

### ప్యాకేజ్ వెర్షన్ మేట్రిక్స్

బహుఏజెంట్ వర్క్‌ఫ్లో వివిధ ప్యాకేజ్‌ల నిర్దిష్ట వెర్షన్లను అవసరం పొందుతుంది. వేరే వెర్షన్‌లు రన్‌టైమ్ లోపాలను కలిగించవచ్చు.

| ప్యాకేజ్ | అవసరమైన వెర్షన్ | చెక్ కమాండ్ |
|----------|------------------|-------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | తాజా ప్రీ-రిలీజ్ | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### సాధారణ వెర్షన్ లోపాలు

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# సరిచేయండి: rc3కు నవీకరించండి
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```
  
**`agent-dev-cli` కనుగొనలేకపోయింది లేదా ఇన్‌స్పెక్టర్ అసమర్థవంతం:**

```powershell
# సవరణ: --pre ఫ్లాగుతో ఇన్‌స్టాల్ చేయండి
pip install agent-dev-cli --pre --upgrade
```
  
**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# సవరించు: mcp ప్యాకేజీని అప్‌గ్రేడ్ చేయండి
pip install mcp --upgrade
```
  
### అన్ని వెర్షన్లను ఒకేసారి తనిఖీ చేయండి

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```
  
అంచనా అవుట్పుట్:

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

## MCP టూల్ సమస్యలు

### MCP టూల్ ఫలితాలు ఇవ్వడం లేదు

**లక్షణం:** Gap cards "Microsoft Learn MCP నుండి ఫలితాలు రాలేదు" లేదా "సిద్ధమైన Microsoft Learn ఫలితాలు కనబడలేదు" అని చెబుతుంది.

**సంభవించే కారణాలు:**

1. **నెట్‌వర్క్ సమస్య** - MCP ఎండ్‌పాయింట్ (`https://learn.microsoft.com/api/mcp`) అజేయమైంది.  
   ```powershell
   # కనెక్టివిటీ పరీక్షించండి
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   ఇది `200` తిరిగిస్తే ఎండ్‌పాయింట్ అందుబాటులో ఉంది.

2. **అత్యంత నిర్దిష్టమైన క్వరీ** - స్కిల్ పేరు Microsoft Learn సెర్చ్‌కు చాలా ప్రత్యేకంగా ఉంది.  
   - ప్రత్యేక నైపుణ్యాలకు ఇది సాధారణం. టూల్ రిప్లైలో fallback URL ఉంటుంది.

3. **MCP సెషన్ టైమౌట్** - Streamable HTTP కనెక్షన్ టైమౌట్ అయ్యింది.  
   - మళ్లీ ప్రయత్నించండి. MCP సెషన్లు తాత్కాలికంగా ఉంటాయి, పునఃకనెక్ట్ అవసరం కావచ్చు.

### MCP లాగ్స్ వివరణ

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```
  
| లాగ్ | అర్థం | చర్య |
|-------|--------|-------|
| `GET → 405` | MCP క్లయింట్ ఇనిషియలైజేషన్ probes | సాధారణం - ఆదర్శించవచ్చు |
| `POST → 200` | టూల్ కాల్ విజయవంతం | ఆశించినది |
| `DELETE → 405` | MCP క్లయింట్ క్లీన్‌అప్ probes | సాధారణం - ఆదర్శించవచ్చు |
| `POST → 400` | తప్పు క్వరీ (దుర్వినియోగమైన) | `search_microsoft_learn_for_plan()` లో `query` పరామితి తనిఖీ చేయండి |
| `POST → 429` | రేట్ లిమిట్ | వేచి మళ్లీ ప్రయత్నించండి. `max_results` పరిమితిని తగ్గించండి |
| `POST → 500` | MCP సర్వర్ లోపం | తాత్కాలికం - పునఃప్రయత్నించండి. ఎక్కువకాలం ఉంటే Microsoft Learn MCP API అచేతనంగా ఉండవచ్చు |
| కనెక్షన్ టైమౌట్ | నెట్‌వర్క్ లేదా MCP సర్వర్ అందుబాటులో లేదు | ఇంటర్నెట్ తనిఖీ. `curl https://learn.microsoft.com/api/mcp` ప్రయత్నించండి |

---

## డిప్లాయ్‌మెంట్ సమస్యలు

### డిప్లాయ్‌మెంట్ తర్వాత కంటెయినర్ ప్రారంభం విఫలమైంది

1. **కంటెయినర్ లాగ్స్ తనిఖీ చేయండి:**  
   - **Microsoft Foundry** సైడ్‌బార్ → **Hosted Agents (Preview)** విస్తరించండి → మీ ఏజెంట్ క్లిక్ చేయండి → వెర్షన్ విస్తరించండి → **Container Details** → **Logs**.  
   - Python స్టాక్ ట్రేస్‌లు లేదా మిస్సింగ్ మాడ్యూల్ లోపాలు చూడండి.

2. **సాధారణ కంటెయినర్ స్టార్ట్ విఫలతలు:**

   | లాగ్ లో లోపం | కారణం | పరిష్కారం |
   |--------------|---------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` లో ప్యాకేజీ లేదు | ప్యాకేజీ జోడించి మళ్లీ డిప్లాయ్ చేయండి |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` env vars సెట్ కాలేదు | `agent.yaml` లో `environment_variables` సెక్షన్ నవీకరించండి |
   | `azure.identity.CredentialUnavailableError` | Managed Identity కాన్ఫిగర్ కాలేదు | Foundry ఇది ఆటోమేటిగా సెట్ చేస్తుంది - ఎక్స్‌టెన్షన్ ద్వారా డిప్లాయ్ చేస్తున్నారు కాబట్టి ధృవీకరించండి |
   | `OSError: port 8088 already in use` | Dockerfile తప్పు పోర్ట్ ఎక్స్‌పోస్ చేయడం లేదా పోర్ట్ ఘర్షణ | Dockerfile లో `EXPOSE 8088` మరియు `CMD ["python", "main.py"]` సరైనదిగా ఉన్నదో చూసుకోండి |
   | కంటెయినర్ కోడ్ 1 తో ఫెయ్యిల్ | `main()` లో హ్యాండిల్ కాని ఎక్సెప్షన్ | లోకల్‌గా మొదటి ([Module 5](05-test-locally.md)) నుండి తనిఖీ చేయండి |

3. **సరైన పరిష్కారం తర్వాత మళ్లీ డిప్లాయ్ చేయండి:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → అదే ఏజెంట్ ఎంపిక → కొత్త వెర్షన్ డిప్లాయ్ చేయండి.

### డిప్లాయ్‌మెంట్ ఎక్కువ వ్యవధి తీసుకుంటుంది

బహుఏజెంట్ కంటెయినర్లు 4 ఏజెంట్ ఇన్స్టాన్సులు ప్రారంభిస్తుంటే ఎక్కువ సమయం పడుతుంది. సాధారణ ప్రారంభ సమయాలు:

| దశ | అంచనా వ్యవధి |
|-----|---------------|
| కంటెయినర్ ఇమేజ్ బిల్డ్ | 1-3 నిమిషాలు |
| ఇమేజ్‌ను ACRకి పుష్ చేయడం | 30-60 సెకన్లు |
| కంటెయినర్ ప్రారంభం (సింగిల్ ఏజెంట్) | 15-30 సెకన్లు |
| కంటెయినర్ ప్రారంభం (బహుఏజెంట్) | 30-120 సెకన్లు |
| ప్లేగ్రౌండ్‌లో ఏజెంట్ అందుబాటులో | "Started" తర్వాత 1-2 నిమిషాలు |

> "Pending" స్థితి 5 నిమిషాలు దాటి ఉంటే, కంటెయినర్ లాగ్స్ లో లోపాలను తనిఖీ చేయండి.

---

## RBAC మరియు అనుమతి సమస్యలు

### `403 Forbidden` లేదా `AuthorizationFailed`

మీకు మీ Foundry ప్రాజెక్టుకు **[Azure AI User](https://aka.ms/foundry-ext-project-role)** పాత్ర అవసరం:

1. [Azure Portal](https://portal.azure.com) → మీ Foundry **ప్రాజెక్ట్** వనరు వెళ్ళండి.  
2. **Access control (IAM)** → **Role assignments** క్లిక్ చేయండి.  
3. మీ పేరు కోసం సెర్చ్ చేసి **Azure AI User** లిస్ట్‌లో ఉన్నదా చూసుకోండి.  
4. లేనట్లయితే: **Add** → **Add role assignment** → **Azure AI User** సెర్చ్ చేసి మీ అకౌంట్‌కు కేటాయించండి.

[RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) డాక్యుమెంటేషన్ చూడండి.

### మోడల్ డిప్లాయ్‌మెంట్ 접근ం లేదు

ఏజెంట్ మోడల్ సంబంధిత లోపాలను ఇస్తే:

1. మోడల్ డిప్లాయ్ అయిందా ధృవీకరించండి: Foundry సైడ్‌బార్ → ప్రాజెక్ట్ విస్తరించండి → **Models** → `gpt-4.1-mini` (లేదా మీ మోడల్) స్థితి **Succeeded** ఉందా చూడండి.  
2. డిప్లాయ్‌మెంట్ పేరు సరిపోతుందా: `.env` లేదా `agent.yaml` లో `MODEL_DEPLOYMENT_NAME` తో సైడ్‌బార్ లోని డిప్లాయ్‌మెంట్ పేరు పోల్చండి.  
3. డిప్లాయ్‌మెంట్ గడువు పూర్తి అయి ఉంటే (ఫ్రీ tier): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) నుండి మళ్లీ డిప్లాయ్ చెయ్యండి (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## ఏజెంట్ ఇన్‌స్పెక్టర్ సమస్యలు

### ఇన్‌స్పెక్టర్ తెరుస్తే "Disconnected" చూపిస్తుంది

1. సర్వర్ నడుస్తున్నదా తనిఖీ చేయండి: టెర్మినల్‌లో "Server running on http://localhost:8088" చూడండి.  
2. పోర్ట్ `5679` తనిఖీ: ఇన్‌స్పెక్టర్ debugpy ద్వారా ఈ పోర్ట్ కనెక్ట్ అవుతుంది.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. సర్వర్ మళ్లీ స్టార్ట్ చేసి ఇన్‌స్పెక్టర్ కొత్తగా తెరవండి.

### ఇన్‌స్పెక్టర్ భాగస్వామి స్పందన చూపిస్తుంది

బహుఏజెంట్ ప్రతిస్పందనలు పొడవుగా ఉంటాయి మరియు స్ట్రీమ్ విధంగా వస్తాయి. పూర్తి ప్రతిస్పందన పూర్తి కాగాకుంటే వేచి ఉండండి (క్షేత్రాల సంఖ్య మరియు MCP కాల్లుల సంఖ్య ఆధారంగా 30-60 సెకన్లు పట్టవచ్చు).

ప్రతిస్పందన తరచుగా త్రింకిపోయినట్లైతే:  
- GapAnalyzer సూచనలలో గ్యాప్ కార్డులు మిళితం కాకుండా `CRITICAL:` బ్లాక్ ఉందో తనిఖీ చేయండి.  
- మీ మోడల్ టోకెన్ పరిమితి పరిగణనలోకి తీసుకోండి - `gpt-4.1-mini` 32K అవుట్పుట్ టోకెన్ల వరకు మద్దతు ఇస్తుంది, సాధారణంగా సరిపోతుంది.

---

## పనితీరు చిట్కాలు

### మెల్లయిన స్పందనలు

బహుఏజెంట్ వర్క్‌ఫ్లోలు క్రమంగా ఆధారపడటం మరియు MCP టూల్ కాల్‌ల కారణంగా సింగిల్ ఏజెంట్ కన్నా నెమ్మదిగా ఉంటాయి.

| ఆప్టిమైజేషన్ | ఎలా ఉపయోగించాలి | ప్రభావం |
|--------------|-----------------|---------|
| MCP కాల్లుపై తగ్గింపు | టూల్ లో `max_results` పరిమితిని తగ్గించడం | HTTP రౌండ్-ట్రిప్‌లు తగ్గుతాయి |
| సూచనల సూటిపరచడం | చిన్న, కేంద్రీకృత ఏజెంట్ ప్రాంప్ట్‌లు | త్వరగా LLM ఉత్పత్తి |
| `gpt-4.1-mini` వాడటం | `gpt-4.1` కంటే వేగవంతం అభివృద్ధికి | సుమారు 2 రెట్లు వేగం పెరుగుతుంది |
| గ్యాప్ కార్డ్ వివరాలు తగ్గించడం | GapAnalyzer సూచనల్లో గ్యాప్ కార్డ్ ఫార్మాట్ సులభతరం | తక్కువ అవుట్పుట్ అవసరం |

### స్థానిక సాధారణ స్పందన సమయాలు

| కాన్ఫిగరేషన్ | అంచనా సమయం |
|--------------|-------------|
| `gpt-4.1-mini`, 3-5 గ్యాప్ కార్డులు | 30-60 సెకన్లు |
| `gpt-4.1-mini`, 8+ గ్యాప్ కార్డులు | 60-120 సెకన్లు |
| `gpt-4.1`, 3-5 గ్యాప్ కార్డులు | 60-120 సెకనులు |
---

## సహాయం పొందడం

మీరు పై పరిష్కారాలను ప్రయత్నించిన తర్వాత బంతిగా ఉంటే:

1. **సర్వర్ సంకేతాలను తనిఖీ చేయండి** - ఎక్కువగా పొరపాట్లు టెర్మినల్‌లో Python స్టాక్ ట్రేస్‌ను ఉత్పత్తి చేస్తాయి. పూర్తి ట్రేస్‌బ్యాక్‌ను చదవండి.
2. **పొరపాటు సందేశాన్ని శోధించండి** - పొరపాటు వാഖ్యం కాపీ చేసి [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)లో శోధించండి.
3. **సమస్యను ఓపెన్ చేయండి** - [వర్క్‌షాప్ రిపొజిటరీ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues)లో సమస్యను నమోదు చేయండి:
   - పొరపాటు సందేశం లేదా స్క్రీన్‌షాట్
   - మీ ప్యాకేజీ వెర్షన్లు (`pip list | Select-String "agent-framework"`)
   - మీ Python వెర్షన్ (`python --version`)
   - సమస్య స్థానికమని లేదా డిప్లాయ్‌మెంట్ తరువాతనటువంటిదని

---

### చెక్‌పాయింట్

- [ ] మీరు భాగం-ఏజెంట్ పొరపాట్లను త్వరిత సమాచారం పట్టిక ద్వారా గుర్తించి సరిచేయగలరు
- [ ] మీరు `.env` కాన్ఫిగరేషన్ సమస్యలను తనిఖీ చేసి సరిచేయడం తెలుసు
- [ ] మీరు ప్యాకేజీ వెర్షన్లు అవసరమైన మ్యాట్రిక్స్‌కు సరిపోతున్నాయా అని ధృవీకరించగలరు
- [ ] మీరు MCP లాగ్ ఎంట్రీలను అర్థం చేసుకొని టూల్ విఫలతలను నిర్ధారణ చేయగలరు
- [ ] మీరు డిప్లాయ్‌మెంట్ విఫలతలకు కాంటైనర్ లాగ్‌లను తనిఖీ చేయడం తెలుసు
- [ ] మీరు Azure పోర్టల్‌లో RBAC పాత్రలను ధృవీకరిస్తారు

---

**మునుపటి:** [07 - Verify in Playground](07-verify-in-playground.md) · **హోమ్:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**డిస్క్లెయిమర్**:  
ఈ డాక్యుమెంట్ AI అనువాద సేవ అయిన [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. సరైన అనువాదానికి ఏర్పాటు చేస్తూ ఉన్నప్పటికీ, ఆటోమేటెడ్ అనువాదాలలో పొరపాట్లు లేదా తప్పుడు అర్థాలు ఉండొచ్చు అని దయచేసి గమనించండి. మాతృభాషలో ఉన్న అసలు డాక్యుమెంట్ అధికారిక మూలంగా పరిగణించబడుతుంది. కీలక సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదాన్ని సూచిస్తున్నాము. ఈ అనువాదం వాడటం వల్ల కలిగే ఏవైనా అర్థం తప్పు లేదా తప్పు అభిప్రాయాలకు మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->