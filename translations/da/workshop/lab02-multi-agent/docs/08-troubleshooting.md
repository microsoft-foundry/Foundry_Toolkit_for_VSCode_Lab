# Modul 8 - Fejlfinding

Dette modul dækker almindelige fejl, løsninger og fejlsøgningsstrategier specifikke for multi-agent workflowet.

## Problemer med agentens output

### GapAnalyzer siger "Jeg har stadig ikke den matchende rapport"

**Symptom:** GapAnalyzer's svar beder dig indsætte en matchende rapport med "Missing Skills" og "Certification Gaps." Dette sker selvom du har sendt både CV og jobbeskrivelse.

**Årsag:** JD-teksten blev ikke sendt videre til JD Agent. Med `context_mode="last_agent"` er `resume_executor` den eneste eksekutor, der nogensinde ser brugerens originale besked. Hvis `RESUME_PARSER_INSTRUCTIONS` ikke inkluderer JD-teksten i sit output, har JD Agent ingen JD at analysere, MatchingAgent kan ikke beregne en fit score, og GapAnalyzer modtager en meningsløs input.

**Diagnose:**

I serverlogs, kig efter MatchingAgent-spanet. Hvis det indeholder:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pass-through mangler eller er brudt.

**Løsning:** Bekræft at `RESUME_PARSER_INSTRUCTIONS` i `main.py` indeholder en `[JOB DESCRIPTION PASS-THROUGH]` sektion og reglen:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bekræft også, at `JOB_DESCRIPTION_INSTRUCTIONS` indeholder en `[PARSED RESUME PASS-THROUGH]` relay-regel:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Hvis en af instruktionsblokkene er en stub fra scaffold guiden, erstat den med den komplette version fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent udskriver "Cannot compute fit score - no JD provided"

Dette er samme rodårsag som ovenfor. MatchingAgent modtog JD Agent’s output men `[PARSED RESUME PASS-THROUGH]` sektionen manglede eller var tom, så den kunne ikke sammenligne de to profiler. Bekræft:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inkluderer relay-reglen: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` fortæller agenten at kigge efter `[JD REQUIREMENTS]` og `[PARSED RESUME PASS-THROUGH]` sektioner.

Erstat begge instruktionsblokke med de komplette versioner fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Svaret optræder to gange

**Symptom:** GapAnalyzer output (eller hele pipeline-outputtet) vises to gange i Agent Inspector svaret.

**Årsag:** `WorkflowBuilder` bruger OR-semantik for indgående kanter - en downstream eksekutor kører så snart **en som helst** forløber fuldfører. Hvis `matching_executor` har to indgående kanter (en fra `resume_executor` og en fra `jd_executor`), kører den to gange: en gang når ResumeParser afsluttes og igen når JD Agent afsluttes. GapAnalyzer kører så også to gange.

**Løsning:** Sørg for at `WorkflowBuilder` grafen er en strengt sekventiel pipeline uden fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # IKKE fra resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Hvis du har en løs `.add_edge(resume_executor, matching_executor)` linje, fjern den. `[PARSED RESUME PASS-THROUGH]` relay i JD Agent’s output giver allerede MatchingAgent adgang til resumeet.

---

## Miljø- og konfigurationsproblemer

### Manglende eller forkerte `.env` værdier

`.env` filen skal være i `PersonalCareerCopilot/` mappen (samme niveau som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Forventet `.env` indhold:

**Sti A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Sti B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Begge stier bruger `FOUNDRY_PROJECT_ENDPOINT`. Værdien varierer: cloud bruger en `https://` Foundry endpoint; lokal bruger `http://localhost:5273/v1`. Kør `foundry model list` for at bekræfte den præcise model alias for Sti B.

> **Find din `FOUNDRY_PROJECT_ENDPOINT`:** 
- Åbn **Foundry Toolkit** sidebjælken i VS Code → højreklik på dit projekt → **Copy Project Endpoint**. 
- Eller gå til [Azure Portal](https://portal.azure.com) → dit Foundry projekt → **Oversigt** → **Project endpoint**.

> **Find dit `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** I Foundry Toolkit sidebjælken, udvid dit projekt → **Models** → find dit udrullede modelnavn (fx `gpt-4.1-mini`).

### Prioritet for miljøvariabler

`main.py` bruger `load_dotenv(override=True)`, hvilket betyder:

| Prioritet | Kilde | Vinder når begge er sat? |
|----------|--------|-------------------------|
| 1 (højeste) | `.env` fil | Ja |
| 2 | Shell / container miljøvariabel | Bruges når samme nøgle ikke findes i `.env` |

Ved lokal udvikling er `.env` kilden til sandhed (ændringer i `.env` påvirker straks kørsel). Ved hosting-integration injicerer Foundry miljøvariabler på container-niveau; da `.env` ikke er en del af det deployerede image i denne lab, bruges de injicerede container-værdier.

---

## Versionskompatibilitet

### Matrice for pakkeversioner

Multi-agent workflowet kræver specifikke pakkeversioner. Uoverensstemmende versioner forårsager runtime-fejl.

| Pakke | Påkrævet version | Tjek-kommando |
|-------|-----------------|---------------|
| `agent-framework-foundry` | seneste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | seneste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | seneste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Almindelige version-fejl

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Ret: geninstaller agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Løsning: opgrader mcp-pakken
pip install mcp --upgrade
```

### Verificer alle versioner på én gang

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Forventet output:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Deploymentsproblemer

### Container starter ikke efter deployment

1. **Tjek containerlogs:**
   - Åbn **Foundry Toolkit** sidebjælken → udvid **Hosted Agents (Preview)** → klik på din agent → udvid versionen → **Container Details** → **Logs**.
   - Kig efter Python stack traces eller manglende modul fejl.

2. **Almindelige container startfejl:**

   | Fejl i logs | Årsag | Løsning |
   |-------------|--------|---------|
   | `ModuleNotFoundError` | `requirements.txt` mangler en pakke | Tilføj pakken, deploy igen |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` eller `.env` miljøvariabler ikke sat | Opdater `agent.yaml` → `environment_variables` sektion (hosted) eller `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ikke konfigureret | Foundry sætter dette automatisk - sørg for deployment via extension |
   | `OSError: port 8088 already in use` | Dockerfile eksponerer forkert port eller portkonflikt | Bekræft `EXPOSE 8088` i Dockerfile og `CMD ["python", "main.py"]` |
   | Container afsluttes med kode 1 | Ubehandlet undtagelse i `main()` | Test lokalt først ([Modul 5](05-test-locally.md)) for at fange fejl før deployment |

3. **Deploy igen efter rettelse:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → vælg samme agent → deploy ny version.

### Deployment tager for lang tid

Multi-agent containere tager længere tid at starte, fordi de opretter 4 agent-instancer ved opstart. Normale ventetider:

| Trin | Forventet varighed |
|------|------------------|
| Container image build | 1-3 minutter |
| Image push til ACR | 30-60 sekunder |
| Container start (enkelt agent) | 15-30 sekunder |
| Container start (multi-agent) | 30-120 sekunder |
| Agent tilgængelig i Playground | 1-2 minutter efter "Started" |

> Hvis status "Pending" fortsætter over 5 minutter, tjek containerlogs for fejl.

---

## RBAC- og tilladelsesproblemer

### `403 Forbidden` eller `AuthorizationFailed`

Du skal have rollen **[Foundry User](https://aka.ms/foundry-ext-project-role)** på dit Foundry projekt (tidligere kaldt **Azure AI User** - rolle ID er uændret):

1. Gå til [Azure Portal](https://portal.azure.com) → din Foundry **projekt** ressource.
2. Klik **Access control (IAM)** → **Role assignments**.
3. Søg efter dit navn → bekræft at **Foundry User** (eller det gamle label **Azure AI User**) står på listen.
4. Hvis det mangler: **Tilføj** → **Add role assignment** → søg efter **Foundry User** → tildel til din konto.

Se dokumentationen for [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) for detaljer.

### Model deployment ikke tilgængelig

Hvis agenten returnerer model-relaterede fejl:

1. Bekræft modellen er deployeret: Foundry sidebar → udvid projekt → **Models** → tjek for `gpt-4.1-mini` (eller din model) med status **Succeeded**.
2. Bekræft deployment navnet matcher: sammenlign `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiske deployment navn i sidebjælken.
3. Hvis deployment er udløbet (gratis tier): deploy igen fra [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problemer (Sti B)

### Foundry Local tjeneste kører ikke

```powershell
# Tjek status
foundry local status

# Start tjenesten, hvis den er stoppet
foundry local start
```

| Symptom | Årsag | Løsning |
|---------|--------|---------|
| Health check returnerer `503` | Tjenesten er ikke startet | `foundry local start` eller klik **Start** i Foundry Toolkit sidebjælken |
| Health check timeout | Model loader stadig | Vent 30–60 sekunder efter start; større modeller tager længere tid |
| `StatusCode: 404` på `/v1/health` | Forkert port | Standard er `5273`. Tjek `foundry local status` for aktuel port |
| Utilstrækkelige ressourcer | Foundry Local har brug for ~4 GB ledig RAM | Luk andre programmer |
| Model download fejler | Lav diskplads | Modeller er 2–8 GB. Frigør plads, kør så `foundry model pull <name>` |

### Modelnavn mismatch

```powershell
# Liste over downloadede modeller og deres præcise aliaser
foundry model list
```

Sæt `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` til det præcise alias vist (fx `phi-4-mini`, ikke `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ved lokal kørsel (Sti B)

Lab'ets `main.py` bruger `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local kræver, at denne variabel peger på den lokale tjeneste - **ikke** `AZURE_AI_PROJECT_ENDPOINT`. Sørg for at din `.env` indeholder:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP værktøjet laver stadig en outbound kald (Sti B)

Dette er forventet. `search_microsoft_learn_for_plan` værktøjet henter læringsressourcer fra `https://learn.microsoft.com/api/mcp`. **Kun skill-navns forespørgslen** går over netværket – CV og JD tekst behandles helt lokalt og sendes aldrig. Hvis fuld offline funktionalitet er nødvendig, tilføj en `try/except` fallback i værktøjet, som returnerer en statisk `learn.microsoft.com` URL når endpoint ikke er tilgængelig.

---

## Få hjælp

Hvis du sidder fast efter at have prøvet ovenstående rettelser:

1. **Tjek serverlogs** - De fleste fejl giver en Python stack trace i terminalen. Læs hele tracebacken.
2. **Søg efter fejlmeddelelsen** - Kopier fejlteksten og søg i [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Opret en issue** - Opret en issue i [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) med:
   - Fejlmeddelelsen eller skærmbillede
   - Dine pakkeversioner (`pip list | Select-String "agent-framework"`)
   - Din Python version (`python --version`)
   - Om problemet er lokalt eller efter deployment

---

### Checkpoint

- [ ] Du ved hvordan du tjekker og retter `.env` konfigurationsproblemer
- [ ] Du kan verificere at pakkeversioner matcher den krævede matrice
- [ ] Du ved hvordan du tjekker containerlogs for deploymentsfejl
- [ ] Du kan verificere RBAC roller i Azure Portal

---

**Forrige:** [07 - Verificer i Playground](07-verify-in-playground.md) · **Næste:** [09 - Opsummering →](09-summary.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->