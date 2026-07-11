# Kaip pristatyti šią sesiją

Ačiū, kad pristatote šią sesiją!

Prieš pristatant dirbtuvę, prašome:

1. Perskaityti šį dokumentą ir visus įtrauktus išteklius iki galo.
2. Peržiūrėti sesijos pristatymo įrašą ir dirbtuvės perėjimą nuo pradžios iki pabaigos.
3. Viena ranka pereiti per abu praktinius laboratorinius darbus **bent vieną kartą** savo kompiuteryje prieš renginį.
4. Patikrinti savo Microsoft Foundry projektą, modelių diegimus ir kvotas.
5. Jei kas nors neaišku, kreiptis į atsakingą asmenį.

---

## Byla santrauka

| Ištekliai                    | Nuoroda                                                                         | Aprašymas                                                                                |
|-----------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Dirbtuvės skaidrių komplektas | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                  | Šios dirbtuvės pristatymo skaidrės su pranešėjo pastabomis ir įterptomis demo vaizdo įrašais|
| Sesijos pristatymo įrašas    | _Bus pateikta atsakingojo asmens_                                              | Dirbtuvių įžanga ir skaidrių perėjimo įrašas                                            |
| Dirbtuvių perėjimo įrašas    | _Bus pateikta atsakingojo asmens_                                              | Abu laboratoriniai darbai nuo pradžios iki pabaigos iš mokinio perspektyvos                 |
| Dirbtuvių dokumentacija     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Šaltinio repozitorija, laboratorijų README failai, žingsnis po žingsnio moduliai          |
| Laboratorija 01 – vienas agentas | [Lab 01](../workshop/lab01-single-agent/README.md)                             | Praktinis darbas: sukurti, išbandyti ir diegti *Explain Like I'm an Executive* talpinamą agentą |
| Laboratorija 02 – kelių agentų darbo eiga | [Lab 02](../workshop/lab02-multi-agent/README.md)                              | Praktinis darbas: sukurti 4-agentų *Resume to Job Fit Evaluator* darbo eigą              |
| Demo 1: Executive Agent      | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                            | Laboratorijos 01 demo: iš techninio žargono išversti į vykdomąją santrauką               |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)  | Laboratorijos 02 demo: 4 agentų darbo eiga, kuri vertina CV atitikimą darbui ir generuoja rekomendacijas |

> **Pastaba treneriams:** Skaidrių komplektas ir vaizdo įrašų nuorodos bus pridėtos, kai įrašai bus paskelbti. Iki tol kreipkitės į atsakingą asmenį (žr. [Kontaktai](#kontaktai)) dėl naujausių medžiagų.

---

## Pradėkime

Šios dirbtuvės moko kūrėjus, kaip sukurti, išbandyti ir diegti DI agentus į **Microsoft Foundry Agent Service** kaip **talpinamus agentus** visiškai iš VS Code, naudojant **Microsoft Foundry Toolkit** plėtinį.

Dirbtuvės suskirstytos į kelias dalis, įskaitant skaidres, **2 tiesioginius demo** ir **2 praktinius laboratorinius darbus**.

### Laiko planas

#### Pilnas pristatymas (apie 2 valandas)

| Laikas          | Aprašymas                                                     |
|----------------|--------------------------------------------------------------|
| 0:00 - 10:00   | Įvadas: talpinami agentai, Foundry Agent Service ir įrankių rinkinys |
| 10:00 - 20:00  | Demo: Executive Agent nuo pradžios iki galo                   |
| 20:00 - 60:00  | Laboratorija 01 - vienas agentas (sukurti, išbandyti lokaliai, diegti, žaidimų aikštelė) |
| 60:00 - 110:00 | Laboratorija 02 - kelių agentų darbo eiga (Resume to Job Fit Evaluator) |
| 110:00 - 120:00| Apibendrinimas, klausimai ir atsakymai, tolesnio mokymosi ištekliai |

#### Trumpas pristatymas (apie 75 minutes)

| Laikas          | Aprašymas                                            |
|-----------------|-----------------------------------------------------|
| 0:00 - 10:00    | Įvadas ir apžvalga                                 |
| 10:00 - 20:00   | Demo: Executive Agent                              |
| 20:00 - 70:00   | Tik laboratorija 01 (referuoti dalyviams Laboratoriją 02 kaip savarankišką) |
| 70:00 - 75:00   | Apibendrinimas ir klausimai                       |

### Paruošimas

| Ištekliai                     | Nuoroda                                                                              | Aprašymas                                         |
|------------------------------|---------------------------------------------------------------------------------------|--------------------------------------------------|
| Dirbtuvių dokumentacija      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)    | Dirbtuvių dokumentacija ir šaltiniai             |
| Laboratorijos 01 instrukcijos | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                        | Praktinis darbas: vienas talpinamas agentas       |
| Laboratorijos 02 instrukcijos | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                          | Praktinis darbas: kelių agentų darbo eiga         |
| Reikalavimų sąrašas           | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)        | Reikalingos priemonės, paskyros ir Azure prieiga  |
| Talpinamų agentų greitas pradėjimas (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Oficialus greitos pradžios vadovas talpinamų agentų diegimui naudojant `azd` |
| Talpinamų agentų regionų prieinamumas  | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Palaikomi regionai talpinamiems agentams (peržiūra) |

### Trenerio reikalavimai

Prieš pristatymą įsitikinkite, kad turite:

- **Azure prenumeratą** su teisėmis kurti išteklius (Savininkas arba Dalyvis išteklių grupėje).
- Prieigą prie **Microsoft Foundry projekto** regione, kuris palaiko talpinamus agentus ([žr. regionų prieinamumą](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)).
- Kvotą **gpt-4.1** (arba **gpt-4.1-mini**) savo Foundry projekte.
- Įdiegti šias priemones:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit plėtinį](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (neprivaloma)
  - Python 3.10 arba naujesnę versiją

Prieš pristatymą bent vieną kartą paleiskite [Talpinamų agentų greitą pradžią su `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd), kad turėtumėte patikrintą Foundry projektą, modelio diegimą ir Azure Container registro nuorodą, jei mokiniui prireiktų pagalbos.

---

## Skaidrių apžvalga

Skaidrių komplektas seka tą pačią eigą kaip laboratoriniai darbai. Siūlomi kalbėjimo punktai kiekvienai daliai:

| Dalies pavadinimas         | Pagrindinė žinutė                                                                                           |
|----------------------------|-------------------------------------------------------------------------------------------------------------|
| Pavadinimas ir darbotvarkė | Pristatykite dirbtuves kaip *VS Code į Foundry*, be vartotojo portalo perjungimo.                            |
| Kodėl talpinami agentai?   | Valdomas vykdymas, ACR pagrindu diegimas, OpenAI suderinamas `/responses` API, ribojamas Foundry projektams.   |
| Architektūros diagrama     | Pereikite per [README architektūrą](../README.md#architecture): karkasas, Inspector, ACR, Agentų paslauga.     |
| Talpinamo agento sandara   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` – ką daro kiekvienas failas.                         |
| Tiesioginis demonstravimas: Executive Agent  | Pereikite į VS Code ir paleiskite [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo nuo pradžios iki galo (žr. [Demo 1](#demo-1-executive-agent)). |
| Tiesioginis demonstravimas: Resume to Job Fit Evaluator | Pereikite į VS Code ir paleiskite [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agentų demo (žr. [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Laboratorija 01 santrauka | Pateikite mokiniams. Nukreipkite į [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Kelių agentų modeliai      | Nuoseklus, lygiagretus, perdavimo modelis – peržiūrėkite prieš pradedant Laboratoriją 02.                    |
| Laboratorija 02 santrauka | Pateikite mokiniams. Nukreipkite į [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Apibendrinimas ir ištekliai | Tolesnio mokymosi nuorodos iš skilties [Papildomi ištekliai](#papildomi-ištekliai).                          |

---

## Demonstracijos

Pristatymo metu yra įtrauktos dvi tiesioginės demonstracijos. Skirkite kiekvienai po 10 minučių.

| Demo                     | Laboratorija | Failai                                                                       | Ką demonstruoti                                    |
|--------------------------|--------------|-----------------------------------------------------------------------------|----------------------------------------------------|
| Executive Agent          | Laboratorija 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Vienas talpinamas agentas; versti techninį žargoną į vykdomąją santrauką |
| Resume to Job Fit Evaluator | Laboratorija 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agentų orkestracija; vertina CV-darbo atitikimą ir generuoja rekomendaciją|

### Demo 1: Executive Agent

Atskiras agentas [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Naudokite kaip 10 minučių demo prieš Laboratoriją 01.

1. Atidarykite [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) ir peržiūrėkite agento aprašymą (sistemos prievardis, modelis, karkasas).
2. Paspauskite `F5`, kad paleistumėte **Agentų Inspector** lokaliai.
3. Įklijuokite pavyzdinį prievardį iš [README](../README.md#see-it-in-action) ir parodykite vykdomosios santraukos atsakymą.
4. Parodykite [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) ir [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile), paaiškindami diegimo artefaktus.
5. Demonstruokite diegimo eigą (Docker build, ACR push, talpinamo agento kūrimas) nepalaukdami pabaigos.

### Demo 2: Resume to Job Fit Evaluator

4 agentų darbo eiga [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Naudokite kaip 10 minučių demo prieš Laboratoriją 02.

1. Atidarykite [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) ir parodykite, kaip keturi agentai jungiasi į nuoseklią orkestraciją.
2. Paspauskite `F5`, kad paleistumėte **Agentų Inspector** kelių agentų darbo eigai.
3. Inspector pokalbyje įklijuokite trumpą darbo aprašymą ir pavyzdinį CV.
4. Pereikite per keturių agentų procesą: CV analizatorius, darbo reikalavimų išskinėtojas, tinkamumo vertintojas ir rekomendacijų rašytojas.
5. Pabrėžkite, kaip kiekvieno sub-agento išvestis tampa kito agento kontekstu, akcentuodami perdavimo modelį.
6. Parodykite [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) ir palyginkite su vieno agente aprašymu Debo 1.

---

## Pristatymo patarimai

- **Nustatykite lūkesčius iš anksto.** Talpinami agentai yra peržiūros režime – iškart nurodykite regionų apribojimus ir kvotas, kad dalyviai nebūtų nustebinti per laboratorinį darbą.
- **Pirmiausia paleiskite reikalavimų tikrinimo užduotį.** Abu laboratoriniai darbai turi `Validate prerequisites` VS Code užduotį – prašykite dalyvių ją paleisti prieš rašant bet kokį kodą.
- **Išlaikykite Agentų Inspector matomą.** Dauguma „aha“ momentų įvyksta tuomet, kai mokiniai mato, kaip vietinis `/responses` ryšys sušvinta.
- **Turėkite atsarginį projektą.** Jei mokinio Foundry projektas pasieks kvotų ribą, suteikite paruoštą projektą diegimo žingsniui, kad neužstrigtų visa grupė.
- **Sujunkite dalyvius poromis.** Laboratorija 02 (kelių agentų) yra žymiai lengvesnė, kai mokiniai gali aptarti orkestraciją su partneriu.
- **Naudokite dokumentacijos modulius kaip patikros taškus.** Kiekvienos laboratorijos `docs/` aplankas suskirstytas į 8 numeruotus modulius – naudokite juos kaip natūralias pertraukėles.
- **Iš anksto parsisiųskite bazinį Docker vaizdą** bendroms laboratorinėms mašinoms, kad išvengtumėte registro dažnio apribojimų.

---

## Problemos sprendimas pristatymo metu

| Simptomas                                    | Pirmas veiksmas, kurį reikia pabandyti                                                               |
|----------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Agentų Inspector negali prisijungti          | Patikrinkite, ar laisvas prievadas `8088` ir ar veikia užduotis `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server`. |
| Debugeris nepavyksta prijungti                | Patikrinkite, ar laisvas prievadas `5679`; jei `debugpy` jau išnaudotas, paleiskite VS Code iš naujo.  |
| `azd up` nepavyksta dėl autentifikacijos klaidos | Paleiskite `az login` ir `azd auth login`, įsitikinkite, kad pasirinktas teisingas nuomininkas.         |
| Diegimas stringa ACR skelbimo metu             | Patikrinkite, ar veikia Docker Desktop ir ar naudotojas turi `AcrPush` teisę registre.                 |
| Modelis grąžina 404 / diegimas nerastas        | Modelio diegimo pavadinimas faile `agent.yaml` turi atitikti diegimą Foundry projekte.                 |

| Talpinamas agentas įstringa `Provisioning` stadijoje         | Patikrinkite, ar projekto regionas [palaiko talpinamus agentus](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ir ar yra prieinamas kvotas. |
| Žaidimų aikštelė grąžina 401                       | Iš naujo autentifikuokite Foundry plėtinį iš VS Code veiklos juostos.                                     |

Dėl išsamesnių nurodymų kiekvienas laboratorijos darbas turi savo `08-troubleshooting.md` dokumentą – nukreipkite mokinius ten:

- Laboratorija 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Laboratorija 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Šios sesijos suaspinimas

Kviečiame pritaikyti dirbtuves savo auditorijai. Dažnos variacijos:

- **Backend auditorijos:** skirkite daugiau laiko `agent.yaml`, Docker ir ACR; sutrumpinkite žaidimų aikštelės demonstraciją.
- **Piliečių kūrėjų auditorijos:** likite Foundry plėtinio sąsajoje skafoldingui; sumažinkite CLI veiksmų skaičių.
- **Vienos sesijos 60 minučių laikas:** pateikite tik įvadas, demonstruokite ir laboratoriją 01.
- **Tik dirbtuvės (be skaidrių) formatas:** atidarykite abiejų laboratorijų READMEs ir naudokite juos kaip pagrindinį scenarijų.

Jei praplėsite laboratorijas, prašome pateikti pakeitimus per PR, kad kiti treniruotojai galėtų pasinaudoti.

---

## Papildomi ištekliai

- [Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/ai-foundry/)
- [Talpinamų agentų apžvalga](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Greitasis pradžios vadovas: įdiekite pirmą talpinamą agentą (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Kaip įdiegti talpinamą agentą (instrukcijos)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry įrankių rinkinys VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontaktai

Jei turite klausimų apie šios sesijos vedimą, prašome atidaryti problemą [dirbtuvių saugykloje](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) ir pažymėti atsakingą asmenį.

| Vaidmuo                | Vardas           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Atsakingas/ kontaktas| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->