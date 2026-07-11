# Module 8 - ပြဿနာရှာဖွေခြင်း

ဒီ module က multi-agent workflow ထက်သက်ဆိုင်တဲ့ လူသုံးများသောအမှားများ၊ ပြင်ဆင်မှုများနဲ့ debugging နည်းဗျူဟာများကိုဖုံးကွယ်ပေးပါတယ်။

## Agent ထွက်ရှိမှု ပြဿနာများ

### GapAnalyzer က “I still don’t have the matching report” လို့ပြောတာ

**လက္ခဏာ:** GapAnalyzer ရဲ့ အဖြေမှာ “Missing Skills” နဲ့ “Certification Gaps” ပါတဲ့ matching report ကို ထည့်ပေးဖို့ တောင်းဆိုတယ်။ သင် resume နဲ့ job description နှစ်ခုလုံးပို့ပြီးဖြစ်ပေမယ့်ဒီအခြေအနေဖြစ်တတ်တယ်။

**အကြောင်းရင်း:** JD စာသားကို JD Agent ကို ပေးပို့ခြင်းမရှိဘူး။ `context_mode="last_agent"` ဖြစ်ရင် `resume_executor` ဆိုတာအသုံးပြုသူရဲ့ မူလစာသားပဲ မြင်ရတဲ့ executor တစ်ခုပါ။ `RESUME_PARSER_INSTRUCTIONS` မှာ JD စာသား မပါဝင်ခဲ့လျှင် JD Agent က JD ကို parse လုပ်စရာမရှိဘူး၊ MatchingAgent က fit score တွက်မရလို့ GapAnalyzer ကို မည်သည့်အဓိပ္ပာယ်မဲ့ input တစ်ခုပဲရောက်ရှိပါတယ်။

**သိရှိရမည့်အချက်:**

server logs ထဲမှာ MatchingAgent span ကို ကြည့်ပါ။ အဲဒါမှာ:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pass-through ပျောက်နေ သို့မဟုတ် ကျိုးပွားနေတယ်။

**ပြုပြင်ရန်:** `main.py` မှာ `RESUME_PARSER_INSTRUCTIONS` မှာ `[JOB DESCRIPTION PASS-THROUGH]` အပိုင်းနဲ့ ဥပဒေရေးခဲ့တဲ့ စည်းမျဉ်းရှိကြောင်း အတည်ပြုပါ။
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
အထို့အပြင် `JOB_DESCRIPTION_INSTRUCTIONS` မှာ `[PARSED RESUME PASS-THROUGH]` relay rule ပါရှိကြောင်း အတည်ပြုပါ:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
ကွဲပြားမှုရှိခဲ့တဲ့ instruction block တခုခု scaffold wizard မှ stub ဆိုရင်တော့ [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) မှ ပြည့်စုံတဲ့ version နဲ့ အစားထိုးပါ။

### MatchingAgent က “Cannot compute fit score - no JD provided” လို့ထွက်လာတာ

ဒါက အထက်မှာပြောခဲ့တဲ့ အကြောင်းရင်းတစ်ခုပါပဲ။ MatchingAgent က JD Agent ရဲ့ output ကို ရရှိခဲ့ပေမယ့် `[PARSED RESUME PASS-THROUGH]` အပိုင်း ပျောက်ပြီး အလွတ်ဖြစ်နေခြင်းကြောင့် နှစ် Profile ကို နှိုင်းယှဉ်၍ မရနိုင်တော့ပါ။ အတည်ပြုပါ။
1. `JOB_DESCRIPTION_INSTRUCTIONS` မှာ relay စည်းမျဉ်း `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.` ပါရှိမယ်။
2. `MATCHING_AGENT_INSTRUCTIONS` က agent ကို `[JD REQUIREMENTS]` နဲ့ `[PARSED RESUME PASS-THROUGH]` အပိုင်းတွေကို ရှာဖွေဖို့ပြောထားတယ်။

instruction block နှစ်ခုလုံးကို [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) မှ ဆက်စပ်ပြီး ပြည့်စုံတဲ့ version နဲ့ အစားထိုးပါ။

### အဖြေက နှစ်ကြိမ် ထွက်လာတာ

**လက္ခဏာ:** GapAnalyzer ထွက်ရှိမှု (သို့) pipeline မှ စုစုပေါင်းထွက်ရှိမှု Agent Inspector မှာ နှစ်ကြိမ်မြောက် ပေါ်နေတယ်။

**အကြောင်းရင်း:** `WorkflowBuilder` က OR-semantics ကို incoming edges များအတွက်သုံးတယ် - downstream executor တစ်ခုသည် predecessor တစ်ခုခုပြီးဆုံးချိန်တွင် မြန်ဆန်စွာ ပျံ့နှံ့သွားတယ်။ `matching_executor` မှာ incoming edges နှစ်ခု ရှိပါက (resume_executor မှတစ်ခုနဲ့ jd_executor မှတစ်ခု) တစ်ကြိမ် ResumeParser ပြီးဆုံးချိန်၊ တစ်ကြိမ် JD Agent ပြီးဆုံးချိန်မှာ ထိခိုက်ခေါ်စေပြီး GapAnalyzer ကို မှတ်ချက်နှစ်ကြိမ် ပြန်လုပ်ပါတယ်။

**ပြုပြင်ရန်:** `WorkflowBuilder` graph ကို တိကျကျပ်တည်းတဲ့ pipeline တစ်ခု အဖြစ် fan-in မရှိစေရန် သေချာစေပါ။

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # resume_executor မှ မဟုတ်ပါ။
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

`.add_edge(resume_executor, matching_executor)` ဆိုတဲ့ မလိုအပ်တဲ့ ပါဝင်မှုရှိရင် ဖယ်ရှားပါ။ JD Agent ထွက်ရှိမှုမှာရှိတဲ့ `[PARSED RESUME PASS-THROUGH]` relay က MatchingAgent ကို resume ဆီ ဝင်ရောက်ခွင့်ပေးပြီးသားဖြစ်ပါတယ်။

---

## ပတ်ဝန်းကျင်နဲ့ ဖွဲ့စည်းမှု ပြဿနာများ

### `.env` မှာ တန်ဖိုးမရှိခြင်း သို့မဟုတ် မှားနေခြင်း

`.env` ဖိုင်ကို `PersonalCareerCopilot/` ဖိုလ်ဒါထဲမှာထားရမည် (`main.py` နှင့် ညီတန်းရာ):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

အသင့်တော်ဆုံး `.env` အကြောင်းအရာ:

**လမ်းကြောင်း A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**လမ်းကြောင်း B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> နှစ်ခုလမ်းကြောင်းလုံးမှာ `FOUNDRY_PROJECT_ENDPOINT` ကို အသုံးပြုပါတယ်။ တန်ဖိုးက မတူပါဘူး။ cloud မှာ `https://` Foundry endpoint ဖြင့် အသုံးပြုသည်။ local မှာ `http://localhost:5273/v1` ဖြစ်သည်။ လမ်းကြောင်း B အတွက် model alias တိကျမှုကို `foundry model list` ဖြင့် အတည်ပြုပါ။

> **သင့် `FOUNDRY_PROJECT_ENDPOINT` ကို ချီဖွင့်ရန်:** 
- VS Code မှာ **Foundry Toolkit** sidebar ဖြင့် သင့် project ကို right-click → **Copy Project Endpoint**။
- (သို့) [Azure Portal](https://portal.azure.com) → သင့် Foundry project → **Overview** → **Project endpoint**။

> **သင့် `AZURE_AI_MODEL_DEPLOYMENT_NAME` ကို ချီဖွင့်ရန်:** Foundry Toolkit sidebar တွင်သင့် project ကိုချဲ့ချင်း → **Models** → သင့် deploy လုပ်ထားသော model နာမည်ကို ရှာပါ (ဥပမာ. `gpt-4.1-mini`)။

### Env var များ၏ ဦးစားပေးမှု

`main.py` မှာ `load_dotenv(override=True)` အသုံးပြုပါတယ်၊ ဒါဆိုလျှင်:

| ဦးစားပေးမှု | မူရင်း | နှစ်ခုရှိတိုင်း ဘယ်ဟာ အောင်နိုင်? |
|----------|--------|------------------------|
| 1 (အမြင့်ဆုံး) | `.env` ဖိုင် | ဟုတ်ပြီ |
| 2 | Shell / container ပတ်ဝန်းကျင် environment variable | `.env` မှာ အဓိက key မရှိတဲ့အခါ အသုံးပြုသည် |

ဒေသတွင်းတိုးတက်မှုမှာ `.env` က တကယ်မှန်ကန်မှုရင်းမြစ်ဖြစ်ပြီး (`.env` ပြင်ဆင်ခြင်းက ချက်ချင်း အကျိုးသက်ရောက်မှုရှိသည်)၊ Hosted deployment မှာတော့ Foundry က container အဆင့်မှာ Env variables များ ထည့်သွင်းပေးပြီး `.env` ကို ဒါ့အစား အသုံးပြုမထားပါဘူး။ ထို့ကြောင့် injected container value များကိုသာ သုံးသည်။

---

## ဗားရှင်းကိုက်ညီမှု

### Package ဗားရှင်း matrix

multi-agent workflow ရဲ့ package ဗားရှင်းတွေ လိုအပ်ချက်ရှိပါတယ်။ ဗားရှင်း မကိုက်ညီမှုက runtime error ဖြစ်စေတတ်ပါတယ်။

| Package | လိုအပ်သော ဗားရှင်း | စစ်ဆေးရန် command |
|---------|-----------------|---------------|
| `agent-framework-foundry` | နောက်ဆုံး | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | နောက်ဆုံး | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | နောက်ဆုံး | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### လူသုံးများသော ဗားရှင်း အမှားများ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ပြုပြင်ပါ: agent-framework-foundry ကိုပြန်လည်ထည့်သွင်းပါ။
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ဖြေရှင်းချက်: mcp package ကိုတိုးမြှင့်ပါ
pip install mcp --upgrade
```

### ဗားရှင်းများအားလုံးကို တစ်ပြိုင်နက်စစ်ဆေးခြင်း

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

စောင့်ကြည့်ရန် output:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Deployment ပြဿနာများ

### Deployment အပြီး	container စတင်မလုပ်နိုင်ခြင်း

1. **Container logs ကိုစစ်ဆေးပါ:**
   - **Foundry Toolkit** sidebar ဖြင့် → **Hosted Agents (Preview)** ကိုချဲ့ → သင့် agent ကို နှိပ် → ဗားရှင်းကိုချဲ့ → **Container Details** → **Logs** ကြည့်ရှုပါ။
   - Python stack trace တွေ သို့မဟုတ် module မရှိ error တွေ ရှာပါ။

2. **Container စတင်မှု မအောင်မြင်မှုများ:**

   | Logs မှာ error | အကြောင်း | ပြုပြင်ရန် |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` မှ package မပါ | package ထည့်ပြီး ပြန် deploy လုပ်ပါ |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` သို့ `.env` ရဲ့ env var မသတ်မှတ်ထားခြင်း | `agent.yaml` → `environment_variables` (hosted) သို့ `.env` (local) မှ တန်ဖိုးထည့်ပါ |
   | `azure.identity.CredentialUnavailableError` | Managed Identity မသတ်မှတ်ခြင်း | Foundry က မှန်ကန်စွာ သတ်မှတ်ပေးတတ်သည် – extension များမှ deploy လုပ်နေတာကို သေချာစေပါ |
   | `OSError: port 8088 already in use` | Dockerfile မှာ port မှား ဒဲ့ သို့ port ပဋိပက္ခ | Dockerfile မှာ `EXPOSE 8088` နှင့် `CMD ["python", "main.py"]` တို့ကို စစ်ဆေးပါ |
   | Container က code 1 ဖြင့် ထွက်သွား | `main()` မှာ မကြိုတင်ကိုင်တွယ်ထားသော exception | ဒေသတွင်း ဖိုင်ပွင့် ([Module 5](05-test-locally.md)) မှာ စမ်းသပ်ပြီး ပြဿနာကို ဖမ်းဆီးပါ |

3. **ပြင်ဆင်ပြီးနောက် ပြန် deploy လုပ်ပါ:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → အဲဒီ agent ကို ပြန်ရွေး → ဗားရှင်းအသစ် deploy လုပ်ပါ။

### Deployment အချိန်ကြာရခြင်း

Multi-agent containers တွေ startup နှုန်း ဆီးတဲ့အတွက် agent instance ၄ ခု ဖန်တီးတာကြောင့် startup ကြာပါတယ်။ အကောင်းစား startup အချိန်များက အောက်ပါအတိုင်းရှိသည် –

| အဆင့် | မျှော်မှန်းထားသော ကြာမြင့်ချိန် |
|-------|------------------|
| Container image တည်ဆောက်ခြင်း | ၁-၃ မိနစ် |
| Image ကို ACR သို့ push ပြုလုပ်ခြင်း | ၃ဝ-၆ဝ စက္ကန့် |
| Container စတင်ခြင်း (single agent) | ၁၅-၃ဝ စက္ကန့် |
| Container စတင်ခြင်း (multi-agent) | ၃ဝ-၁၂၀ စက္ကန့် |
| Agent Playground မှာ အသုံးပြုနိုင်ခြင်း | "Started" ပြီး ၁-၂ မိနစ် |

> “Pending” အခြေအနေနှင့် ၅ မိနစ်ကျော်ကြာနေပါက container logs မှာ error တွေကို စစ်ဆေးပါ။

---

## RBAC နဲ့ အခွင့်အရေး ပြဿနာများ

### `403 Forbidden` သို့မဟုတ် `AuthorizationFailed`

သင့် Foundry project ပေါ်မှာ **[Foundry User](https://aka.ms/foundry-ext-project-role)** role လိုအပ်တယ် (ယခင်မှာ **Azure AI User** လို့ခေါ်ထားခဲ့ပြီး role ID မပြောင်းသေးပါ):

၁။ [Azure Portal](https://portal.azure.com) → သင့် Foundry **project** အရင်းအမြစ်သို့သွားပါ။
၂။ **Access control (IAM)** → **Role assignments** ကိုနှိပ်ပါ။
၃။ သင့်နာမည်ကို ရှာဖွေ → **Foundry User** (သို့မဟုတ် ယနေ့ထိသုံးနေသော legacy label **Azure AI User**) ရှိကြောင်းအတည်ပြုပါ။
၄။ မရှိရင်: **Add** → **Add role assignment** → **Foundry User** ကိုရှာဖွေ → သင့်အကောင့်သို့ပေးအပ်ပါ။

အသေးစိတ်အတွက် [Microsoft Foundry အတွက် RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) စာရွက်ကို ကြည့်ပါ။

### မူဒယ် deployment မရရှိနိုင်ခြင်း

Agent က model နဲ့ဆက်စပ်တဲ့ error ပြန်လာရင်:

၁။ Model တင်ထားမှုပြဿနာမရှိကြောင်း စစ်ဆေးပါ: Foundry sidebar → project ကိုချဲ့ → **Models** → `gpt-4.1-mini` (သို့မဟုတ် သင့် model) ကို **Succeeded** အနေအထားနဲ့ ရှာပါ။
၂။ deployment နာမည်ကို စစ်ဆေးပါ: `.env` (သို့မဟုတ် `agent.yaml`) ရဲ့ `AZURE_AI_MODEL_DEPLOYMENT_NAME` နဲ့ sidebar မှာ အမှန် deployment နာမည်ကို နှိုင်းယှဉ်ပါ။
၃။ Deployment ကြာနှင့် (အခမဲ့အဆင့်): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) မှ ပြန်တင်ပါ (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)။

---

## Foundry Local ပြဿနာများ (လမ်းကြောင်း B)

### Foundry Local service မစတင်ခြင်း

```powershell
# အခြေအနေ စစ်ဆေးပါ
foundry local status

# ရပ်ဆိုင်းကာရှိပါက ဝန်ဆောင်မှုကို စတင်ပါ
foundry local start
```

| လက္ခဏာ | အကြောင်း | ပြုပြင်ရမည့် နည်းလမ်း |
|---------|-------|-----|
| Health check `503` ပြန်တယ် | Service မစလိုက်သေး | `foundry local start` သို့ Foundry Toolkit sidebar တွင် **Start** ကိုနှိပ်ပါ |
| Health check timeout ဖြစ်တယ် | Model မအဆင်သင့် | စတင်ပြီး ၃၀-၆၀ စက္ကန့် တောင့်ဆိုင်းပါ၊ လူကြီးမားတဲ့ model များပိုကြာတတ်သည် |
| `/v1/health` မှာ `StatusCode: 404` | Port မှားယွင်း | အစဉ်အလာ default က `5273` ဖြစ်သည် `foundry local status` မှာ အမှန်တိကျသော port ကို စစ်ဆေးပါ |
| အသုံးပြုနိုင်သော အစိတ်အပိုင်းများ မလုံလောက်ခြင်း | Foundry Local ကို ~4 GB RAM ရှိဖို့လို | အခြား application များကို ပိတ်ပါ |
| Model download မအောင်မြင် | Disk စွန်းရေ တွေလျော့ပါး | Model များ ၂-၈ GB ဖြစ်တယ်။ disk free ခွင့် ထားပါ၊ ပြီးသွားရင် `foundry model pull <name>` |

### Model နာမည်မကိုက်ညီမှု

```powershell
# ဒေါင်းလုပ်လုပ်ထားသောမော်ဒယ်များနှင့်၎င်းတို့၏တိကျသောအမည်များကိုစာရင်းပြပါ
foundry model list
```

`.env` ထဲမှာ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ကို ဘာသာရပ်တိကျတဲ့ alias ဖြင့် (ဥပမာ `phi-4-mini`၊ `Phi-4-mini` မဟုတ်ရပါ) သတ်မှတ်ပါ။

### ဒေသတွင်းစမ်းသပ်မှု (လမ်းကြောင်း B) မှာ `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'`

lab ရဲ့ `main.py` မှာ `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` ကို သုံးသည်။ Foundry Local က service ကို ဒေသတွင်း သတ်မှတ်ခြင်းလိုအပ် - **မဟုတ်** `AZURE_AI_PROJECT_ENDPOINT` ဖြစ်ရပါ။ သင့် `.env` ထဲမှာပါရှိစေရန် သေချာစေပါ။

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP tool ကနေ အပြင်သို့ ဘာသာမပြန်ခေါ်နေဆဲ (လမ်းကြောင်း B)

ဒီအချက်က မျှော်မှန်းထားသလိုပါ။ `search_microsoft_learn_for_plan` tool က learning resources များကို `https://learn.microsoft.com/api/mcp` ဆီကနေ ရယူတယ်။ **Skill-name query ပဲ** network ပေါ်ကို သွားပြီး၊ resume နဲ့ JD စာသားကို သင်ရဲ့ စက်ကွက်မှာပဲ ဆောင်ရွက်ပြီး ပြန်ပို့မထားပါ။ အပြည့်အဝ offline လုပ်ဆောင်ချင်ရင်၊ အဲဒီ tool ထဲမှာ `try/except` ပုံစံ fallback ပေါင်းထည့်၍ endpoint မရောက်ချစ်ပါက `learn.microsoft.com` URL တစ်ခု ပြန်ပေးပါ။

---

## ကူညီမှု ရယူခြင်း

အထက်ပါပြင်ဆင်ချက်အားလုံး ကြိုးစားပြီး မဖြေရှင်းနိုင်ရင်:

1. **Server logs ကိုစစ်ဆေးပါ** - error အများကြီးက Python stack trace တစ်ခုကို terminal မှာ ဖော်ပြမှာဖြစ်သည်။ traceback အပြည့်အစုံကို ဖတ်ပါ။
2. **Error message ကို ရှာဖွေပါ** - error စာသားကို copy လုပ်ပြီး [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) မှာရှာပါ။
3. **Issue တင်ပါ** - [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) မှာ issue တင်ပြီး
   - Error message သို့မဟုတ် screenshot
   - သင့် package ဗားရှင်းများ (`pip list | Select-String "agent-framework"`)
   - သင့် Python ဗားရှင်း (`python --version`)
   - ပြဿနာ ဒေသတွင်းလား ဒါမှမဟုတ် deployment ကြောင့်လား

---

### အခြေအနေ စစ်ဆေးခြင်း

- [ ] `.env` configuration ပြဿနာများကို စစ်ဆေးနည်းနဲ့ ပြင်ဆင်နည်း ပိုင်နိုင်ပါပြီ။
- [ ] လူသုံး package ဗားရှင်းတွေလိုအပ်ချက်နဲ့ ကိုက်ညီမှု ရှိကြောင်း အတည်ပြုနိုင်ပါပြီ။
- [ ] Deployment မအောင်မြင်မှုများအတွက် container logs စစ်ဆေးနည်းကို သိရှိပြီး။
- [ ] Azure Portal မှာ RBAC role များစစ်ဆေးနည်းကို နားလည်ပြီး။

---

**ယခင်:** [07 - Verify in Playground](07-verify-in-playground.md) · **နောက်တော်:** [09 - Summary →](09-summary.md) · **မူလ:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ပြောကြားချက်**
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းနေသော်လည်း၊ စက်ကိရိယာဘာသာပြန်ခြင်းများတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် လိုအပ်ပါသည်။ မူလစာတမ်းကို မူရင်းဘာသာဖြင့်သာ ယုံကြည်စိတ်ချရသော အချက်အလက်အဖြစ် သတ်မှတ်သင့်သည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုကွာခြားမှုများ သို့မဟုတ် မမှန်ကန်သော အသုံးပြုမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မခံပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->