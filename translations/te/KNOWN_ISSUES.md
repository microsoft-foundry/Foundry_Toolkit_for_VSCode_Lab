# తెలిసిన సమస్యలు

ఇది ప్రస్తుత రిపోజిటరీ స్థితితో సంబంధించిన తెలిసిన సమస్యలను ట్రాక్ చేస్తుంది.

> చివరి నవీకరణ: 2026-04-15. Python 3.13 / Windows వద్ద `.venv_ga_test`లో పరీక్షించబడింది.

---

## ప్రస్తుత ప్యాకేజీ పిన్స్ (మూడువైపు ఏజెంట్లు)

| ప్యాకేజీ | ప్రస్తుత వెర్షన్ |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(ఫిక్స్ చేయబడింది — KI-003 చూడండి)* |

---

## KI-001 — GA 1.0.0 అప్‌గ్రేడ్ ఆపివేయబడింది: `agent-framework-azure-ai` తీసివేయబడింది

**స్థితి:** తెరిచి ఉంది | **తీవ్రత:** 🔴 అధిక | **రకం:** బ్రేకింగ్

### వివరణ

`agent-framework-azure-ai` ప్యాకేజీ (పిన్ చేయబడింది `1.0.0rc3` వద్ద) GA విడుదలలో (1.0.0, 2026-04-02 విడుదల) **తీసివేయబడింది/డిప్రీకేట్ చేయబడింది**. దీన్ని ఇలా మార్చబడింది:

- `agent-framework-foundry==1.0.0` — Foundry-ఉగ్మించబడిన ఏజెంట్ ప్యాటర్న్
- `agent-framework-openai==1.0.0` — OpenAI ఆధారిత ఏజెంట్ ప్యాటర్న్

మూడు `main.py` ఫైళ్లన్నీ `agent_framework.azure` నుండి `AzureAIAgentClient` ను దిగుమతి చేసుకుంటాయి, ఇది GA ప్యాకేజీల క్రింద `ImportError` కలిగిస్తుంది. `agent_framework.azure` నేమ్‌స్పేస్ GA లో ఇంకా ఉంది కాని ఇప్పుడు కేవలం Azure Functions తరగతులను మాత్రమే కలిగి ఉంది (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — Foundry ఏజెంట్లు కాదని.

### నిర్ధారించబడిన లోపం (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### ప్రభావిత ఫైళ్లు

| ఫైల్ | లైన్ |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` తో సరిగ్గా పనిచేయదు

**స్థితి:** తెరిచి ఉంది | **తీవ్రత:** 🔴 అధిక | **రకం:** బ్రేకింగ్ (అప్పెన్డింగ్ పై బ్లాక్)

### వివరణ

`azure-ai-agentserver-agentframework==1.0.0b17` (తాజా) హార్డ్-పిన్ చేస్తుంది
`agent-framework-core<=1.0.0rc3`. దీన్ని సహా `agent-framework-core==1.0.0` (GA)
టైడ్‌లో ఇన్‌స్టాల్ చేస్తే pip ను `agent-framework-core`ను తిరిగి `rc3` కు డౌన్‌గ్రేడ్ చేయనిస్తుంది, ఇది అప్పుడు
`agent-framework-foundry==1.0.0` మరియు `agent-framework-openai==1.0.0` ని బ్రేక్ చేస్తుంది.

`azure.ai.agentserver.agentframework` నుండి `from_agent_framework` ను అన్ని ఏజెంట్లు ఉపయోగించి HTTP సర్వర్ బైండ్ చేయడానికి పిలవడం కూడా బ్లాక్ అవుతుంది.

### నిర్ధారించబడిన డిపెండెన్సీ గొడవ (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### ప్రభావిత ఫైళ్లు

మూడు `main.py` ఫైళ్లలోనూ — టాప్-లెవెల్ దిగుమతి మరియు `main()` లో ఫంక్షన్ లో దిగుమతి రెండూ.

---

## KI-003 — `agent-dev-cli --pre` ఫ్లాగ్ అవసరం లేదు

**స్థితి:** ✅ పరిష్కరించబడింది (అప్రభావం) | **తీవ్రత:** 🟢 తక్కువ

### వివరణ

ముందు అన్ని `requirements.txt` ఫైళ్లు `agent-dev-cli --pre` ని ప్రీ-రిలీజ్ CLIను తీసుకునేందుకు ఉపయోగించాయి. GA 1.0.0 విడుదల అయ్యాక 2026-04-02 నుండి, స్థిరమైన విడుదల `agent-dev-cli` ఇప్పుడు `--pre` ఫ్లాగ్ లేకుండా అందుబాటులో ఉంది.

**పరిష్కారం:** `--pre` ఫ్లాగ్ మూడింటి `requirements.txt` ఫైళ్ల నుండి తీసివేయబడింది.

---

## KI-004 — Dockerfiles `python:3.14-slim` (ప్రీ-రిలీజ్ బేస్ ఇమేజ్) ను ఉపయోగిస్తాయి

**స్థితి:** తెరిచి ఉంది | **తీవ్రత:** 🟡 తక్కువ

### వివరణ

అన్ని `Dockerfile`s `FROM python:3.14-slim` ఉపయోగిస్తాయి, ఇది ప్రీ-రిలీజ్ Python బిల్డ్ ని సూచిస్తుంది. ఉత్పత్తి అమరికల కోసం దీన్ని స్థిర విడుదల (ఉదా: `python:3.12-slim`) కు పిన్ చేయాలి.

### ప్రభావిత ఫైళ్లు

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## సూచనలు

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్పృశ్యం**:  
ఈ డాక్యుమెంట్ [Co-op Translator](https://github.com/Azure/co-op-translator) అనే AI అనువాద సేవను ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నించినప్పటికీ, ఆటోమేటిక్ అనువాదాలలో తప్పులు లేదా అసమగ్రతలు ఉన్నట్లు ఉండవచ్చు. మూల భాషలో ఉన్న الأصل డాక్యుమెంట్ అధికారిక మూలంగా పరిగణించాలి. ముఖ్యమైన సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదం చేయించుకోవడం సిఫార్సు చేయబడుతుంది. ఈ అనువాదాన్ని ఉపయోగించే సందర్భంలో ఏమైనా అవగాహన లోపాలు లేదా తప్పు అర్థం చేసుకోవడం వల్ల కలిగే బాధ్యత మేము తీసుకోము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->