# Module 8 - Pag-aayos ng Suliranin

Ang modyul na ito ay isang gabay na sanggunian para sa mga karaniwang problema. I-bookmark ito at bumalik kapag may nagkamali.

---

## 1. Mga error sa pahintulot

### 1.1 Hindi pinahihintulutang `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Pangunahing sanhi:** Nawawala ang `Azure AI User` na papel sa antas ng **project**. Ito ang #1 na error sa workshop.

**Ayusin:**
1. Buksan ang [portal.azure.com](https://portal.azure.com).
2. Hanapin ang iyong Foundry **project** na pangalan → i-click ang resulta ng uri na **"Microsoft Foundry project"** (HINDI parent account).
3. **Access control (IAM)** → **+ Add** → **Add role assignment**.
4. Papel: **Azure AI User** → Next.
5. Mga Miyembro: Piliin ang iyong sarili → Review + assign → Review + assign.
6. **Maghintay ng 1–2 minuto** → subukang muli.

> **Bakit hindi sapat ang Owner/Contributor:** Ang mga papel na ito ay nagbibigay lamang ng mga *management* na aksyon. Ang operasyon ng agent ay nangangailangan ng `agents/write` na *data action*, na mayroon lamang sa `Azure AI User`, `Azure AI Developer`, o `Azure AI Owner`. Tingnan ang [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` habang nagproprovision

**Ayusin:** Hilingin sa iyong admin na magtalaga ng **Contributor** sa resource group, o ipagawa nila ang project para sa iyo at bigyan ka ng **Azure AI User** dito.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Maghintay hanggang: "Rehistrado"
```

---

## 2. Mga error sa Docker

> Ang Docker ay **opsyonal**. Ito ay nalalapat lamang kung naka-install ang Docker Desktop at sinusubukang gumawa ng lokal na build ang extension.

### 2.1 Hindi tumatakbo ang Docker daemon

**Ayusin:** Simulan ang Docker Desktop → maghintay hanggang sa maging "running" ang status → tingnan gamit ang `docker info` → subukang muli.

### 2.2 Nabigo ang build dahil sa mga dependency error

**Ayusin:** Suriin ang baybay ng `requirements.txt`, subukan muna locally: `pip install -r requirements.txt`.

### 2.3 Hindi tugma ang platform (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Mga error sa Authentication

### 3.1 Nabibigo ang `DefaultAzureCredential`

**Ayusin (subukan sa pagkakasunod):**
1. `az login` (muling mag-authenticate)
2. `az account set --subscription "<id>"` (tamang subscription)
3. VS Code → Accounts → Sign Out → Muling Sign In
4. Tiyakin: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Gumagana ang token local pero hindi hosted

**Inaasahan:** Ang mga hosted agent ay gumagamit ng system-managed identity, hindi ang iyong credential. Kung nakakakuha ang hosted agent ng mga error sa auth:
- Tiyakin na ang `AZURE_AI_PROJECT_ENDPOINT` sa `agent.yaml` ay tama
- Suriin na ang managed identity ng proyekto ay may access sa model

---

## 4. Mga error sa Model

### 4.1 Hindi makita ang deployment ng model

**Ayusin:** Case-sensitive ang pangalan. Ihambing ang `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` sa eksaktong pangalan sa Foundry sidebar → Models.

### 4.2 Hindi inaasahang output ng model

**Ayusin:** Suriin ang `AGENT_INSTRUCTIONS` sa `main.py` (hindi ba naputol?). Subukan ang ibang model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Mga error sa Deployment

### 5.1 Hindi pinahihintulutan ang ACR pull

**Ayusin:** Pumunta sa Azure Portal → Container Registry → Access control (IAM) → Magdagdag ng **AcrPull** na papel sa managed identity ng Foundry project.

### 5.2 Hindi magsimula ang Agent (nananatiling "Pending" o "Failed")

Tingnan ang mga log ng container sa sidebar. Mga karaniwang sanhi:

| Mensahe ng Log | Ayusin |
|-------------|-----|
| `ModuleNotFoundError` | Magdagdag ng nawawalang package sa `requirements.txt`, i-redeploy |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Magdagdag ng env var sa `agent.yaml` sa ilalim ng `environment_variables` |
| `Address already in use` | Tiyakin na iisa lamang ang proseso na kumokonekta sa port 8088 |

### 5.3 Timeout ang Deployment

**Ayusin:** Suriin ang koneksyon sa internet. Ang unang deploy ay nag-pupush ng >100MB. Nasa likod ng proxy? Isaayos ang Docker Desktop proxy settings.

---

## 6. Path B - Foundry Local

### 6.1 Hindi magsimula ang Foundry Local

| Suliranin | Ayusin |
|-------|-----|
| `foundry: command not found` | I-reinstall: `winget install Microsoft.FoundryLocal` |
| Hindi sapat ang mga resources | Nangangailangan ang Foundry Local ng ~4GB RAM na libre. Isara ang ibang apps. |
| Nabigo ang pag-download ng model | Suriin ang space sa disk (2–8 GB ang laki ng mga model). Subukang muli: `foundry local models pull <name>` |

### 6.2 Mga error sa model ng Foundry Local

| Suliranin | Ayusin |
|-------|-----|
| Mabagal na tugon | Inaasahan - tumatakbo ang local models sa CPU maliban kung may GPU. Maghinay-hinay. |
| Mababang kalidad ng output | Subukan ang mas malaking model kung kaya ng iyong hardware. Ang `phi-4-mini` ay magandang balanse. |
| Tinanggihan ang koneksyon | Tiyakin na tumatakbo ang Foundry Local: `foundry local status`. I-restart kung kinakailangan. |

---

## 7. Mabilisang sanggunian: Mga papel sa RBAC

| Papel | Saklaw | Nagbibigay |
|------|-------|--------|
| **Azure AI User** | Project | Mga data action: `agents/write`, `agents/read` |
| **Azure AI Developer** | Project/Account | Mga data action + paggawa ng proyekto |
| **Azure AI Owner** | Account | Buong access + pamamahala ng papel |
| **Contributor** | Subscription/RG | Mga management action lamang (**walang** data action) |
| **Owner** | Subscription/RG | Management + pagtatalaga ng papel (**walang** data action) |

---

## 8. Checklist sa pagtatapos ng workshop

| # | Item | Module |
|---|------|--------|
| 1 | Mga kinakailangang naka-install at nasuri | [00](00-prerequisites.md) |
| 2 | Na-install ang Foundry Toolkit extension, nakakonekta ang proyekto (o naka-configure ang Path B) | [01](01-setup.md) |
| 3 | Na-scaffold ang hosted agent | [02](02-create-hosted-agent.md) |
| 4 | Na-configure ang `.env`, naisulat ang mga instruksyon, na-install ang dependencies | [03](03-configure-and-code.md) |
| 5 | Na-test ang agent local - pumasa sa 3 functional na scenario | [04](04-test-locally.md) |
| 6 | Na-deploy sa Foundry (Path A lamang) | [05](05-deploy-to-foundry.md) |
| 7 | Pumasa sa edge-case/safety tests sa cloud (Path A lamang) | [06](06-verify-in-playground.md) |
| 8 | Nasuri ang summary, natukoy ang mga susunod na hakbang | [07](07-summary.md) |

---

**Nakaraan:** [07 - Summary](07-summary.md) · **Bahay:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->