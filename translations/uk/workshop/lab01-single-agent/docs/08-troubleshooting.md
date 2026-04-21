# Модуль 8 - Усунення несправностей

Цей модуль є довідником для усунення кожної поширеної проблеми під час воркшопу. Додайте його до закладок — ви повертатиметесь до нього, коли щось піде не так.

---

## 1. Помилки дозволів

### 1.1 Відмова в доступі `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Причина:** У вас немає ролі `Azure AI User` на рівні **проєкту**. Це найпоширеніша помилка на воркшопі.

**Виправлення - покроково:**

1. Відкрийте [https://portal.azure.com](https://portal.azure.com).
2. У рядку пошуку зверху введіть назву вашого **проєкту Foundry** (наприклад, `workshop-agents`).
3. **Важливо:** Клікніть результат, де тип **"Microsoft Foundry project"**, а НЕ батьківський обліковий запис/хаб ресурс. Це різні ресурси з різними областями дії RBAC.
4. В лівій навігації сторінки проєкту оберіть **Access control (IAM)**.
5. Клікніть вкладку **Role assignments**, щоб перевірити, чи у вас вже є роль:
   - Знайдіть своє ім’я або електронну пошту.
   - Якщо `Azure AI User` вже є → помилка має іншу причину (перевірте крок 8 нижче).
   - Якщо нема → продовжуйте додавати.
6. Клікніть **+ Add** → **Add role assignment**.
7. Вкладка **Role**:
   - Знайдіть [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Виберіть її зі списку.
   - Клікніть **Next**.
8. Вкладка **Members**:
   - Виберіть **User, group, or service principal**.
   - Клікніть **+ Select members**.
   - Знайдіть своє ім’я або email.
   - Відмітьте себе у результатах.
   - Клікніть **Select**.
9. Клікніть **Review + assign** → ще раз **Review + assign**.
10. **Зачекайте 1-2 хвилини** — зміни RBAC потребують часу для поширення.
11. Повторіть операцію, яка не виконалась.

> **Чому ролі Owner/Contributor недостатньо:** RBAC в Azure має два типи дозволів — *управління* і *дії з даними*. Власник і учасник дають управлінські права (створення ресурсів, редагування), але операції агента потребують `agents/write` **дії з даними**, яка є лише у ролях `Azure AI User`, `Azure AI Developer` або `Azure AI Owner`. Див. [документацію Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` під час створення ресурсу

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Причина:** У вас немає дозволу створювати або змінювати ресурси Azure у даній підписці/групі ресурсів.

**Виправлення:**
1. Попросіть адміністратора вашої підписки надати вам роль **Contributor** на групі ресурсів, де розміщений ваш проєкт Foundry.
2. Або нехай вони створять проєкт Foundry для вас і нададуть роль **Azure AI User** на проєкті.

### 1.3 `SubscriptionNotRegistered` для [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Причина:** Підписка Azure не зареєструвала постачальника ресурсів, потрібного для Foundry.

**Виправлення:**

1. Відкрийте термінал і виконайте:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```

2. Чекайте на завершення реєстрації (може зайняти 1-5 хвилин):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Очікуваний вивід: `"Registered"`
3. Повторіть операцію.

---

## 2. Помилки Docker (лише якщо Docker встановлений)

> Docker є **опційним** для цього воркшопу. Ці помилки стосуються випадків, коли у вас встановлено Docker Desktop і розширення Foundry намагається локально зібрати контейнер.

### 2.1 Демон Docker не працює

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Виправлення - покроково:**

1. Знайдіть Docker Desktop у меню Пуск (Windows) або у папці Applications (macOS) і запустіть його.
2. Зачекайте, доки вікно Docker Desktop покаже **"Docker Desktop is running"** — це зазвичай займає 30-60 секунд.
3. Перевірте наявність іконки Docker у системному треї (Windows) або у панелі меню (macOS). Наведіть на неї курсор, щоб побачити статус.
4. Перевірте в терміналі:
   ```powershell
   docker info
   ```
   Якщо виводиться інформація про систему Docker (Server Version, Storage Driver тощо), Docker працює.
5. **Для Windows:** Якщо Docker не запускається:
   - Відкрийте Docker Desktop → **Settings** (піктограма шестерні) → **General**.
   - Переконайтеся, що опція **Use the WSL 2 based engine** увімкнена.
   - Клікніть **Apply & restart**.
   - Якщо WSL 2 не встановлено, виконайте `wsl --install` у PowerShell з правами адміністратора і перезавантажте ПК.
6. Повторіть розгортання.

### 2.2 Збірка Docker не вдається через помилки залежностей

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Виправлення:**
1. Відкрийте `requirements.txt` і переконайтеся, що всі назви пакетів написані правильно.
2. Перевірте правильність фіксації версій:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```

3. Випробуйте встановлення локально спочатку:
   ```bash
   pip install -r requirements.txt
   ```

4. Якщо застосовуєте приватний пакетний індекс, переконайтеся, що Docker має до нього мережевий доступ.

### 2.3 Несумісність платформи контейнера (Apple Silicon)

Якщо ви розгортаєте з Mac на Apple Silicon (M1/M2/M3/M4), контейнер має бути збудований для `linux/amd64`, бо середовище виконання Foundry використовує AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Команда розгортання розширення Foundry зазвичай автоматично враховує це. Якщо виникають помилки, пов’язані з архітектурою, побудуйте вручну з параметром `--platform` і зверніться до команди Foundry.

---

## 3. Помилки автентифікації

### 3.1 Помилка отримання токена у [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview)

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Причина:** Жодне джерело облікових даних у ланцюжку `DefaultAzureCredential` не має дійсного токена.

**Виправлення - спробуйте кожен крок послідовно:**

1. **Повторно увійдіть в Azure CLI** (найпоширеніше рішення):
   ```bash
   az login
   ```
   Відкриється вікно браузера. Увійдіть і поверніться у VS Code.

2. **Встановіть правильну підписку:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Якщо це не потрібна підписка:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Повторний логін у VS Code:**
   - Клікніть по іконці **Accounts** (зображення людини) внизу зліва у VS Code.
   - Натисніть на ім’я акаунту → **Sign Out**.
   - Знову клікніть іконку акаунтів → **Sign in to Microsoft**.
   - Завершіть авторизацію через браузер.

4. **Service principal (тільки для CI/CD сценаріїв):**
   - Встановіть ці змінні оточення у вашому `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Потім перезапустіть процес агента.

5. **Перевірте кеш токенів:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Якщо це не вдається, термін дії токена CLI минув. Знову виконайте `az login`.

### 3.2 Токен працює локально, але не в хостованому розгортанні

**Причина:** Хостований агент використовує ідентичність, що керується системою, яка відрізняється від вашої особистої.

**Виправлення:** Це очікувана поведінка — керована ідентичність створюється автоматично під час розгортання. Якщо хостований агент все одно отримує помилки, перевірте:
1. Чи має керована ідентичність проєкту Foundry доступ до ресурсу Azure OpenAI.
2. Чи правильно вказаний `PROJECT_ENDPOINT` у `agent.yaml`.

---

## 4. Помилки моделей

### 4.1 Розгортання моделі не знайдено

```
Error: Model deployment not found / The specified deployment does not exist
```

**Виправлення - покроково:**

1. Відкрийте файл `.env` і запишіть значення `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Відкрийте бічну панель **Microsoft Foundry** у VS Code.
3. Розгорніть ваш проєкт → **Model Deployments**.
4. Порівняйте назву розгортання тут із значенням у `.env`.
5. Назви **чутливі до регістру** — `gpt-4o` і `GPT-4o` різні.
6. Якщо не співпадають, оновіть `.env`, щоб використовувати точну назву з панелі.
7. Для хостованого розгортання оновіть також `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Модель відповідає неочікуваним вмістом

**Виправлення:**
1. Перегляньте константу `EXECUTIVE_AGENT_INSTRUCTIONS` у `main.py`. Переконайтеся, що вона не була вкорочена або пошкоджена.
2. Перевірте налаштування "температури" моделі (якщо доступне) — нижчі значення дають більш детерміновані результати.
3. Порівняйте модель, що розгорнута (наприклад, `gpt-4o` проти `gpt-4o-mini`) — різні моделі мають різні можливості.

---

## 5. Помилки розгортання

### 5.1 Авторизація при завантаженні з ACR

```
Error: AcrPullUnauthorized
```

**Причина:** Керована ідентичність проєкту Foundry не може завантажити образ контейнера з Azure Container Registry.

**Виправлення - покроково:**

1. Відкрийте [https://portal.azure.com](https://portal.azure.com).
2. У рядку пошуку зверху знайдіть **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Оберіть реєстр, пов’язаний з вашим проєктом Foundry (зазвичай він у тій же групі ресурсів).
4. У лівій навігації натисніть **Access control (IAM)**.
5. Натисніть **+ Add** → **Add role assignment**.
6. Знайдіть і виберіть **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Клікніть **Next**.
7. Оберіть **Managed identity** → натисніть **+ Select members**.
8. Знайдіть і виберіть керовану ідентичність вашого проєкту Foundry.
9. Клікніть **Select** → **Review + assign** → **Review + assign**.

> Зазвичай цю роль налаштовує автоматично розширення Foundry. Якщо ви бачите цю помилку, автоматичне налаштування могло не спрацювати. Спробуйте також повторно розгорнути — розширення може повторити налаштування.

### 5.2 Агент не запускається після розгортання

**Симптоми:** Стан контейнера залишається "Pending" понад 5 хвилин або показує "Failed".

**Виправлення - покроково:**

1. Відкрийте бічну панель **Microsoft Foundry** у VS Code.
2. Клікніть на ваш хостований агент → виберіть версію.
3. У панелі деталей перевірте **Container Details** → шукайте розділ або посилання **Logs**.
4. Прочитайте логи старту контейнера. Типові причини:

| Повідомлення журналу | Причина | Виправлення |
|---------------------|---------|-------------|
| `ModuleNotFoundError: No module named 'xxx'` | Відсутня залежність | Додайте у `requirements.txt` і розгорніть заново |
| `KeyError: 'PROJECT_ENDPOINT'` | Відсутня змінна оточення | Додайте змінну у `agent.yaml` під `env:` |
| `OSError: [Errno 98] Address already in use` | Конфлікт портів | Переконайтесь, що в `agent.yaml` є `port: 8088` і тільки один процес його використовує |
| `ConnectionRefusedError` | Агент не почав слухати | Перевірте `main.py` — виклик `from_agent_framework()` має виконуватись при запуску |

5. Виправте проблему, потім повторіть розгортання з [Модуль 6](06-deploy-to-foundry.md).

### 5.3 Таймаут розгортання

**Виправлення:**
1. Перевірте інтернет-з’єднання — Docker push може бути великим (>100MB для першого розгортання).
2. Якщо за корпоративним проксі, переконайтеся, що налаштування проксі в Docker Desktop коректні: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Спробуйте знову — мережеві перешкоди можуть спричинити тимчасові збої.

---

## 6. Короткий довідник: ролі RBAC

| Роль | Зазвичай застосовується | Що надає |
|------|------------------------|----------|
| **Azure AI User** | Проєкт | Дії з даними: створення, розгортання та виклик агентів (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Проєкт або обліковий запис | Дії з даними + створення проєктів |
| **Azure AI Owner** | Обліковий запис | Повний доступ + управління ролями |
| **Azure AI Project Manager** | Проєкт | Дії з даними + може призначати роль Azure AI User іншим |
| **Contributor** | Підписка/група ресурсів | Управлінські дії (створення/видалення ресурсів). **НЕ включає дії з даними** |
| **Owner** | Підписка/група ресурсів | Управлінські дії + керування ролями. **НЕ включає дії з даними** |
| **Reader** | Будь-яка | Доступ лише для читання управлінських даних |

> **Головне:** Ролі `Owner` і `Contributor` **не включають** дії з даними. Для операцій агента потрібна роль `Azure AI *`. Мінімальна роль для цього воркшопу — **Azure AI User** на рівні **проєкту**.

---

## 7. Контрольний список завершення воркшопу

Використайте це як фінальне підтвердження, що все виконано:

| № | Пункт | Модуль | Пройшли? |
|---|-------|--------|----------|
| 1 | Всі попередні умови встановлені та перевірені | [00](00-prerequisites.md) | |
| 2 | Встановлені Foundry Toolkit та розширення Foundry | [01](01-install-foundry-toolkit.md) | |
| 3 | Створено проєкт Foundry (або вибрано існуючий) | [02](02-create-foundry-project.md) | |
| 4 | Модель розгорнута (наприклад, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Роль користувача Azure AI призначена в масштабі проєкту | [02](02-create-foundry-project.md) | |
| 6 | Створено каркас проєкту для розміщеного агента (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` налаштовано з PROJECT_ENDPOINT та MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Інструкції агента налаштовані у main.py | [04](04-configure-and-code.md) | |
| 9 | Створено віртуальне оточення та встановлено залежності | [04](04-configure-and-code.md) | |
| 10 | Агент протестовано локально за допомогою F5 або терміналу (пройдено 4 базові тести) | [05](05-test-locally.md) | |
| 11 | Розгорнуто у Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Статус контейнера показує "Started" або "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Підтверджено у VS Code Playground (пройдено 4 базові тести) | [07](07-verify-in-playground.md) | |
| 14 | Підтверджено у Foundry Portal Playground (пройдено 4 базові тести) | [07](07-verify-in-playground.md) | |

> **Вітаємо!** Якщо всі пункти виконано, ви завершили весь воркшоп. Ви побудували розміщеного агента з нуля, протестували його локально, розгорнули в Microsoft Foundry та перевірили його в продакшені.

---

**Попередня:** [07 - Verify in Playground](07-verify-in-playground.md) · **Головна:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:  
Цей документ було перекладено за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли в результаті використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->