# Модуль 8 - Усунення несправностей

Цей модуль охоплює поширені помилки, виправлення та стратегії налагодження, специфічні для багатоугентного робочого процесу.

## Проблеми з виходом агента

### GapAnalyzer каже «Я досі не маю звіт для співставлення»

**Симптом:** Відповідь GapAnalyzer просить вставити звіт для співставлення з розділами «Відсутні навички» та «Прогалини у сертифікації». Це відбувається навіть якщо ви надіслали як резюме, так і опис роботи.

**Причина:** Текст JD не було передано далі до JD Agent. При `context_mode="last_agent"`, `resume_executor` є єдиним виконавцем, який бачить вихідне повідомлення користувача. Якщо `RESUME_PARSER_INSTRUCTIONS` не включає текст JD у свій вихід, у JD Agent немає JD для аналізу, MatchingAgent не може обчислити рейтинг відповідності, і GapAnalyzer отримує беззмістовний вхід.

**Діагностика:**

Перегляньте журнали сервера, шукайте span MatchingAgent. Якщо він містить:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
пропуск або ланцюг передачі відсутній або пошкоджений.

**Виправлення:** Переконайтеся, що `RESUME_PARSER_INSTRUCTIONS` у `main.py` містить розділ `[JOB DESCRIPTION PASS-THROUGH]` та правило:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Також переконайтеся, що `JOB_DESCRIPTION_INSTRUCTIONS` містить правило ретрансляції `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Якщо будь-який із цих блоків інструкцій є заготовкою з майстра каркасу, замініть його на повну версію з [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent видає «Не можна обчислити рейтинг відповідності — JD не надано»

Це та сама коренева причина, що й вище. MatchingAgent отримав вихід JD Agent, але розділ `[PARSED RESUME PASS-THROUGH]` був відсутній або порожній, тому він не міг порівняти два профілі. Переконайтеся:
1. `JOB_DESCRIPTION_INSTRUCTIONS` включає правило ретрансляції: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` вказує агенту шукати розділи `[JD REQUIREMENTS]` та `[PARSED RESUME PASS-THROUGH]`.

Замініть обидва блоки інструкцій на повні версії з [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Відповідь з’являється двічі

**Симптом:** Вихід GapAnalyzer (або весь вихід конвеєра) з’являється двічі у відповіді Agent Inspector.

**Причина:** `WorkflowBuilder` використовує OR-семантику для вхідних ребер - виконавець далі запускається, як тільки завершується **будь-який** попередник. Якщо `matching_executor` має два вхідні ребра (одне від `resume_executor` і одне від `jd_executor`), він запускається двічі: один раз, коли завершується ResumeParser, і знову, коли завершується JD Agent. GapAnalyzer також тоді запускається двічі.

**Виправлення:** Переконайтеся, що граф `WorkflowBuilder` є строго послідовним конвеєром без об’єднань:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Якщо є випадкова лінія `.add_edge(resume_executor, matching_executor)`, видаліть її. Ретрансляція `[PARSED RESUME PASS-THROUGH]` у виході JD Agent вже дає MatchingAgent доступ до резюме.

---

## Проблеми з оточенням та конфігурацією

### Відсутні або неправильні значення `.env`

Файл `.env` має бути у каталозі `PersonalCareerCopilot/` (на тому ж рівні, що й `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Очікуваний вміст `.env`:

**Шлях A — хмарний Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Шлях B — Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Обидва шляхи використовують `FOUNDRY_PROJECT_ENDPOINT`. Значення відрізняється: хмара використовує кінцеву точку `https://` Foundry; локально використовується `http://localhost:5273/v1`. Запустіть `foundry model list`, щоб підтвердити точний псевдонім моделі для Шляху B.

> **Як знайти ваш `FOUNDRY_PROJECT_ENDPOINT`:** 
- Відкрийте бічну панель **Foundry Toolkit** у VS Code → клацніть правою кнопкою на вашому проекті → **Copy Project Endpoint**. 
- Або перейдіть на [Azure Portal](https://portal.azure.com) → ваш проект Foundry → **Overview** → **Project endpoint**.

> **Як знайти ваш `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** У бічній панелі Foundry Toolkit відкрийте ваш проект → **Models** → знайдіть ім’я розгорнутої моделі (наприклад, `gpt-4.1-mini`).

### Пріоритет змінних середовища

`main.py` використовує `load_dotenv(override=True)`, що означає:

| Пріоритет | Джерело | Перемагає, коли обидва встановлено? |
|----------|--------|-------------------------------|
| 1 (найвищий) | файл `.env` | Так |
| 2 | Змінна середовища оболонки / контейнера | Використовується, якщо ключ відсутній у `.env` |

У локальній розробці це робить `.env` джерелом істини (редагування `.env` негайно впливає на запуск). У хостинговому розгортанні Foundry впроваджує змінні середовища на рівні контейнера; оскільки `.env` не є частиною розгорнутого образу для цієї лабораторної установки, використовуються впроваджені значення контейнера.

---

## Сумісність версій

### Матриця версій пакетів

Багатоугентний робочий процес вимагає конкретних версій пакетів. Несумісність версій призводить до помилок під час виконання.

| Пакет | Вимагана версія | Команда перевірки |
|---------|-----------------|----------------|
| `agent-framework-foundry` | остання | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | остання | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | остання | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Поширені помилки версій

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Перевірка всіх версій одразу

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Очікуваний результат:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Проблеми з розгортанням

### Контейнер не запускається після розгортання

1. **Перегляньте журнали контейнера:**
   - Відкрийте бічну панель **Foundry Toolkit** → під вашим проектом натисніть **Agents** → вкладка **Hosted Agent** → виберіть вашого агента. Перевірте **Status** на вкладці **Details**, далі відкрийте вкладку **Playground** і використовуйте вкладку **Logs** в панелі **Session Details**, щоб побачити вихідні дані контейнера.
   - Шукайте трасування стеку Python або помилки відсутніх модулів.

2. **Поширені помилки запуску контейнера:**

   | Помилка у логах | Причина | Вирішення |
   |--------------|---------|-----------|
   | `ModuleNotFoundError` | відсутній пакет `requirements.txt` | Додати пакет, розгорнути повторно |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | не встановлено змінні середовища `agent.yaml` або `.env` | Оновити `agent.yaml` → розділ `environment_variables` (хостинг) або `.env` (локально) |
   | `azure.identity.CredentialUnavailableError` | не налаштовано Managed Identity | Foundry налаштовує це автоматично - переконайтесь, що ви розгортаєте через розширення |
   | `OSError: port 8088 already in use` | Dockerfile відкриває неправильний порт або конфлікт портів | Перевірте `EXPOSE 8088` у Dockerfile і `CMD ["python", "main.py"]` |
   | Контейнер завершується з кодом 1 | Неперехоплена виняткова ситуація в `main()` | Спочатку протестуйте локально ([Модуль 5](05-test-locally.md)), щоб виявити помилки перед розгортанням |

3. **Перерозгорніть після виправлення:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → виберіть того самого агента → розгорніть нову версію.

### Розгортання триває надто довго

Контейнери багатоугентної системи запускаються довше, бо під час запуску створюють 4 екземпляри агентів. Звичайні часи запуску:

| Етап | Очікувана тривалість |
|-------|---------------------|
| Побудова образу контейнера | 1-3 хвилини |
| Відправка образу в ACR | 30-60 секунд |
| Запуск контейнера (одиночний агент) | 15-30 секунд |
| Запуск контейнера (багатоугентний) | 30-120 секунд |
| Агент доступний у Playground | 1-2 хвилини після статусу "Started" |

> Якщо статус "Pending" триває понад 5 хвилин, перевірте журнали контейнера на наявність помилок.

---

## Проблеми з RBAC та дозволами

### `403 Forbidden` або `AuthorizationFailed`

Вам потрібна роль **[Foundry User](https://aka.ms/foundry-ext-project-role)** у вашому проекті Foundry (раніше називалась **Azure AI User** - ідентифікатор ролі незмінний):

1. Перейдіть до [Azure Portal](https://portal.azure.com) → вашого ресурсу Foundry **проекту**.
2. Натисніть **Access control (IAM)** → **Role assignments**.
3. Знайдіть своє ім'я → підтвердіть, що вказано **Foundry User** (або стару назву **Azure AI User**).
4. Якщо відсутній: **Add** → **Add role assignment** → знайдіть **Foundry User** → призначте на свій обліковий запис.

Докладніше див. у документації [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Розгортання моделі недоступне

Якщо агент повертає помилки, пов’язані з моделлю:

1. Переконайтеся, що модель розгорнута: бічна панель Foundry → розгорніть проект → **Models** → перевірте `gpt-4.1-mini` (або вашу модель) зі статусом **Succeeded**.
2. Перевірте, чи збігається ім'я розгортання: порівняйте `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` (або `agent.yaml`) з фактичним іменем розгортання в бічній панелі.
3. Якщо розгортання закінчилося (безкоштовний рівень): розгорніть повторно з [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Проблеми з Foundry Local (Шлях B)

### Сервіс Foundry Local не працює

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Симптом | Причина | Виправлення |
|---------|---------|------------|
| Перевірка стану повертає `503` | Сервіс не запущено | `foundry local start` або натисніть **Start** у бічній панелі Foundry Toolkit |
| Перевірка стану не встигає | Модель ще завантажується | Зачекайте 30–60 с після запуску; більші моделі завантажуються довше |
| `StatusCode: 404` на `/v1/health` | Неправильний порт | За замовчуванням `5273`. Перевірте `foundry local status` для фактичного порту |
| Недостатньо ресурсів | Foundry Local потребує ~4 ГБ вільної ОЗП | Закрийте інші програми |
| Завантаження моделі не вдається | Недостатньо місця на диску | Моделі важать 2–8 ГБ. Звільніть місце, потім `foundry model pull <name>` |

### Несумісність імені моделі

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Встановіть `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` точно відповідно до показаного псевдоніма (наприклад, `phi-4-mini`, не `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` при локальному запуску (Шлях B)

В лабораторії `main.py` використовує `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local вимагає, щоб ця змінна вказувала на локальний сервіс - **не на** `AZURE_AI_PROJECT_ENDPOINT`. Переконайтеся, що ваш `.env` містить:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Інструмент MCP все ще робить вихідний виклик (Шлях B)

Це нормально. Інструмент `search_microsoft_learn_for_plan` отримує навчальні ресурси з `https://learn.microsoft.com/api/mcp`. **Тільки запит за назвою навички** надсилається через мережу – резюме та текст JD обробляються повністю на вашому пристрої і ніколи не передаються. Якщо потрібна повністю офлайн-робота, додайте резервне `try/except` у інструмент, яке повертає статичну URL `learn.microsoft.com`, коли кінцева точка недоступна.

---

## Отримання допомоги

Якщо ви застрягли після спроби наведених вище виправлень:

1. **Перевірте журнали сервера** - Більшість помилок виробляють слід стека Python у терміналі. Прочитайте повний трасбек.
2. **Шукайте текст помилки** - Скопіюйте текст помилки і шукайте у [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Відкрийте Issue** - Створіть issue у [репозиторії майстерні](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) з:
   - Повідомленням про помилку або скріншотом
   - Версією вашого пакету (`pip list | Select-String "agent-framework"`)
   - Версією Python (`python --version`)
   - Чи проблема локальна, чи після розгортання

---

### Контрольна точка

- [ ] Ви знаєте, як перевірити і виправити проблеми конфігурації `.env`
- [ ] Ви можете підтвердити, що версії пакетів відповідають потрібній матриці
- [ ] Ви вмієте перевіряти журнали контейнера на предмет помилок розгортання
- [ ] Ви можете перевірити ролі RBAC в Azure Portal

---

**Попередня:** [07 - Verify in Playground](07-verify-in-playground.md) · **Наступна:** [09 - Summary →](09-summary.md) · **Домашня:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:
Цей документ було перекладено за допомогою сервісу штучного інтелекту для перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->