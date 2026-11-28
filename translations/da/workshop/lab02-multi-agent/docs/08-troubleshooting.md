# Modul 8 - Fejlfinding

Denne modul dækker almindelige fejl, rettelser og fejlfinding strategier specifikke for multi-agent workflowet.

## Problemer med agent output

### GapAnalyzer siger “Jeg har stadig ikke den matchende rapport”

**Symptom:** GapAnalyzer’s svar beder dig indsætte en matchende rapport med “Manglende færdigheder” og “Certificeringsgab.” Dette sker selvom du har sendt både et CV og en jobbeskrivelse.

**Årsag:** JD teksten blev ikke videregivet til JD Agent downstream. Med `context_mode="last_agent"` er `resume_executor` den eneste executor, der nogensinde ser brugerens oprindelige besked. Hvis `RESUME_PARSER_INSTRUCTIONS` ikke inkluderer JD teksten i sit output, har JD Agent ingen JD at analysere, MatchingAgent kan ikke beregne en match score, og GapAnalyzer modtager et meningsløst input.

**Diagnose:**

I server loggene, søg efter MatchingAgent span. Hvis den indeholder:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
er pass-through enten manglende eller ødelagt.

**Løsning:** Bekræft at `RESUME_PARSER_INSTRUCTIONS` i `main.py` indeholder en `[JOB DESCRIPTION PASS-THROUGH]` sektion og reglen:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bekræft også at `JOB_DESCRIPTION_INSTRUCTIONS` indeholder en `[PARSED RESUME PASS-THROUGH]` relay regel:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Hvis en af disse instruktionsblokke er en stub fra scaffold guiden, erstat den med den komplette version fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent outputter “Kan ikke beregne fit score - ingen JD angivet”

Dette er samme rodårsag som ovenfor. MatchingAgent modtog JD Agent’s output men `[PARSED RESUME PASS-THROUGH]` sektionen manglede eller var tom, så den kunne ikke sammenligne de to profiler. Bekræft:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inkluderer relay reglen: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` fortæller agenten at søge efter `[JD REQUIREMENTS]` og `[PARSED RESUME PASS-THROUGH]` sektioner.

Erstat begge instruktionsblokke med de komplette versioner fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Svaret vises to gange

**Symptom:** GapAnalyzer output (eller hele pipeline output) vises to gange i Agent Inspector svaret.

**Årsag:** `WorkflowBuilder` bruger OR-semantik for indgående kanter - en downstream executor aktiveres så snart **en hvilken som helst** forgænger fuldfører. Hvis `matching_executor` har to indgående kanter (en fra `resume_executor` og en fra `jd_executor`), aktiveres den to gange: en gang når ResumeParser er færdig og igen når JD Agent er færdig. GapAnalyzer kører derefter også to gange.

**Løsning:** Sikr at `WorkflowBuilder` grafen er en strengt sekventiel pipeline uden fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Hvis du har en løs `.add_edge(resume_executor, matching_executor)` linje, fjern den. `[PARSED RESUME PASS-THROUGH]` relay i JD Agent’s output giver allerede MatchingAgent adgang til CV'et.

---

## Miljø- og konfigurationsproblemer

### Manglende eller forkerte `.env` værdier

Filen `.env` skal være i `PersonalCareerCopilot/` mappen (samme niveau som `main.py`):

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

> Begge stier bruger `FOUNDRY_PROJECT_ENDPOINT`. Værdien varierer: cloud bruger en `https://` Foundry endpoint; lokal bruger `http://localhost:5273/v1`. Kør `foundry model list` for at bekræfte den præcise modelalias for Sti B.

> **Find din `FOUNDRY_PROJECT_ENDPOINT`:** 
- Åbn **Foundry Toolkit** sidebjælke i VS Code → højreklik på dit projekt → **Kopier Projekt Endpoint**. 
- Eller gå til [Azure Portal](https://portal.azure.com) → dit Foundry projekt → **Oversigt** → **Projekt endpoint**.

> **Find din `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** I Foundry Toolkit sidebjælken, udvid dit projekt → **Modeller** → find dit udrullede modelnavn (f.eks. `gpt-4.1-mini`).

### Prioritering af env var

`main.py` bruger `load_dotenv(override=True)`, hvilket betyder:

| Prioritet | Kilde | Vinder når begge er sat? |
|----------|--------|------------------------|
| 1 (højeste) | `.env` fil | Ja |
| 2 | Shell / container miljøvariabel | Bruges når samme nøgle ikke findes i `.env` |

I lokal udvikling gør dette `.env` til sandhedskilden (ændring i `.env` påvirker straks kørsel). I hostet deployment injicerer Foundry miljøvariable på container niveau; da `.env` ikke er del af det deployerede image for dette lab setup, bruges de injicerede container værdier.

---

## Versionskompatibilitet

### Pakke versionsmatrix

Multi-agent workflowet kræver specifikke pakkeversioner. Uoverensstemmende versioner forårsager runtime fejl.

| Pakke | Krævet version | Tjek kommando |
|---------|-----------------|---------------|
| `agent-framework-foundry` | seneste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | seneste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | seneste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Almindelige versionsfejl

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Bekræft alle versioner på én gang

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

1. **Tjek container logs:**
   - Åbn **Foundry Toolkit** sidebjælke → under dit projekt, klik **Agents** → **Hosted Agent** fanen → klik på din agent. Tjek **Status** under **Detaljer** fanen, åbn derefter **Playground** fanen og brug **Logs** fanen i **Session Detaljer** panelet for at se containerens output.
   - Kig efter Python stack traces eller fejl om manglende moduler.

2. **Almindelige container startup fejl:**

   | Fejl i logs | Årsag | Løsning |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` mangler en pakke | Tilføj pakken, deploy igen |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` eller `.env` env vars ikke sat | Opdater `agent.yaml` → `environment_variables` sektion (hosted) eller `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ikke konfigureret | Foundry sætter dette automatisk - sikr du deployer via extensionen |
   | `OSError: port 8088 already in use` | Dockerfile eksponerer forkert port eller port konflikt | Bekræft `EXPOSE 8088` i Dockerfile og `CMD ["python", "main.py"]` |
   | Container lukker med kode 1 | Ubehandlet undtagelse i `main()` | Test lokalt først ([Modul 5](05-test-locally.md)) for at fange fejl før deployment |

3. **Deploy igen efter rettelse:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → vælg samme agent → deploy en ny version.

### Deployment tager for lang tid

Multi-agent containere tager længere tid at starte fordi de opretter 4 agent instanser ved opstart. Normale opstartstider:

| Trin | Forventet varighed |
|-------|------------------|
| Container image build | 1-3 minutter |
| Image push til ACR | 30-60 sekunder |
| Container start (single agent) | 15-30 sekunder |
| Container start (multi-agent) | 30-120 sekunder |
| Agent tilgængelig i Playground | 1-2 minutter efter "Started" |

> Hvis "Pending" status fortsætter over 5 minutter, tjek container logs for fejl.

---

## RBAC- og tilladelsesproblemer

### `403 Forbidden` eller `AuthorizationFailed`

Du skal have **[Foundry User](https://aka.ms/foundry-ext-project-role)** rollen på dit Foundry projekt (tidligere kaldet **Azure AI User** - rolle ID uændret):

1. Gå til [Azure Portal](https://portal.azure.com) → dit Foundry **projekt** resource.
2. Klik **Access control (IAM)** → **Role assignments**.
3. Søg efter dit navn → bekræft at **Foundry User** (eller den tidligere betegnelse **Azure AI User**) er listet.
4. Hvis mangler: **Tilføj** → **Tilføj rolle tildeling** → søg efter **Foundry User** → tildel til din konto.

Se dokumentationen [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) for detaljer.

### Model deployment ikke tilgængelig

Hvis agenten returnerer modelrelaterede fejl:

1. Bekræft modellen er udrullet: Foundry sidebjælke → udvid projekt → **Modeller** → tjek for `gpt-4.1-mini` (eller din model) med status **Succeeded**.
2. Bekræft udrulningsnavnet matcher: sammenlign `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiske udrulningsnavn i sidebjælken.
3. Hvis udrulningen er udløbet (gratis tier): deploy igen fra [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problemer (Sti B)

### Foundry Local service kører ikke

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Symptom | Årsag | Løsning |
|---------|-------|---------|
| Health check returnerer `503` | Service ikke startet | `foundry local start` eller klik **Start** i Foundry Toolkit sidebjælken |
| Health check timeout | Model indlæses stadig | Vent 30–60 sekunder efter start; større modeller tager længere tid |
| `StatusCode: 404` på `/v1/health` | Forkert port | Standard er `5273`. Tjek `foundry local status` for den faktiske port |
| Utilstrækkelige ressourcer | Foundry Local kræver ~4 GB RAM ledigt | Luk andre applikationer |
| Model download fejler | Lav diskplads | Modeller er 2–8 GB. Frigør plads, derefter `foundry model pull <name>` |

### Modelnavn matcher ikke

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Sæt `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` til den præcise alias vist (f.eks. `phi-4-mini`, ikke `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ved lokal kørsel (Sti B)

Lab’ets `main.py` bruger `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local kræver denne variabel peger på den lokale service - **ikke** `AZURE_AI_PROJECT_ENDPOINT`. Sørg for at din `.env` indeholder:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP værktøj laver stadig udgående kald (Sti B)

Dette er forventet. `search_microsoft_learn_for_plan` værktøjet henter læringsressourcer fra `https://learn.microsoft.com/api/mcp`. **Kun forespørgslen på færdighedsnavn** rejser over netværket - CV og JD tekst behandles fuldstændigt på din enhed og overføres aldrig. Hvis fuld offline drift kræves, tilføj en `try/except` fallback i værktøjet der returnerer en statisk `learn.microsoft.com` URL når endpoint ikke er tilgængeligt.

---

## Få hjælp

Hvis du sidder fast efter at have prøvet ovenstående rettelser:

1. **Tjek server logs** - De fleste fejl producerer en Python stack trace i terminalen. Læs hele trace-back.
2. **Søg efter fejlmeddelelsen** - Kopier fejlteksten og søg i [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Åbn en sag** - Opret en sag i [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) med:
   - Fejlmeddelelsen eller skærmbillede
   - Dine pakke versioner (`pip list | Select-String "agent-framework"`)
   - Din Python version (`python --version`)
   - Om problemet er lokalt eller efter deployment

---

### Checkpoint

- [ ] Du ved hvordan du tjekker og retter `.env` konfigurationsproblemer
- [ ] Du kan verificere pakke versioner matcher den nødvendige matrix
- [ ] Du ved hvordan du tjekker container logs for deployment fejl
- [ ] Du kan verificere RBAC roller i Azure Portalen

---

**Forrige:** [07 - Verify in Playground](07-verify-in-playground.md) · **Næste:** [09 - Summary →](09-summary.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->