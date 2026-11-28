# Modul 9 - Oppsummering og neste steg

⏱️ ~5 min

**Gratulerer!** Du har bygget, testet, og (hvis på Sti A) distribuert en fleragent arbeidsflyt ved bruk av Microsoft Foundry og Foundry Toolkit for VS Code.

---

## Hva du bygde

**Resume → Job Fit Evaluator** - en fleragent vert arbeidsflyt som:
- Mottar en CV + stillingsbeskrivelse via HTTP (`POST /responses`)
- Kjører fire spesialiserte agenter i en sekvensiell pipeline - hver agent videresender data den neste trenger
- Returnerer en poengsum for match (0–100 med en detaljert oversikt), en liste over ferdighets- og sertifiseringsgap, og en personlig læringsplan med reelle Microsoft Learn-lenker for hvert gap
- Kaller Microsoft Learn MCP-serveren (`https://learn.microsoft.com/api/mcp`) for å hente offisielle læringsressurser for hvert identifisert ferdighetsgap
- Kjører som én enkelt containerisert vert-agent i Microsoft Foundry Agent Service

---

## Viktige konsepter lært

| Konsept | Hva du øvde på |
|---------|-------------------|
| **Fleragent orkestrering** | `WorkflowBuilder` sekvensiell pipeline med `add_edge()` |
| **Agentspesialisering** | Fire fokuserte agenter presterer bedre enn én generell agent |
| **Content Router-mønster** | ResumeParser fungerer også som en ruter - den bevarer JD-teksten i en `[JOB DESCRIPTION PASS-THROUGH]` seksjon slik at nedstrøms agenter kan få tilgang til den (nødvendig fordi `context_mode="last_agent"` betyr at kun `start_executor` ser den rå brukerbeskjeden) |
| **Content Relay-mønster** | JD Agent videresender `[PARSED RESUME PASS-THROUGH]` videre slik at MatchingAgent får begge profilene; unngår dobbel-trigger ved bruk av OR-semantikk som fan-in grafer ofte gir |
| **MCP verktøyintegrasjon** | `@tool` + `streamable_http_client` som kaller en ekstern MCP-server |
| **Vert Agent livssyklus** | Scaffold → Konfigurer → Test lokalt → Distribuer → Verifiser i skyen |
| **`context_mode="last_agent"`** | Hver executor ser kun utdataene fra sin direkte forgjenger |
| **Foundry Toolkit arbeidsflyt** | Scaffold-veiviser, Agentinspektør, Arbeidsflyt-visualisator, deploy med ett klikk |

---

## Hva du fullførte

<details open>
<summary><strong>🅰️ Sti A - Foundry abonnement</strong></summary>

- [x] Verifiserte Lab 01 oppsett: prosjekt, modell og RBAC fortsatt aktivt
- [x] Scaffoldet et fleragentprosjekt med Workflows-malen
- [x] Skrev fire agentinstruksjonssett (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrerte Microsoft Learn MCP-verktøyet med `streamable_http_client`
- [x] Koblede arbeidsflyt graf med `WorkflowBuilder` (sekvensiell pipeline med content relay)
- [x] Testet lokalt med 2 røyktester (Agentinspektør) - fit score, gap-kort, og MCP URL-er
- [x] Distribuerte til Foundry Agent Service (containerisert, administrert identitet)
- [x] Verifiserte i skyens lekeplass - strukturell samsvar med lokale resultater

</details>

<details open>
<summary><strong>🅱️ Sti B - Foundry Local</strong></summary>

- [x] Verifiserte Lab 01 oppsett: Foundry Local kjører med lokal modell
- [x] Scaffoldet et fleragentprosjekt med Workflows-malen
- [x] Skrev fire agentinstruksjonssett og koblet arbeidsflyt grafen
- [x] Integrerte Microsoft Learn MCP-verktøyet
- [x] Testet lokalt med 2 røyktester
- [x] Validerte fleragent oppførsel uten behov for skyressurser

</details>

---

## Neste steg

### Fortsett å lære

| Ressurs | Beskrivelse |
|----------|-------------|
| **[Agent Framework SDK referanse](https://learn.microsoft.com/agent-framework/)** | API-dokumentasjon for `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP verktøykatalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Koble agenter til andre MCP-servere (Bing, GitHub, tilpasset) |
| **[Legg til kunnskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Grunnfest agentene med dokumenter, vektorbutikker eller Bing-søk |
| **[Foundry Evalueringer](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mål agentkvalitet i stor skala med automatiske evalueringer |
| **[Microsoft Foundry dokumentasjon](https://learn.microsoft.com/azure/foundry/)** | Fullstendig plattformreferanse |
| **[Foundry Toolkit - Hva er nytt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Utgivelsesnotater og endringslogg for utvidelsen |

### Idéer for å utvide denne arbeidsflyten

- **Legg til en 5. agent** - En intervjutreningsagent som genererer sannsynlige intervjuspørsmål basert på gap-rapporten
- **Legg til et Bing-grunnlagsverktøy** - La JD Agent søke etter lignende stillingsannonser for å berike kravene
- **Koble til en CV-database** - Hent kandidatprofiler fra en database via en egendefinert `@tool`
- **Prøv ulike modeller** - Sammenlign `gpt-4.1` mot `gpt-4.1-mini` i output-kvalitet og latenstid
- **Evaluer med Foundry** - Bruk Evaluations-funksjonen til å score fit-rapporter mot et gullstandard datasett

### For Sti B brukere: Oppgrader til sky-distribusjon

Når du er klar til å distribuere i skyen:
1. Skaff et Azure-abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fullfør [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (opprett prosjekt, distribuer modell, tildel RBAC)
3. Oppdater `.env` med Foundry prosjektendepunkt og modell distribusjonsnavn
4. Fortsett fra [Modul 06 - Distribuer til Foundry](06-deploy-to-foundry.md)

---

## Rydd opp ressurser (valgfritt)

Hvis du vil fjerne Azure-ressursene som ble opprettet under denne workshopen:

### Valg 1: Slett ressursgruppen (fjerner alt)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Valg 2: Slett bare vertagenten

1. Åpne [ai.azure.com](https://ai.azure.com) → ditt prosjekt → **Bygg** → **Agenter**.
2. Finn **PersonalCareerCopilot** → klikk **Slett**.

### Valg 3: Slett modell distribusjonen

1. I Foundry sidepanelet, utvid prosjektet ditt → **Modeller**.
2. Høyreklikk på modell distribusjonen → **Slett**.

> **Kostnadsnotat:** Vertagenter påløper kun kostnader når de kjører. Hvis du stopper eller sletter agenten, påløper ingen løpende kostnad. Modell distribusjonen kan pålegge en liten avgift for reservert kapasitet – slett den hvis du er ferdig.

---

**Forrige:** [08 - Feilsøking](08-troubleshooting.md) · **Hjem:** [Lab 02 README](../README.md) · [Workshop Hjem](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->