# Žinomos problemos

Šiame dokumente sekamos žinomos dabartinės saugyklos būsenos problemos.

> Paskutinį kartą atnaujinta: 2026-04-15. Išbandyta su Python 3.13 / Windows `.venv_ga_test`.

---

## Dabartiniai paketų fiksavimai (visi trys agentai)

| Paketas | Dabartinė versija |
|---------|-------------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(ištaisyta — žr. KI-003)* |

---

## KI-001 — GA 1.0.0 atnaujinimas neprasideda: pašalintas `agent-framework-azure-ai`

**Būsena:** Atidaryta | **Sunkumas:** 🔴 Aukštas | **Tipas:** Pertraukiantis

### Aprašymas

`agent-framework-azure-ai` paketas (užfiksuotas kaip `1.0.0rc3`) buvo **pašalintas/nutrauktas**
GA leidime (1.0.0, išleistas 2026-04-02). Jį pakeitė:

- `agent-framework-foundry==1.0.0` — Foundry pagrindu veikiantis agentų modelis
- `agent-framework-openai==1.0.0` — OpenAI pagrindu veikiantis agentų modelis

Visi trys `main.py` failai importuoja `AzureAIAgentClient` iš `agent_framework.azure`, kuris
GA paketų atveju išmeta `ImportError`. `agent_framework.azure` vardų sritis GA vis dar egzistuoja,
bet dabar joje yra tik Azure Functions klasės (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ne Foundry agentai.

### Patvirtinta klaida (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Pažeisti failai

| Failas | Eilutė |
|--------|--------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` nesuderinamas su GA `agent-framework-core`

**Būsena:** Atidaryta | **Sunkumas:** 🔴 Aukštas | **Tipas:** Pertraukiantis (užstrigęs dėl aukštesnės priklausomybės)

### Aprašymas

`azure-ai-agentserver-agentframework==1.0.0b17` (naujausias) griežtai fiksuoja
`agent-framework-core<=1.0.0rc3`. Įdiegus kartu su `agent-framework-core==1.0.0` (GA),
`pip` priverstas **nusileisti** `agent-framework-core` atgal į `rc3`, o tai suardo
`agent-framework-foundry==1.0.0` ir `agent-framework-openai==1.0.0`.

`from azure.ai.agentserver.agentframework import from_agent_framework` kvietimas, kurį naudoja visi
agentai HTTP serverio susiejimui, dėl to taip pat yra užblokuotas.

### Patvirtintas priklausomybių konfliktas (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Pažeisti failai

Visi trys `main.py` failai — tiek viršutiniai importai, tiek funkcijos viduje `main()` importai.

---

## KI-003 — `agent-dev-cli --pre` žymė nebereikalinga

**Būsena:** ✅ Ištaisyta (nepertraukianti) | **Sunkumas:** 🟢 Žemas

### Aprašymas

Visi `requirements.txt` failai anksčiau įtraukė `agent-dev-cli --pre`, kad būtų ištrauktas
ankstesnės versijos CLI. Nuo GA 1.0.0 išleidimo 2026-04-02, stabili `agent-dev-cli` versija
yra prieinama be `--pre` žymės.

**Pridėtas taisymas:** `--pre` žymė pašalinta iš visų trijų `requirements.txt` failų.

---

## KI-004 — Docker failai naudoja `python:3.14-slim` (išankstinės versijos bazinį atvaizdą)

**Būsena:** Atidaryta | **Sunkumas:** 🟡 Žemas

### Aprašymas

Visi `Dockerfile` failai naudoja `FROM python:3.14-slim`, kuris naudoja išankstinę Python kūrimo versiją.
Produkcinėse diegimuose tai turėtų būti užfiksuota į stabilų leidimą (pvz., `python:3.12-slim`).

### Pažeisti failai

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Nuorodos

- [agent-framework-core PyPI svetainėje](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry PyPI svetainėje](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:  
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors stengiamės užtikrinti tikslumą, atkreipkite dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojamas profesionalus žmogaus vertimas. Mes neatsakome už bet kokius nesusipratimus ar klaidingas interpretacijas, kilusias naudojant šį vertimą.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->