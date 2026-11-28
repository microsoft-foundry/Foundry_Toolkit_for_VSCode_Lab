# Modul 7 - Sažetak i sljedeći koraci

⏱️ ~5 min

**Čestitamo!** Izgradili ste, testirali i (ako ste na Putu A) implementirali hostiranog AI agenta koristeći Microsoft Foundry i Foundry Toolkit za VS Code.

---

## Što ste izgradili

**"Objasni kao da sam izvršni direktor"** agenta koji:
- Prima tehnička izvješća o incidentima ili operativna ažuriranja putem HTTP (`POST /responses`)
- Prevodi ih u sažete izvršne izvještaje na razumljivom jeziku
- Slijedi strukturirani izlazni format (Što se dogodilo / Poslovni utjecaj / Sljedeći korak)
- Odbija zahtjeve koji nisu na temu i pokušaje injektiranja prompta
- Radi kao kontejnerski hostirani agent u Microsoft Foundry Agent Service

---

## Ključni naučeni pojmovi

| Pojam | Što ste vježbali |
|---------|-------------------|
| **Arhitektura Agent Frameworka** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` pipeline |
| **Životni ciklus hostiranog agenta** | Scaffold → Konfiguriranje → Lokalno testiranje → Implementacija → Provjera u oblaku |
| **Inženjering sistemskog prompta** | Uloga, publika, izlazni format, pravila, sigurnosni ograničenja i primjeri |
| **Razlike lokalno vs. hostirano** | Identitet (osobna vjerodajnica vs. upravljani identitet), endpoint, mrežni put |
| **Sigurnosne granice** | Obrana od injektiranja prompta, pridržavanje uloge, graciozno rukovanje rubnim slučajevima |
| **Foundry Toolkit workflow** | Kreiranje projekta, implementacija modela, scaffolding agenta, Agent Inspector, implementacija jednim klikom |

---

## Što ste završili

### Put A (Foundry pretplata)

- [x] Postavili Foundry Toolkit i kreirali Foundry projekt s implementiranim modelom
- [x] Scaffoldirali hostiranog agenta s automatski generiranom strukturom projekta
- [x] Napisali strukturirane upute za agenta sa sigurnosnim pravilima
- [x] Testirali lokalno s 3 funkcionalna scenarija (Agent Inspector)
- [x] Implementirali u Foundry Agent Service (kontejnerizirano)
- [x] Potvrdili u cloud playgroundu s 4 rubna/sigurnosna testa

### Put B (Foundry Local)

- [x] Postavili Foundry Toolkit s lokalnim model endpointom
- [x] Scaffoldirali projekt hostiranog agenta
- [x] Napisali strukturirane upute za agenta sa sigurnosnim pravilima
- [x] Testirali lokalno s 3 funkcionalna scenarija
- [x] Potvrdili ponašanje agenta bez potrebe za resursima u oblaku

---

## Sljedeći koraci

### Nastavite učiti

| Resurs | Opis |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Izgradite 4-agentni workflow (Rezime → Evaluator prikladnosti za posao) s obrascima orkestracije |
| **[Dodajte alate svom agentu](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Povežite API-je, baze podataka ili prilagođene funkcije putem Tool Cataloga |
| **[Dodajte znanje (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Osigurajte svoj agent s dokumentima, vektorskim spremištima ili Bing pretraživanjem |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Potpuni referentni materijal platforme |
| **[Agent Framework SDK referenca](https://learn.microsoft.com/agent-framework/)** | API dokumentacija za `agent-framework` paket |
| **[Foundry Toolkit - Što je novo](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Bilješke o izdanju ekstenzije i zapis promjena |

### Ideje za proširenje vašeg agenta

- **Dodajte alat za datum** - Neka agent uključuje kontekst "stanje na danas" u sažetcima
- **Povežite se s bazom podataka incidenata** - Dohvatite stvarne detalje incidenata putem funkcije alata
- **Dodajte alat za Bing pretraživanje** - Neka agent pretražuje nedavne vijesti za dodatni kontekst
- **Isprobajte različite modele** - Usporedite izlaznu kvalitetu `gpt-4.1` i `gpt-4.1-mini`
- **Evaluirajte s Foundryem** - Koristite značajku Evaluations za mjerenje kvalitete agenta u mjerilu

### Za korisnike Puta B: Nadogradite na implementaciju u oblaku

Kada budete spremni implementirati u oblak:
1. Nabavite Azure pretplatu ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Završite [Modul 01, Postavljanje](01-setup.md#step-2-set-up-based-on-your-access) (kreirajte projekt, implementirajte model, dodijelite RBAC)
3. Ažurirajte svoj `.env` s Foundry endpointom projekta i nazivom implementacije modela
4. Nastavite iz [Modul 05 - Implementacija u Foundry](05-deploy-to-foundry.md)

---

## Očistite resurse (opcionalno)

Ako želite ukloniti Azure resurse stvorene tijekom ovog radionice:

### Opcija 1: Izbrišite grupu resursa (uklanja sve)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opcija 2: Izbrišite samo hostiranog agenta

1. Otvorite [ai.azure.com](https://ai.azure.com) → vaš projekt → **Build** → **Agents**.
2. Kliknite na svog agenta → kliknite **Delete**.

### Opcija 3: Izbrišite implementaciju modela

1. U Foundry bočnoj traci proširite svoj projekt → **Models**.
2. Desni klik na implementaciju modela → **Delete**.

> **Napomena o troškovima:** Hostirani agenti naplaćuju se samo dok rade. Ako ga zaustavite ili izbrišete, nema daljnjih troškova. Implementacija modela može naplaćivati malu naknadu za rezervirani kapacitet – izbrišite je ako ste gotovi.

---

**Prethodno:** [06 - Provjera u playgroundu](06-verify-in-playground.md) · **Sljedeće:** [08 - Rješavanje problema (Referenca) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->