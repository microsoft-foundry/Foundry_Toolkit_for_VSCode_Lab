# Modul 8 - Fehlersuche

Dieses Modul behandelt häufige Fehler, Behebungen und Debugging-Strategien, die speziell für den Multi-Agenten-Workflow gelten.

## Probleme mit Agentenausgaben

### GapAnalyzer sagt „Ich habe immer noch nicht den passenden Bericht“

**Symptom:** Die Antwort von GapAnalyzer fordert Sie auf, einen passenden Bericht mit „Fehlende Fähigkeiten“ und „Zertifizierungslücken“ einzufügen. Dies geschieht, obwohl Sie sowohl einen Lebenslauf als auch eine Stellenbeschreibung gesendet haben.

**Ursache:** Der JD-Text wurde nicht an den JD-Agenten weitergegeben. Mit `context_mode="last_agent"` sieht der `resume_executor` als einziger Executor jemals die ursprüngliche Nachricht des Benutzers. Wenn `RESUME_PARSER_INSTRUCTIONS` den JD-Text nicht in seiner Ausgabe enthält, hat der JD-Agent keine Stellenbeschreibung zum Parsen, MatchingAgent kann keine Passgenauigkeit berechnen, und GapAnalyzer erhält eine bedeutungslose Eingabe.

**Diagnose:**

Prüfen Sie in den Serverprotokollen den MatchingAgent-Span. Wenn dieser enthält:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
dann fehlt oder ist der Durchlauf unterbrochen.

**Behebung:** Stellen Sie sicher, dass `RESUME_PARSER_INSTRUCTIONS` in `main.py` einen Abschnitt `[JOB DESCRIPTION PASS-THROUGH]` und die Regel enthält:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Stellen Sie auch sicher, dass `JOB_DESCRIPTION_INSTRUCTIONS` eine Relay-Regel `[PARSED RESUME PASS-THROUGH]` enthält:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Wenn einer der Anweisungsblöcke aus dem Scaffold-Assistenten nur eine Vorlage ist, ersetzen Sie ihn durch die vollständige Version aus [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent gibt aus „Cannot compute fit score - no JD provided“

Dies ist die gleiche Grundursache wie oben. MatchingAgent erhielt die Ausgabe des JD-Agenten, aber der Abschnitt `[PARSED RESUME PASS-THROUGH]` fehlte oder war leer, sodass keine Vergleichbarkeit der Profile möglich war. Bestätigen Sie:
1. `JOB_DESCRIPTION_INSTRUCTIONS` enthält die Relay-Regel: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` weist den Agenten an, nach den Abschnitten `[JD REQUIREMENTS]` und `[PARSED RESUME PASS-THROUGH]` zu suchen.

Ersetzen Sie beide Anweisungsblöcke durch die vollständigen Versionen aus [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Die Antwort erscheint doppelt

**Symptom:** Die Ausgabe von GapAnalyzer (oder die gesamte Pipeline-Ausgabe) erscheint zweimal in der Agent Inspector-Antwort.

**Ursache:** `WorkflowBuilder` verwendet OR-Semantik für eingehende Kanten – ein nachgelagerter Executor wird ausgelöst, sobald **jemand** eines seiner Vorgänger abgeschlossen hat. Wenn `matching_executor` zwei eingehende Kanten hat (eine vom `resume_executor` und eine vom `jd_executor`), wird er zweimal ausgeführt: einmal wenn ResumeParser fertig ist und erneut wenn JD Agent fertig ist. GapAnalyzer wird dann auch zweimal ausgeführt.

**Behebung:** Stellen Sie sicher, dass der `WorkflowBuilder`-Graph eine strikt sequenzielle Pipeline ohne Zusammenführung (Fan-in) ist:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NICHT vom resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Entfernen Sie eine eventuell vorhandene `.add_edge(resume_executor, matching_executor)`-Zeile. Das Relay `[PARSED RESUME PASS-THROUGH]` in der Ausgabe des JD-Agenten gibt MatchingAgent bereits Zugriff auf den Lebenslauf.

---

## Probleme mit Umgebung und Konfiguration

### Fehlende oder falsche `.env`-Werte

Die `.env`-Datei muss im Verzeichnis `PersonalCareerCopilot/` liegen (auf derselben Ebene wie `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Erwarteter Inhalt der `.env`:

**Pfad A – Foundry Cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Pfad B – Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Beide Pfade verwenden `FOUNDRY_PROJECT_ENDPOINT`. Der Wert unterscheidet sich: Cloud verwendet einen `https://` Foundry-Endpunkt; lokal wird `http://localhost:5273/v1` verwendet. Führen Sie `foundry model list` aus, um den genauen Modellalias für Pfad B zu bestätigen.

> **So finden Sie Ihren `FOUNDRY_PROJECT_ENDPOINT`:**
- Öffnen Sie die **Foundry Toolkit**-Seitenleiste in VS Code → Rechtsklick auf Ihr Projekt → **Project Endpoint kopieren**.
- Oder öffnen Sie das [Azure-Portal](https://portal.azure.com) → Ihr Foundry-Projekt → **Übersicht** → **Project endpoint**.

> **So finden Sie Ihren `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Erweitern Sie in der Foundry Toolkit-Seitenleiste Ihr Projekt → **Models** → suchen Sie den Namen Ihres bereitgestellten Modells (z. B. `gpt-4.1-mini`).

### Priorität der Umgebungsvariablen

`main.py` verwendet `load_dotenv(override=True)`, was bedeutet:

| Priorität | Quelle | Gewinnt, wenn beide gesetzt sind? |
|----------|--------|-------------------------------|
| 1 (höchste) | `.env`-Datei | Ja |
| 2 | Shell- / Container-Umgebungsvariable | Wird verwendet, wenn derselbe Schlüssel nicht in `.env` vorhanden ist |

Bei lokaler Entwicklung ist `.env` die Wahrheitquelle (Änderungen an `.env` wirken sich sofort aus). Bei gehosteter Bereitstellung injiziert Foundry Umgebungsvariablen auf Container-Ebene; da `.env` nicht Teil des bereitgestellten Images für dieses Lab ist, werden die injizierten Containerwerte verwendet.

---

## Versionskompatibilität

### Paketversionsmatrix

Der Multi-Agenten-Workflow erfordert spezifische Paketversionen. Nicht übereinstimmende Versionen verursachen Laufzeitfehler.

| Paket | Erforderliche Version | Prüfkommando |
|-------|---------------------|-------------|
| `agent-framework-foundry` | neueste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | neueste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | neueste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Häufige Versionsfehler

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Behebung: agent-framework-foundry neu installieren
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fehlerbehebung: mcp-Paket aktualisieren
pip install mcp --upgrade
```

### Alle Versionen auf einmal überprüfen

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Erwartete Ausgabe:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Bereitstellungsprobleme

### Container startet nach Bereitstellung nicht

1. **Überprüfen Sie die Container-Protokolle:**
   - Öffnen Sie die **Foundry Toolkit**-Seitenleiste → erweitern Sie **Hosted Agents (Preview)** → klicken Sie auf Ihren Agenten → erweitern Sie die Version → **Container Details** → **Logs**.
   - Suchen Sie nach Python-Stacktraces oder fehlenden Modulfehlern.

2. **Häufige Fehler beim Containerstart:**

   | Fehler im Log | Ursache | Behebung |
   |--------------|---------|---------|
   | `ModuleNotFoundError` | `requirements.txt` fehlt ein Paket | Paket hinzufügen, erneut bereitstellen |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` oder `.env` Umgebungsvariablen sind nicht gesetzt | `agent.yaml` → `environment_variables` Abschnitt (gehostet) oder `.env` (lokal) aktualisieren |
   | `azure.identity.CredentialUnavailableError` | Managed Identity nicht konfiguriert | Foundry setzt dies automatisch – stellen Sie sicher, dass Sie über die Erweiterung bereitstellen |
   | `OSError: port 8088 already in use` | Dockerfile gibt falschen Port an oder Portkonflikt | Überprüfen Sie `EXPOSE 8088` im Dockerfile und `CMD ["python", "main.py"]` |
   | Container beendet mit Code 1 | Unbehandelte Ausnahme in `main()` | Testen Sie zuerst lokal ([Modul 5](05-test-locally.md)), um Fehler vor der Bereitstellung zu erfassen |

3. **Nach Behebung neu bereitstellen:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → wählen Sie denselben Agenten → eine neue Version bereitstellen.

### Bereitstellung dauert zu lange

Multi-Agenten-Container benötigen beim Start länger, da sie beim Start 4 Agenteninstanzen erzeugen. Übliche Startzeiten:

| Phase | Erwartete Dauer |
|-------|----------------|
| Container-Image-Build | 1-3 Minuten |
| Image-Push in ACR | 30-60 Sekunden |
| Container startet (einzelner Agent) | 15-30 Sekunden |
| Container startet (Multi-Agent) | 30-120 Sekunden |
| Agent im Playground verfügbar | 1-2 Minuten nach „Started“ |

> Wenn die Statusanzeige „Pending“ länger als 5 Minuten andauert, überprüfen Sie die Container-Logs auf Fehler.

---

## RBAC- und Berechtigungsprobleme

### `403 Forbidden` oder `AuthorizationFailed`

Sie benötigen die Rolle **[Foundry User](https://aka.ms/foundry-ext-project-role)** für Ihr Foundry-Projekt (früher „Azure AI User“ genannt – Rollen-ID unverändert):

1. Gehen Sie zu [Azure Portal](https://portal.azure.com) → Ressource Ihres Foundry-**Projekts**.
2. Klicken Sie auf **Zugriffskontrolle (IAM)** → **Rollen-Zuweisungen**.
3. Suchen Sie nach Ihrem Namen → bestätigen Sie, dass **Foundry User** (oder die alte Bezeichnung **Azure AI User**) aufgeführt ist.
4. Falls nicht vorhanden: **Hinzufügen** → **Rollen-Zuweisung hinzufügen** → suchen Sie **Foundry User** → Ihrer Benutzerkontozuweisen.

Details finden Sie in der Dokumentation zu [RBAC für Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Modellbereitstellung nicht erreichbar

Wenn der Agent modellbezogene Fehler zurückgibt:

1. Vergewissern Sie sich, dass das Modell bereitgestellt ist: Foundry-Seitenleiste → Projekt erweitern → **Models** → prüfen Sie, ob `gpt-4.1-mini` (oder Ihr Modell) mit Status **Succeeded** angezeigt wird.
2. Prüfen Sie, ob der Bereitstellungsname übereinstimmt: vergleichen Sie `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` (oder `agent.yaml`) mit dem tatsächlichen Bereitstellungsnamen in der Seitenleiste.
3. Wenn die Bereitstellung abgelaufen ist (kostenlose Stufe): Stellen Sie neu bereit aus dem [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local-Probleme (Pfad B)

### Foundry Local-Dienst läuft nicht

```powershell
# Status prüfen
foundry local status

# Dienst starten, falls er gestoppt ist
foundry local start
```

| Symptom | Ursache | Behebung |
|---------|---------|---------|
| Health Check gibt `503` zurück | Dienst nicht gestartet | `foundry local start` oder klicken Sie auf **Start** in der Foundry Toolkit-Seitenleiste |
| Health Check läuft ins Timeout | Modell wird noch geladen | 30–60 Sekunden nach Start warten; größere Modelle benötigen mehr Zeit |
| `StatusCode: 404` auf `/v1/health` | Falscher Port | Standard ist `5273`. Prüfen Sie mit `foundry local status` den tatsächlichen Port |
| Ungenügende Ressourcen | Foundry Local benötigt ca. 4 GB freien RAM | Schließen Sie andere Anwendungen |
| Modell-Download schlägt fehl | Wenig Speicherplatz | Modelle sind 2–8 GB groß. Platz schaffen, dann `foundry model pull <name>` ausführen |

### Modellname stimmt nicht überein

```powershell
# Liste heruntergeladener Modelle und ihrer genauen Aliase
foundry model list
```

Setzen Sie `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` auf den exakt angezeigten Alias (z. B. `phi-4-mini`, nicht `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` bei lokalem Lauf (Pfad B)

Das Lab `main.py` verwendet `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local erfordert, dass diese Variable auf den lokalen Dienst zeigt – **nicht** auf `AZURE_AI_PROJECT_ENDPOINT`. Stellen Sie sicher, dass Ihre `.env` enthält:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-Tool macht dennoch einen ausgehenden Aufruf (Pfad B)

Dies ist erwartet. Das Tool `search_microsoft_learn_for_plan` ruft Lernressourcen von `https://learn.microsoft.com/api/mcp` ab. **Nur die Abfrage nach dem Fähigkeitsnamen** wird über das Netzwerk gesendet – Lebenslauf und JD-Text werden vollständig auf Ihrem Gerät verarbeitet und nicht übertragen. Falls ein vollständig offline Betrieb erforderlich ist, fügen Sie im Tool ein `try/except`-Fallback hinzu, das eine statische URL von `learn.microsoft.com` zurückgibt, sofern der Endpunkt nicht erreichbar ist.

---

## Hilfe erhalten

Wenn Sie nach Anwendung der oben genannten Behebungen feststecken:

1. **Überprüfen Sie die Server-Protokolle** – Die meisten Fehler erzeugen einen Python-Stacktrace im Terminal. Lesen Sie die gesamte Rückverfolgung.
2. **Suchen Sie nach der Fehlermeldung** – Kopieren Sie den Fehlertext und suchen Sie in [Microsoft Q&A für Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Öffnen Sie ein Issue** – Legen Sie ein Issue im [Workshop-Repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) an mit:
   - Der Fehlermeldung oder einem Screenshot
   - Ihren Paketversionen (`pip list | Select-String "agent-framework"`)
   - Ihrer Python-Version (`python --version`)
   - Ob das Problem lokal oder nach der Bereitstellung auftritt

---

### Kontrollpunkt

- [ ] Sie wissen, wie man `.env`-Konfigurationsprobleme überprüft und behebt
- [ ] Sie können Paketversionen gemäß der erforderlichen Matrix verifizieren
- [ ] Sie wissen, wie man Container-Logs auf Bereitstellungsfehler überprüft
- [ ] Sie können RBAC-Rollen im Azure Portal verifizieren

---

**Vorheriges:** [07 - Überprüfung im Playground](07-verify-in-playground.md) · **Nächstes:** [09 - Zusammenfassung →](09-summary.md) · **Startseite:** [Lab 02 README](../README.md) · [Workshop Startseite](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->