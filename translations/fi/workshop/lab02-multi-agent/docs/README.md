# Lab 02 - Moni-agenttinen työnkulku: CV → Työhön sopivuuden arvioija

## Kokonainen oppimispolku

Tämä dokumentaatio ohjaa sinut rakentamaan, testaamaan ja ottamaan käyttöön **moni-agenttisen työnkulun**, joka arvioi CV:n ja työpaikan sopivuutta neljän erikoistuneen agentin avulla, joita ohjataan **WorkflowBuilderilla**.

> **Esivaatimus:** Suorita ensin [Lab 01 - Yksittäinen agentti](../../lab01-single-agent/README.md) ennen Lab 02:n aloittamista.

---

## Modulaarit

| # | Moduuli | Mitä teet |
|---|--------|---------------|
| 0 | [Johdanto](00-prerequisites.md) | Mitä rakennat, Lab 01 -tarkistus, Lab 02 vs Lab 01 vertailu |
| 1 | [Ymmärrä moni-agenttinen arkkitehtuuri](01-understand-multi-agent.md) | Tutustu WorkflowBuilderiin, agenttien rooleihin, orkestrointikaavioon |
| 2 | [Luo moni-agenttiprojekti](02-scaffold-multi-agent.md) | Käytä Foundry-laajennuksen ohjatinta pohjaprojektin luomiseen |
| 3 | [Määritä agentit & ympäristö](03-configure-agents.md) | Kirjoita ohjeet 4 agentille, määritä MCP-työkalu, aseta ympäristömuuttujat |
| 4 | [Orkestrointimallit](04-orchestration-patterns.md) | Peräkkäinen ketju, sisällön välitys ja WorkflowBuilderin TAI-semanttiikka |
| 5 | [Testaa paikallisesti](05-test-locally.md) | F5-vikaetsintä Agent Inspectorin kanssa, suorita savutestit CV:llä + työpaikkailmoituksella |
| 6 | [Ota käyttöön Foundryssa](06-deploy-to-foundry.md) | Rakenna kontti, työnnä ACR:ään, rekisteröi isännöity agentti |
| 7 | [Vahvista Playgroundissa](07-verify-in-playground.md) | Testaa otettua agenttia VS Codessa ja Foundryn portaalin playgroundeissa |
| 8 | [Vianetsintä](08-troubleshooting.md) | Korjaa yleisiä moni-agenttisia ongelmia (MCP-virheet, katkennut tuloste, pakettiversiot) |
| 9 | [Yhteenveto & seuraavat askeleet](09-summary.md) | Mitä rakensit, opitut keskeiset käsitteet, siivous ja minne mennä seuraavaksi |

---

**Takaisin:** [Lab 02 README](../README.md) · [Työpajan etusivu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->