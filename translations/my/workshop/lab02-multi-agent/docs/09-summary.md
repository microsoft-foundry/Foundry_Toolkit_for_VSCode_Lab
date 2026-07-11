# မော်ဂျူး ၉ - အကျဉ်းချုပ် နှင့် နောက်တစ်ဆင့်များ

⏱️ ~၅ မိနစ်

**ဂုဏ်ယူပါတယ်!** Microsoft Foundry နှင့် Foundry Toolkit for VS Code ကို အသုံးပြု၍ မျိုးစုံအေဂျင့် workflow တစ်ခုကို တည်ဆောက်၊ စမ်းသပ်ပြီး (Path A တွင်ရှိပါက) တပ်ဆင်ပြီးပြီဖြစ်သည်။

---

## သင်တည်ဆောက်ခဲ့သည်မှာ

**Resume → အလုပ်ကိုက်ညီမှု သုံးသပ်သူ** - မျိုးစုံအေဂျင့်တင်ဆက်ထားသည့် hosted workflow တစ်ခုဖြစ်ပြီး-
- HTTP (`POST /responses`) ကနေ အလုပ်လျှောက်လွှာနှင့် အလုပ်ဖေါ်ပြချက်ကို လက်ခံသည်
- အထူးပြု agent ငါးယောက်ကို ဆက်တိုက်လည်ပတ်စေသည် - agent တစ်ယောက်သည် သူ၏နောက်ထပ်တင်ဆက်သူလိုအပ်သော ဒေတာကို လွှဲပို့သည်
- ကိုက်ညီမှုအဆင့် (0–100 နှင့် အသေးစိတ်ဖွဲ့စည်းချက်), ကျွမ်းကျင်မှုနှင့် လက်မှတ်ခွဲခြားမှုစာရင်း၊ ပုဂ္ဂိုလ်ရေးလေ့လာသင်ယူရန် လမ်းကြောင်းတစ်ခုကို Microsoft Learn ၏ တကယ့်လင့်ခ်များနှင့်ပြန်လည်ပေးပို့သည်
- Microsoft Learn MCP ဆာဗာ (`https://learn.microsoft.com/api/mcp`) ကို ခေါ်ယူပြီး ကျွမ်းကျင်မှု ချို့တဲ့မှုများအတွက် တရားဝင်သင်ယူမှုအရင်းအမြစ်များ ရယူသည်
- Microsoft Foundry Agent Service တွင် တခြားမဲ့ containerized hosted agent တစ်ခုအဖြစ် လည်ပတ်သည်

---

## သင်ရရှိခဲ့သော အဓိကအယူအဆများ

| အယူအဆ | သင်လေ့ကျင့်ခဲ့သည် |
|---------|-------------------|
| **မျိုးစုံအေဂျင့် စီမံခန့်ခွဲမှု** | `WorkflowBuilder` ဆက်တိုက်လည်ပတ်မှု အပိုင်းအစ `add_edge()` နှင့် |
| **အေဂျင့် အထူးပြုမှု** | အထူးပြု agent လေးယောက်သည် ဘုံ agent တစ်ယောက်ထက် ပိုမြင့်မားသော အရည်အသွေးကို ပေးနိုင်သည် |
| **အကြောင်းအရာ အစီအစဉ် ပုံစံ** | ResumeParser သည် router အနေဖြင့် စွမ်းဆောင်သည် - JD စာသားကို `[JOB DESCRIPTION PASS-THROUGH]` အပိုင်းတွင် ထိန်းသိမ်းထားသည့်အတွက် လျှောက်လွှာအောက်ပိုင်း agent များသို့ လွယ်ကူစွာရောက်ရှိစေသည် (context_mode="last_agent" ဆိုသည်မှာ start_executor သာမူလ အသုံးပြုသူ မက်ဆေ့ခ်ျကို ကြည့်မြင်လာသည့်အတွက် လိုအပ်ပါသည်) |
| **အကြောင်းအရာ လှည့်ပတ် ပုံစံ** | JD Agent သည် `[PARSED RESUME PASS-THROUGH]` ကို နောက်ဆုံး agent ထံ လွှဲပြောင်းပေးသည်၊ ထို့ကြောင့် MatchingAgent သည် ရှင်လ profile နှစ်ခုလုံးကို ရရှိနိုင်သည်; fan-in အရွယ်အစား OR-semantics နှစ်ဆခြေမှု ဖြစ်မှုကိုရှောင်ရှားသည် |
| **MCP ကိရိယာ ပေါင်းစည်းမှု** | `@tool` နှင့် `streamable_http_client` အသုံးပြု၍ MCP ဆာဗာတစ်ခုကို ခေါ်ယူသည် |
| **Hosted Agent ဘဝဝင်ထွက်လှုပ်ရှားမှု** | Scaffold → ဖွင့်တပ်ဆင် → ဒေသတွင်းစမ်းသပ် → တပ်ဆင် → Cloud တွင် အတည်ပြု |
| **`context_mode="last_agent"`** | Executor တစ်ယောက်စီသည် သူ၏ တိုက်ရိုက်ရှေ့က agent output ကိုသာ ကြည့်မြင်နိုင်သည် |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, တစ်ခုနှိပ် deployment |

---

## သင်ပြီးစီးခဲ့သည်

<details open>
<summary><strong>🅰️ လမ်းကြောင်း A - Foundry subscription</strong></summary>

- [x] Lab 01 ဖွဲ့စည်းမှုအတည်ပြုချက် - project, model၊ RBAC အားလုံး ထက်တန်းထား
- [x] Workflows template ကိုအသုံးပြုပြီး မျိုးစုံအေဂျင့် project တစ်ခု Scaffold ပြုလုပ်
- [x] ResumeParser, JD Agent, MatchingAgent, GapAnalyzer agent instructions စာရင်းလေးကို ရေးသားခဲ့သည်
- [x] Microsoft Learn MCP ကိရိယာကို `streamable_http_client` ဖြင့် ပေါင်းစည်းတင်ဆက်ခဲ့သည်
- [x] Workflow graph ကို `WorkflowBuilder` ဖြင့် ချိတ်ဆက်ထားသည် (ဆက်တိုက် pipeline နဲ့ Content relay)
- [x] ဒေသတွင်းစမ်းသပ်မှု ၃ခု (Agent Inspector) - fit score, gap cards, MCP URLs စမ်းသပ်ပြီး
- [x] Foundry Agent Service သို့ တင်သွင်းခဲ့သည် (containerized, managed identity)
- [x] Cloud playground တွင် အတည်ပြု - ဒေသတွင်းဖြေထွက်ကို အတည်ပြုခဲ့သည်

</details>

<details open>
<summary><strong>🅱️ လမ်းကြောင်း B - Foundry Local</strong></summary>

- [x] Lab 01 ဖွဲ့စည်းမှုအတည်ပြုချက် - Foundry Local သည် ဒေသတွင်း model ဖြင့် လည်ပတ်中
- [x] Workflows template အသုံးပြုပြီး မျိုးစုံအေဂျင့် project တစ်ခု Scaffold ပြုလုပ်
- [x] agent instructions နှင့် workflow graph ချိတ်ဆက်ရေးသားခဲ့သည်
- [x] Microsoft Learn MCP ကိရိယာ ပေါင်းစည်းတင်ဆက်ခဲ့သည်
- [x] ဒေသတွင်းစမ်းသပ်မှု ၃ခု စမ်းသပ်ခဲ့သည်
- [x] Cloud resource မလိုအပ်ဘဲ မျိုးစုံအေဂျင့် လုပ်ပေါ်မှု အတည်ပြုခဲ့သည်

</details>

---

## နောက်တစ်ဆင့်များ

### သင်ယူမှု ဆက်လက်လုပ်ဆောင်ရန်

| အရင်းအမြစ် | ဖော်ပြချက် |
|----------|-------------|
| **[Agent Framework SDK ကိုးကားချက်](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` API စာတမ်းများ |
| **[MCP tool ကိုယ်စားပြုစာရင်း](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Bing, GitHub သို့မဟုတ် ကိုယ်ပိုင် MCP ဆာဗာများသို့ agent များချိတ်ဆက်ရန် |
| **[အသိပညာ ထည့်သွင်းခြင်း (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | အစီရင်ခံစာများ၊ vector stores သို့မဟုတ် Bing ရှာဖွေရေးဖြင့် agent များကို ခိုင်မြဲစေရန် |
| **[Foundry မှ သုံးသပ်ချက်များ](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | စံချိန်ပြု automated evaluator များဖြင့် agent အရည်အသွေးတိုင်းတာခြင်း |
| **[Microsoft Foundry စာရွက်စာတမ်းများ](https://learn.microsoft.com/azure/foundry/)** | ပြည့်စုံသော ပလက်ဖောင်း ကိုးကားချက် |
| **[Foundry Toolkit - အသစ်တွေ](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Extension ထွက်ရှိမှု မှတ်တမ်းများနှင့် ပြင်ဆင်မှတ်တမ်း |

### ဒီ workflow ကို တိုးချဲ့ဖို့ အကြံပြုချက်များ

- **အေဂျင့် ပဉ္စမ ထည့်ပါ** - အင်တာဗျူးများ ကို ကိုင်တွယ်ညွှန်ပြခြင်း၊ gap report အပေါ် မူတည်၍ မျှော်မှန်း စာမေးပွဲမေးခွန်းများ ထုတ်ပေးသည့် coach တစ်ယောက်
- **Bing grounding tool ထည့်ပါ** - JD Agent သည် အလုပ်လိုအပ်ချက်များကို တိုးတက်စေရန် ဆင်တူအလုပ်ကြော်ငြာများ ရှာဖွေစေပါ
- **Resume ဒေတာဘေ့စ်သို့ ချိတ်ဆက်ပါ** - ကိုယ်ပိုင် `@tool` ဖြင့် ဒေတာဘေ့စ်မှ အလုပ်လျှောက်လွှာကို ရယူပါ
- **မော်ဒယ် မတူညီမှု စမ်းသပ်ပါ** - `gpt-4.1` နှင့် `gpt-4.1-mini` ၏ output အရည်အသွေး နှင့် latency ကို နှိုင်းယှဉ်ပါ
- **Foundry ဖြင့် သုံးသပ်ပါ** - Evaluations feature ကိုအသုံးပြု၍ fit reports များကို ရွှေ dataset နှင့် ဆင်တူစစ်ဆေးပါ

### Path B အသုံးပြုသူများအတွက်- cloud deployment သို့ အဆင့်မြှင့်တင်ရန်

Cloud သို့ deployment ပြုလုပ်ရန် ပြင်ဆင်သောအခါ-
1. Azure subscription ရယူပါ ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. [Lab 01, မော်ဂျူး 01](../../lab01-single-agent/docs/01-setup.md) ဖြေCompletion ပြုလုပ်ပါ (project ဖန်တီးခြင်း, model တပ်ဆင်ခြင်း, RBAC ထားခြင်း)
3. `.env` ဖိုင်တွင် Foundry project endpoint နှင့် model deployment နာမည် update ပြုလုပ်ပါ
4. [Module 06 - Foundry သို့ deployment](06-deploy-to-foundry.md) မှ ဆက်လက်လုပ်ဆောင်ပါ

---

## အရင်းအမြစ်များ ရှင်းလင်းသိမ်းဆည်းခြင်း (ရွေးချယ်စရာ)

ဒီ workshop ကာလအတွင်း ဖန်တီးထားတဲ့ Azure အရင်းအမြစ်များကို ဖယ်ရှားလိုပါက -

### ရွေးချယ်စရာ ၁: resource group ကို ဖျက်ရန် (အားလုံး ဖယ်ရှားမည်)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### ရွေးချယ်စရာ ၂: hosted agent ကိုသာ ဖျက်ရန်

1. [ai.azure.com](https://ai.azure.com) ဖြင့် ဝင်ကြည့်ပြီး → သင့် project → **Build** → **Agents** သို့ သွားပါ။
2. **PersonalCareerCopilot** ကို ရှာပြီး → **ဖျက်ရန်**ကို နှိပ်ပါ။

### ရွေးချယ်စရာ ၃: model deployment ကို ဖျက်ရန်

1. Foundry sidebar မှ သင့် project ကိုချဲ့ထွင်၍ → **Models** ကို နှိပ်ပါ။
2. Model deployment ကို ညာဘက်ကလစ်ဖျက်ရန်ကို နှိပ်ပါ။

> **ကုန်ကျစရိတ် မှတ်ချက်။** Hosted agent များသည် လည်ပတ်သောအခါတွင်သာ ကုန်ကျစရိတ် ဖြစ်တတ်သည်။ agent ကိုရပ်ထားလျှင် သို့မဟုတ် ဖျက်သိမ်းလျှင် တစ်ချိန်တည်းက်သော အခါ ဆက်လက်သုံးစွဲမှုလစ်သည်။ model deployment သည် မှတ်ပုံတင်ထားသောစွမ်းဆောင်ရည်အတွက် တချို့ အသေးစားကပြန်ကျစရိတ် ဖြစ်တတ်သည်- အဆုံးသတ်လိုသူများ ဖျက်ပါ။

---

**မရှေ့: [၀၈ - ပြဿနာဖြေရှင်းခြင်း](08-troubleshooting.md) · **ပင်မစာမျက်နှာ:** [Lab 02 README](../README.md) · [Workshop ပင်မစာမျက်နှာ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ပြောကြားချက်**
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) အသုံးပြု၍ ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးပမ်းနေသော်လည်း၊ စက်ကိရိယာဘာသာပြန်ခြင်းများတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် လိုအပ်ပါသည်။ မူလစာတမ်းကို မူရင်းဘာသာဖြင့်သာ ယုံကြည်စိတ်ချရသော အချက်အလက်အဖြစ် သတ်မှတ်သင့်သည်။ အရေးကြီးသည့် သတင်းအချက်အလက်များအတွက် ပရော်ဖက်ရှင်နယ် လူသားဘာသာပြန်သူဝန်ဆောင်မှုကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုခြင်းမှ ဖြစ်ပေါ်လာသော နားလည်မှုကွာခြားမှုများ သို့မဟုတ် မမှန်ကန်သော အသုံးပြုမှုများအတွက် ကျွန်ုပ်တို့ တာဝန်မခံပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->