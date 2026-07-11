# Moduuli 7 - Yhteenveto ja seuraavat askeleet

⏱️ ~5 min

**Onnittelut!** Olet rakentanut, testannut ja (jos polku A) ottanut käyttöön isännöidyn tekoälyagentin Microsoft Foundryn ja Foundry Toolkitin VS Coden kanssa.

---

## Mitä rakensit

**"Selitä kuin olisin johtaja"** -agentin, joka:
- Vastaanottaa teknisiä häiriöraportteja tai operatiivisia päivityksiä HTTP:n kautta (`POST /responses`)
- Kääntää ne selkokielisiksi johtajayhteenvetoiksi
- Noudattaa jäsenneltyä tulostemuotoa (Mitä tapahtui / Liiketoiminnan vaikutus / Seuraava askel)
- Kieltäytyy aiheen ulkopuolisista pyynnöistä ja kehotteen injektiokokeiluista
- Toimii säilöitettynä isännöitynä agenttina Microsoft Foundry Agent Servicessä

---

## Keskeiset opitut käsitteet

| Käsite | Mitä harjoittelit |
|---------|-------------------|
| **Agenttikehyksen arkkitehtuuri** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` putki |
| **Isännöidyn agentin elinkaari** | Rakentele → Määritä → Testaa paikallisesti → Ota käyttöön → Vahvista pilvessä |
| **Järjestelmäkehotteen suunnittelu** | Rooli, yleisö, tulostemuoto, säännöt, turvallisuusrajoitteet ja esimerkit |
| **Paikallisen ja isännöidyn erot** | Identiteetti (henkilökohtainen tunnus vs. hallittu identiteetti), päätepiste, verkkopolku |
| **Turvallisuusrajat** | Kehotteen injektiovastaus, roolin noudattaminen, reunatapauksien sujuva käsittely |
| **Foundry Toolkit -työnkulku** | Projektin luonti, mallin käyttöönotto, agentin rakentaminen, Agent Inspector, yhden klikkauksen käyttöönotto |

---

## Mitä suorutit

### Polku A (Foundry-tilaus)

- [x] Perustit Foundry Toolkitin ja loit Foundry-projektin, jossa on otettu käyttöön malli
- [x] Rakensit isännöidyn agentin automaattisesti generoituine projektirakenteineen
- [x] Kirjoitit jäsennellyt agentin ohjeet turvallisuussääntöineen
- [x] Testasit paikallisesti kolmella toiminnallisella skenaariolla (Agent Inspector)
- [x] Otit käyttöön Foundry Agent Servicessä (säilöitettynä)
- [x] Vahvistit pilvipelikentässä neljällä reunatapaus/turvallisuustestillä

### Polku B (Foundry Local)

- [x] Perustit Foundry Toolkitin paikallisen mallipäätepisteen kanssa
- [x] Rakensit isännöidyn agenttiprojektin
- [x] Kirjoitit jäsennellyt agentin ohjeet turvallisuussääntöineen
- [x] Testasit paikallisesti kolmella toiminnallisella skenaariolla
- [x] Varmistit agentin toiminnan ilman pilviresursseja

---

## Seuraavat askeleet

### Jatka oppimista

| Resurssi | Kuvaus |
|----------|-------------|
| **[Lab 02 - Moni-agentin orkestrointi](../../lab02-multi-agent/docs/README.md)** | Rakenna 4-agentin työnkulku (Ansioluettelo → Työpaikan soveltuvuusarvioija) orkestrointimalleineen |
| **[Lisää työkaluja agentillesi](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Yhdistä API:t, tietokannat tai mukautetut funktiot Työkalukatalogin kautta |
| **[Lisää tietämystä (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Perusta agenttisi dokumentteihin, vektorivarastoihin tai Bing-haun avulla |
| **[Microsoft Foundryn dokumentaatio](https://learn.microsoft.com/azure/foundry/)** | Täydellinen alustaviite |
| **[Agent Framework SDK -viite](https://learn.microsoft.com/agent-framework/)** | `agent-framework`-paketin API-dokumentaatio |
| **[Foundry Toolkit - Uutta](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Laajennuksen julkaisumuistiinpanot ja muutokset |

### Ideoita agenttisi laajentamiseen

- **Lisää päivämäärätyökalu** - Anna agentin sisällyttää "tämän päivän tilanne" yhteenvetoihin
- **Yhdistä häiriötietokantaan** - Hae todellisia häiriötietoja työkalutoiminnon avulla
- **Lisää Bing-pohjainen haku** - Anna agentin hakea viimeaikaisia uutisia lisäkontekstiksi
- **Kokeile eri malleja** - Vertaa `gpt-4.1`- ja `gpt-4.1-mini`-mallien tuloslaatua
- **Arvioi Foundryn avulla** - Käytä Arviointitoimintoa mitataksesi agentin laatua laajassa mittakaavassa

### Polun B käyttäjille: Päivitys pilvikäyttöönottoon

Kun olet valmis ottamaan käyttöön pilvipalvelussa:
1. Hanki Azure-tilaus ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Suorita [Moduuli 01, Asennus](01-setup.md#step-2-set-up-based-on-your-access) (luo projekti, ota malli käyttöön, määritä RBAC)
3. Päivitä `.env`-tiedoston Foundry-projektin päätepisteellä ja mallin käyttöönoton nimellä
4. Jatka kohdasta [Moduuli 05 - Käyttöönotto Foundryyn](05-deploy-to-foundry.md)

---

## Resurssien siivous (valinnainen)

Jos haluat poistaa tämän työpajan aikana luodut Azure-resurssit:

### Vaihtoehto 1: Poista resurssiryhmä (poistaa kaiken)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Vaihtoehto 2: Poista vain isännöity agentti

1. Avaa [ai.azure.com](https://ai.azure.com) → projektisi → **Rakenna** → **Agentit**.
2. Napsauta agenttiasi → napsauta **Poista**.

### Vaihtoehto 3: Poista mallin käyttöönotto

1. Laajenna Foundryn sivupalkissa projektisi → **Mallit**.
2. Napsauta mallin käyttöönottoa hiiren oikealla → **Poista**.

> **Kustannushuomautus:** Isännöidyt agentit aiheuttavat kustannuksia vain toimiessaan. Jos pysäytät tai poistat agentin, juoksevia kuluja ei synny. Mallin käyttöönotto saattaa aiheuttaa pienen maksun varatusta kapasiteetista – poista se, jos et enää tarvitse.

---

**Edellinen:** [06 - Vahvista pelialustalla](06-verify-in-playground.md) · **Seuraava:** [08 - Vianmääritys (Viite) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->