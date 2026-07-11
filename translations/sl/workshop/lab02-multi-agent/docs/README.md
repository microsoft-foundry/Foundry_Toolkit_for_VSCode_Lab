# Laboratorij 02 - Večagentni delovni tok: Ocena skladnosti življenjepisa z delovnim mestom

## Celotna učna pot

Ta dokumentacija vas vodi skozi izgradnjo, testiranje in uvajanje **večagentnega delovnega toka**, ki ocenjuje skladnost življenjepisa z delovnim mestom z uporabo štirih specializiranih agentov, ki jih orkestrira **WorkflowBuilder**.

> **Predpogoj:** Zaključite [Laboratorij 01 - Enotni agent](../../lab01-single-agent/README.md) pred začetkom laboratorija 02.

---

## Moduli

| # | Modul | Kaj boste naredili |
|---|--------|--------------------|
| 0 | [Uvod](00-prerequisites.md) | Kaj boste zgradili, preverjanje laboratorija 01, primerjava laboratorij 02 in laboratorij 01 |
| 1 | [Razumevanje večagentne arhitekture](01-understand-multi-agent.md) | Spoznajte WorkflowBuilder, vloge agentov, orkestracijski graf |
| 2 | [Postavitev večagentnega projekta](02-scaffold-multi-agent.md) | Uporabite čarovnika razširitve Foundry za postavitev osnovnega projekta |
| 3 | [Konfiguracija agentov in okolja](03-configure-agents.md) | Napišite navodila za 4 agente, konfigurirajte orodje MCP, nastavite okoljske spremenljivke |
| 4 | [Vzorec orkestracije](04-orchestration-patterns.md) | Zaporedna veriga, prenos vsebine in OR-semantika WorkflowBuilderja |
| 5 | [Lokalno testiranje](05-test-locally.md) | F5 razhroščevanje z Agent Inspectorjem, izvajanje hitrih testov z življenjepisom + opisom delovnega mesta |
| 6 | [Uvajanje v Foundry](06-deploy-to-foundry.md) | Izgradnja kontejnerja, pošiljanje v ACR, registracija gostujočega agenta |
| 7 | [Preverjanje v Playgroundu](07-verify-in-playground.md) | Testiranje nameščenega agenta v VS Code in Foundry Portal playgroundih |
| 8 | [Reševanje težav](08-troubleshooting.md) | Popravki pogostih težav z več agenti (napake MCP, skrajšan izhod, različice paketov) |
| 9 | [Povzetek in nadaljnji koraki](09-summary.md) | Kaj ste zgradili, ključni nauki, čiščenje in kam naprej |

---

**Nazaj na:** [Laboratorij 02 README](../README.md) · [Domača stran delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->