# Module 8 - ತೊಂದರೆ ನಿವಾರಣೆ (ಬহು ಏಜೆಂಟ್)

ಈ ಮೋಡ್ಯೂಲ್ ಬಹು ಏಜೆಂಟ್ ಕೆಲಸಗಾರ ಪ್ರವಾಹಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಸಾಮಾನ್ಯ ದೋಷಗಳು, ಸರಿಪಡಿಸುವಿಕೆಗಳು ಮತ್ತು ಡಿಬಗ್ ತಂತ್ರಗಳನ್ನು ಒಳಗೊಂಡಿದೆ. ಸಾಮಾನ್ಯ Foundry ನಿಯೋಜನೆ ಸಮಸ್ಯೆಗಳಿಗೆ, [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md) ಅನ್ನು ಸಹ ನೋಡಿ.

---

## ತ್ವರಿತ ಉಲ್ಲેખ: ದೋಷ → ಸರಿಪಡಿಸುವಿಕೆ

| ದೋಷ / ಲಕ್ಷಣ | ಸಾಧ್ಯತೆ ಕಾರಣ | ಸರಿಪಡಿಸುವಿಕೆ |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` ಫೈಲ್ ಇಲ್ಲ ಅಥವಾ ಮೌಲ್ಯಗಳು ಸೆಟ್ ಆಗಿಲ್ಲ | `PROJECT_ENDPOINT=<ನಿಮ್ಮ-ಎಂಡ್‌ಪಾಯಿಂಟ್>` ಮತ್ತು `MODEL_DEPLOYMENT_NAME=<ನಿಮ್ಮ ಮಾದರಿ>` ಯೊಂದಿಗೆ `.env` ರಚಿಸಿ |
| `ModuleNotFoundError: No module named 'agent_framework'` | ವರ್ಚುವಲ್ ಪರಿಸರ ಸಕ್ರಿಯಗೊಂಡಿಲ್ಲ ಅಥವಾ ಅವಲಂಬನೆಗಳು ಸ್ಥಾಪಿಸಲಿಲ್ಲ | `.\.venv\Scripts\Activate.ps1` ರನ್ನಿಂ ಮಾಡಿ ನಂತರ `pip install -r requirements.txt` ರನ್ನಿಂ ಮಾಡಿ |
| `ModuleNotFoundError: No module named 'mcp'` | MCP ಪ್ಯಾಕೇಜ್ ಸ್ಥಾಪಿಸಲಿಲ್ಲ (requirements ನಲ್ಲಿ ಇಲ್ಲ) | `pip install mcp` ರನ್ನಿಂ ಮಾಡಿ ಅಥವಾ `requirements.txt` ನಲ್ಲಿ ಇದನ್ನು ಟ್ರಾನ್ಸಿಟಿವ್ ಅವಲಂಬನೆ ಆಗಿ ಸೆಟ್ ಮಾಡಿರುವುದನ್ನು ಪರಿಶೀಲಿಸಿ |
| ಏಜೆಂಟ್ ಆರಂಭವಾಗುತ್ತದೆ ಆದರೆ ಖಾಲಿ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ನೀಡುತ್ತದೆ | `output_executors` ಹೊಂದಾಣಿಕೆ ತಪ್ಪಿದ್ದರೆ ಅಥವಾ ಎಡ್ಜ್‌ಗಳು ಇಲ್ಲದಿದ್ದರೆ | `output_executors=[gap_analyzer]` ಮತ್ತು `create_workflow()` ಯಲ್ಲಿನ ಎಲ್ಲಾ ಎಡ್ಜ್‌ಗಳು ಇರುವುದು ಖಚಿತಪಡಿಸಿ |
| ಕೇವಲ 1 gap ಕಾರ್ಡ್ ಮಾತ್ರ (ಮಿಗಿಲೊಂದು ಇಲ್ಲ) | GapAnalyzer ಸೂಚನೆಗಳು ಅಪೂರ್ಣ | `GAP_ANALYZER_INSTRUCTIONS` ನಲ್ಲಿ `CRITICAL:` ಪ್ಯಾರಾಗ್ರಾಫ್ ಸೇರಿಸಿ - [Module 3](03-configure-agents.md) ನೋಡಿ |
| ಫಿಟ್ ಸ್ಕೋರ್ 0 ಅಥವಾ ಲಭ್ಯವಿಲ್ಲ | MatchingAgentಗೆ ಮೇಲ್ಭಾಗದ ಡೇಟಾ ಬಂದಿಲ್ಲ | `add_edge(resume_parser, matching_agent)` ಮತ್ತು `add_edge(jd_agent, matching_agent)` ಎರಡೂ ಇದ್ದವು ಖಚಿತಪಡಿಸಿ |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP ಸರ್ವರ್ ಉಪಕರಣ ಕರೆ ನಿರಾಕರಿಸಿದೆ | ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕವನ್ನು ಪರಿಶೀಲಿಸಿ. ಬ್ರೌಸರ್‌ನಲ್ಲಿ `https://learn.microsoft.com/api/mcp` ತೆರೆಯುವ ಪ್ರಯತ್ನಮಾಡಿ. ಮರುಪ್ರಯತ್ನಿಸಿ |
| output ನಲ್ಲಿ ಯಾವುದೇ Microsoft Learn URLs ಇಲ್ಲ | MCP ಉಪಕರಣ ನೋಂದಣಿಯಾಗಿಲ್ಲ ಅಥವಾ ಎಂಡ್‌ಪಾಯಿಂಟ್ ತಪ್ಪಾಗಿದೆ | GapAnalyzer ನಲ್ಲಿರುವ `tools=[search_microsoft_learn_for_plan]` ಮತ್ತು`MICROSOFT_LEARN_MCP_ENDPOINT` ಸರಿಯಾಗಿದೆ ಎಂದು ಪರಿಶೀಲಿಸಿ |
| `Address already in use: port 8088` | ಇನ್ನೊಂದು ಪ್ರಕ್ರಿಯೆ 8088 ಪೋರ್ಟ್ ಬಳಸುತ್ತಿದೆ | `netstat -ano \| findstr :8088` (Windows) ಅಥವಾ `lsof -i :8088` (macOS/Linux) ರನ್ನಿಂ ಮಾಡಿ ಮತ್ತು ವಿರುದ್ಧ ಪ್ರಕ್ರಿಯೆಯನ್ನು ನಿಲ್ಲಿಸಿ |
| `Address already in use: port 5679` | Debugpy ಪೋರ್ಟ್ ಸಂಧ್ಯೆ | ಇತರೆ ಡೀಬಗ್ ಸೆಷನ್‌ಗಳನ್ನು ನಿಲ್ಲಿಸಿ. ಪ್ರಕ್ರಿಯೆಯನ್ನೇ ಹುಡುಕಿ ಮತ್ತು ಕೊಲ್ಲಲು `netstat -ano \| findstr :5679` ರನ್ನಿಂ ಮಾಡಿ |
| ಏಜೆಂಟ್ ಇನ್ಸ್ಪೆಕ್ಟರ್ ತೆರೆಯುವುದಿಲ್ಲ | ಸರ್ವರ್ ಸಂಪೂರ್ಣ ಆರಂಭವಾಗಿಲ್ಲ ಅಥವಾ ಪೋರ್ಟ್ ಕಾನ್ಫ್ಲಿಕ್ಟ್ | "Server running" ಲಾಗ್‌ಗಾಗಿ ಕಾಯಿರಿ. ಪೋರ್ಟ್ 5679 ಲಭ್ಯವಿರುವುದನ್ನು ಪರಿಶೀಲಿಸಿ |
| `azure.identity.CredentialUnavailableError` | Azure CLI ಗೆ ಲಾಗಿನ್ ಆಗಿಲ್ಲ | `az login` ರನ್ನಿಂ ಮಾಡಿ ನಂತರ ಸರ್ವರ್ ಮರುಪ್ರಾರಂಭ ಮಾಡಿ |
| `azure.core.exceptions.ResourceNotFoundError` | ಮಾದರಿ ನಿಯೋಜನೆ ಇಲ್ಲ | ನಿಮ್ಮ Foundry ಪ್ರಾಜೆಕ್ಟ್‌ನಲ್ಲಿ ನಿಯೋಜಿಸಲಾದ ಮಾದರಿ `MODEL_DEPLOYMENT_NAME` ಹೊಂದಾಣಿಕೆ ಹೊಂದಿದ್ದೇನಾ ಎಂದು ಪರಿಶೀಲಿಸಿ |
| ನಿಯೋಜನೆಯ ನಂತರ ಕನ್ಟೈನರ್ ಸ್ಥಿತಿ "Failed" | ಆರಂಭದಲ್ಲಿ ಕನ್ಟೈನರ್ ಕ್ರ್ಯಾಶ್ | Foundry ಸೈಡ್ಬಾರ್‌ನಲ್ಲಿನ ಕನ್ಟೈನರ್ ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. ಸಾಮಾನ್ಯ: ಪರಿಸರ ಚರಗಳು ಇಲ್ಲ ಅಥವಾ ಆಮದು ದೋಷ |
| ನಿಯೋಜನೆ > 5 ನಿಮಿಷ "Pending" ತೋರಿಸುತ್ತದೆ | ಕನ್ಟೈನರ್ ಪ್ರಾರಂಭಿಸಲು ಸಮಯ ಹೆಚ್ಚು ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದೆ ಅಥವಾ ಸಂಪನ್ಮೂಲ ಮಿತಿ | ಬಹು ಏಜೆಂಟ್ (4 ಏಜೆಂಟ್ ಇನ್ಸ್‌ಟಾನ್ಸ್‌ಗಳು ಸೃಷ್ಟಿ) ಗೆ 5 ನಿಮಿಷ ಕಾಯಿರಿ. ಇನ್ನೂ ಪೆಂಡಿಂಗ್ ಇದ್ದರೆ ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ |
| `ValueError` from `WorkflowBuilder` | ಅಗತ್ಯವಿಲ್ಲದ ಗ್ರಾಫ್ ಕಾಂಫಿಗರೇಶನ್ | `start_executor` ಸೆಟ್ ಆಗಿದೆಯೇ, `output_executors` ಒಂದು ಪಟ್ಟಿ ಆಗಿದೆಯೇ ಮತ್ತು ಸುತ್ತುವ ನೆಲೆ ಎಡ್ಜ್‌ಗಳು ಇಲ್ಲವೇ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ |

---

## ಪರಿಸರ ಮತ್ತು ಕಾನ್ಫಿಗರೇಶನ್ ಸಮಸ್ಯೆಗಳು

### `.env` ಮೌಲ್ಯಗಳು ಕಡಿಮೆಯಾಗಿರುವುದು ಅಥವಾ ತಪ್ಪಾಗಿದೆ

`.env` ಫೈಲ್ `PersonalCareerCopilot/` ಡೈರೆಕ್ಟರಿಯಲ್ಲಿರಬೇಕು (`main.py` ನೊಡನೆ ಸಮಮಟ್ಟದಲ್ಲಿ):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

ನಿರೀಕ್ಷಿತ `.env` ವಿಷಯ:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **ನಿಮ್ಮ PROJECT_ENDPOINT ಅನ್ನು ಹೇಗೆ ಕಂಡುಹಿಡಿಯುವುದು:**  
- VS Code ನಲ್ಲಿ **Microsoft Foundry** Sidebar ತೆರೆಯಿರಿ → ನಿಮ್ಮ ಪ್ರಾಜೆಕ್ಟ್ ಮೇಲೆ ರೈಟ್ ಕ್ಲಿಕ್ ಮಾಡಿ → **Copy Project Endpoint**.  
- ಅಥವಾ [Azure Portal](https://portal.azure.com) → ನಿಮ್ಮ Foundry ಪ್ರಾಜೆಕ್ಟ್ → **Overview** → **Project endpoint** ನೋಡಿ.

> **ನಿಮ್ಮ MODEL_DEPLOYMENT_NAME ನೋಡುವುದು:** Foundry Sidebar ನಲ್ಲಿ ನಿಮ್ಮ ಪ್ರಾಜೆಕ್ಟ್ ವಿಸ್ತರಿಸಿ → **Models** → ನಿಯೋಜಿಸಲಾದ ಮಾದರಿ ಹೆಸರನ್ನು (ಉದಾ: `gpt-4.1-mini`) ಹುಡುಕಿ.

### Env var ಆದ್ಯತೆ

`main.py` ಯಲ್ಲಿ `load_dotenv(override=False)` ಬಳಕೆಗೊಳಿಸಲಾಗಿದೆ, ಅಂದರೆ:

| ಆದ್ಯತೆ | ಮೂಲ | ಎರಡೂ ಸೆಟ್ ಆಗಿದ್ದರೆ ಯಾರು ಗೆಲುವಾಗುತ್ತಾನೆ? |
|----------|--------|----------------------------------------------|
| 1 (ಗರಿಷ್ಠ) | ಶೆಲ್ ಪರಿಸರ ಚರ | ಹೌದು |
| 2 | `.env` ಫೈಲ್ | ಕೇವಲ ಶೆಲ್ ವರ್ ಸೆಟ್ ಆಗದಿದ್ದರೆ |

ಅಂದರೆ Foundry ರನ್‌ಟೈಮ್ ಇನ್‌ವೈರಾನ್‌ಮೆಂಟ್ ವಾರ್ (ಅವನಿಯೋಜನೆಗೆ `agent.yaml` ನಲ್ಲಿ ಆಯ್ಕೆಮಾಡಲಾಗುತ್ತದೆ) `.env` ಮೌಲ್ಯಗಳಿಗಿಂತ ಮೇಲುಗೈ ಹೊಂದಿದ್ದು, ಹಾಕಲ್ಪಟ್ಟ ಸಮಯದಲ್ಲಿ ಅನ್ವಯಿಸುತ್ತದೆ.

---

## ಆವೃತ್ತಿ ಹೊಂದಾಣಿಕೆ

### ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿ ಮ್ಯಾಟ್ರಿಕ್ಸ್

ಬಹು ಏಜೆಂಟ್ ಕೆಲಸಗಾರ ಪ್ರವಾಹವು ನಿರ್ದಿಷ್ಟ ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿಗಳನ್ನು ಅಗತ್ಯಪಡಿಸುತ್ತದೆ. ಮಿಸ್‌ಮ್ಯಾಚ್ ಮಾಡಿದ ಆವೃತ್ತಿಗಳು ರನ್-ಟೈಮ್ ದೋಷಗಳನ್ನು ಉಂಟುಮಾಡಬಹುದು.

| ಪ್ಯಾಕೇಜ್ | ಅಗತ್ಯ ಆವೃತ್ತಿ | ಪರಿಶೀಲನಾ ಆಜ್ಞೆ |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | ಇತ್ತೀಚಿನ ಪ್ರೀ-ರಿಲೀಸ್ | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### ಸಾಮಾನ್ಯ ಆವೃತ್ತಿ ದೋಷಗಳು

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ಸರಿಪಡಿಸಿ: ಆರ್‌ಸಿ3 ಗೆ ಅಪ್‌ಗ್ರೇಡ್ ಮಾಡಿ
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` ಸಿಗುತ್ತಿಲ್ಲ ಅಥವಾ ಇನ್ಸ್ಪೆಕ್ಟರ್ ಹೊಂದಾಣಿಕೆ ಇಲ್ಲ:**

```powershell
# ಸಿದ್ದಿ: --pre ಫ್ಲ್ಯಾಗ್‌ ಜೊತೆಗೆ ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಿ
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ದुरಸ್ತಿ: ಎಂಸಿಪಿ ಪ್ಯಾಕೇಜ್ ಅನ್ನು ಅಪ್ಡೇಟ್ ಮಾಡಿ
pip install mcp --upgrade
```

### ಎಲ್ಲ ಆವೃತ್ತಿಗಳನ್ನು ಒಂದೇ ಸಲ ಪರಿಶೀಲಿಸಿ

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

ನಿರೀಕ್ಷಿತ ಔಟ್‌ಪುಟ್:

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

## MCP ಉಪಕರಣ ಸಂಬಂಧಿ ಸಮಸ್ಯೆಗಳು

### MCP ಉಪಕರಣ ಯಾವುದೇ ಫಲಿತಾಂಶ ನೀಡದಿರುವುದು

**ಲಕ್ಷಣ:** Gap ಕಾರ್ಡ್‌ಗಳಲ್ಲಿ "No results returned from Microsoft Learn MCP" ಅಥವಾ "No direct Microsoft Learn results found" ಎಂದು ತೋರಿಸುತ್ತದೆ.

**ಸಾಧ್ಯ ಕಾರಣಗಳು:**

1. **ನೆಟ್ವರ್ಕ್ ಸಮಸ್ಯೆ** - MCP ಎಂಡ್‌ಪಾಯಿಂಟ್ (`https://learn.microsoft.com/api/mcp`) ತಲುಪಲಾಗುತ್ತಿಲ್ಲ.
   ```powershell
   # ಸಂಪರ್ಕೆಯನ್ನು ಪರೀಕ್ಷಿಸಿ
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   ಇದು `200` ಅನ್ನು ತಿರುಗಿಸಿದರೆ, ಎಂಡ್‌ಪಾಯಿಂಟ್ ತಲುಪಬಹುದಾಗಿದೆ.

2. **ಚಿಗುರು ಪ್ರಶ್ನೆ** - ಕೌಶಲ್ಯ ಹೆಸರು Microsoft Learn ಹುಡುಕಾಟಕ್ಕಿಂತ ತುಂಬಾ ವಿಶೇಷವಾಗಿದೆ.  
   - ಬಹುಶಃ ಅತ್ಯಂತ ವಿಶಿಷ್ಟ ಕೌಶಲ್ಯಗಳಿಗೆ ಇದು ಸಾಮಾನ್ಯ. ಉಪಕರಣ ಪ್ರತಿಕ್ರಿಯಾಗೆ ಬ್ಯಾಕಪ್ URL ಅನ್ನು ಒಳಗೊಂಡಿದೆ.

3. **MCP ಸೆಷನ್ ಗಡುವು ಸಮಯ ಮುಗಿದಿದೆ** - Streamable HTTP ಸಂಪರ್ಕ ಸಮಯ ಮೀರಿದೆ.  
   - ಮರುಪ್ರಯತ್ನಿಸಿ. MCP ಸೆಷನ್‌ಗಳು ಅಲ್ಪಕಾಲಿಕವಾಗಿದ್ದು ಮರುಸಂಪರ್ಕ ಬೇಕಾಗಬಹುದು.

### MCP ಲಾಗ್‌ಗಳ ವಿವರಣೆ

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| ಲಾಗ್ | ಅರ್ಥ | ಕ್ರಮ |
|-----|---------|--------|
| `GET → 405` | MCP ಕ್ಲೈಂಟ್ ಪ್ರಾರಂಭಿಕ ಪರೀಕ್ಷೆಗಳು | ಸಾಮಾನ್ಯ - ನಿರ್ಲಕ್ಷಿಸಿ |
| `POST → 200` | ಉಪಕರಣ ಕರೆ ಯಶಸ್ವಿ | ನಿರೀಕ್ಷಿತ |
| `DELETE → 405` | MCP ಕ್ಲೈಂಟ್ ಕ್ಲೀನ್-ಅಪ್ ಪರೀಕ್ಷೆಗಳು | ಸಾಮಾನ್ಯ - ನಿರ್ಲಕ್ಷಿಸಿ |
| `POST → 400` | ತಪ್ಪು ವಿನಂತಿ (ಖರಾಬು ಕ್ವೇರಿ) | `search_microsoft_learn_for_plan()` ನಲ್ಲಿ `query` ಪರಾಮೀಟರ್ ಪರಿಶೀಲಿಸಿ |
| `POST → 429` | ದರ ಮಿತಿಬದ್ಧ | ಕಾಯಿರಿ ಮತ್ತು ಮರುಪ್ರಯತ್ನಿಸಿ. `max_results` ಪರಾಮೀಟರ್ ಕಡಿಮೆ ಮಾಡಿ |
| `POST → 500` | MCP ಸರ್ವರ್ ದೋಷ | ತಾತ್ಕಾಲಿಕ - ಮರುಪ್ರಯತ್ನಿಸಿ. ನಿರಂತರ ಇದ್ದರೆ, Microsoft Learn MCP API ಡೌನ್ ಆಗಿರಬಹುದು |
| ಸಂಪರ್ಕ ಸಮಯ ಮೀರಿದೆ | ನೆಟ್ವರ್ಕ್ ಸಮಸ್ಯೆ ಅಥವಾ MCP ಸರ್ವರ್ ಲಭ್ಯವಿಲ್ಲ | ಇಂಟರ್ನೆಟ್ ಪರಿಶೀಲಿಸಿ. `curl https://learn.microsoft.com/api/mcp` ಅನ್ನು ಪ್ರಯತ್ನಿಸಿ |

---

## ನಿಯೋಜನೆ ಸಮಸ್ಯೆಗಳು

### ನಿಯೋಜನೆ ನಂತರ ಕನ್ಟೈನರ್ ಪ್ರಾರಂಭವಾಗುತ್ತಿಲ್ಲ

1. **ಕಂಟೈನರ್ ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ:**  
   - **Microsoft Foundry** Sidebar ತೆರೆಯಿರಿ → **Hosted Agents (Preview)** ವಿಸ್ತರಿಸಿ → ನಿಮ್ಮ ಏಜೆಂಟ್ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ → ಆ ಆವೃತ್ತಿಯನ್ನು ವಿಸ್ತರಿಸಿ → **Container Details** → **Logs**.  
   - Python ಸ್ಟಾಕ್ ಟ್ರೇಸ್ ಅಥವಾ ಮೋಡ್ಯೂಲ್ ಕಾಣದ ತಪ್ಪುಗಳಿಗಾಗಿ ಪರಿಶೀಲಿಸಿ.

2. **ಸಾಮಾನ್ಯ ಕನ್ಟೈನರ್ ಸ್ಟಾರ್ಟ್ ವಿಫಲತೆಗಳು:**

   | ಲಾಗ್‌ನ ದೋಷಗಳು | ಕಾರಣ | ಸರಿಪಡಿಸುವಿಕೆ |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` ನಲ್ಲಿ ಪ್ಯಾಕೇಜ್ ಇಲ್ಲ | ಪ್ಯಾಕೇಜ್ ಸೇರಿಸಿ, ಮರುನಿಯೋಜನೆ ಮಾಡಿ |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` ಪರಿಸರ ಚರಗಳಿಲ್ಲ | `agent.yaml` → `environment_variables` ವಿಭಾಗವನ್ನು تازهಮಾಡಿ |
   | `azure.identity.CredentialUnavailableError` | ಮ್ಯಾನೇಜ್ಡ್ ಐಡೆಂಟಿಟಿ ಸೆಟ್ ಆಗಿಲ್ಲ | Foundry ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಇವೇಟ್ ಮಾಡುತ್ತದೆ - ಎಕ್ಸ್ಟೆನ್ಶನ್ ಮೂಲಕ ನಿಯೋಜಿಸುವುದಾಗಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ |
   | `OSError: port 8088 already in use` | Dockerfile ನಲ್ಲಿ ತಪ್ಪು ಪೋರ್ಟ್ ಅಥವಾ ಪೋರ್ಟ್ ಸಂಧ್ಯೆ | Dockerfile ನಲ್ಲಿ `EXPOSE 8088` ಮತ್ತು `CMD ["python", "main.py"]` ಸರಿಯಾದುದೇ ಎಂದು ಪರಿಶೀಲಿಸಿ |
   | ಕನ್ಟೈನರ್ ಕೋಡ್ 1ೊಂದಿಗೆ ನಿಂತಿದೆ | `main()` ನಲ್ಲಿ ಅಪಹರಿಸಲಾಗದ ಹೊರತುಪಡಿಸಿದೆ | ಮೊದಲಿಯಾಗಿ ಸ್ಥಳೀಯವಾಗಿ ([Module 5](05-test-locally.md)) ಪರೀಕ್ಷಿಸಿ, ನಂತರ ನಿಯೋಜಿಸಿ |

3. **ತಪ್ಪು ಸರಿಪಡಿಸಿ ನಂತರ ಮರುನಿಯೋಜನೆ ಮಾಡಿ:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → ಅದೇ ಏಜೆಂಟ್ ಆರಿಸಿ → ಹೊಸ ಆವೃತ್ತಿಯನ್ನು ನಿಯೋಜಿಸಿ.

### ನಿಯೋಜನೆ ಮಿಗಿಲಾಗಿ ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದೆ

ಬಹು ಏಜೆಂಟ್ ಕನ್ಟೈನರ್‌ಗಳು ಪ್ರಾರಂಭಿಸಲು ಹೆಚ್ಚು ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುತ್ತವೆ ಏಕೆಂದರೆ ಆರಂಭದಲ್ಲಿ 4 ಏಜೆಂಟ್ ಇನ್ಸ್ಟೆನ್ಸ್‌ಗಳನ್ನು ಸೃಷ್ಟಿಸುತ್ತವೆ. ಸಾಮಾನ್ಯ ಪ್ರಾರಂಭ ಸಮಯಗಳು:

| ಹಂತ | ನಿರೀಕ್ಷಿತ ಅವಧಿ |
|-------|------------------|
| ಕನ್ಟೈನರ್ ಇಮೇಜ್ ನಿರ್ಮಾಣ | 1-3 ನಿಮಿಷಗಳು |
| ACR ಗೆ ಇಮೇಜ್ ತಳ್ಳುವುದು | 30-60 ಸೆಕೆಂಡುಗಳು |
| ಕನ್ಟೈನರ್ ಪ್ರಾರಂಭ (ಒಂದು ಏಜೆಂಟ್) | 15-30 ಸೆಕೆಂಡುಗಳು |
| ಕನ್ಟೈನರ್ ಪ್ರಾರಂಭ (ಬಹು ಏಜೆಂಟ್) | 30-120 ಸೆಕೆಂಡುಗಳು |
| ಏಜೆಂಟ್ ಪ್ಲೇಗ್ರೌಂಡ್ ನಲ್ಲಿ ಲಭ್ಯ | "Started" ನಂತರ 1-2 ನಿಮಿಷಗಳು |

> "Pending" ಸ್ಥಿತಿ 5 ನಿಮಿಷಗಳಿಗಿಂತ ಹೆಚ್ಚು ಇದ್ದರೆ, ಕನ್ಟೈನರ್ ಲಾಗ್‌ಗಳಲ್ಲಿ ದೋಷಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.

---

## RBAC ಮತ್ತು ಅನುಮತಿ ಸಮಸ್ಯೆಗಳು

### `403 Forbidden` ಅಥವಾ `AuthorizationFailed`

ನಿಮ್ಮ Foundry ಪ್ರಾಜೆಕ್ಟ್ ಮೇಲೆ **[Azure AI User](https://aka.ms/foundry-ext-project-role)** ಪಾತ್ರ ಬೇಕು:

1. [Azure Portal](https://portal.azure.com) → ನಿಮ್ಮ Foundry **project** ಸಂಪನ್ಮೂಲಕ್ಕೆ ಹೋಗಿ.  
2. **Access control (IAM)** → **Role assignments** ಕ್ಲಿಕ್ ಮಾಡಿ.  
3. ನಿಮ್ಮ ಹೆಸರನ್ನು ಹುಡುಕಿ → **Azure AI User** ಪಟ್ಟಿ ಇದೆ ಎಂದು ದೃಢಪಡಿಸಿ.  
4. ಇಲ್ಲದಿದ್ದರೆ: **Add** → **Add role assignment** → **Azure AI User** ಹುಡುಕಿ → ನಿಮ್ಮ ಖಾತೆಗೆ ನಿಯೋಜಿಸಿ.

ವಿಸ್ತೃತ ವಿವರಗಳಿಗೆ [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ಡಾಕ್ಯುಮೆಂಟೇಷನ್ ನೋಡಿ.

### ಮಾದರಿ ನಿಯೋಜನೆ ಲಭ್ಯವಿಲ್ಲ

ಏಜೆಂಟ್ ಮಾದರಿ ಸಂಬಂಧಿತ ದೋಷಗಳನ್ನು ನೀಡುತ್ತಿದ್ದರೆ:

1. ಮಾದರಿ ನಿಯೋಜಿತವಾಗಿದೆ ಎಂದು ಖಚಿತಪಡಿಸಿ: Foundry Sidebar → ಪ್ರಾಜೆಕ್ಟ್ ವಿಸ್ತರಿಸಿ → **Models** → `gpt-4.1-mini` (ಅಥವಾ ನಿಮ್ಮ ಮಾದರಿ) ಇದ್ದು ಸ್ಥಿತಿ **Succeeded** ಎಂದು ಪರಿಶೀಲಿಸಿ.  
2. ನಿಯೋಜನೆ ಹೆಸರು ಹೊಂದಿಕೆಯಾಗುತ್ತದೆಯಾ ಎಂಬುದನ್ನು ಪರಿಶೀಲಿಸಿ: `.env` (ಅಥವಾ `agent.yaml`) ಯಲ್ಲಿರುವ `MODEL_DEPLOYMENT_NAME` ಮತ್ತು Sidebar‌ನ ನಿಯೋಜನೆಯ ಹೆಸರನ್ನು ಹೋಲಿಸಿ.  
3. ನಿಯೋಜನೆ ಅವಧಿ ಮುಗಿದಿದ್ದರೆ (ಉಚಿತ ತರಗತಿ): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) ನಿಂದ ಮರುನಿಯೋಜಿಸಿ (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## ಏಜೆಂಟ್ ಇನ್ಸ್ಪೆಕ್ಟರ್ ಸಮಸ್ಯೆಗಳು

### ಇನ್ಸ್ಪೆಕ್ಟರ್ ತೆರೆಯುತ್ತಿದೆ ಆದರೆ "Disconnected" ತೋರಿಸುತ್ತದೆ

1. ಸರ್ವರ್ ಚಲಿಸುತ್ತಿದೆ ಎಂದು ಖಚಿತಪಡಿಸಿ: ಟರ್ಮಿನಲ್‌ನಲ್ಲಿ "Server running on http://localhost:8088" ಕಾಣಲು ಪರಿಶೀಲಿಸಿ.  
2. ಪೋರ್ಟ್ `5679` ಪರಿಶೀಲಿಸಿ: ಇನ್ಸ್ಪೆಕ್ಟರ್ debugpy ಮೂಲಕ 5679 ಪೋರ್ಟ್ ನಲ್ಲಿ ಸಂಪರ್ಕ ಹೊಂದುತ್ತದೆ.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. ಸರ್ವರ್ ಮರುಪ್ರಾರಂಭಿಸಿ ಮತ್ತು ಇನ್ಸ್ಪೆಕ್ಟರ್ ಪುನಃ ತೆರೆಯಿರಿ.

### ಇನ್ಸ್ಪೆಕ್ಟರ್ ಭಾಗಶಃ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ತೋರಿಸುತ್ತದೆ

ಬಹು ಏಜೆಂಟ್ ಪ್ರತಿಕ್ರಿಯೆಗಳು ದೀರ್ಘವಾಗಿದ್ದು ಕ್ರಮೇಣ ಸ್ಟ್ರೀಮ್ ಆಗಿ ಬರುತ್ತವೆ. ಸಂಪೂರ್ಣ ಪ್ರತಿಕ್ರಿಯೆ ಪೂರ್ಣಗೊಳ್ಳಲು ಕಾಯಿರಿ (30-60 ಸೆಕೆಂಡುಗಳು gap ಕಾರ್ಡ್‌ಗಳ ಸಂಖ್ಯೆ ಮತ್ತು MCP ಉಪಕರಣ ಕರೆಗಳ ಮೇಲೆ ಅವಲಂಬಿತ).

ಯಾವಾಗಲೂ ಪ್ರತಿಕ್ರಿಯೆ ಕಡಿತವಾಗಿದ್ದರೆ:  
- GapAnalyzer ಸೂಚನೆಗಳಲ್ಲಿ `CRITICAL:` ಬ್ಲಾಕ್ ಸೇರಿಸಲಾಗಿದೆ ಎಂಬುದನ್ನು ಪರಿಶೀಲಿಸಿ, ಇದು gap ಕಾರ್ಡ್‌ಗಳನ್ನು ಮಿಶ್ರಣ ಮಾಡದೇ प्रतिबಂಧಿಸುತ್ತದೆ.  
- ನಿಮ್ಮ ಮಾದರಿಯ ಟೋಕನ್ ಗಡಿಯನ್ನು ಪರಿಶೀಲಿಸಿ - `gpt-4.1-mini` 32K ಟೋಕನ್ ಔಟ್‌ಪುಟ್ ಬೆಂಬಲಿಸುತ್ತದೆ, ಇದು ಸಾಕಷ್ಟು ಆಗಿರಬೇಕು.

---

## ಕಾರ್ಯಕ್ಷಮತಾ ಸಲಹೆಗಳು

### ನಿಧಾನ ಪ್ರತಿಕ್ರಿಯೆಗಳು

ಬಹು ಏಜೆಂಟ್ ಕೆಲಸಗಾರ ಪ್ರವಾಹಗಳು ಕ್ರಮವಾಗಿ ನಿರ್ಬಂಧಿತ ಅವಲಂಬನೆಗಳು ಮತ್ತು MCP ಉಪಕರಣ ಕರೆಗಳ ಕಾರಣ ಸ್ವಾಭಾವಿಕವಾಗಿ ನಿಧಾನವಾಗಿರುತ್ತವೆ.

| ಸುಧಾರಣೆ | ಹೇಗೆ | ಪರಿಣಾಮ |
|-------------|-----|--------|
| MCP ಕರೆಗಳನ್ನು ಕಡಿಮೆ ಮಾಡುವುದು | ಉಪಕರಣದ `max_results` ಪರಿಮಾಣ ಕಡಿಮೆಮಾಡುವುದು | ಕಡಿಮೆ HTTP ಸುತ್ತುಮುತ್ತುಗಳು |
| ಸೂಚನೆಗಳನ್ನು ಸರಳಗೊಳಿಸುವುದು | ಪುಟಾಣಿ, ಗುರಿದಾಯಕ ಏಜೆಂಟ್ ಸಂದೇಶಗಳು | ವೇಗವಾದ LLM ನಿರ್ಣಯ |
| `gpt-4.1-mini` ಬಳಸಿ | ಅಭಿವೃದ್ಧಿಗೆ `gpt-4.1`ಗಿಂತ ವೇಗವಾಗಿ | ಸುಮಾರು 2x ವೇಗ ಸುಧಾರಣೆ |
| gap ಕಾರ್ಡ್ ವಿವರ ಕಡಿಮೆ ಮಾಡುವುದು | GapAnalyzer ಸೂಚನೆಗಳಲ್ಲಿ gap ಕಾರ್ಡ್ ಫಾರ್ಮ್ಯಾಟ್ ಸರಳಗೊಳಿಸುವಿಕೆ | ರಚನೆ ಕಡಿಮೆ ಆಗುವುದು |

### ಸಾಮಾನ್ಯ ಪ್ರತಿಕ್ರಿಯೆ ಸಮಯಗಳು (ಸ್ಥಳೀಯ)

| ಕಾನ್ಫಿಗರೇಶನ್ | ನಿರೀಕ್ಷಿತ ಸಮಯ |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap ಕಾರ್ಡ್‌ಗಳು | 30-60 ಸೆಕೆಂಡುಗಳು |
| `gpt-4.1-mini`, 8+ gap ಕಾರ್ಡ್‌ಗಳು | 60-120 ಸೆಕೆಂಡುಗಳು |
| `gpt-4.1`, 3-5 gap ಕಾರ್ಡ್‌ಗಳು | 60-120 ಸೆಕೆಂಡುಗಳು |
---

## ಸಹಾಯ ಪಡೆಯುವುದು

ನೀವು ಮೇಲಿನ ಸವಾಲುಗಳನ್ನು ಪ್ರಯತ್ನಿಸಿದ ನಂತರ ಅटकಿಕೊಂಡಿದ್ದರೆ:

1. **ಸರ್ವರ್ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ** - ಬಹುತೇಕ ತಪ್ಪುಗಳು ಟರ್ಮಿನಲ್‌ನಲ್ಲಿ Python ಸ್ಟಾಕ್ ಟ್ರೇಸ್ ಅನ್ನು ಉತ್ಪಾದಿಸುತ್ತವೆ. ಸಂಪೂರ್ಣ ಟ್ರ್ಯಾಸ್ಬ್ಯಾಕ್ ಅನ್ನು ಓದಿರಿ.
2. **ದೋಷ ಸಂದೇಶವನ್ನು ಹುಡುಕಿ** - ದೋಷ ಪಠ್ಯವನ್ನು ಪ್ರತಿರೂಪಿಸಿ ಮತ್ತು [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) ನಲ್ಲಿ ಹುಡುಕಿ.
3. **ಇಶ್ಯೂ ತೆರೆಯಿರಿ** - ಕೆಳಗಿನ ವಿವರಗಳೊಂದಿಗೆ [ವರ್ಕ್‌ಶಾಪ್ ರೆಪೊಸಿಟರಿ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) ಯಲ್ಲಿ ಇಶ್ಯೂ ಅನ್ನು ದಾಖಲು ಮಾಡಿರಿ:
   - ದೋಷ ಸಂದೇಶ ಅಥವಾ ಸ್ಕ್ರೀನ್‌ಶಾಟ್
   - ನಿಮ್ಮ ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿಗಳು (`pip list | Select-String "agent-framework"`)
   - ನಿಮ್ಮ Python ಆವೃತ್ತಿ (`python --version`)
   - ಸಮಸ್ಯೆ ಸ್ಥಳೀಯವಾಗಿದೆಯಾ ಅಥವಾ ನಿಯೋಜನೆಯ ನಂತರವೆಯಾ ಎಂದು

---

### ಪರಿಶೀಲನಾ ಬಿಂದು

- [ ] ನೀವು ಸಾಮಾನ್ಯ ಬಹು-ಏಜೆಂಟ್ ದೋಷಗಳನ್ನು ತ್ವರಿತ ಸೂಚಕ ಪದಕೋಪಿಂದ ಗುರುತಿಸಿ ಸರಿಪಡಿಸಬಹುದು
- [ ] ನೀವು `.env` ಸಂರಚನಾ ಸಮಸ್ಯೆಗಳನ್ನು ಪರಿಶೀಲಿಸುವ ಮತ್ತು ಸರಿಪಡಿಸುವ ವಿಧಾನವನ್ನು ತಿಳಿದಿದ್ದೀರಾ
- [ ] ನೀವು ಪ್ಯಾಕೇಜ್ ಆವೃತ್ತಿಗಳು ಅಗತ್ಯ ಮ್ಯಾಟ್ರಿಕ್ಸ್‌ಗೆ ಹೊಂದಿಕೆಯಾಗಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಬಹುದು
- [ ] ನೀವು MCP ಲಾಗ್ ನುಡಿಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಂಡು ಸಾಧನ ವೈಫಲ್ಯಗಳನ್ನು ರೋಗನಿರ್ಧಾರ ಮಾಡಬಹುದು
- [ ] ನೀವು ನಿಯೋಜನೆ ವೈಫಲ್ಯಗಳಿಗೆ ಕನ್ಟೈನರ್ ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸುವ ವಿಧಾನವನ್ನು ತಿಳಿದಿದ್ದೀರಾ
- [ ] ನೀವು Azure ಪೋರ್ಟಲ್‌ನಲ್ಲಿ RBAC ಪಾತ್ರಗಳನ್ನು ಪರಿಶೀಲಿಸಬಹುದಾಗಿದೆ

---

**ಹಿಂದಿನದು:** [07 - Verify in Playground](07-verify-in-playground.md) · **ಮನೆ:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ಘೋಷಣೆ**:  
ಈ ದಸ್ತಾವೇಜು [Co-op Translator](https://github.com/Azure/co-op-translator) ಎಂಬ AI ಅನುವಾದ ಸೇವೆಯ ಮೂಲಕ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ನಿಖರತೆಗೆ ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದರೂ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ತಪ್ಪುಗಳು ಅಥವಾ ಅಸತ್ಯತೆಗಳು ಇರಬಹುದು ಎಂಬದರ ಬಗ್ಗೆ ದಯವಿಟ್ಟು ಜಾಗರೂಕರಾಗಿ ఉండಿ. ಮೂಲ ಭಾಷೆಯಲ್ಲಿರುವ ದಸ್ತಾವೇಜು ಅಧಿಕೃತ ಮೂಲವಾಗಿ ಪರಿಗಣಿಸಲು ಆಗುತ್ತದೆ. ಮಹತ್ವದ ಮಾಹಿತಿಗಾಗಿ ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದ ಶಿಫಾರಸ್ಸು ಮಾಡಲಾಗಿದೆ. ಈ ಅನುವಾದದಿಂದ ಉಂಟಾಗುವ ಯಾವುದೇ ಭಾಷಾಂತರಾತ್ಮಕ ಅರ್ಥತೊಂದರೆಗಳಿಗಾಗಿ ನಾವು ಹೊಣೆಗಾರರಾಗುವುದಿಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->