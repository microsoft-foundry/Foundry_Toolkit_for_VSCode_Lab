# 8. modul – Hibakeresés (Többügynökös)

Ez a modul a többügynökös munkafolyamatra jellemző gyakori hibákat, javításokat és hibakeresési stratégiákat tárgyalja. Általános Foundry telepítési problémák esetén tekintse meg a [Lab 01 hibakeresési útmutatót](../../lab01-single-agent/docs/08-troubleshooting.md) is.

---

## Gyors referencia: Hiba → Javítás

| Hiba / Tünet | Lehetséges ok | Javítás |
|--------------|---------------|---------|
| `RuntimeError: Missing required environment variable(s)` | Hiányzik a `.env` fájl vagy nincsenek beállítva az értékek | Hozzon létre egy `.env` fájlt a `PROJECT_ENDPOINT=<az-ön-végpontja>` és `MODEL_DEPLOYMENT_NAME=<az-ön-modelle>` értékekkel |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtual environment nincs aktiválva vagy a függőségek nincsenek telepítve | Futtassa a `.\.venv\Scripts\Activate.ps1` parancsot, majd a `pip install -r requirements.txt` parancsot |
| `ModuleNotFoundError: No module named 'mcp'` | MCP csomag nincs telepítve (hiányzik a requirements-ből) | Futtassa a `pip install mcp` parancsot vagy ellenőrizze, hogy a `requirements.txt` tartalmazza mint transzitív függőség |
| Az ügynök elindul, de üres választ ad vissza | `output_executors` hiányzik vagy rosszul van beállítva az élek | Ellenőrizze, hogy az `output_executors=[gap_analyzer]` szerepel és minden él létezik a `create_workflow()` függvényben |
| Csak 1 gap kártya jelenik meg (a többi hiányzik) | GapAnalyzer utasítások nem teljesek | Adja hozzá a `CRITICAL:` bekezdést a `GAP_ANALYZER_INSTRUCTIONS`-hoz – lásd [3. modul](03-configure-agents.md) |
| Fit pont 0 vagy hiányzik | MatchingAgent nem kapott adatot a bemenetről | Ellenőrizze, hogy mindkettő létezik: `add_edge(resume_parser, matching_agent)` és `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP szerver elutasította az eszköz hívást | Ellenőrizze az internetkapcsolatot. Próbálja meg megnyitni a `https://learn.microsoft.com/api/mcp` URL-t böngészőben. Próbálja újra |
| Nem jelennek meg Microsoft Learn URL-ek a kimenetben | MCP eszköz nincs regisztrálva vagy hibás az endpoint | Ellenőrizze, hogy `tools=[search_microsoft_learn_for_plan]` szerepel a GapAnalyzer-nál és hogy a `MICROSOFT_LEARN_MCP_ENDPOINT` helyes |
| `Address already in use: port 8088` | Egy másik folyamat használja a 8088-as portot | Futtassa a `netstat -ano \| findstr :8088` (Windows) vagy `lsof -i :8088` (macOS/Linux) parancsot, majd állítsa le az ütköző folyamatot |
| `Address already in use: port 5679` | Debugpy port ütközés | Állítsa le a többi hibakereső munkamenetet. `netstat -ano \| findstr :5679` segít megtalálni és leállítani a folyamatot |
| Az Agent Inspector nem nyílik meg | A szerver nincs teljesen elindulva vagy port ütközés van | Várjon a „Server running” naplóüzenetre. Ellenőrizze, hogy a 5679-es port szabad-e |
| `azure.identity.CredentialUnavailableError` | Nem jelentkezett be az Azure CLI-be | Futtassa az `az login` parancsot, majd indítsa újra a szervert |
| `azure.core.exceptions.ResourceNotFoundError` | Nem létező model telepítés | Ellenőrizze, hogy a `MODEL_DEPLOYMENT_NAME` megegyezik egy telepített modellel a Foundry projektben |
| A konténer állapota "Failed" telepítés után | Konténer lefagy az indításkor | Ellenőrizze a konténer naplókat a Foundry oldalsávban. Gyakori ok: hiányzó környezeti változó vagy import hiba |
| A telepítés "Pending" állapoton marad > 5 percig | Konténer túl lassú az induláshoz vagy erőforrás korlátok | Várjon 5 percet a többügynökös indításra (4 ügynököt hoz létre). Ha továbbra is "Pending", ellenőrizze a naplókat |
| `ValueError` a `WorkflowBuilder`-ből | Érvénytelen gráf konfiguráció | Győződjön meg róla, hogy a `start_executor` be van állítva, az `output_executors` lista és nincsenek körkörös élek |

---

## Környezeti és konfigurációs problémák

### Hiányzó vagy hibás `.env` értékek

A `.env` fájlnak a `PersonalCareerCopilot/` könyvtárban kell lennie (ugyanazon a szinten, mint a `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Várható `.env` tartalom:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **PROJECT_ENDPOINT megtalálása:**  
- Nyissa meg a **Microsoft Foundry** oldalsávot VS Code-ban → kattintson jobb gombbal a projektre → **Copy Project Endpoint**.  
- Vagy lépjen az [Azure Portalra](https://portal.azure.com) → a Foundry projekt → **Áttekintés** → **Project endpoint**.

> **MODEL_DEPLOYMENT_NAME megtalálása:** A Foundry oldalsávban bontsa ki a projektet → **Models** → keresse meg a telepített modell nevét (például `gpt-4.1-mini`).

### Környezeti változók prioritása

A `main.py` a `load_dotenv(override=False)` hívást használja, ami azt jelenti:

| Prioritás | Forrás | Kinek az értéke érvényes, ha mindkettő be van állítva? |
|-----------|--------|---------------------------------------------------------|
| 1 (legmagasabb) | Shell környezeti változó | A shell változó |
| 2 | `.env` fájl | Csak ha nincs shell változó |

Ez azt jelenti, hogy a Foundry futtatási környezetben (ami az `agent.yaml`-ban van megadva) beállított környezeti változók előnyt élveznek a `.env` fájl értékei fölött a hosztolt telepítés során.

---

## Verzió kompatibilitás

### Csomag verzió mátrix

A többügynökös munkafolyamat konkrét csomagverziókat igényel. A nem megfelelők futási hibákat okozhatnak.

| Csomag | Szükséges verzió | Ellenőrző parancs |
|--------|------------------|-------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | legfrissebb pre-release | `pip show agent-dev-cli` |
| Python | 3.10 vagy újabb | `python --version` |

### Gyakori verzió hibák

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Javítás: frissítés rc3-ra
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nincs telepítve vagy Inspector nem kompatibilis:**

```powershell
# Javítás: telepítés a --pre kapcsolóval
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Javítás: frissítsd az mcp csomagot
pip install mcp --upgrade
```

### Verziók egyszeri ellenőrzése

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Várt kimenet:

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

## MCP eszköz problémák

### MCP eszköz nem ad vissza eredményt

**Tünet:** A gap kártyákon az szerepel, hogy „No results returned from Microsoft Learn MCP” vagy „No direct Microsoft Learn results found”.

**Lehetséges okok:**

1. **Hálózati probléma** – Az MCP végpont (`https://learn.microsoft.com/api/mcp`) nem elérhető.  
   ```powershell
   # Kapcsolat tesztelése
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Ha ez `200`-as választ ad, az endpoint elérhető.

2. **Túl szűk lekérdezés** – Az adott készség neve túl speciális a Microsoft Learn kereséshez.  
   - Ez várható nagyon specializált készségek esetén. Az eszköz tartalmaz visszaeső URL-t a válaszban.

3. **MCP munkamenet időtúllépés** – A Streamable HTTP kapcsolat lejárt.  
   - Próbálja meg újra a kérést. Az MCP munkamenetek ideiglenesek és szükség lehet újracsatlakozásra.

### MCP naplók magyarázata

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Napló | Jelentés | Teendő |
|-------|----------|--------|
| `GET → 405` | MCP kliens próbakérések induláskor | Normális – figyelmen kívül hagyható |
| `POST → 200` | Eszközhívás sikeres | Várt állapot |
| `DELETE → 405` | MCP kliens próbakérések takarításkor | Normális – figyelmen kívül hagyható |
| `POST → 400` | Hibás kérés (hibás lekérdezés) | Ellenőrizze a `query` paramétert a `search_microsoft_learn_for_plan()`-ban |
| `POST → 429` | Lekérdezési limit túllépve | Várjon és próbálja újra. Csökkentse a `max_results` paramétert |
| `POST → 500` | MCP szerverhiba | Átmeneti – próbálja újra. Ha tartós, a Microsoft Learn MCP API hibás lehet |
| Kapcsolati időtúllépés | Hálózati probléma vagy MCP szerver nem elérhető | Ellenőrizze az internetkapcsolatot. Próbálja meg a `curl https://learn.microsoft.com/api/mcp` parancsot |

---

## Telepítési problémák

### Konténer indítási hiba telepítés után

1. **Ellenőrizze a konténer naplókat:**  
   - Nyissa meg a **Microsoft Foundry** oldalsávot → bontsa ki a **Hosted Agents (Preview)** részt → kattintson az ügynökre → bontsa ki a verziót → **Container Details** → **Logs**.  
   - Keresse a Python stack trace-eket vagy modul hiány hibákat.

2. **Gyakori konténer indítás hibák:**

   | Naplóbeli hiba | Oka | Javítás |
   |----------------|-----|---------|
   | `ModuleNotFoundError` | Hiányzó csomag a `requirements.txt`-ben | Adja hozzá a csomagot, majd telepítse újra |
   | `RuntimeError: Missing required environment variable` | `agent.yaml`-ban hiányzó környezeti változók | Frissítse az `agent.yaml` → `environment_variables` szekciót |
   | `azure.identity.CredentialUnavailableError` | Nincs konfigurálva a Managed Identity | Ezt a Foundry automatikusan beállítja – győződjön meg róla, hogy az extensionból telepít |
   | `OSError: port 8088 already in use` | Dockerfile rossz portot ad meg vagy portütközés | Ellenőrizze az `EXPOSE 8088` beállítást a Dockerfile-ban és a `CMD ["python", "main.py"]` parancsot |
   | A konténer kilép kóddal 1 | Kezelt kivétel a `main()` függvényben | Először tesztelje lokálisan ([5. modul](05-test-locally.md)), hogy észlelje a hibákat telepítés előtt |

3. **Javítás után újratelepítés:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → válassza ki ugyanazt az ügynököt → telepítsen új verziót.

### Telepítés túl hosszú ideig tart

A többügynökös konténerek hosszabb ideig indulnak, mert indításkor 4 ügynök példányt hoznak létre. Normál indítási idők:

| Fázis | Várható idő |
|-------|-------------|
| Konténer imagen építése | 1–3 perc |
| Kép feltöltése az ACR-be | 30–60 másodperc |
| Konténer indítás (egyszerű ügynök) | 15–30 másodperc |
| Konténer indítás (többügynök) | 30–120 másodperc |
| Ügynök elérhető a Playgroundban | 1–2 perc a „Started” után |

> Ha az állapot továbbra is „Pending” több mint 5 percig, ellenőrizze a konténer naplókat hibák után kutatva.

---

## RBAC és jogosultsági problémák

### `403 Forbidden` vagy `AuthorizationFailed`

Az Önnek szüksége van a **[Azure AI User](https://aka.ms/foundry-ext-project-role)** szerepkörre a Foundry projektjén:

1. Nyissa meg az [Azure Portal](https://portal.azure.com) → Foundry **projekt** erőforrását.
2. Kattintson az **Access control (IAM)** → **Role assignments** menüpontra.
3. Keresse meg a nevét → ellenőrizze, hogy szerepel-e az **Azure AI User**.
4. Hiány esetén: **Add** → **Add role assignment** → keresse meg az **Azure AI User** szerepet → adja hozzá az Ön fiókjához.

Részletekért olvassa el a [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokumentációt.

### Modell telepítés nem elérhető

Ha az ügynök modellhez kapcsolódó hibákat ad vissza:

1. Ellenőrizze, hogy a modell telepítve van: Foundry oldalsáv → bontsa ki a projektet → **Models** → nézze meg, hogy a `gpt-4.1-mini` (vagy az Ön modellje) státusza **Succeeded**-e.
2. Ellenőrizze, hogy a telepítés neve egyezik-e: hasonlítsa össze a `.env`-ben (vagy `agent.yaml`-ban) lévő `MODEL_DEPLOYMENT_NAME`-et a tényleges telepítés nevével az oldalsávban.
3. Ha a telepítés lejárt (free tier): telepítse újra a [Model Catalogból](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector problémák

### Inspector megnyílik, de „Disconnected” üzenetet mutat

1. Ellenőrizze, hogy a szerver fut: nézze az „Server running on http://localhost:8088” üzenetet a terminálban.
2. Ellenőrizze a 5679-es portot: az Inspector debugpy-val csatlakozik ezen a porton.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Indítsa újra a szervert és nyissa meg újra az Inspectort.

### Inspector csak részleges választ mutat

A többügynökös válaszok hosszúak és folyamatosan, részenként érkeznek. Várja meg, amíg a teljes válasz elkészül (ez 30–60 másodperc lehet a gap kártyák számától és az MCP hívások számától függően).

Ha a válasz konzisztensen hiányos:  
- Ellenőrizze, hogy a GapAnalyzer utasítások tartalmazzák a `CRITICAL:` blokkot, ami megakadályozza a gap kártyák összevonását.  
- Ellenőrizze a modell token limitjét – a `gpt-4.1-mini` támogat akár 32K kimeneti tokent is, ami általában elegendő.

---

## Teljesítmény tippek

### Lassú válaszok

A többügynökös folyamatok természetüknél fogva lassabbak, mint az együgynökösök, a szekvenciális függőségek és az MCP eszköz hívások miatt.

| Optimalizáció | Hogyan | Hatás |
|---------------|--------|-------|
| MCP hívások csökkentése | Csökkentse a `max_results` paraméter értékét az eszközben | Kevesebb HTTP körút |
| Utasítások egyszerűsítése | Rövidebb, fókuszáltabb ügynök parancsok | Gyorsabb LLM inferencia |
| `gpt-4.1-mini` használata | Gyorsabb fejlesztési forduló, mint a `gpt-4.1` | Körülbelül kétszeres gyorsulás |
| Gap kártya részletezés csökkentése | Egyszerűsítse a gap kártya formátumot a GapAnalyzer utasításokban | Kevesebb kimenet generálása |

### Tipikus válaszidők (helyi)

| Konfiguráció | Várt idő |
|--------------|----------|
| `gpt-4.1-mini`, 3-5 gap kártya | 30–60 másodperc |
| `gpt-4.1-mini`, 8+ gap kártya | 60–120 másodperc |
| `gpt-4.1`, 3-5 gap kártya | 60–120 másodperc |
---

## Segítség kérése

Ha elakadtál a fentiek kipróbálása után:

1. **Ellenőrizd a szerver naplókat** – A legtöbb hiba Python hívási visszakövetést ad a terminálon. Olvasd el a teljes visszakövetést.
2. **Keresd meg a hibaüzenetet** – Másold ki a hibaszöveget, és keresd meg a [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) oldalán.
3. **Nyiss egy hibajegyet** – Adj be hibajegyet a [workshop tárolóban](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) a következőkkel:
   - A hibaüzenet vagy képernyőkép
   - A csomagjaid verziói (`pip list | Select-String "agent-framework"`)
   - A Python verziód (`python --version`)
   - Helyi vagy telepítés utáni probléma-e

---

### Ellenőrző lista

- [ ] Képes vagy azonosítani és javítani a leggyakoribb többügynökös hibákat a gyorsreferencia táblázat segítségével
- [ ] Tudod, hogyan kell ellenőrizni és javítani a `.env` konfigurációs problémákat
- [ ] Ellenőrizni tudod, hogy a csomagverziók megfelelnek-e a szükséges mátrixnak
- [ ] Érted az MCP naplóbejegyzéseket és képes vagy diagnosztizálni az eszközhibákat
- [ ] Tudod, hogyan kell ellenőrizni a konténer naplókat telepítési hibák esetén
- [ ] Ellenőrizni tudod az RBAC szerepköröket az Azure Portálon

---

**Előző:** [07 - Ellenőrzés a játszóhelyen](07-verify-in-playground.md) · **Kezdőlap:** [Lab 02 README](../README.md) · [Workshop kezdőlap](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:  
A dokumentumot az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével fordítottuk le. Bár pontos fordításra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti, anyanyelvi dokumentum tekintendő hiteles forrásnak. Kritikus információk esetén professzionális emberi fordítást javaslunk. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy félrefordításokért.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->