# Modul 7 - Resumé & Næste Skridt

⏱️ ~5 min

**Tillykke!** Du har bygget, testet og (hvis på sti A) deployeret en hostet AI-agent ved hjælp af Microsoft Foundry og Foundry Toolkit til VS Code.

---

## Hvad du byggede

En **"Forklar som om jeg er en Direktør"** agent, der:
- Modtager tekniske hændelsesrapporter eller driftsopdateringer via HTTP (`POST /responses`)
- Oversætter dem til letforståelige direktørsammendrag
- Følger et struktureret outputformat (Hvad skete der / Forretningspåvirkning / Næste skridt)
- Afviser irrelevante forespørgsler og forsøg på promptinjektion
- Kører som en containeriseret hostet agent i Microsoft Foundry Agent Service

---

## Centrale begreber lært

| Begreb | Hvad du øvede dig på |
|---------|-------------------|
| **Agent Framework arkitektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hosted Agent livscyklus** | Scaffold → Konfigurér → Test lokalt → Deploy → Verificer i skyen |
| **System prompt engineering** | Rolle, målgruppe, outputformat, regler, sikkerhedsbegrænsninger og eksempler |
| **Lokale vs. hostede forskelle** | Identitet (personlige legitimationsdata vs. managed identity), endpoint, netværksvej |
| **Sikkerhedsgrænser** | Forsvar mod promptinjektion, rolleoverholdelse, elegant håndtering af kanttilfælde |
| **Foundry Toolkit workflow** | Projektoprettelse, modeludrulning, agent scaffolding, Agent Inspector, one-click deploy |

---

## Hvad du gennemførte

### Sti A (Foundry abonnement)

- [x] Konfigurerede Foundry Toolkit og oprettede et Foundry-projekt med en deployeret model
- [x] Scaffoldede en hostet agent med autogenereret projektstruktur
- [x] Skrev strukturerede agentinstruktioner med sikkerhedsregler
- [x] Testede lokalt med 3 funktionelle scenarier (Agent Inspector)
- [x] Deployede til Foundry Agent Service (containeriseret)
- [x] Verificerede i cloud playground med 4 kanttilfælde/sikkerhedstests

### Sti B (Foundry Local)

- [x] Konfigurerede Foundry Toolkit med en lokal model-endpoint
- [x] Scaffoldede et hostet agent-projekt
- [x] Skrev strukturerede agentinstruktioner med sikkerhedsregler
- [x] Testede lokalt med 3 funktionelle scenarier
- [x] Validerede agentadfærd uden behov for sky-ressourcer

---

## Næste skridt

### Fortsæt læringen

| Ressource | Beskrivelse |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Byg en 4-agent workflow (Resume → Job Fit Evaluator) med orkestreringsmønstre |
| **[Tilføj værktøjer til din agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Tilslut API'er, databaser eller brugerdefinerede funktioner via Tool Catalog |
| **[Tilføj viden (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Forankr din agent med dokumenter, vektorlager eller Bing-søgning |
| **[Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fuld platformreference |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API-dokumentation for `agent-framework` pakken |
| **[Foundry Toolkit - Nyheder](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Udgivelsesnoter og ændringslog for udvidelsen |

### Idéer til at udvide din agent

- **Tilføj et datoværktøj** - Lad agenten inkludere "pr. dags dato" kontekst i sammendrag
- **Forbind til en hændelsesdatabase** - Hent reelle hændelsesdetaljer via en værktøjsfunktion
- **Tilføj et Bing-forankringsværktøj** - Lad agenten slå nyheder op for yderligere kontekst
- **Prøv forskellige modeller** - Sammenlign outputkvalitet af `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluer med Foundry** - Brug Evaluations-funktionen til at måle agentkvalitet i stor skala

### For Sti B brugere: Opgrader til cloud deployment

Når du er klar til at deployere til skyen:
1. Skaff et Azure abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fuldfør [Modul 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (opret projekt, deploy model, tildel RBAC)
3. Opdater din `.env` med Foundry projekt-endpoint og model deployment navn
4. Fortsæt fra [Modul 05 - Deploy til Foundry](05-deploy-to-foundry.md)

---

## Ryd op i ressourcer (valgfrit)

Hvis du vil fjerne Azure-ressourcerne, der blev oprettet under denne workshop:

### Mulighed 1: Slet resourcegruppen (fjerner alt)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Mulighed 2: Slet kun den hostede agent

1. Åbn [ai.azure.com](https://ai.azure.com) → dit projekt → **Build** → **Agents**.
2. Klik på din agent → klik **Slet**.

### Mulighed 3: Slet model deployment

1. Udvid dit projekt i Foundry sidebaren → **Models**.
2. Højreklik på model deployment → **Slet**.

> **Omkostningsnotat:** Hostede agenter koster kun, når de kører. Hvis du stopper eller sletter agenten, er der ingen løbende omkostning. Model deployment kan medføre en lille omkostning for reserveret kapacitet - slet den, hvis du er færdig.

---

**Forrige:** [06 - Verificer i Playground](06-verify-in-playground.md) · **Næste:** [08 - Fejlfinding (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->