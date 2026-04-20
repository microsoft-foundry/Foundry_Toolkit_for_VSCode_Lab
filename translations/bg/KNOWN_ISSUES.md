# Известни проблеми

Този документ проследява известни проблеми с текущото състояние на репозитория.

> Последна актуализация: 2026-04-15. Тествано с Python 3.13 / Windows в `.venv_ga_test`.

---

## Текущи фиксирани версии на пакети (всички три агента)

| Package | Current Version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(фиксирано — виж KI-003)* |

---

## KI-001 — Надграждане до GA 1.0.0 блокирано: `agent-framework-azure-ai` премахнат

**Статус:** Отворен | **Тежест:** 🔴 Висока | **Тип:** Критична промяна

### Описание

Пакетът `agent-framework-azure-ai` (фиксиран на `1.0.0rc3`) е **премахнат/оттеглен**
в GA версията (1.0.0, издадена 2026-04-02). Той е заменен от:

- `agent-framework-foundry==1.0.0` — агентен модел с хостинг във Foundry
- `agent-framework-openai==1.0.0` — агентен модел, базиран на OpenAI

Всички три файла `main.py` импортират `AzureAIAgentClient` от `agent_framework.azure`, което
генерира `ImportError` при GA пакетите. Пространството от имена `agent_framework.azure` все още съществува
в GA, но вече съдържа само класове за Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — не Foundry агенти.

### Потвърдена грешка (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Засегнати файлове

| Файл | Ред |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` несъвместим с GA `agent-framework-core`

**Статус:** Отворен | **Тежест:** 🔴 Висока | **Тип:** Критична промяна (блокира се от upstream)

### Описание

`azure-ai-agentserver-agentframework==1.0.0b17` (най-новият) твърдо фиксира
`agent-framework-core<=1.0.0rc3`. Инсталирането му заедно с `agent-framework-core==1.0.0` (GA)
задължава pip да **понижи версията** на `agent-framework-core` обратно до `rc3`, което нарушава
`agent-framework-foundry==1.0.0` и `agent-framework-openai==1.0.0`.

Следователно извикването `from azure.ai.agentserver.agentframework import from_agent_framework`, използвано от всички
агенти за свързване на HTTP сървъра, също е блокирано.

### Потвърден конфликт на зависимости (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Засегнати файлове

Всички три файла `main.py` — както горното ниво на импорти, така и импорта във функцията `main()`.

---

## KI-003 — Флагът `agent-dev-cli --pre` вече не е необходим

**Статус:** ✅ Фиксиран (без критична промяна) | **Тежест:** 🟢 Ниска

### Описание

Всички файлове `requirements.txt` преди това включваха `agent-dev-cli --pre`, за да изтеглят
пре-релийз CLI. След издаването на GA 1.0.0 на 2026-04-02, стабилната версия на
`agent-dev-cli` вече е налична без флага `--pre`.

**Прилагано решение:** Флагът `--pre` е премахнат от всичките три файла `requirements.txt`.

---

## KI-004 — Dockerfile файловете използват `python:3.14-slim` (първоначален образ за предварително издание)

**Статус:** Отворен | **Тежест:** 🟡 Ниска

### Описание

Всички `Dockerfile` файлове използват `FROM python:3.14-slim`, който е предварителна версия на Python.
За продукционни внедрявания това трябва да бъде фиксирано към стабилно издание (например `python:3.12-slim`).

### Засегнати файлове

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Препратки

- [agent-framework-core в PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry в PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:
Този документ е преведен с помощта на AI преводаческа услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия първичен език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален превод от човешки преводач. Ние не носим отговорност за никакви недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->