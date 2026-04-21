# Labor 02 - Mitmeagendi töölahendus: CV → Töö sobivuse hindaja

## Täielik õpitee

See dokumentatsioon juhendab sind mitmeagendi töölahenduse loomisel, testimisel ja juurutamisel, mis hindab CV ja töö sobivust, kasutades nelja spetsialiseerunud agenti, keda juhib **WorkflowBuilder**.

> **Eeltingimus:** Enne labori 02 alustamist lõpeta [Labor 01 - Üksikagent](../../lab01-single-agent/README.md).

---

## Moodulid

| # | Moodul | Mida sa teed |
|---|--------|--------------|
| 0 | [Eeltingimused](00-prerequisites.md) | Kontrolli labori 01 lõpetamist, mõista mitmeagendi mõisteid |
| 1 | [Mõista mitmeagendi arhitektuuri](01-understand-multi-agent.md) | Õpi WorkflowBuilderit, agentide rolle, orkestreerimisgraafikut |
| 2 | [Mitmeagendi projekti alus](02-scaffold-multi-agent.md) | Kasuta Foundry laiendust mitmeagendi töölahenduse alustamiseks |
| 3 | [Agendid ja keskkond valmis seadistada](03-configure-agents.md) | Kirjuta juhiseid 4 agendile, seadista MCP tööriist, määra keskkonnamuutujad |
| 4 | [Orkestreerimismustrid](04-orchestration-patterns.md) | Uuri paralleelset hajutatust, järjestikust koondamist ja alternatiivseid mustreid |
| 5 | [Testi kohapeal](05-test-locally.md) | F5 silumine Agent Inspectori abil, tee suitsutestid CV ja töökuulutusega |
| 6 | [Juuruta Foundrysse](06-deploy-to-foundry.md) | Koosta konteiner, lükka ACR-i, registreeri majutatud agent |
| 7 | [Kontrolli Playgroundis](07-verify-in-playground.md) | Testi juurutatud agenti VS Code ja Foundry portaali mänguväljakutel |
| 8 | [Veaotsing](08-troubleshooting.md) | Paranda tavalisi mitmeagendi probleeme (MCP vead, katkine väljund, paketiversioonid) |

---

## Hinnanguline aeg

| Kogemustase | Aeg |
|-------------|-----|
| Labor 01 hiljutine lõpetamine | 45-60 minutit |
| Mõningane Azure AI kogemus | 60-90 minutit |
| Esmakordne mitmeagendiga | 90-120 minutit |

---

## Arhitektuur lühidalt

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

**Tagasi:** [Labor 02 Lugege mind](../README.md) · [Töötoa avaleht](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastutusest vabastamine**:  
See dokument on tõlgitud tehisintellekti tõlketeenuse [Co-op Translator](https://github.com/Azure/co-op-translator) abil. Kuigi püüdleme täpsuse poole, tuleb arvestada, et automaatsed tõlked võivad sisaldada vigu või ebatäpsusi. Originaaldokument selles emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlke kasutamisest tingitud arusaamatuste või valesti mõistmiste eest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->