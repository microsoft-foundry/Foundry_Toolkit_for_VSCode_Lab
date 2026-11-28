# Modul 9 - Zusammenfassung & nächste Schritte

⏱️ ~5 Min.

**Herzlichen Glückwunsch!** Sie haben einen Multi-Agenten-Workflow mit Microsoft Foundry und dem Foundry Toolkit für VS Code erstellt, getestet und (wenn auf Pfad A) bereitgestellt.

---

## Was Sie gebaut haben

Der **Resume → Job Fit Evaluator** – ein gehosteter Multi-Agenten-Workflow, der:
- Einen Lebenslauf + eine Stellenbeschreibung per HTTP empfängt (`POST /responses`)
- Vier spezialisierte Agenten in einer sequentiellen Pipeline ausführt - jeder Agent übermittelt die Daten an seinen Nachfolger, die dieser benötigt
- Eine Fit-Bewertung (0–100 mit Aufschlüsselung), eine Liste von Kompetenz- und Zertifikatslücken sowie eine personalisierte Lern-Roadmap mit echten Microsoft Learn-Links für jede Lücke zurückgibt
- Den Microsoft Learn MCP-Server (`https://learn.microsoft.com/api/mcp`) aufruft, um offizielle Lernressourcen für jede erkannte Kompetenzlücke abzurufen
- Als einzelner containerisierter, gehosteter Agent im Microsoft Foundry Agent Service läuft

---

## Wichtige Konzepte, die Sie gelernt haben

| Konzept | Was Sie geübt haben |
|---------|-------------------|
| **Multi-Agenten-Orchestrierung** | `WorkflowBuilder` sequentielle Pipeline mit `add_edge()` |
| **Agentenspezialisierung** | Vier fokussierte Agenten übertreffen einen Agenten mit allgemeinem Zweck |
| **Content Router Pattern** | ResumeParser fungiert gleichzeitig als Router – er bewahrt den JD-Text in einem `[JOB DESCRIPTION PASS-THROUGH]`-Abschnitt auf, so dass nachgelagerte Agenten darauf zugreifen können (erforderlich, weil `context_mode="last_agent"` bedeutet, dass nur der `start_executor` die rohe Benutzer-Nachricht sieht) |
| **Content Relay Pattern** | JD Agent leitet `[PARSED RESUME PASS-THROUGH]` weiter, sodass MatchingAgent beide Profile erhält; vermeidet die OR-Semantik Doppel-Auslösung, die Fan-in-Graphen verursachen |
| **MCP-Tool-Integration** | `@tool` + `streamable_http_client` zum Aufrufen eines externen MCP-Servers |
| **Lebenszyklus des gehosteten Agents** | Gerüst erstellen → Konfigurieren → Lokal testen → Bereitstellen → In der Cloud überprüfen |
| **`context_mode="last_agent"`** | Jeder Executor sieht nur die Ausgabe seines direkten Vorgängers |
| **Foundry Toolkit Workflow** | Scaffold-Assistent, Agent Inspector, Workflow Visualizer, Ein-Klick-Bereitstellung |

---

## Was Sie abgeschlossen haben

<details open>
<summary><strong>🅰️ Pfad A - Foundry-Abonnement</strong></summary>

- [x] Überprüfung der Lab 01 Einrichtung: Projekt, Modell und RBAC noch aktiv
- [x] Ein Multi-Agenten-Projekt mit der Workflows-Vorlage eingerüstet
- [x] Vier Agenten-Anweisungssets geschrieben (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Das Microsoft Learn MCP-Tool mit `streamable_http_client` integriert
- [x] Den Workflow-Graphen mit `WorkflowBuilder` verdrahtet (sequentielle Pipeline mit Inhaltsweiterleitung)
- [x] Lokal mit 2 Smoke-Tests getestet (Agent Inspector) – Fit-Score, Gap-Karten und MCP-URLs
- [x] In den Foundry Agent Service (containerisiert, verwaltete Identität) bereitgestellt
- [x] In der Cloud-Testumgebung verifiziert – strukturelle Konsistenz mit lokalen Ergebnissen

</details>

<details open>
<summary><strong>🅱️ Pfad B - Foundry Local</strong></summary>

- [x] Überprüfung der Lab 01 Einrichtung: Foundry Local läuft mit einem lokalen Modell
- [x] Ein Multi-Agenten-Projekt mit der Workflows-Vorlage eingerüstet
- [x] Vier Agenten-Anweisungssets geschrieben und den Workflow-Graphen verdrahtet
- [x] Das Microsoft Learn MCP-Tool integriert
- [x] Lokal mit 2 Smoke-Tests getestet
- [x] Das Multi-Agenten-Verhalten validiert, ohne Cloud-Ressourcen zu benötigen

</details>

---

## Nächste Schritte

### Lernen Sie weiter

| Ressource | Beschreibung |
|----------|-------------|
| **[Agent Framework SDK Referenz](https://learn.microsoft.com/agent-framework/)** | API-Dokumentation für `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP Tool Katalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Agenten mit anderen MCP-Servern verbinden (Bing, GitHub, benutzerdefiniert) |
| **[Wissen hinzufügen (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Agenten mit Dokumenten, Vektorenspeichern oder Bing-Suche grundieren |
| **[Foundry Bewertungen](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Agentenqualität im großen Maßstab mit automatisierten Bewertungen messen |
| **[Microsoft Foundry Dokumentation](https://learn.microsoft.com/azure/foundry/)** | Vollständige Plattformreferenz |
| **[Foundry Toolkit – Neuigkeiten](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Erweiterungs-Release-Notes und Changelog |

### Ideen zur Erweiterung dieses Workflows

- **Einen 5. Agenten hinzufügen** – Ein Interview-Coach, der basierend auf dem Gap-Bericht wahrscheinliche Interviewfragen erstellt
- **Ein Bing-Grundierungstool hinzufügen** – Dem JD Agent erlauben, nach ähnlichen Stellenangeboten zu suchen, um Anforderungen zu bereichern
- **Mit einer Lebenslauf-Datenbank verbinden** – Kandidatenprofile über eine benutzerdefinierte `@tool` aus einer Datenbank abrufen
- **Verschiedene Modelle ausprobieren** – `gpt-4.1` vs. `gpt-4.1-mini` bezüglich Ausgabequalität und Latenz vergleichen
- **Mit Foundry evaluieren** – Verwenden Sie die Bewertungsfunktion, um Fit-Berichte mit einem Goldstandard-Datensatz zu bewerten

### Für Benutzer von Pfad B: Upgrade zur Cloud-Bereitstellung

Wenn Sie bereit sind, in die Cloud bereitzustellen:
1. Holen Sie sich ein Azure-Abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Vervollständigen Sie [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (Projekt erstellen, Modell bereitstellen, RBAC zuweisen)
3. Aktualisieren Sie Ihr `.env` mit dem Foundry-Projektendpunkt und dem Namen der Modellbereitstellung
4. Fahren Sie fort mit [Modul 06 - Bereitstellung in Foundry](06-deploy-to-foundry.md)

---

## Ressourcen bereinigen (optional)

Wenn Sie die im Workshop erstellten Azure-Ressourcen entfernen möchten:

### Option 1: Löschen Sie die Ressourcengruppe (entfernt alles)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Löschen Sie nur den gehosteten Agent

1. Öffnen Sie [ai.azure.com](https://ai.azure.com) → Ihr Projekt → **Build** → **Agents**.
2. Finden Sie **PersonalCareerCopilot** → klicken Sie auf **Löschen**.

### Option 3: Löschen der Modellbereitstellung

1. Erweitern Sie in der Foundry-Seitenleiste Ihr Projekt → **Modelle**.
2. Klicken Sie mit der rechten Maustaste auf die Modellbereitstellung → **Löschen**.

> **Kosten-Hinweis:** Gehostete Agents verursachen nur Kosten, wenn sie ausgeführt werden. Wenn Sie den Agent stoppen oder löschen, fallen keine laufenden Gebühren an. Die Modellbereitstellung kann eine kleine Gebühr für reservierte Kapazität verursachen – löschen Sie sie, wenn Sie fertig sind.

---

**Vorherige:** [08 - Fehlerbehebung](08-troubleshooting.md) · **Start:** [Lab 02 README](../README.md) · [Workshop Startseite](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->