# Wie Sie diese Sitzung durchführen

Vielen Dank, dass Sie diese Sitzung durchführen!

Bitte beachten Sie vor der Durchführung des Workshops:

1. Lesen Sie dieses Dokument und alle enthaltenen Ressourcen vollständig durch.
2. Sehen Sie sich die Aufzeichnung der Sitzung und den Workshop-Durchgang von Anfang bis Ende an.
3. Durchlaufen Sie beide praktischen Übungen **mindestens einmal** vollständig auf Ihrem eigenen Computer vor der Veranstaltung.
4. Validieren Sie Ihr Microsoft Foundry-Projekt, Modellbereitstellungen und Kontingente.
5. Wenden Sie sich an den Betreuer, falls etwas unklar ist.

---

## Dateizusammenfassung

| Ressource                    | Link                                                                             | Beschreibung                                                                              |
|-----------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Workshop-Folien              | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                         | Präsentationsfolien für diesen Workshop mit Moderationsnotizen und eingebetteten Demovideos|
| Aufzeichnung der Sitzung     | _Wird vom Betreuer bereitgestellt_                                              | Einführung in den Workshop und Durchgang der Folien als Aufzeichnung                       |
| End-to-End-Aufzeichnung      | _Wird vom Betreuer bereitgestellt_                                              | Komplette Aufzeichnung beider Übungen aus der Sicht eines Lernenden                        |
| Workshop-Dokumentation       | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                                            | Quell-Repository, Lab-READMEs, Schritt-für-Schritt-Module                                 |
| Lab 01 - Einzelagent         | [Lab 01](../workshop/lab01-single-agent/README.md)                                                | Praktische Übung: Erstellen, Testen und Bereitstellen des *Explain Like I'm an Executive*-Hosted Agent |
| Lab 02 - Multi-Agent Workflow| [Lab 02](../workshop/lab02-multi-agent/README.md)                                                | Praktische Übung: Erstellen des 4-Agenten *Resume to Job Fit Evaluator*-Workflows          |
| Demo 1: Executive Agent      | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                          | Demo zu Lab 01: Technischen Jargon in eine Management-Zusammenfassung übersetzen          |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                              | Demo zu Lab 02: 4-Agenten-Workflow, der Bewerbungs-Job-Passung bewertet und Empfehlungen generiert |

> **Hinweis für Trainer:** Folien und Videolinks werden hinzugefügt, sobald die Aufzeichnungen veröffentlicht sind. Bis dahin kontaktieren Sie den Betreuer (siehe [Kontakte](#contacts)) für die aktuellsten Materialien.

---

## Einstieg

Dieser Workshop zeigt Entwicklern, wie sie KI-Agenten mithilfe der **Microsoft Foundry Toolkit**-Erweiterung vollständig in VS Code erstellen, testen und als **Hosted Agents** im **Microsoft Foundry Agent Service** bereitstellen können.

Der Workshop ist in mehrere Abschnitte unterteilt, darunter Folien, **2 Live-Demos** und **2 praktische Übungen**.

### Zeitplan

#### Komplettdurchführung (ca. 2 Stunden)

| Zeit            | Beschreibung                                                        |
|-----------------|-------------------------------------------------------------------|
| 0:00 - 10:00    | Einführung: Hosted Agents, Foundry Agent Service und Toolkit       |
| 10:00 - 20:00   | Demo: Executive Agent End-to-End                                  |
| 20:00 - 60:00   | Lab 01 - Einzelagent (bauen, lokal testen, bereitstellen, Playground) |
| 60:00 - 110:00  | Lab 02 - Multi-Agent Workflow (Resume to Job Fit Evaluator)       |
| 110:00 - 120:00 | Abschluss, Fragen & Antworten sowie weiterführende Lernressourcen |

#### Kurzform (ca. 75 Minuten)

| Zeit          | Beschreibung                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Einführung und Überblick                                     |
| 10:00 - 20:00 | Demo: Executive Agent                                       |
| 20:00 - 70:00 | Nur Lab 01 (Teilnehmer auf Lab 02 als Selbstlerneinheit verweisen) |
| 70:00 - 75:00 | Abschluss und Fragen & Antworten                             |

### Vorbereitung

| Ressource                     | Link                                                                                          | Beschreibung                                   |
|------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------|
| Workshop-Dokumentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                                                          | Workshop-Dokumentation und Quellcode            |
| Lab 01-Anleitungen            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                                  | Praktische Übung: Einzelner gehosteter Agent    |
| Lab 02-Anleitungen            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                                  | Praktische Übung: Multi-Agent-Workflow           |
| Checkliste der Voraussetzungen | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                                              | Benötigte Tools, Konten und Azure-Zugriff       |
| Schnellstart Hosted Agents (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)                                                             | Offizieller Schnellstart zur Bereitstellung eines Hosted Agents mit `azd` |
| Verfügbare Regionen für Hosted Agents | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)                                                           | Unterstützte Regionen für Hosted Agents (Vorschau) |

### Voraussetzungen für Trainer

Stellen Sie vor der Durchführung sicher, dass Sie Folgendes haben:

- Ein **Azure-Abonnement** mit Berechtigung zum Erstellen von Ressourcen (Owner oder Contributor für eine Ressourcengruppe).
- Zugriff auf ein **Microsoft Foundry Projekt** in einer [Region, die Hosted Agents unterstützt](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kontingent für **gpt-4.1** (oder **gpt-4.1-mini**) in Ihrem Foundry-Projekt.
- Die folgenden Tools installiert:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit-Erweiterung](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Optional)
  - Python 3.12 oder neuer

Führen Sie vor der Durchführung mindestens einmal den [Schnellstart Hosted Agents mit `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) durch, damit Sie ein bekannt funktionierendes Foundry-Projekt, eine Modellbereitstellung und ein Azure Container Registry zur Hand haben, falls ein Lernender nicht weiterkommt.

---

## Durchgang durch die Folien

Der Foliensatz folgt dem gleichen Ablauf wie die Übungen. Vorgeschlagene Gesprächspunkte für jeden Abschnitt:

| Abschnitt                    | Kernbotschaft                                                                                            |
|-----------------------------|----------------------------------------------------------------------------------------------------------|
| Titel und Agenda             | Stellen Sie den Workshop als *VS Code zu Foundry* dar, ohne Portalwechsel.                              |
| Warum Hosted Agents?         | Verwaltete Laufzeit, ACR-basierte Bereitstellung, OpenAI-kompatible `/responses`-API, auf Foundry-Projekte beschränkt. |
| Architekturdiagramm         | Gehen Sie das [README Architektur](../README.md#architecture) durch: Scaffold, Inspector, ACR, Agent Service. |
| Anatomie eines Hosted Agents | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - was jede Datei macht.                          |
| Live-Demo: Executive Agent  | Wechseln Sie zu VS Code und führen Sie die [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) Demo durch (siehe [Demo 1](#demo-1-executive-agent)). |
| Live-Demo: Resume to Job Fit Evaluator | Wechseln Sie zu VS Code und führen Sie die [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-Agenten-Demo aus (siehe [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 Kurzvorstellung      | Übergabe an die Lernenden. Verweisen Sie auf [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md).               |
| Multi-Agent Muster          | Sequenziell vs parallel vs Übergabe - Vorschau vor Beginn von Lab 02.                                  |
| Lab 02 Kurzvorstellung      | Übergabe an die Lernenden. Verweisen Sie auf [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md).               |
| Abschluss und Ressourcen    | Weiterführende Lernlinks aus dem Abschnitt [Zusätzliche Ressourcen](#additional-resources).            |

---

## Demos

In der Durchführung sind zwei Live-Demos enthalten. Planen Sie jeweils 10 Minuten ein.

| Demo                     | Lab  | Dateien                              | Was zu zeigen ist                                     |
|--------------------------|------|-----------------------------------|------------------------------------------------------|
| Executive Agent          | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Einzelner Hosted Agent; technischen Jargon in einen Executive Summary übersetzen |
| Resume to Job Fit Evaluator | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-Agenten-Orchestrierung; Bewerbungs-Job-Passung bewerten und Empfehlung generieren |

### Demo 1: Executive Agent

Ein eigenständiger Agent in [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Nutzen Sie dies als 10-Minuten-Demo vor Lab 01.

1. Öffnen Sie [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) und gehen Sie die Agent-Definition durch (Systemprompt, Modell, Framework).
2. Drücken Sie `F5`, um den **Agent Inspector** lokal zu starten.
3. Fügen Sie den Beispiels-Prompt aus dem [README](../README.md#see-it-in-action) ein und zeigen Sie die Antwort des Executive Summaries.
4. Zeigen Sie [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) und [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile), um die Bereitstellungsartefakte zu erläutern.
5. Demonstrieren Sie den Bereitstellungsablauf (Docker-Build, ACR-Push, Erstellung des Hosted Agents), ohne auf die Fertigstellung zu warten.

### Demo 2: Resume to Job Fit Evaluator

Ein 4-Agenten-Workflow in [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Nutzen Sie dies als 10-Minuten-Demo vor Lab 02.

1. Öffnen Sie [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) und zeigen Sie, wie die vier Agenten in einer sequentiellen Orchestrierung verbunden sind.
2. Drücken Sie `F5`, um den **Agent Inspector** für den Multi-Agent-Workflow zu starten.
3. Fügen Sie eine kurze Stellenbeschreibung und einen Beispiellebenslauf in den Inspector-Chat ein.
4. Gehen Sie die vier Agenten-Pipeline durch: Lebenslauf-Parser, Job-Anforderungsextraktor, Passungsbewertung und Empfehlungsschreiber.
5. Weisen Sie darauf hin, wie die Ausgabe jedes Unteragenten zum Kontext des nächsten Agenten wird und heben Sie das Übergabemuster hervor.
6. Zeigen Sie [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml), um es mit dem Einzelagenten-Äquivalent aus Demo 1 zu vergleichen.

---

## Tipps zur Durchführung

- **Erwarten Sie Erwartungen frühzeitig.** Hosted Agents sind in der Vorschau – weisen Sie upfront auf Regionsbeschränkungen und Kontingente hin, damit Teilnehmer nicht mitten im Lab überrascht werden.
- **Führen Sie zuerst die Voraussetzungen-Aufgabe aus.** Beide Labs liefern eine `Validate prerequisites` VS Code-Task – lassen Sie die Teilnehmer diese vor dem Schreiben von Code ausführen.
- **Halten Sie den Agent Inspector sichtbar.** Die meisten "Aha"-Momente treten auf, wenn Lernende die lokale `/responses`-Hin- und Rückreise aufleuchten sehen.
- **Halten Sie ein Backup-Projekt bereit.** Falls das Foundry-Projekt eines Lernenden ein Kontingentlimit erreicht, teilen Sie ein vorab bereitgestelltes Projekt für den Bereitstellungsschritt, statt den Raum zu blockieren.
- **Paaren Sie die Teilnehmer.** Lab 02 (Multi-Agent) ist deutlich leichter, wenn Lernende das Orchestrieren mit einem Partner besprechen können.
- **Nutzen Sie die Dok-Module als Checkpoints.** Jeder `docs/`-Ordner eines Labs ist in nummerierte Module unterteilt – verwenden Sie diese als natürliche Pausenpunkte.
- **Laden Sie das Basis-Docker-Image vor** auf gemeinsam genutzten Lab-Maschinen, um Registry-Rate-Limits zu vermeiden.

---

## Fehlerbehebung während der Durchführung

| Symptom                                    | Erstes zu versuchendes Vorgehen                                                           |
|--------------------------------------------|--------------------------------------------------------------------------------------------|
| Agent Inspector kann keine Verbindung herstellen | Prüfen Sie, ob Port `8088` frei ist und die `Run Agent HTTP Server` Task ausgeführt wird. |
| Debugger kann nicht anhängen               | Prüfen Sie, ob Port `5679` frei ist; starten Sie VS Code neu, falls `debugpy` bereits belegt ist. |
| `azd up` schlägt mit Authentifizierungsfehler fehl | Führen Sie `az login` und `azd auth login` aus, und stellen Sie sicher, dass der richtige Mandant ausgewählt ist. |
| Bereitstellung hängt beim ACR-Push          | Stellen Sie sicher, dass Docker Desktop läuft und der Benutzer `AcrPush` auf das Registry hat. |
| Modell gibt 404 / Deployment nicht gefunden zurück | Der Name der Modellbereitstellung in `agent.yaml` muss mit der Bereitstellung im Foundry-Projekt übereinstimmen. |
| Gehosteter Agent hängt bei `Provisioning`          | Überprüfen Sie, ob die Projektregion [gehostete Agents unterstützt](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) und ob Kontingent verfügbar ist. |
| Playground gibt 401 zurück                    | Authentifizieren Sie die Foundry-Erweiterung erneut über die Aktivitätsleiste in VS Code.                     |

Für tiefere Anleitungen hat jedes Labor sein eigenes `08-troubleshooting.md`-Dokument – verlinken Sie Lernende dorthin:

- Labor 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Labor 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Anpassung dieser Sitzung

Sie können den Workshop gerne an Ihr Publikum anpassen. Übliche Varianten:

- **Backend-Publikum:** mehr Zeit für `agent.yaml`, Docker und ACR einplanen; die Playground-Demo kürzen.
- **Citizen-Developer-Publikum:** in der Foundry-Erweiterungs-Benutzeroberfläche für das Gerüstblech bleiben; CLI-Schritte reduzieren.
- **Einzelner 60-Minuten-Slot:** nur Einleitung, Demo und Labor 01 durchführen.
- **Nur Workshop-Format (keine Folien):** Öffnen Sie beide Lab-READMEs und verwenden Sie diese als primäres Skript.

Wenn Sie die Labs erweitern, tragen Sie bitte die Änderungen über einen PR zurück bei, damit andere Trainer davon profitieren.

---

## Zusätzliche Ressourcen

- [Microsoft Foundry Dokumentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Übersicht gehosteter Agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Schnellstart: Stellen Sie Ihren ersten gehosteten Agenten bereit (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Einen gehosteten Agenten bereitstellen (How-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry Toolkit für VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakte

Wenn Sie Fragen zur Durchführung dieser Sitzung haben, öffnen Sie bitte ein Issue im [Workshop-Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) und markieren Sie den Maintainer.

| Rolle               | Name           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Maintainer / Kontakt | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->