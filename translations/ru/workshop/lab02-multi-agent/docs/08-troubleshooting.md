# Модуль 8 – Устранение неполадок

В этом модуле рассматриваются распространенные ошибки, исправления и стратегии отладки, специфичные для многопользовательского рабочего процесса.

## Проблемы с выводом агента

### GapAnalyzer говорит: «У меня все еще нет соответствующего отчета»

**Симптом:** Ответ GapAnalyzer просит вас вставить отчет о соответствии с пунктами «Отсутствующие навыки» и «Пробелы в сертификации». Это происходит даже если вы отправили и резюме, и описание вакансии.

**Причина:** Текст JD не был передан дальше агенту JD. С `context_mode="last_agent"`, `resume_executor` — единственный исполнитель, который когда-либо видит исходное сообщение пользователя. Если `RESUME_PARSER_INSTRUCTIONS` не включает текст JD в свой вывод, агент JD не получает JD для анализа, MatchingAgent не может вычислить коэффициент соответствия, а GapAnalyzer получает бессмысленный ввод.

**Диагностика:**

В журналах сервера найдите спан MatchingAgent. Если он содержит:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
прохождение отсутствует или нарушено.

**Исправление:** Подтвердите, что `RESUME_PARSER_INSTRUCTIONS` в `main.py` содержит раздел `[JOB DESCRIPTION PASS-THROUGH]` и правило:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Также подтвердите, что `JOB_DESCRIPTION_INSTRUCTIONS` содержит правило ретрансляции `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Если один из этих блоков инструкций является заглушкой от мастера каркаса, замените его полной версией из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent выводит «Невозможно вычислить коэффициент соответствия – JD не предоставлен»

Это та же основная причина, что и выше. MatchingAgent получил вывод JD Agent, но секция `[PARSED RESUME PASS-THROUGH]` отсутствовала или была пустой, поэтому он не мог сравнить два профиля. Подтвердите:
1. `JOB_DESCRIPTION_INSTRUCTIONS` включает правило ретрансляции: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` указывает агенту искать секции `[JD REQUIREMENTS]` и `[PARSED RESUME PASS-THROUGH]`.

Замените оба блока инструкций полными версиями из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Ответ появляется дважды

**Симптом:** Вывод GapAnalyzer (или весь вывод конвейера) появляется дважды в ответе Agent Inspector.

**Причина:** `WorkflowBuilder` использует ИЛИ-семантику для входящих рёбер — нижестоящий исполнитель запускается, как только **любой** предшественник завершится. Если `matching_executor` имеет два входящих ребра (одно от `resume_executor` и одно от `jd_executor`), он срабатывает дважды: один раз, когда ResumeParser заканчивается, и второй — когда JD Agent заканчивается. GapAnalyzer тогда также запускается дважды.

**Решение:** Убедитесь, что граф `WorkflowBuilder` является строго последовательным конвейером без слияния:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Если у вас есть лишняя строка `.add_edge(resume_executor, matching_executor)`, удалите её. Ретрансляция `[PARSED RESUME PASS-THROUGH]` в выводе JD Agent уже даёт доступ MatchingAgent к резюме.

---

## Проблемы с окружением и конфигурацией

### Отсутствующие или неверные значения `.env`

Файл `.env` должен находиться в каталоге `PersonalCareerCopilot/` (на том же уровне, что и `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Ожидаемый контент `.env`:

**Путь A - оболочка Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Путь B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Оба пути используют `FOUNDRY_PROJECT_ENDPOINT`. Значения отличаются: облачный путь использует конечную точку Foundry `https://`; локальный — `http://localhost:5273/v1`. Запустите `foundry model list`, чтобы подтвердить точный алиас модели для Пути B.

> **Поиск вашего `FOUNDRY_PROJECT_ENDPOINT`:** 
- Откройте боковую панель **Foundry Toolkit** в VS Code → щелкните правой кнопкой мыши по проекту → **Copy Project Endpoint**. 
- Или перейдите в [Azure Portal](https://portal.azure.com) → ваш проект Foundry → **Overview** → **Project endpoint**.

> **Поиск вашего `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** В боковой панели Foundry Toolkit разверните ваш проект → **Models** → найдите имя развернутой модели (например, `gpt-4.1-mini`).

### Приоритет переменных окружения

`main.py` использует `load_dotenv(override=True)`, что означает:

| Приоритет | Источник | Побеждает, если оба заданы? |
|----------|--------|------------------------------|
| 1 (самый высокий) | файл `.env` | Да |
| 2 | Переменная окружения оболочки / контейнера | Используется, если такой ключ отсутствует в `.env` |

В локальной разработке это делает `.env` единственным источником истины (редактирование `.env` сразу влияет на запуски). В размещенной среде Foundry внедряет переменные окружения на уровне контейнера; поскольку `.env` не входит в развернутый образ для этой лабораторной настройки, используются внедренные значения контейнера.

---

## Совместимость версий

### Матрица версий пакетов

Мультиагентский рабочий процесс требует определенных версий пакетов. Несоответствие версий приводит к ошибкам во время выполнения.

| Пакет | Требуемая версия | Команда проверки |
|---------|-----------------|------------------|
| `agent-framework-foundry` | последняя | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | последняя | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | последняя | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Распространённые ошибки версий

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

### Проверка всех версий одновременно

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Ожидаемый вывод:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Проблемы с развертыванием

### Контейнер не запускается после развертывания

1. **Проверьте логи контейнера:**
   - Откройте боковую панель **Foundry Toolkit** → под вашим проектом нажмите **Agents** → вкладка **Hosted Agent** → кликните по вашему агенту. Проверьте **Status** на вкладке **Details**, затем перейдите на вкладку **Playground** и используйте вкладку **Logs** в панели **Session Details**, чтобы увидеть вывод контейнера.
   - Ищите трассировки стека Python или ошибки отсутствующих модулей.

2. **Распространённые ошибки запуска контейнера:**

   | Ошибка в логах | Причина | Решение |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | отсутствует пакет `requirements.txt` | Добавьте пакет, повторно разверните |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | переменные окружения `agent.yaml` или `.env` не установлены | Обновите раздел `agent.yaml` → `environment_variables` (хостинг) или `.env` (локально) |
   | `azure.identity.CredentialUnavailableError` | Не настроена управляемая идентичность | Foundry автоматически настраивает это — убедитесь, что вы развертываете через расширение |
   | `OSError: port 8088 already in use` | Dockerfile открывает неправильный порт или конфликт портов | Проверьте `EXPOSE 8088` в Dockerfile и `CMD ["python", "main.py"]` |
   | Контейнер завершается с кодом 1 | Необработанное исключение в `main()` | Сначала протестируйте локально ([Модуль 5](05-test-locally.md)), чтобы выявить ошибки до развертывания |

3. **Повторное развертывание после исправления:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → выберите того же агента → разверните новую версию.

### Развертывание занимает слишком много времени

Контейнеры с несколькими агентами запускаются дольше, так как при старте создаются 4 экземпляра агента. Обычное время запуска:

| Этап | Ожидаемая продолжительность |
|-------|------------------|
| Сборка образа контейнера | 1-3 минуты |
| Отправка образа в ACR | 30-60 секунд |
| Запуск контейнера (одиночный агент) | 15-30 секунд |
| Запуск контейнера (мультиагент) | 30-120 секунд |
| Агент доступен в Playground | 1-2 минуты после «Started» |

> Если статус «Pending» продолжается более 5 минут, проверьте логи контейнера на наличие ошибок.

---

## Проблемы с RBAC и разрешениями

### `403 Forbidden` или `AuthorizationFailed`

Вам нужна роль **[Foundry User](https://aka.ms/foundry-ext-project-role)** в вашем проекте Foundry (ранее называлась **Azure AI User** — ID роли не изменился):

1. Перейдите на [Azure Portal](https://portal.azure.com) → ваш ресурс **проекта** Foundry.
2. Нажмите **Управление доступом (IAM)** → **Назначения ролей**.
3. Найдите свое имя → убедитесь, что указан **Foundry User** (или устаревшая метка **Azure AI User**).
4. Если отсутствует: **Добавить** → **Добавить назначение роли** → найдите **Foundry User** → назначьте своей учетной записи.

Подробности смотрите в документации [RBAC для Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Развертывание модели недоступно

Если агент возвращает ошибки, связанные с моделью:

1. Проверьте, что модель развернута: боковая панель Foundry → разверните проект → **Модели** → проверьте наличие `gpt-4.1-mini` (или вашей модели) со статусом **Succeeded**.
2. Проверьте, что имя развертывания совпадает: сравните `AZURE_AI_MODEL_DEPLOYMENT_NAME` в `.env` (или `agent.yaml`) с фактическим именем развертывания на боковой панели.
3. Если развертывание истекло (бесплатный уровень): разверните заново из [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Открыть каталог моделей**).

---

## Проблемы с Foundry Local (Путь B)

### Служба Foundry Local не работает

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Симптом | Причина | Решение |
|---------|---------|---------|
| Проверка состояния возвращает `503` | Служба не запущена | `foundry local start` или нажмите **Запустить** в боковой панели Foundry Toolkit |
| Проверка состояния завершается по тайм-ауту | Модель еще загружается | Подождите 30–60 с после запуска; большие модели загружаются дольше |
| `StatusCode: 404` на `/v1/health` | Неправильный порт | По умолчанию `5273`. Проверьте `foundry local status` для актуального порта |
| Недостаточно ресурсов | Foundry Local требует около 4 ГБ свободной оперативной памяти | Закройте другие приложения |
| Сбой загрузки модели | Мало места на диске | Модели занимают 2–8 ГБ. Освободите место, затем `foundry model pull <name>` |

### Несоответствие имени модели

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Установите `AZURE_AI_MODEL_DEPLOYMENT_NAME` в `.env` точно в соответствии с показанным псевдонимом (например, `phi-4-mini`, а не `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` при локальном запуске (Путь B)

`main.py` лаборатории использует `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local требует, чтобы эта переменная указывала на локальный сервис — **не** на `AZURE_AI_PROJECT_ENDPOINT`. Убедитесь, что ваш `.env` содержит:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP-инструмент все еще делает исходящий вызов (Путь B)

Это ожидаемо. Инструмент `search_microsoft_learn_for_plan` загружает обучающие ресурсы с `https://learn.microsoft.com/api/mcp`. **Только запрос по названию навыка** отправляется через сеть — резюме и текст JD полностью обрабатываются на вашем устройстве и никогда не передаются. Если требуется полностью автономная работа, добавьте `try/except` резервный режим в инструмент, который возвращает статичный URL `learn.microsoft.com`, если конечная точка недоступна.

---

## Получение помощи

Если вы зашли в тупик после попыток исправления выше:

1. **Проверьте логи сервера** — Большинство ошибок сопровождаются трассировкой стека Python в терминале. Прочитайте полный traceback.
2. **Поиск сообщения об ошибке** — Скопируйте текст ошибки и выполните поиск в [Microsoft Q&A для Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Создание issue** — Создайте issue в [репозитории воркшопа](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) с указанием:
   - Сообщения об ошибке или скриншота
   - Ваших версий пакетов (`pip list | Select-String "agent-framework"`)
   - Вашей версии Python (`python --version`)
   - Уточнением: локальная ли проблема или после деплоя

---

### Контрольная точка

- [ ] Вы умеете проверять и исправлять проблемы с конфигурацией `.env`
- [ ] Вы можете проверить соответствие версий пакетов требуемой матрице
- [ ] Вы знаете, как проверять логи контейнеров на предмет сбоев при деплое
- [ ] Вы можете проверить роли RBAC в Azure Portal

---

**Предыдущая:** [07 - Проверка в Playground](07-verify-in-playground.md) · **Следующая:** [09 - Итоги →](09-summary.md) · **Главная:** [Lab 02 README](../README.md) · [Главная воркшопа](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->