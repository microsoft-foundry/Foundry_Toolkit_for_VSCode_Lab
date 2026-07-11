# Modul 9 - Shrnutí a další kroky

⏱️ ~5 min

**Gratulujeme!** Vybudovali jste, otestovali a (pokud jste na cestě A) nasadili víceagentní pracovní postup pomocí Microsoft Foundry a Foundry Toolkit pro VS Code.

---

## Co jste vybudovali

**Resume → Job Fit Evaluator** - víceagentní hostovaný pracovní postup, který:
- Přijme životopis + popis práce přes HTTP (`POST /responses`)
- Spustí čtyři specializované agenty v sekvenčním řetězci - každý agent předává data, která jeho nástupce potřebuje
- Vrací skóre shody (0–100 s rozpisem), seznam mezer ve dovednostech a certifikacích a personalizovanou vzdělávací cestu s reálnými odkazy Microsoft Learn pro každou mezeru
- Volá Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`) pro získání oficiálních vzdělávacích zdrojů pro každou identifikovanou mezeru ve dovednostech
- Běží jako jediný kontejnerizovaný hostovaný agent ve službě Microsoft Foundry Agent Service

---

## Klíčové koncepty, které jste se naučili

| Koncept | Co jste si procvičili |
|---------|-------------------|
| **Multi-agentní orchestraci** | Sekvenční pipeline `WorkflowBuilder` s `add_edge()` |
| **Specializaci agentů** | Čtyři specializovaní agenti překonají jednoho obecného agenta |
| **Pattern Content Router** | ResumeParser slouží také jako router - zachovává text JD v sekci `[JOB DESCRIPTION PASS-THROUGH]`, aby k ní mohli přistupovat downstream agenti (nutné, protože `context_mode="last_agent"` znamená, že pouze `start_executor` vidí surovou uživatelskou zprávu) |
| **Pattern Content Relay** | JD Agent přeposílá `[PARSED RESUME PASS-THROUGH]` dál, takže MatchingAgent dostane oba profily; zabraňuje OR-semantiky dvojitému spuštění, které způsobují fan-in grafy |
| **Integrace MCP nástroje** | `@tool` + `streamable_http_client` volající externí MCP server |
| **Životní cyklus hostovaného agenta** | Scaffold → Konfigurace → Lokální testování → Nasazení → Ověření v cloudu |
| **`context_mode="last_agent"`** | Každý executor vidí pouze výstup svého přímého předchůdce |
| **Foundry Toolkit workflow** | Scaffold průvodce, Agent Inspector, Workflow Visualizer, nasazení jedním kliknutím |

---

## Co jste dokončili

<details open>
<summary><strong>🅰️ Cesta A - Předplatné Foundry</strong></summary>

- [x] Ověřili nastavení Lab 01: projekt, model a RBAC stále aktivní
- [x] Vytvořili víceagentní projekt pomocí šablony Workflows
- [x] Napsali čtyři sady instrukcí agentů (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrovali Microsoft Learn MCP nástroj s `streamable_http_client`
- [x] Propojili workflow graf pomocí `WorkflowBuilder` (sekvenční pipeline s přenosem obsahu)
- [x] Testovali lokálně se 3 smoke testy (Agent Inspector) - skóre, karty mezer a URL MCP
- [x] Nasadili do Foundry Agent Service (kontejnerizované, spravovaná identita)
- [x] Ověřili v cloud playground - strukturální shoda s lokálními výsledky

</details>

<details open>
<summary><strong>🅱️ Cesta B - Foundry Local</strong></summary>

- [x] Ověřili nastavení Lab 01: Foundry Local běží na lokálním modelu
- [x] Vytvořili víceagentní projekt pomocí šablony Workflows
- [x] Napsali čtyři sady instrukcí agentů a propojili workflow graf
- [x] Integrovali Microsoft Learn MCP nástroj
- [x] Testovali lokálně se 3 smoke testy
- [x] Ověřili víceagentní chování bez potřeby cloudových zdrojů

</details>

---

## Další kroky

### Pokračujte ve studiu

| Zdroj | Popis |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API dokumentace pro `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Připojení agentů k dalším MCP serverům (Bing, GitHub, vlastní) |
| **[Přidání znalostí (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ukotvení agentů dokumenty, vektorovými úložišti nebo vyhledáváním Bing |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Měření kvality agentů ve velkém s automatizovanými evaluátory |
| **[Microsoft Foundry dokumentace](https://learn.microsoft.com/azure/foundry/)** | Kompletní reference platformy |
| **[Foundry Toolkit - Co je nového](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Poznámky k vydání rozšíření a changelog |

### Nápady na rozšíření tohoto workflow

- **Přidat 5. agenta** - Trenéra na pohovor, který vytvoří pravděpodobné otázky na základě zprávy o mezerách
- **Přidat Bing grounding tool** - Nechat JD Agenta vyhledávat podobné pracovní nabídky pro obohacení požadavků
- **Připojit k databázi životopisů** - Tahat profily kandidátů z databáze pomocí vlastního `@tool`
- **Zkoušet různé modely** - Porovnat kvalitu a dobu odezvy modelů `gpt-4.1` vs. `gpt-4.1-mini`
- **Vyhodnocovat pomocí Foundry** - Použít funkci Evaluations pro skórování zpráv shody proti zlaté sadě dat

### Pro uživatele cesty B: Upgrade na cloudové nasazení

Až budete připraveni nasadit do cloudu:
1. Získejte Azure předplatné ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dokončete [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (vytvořte projekt, nasaďte model, přiřaďte RBAC)
3. Aktualizujte svůj `.env` s koncovým bodem projektu Foundry a názvem nasazení modelu
4. Pokračujte od [Modulu 06 - Deploy to Foundry](06-deploy-to-foundry.md)

---

## Vyčištění zdrojů (volitelné)

Pokud chcete odstranit Azure zdroje vytvořené během tohoto workshopu:

### Možnost 1: Smazat skupinu zdrojů (odstraní vše)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Možnost 2: Smazat pouze hostovaného agenta

1. Otevřete [ai.azure.com](https://ai.azure.com) → svůj projekt → **Build** → **Agents**.
2. Najděte **PersonalCareerCopilot** → klikněte na **Delete**.

### Možnost 3: Smazat nasazení modelu

1. V postranním panelu Foundry rozbalte svůj projekt → **Models**.
2. Pravým tlačítkem klikněte na nasazení modelu → **Delete**.

> **Poznámka k nákladům:** Hostovaní agenti účtují náklady jen při běhu. Pokud zastavíte nebo smažete agenta, neexistují žádné průběžné poplatky. Nasazení modelu může způsobit malý poplatek za vyhrazenou kapacitu – smažte ho, pokud jste hotovi.

---

**Předchozí:** [08 - Troubleshooting](08-troubleshooting.md) · **Domů:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->