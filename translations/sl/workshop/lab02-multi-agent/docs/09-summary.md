# Modul 9 - Povzetek in naslednji koraki

⏱️ ~5 min

**Čestitke!** Ustvarili, preizkusili in (če ste na poti A) uvedli večagentni potek dela z uporabo Microsoft Foundry in Foundry Toolkit za VS Code.

---

## Kaj ste ustvarili

**Ocenjevalec ujemanja življenjepisa z delovnim mestom** – večagentni gostujoči potek dela, ki:
- Prejme življenjepis + opis delovnega mesta preko HTTP (`POST /responses`)
- Izvede štiri specializirane agente v zaporedni verigi - vsak agent prenese podatke, ki jih potrebuje njegov naslednik
- Vrne oceno ujemanja (0–100 z razčlenitvijo), seznam vrzeli v veščinah in certifikatih ter personalizirano učno pot z dejanskimi povezavami do Microsoft Learn za vsako vrzel
- Pokliče Microsoft Learn MCP strežnik (`https://learn.microsoft.com/api/mcp`) za pridobitev uradnih učnih virov za vsako ugotovljeno vrzel v veščinah
- Teče kot en sam kontejniran gostujoči agent v Microsoft Foundry Agent Service

---

## Ključni naučeni koncepti

| Koncept | Kaj ste vadili |
|---------|-------------------|
| **Večagentna orkestracija** | `WorkflowBuilder` zaporedna veriga z `add_edge()` |
| **Specializacija agentov** | Štirje osredotočeni agenti presegajo enega splošno uporabnega agenta |
| **Vzorčni vzorec usmerjevalnika vsebine** | ResumeParser deluje tudi kot usmerjevalnik - tekst JD ohrani v `[JOB DESCRIPTION PASS-THROUGH]` sekciji, da ga lahko uporabljajo nadaljnji agenti (zahtevano, ker `context_mode="last_agent"` pomeni, da samo `start_executor` vidi surovo uporabniško sporočilo) |
| **Vzorčni vzorec predaje vsebine** | JD Agent prenaša `[PARSED RESUME PASS-THROUGH]` naprej, tako da MatchingAgent dobi oba profila; preprečuje OR-semantiko dvojnega sprožanja, ki jo povzročajo grafi fan-in |
| **Integracija MCP orodja** | `@tool` + `streamable_http_client` klicanje zunanjega MCP strežnika |
| **Življenjski cikel gostujočega agenta** | Scaffold → Konfiguriraj → Testiraj lokalno → Uvedi → Preveri v oblaku |
| **`context_mode="last_agent"`** | Vsak izvajalec vidi le izhod neposrednega predhodnika |
| **Potek dela Foundry Toolkit** | Čarovnik za postavitev, Agent Inspector, Vizualizator poteka dela, uvajanje z enim klikom |

---

## Kaj ste dokončali

<details open>
<summary><strong>🅰️ Pot A - naročnina Foundry</strong></summary>

- [x] Preverili nastavitve laboratorija 01: projekt, model in RBAC še aktivni
- [x] Postavili večagentni projekt z uporabo predloge Workflows
- [x] Napisali štiri nabori navodil za agente (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrirali Microsoft Learn MCP orodje z `streamable_http_client`
- [x] Povezali graf poteka dela z `WorkflowBuilder` (zaporedna cev z relacijo vsebine)
- [x] Testirali lokalno z 2 dimnimi testi (Agent Inspector) - ocena ujemanja, kartice vrzeli in URL-ji MCP
- [x] Uvedli v Foundry Agent Service (kontejnerizirano, upravljana identiteta)
- [x] Preverili v oblačni igralnici - strukturna skladnost z lokalnimi rezultati

</details>

<details open>
<summary><strong>🅱️ Pot B - Foundry Local</strong></summary>

- [x] Preverili nastavitve laboratorija 01: Foundry Local deluje z lokalnim modelom
- [x] Postavili večagentni projekt z uporabo predloge Workflows
- [x] Napisali štiri nabori navodil za agente in povezali graf poteka dela
- [x] Integrirali Microsoft Learn MCP orodje
- [x] Testirali lokalno z 2 dimnimi testi
- [x] Potrdili večagentno delovanje brez potrebe po oblačnih virih

</details>

---

## Naslednji koraki

### Nadaljujte z učenjem

| Vir | Opis |
|----------|-------------|
| **[Referenca Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | API dokumentacija za `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalog MCP orodij](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Povežite agente z drugimi MCP strežniki (Bing, GitHub, po meri) |
| **[Dodajanje znanja (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Podprite agente z dokumenti, vektorskimi shrambami ali Bing iskanjem |
| **[Foundry Evalvacije](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Merite kakovost agentov na obsegu z avtomatiziranimi evalvatorji |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Celovita referenca platforme |
| **[Foundry Toolkit - Kaj je novega](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Zapiski izdaj in dnevnik sprememb razširitve |

### Ideje za razširitev tega poteka dela

- **Dodajte 5. agenta** - Coach za intervjuje, ki proizvaja verjetna vprašanja za razgovore na podlagi poročila o vrzelih
- **Dodajte Bing orodje za podlage** - Naj JD Agent išče podobne objave delovnih mest za obogatitev zahtev
- **Povežite z bazo življenjepisov** - Pridobite profile kandidatov iz baze preko po meri narejenega `@tool`
- **Preizkusite različne modele** - Primerjajte kakovost in latenco izhodov `gpt-4.1` in `gpt-4.1-mini`
- **Evaluirajte z Foundry** - Uporabite funkcijo Evalvacij za oceno poročil o ujemanju glede na zlati nabor podatkov

### Za uporabnike poti B: Nadgradite na uvajanje v oblaku

Ko ste pripravljeni za uvajanje v oblak:
1. Pridobite naročnino Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dokončajte [Laboratorij 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (ustvarite projekt, uvedite model, nastavite RBAC)
3. Posodobite svojo `.env` z dostopno točko projekta Foundry in imenom uvajanja modela
4. Nadaljujte iz [Modul 06 - Uvedba v Foundry](06-deploy-to-foundry.md)

---

## Očistite vire (neobvezno)

Če želite odstraniti vire Azure, ustvarjene med to delavnico:

### Možnost 1: Izbrišite skupino virov (odstrani vse)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Možnost 2: Izbrišite samo gostujočega agenta

1. Odprite [ai.azure.com](https://ai.azure.com) → vaš projekt → **Build** → **Agents**.
2. Poiščite **PersonalCareerCopilot** → kliknite **Delete**.

### Možnost 3: Izbrišite uvajanje modela

1. V stranski vrstici Foundry razširite svoj projekt → **Models**.
2. Z desnim klikom na uvajanje modela → **Delete**.

> **Opomba o stroških:** Gostujoči agenti povzročajo stroške le med izvajanjem. Če ustavite ali izbrišete agenta, ni stalnih stroškov. Uvajanje modela lahko povzroča majhen strošek za rezervirano zmogljivost - izbrišite ga, če ste končali.

---

**Prejšnji:** [08 - Odpravljanje težav](08-troubleshooting.md) · **Domov:** [Lab 02 README](../README.md) · [Domov delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->