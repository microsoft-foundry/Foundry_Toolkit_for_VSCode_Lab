# Modul 8 - Felsökning

Denna modul täcker vanliga fel, lösningar och felsökningsstrategier som är specifika för multi-agent arbetsflödet.

## Problem med agentens output

### GapAnalyzer säger ”Jag har fortfarande inte matchande rapport”

**Symptom:** GapAnalyzer:s svar ber dig klistra in en matchande rapport med ”Saknade färdigheter” och ”Certifieringsluckor.” Detta händer även när du har skickat både ett CV och en arbetsbeskrivning.

**Orsak:** JD-texten skickades inte vidare till JD Agent. Med `context_mode="last_agent"` är `resume_executor` den enda exekutorn som någonsin ser användarens ursprungliga meddelande. Om `RESUME_PARSER_INSTRUCTIONS` inte inkluderar JD-texten i sin output har JD Agent ingen JD att tolka, MatchingAgent kan inte beräkna en passningspoäng, och GapAnalyzer får en meningslös input.

**Diagnos:**

I serverloggarna, sök efter MatchingAgent-spannet. Om den innehåller:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
så saknas eller är passeringen trasig.

**Lösning:** Bekräfta att `RESUME_PARSER_INSTRUCTIONS` i `main.py` innehåller en `[JOB DESCRIPTION PASS-THROUGH]`-sektion och regeln:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bekräfta också att `JOB_DESCRIPTION_INSTRUCTIONS` innehåller en `[PARSED RESUME PASS-THROUGH]` vidarebefordringsregel:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Om någon av instruktionsblocken är ett stub från Scaffold Wizard, ersätt den med den kompletta versionen från [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent returnerar ”Kan inte beräkna passningspoäng - ingen JD angiven”

Detta är samma grundorsak som ovan. MatchingAgent mottog JD Agents output men `[PARSED RESUME PASS-THROUGH]`-sektionen saknades eller var tom, så den kunde inte jämföra de två profilerna. Bekräfta:
1. `JOB_DESCRIPTION_INSTRUCTIONS` innehåller vidarebefordringsregeln: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` instruerar agenten att leta efter `[JD REQUIREMENTS]` och `[PARSED RESUME PASS-THROUGH]` sektioner.

Ersätt båda instruktionsblocken med de kompletta versionerna från [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Svaret visas två gånger

**Symptom:** GapAnalyzer-output (eller hela pipeline-output) visas två gånger i Agent Inspector-svaret.

**Orsak:** `WorkflowBuilder` använder OR-semantik för inkommande kanter - en nedströms exekutor aktiveras så fort **någon** föregångare slutförs. Om `matching_executor` har två inkommande kanter (en från `resume_executor` och en från `jd_executor`), körs den två gånger: en gång när ResumeParser är klar och en gång när JD Agent är klar. Då körs även GapAnalyzer två gånger.

**Lösning:** Se till att `WorkflowBuilder`-grafen är en strikt sekventiell pipeline utan fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Om du har en överflödig `.add_edge(resume_executor, matching_executor)`-rad, ta bort den. `[PARSED RESUME PASS-THROUGH]`-vidarebefordringen i JD Agents output ger redan MatchingAgent åtkomst till CV:t.

---

## Miljö- och konfigurationsproblem

### Saknade eller felaktiga `.env` värden

Filen `.env` måste finnas i katalogen `PersonalCareerCopilot/` (på samma nivå som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Förväntat innehåll i `.env`:

**Sökväg A - Foundry Cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Sökväg B - Foundry Lokalt:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Båda sökvägarna använder `FOUNDRY_PROJECT_ENDPOINT`. Värdet skiljer sig: cloud använder en `https://` Foundry-endpoint; lokal använder `http://localhost:5273/v1`. Kör `foundry model list` för att bekräfta exakt modellalias för Sökväg B.

> **Så hittar du ditt `FOUNDRY_PROJECT_ENDPOINT`:** 
- Öppna **Foundry Toolkit** sidofält i VS Code → högerklicka på ditt projekt → **Kopiera projektsendpoint**. 
- Eller gå till [Azure Portal](https://portal.azure.com) → ditt Foundry-projekt → **Översikt** → **Projektsendpoint**.

> **Så hittar du ditt `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** I Foundry Toolkit sidofält, expandera ditt projekt → **Modeller** → hitta ditt distribuerade modellnamn (t.ex., `gpt-4.1-mini`).

### Prioritering av miljövariabler

`main.py` använder `load_dotenv(override=True)`, vilket betyder:

| Prioritet | Källa | Vinner när båda är satta? |
|----------|--------|----------------------------|
| 1 (högst) | `.env` fil | Ja |
| 2 | Shell / container-miljövariabel | Används när samma nyckel saknas i `.env` |

Vid lokal utveckling gör detta `.env` till sanningens källa (ändring i `.env` påverkar körningar omedelbart). Vid hostad distribution injicerar Foundry miljövariabler på containernivå; eftersom `.env` inte är del av den distribuerade bilden för denna laborationssetup används de injicerade container-värdena.

---

## Versionskompatibilitet

### Paketversionsmatris

Multi-agent arbetsflödet kräver specifika paketversioner. Icke-matcherande versioner orsakar körtidsfel.

| Paket | Krävd version | Kontrollkommando |
|---------|---------------|------------------|
| `agent-framework-foundry` | senaste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | senaste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | senaste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Vanliga versionsfel

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

1. **Kolla containerloggar:** 
   - Öppna **Foundry Toolkit** sidofält → under ditt projekt, klicka på **Agents** → fliken **Hosted Agent** → klicka på din agent. Kontrollera **Status** under fliken **Detaljer**, öppna sedan fliken **Playground** och använd fliken **Loggar** i panelen **Sessionsdetaljer** för att se containerns output.
   - Leta efter Python stackspår eller fel på saknade moduler.

2. **Vanliga startup-fel för container:**

   | Fel i loggar | Orsak | Lösning |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` saknar ett paket | Lägg till paketet, distribuera om |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` eller `.env` miljövariabler saknas | Uppdatera `agent.yaml` → `environment_variables` sektion (hostad) eller `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Hanterad identitet inte konfigurerad | Foundry ställer in detta automatiskt - säkerställ att du distribuerar via tillägget |
   | `OSError: port 8088 already in use` | Dockerfile exponerar fel port eller portkonflikt | Verifiera `EXPOSE 8088` i Dockerfile och `CMD ["python", "main.py"]` |
   | Containern avslutas med kod 1 | Ohanterat undantag i `main()` | Testa lokalt först ([Modul 5](05-test-locally.md)) för att upptäcka fel innan distribution |

3. **Distribuera om efter fix:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → välj samma agent → distribuera en ny version.

### Distribution tar för lång tid

Multi-agent containrar tar längre tid på sig att starta eftersom de skapar 4 agentinstanser vid start. Normala starttider:

| Steg | Förväntad tid |
|-------|--------------|
| Containerbildsbygge | 1-3 minuter |
| Push av bild till ACR | 30-60 sekunder |
| Containerstart (enkel agent) | 15-30 sekunder |
| Containerstart (multi-agent) | 30-120 sekunder |
| Agent tillgänglig i Playground | 1-2 minuter efter "Started" |

> Om status "Pending" kvarstår mer än 5 minuter, kontrollera containerloggar för fel.

---

## RBAC och behörighetsproblem

### `403 Forbidden` eller `AuthorizationFailed`

Du behöver rollen **[Foundry User](https://aka.ms/foundry-ext-project-role)** på ditt Foundry-projekt (tidigare kallad **Azure AI User** - roll-ID är oförändrat):

1. Gå till [Azure Portal](https://portal.azure.com) → din Foundry **projekt**resurs.
2. Klicka på **Åtkomstkontroll (IAM)** → **Rolltilldelningar**.
3. Sök efter ditt namn → bekräfta att **Foundry User** (eller den gamla etiketten **Azure AI User**) finns listad.
4. Om saknas: **Lägg till** → **Lägg till rolltilldelning** → sök efter **Foundry User** → tilldela ditt konto.

Se dokumentationen [RBAC för Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) för detaljer.

### Modell-distribution ej åtkomlig

Om agenten returnerar modellrelaterade fel:

1. Verifiera att modellen är distribuerad: Foundry sidofält → expandera projektet → **Modeller** → kontrollera `gpt-4.1-mini` (eller din modell) med status **Succeeded**.
2. Verifiera att distributionsnamnet stämmer: jämför `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiska distributionsnamnet i sidofältet.
3. Om distributionen gått ut (gratisnivå): distribuera om från [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Lokalt-problem (Sökväg B)

### Foundry Lokalt-tjänsten körs inte

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Symptom | Orsak | Lösning |
|---------|-------|---------|
| Health check returnerar `503` | Tjänsten har inte startat | `foundry local start` eller klicka på **Start** i Foundry Toolkit sidofält |
| Health check timeout | Modellen håller på att laddas | Vänta 30–60 s efter start; större modeller tar längre tid |
| `StatusCode: 404` på `/v1/health` | Fel port | Standard är `5273`. Kontrollera `foundry local status` för faktisk port |
| Otillräckliga resurser | Foundry Lokalt behöver ~4 GB RAM ledigt | Stäng andra program |
| Modellnedladdning misslyckas | Lågt diskutrymme | Modeller är 2–8 GB. Frigör plats, sedan `foundry model pull <name>` |

### Modellnamn stämmer inte

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Sätt `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` till exakt alias som visas (t.ex., `phi-4-mini`, inte `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` vid lokal körning (Sökväg B)

Laborationens `main.py` använder `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Lokalt kräver att denna variabel pekar på den lokala tjänsten - **inte** `AZURE_AI_PROJECT_ENDPOINT`. Säkerställ att din `.env` innehåller:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-verktyget gör fortfarande ett utgående anrop (Sökväg B)

Detta är förväntat. `search_microsoft_learn_for_plan`-verktyget hämtar lärresurser från `https://learn.microsoft.com/api/mcp`. **Endast skicknamnsfrågan** skickas över nätverket - CV och JD-text bearbetas helt på din enhet och överförs aldrig. Om full offline-funktion krävs, lägg till en `try/except` fallback i verktyget som returnerar en statisk `learn.microsoft.com` URL när endpointen inte är nåbar.

---

## Få hjälp

Om du kör fast efter att ha provat ovanstående lösningar:

1. **Kolla serverloggarna** - De flesta fel ger en Python stacktrace i terminalen. Läs hela tracebacken.
2. **Sök på felmeddelandet** - Kopiera feltexten och sök i [Microsoft Q&A för Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Öppna ett ärende** - Skapa ett ärende i [workshop-repositoriet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) med:
   - Felmeddelandet eller en skärmbild
   - Dina paketversioner (`pip list | Select-String "agent-framework"`)
   - Din Python-version (`python --version`)
   - Om problemet är lokalt eller efter distribution

---

### Checkpoint

- [ ] Du vet hur du kontrollerar och åtgärdar `.env` konfigurationsproblem
- [ ] Du kan verifiera att paketversioner matchar krävd matris
- [ ] Du vet hur du kontrollerar containerloggar för distributionsfel
- [ ] Du kan verifiera RBAC-roller i Azure Portal

---

**Föregående:** [07 - Verifiera i Playground](07-verify-in-playground.md) · **Nästa:** [09 - Sammanfattning →](09-summary.md) · **Start:** [Lab 02 README](../README.md) · [Workshop Hem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->