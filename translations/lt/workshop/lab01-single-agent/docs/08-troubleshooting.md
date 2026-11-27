# Modulis 8 - Trikčių šalinimas

Šis modulis yra bendrų problemų nuorodų vadovas. Įsidiekite jį žymių juostoje ir grįžkite, kai kas nors nepavyksta.

---

## 1. Leidimų klaidos

### 1.1 `agents/write` leidimas atmestas

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Pagrindinė priežastis:** Trūksta `Azure AI User` vaidmens **projekto** lygyje. Tai yra dažniausia dirbtuvių klaida.

**Sprendimas:**
1. Atidarykite [portal.azure.com](https://portal.azure.com).
2. Ieškokite savo Foundry **projekto** pavadinimo → spustelėkite rezultatą, kurio tipas yra **"Microsoft Foundry project"** (NE tėvinis paskyros).
3. **Prieigos valdymas (IAM)** → **+ Pridėti** → **Pridėti vaidmens paskyrimą**.
4. Vaidmuo: **Azure AI User** → Toliau.
5. Nariai: Pasirinkite save → Peržiūrėti + priskirti → Peržiūrėti + priskirti.
6. **Palaukite 1–2 minutes** → bandykite dar kartą.

> **Kodėl Owner/Contributor nepakanka:** Šie vaidmenys suteikia tik *valdymo* veiksmus. Agentų operacijos reikalauja `agents/write` *duomenų veiksmo*, kuris yra tik `Azure AI User`, `Azure AI Developer` arba `Azure AI Owner`. Žr. [Foundry RBAC dokumentaciją](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` diegiant

**Sprendimas:** Paprašykite savo administratoriaus priskirti **Contributor** prie resursų grupės arba tegul jie sukuria projektą jums ir suteikia **Azure AI User** teises.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker klaidos

> Docker yra **pasirinktinė**. Šios klaidos taikomos tik tada, jei įdiegtas Docker Desktop ir plėtinys bando vietinį build.

### 2.1 Docker demonas neveikia

**Sprendimas:** Paleiskite Docker Desktop → palaukite, kol bus rodoma "veikia" būseną → patikrinkite su `docker info` → bandykite dar kartą.

### 2.2 Build nepavyksta dėl priklausomybių klaidų

**Sprendimas:** Patikrinkite `requirements.txt` rašybą, pirmiausia patikrinkite vietoje: `pip install -r requirements.txt`.

### 2.3 Platformos neatitikimas (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentifikacijos klaidos

### 3.1 `DefaultAzureCredential` nepavyksta

**Sprendimas (bandykite nuosekliai):**
1. `az login` (pakartotinė autentifikacija)
2. `az account set --subscription "<id>"` (teisinga prenumerata)
3. VS Code → Paskyros → Atsijungti → Prisijungti iš naujo
4. Patikrinkite: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Žetonas veikia vietoje, bet ne talpinamoje aplinkoje

**Numatoma:** Talpinami agentai naudoja sistemos valdomą identitetą, o ne jūsų kredencialą. Jei talpinamame agente kyla autentifikacijos klaidos:
- Patikrinkite, ar `AZURE_AI_MODEL_DEPLOYMENT_NAME` `agent.yaml` reikšmė atitinka jūsų modelio diegimo pavadinimą (`FOUNDRY_PROJECT_ENDPOINT` įterpiamas Foundry vykdymo metu - jo nereikia deklaruoti `agent.yaml`)
- Įsitikinkite, kad projekto valdomas identitetas turi prieigą prie modelio

---

## 4. Modelio klaidos

### 4.1 Modelio dieginys nerastas

**Sprendimas:** Pavadinimas yra **didžiųjų ir mažųjų raidžių jautrus**. Palyginkite `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` su tikru pavadinimu Foundry šoninės juostos skyriuje → Modeliai.

### 4.2 Netikėtas modelio išvestis

**Sprendimas:** Peržiūrėkite `AGENT_INSTRUCTIONS` `main.py` (ar neapkarpyta?). Išbandykite kitą modelį (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Diegimo klaidos

### 5.1 ACR pull neautorizuotas

**Sprendimas:** Azure portalas → Container Registry → Prieigos valdymas (IAM) → Pridėti **AcrPull** vaidmenį Foundry projekto valdomam identitetui.

### 5.2 Agentas nepaleidžiamas (lieka "Laukiama" arba "Nepavyko")

Patikrinkite konteinerio žurnalus šoninėje juostoje. Dažnos priežastys:

| Žurnalo pranešimas | Sprendimas |
|-------------|-----|
| `ModuleNotFoundError` | Pridėkite trūkstamą paketą į `requirements.txt`, diegkite iš naujo |
| `ValueError: Missing required environment variables` | Patikrinkite, ar `AZURE_AI_MODEL_DEPLOYMENT_NAME` deklaruotas `agent.yaml` pagal `environment_variables` ir turi reikšmę, tada diegkite iš naujo. `FOUNDRY_PROJECT_ENDPOINT` įterpiamas Foundry vykdymo metu |
| `Address already in use` | Įsitikinkite, kad tik vienas procesas naudoja 8088 prievadą |

### 5.3 Diegimas išeina iš laiko ribų

**Sprendimas:** Patikrinkite interneto ryšį. Pirmasis diegimas siunčia >100MB. Ar naudojate proxy serverį? Sukonfigūruokite Docker Desktop proxy nustatymus.

---

## 6. B kelias - Foundry Local

### 6.1 Foundry Local nepasileidžia

| Problema | Sprendimas |
|-------|-----|
| `foundry: command not found` | Iš naujo įdiekite: `winget install Microsoft.FoundryLocal` |
| Nepakankamai išteklių | Foundry Local reikalauja ~4GB laisvos RAM. Uždarykite kitas programas. |
| Modelio atsisiuntimas nepavyksta | Patikrinkite disko vietą (modeliai užima 2–8 GB). Bandykite dar kartą: `foundry local models pull <name>` |

### 6.2 Foundry Local modelio klaidos

| Problema | Sprendimas |
|-------|-----|
| Lėtas atsakymas | Numatytas - vietiniai modeliai veikia CPU, jei neturite GPU. Būkite kantrūs. |
| Prasta kokybės išvestis | Jei jūsų įrenginys leidžia, išbandykite didesnį modelį. `phi-4-mini` yra geras balansas. |
| Ryšys atmestas | Patikrinkite, ar Foundry Local veikia: `foundry local status`. Prireikus paleiskite iš naujo. |

---

## 7. Greitos nuorodos: RBAC vaidmenys

| Vaidmuo | Apimtis | Suteikia |
|------|-------|--------|
| **Azure AI User** | Projektas | Duomenų veiksmai: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projektas/Paskyra | Duomenų veiksmai + projekto kūrimas |
| **Azure AI Owner** | Paskyra | Pilna prieiga + vaidmenų valdymas |
| **Contributor** | Prenumerata/RG | Tik valdymo veiksmai (**be** duomenų veiksmų) |
| **Owner** | Prenumerata/RG | Valdymas + vaidmenų paskyrimas (**be** duomenų veiksmų) |

---

## 8. Dirbtuvės užbaigimo kontrolinis sąrašas

| # | Punktas | Modulis |
|---|------|--------|
| 1 | Išankstiniai reikalavimai įdiegti ir patikrinti | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit plėtinys įdiegtas, projektas prijungtas (arba konfigūruotas B kelias) | [01](01-setup.md) |
| 3 | Talpinamas agentas paruoštas | [02](02-create-hosted-agent.md) |
| 4 | `.env` sukonfigūruotas, instrukcijos parašytos, priklausomybės įdiegtos | [03](03-configure-and-code.md) |
| 5 | Agentas išbandytas lokaliai – praeiti 3 funkciniai scenarijai | [04](04-test-locally.md) |
| 6 | Išdėstytas Foundry (tik A kelias) | [05](05-deploy-to-foundry.md) |
| 7 | Kraštutiniai/saugumo testai praeiti debesyje (tik A kelias) | [06](06-verify-in-playground.md) |
| 8 | Apžvalga peržiūrėta, nustatyti kiti veiksmai | [07](07-summary.md) |

---

**Ankstesnis:** [07 - Apžvalga](07-summary.md) · **Pagrindinis:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->