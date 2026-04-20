# Modul 8 - Odpravljanje težav (večagentni)

Ta modul zajema pogoste napake, popravke in strategije odpravljanja težav, specifične za večagentni delovni tok. Za splošne težave z uvajanjem Foundry si oglejte tudi [vodnik za odpravljanje težav v laboratoriju 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Hitri pregled: Napaka → Popravek

| Napaka / Simptom | Verjeten vzrok | Popravek |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Manjkajoča datoteka `.env` ali nastavljene vrednosti | Ustvarite `.env` z `PROJECT_ENDPOINT=<your-endpoint>` in `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtualno okolje ni aktivirano ali odvisnosti niso nameščene | Zaženite `.\.venv\Scripts\Activate.ps1`, nato `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Paket MCP ni nameščen (manjka v requirements) | Zaženite `pip install mcp` ali preverite, da je v `requirements.txt` kot prehodna odvisnost |
| Agent se zažene, a vrne prazni odgovor | Neskladje `output_executors` ali manjkajoče povezave | Preverite `output_executors=[gap_analyzer]` in da vse povezave obstajajo v `create_workflow()` |
| Samo 1 karta vrzeli (ostale manjkajo) | Navodila GapAnalyzer niso popolna | Dodajte odstavek `CRITICAL:` v `GAP_ANALYZER_INSTRUCTIONS` - glejte [Modul 3](03-configure-agents.md) |
| Ocena ujemanja je 0 ali manjka | MatchingAgent ni prejel podatkov iz višje ravni | Preverite, da sta `add_edge(resume_parser, matching_agent)` in `add_edge(jd_agent, matching_agent)` prisotni |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP strežnik je zavrnil klic orodja | Preverite internetno povezavo. Poskusite odpreti `https://learn.microsoft.com/api/mcp` v brskalniku. Poskusite znova |
| V izhodu ni URL-jev Microsoft Learn | Orodje MCP ni registrirano ali napačen endpoint | Preverite `tools=[search_microsoft_learn_for_plan]` na GapAnalyzer in pravilen `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | Drugi proces uporablja vrata 8088 | Zaženite `netstat -ano \| findstr :8088` (Windows) ali `lsof -i :8088` (macOS/Linux) in ustavite konfliktni proces |
| `Address already in use: port 5679` | Konflikt vrat Debugpy | Ustavite druge debug seje. Zaženite `netstat -ano \| findstr :5679` za iskanje in ustavitev procesa |
| Agent Inspector se ne odpre | Strežnik se ni povsem zagnal ali konflikt vrat | Počakajte na zapis "Server running". Preverite, da so vrata 5679 prosta |
| `azure.identity.CredentialUnavailableError` | Niste prijavljeni v Azure CLI | Zaženite `az login` in nato ponovno zaženite strežnik |
| `azure.core.exceptions.ResourceNotFoundError` | Model ni nameščen | Preverite, da se `MODEL_DEPLOYMENT_NAME` ujema z nameščenim modelom v vašem Foundry projektu |
| Status kontejnerja "Failed" po uvajanju | Zrušitev kontejnerja pri zagonu | Preverite dnevnik kontejnerja v stranski vrstici Foundry. Pogoste težave: manjkajoča spremenljivka okolja ali napaka uvoza |
| Uvajanje prikazuje "Pending" več kot 5 minut | Kontejner potrebuje preveč časa za zagon ali omejitve virov | Počakajte do 5 minut za večagentni način (ustvari 4 primere agentov). Če je še vedno čaka, preverite dnevnik |
| `ValueError` iz `WorkflowBuilder` | Neveljavna konfiguracija grafa | Prepričajte se, da je `start_executor` nastavljen, `output_executors` je seznam in ni krožnih povezav |

---

## Težave z okoljem in konfiguracijo

### Manjkajoče ali napačne vrednosti `.env`

Datoteka `.env` mora biti v mapi `PersonalCareerCopilot/` (na isti ravni kot `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Pričakovana vsebina `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Kako najti PROJECT_ENDPOINT:** 
- Odprite stransko vrstico **Microsoft Foundry** v VS Code → z desnim klikom kliknite vaš projekt → **Copy Project Endpoint**. 
- Ali pojdite na [Azure Portal](https://portal.azure.com) → vaš Foundry projekt → **Pregled** → **Projektni končni naslov**.

> **Kako najti MODEL_DEPLOYMENT_NAME:** V stranski vrstici Foundry razširite projekt → **Models** → poiščite ime nameščenega modela (npr. `gpt-4.1-mini`).

### Prednost vrednosti okolja

`main.py` uporablja `load_dotenv(override=False)`, kar pomeni:

| Prioriteta | Vir | Katera zmaga, če sta obe nastavljeni? |
|----------|--------|------------------------|
| 1 (najvišja) | Spremenljivka okolja lupine | Da |
| 2 | Datoteka `.env` | Samo, če lupinska spremenljivka ni nastavljena |

To pomeni, da runtime spremenljivke Foundry (nastavljene prek `agent.yaml`) prevladajo nad `.env` vrednostmi med gostovanim uvajanjem.

---

## Združljivost različic

### Matrika različic paketov

Za delovni tok več agentov so potrebne specifične različice paketov. Neujemanje povzroča napake pri izvajanju.

| Paket | Zahtevana različica | Ukaz za preverjanje |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | najnovejša predizdaja | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Pogoste napake zaradi različice

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Popravek: nadgradnja na rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` ni najden ali incompatibilen Inspector:**

```powershell
# Popravek: namestitev z zastavico --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Popravek: nadgradnja paketa mcp
pip install mcp --upgrade
```

### Preverite vse različice naenkrat

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Pričakovani izhod:

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

## Težave z orodjem MCP

### Orodje MCP ne vrne rezultatov

**Simptom:** Karte vrzeli kažejo "No results returned from Microsoft Learn MCP" ali "No direct Microsoft Learn results found".

**Možni vzroki:**

1. **Težava z omrežjem** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) ni dostopen.
   ```powershell
   # Preizkusi povezljivost
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Če to vrne `200`, je endpoint dostopen.

2. **Povpraševanje je preveč specifično** - Ime veščine je preozko za iskanje Microsoft Learn.
   - To je pričakovano za zelo specializirane veščine. Orodje ima rezervni URL v odgovoru.

3. **Potekel čas seje MCP** - Povezava Streamable HTTP je potekla.
   - Poskusite znova. Seje MCP so začasne in potrebujejo ponovno povezavo.

### Pojasnilo dnevnikov MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Dnevnik | Pomen | Ukrep |
|-----|---------|--------|
| `GET → 405` | MCP klient preverja pri inicializaciji | Normalno - prezrite |
| `POST → 200` | Klic orodja uspešen | Pričakovano |
| `DELETE → 405` | MCP klient preverja pri čiščenju | Normalno - prezrite |
| `POST → 400` | Napačen zahtevek (nepravilen poizvedba) | Preverite parameter `query` v `search_microsoft_learn_for_plan()` |
| `POST → 429` | Omejeno s kvačo | Počakajte in poskusite znova. Zmanjšajte parameter `max_results` |
| `POST → 500` | Napaka MCP strežnika | Začasno - poskusite znova. Če vztraja, je Microsoft Learn MCP API lahko nedosegljiv |
| Prekinitev povezave zaradi časovnega izteka | Težava z omrežjem ali MCP strežnik ni dosegljiv | Preverite internet. Poskusite `curl https://learn.microsoft.com/api/mcp` |

---

## Težave z uvajanjem

### Kontejner ne uspe zagnati po uvajanju

1. **Preverite dnevnike kontejnerja:**
   - Odprite stransko vrstico **Microsoft Foundry** → razširite **Hosted Agents (Preview)** → kliknite vašega agenta → razširite različico → **Podrobnosti kontejnerja** → **Dnevniki**.
   - Poiščite sledove napak v Pythonu ali napake o manjkajočem modulu.

2. **Pogoste napake pri zagonu kontejnerja:**

   | Napaka v dnevniku | Vzrok | Popravek |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` manjka paket | Dodajte paket, ponovno uvajanje |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` ne nastavlja spremenljivk okolja | Posodobite razdelek `environment_variables` v `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Ni nastavljena Managed Identity | Foundry to nastavi samodejno - zagotovite uvajanje z razširitvijo |
   | `OSError: port 8088 already in use` | Dockerfile izpostavlja napačna vrata ali konflikt vrat | Preverite `EXPOSE 8088` v Dockerfile in `CMD ["python", "main.py"]` |
   | Kontejner zapre z kodo 1 | Neobdelana izjema v `main()` | Najprej testirajte lokalno ([Modul 5](05-test-locally.md)) za ulov napak pred uvajanjem |

3. **Ponovno uvesti po popravljanju:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → izberite istega agenta → uvesti novo različico.

### Uvajanje traja predolgo

Večagentni kontejnerji potrebujejo več časa za zagon, ker na zagonu ustvarijo 4 primere agentov. Normalni časi zagona:

| Faza | Pričakovan čas |
|-------|------------------|
| Izgradnja slike kontejnerja | 1-3 minute |
| Potisk slike v ACR | 30-60 sekund |
| Zagon kontejnerja (en agent) | 15-30 sekund |
| Zagon kontejnerja (več agentov) | 30-120 sekund |
| Agent na voljo v Playgroundu | 1-2 minuti po "Started" |

> Če stanje "Pending" traja več kot 5 minut, preverite dnevnike kontejnerja za napake.

---

## Težave z RBAC in dovoljenji

### `403 Forbidden` ali `AuthorizationFailed`

Potrebujete vlogo **[Azure AI User](https://aka.ms/foundry-ext-project-role)** na vašem projektu Foundry:

1. Pojdite na [Azure Portal](https://portal.azure.com) → vaš Foundry **projekt**.
2. Kliknite **Access control (IAM)** → **Role assignments**.
3. Poiščite svoje ime → potrdite, da je **Azure AI User** na seznamu.
4. Če manjka: **Add** → **Add role assignment** → poiščite **Azure AI User** → dodelite svojemu računu.

Podrobnosti najdete v dokumentaciji o [RBAC za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Model ni dostopen

Če agent vrne napake, povezane z modelom:

1. Preverite, da je model nameščen: v stranski vrstici Foundry razširite projekt → **Models** → preverite `gpt-4.1-mini` (ali vaš model) s statusom **Succeeded**.
2. Preverite, da se ime uvajanja ujema: primerjajte `MODEL_DEPLOYMENT_NAME` v `.env` (ali `agent.yaml`) z dejanskim imenom uvajanja v stranski vrstici.
3. Če je uvajanje poteklo (brezplačni načrt): ponovno uvedite iz [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Težave z Agent Inspectorjem

### Inspector se odpre, a kaže "Disconnected"

1. Preverite, da strežnik teče: preverite vrstico "Server running on http://localhost:8088" v terminalu.
2. Preverite vrata `5679`: Inspector se povezuje preko debugpy prek vrat 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Ponovno zaženite strežnik in ponovno odprite Inspector.

### Inspector kaže delni odgovor

Odgovori več agentov so dolgi in se pretočno prikazujejo postopoma. Počakajte, da celoten odgovor zaključi (lahko traja 30-60 sekund, odvisno od števila kart vrzeli in klicev orodja MCP).

Če je odgovor dosledno skrajšan:
- Preverite, da navodila GapAnalyzer vsebujejo blok `CRITICAL:`, ki preprečuje združevanje kart vrzeli.
- Preverite omejitev žetonov vašega modela - `gpt-4.1-mini` podpira do 32K izhodnih žetonov, kar naj bi bilo dovolj.

---

## Nasveti za zmogljivost

### Počasni odgovori

Delovni tok več agentov je iz narave počasnejši kot en agent, zaradi zaporednih odvisnosti in klicev orodja MCP.

| Optimizacija | Kako | Vpliv |
|-------------|-----|--------|
| Zmanjšajte število klicev MCP | Znižajte parameter `max_results` v orodju | Manj HTTP klicev |
| Poenostavite navodila | Krajši, bolj osredotočeni agentovi pozivi | Hitrejše izvajanje LLM |
| Uporabite `gpt-4.1-mini` | Hitreje kot `gpt-4.1` za razvoj | ~2x hitrejše |
| Zmanjšajte podrobnosti kart vrzeli | Poenostavite format kart vrzeli v navodilih GapAnalyzer | Manj izhoda za generiranje |

### Tipični časi odgovorov (lokalno)

| Konfiguracija | Pričakovan čas |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 kart vrzeli | 30-60 sekund |
| `gpt-4.1-mini`, 8+ kart vrzeli | 60-120 sekund |
| `gpt-4.1`, 3-5 kart vrzeli | 60-120 sekund |
---

## Pridobivanje pomoči

Če ste obtičali po poskusu zgornjih popravkov:

1. **Preverite dnevnike strežnika** – Večina napak prikaže sled skladovnice (stack trace) Pythona v terminalu. Preberite celoten sled.
2. **Poiščite sporočilo o napaki** – Kopirajte besedilo napake in iščite v [Microsoft Q&A za Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Odprite prijavo** – Ustvarite prijavo v [delavski skladišču](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) z:
   - sporočilom o napaki ali posnetkom zaslona
   - različicami vaših paketov (`pip list | Select-String "agent-framework"`)
   - vašo različico Pythona (`python --version`)
   - ali je težava lokalna ali po namestitvi

---

### Kontrolna točka

- [ ] Znate identificirati in odpraviti najpogostejše napake več agentov z uporabo pregledne tabele
- [ ] Znate preveriti in popraviti konfiguracijske težave v `.env`
- [ ] Znate preveriti, ali se različice paketov ujemajo s predpisano matriko
- [ ] Razumete vnose dnevnikov MCP in lahko diagnosticirate napake orodja
- [ ] Znate preveriti dnevnike v vsebniku za napake po namestitvi
- [ ] Znate preveriti vloge RBAC v Azure Portalu

---

**Prejšnje:** [07 - Potrditev v igralnem polju](07-verify-in-playground.md) · **Domov:** [Navodila Lab 02](../README.md) · [Domača stran delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:  
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, prosimo, upoštevajte, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku velja za avtoritativni vir. Za ključne informacije priporočamo strokovni človeški prevod. Nismo odgovorni za morebitna nesporazume ali napačne interpretacije, ki bi nastale zaradi uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->