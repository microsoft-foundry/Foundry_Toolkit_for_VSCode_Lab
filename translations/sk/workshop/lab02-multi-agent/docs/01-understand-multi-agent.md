# Modul 1 - Pochopte architektúru

⏱️ ~5 min

Predtým, než začnete písať akýkoľvek kód, tu je rýchly prehľad toho, čo vytvárate a ako to funguje.

---

## Čo vytvárate

Vložíte **životopis** a **popis práce**. Pracovný tok vráti:

- Hodnotenie zhody (0–100 s rozpisom)
- Zoznam medzier v zručnostiach a certifikáciách
- Personalizovanú učebnú cestu s odkazmi na Microsoft Learn pre každú medzeru

---

## Štyria agenti

Jeden agent, ktorý sa snaží spracovať, ohodnotiť a naplánovať všetko naraz, má tendenciu ponáhľať sa a produkovať povrchné výsledky. Rozdelenie práce na štyroch špecializovaných agentov prináša lepšie výsledky:

| Agent | Čo robí |
|-------|---------|
| **ResumeParser** | Spracuje životopis; prepíše popis práce doslovne do `[JOB DESCRIPTION PASS-THROUGH]` pre ďalších agentov |
| **JobDescriptionAgent** | Extrahuje požiadavky z popisu práce; posiela ďalej `[PARSED RESUME]` ako `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | Porovnáva označené sekcie; vytvára skóre zhody 0–100 a zoznam medzier |
| **GapAnalyzer** | Vytvára učebnú cestu; vyhľadáva na Microsoft Learn pre každú medzeru |

---

## Orchestration graph

Pracovný tok je **sekvenčný pipeline** - každý agent odovzdáva svoj výstup ďalšiemu:

```mermaid
flowchart LR
    A["Vstup používateľa"] --> B["Parser životopisu"]
    B -- "analyzovaný životopis + prenos popisu práce" --> C["Agent pre popis práce"]
    C -- "požiadavky z popisu práce + prenos životopisu" --> D["Agent zhody"]
    D -- "správa zhody + medzery" --> E["Analýza medzier + MCP"]
    E --> F["Konečný výstup"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** prijme používateľský vstup, spracuje životopis a prepíše popis práce do `[JOB DESCRIPTION PASS-THROUGH]`.
2. **JD Agent** extrahuje štruktúrované požiadavky a posiela ďalej `[PARSED RESUME PASS-THROUGH]`.
3. **MatchingAgent** porovnáva obe sekcie a vytvára skóre zhody a zoznam medzier.
4. **GapAnalyzer** vytvára cestovnú mapu a volá nástroj Microsoft Learn MCP pre každú medzeru.

---

## Ako sa to mapuje do kódu

V `main.py` popisujete tento graf pomocou `WorkflowBuilder`:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # prvý agent na prijatie vstupu od používateľa
        output_executors=[gap_executor],      # posledný agent - jeho výstup je odpoveď
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → agent pracovnej ponuky
    .add_edge(jd_executor, matching_executor)     # agent pracovnej ponuky → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

Každý `Agent` je zabalený v `AgentExecutor`. Volania `add_edge()` definujú striktne sekvenčný pipeline - každý agent dostáva iba výstup jeho priameho predchodcu.

> `context_mode="last_agent"` znamená, že každý vykonávateľ vidí iba výstup svojho priameho predchodcu. ResumeParser a JD Agent preposielajú dáta v označených sekciách tak, aby každý ďalší agent mal presne to, čo potrebuje.

---

## Nástroj MCP

GapAnalyzer má jeden nástroj: `search_microsoft_learn_for_plan`. Pripája sa k `https://learn.microsoft.com/api/mcp` a vracia skutočné odkazy Microsoft Learn pre každú medzeru v zručnostiach.

Keď sa nástroj spustí, uvidíte tieto záznamy - všetko očakávané:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

Obávajte sa iba, keď `POST` vráti chybu.

---

**Predchádzajúce:** [00 - Požiadavky](00-prerequisites.md) · **Ďalšie:** [02 - Nastavte projekt →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->