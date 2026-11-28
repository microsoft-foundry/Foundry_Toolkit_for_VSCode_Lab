# Modul 7 - Sammanfattning & Nästa steg

⏱️ ~5 min

**Grattis!** Du har byggt, testat och (om på Väg A) distribuerat en hostad AI-agent med Microsoft Foundry och Foundry Toolkit för VS Code.

---

## Vad du byggde

En **"Förklara som för en chef"**-agent som:
- Tar emot tekniska incidentrapporter eller driftuppdateringar via HTTP (`POST /responses`)
- Översätter dem till lättförståeliga sammanfattningar för chefer
- Följer ett strukturerat utdataformat (Vad hände / Affärspåverkan / Nästa steg)
- Vägrar avvikande förfrågningar och försök till prompt-injektion
- Körs som en containeriserad hostad agent i Microsoft Foundry Agent Service

---

## Viktiga koncept du lärde dig

| Koncept | Vad du övade på |
|---------|-------------------|
| **Agent Framework-arkitektur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Hosted Agent livscykel** | Scaffold → Konfigurera → Testa lokalt → Distribuera → Verifiera i molnet |
| **System prompt-engineering** | Roll, publik, utdataformat, regler, säkerhetsbegränsningar och exempel |
| **Skillnader mellan lokalt och hostat** | Identitet (personlig uppgift vs. hanterad identitet), endpoint, nätverksväg |
| **Säkerhetsgränser** | Försvar mot prompt-injektion, rollföljsamhet, hantering av kantfall på ett smidigt sätt |
| **Foundry Toolkit-arbetsflöde** | Projekt skapande, modelldistribution, agent-scaffolding, Agent Inspector, en-klicks distribution |

---

## Vad du slutförde

### Väg A (Foundry-prenumeration)

- [x] Installerade Foundry Toolkit och skapade ett Foundry-projekt med distribuerad modell
- [x] Scaffoldade en hostad agent med automatiskt genererad projektstruktur
- [x] Skrev strukturerade agentinstruktioner med säkerhetsregler
- [x] Testade lokalt med 3 funktionella scenarier (Agent Inspector)
- [x] Distribuerade till Foundry Agent Service (containeriserad)
- [x] Verifierade i molnets lekplats med 4 kantfalls-/säkerhetstester

### Väg B (Foundry Lokalt)

- [x] Installerade Foundry Toolkit med en lokal modellemdpoint
- [x] Scaffoldade ett hostat agentprojekt
- [x] Skrev strukturerade agentinstruktioner med säkerhetsregler
- [x] Testade lokalt med 3 funktionella scenarier
- [x] Validerade agentbeteende utan att behöva molnresurser

---

## Nästa steg

### Fortsätt lärandet

| Resurs | Beskrivning |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orkestrering](../../lab02-multi-agent/docs/README.md)** | Bygg ett arbetsflöde med 4 agenter (Resume → Job Fit Evaluator) med orkestreringsmönster |
| **[Lägg till verktyg till din agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Anslut API:er, databaser eller anpassade funktioner via Tool Catalog |
| **[Lägg till kunskap (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ge din agent underlag med dokument, vektorlagring eller Bing-sökning |
| **[Microsoft Foundry-dokumentation](https://learn.microsoft.com/azure/foundry/)** | Fullständig plattformsreferens |
| **[Agent Framework SDK-referens](https://learn.microsoft.com/agent-framework/)** | API-dokumentation för `agent-framework` paketet |
| **[Foundry Toolkit - Vad är nytt](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Tilläggsreleasenoter och ändringslogg |

### Idéer för att utöka din agent

- **Lägg till ett datumverktyg** - Låt agenten inkludera "per idag"-kontekst i sammanfattningar
- **Anslut till en incidentdatabas** - Hämta faktiska incidentdetaljer via en verktygsfunktion
- **Lägg till ett Bing-verktyg för underlag** - Låt agenten söka efter senaste nyheter för mer kontext
- **Testa olika modeller** - Jämför `gpt-4.1` mot `gpt-4.1-mini` i utdata kvalitet
- **Utvärdera med Foundry** - Använd Evaluations-funktionen för att mäta agentens kvalitet i stor skala

### För Väg B-användare: Uppgradera till molndistribution

När du är redo att distribuera till molnet:
1. Skaffa en Azure-prenumeration ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Slutför [Modul 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (skapa projekt, distribuera modell, tilldela RBAC)
3. Uppdatera din `.env` med Foundry-projektets endpoint och modellens distributionsnamn
4. Fortsätt från [Modul 05 - Distribuera till Foundry](05-deploy-to-foundry.md)

---

## Rensa resurser (valfritt)

Om du vill ta bort Azure-resurser skapade under denna workshop:

### Alternativ 1: Ta bort resursgruppen (tar bort allt)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Alternativ 2: Ta bort bara den hostade agenten

1. Öppna [ai.azure.com](https://ai.azure.com) → ditt projekt → **Bygg** → **Agenter**.
2. Klicka på din agent → klicka **Ta bort**.

### Alternativ 3: Ta bort modelldistributionen

1. I Foundry sidofält, expandera ditt projekt → **Modeller**.
2. Högerklicka på modelldistributionen → **Ta bort**.

> **Kostnadsnotering:** Hostade agenter kostar bara när de körs. Om du stoppar eller tar bort agenten, pågår ingen avgift. Modelldistributionen kan medföra en liten kostnad för reserverad kapacitet - ta bort den om du är klar.

---

**Föregående:** [06 - Verifiera i Lekplatsen](06-verify-in-playground.md) · **Nästa:** [08 - Felsökning (Referens) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->