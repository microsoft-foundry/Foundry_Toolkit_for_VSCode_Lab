# Labor 02 - Többügynökös munkafolyamat: Önéletrajz → Állásalkalmassági értékelő

## Teljes tanulási útvonal

Ez a dokumentáció végigvezeti Önt egy **többügynökös munkafolyamat** építésén, tesztelésén és telepítésén, amely az önéletrajz és az állás megfelelőségét értékeli négy speciális ügynök segítségével, azokat a **WorkflowBuilder** irányítja.

> **Előfeltétel:** A Labor 02 elkezdése előtt fejezze be a [Labor 01 - Egy ügynök](../../lab01-single-agent/README.md) munkát.

---

## Modulok

| # | Modul | Amit csinálni fogsz |
|---|--------|--------------------|
| 0 | [Bevezetés](00-prerequisites.md) | Amit építeni fogsz, Labor 01 ellenőrzése, Labor 02 és Labor 01 összehasonlítása |
| 1 | [A többügynökös architektúra megértése](01-understand-multi-agent.md) | Ismerkedj a WorkflowBuilderrel, az ügynöki szerepekkel, az összehangolási gráffal |
| 2 | [A többügynökös projekt alapjainak létrehozása](02-scaffold-multi-agent.md) | Használd a Foundry kiterjesztés varázslóját az alapprojekt előkészítéséhez |
| 3 | [Ügynökök és környezet konfigurálása](03-configure-agents.md) | Írj utasításokat 4 ügynök számára, konfiguráld az MCP eszközt, állítsd be a környezeti változókat |
| 4 | [Összehangolási minták](04-orchestration-patterns.md) | Szekvenciális lánc, tartalom továbbítás, és WorkflowBuilder VAGY-szemantika |
| 5 | [Helyi tesztelés](05-test-locally.md) | F5 hibakeresés Agent Inspectorral, smoke tesztek futtatása önéletrajzzal + állásleírással |
| 6 | [Telepítés a Foundryba](06-deploy-to-foundry.md) | Konténer építése, feltöltés az ACR-be, hosztolt ügynök regisztrálása |
| 7 | [Ellenőrzés a Playground-ban](07-verify-in-playground.md) | Telepített ügynök tesztelése VS Code és Foundry Portal playgroundokban |
| 8 | [Hibakeresés](08-troubleshooting.md) | Gyakori többügynökös problémák javítása (MCP hibák, rövidült kimenet, csomag verziók) |
| 9 | [Összefoglaló & Következő lépések](09-summary.md) | Amit építettél, elsajátított kulcskoncepciók, takarítás, és merre tovább |

---

**Vissza ide:** [Labor 02 README](../README.md) · [Workshop kezdőlap](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->