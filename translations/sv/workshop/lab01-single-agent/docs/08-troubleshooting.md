# Modul 8 - Felsökning

Denna modul är en referensguide för varje vanligt problem som uppstår under workshopen. Bokmärk den – du kommer att återkomma till den när något går fel.

---

## 1. Behörighetsfel

### 1.1 `agents/write` behörighet nekad

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Rotorsak:** Du har inte rollen `Azure AI User` på **projekt**-nivå. Detta är det mest vanliga felet i workshopen.

**Åtgärd - steg för steg:**

1. Öppna [https://portal.azure.com](https://portal.azure.com).
2. Skriv namnet på ditt **Foundry-projekt** (t.ex. `workshop-agents`) i sökfältet högst upp.
3. **Viktigt:** Klicka på resultatet som visar typ **"Microsoft Foundry project"**, INTE överordnad konto-/hub-resurs. Detta är olika resurser med olika RBAC-omfattning.
4. I navigationsmenyn till vänster på projektsidan klickar du på **Access control (IAM)**.
5. Klicka på fliken **Role assignments** för att kontrollera om du redan har rollen:
   - Sök på ditt namn eller e-post.
   - Om `Azure AI User` redan listas → orsaken är en annan (se steg 8 nedan).
   - Om den inte listas → fortsätt för att lägga till den.
6. Klicka på **+ Add** → **Add role assignment**.
7. I fliken **Role**:
   - Sök efter [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Välj den i resultaten.
   - Klicka på **Next**.
8. I fliken **Members**:
   - Välj **User, group, or service principal**.
   - Klicka på **+ Select members**.
   - Sök efter ditt namn eller e-postadress.
   - Välj dig själv i resultaten.
   - Klicka på **Select**.
9. Klicka på **Review + assign** → **Review + assign** igen.
10. **Vänta 1-2 minuter** - RBAC-ändringar tar tid att sprida sig.
11. Försök igen med operationen som misslyckades.

> **Varför Owner/Contributor inte räcker:** Azure RBAC har två typer av behörigheter – *management actions* och *data actions*. Owner och Contributor ger management actions (skapa resurser, ändra inställningar), men agent-operationer kräver `agents/write` **data action**, som endast ingår i rollerna `Azure AI User`, `Azure AI Developer` eller `Azure AI Owner`. Se [Foundry RBAC-dokumentationen](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` vid resursprovisionering

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Rotorsak:** Du har inte behörighet att skapa eller ändra Azure-resurser i detta abonnemang/resursgrupp.

**Åtgärd:**
1. Be din abonnemangsadministratör tilldela dig rollen **Contributor** på resursgruppen där ditt Foundry-projekt finns.
2. Alternativt, be dem skapa Foundry-projektet åt dig och ge dig rollen **Azure AI User** på projektet.

### 1.3 `SubscriptionNotRegistered` för [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Rotorsak:** Azure-abonnemanget har inte registrerat resursleverantören som krävs för Foundry.

**Åtgärd:**

1. Öppna en terminal och kör:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Vänta tills registreringen är klar (kan ta 1-5 minuter):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Förväntad utdata: `"Registered"`
3. Försök igen med operationen.

---

## 2. Docker-fel (endast om Docker är installerat)

> Docker är **valfritt** för denna workshop. Dessa fel gäller bara om du har Docker Desktop installerat och Foundry-tillägget försöker göra en lokal container-bygge.

### 2.1 Docker daemon körs inte

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Åtgärd - steg för steg:**

1. **Hitta Docker Desktop** i Start-menyn (Windows) eller i Program (macOS) och starta det.
2. Vänta tills Docker Desktop-fönstret visar **"Docker Desktop is running"** - detta tar vanligtvis 30-60 sekunder.
3. Leta efter Docker-hvalens ikon i systemfältet (Windows) eller menyraden (macOS). Håll musen över ikonen för att kontrollera status.
4. Kontrollera i terminal:
   ```powershell
   docker info
   ```
   Om detta skriver ut Docker-systeminformation (Server Version, Storage Driver, etc.) är Docker igång.
5. **Windows-specifikt:** Om Docker fortfarande inte startar:
   - Öppna Docker Desktop → **Settings** (växelikon) → **General**.
   - Säkerställ att **Use the WSL 2 based engine** är markerad.
   - Klicka på **Apply & restart**.
   - Om WSL 2 inte är installerat, kör `wsl --install` i en upphöjd PowerShell och starta om datorn.
6. Försök distribuera igen.

### 2.2 Docker build misslyckas med beroendefel

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Åtgärd:**
1. Öppna `requirements.txt` och kontrollera att alla paketnamn är korrekt stavade.
2. Säkerställ att versionspinnen är korrekt:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Testa installationen lokalt först:
   ```bash
   pip install -r requirements.txt
   ```
4. Om du använder ett privat paketindex, se till att Docker har nätverksåtkomst till det.

### 2.3 Plattformsmissanpassning för container (Apple Silicon)

Om du distribuerar från en Apple Silicon Mac (M1/M2/M3/M4) måste containern byggas för `linux/amd64` eftersom Foundrys container-runtime använder AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry-tilläggets deploy-kommando hanterar detta automatiskt i de flesta fall. Om du får arkitekturrelaterade fel, bygg manuellt med flaggan `--platform` och kontakta Foundry-teamet.

---

## 3. Autentiseringsfel

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) kan inte hämta en token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Rotorsak:** Ingen av credential-källorna i `DefaultAzureCredential`-kedjan har en giltig token.

**Åtgärd - prova varje steg i ordning:**

1. **Logga in igen via Azure CLI** (vanligaste lösningen):
   ```bash
   az login
   ```
   Ett webbläsarfönster öppnas. Logga in och återgå sedan till VS Code.

2. **Ställ in rätt prenumeration:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Om det inte är rätt prenumeration:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Logga in igen via VS Code:**
   - Klicka på **Accounts**-ikonen (personikon) längst ner till vänster i VS Code.
   - Klicka på ditt kontonamn → **Sign Out**.
   - Klicka på Accounts-ikonen igen → **Sign in to Microsoft**.
   - Slutför inloggningen i webbläsaren.

4. **Service principal (endast CI/CD-scenarier):**
   - Sätt följande miljövariabler i din `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Starta om agent-processen.

5. **Kontrollera token-cache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Om detta misslyckas har din CLI-token gått ut. Kör `az login` igen.

### 3.2 Token fungerar lokalt men inte i hostad distribution

**Rotorsak:** Den hostade agenten använder en systemhanterad identitet, vilket skiljer sig från dina personliga uppgifter.

**Åtgärd:** Detta är förväntat beteende - den hanterade identiteten tilldelas automatiskt vid distribution. Om den hostade agenten ändå får autentiseringsfel:
1. Kontrollera att Foundry-projektets hanterade identitet har åtkomst till Azure OpenAI-resursen.
2. Verifiera att `PROJECT_ENDPOINT` i `agent.yaml` är korrekt.

---

## 4. Modellfel

### 4.1 Modelldistribution hittades inte

```
Error: Model deployment not found / The specified deployment does not exist
```

**Åtgärd - steg för steg:**

1. Öppna din `.env`-fil och notera värdet för `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Öppna **Microsoft Foundry** sidopanelen i VS Code.
3. Expandera ditt projekt → **Model Deployments**.
4. Jämför namnet på distributionen där med värdet i din `.env`.
5. Namnet är **skiftlägeskänsligt** – `gpt-4o` skiljer sig från `GPT-4o`.
6. Om de inte stämmer överens, uppdatera `.env` med exakt det namn som visas i sidopanelen.
7. För hostad distribution, uppdatera även `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modellen svarar med oväntat innehåll

**Åtgärd:**
1. Granska konstanten `EXECUTIVE_AGENT_INSTRUCTIONS` i `main.py`. Kontrollera att den inte är avklippt eller korrupt.
2. Kontrollera modellens temperaturinställning (om konfigurerbar) - lägre värden ger mer deterministiska svar.
3. Jämför den distribuerade modellen (t.ex. `gpt-4o` vs `gpt-4o-mini`) - olika modeller har olika kapabiliteter.

---

## 5. Distributionsfel

### 5.1 ACR pull-behörighet

```
Error: AcrPullUnauthorized
```

**Rotorsak:** Foundry-projektets hanterade identitet kan inte hämta containerbilden från Azure Container Registry.

**Åtgärd - steg för steg:**

1. Öppna [https://portal.azure.com](https://portal.azure.com).
2. Sök efter **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** i sökfältet högst upp.
3. Klicka på det register som är kopplat till ditt Foundry-projekt (vanligtvis i samma resursgrupp).
4. I vänstermenyn klicka på **Access control (IAM)**.
5. Klicka på **+ Add** → **Add role assignment**.
6. Sök efter **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** och välj det. Klicka på **Next**.
7. Välj **Managed identity** → klicka på **+ Select members**.
8. Hitta och välj Foundry-projektets hanterade identitet.
9. Klicka på **Select** → **Review + assign** → **Review + assign**.

> Denna rolltilldelning sätts normalt upp automatiskt av Foundry-tillägget. Om du ser detta fel kan den automatiska inställningen ha misslyckats. Du kan också försöka distribuera på nytt - tillägget kan försöka igen.

### 5.2 Agenten startar inte efter distribution

**Symptom:** Container-statusen står kvar på "Pending" mer än 5 minuter eller visar "Failed".

**Åtgärd - steg för steg:**

1. Öppna **Microsoft Foundry** sidopanel i VS Code.
2. Klicka på din hostade agent → välj version.
3. I detaljpanelen, kontrollera **Container Details** → leta efter en **Logs**-sektion eller länk.
4. Läs startloggarna för containern. Vanliga orsaker:

| Loggmeddelande | Orsak | Åtgärd |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Saknad beroende | Lägg till i `requirements.txt` och distribuera om |
| `KeyError: 'PROJECT_ENDPOINT'` | Saknad miljövariabel | Lägg till env-variabeln i `agent.yaml` under `env:` |
| `OSError: [Errno 98] Address already in use` | Portkonflikt | Säkerställ att `agent.yaml` har `port: 8088` och att endast en process binder den |
| `ConnectionRefusedError` | Agent lyssnar inte | Kontrollera `main.py` - anropet `from_agent_framework()` måste köras vid start |

5. Fixa problemet och distribuera om från [Modul 6](06-deploy-to-foundry.md).

### 5.3 Distributionen tidsbegränsas

**Åtgärd:**
1. Kontrollera din internetanslutning - Docker push kan vara stor (>100MB vid första distribution).
2. Om du är bakom en företagsproxy, kontrollera att proxyinställningarna för Docker Desktop är konfigurerade: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Försök igen - nätverkshaverier kan orsaka temporära fel.

---

## 6. Snabbreferens: RBAC-roller

| Roll | Typisk omfattning | Vad den ger |
|------|-------------------|-------------|
| **Azure AI User** | Projekt | Dataåtgärder: bygga, distribuera och anropa agenter (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt eller Konto | Dataåtgärder + projektskapande |
| **Azure AI Owner** | Konto | Full åtkomst + hantering av rolltilldelningar |
| **Azure AI Project Manager** | Projekt | Dataåtgärder + kan tilldela Azure AI User till andra |
| **Contributor** | Prenumeration/RG | Managementactions (skapa/radera resurser). **Inkluderar INTE dataåtgärder** |
| **Owner** | Prenumeration/RG | Managementactions + rolltilldelning. **Inkluderar INTE dataåtgärder** |
| **Reader** | Alla | Endast läsåtkomst för management |

> **Viktig lärdom:** `Owner` och `Contributor` inkluderar **INTE** dataåtgärder. Du behöver alltid en `Azure AI *`-roll för agentoperationer. Minsta roll för denna workshop är **Azure AI User** på **projekt**-omfattning.

---

## 7. Checklista för workshopslut

Använd denna som slutgiltigt bevis på att du har genomfört allt:

| # | Punkt | Modul | Godkänd? |
|---|-------|-------|----------|
| 1 | Alla förutsättningar installerade och verifierade | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit och Foundry-tillägg installerade | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry-projekt skapat (eller befintligt projekt valt) | [02](02-create-foundry-project.md) | |
| 4 | Modell distribuerad (t.ex., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI-användarroll tilldelad på projektnivå | [02](02-create-foundry-project.md) | |
| 6 | Hosted agent-projekt skapat (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfigurerad med PROJECT_ENDPOINT och MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agentinstruktioner anpassade i main.py | [04](04-configure-and-code.md) | |
| 9 | Virtuellt miljö skapat och beroenden installerade | [04](04-configure-and-code.md) | |
| 10 | Agent testad lokalt med F5 eller terminal (4 röktester godkända) | [05](05-test-locally.md) | |
| 11 | Distribuerad till Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Containerstatus visar "Started" eller "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verifierad i VS Code Playground (4 röktester godkända) | [07](07-verify-in-playground.md) | |
| 14 | Verifierad i Foundry Portal Playground (4 röktester godkända) | [07](07-verify-in-playground.md) | |

> **Grattis!** Om alla punkter är ikryssade har du slutfört hela workshopen. Du har byggt en hosted agent från grunden, testat den lokalt, distribuerat den till Microsoft Foundry och validerat den i produktion.

---

**Föregående:** [07 - Verify in Playground](07-verify-in-playground.md) · **Hem:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:  
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, vänligen observera att automatiska översättningar kan innehålla fel eller brister. Originaldokumentet på dess ursprungsspråk bör anses vara den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår från användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->