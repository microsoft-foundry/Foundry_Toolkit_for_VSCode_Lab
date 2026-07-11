# မော်ဂျူး ၈ - ပြဿနာဖြေရှင်းခြင်း

ဤမော်ဂျူးသည် သာမန်ပြဿနာများအတွက် ကိုးကားလမ်းညွှန်စာအုပ် ဖြစ်သည်။ အမှတ်တံဆိပ်ထားပြီး မည်သည့်ပြဿနာဖြစ်ပါက ပြန်လည်သွားပါ။

---

## ၁။ ခွင့်ပြုချက်အမှားများ

### ၁.၁ `agents/write` ခွင့်ပြုချက် လက်မခံခြင်း

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**ဘာကြောင့်ဖြစ်တာလဲ။**  **project** အဆင့်တွင် `Azure AI User` အခန်းကဏ္ဍ ပျောက်ဆုံးနေခြင်း။  ဤသည်သည် အမှား#1 ဖြစ်သည်။

**ဖြေရှင်းနည်း-**
၁။ [portal.azure.com](https://portal.azure.com) ကိုဖွင့်ပါ။
၂။ သင့် Foundry **project** နာမည်ကို ရှာဖွေ→ **"Microsoft Foundry project"** (အဖိုးတန် parent အကောင့်မဟုတ်ပါ) အမျိုးအစားရလဒ်ကို နှိပ်ပါ။
၃။ **Access control (IAM)** → **+ Add** → **Add role assignment** ကိုနှိပ်ပါ။
၄။ အခန်းကဏ္ဍ: **Azure AI User** → Next ကိုနှိပ်ပါ။
၅။ အဖွဲ့ဝင်များ: သင့်ကိုယ်ကို ရွေးပါ → Review + assign → Review + assign ကိုနှိပ်ပါ။
၆။ **၁–၂ မိနစ် စောင့်ပါ** → ထပ်မံကြိုးစားပါ။

> **ဘာကြောင့် Owner/Contributor သာမက ဒါလုံလောက်လဲ မဟုတ်တာ။** ဤအခန်းကဏ္ဍများသည် *စီမံခန့်ခွဲမှု* လုပ်ဆောင်ချက်များသာ ပေးသည်။ Agent လုပ်ဆောင်မှုများအတွက် `agents/write` *ဒေတာ လုပ်ဆောင်ချက်* လိုအပ်သည်၊ ၎င်းသည် `Azure AI User`, `Azure AI Developer`, သို့မဟုတ် `Azure AI Owner` မှသာ ပေးသည်။ [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) တွင်ကြည့်ပါ။

### ၁.၂ `AuthorizationFailed` provisioning လုပ်စဉ်တွင်ဖြစ်သည်

**ဖြေရှင်းနည်း**: သင့်အက်မင်အား resource group တွင် **Contributor** ခန့်အပ်ရန် လိုအပ်သည်၊ သို့မဟုတ် သူတို့က project ကို ဖန်တီးပြီး သင့်အား **Azure AI User** ပေးစတင်ပါစေ။

### ၁.၃ `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# "သိမ်းဆည်းပြီး" ဆိုသည်အထိ စောင့်ပါ။
```

---

## ၂။ Docker အမှားများ

> Docker သည် **နောက်ခံရွေးချယ်စရာ** ဖြစ်သည်။ ဤအမှားများမှာ Docker Desktop ထည့်သွင်းပြီး extension မှ ဒေသတွင်း တည်ဆောက်မှု ပြုလုပ်သောအခါတွင်သာ အသက်ဝင်သည်။

### ၂.၁ Docker daemon မလည်ပတ်ခြင်း

**ဖြေရှင်းနည်း**: Docker Desktop ကို စတင်ထားပါ → "running" အခြေအနေကို စောင့်ပါ → `docker info` ဖြင့်အတည်ပြုပါ → ထပ်မံကြိုးစားပါ။

### ၂.၂ ဆောက်လုပ်မှုတွင် ချို့ယွင်းချက်များရှိခြင်း

**ဖြေရှင်းနည်း**: `requirements.txt` စာလုံးပေါင်းမှန်မှန် ဆောင်ရွက်ပါ၊ ဒေသတွင်းစမ်းသပ်ပါ: `pip install -r requirements.txt`။

### ၂.၃ ပလက်ဖောင်း မကိုက်ညီမှု (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## ၃။ အတည်ပြုချက်အမှားများ

### ၃.၁ `DefaultAzureCredential` မအောင်မြင်ခြင်း

**ဖြေရှင်းနည်း (အဆင့်လိုက်စမ်းကြည့်ပါ):**
၁။ `az login` (ပြန်လည် အတည်ပြုရန်)
၂။ `az account set --subscription "<id>"` (မှန်ကန်သော subscription)
၃။ VS Code → Accounts → Sign Out → ပြန်လည် Sign In ပြုလုပ်ပါ
၄။ စစ်ဆေးရန်: `az account get-access-token --resource https://cognitiveservices.azure.com`

### ၃.၂ locally မှာ token အလုပ်လုပ်သော်လည်း hosted တွင်မဟုတ်

**မျှော်မှန်းချက်**: Hosted agents များသည် système ၏စီမံခန့်ခွဲထားသောအိုင်ဒင်တစ်တစ်ကို အသုံးပြုသည်၊ သင့် credential မဟုတ်ပါ။ Hosted agent များတွင် auth အမှားများ ရှိပါက-
-  `agent.yaml` မှာ `AZURE_AI_PROJECT_ENDPOINT` မှန်ကန်ကြောင်း အတည်ပြုပါ
- project ၏ စီမံခန့်ခွဲထားသောအိုင်ဒင်တစ်တစ်တွင် model ခွင့်ပြုချက်ရှိကြောင်း စစ်ဆေးပါ

---

## ၄။ ပုံစံအမှားများ

### ၄.၁ ပုံစံ တပ်ဆင်မှု မတွေ့ပါ

**ဖြေရှင်းနည်း**: နာမည်သည် **အက္ခရာ အမည်အတိုင်း** ဖြစ်ရမည်။ `.env` မှ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ကို Foundry sidebar → Models တွင်ရှိသည့် မှန်ကန်သောနာမည်နှင့် နှိုင်းယှဉ်ပါ။

### ၄.၂ မမျှော်လင့်သည့် ပုံစံ output

**ဖြေရှင်းနည်း**: `main.py` မှ  `AGENT_INSTRUCTIONS` ကို ပြန်လည်ကြည့်ရှုပါ (တောက်လျောက် မဖြတ်ထားပါကလား?)။ မတူညီသော ပုံစံ (e.g., `gpt-4.1` နှင့် `gpt-4.1-mini`) ကို စမ်းပါ။

---

## ၅။ တပ်ဆင်မှု အမှားများ

### ၅.၁ ACR pull ခွင့်မရှိခြင်း

**ဖြေရှင်းနည်း**: Azure Portal → Container Registry → Access control (IAM) → Foundry project ၏ စီမံခန့်ခွဲထားသောအိုင်ဒင်တစ်တစ်သို့  **AcrPull** အခန်းကဏ္ဍ ပေါင်းထည့်ပါ။

### ၅.၂ Agent စတင်မရ ( "Pending" သို့မဟုတ် "Failed" အနေအထားတွင် ဆက်ထား)

Sidebar တွင် container log များကို စစ်ဆေးပါ။ ပုံမှန် ဖြစ်ရပ်များ-

| Log message | Fix |
|-------------|-----|
| `ModuleNotFoundError` | `requirements.txt` ထဲတွင် လက်မဲ့ package ကို ထည့်သွင်းပါ၊ ပြန်တပ်ဆင်ပါ |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | `agent.yaml` ၏ `environment_variables` အောက်တွင် env var ထည့်ပါ |
| `Address already in use` | ပေါ့တ် 8088 သည် တစ်ခုတည်းသော လုပ်ငန်းစဉ်မှသာ bind ဖြစ်ရန် သေချာပါစေ |

### ၅.၃ တပ်ဆင်မှု စောင့်နေရမှု

**ဖြေရှင်းနည်း**: အင်တာနက် ချိတ်ဆက်မှုကို စစ်ဆေးပါ။ ပထမဆုံး တပ်ဆင်မှုမှာ >100MB  ဖြစ်သည်။ Proxy အောက်မှာလား? Docker Desktop proxy ဖက်ဆက်မှုကို ဆက်တင်ပြုပြင်ပါ။

---

## ၆။ လမ်းကြောင်း B - Foundry Local

### ၆.၁ Foundry Local မစတင်နိုင်ခြင်း

| ပြဿနာ | ဖြေရှင်းနည်း |
|-------|-----|
| `foundry: command not found` | ပြန်တပ်ဆင်ရန်: `winget install Microsoft.FoundryLocal` |
| အရင်းအမြစ် မလုံလောက်ခြင်း | Foundry Local သည် ~4GB RAM လွတ်ငွေလိုသည်။ အခြား app များပိတ်ပါ။ |
| ပုံစံ ဒေါင်းလုပ်မရ | ဒစ်စက့် နေရာစစ်ဆေးပါ (ပုံစံများမှာ 2–8 GB)။ ထပ်မံစမ်းသပ်ရန်: `foundry local models pull <name>` |

### ၆.၂ Foundry Local ပုံစံ အမှားများ

| ပြဿနာ | ဖြေရှင်းနည်း |
|-------|-----|
| တုံ့ပြန်ချက် အနည်းငယ် နှေးကွေးခြင်း | မျှော်လင့်ရ - ဒေသတွင်းပုံစံများသည် GPU မရှိသည့် CPU ပေါ်တွင် လည်ပတ်သည်။ သည်းခံပါ။ |
| ထွက်ရှိမှု အရည်အသွေး မကောင်းခြင်း | သင့် ဟာဒ်ဝဲနှင့် ကိုက်ညီပါက ပိုကြီးသော ပုံစံကို စမ်းပါ။ `phi-4-mini` သည် သင့်တော်သော အထွတ်အထိပ်ဖြစ်သည်။ |
| ချိတ်ဆက်မှု ငြင်းဆိုခြင်း | Foundry Local  လည်ပတ်နေပါစေ: `foundry local status` ။ လိုအပ်ပါက ပြန်လည်စတင်ပါ။ |

---

## ၇။ မြန်ဆန်သော ကိုးကား: RBAC အခန်းကဏ္ဍများ

| အခန်းကဏ္ဍ | အတိုင်းအတာ | ပံ့ပိုးသည့်အရာ |
|------|-------|--------|
| **Azure AI User** | Project | ဒေတာလုပ်ဆောင်ချက်များ: `agents/write`, `agents/read` |
| **Azure AI Developer** | Project/Account | ဒေတာလုပ်ဆောင်ချက်များ + project ဖန်တီးခြင်း |
| **Azure AI Owner** | Account | ပြည့်စုံသော အသုံးပြုခွင့် + အခန်းကဏ္ဍ စီမံခန့်ခွဲမှု |
| **Contributor** | Subscription/RG | စီမံခန့်ခွဲမှု လုပ်ဆောင်ချက်များသာ (**မပါ** ဒေတာလုပ်ဆောင်ချက်များ) |
| **Owner** | Subscription/RG | စီမံခန့်ခွဲမှု + အခန်းကဏ္ဍ ခန့်အပ်ခြင်း (**မပါ** ဒေတာလုပ်ဆောင်ချက်များ) |

---

## ၈။ အလုပ်ရုံပြီးစီးမှု စစ်ဆေးရန်စာရင်း

| # | ပစ္စည်း | မော်ဂျူး |
|---|------|--------|
| ၁ | မတိုင်မှီလိုအပ်ချက်များ ထည့်သွင်းပြီးစစ်ဆေးပြီး | [00](00-prerequisites.md) |
| ၂ | Foundry Toolkit extension ထည့်သွင်းပြီး project ချိတ်ဆက်ခြင်း (သို့မဟုတ် လမ်းကြောင်း B ပြင်ဆင်ထားသည်) | [01](01-setup.md) |
| ၃ | Hosted agent တည်ဆောက်ပြီး | [02](02-create-hosted-agent.md) |
| ၄ | `.env` ပြင်ဆင်ပြီး အညွန်းရေးသားပြီး လိုအပ်သော ဆော့ဖ်ဝဲများ ထည့်သွင်းပြီး | [03](03-configure-and-code.md) |
| ၅ | Agent ကို ဒေသတွင်း စမ်းသပ်ပြီး - ၃ ဆောင်ရွက်ချက် အောင်မြင် | [04](04-test-locally.md) |
| ၆ | Foundry တွင် တပ်ဆင်ပြီး (လမ်းကြောင်း A သာ) | [05](05-deploy-to-foundry.md) |
| ၇ | ကျပ်တည်းမှု/လုံခြုံရေး စမ်းသပ်မှုများကို မိုဃ်း/cloud တွင် အောင်မြင် | (လမ်းကြောင်း A သာ) | [06](06-verify-in-playground.md) |
| ၈ | အနှစ်ချုပ် ကိုရှေ့ဆက် အဆင့်များသတ်မှတ်ပြီး စစ်ဆေးချက် | [07](07-summary.md) |

---

**ယခင်**: [07 - အနှစ်ချုပ်](07-summary.md) · **မူလ**: [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ပြောကြားချက်**
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းနေသော်လည်း၊ စက်ကိရိယာဘာသာပြန်ခြင်းများတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် လိုအပ်ပါသည်။ မူလစာတမ်းကို မူရင်းဘာသာဖြင့်သာ ယုံကြည်စိတ်ချရသော အချက်အလက်အဖြစ် သတ်မှတ်သင့်သည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုကွာခြားမှုများ သို့မဟုတ် မမှန်ကန်သော အသုံးပြုမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မခံပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->