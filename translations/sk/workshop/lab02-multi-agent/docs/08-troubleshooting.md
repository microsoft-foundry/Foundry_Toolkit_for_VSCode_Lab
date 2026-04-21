# Modul 8 - Riešenie problémov (Multi-Agent)

Tento modul pokrýva bežné chyby, opravy a stratégie ladenia špecifické pre multi-agentný pracovný tok. Pre všeobecné problémy s nasadením Foundry sa tiež pozrite na [Lab 01 príručku riešenia problémov](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Rýchla referencia: Chyba → Oprava

| Chyba / Príznak | Pravdepodobná príčina | Oprava |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Súbor `.env` chýba alebo hodnoty nie sú nastavené | Vytvorte `.env` so `PROJECT_ENDPOINT=<your-endpoint>` a `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuálne prostredie nie je aktivované alebo závislosti nie sú nainštalované | Spustite `.\.venv\Scripts\Activate.ps1` potom `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Balík MCP nie je nainštalovaný (chýba v požiadavkách) | Spustite `pip install mcp` alebo skontrolujte, či je v `requirements.txt` ako tranzitívna závislosť |
| Agent sa spustí, ale vracia prázdnu odpoveď | Nesúlad `output_executors` alebo chýbajú spoje (edges) | Overte `output_executors=[gap_analyzer]` a či všetky spoje existujú v `create_workflow()` |
| Len 1 gap karta (ostatné chýbajú) | Inštrukcie GapAnalyzer nie sú kompletné | Pridajte odsek `CRITICAL:` do `GAP_ANALYZER_INSTRUCTIONS` - pozri [Modul 3](03-configure-agents.md) |
| Skóre zhody je 0 alebo chýba | MatchingAgent nedostal dáta z upstream | Overte, či existujú `add_edge(resume_parser, matching_agent)` a `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server odmietol volanie nástroja | Skontrolujte pripojenie na internet. Skúste otvoriť `https://learn.microsoft.com/api/mcp` v prehliadači. Skúste znova |
| Žiadne Microsoft Learn URL vo výstupe | MCP nástroj nie je registrovaný alebo je chybný endpoint | Overte `tools=[search_microsoft_learn_for_plan]` na GapAnalyzer a správnosť `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | Iný proces používa port 8088 | Spustite `netstat -ano \| findstr :8088` (Windows) alebo `lsof -i :8088` (macOS/Linux) a ukončite konfliktujúci proces |
| `Address already in use: port 5679` | Konflikt portu debugpy | Ukončite ostatné debug session. Spustite `netstat -ano \| findstr :5679` pre nájdenie a ukončenie procesu |
| Agent Inspector sa neotvorí | Server nie je úplne spustený alebo je konflikt portov | Počkajte na log "Server running". Skontrolujte, či je port 5679 voľný |
| `azure.identity.CredentialUnavailableError` | Nie ste prihlásený do Azure CLI | Spustite `az login` a reštartujte server |
| `azure.core.exceptions.ResourceNotFoundError` | Nasadenie modelu neexistuje | Overte, či sa `MODEL_DEPLOYMENT_NAME` zhoduje s nasadeným modelom vo vašom projekte Foundry |
| Stav kontajnera "Failed" po nasadení | Kontajner spadol pri štarte | Skontrolujte logy kontajnera v Foundry postrannom paneli. Bežné: chýbajúca env premenná alebo chyba importu |
| Nasadenie sa zobrazuje ako "Pending" > 5 minút | Kontajner sa štartuje príliš dlho alebo obmedzenia zdrojov | Počkajte až 5 minút pre multi-agent (vytvára 4 inštancie agenta). Ak stále čaká, skontrolujte logy |
| `ValueError` z `WorkflowBuilder` | Neplatná konfigurácia grafu | Uistite sa, že `start_executor` je nastavený, `output_executors` je zoznam a nie sú kruhové spoje |

---

## Problémy s prostredím a konfiguráciou

### Chýbajúce alebo nesprávne hodnoty `.env`

Súbor `.env` musí byť v adresári `PersonalCareerCopilot/` (na rovnakej úrovni ako `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Očakávaný obsah `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Ako nájsť PROJECT_ENDPOINT:** 
- Otvorte postranný panel **Microsoft Foundry** vo VS Code → kliknite pravým tlačidlom na projekt → **Copy Project Endpoint**. 
- Alebo choďte na [Azure Portal](https://portal.azure.com) → váš projekt Foundry → **Prehľad** → **Project endpoint**.

> **Ako nájsť MODEL_DEPLOYMENT_NAME:** V Foundry postrannom paneli rozbaľte projekt → **Models** → nájdite názov nasadeného modelu (napr. `gpt-4.1-mini`).

### Priorita env premenných

`main.py` používa `load_dotenv(override=False)`, čo znamená:

| Priorita | Zdroj | Vyhrá, ak sú obe nastavené? |
|----------|--------|------------------------|
| 1 (najvyššia) | Premenná prostredia shellu | Áno |
| 2 | Súbor `.env` | Len ak shell premenná nie je nastavená |

To znamená, že runtime env premenné Foundry (nastavené cez `agent.yaml`) majú prednosť pred hodnotami `.env` pri nasadení.

---

## Kompatibilita verzií

### Matica verzií balíkov

Multi-agentný pracovný tok vyžaduje špecifické verzie balíkov. Nezladené verzie spôsobujú runtime chyby.

| Balík | Požadovaná verzia | Príkaz na kontrolu |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | najnovšia pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Bežné chyby verzií

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Oprava: aktualizácia na rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nenájdený alebo Inspector nekompatibilný:**

```powershell
# Oprava: inštalovať s príznakom --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Oprava: aktualizovať balík mcp
pip install mcp --upgrade
```

### Overenie všetkých verzií naraz

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Očakávaný výstup:

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

## Problémy s MCP nástrojom

### MCP nástroj nevracia výsledky

**Príznak:** Gap karty hlásia "No results returned from Microsoft Learn MCP" alebo "No direct Microsoft Learn results found".

**Možné príčiny:**

1. **Sieťový problém** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) nie je dostupný.
   ```powershell
   # Otestujte pripojenie
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Ak vráti `200`, endpoint je dostupný.

2. **Príliš špecifický dotaz** - Názov zručnosti je príliš úzky pre vyhľadávanie Microsoft Learn.
   - Toto je očakávané pre veľmi špecializované zručnosti. Nástroj má v odpovedi záložnú URL.

3. **Časový limit MCP relácie** - Streamable HTTP pripojenie vypršalo.
   - Skúste požiadavku znova. MCP relácie sú dočasné a môže byť potrebné opätovné prepojenie.

### Vysvetlenie MCP logov

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Význam | Akcia |
|-----|---------|--------|
| `GET → 405` | MCP klient testuje počas inicializácie | Normálne - ignorujte |
| `POST → 200` | Volanie nástroja úspešné | Očakávané |
| `DELETE → 405` | MCP klient testuje počas ukončenia | Normálne - ignorujte |
| `POST → 400` | Nesprávna požiadavka (chybný dotaz) | Skontrolujte parameter `query` v `search_microsoft_learn_for_plan()` |
| `POST → 429` | Limitované počtom volaní | Počkajte a skúste znova. Znížte parameter `max_results` |
| `POST → 500` | Chyba MCP servera | Prechodná - skúste znova. Ak pretrváva, Microsoft Learn MCP API môže byť nedostupné |
| Časový limit pripojenia | Sieťový problém alebo server MCP nedostupný | Skontrolujte internet. Skúste `curl https://learn.microsoft.com/api/mcp` |

---

## Problémy s nasadením

### Kontajner po nasadení nezačne

1. **Skontrolujte logy kontajnera:**
   - Otvorte postranný panel **Microsoft Foundry** → rozbaľte **Hosted Agents (Preview)** → kliknite na svojho agenta → rozbaľte verziu → **Container Details** → **Logs**.
   - Hľadajte python chyby alebo chýbajúce moduly.

2. **Bežné chyby pri štarte kontajnera:**

   | Chyba v logoch | Príčina | Oprava |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | V `requirements.txt` chýba balík | Pridajte balík, znovu nasaďte |
   | `RuntimeError: Missing required environment variable` | Env premenné v `agent.yaml` nie sú nastavené | Aktualizujte sekciu `environment_variables` v `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity nie je nakonfigurovaný | Foundry to nastavuje automaticky - nasadzujte cez rozšírenie |
   | `OSError: port 8088 already in use` | Dockerfile exponuje nesprávny port alebo je konflikt portov | Overte `EXPOSE 8088` v Dockerfile a `CMD ["python", "main.py"]` |
   | Kontajner končí kód 1 | Nezachytená výnimka v `main()` | Najprv otestujte lokálne ([Modul 5](05-test-locally.md)) pre zachytenie chýb pred nasadením |

3. **Znovu nasaďte po oprave:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → vyberte rovnakého agenta → nasaďte novú verziu.

### Nasadenie trvá príliš dlho

Multi-agentné kontajnery sa štartujú dlhšie, pretože vytvárajú 4 inštancie agenta pri štarte. Bežné časy štartu:

| Fáza | Očakávaná doba |
|-------|------------------|
| Vytvorenie obrazu kontajnera | 1-3 minúty |
| Push obrazu do ACR | 30-60 sekúnd |
| Štart kontajnera (single agent) | 15-30 sekúnd |
| Štart kontajnera (multi-agent) | 30-120 sekúnd |
| Agent dostupný v Playground | 1-2 minúty po "Started" |

> Ak stav "Pending" pretrváva viac ako 5 minút, skontrolujte logy kontajnera na chyby.

---

## Problémy s RBAC a oprávneniami

### `403 Forbidden` alebo `AuthorizationFailed`

Potrebujete rolu **[Azure AI User](https://aka.ms/foundry-ext-project-role)** vo vašom projekte Foundry:

1. Choďte na [Azure Portal](https://portal.azure.com) → váš projekt Foundry.
2. Kliknite na **Access control (IAM)** → **Role assignments**.
3. Vyhľadajte svoje meno → overte, či je uvedená rola **Azure AI User**.
4. Ak chýba: **Add** → **Add role assignment** → vyhľadajte **Azure AI User** → priraďte svojmu účtu.

Pozrite si dokumentáciu [RBAC pre Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) pre detaily.

### Nasadenie modelu nie je prístupné

Ak agent vracia chyby súvisiace s modelom:

1. Overte, či je model nasadený: postranný panel Foundry → rozbaľte projekt → **Models** → skontrolujte `gpt-4.1-mini` (alebo váš model) s stavom **Succeeded**.
2. Overte, či sa názov nasadenia zhoduje: porovnajte `MODEL_DEPLOYMENT_NAME` v `.env` (alebo `agent.yaml`) s faktickým názvom nasadenia v postrannom paneli.
3. Ak nasadenie vypršalo (free tier): znovu nasaďte z [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problémy s Agent Inspector

### Inspector sa otvorí, ale ukazuje "Disconnected"

1. Overte, či server beží: skontrolujte, či sa v termináli zobrazuje "Server running on http://localhost:8088".
2. Skontrolujte port `5679`: Inspector sa pripája cez debugpy na porte 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Reštartujte server a znovu otvorte Inspector.

### Inspector zobrazuje čiastočnú odpoveď

Odpovede multi-agenta sú dlhé a prúdia postupne. Počkajte, kým sa celá odpoveď dokončí (môže to trvať 30-60 sekúnd v závislosti od počtu gap kariet a volaní MCP nástroja).

Ak je odpoveď konzistentne orezaná:
- Skontrolujte, či inštrukcie GapAnalyzer obsahujú blok `CRITICAL:`, ktorý zabraňuje zlučovaniu gap kariet.
- Skontrolujte limit tokenov vášho modelu - `gpt-4.1-mini` podporuje až 32K výstupných tokenov, čo by malo byť dostatočné.

---

## Tipy pre výkon

### Pomalé odpovede

Multi-agentné pracovné toky sú inherentne pomalšie ako single-agentné kvôli sekvenčným závislostiam a volaniam MCP nástroja.

| Optimalizácia | Ako | Dopad |
|-------------|-----|--------|
| Znížiť volania MCP | Znížením parametra `max_results` v nástroji | Menej HTTP požiadaviek |
| Zjednodušiť inštrukcie | Kratšie, fokusované agentné podnety | Rýchlejšie LLM vyhodnotenie |
| Použiť `gpt-4.1-mini` | Rýchlejší ako `gpt-4.1` pre vývoj | ~2x zrýchlenie |
| Znížiť detaily gap karty | Jednoduchší formát gap karty v inštrukciách GapAnalyzer | Menej výstupu na generovanie |

### Typické časy odozvy (lokálne)

| Konfigurácia | Očakávaný čas |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap kariet | 30-60 sekúnd |
| `gpt-4.1-mini`, 8+ gap kariet | 60-120 sekúnd |
| `gpt-4.1`, 3-5 gap kariet | 60-120 sekúnd |
---

## Získanie pomoci

Ak ste uviazli po vyskúšaní vyššie uvedených opráv:

1. **Skontrolujte logy servera** - Väčšina chýb vytvára v termináli Python stack trace. Prečítajte si celý traceback.
2. **Vyhľadajte chybové hlásenie** - Skopírujte text chyby a vyhľadajte ho v [Microsoft Q&A pre Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Otvorte issue** - Založte issue v [workshop repozitári](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) spolu s:
   - Chybovým hlásením alebo screenshotom
   - Verziami vašich balíkov (`pip list | Select-String "agent-framework"`)
   - Verziou Pythonu (`python --version`)
   - Informáciou, či je problém lokálny alebo po nasadení

---

### Kontrolný zoznam

- [ ] Viete identifikovať a opraviť najbežnejšie chyby viacerých agentov pomocou prehľadnej tabuľky
- [ ] Viete, ako skontrolovať a opraviť problémy s konfiguráciou `.env`
- [ ] Viete overiť, či verzie balíkov zodpovedajú požadovanej matici
- [ ] Rozumiete zápisom v MCP logoch a viete diagnostikovať zlyhania nástrojov
- [ ] Viete, ako skontrolovať logy kontajnerov pri zlyhaniach nasadenia
- [ ] Viete overiť RBAC role v Azure Portáli

---

**Predchádzajúce:** [07 - Verify in Playground](07-verify-in-playground.md) · **Domov:** [Lab 02 README](../README.md) · [Domov Workshopu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zrieknutie sa zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa usilujeme o presnosť, prosím vezmite na vedomie, že automatizované preklady môžu obsahovať chyby alebo nepresnosti. Považujte pôvodný dokument v jeho rodnom jazyku za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za akékoľvek nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->