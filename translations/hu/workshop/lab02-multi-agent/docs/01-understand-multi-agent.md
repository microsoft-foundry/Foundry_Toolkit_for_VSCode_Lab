# 1. modul - Értsd meg a felépítést

⏱️ ~5 perc

Mielőtt bármilyen kódot írnál, itt egy gyors áttekintés arról, hogy mit építesz és hogyan működik.

---

## Amit építesz

Beillesztesz egy **önéletrajzot** és egy **állásleírást**. A munkafolyamat ezt adja vissza:

- Egy illeszkedési pontszámot (0–100, részletes bontással)
- Egy listát a hiányzó készségekről és tanúsítványokról
- Egy személyre szabott tanulási útitervet Microsoft Learn linkekkel minden hiányzó területhez

---

## A négy ügynök

Egyetlen ügynök, amely egyszerre próbálja elvégezni a feldolgozást, pontozást és tervezést, általában kapkod és sekélyes eredményt produkál. A munka négy specializált ügynökre bontása jobb eredményeket ad:

| Ügynök | Amit csinál |
|-------|--------------|
| **ResumeParser** | Feldolgozza az önéletrajzot; az állásleírást szó szerint bemásolja a `[JOB DESCRIPTION PASS-THROUGH]` mezőbe a további ügynökök számára |
| **JobDescriptionAgent** | Kinyeri az állásleírás követelményeit a pass-through-ból; továbbítja a `[PARSED RESUME]`-t mint `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | Összehasonlítja mindkét címkézett szekciót; 0–100 közötti illeszkedési pontszámot és hiánylistát készít |
| **GapAnalyzer** | Megépíti a tanulási útitervet; Microsoft Learn keresést végez minden hiányzó területre |

---

## Az összehangolási diagram

A munkafolyamat egy **sorrendben futó csővezeték** - minden ügynök átadja a kimenetét a következőnek:

```mermaid
flowchart LR
    A["Felhasználói bemenet"] --> B["Önéletrajz elemző"]
    B -- "elemzett önéletrajz + munkaköri leírás továbbítás" --> C["Munkaköri leírás ügynök"]
    C -- "munkaköri követelmények + önéletrajz továbbítás" --> D["Illesztő ügynök"]
    D -- "illeszkedési jelentés + hiányosságok" --> E["Hiányelemző + MCP"]
    E --> F["Végső kimenet"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. A **ResumeParser** megkapja a felhasználói bemenetet, feldolgozza az önéletrajzot, és bemásolja az állásleírást a `[JOB DESCRIPTION PASS-THROUGH]` mezőbe.
2. A **JD Agent** kinyeri a strukturált követelményeket, és továbbítja a `[PARSED RESUME PASS-THROUGH]`-t.
3. A **MatchingAgent** összehasonlítja a két szekciót, és illeszkedési pontszámot, valamint hiánylistát készít.
4. A **GapAnalyzer** elkészíti az útitervet, és minden hiányzó területhez meghívja a Microsoft Learn MCP eszközét.

---

## Hogyan kapcsolódik mindez a kódhoz

A `main.py` fájlban a `WorkflowBuilder` segítségével írod le ezt a gráfot:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # első ügynök, aki megkapja a felhasználói bemenetet
        output_executors=[gap_executor],      # utolsó ügynök - az ő kimenete a válasz
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JD ügynök
    .add_edge(jd_executor, matching_executor)     # JD ügynök → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

Minden `Agent` egy `AgentExecutor`-be van csomagolva. Az `add_edge()` hívások szigorúan sorrendben futó csővezetéket definiálnak - minden ügynök csak az előző közvetlen kimenetét kapja meg.

> A `context_mode="last_agent"` azt jelenti, hogy minden executor csak az előző közvetlen kimenetét látja. A ResumeParser és JD Agent továbbítják az adatokat címkézett szekciókban, így minden további ügynök pontosan azt kapja, amire szüksége van.

---

## Az MCP eszköz

A GapAnalyzer-nek egyetlen eszköze van: `search_microsoft_learn_for_plan`. Ez a `https://learn.microsoft.com/api/mcp`-hez kapcsolódik, és valós Microsoft Learn linkeket ad vissza minden hiányzó készséghez.

Az eszköz futtatásakor ezek a naplók jelennek meg - mind várt eredmény:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

Csak akkor aggódj, ha a `POST` hibát jelez vissza.

---

**Előző:** [00 - Előfeltételek](00-prerequisites.md) · **Következő:** [02 - A projekt felépítése →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->