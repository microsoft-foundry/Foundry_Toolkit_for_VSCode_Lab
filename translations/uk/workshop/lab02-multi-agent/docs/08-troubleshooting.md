# Модуль 8 - Вирішення проблем (Multi-Agent)

Цей модуль охоплює поширені помилки, виправлення та стратегії відлагодження, специфічні для багатоустановного робочого процесу. Для загальних проблем з розгортанням Foundry також звертайтеся до [підручника з усунення неполадок лабораторії 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Швидка довідка: Помилка → Виправлення

| Помилка / Симптом | Ймовірна причина | Виправлення |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Відсутній файл `.env` або значення не встановлені | Створіть `.env` з `PROJECT_ENDPOINT=<your-endpoint>` та `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Віртуальне середовище не активоване або залежності не встановлені | Запустіть `.\.venv\Scripts\Activate.ps1` потім `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Пакет MCP не встановлений (відсутній у requirements) | Запустіть `pip install mcp` або перевірте, чи включено його як транзитивну залежність у `requirements.txt` |
| Агент запускається, але повертає порожню відповідь | Несумісність `output_executors` або відсутні ребра | Перевірте `output_executors=[gap_analyzer]` і чи всі ребра існують у `create_workflow()` |
| Лише одна картка пропуску (інші відсутні) | Інструкції GapAnalyzer неповні | Додайте абзац `CRITICAL:` до `GAP_ANALYZER_INSTRUCTIONS` - див. [Модуль 3](03-configure-agents.md) |
| Оцінка відповідності 0 або відсутня | MatchingAgent не отримав дані з попереднього кроку | Переконайтеся, що існують обидва `add_edge(resume_parser, matching_agent)` і `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Сервер MCP відхилив виклик інструменту | Перевірте інтернет-з’єднання. Спробуйте відкрити `https://learn.microsoft.com/api/mcp` у браузері. Повторіть спробу |
| Вивід не містить URL Microsoft Learn | Інструмент MCP не зареєстровано або неправильна кінцева точка | Перевірте `tools=[search_microsoft_learn_for_plan]` на GapAnalyzer і правильність `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | Інший процес використовує порт 8088 | Запустіть `netstat -ano \| findstr :8088` (Windows) або `lsof -i :8088` (macOS/Linux) і зупиніть конфліктний процес |
| `Address already in use: port 5679` | Конфлікт порту debugpy | Зупиніть інші сесії відлагодження. Виконайте `netstat -ano \| findstr :5679` щоб знайти та завершити процес |
| Агент Inspector не відкривається | Сервер не повністю запущений або конфлікт порту | Дочекайтеся журналу "Server running". Переконайтеся, що порт 5679 вільний |
| `azure.identity.CredentialUnavailableError` | Не виконано вхід через Azure CLI | Запустіть `az login`, потім перезапустіть сервер |
| `azure.core.exceptions.ResourceNotFoundError` | Розгортання моделі не існує | Перевірте, що `MODEL_DEPLOYMENT_NAME` співпадає з розгорнутою моделлю у вашому проєкті Foundry |
| Статус контейнера "Failed" після розгортання | Збій контейнера під час запуску | Перевірте журнали контейнера у боковій панелі Foundry. Типово: відсутня змінна середовища або помилка імпорту |
| Розгортання показує "Pending" більше 5 хвилин | Контейнер занадто довго запускається або обмеження ресурсів | Зачекайте до 5 хвилин для багатоустановного агенту (створює 4 інстанси). Якщо стан зберігається, перевірте логи |
| `ValueError` з `WorkflowBuilder` | Неправильна конфігурація графа | Переконайтеся, що `start_executor` встановлено, `output_executors` є списком, і відсутні циклічні ребра |

---

## Проблеми з оточенням та конфігурацією

### Відсутні або неправильні значення `.env`

Файл `.env` має знаходитись у каталозі `PersonalCareerCopilot/` (на тому ж рівні, що й `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Очікуваний вміст `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Як знайти PROJECT_ENDPOINT:** 
- Відкрийте бокову панель **Microsoft Foundry** у VS Code → клацніть правою кнопкою миші по вашому проєкту → **Copy Project Endpoint**. 
- Або зайдіть на [Azure Portal](https://portal.azure.com) → ваш проєкт Foundry → **Overview** → **Project endpoint**.

> **Як знайти MODEL_DEPLOYMENT_NAME:** У боковій панелі Foundry розгорніть ваш проєкт → **Models** → знайдіть назву вашої розгорнутої моделі (наприклад, `gpt-4.1-mini`).

### Пріоритет змінних оточення

`main.py` використовує `load_dotenv(override=False)`, що означає:

| Пріоритет | Джерело | Перемагає, якщо обидва встановлені? |
|----------|--------|------------------------|
| 1 (найвищий) | Змінна оточення оболонки | Так |
| 2 | Файл `.env` | Лише якщо змінна оболонки не встановлена |

Це означає, що змінні оточення Foundry runtime (встановлені через `agent.yaml`) мають пріоритет над `.env` під час розгортання в хості.

---

## Сумісність версій

### Матриця версій пакетів

Для багатоустановного робочого процесу потрібні певні версії пакетів. Несумісні версії викликають помилки під час виконання.

| Пакет | Потрібна версія | Команда перевірки |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | остання pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Поширені помилки версій

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Виправлення: оновлення до rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` не знайдено або Inspector несумісний:**

```powershell
# Виправлення: встановлення з прапором --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Виправлення: оновлення пакету mcp
pip install mcp --upgrade
```

### Перевірка всіх версій одразу

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Очікуваний вивід:

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

## Проблеми з інструментом MCP

### Інструмент MCP не повертає результатів

**Симптом:** Картки пропуску висвічують "No results returned from Microsoft Learn MCP" або "No direct Microsoft Learn results found".

**Можливі причини:**

1. **Проблеми з мережею** - кінцева точка MCP (`https://learn.microsoft.com/api/mcp`) недоступна.
   ```powershell
   # Тестувати з'єднання
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Якщо повертає `200`, кінцева точка доступна.

2. **Занадто конкретний запит** - назва навички надмірно вузька для пошуку Microsoft Learn.
   - Це очікувано для дуже спеціалізованих навичок. Інструмент має резервний URL у відповіді.

3. **Таймаут сесії MCP** - стрімове HTTP-з’єднання пройшло таймаут.
   - Повторіть запит. Сесії MCP тимчасові, можливо потрібно перепідключення.

### Пояснення журналів MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Журнал | Значення | Дія |
|-----|---------|--------|
| `GET → 405` | MCP клієнт перевіряє під час ініціалізації | Нормально - ігнорувати |
| `POST → 200` | Виклик інструменту успішний | Очікувано |
| `DELETE → 405` | MCP клієнт перевіряє під час очищення | Нормально - ігнорувати |
| `POST → 400` | Некоректний запит (помилковий формат запиту) | Перевірте параметр `query` в `search_microsoft_learn_for_plan()` |
| `POST → 429` | Обмеження швидкості | Зачекайте і спробуйте знову. Зменшіть параметр `max_results` |
| `POST → 500` | Помилка сервера MCP | Тимчасово - повторіть спробу. Якщо повторюється, можливо API MCP Microsoft Learn недоступне |
| Таймаут з’єднання | Проблеми мережі або сервер MCP недоступний | Перевірте інтернет. Спробуйте `curl https://learn.microsoft.com/api/mcp` |

---

## Проблеми з розгортанням

### Контейнер не запускається після розгортання

1. **Перевірте журнали контейнера:**
   - Відкрийте бокову панель **Microsoft Foundry** → розгорніть **Hosted Agents (Preview)** → натисніть вашого агента → розгорніть версію → **Container Details** → **Logs**.
   - Шукайте трасування у Python або помилки відсутніх модулів.

2. **Типові помилки запуску контейнера:**

   | Помилка у логах | Причина | Виправлення |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Відсутній пакет у `requirements.txt` | Додайте пакет, повторно розгорніть |
   | `RuntimeError: Missing required environment variable` | Змінні оточення `agent.yaml` не встановлені | Оновіть секцію `environment_variables` в `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Не налаштований Managed Identity | Foundry це робить автоматично - перевірте, що розгортаєте через розширення |
   | `OSError: port 8088 already in use` | Dockerfile експонує неправильний порт або конфлікт порту | Переконайтеся в `EXPOSE 8088` в Dockerfile і `CMD ["python", "main.py"]` |
   | Контейнер завершується з кодом 1 | Необроблена помилка в `main()` | Спершу протестуйте локально ([Модуль 5](05-test-locally.md)), щоб виявити помилки перед розгортанням |

3. **Перерозгорніть після виправлення:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → оберіть того ж агента → розгорніть нову версію.

### Розгортання займає забагато часу

Багатоустановні контейнери запускаються довше, бо створюють 4 інстанси агентів при запуску. Типові часи запуску:

| Етап | Очікуваний час |
|-------|------------------|
| Збірка образу контейнера | 1-3 хвилини |
| Відправка образу в ACR | 30-60 секунд |
| Запуск контейнера (один агент) | 15-30 секунд |
| Запуск контейнера (багато агентів) | 30-120 секунд |
| Агент доступний у Playground | 1-2 хвилини після "Started" |

> Якщо статус "Pending" зберігається понад 5 хвилин, перевірте журнали контейнера на помилки.

---

## Проблеми з RBAC та дозволами

### `403 Forbidden` або `AuthorizationFailed`

Вам потрібна роль **[Azure AI User](https://aka.ms/foundry-ext-project-role)** у вашому Foundry проєкті:

1. Перейдіть на [Azure Portal](https://portal.azure.com) → ресурс вашого Foundry **проєкту**.
2. Клікніть **Access control (IAM)** → **Role assignments**.
3. Знайдіть своє ім’я → переконайтеся, що є **Azure AI User**.
4. Якщо відсутня: **Add** → **Add role assignment** → знайдіть **Azure AI User** → призначте на свій обліковий запис.

Детальніше дивіться у документації [RBAC для Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Недоступність розгортання моделі

Якщо агент повертає помилки, пов’язані з моделлю:

1. Перевірте, що модель розгорнута: у боковій панелі Foundry → розгорніть проєкт → **Models** → перевірте, що `gpt-4.1-mini` (або ваша модель) має статус **Succeeded**.
2. Переконайтеся, що ім’я розгортання збігається: порівняйте `MODEL_DEPLOYMENT_NAME` у `.env` (або `agent.yaml`) з фактичним ім’ям розгортання у боковій панелі.
3. Якщо розгортання закінчилося (безкоштовний рівень): розгорніть знову з [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Проблеми з Agent Inspector

### Inspector відкривається, але показує "Disconnected"

1. Переконайтеся, що сервер запущений: перевірте повідомлення "Server running on http://localhost:8088" у терміналі.
2. Перевірте порт `5679`: Inspector підключається через debugpy на порті 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Перезапустіть сервер і відкрийте Inspector знову.

### Inspector показує часткову відповідь

Відповіді багатоустановного агента довгі й надходять стрімінгово поступово. Дочекайтеся повного завершення відповіді (може зайняти 30-60 секунд залежно від кількості карток пропуску та викликів інструменту MCP).

Якщо відповідь постійно обрізається:
- Перевірте, що інструкції GapAnalyzer містять блок `CRITICAL:`, який забороняє об’єднання карток пропуску.
- Перевірте ліміт токенів вашої моделі - `gpt-4.1-mini` підтримує до 32К вивідних токенів, що має бути достатньо.

---

## Поради щодо продуктивності

### Повільні відповіді

Багатоустановні робочі процеси за своєю природою повільніші за одноустановні через послідовні залежності і виклики інструменту MCP.

| Оптимізація | Як зробити | Вплив |
|-------------|-----|--------|
| Зменшити виклики MCP | Знизити параметр `max_results` в інструменті | Менше HTTP-запитів |
| Спрощення інструкцій | Коротші, сфокусовані підказки агента | Швидше направлене розумове моделювання (LLM) |
| Використання `gpt-4.1-mini` | Швидше за `gpt-4.1` для розробки | Приблизно у 2 рази швидше |
| Зменшити деталізацію карток пропуску | Спрощення формату карток у інструкціях GapAnalyzer | Менше вихідних даних для генерації |

### Типові часи відповіді (локально)

| Конфігурація | Очікуваний час |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 карток пропуску | 30-60 секунд |
| `gpt-4.1-mini`, 8+ карток пропуску | 60-120 секунд |
| `gpt-4.1`, 3-5 карток пропуску | 60-120 секунд |
---

## Отримання допомоги

Якщо ви застрягли після спроби наведених вище виправлень:

1. **Перевірте журнали сервера** - Більшість помилок генерують трасу стека Python у терміналі. Прочитайте повний трасування.
2. **Пошукайте повідомлення про помилку** - Скопіюйте текст помилки і пошукайте на [Microsoft Q&A для Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Відкрийте issue** - Створіть issue у [репозиторії воркшопу](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) з:
   - Повідомленням про помилку або скріншотом
   - Версіями ваших пакетів (`pip list | Select-String "agent-framework"`)
   - Версією Python (`python --version`)
   - Чи проблема локальна, чи після розгортання

---

### Контрольний список

- [ ] Ви можете ідентифікувати та виправити найпоширеніші помилки багатоядерних агентів, використовуючи таблицю швидких посилань
- [ ] Ви знаєте, як перевірити та виправити проблеми конфігурації `.env`
- [ ] Ви можете перевірити, чи відповідають версії пакетів необхідній матриці
- [ ] Ви розумієте записи журналу MCP і можете діагностувати збої інструментів
- [ ] Ви знаєте, як перевірити журнали контейнерів на наявність помилок розгортання
- [ ] Ви можете перевірити ролі RBAC в Azure Portal

---

**Попередня:** [07 - Verify in Playground](07-verify-in-playground.md) · **Головна:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:  
Цей документ було перекладено за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, просимо враховувати, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ на рідній мові слід вважати авторитетним джерелом. Для критичної інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння чи неправильне трактування, що виникли внаслідок використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->