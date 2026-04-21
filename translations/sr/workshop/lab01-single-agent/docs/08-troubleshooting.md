# Модул 8 - Решавање проблема

Овај модул је референтни водич за сваки уобичајени проблем који се јавља током радионице. Додајте га у обележиваче - враћаћете му се кад год нешто крене наопако.

---

## 1. Грешке у дозволама

### 1.1 Одбијено `agents/write` овлашћење

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Основни узрок:** Немате улогу `Azure AI User` на нивоу **пројекта**. Ово је најчешћа грешка на радионици.

**Поправка - корак по корак:**

1. Отворите [https://portal.azure.com](https://portal.azure.com).
2. У горњој траци за претрагу укуцајте име вашег **Foundry пројекта** (нпр. `workshop-agents`).
3. **Критично:** Кликните резултат који показује тип **"Microsoft Foundry project"**, НЕ родитељски налог/ресурс хаба. Ово су различити ресурси са различитим RBAC опсезима.
4. У левој навигацији странице пројекта кликните **Access control (IAM)**.
5. Кликните картицу **Role assignments** да проверите да ли већ имате улогу:
   - Претражите по имену или имејлу.
   - Ако је `Azure AI User` већ наведен → грешка је из другог разлога (погледајте корак 8 доле).
   - Ако није наведен → наставите са додавањем.
6. Кликните **+ Add** → **Add role assignment**.
7. У картици **Role**:
   - Претражите [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Изаберите га са резултата.
   - Кликните **Next**.
8. У картици **Members**:
   - Изаберите **User, group, or service principal**.
   - Кликните **+ Select members**.
   - Претражите своје име или имејл адресу.
   - Изаберите себе са резултата.
   - Кликните **Select**.
9. Кликните **Review + assign** → поново **Review + assign**.
10. **Сачекајте 1-2 минута** - RBAC промене захтевају време за пропагацију.
11. Покушајте поново операцију која је пропала.

> **Зашто Owner/Contributor није довољно:** Azure RBAC има две врсте дозвола - *управљачке акције* и *акције над подацима*. Owner и Contributor дозвољавају управљачке акције (креирање ресурса, измену подешавања), али операције агента захтевају `agents/write` **акцију над подацима**, која је укључена само у улогама `Azure AI User`, `Azure AI Developer` или `Azure AI Owner`. Погледајте [Foundry RBAC документацију](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` приликом постављања ресурса

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Основни узрок:** Немате овлашћење да креирате или модификујете Azure ресурсе у овом претплатном плану/ресурсној групи.

**Поправка:**
1. Затражите од администратора претплате да вам додели улогу **Contributor** на ресурсној групи где се налази ваш Foundry пројекат.
2. Алтернативно, замолите да вам они креирају Foundry пројекат и доделе вам улогу **Azure AI User** на пројекту.

### 1.3 `SubscriptionNotRegistered` за [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Основни узрок:** Azure претплата није регистровала провајдера ресурса потребног за Foundry.

**Поправка:**

1. Отворите терминал и покрените:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Сачекајте да се регистрација заврши (може трајати 1-5 минута):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Очекујани исход: `"Registered"`
3. Покушајте поново операцију.

---

## 2. Docker грешке (само ако је Docker инсталиран)

> Docker је **опционо** за ову радионицу. Ове грешке важe само ако имате инсталиран Docker Desktop и Foundry екстензија покушава локално да гради контејнер.

### 2.1 Docker демон не ради

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Поправка - корак по корак:**

1. Пронађите Docker Desktop у Start менију (Windows) или Applications (macOS) и покрените га.
2. Сачекајте да се појави прозор Docker Desktop са поруком **"Docker Desktop is running"** - обично траје 30-60 секунди.
3. Потражите иконицу Docker кита у системској траци (Windows) или мени бару (macOS). Пређите мишем преко ње да прегледате статус.
4. Проверите у терминалу:
   ```powershell
   docker info
   ```
   Ако ово испише информације о Docker систему (Server Version, Storage Driver и сл.), Docker ради.
5. **Специфично за Windows:** Ако Docker и даље не креће:
   - Отворите Docker Desktop → **Settings** (икона зупчаника) → **General**.
   - Проверите да је означено **Use the WSL 2 based engine**.
   - Кликните **Apply & restart**.
   - Ако WSL 2 није инсталиран, покрените `wsl --install` у повишеном PowerShell-у и рестартујте рачунар.
6. Поново покушајте са постављањем.

### 2.2 Docker build пада због грешака у зависностима

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Поправка:**
1. Отворите `requirements.txt` и проверите да ли су сви називи пакета исправно написани.
2. Уверите се да је верзија правилно фиксна:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Прво тестирате локалну инсталацију:
   ```bash
   pip install -r requirements.txt
   ```
4. Ако користите приватни пакет индекс, уверите се да Docker има мрежни приступ њему.

### 2.3 Неслагање платформе контејнера (Apple Silicon)

Ако деплојујете са Apple Silicon Mac (M1/M2/M3/M4), контејнер мора бити изграђен за `linux/amd64` јер Foundry окruženје користи AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Deploy команда из Foundry екстензије аутоматски обрађује ово у већини случајева. Ако видите грешке везане за архитектуру, направите build ручно са `--platform` опцијом и контактирајте тим Foundry.

---

## 3. Грешке у аутентификацији

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) не успева да добије токен

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Основни узрок:** Ниједан од извора креденцијала у ланцу `DefaultAzureCredential` нема валидан токен.

**Поправка - испробајте кораке редом:**

1. **Поново се пријавите преко Azure CLI** (најчешће решење):
   ```bash
   az login
   ```
   Отвориће се прозор прегледача. Пријавите се, па се вратите у VS Code.

2. **Подесите исправну претплату:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Ако ово није исправна претплата:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Поново се пријавите преко VS Code-а:**
   - Кликните на икону **Accounts** (личица) у доњем левом углу VS Code-а.
   - Кликните име налога → **Sign Out**.
   - Поново кликните на икону акаунта → **Sign in to Microsoft**.
   - Завршите пријаву преко прегледача.

4. **Service principal (само за CI/CD сценарије):**
   - Поставите ове environment варијабле у `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Затим рестартујте агент процес.

5. **Проверите кеш токена:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Ако ово не успе, ваш CLI токен је истекао. Поново покрените `az login`.

### 3.2 Токен ради локално али не и на хостованом деплоју

**Основни узрок:** Хостовани агент користи системски управљани идентитет, који је другачији од вашег личног креденцијала.

**Поправка:** Ово је очекивано понашање - управљани идентитет се аутоматски креира током деплоја. Ако хостовани агент и даље има грешке у аутентификацији:
1. Проверите да ли управљани идентитет Foundry пројекта има приступ Azure OpenAI ресурсу.
2. Уверите се да је `PROJECT_ENDPOINT` у `agent.yaml` исправан.

---

## 4. Грешке у моделу

### 4.1 Није пронађено постављање модела

```
Error: Model deployment not found / The specified deployment does not exist
```

**Поправка - корак по корак:**

1. Отворите ваш `.env` фајл и забележите вредност `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Отворите **Microsoft Foundry** бочну траку у VS Code.
3. Проширите ваш пројекат → **Model Deployments**.
4. Упоредите име постављања са `.env` вредношћу.
5. Име је **осетљиво на величину слова** - `gpt-4o` није исто као `GPT-4o`.
6. Ако не поклапају, ажурирајте `.env` да користи тачно име које видите у бочној траци.
7. За хостовани деплој, такође ажурирајте `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Модел даје неочекивани одговор

**Поправка:**
1. Прегледајте константу `EXECUTIVE_AGENT_INSTRUCTIONS` у `main.py`. Уверите се да није скраћена или оштећена.
2. Проверите подешавање температуре модела (ако је конфигуришуће) - ниже вредности дају детерминистичкије резултате.
3. Упоредите који модел је постављен (нпр. `gpt-4o` против `gpt-4o-mini`) - различити модели имају различите могућности.

---

## 5. Грешке у деплоју

### 5.1 ACR pull овлашћење

```
Error: AcrPullUnauthorized
```

**Основни узрок:** Управљани идентитет Foundry пројекта не може преузети слику контејнера са Azure Container Registry.

**Поправка - корак по корак:**

1. Отворите [https://portal.azure.com](https://portal.azure.com).
2. У горњој траци за претрагу потражите **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Кликните на регистри који је повезан са вашим Foundry пројектом (обично у истој ресурсној групи).
4. У левој навигацији кликните **Access control (IAM)**.
5. Кликните **+ Add** → **Add role assignment**.
6. Потражите и изаберите **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Кликните **Next**.
7. Изаберите **Managed identity** → кликните **+ Select members**.
8. Пронађите и одаберите управљани идентитет Foundry пројекта.
9. Кликните **Select** → **Review + assign** → **Review + assign**.

> Ова улога се обично аутоматски подешава преко Foundry екстензије. Ако видите ову грешку, аутоматска конфигурација можда није успела. Можете покушати поновно постављање - екстензија ће можда поновити подешавање.

### 5.2 Агент не може да се покрене након деплоја

**Симптоми:** Статус контејнера остаје "Pending" дуже од 5 минута или показује "Failed".

**Поправка - корак по корак:**

1. Отворите **Microsoft Foundry** бочну траку у VS Code.
2. Кликните на ваш хостовани агент → изаберите верзију.
3. У панелу за детаље проверите **Container Details** → потражите одељак или линк за **Logs**.
4. Прочитајте логове покретања контејнера. Чести разлози:

| Порука у логовима | Узрок | Поправка |
|-------------------|--------|----------|
| `ModuleNotFoundError: No module named 'xxx'` | Недостаје зависност | Додајте је у `requirements.txt` и поново деплојујте |
| `KeyError: 'PROJECT_ENDPOINT'` | Недостаје environment варијабла | Додајте варијаблу у `agent.yaml` под `env:` |
| `OSError: [Errno 98] Address already in use` | Конфликт портова | У `agent.yaml` користите `port: 8088` и осигурајте да само један процес користи тај порт |
| `ConnectionRefusedError` | Агент није почео да слуша | Проверите `main.py` - позив `from_agent_framework()` мора да се изврши при покретању |

5. Исправите проблем, па поново деплојујте из [Модула 6](06-deploy-to-foundry.md).

### 5.3 Постављање истекло

**Поправка:**
1. Проверите интернет конекцију - Docker push може бити велик (>100MB за први деплој).
2. Ако сте иза корпоративног проксија, уверите се да су Docker Desktop proxy подешавања конфигурисана: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Покушајте поново - мрежни проблеми могу изазвати привремене неуспехе.

---

## 6. Брза референца: RBAC улоге

| Улога | Типичан опсег | Шта омогућава |
|-------|--------------|----------------|
| **Azure AI User** | Пројекат | Акције над подацима: креирање, деплој и позив агената (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Пројекат или налог | Акције над подацима + креирање пројеката |
| **Azure AI Owner** | Налог | Потпуни приступ + управљање улогама |
| **Azure AI Project Manager** | Пројекат | Акције над подацима + може додељивати Azure AI User другима |
| **Contributor** | Претплата/ресурсна група | Управљачке акције (креирање/брисање ресурса). **НЕ укључује акције над подацима** |
| **Owner** | Претплата/ресурсна група | Управљачке акције + управљање улогама. **НЕ укључује акције над подацима** |
| **Reader** | Било који | Само читање управљачког приступа |

> **Кључна напомена:** `Owner` и `Contributor` НЕ укључују акције над подацима. За рад агената увек вам треба нека `Azure AI *` улога. Минимална улога за ову радионицу је **Azure AI User** на нивоу **пројекта**.

---

## 7. Контролна листа за завршетак радионице

Користите ово као завршни потпис да сте све завршили:

| # | Ставка | Модул | Прошао? |
|---|--------|-------|---------|
| 1 | Сви предуслови инсталирани и проверени | [00](00-prerequisites.md) | |
| 2 | Инсталирани Foundry Toolkit и Foundry екстензије | [01](01-install-foundry-toolkit.md) | |
| 3 | Креиран Foundry пројекат (или изабран постојећи) | [02](02-create-foundry-project.md) | |
| 4 | Модел постављен у рад (нпр. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Ролa корисника Azure AI додељена на обиму пројекта | [02](02-create-foundry-project.md) | |
| 6 | Скелеон пројекта са хостованим агентом (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` конфигурисан са PROJECT_ENDPOINT и MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Упутства за агента прилагођена у main.py | [04](04-configure-and-code.md) | |
| 9 | Виртуелно окружење креирано и зависности инсталиране | [04](04-configure-and-code.md) | |
| 10 | Агент тестиран локално помоћу F5 или терминала (прошла 4 дымна теста) | [05](05-test-locally.md) | |
| 11 | Постављено у Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Статус контејнера приказује "Started" или "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Потврђено у VS Code Playground (прошла 4 дымна теста) | [07](07-verify-in-playground.md) | |
| 14 | Потврђено у Foundry Portal Playground (прошла 4 дымна теста) | [07](07-verify-in-playground.md) | |

> **Честитамо!** Ако су све ставке означене, завршили сте целу радионицу. Креирали сте хостованог агента од нуле, тестирали га локално, поставили га у Microsoft Foundry и верификовали га у продукцији.

---

**Претходно:** [07 - Verify in Playground](07-verify-in-playground.md) · **Почетна:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ограничење одговорности**:  
Овај документ је преведен коришћењем AI преводилачке услуге [Co-op Translator](https://github.com/Azure/co-op-translator). Иако тежимо прецизности, имајте у виду да аутоматски преводи могу садржати грешке или нетачности. Изворни документ на свом изворном језику треба сматрати ауторитетним извором. За критичне информације препоручује се стручни људски превод. Нисмо одговорни за било каква неспоразума или погрешне тумачења која произилазе из употребе овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->