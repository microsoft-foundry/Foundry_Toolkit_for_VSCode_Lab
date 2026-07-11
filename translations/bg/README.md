# Foundry Toolkit + Foundry Hosted Agents Workshop

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

Създавайте, тествайте и внедрявайте AI агенти в **Microsoft Foundry Agent Service** като **Hosted Agents** - изцяло от VS Code, използвайки **Microsoft Foundry разширението** и **Foundry Toolkit**.

> **Hosted Agents в момента са в предварителен преглед.** Поддържаните региони са ограничени - вижте [наличност на региони](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Папката `agent/` във всяка лаборатория е **автоматично създадена** от Foundry разширението - след това персонализирате кода, тествате локално и внедрявате.

### 🌐 Поддръжка на множество езици

#### Поддържа се чрез GitHub Action (Автоматизирано и винаги актуално)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](./README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Предпочитате да копирате локално?**
>
> Това хранилище включва над 50 езикови превода, което значително увеличава размера за изтегляне. За да клонирате без преводи, използвайте sparse checkout:
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
> Това ви дава всичко необходимо за завършване на курса с много по-бързо изтегляне.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Архитектура

```mermaid
flowchart TB
    subgraph Local["Локална разработка (VS Code)"]
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
        Scaffold -- "F5 Отстраняване на грешки" --> Inspector
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
    (localhost:8088)" --> Създаване на скеле
    Playground -- "Тестови подсказки" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Поток:** Foundry разширението създава агента → вие персонализирате кода и инструкциите → тествате локално с Agent Inspector → внедрявате в Foundry (Docker изображение изпратено в ACR) → проверявате в Playground.

---

## Какво ще създадете

| Лаборатория | Описание | Статус |
|-----|-------------|--------|
| **Лаб 01 - Единичен агент** | Създайте **"Обясни като за ръководител" агент**, тествайте го локално и го внедрете във Foundry | ✅ Наличен |
| **Лаб 02 - Многоагентен работен процес** | Създайте **"Оценител на автобиографии и подходящост за работа"** - 4 агента си сътрудничат за оценка на автобиографията и генериране на учебна пътна карта | ✅ Наличен |

---

## Запознайте се с агента за ръководството

В този уъркшоп ще създадете **"Обясни като за ръководител" агент** - AI агент, който преобразува сложния технически жаргон в спокойни, представими резюмета за заседателната зала. Защото, да бъдем честни, никой в управлението не иска да слуша за "изчерпване на thread pool, причинено от синхронни повиквания, въведени във v3.2."

Създадох този агент след твърде много случаи, в които перфектно направеният ми анализ след инцидент получаваше отговор: *"Така... сайтът е паднал или не?"*

### Как работи

Въвеждате му техническо обновление. Той връща резюме за ръководството - три ключови точки, без жаргон, без трасета на грешки, без екзистенциална тревога. Само **какво се е случило**, **влияние върху бизнеса** и **следваща стъпка**.

### Вижте го в действие

**Вие казвате:**
> "Забавянето на API се увеличи поради изчерпване на thread pool, причинено от синхронни повиквания, въведени във v3.2."

**Агентът отговаря:**

> **Резюме за ръководството:**
> - **Какво се случи:** След последното издание системата забави.
> - **Влияние върху бизнеса:** Някои потребители изпитаха забавяния при използване на услугата.
> - **Следваща стъпка:** Промяната е върната обратно и се подготвя поправка преди повторно внедряване.

### Защо точно този агент?

Това е прост, едноцелеви агент - перфектен за да научите работния процес на hosted agent от край до край без да се затормозявате с комплексни инструментални вериги. И честно? Всеки инженеринг екип може да използва такъв.

---

## Структура на уъркшопа

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

> **Бележка:** Папката `agent/` във всяка лаборатория е това, което **Microsoft Foundry разширението** генерира когато стартирате `Microsoft Foundry: Create a New Hosted Agent` от Командния панел. След това файловете се персонализират с инструкциите, инструментите и конфигурацията на вашия агент. Лаб 01 ви води през създаването му от нулата.

---

## Започване

### 1. Клонирайте хранилището

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Настройте виртуална Python среда

```bash
python -m venv venv
```

Активирайте я:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Инсталирайте зависимости

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Конфигурирайте променливи на средата

Копирайте примерния `.env` файл в папката на агента и попълнете вашите стойности:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Редактирайте `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Следвайте лабораториите на уъркшопа

Всяка лаборатория е самостоятелна с собствени модули. Започнете с **Лаб 01**, за да научите основите, след това преминете към **Лаб 02** за многоагентни работни потоци.

#### Лаб 01 - Единичен агент ([пълни инструкции](workshop/lab01-single-agent/README.md))

| # | Модул | Връзка |
|---|------|-------|
| 1 | Прочетете предварителните условия | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Инсталирайте Foundry Toolkit и Foundry разширението | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Създайте Foundry проект | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Създайте hosted агент | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Конфигурирайте инструкции и среда | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Тествайте локално | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Внедрете в Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Проверете в playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Отстраняване на проблеми | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Лаб 02 - Многоагентен работен поток ([пълни инструкции](workshop/lab02-multi-agent/README.md))

| # | Модул | Връзка |
|---|------|-------|
| 1 | Предварителни условия (Лаб 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Разбиране на многоагентната архитектура | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Създаване на многоагентен проект | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Конфигуриране на агенти и среда | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Патерни за оркестрация | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Тествайте локално (многоагентен) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Деплой в Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Проверка в playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Отстраняване на неизправности (многоагентна) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Поддръжник

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

## Необходими разрешения (бърза справка)

| Сценарий | Необходими роли |
|----------|---------------|
| Създаване на нов проект Foundry | **Azure AI Owner** върху ресурс Foundry |
| Деплой в съществуващ проект (нови ресурси) | **Azure AI Owner** + **Contributor** върху абонамент |
| Деплой в напълно конфигуриран проект | **Reader** върху акаунта + **Azure AI User** върху проекта |

> **Важно:** Ролите Azure `Owner` и `Contributor` включват само *разрешения за управление*, а не *разработване* (действия с данни). За да създавате и деплойвате агенти, ви трябва **Azure AI User** или **Azure AI Owner**.

---

## Референции

- [Първи стъпки: Деплой на първия ви хостван агент (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Какво са хоствани агенти?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Създаване на работни потоци с хоствани агенти във VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Деплой на хостван агент](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC за Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Пример с Architecture Review Agent](https://github.com/Azure-Samples/agent-architecture-review-sample) - Реален хостван агент с MCP инструменти, диаграми Excalidraw и двойно разгръщане

---


## Лиценз

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:
Този документ е преведен с помощта на AI преводачески услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да е недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->