# Moduuli 9 - Yhteenveto ja seuraavat askeleet

⏱️ ~5 min

**Onnittelut!** Olet rakentanut, testannut ja (jos polku A) ottanut käyttöön moniedustajan työnkulun Microsoft Foundryn ja Foundry Toolkit for VS Coden avulla.

---

## Mitä rakensit

**Resume → Job Fit Evaluator** - moniedustajan isännöimä työnkulku, joka:
- Vastaanottaa ansioluettelon + työkuvauksen HTTP:n kautta (`POST /responses`)
- Suorittaa neljä erikoistunutta agenttia peräkkäisessä putkistossa - jokainen agentti välittää seuraajansa tarvitsemat tiedot
- Palauttaa sopivuuspisteen (0–100 erittelyineen), taito- ja sertifiointikuilulistan sekä henkilökohtaisen oppimispolun, jossa on todelliset Microsoft Learn -linkit jokaiseen kuiluun
- Kutsuu Microsoft Learn MCP -palvelinta (`https://learn.microsoft.com/api/mcp`) hakeakseen viralliset oppimateriaalit jokaiseen tunnistettuun taitokuiluun
- Suoritetaan yhtenä konttina isännöitynä agenttina Microsoft Foundry Agent Servicessä

---

## Keskeiset opitut käsitteet

| Käsite | Mitä harjoittelit |
|---------|-------------------|
| **Moniedustajan orkestrointi** | `WorkflowBuilder` peräkkäinen putkisto `add_edge()`-menetelmällä |
| **Agenttien erikoistuminen** | Neljä keskittynyttä agenttia päihittää yhden yleiskäyttöagentin |
| **Sisällönreititin-malli** | ResumeParser toimii myös reitittimenä - se säilyttää JD-tekstin `[JOB DESCRIPTION PASS-THROUGH]`-osiossa, jotta jälkimmäiset agentit pääsevät siihen käsiksi (tarvitaan, koska `context_mode="last_agent"` tarkoittaa, että vain `start_executor` näkee raakakäyttäjäviestin) |
| **Sisällönvälitysmalli** | JD Agent välittää `[PARSED RESUME PASS-THROUGH]` eteenpäin, jolloin MatchingAgent saa molemmat profiilit; välttää OR-semanttisen kaksoiskäynnistyksen, johon fan-in-kaaviot johtavat |
| **MCP-työkalun integrointi** | `@tool` + `streamable_http_client` kutsuu ulkoista MCP-palvelinta |
| **Isännöidyn agentin elinkaari** | Rakentaminen → Konfigurointi → Testaus paikallisesti → Julkaisu → Varmistus pilvessä |
| **`context_mode="last_agent"`** | Jokainen suorittaja näkee vain suoran edeltäjänsä tuloksen |
| **Foundry Toolkit -työnkulku** | Rakennetyökalu, Agenttien tarkastaja, Työnkulun visualisointityökalu, yhden klikkauksen julkaisutoiminto |

---

## Mitä sait valmiiksi

<details open>
<summary><strong>🅰️ Polku A - Foundry-tilaus</strong></summary>

- [x] Vahvistettu Lab 01 asennus: projekti, malli ja RBAC edelleen aktiivisia
- [x] Luotu moniedustajaprojekti Workflows-mallipohjalla
- [x] Kirjoitettu neljä agentin ohjesarjaa (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integroitu Microsoft Learn MCP -työkalu `streamable_http_client`-menetelmällä
- [x] Kytketty työnkulun kaavio `WorkflowBuilder`-luokalla (peräkkäinen putkisto sisällönvälityksellä)
- [x] Testattu paikallisesti kolmella savutestillä (Agenttien tarkastaja) - sopivuuspiste, kuilukortit ja MCP-URL:t
- [x] Julkaistu Foundry Agent Serviceen (konttina, hallittu identiteetti)
- [x] Vahvistettu pilvileikkikentässä - rakenteellinen yhdenmukaisuus paikallisten tulosten kanssa

</details>

<details open>
<summary><strong>🅱️ Polku B - Foundry Local</strong></summary>

- [x] Vahvistettu Lab 01 asennus: Foundry Local käynnissä paikallisen mallin kanssa
- [x] Luotu moniedustajaprojekti Workflows-mallipohjalla
- [x] Kirjoitettu neljä agentin ohjesarjaa ja yhdistetty työnkulun kaavio
- [x] Integroitu Microsoft Learn MCP -työkalu
- [x] Testattu paikallisesti kolmella savutestillä
- [x] Varmistettu moniedustajien toiminta ilman pilviresursseja

</details>

---

## Seuraavat askeleet

### Jatka oppimista

| Resurssi | Kuvaus |
|----------|-------------|
| **[Agent Framework SDK -viite](https://learn.microsoft.com/agent-framework/)** | API-dokumentaatio `agent-framework-foundry`lle, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP-työkaluluettelo](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Yhdistä agentit muihin MCP-palvelimiin (Bing, GitHub, oma) |
| **[Lisää tietämystä (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Tue agenteja dokumenteilla, vektorivarastoilla tai Bing-haulla |
| **[Foundry-arvioinnit](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mittaa agenttien laatua laajasti automatisoitujen arvioijien avulla |
| **[Microsoft Foundry dokumentaatio](https://learn.microsoft.com/azure/foundry/)** | Täydellinen alustan viite |
| **[Foundry Toolkit - Uutuudet](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Laajennuksen julkaisumuistiinpanot ja muutokset |

### Ideoita työnkulun laajentamiseksi

- **Lisää 5. agentti** - Haastattelukouluttaja, joka laatii todennäköisiä haastattelukysymyksiä kuilaraportin perusteella
- **Lisää Bing-perustustyökalu** - Anna JD Agentin hakea samankaltaisia työpaikkailmoituksia vaatimusten rikastamiseksi
- **Yhdistä ansioluettelotietokantaan** - Hae ehdokasprofiileja tietokannasta mukautetun `@tool`-liitännän avulla
- **Kokeile eri malleja** - Vertaa `gpt-4.1` ja `gpt-4.1-mini` laatua ja vasteaikaa
- **Arvioi Foundryn avulla** - Käytä Arvioinnit-toimintoa sopivuusarvioiden pisteyttämiseen kultaisen tietoaineiston perusteella

### Polku B:n käyttäjille: Päivitys pilvijulkaisuun

Kun olet valmis julkaisemaan pilvessä:
1. Hanki Azure-tilaus ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Suorita [Lab 01, Moduuli 01](../../lab01-single-agent/docs/01-setup.md) (luo projekti, julkaise malli, määritä RBAC)
3. Päivitä `.env` sisältämään Foundry-projektin päätepiste ja mallijulkaisu
4. Jatka osiosta [Moduuli 06 - Julkaise Foundryyn](06-deploy-to-foundry.md)

---

## Puhdista resurssit (valinnainen)

Jos haluat poistaa workshopin aikana luodut Azure-resurssit:

### Vaihtoehto 1: Poista resurssiryhmä (poistaa kaiken)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Vaihtoehto 2: Poista vain isännöity agentti

1. Avaa [ai.azure.com](https://ai.azure.com) → projektisi → **Build** → **Agents**.
2. Etsi **PersonalCareerCopilot** → klikkaa **Delete**.

### Vaihtoehto 3: Poista mallijulkaisu

1. Laajenna Foundry-sivupalkissa projektisi → **Models**.
2. Napsauta mallijulkaisua hiiren kakkospainikkeella → **Delete**.

> **Kustannusmuistutus:** Isännöidyt agentit aiheuttavat kustannuksia vain käynnissä ollessaan. Jos pysäytät tai poistat agentin, kuukausittaisia maksuja ei kerry. Mallijulkaisu saattaa aiheuttaa pienen kustannuksen varatusta kapasiteetista - poista se, kun et enää tarvitse.

---

**Edellinen:** [08 - Vianmääritys](08-troubleshooting.md) · **Koti:** [Lab 02 Lue minut](../README.md) · [Workshopin aloitussivu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->