# Модуль 8 - Устранение неполадок (Мультиагент)

В этом модуле рассматриваются распространённые ошибки, исправления и стратегии отладки, специфичные для мультиагентного рабочего процесса. Для общих проблем с развертыванием Foundry также обратитесь к [руководству по устранению неполадок Лаба 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Быстрая справка: Ошибка → Исправление

| Ошибка / Симптом | Возможная причина | Исправление |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Файл `.env` отсутствует или значения не заданы | Создайте `.env` с `PROJECT_ENDPOINT=<your-endpoint>` и `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Виртуальное окружение не активировано или зависимости не установлены | Выполните `.\.venv\Scripts\Activate.ps1` затем `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Пакет MCP не установлен (отсутствует в requirements) | Выполните `pip install mcp` или проверьте, что `requirements.txt` включает его как транзитивную зависимость |
| Агент запускается, но возвращает пустой ответ | Несовпадение `output_executors` или отсутствуют ребра | Проверьте `output_executors=[gap_analyzer]` и что все ребра существуют в `create_workflow()` |
| Только 1 карточка gap (остальные отсутствуют) | Инструкции GapAnalyzer неполные | Добавьте параграф `CRITICAL:` в `GAP_ANALYZER_INSTRUCTIONS` - см. [Модуль 3](03-configure-agents.md) |
| Оценка соответствия равна 0 или отсутствует | MatchingAgent не получил данные с предыдущего шага | Проверьте, что существуют оба `add_edge(resume_parser, matching_agent)` и `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Сервер MCP отклонил вызов инструмента | Проверьте подключение к интернету. Попробуйте открыть `https://learn.microsoft.com/api/mcp` в браузере. Повторите попытку |
| В выводе нет ссылок Microsoft Learn | Инструмент MCP не зарегистрирован или неправильный endpoint | Проверьте `tools=[search_microsoft_learn_for_plan]` у GapAnalyzer и правильность `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | Другой процесс использует порт 8088 | Выполните `netstat -ano \| findstr :8088` (Windows) или `lsof -i :8088` (macOS/Linux) и остановите конфликтующий процесс |
| `Address already in use: port 5679` | Конфликт порта Debugpy | Остановите другие сессии отладки. Выполните `netstat -ano \| findstr :5679`, чтобы найти и завершить процесс |
| Инспектор агента не открывается | Сервер ещё не полностью запущен или конфликт портов | Дождитесь лог "Server running". Проверьте свободен ли порт 5679 |
| `azure.identity.CredentialUnavailableError` | Не выполнен вход в Azure CLI | Выполните `az login`, затем перезапустите сервер |
| `azure.core.exceptions.ResourceNotFoundError` | Развертывание модели отсутствует | Проверьте, что `MODEL_DEPLOYMENT_NAME` совпадает с развернутой моделью в вашем проекте Foundry |
| Статус контейнера "Failed" после развертывания | Сбой контейнера при запуске | Проверьте логи контейнера в панели Foundry. Часто: отсутствует переменная окружения или ошибка импорта |
| Развертывание показывает "Pending" более 5 минут | Контейнер слишком долго запускается или ограничены ресурсы | Подождите до 5 минут для мультиагента (создаёт 4 экземпляра агента). Если всё ещё в ожидании - проверьте логи |
| `ValueError` из `WorkflowBuilder` | Некорректная конфигурация графа | Убедитесь, что `start_executor` задан, `output_executors` — список, и отсутствуют циклические ребра |

---

## Проблемы с окружением и конфигурацией

### Отсутствующие или неверные значения в `.env`

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

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Как найти ваш PROJECT_ENDPOINT:** 
- Откройте панель **Microsoft Foundry** в VS Code → кликните правой кнопкой по проекту → **Copy Project Endpoint**. 
- Либо перейдите в [Azure Portal](https://portal.azure.com) → ваш проект Foundry → **Overview** → **Project endpoint**.

> **Как найти MODEL_DEPLOYMENT_NAME:** В боковой панели Foundry раскройте проект → **Models** → найдите имя вашей развернутой модели (например, `gpt-4.1-mini`).

### Приоритет переменных окружения

`main.py` использует `load_dotenv(override=False)`, что означает:

| Приоритет | Источник | Побеждает если оба заданы? |
|----------|--------|------------------------|
| 1 (высший) | Переменная среды оболочки | Да |
| 2 | Файл `.env` | Только если переменная среды не задана |

Это означает, что переменные среды Foundry во время хостинга (задаваемые через `agent.yaml`) имеют приоритет над значениями из `.env`.

---

## Совместимость версий

### Матрица версий пакетов

Для мультиагентного рабочего процесса требуются конкретные версии пакетов. Несовпадение версий вызывает ошибки времени выполнения.

| Пакет | Требуемая версия | Команда проверки |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | последняя предварительная версия | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Частые ошибки версий

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Исправлено: обновление до rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` не найден или несовместимость Inspector:**

```powershell
# Исправление: установка с флагом --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Исправлено: обновление пакета mcp
pip install mcp --upgrade
```

### Проверить все версии сразу

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Ожидаемый вывод:

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

## Проблемы с инструментом MCP

### MCP-инструмент не возвращает результаты

**Симптом:** Карточки gap показывают "No results returned from Microsoft Learn MCP" или "No direct Microsoft Learn results found".

**Возможные причины:**

1. **Проблемы с сетью** — не удаётся достучаться до MCP endpoint (`https://learn.microsoft.com/api/mcp`).
   ```powershell
   # Проверка соединения
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Если возвращается `200`, endpoint доступен.

2. **Слишком специфичный запрос** — название навыка слишком узкоспециализировано для поиска Microsoft Learn.
   - Это ожидаемо для очень специализированных навыков. Инструмент возвращает fallback URL в ответе.

3. **Тайм-аут сессии MCP** — востанавливаемое HTTP соединение истекло.
   - Повторите запрос. Сессии MCP эфемерны и могут требовать переподключения.

### Объяснение логов MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Лог | Значение | Действие |
|-----|---------|--------|
| `GET → 405` | MCP клиент проверяется во время инициализации | Нормально - игнорировать |
| `POST → 200` | Вызов инструмента успешен | Ожидаемо |
| `DELETE → 405` | MCP клиент проверяется во время очистки | Нормально - игнорировать |
| `POST → 400` | Некорректный запрос (неправильный query) | Проверьте параметр `query` в `search_microsoft_learn_for_plan()` |
| `POST → 429` | Ограничение по частоте | Подождите и повторите. Уменьшите параметр `max_results` |
| `POST → 500` | Ошибка сервера MCP | Временная. Если повторяется — возможно MCP API Microsoft Learn недоступен |
| Тайм-аут соединения | Сеть или сервер MCP недоступен | Проверьте интернет. Попробуйте `curl https://learn.microsoft.com/api/mcp` |

---

## Проблемы с развертыванием

### Контейнер не запускается после развертывания

1. **Проверьте логи контейнера:**
   - Откройте боковую панель **Microsoft Foundry** → раскройте **Hosted Agents (Preview)** → кликните по вашему агенту → раскройте версию → **Container Details** → **Logs**.
   - Ищите трассировки стека Python или ошибки отсутствующих модулей.

2. **Распространённые причины сбоев запуска контейнера:**

   | Ошибка в логах | Причина | Исправление |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | В `requirements.txt` отсутствует пакет | Добавьте пакет, разверните заново |
   | `RuntimeError: Missing required environment variable` | Переменные окружения в `agent.yaml` не заданы | Обновите секцию `environment_variables` в `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Управляемая учётная запись не настроена | Foundry настраивает автоматически - убедитесь, что развертываете через расширение |
   | `OSError: port 8088 already in use` | Dockerfile указывает неправильный порт или конфликт портов | Проверьте `EXPOSE 8088` в Dockerfile и команду `CMD ["python", "main.py"]` |
   | Контейнер завершился с кодом 1 | Необработанное исключение в `main()` | Сначала протестируйте локально ([Модуль 5](05-test-locally.md)), чтобы поймать ошибки до развертывания |

3. **Повторное развертывание после исправлений:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → выберите того же агента → разверните новую версию.

### Развертывание длится слишком долго

Контейнеры мультиагента запускаются дольше, так как создают 4 экземпляра агента при старте. Типичные времена запуска:

| Этап | Ожидаемая длительность |
|-------|------------------|
| Сборка образа контейнера | 1-3 минуты |
| Загрузка образа в ACR | 30-60 секунд |
| Запуск контейнера (один агент) | 15-30 секунд |
| Запуск контейнера (мультиагент) | 30-120 секунд |
| Агент доступен в Playground | 1-2 минуты после "Started" |

> Если статус "Pending" длится более 5 минут, проверьте логи контейнера на наличие ошибок.

---

## Проблемы с RBAC и разрешениями

### `403 Forbidden` или `AuthorizationFailed`

Вам нужна роль **[Azure AI User](https://aka.ms/foundry-ext-project-role)** в вашем проекте Foundry:

1. Перейдите в [Azure Portal](https://portal.azure.com) → ресурс вашего проекта Foundry.
2. Выберите **Access control (IAM)** → **Role assignments**.
3. Найдите своё имя → убедитесь, что есть роль **Azure AI User**.
4. Если отсутствует: нажмите **Add** → **Add role assignment** → найдите **Azure AI User** → назначьте своей учетной записи.

Подробности смотрите в документации [RBAC для Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Недоступность развертывания модели

Если агент возвращает ошибки, связанные с моделью:

1. Проверьте, что модель развернута: в боковой панели Foundry раскройте проект → **Models** → найдите `gpt-4.1-mini` (или вашу модель) со статусом **Succeeded**.
2. Проверьте, что имя развертывания совпадает: сравните `MODEL_DEPLOYMENT_NAME` в `.env` (или `agent.yaml`) с фактическим именем развертывания в боковой панели.
3. Если срок действия развертывания истёк (бесплатный тариф): разверните заново через [Каталог моделей](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Проблемы с Agent Inspector

### Inspector открывается, но показывает "Disconnected"

1. Убедитесь, что сервер запущен: проверьте в терминале строку "Server running on http://localhost:8088".
2. Проверьте порт `5679`: Inspector подключается через debugpy по порту 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Перезапустите сервер и откройте Inspector заново.

### Inspector показывает неполный ответ

Ответы мультиагента длинные и передаются по частям. Дождитесь полного окончания ответа (может занять 30-60 секунд в зависимости от количества gap карт и вызовов MCP).

Если ответ постоянно обрезается:
- Проверьте, что в инструкциях GapAnalyzer есть блок `CRITICAL:`, который предотвращает объединение gap карт.
- Проверьте лимит токенов вашей модели — `gpt-4.1-mini` поддерживает до 32К выходных токенов, чего должно быть достаточно.

---

## Советы по производительности

### Медленные ответы

Мультиагентные рабочие процессы изначально медленнее одиночных из-за последовательных зависимостей и вызовов инструмента MCP.

| Оптимизация | Как | Влияние |
|-------------|-----|--------|
| Уменьшить количество вызовов MCP | Снизить параметр `max_results` в инструменте | Меньше HTTP запросов |
| Упростить инструкции | Более короткие, сфокусированные подсказки агента | Быстрее вывод модели |
| Использовать `gpt-4.1-mini` | Быстрее, чем `gpt-4.1` для разработки | Приблизительно в 2 раза быстрее |
| Уменьшить детализацию gap карт | Упростить формат gap карт в инструкциях GapAnalyzer | Меньше объема вывода |

### Типичные времена отклика (локально)

| Конфигурация | Ожидаемое время |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap карт | 30-60 секунд |
| `gpt-4.1-mini`, 8+ gap карт | 60-120 секунд |
| `gpt-4.1`, 3-5 gap карт | 60-120 секунд |
---

## Получение помощи

Если вы застряли после попыток исправить ошибки, указанные выше:

1. **Проверьте логи сервера** - Большинство ошибок выводят трассировку стека Python в терминале. Прочитайте полный traceback.
2. **Ищите сообщение об ошибке** - Скопируйте текст ошибки и выполните поиск в [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Откройте issue** - Создайте issue в [репозитории мастерской](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues), указав:
   - Сообщение об ошибке или скриншот
   - Версии ваших пакетов (`pip list | Select-String "agent-framework"`)
   - Версию Python (`python --version`)
   - Является ли проблема локальной или после развертывания

---

### Контрольный список

- [ ] Вы можете определить и исправить наиболее распространённые ошибки многозадачных агентов, используя таблицу быстрого доступа
- [ ] Вы умеете проверять и исправлять проблемы конфигурации `.env`
- [ ] Вы можете проверить, что версии пакетов соответствуют требуемой матрице
- [ ] Вы понимаете записи логов MCP и можете диагностировать сбои инструментов
- [ ] Вы знаете, как проверять логи контейнеров при сбоях развертывания
- [ ] Вы можете проверить роли RBAC в Azure Portal

---

**Назад:** [07 - Verify in Playground](07-verify-in-playground.md) · **Домой:** [Lab 02 README](../README.md) · [Главная мастерская](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:  
Этот документ был переведен с использованием сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия обеспечить точность, имейте в виду, что автоматические переводы могут содержать ошибки или неточности. Оригинальный документ на его родном языке следует считать официальным источником. Для критически важной информации рекомендуется обращаться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования данного перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->