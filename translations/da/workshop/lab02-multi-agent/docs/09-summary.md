# Modul 9 - Resumé & Næste skridt

⏱️ ~5 min

**Tillykke!** Du har bygget, testet, og (hvis på Sti A) deployeret en multi-agent workflow ved brug af Microsoft Foundry og Foundry Toolkit til VS Code.

---

## Hvad du har bygget

**Resume → Job Fit Evaluator** - en multi-agent hosted workflow som:
- Modtager et CV + jobbeskrivelse via HTTP (`POST /responses`)
- Kører fire specialiserede agenter i en sekventiel pipeline - hver agent sender data videre til sin efterfølger
- Returnerer en fit score (0–100 med opdeling), en liste over kompetence- og certificeringshuller, samt en personlig læringsplan med reelle Microsoft Learn links for hvert hul
- Kalder Microsoft Learn MCP-serveren (`https://learn.microsoft.com/api/mcp`) for at hente officielle læringsressourcer for hvert identificeret kompetencehul
- Kører som en enkelt containeriseret hosted agent i Microsoft Foundry Agent Service

---

## Nøglekoncepter lært

| Koncept | Hvad du har øvet |
|---------|-------------------|
| **Multi-agent orkestrering** | `WorkflowBuilder` sekventiel pipeline med `add_edge()` |
| **Agentspecialisering** | Fire fokuserede agenter overgår en enkelt generalistagent |
| **Content Router mønster** | ResumeParser fungerer også som en router - den bevarer JD-teksten i en `[JOB DESCRIPTION PASS-THROUGH]` sektion, så downstream agenter kan tilgå den (nødvendigt fordi `context_mode="last_agent"` betyder, at kun `start_executor` ser den rå brugerbesked) |
| **Content Relay mønster** | JD Agent sender `[PARSED RESUME PASS-THROUGH]` videre, så MatchingAgent får begge profiler; undgår OR-semantikkens dobbelt-trigger som fan-in grafer kan forårsage |
| **MCP værktøjsintegration** | `@tool` + `streamable_http_client` som kalder en ekstern MCP server |
| **Hosted Agent livscyklus** | Scaffold → Konfigurer → Test lokalt → Deploy → Verificer i skyen |
| **`context_mode="last_agent"`** | Hver executor ser kun output fra sin direkte forgænger |
| **Foundry Toolkit workflow** | Scaffold wizard, Agent Inspector, Workflow Visualizer, one-click deploy |

---

## Hvad du har færdiggjort

<details open>
<summary><strong>🅰️ Sti A - Foundry abonnement</strong></summary>

- [x] Verificeret Lab 01 setup: projekt, model, og RBAC stadig aktiv
- [x] Scaffoldet et multi-agent projekt ved brug af Workflows-skabelonen
- [x] Skrevet fire agent instruktioner (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integreret Microsoft Learn MCP værktøjet med `streamable_http_client`
- [x] Forbundet workflow graf med `WorkflowBuilder` (sekventiel pipeline med content relay)
- [x] Testet lokalt med 3 røggentest (Agent Inspector) - fit score, gap kort, og MCP URL’er
- [x] Deployeret til Foundry Agent Service (containeriseret, managed identity)
- [x] Verificeret i skylegeplads - strukturel konsistens med lokale resultater

</details>

<details open>
<summary><strong>🅱️ Sti B - Foundry Local</strong></summary>

- [x] Verificeret Lab 01 setup: Foundry Local kører med lokal model
- [x] Scaffoldet et multi-agent projekt med Workflows-skabelonen
- [x] Skrevet fire agent instruktioner og forbundet workflow graf
- [x] Integreret Microsoft Learn MCP værktøjet
- [x] Testet lokalt med 3 røggentest
- [x] Valideret multi-agent adfærd uden brug af skyeressourcer

</details>

---

## Næste skridt

### Fortsæt med at lære

| Ressource | Beskrivelse |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API-dokumentation for `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP værktøjskatalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Forbind agenter til andre MCP servere (Bing, GitHub, custom) |
| **[Tilføj viden (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Underbyg agenter med dokumenter, vektorlagre eller Bing-søgning |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mål agentkvalitet i stor skala med automatiserede evalueringer |
| **[Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fuld platformreference |
| **[Foundry Toolkit - Hvad er nyt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Udvidelsesudgivelsesnoter og ændringslog |

### Ideer til at forlænge denne workflow

- **Tilføj en 5. agent** - En interviewcoach, der genererer sandsynlige interviewspørgsmål baseret på gap-rapporten
- **Tilføj et Bing grounding værktøj** - Lad JD Agent søge efter lignende jobopslag for at berige kravene
- **Forbind til en CV-database** - Hent kandidatprofiler fra en database via et custom `@tool`
- **Prøv forskellige modeller** - Sammenlign outputkvalitet og latenstid for `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluer med Foundry** - Brug Evaluations funktion til at score fit rapporter mod et guld-standard datasæt

### For brugere på Sti B: Opgrader til cloud deployment

Når du er klar til at deployere til skyen:
1. Få et Azure abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fuldfør [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (opret projekt, deploy model, tildel RBAC)
3. Opdater din `.env` med Foundry projekt-endpoint og model deployment navn
4. Fortsæt fra [Modul 06 - Deploy til Foundry](06-deploy-to-foundry.md)

---

## Ryd op i ressourcer (valgfrit)

Hvis du ønsker at fjerne Azure ressourcer oprettet under workshoppen:

### Mulighed 1: Slet resource gruppen (fjerner alt)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Mulighed 2: Slet kun den hosted agent

1. Åbn [ai.azure.com](https://ai.azure.com) → dit projekt → **Build** → **Agents**.
2. Find **PersonalCareerCopilot** → klik **Delete**.

### Mulighed 3: Slet model deployment

1. I Foundry sidemenuen, udvid dit projekt → **Models**.
2. Højreklik på model deployment → **Delete**.

> **Omkostningsnote:** Hosted agenter koster kun, når de kører. Hvis du stopper eller sletter agenten, er der ingen løbende omkostning. Model deployment kan medføre en lille omkostning for reserveret kapacitet – slet den, hvis du er færdig.

---

**Forrige:** [08 - Fejlfinding](08-troubleshooting.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->