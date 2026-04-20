# Познати проблеми

Овај документ прати познате проблеме са тренутним стањем репозиторијума.

> Последње ажурирање: 2026-04-15. Тестирано на Python 3.13 / Windows у `.venv_ga_test`.

---

## Тренутне закључане верзије пакета (сва три агента)

| Пакет | Тренутна верзија |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(исправљено — види KI-003)* |

---

## KI-001 — Прелазак на GA 1.0.0 Блокиран: `agent-framework-azure-ai` је Уклоњен

**Статус:** Отворено | **Сериозност:** 🔴 Висока | **Тип:** Прекидајући

### Опис

Пакет `agent-framework-azure-ai` (закључан на `1.0.0rc3`) је **уклоњен/депрецатиран**
у GA издању (1.0.0, објављен 2026-04-02). Заменио га је:

- `agent-framework-foundry==1.0.0` — образац агента хостован у Foundry-у
- `agent-framework-openai==1.0.0` — образац агента подржан од стране OpenAI

Сва три `main.py` фајла увозе `AzureAIAgentClient` из `agent_framework.azure`, што
изазива `ImportError` са GA пакетима. `agent_framework.azure` namespace и даље постоји
у GA, али сад садржи само Azure Functions класе (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — а не Foundry агенте.

### Потврђена грешка (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Погођени фајлови

| Фајл | Ред |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Неблагодарно са GA `agent-framework-core`

**Статус:** Отворено | **Сериозност:** 🔴 Висока | **Тип:** Прекидајући (заглављен због надређеног)

### Опис

`azure-ai-agentserver-agentframework==1.0.0b17` (најновије) оштро закључава
`agent-framework-core<=1.0.0rc3`. Инсталирање уз `agent-framework-core==1.0.0` (GA)
присиљава pip да **поништи надоградњу** `agent-framework-core` назад на `rc3`, што онда
крши `agent-framework-foundry==1.0.0` и `agent-framework-openai==1.0.0`.

Позив `from azure.ai.agentserver.agentframework import from_agent_framework` који користе сви
агенти за везивање HTTP сервера је стога такође блокиран.

### Потврђени конфликт зависности (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Погођени фајлови

Сва три `main.py` фајла — и увоз на врху и увоз у функцији у `main()`.

---

## KI-003 — Флаг `agent-dev-cli --pre` Више Није Потребан

**Статус:** ✅ Фиксирано (непрекидајуће) | **Сериозност:** 🟢 Ниска

### Опис

Сви `requirements.txt` фајлови су раније укључивали `agent-dev-cli --pre` да би повукли
пре-релизну верзију CLI-а. Од када је GA 1.0.0 објављен 2026-04-02, стабилна верзија
`agent-dev-cli` је сада доступна без флага `--pre`.

**Примењена поправка:** Флаг `--pre` је уклоњен са сва три `requirements.txt` фајла.

---

## KI-004 — Dockerfile-ови Користе `python:3.14-slim` (Прирелизна Основна Слика)

**Статус:** Отворено | **Сериозност:** 🟡 Ниска

### Опис

Сви `Dockerfile` користе `FROM python:3.14-slim` који прати прирелизну Python верзију.
За продукционе примене ово треба да буде закључано на стабилно издање (нпр. `python:3.12-slim`).

### Погођени фајлови

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Референце

- [agent-framework-core на PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry на PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Одрицање од одговорности**:  
Овај документ је преведен коришћењем AI услуге за превођење [Co-op Translator](https://github.com/Azure/co-op-translator). Иако тежимо ка прецизности, имајте у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитетним извором. За критичне информације препоручује се професионални људски превод. Не сносимо одговорност за било какве неспоразуме или погрешна тумачења која произилазе из коришћења овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->