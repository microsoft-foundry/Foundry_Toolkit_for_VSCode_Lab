# Hvordan levere denne sesjonen

Takk for at du leverer denne sesjonen!

Før du leverer workshoppen, vennligst:

1. Les dette dokumentet og alle inkluderte ressurser i sin helhet.
2. Se gjennom økten sin leveringsopptak og workshopens ende-til-ende gjennomgang.
3. Gå gjennom begge praktiske laboratoriene ende-til-ende på din egen maskin **minst én gang** før arrangementet.
4. Valider ditt Microsoft Foundry-prosjekt, modellutplasseringer og kvoter.
5. Ta kontakt med vedlikeholderen dersom noe er uklart.

---

## Filoversikt

| Ressurs                      | Lenke                                                                             | Beskrivelse                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop slide deck           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Presentasjonsbilder for denne workshoppen med presentatørnotater og innebygde demovideoer   |
| Økt sitt leveringsopptak    | _Skal leveres av vedlikeholderen_                                               | Workshop-intro og gjennomgang av lysbilder opptak                                           |
| Workshop ende-til-ende opptak | _Skal leveres av vedlikeholderen_                                               | Ende-til-ende opptak av begge laboratorier fra en lærers perspektiv                         |
| Workshop dokumentasjon        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Kildearkiv, lab README-filer, trinn-for-trinn moduler                                      |
| Lab 01 - enkeltagent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Praktisk lab: bygg, test og deployer *Explain Like I'm an Executive* hostet agent           |
| Lab 02 - fleragent arbeidsflyt | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Praktisk lab: bygg 4-agent *Resume to Job Fit Evaluator* arbeidsflyt                       |
| Demo 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Lab 01 demo: oversett teknisk sjargong til en lederoppsummering                            |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Lab 02 demo: 4-agent arbeidsflyt som vurderer resume-job matching og genererer anbefalinger |

> **Merk for trenere:** Slides og videolenker vil legges til så snart opptakene er publisert. Inntil da, ta kontakt med vedlikeholder (se [Kontakter](#kontakter)) for de siste ressursene.

---

## Kom i gang

Denne workshoppen lærer utviklere hvordan de kan bygge, teste og deployere AI-agenter til **Microsoft Foundry Agent Service** som **Hosted Agents** helt fra VS Code, ved å bruke **Microsoft Foundry Toolkit**-utvidelsen.

Workshoppen er delt inn i flere seksjoner inkludert lysbilder, **2 live demoer**, og **2 praktiske laboratorier**.

### Tidsskjema

#### Full levering (omtrent 2 timer)

| Tid             | Beskrivelse                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Intro: hosted agents, Foundry Agent Service og toolkit                |
| 10:00 - 20:00   | Demo: Executive Agent ende-til-ende                                 |
| 20:00 - 60:00   | Lab 01 - enkeltagent (bygg, lokal test, deploy, lekeområde)          |
| 60:00 - 110:00  | Lab 02 - fleragent arbeidsflyt (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00 | Oppsummering, spørsmål & svar og videre læringsressurser             |

#### Kort levering (omtrent 75 minutter)

| Tid          | Beskrivelse                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Intro og oversikt                                           |
| 10:00 - 20:00 | Demo: Executive Agent                                        |
| 20:00 - 70:00 | Kun Lab 01 (peke deltakere til Lab 02 som selvstudium)        |
| 70:00 - 75:00 | Oppsummering og spørsmål & svar                              |

### Forberedelse

| Ressurs                       | Lenke                                                                                          | Beskrivelse                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Workshop dokumentasjon         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Workshop dokumentasjon og kilde                    |
| Lab 01 instruksjoner            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Praktisk lab: enkelt hostet agent                  |
| Lab 02 instruksjoner            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Praktisk lab: fleragent arbeidsflyt                 |
| Forutsetningssjekkliste        | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Verktøy, kontoer og tilgang til Azure som kreves  |
| Hurtigstart Hosted agents (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Offisiell hurtigstart for å distribuere en hosted agent med `azd` |
| Tilgjengelighet av hosted agents regioner | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Støttede regioner for hosted agents (preview)     |

### Treningsforutsetninger

Før du leverer, sørg for at du har:

- Et **Azure-abonnement** med tillatelse til å opprette ressurser (Owner eller Contributor på en ressursgruppe).
- Tilgang til et **Microsoft Foundry-prosjekt** i en [region som støtter hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvote for **gpt-4.1** (eller **gpt-4.1-mini**) i ditt Foundry-prosjekt.
- Følgende verktøy installert:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit-utvidelsen](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (valgfritt)
  - Python 3.10 eller nyere

Kjør [Hosted agents hurtigstart med `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) minst én gang før levering slik at du har et kjent-godt Foundry-prosjekt, modellutplassering, og Azure Container Registry å referere til hvis en deltaker skulle stå fast.

---

## Gjennomgang av slides

Lysbildene følger samme flyt som laboratoriene. Foreslåtte samtalepunkter for hver seksjon:

| Seksjon                     | Hovedbudskap                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Tittel og agenda            | Rammeverk workshoppen som *VS Code til Foundry* uten behov for å bytte portal.                               |
| Hvorfor hosted agents?      | Administrert runtime, ACR-basert deploy, OpenAI-kompatibel `/responses` API, avgrenset til Foundry-prosjekter.  |
| Arkitekturdiagram          | Gå gjennom [README arkitekturen](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.         |
| Anatomi av en hosted agent | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - hva hver fil gjør.                                |
| Live demo: Executive Agent  | Bytt til VS Code og kjør demoen [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) ende-til-ende (se [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Bytt til VS Code og kjør [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo (se [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 kort                 | Overlever til deltakerne. Peker til [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Multi-agent mønstre         | Sekvensiell vs parallell vs overlevering - forhåndsvis før Lab 02 starter.                                   |
| Lab 02 kort                 | Overlever til deltakerne. Peker til [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Oppsummering og ressurser   | Videre læringslenker fra [Tilleggsressurser](#tilleggsressurser) seksjonen.                              |

---

## Demoer

To live demoer er inkludert i leveringen. Sett av 10 minutter til hver.

| Demo | Lab | Filer | Hva å vise |
|------|-----|-------|--------------|
| Executive Agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Enkelt hostet agent; oversett teknisk sjargong til en lederoppsummering |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orkestrering; vurder resume-job matching og generer anbefaling |

### Demo 1: Executive Agent

En frittstående agent i [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Bruk denne som en 10-minutters demo før Lab 01.

1. Åpne [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) og gå gjennom agent-definisjonen (system prompt, modell, rammeverk).
2. Trykk `F5` for å starte **Agent Inspector** lokalt.
3. Lim inn eksempelprompten fra [README](../README.md#see-it-in-action) og vis oppsummeringssvar for leder.
4. Vis [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) og [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) for å forklare distribusjonsartefaktene.
5. Demonstrer deploy-flyten (Docker build, ACR push, hosted agent create) uten å vente på fullføring.

### Demo 2: Resume to Job Fit Evaluator

En arbeidsflyt med 4 agenter i [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Bruk denne som en 10-minutters demo før Lab 02.

1. Åpne [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) og vis hvordan de fire agentene er koblet sammen i en sekvensiell orkestrering.
2. Trykk `F5` for å starte **Agent Inspector** for fler-agent arbeidsflyten.
3. Lim inn en kort stillingsbeskrivelse og et eksempel på CV i Inspector chatten.
4. Gå gjennom fire-agent pipeline: CV-parser, jobbkrav-uttrekker, matchingsvurderer og anbefalingsskriver.
5. Pek ut hvordan hver sub-agent sitt output blir neste agents kontekst, fremhev overleveringsmønsteret.
6. Vis [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) for å sammenligne med enkel-agent-ekvivalenten fra Demo 1.

---

## Leveringstips

- **Sett forventninger tidlig.** Hosted agents er i preview - påpek regionsbegrensninger og kvoter på forhånd slik at deltakerne ikke blir overrasket midt i laben.
- **Kjør forutsetningsoppgaven først.** Begge labene har en `Validate prerequisites` VS Code-oppgave - la deltakerne kjøre den før det skrives kode.
- **Hold Agent Inspector synlig.** De fleste "aha"-øyeblikk skjer når deltakerne ser lokal `/responses` tur-retur blinke.
- **Ha et reserveprosjekt.** Hvis en deltakers Foundry-prosjekt treffer kvotebegrensning, del et ferdig oppsatt prosjekt for deploy-steget istedenfor å blokkere rommet.
- **Parvis deltakere.** Lab 02 (fleragent) er betydelig enklere når deltakerne kan snakke gjennom orkestreringen med en partner.
- **Bruk dokumentasjonsmoduler som sjekkpunkter.** Hver labs `docs/`-mappe er delt i 8 nummererte moduler - bruk disse som naturlige pausesteder.
- **Forhåndstrekk basis Docker-image** på delte labmaskiner for å unngå rate limits i registeret.

---

## Feilsøking under levering

| Symptom                                      | Første forsøk på løsning                                                                                |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector kan ikke koble til           | Bekreft at port `8088` er ledig og at `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` oppgaven kjører. |
| Feilsøker klarer ikke å koble til             | Sjekk at port `5679` er ledig; restart VS Code hvis `debugpy` allerede er bundet.                        |
| `azd up` feiler med autentiseringsfeil       | Kjør `az login` og `azd auth login`, sørg for at riktig leietaker er valgt.                             |
| Deploy henger ved ACR push                      | Sjekk at Docker Desktop kjører og at brukeren har `AcrPush` på registeret.                             |
| Modell returnerer 404 / deployment-not-found  | Modellutplasseringens navn i `agent.yaml` må samsvare med deploy i Foundry-prosjektet.                  |

| Vert agent sitter fast i `Provisioning`         | Verifiser at prosjektregionen [støtter vertede agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) og at kvoten er tilgjengelig. |
| Playground returnerer 401                       | Autentiser Foundry-utvidelsen på nytt fra VS Code-aktivitetslinjen.                                     |

For dypere veiledning leveres hver lab med sin egen `08-troubleshooting.md`-fil - lenk deltakere dit:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Tilpasse denne økten

Du er velkommen til å tilpasse workshoppen for ditt publikum. Vanlige variasjoner:

- **Backend-publikum:** bruk mer tid på `agent.yaml`, Docker og ACR; forkort playground-demoen.
- **Citizen-developer-publikum:** bli i Foundry-utvidelsens brukergrensesnitt for oppsett; reduser CLI-trinn.
- **Enkel 60-minutters sesjon:** gjennomfør kun introduksjon, demo og Lab 01.
- **Kun workshop (ingen lysbilder)-format:** åpne begge lab-README-ene og bruk dem som hovedmanus.

Hvis du utvider labene, vennligst bidra med endringene via PR slik at andre trenere kan dra nytte av dem.

---

## Tilleggsressurser

- [Microsoft Foundry-dokumentasjon](https://learn.microsoft.com/azure/ai-foundry/)
- [Oversikt over vertede agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Rask start: distribuer din første vertede agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Distribuer en vertet agent (hvordan)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakter

Hvis du har spørsmål om gjennomføringen av denne økten, vennligst åpne en sak i [workshop-repositoriet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) og merk vedlikeholderen.

| Rolle                | Navn           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Vedlikeholder / kontakt| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->