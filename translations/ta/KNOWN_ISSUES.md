# அறியப்பட்ட பிரச்சினைகள்

இந்த ஆவணம் தற்போதைய ரெப்பொசிடோரியின் நிலைமை வாயிலான அறியப்பட்ட பிரச்சினைகளை கண்காணிக்கிறது.

> சமீபத்தில் புதுப்பிக்கப்பட்டது: 2026-04-15. Python 3.13 / Windows இல் `.venv_ga_test`-ஆல் சோதிக்கப்பட்டது.

---

## தற்போதைய தொகுப்பு பின்கள் (மூன்று முகவர்களும்)

| தொகுப்பு | தற்போதைய பதிப்பு |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(ப_fix செய்தது — பாருங்கள KI-003)* |

---

## KI-001 — GA 1.0.0 மேம்பாடு தடையாயிற்று: `agent-framework-azure-ai` நீக்கப்பட்டது

**நிலைமை:** திறந்திருக் கூறப்பட்டது | **கடுமை:** 🔴 உயர் | **வகை:** உடைக்கும்

### விவரம்

`agent-framework-azure-ai` தொகுப்பு (`1.0.0rc3` இல் பின்கூட்டப்பட்ட) GA வெளியீட்டில் (1.0.0, 2026-04-02 வெளியிடப்பட்டது) **நீக்கப்பட்டு/காலாவதியானதாயிற்று**. இதன் மாற்றாக:

- `agent-framework-foundry==1.0.0` — Foundry-வழங்கபட்ட முகவர் மாதிரி
- `agent-framework-openai==1.0.0` — OpenAI ஆதரவுடன் முகவர் மாதிரி

மூன்றாம்படி `main.py` கோப்புகள் அனைவரும் `agent_framework.azure` இலிருந்து `AzureAIAgentClient`-ஐ இறக்குமதி செய்கின்றன, இது GA தொகுப்புகளில் `ImportError` ஏற்படுத்துகிறது. `agent_framework.azure` பெயரிடல் GA இல் இன்னும் உள்ளது, ஆனால் இப்போது வெறும் Azure Functions வகுப்புக்களை கொண்டுள்ளது (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — Foundry முகவர்களை அல்ல.

### உறுதிப்படுத்தப்பட்ட பிழை (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### பாதிக்கப்பட்ட கோப்புகள்

| கோப்பு | வரி |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` உடன் பொருந்தவில்லை

**நிலைமை:** திறந்திருத் | **கடுமை:** 🔴 உயர் | **வகை:** உடைக்கும் (மேல்நிலை மூலம் தடுப்பு)

### விவரம்

`azure-ai-agentserver-agentframework==1.0.0b17` (சமீபத்தியது) கடுமையான பின்கூட்டை செய்கிறது `agent-framework-core<=1.0.0rc3` ஆக. இதை GA பதிப்பு `agent-framework-core==1.0.0` உடன் நிறுவுவது, pip-ஐ `agent-framework-core`-ஐ மீண்டும் `rc3` க்கு கிழிக்க செய்யும், இது அதன் பிறகு `agent-framework-foundry==1.0.0` மற்றும் `agent-framework-openai==1.0.0` உடன் வேலை நிறுத்துகிறது.

அதனால், அனைத்து முகவர்களும் HTTP சர்வரை பிணைக்க `from azure.ai.agentserver.agentframework import from_agent_framework` பயன்படுத்துவதும் தடுப்பட்டுள்ளது.

### உறுதிப்படுத்தப்பட்ட சார்பு மோதல் (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### பாதிக்கப்பட்ட கோப்புகள்

மூன்று `main.py` கோப்புகளும் — மேல் நிலை இறக்கம் மற்றும் `main()` இல் உள்ள செயல்பாட்டு இறக்கம் இரண்டும்.

---

## KI-003 — `agent-dev-cli --pre` கொடி இனி தேவையில்லை

**நிலைமை:** ✅ திருத்தப்பட்டது (உடைப்பு இல்லாதது) | **கடுமை:** 🟢 குறைவு

### விவரம்

முந்தைய அனைத்து `requirements.txt` கோப்புகளும் முன் வெளியீட்டு CLI-ஐ பிரிதல் செய்ய `agent-dev-cli --pre` சேர்த்திருந்தன. GA 1.0.0 வெளியிடப்பட்ட 2026-04-02 முதல், `agent-dev-cli` சுருக்கமான வெளியீடு இப்போது `--pre` கொடியின்றி கிடைக்கிறது.

**திருத்தம் செய்தது:** மூன்று `requirements.txt` கோப்புகளிலிருந்தும் `--pre` கொடி அகற்றப்பட்டுள்ளது.

---

## KI-004 — Dockerfile கள் `python:3.14-slim` (முன்-வெளியீடு அடிப்படை படம்) பயன்படுத்துகின்றன

**நிலைமை:** திறந்திருக் கூறப்பட்டது | **கடுமை:** 🟡 குறைவு

### விவரம்

அனைத்து `Dockerfile`களும் `FROM python:3.14-slim` என்பதைக் பயன்படுத்துகின்றன, இது முன் வெளியீட்டு Python கட்டுமானத்தை பின்தொடர்கிறது. உற்பத்தி அமைப்புகளில் இது நிலையான வெளியீட்டுடன் பின்கூட்டப்பட வேண்டும் (எ.கா., `python:3.12-slim`).

### பாதிக்கப்பட்ட கோப்புகள்

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## குறிப்பிடல்கள்

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**விலக்கீடு**:  
இந்த ஆவணம் ஏ.ஐ. மொழிபெயர்ப்பு சேவை [Co-op Translator](https://github.com/Azure/co-op-translator) பயன்படுத்தி மொழிபெயர்க்கப்பட்டுள்ளது. நாங்கள் துல்லியமாக இருக்க முயல்வாலும், தானியங்கி மொழிபெயர்ப்புகளில் பிழைகள் அல்லது தவறுகள் இருக்க வாய்ப்பு உண்டு. அசல் ஆவணம் அதன் சொந்த மொழியில் அதிகாரப் பயனுள்ள மூலமாக கருதப்பட வேண்டும். முக்கியமான தகவலுக்கு, தொழில்முறை மனித மொழிபெயர்ப்பு பரிந்துரைக்கப்படும். இந்த மொழிபெயர்ப்பின் பயன்பாட்டிலிருந்து ஏற்படும் எந்த புரிதலிழப்புகளுக்கும் அல்லது தவறான விளக்கங்களுக்கும் நாங்கள் பொறுப்பு ஏற்க முடியாது.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->