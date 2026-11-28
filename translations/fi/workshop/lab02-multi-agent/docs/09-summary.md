# Moduuli 9 - Yhteenveto & Seuraavat vaiheet

⏱️ ~5 min

**Onnittelut!** Olet rakentanut, testannut ja (polulla A) ottanut käyttöön moniedustajan työnkulun käyttäen Microsoft Foundrya ja Foundry Toolkitia VS Codeen.

---

## Mitä rakensit

**Ansioluettelo → Työhön soveltuvuuden arvioija** - moniedustajan isännöimä työnkulku, joka:
- Vastaanottaa ansioluettelon + työkuvauksen HTTP:n kautta (`POST /responses`)
- Suorittaa neljä erikoistettua agenttia peräkkäisessä putkessa - kukin agentti välittää seuraajalleen tarvitseman datan
- Palauttaa soveltuvuusarvon (0–100 erittelyineen), taidot ja sertifikaattivajeiden listan sekä henkilökohtaisen oppimispolun todellisilla Microsoft Learn -linkeillä jokaista vajetta varten
- Kutsuu Microsoft Learn MCP -palvelinta (`https://learn.microsoft.com/api/mcp`) noutaakseen viralliset oppimateriaalit jokaiseen tunnistettuun taitovajeeseen
- Toimii yksittäisenä konttina isännöitynä agenttina Microsoft Foundryn Agent Service -palvelussa

---

## Avainkäsitteet, joita opit

| Käsite | Mitä harjoittelit |
|---------|-------------------|
| **Moniedustajan orkestrointi** | `WorkflowBuilder` peräkkäinen putki käyttäen `add_edge()` |
| **Agenttien erikoistuminen** | Neljä fokusoitua agenttia on tehokkaampi kuin yksi yleiskäyttöinen agentti |
| **Sisällön reititin -malli** | ResumeParser toimii myös reitittimenä - se säilyttää työkuvauksen tekstin `[JOB DESCRIPTION PASS-THROUGH]`-osiossa jotta seuraavat agentit voivat käyttää sitä (tarvitaan koska `context_mode="last_agent"` tarkoittaa, että vain `start_executor` näkee alkuperäisen käyttäjäviestin) |
| **Sisällön välitysmalli** | JD Agent välittää `[PARSED RESUME PASS-THROUGH]` eteenpäin niin, että MatchingAgent saa molemmat profiilit; välttää OR-semantikan kaksoislaukaisun, jonka fan-in-kaaviot aiheuttavat |
| **MCP-työkalun integrointi** | `@tool` + `streamable_http_client` kutsumassa ulkoista MCP-palvelinta |
| **Isännöidyn agentin elinkaari** | Luominen → Konfigurointi → Paikallinen testaus → Julkaisu → Varmistus pilvessä |
| **`context_mode="last_agent"`** | Jokainen suorittaja näkee vain suoraan edeltäjänsä tuloksen |
| **Foundry Toolkit -työnkulku** | Luonti-apuri, Agenttien tarkastaja, Työnkulun visualisointi, yhden klikkauksen julkaisu |

---

## Mitä sait valmiiksi

<details open>
<summary><strong>🅰️ Polku A - Foundry-tilaus</strong></summary>

- [x] Varmistettu Lab 01:n asennus: projekti, malli ja RBAC vielä toiminnassa
- [x] Luotu moniedustajaprojekti Workflows-mallipohjalla
- [x] Kirjoitettu neljä agentin ohjeistussarjaa (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integroitu Microsoft Learn MCP -työkalu `streamable_http_client` kanssa
- [x] Kytketty työnkulun kaavio `WorkflowBuilder`-menetelmällä (peräkkäinen putki sisällön välityksellä)
- [x] Testattu paikallisesti kahdella savutestillä (Agent Inspector) - soveltuvuusarvo, vaje-kortit ja MCP-URL-osoitteet
- [x] Julkaistu Foundry Agent Serviceen (konttina, hallinnoitu identiteetti)
- [x] Tarkistettu pilvipelikentällä - rakenteellinen yhdenmukaisuus paikallisten tulosten kanssa

</details>

<details open>
<summary><strong>🅱️ Polku B - Foundry Local</strong></summary>

- [x] Varmistettu Lab 01:n asennus: Foundry Local käynnissä paikallisen mallin kanssa
- [x] Luotu moniedustajaprojekti Workflows-mallipohjalla
- [x] Kirjoitettu neljä agentin ohjeistussarjaa ja kytketty työnkulun kaavio
- [x] Integroitu Microsoft Learn MCP -työkalu
- [x] Testattu paikallisesti kahdella savutestillä
- [x] Vahvistettu moniedustajan käyttäytyminen ilman pilviresursseja

</details>

---

## Seuraavat vaiheet

### Jatka oppimista

| Resurssi | Kuvaus |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API-dokumentaatio `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Yhdistä agentit muihin MCP-palvelimiin (Bing, GitHub, mukautettuja) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Maadoita agentit dokumenteilla, vektorivarastoilla tai Bing-haulla |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mittaa agenttien laatua automaattisilla arvioijilla mittakaavassa |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Koko alustan dokumentaatio |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Laajennuksen julkaisumuistiinpanot ja muutokset |

### Ideoita tämän työnkulun laajentamiseen

- **Lisää 5. agentti** - Haastattelukouluttaja, joka tuottaa mahdollisia haastattelukysymyksiä vajaraportin pohjalta
- **Lisää Bing-maadoitustyökalu** - Anna JD Agentin etsiä samankaltaisia työpaikkailmoituksia vaatimusten rikastamiseksi
- **Yhdistä ansioluetteloraporttikantaan** - Hae kandidaattiprofiileja tietokannasta mukautetun `@tool` avulla
- **Kokeile eri malleja** - Vertaa `gpt-4.1` vs. `gpt-4.1-mini` tuotannon laatua ja viivettä
- **Arvioi Foundryn avulla** - Käytä Evaluations-ominaisuutta soveltuvuusraporttien pisteyttämiseen kultadatan perusteella

### Path B -käyttäjille: Päivitys pilvijakeluun

Kun olet valmis julkaisemaan pilveen:
1. Hanki Azure-tilaus ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Suorita [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (luo projekti, julkaise malli, määrää RBAC)
3. Päivitä `.env` Foundry-projektin päätepisteellä ja mallin julkaisun nimellä
4. Jatka kohdasta [Module 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Resurssien siivous (valinnainen)

Jos haluat poistaa tämän workshopin aikana luodut Azure-resurssit:

### Vaihtoehto 1: Poista resurssiryhmä (poistaa kaiken)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Vaihtoehto 2: Poista vain isännöity agentti

1. Avaa [ai.azure.com](https://ai.azure.com) → projekti → **Build** → **Agents**.
2. Etsi **PersonalCareerCopilot** → napsauta **Delete**.

### Vaihtoehto 3: Poista mallin julkaisu

1. Foundryn sivupalkissa laajenna projektisi → **Models**.
2. Napsauta mallin julkaisua hiiren oikealla → **Delete**.

> **Kustannusmuistutus:** Isännöidyt agentit maksavat vain silloin kun ne ovat käynnissä. Jos pysäytät tai poistat agentin, ei tule jatkuvia maksuja. Mallin julkaisu saattaa aiheuttaa pienen varatun kapasiteetin maksun - poista se jos olet valmis.

---

**Edellinen:** [08 - Vianetsintä](08-troubleshooting.md) · **Koti:** [Lab 02 README](../README.md) · [Workshopin kotisivu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->