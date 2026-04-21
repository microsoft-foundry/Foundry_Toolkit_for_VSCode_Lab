# Lab 02 - Többügynökös munkafolyamat: Önéletrajz → Állásalkalmasság értékelő

## Teljes tanulási útvonal

Ez a dokumentáció végigvezet azon, hogyan építsünk, teszteljünk és telepítsünk egy **többügynökös munkafolyamatot**, amely négy specializált ügynök segítségével, a **WorkflowBuilder** által koordinálva értékeli az önéletrajz és az állás közötti illeszkedést.

> **Előfeltétel:** A Lab 01 - Egyetlen ügynök befejezése [Lab 01 - Single Agent](../../lab01-single-agent/README.md) szükséges a Lab 02 elkezdése előtt.

---

## Modulok

| # | Modul | Mit fogsz csinálni |
|---|--------|--------------------|
| 0 | [Előfeltételek](00-prerequisites.md) | A Lab 01 befejezésének ellenőrzése, a többügynökös koncepciók megértése |
| 1 | [Többügynökös architektúra megértése](01-understand-multi-agent.md) | Megismerni a WorkflowBuilder-t, az ügynökök szerepét, az összehangolási gráfot |
| 2 | [A többügynökös projekt felvázolása](02-scaffold-multi-agent.md) | A Foundry bővítmény használata többügynökös munkafolyamat felvázolásához |
| 3 | [Ügynökök és környezet konfigurálása](03-configure-agents.md) | 4 ügynök utasításainak megírása, MCP eszköz konfigurálása, környezeti változók beállítása |
| 4 | [Összehangolási minták](04-orchestration-patterns.md) | Párhuzamos kibontás, soros összegzés és alternatív minták felfedezése |
| 5 | [Helyi tesztelés](05-test-locally.md) | F5-ös hibakeresés Agent Inspectorral, smoke tesztek futtatása önéletrajzzal és állásleírással |
| 6 | [Telepítés Foundry-ba](06-deploy-to-foundry.md) | Konténer építése, ACR-be tolás, hosztolt ügynök regisztrálása |
| 7 | [Ellenőrzés a Playgroundban](07-verify-in-playground.md) | A telepített ügynök tesztelése VS Code és Foundry Portal playground környezetekben |
| 8 | [Hibakeresés](08-troubleshooting.md) | Gyakori többügynökös problémák javítása (MCP hibák, levágott kimenet, csomagverziók) |

---

## Becsült idő

| Tapasztalati szint | Idő |
|--------------------|-----|
| Nemrég befejezett Lab 01 | 45-60 perc |
| Néhány Azure AI tapasztalat | 60-90 perc |
| Többügynökökkel először | 90-120 perc |

---

## Architektúra áttekintés

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Vissza ide:** [Lab 02 README](../README.md) · [Workshop főoldal](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:  
Ez a dokumentum az [Co-op Translator](https://github.com/Azure/co-op-translator) AI fordító szolgáltatás segítségével készült. Bár törekszünk a pontosságra, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Kritikus információk esetén professzionális emberi fordítást javaslunk. Nem vállalunk felelősséget az ebből a fordításból eredő félreértésekért vagy félreértelmezésekért.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->