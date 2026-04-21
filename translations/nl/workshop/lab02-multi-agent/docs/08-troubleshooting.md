# Module 8 - Problemen oplossen (Multi-Agent)

Deze module behandelt veelvoorkomende fouten, oplossingen en debugstrategieën specifiek voor de multi-agent workflow. Raadpleeg voor algemene Foundry-implementatieproblemen ook de [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Snelle referentie: Fout → Oplossing

| Fout / Symbool | Waarschijnlijke oorzaak | Oplossing |
|----------------|--------------------------|-----------|
| `RuntimeError: Missing required environment variable(s)` | `.env` bestand ontbreekt of waarden niet ingesteld | Maak `.env` aan met `PROJECT_ENDPOINT=<your-endpoint>` en `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuele omgeving niet geactiveerd of dependencies niet geïnstalleerd | Voer uit `.\.venv\Scripts\Activate.ps1` en daarna `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP pakket niet geïnstalleerd (ontbreekt in requirements) | Voer uit `pip install mcp` of controleer of `requirements.txt` het als transitieve dependency bevat |
| Agent start, maar geeft lege respons terug | `output_executors` komt niet overeen of randen ontbreken | Controleer `output_executors=[gap_analyzer]` en dat alle randen bestaan in `create_workflow()` |
| Slechts 1 gap card (rest ontbreekt) | GapAnalyzer instructies onvolledig | Voeg de `CRITICAL:` paragraaf toe aan `GAP_ANALYZER_INSTRUCTIONS` - zie [Module 3](03-configure-agents.md) |
| Fit score is 0 of ontbreekt | MatchingAgent ontving geen upstream data | Controleer dat zowel `add_edge(resume_parser, matching_agent)` als `add_edge(jd_agent, matching_agent)` bestaan |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server weigerde de toolaanroep | Controleer internetconnectiviteit. Probeer `https://learn.microsoft.com/api/mcp` in browser te openen. Probeer opnieuw |
| Geen Microsoft Learn URL’s in output | MCP tool niet geregistreerd of endpoint onjuist | Controleer `tools=[search_microsoft_learn_for_plan]` op GapAnalyzer en dat `MICROSOFT_LEARN_MCP_ENDPOINT` correct is |
| `Address already in use: port 8088` | Een ander proces gebruikt poort 8088 | Voer uit `netstat -ano \| findstr :8088` (Windows) of `lsof -i :8088` (macOS/Linux) en stop het conflicterende proces |
| `Address already in use: port 5679` | Debugpy poortconflict | Stop andere debugsessies. Voer uit `netstat -ano \| findstr :5679` om het proces te vinden en te beëindigen |
| Agent Inspector opent niet | Server is niet volledig gestart of poortconflict | Wacht op "Server running" log. Controleer of poort 5679 vrij is |
| `azure.identity.CredentialUnavailableError` | Niet aangemeld bij Azure CLI | Voer `az login` uit en herstart de server |
| `azure.core.exceptions.ResourceNotFoundError` | Modelimplementatie bestaat niet | Controleer dat `MODEL_DEPLOYMENT_NAME` overeenkomt met een geïmplementeerd model in je Foundry-project |
| Containerstatus "Failed" na implementatie | Container crashed bij opstarten | Controleer containerlogs in Foundry zijbalk. Veel voorkomend: ontbrekende env var of importfout |
| Implementatie blijft > 5 minuten op "Pending" staan | Container doet te lang over starten of resourcebeperkingen | Wacht tot 5 minuten voor multi-agent (maakt 4 agent-instanties aan). Bij aanhoudend "pending", check logs |
| `ValueError` van `WorkflowBuilder` | Ongeldige grafiekconfiguratie | Zorg dat `start_executor` is ingesteld, `output_executors` een lijst is, en dat er geen circulaire randen zijn |

---

## Omgevings- en configuratieproblemen

### Ontbrekende of onjuiste `.env` waarden

Het `.env` bestand moet in de `PersonalCareerCopilot/` map staan (zelfde niveau als `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Verwachte `.env` inhoud:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Jouw PROJECT_ENDPOINT vinden:**  
- Open de **Microsoft Foundry** zijbalk in VS Code → rechtsklik je project → **Copy Project Endpoint**.  
- Of ga naar [Azure Portal](https://portal.azure.com) → je Foundry project → **Overzicht** → **Project endpoint**.

> **Jouw MODEL_DEPLOYMENT_NAME vinden:** In de Foundry zijbalk, vouw je project uit → **Models** → zoek je geïmplementeerde modelnaam (bijv. `gpt-4.1-mini`).

### Prioriteit van env variabelen

`main.py` gebruikt `load_dotenv(override=False)`, wat betekent:

| Prioriteit | Bron | Wint als beide zijn ingesteld? |
|------------|------|--------------------------------|
| 1 (hoogst) | Shell omgevingsvariabele | Ja |
| 2 | `.env` bestand | Alleen als shell var niet is ingesteld |

Dit betekent dat Foundry runtime env vars (ingesteld via `agent.yaml`) voorrang krijgen boven `.env` waarden tijdens gehoste implementatie.

---

## Versiecompatibiliteit

### Pakketversiematrix

De multi-agent workflow vereist specifieke pakketversies. Niet-overeenkomende versies veroorzaken runtime fouten.

| Pakket | Vereiste versie | Controle commando |
|--------|-----------------|-------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | laatste pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Veelvoorkomende versie fouten

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Opgelost: upgraden naar rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` niet gevonden of Inspector incompatibel:**

```powershell
# Opgelost: installeren met de --pre vlag
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Oplossen: upgrade mcp-pakket
pip install mcp --upgrade
```

### Controleer alle versies tegelijk

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Verwachte output:

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

## MCP tool problemen

### MCP tool geeft geen resultaten terug

**Symptoom:** Gap cards tonen "No results returned from Microsoft Learn MCP" of "No direct Microsoft Learn results found".

**Mogelijke oorzaken:**

1. **Netwerkprobleem** - Het MCP endpoint (`https://learn.microsoft.com/api/mcp`) is niet bereikbaar.  
   ```powershell
   # Test verbinding
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Als dit `200` teruggeeft, is het endpoint bereikbaar.

2. **Te specifieke query** - De vaardigheidsnaam is te niche voor Microsoft Learn zoekfunctie.  
   - Dit is te verwachten voor zeer gespecialiseerde vaardigheden. De tool heeft een fallback URL in de respons.

3. **MCP sessie time-out** - De Streamable HTTP verbinding is verlopen.  
   - Probeer het verzoek opnieuw. MCP sessies zijn vluchtig en vereisen mogelijk herverbinding.

### Uitleg MCP logs

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Betekenis | Actie |
|-----|-----------|-------|
| `GET → 405` | MCP client test tijdens initialisatie | Normaal - negeer |
| `POST → 200` | Toolaanroep geslaagd | Verwacht |
| `DELETE → 405` | MCP client test tijdens opruiming | Normaal - negeer |
| `POST → 400` | Slecht verzoek (onjuiste query) | Controleer de `query` parameter in `search_microsoft_learn_for_plan()` |
| `POST → 429` | Rate limiting | Wacht en probeer opnieuw. Verminder `max_results` parameter |
| `POST → 500` | MCP server fout | Tijdelijk - probeer opnieuw. Bij aanhoudend probleem kan Microsoft Learn MCP API down zijn |
| Timeout verbinding | Netwerkprobleem of MCP server onbeschikbaar | Controleer internet. Probeer `curl https://learn.microsoft.com/api/mcp` |

---

## Implementatieproblemen

### Container start niet na implementatie

1. **Controleer containerlogs:**  
   - Open de **Microsoft Foundry** zijbalk → vouw **Hosted Agents (Preview)** uit → klik je agent → vouw de versie uit → **Container Details** → **Logs**.  
   - Zoek naar Python stacktraces of fouten over ontbrekende modules.

2. **Veelvoorkomende container startup fouten:**

   | Fout in logs | Oorzaak | Oplossing |
   |--------------|---------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` mist een pakket | Voeg het pakket toe, implementeer opnieuw |
   | `RuntimeError: Missing required environment variable` | Env vars in `agent.yaml` niet ingesteld | Pas `agent.yaml` aan → sectie `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity niet geconfigureerd | Foundry stelt dit automatisch in - zorg voor implementatie via extensie |
   | `OSError: port 8088 already in use` | Dockerfile exposeert verkeerde poort of poortconflict | Controleer `EXPOSE 8088` in Dockerfile en `CMD ["python", "main.py"]` |
   | Container stopt met code 1 | Ongehandelde uitzondering in `main()` | Test lokaal eerst ([Module 5](05-test-locally.md)) om fouten voor implementatie te vangen |

3. **Implementeer opnieuw na fix:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → selecteer dezelfde agent → implementeer nieuwe versie.

### Implementatie duurt te lang

Multi-agent containers starten langer omdat ze bij opstarten 4 agent-instanties creëren. Normale opstarttijden:

| Fase | Verwachte duur |
|-------|----------------|
| Container image build | 1-3 minuten |
| Image push naar ACR | 30-60 seconden |
| Container start (enkele agent) | 15-30 seconden |
| Container start (multi-agent) | 30-120 seconden |
| Agent beschikbaar in Playground | 1-2 minuten na "Started" |

> Als status "Pending" langer dan 5 minuten aanhoudt, controleer containerlogs op fouten.

---

## RBAC- en machtigingsproblemen

### `403 Forbidden` of `AuthorizationFailed`

Je hebt de **[Azure AI User](https://aka.ms/foundry-ext-project-role)** rol nodig op je Foundry-project:

1. Ga naar [Azure Portal](https://portal.azure.com) → je Foundry **project** resource.  
2. Klik **Access control (IAM)** → **Role assignments**.  
3. Zoek je naam → controleer dat **Azure AI User** is vermeld.  
4. Ontbreekt deze: **Add** → **Add role assignment** → zoek **Azure AI User** → wijs toe aan je account.

Zie de [RBAC voor Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) documentatie voor details.

### Modelimplementatie niet toegankelijk

Als de agent model-gerelateerde fouten geeft:

1. Controleer dat het model is geïmplementeerd: Foundry zijbalk → vouw project uit → **Models** → controleer op `gpt-4.1-mini` (of jouw model) met status **Succeeded**.  
2. Controleer dat de implementatienaam overeenkomt: vergelijk `MODEL_DEPLOYMENT_NAME` in `.env` (of `agent.yaml`) met de daadwerkelijke implementatienaam in de zijbalk.  
3. Als de implementatie verlopen is (gratis tier): implementeer opnieuw vanuit [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector problemen

### Inspector opent maar toont "Disconnected"

1. Controleer dat de server draait: zoek naar "Server running on http://localhost:8088" in de terminal.  
2. Controleer poort `5679`: Inspector maakt verbinding via debugpy op poort 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Herstart de server en open Inspector opnieuw.

### Inspector toont gedeeltelijke respons

Multi-agent responsen zijn lang en worden incrementeel gestreamd. Wacht tot de volledige respons klaar is (kan 30-60 seconden duren, afhankelijk van het aantal gap cards en MCP tool-aanroepen).

Als de respons steeds ingekort is:  
- Controleer dat de GapAnalyzer instructies de `CRITICAL:` sectie bevatten die voorkomt dat gap cards worden gecombineerd.  
- Controleer de tokenlimiet van je model - `gpt-4.1-mini` ondersteunt tot 32K output tokens, wat voldoende moet zijn.

---

## Prestatie-tips

### Trage responsen

Multi-agent workflows zijn intrinsiek trager dan single-agent vanwege sequentiële afhankelijkheden en MCP tool-aanroepen.

| Optimalisatie | Hoe | Impact |
|---------------|-----|--------|
| MCP-aanroepen verminderen | Verlaag `max_results` parameter in de tool | Minder HTTP verzoeken |
| Instructies vereenvoudigen | Kortere, meer gerichte agent prompts | Snellere LLM inferentie |
| Gebruik `gpt-4.1-mini` | Sneller dan `gpt-4.1` voor ontwikkeling | Ongeveer 2x sneller |
| Minder detail in gap cards | Vereenvoudig het gap card formaat in GapAnalyzer instructies | Minder output om te genereren |

### Typische responstijden (lokaal)

| Configuratie | Verwachte tijd |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap cards | 30-60 seconden |
| `gpt-4.1-mini`, 8+ gap cards | 60-120 seconden |
| `gpt-4.1`, 3-5 gap cards | 60-120 seconden |
---

## Hulp krijgen

Als je vastloopt na het proberen van de bovenstaande oplossingen:

1. **Controleer de serverlogs** - De meeste fouten produceren een Python stacktrace in de terminal. Lees de volledige traceback.
2. **Zoek de foutmelding op** - Kopieer de fouttekst en zoek in de [Microsoft Q&A voor Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Open een issue** - Maak een issue aan in de [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) met:
   - De foutmelding of screenshot
   - Je pakketversies (`pip list | Select-String "agent-framework"`)
   - Je Python-versie (`python --version`)
   - Of het probleem lokaal is of na deployment

---

### Controlepunten

- [ ] Je kunt de meest voorkomende fouten met meerdere agents identificeren en oplossen met behulp van de snelreferentietabel
- [ ] Je weet hoe je problemen met de `.env`-configuratie kunt controleren en oplossen
- [ ] Je kunt verifiëren dat pakketversies overeenkomen met de vereiste matrix
- [ ] Je begrijpt MCP logboekvermeldingen en kunt tool-fouten diagnosticeren
- [ ] Je weet hoe je containerlogs kunt controleren op deploymentfouten
- [ ] Je kunt RBAC-rollen verifiëren in de Azure Portal

---

**Vorige:** [07 - Verifiëren in Playground](07-verify-in-playground.md) · **Home:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI-vertalingsservice [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat automatische vertalingen fouten of onjuistheden kunnen bevatten. Het oorspronkelijke document in de oorspronkelijke taal moet als de gezaghebbende bron worden beschouwd. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->