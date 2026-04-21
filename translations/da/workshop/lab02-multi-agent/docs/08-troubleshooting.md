# Modul 8 - Fejlfinding (Multi-Agent)

Dette modul dækker almindelige fejl, rettelser og debugging-strategier specifikt for multi-agent workflowet. For generelle Foundry-implementeringsproblemer, se også [Lab 01 fejlfinding guide](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Hurtig reference: Fejl → Løsning

| Fejl / Symptom | Sandsynlig årsag | Løsning |
|----------------|------------------|---------|
| `RuntimeError: Missing required environment variable(s)` | `.env` fil mangler eller værdier ikke sat | Opret `.env` med `PROJECT_ENDPOINT=<your-endpoint>` og `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuelt miljø ikke aktiveret eller dependencies ikke installeret | Kør `.\.venv\Scripts\Activate.ps1` og derefter `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP-pakken ikke installeret (mangler i requirements) | Kør `pip install mcp` eller tjek at `requirements.txt` inkluderer den som transitiv dependency |
| Agent starter men returnerer tomt svar | `output_executors` uoverensstemmelse eller manglende edges | Bekræft `output_executors=[gap_analyzer]` og at alle edges findes i `create_workflow()` |
| Kun 1 gap card (resten mangler) | GapAnalyzer instruktioner ufuldstændige | Tilføj `CRITICAL:` afsnittet til `GAP_ANALYZER_INSTRUCTIONS` - se [Modul 3](03-configure-agents.md) |
| Fit-score er 0 eller fraværende | MatchingAgent modtog ikke upstream data | Bekræft både `add_edge(resume_parser, matching_agent)` og `add_edge(jd_agent, matching_agent)` findes |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP-serveren afviste værktøjskaldet | Tjek internetforbindelse. Prøv at åbne `https://learn.microsoft.com/api/mcp` i browser. Prøv igen |
| Ingen Microsoft Learn URLs i output | MCP værktøj ikke registreret eller forkert endpoint | Bekræft `tools=[search_microsoft_learn_for_plan]` på GapAnalyzer og at `MICROSOFT_LEARN_MCP_ENDPOINT` er korrekt |
| `Address already in use: port 8088` | En anden proces bruger port 8088 | Kør `netstat -ano \| findstr :8088` (Windows) eller `lsof -i :8088` (macOS/Linux) og stop den konflikterende proces |
| `Address already in use: port 5679` | Debugpy port konflikt | Stop andre debug-sessioner. Kør `netstat -ano \| findstr :5679` for at finde og dræbe processen |
| Agent Inspector vil ikke åbne | Serveren er ikke fuldt startet eller port konflikt | Vent på "Server running" log. Tjek at port 5679 er fri |
| `azure.identity.CredentialUnavailableError` | Ikke logget ind i Azure CLI | Kør `az login` og genstart serveren |
| `azure.core.exceptions.ResourceNotFoundError` | Model deployment findes ikke | Tjek at `MODEL_DEPLOYMENT_NAME` matcher en deployet model i dit Foundry-projekt |
| Container status "Failed" efter deployment | Container crasher ved opstart | Tjek container logs i Foundry sidebar. Almindeligt: manglende env var eller import-fejl |
| Deployment viser "Pending" i > 5 minutter | Container tager for lang tid at starte eller resourcebegrænsninger | Vent op til 5 minutter for multi-agent (opretter 4 agent-instancer). Hvis stadig pending, tjek logs |
| `ValueError` fra `WorkflowBuilder` | Ugyldig graf-konfiguration | Sørg for `start_executor` er sat, `output_executors` er en liste, og der ikke er cirkulære edges |

---

## Miljø- og konfigurationsproblemer

### Manglende eller forkerte `.env` værdier

`.env`-filen skal ligge i `PersonalCareerCopilot/` mappen (samme niveau som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Forventet `.env` indhold:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Sådan finder du dit PROJECT_ENDPOINT:**  
- Åbn **Microsoft Foundry** sidebar i VS Code → højreklik dit projekt → **Copy Project Endpoint**.  
- Eller gå til [Azure Portal](https://portal.azure.com) → dit Foundry projekt → **Overview** → **Project endpoint**.

> **Sådan finder du dit MODEL_DEPLOYMENT_NAME:** I Foundry sidebar, udvid dit projekt → **Models** → find navnet på din deployede model (f.eks. `gpt-4.1-mini`).

### Env var prioritet

`main.py` bruger `load_dotenv(override=False)`, hvilket betyder:

| Prioritet | Kilde | Vinder hvis begge er sat? |
|-----------|-------|---------------------------|
| 1 (højeste) | Shell miljøvariabel | Ja |
| 2 | `.env` fil | Kun hvis shell variablen ikke er sat |

Det betyder Foundry runtime env vars (sat via `agent.yaml`) har højere prioritet end `.env` værdier under hosted deployment.

---

## Versionskompatibilitet

### Pakkeversionsmatrix

Multi-agent workflowet kræver specifikke pakkeversioner. Mismatchede versioner forårsager runtimefejl.

| Pakke | Krævet version | Tjek-kommando |
|--------|----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | nyeste pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Almindelige versionsfejl

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Rettelse: opgrader til rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` ikke fundet eller Inspector inkompatibel:**

```powershell
# Løsning: installer med --pre flag
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Rettelse: opgrader mcp-pakken
pip install mcp --upgrade
```

### Bekræft alle versioner på én gang

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Forventet output:

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

## MCP værktøjsproblemer

### MCP værktøj returnerer ingen resultater

**Symptom:** Gap cards siger "No results returned from Microsoft Learn MCP" eller "No direct Microsoft Learn results found".

**Mulige årsager:**

1. **Netværksproblem** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) er ikke tilgængeligt.  
   ```powershell
   # Test forbindelse
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
 Hvis denne returnerer `200`, er endpoint opnåelig.

2. **Forespørgsel for specifik** - Færdighedsnavnet er for niche for Microsoft Learn søgning.  
   - Dette er forventet for meget specialiserede færdigheder. Værktøjet har en fallback URL i svaret.

3. **MCP session timeout** - Den Streamable HTTP forbindelse timeoutede.  
   - Forsøg at sende forespørgslen igen. MCP sessioner er midlertidige og kan kræve genforbindelse.

### Forklaring af MCP logs

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Betydning | Handling |
|-----|-----------|----------|
| `GET → 405` | MCP klient probes under initialisering | Normalt - ignorer |
| `POST → 200` | Værktøjskald lykkedes | Forventet |
| `DELETE → 405` | MCP klient probes under oprydning | Normalt - ignorer |
| `POST → 400` | Dårlig forespørgsel (forkert formateret query) | Tjek `query` parameter i `search_microsoft_learn_for_plan()` |
| `POST → 429` | Rate begrænset | Vent og prøv igen. Reducer `max_results` parameter |
| `POST → 500` | MCP serverfejl | Midlertidigt - prøv igen. Vedvarende fejl kan betyde Microsoft Learn MCP API er nede |
| Connection timeout | Netværksproblem eller MCP server utilgængelig | Tjek internet. Prøv `curl https://learn.microsoft.com/api/mcp` |

---

## Deploymentsproblemer

### Container fejler ved start efter deployment

1. **Tjek container logs:**  
   - Åbn **Microsoft Foundry** sidebar → udvid **Hosted Agents (Preview)** → klik på din agent → udvid versionen → **Container Details** → **Logs**.  
   - Kig efter Python stack traces eller manglende modul-fejl.

2. **Almindelige container-startfejl:**

   | Fejl i logs | Årsag | Løsning |
   |-------------|--------|---------|
   | `ModuleNotFoundError` | `requirements.txt` mangler en pakke | Tilføj pakken, deploy igen |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` env vars ikke sat | Opdater `agent.yaml` → `environment_variables` sektionen |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ikke konfigureret | Foundry sætter dette automatisk - sørg for at deploye via extension |
   | `OSError: port 8088 already in use` | Dockerfile eksponerer forkert port eller portkonflikt | Bekræft `EXPOSE 8088` i Dockerfile og `CMD ["python", "main.py"]` |
   | Container afslutter med kode 1 | Ikke-håndteret undtagelse i `main()` | Test lokalt først ([Modul 5](05-test-locally.md)) for at fange fejl før deployment |

3. **Deploy igen efter rettelse:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → vælg samme agent → deploy ny version.

### Deployment tager for lang tid

Multi-agent containere tager længere tid at starte, fordi de opretter 4 agent-instanser ved opstart. Normale opstartstider:

| Fase | Forventet varighed |
|-------|-------------------|
| Byg container image | 1-3 minutter |
| Push image til ACR | 30-60 sekunder |
| Container start (single agent) | 15-30 sekunder |
| Container start (multi-agent) | 30-120 sekunder |
| Agent tilgængelig i Playground | 1-2 minutter efter "Started" |

> Hvis status "Pending" fortsætter i mere end 5 minutter, tjek container logs for fejl.

---

## RBAC og tilladelsesproblemer

### `403 Forbidden` eller `AuthorizationFailed`

Du skal have rollen **[Azure AI User](https://aka.ms/foundry-ext-project-role)** på dit Foundry projekt:

1. Gå til [Azure Portal](https://portal.azure.com) → din Foundry **projekt**-ressource.  
2. Klik på **Access control (IAM)** → **Role assignments**.  
3. Søg efter dit navn → bekræft at **Azure AI User** er listet.  
4. Hvis mangler: **Tilføj** → **Add role assignment** → søg efter **Azure AI User** → tildel din konto.

Se dokumentationen [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) for detaljer.

### Model deployment ikke tilgængelig

Hvis agenten returnerer modellrelaterede fejl:

1. Bekræft modellen er deployet: Foundry sidebar → udvid projekt → **Models** → tjek for `gpt-4.1-mini` (eller din model) med status **Succeeded**.  
2. Bekræft deploymentsnavn matcher: sammenlign `MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiske deploymentnavn i sidebar.  
3. Hvis deployment er udløbet (free tier): redeploy fra [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector problemer

### Inspector åbner men viser "Disconnected"

1. Bekræft serveren kører: tjek for "Server running on http://localhost:8088" i terminalen.  
2. Tjek port `5679`: Inspector forbinder via debugpy på port 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Genstart serveren og åbn Inspector igen.

### Inspector viser delvist svar

Multi-agent svar er lange og streames gradvist. Vent på at det fulde svar er færdigt (kan tage 30-60 sekunder afhængigt af antal gap cards og MCP værktøjskald).

Hvis svaret konsekvent afbrydes:  
- Tjek at GapAnalyzer instruktionerne har `CRITICAL:` blokken, som forhindrer sammenlægning af gap cards.  
- Tjek din models token-limit - `gpt-4.1-mini` understøtter op til 32K output tokens, hvilket bør være tilstrækkeligt.

---

## Performance tips

### Langsomme svar

Multi-agent workflows er inherent langsommere end single-agent grundet sekventielle afhængigheder og MCP værktøjskald.

| Optimering | Hvordan | Effekt |
|------------|---------|--------|
| Reducer MCP kald | Sænk `max_results` parameter i værktøjet | Færre HTTP round-trips |
| Forenkle instruktioner | Kortere, mere fokuserede agent-prompts | Hurtigere LLM inferens |
| Brug `gpt-4.1-mini` | Hurtigere end `gpt-4.1` til udvikling | Ca. 2x hastighedsforbedring |
| Reducer detalje i gap cards | Forenkle gap card format i GapAnalyzer instruktioner | Mindre output at generere |

### Typiske svartider (lokalt)

| Konfiguration | Forventet tid |
|---------------|--------------|
| `gpt-4.1-mini`, 3-5 gap cards | 30-60 sekunder |
| `gpt-4.1-mini`, 8+ gap cards | 60-120 sekunder |
| `gpt-4.1`, 3-5 gap cards | 60-120 sekunder |
---

## Få hjælp

Hvis du sidder fast efter at have prøvet rettelserne ovenfor:

1. **Tjek serverlogfilerne** - De fleste fejl giver en Python stack trace i terminalen. Læs den fulde traceback.
2. **Søg efter fejlmeddelelsen** - Kopiér fejlteksten og søg i [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Opret et issue** - Opret et issue på [workshop-repositoriet](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) med:
   - Fejlmeddelelsen eller en skærmbillede
   - Dine pakkeversioner (`pip list | Select-String "agent-framework"`)
   - Din Python-version (`python --version`)
   - Om problemet er lokalt eller efter udrulning

---

### Checkpoint

- [ ] Du kan identificere og rette de mest almindelige multi-agent fejl ved hjælp af hurtig reference-tabellen
- [ ] Du ved, hvordan man tjekker og retter `.env` konfigurationsproblemer
- [ ] Du kan verificere, at pakkeversioner matcher den krævede matrix
- [ ] Du forstår MCP logposter og kan diagnosticere fejlfunktioner i værktøjet
- [ ] Du ved, hvordan man tjekker containerlogfiler for udrulningsfejl
- [ ] Du kan verificere RBAC-roller i Azure-portalen

---

**Forrige:** [07 - Verify in Playground](07-verify-in-playground.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:  
Dette dokument er oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår ved brug af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->