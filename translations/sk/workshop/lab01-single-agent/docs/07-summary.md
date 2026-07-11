# Modul 7 - Súhrn a ďalšie kroky

⏱️ ~5 min

**Gratulujeme!** Vytvorili ste, otestovali a (ak ste na ceste A) nasadili hostovaného AI agenta pomocou Microsoft Foundry a Foundry Toolkit pre VS Code.

---

## Čo ste vytvorili

Agenta **"Vysvetli mi to ako manažérovi"**, ktorý:
- Prijíma technické hlásenia incidentov alebo operačné aktualizácie cez HTTP (`POST /responses`)
- Prekladá ich do jednoduchých výkonných zhrnutí
- Nasleduje štruktúrovaný výstupný formát (Čo sa stalo / Dopad na biznis / Ďalší krok)
- Odmieta žiadosti mimo témy a pokusy o injektáž promptu
- Beží ako kontajnerizovaný hostovaný agent v Microsoft Foundry Agent Service

---

## Kľúčové koncepty, ktoré ste sa naučili

| Koncept | Čo ste precvičovali |
|---------|-------------------|
| **Architektúra Agent Frameworku** | Pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Životný cyklus hostovaného agenta** | Scaffold → Konfigurácia → Lokálne testovanie → Nasadenie → Overenie v cloude |
| **Inžinierstvo systémových promptov** | Rola, publikum, formát výstupu, pravidlá, bezpečnostné obmedzenia a príklady |
| **Rozdiely medzi lokálnym a hostovaným** | Identita (osobná poverenia vs. spravovaná identita), endpoint, sieťová cesta |
| **Bezpečnostné hranice** | Obrana proti injektácii promptu, dodržiavanie rolí, elegantné spracovanie okrajových prípadov |
| **Workflow Foundry Toolkit** | Vytvorenie projektu, nasadenie modelu, scaffolding agenta, Agent Inspector, one-click deploy |

---

## Čo ste dokončili

### Cesta A (Foundry predplatné)

- [x] Nastavili ste Foundry Toolkit a vytvorili Foundry projekt s nasadeným modelom
- [x] Scaffoldovali hostovaného agenta s automaticky generovanou štruktúrou projektu
- [x] Napísali štruktúrované inštrukcie pre agenta s bezpečnostnými pravidlami
- [x] Testovali lokálne s 3 funkčnými scenármi (Agent Inspector)
- [x] Nasadili do Foundry Agent Service (kontajnerizované)
- [x] Overili v cloudovom playgrounde so 4 testami okrajových prípadov/bezpečnosti

### Cesta B (Foundry Local)

- [x] Nastavili Foundry Toolkit s lokálnym modelovým endpointom
- [x] Scaffoldovali projekt hostovaného agenta
- [x] Napísali štruktúrované inštrukcie pre agenta s bezpečnostnými pravidlami
- [x] Testovali lokálne s 3 funkčnými scenármi
- [x] Overili správanie agenta bez potreby cloudových zdrojov

---

## Ďalšie kroky

### Pokračujte v učení

| Zdroje | Popis |
|----------|-------------|
| **[Lab 02 - Orchestrácia viacerých agentov](../../lab02-multi-agent/docs/README.md)** | Vytvorte workflow so 4 agentmi (Resume → Evaluátor pracovnej vhodnosti) s orchestráciou |
| **[Pridajte nástroje k svojmu agentovi](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Pripojte API, databázy alebo vlastné funkcie cez Katalóg nástrojov |
| **[Pridajte znalosti (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Zakladajte svojho agenta na dokumentoch, vektorových storech alebo Bing vyhľadávaní |
| **[Dokumentácia Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Kompletná referencia platformy |
| **[Agent Framework SDK referencia](https://learn.microsoft.com/agent-framework/)** | API dokumentácia pre balík `agent-framework` |
| **[Foundry Toolkit - Novinky](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Poznámky k vydaniu rozšírenia a changelog |

### Nápady na rozšírenie agenta

- **Pridajte nástroj na dátum** - Nech agent zahrnie kontext „k dnešnému dňu“ v zhrnutiach
- **Pripojte sa k databáze incidentov** - Získavajte skutočné detaily incidentov cez nástrojovú funkciu
- **Pridajte nástroj pre Bing grounding** - Nech agent vyhľadáva aktuálne správy pre ďalší kontext
- **Vyskúšajte rôzne modely** - Porovnajte kvalitu výstupu `gpt-4.1` vs. `gpt-4.1-mini`
- **Vyhodnoťte pomocou Foundry** - Použite funkciu Evaluations na meranie kvality agenta vo veľkom

### Pre používateľov cesty B: Prejdite na nasadenie v cloude

Keď budete pripravení nasadiť do cloudu:
1. Získajte Azure predplatné ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dokončite [Modul 01, Nastavenie](01-setup.md#step-2-set-up-based-on-your-access) (vytvorenie projektu, nasadenie modelu, priradenie RBAC)
3. Aktualizujte svoj `.env` s endpointom projektu Foundry a názvom nasadenia modelu
4. Pokračujte od [Modul 05 - Nasadenie do Foundry](05-deploy-to-foundry.md)

---

## Vyčistenie zdrojov (voliteľné)

Ak chcete odstrániť Azure zdroje vytvorené počas tohto workshopu:

### Možnosť 1: Odstrániť skupinu zdrojov (odstráni všetko)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Možnosť 2: Odstrániť len hostovaného agenta

1. Otvorte [ai.azure.com](https://ai.azure.com) → svoj projekt → **Build** → **Agents**.
2. Kliknite na svojho agenta → kliknite na **Delete**.

### Možnosť 3: Odstrániť nasadenie modelu

1. V Foundry bočnom paneli rozbaľte svoj projekt → **Models**.
2. Kliknite pravým tlačidlom na nasadenie modelu → **Delete**.

> **Poznámka o nákladoch:** Hostovaní agenti účtujú náklady len počas chodu. Ak agenta zastavíte alebo odstránite, nebudú účtované žiadne priebežné poplatky. Nasadenie modelu môže spôsobiť malý poplatok za rezervovanú kapacitu – odstráňte ho, ak ste skončili.

---

**Predchádzajúce:** [06 - Overenie v Playground](06-verify-in-playground.md) · **Ďalšie:** [08 - Riešenie problémov (referencia) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->