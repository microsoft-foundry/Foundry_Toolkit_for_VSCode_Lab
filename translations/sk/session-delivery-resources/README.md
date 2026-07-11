# Ako viesť túto reláciu

Ďakujeme, že vediete túto reláciu!

Pred uskutočnením workshopu prosím:

1. Prečítajte si tento dokument a všetky zahrnuté zdroje celý.
2. Pozrite si záznam z vedenia relácie a prechod workshopom krok za krokom.
3. Prejdite oba praktické laboratórne cvičenia na vlastnom počítači **aspoň raz** pred podujatím.
4. Overte si svoj projekt Microsoft Foundry, nasadenia modelov a kvóty.
5. Ak čokoľvek nie je jasné, kontaktujte správcu.

---

## Zhrnutie súborov

| Zdroj                         | Odkaz                                                                             | Popis                                                                                     |
|-------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Prezentácia workshopu         | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                    | Prezentácia k workshopu s poznámkami pre lektora a vloženými demo videami                  |
| Záznam vedenia relácie        | _Bude poskytnutý správcom_                                                      | Záznam úvodu do workshopu a prechodu prezentáciou                                          |
| Záznam workshopu krok za krokom | _Bude poskytnutý správcom_                                                    | Kompletný záznam oboch laboratórnych cvičení z pohľadu účastníka                           |
| Dokumentácia workshopu        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Zdrojové úložisko, README laboratórií, moduly krok za krokom                              |
| Laboratórium 01 - jediný agent | [Lab 01](../workshop/lab01-single-agent/README.md)                             | Praktické cvičenie: vytvorte, otestujte a nasadte hosťovaného agenta *Explain Like I'm an Executive* |
| Laboratórium 02 - workflow s viacerými agentmi | [Lab 02](../workshop/lab02-multi-agent/README.md)                    | Praktické cvičenie: vytvorte workflow so 4 agentmi *Resume to Job Fit Evaluator*           |
| Demo 1: Výkonný agent         | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                            | Demo z Lab 01: preložiť technický žargón do výkonného súhrnu                               |
| Demo 2: Hodnotiť zhody životopisu pre prácu | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Demo z Lab 02: workflow so 4 agentmi, ktorý hodnotí zhody životopisu a vytvára odporúčania  |

> **Poznámka pre školiteľov:** Prezentácia a odkazy na video budú pridané po zverejnení záznamov. Do vtedy kontaktujte správcu (pozri [Kontakty](#kontakty)) pre najnovšie materiály.

---

## Začnite

Tento workshop učí vývojárov, ako vytvárať, testovať a nasadzovať AI agentov do **Microsoft Foundry Agent Service** ako **Hosted Agents** kompletne z VS Code pomocou rozšírenia **Microsoft Foundry Toolkit**.

Workshop je rozdelený do viacerých častí vrátane prezentácie, **2 živých demo** a **2 praktických laboratórií**.

### Časový harmonogram

#### Plná dodávka (cca 2 hodiny)

| Čas            | Popis                                                               |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Úvod: hosťovaní agenti, Foundry Agent Service a toolkit              |
| 10:00 - 20:00   | Demo: Výkonný agent krok za krokom                                  |
| 20:00 - 60:00   | Laboratórium 01 - jediný agent (tvorba, lokálny test, nasadenie, playground) |
| 60:00 - 110:00  | Laboratórium 02 - workflow s viacerými agentmi (Resume to Job Fit Evaluator) |
| 110:00 - 120:00 | Zhrnutie, otázky a odpovede, zdroje na pokračovanie                  |

#### Krátka dodávka (cca 75 minút)

| Čas          | Popis                                                  |
|---------------|--------------------------------------------------------|
| 0:00 - 10:00  | Úvod a prehľad                                         |
| 10:00 - 20:00 | Demo: Výkonný agent                                    |
| 20:00 - 70:00 | Iba Laboratórium 01 (účastníkov nasmerujte na Lab 02 ako samostatné štúdium) |
| 70:00 - 75:00 | Zhrnutie a otázky a odpovede                           |

### Príprava

| Zdroj                          | Odkaz                                                                                  | Popis                                             |
|--------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------|
| Dokumentácia workshopu         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)     | Dokumentácia workshopu a zdroj                     |
| Inštrukcie k Lab 01             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                        | Praktické cvičenie: jediný hosťovaný agent         |
| Inštrukcie k Lab 02             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                          | Praktické cvičenie: workflow viacerých agentov     |
| Kontrolný zoznam predpokladov   | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)        | Požadované nástroje, účty a prístup do Azure       |
| Rýchly štart pre hosťovaných agentov (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Oficiálny rýchly štart pre nasadenie hosťovaného agenta pomocou `azd` |
| Dostupnosť hosťovaných agentov podľa regiónov | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Podporované regióny pre hosťovaných agentov (preview) |

### Požiadavky na školiteľa

Pred dodaním sa uistite, že máte:

- **Azure predplatné** s povolením vytvárať zdroje (vlastník alebo spolupracovník na skupine zdrojov).
- Prístup k **Microsoft Foundry projektu** v [regióne, ktorý podporuje hosťovaných agentov](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvótu pre **gpt-4.1** (alebo **gpt-4.1-mini**) vo vašom Foundry projekte.
- Nasledujúce nástroje nainštalované:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Rozšírenie Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (voliteľné)
  - Python 3.10 alebo novší

Pred dodaním aspoň raz spustite [Rýchly štart hosťovaných agentov s `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd), aby ste mali overený projekt Foundry, nasadenie modelu a Azure Container Registry, ku ktorým sa môžete odvolať, ak účastník bude mať problém.

---

## Prechod prezentáciou

Prezentácia nasleduje podobný tok ako laboratóriá. Navrhované body na hovorenie pre každú sekciu:

| Sekcia                      | Kľúčová správa                                                                                              |
|-----------------------------|------------------------------------------------------------------------------------------------------------|
| Názov a agenda              | Predstavte workshop ako *VS Code do Foundry* bez potreby prepínania portálu.                               |
| Prečo hosťovaní agenti?    | Spravované runtime, nasadenie založené na ACR, OpenAI-kompatibilné `/responses` API, viazané na projekty Foundry. |
| Architektonický diagram    | Prejdite [architektúru z README](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.        |
| Anatomia hosťovaného agenta | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - vysvetlite, čo robí každý súbor.                |
| Živé demo: Výkonný agent   | Prepnite do VS Code a spustite demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) krok za krokom (pozri [Demo 1](#demo-1-výkonný-agent)). |
| Živé demo: Resume to Job Fit Evaluator | Prepnite do VS Code a spustite 4-agentové demo [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (pozri [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Stručný úvod do Lab 01     | Odovzdajte účastníkom. Ukážte na [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Vzory multi-agentov        | Sekvenčné vs súbežné vs odovzdanie - predvedenie pred začiatkom Lab 02.                                    |
| Stručný úvod do Lab 02     | Odovzdajte účastníkom. Ukážte na [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Zhrnutie a zdroje          | Odkazy na ďalšie štúdium zo sekcie [Ďalšie zdroje](#dodatočné-zdroje).                                 |

---

## Demo

Sú zahrnuté dve živé demo. Vyhraďte si na každé 10 minút.

| Demo                 | Laboratórium | Súbory                                                     | Čo ukázať                                                    |
|----------------------|--------------|------------------------------------------------------------|--------------------------------------------------------------|
| Výkonný agent        | Lab 01       | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Jeden hosťovaný agent; preložiť technický žargón do výkonného zhrnutia |
| Resume to Job Fit Evaluator | Lab 02       | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orchestrácia so 4 agentmi; hodnotenie zhody životopisu a generovanie odporúčania |

### Demo 1: Výkonný agent

Samostatný agent v [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Použite ho ako 10-minútové demo pred Lab 01.

1. Otvorte [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) a prejdite definíciu agenta (systémový prompt, model, framework).
2. Stlačte `F5` na spustenie **Agent Inspector** lokálne.
3. Vložte ukážkový prompt z [README](../README.md#see-it-in-action) a ukážte odpoveď ako exekutívny súhrn.
4. Ukážte [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) a [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) a vysvetlite nasadzovacie artefakty.
5. Predveďte tok nasadenia (Docker build, ACR push, vytvorenie hosťovaného agenta) bez čakania na dokončenie.

### Demo 2: Resume to Job Fit Evaluator

Workflow so 4 agentmi v [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Použite ho ako 10-minútové demo pred Lab 02.

1. Otvorte [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) a ukážte, ako sú štyria agenti prepojení v sekvenčnej orchestrácii.
2. Stlačte `F5` na spustenie **Agent Inspector** pre multi-agent workflow.
3. V Inspektorovi vložte krátky popis pracovnej pozície a ukážkový životopis do chatu.
4. Prejdite pipeline so štyrmi agentmi: parser životopisu, extraktor požiadaviek na prácu, hodnotiteľ zhody a autor odporúčaní.
5. Poukážte, ako výstup každého sub-agenta sa stáva kontextom ďalšieho agenta, zdôraznite vzor odovzdania.
6. Ukážte [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) v porovnaní s ekvivalentom pre jedného agenta z Demo 1.

---

## Tipy pre vedenie relácie

- **Nastavte očakávania hneď na začiatku.** Hosťovaní agenti sú vo verzii preview - jasne povedzte obmedzenia regiónov a kvóty, aby účastníci neboli prekvapení počas laboratória.
- **Najprv spustite úlohu predpokladov.** Obe laboratóriá obsahujú úlohu `Validate prerequisites` vo VS Code - nechajte účastníkov ju spustiť pred tým, ako začnú písať kód.
- **Majte Agent Inspector stále viditeľný.** Väčšina "aha" momentov nastáva, keď účastníci vidia rozsvietený lokálny cyklus požiadaviek `/responses`.
- **Majte záložný projekt.** Ak účastníkov projekt Foundry narazí na kvótový limit, zdieľajte predpripravený projekt pre krok nasadenia, aby ste neblokovali skupinu.
- **Párujte účastníkov.** Lab 02 (multi-agent) je podstatne jednoduchšie, keď si účastníci môžu prejsť orchestráciu s partnerom.
- **Používajte moduly z dokumentácie ako kontrolné body.** Každá zložka `docs/` v laboratóriách je rozdelená do 8 číslovaných modulov - použite ich ako prirodzené body na pauzu.
- **Prednačítajte základný Docker obraz** na zdieľaných laboratórnych strojoch, aby ste sa vyhli limitom rýchlosti registru.

---

## Riešenie problémov počas vedenia

| Príznak                                     | Prvá vec na vyskúšanie                                                                        |
|---------------------------------------------|------------------------------------------------------------------------------------------------|
| Agent Inspector sa nedokáže pripojiť         | Overte, že port `8088` je voľný a úloha `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` beží. |
| Debugger sa nepripája                        | Skontrolujte, či je port `5679` voľný; reštartujte VS Code, ak `debugpy` už beží.              |
| `azd up` zlyháva s chybou autentifikácie    | Spustite `az login` a `azd auth login`, uistite sa, že je vybraný správny tenant.              |
| Nasadenie uviazne pri pushi do ACR           | Skontrolujte, či beží Docker Desktop a používateľ má právo `AcrPush` na registry.              |
| Model vracia 404 / nasadenie nenájdené      | Názov nasadenia modelu v `agent.yaml` musí zodpovedať nasadeniu v projekte Foundry.            |

| Hostovaný agent uviazol v stave `Provisioning` | Overte, či región projektu [podporuje hostovaných agentov](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) a či je dostupná kvóta. |
| Playground vrátil 401                         | Znovu sa autentifikujte pomocou rozšírenia Foundry z aktivity panela VS Code.                         |

Pre hlbšie usmernenie má každý lab svoj vlastný dokument `08-troubleshooting.md` - nasmerujte študentov tam:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Prispôsobenie tejto relácie

Workshop môžete prispôsobiť pre svoje publikum. Bežné varianty:

- **Pre backendové publikum:** venujte viac času `agent.yaml`, Dockeru a ACR; skráťte demo na playgrounde.
- **Pre občianskych vývojárov:** zostaňte v používateľskom rozhraní rozšírenia Foundry pri scaffoldingu; zredukujte kroky cez CLI.
- **Jednotlivý 60-minútový blok:** odprezentujte iba úvod, demo a Lab 01.
- **Formát iba workshop (bez slidov):** otvorte oba lab README a používajte ich ako hlavný scenár.

Ak rozšírite laby, prosím, prispejte spätnými zmenami cez PR, aby z nich mali úžitok aj ďalší školitelia.

---

## Dodatočné zdroje

- [Dokumentácia Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Prehľad hostovaných agentov](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Rýchly štart: nasadenie prvého hostovaného agenta (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Nasadenie hostovaného agenta (návod)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit pre VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakty

Ak máte otázky ohľadom vedenia tejto relácie, otvorte prosím issue v [workshop repozitári](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) a označte udržiavateľa.

| Rola                | Meno           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Udržiavateľ / kontakt| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->