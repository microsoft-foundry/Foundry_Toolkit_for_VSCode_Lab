# Modul 9 - Zhrnutie a ďalšie kroky

⏱️ ~5 min

**Gratulujeme!** Zostavili ste, otestovali a (ak ste na ceste A) nasadili viacagentný pracovný tok pomocou Microsoft Foundry a Foundry Toolkit pre VS Code.

---

## Čo ste vytvorili

**Resume → Job Fit Evaluator** - viacagentný hosťovaný pracovný tok, ktorý:
- Prijíma životopis + popis pracovnej pozície cez HTTP (`POST /responses`)
- Spúšťa štyroch špecializovaných agentov v sekvenčnej pipeline - každý agent posiela dáta, ktoré potrebuje jeho nasledovník
- Vracia skóre zhody (0–100 s rozpisom), zoznam medzier v zručnostiach a certifikáciách a personalizovanú cestu učenia s reálnymi odkazmi na Microsoft Learn pre každú medzeru
- Volá MCP server Microsoft Learn (`https://learn.microsoft.com/api/mcp`), aby získal oficiálne zdroje učenia pre každú zistenú medzeru v zručnostiach
- Beží ako jeden kontajnerizovaný hosťovaný agent v Microsoft Foundry Agent Service

---

## Kľúčové naučené koncepty

| Koncept | Čo ste si precvičili |
|---------|-------------------|
| **Multi-agent orchestration** | Sekvenčná pipeline `WorkflowBuilder` s `add_edge()` |
| **Agenti špecializácie** | Štyria zameraní agenti prekonávajú jedného všeobecného agenta |
| **Pattern Content Router** | ResumeParser plní aj úlohu routera - uchováva text JD v sekcii `[JOB DESCRIPTION PASS-THROUGH]`, aby k nemu mali prístup ďalší agenti (potrebné, pretože `context_mode="last_agent"` znamená, že len `start_executor` vidí surovú užívateľskú správu) |
| **Pattern Content Relay** | Agent JD posiela ďalej `[PARSED RESUME PASS-THROUGH]`, takže MatchingAgent dostane oba profily; zabraňuje dvojitému spusteniu OR-semantikou, ktorú spôsobujú fan-in grafy |
| **Integrácia MCP nástroja** | `@tool` + `streamable_http_client` volanie externého MCP servera |
| **Životný cyklus hosťovaného agenta** | Scaffold → Konfigurácia → Lokálne testovanie → Nasadenie → Overenie v cloude |
| **`context_mode="last_agent"`** | Každý executor vidí iba výstup svojho priamého predchodcu |
| **Foundry Toolkit workflow** | Príručka scaffoldingu, Agent Inspector, Workflow Visualizer, nasadenie na jedno kliknutie |

---

## Čo ste dokončili

<details open>
<summary><strong>🅰️ Cesta A - Foundry predplatné</strong></summary>

- [x] Overená inštalácia Lab 01: projekt, model a RBAC stále aktívne
- [x] Scaffoldovali multi-agentný projekt pomocou šablóny Workflows
- [x] Napísali štyri sady inštrukcií pre agentov (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrovali Microsoft Learn MCP nástroj so `streamable_http_client`
- [x] Prepojili graf pracovného toku pomocou `WorkflowBuilder` (sekvenčná pipeline s relay obsahu)
- [x] Lokálne otestované s 3 testami sanity (Agent Inspector) - skóre zhody, gap karty a MCP URL
- [x] Nasadené do Foundry Agent Service (kontajnerizované, spravovaná identita)
- [x] Overené v cloud playground - štrukturálna zhodnosť s lokálnymi výsledkami

</details>

<details open>
<summary><strong>🅱️ Cesta B - Foundry Local</strong></summary>

- [x] Overená inštalácia Lab 01: Foundry Local beží s lokálnym modelom
- [x] Scaffoldovali multi-agentný projekt pomocou šablóny Workflows
- [x] Napísali štyri sady inštrukcií pre agentov a prepojili graf pracovného toku
- [x] Integrovali Microsoft Learn MCP nástroj
- [x] Lokálne otestované s 3 testami
- [x] Overené multi-agentné správanie bez potreby cloudových zdrojov

</details>

---

## Ďalšie kroky

### Pokračujte v učení

| Zdroj | Popis |
|----------|-------------|
| **[Agent Framework SDK referencia](https://learn.microsoft.com/agent-framework/)** | API dokumentácia pre `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalóg MCP nástrojov](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Pripojenie agentov na ďalšie MCP servery (Bing, GitHub, vlastné) |
| **[Pridať vedomosti (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Založiť agentov na dokumentoch, vektorových úložiskách alebo Bing vyhľadávaní |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Meranie kvality agentov vo veľkom so samohodnotením |
| **[Microsoft Foundry dokumentácia](https://learn.microsoft.com/azure/foundry/)** | Kompletná referenčná platforma |
| **[Foundry Toolkit - Čo je nové](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Poznámky k vydaniu a changelog rozšírenia |

### Nápady na rozšírenie tohto pracovného toku

- **Pridať 5. agenta** - Kouča pre pohovory, ktorý vytvára pravdepodobné otázky na základe správy o medzerách
- **Pridať nástroj Bing grounding** - Nechať JD agenta vyhľadávať podobné pracovné ponuky na obohatenie požiadaviek
- **Prepojiť s databázou životopisov** - Sťahovať profily kandidátov z databázy cez vlastný `@tool`
- **Vyskúšať rôzne modely** - Porovnať kvalitu a latenciu výstupu modelov `gpt-4.1` vs. `gpt-4.1-mini`
- **Vyhodnotiť pomocou Foundry** - Použiť funkciu Evaluations na skórovanie správ o zhode voči zlatej dátovej množine

### Pre používateľov Cesty B: Prejdite na cloudové nasadenie

Keď budete pripravení nasadiť do cloudu:
1. Získajte Azure predplatné ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dokončite [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (vytvorte projekt, nasadte model, priraďte RBAC)
3. Aktualizujte svoj `.env` s Foundry projektovým endpointom a názvom nasadenia modelu
4. Pokračujte z [Modulu 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Odstránenie zdrojov (voliteľné)

Ak chcete odstrániť Azure zdroje vytvorené počas tohto workshopu:

### Možnosť 1: Odstrániť resource group (odstráni všetko)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Možnosť 2: Odstrániť iba hosťovaného agenta

1. Otvorte [ai.azure.com](https://ai.azure.com) → váš projekt → **Build** → **Agents**.
2. Nájdite **PersonalCareerCopilot** → kliknite na **Delete**.

### Možnosť 3: Odstrániť nasadenie modelu

1. V Foundry bočnom paneli rozbaľte svoj projekt → **Models**.
2. Kliknite pravým tlačidlom na nasadenie modelu → **Delete**.

> **Poznámka o nákladoch:** Hosťovaní agenti účtujú poplatok iba keď bežia. Ak agenta zastavíte alebo odstránite, neplatíte ďalej. Nasadenie modelu môže spôsobiť malý poplatok za rezervovanú kapacitu - odstráňte ho, ak ste skončili.

---

**Predchádzajúce:** [08 - Riešenie problémov](08-troubleshooting.md) · **Domov:** [Lab 02 README](../README.md) · [Domov workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->