# Известные проблемы

Этот документ отслеживает известные проблемы текущего состояния репозитория.

> Последнее обновление: 2026-04-15. Тестировалось с Python 3.13 / Windows в `.venv_ga_test`.

---

## Текущие версии пакетов (все три агента)

| Пакет | Текущая версия |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(исправлено — см. KI-003)* |

---

## KI-001 — Блокировка обновления до GA 1.0.0: `agent-framework-azure-ai` удалён

**Статус:** Открыто | **Серьёзность:** 🔴 Высокая | **Тип:** Критическая

### Описание

Пакет `agent-framework-azure-ai` (зафиксирован в `1.0.0rc3`) был **удалён/устарел**
в релизе GA (1.0.0, выпущен 2026-04-02). Он заменён на:

- `agent-framework-foundry==1.0.0` — паттерн агента на базе Foundry
- `agent-framework-openai==1.0.0` — паттерн агента на базе OpenAI

Все три файла `main.py` импортируют `AzureAIAgentClient` из `agent_framework.azure`, что
приводит к `ImportError` при использовании GA пакетов. Пространство имён `agent_framework.azure` в GA
всё ещё существует, но теперь содержит только классы Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`), а не агенты Foundry.

### Подтверждённая ошибка (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Затронутые файлы

| Файл | Строка |
|------|--------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` несовместим с GA `agent-framework-core`

**Статус:** Открыто | **Серьёзность:** 🔴 Высокая | **Тип:** Критическая (зависит от upstream)

### Описание

`azure-ai-agentserver-agentframework==1.0.0b17` (последний) строго фиксирует
`agent-framework-core<=1.0.0rc3`. Установка вместе с `agent-framework-core==1.0.0` (GA)
принуждает pip **понизить версию** `agent-framework-core` обратно до `rc3`, что ломает
`agent-framework-foundry==1.0.0` и `agent-framework-openai==1.0.0`.

Вызов `from azure.ai.agentserver.agentframework import from_agent_framework`, используемый всеми
агентами для связывания HTTP-сервера, тоже заблокирован.

### Подтверждённый конфликт зависимостей (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Затронутые файлы

Все три файла `main.py` — и верхнеуровневый импорт, и импорт внутри функции `main()`.

---

## KI-003 — Флаг `agent-dev-cli --pre` больше не нужен

**Статус:** ✅ Исправлено (без критического влияния) | **Серьёзность:** 🟢 Низкая

### Описание

Ранее все файлы `requirements.txt` включали `agent-dev-cli --pre` для получения
предварительной версии CLI. С момента выхода GA 1.0.0 2026-04-02, стабильный релиз
`agent-dev-cli` доступен без флага `--pre`.

**Исправление:** Флаг `--pre` был удалён из всех трёх файлов `requirements.txt`.

---

## KI-004 — Dockerfile используют `python:3.14-slim` (предрелизный базовый образ)

**Статус:** Открыто | **Серьёзность:** 🟡 Низкая

### Описание

Все `Dockerfile` используют `FROM python:3.14-slim`, который основан на предрелизной сборке Python.
Для продакшен-развёртываний его следует зафиксировать на стабильном релизе (например, `python:3.12-slim`).

### Затронутые файлы

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Ссылки

- [agent-framework-core на PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry на PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:  
Данный документ был переведен с помощью службы автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, просим учитывать, что автоматические переводы могут содержать ошибки или неточности. Оригинальный документ на его родном языке следует считать авторитетным источником. Для критически важной информации рекомендуется использовать профессиональный перевод человеком. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->