# Modul 1 - Pochopení architektury

⏱️ ~5 minut

Než začnete psát kód, zde je rychlý přehled toho, co vytváříte a jak to funguje.

---

## Co vytváříte

Vložíte **životopis** a **popis pracovní pozice**. Workflow vrátí:

- Skóre shody (0–100 s rozpisem)
- Seznam dovednostních a certifikačních mezer
- Personalizovanou učební cestu s odkazy na Microsoft Learn pro každou mezeru

---

## Čtyři agenti

Jeden agent, který se snaží vše analyzovat, hodnotit a plánovat najednou, má tendenci spěchat a produkovat povrchní výsledky. Rozdělení práce do čtyř specializovaných agentů přináší lepší výsledky:

| Agent | Co dělá |
|-------|-------------|
| **ResumeParser** | Analyzuje životopis; doslovně zkopíruje popis práce do `[JOB DESCRIPTION PASS-THROUGH]` pro další agenty |
| **JobDescriptionAgent** | Extrahuje požadavky z popisu práce; přeposílá `[PARSED RESUME]` dále jako `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | Porovnává obě označené části; vytváří skóre shody 0–100 a seznam mezer |
| **GapAnalyzer** | Vytváří učební cestu; hledá na Microsoft Learn pro každou mezeru |

---

## Orchestrace grafu

Workflow je **sekvenční pipeline** - každý agent předává svůj výstup dalšímu:

```mermaid
flowchart LR
    A["Vstup uživatele"] --> B["Parser životopisu"]
    B -- "zpracovaný životopis + přenos popisu práce" --> C["Agent popisu práce"]
    C -- "požadavky popisu práce + přenos životopisu" --> D["Agent pro shodu"]
    D -- "zpráva o shodě + mezery" --> E["Analýza mezer + MCP"]
    E --> F["Konečný výstup"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** obdrží vstup od uživatele, analyzuje životopis a zkopíruje popis práce do `[JOB DESCRIPTION PASS-THROUGH]`.
2. **JD Agent** extrahuje strukturované požadavky a přeposílá `[PARSED RESUME PASS-THROUGH]` dále.
3. **MatchingAgent** porovnává obě části a vytvoří skóre shody a seznam mezer.
4. **GapAnalyzer** vytvoří plán a zavolá nástroj Microsoft Learn MCP pro každou mezeru.

---

## Jak to odpovídá kódu

V `main.py` popisujete tento graf pomocí `WorkflowBuilder`:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # první agent, který přijímá vstup uživatele
        output_executors=[gap_executor],      # poslední agent - jeho výstup je odpověď
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JD agent
    .add_edge(jd_executor, matching_executor)     # JD agent → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

Každý `Agent` je zabalen do `AgentExecutor`. Volání `add_edge()` definují přísně sekvenční pipeline - každý agent přijímá pouze výstup svého přímého předchůdce.

> `context_mode="last_agent"` znamená, že každý executor vidí pouze výstup svého přímého předchůdce. ResumeParser a JD Agent přeposílají data ve označených částech, takže každý následující agent má přesně to, co potřebuje.

---

## Nástroj MCP

GapAnalyzer má jeden nástroj: `search_microsoft_learn_for_plan`. Připojuje se na `https://learn.microsoft.com/api/mcp` a vrací skutečné odkazy Microsoft Learn pro každou dovednostní mezeru.

Když se nástroj spustí, uvidíte tyto logy - všechny očekávané:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

Starosti si dělejte pouze tehdy, pokud `POST` vrátí chybu.

---

**Předchozí:** [00 - Požadavky (prerequisites)](00-prerequisites.md) · **Další:** [02 - Vytvoření kostry projektu →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->