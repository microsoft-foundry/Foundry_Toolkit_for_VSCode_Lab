# Modul 8 - Feilsøking

Denne modulen dekker vanlige feil, løsninger og feilsøkingsstrategier spesifikke for multi-agent arbeidsflyten.

## Problemer med agentens utdata

### GapAnalyzer sier «Jeg har fortsatt ikke mottatt den samsvarende rapporten»

**Symptom:** GapAnalyzers svar ber deg lime inn en samsvarende rapport med «Mangler ferdigheter» og «Sertifiseringsgap». Dette skjer selv når du sendte både en CV og en stillingsbeskrivelse.

**Årsak:** JD-teksten ble ikke sendt videre til JD Agent. Med `context_mode="last_agent"` er `resume_executor` den eneste utføreren som noensinne ser brukerens opprinnelige melding. Hvis `RESUME_PARSER_INSTRUCTIONS` ikke inkluderer JD-teksten i utdataene sine, har ikke JD Agent noen JD å analysere, MatchingAgent kan ikke beregne en poengsum for samsvar, og GapAnalyzer mottar input som ikke gir mening.

**Diagnose:**

I serverloggene, se etter MatchingAgent-spennet. Hvis det inneholder:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pass-through mangler eller er ødelagt.

**Løsning:** Bekreft at `RESUME_PARSER_INSTRUCTIONS` i `main.py` inneholder en `[JOB DESCRIPTION PASS-THROUGH]`-seksjon og regelen:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bekreft også at `JOB_DESCRIPTION_INSTRUCTIONS` inneholder en `[PARSED RESUME PASS-THROUGH]` relay-regel:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Hvis noen av instruksjonsblokkene er en stub fra scaffold-veiviseren, erstatt den med komplett versjon fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent gir ut «Kan ikke beregne samsvarspoeng - ingen JD gitt»

Dette har samme grunnårsak som ovenfor. MatchingAgent mottok utdata fra JD Agent, men `[PARSED RESUME PASS-THROUGH]`-seksjonen manglet eller var tom, så den kunne ikke sammenligne de to profilene. Bekreft:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inkluderer relay-regelen: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` forteller agenten om å lete etter `[JD REQUIREMENTS]` og `[PARSED RESUME PASS-THROUGH]` seksjoner.

Erstatt begge instruksjonsblokker med komplette versjoner fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Svaret dukker opp to ganger

**Symptom:** GapAnalyzer-utdata (eller hele pipeline-utdata) vises to ganger i Agent Inspector-svaret.

**Årsak:** `WorkflowBuilder` bruker ELLER-semantikk for innkommende kanter – en nedstrøms utfører trigges så snart **hvilken som helst** forgjenger fullfører. Hvis `matching_executor` har to innkommende kanter (en fra `resume_executor` og en fra `jd_executor`), trigges den to ganger: én gang når ResumeParser fullfører og en gang til når JD Agent fullfører. GapAnalyzer kjører da også to ganger.

**Løsning:** Sørg for at `WorkflowBuilder`-grafen er en strengt sekvensiell pipeline uten fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Hvis du har en feilplassert `.add_edge(resume_executor, matching_executor)`-linje, fjern den. `[PARSED RESUME PASS-THROUGH]`-relayet i JD Agents utdata gir allerede MatchingAgent tilgang til CV-en.

---

## Miljø- og konfigurasjonsproblemer

### Manglende eller feil `.env`-verdier

Filen `.env` må ligge i katalogen `PersonalCareerCopilot/` (samme nivå som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Forventet innhold i `.env`:

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

> Begge stier bruker `FOUNDRY_PROJECT_ENDPOINT`. Verdiene er forskjellige: cloud bruker en `https://` Foundry-endepunkt; lokal bruker `http://localhost:5273/v1`. Kjør `foundry model list` for å bekrefte eksakt modellalias for sti B.

> **Slik finner du din `FOUNDRY_PROJECT_ENDPOINT`:** 
- Åpne **Foundry Toolkit**-sidefeltet i VS Code → høyreklikk prosjektet ditt → **Kopier prosjektendepunkt**. 
- Eller gå til [Azure Portal](https://portal.azure.com) → ditt Foundry-prosjekt → **Oversikt** → **Prosjektendepunkt**.

> **Slik finner du din `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** I Foundry Toolkit-sidefeltet, utvid prosjektet ditt → **Modeller** → finn navnet på den distribuerte modellen (f.eks. `gpt-4.1-mini`).

### Prioritering av miljøvariabler

`main.py` bruker `load_dotenv(override=True)`, som betyr:

| Prioritet | Kilde | Vinner når begge er satt? |
|----------|--------|-------------------------|
| 1 (høyest) | `.env`-fil | Ja |
| 2 | Shell / container miljøvariabel | Brukes når samme nøkkel ikke finnes i `.env` |

Ved lokal utvikling gjør dette `.env` til sannhetskilden (endring i `.env` påvirker kjøringer umiddelbart). Ved hosted distribusjon injiserer Foundry miljøvariabler på container-nivå; siden `.env` ikke er del av det distribuerte bildet for dette lab-oppsettet, brukes de injiserte container-verdiene.

---

## Versjonskompatibilitet

### Pakkeversjonsmatrise

Multi-agent arbeidsflyten krever spesifikke pakkeversjoner. Feil versjoner forårsaker kjøretidsfeil.

| Pakke | Krevet versjon | Sjekk-kommando |
|---------|-----------------|---------------|
| `agent-framework-foundry` | nyeste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | nyeste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | nyeste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Vanlige versjonsfeil

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

### Verifiser alle versjoner på en gang

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Forventet utdata:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Distribusjonsproblemer

### Container starter ikke etter distribusjon

1. **Sjekk container-logger:** 
   - Åpne **Foundry Toolkit**-sidefeltet → under prosjektet ditt, klikk **Agents** → **Hosted Agent**-fanen → klikk agenten din. Sjekk **Status** under **Detaljer**-fanen, åpne deretter **Playground**-fanen og bruk **Logs**-fanen i **Session Details**-panelet for å se containerens output.
   - Se etter Python stack traces eller manglende modul-feil.

2. **Vanlige container-startfeil:**

   | Feil i logger | Årsak | Løsning |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` mangler en pakke | Legg til pakken, deploy på nytt |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` eller `.env` miljøvariabler ikke satt | Oppdater `agent.yaml` → `environment_variables` seksjon (hosted) eller `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Administrert identitet ikke konfigurert | Foundry setter dette automatisk – sørg for at du deployer via utvidelsen |
   | `OSError: port 8088 already in use` | Dockerfile eksponerer feil port eller portkonflikt | Verifiser `EXPOSE 8088` i Dockerfile og `CMD ["python", "main.py"]` |
   | Container avsluttes med kode 1 | Ubehandlet unntak i `main()` | Test lokalt først ([Modul 5](05-test-locally.md)) for å fange feil før distribusjon |

3. **Distribuer på nytt etter fiksering:** 
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → velg samme agent → deploy ny versjon.

### Distribusjonen tar for lang tid

Multi-agent containere tar lengre tid å starte fordi de oppretter 4 agent-instansene ved oppstart. Vanlige oppstartstider:

| Fase | Forventet varighet |
|-------|-------------------|
| Bygging av containerbilde | 1-3 minutter |
| Push av bilde til ACR | 30-60 sekunder |
| Start av container (enkel agent) | 15-30 sekunder |
| Start av container (multi-agent) | 30-120 sekunder |
| Agent tilgjengelig i Playground | 1-2 minutter etter «Started» |

> Hvis status «Pending» vedvarer mer enn 5 minutter, sjekk container-logger for feil.

---

## RBAC- og rettighetsproblemer

### `403 Forbidden` eller `AuthorizationFailed`

Du trenger rollen **[Foundry User](https://aka.ms/foundry-ext-project-role)** på Foundry-prosjektet ditt (tidligere kalt **Azure AI User** – rolle-ID er uendret):

1. Gå til [Azure Portal](https://portal.azure.com) → Finn Foundry **prosjekt**-ressursen din.
2. Klikk **Access control (IAM)** → **Role assignments**.
3. Søk på navnet ditt → bekreft at **Foundry User** (eller den gamle etiketten **Azure AI User**) er oppført.
4. Hvis mangler: **Legg til** → **Add role assignment** → søk etter **Foundry User** → tilordne til kontoen din.

Se [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokumentasjonen for detaljer.

### Modell-distribusjon er ikke tilgjengelig

Hvis agenten returnerer modellrelaterte feil:

1. Verifiser at modellen er distribuert: Foundry sidebar → utvid prosjekt → **Modeller** → sjekk etter `gpt-4.1-mini` (eller modellen din) med status **Succeeded**.
2. Kontroller at distribusjonsnavnet samsvarer: sammenlign `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiske distribusjonsnavnet i sidebar.
3. Hvis distribusjonen har utløpt (gratisnivå): distribuer på nytt fra [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problemer (Sti B)

### Foundry Local-tjenesten kjører ikke

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Symptom | Årsak | Løsning |
|---------|-------|---------|
| Helsekontroll returnerer `503` | Tjenesten er ikke startet | `foundry local start` eller klikk **Start** i Foundry Toolkit-sidefeltet |
| Helsekontroll går ut på tid | Modell lastes fortsatt | Vent 30–60 sekunder etter oppstart; større modeller tar lengre tid |
| `StatusCode: 404` på `/v1/health` | Feil port | Standard er `5273`. Sjekk `foundry local status` for faktisk port |
| Utilstrekkelige ressurser | Foundry Local trenger ~4 GB RAM ledig | Lukk andre applikasjoner |
| Modellnedlasting mislykkes | Lite diskplass | Modeller er 2–8 GB. Frigjør plass, så `foundry model pull <name>` |

### Modellnavn stemmer ikke

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Sett `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` til eksakt alias som vist (f.eks. `phi-4-mini`, ikke `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ved lokal kjøring (Sti B)

Labens `main.py` bruker `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local krever at denne variabelen peker til lokal tjeneste – **ikke** `AZURE_AI_PROJECT_ENDPOINT`. Sørg for at `.env` inneholder:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-verktøyet gjør fortsatt utgående kall (Sti B)

Dette er forventet. `search_microsoft_learn_for_plan`-verktøyet henter læringsressurser fra `https://learn.microsoft.com/api/mcp`. **Kun ferdighetsnavn-forespørselen** går over nettverket – CV og JD-tekst bearbeides fullstendig på enheten din og sendes aldri. Hvis full offline-operasjon kreves, legg til en `try/except` fallback i verktøyet som returnerer en statisk `learn.microsoft.com`-URL når endepunktet ikke er tilgjengelig.

---

## Få hjelp

Hvis du sitter fast etter å ha prøvd løsningene over:

1. **Sjekk serverloggene** – De fleste feil gir en Python stack trace i terminalen. Les hele tracebacken.
2. **Søk på feilmeldingen** – Kopier feiltekst og søk i [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Åpne en sak** – Opprett en sak i [workshop-repositoriet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) med:
   - Feilmeldingen eller skjermbilde
   - Dine pakkeversjoner (`pip list | Select-String "agent-framework"`)
   - Din Python-versjon (`python --version`)
   - Om problemet oppstår lokalt eller etter distribusjon

---

### Sjekkpunkter

- [ ] Du vet hvordan du sjekker og fikser `.env` konfigurasjonsproblemer
- [ ] Du kan verifisere at pakkeversjonene samsvarer med kravmatrisen
- [ ] Du vet hvordan du sjekker container-logger for distribusjonsfeil
- [ ] Du kan verifisere RBAC-roller i Azure Portal

---

**Forrige:** [07 - Verifiser i Playground](07-verify-in-playground.md) · **Neste:** [09 - Sammendrag →](09-summary.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->