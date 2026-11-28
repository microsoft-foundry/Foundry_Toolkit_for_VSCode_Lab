# Modul 9 - Sažetak i sljedeći koraci

⏱️ ~5 min

**Čestitamo!** Izgradili ste, testirali i (ako ste na Putu A) implementirali višesagentni tijek rada koristeći Microsoft Foundry i Foundry Toolkit za VS Code.

---

## Što ste izgradili

**Procjenjivač usklađenosti životopisa s poslom** - višesagentni hostani tijek rada koji:
- Prima životopis + opis posla putem HTTP (`POST /responses`)
- Pokreće četiri specijalizirana agenta u sekvencijalnom lancu - svaki agent prosljeđuje podatke koje njegov sljedbenik treba
- Vraća ocjenu usklađenosti (0–100 s razradom), popis nedostataka vještina i certifikata te personalizirani plan učenja sa stvarnim Microsoft Learn vezama za svaki nedostatak
- Poziva Microsoft Learn MCP poslužitelj (`https://learn.microsoft.com/api/mcp`) kako bi dohvatili službene obrazovne resurse za svaki identificirani nedostatak vještina
- Radi kao jedan kontejnerizirani hostani agent u Microsoft Foundry Agent Service

---

## Ključni naučeni koncepti

| Koncept | Što ste vježbali |
|---------|-------------------|
| **Multi-agent orkestracija** | `WorkflowBuilder` sekvencijalni lanac s `add_edge()` |
| **Specijalizacija agenta** | Četiri fokusirana agenta nadmašuju jednog opće namjene |
| **Content Router obrazac** | ResumeParser služi kao usmjerivač - čuva tekst opisa posla u `[JOB DESCRIPTION PASS-THROUGH]` sekciji kako bi agenti nizvodno mogli pristupiti istom (potrebno jer `context_mode="last_agent"` znači da samo `start_executor` vidi sirovu korisničku poruku) |
| **Content Relay obrazac** | JD Agent prosljeđuje `[PARSED RESUME PASS-THROUGH]` naprijed tako da MatchingAgent dobiva oba profila; izbjegava dvostruku aktivaciju OR-semantike koju uzrokuju fan-in grafovi |
| **Integracija MCP alata** | `@tool` + `streamable_http_client` pozivanje vanjskog MCP poslužitelja |
| **Životni ciklus hostanog agenta** | Scaffold → Konfiguriraj → Lokalno testiraj → Implementiraj → Provjeri u oblaku |
| **`context_mode="last_agent"`** | Svaki izvršitelj vidi samo izlaz svog izravnog prethodnika |
| **Foundry Toolkit tijek rada** | Čarobnjak za Scaffold, Agent Inspector, Workflow Visualizer, implementacija jednim klikom |

---

## Što ste dovršili

<details open>
<summary><strong>🅰️ Put A - Foundry pretplata</strong></summary>

- [x] Potvrdili postavljanje Lab 01: projekt, model i RBAC još aktivni
- [x] Scaffoldali višesagentni projekt koristeći Workflows predložak
- [x] Napisali četiri seta uputa za agente (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrirali Microsoft Learn MCP alat s `streamable_http_client`
- [x] Spojili tijek rada graf s `WorkflowBuilder` (sekvencijalni lanac s prosljeđivanjem sadržaja)
- [x] Testirali lokalno s 2 smoke testa (Agent Inspector) - ocjena usklađenosti, kartice nedostataka i MCP URL-ovi
- [x] Implementirali u Foundry Agent Service (kontejnerizirano, upravljani identitet)
- [x] Potvrdili u cloud playgroundu - strukturna konzistentnost s lokalnim rezultatima

</details>

<details open>
<summary><strong>🅱️ Put B - Foundry Local</strong></summary>

- [x] Potvrdili postavljanje Lab 01: Foundry Local radi s lokalnim modelom
- [x] Scaffoldali višesagentni projekt koristeći Workflows predložak
- [x] Napisali četiri seta uputa za agente i spojili tijek rada graf
- [x] Integrirali Microsoft Learn MCP alat
- [x] Testirali lokalno s 2 smoke testa
- [x] Potvrdili ponašanje višesagentnog sustava bez potrebe za resursima u oblaku

</details>

---

## Sljedeći koraci

### Nastavite učiti

| Resurs | Opis |
|----------|-------------|
| **[Agent Framework SDK referenca](https://learn.microsoft.com/agent-framework/)** | API dokumentacija za `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP alat katalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Povežite agente s drugim MCP poslužiteljima (Bing, GitHub, prilagođeni) |
| **[Dodaj znanje (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Temeljite agente na dokumentima, vektorskim spremištima ili Bing pretraživanju |
| **[Foundry evaluacije](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mjerite kvalitetu agenata u velikom obimu s automatiziranim evaluatorima |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Potpuna referenca platforme |
| **[Foundry Toolkit - Što je novo](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Bilješke o izdanju proširenja i dnevnik promjena |

### Ideje za proširenje ovog tijeka rada

- **Dodajte 5. agenta** - Trener za intervjue koji generira vjerojatna pitanja za intervju na temelju izvještaja o nedostacima
- **Dodajte Bing alat za oslonac** - Dopustite JD Agentu da traži slične oglase za posao radi obogaćivanja zahtjeva
- **Povežite se s bazom životopisa** - Povucite profile kandidata iz baze podataka putem prilagođenog `@tool`
- **Isprobajte različite modele** - Usporedite kvalitetu i latenciju izlaza `gpt-4.1` i `gpt-4.1-mini`
- **Evaluirajte s Foundry** - Koristite značajku Evaluations za ocjenjivanje izvještaja o usklađenosti prema zlatnom skupu podataka

### Za korisnike Puta B: nadogradite na implementaciju u oblaku

Kad budete spremni za implementaciju u oblak:
1. Nabavite Azure pretplatu ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dovršite [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (kreirajte projekt, implementirajte model, dodijelite RBAC)
3. Ažurirajte svoj `.env` s krajnjom točkom Foundry projekta i imenom implementacije modela
4. Nastavite s [Modulom 06 - Implementacija u Foundry](06-deploy-to-foundry.md)

---

## Čišćenje resursa (opcionalno)

Ako želite ukloniti Azure resurse stvorene tijekom ovog radnog okruženja:

### Opcija 1: Izbrišite grupu resursa (uklanja sve)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opcija 2: Izbrišite samo hostanog agenta

1. Otvorite [ai.azure.com](https://ai.azure.com) → vaš projekt → **Build** → **Agents**.
2. Pronađite **PersonalCareerCopilot** → kliknite **Delete**.

### Opcija 3: Izbrišite implementaciju modela

1. U Foundry bočnoj traci proširite svoj projekt → **Models**.
2. Kliknite desnom tipkom miša na implementaciju modela → **Delete**.

> **Napomena o troškovima:** Hostani agenti troškove stvaraju samo dok rade. Ako zaustavite ili izbrišete agenta, nema daljnjih troškova. Implementacija modela može stvarati mali trošak za rezervirani kapacitet – izbrišite je ako ste završili.

---

**Prethodno:** [08 - Rješavanje problema](08-troubleshooting.md) · **Početna:** [Lab 02 README](../README.md) · [Početna radionice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->