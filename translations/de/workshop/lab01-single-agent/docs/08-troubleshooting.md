# Modul 8 - Fehlerbehebung

Dieses Modul ist ein Nachschlagewerk für häufige Probleme. Lesezeichen setzen und zurückkehren, wenn etwas schiefgeht.

---

## 1. Berechtigungsfehler

### 1.1 `agents/write` Berechtigung verweigert

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Ursache:** Fehlende Rolle `Azure AI User` auf **Projektebene**. Dies ist der häufigste Workshop-Fehler.

**Lösung:**
1. Öffne [portal.azure.com](https://portal.azure.com).
2. Suche deinen Foundry **Projekt**-Namen → klicke das Ergebnis vom Typ **"Microsoft Foundry project"** (NICHT der übergeordnete Account).
3. **Zugriffskontrolle (IAM)** → **+ Hinzufügen** → **Rollen zuweisen**.
4. Rolle: **Azure AI User** → Weiter.
5. Mitglieder: Wähle dich selbst aus → Überprüfen + zuweisen → Überprüfen + zuweisen.
6. **1–2 Minuten warten** → erneut versuchen.

> **Warum Owner/Contributor nicht ausreichen:** Diese Rollen erlauben nur *Verwaltungs*-Aktionen. Agent-Operationen erfordern die `agents/write` *Datenaktion*, die nur in `Azure AI User`, `Azure AI Developer` oder `Azure AI Owner` enthalten ist. Siehe [Foundry RBAC Dokumentation](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` während der Bereitstellung

**Lösung:** Bitten Sie Ihren Administrator, Ihnen die Rolle **Contributor** auf die Ressourcengruppe zuzuweisen oder lassen Sie ihn das Projekt für Sie erstellen und Ihnen die Rolle **Azure AI User** darauf zuweisen.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Warten bis: "Registriert"
```

---

## 2. Docker-Fehler

> Docker ist **optional**. Diese Fehler treten nur auf, wenn Docker Desktop installiert ist und die Erweiterung versucht, lokal zu bauen.

### 2.1 Docker-Daemon läuft nicht

**Lösung:** Starte Docker Desktop → warte auf "running"-Status → mit `docker info` überprüfen → erneut versuchen.

### 2.2 Build schlägt wegen Abhängigkeitsfehlern fehl

**Lösung:** Rechtschreibung von `requirements.txt` überprüfen, lokal testen mit: `pip install -r requirements.txt`.

### 2.3 Plattforminkompatibilität (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Authentifizierungsfehler

### 3.1 `DefaultAzureCredential` schlägt fehl

**Lösung (in dieser Reihenfolge versuchen):**
1. `az login` (erneute Authentifizierung)
2. `az account set --subscription "<id>"` (korrekte Subscription)
3. VS Code → Konten → Abmelden → erneutes Anmelden
4. Überprüfen: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funktioniert lokal, aber nicht gehostet

**Erwartung:** Gehostete Agenten verwenden systemverwaltete Identität, nicht Ihre Anmeldedaten. Wenn der gehostete Agent Authentifizierungsfehler bekommt:
- Überprüfen, ob `AZURE_AI_PROJECT_ENDPOINT` in `agent.yaml` korrekt ist
- Prüfen, ob die verwaltete Identität des Projekts Zugriff auf das Modell hat

---

## 4. Modell-Fehler

### 4.1 Modell-Bereitstellung nicht gefunden

**Lösung:** Der Name ist **Groß-/Kleinschreibung beachten**. Vergleiche `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` mit dem exakten Namen in der Foundry-Seitenleiste → Modelle.

### 4.2 Unerwartete Modellausgabe

**Lösung:** Überprüfe `AGENT_INSTRUCTIONS` in `main.py` (nicht abgeschnitten?). Probiere ein anderes Modell (`gpt-4.1` vs. `gpt-4.1-mini`).

---

## 5. Bereitstellungsfehler

### 5.1 ACR Pull nicht autorisiert

**Lösung:** Azure Portal → Container Registry → Zugriffskontrolle (IAM) → Rolle **AcrPull** der verwalteten Identität des Foundry-Projekts hinzufügen.

### 5.2 Agent startet nicht (bleibt "Pending" oder "Failed")

Überprüfe Container-Logs in der Seitenleiste. Häufige Ursachen:

| Lognachricht | Lösung |
|-------------|--------|
| `ModuleNotFoundError` | Fehlendes Paket zu `requirements.txt` hinzufügen, neu bereitstellen |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Env-Var zu `agent.yaml` unter `environment_variables` hinzufügen |
| `Address already in use` | Sicherstellen, dass nur ein Prozess Port 8088 bindet |

### 5.3 Bereitstellung läuft ins Timeout

**Lösung:** Internetverbindung überprüfen. Erste Bereitstellung überträgt >100MB. Hinter Proxy? Docker Desktop Proxy-Einstellungen konfigurieren.

---

## 6. Pfad B - Foundry Local

### 6.1 Foundry Local startet nicht

| Problem | Lösung |
|---------|--------|
| `foundry: command not found` | Neu installieren: `winget install Microsoft.FoundryLocal` |
| Nicht genügend Ressourcen | Foundry Local benötigt ~4GB freien RAM. Andere Apps schließen. |
| Modell-Download schlägt fehl | Festplattenspeicher prüfen (Modelle sind 2–8 GB). Erneut versuchen: `foundry local models pull <name>` |

### 6.2 Foundry Local Modell-Fehler

| Problem | Lösung |
|---------|--------|
| Langsame Antworten | Erwartet – lokale Modelle laufen auf CPU, es sei denn, du hast eine GPU. Geduldig sein. |
| Schlechte Ausgabequalität | Größeres Modell versuchen, wenn Hardware es erlaubt. `phi-4-mini` ist ein guter Kompromiss. |
| Verbindung verweigert | Prüfen, ob Foundry Local läuft: `foundry local status`. Bei Bedarf neu starten. |

---

## 7. Schnellreferenz: RBAC-Rollen

| Rolle | Umfang | Gewährt |
|-------|--------|---------|
| **Azure AI User** | Projekt | Datenaktionen: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Datenaktionen + Projekterstellung |
| **Azure AI Owner** | Konto | Vollzugriff + Rollenverwaltung |
| **Contributor** | Subscription/RG | Nur Verwaltungsaktionen (**keine** Datenaktionen) |
| **Owner** | Subscription/RG | Verwaltung + Rollenzuweisung (**keine** Datenaktionen) |

---

## 8. Workshop-Abschluss-Checkliste

| # | Punkt | Modul |
|---|-------|--------|
| 1 | Voraussetzungen installiert und geprüft | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit-Erweiterung installiert, Projekt verbunden (oder Pfad B konfiguriert) | [01](01-setup.md) |
| 3 | Gehosteter Agent eingerichtet | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfiguriert, Anweisungen geschrieben, Abhängigkeiten installiert | [03](03-configure-and-code.md) |
| 5 | Agent lokal getestet - 3 Funktionsszenarien erfolgreich | [04](04-test-locally.md) |
| 6 | Bereitstellung in Foundry (nur Pfad A) | [05](05-deploy-to-foundry.md) |
| 7 | Randfall-/Sicherheitstests in der Cloud bestanden (nur Pfad A) | [06](06-verify-in-playground.md) |
| 8 | Zusammenfassung überprüft, nächste Schritte identifiziert | [07](07-summary.md) |

---

**Vorheriges:** [07 - Zusammenfassung](07-summary.md) · **Start:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->