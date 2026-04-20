# Labor 02 - Multi-Agenten-Workflow: Lebenslauf → Job-Fit-Bewerter

## Vollständiger Lernpfad

Diese Dokumentation führt Sie durch den Aufbau, das Testen und das Bereitstellen eines **Multi-Agenten-Workflows**, der die Übereinstimmung von Lebenslauf und Stelle mit vier spezialisierten Agenten bewertet, die über den **WorkflowBuilder** orchestriert werden.

> **Voraussetzung:** Schließen Sie [Labor 01 - Einzelner Agent](../../lab01-single-agent/README.md) ab, bevor Sie mit Labor 02 beginnen.

---

## Module

| # | Modul | Was Sie tun werden |
|---|--------|--------------------|
| 0 | [Voraussetzungen](00-prerequisites.md) | Überprüfen Sie den Abschluss von Labor 01, verstehen Sie Multi-Agenten-Konzepte |
| 1 | [Multi-Agenten-Architektur verstehen](01-understand-multi-agent.md) | Lernen Sie WorkflowBuilder, Agentenrollen, Orchestrierungsgraph kennen |
| 2 | [Multi-Agenten-Projekt aufsetzen](02-scaffold-multi-agent.md) | Verwenden Sie die Foundry-Erweiterung, um einen Multi-Agenten-Workflow aufzusetzen |
| 3 | [Agenten & Umgebung konfigurieren](03-configure-agents.md) | Schreiben Sie Anweisungen für 4 Agenten, konfigurieren Sie das MCP-Tool, setzen Sie Umgebungsvariablen |
| 4 | [Orchestrierungsmuster](04-orchestration-patterns.md) | Erkunden Sie parallelen Fan-Out, sequentielle Aggregation und alternative Muster |
| 5 | [Lokal testen](05-test-locally.md) | F5-Debug mit Agent Inspector, führen Sie Smoke-Tests mit Lebenslauf + JD durch |
| 6 | [Bereitstellen in Foundry](06-deploy-to-foundry.md) | Erstellen Sie Container, pushen Sie zu ACR, registrieren Sie gehosteten Agenten |
| 7 | [Im Playground verifizieren](07-verify-in-playground.md) | Testen Sie den bereitgestellten Agenten in VS Code und Foundry Portal Playgrounds |
| 8 | [Fehlerbehebung](08-troubleshooting.md) | Beheben Sie häufige Multi-Agenten-Probleme (MCP-Fehler, abgeschnittene Ausgabe, Paketversionen) |

---

## Geschätzte Zeit

| Erfahrungslevel | Zeit |
|-----------------|------|
| Labor 01 kürzlich abgeschlossen | 45-60 Minuten |
| Etwas Azure AI Erfahrung | 60-90 Minuten |
| Erstmals mit Multi-Agenten | 90-120 Minuten |

---

## Architektur auf einen Blick

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Zurück zu:** [Labor 02 README](../README.md) · [Workshop-Startseite](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprache ist als maßgebliche Quelle zu betrachten. Für kritische Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->