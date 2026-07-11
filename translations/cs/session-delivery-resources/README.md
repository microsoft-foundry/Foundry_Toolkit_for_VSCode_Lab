# Jak prezentovat tuto sekci

Děkujeme, že prezentujete tuto sekci!

Před prezentací workshopu prosím:

1. Přečtěte si celý tento dokument a všechny přiložené zdroje.
2. Podívejte se na záznam prezentace a průchod workshopem od začátku do konce.
3. Projděte si oba hands-on laby od začátku do konce sami na svém počítači **alespoň jednou** před akcí.
4. Ověřte svůj Microsoft Foundry projekt, nasazení modelů a kvóty.
5. V případě nejasností kontaktujte správce.

---

## Shrnutí souborů

| Zdroj                          | Odkaz                                                                             | Popis                                                                                      |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Prezentace workshopu           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Prezentační snímky pro tento workshop s poznámkami prezentujícího a vloženými demo videi  |
| Záznam prezentace              | _Bude poskytnut správcem_                                                        | Záznam úvodu workshopu a průchodu snímky                                                   |
| End-to-end záznam workshopu   | _Bude poskytnut správcem_                                                        | Celý záznam obou labů z pohledu účastníka                                                 |
| Dokumentace workshopu          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Zdrojové úložiště, lab README, moduly krok za krokem                                       |
| Lab 01 - jeden agent           | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Hands-on lab: vytvoření, testování a nasazení *Explain Like I'm an Executive* hostovaného agenta |
| Lab 02 - workflow více agentů  | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Hands-on lab: vytvoření workflow *Resume to Job Fit Evaluator* se 4 agenty                 |
| Demo 1: Výkonný Agent          | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                              | Demo Lab 01: převod technického žargonu do výkonného souhrnu                               |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)     | Demo Lab 02: workflow se 4 agenty, který hodnotí shodu životopisu s pozicí a generuje doporučení |

> **Poznámka pro školitele:** Prezentace a video odkazy budou přidány jakmile budou záznamy zveřejněny. Do té doby kontaktujte správce (viz [Kontakty](#kontakty)) pro nejnovější materiály.

---

## Začínáme

Tento workshop učí vývojáře, jak vytvářet, testovat a nasazovat AI agenty do **Microsoft Foundry Agent Service** jako **hostované agenty** zcela z prostředí VS Code pomocí rozšíření **Microsoft Foundry Toolkit**.

Workshop je rozdělen na několik částí, včetně snímků, **2 živých dem** a **2 praktických labů**.

### Časový harmonogram

#### Kompletní prezentace (přibližně 2 hodiny)

| Čas            | Popis                                                               |
|-----------------|---------------------------------------------------------------------|
| 0:00 - 10:00    | Úvod: hostovaní agenti, Foundry Agent Service a toolkit             |
| 10:00 - 20:00   | Demo: Výkonný Agent od začátku do konce                            |
| 20:00 - 60:00   | Lab 01 - jeden agent (vytvoření, lokální test, nasazení, playground)|
| 60:00 - 110:00  | Lab 02 - workflow více agentů (Resume to Job Fit Evaluator)        |
| 110:00 - 120:00 | Shrnutí, otázky a odpovědi, zdroje pro pokračující učení           |

#### Zkrácená prezentace (přibližně 75 minut)

| Čas          | Popis                                                      |
|---------------|------------------------------------------------------------|
| 0:00 - 10:00  | Úvod a přehled                                            |
| 10:00 - 20:00 | Demo: Výkonný Agent                                       |
| 20:00 - 70:00 | Pouze Lab 01 (odkáže účastníky na Lab 02 jako samostudium)|
| 70:00 - 75:00 | Shrnutí a otázky a odpovědi                               |

### Příprava

| Zdroj                         | Odkaz                                                                                        | Popis                                       |
|-------------------------------|----------------------------------------------------------------------------------------------|----------------------------------------------|
| Dokumentace workshopu          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)           | Dokumentace workshopu a zdroje               |
| Instrukce pro Lab 01           | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                              | Hands-on lab: jeden hostovaný agent           |
| Instrukce pro Lab 02           | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                | Hands-on lab: workflow více agentů            |
| Kontrolní seznam předpokladů   | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)              | Nástroje, účty a přístup k Azure požadovány  |
| Rychlý start hostovaných agentů (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Oficiální rychlý start nasazení hostovaného agenta pomocí `azd` |
| Dostupnost hostovaných agentů podle regionu | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Podporované regiony pro hostované agenty (preview) |

### Požadavky na školitele

Před prezentací si ověřte, že máte:

- **Azure předplatné** s oprávněním vytvářet prostředky (vlastník nebo přispěvatel na skupinu prostředků).
- Přístup k **Microsoft Foundry projektu** v [regionu, který podporuje hostované agenty](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvótu pro **gpt-4.1** (nebo **gpt-4.1-mini**) ve vašem Foundry projektu.
- Následující nainstalované nástroje:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Rozšíření Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (volitelné)
  - Python 3.10 nebo novější

Proveďte [Rychlý start hostovaných agentů s `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) alespoň jednou před prezentací, abyste měli ověřený funkční Foundry projekt, nasazení modelu a Azure Container Registry jako referenci, pokud by se někdo zasekl.

---

## Průchod prezentací

Prezentace kopíruje tok labů. Doporučené body k projednání pro každou sekci:

| Sekce                       | Klíčové sdělení                                                                                              |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Titul a agenda              | Nastavte workshop jako *VS Code do Foundry* bez nutnosti přepínání portálu.                                 |
| Proč hostovaní agenti?      | Spravované běhové prostředí, nasazení přes ACR, rozhraní kompatibilní s OpenAI `/responses` API, omezeno na Foundry projekty. |
| Architektonický diagram    | Projděte [architekturu v README](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.          |
| Anatomie hostovaného agenta | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - co dělá každý soubor.                               |
| Živé demo: Výkonný Agent    | Přepněte do VS Code a spusťte demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) od začátku do konce (viz [Demo 1](#demo-1-výkonný-agent)). |
| Živé demo: Resume to Job Fit Evaluator | Přepněte do VS Code a spusťte 4-agent demo [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (viz [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Shrnutí Lab 01             | Předejte účastníkům. Odkaz na [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Vzory více agentů          | Sekvenční vs paralelní vs předání - náhled před začátkem Lab 02.                                            |
| Shrnutí Lab 02             | Předejte účastníkům. Odkaz na [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Shrnutí a zdroje           | Odkazy pro pokračující učení z sekce [Další zdroje](#další-zdroje).                                 |

---

## Dema

V rámci prezentace jsou zahrnuta dvě živá dema. Vyhraďte si na každé 10 minut.

| Demo | Lab | Soubory | Co ukázat |
|------|-----|--------|------------|
| Výkonný Agent | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Jeden hostovaný agent; převod technického žargonu do výkonného souhrnu |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orchestrace se 4 agenty; hodnocení shody životopisu s pozicí a generování doporučení |

### Demo 1: Výkonný Agent

Samostatný agent v [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Použijte toto demo na 10 minut před Lab 01.

1. Otevřete [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) a projděte definici agenta (systémový prompt, model, framework).
2. Stiskněte `F5` pro spuštění **Agent Inspector** lokálně.
3. Vložte ukázkový prompt z [README](../README.md#see-it-in-action) a ukažte odpověď s výkonným shrnutím.
4. Ukažte [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) a [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) k vysvětlení artefaktů nasazení.
5. Demonstrujte průběh nasazení (Docker build, ACR push, vytvoření hostovaného agenta) bez čekání na dokončení.

### Demo 2: Resume to Job Fit Evaluator

Workflow se 4 agenty v [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Použijte toto demo na 10 minut před Lab 02.

1. Otevřete [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) a ukažte, jak jsou čtyři agenti propojeni v sekvenční orchestraci.
2. Stiskněte `F5` pro spuštění **Agent Inspector** pro workflow více agentů.
3. Vložte krátký popis práce a ukázkový životopis do chatu Inspectoru.
4. Projděte výstupní pipeline čtyř agentů: parser životopisu, extraktor požadavků na pozici, skórovač shody a autor doporučení.
5. Poukažte, jak výstup každého sub-agenta slouží jako kontext pro následující agenta, zvýrazněte vzor předání.
6. Ukažte [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) pro srovnání s ekvivalentem jednoho agenta z Demo 1.

---

## Tipy pro prezentaci

- **Nastavte očekávání hned na začátku.** Hostovaní agenti jsou v preview - upozorněte na regionální omezení a kvóty ihned, aby účastníci nebyli překvapeni uprostřed labu.
- **Nejdříve spusťte úlohu ověření předpokladů.** Oba laby obsahují VS Code úlohu `Validate prerequisites` - nechte účastníky spustit ji dříve, než začnou psát kód.
- **Mějte Agent Inspector viditelný.** Nejvíce „aha“ okamžiků nastává, když účastníci vidí lokální `/responses` obousměrnou komunikaci.
- **Mějte záložní projekt.** Pokud se účastníkův Foundry projekt dostane do kvóty, sdílejte předem připravený projekt pro krok nasazení, aby nedošlo k zablokování místnosti.
- **Párujte účastníky.** Lab 02 (více agentů) je výrazně snazší, pokud si účastníci mohou orchestraci probrat s partnerem.
- **Používejte moduly dokumentace jako kontrolní body.** Každý lab obsahuje složku `docs/` rozdělenou do 8 očíslovaných modulů - použijte je jako přirozené body pro zastavení.
- **Předem stáhněte základní Docker obraz** na sdílených lab strojích, aby nedocházelo k omezením kvóty registry.

---

## Řešení problémů během prezentace

| Symptomy                                    | První krok, co vyzkoušet                                                                           |
|---------------------------------------------|----------------------------------------------------------------------------------------------------|
| Agent Inspector se nemůže připojit          | Ověřte, že port `8088` je volný a že je spuštěna úloha `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server`. |
| Ladící nástroj se nepřipojí                   | Zkontrolujte, že port `5679` je volný; restartujte VS Code, pokud je `debugpy` již zabraný.           |
| `azd up` selže s chybou ověření              | Proveďte `az login` a `azd auth login`, ujistěte se, že je vybrán správný tenant.                   |
| Nasazení visí při push na ACR                 | Ověřte, že Docker Desktop běží a uživatel má práva `AcrPush` na registry.                           |
| Model vrací 404 / nasazení nenalezeno        | Název nasazení modelu v `agent.yaml` musí odpovídat nasazení ve Foundry projektu.                   |

| Hostovaný agent uvízl v `Provisioning`       | Ověřte, že region projektu [podporuje hostované agenty](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) a že je k dispozici kvóta. |
| Playground vrací 401                       | Znovu se autentizujte ve Foundry rozšíření z aktivity VS Code.                                     |

Pro hlubší návod má každý lab svůj vlastní dokument `08-troubleshooting.md` - odkážte studenty tam:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Přizpůsobení této lekce

Máte možnost workshop přizpůsobit svému publiku. Běžné varianty:

- **Publikum zaměřené na backend:** věnujte více času `agent.yaml`, Dockeru a ACR; zkraťte demo playgroundu.
- **Občanský vývojářské publikum:** zůstaňte v UI Foundry rozšíření pro scaffolding; omezte kroky v CLI.
- **Jednotná 60minutová relace:** předveďte úvod, demo a pouze Lab 01.
- **Formát pouze workshop (bez slidů):** otevřete oba lab README a použijte je jako hlavní scénář.

Pokud rozšíříte laby, prosím přispějte změny zpět přes PR, aby měli prospěch i další lektoři.

---

## Další zdroje

- [Dokumentace Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Přehled hostovaných agentů](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Rychlý start: nasazení prvního hostovaného agenta (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Nasazení hostovaného agenta (návod)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit pro VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakty

Máte-li otázky ohledně vedení této lekce, otevřete issue v [repozitáři workshopu](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) a označte správce.

| Role                | Jméno           | GitHub                                                  |
|---------------------|-----------------|---------------------------------------------------------|
| Správce / kontakt   | Shivam Goyal    | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->