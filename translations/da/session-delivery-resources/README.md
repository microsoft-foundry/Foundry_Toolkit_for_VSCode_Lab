# Hvordan man leverer denne session

Tak for at levere denne session!

Før du leverer workshoppen, bedes du:

1. Læse dette dokument og alle inkluderede ressourcer i deres fulde omfang.
2. Se optagelsen af sessionens levering og gennemgangen af workshoppen fra start til slut.
3. Gennemføre begge hands-on labs fra start til slut på din egen maskine **mindst én gang** før eventet.
4. Validere dit Microsoft Foundry-projekt, modeludrulninger og kvoter.
5. Kontakte vedligeholderen, hvis noget er uklart.

---

## Filoversigt

| Ressource                    | Link                                                                             | Beskrivelse                                                                            |
|-----------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Workshop slide deck          | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                         | Præsentationsslides til denne workshop med præsentationsnoter og indlejrede demo-videoer |
| Optagelse af sessionens levering | _Tilvejebringes af vedligeholderen_                                           | Introduktion til workshoppen og gennemgang af slides                                     |
| Optagelse af workshop fra start til slut | _Tilvejebringes af vedligeholderen_                                           | Optagelse af begge labs set fra en lærendes perspektiv                                  |
| Workshop dokumentation      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                                           | Kilderepository, lab-README-filer, trin-for-trin moduler                               |
| Lab 01 - enkelt agent       | [Lab 01](../workshop/lab01-single-agent/README.md)                                               | Hands-on lab: byg, test og deployér *Explain Like I'm an Executive* værtsagent          |
| Lab 02 - multi-agent workflow| [Lab 02](../workshop/lab02-multi-agent/README.md)                                               | Hands-on lab: byg 4-agent *Resume to Job Fit Evaluator* workflow                        |
| Demo 1: Executive Agent     | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                          | Lab 01 demo: oversæt teknisk jargon til et ledelsesresumé                              |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                               | Lab 02 demo: 4-agent workflow der scorer cv-job match og genererer anbefalinger        |

> **Note til undervisere:** Slide deck og videolinks tilføjes, når optagelserne offentliggøres. Indtil da, kontakt vedligeholderen (se [Kontakter](#contacts)) for de seneste materialer.

---

## Kom godt i gang

Denne workshop lærer udviklere, hvordan man bygger, tester og deployerer AI-agenter til **Microsoft Foundry Agent Service** som **Hosted Agents** direkte fra VS Code ved hjælp af **Microsoft Foundry Toolkit** udvidelsen.

Workshoppen er opdelt i flere sektioner inklusive slides, **2 live demos**, og **2 hands-on labs**.

### Tidsplan

#### Fuld levering (ca. 2 timer)

| Tid             | Beskrivelse                                                        |
|-----------------|--------------------------------------------------------------------|
| 0:00 - 10:00    | Intro: hosted agents, Foundry Agent Service, og toolkit            |
| 10:00 - 20:00   | Demo: Executive Agent fra start til slut                           |
| 20:00 - 60:00   | Lab 01 - enkelt agent (byg, test lokalt, deploy, playground)       |
| 60:00 - 110:00  | Lab 02 - multi-agent workflow (Resume to Job Fit Evaluator)       |
| 110:00 - 120:00 | Afrunding, Q&A og materialer til videre læring                     |

#### Kort levering (ca. 75 minutter)

| Tid          | Beskrivelse                                                  |
|--------------|--------------------------------------------------------------|
| 0:00 - 10:00 | Intro og overblik                                           |
| 10:00 - 20:00| Demo: Executive Agent                                       |
| 20:00 - 70:00| Kun Lab 01 (henvis deltagerne til Lab 02 som selvstart)    |
| 70:00 - 75:00| Afrunding og Q&A                                           |

### Forberedelse

| Ressource                     | Link                                                                                      | Beskrivelse                                |
|------------------------------|-------------------------------------------------------------------------------------------|--------------------------------------------|
| Workshop dokumentation        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                                                     | Workshop dokumentation og kilde             |
| Lab 01 instruktioner          | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                            | Hands-on lab: enkelt hosted agent            |
| Lab 02 instruktioner          | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                            | Hands-on lab: multi-agent workflow           |
| Forudsætningscheckliste       | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                                         | Nødvendige værktøjer, konti og Azure adgang |
| Hosted agents quickstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)                                                        | Officiel quickstart til at deployere hosted agent med `azd`   |
| Hosted agents regions tilgængelighed | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)                                                  | Understøttede regioner for hosted agents (preview)                            |

### Forudsætninger for underviseren

Før du leverer, sørg for at du har:

- Et **Azure abonnement** med tilladelse til at oprette ressourcer (Ejer eller Bidragyder på en ressourcegruppe).
- Adgang til et **Microsoft Foundry projekt** i en [region, der understøtter hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvote for **gpt-4.1** (eller **gpt-4.1-mini**) i dit Foundry projekt.
- Følgende værktøjer installeret:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Valgfrit)
  - Python 3.12 eller nyere

Kør [Hosted agents quickstart med `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) mindst én gang før levering, så du har et kendt godt Foundry-projekt, modeludrulning og Azure Container Registry at referere til, hvis en deltager sidder fast.

---

## Slide gennemgang

Decket følger samme flow som labs. Forslåede samtalepunkter for hver sektion:

| Sektion                    | Hovedbudskab                                                                                              |
|----------------------------|----------------------------------------------------------------------------------------------------------|
| Titel og agenda            | Ram workshoppen ind som *VS Code til Foundry* uden behov for portal-skift.                               |
| Hvorfor hosted agents?      | Administreret runtime, ACR-baseret deployment, OpenAI-kompatibel `/responses` API, scoped til Foundry projekter. |
| Arkitekturdiagram          | Gennemgå [README arkitektur](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.          |
| Anatomi af en hosted agent | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - hvad hver fil gør.                     |
| Live demo: Executive Agent | Skift til VS Code og kør [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demoen fra start til slut (se [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Skift til VS Code og kør [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo (se [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 kort                | Overlad til deltagerne. Henvis til [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md).                      |
| Multi-agent mønstre        | Sekventiel vs samtidig vs overlevering - intro inden Lab 02 starter.                                   |
| Lab 02 kort                | Overlad til deltagerne. Henvis til [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md).                      |
| Afrunding og ressourcer    | Links til videre læring fra afsnittet [Yderligere ressourcer](#additional-resources).                  |

---

## Demoer

To live demos er inkluderet i leveringen. Afhold 10 minutter til hver.

| Demo                       | Lab    | Filer                       | Hvad der skal vises                                               |
|----------------------------|--------|-----------------------------|------------------------------------------------------------------|
| Executive Agent            | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)  | Enkelt hosted agent; oversæt teknisk jargon til ledelsesresumé   |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)  | 4-agent orkestrering; scor cv-job match og generer anbefaling    |

### Demo 1: Executive Agent

En selvstændig agent i [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Brug denne som en 10 minutters demo før Lab 01.

1. Åbn [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) og gennemgå agentdefinitionen (systemprompt, model, framework).
2. Tryk `F5` for at starte **Agent Inspector** lokalt.
3. Indsæt eksempelprompten fra [README](../README.md#see-it-in-action) og vis executive-summary responsen.
4. Vis [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) og [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) for at forklare deployeringsartefakterne.
5. Demonstrer deploymentsflowet (Docker build, ACR push, hosted agent create) uden at vente på afslutning.

### Demo 2: Resume to Job Fit Evaluator

En 4-agent workflow i [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Brug denne som en 10 minutters demo før Lab 02.

1. Åbn [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) og vis, hvordan de fire agenter forbindes i en sekventiel orkestrering.
2. Tryk `F5` for at starte **Agent Inspector** for multi-agent workflowet.
3. Indsæt en kort jobbeskrivelse og et eksempel-cv i Inspector chatten.
4. Gå igennem fire-agent pipelinen: cv-parser, jobkrav-udtrækker, fit scorer og anbefalingsskriver.
5. Påpeg hvordan outputtet fra hver under-agent bliver kontekst for den næste agent, med fokus på overleveringsmønsteret.
6. Vis [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) for at sammenligne med enkelt-agent ekvivalenten fra Demo 1.

---

## Tips til levering

- **Sæt forventninger tidligt.** Hosted agents er i preview - nævn regionsbegrænsninger og kvoter på forhånd, så deltagerne ikke bliver overrasket midt i lab’en.
- **Kør forudsætningsopgaven først.** Begge labs har en `Validate prerequisites` VS Code-opgave - lad deltagerne køre den, inden der skrives kode.
- **Hold Agent Inspector synlig.** De fleste "aha"-øjeblikke sker, når deltagerne ser den lokale `/responses` rundtur lyses op.
- **Hav et backup-projekt.** Hvis en deltager støder på kvotebegrænsning i Foundry-projektet, del et forudklargjort projekt til deployeringstrinnet i stedet for at blokere rummet.
- **Par deltagere sammen.** Lab 02 (multi-agent) er markant lettere, når deltagerne kan snakke orkestreringen igennem sammen.
- **Brug dokumentationsmoduler som checkpoints.** Hver labs `docs/` mappe er delt i nummererede moduler - brug dem som naturlige pauser.
- **Forhent basis Docker image** på fælles labmaskiner for at undgå registry-rate begrænsninger.

---

## Fejlfinding under levering

| Symptom                                   | Første forsøg på løsning                                                                                    |
|-------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Agent Inspector kan ikke forbinde          | Bekræft at port `8088` er ledig, og at `Run Agent HTTP Server` opgaven kører.                           |
| Debugger kan ikke tilknyttes               | Tjek at port `5679` er ledig; genstart VS Code hvis `debugpy` allerede er bundet.           |
| `azd up` fejler med auth fejl   | Kør `az login` og `azd auth login`, sørg for at den korrekte tenant er valgt.                        |
| Deployering hænger ved ACR push             | Tjek at Docker Desktop kører, og at brugeren har `AcrPush` på registret.                             |
| Model returnerer 404 / deployment-not-found| Modeludrulningsnavnet i `agent.yaml` skal matche udrulningen i Foundry-projektet.                        |
| Hosted agent sidder fast i `Provisioning`| Bekræft at projektsregionen [understøtter hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability), og at kvote er tilgængelig. |
| Playground returnerer 401                   | Re-autentificer Foundry-udvidelsen fra VS Code’s aktivitetslinje.                                           |

For dybere vejledning følger hver lab sin egen `08-troubleshooting.md` dokumentation - henvis deltagerne derhen:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Tilpasning af denne session

Du er velkommen til at tilpasse workshoppen til dit publikum. Almindelige variationer:

- **Backend publikum:** brug mere tid på `agent.yaml`, Docker og ACR; skær ned på playground-demoen.
- **Citizen-developer publikum:** bliv i Foundry-udvidelsens UI til scaffolding; reducer CLI-trin.
- **Single-track 60-minutters slot:** lever kun intro, demo og Lab 01.
- **Kun workshop-format (ingen slides):** åbn begge lab READMEs og brug dem som det primære manuskript.

Hvis du udvider labs, bedes du bidrage med ændringerne via PR, så andre trænere kan få gavn af det.

---

## Yderligere ressourcer

- [Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Oversigt over hosted agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Quickstart: deploy din første hosted agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Deploy en hosted agent (how-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry Toolkit til VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakter

Hvis du har spørgsmål om afholdelse af denne session, så opret et issue i [workshop-repositoriet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) og tag vedligeholderen.

| Rolle               | Navn           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Vedligeholder / kontakt | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->