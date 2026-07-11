# Modul 8 - Felsökning

Den här modulen täcker vanliga fel, lösningar och felsökningsstrategier specifika för multi-agent-flödet.

## Problem med agentutdata

### GapAnalyzer säger ”Jag har fortfarande inte matchande rapport”

**Symptom:** GapAnalyzers svar ber dig klistra in en matchande rapport med ”Saknade färdigheter” och ”Certifieringsluckor.” Detta händer även när du skickat både ett CV och en jobbannons.

**Orsak:** JD-texten skickades inte vidare till JD Agent. Med `context_mode="last_agent"` är `resume_executor` den enda exekutören som någonsin ser användarens ursprungliga meddelande. Om `RESUME_PARSER_INSTRUCTIONS` inte inkluderar JD-texten i sin output har JD Agent inget JD att tolka, MatchingAgent kan inte beräkna en passningspoäng och GapAnalyzer får en meningslös input.

**Diagnos:**

I serverloggarna, leta efter MatchingAgent-spannet. Om det innehåller:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pass-through saknas eller är bruten.

**Åtgärd:** Bekräfta att `RESUME_PARSER_INSTRUCTIONS` i `main.py` innehåller en `[JOB DESCRIPTION PASS-THROUGH]`-sektion och regeln:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bekräfta också att `JOB_DESCRIPTION_INSTRUCTIONS` innehåller en `[PARSED RESUME PASS-THROUGH]` vidarebefordringsregel:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Om någon av instruktionsblocken är en stub från scaffold-wizard, ersätt den med fullständig version från [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent ger ut ”Kan inte beräkna passningspoäng - inget JD tillhandahållet”

Detta har samma grundorsak som ovan. MatchingAgent fick JD Agents output men `[PARSED RESUME PASS-THROUGH]`-sektionen saknades eller var tom, så den kunde inte jämföra de två profilerna. Bekräfta:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inkluderar vidarebefordringsregeln: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` instruerar agenten att leta efter `[JD REQUIREMENTS]` och `[PARSED RESUME PASS-THROUGH]` sektioner.

Ersätt båda instruktionsblocken med fullständiga versioner från [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Svaret visas två gånger

**Symptom:** GapAnalyzer-utdata (eller hela pipeline-utdata) visas två gånger i Agent Inspectors svar.

**Orsak:** `WorkflowBuilder` använder OR-semantik för inkommande kanter – en nedströms exekutör aktiveras så snart **någon** föregångare är klar. Om `matching_executor` har två inkommande kanter (en från `resume_executor` och en från `jd_executor`), aktiveras den två gånger: en gång när ResumeParser är klar och en gång när JD Agent är klar. GapAnalyzer körs då också två gånger.

**Åtgärd:** Säkerställ att `WorkflowBuilder`-grafen är en strikt sekventiell pipeline utan fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # INTE från resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Om du har en överflödig rad `.add_edge(resume_executor, matching_executor)`, ta bort den. `[PARSED RESUME PASS-THROUGH]`-vidarebefordringen i JD Agents output ger redan MatchingAgent tillgång till CV:t.

---

## Miljö- och konfigurationsproblem

### Saknade eller felaktiga `.env`-värden

`.env`-filen måste finnas i katalogen `PersonalCareerCopilot/` (samma nivå som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Förväntat innehåll i `.env`:

**Väg A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Väg B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Båda vägar använder `FOUNDRY_PROJECT_ENDPOINT`. Värdet skiljer sig: cloud använder en `https://` Foundry-endpoint; local använder `http://localhost:5273/v1`. Kör `foundry model list` för att bekräfta exakt modellalias för Väg B.

> **Hitta ditt `FOUNDRY_PROJECT_ENDPOINT`:** 
- Öppna **Foundry Toolkit** sidofält i VS Code → högerklicka på ditt projekt → **Copy Project Endpoint**.
- Eller gå till [Azure Portal](https://portal.azure.com) → ditt Foundry-projekt → **Översikt** → **Projektendpoint**.

> **Hitta ditt `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** I Foundry Toolkit sidofält, expandera ditt projekt → **Modeller** → hitta ditt distribuerade modellnamn (t.ex. `gpt-4.1-mini`).

### Prioritering av miljövariabler

`main.py` använder `load_dotenv(override=True)`, vilket innebär:

| Prioritet | Källa | Vinner när båda är satta? |
|----------|--------|------------------------|
| 1 (högst) | `.env`-fil | Ja |
| 2 | Shell / container-miljövariabel | Används när samma nyckel inte finns i `.env` |

Vid lokal utveckling är `.env` sanningskällan (redigering av `.env` påverkar körningar omedelbart). Vid hostad distribution injicerar Foundry miljövariabler på containernivå; eftersom `.env` inte är del av den deployade imagen för denna labbmiljö, används de injicerade container-värdena.

---

## Versionskompatibilitet

### Paketversionsmatris

Multi-agent-flödet kräver specifika paketversioner. Mismatchade versioner orsakar körningsfel.

| Paket | Krävd version | Kontrollkommando |
|---------|-----------------|---------------|
| `agent-framework-foundry` | senaste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | senaste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | senaste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Vanliga versionsfel

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Åtgärd: installera om agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Åtgärd: uppgradera mcp-paketet
pip install mcp --upgrade
```

### Verifiera alla versioner på en gång

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Förväntad output:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Distributionsproblem

### Containern startar inte efter distribution

1. **Kontrollera containerloggar:**
   - Öppna **Foundry Toolkit** sidofält → expandera **Hosted Agents (Preview)** → klicka på din agent → expandera versionen → **Container Details** → **Logs**.
   - Leta efter Python stacktraces eller modulfel.

2. **Vanliga orsaker till container-startfel:**

   | Fel i loggar | Orsak | Åtgärd |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` saknar ett paket | Lägg till paketet, distribuera om |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` eller `.env` miljövariabler inte satta | Uppdatera `agent.yaml` → `environment_variables`-sektionen (hostad) eller `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ej konfigurerad | Foundry sätter detta automatiskt - säkerställ att du distribuerar via extensionen |
   | `OSError: port 8088 already in use` | Dockerfile exponerar fel port eller portkonflikt | Kontrollera `EXPOSE 8088` i Dockerfile och `CMD ["python", "main.py"]` |
   | Container avslutas med kod 1 | Ohanterat undantag i `main()` | Testa lokalt först ([Modul 5](05-test-locally.md)) för att fånga fel före distribution |

3. **Distribuera om efter fix:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → välj samma agent → distribuera ny version.

### Distribution tar för lång tid

Multi-agent-containrar tar längre tid att starta eftersom de skapar 4 agentinstanser vid start. Normala starttider:

| Steg | Förväntad varaktighet |
|-------|------------------|
| Containerbildbyggnad | 1-3 minuter |
| Bildpush till ACR | 30-60 sekunder |
| Containers start (enkel agent) | 15-30 sekunder |
| Containers start (multi-agent) | 30-120 sekunder |
| Agent tillgänglig i Playground | 1-2 minuter efter ”Started” |

> Om ”Pending”-statusen kvarstår längre än 5 minuter, kontrollera containerloggar för fel.

---

## RBAC- och behörighetsproblem

### `403 Forbidden` eller `AuthorizationFailed`

Du behöver rollen **[Foundry User](https://aka.ms/foundry-ext-project-role)** på ditt Foundry-projekt (tidigare kallad **Azure AI User** - roll-ID oförändrat):

1. Gå till [Azure Portal](https://portal.azure.com) → din Foundry **project** resurs.
2. Klicka **Access control (IAM)** → **Rolltilldelningar**.
3. Sök efter ditt namn → bekräfta att **Foundry User** (eller den gamla beteckningen **Azure AI User**) är listad.
4. Om saknas: **Lägg till** → **Lägg till rolltilldelning** → sök efter **Foundry User** → tilldela till ditt konto.

Se dokumentationen [RBAC för Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) för detaljer.

### Modelldistribution ej åtkomlig

Om agenten returnerar modellrelaterade fel:

1. Bekräfta att modellen är distribuerad: Foundry sidofält → expandera projekt → **Modeller** → kontrollera att `gpt-4.1-mini` (eller din modell) har status **Succeeded**.
2. Bekräfta att distributionsnamnet matchar: jämför `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiska distributionsnamnet i sidofältet.
3. Om distributionen gått ut (gratisnivå): distribuera om från [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local-problem (Väg B)

### Foundry Local-tjänst körs inte

```powershell
# Kontrollera status
foundry local status

# Starta tjänsten om den är stoppad
foundry local start
```

| Symptom | Orsak | Åtgärd |
|---------|-------|-----|
| Hälsokontroll returnerar `503` | Tjänsten är inte startad | Kör `foundry local start` eller klicka **Start** i Foundry Toolkit sidofält |
| Hälsokontroll timeout | Modell laddar fortfarande | Vänta 30–60 s efter start; större modeller tar längre tid |
| `StatusCode: 404` på `/v1/health` | Fel port | Standard är `5273`. Kontrollera `foundry local status` för aktuell port |
| Otillräckliga resurser | Foundry Local behöver ~4 GB RAM ledigt | Stäng andra applikationer |
| Modellnedladdning misslyckas | Lågt diskutrymme | Modeller är 2–8 GB. Frigör utrymme, sedan `foundry model pull <namn>` |

### Modellnamnsdiscrepans

```powershell
# Lista nedladdade modeller och deras exakta alias
foundry model list
```

Sätt `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` till exakt alias som visas (t.ex. `phi-4-mini`, inte `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` vid lokal körning (Väg B)

Labbets `main.py` använder `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local kräver att denna variabel pekar på den lokala tjänsten - **inte** `AZURE_AI_PROJECT_ENDPOINT`. Säkerställ att din `.env` innehåller:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-verktyget gör fortfarande ett utgående anrop (Väg B)

Detta är förväntat. Verktyget `search_microsoft_learn_for_plan` hämtar lärresurser från `https://learn.microsoft.com/api/mcp`. **Endast frågan om färdighetsnamn** skickas över nätverket – CV och JD-text processas helt lokalt på din enhet och skickas aldrig iväg. Om full offline-drift krävs, lägg till en `try/except` fallback i verktyget som returnerar en statisk `learn.microsoft.com` URL när endpointen är otillgänglig.

---

## Få hjälp

Om du fastnar efter att ha provat ovanstående lösningar:

1. **Kontrollera serverloggarna** - De flesta fel ger en Python stacktrace i terminalen. Läs hela tracebacken.
2. **Sök på felmeddelandet** - Kopiera feltexten och sök i [Microsoft Q&A för Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Öppna ett ärende** - Skapa ett issue i [workshop-repositoryt](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) med:
   - Felmeddelandet eller skärmdump
   - Dina paketversioner (`pip list | Select-String "agent-framework"`)
   - Din Python-version (`python --version`)
   - Om problemet är lokalt eller efter distribution

---

### Kontrollpunkt

- [ ] Du vet hur du kontrollerar och åtgärdar `.env`-konfigurationsproblem
- [ ] Du kan verifiera paketversioner mot kravmatrisen
- [ ] Du vet hur du kontrollerar containerloggar för distributionsfel
- [ ] Du kan verifiera RBAC-roller i Azure-portalen

---

**Föregående:** [07 - Verifiera i Playground](07-verify-in-playground.md) · **Nästa:** [09 - Sammanfattning →](09-summary.md) · **Start:** [Lab 02 README](../README.md) · [Workshop Startsida](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->