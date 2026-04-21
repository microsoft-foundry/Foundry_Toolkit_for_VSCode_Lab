# Modul 8 - Fehlerbehebung (Multi-Agent)

Dieses Modul behandelt häufige Fehler, Lösungen und Debugging-Strategien, die speziell für den Multi-Agent-Workflow gelten. Für allgemeine Foundry-Bereitstellungsprobleme siehe auch den [Lab 01 Fehlerbehebungsleitfaden](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Schnellreferenz: Fehler → Lösung

| Fehler / Symptom | Wahrscheinliche Ursache | Lösung |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` Datei fehlt oder Werte nicht gesetzt | Erstelle `.env` mit `PROJECT_ENDPOINT=<your-endpoint>` und `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuelle Umgebung nicht aktiviert oder Abhängigkeiten nicht installiert | Führe `.\.venv\Scripts\Activate.ps1` aus, dann `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP-Paket nicht installiert (fehlt in requirements) | Führe `pip install mcp` aus oder prüfe, dass `requirements.txt` es als transitive Abhängigkeit enthält |
| Agent startet, gibt aber leere Antwort zurück | `output_executors` stimmt nicht überein oder Kanten fehlen | Prüfe `output_executors=[gap_analyzer]` und dass alle Kanten in `create_workflow()` existieren |
| Nur 1 Gap Card (Rest fehlt) | GapAnalyzer-Anweisungen unvollständig | Füge den `CRITICAL:` Absatz zu `GAP_ANALYZER_INSTRUCTIONS` hinzu - siehe [Modul 3](03-configure-agents.md) |
| Fit Score ist 0 oder fehlt | MatchingAgent hat keine Eingabedaten erhalten | Prüfe, dass sowohl `add_edge(resume_parser, matching_agent)` als auch `add_edge(jd_agent, matching_agent)` existieren |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP-Server hat Tool-Aufruf abgelehnt | Prüfe Internetverbindung. Öffne `https://learn.microsoft.com/api/mcp` im Browser. Versuche es erneut |
| Keine Microsoft Learn URLs in Ausgabe | MCP-Tool nicht registriert oder falscher Endpunkt | Prüfe `tools=[search_microsoft_learn_for_plan]` im GapAnalyzer und dass `MICROSOFT_LEARN_MCP_ENDPOINT` korrekt ist |
| `Address already in use: port 8088` | Ein anderer Prozess nutzt Port 8088 | Führe `netstat -ano \| findstr :8088` (Windows) oder `lsof -i :8088` (macOS/Linux) aus und beende den Konfliktprozess |
| `Address already in use: port 5679` | Debugpy Port-Konflikt | Beende andere Debug-Sitzungen. Führe `netstat -ano \| findstr :5679` aus, finde und töte den Prozess |
| Agent Inspector lässt sich nicht öffnen | Server nicht vollständig gestartet oder Port-Konflikt | Warte auf "Server running" Log. Prüfe, dass Port 5679 frei ist |
| `azure.identity.CredentialUnavailableError` | Nicht bei Azure CLI angemeldet | Führe `az login` aus, dann Server neu starten |
| `azure.core.exceptions.ResourceNotFoundError` | Modell-Bereitstellung existiert nicht | Prüfe, dass `MODEL_DEPLOYMENT_NAME` zu einem bereitgestellten Modell in deinem Foundry-Projekt passt |
| Containerstatus "Failed" nach Bereitstellung | Containerabsturz beim Start | Prüfe Container-Logs in der Foundry-Seitenleiste. Häufig: fehlende Umgebungsvariable oder Importfehler |
| Bereitstellung zeigt >5 Minuten "Pending" | Container braucht zu lange zum Starten oder Ressourcenlimits | Warte bis zu 5 Minuten für Multi-Agent (erstellt 4 Agent-Instanzen). Wenn weiterhin Pending, Logs prüfen |
| `ValueError` von `WorkflowBuilder` | Ungültige Graph-Konfiguration | Sicherstellen, dass `start_executor` gesetzt ist, `output_executors` eine Liste ist und keine zirkulären Kanten existieren |

---

## Umgebung und Konfigurationsprobleme

### Fehlende oder falsche `.env` Werte

Die `.env` Datei muss im Verzeichnis `PersonalCareerCopilot/` liegen (auf gleicher Ebene wie `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Erwarteter `.env` Inhalt:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **So findest du deinen PROJECT_ENDPOINT:**  
- Öffne die **Microsoft Foundry** Seitenleiste in VS Code → Rechtsklick auf dein Projekt → **Projektendpunkt kopieren**.  
- Oder gehe zum [Azure Portal](https://portal.azure.com) → dein Foundry-Projekt → **Übersicht** → **Projektendpunkt**.

> **So findest du deinen MODEL_DEPLOYMENT_NAME:** In der Foundry-Seitenleiste dein Projekt erweitern → **Modelle** → suche den Namen des bereitgestellten Modells (z.B. `gpt-4.1-mini`).

### Vorrang von Umgebungsvariablen

`main.py` verwendet `load_dotenv(override=False)`, was bedeutet:

| Priorität | Quelle | Gewinnt, wenn beide gesetzt sind? |
|----------|--------|------------------------|
| 1 (höchste) | Shell-Umgebungsvariable | Ja |
| 2 | `.env` Datei | Nur wenn Shell-Var nicht gesetzt ist |

Das bedeutet, dass Foundry-Laufzeit-Umgebungsvariablen (gesetzt über `agent.yaml`) Vorrang vor `.env` Werten während der gehosteten Bereitstellung haben.

---

## Versionskompatibilität

### Paketversionsmatrix

Der Multi-Agent-Workflow benötigt bestimmte Paketversionen. Nicht übereinstimmende Versionen verursachen Laufzeitfehler.

| Paket | Erforderliche Version | Prüfbefehl |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | neueste Vorabversion | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Häufige Versionsfehler

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fehlerbehebung: Upgrade auf rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nicht gefunden oder Inspector inkompatibel:**

```powershell
# Korrektur: Installation mit dem --pre-Flag
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fehlerbehebung: mcp-Paket aktualisieren
pip install mcp --upgrade
```

### Alle Versionen auf einmal überprüfen

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Erwartete Ausgabe:

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

## MCP Tool-Probleme

### MCP Tool liefert keine Ergebnisse

**Symptom:** Gap Cards zeigen „No results returned from Microsoft Learn MCP“ oder „No direct Microsoft Learn results found“.

**Mögliche Ursachen:**

1. **Netzwerkproblem** - Der MCP-Endpunkt (`https://learn.microsoft.com/api/mcp`) ist nicht erreichbar.  
   ```powershell
   # Verbindung testen
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Wenn dies `200` zurückgibt, ist der Endpunkt erreichbar.

2. **Abfrage zu spezifisch** - Der Skillname ist zu spezialisiert für die Microsoft Learn Suche.  
   - Das ist bei sehr spezialisierten Skills zu erwarten. Das Tool enthält eine Fallback-URL in der Antwort.

3. **MCP Session Timeout** - Die Streamable HTTP-Verbindung ist abgelaufen.  
   - Anfrage erneut versuchen. MCP Sitzungen sind flüchtig und müssen eventuell neu verbunden werden.

### MCP Logs erklärt

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Bedeutung | Maßnahme |
|-----|---------|--------|
| `GET → 405` | MCP Client prüft während Initialisierung | Normal - ignorieren |
| `POST → 200` | Tool-Aufruf erfolgreich | Erwartet |
| `DELETE → 405` | MCP Client prüft während Reinigung | Normal - ignorieren |
| `POST → 400` | Ungültige Anfrage (fehlerhafte Abfrage) | Prüfe den `query` Parameter in `search_microsoft_learn_for_plan()` |
| `POST → 429` | Rate Limiting | Warte und versuche erneut. `max_results` Parameter verringern |
| `POST → 500` | MCP Serverfehler | Vorübergehend - erneut versuchen. Falls dauerhaft, ist die Microsoft Learn MCP API möglicherweise ausgefallen |
| Verbindungs-Timeout | Netzwerkproblem oder MCP Server nicht verfügbar | Internet prüfen. Versuche `curl https://learn.microsoft.com/api/mcp` |

---

## Bereitstellungsprobleme

### Container startet nach Bereitstellung nicht

1. **Container-Logs prüfen:**  
   - Öffne die **Microsoft Foundry** Seitenleiste → erweitere **Hosted Agents (Preview)** → klicke deinen Agent → erweitere die Version → **Container Details** → **Logs**.  
   - Suche nach Python-Stacktraces oder fehlenden Modul-Fehlern.

2. **Häufige Container-Startfehler:**

   | Fehler in Logs | Ursache | Lösung |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` fehlt ein Paket | Paket hinzufügen, neu bereitstellen |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` Umgebungsvariablen nicht gesetzt | `agent.yaml` → Abschnitt `environment_variables` aktualisieren |
   | `azure.identity.CredentialUnavailableError` | Managed Identity nicht konfiguriert | Foundry setzt dies automatisch - stelle sicher, dass du über die Extension bereitstellst |
   | `OSError: port 8088 already in use` | Dockerfile exponiert falschen Port oder Portkonflikt | `EXPOSE 8088` im Dockerfile und `CMD ["python", "main.py"]` prüfen |
   | Container endet mit Code 1 | Unbehandelte Ausnahme in `main()` | Lokale Tests zuerst durchführen ([Modul 5](05-test-locally.md)), um Fehler vor dem Bereitstellen zu erkennen |

3. **Nach Fehlerbehebung neu bereitstellen:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → selben Agent wählen → neue Version bereitstellen.

### Bereitstellung dauert zu lange

Multi-Agent-Container brauchen länger zum Start, da sie 4 Agent-Instanzen beim Start erzeugen. Normale Startzeiten:

| Phase | Erwartete Dauer |
|-------|------------------|
| Container-Image-Build | 1-3 Minuten |
| Image Push zu ACR | 30-60 Sekunden |
| Container-Start (Single Agent) | 15-30 Sekunden |
| Container-Start (Multi-Agent) | 30-120 Sekunden |
| Agent im Playground verfügbar | 1-2 Minuten nach "Started" |

> Wenn der Status „Pending“ länger als 5 Minuten anhält, prüfe die Container-Logs auf Fehler.

---

## RBAC- und Berechtigungsprobleme

### `403 Forbidden` oder `AuthorizationFailed`

Du benötigst die **[Azure AI User](https://aka.ms/foundry-ext-project-role)** Rolle für dein Foundry-Projekt:

1. Gehe zum [Azure Portal](https://portal.azure.com) → deine Foundry **Projekt**-Ressource.  
2. Klicke auf **Zugriffskontrolle (IAM)** → **Rollenzuweisungen**.  
3. Suche deinen Namen → bestätige, dass **Azure AI User** gelistet ist.  
4. Falls nicht vorhanden: **Hinzufügen** → **Rollenzuweisung hinzufügen** → suche **Azure AI User** → weise deinem Konto zu.

Siehe die [RBAC für Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) Dokumentation für Details.

### Modellbereitstellung nicht zugreifbar

Wenn der Agent modellbezogene Fehler zurückgibt:

1. Prüfe, ob das Modell bereitgestellt ist: Foundry-Seitenleiste → Projekt erweitern → **Modelle** → suche `gpt-4.1-mini` (oder dein Modell) mit Status **Succeeded**.  
2. Prüfe, dass der Bereitstellungsname übereinstimmt: vergleiche `MODEL_DEPLOYMENT_NAME` in `.env` (oder `agent.yaml`) mit dem tatsächlichen Namen in der Seitenleiste.  
3. Wenn die Bereitstellung abgelaufen ist (Free Tier): stelle es neu bereit aus dem [Modellkatalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector Probleme

### Inspector öffnet sich, zeigt aber „Disconnected“

1. Prüfe, ob der Server läuft: Suche nach „Server running on http://localhost:8088“ im Terminal.  
2. Prüfe Port `5679`: Inspector verbindet sich via debugpy auf Port 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Starte den Server neu und öffne den Inspector erneut.

### Inspector zeigt nur Teilantwort

Multi-Agent-Antworten sind lang und werden inkrementell gestreamt. Warte, bis die komplette Antwort fertig ist (kann 30-60 Sekunden dauern, je nach Anzahl der Gap Cards und MCP Tool-Aufrufen).

Wenn die Antwort konsistent abgeschnitten ist:  
- Prüfe, dass die GapAnalyzer-Anweisungen den `CRITICAL:` Block enthalten, der das Zusammenführen von Gap Cards verhindert.  
- Prüfe das Token-Limit deines Modells – `gpt-4.1-mini` unterstützt bis zu 32K Ausgabe-Token, was ausreichend sein sollte.

---

## Leistungstipps

### Langsame Antworten

Multi-Agent-Workflows sind aufgrund sequentieller Abhängigkeiten und MCP Tool-Aufrufen von Natur aus langsamer als Single-Agent.

| Optimierung | Wie | Auswirkung |
|-------------|-----|------------|
| MCP-Aufrufe reduzieren | `max_results` Parameter im Tool senken | Weniger HTTP-Roundtrips |
| Anweisungen vereinfachen | Kürzere, fokussierte Agent-Prompts | Schnellere LLM-Inferenz |
| `gpt-4.1-mini` nutzen | Schneller als `gpt-4.1` für Entwicklung | Ca. 2x Geschwindigkeitsverbesserung |
| Gap Card Detail reduzieren | Gap Card Format in GapAnalyzer Anweisungen vereinfachen | Weniger Ausgabe zu generieren |

### Typische Antwortzeiten (lokal)

| Konfiguration | Erwartete Zeit |
|--------------|----------------|
| `gpt-4.1-mini`, 3-5 Gap Cards | 30-60 Sekunden |
| `gpt-4.1-mini`, 8+ Gap Cards | 60-120 Sekunden |
| `gpt-4.1`, 3-5 Gap Cards | 60-120 Sekunden |
---

## Hilfe erhalten

Wenn Sie nach den oben genannten Korrekturen nicht weiterkommen:

1. **Überprüfen Sie die Serverprotokolle** – Die meisten Fehler erzeugen eine Python-Stack-Trace im Terminal. Lesen Sie die vollständige Rückverfolgung.
2. **Suchen Sie nach der Fehlermeldung** – Kopieren Sie den Fehlermeldungstext und suchen Sie in den [Microsoft Q&A für Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Öffnen Sie ein Issue** – Erstellen Sie ein Issue im [Workshop-Repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) mit:
   - Der Fehlermeldung oder einem Screenshot
   - Ihren Paketversionen (`pip list | Select-String "agent-framework"`)
   - Ihrer Python-Version (`python --version`)
   - Ob das Problem lokal oder nach der Bereitstellung auftritt

---

### Kontrollpunkte

- [ ] Sie können die häufigsten Multi-Agenten-Fehler mit der Schnellreferenztabelle identifizieren und beheben
- [ ] Sie wissen, wie Sie `.env`-Konfigurationsprobleme überprüfen und beheben
- [ ] Sie können überprüfen, ob die Paketversionen mit der erforderlichen Matrix übereinstimmen
- [ ] Sie verstehen MCP-Protokolleinträge und können Werkzeugfehler diagnostizieren
- [ ] Sie wissen, wie Sie Containerprotokolle bei Bereitstellungsfehlern prüfen
- [ ] Sie können RBAC-Rollen im Azure-Portal überprüfen

---

**Vorheriger:** [07 - Verify in Playground](07-verify-in-playground.md) · **Startseite:** [Lab 02 README](../README.md) · [Workshop Startseite](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner ursprünglichen Sprache gilt als maßgebliche Quelle. Für wichtige Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Nutzung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->