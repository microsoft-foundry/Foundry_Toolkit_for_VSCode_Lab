# Hvordan holde denne økten

Takk for at du holder denne økten!

Før du holder workshoppen, vennligst:

1. Les dette dokumentet og alle inkluderte ressurser i sin helhet.
2. Se opptaket av sesjonsleveringen og gjennomgangen av workshoppen fra start til slutt.
3. Gå gjennom begge praktiske labber fra start til slutt på din egen maskin **minst én gang** før arrangementet.
4. Verifiser ditt Microsoft Foundry-prosjekt, modellutrullinger og kvoter.
5. Ta kontakt med vedlikeholderen hvis noe er uklart.

---

## Filoversikt

| Ressurs                      | Lenke                                                                             | Beskrivelse                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop-presentasjon         | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Presentasjonslysbilder for denne workshopen med presentatørnotater og innebygde demovideoer |
| Opptak av sesjonslevering    | _Vil bli levert av vedlikeholder_                                               | Innledning til workshoppen og gjennomgang av lysbildene i opptak                           |
| Opptak av end-to-end workshop | _Vil bli levert av vedlikeholder_                                               | End-to-end opptak av begge labber fra en deltakers perspektiv                              |
| Workshopdokumentasjon        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Kilde-repository, lab-lesmeg, trinnvise moduler                                            |
| Lab 01 - enkelt agent         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Praktisk lab: bygg, test, og deployer *Explain Like I'm an Executive* hostet agent         |
| Lab 02 - fleragent arbeidsflyt | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Praktisk lab: bygg 4-agent *Resume to Job Fit Evaluator* arbeidsflyt                       |
| Demo 1: Executive Agent       | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Lab 01 demo: oversett teknisk sjargong til en lederoppsummering                            |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Lab 02 demo: 4-agent arbeidsflyt som vurderer CV-jobb-pasning og genererer anbefalinger     |

> **Merk til trenere:** Lysbildebunken og video lenker blir lagt til når opptakene er publisert. Inntil da, kontakt vedlikeholder (se [Kontakter](#contacts)) for siste oppdateringer.

---

## Kom i gang

Denne workshopen lærer utviklere å bygge, teste og deployere AI-agenter til **Microsoft Foundry Agent Service** som **Hosted Agents** helt fra VS Code, ved bruk av **Microsoft Foundry Toolkit**-utvidelsen.

Workshopen er delt inn i flere seksjoner, inkludert lysbilder, **2 live-demoer**, og **2 praktiske labber**.

### Tidspunkt

#### Full levering (omtrent 2 timer)

| Tid              | Beskrivelse                                                          |
|------------------|----------------------------------------------------------------------|
| 0:00 - 10:00     | Introduksjon: Hosted agents, Foundry Agent Service og toolkit        |
| 10:00 - 20:00    | Demo: Executive Agent end-to-end                                     |
| 20:00 - 60:00    | Lab 01 - enkelt agent (bygg, test lokalt, deploy, lekeområde)        |
| 60:00 - 110:00   | Lab 02 - fleragent arbeidsflyt (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00  | Oppsummering, spørsmål og svar, og ressurser for videre læring       |

#### Kort levering (omtrent 75 minutter)

| Tid             | Beskrivelse                                                      |
|-----------------|-----------------------------------------------------------------|
| 0:00 - 10:00    | Introduksjon og oversikt                                        |
| 10:00 - 20:00   | Demo: Executive Agent                                           |
| 20:00 - 70:00   | Kun Lab 01 (vis Lab 02 som selvstudium)                        |
| 70:00 - 75:00   | Oppsummering og spørsmål og svar                               |

### Forberedelse

| Ressurs                        | Lenke                                                                                          | Beskrivelse                                    |
|-------------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------------|
| Workshopdokumentasjon          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Workshopdokumentasjon og kildekode             |
| Lab 01 instruksjoner           | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Praktisk lab: enkelt hostet agent              |
| Lab 02 instruksjoner           | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Praktisk lab: fleragent arbeidsflyt            |
| Sjekkliste for forutsetninger | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Verktøy, kontoer og Azure-tilgang kreves       |
| Hosted agents kjappstart (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Offisiell kjappstart for å deployere en hosted agent med `azd` |
| Tilgjengelighet av hosted agents regioner | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Støttede regioner for hosted agents (preview)  |

### Forutsetninger for treneren

Før du holder økten, sørg for at du har:

- Et **Azure-abonnement** med tillatelse til å opprette ressurser (Owner eller Contributor på en ressursgruppe).
- Tilgang til et **Microsoft Foundry-prosjekt** i en [region som støtter hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvote for **gpt-4.1** (eller **gpt-4.1-mini**) i Foundry-prosjektet ditt.
- Følgende verktøy installert:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (valgfritt)
  - Python 3.12 eller nyere

Kjør [Hosted agents kjappstart med `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) minst én gang før økten, slik at du har et kjent fungerende Foundry-prosjekt, modellutrulling, og Azure Container Registry å referere til hvis en deltaker støter på problemer.

---

## Lysbildegjennomgang

Presentasjonen følger samme flyt som labbene. Forslag til viktige punkter for hver seksjon:

| Seksjon                     | Hovedbudskap                                                                                                  |
|----------------------------|--------------------------------------------------------------------------------------------------------------|
| Tittel og agenda           | Rammeverk workshoppen som *VS Code til Foundry* uten behov for å bytte portal.                               |
| Hvorfor hosted agents?     | Administrert runtime, ACR-basert deploy, OpenAI-kompatibel `/responses` API, avgrenset til Foundry-prosjekter.|
| Arkitekturdiagram          | Gå gjennom [README-arkitektur](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.            |
| Anatomien til en hosted agent | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - hva hver fil gjør.                        |
| Live demo: Executive Agent | Bytt til VS Code og kjør [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demoen fra start til slutt (se [Demo 1](#demo-1-executive-agent)). |
| Live demo: Resume to Job Fit Evaluator | Bytt til VS Code og kjør [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent demo (se [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Kort om Lab 01             | Overlever til deltakerne. Vis til [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Fleragentmønstre           | Sekvensiell vs samtidig vs overlevering - forhåndsvis før Lab 02 starter.                                   |
| Kort om Lab 02             | Overlever til deltakerne. Vis til [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Oppsummering og ressurser  | Lenker for videre læring fra [Ytterligere ressurser](#additional-resources) seksjonen.                    |

---

## Demoer

To live-demoer er inkludert i leveringen. Allocér 10 minutter til hver.

| Demo                     | Lab   | Filer                     | Hva som skal vises                            |
|--------------------------|-------|---------------------------|----------------------------------------------|
| Executive Agent          | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Enkelt hostet agent; oversett teknisk sjargong til en lederoppsummering |
| Resume to Job Fit Evaluator | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orkestrering; vurder CV-jobb-pasning og lag en anbefaling    |

### Demo 1: Executive Agent

En frittstående agent i [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Bruk denne som en 10-minutters demo før Lab 01.

1. Åpne [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) og gå gjennom agentdefinisjonen (systemprompt, modell, rammeverk).
2. Trykk `F5` for å starte **Agent Inspector** lokalt.
3. Lim inn eksempelprompt fra [README](../README.md#see-it-in-action) og vis responset for lederoppsummering.
4. Vis [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) og [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) for å forklare deployartefaktene.
5. Demonstrer deployflyten (Docker build, ACR push, hosted agent opprettelse) uten å vente på fullføring.

### Demo 2: Resume to Job Fit Evaluator

En 4-agent arbeidsflyt i [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Bruk denne som en 10-minutters demo før Lab 02.

1. Åpne [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) og vis hvordan de fire agentene er koblet i en sekvensiell orkestrering.
2. Trykk `F5` for å starte **Agent Inspector** for fleragent arbeidsflyt.
3. Lim inn en kort stillingsbeskrivelse og et eksempel på CV i Inspector-chatten.
4. Gå gjennom den fire-agenters pipeline: CV-parser, jobbkravsekstraktor, vurderingsskårer, og anbefalingsskriver.
5. Påpek hvordan hver underagents utdata blir neste agents kontekst, og fremhev overleveringsmønsteret.
6. Vis [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) for å sammenligne med enkelt-agent ekvivalent fra Demo 1.

---

## Tips for leveringen

- **Sett forventninger tidlig.** Hosted agents er i forhåndsvisning – informer om regionsbegrensninger og kvoter på forhånd så deltakerne ikke blir overrasket midt i labben.
- **Kjør forutsetningsoppgaven først.** Begge labber har en `Validate prerequisites` VS Code-oppgave – la deltakerne kjøre den før noen koding.
- **Hold Agent Inspector synlig.** De fleste “aha”-øyeblikk skjer når deltakerne ser den lokale `/responses` rundtur lyse opp.
- **Ha et reserveprosjekt.** Hvis en deltakers Foundry-prosjekt treffer en kvotebegrensning, del et forhåndsprovisionert prosjekt for deploy-steget i stedet for å blokkere rommet.
- **Par deltakerne.** Lab 02 (fleragent) er betydelig enklere når deltakerne kan diskutere orkestreringen med en partner.
- **Bruk dokumentasjonsmodulene som sjekkpunkter.** Hver labs `docs/`-mappe er delt opp i nummererte moduler – bruk disse som naturlige pausepunkter.
- **Forhåndstrekk basis Docker-bilde** på delte lab-maskiner for å unngå ratebegrensninger i registeret.

---

## Feilsøking under leveringen

| Symptom                                      | Første ting å prøve                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector kan ikke koble til           | Bekreft at port `8088` er ledig og at `Run Agent HTTP Server`-oppgaven kjører.                      |
| Debugger klarer ikke å koble til             | Sjekk at port `5679` er ledig; start VS Code på nytt hvis `debugpy` allerede er bundet. |
| `azd up` feiler med autentiseringsfeil | Kjør `az login` og `azd auth login`, sørg for at riktig tenant er valgt.                         |
| Deploy henger på ACR push                     | Sjekk at Docker Desktop kjører og at brukeren har `AcrPush` på registeret.                       |
| Modell returnerer 404 / deployment-not-found | Navnet på modellutrullingen i `agent.yaml` må samsvare med deployeringen i Foundry-prosjektet.       |
| Hosted agent sitter fast i `Provisioning`     | Verifiser at prosjektets region [støtter hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) og at kvote er tilgjengelig. |
| Playground returnerer 401                      | Re-autentiser Foundry-utvidelsen fra VS Code aktivitetspanelet.                                          |

For grundigere veiledning, hver lab har sin egen `08-troubleshooting.md`-dokumentasjon - lenk deltakerne dit:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Tilpasse denne økten

Du er velkommen til å tilpasse workshoppen for ditt publikum. Vanlige variasjoner:

- **Backend-publikum:** bruk mer tid på `agent.yaml`, Docker og ACR; kutt ned demoen i lekeområdet.
- **Citizen-utvikler publikum:** hold deg i Foundry-utvidelsens UI for scaffold; reduser CLI-steget.
- **Enkeltspor 60-minutters økt:** lever kun intro, demo og Lab 01.
- **Kun workshop-format (ingen lysbilder):** åpne begge lab-READMEene og bruk dem som hovedmanus.

Hvis du utvider labene, vennligst bidra med endringene via PR slik at andre trenere kan dra nytte av dem.

---

## Ytterligere ressurser

- [Microsoft Foundry-dokumentasjon](https://learn.microsoft.com/azure/ai-foundry/)
- [Oversikt over hostede agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Raskstart: distribuer din første hostede agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Distribuer en hostet agent (hvordan)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakter

Hvis du har spørsmål om gjennomføringen av denne økten, vennligst åpne en sak i [workshop-repositoriet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) og tagg vedlikeholderen.

| Rolle               | Navn           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Vedlikeholder / kontakt | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->