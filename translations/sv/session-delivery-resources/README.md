# Hur man håller denna session

Tack för att du håller denna session!

Innan du håller workshoppen, vänligen:

1. Läs detta dokument och alla inkluderade resurser i sin helhet.
2. Titta på inspelningen av sessionsgenomgången och workshoppen steg-för-steg.
3. Gå igenom båda praktiska labben från början till slut på din egen dator **minst en gång** innan eventet.
4. Validera ditt Microsoft Foundry-projekt, modellutplaceringar och kvoter.
5. Kontakta ansvarig om något är oklart.

---

## Filöversikt

| Resurs                       | Länk                                                                              | Beskrivning                                                                               |
|-----------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Workshop-slide-presentation  | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                            | Presentation med slides för denna workshop med presentatörsanteckningar och inbäddade demovideor |
| Inspelning av sessionsgenomgång | _Tillhandahålls av ansvarig_                                                     | Inspelning av workshopintroduktion och genomgång av slides                               |
| Inspelning av workshoppen steg-för-steg | _Tillhandahålls av ansvarig_                                                | Steg-för-steg-inspelning av båda labben ur en deltagares perspektiv                      |
| Workshop-dokumentation       | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                                              | Källkodsförråd, labb-README-filer, steg-för-steg-moduler                               |
| Lab 01 - enskild agent       | [Lab 01](../workshop/lab01-single-agent/README.md)                                                  | Praktisk labb: bygg, testa och distribuera den *Explain Like I'm an Executive*-hostade agenten |
| Lab 02 - flersidig agentworkflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                                             | Praktisk labb: bygg 4-agenters *Resume to Job Fit Evaluator*-workflow                   |
| Demo 1: Executive Agent      | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                            | Demo från Lab 01: översätt tekniskt jargong till en executive summering                  |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                              | Demo från Lab 02: 4-agenters workflow som poängsätter CV-job matchning och genererar rekommendationer |

> **Notering för tränare:** Slide presentation och videolänkar kommer att läggas till när inspelningarna publiceras. Kontakta ansvarig (se [Kontakter](#contacts)) för de senaste resurserna tills vidare.

---

## Kom igång

Denna workshop lär utvecklare hur man bygger, testar och distribuerar AI-agenter till **Microsoft Foundry Agent Service** som **hostade agenter** helt från VS Code med hjälp av **Microsoft Foundry Toolkit**-tillägget.

Workshoppen är uppdelad i flera sektioner inklusive slides, **2 live-demonstrationer** och **2 praktiska labbar**.

### Tidplan

#### Full leverans (cirka 2 timmar)

| Tid           | Beskrivning                                                           |
|---------------|----------------------------------------------------------------------|
| 0:00 - 10:00  | Introduktion: hostade agenter, Foundry Agent Service och toolkit      |
| 10:00 - 20:00 | Demo: Executive Agent från början till slut                           |
| 20:00 - 60:00 | Lab 01 - en agent (bygg, testa lokalt, distribuera, playground)       |
| 60:00 - 110:00| Lab 02 - flersidig agentworkflow (Resume to Job Fit Evaluator)        |
| 110:00 - 120:00 | Avslutning, frågor och svar, samt resurser för fortsatt lärande       |

#### Kort leverans (cirka 75 minuter)

| Tid            | Beskrivning                                                      |
|----------------|------------------------------------------------------------------|
| 0:00 - 10:00   | Introduktion och överblick                                      |
| 10:00 - 20:00  | Demo: Executive Agent                                           |
| 20:00 - 70:00  | Endast Lab 01 (peka deltagare till Lab 02 för egen takt)       |
| 70:00 - 75:00  | Avslutning och frågestund                                       |

### Förberedelse

| Resurs                      | Länk                                                                                   | Beskrivning                                              |
|-----------------------------|----------------------------------------------------------------------------------------|----------------------------------------------------------|
| Workshop-dokumentation      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                                                  | Workshop-dokumentation och källkod                        |
| Lab 01 instruktioner       | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                          | Praktisk labb: enskild hostad agent                       |
| Lab 02 instruktioner       | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                          | Praktisk labb: flersidig agentworkflow                    |
| Förkunskapschecklista      | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                                       | Verktyg, konton och Azure-åtkomst som krävs               |
| Snabbstart hostade agenter (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)                                                  | Officiell snabbstart för utplacering av hostad agent med `azd` |
| Tillgängliga regioner för hostade agenter | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)                                              | Stödda regioner för hostade agenter (preview)             |

### Tränarens förutsättningar

Innan du håller sessionen, säkerställ att du har:

- En **Azure-prenumeration** med behörighet att skapa resurser (Ägare eller Bidragsgivare på resursgrupp).
- Tillgång till ett **Microsoft Foundry-projekt** i en [region som stöder hostade agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvot för **gpt-4.1** (eller **gpt-4.1-mini**) i ditt Foundry-projekt.
- Följande verktyg installerade:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (valfritt)
  - Python 3.12 eller senare

Kör [Hosted agents snabbstart med `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) minst en gång innan sessionen så att du har ett känt fungerande Foundry-projekt, modellutplacering och Azure Container Registry att referera till om någon fastnar.

---

## Genomgång av slides

Presentationen följer samma flöde som labben. Föreslagna samtalspunkter för varje sektion:

| Sektion                   | Nyckelbudskap                                                                                          |
|---------------------------|------------------------------------------------------------------------------------------------------|
| Titel och agenda          | Beskriv workshoppen som *VS Code till Foundry* utan krav på portalväxling.                          |
| Varför hostade agenter?   | Hanterad runtime, ACR-baserad distribution, OpenAI-kompatibel `/responses` API, scoped till Foundry-projekt. |
| Arkitekturdiagram         | Gå igenom [README-arkitektur](../README.md#architecture): scaffolding, Inspector, ACR, Agent Service. |
| Anatomi av en hostad agent | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` – vad varje fil gör.       |
| Live-demo: Executive Agent| Byt till VS Code och kör [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demon från början till slut (se [Demo 1](#demo-1-executive-agent)). |
| Live-demo: Resume to Job Fit Evaluator | Byt till VS Code och kör [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agent-demo (se [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Lab 01 brief             | Överlämna till deltagarna. Pekar på [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md).                   |
| Flersidiga agentmönster  | Sekventiell vs parallell vs överlämning - introduktion innan Lab 02 startar.                        |
| Lab 02 brief             | Överlämna till deltagarna. Pekar på [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md).                   |
| Avslutning och resurser  | Länkar för fortsatt lärande från [Ytterligare resurser](#additional-resources) sektionen.          |

---

## Demoer

Två live-demoer ingår i leveransen. Avsätt 10 minuter för varje.

| Demo                  | Labb   | Filer                                                   | Vad som ska visas                                                   |
|-----------------------|--------|---------------------------------------------------------|-------------------------------------------------------------------|
| Executive Agent       | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)            | Enskild hostad agent; översätt tekniskt jargong till executivesammanfattning |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)           | 4-agent orkestrering; poängsätt CV-job matchning och generera rekommendation |

### Demo 1: Executive Agent

En fristående agent i [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Använd som 10-minuters demo innan Lab 01.

1. Öppna [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) och gå igenom agentdefinitionen (systemprompt, modell, ramverk).
2. Tryck `F5` för att starta **Agent Inspector** lokalt.
3. Klistra in exempelprompten från [README](../README.md#see-it-in-action) och visa executivesammanfattningssvaret.
4. Visa [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) och [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) för att förklara distributionsartefakterna.
5. Demonstrera distributionsflödet (Docker build, ACR push, hostad agent skapa) utan att vänta på slutförande.

### Demo 2: Resume to Job Fit Evaluator

En 4-agentors workflow i [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Använd som 10-minuters demo innan Lab 02.

1. Öppna [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) och visa hur de fyra agenterna är kopplade i en sekventiell orkestrering.
2. Tryck `F5` för att starta **Agent Inspector** för multi-agent workflow.
3. Klistra in en kort arbetsbeskrivning och ett exempel-CV i Inspector-chattfönstret.
4. Gå igenom fyra-agenteranläggningen: CV-parser, jobbkravsutdragare, matchningsbedömare och rekommendationsförfattare.
5. Påpeka hur varje underagents utdata blir nästa agents kontext och belys överlämningsmönstret.
6. Visa [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) för jämförelse med motsvarande enskilda agent från Demo 1.

---

## Leveranstips

- **Sätt förväntningarna tidigt.** Hostade agenter är i preview - betona regionbegränsningar och kvot upfront så att deltagarna inte överraskas mitt i labben.
- **Kör förberedande uppgifter först.** Båda labben har en `Validate prerequisites` VS Code-uppgift - låt deltagarna köra denna innan någon kod skrivs.
- **Håll Agent Inspector synlig.** De flesta "aha"-upplevelser sker när deltagarna ser den lokala `/responses` rundresan lysa upp.
- **Ha ett backup-projekt.** Om en deltagares Foundry-projekt träffar en kvotgräns, dela ett förkonfigurerat projekt för distributionssteget så att rummet inte blir blockerat.
- **Para ihop deltagarna.** Lab 02 (flersidig agent) är märkbart enklare när deltagarna kan diskutera orkestreringen med en partner.
- **Använd dokumentationsmodulerna som kontrollpunkter.** Varje labbs `docs/` mapp är uppdelad i numrerade moduler - använd dessa som naturliga pauspunkter.
- **Förladda bas-Dockerbilden** på delade labbdatorer för att undvika registreringshastighetsbegränsningar.

---

## Felsökning under leverans

| Symptom                                   | Första åtgärden att prova                                                      |
|-------------------------------------------|-------------------------------------------------------------------------------|
| Agent Inspector kan inte ansluta          | Bekräfta att port `8088` är fri och att `Run Agent HTTP Server`-uppgiften är igång.         |
| Debugger kan inte kopplas                   | Kontrollera att port `5679` är fri; starta om VS Code om `debugpy` redan är bunden.          |
| `azd up` misslyckas med autentiseringsfel | Kör `az login` och `azd auth login`, säkerställ att rätt tenant är vald.                    |
| Distribution hänger sig vid ACR push       | Kontrollera att Docker Desktop körs och att användaren har `AcrPush` på registret.              |
| Modell returnerar 404 / deployment-not-found | Modellutplaceringens namn i `agent.yaml` måste matcha utplaceringen i Foundry-projektet.        |
| Hostad agent fast i `Provisioning`       | Verifiera att projektregionen [stöder hostade agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) och att kvot finns tillgänglig. |
| Playground returnerar 401                  | Autentisera om Foundry-tillägget från VS Code aktivitetsfältet.                    |

För djupare vägledning levererar varje labb en egen `08-troubleshooting.md`-dokumentation – länka deltagare dit:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Anpassa denna session

Du är välkommen att anpassa workshoppen för din publik. Vanliga varianter:

- **Backend-publiker:** spendera mer tid på `agent.yaml`, Docker och ACR; korta ner playground-demon.
- **Citizen-developer-publiker:** håll dig i Foundry-tilläggets UI för scaffolding; minska CLI-steg.
- **Enkelspårig 60-minuters slot:** leverera endast introduktion, demo och Lab 01.
- **Endast workshop-format (inga slides):** öppna båda labb-README-filerna och använd dem som huvudsakligt manus.

Om du utökar labben, vänligen bidra med ändringarna tillbaka via PR så att andra tränare kan dra nytta av dem.

---

## Ytterligare resurser

- [Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Översikt över hostade agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Snabbstart: distribuera din första hostade agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Distribuera en hostad agent (how-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry Toolkit för VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakter

Om du har frågor om att leverera denna session, vänligen öppna ett ärende på [workshop-repositoriet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) och tagga underhållaren.

| Roll                | Namn           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Underhållare / kontakt| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->