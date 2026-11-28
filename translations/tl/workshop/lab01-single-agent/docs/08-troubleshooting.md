# Module 8 - Pag-troubleshoot

Ang module na ito ay isang gabay sa mga karaniwang isyu. I-bookmark ito at bumalik kapag may nagkamali.

---

## 1. Mga error sa pahintulot

### 1.1 `agents/write` permission denied

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Pinagmulan ng problema:** Nawawalang `Azure AI User` na papel sa antas ng **project**. Ito ang #1 na error sa workshop.

**Ayusin:**
1. Buksan ang [portal.azure.com](https://portal.azure.com).
2. Hanapin ang pangalan ng iyong Foundry **project** → i-click ang resulta na uri **"Microsoft Foundry project"** (HINDI ang parent account).
3. **Access control (IAM)** → **+ Add** → **Add role assignment**.
4. Papel: **Azure AI User** → Susunod.
5. Mga Miyembro: Piliin ang iyong sarili → Review + assign → Review + assign.
6. **Maghintay ng 1–2 minuto** → subukang muli.

> **Bakit hindi sapat ang Owner/Contributor:** Ang mga papel na ito ay nagbibigay lang ng *management* na mga aksyon. Nangangailangan ang operasyon ng ahente ng `agents/write` *data action*, na nasa lamang `Azure AI User`, `Azure AI Developer`, o `Azure AI Owner`. Tingnan ang [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` habang nagpo-provision

**Ayusin:** Hilingin sa iyong admin na magtalaga ng **Contributor** sa resource group, o hayaan silang likhain ang proyekto para sa iyo at bigyan ka ng **Azure AI User** dito.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Mga error sa Docker

> Ang Docker ay **opsyonal**. Ito ay nalalapat lamang kung naka-install ang Docker Desktop at sinusubukang magsagawa ng lokal na build ang extension.

### 2.1 Hindi tumatakbo ang Docker daemon

**Ayusin:** Simulan ang Docker Desktop → maghintay hanggang sa "running" status → tiyakin gamit ang `docker info` → subukang muli.

### 2.2 Nabibigo ang build dahil sa mga error sa dependency

**Ayusin:** Suriin ang ispeling ng `requirements.txt`, subukan muna nang lokal: `pip install -r requirements.txt`.

### 2.3 Hindi tugma ang platform (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Mga error sa autentikasyon

### 3.1 Nabibigo ang `DefaultAzureCredential`

**Ayusin (subukang sunod-sunod):**
1. `az login` (muling mag-autenticate)
2. `az account set --subscription "<id>"` (tamang subscription)
3. VS Code → Accounts → Sign Out → Muling Sign In
4. Tiyakin: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Gumagana ang token sa lokal pero hindi sa hosted

**Inaasahan:** Ginagamit ng hosted agents ang system-managed identity, hindi ang iyong kredensyal. Kung nakakakuha ng error sa autentikasyon ang hosted agent:
- Tiyakin na ang `AZURE_AI_MODEL_DEPLOYMENT_NAME` sa `agent.yaml` ay tumutukoy sa pangalan ng iyong model deployment (`FOUNDRY_PROJECT_ENDPOINT` ay ini-inject ng Foundry sa runtime - huwag ideklara ito sa `agent.yaml`)
- Suriin na ang managed identity ng proyekto ay may access sa modelo

---

## 4. Mga error sa modelo

### 4.1 Hindi makita ang model deployment

**Ayusin:** Ang pangalan ay **case-sensitive**. Ihambing ang `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` gamit ang eksaktong pangalan sa Foundry sidebar → Models.

### 4.2 Hindi inaasahang output ng modelo

**Ayusin:** Suriin ang `AGENT_INSTRUCTIONS` sa `main.py` (hindi ba ito pinutol?). Subukan ang ibang modelo (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Mga error sa deployment

### 5.1 Hindi awtorisadong pag-pull mula sa ACR

**Ayusin:** Azure Portal → Container Registry → Access control (IAM) → Magdagdag ng **AcrPull** na papel sa managed identity ng Foundry project.

### 5.2 Nabigong magsimula ang agent (nananatiling "Pending" o "Failed")

Tingnan ang mga container logs sa sidebar. Mga karaniwang sanhi:

| Mensahe sa log | Ayusin |
|-------------|-----|
| `ModuleNotFoundError` | Magdagdag ng nawawalang package sa `requirements.txt`, i-redeploy |
| `ValueError: Missing required environment variables` | Kumpirmahin na ang `AZURE_AI_MODEL_DEPLOYMENT_NAME` ay naka-deklara sa `agent.yaml` sa ilalim ng `environment_variables` at may value, pagkatapos ay i-redeploy. Ang `FOUNDRY_PROJECT_ENDPOINT` ay ini-inject ng Foundry sa runtime |
| `Address already in use` | Siguraduhing iisa lamang ang proseso na nakakabit sa port 8088 |

### 5.3 Nagrereklamo ang deployment ng timeout

**Ayusin:** Suriin ang koneksyon sa internet. Ang unang deploy ay nagpapadala ng >100MB. Nasa likod ng proxy? I-configure ang Docker Desktop proxy settings.

---

## 6. Landas B - Foundry Local

### 6.1 Hindi nagsisimula ang Foundry Local

| Isyu | Ayusin |
|-------|-----|
| `foundry: command not found` | I-reinstall: `winget install Microsoft.FoundryLocal` |
| Hindi sapat ang resources | Ang Foundry Local ay nangangailangan ng ~4GB RAM na libre. Isara ang ibang mga app. |
| Nabibigo ang pag-download ng modelo | Suriin ang disk space (2–8 GB ang mga modelo). Subukang muli: `foundry local models pull <name>` |

### 6.2 Mga error sa modelo ng Foundry Local

| Isyu | Ayusin |
|-------|-----|
| Mabagal ang mga tugon | Inaasahan - ang mga lokal na modelo ay tumatakbo sa CPU maliban kung may GPU ka. Maghintay lang. |
| Mahinang kalidad ng output | Subukan ang mas malaking modelo kung kayang-hardware mo. Ang `phi-4-mini` ay magandang balanse. |
| Tinatanggihan ang koneksyon | Tiyaking tumatakbo ang Foundry Local: `foundry local status`. I-restart kung kinakailangan. |

---

## 7. Mabilisang sanggunian: Mga papel ng RBAC

| Papel | Saklaw | Nagbibigay ng karapatan |
|------|-------|--------|
| **Azure AI User** | Project | Mga aksyon sa data: `agents/write`, `agents/read` |
| **Azure AI Developer** | Project/Account | Mga aksyon sa data + paglikha ng proyekto |
| **Azure AI Owner** | Account | Buong access + pamamahala ng papel |
| **Contributor** | Subscription/RG | Mga aksyon sa pamamahala lamang (**hindi** mga aksyon sa data) |
| **Owner** | Subscription/RG | Pamamahala + pagtatalaga ng papel (**hindi** mga aksyon sa data) |

---

## 8. Checklist para sa pagtatapos ng workshop

| # | Bagay | Module |
|---|------|--------|
| 1 | Na-install at na-verify ang mga prerequisites | [00](00-prerequisites.md) |
| 2 | Na-install ang Foundry Toolkit extension, nakakonekta ang proyekto (o na-configure ang Path B) | [01](01-setup.md) |
| 3 | Na-setup ang hosted agent | [02](02-create-hosted-agent.md) |
| 4 | `.env` nakonpigura, instruksyon naisulat, mga dependency na-install | [03](03-configure-and-code.md) |
| 5 | Sinubukan ang Ahente nang lokal - 3 matagumpay na senaryo | [04](04-test-locally.md) |
| 6 | Na-deploy sa Foundry (Path A lamang) | [05](05-deploy-to-foundry.md) |
| 7 | Lumipas ang mga edge-case/safety test sa cloud (Path A lamang) | [06](06-verify-in-playground.md) |
| 8 | Nasuri ang buod, natukoy ang mga susunod na hakbang | [07](07-summary.md) |

---

**Nuna:** [07 - Buod](07-summary.md) · **Bahay:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->