# Modul 8 - Fehlerbehebung

Dieses Modul ist ein Referenzhandbuch für häufige Probleme. Lesezeichen setzen und zurückkehren, wenn etwas schiefgeht.

---

## 1. Berechtigungsfehler

### 1.1 `agents/write` Berechtigung verweigert

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Ursache:** Fehlende `Azure AI User` Rolle auf der **Projekt**-Ebene. Dies ist der häufigste Fehler im Workshop.

**Lösung:**
1. Öffnen Sie [portal.azure.com](https://portal.azure.com).
2. Suchen Sie nach Ihrem Foundry-**Projekt**namen → Klicken Sie auf das Ergebnis vom Typ **"Microsoft Foundry project"** (NICHT das übergeordnete Konto).
3. **Zugriffskontrolle (IAM)** → **+ Hinzufügen** → **Rollenzuweisung hinzufügen**.
4. Rolle: **Azure AI User** → Weiter.
5. Mitglieder: Wählen Sie sich selbst aus → Überprüfen + zuweisen → Überprüfen + zuweisen.
6. **1–2 Minuten warten** → erneut versuchen.

> **Warum Owner/Contributor nicht ausreicht:** Diese Rollen erlauben nur *Verwaltungs*aktionen. Agenten-Operationen benötigen die `agents/write` *Datenaktion*, die nur in `Azure AI User`, `Azure AI Developer` oder `Azure AI Owner` enthalten ist. Siehe [Foundry RBAC-Dokumentation](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` während der Bereitstellung

**Lösung:** Bitten Sie Ihren Administrator, **Contributor** auf der Ressourcengruppe zuzuweisen oder das Projekt für Sie zu erstellen und Ihnen **Azure AI User** darauf zu geben.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker-Fehler

> Docker ist **optional**. Diese treten nur auf, wenn Docker Desktop installiert ist und die Erweiterung versucht, lokal zu bauen.

### 2.1 Docker-Daemon läuft nicht

**Lösung:** Starten Sie Docker Desktop → warten Sie auf den Status „laufend“ → prüfen mit `docker info` → erneut versuchen.

### 2.2 Build schlägt mit Abhängigkeitsfehlern fehl

**Lösung:** Überprüfen Sie die Schreibweise von `requirements.txt`, testen Sie zuerst lokal: `pip install -r requirements.txt`.

### 2.3 Plattform-Mismatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Authentifizierungsfehler

### 3.1 `DefaultAzureCredential` schlägt fehl

**Lösung (in Reihenfolge versuchen):**
1. `az login` (erneute Authentifizierung)
2. `az account set --subscription "<id>"` (korrektes Abonnement)
3. VS Code → Konten → Abmelden → erneut anmelden
4. Überprüfen: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funktioniert lokal, aber nicht gehostet

**Erwartet:** Gehostete Agenten verwenden eine systemverwaltete Identität, nicht Ihre Anmeldedaten. Wenn der gehostete Agent Authentifizierungsfehler erhält:
- Prüfen, ob `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `agent.yaml` auf Ihren Modellbereitstellungsnamen verweist (`FOUNDRY_PROJECT_ENDPOINT` wird von Foundry zur Laufzeit injiziert – nicht in `agent.yaml` deklarieren)
- Prüfen Sie, dass die verwaltete Identität des Projekts Zugriff auf das Modell hat

---

## 4. Modellfehler

### 4.1 Modellbereitstellung nicht gefunden

**Lösung:** Der Name ist **Groß-/Kleinschreibung beachten**. Vergleichen Sie `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` mit dem genauen Namen in der Foundry-Seitenleiste → Modelle.

### 4.2 Unerwartete Modell-Ausgabe

**Lösung:** Überprüfen Sie `AGENT_INSTRUCTIONS` in `main.py` (nicht abgeschnitten?). Versuchen Sie ein anderes Modell (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Bereitstellungsfehler

### 5.1 ACR-Pull nicht autorisiert

**Lösung:** Azure-Portal → Container Registry → Zugriffskontrolle (IAM) → **AcrPull**-Rolle für die verwaltete Identität des Foundry-Projekts hinzufügen.

### 5.2 Agent startet nicht (bleibt „Ausstehend“ oder „Fehlgeschlagen“)

Container-Protokolle in der Seitenleiste prüfen. Häufige Ursachen:

| Protokollnachricht | Lösung |
|-------------------|---------|
| `ModuleNotFoundError` | Fehlendes Paket zu `requirements.txt` hinzufügen, neu bereitstellen |
| `ValueError: Missing required environment variables` | Bestätigen, dass `AZURE_AI_MODEL_DEPLOYMENT_NAME` in `agent.yaml` unter `environment_variables` deklariert ist und einen Wert hat, dann neu bereitstellen. `FOUNDRY_PROJECT_ENDPOINT` wird von Foundry zur Laufzeit injiziert |
| `Address already in use` | Sicherstellen, dass nur ein Prozess an Port 8088 gebunden ist |

### 5.3 Bereitstellung läuft ins Zeitlimit

**Lösung:** Internetverbindung prüfen. Erste Bereitstellung überträgt >100MB. Hinter Proxy? Docker Desktop-Proxy-Einstellungen konfigurieren.

---

## 6. Pfad B - Foundry Local

### 6.1 Foundry Local startet nicht

| Problem | Lösung |
|---------|-------|
| `foundry: command not found` | Neuinstallation: `winget install Microsoft.FoundryLocal` |
| Unzureichende Ressourcen | Foundry Local benötigt ~4GB freien RAM. Andere Apps schließen. |
| Modell-Download schlägt fehl | Festplattenspeicher prüfen (Modelle sind 2–8 GB). Erneut versuchen: `foundry local models pull <name>` |

### 6.2 Foundry Local Modellfehler

| Problem | Lösung |
|---------|-------|
| Langsame Antworten | Erwartet – lokale Modelle laufen auf der CPU, es sei denn, Sie haben eine GPU. Geduldig sein. |
| Schlechte Ausgabequalität | Wenn Ihre Hardware es erlaubt, ein größeres Modell probieren. `phi-4-mini` ist ein guter Kompromiss. |
| Verbindung abgelehnt | Prüfen, ob Foundry Local läuft: `foundry local status`. Bei Bedarf neu starten. |

---

## 7. Kurzübersicht: RBAC-Rollen

| Rolle | Bereich | Gewährt |
|-------|--------|---------|
| **Azure AI User** | Projekt | Datenaktionen: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Datenaktionen + Projekterstellung |
| **Azure AI Owner** | Konto | Vollzugriff + Rollenzuweisung |
| **Contributor** | Abonnement/RG | Nur Verwaltungsaktionen (**keine** Datenaktionen) |
| **Owner** | Abonnement/RG | Verwaltung + Rollenzuweisung (**keine** Datenaktionen) |

---

## 8. Checkliste zur Workshop-Abschluss

| # | Punkt | Modul |
|---|-------|--------|
| 1 | Voraussetzungen installiert und überprüft | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit-Erweiterung installiert, Projekt verbunden (oder Pfad B konfiguriert) | [01](01-setup.md) |
| 3 | Gehosteter Agent erstellt | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfiguriert, Anweisungen geschrieben, Abhängigkeiten installiert | [03](03-configure-and-code.md) |
| 5 | Agent lokal getestet - 3 funktionale Szenarien bestanden | [04](04-test-locally.md) |
| 6 | In Foundry bereitgestellt (nur Pfad A) | [05](05-deploy-to-foundry.md) |
| 7 | Randfall-/Sicherheitstests in der Cloud bestanden (nur Pfad A) | [06](06-verify-in-playground.md) |
| 8 | Zusammenfassung überprüft, nächste Schritte festgelegt | [07](07-summary.md) |

---

**Vorherige:** [07 - Zusammenfassung](07-summary.md) · **Startseite:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->