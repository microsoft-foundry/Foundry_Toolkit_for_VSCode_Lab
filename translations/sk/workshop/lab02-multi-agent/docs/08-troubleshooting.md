# Modul 8 - Riešenie problémov

Tento modul pokrýva bežné chyby, opravy a stratégie ladenia špecifické pre workflow s viacerými agentmi.

## Problémy s výstupom agenta

### GapAnalyzer hovorí „Stále nemám zodpovedajúcu správu“

**Príznak:** Odozva GapAnalyzer vás žiada, aby ste vložili zodpovedajúcu správu so „Chýbajúcimi zručnosťami“ a „Certifikačnými medzerami“. Toto sa deje aj keď ste poslali životopis aj popis pracovnej pozície.

**Príčina:** Text popisu pracovnej pozície (JD) nebol odovzdaný ďalej agentovi JD. Pri `context_mode="last_agent"` je `resume_executor` jediný vykonávateľ, ktorý niekedy vidí pôvodnú správu používateľa. Ak `RESUME_PARSER_INSTRUCTIONS` nezahrňujú text JD vo svojom výstupe, agent JD nemá žiadny JD na analyzovanie, MatchingAgent nevie vypočítať skóre zhody a GapAnalyzer dostáva nezmyselný vstup.

**Diagnóza:**

V logoch servera hľadajte rozsah MatchingAgent. Ak obsahuje:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
je priepustnosť chýbajúca alebo poškodená.

**Oprava:** Overte, že `RESUME_PARSER_INSTRUCTIONS` v `main.py` obsahuje sekciu `[JOB DESCRIPTION PASS-THROUGH]` a pravidlo:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Tiež skontrolujte, že `JOB_DESCRIPTION_INSTRUCTIONS` obsahujú pravidlo preposielania `[PARSED RESUME PASS-THROUGH]:`
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Ak je niektorý blok inštrukcií náhradný zo sprievodcu scaffoldu, nahraďte ho kompletnou verziou z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent vracia „Nie je možné vypočítať skóre zhody - nebol poskytnutý JD“

To je rovnaká základná príčina ako vyššie. MatchingAgent dostal výstup od agenta JD, ale sekcia `[PARSED RESUME PASS-THROUGH]` chýbala alebo bola prázdna, takže nemohol porovnať oba profily. Overte:
1. `JOB_DESCRIPTION_INSTRUCTIONS` obsahuje pravidlo preposielania: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` hovorí agentovi, aby hľadal sekcie `[JD REQUIREMENTS]` a `[PARSED RESUME PASS-THROUGH]`.

Nahraďte oba bloky inštrukcií kompletnými verziami z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odozva sa zobrazuje dvakrát

**Príznak:** Výstup GapAnalyzer (alebo celý výstup pipeline) sa objavuje dvakrát v odpovedi v Agent Inspector.

**Príčina:** `WorkflowBuilder` používa OR sémantiku pre vstupné hrany - downstream vykonávateľ sa spustí, keď ktorýkoľvek predchodca skončí. Ak má `matching_executor` dve vstupné hrany (jednu zo `resume_executor` a jednu z `jd_executor`), spustí sa dvakrát: raz keď skončí ResumeParser a znova keď skončí JD Agent. GapAnalyzer sa potom tiež spustí dvakrát.

**Oprava:** Zaistite, aby graf `WorkflowBuilder` bol prísne sekvenčný pipeline bez fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NIE z resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Ak máte zbytočný riadok `.add_edge(resume_executor, matching_executor)`, odstráňte ho. Relay `[PARSED RESUME PASS-THROUGH]` vo výstupe agenta JD už dáva MatchingAgentovi prístup k životopisu.

---

## Problémy s prostredím a konfiguráciou

### Chýbajúce alebo nesprávne hodnoty `.env`

Súbor `.env` musí byť v adresári `PersonalCareerCopilot/` (rovnaká úroveň ako `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Očakávaný obsah `.env`:

**Cesta A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Cesta B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Obe cesty používajú `FOUNDRY_PROJECT_ENDPOINT`. Hodnota sa líši: cloud používa `https://` endpoint Foundry; lokálne je to `http://localhost:5273/v1`. Spustite `foundry model list` pre potvrdenie presného aliasu modelu pre cestu B.

> **Ako nájsť váš `FOUNDRY_PROJECT_ENDPOINT`:** 
- Otvorte postranný panel **Foundry Toolkit** vo VS Code → kliknite pravým tlačidlom na projekt → **Copy Project Endpoint**. 
- Alebo choďte na [Azure Portal](https://portal.azure.com) → váš Foundry projekt → **Prehľad** → **Project endpoint**.

> **Ako nájsť vaše `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** V postrannom paneli Foundry Toolkit rozbaľte projekt → **Models** → nájdite nasadený názov modelu (napr. `gpt-4.1-mini`).

### Priorita premenných prostredia

`main.py` používa `load_dotenv(override=True)`, čo znamená:

| Priorita | Zdroj | Vyhrá ak sú nastavené obe? |
|----------|--------|---------------------------|
| 1 (najvyššia) | `.env` súbor | Áno |
| 2 | Premenná shellu / kontajnera | Používa sa, keď rovnaký kľúč nie je v `.env` |

Pri lokálnom vývoji je `.env` zdrojom pravdy (úprava `.env` okamžite ovplyvňuje behy). Pri hostovanej nasadení Foundry injektuje premenné prostredia na úrovni kontajnera; keďže `.env` nie je súčasťou nasadenej image pre túto lab konfiguráciu, používajú sa injektované hodnoty kontajnera.

---

## Kompatibilita verzií

### Matica verzií balíkov

Workflow s viacerými agentmi vyžaduje špecifické verzie balíkov. Nesprávne verzie spôsobujú runtime chyby.

| Balík | Požadovaná verzia | Príkaz na kontrolu |
|---------|-----------------|-------------------|
| `agent-framework-foundry` | najnovšia | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | najnovšia | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | najnovšia | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Bežné chyby verzií

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Opraviť: preinštalovať agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Oprava: aktualizácia balíka mcp
pip install mcp --upgrade
```

### Overiť všetky verzie naraz

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Očakávaný výstup:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problémy s nasadením

### Kontajner po nasadení nespustí sa

1. **Skontrolujte logy kontajnera:**
   - Otvorte postranný panel **Foundry Toolkit** → rozbaľte **Hosted Agents (Preview)** → kliknite na svojho agenta → rozbaľte verziu → **Detaily kontajnera** → **Logy**.
   - Hľadajte Python stack trace alebo chyby chýbajúcich modulov.

2. **Bežné chyby pri spúšťaní kontajnera:**

   | Chyba v logoch | Príčina | Oprava |
   |---------------|---------|-------|
   | `ModuleNotFoundError` | `requirements.txt` chýba balík | Pridajte balík, znovu nasadte |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` alebo `.env` nemajú nastavené premenné | Aktualizujte sekciu `environment_variables` v `agent.yaml` (hostované) alebo `.env` (lokálne) |
   | `azure.identity.CredentialUnavailableError` | Nie je nastavená Managed Identity | Foundry to nastavuje automaticky - zabezpečte nasadenie cez rozšírenie |
   | `OSError: port 8088 already in use` | Dockerfile vystavuje nesprávny port alebo konflikt portov | Overte `EXPOSE 8088` v Dockerfile a `CMD ["python", "main.py"]` |
   | Kontajner končí kódom 1 | Nezachytená výnimka v `main()` | Najskôr testujte lokálne ([Modul 5](05-test-locally.md)) pre zachytenie chýb pred nasadením |

3. **Znovu nasadiť po oprave:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → vyberte rovnakého agenta → nasadiť novú verziu.

### Nasadenie trvá príliš dlho

Kontajnery pre workflow s viacerými agentmi sa spúšťajú dlhšie, pretože na štarte vytvárajú 4 inštancie agenta. Bežné doby spustenia:

| Fáza | Očakávaná doba trvania |
|-------|-----------------------|
| Vytvorenie image kontajnera | 1-3 minúty |
| Push image do ACR | 30-60 sekúnd |
| Štart kontajnera (jeden agent) | 15-30 sekúnd |
| Štart kontajnera (viac agentov) | 30-120 sekúnd |
| Agent dostupný v Playground | 1-2 minúty po „Started“ |

> Ak stav „Pending“ pretrváva dlhšie ako 5 minút, skontrolujte logy kontajnera pre chyby.

---

## Problémy s RBAC a povoleniami

### `403 Forbidden` alebo `AuthorizationFailed`

Potrebujete rolu **[Foundry User](https://aka.ms/foundry-ext-project-role)** vo vašom Foundry projekte (predtým pomenovaná **Azure AI User** - ID roly sa nezmenilo):

1. Choďte na [Azure Portal](https://portal.azure.com) → váš Foundry **projekt**.
2. Kliknite na **Prístupové ovládanie (IAM)** → **Priradenia rolí**.
3. Vyhľadajte svoje meno → potvrďte, že je uvedený **Foundry User** (alebo starší názov **Azure AI User**).
4. Ak chýba: **Pridať** → **Pridať priradenie roly** → vyhľadajte **Foundry User** → priraďte svojmu účtu.

Podrobnosti nájdete v dokumentácii [RBAC pre Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Nasadenie modelu nie je dostupné

Ak agent vracia chyby týkajúce sa modelu:

1. Overte, či je model nasadený: postranný panel Foundry → rozbaľte projekt → **Models** → skontrolujte, či `gpt-4.1-mini` (alebo váš model) má stav **Succeeded**.
2. Overte zhodu názvu nasadenia: porovnajte `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` (alebo `agent.yaml`) s reálnym názvom nasadenia v postrannom paneli.
3. Ak expirovalo (bezplatný tier): znovu nasadte cez [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problémy Foundry Local (Cesta B)

### Služba Foundry Local neběží

```powershell
# Skontrolovať stav
foundry local status

# Spustiť službu, ak je zastavená
foundry local start
```

| Príznak | Príčina | Oprava |
|---------|---------|-------|
| Health check vracia `503` | Služba nebola spustená | `foundry local start` alebo kliknite na **Start** v postrannom paneli Foundry Toolkit |
| Health check vypršal | Model sa stále načítava | Počkajte 30–60 s po štarte; väčšie modely načítavajú dlhšie |
| `StatusCode: 404` na `/v1/health` | Nesprávny port | Predvolený je `5273`. Skontrolujte `foundry local status` pre aktuálny port |
| Nedostatok zdrojov | Foundry Local potrebuje ~4 GB RAM voľného | Zavrite ostatné aplikácie |
| Sťahovanie modelu zlyháva | Nedostatok miesta na disku | Modely majú 2–8 GB. Uvoľnite miesto a potom spustite `foundry model pull <name>` |

### Nesúlad názvu modelu

```powershell
# Zoznam stiahnutých modelov a ich presných aliasov
foundry model list
```

Nastavte `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` presne podľa zobrazeného aliasu (napr. `phi-4-mini`, nie `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` pri lokálnom behu (Cesta B)

`main.py` v labe používa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local vyžaduje, aby táto premenná smerovala na lokálnu službu — **nie** `AZURE_AI_PROJECT_ENDPOINT`. Uistite sa, že `.env` obsahuje:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP nástroj stále vykonáva odchozí dopyt (Cesta B)

Toto je očakávané. Nástroj `search_microsoft_learn_for_plan` získava vzdelávacie zdroje z `https://learn.microsoft.com/api/mcp`. **Iba dotaz na meno zručnosti** prechádza sieťou - životopis a text JD spracúvajú sa kompletne na vašom zariadení a nikdy nie sú prenesené. Ak je potrebná plná offline prevádzka, pridajte do nástroja `try/except` záložný mechanizmus, ktorý vráti statickú URL `learn.microsoft.com`, keď nie je možné dosiahnuť endpoint.

---

## Ako získať pomoc

Ak ste zaseknutí po vyskúšaní vyššie uvedených opráv:

1. **Skontrolujte logy servera** – Väčšina chýb produkuje Python stack trace v termináli. Prečítajte si celý traceback.
2. **Vyhľadajte text chyby** – Skopírujte text chyby a vyhľadajte ho v [Microsoft Q&A pre Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Otvorte issue** – Vytvorte issue v [repozitári workshopu](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) s:
   - Textom chyby alebo screenshotom
   - Verziami balíkov (`pip list | Select-String "agent-framework"`)
   - Verziou Pythonu (`python --version`)
   - Informáciou, či je problém lokálny alebo po nasadení

---

### Kontrolný zoznam

- [ ] Viete skontrolovať a opraviť problémy konfigurácie `.env`
- [ ] Viete overiť, že verzie balíkov zodpovedajú požadovanej matici
- [ ] Viete skontrolovať logy kontajnera pre neúspechy nasadenia
- [ ] Viete overiť RBAC role v Azure Porte

---

**Predchádzajúci:** [07 - Overovanie v Playground](07-verify-in-playground.md) · **Ďalší:** [09 - Zhrnutie →](09-summary.md) · **Domov:** [Lab 02 README](../README.md) · [Domov workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->