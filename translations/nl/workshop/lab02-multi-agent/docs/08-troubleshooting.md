# Module 8 - Problemen oplossen

Deze module behandelt veelvoorkomende fouten, oplossingen en debugstrategieën specifiek voor de multi-agent workflow.

## Problemen met agentuitvoer

### GapAnalyzer zegt “Ik heb nog steeds het bijbehorende rapport niet”

**Symptoom:** GapAnalyzer’s antwoord vraagt je een bijbehorend rapport te plakken met “Ontbrekende vaardigheden” en “Certificeringslacunes.” Dit gebeurt zelfs als je zowel een cv als een functiebeschrijving hebt gestuurd.

**Oorzaak:** De JD-tekst werd niet doorgegeven aan de JD Agent. Met `context_mode="last_agent"` is `resume_executor` de enige executor die de originele gebruikersboodschap ziet. Als `RESUME_PARSER_INSTRUCTIONS` de JD-tekst niet in zijn uitvoer opneemt, heeft JD Agent geen JD om te ontleden, kan MatchingAgent geen geschiktheidsscore berekenen, en ontvangt GapAnalyzer een betekenisloze invoer.

**Diagnose:**

Zoek in de serverlogs naar de MatchingAgent-span. Als deze bevat:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
dan ontbreekt of is de doorgifte gebroken.

**Oplossing:** Bevestig dat `RESUME_PARSER_INSTRUCTIONS` in `main.py` een `[JOB DESCRIPTION PASS-THROUGH]` sectie bevat en de regel:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bevestig ook dat `JOB_DESCRIPTION_INSTRUCTIONS` een `[PARSED RESUME PASS-THROUGH]` doorgeefregel bevat:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Als een van beide instructieblokken een placeholder is van de scaffold wizard, vervang deze dan door de volledige versie uit [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent geeft “Kan geschiktheidsscore niet berekenen - geen JD meegeleverd” weer

Dit is dezelfde onderliggende oorzaak als hierboven. MatchingAgent ontving de uitvoer van JD Agent, maar de `[PARSED RESUME PASS-THROUGH]` sectie ontbrak of was leeg, dus kon hij de twee profielen niet vergelijken. Bevestig:
1. `JOB_DESCRIPTION_INSTRUCTIONS` bevat de doorgeefregel: `Kopieer [PARSED RESUME] letter voor letter - Matching Agent is hiervan downstream afhankelijk.`
2. `MATCHING_AGENT_INSTRUCTIONS` zegt tegen de agent te zoeken naar de secties `[JD REQUIREMENTS]` en `[PARSED RESUME PASS-THROUGH]`.

Vervang beide instructieblokken door de complete versies uit [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### De reactie verschijnt twee keer

**Symptoom:** GapAnalyzer-uitvoer (of de volledige pijplijnuitvoer) verschijnt twee keer in de Agent Inspector-respons.

**Oorzaak:** `WorkflowBuilder` gebruikt OF-semantiek voor binnenkomende koppelingen - een downstream executor start zodra **één** voorganger klaar is. Als `matching_executor` twee inkomende koppelingen heeft (een van `resume_executor` en een van `jd_executor`), start hij twee keer: een keer als ResumeParser klaar is en nog een keer als JD Agent klaar is. GapAnalyzer draait dan ook twee keer.

**Oplossing:** Zorg ervoor dat de `WorkflowBuilder` grafiek een strikt sequentiële pijplijn is zonder samenkomende ingangen (fan-in):

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NIET van resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Als je een ongewenste `.add_edge(resume_executor, matching_executor)` regel hebt, verwijder deze dan. De `[PARSED RESUME PASS-THROUGH]` doorgeefregel in JD Agent’s uitvoer geeft MatchingAgent al toegang tot het cv.

---

## Omgevings- en configuratieproblemen

### Ontbrekende of onjuiste `.env` waarden

Het `.env` bestand moet in de `PersonalCareerCopilot/` directory staan (op hetzelfde niveau als `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Verwachte `.env` inhoud:

**Pad A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Pad B - Foundry lokaal:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Beide paden gebruiken `FOUNDRY_PROJECT_ENDPOINT`. De waarde verschilt: cloud gebruikt een `https://` Foundry eindpunt; lokaal gebruikt `http://localhost:5273/v1`. Voer `foundry model list` uit om de exacte modelalias voor Pad B te bevestigen.

> **Je `FOUNDRY_PROJECT_ENDPOINT` vinden:** 
- Open de **Foundry Toolkit** zijbalk in VS Code → klik met de rechtermuisknop op je project → **Copy Project Endpoint**. 
- Of ga naar [Azure Portal](https://portal.azure.com) → jouw Foundry project → **Overzicht** → **Project endpoint**.

> **Je `AZURE_AI_MODEL_DEPLOYMENT_NAME` vinden:** In de Foundry Toolkit zijbalk, vouw je project uit → **Modellen** → zoek je naam van het gedeployde model (bv. `gpt-4.1-mini`).

### Prioriteit van omgevingsvariabelen

`main.py` gebruikt `load_dotenv(override=True)`, wat betekent:

| Prioriteit | Bron | Heeft voorrang als beide zijn ingesteld? |
|-----------|-------|--------------------------------------|
| 1 (hoogste) | `.env` bestand | Ja |
| 2 | Shell / container omgevingsvariabele | Wordt gebruikt als dezelfde sleutel niet in `.env` aanwezig is |

In lokale ontwikkeling maakt dit `.env` de waarheidbron (wijzigingen in `.env` beïnvloeden direct het programma). In gehoste deployment injecteert Foundry omgevingsvariabelen op container niveau; omdat `.env` geen deel uitmaakt van het gedeployde image in deze labopstelling, worden de geïnjecteerde containerwaarden gebruikt.

---

## Versiecompatibiliteit

### Matrix van pakketversies

De multi-agent workflow vereist specifieke pakketversies. Niet-overeenkomende versies veroorzaken runtime fouten.

| Pakket | Vereiste versie | Controlecommando |
|--------|-----------------|-----------------|
| `agent-framework-foundry` | laatste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | laatste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | laatste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Veelvoorkomende versie fouten

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Oplossing: herinstalleer agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Opgelost: mcp-pakket bijwerken
pip install mcp --upgrade
```

### Controleer alle versies tegelijk

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Verwachte uitvoer:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Deploymentsproblemen

### Container start niet na deployment

1. **Controleer container logs:**
   - Open de **Foundry Toolkit** zijbalk → vouw **Hosted Agents (Preview)** uit → klik op jouw agent → vouw versie uit → **Container Details** → **Logs**.
   - Zoek naar Python stacktraces of ontbrekende module fouten.

2. **Veelvoorkomende container start fouten:**

   | Fout in logs | Oorzaak | Oplossing |
   |-------------|---------|----------|
   | `ModuleNotFoundError` | `requirements.txt` mist een pakket | Voeg het pakket toe, herdeploy |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` of `.env` env vars niet ingesteld | Werk `agent.yaml` → `environment_variables` sectie (gehost) of `.env` (lokaal) bij |
   | `azure.identity.CredentialUnavailableError` | Managed Identity niet geconfigureerd | Foundry stelt dit automatisch in - zorg dat je via de extensie deployt |
   | `OSError: port 8088 already in use` | Dockerfile exposeert verkeerde poort of poortconflict | Controleer `EXPOSE 8088` in Dockerfile en `CMD ["python", "main.py"]` |
   | Container stopt met code 1 | Ongeregelde uitzondering in `main()` | Test lokaal eerst ([Module 5](05-test-locally.md)) om fouten te vangen voor deployment |

3. **Herdeploy na reparatie:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → selecteer dezelfde agent → deploy een nieuwe versie.

### Deployment duurt te lang

Multi-agent containers starten langzamer omdat ze bij het opstarten 4 agent instanties aanmaken. Normale opstarttijden:

| Fase | Verwachte duur |
|-------|----------------|
| Container image build | 1-3 minuten |
| Image push naar ACR | 30-60 seconden |
| Container start (enkele agent) | 15-30 seconden |
| Container start (multi-agent) | 30-120 seconden |
| Agent beschikbaar in Playground | 1-2 minuten na "Started" |

> Als de status “Pending” langer dan 5 minuten aanhoudt, controleer dan container logs op fouten.

---

## RBAC- en machtigingsproblemen

### `403 Forbidden` of `AuthorizationFailed`

Je hebt de **[Foundry User](https://aka.ms/foundry-ext-project-role)** rol nodig op je Foundry project (voorheen genaamd **Azure AI User** - rol-ID ongewijzigd):

1. Ga naar [Azure Portal](https://portal.azure.com) → je Foundry **project** resource.
2. Klik **Toegangsbeheer (IAM)** → **Roltoewijzingen**.
3. Zoek je naam → bevestig dat **Foundry User** (of het legacy label **Azure AI User**) vermeld staat.
4. Indien ontbrekend: **Toevoegen** → **Roltoewijzing toevoegen** → zoek **Foundry User** → wijs toe aan je account.

Zie de [RBAC voor Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) documentatie voor details.

### Model deployment niet toegankelijk

Als de agent model-gerelateerde fouten geeft:

1. Controleer dat het model gedeployed is: Foundry zijbalk → vouw project uit → **Modellen** → controleer op `gpt-4.1-mini` (of jouw model) met status **Succeeded**.
2. Controleer dat de deploymentnaam overeenkomt: vergelijk `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` (of `agent.yaml`) met de werkelijke deploymentnaam in de zijbalk.
3. Als de deployment verlopen is (gratis tier): herdeploy vanuit [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problemen (Pad B)

### Foundry Local service draait niet

```powershell
# Controleer status
foundry local status

# Start de service als deze is gestopt
foundry local start
```

| Symptoom | Oorzaak | Oplossing |
|----------|---------|----------|
| Health check geeft `503` | Service niet gestart | `foundry local start` of klik **Start** in Foundry Toolkit zijbalk |
| Health check time-out | Model wordt nog geladen | Wacht 30–60 s na starten; grotere modellen duren langer |
| `StatusCode: 404` op `/v1/health` | Verkeerde poort | Standaard is `5273`. Controleer `foundry local status` voor de werkelijke poort |
| Onvoldoende resources | Foundry Local heeft ~4 GB RAM vrij nodig | Sluit andere programma's |
| Model download mislukt | Weinig schijfruimte | Modellen zijn 2–8 GB. Maak ruimte vrij en voer dan `foundry model pull <naam>` uit |

### Modelnaam komt niet overeen

```powershell
# Lijst met gedownloade modellen en hun exacte aliassen
foundry model list
```

Stel `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` in op de exacte alias zoals getoond (bv. `phi-4-mini`, niet `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` bij lokale run (Pad B)

De `main.py` van het lab gebruikt `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local vereist dat deze variabele verwijst naar de lokale service - **niet** `AZURE_AI_PROJECT_ENDPOINT`. Zorg dat je `.env` het volgende bevat:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-tool maakt nog steeds een uitgaande call (Pad B)

Dit is verwacht. De tool `search_microsoft_learn_for_plan` haalt leermaterialen op van `https://learn.microsoft.com/api/mcp`. **Alleen de vaardigheidsnaam zoekopdracht** gaat via het netwerk - cv en JD-tekst worden volledig op jouw device verwerkt en nooit verzonden. Als volledig offline gebruik vereist is, voeg dan een `try/except` fallback toe in de tool die een statische `learn.microsoft.com` URL retourneert als het endpunt niet bereikbaar is.

---

## Hulp krijgen

Als je vastloopt nadat je bovenstaande oplossingen hebt geprobeerd:

1. **Controleer de serverlogs** - De meeste fouten geven een Python stacktrace in de terminal. Lees de volledige traceback.
2. **Zoek de foutmelding op** - Kopieer de fouttekst en zoek in de [Microsoft Q&A voor Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Open een issue** - Dien een issue in op de [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) met:
   - De foutmelding of screenshot
   - Jouw pakketversies (`pip list | Select-String "agent-framework"`)
   - Jouw Python versie (`python --version`)
   - Of het probleem lokaal is of na deployment

---

### Checkpoint

- [ ] Je weet hoe je `.env` configuratieproblemen controleert en repareert
- [ ] Je kunt pakketversies verifiëren aan de hand van de vereiste matrix
- [ ] Je weet hoe je containerlogs controleert bij deploymentfouten
- [ ] Je kunt RBAC-rollen controleren in de Azure Portal

---

**Vorige:** [07 - Verifiëren in Playground](07-verify-in-playground.md) · **Volgende:** [09 - Samenvatting →](09-summary.md) · **Start:** [Lab 02 README](../README.md) · [Workshop Startpagina](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->