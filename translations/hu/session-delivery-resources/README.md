# Hogyan add elő ezt az ülést

Köszönjük, hogy előadod ezt az ülést!

Az esemény megtartása előtt, kérjük:

1. Olvasd el ezt a dokumentumot és az összes csatolt anyagot teljes egészében.
2. Nézd meg az ülés felvételét és a workshop teljes végigvezetését.
3. Menj végig mindkét gyakorlati laboron teljes egészében a saját gépeden **legalább egyszer** az esemény előtt.
4. Érvényesítsd a Microsoft Foundry projektedet, modell telepítéseket és kvótákat.
5. Ha bármi nem világos, fordulj a karbantartóhoz.

---

## Fájl összefoglaló

| Erőforrás                      | Link                                                                             | Leírás                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop diákkészlet           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Prezentáció diákkal a workshophoz, előadói jegyzetekkel és beágyazott demóvideókkal        |
| Ülés felvétel                 | _A karbantartó fogja biztosítani_                                               | Workshop bevezető és diák bemutatása felvételen                                              |
| Workshop végigvezetés         | _A karbantartó fogja biztosítani_                                               | Mindkét labor végigvezetése a tanuló szemszögéből rögzítve                              |
| Workshop dokumentáció         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Forrás repository, labor README fájlok, lépésről lépésre modulok                                       |
| Labor 01 - egyetlen ügynök     | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Gyakorlati labor: építsd meg, teszteld és telepítsd az *Explain Like I'm an Executive* hosztolt ügynököt     |
| Labor 02 - több ügynök munkafolyamat | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Gyakorlati labor: építsd meg a 4-ügynökös *Resume to Job Fit Evaluator* munkafolyamatot                     |
| Demó 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Labor 01 demó: szakkifejezések lefordítása vezetői összefoglalóra                          |
| Demó 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Labor 02 demó: 4-ügynökös munkafolyamat, amely értékeli az önéletrajz és az állás megfelelését és javaslatokat készít     |

> **Megjegyzés oktatóknak:** A dia és videó linkek a felvételek megjelenése után kerülnek hozzáadásra. Addig is keressétek a karbantartót (lásd [Elérhetőségek](#kapcsolatok)) a legfrissebb anyagokért.

---

## Kezdés

Ez a workshop megtanítja a fejlesztőknek, hogyan építsenek, teszteljenek és telepítsenek MI ügynököket a **Microsoft Foundry Agent Service**-hez, mint **Hosztolt Ügynököket**, teljes egészében a VS Code használatával, a **Microsoft Foundry Toolkit** kiterjesztés segítségével.

A workshop több részből áll, beleértve a diákat, **2 élő demót** és **2 gyakorlati labort**.

### Időzítés

#### Teljes előadás (kb. 2 óra)

| Idő            | Leírás                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Bevezető: hosztolt ügynökök, Foundry Agent Service és toolkit         |
| 10:00 - 20:00   | Demó: Executive Agent végigvezető bemutató                                     |
| 20:00 - 60:00   | Labor 01 - egyetlen ügynök (építés, helyi tesztelés, telepítés, játszótér)     |
| 60:00 - 110:00  | Labor 02 - több ügynökös munkafolyamat (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00 | Összegzés, kérdések és válaszok, és további tanulási források                       |

#### Rövid előadás (kb. 75 perc)

| Idő          | Leírás                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Bevezető és áttekintés                                           |
| 10:00 - 20:00 | Demó: Executive Agent                                        |
| 20:00 - 70:00 | Csak Labor 01 (a résztvevőket irányítani Labor 02 önálló ütemezésére)        |
| 70:00 - 75:00 | Összegzés és kérdések                                              |

### Előkészület

| Erőforrás                       | Link                                                                                          | Leírás                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Workshop dokumentáció         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Workshop dokumentáció és forrás                 |
| Labor 01 utasítások            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Gyakorlati labor: egy hosztolt ügynök                 |
| Labor 02 utasítások            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Gyakorlati labor: több ügynökös munkafolyamat                |
| Előfeltételek lista        | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Eszközök, fiókok és Azure hozzáférés szükséges        |
| Hosztolt ügynökök gyors kezdés (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Hivatalos gyors kezdés az `azd`-vel történő hosztolt ügynök telepítéshez |
| Hosztolt ügynökök régió elérhetősége | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Hosztolt ügynökök támogatott régiói (előnézet)     |

### Oktatói előfeltételek

Az előadás megtartása előtt győződj meg róla, hogy rendelkezel:

- Egy **Azure előfizetés** erőforrás létrehozási jogosultsággal (Tulajdonos vagy Közreműködő egy erőforráscsoporton).
- Hozzáférés egy **Microsoft Foundry projekthez** egy [hosztolt ügynököket támogató régióban](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvóta a **gpt-4.1** (vagy **gpt-4.1-mini**) használatához a Foundry projektedben.
- A következő eszközök telepítve:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit kiterjesztés](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (opcionális)
  - Python 3.10 vagy újabb

Futtasd a [Hosztolt ügynökök azd-vel gyors kezdését](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) legalább egyszer az előadás előtt, hogy rendelkezz ismert, működő Foundry projekttel, modell telepítéssel és Azure Container Registry-vel, amelyre hivatkozhatsz, ha egy tanuló elakad.

---

## Diák végigvezetése

A diákkészlet követi a laborok menetét. Minden szakaszhoz javasolt beszédpontok:

| Szakasz                     | Kulcsüzenet                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Cím és napirend            | Keretezd úgy a workshopot, hogy *VS Code-tól Foundry-ig* portal váltás nélkül.                                |
| Miért hosztolt ügynökök?          | Kezelt futtató környezet, ACR alapú telepítés, OpenAI-kompatibilis `/responses` API, Foundry projektekre korlátozva.        |
| Architektúra ábra        | Vezesd végig a [README architektúrán](../README.md#architecture): sablon, Inspector, ACR, Agent Service.   |
| Hosztolt ügynök anatómiája   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - mit csinál mindegyik fájl.                              |
| Élő demó: Executive Agent  | Válts VS Code-ra és futtasd végig a [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demót (lásd [Demo 1](#demó-1-executive-agent)). |
| Élő demó: Resume to Job Fit Evaluator | Válts VS Code-ra és futtasd a [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-ügynökös demót (lásd [Demo 2](#demó-2-resume-to-job-fit-evaluator)). |
| Labor 01 röviden                | Átadod a tanulóknak. Mutass rá a [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md) dokumentációra. |
| Több ügynökös minták        | Sorrendben, párhuzamos, átadásos minták - előnézet a Labor 02 előtt.                                           |
| Labor 02 röviden                | Átadod a tanulóknak. Mutass rá a [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md) dokumentációra. |
| Összegzés és források       | További tanulási források a [További erőforrások](#további-források) szakaszból.                      |

---

## Demók

Két élő demó tartozik az előadás anyagához. Mindkettőre szánj 10 percet.

| Demó | Labor | Fájlok | Mit mutassunk |
|------|-----|-------|--------------|
| Executive Agent | Labor 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Egyetlen hosztolt ügynök; műszaki zsargont lefordít vezetői összefoglalóvá |
| Resume to Job Fit Evaluator | Labor 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-ügynökös koordináció; értékeli az önéletrajz-állás illeszkedést és ajánlást készít |

### Demó 1: Executive Agent

Egy különálló ügynök a [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) könyvtárban. Használd ezt a 10 perces demót a Labor 01 előtt.

1. Nyisd meg a [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py)-t és tekintsd át az ügynök definícióját (rendszer prompt, modell, keretrendszer).
2. Nyomd meg az `F5` gombot, hogy elindítsd a **Agent Inspector**-t helyben.
3. Illeszd be a minta promptot a [README](../README.md#see-it-in-action) alapján és mutasd be a vezetői összefoglaló válaszát.
4. Mutasd meg a [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) és a [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) fájlokat, hogy elmagyarázd a telepítési elemeket.
5. Mutass be a telepítési folyamatot (Docker build, ACR push, hosztolt ügynök létrehozás) anélkül, hogy megvárnád a befejezést.

### Demó 2: Resume to Job Fit Evaluator

Egy 4-ügynökös munkafolyamat a [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) könyvtárban. Használd ezt a 10 perces demót a Labor 02 előtt.

1. Nyisd meg a [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)-t és mutasd meg, hogyan vannak összeépítve a négy ügynök egy szekvenciális koordinációban.
2. Nyomd meg az `F5` gombot a **Agent Inspector** elindításához a több ügynökös munkafolyamathoz.
3. Illeszd be egy rövid állásleírást és egy minta önéletrajzot az Inspector chat-be.
4. Vezesd végig a négy ügynökös csővezetéket: önéletrajz elemző, álláskövetelmény kinyerő, illeszkedés pontozó és ajánlás író.
5. Mutasd meg, hogyan válik minden alügynök kimenete a következő ügynök kontextusává, kiemelve az átadási mintát.
6. Mutasd meg a [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) fájlt, hogy összehasonlítsd az egy ügynökös verzióval az 1-es demóból.

---

## Előadási tippek

- **Állítsd be az elvárásokat korán.** A hosztolt ügynökök előnézetben vannak - hangsúlyozd a régióbeli korlátokat és kvótákat, hogy a résztvevők ne lepődjenek meg a labor közben.
- **Először futtasd le az előfeltételek ellenőrző feladatot.** Mindkét labor tartalmaz egy `Validate prerequisites` VS Code feladatot - ezt futtasd le a kódírás előtt.
- **Tartsd láthatóan az Agent Inspectort.** A legtöbb „aha” pillanat akkor történik, amikor a tanulók látják a helyi `/responses` körforgás világítását.
- **Legyen tartalék projekted.** Ha egy tanuló Foundry projektje eléri a kvótahatárt, ossz meg egy előre előkészített projektet a telepítési lépéshez, hogy ne álljon meg a csoport.
- **Párosítsd a résztvevőket.** A Labor 02 (több ügynök) jelentősen könnyebb, ha a tanulók kettesével megbeszélhetik a koordinációt.
- **Használd a docs modulokat vezérpontokként.** Minden labor `docs/` mappája 8 számozott modulra van osztva - használd ezeket természetes szünetekként.
- **Előre húzd le az alap Docker képet** megosztott lab gépeken, hogy elkerüld a registry korlátozásokat.

---

## Hibaelhárítás az előadás során

| Tünet                                      | Első teendő                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Az Agent Inspector nem tud kapcsolódni               | Ellenőrizd, hogy a `8088` port szabad-e és fut-e a `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` feladat.   |
| A hibakereső nem csatlakozik                     | Nézd meg, hogy a `5679` port szabad-e; indítsd újra a VS Code-ot, ha a `debugpy` már foglalt.                           |
| `azd up` hitelesítési hibát ad               | Futtasd az `az login` és `azd auth login` parancsokat, ellenőrizd, hogy a megfelelő bérlő van kiválasztva.                              |
| A telepítés beragad az ACR push-nál                 | Ellenőrizd, hogy fut-e a Docker Desktop és van-e `AcrPush` jogosultságod a registry-ben.                              |
| A modell 404-et ad vissza / deployment-not-found     | Az agent.yaml-ban lévő modell telepítés nevének meg kell egyeznie a Foundry projektben lévő telepítéssel.              |

| A hosztolt ügynök `Provisioning` állapotban ragadt         | Ellenőrizze, hogy a projekt régiója [támogatja-e a hosztolt ügynököket](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) és hogy van-e kvóta elérhető. |
| A Playground 401-es hibát ad vissza                  | Jelentkezzen be újból a Foundry kiterjesztésbe a VS Code tevékenységi sávján keresztül.          |

Mélyebb útmutatásért minden labor saját `08-troubleshooting.md` fájlt tartalmaz – irányítsa a tanulókat oda:

- Labor 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Labor 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## A foglalkozás testreszabása

Nyugodtan alakítsa a workshopot a saját közönsége igényeihez. Gyakori változatok:

- **Backend közönségek:** több időt szánjon az `agent.yaml`-ra, a Dockerre és az ACR-re; csökkentse a playground bemutatót.
- **Citizen-developer közönségek:** maradjanak a Foundry kiterjesztés UI-jában az alapozásra; csökkentsék a CLI lépéseket.
- **Egysávos 60 perces időkeret:** csak az bevezetés, bemutató és az 01-es labor.
- **Workshop-only (nincs diákkal) formátum:** nyissa meg mindkét labor README-jét és használja őket elsődleges forgatókönyvként.

Ha kiterjeszti a laborokat, kérjük, járuljon hozzá a változtatásokkal PR-en keresztül, hogy más oktatók is hasznot húzhassanak belőle.

---

## További források

- [Microsoft Foundry dokumentáció](https://learn.microsoft.com/azure/ai-foundry/)
- [Hosztolt ügynökök áttekintése](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Gyors kezdés: telepítse első hosztolt ügynökét (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Hosztolt ügynök telepítése (hogyan)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit VS Code-hoz](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kapcsolatok

Ha kérdése van a foglalkozás megtartásával kapcsolatban, kérjük, nyisson egy hibajegyet a [workshop adattárban](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) és jelölje meg a karbantartót.

| Szerep             | Név            | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Karbantartó / kapcsolat| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->