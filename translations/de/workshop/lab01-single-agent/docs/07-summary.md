# Modul 7 - Zusammenfassung & nächste Schritte

⏱️ ~5 min

**Herzlichen Glückwunsch!** Du hast einen gehosteten KI-Agenten mit Microsoft Foundry und dem Foundry Toolkit für VS Code erstellt, getestet und (wenn auf Pfad A) bereitgestellt.

---

## Was du gebaut hast

Einen **„Erkläre es mir wie einem Geschäftsführer“-Agenten**, der:
- Technische Vorfallberichte oder Betriebsupdates per HTTP (`POST /responses`) empfängt
- Diese in verständliche Executive Summaries übersetzt
- Ein strukturiertes Ausgabeformat folgt (Was ist passiert / Geschäftliche Auswirkungen / Nächster Schritt)
- Themenfremde Anfragen und Versuche von Prompt Injection ablehnt
- Als containerisierter gehosteter Agent im Microsoft Foundry Agent Service läuft

---

## Wichtige Konzepte, die du gelernt hast

| Konzept | Was du geübt hast |
|---------|-------------------|
| **Agent Framework Architektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` Pipeline |
| **Lebenszyklus eines gehosteten Agents** | Scaffold → Konfigurieren → Lokal testen → Bereitstellen → In der Cloud verifizieren |
| **System-Prompt-Engineering** | Rolle, Zielgruppe, Ausgabeformat, Regeln, Sicherheitsbeschränkungen und Beispiele |
| **Unterschiede lokal vs. gehostet** | Identität (persönliche Anmeldeinformationen vs. verwaltete Identität), Endpunkt, Netzwerkpfad |
| **Sicherheitsgrenzen** | Schutz gegen Prompt Injection, Rollentreue, ordnungsgemäße Behandlung von Randfällen |
| **Foundry Toolkit Arbeitsablauf** | Projekterstellung, Modellausbringung, Agentengerüst, Agent Inspector, One-Click-Deploy |

---

## Was du abgeschlossen hast

### Pfad A (Foundry-Abonnement)

- [x] Foundry Toolkit eingerichtet und ein Foundry-Projekt mit bereitgestelltem Modell erstellt
- [x] Einen gehosteten Agenten mit automatisch generierter Projektstruktur gescaffoldt
- [x] Strukturierte Agentenanweisungen mit Sicherheitsregeln geschrieben
- [x] Lokal mit 3 funktionalen Szenarien getestet (Agent Inspector)
- [x] Im Foundry Agent Service bereitgestellt (containerisiert)
- [x] Im Cloud-Playground mit 4 Randfall-/Sicherheitstests verifiziert

### Pfad B (Foundry Local)

- [x] Foundry Toolkit mit lokalem Modell-Endpunkt eingerichtet
- [x] Ein gehostetes Agentenprojekt gescaffoldt
- [x] Strukturierte Agentenanweisungen mit Sicherheitsregeln geschrieben
- [x] Lokal mit 3 funktionalen Szenarien getestet
- [x] Agentenverhalten validiert ohne Cloud-Ressourcen zu benötigen

---

## Nächste Schritte

### Weiterlernen

| Ressource | Beschreibung |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestrierung](../../lab02-multi-agent/docs/README.md)** | Erstelle einen 4-Agenten-Workflow (Lebenslauf → Job-Fit-Bewerter) mit Orchestrierungsmustern |
| **[Füge deinem Agenten Tools hinzu](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Verbinde APIs, Datenbanken oder benutzerdefinierte Funktionen über den Tool-Katalog |
| **[Wissen hinzufügen (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Verankere deinen Agenten mit Dokumenten, Vektorspeichern oder Bing-Suche |
| **[Microsoft Foundry Dokumentation](https://learn.microsoft.com/azure/foundry/)** | Komplette Plattformreferenz |
| **[Agent Framework SDK-Referenz](https://learn.microsoft.com/agent-framework/)** | API-Dokumentation für das `agent-framework` Paket |
| **[Foundry Toolkit - Neuigkeiten](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Erweiterungsveröffentlichungen und Änderungsprotokoll |

### Ideen zur Erweiterung deines Agenten

- **Füge ein Datums-Tool hinzu** - Lass den Agenten „Stand heute“ Kontext in Zusammenfassungen einfügen
- **Verbinde dich mit einer Incident-Datenbank** - Ziehe echte Vorfalldetails über eine Tool-Funktion
- **Füge ein Bing-Grundierungs-Tool hinzu** - Lass den Agenten aktuelle Nachrichten für zusätzlichen Kontext nachschlagen
- **Teste verschiedene Modelle** - Vergleiche die Ausgabequalität von `gpt-4.1` vs. `gpt-4.1-mini`
- **Bewerte mit Foundry** - Nutze die Evaluationsfunktion, um Agentenqualität im großen Maßstab zu messen

### Für Pfad-B-Nutzer: Upgrade zur Cloud-Bereitstellung

Wenn du bereit bist, in die Cloud zu deployen:
1. Hole dir ein Azure-Abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Schließe [Modul 01, Einrichtung](01-setup.md#step-2-set-up-based-on-your-access) ab (Projekt erstellen, Modell bereitstellen, RBAC zuweisen)
3. Aktualisiere deine `.env` mit dem Foundry-Projektendpunkt und dem Namen der Modellbereitstellung
4. Setze fort bei [Modul 05 - Bereitstellung in Foundry](05-deploy-to-foundry.md)

---

## Ressourcen bereinigen (optional)

Wenn du die während dieses Workshops erstellten Azure-Ressourcen entfernen möchtest:

### Option 1: Lösche die Ressourcengruppe (entfernt alles)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2: Lösche nur den gehosteten Agenten

1. Öffne [ai.azure.com](https://ai.azure.com) → dein Projekt → **Build** → **Agents**.
2. Klicke deinen Agenten an → klicke **Löschen**.

### Option 3: Lösche die Modellbereitstellung

1. Erweitere in der Foundry-Seitenleiste dein Projekt → **Modelle**.
2. Rechtsklicke die Modellbereitstellung → **Löschen**.

> **Kostenhinweis:** Gehostete Agenten verursachen nur Kosten, wenn sie laufen. Wenn du den Agenten stoppst oder löscht, gibt es keine laufenden Kosten. Die Modellbereitstellung kann geringe Kosten für reservierte Kapazität verursachen – lösche sie, wenn du fertig bist.

---

**Zurück:** [06 - Verifizieren im Playground](06-verify-in-playground.md) · **Weiter:** [08 - Fehlerbehebung (Referenz) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->