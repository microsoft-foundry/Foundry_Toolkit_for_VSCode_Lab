# Modul 8 - Řešení problémů

Tento modul je referenční příručka pro všechny běžné problémy, na které během workshopu narazíte. Uložte si ho do záložek – budete se k němu vracet vždy, když něco nebude fungovat.

---

## 1. Chybové hlášky ohledně oprávnění

### 1.1 Zamítnutí oprávnění `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Hlavní příčina:** Nemáte přiřazenou roli `Azure AI User` na úrovni **projektu**. Toto je nejběžnější chyba ve workshopu.

**Řešení krok za krokem:**

1. Otevřete [https://portal.azure.com](https://portal.azure.com).
2. Do horního vyhledávacího pole napište název vašeho **Foundry projektu** (např. `workshop-agents`).
3. **Důležité:** Klikněte na výsledek, který má typ **"Microsoft Foundry project"**, NE na mateřský účet/hub. Jedná se o různé zdroje s různými rozsahy RBAC.
4. V levém navigačním menu stránky projektu klikněte na **Access control (IAM)**.
5. Klikněte na záložku **Role assignments** a zkontrolujte, zda již máte roli:
   - Vyhledejte své jméno nebo e-mail.
   - Pokud je `Azure AI User` již uveden → chyba má jiný důvod (viz krok 8 níže).
   - Pokud není uveden → pokračujte v přidání role.
6. Klikněte na **+ Add** → **Add role assignment**.
7. V záložce **Role**:
   - Vyhledejte [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Vyberte ji z výsledků.
   - Klikněte na **Next**.
8. V záložce **Members**:
   - Vyberte **User, group, or service principal**.
   - Klikněte na **+ Select members**.
   - Vyhledejte své jméno nebo e-mailovou adresu.
   - Vyberte se ze seznamu.
   - Klikněte na **Select**.
9. Klikněte na **Review + assign** → znovu **Review + assign**.
10. **Počkejte 1-2 minuty** - změny RBAC potřebují čas na propagaci.
11. Zkuste operaci, která selhala, znovu.

> **Proč není role Owner/Contributor dostatečná:** Azure RBAC rozlišuje dva typy oprávnění – *správní akce* a *datové akce*. Role Owner a Contributor udělují správní akce (vytváření zdrojů, úpravy nastavení), ale operace agenta vyžadují datovou akci `agents/write`, která je obsažená pouze v rolích `Azure AI User`, `Azure AI Developer` nebo `Azure AI Owner`. Více viz [Foundry RBAC dokumentace](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 Chyba `AuthorizationFailed` při vytváření zdroje

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Hlavní příčina:** Nemáte oprávnění vytvářet nebo upravovat Azure zdroje v tomto předplatném/skupině prostředků.

**Řešení:**
1. Požádejte správce předplatného, aby vám přiřadil roli **Contributor** ve skupině prostředků, kde je váš Foundry projekt.
2. Alternativně požádejte, aby vám vytvořil Foundry projekt a přiřadil vám roli **Azure AI User** na projektu.

### 1.3 Chyba `SubscriptionNotRegistered` pro [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Hlavní příčina:** Azure předplatné není zaregistrováno u poskytovatele zdrojů potřebného pro Foundry.

**Řešení:**

1. Otevřete terminál a spusťte:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Počkejte na dokončení registrace (může trvat 1-5 minut):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Očekávaný výstup: `"Registered"`
3. Zkuste operaci znovu.

---

## 2. Chybové hlášky Dockeru (pouze pokud je nainstalován Docker)

> Docker je pro tento workshop **volitelný**. Tyto chyby platí pouze pokud máte nainstalovaný Docker Desktop a rozšíření Foundry se pokouší o lokální build kontejneru.

### 2.1 Docker démon neběží

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Řešení krok za krokem:**

1. **Najděte Docker Desktop** v nabídce Start (Windows) nebo v Aplikacích (macOS) a spusťte ho.
2. Počkejte, až se v okně Docker Desktop zobrazí nápis **"Docker Desktop is running"** – obvykle to trvá 30–60 sekund.
3. Hledejte ikonu velryby Dockeru v systémové liště (Windows) nebo v menu baru (macOS). Najetím myši se zobrazí stav.
4. Ověřte v terminálu:
   ```powershell
   docker info
   ```
   Pokud se zobrazí informace o systému Docker (verze serveru, storage driver atd.), Docker běží.
5. **Specifické pro Windows:** Pokud Docker stále nenaběhne:
   - Otevřete Docker Desktop → **Settings** (ikona ozubeného kola) → **General**.
   - Ujistěte se, že je zaškrtnuto **Use the WSL 2 based engine**.
   - Klikněte na **Apply & restart**.
   - Pokud není nainstalován WSL 2, spusťte v PowerShellu s právy správce `wsl --install` a restartujte PC.
6. Zkuste deploy znovu.

### 2.2 Selhání docker build kvůli chybějícím závislostem

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Řešení:**
1. Otevřete `requirements.txt` a ověřte správnost názvů všech balíčků.
2. Ujistěte se, že jsou verze správně připnuty:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Nejprve otestujte instalaci lokálně:
   ```bash
   pip install -r requirements.txt
   ```
4. Pokud používáte soukromý index balíčků, ujistěte se, že Docker má k němu síťový přístup.

### 2.3 Nesoulad platformy kontejneru (Apple Silicon)

Pokud nasazujete z Apple Silicon Macu (M1/M2/M3/M4), musí být kontejner postaven pro `linux/amd64`, protože Foundry runtime používá AMD64 architekturu.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Rozšíření Foundry při deploy používá tento parametr automaticky ve většině případů. Pokud se objeví chyby související s architekturou, postavte kontejner ručně s příznakem `--platform` a kontaktujte tým Foundry.

---

## 3. Chyby autentizace

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) selže při získání tokenu

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Hlavní příčina:** Žádný zdroj přihlašovacích údajů v řetězci `DefaultAzureCredential` nemá platný token.

**Řešení - vyzkoušejte kroky v uvedeném pořadí:**

1. **Znovu se přihlaste přes Azure CLI** (nejčastější řešení):
   ```bash
   az login
   ```
   Otevře se okno prohlížeče. Přihlaste se, pak se vraťte do VS Code.

2. **Nastavte správné předplatné:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Pokud to není správné předplatné:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Znovu se přihlaste přes VS Code:**
   - Klikněte na ikonu **Účty** (postavička) vlevo dole ve VS Code.
   - Klikněte na své jméno → **Odhlásit se**.
   - Znovu klikněte na ikonu Účty → **Přihlásit se do Microsoft**.
   - Dokončete přihlašovací proces v prohlížeči.

4. **Service principal (pouze scénáře CI/CD):**
   - Nastavte tyto proměnné prostředí ve svém `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Poté restartujte proces agenta.

5. **Zkontrolujte cache tokenů:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Pokud to selže, vypršel vám token CLI. Znovu spusťte `az login`.

### 3.2 Token funguje lokálně, ale ne při hostovaném nasazení

**Hlavní příčina:** Hostovaný agent používá systémově spravovanou identitu, která se liší od vašeho osobního přihlašovacího údaje.

**Řešení:** Toto je očekávané chování – spravovaná identita se vytvoří automaticky během nasazení. Pokud hostovaný agent přesto dostává chyby autentizace:
1. Zkontrolujte, že spravovaná identita Foundry projektu má přístup k Azure OpenAI zdroji.
2. Ověřte správnost `PROJECT_ENDPOINT` v `agent.yaml`.

---

## 4. Chyby modelu

### 4.1 Modelová nasazení nenalezena

```
Error: Model deployment not found / The specified deployment does not exist
```

**Řešení krok za krokem:**

1. Otevřete svůj `.env` soubor a zapamatujte si hodnotu `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Otevřete postranní panel **Microsoft Foundry** ve VS Code.
3. Rozbalte svůj projekt → **Model Deployments**.
4. Porovnejte uvedený název nasazení s hodnotou v `.env`.
5. Název je **citlivý na velikost písmen** – `gpt-4o` není stejné jako `GPT-4o`.
6. Pokud se neshodují, aktualizujte v `.env` přesný název ze sidebaru.
7. Pro hostované nasazení také aktualizujte `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model odpovídá neočekávaným obsahem

**Řešení:**
1. Prohlédněte si konstantu `EXECUTIVE_AGENT_INSTRUCTIONS` v `main.py`. Ujistěte se, že nebyla zkrácena nebo poškozena.
2. Zkontrolujte nastavení teploty modelu (pokud lze nastavovat) – nižší hodnoty vedou k determinističtějším výstupům.
3. Porovnejte, který model je nasazen (např. `gpt-4o` vs `gpt-4o-mini`) – různé modely mají různé schopnosti.

---

## 5. Chyby nasazení

### 5.1 ACR autorizace pro pull

```
Error: AcrPullUnauthorized
```

**Hlavní příčina:** Spravovaná identita Foundry projektu nemůže stáhnout kontejnerový obraz z Azure Container Registry.

**Řešení krok za krokem:**

1. Otevřete [https://portal.azure.com](https://portal.azure.com).
2. Vyhledejte **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** v horním vyhledávání.
3. Klikněte na registr spojený s vaším Foundry projektem (obvykle ve stejné skupině prostředků).
4. V levém menu klikněte na **Access control (IAM)**.
5. Klikněte na **+ Add** → **Add role assignment**.
6. Vyhledejte a vyberte **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Klikněte na **Next**.
7. Vyberte **Managed identity** → klikněte na **+ Select members**.
8. Najděte a vyberte spravovanou identitu Foundry projektu.
9. Klikněte na **Select** → **Review + assign** → **Review + assign**.

> Toto přiřazení role je běžně nastaveno automaticky rozšířením Foundry. Pokud se tato chyba objeví, může být automatické nastavení chybné. Zkuste také znovu nasadit – rozšíření může automaticky opakovat konfiguraci.

### 5.2 Agent se po nasazení nespustí

**Příznaky:** Stav kontejneru zůstává déle než 5 minut na „Pending“ nebo je „Failed“.

**Řešení krok za krokem:**

1. Otevřete postranní panel **Microsoft Foundry** ve VS Code.
2. Klikněte na svého hostovaného agenta → vyberte verzi.
3. V panelu detailů zkontrolujte **Container Details** → hledejte sekci nebo odkaz **Logs**.
4. Přečtěte si startovací logy kontejneru. Časté příčiny:

| Text v logu | Příčina | Řešení |
|-------------|---------|--------|
| `ModuleNotFoundError: No module named 'xxx'` | Chybějící závislost | Přidejte ji do `requirements.txt` a nasaďte znovu |
| `KeyError: 'PROJECT_ENDPOINT'` | Chybějící environmentální proměnná | Přidejte proměnnou do `agent.yaml` pod `env:` |
| `OSError: [Errno 98] Address already in use` | Konflikt portu | Ujistěte se, že `agent.yaml` má `port: 8088` a žádný jiný proces port nepoužívá |
| `ConnectionRefusedError` | Agent neposlouchá | Zkontrolujte `main.py` - volání `from_agent_framework()` musí proběhnout při startu |

5. Opravte chybu a poté nasadte znovu podle [Modul 6](06-deploy-to-foundry.md).

### 5.3 Časový limit nasazení

**Řešení:**
1. Zkontrolujte připojení k internetu – push Dockeru může být velký (>100MB první nasazení).
2. Pokud jste za firemním proxy, nastavte proxy v Docker Desktop: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Zkuste znovu – výpadky sítě mohou způsobit krátkodobé chyby.

---

## 6. Rychlá reference: RBAC role

| Role | Typický rozsah | Co uděluje |
|------|----------------|------------|
| **Azure AI User** | Projekt | Datové akce: sestavení, nasazení a volání agentů (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt nebo účet | Datové akce + vytváření projektů |
| **Azure AI Owner** | Účet | Plný přístup + správa přiřazení rolí |
| **Azure AI Project Manager** | Projekt | Datové akce + může přiřazovat roli Azure AI User ostatním |
| **Contributor** | Předplatné/Skupina prostředků | Správní akce (vytváření/mazání zdrojů). **Nezahrnuje datové akce** |
| **Owner** | Předplatné/Skupina prostředků | Správní akce + správa rolí. **Nezahrnuje datové akce** |
| **Reader** | Jakýkoli | Pouze pro čtení správních zdrojů |

> **Klíčová poznámka:** Role `Owner` a `Contributor` **nezahrnují datové akce**. Pro operace s agenty vždy potřebujete roli `Azure AI *`. Minimální role pro tento workshop je **Azure AI User** na úrovni **projektu**.

---

## 7. Kontrolní seznam dokončení workshopu

Použijte jako finální potvrzení, že máte vše hotovo:

| # | Položka | Modul | Splněno? |
|---|---------|-------|----------|
| 1 | Všechny předpoklady nainstalovány a ověřeny | [00](00-prerequisites.md) | |
| 2 | Nainstalovány Foundry Toolkit a rozšíření Foundry | [01](01-install-foundry-toolkit.md) | |
| 3 | Vytvořen Foundry projekt (nebo vybrán existující projekt) | [02](02-create-foundry-project.md) | |
| 4 | Model nasazen (např. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Přiřazena role Azure AI User v rozsahu projektu | [02](02-create-foundry-project.md) | |
| 6 | Projekt hostovaného agenta připraven (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` nakonfigurován se PROJECT_ENDPOINT a MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instrukce agenta upraveny v main.py | [04](04-configure-and-code.md) | |
| 9 | Vytvořeno virtuální prostředí a nainstalovány závislosti | [04](04-configure-and-code.md) | |
| 10 | Agent otestován lokálně pomocí F5 nebo terminálu (4 úspěšné základní testy) | [05](05-test-locally.md) | |
| 11 | Nasazeno do Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Stav kontejneru zobrazuje "Started" nebo "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Ověřeno v VS Code Playground (4 úspěšné základní testy) | [07](07-verify-in-playground.md) | |
| 14 | Ověřeno ve Foundry Portal Playground (4 úspěšné základní testy) | [07](07-verify-in-playground.md) | |

> **Gratulujeme!** Pokud jsou všechny položky zaškrtnuté, dokončili jste celý workshop. Postavili jste hostovaného agenta od začátku, otestovali ho lokálně, nasadili do Microsoft Foundry a ověřili v produkci.

---

**Předchozí:** [07 - Verify in Playground](07-verify-in-playground.md) · **Domů:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Upozornění**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). I když usilujeme o přesnost, mějte prosím na paměti, že automatické překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho rodném jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nepřebíráme odpovědnost za jakékoli nedorozumění nebo nesprávné výklady vyplývající z použití tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->