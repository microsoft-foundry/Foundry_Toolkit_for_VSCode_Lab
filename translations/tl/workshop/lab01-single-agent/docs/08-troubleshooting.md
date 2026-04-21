# Module 8 - Pagsusuri ng Problema

Ang module na ito ay isang sangguniang gabay para sa bawat karaniwang isyu na nararanasan sa workshop. I-bookmark ito - babalikan mo ito kapag may nagkamali.

---

## 1. Mga error sa Pahintulot

### 1.1 `agents/write` permission denied

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Pangunahing sanhi:** Wala kang `Azure AI User` na papel sa **project** na antas. Ito ang pinakakaraniwang error sa workshop.

**Ayusin - hakbang-hakbang:**

1. Buksan ang [https://portal.azure.com](https://portal.azure.com).
2. Sa search bar sa itaas, i-type ang pangalan ng iyong **Foundry project** (hal., `workshop-agents`).
3. **Mahalaga:** I-click ang resulta na nagpapakita ng uri na **"Microsoft Foundry project"**, HINDI ang parent account/hub resource. Iba ito sa mga resources na may magkakaibang RBAC scope.
4. Sa kaliwang navigation sa pahina ng project, i-click ang **Access control (IAM)**.
5. I-click ang tab na **Role assignments** upang tingnan kung mayroon ka nang papel:
   - Hanapin ang iyong pangalan o email.
   - Kung `Azure AI User` ay nakalista na → iba ang sanhi ng error (tingnan ang Step 8 sa ibaba).
   - Kung wala → ituloy ang pagdaragdag nito.
6. I-click ang **+ Add** → **Add role assignment**.
7. Sa tab na **Role**:
   - Hanapin ang [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Piliin ito mula sa mga resulta.
   - I-click ang **Next**.
8. Sa tab na **Members**:
   - Piliin ang **User, group, or service principal**.
   - I-click ang **+ Select members**.
   - Hanapin ang iyong pangalan o email address.
   - Piliin ang iyong sarili mula sa mga resulta.
   - I-click ang **Select**.
9. I-click ang **Review + assign** → muli ang **Review + assign**.
10. **Maghintay ng 1-2 minuto** - nagtatagal ang pagpapalaganap ng RBAC changes.
11. Subukang muli ang operasyon na nabigo.

> **Bakit hindi sapat ang Owner/Contributor:** Ang Azure RBAC ay may dalawang uri ng pahintulot - *management actions* at *data actions*. Ang Owner at Contributor ay nagbibigay ng management actions (gumawa ng resources, i-edit ang settings), ngunit ang mga operasyon ng agent ay nangangailangan ng `agents/write` **data action**, na kasama lamang sa mga papel na `Azure AI User`, `Azure AI Developer`, o `Azure AI Owner`. Tingnan ang [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` kapag nagpaprovide ng resource

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Pangunahing sanhi:** Wala kang pahintulot na gumawa o magbago ng Azure resources sa subscription/resource group na ito.

**Ayusin:**
1. Hilingin sa administrator ng subscription na italaga sa iyo ang papel na **Contributor** sa resource group kung saan nakalagay ang iyong Foundry project.
2. Bilang alternatibo, hilingin sa kanila na gumawa ng Foundry project para sa iyo at ibigay ang **Azure AI User** sa project.

### 1.3 `SubscriptionNotRegistered` para sa [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Pangunahing sanhi:** Hindi pa nare-register ng Azure subscription ang resource provider na kailangan para sa Foundry.

**Ayusin:**

1. Buksan ang terminal at patakbuhin:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Maghintay hanggang matapos ang registration (maaari tumagal ng 1-5 minuto):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Inaasahang output: `"Registered"`
3. Subukang muli ang operasyon.

---

## 2. Mga error ng Docker (kung naka-install ang Docker lamang)

> Ang Docker ay **opsyonal** para sa workshop na ito. Ang mga error na ito ay umiiral lamang kung naka-install ang Docker Desktop at sinubukan ng Foundry extension na gumawa ng lokal na container build.

### 2.1 Hindi tumatakbo ang Docker daemon

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Ayusin - hakbang-hakbang:**

1. **Hanapin ang Docker Desktop** sa iyong Start menu (Windows) o Applications (macOS) at buksan ito.
2. Maghintay hanggang ipakita ng Docker Desktop window ang **"Docker Desktop is running"** - karaniwang tumatagal ito ng 30-60 segundo.
3. Hanapin ang Docker whale icon sa iyong system tray (Windows) o menu bar (macOS). I-hover ito upang kumpirmahin ang status.
4. I-verify sa terminal:
   ```powershell
   docker info
   ```
   Kung nagpapakita ito ng Docker system information (Server Version, Storage Driver, atbp.), tumatakbo ang Docker.
5. **Para sa Windows lamang:** Kung hindi pa rin magsimula ang Docker:
   - Buksan ang Docker Desktop → **Settings** (gear icon) → **General**.
   - Siguraduhing naka-check ang **Use the WSL 2 based engine**.
   - I-click ang **Apply & restart**.
   - Kung wala pang naka-install na WSL 2, patakbuhin ang `wsl --install` sa isang elevated PowerShell at i-restart ang iyong computer.
6. Subukang muli ang deployment.

### 2.2 Nabibigo ang Docker build dahil sa dependency errors

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Ayusin:**
1. Buksan ang `requirements.txt` at tiyaking tama ang spelling ng lahat ng mga pangalan ng package.
2. Siguraduhing tama ang version pinning:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Subukan munang i-install nang lokal:
   ```bash
   pip install -r requirements.txt
   ```
4. Kung gumagamit ng private package index, siguraduhing may network access ang Docker dito.

### 2.3 Hindi tugmang platform ng container (Apple Silicon)

Kung nagde-deploy mula sa Apple Silicon Mac (M1/M2/M3/M4), ang container ay dapat itayo para sa `linux/amd64` dahil ginagamit ng Foundry container runtime ang AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Awtomatikong inaayos ng deploy command ng Foundry extension ito sa karamihan ng kaso. Kung makakita ka ng error na may kaugnayan sa architecture, itayo ito nang mano-mano gamit ang `--platform` flag at makipag-ugnayan sa team ng Foundry.

---

## 3. Mga error sa Authentication

### 3.1 Nabigo ang [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) sa pagkuha ng token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Pangunahing sanhi:** Wala sa mga pinagkukunan ng kredensyal sa `DefaultAzureCredential` chain ang may valid na token.

**Ayusin - subukan ang bawat hakbang nang sunod-sunod:**

1. **Mag-login muli gamit ang Azure CLI** (pinakakaraniwang solusyon):
   ```bash
   az login
   ```
   Magbubukas ang browser window. Mag-sign in, pagkatapos ay bumalik sa VS Code.

2. **I-set ang tamang subscription:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Kung hindi ito ang tamang subscription:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Mag-login muli gamit ang VS Code:**
   - I-click ang icon na **Accounts** (icon ng tao) sa ibabang kaliwa ng VS Code.
   - I-click ang iyong pangalan ng account → **Sign Out**.
   - I-click muli ang Accounts icon → **Sign in to Microsoft**.
   - Kumpletuhin ang browser sign-in flow.

4. **Service principal (para sa mga CI/CD scenario lamang):**
   - Itakda ang mga environment variable na ito sa iyong `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Pagkatapos ay i-restart ang iyong proseso ng agent.

5. **Suriin ang token cache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Kung nabigo ito, nag-expire na ang token ng iyong CLI. Patakbuhin muli ang `az login`.

### 3.2 Gumagana ang token nang lokal ngunit hindi sa hosted deployment

**Pangunahing sanhi:** Gumagamit ang hosted agent ng system-managed identity na iba sa iyong personal na kredensyal.

**Ayusin:** Ito ay inaasahang gawi - ang managed identity ay awtomatikong naipoprovide sa panahon ng deployment. Kung nakakatanggap pa rin ang hosted agent ng mga error sa auth:
1. Suriin na ang managed identity ng Foundry project ay may access sa Azure OpenAI resource.
2. I-verify na tama ang `PROJECT_ENDPOINT` sa `agent.yaml`.

---

## 4. Mga error sa Modelo

### 4.1 Hindi makita ang Model deployment

```
Error: Model deployment not found / The specified deployment does not exist
```

**Ayusin - hakbang-hakbang:**

1. Buksan ang iyong `.env` file at tandaan ang halaga ng `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Buksan ang **Microsoft Foundry** sidebar sa VS Code.
3. Palawakin ang iyong project → **Model Deployments**.
4. Ihambing ang pangalan ng deployment na nakalista sa sidebar sa halaga sa iyong `.env`.
5. Ang pangalan ay **case-sensitive** - ang `gpt-4o` ay iba sa `GPT-4o`.
6. Kung hindi sila magkatugma, i-update ang iyong `.env` upang gamitin ang eksaktong pangalan na nakikita sa sidebar.
7. Para sa hosted deployment, i-update din ang `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Nagbibigay ang modelo ng hindi inaasahang nilalaman

**Ayusin:**
1. Suriin ang `EXECUTIVE_AGENT_INSTRUCTIONS` constant sa `main.py`. Siguraduhing hindi ito naputol o nasira.
2. Tingnan ang setting ng temperatura ng modelo (kung nako-configure) - mas mababang halaga ang nagbibigay ng mas deterministic na output.
3. Ihambing ang modelo na dineploy (hal., `gpt-4o` kumpara sa `gpt-4o-mini`) - magkaiba ang kakayahan ng mga modelo.

---

## 5. Mga error sa Deployment

### 5.1 ACR pull authorization

```
Error: AcrPullUnauthorized
```

**Pangunahing sanhi:** Hindi makapag-pull ang managed identity ng Foundry project ng container image mula sa Azure Container Registry.

**Ayusin - hakbang-hakbang:**

1. Buksan ang [https://portal.azure.com](https://portal.azure.com).
2. Hanapin ang **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** sa search bar sa itaas.
3. I-click ang registry na kaugnay ng iyong Foundry project (karaniwang nasa parehong resource group).
4. Sa kaliwang navigation, i-click ang **Access control (IAM)**.
5. I-click ang **+ Add** → **Add role assignment**.
6. Hanapin ang **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** at piliin ito. I-click ang **Next**.
7. Piliin ang **Managed identity** → i-click ang **+ Select members**.
8. Hanapin at piliin ang managed identity ng Foundry project.
9. I-click ang **Select** → **Review + assign** → **Review + assign**.

> Karaniwang awtomatikong itinatakda ng Foundry extension ang papel na ito. Kung nakita mo ang error na ito, maaaring nabigo ang awtomatikong setup. Maaari mo ring subukang muling i-deploy - maaaring i-retry ng extension ang setup.

### 5.2 Nabibigo ang agent na magsimula pagkatapos ng deployment

**Mga Senyales:** Nananatili ang katayuan ng container na "Pending" ng mahigit 5 minuto o nagpapakita ng "Failed".

**Ayusin - hakbang-hakbang:**

1. Buksan ang **Microsoft Foundry** sidebar sa VS Code.
2. I-click ang iyong hosted agent → piliin ang bersyon.
3. Sa detail panel, tingnan ang **Container Details** → hanapin ang seksyong **Logs** o link.
4. Basahin ang mga startup log ng container. Karaniwang sanhi:

| Mensahe ng Log | Sanhi | Ayusin |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Nawawalang dependency | Idagdag ito sa `requirements.txt` at muling i-deploy |
| `KeyError: 'PROJECT_ENDPOINT'` | Nawawalang environment variable | Idagdag ang env var sa `agent.yaml` sa ilalim ng `env:` |
| `OSError: [Errno 98] Address already in use` | Conflict sa port | Siguraduhing ang `agent.yaml` ay may `port: 8088` at iisang proseso lamang ang nakabind dito |
| `ConnectionRefusedError` | Hindi nagsimula ang agent sa pakikinig | Suriin ang `main.py` - ang tawag na `from_agent_framework()` ay dapat tumakbo sa startup |

5. Ayusin ang isyu, pagkatapos ay muling i-deploy mula sa [Module 6](06-deploy-to-foundry.md).

### 5.3 Nag-timeout ang deployment

**Ayusin:**
1. Suriin ang iyong koneksyon sa internet - maaaring malaki ang Docker push (>100MB sa unang deploy).
2. Kung nasa likod ng corporate proxy, siguraduhing naayos ang proxy settings sa Docker Desktop: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Subukang muli - maaaring pansamantalang problema lang ang network.

---

## 6. Mabilisang sanggunian: Mga papel sa RBAC

| Papel | Karaniwang saklaw | Ano ang ibinibigay nito |
|------|---------------|----------------|
| **Azure AI User** | Project | Mga data action: gumawa, mag-deploy, at mag-invoke ng agents (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Project o Account | Data actions + paggawa ng project |
| **Azure AI Owner** | Account | Buong access + pamamahala ng role assignments |
| **Azure AI Project Manager** | Project | Data actions + maaaring magtalaga ng Azure AI User sa iba |
| **Contributor** | Subscription/RG | Mga management actions (gumawa/bura ng resources). **Hindi kabilang ang data actions** |
| **Owner** | Subscription/RG | Management actions + role assignment. **Hindi kabilang ang data actions** |
| **Reader** | Anumang antas | Read-only management access |

> **Mahalagang tandaan:** Ang `Owner` at `Contributor` ay **HINDI** kasama ang data actions. Kailangan mo palaging isang `Azure AI *` na papel para sa mga operasyon ng agent. Ang pinakamababang papel para sa workshop na ito ay **Azure AI User** sa saklaw na **project**.

---

## 7. Checklist para sa kompletong workshop

Gamitin ito bilang huling pirmahan na natapos mo na ang lahat:

| # | Item | Module | Pumasa? |
|---|------|--------|---|
| 1 | Lahat ng kinakailangan ay naka-install at nasigurong gumagana | [00](00-prerequisites.md) | |
| 2 | Na-install ang Foundry Toolkit at Foundry extensions | [01](01-install-foundry-toolkit.md) | |
| 3 | Nalikha ang Foundry project (o napili ang umiiral na project) | [02](02-create-foundry-project.md) | |
| 4 | Naipadala ang modelo (hal., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Na-assign ang Azure AI User role sa saklaw ng proyekto | [02](02-create-foundry-project.md) | |
| 6 | Na-scaffold ang hosted agent project (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | Na-configure ang `.env` gamit ang PROJECT_ENDPOINT at MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Na-customize ang mga tagubilin ng agent sa main.py | [04](04-configure-and-code.md) | |
| 9 | Nalikha ang virtual environment at na-install ang mga dependencies | [04](04-configure-and-code.md) | |
| 10 | Nasubukan ang agent nang lokal gamit ang F5 o terminal (nakapasa sa 4 na smoke test) | [05](05-test-locally.md) | |
| 11 | Naipadala sa Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Ipinapakita ng status ng container ang "Started" o "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Naverify sa VS Code Playground (nakapasa sa 4 na smoke test) | [07](07-verify-in-playground.md) | |
| 14 | Naverify sa Foundry Portal Playground (nakapasa sa 4 na smoke test) | [07](07-verify-in-playground.md) | |

> **Pagbati!** Kung lahat ng item ay naka-tsek na, natapos mo na ang buong workshop. Nakabuo ka ng hosted agent mula sa simula, nasubukan ito nang lokal, naipadala sa Microsoft Foundry, at na-validate ito sa produksiyon.

---

**Nakaraan:** [07 - Verify in Playground](07-verify-in-playground.md) · **Bahay:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pahayag ng Pagtanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyong AI na pagsasalin na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong mga pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatumpak. Ang orihinal na dokumento sa kanyang katutubong wika ang dapat ituring na pangunahing pinagmulan. Para sa mga kritikal na impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->