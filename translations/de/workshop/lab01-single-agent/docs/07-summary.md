# Modul 7 - Zusammenfassung & Nächste Schritte

⏱️ ~5 Min.

**Herzlichen Glückwunsch!** Sie haben einen gehosteten KI-Agenten mit Microsoft Foundry und dem Foundry Toolkit für VS Code erstellt, getestet und (falls auf Pfad A) bereitgestellt.

---

## Was Sie erstellt haben

Einen **„Erkläre es mir wie einem Geschäftsführer“** Agenten, der:
- Empfängt technische Vorfallmeldungen oder betriebliche Updates über HTTP (`POST /responses`)
- Übersetzt sie in verständliche Executive Summaries
- Folgt einem strukturierten Ausgabeformat (Was ist passiert / Geschäftsauswirkung / Nächster Schritt)
- Lehnt themenfremde Anfragen und Prompt Injection Versuche ab
- Läuft als containerisierter gehosteter Agent im Microsoft Foundry Agent Service

---

## Wichtige erlernte Konzepte

| Konzept | Was Sie geübt haben |
|---------|-------------------|
| **Agent Framework Architektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` Pipeline |
| **Lebenszyklus gehosteter Agents** | Scaffold → Konfigurieren → Lokal testen → Bereitstellen → Im Cloud überprüfen |
| **System Prompt Engineering** | Rolle, Zielgruppe, Ausgabeformat, Regeln, Sicherheitsvorgaben und Beispiele |
| **Lokale vs. gehostete Unterschiede** | Identität (persönliche Anmeldedaten vs. verwaltete Identität), Endpunkt, Netzwerkpfad |
| **Sicherheitsgrenzen** | Prompt-Injection-Abwehr, Rollentreue, eleganter Umgang mit Randfällen |
| **Foundry Toolkit Workflow** | Projektanlage, Modellbereitstellung, Agent Scaffold, Agent Inspector, Ein-Klick-Bereitstellung |

---

## Was Sie abgeschlossen haben

### Weg A (Foundry-Abonnement)

- [x] Foundry Toolkit eingerichtet und ein Foundry-Projekt mit bereitgestelltem Modell erstellt
- [x] Einen gehosteten Agenten mit automatisch generierter Projektstruktur gescaffoldet
- [x] Strukturierte Agentenanweisungen mit Sicherheitsregeln geschrieben
- [x] Lokal mit 3 funktionalen Szenarien getestet (Agent Inspector)
- [x] Im Foundry Agent Service (containerisiert) bereitgestellt
- [x] Im Cloud Playground mit 4 Randfall-/Sicherheits-Tests verifiziert

### Weg B (Foundry Local)

- [x] Foundry Toolkit mit lokalem Modellendpunkt eingerichtet
- [x] Einen gehosteten Agentenprojekt gescaffoldet
- [x] Strukturierte Agentenanweisungen mit Sicherheitsregeln geschrieben
- [x] Lokal mit 3 funktionalen Szenarien getestet
- [x] Agentenverhalten validiert, ohne Cloud-Ressourcen zu benötigen

---

## Nächste Schritte

### Weiterlernen

| Ressource | Beschreibung |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestrierung](../../lab02-multi-agent/docs/README.md)** | Erstellen eines Workflows mit 4 Agenten (Lebenslauf → Job Fit Evaluator) mit Orchestrierungsmustern |
| **[Werkzeuge zu Ihrem Agenten hinzufügen](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Verbinden von APIs, Datenbanken oder benutzerdefinierten Funktionen über den Tool-Katalog |
| **[Wissen hinzufügen (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ihren Agenten mit Dokumenten, Vektor-Stores oder Bing-Suche fundieren |
| **[Microsoft Foundry Dokumentation](https://learn.microsoft.com/azure/foundry/)** | Vollständige Plattformreferenz |
| **[Agent Framework SDK Referenz](https://learn.microsoft.com/agent-framework/)** | API-Dokumentation für `agent-framework` Paket |
| **[Foundry Toolkit - Neuigkeiten](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Erweiterungs-Release-Notes und Änderungsprotokoll |

### Ideen zur Erweiterung Ihres Agenten

- **Fügen Sie ein Datumswerkzeug hinzu** - Ermöglichen Sie dem Agenten, den Kontext "Stand heute" in Zusammenfassungen einzubeziehen
- **Verbinden Sie eine Incident-Datenbank** - Ziehen Sie reale Vorfalldetails über eine Tool-Funktion
- **Fügen Sie ein Bing-Fundament-Werkzeug hinzu** - Ermöglichen Sie dem Agenten, aktuelle Nachrichten für zusätzlichen Kontext nachzuschlagen
- **Probieren Sie verschiedene Modelle aus** - Vergleichen Sie die Ausgabequalität von `gpt-4.1` vs. `gpt-4.1-mini`
- **Bewerten Sie mit Foundry** - Verwenden Sie die Evaluationsfunktion, um die Agentenqualität im Maßstab zu messen

### Für Weg B Nutzer: Upgrade zur Cloud-Bereitstellung

Wenn Sie bereit sind, in die Cloud bereitzustellen:
1. Holen Sie sich ein Azure-Abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Komplettieren Sie [Modul 01, Einrichtung](01-setup.md#step-2-set-up-based-on-your-access) (Projekt erstellen, Modell bereitstellen, RBAC zuweisen)
3. Aktualisieren Sie Ihre `.env` mit dem Foundry-Projektendpunkt und dem Namen der Modellbereitstellung
4. Fahren Sie fort mit [Modul 05 - Bereitstellung in Foundry](05-deploy-to-foundry.md)

---

## Ressourcen bereinigen (optional)

Wenn Sie die während dieses Workshops erstellten Azure-Ressourcen entfernen möchten:

### Option 1: Löschen der Ressourcengruppe (entfernt alles)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Nur den gehosteten Agent löschen

1. Öffnen Sie [ai.azure.com](https://ai.azure.com) → Ihr Projekt → **Build** → **Agents**.
2. Klicken Sie auf Ihren Agent → klicken Sie auf **Löschen**.

### Option 3: Die Modellbereitstellung löschen

1. Erweitern Sie in der Foundry-Seitenleiste Ihr Projekt → **Models**.
2. Rechtsklicken Sie auf die Modellbereitstellung → **Löschen**.

> **Kostenhinweis:** Gehostete Agenten verursachen nur Kosten, wenn sie laufen. Wenn Sie den Agent stoppen oder löschen, fallen keine laufenden Gebühren an. Die Modellbereitstellung kann eine kleine Gebühr für reservierte Kapazität verursachen – löschen Sie sie, wenn Sie fertig sind.

---

**Vorherige:** [06 - Überprüfung im Playground](06-verify-in-playground.md) · **Nächste:** [08 - Fehlerbehebung (Referenz) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->