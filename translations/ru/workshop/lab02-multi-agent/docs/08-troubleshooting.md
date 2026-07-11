# Модуль 8 - Устранение неисправностей

В этом модуле рассматриваются распространённые ошибки, способы их исправления и стратегии отладки, специфичные для многоагентного рабочего процесса.

## Проблемы с выводом агента

### GapAnalyzer говорит «У меня всё ещё нет отчёта сопоставления»

**Симптом:** Ответ GapAnalyzer предлагает вставить отчёт сопоставления с «Отсутствующими навыками» и «Пробелами в сертификации». Это происходит даже если вы отправили и резюме, и описание вакансии.

**Причина:** Текст описания вакансии не был передан дальше агенту JD. При `context_mode="last_agent"` только `resume_executor` видит исходное сообщение пользователя. Если `RESUME_PARSER_INSTRUCTIONS` не включает текст описания вакансии в свой вывод, агент JD не имеет описания вакансии для обработки, MatchingAgent не может вычислить коэффициент соответствия, а GapAnalyzer получает бессмысленный ввод.

**Диагностика:**

В логах сервера найдите спэн MatchingAgent. Если он содержит:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
передача отсутствует или нарушена.

**Исправление:** Убедитесь, что `RESUME_PARSER_INSTRUCTIONS` в `main.py` содержит раздел `[JOB DESCRIPTION PASS-THROUGH]` и правило:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Также подтвердите, что `JOB_DESCRIPTION_INSTRUCTIONS` содержит правило передачи `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Если один из блоков инструкций является заглушкой из мастера создания, замените его полной версией из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent выводит «Cannot compute fit score - no JD provided»

Это та же корневая причина, что и выше. MatchingAgent получил вывод агента JD, но секция `[PARSED RESUME PASS-THROUGH]` отсутствовала или была пустой, поэтому он не смог сравнить два профиля. Проверьте:
1. `JOB_DESCRIPTION_INSTRUCTIONS` включает правило передачи: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` указывает агенту искать секции `[JD REQUIREMENTS]` и `[PARSED RESUME PASS-THROUGH]`.

Замените оба блока инструкций на полные версии из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Ответ повторяется дважды

**Симптом:** Вывод GapAnalyzer (или весь вывод пайплайна) появляется дважды в ответе инспектора агента.

**Причина:** `WorkflowBuilder` использует OR-семантику для входящих рёбер — потомственный исполнитель запускается, как только любой из предшественников завершится. Если у `matching_executor` есть два исходящих ребра (одно от `resume_executor` и одно от `jd_executor`), он запускается дважды: один раз после завершения ResumeParser и второй раз после агента JD. Следовательно, GapAnalyzer также запускается дважды.

**Исправление:** Убедитесь, что граф `WorkflowBuilder` — строго последовательный пайплайн без слияния входящих:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # НЕ из resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Если у вас есть лишняя строка `.add_edge(resume_executor, matching_executor)`, удалите её. Релей `[PARSED RESUME PASS-THROUGH]` в выводе агента JD уже предоставляет MatchingAgent доступ к резюме.

---

## Проблемы с окружением и конфигурацией

### Отсутствуют или неправильны значения в `.env`

Файл `.env` должен находиться в каталоге `PersonalCareerCopilot/` (на том же уровне, что и `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Ожидаемое содержимое `.env`:

**Путь A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Путь B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Оба пути используют `FOUNDRY_PROJECT_ENDPOINT`. Значение отличается: облако использует конечную точку Foundry с `https://`; локально используется `http://localhost:5273/v1`. Запустите `foundry model list`, чтобы подтвердить точный псевдоним модели для Пути B.

> **Как найти ваш `FOUNDRY_PROJECT_ENDPOINT`:** 
- Откройте боковую панель **Foundry Toolkit** в VS Code → кликните правой кнопкой по вашему проекту → **Copy Project Endpoint**. 
- Или перейдите в [Azure Portal](https://portal.azure.com) → ваш проект Foundry → **Обзор** → **Project endpoint**.

> **Как найти `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** В боковой панели Foundry Toolkit раскройте ваш проект → **Models** → найдите имя развернутой модели (например, `gpt-4.1-mini`).

### Приоритет переменных окружения

`main.py` использует `load_dotenv(override=True)`, что означает:

| Приоритет | Источник | Побеждает, если оба заданы? |
|----------|--------|------------------------|
| 1 (высший) | файл `.env` | Да |
| 2 | Переменная среды оболочки / контейнера | Используется если того же ключа в `.env` нет |

В локальной разработке это делает `.env` источником истины (редактирование `.env` немедленно влияет на запуски). В размещённой среде Foundry внедряет переменные окружения на уровне контейнера; поскольку `.env` не входит в состав образа для этой лабораторной установки, используются внедрённые значения контейнера.

---

## Совместимость версий

### Матрица версий пакетов

Многоагентный рабочий процесс требует конкретных версий пакетов. Несовпадающие версии вызывают ошибки во время выполнения.

| Пакет | Требуемая версия | Команда проверки |
|---------|-----------------|---------------|
| `agent-framework-foundry` | последняя | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | последняя | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | последняя | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Частые ошибки версий

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Исправление: переустановить agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Исправить: обновить пакет mcp
pip install mcp --upgrade
```

### Проверить все версии одним махом

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
   - Откройте боковую панель **Foundry Toolkit** → раскройте **Hosted Agents (Preview)** → выберите вашего агента → раскройте версию → **Container Details** → **Logs**.
   - Ищите трассировки стека Python или ошибки отсутствующих модулей.

2. **Типичные ошибки запуска контейнера:**

   | Ошибка в логах | Причина | Исправление |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Отсутствует пакет в `requirements.txt` | Добавьте пакет, задеплойте повторно |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Переменные окружения в `agent.yaml` или `.env` не заданы | Обновите раздел `environment_variables` в `agent.yaml` (хостинг) или `.env` (локально) |
   | `azure.identity.CredentialUnavailableError` | Управляемая учётная запись не настроена | Foundry настраивает автоматически — убедитесь, что развертываете через расширение |
   | `OSError: port 8088 already in use` | Dockerfile указывает неправильный порт или конфликт портов | Проверьте `EXPOSE 8088` в Dockerfile и `CMD ["python", "main.py"]` |
   | Контейнер завершается с кодом 1 | Необработанное исключение в `main()` | Сначала протестируйте локально ([Модуль 5](05-test-locally.md)), чтобы поймать ошибки до развертывания |

3. **Заново разверните после исправления:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → выберите того же агента → разверните новую версию.

### Развертывание занимает слишком много времени

Многоагентные контейнеры запускаются дольше, потому что при старте создают 4 экземпляра агента. Обычно время запуска:

| Этап | Ожидаемая продолжительность |
|-------|------------------|
| Сборка образа контейнера | 1-3 минуты |
| Отправка образа в ACR | 30-60 секунд |
| Запуск контейнера (один агент) | 15-30 секунд |
| Запуск контейнера (многоагентный) | 30-120 секунд |
| Агент доступен в Playground | 1-2 минуты после «Started» |

> Если статус «Pending» сохраняется более 5 минут, проверьте логи контейнера на ошибки.

---

## Проблемы с RBAC и разрешениями

### `403 Forbidden` или `AuthorizationFailed`

Вам нужна роль **[Foundry User](https://aka.ms/foundry-ext-project-role)** в вашем проекте Foundry (ранее называлась **Azure AI User** — ID роли не изменён):

1. Перейдите в [Azure Portal](https://portal.azure.com) → ваш ресурс **проект** Foundry.
2. Нажмите **Управление доступом (IAM)** → **Назначения ролей**.
3. Найдите своё имя → убедитесь, что указана роль **Foundry User** (или устаревшая метка **Azure AI User**).
4. Если отсутствует: **Добавить** → **Добавить назначение роли** → найдите **Foundry User** → назначьте аккаунту.

Подробнее смотрите в документации [RBAC для Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Развернутая модель недоступна

Если агент возвращает ошибки, связанные с моделью:

1. Проверьте, что модель развернута: боковая панель Foundry → раскройте проект → **Models** → проверьте наличие `gpt-4.1-mini` (или вашей модели) со статусом **Succeeded**.
2. Проверьте соответствие имени развертывания: сравните `AZURE_AI_MODEL_DEPLOYMENT_NAME` в `.env` (или `agent.yaml`) с фактическим именем развертывания в боковой панели.
3. Если развертывание истекло (бесплатный тариф): разверните заново из [Каталога моделей](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Проблемы Foundry Local (Путь B)

### Сервис Foundry Local не запущен

```powershell
# Проверить статус
foundry local status

# Запустить службу, если она остановлена
foundry local start
```

| Симптом | Причина | Исправление |
|---------|-------|-----|
| Проверка работоспособности возвращает `503` | Сервис не запущен | `foundry local start` или нажмите **Start** в боковой панели Foundry Toolkit |
| Проверка работоспособности таймаутится | Модель ещё загружается | Подождите 30–60 с после запуска; большие модели загружаются дольше |
| `StatusCode: 404` на `/v1/health` | Неправильный порт | По умолчанию `5273`. Проверьте фактический порт с помощью `foundry local status` |
| Недостаточно ресурсов | Foundry Local требует ~4 ГБ свободной ОЗУ | Закройте другие приложения |
| Не удалось скачать модель | Недостаточно места на диске | Модели весят 2–8 ГБ. Освободите место, затем `foundry model pull <name>` |

### Несовпадение имени модели

```powershell
# Список загруженных моделей и их точных псевдонимов
foundry model list
```

Установите `AZURE_AI_MODEL_DEPLOYMENT_NAME` в `.env` точно в соответствии с показанным псевдонимом (например, `phi-4-mini`, не `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` при локальном запуске (Путь B)

В lab `main.py` использует `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local ожидает, что эта переменная укажет на локальный сервис — **не** `AZURE_AI_PROJECT_ENDPOINT`. Убедитесь, что в вашем `.env` есть:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Инструмент MCP всё ещё вызывает внешний запрос (Путь B)

Это ожидаемо. Инструмент `search_microsoft_learn_for_plan` получает учебные материалы с `https://learn.microsoft.com/api/mcp`. **Поисковый запрос по названию навыка** передаётся по сети — резюме и текст описания вакансии обрабатываются полностью локально и не передаются. Если требуется полностью офлайн-режим, добавьте в инструмент обработчик `try/except`, который возвращает статический URL `learn.microsoft.com`, когда конечная точка недоступна.

---

## Получение помощи

Если вы застряли после попыток исправления выше:

1. **Проверьте логи сервера** — Большинство ошибок сопровождаются трассировкой стека Python в терминале. Прочитайте полный traceback.
2. **Поиск по сообщению об ошибке** — Скопируйте текст ошибки и выполните поиск в [Microsoft Q&A для Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Откройте issue** — Создайте тикет в [репозитории мастерской](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) с:
   - Сообщением об ошибке или скриншотом
   - Версиями пакетов (`pip list | Select-String "agent-framework"`)
   - Версией Python (`python --version`)
   - Информацией, локальная ли проблема или после развертывания

---

### Контрольная точка

- [ ] Вы умеете проверять и исправлять проблемы конфигурации `.env`
- [ ] Вы можете подтвердить, что версии пакетов соответствуют требуемой матрице
- [ ] Вы знаете, как проверять логи контейнера при сбоях развертывания
- [ ] Вы умеете проверять роли RBAC в Azure Portal

---

**Предыдущий:** [07 - Проверка в Playground](07-verify-in-playground.md) · **Следующий:** [09 - Итоги →](09-summary.md) · **Домой:** [Lab 02 README](../README.md) · [Главная страница мастерской](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->