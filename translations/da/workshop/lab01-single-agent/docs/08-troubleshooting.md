# Modul 8 - Fejlfinding

Dette modul er en referenceguide for alle almindelige problemer, der opstår under workshoppen. Bogmærk det - du vil vende tilbage til det, hver gang noget går galt.

---

## 1. Tilladelsesfejl

### 1.1 `agents/write` tilladelse nægtet

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Grundårsag:** Du har ikke rollen `Azure AI User` på **projekt**-niveau. Dette er den mest almindelige fejl i workshoppen.

**Løsning - trin for trin:**

1. Åbn [https://portal.azure.com](https://portal.azure.com).
2. Skriv navnet på dit **Foundry-projekt** i den øverste søgelinje (f.eks. `workshop-agents`).
3. **Kritisk:** Klik på resultatet, der viser typen **"Microsoft Foundry project"**, IKKE den overordnede konto/hub-ressource. Disse er forskellige ressourcer med forskellige RBAC-omfang.
4. Klik i venstre navigation på projektets side på **Access control (IAM)**.
5. Klik på fanen **Role assignments** for at tjekke, om du allerede har rollen:
   - Søg efter dit navn eller email.
   - Hvis `Azure AI User` allerede er listet → har fejlen en anden årsag (tjek trin 8 nedenfor).
   - Hvis ikke listet → fortsæt med at tilføje den.
6. Klik **+ Add** → **Add role assignment**.
7. På fanen **Role**:
   - Søg efter [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Vælg den fra resultaterne.
   - Klik **Next**.
8. På fanen **Members**:
   - Vælg **User, group, or service principal**.
   - Klik **+ Select members**.
   - Søg efter dit navn eller emailadresse.
   - Vælg dig selv fra resultaterne.
   - Klik **Select**.
9. Klik **Review + assign** → klik **Review + assign** igen.
10. **Vent 1-2 minutter** - RBAC-ændringer tager tid at trænge igennem.
11. Prøv den fejlede operation igen.

> **Hvorfor Owner/Contributor ikke er nok:** Azure RBAC har to typer tilladelser - *management actions* og *data actions*. Owner og Contributor giver management actions (oprette ressourcer, ændre indstillinger), men agent operationer kræver `agents/write` **data action**, som kun er inkluderet i `Azure AI User`, `Azure AI Developer` eller `Azure AI Owner` rollerne. Se [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` under oprettelse af ressourcer

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Grundårsag:** Du har ikke tilladelse til at oprette eller ændre Azure-ressourcer i dette abonnement/ressourcegruppe.

**Løsning:**
1. Bed din abonnementadministrator om at tildele dig rollen **Contributor** på den ressourcegruppe, hvor dit Foundry-projekt ligger.
2. Alternativt kan du bede dem oprette Foundry-projektet for dig og give dig **Azure AI User** på projektet.

### 1.3 `SubscriptionNotRegistered` for [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Grundårsag:** Azure-abonnementet har ikke registreret den nødvendige ressourcetilbyder til Foundry.

**Løsning:**

1. Åbn en terminal og kør:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```

2. Vent på, at registreringen er færdig (kan tage 1-5 minutter):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Forventet output: `"Registered"`
3. Prøv operationen igen.

---

## 2. Docker-fejl (kun hvis Docker er installeret)

> Docker er **valgfrit** til denne workshop. Disse fejl gælder kun, hvis du har Docker Desktop installeret, og Foundry-udvidelsen forsøger en lokal containerbygning.

### 2.1 Docker daemon kører ikke

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Løsning - trin for trin:**

1. **Find Docker Desktop** i din Start-menu (Windows) eller Programmer (macOS) og start det.
2. Vent på, at Docker Desktop-vinduet viser **"Docker Desktop is running"** - det tager typisk 30-60 sekunder.
3. Kig efter Docker-hval-ikonet i systembakken (Windows) eller menulinjen (macOS). Hold musen over for at bekræfte status.
4. Verificer i en terminal:
   ```powershell
   docker info
   ```
   Hvis dette printer Docker systeminformation (Server Version, Storage Driver osv.), kører Docker.
5. **Windows-specifikt:** Hvis Docker stadig ikke vil starte:
   - Åbn Docker Desktop → **Settings** (tandhjulsikon) → **General**.
   - Sørg for, at **Use the WSL 2 based engine** er markeret.
   - Klik **Apply & restart**.
   - Hvis WSL 2 ikke er installeret, kør `wsl --install` i en forhøjet PowerShell og genstart computeren.
6. Prøv udrulningen igen.

### 2.2 Docker build fejler med afhængighedsfejl

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Løsning:**
1. Åbn `requirements.txt` og tjek, at alle pakkenavne er stavet korrekt.
2. Sørg for, at versionsangivelsen er korrekt:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```

3. Test installationen lokalt først:
   ```bash
   pip install -r requirements.txt
   ```

4. Hvis du bruger et privat pakkeindeks, skal du sikre, at Docker har netværksadgang til det.

### 2.3 Container platform mismatch (Apple Silicon)

Hvis du deployerer fra en Apple Silicon Mac (M1/M2/M3/M4), skal containeren bygges til `linux/amd64`, fordi Foundrys containerruntime bruger AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry-udvidelsens deploy-kommando håndterer dette automatisk i de fleste tilfælde. Hvis du ser arkitekturrelaterede fejl, byg manuelt med `--platform` flaget og kontakt Foundry-teamet.

---

## 3. Autentificeringsfejl

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) kan ikke hente en token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Grundårsag:** Ingen af credentials-kilderne i `DefaultAzureCredential` kæden har en gyldig token.

**Løsning - prøv hvert trin i rækkefølge:**

1. **Log ind igen via Azure CLI** (den mest almindelige løsning):
   ```bash
   az login
   ```
   Et browservindue åbner. Log ind og vend tilbage til VS Code.

2. **Sæt det korrekte abonnement:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Hvis det ikke er det rigtige abonnement:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Log ind igen via VS Code:**
   - Klik på **Accounts** ikonet (personikonet) nederst til venstre i VS Code.
   - Klik på dit kontonavn → **Sign Out**.
   - Klik på Accounts-ikonet igen → **Sign in to Microsoft**.
   - Fuldfør browsertilganganmeldelsen.

4. **Service principal (kun CI/CD scenarier):**
   - Sæt disse miljøvariabler i din `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Genstart derefter din agentproces.

5. **Tjek token cache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Hvis dette fejler, er din CLI-token udløbet. Kør `az login` igen.

### 3.2 Token virker lokalt men ikke i hosted deployment

**Grundårsag:** Den hosted agent bruger en system-administreret identitet, som er forskellig fra din personlige credential.

**Løsning:** Dette er forventet opførsel - den administrerede identitet oprettes automatisk under deployment. Hvis den hosted agent stadig får auth-fejl:
1. Tjek, at Foundry-projektets administrerede identitet har adgang til Azure OpenAI-ressourcen.
2. Bekræft, at `PROJECT_ENDPOINT` i `agent.yaml` er korrekt.

---

## 4. Model-fejl

### 4.1 Model deployment ikke fundet

```
Error: Model deployment not found / The specified deployment does not exist
```

**Løsning - trin for trin:**

1. Åbn din `.env` fil og noter værdien af `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Åbn **Microsoft Foundry** sidebaren i VS Code.
3. Udvid dit projekt → **Model Deployments**.
4. Sammenlign deploymentsnavnet der med værdien i din `.env`.
5. Navnet er **case-sensitive** - `gpt-4o` er forskelligt fra `GPT-4o`.
6. Hvis de ikke stemmer overens, opdater din `.env` med det præcise navn vist i sidebaren.
7. For hosted deployment, opdater også `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model svarer med uventet indhold

**Løsning:**
1. Gennemgå konstanten `EXECUTIVE_AGENT_INSTRUCTIONS` i `main.py`. Sørg for, at den ikke er afkortet eller korrumperet.
2. Tjek modeltemperaturindstillingen (hvis konfigurerbar) - lavere værdier giver mere deterministiske output.
3. Sammenlign den deployede model (f.eks. `gpt-4o` vs `gpt-4o-mini`) - forskellige modeller har forskellige kapaciteter.

---

## 5. Deploymentsfejl

### 5.1 ACR pull autorisation

```
Error: AcrPullUnauthorized
```

**Grundårsag:** Foundry-projektets administrerede identitet kan ikke trække container-billedet fra Azure Container Registry.

**Løsning - trin for trin:**

1. Åbn [https://portal.azure.com](https://portal.azure.com).
2. Søg efter **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** i den øverste søgelinje.
3. Klik på registreringen tilknyttet dit Foundry-projekt (typisk i samme ressourcegruppe).
4. Klik i venstre navigation på **Access control (IAM)**.
5. Klik **+ Add** → **Add role assignment**.
6. Søg efter **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** og vælg den. Klik **Next**.
7. Vælg **Managed identity** → klik **+ Select members**.
8. Find og vælg Foundry-projektets administrerede identitet.
9. Klik **Select** → **Review + assign** → **Review + assign**.

> Denne rolle tildeles normalt automatisk af Foundry-udvidelsen. Hvis du ser denne fejl, kan den automatiske opsætning være mislykkedes. Du kan også prøve at udrulle igen - udvidelsen forsøger måske opsætningen igen.

### 5.2 Agenten starter ikke efter deployment

**Symptomer:** Containerstatus forbliver "Pending" i mere end 5 minutter eller viser "Failed".

**Løsning - trin for trin:**

1. Åbn **Microsoft Foundry** sidebaren i VS Code.
2. Klik på din hosted agent → vælg version.
3. I detaljepanelet, tjek **Container Details** → kig efter en **Logs** sektion eller link.
4. Læs containerens opstartslog. Almindelige årsager:

| Log besked | Årsag | Løsning |
|-------------|-------|---------|
| `ModuleNotFoundError: No module named 'xxx'` | Manglende afhængighed | Tilføj den i `requirements.txt` og deploy igen |
| `KeyError: 'PROJECT_ENDPOINT'` | Manglende miljøvariabel | Tilføj env variablen i `agent.yaml` under `env:` |
| `OSError: [Errno 98] Address already in use` | Portkonflikt | Sørg for, at `agent.yaml` har `port: 8088` og kun én proces bruger den |
| `ConnectionRefusedError` | Agenten startede ikke op til at lytte | Tjek `main.py` - `from_agent_framework()` kaldet skal køre ved opstart |

5. Ret problemet, og deploy igen fra [Modul 6](06-deploy-to-foundry.md).

### 5.3 Deployment timeout

**Løsning:**
1. Tjek din internetforbindelse - Docker push kan være stor (>100MB ved første deploy).
2. Hvis du er bag en virksomhedsproxy, skal du sikre, at Docker Desktop proxyindstillinger er konfigureret: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Prøv igen - netværk er ustabilt og kan give midlertidige fejl.

---

## 6. Hurtig reference: RBAC roller

| Rolle | Typisk omfang | Hvad den giver |
|-------|---------------|----------------|
| **Azure AI User** | Projekt | Data actions: bygge, deploye og kalde agenter (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt eller Konto | Data actions + projektoprettelse |
| **Azure AI Owner** | Konto | Fuld adgang + rolle tildelingsstyring |
| **Azure AI Project Manager** | Projekt | Data actions + kan tildele Azure AI User til andre |
| **Contributor** | Abonnement/RG | Management actions (oprette/slette ressourcer). **Inkluderer IKKE data actions** |
| **Owner** | Abonnement/RG | Management actions + rolle tildeling. **Inkluderer IKKE data actions** |
| **Reader** | Alle | Læse-adgang til management |

> **Vigtig pointe:** `Owner` og `Contributor` inkluderer **IKKE** data actions. Du skal altid have en `Azure AI *` rolle for agentoperationer. Minimumsrollen til denne workshop er **Azure AI User** på **projekt**-omfang.

---

## 7. Workshop afslutningscheckliste

Brug denne som en endelig bekræftelse på, at du har gennemført alt:

| # | Punkt | Modul | Bestået? |
|---|-------|-------|----------|
| 1 | Alle forudsætninger installeret og verificeret | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit og Foundry-udvidelser installeret | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry-projekt oprettet (eller eksisterende projekt valgt) | [02](02-create-foundry-project.md) | |
| 4 | Model implementeret (f.eks. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI-brugerrolle tildelt på projektomfang | [02](02-create-foundry-project.md) | |
| 6 | Hosted agent-projekt opsat (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfigureret med PROJECT_ENDPOINT og MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agentinstruktioner tilpasset i main.py | [04](04-configure-and-code.md) | |
| 9 | Virtuelt miljø oprettet og afhængigheder installeret | [04](04-configure-and-code.md) | |
| 10 | Agent testet lokalt med F5 eller terminal (4 røgtest bestået) | [05](05-test-locally.md) | |
| 11 | Udrullet til Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Containerstatus viser "Started" eller "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verificeret i VS Code Playground (4 røgtest bestået) | [07](07-verify-in-playground.md) | |
| 14 | Verificeret i Foundry Portal Playground (4 røgtest bestået) | [07](07-verify-in-playground.md) | |

> **Tillykke!** Hvis alle punkter er afkrydset, har du gennemført hele workshoppen. Du har bygget en hosted agent fra bunden, testet den lokalt, udrullet den til Microsoft Foundry og valideret den i produktion.

---

**Forrige:** [07 - Verify in Playground](07-verify-in-playground.md) · **Hjem:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:  
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør anses for at være den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->