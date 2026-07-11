# Kuidas seda sessiooni läbi viia

Tänan, et viite selle sessiooni läbi!

Enne töötuba viimist palun:

1. Lugege see dokument ja kõik kaasatud materjalid läbi.
2. Vaadake sessiooni salvestust ja töötoa algusest lõpuni läbivaatamist.
3. Tehke mõlemad praktilised ülesanded läbi oma masinas **vähemalt üks kord** enne üritust.
4. Kontrollige oma Microsoft Foundry projekti, mudeli juurutusi ja kvoote.
5. Kui midagi on ebaselge, pöörduge hooldajate poole.

---

## Failide kokkuvõte

| Ressurss                    | Link                                                                             | Kirjeldus                                                                           |
|-----------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Töötoa slaidide deck        | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                    | Töötoa presentatsioonislaidid koos esineja märkmete ja sisse ehitatud demo videodega |
| Sessiooni salvestus         | _Hooldaja poolt esitatakse_                                                     | Töötoa sissejuhatus ja slaidide läbivaatuse salvestus                              |
| Töötoa algusest lõpuni salvestus | _Hooldaja poolt esitatakse_                                                     | Mõlema töötoa harjutuse algusest lõpuni salvestus õppija vaatepunktist              |
| Töötoa dokumentatsioon      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Allikakood, harjutuste README failid, samm-sammult moodulid                         |
| Harjutus 01 – ühe agendi        | [Lab 01](../workshop/lab01-single-agent/README.md)                             | Praktiline ülesanne: ehitada, testida ja juurutada *Explain Like I'm an Executive* majutatud agent |
| Harjutus 02 – mitme agendi töövoog | [Lab 02](../workshop/lab02-multi-agent/README.md)                              | Praktiline ülesanne: ehitada 4-agendi *Resume to Job Fit Evaluator* töövoog        |
| Demo 1: Juhataja agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                           | Harjutus 01 demo: tõlgi tehniline žargoon juhataja kokkuvõtteks                    |
| Demo 2: CV sobivuse hindaja         | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)   | Harjutus 02 demo: 4-agendi töövoog, mis hindab CV ja töö sobivust ja annab soovitusi |

> **Märkus koolitajatele:** Slaidide deck ja videolinkid lisatakse, kui salvestused on avaldatud. Seni võtke uuemate materjalide saamiseks ühendust hooldajaga (vt [Kontaktid](#kontaktid)).

---

## Alustamine

See töötuba õpetab arendajaid, kuidas ehitada, testida ja juurutada tehisintellekti agente **Microsoft Foundry Agent Service’i** platvormil kui **majutatavaid agente** täielikult VS Code'i kasutades, kasutades **Microsoft Foundry Toolkit** laiendust.

Töötuba on jaotatud mitmeks osaks, mis sisaldavad slaide, **2 otseülekande demo** ning **2 praktilist harjutust**.

### Ajastus

#### Täispikk esitlus (umbes 2 tundi)

| Aeg            | Kirjeldus                                                            |
|----------------|----------------------------------------------------------------------|
| 0:00 - 10:00   | Sissejuhatus: majutatud agendid, Foundry Agent Service ja toolkit      |
| 10:00 - 20:00  | Demo: Juhataja agent algusest lõpuni                                |
| 20:00 - 60:00  | Harjutus 01 – ühe agendi ülesanne (ehita, testi lokaalselt, juuruta, prooviala) |
| 60:00 - 110:00 | Harjutus 02 – mitme agendi töövoog (CV sobivuse hindaja)              |
| 110:00 - 120:00| Kokkuvõte, küsimused ja vastused ning edasise õppimise ressursid       |

#### Lühike esitlus (umbes 75 minutit)

| Aeg           | Kirjeldus                                                        |
|---------------|----------------------------------------------------------------|
| 0:00 - 10:00  | Sissejuhatus ja ülevaade                                        |
| 10:00 - 20:00 | Demo: Juhataja agent                                           |
| 20:00 - 70:00 | Ainult Harjutus 01 (suunake osalejad Harjutus 02 juurde iseseisvalt) |
| 70:00 - 75:00 | Kokkuvõte ja küsimused                                         |

### Ettevalmistus

| Ressurss                        | Link                                                                                          | Kirjeldus                                              |
|--------------------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------|
| Töötoa dokumentatsioon          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Töötoa dokumentatsioon ja allikad                      |
| Harjutus 01 juhised             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Praktiline ülesanne: ühe majutatud agendi loomine     |
| Harjutus 02 juhised             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Praktiline ülesanne: mitme agendi töövoog             |
| Eeltingimuste kontrollnimekiri | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Vajalike tööriistade, kontode ja Azure juurdepääsu loetelu |
| Majutatud agentide kiirstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Ametlik kiirstart majutatud agendi juurutamiseks `azd` abil |
| Majutatud agentide regioonide saadavus | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Toetatud regioonid majutatud agentidele (eelvaade)      |

### Koolitaja eelteadmised

Enne esitamist veenduge, et Teil oleks olemas:

- **Azure tellimus**, millel on luba ressursse luua (omanik või kaastööline ressursigrupis).
- Juurdepääs **Microsoft Foundry projektile** [majutatud agentidega toetatud regioonis](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvoot **gpt-4.1** (või **gpt-4.1-mini**) jaoks teie Foundry projektis.
- Järgmiste tööriistade installatsioon:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit laiendus](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (valikuline)
  - Python 3.10 või uuem

Käivitage enne töötuba vähemalt üks kord [Hosted agents quickstart `azd`-ga](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd), et omada kontrollitud Foundry projekti, mudeli juurutust ja Azure Container Registry’t, mida kasutada tekkivate küsimuste korral.

---

## Slaidide läbivaade

Deck järgib sama struktuuri nagu harjutused. Iga osa soovitatud rääkepunktid:

| Osa                       | Peamine sõnum                                                                                      |
|---------------------------|--------------------------------------------------------------------------------------------------|
| Pealkiri ja päevakord     | Sõnastage töötuba kui *VS Code to Foundry*, ilma et oleks vaja portaali vahetada.                |
| Miks majutatud agendid?    | Hallatud jooksuaeg, ACR-põhine juurutus, OpenAI-kompatible `/responses` API, piiratud Foundry projektidele. |
| Arhitektuuri diagramm      | Läbivaade [README arhitektuurist](../README.md#architecture): scaffolding, Inspector, ACR, Agent Service |
| Majutatud agendi olemus    | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - iga faili ülesanded.                   |
| Otseülekande demo: Juhataja agent | Lülituge VS Code’i ja jooksutage [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo algusest lõpuni (vt [Demo 1](#demo-1-juhataja-agent)). |
| Otseülekande demo: CV sobivuse hindaja | Lülituge VS Code’i ja jooksutage [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agendi demo (vt [Demo 2](#demo-2-cv-sobivuse-hindaja)). |
| Harjutus 01 tutvustus       | Andke õppijatele üle, suunake [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Mitme agendi mustrid        | Sekventaalne vs korraga vs üleandmine - eelvaade enne Harjutus 02 algust.                         |
| Harjutus 02 tutvustus       | Andke õppijatele üle, suunake [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Kokkuvõte ja ressursid     | Edasise õppimise lingid [Täiendavate ressursside](#täiendavad-ressursid) sektsioonist.             |

---

## Demod

Esitluses on kaasatud kaks otseülekande demo. Igaühele eraldage 10 minutit.

| Demo                | Harjutus | Failid                                              | Mida näidata                                      |
|---------------------|----------|----------------------------------------------------|--------------------------------------------------|
| Juhataja agent      | Harjutus 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Üksik majutatud agent; tõlkige tehniline keelekasutus juhataja kokkuvõtteks |
| CV sobivuse hindaja | Harjutus 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agendi orkestreerimine; hindage CV-töö sobivust ja tehke soovitusi |

### Demo 1: Juhataja agent

Iseseisev agent kaustas [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Kasutage seda 10-minutilise demonstreerimiseks enne Harjutus 01 algust.

1. Avage [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) ja tutvustage agendi määratlust (süsteemi sõnum, mudel, raamistik).
2. Vajutage `F5`, et käivitada **Agent Inspector** lokaalselt.
3. Kleepige näidisüleskutse [README-st](../README.md#see-it-in-action) ja näidake juhatajalt saadud kokkuvõttevastust.
4. Näidake [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) ja [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile), et seletada juurutuse artefakte.
5. Demonstreerige juurutusprotsessi (Docker build, ACR push, majutatud agendi loomine) ilma edasilükkamiseta.

### Demo 2: CV sobivuse hindaja

Nelja agendi töövoog kaustas [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Kasutage seda 10-minutilise demonstreerimiseks enne Harjutus 02 algust.

1. Avage [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ja selgitage, kuidas neli agenti on järjestikuse orkestreerimise jaoks ühendatud.
2. Vajutage `F5`, et käivitada **Agent Inspector** mitme agendi töövoo jaoks.
3. Kopeerige lühike töökuulutus ja näidis-CV Inspector'i vestlusesse.
4. Läbige nelja agendi torujuhe: CV parser, töö nõuete eraldaja, sobivuse hindaja ja soovituste kirjutaja.
5. Näidake, kuidas iga sub-agendi väljund saab järgmise agendi kontekstiks, tõstes esile üleandmise mustrit.
6. Näidake [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml), et võrrelda seda Demo 1 vastava üksikagendiga.

---

## Esitlusnõuanded

- **Pange ootused paika varakult.** Majutatud agendid on eelvaates - teavitage regioonipiirangutest ja kvootidest enne töötuba, et osalejad ei jääks vahepeal üllatuma.
- **Käivitage eeltingimuste ülesanne esimesena.** Mõlemal harjutusel on `Validate prerequisites` VS Code ülesanne - laske osalejatel see enne koodi kirjutamist läbi teha.
- **Hoidke Agent Inspector nähtaval.** Enamik "aha" hetki tekib, kui õppijad näevad kohalikku `/responses` ringkäiku valgustumas.
- **Olge varuprojekt valmis.** Kui õppija Foundry projekt jõuab kvootide piirini, jagage eelnevalt valmis projekte juurutusastmes, et vältida ruumi blokeerimist.
- **Paaristage osalejad.** Harjutus 02 (mitme agendi töövoog) on oluliselt lihtsam, kui osalejad saavad orkestreerimist partneriga arutada.
- **Kasuta dokumentatsioonimooduleid peatustena.** Iga harjutuse `docs/` kaust jaguneb 8 numbritud mooduliks - kasuta neid loomulikeks pauspunktideks.
- **Eelpüllake baaspildi Docker masinatesse**, et vältida repositooriumi määrangupiiranguid.

---

## Probleemide lahendamine esitamise ajal

| Sümptom                                 | Esimene proovimiseks sobiv asi                                                        |
|-----------------------------------------|---------------------------------------------------------------------------------------|
| Agent Inspector ei saa ühendust         | Kontrolli, et port `8088` on vaba ja et `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` ülesanne töötab. |
| Debuggeri kinnitamine ei õnnestu        | Kontrolli, et port `5679` on vaba; taaskäivita VS Code, kui `debugpy` on juba seotud.   |
| `azd up` annab autentimisvea           | Käivita `az login` ja `azd auth login`, veendu, et õige tenant on valitud.            |
| Juurutus jääb pidama ACR push ajal       | Kontrolli, et Docker Desktop töötab ja kasutajal on ACR repositooriumile `AcrPush` õigus. |
| Mudel tagastab 404 / deployment-not-found | Mudeli juurutuse nimi `agent.yaml` failis peab ühtima Foundry projekti juurutusega.     |

| Hostitud agendi kinni jäämine `Provisioning` olekus | Kontrollige, kas projekti piirkond [toetab hostitud agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ja kas kvota on saadaval. |
| Mänguväljak tagastab 401                    | Autentige Foundry laiendus uuesti VS Code aktiivsusribalt.                                       |

Põhjalikumate juhiste jaoks on igal laboris oma `08-troubleshooting.md` dokument - suunake õppijad sinna:

- Labor 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Labor 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Sessiiooni kohandamine

Olete teretulnud töötoa kohandamiseks oma publikule. Levinud variandid:

- **Andmebaasi publik:** veetke rohkem aega `agent.yaml`, Dockeri ja ACR-ga; vähendage mänguväljaku demosid.
- **Kodaniku-arendaja publik:** jääge Foundry laienduse kasutajaliidesesse scaffoldinguks; vähendage käsurea samme.
- **Üksikut 60-minutilist sessiooni:** esitage ainult sissejuhatus, demo ja Labor 01.
- **Ainult töötuba (ilma slaidideta) formaat:** avage mõlemad laborite README failid ja kasutage neid põhiskriptina.

Kui laiendate laboreid, palun andke muudatused tagasi PR-i kaudu, et ka teised koolitajad sellest kasu saaksid.

---

## Täiendavad ressursid

- [Microsoft Foundry dokumentatsioon](https://learn.microsoft.com/azure/ai-foundry/)
- [Hostitud agentide ülevaade](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Kiire algus: deploy oma esimene hostitud agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Hostitud agendi paigaldamine (kuidas teha)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry tööriistakomplekt VS Code jaoks](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontaktid

Kui teil on selle sessiooni läbiviimise kohta küsimusi, avage palun teema [töötoa hoidlas](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) ja märkige hooldaja.

| Roll                | Nimi           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Hooldaja / kontakt | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->