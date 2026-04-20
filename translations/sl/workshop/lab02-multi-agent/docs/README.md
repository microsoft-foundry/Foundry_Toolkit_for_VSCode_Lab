# Lab 02 - Večagentni potek dela: Evalvator ujemanja življenjepisa s službo

## Celotna učna pot

Ta dokumentacija vas vodi skozi izdelavo, testiranje in uvajanje **večagentnega poteka dela**, ki ocenjuje ujemanje življenjepisa s službo z uporabo štirih specializiranih agentov, orkestriranih preko **WorkflowBuilderja**.

> **Predpogoj:** Pred začetkom laboratorija 02 dokončajte [Lab 01 - Enojni agent](../../lab01-single-agent/README.md).

---

## Moduli

| # | Modul | Kaj boste naredili |
|---|--------|--------------------|
| 0 | [Predpogoji](00-prerequisites.md) | Preverite dokončanje Lab 01, razumite koncepte večagentnosti |
| 1 | [Razumevanje večagentne arhitekture](01-understand-multi-agent.md) | Spoznajte WorkflowBuilder, vloge agentov, orkestracijski graf |
| 2 | [Postavitev večagentnega projekta](02-scaffold-multi-agent.md) | Uporabite razširitev Foundry za postavitev večagentnega poteka dela |
| 3 | [Konfiguracija agentov in okolja](03-configure-agents.md) | Napišite navodila za 4 agente, konfigurirajte MCP orodje, nastavite okoljske spremenljivke |
| 4 | [Orkestracijski vzorci](04-orchestration-patterns.md) | Raziščite vzorce vzporednega razvejanja, zaporednega združevanja in alternativne vzorce |
| 5 | [Lokalno testiranje](05-test-locally.md) | Odpravljanje napak s F5 in Agent Inspectorjem, poganjanje osnovnih testov z življenjepisom in opisom dela |
| 6 | [Uvajanje v Foundry](06-deploy-to-foundry.md) | Izgradnja kontejnerja, potisk v ACR, registracija gostujočega agenta |
| 7 | [Preverjanje v Playgroundu](07-verify-in-playground.md) | Testiranje uvedenega agenta v VS Code in Foundry Portal playgroundih |
| 8 | [Reševanje težav](08-troubleshooting.md) | Popravljanje pogostih težav večagentnega sistema (MCP napake, skrajšana izhodna vsebina, različice paketov) |

---

## Ocenjeni čas

| Raven izkušenj | Čas |
|-----------------|------|
| Nedavno dokončan Lab 01 | 45–60 minut |
| Nekaj izkušenj z Azure AI | 60–90 minut |
| Prvič z večagentnim sistemom | 90–120 minut |

---

## Arhitektura na kratko

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

**Nazaj na:** [Lab 02 README](../README.md) · [Domača stran delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da samodejni prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovi izvorni jezikovni različici velja za avtoritativni vir. Za ključne informacije priporočamo strokovni človeški prevod. Ne odgovarjamo za kakršne koli nesporazume ali napačne razlage, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->