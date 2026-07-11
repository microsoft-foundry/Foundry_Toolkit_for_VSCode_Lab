# Модул 8 - Отстраняване на проблеми

Този модул обхваща често срещани грешки, поправки и стратегии за отстраняване на грешки, специфични за многo-агентния работен поток.

## Проблеми с изхода на агента

### GapAnalyzer казва "Все още нямам съответстващия доклад"

**Симптом:** Отговорът на GapAnalyzer ви моли да поставите доклад за съвпадение с „Липсващи умения“ и „Проблеми с сертифицирането“. Това се случва, дори когато сте изпратили както автобиография, така и описание на работата.

**Причина:** Текстът на JD не е предаден на JD Agent. С `context_mode="last_agent"`, `resume_executor` е единственият изпълнител, който вижда оригиналното съобщение на потребителя. Ако `RESUME_PARSER_INSTRUCTIONS` не включва текста на JD в изхода си, JD Agent няма JD за анализиране, MatchingAgent не може да изчисли оценка за съвпадение и GapAnalyzer получава безсмислен вход.

**Диагноза:**

В логовете на сървъра потърсете спана на MatchingAgent. Ако съдържа:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
пропускът на информация е липсващ или счупен.

**Поправка:** Потвърдете, че `RESUME_PARSER_INSTRUCTIONS` в `main.py` съдържа секция `[JOB DESCRIPTION PASS-THROUGH]` и правилото:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Също потвърдете, че `JOB_DESCRIPTION_INSTRUCTIONS` съдържа ретранслационно правило `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Ако някой от инструкционните блокове е шаблон от скелета, заменете го с пълната версия от [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent извежда „Не може да изчисли оценка за съвпадение - няма предоставен JD“

Това е същата основна причина като по-горе. MatchingAgent е получил изхода на JD Agent, но секцията `[PARSED RESUME PASS-THROUGH]` липсва или е празна, така че не може да сравни двата профила. Потвърдете:
1. `JOB_DESCRIPTION_INSTRUCTIONS` включва правилото за ретранслация: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` казва на агента да търси секции `[JD REQUIREMENTS]` и `[PARSED RESUME PASS-THROUGH]`.

Заменете двата инструкционни блока с пълните версии от [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Отговорът се появява два пъти

**Симптом:** Изходът на GapAnalyzer (или целият изход на конвейера) се появява два пъти в отговора на Agent Inspector.

**Причина:** `WorkflowBuilder` използва OR-семантика за входящи връзки - последващ изпълнител се активира веднага щом **някой** предшественик завърши. Ако `matching_executor` има две входящи връзки (една от `resume_executor` и една от `jd_executor`), той се активира два пъти: веднъж когато ResumeParser завърши и отново когато JD Agent завърши. След това GapAnalyzer също се изпълнява два пъти.

**Поправка:** Уверете се, че графът на `WorkflowBuilder` е строго последователен конвейер без фан-ин:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # НЕ е от resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Ако имате излишен ред `.add_edge(resume_executor, matching_executor)`, премахнете го. Ретранслата `[PARSED RESUME PASS-THROUGH]` в изхода на JD Agent вече дава на MatchingAgent достъп до резюмето.

---

## Проблеми с околната среда и конфигурацията

### Липсващи или грешни стойности в `.env`

Файлът `.env` трябва да е в директорията `PersonalCareerCopilot/` (на същото ниво като `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Очаквано съдържание на `.env`:

**Път A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Път B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> И по двата пътя се използва `FOUNDRY_PROJECT_ENDPOINT`. Стойността е различна: облакът използва `https://` Foundry endpoint; локално се използва `http://localhost:5273/v1`. Стартирайте `foundry model list`, за да потвърдите точния модел на алиаса за Път Б.

> **Намиране на вашия `FOUNDRY_PROJECT_ENDPOINT`:**
- Отворете страничната лента на **Foundry Toolkit** в VS Code → кликнете с десен бутон върху проекта си → **Copy Project Endpoint**.
- Или отидете на [Azure Portal](https://portal.azure.com) → вашия Foundry проект → **Overview** → **Project endpoint**.

> **Намиране на вашия `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** В страничната лента на Foundry Toolkit, разширете проекта си → **Models** → намерете името на деплойнатия модел (например, `gpt-4.1-mini`).

### Приоритет на променливите на средата

`main.py` използва `load_dotenv(override=True)`, което означава:

| Приоритет | Източник | Избира се, когато и двата са настроени? |
|----------|--------|------------------------|
| 1 (на най-висок приоритет) | Файл `.env` | Да |
| 2 | Shell / променлива на контейнера | Използва се, когато същият ключ липсва в `.env` |

В локалната разработка това прави `.env` източник на истината (редактирането на `.env` веднага влияе на изпълненията). При хоствана инсталация, Foundry инжектира променливи на средата на ниво контейнер; тъй като `.env` не е част от деплойнатото изображение за тази лабораторна настройка, се използват стойностите, инжектирани в контейнера.

---

## Съвместимост на версиите

### Матрица на версиите на пакетите

Многo-агентният работен поток изисква специфични версии на пакетите. Несъответствията в версиите причиняват грешки по време на изпълнение.

| Пакет | Изисквана версия | Команда за проверка |
|---------|-----------------|---------------|
| `agent-framework-foundry` | последна | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | последна | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | последна | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Чести грешки с версии

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Поправка: преинсталирайте agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Поправка: ъпгрейд на пакета mcp
pip install mcp --upgrade
```

### Проверете всички версии наведнъж

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Очакван изход:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Проблеми при деплоймънт

### Контейнерът не стартира след деплоймънт

1. **Проверете логовете на контейнера:**
   - Отворете страничната лента на **Foundry Toolkit** → разширете **Hosted Agents (Preview)** → кликнете вашия агент → разширете версията → **Container Details** → **Logs**.
   - Потърсете Python stack trace или грешки за липсващи модули.

2. **Чести причини за неуспех при стартиране на контейнер:**

   | Грешка в логовете | Причина | Поправка |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` липсва пакет | Добавете пакета, прегодете |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Променливи в `agent.yaml` или `.env` не са зададени | Актуализирайте `agent.yaml` → секция `environment_variables` (хоствано) или `.env` (локално) |
   | `azure.identity.CredentialUnavailableError` | Управлявана идентичност не е конфигурирана | Foundry го задава автоматично – уверете се, че публикувате през разширението |
   | `OSError: port 8088 already in use` | Dockerfile експонира грешен порт или конфликт на портове | Проверете `EXPOSE 8088` в Dockerfile и `CMD ["python", "main.py"]` |
   | Контейнерът излиза с код 1 | Необработено изключение в `main()` | Тествайте локално първо ([Модул 5](05-test-locally.md)) за прихващане на грешки |

3. **Повторете деплоймънта след поправката:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → изберете същия агент → пуснете нова версия.

### Деплоймънтът отнема твърде много време

Многo-агентните контейнери отнемат повече време за стартиране, тъй като създават 4 екземпляра на агента при стартиране. Нормални времена за стартиране:

| Етап | Очаквана продължителност |
|-------|------------------|
| Създаване на изображение на контейнера | 1-3 минути |
| Избутване на изображение към ACR | 30-60 секунди |
| Стартиране на контейнер (един агент) | 15-30 секунди |
| Стартиране на контейнер (многo-агент) | 30-120 секунди |
| Агент наличен в Playground | 1-2 минути след "Started" |

> Ако статусът "Pending" продължи повече от 5 минути, проверете логовете на контейнера за грешки.

---

## RBAC и проблеми с разрешения

### `403 Forbidden` или `AuthorizationFailed`

Трябва ви роля **[Foundry User](https://aka.ms/foundry-ext-project-role)** за вашия Foundry проект (преди наричана **Azure AI User** - с идентификатор на ролята непроменен):

1. Отидете на [Azure Portal](https://portal.azure.com) → вашия ресурс на Foundry **проект**.
2. Кликнете **Access control (IAM)** → **Role assignments**.
3. Потърсете името си → потвърдете, че **Foundry User** (или наследеното име **Azure AI User**) е в списъка.
4. Ако липсва: **Add** → **Add role assignment** → потърсете **Foundry User** → присвоете на своя акаунт.

Вижте документацията [RBAC за Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) за подробности.

### Моделът не е достъпен при деплоймънт

Ако агентът връща грешки, свързани с модела:

1. Потвърдете, че моделът е деплойнат: странична лента на Foundry → разширете проекта → **Models** → проверете дали `gpt-4.1-mini` (или вашият модел) е със статус **Succeeded**.
2. Потвърдете, че името на деплоймънта съвпада: сравнете `AZURE_AI_MODEL_DEPLOYMENT_NAME` в `.env` (или `agent.yaml`) с реалното име на деплоймънта в страничната лента.
3. Ако деплоймънтът е изтекъл (безплатния слой): деплойнете повторно от [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Проблеми с Foundry Local (Път B)

### Сервисът Foundry Local не работи

```powershell
# Провери състоянието
foundry local status

# Стартирай услугата, ако е спряна
foundry local start
```

| Симптом | Причина | Поправка |
|---------|-------|-----|
| Здравен чек връща `503` | Сервисът не е стартиран | Стартирайте `foundry local start` или кликнете **Start** в страничната лента на Foundry Toolkit |
| Здравен чек изтича | Моделът се зарежда все още | Изчакайте 30–60 сек. след стартиране; по-големите модели отнемат повече време |
| `StatusCode: 404` при `/v1/health` | Грешен порт | По подразбиране е `5273`. Проверете с `foundry local status` за реалния порт |
| Недостатъчни ресурси | Foundry Local изисква ~4 GB RAM свободна памет | Затворете други приложения |
| Свалянето на модела неуспешно | Липса на дисково пространство | Моделите са 2–8 GB. Освободете място, след това `foundry model pull <name>` |

### Несъответствие на името на модела

```powershell
# Избройте изтеглените модели и техните точни псевдоними
foundry model list
```

Задайте `AZURE_AI_MODEL_DEPLOYMENT_NAME` в `.env` на точния алиас, показан (например, `phi-4-mini`, а не `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` при локално стартиране (Път B)

В `main.py` на лабораторията се използва `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local изисква тази променлива да посочва локалната услуга – **не** `AZURE_AI_PROJECT_ENDPOINT`. Уверете се, че вашият `.env` съдържа:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP инструментът все още прави външен вик (Път B)

Това е очаквано. Инструментът `search_microsoft_learn_for_plan` извлича учебни ресурси от `https://learn.microsoft.com/api/mcp`. **Само името на умението** се пуска по мрежата - автобиографията и текста на JD се обработват изцяло на вашето устройство и никога не се предават. Ако е необходим пълен офлайн режим, добавете `try/except` резервен вариант в инструмента, който връща статичен URL на `learn.microsoft.com`, когато крайната точка е недостъпна.

---

## Получаване на помощ

Ако сте блокирани след опитите за поправки по-горе:

1. **Проверете логовете на сървъра** – Повечето грешки генерират стектрейс в терминала. Прочетете целия трейскбек.
2. **Потърсете съобщението за грешка** – Копирайте текста на грешката и потърсете в [Microsoft Q&A за Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Отворете issue** – Създайте issue в [репото на работилницата](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) с:
   - Съобщението за грешка или екранна снимка
   - Версиите на пакетите ви (`pip list | Select-String "agent-framework"`)
   - Версията на Python (`python --version`)
   - Дали проблемът е локален или след деплоймънт

---

### Контролна точка

- [ ] Знаете как да проверите и поправите конфигурационни проблеми с `.env`
- [ ] Можете да проверите дали версиите на пакетите съвпадат с изискуемата матрица
- [ ] Знаете как да проверите логовете на контейнера за неуспешен деплоймънт
- [ ] Можете да проверите RBAC ролите в Azure портала

---

**Предишен:** [07 - Проверка в Playground](07-verify-in-playground.md) · **Следващ:** [09 - Обобщение →](09-summary.md) · **Начало:** [Lab 02 README](../README.md) · [Начало на работилницата](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:
Този документ е преведен с помощта на AI преводачески услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да е недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->