# Modul 8 - Feilsøking

Denne modulen dekker vanlige feil, rettelser og feilsøkingsstrategier spesifikt for multi-agent arbeidsflyten.

## Problemer med agentutdata

### GapAnalyzer sier «Jeg har fortsatt ikke samsvarsrapporten»

**Symptom:** GapAnalyzers svar ber deg lime inn en samsvarsrapport med «Manglende ferdigheter» og «Sertifiseringsmangler». Dette skjer selv når du har sendt både en CV og en stillingsbeskrivelse.

**Årsak:** JD-teksten ble ikke sendt videre til JD Agent. Med `context_mode="last_agent"`, er `resume_executor` den eneste eksekutøren som noen gang ser brukerens opprinnelige melding. Hvis `RESUME_PARSER_INSTRUCTIONS` ikke inkluderer JD-teksten i sin utdata, har ikke JD Agent noen JD å analysere, MatchingAgent kan ikke beregne en tilpassingsscore, og GapAnalyzer mottar et meningsløst input.

**Diagnose:**

I serverloggene, se etter MatchingAgent-span. Hvis den inneholder:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pass-through mangler eller er ødelagt.

**Løsning:** Bekreft at `RESUME_PARSER_INSTRUCTIONS` i `main.py` inneholder en `[JOB DESCRIPTION PASS-THROUGH]` seksjon og regelen:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bekreft også at `JOB_DESCRIPTION_INSTRUCTIONS` inneholder en `[PARSED RESUME PASS-THROUGH]` overføringsregel:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Hvis noen av instruksjonsblokkene er et stub fra stillasveiviseren, erstatt det med den komplette versjonen fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent gir “Kan ikke beregne tilpassingsscore - ingen JD levert”

Dette er samme grunnårsak som ovenfor. MatchingAgent mottok JD Agents utdata, men `[PARSED RESUME PASS-THROUGH]`-seksjonen var manglende eller tom, så den kunne ikke sammenligne de to profilene. Bekreft:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inkluderer overføringsregelen: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` instruerer agenten til å lete etter `[JD REQUIREMENTS]` og `[PARSED RESUME PASS-THROUGH]` seksjoner.

Erstatt begge instruksjonsblokker med de komplette versjonene fra [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Responsen vises to ganger

**Symptom:** GapAnalyzer-utdata (eller hele pipeline-utdata) vises to ganger i Agent Inspector-svaret.

**Årsak:** `WorkflowBuilder` bruker ELLER-semantikk for innkommende kanter - en nedstrøms eksekutør aktiveres så snart **en hvilken som helst** forløper er fullført. Hvis `matching_executor` har to innkommende kanter (en fra `resume_executor` og en fra `jd_executor`), aktiveres den to ganger: én gang når ResumeParser avsluttes og igjen når JD Agent avsluttes. GapAnalyzer kjører da også to ganger.

**Løsning:** Sørg for at `WorkflowBuilder`-grafen er en strikt sekvensiell pipeline uten samløp (fan-in):

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # IKKE fra resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Hvis du har en løs `.add_edge(resume_executor, matching_executor)` linje, fjern den. `[PARSED RESUME PASS-THROUGH]` overføringen i JD Agents utdata gir allerede MatchingAgent tilgang til CV-en.

---

## Miljø- og konfigurasjonsproblemer

### Manglende eller feil `.env`-verdier

`.env`-filen må ligge i `PersonalCareerCopilot/` katalogen (samme nivå som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Forventet `.env`-innhold:

**Sti A - Foundry sky:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Sti B - Foundry lokal:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Begge stier bruker `FOUNDRY_PROJECT_ENDPOINT`. Verdien er forskjellig: sky bruker en `https://` Foundry-endepunkt; lokal bruker `http://localhost:5273/v1`. Kjør `foundry model list` for å bekrefte eksakt modell-alias for Sti B.

> **Finne din `FOUNDRY_PROJECT_ENDPOINT`:**
- Åpne **Foundry Toolkit** sidepanelet i VS Code → høyreklikk prosjektet ditt → **Copy Project Endpoint**.
- Eller gå til [Azure Portal](https://portal.azure.com) → ditt Foundry-prosjekt → **Oversikt** → **Prosjekt-endepunkt**.

> **Finne ditt `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** I Foundry Toolkit-sidepanelet, utvid prosjektet ditt → **Models** → finn navnet på din utplasserte modell (f.eks. `gpt-4.1-mini`).

### Prioritering av miljøvariable

`main.py` bruker `load_dotenv(override=True)`, som betyr:

| Prioritet | Kilde | Vinner når begge er satt? |
|----------|--------|--------------------------|
| 1 (høyest) | `.env` fil | Ja |
| 2 | Shell / container miljøvariabel | Brukes når samme nøkkel ikke finnes i `.env` |

I lokal utvikling gjør dette `.env` til sannhetskilden (endinger i `.env` påvirker kjøringer umiddelbart). Ved hostet utrulling injiserer Foundry miljøvariable på container-nivå; siden `.env` ikke er en del av det utplasserte bildet for denne lab-oppsettet, brukes de injiserte containerverdiene.

---

## Versjonskompatibilitet

### Pakkeversjonsmatrise

Multi-agent arbeidsflyten krever spesifikke pakkeversjoner. Uoverensstemmelser i versjoner forårsaker kjøretidsfeil.

| Pakke | Påkrevd versjon | Sjekk-kommando |
|-------|-----------------|-----------------|
| `agent-framework-foundry` | nyeste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | nyeste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | nyeste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Vanlige versjonsfeil

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fiks: installer agent-framework-foundry på nytt
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fiks: oppgrader mcp-pakken
pip install mcp --upgrade
```

### Bekreft alle versjoner samtidig

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

## Utrullingsproblemer

### Container starter ikke etter utrulling

1. **Sjekk containerlogger:**
   - Åpne **Foundry Toolkit** sidepanelet → utvid **Hosted Agents (Preview)** → klikk på agenten din → utvid versjonen → **Container Details** → **Logs**.
   - Se etter Python stack traces eller manglende modul-feil.

2. **Vanlige container startup-feil:**

   | Feil i logger | Årsak | Løsning |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` mangler en pakke | Legg til pakken, deploy på nytt |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` eller `.env` miljøvariabler ikke satt | Oppdater `agent.yaml` → `environment_variables` seksjon (hostet) eller `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ikke konfigurert | Foundry setter dette automatisk - sørg for at du deployerer via utvidelsen |
   | `OSError: port 8088 already in use` | Dockerfile eksponerer feil port eller portkonflikt | Verifiser `EXPOSE 8088` i Dockerfile og `CMD ["python", "main.py"]` |
   | Container avsluttes med kode 1 | Uhåndtert unntak i `main()` | Test lokalt først ([Modul 5](05-test-locally.md)) for å fange feil før deploy |

3. **Deploy på nytt etter fiksing:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → velg samme agent → deploy en ny versjon.

### Utrulling tar for lang tid

Multi-agent containere tar lengre tid å starte fordi de lager 4 agentinstanser ved oppstart. Normale oppstartstider:

| Fase | Forventet varighet |
|------|------------------|
| Bygging av containerbilde | 1-3 minutter |
| Push av bilde til ACR | 30-60 sekunder |
| Containerstart (enkel agent) | 15-30 sekunder |
| Containerstart (multi-agent) | 30-120 sekunder |
| Agent tilgjengelig i Playground | 1-2 minutter etter «Started» |

> Hvis statusen "Pending" vedvarer utover 5 minutter, sjekk container-logger for feil.

---

## RBAC og tillatelsesproblemer

### `403 Forbidden` eller `AuthorizationFailed`

Du trenger rollen **[Foundry User](https://aka.ms/foundry-ext-project-role)** på ditt Foundry-prosjekt (tidligere kalt **Azure AI User** - rolle-ID uendret):

1. Gå til [Azure Portal](https://portal.azure.com) → ditt Foundry **prosjekt**-ressurs.
2. Klikk **Access control (IAM)** → **Role assignments**.
3. Søk etter navnet ditt → bekreft at **Foundry User** (eller det gamle navnet **Azure AI User**) er oppført.
4. Hvis mangler: **Legg til** → **Add role assignment** → søk etter **Foundry User** → tilordne til kontoen din.

Se [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokumentasjonen for detaljer.

### Modellutrulling ikke tilgjengelig

Hvis agenten returnerer modellrelaterte feil:

1. Bekreft at modellen er utplassert: Foundry sidepanel → utvid prosjekt → **Models** → sjekk etter `gpt-4.1-mini` (eller din modell) med status **Succeeded**.
2. Bekreft at utrullingsnavnet stemmer: sammenlign `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiske utrullingsnavnet i sidepanelet.
3. Hvis utrullingen er utløpt (gratisnivå): deploy på nytt fra [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problemer (Sti B)

### Foundry Local-tjenesten kjører ikke

```powershell
# Sjekk status
foundry local status

# Start tjenesten hvis den er stoppet
foundry local start
```

| Symptom | Årsak | Løsning |
|---------|-------|---------|
| Helse-sjekk returnerer `503` | Tjenesten ikke startet | `foundry local start` eller klikk **Start** i Foundry Toolkit-sidepanelet |
| Helse-sjekk timeouter | Modell lastes fortsatt | Vent 30–60 s etter oppstart; større modeller tar lengre tid |
| `StatusCode: 404` på `/v1/health` | Feil port | Standard er `5273`. Sjekk `foundry local status` for faktisk port |
| Utilstrekkelige ressurser | Foundry Local trenger ~4 GB RAM ledig | Lukk andre applikasjoner |
| Nedlasting av modell feiler | Lav diskplass | Modeller er 2–8 GB. Frigjør plass, så `foundry model pull <name>` |

### Modellnavn stemmer ikke

```powershell
# Liste over nedlastede modeller og deres eksakte aliaser
foundry model list
```

Sett `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `.env` til eksakt alias som vist (f.eks. `phi-4-mini`, ikke `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ved lokal kjøring (Sti B)

Labens `main.py` bruker `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local krever at denne variabelen peker til den lokale tjenesten - **ikke** `AZURE_AI_PROJECT_ENDPOINT`. Sørg for at `.env` inneholder:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-verktøyet gjør fortsatt en utgående kall (Sti B)

Dette er forventet. Verktøyet `search_microsoft_learn_for_plan` henter læringsressurser fra `https://learn.microsoft.com/api/mcp`. **Bare ferdighetsnavn-spørringen** går over nettverket - CV og JD-tekst behandles helt på din enhet og sendes aldri bort. Hvis fullstendig offline drift kreves, legg til en `try/except` fallback i verktøyet som returnerer en statisk `learn.microsoft.com` URL når endepunktet ikke er tilgjengelig.

---

## Få hjelp

Hvis du sitter fast etter å ha prøvd rettelsene ovenfor:

1. **Sjekk serverloggene** - De fleste feil gir en Python stack trace i terminalen. Les hele tracebacken.
2. **Søk etter feilmeldingen** - Kopier feilmeldingen og søk i [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Åpne en sak** - Opprett en issue i [workshop-repositoriet](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) med:
   - Feilmeldingen eller skjermbilde
   - Dine pakkversjoner (`pip list | Select-String "agent-framework"`)
   - Din Python-versjon (`python --version`)
   - Om problemet er lokalt eller etter utrulling

---

### Sjekkpunkter

- [ ] Du vet hvordan du sjekker og fjerner `.env` konfigurasjonsproblemer
- [ ] Du kan verifisere at pakkeversjoner samsvarer med den påkrevde matrisen
- [ ] Du vet hvordan du sjekker containerlogger for utrullingsfeil
- [ ] Du kan verifisere RBAC-roller i Azure-portalen

---

**Forrige:** [07 - Verifiser i Playground](07-verify-in-playground.md) · **Neste:** [09 - Sammendrag →](09-summary.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->