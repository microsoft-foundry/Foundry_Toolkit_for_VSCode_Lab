# Hur man levererar denna session

Tack för att du levererar denna session!

Innan du levererar workshopen, vänligen:

1. Läs detta dokument och alla inkluderade resurser i sin helhet.
2. Titta på inspelningen av sessionens leverans och genomgången av workshopen från början till slut.
3. Gå igenom båda de praktiska labben från början till slut på din egen dator **minst en gång** före eventet.
4. Validera ditt Microsoft Foundry-projekt, modellutplaceringar och kvoter.
5. Kontakta ansvarig om något är oklart.

---

## Sammanfattning av filer

| Resurs                        | Länk                                                                             | Beskrivning                                                                              |
|------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Workshop presentation        | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Presentationsbilder för denna workshop med anteckningar för presentatören och inbäddade demovideor |
| Inspelning av sessionsleverans | _Tillhandahålls av ansvarig_                                                     | Inspelning av introduktion till workshopen och genomgång av bilder                        |
| Inspelning av end-to-end-workshop | _Tillhandahålls av ansvarig_                                                     | End-to-end-inspelning av båda labben från en deltagares perspektiv                        |
| Workshopsdokumentation       | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Källkodsförråd, labb-README-filer, steg-för-steg-moduler                                 |
| Labb 01 - enskild agent      | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Praktiskt labb: bygg, testa och distribuera den *Explain Like I'm an Executive* hostade agenten |
| Labb 02 - multi-agent-arbetsflöde | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Praktiskt labb: bygg arbetsflödet för 4-agents *Resume to Job Fit Evaluator*             |
| Demo 1: Executive Agent            | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Demo för labb 01: översätt tekniskt språk till en sammanfattning för ledningen           |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demo för labb 02: 4-agenters arbetsflöde som poängsätter CV-jobp-matchning och genererar rekommendationer |

> **Notis för utbildare:** Presentation och videolänkar kommer att läggas till när inspelningarna publiceras. Under tiden, kontakta den ansvarige (se [Kontakter](#kontakter)) för de senaste tillgångarna.

---

## Kom igång

Denna workshop lär utvecklare hur man bygger, testar och distribuerar AI-agenter till **Microsoft Foundry Agent Service** som **Hostade agenter** helt och hållet från VS Code, med hjälp av tillägget **Microsoft Foundry Toolkit**.

Workshopen är uppdelad i flera sektioner inklusive slides, **2 live-demos** och **2 praktiska labb**.

### Tidsschema

#### Full leverans (cirka 2 timmar)

| Tid             | Beskrivning                                                         |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Introduktion: hostade agenter, Foundry Agent Service, och toolkit    |
| 10:00 - 20:00   | Demo: Executive Agent från början till slut                         |
| 20:00 - 60:00   | Labb 01 - enskild agent (bygg, testa lokalt, deploya, lekplats)     |
| 60:00 - 110:00  | Labb 02 - multi-agent-arbetsflöde (Resume to Job Fit Evaluator)    |
| 110:00 - 120:00 | Avslutning, frågor och svar, och resurser för fortsatt lärande       |

#### Kort leverans (cirka 75 minuter)

| Tid             | Beskrivning                                                        |
|-----------------|------------------------------------------------------------------|
| 0:00 - 10:00    | Introduktion och översikt                                         |
| 10:00 - 20:00   | Demo: Executive Agent                                            |
| 20:00 - 70:00   | Endast Labb 01 (pek deltagarna till Labb 02 som självstudie)      |
| 70:00 - 75:00   | Avslutning och frågor                                            |

### Förberedelser

| Resurs                         | Länk                                                                                         | Beskrivning                                      |
|--------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------|
| Workshopsdokumentation         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)            | Workshopsdokumentation och källkod                |
| Instruktioner för Labb 01      | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                               | Praktiskt labb: enskild hostad agent              |
| Instruktioner för Labb 02      | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                 | Praktiskt labb: arbetsflöde med flera agenter    |
| Checklista för förkunskaper     | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)               | Verktyg, konton och Azure-åtkomst som krävs      |
| Snabbinstruktion för hostade agenter (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Officiell snabbstart för att distribuera en hostad agent med `azd` |
| Tillgänglighet för regioner för hostade agenter | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Stödda regioner för hostade agenter (förhandsgranskning) |

### Förkunskaper för utbildare

Innan du levererar, se till att du har:

- Ett **Azure-abonnemang** med behörighet att skapa resurser (Ägare eller Bidragsgivare på en resursgrupp).
- Tillgång till ett **Microsoft Foundry-projekt** i en [region som stödjer hostade agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvot för **gpt-4.1** (eller **gpt-4.1-mini**) i ditt Foundry-projekt.
- Följande verktyg installerade:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Frivilligt)
  - Python 3.10 eller senare

Kör [Snabbinstruktionen för hostade agenter med `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) minst en gång innan leverans så att du har ett känt fungerande Foundry-projekt, modellutplacering och Azure Container Registry att referera till om en deltagare fastnar.

---

## Genomgång av slides

Presentationen följer samma flöde som labben. Föreslagna samtalspunkter för varje sektion:

| Sektion                    | Nyckelbudskap                                                                                                   |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| Titel och agenda            | Rama in workshopen som *VS Code till Foundry* utan behov av att växla portal.                                  |
| Varför hostade agenter?    | Hanterad runtime, ACR-baserad distribution, OpenAI-kompatibel `/responses` API, avgränsad till Foundry-projekt. |
| Arkitekturdiagram          | Gå igenom [README-arkitekturen](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.           |
| Anatomien av en hostad agent | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` – vad varje fil gör.                                  |
| Live-demo: Executive Agent | Växla till VS Code och kör demon i [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) från början till slut (se [Demo 1](#demo-1-executive-agent)). |
| Live-demo: Resume to Job Fit Evaluator | Växla till VS Code och kör 4-agenters demon i [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (se [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Kort om Labb 01             | Ge över till deltagarna. Peka på [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Mönster för multi-agent    | Sekventiell vs parallell vs överlämning - förhandsgranska innan Labb 02 startar.                               |
| Kort om Labb 02             | Ge över till deltagarna. Peka på [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Avslutning och resurser    | Länkar för fortsatt lärande från sektionen [Ytterligare resurser](#ytterligare-resurser).                      |

---

## Demovisa

Två live-demos ingår i leveransen. Avsätt 10 minuter till vardera.

| Demo | Labb | Filer | Vad att visa |
|------|------|-------|--------------|
| Executive Agent            | Labb 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Enskild hostad agent; översätt tekniskt språk till en sammanfattning för ledningen |
| Resume to Job Fit Evaluator | Labb 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Koordinering av 4 agenter; bedöm CV-jobp-matchning och generera rekommendation |

### Demo 1: Executive Agent

En fristående agent i [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Använd denna som en 10-minuters demo före Labb 01.

1. Öppna [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) och gå igenom agentdefinitionen (systemprompt, modell, ramverk).
2. Tryck på `F5` för att starta **Agent Inspector** lokalt.
3. Klistra in exempelprompten från [README](../README.md#see-it-in-action) och visa svaret som är en sammanfattning för ledningen.
4. Visa [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) och [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) för att förklara distributionsartefakterna.
5. Demonstrera distributionsflödet (Docker build, ACR push, skapa hostad agent) utan att vänta på slutförande.

### Demo 2: Resume to Job Fit Evaluator

Ett arbetsflöde med 4 agenter i [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Använd denna som en 10-minuters demo före Labb 02.

1. Öppna [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) och visa hur de fyra agenterna är kopplade i en sekventiell orkestrering.
2. Tryck på `F5` för att starta **Agent Inspector** för multi-agent-arbetsflödet.
3. Klistra in en kort arbetsbeskrivning och ett exempel-CV i Inspector-chatten.
4. Gå igenom arbetsflödet med fyra agenter: CV-parsare, kravutdragare, matchningspoängsättare och rekommendationsförfattare.
5. Påpeka hur varje underagents output blir nästa agents kontext och framhäv överlämningsmönstret.
6. Visa [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) för att jämföra med motsvarande enskilda agent från Demo 1.

---

## Tips för leverans

- **Sätt förväntningarna tidigt.** Hostade agenter är i förhandsgranskning - påpeka regionsbegränsningar och kvoter direkt så att deltagare inte blir överraskade mitt under labben.
- **Kör förkunskapsuppgiften först.** Båda labben levereras med en VS Code-uppgift `Validate prerequisites` - låt deltagarna köra den innan någon kod skrivs.
- **Håll Agent Inspector synlig.** De flesta "aha"-ögonblicken sker när deltagarna ser det lokala `/responses` rundresesamtalet tändas.
- **Ha ett reservprojekt.** Om en deltagares Foundry-projekt når kvotgräns, dela ett förprovisionerat projekt för distributionssteget istället för att blockera rummet.
- **Para ihop deltagarna.** Labb 02 (multi-agent) är avsevärt enklare när deltagare kan diskutera orkestreringen med en partner.
- **Använd dokumentationsmodulerna som pauspunkter.** Varje labbs `docs/`-mapp är uppdelad i 8 numrerade moduler - använd dessa som naturliga pauspunkter.
- **Förhämta bas-Dockerimagen** på delade labbmaskiner för att undvika gränser för registerhastighet.

---

## Felsökning under leverans

| Symptom                                   | Första åtgärd att prova                                                                        |
|-------------------------------------------|----------------------------------------------------------------------------------------------|
| Agent Inspector kan inte ansluta           | Bekräfta att port `8088` är ledig och att uppgiften `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` körs. |
| Debuggern ansluter inte                      | Kontrollera att port `5679` är tillgänglig; starta om VS Code om `debugpy` redan är bunden.     |
| `azd up` misslyckas med autentiseringsfel  | Kör `az login` och `azd auth login`, säkerställ att rätt tenant är vald.                      |
| Distribution fastnar vid ACR push           | Kontrollera att Docker Desktop körs och att användaren har `AcrPush` på registret.             |
| Modell returnerar 404 / deployment-not-found | Modellutplaceringens namn i `agent.yaml` måste matcha utplaceringen i Foundry-projektet.     |

| Värdbaserad agent fastnat i `Provisioning`         | Kontrollera att projektets region [stöder värdbaserade agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) och att kvot finns tillgänglig. |
| Playground returnerar 401                       | Logga in igen i Foundry-tillägget från VS Code aktivitetsfält.                                     |

För mer djupgående vägledning levereras varje labb med sin egen `08-troubleshooting.md`-fil - länka deltagarna dit:

- Labb 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Labb 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Anpassa denna session

Du är välkommen att anpassa workshopen för din publik. Vanliga variationer:

- **Backend-publik:** spendera mer tid på `agent.yaml`, Docker och ACR; korta ner playground-demot.
- **Citizen-developer-publik:** håll dig inom Foundry-tilläggets UI för strukturering; minska CLI-stegen.
- **Endast ett 60-minutersspår:** leverera endast introduktion, demo och Labb 01.
- **Endast workshop (inga bilder) format:** öppna båda labbens README-filer och använd dem som huvudsakligt manus.

Om du utökar labben, vänligen bidra med ändringarna via PR så att andra instruktörer får nytta av dem.

---

## Ytterligare resurser

- [Microsoft Foundry-dokumentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Översikt av värdbaserade agenter](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Snabbstart: distribuera din första värdbaserade agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Distribuera en värdbaserad agent (hur man gör)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit för VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakter

Om du har frågor om att genomföra denna session, vänligen öppna ett ärende i [workshopförrådet](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) och tagga ansvarig.

| Roll                | Namn           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Ansvarig / kontakt  | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->