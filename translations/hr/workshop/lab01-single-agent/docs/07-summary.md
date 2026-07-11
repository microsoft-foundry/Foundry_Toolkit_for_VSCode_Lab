# Modul 7 - Sažetak i sljedeći koraci

⏱️ ~5 min

**Čestitamo!** Izgradili ste, testirali i (ako ste na Putu A) implementirali hostiranog AI agenta koristeći Microsoft Foundry i Foundry Toolkit za VS Code.

---

## Što ste izgradili

**Agent "Objasni mi kao izvršnom direktoru"** koji:
- Prima tehničke izvještaje o incidentima ili operativne vijesti putem HTTP-a (`POST /responses`)
- Prevodi ih u sažete izvještaje običnim jezikom za izvršne direktore
- Prati strukturirani izlazni format (Što se dogodilo / Poslovni utjecaj / Sljedeći korak)
- Odbija zahtjeve koji nisu povezani s temom i pokušaje ubrizgavanja upita
- Radi kao kontejnerizirani hostirani agent u Microsoft Foundry Agent Service

---

## Ključni naučeni pojmovi

| Pojam | Što ste uvježbavali |
|---------|-------------------|
| **Agent Framework arhitektura** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Životni ciklus hostiranog agenta** | Scaffold → Konfiguriraj → Testiraj lokalno → Implementiraj → Verificiraj u oblaku |
| **Inženjering sistemskog upita** | Uloga, publika, izlazni format, pravila, sigurnosna ograničenja i primjeri |
| **Razlike lokalno vs. hostirano** | Identitet (osobni vjerodajnici vs. upravljani identitet), endpoint, mrežni put |
| **Sigurnosne granice** | Obrana od ubrizgavanja upita, pridržavanje uloge, elegantno rukovanje rubnim slučajevima |
| **Radni tijek Foundry Toolkita** | Kreiranje projekta, implementacija modela, scaffoldanje agenta, Agent Inspector, implementacija jednim klikom |

---

## Što ste dovršili

### Put A (Foundry pretplata)

- [x] Postavili Foundry Toolkit i stvorili Foundry projekt s implementiranim modelom
- [x] Scaffoldali hostiranog agenta s automatski generiranom strukturom projekta
- [x] Napisali strukturirane upute za agenta sa sigurnosnim pravilima
- [x] Testirali lokalno s 3 funkcionalna scenarija (Agent Inspector)
- [x] Implementirali u Foundry Agent Service (kontejnerizirano)
- [x] Verificirali u cloud playgroundu s 4 testa rubnih slučajeva/sigurnosti

### Put B (Foundry Local)

- [x] Postavili Foundry Toolkit s lokalnim model endpointom
- [x] Scaffoldali projekt hostiranog agenta
- [x] Napisali strukturirane upute za agenta sa sigurnosnim pravilima
- [x] Testirali lokalno s 3 funkcionalna scenarija
- [x] Validirali ponašanje agenta bez potrebe za resursima u oblaku

---

## Sljedeći koraci

### Nastavite s učenjem

| Izvor | Opis |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Izgradite tijek rada s 4 agenta (Resume → Job Fit Evaluator) s obrascima orkestracije |
| **[Dodajte alate svom agentu](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Povežite API-je, baze podataka ili prilagođene funkcije putem Tool Cataloga |
| **[Dodajte znanje (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Utemeljite svog agenta dokumentima, vektorskim spremištima ili Bing pretraživanjem |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Potpuna referenca platforme |
| **[Agent Framework SDK referenca](https://learn.microsoft.com/agent-framework/)** | API dokumentacija za paket `agent-framework` |
| **[Foundry Toolkit - Novosti](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Bilješke o izdanju ekstenzije i povijest promjena |

### Ideje za proširenje vašeg agenta

- **Dodajte alat za datum** - Neka agent uključi kontekst "stanje na dan" u sažetke
- **Povežite se s bazom incidenata** - Povucite stvarne detalje incidenata putem funkcije alata
- **Dodajte alat za Bing upite** - Neka agent pretražuje najnovije vijesti za dodatni kontekst
- **Isprobajte različite modele** - Usporedite kvalitetu izlaza `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluirajte s Foundryjem** - Koristite značajku Evaluacije za mjerenje kvalitete agenta u obimu

### Za korisnike Puta B: Nadogradite na implementaciju u oblaku

Kad budete spremni implementirati u oblak:
1. Nabavite Azure pretplatu ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dovršite [Modul 01, Postavljanje](01-setup.md#step-2-set-up-based-on-your-access) (kreirajte projekt, implementirajte model, dodijelite RBAC)
3. Ažurirajte svoj `.env` s Foundry project endpointom i imenom implementacije modela
4. Nastavite iz [Modula 05 - Deploy to Foundry](05-deploy-to-foundry.md)

---

## Čišćenje resursa (opcionalno)

Ako želite ukloniti Azure resurse kreirane tijekom ovog radionice:

### Opcija 1: Izbrišite grupu resursa (uklanja sve)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opcija 2: Izbrišite samo hostiranog agenta

1. Otvorite [ai.azure.com](https://ai.azure.com) → vaš projekt → **Build** → **Agents**.
2. Kliknite na svog agenta → kliknite **Delete**.

### Opcija 3: Izbrišite implementaciju modela

1. U Foundry bočnoj traci, proširite svoj projekt → **Models**.
2. Desni klik na implementaciju modela → **Delete**.

> **Napomena o troškovima:** Hostirani agenti naplaćuju se samo dok rade. Ako zaustavite ili izbrišete agenta, nema stalnih troškova. Implementacija modela može imati malu naknadu za rezervirani kapacitet - izbrišite je ako ste završili.

---

**Prethodni:** [06 - Verify in Playground](06-verify-in-playground.md) · **Sljedeći:** [08 - Troubleshooting (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->