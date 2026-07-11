# Labor 02 - Mitme-agendi töövoog: CV → töö sobivuse hindaja

## Täispikk õppeteekond

See dokumentatsioon juhendab sind samm-sammult koostama, testima ja juurutama **mitme-agendi töövoogu**, mis hindab CV ja töö sobivust, kasutades nelja spetsialiseerunud agenti, keda juhib **WorkflowBuilder**.

> **Nõue:** Enne labori 02 alustamist lõpeta [Labor 01 - Üks agent](../../lab01-single-agent/README.md).

---

## Moodulid

| # | Moodul | Mida sa teed |
|---|--------|-------------|
| 0 | [Sissejuhatus](00-prerequisites.md) | Mida sa ehitad, labor 01 kontroll, labor 02 vs labor 01 võrdlus |
| 1 | [Mõista mitme-agendi arhitektuuri](01-understand-multi-agent.md) | Õpi WorkflowBuilderi, agentide rollide ja orkestratsiooni graafi kohta |
| 2 | [Alusta mitme-agendi projekti](02-scaffold-multi-agent.md) | Kasuta Foundry laienduse viisardit baasprojekti alustamiseks |
| 3 | [Seadista agendid ja keskkond](03-configure-agents.md) | Kirjuta juhised 4 agendile, seadista MCP tööriist, määra keskkonnamuutujad |
| 4 | [Orkestratsiooni mustrid](04-orchestration-patterns.md) | Järjestikuneahel, sisutalitlus ja WorkflowBuilderi OR-semantika |
| 5 | [Testi kohapeal](05-test-locally.md) | F5 veadediagnostika Agent Inspectoriga, käivita suitsutestid koos CV ja töökuulutusega |
| 6 | [Juuruta Foundry’sse](06-deploy-to-foundry.md) | Ehita konteiner, lae ACR-i, registreeri majutatud agent |
| 7 | [Kontrolli mänguväljakul](07-verify-in-playground.md) | Testi juurutatud agenti VS Code ja Foundry portaalide mänguväljakutel |
| 8 | [Tõrkeotsing](08-troubleshooting.md) | Lahenda levinud mitme-agendi probleemid (MCP vead, katkised väljundid, paketiversioonid) |
| 9 | [Kokkuvõte ja järgmised sammud](09-summary.md) | Mida sa ehitasid, õppitud põhikontseptsioonid, koristamine ja kuhu edasi minna |

---

**Tagasi:** [Labor 02 README](../README.md) · [Töötoa avaleht](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->