# Moduuli 7 - Yhteenveto & Seuraavat askeleet

⏱️ ~5 min

**Onnittelut!** Olet rakentanut, testannut ja (jos polulla A) ottanut käyttöön isännöidyn tekoälyagentin käyttäen Microsoft Foundrya ja Foundry Toolkitia VS Codeen.

---

## Mitä rakensit

**"Selitä kuin olisin johtaja"** -agentin, joka:
- Vastaanottaa teknisiä häiriöraportteja tai operatiivisia päivityksiä HTTP:n kautta (`POST /responses`)
- Kääntää ne selkokielisiksi johtajayhteenvetoiksi
- Noudata jäsenneltyä tulostemuotoa (Mitä tapahtui / Liiketoiminnan vaikutus / Seuraava askel)
- Kieltäytyy aiheen ulkopuolisista pyynnöistä ja kehotteiden injektiokokeiluista
- Toimii säilöistettynä isännöitynä agenttina Microsoft Foundry Agent Service -palvelussa

---

## Keskeiset opitut käsitteet

| Käsite | Mitä harjoittelit |
|---------|-------------------|
| **Agenttikehyksen arkkitehtuuri** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` putki |
| **Isännöidyn agentin elinkaari** | Kehikko → Määrittely → Paikallinen testaus → Julkaisu → Pilven varmistus |
| **Järjestelmäkehotteiden suunnittelu** | Rooli, yleisö, tulostemuoto, säännöt, turvallisuusrajoitukset ja esimerkit |
| **Paikallinen vs. isännöity eroavaisuus** | Identiteetti (henkilökohtainen tunnistus vs. hallittu identiteetti), päätepiste, verkkopolku |
| **Turvallisuusrajat** | Kehoteinjektioiden torjunta, roolin noudattaminen, reunatapauksien hallittu käsittely |
| **Foundryn työkaluputken työnkulku** | Projektin luonti, mallien käyttöönotto, agentin kehikko, Agenttitarkastaja, yhdellä klikkauksella julkaisu |

---

## Mitä teit valmiiksi

### Polku A (Foundry-tilaus)

- [x] Asensit Foundry Toolkitin ja loit Foundry-projektin julkaistulla mallilla
- [x] Kehitit isännöidyn agentin automaattisesti luodulla projektirakenteella
- [x] Kirjoitit jäsennellyt agentin ohjeet turvallisuussäännöillä
- [x] Testasit paikallisesti 3 toiminnallisessa skenaariossa (Agenttitarkastaja)
- [x] Otit käyttöön Foundry Agent Servicessä (säilöitetty)
- [x] Varmistit pilvileikkikentässä 4 reunatapaus-/turvallisuustestiä

### Polku B (Foundry Local)

- [x] Asensit Foundry Toolkitin paikallisella malli-päätepisteellä
- [x] Kehitit isännöidyn agenttiprojektin
- [x] Kirjoitit jäsennellyt agentin ohjeet turvallisuussäännöillä
- [x] Testasit paikallisesti 3 toiminnallisessa skenaariossa
- [x] Varmistit agentin käyttäytymisen ilman pilviresursseja

---

## Seuraavat askeleet

### Jatka oppimista

| Resurssi | Kuvaus |
|----------|-------------|
| **[Lab 02 - Moniagenttien orkestrointi](../../lab02-multi-agent/docs/README.md)** | Rakenna 4-agenttinen työnkulku (Ansioluettelo → Työn soveltuvuusarvioija) orkestrointimalleilla |
| **[Lisää työkaluja agenttiisi](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Yhdistä API:t, tietokannat tai mukautetut funktiot Työkaluluettelon kautta |
| **[Lisää tietoa (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Perusta agenttisi dokumentteihin, vektorisäilöihin tai Bing-hakuun |
| **[Microsoft Foundryn dokumentaatio](https://learn.microsoft.com/azure/foundry/)** | Kattava alustan viite |
| **[Agent Framework SDK viitetiedot](https://learn.microsoft.com/agent-framework/)** | API-dokumentaatio `agent-framework`-paketille |
| **[Foundry Toolkit - Mitä uutta](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Laajennuksen julkaisumuistiinpanot ja muutosloki |

### Ideoita agenttisi laajentamiseen

- **Lisää päivämäärätyökalu** - Anna agentin sisällyttää "tämän päivän tilanteen" konteksti yhteenvetoihin
- **Yhdistä häiriötietokantaan** - Hae todellisia häiriötietoja työkalufunktion kautta
- **Lisää Bing-hakutyökalu** - Anna agentin hakea viimeaikaisia uutisia lisäkontekstiksi
- **Kokeile erilaisia malleja** - Vertaa `gpt-4.1` ja `gpt-4.1-mini` tulosten laatua
- **Arvioi Foundryn avulla** - Käytä Arviointitoimintoa mittaamaan agentin laatua laajassa mittakaavassa

### Polun B käyttäjille: Päivitys pilvipalveluun

Kun olet valmis julkaisemaan pilveen:
1. Hanki Azure-tilaus ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Suorita [Moduuli 01, Asennus](01-setup.md#step-2-set-up-based-on-your-access) (luo projekti, ota malli käyttöön, määritä RBAC)
3. Päivitä `.env` Foundry-projektin päätepisteellä ja mallin julkaisun nimellä
4. Jatka osiosta [Module 05 - Deploy to Foundry](05-deploy-to-foundry.md)

---

## Resurssien siivous (valinnainen)

Jos haluat poistaa tämän työpajan aikana luodut Azure-resurssit:

### Vaihtoehto 1: Poista resurssiryhmä (poistaa kaiken)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Vaihtoehto 2: Poista pelkkä isännöity agentti

1. Avaa [ai.azure.com](https://ai.azure.com) → projektisi → **Build** → **Agents**.
2. Klikkaa agenttiasi → klikkaa **Delete**.

### Vaihtoehto 3: Poista mallin käyttöönotto

1. Foundry-sivupalkissa laajenna projektisi → **Models**.
2. Oikealla napsautuksella mallin käyttöönotto → **Delete**.

> **Kustannusmuistutus:** Isännöidyt agentit aiheuttavat kustannuksia vain, kun ne ovat käynnissä. Jos pysäytät tai poistat agentin, kustannuksia ei tule. Mallin käyttöönotosta voi tulla pieni maksu varatusta kapasiteetista – poista se, jos olet valmis.

---

**Edellinen:** [06 - Verify in Playground](06-verify-in-playground.md) · **Seuraava:** [08 - Troubleshooting (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->