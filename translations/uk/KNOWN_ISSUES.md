# Відомі проблеми

Цей документ відстежує відомі проблеми з поточним станом репозиторію.

> Останнє оновлення: 2026-04-15. Тестувалося на Python 3.13 / Windows у `.venv_ga_test`.

---

## Поточні фіксовані версії пакетів (усі три агенти)

| Пакет | Поточна версія |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(виправлено — див. KI-003)* |

---

## KI-001 — Оновлення до GA 1.0.0 Заблоковано: `agent-framework-azure-ai` Видалено

**Статус:** Відкрито | **Серйозність:** 🔴 Висока | **Тип:** Критична помилка

### Опис

Пакет `agent-framework-azure-ai` (зафіксований на `1.0.0rc3`) був **видалений/застарілий**
у релізі GA (1.0.0, випущено 2026-04-02). Його замінюють:

- `agent-framework-foundry==1.0.0` — шаблон агента на основі Foundry
- `agent-framework-openai==1.0.0` — шаблон агента на основі OpenAI

Всі три файли `main.py` імпортують `AzureAIAgentClient` з `agent_framework.azure`, що
призводить до `ImportError` під час використання пакетів GA. Простір імен `agent_framework.azure` все ще існує
в GA, але тепер містить лише класи Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — а не агенти Foundry.

### Підтверджена помилка (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Затронуті файли

| Файл | Рядок |
|------|-------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Несумісний з GA `agent-framework-core`

**Статус:** Відкрито | **Серйозність:** 🔴 Висока | **Тип:** Критична помилка (залежить від upstream)

### Опис

`azure-ai-agentserver-agentframework==1.0.0b17` (найновіша версія) жорстко фіксує
`agent-framework-core<=1.0.0rc3`. Встановлення його разом із `agent-framework-core==1.0.0` (GA)
призводить до **пониження версії** `agent-framework-core` назад до `rc3`, що потім ламає
`agent-framework-foundry==1.0.0` та `agent-framework-openai==1.0.0`.

Виклик `from azure.ai.agentserver.agentframework import from_agent_framework`, який
використовують всі агенти для прив'язки HTTP сервера, також блокується.

### Підтверджений конфлікт залежностей (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Затронуті файли

Всі три файли `main.py` — і верхньорівневий імпорт, і імпорт всередині функції `main()`.

---

## KI-003 — Прапорець `agent-dev-cli --pre` більше не потрібен

**Статус:** ✅ Виправлено (без критичних змін) | **Серйозність:** 🟢 Низька

### Опис

Усі файли `requirements.txt` раніше включали `agent-dev-cli --pre` для отримання
передрелізної версії CLI. Від часу випуску GA 1.0.0 (2026-04-02) стабільна версія
`agent-dev-cli` тепер доступна без прапорця `--pre`.

**Виправлення:** Прапорець `--pre` було вилучено з усіх трьох файлів `requirements.txt`.

---

## KI-004 — Dockerfile використовує `python:3.14-slim` (базовий образ передрелізу)

**Статус:** Відкрито | **Серйозність:** 🟡 Низька

### Опис

Усі `Dockerfile` використовують `FROM python:3.14-slim`, який базується на передрелізній збірці Python.
Для виробничих розгортань слід фіксувати версію на стабільному релізі (наприклад, `python:3.12-slim`).

### Затронуті файли

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Посилання

- [agent-framework-core на PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry на PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:
Цей документ був перекладений за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, зверніть увагу, що автоматизовані переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується звертатися до професійного людського перекладу. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->