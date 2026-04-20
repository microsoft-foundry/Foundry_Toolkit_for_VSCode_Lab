# Lab 02 - Moniagenttinen työnkulku: CV → Työhön sopivuuden arvioija

## Koko oppimispolku

Tämä dokumentaatio opastaa sinut rakentamaan, testaamaan ja käyttämään **moniagenttista työnkulkua**, joka arvioi CV:n ja työpaikan sopivuutta neljän erikoistuneen agentin avulla, joita ohjataan **WorkflowBuilderilla**.

> **Edellytys:** Suorita [Lab 01 - Yksi agentti](../../lab01-single-agent/README.md) ennen Lab 02:n aloittamista.

---

## Modulien sisältö

| # | Moduli | Mitä teet |
|---|--------|-----------|
| 0 | [Edellytykset](00-prerequisites.md) | Varmista Lab 01 valmistuminen, ymmärrä moniagenttikonseptit |
| 1 | [Moniagenttinen arkkitehtuuri](01-understand-multi-agent.md) | Opiskele WorkflowBuilder, agenttien roolit, orkestrointikaavio |
| 2 | [Moniagenttisen projektin luonnin pohja](02-scaffold-multi-agent.md) | Käytä Foundry-laajennusta moniagenttisen työnkulun pohjana |
| 3 | [Agenttien & ympäristön konfigurointi](03-configure-agents.md) | Kirjoita ohjeet 4 agentille, määritä MCP-työkalu, aseta ympäristömuuttujat |
| 4 | [Orkestrointimallit](04-orchestration-patterns.md) | Tutki rinnakkaista haarautumista, peräkkäistä yhdistämistä ja vaihtoehtoisia malleja |
| 5 | [Testaa paikallisesti](05-test-locally.md) | Käynnistä F5-debugger Agent Inspectorilla, suorita pikatestit CV:llä + tehtävänkuvauksella |
| 6 | [Ota käyttöön Foundryssa](06-deploy-to-foundry.md) | Rakenna kontti, työnnä ACR:ään, rekisteröi isännöity agentti |
| 7 | [Varmista Playgroundissa](07-verify-in-playground.md) | Testaa otettua agenttia VS Code ja Foundry Portalin playgroundeissa |
| 8 | [Vianmääritys](08-troubleshooting.md) | Korjaa yleiset moniagenttiongelmat (MCP-virheet, lyhennetty tuloste, pakettiversiot) |

---

## Arvioitu aika

| Kokemustaso | Aika |
|-------------|------|
| Lab 01 hiljattain suoritettu | 45–60 minuuttia |
| Jonkin verran Azure AI -kokemusta | 60–90 minuuttia |
| Ensikertaa moniagentin kanssa | 90–120 minuuttia |

---

## Arkkitehtuuri yleiskatsauksena

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

**Takaisin:** [Lab 02 README](../README.md) · [Työpajan kotisivu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Pyrimme tarkkuuteen, mutta ole hyvä ja huomioi, että automaattikäännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulee pitää auktoritatiivisena lähteenä. Tärkeiden tietojen osalta suositellaan ammatillista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä johtuvista väärinkäsityksistä tai virhetulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->