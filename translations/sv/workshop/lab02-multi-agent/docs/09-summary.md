# Modul 9 - Sammanfattning & Nästa steg

⏱️ ~5 min

**Grattis!** Du har byggt, testat och (om du är på Väg A) distribuerat ett multi-agent arbetsflöde med Microsoft Foundry och Foundry Toolkit för VS Code.

---

## Vad du byggde

**Resume → Job Fit Evaluator** - ett multi-agent hostat arbetsflöde som:
- Tar emot ett CV + en jobbannons via HTTP (`POST /responses`)
- Kör fyra specialiserade agenter i en sekventiell pipeline - varje agent vidarebefordrar data som dess efterföljare behöver
- Returnerar en matchningspoäng (0–100 med en uppdelning), en lista över kompetens- och certifieringsluckor, och en personlig lärandeplan med riktiga Microsoft Learn-länkar för varje lucka
- Anropar Microsoft Learn MCP-servern (`https://learn.microsoft.com/api/mcp`) för att hämta officiella lärresurser för varje identifierad kompetenslucka
- Körs som en enda containeriserad hostad agent i Microsoft Foundry Agent Service

---

## Viktiga begrepp som lärdes

| Begrepp | Vad du övade på |
|---------|-------------------|
| **Multi-agent orkestrering** | `WorkflowBuilder` sekventiell pipeline med `add_edge()` |
| **Agentspecialisering** | Fyra fokuserade agenter presterar bättre än en generalistagent |
| **Content Router-mönster** | ResumeParser fungerar även som en router - den bevarar JD-texten i en `[JOB DESCRIPTION PASS-THROUGH]`-sektion så att efterföljande agenter kan komma åt den (krävs eftersom `context_mode="last_agent"` innebär att endast `start_executor` ser det råa användarmeddelandet) |
| **Content Relay-mönster** | JD Agent vidarebefordrar `[PARSED RESUME PASS-THROUGH]` framåt så MatchingAgent får båda profilerna; undviker OR-semantikens dubbelutlösning som fan-in grafer orsakar |
| **MCP-verktygsintegration** | `@tool` + `streamable_http_client` som anropar en extern MCP-server |
| **Livscykel för hostad agent** | Scaffold → Konfigurera → Testa lokalt → Distribuera → Verifiera i molnet |
| **`context_mode="last_agent"`** | Varje exekutor ser endast sin direkta föregångares output |
| **Foundry Toolkit arbetsflöde** | Scaffold-guiden, Agent Inspector, Workflow Visualizer, ett-Klick-distribuera |

---

## Vad du slutförde

<details open>
<summary><strong>🅰️ Väg A - Foundry-abonnemang</strong></summary>

- [x] Verifierade Lab 01-installation: projekt, modell och RBAC fortfarande aktiva
- [x] Scaffoldade ett multi-agent projekt med Workflows-mallen
- [x] Skrev fyra agentinstruktionsuppsättningar (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrerade Microsoft Learn MCP-verktyget med `streamable_http_client`
- [x] Kopplade arbetsflödesgrafen med `WorkflowBuilder` (sekventiell pipeline med content relay)
- [x] Testade lokalt med 3 röktester (Agent Inspector) - matchningspoäng, luckkort och MCP-URL:er
- [x] Distribuerade till Foundry Agent Service (containeriserad, hanterad identitet)
- [x] Verifierade i molnets testmiljö - strukturell överensstämmelse med lokala resultat

</details>

<details open>
<summary><strong>🅱️ Väg B - Foundry Local</strong></summary>

- [x] Verifierade Lab 01-installation: Foundry Local körs med en lokal modell
- [x] Scaffoldade ett multi-agent projekt med Workflows-mallen
- [x] Skrev fyra agentinstruktionsuppsättningar och kopplade arbetsflödesgrafen
- [x] Integrerade Microsoft Learn MCP-verktyget
- [x] Testade lokalt med 3 röktester
- [x] Validerade multi-agent beteende utan behov av molnresurser

</details>

---

## Nästa steg

### Fortsätt lära dig

| Resurs | Beskrivning |
|----------|-------------|
| **[Agent Framework SDK-referens](https://learn.microsoft.com/agent-framework/)** | API-dokumentation för `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP-verktygskatalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Koppla agenter till andra MCP-servrar (Bing, GitHub, anpassade) |
| **[Lägg till kunskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Förankra agenter med dokument, vektorbutiker eller Bing-sökning |
| **[Foundry-utvärderingar](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mät agentkvalitet i stor skala med automatiserade utvärderare |
| **[Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fullständig plattformsreferens |
| **[Foundry Toolkit - Nyheter](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Versionsnoteringar och ändringslogg för tillägget |

### Idéer för att utöka detta arbetsflöde

- **Lägg till en 5:e agent** - En intervjucoach som skapar troliga intervjufrågor baserat på luckrapporten
- **Lägg till ett Bing-verktyg för förankring** - Låt JD Agent söka efter liknande jobbannonser för att berika kravspecifikationen
- **Koppla till en CV-databas** - Hämta kandidatprofiler från en databas via ett anpassat `@tool`
- **Testa olika modeller** - Jämför `gpt-4.1` och `gpt-4.1-mini` outputkvalitet och latens
- **Utvärdera med Foundry** - Använd funktionen Utvärderingar för att poängsätta matchningsrapporter mot en gulddataset

### För användare på Väg B: Uppgradera till molndistribution

När du är redo att distribuera till molnet:
1. Skaffa ett Azure-abonnemang ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Slutför [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (skapa projekt, distribuera modell, tilldela RBAC)
3. Uppdatera din `.env` med Foundry projekt-endpoint och modellens distributionsnamn
4. Fortsätt från [Modul 06 - Distribuera till Foundry](06-deploy-to-foundry.md)

---

## Rensa upp resurser (valfritt)

Om du vill ta bort de Azure-resurser som skapades under denna workshop:

### Alternativ 1: Radera resursgruppen (tar bort allting)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Alternativ 2: Radera endast den hostade agenten

1. Öppna [ai.azure.com](https://ai.azure.com) → ditt projekt → **Bygg** → **Agenter**.
2. Hitta **PersonalCareerCopilot** → klicka på **Radera**.

### Alternativ 3: Radera modellens distribution

1. I Foundry sidomeny, expandera ditt projekt → **Modeller**.
2. Högerklicka på modellens distribution → **Radera**.

> **Kostnadsnotis:** Hostade agenter genererar endast kostnad när de körs. Om du stoppar eller raderar agenten finns ingen löpande avgift. Modellens distribution kan generera en liten kostnad för reserverad kapacitet - radera den om du är klar.

---

**Föregående:** [08 - Felsökning](08-troubleshooting.md) · **Hem:** [Lab 02 README](../README.md) · [Workshop Hem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->