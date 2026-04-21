# Laboratoř 02 - Víceagentní pracovní postup: Hodnocení shody životopisu a práce

## Kompletní výuková cesta

Tato dokumentace vás provede vytvářením, testováním a nasazováním **víceagentního pracovního postupu**, který hodnotí shodu životopisu s pracovním místem pomocí čtyř specializovaných agentů orchestrujících prostřednictvím **WorkflowBuilder**.

> **Předpoklad:** Dokončete [Laboratoř 01 - Jednoagentní](../../lab01-single-agent/README.md) před zahájením Laboratoře 02.

---

## Moduly

| # | Modul | Co provedete |
|---|--------|--------------|
| 0 | [Předpoklady](00-prerequisites.md) | Ověření dokončení Laboratoře 01, pochopení konceptů víceagentního systému |
| 1 | [Pochopení víceagentní architektury](01-understand-multi-agent.md) | Naučíte se WorkflowBuilder, role agentů, orchestrace grafu |
| 2 | [Základ víceagentního projektu](02-scaffold-multi-agent.md) | Použijte rozšíření Foundry pro vytvoření rámce víceagentního pracovního postupu |
| 3 | [Konfigurace agentů a prostředí](03-configure-agents.md) | Napište instrukce pro 4 agenty, nakonfigurujte nástroj MCP, nastavte proměnné prostředí |
| 4 | [Orchestrace vzorů](04-orchestration-patterns.md) | Prozkoumejte paralelní rozložení, sekvenční agregaci a alternativní vzory |
| 5 | [Testování lokálně](05-test-locally.md) | Ladění pomocí F5 s Agent Inspector, spuštění testů na zkoušku s životopisem + popisem práce |
| 6 | [Nasazení do Foundry](06-deploy-to-foundry.md) | Vytvoření kontejneru, push do ACR, registrace hostovaného agenta |
| 7 | [Ověření v playgroundu](07-verify-in-playground.md) | Testování nasazeného agenta ve VS Code a Foundry Portal playgroundech |
| 8 | [Řešení potíží](08-troubleshooting.md) | Řešení běžných problémů víceagentních systémů (chyby MCP, ořezaný výstup, verze balíčků) |

---

## Odhadovaný čas

| Úroveň zkušeností | Čas |
|------------------|-----|
| Nedávno dokončeno Laboratoř 01 | 45-60 minut |
| Nějaká zkušenost se Azure AI | 60-90 minut |
| Poprvé s víceagentními systémy | 90-120 minut |

---

## Architektura na první pohled

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

**Zpět na:** [Laboratoř 02 README](../README.md) · [Úvodní stránka workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). I když se snažíme o přesnost, mějte prosím na paměti, že automatické překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoliv nedorozumění nebo špatné výklady vyplývající z použití tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->