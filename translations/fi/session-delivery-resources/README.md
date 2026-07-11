# Kuinka toteuttaa tämä sessio

Kiitos, että toteutat tämän session!

Ennen työpajan toteutusta, tee seuraavat:

1. Lue tämä asiakirja ja kaikki siihen sisältyvät resurssit kokonaisuudessaan.
2. Katso session toteutusvideo ja työpajan läpikäynti alusta loppuun.
3. Käy läpi molemmat käytännön laboratoriot loppuun asti omalla koneellasi **vähintään kerran** ennen tapahtumaa.
4. Vahvista Microsoft Foundry -projektisi, mallien käyttöönotot ja kvotat.
5. Ota yhteyttä ylläpitäjään, jos jokin on epäselvää.

---

## Tiedostoyhteenveto

| Resurssi                     | Linkki                                                                            | Kuvaus                                                                                      |
|-----------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Työpajan esitysdioitus       | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                    | Työpajan esitysdiaesitykset esittäjän muistiinpanoineen ja upotettuine demovideoineen        |
| Session toteutusvideo         | _Ylläpitäjän toimittama_                                                         | Työpajan esittely ja diojen läpikäynti videolla                                             |
| Työpajan läpikäyntivideo      | _Ylläpitäjän toimittama_                                                         | Molempien laboratorioiden läpikäynti videolla oppijan näkökulmasta                          |
| Työpajadokumentaatio         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Lähdekoodivarasto, laboratoriolukemiset, vaiheittaiset moduulit                            |
| Lab 01 - yksittäinen agentti | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Käytännön laboratorio: *Explain Like I'm an Executive* -isäntäagentin rakentaminen, testaus ja käyttöönotto |
| Lab 02 - monagenttityönkulku | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Käytännön laboratorio: neljän agentin *Resume to Job Fit Evaluator* -työnkulun rakentaminen   |
| Demo 1: Executive Agent       | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                             | Lab 01 demonstraatio: teknisen jargon kääntäminen johtoryhmälle suunnatuksi tiivistelmäsisällöksi |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Lab 02 demonstraatio: neljän agentin työnkulku, joka arvioi ansioluettelon ja työpaikan yhteensopivuutta sekä tuottaa suosituksia |

> **Huomio kouluttajille:** Dioitus ja videot lisätään, kun nauhoitukset julkaistaan. Sitä ennen ota yhteyttä ylläpitäjään (katso [Yhteystiedot](#yhteystiedot)) saadaksesi uusimmat materiaalit.

---

## Aloittaminen

Tämä työpaja opettaa kehittäjiä rakentamaan, testaamaan ja ottamaan käyttöön tekoälyagentteja **Microsoft Foundry Agent Service** -palveluun **Isäntäagenteiksi** kokonaan VS Code -ympäristöstä käyttäen **Microsoft Foundry Toolkit** -laajennusta.

Työpaja on jaettu useisiin osioihin sisältäen dioja, **2 live-demosta** ja **2 käytännön laboratoriota**.

### Aikataulu

#### Koko toteutus (noin 2 tuntia)

| Aika           | Kuvaus                                                               |
|----------------|----------------------------------------------------------------------|
| 0:00 - 10:00   | Johdanto: isäntäagentit, Foundry Agent Service ja toolkit            |
| 10:00 - 20:00  | Demo: Executive Agent kokonaisuudessaan                              |
| 20:00 - 60:00  | Lab 01 - yksittäinen agentti (rakennus, paikallinen testaus, käyttöönotto, leikkikenttä) |
| 60:00 - 110:00 | Lab 02 - monagenttityönkulku (Resume to Job Fit Evaluator)           |
| 110:00 - 120:00| Yhteenveto, kysymykset ja vastaukset sekä jatko-opiskeluresurssit     |

#### Lyhyt toteutus (noin 75 minuuttia)

| Aika          | Kuvaus                                                            |
|---------------|------------------------------------------------------------------|
| 0:00 - 10:00  | Johdanto ja yleiskatsaus                                        |
| 10:00 - 20:00 | Demo: Executive Agent                                           |
| 20:00 - 70:00 | Vain Lab 01 (ohjaa osallistujat tekemään Lab 02 itsenäisesti)   |
| 70:00 - 75:00 | Yhteenveto ja kysymykset                                        |

### Valmistautuminen

| Resurssi                      | Linkki                                                                                  | Kuvaus                                         |
|------------------------------|-----------------------------------------------------------------------------------------|------------------------------------------------|
| Työpajadokumentaatio          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)        | Työpajadokumentaatio ja lähdekoodi             |
| Lab 01 ohjeet                 | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                           | Käytännön laboratorio: yksittäinen isäntäagentti            |
| Lab 02 ohjeet                 | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                             | Käytännön laboratorio: monagenttityönkulku  |
| Esivaatimusten tarkistuslista | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)           | Tarvittavat työkalut, tilit ja Azure-käyttöoikeudet    |
| Isäntäagenttien pikaopas (azd)| [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Virallinen pikaopas isäntäagentin käyttöönottoon `azd`-työkalulla |
| Isäntäagenttien alueellinen saatavuus | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Tuetut alueet isäntäagenteille (esikatselu)           |

### Kouluttajan vaatimukset

Ennen toteutusta varmista, että sinulla on:

- **Azure-tilaus**, jolla on oikeus luoda resursseja (Omistaja tai Avustaja resurssiryhmässä).
- Pääsy **Microsoft Foundry -projektiin** [alueella, joka tukee isäntäagenteja](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvota **gpt-4.1** (tai **gpt-4.1-mini**) Foundry-projektissasi.
- Seuraavat asennetut työkalut:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit -laajennus](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Valinnainen)
  - Python 3.10 tai uudempi

Suorita [Isäntäagenttien pikaopas `azd`:llä](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) vähintään kerran ennen toteutusta, jotta sinulla on tunnetusti toimiva Foundry-projekti, mallin käyttöönotto ja Azure Container Registry käytettävissä, jos oppija jää jumiin.

---

## Dian läpikäynti

Esitysdioitus noudattaa samaa rakennetta kuin laboratoriot. Ehdotetut puheenaiheet jokaiselle osalle:

| Osio                        | Keskeinen viesti                                                                                             |
|----------------------------|-------------------------------------------------------------------------------------------------------------|
| Otsikko ja agenda           | Kehystä työpaja *VS Codesta Foundryyn* ilman portaalin vaihtoa.                                            |
| Miksi isäntäagentit?       | Hallittu ajoitus, ACR-pohjainen käyttöönotto, OpenAI-yhteensopiva `/responses` API, rajattu Foundry-projekteihin. |
| Arkkitehtuurikaavio         | Käy läpi [README arkkitehtuuri](../README.md#architecture): scaffolding, Inspector, ACR, Agent Service.      |
| Isäntäagentin rakenne       | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - mitä kukin tiedosto tekee.                         |
| Live-demo: Executive Agent  | Vaihda VS Codeen ja suorita [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo alusta loppuun (katso [Demo 1](#demo-1-executive-agent)). |
| Live-demo: Resume to Job Fit Evaluator | Vaihda VS Codeen ja suorita [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) neljän agentin demo (katso [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 lyhyt esittely      | Anna osallistujille. Viittaa [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Monagenttimallit            | Peräkkäinen vs rinnakkainen vs luovutus - esikatsele ennen Lab 02:n aloitusta.                               |
| Lab 02 lyhyt esittely      | Anna osallistujille. Viittaa [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Yhteenveto ja resurssit     | Jatko-opiskeluresurssit [Lisäresurssit](#lisäresurssit) -osiosta.                                     |

---

## Demot

Toteutuksessa on mukana kaksi live-demoa. Varaukset kullekin 10 minuuttia.

| Demo               | Lab  | Tiedostot                                                 | Näytettävä sisältö                                     |
|--------------------|------|-----------------------------------------------------------|--------------------------------------------------------|
| Executive Agent     | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Yksittäinen isäntäagentti; käännä tekninen jargon johtoryhmätiivistelmäksi |
| Resume to Job Fit Evaluator | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Neljän agentin orkestrointi; pisteytä ansioluettelon ja työn yhteensopivuus ja luo suositus |

### Demo 1: Executive Agent

Itsenäinen agentti sijainnissa [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Käytä tätä 10 minuutin demon esittelyyn ennen Lab 01:a.

1. Avaa [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) ja käy läpi agentin määritelmä (järjestelmän kehote, malli, kehys).
2. Paina `F5` käynnistääksesi **Agent Inspectorin** paikallisesti.
3. Liitä esimerkkikehote [README](../README.md#see-it-in-action) -kohdasta ja näytä johtoryhmätiivistelmä.
4. Näytä [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) ja [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) selittääksesi käyttöönoton artefaktit.
5. Demonstroi käyttöönoton kulku (Docker-rakennus, ACR-push, isäntäagentin luonti) ilman odotusta valmistumiseen.

### Demo 2: Resume to Job Fit Evaluator

Neljän agentin työnkulku sijainnissa [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Käytä tätä 10 minuutin demon esittelyyn ennen Lab 02:a.

1. Avaa [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ja näytä, kuinka neljä agenttia on kytketty peräkkäiseen orkestrointiin.
2. Paina `F5` käynnistääksesi **Agent Inspectorin** monagenttityönkululle.
3. Liitä lyhyt työkuvaus ja esimerkkian sioluettelo Inspector-chatissa.
4. Käy läpi neljän agentin putki: ansioluettelon jäsentäjä, työvaatimusten poimija, yhteensopivuuden pisteyttäjä ja suositusten kirjoittaja.
5. Korosta, kuinka jokaisen alatason agentin tuotos toimii seuraavan agentin kontekstina, korosta luovutusmallia.
6. Näytä [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) vertaillaksesi Demo 1:n yksittäisen agentin vastaavan kanssa.

---

## Toteutusvinkit

- **Aseta odotukset varhaisessa vaiheessa.** Isäntäagentit ovat esikatseluvaiheessa – tuo alueelliset rajoitukset ja kvotat selkeästi esiin, jotta osallistujat eivät ylläty työn aikana.
- **Suorita esivaatimusten tehtävä ensin.** Molemmat laboratoriot sisältävät `Validate prerequisites` -VS Code -tehtävän – anna osallistujien ajaa se ennen koodaamisen aloittamista.
- **Pidä Agent Inspector näkyvissä.** Useimmat "aha" -hetket tapahtuvat, kun oppijat näkevät paikallisen `/responses`-kierroksen syttymisen.
- **Ole varalla varaprojekti.** Jos oppijan Foundry-projekti kohtaa kvotarajan, tarjoa etukäteen varattu projekti käyttöönotto vaiheessa, jotta luokka ei pysähdy.
- **Parita osallistujat.** Lab 02 (monagenttityönkulku) on selvästi helpompi, kun oppijat voivat keskustella yhteistyökumppanin kanssa orkestroinnista.
- **Käytä dokumentaatiomoduuleja tarkastuskohtina.** Kunkin laboratorion `docs/` -kansio on jaettu 8 numeroituun moduuliin – käytä näitä luonnollisina taukokohtina.
- **Vedä perus-Docker-kuva valmiiksi** jaetuille lab-koneille välttääksesi rekisterin nopeusrajoitukset.

---

## Vianmääritys toteutuksen aikana

| Oire                                     | Ensimmäinen kokeiltava asia                                                                             |
|------------------------------------------|---------------------------------------------------------------------------------------------------------|
| Agent Inspector ei yhdisty                | Varmista, että portti `8088` on vapaa ja `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` -tehtävä toimii. |
| Debuggeri ei kiinnity                    | Tarkista, että portti `5679` on vapaa; käynnistä VS Code uudelleen, jos `debugpy` on jo sidottu.          |
| `azd up` epäonnistuu autentikointivirheeseen | Suorita `az login` ja `azd auth login`, varmista että oikea vuokraaja on valittu.                         |
| Käyttöönotto jumittuu ACR pushissa       | Tarkista, että Docker Desktop toimii ja käyttäjällä on `AcrPush` lupa rekisteriin.                        |
| Malli palauttaa 404 / deployment-not-found | Mallin käyttöönoton nimi `agent.yaml`-tiedostossa täytyy vastata Foundry-projektin käyttöönottoa.         |

| Isännöity agentti jumissa tilassa `Provisioning` | Varmista, että projektin alue [tukee isännöityjä agentteja](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ja että kiintiötä on saatavilla. |
| Playground palauttaa 401                          | Kirjaudu uudelleen Foundry-laajennukseen VS Coden toiminta-palkista.                                     |

Syvällisempää ohjausta varten jokainen labratuotanto sisältää oman `08-troubleshooting.md` -tiedoston – ohjaa opiskelijat sinne:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Tämän istunnon räätälöinti

Olet tervetullut mukauttamaan työpajaa yleisöllesi. Yleisiä variaatioita:

- **Backend-yleisöt:** käytä enemmän aikaa `agent.yaml`-tiedostoon, Dockeriin ja ACR:ään; lyhennä playground-demoa.
- **Citizen-kehittäjäyleisöt:** pysy Foundry-laajennuksen käyttöliittymässä kehystä varten; vähennä komentorivitoimia.
- **Yhden raidan 60 minuutin osio:** esittele vain johdanto, demo ja Lab 01.
- **Pelkkä työpaja (ei dioja) -formaatti:** avaa molemmat labien README:t ja käytä niitä pääasiallisena käsikirjoituksena.

Jos laajennat labratuotantoja, ole hyvä ja palauta muutokset PR:n kautta, jotta muut kouluttajat hyötyvät.

---

## Lisäresurssit

- [Microsoft Foundryn dokumentaatio](https://learn.microsoft.com/azure/ai-foundry/)
- [Isännöityjen agenttien yleiskatsaus](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Nopea aloitus: ota ensimmäinen isännöity agentti käyttöön (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Isännöidyn agentin käyttöönotto (ohje)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit VS Codeen](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Yhteystiedot

Jos sinulla on kysyttävää tämän istunnon toteutuksesta, avaa issue [workshop-repositoriossa](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) ja tägää vastuuhenkilö.

| Rooli                 | Nimi           | GitHub                                                  |
|-----------------------|----------------|---------------------------------------------------------|
| Vastuuhenkilö / kontakti | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->