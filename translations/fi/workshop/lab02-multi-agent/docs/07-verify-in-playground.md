# Moduuli 7 - Vahvista Playgroundissa

⏱️ ~10 min

Tässä moduulissa testaat käyttöönotetun moni-agenttisen työnkulun VS Codessa ja Foundry-portaalissa varmistaen, että agentti käyttäytyy samalla tavalla kuin paikallisesti testattaessa.

---

## Miksi testata uudelleen käyttöönoton jälkeen?

Isäntäympäristö poikkeaa paikallisesta muutamilla tärkeillä tavoilla:

| | Paikallinen | Isännöity |
|--|-----------|------------|
| **Tunniste** | Henkilökohtainen sisäänkirjautumisesi (`DefaultAzureCredential`) | Kullekin agentille omistettu Entra-tunniste (automaattisesti määritetty käyttöönoton yhteydessä) |
| **Päätepiste** | `http://localhost:8088/responses` | Foundry Agent Service hallinnoima URL |
| **Verkko** | Laiteesi → Azure OpenAI + MCP | Azure-verkon selkäranka (alhaisempi latenssi) |

Väärin määritetty ympäristömuuttuja, RBAC-ongelma tai estetty MCP:n ulospäin suuntautuva kutsu näkyisi ensin täällä.

---

## Vaihtoehto A: Testaa VS Code Playgroundissa (suositeltava ensin)

### Vaihe 1: Siirry isännöityyn agenttiisi

1. Napsauta **Foundry Toolkit** -kuvaketta Aktiviteettipalkissa.
2. Laajenna projektisi → **Hosted Agents (Preview)** → etsi agenttisi.

![Foundry Toolkit sivupalkki näyttää Hosted Agents (Preview) -osion, jossa on resume-job-fit-evaluator ja sen käyttöönotetut versiot](../../../../../translated_images/fi/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Vaihe 2: Valitse versio

1. Napsauta agenttia laajentaaksesi sen versiot.
2. Napsauta `v1` → varmista, että tila on **active** (sivupalkissa voi näkyä "Running" tai "Started" - molemmat tarkoittavat samaa valmista tilaa).

### Vaihe 3: Avaa Playground

1. Napsauta **Playground** (tai napsauta versiota hiiren oikealla → **Open in Playground**).
2. Keskusteluikkuna avautuu VS Code -välilehdelle.

### Vaihe 4: Suorita savutestit

Käytä samoja 3 testiä kuin [Moduulissa 5](05-test-locally.md). Kirjoita kukin viesti Playground-syötekenttään ja paina **Send** (tai **Enter**).

#### Testi 1 - Täysi ansioluettelo + JD (vakio kulku)

Liitä kokonainen ansioluettelo + JD -kehotus Moduulin 5 Testi 1 mukaan (Jane Doe + Senior Cloud Engineer Contoso Ltd:llä).

**Odotettu:**
- Soveltuvuusarvio pisteytyksineen (100 pisteen asteikko)
- Vastaa taitoja -osio
- Puuttuvat taidot -osio
- **Yksi aukko-kortti jokaista puuttuvaa taitoa kohden** Microsoft Learn -URL-osoitteilla
- Oppimispolku aikatauluineen

#### Testi 2 - Pikatesti (minimaalinen syöte)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Odotettu:**
- Alhaisempi soveltuvuusarvio (< 40)
- Rehellinen arviointi vaiheistetulla oppimispolulla
- Useita aukko-kortteja (AWS, Kubernetes, Terraform, CI/CD, kokemusaukko)

#### Testi 3 - Hyvin soveltuva ehdokas

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Odotettu:**
- Korkea soveltuvuusarvio (≥ 80)
- Keskittyy haastatteluun valmistautumiseen ja hiomiseen
- Vähän tai ei lainkaan aukko-kortteja
- Lyhyt aikataulu keskittyen valmistautumiseen

### Vaihe 5: Vertaa paikallisiin tuloksiin

Avaa muistiinpanosi tai selainvälilehtesi Moduulista 5, johon tallensit paikalliset vastaukset. Jokaiselle testille:

- Onko vastauksessa **sama rakenne** (soveltuvuusarvio, aukko-kortit, oppimispolku)?
- Noudettaako se **samaa pisteytyssysteemiä** (100 pisteen erittely)?
- Onko **Microsoft Learn -URL-osoitteet** edelleen mukana aukko-korteissa?
- Onko **yksi aukko-kortti per puuttuva taito** (ei katkaistu)?

> **Pienet sanamuutokset ovat normaaleja** - malli ei ole deterministinen. Keskity rakenteeseen, pisteytyksen yhdenmukaisuuteen ja MCP-työkalun käyttöön.

---

## Vaihtoehto B: Testaa Foundry-portaalissa

[Foundry Portal](https://ai.azure.com) tarjoaa verkkopohjaisen playgroundin, joka on hyödyllinen tiimikavereiden tai sidosryhmien kanssa jaettavaksi.

### Vaihe 1: Avaa Foundry Portal

1. Avaa selain ja siirry osoitteeseen [https://ai.azure.com](https://ai.azure.com).
2. Kirjaudu sisään samalla Azure-tilillä, jota olet käyttänyt koko työpajan ajan.

### Vaihe 2: Siirry projektiisi

1. Kotisivulla etsi vasemman sivupalkin kohdalta **Recent projects**.
2. Napsauta projektisi nimeä (esim. `workshop-agents`).
3. Jos et näe projektia, napsauta **All projects** ja hae sitä.

### Vaihe 3: Etsi käyttöönotettu agenttisi

1. Valitse projektin vasemmassa navigaatiossa **Build** → **Agents** (tai etsi **Agents**-osio).
2. Sinun pitäisi nähdä lista agenteista. Etsi käyttöönotettu agenttisi (esim. `resume-job-fit-evaluator`).
3. Napsauta agentin nimeä avataksesi sen tiedot.

### Vaihe 4: Avaa Playground

1. Agentin tietosivulla katso yläreunan työkalupalkkia.
2. Napsauta **Open in playground** (tai **Try in playground**).
3. Keskusteluikkuna aukeaa.

### Vaihe 5: Suorita samat savutestit

Toista kaikki 3 testiä VS Code Playground -osiosta yllä. Vertaa kutakin vastausta sekä paikallisiin tuloksiin (Moduuli 5) että VS Code Playgroundin tuloksiin (vaihtoehto A yllä).

---

## Moni-agentti-spesifinen varmennus

Peruskelpoisuuden lisäksi varmista nämä moni-agentille ominaiset käyttäytymiset:

### MCP työkalun suoritus

| Tarkista | Miten varmistaa | Läpäisyehto |
|---------|-----------------|-------------|
| MCP-kutsut onnistuvat | Aukko-korteissa osoitteet `learn.microsoft.com` | Oikeat URL-osoitteet, ei korvaavia viestejä |
| Useita MCP-kutsuja | Jokaisella Korkea/Keskitason prioriteetin aukolla on resursseja | Ei vain ensimmäinen aukko-kortti |
| MCP-fallback toimii | Jos URL-osoitteet puuttuvat, tarkista korvaava teksti | Agentti tuottaa aukko-kortit (URL-osoitteista riippumatta) |

### Agenttien koordinointi

| Tarkista | Miten varmistaa | Läpäisyehto |
|---------|-----------------|-------------|
| Kaikki 4 agenttia käynnissä | Tuloste sisältää soveltuvuusarvion JA aukko-kortit | Arvio tulee MatchingAgentilta, kortit GapAnalyzerilta |
| Peräkkäinen suoritus | Vastausaika on kohtuullinen (< 2 min) | Jos > 3 min, tarkista virheet terminaalin lokista |
| Datan eheys | Aukko-korteissa viitataan taitoihin matching-raportista | Ei kuvitteellisia taitoja, joita ei ole JD:ssä |

---

## Varmennusrubriikki

Käytä tätä rubriikkia arvioidessasi moni-agenttisen työnkulun isännöityä käyttäytymistä:

| # | Kriteeri | Läpäisyehto | Läpäisy? |
|---|----------|-------------|----------|
| 1 | **Toiminnallinen oikeellisuus** | Agentti vastaa ansioluettelo + JD:hen soveltuvuusarviolla ja aukkoanalyysilla | |
| 2 | **Pisteytyksen yhdenmukaisuus** | Soveltuvuusarvio käyttää 100 pisteen asteikkoa erittelyineen | |
| 3 | **Aukko-korttien täydellisyys** | Yksi kortti jokaista puuttuvaa taitoa kohden (ei katkaistu tai yhdistetty) | |
| 4 | **MCP työkalun integraatio** | Aukko-korteissa on oikeat Microsoft Learn -URL-osoitteet | |
| 5 | **Rakenteen yhdenmukaisuus** | Tulosteen rakenne vastaa paikallisen ja isännöidyn suorituksen välillä | |
| 6 | **Vastausaika** | Isännöity agentti vastaa täydessä arvioinnissa 2 minuutin sisällä | |
| 7 | **Ei virheitä** | Ei HTTP 500 virheitä, aikakatkaisuja tai tyhjiä vastauksia | |

> "Läpimenolla" tarkoitetaan, että kaikki 7 kriteeriä täyttyvät kaikissa 3 savutestissä vähintään yhdessä playgroundissa (VS Code tai Portaali).

---

## Playground-ongelmien vianmääritys

| Oire | Todennäköinen syy | Korjaus |
|-------|---------------|---------|
| Playground ei lataudu | Säiliö ei ole `active`-tilassa | Palaa [Moduuli 6](06-deploy-to-foundry.md) sivulle, vahvista käyttöönoton tila. Odota jos `creating` |
| Agentti palauttaa tyhjän vastauksen | Mallin käyttöönoton nimi ei vastaa | Tarkista `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` vastaa käyttöönotettua mallia |
| Agentti palauttaa virheilmoituksen | [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) -käyttöoikeus puuttuu | Määritä **[Foundry User](https://aka.ms/foundry-ext-project-role)** (aiemmin Azure AI User) projektin tasolla |
| Ei Microsoft Learn -URL-osoitteita aukko-korteissa | MCP:n ulospäin suuntautuva liikenne estetty tai MCP-palvelin ei käytettävissä | Tarkista, että säiliö pääsee `learn.microsoft.com` -osoitteeseen. Katso [Moduuli 8](08-troubleshooting.md) |
| Vain 1 aukko-kortti (katkaistu) | GapAnalyzer-ohjeesta puuttuu "CRITICAL" -lohko | Tarkista [Moduuli 3, Vaihe 2.4](03-configure-agents.md) |
| Soveltuvuusarvio poikkeaa paikallisesta suuresti | Eri malli tai ohjeet otettu käyttöön | Vertaa `agent.yaml`-ympäristömuuttujia paikalliseen `.env`-tiedostoon. Ota käyttöön uudelleen tarpeen mukaan |
| "Agentti ei löydy" portaalissa | Käyttöönotto on vielä leviämässä tai epäonnistui | Odota 2 minuuttia, päivitä sivu. Jos puuttuu edelleen, ota uudelleen käyttöön [Moduuli 6](06-deploy-to-foundry.md) sivulta |

---

### Tarkistuspiste

- [ ] Testattu agentti VS Code Playgroundissa - kaikki 3 savutestiä läpäisty
- [ ] Testattu agentti [Foundry Portaalissa](https://ai.azure.com) Playgroundissa - kaikki 3 savutestiä läpäisty
- [ ] Vastaukset ovat rakenteellisesti yhteneväiset paikallisen testauksen kanssa (soveltuvuusarvio, aukko-kortit, oppimispolku)
- [ ] Microsoft Learn -URL-osoitteet ovat läsnä aukko-korteissa (MCP työkalu toimii isännöidyssä ympäristössä)
- [ ] Yksi aukko-kortti jokaista puuttuvaa taitoa kohden (ei katkaisua)
- [ ] Ei virheitä tai aikakatkaisuja testauksen aikana
- [ ] Täytetty varmistusrubriikki (kaikki 7 kriteeriä läpäisty)

---

**Edellinen:** [06 - Käyttöönotto Foundryssa](06-deploy-to-foundry.md) · **Seuraava:** [08 - Vianmääritys →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->