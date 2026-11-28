# Modul 7 - Resumé & Næste Skridt

⏱️ ~5 min

**Tillykke!** Du har bygget, testet og (hvis på Spor A) udrullet en hostet AI-agent ved hjælp af Microsoft Foundry og Foundry Toolkit til VS Code.

---

## Hvad du har bygget

En **"Forklar Som Om Jeg Er en Leder"**-agent, der:
- Modtager tekniske hændelsesrapporter eller operationelle opdateringer via HTTP (`POST /responses`)
- Oversætter dem til almindelige sproglige ledelsesresumeer
- Følger et struktureret outputformat (Hvad skete der / Forretningspåvirkning / Næste skridt)
- Afviser off-topic forespørgsler og forsøg på prompt-injektion
- Kører som en containeriseret hostet agent i Microsoft Foundry Agent Service

---

## Centrale begreber lært

| Begreb | Hvad du har øvet dig i |
|---------|-------------------|
| **Agent Framework arkitektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hosted Agent livscyklus** | Scaffold → Konfigurér → Test lokalt → Deploy → Verificér i skyen |
| **System prompt engineering** | Rolle, målgruppe, outputformat, regler, sikkerhedsbegrænsninger og eksempler |
| **Forskelle mellem lokalt og hostet** | Identitet (personligt legitimationskort vs. administreret identitet), endpoint, netværkssti |
| **Sikkerhedsgrænser** | Forsvar mod prompt-injektion, rolleoverholdelse, elegant håndtering af kanttilfælde |
| **Foundry Toolkit arbejdsgang** | Projektoprettelse, modeludrulning, agent scaffolding, Agent Inspector, ét-klik udrulning |

---

## Hvad du har gennemført

### Spor A (Foundry abonnement)

- [x] Konfigureret Foundry Toolkit og oprettet et Foundry-projekt med udrullet model
- [x] Scaffolded en hosted agent med autogenereret projektstruktur
- [x] Skrev strukturerede agentinstruktioner med sikkerhedsregler
- [x] Testet lokalt med 3 funktionelle scenarier (Agent Inspector)
- [x] Deployet til Foundry Agent Service (containeriseret)
- [x] Verificeret i cloud playground med 4 kanttilfælde/sikkerhedstests

### Spor B (Foundry Lokalt)

- [x] Konfigureret Foundry Toolkit med et lokalt model-endpoint
- [x] Scaffolded et hosted agent projekt
- [x] Skrev strukturerede agentinstruktioner med sikkerhedsregler
- [x] Testet lokalt med 3 funktionelle scenarier
- [x] Valideret agentadfærd uden behov for skyressourcer

---

## Næste skridt

### Fortsæt med at lære

| Ressource | Beskrivelse |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Byg en 4-agent arbejdsgang (CV → Job Fit Evaluator) med orkestreringsmønstre |
| **[Tilføj værktøjer til din agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Forbind APIer, databaser eller brugerdefinerede funktioner via Tool Catalog |
| **[Tilføj viden (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ground din agent med dokumenter, vektorlager eller Bing-søgning |
| **[Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fuld platformreferance |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API-dokumentation for `agent-framework` pakken |
| **[Foundry Toolkit - Nyheder](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Udvidelsesrelease-noter og changelog |

### Ideer til at udvide din agent

- **Tilføj et datoværktøj** - Lad agenten inkludere "pr. dags dato" kontekst i resumeer
- **Forbind til en hændelsesdatabase** - Træk faktiske hændelsesdetaljer via en værktøjsfunktion
- **Tilføj et Bing groundingsværktøj** - Lad agenten slå op i seneste nyheder for yderligere kontekst
- **Prøv forskellige modeller** - Sammenlign outputkvalitet fra `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluer med Foundry** - Brug Evaluations-funktionen til at måle agentkvalitet i stor skala

### For Spor B brugere: Opgradér til cloud-udrulning

Når du er klar til at udrulle til skyen:
1. Få et Azure-abonnement ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Fuldfør [Modul 01, Opsætning](01-setup.md#step-2-set-up-based-on-your-access) (opret projekt, deploy model, tildel RBAC)
3. Opdater din `.env` med Foundry-projektets endpoint og modeludrulningsnavn
4. Fortsæt fra [Modul 05 - Deploy til Foundry](05-deploy-to-foundry.md)

---

## Ryd op i ressourcerne (valgfrit)

Hvis du ønsker at fjerne de Azure-ressourcer, der er oprettet under workshoppen:

### Mulighed 1: Slet ressourcegruppen (fjerner alt)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Mulighed 2: Slet kun den hostede agent

1. Åbn [ai.azure.com](https://ai.azure.com) → dit projekt → **Build** → **Agents**.
2. Klik på din agent → klik **Delete**.

### Mulighed 3: Slet modeludrulningen

1. I Foundry sidebar, udvid dit projekt → **Models**.
2. Højreklik på modeludrulningen → **Delete**.

> **Bemærk om omkostninger:** Hosted agenter påløber kun omkostninger, når de kører. Hvis du stopper eller sletter agenten, er der ingen løbende omkostninger. Modeludrulningen kan medføre et lille gebyr for reserveret kapacitet - slet den, hvis du er færdig.

---

**Forrige:** [06 - Verificér i Playground](06-verify-in-playground.md) · **Næste:** [08 - Fejlfinding (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->