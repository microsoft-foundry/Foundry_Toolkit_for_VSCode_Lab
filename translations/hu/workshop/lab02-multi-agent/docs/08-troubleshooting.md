# 8. modul - Hibakeresés

Ez a modul a többügynökös munkafolyamatra jellemző gyakori hibákat, javításokat és hibakeresési stratégiákat tárgyalja.

## Ügynök kimeneti problémák

### A GapAnalyzer azt mondja: „Még mindig nincs meg a megfelelő jelentés”

**Tünet:** A GapAnalyzer válasza azt kéri, hogy illessz be egy „Hiányzó készségeket” és „Tanúsítványi hiányosságokat” tartalmazó egyező jelentést. Ez akkor is előfordul, ha mind az önéletrajzot, mind az állásleírást elküldted.

**Oka:** Az állásleírás szövege nem jutott továbbításra a JD Agent felé. A `context_mode="last_agent"` esetén a `resume_executor` az egyetlen végrehajtó, amely valaha látja a felhasználó eredeti üzenetét. Ha a `RESUME_PARSER_INSTRUCTIONS` nem tartalmazza az állásleírás szövegét a kimenetben, a JD Agent-nek nincs feldolgoznivaló állásleírása, a MatchingAgent nem tud illeszkedési pontszámot számolni, és a GapAnalyzer értelmetlen bemenetet kap.

**Diagnózis:**

A szerver naplókban keresd a MatchingAgent spant. Ha az tartalmazza:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
a továbbítás hiányzik vagy sérült.

**Javítás:** Győződj meg arról, hogy a `main.py`-ban a `RESUME_PARSER_INSTRUCTIONS` tartalmaz egy `[JOB DESCRIPTION PASS-THROUGH]` szakaszt és a szabályt:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Ellenőrizd azt is, hogy a `JOB_DESCRIPTION_INSTRUCTIONS` tartalmaz egy `[PARSED RESUME PASS-THROUGH]` továbbító szabályt:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Ha bármelyik utasításblokk sablon a scaffold varázslóból, cseréld ki annak teljes verziójára a [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) fájlból.

### A MatchingAgent ezt adja vissza: „Nem tudom kiszámítani az illeszkedési pontszámot - nincs megadva állásleírás”

Ez ugyanaz az alapvető ok, mint fent. A MatchingAgent megkapta a JD Agent kimenetét, de a `[PARSED RESUME PASS-THROUGH]` szakasz hiányzott vagy üres volt, ezért nem tudta összehasonlítani a két profilt. Ellenőrizd:
1. A `JOB_DESCRIPTION_INSTRUCTIONS` tartalmazza a továbbító szabályt: `Másold le [PARSED RESUME] szó szerint - a Matching Agent erre támaszkodik lefelé.`
2. A `MATCHING_AGENT_INSTRUCTIONS` utasítja az ügynököt, hogy keresse a `[JD REQUIREMENTS]` és `[PARSED RESUME PASS-THROUGH]` szakaszokat.

Cseréld le mindkét utasításblokkot a teljes verziókra a [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) fájlból.

### A válasz kétszer jelenik meg

**Tünet:** A GapAnalyzer kimenet (vagy az egész adatfolyam kimenete) kétszer jelenik meg az Agent Inspector válaszában.

**Oka:** A `WorkflowBuilder` OR-szemantikát használ a bejövő élekhez - egy lefelé mutató végrehajtó akkor indul el, amint **bármelyik** elődje befejeződik. Ha a `matching_executor`-nek két bejövő éle van (egy a `resume_executor`-tól és egy a `jd_executor`-tól), kétszer indul el: egyszer, amikor a ResumeParser befejeződik, és egyszer, amikor a JD Agent befejeződik. Ekkor a GapAnalyzer is kétszer fut.

**Javítás:** Biztosítsd, hogy a `WorkflowBuilder` gráf szigorúan szekvenciális adatfolyam legyen fan-in nélkül:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NEM a resume_executor-tól
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Ha találsz egy felesleges `.add_edge(resume_executor, matching_executor)` sort, távolítsd el. A JD Agent kimenetében lévő `[PARSED RESUME PASS-THROUGH]` továbbítás már hozzáférést ad a MatchingAgentnek az önéletrajzhoz.

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

Várt `.env` tartalom:

**A útvonal - Foundry felhő:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**B útvonal - Foundry helyi:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Mindkét útvonal a `FOUNDRY_PROJECT_ENDPOINT` változót használja. Az érték különbözik: a felhő az `https://` Foundry végpontot használja; a helyi a `http://localhost:5273/v1`-et. A pontos modell alias megerősítéséhez futtasd a `foundry model list` parancsot a B útvonalhoz.

> **Hogyan találhatod meg a `FOUNDRY_PROJECT_ENDPOINT` értéket:** 
- Nyisd meg a VS Code-ban a **Foundry Toolkit** oldalsávot → jobb klikk a projekteden → **Copy Project Endpoint**. 
- Vagy menj az [Azure Portal](https://portal.azure.com) oldalra → a Foundry projektedhez → **Áttekintés** → **Projekt végpont**.

> **Hogyan találhatod meg az `AZURE_AI_MODEL_DEPLOYMENT_NAME` értékét:** A Foundry Toolkit oldalsávban bontsd ki a projektedet → **Models** → keresd meg a telepített modell nevét (pl. `gpt-4.1-mini`).

### Környezeti változó előnyben részesítése

A `main.py` használja a `load_dotenv(override=True)`-t, ami azt jelenti:

| Prioritás | Forrás | Az mindkettő esetén nyer? |
|----------|--------|-----------------------|
| 1 (legmagasabb) | `.env` fájl | Igen |
| 2 | Shell / konténer környezeti változó | Akkor használja, ha nincs meg a kulcs a `.env`-ben |

Helyi fejlesztésnél ez azt jelenti, hogy a `.env` az igazság forrása (a `.env` szerkesztése azonnal hatással van a futtatásra). Üzemeltetett telepítésben a Foundry a környezeti változókat a konténer szintjén injektálja; mivel a `.env` nem része a telepített képnek ehhez a laborszinthez, az injektált konténerértékeket használja.

---

## Verzió kompatibilitás

### Csomag verzió mátrix

A többügynökös munkafolyamat konkrét csomagverziókat igényel. A nem egyező verziók futásidejű hibákat okoznak.

| Csomag | Szükséges verzió | Ellenőrző parancs |
|---------|-----------------|------------------|
| `agent-framework-foundry` | legfrissebb | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | legfrissebb | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | legfrissebb | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Gyakori verzióhibák

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Javítás: újratelepíteni az agent-framework-foundry-t
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Javítás: frissítse az mcp csomagot
pip install mcp --upgrade
```

### Ellenőrizd egyszerre az összes verziót

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Várt kimenet:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Telepítési problémák

### A konténer nem indul el a telepítés után

1. **Ellenőrizd a konténer naplóit:**
   - Nyisd meg a **Foundry Toolkit** oldalsávot → bontsd ki a **Hosted Agents (Preview)** → kattints az ügynökre → bontsd ki a verziót → **Container Details** → **Logs**.
   - Keresd a Python stack trace-eket vagy hiányzó modul hibákat.

2. **Gyakori konténer indítási hibák:**

   | Hiba a naplóban | Oka | Javítás |
   |-----------------|-----|--------|
   | `ModuleNotFoundError` | Hiányzik csomag a `requirements.txt`-ből | Add hozzá, majd telepítsd újra |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Nem állították be az `agent.yaml` vagy `.env` környezeti változókat | Frissítsd az `agent.yaml` → `environment_variables` szakaszt (hostolt) vagy a `.env`-et (helyi) |
   | `azure.identity.CredentialUnavailableError` | Kezelt identitás nincs konfigurálva | A Foundry automatikusan beállítja - győződj meg arról, hogy bővítményen keresztül telepítesz |
   | `OSError: port 8088 already in use` | A Dockerfile rossz portot exponál vagy portütközés van | Ellenőrizd a `Dockerfile`-ban az `EXPOSE 8088`-at és a `CMD ["python", "main.py"]` parancsot |
   | A konténer kilép 1-es kóddal | Kezeltlen kivétel a `main()`-ben | Teszteld helyben először ([8. modul](05-test-locally.md)) a telepítés előtt |

3. **Telepítés újra a javítás után:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → válaszd ugyanazt az ügynököt → telepíts egy új verziót.

### A telepítés túl sokáig tart

A többügynökös konténerek lassabban indulnak, mert az indításkor 4 ügynök-példányt hoznak létre. Átlagos indulási idők:

| Fázis | Várt időtartam |
|--------|---------------|
| Konténer kép építése | 1-3 perc |
| Kép feltöltése az ACR-be | 30-60 másodperc |
| Konténer indítása (egy ügynök) | 15-30 másodperc |
| Konténer indítása (több ügynök) | 30-120 másodperc |
| Ügynök elérhető a Playgroundon | 1-2 perc „Started” után |

> Ha az „Pending” állapot 5 percnél tovább fennáll, ellenőrizd a konténer naplóit hibák után.

---

## RBAC és jogosultsági problémák

### `403 Forbidden` vagy `AuthorizationFailed`

Szükséged van a **[Foundry User](https://aka.ms/foundry-ext-project-role)** szerepkörre a Foundry projektedben (korábban **Azure AI User** néven, szerepkör azonosító változatlan):

1. Menj az [Azure Portal](https://portal.azure.com) oldalra → a Foundry **projekt** erőforrásodhoz.
2. Kattints az **Access control (IAM)** → **Role assignments** menüpontra.
3. Keresd meg a neved → ellenőrizd, hogy szerepel-e a **Foundry User** (vagy a régebbi címke szerint **Azure AI User**).
4. Ha hiányzik: **Hozzáadás** → **Add role assignment** → keresd meg a **Foundry User**-t → rendeld hozzá a fiókodhoz.

Részletekért lásd a [RBAC Microsoft Foundry-hoz](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokumentációt.

### A modell telepítése nem elérhető

Ha az ügynök modellhez kapcsolódó hibákat jelez:

1. Győződj meg róla, hogy a modell telepítve van: Foundry oldalsáv → bontsd ki a projektet → **Models** → nézd meg, hogy a `gpt-4.1-mini` (vagy a te modell) státusza **Succeeded**.
2. Ellenőrizd, hogy a telepítés neve egyezik-e: hasonlítsd össze a `.env`-ben (vagy `agent.yaml`-ban) az `AZURE_AI_MODEL_DEPLOYMENT_NAME` értékét a tényleges telepítési névvel a oldalsávban.
3. Ha a telepítés lejárt (ingyenes szint): telepítsd újra a [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) segítségével (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local problémák (B útvonal)

### A Foundry Local szolgáltatás nem fut

```powershell
# Állapot ellenőrzése
foundry local status

# Indítsa el a szolgáltatást, ha leállt
foundry local start
```

| Tünet | Oka | Javítás |
|--------|-----|--------|
| Egészségügyi ellenőrzés `503`-at ad vissza | A szolgáltatás nem indult el | Futtasd a `foundry local start` parancsot vagy kattints a **Start**-ra a Foundry Toolkit oldalsávban |
| Az egészségügyi ellenőrzés időtúllépéses | A modell még töltődik | Várj 30–60 másodpercet az indítás után; a nagyobb modellek tovább töltenek |
| `/v1/health` végponton `StatusCode: 404` | Rossz port | Az alapértelmezett `5273`. Ellenőrizd a `foundry local status` parancsot a tényleges portról |
| Erőforrások elégtelenek | A Foundry Localnak kb. 4 GB szabad RAM kell | Zárj be más alkalmazásokat |
| A modell letöltése meghiúsul | Kevés a lemezterület | A modellek 2–8 GB méretűek. Szabadíts fel helyet, majd futtasd a `foundry model pull <név>` parancsot |

### Modellnév nem egyezik

```powershell
# Az letöltött modellek és azok pontos aliasainak listázása
foundry model list
```

Állítsd be az `AZURE_AI_MODEL_DEPLOYMENT_NAME` értékét a `.env` fájlban pontosan a megadott aliasra (például `phi-4-mini`, nem `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` helyi futtatáskor (B útvonal)

A lab `main.py`-ja használja az `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` változót. A Foundry Local ezt a változót a helyi szolgáltatásra kell állítani - **nem** az `AZURE_AI_PROJECT_ENDPOINT`-re. Győződj meg, hogy a `.env` tartalmazza:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Az MCP eszköz még mindig kimenő hívást tesz (B útvonal)

Ez várható. A `search_microsoft_learn_for_plan` eszköz a `https://learn.microsoft.com/api/mcp` címen keres tananyagot. **Csak a készségnév lekérdezés** megy ki a hálózatra - az önéletrajz és az állásleírás szövegét teljesen a helyi eszközöd dolgozza fel és nem továbbítja. Ha teljesen offline működés szükséges, adj az eszközhöz egy `try/except` hibakezelőt, amely egy statikus `learn.microsoft.com` URL-t ad vissza, ha a végpont nem elérhető.

---

## Segítségkérés

Ha elakadtál a fentiek kipróbálása után:

1. **Nézd meg a szerver naplókat** - A legtöbb hiba Python stack trace-et generál a terminálban. Olvasd el a teljes hibakövetést.
2. **Keresd meg a hibaüzenetet** - Másold ki a hiba szövegét és keresd a [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) oldalon.
3. **Nyiss hibajegyet** - Nyújts be hibajegyet a [műhely tárolóban](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) a következőkkel:
   - A hibaüzenet vagy képernyőfotó
   - A csomagverzióid (`pip list | Select-String "agent-framework"`)
   - A Python verziód (`python --version`)
   - Helyi probléma vagy telepítés utáni

---

### Ellenőrzőpont

- [ ] Tudod, hogyan ellenőrizd és javítsd a `.env` konfigurációs problémákat
- [ ] Ellenőrizni tudod, hogy a csomagverziók megfelelnek-e a szükséges mátrixnak
- [ ] Tudod, hogyan nézd meg a konténer naplókat telepítési hibák esetén
- [ ] Ellenőrizni tudod az RBAC szerepköröket az Azure Portálon

---

**Előző:** [07 - Ellenőrzés a Playgroundon](07-verify-in-playground.md) · **Következő:** [09 - Összefoglalás →](09-summary.md) · **Főoldal:** [Lab 02 README](../README.md) · [Műhely főoldal](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->