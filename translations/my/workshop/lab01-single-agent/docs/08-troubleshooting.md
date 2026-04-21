# Module 8 - ပြဿနာဖြေရှင်းခြင်း

ဒီ module က အလုပ်ရုံဆွေးနွေးပွဲအတွင်း တွေ့ကြုံရသော ပုံမှန်ပြဿနာတစ်ခုချင်းစီအတွက် အညွှန်းလမ်းညွှန်ဖြစ်ပါတယ်။ Bookmark လုပ်ပါ - အခြေအနေမမှန်လာတဲ့အခါ မည်သည့်အချိန်မဆို ပြန်လည်ကြည့်ရှုနိုင်ပါမယ်။

---

## 1. ခွင့်ပြုချက်အမှားများ

### 1.1 `agents/write` ခွင့်ပြုချက် ပိတ်ထားသည်

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**အကြောင်းရင်း:** သင်မှာ **project** အဆင့်တွင် `Azure AI User` role မရှိပါ။ Workshop ထဲမှာ အများဆုံး ဖြစ်ပေါ်သော အမှားဖြစ်သည်။

**ပြင်ဆင်ရန် - အဆင့်လိုက်:**

1. [https://portal.azure.com](https://portal.azure.com) ကိုဖွင့်ပါ။
2. အပေါ်ဆုံးရှာဖွေမှုဘားတွင် သင့် **Foundry project** အမည် (ဥပမာ `workshop-agents`) ကို ရိုက်ထည့်ပါ။
3. **အရေးကြီး:** ရလဒ်ထဲမှ **"Microsoft Foundry project"** အမျိုးအစားပြထားသောအရာကိုနှိပ်ပါ၊ မဟုတ်ရင် parent account/hub resource ကို မနှိပ်ပါနှင့်။ ၎င်းတို့သည် မတူညီသော RBAC scope များဖြစ်သည်။
4. project စာမျက်နှာ၏ ဘယ်ဘက် navigation မှာ **Access control (IAM)** ကိုနှိပ်ပါ။
5. **Role assignments** tab ကိုနှိပ်၍ သင့်မှာ role ရှိမရှိ ထောက်လှမ်းပါ။
   - သင့်နာမည် သို့မဟုတ် အီးမေးလ်ကို ရှာဖွေပါ။
   - `Azure AI User` ရှိပြီးသားဆို → အမှားအကြောင်းတခြားတစ်ခုပဲဖြစ်သည် (အောက်မှာ Step 8 ကိုကြည့်ပါ)။
   - မရှိဘဲရှိကောင်း → ထည့်သွင်းရန် ဆက်လုပ်ပါ။
6. **+ Add** → **Add role assignment** ကိုနှိပ်ပါ။
7. **Role** tab တွင်
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) ကို ရှာဖွေပါ။
   - ရလဒ်ထဲမှ ရွေးပါ။
   - **Next** ကိုနှိပ်ပါ။
8. **Members** tab တွင်
   - **User, group, or service principal** ကိုရွေးပါ။
   - **+ Select members** ကိုနှိပ်ပါ။
   - သင့်နာမည် သို့မဟုတ် အီးမေးလ်လိပ်စာကို ရှာပါ။
   - ရလဒ်ထဲမှ ကိုယ်တိုင်ကို ရွေးပါ။
   - **Select** ကိုနှိပ်ပါ။
9. **Review + assign** → ထပ်မံ **Review + assign** ကိုနှိပ်ပါ။
10. **၁-၂ မိနစ် စောင့်ပါ** - RBAC ပြောင်းလဲမှုများ သက်ရောက်ရန် အချိန်ယူသည်။
11. ပျက်ကွက်ခဲ့သော လုပ်ဆောင်ချက်ကို ထပ်မံလုပ်ဆောင်ပါ။

> **Owner/Contributor သာမကကြောင်း:** Azure RBAC တွင် ခွင့်ပြုချက်နှစ်မျိုးရှိသည် - *management actions* နှင့် *data actions*။ Owner နှင့် Contributor တွင် resource ဖန်တီးခြင်း၊ ဆက်တင်ပြင်ဆင်ခြင်းစသည့် management actions များ ရှိသော်လည်း agent လုပ်ဆောင်ချက်များအတွက် `agents/write` **data action** လိုအပ်သည်၊ ၎င်းသည် `Azure AI User`, `Azure AI Developer`, သို့မဟုတ် `Azure AI Owner` role များတွင်သာပါဝင်သည်။ [Foundry RBAC documentation](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ကို ကြည့်ရှုပါ။

### 1.2 ရင်းမြစ် ထည့်သွင်းစဉ် `AuthorizationFailed` ဖြစ်ခြင်း

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**အကြောင်းရင်း:** သင်သည် ဤ subscription/resource group တွင် Azure ရင်းမြစ်များ ဖန်တီးခြင်း သို့မဟုတ် ပြင်ဆင်ခြင်း ခွင့်မရှိပါ။

**ပြင်ဆင်ရန်:**
1. သင့် subscription အက်မင်ကို Foundry project ရှိ resource group တွင် **Contributor** role သတ်မှတ်ရန် တောင်းဆိုပါ။
2. ဒဖိုသို့မဟုတ် Foundry project ကို သင့်အတွက် ဖန်တီးပေးပြီး project အတွက် **Azure AI User** role ပေးရန် တောင်းဆိုနိုင်သည်။

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) အတွက် `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**အကြောင်းရင်း:** Foundry အသုံးပြုရန် လိုအပ်သော resource provider ကို Azure subscription မှ မှတ်ပုံတင် မထားသေးပါ။

**ပြင်ဆင်ရန်:**

1. တမန်နယ်ဖွင့်ပြီး အောက်ပါကို run ပါ -
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```

2. မှတ်ပုံတင် ပြီးစီးသည်ထိ (၁ မှ ၅ မိနစ်ကြားကြာနိုင်သည်) စောင့်ပါ -
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   မျှော်မှန်း output: `"Registered"`
3. လုပ်ဆောင်ချက်ကို ထပ်မံကြိုးစားပါ။

---

## 2. Docker အမှားများ (Docker ထည့်သွင်းထားပါကသာ)

> Docker သည် ဒီ workshop အတွက် **အလိုလျောက်မဟုတ်ပါ**။ ယင်းမှတ်ချက်များသည် သင် Docker Desktop ထည့်သွင်းထားပြီး Foundry extension က local container build လုပ်သောအခါ သက်သာသည့် အမှားများသာ ဖြစ်သည်။

### 2.1 Docker daemon မစတင်ခြင်း

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**ပြင်ဆင်ရန် - အဆင့်လိုက်:**

1. သင့် Start menu (Windows) သို့မဟုတ် Applications (macOS) မှ **Docker Desktop** ကို ရှာဖွေဖွင့်ပါ။
2. Docker Desktop ပြတင်းပေါ်တွင် **"Docker Desktop is running"** မပြရသည်ထိ ကာလ ၃၀ မှ ၆၀ စက္ကန့် စောင့်ပါ။
3. System tray (Windows) သို့မဟုတ် menu bar (macOS) တွင် Docker ရေပန်းရိုင်း icon ရှိနေမရှိ ကြည့်ပါ။ အခြေအနေကို အတည်ပြုရန် hover လုပ်၍ကြည့်ပါ။
4. တမန်နယ်တစ်ခုတွင် အောက်ပါ command run လုပ်၍ စစ်ဆေးပါ -
   ```powershell
   docker info
   ```
   Docker စနစ်အချက်အလက် (Server Version, Storage Driver စသည်) ပုံစံအသစ် ပြသည်ဆို Docker စတင်နေသည်။
5. **Windows အတွက် အထူးသဖြင့်:** Docker မစတင်ပါက -
   - Docker Desktop → **Settings** (gear icon) → **General** ကိုဖွင့်ပါ။
   - **Use the WSL 2 based engine** ကိုစစ်ဆေးပါ။
   - **Apply & restart** ကိုနှိပ်ပါ။
   - WSL 2 မထည့်သွင်းထားပါက PowerShell မှာ `wsl --install` ကို administrator ပါဝါဖြင့် run လုပ်ပြီး computer ကို restart လုပ်ပါ။
6. ပြန်လည် deploy ပြုလုပ်ပါ။

### 2.2 Docker build တွင် dependency အမှား

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**ပြင်ဆင်ရန်:**
1. `requirements.txt` ဖိုင်ရှိ အကုဒ်စာရင်းများမှန်ကန်စွာ ရိုက်ထားပါစေ။
2. ဗားရှင်း pinning မှန်ကန်မှုကို စစ်ဆေးပါ -
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```

3. ဒေသတွင်း install လုပ်၍ စမ်းသပ်ပါ -
   ```bash
   pip install -r requirements.txt
   ```

4. ပုဂ္ဂလိက package မရှိမဖြစ်လိုအပ်ပါက Docker ကို network access ရှိစေရန် စစ်ဆေးပါ။

### 2.3 Container platform မကိုက်ညီမှု (Apple Silicon)

Apple Silicon Mac (M1/M2/M3/M4) မှ deployment လုပ်သောအခါ `linux/amd64` အတွက် container ကိုသာ တည်ဆောက်ရမည်ဖြစ်သည်၊ အကြောင်းက Foundry ရဲ့ container runtime က AMD64 ကုဒ်မှအသုံးပြုခြင်းဖြစ်ပါသည်။

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry extension ရဲ့ deploy command က ၎င်းကို များသောအားဖြင့် အလိုအလျောက် ကိုင်တွယ်ပေးသည်။ architecture ဆိုင်ရာ အမှားတွေမြင်ရင်၊ `--platform` flag ဖြင့် manual တည်ဆောက်ပြီး Foundry အဖွဲ့ကို ဆက်သွယ်ပါ။

---

## 3. အတည်ပြုခွင့် အမှားများ

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) မှ token ရယူရန် မအောင်မြင်ခြင်း

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**အကြောင်းရင်း:** `DefaultAzureCredential` လျှှောက်လွှာတွင် အမှန်တကယ် token ရနိုင်သော credential source မရှိပါ။

**ပြင်ဆင်ရန် - အဆင့်လိုက်ကြိုးစားပါ:**

1. **Azure CLI မှ ပြန်လည် login ဝင်ပါ** (အများဆုံး စစ်မှန်သော နည်းလမ်း) -
   ```bash
   az login
   ```
   browser တစ်ခုဖွင့်ပါ။ လော့ဂ်အင်ပြီး ရောက်လာပါ။

2. **မှန်ကန်သော subscription ကို သတ်မှတ်ပါ:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   မမှန်ပါက -
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code မှ ပြန်လည် login ဝင်ပါ:**
   - VS Code ၏ ဘယ်အောက်သို့အကောင့် (Accounts) အိုင်ကွန်ကို နှိပ်ပါ။
   - သင့်အကောင့်နာမည် → **Sign Out** ကိုရွေးပါ။
   - Accounts icon ထပ်နှိပ်ပြီး → **Sign in to Microsoft** ကိုရွေးပါ။
   - browser login လုပ်ကိုယ်ထမ်း ပြီးစီးပါ။

4. **Service principal (CI/CD အခြေအနေများအတွက်သာ):**
   - `.env` တွင် အောက်ပါ environment variables များ သတ်မှတ်ပါ -
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```

   - ထို့နောက် agent လုပ်ငန်းစဉ်ကို ပြန်စတင်ပါ။

5. **token cache ကို စစ်ဆေးပါ:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```

   ယင်း မအောင်မြင်ပါက CLI token သက်တမ်းကုန်ဆုံးသွားသည်; `az login` ကို ပြန်လည် run ပါ။

### 3.2 Token ကို ဒေသတွင်းအောင်မြင် သော်လည်း hosted deployment တွင် မအောင်မြင်ခြင်း

**အကြောင်းရင်း:** Hosted agent သည် system-managed identity ကို အသုံးပြုသည်၊ သင်၏ ကိုယ်ပိုင် credentials နှင့် မတူပါ။

**ပြင်ဆင်ရန်:** ဤသည်မှာ မျှော်မမှန်သောအပြုအမူ ဖြစ်သည်။ Deployment သည် managed identity ကို ကိုယ်တိုင်ထုတ်ပေးသည်။ Hosted agent အကောင့်မှ auth အမှားရှိသေးလျှင် -
1. Foundry project ရဲ့ managed identity ဖြင့် Azure OpenAI resource ရရှိနိုင်ပြီး သင့်တော်သည်ကို စစ်ဆေးပါ။
2. `agent.yaml` ထဲရှိ `PROJECT_ENDPOINT` မှန်ကန်မှုရှိကြောင်း အတည်ပြုပါ။

---

## 4. Model အမှားများ

### 4.1 Model deployment မတွေ့ရှိခြင်း

```
Error: Model deployment not found / The specified deployment does not exist
```

**ပြင်ဆင်ရန် - အဆင့်လိုက်:**

1. သင့် `.env` ဖိုင်ထဲရှိ `AZURE_AI_MODEL_DEPLOYMENT_NAME` တန်ဖိုးကို မှတ်သားပါ။
2. VS Code မှ **Microsoft Foundry** sidebar ကိုဖွင့်ပါ။
3. သင့် project ကို ဖွင့်ပြပြီး → **Model Deployments** ကိုရှာပါ။
4. deployment အမည်ကို sidebar တွင်ပြထားသော နာမည်နှင့် `.env` မှ ကိုက်ညီမှုရှိကြောင်း နှိုင်းယှဉ်ပါ။
5. နာမည်သည် **case-sensitive** ဖြစ်သည် - `gpt-4o` နှင့် `GPT-4o` မတူပါ။
6. မကိုက်ညီပါက `.env` ထည့်သွင်းထားသော အမည်ကို sidebar တွင်ပြထားသည်နှင့် တိကျစွာ ပြင်ဆင်ပါ။
7. hosted deployment အတွက် `agent.yaml` ကိုလည်း မျိုးလိုအပ်ပါက ပြင်ဆင်ပါ။
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model မှ မျှော်လင့်မထားသော အကြောင်းအရာ ဖြင့် ပြန်ကြားသည်

**ပြင်ဆင်ရန်:**
1. `main.py` ဖိုင်ရှိ `EXECUTIVE_AGENT_INSTRUCTIONS` constant ကို ပြန်လည်စစ်ဆေးပါ။ ထောင့် ထိန်း ချုပ်တော့ခြင်း သို့မဟုတ် ပြင်လဲခံရခြင်း မရှိကြောင်း သေချာစေရန်။
2. Model temperature ကို စစ်ဆေးပါ (ပြင်ဆင်နိုင်ပါက) - လျော့နည်းသော တန်ဖိုးများသည် စနစ်တကျဖြစ်စေသည်။
3. ရရှိထားသော model (ဥပမာ `gpt-4o` 與 `gpt-4o-mini`) ကို နှိုင်းယှဉ်ပါ - model များကွဲပြားမှုများရှိသည်။

---

## 5. Deployment အမှားများ

### 5.1 ACR pull ခွင့်ပြုချက်

```
Error: AcrPullUnauthorized
```

**အကြောင်းရင်း:** Foundry project ရဲ့ managed identity က Azure Container Registry မှ container ပုံရိပ်ကို မဆွဲနိုင်ပါ။

**ပြင်ဆင်ရန် - အဆင့်လိုက်:**

1. [https://portal.azure.com](https://portal.azure.com) ကိုဖွင့်ပါ။
2. အပေါ်ဆုံးရှာဖွေမှုဘားတွင် **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** ရှာပါ။
3. သင့် Foundry project နှင့်ဆက်စပ်သော registry ကိုနှိပ်ပါ (လက်ရှိ resource group တူနေတာ ဖြစ်နိုင်ပါသည်)။
4. ဘယ် navigation ကို နှိပ်ပြီး **Access control (IAM)** ကိုရွေးပါ။
5. **+ Add** → **Add role assignment** ကိုနှိပ်ပါ။
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** ကို ရှာပြီး ရွေးပါ။ **Next** နှိပ်ပါ။
7. **Managed identity** ကို ရွေးပြီး → **+ Select members** ကိုနှိပ်ပါ။
8. Foundry project ရဲ့ managed identity ကို ရှာ၍ ရွေးချယ်ပါ။
9. **Select** → **Review + assign** → ထပ်မံ **Review + assign** နှိပ်ပါ။

> ၎င်း role assignment ကို Foundry extension မှ ပုံမှန်အားဖြင့် အလိုအလျောက် ပြုလုပ်ပေးသည်။ အမှားဖြစ်ပါက automatic setup မအောင်မြင်ခြင်း ဖြစ်နိုင်ပြီး ပြန်လည် deploy လုပ်ကြည့်ပါ - extension က setup ကို ထပ်တလဲလဲ ကြိုးစားနိုင်ပါသည်။

### 5.2 Agent deployment အပြီး စတင်မလုပ်ခြင်း

**လက္ခဏာများ:** Container status သည် ၅ မိနစ်ထက် မပြတ် ဖော်ပြချက် "Pending" သို့မဟုတ် "Failed" ဖြစ်သည်။

**ပြင်ဆင်ရန် - အဆင့်လိုက်:**

1. VS Code မှ **Microsoft Foundry** sidebar ကိုဖွင့်ပါ။
2. သင့် hosted agent ကိုနှိပ်ပြီး → ဗားရှင်းရွေးချယ်ပါ။
3. အသေးစိတ် panel တွင် **Container Details** → **Logs** အပိုင်း သို့မဟုတ် လင့်ခ်ကို ရှာပါ။
4. Container စတင်မှု log များကို ဖတ်ပါ။ ပုံမှန် ဖြစ်ရပ်များ -

| Log message | အကြောင်းရင်း | ပြင်ဆင်နည်း |
|-------------|--------------|--------------|
| `ModuleNotFoundError: No module named 'xxx'` | Dependency မရှိခြင်း | `requirements.txt` တွင် ထည့်သွင်း ပြီး redeploy လုပ်ပါ |
| `KeyError: 'PROJECT_ENDPOINT'` | Environment variable မထည့်သွင်းခြင်း | `agent.yaml` ထဲ `env:` အောက်တွင် ထည့်သွင်းပါ |
| `OSError: [Errno 98] Address already in use` | Port conflicts ဖြစ်ခြင်း | `agent.yaml` တွင် `port: 8088` ဖြင့် သတ်မှတ်၍ တစ်ခုတည်းသောလုပ်ငန်းစဉ်သာ bind ဖြစ်စေရန် |
| `ConnectionRefusedError` | Agent စတင်၍ နားထောင်ခြင်း မလုပ်သည့်အတွက် | `main.py` မှာ `from_agent_framework()` ကို စတင်သည့်အချိန် run လိုက်ရန် |

5. ပြဿနာကို ရှာဖွေပြီး ပြုပြင်ပြီးနောက် [Module 6](06-deploy-to-foundry.md) မှ ပြန် deploy လုပ်ပါ။

### 5.3 Deployment အချိန်ကုန်

**ပြင်ဆင်ရန်:**
1. သင့်အင်တာနက် ချိတ်ဆက်မှုကို စစ်ဆေးပါ - Docker push က အကြီး (>100MB အထိ ပထမဆုံး deploy အတွက်) ဖြစ်နိုင်သည်။
2. ကော်ပိုရေးရှင်း proxy အောက်တွင်ရှိပါက Docker Desktop proxy ဆက်တင်များကို စစ်ဆေးပါ: **Docker Desktop** → **Settings** → **Resources** → **Proxies**।
3. နောက်တစ်ကြိမ် ပြန်ကြိုးစားပါ၊ ကွန်ယက်နောက်ခံလုပ်ဆောင်မှုများ ကြားကာ ပြဿနာဖြစ်နိုင်ပါသည်။

---

## 6. အလျင်အမြန် အညွှန်း: RBAC roles

| Role | ရိုးရိုး scope | ပေးသော ခွင့်ပြုချက်များ |
|------|---------------|-------------------------|
| **Azure AI User** | Project | Data actions: agent ကို တည်ဆောက်၊ deploy နှင့် ခေါ်ယူခြင်း (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Project သို့မဟုတ် Account | Data actions + project ဖန်တီးခြင်း |
| **Azure AI Owner** | Account | အပြည့်အစုံ ဝင်ရောက်ခွင့် + role assignment စီမံခန့်ခွဲမှု |
| **Azure AI Project Manager** | Project | Data actions + Azure AI User ကိုအခြားသူများအတွက် သတ်မှတ်နိုင်ခြင်း |
| **Contributor** | Subscription/RG | Management actions (resources ဖန်တီး/ဖျက်)။ **Data actions မပါဝင်ပါ** |
| **Owner** | Subscription/RG | Management actions + role assignment။ **Data actions မပါဝင်ပါ** |
| **Reader** | ဘယ်သည့်အဆင့်မဆို | ဖတ်ခြင်းသာဝင်ရောက်ခွင့် |

> **အဓိကလက်ခံချက်:** `Owner` နှင့် `Contributor` များမှာ data actions မပါဝင်ပါ။ Agent လုပ်ငန်းများအတွက် အမြဲတမ်း `Azure AI *` role လိုအပ်ပါသည်။ ဒီ workshop အတွက်အနည်းဆုံး role ဖြစ်တာက **Azure AI User** ဖြစ်ပြီး **project** scope မှာ သတ်မှတ်ထားရပါမယ်။

---

## 7. Workshop ပြီးစီးကြောင်း စစ်ဆေးရန် စာရင်း

အောက်ပါအတိုင်း သင်အားလုံး ပြီးစီးကြောင်း ကို သတ်မှတ်ပါ -

| # | အချက်အလက် | Module | ဖြတ်သန်းပြီး? |
|---|-------------|--------|---------------|
| 1 | အားလုံး လိုအပ်ချက်များ ထည့်သွင်းပြီး စစ်ဆေးထားသည် | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit နှင့် Foundry extensions ထည့်သွင်းထားသည် | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry project အသစ် ဖန်တီးထားသည် (သို့မဟုတ် ရှိပြီးသား project ရွေးချယ်ထားသည်) | [02](02-create-foundry-project.md) | |
| 4 | မော်ဒယ် တပ်ဆင်ပြီး (ဥပမာ gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI အသုံးပြုသူ အခန်းကဏ္ဍကို ပရောဂျက်အကွက်တွင် ခန့်အပ်ပြီး | [02](02-create-foundry-project.md) | |
| 6 | Hosted agent ပရောဂျက် အခြေခံဖိုင်တည်ဆောက်ပြီး (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` ကို PROJECT_ENDPOINT နှင့် MODEL_DEPLOYMENT_NAME ဖြင့် ပြင်ဆင်ပြီး | [04](04-configure-and-code.md) | |
| 8 | main.py တွင် Agent အညွှန်းများကို လက်ဆောင်ပြင်ဆင်ပြီး | [04](04-configure-and-code.md) | |
| 9 | Virtual environment ဖန်တီးပြီး မှီခိုဖိုင်များ တပ်ဆင်ပြီး | [04](04-configure-and-code.md) | |
| 10 | Agent ကို ဒေသတွင်းတွင် F5 သို့မဟုတ် terminal ဖြင့် စစ်ဆေးပြီး (smoke test ၄ ခု ကျော်) | [05](05-test-locally.md) | |
| 11 | Foundry Agent Service သို့ တပ်ဆင်ပြီး | [06](06-deploy-to-foundry.md) | |
| 12 | ကွန်တိန်နာ အခြေအနေ "Started" သို့မဟုတ် "Running" ဟု ပြသသည် | [06](06-deploy-to-foundry.md) | |
| 13 | VS Code Playground တွင် အတည်ပြုပြီး (smoke test ၄ ခု ကျော်) | [07](07-verify-in-playground.md) | |
| 14 | Foundry Portal Playground တွင် အတည်ပြုပြီး (smoke test ၄ ခု ကျော်) | [07](07-verify-in-playground.md) | |

> **ကံကောင်းပါစေ!** အချက်အားလုံးစစ်ဆေးထားပါက စစ်ဆေးမှု အစုံကို ဖျော်ဖြေပြီးဖြစ်သည်။ သင်သည် hosted agent ကို မူလကနေတည်ဆောက်ပြီး ဒေသတွင်းအတွက် စမ်းသပ်ပြီး Microsoft Foundry တွင် တပ်ဆင်ပြီး ထုတ်လုပ်မှုအတွက် အတည်ပြုပြီးဖြစ်သည်။

---

**အရင်စာမျက်နှာ:** [07 - Verify in Playground](07-verify-in-playground.md) · **ပင်မစာမျက်နှာ:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**အကြောင်းကြားချက်**:  
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးစားပါသော်လည်း ဆော့ဖ်ဝဲမှန်ကန်မှုတွင် အမှားများ သို့မဟုတ် မှန်ကန်မှုနည်းပါးမှုများ ရှိနိုင်ကြောင်း သိရှိရန်လိုအပ်ပါသည်။ မူရင်းစာတမ်း၏ မိသားစကားအတိုင်းသာ အတည်ပြုရင်းမြစ်အဖြစ် ယူဆသင့်ပါသည်။ အရေးကြီးသော သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူ၏ ဘာသာပြန်ချက်ကို အကြံပြုအပ်ပါသည်။ ဤဘာသာပြန်မှု အသုံးပြုမှုကြောင့် ဖြစ်ပေါ်လာသော နားလည်မှုစွဲလမ်းမှုများ သို့မဟုတ် မှားယွင်းဖတ်ယူမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မယူပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->