# Modul 8 - Feilsøking

Denne modulen er en referanseguide for vanlige problemer. Bokmerk den og kom tilbake når noe går galt.

---

## 1. Tilgangsfeil

### 1.1 `agents/write` tillatelse nektes

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Hovedårsak:** Manglende `Azure AI User`-rolle på **prosjektnivå**. Dette er feil #1 i workshop.

**Løsning:**
1. Åpne [portal.azure.com](https://portal.azure.com).
2. Søk etter navnet på Foundry **prosjektet** ditt → klikk resultatet av typen **"Microsoft Foundry project"** (IKKE overordnet konto).
3. **Tilgangskontroll (IAM)** → **+ Legg til** → **Legg til rolleoppgave**.
4. Rolle: **Azure AI User** → Neste.
5. Medlemmer: Velg deg selv → Gjennomgå + tilordne → Gjennomgå + tilordne.
6. **Vent 1–2 minutter** → prøv igjen.

> **Hvorfor Eier/Bidragsyter ikke er nok:** Disse rollene gir kun *administrative* handlinger. Agentoperasjoner krever `agents/write` *datahandling*, som bare finnes i `Azure AI User`, `Azure AI Developer` eller `Azure AI Owner`. Se [Foundry RBAC-dokumentasjon](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` under provisjonering

**Løsning:** Be administratoren din tilordne **Bidragsyter** på ressursgruppen, eller få dem til å opprette prosjektet for deg og gi deg **Azure AI User** på det.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Vent til: "Registrert"
```

---

## 2. Docker-feil

> Docker er **valgfritt**. Disse gjelder kun hvis Docker Desktop er installert og utvidelsen forsøker en lokal bygging.

### 2.1 Docker daemon kjører ikke

**Løsning:** Start Docker Desktop → vent på status "kjører" → verifiser med `docker info` → prøv igjen.

### 2.2 Bygg feiler med avhengighetsfeil

**Løsning:** Sjekk stavemåten i `requirements.txt`, test lokalt først: `pip install -r requirements.txt`.

### 2.3 Plattformukompatibilitet (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentiseringsfeil

### 3.1 `DefaultAzureCredential` feiler

**Løsning (prøv i rekkefølge):**
1. `az login` (autentiser på nytt)
2. `az account set --subscription "<id>"` (korrekt abonnement)
3. VS Code → Kontoer → Logg ut → Logg inn igjen
4. Verifiser: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token fungerer lokalt men ikke hos host

**Forventet:** Hostede agenter bruker systemadministrert identitet, ikke dine legitimasjoner. Hvis hostet agent får autentiseringsfeil:
- Verifiser at `AZURE_AI_PROJECT_ENDPOINT` i `agent.yaml` er korrekt
- Sjekk at prosjektets administrerte identitet har tilgang til modellen

---

## 4. Modellfeil

### 4.1 Modell-distribusjon ikke funnet

**Løsning:** Navnet er **store/små bokstaver-sensitive**. Sammenlign `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` med nøyaktig navn i Foundry sidepanel → Modeller.

### 4.2 Uventet modellutdata

**Løsning:** Gjennomgå `AGENT_INSTRUCTIONS` i `main.py` (ikke trunkert?). Prøv en annen modell (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Distribusjonsfeil

### 5.1 ACR pull ikke autorisert

**Løsning:** Azure Portal → Container Register → Tilgangskontroll (IAM) → Legg til **AcrPull**-rollen for Foundry-prosjektets administrerte identitet.

### 5.2 Agent starter ikke (forblir "Pending" eller "Failed")

Sjekk container-logger i sidepanelet. Vanlige årsaker:

| Loggmelding | Løsning |
|-------------|--------|
| `ModuleNotFoundError` | Legg til manglende pakke i `requirements.txt`, distribuer på nytt |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Legg til miljøvariabel i `agent.yaml` under `environment_variables` |
| `Address already in use` | Sørg for at kun én prosess binder til port 8088 |

### 5.3 Distribusjon går ut på tid

**Løsning:** Sjekk internettforbindelsen. Første distribusjon pusher >100MB. Bak en proxy? Konfigurer Docker Desktop proxy-innstillinger.

---

## 6. Path B - Foundry Local

### 6.1 Foundry Local starter ikke

| Problem | Løsning |
|---------|---------|
| `foundry: command not found` | Installer på nytt: `winget install Microsoft.FoundryLocal` |
| Utilstrekkelige ressurser | Foundry Local trenger ~4GB RAM ledig. Lukk andre apper. |
| Modellnedlasting feiler | Sjekk diskplass (modeller er 2–8 GB). Prøv igjen: `foundry local models pull <name>` |

### 6.2 Foundry Local modellfeil

| Problem | Løsning |
|---------|---------|
| Trege responser | Forventet - lokale modeller kjører på CPU med mindre du har GPU. Vær tålmodig. |
| Dårlig kvalitet på utdata | Prøv en større modell hvis maskinvaren din tillater det. `phi-4-mini` er en god balanse. |
| Tilkobling nektes | Verifiser at Foundry Local kjører: `foundry local status`. Start på nytt om nødvendig. |

---

## 7. Rask referanse: RBAC-roller

| Rolle | Omfang | Gir |
|-------|--------|-----|
| **Azure AI User** | Prosjekt | Datahandlinger: `agents/write`, `agents/read` |
| **Azure AI Developer** | Prosjekt/Konto | Datahandlinger + prosjektopprettelse |
| **Azure AI Owner** | Konto | Full tilgang + rolleadministrasjon |
| **Contributor** | Abonnement/RG | Kun administrasjonshandlinger (**ingen** datahandlinger) |
| **Owner** | Abonnement/RG | Administrasjon + rolleoppgave (**ingen** datahandlinger) |

---

## 8. Workshop fullføringsliste

| # | Element | Modul |
|---|---------|--------|
| 1 | Forutsetninger installert og verifisert | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit-utvidelsen installert, prosjekt koblet til (eller Path B konfigurert) | [01](01-setup.md) |
| 3 | Hostet agent generert | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfigurert, instruksjoner skrevet, avhengigheter installert | [03](03-configure-and-code.md) |
| 5 | Agent testet lokalt – 3 funksjonelle scenarioer godkjent | [04](04-test-locally.md) |
| 6 | Distribuert til Foundry (kun Path A) | [05](05-deploy-to-foundry.md) |
| 7 | Edge-case/sikkerhetstester bestått i skyen (kun Path A) | [06](06-verify-in-playground.md) |
| 8 | Sammendrag gjennomgått, neste steg identifisert | [07](07-summary.md) |

---

**Forrige:** [07 - Sammendrag](07-summary.md) · **Hjem:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->