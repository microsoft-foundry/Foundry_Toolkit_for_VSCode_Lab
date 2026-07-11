# 8 modulis – Trikčių šalinimas

Šis modulis yra dažnai pasitaikančių problemų nuorodų vadovas. Pažymėkite jį ir grįžkite, kai ką nors nepavyks.

---

## 1. Leidimų klaidos

### 1.1 Leidimas `agents/write` nepatvirtintas

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Pagrindinė priežastis:** Trūksta `Azure AI User` vaidmens **projekto** lygyje. Tai yra dažniausia klaida dirbtuvėse.

**Sprendimas:**
1. Atidarykite [portal.azure.com](https://portal.azure.com).
2. Ieškokite savo Foundry **projekto** pavadinimo → spustelėkite rezultatą, kurio tipas yra **"Microsoft Foundry project"** (NE tėvinė paskyra).
3. **Prieigos valdymas (IAM)** → **+ Pridėti** → **Pridėti vaidmens priskyrimą**.
4. Vaidmuo: **Azure AI User** → Toliau.
5. Nariai: Pasirinkite save → Peržiūrėti ir priskirti → Peržiūrėti ir priskirti.
6. **Palaukite 1–2 minutes** → bandykite dar kartą.

> **Kodėl savininko/įnašytojo vaidmens nepakanka:** Šie vaidmenys suteikia tik *valdymo* veiksmus. Agentų operacijoms reikia `agents/write` *duomenų veiksmo*, kuris yra tik `Azure AI User`, `Azure AI Developer`, arba `Azure AI Owner`. Žr. [Foundry RBAC dokumentaciją](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` klaida diegiant

**Sprendimas:** Paprašykite savo administratoriaus priskirti **Contributor** vaidmenį išteklių grupei arba tegul jis sukuria projektą ir suteikia jums **Azure AI User** vaidmenį.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Palaukite, kol bus: „Užregistruota“
```

---

## 2. Docker klaidos

> Docker yra **pasirinktinė**. Šios klaidos taikomos tik jei įdiegta Docker Desktop ir plėtinys bando vietinį build procesą.

### 2.1 Docker daemon neveikia

**Sprendimas:** Paleiskite Docker Desktop → palaukite kol bus "running" būsena → patikrinkite su `docker info` → bandykite dar kartą.

### 2.2 Statybos klaidos dėl priklausomybių

**Sprendimas:** Patikrinkite ar `requirements.txt` taisyklingas, išbandykite vietoje pirmiau: `pip install -r requirements.txt`.

### 2.3 Platformos neatitikimas (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentifikavimo klaidos

### 3.1 `DefaultAzureCredential` nepavyksta

**Sprendimas (išbandykite paeiliui):**
1. `az login` (perautentifikuotis)
2. `az account set --subscription "<id>"` (nustatyti teisingą prenumeratą)
3. VS Code → Paskyros → Atsijungti → Prisijungti iš naujo
4. Patikrinkite: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Tokenas veikia vietoje, bet ne talpinant

**Tikėtina priežastis:** Talpinami agentai naudoja sistemos valdomą tapatybę, o ne jūsų kredencialus. Jei talpinama agentas gauna autentifikacijos klaidas:
- Patikrinkite, ar `AZURE_AI_PROJECT_ENDPOINT` faile `agent.yaml` yra teisinga
- Patikrinkite, ar projekto valdomoji tapatybė turi prieigą prie modelio

---

## 4. Modelio klaidos

### 4.1 Modelio diegimas nerastas

**Sprendimas:** Pavadinimas yra **jautrus didžiosioms raidėms**. Palyginkite `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` su tiksliu pavadinimu Foundry šoniniame meniu → Modeliai.

### 4.2 Netikėtas modelio išvestis

**Sprendimas:** Peržiūrėkite `AGENT_INSTRUCTIONS` faile `main.py` (ar nėra nutrūkęs?). Išbandykite kitą modelį (`gpt-4.1` prieš `gpt-4.1-mini`).

---

## 5. Diegimo klaidos

### 5.1 ACR pull neautorizuotas

**Sprendimas:** Azure Portal → Container Registry → Prieigos valdymas (IAM) → Pridėti **AcrPull** vaidmenį Foundry projekto valdomai tapatybei.

### 5.2 Agentas nepaleidžiamas (lieka "Pending" arba "Failed")

Patikrinkite konteinerio žurnalus šoniniame meniu. Dažnos priežastys:

| Žurnalo pranešimas | Sprendimas |
|-------------|-----|
| `ModuleNotFoundError` | Pridėkite trūkstamą paketą prie `requirements.txt`, diegkite iš naujo |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Pridėkite aplinkos kintamąjį į `agent.yaml` skiltyje `environment_variables` |
| `Address already in use` | Užtikrinkite, kad tik vienas procesas užima 8088 prievadą |

### 5.3 Diegimo laikas baigėsi

**Sprendimas:** Patikrinkite interneto ryšį. Pirmasis diegimas siunčia >100MB. Esate už proxy? Konfigūruokite Docker Desktop proxy nustatymus.

---

## 6. Kelias B – Foundry Local

### 6.1 Foundry Local nepaleidžiamas

| Problema | Sprendimas |
|-------|-----|
| `foundry: command not found` | Perinstaliuokite: `winget install Microsoft.FoundryLocal` |
| Nepakanka išteklių | Foundry Local reikalauja ~4GB RAM laisvos. Uždarykite kitas programas. |
| Modelio atsisiuntimas nepavyksta | Patikrinkite disko vietą (modeliai 2–8 GB). Bandykite vėl: `foundry local models pull <name>` |

### 6.2 Foundry Local modelio klaidos

| Problema | Sprendimas |
|-------|-----|
| Lėti atsakymai | Tai normalu – vietiniai modeliai veikia CPU, nebent turite GPU. Kantrybės. |
| Prasta kokybė išvesties | Išbandykite didesnį modelį, jei aparatinė įranga leidžia. `phi-4-mini` yra geras balansas. |
| Ryšys atmestas | Patikrinkite, ar Foundry Local paleistas: `foundry local status`. Jei reikia, paleiskite iš naujo. |

---

## 7. Greita santrauka: RBAC vaidmenys

| Vaidmuo | Apimtis | Suteikia |
|------|-------|--------|
| **Azure AI User** | Projektas | Duomenų veiksmai: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projektas/Paskyra | Duomenų veiksmai + projekto kūrimas |
| **Azure AI Owner** | Paskyra | Pilnas priėjimas + vaidmenų valdymas |
| **Contributor** | Prenumerata/Išteklių grupė | Tik valdymo veiksmai (**be** duomenų veiksmų) |
| **Owner** | Prenumerata/Išteklių grupė | Valdymo veiksmai + vaidmenų priskyrimas (**be** duomenų veiksmų) |

---

## 8. Dirbtuvių užbaigimo kontrolinis sąrašas

| Nr. | Elementas | Modulis |
|---|------|--------|
| 1 | Iš anksto reikalingos priemonės įdiegtos ir patikrintos | [00](00-prerequisites.md) |
| 2 | Įdiegtas Foundry Toolkit pletinys, projektas prijungtas (arba sukonfigūruotas Kelias B) | [01](01-setup.md) |
| 3 | Sutvirtintas talpinamas agentas | [02](02-create-hosted-agent.md) |
| 4 | Sukonfigūruotas `.env`, parašytos instrukcijos, įdiegtos priklausomybės | [03](03-configure-and-code.md) |
| 5 | Agentas išbandytas vietoje – praėjo 3 funkcionalūs scenarijai | [04](04-test-locally.md) |
| 6 | Išdiegtas Foundry (tik Kelias A) | [05](05-deploy-to-foundry.md) |
| 7 | Debesyje pavyko kraštutiniai / saugumo testai (tik Kelias A) | [06](06-verify-in-playground.md) |
| 8 | Peržiūrėta santrauka, nustatytos kitos žingsniai | [07](07-summary.md) |

---

**Ankstesnis:** [07 - Santrauka](07-summary.md) · **Pradžia:** [Dirbtuvių README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->