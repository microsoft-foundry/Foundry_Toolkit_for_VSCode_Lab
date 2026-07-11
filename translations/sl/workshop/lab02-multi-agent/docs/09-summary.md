# Modul 9 - Povzetek in naslednji koraki

⏱️ ~5 min

**Čestitamo!** Ustvarili, preizkusili in (če ste na poti A) uvedli večagentni potek dela z uporabo Microsoft Foundry in Foundry Toolkit za VS Code.

---

## Kaj ste ustvarili

**Ocenjevalnik ustreznosti življenjepisa za delovno mesto** - večagentni gostovani potek dela, ki:
- Prejme življenjepis + opis delovnega mesta preko HTTP (`POST /responses`)
- Izvaja štiri specializirane agente v zaporedni verigi - vsak agent posreduje podatke naslednjemu agentu
- Vrača oceno primernosti (0–100 z razčlenitvijo), seznam vrzeli v znanju in certifikatih ter personalizirano učni načrt z realnimi povezavami na Microsoft Learn za vsako vrzel
- Pokliče strežnik Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) za pridobitev uradnih učnih virov za vsako identificirano vrzel v znanju
- Deluje kot en sam vsebniki gostujoči agent v Microsoft Foundry Agent Service

---

## Ključni pojmi, ki ste jih spoznali

| Pojem | Kaj ste vadili |
|---------|-------------------|
| **Večagentna orkestracija** | Zaporedni potek dela `WorkflowBuilder` z `add_edge()` |
| **Specializacija agenta** | Štirje osredotočeni agenti prekašajo enega splošnega agenta |
| **Vzorček vsebinskega usmerjevalnika** | ResumeParser deluje tudi kot usmerjevalnik - ohranja besedilo JD v razdelku `[PREHOD OPISA DELOVNEGA MESTA]`, da ga lahko dostopajo spodnji agenti (to je potrebno, ker `context_mode="last_agent"` pomeni, da samo `start_executor` vidi surovo sporočilo uporabnika) |
| **Vzorček posredovanja vsebine** | JD Agent posreduje `[PREHOD RAZČLENJENEGA ŽIVLJENJEPISA]` naprej, da MatchingAgent dobi oba profila; preprečuje dvojno sprožilo z OR-semantiko, ki jo povzročajo grafi z združitvijo |
| **Integracija MCP orodja** | `@tool` + `streamable_http_client`, ki kliče zunanji MCP strežnik |
| **Življenjski cikel gostujočega agenta** | Nastavitev → Konfiguracija → Lokalno testiranje → Uvedba → Preverjanje v oblaku |
| **`context_mode="last_agent"`** | Vsak izvrševalec vidi samo izhod svojega neposrednega predhodnika |
| **Potek dela Foundry Toolkit** | Čarovnik za nastavitev, Agent Inspector, Vizualizator poteka dela, uvedba z enim klikom |

---

## Kaj ste zaključili

<details open>
<summary><strong>🅰️ Pot A - naročnina Foundry</strong></summary>

- [x] Preverjena nastavitev Lab 01: projekt, model in RBAC še aktivni
- [x] Ustvarjen večagentni projekt z uporabo predloge Workflows
- [x] Napisane štiri množice navodil za agente (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrirano Microsoft Learn MCP orodje z `streamable_http_client`
- [x] Povezan graf poteka dela z `WorkflowBuilder` (zaporedni potek dela z posredovanjem vsebine)
- [x] Lokalno preizkuseno s 3 osnovnimi testi (Agent Inspector) - ocena primernosti, vrzeli, in URL-ji MCP
- [x] Uvedeno v Foundry Agent Service (vsebnik, upravljana identiteta)
- [x] Preverjeno v oblačnem okolju - strukturna skladnost z lokalnimi rezultati

</details>

<details open>
<summary><strong>🅱️ Pot B - Foundry Local</strong></summary>

- [x] Preverjena nastavitev Lab 01: Foundry Local teče z lokalnim modelom
- [x] Ustvarjen večagentni projekt z uporabo predloge Workflows
- [x] Napisane štiri množice navodil za agente in povezan graf poteka dela
- [x] Integrirano Microsoft Learn MCP orodje
- [x] Lokalno preizkuseno s 3 osnovnimi testi
- [x] Preverjeno večagentno obnašanje brez potrebe po oblačnih virih

</details>

---

## Naslednji koraki

### Nadaljujte z učenjem

| Vir | Opis |
|----------|-------------|
| **[Reference Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | API dokumentacija za `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalog MCP orodij](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Povežite agente z drugimi MCP strežniki (Bing, GitHub, po meri) |
| **[Dodajte znanje (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Opremljanje agentov z dokumenti, vektorskimi skladi ali Bing iskanjem |
| **[Foundry Evaluacije](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Merjenje kakovosti agentov v obsegu z avtomatiziranimi ocenjevalci |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Celoten referenčni sistem platforme |
| **[Foundry Toolkit - Novosti](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Zapiski izdaj razširitve in spremenjeno zgodovino |

### Ideje za razširitev tega poteka dela

- **Dodajte 5. agenta** - Trenutnega intervjujev, ki izdela verjetna vprašanja na podlagi poročila o vrzelih
- **Dodajte Bing orodje za podlago** - Naj JD Agent poišče podobna delovna mesta za obogatitev zahtev
- **Povežite z bazo življenjepisov** - Pridobivanje profilov kandidatov iz baze prek lastnega `@tool`
- **Preizkusite različne modele** - Primerjajte kakovost in zakasnitev izhodov `gpt-4.1` proti `gpt-4.1-mini`
- **Ocenite z Foundry** - Uporabite funkcijo Ocene za točkovanje poročil o ustreznosti s primerjalnim zlatim naborom

### Za uporabnike poti B: Nadgradnja na uvajanje v oblak

Ko ste pripravljeni na uvajanje v oblak:
1. Pridobite naročnino Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dokončajte [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (ustvarite projekt, uvedite model, dodelite RBAC)
3. Posodobite svojo `.env` datoteko z endpointom projekta Foundry in imenom namestitve modela
4. Nadaljujte od [Modul 06 - Uvedba v Foundry](06-deploy-to-foundry.md)

---

## Počistite vire (neobvezno)

Če želite odstraniti vire Azure ustvarjene med delavnico:

### Možnost 1: Izbrišite skupino virov (odstrani vse)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Možnost 2: Izbrišite samo gostujočega agenta

1. Odprite [ai.azure.com](https://ai.azure.com) → vaš projekt → **Build** → **Agents**.
2. Poiščite **PersonalCareerCopilot** → kliknite **Delete**.

### Možnost 3: Izbrišite namestitev modela

1. V stranski vrstici Foundry razširite svoj projekt → **Models**.
2. Z desno tipko kliknite namestitev modela → **Delete**.

> **Opomba o stroških:** Gostujoči agenti povzročajo stroške samo med izvajanjem. Če ustavite ali izbrišete agenta, ni nadaljnjih stroškov. Namestitev modela lahko povzroča majhen strošek zaradi rezervirane zmogljivosti - izbrišite jo, če ste končali.

---

**Prej:** [08 - Odpravljanje težav](08-troubleshooting.md) · **Domov:** [Lab 02 README](../README.md) · [Domača stran delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->