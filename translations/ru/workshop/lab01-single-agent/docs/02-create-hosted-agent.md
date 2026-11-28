# Модуль 2 - Создание нового размещённого агента

⏱️ ~5 мин

В этом модуле вы используете Foundry Toolkit для **создания проекта размещённого агента**. Каркас генерирует полную структуру проекта - `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt` и конфигурацию отладки VS Code - чтобы вы могли сосредоточиться на настройке поведения агента.

> **Ключевая идея:** Папка `agent/` в этой лабораторной работе является примером того, что генерирует Foundry Toolkit. Вам не нужно писать эти файлы с нуля.

### Поток мастера создания

```mermaid
flowchart LR
    A["Command Palette:
    Create new Hosted Agent"] --> B["Language:
    Python"]
    B --> C["Framework:
    Agent Framework"]
    C --> D["API type:
    Response API"]
    D --> E["Template:
    Basic"]
    E --> F["Workspace folder
    & agent name"]
    F --> G["Generated project"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#7B68EE,color:#fff
    style E fill:#7B68EE,color:#fff
    style F fill:#7B68EE,color:#fff
    style G fill:#27AE60,color:#fff
```

---

## Шаг 1: Откройте мастер создания размещённого агента

1. Нажмите `Ctrl+Shift+P` чтобы открыть **Палитру команд**.
2. Введите: **Foundry Toolkit: Create new Hosted Agent** и выберите его.

> **Альтернатива: Создание через Foundry Portal**
> Если предпочитаете браузер, вы можете создать проект на [https://ai.azure.com](https://ai.azure.com). После создания проекта вернитесь в VS Code и используйте боковую панель **Foundry Toolkit** для подключения к нему.

> **Альтернатива:** В боковой панели Foundry Toolkit наведите курсор на **Agents** под вашим проектом, нажмите иконку **+**, затем выберите **Create in Code With Template**.

## Шаг 2: Выберите настройки

![Создание размещённого агента из образца - вкладка деталей агента с фильтрами Язык, Фреймворк, Протокол и Шаблон](../../../../../translated_images/ru/02-hosted-agents-sample.0aabd1638936c591.webp)

1. В левой навигационной/опционной секции выберите следующее:

| Меню | Выбор | Примечания |
|--------|-----------|-------|
| **Язык** | Python | Также поддерживается C# |
| **Фреймворк** | Agent Framework | Простой старт с использованием Agent Framework SDK |
| **Тип API** | Response API | `POST /responses` - диалоговый, с управляемой платформой историей |
| **Шаблон** | Basic | Простой старт с использованием Agent Framework SDK |

2. После выбора нажмите **Далее**

![Создание размещённого агента - вкладка создания с опциями папки рабочего пространства, имени папки и настройки окружения](../../../../../translated_images/ru/02-create-hosted-agents.9f10b6a566df3053.webp)

3. В следующем окне выберите следующее:

| Меню | Выбор | Примечания |
|--------|-----------|-------|
| **Папка рабочего пространства** | Выберите целевую папку | например, `/workspace/Foundry_Toolkit_for_VSCode_Lab/` или подпапку в этом репозитории |
| **Имя агента** | Введите имя | например, `executive-summary-agent` |
| **Настройка окружения** | пропустить настройку пока |  |

Нажмите **создать** для создания нашего агента. Будет создана новая папка с именем размещённого агента.

## Шаг 3: Осмотрите сгенерированный проект

После завершения создания убедитесь, что в Проводнике (`Ctrl+Shift+E`) видны следующие файлы:

```
📂 executive-summary-agent/
├── .env                ← Environment variables (placeholders)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Agent entry point (your main code)
└── requirements.txt    ← Python dependencies
```

### Объяснение ключевых файлов

| Файл | Назначение |
|------|---------|
| `agent.yaml` | Объявляет агента как `kind: hosted`, сопоставляет переменные окружения, определяет протокол `/responses` |
| `main.py` | Создаёт `FoundryChatClient` → оборачивает в `Agent` с инструкциями → обслуживает через `ResponsesHostServer` на порту 8088 |
| `Dockerfile` | Использует `python:3.12-slim`, устанавливает зависимости, открывает порт 8088, запускает `main.py` |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp`, `debugpy` |

> **Важно:** Открывайте сгенерированную папку агента напрямую в VS Code (саму папку `agent/`), чтобы `.vscode/launch.json` и `tasks.json` правильно работали при отладке F5.

---

### ✅ Контрольная точка

- [ ] Создан проект каркаса со всеми ожидаемыми файлами
- [ ] `agent.yaml` показывает `kind: hosted` и `protocol: responses`
- [ ] `main.py` импортирует `Agent`, `FoundryChatClient`, `ResponsesHostServer`
- [ ] Папка агента открыта в VS Code как корень рабочего пространства

---

**Предыдущий:** [01 - Настройка](01-setup.md) · **Следующий:** [03 - Конфигурация и код →](03-configure-and-code.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->