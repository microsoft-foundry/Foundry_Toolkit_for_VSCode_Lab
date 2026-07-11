# Laboratoř 02 - Víceagentní pracovní postup: Hodnocení shody životopisu s pracovním místem

## Kompletní učební cesta

Tato dokumentace vás provede tvorbou, testováním a nasazením **víceagentního pracovního postupu**, který vyhodnocuje shodu životopisu s pracovním místem pomocí čtyř specializovaných agentů řízených přes **WorkflowBuilder**.

> **Požadavek:** Před zahájením laboratorního cvičení 02 dokončete [Laboratoř 01 - Jeden agent](../../lab01-single-agent/README.md).

---

## Moduly

| # | Modul | Co budete dělat |
|---|--------|-----------------|
| 0 | [Úvod](00-prerequisites.md) | Co vytvoříte, ověření Laboratoře 01, srovnání Laboratoře 02 a 01 |
| 1 | [Porozumění víceagentní architektuře](01-understand-multi-agent.md) | Naučte se WorkflowBuilder, role agentů, graf orchestraci |
| 2 | [Vytvoření kostry víceagentního projektu](02-scaffold-multi-agent.md) | Použijte průvodce rozšířením Foundry pro vytvoření základního projektu |
| 3 | [Konfigurace agentů a prostředí](03-configure-agents.md) | Napište instrukce pro 4 agenty, nakonfigurujte nástroj MCP, nastavte proměnné prostředí |
| 4 | [Orchestrace vzory](04-orchestration-patterns.md) | Sekvenční řetězec, předávání obsahu a OR-semantika WorkflowBuilder |
| 5 | [Testování lokálně](05-test-locally.md) | Ladění pomocí F5 a Agent Inspector, spuštění jednoduchých testů s životopisem a popisem práce |
| 6 | [Nasazení do Foundry](06-deploy-to-foundry.md) | Vytvoření kontejneru, push do ACR, registrace hostovaného agenta |
| 7 | [Ověření v Playground](07-verify-in-playground.md) | Testování nasazeného agenta v prostředích VS Code a Foundry Portal playground |
| 8 | [Řešení problémů](08-troubleshooting.md) | Oprava běžných problémů s víceagenty (chyby MCP, oříznutý výstup, verze balíčků) |
| 9 | [Shrnutí a další kroky](09-summary.md) | Co jste vytvořili, klíčové naučené koncepty, úklid a kam pokračovat dále |

---

**Zpět na:** [Laboratoř 02 README](../README.md) · [Domovská stránka workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->