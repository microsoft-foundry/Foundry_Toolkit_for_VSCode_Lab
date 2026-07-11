# Moduuli 1 - Ymmärrä arkkitehtuuri

⏱️ ~5 min

Ennen koodin kirjoittamista tässä on nopea yleiskatsaus siitä, mitä rakennat ja miten se toimii.

---

## Mitä rakennat

Liität **ansioluettelon** ja **työpaikkailmoituksen**. Työnkulku palauttaa:

- Soveltuvuuspisteet (0–100 eriteltynä)
- Lista taito- ja sertifikaattivajeista
- Henkilökohtainen oppimispolku Microsoft Learn -linkkeineen jokaiselle vajeelle

---

## Neljä agenttia

Yksi agentti, joka yrittää jäsentää, pisteyttää ja suunnitella kaiken kerralla, kiirehtii helposti ja tuottaa pinnallisen lopputuloksen. Työn jakaminen neljälle erikoistuneelle agentille antaa paremmat tulokset:

| Agentti | Mitä se tekee |
|---------|--------------|
| **ResumeParser** | Jäsentää ansioluettelon; kopioi työpaikkailmoituksen sanasta sanaan `[JOB DESCRIPTION PASS-THROUGH]` -kohteeseen seuraavia agentteja varten |
| **JobDescriptionAgent** | Erottaa työpaikkailmoituksen vaatimukset pass-through-kohteesta; välittää `[PARSED RESUME]` eteenpäin nimettynä `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | Vertaa molempia merkattuja osia; tuottaa soveltuvuuspistemäärän (0–100) ja vajelistan |
| **GapAnalyzer** | Laatii oppimispolun; etsii Microsoft Learn -materiaaleja jokaiselle vajeelle |

---

## Orkestrointikaavio

Työnkulku on **peräkkäinen putkisto** – kukin agentti välittää tuloksensa seuraavalle:

```mermaid
flowchart LR
    A["Käyttäjän syöte"] --> B["Ansioluettelon jäsentäjä"]
    B -- "jäsennetty ansioluettelo + työpaikkakuvan välitys" --> C["Työpaikkakuvausagentti"]
    C -- "työpaikkavaatimukset + ansioluettelon välitys" --> D["Vastaavuusagentti"]
    D -- "soveltuvuusraportti + aukot" --> E["Aukkoanalyysi + MCP"]
    E --> F["Lopullinen tulos"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** vastaanottaa käyttäjän syötteen, jäsentää ansioluettelon ja kopioi työpaikkailmoituksen `[JOB DESCRIPTION PASS-THROUGH]`-kenttään.
2. **JD Agent** poimii rakenteelliset vaatimukset ja välittää `[PARSED RESUME PASS-THROUGH]` eteenpäin.
3. **MatchingAgent** vertaa molempia osioita ja tuottaa soveltuvuuspistemäärän ja vajelistan.
4. **GapAnalyzer** laatii oppimispolun ja käyttää Microsoft Learn MCP -työkalua jokaiselle vajeelle.

---

## Miten tämä liittyy koodiin

`main.py`-tiedostossa kuvaat tämän kaavion `WorkflowBuilder`-luokan avulla:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # ensimmäinen agentti, joka vastaanottaa käyttäjän syötteen
        output_executors=[gap_executor],      # viimeinen agentti - sen ulostulo on vastaus
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JD Agentti
    .add_edge(jd_executor, matching_executor)     # JD Agentti → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

Kukin `Agent` kääritään `AgentExecutor`-instanssiin. `add_edge()`-kutsut määrittävät tiukasti peräkkäisen putkiston – kukin agentti saa vain suoraan edeltäjänsä tuloksen.

> `context_mode="last_agent"` tarkoittaa, että kukin suoritin näkee vain suoraan edeltäjänsä tuloksen. ResumeParser ja JD Agent välittävät tiedot eteenpäin nimetyissä osioissa, joten kukin downstream-agentti saa juuri tarvitsemansa tiedot.

---

## MCP-työkalu

GapAnalyzerilla on yksi työkalu: `search_microsoft_learn_for_plan`. Se yhdistää osoitteeseen `https://learn.microsoft.com/api/mcp` ja palauttaa oikeat Microsoft Learn -linkit jokaiselle taitovajeelle.

Kun työkalu suoritetaan, näet nämä lokit – kaikki odotettuja:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

Huolehdi vain, jos `POST`-kutsu palauttaa virheen.

---

**Edellinen:** [00 - Ennen aloittamista](00-prerequisites.md) · **Seuraava:** [02 - Projektin runko →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->