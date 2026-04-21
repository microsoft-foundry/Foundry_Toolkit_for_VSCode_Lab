# Masuala Yanayojulikana

Hati hii inafuatilia masuala yanayojulikana na hali ya hifadhidata ya sasa.

> Imesasishwa Tarehe: 2026-04-15. Imejaribiwa dhidi ya Python 3.13 / Windows katika `.venv_ga_test`.

---

## Vipini vya Kifurushi vya Sasa (mawakala wote watatu)

| Kifurushi | Toleo la Sasa |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(imekamilishwa — angalia KI-003)* |

---

## KI-001 — Kuboresha GA 1.0.0 Kuzuia: `agent-framework-azure-ai` Imetolewa

**Hali:** Imefunguliwa | **Ukali:** 🔴 Juu | **Aina:** Kuvunja

### Maelezo

Kifurushi cha `agent-framework-azure-ai` (imepiniwa `1.0.0rc3`) kili **tolewa/kufutwa**
katika toleo la GA (1.0.0, lililotolewa 2026-04-02). Kimebadilishwa na:

- `agent-framework-foundry==1.0.0` — Msimbo wa wakala unaoendeshwa na Foundry
- `agent-framework-openai==1.0.0` — Msimbo wa wakala unaounga mkono OpenAI

Faili zote tatu za `main.py` zinaingiza `AzureAIAgentClient` kutoka `agent_framework.azure`, ambayo
inasababisha `ImportError` chini ya vifurushi vya GA. Nafasi ya jina `agent_framework.azure` bado ipo
katika GA lakini sasa ina darasa za Azure Functions pekee (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — si mawakala wa Foundry.

### Hitilafu iliyothibitishwa (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Faili zilizoathirika

| Faili | Mstari |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Haifanani na GA `agent-framework-core`

**Hali:** Imefunguliwa | **Ukali:** 🔴 Juu | **Aina:** Kuvunja (inazuia kwa upande wa juu)

### Maelezo

`azure-ai-agentserver-agentframework==1.0.0b17` (ya hivi majuzi) inawekwa ngumu
`agent-framework-core<=1.0.0rc3`. Kuinstall pamoja na `agent-framework-core==1.0.0` (GA)
kunalazimisha pip **kusogeza nyuma** `agent-framework-core` kurudi `rc3`, ambayo kisha huvunja
`agent-framework-foundry==1.0.0` na `agent-framework-openai==1.0.0`.

Sehemu ya `from azure.ai.agentserver.agentframework import from_agent_framework` inayotumiwa na mawakala wote
kuunganisha seva ya HTTP pia inazuiliwa.

### Migongano ya utegemezi iliyothibitishwa (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Faili zilizoathirika

Faili zote tatu za `main.py` — pamoja na uingizaji wa ngazi ya juu na uingizaji ndani ya kazi katika `main()`.

---

## KI-003 — Bendera ya `agent-dev-cli --pre` Haibidi Tena

**Hali:** ✅ Imerekebishwa (isiyovunja) | **Ukali:** 🟢 Chini

### Maelezo

Faili zote za `requirements.txt` zilijumuisha awali `agent-dev-cli --pre` kuvuta
CLI ya awali. Tangu GA 1.0.0 ilipopatikana tarehe 2026-04-02, toleo thabiti la
`agent-dev-cli` sasa linapatikana bila bendera ya `--pre`.

**Rekebisho lilifanywa:** Bendera ya `--pre` imeondolewa kutoka kwenye faili zote tatu za `requirements.txt`.

---

## KI-004 — Faili za Docker Zinatumia `python:3.14-slim` (Picha ya Msingi ya Awali)

**Hali:** Imefunguliwa | **Ukali:** 🟡 Chini

### Maelezo

Faili zote za `Dockerfile` zinatumia `FROM python:3.14-slim` ambayo inafuata toleo la awali la Python.
Kwa utoaji wa uzalishaji inapaswa kuwekwa kwa toleo thabiti (kwa mfano, `python:3.12-slim`).

### Faili zilizoathirika

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Marejeo

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Halo**:  
Hati hii imetafsiriwa kwa kutumia huduma ya utafsiri wa AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kwa usahihi, tafadhali fahamu kuwa tafsiri za kiotomatiki zinaweza kuwa na makosa au upendeleo. Hati ya asili katika lugha yake ya asili inapaswa kuzingatiwa kama chanzo chenye mamlaka. Kwa taarifa muhimu, tafsiri ya mtu mtaalamu inashauriwa. Hatuna wajibu kwa kutoelewana au tafsiri potofu zinazotokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->