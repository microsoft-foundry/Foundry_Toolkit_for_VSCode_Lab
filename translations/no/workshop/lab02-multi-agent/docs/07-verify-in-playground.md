# Modul 7 - Verifiser i Playground

⏱️ ~10 min

I denne modulen tester du din distribuerte multi-agent arbeidsflyt i VS Code og Foundry Portal, og bekrefter at agenten oppfører seg likt som under lokal testing.

---

## Hvorfor teste på nytt etter distribusjon?

Det hostede miljøet skiller seg fra lokalt på noen viktige måter:

| | Lokalt | Hostet |
|--|-------|--------|
| **Identitet** | Din personlige pålogging (`DefaultAzureCredential`) | Dedikert per-agent Entra-identitet (auto-provisionert ved distribusjon) |
| **Endepunkt** | `http://localhost:8088/responses` | Foundry Agent Service administrert URL |
| **Nettverk** | Din maskin → Azure OpenAI + MCP | Azure ryggrad (lavere ventetid) |

En feilkonfigurert miljøvariabel, RBAC-problem, eller blokkert MCP utgående kall vil først dukke opp her.

---

## Alternativ A: Test i VS Code Playground (anbefalt først)

### Trinn 1: Naviger til din hostede agent

1. Klikk på **Foundry Toolkit**-ikonet i Aktivitetslinjen.
2. Utvid prosjektet ditt → **Hosted Agents (Preview)** → finn agenten din.

![Foundry Toolkit sidebar showing Hosted Agents (Preview) with resume-job-fit-evaluator and its deployed versions](../../../../../translated_images/no/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Trinn 2: Velg en versjon

1. Klikk på agenten for å utvide dens versjoner.
2. Klikk `v1` → bekreft at status er **aktiv** (sidebaren kan vise "Running" eller "Started" - begge indikerer samme klare tilstand).

### Trinn 3: Åpne Playground

1. Klikk **Playground** (eller høyreklikk versjon → **Open in Playground**).
2. Et chatte-vindu åpnes i en VS Code-fane.

### Trinn 4: Kjør dine smoketester

Bruk de samme 3 testene fra [Modul 5](05-test-locally.md). Skriv hver melding i Playground input-boksen og trykk **Send** (eller **Enter**).

#### Test 1 - Full CV + stillingsbeskrivelse (standardflyt)

Lim inn den fullstendige CV + stillingsbeskrivelse-prompten fra Modul 5, Test 1 (Jane Doe + Senior Cloud Engineer hos Contoso Ltd).

**Forventet:**
- Passformpoeng med detaljert utregning (100-poengs skala)
- Matchede ferdigheter seksjon
- Manglende ferdigheter seksjon
- **Ett gap-kort per manglende ferdighet** med Microsoft Learn URLer
- Læringsplan med tidslinje

#### Test 2 - Rask kort test (minimal input)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Forventet:**
- Lavere passformpoeng (< 40)
- Ærlig vurdering med trinnvis læringsvei
- Flere gap-kort (AWS, Kubernetes, Terraform, CI/CD, erfaring gap)

#### Test 3 - Høy passform kandidat

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Forventet:**
- Høyt passformpoeng (≥ 80)
- Fokus på intervjuberedskap og finpussing
- Få eller ingen gap-kort
- Kort tidslinje med fokus på forberedelse

### Trinn 5: Sammenlign med lokale resultater

Åpne dine notater eller nettleserfane fra Modul 5 hvor du lagret lokale svar. For hver test:

- Har svaret **samme struktur** (passformpoeng, gap-kort, læringsplan)?
- Følger det **samme poengsystem** (100-poengs oppdeling)?
- Er **Microsoft Learn URLer** fortsatt til stede i gap-kortene?
- Er det **ett gap-kort per manglende ferdighet** (ikke avkortet)?

> **Små ordvalgsforskjeller er normalt** - modellen er ikke-deterministisk. Fokuser på struktur, poengkonsistens, og bruk av MCP-verktøy.

---

## Alternativ B: Test i Foundry Portal

[Foundry Portal](https://ai.azure.com) tilbyr en nettbasert playground som er nyttig for deling med kolleger eller interessenter.

### Trinn 1: Åpne Foundry Portal

1. Åpne nettleseren og gå til [https://ai.azure.com](https://ai.azure.com).
2. Logg på med samme Azure-konto som du har brukt gjennom hele workshoppen.

### Trinn 2: Naviger til prosjektet ditt

1. På startsiden, se etter **Recent projects** i venstre sidemeny.
2. Klikk på prosjektnavnet ditt (f.eks. `workshop-agents`).
3. Hvis du ikke ser det, klikk **All projects** og søk etter det.

### Trinn 3: Finn din distribuerte agent

1. I prosjektets venstremeny, klikk **Build** → **Agents** (eller se etter **Agents**-seksjonen).
2. Du bør se en liste over agenter. Finn din distribuerte agent (f.eks. `resume-job-fit-evaluator`).
3. Klikk på agentnavnet for å åpne detaljsiden.

### Trinn 4: Åpne Playground

1. På agentens detaljside, se øverst i verktøylinjen.
2. Klikk **Open in playground** (eller **Try in playground**).
3. En chat-grensesnitt åpnes.

### Trinn 5: Kjør de samme smoketestene

Gjenta alle 3 testene fra VS Code Playground seksjonen over. Sammenlign hvert svar med både lokale resultater (Modul 5) og VS Code Playground resultater (Alternativ A ovenfor).

---

## Multi-agent spesifikk verifisering

Utover grunnleggende korrekthet, verifiser disse multi-agent-spesifikke oppførslene:

### MCP verktøykjøring

| Sjekk | Hvordan verifisere | Godkjenningsbetingelse |
|-------|---------------|----------------|
| MCP-kall lykkes | Gap-kort inneholder `learn.microsoft.com` URLer | Ekte URLer, ikke fallback-meldinger |
| Flere MCP-kall | Hvert High/Medium prioriterte gap har ressurser | Ikke bare det første gap-kortet |
| MCP fallback fungerer | Hvis URLer mangler, sjekk for fallback-tekst | Agenten produserer fortsatt gap-kort (med eller uten URLer) |

### Agent-koordinering

| Sjekk | Hvordan verifisere | Godkjenningsbetingelse |
|-------|---------------|----------------|
| Alle 4 agenter kjørte | Output inneholder passformpoeng OG gap-kort | Poeng fra MatchingAgent, kort fra GapAnalyzer |
| Sekvensiell kjøring | Responstid er rimelig (< 2 min) | Hvis > 3 min, sjekk for feil i terminalloggen |
| Dataintegritet | Gap-kort refererer ferdigheter fra matching-rapporten | Ingen hallusinerte ferdigheter som ikke er i stillingsbeskrivelsen |

---

## Valideringsrubrikk

Bruk denne rubrikken til å evaluere multi-agent arbeidsflytens hostede oppførsel:

| # | Kriterium | Godkjenningsbetingelse | Godkjent? |
|---|----------|---------------|-------|
| 1 | **Funksjonell korrekthet** | Agent svarer på CV + stillingsbeskrivelse med passformpoeng og gap-analyse | |
| 2 | **Poengkonsistens** | Passformpoeng bruker 100-poengs skala med detaljert utregning | |
| 3 | **Gap-kort fullstendighet** | Ett kort per manglende ferdighet (ikke avkortet eller kombinert) | |
| 4 | **MCP verktøyintegrasjon** | Gap-kort inkluderer ekte Microsoft Learn URLer | |
| 5 | **Strukturell konsistens** | Output-strukturen matcher mellom lokale og hostede kjøringer | |
| 6 | **Responstid** | Hostet agent svarer innen 2 minutter for full vurdering | |
| 7 | **Ingen feil** | Ingen HTTP 500-feil, tidsavbrudd eller tomme svar | |

> En "godkjent" betyr at alle 7 kriteriene er oppfylt for alle 3 smoketester i minst en playground (VS Code eller Portal).

---

## Feilsøking av playground-problemer

| Symptom | Sannsynlig årsak | Løsning |
|---------|-------------|-----|
| Playground lastes ikke | Container ikke i `active` status | Gå tilbake til [Modul 6](06-deploy-to-foundry.md), sjekk distribusjonsstatus. Vent om `creating` |
| Agent returnerer tomt svar | Modell distribusjonsnavn samsvarer ikke | Sjekk `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` samsvarer med din distribuerte modell |
| Agent returnerer feilmelding | Manglende [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) tillatelse | Tildel **[Foundry User](https://aka.ms/foundry-ext-project-role)** (tidligere Azure AI User) på prosjektomfang |
| Ingen Microsoft Learn URLer i gap-kort | MCP utgående blokkert eller MCP-server utilgjengelig | Sjekk om container kan nå `learn.microsoft.com`. Se [Modul 8](08-troubleshooting.md) |
| Bare 1 gap-kort (avkortet) | Manglende "CRITICAL" blokk i GapAnalyzer instruksjoner | Gå gjennom [Modul 3, Trinn 2.4](03-configure-agents.md) |
| Passformpoeng veldig forskjellig fra lokalt | Annen modell eller instruksjoner distribuert | Sammenlign `agent.yaml` miljøvariabler med lokal `.env`. Distribuer på nytt om nødvendig |
| "Agent ikke funnet" i Portal | Distribusjonen holder på å propagere eller feilet | Vent 2 minutter, oppdater. Hvis fortsatt mangler, distribuer på nytt fra [Modul 6](06-deploy-to-foundry.md) |

---

### Sjekkpunkter

- [ ] Testet agent i VS Code Playground - alle 3 smoketester bestått
- [ ] Testet agent i [Foundry Portal](https://ai.azure.com) Playground - alle 3 smoketester bestått
- [ ] Svarene er strukturelt konsistente med lokal testing (passformpoeng, gap-kort, læringsplan)
- [ ] Microsoft Learn URLer er til stede i gap-kort (MCP-verktøy fungerer i hostet miljø)
- [ ] Ett gap-kort per manglende ferdighet (ingen avkortning)
- [ ] Ingen feil eller tidsavbrudd under testing
- [ ] Fullført valideringsrubrikk (alle 7 kriterier bestått)

---

**Forrige:** [06 - Distribuer til Foundry](06-deploy-to-foundry.md) · **Neste:** [08 - Feilsøking →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->