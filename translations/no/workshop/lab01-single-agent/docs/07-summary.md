# Modul 7 - Sammendrag og neste steg

⏱️ ~5 min

**Gratulerer!** Du har bygget, testet, og (hvis på vei A) distribuert en hostet AI-agent ved bruk av Microsoft Foundry og Foundry Toolkit for VS Code.

---

## Hva du bygde

En **"Forklar som om jeg er en leder"**-agent som:
- Mottar tekniske hendelsesrapporter eller driftsoppdateringer via HTTP (`POST /responses`)
- Oversetter dem til lettfattelige lederoppsummeringer
- Følger et strukturert utdataformat (Hva skjedde / Forretningspåvirkning / Neste steg)
- Avviser irrelevante forespørsler og forsøk på prompt-injeksjon
- Kjører som en containerisert hostet agent i Microsoft Foundry Agent Service

---

## Viktige konsepter lært

| Konsept | Hva du praktiserte |
|---------|-------------------|
| **Agent Framework-arkitektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Lifecycle for hostet agent** | Scaffold → Konfigurer → Test lokalt → Distribuer → Verifiser i skyen |
| **System prompt-utforming** | Rolle, målgruppe, utdataformat, regler, sikkerhetsbegrensninger og eksempler |
| **Forskjeller mellom lokal og hostet** | Identitet (personlig legitimasjon vs. administrert identitet), endepunkt, nettverksvei |
| **Sikkerhetsgrenser** | Forsvar mot prompt-injeksjon, rolleoverholdelse, elegant håndtering av kanttilfeller |
| **Foundry Toolkit arbeidsflyt** | Prosjektopprettelse, modellutplassering, agentskjelett, Agent Inspector, ett-klikk distribusjon |

---

## Hva du fullførte

### Vei A (Foundry abonnement)

- [x] Satte opp Foundry Toolkit og opprettet et Foundry-prosjekt med distribuert modell
- [x] Scaffoldet en hostet agent med autogenerert prosjektstruktur
- [x] Skrev strukturerte agentinstruksjoner med sikkerhetsregler
- [x] Testet lokalt med 3 funksjonelle scenarioer (Agent Inspector)
- [x] Distribuerte til Foundry Agent Service (containerisert)
- [x] Verifiserte i skyens lekeplass med 4 kant-/sikkerhetstester

### Vei B (Foundry Local)

- [x] Satte opp Foundry Toolkit med et lokalt model-endepunkt
- [x] Scaffoldet et prosjekt for hostet agent
- [x] Skrev strukturerte agentinstruksjoner med sikkerhetsregler
- [x] Testet lokalt med 3 funksjonelle scenarioer
- [x] Validerte agentens oppførsel uten behov for skyressurser

---

## Neste steg

### Fortsett å lære

| Ressurs | Beskrivelse |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Bygg en 4-agent arbeidsflyt (CV → Jobbanalyse) med orkestreringsmønstre |
| **[Legg til verktøy i agenten din](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Koble til APIer, databaser eller egendefinerte funksjoner via Tool Catalog |
| **[Legg til kunnskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Forankre agenten med dokumenter, vektorlager eller Bing-søk |
| **[Microsoft Foundry dokumentasjon](https://learn.microsoft.com/azure/foundry/)** | Full plattformreferanse |
| **[Agent Framework SDK-referanse](https://learn.microsoft.com/agent-framework/)** | API-dokumentasjon for `agent-framework`-pakken |
| **[Foundry Toolkit - Hva er nytt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Utvidelsesutgivelsesnotater og endringslogg |

### Ideer for å utvide agenten din

- **Legg til et datoverktøy** - La agenten inkludere "per dags dato"-kontekst i oppsummeringer
- **Koble til en hendelsesdatabase** - Hent reelle hendelsesdetaljer via en verktøyfunksjon
- **Legg til et Bing-forankringsverktøy** - La agenten søke etter siste nytt for ekstra kontekst
- **Prøv forskjellige modeller** - Sammenlign `gpt-4.1` vs. `gpt-4.1-mini` utdata-kvalitet
- **Evaluer med Foundry** - Bruk Evaluations-funksjonen for å måle agentkvalitet i stor skala

### For brukere av vei B: Oppgrader til distribusjon i skyen

Når du er klar til å distribuere til skyen:
1. Skaff et Azure-abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fullfør [Modul 01, Oppsett](01-setup.md#step-2-set-up-based-on-your-access) (opprett prosjekt, distribuer modell, tilordne RBAC)
3. Oppdater din `.env` med Foundry prosjekts endepunkt og modellutplasseringsnavn
4. Fortsett fra [Modul 05 - Distribuer til Foundry](05-deploy-to-foundry.md)

---

## Rydd opp ressurser (valgfritt)

Hvis du vil fjerne Azure-ressursene som ble opprettet under denne workshoppen:

### Alternativ 1: Slett ressursgruppen (sletter alt)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Alternativ 2: Slett bare den hostede agenten

1. Åpne [ai.azure.com](https://ai.azure.com) → prosjektet ditt → **Build** → **Agents**.
2. Klikk på agenten din → klikk **Delete**.

### Alternativ 3: Slett modellutplasseringen

1. I Foundry sidemeny, utvid prosjektet ditt → **Models**.
2. Høyreklikk på modellutplasseringen → **Delete**.

> **Kostnadsnotat:** Hostede agenter påløper kun kostnad når de kjører. Hvis du stopper eller sletter agenten, påløper ingen løpende kostnad. Modellutplasseringen kan påføre en liten kostnad for reservert kapasitet – slett den hvis du er ferdig.

---

**Forrige:** [06 - Verifiser i lekeplass](06-verify-in-playground.md) · **Neste:** [08 - Feilsøking (Referanse) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->