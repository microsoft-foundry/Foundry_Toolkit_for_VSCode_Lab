# Module 8 - ပြဿနာဖြေရှင်းခြင်း (Multi-Agent)

ဤမော်ဂျူးတွင် multi-agent အလုပ်စဉ်အတွက် အထူးပြု ပြဿနာများ၊ ဖြေရှင်းနည်းများနှင့် debugging အကြံပြုနည်းများကို ဖော်ပြထားသည်။ Foundry တပ်ဆင်မှုဆိုင်ရာအခြေအနေများအတွက်လည်း [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md) ကိုလေ့လာပါ။

---

## အကြိမ်အမှတ်တရ: အမှား → ဖြေရှင်းနည်း

| အမှား / သလိုက် လက္ခဏာ | ဖြစ်ပေါ်နိုင်သော အကြောင်းပြချက် | ဖြေရှင်းနည်း |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` ဖိုင်လက်မရှိခြင်း သို့မဟုတ် တန်ဖိုးများအပ်ထားခြင်းမရှိ | `PROJECT_ENDPOINT=<your-endpoint>` နှင့် `MODEL_DEPLOYMENT_NAME=<your-model>` ပါသော `.env` ဖိုင်ကို ဖန်တီးပါ |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtual environment မဖွင့်ထားခြင်း သို့မဟုတ် လိုအပ်သော dependency မတပ်ဆင်ထားခြင်း | `.\.venv\Scripts\Activate.ps1` ကို ပြေးပြီးနောက် `pip install -r requirements.txt` ထပ်ဆောင်ရွက်ပါ |
| `ModuleNotFoundError: No module named 'mcp'` | MCP package မတပ်ဆင်ခြင်း (requirements တွင် မပါ) | `pip install mcp` သို့မဟုတ် `requirements.txt` တွင် အတည်ပြုပါ |
| Agent စတင်သော်လည်း ဖန်တီးခံရသည့် တုံ့ပြန်မှုသည် ဖေါ်ပြချက်မရှိခြင်း | `output_executors` မတွဲညီမှု သို့မဟုတ် edges မရှိခြင်း | `output_executors=[gap_analyzer]` ဖြစ်ကြောင်း နှင့် `create_workflow()` တွင် အားလုံးသော edges ရှိကြောင်း အတည်ပြုပါ |
| Gap card ၁ ချောင်းသာ ရှိနောက် ကျန်များ မရှိခြင်း | GapAnalyzer ညွှန်းကြားချက် မပြည့်စုံခြင်း | `GAP_ANALYZER_INSTRUCTIONS` တွင် `CRITICAL:` ပါရာဂရပ် ပါထည့်ပါ - [Module 3](03-configure-agents.md) ကို ကြည့်ပါ |
| Fit score သည် ၀ ဖြစ်ခြင်း သို့မဟုတ် မရှိခြင်း | MatchingAgent သည် upstream data မရရှိခြင်း | `add_edge(resume_parser, matching_agent)` နှင့် `add_edge(jd_agent, matching_agent)` တို့ ရှိကြောင်း စစ်ဆေးပါ |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server မှ tool call ကို ငြင်းပယ်ခြင်း | အင်တာနက်ချိတ်ဆက်မှုကို စစ်ဆေးပါ။ `https://learn.microsoft.com/api/mcp` ကို browser တွင် ဖွင့်ကြည့်ပါ။ ထပ်မံကြိုးစားပါ |
| တုံ့ပြန်မှုတွင် Microsoft Learn URL မပါခြင်း | MCP tool မှတ်ပုံတင်မထားခြင်း သို့မဟုတ် endpoint မှားခြင်း | GapAnalyzer တွင် `tools=[search_microsoft_learn_for_plan]` နှင့် `MICROSOFT_LEARN_MCP_ENDPOINT` မှန်ကန်ကြောင်းအတည်ပြုပါ |
| `Address already in use: port 8088` | တခြားလုပ်ဆောင်မှုက port 8088 ကို အသုံးပြုနေခြင်း | Windows တွင် `netstat -ano \| findstr :8088` သို့မဟုတ် macOS/Linux တွင် `lsof -i :8088` ဖြင့်ရှာပြီး အတားအဆီးလုပ်ဆောင်မှုကို ရပ်ပါ |
| `Address already in use: port 5679` | Debugpy port ရှင်းလင်းမှုမရှိခြင်း | အခြား debug အစီအစဉ်များ ရပ်ပါ။ `netstat -ano \| findstr :5679` ဖြင့် စစ်ဆေးပြီး ဖျက်ရပါမည် |
| Agent Inspector မဖွင့်နိုင်ခြင်း | Server မပြည့်စုံစွာ စတင်ခြင်း သို့မဟုတ် port ရှုပ်ထွေးမှု | "Server running" စာသား လိုင်းတစ်ကြောင်း ပြလာမှစောင့်ရှောက်ပါ။ port 5679 လွတ်ကြောင်းစစ်ဆေးပါ |
| `azure.identity.CredentialUnavailableError` | Azure CLI တွင် လက်မှတ်မရှိခြင်း | `az login` ပြေးပြီး server ကို ပြန်စတင်ပါ |
| `azure.core.exceptions.ResourceNotFoundError` | Model deployment မရှိခြင်း | `MODEL_DEPLOYMENT_NAME` သည် Foundry project တွင် စီစဉ်ထားသော model နာမည်နှင့် ကိုက်ညီကြောင်း စစ်ဆေးပါ |
| Deployment ပြီးဆုံးပြီးပြီးနောက် Container status "Failed" ဖြစ်ခြင်း | Container စတင်မှုအတွင်း crash ဖြစ်ခြင်း | Foundry sidebar တွင် container logs ကို စစ်ဆေးပါ။ အများအားဖြင့် env var ဖိုင် မတည်ရှိခြင်း သို့မဟုတ် import error ဖြစ်သောကြောင့်ဖြစ်သည် |
| Deployment အချိန် "Pending" အနေဖြင့် ၅ မိနစ်ထက် ကျော်ရင် | Container အစတင်ရန် အချိန်ကြာခြင်း သို့မဟုတ် resource ကန့်သတ်မှု | multi-agent မော်ဒယ်တွင် agent instance ၄ ခု ဖန်တီးသည့်အတွက် ၅ မိနစ်အထိ စောင့်ပါ။ ထပ်လည်ဖြစ်နေရင် logs ကြည့်ပါ |
| `ValueError` အမှား `WorkflowBuilder` မှ | Graph configuration မှားခြင်း | `start_executor` သတ်မှတ်ထားခြင်း၊ `output_executors` သည် စာရင်းဖြစ်ခြင်း၊ နှင့် အဝိုင်း edges မရှိခြင်းကို သေချာစစ်ဆေးပါ |

---

## ပတ်ဝန်းကျင်နှင့် ကွန်ဖစ်ဂျာရေးရှင်း ပြဿနာများ

### `.env` ဖိုင်မရှိခြင်း သို့မဟုတ် မှားယွင်းသော တန်ဖိုးများ

`.env` ဖိုင်သည် `PersonalCareerCopilot/` ဖိုဒါအတွင်းရှိရမည် (main.py နှင့် တန်းတူ အလွှာ) -

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```
  
မျှော်မှန်းထားသော `.env` အကြောင်းအရာ -

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```
  
> **PROJECT_ENDPOINT ရှာဖွေရန်:**  
- VS Code တွင် **Microsoft Foundry** sidebar ကိုဖွင့်၍ သင်၏ project ကို right-click → **Copy Project Endpoint** ကိုနှိပ်ပါ။  
- ဒါမှမဟုတ် [Azure Portal](https://portal.azure.com) → သင်၏ Foundry project → **Overview** → **Project endpoint** ကိုသွားပါ။

> **MODEL_DEPLOYMENT_NAME ရှာဖွေရန်:** Foundry sidebar တွင် သင့် project ကို ဖြည့်ချဲ့ပြီး **Models** → သင့် deploy လုပ်ထားသော model နာမည် (ဥပမာ `gpt-4.1-mini`) ကိုရှာပါ။

### Env var ဦးစားပေးမှု

`main.py` မှာ `load_dotenv(override=False)` ကိုသုံးသည်။ ဤအတိုင်းဆိုသည်မှာ -

| ဦးစားပေးမှု | အရင်းအမြစ် | နှစ်ခုစလုံးရှိပါက ဘယ်ဟာအရေးကြီးသည်? |
|----------|--------|------------------------|
| ၁ (အမြင့်ဆုံး) | Shell environment variable | ဟုတ်သည် |
| ၂ | `.env` ဖိုင် | Shell var မရှိပါကသာ အသုံးပြုမည် |

ဤအတိုင်း Foundry runtime env var (agent.yaml မှဖန်တီးထားသော) သည် hosted deployment အတွင်း `.env` တန်ဖိုးများထက် ဦးစားပေးသည်။

---

## ဗားရှင်း ကိုက်ညီမှု

### Package ဗားရှင်းဇယား

multi-agent workflow အတွက် အတိအကျ ဗားရှင်းများလိုအပ်သည်။ မကိုက်ညီလျှင် runtime အမှားဖြစ်ပေါ်သည်။

| Package | လိုအပ်သော ဗားရှင်း | စစ်ဆေးရန် Command |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | နောက်ဆုံးဗားရှင်း (pre-release) | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### လူသုံးမှု Error များ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# ပြင်ဆင်ချက်: rc3 သို့ အဆင့်မြှင့်တင်ခြင်း
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```
  
**`agent-dev-cli` မတွေ့ရှိခြင်း သို့မဟုတ် Inspector နှင့် ကိုက်ညီမှုမရှိခြင်း**

```powershell
# အမှားပြုပြင်ခြင်း: --pre အလံစနစ်ဖြင့် ထည့်သွင်းပါ။
pip install agent-dev-cli --pre --upgrade
```
  
**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# ပြင်ဆင်ချက်: mcp အထုပ်အား အဆင့်မြှင့်တင်ခြင်း
pip install mcp --upgrade
```
  
### ဗားရှင်းများအားလုံးကို တပြိုင်နက် စစ်ဆေးရန်

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```
  
မျှော်မှန်းထားသော output -

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```
  
---

## MCP tool ပြဿနာများ

### MCP tool မှ ရလဒ် မပြန်လာခြင်း

**လက္ခဏာ:** Gap card များတွင် "No results returned from Microsoft Learn MCP" သို့မဟုတ် "No direct Microsoft Learn results found" ဟူသော စာသားများ ပြသည်။

**ဖြစ်နိုင်သောအချက်များ**

1. **ကွန်ယက်ပြဿနာ** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) ကို ချိတ်ဆက်၍မရပါ။
   ```powershell
   # ချိတ်ဆက်မှုကို စမ်းသပ်ပါ
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   ၎င်းသည် `200` တုံ့ပြန်ပါက endpoint သို့ ချိတ်ဆက်နိုင်သည်။

2. **မေးခွန်း ပုံသဏ္ဍာန် ကြီးလွန်းခြင်း** - သင်္ချာနည်းပညာအမည်သည် Microsoft Learn ရှာဖွေမှုအတွက် သီးသန့်လွန်လွန်ဖြစ်နေခြင်း။
   - အထူးပြု ကျွမ်းကျင်မှုများအတွက် မျှော်မှန်းထားသည့်အကြောင်းဖြစ်သည်။ tool တွင် အကြောင်းပြန် URL တစ်ခုပါရှိသည်။

3. **MCP session timeout ဖြစ်ခြင်း** - Streamable HTTP ချိတ်ဆက်မှု အချိန်ကုန်ဆုံးပြီ။
   - ပြန်ကြိုးစားပါ။ MCP session များသည် အတိုကြာခံပြီး ထပ်မံ ချိတ်ဆက်ရန်လိုသည်။

### MCP log များ၏ အဓိပ္ပါယ်

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```
  
| Log | အဓိပ္ပါယ် | လုပ်ဆောင်ချက် |
|-----|---------|--------|
| `GET → 405` | MCP client မစိတ်ကြိုတင် စစ်ဆေးခြင်း | ပုံမှန် - မထားရ။ |
| `POST → 200` | Tool call အောင်မြင်မှု | မျှော်မှန်းထားသည်။ |
| `DELETE → 405` | MCP client မစိတ်ကြိုတင် ပိတ်သိမ်းခြင်း | ပုံမှန် - မထားရ။ |
| `POST → 400` | မမှန်ကန်သော မေးခွန်း | `search_microsoft_learn_for_plan()` တွင် `query` parameter ကို စစ်ဆေးပါ |
| `POST → 429` | အမြင့်နှုန်း ကန့်သတ်ချက် | စောင့်ပါ၊ ပြန်ကြိုးစားပါ။ `max_results` parameter ကို လျော့နည်းစေပါ |
| `POST → 500` | MCP server အမှား | ကာလယာ - ထပ်ကြိုးစားပါ။ ကြာရှည်ခံလျှင် Microsoft Learn MCP API ပြတ်တောင်းခြင်းဖြစ် နိုင်သည် |
| ချိတ်ဆက်မှု အချိန်ကုန်ခြင်း | ကွန်ယက်ပြဿနာ သို့မဟုတ် MCP server မရရှိနိုင်ခြင်း | အင်တာနက်ပြဿနာကိုစစ်ဆေးပါ။ `curl https://learn.microsoft.com/api/mcp` ဖြင့် ကြိုးစား၍သေချာပါစေ |

---

## Deployment ပြဿနာများ

### Container စတင်မှု ပြန်လည်ပြတ်တောက်ခြင်း

1. **Container logs ကို စစ်ဆေးပါ:**
   - **Microsoft Foundry** sidebar ကိုဖွင့်ပြီး → **Hosted Agents (Preview)** ကို ဖြည့်ချဲ့ပါ → သင်၏ agent ကို နှိပ်ပါ → ဗားရှင်းကို ဖြည့်ချဲ့ပါ → **Container Details** → **Logs** ကိုကြည့်ပါ။
   - Python stack trace များသို့မဟုတ် module မရှိသော အမှားများ ရှာပါ။

2. **အလေ့အထများသော Container စတင်မှု ပြတ်တောက်မှုများ**

   | အမှား | ဖြစ်ပေါ်မှု | ဖြေရှင်းနည်း |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` တွင် package မပါခြင်း | package ထည့်ပြီး ထပ်မံ deploy လုပ်ပါ |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` တွင် env var မဖော်ပြခြင်း | `agent.yaml` → `environment_variables` အပိုင်းကို အသစ်ရေးပါ |
   | `azure.identity.CredentialUnavailableError` | Managed Identity မရှိခြင်း | Foundry သည် အလိုအလျောက်တပ်ဆင်ထားသည် - extension မှတဆင့် deploy လုပ်ရန် သေချာစေပါ |
   | `OSError: port 8088 already in use` | Dockerfile မှ port မှားပြထားခြင်း သို့မဟုတ် port ရှုပ်ထွေးမှု | Dockerfile ထဲတွင် `EXPOSE 8088` နှင့် `CMD ["python", "main.py"]` မှန်ကန်ကြောင်းစစ်ဆေးပါ |
   | Container exit code 1 | `main()` တွင် ဆုံးဖြတ်မရ exception ဖြစ်ခြင်း | ဒေသတွင်းတွင်စမ်းသပ်ပါ ([Module 5](05-test-locally.md)) အမှားဖြစ်မှသာ deploy လုပ်ပါ |

3. **ဖြေရှင်းပြီးနောက် ပြန်လည် deploy ချပါ:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → agent ကို ရွေးချယ် → ဗားရှင်း အသစ် deploy လုပ်ပါ။

### Deployment စောင့်ချိန် ကြာခြင်း

multi-agent container များသည် စတင်ရာတွင် agent instance ၄ခု ဖန်တီးသောကြောင့် စောင့်ချိန်များသည် ပိုရှည်သည်။ စနစ်တိုင်းကိုးကားအချိန်များမှာ -

| အဆင့် | မျှော်မှန်းချိန် |
|-------|------------------|
| Container image တည်ဆောက်ခြင်း | ၁-၃ မိနစ် |
| ACR သို့ image ပို့ခြင်း | ၃၀-၆၀ စက္ကန့် |
| Container စတင်ခြင်း (single agent) | ၁၅-၃၀ စက္ကန့် |
| Container စတင်ခြင်း (multi-agent) | ၃၀-၁၂၀ စက္ကန့် |
| Playground တွင် agent အသုံးပြုနိုင်ခြင်း | "Started" ပြီးနောက် ၁-၂ မိနစ် |

> "Pending" အခြေအနေ ၅ မိနစ်ကျော်ရင် container logs တွင်အမှားများ စစ်ဆေးပါ။

---

## RBAC နှင့် ခွင့်ပြုချက် ပြဿနာများ

### `403 Forbidden` သို့မဟုတ် `AuthorizationFailed`

သင်၏ Foundry project တွင် **[Azure AI User](https://aka.ms/foundry-ext-project-role)** role လိုအပ်ပါသည်-

1. [Azure Portal](https://portal.azure.com) → သင့် Foundry **project** resource သို့ သွားပါ။
2. **Access control (IAM)** → **Role assignments** ကို နှိပ်ပါ။
3. သင့်နာမည် ရှာဖွေပြီး **Azure AI User** ပေးထားဖူးမှ အတည်ပြုပါ။
4. မရှိပါက - **Add** → **Add role assignment** → **Azure AI User** ရှာပြီး သင့်အကောင့်သို့ ပေးအပ်ပါ။

အသေးစိတ်အတွက် [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ကို ကြည့်ပါ။

### Model deployment မရရှိနိုင်ခြင်း

Agent မော်ဒယ်နှင့်ပတ်သက်သော အမှားရှိပါက -

1. မော်ဒယ် တပ်ဆင်ထားသည်ကို အတည်ပြုပါ။ Foundry sidebar → project ဖြည့်ချဲ့ → **Models** → `gpt-4.1-mini` (သို့မဟုတ် သင့် model) တွင် status **Succeeded** ရှိခြင်း။
2. deployment နာမည် ကိုက်ညီမှုကိုစစ်ဆေးပါ။ `.env` သို့မဟုတ် `agent.yaml` ထဲမှ `MODEL_DEPLOYMENT_NAME` နှင့် sidebar မှ deployment နာမည်ကို နှိုင်းယှဉ်ပါ။
3. deployment သက်တမ်းကုန်သွားပါက (free tier) [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) မှ ထပ်မံ Deploy လုပ်ပါ (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)။

---

## Agent Inspector ပြဿနာများ

### Inspector ဖွင့်သော်လည်း "Disconnected" ပြသခြင်း

1. Server မပြတ်ပိတ် တပ်ဆင်မှု ရှိကြောင်း အတည်ပြုပါ။ terminal တွင် "Server running on http://localhost:8088" စာသားရှိရမည်။
2. port `5679` ကိုစစ်ဆေးပါ။ Inspector သည် debugpy ဖြင့် port 5679 တွင် ချိတ်ဆက်သည်။
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Server ကို ပြန်စတင်ပြီး Inspector ကို ထပ်ဖွင့်ပါ။

### Inspector တုံ့ပြန်မှု အချို့တင်ပြခြင်း

multi-agent တုံ့ပြန်မှုများသည် ကြာရှည်ပြီး လေ့လာထုတ်နောက်ခံဖြင့် ဆက်တိုက် သွားလာသည်။ အပြည့်အစုံဖြစ်ရန် (gap card အရေအတွက်နှင့် MCP tool calls ပမာဏမူတည်၍) ၃ဝ-၆ဝ စက္ကန့်လိုအပ်တတ်သည်။

တုံ့ပြန်မှု မပြည့်စုံဆက်တိုက် ဖြစ်လျှင် -  
- GapAnalyzer အညွှန်းတွင် `CRITICAL:` များပါရှိပြီး gap card များပေါင်းစည်းခြင်းကို တားမြစ်ထားကြောင်း စစ်ဆေးပါ။  
- သင်၏ model token ကန့်သတ်ချက်ကို စစ်ဆေးပါ - `gpt-4.1-mini` မှ ၃၂,၀၀၀ output token ထောက်ပံ့သည်။ လုံလောက်သည်။

---

## စွမ်းဆောင်ရည် အကြံပြုချက်များ

### တုံ့ပြန်ချက် နစ်နာမှု

multi-agent workflow များမှာ single-agent ထက် တိုးတက်မှု သက်သာမှုရရှိသည်မှာ sequential မူပိုင်ခွင့်များနှင့် MCP tool call များကြောင့်ဖြစ်ပါသည်။

| အကြံပြုချက် | မည်သို့တိုးတက်စေသနည်း | သက်ရောက်မှု |
|-------------|-----|--------|
| MCP calls လျော့ပါ | tools အတွက် `max_results` parameter ကို လျော့နည်းစေပါ | HTTP round-trip များလျော့ပါ |
| ညွှန်ကြားချက် ရိုးရှင်းဖြစ်စေ | Agent prompts ကို အတိုချုပ်၍ညှိနှိုင်းပါ | LLM ကို ပိုမြန်စေလိမ့်မည် |
| `gpt-4.1-mini` သုံးပါ | `gpt-4.1` ထက် ဖန်တီးမှု ပိုမြန်သည် | ၂ဆ အမြန်ပြန်သွားမှု |
| gap card အသေးစိတ် လျော့ပါ | GapAnalyzer အညွှန်းတွင် gap card ပုံစံ ရိုးရှင်းစေခြင်း | output ပမာဏ လျော့သည် |

### ပုံမှန် တုံ့ပြန်ချိန်များ (ဒေသတွင်း)

| ကွန်ဖစ်ဂျာရေးရှင်း | မျှော်မှန်းချိန် |
|--------------|---------------|
| `gpt-4.1-mini`, gap card ၃-၅ ခု | ၃၀-၆၀ စက္ကန့် |
| `gpt-4.1-mini`, gap card ၈ ကျော် | ၆၀-၁၂၀ စက္ကန့် |
| `gpt-4.1`, gap card ၃-၅ ခု | ၆၀-၁၂၀ စက္ကန့် |
---

## အကူအညီရယူခြင်း

အထက်ပါပြင်ဆင်ချက်များကိုကြိုးစားပြီးမှ မဖြေရှင်းနိုင်ပါက-

1. **ဆာဗာလော့ဂ်များကို စစ်ဆေးပါ** - အမှားအပျက်များအများစုသည် တာမီနယ်တွင် Python stack trace တစ်ခု ထုတ်ပေးသည်။ စုံလင်သော traceback ကိုဖတ်ပါ။
2. **အမှားစာသားကို ရှာဖွေပါ** - အမှားစာသားကို ကူးယူပြီး [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) တွင် ရှာဖွေပါ။
3. **ပြဿနာတင်ပါ** - [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) တွင် ပြဿနာတင်ရန်အတွက်-
   - အမှားစာသား သို့မဟုတ် screenshot
   - သင့် package များ ဗားရှင်းများ (`pip list | Select-String "agent-framework"`)
   - သင့် Python ဗားရှင်း (`python --version`)
   - ပြဿနာသည် ဒေသတွင်းဖြစ်မသည်၊ ထုတ်လုပ်ပြီးနောက်ဖြစ်မည်ဟု ဖေါ်ပြပါ

---

### စစ်ဆေးရန်အချက်များ

- [ ] အများဆုံးသော multi-agent အမှားများကို ရောင်ပြာဇယား အသုံးပြု၍ ပါးနပ်တတ်ပါသည်
- [ ] `.env` ဖိုင် ဆက်တင်နဲ့ ပတ်သက်သောပြဿနာများကို စစ်ဆေး ပြုပြင်နည်းကို သိရှိပါသည်
- [ ] လိုအပ်သော matrix နှင့်ထပ်တူ package ဗားရှင်းများကို မှန်ကန်မှု စစ်ဆေးနိုင်ပါသည်
- [ ] MCP log အချက်အလက်များကို မြင်သာပြီး သီအိုရီးကို နားလည်ထားပြီး ကိရိယာ မအောင်မြင်မှုများကို ရှာဖွေစစ်ဆေးနိုင်ပါသည်
- [ ] ထုတ်လုပ်မှု မအောင်မြင်မှုများအတွက် container log များကို စစ်ဆေးနည်း သိပါသည်
- [ ] Azure Portal တွင် RBAC အခန်းကဏ္ဍများကို စစ်ဆေး ပြုပြင်နိုင်သည်

---

**ယခင်:** [07 - Verify in Playground](07-verify-in-playground.md) · **ပင်မစာမျက်နှာ:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ဤစာရွက်စာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) ဖြင့် ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းမိသော်၊ အလိုအလျောက် ဘာသာပြန်ခြင်းများတွင် အမှားအယွင်းများ သို့မဟုတ် မမှန်ကန်မှုများ ပါဝင်နိုင်ကြောင်း အသိပေးအပ်ပါသည်။ မူလစာရွက်စာတမ်းကို မူရင်းဘာသာဖြင့်သာ တရားဝင်အတည်ပြုရမည့် အရင်းအမြစ်အဖြစ် သတ်မှတ်သင့်ပါသည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် လူ့ပညာရှင်ဘာသာပြန်ခြင်းကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက် အသုံးပြုရာမှ ဖြစ်ပေါ်လာနိုင်သည့် နားမလည်မှုများ သို့မဟုတ် မှားအကောက်အဋ္ဌာန်းမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မယူပါ။**
<!-- CO-OP TRANSLATOR DISCLAIMER END -->