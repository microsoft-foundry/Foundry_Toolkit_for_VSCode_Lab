# 7. modul - Ellenőrzés a Playgroudban

⏱️ ~10 perc

Ebben a modulban teszteled a telepített többügynökös munkafolyamatodat VS Code-ban és a Foundry Portálon, megerősítve, hogy az ügynök ugyanúgy viselkedik, mint a helyi teszteléskor.

---

## Miért teszteljünk újra telepítés után?

A hosztolt környezet néhány fontos ponton eltér a helyitől:

| | Helyi | Hosztolt |
|--|-------|--------|
| **Identitás** | A személyes bejelentkezésed (`DefaultAzureCredential`) | Ügynökönként dedikált Entra-identitás (telepítéskor automatikusan létrejön) |
| **Végpont** | `http://localhost:8088/responses` | A Foundry Agent Service által kezelt URL |
| **Hálózat** | A géped → Azure OpenAI + MCP | Azure gerinchálózat (alacsonyabb késleltetés) |

Egy hibásan beállított környezeti változó, RBAC probléma vagy blokkolt MCP kimenő hívás itt jelenne meg először.

---

## A lehetőség A: Tesztelés VS Code Playground-ban (ajánlott először)

### 1. lépés: Navigálj a hosztolt ügynöködhöz

1. Kattints a **Foundry Toolkit** ikonra a Tevékenységsávban.
2. Bontsd ki a projekted → **Hosted Agents (Preview)** → keresd meg az ügynöködet.

![Foundry Toolkit oldalsáv, amely a Hosted Agents (Preview) részt mutatja a resume-job-fit-evaluatorral és a telepített verzióival](../../../../../translated_images/hu/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### 2. lépés: Válassz verziót

1. Kattints az ügynökre a verziók kibontásához.
2. Kattints a `v1`-re → győződj meg róla, hogy az állapot **aktív** (az oldalsávon "Running" vagy "Started" is megjelenhet - mindkettő azonos készenléti állapotot jelöl).

### 3. lépés: Nyisd meg a Playground-ot

1. Kattints a **Playground**-ra (vagy jobb klikk a verzióra → **Open in Playground**).
2. Egy csevegőablak nyílik meg egy VS Code fülön.

### 4. lépés: Futtasd a füstteszteket

Használd ugyanazokat a 3 tesztet a [5. modulból](05-test-locally.md). Gépelj be minden üzenetet a Playground bemeneti mezőjébe és nyomj **Küldés**-t (vagy **Enter**-t).

#### 1. teszt - Teljes önéletrajz + álláshirdetés (standard folyamat)

Illeszd be a teljes önéletrajz + JD promptot az 5. modul 1. tesztjéből (Jane Doe + Senior Cloud Engineer a Contoso Ltd.-nél).

**Várt eredmény:**
- Illeszkedési pontszám és részletezés (100 pontos skálán)
- Megfelelő képességek szakasza
- Hiányzó képességek szakasza
- **Egy részkártya minden hiányzó képességhez** Microsoft Learn URL-ekkel
- Tanulási ütemterv idővonallal

#### 2. teszt - Gyors rövid teszt (minimális bemenet)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Várt eredmény:**
- Alacsonyabb illeszkedési pontszám (< 40)
- Őszinte értékelés szakaszos tanulási úttal
- Több részkártya (AWS, Kubernetes, Terraform, CI/CD, tapasztalati hiány)

#### 3. teszt - Magasan illeszkedő jelölt

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Várt eredmény:**
- Magas illeszkedési pontszám (≥ 80)
- Fókusz az interjúra való felkészültségen és csiszoláson
- Kevés vagy semmilyen részkártya
- Rövid idővonal a felkészülésre

### 5. lépés: Hasonlítsd össze a helyi eredményekkel

Nyisd meg a megjegyzéseidet vagy böngészőfület az 5. modulból, ahol a helyi válaszokat mentetted. Minden tesztnél:

- Ugyanaz a **struktúra** (illeszkedési pontszám, részkártyák, ütemterv)?
- Ugyanaz a **pontozási séma** (100 pontos részletes bontás)?
- A **Microsoft Learn URL-ek** még mindig jelen vannak a részkártyákban?
- Minden hiányzó képességhez **egy részkártya** (nem lerövidítve)?

> **Apró szóhasználati különbségek normálisak** - a modell nem determinisztikus. Az összes struktúrájára, pontozásának konzisztenciájára és az MCP eszköz használatára koncentrálj.

---

## B lehetőség: Teszt a Foundry Portálon

A [Foundry Portál](https://ai.azure.com) egy webalapú playgroundot kínál, amely hasznos lehet csapattagokkal vagy érdekeltekkel való megosztáshoz.

### 1. lépés: Nyisd meg a Foundry Portált

1. Nyisd meg a böngésződet, és menj a [https://ai.azure.com](https://ai.azure.com) oldalra.
2. Jelentkezz be ugyanazzal az Azure-fiókkal, amelyet a workshop során használtál.

### 2. lépés: Navigálj a projekthez

1. A kezdőlapon keresd a bal oldali sávban a **Legutóbbi projektek** részt.
2. Kattints a projekt nevére (pl. `workshop-agents`).
3. Ha nem látod, kattints az **Összes projekt** elemre és keresd meg.

### 3. lépés: Keresd meg a telepített ügynököt

1. A projekt bal oldali navigációjában kattints a **Build** → **Agents** menüre (vagy keresd az **Agents** szekciót).
2. Látnod kell egy listát az ügynökökről. Keresd meg a telepített ügynököt (pl. `resume-job-fit-evaluator`).
3. Kattints az ügynök nevére, hogy megnyisd a részletes oldalt.

### 4. lépés: Nyisd meg a Playground-ot

1. Az ügynök részletes oldalán nézd meg a felső eszköztárat.
2. Kattints az **Open in playground** (vagy **Try in playground**) gombra.
3. Megnyílik egy csevegő felület.

### 5. lépés: Futtasd ugyanazokat a füstteszteket

Ismételd meg mind a 3 tesztet az előző VS Code Playground szekcióból. Hasonlítsd össze minden választ a helyi eredményekkel (5. modul) és a VS Code Playground-ban kapott eredményekkel (A lehetőség fentebb).

---

## Többügynökös specifikus ellenőrzés

Az alap helyességen túl ellenőrizd ezeket a többügynökös specifikus viselkedéseket:

### MCP eszköz végrehajtás

| Ellenőrzés | Hogyan ellenőrizd | Átmeneti feltétel |
|-------|---------------|----------------|
| MCP hívások sikeresek | A részkártyák tartalmaznak `learn.microsoft.com` URL-eket | Valódi URL-ek, nem helyettesítő üzenetek |
| Többszörös MCP hívás | Minden magas/közepes prioritású részkártyának van erőforrása | Nem csak az első részkártya |
| MCP helyettesítés működik | Ha hiányoznak URL-ek, van helyettesítő szöveg | Az ügynök továbbra is készít részkártyákat (URL-lel vagy nélkülük) |

### Ügynök koordináció

| Ellenőrzés | Hogyan ellenőrizd | Átmeneti feltétel |
|-------|---------------|----------------|
| Mind a 4 ügynök futott | A kimenet tartalmaz illeszkedési pontszámot ÉS részkártyákat | A pontszámot a MatchingAgent adja, a kártyákat a GapAnalyzer |
| Szekvenciális futtatás | A válaszidő ésszerű (< 2 perc) | Ha > 3 perc, ellenőrizd a terminál log hibáit |
| Adatfolyam integritás | A részkártyák a matching jelentés képességeire hivatkoznak | Nincsenek kitalált képességek, amik nincsenek a JD-ben |

---

## Értékelési rubrika

Ezt a rubrikát használd a többügynökös munkafolyamat hosztolt viselkedésének értékeléséhez:

| # | Kritérium | Átmeneti feltétel | Átment? |
|---|----------|---------------|-------|
| 1 | **Funkcionális helyesség** | Az ügynök válaszol az önéletrajz + JD bemenetre illeszkedési pontszámmal és részelemzéssel | |
| 2 | **Pontozási konzisztencia** | Az illeszkedési pontszám 100 pontos skálán és részletezéssel készül | |
| 3 | **Részkártya teljesség** | Minden hiányzó képességre egy kártya van (nem rövidített vagy összefésült) | |
| 4 | **MCP eszköz integráció** | A részkártyák valós Microsoft Learn URL-eket tartalmaznak | |
| 5 | **Strukturális konzisztencia** | A kimenet struktúrája megegyezik a helyi és hosztolt futások között | |
| 6 | **Válaszidő** | A hosztolt ügynök 2 percen belül válaszol a teljes értékelésre | |
| 7 | **Nincsenek hibák** | Nincsenek HTTP 500 hibák, időtúllépések vagy üres válaszok | |

> Egy "átmenet" azt jelenti, hogy mind a 7 kritérium teljesül mind a 3 füsttesztre legalább egy playgroundban (VS Code vagy Portál).

---

## Playground hibakeresés

| Tünet | Valószínű ok | Javítás |
|---------|-------------|-----|
| A Playground nem töltődik be | A tároló nincs `active` állapotban | Lépj vissza a [6. modulhoz](06-deploy-to-foundry.md), ellenőrizd a telepítés állapotát. Várj, ha `creating` |
| Az ügynök üres választ ad | Modell telepítési név eltérés | Ellenőrizd az `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` megegyezik-e a telepített modelleddel |
| Az ügynök hibát jelez | Hiányzó [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) jogosultság | Adj hozzá **[Foundry User](https://aka.ms/foundry-ext-project-role)** (korábban Azure AI User) jogosultságot projekt szinten |
| Nincsenek Microsoft Learn URL-ek a részkártyákban | MCP kimenő hívás tiltva vagy MCP szerver nem elérhető | Ellenőrizd, hogy a konténer eléri-e a `learn.microsoft.com`-ot. Lásd [8. modul](08-troubleshooting.md) |
| Csak 1 részkártya van (rövidített) | Hiányzik a GapAnalyzer "CRITICAL" blokkja | Tekintsd át a [3. modul 2.4 lépését](03-configure-agents.md) |
| Az illeszkedési pontszám nagyon eltér a helyitől | Más modell vagy utasítások telepítve | Hasonlítsd össze az `agent.yaml` környezeti változóit a helyi `.env` fájllal. Szükség esetén telepítsd újra |
| „Agent not found” a Portálon | A telepítés még terjed vagy sikertelen | Várj 2 percet, frissítsd az oldalt. Ha továbbra hiányzik, telepítsd újra a [6. modulból](06-deploy-to-foundry.md) |

---

### Ellenőrzőpont

- [ ] Tesztelted az ügynököt VS Code Playground-ban - mind a 3 füstteszt sikeres
- [ ] Tesztelted az ügynököt a [Foundry Portál](https://ai.azure.com) Playground-jában - mind a 3 füstteszt sikeres
- [ ] A válaszok strukturálisan konzisztenssek a helyi teszteléssel (illeszkedési pontszám, részkártyák, ütemterv)
- [ ] Microsoft Learn URL-ek jelen vannak a részkártyákban (MCP eszköz működik a hosztolt környezetben)
- [ ] Egy részkártya minden hiányzó képességhez (nincs rövidítés)
- [ ] Nincsenek hibák vagy időtúllépések a tesztelés során
- [ ] Kitöltötted az értékelési rubrikát (mind a 7 kritérium teljesült)

---

**Előző:** [06 - Telepítés Foundry-ba](06-deploy-to-foundry.md) · **Következő:** [08 - Hibakeresés →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->