# PersonalCareerCopilot - CV → Jobmatch Evaluator

En workflow-først multi-agent app, der vurderer hvor godt et CV matcher en jobbeskrivelse, og derefter genererer en personlig læringsplan for at lukke hullerne.

---

## Agenter

| Agent | Rolle | Værktøjer |
|-------|------|---------|
| **ResumeParser** | Ekstraherer strukturerede færdigheder, erfaring, certificeringer fra CV-tekst | - |
| **JobDescriptionAgent** | Ekstraherer krævede/foretrukne færdigheder, erfaring, certificeringer fra en jobbeskrivelse | - |
| **MatchingAgent** | Sammenligner profil vs krav → matchscore (0-100) + matchede/manglende færdigheder | - |
| **GapAnalyzer** | Bygger en personlig læringsplan med Microsoft Learn ressourcer | `search_microsoft_learn_for_plan` (MCP) |

## Workflow

```mermaid
flowchart LR
    UserInput["User Input: Resume + Job Description"] --> ResumeParser
    ResumeParser -- "parsed resume + JD relay" --> JobDescriptionAgent
    JobDescriptionAgent -- "JD requirements + resume relay" --> MatchingAgent
    MatchingAgent -- "fit report + gaps" --> GapAnalyzerMCP["Gap Analyzer +\nMicrosoft Learn MCP"]
    GapAnalyzerMCP --> FinalOutput["Final Output:\nFit Score + Roadmap"]
```

---

## Kom godt i gang

### 1. Opsæt miljø

Denne mappe er referencens implementering for workflow-baserede Lab 02 skabelon. Dens `main.py` bruger de eksisterende prompt-blocks plus `WorkflowBuilder` til at forbinde de fire agenter.

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. Konfigurer legitimationsoplysninger

Opret en `.env` fil i denne mappe:

```powershell
copy .env .env.bak 2>$null; echo $null > .env
```

Rediger `.env`:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| Værdi | Hvor findes det |
|-------|-----------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Foundry Toolkit sidebjælke → højreklik dit projekt → **Kopiér projektendepunkt** |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Foundry sidebjælke → udvid projekt → **Modeller + endepunkter** → udrulningsnavn |

### 3. Kør lokalt

```powershell
python -m debugpy --listen 127.0.0.1:5679 main.py --port 8088
```

Eller brug VS Code opgaven: `Ctrl+Shift+P` → **Opgaver: Kør opgave** → **Kør Agent HTTP-server**.

For F5-debugging, brug **Debug Local Agent HTTP Server**.

### 4. Test med Agent Inspector

Åbn Agent Inspector: `Ctrl+Shift+P` → **Foundry Toolkit: Åbn Agent Inspector**.

Indsæt denne testprompt:

```
Resume:
Jane Doe
Senior Software Engineer with 5 years of experience in Python, Django, and AWS.
Built microservices handling 10K+ requests/second. Led a team of 4 developers.
Certifications: AWS Solutions Architect Associate.
Education: B.S. Computer Science, State University.

Job Description:
Senior Cloud Engineer at Contoso Ltd.
Required: Python, Azure, Kubernetes, Terraform, CI/CD pipelines.
Preferred: Go, monitoring (Prometheus/Grafana), cost optimization.
Experience: 5+ years in cloud infrastructure.
Certifications: Azure Solutions Architect Expert preferred.
```

**Forventet:** En matchscore (0-100), matchede/manglende færdigheder og en personlig læringsplan med Microsoft Learn URL'er.

### 5. Udrul til Foundry

`Ctrl+Shift+P` → **Foundry Toolkit: Udrul hostet agent** → vælg dit projekt → bekræft.

---

## Projektstruktur

```
PersonalCareerCopilot/
├── .env                ← Your credentials (git-ignored)
├── agent.yaml          ← Hosted agent definition (name, resources, env vars)
├── Dockerfile          ← Container image for Foundry deployment
├── main.py             ← 4-agent workflow (instructions, MCP tool, WorkflowBuilder)
└── requirements.txt    ← Python dependencies
```

## Nøglefiler

### `agent.yaml`

Definerer den hostede agent for Foundry Agent Service:
- `kind: hosted` - kører som en administreret container
- `protocols` - `responses` protokol med `version: 2.0.0`, der eksponerer `/responses` HTTP-endepunktet
- `environment_variables` - `AZURE_AI_MODEL_DEPLOYMENT_NAME` er deklareret her; `FOUNDRY_PROJECT_ENDPOINT` injiceres automatisk ved udrulning

### `main.py`

Indeholder:
- **Agent-instruktioner** - fire `*_INSTRUCTIONS` konstanter, én pr. agent
- **MCP-værktøj** - `search_microsoft_learn_for_plan()` kalder `https://learn.microsoft.com/api/mcp` via Streamable HTTP
- **Agent oprettelse** - fire `Agent()` + `AgentExecutor()` instanser, der deler én `FoundryChatClient`
- **Workflow diagram** - `WorkflowBuilder` forbinder agenter som en sekventiel pipeline: ResumeParser → JD Agent → MatchingAgent → GapAnalyzer
- **Server opstart** - `ResponsesHostServer` kører på port 8088

### `requirements.txt`

| Pakke | Formål |
|---------|---------|
| `agent-framework-foundry` | Kernemiljø: `Agent`, `AgentExecutor`, `WorkflowBuilder`, `@tool`, `FoundryChatClient` |
| `agent-framework-foundry-hosting` | `ResponsesHostServer` + Foundry hosting integration |
| `mcp<2,>=1.24.0` | MCP-klient til GapAnalyzer (`streamable_http_client`) |
| `debugpy` | Python-debugging (F5 i VS Code) |

---

## Fejlfinding

| Problem | Løsning |
|-------|--------|
| `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` eller `KeyError: 'AZURE_AI_MODEL_DEPLOYMENT_NAME'` | Opret `.env` med både `FOUNDRY_PROJECT_ENDPOINT` og `AZURE_AI_MODEL_DEPLOYMENT_NAME` sat |
| `ModuleNotFoundError: No module named 'agent_framework'` | Aktivér venv og kør `pip install -r requirements.txt` |
| Ingen Microsoft Learn URL'er i output | Tjek internetforbindelse til `https://learn.microsoft.com/api/mcp` |
| Kun 1 gap-kort (afkortet) | Bekræft `GAP_ANALYZER_INSTRUCTIONS` inkluderer `CRITICAL:` blokken |
| Port 8088 i brug | Stop andre servere: `netstat -ano \| findstr :8088` |

For detaljeret fejlfinding, se [Modul 8 - Fejlfinding](../docs/08-troubleshooting.md).

---

**Fuld gennemgang:** [Lab 02 Docs](../docs/README.md) · **Tilbage til:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->