# Modul 8 - Fehlerbehebung

Dieses Modul ist ein Nachschlagewerk für jede häufige Fehlermeldung, die während des Workshops auftritt. Setzen Sie ein Lesezeichen – Sie werden es immer wieder zurate ziehen, wenn etwas schiefgeht.

---

## 1. Berechtigungsfehler

### 1.1 `agents/write` Berechtigung verweigert

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Ursache:** Sie haben die Rolle `Azure AI User` nicht auf **Projektebene**. Dies ist der mit Abstand häufigste Fehler im Workshop.

**Lösung - Schritt für Schritt:**

1. Öffnen Sie [https://portal.azure.com](https://portal.azure.com).
2. Geben Sie in der oberen Suchleiste den Namen Ihres **Foundry-Projekts** ein (z.B. `workshop-agents`).
3. **Wichtig:** Klicken Sie auf das Ergebnis mit dem Typ **"Microsoft Foundry project"** und NICHT auf das übergeordnete Konto/Hub-Ressource. Dies sind unterschiedliche Ressourcen mit verschiedenen RBAC-Bereichen.
4. Klicken Sie in der linken Navigation der Projektseite auf **Zugriffskontrolle (IAM)**.
5. Klicken Sie auf die Registerkarte **Rollen-Zuweisungen**, um zu prüfen, ob Sie die Rolle bereits haben:
   - Suchen Sie nach Ihrem Namen oder Ihrer E-Mail.
   - Wenn `Azure AI User` bereits aufgeführt ist → liegt der Fehler woanders (siehe Schritt 8 unten).
   - Wenn nicht aufgeführt → fahren Sie fort, die Rolle hinzuzufügen.
6. Klicken Sie auf **+ Hinzufügen** → **Rollen-Zuweisung hinzufügen**.
7. Im Tab **Rolle**:
   - Suchen Sie nach [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Wählen Sie es aus den Ergebnissen aus.
   - Klicken Sie auf **Weiter**.
8. Im Tab **Mitglieder**:
   - Wählen Sie **Benutzer, Gruppe oder Dienstprinzipal** aus.
   - Klicken Sie auf **+ Mitglieder auswählen**.
   - Suchen Sie Ihren Namen oder Ihre E-Mail-Adresse.
   - Wählen Sie sich selbst aus den Ergebnissen aus.
   - Klicken Sie auf **Auswählen**.
9. Klicken Sie auf **Überprüfen + zuweisen** → erneut auf **Überprüfen + zuweisen**.
10. **Warten Sie 1-2 Minuten** - RBAC-Änderungen brauchen Zeit zur Ausbreitung.
11. Versuchen Sie die fehlgeschlagene Aktion erneut.

> **Warum Besitzer/Beitragender nicht genug sind:** Azure RBAC unterscheidet zwei Berechtigungstypen – *Managementaktionen* und *Datenaktionen*. Besitzer und Beitragender gewähren Managementaktionen (Ressourcen erstellen, Einstellungen ändern), aber Agenten-Operationen erfordern die `agents/write` **Datenaktion**, die nur in den Rollen `Azure AI User`, `Azure AI Developer` oder `Azure AI Owner` enthalten ist. Siehe [Foundry RBAC-Dokumentation](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` bei Ressourcenerstellung

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Ursache:** Sie haben keine Berechtigung, Azure-Ressourcen in diesem Abonnement oder dieser Ressourcengruppe zu erstellen oder zu ändern.

**Lösung:**
1. Bitten Sie Ihren Abonnement-Administrator, Ihnen die Rolle **Beitragender (Contributor)** auf der Ressourcengruppe zuzuweisen, in der sich Ihr Foundry-Projekt befindet.
2. Alternativ lassen Sie das Foundry-Projekt für Sie erstellen und erhalten Sie die Rolle **Azure AI User** auf dem Projekt.

### 1.3 `SubscriptionNotRegistered` für [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Ursache:** Das Azure-Abonnement hat den benötigten Ressourcenanbieter für Foundry nicht registriert.

**Lösung:**

1. Öffnen Sie ein Terminal und führen Sie aus:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Warten Sie, bis die Registrierung abgeschlossen ist (kann 1-5 Minuten dauern):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Erwarten Sie die Ausgabe: `"Registered"`
3. Versuchen Sie es erneut.

---

## 2. Docker-Fehler (nur bei installierter Docker-Version)

> Docker ist für diesen Workshop **optional**. Diese Fehler treten nur auf, wenn Sie Docker Desktop installiert haben und die Foundry-Erweiterung lokal einen Container baut.

### 2.1 Docker-Daemon läuft nicht

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Lösung - Schritt für Schritt:**

1. Finden Sie Docker Desktop im Startmenü (Windows) oder in den Anwendungen (macOS) und starten Sie es.
2. Warten Sie, bis das Docker Desktop-Fenster **"Docker Desktop is running"** zeigt – das dauert meist 30-60 Sekunden.
3. Suchen Sie das Docker-Wal-Symbol im System-Tray (Windows) oder in der Menüleiste (macOS). Fahren Sie mit der Maus darüber, um den Status zu prüfen.
4. Überprüfen Sie im Terminal:
   ```powershell
   docker info
   ```
   Wenn Systeminformationen zu Docker (Server Version, Storage Driver etc.) angezeigt werden, läuft Docker.
5. **Windows-spezifisch:** Wenn Docker immer noch nicht startet:
   - Öffnen Sie Docker Desktop → **Einstellungen** (Zahnrad-Symbol) → **Allgemein**.
   - Aktivieren Sie **Use the WSL 2 based engine**.
   - Klicken Sie auf **Übernehmen & Neustart**.
   - Falls WSL 2 nicht installiert ist, führen Sie `wsl --install` in einer erhöhten PowerShell aus und starten Sie den Rechner neu.
6. Versuchen Sie die Bereitstellung erneut.

### 2.2 Docker-Build schlägt mit Abhängigkeitsfehlern fehl

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Lösung:**
1. Öffnen Sie `requirements.txt` und prüfen Sie alle Paketnamen auf Rechtschreibung.
2. Vergewissern Sie sich, dass die Versionierung korrekt ist:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Testen Sie die Installation zunächst lokal:
   ```bash
   pip install -r requirements.txt
   ```
4. Bei Nutzung eines privaten Paketindex stellen Sie sicher, dass Docker Zugang zum Netzwerk hat.

### 2.3 Container-Plattform stimmt nicht überein (Apple Silicon)

Wenn Sie von einem Apple Silicon Mac (M1/M2/M3/M4) bereitstellen, muss der Container für `linux/amd64` gebaut sein, da Foundrys Container-Laufzeit AMD64 verwendet.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Der Deploy-Befehl der Foundry-Erweiterung handhabt dies in den meisten Fällen automatisch. Bei Architekturfehlern bauen Sie manuell mit dem `--platform`-Flag und kontaktieren das Foundry-Team.

---

## 3. Authentifizierungsfehler

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) kann kein Token abrufen

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Ursache:** Keine der Anmeldeinformationen in der `DefaultAzureCredential`-Kette besitzt ein gültiges Token.

**Lösung - probieren Sie jeden Schritt der Reihenfolge nach aus:**

1. **Neuanmeldung über Azure CLI** (häufigste Lösung):
   ```bash
   az login
   ```
   Ein Browserfenster öffnet sich. Melden Sie sich an und kehren Sie dann zu VS Code zurück.

2. **Setzen Sie das richtige Abonnement:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Wenn dies nicht das richtige Abonnement ist:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Neuanmeldung über VS Code:**
   - Klicken Sie links unten in VS Code auf das **Konten**-Symbol (Person-Symbol).
   - Klicken Sie auf Ihren Kontonamen → **Abmelden**.
   - Klicken Sie erneut auf das Konten-Symbol → **Bei Microsoft anmelden**.
   - Folgen Sie dem Anmeldevorgang im Browser.

4. **Dienstprinzipal (nur CI/CD-Szenarien):**
   - Setzen Sie diese Umgebungsvariablen in Ihrer `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Starten Sie dann Ihren Agent-Prozess neu.

5. **Überprüfen Sie den Token-Cache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Schlägt dies fehl, ist Ihr CLI-Token abgelaufen. Führen Sie erneut `az login` aus.

### 3.2 Token funktioniert lokal, aber nicht in gehosteter Bereitstellung

**Ursache:** Der gehostete Agent nutzt eine systemverwaltete Identität, die sich von Ihren persönlichen Anmeldedaten unterscheidet.

**Lösung:** Dies ist erwartetes Verhalten – die verwaltete Identität wird bei der Bereitstellung automatisch bereitgestellt. Falls der gehostete Agent trotzdem Authentifizierungsfehler bekommt:
1. Prüfen Sie, ob die verwaltete Identität des Foundry-Projekts Zugriff auf die Azure OpenAI-Ressource hat.
2. Überprüfen Sie, ob `PROJECT_ENDPOINT` in `agent.yaml` korrekt ist.

---

## 4. Modellfehler

### 4.1 Modellbereitstellung nicht gefunden

```
Error: Model deployment not found / The specified deployment does not exist
```

**Lösung - Schritt für Schritt:**

1. Öffnen Sie Ihre `.env`-Datei und notieren Sie den Wert von `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Öffnen Sie die **Microsoft Foundry** Seitenleiste in VS Code.
3. Erweitern Sie Ihr Projekt → **Modellbereitstellungen**.
4. Vergleichen Sie den dort angezeigten Bereitstellungsnamen mit dem Wert in Ihrer `.env`.
5. Der Name ist **Groß-/Kleinschreibung beachten** – `gpt-4o` unterscheidet sich von `GPT-4o`.
6. Stimmen die Namen nicht überein, aktualisieren Sie Ihre `.env`, um genau den Namen aus der Seitenleiste zu verwenden.
7. Für gehostete Bereitstellung aktualisieren Sie auch `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modell antwortet mit unerwartetem Inhalt

**Lösung:**
1. Überprüfen Sie die Konstante `EXECUTIVE_AGENT_INSTRUCTIONS` in `main.py`. Stellen Sie sicher, dass sie nicht abgeschnitten oder beschädigt ist.
2. Prüfen Sie die Modelltetemperatur-Einstellung (falls konfigurierbar) – niedrigere Werte erzeugen deterministischere Ausgaben.
3. Vergleichen Sie das eingesetzte Modell (z.B. `gpt-4o` vs. `gpt-4o-mini`) – unterschiedliche Modelle haben unterschiedliche Fähigkeiten.

---

## 5. Fehler bei der Bereitstellung

### 5.1 ACR-Pull-Autorisierung

```
Error: AcrPullUnauthorized
```

**Ursache:** Die verwaltete Identität des Foundry-Projekts kann das Container-Image aus dem Azure Container Registry nicht herunterladen.

**Lösung - Schritt für Schritt:**

1. Öffnen Sie [https://portal.azure.com](https://portal.azure.com).
2. Suchen Sie in der oberen Suchleiste nach **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Klicken Sie auf das Registry, das mit Ihrem Foundry-Projekt verknüpft ist (gewöhnlich in derselben Ressourcengruppe).
4. Klicken Sie in der linken Navigation auf **Zugriffskontrolle (IAM)**.
5. Klicken Sie auf **+ Hinzufügen** → **Rollen-Zuweisung hinzufügen**.
6. Suchen Sie nach **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** und wählen Sie es aus. Klicken Sie auf **Weiter**.
7. Wählen Sie **Verwaltete Identität** → klicken Sie auf **+ Mitglieder auswählen**.
8. Suchen und wählen Sie die verwaltete Identität des Foundry-Projekts aus.
9. Klicken Sie auf **Auswählen** → **Überprüfen + zuweisen** → **Überprüfen + zuweisen**.

> Diese Rollen-Zuweisung wird normalerweise automatisch von der Foundry-Erweiterung eingerichtet. Wenn Sie diesen Fehler sehen, könnte die automatische Einrichtung fehlgeschlagen sein. Sie können auch eine Neu-Bereitstellung versuchen – die Erweiterung versucht die Einrichtung dann erneut.

### 5.2 Agent startet nach Bereitstellung nicht

**Symptome:** Containerstatus bleibt länger als 5 Minuten "Ausstehend" oder zeigt "Fehlgeschlagen".

**Lösung - Schritt für Schritt:**

1. Öffnen Sie die **Microsoft Foundry** Seitenleiste in VS Code.
2. Klicken Sie auf Ihren gehosteten Agenten → wählen Sie die Version aus.
3. Prüfen Sie im Detailbereich unter **Container Details** → suchen Sie nach einem Bereich oder Link zu **Logs**.
4. Lesen Sie die Container-Startprotokolle. Häufige Ursachen:

| Lognachricht | Ursache | Lösung |
|-------------|---------|--------|
| `ModuleNotFoundError: No module named 'xxx'` | Fehlende Abhängigkeit | Fügen Sie diese in `requirements.txt` hinzu und deployen Sie erneut |
| `KeyError: 'PROJECT_ENDPOINT'` | Fehlende Umgebungsvariable | Fügen Sie die Umgebungsvariable in `agent.yaml` unter `env:` hinzu |
| `OSError: [Errno 98] Address already in use` | Portkonflikt | Stellen Sie sicher, dass `agent.yaml` `port: 8088` hat und nur ein Prozess darauf zugreift |
| `ConnectionRefusedError` | Agent hat nicht mit Zuhören begonnen | Prüfen Sie `main.py` - der `from_agent_framework()` Aufruf muss beim Start ausgeführt werden |

5. Beheben Sie das Problem und deployen Sie erneut mit [Modul 6](06-deploy-to-foundry.md).

### 5.3 Bereitstellung läuft ins Zeitlimit

**Lösung:**
1. Prüfen Sie Ihre Internetverbindung – der Docker-Push kann groß sein (>100MB bei der ersten Bereitstellung).
2. Wenn Sie hinter einem Unternehmensproxy sind, stellen Sie sicher, dass die Proxy-Einstellungen in Docker Desktop konfiguriert sind: **Docker Desktop** → **Einstellungen** → **Ressourcen** → **Proxies**.
3. Versuchen Sie es erneut – Netzwerkprobleme können vorübergehende Fehler verursachen.

---

## 6. Schnelle Referenz: RBAC-Rollen

| Rolle | Typischer Umfang | Was sie ermöglicht |
|-------|------------------|--------------------|
| **Azure AI User** | Projekt | Datenaktionen: Agenten bauen, bereitstellen und ausführen (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt oder Konto | Datenaktionen + Projektanlage |
| **Azure AI Owner** | Konto | Vollzugriff + Rollenverwaltung |
| **Azure AI Project Manager** | Projekt | Datenaktionen + Zuweisung der Rolle Azure AI User an andere |
| **Contributor** | Abonnement/RG | Managementaktionen (Ressourcen erstellen/löschen). **Keine Datenaktionen** |
| **Owner** | Abonnement/RG | Managementaktionen + Rollenverwaltung. **Keine Datenaktionen** |
| **Reader** | Beliebig | Nur Lesender Verwaltungszugriff |

> **Wichtig:** `Owner` und `Contributor` enthalten **KEINE** Datenaktionen. Für Agenten-Operationen benötigen Sie immer eine `Azure AI *` Rolle. Die minimal erforderliche Rolle für diesen Workshop ist **Azure AI User** auf **Projektebene**.

---

## 7. Checkliste für Abschluss des Workshops

Verwenden Sie dies als abschließende Bestätigung, dass alles erledigt ist:

| # | Punkt | Modul | Erledigt? |
|---|-------|-------|-----------|
| 1 | Alle Voraussetzungen installiert und überprüft | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit und Foundry-Erweiterungen installiert | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry-Projekt erstellt (oder bestehendes Projekt ausgewählt) | [02](02-create-foundry-project.md) | |
| 4 | Modell bereitgestellt (z. B. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI-Benutzerrolle auf Projektebene zugewiesen | [02](02-create-foundry-project.md) | |
| 6 | Hosted Agent-Projekt eingerichtet (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` mit PROJECT_ENDPOINT und MODEL_DEPLOYMENT_NAME konfiguriert | [04](04-configure-and-code.md) | |
| 8 | Agentenanweisungen in main.py angepasst | [04](04-configure-and-code.md) | |
| 9 | Virtuelle Umgebung erstellt und Abhängigkeiten installiert | [04](04-configure-and-code.md) | |
| 10 | Agent lokal mit F5 oder Terminal getestet (4 Smoke-Tests bestanden) | [05](05-test-locally.md) | |
| 11 | Bereitstellung im Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Containerstatus zeigt „Gestartet“ oder „Läuft“ an | [06](06-deploy-to-foundry.md) | |
| 13 | In VS Code Playground verifiziert (4 Smoke-Tests bestanden) | [07](07-verify-in-playground.md) | |
| 14 | Im Foundry Portal Playground verifiziert (4 Smoke-Tests bestanden) | [07](07-verify-in-playground.md) | |

> **Herzlichen Glückwunsch!** Wenn alle Punkte abgehakt sind, haben Sie den gesamten Workshop abgeschlossen. Sie haben einen Hosted Agent von Grund auf erstellt, lokal getestet, in Microsoft Foundry bereitgestellt und in der Produktion validiert.

---

**Zurück:** [07 - Verify in Playground](07-verify-in-playground.md) · **Start:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:  
Dieses Dokument wurde mithilfe des KI-Übersetzungsdienstes [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir auf Genauigkeit achten, bitten wir zu beachten, dass automatische Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Originalsprache gilt als maßgebliche Quelle. Für wichtige Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->