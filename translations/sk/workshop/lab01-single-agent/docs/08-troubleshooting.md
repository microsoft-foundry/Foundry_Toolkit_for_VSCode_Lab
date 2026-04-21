# Modul 8 - Riešenie problémov

Tento modul je referenčným sprievodcom pre každý bežný problém, na ktorý môžete naraziť počas workshopu. Uložte si ho do záložiek – budete sa k nemu vracať vždy, keď niečo nebude fungovať.

---

## 1. Chyby oprávnení

### 1.1 Odmietnuté oprávnenie `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Hlavná príčina:** Nemáte priradenú rolu `Azure AI User` na úrovni **projektu**. Toto je najčastejšia chyba v workshope.

**Riešenie - krok za krokom:**

1. Otvorte [https://portal.azure.com](https://portal.azure.com).
2. Do vyhľadávacieho poľa hore zadajte názov svojho **Foundry projektu** (napr. `workshop-agents`).
3. **Dôležité:** Kliknite na výsledok, ktorý má typ **"Microsoft Foundry project"**, NIE na nadriadený účet/hub zdroj. Ide o rôzne zdroje s rôznymi rozsahmi RBAC.
4. V ľavom navigačnom paneli stránky projektu kliknite na **Access control (IAM)**.
5. Kliknite na kartu **Role assignments**, aby ste skontrolovali, či už máte rolu:
   - Vyhľadajte svoje meno alebo e-mail.
   - Ak je `Azure AI User` už uvedený → chyba má iný dôvod (skontrolujte krok 8 nižšie).
   - Ak nie je uvedený → pokračujte v pridávaní.
6. Kliknite na **+ Add** → **Add role assignment**.
7. Na karte **Role**:
   - Vyhľadajte [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Vyberte ju zo zoznamu.
   - Kliknite na **Next**.
8. Na karte **Members**:
   - Vyberte **User, group, or service principal**.
   - Kliknite na **+ Select members**.
   - Vyhľadajte svoje meno alebo e-mailovú adresu.
   - Vyberte sa zo zoznamu.
   - Kliknite na **Select**.
9. Kliknite na **Review + assign** → znovu **Review + assign**.
10. **Počkajte 1-2 minúty** - zmeny RBAC sa aplikujú s oneskorením.
11. Skúste znova operáciu, ktorá zlyhala.

> **Prečo roly Owner/Contributor nestačia:** Azure RBAC má dva typy oprávnení - *manažérske akcie* a *dátové akcie*. Owner a Contributor povoľujú manažérske akcie (vytváranie zdrojov, úprava nastavení), ale operácie s agentmi vyžadujú dátovú akciu `agents/write`, ktorá je zahrnutá iba v rolách `Azure AI User`, `Azure AI Developer` alebo `Azure AI Owner`. Viac informácií nájdete v [Foundry RBAC dokumentácii](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` počas poskytovania zdrojov

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Hlavná príčina:** Nemáte oprávnenie vytvárať alebo meniť Azure zdroje v tomto predplatnom/skupine prostriedkov.

**Riešenie:**
1. Požiadajte svojho administrátora predplatného, aby vám pridelil rolu **Contributor** na skupine zdrojov, kde sa nachádza váš Foundry projekt.
2. Alternatívne ho požiadajte, aby vám vytvoril Foundry projekt a pridelil rolu **Azure AI User** na projekte.

### 1.3 `SubscriptionNotRegistered` pre [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Hlavná príčina:** Azure predplatné nezaregistrovalo poskytovateľa zdrojov potrebného pre Foundry.

**Riešenie:**

1. Otvorte terminál a spustite:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Počkajte na dokončenie registrácie (môže trvať 1-5 minút):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Očakávaný výstup: `"Registered"`
3. Skúste operáciu znova.

---

## 2. Chyby Dockeru (len ak je Docker nainštalovaný)

> Docker je na tomto workshope **voliteľný**. Tieto chyby sa týkajú iba ak máte nainštalovaný Docker Desktop a rozšírenie Foundry sa pokúša o lokálnu stavbu kontajnera.

### 2.1 Docker daemon neběží

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Riešenie - krok za krokom:**

1. **Nájdite Docker Desktop** v Štart menu (Windows) alebo v Aplikáciách (macOS) a spustite ho.
2. Počkajte, kým okno Docker Desktop nezobrazí **"Docker Desktop is running"** – trvá to obvykle 30-60 sekúnd.
3. Skontrolujte ikonu veľryby Docker v systémovej lište (Windows) alebo menu bare (macOS). Najeďte myšou, aby ste videli stav.
4. Overte v termináli:
   ```powershell
   docker info
   ```
   Ak vypíše informácie o systéme Docker (Verzia servera, Storage Driver atď.), Docker beží.
5. **Špecifické pre Windows:** Ak Docker stále neštartuje:
   - Otvorte Docker Desktop → **Settings** (ikona ozubeného kolieska) → **General**.
   - Skontrolujte, či je zaškrtnutá možnosť **Use the WSL 2 based engine**.
   - Kliknite na **Apply & restart**.
   - Ak WSL 2 nie je nainštalované, spustite `wsl --install` v zvýšenom PowerShelli a reštartujte počítač.
6. Skúste nasadenie znova.

### 2.2 Docker build zlyháva s chybami závislostí

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Riešenie:**
1. Otvorte `requirements.txt` a skontrolujte, či sú všetky názvy balíkov správne napísané.
2. Uistite sa, že verzie sú správne pripnuté:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Najskôr otestujte inštaláciu lokálne:
   ```bash
   pip install -r requirements.txt
   ```
4. Ak používate privátny index balíkov, uistite sa, že Docker má k nemu sieťový prístup.

### 2.3 Nezhoda platformy kontajnera (Apple Silicon)

Ak nasadzujete z Macu s Apple Silicon (M1/M2/M3/M4), kontajner musí byť postavený pre `linux/amd64`, pretože runtime Foundry používa AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Príkaz deploy rozšírenia Foundry to väčšinou spraví automaticky. Ak sa zobrazia chyby súvisiace s architektúrou, zostavte kontajner manuálne s parametrom `--platform` a kontaktujte tím Foundry.

---

## 3. Chyby autentifikácie

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) zlyháva pri prístupe ku tokenu

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Hlavná príčina:** Žiaden z credential zdrojov v reťazci `DefaultAzureCredential` nemá platný token.

**Riešenie - vyskúšajte každý krok postupne:**

1. **Prihláste sa znova cez Azure CLI** (najčastejšie riešenie):
   ```bash
   az login
   ```
   Otvorí sa prehliadač. Prihláste sa a vráťte sa do VS Code.

2. **Nastavte správne predplatné:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Ak toto nie je správne predplatné:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Prihláste sa znova vo VS Code:**
   - Kliknite na ikonu **Accounts** (ikona osoby) dole vľavo vo VS Code.
   - Kliknite na svoje meno → **Sign Out**.
   - Kliknite opäť na ikonu účtov → **Sign in to Microsoft**.
   - Dokončite prihlasovací proces v prehliadači.

4. **Service principal (iba pre CI/CD prípady):**
   - Nastavte tieto environmentálne premenné vo vašom `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Potom reštartujte agent proces.

5. **Skontrolujte token cache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Ak zlyhá, platnosť vášho CLI tokenu vypršala. Spustite znova `az login`.

### 3.2 Token funguje lokálne, ale nie pri hosťovanom nasadení

**Hlavná príčina:** Hosťovaný agent používa systémovú spravovanú identitu, ktorá je iná než vaše osobné poverenie.

**Riešenie:** Toto je očakávané správanie - spravovaná identita sa automaticky vytvorí pri nasadení. Ak hosťovaný agent stále hlási chyby autentifikácie:
1. Skontrolujte, či má spravovaná identita Foundry projektu prístup k Azure OpenAI zdroju.
2. Overte, že `PROJECT_ENDPOINT` v `agent.yaml` je správny.

---

## 4. Chyby modelu

### 4.1 Nenájdené nasadenie modelu

```
Error: Model deployment not found / The specified deployment does not exist
```

**Riešenie - krok za krokom:**

1. Otvorte súbor `.env` a zapíšte si hodnotu `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Otvorte bočný panel **Microsoft Foundry** vo VS Code.
3. Rozbaľte svoj projekt → **Model Deployments**.
4. Porovnajte meno nasadenia uvedené tam s hodnotou v `.env`.
5. Názov je **s citlivosťou na veľkosť písmen** - `gpt-4o` nie je to isté ako `GPT-4o`.
6. Ak sa nezhodujú, upravte `.env`, aby obsahoval presný názov podľa bočného panela.
7. Pre hosťované nasadenie tiež upravte `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model odpovedá neočakávaným obsahom

**Riešenie:**
1. Skontrolujte konštantu `EXECUTIVE_AGENT_INSTRUCTIONS` v `main.py`. Uistite sa, že nebola skrátená alebo poškodená.
2. Skontrolujte nastavenie teploty modelu (ak je nakonfigurovateľné) – nižšie hodnoty vedú k deterministickejším výstupom.
3. Porovnajte nasadený model (napr. `gpt-4o` vs `gpt-4o-mini`) – rôzne modely majú rôzne schopnosti.

---

## 5. Chyby nasadenia

### 5.1 Autorizácia ťahania z ACR

```
Error: AcrPullUnauthorized
```

**Hlavná príčina:** Spravovaná identita Foundry projektu nemôže vytiahnuť image kontajnera z Azure Container Registry.

**Riešenie - krok za krokom:**

1. Otvorte [https://portal.azure.com](https://portal.azure.com).
2. Do vyhľadávacieho poľa hore zadajte **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Kliknite na registry priradený k vášmu Foundry projektu (väčšinou v tej istej skupine zdrojov).
4. V ľavom navigačnom paneli kliknite na **Access control (IAM)**.
5. Kliknite na **+ Add** → **Add role assignment**.
6. Vyhľadajte rolu **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** a vyberte ju. Kliknite na **Next**.
7. Vyberte **Managed identity** → kliknite na **+ Select members**.
8. Nájdite a vyberte spravovanú identitu Foundry projektu.
9. Kliknite na **Select** → **Review + assign** → **Review + assign**.

> Táto asignácia roly je zvyčajne nastavená automaticky rozšírením Foundry. Ak vidíte túto chybu, automatické nastavenie mohlo zlyhať. Môžete tiež skúsiť nasadenie zopakovať – rozšírenie sa pokúsi nastavenie zopakovať.

### 5.2 Agent sa po nasadení nespustí

**Príznaky:** Stav kontajnera ostáva „Pending“ cez 5 minút alebo ukazuje „Failed“.

**Riešenie - krok za krokom:**

1. Otvorte bočný panel **Microsoft Foundry** vo VS Code.
2. Kliknite na svoj hosťovaný agent → vyberte verziu.
3. V detailnom paneli skontrolujte **Container Details** → vyhľadajte sekciu alebo odkaz **Logs**.
4. Prečítajte si logy štartu kontajnera. Bežné príčiny:

| Hlásenie v logu | Príčina | Riešenie |
|-----------------|---------|----------|
| `ModuleNotFoundError: No module named 'xxx'` | Chýbajúca závislosť | Pridajte ju do `requirements.txt` a nasadzujte znova |
| `KeyError: 'PROJECT_ENDPOINT'` | Chýbajúca premenná prostredia | Pridajte env var do `agent.yaml` pod `env:` |
| `OSError: [Errno 98] Address already in use` | Konflikt portu | Uistite sa, že `agent.yaml` obsahuje `port: 8088` a že len jeden proces ho používa |
| `ConnectionRefusedError` | Agent nezačal počúvať | Skontrolujte `main.py` – volanie `from_agent_framework()` sa musí spustiť pri štarte |

5. Opravte problém a nasadzujte znova podľa [Modulu 6](06-deploy-to-foundry.md).

### 5.3 Nasadenie vypršalo

**Riešenie:**
1. Skontrolujte pripojenie na internet – push Docker image môže byť veľký (>100MB pri prvom nasadení).
2. Ak ste za firemným proxy, nastavte proxy v Docker Desktop: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Skúste to znova – sieťové výpadky môžu spôsobiť dočasné chyby.

---

## 6. Rýchla referencia: RBAC roly

| Rola | Typický rozsah | Čo povoľuje |
|------|----------------|-------------|
| **Azure AI User** | Projekt | Dátové akcie: build, deploy a volania agentov (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt alebo účet | Dátové akcie + tvorba projektov |
| **Azure AI Owner** | Účet | Plný prístup + správa priradení rolí |
| **Azure AI Project Manager** | Projekt | Dátové akcie + môže priraďovať Azure AI User iným |
| **Contributor** | Predplatné/skupina zdrojov | Manažérske akcie (vytváranie/mazanie zdrojov). **Nezahŕňa dátové akcie** |
| **Owner** | Predplatné/skupina zdrojov | Manažérske akcie + správa rolí. **Nezahŕňa dátové akcie** |
| **Reader** | Ktorýkoľvek | Iba čítací manažérsky prístup |

> **Dôležité:** Role `Owner` a `Contributor` **nezahŕňajú** dátové akcie. Pre operácie agentov vždy potrebujete niektorú **Azure AI** rolu. Minimálna rola pre tento workshop je **Azure AI User** na úrovni **projektu**.

---

## 7. Kontrolný zoznam dokončenia workshopu

Použite toto ako finálne potvrdenie, že ste absolvovali všetko:

| # | Položka | Modul | Splnené? |
|---|----------|-------|----------|
| 1 | Všetky predpoklady nainštalované a overené | [00](00-prerequisites.md) | |
| 2 | Nainštalovaný Foundry Toolkit a rozšírenia Foundry | [01](01-install-foundry-toolkit.md) | |
| 3 | Vytvorený Foundry projekt (alebo vybraný existujúci) | [02](02-create-foundry-project.md) | |
| 4 | Model nasadený (napr. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Priradená úloha používateľa Azure AI na úrovni projektu | [02](02-create-foundry-project.md) | |
| 6 | Vytvorený projekt so šablónou hosťovaného agenta (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` nakonfigurovaný s PROJECT_ENDPOINT a MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Prispôsobené pokyny pre agenta v main.py | [04](04-configure-and-code.md) | |
| 9 | Vytvorené virtuálne prostredie a nainštalované závislosti | [04](04-configure-and-code.md) | |
| 10 | Agent otestovaný lokálne pomocou F5 alebo terminálu (úspešné 4 základné testy) | [05](05-test-locally.md) | |
| 11 | Nasadené do služby Foundry Agent | [06](06-deploy-to-foundry.md) | |
| 12 | Stav kontajnera zobrazuje "Started" alebo "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Overené v prostredí VS Code Playground (úspešné 4 základné testy) | [07](07-verify-in-playground.md) | |
| 14 | Overené v Foundry Portal Playground (úspešné 4 základné testy) | [07](07-verify-in-playground.md) | |

> **Blahoželáme!** Ak sú všetky položky zaškrtnuté, dokončili ste celý workshop. Vytvorili ste hosťovaného agenta od základov, otestovali ho lokálne, nasadili do Microsoft Foundry a overili v produkcii.

---

**Predchádzajúce:** [07 - Overenie v Playground](07-verify-in-playground.md) · **Domov:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zrieknutie sa zodpovednosti**:  
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Aj keď sa snažíme o presnosť, majte prosím na pamäti, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho rodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za akékoľvek nedorozumenia alebo nesprávne výklady vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->