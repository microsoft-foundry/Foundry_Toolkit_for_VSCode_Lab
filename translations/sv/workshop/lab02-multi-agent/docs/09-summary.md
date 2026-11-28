# Modul 9 - Sammanfattning & Nästa steg

⏱️ ~5 min

**Grattis!** Du har byggt, testat och (om du följer Väg A) distribuerat ett multi-agent-arbetsflöde med Microsoft Foundry och Foundry Toolkit för VS Code.

---

## Vad du byggde

**Resume → Job Fit Evaluator** - ett multi-agent-hostat arbetsflöde som:
- Tar emot ett CV + jobbprofil via HTTP (`POST /responses`)
- Kör fyra specialiserade agenter i en sekventiell pipeline - varje agent vidarebefordrar data som nästa agent behöver
- Returnerar en passande poäng (0–100 med en uppdelning), en lista över kompetens- och certifieringsgap samt en personlig lärandeplan med riktiga Microsoft Learn-länkar för varje gap
- Anropar Microsoft Learn MCP-servern (`https://learn.microsoft.com/api/mcp`) för att hämta officiella läranderesurser för varje identifierat kompetensgap
- Körs som en enda containeriserad hostad agent i Microsoft Foundry Agent Service

---

## Nyckelkoncept som lärts

| Koncept | Vad du tränade på |
|---------|--------------------|
| **Multi-agent orkestrering** | `WorkflowBuilder` sekventiell pipeline med `add_edge()` |
| **Agentspecialisering** | Fyra fokuserade agenter överträffar en allmän agent |
| **Content Router-mönster** | ResumeParser fungerar också som router - den bevarar jobbprofiltexten i en `[JOB DESCRIPTION PASS-THROUGH]`-sektion så att efterföljande agenter kan komma åt den (krävs eftersom `context_mode="last_agent"` innebär att endast `start_executor` ser det råa användarmeddelandet) |
| **Content Relay-mönster** | JD Agent vidarebefordrar `[PARSED RESUME PASS-THROUGH]` så att MatchingAgent får båda profilerna; undviker OR-semantikens dubbla triggereffekt som fan-in-diagram orsakar |
| **MCP-verktygsintegration** | `@tool` + `streamable_http_client` som anropar en extern MCP-server |
| **Hosted Agent-livscykel** | Scaffold → Konfigurera → Testa lokalt → Distribuera → Verifiera i molnet |
| **`context_mode="last_agent"`** | Varje exekverare ser bara sin direkta föregångares output |
| **Foundry Toolkit arbetsflöde** | Scaffold-guide, Agent Inspector, Workflow Visualizer, ett-klicks distribution |

---

## Vad du slutförde

<details open>
<summary><strong>🅰️ Väg A - Foundry-abonnemang</strong></summary>

- [x] Verifierade Lab 01-setup: projekt, modell och RBAC fortfarande aktiva
- [x] Scaffoldade ett multi-agent-projekt med Workflows-mallen
- [x] Skrev fyra agentinstruktionsuppsättningar (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrerade Microsoft Learn MCP-verktyget med `streamable_http_client`
- [x] Kopplade arbetsflödesgrafen med `WorkflowBuilder` (sekventiell pipeline med content relay)
- [x] Testade lokalt med 2 smoke-tester (Agent Inspector) - passpoäng, gap-kort och MCP-URL:er
- [x] Distribuerade till Foundry Agent Service (containeriserad, managed identity)
- [x] Verifierade i molnets playground - strukturell konsistens med lokala resultat

</details>

<details open>
<summary><strong>🅱️ Väg B - Foundry Local</strong></summary>

- [x] Verifierade Lab 01-setup: Foundry Local körs med lokal modell
- [x] Scaffoldade ett multi-agent-projekt med Workflows-mallen
- [x] Skrev fyra agentinstruktionsuppsättningar och kopplade arbetsflödesgrafen
- [x] Integrerade Microsoft Learn MCP-verktyget
- [x] Testade lokalt med 2 smoke-tester
- [x] Validerade multi-agentbeteende utan behov av molnresurser

</details>

---

## Nästa steg

### Fortsätt lära dig

| Resurs | Beskrivning |
|----------|-------------|
| **[Agent Framework SDK referens](https://learn.microsoft.com/agent-framework/)** | API-dokumentation för `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP verktygskatalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Koppla agenter till andra MCP-servrar (Bing, GitHub, anpassad) |
| **[Lägg till kunskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ge agenter grund med dokument, vektorlagringar eller Bing-sökning |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mät agentkvalitet i stor skala med automatiserade evaluatorer |
| **[Microsoft Foundry-dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fullständig plattformsreferens |
| **[Foundry Toolkit - Vad är nytt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Tilläggens versionsanteckningar och changelog |

### Idéer för att utöka detta arbetsflöde

- **Lägg till en 5:e agent** - En intervjucoach som producerar sannolika intervjufrågor baserade på gap-rapporten
- **Lägg till ett Bing-grundverktyg** - Låt JD Agent söka efter liknande jobbannonser för att berika kravspecifikationen
- **Koppla till en CV-databas** - Hämta kandidatprofiler från en databas via en anpassad `@tool`
- **Testa olika modeller** - Jämför `gpt-4.1` och `gpt-4.1-mini` output-kvalitet och latens
- **Utvärdera med Foundry** - Använd Evaluations-funktionen för att poängsätta passningsrapporter mot en gyllene dataset

### För användare på Väg B: Uppgradera till molndistribution

När du är redo att distribuera i molnet:
1. Skaffa en Azure-prenumeration ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Slutför [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (skapa projekt, distribuera modell, tilldela RBAC)
3. Uppdatera din `.env` med Foundry-projektets endpoint och modellens distributionsnamn
4. Fortsätt från [Modul 06 - Distribuera till Foundry](06-deploy-to-foundry.md)

---

## Rensa upp resurser (frivilligt)

Om du vill ta bort Azure-resurserna som skapades under denna workshop:

### Alternativ 1: Ta bort resursgruppen (tar bort allt)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Alternativ 2: Ta bara bort den hostade agenten

1. Öppna [ai.azure.com](https://ai.azure.com) → ditt projekt → **Build** → **Agents**.
2. Hitta **PersonalCareerCopilot** → klicka **Delete**.

### Alternativ 3: Ta bort modellens distribution

1. I Foundry-sidofältet, expandera ditt projekt → **Models**.
2. Högerklicka på modellens distribution → **Delete**.

> **Kostnadsnotering:** Hostade agenter kostar bara när de körs. Om du stoppar eller tar bort agenten, finns ingen pågående kostnad. Modellens distribution kan medföra en liten kostnad för reserverad kapacitet - ta bort den om du är klar.

---

**Föregående:** [08 - Felsökning](08-troubleshooting.md) · **Hem:** [Lab 02 README](../README.md) · [Workshop Hem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->