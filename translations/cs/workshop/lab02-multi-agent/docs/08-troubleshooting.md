# Modul 8 - Řešení problémů (Multi-Agent)

Tento modul pokrývá běžné chyby, opravy a strategie ladění specifické pro multi-agentní pracovní postup. Pro obecné problémy s nasazením Foundry se také podívejte na [průvodce řešením problémů Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Rychlá reference: Chyba → Oprava

| Chyba / Příznak | Pravděpodobná příčina | Oprava |
|----------------|-----------------------|--------|
| `RuntimeError: Missing required environment variable(s)` | Soubor `.env` chybí nebo hodnoty nejsou nastaveny | Vytvořte `.env` se `PROJECT_ENDPOINT=<váš-endpoint>` a `MODEL_DEPLOYMENT_NAME=<váš-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuální prostředí není aktivováno nebo chybí závislosti | Spusťte `.\.venv\Scripts\Activate.ps1` a poté `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Balíček MCP není nainstalován (chybí v requirements) | Spusťte `pip install mcp` nebo zkontrolujte, že `requirements.txt` ho zahrnuje jako tranzitivní závislost |
| Agent se spustí, ale vrací prázdnou odpověď | Nesoulad `output_executors` nebo chybějící hranice | Ověřte `output_executors=[gap_analyzer]` a že všechny hrany existují ve `create_workflow()` |
| Je pouze 1 gap karta (ostatní chybí) | Instrukce GapAnalyzer jsou neúplné | Přidejte odstavec `CRITICAL:` do `GAP_ANALYZER_INSTRUCTIONS` - viz [Modul 3](03-configure-agents.md) |
| Skóre shody je 0 nebo chybí | MatchingAgent neobdržel data z upstream | Ověřte existenci obou `add_edge(resume_parser, matching_agent)` a `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server odmítl volání nástroje | Zkontrolujte připojení k internetu. Zkuste otevřít `https://learn.microsoft.com/api/mcp` v prohlížeči. Opakujte pokus |
| V výstupu nejsou žádné Microsoft Learn URL | MCP nástroj není registrován nebo endpoint je špatný | Ověřte `tools=[search_microsoft_learn_for_plan]` na GapAnalyzer a správnost `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | Jiný proces používá port 8088 | Spusťte `netstat -ano \| findstr :8088` (Windows) nebo `lsof -i :8088` (macOS/Linux) a zastavte konflikt |
| `Address already in use: port 5679` | Konflikt portu Debugpy | Zastavte ostatní debugovací sessiony. Spusťte `netstat -ano \| findstr :5679` a ukončete proces |
| Agent Inspector se neotevře | Server není plně spuštěn nebo konflikt portu | Počkejte na log "Server running". Zkontrolujte, že port 5679 je volný |
| `azure.identity.CredentialUnavailableError` | Nejste přihlášeni do Azure CLI | Spusťte `az login` a restartujte server |
| `azure.core.exceptions.ResourceNotFoundError` | Nasazení modelu neexistuje | Ověřte, že `MODEL_DEPLOYMENT_NAME` odpovídá nasazenému modelu ve vašem Foundry projektu |
| Stav kontejneru "Failed" po nasazení | Kontejner spadl při spuštění | Zkontrolujte logy kontejneru v postranním panelu Foundry. Časté příčiny: chybějící env var nebo chyba importu |
| Nasazení zobrazuje "Pending" déle než 5 minut | Kontejner se spouští příliš dlouho nebo omezení zdrojů | Počkejte až 5 minut u multi-agent (vytváří 4 instance agenta). Pokud je stále čekající, zkontrolujte logy |
| `ValueError` z `WorkflowBuilder` | Neplatná konfigurace grafu | Ujistěte se, že `start_executor` je nastaven, `output_executors` je seznam a nejsou tam kruhové hrany |

---

## Problémy s prostředím a konfigurací

### Chybějící nebo nesprávné hodnoty `.env`

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

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Jak najít svůj PROJECT_ENDPOINT:**  
- Otevřete postranní panel **Microsoft Foundry** ve VS Code → pravým klikem na váš projekt → **Copy Project Endpoint**.  
- Nebo přejděte do [Azure Portal](https://portal.azure.com) → váš Foundry projekt → **Overview** → **Project endpoint**.

> **Jak najít MODEL_DEPLOYMENT_NAME:** V postranním panelu Foundry rozbalte projekt → **Models** → najděte název nasazeného modelu (např. `gpt-4.1-mini`).

### Priorita env proměnných

`main.py` používá `load_dotenv(override=False)`, což znamená:

| Priorita | Zdroj | Vyhraje pokud jsou oba nastavené? |
|----------|--------|----------------------------------|
| 1 (nejvyšší) | Shell environment variable | Ano |
| 2 | `.env` soubor | Pouze pokud shell var není nastaven |

To znamená, že runtime env proměnné Foundry (nastavené v `agent.yaml`) mají přednost před hodnotami `.env` při hostovaném nasazení.

---

## Kompatibilita verzí

### Matice verzí balíčků

Multi-agentní pracovní postup vyžaduje specifické verze balíčků. Nesoulad verzí způsobuje chyby za běhu.

| Balíček | Vyžadovaná verze | Příkaz pro kontrolu |
|---------|------------------|--------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | nejnovější pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Běžné chyby verzí

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Oprava: aktualizace na rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nenalezen nebo Inspector nekompatibilní:**

```powershell
# Oprava: instalace s příznakem --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Oprava: aktualizace balíčku mcp
pip install mcp --upgrade
```

### Ověření všech verzí najednou

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Očekávaný výstup:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Problémy s MCP nástrojem

### MCP nástroj nevrací výsledky

**Příznak:** Gap karty zobrazují „No results returned from Microsoft Learn MCP“ nebo „No direct Microsoft Learn results found“.

**Možné příčiny:**

1. **Síťový problém** – MCP endpoint (`https://learn.microsoft.com/api/mcp`) není dosažitelný.  
   ```powershell
   # Otestovat připojení
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
 Pokud to vrátí `200`, je endpoint dostupný.

2. **Dotaz příliš specifický** – Název dovednosti je příliš specializovaný pro vyhledávání Microsoft Learn.  
   - Je to očekávané u velmi specifických dovedností. Nástroj vrací alternativní URL v odpovědi.

3. **Timeout MCP sezení** – Streamable HTTP připojení vypršelo.  
   - Opakujte požadavek. MCP sezení jsou efemerní a je třeba je znovu navázat.

### Vysvětlení MCP logů

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Význam | Akce |
|-----|--------|-------|
| `GET → 405` | MCP klient testuje při inicializaci | Normální - ignorujte |
| `POST → 200` | Volání nástroje úspěšné | Očekávané |
| `DELETE → 405` | MCP klient testuje při úklidu | Normální - ignorujte |
| `POST → 400` | Špatný požadavek (nesprávný dotaz) | Zkontrolujte parametr `query` v `search_microsoft_learn_for_plan()` |
| `POST → 429` | Omezení rychlosti | Počkejte a zkuste to znovu. Snižte parametr `max_results` |
| `POST → 500` | Chyba MCP serveru | Přechodná - opakujte. Pokud trvá, MCP API Microsoft Learn může být mimo provoz |
| Timeout připojení | Síťový problém nebo MCP server nedostupný | Zkontrolujte internet. Zkuste `curl https://learn.microsoft.com/api/mcp` |

---

## Problémy s nasazením

### Kontejner se po nasazení nespustí

1. **Zkontrolujte logy kontejneru:**  
   - Otevřete postranní panel **Microsoft Foundry** → rozbalte **Hosted Agents (Preview)** → klikněte na svého agenta → rozbalte verzi → **Container Details** → **Logs**.  
   - Hledejte Python výjimky nebo chyby chybějících modulů.

2. **Běžné příčiny selhání při startu kontejneru:**

   | Chyba v logu | Příčina | Oprava |
   |--------------|---------|--------|
   | `ModuleNotFoundError` | V `requirements.txt` chybí balíček | Přidejte balíček, znovu nasaďte |
   | `RuntimeError: Missing required environment variable` | Env proměnné v `agent.yaml` nejsou nastaveny | Aktualizujte sekci `environment_variables` v `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity není nastaven | Foundry to nastavuje automaticky – ujistěte se, že nasazujete přes rozšíření |
   | `OSError: port 8088 already in use` | Dockerfile vystavuje špatný port nebo je konflikt portu | Ověřte `EXPOSE 8088` v Dockerfile a `CMD ["python", "main.py"]` |
   | Kontejner končí s kódem 1 | Nezachycená výjimka v `main()` | Nejprve testujte lokálně ([Modul 5](05-test-locally.md)) pro odchyt chyb před nasazením |

3. **Po opravě znovu nasaďte:**  
   `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → vyberte stejného agenta → nasaďte novou verzi.

### Nasazení trvá příliš dlouho

Multi-agent kontejnery se spouští déle, protože při spuštění vytvoří 4 instance agenta. Očekávané doby spuštění:

| Fáze | Očekávaná doba |
|-------|----------------|
| Sestavení kontejnerového image | 1-3 minuty |
| Push image do ACR | 30-60 sekund |
| Start kontejneru (single agent) | 15-30 sekund |
| Start kontejneru (multi-agent) | 30-120 sekund |
| Agent dostupný v Playgroundu | 1-2 minuty po "Started" |

> Pokud stav „Pending“ přetrvává déle než 5 minut, zkontrolujte logy kontejneru kvůli chybám.

---

## Problémy s RBAC a oprávněními

### `403 Forbidden` nebo `AuthorizationFailed`

Potřebujete roli **[Azure AI User](https://aka.ms/foundry-ext-project-role)** ve vašem Foundry projektu:

1. Přejděte na [Azure Portal](https://portal.azure.com) → váš Foundry **projekt**.  
2. Klikněte na **Access control (IAM)** → **Role assignments**.  
3. Vyhledejte své jméno → potvrďte, že je uvedena role **Azure AI User**.  
4. Pokud chybí: **Přidat** → **Add role assignment** → vyhledejte **Azure AI User** → přiřaďte si ji.

Viz dokumentace [RBAC pro Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) pro podrobnosti.

### Nasazení modelu není přístupné

Pokud agent vrací chyby související s modelem:

1. Ověřte, že je model nasazen: V postranním panelu Foundry rozbalte projekt → **Models** → zkontrolujte `gpt-4.1-mini` (nebo váš model) se stavem **Succeeded**.  
2. Ověřte shodu názvu nasazení: Porovnejte `MODEL_DEPLOYMENT_NAME` v `.env` (nebo v `agent.yaml`) s aktuálním názvem nasazení ve sidebaru.  
3. Pokud nasazení vypršelo (bezplatná vrstva): znovu nasaďte z [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problémy s Agent Inspectorem

### Inspector se otevře, ale ukazuje "Disconnected"

1. Ověřte, že server běží: hledejte v terminálu „Server running on http://localhost:8088“.  
2. Zkontrolujte port `5679`: Inspector se připojuje přes debugpy na port 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Restartujte server a znovu otevřete Inspector.

### Inspector ukazuje částečnou odpověď

Odpovědi multi-agenta jsou dlouhé a proudí inkrementálně. Počkejte na dokončení celé odpovědi (může trvat 30-60 sekund podle počtu gap karet a volání MCP nástroje).

Pokud je odpověď pravidelně oříznutá:  
- Zkontrolujte, zda instrukce GapAnalyzer obsahují blok `CRITICAL:`, který brání kombinaci gap karet.  
- Zkontrolujte limit tokenů vašeho modelu – `gpt-4.1-mini` podporuje až 32K výstupních tokenů, což by mělo stačit.

---

## Tipy pro výkon

### Pomalé odpovědi

Multi-agentní workflow jsou inherentně pomalejší než single-agentní kvůli sekvenčním závislostem a voláním MCP nástroje.

| Optimalizace | Jak | Dopad |
|--------------|-----|-------|
| Snížit počet MCP volání | Níže nastavte parametr `max_results` v nástroji | Méně HTTP požadavků |
| Zjednodušit instrukce | Kratší, více cílené promptování agenta | Rychlejší inference LLM |
| Použít `gpt-4.1-mini` | Rychlejší než `gpt-4.1` pro vývoj | Zhruba 2x rychlejší |
| Snížit detail gap karet | Zjednodušit formátace gap karty v instrukcích GapAnalyzer | Méně generovaného výstupu |

### Typické doby odpovědí (lokálně)

| Konfigurace | Očekávaná doba |
|-------------|---------------|
| `gpt-4.1-mini`, 3-5 gap karet | 30-60 sekund |
| `gpt-4.1-mini`, 8+ gap karet | 60-120 sekund |
| `gpt-4.1`, 3-5 gap karet | 60-120 sekund |
---

## Získání pomoci

Pokud si nevíte rady po vyzkoušení výše uvedených oprav:

1. **Zkontrolujte logy serveru** - Většina chyb generuje v terminálu Python stack trace. Přečtěte si celý traceback.
2. **Vyhledejte chybovou zprávu** - Zkopírujte text chyby a vyhledejte ho na [Microsoft Q&A pro Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Otevřete issue** - Vytvořte issue na [workshop repozitáři](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) s:
   - Chybovou zprávou nebo screenshotem
   - Verzemi vašich balíčků (`pip list | Select-String "agent-framework"`)
   - Vaší verzí Pythonu (`python --version`)
   - Informací, jestli je problém lokální nebo po nasazení

---

### Kontrolní seznam

- [ ] Dokážete identifikovat a opravit nejčastější chyby v multi-agent systému pomocí rychlé reference
- [ ] Umíte zkontrolovat a opravit konfiguraci `.env`
- [ ] Dokážete ověřit, že verze balíčků odpovídají požadované matici
- [ ] Rozumíte zápisům v MCP logu a dokážete diagnostikovat selhání nástrojů
- [ ] Umíte zkontrolovat logy kontejneru v případě neúspěchu nasazení
- [ ] Dokážete ověřit role RBAC v Azure Portalu

---

**Předchozí:** [07 - Verify in Playground](07-verify-in-playground.md) · **Domů:** [Lab 02 README](../README.md) · [Domovská stránka workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o vyloučení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). I když usilujeme o přesnost, mějte prosím na paměti, že automatické překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho rodném jazyce by měl být považován za autoritativní zdroj. Pro důležité informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakákoli nedorozumění nebo nesprávné výklady vyplývající z použití tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->