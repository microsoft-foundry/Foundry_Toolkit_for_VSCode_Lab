# Module 8 - Felsökning (Multi-Agent)

Den här modulen täcker vanliga fel, åtgärder och felsökningsstrategier specifika för multi-agent arbetsflödet. För allmänna problem med Foundry-distribution, se även [Lab 01 felsökningsguide](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Snabbreferens: Fel → Åtgärd

| Fel / Symptom | Trolig orsak | Åtgärd |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env`-fil saknas eller värden inte satta | Skapa `.env` med `PROJECT_ENDPOINT=<your-endpoint>` och `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuellt miljö inte aktiverad eller beroenden inte installerade | Kör `.\.venv\Scripts\Activate.ps1` sedan `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP-paketet inte installerat (saknas i requirements) | Kör `pip install mcp` eller kontrollera att `requirements.txt` inkluderar det som transitivt beroende |
| Agenten startar men returnerar tomt svar | `output_executors` mismatch eller saknade kanter | Verifiera `output_executors=[gap_analyzer]` och att alla kanter finns i `create_workflow()` |
| Endast 1 gap-kort (resterande saknas) | GapAnalyzer-instruktioner ofullständiga | Lägg till `CRITICAL:`-avsnittet i `GAP_ANALYZER_INSTRUCTIONS` - se [Module 3](03-configure-agents.md) |
| Fit-poängen är 0 eller saknas | MatchingAgent mottog inte upstream-data | Verifiera att både `add_edge(resume_parser, matching_agent)` och `add_edge(jd_agent, matching_agent)` finns |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP-servern avvisade verktygsanropet | Kontrollera internetanslutning. Testa att öppna `https://learn.microsoft.com/api/mcp` i webbläsare. Försök igen |
| Inga Microsoft Learn-URL:er i utdata | MCP-verktyget inte registrerat eller fel endpoint | Verifiera `tools=[search_microsoft_learn_for_plan]` på GapAnalyzer och att `MICROSOFT_LEARN_MCP_ENDPOINT` är korrekt |
| `Address already in use: port 8088` | En annan process använder port 8088 | Kör `netstat -ano \| findstr :8088` (Windows) eller `lsof -i :8088` (macOS/Linux) och stoppa den konfliktande processen |
| `Address already in use: port 5679` | Konflikt på debugpy-port | Stoppa andra debug-sessioner. Kör `netstat -ano \| findstr :5679` för att hitta och avsluta processen |
| Agent Inspector öppnas inte | Servern är inte helt startad eller portkonflikt | Vänta på "Server running" i loggen. Kontrollera att port 5679 är ledig |
| `azure.identity.CredentialUnavailableError` | Ej inloggad i Azure CLI | Kör `az login` och starta om servern |
| `azure.core.exceptions.ResourceNotFoundError` | Modellutplacering finns inte | Kontrollera att `MODEL_DEPLOYMENT_NAME` matchar en utplacerad modell i ditt Foundry-projekt |
| Containerstatus "Failed" efter distribution | Containerkrasch vid start | Kontrollera containerloggar i Foundry sidopanel. Vanligt: saknad miljövariabel eller importfel |
| Distribution visar "Pending" > 5 minuter | Containern tar för lång tid att starta eller resursgränser | Vänta upp till 5 minuter för multi-agent (skapar 4 agentinstanser). Om fortfarande pending, kontrollera loggar |
| `ValueError` från `WorkflowBuilder` | Ogiltig grafkonfiguration | Säkerställ att `start_executor` är satt, `output_executors` är en lista och att inga cirkulära kanter finns |

---

## Miljö- och konfigurationsproblem

### Saknade eller felaktiga `.env`-värden

`.env`-filen måste finnas i `PersonalCareerCopilot/`-katalogen (samma nivå som `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Förväntat innehåll i `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Hitta ditt PROJECT_ENDPOINT:**  
- Öppna **Microsoft Foundry** sidopanel i VS Code → högerklicka på ditt projekt → **Copy Project Endpoint**.  
- Eller gå till [Azure Portal](https://portal.azure.com) → ditt Foundry-projekt → **Overview** → **Project endpoint**.

> **Hitta ditt MODEL_DEPLOYMENT_NAME:** I Foundry sidopanel, expandera ditt projekt → **Models** → hitta namnet på din utplacerade modell (t.ex. `gpt-4.1-mini`).

### Prioritering av miljövariabler

`main.py` använder `load_dotenv(override=False)`, vilket innebär:

| Prioritet | Källa | Vinner om båda är satta? |
|----------|--------|------------------------|
| 1 (högst) | Shell-miljövariabel | Ja |
| 2 | `.env`-fil | Endast om shell-variabel inte är satt |

Detta betyder att Foundry runtime-miljövariabler (satta via `agent.yaml`) har företräde över `.env` under hostad distribution.

---

## Versionskompatibilitet

### Paketversionsmatris

Multi-agent arbetsflödet kräver specifika paketversioner. Felaktiga versioner orsakar runtime-fel.

| Paket | Krävd version | Kontrollkommando |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | senaste pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Vanliga versionsfel

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fixa: uppgradera till rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` saknas eller Inspector inkompatibel:**

```powershell
# Fixa: installera med --pre-flaggan
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fixa: uppgradera mcp-paketet
pip install mcp --upgrade
```

### Kontrollera alla versioner på en gång

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Förväntad utdata:

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

## MCP-verktygsproblem

### MCP-verktyget returnerar inga resultat

**Symptom:** Gap-korten säger "No results returned from Microsoft Learn MCP" eller "No direct Microsoft Learn results found".

**Möjliga orsaker:**

1. **Nätverksproblem** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) är otillgänglig.  
   ```powershell
   # Testa anslutning
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
 Om detta returnerar `200` är endpoint nåbar.

2. **Frågan är för specifik** - Kompetensnamnet är för nischat för Microsoft Learn-sökning.  
   - Detta är förväntat för mycket specialiserade kompetenser. Verktyget har en fallback-URL i svaret.

3. **MCP-session time out** - Streamable HTTP-anslutningen gick ut.  
   - Försök igen. MCP-sessioner är flyktiga och kan behöva återanslutas.

### MCP-loggar förklarade

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Logg | Betydelse | Åtgärd |
|-----|---------|--------|
| `GET → 405` | MCP-klienten gör sonderingar vid initiering | Normalt - ignorera |
| `POST → 200` | Verktygsanrop lyckades | Förväntat |
| `DELETE → 405` | MCP-klienten gör sonderingar vid städning | Normalt - ignorera |
| `POST → 400` | Dålig förfrågan (felaktig fråga) | Kontrollera `query`-parametern i `search_microsoft_learn_for_plan()` |
| `POST → 429` | Begränsad av hastighet | Vänta och försök igen. Minska `max_results`-parametern |
| `POST → 500` | MCP-serverfel | Tillfälligt - försök igen. Om kvarstår, kan Microsoft Learn MCP API vara nere |
| Timeout för anslutning | Nätverksproblem eller MCP-server otillgänglig | Kontrollera internet. Testa `curl https://learn.microsoft.com/api/mcp` |

---

## Distributionsproblem

### Container startar inte efter distribution

1. **Kontrollera containerloggar:**  
   - Öppna **Microsoft Foundry** sidopanel → expandera **Hosted Agents (Preview)** → klicka på din agent → expandera version → **Container Details** → **Logs**.  
   - Leta efter Python stacktraces eller saknade modul-fel.

2. **Vanliga container-startfel:**

   | Fel i loggar | Orsak | Åtgärd |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` saknar paket | Lägg till paketet, distribuera om |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` miljövariabler inte satta | Uppdatera sektion `environment_variables` i `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity ej konfigurerad | Foundry sätter detta automatiskt - se till att distribuera via extension |
   | `OSError: port 8088 already in use` | Dockerfile exponerar fel port eller portkonflikt | Kontrollera `EXPOSE 8088` i Dockerfile och `CMD ["python", "main.py"]` |
   | Container avslutas med kod 1 | Ohanterat undantag i `main()` | Testa lokalt först ([Module 5](05-test-locally.md)) för att fånga fel innan distribution |

3. **Distribuera om efter fix:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → välj samma agent → distribuera ny version.

### Distribution tar för lång tid

Multi-agent-containrar tar längre tid att starta eftersom de skapar 4 agentinstanser vid uppstart. Normala starttider:

| Steg | Förväntad tid |
|-------|------------------|
| Bygga containerimage | 1-3 minuter |
| Pusha image till ACR | 30-60 sekunder |
| Containerstart (enkel agent) | 15-30 sekunder |
| Containerstart (multi-agent) | 30-120 sekunder |
| Agent tillgänglig i Playground | 1-2 minuter efter "Started" |

> Om "Pending"-status kvarstår efter 5 minuter, kontrollera containerloggar för fel.

---

## RBAC och behörighetsproblem

### `403 Forbidden` eller `AuthorizationFailed`

Du behöver rollen **[Azure AI User](https://aka.ms/foundry-ext-project-role)** på ditt Foundry-projekt:

1. Gå till [Azure Portal](https://portal.azure.com) → din Foundry **projekt**-resurs.  
2. Klicka **Access control (IAM)** → **Role assignments**.  
3. Sök på ditt namn → verifiera att **Azure AI User** finns listad.  
4. Om saknas: **Add** → **Add role assignment** → sök efter **Azure AI User** → tilldela till ditt konto.

Se dokumentationen för [RBAC för Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) för detaljer.

### Modellutplacering ej tillgänglig

Om agenten returnerar modellrelaterade fel:

1. Verifiera att modellen är utplacerad: Foundry sidopanel → expandera projekt → **Models** → kontrollera `gpt-4.1-mini` (eller din modell) med status **Succeeded**.  
2. Verifiera att utplaceringsnamnet stämmer: jämför `MODEL_DEPLOYMENT_NAME` i `.env` (eller `agent.yaml`) med det faktiska namnet i sidopanelen.  
3. Om utplaceringen gått ut (gratisnivå): distribuera om från [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector-problem

### Inspector öppnas men visar "Disconnected"

1. Kontrollera att servern körs: leta efter "Server running on http://localhost:8088" i terminalen.  
2. Kontrollera port `5679`: Inspector ansluter via debugpy på port 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Starta om servern och öppna Inspector igen.

### Inspector visar delvis svar

Multi-agent svar är långa och strömmas inkrementellt. Vänta på fullständigt svar (kan ta 30-60 sekunder beroende på antal gap-kort och MCP-verktygsanrop).

Om svaret konsekvent är avklippt:  
- Kontrollera att GapAnalyzer-instruktionerna har `CRITICAL:`-block som förhindrar sammanslagning av gap-kort.  
- Kontrollera din modells token-gräns - `gpt-4.1-mini` stödjer upp till 32K output tokens, vilket bör räcka.

---

## Prestandatips

### Långsamma svar

Multi-agent arbetsflöden är naturligt långsammare än enkel agent på grund av sekventiella beroenden och MCP-verktygsanrop.

| Optimering | Hur | Effekt |
|-------------|-----|--------|
| Minska MCP-anrop | Sänk `max_results`-parametern i verktyget | Färre HTTP-omgångar |
| Förenkla instruktioner | Kortare, mer fokuserade agent-promptar | Snabbare LLM-inferens |
| Använd `gpt-4.1-mini` | Snabbare än `gpt-4.1` för utveckling | ~2x snabbare |
| Minska detalj i gap-kort | Förenkla gap-kortsformatet i GapAnalyzer-instruktionerna | Mindre output att generera |

### Typiska svarstider (lokalt)

| Konfiguration | Förväntad tid |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap-kort | 30-60 sekunder |
| `gpt-4.1-mini`, 8+ gap-kort | 60-120 sekunder |
| `gpt-4.1`, 3-5 gap-kort | 60-120 sekunder |
---

## Få hjälp

Om du fastnar efter att ha försökt med lösningarna ovan:

1. **Kontrollera serverloggarna** - De flesta fel ger en Python stacktrace i terminalen. Läs hela tracebacken.
2. **Sök efter felmeddelandet** - Kopiera feltexten och sök i [Microsoft Q&A för Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Öppna ett ärende** - Skapa ett ärende i [workshop-repositoriet](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) med:
   - Felmeddelandet eller en skärmdump
   - Dina paketversioner (`pip list | Select-String "agent-framework"`)
   - Din Python-version (`python --version`)
   - Om felet är lokalt eller efter driftsättning

---

### Kontrollpunkt

- [ ] Du kan identifiera och åtgärda de vanligaste multi-agent-felen med hjälp av snabbreferenstabellen
- [ ] Du vet hur man kontrollerar och åtgärdar `.env`-konfigurationsproblem
- [ ] Du kan verifiera att paketversionerna stämmer överens med den kräva matrisen
- [ ] Du förstår MCP-logginlägg och kan diagnostisera verktygshaverier
- [ ] Du vet hur man kontrollerar containerloggar vid driftsättningsfel
- [ ] Du kan verifiera RBAC-roller i Azure-portalen

---

**Föregående:** [07 - Verify in Playground](07-verify-in-playground.md) · **Hem:** [Lab 02 README](../README.md) · [Workshop Hem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, vänligen ha i åtanke att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->