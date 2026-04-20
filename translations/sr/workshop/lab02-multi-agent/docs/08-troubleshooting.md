# Модул 8 - Решавање проблема (Вишеуљни агент)

Овај модул покрива уобичајене грешке, исправке и стратегије отклањања грешака специфичне за вишеуљни радни ток. За општа питања о Foundry распоређивању, погледајте и [Lab 01 водич за решавање проблема](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Брза референца: Грешка → Поправка

| Грешка / Симптом | Веројатни узрок | Поправка |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` фајл недостаје или вредности нису постављене | Креирајте `.env` са `PROJECT_ENDPOINT=<ваш-ендпоинт>` и `MODEL_DEPLOYMENT_NAME=<ваш-модел>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Виртуално окружење није активирано или зависности нису инсталиране | Покрените `.\.venv\Scripts\Activate.ps1` затим `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP пакет није инсталиран (недостаје у requirements) | Покрените `pip install mcp` или проверите да је у `requirements.txt` као транзитивна зависност |
| Агент почиње али враћа празан одговор | Неподударање `output_executors` или недостају ивице | Проверите `output_executors=[gap_analyzer]` и да све ивице постоје у `create_workflow()` |
| Само 1 gap card (остали недостају) | Упутства за GapAnalyzer непотпуна | Додајте `CRITICAL:` пасус у `GAP_ANALYZER_INSTRUCTIONS` - види [Модул 3](03-configure-agents.md) |
| Почетни резултат је 0 или одсутан | MatchingAgent није примио податке са горње стране | Проверите да постоје и `add_edge(resume_parser, matching_agent)` и `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP сервер је одбио позив алата | Проверите интернет конекцију. Покушајте отворити `https://learn.microsoft.com/api/mcp` у прегледачу. Поновите |
| Ни један Microsoft Learn URL у излазу | MCP алат није регистрован или је ендпоинт погрешан | Проверите `tools=[search_microsoft_learn_for_plan]` на GapAnalyzer и да је `MICROSOFT_LEARN_MCP_ENDPOINT` тачан |
| `Address already in use: port 8088` | Други процес користи порт 8088 | Покрените `netstat -ano \| findstr :8088` (Windows) или `lsof -i :8088` (macOS/Linux) и зауставите конфликтни процес |
| `Address already in use: port 5679` | Конфликт порта Debugpy | Зауставите друге debug сесије. Покрените `netstat -ano \| findstr :5679` да пронађете и убијете процес |
| Agent Inspector се не отвара | Сервер није у потпуности покренут или конфликт порта | Сачекајте "Server running" лог. Проверите да порт 5679 није заузет |
| `azure.identity.CredentialUnavailableError` | Није пријављен у Azure CLI | Покрените `az login` затим поново покрените сервер |
| `azure.core.exceptions.ResourceNotFoundError` | Model deployment не постоји | Проверите да `MODEL_DEPLOYMENT_NAME` одговара модели који је распоредио ваш Foundry пројекат |
| Статус контејнера "Failed" после распореда | Контејнер се срушио при покретању | Проверите логове контејнера у Foundry бочној траци. Често: недостаје env var или грешка при увозу |
| Равнотежа приказује "Pending" дуже од 5 минута | Контејнер споро покреће или ограничења ресурса | Сачекајте до 5 минута за вишеуљни (покреће 4 инстанце агената). Ако је још у статусу pending, проверите логове |
| `ValueError` из `WorkflowBuilder` | Неважећа конфигурација графа | Проверите да је `start_executor` постављен, `output_executors` је листа и нема цикличних ивица |

---

## Проблеми са окружењем и конфигурацијом

### Недостајуће или погрешне вредности у `.env`

`.env` фајл мора бити у `PersonalCareerCopilot/` директоријуму (на истом нивоу као `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Очекујени садржај `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Како пронаћи ваш PROJECT_ENDPOINT:** 
- Отворите **Microsoft Foundry** бочну траку у VS Code → кликните десним тастером на пројекат → **Copy Project Endpoint**. 
- Или идите на [Azure Portal](https://portal.azure.com) → ваш Foundry пројекат → **Overview** → **Project endpoint**.

> **Како пронаћи MODEL_DEPLOYMENT_NAME:** У Foundry бочној траци, проширите ваш пројекат → **Models** → пронађите име распореденог модела (нпр. `gpt-4.1-mini`).

### Преовлађујућа вредност у env променљивим

`main.py` користи `load_dotenv(override=False)`, што значи:

| Приоритет | Извор | Побеђује ако су оба постављена? |
|----------|--------|-------------------------------|
| 1 (највиши) | Променљива окружења шкоља | Да |
| 2 | `.env` фајл | Само ако шкољска променљива није подешена |

Ово значи да Foundry runtime env vars (постављене преко `agent.yaml`) имају приоритет над `.env` вредностима током хостованог распореда.

---

## Компатибилност верзија

### Матрица верзија пакета

Вишеуљни радни ток захтева специфичне верзије пакета. Незадовољавајуће верзије изазивају грешке при извршавању.

| Пакет | Потребна верзија | Команда за проверу |
|---------|-----------------|-------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | најновији пред-издање | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Честе грешке везане за верзије

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Поправка: надоградња на rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` није пронађен или Inspector није компатибилан:**

```powershell
# Поправка: инсталација са --pre опцијом
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Поправка: надоградња mcp пакета
pip install mcp --upgrade
```

### Проверите све верзије одједном

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Очекујани излаз:

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

## Проблеми са MCP алатом

### MCP алат не враћа резултате

**Симптом:** Gap картице кажу "No results returned from Microsoft Learn MCP" или "No direct Microsoft Learn results found".

**Могући узроци:**

1. **Мрежни проблем** - MCP ендпоинт (`https://learn.microsoft.com/api/mcp`) није доступан.
   ```powershell
   # Тестирај повезаност
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Ако врати `200`, ендпоинт је доступан.

2. **Превише специфичан упит** - Име вештине је превише ниша за Microsoft Learn претрагу.
   - Ово је очекивано за веома специјализоване вештине. Алат има резервни URL у одговору.

3. **Истек сесије MCP** - Streamable HTTP веза је истекла.
   - Поновите захтев. MCP сесије су ефермерне и могу захтевати поновно повезивање.

### Објашњење MCP логова

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Лог | Значење | Акција |
|-----|---------|--------|
| `GET → 405` | MCP клијент провера током иницијализације | Нормално - игноришите |
| `POST → 200` | Позив алата успео | Очекујемо |
| `DELETE → 405` | MCP клијент провера током чишћења | Нормално - игноришите |
| `POST → 400` | Лош захтев (погрешан упит) | Проверите параметар `query` у `search_microsoft_learn_for_plan()` |
| `POST → 429` | Ограничење у броју позива | Сачекајте и покушајте поново. Смањите `max_results` параметар |
| `POST → 500` | Грешка сервера MCP | Привремена - понављајте захтеве. Ако траје, Microsoft Learn MCP API може бити недоступан |
| Тайм-аут везе | Мрежни проблем или MCP сервер није доступан | Проверите интернет. Покушајте `curl https://learn.microsoft.com/api/mcp` |

---

## Проблеми при распореду

### Контенер не успева да се покрене после распореда

1. **Проверите логове контејнера:**
   - Отворите **Microsoft Foundry** бочно траку → проширите **Hosted Agents (Preview)** → кликните на вашег агента → проширите верзију → **Container Details** → **Logs**.
   - Потражите Python traceback или грешке о недостајућим модулима.

2. **Чести узроци неуспеха покретања контејнера:**

   | Грешка у логовима | Узрок | Поправка |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` недостаје пакет | Додајте пакет и поново распоредите |
   | `RuntimeError: Missing required environment variable` | env променљиве нису постављене у `agent.yaml` | Ажурирајте `environment_variables` у `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity није конфигурисан | Foundry то подешава аутоматски - уверите се да распоређујете преко екстензије |
   | `OSError: port 8088 already in use` | Dockerfile излаже погрешан порт или постоји конфликт порта | Проверите `EXPOSE 8088` у Dockerfile и `CMD ["python", "main.py"]` |
   | Контенер излази са кодом 1 | Несанирана изузетна ситуација у `main()` | Тестирајте локално прво ([Модул 5](05-test-locally.md)) да ухватите грешке пре распореда |

3. **Поново распоредите након исправке:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → изаберите исти агент → распореди нову верзију.

### Распоред траје превише

Више агентски контејнери трају дуже за покретање јер креирају 4 инстанце агената при покретању. Нормално време покретања:

| Фаза | Очекивано трајање |
|-------|------------------|
| Изградња слика контејнера | 1-3 минута |
| Пуш слика у ACR | 30-60 секунди |
| Покретање контејнера (један агент) | 15-30 секунди |
| Покретање контејнера (више агената) | 30-120 секунди |
| Агент доступан у Playground-у | 1-2 минута након "Started" |

> Ако статус "Pending" траје дуже од 5 минута, проверите логове контејнера за грешке.

---

## RBAC и проблеми са дозволама

### `403 Forbidden` или `AuthorizationFailed`

Потребна вам је **[Azure AI User](https://aka.ms/foundry-ext-project-role)** улога на вашем Foundry пројекту:

1. Идите на [Azure Portal](https://portal.azure.com) → ресурс вашег Foundry **пројекта**.
2. Кликните **Access control (IAM)** → **Role assignments**.
3. Претражите ваше име → проверите да ли је наведена улога **Azure AI User**.
4. Ако недостаје: **Add** → **Add role assignment** → претражите **Azure AI User** → доделите вашем налогу.

Погледајте документацију за [RBAC у Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) за детаље.

### Недоступност распоређеног модела

Ако агент враћа грешке везане за модел:

1. Проверите да је модел распоређен: Foundry бочна трака → проширите пројекат → **Models** → проверите да ли `gpt-4.1-mini` (или ваш модел) има статус **Succeeded**.
2. Проверите да име распореда одговара: упоредите `MODEL_DEPLOYMENT_NAME` у `.env` (или `agent.yaml`) са стварним именом распореда у бочној траци.
3. Ако је распоред истекао (бесплатни ниво): поново распоредите из [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Проблеми са Agent Inspector-ом

### Inspector се отвара али приказује "Disconnected"

1. Проверите да ли сервер ради: потражите "Server running on http://localhost:8088" у терминалу.
2. Проверите порт `5679`: Inspector се повезује преко debugpy на порт 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Поново покрените сервер и отворите Inspector поново.

### Inspector приказује делимичан одговор

Вишеуљни одговори су дужи и пристижу струјно постепено. Сачекајте да се цео одговор заврши (може трајати 30-60 секунди зависно од броја gap картица и MCP позива).

Ако је одговор често скраћен:
- Проверите да упутства GapAnalyzer садрже `CRITICAL:` блок који спречава спајање gap картица.
- Проверите лимит токена вашег модела - `gpt-4.1-mini` подржава до 32К излазних токена, што би требало бити довољно.

---

## Савети за перформансе

### Спори одговори

Вишеуљни радни токови су у природи спорији од појединачних агената због секвенцијалних зависности и MCP позива.

| Оптимизација | Како | Утицај |
|-------------|-----|--------|
| Смањити број MCP позива | Смањити параметар `max_results` у алату | Мање HTTP позива |
| Поједноставити упутства | Краткији, фокусираније агенске поруке | Бржи LLM inferencing |
| Користити `gpt-4.1-mini` | Бржи од `gpt-4.1` за развој | Око 2 пута брже |
| Смањити детаљност gap картица | Поједноставити формат gap картица у упутствима GapAnalyzer-а | Мање генерисаног излаза |

### Типично време одговора (локално)

| Конфигурација | Очекивано време |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap картица | 30-60 секунди |
| `gpt-4.1-mini`, 8+ gap картица | 60-120 секунди |
| `gpt-4.1`, 3-5 gap картица | 60-120 секунди |
---

## Добијање помоћи

Ако сте заглављени након испробавања горе поменутих исправки:

1. **Проверите логове сервера** - Већина грешака производи Python stack traceback у терминалу. Прочитајте цео traceback.
2. **Претражите поруку о грешци** - Копирајте текст грешке и претражите на [Microsoft Q&A за Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Отворите питање** - Креирајте issue у [workshop репозиторијуму](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) са:
   - Поруком о грешци или снимком екрана
   - Верзијама пакета (`pip list | Select-String "agent-framework"`)
   - Ваша Python верзија (`python --version`)
   - Да ли је проблем локалан или након деплоyмента

---

### Контролна тачка

- [ ] Можете идентификовати и поправити најчешће више-агентске грешке користећи брзу референтну табелу
- [ ] Знате како да проверите и исправите `.env` конфигурационе проблеме
- [ ] Можете проверити да ли верзије пакета одговарају потребној матрици
- [ ] Разумете MCP записе у логовима и можете дијагностиковати неуспехе алата
- [ ] Знате како да проверите логове контејнера за грешке у деплоyменту
- [ ] Можете проверити RBAC улоге у Azure Порталу

---

**Претходно:** [07 - Verify in Playground](07-verify-in-playground.md) · **Почетна:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Искључење одговорности**:
Овај документ је преведен коришћењем AI сервиса за превод [Co-op Translator](https://github.com/Azure/co-op-translator). Иако тежимо прецизности, молимо имајте на уму да аутоматизовани преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитетним извором. За критичне информације препоручује се професионални људски превод. Нисмо одговорни за било каква неспоразума или погрешна тумачења која могу произићи из коришћења овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->