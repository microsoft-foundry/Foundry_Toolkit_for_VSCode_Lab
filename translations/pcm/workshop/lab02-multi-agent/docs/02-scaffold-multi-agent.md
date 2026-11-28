# Module 2 - Setup di Multi-Agent Project

⏱️ ~5 min

For dis module, you go use [Foundry Toolkit for VS Code](https://aka.ms/foundrytk) to **setup one multi-agent project**. Di wizard go make `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`, plus VS Code debug configuration - so you fit focus for arrange di 4-agent workflow for Module 3.

> **Main tins:** Di scaffold na one working stub wey get one agent. You go change di placeholder logic wit di `WorkflowBuilder` graph for Module 3. You no go write di boilerplate from scratch.

> **Example wey dem dey use:** [`PersonalCareerCopilot/`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot) na one complete working example. Use am to compare wetin you dey do as you dey go.

### Scaffold wizard flow

```mermaid
flowchart LR
    A[Command Palette: Create New Hosted Agent] --> B[Language: Python]
    B --> C[API Type: Response API]
    C --> D[Template: Workflows]
    D --> E[Select Model]
    E --> F[Workspace Folder and Agent Name]
    F --> G[Generated Project]
```

---

## Step 1: Open di Create Hosted Agent wizard

1. Press `Ctrl+Shift+P` to open di **Command Palette**.
2. Type: **Foundry Toolkit: Create new Hosted Agent** and select am.
3. Di wizard go open for di **Agent Details** tab.

> **Another way:** Click di **Foundry Toolkit** icon for di Activity Bar → click di **+** icon near **Hosted Agents** → **Create New Hosted Agent**.

---

## Step 2: Choose settings

![Create Hosted Agent from Sample - Agent Details tab with Workflows template selected](../../../../../translated_images/pcm/02-scaffold-wizard-details.af4798708b4a87f4.webp)

1. For the left navigation/options section, select di following:

| Menu | Selection | Notes |
|--------|-----------|-------|
| **Language** | Python | C# (.NET) still dey supported |
| **Framework** | Agent Framework | E go give `Agent`, `AgentExecutor`, `WorkflowBuilder` |
| **API type** | Response API | `POST /responses` - platform-managed history, streaming support |
| **Template** | **Workflows** | E dey process requests through many agents one after the other |

2. Once you select am, click **Next**

![Create Hosted Agent from Sample - Create tab showing PersonalCareerCopilot as the folder name](../../../../../translated_images/pcm/02-scaffold-wizard-create.ae0c285c309698ba.webp)

3. For di next window, select di following:

| Menu | Selection | Notes |
|--------|-----------|-------|
| **Workspace folder** | Browse go target folder | e.g., `workshop/lab02-multi-agent/` for dis repo |
| **Agent name** | `PersonalCareerCopilot` | Dis one go be di project directory name |
| **Model Deployment** | Select your deployed model | e.g., `gpt-4.1-mini` from Lab 01 |

4. Click **Create** to setup di project. VS Code go generate di files and open di folder.

> **Tip:** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series) balance speed and quality well well for multi-agent development.

---

## Step 3: Check di generated project

After you finish scaffold, check say you see these files for di Explorer (`Ctrl+Shift+E`):

```
📂 <your-agent-name>/
├── .azdignore          ← Files excluded from Azure Developer CLI deployments
├── .dockerignore       ← Files excluded from Docker builds
├── .env                ← Environment variables (placeholders - fill in Module 3)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted, protocol: responses)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Stub agent entry point (replace with WorkflowBuilder in Module 3)
└── requirements.txt    ← Python dependencies
```

> **Important:** Open dis scaffolded folder directly for VS Code so `.vscode/launch.json` and `tasks.json` go work well for F5 debugging.

### Key files we explain

| File | Purpose |
|------|---------|
| `agent.yaml` | E dey declare `kind: hosted`, map env vars, define di `/responses` protocol |
| `main.py` | Stub: one `FoundryChatClient` → `Agent` → `ResponsesHostServer`. You go change dis one to 4 agents + `WorkflowBuilder` for Module 3 |
| `Dockerfile` | `python:3.12-slim`, e install `requirements.txt`, e expose port 8088, e run `python main.py` |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp<2,>=1.24.0`, `debugpy` |

> **Reference:** See [`PersonalCareerCopilot/agent.yaml`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) and [`PersonalCareerCopilot/requirements.txt`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/requirements.txt) for the full generated content.

---

### ✅ Checkpoint

- [ ] Scaffold wizard don complete - new project folder dey show for Explorer
- [ ] All di files we expect dey: `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`
- [ ] `agent.yaml` dey show `kind: hosted` and `protocol: responses`
- [ ] `main.py` dey import `Agent`, `FoundryChatClient`, `ResponsesHostServer`
- [ ] Scaffolded folder open as di VS Code workspace root
- [ ] You sabi say `main.py` na stub - `WorkflowBuilder` go add am for Module 3

---

**Previous:** [01 - Understand Multi-Agent Architecture](01-understand-multi-agent.md) · **Next:** [03 - Configure Agents & Environment →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->