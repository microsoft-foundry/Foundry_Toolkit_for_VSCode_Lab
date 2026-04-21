# သိရှိထားသော ပြဿနာများ

ဤစာတမ်းသည် လက်ရှိ repository အခြေအနေတွင် သိရှိထားသော ပြဿနာများကို လိုက်လံမှတ်တမ်းတင်ထားသည်။

> နောက်ဆုံး အပ်ဒိတ်ပြုလုပ်သည့်နေ့: 2026-04-15။ Python 3.13 / Windows တွင် `.venv_ga_test` ကို စမ်းသပ်သည်။

---

## လက်ရှိ Package များ၏ Version သတ်မှတ်ချက်များ (သုံးဦးလုံး Agent များ)

| Package | လက်ရှိ Version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(ပြင်ဆင်ပြီး — KI-003 ကို ကြည့်ရှုပါ)* |

---

## KI-001 — GA 1.0.0 အဆင့်မြှင့်တင်မှု အတားအဆီး: `agent-framework-azure-ai` ဖယ်ရှားခံခဲ့သည်

**အခြေအနေ:** ဖွင့်ထားသည် | **ထိခိုက်မှု:** 🔴 အလွန်မြင့်မား | **အမျိုးအစား:** ချိုးဖျက်မှု

### ဖော်ပြချက်

`agent-framework-azure-ai` package (version `1.0.0rc3` သတ်မှတ်ထားသော) ကို GA မိတ္တူမိတ်ဆက်မှု (1.0.0, 2026-04-02 မှ မိတ်ဆက်) တွင် **ဖယ်ရှား/တားမြစ်** လုပ်ခဲ့သည်။
ဒါကို အောက်ပါ package များဖြင့် အစားထိုးထားသည်။

- `agent-framework-foundry==1.0.0` — Foundry ပလက်ဖောင်းတွင် မျိုးဆက် အသစ်အာဂျင့် ပုံစံ
- `agent-framework-openai==1.0.0` — OpenAI အစိတ်အပိုင်း မျိုးဆက် အသစ်အာဂျင့် ပုံစံ

သုံးဦးလုံး `main.py` ဖိုင်များတွင် `AzureAIAgentClient` ကို `agent_framework.azure` မှ ယူသုံးသည်။ GA package များအောက်တွင် မလိုက်ဖက်သော `ImportError` ဖြစ်ပေါ်သည်။ GA အတွင်း `agent_framework.azure` namespace သည် ရှိသည်၊ သို့သော် ယင်းတွင် Azure Functions အသုံးပြုသည့် class များသာပါဝင်ပြီး Foundry အာဂျင့် မဟုတ်ပါ (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`)။

### သေချာပြီဖြစ်သော အမှား (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### ထိခိုက်သော ဖိုင်များ

| ဖိုင် | အတန်း |
|------|-------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` သည် GA `agent-framework-core` နှင့် မလိုက်ဖက်မှုရှိသည်

**အခြေအနေ:** ဖွင့်ထားသည် | **ထိခိုက်မှု:** 🔴 အလွန်မြင့်မား | **အမျိုးအစား:** ချိုးဖျက်မှု (အပေါ်ပိုင်းမှ တားမြစ်ခံထား)

### ဖော်ပြချက်

`azure-ai-agentserver-agentframework==1.0.0b17` (နောက်ဆုံးထွက်) သည်
`agent-framework-core<=1.0.0rc3` ကို စည်းကမ်းတစ်ရပ်အနေနဲ့ မှတ်ထားသည်။ `agent-framework-core==1.0.0` (GA) ကို တပြိုင်နက်တည်း ထည့်သွင်းခြင်းသည် pip ကို `rc3` version သို့ ပြန်လျော့ချ ဖို့ বাধကြောင်းလမ်းပြသည့် ဖြစ်စဉ်ဖြစ်ကာ၊ ထိုအခါ `agent-framework-foundry==1.0.0` နှင့် `agent-framework-openai==1.0.0` များ ကျဆင်းမှုရှိစေသည်။

HTTP ဝန်ဆောင်မှု server ကို bindings ပြုလုပ်ရန် အသုံးပြုသော `from azure.ai.agentserver.agentframework import from_agent_framework` ဖုန်းမှုလည်း အတားအဆီးဖြစ်နေသည်။

### သေချာပြီဖြစ်သော dependency မဟုတ်မှု (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### ထိခိုက်သော ဖိုင်များ

`main.py` သုံးဖိုင်လုံး၏ ထိပ်ဆုံး import နဲ့ `main()` အတွင်း import နှစ်ခါ ပြုလုပ်ထားသည်။

---

## KI-003 — `agent-dev-cli --pre` အချက်ပြ မလိုတော့တော့ပါ

**အခြေအနေ:** ✅ ပြင်ဆင်ပြီး (ချိုးဖျက်မှုမရှိ) | **ထိခိုက်မှု:** 🟢 နည်းသော

### ဖော်ပြချက်

ယခင်က `requirements.txt` ဖိုင်များအားလုံးတွင် pre-release CLI ကို ယူရန် `agent-dev-cli --pre` အချက်ပြထည့်ထားသည်။ GA 1.0.0 မှ 2026-04-02 တွင် မိတ်ဆက်ပြီးနောက် `agent-dev-cli` သည် `--pre` အချက်ပြ မပါဘဲ ဖြစ်လာသည်။

**ပြင်ဆင်မှု။** `requirements.txt` သုံးခုလုံးမှ `--pre` အချက်ပြ ဖယ်ရှားပြီးဖြစ်သည်။

---

## KI-004 — Dockerfiles များသည် `python:3.14-slim` (Pre-release Base Image) ကို အသုံးပြုထားသည်

**အခြေအနေ:** ဖွင့်ထားသည် | **ထိခိုက်မှု:** 🟡 နည်းသော

### ဖော်ပြချက်

Dockerfile များအားလုံးတွင် `FROM python:3.14-slim` ကို အသုံးပြုထားပြီး ၎င်းသည် Python ၏ pre-release build တစ်ခုဖြစ်သည်။ ထုတ်လုပ်မှု Deployment များတွင် သေချာသော stable release (ဥပမာ - `python:3.12-slim`) ကို သတ်မှတ်ရန် လိုအပ်ပါသည်။

### ထိခိုက်သော ဖိုင်များ

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## ကိုးကားချက်များ

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**အသိပေးချက်**  
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) မှတဆင့် ဘာသာပြန်ထားပါသည်။ မှန်ကန်မှုအတွက် ကြိုးပမ်းထားပေမယ့် ကိုယ်ပိုင်ပြုပြင်မှုမရှိသော ဘာသာပြန်ချက်များတွင် အမှားများ သို့မဟုတ် မှားယွင်းမှုများရှိနိုင်ကြောင်း သတိပြုပါ။ မူရင်းစာတမ်းကို မူရင်းဘာသာဖြင့်သာ အတည်ပြုရမည့် အရင်းအမြစ်အဖြစ် ထည့်သတ်စဉ်းစားသင့်သည်။ အရေးကြီးသည့်အချက်အလက်များအတွက် ကျွမ်းကျင်သော လူသားဘာသာပြန်ခြင်းကို အကြံပြုပါသည်။ ဤဘာသာပြန်ခြင်းကိုအသုံးပြုမှုကြောင့် ဖြစ်ပေါ်နိုင်သည့် နားလည်မှုမှားခြင်းများ သို့မဟုတ် မှားယွင်းနားလည်မှုများအတွက် ကျွန်ုပ်တို့ ဦးစားမပေးပါကြောင်း အသိပေးအပ်ပါသည်။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->