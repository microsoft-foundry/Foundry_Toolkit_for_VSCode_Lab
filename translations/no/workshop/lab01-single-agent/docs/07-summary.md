# Modul 7 - Oppsummering & Neste steg

⏱️ ~5 min

**Gratulerer!** Du har bygget, testet og (hvis på Vei A) distribuert en hostet AI-agent ved hjelp av Microsoft Foundry og Foundry Toolkit for VS Code.

---

## Hva du bygde

En **"Forklar som om jeg er en leder"**-agent som:
- Mottar tekniske hendelsesrapporter eller driftsoppdateringer via HTTP (`POST /responses`)
- Oversetter dem til enkle språklige lederoppsummeringer
- Følger et strukturert utdataformat (Hva skjedde / Forretningspåvirkning / Neste steg)
- Avviser utenfor tema forespørsler og forsøk på prompt-injeksjon
- Kjører som en containerisert hostet agent i Microsoft Foundry Agent Service

---

## Nøkkelkonsepter lært

| Konsept | Hva du øvde på |
|---------|-------------------|
| **Agent Framework arkitektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hostet Agent livssyklus** | Scaffold → Konfigurer → Test lokalt → Distribuer → Verifiser i skyen |
| **System-prompt ingeniørkunst** | Rolle, publikum, utdataformat, regler, sikkerhetsbegrensninger og eksempler |
| **Forskjeller lokalt vs. hostet** | Identitet (personlig legitimasjon vs. administrert identitet), endepunkt, nettverkssti |
| **Sikkerhetsgrenser** | Forsvar mot prompt-injeksjon, rolleoverholdelse, elegant håndtering av kanttilfeller |
| **Foundry Toolkit arbeidsflyt** | Opprettelse av prosjekt, modellutplassering, agent scaffolding, Agent Inspector, ett-klikk distribusjon |

---

## Hva du fullførte

### Vei A (Foundry abonnement)

- [x] Satte opp Foundry Toolkit og opprettet et Foundry-prosjekt med distribuert modell
- [x] Scaffoldet en hostet agent med automatisk generert prosjektstruktur
- [x] Skrev strukturerte agentinstruksjoner med sikkerhetsregler
- [x] Testet lokalt med 3 funksjonelle scenarier (Agent Inspector)
- [x] Distribuerte til Foundry Agent Service (containerisert)
- [x] Verifiserte i sky-lekeplass med 4 kanttilfelle/sikkerhetstester

### Vei B (Foundry Lokalt)

- [x] Satte opp Foundry Toolkit med et lokalt modell-endepunkt
- [x] Scaffoldet et hostet agent-prosjekt
- [x] Skrev strukturerte agentinstruksjoner med sikkerhetsregler
- [x] Testet lokalt med 3 funksjonelle scenarier
- [x] Validerte agentadferd uten behov for skyressurser

---

## Neste steg

### Fortsett å lære

| Ressurs | Beskrivelse |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Bygg en 4-agent arbeidsflyt (CV → Jobbanalyse) med orkestreringsmønstre |
| **[Legg til verktøy til agenten din](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Koble til API-er, databaser eller egendefinerte funksjoner via Tool Catalog |
| **[Legg til kunnskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Forankre agenten din med dokumenter, vektorlagre eller Bing-søk |
| **[Microsoft Foundry dokumentasjon](https://learn.microsoft.com/azure/foundry/)** | Full plattformreferanse |
| **[Agent Framework SDK referanse](https://learn.microsoft.com/agent-framework/)** | API-dokumentasjon for `agent-framework` pakken |
| **[Foundry Toolkit - Hva er nytt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Tilleggets utgivelsesnotater og endringslogg |

### Ideer for å utvide agenten din

- **Legg til et dato-verktøy** - La agenten inkludere "per i dag" kontekst i oppsummeringer
- **Koble til en hendelsesdatabase** - Hent detaljer om faktiske hendelser via et verktøy
- **Legg til et Bing-forankringsverktøy** - La agenten slå opp ferske nyheter for ekstra kontekst
- **Prøv forskjellige modeller** - Sammenlign `gpt-4.1` vs. `gpt-4.1-mini` output-kvalitet
- **Evaluer med Foundry** - Bruk Evalueringer-funksjonen for å måle agentkvalitet i stor skala

### For Vei B-brukere: Oppgrader til sky-distribusjon

Når du er klar til å distribuere til skyen:
1. Skaff et Azure-abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fullfør [Modul 01, Oppsett](01-setup.md#step-2-set-up-based-on-your-access) (opprett prosjekt, distribuer modell, tilordne RBAC)
3. Oppdater din `.env` med Foundry-prosjektets endepunkt og modellens distribusjonsnavn
4. Fortsett fra [Modul 05 - Distribuer til Foundry](05-deploy-to-foundry.md)

---

## Rydd opp ressurser (valgfritt)

Hvis du ønsker å fjerne Azure-ressursene som ble opprettet under denne workshop-en:

### Alternativ 1: Slett ressursgruppen (fjerner alt)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Alternativ 2: Slett kun den hostede agenten

1. Åpne [ai.azure.com](https://ai.azure.com) → ditt prosjekt → **Bygg** → **Agenter**.
2. Klikk på agenten din → klikk **Slett**.

### Alternativ 3: Slett modell-distribusjonen

1. I Foundry sidefelt, utvid ditt prosjekt → **Modeller**.
2. Høyreklikk modell-distribusjonen → **Slett**.

> **Kostnadsnotat:** Hostede agenter påløper kostnad kun når de kjører. Hvis du stopper eller sletter agenten, er det ingen løpende kostnad. Modell-distribusjonen kan påløpe en liten kostnad for reservert kapasitet - slett den hvis du er ferdig.

---

**Forrige:** [06 - Verifiser i lekeplass](06-verify-in-playground.md) · **Neste:** [08 - Feilsøking (Referanse) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal betraktes som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->