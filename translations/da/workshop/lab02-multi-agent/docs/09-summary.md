# Modul 9 - Opsummering & Næste Skridt

⏱️ ~5 min

**Tillykke!** Du har bygget, testet og (hvis på Sti A) implementeret en multi-agent arbejdsgang ved brug af Microsoft Foundry og Foundry Toolkit til VS Code.

---

## Hvad du har bygget

**Resume → Job Fit Evaluator** - en multi-agent hostet arbejdsgang, der:
- Modtager et CV + jobbeskrivelse via HTTP (`POST /responses`)
- Kører fire specialiserede agenter i en sekventiel pipeline - hver agent sender de data videre, som dens efterfølger har brug for
- Returnerer en fit score (0–100 med en opdeling), en liste over færdigheds- og certificeringsmangler, samt en personlig læringsplan med ægte Microsoft Learn links for hver mangel
- Kalder Microsoft Learn MCP serveren (`https://learn.microsoft.com/api/mcp`) for at hente officielle læringsressourcer for hver identificeret færdighedsmangel
- Kører som en enkelt containeriseret hostet agent i Microsoft Foundry Agent Service

---

## Vigtige begreber lært

| Begreb | Hvad du øvede |
|---------|-------------------|
| **Multi-agent orkestrering** | `WorkflowBuilder` sekventiel pipeline med `add_edge()` |
| **Agent specialisering** | Fire fokuserede agenter klarer sig bedre end én general purpose agent |
| **Content Router mønster** | ResumeParser fungerer også som router - den bevarer JD-teksten i en `[JOB DESCRIPTION PASS-THROUGH]` sektion så efterfølgende agenter kan få adgang til den (nødvendigt fordi `context_mode="last_agent"` betyder at kun `start_executor` ser den rå brugermeddelelse) |
| **Content Relay mønster** | JD Agent sender `[PARSED RESUME PASS-THROUGH]` fremad så MatchingAgent får begge profiler; undgår OR-semantik dobbelt-trigger som fan-in grafer forårsager |
| **MCP værktøjsintegration** | `@tool` + `streamable_http_client` kalder en ekstern MCP server |
| **Hosted Agent livscyklus** | Scaffold → Konfigurer → Test lokalt → Implementer → Verificer i skyen |
| **`context_mode="last_agent"`** | Hver executor ser kun output fra sin direkte forgænger |
| **Foundry Toolkit arbejdsgang** | Scaffold wizard, Agent Inspector, Workflow Visualizer, one-click deploy |

---

## Hvad du har gennemført

<details open>
<summary><strong>🅰️ Sti A - Foundry abonnement</strong></summary>

- [x] Bekræftede Lab 01 setup: projekt, model og RBAC stadig aktivt
- [x] Scaffoldede et multi-agent projekt ved brug af Workflows skabelonen
- [x] Skrev fire agent instruktioner (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrerede Microsoft Learn MCP værktøjet med `streamable_http_client`
- [x] Forbundne workflow grafen med `WorkflowBuilder` (sekventiel pipeline med content relay)
- [x] Testede lokalt med 2 smoke tests (Agent Inspector) - fit score, gap kort og MCP URL'er
- [x] Implementerede i Foundry Agent Service (containeriseret, managed identity)
- [x] Bekræftede i cloud playground - strukturel konsistens med lokale resultater

</details>

<details open>
<summary><strong>🅱️ Sti B - Foundry Local</strong></summary>

- [x] Bekræftede Lab 01 setup: Foundry Local kører med en lokal model
- [x] Scaffoldede et multi-agent projekt ved brug af Workflows skabelonen
- [x] Skrev fire agent instruktioner og forbandt workflow grafen
- [x] Integrerede Microsoft Learn MCP værktøjet
- [x] Testede lokalt med 2 smoke tests
- [x] Validerede multi-agent adfærd uden behov for skyressourcer

</details>

---

## Næste skridt

### Fortsæt læringen

| Resurse | Beskrivelse |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API dokumentation for `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool katalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Forbind agenter til andre MCP servere (Bing, GitHub, custom) |
| **[Tilføj viden (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ground agenter med dokumenter, vektorlager eller Bing-søgning |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mål agentkvalitet i stor skala med automatiserede evaluatorer |
| **[Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fuldt platformreferat |
| **[Foundry Toolkit - Hvad er nyt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Udvidelsesudgivelsesnoter og changelog |

### Ideer til at udvide denne arbejdsgang

- **Tilføj en 5. agent** - En interview coach der genererer sandsynlige interviewspørgsmål baseret på gapanalysen
- **Tilføj et Bing groundingsværktøj** - Lad JD Agent søge efter lignende jobannoncer for at berige kravene
- **Forbind til en CV-database** - Hent kandidatprofiler fra en database via en custom `@tool`
- **Prøv forskellige modeller** - Sammenlign outputkvalitet og latenstid for `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluer med Foundry** - Brug Evaluations-funktionen til at score fit-rapporter mod et guld-datasæt

### For Sti B brugere: Opgrader til cloud-implementering

Når du er klar til at implementere til skyen:
1. Få et Azure abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Gennemfør [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (opret projekt, implementer model, tildel RBAC)
3. Opdater din `.env` med Foundry-projektendepunktet og modelimplementeringsnavnet
4. Fortsæt fra [Modul 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Ryd op i ressourcer (valgfrit)

Hvis du vil fjerne Azure-ressourcerne oprettet under denne workshop:

### Mulighed 1: Slet resourcegruppen (fjerner alt)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Mulighed 2: Slet kun den hostede agent

1. Åbn [ai.azure.com](https://ai.azure.com) → dit projekt → **Build** → **Agents**.
2. Find **PersonalCareerCopilot** → klik **Delete**.

### Mulighed 3: Slet modelimplementeringen

1. I Foundry sidebar, udvid dit projekt → **Models**.
2. Højreklik på modelimplementeringen → **Delete**.

> **Omkostningsnote:** Hostede agenter påfører kun omkostninger når de kører. Hvis du stopper eller sletter agenten, er der ingen løbende omkostninger. Modelimplementeringen kan påføre en lille udgift for reserveret kapacitet - slet den hvis du er færdig.

---

**Forrige:** [08 - Fejlfinding](08-troubleshooting.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->