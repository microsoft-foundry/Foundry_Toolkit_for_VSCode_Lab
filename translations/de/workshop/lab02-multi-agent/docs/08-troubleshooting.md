# Modul 8 - Fehlerbehebung

Dieses Modul behandelt häufige Fehler, Behebungen und Debugging-Strategien speziell für den Multi-Agenten-Workflow.

## Probleme mit Agentenausgaben

### GapAnalyzer sagt „Ich habe den Matching-Bericht immer noch nicht“

**Symptom:** Die Antwort von GapAnalyzer fordert Sie auf, einen Matching-Bericht mit „Fehlenden Fähigkeiten“ und „Zertifizierungslücken“ einzufügen. Dies passiert, obwohl Sie sowohl einen Lebenslauf als auch eine Stellenbeschreibung gesendet haben.

**Ursache:** Der JD-Text wurde nicht an den JD Agent weitergeleitet. Mit `context_mode="last_agent"` sieht nur `resume_executor` als einziger Executor die ursprüngliche Nutzeranfrage. Wenn `RESUME_PARSER_INSTRUCTIONS` den JD-Text nicht in seiner Ausgabe einschließt, hat der JD Agent keine JD zu parsen, MatchingAgent kann keinen Fit-Score berechnen und GapAnalyzer erhält eine bedeutungslose Eingabe.

**Diagnose:**

Suchen Sie in den Serverprotokollen nach dem MatchingAgent-Span. Wenn dieser Folgendes enthält:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
geht der Durchleitungsprozess verloren oder ist defekt.

**Behebung:** Bestätigen Sie, dass `RESUME_PARSER_INSTRUCTIONS` in `main.py` einen `[JOB DESCRIPTION PASS-THROUGH]`-Abschnitt und die Regel enthält:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Bestätigen Sie auch, dass `JOB_DESCRIPTION_INSTRUCTIONS` eine `[PARSED RESUME PASS-THROUGH]`-Relaisregel hat:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Falls einer der Anweisungsabschnitte eine Platzhalter-Version aus dem Scaffold-Assistenten ist, ersetzen Sie diesen durch die vollständige Version von [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent gibt „Cannot compute fit score - no JD provided“ aus

Dies ist dieselbe Ursache wie oben. MatchingAgent hat die Ausgabe des JD Agent erhalten, aber der `[PARSED RESUME PASS-THROUGH]`-Abschnitt war fehlend oder leer, daher konnte er die beiden Profile nicht vergleichen. Bestätigen Sie:
1. `JOB_DESCRIPTION_INSTRUCTIONS` enthält die Relaisregel: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` weist den Agenten an, nach `[JD REQUIREMENTS]` und `[PARSED RESUME PASS-THROUGH]` Abschnitten zu suchen.

Ersetzen Sie beide Anweisungsabschnitte durch die vollständigen Versionen von [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Die Antwort erscheint zweimal

**Symptom:** Die Ausgabe von GapAnalyzer (oder die gesamte Pipeline-Ausgabe) erscheint doppelt in der Antwort des Agent Inspector.

**Ursache:** `WorkflowBuilder` verwendet OR-Semantik für eingehende Kanten – ein nachgelagerter Executor wird ausgelöst, sobald **irgendein** Vorgänger abgeschlossen ist. Wenn `matching_executor` zwei eingehende Kanten hat (eine von `resume_executor` und eine von `jd_executor`), wird er zweimal ausgelöst: einmal wenn ResumeParser fertig ist und erneut, wenn JD Agent fertig ist. GapAnalyzer läuft dann ebenfalls zweimal.

**Behebung:** Stellen Sie sicher, dass der `WorkflowBuilder`-Graph eine strikt sequenzielle Pipeline ohne Fan-in ist:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Wenn Sie eine einzelne `.add_edge(resume_executor, matching_executor)`-Zeile finden, entfernen Sie diese. Das `[PARSED RESUME PASS-THROUGH]`-Relais in der JD Agent-Ausgabe gibt MatchingAgent bereits Zugriff auf den Lebenslauf.

---

## Umgebung und Konfigurationsprobleme

### Fehlende oder falsche `.env` Werte

Die `.env`-Datei muss im `PersonalCareerCopilot/`-Verzeichnis liegen (gleiche Ebene wie `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Erwarteter Inhalt von `.env`:

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

> Beide Pfade verwenden `FOUNDRY_PROJECT_ENDPOINT`. Der Wert ist unterschiedlich: Cloud verwendet einen `https://` Foundry-Endpunkt; lokal wird `http://localhost:5273/v1` verwendet. Führen Sie `foundry model list` aus, um den genauen Modell-Alias für Pfad B zu bestätigen.

> **So finden Sie Ihren `FOUNDRY_PROJECT_ENDPOINT`:** 
- Öffnen Sie die **Foundry Toolkit**-Seitenleiste in VS Code → Rechtsklick auf Ihr Projekt → **Projekt-Endpunkt kopieren**. 
- Oder gehen Sie zum [Azure Portal](https://portal.azure.com) → Ihr Foundry-Projekt → **Übersicht** → **Projekt-Endpunkt**.

> **So finden Sie Ihren `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Erweitern Sie in der Foundry Toolkit-Seitenleiste Ihr Projekt → **Modelle** → suchen Sie Ihren bereitgestellten Modellnamen (z. B. `gpt-4.1-mini`).

### Priorität von Umgebungsvariablen

`main.py` verwendet `load_dotenv(override=True)`, was bedeutet:

| Priorität | Quelle | Hat Vorrang, wenn beide gesetzt sind? |
|----------|--------|-------------------------------|
| 1 (höchste) | `.env`-Datei | Ja |
| 2 | Shell- / Container-Umgebungsvariable | Wird verwendet, wenn derselbe Schlüssel nicht in `.env` vorhanden ist |

In der lokalen Entwicklung ist `.env` die Quelle der Wahrheit (Änderung in `.env` wirkt sich sofort auf Laufzeiten aus). In der gehosteten Bereitstellung injiziert Foundry Umgebungsvariablen auf Container-Ebene; da `.env` nicht Teil des bereitgestellten Images in diesem Lab-Setup ist, werden die injizierten Containerwerte verwendet.

---

## Versionskompatibilität

### Paket-Versionsmatrix

Der Multi-Agenten-Workflow erfordert spezifische Paketversionen. Versionen, die nicht zueinander passen, verursachen Laufzeitfehler.

| Paket | Erforderliche Version | Prüf-Befehl |
|---------|--------------------|-------------|
| `agent-framework-foundry` | neueste | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | neueste | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | neueste | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Häufige Versionsfehler

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

### Alle Versionen auf einmal prüfen

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

1. **Container-Protokolle prüfen:**
   - Öffnen Sie die **Foundry Toolkit**-Seitenleiste → unter Ihrem Projekt klicken Sie auf **Agents** → Tab **Hosted Agent** → klicken Sie Ihren Agenten an. Prüfen Sie den **Status** auf dem Tab **Details**, öffnen Sie dann den **Playground** Tab und nutzen Sie den **Logs** Tab im **Session Details**-Panel, um die Container-Ausgabe zu sehen.
   - Suchen Sie nach Python-Stack-Traces oder Fehlern zu fehlenden Modulen.

2. **Häufige Ursachen für Container-Startfehler:**

   | Fehler in Protokollen | Ursache | Behebung |
   |----------------------|---------|----------|
   | `ModuleNotFoundError` | `requirements.txt` fehlt ein Paket | Paket hinzufügen, neu bereitstellen |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` oder `.env`-Umgebungsvariablen nicht gesetzt | Aktualisieren Sie `agent.yaml` → `environment_variables` Abschnitt (gehostet) oder `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity nicht konfiguriert | Foundry setzt das automatisch - stellen Sie sicher, dass Sie über die Extension bereitstellen |
   | `OSError: port 8088 already in use` | Dockerfile gibt falschen Port frei oder Portkonflikt | Prüfen Sie `EXPOSE 8088` im Dockerfile und `CMD ["python", "main.py"]` |
   | Container beendet mit Code 1 | Unbehandelter Fehler in `main()` | Testen Sie vorher lokal ([Modul 5](05-test-locally.md)), um Fehler vor der Bereitstellung zu erkennen |

3. **Nach Behebung erneut bereitstellen:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Hosted Agent bereitstellen** → denselben Agent auswählen → neue Version bereitstellen.

### Bereitstellung dauert zu lange

Multi-Agenten-Container brauchen beim Start länger, weil sie beim Start 4 Agent-Instanzen erzeugen. Normale Startzeiten:

| Schritt | Erwartete Dauer |
|--------|-----------------|
| Container-Image-Erstellung | 1-3 Minuten |
| Image-Push zu ACR | 30-60 Sekunden |
| Container-Start (einzelner Agent) | 15-30 Sekunden |
| Container-Start (Multi-Agent) | 30-120 Sekunden |
| Agent im Playground verfügbar | 1-2 Minuten nach „Gestartet“ |

> Wenn der Status „Ausstehend“ länger als 5 Minuten anhält, prüfen Sie Container-Protokolle auf Fehler.

---

## RBAC- und Berechtigungsprobleme

### `403 Forbidden` oder `AuthorizationFailed`

Sie benötigen die Rolle **[Foundry User](https://aka.ms/foundry-ext-project-role)** in Ihrem Foundry-Projekt (früher **Azure AI User** genannt – Rollen-ID unverändert):

1. Gehen Sie zum [Azure Portal](https://portal.azure.com) → Ihrer Foundry-**Projekt**-Ressource.
2. Klicken Sie auf **Zugriffskontrolle (IAM)** → **Rollenzuweisungen**.
3. Suchen Sie nach Ihrem Namen → bestätigen Sie, dass **Foundry User** (oder die alte Bezeichnung **Azure AI User**) aufgelistet ist.
4. Wenn fehlen: **Hinzufügen** → **Rollenzuweisung hinzufügen** → nach **Foundry User** suchen → Ihrem Konto zuweisen.

Details finden Sie in der Dokumentation zu [RBAC für Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Modellbereitstellung nicht zugänglich

Wenn der Agent modellbezogene Fehler zurückgibt:

1. Vergewissern Sie sich, dass das Modell bereitgestellt ist: Foundry-Seitenleiste → Projekt erweitern → **Models** → suchen Sie nach `gpt-4.1-mini` (oder Ihrem Modell) mit Status **Succeeded**.
2. Prüfen Sie, ob der Bereitstellungsname übereinstimmt: vergleichen Sie `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` (oder `agent.yaml`) mit dem tatsächlichen Bereitstellungsnamen in der Seitenleiste.
3. Falls die Bereitstellung abgelaufen ist (kostenfreie Stufe): erneut bereitstellen aus dem [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Modulkatalog öffnen**).

---

## Probleme mit Foundry Local (Pfad B)

### Foundry Local Dienst läuft nicht

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Symptom | Ursache | Behebung |
|---------|---------|----------|
| Gesundheitscheck gibt `503` zurück | Dienst nicht gestartet | `foundry local start` oder klicken Sie auf **Start** in der Foundry Toolkit-Seitenleiste |
| Gesundheitscheck läuft ins Timeout | Modell wird noch geladen | Warten Sie 30–60 s nach Start, größere Modelle brauchen länger |
| `StatusCode: 404` auf `/v1/health` | Falscher Port | Standard ist `5273`. Prüfen Sie `foundry local status` für den aktuellen Port |
| Nicht genügend Ressourcen | Foundry Local braucht ca. 4 GB freien RAM | Schließen Sie andere Anwendungen |
| Modellspeicherung schlägt fehl | Wenig Speicherplatz | Modelle sind 2–8 GB groß. Platz freimachen, dann `foundry model pull <name>` |

### Modellnamensabweichung

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Setzen Sie `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `.env` genau auf den Alias, der angezeigt wird (z. B. `phi-4-mini`, nicht `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` bei lokalem Lauf (Pfad B)

Das Lab-`main.py` verwendet `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local verlangt, dass diese Variable auf den lokalen Dienst zeigt – **nicht** auf `AZURE_AI_PROJECT_ENDPOINT`. Stellen Sie sicher, dass Ihre `.env` Folgendes enthält:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-Tool führt trotzdem ausgehenden Aufruf durch (Pfad B)

Das ist erwartungsgemäß. Das `search_microsoft_learn_for_plan`-Tool lädt Lernressourcen von `https://learn.microsoft.com/api/mcp`. **Nur die Abfrage nach dem Fertigkeitsnamen** wird über das Netzwerk gesendet – Lebenslauf- und JD-Text werden vollständig auf Ihrem Gerät verarbeitet und nie übertragen. Wenn ein vollständig offline Betrieb gewünscht ist, fügen Sie im Tool einen `try/except`-Fallback hinzu, der eine statische `learn.microsoft.com` URL zurückgibt, wenn der Endpunkt nicht erreichbar ist.

---

## Hilfe erhalten

Wenn Sie nach den obigen Behebungen nicht weiterkommen:

1. **Prüfen Sie die Server-Protokolle** – Die meisten Fehler erzeugen einen Python-Stack-Trace im Terminal. Lesen Sie die vollständige Rückverfolgung.
2. **Suchen Sie die Fehlermeldung** – Kopieren Sie den Fehlertext und suchen Sie im [Microsoft Q&A für Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Eröffnen Sie ein Issue** – Melden Sie ein Problem im [Workshop-Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) mit:
   - Der Fehlermeldung oder einem Screenshot
   - Ihren Paketversionen (`pip list | Select-String "agent-framework"`)
   - Ihrer Python-Version (`python --version`)
   - Ob das Problem lokal oder nach der Bereitstellung auftrat

---

### Checkpoint

- [ ] Sie wissen, wie man `.env` Konfigurationsprobleme überprüft und behebt
- [ ] Sie können Paketversionen verifizieren, dass sie der erforderlichen Matrix entsprechen
- [ ] Sie wissen, wie man Container-Protokolle auf Bereitstellungsfehler prüft
- [ ] Sie können RBAC-Rollen im Azure Portal überprüfen

---

**Vorheriges:** [07 - Überprüfung im Playground](07-verify-in-playground.md) · **Nächstes:** [09 - Zusammenfassung →](09-summary.md) · **Startseite:** [Lab 02 README](../README.md) · [Workshop Startseite](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->