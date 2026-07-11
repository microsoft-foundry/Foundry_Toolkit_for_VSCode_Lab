# Модул 8 - Решавање проблема

Овај модул покрива уобичајене грешке, исправке и стратегије отклањања грешака специфичне за мулти-агентски ток рада.

## Проблеми са излазом агента

### GapAnalyzer каже „Још увек немам одговарајући извештај“

**Симптом:** Одговор GapAnalyzer-а тражи да залепите извештај који се поклапа и садржи „Недостајуће вештине“ и „Празнине у сертификатима“. Ово се дешава чак и када сте послали и резиме и опис посла.

**Узрок:** Текст JD-а није прослеђен даље ка JD агенту. Са `context_mode="last_agent"`, `resume_executor` је једини извршилац који икада види оригиналну поруку корисника. Ако `RESUME_PARSER_INSTRUCTIONS` не садржи текст JD-а у свом излазу, JD агент нема JD за анализу, MatchingAgent не може да израчуна резултат подударања, а GapAnalyzer добија бесмислен улаз.

**Дијагноза:**

У логовима сервера, потражите опсег MatchingAgent-а. Ако садржи:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
пролазак је изостао или је покварен.

**Исправка:** Потврдите да `RESUME_PARSER_INSTRUCTIONS` у `main.py` садржи одељак `[JOB DESCRIPTION PASS-THROUGH]` и правило:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Такође потврдите да `JOB_DESCRIPTION_INSTRUCTIONS` садржи правило за прослеђивање `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Ако је било који од блокова упутстава шематски из чаробњака за постављање, замените га комплетном верзијом из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent исписује „Не могу да израчунам резултат подударања - није обезбеђен JD“

Ово је исти основни узрок као и горе. MatchingAgent је примио излаз JD агента, али одељак `[PARSED RESUME PASS-THROUGH]` је недостајао или је био празан, па није могао да упореди два профила. Потврдите:
1. `JOB_DESCRIPTION_INSTRUCTIONS` укључује правило за прослеђивање: `Копирај [PARSED RESUME] дословно - MatchingAgent се ослања на то даље у ланцу.`
2. `MATCHING_AGENT_INSTRUCTIONS` упућује агента да тражи одељке `[JD REQUIREMENTS]` и `[PARSED RESUME PASS-THROUGH]`.

Замените оба блока упутстава комплетним верзијама из [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Одговор се појављује два пута

**Симптом:** Излаз GapAnalyzer-а (или цео излаз из све цевовода) појављује се два пута у одговору Agent Inspector-а.

**Узрок:** `WorkflowBuilder` користи OR-семантику за улазне ивице - доњи извршилац се активира чим **било који** претходник заврши. Ако `matching_executor` има две улазне ивице (једна од `resume_executor` и једна од `jd_executor`), активира се два пута: једном када ResumeParser заврши и опет када JD агент заврши. Затим се и GapAnalyzer покреће два пута.

**Исправка:** Обезбедите да график `WorkflowBuilder` буде строго секвенцијални цевовод без конвергенције:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # НЕ из resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Ако имате нежељену линију `.add_edge(resume_executor, matching_executor)`, уклоните је. Прослеђивање `[PARSED RESUME PASS-THROUGH]` у излазу JD агента већ омогућава MatchingAgent-у приступ резимеу.

---

## Проблеми са окружењем и конфигурацијом

### Недостајуће или погрешне вредности у `.env`

Фајл `.env` мора бити у директоријуму `PersonalCareerCopilot/` (на истом нивоу као `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Очекиван садржај `.env`:

**Путања А - Foundry облак:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Путања Б - Foundry локално:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Обе путање користе `FOUNDRY_PROJECT_ENDPOINT`. Вредности се разликују: облак користи `https://` Foundry крајњу тачку; локално је `http://localhost:5273/v1`. Покрените `foundry model list` да бисте проверили тачан алијас модела за Пут Б.

> **Како пронаћи `FOUNDRY_PROJECT_ENDPOINT`:** 
- Отворите **Foundry Toolkit** бочни мени у VS Code → кликните десним тастером на пројекат → **Copy Project Endpoint**. 
- Или идите на [Azure Portal](https://portal.azure.com) → ваш Foundry пројекат → **Преглед** → **Project endpoint**.

> **Како пронаћи `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** У Foundry Toolkit бочном менију, проширите пројекат → **Модели** → пронађите име вашег распоређеног модела (нпр. `gpt-4.1-mini`).

### Преференција променљивих окружења

`main.py` користи `load_dotenv(override=True)`, што значи:

| Приоритет | Извор | Побеђује када су оба постављена? |
|----------|--------|----------------------------|
| 1 (највиши) | `.env` фајл | Да |
| 2 | Променљива окружења у шкољци / контејнеру | Користи се ако исти кључ није присутан у `.env` |

У локалном развоју, ово чини `.env` стварним извором (уређивање `.env` одмах утиче на извршења). У хостованој имплементацији, Foundry убацује променљиве окружења на нивоу контејнера; пошто `.env` није део деплојованог имиджа за овај лаб, користе се вредности из контејнера.

---

## Компатибилност верзија

### Матрица верзија пакета

Мулти-агентски ток рада захтева специфичне верзије пакета. Неслагање верзија изазива грешке при покретању.

| Пакет | Потребна верзија | Команда за проверу |
|---------|-----------------|------------------|
| `agent-framework-foundry` | најновија | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | најновија | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | најновија | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Уобичајене грешке верзије

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Поправка: поново инсталирати agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Поправка: надоградња mcp пакета
pip install mcp --upgrade
```

### Верификујте све верзије одједном

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

## Проблеми при распоређивању

### Контејнер не успева да се покрене након распоређивања

1. **Проверите логове контејнера:**
   - Отворите **Foundry Toolkit** бочни мени → проширите **Hosted Agents (Preview)** → кликните на ваш агент → проширите верзију → **Container Details** → **Logs**.
   - Потражите Python стек трагове или грешке недостајућег модула.

2. **Чести узроци неуспеха покретања контејнера:**

   | Грешка у логовима | Узрок | Исправка |
   |------------------|--------|----------|
   | `ModuleNotFoundError` | `requirements.txt` недостаје пакет | Додајте пакет, поново распоредите |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Нема подешавања env вриједности у `agent.yaml` или `.env` | Ажурирајте део `environment_variables` у `agent.yaml` (хостовано) или `.env` (локално) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity није конфигурисана | Foundry ово подешава аутоматски - уверите се да распоређујете преко екстензије |
   | `OSError: port 8088 already in use` | Dockerfile открива погрешан порт или постоји конфликт порта | Проверите `EXPOSE 8088` у Dockerfile-у и `CMD ["python", "main.py"]` |
   | Контејнер излази са кодом 1 | Неконтролисана изузетак у `main()` | Тестирајте локално прво ([Модул 5](05-test-locally.md)) да ухватите грешке пре распоређивања |

3. **Поново распоредите након исправке:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → изаберите исти агент → распоредите нову верзију.

### Распоређивање траје предуго

Мулти-агентски контејнери траже дуже за покретање јер креирају 4 инстанце агената при покретању. Нормално време покретања:

| Фаза | Очекивано трајање |
|-------|------------------|
| Изградња слике контејнера | 1-3 минута |
| Пуш слике у ACR | 30-60 секунди |
| Покретање контејнера (један агент) | 15-30 секунди |
| Покретање контејнера (мулти-агент) | 30-120 секунди |
| Агент доступан на Playground-у | 1-2 минута након "Started" |

> Ако статус „Pending“ траје дуже од 5 минута, проверите логове контејнера за грешке.

---

## Проблеми са RBAC и дозволама

### `403 Forbidden` или `AuthorizationFailed`

Потребна вам је улога **[Foundry User](https://aka.ms/foundry-ext-project-role)** на вашем Foundry пројекту (раније названа **Azure AI User** - ид улоге није промењен):

1. Идите на [Azure Portal](https://portal.azure.com) → ресурс вашег Foundry **пројекта**.
2. Кликните **Access control (IAM)** → **Доделе улога**.
3. Тражите своје име → потврдите да је наведено **Foundry User** (или наслеђена ознака **Azure AI User**).
4. Ако недостаје: **Додај** → **Додај доделу улоге** → претражите **Foundry User** → доделите свом рачуну.

Погледајте документацију [RBAC за Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) за детаље.

### Распоређивање модела није доступно

Ако агент враћа грешке везане за модел:

1. Потврдите да је модел распоређен: Foundry бочни мени → проширите пројекат → **Models** → проверите постојање `gpt-4.1-mini` (или вашег модела) са статусом **Succeeded**.
2. Потврдите да се име распоређивања поклапа: упоредите `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` (или `agent.yaml`) са стварним именом распоређивања у бочном менију.
3. Ако је распоређивање истекло (бесплатни ниво): поново распоредите из [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Проблеми са Foundry Local (Пут Б)

### Foundry Local сервис није покренут

```powershell
# Проверите статус
foundry local status

# Покрените услугу ако је заустављена
foundry local start
```

| Симптом | Узрок | Исправка |
|---------|-------|---------|
| Health check враћа `503` | Сервис није покренут | Покрените `foundry local start` или кликните **Start** у Foundry Toolkit бочном менију |
| Health check истекне | Модел се још учитава | Причекајте 30–60 с након покретања; већи модели траже више времена |
| `StatusCode: 404` на `/v1/health` | Погрешан порт | Подразумевани је `5273`. Проверите `foundry local status` за стварни порт |
| Недовољно ресурса | Foundry Local захтева око 4 ГБ RAM слободно | Затворите друге апликације |
| Преузимање модела не успева | Мало слободног простора на диску | Модели су 2–8 ГБ. Ослободите простор, затим `foundry model pull <name>` |

### Неслагање имена модела

```powershell
# Наведи преузете моделе и њихове тачне алијасе
foundry model list
```

Поставите `AZURE_AI_MODEL_DEPLOYMENT_NAME` у `.env` на тачан алијас приказан (нпр. `phi-4-mini`, не `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` при локалном покретању (Пут Б)

Лабораторијски `main.py` користи `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local захтева да ова променљива показује на локални сервис - **не** на `AZURE_AI_PROJECT_ENDPOINT`. Уверите се да ваш `.env` садржи:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP алат ипак прави одлазни позив (Пут Б)

Ово је очекивано. Алат `search_microsoft_learn_for_plan` добија ресурсе учења са `https://learn.microsoft.com/api/mcp`. **Само упит по имену вештине** путује преко мреже - резиме и текст JD обрађују се у потпуности на вашем уређају и никада се не преносе. Ако је потребан потпуни офлајн рад, додајте `try/except` резерву у алат која враћа статички `learn.microsoft.com` URL када крајња тачка није доступна.

---

## Добијање помоћи

Ако сте заглављени након што сте пробали горе наведене исправке:

1. **Проверите логове сервера** - Већина грешака производи Python стек трагове у терминалу. Прочитајте цео трејсбек.
2. **Претражите поруку о грешци** - Копирајте текст грешке и претражите у [Microsoft Q&A за Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Отворите issue** - Креирајте issue у [репозиторијуму радионице](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) са:
   - Поруком или снимком грешке
   - Верзијама ваших пакета (`pip list | Select-String "agent-framework"`)
   - Вашом Python верзијом (`python --version`)
   - Да ли је проблем локалан или после распоређивања

---

### Контролна тачка

- [ ] Знате како да проверите и поправите проблеме са `.env` конфигурацијом
- [ ] Можете потврдити да верзије пакета одговарају потребној матрици
- [ ] Знате како да проверите логове контејнера за неуспешна распоређивања
- [ ] Можете проверити RBAC улоге у Azure порталу

---

**Претходна:** [07 - Проверите у Playground-у](07-verify-in-playground.md) · **Следећа:** [09 - Резиме →](09-summary.md) · **Почетна:** [Lab 02 README](../README.md) · [Почетак радионице](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Изјава о одрицању одговорности**:
Овај документ је преведен коришћењем услуге за аутоматски превод [Co-op Translator](https://github.com/Azure/co-op-translator). Иако тежимо тачности, имајте у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитативним извором. За критичне информације препоручује се професионални људски превод. Нисмо одговорни за било каква неспоразума или погрешна тумачења која произилазе из коришћења овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->