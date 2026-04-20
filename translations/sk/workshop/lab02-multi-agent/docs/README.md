# Lab 02 - Viacagentový pracovný postup: Vyhodnotenie zhody životopisu s pracovnou pozíciou

## Kompletná vzdelávacia cesta

Táto dokumentácia vás prevedie vytváraním, testovaním a nasadzovaním **viacagentového pracovného postupu**, ktorý vyhodnocuje zhodu životopisu s pracovnou pozíciou pomocou štyroch špecializovaných agentov orchestrujúci cez **WorkflowBuilder**.

> **Predpoklad:** Dokončite [Lab 01 - Jednoagentový](../../lab01-single-agent/README.md) pred začatím Lab 02.

---

## Moduly

| # | Modul | Čo urobíte |
|---|--------|------------|
| 0 | [Predpoklady](00-prerequisites.md) | Overenie dokončenia Lab 01, porozumenie konceptom viacagentovej architektúry |
| 1 | [Pochopenie viacagentovej architektúry](01-understand-multi-agent.md) | Naučte sa WorkflowBuilder, roly agentov, orchestráciu pomocou grafu |
| 2 | [Základná štruktúra viacagentového projektu](02-scaffold-multi-agent.md) | Použite rozšírenie Foundry na vytvorenie základnej štruktúry viacagentového pracovného postupu |
| 3 | [Konfigurácia agentov a prostredia](03-configure-agents.md) | Napíšte inštrukcie pre 4 agentov, nastavte nástroj MCP, nastavte premenné prostredia |
| 4 | [Orchestačné vzory](04-orchestration-patterns.md) | Preskúmajte paralelné rozvetvenie, sekvenčné agregovanie a alternatívne vzory |
| 5 | [Testovanie lokálne](05-test-locally.md) | Ladiť pomocou Agent Inspector a F5, spustiť základné testy so životopisom + pracovným popisom |
| 6 | [Nasadenie do Foundry](06-deploy-to-foundry.md) | Vytvorte kontajner, odošlite do ACR, zaregistrujte hostovaného agenta |
| 7 | [Overenie v Playground](07-verify-in-playground.md) | Testovanie nasadeného agenta vo VS Code a Foundry Portal playgroundoch |
| 8 | [Riešenie problémov](08-troubleshooting.md) | Oprava bežných problémov s viacagentovým systémom (MCP chyby, skrátený výstup, verzie balíčkov) |

---

## Odhadovaný čas

| Úroveň skúseností | Čas |
|-------------------|-----|
| Nedávno dokončený Lab 01 | 45-60 minút |
| Niektoré skúsenosti s Azure AI | 60-90 minút |
| Prvýkrát s viacagentovým pracovným postupom | 90-120 minút |

---

## Architektúra v skratke

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

**Späť na:** [Lab 02 README](../README.md) · [Domovská stránka workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zrieknutie sa zodpovednosti**:  
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Aj keď usilovne dbáme na presnosť, berte prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Originálny dokument v jeho pôvodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za akékoľvek nedorozumenia alebo nesprávne výklady vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->