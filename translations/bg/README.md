# Foundry Toolkit + Foundry Hosted Agents Workshop

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.0.0rc3-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents/)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Изградете, тествайте и разгръщайте AI агенти към **Microsoft Foundry Agent Service** като **Hosted Agents** - изцяло от VS Code с помощта на **Microsoft Foundry extension** и **Foundry Toolkit**.

> **Hosted Agents в момента са в предварителна версия.** Поддържаните региони са ограничени - вижте [region availability](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Папката `agent/` във всяка лаборатория се **генерира автоматично** от Foundry extension - след това персонализирате кода, тествате локално и разгръщате.

### 🌐 Поддръжка на много езици

#### Поддържа се чрез GitHub Action (Автоматизирано и винаги актуално)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](./README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Предпочитате да клонирате локално?**
>
> Това хранилище включва над 50 езикови превода, което значително увеличава размера на изтеглянето. За да клонирате без преводите, използвайте sparse checkout:
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
> Така получавате всичко необходимо за завършване на курса с много по-бързо изтегляне.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Архитектура

```mermaid
flowchart TB
    subgraph Local["Локална разработка (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Разширение"]
        FoundryToolkit["Foundry Toolkit
        Разширение"]
        Scaffold["Създаден код на агент
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Инспектор на агент
        (Локално тестване)"]
        FE -- "Създаване на нов
        хостван агент" --> Scaffold
        Scaffold -- "Отстраняване на грешки с F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Изпълнение на хостван агент)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Разгръщане
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Тестване на заявки" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**Поток:** Foundry extension генерира агента → вие персонализирате кода и инструкциите → тествате локално с Agent Inspector → разгръщате в Foundry (Docker образ изпратен в ACR) → проверявате в Playground.

---

## Какво ще изградите

| Лаборатория | Описание | Статус |
|-----|-------------|--------|
| **Лаб 01 - Един агент** | Изградете **"Обясни като за изпълнителен директор" агент**, тествайте го локално и го разположете в Foundry | ✅ Достъпен |
| **Лаб 02 - Мултиагентен работен процес** | Изградете **"Оценка на съвместимост на автобиография с работа"** - 4 агента си сътрудничат, за да оценят съвместимостта и да генерират пътна карта за обучение | ✅ Достъпен |

---

## Запознайте се с агента за изпълнителни директори

В този работилница ще изградите **"Обясни като за изпълнителен директор" агент** – AI агент, който взема сложен технически жаргон и го превежда в спокойни, готови за съвета на директорите резюмета. Защото, честно казано, никой в C-suite не иска да слуша за "изморяване на нишковия пул, причинено от синхронни повиквания, въведени във v3.2."

Изградих този агент след твърде много случаи, в които перфектно формулираният ми пост-мортем получаваше отговор: *"Така… сайтовеа свален или не?"*

### Как работи

Въвеждате му техническа актуализация. Той връща изпълнително резюме – три точки, без жаргон, без стек трайсове, без екзистенциален страх. Само **какво се е случило**, **влияние върху бизнеса**, и **следваща стъпка**.

### Вижте го в действие

**Вие казвате:**
> "Забавянето на API нарасна поради изчерпване на нишковия пул, причинено от синхронни повиквания, въведени във v3.2."

**Агентът отговаря:**

> **Изпълнително резюме:**
> - **Какво се случи:** След последното пускане системата забави.
> - **Влияние върху бизнеса:** Някои потребители изпитаха забавяне при използване на услугата.
> - **Следваща стъпка:** Промяната е отменена и се подготвя поправка преди повторно разгръщане.

### Защо този агент?

Това е изключително прост и целенасочен агент – перфектен за научаване на процеса за мултиагентна работна среда от край до край без да се затъва в сложни инструменти. И честно? Всеки инженеринг екип може да се възползва от такъв.

---

## Структура на работилницата

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
├── 📂 ExecutiveAgent/                ← Standalone hosted agent project
│   ├── agent.yaml
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-install-foundry-toolkit.md
    │   │   ├── 02-create-foundry-project.md
    │   │   ├── 03-create-hosted-agent.md
    │   │   ├── 04-configure-and-code.md
    │   │   ├── 05-test-locally.md
    │   │   ├── 06-deploy-to-foundry.md
    │   │   ├── 07-verify-in-playground.md
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

> **Забележка:** Папката `agent/` във всяка лаборатория е това, което **Microsoft Foundry extension** генерира, когато стартирате `Microsoft Foundry: Create a New Hosted Agent` от Command Palette. След това файловете се персонализират с инструкции, инструменти и конфигурация на агента. Лаб 01 ви води през създаването на това от нулата.

---

## Започване

### 1. Клонирайте хранилището

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Настройте Python виртуална среда

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

Копирайте примерния `.env` файл в папката на агента и попълнете стойностите си:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Редактирайте `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Следвайте лабораториите

Всяка лаборатория е самостоятелна с собствени модули. Започнете с **Лаб 01** за да научите основите, след това продължете с **Лаб 02** за мултиагентен работен процес.

#### Лаб 01 - Един агент ([пълни инструкции](workshop/lab01-single-agent/README.md))

| № | Модул | Линк |
|---|--------|------|
| 1 | Прочетете предпоставките | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Инсталирайте Foundry Toolkit & Foundry extension | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Създайте Foundry проект | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | Създайте hosted агент | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | Конфигурирайте инструкции и среда | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | Тествайте локално | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Разгърнете в Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Потвърдете в playground | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | Отстраняване на проблеми | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Лаб 02 - Мултиагентен работен процес ([пълни инструкции](workshop/lab02-multi-agent/README.md))

| № | Модул | Линк |
|---|--------|------|
| 1 | Предпоставки (Лаб 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Разберете мултиагентната архитектура | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Генерирайте мултиагентния проект | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Конфигурирайте агенти и среда | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Модели на оркестрация | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Тествайте локално (мултиагентен) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Деплой към Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Проверка в playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Отстраняване на проблеми (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Поддържащ

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## Изисквани разрешения (бърза справка)

| Сценарий | Изисквани роли |
|----------|---------------|
| Създаване на нов проект в Foundry | **Azure AI Owner** върху ресурса Foundry |
| Деплой към съществуващ проект (нови ресурси) | **Azure AI Owner** + **Contributor** върху абонамента |
| Деплой към напълно конфигуриран проект | **Reader** върху акаунта + **Azure AI User** върху проекта |

> **Важно:** Ролите `Owner` и `Contributor` в Azure включват само *управленски* права, а не права за *разработка* (действия с данни). Трябва ви **Azure AI User** или **Azure AI Owner**, за да създавате и деплойвате агенти.

---

## Препратки

- [Бърз старт: Деплой на първия ви хостван агент (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Какво представляват хостваните агенти?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Създаване на работни потоци за хоствани агенти във VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Деплой на хостван агент](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC за Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Пример за агент за архитектурен преглед](https://github.com/Azure-Samples/agent-architecture-review-sample) - Действителен хостван агент с MCP инструменти, диаграми от Excalidraw и двоен деплой

---

## Лиценз

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:  
Този документ е преведен с помощта на AI преводаческа услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за всякакви недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->