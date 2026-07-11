# Hvordan man leverer denne session

Tak for at du leverer denne session!

Inden du leverer workshoppen, bedes du:

1. Læse dette dokument og alle inkluderede ressourcer i deres helhed.
2. Se optagelsen af sessionsleveringen og gennemgangen af workshoppen fra ende til anden.
3. Gennemføre begge hands-on laboratorier fra ende til anden på din egen maskine **mindst én gang** inden arrangementet.
4. Validere dit Microsoft Foundry-projekt, modeludrulninger og kvoter.
5. Kontakte vedligeholderen, hvis noget er uklart.

---

## Filoversigt

| Ressource                    | Link                                                                             | Beskrivelse                                                                             |
|-----------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Workshop slide deck           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Præsentationsslides til denne workshop med præsentatørnoter og indlejrede demo-videoer   |
| Optagelse af sessionslevering | _Udleveres af vedligeholderen_                                               | Workshop-intro og gennemgang af slides optagelse                                        |
| Workshop end-to-end optagelse | _Udleveres af vedligeholderen_                                               | End-to-end optagelse af begge laboratorier fra en lærendes perspektiv                   |
| Workshop dokumentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Kilderepository, lab README-filer, trin-for-trin moduler                                |
| Lab 01 - enkelt agent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Hands-on laboratorium: byg, test og udrul *Explain Like I'm an Executive* hosted agent   |
| Lab 02 - multi-agent workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Hands-on laboratorium: byg 4-agent *Resume to Job Fit Evaluator* workflow                |
| Demo 1: Executive Agent       | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                             | Lab 01 demo: oversæt teknisk jargon til et ledelsessammendrag                           |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)  | Lab 02 demo: 4-agent workflow som scorer resume-job fit og genererer anbefalinger       |

> **Note til trænere:** Slide deck og videolinks tilføjes, når optagelserne er offentliggjort. Indtil da, kontakt vedligeholderen (se [Kontakter](#kontakter)) for de nyeste materialer.

---

## Kom godt i gang

Denne workshop lærer udviklere at bygge, teste og udrulle AI-agenter til **Microsoft Foundry Agent Service** som **Hosted Agents** fuldstændigt fra VS Code ved hjælp af **Microsoft Foundry Toolkit** udvidelsen.

Workshoppen er opdelt i flere sektioner inklusive slides, **2 live-demoer** og **2 hands-on laboratorier**.

### Tidspunkt

#### Fuld levering (ca. 2 timer)

| Tid             | Beskrivelse                                                           |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Intro: hosted agents, Foundry Agent Service og toolkit               |
| 10:00 - 20:00   | Demo: Executive Agent fra ende til anden                             |
| 20:00 - 60:00   | Lab 01 - enkelt agent (byg, test lokalt, udrul, playground)           |
| 60:00 - 110:00  | Lab 02 - multi-agent workflow (Resume to Job Fit Evaluator)          |
| 110:00 - 120:00 | Opsummering, Q&A og ressourcer til fortsat læring                   |

#### Kort levering (ca. 75 minutter)

| Tid          | Beskrivelse                                                    |
|--------------|----------------------------------------------------------------|
| 0:00 - 10:00 | Intro og oversigt                                             |
| 10:00 - 20:00| Demo: Executive Agent                                         |
| 20:00 - 70:00| Kun Lab 01 (henvis deltagere til Lab 02 som selvstudie)      |
| 70:00 - 75:00| Opsummering og Q&A                                           |

### Forberedelse

| Ressource                       | Link                                                                                          | Beskrivelse                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Workshop dokumentation          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Workshop dokumentation og kildekode                |
| Lab 01 instruktioner            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Hands-on laboratorium: enkelt hosted agent          |
| Lab 02 instruktioner            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Hands-on laboratorium: multi-agent workflow         |
| Præ-krav tjekliste             | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Nødvendige værktøjer, konti og Azure-adgang          |
| Hosted agents quickstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Officiel quickstart til udrulning af hosted agent med `azd` |
| Hosted agents region tilgængelighed | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Understøttede regioner for hosted agents (preview)   |

### Træner forudsætninger

Før du leverer, skal du sikre dig, at du har:

- Et **Azure-abonnement** med tilladelse til at oprette ressourcer (Owner eller Contributor på en ressourcegruppe).
- Adgang til et **Microsoft Foundry-projekt** i en [region, der understøtter hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvote til **gpt-4.1** (eller **gpt-4.1-mini**) i dit Foundry-projekt.
- Følgende værktøjer installeret:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit udvidelse](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (valgfrit)
  - Python 3.10 eller nyere

Kør [Hosted agents quickstart med `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) mindst én gang før levering, så du har et kendt godt Foundry-projekt, modeludrulning og Azure Container Registry at referere til, hvis en deltager sidder fast.

---

## Slide-gennemgang

Dækket følger samme flow som laboratorierne. Foreslåede samtalepunkter for hver sektion:

| Sektion                      | Nøglebudskab                                                                                                |
|-----------------------------|------------------------------------------------------------------------------------------------------------|
| Titel og agenda              | Indram workshoppen som *VS Code til Foundry* uden behov for portal-skift.                                 |
| Hvorfor hosted agents?       | Administreret runtime, ACR-baseret udrulning, OpenAI-kompatibel `/responses` API, scoped til Foundry-projekter. |
| Arkitektur diagram          | Gennemgå [README arkitektur](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.            |
| Anatomi af en hosted agent   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - hvad hver fil gør.                              |
| Live demo: Executive Agent   | Skift til VS Code og kør [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo fra ende til anden (se [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Skift til VS Code og kør [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo (se [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 kort                  | Overdrag til deltagerne. Henvis til [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Multi-agent mønstre         | Sekventiel vs samtidig vs overlevering - forhåndsvis inden Lab 02 starter.                                  |
| Lab 02 kort                  | Overdrag til deltagerne. Henvis til [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Opsummering og ressourcer    | Links til fortsat læring fra [Yderligere ressourcer](#yderligere-ressourcer) sektionen.                      |

---

## Demoer

To live-demoer er inkluderet i leveringen. Afsæt 10 minutter til hver.

| Demo | Lab | Filer | Hvad der vises |
|------|-----|-------|----------------|
| Executive Agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Enkel hosted agent; oversæt teknisk jargon til et ledelsessammendrag |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orkestrering; vurder resume-job fit og generer en anbefaling |

### Demo 1: Executive Agent

En enkeltstående agent i [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Brug denne som en 10-minutters demo før Lab 01.

1. Åbn [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) og gennemgå agentdefinitionen (systemprompt, model, framework).
2. Tryk `F5` for at starte **Agent Inspector** lokalt.
3. Indsæt eksempelprompten fra [README](../README.md#see-it-in-action) og vis executive-summary svaret.
4. Vis [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) og [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) for at forklare udrulningsartefakterne.
5. Demonstrer udrulningsflowet (Docker build, ACR push, hosted agent oprettelse) uden at vente på færdiggørelse.

### Demo 2: Resume to Job Fit Evaluator

En 4-agent workflow i [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Brug denne som en 10-minutters demo før Lab 02.

1. Åbn [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) og vis, hvordan de fire agenter er forbundet i en sekventiel orkestrering.
2. Tryk `F5` for at starte **Agent Inspector** for multi-agent workflowet.
3. Indsæt en kort jobbeskrivelse og et eksempel på et CV i Inspector chatten.
4. Gå igennem fire-agent pipeline: CV-parser, jobkrav-ekstraktor, fit scorer og anbefalingsforfatter.
5. Peg på, hvordan hver sub-agent's output bliver næste agents kontekst, og fremhæv overleveringsmønsteret.
6. Vis [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) for at sammenligne med enkelt-agent ekvivalent fra Demo 1.

---

## Leveringstips

- **Sæt forventninger tidligt.** Hosted agents er i preview - gør opmærksom på regionbegrænsninger og kvoter fra starten, så deltagerne ikke bliver overraskede midt i laboratoriet.
- **Kør præ-krav opgaven først.** Begge laboratorier indeholder en `Validate prerequisites` VS Code opgave - lad deltagerne køre den, før der skrives kode.
- **Hold Agent Inspector synlig.** De fleste "aha"-øjeblikke sker, når deltagerne ser den lokale `/responses` round-trip lyse op.
- **Hav et backup-projekt klar.** Hvis en deltager når en kvoteblokering i Foundry-projektet, del et forudprovisioneret projekt til udrulningstrinnet i stedet for at blokere lokalet.
- **Par deltagerne.** Lab 02 (multi-agent) er mærkbart lettere, når deltagerne kan diskutere orkestreringen med en partner.
- **Brug dokumentationsmodulerne som check-punkter.** Hvert labs `docs/` mappe er opdelt i 8 nummererede moduler - brug dem som naturlige pausepunkter.
- **Forhent den grundlæggende Docker image** på fælles lab-maskiner for at undgå registreringshastighedsbegrænsninger.

---

## Fejlfinding under levering

| Symptom                                 | Første ting at prøve                                                                                           |
|----------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Agent Inspector kan ikke oprette forbindelse | Bekræft at port `8088` er ledig, og at opgaven `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` kører.        |
| Debugger kan ikke tilknyttes           | Tjek at port `5679` er ledig; genstart VS Code, hvis `debugpy` allerede er bundet.                              |
| `azd up` fejler med autorisationsfejl | Kør `az login` og `azd auth login`, sikr at den korrekte tenant er valgt.                                      |
| Udrulning hænger ved ACR push           | Tjek at Docker Desktop kører, og at brugeren har `AcrPush` på registeret.                                     |
| Model returnerer 404 / deployment-not-found | Modellenavn i `agent.yaml` skal matche udrulningen i Foundry-projektet.                                       |

| Hostet agent sidder fast i `Provisioning`     | Bekræft at projektets region [understøtter hostede agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) og at der er kvote tilgængelig. |
| Playground returnerer 401                     | Re-autentificér Foundry-udvidelsen fra VS Code aktivitetslinjen.                                |

For dybere vejledning har hvert laboratorium sin egen `08-troubleshooting.md`-fil - henvis deltagere dertil:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Tilpasning af denne session

Du er velkommen til at tilpasse workshoppen til dit publikum. Almindelige variationer:

- **Backend-publikum:** brug mere tid på `agent.yaml`, Docker og ACR; skær playground-demoen ned.
- **Citizen-developer-publikum:** bliv i Foundry-udvidelsens UI til scaffolding; reducer CLI-trin.
- **Enkelt 60-minutters session:** lever kun introduktion, demo og Lab 01.
- **Kun workshop (ingen slides) format:** åbn begge laboratoriums-README'er og brug dem som primært manuskript.

Hvis du udvider laboratorierne, bedes du bidrage med ændringerne via PR, så andre undervisere kan få glæde af dem.

---

## Yderligere ressourcer

- [Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Oversigt over hostede agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Kom godt i gang: deploy din første hostede agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Deploy en hostet agent (how-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit til VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakter

Hvis du har spørgsmål om gennemførelse af denne session, så opret venligst et issue i [workshop-repositoriet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) og tag vedligeholderen.

| Rolle               | Navn           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Vedligeholder / kontakt| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->