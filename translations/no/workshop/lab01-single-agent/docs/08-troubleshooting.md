# Modul 8 - Feilsøking

Denne modulen er en referanseguide for alle vanlige problemer som oppstår under workshoppen. Bokmerk den – du vil komme tilbake til den når noe går galt.

---

## 1. Tillatelsesfeil

### 1.1 `agents/write` tillatelse nektet

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Hovedårsak:** Du har ikke rollen `Azure AI User` på **prosjektnivå**. Dette er den vanligste feilen i workshoppen.

**Løsning - steg for steg:**

1. Åpne [https://portal.azure.com](https://portal.azure.com).
2. Skriv inn navnet på ditt **Foundry-prosjekt** (f.eks. `workshop-agents`) i søkefeltet øverst.
3. **Kritisk:** Klikk resultatet som viser type **"Microsoft Foundry project"**, ikke den overordnede konto-/hub-ressursen. Dette er ulike ressurser med forskjellige RBAC-områder.
4. I venstre navigasjon på prosjektets side, klikk **Access control (IAM)**.
5. Klikk fanen **Role assignments** for å sjekke om du allerede har rollen:
   - Søk etter ditt navn eller e-post.
   - Hvis `Azure AI User` allerede står oppført → feilen har en annen årsak (sjekk steg 8 under).
   - Hvis ikke oppført → gå videre til å legge den til.
6. Klikk **+ Add** → **Add role assignment**.
7. I fanen **Role**:
   - Søk etter [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Velg den fra resultatene.
   - Klikk **Next**.
8. I fanen **Members**:
   - Velg **User, group, or service principal**.
   - Klikk **+ Select members**.
   - Søk etter ditt navn eller e-postadresse.
   - Velg deg selv fra resultatene.
   - Klikk **Select**.
9. Klikk **Review + assign** → deretter **Review + assign** igjen.
10. **Vent 1-2 minutter** – RBAC-endringer tar tid å gjennomføre.
11. Prøv operasjonen som feilet på nytt.

> **Hvorfor Owner/Contributor ikke er nok:** Azure RBAC har to typer tillatelser - *administrasjonshandlinger* og *datahandlinger*. Owner og Contributor gir tilgang til administrasjonshandlinger (lage ressurser, endre innstillinger), men agentoperasjoner krever `agents/write` **datahandling**, som kun finnes i rollene `Azure AI User`, `Azure AI Developer` eller `Azure AI Owner`. Se [Foundry RBAC-dokumentasjon](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` under ressursoppretting

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Hovedårsak:** Du har ikke tillatelse til å opprette eller endre Azure-ressurser i dette abonnementet/ressursgruppen.

**Løsning:**
1. Be administratoren for abonnementet om å tildele deg rollen **Contributor** på ressursgruppen hvor Foundry-prosjektet ditt ligger.
2. Alternativt, be dem opprette Foundry-prosjektet for deg og gi deg **Azure AI User** på prosjektet.

### 1.3 `SubscriptionNotRegistered` for [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Hovedårsak:** Azure-abonnementet har ikke registrert ressursleverandøren som trengs for Foundry.

**Løsning:**

1. Åpne en terminal og kjør:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Vent til registreringen er fullført (kan ta 1-5 minutter):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Forventet utdata: `"Registered"`
3. Prøv operasjonen på nytt.

---

## 2. Docker-feil (kun hvis Docker er installert)

> Docker er **valgfritt** for denne workshoppen. Disse feilene gjelder bare hvis du har Docker Desktop installert og Foundry-utvidelsen prøver å bygge en lokal container.

### 2.1 Docker daemon kjører ikke

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Løsning - steg for steg:**

1. Finn Docker Desktop i Start-menyen (Windows) eller Programmer (macOS) og start den.
2. Vent til Docker Desktop-vinduet viser **"Docker Desktop is running"** – dette tar vanligvis 30-60 sekunder.
3. Se etter Docker-hvalikonet i systemstatusfeltet (Windows) eller menylinjen (macOS). Hold musepekeren over det for å bekrefte status.
4. Verifiser i en terminal:
   ```powershell
   docker info
   ```
   Hvis dette viser Docker systeminformasjon (Server Version, Storage Driver osv.), kjører Docker.
5. **Windows-spesifikt:** Hvis Docker fortsatt ikke starter:
   - Åpne Docker Desktop → **Settings** (tannhjul-ikon) → **General**.
   - Sørg for at **Use the WSL 2 based engine** er kryssavklart.
   - Klikk **Apply & restart**.
   - Hvis WSL 2 ikke er installert, kjør `wsl --install` i en opphøyd PowerShell og start maskinen på nytt.
6. Prøv distribusjonen på nytt.

### 2.2 Docker build feiler med avhengighetsfeil

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Løsning:**
1. Åpne `requirements.txt` og forsikre deg om at alle pakkenavn er skrevet riktig.
2. Sørg for at versjonspinningen er korrekt:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Test installasjonen lokalt først:
   ```bash
   pip install -r requirements.txt
   ```
4. Hvis du bruker en privat pakkeregister, må du sikre at Docker har nettverkstilgang til det.

### 2.3 Containerplattform-mismatch (Apple Silicon)

Ved distribusjon fra en Apple Silicon Mac (M1/M2/M3/M4), må containeren bygges for `linux/amd64` fordi Foundrys containermotor bruker AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry-utvidelsens deploy-kommando håndterer dette automatisk i de fleste tilfeller. Hvis du ser arkitekturrelaterte feil, bygg manuelt med `--platform` flagget og kontakt Foundry-teamet.

---

## 3. Autentiseringsfeil

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) klarer ikke hente en token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Hovedårsak:** Ingen av legitimasjonskildene i `DefaultAzureCredential` kjeden har en gyldig token.

**Løsning - prøv hvert steg i rekkefølge:**

1. **Logg inn på nytt via Azure CLI** (vanligste løsning):
   ```bash
   az login
   ```
   Et nettleservindu åpnes. Logg inn, og gå deretter tilbake til VS Code.

2. **Sett riktig abonnement:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Hvis dette ikke er riktig abonnement:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Logg inn på nytt via VS Code:**
   - Klikk på **Accounts**-ikonet (person-ikon) nederst til venstre i VS Code.
   - Klikk på kontonavnet ditt → **Sign Out**.
   - Klikk på kontoikonet igjen → **Sign in to Microsoft**.
   - Fullfør innloggingsflyten i nettleseren.

4. **Service principal (kun CI/CD-scenarier):**
   - Sett disse miljøvariablene i `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Start deretter agent-prosessen på nytt.

5. **Sjekk token-cachen:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Hvis dette feiler, har CLI-token din utløpt. Kjør `az login` på nytt.

### 3.2 Token fungerer lokalt, men ikke i hostet distribusjon

**Hovedårsak:** Den hostede agenten bruker en systemadministrert identitet, som er forskjellig fra dine personlige legitimasjoner.

**Løsning:** Dette er forventet oppførsel – den administrerte identiteten opprettes automatisk under distribusjonen. Hvis den hostede agenten fortsatt får autentiseringsfeil:
1. Sjekk at Foundry-prosjektets administrerte identitet har tilgang til Azure OpenAI-ressursen.
2. Verifiser at `PROJECT_ENDPOINT` i `agent.yaml` er korrekt.

---

## 4. Modellfeil

### 4.1 Modellutrulling ikke funnet

```
Error: Model deployment not found / The specified deployment does not exist
```

**Løsning - steg for steg:**

1. Åpne `.env`-filen og noter verdien for `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Åpne **Microsoft Foundry**-sidemenyen i VS Code.
3. Utvid prosjektet ditt → **Model Deployments**.
4. Sammenlign utrullingsnavnet der med verdien i `.env`.
5. Navnet er **case-sensitivt** – `gpt-4o` er forskjellig fra `GPT-4o`.
6. Hvis de ikke stemmer overens, oppdater `.env` til å bruke nøyaktig navnet som vises i sidemenyen.
7. For hostet distribusjon, oppdater også `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modell svarer med uventet innhold

**Løsning:**
1. Gjennomgå konstanten `EXECUTIVE_AGENT_INSTRUCTIONS` i `main.py`. Sørg for at den ikke er trunkert eller korrupt.
2. Sjekk modellens temperaturinnstilling (hvis konfigurerbar) – lavere verdier gir mer deterministiske utdata.
3. Sammenlign den deployerte modellen (f.eks. `gpt-4o` vs `gpt-4o-mini`) – forskjellige modeller har ulike egenskaper.

---

## 5. Distribusjonsfeil

### 5.1 ACR pull-autorisering

```
Error: AcrPullUnauthorized
```

**Hovedårsak:** Foundry-prosjektets administrerte identitet kan ikke hente containerbildet fra Azure Container Registry.

**Løsning - steg for steg:**

1. Åpne [https://portal.azure.com](https://portal.azure.com).
2. Søk etter **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** i søkefeltet øverst.
3. Klikk på registeret tilknyttet Foundry-prosjektet ditt (typisk i samme ressursgruppe).
4. I venstre navigasjon, klikk **Access control (IAM)**.
5. Klikk **+ Add** → **Add role assignment**.
6. Søk etter **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** og velg den. Klikk **Next**.
7. Velg **Managed identity** → klikk **+ Select members**.
8. Finn og velg Foundry-prosjektets administrerte identitet.
9. Klikk **Select** → **Review + assign** → **Review + assign**.

> Denne rollefordelingen settes normalt automatisk opp av Foundry-utvidelsen. Hvis du ser denne feilen, kan den automatiske oppsettet ha feilet. Du kan også prøve å distribuere på nytt – utvidelsen kan forsøke oppsettet på nytt.

### 5.2 Agent starter ikke etter distribusjon

**Symptomer:** Containerstatus står på "Pending" i mer enn 5 minutter eller viser "Failed".

**Løsning - steg for steg:**

1. Åpne **Microsoft Foundry**-sidemenyen i VS Code.
2. Klikk på din hostede agent → velg versjonen.
3. I detaljpanelet, sjekk **Container Details** → se etter en **Logs** seksjon eller lenke.
4. Les container-startloggene. Vanlige årsaker:

| Loggmelding | Årsak | Løsning |
|-------------|-------|---------|
| `ModuleNotFoundError: No module named 'xxx'` | Manglende avhengighet | Legg den til i `requirements.txt` og distribuer på nytt |
| `KeyError: 'PROJECT_ENDPOINT'` | Manglende miljøvariabel | Legg til miljøvariabelen i `agent.yaml` under `env:` |
| `OSError: [Errno 98] Address already in use` | Portkonflikt | Sørg for at `agent.yaml` har `port: 8088` og at kun én prosess binder den |
| `ConnectionRefusedError` | Agenten startet ikke å lytte | Sjekk `main.py` - `from_agent_framework()` må kjøre ved oppstart |

5. Rett opp feilen, og distribuer på nytt fra [Modul 6](06-deploy-to-foundry.md).

### 5.3 Distribusjon tidsavbrytes

**Løsning:**
1. Sjekk internettforbindelsen din – Docker push kan være stor (>100MB ved første distribusjon).
2. Hvis du er bak en bedriftsproxy, sørg for at Docker Desktop proxy-innstillinger er konfigurert: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Prøv igjen – nettverksforstyrrelser kan forårsake midlertidige feil.

---

## 6. Hurtigreferanse: RBAC-roller

| Rolle | Typisk omfang | Hva den gir |
|-------|---------------|-------------|
| **Azure AI User** | Prosjekt | Datahandlinger: bygg, distribuer og kall agenter (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Prosjekt eller konto | Datahandlinger + prosjektoppretting |
| **Azure AI Owner** | Konto | Full tilgang + rolleadministrasjon |
| **Azure AI Project Manager** | Prosjekt | Datahandlinger + kan tildele Azure AI User til andre |
| **Contributor** | Abonnement/RG | Administrasjonshandlinger (opprette/slette ressurser). **Inkluderer IKKE datahandlinger** |
| **Owner** | Abonnement/RG | Administrasjonshandlinger + rolleadministrasjon. **Inkluderer IKKE datahandlinger** |
| **Reader** | Alle | Kun lesetilgang til administrasjon |

> **Hovedpoeng:** `Owner` og `Contributor` inkluderer **IKKE** datahandlinger. Du trenger alltid en `Azure AI *`-rolle for agentoperasjoner. Minimumsrollen for denne workshoppen er **Azure AI User** på **prosjektnivå**.

---

## 7. Sjekkliste for gjennomføring av workshop

Bruk denne som en siste sjekk for at du har fullført alt:

| # | Element | Modul | Godkjent? |
|---|---------|-------|-----------|
| 1 | Alle forutsetninger installert og verifisert | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit og Foundry-utvidelser installert | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry-prosjekt opprettet (eller eksisterende prosjekt valgt) | [02](02-create-foundry-project.md) | |
| 4 | Modell distribuert (f.eks. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI-brukerrolle tildelt på prosjektomfang | [02](02-create-foundry-project.md) | |
| 6 | Hosted agent prosjekt skaffolder (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfigurert med PROJECT_ENDPOINT og MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Agentinstruksjoner tilpasset i main.py | [04](04-configure-and-code.md) | |
| 9 | Virtuelt miljø opprettet og avhengigheter installert | [04](04-configure-and-code.md) | |
| 10 | Agent testet lokalt med F5 eller terminal (4 røyktester bestått) | [05](05-test-locally.md) | |
| 11 | Distribuert til Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Containerstatus viser "Started" eller "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verifisert i VS Code Playground (4 røyktester bestått) | [07](07-verify-in-playground.md) | |
| 14 | Verifisert i Foundry Portal Playground (4 røyktester bestått) | [07](07-verify-in-playground.md) | |

> **Gratulerer!** Hvis alle punktene er avkrysset, har du fullført hele workshoppen. Du har bygget en hosted agent fra bunnen av, testet den lokalt, distribuert den til Microsoft Foundry, og validert den i produksjon.

---

**Forrige:** [07 - Verifiser i Playground](07-verify-in-playground.md) · **Hjem:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:  
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vennligst vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det originale dokumentet på dets opprinnelige språk bør betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->