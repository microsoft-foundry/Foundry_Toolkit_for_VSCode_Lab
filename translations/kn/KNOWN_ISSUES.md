# ತಿಳಿದಿರುವ ಸಮಸ್ಯೆಗಳನ್ನನು

ಈ ದಾಖಲೆ ಪ್ರಸ್ತುತ ರೆಪೊಸಿಟರಿ ಸ್ಥಿತಿಯೊಂದಿಗೆ ತಿಳಿದಿರುವ ಸಮಸ್ಯೆಗಳನ್ನನು ಟ್ರ್ಯಾಕ್ ಮಾಡುತ್ತದೆ.

> ಕೊನೆಯದಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ: 2026-04-15. Python 3.13 / Windows ನಲ್ಲಿ `.venv_ga_test` ಮೇಲೆ ಪರೀಕ್ಷಿಸಲಾಗಿದೆ.

---

## ಪ್ರಸ್ತುತ ಪ್ಯಾಕೇಜ್ ಪಿನ್ಗಳು (ಎಲ್ಲಾ ಮೂರು ಏಜೆಂಟ್ಸ್)

| ಪ್ಯಾಕೇಜ್ | ಪ್ರಸ್ತುತ ಆವೃತ್ತಿ |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(ನಿರ್ಧರಿಸಲಾಗಿದೆ — KI-003 ಅನ್ನು ನೋಡಿ)* |

---

## KI-001 — GA 1.0.0 ಅಪ್‌ಗ್ರೇಡ್ ತಡೆಯಲ್ಪಟ್ಟಿದೆ: `agent-framework-azure-ai` ಅನ್ನು ತೆಗೆದುಹಾಕಲಾಗಿದೆ

**ಸ್ಥಿತಿ:** ತೆರೆಯಲಾಗಿದೆ | **ಗಂಭೀರತೆ:** 🔴 ಉನ್ನತ | **ತരം:** ಬ್ರೇಕಿಂಗ್

### ವಿವರಣೆ

`agent-framework-azure-ai` ಪ್ಯಾಕೇಜ್ (`1.0.0rc3` ನಲ್ಲಿದೆ), GA ಬಿಡುಗಡೆ (1.0.0, 2026-04-02 ರಲ್ಲಿ ಬಿಡುಗಡೆಗೊಂಡ) ನಲ್ಲಿ **ತೆಗೆಯಲ್ಪಟ್ಟ/ನಿರಾಸು ಮಾಡಿದ** ಆಗಿದ್ದಿದೆ. ಇದನ್ನು ಕೆಳಗಿನವುಗಳು ಬದಲಾಯಿಸಿದ್ದವೆ:

- `agent-framework-foundry==1.0.0` — Foundry ಆತಿಥ್ಯ ಏಜೆಂಟ್ ಪ್ಯಾಟರ್ನ್
- `agent-framework-openai==1.0.0` — OpenAI ಆಧಾರಿತ ಏಜೆಂಟ್ ಪ್ಯಾಟರ್ನ್

ಎಲ್ಲಾ `main.py` ಕಡತಗಳು `agent_framework.azure` ರಿಂದ `AzureAIAgentClient` ಅನ್ನು ಆಮದುಮಾಡುತ್ತವೆ, ಇದು GA ಪ್ಯಾಕೇಜ್‌ಗಳಲ್ಲಿ `ImportError` ಹೊಂದಿಸುತ್ತದೆ. GA ಯಲ್ಲಿಯೂ `agent_framework.azure` ನamespace ಇರುತ್ತದೆ ಆದರೆ ಅದು ಈಗ ಕೇವಲ Azure Functions ವರ್ಗಗಳನ್ನು ( `DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) ಹೊಂದಿದೆ — Foundry ಏಜೆಂಟ್ಸ್ ಅಲ್ಲ.

### ದೃಢೀಕರಿಸಿದ ದೋಷ (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### ಪ್ರಭಾವಿತ ಕಡತಗಳು

| ಕಡತ | ಸಾಲು |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` ಜೊತೆಗೆ ಹೊಂದಿಕೆಯಲ್ಲ

**ಸ್ಥಿತಿ:** ತೆರೆಯಲಾಗಿದೆ | **ಗಂಭೀರತೆ:** 🔴 ಉನ್ನತ | **ತരം:** ಬ್ರೇಕಿಂಗ್ (ಅಪ್ತಸತತೆಯ ಮೇಲೆ ತಡೆಯಲ್ಪಟ್ಟಿದೆ)

### ವಿವರಣೆ

`azure-ai-agentserver-agentframework==1.0.0b17` (ಇತ್ತೀಚಿನ) ಕಠಿಣವಾಗಿ 
`agent-framework-core<=1.0.0rc3` ಅನ್ನು ಪಿನ್ ಮಾಡುತ್ತದೆ. ಇದನ್ನು GA (1.0.0) ಹೊಂದಿರುವ 
`agent-framework-core==1.0.0` ಜೊತೆಗೆ ಇನ್ಸ್ಟಾಲ್ ಮಾಡಿದರೆ, pip ಅನ್ನು 
`agent-framework-core` ನ್ನು ಮತ್ತೆ `rc3` ಗೆ ಡೌನ್‌ಗ್ರೇಡ್ ಮಾಡಲು ಬಲಪಡಿಸುತ್ತದೆ, ಇದು ನಂತರ 
`agent-framework-foundry==1.0.0` ಮತ್ತು `agent-framework-openai==1.0.0` ಅನ್ನು ಭಂಗಮಾಡುತ್ತದೆ.

ಎಲ್ಲಾ ಏಜೆಂಟ್ಗಳು HTTP ಸರ್ವರ್ ಅನ್ನು ಬಂಧಿಸಲು ಬಳಸುವ `from azure.ai.agentserver.agentframework import from_agent_framework` ಕರೆ ಇದರಿಂದ ಕೂಡ ತಡೆಯಲ್ಪಟ್ಟಿದೆ.

### ದೃಢೀಕರಿಸಿದ ಅವಲಂಬನೆ ಗೊಂದಲ (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### ಪ್ರಭಾವಿತ ಕಡತಗಳು

ಮೂರು `main.py` ಕಡತಗಳಲ್ಲೂ — ಮೇಲಿನ ಮಟ್ಟದ ಆಮದು ಮತ್ತು `main()` లో ಫಂಕ್ಷನಿನೊಳಗಿನ ಆಮದು ಎರಡೂ.

---

## KI-003 — `agent-dev-cli --pre` ಧ್ವಜ ಈಗ ಬಳಕೆಯಲ್ಲ

**ಸ್ಥಿತಿ:** ✅ ಸರಿಪಡಿಸಲಾಗಿದೆ (ಬ್ರೇಕಿಂಗ್ ಇಲ್ಲ) | **ಗಂಭೀರತೆ:** 🟢 ಕಡಿಮೆ

### ವಿವರಣೆ

ಕೊನೆಯವರೆಗೂ ಎಲ್ಲಾ `requirements.txt` ಕಡತಗಳು `agent-dev-cli --pre` ಅನ್ನು 
ಪೂರ್ವ ಬಿಡುಗಡೆ CLI ಅನ್ನು ಪಡೆಯಲು ಒಳಗೊಂಡಿದ್ದವು. GA 1.0.0 2026-04-02 ರಂದು ಬಿಡುಗಡೆ ಮಾಡಿದ 
ನಂತರ, `agent-dev-cli` ಸ್ಥಿರ ಬಿಡುಗಡೆ ಈಗ `--pre` ಧ್ವಜವಿಲ್ಲದೆ ಲಭ್ಯವಿದೆ.

**ಸರಿಪಡಿಸಿದ:** ಮೂರು `requirements.txt` ಕಡತಗಳಲ್ಲೂ `--pre` ಧ್ವಜವನ್ನು ತೆಗೆದುಹಾಕಲಾಗಿದೆ.

---

## KI-004 — Dockerfiles `python:3.14-slim` (ಪೂರ್ವ ಬಿಡುಗಡೆಯ ಮೂಲ ಚಿತ್ರ) ಬಳಕೆಮಾಡುತ್ತವೆ

**ಸ್ಥಿತಿ:** ತೆರೆಯಲಾಗಿದೆ | **ಗಂಭീരತೆ:** 🟡 ಕಡಿಮೆ

### ವಿವರಣೆ

ಎಲ್ಲಾ `Dockerfile` ಗಳು `FROM python:3.14-slim` ಬಳಸುವವು, ಇದು ಪೂರ್ವ ಬಿಡುಗಡೆಯ Python ಬಿಲ್ಡ್ ಅನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡುತ್ತದೆ.
ಉತ್ಪಾದನಾ ನಿಯೋಜನೆಗಾಗಿ ಇದನ್ನು ಸ್ಥಿರ ಬಿಡುಗಡೆಗೆ (ಉದಾ. `python:3.12-slim`) ಪಿನ್ ಮಾಡಬೇಕು.

### ಪ್ರಭಾವಿತ ಕಡತಗಳು

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## સંદર્ભಗಳು

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ತಪ್ಪು ಭಾರವೇ ಮುಕ್ತಾಯ**:  
ಈ ದಸ್ತಾವೇಜು [Co-op Translator](https://github.com/Azure/co-op-translator) ಎಂಬ AI ಅನುವಾದ ಸೇವೆಯನ್ನು ಬಳಸಿ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ಶುದ್ಧತೆಗೆ ಪ್ರಯತ್ನಿಸುವಾಗ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ತಪ್ಪುಗಳು ಅಥವಾ ಅಸತ್ಯತೆಗಳು ಇರಬಹುದು ಎಂಬುದನ್ನು ದಯವಿಟ್ಟು ಗಮನದಲ್ಲಿಡಿ. ಮೂಲ ಭಾಷೆಯಲ್ಲಿನ ಮೂಲ ದಸ್ತಾವೇಜುಗಳನ್ನು ಅಧಿಕಾರಿಯ ಮೂಲವಾಗಿ ಪರಿಗಣಿಸಬೇಕು. ಪ್ರಮುಖ ಮಾಹಿತಿಗಾಗಿ, ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ. ಈ ಅನುವಾದ ಬಳಕೆಯಿಂದ ಉಂಟಾಗುವ ಅರ್ಥಚಾಚಿ ಅಥವಾ ತಪ್ಪು ವಿವರಣೆಗಳಿಗೆ ನಾವು ಉತ್ತರದಾಯಕರಾಗಿರುವುದಿಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->