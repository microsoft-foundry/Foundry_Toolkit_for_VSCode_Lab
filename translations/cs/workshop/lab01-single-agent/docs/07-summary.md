# Modul 7 - Shrnutí & Další kroky

⏱️ ~5 min

**Gratulujeme!** Vytvořili jste, otestovali a (pokud jste na cestě A) nasadili hostovaného AI agenta pomocí Microsoft Foundry a Foundry Toolkit pro VS Code.

---

## Co jste vytvořili

Agenta **„Vysvětli to jako by to byl výkonný ředitel“**, který:
- Přijímá technické incidentní zprávy nebo provozní aktualizace přes HTTP (`POST /responses`)
- Překládá je do jednoduše srozumitelných shrnutí pro vedení
- Dodržuje strukturovaný formát výstupu (Co se stalo / Obchodní dopad / Další krok)
- Odmítá nesouvisející požadavky a pokusy o prompt injection
- Běží jako kontejnerizovaný hostovaný agent v Microsoft Foundry Agent Service

---

## Klíčové pojmy, které jste se naučili

| Pojem | Co jste cvičili |
|---------|-------------------|
| **Architektura Agent Frameworku** | Pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Životní cyklus hostovaného agenta** | Scaffold → Konfigurace → Lokální test → Nasazení → Ověření v cloudu |
| **Inženýrství systémových výzev (prompt engineering)** | Role, publikum, formát výstupu, pravidla, bezpečnostní omezení a příklady |
| **Rozdíly mezi lokálním a hostovaným** | Identita (osobní pověření vs. spravovaná identita), endpoint, síťová cesta |
| **Bezpečnostní hranice** | Obrana proti prompt injection, dodržování role, zdvořilé řešení hraničních případů |
| **Workflow Foundry Toolkitu** | Vytvoření projektu, nasazení modelu, scaffolding agenta, Agent Inspector, nasazení jedním klikem |

---

## Co jste dokončili

### Cesta A (Foundry předplatné)

- [x] Nastavili Foundry Toolkit a vytvořili Foundry projekt s nasazeným modelem
- [x] Scaffoldovali hostovaného agenta s automaticky generovanou strukturou projektu
- [x] Napsali strukturované pokyny pro agenta včetně pravidel bezpečnosti
- [x] Lokálně otestovali 3 funkční scénáře (Agent Inspector)
- [x] Nasadili do Foundry Agent Service (kontejnerizováno)
- [x] Ověřili v cloudovém playgroundu se 4 hraničními/bezpečnostními testy

### Cesta B (Foundry Local)

- [x] Nastavili Foundry Toolkit s lokálním endpointem modelu
- [x] Scaffoldovali hostovaný agent projekt
- [x] Napsali strukturované pokyny pro agenta včetně pravidel bezpečnosti
- [x] Lokálně otestovali 3 funkční scénáře
- [x] Ověřili chování agenta bez potřeby cloudových zdrojů

---

## Další kroky

### Pokračujte ve vzdělávání

| Zdroje | Popis |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Vytvořte pracovní postup se 4 agenty (Resume → Job Fit Evaluator) s orchestrace vzory |
| **[Přidání nástrojů do vašeho agenta](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Připojení API, databází nebo vlastních funkcí přes Tool Catalog |
| **[Přidání znalostí (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Založte agenta na dokumentech, vektorových úložištích nebo vyhledávání Bing |
| **[Microsoft Foundry dokumentace](https://learn.microsoft.com/azure/foundry/)** | Kompletní referenční příručka platformy |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | API dokumentace balíčku `agent-framework` |
| **[Foundry Toolkit - Co je nového](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Poznámky k vydání rozšíření a changelog |

### Nápady, jak rozšířit svého agenta

- **Přidejte nástroj pro datum** - Nechte agenta zahrnout kontext "aktuálního dne" do shrnutí
- **Připojte se k databázi incidentů** - Stahujte skutečné údaje o incidentech pomocí funkce nástroje
- **Přidejte nástroj pro vyhledávání Bing** - Nechte agenta dohledat aktuální zprávy pro další kontext
- **Vyzkoušejte různé modely** - Porovnejte kvalitu výstupu `gpt-4.1` vs. `gpt-4.1-mini`
- **Ohodnoťte s Foundry** - Použijte funkci Evaluations k měření kvality agenta ve velkém měřítku

### Pro uživatele cesty B: Přechod na nasazení v cloudu

Jakmile budete připraveni nasadit do cloudu:
1. Získejte předplatné Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dokončete [Modul 01, Nastavení](01-setup.md#step-2-set-up-based-on-your-access) (vytvoření projektu, nasazení modelu, přiřazení RBAC)
3. Aktualizujte svůj `.env` s Foundry endpointem projektu a názvem nasazení modelu
4. Pokračujte od [Modulu 05 - Nasazení do Foundry](05-deploy-to-foundry.md)

---

## Vyčištění zdrojů (volitelné)

Pokud chcete odstranit Azure zdroje vytvořené během tohoto workshopu:

### Možnost 1: Smazat skupinu zdrojů (odstraní vše)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Možnost 2: Smazat pouze hostovaného agenta

1. Otevřete [ai.azure.com](https://ai.azure.com) → svůj projekt → **Build** → **Agents**.
2. Klikněte na svého agenta → klikněte na **Delete**.

### Možnost 3: Smazat nasazení modelu

1. V postranním panelu Foundry rozbalte svůj projekt → **Models**.
2. Klikněte pravým tlačítkem na nasazení modelu → **Delete**.

> **Poznámka ke nákladům:** Hostovaní agenti účtují náklady pouze při běhu. Pokud zastavíte nebo smažete agenta, neplatíte nic dál. Nasazení modelu může účtovat malý poplatek za rezervovanou kapacitu - smazat ho, pokud skončíte.

---

**Předchozí:** [06 - Ověření v Playgroundu](06-verify-in-playground.md) · **Další:** [08 - Odstraňování problémů (Reference) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->