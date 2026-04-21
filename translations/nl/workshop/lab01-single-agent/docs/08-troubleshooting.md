# Module 8 - Problemen oplossen

Deze module is een referentiegids voor elk veelvoorkomend probleem dat tijdens de workshop wordt tegengekomen. Bladwijzer het – je komt er telkens op terug wanneer er iets misgaat.

---

## 1. Machtigingsfouten

### 1.1 `agents/write` toestemming geweigerd

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Oorzaak:** Je hebt niet de rol `Azure AI User` op **project**-niveau. Dit is de meest voorkomende fout in de workshop.

**Oplossing - stap voor stap:**

1. Open [https://portal.azure.com](https://portal.azure.com).
2. Typ in de bovenste zoekbalk de naam van je **Foundry-project** (bijvoorbeeld `workshop-agents`).
3. **Belangrijk:** Klik op het resultaat waarvan het type **"Microsoft Foundry project"** is, NIET het bovenliggende account-/hubresource. Dit zijn verschillende resources met verschillende RBAC-reikwijdten.
4. Klik in de linker navigatie van de projectpagina op **Toegangsbeheer (IAM)**.
5. Klik op het tabblad **Roltoewijzingen** om te controleren of je de rol al hebt:
   - Zoek je naam of e-mailadres.
   - Als `Azure AI User` al vermeld staat → heeft de fout een andere oorzaak (controleer stap 8 hieronder).
   - Als niet vermeld → ga door en voeg het toe.
6. Klik **+ Toevoegen** → **Roltoewijzing toevoegen**.
7. In het tabblad **Rol**:
   - Zoek naar [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Selecteer deze.
   - Klik **Volgende**.
8. In het tabblad **Leden**:
   - Selecteer **Gebruiker, groep of serviceprincipal**.
   - Klik **+ Selecteer leden**.
   - Zoek je naam of e-mailadres.
   - Selecteer jezelf in de resultaten.
   - Klik **Selecteren**.
9. Klik **Controleren + toewijzen** → klik opnieuw op **Controleren + toewijzen**.
10. **Wacht 1-2 minuten** – RBAC-wijzigingen hebben tijd nodig om door te voeren.
11. Probeer de mislukte bewerking opnieuw uit te voeren.

> **Waarom Owner/Contributor niet genoeg is:** Azure RBAC heeft twee soorten machtigingen - *beheeracties* en *gegevensacties*. Owner en Contributor verlenen beheeracties (resources aanmaken, instellingen bewerken), maar agent-acties vereisen de `agents/write` **gegevensactie**, die alleen is opgenomen in `Azure AI User`, `Azure AI Developer` of `Azure AI Owner` rollen. Zie [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` tijdens resource provisioning

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Oorzaak:** Je hebt geen toestemming om Azure-resources te maken of te wijzigen in deze abonnement/resourcegroep.

**Oplossing:**
1. Vraag je abonnementbeheerder om jou de rol **Contributor** toe te wijzen op de resourcegroep waar je Foundry-project zich bevindt.
2. Of vraag hen om het Foundry-project voor je te maken en jou de rol **Azure AI User** op het project te geven.

### 1.3 `SubscriptionNotRegistered` voor [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Oorzaak:** Het Azure-abonnement heeft de benodigde resourceprovider voor Foundry nog niet geregistreerd.

**Oplossing:**

1. Open een terminal en voer uit:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Wacht tot de registratie is voltooid (kan 1-5 minuten duren):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Verwachte output: `"Registered"`
3. Probeer de bewerking opnieuw.

---

## 2. Dockerfouten (alleen als Docker is geïnstalleerd)

> Docker is **optioneel** voor deze workshop. Deze fouten gelden alleen als je Docker Desktop hebt geïnstalleerd en de Foundry-extensie probeert lokaal een container te bouwen.

### 2.1 Docker daemon draait niet

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Oplossing - stap voor stap:**

1. Zoek **Docker Desktop** in je Startmenu (Windows) of Applicaties-map (macOS) en start het op.
2. Wacht tot het Docker Desktop-venster **"Docker Desktop is running"** toont – dit duurt doorgaans 30-60 seconden.
3. Zoek naar het Docker walvissymbool in je systeemvak (Windows) of menubalk (macOS). Houd de muis erop om de status te zien.
4. Controleer in een terminal:
   ```powershell
   docker info
   ```
   Als dit Docker-systeeminformatie (Server Version, Storage Driver, enz.) print, draait Docker.
5. **Specifiek voor Windows:** Als Docker nog steeds niet start:
   - Open Docker Desktop → **Instellingen** (tandwielicoon) → **Algemeen**.
   - Zorg dat **Gebruik de op WSL 2 gebaseerde engine** is aangevinkt.
   - Klik op **Toepassen & herstarten**.
   - Als WSL 2 niet is geïnstalleerd, voer `wsl --install` uit in een verhoogde PowerShell en herstart de computer.
6. Probeer de deployment opnieuw.

### 2.2 Docker build mislukt met afhankelijkheidsfouten

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Oplossing:**
1. Open `requirements.txt` en controleer of alle pakketnamen correct gespeld zijn.
2. Zorg dat de versie-aanduiding (version pinning) klopt:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Test eerst lokaal de installatie:
   ```bash
   pip install -r requirements.txt
   ```
4. Gebruik je een private package index, zorg dat Docker netwerktoegang heeft tot deze index.

### 2.3 Container platform mismatch (Apple Silicon)

Als je vanaf een Apple Silicon Mac (M1/M2/M3/M4) uitrolt, moet de container worden gebouwd voor `linux/amd64` omdat Foundry’s container runtime AMD64 gebruikt.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> De deploy-opdracht van de Foundry-extensie verzorgt dit automatisch in de meeste gevallen. Zie je foutmeldingen over architectuur, bouw dan handmatig met de `--platform` vlag en neem contact op met het Foundry-team.

---

## 3. Authenticatiefouten

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) kan geen token verkrijgen

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Oorzaak:** Geen van de credential-bronnen in de `DefaultAzureCredential` keten heeft een geldig token.

**Oplossing - probeer elke stap op volgorde:**

1. **Login opnieuw via Azure CLI** (meest voorkomende oplossing):
   ```bash
   az login
   ```
   Er opent een browservenster. Log in en ga daarna terug naar VS Code.

2. **Zet het juiste abonnement:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Als dit niet het juiste abonnement is:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Login opnieuw via VS Code:**
   - Klik onderin links op het **Accounts** icoon (persoon).
   - Klik op je accountnaam → **Uitloggen**.
   - Klik opnieuw op het Accounts-icoon → **Aanmelden bij Microsoft**.
   - Voltooi de aanmeldprocedure in de browser.

4. **Service principal (alleen bij CI/CD scenario’s):**
   - Zet deze omgevingsvariabelen in je `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Herstart daarna je agentproces.

5. **Controleer tokencache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Als dit mislukt, is je CLI-token verlopen. Voer opnieuw `az login` uit.

### 3.2 Token werkt lokaal maar niet bij gehoste deployment

**Oorzaak:** De gehoste agent gebruikt een system-managed identity, die anders is dan je persoonlijke credential.

**Oplossing:** Dit is verwacht gedrag - de managed identity wordt automatisch aangemaakt bij deployment. Als de gehoste agent toch authenticatiefouten krijgt:
1. Controleer of de managed identity van het Foundry-project toegang heeft tot de Azure OpenAI-resource.
2. Controleer of `PROJECT_ENDPOINT` in `agent.yaml` correct is.

---

## 4. Modelfouten

### 4.1 Modeldeployment niet gevonden

```
Error: Model deployment not found / The specified deployment does not exist
```

**Oplossing - stap voor stap:**

1. Open je `.env` bestand en noteer de waarde van `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Open de **Microsoft Foundry** zijbalk in VS Code.
3. Vouw je project uit → **Model Deployments**.
4. Vergelijk de daarin vermelde deploymentnaam met de waarde in je `.env`.
5. De naam is **hoofdlettergevoelig** – `gpt-4o` is anders dan `GPT-4o`.
6. Komt het niet overeen? Pas dan je `.env` aan met de exacte naam die in de zijbalk staat.
7. Werk bij gehoste deployment ook `agent.yaml` bij:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model reageert met onverwachte inhoud

**Oplossing:**
1. Bekijk de constante `EXECUTIVE_AGENT_INSTRUCTIONS` in `main.py`. Controleer of deze niet is ingekort of beschadigd.
2. Controleer de modeltemperatuurinstelling (indien configureerbaar) – lagere waarden geven meer deterministische uitkomsten.
3. Vergelijk het gebruikte model (bijvoorbeeld `gpt-4o` versus `gpt-4o-mini`) – verschillende modellen hebben verschillende capaciteiten.

---

## 5. Deploymentfouten

### 5.1 ACR pull authorisatie

```
Error: AcrPullUnauthorized
```

**Oorzaak:** De managed identity van het Foundry-project kan de containerafbeelding niet ophalen uit Azure Container Registry.

**Oplossing - stap voor stap:**

1. Open [https://portal.azure.com](https://portal.azure.com).
2. Zoek naar **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** in de bovenste zoekbalk.
3. Klik op de registry die bij je Foundry-project hoort (meestal in dezelfde resourcegroep).
4. Klik in de linker navigatie op **Toegangsbeheer (IAM)**.
5. Klik **+ Toevoegen** → **Roltoewijzing toevoegen**.
6. Zoek en selecteer **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Klik **Volgende**.
7. Selecteer **Managed identity** → klik **+ Selecteer leden**.
8. Zoek en selecteer de managed identity van het Foundry-project.
9. Klik **Selecteren** → **Controleren + toewijzen** → **Controleren + toewijzen**.

> Deze roltoewijzing wordt normaal gesproken automatisch aangemaakt door de Foundry-extensie. Zie je deze fout, dan is die automatische setup mogelijk mislukt. Je kunt ook proberen opnieuw te deployen – de extensie probeert de setup opnieuw.

### 5.2 Agent start niet na deployment

**Symptomen:** Containerstatus blijft langer dan 5 minuten op "Pending" staan of toont "Failed".

**Oplossing - stap voor stap:**

1. Open de **Microsoft Foundry** zijbalk in VS Code.
2. Klik op je gehoste agent → selecteer de versie.
3. Bekijk in het detailpaneel **Container Details** → zoek naar een **Logs**-sectie of link.
4. Lees de container startup logs. Veelvoorkomende oorzaken:

| Logmelding | Oorzaak | Oplossing |
|------------|---------|-----------|
| `ModuleNotFoundError: No module named 'xxx'` | Ontbrekende afhankelijkheid | Voeg toe in `requirements.txt` en deploy opnieuw |
| `KeyError: 'PROJECT_ENDPOINT'` | Ontbrekende omgevingsvariabele | Voeg de env var toe in `agent.yaml` onder `env:` |
| `OSError: [Errno 98] Address already in use` | Poortconflict | Zorg dat `agent.yaml` `port: 8088` heeft en dat er maar één proces bindt aan deze poort |
| `ConnectionRefusedError` | Agent luistert niet | Controleer `main.py` – de `from_agent_framework()` oproep moet bij opstarten draaien |

5. Los het probleem op en deploy opnieuw volgens [Module 6](06-deploy-to-foundry.md).

### 5.3 Deployment time-out

**Oplossing:**
1. Controleer je internetverbinding – de Docker push kan groot zijn (>100MB voor de eerste deployment).
2. Staat je achter een bedrijfsproxy? Zorg dat de proxy-instellingen in Docker Desktop zijn geconfigureerd: **Docker Desktop** → **Instellingen** → **Resources** → **Proxies**.
3. Probeer opnieuw – netwerkstoringen kunnen tijdelijke fouten veroorzaken.

---

## 6. Snelle referentie: RBAC-rollen

| Rol | Typische reikwijdte | Wat het verleent |
|-----|---------------------|------------------|
| **Azure AI User** | Project | Gegevensacties: bouwen, deployen en aanroepen van agents (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Project of Account | Gegevensacties + project aanmaken |
| **Azure AI Owner** | Account | Volledige toegang + rolbeheer |
| **Azure AI Project Manager** | Project | Gegevensacties + kan Azure AI User aan anderen toewijzen |
| **Contributor** | Abonnement/RG | Beheeracties (resources maken/verwijderen). **Bevat GEEN gegevensacties** |
| **Owner** | Abonnement/RG | Beheeracties + rolbeheer. **Bevat GEEN gegevensacties** |
| **Reader** | Elk | Alleen-lezen beheer toegang |

> **Belangrijk:** `Owner` en `Contributor` bevatten GEEN gegevensacties. Je hebt altijd een `Azure AI *` rol nodig voor agentacties. De minimale rol voor deze workshop is **Azure AI User** op **project**-niveau.

---

## 7. Workshop afrondingschecklist

Gebruik dit als een laatste controle dat je alles hebt voltooid:

| # | Item | Module | Behaald? |
|---|------|--------|----------|
| 1 | Alle vereisten geïnstalleerd en geverifieerd | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit en Foundry extensies geïnstalleerd | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry project aangemaakt (of bestaand project geselecteerd) | [02](02-create-foundry-project.md) | |
| 4 | Model ingezet (bijv. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI-gebruikersrol toegewezen op projectniveau | [02](02-create-foundry-project.md) | |
| 6 | Gehoste agentproject gescaffold (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` geconfigureerd met PROJECT_ENDPOINT en MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agentinstructies aangepast in main.py | [04](04-configure-and-code.md) | |
| 9 | Virtuele omgeving aangemaakt en afhankelijkheden geïnstalleerd | [04](04-configure-and-code.md) | |
| 10 | Agent lokaal getest met F5 of terminal (4 smokes tests geslaagd) | [05](05-test-locally.md) | |
| 11 | Ingezet naar Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Containerstatus toont "Started" of "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Gecontroleerd in VS Code Playground (4 smokes tests geslaagd) | [07](07-verify-in-playground.md) | |
| 14 | Gecontroleerd in Foundry Portal Playground (4 smokes tests geslaagd) | [07](07-verify-in-playground.md) | |

> **Gefeliciteerd!** Als alle items zijn aangevinkt, heb je de hele workshop voltooid. Je hebt een gehoste agent vanaf nul gebouwd, lokaal getest, ingezet naar Microsoft Foundry en gevalideerd in productie.

---

**Vorige:** [07 - Verifiëren in Playground](07-verify-in-playground.md) · **Start:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsdienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat automatische vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->