# ಮాడ್ಯೂಲ್ 8 - ಸಮಸ್ಯೆಗಳು ಪರಿಹರಿಸುವುದು

ಈ ಮಾಡ್ಯೂಲ್ ಬಹು-ಏಜೆಂಟ್ ವರ್ಕ್‌ಫ್ಲೋಗೆ ವಿಶೇಷವಾದ ಸಾಮಾನ್ಯ ದೋಷಗಳು, ಸರಿಪಡಿಸಲು ವಿಧಾನಗಳು ಮತ್ತು ಡಿಬಗ್ ತಂತ್ರಗಳನ್ನು ಒಳಗೊಂಡಿದೆ.

## ಏಜೆಂಟ್ ಔಟ್‌ಪುಟ್ ಸಮಸ್ಯೆಗಳು

### GapAnalyzer “ನನಗೆ ಇನ್ನುವೂ ಹೊಂದಾಣಿಕೆ ವರದಿ ಇಲ್ಲ” ಎನ್ನುತ್ತಿದೆ

**ಲಕ್ಷಣ:** GapAnalyzer ಪ್ರತಿಕ್ರಿಯೆಯಲ್ಲಿ “ಕೈವೇಳದ ಕೌಶಲಗಳು” ಹಾಗೂ “ಪ್ರಮಾಣಪತ್ರದ ಕೊರತೆಗಳು” ಹೊಂದಿರುವ ಹೊಂದಾಣಿಕೆಯ ವರದಿಯನ್ನು ಹಾಕಲು ಕೇಳುತ್ತದೆ. ನೀವು ರೆಜ್ಯೂಮ್ ಮತ್ತು ಉದ್ಯೋಗ ವಿವರಣೆಯನ್ನು ಎರಡನ್ನೂ ಕಳುಹಿಸಿದಾಗಲೂ ಇದು ಸಂಭವಿಸುತ್ತದೆ.

**ಕಾರಣ:** JD ಪಠ್ಯ JD ಏಜೆಂಟ್‌ಗೆ ಕೆಳಸಾಗಿಸಿ ಕಳುಹಿಸಲಾಗಿಲ್ಲ. `context_mode="last_agent"` ಇದ್ದಾಗ, `resume_executor` ಮಾತ್ರ ಬಳಕೆದಾರರು ಆರಂಭಿಕ ಸಂದೇಶವನ್ನು ಕಂಡುಕೊಳ್ಳುವ ಎಕ್ಸಿಕ್ಯೂಟರ್. `RESUME_PARSER_INSTRUCTIONS` JD ಪಠ್ಯವನ್ನು ಅದರ ಔಟ್‌ಪುಟ್‌ನಲ್ಲಿ ಸೇರಿಸದಿದ್ದರೆ, JD ಏಜೆಂಟ್‌ಗೆ JD ಇಲ್ಲ, MatchingAgent ಹೊಂದಾಣಿಕೆ ಅಂಕೆ ಲೆಕ್ಕಿಸಲಾಗದು, ಮತ್ತು GapAnalyzer ಅರ್ಥರಹಿತ ಇನ್‌ಪುಟ್ ಸ್ವೀಕರಿಸುತ್ತದೆ.

**ರೋಗನಿರ್ಣಯ:**

ಸರ್ವರ್ ಲಾಗ್‌ಗಳಲ್ಲಿ MatchingAgent ಸ್ಪಾನ್ ನೋಡಿರಿ. ಇದರಲ್ಲಿ:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
ಕೆಳಕ್ಕೆ ಸಾಗಿಸುವುದು ಕೊರತೆ ಅಥವಾ ಮುರಿದುಹೋಗಿದೆ.

**ಸರಿಪಡಿಸುವುದು:** `main.py`ಯಲ್ಲಿ `RESUME_PARSER_INSTRUCTIONS` ನಲ್ಲಿ `[JOB DESCRIPTION PASS-THROUGH]` ವಿಭಾಗ ಮತ್ತು ನಿಯಮವಿದೆ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
`JOB_DESCRIPTION_INSTRUCTIONS` ನಲ್ಲಿ `[PARSED RESUME PASS-THROUGH]` ರಿಲೇ ನಿಯಮವೂ ಇದೆ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
ಯಾವುದೇ ನಿರ್ದೇಶನ ಬ್ಲಾಕ್ ಸ್ಕ್ಯಾಫೋಲ್ಡ್ ವಿಜಾರ್ಡ್‌ನ ಸ್ಥೂಲವಾಗಿದ್ದರೆ, ಅದನ್ನು [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ನ ಸಂಪೂರ್ಣ ಆವೃತ್ತಿಯಿಂದ ಬದಲಾಯಿಸಿ.

### MatchingAgent “Cannot compute fit score - no JD provided” ಎಂದು ಔಟ್‌ಪುಟ್ ಮಾಡಿ

ಇದು ಮೇಲಿನ ಅದೇ ಮೂಲ ಕಾರಣ. MatchingAgent JD ಏಜೆಂಟ್ ಔಟ್‌ಪುಟ್ ಸ್ವೀಕರಿಸಿದೆ ಆದರೆ `[PARSED RESUME PASS-THROUGH]` ವಿಭಾಗ ಕೊರತೆ ಅಥವಾ ಖಾಲಿ, ಆದರಿಂದ ಎರಡು ಪ್ರೊಫೈಲ್‌ಗಳನ್ನು ಹೋಲಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ:
1. `JOB_DESCRIPTION_INSTRUCTIONS` ರಿಲೇ ನಿಯಮವನ್ನು ಒಳಗೊಂಡಿದೆ: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` ಏಜೆಂಟ್‌ನ್ನು `[JD REQUIREMENTS]` ಮತ್ತು `[PARSED RESUME PASS-THROUGH]` ವಿಭಾಗಗಳನ್ನು ಹುಡುಕಲು ಸೂಚಿಸುತ್ತದೆ.

ಎರಡು ನಿರ್ದೇಶನ ಬ್ಲಾಸ್‌ಗಳನ್ನೂ [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ನ ಸಂಪೂರ್ಣ ಆವೃತ್ತಿ ಮೂಲಕ ಬದಲಾಯಿಸಿ.

### ಪ್ರತಿಕ್ರಿಯೆ ಎರಡು ಬಾರಿ ಕಾಣುತ್ತದೆ

**ಲಕ್ಷಣ:** GapAnalyzer ಔಟ್‌ಪುಟ್ (ಅಥವಾ ಸಂಪೂರ್ಣ ಪೈಪ್‌ಲೈನ್ ಔಟ್‌ಪುಟ್) ಏಜೆಂಟ್ ಇನ್ಸ್‌ಪೆಕ್ಟರ್ ಪ್ರತಿಕ್ರિયામાં ಎರಡು ಬಾರಿ ಕಾಣುತ್ತದೆ.

**ಕಾರಣ:** `WorkflowBuilder` ಬರುವ ಎಡ್ಜ್‌ಗಳಿಗೆ OR-ಸಮುಚ್ಛಯೆಯನ್ನು ಬಳಸುತ್ತದೆ - ಯಾವುದೇ ಪೂರ್ವ ಪ್ರಕ್ರಿಯೆಯು ಪೂರ್ಣಗೊಳ್ಳುವಷ್ಟರಲ್ಲಿ ಕೆಳಗಿನ ಎಕ್ಸಿಕ್ಯೂಟರ್ ಆಗುದು. `matching_executor` ಎರಡು ಬರುವ ಎಡ್ಜ್‌ಗಳಾಗಿದ್ದರೆ (`resume_executor` ಮತ್ತು `jd_executor`), ಅದು ಎರಡು ಬಾರಿ ಕಾಣುತ್ತದೆ: ಮೊದಲನೆಯದಾಗಿ ResumeParser ಮುಗಿದಾಗ ಮತ್ತು ಮತ್ತೊಮ್ಮೆ JD ಏಜೆಂಟ್ ಮುಗಿದಾಗ. GapAnalyzer ಕೂಡ ಎರಡು ಬಾರಿ ನಡೆಯುತ್ತದೆ.

**ಸರಿಪಡಿಸುವುದು:** ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ `WorkflowBuilder` ಗ್ರಾಫ್ ಕಟ್ಟುನಿಟ್ಟಾದ ಕ್ರಮಿಕ ಪೈಪ್‌ಲೈನ್ ಆಗಿದ್ದು ಯಾವುದೇ ಫ್ಯಾನ್-ಇನ್ ಇಲ್ಲ:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # ರೆಸ್ಯೂಮ್_ಕಾರ್ಯನಿರ್ವಹಕರಿಂದ ಅಲ್ಲ
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

ಸಿನಿಮ `.add_edge(resume_executor, matching_executor)` ಇರುವ ಲೈನನ್ನು ತೆಗೆದುಹಾಕಿ. JD ಏಜೆಂಟ್ ಔಟ್‌ಪುಟ್‌ನ `[PARSED RESUME PASS-THROUGH]` ರಿಲೇ ಈಗಾಗಲೇ MatchingAgentಗೆ ರೆಜ್ಯೂಮ್ ಪ್ರವೇಶ ನೀಡುತ್ತದೆ.

---

## ಪರಿಸರ ಮತ್ತು ಸಂರಚನಾ ಸಮಸ್ಯೆಗಳು

### `.env` ಮೌಲ್ಯಗಳು ಕಾಣದಿರುವುದು ಅಥವಾ ತಪ್ಪು

`.env` ಫೈಲ್ `PersonalCareerCopilot/` ಡೈರೆಕ್ಟರಿಯಲ್ಲಿ ಇರಬೇಕು (`main.py` ಜೊತೆಗೆ ಸಮಾನ ಮಟ್ಟದಲ್ಲಿ):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

ನಿರೀಕ್ಷಿತ `.env` ವಿಷಯ:

**ಮಾರ್ಗ A - Foundry ಕ್ಲೌಡ್:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**ಮಾರ್ಗ B - Foundry ಲೋಕಲ್:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> ಎರಡೂ ಮಾರ್ಗಗಳು `FOUNDRY_PROJECT_ENDPOINT` ಬಳಸುತ್ತವೆ. ಮೌಲ್ಯವು ವಿಭಿನ್ನ: ಕ್ಲೌಡ್ `https://` Foundry ಎಂಡ್‌ಪಾಯಿಂಟ್; ಲೋಕರ  `http://localhost:5273/v1`. ನಿಖರ ಮಾದರಿ_ALIAS ಗುರುತಿಸಲು `foundry model list` ಅನ್ನು ಚಾಲನೆ ಮಾಡಿ ಮಾರ್ಗ B ಗೆ.

> **ನಿಮ್ಮ `FOUNDRY_PROJECT_ENDPOINT` ಹುಡುಕುವುದು:** 
- VS Code ನಲ್ಲಿ **Foundry Toolkit** ಸೈಡ್‌ಬಾರ್ನಲ್ಲಿ ನಿಮ್ಮ ಪ್ರಾಜೆಕ್ಟ್ ಮೇಲೆ ರೈಟ್ ಕ್ಲಿಕ್ → **Copy Project Endpoint**.
- ಅಥವಾ [Azure Portal](https://portal.azure.com) → ನಿಮ್ಮ Foundry ಪ್ರಾಜೆಕ್ಟ್ → **Overview** → **Project endpoint**.

> **ನಿಮ್ಮ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ಹುಡುಕುವುದು:** Foundry Toolkit Sidebar ನಲ್ಲಿ ನಿಮ್ಮ ಪ್ರಾಜೆಕ್ಟ್ ವಿಸ್ತರಿಸಿ → **Models** → ಎಲ್ಲಿದ್ದರೂ ನಿಮ್ಮ ನಿಯೋಜಿತ ಮಾದರಿ ಹೆಸರು (ಉದಾ: `gpt-4.1-mini`) ಕಂಡುಕೊಳ್ಳಿ.

### ಪರಿಸರ ರೂಪಾಂತರಣ ಆದ್ಯತೆ

`main.py` ನಲ್ಲಿ `load_dotenv(override=True)` ಬಳಕೆ:

| ಆದ್ಯತೆ | ಮೂಲ | ಎರಡೂ ಸೆಟ್ ಇದ್ದರೆ ಯಾವುದು ಗೆಲ್ಲುತ್ತದೆ? |
|---------|--------|-------------------------|
| 1 (ಅತ್ಯುನ್ನತ) | `.env` ಫೈಲ್ | ಹೌದು |
| 2 | ಶೆಲ್ / ಕಂಟೇನರ್ ಪರಿಸರ ಚರ | `.env` ನಲ್ಲಿ ಅದೇ ಕೀ ಇರುವುದಿಲ್ಲದಿದ್ದಾಗ ಬಳಸುವುದು |

ಸ್ಥಳೀಯ ಅಭಿವೃದ್ಧಿಯಲ್ಲಿ `.env` ಸ್ಥಳದ ಮಾಹಿತಿ ಮೂಲ (ಎಡಿಟ್ ಮImmutable `.env` ತಕ್ಷಣ ಕಾರ್ಯಾಚರಣೆ ಮೇಲೆ ಪರಿಣಾಮ ಬೀರುತ್ತದೆ). ಆನ್‌ಲೈನ್ ನಿಯೋಜನೆಯಲ್ಲಿ, Foundry ಕಂಟೇನರ್ ಮಟ್ಟದಲ್ಲಿ ಪರಿಸರ ಚರಗಳನ್ನು ಎಂಜೆಕ್ಟ್ ಮಾಡುತ್ತದೆ; `.env` ಈ ಪ್ರಯೋಗದಲ್ಲಿ ನಿಯೋಜಿತ ಚಿತ್ರ ಭಾಗವಾಗಿಲ್ಲದಿರಲಿ, ಎಂಜೆಕ್ಟ್ ಮಾಡಿದ ಮೌಲ್ಯಗಳನ್ನು ಬಳಸಲಾಗುತ್ತದೆ.

---

## ಆವೃತ್ತಿ ಹೊಂದಾಣಿಕೆ

### ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿ ಮ್ಯಾಟ್ರಿಕ್ಸ್

ಬಹು-ಏಜೆಂಟ್ ವರ್ಕ್ಫ್ಲೋಗೆ ನಿಶ್ಚಿತ ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿಗಳ ಅಗತ್ಯವಿದೆ. ಹೊಂದಿಕೆಗೆ ಇಲ್ಲದ ಆವೃತ್ತಿಗಳು ರನ್ ಟೈಮ್ ದೋಷಗಳಿಗೆ ಕಾರಣವಾಗುತ್ತವೆ.

| ಪ್ಯಾಕೇಜ್ | ಅಗತ್ಯ ಆವೃತ್ತಿ | ಪರಿಶೀಲನೆ ಕಮಾನ್ಡ್ |
|---------|-----------------|--------------------|
| `agent-framework-foundry` | ಇತ್ತೀಚಿನ | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ಇತ್ತೀಚಿನ | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ಇತ್ತೀಚಿನ | `pip show debugpy` |
| ಪೈಥಾನ್ | 3.12+ | `python --version` |

### ಸಾಮಾನ್ಯ ಆವೃತ್ತಿ ದೋಷಗಳು

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ಸರಿಪಡಿಸಿ: ಏಜೆಂಟ್-ಫ್ರೇಮ್‌ವರ್ಕ್-ಫೌಂಡ್ರಿ ಅನ್ನು ಮರುಸ್ಥಾಪಿಸಿ
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ಸರಿಪಡಿಸಿ: mcp ಪ್ಯಾಕೇಜ್ ಅನ್ನುನವೀಕರಿಸಿ
pip install mcp --upgrade
```

### ಎಲ್ಲಾ ಆವೃತ್ತಿಗಳನ್ನು ಒಂದೇ ಸಮಯದಲ್ಲಿ ಪರಿಶೀಲಿಸಿ

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

ನಿರೀಕ್ಷಿತ ಔಟ್‌ಪುಟ್:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## ನಿಯೋಜನೆ ಸಮಸ್ಯೆಗಳು

### ನಿಯೋಜನೆಯ ನಂತರ ಕಂಟೇನರ್ ಪ್ರಾರಂಭವಾಗುತ್ತಿಲ್ಲ

1. **ಕಂಟೇನರ್ ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ:**
   - **Foundry Toolkit**.sidebar ತೆರೆಯಿರಿ → **Hosted Agents (Preview)** ವಿಸ್ತರಿಸಿ → ನಿಮ್ಮ ಏಜೆಂಟ್ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ → ಆವೃತ್ತಿ ವಿಸ್ತರಿಸಿ → **Container Details** → **Logs**.
   - ಪೈಥಾನ್ ಸ್ಟಾಕ್ ಟ್ರೇಸ್ ಅಥವಾ ಮಾಯವಾದ ಮಾಯಾಜಾಲ ದೋಷ ಹುಡುಕಿ.

2. **ಸಾಮಾನ್ಯ ಕಂಟೇನರ್ ಪ್ರಾರಂಭ ವೈಫಲ್ಯಗಳು:**

   | ಲಾಗ್ ದೋಷ | ಕಾರಣ | ಸರಿಪಡಿಸುವುದು |
   |------------|-------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` ಪ್ಯಾಕೇಜ್ ಇಲ್ಲ | ಪ್ಯಾಕೇಜ್ ಸೇರಿಸಿ, ಮರು-ನಿಯೋಜನೆ ಮಾಡಿರಿ |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` ಅಥವಾ `.env` ಪರಿಸರ ಚರ ಸೆಟ್ ಇಲ್ಲ | `agent.yaml` → `environment_variables` ವಿಭಾಗ (ಆನ್‌ಲೋಡ್) ಅಥವಾ `.env` (ಸ್ಥಳೀಯ) ನವೀಕರಿಸಿ |
   | `azure.identity.CredentialUnavailableError` | ನಿರ್ವಹಿತ ಗುರುತು تنظیم ಇಲ್ಲ | Foundry ಸ್ವಯಂಚಾಲಿತವಾಗಿ ನಿಗದಿಪಡಿಸುತ್ತದೆ - ವಿಸ್ತರಣೆ ಮೂಲಕ ನಿಯೋಜನೆ ಮಾಡುತ್ತಿದ್ದೀರಿ ಎಂದು ಖಚಿತಪಡಿಸಿ |
   | `OSError: port 8088 already in use` | ಡಾಕರ್‌ಫೈಲ್ ತಪ್ಪು ಪೋರ್ಟ್ ಎಕ್ಸ್‌ಪೋಸ್ ಅಥವಾ ಪೋರ್ಟ್ ಸಂಧಿ | `EXPOSE 8088` ಡಾಕರ್‍ಫೈಲ್ ಮತ್ತು `CMD ["python", "main.py"]` ಪರಿಶೀಲಿಸಿ |
   | ಕಂಟೇನರ್ ಕೋಡ್ 1 ಸಹಿತ ನಿಷ್ಕ್ರಮಣ | `main()` ನಲ್ಲಿ ಹಿಡಿದಿಡದ ಹೊರತುಪಡಿಸುವಿಕೆ | ಮೊದಲು ಸ್ಥಳೀಯವಾಗಿ ಪರೀಕ್ಷಿಸಿ ([ಮಾಡ್ಯೂಲ್ 5](05-test-locally.md)) ದೋಷಗಳನ್ನು ಹಿಡಿಯಿರಿ ನಂತರ ನಿಯೋಜಿಸಿ |

3. **ಸರಿಪಡಿಸಿ ಮರು-ನಿಯೋಜಿಸಿ:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → ಅದೇ ಏಜೆಂಟ್ ಆಯ್ಕೆಮಾಡಿ → ಹೊಸ ಆವೃತ್ತಿ ನಿಯೋಜಿಸಿ.

### ನಿಯೋಜನೆ ಸಮಯ ಹೆಚ್ಚು ತೆಗೆದುಕೊಳ್ಳುತ್ತದೆ

ಬಹು-ಏಜೆಂಟ್ ಕಂಟೇನರ್‌ಗಳು ಪ್ರಾರಂಭ ಮಾಡಲು ಹೆಚ್ಚು ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುತ್ತವೆ ಏಕೆಂದರೆ ಪ್ರಾರಂಭದಾಗ 4 ಏಜೆಂಟ್ ಕಾರ್ಯಪ್ರತಿನಿಧಿಗಳನ್ನು ಸೃಷ್ಟಿಸುತ್ತವೆ. ಸಾಮಾನ್ಯ ಪ್ರಾರಂಭ ಸಮಯಗಳು:

| ಹಂತ | ನಿರೀಕ್ಷಿತ ಅವಧಿ |
|-------|----------------|
| ಕಂಟೇನರ್ ಇಮೇಜ್ ನಿರ್ಮಾಣ | 1-3 ನಿಮಿಷಗಳು |
| ಇಮೇಜ್ ACR ಗೆ ಒತ್ತಿ | 30-60 ಸೆಕೆಂಡುಗಳು |
| ಕಂಟೇನರ್ ಪ್ರಾರಂಭ (ಏಕ ಏಜೆಂಟ್) | 15-30 ಸೆಕೆಂಡುಗಳು |
| ಕಂಟೇನರ್ ಪ್ರಾರಂಭ (ಬಹು-ಏಜೆಂಟ್) | 30-120 ಸೆಕೆಂಡುಗಳು |
| ಏಜೆಂಟ್ ಪ್ಲೇಗ್ರೌಂಡಿನಲ್ಲಿ ಲಭ್ಯವಿದೆ | "ಪ್ರಾರಂಭಿಸಲಾಗಿದೆ" ನಂತರ 1-2 ನಿಮಿಷಗಳು |

> "Pending" ಸ್ಥಿತಿ 5 ನಿಮಿಷಗಳಿಗಿಂತ ಹೆಚ್ಚು ಉಳಿದರೆ, ಕಂಟೇನರ್ ಲಾಗ್‌ಗಳು ದೋಷಗಳಿಗೆ ಪರಿಶೀಲಿಸಿ.

---

## RBAC ಮತ್ತು ಅನುಮತಿ ಸಮಸ್ಯೆಗಳು

### `403 Forbidden` ಅಥವಾ `AuthorizationFailed`

ನೀವು ನಿಮ್ಮ Foundry ಪ್ರಾಜೆಕ್ಟ್‌ನಲ್ಲಿ **[Foundry User](https://aka.ms/foundry-ext-project-role)** ಪಾತ್ರ ಹೊಂದಿರಬೇಕು (ಹಿಂದೆ **Azure AI User** ಎಂದು ಕರೆಯಲ್ಪಟ್ಟಿದ್ದು - ಪಾತ್ರ ID ಬದಲಾಗಿಲ್ಲ):

1. [Azure Portal](https://portal.azure.com) ಗೆ ಹೋಗಿ → ನಿಮ್ಮ Foundry **ಪ್ರಾಜೆಕ್ಟ್** ಸಂಪನ್ಮೂಲ.
2. ಕ್ಲಿಕ್ ಮಾಡಿ **Access control (IAM)** → **Role assignments**.
3. ನಿಮ್ಮ ಹೆಸರು ಹುಡುಕಿ → ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ **Foundry User** (ಅಥವಾ ಹಳೆಯ ಲೇಬಲ್ **Azure AI User**) ಪಟ್ಟಿ ಇದೆ.
4. ಇಲ್ಲದೆ ಇದ್ದರೆ: **Add** → **Add role assignment** → **Foundry User** ಹುಡುಕಿ → ನಿಮ್ಮ ಖಾತೆಗೆ ನಿಯೋಜಿಸಿ.

ವಿವರಗಳಿಗೆ [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ಡಾಕ್ಯುಮೆಂಟೇಶನ್ ನೋಡಿ.

### ಮಾದರಿ ನಿಯೋಜನೆ ತಲುಪಬಹುದಿಲ್ಲ

ಏಜೆಂಟ್ ಮಾದರಿ-ಸಂಬಂಧಿತ ದೋಷಗಳನ್ನು ನೀಡಿದರೆ:

1. ಮಾದರಿ ನಿಯೋಜಿಸಲಾಗಿದೆ ಎಂಬುದು ಪರಿಶೀಲಿಸಿ: Foundry Sidebar → ಪ್ರಾಜೆಕ್ಟ್ ವಿಸ್ತರಿಸಿ → **Models** → `gpt-4.1-mini` (ಅಥವಾ ನಿಮ್ಮ ಮಾದರಿ) ಸ್ಥಿತಿ **Succeeded** ಇದೆಯೆಂದು ನೋಡಿರಿ.
2. ನಿಯೋಜನೆಯ ಹೆಸರು ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ ಎಂದು ಪರಿಶೀಲಿಸಿ: `.env` (ಅಥವಾ `agent.yaml`)ಯಲ್ಲಿನ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ನಲ್ಲಿಗೆ ಹೋಲಿಸಿ Sidebar ನಲ್ಲಿ ನಿಖರ ನಿಯೋಜನಾ ಹೆಸರನ್ನು ನೋಡಿ.
3. ನಿಯೋಜನೆ ಅವಧಿ ಮುಗಿದಿದ್ದರೆ (ಫ್ರೀ ಟಿಯರ್): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) ನಿಂದ ಮರು-ನಿಯೋಜಿಸಿ (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local ಸಮಸ್ಯೆಗಳು (ಮಾರ್ಗ B)

### Foundry Local ಸೇವೆ ಚಾಲನೆಯಲ್ಲಿಲ್ಲ

```powershell
# ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ
foundry local status

# ನಿಲ್ಲಿಸಿದ್ದರೆ ಸೇವೆಯನ್ನು ಪ್ರಾರಂಭಿಸಿ
foundry local start
```

| ಲಕ್ಷಣ | ಕಾರಣ | ಸರಿಪಡಿಸುವುದು |
|---------|-------|-----------|
| ಆರೋಗ್ಯ ಪರಿಶೀಲನೆ `503` ನೀಡುತ್ತದೆ | ಸೇವೆ ಪ್ರಾರಂಭವಾಗಿಲ್ಲ | `foundry local start` ಅಥವಾ Foundry Toolkit Sidebarನಲ್ಲಿ **Start** ಕ್ಲಿಕ್ ಮಾಡಿ |
| ಆರೋಗ್ಯ ಪರಿಶೀಲನೆ ಟೈಮ್ ಔಟ್ ಆಗಿದೆ | ಮಾದರಿ ಇನ್ನೂ ಲೋಡ್ ಆಗುತ್ತಿದೆ | ಪ್ರಾರಂಭನಂತರ 30–60 ಸೆಕೆಂಡು ಕಾಯಿರಿ; ದೊಡ್ಡ ಮಾದರಿಗಳು ಹೆಚ್ಚಿನ ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುತ್ತವೆ |
| `/v1/health` ನಲ್ಲಿ `StatusCode: 404` | ತಪ್ಪು ಪೋರ್ಟ್ | ಡೀಫಾಲ್ಟ್ `5273`. ನಿಖರ ಪೋರ್ಟ್ ಗಾಗಿ `foundry local status` ನೋಡಿ |
| ಸಂಪನ್ಮೂಲ ಸಮರ್ಪಕವಿಲ್ಲ | Foundry Local ಗೆ ~4 GB RAM ನವಿರುದ್ಧ ಸ್ಥಾನ ಅಗತ್ಯವಿದೆ | ಇತರೆ ಅಪ್ಲಿಕೇಶನ್‌ಗಳನ್ನು ಮುಚ್ಚಿ |
| ಮಾದರಿ ಡೌನ್ಲೋಡ್ ವಿಫಲವಾಯಿತು | ಕಡಿಮೆ ಡಿಸ್ಕ್ ಜಾಗ | ಮಾದರಿಗಳು 2–8 GB. ಜಾಗ ತೆರವು ಮಾಡಿರಿ, ನಂತರ `foundry model pull <name>` ರನ್ನ ಮಾಡಲು |

### ಮಾದರಿ ಹೆಸರು ಹೊಂದಾಣಿಕೆ ದೋಷ

```powershell
# ಡೌನ್‌ಲೋಡ್ ಮಾಡಿದ ಮಾದರಿಗಳು ಮತ್ತು ಅವುಗಳ ನಿಖರವಾದ ಬದಲಾವಣೆ ಹೆಸರುಗಳನ್ನು ಪಟ್ಟಿ ಮಾಡಿ
foundry model list
```

`.env` ನಲ್ಲಿ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ನಿಖರವಾಗಿ ತೋರಿಸಿದ ಅಲಿಯಾಸ್ ಆಗಿರಲಿ (ಉದಾ: `phi-4-mini`, `Phi-4-mini` ಅಲ್ಲ).

### ಸ್ಥಳೀಯ ಚಾಲನೆ (ಮಾರ್ಗ B) ನಲ್ಲಿ `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'`

ಲ್ಯಾಬ್ ನ `main.py` `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` ಬಳಕೆ ಮಾಡುತ್ತದೆ. Foundry Local ಈ ಚರವನ್ನು ಸ್ಥಳೀಯ ಸೇವೆಯ ಕಡೆಗೆ ಸೂಚಿಸಬೇಕು - `AZURE_AI_PROJECT_ENDPOINT` ಅಲ್ಲ. ನಿಮ್ಮ `.env` ಇದನ್ನು ಹೊಂದಿರಲಿ:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP ಟೂಲ್ ಇನ್ನೂ ಹೊರಗಡೆ ಕರೆ ಮಾಡುತ್ತದೆ (ಮಾರ್ಗ B)

ಇದು ನಿರೀಕ್ಷಿತ. `search_microsoft_learn_for_plan` ಟೂಲ್ `https://learn.microsoft.com/api/mcp` ನಿಂದ ಅಧ್ಯಯನ ಸಂಪನ್ಮೂಲಗಳನ್ನು ಪಡೆಯುತ್ತದೆ. **ಕೌಶಲ ಹೆಸರು ಪ್ರಶ್ನೆ ಮಾತ್ರ** ನೆಟ್ವರ್ಕ್ ಮೂಲಕ ಸಾಗುತ್ತದೆ - ರೆಜ್ಯೂಮ್ ಮತ್ತು JD ಪಠ್ಯ ಸಂಪೂರ್ಣವಾಗಿ ನಿಮ್ಮ ಸಾಧನದಲ್ಲಿ ಪ್ರಕ್ರಿಯೆಗೆ ಒಳಗಾಗಿ ಇರುತ್ತದೆ ಮತ್ತು ಸಂವಹನವಾಗುವುದಿಲ್ಲ. ಸಂಪೂರ್ಣ ಆಫ್‌ಲೈನ್ ಕಾರ್ಯಾಚರಣೆ ಬೇಕಿದ್ದರೆ, ಟೂಲ್‌ನಲ್ಲಿ ತಲುಪದಾಗ ಸ್ಥಿರ `learn.microsoft.com` URL ನೀಡುವ `try/except` ಬ್ಯಾಕ್ಅಪ್ ಸೇರಿಸಿ.

---

## ಸಹಾಯ ಪಡೆಯುವುದು

ಮೇಲಿನ ಸರಿಪಡಿಸುವ ಪ್ರಯತ್ನಗಳ ನಂತರ ನೀವು ಸಿಲುಕಿ ಹೋದರೆ:

1. **ಸರ್ವರ್ ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ** - ದೊಡ್ಡದಾದ ದೋಷಗಳು ಪೈಥಾನ್ ಸ್ಟಾಕ್ ಟ್ರೇಸ್ ನೀಡುತ್ತವೆ. ಸಂಪೂರ್ಣ ಟ್ರೇಬ್ರೈಸ್ ಓದಿ.
2. **ದೋಷ ಸಂದೇಶ ಹುಡುಕಿ** - ದೋಷ ಪಠ್ಯವನ್ನು ನಕಲಿಸಿ [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) ನಲ್ಲಿ ಹುಡುಕಿ.
3. **ಇಷ್ಯೂ ತೆರೆಯಿರಿ** - [ ವರ್ಕ್‌ಶಾಪ್ ರೆಪೊ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) ನಲ್ಲಿ ಇಷ್ಯೂ ಫೈಲ್ ಮಾಡಿ:
   - ದೋಷ ಸಂದೇಶ ಅಥವಾ ಸ್ಕ್ರೀನ್‌ಶಾಟ್
   - ನಿಮ್ಮ ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿಗಳು (`pip list | Select-String "agent-framework"`)
   - ನಿಮ್ಮ ಪೈಥಾನ್ ಆವೃತ್ತಿ (`python --version`)
   - ಸಮಸ್ಯೆ ಸ್ಥಳೀಯ ಅಥವಾ ನಿಯೋಜನೆಯ ಬಳಿಕವಾಗಿದೆಯೇ ಎನ್ನುವುದು

---

### ಪರಿಶೀಲನೆ ಬಿಂದು

- [ ] `.env` ಸಂರಚನಾ ಸಮಸ್ಯೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಸರಿಪಡಿಸುವುದು ಗೊತ್ತು
- [ ] ಅಗತ್ಯ ಮ್ಯಾಟ್ರಿಕ್ಸ್‍ಗೆ ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿಗಳನ್ನು ಪರಿಶೀಲಿಸುವ ಸಾಧ್ಯತೆ ಇದೆ
- [ ] ನಿಯೋಜನೆ ವೈಫಲ್ಯಗಳಿಗೆ ಕಂಟೇನರ್ ಲಾಗ್ ಪರಿಶೀಲಿಸುವುದು ತಿಳಿದಿದೆ
- [ ] ನೀವು Azure ಪೋರ್ಟಲ್‌ನಲ್ಲಿ RBAC ಪಾತ್ರಗಳನ್ನು ಪರಿಶೀಲಿಸಬಹುದು

---

**ಹಿಂದಿನ:** [07 - ಪ್ಲೇಗ್ರೌಂಡ್ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ](07-verify-in-playground.md) · **ಮುಂದಿನ:** [09 - ಸಮಾರೋಪ →](09-summary.md) · **ಮನೆ:** [ಲ್ಯಾಬ್ 02 README](../README.md) · [ವರ್ಕ್‌ಶಾಪ್ ಮನೆ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ಅಸ್ವೀಕಾರ**:
ಈ ದಸ್ತಾವೇಜು AI ಅನುವಾದ ಸೇವೆ [Co-op Translator](https://github.com/Azure/co-op-translator) ಬಳಸಿ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ನಿಖರತೆಯನ್ನು ಸಾಧಿಸಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದರೂ, ದಯವಿಟ್ಟು ಗಮನಿಸಿ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ದೋಷಗಳು ಅಥವಾ ಅಸಡ್ಡೆಗಳು ಇರಬಹುದು. ಮೂಲ ಭಾಷೆಯಲ್ಲಿರುವ ಮೂಲ ದಸ್ತಾವೇಜು ಪ್ರಾಮಾಣಿಕ ಮೂಲವೆಂದು ಪರಿಗಣಿಸಬೇಕು. ಪ್ರಮುಖ ಮಾಹಿತಿಗಾಗಿ, ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ. ಈ ಅನುವಾದವನ್ನು ಬಳಸುವ ಮೂಲಕ ಉಂಟಾಗುವ ಯಾವುದೇ ತಪ್ಪು ಅರ್ಥಗಳ ಅಥವಾ ತಪ್ಪು ವ್ಯಾಖ್ಯಾನಗಳ ಬಗ್ಗೆ ನಾವು ಹೊಣೆಗಾರರಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->