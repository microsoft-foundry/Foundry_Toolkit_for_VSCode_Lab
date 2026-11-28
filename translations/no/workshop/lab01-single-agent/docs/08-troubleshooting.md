# Modul 8 - Feilsøking

Denne modulen er en referanseguide for vanlige problemer. Bokmerk den og kom tilbake når noe går galt.

---

## 1. Tillatelsesfeil

### 1.1 `agents/write` tillatelse nektes

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Hovedårsak:** Manglende `Azure AI User`-rolle på **prosjekt**nivå. Dette er den vanligste feilen i workshoppen.

**Løsning:**
1. Åpne [portal.azure.com](https://portal.azure.com).
2. Søk etter navnet på Foundry-**prosjektet** ditt → klikk resultatet av typen **"Microsoft Foundry project"** (IKKE foreldre-kontoen).
3. **Tilgangskontroll (IAM)** → **+ Legg til** → **Legg til rolle-tilordning**.
4. Rolle: **Azure AI User** → Neste.
5. Medlemmer: Velg deg selv → Gjennomgå + tilordne → Gjennomgå + tilordne.
6. **Vent 1–2 minutter** → prøv igjen.

> **Hvorfor Owner/Contributor ikke er nok:** Disse rollene gir kun *administrasjons*-handlinger. Agent-operasjoner krever `agents/write` *datahandling*, som kun finnes i `Azure AI User`, `Azure AI Developer` eller `Azure AI Owner`. Se [Foundry RBAC-dokumentasjon](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` under provisjonering

**Løsning:** Be administratoren din tilordne **Contributor** på ressursgruppen, eller la dem opprette prosjektet for deg og gi deg **Azure AI User** på det.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker-feil

> Docker er **valgfritt**. Disse gjelder kun hvis Docker Desktop er installert og utvidelsen forsøker lokal bygging.

### 2.1 Docker daemon kjører ikke

**Løsning:** Start Docker Desktop → vent til status er "kjører" → verifiser med `docker info` → prøv igjen.

### 2.2 Bygg mislykkes med avhengighetsfeil

**Løsning:** Kontroller stavemåten til `requirements.txt`, test lokalt først: `pip install -r requirements.txt`.

### 2.3 Plattform-mismatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentiseringsfeil

### 3.1 `DefaultAzureCredential` mislykkes

**Løsning (prøv i denne rekkefølgen):**
1. `az login` (autentiser på nytt)
2. `az account set --subscription "<id>"` (korrekt abonnement)
3. VS Code → Kontoer → Logg ut → Logg inn igjen
4. Verifiser: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token fungerer lokalt men ikke på hostet agent

**Forventet:** Hostede agenter bruker systemadministrert identitet, ikke dine legitimasjoner. Hvis den hostede agenten får autentiseringsfeil:
- Verifiser at `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `agent.yaml` løser til navnet på modellimplementeringen din (`FOUNDRY_PROJECT_ENDPOINT` injiseres av Foundry ved kjøring - ikke deklarer den i `agent.yaml`)
- Sjekk at prosjektets administrerte identitet har tilgang til modellen

---

## 4. Modelfeil

### 4.1 Modellimplementering ikke funnet

**Løsning:** Navnet er **sensitivt for store og små bokstaver**. Sammenlign `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` med det nøyaktige navnet i Foundry sidepanelet → Modeller.

### 4.2 Uventet modellutgang

**Løsning:** Gjennomgå `AGENT_INSTRUCTIONS` i `main.py` (ikke avkortet?). Prøv en annen modell (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Distribusjonsfeil

### 5.1 ACR pull ikke autorisert

**Løsning:** Azure-portalen → Container Register → Tilgangskontroll (IAM) → Legg til **AcrPull**-rolle til prosjektets administrerte identitet.

### 5.2 Agenten starter ikke (blir "Venter" eller "Mislyktes")

Sjekk containerlogger i sidepanelet. Vanlige årsaker:

| Loggmelding | Løsning |
|-------------|--------|
| `ModuleNotFoundError` | Legg til manglende pakke i `requirements.txt`, deploy på nytt |
| `ValueError: Missing required environment variables` | Bekreft at `AZURE_AI_MODEL_DEPLOYMENT_NAME` er deklarert i `agent.yaml` under `environment_variables` og har verdi, deploy på nytt. `FOUNDRY_PROJECT_ENDPOINT` injiseres av Foundry ved kjøring |
| `Address already in use` | Sikre at kun en prosess binder seg til port 8088 |

### 5.3 Distribusjon timer ut

**Løsning:** Sjekk internettforbindelse. Første distribusjon laster opp >100MB. Bak en proxy? Konfigurer proxy-innstillingene i Docker Desktop.

---

## 6. Tilnærming B - Foundry Local

### 6.1 Foundry Local vil ikke starte

| Problem | Løsning |
|---------|--------|
| `foundry: command not found` | Reinstaller: `winget install Microsoft.FoundryLocal` |
| Utilstrekkelige ressurser | Foundry Local trenger ~4GB ledig RAM. Lukk andre apper. |
| Modellnedlasting mislykkes | Sjekk diskplass (modeller er 2–8 GB). Prøv på nytt: `foundry local models pull <name>` |

### 6.2 Foundry Local modelfeil

| Problem | Løsning |
|---------|--------|
| Trege responser | Forventet - lokale modeller kjører på CPU med mindre du har GPU. Vær tålmodig. |
| Dårlig kvalitet på utdata | Prøv en større modell hvis maskinvaren tillater det. `phi-4-mini` er en god balanse. |
| Forbindelse nektes | Verifiser at Foundry Local kjører: `foundry local status`. Start på nytt om nødvendig. |

---

## 7. Rask referanse: RBAC-roller

| Rolle | Omfang | Gir |
|-------|--------|-------|
| **Azure AI User** | Prosjekt | Datahandlinger: `agents/write`, `agents/read` |
| **Azure AI Developer** | Prosjekt/Konto | Datahandlinger + prosjektopprettelse |
| **Azure AI Owner** | Konto | Full tilgang + rolleadministrasjon |
| **Contributor** | Abonnement/RG | Kun administrasjonshandlinger (**ingen** datahandlinger) |
| **Owner** | Abonnement/RG | Administrasjon + rolle-tilordning (**ingen** datahandlinger) |

---

## 8. Workshop fullførings-sjekkliste

| # | Element | Modul |
|---|---------|-------|
| 1 | Forutsetninger installert og verifisert | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit-utvidelsen installert, prosjekt tilkoblet (eller Tilnærming B konfigurert) | [01](01-setup.md) |
| 3 | Hostet agent satt opp | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfigurert, instruksjoner skrevet, avhengigheter installert | [03](03-configure-and-code.md) |
| 5 | Agent testet lokalt - 3 funksjonelle scenarioer bestått | [04](04-test-locally.md) |
| 6 | Distribuert til Foundry (kun Tilnærming A) | [05](05-deploy-to-foundry.md) |
| 7 | Edge-case/sikkerhetstester bestått i skyen (kun Tilnærming A) | [06](06-verify-in-playground.md) |
| 8 | Oppsummering gjennomgått, neste steg identifisert | [07](07-summary.md) |

---

**Forrige:** [07 - Oppsummering](07-summary.md) · **Hjem:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->