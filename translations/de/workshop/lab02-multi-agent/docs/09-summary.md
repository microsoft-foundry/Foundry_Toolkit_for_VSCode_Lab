# Modul 9 - Zusammenfassung & nächste Schritte

⏱️ ~5 Min.

**Herzlichen Glückwunsch!** Sie haben einen Multi-Agenten-Workflow mit Microsoft Foundry und dem Foundry Toolkit für VS Code gebaut, getestet und (wenn auf Pfad A) bereitgestellt.

---

## Was Sie gebaut haben

Der **Lebenslauf → Job-Fit-Bewerter** – ein multi-agenten-gehosteter Workflow, der:
- Einen Lebenslauf + Stellenbeschreibung per HTTP empfängt (`POST /responses`)
- Vier spezialisierte Agenten in einer sequenziellen Pipeline ausführt – jeder Agent übergibt die Daten, die sein Nachfolger benötigt
- Einen Fit-Score (0–100 mit Aufschlüsselung), eine Liste von Kompetenz- und Zertifikatslücken sowie eine personalisierte Lern-Roadmap mit echten Microsoft Learn-Links für jede Lücke zurückgibt
- Den Microsoft Learn MCP-Server (`https://learn.microsoft.com/api/mcp`) aufruft, um offizielle Lernressourcen für jede identifizierte Kompetenzlücke abzurufen
- Als einzelner containerisierter und gehosteter Agent im Microsoft Foundry Agent Service läuft

---

## Zentrale Konzepte, die Sie gelernt haben

| Konzept | Was Sie geübt haben |
|---------|-------------------|
| **Multi-Agenten-Orchestrierung** | `WorkflowBuilder` sequenzielle Pipeline mit `add_edge()` |
| **Agentenspezialisierung** | Vier fokussierte Agenten sind leistungsfähiger als ein Allzweck-Agent |
| **Content Router Muster** | ResumeParser fungiert auch als Router – er bewahrt den JD-Text in einem `[JOB DESCRIPTION PASS-THROUGH]`-Abschnitt auf, sodass nachgelagerte Agenten darauf zugreifen können (erforderlich, weil `context_mode="last_agent"` bedeutet, dass nur der `start_executor` die rohe Benutzer-Nachricht sieht) |
| **Content Relay Muster** | JD Agent leitet `[PARSED RESUME PASS-THROUGH]` weiter, sodass MatchingAgent beide Profile erhält; vermeidet die OR-Semantik-Doppel-Auslösung, die Fan-in-Grafen verursachen |
| **MCP Tool-Integration** | `@tool` + `streamable_http_client`, das einen externen MCP-Server aufruft |
| **Lifecycle des gehosteten Agenten** | Scaffold → Konfigurieren → Lokal testen → Bereitstellen → Überprüfen in der Cloud |
| **`context_mode="last_agent"`** | Jeder Executor sieht nur die Ausgabe seines direkten Vorgängers |
| **Foundry Toolkit Workflow** | Scaffold-Assistent, Agent Inspector, Workflow Visualizer, Ein-Klick-Bereitstellung |

---

## Was Sie abgeschlossen haben

<details open>
<summary><strong>🅰️ Pfad A – Foundry-Abonnement</strong></summary>

- [x] Labor 01 Setup verifiziert: Projekt, Modell und RBAC sind noch aktiv
- [x] Multi-Agenten-Projekt mit dem Workflows-Template gescaffoldet
- [x] Vier Agenten-Instruktionssets geschrieben (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Microsoft Learn MCP Tool mit `streamable_http_client` integriert
- [x] Workflow-Graph mit `WorkflowBuilder` verdrahtet (sequenzielle Pipeline mit Content-Relay)
- [x] Lokal mit 3 Smoketests (Agent Inspector) getestet – Fit-Score, Lücken-Karten und MCP-URLs
- [x] Bereitstellung im Foundry Agent Service (containerisiert, verwaltete Identität)
- [x] In der Cloud-Playground verifiziert – strukturelle Konsistenz mit lokalen Ergebnissen

</details>

<details open>
<summary><strong>🅱️ Pfad B – Foundry Local</strong></summary>

- [x] Lab 01 Setup verifiziert: Foundry Local läuft mit lokalem Modell
- [x] Multi-Agenten-Projekt mit dem Workflows-Template gescaffoldet
- [x] Vier Agenten-Instruktionssets geschrieben und Workflow-Graph verdrahtet
- [x] Microsoft Learn MCP Tool integriert
- [x] Lokal mit 3 Smoketests getestet
- [x] Multi-Agenten-Verhalten validiert, ohne Cloud-Ressourcen zu benötigen

</details>

---

## Nächste Schritte

### Weiterlernen

| Ressource | Beschreibung |
|----------|-------------|
| **[Agent Framework SDK Referenz](https://learn.microsoft.com/agent-framework/)** | API-Dokumentation für `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP Tool-Katalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Agenten mit anderen MCP-Servern verbinden (Bing, GitHub, benutzerdefiniert) |
| **[Wissen hinzufügen (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Agenten mit Dokumenten, Vektorspeichern oder Bing-Suche anreichern |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Agentenqualität in großem Maßstab mit automatisierten Evaluierungen messen |
| **[Microsoft Foundry Dokumentation](https://learn.microsoft.com/azure/foundry/)** | Vollständige Plattformreferenz |
| **[Foundry Toolkit – Neuigkeiten](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Erweiterungs-Release-Notes und Changelog |

### Ideen zur Erweiterung dieses Workflows

- **Fügen Sie einen 5. Agenten hinzu** – Ein Interview-Coach, der basierend auf dem Lückenbericht wahrscheinliche Interviewfragen erzeugt
- **Fügen Sie ein Bing-Grundierungstool hinzu** – Lassen Sie den JD Agent ähnliche Stellenanzeigen suchen, um Anforderungen zu ergänzen
- **Anbindung an eine Lebenslauf-Datenbank** – Kandidatenprofile über ein benutzerdefiniertes `@tool` aus einer Datenbank abrufen
- **Probieren Sie verschiedene Modelle aus** – Vergleich der Ausgabequalität und Latenz von `gpt-4.1` vs. `gpt-4.1-mini`
- **Bewerten mit Foundry** – Verwenden Sie die Evaluationsfunktion, um Fit-Berichte gegen einen Gold-Datensatz zu bewerten

### Für Pfad-B-Nutzer: Upgrade zur Cloud-Bereitstellung

Wenn Sie bereit sind, in die Cloud bereitzustellen:
1. Holen Sie sich ein Azure-Abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Absolvieren Sie [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (Projekt erstellen, Modell bereitstellen, RBAC zuweisen)
3. Aktualisieren Sie Ihre `.env` mit dem Foundry-Projektendpunkt und dem Namen der Modellbereitstellung
4. Fahren Sie fort mit [Modul 06 – Bereitstellung in Foundry](06-deploy-to-foundry.md)

---

## Ressourcen bereinigen (optional)

Wenn Sie die während dieses Workshops erstellten Azure-Ressourcen entfernen möchten:

### Option 1: Ressourcengruppe löschen (entfernt alles)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Nur den gehosteten Agent löschen

1. Öffnen Sie [ai.azure.com](https://ai.azure.com) → Ihr Projekt → **Erstellen** → **Agenten**.
2. Finden Sie **PersonalCareerCopilot** → klicken Sie auf **Löschen**.

### Option 3: Die Modellbereitstellung löschen

1. Erweitern Sie in der Foundry-Seitenleiste Ihr Projekt → **Modelle**.
2. Rechtsklicken Sie auf die Modellbereitstellung → **Löschen**.

> **Kostenhinweis:** Gehostete Agenten verursachen nur Kosten, wenn sie laufen. Wenn Sie den Agent stoppen oder löschen, fallen keine laufenden Kosten an. Die Modellbereitstellung kann geringe Kosten für reservierte Kapazität verursachen – löschen Sie sie, wenn Sie fertig sind.

---

**Vorheriges:** [08 - Fehlerbehebung](08-troubleshooting.md) · **Startseite:** [Lab 02 README](../README.md) · [Workshop Startseite](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->