# Модул 8 - Решавање проблема

Овај модул обухвата честе грешке, исправке и стратегије отклањања грешака специфичне за мулти-агентски радни ток.

## Проблеми са излазом агента

### GapAnalyzer каже „Још увек немам одговарајући извештај“

**Симптом:** Одговор GapAnalyzera тражи да залепите одговарајући извештај са „Недостајућим вештинама“ и „Празнинама у сертификатима.“ Ово се дешава чак и када сте послали и CV и опис посла.

**Узрок:** Текст JD није прослеђен даље JD агенту. Са `context_mode="last_agent"`, `resume_executor` је једини извршилац који икада види оригиналну поруку корисника. Ако `RESUME_PARSER_INSTRUCTIONS` не укључује JD текст у свој излаз, JD агент нема JD за парсирање, MatchingAgent не може израчунати резултат уклапања, и GapAnalyzer добија бесмислен улаз.

**Дијагноза:**

У серверским записима потражите MatchingAgent span. Ако садржи:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
пренос података недостаје или је прекинут.

**Исправка:** Потврдите да `RESUME_PARSER_INSTRUCTIONS` у `main.py` садржи `[JOB DESCRIPTION PASS-THROUGH]` секцију и правило:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Такође потврдите да `JOB_DESCRIPTION_INSTRUCTIONS` садржи `[PARSED RESUME PASS-THROUGH]` правило преношења:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Ако је било који од блокова упутстава шаблон са мастер Wizard-а, замените га комплетном верзијом из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent излази са „Не може се израчунати резултат уклапања - није обезбеђен JD“

Ово је исти корени узрок као горе. MatchingAgent је примио излаз JD агента али је `[PARSED RESUME PASS-THROUGH]` секција недостајала или била празна, па није могао упоредити два профила. Потврдите:
1. `JOB_DESCRIPTION_INSTRUCTIONS` укључује правило преношења: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` указује агенту да тражи `[JD REQUIREMENTS]` и `[PARSED RESUME PASS-THROUGH]` секције.

Замените оба блока упутстава комплетним верзијама из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Одговор се појављује два пута

**Симптом:** Излаз GapAnalyzera (или целокупан излаз ланца) се појављује два пута у одговору Agent Inspectora.

**Узрок:** `WorkflowBuilder` користи OR-семантику за долазне ивице - доњи извршилац се активира чим **било који** претходник заврши. Ако `matching_executor` има две долазне ивице (једну од `resume_executor` и једну од `jd_executor`), активира се два пута: једном када ResumeParser заврши и поново када JD Agent заврши. Потом и GapAnalyzer ради два пута.

**Поправка:** Обезбедите да граф `WorkflowBuilder` буде строго секвенцијални пипелине без фан-ин:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Ако имате насумичну `.add_edge(resume_executor, matching_executor)` линију, уклоните је. `[PARSED RESUME PASS-THROUGH]` релеј у излазу JD Agent-а већ омогућава MatchingAgent приступ резимеу.

---

## Проблеми са окружењем и конфигурацијом

### Недостајуће или погрешне `.env` вредности

`.env` датотека мора бити у `PersonalCareerCopilot/` директоријуму (на истом нивоу као `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Очекивани садржај `.env`:

**Путања A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Путања B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Оба пута користе `FOUNDRY_PROJECT_ENDPOINT`. Вредност се разликује: cloud користи `https://` Foundry крајњу тачку; local користи `http://localhost:5273/v1`. Покрените `foundry model list` да бисте потврдили тачан алјас модела за Путању B.

> **Како пронаћи свој `FOUNDRY_PROJECT_ENDPOINT`:** 
- Отворите **Foundry Toolkit** бочни панел у VS Code → кликните десним кликом на свој пројекат → **Copy Project Endpoint**. 
- Или идите на [Azure Portal](https://portal.azure.com) → свој Foundry пројекат → **Overview** → **Project endpoint**.

> **Како пронаћи свој `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** У Foundry Toolkit бочном панелу, проширите свој пројекат → **Models** → пронађите име распоређеног модела (нпр. `gpt-4.1-mini`).

### Приоритет еколошких променљивих

`main.py` користи `load_dotenv(override=True)`, што значи:

| Приоритет | Извор | Побеђује када су обоје подешени? |
|----------|--------|------------------------------|
| 1 (највиши) | `.env` датотека | Да |
| 2 | Shell / окружење контејнера | Користи се ако исти кључ није у `.env` |

При локалном развоју, ово чини `.env` извором истине (уредбе `.env` одмах утичу на извршења). При хостованој примени, Foundry убризгава еколошке променљиве на нивоу контејнера; пошто `.env` није део имплементиране слике за овај лаб, користе се убризгане вредности контејнера.

---

## Компатибилност верзија

### Матрица верзија пакета

Радни ток са више агената захтева специфичне верзије пакета. Неслагање верзија изазива грешке током извршења.

| Пакет | Потребна верзија | Налог за проверу |
|---------|-----------------|---------------|
| `agent-framework-foundry` | најновије | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | најновије | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | најновије | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Уобичајене грешке верзије

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

### Проверите све верзије одједном

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Очекивани излаз:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Проблеми са деплојментом

### Контејнер не успева да се покрене након деплојмента

1. **Проверите дневнике контејнера:**
   - Отворите **Foundry Toolkit** бочни панел → под својим пројектом, кликните **Agents** → таб **Hosted Agent** → кликните на свог агента. Проверите **Status** на табу **Details**, затим отворите таб **Playground** и употребите таб **Logs** у панелу **Session Details** за увид у излаз контејнера.
   - Потражите Python стектрасе или грешке о недостајућем модулима.

2. **Уобичајени узроци неуспеха покретања контејнера:**

   | Грешка у дневнику | Узрок | Поправка |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` недостаје пакет | Додајте пакет, поново деплојујте |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` или `.env` еколошке променљиве нису подешене | Ажурирајте `agent.yaml` → `environment_variables` одељак (хостовано) или `.env` (локално) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity није конфигурисан | Foundry аутоматски подешава - обезбедите да деплојујете преко екстензије |
   | `OSError: port 8088 already in use` | Dockerfile излаже погрешан порт или конфликт портова | Верификујте `EXPOSE 8088` у Dockerfile и `CMD ["python", "main.py"]` |
   | Контејнер излази са кодом 1 | Непозната изузетак у `main()` | Прво тестирајте локално ([Модул 5](05-test-locally.md)) да бисте уочили грешке пре деплоја |

3. **Поново деплојујте након исправке:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → изаберите истог агента → деплојујте нову верзију.

### Деплојмент траје предуго

Мулти-агент контејнери полако се покрећу јер направе 4 инстанце агената при покретању. Нормално време покретања:

| Фаза | Очекивани трајање |
|-------|------------------|
| Изградња слике контејнера | 1-3 минута |
| Пуш слике у ACR | 30-60 секунди |
| Покретање контејнера (један агент) | 15-30 секунди |
| Покретање контејнера (више агената) | 30-120 секунди |
| Агент доступан у Playground-у | 1-2 минута након "Started" |

> Ако статус "Pending" траје дуже од 5 минута, проверите дневнике контејнера за грешке.

---

## RBAC и проблеми са дозволама

### `403 Forbidden` или `AuthorizationFailed`

Потребна вам је улога **[Foundry User](https://aka.ms/foundry-ext-project-role)** на вашем Foundry пројекту (раније звано **Azure AI User** - ID улоге се није променио):

1. Идите на [Azure Portal](https://portal.azure.com) → ресурс вашег Foundry **пројекта**.
2. Кликните **Access control (IAM)** → **Role assignments**.
3. Претражите своје име → потврдите да је **Foundry User** (или ранија ознака **Azure AI User**) на листи.
4. Ако недостаје: **Add** → **Add role assignment** → претражите **Foundry User** → доделите свом налогу.

Погледајте документацију [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) за детаље.

### Модел распоређен није доступан

Ако агент враћа грешке везане за модел:

1. Потврдите да је модел распоређен: Foundry бочни панел → проширите пројекат → **Models** → проверите да ли `gpt-4.1-mini` (или ваш модел) има статус **Succeeded**.
2. Потврдите да се име распоређивања поклапа: упоредите `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` (или `agent.yaml`) са стварним именом распоређивања у бочном панелу.
3. Ако је распоређивање истекло (бесплатни ниво): поново распоредите из [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Проблеми са Foundry Local (Путања B)

### Foundry Local сервис није покренут

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Симптом | Узрок | Поправка |
|---------|-------|-----|
| Health check враћа `503` | Сервис није покренут | `foundry local start` или кликните **Start** у Foundry Toolkit бочној траци |
| Health check истекне | Модел се још учитава | Сачекајте 30–60 с након покретања; већи модели траже дуже |
| `StatusCode: 404` на `/v1/health` | Погрешан порт | Подразумевано је `5273`. Проверите `foundry local status` за стварни порт |
| Недовољно ресурса | Foundry Local треба ~4 GB RAM-а слободно | Затворите друге апликације |
| Преузимање модела не успева | Недовољно простора на диску | Модели су 2–8 GB. Ослободите простор, затим `foundry model pull <name>` |

### Неподударност имена модела

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Поставите `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` на тачан алјас приказан (нпр. `phi-4-mini`, не `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` приликом локалног покретања (Путања B)

Лаб је `main.py` користи `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local захтева да ова променљива показује на локални сервис - **не** `AZURE_AI_PROJECT_ENDPOINT`. Осигурајте да ваш `.env` садржи:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP алат и даље прави излазни позив (Путања B)

Ово је очекивано. `search_microsoft_learn_for_plan` алат преузима ресурсе за учење са `https://learn.microsoft.com/api/mcp`. **Само упит за име вештине** путује мрежом - резиме и JD текст се обрађују у потпуности на вашем уређају и никада се не преносе. Ако је потребно потпуно офлајн функционисање, додајте `try/except` резерву у алат који враћа статичан `learn.microsoft.com` URL када крајња тачка није доступна.

---

## Како добити помоћ

Ако сте запели након покушаја горе наведених решења:

1. **Проверите серверске дневнике** - Већина грешака производи Python стектрејс у терминалу. Прочитајте цео traceback.
2. **Претражите поруку о грешци** - Копирајте текст грешке и претражите на [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Отворите issue** - Поднесите issue у [workshop репозиторијум](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) са:
   - Поруком о грешци или снимком екрана
   - Верзијама пакета (`pip list | Select-String "agent-framework"`)
   - Вашом Python верзијом (`python --version`)
   - Да ли је проблем локалан или након деплоја

---

### Контролна тачка

- [ ] Знате како да проверите и исправите проблеме са `.env` конфигурацијом
- [ ] Можете верификовати да верзије пакета одговарају потребној матрици
- [ ] Знате како да проверите дневнике контејнера за неуспехе деплоја
- [ ] Можете да проверите RBAC улоге у Azure порталу

---

**Претходно:** [07 - Verify in Playground](07-verify-in-playground.md) · **Следеће:** [09 - Summary →](09-summary.md) · **Почетак:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Изјава о одрицању одговорности**:
Овај документ је преведен коришћењем услуге за аутоматски превод [Co-op Translator](https://github.com/Azure/co-op-translator). Иако тежимо тачности, имајте у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитативним извором. За критичне информације препоручује се професионални људски превод. Нисмо одговорни за било каква неспоразума или погрешна тумачења која произилазе из коришћења овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->