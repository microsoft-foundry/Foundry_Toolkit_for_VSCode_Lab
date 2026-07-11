# 7. modul - Összefoglaló és következő lépések

⏱️ ~5 perc

**Gratulálunk!** Létrehoztál, teszteltél, és (ha az A útvonalon vagy) üzembe helyeztél egy hosztolt AI ügynököt a Microsoft Foundry és a Foundry Toolkit for VS Code segítségével.

---

## Amit létrehoztál

Egy **„Magyarázd el, mintha vezető lennék”** ügynököt, amely:
- Műszaki eseményjelentéseket vagy operatív frissítéseket fogad HTTP-n keresztül (`POST /responses`)
- Egyszerű, vezetői összefoglalókra fordítja őket
- Egy strukturált kimeneti formátumot követ (Mi történt / Üzleti hatás / Következő lépés)
- Elutasítja a témán kívüli kéréseket és a prompt injekciós kísérleteket
- Konténerizált hosztolt ügynökként fut a Microsoft Foundry Agent Service-ben

---

## Fontos fogalmak, amiket megtanultál

| Fogalom | Mit gyakoroltál |
|---------|-------------------|
| **Agent Framework architektúra** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` folyamat |
| **Hosztolt ügynök életciklus** | Vázlatkészítés → Konfigurálás → Helyi tesztelés → Üzembe helyezés → Felhőben ellenőrzés |
| **Rendszer prompt tervezés** | Szerep, célközönség, kimeneti formátum, szabályok, biztonsági korlátok, példák |
| **Helyi vs. hosztolt különbségek** | Identitás (személyes hitelesítő vs. kezelt identitás), végpont, hálózati útvonal |
| **Biztonsági határok** | Prompt injekció elleni védelem, szerep megtartása, szélsőséges helyzetek elegáns kezelése |
| **Foundry Toolkit munkafolyamat** | Projekt létrehozása, modell üzembe helyezése, ügynök vázlatkészítése, Agent Inspector, egérkattintásos üzembe helyezés |

---

## Amit befejeztél

### A út (Foundry előfizetés)

- [x] Beállítottad a Foundry Toolkit-et és létrehoztál egy Foundry projektet egy üzembe helyezett modellel
- [x] Vázoltál egy hosztolt ügynököt automatikusan generált projektstruktúrával
- [x] Megírtál strukturált ügynök utasításokat biztonsági szabályokkal
- [x] Helyileg tesztelted három funkcionális forgatókönyvvel (Agent Inspector)
- [x] Üzembe helyezted a Foundry Agent Service-ben (konténerizált)
- [x] Felhős környezetben ellenőrizted négy szélsőséges/biztonsági teszttel

### B út (Foundry Local)

- [x] Beállítottad a Foundry Toolkit-et helyi modell végponttal
- [x] Vázoltál egy hosztolt ügynök projektet
- [x] Megírtál strukturált ügynök utasításokat biztonsági szabályokkal
- [x] Helyileg tesztelted három funkcionális forgatókönyvvel
- [x] Ellenőrizted az ügynök viselkedését felhő alapú erőforrások nélkül

---

## Következő lépések

### Tanulás folytatása

| Forrás | Leírás |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Négy ügynökös munkafolyamat építése (Önéletrajz → Munkaalkalmasság értékelő) összehangolási mintákkal |
| **[Eszközök hozzáadása az ügynöködhöz](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | API-k, adatbázisok vagy egyedi funkciók csatlakoztatása az Eszköztár segítségével |
| **[Tudás hozzáadása (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ügynököd megalapozása dokumentumokkal, vektortárolókkal vagy Bing kereséssel |
| **[Microsoft Foundry dokumentáció](https://learn.microsoft.com/azure/foundry/)** | Teljes platform referencia |
| **[Agent Framework SDK referencia](https://learn.microsoft.com/agent-framework/)** | `agent-framework` csomag API dokumentáció |
| **[Foundry Toolkit - Újdonságok](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Bővítmény kiadási jegyzetek és változásnapló |

### Ötletek az ügynököd bővítéséhez

- **Adj hozzá dátumeszközt** - Engedd, hogy az ügynök „mai napon” kontextust foglaljon összegekbe
- **Csatlakozz egy eseményadatbázishoz** - Valós eseményadatokat húzz eszköz funkción keresztül
- **Adj hozzá Bing megalapozó eszközt** - Engedd, hogy az ügynök frissebb híreket nézzen meg további kontextusért
- **Próbálj ki különböző modelleket** - Hasonlítsd össze a `gpt-4.1` és `gpt-4.1-mini` kimeneti minőségét
- **Értékeld a Foundry segítségével** - Használd az Értékelések funkciót az ügynök minőségének mérése érdekében nagy skálán

### B útvonal használóinak: Frissítés felhős üzembe helyezésre

Ha készen állsz a felhőbe történő telepítésre:
1. Szerezz egy Azure előfizetést ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fejezd be az [1. modult, Beállítás](01-setup.md#step-2-set-up-based-on-your-access) (projekt létrehozása, modell üzembe helyezése, RBAC hozzárendelése)
3. Frissítsd a `.env` fájlodat a Foundry projekt végpontjával és a modell üzembe helyezés nevével
4. Folytasd a [5. modul - Foundry-be telepítés](05-deploy-to-foundry.md) anyaggal

---

## Erőforrások tisztítása (opcionális)

Ha el szeretnéd távolítani az ebben a workshopban létrehozott Azure erőforrásokat:

### 1. lehetőség: Erőforráscsoport törlése (mindent eltávolít)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 2. lehetőség: Csak a hosztolt ügynök törlése

1. Nyisd meg az [ai.azure.com](https://ai.azure.com) oldalt → a projekted → **Build** → **Agents**.
2. Kattints az ügynöködre → majd a **Törlés** gombra.

### 3. lehetőség: A modell üzembe helyezés törlése

1. A Foundry oldalsávban bontsd ki a projektedet → **Models**.
2. Kattints jobb gombbal a modell üzembe helyezésére → **Törlés**.

> **Költség megjegyzés:** A hosztolt ügynökök csak futás közben generálnak költséget. Ha leállítod vagy törlöd az ügynököt, nincs folyamatos díj. A modell üzembe helyezés kis díjat vonhat maga után a fenntartott kapacitásért — töröld, ha már nincs rá szükség.

---

**Előző:** [06 - Playground Ellenőrzés](06-verify-in-playground.md) · **Következő:** [08 - Hibakeresés (Referencia) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->