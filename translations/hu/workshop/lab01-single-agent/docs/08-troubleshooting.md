# 8. modul - Hibakeresés

Ez a modul a gyakori problémák referencia útmutatója. Könyvjelzőzze, és térjen vissza, ha valami nem működik.

---

## 1. Engedélyhibák

### 1.1 `agents/write` jogosultság megtagadva

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Ok:** Hiányzik az `Azure AI User` szerepkör a **projekt** szinten. Ez a leggyakoribb workshop hiba.

**Javítás:**
1. Nyissa meg a [portal.azure.com](https://portal.azure.com) oldalt.
2. Keresse meg a Foundry **projekt** nevét → kattintson a **"Microsoft Foundry project"** típusú találatra (NEM a szülő fiókra).
3. **Hozzáférés-vezérlés (IAM)** → **+ Hozzáadás** → **Szerepkör hozzárendelés hozzáadása**.
4. Szerepkör: **Azure AI User** → Tovább.
5. Tagok: válassza ki saját magát → Áttekintés + hozzárendelés → Áttekintés + hozzárendelés.
6. **Várjon 1-2 percet** → próbálja újra.

> **Miért nem elég az Owner/Contributor:** Ezek a szerepkörök csak *kezelői* műveleteket engedélyeznek. Az agent műveletekhez szükséges az `agents/write` *adatművelet*, amely csak az `Azure AI User`, `Azure AI Developer` vagy `Azure AI Owner` szerepkörökben van meg. Lásd: [Foundry RBAC dokumentáció](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` hibák a telepítés során

**Javítás:** Kérje meg az adminisztrátorát, hogy rendeljen hozzá **Contributor** szerepkört az erőforráscsoporthoz, vagy hozza létre Ön helyette a projektet, és adja meg az Önnek az **Azure AI User** szerepkört.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Várjon, amíg megjelenik: "Regisztrálva"
```

---

## 2. Docker hibák

> A Docker használata **opcionális**. Ezek csak akkor relevánsak, ha a Docker Desktop telepítve van, és a kiterjesztés helyi buildet próbál végrehajtani.

### 2.1 Docker daemon nem fut

**Javítás:** Indítsa el a Docker Desktopot → várja meg, hogy az állapot "fut" legyen → ellenőrizze a `docker info` parancs segítségével → próbálja újra.

### 2.2 Build hibák függőségek miatt

**Javítás:** Ellenőrizze a `requirements.txt` helyesírását, először helyben tesztelje: `pip install -r requirements.txt`.

### 2.3 Platform eltérés (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Hitelesítési hibák

### 3.1 `DefaultAzureCredential` hibája

**Javítás (próbálja sorrendben):**
1. `az login` (újra hitelesítés)
2. `az account set --subscription "<id>"` (helyes előfizetés beállítása)
3. VS Code → Fiókok → Kijelentkezés → Újra bejelentkezés
4. Ellenőrizze: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token helyi működése, de hosztolt ügynöknél nem működik

**Ez várható:** A hosztolt ügynökök rendszerkezelte identitást használnak, nem az Ön hitelesítő adatait. Ha a hosztolt ügynök hitelesítési hibákat kap:
- Ellenőrizze, hogy az `agent.yaml` fájlban helyes-e az `AZURE_AI_PROJECT_ENDPOINT`
- Győződjön meg arról, hogy a projekt kezelői identitása hozzáfér a modellhez

---

## 4. Modellhibák

### 4.1 Modelltelepítés nem található

**Javítás:** A név **nagybetű-érzékeny**. Hasonlítsa össze a `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` értékét a pontos névvel a Foundry oldalsávban → Modellek.

### 4.2 Váratlan modell kimenet

**Javítás:** Vizsgálja át az `AGENT_INSTRUCTIONS`-t a `main.py`-ban (nem lett-e levágva?). Próbáljon ki más modellt (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Telepítési hibák

### 5.1 ACR lehúzás jogosulatlan

**Javítás:** Azure Portal → Konténerregisztráció → Hozzáférés-vezérlés (IAM) → Adja hozzá az **AcrPull** szerepkört a Foundry projekt kezelői identitásához.

### 5.2 Az ügynök nem indul el (marad "Pending" vagy "Failed")

Ellenőrizze a konténer naplóit az oldalsávon. Gyakori okok:

| Naplóüzenet | Javítás |
|-------------|-----|
| `ModuleNotFoundError` | Adja hozzá a hiányzó csomagot a `requirements.txt`-hez, majd telepítse újra |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Adja hozzá a környezeti változót az `agent.yaml`-hoz az `environment_variables` alatt |
| `Address already in use` | Győződjön meg róla, hogy csak egy folyamat kötődik a 8088-as portra |

### 5.3 Telepítés időtúllépés miatt meghiúsul

**Javítás:** Ellenőrizze az internetkapcsolatot. Az első telepítés több mint 100 MB feltöltést jelent. Proxy mögött van? Állítsa be a Docker Desktop proxy-beállításait.

---

## 6. B út - Foundry Local

### 6.1 Foundry Local nem indul el

| Probléma | Javítás |
|-------|-----|
| `foundry: command not found` | Telepítse újra: `winget install Microsoft.FoundryLocal` |
| Nem elegendő erőforrás | A Foundry Localnak ~4 GB szabad RAM kell. Zárjon be más alkalmazásokat. |
| Modell letöltés sikertelen | Ellenőrizze a lemezterületet (a modellek 2-8 GB-osak). Próbálja újra: `foundry local models pull <név>` |

### 6.2 Foundry Local modellhibák

| Probléma | Javítás |
|-------|-----|
| Lassú válaszok | Ez várható - a helyi modellek CPU-n futnak, ha nincs GPU. Legyen türelmes. |
| Gyenge minőségű kimenet | Próbáljon nagyobb modellt, ha a hardvere engedi. A `phi-4-mini` jó egyensúly. |
| Kapcsolat elutasítva | Ellenőrizze, hogy a Foundry Local fut-e: `foundry local status`. Szükség esetén indítsa újra. |

---

## 7. Gyors hivatkozás: RBAC szerepkörök

| Szerepkör | Hatókör | Jogosultságok |
|------|-------|--------|
| **Azure AI User** | Projekt | Adatműveletek: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Fiók | Adatműveletek + projekt létrehozás |
| **Azure AI Owner** | Fiók | Teljes hozzáférés + szerepkör-kezelés |
| **Contributor** | Előfizetés/ER | Csak kezelői műveletek (**nincs** adatművelet) |
| **Owner** | Előfizetés/ER | Kezelői műveletek + szerepkör hozzárendelés (**nincs** adatművelet) |

---

## 8. Workshop befejezési ellenőrzőlista

| # | Tétel | Modul |
|---|------|--------|
| 1 | Előfeltételek telepítve és ellenőrizve | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit kiterjesztés telepítve, projekt csatlakoztatva (vagy B út konfigurálva) | [01](01-setup.md) |
| 3 | Hosztolt agent felállítva | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfigurálva, utasítások megírva, függőségek telepítve | [03](03-configure-and-code.md) |
| 5 | Agent helyben tesztelve – 3 funkcionális szcenárió sikeres | [04](04-test-locally.md) |
| 6 | Telepítve a Foundry-ba (csak A út) | [05](05-deploy-to-foundry.md) |
| 7 | Szél-eseti/biztonsági tesztek átmentek a felhőben (csak A út) | [06](06-verify-in-playground.md) |
| 8 | Összefoglaló áttekintve, következő lépések azonosítva | [07](07-summary.md) |

---

**Előző:** [07 - Összefoglaló](07-summary.md) · **Főoldal:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->