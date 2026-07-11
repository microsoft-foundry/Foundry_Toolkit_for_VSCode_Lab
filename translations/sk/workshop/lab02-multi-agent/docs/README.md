# Lab 02 - Viacagentný pracovný postup: Hodnotiaci nástroj zhody životopisu a pracovnej pozície

## Celá vzdelávacia cesta

Táto dokumentácia vás prevedie procesom vytvorenia, testovania a nasadenia **viacagentného pracovného postupu**, ktorý hodnotí zhodu životopisu s pracovnou pozíciou pomocou štyroch špecializovaných agentov koordinovaných cez **WorkflowBuilder**.

> **Predpoklad:** Dokončite [Lab 01 - Jednoagentný](../../lab01-single-agent/README.md) pred začatím Lab 02.

---

## Moduly

| # | Modul | Čo budete robiť |
|---|--------|---------------|
| 0 | [Úvod](00-prerequisites.md) | Čo vybudujete, overenie Lab 01, porovnanie Lab 02 a Lab 01 |
| 1 | [Pochopenie viacagentnej architektúry](01-understand-multi-agent.md) | Naučte sa WorkflowBuilder, úlohy agentov, orkestračný graf |
| 2 | [Základ viacagentného projektu](02-scaffold-multi-agent.md) | Použite sprievodcu rozšírenia Foundry na vytvorenie základného projektu |
| 3 | [Konfigurácia agentov a prostredia](03-configure-agents.md) | Napíšte inštrukcie pre 4 agentov, nastavte nástroj MCP, nastavte premenné prostredia |
| 4 | [Orkestračné vzory](04-orchestration-patterns.md) | Sekvenčný reťazec, prenos obsahu a OR-semantika WorkflowBuilder |
| 5 | [Testovanie lokálne](05-test-locally.md) | Ladenie pomocou F5 s Agent Inspector, spustenie základných testov s životopisom + JD |
| 6 | [Nasadenie do Foundry](06-deploy-to-foundry.md) | Vytvorenie kontajnera, push do ACR, registrácia hostovaného agenta |
| 7 | [Overenie v Playground](07-verify-in-playground.md) | Testovanie nasadeného agenta vo VS Code a Foundry portáli |
| 8 | [Riešenie problémov](08-troubleshooting.md) | Riešenie bežných problémov viacagentného systému (chyby MCP, prerušený výstup, verzie balíkov) |
| 9 | [Zhrnutie a ďalšie kroky](09-summary.md) | Čo ste vybudovali, kľúčové naučené koncepty, upratovanie a kam ďalej |

---

**Späť na:** [Lab 02 README](../README.md) · [Domovská stránka workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->