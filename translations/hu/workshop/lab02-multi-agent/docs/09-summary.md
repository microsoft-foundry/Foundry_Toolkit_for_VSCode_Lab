# 9. modul - Összefoglaló & Következő lépések

⏱️ ~5 perc

**Gratulálunk!** Elkészítetted, letesztelted, és (Path A esetén) üzembe helyezted egy többügynökös munkafolyamatot a Microsoft Foundry és a Foundry Toolkit for VS Code használatával.

---

## Amit építettél

A **Önéletrajz → Munkakör-alkalmasság értékelő** - egy többügynökös hosztolt munkafolyamat, amely:
- Önéletrajzot + munkaköri leírást fogad HTTP-n keresztül (`POST /responses`)
- Négy specializált ügynököt futtat egymás után - minden ügynök továbbítja az adatokat a következőnek
- Visszaad egy alkalmassági pontszámot (0–100 bontásban), egy készség- és tanúsítványhiány listát, és egy személyre szabott tanulási térképet valódi Microsoft Learn linkekkel minden hiányhoz
- Meghívja a Microsoft Learn MCP szervert (`https://learn.microsoft.com/api/mcp`), hogy hivatalos tanulási forrásokat szerezzen minden azonosított készséghiányhoz
- Egyetlen konténerizált hosztolt ügynökként fut a Microsoft Foundry Agent Service-ben

---

## Főbb tanult fogalmak

| Fogalom | Mit gyakoroltál |
|---------|---------------|
| **Többügynökös koordináció** | `WorkflowBuilder` egymás utáni feldolgozási lánc `add_edge()` használatával |
| **Ügynök specializáció** | Négy fókuszált ügynök jobb teljesítményű, mint egy általános célú |
| **Content Router minta** | A ResumeParser router szerepét is betölti - megőrzi az JD szöveget egy `[JOB DESCRIPTION PASS-THROUGH]` szakaszban, hogy a későbbi ügynökök hozzáférhessenek (szükséges, mert `context_mode="last_agent"` esetén csak a `start_executor` látja a felhasználó nyers üzenetét) |
| **Content Relay minta** | A JD Agent továbbítja a `[PARSED RESUME PASS-THROUGH]` adatot, így a MatchingAgent mindkét profilt megkapja; elkerüli az OR-szemantika dupla triggerelést, amit a fan-in gráfok okoznak |
| **MCP eszköz integráció** | `@tool` + `streamable_http_client` egy külső MCP szerver hívásához |
| **Hosztolt ügynök életciklusa** | Vázlat készítés → Konfigurálás → Helyi tesztelés → Telepítés → Ellenőrzés a felhőben |
| **`context_mode="last_agent"`** | Minden futtató csak közvetlen elődje kimenetét látja |
| **Foundry Toolkit munkafolyamat** | Vázlat varázsló, Ügynök Ellenőrző, Munkafolyamat Vizualizáló, egykattintásos üzembe helyezés |

---

## Amit befejeztél

<details open>
<summary><strong>🅰️ A útvonal - Foundry előfizetés</strong></summary>

- [x] Ellenőrizted az 01-es labor környezetet: projekt, modell és RBAC továbbra is aktív
- [x] Többügynökös projekt alapvázat hoztál létre a Workflows sablon alapján
- [x] Négy ügynök utasítás készletet írtál (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integráltad a Microsoft Learn MCP eszközt a `streamable_http_client` segítségével
- [x] Összekötötted a munkafolyamat gráfot a `WorkflowBuilder`-rel (egymás utáni csővezeték tartalom továbbítással)
- [x] Helyi tesztelés 3 gyakorlati teszttel (Ügynök Ellenőrző) - alkalmassági pont, hiánykártyák, és MCP URL-ek
- [x] Üzembe helyezted a Foundry Agent Service-ben (konténerizált, kezelt identitással)
- [x] Ellenőrizted a felhő playground-ban - szerkezeti összhang a helyi eredményekkel

</details>

<details open>
<summary><strong>🅱️ B útvonal - Foundry Local</strong></summary>

- [x] Ellenőrizted az 01-es labor környezetet: Foundry Local fut helyi modellel
- [x] Többügynökös projekt alapvázat hoztál létre a Workflows sablon alapján
- [x] Négy ügynök utasítás készletet írtál és összekapcsoltad a munkafolyamat gráfot
- [x] Integráltad a Microsoft Learn MCP eszközt
- [x] Helyi tesztelés 3 gyakorlati teszttel
- [x] Érvényesítetted a többügynökös viselkedést felhő erőforrások nélkül

</details>

---

## Következő lépések

### Folytasd a tanulást

| Forrás | Leírás |
|----------|---------|
| **[Agent Framework SDK referencia](https://learn.microsoft.com/agent-framework/)** | API dokumentáció az `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor`-hez |
| **[MCP eszközkatalógus](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Ügynökök csatlakoztatása más MCP szerverekhez (Bing, GitHub, egyedi) |
| **[Tudás hozzáadása (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ügynökök alapozása dokumentumokkal, vektor tárolókkal vagy Bing kereséssel |
| **[Foundry értékelések](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Ügynök minőség mérés nagy skálán automatizált értékelőkkel |
| **[Microsoft Foundry dokumentáció](https://learn.microsoft.com/azure/foundry/)** | Teljes platform referencia |
| **[Foundry Toolkit - újdonságok](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Bővítmény kiadási jegyzék és változásnapló |

### Ötletek a munkafolyamat bővítésére

- **Adj hozzá egy 5. ügynököt** - Egy interjú coach-ot, amely valószínű interjú kérdéseket készít a hiányjelentés alapján
- **Adj hozzá egy Bing alapozó eszközt** - Hagyd, hogy a JD Agent hasonló álláshirdetések között keressen, hogy bővítse a követelményeket
- **Csatlakozz egy önéletrajz adatbázishoz** - Húzz le jelölt profilokat adatbázisból egy egyedi `@tool` segítségével
- **Próbálj ki különböző modelleket** - Összehasonlítva a `gpt-4.1` és a `gpt-4.1-mini` kimeneti minőségét és késleltetését
- **Értékeld a Foundry-val** - Használd az Értékelési funkciót, hogy pontozd az alkalmassági jelentéseket egy arany adathalmaz alapján

### Path B felhasználók számára: Frissítés felhőbe történő telepítéshez

Ha készen állsz a felhőbe telepítésre:
1. Szerezz egy Azure előfizetést ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fejezd be az [01-es labor, 01-es modul](../../lab01-single-agent/docs/01-setup.md) lépéseit (projekt létrehozása, modell telepítése, RBAC hozzárendelés)
3. Frissítsd az `.env` fájlodat a Foundry projekt végpontjával és a modell telepítés nevével
4. Folytasd a [06 - Telepítés Foundry-ba](06-deploy-to-foundry.md) modulból

---

## Erőforrások tisztítása (opcionális)

Ha törölni szeretnéd az ebben a workshopban létrehozott Azure erőforrásokat:

### 1. lehetőség: Töröld az erőforráscsoportot (mindent eltávolít)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 2. lehetőség: Csak a hosztolt ügynök törlése

1. Nyisd meg a [ai.azure.com](https://ai.azure.com) oldalt → a projekted → **Build** → **Agents**.
2. Találd meg a **PersonalCareerCopilot** → kattints a **Törlés** gombra.

### 3. lehetőség: A modell telepítésének törlése

1. A Foundry oldalsávban bontsd ki a projekted → **Models**.
2. Kattints jobb gombbal a modell telepítésére → **Törlés**.

> **Költség megjegyzés:** A hosztolt ügynökök csak futás közben generálnak költséget. Ha leállítod vagy törlöd az ügynököt, nincs további díj. A modell telepítés kis díjat vonhat maga után a fenntartott kapacitásért – töröld, ha végeztél vele.

---

**Előző:** [08 - Hibakeresés](08-troubleshooting.md) · **Főoldal:** [Lab 02 README](../README.md) · [Workshop főoldal](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->