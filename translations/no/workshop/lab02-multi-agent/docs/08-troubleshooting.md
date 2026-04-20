# Modul 8 - Feilsøking (Multi-Agent)

Denne modulen dekker vanlige feil, løsninger og feilsøkingsstrategier spesifikt for multi-agent arbeidsflyten. For generelle Foundry distribusjonsproblemer, se også [Lab 01 feilsøkingsguide](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Kjapp referanse: Feil → Løsning

| Feil / Symptom | Sannsynlig Årsak | Løsning |
|----------------|-----------------|---------|
| `RuntimeError: Missing required environment variable(s)` | `.env` fil mangler eller verdier ikke satt | Lag `.env` med `PROJECT_ENDPOINT=<din-endpoint>` og `MODEL_DEPLOYMENT_NAME=<din-modell>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuelt miljø ikke aktivert eller avhengigheter ikke installert | Kjør `.\.venv\Scripts\Activate.ps1` deretter `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP-pakke ikke installert (manglende i requirements) | Kjør `pip install mcp` eller sjekk at `requirements.txt` inkluderer det som transitiv avhengighet |
| Agent starter men returnerer tomt svar | `output_executors` stemmer ikke overens eller kanter mangler | Verifiser `output_executors=[gap_analyzer]` og at alle kanter finnes i `create_workflow()` |
| Bare 1 gap-kort (resten mangler) | GapAnalyzer instruksjoner ufullstendige | Legg til `CRITICAL:` paragrafen i `GAP_ANALYZER_INSTRUCTIONS` - se [Modul 3](03-configure-agents.md) |
| Fit score er 0 eller mangler | MatchingAgent mottok ikke data oppstrøms | Verifiser at både `add_edge(resume_parser, matching_agent)` og `add_edge(jd_agent, matching_agent)` er definert |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP-server avviste verktøysanropet | Sjekk internettforbindelsen. Prøv å åpne `https://learn.microsoft.com/api/mcp` i nettleser. Prøv igjen |
| Ingen Microsoft Learn URL-er i output | MCP-verktøy ikke registrert eller feil endpoint | Verifiser `tools=[search_microsoft_learn_for_plan]` på GapAnalyzer og at `MICROSOFT_LEARN_MCP_ENDPOINT` er korrekt |
| `Address already in use: port 8088` | Annen prosess bruker port 8088 | Kjør `netstat -ano | findstr :8088` (Windows) eller `lsof -i :8088` (macOS/Linux) og stopp prosessen som konflikerer |
| `Address already in use: port 5679` | Konflikt på Debugpy port | Stopp andre feilsøkingssesjoner. Kjør `netstat -ano | findstr :5679` for å finne og avslutte prosessen |
| Agent Inspector åpnes ikke | Server ikke fullt startet eller portkonflikt | Vent på "Server running" i logg. Sjekk at port 5679 er ledig |
| `azure.identity.CredentialUnavailableError` | Ikke pålogget Azure CLI | Kjør `az login` og restart serveren |
| `azure.core.exceptions.ResourceNotFoundError` | Modell distribusjon eksisterer ikke | Sjekk at `MODEL_DEPLOYMENT_NAME` stemmer med en distribuert modell i Foundry-prosjektet ditt |
| Container status "Failed" etter distribusjon | Container krasjer ved oppstart | Sjekk container-logger i Foundry sidebar. Vanlig: manglende miljøvariabel eller importfeil |
| Distribusjon viser "Pending" > 5 minutter | Container tar for lang tid å starte eller ressursbegrensninger | Vent opptil 5 minutter for multi-agent (lager 4 agent-instansser). Hvis fortsatt ventende, sjekk logger |
| `ValueError` fra `WorkflowBuilder` | Ugyldig grafkonfigurasjon | Sørg for at `start_executor` er satt, `output_executors` er en liste, og ingen sirkulære kanter |

---

## Miljø- og konfigurasjonsproblemer

### Manglende eller feil `.env` verdier

`.env` filen må ligge i `PersonalCareerCopilot/` mappen (på samme nivå som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Forventet `.env` innhold:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Finne din PROJECT_ENDPOINT:**  
- Åpne **Microsoft Foundry** sidepanel i VS Code → høyreklikk på prosjektet ditt → **Copy Project Endpoint**.  
- Eller gå til [Azure Portal](https://portal.azure.com) → ditt Foundry-prosjekt → **Oversikt** → **Project endpoint**.

> **Finne din MODEL_DEPLOYMENT_NAME:** I Foundry sidepanelet, utvid prosjektet → **Models** → finn navnet på den distribuerte modellen (f.eks. `gpt-4.1-mini`).

### Prioritering av miljøvariabler

`main.py` bruker `load_dotenv(override=False)`, som betyr:

| Prioritet | Kilde | Vinner hvis begge er satt? |
|-----------|-------|----------------------------|
| 1 (høyest) | Shell miljøvariabel | Ja |
| 2 | `.env` fil | Kun hvis shell-variabel ikke er satt |

Dette betyr at Foundry runtime miljøvariabler (satt via `agent.yaml`) har prioritet over `.env` verdier under hostet distribusjon.

---

## Versjonskompatibilitet

### Pakkeversjonsmatrise

Multi-agent arbeidsflyten krever spesifikke pakkeversjoner. Versjonsmismatch fører til kjøretidsfeil.

| Pakke | Påkrevd Versjon | Sjekk-kommando |
|-------|-----------------|----------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | siste forhåndsutgivelse | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Vanlige versjonsfeil

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fiks: oppgradering til rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` ikke funnet eller Inspector inkompatibel:**

```powershell
# Fiks: installer med --pre-flagget
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fiks: oppgrader mcp-pakken
pip install mcp --upgrade
```

### Verifiser alle versjoner samtidig

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

## MCP verktøyproblemer

### MCP verktøy returnerer ingen resultater

**Symptom:** Gap-kort viser "No results returned from Microsoft Learn MCP" eller "No direct Microsoft Learn results found".

**Mulige årsaker:**

1. **Nettverksproblem** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) er utilgjengelig.
   ```powershell
   # Test tilkobling
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Hvis dette returnerer `200`, er endepunktet tilgjengelig.

2. **For spesifikk spørring** - Ferdighetsnavnet er for nisje for Microsoft Learn søk.
   - Dette er forventet for svært spesialiserte ferdigheter. Verktøyet har fallback URL i responsen.

3. **MCP sesjonstid utløpt** - Streamable HTTP-tilkoblingen tidsavbrutt.
   - Prøv forespørselen på nytt. MCP sesjoner er flyktige og kan trenge ny tilkobling.

### MCP logger forklart

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Logg | Betydning | Handling |
|------|-----------|----------|
| `GET → 405` | MCP klientprober under initiering | Normal - ignorer |
| `POST → 200` | Verktøysanrop lykkes | Forventet |
| `DELETE → 405` | MCP klientprober under opprydding | Normal - ignorer |
| `POST → 400` | Feilaktig forespørsel (ugyldig spørring) | Sjekk `query`-parameter i `search_microsoft_learn_for_plan()` |
| `POST → 429` | Begrenset i bruk | Vent og prøv på nytt. Reduser `max_results`-parameter |
| `POST → 500` | MCP serverfeil | Midlertidig - prøv igjen. Hvis vedvarende, kan Microsoft Learn MCP API være nede |
| Tidsavbrudd for tilkobling | Nettverksproblem eller MCP server utilgjengelig | Sjekk internett. Prøv `curl https://learn.microsoft.com/api/mcp` |

---

## Distribusjonsproblemer

### Container feiler å starte etter distribusjon

1. **Sjekk container-logger:**
   - Åpne **Microsoft Foundry** sidepanel → utvid **Hosted Agents (Preview)** → klikk på agenten din → utvid versjonen → **Container Details** → **Logs**.
   - Se etter Python stack traces eller manglende modulfeil.

2. **Vanlige feil ved container-start:**

   | Feil i logg | Årsak | Løsning |
   |-------------|--------|---------|
   | `ModuleNotFoundError` | `requirements.txt` mangler pakke | Legg til pakken, distribuer på nytt |
   | `RuntimeError: Missing required environment variable` | Miljøvariabler i `agent.yaml` ikke satt | Oppdater `agent.yaml` → `environment_variables` seksjon |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ikke konfigurert | Foundry setter dette automatisk - sørg for at du deployer via utvidelsen |
   | `OSError: port 8088 already in use` | Dockerfile eksponerer feil port eller portkonflikt | Verifiser `EXPOSE 8088` i Dockerfile og `CMD ["python", "main.py"]` |
   | Container avsluttes med kode 1 | Ubehandlet unntak i `main()` | Test lokalt først ([Modul 5](05-test-locally.md)) for å fange feil før distribusjon |

3. **Deploy på nytt etter fiks:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → velg samme agent → deploy ny versjon.

### Distribusjonen tar for lang tid

Multi-agent containere tar lengre tid å starte fordi de lager 4 agent-instansser ved oppstart. Vanlige oppstartstider:

| Fase | Forventet varighet |
|-------|-------------------|
| Container image bygging | 1-3 minutter |
| Image push til ACR | 30-60 sekunder |
| Container start (enkel agent) | 15-30 sekunder |
| Container start (multi-agent) | 30-120 sekunder |
| Agent tilgjengelig i Playground | 1-2 minutter etter "Started" |

> Hvis "Pending" status varer over 5 minutter, sjekk container-logger for feil.

---

## RBAC og tilgangsproblemer

### `403 Forbidden` eller `AuthorizationFailed`

Du trenger **[Azure AI User](https://aka.ms/foundry-ext-project-role)** rolle på Foundry-prosjektet ditt:

1. Gå til [Azure Portal](https://portal.azure.com) → ditt Foundry **prosjekt** ressurs.
2. Klikk **Access control (IAM)** → **Role assignments**.
3. Søk etter navnet ditt → bekreft at **Azure AI User** er listet.
4. Hvis mangler: **Legg til** → **Add role assignment** → søk etter **Azure AI User** → tildel til din konto.

Se dokumentasjonen for [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) for detaljer.

### Modell distribusjon ikke tilgjengelig

Hvis agenten gir modellrelaterte feil:

1. Verifiser at modellen er distribuert: Foundry sidepanel → utvid prosjekt → **Models** → se etter `gpt-4.1-mini` (eller din modell) med status **Succeeded**.
2. Verifiser at distribusjonsnavnet stemmer: sammenlign `MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med faktisk distribusjonsnavn i sidepanelet.
3. Hvis distribusjonen er utløpt (gratis nivå): deploy på nytt fra [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector problemer

### Inspector åpnes men viser "Disconnected"

1. Verifiser at serveren kjører: sjekk etter "Server running on http://localhost:8088" i terminal.
2. Sjekk port `5679`: Inspector kobler via debugpy på port 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Restart server og åpne Inspector på nytt.

### Inspector viser delvis svar

Multi-agent svar er lange og strømmer inkrementelt. Vent på at hele svaret fullføres (kan ta 30-60 sekunder avhengig av antall gap-kort og MCP-verktøysanrop).

Hvis svaret konsekvent er avkortet:
- Sjekk at GapAnalyzer instrukser har `CRITICAL:` blokken som forhindrer sammenslåing av gap-kort.
- Sjekk modellens token-grense - `gpt-4.1-mini` støtter opptil 32K output tokens, noe som skal være tilstrekkelig.

---

## Ytelsestips

### Trege svar

Multi-agent arbeidsflyter er naturlig tregere enn enkelt-agent pga. sekvensielle avhengigheter og MCP-verktøysanrop.

| Optimalisering | Hvordan | Effekt |
|----------------|---------|--------|
| Reduser MCP-anrop | Senk `max_results` parameter i verktøyet | Færre HTTP rundreiser |
| Forenkle instruksjoner | Kortere, mer fokuserte agent-prompt | Raskere LLM inferens |
| Bruk `gpt-4.1-mini` | Raskere enn `gpt-4.1` under utvikling | ~2x hastighetsforbedring |
| Reduser detaljnivå i gap-kort | Forenkle gap-kortformat i GapAnalyzer instrukser | Mindre output som skal genereres |

### Typiske svartider (lokalt)

| Konfigurasjon | Forventet tid |
|---------------|---------------|
| `gpt-4.1-mini`, 3-5 gap-kort | 30-60 sekunder |
| `gpt-4.1-mini`, 8+ gap-kort | 60-120 sekunder |
| `gpt-4.1`, 3-5 gap-kort | 60-120 sekunder |
---

## Få hjelp

Hvis du sitter fast etter å ha prøvd løsningene ovenfor:

1. **Sjekk serverloggene** - De fleste feil gir en Python stack trace i terminalen. Les hele tracebacken.
2. **Søk etter feilmeldingen** - Kopier feilmeldingen og søk i [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Åpne en sak** - Opprett en sak i [workshop-repositoriet](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) med:
   - Feilmeldingen eller skjermbilde
   - Dine pakkversjoner (`pip list | Select-String "agent-framework"`)
   - Din Python-versjon (`python --version`)
   - Om problemet er lokalt eller etter distribusjon

---

### Sjekkpunkt

- [ ] Du kan identifisere og fikse de vanligste feilene med multi-agenter ved hjelp av hurtigreferansetabellen
- [ ] Du vet hvordan du sjekker og fikser `.env` konfigurasjonsproblemer
- [ ] Du kan verifisere at pakkversjoner stemmer overens med krevd matrise
- [ ] Du forstår MCP loggoppføringer og kan diagnostisere verktøyfeil
- [ ] Du vet hvordan du sjekker containerlogger for distribusjonsfeil
- [ ] Du kan verifisere RBAC-roller i Azure-portalen

---

**Forrige:** [07 - Verify in Playground](07-verify-in-playground.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettingstjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vennligst vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på dets opprinnelige språk bør betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for misforståelser eller feiltolkninger som oppstår som følge av bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->