# Modul 8 - Fejlfinding

Dette modul er en referenceguide for almindelige problemer. Bogmærk den og vend tilbage, når noget går galt.

---

## 1. Tilladelsesfejl

### 1.1 `agents/write` tilladelse nægtet

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Hovedårsag:** Manglende `Azure AI User`-rolle på **projekt**-niveau. Dette er workshopfejl nr. 1.

**Løsning:**
1. Åbn [portal.azure.com](https://portal.azure.com).
2. Søg efter navnet på dit Foundry **projekt** → klik på resultatet af typen **"Microsoft Foundry project"** (IKKE forældre-konto).
3. **Access control (IAM)** → **+ Tilføj** → **Tilføj rolle-tildeling**.
4. Rolle: **Azure AI User** → Næste.
5. Medlemmer: Vælg dig selv → Gennemse + tildel → Gennemse + tildel.
6. **Vent 1–2 minutter** → prøv igen.

> **Hvorfor Owner/Contributor ikke er nok:** Disse roller giver *kun* administrationshandlinger. Agent-operationer kræver `agents/write` *data-handling*, som kun findes i `Azure AI User`, `Azure AI Developer` eller `Azure AI Owner`. Se [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` under oprettelse

**Løsning:** Bed din administrator tildele **Contributor** på ressourcegruppen, eller få dem til at oprette projektet for dig og give dig **Azure AI User** på det.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Vent indtil: "Registreret"
```

---

## 2. Docker-fejl

> Docker er **valgfrit**. Disse gælder kun, hvis Docker Desktop er installeret, og udvidelsen forsøger en lokal build.

### 2.1 Docker daemon kører ikke

**Løsning:** Start Docker Desktop → vent på "kører"-status → verificer med `docker info` → prøv igen.

### 2.2 Build fejler med afhængighedsfejl

**Løsning:** Kontroller stavningen i `requirements.txt`, test lokalt først: `pip install -r requirements.txt`.

### 2.3 Plattformismatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentificeringsfejl

### 3.1 `DefaultAzureCredential` fejler

**Løsning (prøv i rækkefølge):**
1. `az login` (genautentificer)
2. `az account set --subscription "<id>"` (korrekt abonnement)
3. VS Code → Konti → Log ud → Log ind igen
4. Verificer: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token virker lokalt men ikke hostet

**Forventet:** Hostede agenter bruger system-administreret identitet, ikke dine legitimationsoplysninger. Hvis den hostede agent får auth-fejl:
- Verificer at `AZURE_AI_PROJECT_ENDPOINT` i `agent.yaml` er korrekt
- Tjek at projektets administrerede identitet har modeladgang

---

## 4. Model-fejl

### 4.1 Modeludrulning ikke fundet

**Løsning:** Navnet er **case-sensitive**. Sammenlign `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` med det præcise navn i Foundry sidemenu → Models.

### 4.2 Uventet modeloutput

**Løsning:** Gennemgå `AGENT_INSTRUCTIONS` i `main.py` (ikke afkortet?). Prøv en anden model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Udrulningsfejl

### 5.1 ACR pull ikke autoriseret

**Løsning:** Azure Portal → Container Registry → Access control (IAM) → Tilføj **AcrPull**-rolle til Foundry projektets administrerede identitet.

### 5.2 Agent fejler at starte (bliver ved med at være "Pending" eller "Failed")

Tjek container logs i sidemenuen. Almindelige årsager:

| Logbesked | Løsning |
|-------------|-----|
| `ModuleNotFoundError` | Tilføj manglende pakke til `requirements.txt`, udrul igen |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Tilføj miljøvariabel til `agent.yaml` under `environment_variables` |
| `Address already in use` | Sørg for at kun én proces binder til port 8088 |

### 5.3 Udrulning timeout

**Løsning:** Tjek internetforbindelse. Første udrulning skubber >100MB. Bag en proxy? Konfigurer Docker Desktop proxy-indstillinger.

---

## 6. Sti B - Foundry Local

### 6.1 Foundry Local vil ikke starte

| Problem | Løsning |
|-------|-----|
| `foundry: command not found` | Geninstaller: `winget install Microsoft.FoundryLocal` |
| Utilstrækkelige ressourcer | Foundry Local kræver ~4GB RAM fri. Luk andre apps. |
| Modeldownload fejler | Tjek diskplads (modeller er 2–8 GB). Prøv igen: `foundry local models pull <name>` |

### 6.2 Foundry Local model-fejl

| Problem | Løsning |
|-------|-----|
| Langsomme svar | Forventet - lokale modeller kører på CPU medmindre du har en GPU. Vær tålmodig. |
| Dårlig kvalitet output | Prøv en større model hvis din hardware tillader det. `phi-4-mini` er en god balance. |
| Forbindelse nægtet | Verificer Foundry Local kører: `foundry local status`. Genstart om nødvendigt. |

---

## 7. Hurtig reference: RBAC-roller

| Rolle | Omfang | Tildeler |
|------|-------|--------|
| **Azure AI User** | Projekt | Datahandlinger: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Datahandlinger + projektoprettelse |
| **Azure AI Owner** | Konto | Fuld adgang + rolleadministration |
| **Contributor** | Abonnement/RG | Kun administrationshandlinger (**ingen** datahandlinger) |
| **Owner** | Abonnement/RG | Administration + rolle-tildeling (**ingen** datahandlinger) |

---

## 8. Workshop afslutningscheckliste

| # | Punkt | Modul |
|---|------|--------|
| 1 | Forudsætninger installeret og verificeret | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit extension installeret, projekt forbundet (eller Sti B konfigureret) | [01](01-setup.md) |
| 3 | Hosted agent oprettet | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfigureret, instruktioner skrevet, afhængigheder installeret | [03](03-configure-and-code.md) |
| 5 | Agent testet lokalt - 3 funktionelle scenarier bestået | [04](04-test-locally.md) |
| 6 | Udrullet til Foundry (kun Sti A) | [05](05-deploy-to-foundry.md) |
| 7 | Edge-case/sikkerhedstest bestået i skyen (kun Sti A) | [06](06-verify-in-playground.md) |
| 8 | Resumé gennemgået, næste skridt identificeret | [07](07-summary.md) |

---

**Forrige:** [07 - Resumé](07-summary.md) · **Hjem:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->