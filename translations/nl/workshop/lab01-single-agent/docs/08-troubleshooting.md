# Module 8 - Problemen oplossen

Deze module is een referentiegids voor veelvoorkomende problemen. Blader deze bladwijzer en kom terug als er iets misgaat.

---

## 1. Machtigingsfouten

### 1.1 `agents/write` toestemming geweigerd

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Oorzaak:** Ontbrekende `Azure AI User` rol op het **project** niveau. Dit is de #1 fout in de workshop.

**Oplossing:**
1. Open [portal.azure.com](https://portal.azure.com).
2. Zoek naar de naam van je Foundry **project** → klik op het resultaat van het type **"Microsoft Foundry project"** (NIET het bovenliggende account).
3. **Toegangscontrole (IAM)** → **+ Toevoegen** → **Roltoewijzing toevoegen**.
4. Rol: **Azure AI User** → Volgende.
5. Leden: Selecteer jezelf → Controleren + toewijzen → Controleren + toewijzen.
6. **Wacht 1–2 minuten** → probeer opnieuw.

> **Waarom eigenaar/bijdrager niet genoeg is:** Deze rollen verlenen alleen *beheer* acties. Agent acties vereisen de `agents/write` *data actie*, die alleen in `Azure AI User`, `Azure AI Developer`, of `Azure AI Owner` zit. Zie [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` tijdens provisioning

**Oplossing:** Vraag je beheerder om **Contributor** toe te wijzen op de resourcegroep, of laat hen het project voor je aanmaken en je **Azure AI User** geven.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wacht tot: "Geregistreerd"
```

---

## 2. Docker fouten

> Docker is **optioneel**. Dit geldt alleen als Docker Desktop is geïnstalleerd en de extensie probeert lokaal te bouwen.

### 2.1 Docker daemon draait niet

**Oplossing:** Start Docker Desktop → wacht tot status "running" → verifieer met `docker info` → probeer opnieuw.

### 2.2 Build mislukt met afhankelijkheidsfouten

**Oplossing:** Controleer de spelling van `requirements.txt`, test lokaal eerst: `pip install -r requirements.txt`.

### 2.3 Platform mismatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Authenticatiefouten

### 3.1 `DefaultAzureCredential` faalt

**Oplossing (probeer in volgorde):**
1. `az login` (her-authenticeren)
2. `az account set --subscription "<id>"` (juiste abonnement)
3. VS Code → Accounts → Afmelden → opnieuw aanmelden
4. Verifieer: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token werkt lokaal maar niet gehost

**Verwachting:** Gehoste agents gebruiken systeem-beheerde identiteit, niet je eigen inloggegevens. Als de gehoste agent authenticatiefouten krijgt:
- Controleer of `AZURE_AI_PROJECT_ENDPOINT` in `agent.yaml` correct is
- Controleer dat de beheerde identiteit van het project modeltoegang heeft

---

## 4. Modelfouten

### 4.1 Model deployment niet gevonden

**Oplossing:** De naam is **hoofdlettergevoelig**. Vergelijk `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` met de exacte naam in de Foundry zijbalk → Modellen.

### 4.2 Onverwachte modeloutput

**Oplossing:** Bekijk `AGENT_INSTRUCTIONS` in `main.py` (niet afgekapt?). Probeer een ander model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Deployment fouten

### 5.1 ACR pull niet gemachtigd

**Oplossing:** Azure Portal → Container Registry → Toegangscontrole (IAM) → Voeg **AcrPull** rol toe aan de beheerde identiteit van het Foundry project.

### 5.2 Agent start niet (blijft "Pending" of "Failed")

Controleer de container logs in de zijbalk. Veelvoorkomende oorzaken:

| Logbericht | Oplossing |
|-------------|-----|
| `ModuleNotFoundError` | Voeg het ontbrekende pakket toe aan `requirements.txt`, herdeployen |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Voeg env var toe aan `agent.yaml` onder `environment_variables` |
| `Address already in use` | Zorg dat slechts één proces naar poort 8088 luistert |

### 5.3 Deployment time-out

**Oplossing:** Controleer je internetverbinding. De eerste deploy uploadt >100MB. Zit je achter een proxy? Stel Docker Desktop proxy instellingen in.

---

## 6. Pad B - Foundry Local

### 6.1 Foundry Local wil niet starten

| Probleem | Oplossing |
|-------|-----|
| `foundry: command not found` | Herinstalleer: `winget install Microsoft.FoundryLocal` |
| Onvoldoende resources | Foundry Local heeft ~4GB RAM vrij nodig. Sluit andere apps. |
| Model download mislukt | Controleer schijfruimte (modellen zijn 2–8 GB). Probeer opnieuw: `foundry local models pull <name>` |

### 6.2 Foundry Local modelfouten

| Probleem | Oplossing |
|-------|-----|
| Trage reacties | Verwacht - lokale modellen draaien op CPU tenzij je een GPU hebt. Heb geduld. |
| Slechte outputkwaliteit | Probeer een groter model als je hardware het toelaat. `phi-4-mini` is een goede balans. |
| Verbinding geweigerd | Controleer of Foundry Local draait: `foundry local status`. Herstart indien nodig. |

---

## 7. Snelle referentie: RBAC-rollen

| Rol | Reikwijdte | Verleent |
|------|-------|--------|
| **Azure AI User** | Project | Data acties: `agents/write`, `agents/read` |
| **Azure AI Developer** | Project/Account | Data acties + project creatie |
| **Azure AI Owner** | Account | Volledige toegang + rolbeheer |
| **Contributor** | Abonnement/RG | Alleen beheeracties (**geen** data acties) |
| **Owner** | Abonnement/RG | Beheer + roltoewijzing (**geen** data acties) |

---

## 8. Workshop voltooiingschecklist

| # | Item | Module |
|---|------|--------|
| 1 | Vereisten geïnstalleerd en geverifieerd | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit extensie geïnstalleerd, project verbonden (of Pad B geconfigureerd) | [01](01-setup.md) |
| 3 | Gehoste agent opgezet | [02](02-create-hosted-agent.md) |
| 4 | `.env` geconfigureerd, instructies geschreven, afhankelijkheden geïnstalleerd | [03](03-configure-and-code.md) |
| 5 | Agent lokaal getest - 3 functionele scenario's geslaagd | [04](04-test-locally.md) |
| 6 | Uitgevoerd naar Foundry (alleen Pad A) | [05](05-deploy-to-foundry.md) |
| 7 | Randgeval/veiligheidstests geslaagd in cloud (alleen Pad A) | [06](06-verify-in-playground.md) |
| 8 | Samenvatting herzien, volgende stappen geïdentificeerd | [07](07-summary.md) |

---

**Vorige:** [07 - Samenvatting](07-summary.md) · **Start:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->