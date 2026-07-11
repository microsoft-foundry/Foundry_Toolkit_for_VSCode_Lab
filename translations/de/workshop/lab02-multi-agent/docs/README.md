# Labor 02 - Multi-Agent Workflow: Lebenslauf → Job Fit Evaluator

## Vollständiger Lernpfad

Diese Dokumentation führt Sie durch den Aufbau, das Testen und den Einsatz eines **Multi-Agent Workflows**, der die Übereinstimmung von Lebenslauf und Job mithilfe von vier spezialisierten Agenten bewertet, die über **WorkflowBuilder** orchestriert werden.

> **Voraussetzung:** Schließen Sie [Labor 01 - Einzelner Agent](../../lab01-single-agent/README.md) ab, bevor Sie mit Labor 02 beginnen.

---

## Module

| # | Modul | Was Sie tun werden |
|---|--------|--------------------|
| 0 | [Einführung](00-prerequisites.md) | Was Sie bauen, Überprüfung von Labor 01, Vergleich Labor 02 vs Labor 01 |
| 1 | [Multi-Agent-Architektur verstehen](01-understand-multi-agent.md) | Lernen Sie WorkflowBuilder, Agentenrollen, Orchestrierungsgraph kennen |
| 2 | [Multi-Agent-Projekt scaffolden](02-scaffold-multi-agent.md) | Verwenden Sie den Foundry-Erweiterungsassistenten zum Erstellen des Basisprojekts |
| 3 | [Agenten & Umgebung konfigurieren](03-configure-agents.md) | Schreiben Sie Anweisungen für 4 Agenten, konfigurieren Sie das MCP-Tool, setzen Sie Umgebungsvariablen |
| 4 | [Orchestrierungsmuster](04-orchestration-patterns.md) | Sequenzielle Kette, Inhaltsweiterleitung und WorkflowBuilder-OR-Semantik |
| 5 | [Lokal testen](05-test-locally.md) | F5-Debug mit Agent Inspector, führen Sie Smoke-Tests mit Lebenslauf + JD durch |
| 6 | [In Foundry bereitstellen](06-deploy-to-foundry.md) | Container bauen, in ACR pushen, gehosteten Agent registrieren |
| 7 | [Im Playground verifizieren](07-verify-in-playground.md) | Testen Sie den bereitgestellten Agenten in VS Code- und Foundry-Portal-Playgrounds |
| 8 | [Fehlerbehebung](08-troubleshooting.md) | Beheben Sie häufige Multi-Agent-Probleme (MCP-Fehler, abgeschnittene Ausgabe, Paketversionen) |
| 9 | [Zusammenfassung & nächste Schritte](09-summary.md) | Was Sie gebaut haben, erlernte Schlüsselkonzepte, Aufräumen und wohin als Nächstes |

---

**Zurück zu:** [Labor 02 README](../README.md) · [Workshop-Startseite](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->