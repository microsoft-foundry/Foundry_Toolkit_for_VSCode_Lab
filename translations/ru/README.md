# Foundry Toolkit + Мастерская по Hosted Agents в Foundry

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Создавайте, тестируйте и развертывайте AI-агентов в **Microsoft Foundry Agent Service** как **Hosted Agents** — полностью из VS Code с помощью **расширения Microsoft Foundry** и **Foundry Toolkit**.

> **Hosted Agents находятся на стадии предварительного просмотра.** Поддерживаемые регионы ограничены — смотрите [доступность регионов](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Папка `agent/` внутри каждой лабораторной работы **автоматически создается** расширением Foundry — вы затем настраиваете код, тестируете локально и развертываете.

### 🌐 Многоязычная поддержка

#### Поддерживается через GitHub Action (автоматизировано и всегда актуально)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](./README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Предпочитаете клонировать локально?**
>
> В этом репозитории есть более 50 переводов на разные языки, что значительно увеличивает размер загрузки. Чтобы клонировать без переводов, используйте sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Это даст вам всё необходимое для прохождения курса с гораздо более быстрой загрузкой.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Архитектура

```mermaid
flowchart TB
    subgraph Local["Локальная разработка (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "Отладка F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Создание каркаса
    Playground -- "Тестовые подсказки" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Процесс:** Расширение Foundry создает структуру агента → вы настраиваете код и инструкции → тестируете локально с Agent Inspector → развертываете в Foundry (docker-образ отправляется в ACR) → проверяете в Playground.

---

## Что вы создадите

| Лабораторная работа | Описание | Статус |
|-----|-------------|--------|
| **Лабораторная 01 - Один агент** | Создайте **агента "Объясни, как если бы я исполнительный директор"**, протестируйте локально и разверните в Foundry | ✅ Доступно |
| **Лабораторная 02 - Многоагентный рабочий процесс** | Создайте **"Оценщик соответствия резюме - оценщик соответствия вакансии"** - 4 агента работают вместе, чтобы оценить соответствие резюме и составить дорожную карту обучения | ✅ Доступно |

---

## Познакомьтесь с агентом Executive

В этой мастерской вы создадите **агента "Объясни, как если бы я исполнительный директор"** — AI-агента, который берет сложный технический жаргон и превращает его в спокойные, готовые к заседанию совета резюме. Потому что, честно говоря, никто из руководства не хочет слышать о "истощении пула потоков, вызванном синхронными вызовами, введёнными в версии 3.2".

Я создал этого агента после слишком большого количества случаев, когда мой идеально составленный отчет о проблемах встречал ответ: *"Так... сайт работает или нет?"*

### Как это работает

Вы даёте агенту техническое обновление. Он выдает резюме для руководства - три пункта, без жаргона, без стек-трейсов, без экзистенциального ужаса. Просто **что произошло**, **влияние на бизнес**, и **следующий шаг**.

### Посмотрите его в действии

**Вы говорите:**
> "Задержка API увеличилась из-за истощения пула потоков, вызванного синхронными вызовами, введёнными в версии 3.2."

**Агент отвечает:**

> **Резюме для руководства:**
> - **Что произошло:** После последнего обновления система замедлилась.
> - **Влияние на бизнес:** Некоторые пользователи столкнулись с задержками при использовании сервиса.
> - **Следующий шаг:** Изменение было отменено, готовится исправление перед повторным развертыванием.

### Зачем нужен этот агент?

Это предельно простой, целенаправленный агент — идеально подходит для изучения рабочего процесса hosted agents от начала до конца без запутывания в сложных инструментах. И, честно говоря, каждая инженерная команда могла бы иметь такого.

---

## Структура мастерской

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **Примечание:** Папка `agent/` внутри каждой лабораторной работы создаётся расширением **Microsoft Foundry** при запуске команды `Microsoft Foundry: Create a New Hosted Agent` из Command Palette. Файлы затем настраиваются с инструкциями, инструментами и конфигурацией вашего агента. Лабораторная 01 проведет вас через процесс создания с нуля.

---

## Начало работы

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Настройте виртуальное окружение Python

```bash
python -m venv venv
```

Активируйте его:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Установите зависимости

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Настройте переменные окружения

Скопируйте пример файла `.env` в папку агента и заполните ваши значения:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Отредактируйте `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Следуйте лабораторным работам

Каждая лабораторная работа автономна со своими модулями. Начните с **Лабораторной 01**, чтобы изучить основы, затем переходите к **Лабораторной 02** для многоагентных рабочих процессов.

#### Лабораторная 01 - Один агент ([полные инструкции](workshop/lab01-single-agent/README.md))

| № | Модуль | Ссылка |
|---|--------|------|
| 1 | Прочитать требования | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Установить Foundry Toolkit и расширение Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Создать проект Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Создать hosted agent | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Настроить инструкции и окружение | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Тестировать локально | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Развернуть в Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Проверить в playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Устранение неполадок | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Лабораторная 02 - Многоагентный рабочий процесс ([полные инструкции](workshop/lab02-multi-agent/README.md))

| № | Модуль | Ссылка |
|---|--------|------|
| 1 | Требования (Лабораторная 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Понять архитектуру многоагентной системы | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Создать структуру многоагентного проекта | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Настроить агентов и окружение | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Шаблоны оркестровки | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Тестировать локально (многоагентный) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Развертывание в Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Проверка в playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Решение проблем (многоагентный режим) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Ответственный за поддержку

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Шивам Гоял</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## Необходимые разрешения (быстрая справка)

| Сценарий | Необходимые роли |
|----------|---------------|
| Создание нового проекта Foundry | **Владелец Azure AI** для ресурса Foundry |
| Развертывание в существующий проект (новые ресурсы) | **Владелец Azure AI** + **Участник** для подписки |
| Развертывание в полностью настроенный проект | **Читатель** для учетной записи + **Пользователь Azure AI** для проекта |

> **Важно:** роли Azure `Владелец` и `Участник` включают только *управленческие* разрешения, а не *разработческие* (действия с данными). Для создания и развертывания агентов вам нужны **Пользователь Azure AI** или **Владелец Azure AI**.

---

## Ресурсы

- [Быстрый старт: развертывание вашего первого хостингового агента (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Что такое хостинговые агенты?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Создание рабочих процессов хостинговых агентов в VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Развертывание хостингового агента](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC для Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Пример агента для обзора архитектуры](https://github.com/Azure-Samples/agent-architecture-review-sample) - Реальный хостинговый агент с инструментами MCP, диаграммами Excalidraw и двойным развертыванием

---


## Лицензия

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->