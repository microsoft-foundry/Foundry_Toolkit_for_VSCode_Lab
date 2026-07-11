# Hoe deze sessie te geven

Bedankt dat je deze sessie geeft!

Voordat je de workshop geeft, gelieve:

1. Dit document en alle bijbehorende bronnen volledig door te lezen.
2. De opname van de sessie en de volledige walkthrough van de workshop te bekijken.
3. Beide hands-on labs minimaal één keer volledig door te lopen op je eigen machine vóór het evenement.
4. Je Microsoft Foundry-project, modeldeployments en quota te valideren.
5. Contact op te nemen met de beheerder als er iets onduidelijk is.

---

## Bestandssamenvatting

| Bron                        | Link                                                                             | Beschrijving                                                                             |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop slide deck           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Presentatieslides voor deze workshop met presentatornotities en ingesloten demovideo's    |
| Opname van sessie            | _Wordt aangeleverd door de beheerder_                                               | Workshop introductie en slide walkthrough opname                                        |
| Volledige workshop opname    | _Wordt aangeleverd door de beheerder_                                               | Volledige opname van beide labs vanuit het perspectief van een deelnemer                 |
| Workshopdocumentatie         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Bronrepository, lab READMEs, stapsgewijze modules                                       |
| Lab 01 - enkele agent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Hands-on lab: bouw, test en deployeer de *Explain Like I'm an Executive* gehoste agent    |
| Lab 02 - multi-agent workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Hands-on lab: bouw de 4-agent *Resume to Job Fit Evaluator* workflow                      |
| Demo 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Lab 01 demo: vertaal technische jargon naar een executive samenvatting                   |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Lab 02 demo: 4-agent workflow die cv-positie fit beoordeelt en aanbevelingen genereert    |

> **Opmerking voor trainers:** De slide deck en videolinks worden toegevoegd zodra de opnames zijn gepubliceerd. Tot die tijd kun je contact opnemen met de beheerder (zie [Contacten](#contacten)) voor de meest recente materialen.

---

## Aan de slag

Deze workshop leert ontwikkelaars hoe ze AI-agents kunnen bouwen, testen en inzetten naar **Microsoft Foundry Agent Service** als **Hosted Agents** volledig vanuit VS Code, met behulp van de **Microsoft Foundry Toolkit** extensie.

De workshop is opgedeeld in meerdere secties waaronder slides, **2 live demo’s**, en **2 hands-on labs**.

### Tijdsplanning

#### Volledige sessie (ongeveer 2 uur)

| Tijd            | Beschrijving                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Intro: hosted agents, Foundry Agent Service, en de toolkit            |
| 10:00 - 20:00   | Demo: Executive Agent van begin tot eind                              |
| 20:00 - 60:00   | Lab 01 - enkele agent (bouwen, lokaal testen, deployen, playground)   |
| 60:00 - 110:00  | Lab 02 - multi-agent workflow (Resume to Job Fit Evaluator)           |
| 110:00 - 120:00 | Afronding, Q&A, en bronnen voor verder leren                          |

#### Korte sessie (ongeveer 75 minuten)

| Tijd          | Beschrijving                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Intro en overzicht                                            |
| 10:00 - 20:00 | Demo: Executive Agent                                         |
| 20:00 - 70:00 | Alleen Lab 01 (deelnemers wijzen op Lab 02 als zelfstudie)   |
| 70:00 - 75:00 | Afronding en Q&A                                             |

### Voorbereiding

| Bron                          | Link                                                                                          | Beschrijving                                     |
|-------------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------|
| Workshopdocumentatie          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Workshopdocumentatie en broncode                  |
| Lab 01 instructies           | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Hands-on lab: enkele gehoste agent                |
| Lab 02 instructies           | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Hands-on lab: multi-agent workflow                 |
| Checklist vereisten           | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Vereiste tools, accounts en Azure-toegang          |
| Hosted agents quickstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Officiële quickstart voor het uitrollen van een hosted agent met `azd` |
| Beschikbaarheid hosted agents regio | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Ondersteunde regio’s voor hosted agents (preview)  |

### Voorwaarden voor trainers

Zorg er voor dat je vóór de sessie:

- Een **Azure-abonnement** hebt met toestemming om resources te maken (Eigenaar of Medewerker op een resourcegroep).
- Toegang hebt tot een **Microsoft Foundry-project** in een [regio die hosted agents ondersteunt](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota hebt voor **gpt-4.1** (of **gpt-4.1-mini**) in je Foundry-project.
- De volgende tools geïnstalleerd hebt:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit-extensie](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (optioneel)
  - Python 3.10 of later

Draai de [Hosted agents quickstart met `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) minstens één keer vóór de sessie, zodat je een bekend goed Foundry-project, modeldeployment en Azure Container Registry hebt om op terug te vallen als een deelnemer vastloopt.

---

## Slide walkthrough

De slides volgen dezelfde opbouw als de labs. Voorgestelde gesprekspunten per sectie:

| Sectie                      | Kernboodschap                                                                                              |
|-----------------------------|-----------------------------------------------------------------------------------------------------------|
| Titel en agenda             | Kader de workshop als *VS Code naar Foundry* zonder te wisselen tussen portals.                           |
| Waarom hosted agents?       | Beheerde runtime, ACR-gebaseerde deployment, OpenAI-compatibele `/responses` API, gebonden aan Foundry-projecten. |
| Architectuur diagram        | Loop de [README architectuur](../README.md#architecture) door: scaffold, Inspector, ACR, Agent Service.    |
| Anatomie van een hosted agent | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - wat doet elk bestand.                         |
| Live demo: Executive Agent  | Wissel naar VS Code en voer de [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo volledig uit (zie [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Wissel naar VS Code en voer de [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo uit (zie [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 overzicht            | Geef aan de deelnemers over. Verwijs naar [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Multi-agent patronen         | Sequentieel vs gelijktijdig vs overdracht - kort bespreken voor start Lab 02.                             |
| Lab 02 overzicht            | Geef aan de deelnemers over. Verwijs naar [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Afronding en bronnen        | Links voor verder leren uit de sectie [Aanvullende bronnen](#aanvullende-bronnen).                       |

---

## Demo’s

Er zijn twee live demo’s opgenomen in de sessie. Reserveer 10 minuten voor elk.

| Demo | Lab | Bestanden | Wat te tonen |
|------|-----|----------|--------------|
| Executive Agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Enkele gehoste agent; vertaal technische jargon naar een executive samenvatting |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orkestratie; beoordeel cv-positie fit en genereer aanbeveling |

### Demo 1: Executive Agent

Een zelfstandige agent in [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Gebruik dit als een 10-minuten durende demo vóór Lab 01.

1. Open [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) en loop door de agentdefinitie (systeem prompt, model, framework).
2. Druk op `F5` om de **Agent Inspector** lokaal te starten.
3. Plak de voorbeeldprompt uit de [README](../README.md#see-it-in-action) en toon de executive-summary respons.
4. Toon [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) en [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) om de deployment artefacten uit te leggen.
5. Demonstreer de deployment flow (Docker build, ACR push, hosted agent create) zonder op de voltooiing te wachten.

### Demo 2: Resume to Job Fit Evaluator

Een 4-agent workflow in [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Gebruik dit als een 10-minuten durende demo vóór Lab 02.

1. Open [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) en laat zien hoe de vier agents achtereenvolgens met elkaar verbonden zijn in een sequentiële orkestratie.
2. Druk op `F5` om de **Agent Inspector** voor de multi-agent workflow te starten.
3. Plak een korte functiebeschrijving en een voorbeeld-cv in de Inspector chat.
4. Loop door de vier-agent pipeline: resume parser, job requirement extractor, fit scorer, en recommendation writer.
5. Benadruk hoe de output van elke sub-agent de context wordt voor de volgende agent, en licht het overdrachtspatroon toe.
6. Toon [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) om te vergelijken met de enkele agent uit Demo 1.

---

## Tips voor het geven

- **Stel verwachtingen vroeg duidelijk.** Hosted agents zijn in preview – wijs op regiobeperkingen en quota zodat deelnemers niet tijdens het lab verrast worden.
- **Laat eerst de vereisten-check uitvoeren.** Beide labs bevatten een `Validate prerequisites` VS Code taak – laat deelnemers deze uitvoeren voordat ze code schrijven.
- **Houd de Agent Inspector zichtbaar.** De meeste “aha” momenten ontstaan wanneer deelnemers de lokale `/responses` round-trip zien oplichten.
- **Heb een back-up project klaar.** Als het Foundry-project van een deelnemer de quota overschrijdt, deel dan een vooraf geprovisioneerd project voor de deployment stap om blokkering te voorkomen.
- **Werk in duo’s.** Lab 02 (multi-agent) is aanmerkelijk eenvoudiger wanneer deelnemers de orkestratie kunnen bespreken met een partner.
- **Gebruik de docs modules als stopmomenten.** De `docs/` map van elk lab is verdeeld in 8 genummerde modules – gebruik deze natuurlijke pauzepunten.
- **Download vooraf de basis Docker-image** op gedeelde labmachines om limieten van de registry te vermijden.

---

## Problemen oplossen tijdens de sessie

| Symptom                                      | Eerste actie                                                                                         |
|----------------------------------------------|----------------------------------------------------------------------------------------------------|
| Agent Inspector kan niet verbinden            | Controleer of poort `8088` vrij is en of de taak `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` actief is. |
| Debugger kan niet binden                       | Controleer of poort `5679` vrij is; herstart VS Code als `debugpy` al gebonden is.                  |
| `azd up` faalt met authenticatiefout          | Voer `az login` en `azd auth login` uit, zorg dat de juiste tenant is geselecteerd.                 |
| Deployment blijft hangen bij ACR push          | Controleer of Docker Desktop draait en de gebruiker `AcrPush` rechten heeft op de registry.        |
| Model geeft 404 / deployment-niet-gevonden     | De model deploymentnaam in `agent.yaml` moet overeenkomen met die in het Foundry-project.          |

| Gehoste agent blijft hangen in `Provisioning`         | Controleer of de projectregio [gehoste agents ondersteunt](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) en dat er quota beschikbaar is. |
| Playground geeft 401 terug                       | Authenticeer de Foundry-extensie opnieuw via de VS Code-activiteitenbalk.                                     |

Voor diepgaandere begeleiding levert elke lab zijn eigen `08-troubleshooting.md` document - link deelnemers daarheen:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Deze sessie aanpassen

Je bent vrij om de workshop aan te passen voor je publiek. Veelvoorkomende varianten:

- **Backend-publiek:** besteed meer tijd aan `agent.yaml`, Docker en ACR; verkort de playground-demo.
- **Citizen-developer-publiek:** blijf in de Foundry-extensie UI voor scaffolding; verminder de CLI-stappen.
- **Enkelvoudige 60-minuten sessie:** geef alleen intro, demo en Lab 01.
- **Alleen workshop (geen slides) formaat:** open beide lab READMEs en gebruik deze als het primaire script.

Als je de labs uitbreidt, draag dan de wijzigingen terug bij via een PR zodat andere trainers er profijt van hebben.

---

## Aanvullende bronnen

- [Microsoft Foundry documentatie](https://learn.microsoft.com/azure/ai-foundry/)
- [Overzicht gehoste agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Quickstart: zet je eerste gehoste agent uit (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Gehoste agent uitrollen (how-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit voor VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contacten

Als je vragen hebt over het geven van deze sessie, open dan een issue in de [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) en tag de maintainer.

| Rol                 | Naam           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Onderhouder / contact| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->