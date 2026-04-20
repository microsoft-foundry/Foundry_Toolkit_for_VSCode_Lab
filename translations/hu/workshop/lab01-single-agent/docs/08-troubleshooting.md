# 8. modul - Hibakeresés

Ez a modul referenciaútmutató a workshop során felmerülő minden gyakori probléma esetén. Könyvjelzőzd - bármikor visszatérhetsz hozzá, ha valami nem működik.

---

## 1. Jogosultsági hibák

### 1.1 `agents/write` engedély megtagadva

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Alapvető ok:** Nincs `Azure AI User` szerepköröd a **projekt** szinten. Ez a workshop leggyakoribb hibája.

**Javítás - lépésről lépésre:**

1. Nyisd meg a [https://portal.azure.com](https://portal.azure.com) oldalt.
2. A felső keresősávba írd be a **Foundry projekt** nevét (pl. `workshop-agents`).
3. **Fontos:** Kattints arra az eredményre, amelyik típusa **"Microsoft Foundry project"**, NEM a szülő fiók/központi erőforrás. Ezek különböző erőforrások, eltérő RBAC hatókörrel.
4. A projekt oldal bal oldali navigációjában kattints az **Hozzáférés vezérlés (IAM)** menüpontra.
5. Kattints a **Szerepkör hozzárendelések** fülre, hogy ellenőrizd, van-e már szerepköröd:
   - Keress rá a nevedre vagy email címedre.
   - Ha az `Azure AI User` szerepkör már szerepel → a hiba más okból van (nézd meg a 8. lépést lent).
   - Ha nem szerepel → folytasd a hozzáadással.
6. Kattints a **+ Hozzáadás** → **Szerepkör hozzárendelés hozzáadása** gombra.
7. A **Szerepkör** fülön:
   - Keress rá az [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) szerepkörre.
   - Válaszd ki az eredmények közül.
   - Kattints a **Tovább** gombra.
8. A **Tagok** fülön:
   - Válaszd a **Felhasználó, csoport vagy szolgáltatás principal** lehetőséget.
   - Kattints a **+ Tagok kiválasztása** gombra.
   - Keresd meg a neved vagy email címed.
   - Válaszd ki magad az eredmények közül.
   - Kattints a **Kiválasztás** gombra.
9. Kattints a **Ellenőrzés és hozzárendelés** → ismét **Ellenőrzés és hozzárendelés**.
10. **Várj 1-2 percet** - az RBAC változásoknak időre van szükségük a terjedéshez.
11. Próbáld újra a sikertelen műveletet.

> **Miért nem elég az Owner/Contributor:** Az Azure RBAC két típusú engedélyt tartalmaz: *kezelési műveletek* és *adat műveletek*. Az Owner és Contributor a kezelési műveleteket biztosítják (erőforrások létrehozása, beállítások szerkesztése), de az ügynök műveletekhez az `agents/write` **adat művelet** szükséges, ami csak az `Azure AI User`, `Azure AI Developer` vagy `Azure AI Owner` szerepkörökben van benne. Részletekért lásd a [Foundry RBAC dokumentációt](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` hiba erőforrás létrehozásakor

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Alapvető ok:** Nincs jogosultságod létrehozni vagy módosítani Azure erőforrásokat ebben az előfizetésben/erőforráscsoportban.

**Javítás:**
1. Kérd az előfizetés adminisztrátorát, hogy rendeljen hozzád **Contributor** szerepkört azon az erőforráscsoporton, ahol a Foundry projekted van.
2. Alternatívaként kérd meg, hogy hozza létre helyetted a Foundry projektet, és adjon neked **Azure AI User** szerepkört a projekten.

### 1.3 `SubscriptionNotRegistered` hiba a [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) esetén

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Alapvető ok:** Az Azure előfizetés még nem regisztrálta a Foundry működéséhez szükséges erőforrás-szolgáltatót.

**Javítás:**

1. Nyiss egy terminált és futtasd:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Várj a regisztráció befejezésére (1-5 perc is lehet):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Várt kimenet: `"Registered"`
3. Próbáld újra a műveletet.

---

## 2. Docker hibák (ha Docker telepítve van)

> A workshophoz a Docker **nem kötelező**. Ezek a hibák csak akkor léphetnek fel, ha a Docker Desktop telepítve van, és a Foundry kiterjesztés helyi konténer építését próbálja.

### 2.1 Docker démon nem fut

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Javítás - lépésről lépésre:**

1. Keresd meg a Docker Desktopot a Start menüben (Windows) vagy az Alkalmazások között (macOS) és indítsd el.
2. Várj, amíg megjelenik a Docker Desktop ablakban a **"Docker Desktop is running"** üzenet - ez általában 30-60 másodperc.
3. Nézd meg a Docker bálna ikonját a tálcán (Windows) vagy a menüsorban (macOS). Vidd fölé az egeret a státusz megerősítéséhez.
4. Ellenőrizd terminálban:
   ```powershell
   docker info
   ```
   Ha kiírja a Docker rendszerinformációkat (Server Version, Storage Driver, stb.), akkor a Docker fut.
5. **Windows specifikus:** Ha a Docker nem indul el:
   - Nyisd meg a Docker Desktopot → **Beállítások** (fogaskerék ikon) → **Általános**.
   - Ellenőrizd, hogy be van-e pipálva a **Use the WSL 2 based engine**.
   - Kattints az **Alkalmaz és újraindít** gombra.
   - Ha a WSL 2 nincs telepítve, futtasd a `wsl --install` parancsot egy emelt PowerShell ablakban, majd indítsd újra a gépet.
6. Próbáld újra a telepítést.

### 2.2 Docker build hibák függőségi problémákkal

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Javítás:**
1. Nyisd meg a `requirements.txt` fájlt, és ellenőrizd, hogy a csomagnevek helyesen vannak-e írva.
2. Ellenőrizd a verzió megkötéseket:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Először teszteld helyben a telepítést:
   ```bash
   pip install -r requirements.txt
   ```
4. Ha privát csomagtárat használsz, ellenőrizd, hogy a Docker képes hálózati hozzáférésre.

### 2.3 Konténer platform egyezőség hiánya (Apple Silicon)

Ha Apple Silicon Mac-ről (M1/M2/M3/M4) telepítesz, a konténert `linux/amd64` platformra kell építeni, mert a Foundry konténer futtatója AMD64-et használ.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> A Foundry kiterjesztés deploy parancsa ezt általában automatikusan kezeli. Ha architektúrális hibákat látsz, építsd manuálisan a `--platform` opcióval, és vedd fel a kapcsolatot a Foundry csapattal.

---

## 3. Hitelesítési hibák

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) nem tud tokenhez jutni

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Alapvető ok:** A `DefaultAzureCredential` lánc egyik hitelesítési forrása sem tartalmaz érvényes tokent.

**Javítás - próbáld meg sorban a következő lépéseket:**

1. **Jelentkezz be újra Azure CLI-n keresztül** (ez a leggyakoribb megoldás):
   ```bash
   az login
   ```
   Megnyílik egy böngészőablak. Jelentkezz be, majd térj vissza a VS Code-ba.

2. **Állítsd be a helyes előfizetést:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Ha nem a megfelelő előfizetés:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Jelentkezz be újra a VS Code-on keresztül:**
   - Kattints a bal alsó sarokban az **Fiókok** ikonra (ember ikon).
   - Kattints a fiókodra → **Kijelentkezés**.
   - Kattints újra az Fiókok ikonra → **Bejelentkezés Microsoft-fiókkal**.
   - Kövesd a böngészős bejelentkezési lépéseket.

4. **Szolgáltatás főnév (csak CI/CD esetén):**
   - Állítsd be ezeket a környezeti változókat a `.env` fájlban:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Majd indítsd újra az ügynök folyamatot.

5. **Ellenőrizd a token gyorsítótárat:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Ha ez meghiúsul, a CLI tokened lejárt. Futtasd újra az `az login` parancsot.

### 3.2 Token működik helyben, de nem a hosztolt telepítésnél

**Alapvető ok:** A hosztolt ügynök egy rendszer által kezelt identitást használ, amely eltér a személyes hitelesítésedtől.

**Javítás:** Ez elvárt viselkedés - a kezelten kezelt identitás automatikusan létrejön a telepítés során. Ha a hosztolt ügynök mégis hitelesítési hibákat kap:
1. Ellenőrizd, hogy a Foundry projekt kezelten kezelt identitása hozzáfér az Azure OpenAI erőforráshoz.
2. Győződj meg róla, hogy a `PROJECT_ENDPOINT` az `agent.yaml` fájlban helyes.

---

## 4. Modell hibák

### 4.1 Modell telepítés nem található

```
Error: Model deployment not found / The specified deployment does not exist
```

**Javítás - lépésről lépésre:**

1. Nyisd meg a `.env` fájlt, és jegyezd fel az `AZURE_AI_MODEL_DEPLOYMENT_NAME` értékét.
2. Nyisd meg a **Microsoft Foundry** oldalsávot a VS Code-ban.
3. Bontsd ki a projektedet → **Model Deployments** (Modell telepítések).
4. Hasonlítsd össze a listázott telepítés nevét a `.env` fájlban szereplővel.
5. A név **kis- és nagybetű érzékeny** - a `gpt-4o` nem ugyanaz, mint a `GPT-4o`.
6. Ha nem egyeznek, frissítsd a `.env` fájlban a pontosan megadott névre.
7. Hosztolt telepítés esetén frissítsd az `agent.yaml` fájlt is:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modell váratlan tartalommal válaszol

**Javítás:**
1. Nézd át az `EXECUTIVE_AGENT_INSTRUCTIONS` konstans értékét a `main.py` fájlban. Győződj meg arról, hogy nem lett megvágva vagy sérült.
2. Ellenőrizd a modell hőmérséklet beállítást (ha állítható) - alacsonyabb érték determinisztikusabb kimenetet eredményez.
3. Hasonlítsd össze, hogy mely modell van telepítve (pl. `gpt-4o` vs. `gpt-4o-mini`) - a különböző modellek más képességekkel rendelkeznek.

---

## 5. Telepítési hibák

### 5.1 ACR (Azure Container Registry) lehívási jogosultság

```
Error: AcrPullUnauthorized
```

**Alapvető ok:** A Foundry projekt kezelten kezelt identitása nem tudja lehúzni a konténer képet az Azure Container Registryből.

**Javítás - lépésről lépésre:**

1. Nyisd meg a [https://portal.azure.com](https://portal.azure.com) oldalt.
2. Keress rá a felső keresőben a **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** kifejezésre.
3. Kattints arra a regiszterre, amely a Foundry projekthez tartozik (általában ugyanabban az erőforráscsoportban van).
4. A bal oldali navigációban kattints az **Hozzáférés vezérlés (IAM)** pontra.
5. Kattints a **+ Hozzáadás** → **Szerepkör hozzárendelés hozzáadása** gombra.
6. Keress rá az **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** szerepkörre és válaszd ki. Kattints a **Tovább** gombra.
7. Válaszd a **Kezelt identitás** lehetőséget → Kattints a **+ Tagok kiválasztása** gombra.
8. Keresd meg és válaszd ki a Foundry projekt kezelt identitását.
9. Kattints a **Kiválasztás** → **Ellenőrzés és hozzárendelés** → ismét **Ellenőrzés és hozzárendelés**.

> Ez a szerepkör hozzárendelés rendszerint automatikusan megtörténik a Foundry kiterjesztés által. Ha ezt a hibát látod, az automatikus beállítás valószínűleg nem sikerült. Próbáld meg újból telepíteni - a kiterjesztés újrapróbálkozhat a beállítással.

### 5.2 Az ügynök nem indul el a telepítés után

**Tünetek:** A konténer állapota több mint 5 percig „Függőben” marad vagy „Failed” (Sikertelen).

**Javítás - lépésről lépésre:**

1. Nyisd meg a **Microsoft Foundry** oldalsávot a VS Code-ban.
2. Kattints a hosztolt ügynöködre → válaszd ki a verziót.
3. A részletek panelen ellenőrizd a **Container Details** részt → keress **Naplók** szekciót vagy linket.
4. Olvasd el a konténer indítási naplókat. Gyakori okok:

| Napló üzenet | Ok | Javítás |
|-------------|----|---------|
| `ModuleNotFoundError: No module named 'xxx'` | Hiányzó függőség | Add hozzá a `requirements.txt`-hez és telepítsd újra |
| `KeyError: 'PROJECT_ENDPOINT'` | Hiányzó környezeti változó | Add hozzá az `agent.yaml` alatt az `env:` szekcióhoz |
| `OSError: [Errno 98] Address already in use` | Port ütközés | Győződj meg róla, hogy az `agent.yaml` fájlban a `port: 8088`, és csak egy folyamat foglalja azt |
| `ConnectionRefusedError` | Az ügynök nem kezdett el figyelni | Ellenőrizd a `main.py`-ben, hogy a `from_agent_framework()` hívás induláskor lefut-e |

5. Javítsd a problémát, majd telepítsd újra a [6. modulból](06-deploy-to-foundry.md).

### 5.3 A telepítés időtúllépés miatt meghiúsul

**Javítás:**
1. Ellenőrizd az internetkapcsolatot - a Docker push nagy lehet (>100MB az első telepítéskor).
2. Ha vállalati proxy mögött vagy, ellenőrizd a Docker Desktop proxy beállításait: **Docker Desktop** → **Beállítások** → **Erőforrások** → **Proxyk**.
3. Próbáld újra - hálózati hibák okozhatnak átmeneti sikertelenséget.

---

## 6. Gyors hivatkozás: RBAC szerepkörök

| Szerepkör | Tipikus hatókör | Mit biztosít |
|----------|-----------------|-------------|
| **Azure AI User** | Projekt | Adatműveletek: ügynökök létrehozása, telepítése, hívása (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt vagy Fiók | Adatműveletek + projekt létrehozás |
| **Azure AI Owner** | Fiók | Teljes hozzáférés + szerepkörtervezés |
| **Azure AI Project Manager** | Projekt | Adatműveletek + tud másoknak Azure AI User szerepkört adni |
| **Contributor** | Előfizetés/Erőforráscsoport | Kezelési műveletek (erőforrás létrehozás/törlés). **Nem tartalmaz adatműveleteket** |
| **Owner** | Előfizetés/Erőforráscsoport | Kezelési műveletek + szerepkörtervezés. **Nem tartalmaz adatműveleteket** |
| **Reader** | Bármely | Csak olvasási kezelési hozzáférés |

> **Fontos:** Az `Owner` és a `Contributor` szerepkörök **NEM** tartalmaznak adatművelet jogokat. Ügynök műveletekhez mindig szükséges egy `Azure AI *` szerepkör. Ennek a workshopnak a minimális szerepköre az **Azure AI User** a **projekt** szinten.

---

## 7. Workshop befejezési ellenőrzőlista

Használd ezt végső ellenőrzésként, hogy minden kész:

| # | Tétel | Modul | Kész? |
|---|-------|-------|-------|
| 1 | Minden előfeltétel telepítve és ellenőrizve | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit és Foundry kiterjesztések telepítve | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry projekt létrehozva (vagy meglévő projekt kiválasztva) | [02](02-create-foundry-project.md) | |
| 4 | Modell telepítve (pl. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI Felhasználói szerep hozzárendelve projekt szinten | [02](02-create-foundry-project.md) | |
| 6 | Hosted agent projekt előkészítve (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` konfigurálva PROJECT_ENDPOINT és MODEL_DEPLOYMENT_NAME értékekkel | [04](04-configure-and-code.md) | |
| 8 | Agent utasítások testreszabva a main.py fájlban | [04](04-configure-and-code.md) | |
| 9 | Virtuális környezet létrehozva és függőségek telepítve | [04](04-configure-and-code.md) | |
| 10 | Agent helyben tesztelve F5 vagy terminál segítségével (4 füstteszt sikeres) | [05](05-test-locally.md) | |
| 11 | Telepítve a Foundry Agent Szolgáltatásba | [06](06-deploy-to-foundry.md) | |
| 12 | Konténer állapot "Started" vagy "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Ellenőrizve VS Code Playgroundban (4 füstteszt sikeres) | [07](07-verify-in-playground.md) | |
| 14 | Ellenőrizve a Foundry Portal Playgroundban (4 füstteszt sikeres) | [07](07-verify-in-playground.md) | |

> **Gratulálunk!** Ha az összes pont be van jelölve, akkor befejezted az egész workshopot. Zero-ról építettél egy hosted agentet, helyben letesztelted, telepítetted a Microsoft Foundry-ba, és éles környezetben is validáltad.

---

**Előző:** [07 - Ellenőrzés a Playground-ban](07-verify-in-playground.md) · **Kezdőlap:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Felelősség kizárása**:  
Ez a dokumentum az AI fordító szolgáltatás [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár igyekszünk a pontosságra, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén szakmai emberi fordítást javaslunk. Nem vállalunk felelősséget az ebből a fordításból eredő félreértésekért vagy félreértelmezésekért.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->