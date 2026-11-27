# Kuidas see sessioon läbi viia

Aitäh, et viite selle sessiooni läbi!

Enne töötuba läbiviimist palun:

1. Lugege see dokument ja kõik seotud ressursid hoolikalt läbi.
2. Vaadake sessiooni läbiviimise salvestust ja töötoa kogu protsessi ülevaadet.
3. Läbige mõlemad praktilised töötoad oma masinas **vähemalt üks kord** enne sündmust.
4. Kontrollige oma Microsoft Foundry projekti, mudelite juurutusi ja kvoote.
5. Kui midagi jääb ebaselgeks, võtke ühendust haldajaga.

---

## Faili kokkuvõte

| Ressurss                      | Link                                                                             | Kirjeldus                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Töötoa slaidide komplekt       | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Selle töötoa esitlusslaidid koos esitaja märkmete ja manustatud demo videotega               |
| Sessiooni läbiviimise salvestus| _Vastutab haldaja_                                               | Töötoa sissejuhatus ja slaidide läbivaatamise salvestus                                    |
| Töötoa kogu protsessi salvestus| _Vastutab haldaja_                                               | Kogu mõlema töötoa ülesande salvestus õppija vaatenurgast                                  |
| Töötoa dokumentatsioon         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Allikate hoidla, töötoa juhendid, samm-sammult moodulid                                     |
| Töötuba 01 - üksagent          | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Praktiline töötuba: ehitada, testida ja juurutada *Explain Like I'm an Executive* majutatud agent |
| Töötuba 02 - mitu-agent töövoog| [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Praktiline töötuba: ehitada 4-agendi *Resume to Job Fit Evaluator* töövoog                   |
| Demo 1: Executive Agent        | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Töötuba 01 demo: tõlkida tehnilist žargooni juhtkonna kokkuvõtteks                           |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Töötuba 02 demo: 4-agendi töövoog, mis hindab CV ja töö sobivust ning annab soovitusi         |

> **Märkus koolitajatele:** Slaidikomplekt ja videolinkid lisatakse, kui salvestused avalikustatakse. Seni võtke värskemate materjalide saamiseks ühendust haldajaga (vt [Kontaktid](#contacts)).

---

## Alustamine

See töötuba õpetab arendajaid, kuidas ehitada, testida ja juurutada tehisintellekti agente **Microsoft Foundry Agent Service'isse** kui **majutatuid agente** täielikult VS Code'i kaudu, kasutades **Microsoft Foundry Toolkiti** laiendust.

Töötoa koosseisu kuuluvad mitmed sektsioonid, sealhulgas slaidid, **2 reaalajas demo** ja **2 praktilist töökohta**.

### Ajakava

#### Täismahus läbiviimine (umbes 2 tundi)

| Aeg            | Kirjeldus                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Sissejuhatus: majutatud agendid, Foundry Agent Service ja tööriistakomplekt |
| 10:00 - 20:00   | Demo: Executive Agent algusest lõpuni                               |
| 20:00 - 60:00   | Töötuba 01 - üksagent (koosta, testi kohapeal, juuruta, katseväljak)|
| 60:00 - 110:00  | Töötuba 02 - mitu-agent töövoog (Resume to Job Fit Evaluator)        |
| 110:00 - 120:00 | Kokkuvõte, küsimused ja vastused ning jätkuva õppimise ressursid     |

#### Lühendatud läbiviimine (umbes 75 minutit)

| Aeg          | Kirjeldus                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Sissejuhatus ja ülevaade                                   |
| 10:00 - 20:00 | Demo: Executive Agent                                      |
| 20:00 - 70:00 | Ainult Töötuba 01 (osalejatele suunata Töötuba 02 iseseisvaks õppimiseks) |
| 70:00 - 75:00 | Kokkuvõte ja küsimused-vastused                            |

### Ettevalmistus

| Ressurss                       | Link                                                                                          | Kirjeldus                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Töötoa dokumentatsioon         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Töötoa dokumentatsioon ja lähtekood                 |
| Töötuba 01 juhendid            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Praktiline töötuba: üks majutatud agent           |
| Töötuba 02 juhendid            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Praktiline töötuba: mitu-agendi töövoog            |
| Eeltingimuste kontrollnimekiri| [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Vajalikud tööriistad, kontod ja Azure ligipääs    |
| Hostitud agentide kiire alustamine (azd) | [Õpi](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Ametlik kiire juhend hostitud agendi juurutamiseks koos `azd` |
| Hostitud agentide piirkondade kättesaadavus | [Õpi](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Toetatud piirkonnad hostitud agentide jaoks (eelvaade)     |

### Koolitaja eeltingimused

Enne tarnimist veendu, et sul on:

- **Azure'i tellimus** koos ressursi loomise õigusega (omanik või kaastöötaja ressursigrupil).
- Juurdepääs **Microsoft Foundry projekti**le [regioonis, mis toetab hostitud agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Piirang **gpt-4.1** (või **gpt-4.1-mini**) jaoks teie Foundry projektis.
- Järgnevad tööriistad paigaldatud:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit laiendus](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Valikuline)
  - Python 3.12 või uuem

Käivitage [Hostitud agentide kiire käivitamine `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) vähemalt kord enne kohaletoimetamist, et teil oleks teada-tuntud töökorras Foundry projekt, mudeli juurutus ja Azure konteineriregister, millele viidata, kui õppija jääb toppama.

---

## Esitluse läbikäik

Esitlus järgib sama voogu nagu laborid. Soovitatud rääkimispunktid iga sektsiooni kohta:

| Sektsioon                    | Peamine sõnum                                                                                                 |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Pealkiri ja päevakord       | Raamige töötuba kui *VS Code kuni Foundry* ilma portaali vahetamiseta.                                       |
| Miks hostitud agendid?      | Hallatud käitusaeg, ACR-põhine juurutus, OpenAI-ga ühilduv `/responses` API, aheldatud Foundry projektidele.|
| Arhitektuuri diagramm       | Läbivaade [README arhitektuurist](../README.md#architecture): karkass, Inspector, ACR, Agent Service.           |
| Hostitud agenndi anatoomia   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - mida iga fail teeb.                              |
| Otseülekanne: Täidesaatev agent  | Vaheta VS Code’i ja käivita [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo algusest lõpuni (vaata [Demo 1](#demo-1-executive-agent)). |
| Otseülekanne: CV-st töö sobivuse hindajani | Vaheta VS Code’i ja käivita [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agendi demo (vaata [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 ülevaade                | Anna õppijatele. Osuta [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md) poole. |
| Mitme-agendi mustrid        | Järjestikune vs samaaegne vs üleandmine - eelvaade enne Lab 02 algust.                                           |
| Lab 02 ülevaade                | Anna õppijatele. Osuta [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md) poole. |
| Kokkuvõte ja ressursid       | Edasise õppimise lingid [Täiendavad ressursid](#additional-resources) sektsioonist.                      |

---

## Demod

Kättetoimetamisse kuulub kaks otseülekannet. Igaühele eralda 10 minutit.

| Demo | Labor | Failid | Mida näidata |
|------|-----|-------|--------------|
| Täidesaatev agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Üksik hostitud agent; tõlgenda tehnilisi termineid täidesaatvaks kokkuvõtteks |
| CV sobivuse hindaja tööle | Labor 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agendi orkestreerimine; skoori CV-töö sobivust ja genereeri soovitus |

### Demo 1: Juhtagent

Iseseisev agent [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Kasuta seda 10-minutilise demo jaoks enne Laborit 01.

1. Ava [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) ja tutvu agendi määratlusega (süsteemipäring, mudel, raamistik).
2. Vajuta `F5`, et käivitada **Agent Inspector** lokaalselt.
3. Kleebi proovitõuge [README](../README.md#see-it-in-action)-st ja näita tegevjuhi kokkuvõtte vastust.
4. Näita [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) ja [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile), et selgitada kasutuselevõtu artefakte.
5. Demonstreeri kasutuselevõtu voogu (Dockeri ehitus, ACR-i tõstmine, hostitud agendi loomine) ilma valmimist ootamata.

### Demo 2: CV sobivuse hindaja tööle

4-agendi töövoog [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Kasuta seda 10-minutilise demo jaoks enne Laborit 02.

1. Ava [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ja näita, kuidas neli agenti on järjestuslikult kokku ühendatud.
2. Vajuta `F5`, et käivitada **Agent Inspector** mitme agendi töövoo jaoks.
3. Kleepige lühike töökuulutuse kirjeldus ja näidisele resume Inspector'i vestlusesse.
4. Läbige nelja agendi torujuhe: CV parser, töö nõuete ekstraktor, sobivuse hindaja ja soovitus kirjutaja.
5. Näidake, kuidas iga alaagendi väljund saab järgmise agendi kontekstiks, rõhutades üleandmise mustrit.
6. Kuvage [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml), et võrrelda Demo 1 üheagendi vastavusega.

---

## Esitlussoovitused

- **Seadke ootused varakult.** Hostitud agendid on eelvaates – nimetage piirkonna piirangud ja kvoodi üle, et osalejad ei saaks labori keskel üllatust.
- **Käitage esmalt eeltingimuste ülesannet.** Mõlemad laboratorid sisaldavad `Validate prerequisites` VS Code ülesannet – laske osalejatel see enne koodi kirjutamist läbi teha.
- **Hoidke Agent Inspectorit nähtaval.** Enamik "ahha" hetki tekib, kui õppijad näevad kohalikku `/responses` tagasisidet.
- **Olge varuplaaniga projekt olemas.** Kui õppija Foundry projekt jõuab kvoodi piirini, jagage eelproovis valmis projekt juurutamisetapiks, et mitte takistada rühma.
- **Paigutage osalejad paari.** Labor 02 (mitme agendiga) on märgatavalt lihtsam, kui õppijad saavad koos orkestreerimist arutada.
- **Kasutage dokumentatsiooni mooduleid kontrollpunktidena.** Iga labori `docs/` kaust on jagatud nummerdatud mooduliteks – kasutage neid loomulike pauside tegemiseks.
- **Eeltõmmake põhidocker-pilt** jagatud laborimasinatel, et vältida registri kiiruspiiranguid.

---

## Tõrkeotsing esituse ajal

| Sümptom                                     | Esimene proovimine                                                                                         |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector ei saa ühendust               | Kinnitage, et port `8088` on vaba ja `Run Agent HTTP Server` ülesanne töötab.               |
| Silur ebaõnnestub külge kinnituma                     | Kontrollige, et port `5679` on vaba; taaskäivitage VS Code, kui `debugpy` on juba seotud.                           |
| `azd up` ebaõnnestub autentimisveaga               | Käivitage `az login` ja `azd auth login`, veenduge, et on valitud õige üürnik.                              |
| Deploy kinni jäänud ACR push juures                 | Kontrollige, et Docker Desktop töötab ja kasutajal on `AcrPush` registris.                              |
| Mudel tagastab 404 / deployment-not-found     | Mudeli paigutuse nimi `agent.yaml` peab vastama paigutusele Foundry projektis.              |
| Hostitud agent takerdunud `Provisioning`         | Kontrollige, et projekti piirkond [toetab hostitud agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ja et kohalik piirang on saadaval. |
| Playground tagastab 401                       | Autentige uuesti Foundry laiendus VS Code aktiivsusribalt.                                     |

Täiendava juhendamise jaoks saadab iga labor kaasa oma `08-troubleshooting.md` dokumendi - suunake õppijaid sinna:

- Labor 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Labor 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Selle sessiooni kohandamine

Võite töötoa kohandada oma publiku jaoks. Levinud variatsioonid:

- **Tagapõhja publikutel:** veetke rohkem aega `agent.yaml`, Dockeri ja ACR-i juures; kärpige playground demo.
- **Kodanike-arendajate sihtrühm:** jäädvustage Foundry laienduse kasutajaliideses skafoldimiseks; vähendage CLI samme.
- **Ühe rajaga 60-minutiline aeg:** esitage ainult sissejuhatus, demo ja labor 01.
- **Ainult töötuba (ilma slaidideta) formaat:** ava mõlemad õpitoa README-d ja kasuta neid peamise skriptina.

Kui laiendad õpitubasid, palun anna muudatused tagasi PR-i kaudu, et teised koolitajad saaksid kasu.

---

## Täiendavad allikad

- [Microsoft Foundry dokumentatsioon](https://learn.microsoft.com/azure/ai-foundry/)
- [Hostitud agendi ülevaade](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Kiirstart: juhi oma esimest hostitud agenti (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Hostitud agendi juurutamine (kuidas)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry tööriistade komplekt VS Code jaoks](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontaktid

Kui sul on küsimusi selle sessiooni läbiviimise kohta, palun ava probleem [töötoa hoidlasse](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) ja märgista hooldaja.

| Roll                | Nimi           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Hooldaja / kontakt  | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)               |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->