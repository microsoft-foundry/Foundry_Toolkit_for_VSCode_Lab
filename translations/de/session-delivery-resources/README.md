# Wie diese Sitzung durchgeführt wird

Danke, dass Sie diese Sitzung durchführen!

Vor der Durchführung des Workshops bitte:

1. Lesen Sie dieses Dokument und alle enthaltenen Ressourcen vollständig durch.
2. Sehen Sie sich die Aufnahme der Sitzungsdurchführung und den Workshop-End-to-End-Durchlauf an.
3. Durchlaufen Sie beide Hands-on-Labs auf Ihrer eigenen Maschine **mindestens einmal** vor der Veranstaltung komplett.
4. Überprüfen Sie Ihr Microsoft Foundry-Projekt, Modellbereitstellungen und Kontingente.
5. Kontaktieren Sie den Verantwortlichen, falls etwas unklar ist.

---

## Dateiübersicht

| Ressource                    | Link                                                                             | Beschreibung                                                                                 |
|-----------------------------|----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Workshop-Foliensatz          | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                    | Präsentationsfolien für diesen Workshop mit Sprecher-Notizen und eingebetteten Demo-Videos  |
| Aufnahme der Sitzungsdurchführung | _Wird vom Verantwortlichen bereitgestellt_                                   | Aufnahme der Workshop-Einführung und Durchlauf der Folien                                 |
| Aufnahme des vollständigen Workshops | _Wird vom Verantwortlichen bereitgestellt_                                   | End-to-End-Aufnahme beider Labs aus Sicht eines Lernenden                                 |
| Workshop-Dokumentation      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Quell-Repository, Lab-READMEs, Schritt-für-Schritt-Module                                 |
| Lab 01 - einzelner Agent     | [Lab 01](../workshop/lab01-single-agent/README.md)                             | Hands-on-Lab: Erstellen, Testen und Bereitstellen des *Explain Like I'm an Executive*-Agents|
| Lab 02 - Multi-Agent-Workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                            | Hands-on-Lab: Erstellen des 4-Agenten *Resume to Job Fit Evaluator* Workflows              |
| Demo 1: Executive Agent      | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                           | Lab 01 Demo: Übersetzung technischer Fachbegriffe in eine Executive-Zusammenfassung        |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Lab 02 Demo: 4-Agenten-Workflow, der Lebenslauf-Job-Passung bewertet und Empfehlungen generiert |

> **Hinweis für Trainer:** Foliensatz- und Videolinks werden hinzugefügt, sobald die Aufnahmen veröffentlicht sind. Bis dahin kontaktieren Sie den Verantwortlichen (siehe [Kontakte](#kontakte)) für die neuesten Materialien.

---

## Einstieg

Dieser Workshop lehrt Entwickler:innen, wie man KI-Agenten vollständig über VS Code mit Hilfe der Erweiterung **Microsoft Foundry Toolkit** baut, testet und als **Hosted Agents** im **Microsoft Foundry Agent Service** bereitstellt.

Der Workshop ist in mehrere Abschnitte unterteilt, darunter Folien, **2 Live-Demos** und **2 Hands-on-Labs**.

### Zeitplan

#### Vollständige Durchführung (ca. 2 Stunden)

| Zeit            | Beschreibung                                                      |
|-----------------|------------------------------------------------------------------|
| 0:00 - 10:00    | Einführung: Hosted Agents, Foundry Agent Service und Toolkit      |
| 10:00 - 20:00   | Demo: Executive Agent End-to-End                                 |
| 20:00 - 60:00   | Lab 01 - einzelner Agent (bauen, lokal testen, bereitstellen, Playground) |
| 60:00 - 110:00  | Lab 02 - Multi-Agent-Workflow (Resume to Job Fit Evaluator)      |
| 110:00 - 120:00 | Abschluss, Fragen & Antworten, Ressourcen zum Weiterlernen        |

#### Verkürzte Durchführung (ca. 75 Minuten)

| Zeit          | Beschreibung                                              |
|---------------|----------------------------------------------------------|
| 0:00 - 10:00  | Einführung und Überblick                                 |
| 10:00 - 20:00 | Demo: Executive Agent                                    |
| 20:00 - 70:00 | Nur Lab 01 (Weisen Sie die Teilnehmenden auf Lab 02 als Selbstlernangebot hin) |
| 70:00 - 75:00 | Abschluss und Fragen & Antworten                          |

### Vorbereitung

| Ressource                     | Link                                                                                      | Beschreibung                                     |
|------------------------------|-------------------------------------------------------------------------------------------|-------------------------------------------------|
| Workshop-Dokumentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)         | Workshop-Dokumentation und Quellcode              |
| Lab 01 Anleitungen            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                            | Hands-on-Lab: Einzelner gehosteter Agent         |
| Lab 02 Anleitungen            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                              | Hands-on-Lab: Multi-Agent-Workflow                |
| Checkliste Voraussetzungen    | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)            | Benötigte Tools, Konten und Azure-Zugriff         |
| Hosted Agents Schnellstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Offizielles Schnellstart-Tutorial zum Bereitstellen eines Hosted Agents mit `azd` |
| Hosted Agents Verfügbarkeiten | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Unterstützte Regionen für Hosted Agents (Vorschau)|

### Voraussetzungen für Trainer:innen

Bevor Sie starten, stellen Sie sicher, dass Sie haben:

- Ein **Azure-Abonnement** mit Berechtigung zum Erstellen von Ressourcen (Eigentümer oder Mitwirkender auf einer Ressourcengruppe).
- Zugriff auf ein **Microsoft Foundry Projekt** in einer [Region mit Hosted Agents Unterstützung](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kontingent für **gpt-4.1** (oder **gpt-4.1-mini**) in Ihrem Foundry-Projekt.
- Folgende Tools installiert:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit Erweiterung](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (optional)
  - Python 3.10 oder höher

Führen Sie den [Hosted Agents Schnellstart mit `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) mindestens einmal vor der Durchführung aus, damit Sie ein funktionierendes Foundry-Projekt, Modellbereitstellung und Azure Container Registry haben, auf das Sie verweisen können, falls ein Lernender hängenbleibt.

---

## Foliendurchlauf

Das Deck folgt dem gleichen Ablauf wie die Labs. Vorgeschlagene Gesprächspunkte zu jedem Abschnitt:

| Abschnitt                  | Hauptaussage                                                                                                 |
|----------------------------|-------------------------------------------------------------------------------------------------------------|
| Titel und Agenda           | Stellen Sie den Workshop als *VS Code zu Foundry* dar, ohne Portalwechsel.                                  |
| Warum Hosted Agents?       | Verwaltete Laufzeit, ACR-basierte Bereitstellung, OpenAI-kompatible `/responses` API, auf Foundry-Projekte begrenzt. |
| Architekturdiagramm        | Durchgehen der [README Architektur](../README.md#architecture): Scaffold, Inspector, ACR, Agent Service.     |
| Aufbau eines Hosted Agents | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - was jede Datei macht.                            |
| Live-Demo: Executive Agent | Wechsel zu VS Code und führen Sie die [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) Demo komplett durch (siehe [Demo 1](#demo-1-executive-agent)). |
| Live-Demo: Resume to Job Fit Evaluator | Wechsel zu VS Code und führen Sie die [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-Agenten Demo durch (siehe [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 Kurzeinführung      | Übergabe an die Lernenden. Verweisen Sie auf [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Multi-Agent Mustermodelle  | Sequentiell vs. gleichzeitig vs. Übergabe - Vorschau vor dem Start von Lab 02.                             |
| Lab 02 Kurzeinführung      | Übergabe an die Lernenden. Verweisen Sie auf [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Abschluss und Ressourcen    | Links zum Weiterlernen aus dem Abschnitt [Zusätzliche Ressourcen](#weitere-ressourcen).                   |

---

## Demos

Zwei Live-Demos sind in der Durchführung enthalten. Planen Sie jeweils 10 Minuten ein.

| Demo                | Lab   | Dateien                                                      | Was gezeigt wird                                        |
|---------------------|-------|--------------------------------------------------------------|--------------------------------------------------------|
| Executive Agent     | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Einzelner gehosteter Agent; Übersetzung technischer Fachsprache in eine Executive-Zusammenfassung |
| Resume to Job Fit Evaluator | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-Agenten-Orchestrierung; Bewertung der Lebenslauf-Job-Passung und Empfehlungserstellung       |

### Demo 1: Executive Agent

Ein eigenständiger Agent in [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Nutzen Sie diesen als 10-Minuten-Demo vor Lab 01.

1. Öffnen Sie [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) und gehen Sie die Agent-Definition durch (System-Prompt, Modell, Framework).
2. Drücken Sie `F5`, um den **Agent Inspector** lokal zu starten.
3. Fügen Sie den Beispiel-Prompt aus der [README](../README.md#see-it-in-action) ein und zeigen Sie die Executive-Zusammenfassungs-Antwort.
4. Zeigen Sie [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) und [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile), um die Bereitstellungsartefakte zu erklären.
5. Demonstrieren Sie den Bereitstellungsablauf (Docker Build, ACR Push, Hosted Agent Erstellen) ohne auf die Fertigstellung zu warten.

### Demo 2: Resume to Job Fit Evaluator

Ein 4-Agenten-Workflow in [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Nutzen Sie diesen als 10-Minuten-Demo vor Lab 02.

1. Öffnen Sie [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) und zeigen Sie, wie die vier Agenten in einer sequentiellen Orchestrierung verbunden sind.
2. Drücken Sie `F5`, um den **Agent Inspector** für den Multi-Agenten-Workflow zu starten.
3. Fügen Sie eine kurze Stellenbeschreibung und einen Beispiel-Lebenslauf im Inspector-Chat ein.
4. Gehen Sie die Pipeline der vier Agenten durch: Lebenslauf-Parser, Job-Anforderungs-Extraktor, Passungsbeurteiler und Empfehlungsschreiber.
5. Weisen Sie darauf hin, wie die Ausgabe jedes Sub-Agenten zum Kontext des nächsten Agenten wird und heben Sie das Übergabemuster hervor.
6. Zeigen Sie [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) zum Vergleich mit dem Einzelagenten-Äquivalent aus Demo 1.

---

## Tipps für die Durchführung

- **Erwarten Sie Erwartungen frühzeitig.** Hosted Agents sind im Preview-Status – weisen Sie von Anfang an auf Regionsbegrenzungen und Kontingente hin, damit Teilnehmende während des Labs nicht überrascht werden.
- **Führen Sie zuerst die Voraussetzungen-Task aus.** Beide Labs enthalten eine VS Code Aufgabe „Voraussetzungen überprüfen“ - lassen Sie die Teilnehmenden diese ausführen, bevor Code geschrieben wird.
- **Halten Sie den Agent Inspector sichtbar.** Die meisten "Aha"-Momente passieren, wenn Lernende die lokale `/responses`-Round-Trip-Anzeige sehen.
- **Haben Sie ein Backup-Projekt bereit.** Wenn das Foundry-Projekt eines Lernenden das Kontingent überschreitet, teilen Sie ein vorprovisioniertes Projekt zum Bereitstellungsschritt, um Blockaden im Raum zu vermeiden.
- **Paaren Sie Teilnehmende.** Lab 02 (Multi-Agent) ist deutlich leichter, wenn Lernende den Workflow mit einem Partner besprechen können.
- **Nutzen Sie die Dokumentationsmodule als Checkpoints.** Jedes Lab enthält im `docs/` Ordner 8 nummerierte Module – nutzen Sie sie als natürliche Pausenpunkte.
- **Ziehen Sie das Basis-Docker-Image vorab** auf gemeinsam genutzten Lab-Rechnern, um Registrierungsrate-Limits zu vermeiden.

---

## Fehlerbehebung während der Durchführung

| Symptom                                      | Erstes, was zu versuchen ist                                                                             |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector kann keine Verbindung herstellen | Stellen Sie sicher, dass der Port `8088` frei ist und die Aufgabe `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` läuft. |
| Debugger kann nicht verbinden                    | Überprüfen Sie, dass Port `5679` frei ist; starten Sie VS Code neu, falls `debugpy` bereits gebunden ist.   |
| `azd up` schlägt mit Authentifizierungsfehler fehl  | Führen Sie `az login` und `azd auth login` aus, stellen Sie sicher, dass der korrekte Mandant ausgewählt ist. |
| Bereitstellung hängt beim ACR Push               | Prüfen Sie, ob Docker Desktop läuft und der Benutzer `AcrPush` auf dem Registry hat.                        |
| Modell liefert 404 / deployment nicht gefunden   | Der Name der Modellbereitstellung in `agent.yaml` muss mit der Bereitstellung im Foundry-Projekt übereinstimmen. |

| Hosted Agent hängt in `Provisioning`         | Überprüfen Sie, ob die Projektregion [gehostete Agents unterstützt](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) und ob Kontingent verfügbar ist. |
| Playground gibt 401 zurück                   | Authentifizieren Sie die Foundry-Erweiterung über die VS Code-Aktivitätsleiste erneut.           |

Für tiefere Anleitungen hat jedes Labor seine eigene `08-troubleshooting.md`-Datei – verlinken Sie die Lernenden dort:

- Labor 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Labor 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Anpassung dieser Sitzung

Sie können den Workshop gerne an Ihr Publikum anpassen. Übliche Varianten:

- **Backend-Publikum:** mehr Zeit für `agent.yaml`, Docker und ACR verwenden; Playground-Demo kürzen.
- **Citizen-Developer-Publikum:** im Foundry-Erweiterungs-UI für das Scaffolding bleiben; CLI-Schritte reduzieren.
- **Einzel-Track 60-Minuten-Slot:** nur Einführung, Demo und Labor 01 durchführen.
- **Workshop-Only (keine Folien) Format:** beide Labor-READMEs öffnen und als primäres Skript verwenden.

Wenn Sie die Labore erweitern, bitte die Änderungen per PR zurückgeben, damit andere Trainer davon profitieren.

---

## Weitere Ressourcen

- [Microsoft Foundry Dokumentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Übersicht gehosteter Agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Schnellstart: Deinen ersten gehosteten Agent bereitstellen (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Bereitstellung eines gehosteten Agents (How-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit für VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakte

Wenn Sie Fragen zur Durchführung dieser Sitzung haben, eröffnen Sie bitte ein Issue im [Workshop-Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) und taggen Sie den Maintainer.

| Rolle               | Name           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Maintainer / Kontakt | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->