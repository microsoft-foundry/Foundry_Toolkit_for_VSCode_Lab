# Modul 9 - Sažetak i sljedeći koraci

⏱️ ~5 min

**Čestitamo!** Izgradili ste, testirali i (ako ste na Putu A) implementirali višelagodni tijek rada koristeći Microsoft Foundry i Foundry Toolkit za VS Code.

---

## Što ste izgradili

**Procjenitelj usklađenosti životopisa s poslom** - višelagodni hostani tijek rada koji:
- Prima životopis + opis posla putem HTTP-a (`POST /responses`)
- Pokreće četiri specijalizirana agenta u sekvencijalnom tijeku - svaki agent prenosi podatke koje njegov nasljednik treba
- Vraća rezultat usklađenosti (0–100 s razlaganjem), popis vještina i certifikata koje nedostaju, i personaliziranu roadmapu učenja s pravim Microsoft Learn vezama za svaki nedostatak
- Poziva Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) za dohvat službenih izvora učenja za svaki identificirani nedostatak vještine
- Pokreće se kao jedan kontejnerizirani hostani agent u Microsoft Foundry Agent Service

---

## Ključni naučeni koncepti

| Koncept | Što ste vježbali |
|---------|-------------------|
| **Orkestracija višelagodnoga rada** | `WorkflowBuilder` sekvencijalni tijek s `add_edge()` |
| **Specijalizacija agenata** | Četiri fokusirana agenta nadmašuju jednog općeg agenta |
| **Predložak Content Router** | ResumeParser služi i kao usmjerivač - čuva tekst JD u odjeljku `[JOB DESCRIPTION PASS-THROUGH]` da bi ga mogu downstream agenti dohvatiti (potrebno jer `context_mode="last_agent"` znači da samo `start_executor` vidi sirovu korisničku poruku) |
| **Predložak Content Relay** | JD Agent prenosi `[PARSED RESUME PASS-THROUGH]` dalje tako da MatchingAgent dobiva oba profila; izbjegava OR-semantiku dvostrukog okidanja koju uzrokuju fan-in grafovi |
| **Integracija MCP alata** | `@tool` + `streamable_http_client` pozivanje vanjskog MCP servera |
| **Životni ciklus hostanog agenta** | Scaffold → Konfiguracija → Lokalno testiranje → Implementacija → Provjera u oblaku |
| **`context_mode="last_agent"`** | Svaki izvršitelj vidi samo izlaz svog izravnog prethodnika |
| **Foundry Toolkit tijek rada** | Scaffold čarobnjak, Inspektor agenata, Visualizer tijeka rada, jednim klikom implementacija |

---

## Što ste dovršili

<details open>
<summary><strong>🅰️ Put A - Foundry pretplata</strong></summary>

- [x] Potvrđen postav Lab 01: projekt, model i RBAC još aktivni
- [x] Scaffoldan višelagodni projekt korištenjem Workflows šablone
- [x] Napisani skupovi uputa za četiri agenta (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integriran Microsoft Learn MCP alat sa `streamable_http_client`
- [x] Konfigurirana graf tijeka rada sa `WorkflowBuilder` (sekvencijalni tijek sa prenošenjem sadržaja)
- [x] Testirano lokalno s 3 osnovna testa (Agent Inspector) - rezultat usklađenosti, kartice s nedostacima i MCP URL-ovi
- [x] Implementirano u Foundry Agent Service (kontejnerizirano, upravljani identitet)
- [x] Potvrđeno u oblaku playground - strukturna dosljednost s lokalnim rezultatima

</details>

<details open>
<summary><strong>🅱️ Put B - Foundry Local</strong></summary>

- [x] Potvrđen postav Lab 01: Foundry Local pokrenut s lokalnim modelom
- [x] Scaffoldan višelagodni projekt korištenjem Workflows šablone
- [x] Napisani skupovi uputa za četiri agenta i podešen tijek rada
- [x] Integriran Microsoft Learn MCP alat
- [x] Testirano lokalno s 3 osnovna testa
- [x] Potvrđeno višelagodno ponašanje bez potrebe za oblačnim resursima

</details>

---

## Sljedeći koraci

### Nastavite učiti

| Resurs | Opis |
|----------|-------------|
| **[Agent Framework SDK referenca](https://learn.microsoft.com/agent-framework/)** | API dokumentacija za `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP alat katalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Povežite agente s drugim MCP serverima (Bing, GitHub, po mjeri) |
| **[Dodavanje znanja (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Prizemljite agente s dokumentima, vektorskim spremištima ili Bing pretragom |
| **[Foundry evaluacije](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mjerite kvalitetu agenata u velikoj mjeri s automatiziranim evaluatorima |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Kompletnu referencu platforme |
| **[Foundry Toolkit - Što je novo](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Bilješke o izdanju ekstenzije i zapis promjena |

### Ideje za proširenje ovog tijeka rada

- **Dodajte petog agenta** - Trenera za intervjue koji izrađuje vjerojatna pitanja na temelju izvještaja o nedostacima
- **Dodajte Bing alat za prizemljenje** - Neka JD Agent pretražuje slične oglase za posao kako bi obogatio zahtjeve
- **Povežite s bazom životopisa** - Povucite profile kandidata iz baze preko prilagođenog `@tool`
- **Isprobajte različite modele** - Usporedite kvalitetu i latenciju izlaza `gpt-4.1` i `gpt-4.1-mini`
- **Evaluirajte s Foundry** - Koristite značajku Evaluacija za ocjenu izvještaja o usklađenosti prema zlatnom skupu podataka

### Za korisnike Puta B: Nadogradite na implementaciju u oblaku

Kad ste spremni za implementaciju u oblak:
1. Nabavite Azure pretplatu ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dovršite [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (kreirajte projekt, implementirajte model, dodijelite RBAC)
3. Ažurirajte svoj `.env` s krajnjom točkom Foundry projekta i imenom implementacije modela
4. Nastavite s [Modulom 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Očistite resurse (opcionalno)

Ako želite ukloniti Azure resurse kreirane tijekom ovog radionice:

### Opcija 1: Izbrišite grupu resursa (uklanja sve)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opcija 2: Izbrišite samo hostanog agenta

1. Otvorite [ai.azure.com](https://ai.azure.com) → vaš projekt → **Build** → **Agents**.
2. Pronađite **PersonalCareerCopilot** → kliknite **Delete**.

### Opcija 3: Izbrišite implementaciju modela

1. U Foundry bočnoj traci proširite vaš projekt → **Models**.
2. Desni klik na implementaciju modela → **Delete**.

> **Napomena o troškovima:** Hostani agenti naplaćuju se samo dok rade. Ako zaustavite ili izbrišete agenta, nema daljnjih troškova. Implementacija modela može naplaćivati malu naknadu za rezervirani kapacitet - izbrišite ju ako ste gotovi.

---

**Prethodno:** [08 - Rješavanje problema](08-troubleshooting.md) · **Početna:** [Lab 02 README](../README.md) · [Početna radionice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->