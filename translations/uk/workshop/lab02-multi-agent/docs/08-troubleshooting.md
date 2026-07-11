# Модуль 8 - Виправлення помилок

У цьому модулі розглядаються поширені помилки, способи їх виправлення та стратегії відлагодження, специфічні для багатогентного робочого процесу.

## Проблеми з виводом агента

### GapAnalyzer каже «Я все ще не маю відповідного звіту»

**Симптом:** У відповідь GapAnalyzer просить вставити відповідний звіт із «Відсутніми навичками» та «Пробілами у сертифікації». Це відбувається навіть коли ви надіслали і резюме, і опис роботи.

**Причина:** Текст JD не був переданий далі JD Agent. При `context_mode="last_agent"` `resume_executor` є єдиним виконавцем, який коли-небудь бачить оригінальне повідомлення користувача. Якщо `RESUME_PARSER_INSTRUCTIONS` не включає текст JD у свій вивід, JD Agent немає JD для аналізу, MatchingAgent не може обчислити оцінку відповідності, а GapAnalyzer отримує недоречне вхідне повідомлення.

**Діагностика:**

У журналах сервера дізнайтесь, чи є span MatchingAgent. Якщо він містить:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
передача відсутня або зламана.

**Виправлення:** Переконайтеся, що `RESUME_PARSER_INSTRUCTIONS` у `main.py` містить розділ `[JOB DESCRIPTION PASS-THROUGH]` і правило:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Також переконайтеся, що `JOB_DESCRIPTION_INSTRUCTIONS` містить правило ретрансляції `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Якщо будь-який блок інструкцій є шаблоном із «майстра» встановлення, замініть його на повну версію з [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent виводить «Cannot compute fit score - no JD provided»

Це та сама коренева причина, що й вище. MatchingAgent отримав вивід JD Agent, але розділ `[PARSED RESUME PASS-THROUGH]` був відсутній або порожній, тому порівняти два профілі він не зміг. Переконайтеся:
1. `JOB_DESCRIPTION_INSTRUCTIONS` містить правило ретрансляції: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` вказує агенту шукати розділи `[JD REQUIREMENTS]` і `[PARSED RESUME PASS-THROUGH]`.

Замініть обидва блоки інструкцій повними версіями з [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Відповідь з’являється двічі

**Симптом:** Вивід GapAnalyzer (або весь вивід конвеєра) з’являється двічі у відповіді Agent Inspector.

**Причина:** `WorkflowBuilder` використовує OR-семантику для вхідних ребер — наступний виконавець запускається відразу, як виконується будь-який із попередників. Якщо `matching_executor` має два вхідні ребра (одне від `resume_executor`, інше від `jd_executor`), він запускається двічі: коли закінчується ResumeParser і коли закінчується JD Agent. GapAnalyzer теж запускається двічі.

**Виправлення:** Забезпечте, що граф `WorkflowBuilder` є строго послідовним конвеєром без «входів з кількох вершин»:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # НЕ з resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Якщо у вас є зайвий рядок `.add_edge(resume_executor, matching_executor)`, видаліть його. Ретрансляція `[PARSED RESUME PASS-THROUGH]` у виводі JD Agent вже дає доступ MatchingAgent до резюме.

---

## Проблеми з оточенням і конфігурацією

### Відсутні або неправильні значення у файлі `.env`

Файл `.env` має розміщуватися у каталозі `PersonalCareerCopilot/` (на тому ж рівні, що і `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Очікуваний вміст `.env`:

**Шлях A - хмарна Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Шлях B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Обидва шляхи використовують `FOUNDRY_PROJECT_ENDPOINT`. Значення різняться: хмара використовує `https://` Foundry endpoint; локально використовується `http://localhost:5273/v1`. Запустіть `foundry model list`, щоб підтвердити точний псевдонім моделі для Шляху B.

> **Як дізнатися `FOUNDRY_PROJECT_ENDPOINT`:**
- Відкрийте панель **Foundry Toolkit** у VS Code → правою кнопкою миші клікніть по проєкту → **Copy Project Endpoint**.
- Або зайдіть у [Azure Portal](https://portal.azure.com) → ваш проєкт Foundry → **Overview** → **Project endpoint**.

> **Як дізнатися `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** У панелі Foundry Toolkit розгорніть проєкт → **Models** → знайдіть ім’я розгорнутої моделі (наприклад, `gpt-4.1-mini`).

### Пріоритет змінних оточення

`main.py` використовує `load_dotenv(override=True)`, що означає:

| Пріоритет | Джерело | Виграє, якщо встановлені обидва? |
|----------|--------|-------------------------------|
| 1 (найвищий) | файл `.env` | Так |
| 2 | Змінна оточення оболонки / контейнера | Використовується, якщо такого ключа немає у `.env` |

У локальній розробці це робить `.env` джерелом істини (редагування `.env` відразу впливає на запуск). При розгортанні в хмарі Foundry впроваджує змінні оточення на рівні контейнера; оскільки `.env` не є частиною розгорнутого образу для цієї лабораторної установки, використовуються впроваджені у контейнер значення.

---

## Сумісність версій

### Матриця версій пакетів

Багатогентний робочий процес вимагає певних версій пакетів. Невідповідність версій спричиняє помилки під час виконання.

| Пакет | Вимагана версія | Команда перевірки |
|---------|-----------------|------------------|
| `agent-framework-foundry` | остання | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | остання | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | остання | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Поширені помилки версій

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Виправлення: перевстановити agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Виправлення: оновлення пакету mcp
pip install mcp --upgrade
```

### Перевірка версій одразу

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Очікуваний вивід:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Проблеми з розгортанням

### Контейнер не запускається після розгортання

1. **Перевірте логи контейнера:**
   - Відкрийте панель Foundry Toolkit → розгорніть **Hosted Agents (Preview)** → натисніть вашого агента → розгорніть версію → **Container Details** → **Logs**.
   - Шукайте трасування стека Python або помилки відсутності модулів.

2. **Поширені причини непуску контейнера:**

   | Помилка в логах | Причина | Виправлення |
   |-----------------|--------|------------|
   | `ModuleNotFoundError` | У `requirements.txt` відсутній пакет | Додайте пакет, повторно розгорніть |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Змінні оточення у `agent.yaml` або `.env` не встановлені | Оновіть секцію `environment_variables` у `agent.yaml` (хостинг) або `.env` (локально) |
   | `azure.identity.CredentialUnavailableError` | Менеджована ідентичність не налаштована | Foundry налаштовує це автоматично — переконайтеся, що розгортаєтесь через розширення |
   | `OSError: port 8088 already in use` | Dockerfile відкриває неправильний порт або конфлікт портів | Перевірте `EXPOSE 8088` у Dockerfile і `CMD ["python", "main.py"]` |
   | Контейнер завершується з кодом 1 | Необроблена виключна ситуація у `main()` | Спочатку протестуйте локально ([Модуль 5](05-test-locally.md)), щоб вловити помилки до розгортання |

3. **Повторне розгортання після виправлення:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → виберіть того ж агента → розгорніть нову версію.

### Розгортання триває занадто довго

Контейнери багатогентного робочого процесу запускаються довше, бо при старті створюють 4 екземпляри агента. Звичайний час запуску:

| Етап | Очікувана тривалість |
|-------|---------------------|
| Збірка образу контейнера | 1-3 хвилини |
| Відправка образу в ACR | 30-60 секунд |
| Запуск контейнера (один агент) | 15-30 секунд |
| Запуск контейнера (багатогентний) | 30-120 секунд |
| Агент доступний у Playground | 1-2 хвилини після статусу «Started» |

> Якщо статус «Pending» триває більше 5 хвилин, перевірте логи контейнера на помилки.

---

## Проблеми RBAC та дозволів

### `403 Forbidden` або `AuthorizationFailed`

Вам потрібна роль **[Foundry User](https://aka.ms/foundry-ext-project-role)** у вашому проєкті Foundry (раніше називалася **Azure AI User** – ID ролі незмінний):

1. Перейдіть до [Azure Portal](https://portal.azure.com) → ресурс вашого проєкту Foundry.
2. Натисніть **Access control (IAM)** → **Role assignments**.
3. Знайдіть своє ім’я → переконайтеся, що є роль **Foundry User** (або застаріла **Azure AI User**).
4. Якщо відсутня: **Додати** → **Add role assignment** → знайдіть **Foundry User** → призначте на свій аккаунт.

Дивіться документацію [RBAC для Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) для деталей.

### Модель розгортання недоступна

Якщо агент повертає помилки, пов’язані з моделлю:

1. Перевірте, що модель розгорнута: панель Foundry → розгорніть проєкт → **Models** → перевірте, чи є `gpt-4.1-mini` (або ваша модель) зі статусом **Succeeded**.
2. Переконайтеся, що ім’я розгортання співпадає: порівняйте `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` (або `agent.yaml`) з фактичним іменем розгортання у панелі.
3. Якщо розгортання минуло (безплатний рівень): повторно розгорніть з [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Проблеми Foundry Local (Шлях B)

### Сервіс Foundry Local не запущений

```powershell
# Перевірити статус
foundry local status

# Запустити службу, якщо вона зупинена
foundry local start
```

| Симптом | Причина | Виправлення |
|---------|--------|------------|
| Health check повертає `503` | Сервіс не запущено | `foundry local start` або натисніть **Start** у панелі Foundry Toolkit |
| Health check вичерпав час очікування | Модель все ще завантажується | Почекайте 30–60 с після старту; великі моделі завантажуються довше |
| `StatusCode: 404` на `/v1/health` | Неправильний порт | Стандартний порт `5273`. Перевірте `foundry local status` для фактичного порту |
| Недостатньо ресурсів | Foundry Local потребує ~4 ГБ вільної оперативної пам’яті | Закрийте інші додатки |
| Завантаження моделі не вдається | Низько місця на диску | Моделі мають розмір 2–8 ГБ. Звільніть місце, потім `foundry model pull <name>` |

### Несумісність імені моделі

```powershell
# Список завантажених моделей та їх точних псевдонімів
foundry model list
```

Встановіть `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` точно таким, як відображено (наприклад, `phi-4-mini`, а не `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` при локальному запуску (Шлях B)

У `main.py` лабораторії використовується `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local вимагає, щоб ця змінна вказувала на локальний сервіс — **не** `AZURE_AI_PROJECT_ENDPOINT`. Переконайтеся, що у вашому `.env` є:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Інструмент MCP все ще робить зовнішній виклик (Шлях B)

Це очікувано. Інструмент `search_microsoft_learn_for_plan` отримує навчальні ресурси з `https://learn.microsoft.com/api/mcp`. **Лише запит назви навички** передається мережею — резюме та текст JD повністю опрацьовуються на вашому пристрої й ніколи не передаються. Якщо потрібна повністю офлайн-робота, додайте у інструмент `try/except` із запасним варіантом, який повертає статичну URL `learn.microsoft.com`, коли endpoint недоступний.

---

## Отримання допомоги

Якщо ви застрягли після спроб вищенаведених виправлень:

1. **Перевірте логи сервера** — більшість помилок породжують трасування стека Python у терміналі. Уважно прочитайте повний трасбек.
2. **Пошукайте повідомлення про помилку** — скопіюйте текст помилки і пошукайте на [Microsoft Q&A для Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Відкрийте issue** — створіть issue у [репозиторії майстер-класу](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) з:
   - текстом або скріншотом помилки
   - версіями пакетів (`pip list | Select-String "agent-framework"`)
   - вашою версією Python (`python --version`)
   - інформацією, чи помилка локальна чи після розгортання

---

### Контрольний список

- [ ] Ви знаєте, як перевірити та виправити проблеми конфігурації `.env`
- [ ] Ви можете перевірити, що версії пакетів відповідають вимогам
- [ ] Ви знаєте, як перевіряти логи контейнера при збоях розгортання
- [ ] Ви можете перевіряти ролі RBAC у порталі Azure

---

**Попередній:** [07 - Verify in Playground](07-verify-in-playground.md) · **Наступний:** [09 - Summary →](09-summary.md) · **Домашня:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:
Цей документ було перекладено за допомогою сервісу штучного інтелекту для перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->