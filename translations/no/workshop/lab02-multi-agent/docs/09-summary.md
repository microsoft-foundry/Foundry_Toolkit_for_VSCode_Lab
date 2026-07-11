# Modul 9 - Oppsummering og neste steg

⏱️ ~5 min

**Gratulerer!** Du har bygget, testet og (hvis på Sti A) distribuert en multi-agent arbeidsflyt ved hjelp av Microsoft Foundry og Foundry Toolkit for VS Code.

---

## Det du bygde

**CV → Jobbtilpasningsevaluerer** – en multi-agent hostet arbeidsflyt som:
- Mottar en CV + stillingsbeskrivelse via HTTP (`POST /responses`)
- Kjører fire spesialiserte agenter i en sekvensiell pipeline – hver agent sender data videre som etterfølgeren trenger
- Returnerer en tilpasningsscore (0–100 med detaljert nedbrytning), en liste over ferdigheter og sertifikatgap, samt en personlig læringsplan med ekte Microsoft Learn-lenker for hvert gap
- Kaller Microsoft Learn MCP-serveren (`https://learn.microsoft.com/api/mcp`) for å hente offisielle læringsressurser for hvert identifisert ferdighetsgap
- Kjører som en enkelt containerisert hostet agent i Microsoft Foundry Agent Service

---

## Viktige konsepter lært

| Konsept | Hva du praktiserte |
|---------|-------------------|
| **Multi-agent orkestrering** | `WorkflowBuilder` sekvensiell pipeline med `add_edge()` |
| **Agentspesialisering** | Fire fokuserte agenter gir bedre resultater enn én allmenn-agent |
| **Content Router-mønster** | ResumeParser fungerer også som en ruter – den bevarer JD-teksten i en `[JOB DESCRIPTION PASS-THROUGH]`-seksjon slik at nedstrøms agenter kan få tilgang til den (nødvendig fordi `context_mode="last_agent"` betyr at bare `start_executor` ser den rå brukerbeskjeden) |
| **Content Relay-mønster** | JD Agent sender `[PARSED RESUME PASS-THROUGH]` videre slik at MatchingAgent får begge profiler; unngår OR-semantikkens dobbelutløsing som fan-in grafer kan medføre |
| **MCP verktøyintegrasjon** | `@tool` + `streamable_http_client` som kaller en ekstern MCP-server |
| **Hosted Agent livssyklus** | Scaffold → Konfigurer → Lokal testing → Distribuer → Verifiser i skyen |
| **`context_mode="last_agent"`** | Hver executor ser kun output fra sin direkte forgjenger |
| **Foundry Toolkit arbeidsflyt** | Scaffold-veiviser, Agentinspektør, Arbeidsflytsvisualisering, ett-klikk distribusjon |

---

## Det du fullførte

<details open>
<summary><strong>🅰️ Sti A - Foundry abonnement</strong></summary>

- [x] Verifiserte Lab 01-oppsett: prosjekt, modell og RBAC fortsatt aktiv
- [x] Scaffoldet et multi-agent prosjekt med Workflows-mal
- [x] Skrev fire agent instruksjonssett (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrerte Microsoft Learn MCP-verktøy med `streamable_http_client`
- [x] Koblede arbeidsflyt grafen med `WorkflowBuilder` (sekvensiell pipeline med content relay)
- [x] Testet lokalt med 3 røyktester (Agent Inspector) – tilpasningsscore, gapkort, og MCP-URLer
- [x] Distribuerte til Foundry Agent Service (containerisert, administrert identitet)
- [x] Verifiserte i sky playground – strukturell konsistens med lokale resultater

</details>

<details open>
<summary><strong>🅱️ Sti B - Foundry Local</strong></summary>

- [x] Verifiserte Lab 01-oppsett: Foundry Local kjører med lokal modell
- [x] Scaffoldet et multi-agent prosjekt med Workflows-mal
- [x] Skrev fire agent instruksjonssett og koblet arbeidsflyt grafen
- [x] Integrerte Microsoft Learn MCP-verktøy
- [x] Testet lokalt med 3 røyktester
- [x] Validerte multi-agent atferd uten behov for skytjenester

</details>

---

## Neste steg

### Fortsett å lære

| Ressurs | Beskrivelse |
|----------|-------------|
| **[Agent Framework SDK referanse](https://learn.microsoft.com/agent-framework/)** | API-dokumentasjon for `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP verktøykatalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Koble agenter til andre MCP-servere (Bing, GitHub, egendefinert) |
| **[Legg til kunnskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Forankre agenter med dokumenter, vektorbutikker eller Bing-søk |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mål agentkvalitet i stor skala med automatiserte evalueringer |
| **[Microsoft Foundry dokumentasjon](https://learn.microsoft.com/azure/foundry/)** | Full plattformreferanse |
| **[Foundry Toolkit - Hva er nytt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Utvidelsesutgivelsesnotater og endringslogg |

### Idéer for å utvide denne arbeidsflyten

- **Legg til en 5. agent** – En intervjukoach som produserer sannsynlige intervjuspørsmål basert på gaprapporten
- **Legg til et Bing forankringsverktøy** – La JD Agent søke etter lignende stillingsannonser for å berike kravene
- **Koble til en CV-database** – Hent kandidatprofiler fra en database via et egendefinert `@tool`
- **Prøv forskjellige modeller** – Sammenlign `gpt-4.1` vs. `gpt-4.1-mini` output kvalitet og ventetid
- **Evaluer med Foundry** – Bruk Evaluations-funksjonen for å score tilpasningsrapporter mot et gullstandard datasett

### For brukere av Sti B: Oppgrader til sky-distribusjon

Når du er klar til å distribuere til skyen:
1. Skaff et Azure-abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fullfør [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (opprett prosjekt, distribuer modell, tildel RBAC)
3. Oppdater din `.env` med Foundry prosjektendepunkt og modell distribusjonsnavn
4. Fortsett fra [Modul 06 – Distribuer til Foundry](06-deploy-to-foundry.md)

---

## Rydd opp ressurser (valgfritt)

Hvis du vil fjerne Azure-ressursene som ble opprettet under denne workshopen:

### Alternativ 1: Slett ressursgruppen (fjerner alt)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Alternativ 2: Slett bare den hostede agenten

1. Åpne [ai.azure.com](https://ai.azure.com) → ditt prosjekt → **Build** → **Agents**.
2. Finn **PersonalCareerCopilot** → klikk **Delete**.

### Alternativ 3: Slett modell distribusjonen

1. I Foundry sidepanelet, utvid prosjektet ditt → **Models**.
2. Høyreklikk modell distribusjonen → **Delete**.

> **Kostnadsnotat:** Hostede agenter påfører kostnad kun når de kjører. Hvis du stopper eller sletter agenten, er det ingen løpende kostnad. Modell distribusjonen kan påføre en liten kostnad for reservert kapasitet – slett den hvis du er ferdig.

---

**Forrige:** [08 - Feilsøking](08-troubleshooting.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->