# Modul 8 - Řešení problémů

Tento modul pokrývá běžné chyby, opravy a strategie ladění specifické pro multi-agentní pracovní postup.

## Problémy se vstupy agentů

### GapAnalyzer říká „Stále nemám odpovídající zprávu“

**Příznak:** Odezva GapAnalyzer vás vyzývá ke vložení odpovídající zprávy s „Chybějícími dovednostmi“ a „Certifikačními mezerami“. To se stane i když jste poslali životopis i popis práce.

**Příčina:** Text JD nebyl předán dále agentovi JD. S `context_mode="last_agent"` je `resume_executor` jediný vykonavatel, který kdy vidí původní uživatelskou zprávu. Pokud `RESUME_PARSER_INSTRUCTIONS` nezahrnuje text JD ve svém výstupu, agent JD nemá žádný JD k rozparsování, MatchingAgent nemůže vypočítat skóre shody a GapAnalyzer dostává nesmyslný vstup.

**Diagnóza:**

V serverových logách vyhledejte rozsah MatchingAgent. Pokud obsahuje:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pass-through chybí nebo je poškozený.

**Oprava:** Ověřte, že `RESUME_PARSER_INSTRUCTIONS` v `main.py` obsahuje sekci `[JOB DESCRIPTION PASS-THROUGH]` a pravidlo:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Také potvrďte, že `JOB_DESCRIPTION_INSTRUCTIONS` obsahuje přeposílací pravidlo `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Pokud je kterýkoli blok instrukcí výchozí (stub) ze scaffold wizardu, nahraďte jej kompletní verzí z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent vypisuje „Nelze spočítat skóre shody - nebyl poskytnut JD“

To je stejná kořenová příčina jako výše. MatchingAgent obdržel výstup agenta JD, ale sekce `[PARSED RESUME PASS-THROUGH]` chyběla nebo byla prázdná, takže nemohl porovnat oba profily. Ověřte:
1. `JOB_DESCRIPTION_INSTRUCTIONS` obsahuje přeposílací pravidlo: `Kopírovat [PARSED RESUME] doslovně - Matching Agent na tom závisí dále.`
2. `MATCHING_AGENT_INSTRUCTIONS` říkají agentovi, aby hledal sekce `[JD REQUIREMENTS]` a `[PARSED RESUME PASS-THROUGH]`.

Nahraďte oba bloky instrukcí kompletními verzemi z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odezva se objeví dvakrát

**Příznak:** Výstup GapAnalyzer (nebo celý výstup pipeline) se objeví dvakrát v odpovědi Agent Inspector.

**Příčina:** `WorkflowBuilder` používá OR-sémantiku pro příchozí hrany - downstream vykonavatel spustí se, jakmile **jakýkoli** předchůdce dokončí. Pokud má `matching_executor` dvě příchozí hrany (jednu od `resume_executor` a jednu od `jd_executor`), spustí se dvakrát: jednou po dokončení ResumeParser a podruhé po dokončení JD Agenta. GapAnalyzer pak také běží dvakrát.

**Oprava:** Ujistěte se, že graf `WorkflowBuilder` je přísně sekvenční pipeline bez vícenásobného vstupu (fan-in):

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NE z resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Pokud máte někde volání `.add_edge(resume_executor, matching_executor)`, odstraňte jej. Přeposílání `[PARSED RESUME PASS-THROUGH]` ve výstupu JD Agenta již dává MatchingAgentovi přístup k životopisu.

---

## Problémy s prostředím a konfigurací

### Chybějící nebo nesprávné hodnoty v `.env`

Soubor `.env` musí být v adresáři `PersonalCareerCopilot/` (na stejné úrovni jako `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Očekávaný obsah `.env`:

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

> Obě cesty používají `FOUNDRY_PROJECT_ENDPOINT`. Hodnota se liší: cloud používá `https://` endpoint Foundry; local používá `http://localhost:5273/v1`. Spusťte `foundry model list` pro přesné ověření aliasu modelu pro Cestu B.

> **Jak najít svůj `FOUNDRY_PROJECT_ENDPOINT`:**
- Otevřete postranní panel **Foundry Toolkit** ve VS Code → pravým tlačítkem klikněte na svůj projekt → **Copy Project Endpoint**.
- Nebo jděte na [Azure Portal](https://portal.azure.com) → svůj Foundry projekt → **Overview** → **Project endpoint**.

> **Jak najít svůj `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** V postranním panelu Foundry Toolkit rozbalte projekt → **Models** → najděte jméno nasazeného modelu (např. `gpt-4.1-mini`).

### Priorita proměnných prostředí

`main.py` používá `load_dotenv(override=True)`, což znamená:

| Priorita | Zdroj | Výhra při nastavení obou? |
|----------|--------|-------------------------|
| 1 (nejvyšší) | Soubor `.env` | Ano |
| 2 | Shell / kontejnerová proměnná prostředí | Použito pokud stejný klíč není v `.env` |

V lokálním vývoji je `.env` zdroj pravdy (úprava `.env` okamžitě ovlivní spuštění). V hosted nasazení Foundry injektuje proměnné prostředí na úrovni kontejneru; protože `.env` není součástí nasazeného image v tomto labovém setupu, používají se injektované hodnoty kontejneru.

---

## Kompatibilita verzí

### Matice verzí balíčků

Multi-agentní pracovní postup vyžaduje specifické verze balíčků. Nesoulad verzí způsobuje chyby za běhu.

| Balíček | Požadovaná verze | Příkaz pro kontrolu |
|---------|-----------------|---------------------|
| `agent-framework-foundry` | nejnovější | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | nejnovější | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | nejnovější | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Běžné chyby verzí

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Oprava: přeinstalovat agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Oprava: aktualizace balíčku mcp
pip install mcp --upgrade
```

### Ověřte všechny verze najednou

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Očekávaný výstup:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problémy při nasazení

### Kontejner nenastartuje po nasazení

1. **Zkontrolujte logy kontejneru:**
   - Otevřete postranní panel **Foundry Toolkit** → rozbalte **Hosted Agents (Preview)** → klikněte na svého agenta → rozbalte verzi → **Container Details** → **Logs**.
   - Hledejte Python tracebacky nebo chyby chybějících modulů.

2. **Běžné příčiny selhání spuštění kontejneru:**

   | Chyba v logu | Příčina | Oprava |
   |--------------|---------|--------|
   | `ModuleNotFoundError` | `requirements.txt` chybí balíček | Přidejte balíček, znovu nasaďte |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Env proměnné v `agent.yaml` nebo `.env` nejsou nastaveny | Aktualizujte sekci `environment_variables` v `agent.yaml` (hosted) nebo `.env` (lokálně) |
   | `azure.identity.CredentialUnavailableError` | Není nastaven Managed Identity | Foundry to automaticky nastavuje - ujistěte se, že nasazujete přes rozšíření |
   | `OSError: port 8088 already in use` | Dockerfile vystavuje špatný port nebo port je obsazený | Ověřte `EXPOSE 8088` v Dockerfile a `CMD ["python", "main.py"]` |
   | Kontejner končí s kódem 1 | Nezachycená výjimka v `main()` | Testujte nejdříve lokálně ([Modul 5](05-test-locally.md)), abyste odhalili chyby před nasazením |

3. **Znovu nasaďte po opravě:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → vyberte stejného agenta → nasaďte novou verzi.

### Nasazení trvá příliš dlouho

Multi-agentní kontejnery trvají déle na start, protože při spuštění vytvoří 4 instance agenta. Normální doby spuštění:

| Fáze | Očekávaná doba |
|-------|-----------------|
| Sestavení image kontejneru | 1-3 minuty |
| Push image do ACR | 30-60 sekund |
| Start kontejneru (jediný agent) | 15-30 sekund |
| Start kontejneru (multi-agent) | 30-120 sekund |
| Agent dostupný ve hřišti (Playground) | 1-2 minuty po „Started“ |

> Pokud stav „Pending“ přetrvává déle než 5 minut, zkontrolujte logy kontejneru na chyby.

---

## Problémy s RBAC a oprávněními

### `403 Forbidden` nebo `AuthorizationFailed`

Potřebujete roli **[Foundry User](https://aka.ms/foundry-ext-project-role)** ve vašem Foundry projektu (dříve nazývána **Azure AI User** - ID role zůstává stejné):

1. Jděte na [Azure Portal](https://portal.azure.com) → váš Foundry **projekt**.
2. Klikněte na **Access control (IAM)** → **Role assignments**.
3. Vyhledejte své jméno → ověřte, že je uveden **Foundry User** (nebo stará značka **Azure AI User**).
4. Pokud chybí: **Přidat** → **Add role assignment** → vyhledejte **Foundry User** → přiřaďte ke svému účtu.

Podrobnosti najdete v dokumentaci [RBAC pro Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Nasazení modelu není přístupné

Pokud agent vrací chyby související s modelem:

1. Ověřte, že model je nasazený: Foundry sidebar → rozbalte projekt → **Models** → zkontrolujte, zda `gpt-4.1-mini` (nebo váš model) je ve stavu **Succeeded**.
2. Ověřte, zda se jméno nasazení shoduje: porovnejte `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` (nebo `agent.yaml`) s aktuálním jménem nasazení v sidebaru.
3. Pokud nasazení vypršelo (free tier): nasaďte znovu z [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problémy Foundry Local (Cesta B)

### Služba Foundry Local neběží

```powershell
# Zkontrolovat stav
foundry local status

# Spusťte službu, pokud je zastavena
foundry local start
```

| Příznak | Příčina | Oprava |
|---------|---------|--------|
| Kontrola zdraví vrací `503` | Služba není spuštěna | `foundry local start` nebo klikněte na **Start** v Foundry Toolkit sidebaru |
| Kontrola zdraví vyprší | Model se stále načítá | Počkejte 30–60 s po spuštění; větší modely trvají déle |
| `StatusCode: 404` na `/v1/health` | Špatný port | Výchozí je `5273`. Zkontrolujte `foundry local status` pro aktuální port |
| Nedostatek zdrojů | Foundry Local potřebuje ~4 GB volné RAM | Zavřete jiné aplikace |
| Stažení modelu selže | Nedostatek místa na disku | Modely jsou 2–8 GB. Uvolněte místo, pak `foundry model pull <name>` |

### Neshoda jména modelu

```powershell
# Vypište stažené modely a jejich přesné aliasy
foundry model list
```

Nastavte `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` přesně podle zobrazeného aliasu (např. `phi-4-mini`, ne `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` při lokálním spuštění (Cesta B)

Lab `main.py` používá `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local vyžaduje, aby tato proměnná směřovala na lokální službu - **ne** na `AZURE_AI_PROJECT_ENDPOINT`. Ujistěte se, že váš `.env` obsahuje:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Nástroj MCP stále dělá odchozí volání (Cesta B)

To je očekávané. Nástroj `search_microsoft_learn_for_plan` načítá učební zdroje z `https://learn.microsoft.com/api/mcp`. **Pouze dotaz na název dovednosti** putuje po síti - životopisy a text JD jsou zpracovávány zcela na vašem zařízení a nikdy nejsou přenášeny. Pokud je vyžadován plně offline režim, přidejte `try/except` záložní mechanismus v nástroji, který vrátí statickou URL z `learn.microsoft.com`, když je endpoint nedostupný.

---

## Jak získat pomoc

Pokud jste zaseklí po vyzkoušení výše uvedených oprav:

1. **Zkontrolujte serverové logy** - Většina chyb produkuje Python traceback v terminálu. Přečtěte si celý traceback.
2. **Vyhledejte chybovou zprávu** - Zkopírujte text chyby a hledejte na [Microsoft Q&A pro Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Otevřete issue** - Nahlaste problém v [repozitáři workshopu](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) s:
   - Chybovou zprávou nebo screenshotem
   - Verzemi balíčků (`pip list | Select-String "agent-framework"`)
   - Verzí Pythonu (`python --version`)
   - Informací, zda je problém lokální nebo po nasazení

---

### Kontrolní seznam

- [ ] Umíte zkontrolovat a opravit problémy s konfigurací `.env`
- [ ] Dokážete ověřit, že verze balíčků odpovídají požadované matici
- [ ] Umíte zkontrolovat logy kontejneru kvůli selhání při nasazení
- [ ] Dokážete ověřit role RBAC v Azure Portalu

---

**Předchozí:** [07 - Verify in Playground](07-verify-in-playground.md) · **Další:** [09 - Shrnutí →](09-summary.md) · **Domů:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->