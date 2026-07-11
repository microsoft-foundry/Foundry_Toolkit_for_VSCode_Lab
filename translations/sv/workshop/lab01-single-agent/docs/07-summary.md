# Modul 7 - Sammanfattning & Nästa steg

⏱️ ~5 min

**Grattis!** Du har byggt, testat och (om på Bana A) distribuerat en hostad AI-agent med Microsoft Foundry och Foundry Toolkit för VS Code.

---

## Vad du byggde

En **"Förklara som om jag vore en chef"** agent som:
- Tar emot tekniska incidentrapporter eller operativa uppdateringar via HTTP (`POST /responses`)
- Översätter dem till sammanfattningar på vardagligt språk för chefer
- Följer ett strukturerat utdataformat (Vad hände / Affärspåverkan / Nästa steg)
- Vägrar ämnesfrämmande förfrågningar och försök till promptinjektion
- Körs som en containeriserad hostad agent i Microsoft Foundry Agent Service

---

## Viktiga koncept som lärdes

| Koncept | Vad du övade på |
|---------|-------------------|
| **Agent Framework-arkitektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hosted Agent livscykel** | Skapa stomme → Konfigurera → Testa lokalt → Distribuera → Verifiera i molnet |
| **Systempromptutformning** | Roll, målgrupp, utdataformat, regler, säkerhetsbegränsningar och exempel |
| **Skillnader lokal vs. hosted** | Identitet (personliga behörigheter vs. hanterad identitet), endpoint, nätverksväg |
| **Säkerhetsgränser** | Försvar mot promptinjektion, följsamhet till roll, smidig hantering av kantfall |
| **Foundry Toolkit-arbetsflöde** | Projekt skapande, modellutplacering, agentstomme, Agent Inspector, en-klicks distribution |

---

## Vad du slutförde

### Bana A (Foundry-prenumeration)

- [x] Installerade Foundry Toolkit och skapade ett Foundry-projekt med distribuerad modell
- [x] Skapade en hostad agent med autogenererad projektstruktur
- [x] Skrev strukturerade agentinstruktioner med säkerhetsregler
- [x] Testade lokalt med 3 funktionella scenarier (Agent Inspector)
- [x] Distribuerade till Foundry Agent Service (containeriserad)
- [x] Verifierade i cloud playground med 4 kantfall/säkerhetstester

### Bana B (Foundry Lokal)

- [x] Installerade Foundry Toolkit med lokal modell-endpoint
- [x] Skapade ett hostat agentprojekt
- [x] Skrev strukturerade agentinstruktioner med säkerhetsregler
- [x] Testade lokalt med 3 funktionella scenarier
- [x] Validerade agentbeteende utan att behöva molnresurser

---

## Nästa steg

### Fortsätt lära dig

| Resurs | Beskrivning |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Bygg ett arbetsflöde med 4 agenter (CV → Job Fit Evaluator) med orkestreringsmönster |
| **[Lägg till verktyg till din agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Koppla API:er, databaser eller anpassade funktioner via Tool Catalog |
| **[Lägg till kunskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Förankra din agent med dokument, vektorbutiker eller Bing-sökning |
| **[Microsoft Foundry dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fullständig plattformsreferens |
| **[Agent Framework SDK-referens](https://learn.microsoft.com/agent-framework/)** | API-dokumentation för `agent-framework` paketet |
| **[Foundry Toolkit - Nyheter](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Förlängningsreleaseanteckningar och ändringshistorik |

### Idéer för att utöka din agent

- **Lägg till ett datumverktyg** - Låt agenten inkludera "fr.o.m. idag" kontext i sammanfattningar
- **Koppla till en incidentdatabas** - Hämta verkliga incidentdetaljer via en verktygsfunktion
- **Lägg till ett Bing-förankringsverktyg** - Låt agenten söka efter senaste nyheter för extra kontext
- **Testa olika modeller** - Jämför `gpt-4.1` mot `gpt-4.1-mini` utdata kvalitet
- **Utvärdera med Foundry** - Använd Evaluations-funktionen för att mäta agentkvalitet i stor skala

### För Bana B-användare: Uppgradera till molndistribution

När du är redo att distribuera till molnet:
1. Skaffa en Azure-prenumeration ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Slutför [Modul 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (skapa projekt, distribuera modell, tilldela RBAC)
3. Uppdatera din `.env` med Foundry projekt-endpoint och modellens distributionsnamn
4. Fortsätt från [Modul 05 - Distribuera till Foundry](05-deploy-to-foundry.md)

---

## Rensa resurser (valfritt)

Om du vill ta bort Azure-resurser skapade under denna workshop:

### Alternativ 1: Ta bort resursgruppen (tar bort allt)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Alternativ 2: Ta bort bara den hostade agenten

1. Öppna [ai.azure.com](https://ai.azure.com) → ditt projekt → **Build** → **Agents**.
2. Klicka på din agent → klicka **Delete**.

### Alternativ 3: Ta bort modell-distributionen

1. I Foundry sidopanel, expandera ditt projekt → **Models**.
2. Högerklicka på modell-distributionen → **Delete**.

> **Kostnadsnotering:** Hostade agenter kostar endast när de körs. Om du stoppar eller tar bort agenten, uppstår ingen fortsatt kostnad. Modell-distributionen kan medföra en liten kostnad för reserverad kapacitet - ta bort den om du är klar.

---

**Föregående:** [06 - Verifiera i Playground](06-verify-in-playground.md) · **Nästa:** [08 - Felsökning (Referens) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->