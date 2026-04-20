# Modul 8 - Rješavanje problema (Više agenata)

Ovaj modul pokriva uobičajene pogreške, popravke i strategije otklanjanja pogrešaka specifične za radni tok s više agenata. Za opće probleme s implementacijom Foundryja, također pogledajte [Lab 01 vodič za rješavanje problema](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Brzi pregled: Pogreška → Popravak

| Pogreška / Simptom | Vjerojatan uzrok | Popravak |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Nedostaje `.env` datoteka ili vrijednosti nisu postavljene | Kreirajte `.env` s `PROJECT_ENDPOINT=<your-endpoint>` i `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtualno okruženje nije aktivirano ili nisu instalirane ovisnosti | Pokrenite `.\.venv\Scripts\Activate.ps1` zatim `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP paket nije instaliran (nedostaje u zahtjevima) | Pokrenite `pip install mcp` ili provjerite da je u `requirements.txt` kao tranzitivna ovisnost |
| Agent se pokrene, ali vraća prazni odgovor | `output_executors` se ne podudara ili nedostaju veze (edges) | Provjerite `output_executors=[gap_analyzer]` i jesu li sve veze prisutne u `create_workflow()` |
| Samo 1 gap kartica (ostatak nedostaje) | Upute za GapAnalyzer su nepotpune | Dodajte odlomak `CRITICAL:` u `GAP_ANALYZER_INSTRUCTIONS` - vidi [Modul 3](03-configure-agents.md) |
| Fit score je 0 ili nedostaje | MatchingAgent nije primio podatke iz višeg sloja | Provjerite postoje li i `add_edge(resume_parser, matching_agent)` i `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server je odbio poziv alata | Provjerite internetsku vezu. Pokušajte otvoriti `https://learn.microsoft.com/api/mcp` u pregledniku. Ponovite pokušaj |
| Nema Microsoft Learn URL-ova u izlazu | MCP alat nije registriran ili je endpoint pogrešan | Provjerite `tools=[search_microsoft_learn_for_plan]` na GapAnalyzeru i je li `MICROSOFT_LEARN_MCP_ENDPOINT` točan |
| `Address already in use: port 8088` | Drugi proces koristi port 8088 | Pokrenite `netstat -ano \| findstr :8088` (Windows) ili `lsof -i :8088` (macOS/Linux) i zaustavite sukobljeni proces |
| `Address already in use: port 5679` | Sukob s debugpy portom | Zaustavite druge debug sesije. Pokrenite `netstat -ano \| findstr :5679` da pronađete i ubijete proces |
| Agent Inspector se neće otvoriti | Server nije u potpunosti pokrenut ili sukob porta | Pričekajte da se pojavi "Server running" u zapisu. Provjerite je li port 5679 slobodan |
| `azure.identity.CredentialUnavailableError` | Niste prijavljeni u Azure CLI | Pokrenite `az login` pa ponovno pokrenite server |
| `azure.core.exceptions.ResourceNotFoundError` | Implementacija modela ne postoji | Provjerite da `MODEL_DEPLOYMENT_NAME` odgovara implementiranom modelu u vašem Foundry projektu |
| Status kontejnera "Failed" nakon implementacije | Kontejner se srušio prilikom pokretanja | Provjerite logove kontejnera u Foundry bočnoj traci. Često je uzrok nedostajuća varijabla okoline ili greška u importu |
| Implementacija pokazuje "Pending" više od 5 minuta | Kontejner predugo traje za pokretanje ili ima ograničenja resursa | Pričekajte do 5 minuta za multi-agent (stvara 4 instance agenta). Ako je i dalje pending, provjerite logove |
| `ValueError` iz `WorkflowBuilder` | Neispravna konfiguracija grafa | Osigurajte da je `start_executor` postavljen, da je `output_executors` lista i da nema cikličnih veza |

---

## Problemi s okolinom i konfiguracijom

### Nedostajuće ili pogrešne vrijednosti `.env`

Datoteka `.env` mora biti u direktoriju `PersonalCareerCopilot/` (na istoj razini kao `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Očekivani sadržaj `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Pronalaženje vašeg PROJECT_ENDPOINT:** 
- Otvorite **Microsoft Foundry** bočnu traku u VS Code → desni klik na projekt → **Copy Project Endpoint**. 
- Ili idite na [Azure Portal](https://portal.azure.com) → vaš Foundry projekt → **Overview** → **Project endpoint**.

> **Pronalaženje vašeg MODEL_DEPLOYMENT_NAME:** U bočnoj traci Foundryja proširite projekt → **Models** → pronađite ime vašeg implementiranog modela (npr. `gpt-4.1-mini`).

### Prioritet varijabli okoline

`main.py` koristi `load_dotenv(override=False)`, što znači:

| Prioritet | Izvor | Pobjednik ako su oba postavljena? |
|----------|--------|----------------------------------|
| 1 (najviši) | Varijabla okoline školjke (shell) | Da |
| 2 | `.env` datoteka | Samo ako školjka nema postavljenu varijablu |

To znači da Foundry runtime varijable okoline (postavljene putem `agent.yaml`) imaju prednost nad `.env` vrijednostima tijekom hostane implementacije.

---

## Kompatibilnost verzija

### Matrica verzija paketa

Radni tok s više agenata zahtijeva specifične verzije paketa. Nepodudarne verzije uzrokuju pogreške pri izvođenju.

| Paket | Tražena verzija | Komanda za provjeru |
|---------|-----------------|---------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | najnovija pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Uobičajene pogreške verzija

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Popravi: nadogradnja na rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nije pronađen ili Inspector nije kompatibilan:**

```powershell
# Popravi: instaliraj s --pre zastavicom
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Popravi: nadogradi mcp paket
pip install mcp --upgrade
```

### Provjerite sve verzije odjednom

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Očekivani izlaz:

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

## Problemi s MCP alatom

### MCP alat ne vraća rezultate

**Simptom:** Gap kartice prikazuju "No results returned from Microsoft Learn MCP" ili "No direct Microsoft Learn results found".

**Mogući uzroci:**

1. **Problem s mrežom** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) nije dostupan.
   ```powershell
   # Testiraj povezanost
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Ako ovo vrati `200`, endpoint je dostupan.

2. **Upit je previše specifičan** - Ime vještine je previše usko za Microsoft Learn pretraživanje.
   - Ovo je očekivano za vrlo specijalizirane vještine. Alat ima rezervni URL u odgovoru.

3. **MCP sesija je istekla** - Streamable HTTP veza je istekla.
   - Ponovite zahtjev. MCP sesije su kratkotrajnog trajanja i mogu zahtijevati ponovno spajanje.

### Objašnjenje MCP logova

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Značenje | Radnja |
|-----|---------|--------|
| `GET → 405` | MCP klijent testira tijekom inicijalizacije | Normalno - zanemarite |
| `POST → 200` | Poziv alata je uspješan | Očekivano |
| `DELETE → 405` | MCP klijent testira tijekom čišćenja | Normalno - zanemarite |
| `POST → 400` | Loš zahtjev (neispravan upit) | Provjerite parametar `query` u `search_microsoft_learn_for_plan()` |
| `POST → 429` | Ograničenje brzine (rate limited) | Pričekajte i pokušajte ponovo. Smanjite parametar `max_results` |
| `POST → 500` | Greška MCP servera | Privremeno - pokušajte ponovo. Ako traje, Microsoft Learn MCP API može biti nedostupan |
| Vrijeme veze isteklo | Problem s mrežom ili MCP server nije dostupan | Provjerite internet. Pokušajte `curl https://learn.microsoft.com/api/mcp` |

---

## Problemi s implementacijom

### Kontejner ne uspijeva pokrenuti se nakon implementacije

1. **Provjerite logove kontejnera:**
   - Otvorite **Microsoft Foundry** bočnu traku → proširite **Hosted Agents (Preview)** → kliknite na vašeg agenta → proširite verziju → **Container Details** → **Logs**.
   - Tražite Python stog tragove ili greške nedostajućih modula.

2. **Uobičajeni uzroci pogrešaka pri pokretanju kontejnera:**

   | Pogreška u logovima | Uzrok | Popravak |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` ne sadrži paket | Dodajte paket, ponovno implementirajte |
   | `RuntimeError: Missing required environment variable` | Varijable okoline u `agent.yaml` nisu postavljene | Ažurirajte `agent.yaml` → dio `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity nije konfigurirana | Foundry automatski postavlja - osigurajte implementaciju preko ekstenzije |
   | `OSError: port 8088 already in use` | Dockerfile otkriva pogrešan port ili sukob porta | Provjerite `EXPOSE 8088` u Dockerfileu i `CMD ["python", "main.py"]` |
   | Kontejner izlazi s kodom 1 | Neuhvaćena iznimka u `main()` | Prvo testirajte lokalno ([Modul 5](05-test-locally.md)) da uhvatite greške prije implementacije |

3. **Ponovno implementirajte nakon popravka:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → odaberite istog agenta → implementirajte novu verziju.

### Implementacija traje predugo

Multi-agent kontejneri traju duže za pokretanje jer stvaraju 4 instance agenta pri pokretanju. Normalno trajanje pokretanja:

| Faza | Očekivano trajanje |
|-------|------------------|
| Izgradnja image kontejnera | 1-3 minute |
| Slanje image u ACR | 30-60 sekundi |
| Pokretanje kontejnera (jedan agent) | 15-30 sekundi |
| Pokretanje kontejnera (više agenata) | 30-120 sekundi |
| Agent dostupan u Playgroundu | 1-2 minute nakon statusa "Started" |

> Ako status "Pending" traje duže od 5 minuta, provjerite logove kontejnera zbog grešaka.

---

## RBAC i problemi s dopuštenjima

### `403 Forbidden` ili `AuthorizationFailed`

Potrebna vam je uloga **[Azure AI User](https://aka.ms/foundry-ext-project-role)** na vašem Foundry projektu:

1. Idite na [Azure Portal](https://portal.azure.com) → vaš Foundry **projekt** resurs.
2. Kliknite **Access control (IAM)** → **Role assignments**.
3. Potražite svoje ime → potvrdite da je **Azure AI User** na listi.
4. Ako nedostaje: **Add** → **Add role assignment** → potražite **Azure AI User** → dodijelite vašem računu.

Za detalje pogledajte dokumentaciju [RBAC za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Implementacija modela nije dostupna

Ako agent vraća pogreške vezane za model:

1. Provjerite da je model implementiran: Foundry bočna traka → proširite projekt → **Models** → provjerite postoji li `gpt-4.1-mini` (ili vaš model) sa statusom **Succeeded**.
2. Provjerite podudara li se ime implementacije: usporedite `MODEL_DEPLOYMENT_NAME` u `.env` (ili `agent.yaml`) s pravim imenom implementacije u bočnoj traci.
3. Ako je implementacija istekla (besplatni sloj): ponovno implementirajte iz [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problemi s Agent Inspektorom

### Inspektor se otvara, ali pokazuje "Disconnected"

1. Provjerite radi li server: u terminalu potražite "Server running on http://localhost:8088".
2. Provjerite port `5679`: Inspektor se povezuje preko debugpy na port 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Ponovno pokrenite server i ponovno otvorite inspektor.

### Inspektor prikazuje djelomični odgovor

Odgovori više agenata su dugi i strujaju inkrementalno. Pričekajte da se cijeli odgovor dovrši (može potrajati 30-60 sekundi, ovisno o broju gap kartica i MCP poziva).

Ako je odgovor stalno skraćen:
- Provjerite da GapAnalyzer upute sadrže blok `CRITICAL:` koji sprječava spajanje gap kartica.
- Provjerite ograničenje tokena vašeg modela - `gpt-4.1-mini` podržava do 32K izlaznih tokena, što bi trebalo biti dovoljno.

---

## Savjeti za performanse

### Spori odgovori

Radni tok s više agenata je inherentno sporiji od jednoga zbog sekvencijalnih ovisnosti i MCP poziva.

| Optimizacija | Kako | Utjecaj |
|-------------|-----|---------|
| Smanjite pozive MCP alatu | Smanjite parametar `max_results` u alatu | Manje HTTP zahtjeva |
| Pojednostavite upute | Kraći, fokusiraniji agent promptovi | Brže izvođenje LLM-a |
| Koristite `gpt-4.1-mini` | Brži od `gpt-4.1` za razvoj | Otprilike 2x brže |
| Smanjite detalje gap kartica | Pojednostavite format gap kartica u GapAnalyzer uputama | Manje generiranog izlaza |

### Tipično trajanje odgovora (lokalno)

| Konfiguracija | Očekivano vrijeme |
|--------------|-------------------|
| `gpt-4.1-mini`, 3-5 gap kartica | 30-60 sekundi |
| `gpt-4.1-mini`, 8+ gap kartica | 60-120 sekundi |
| `gpt-4.1`, 3-5 gap kartica | 60-120 sekundi |
---

## Dobivanje pomoći

Ako zapnete nakon što ste isprobali gore navedene popravke:

1. **Provjerite zapisnike servera** - Većina pogrešaka generira Python stack trace u terminalu. Pročitajte cijeli traceback.
2. **Pretražite poruku o pogrešci** - Kopirajte tekst pogreške i potražite na [Microsoft Q&A za Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Otvorite problem (issue)** - Podnesite issue na [workshop repozitoriju](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) s:
   - Porukom o pogrešci ili snimkom zaslona
   - Verzijama vaših paketa (`pip list | Select-String "agent-framework"`)
   - Verzijom Pythona (`python --version`)
   - Je li problem lokalni ili nakon implementacije

---

### Kontrolna lista

- [ ] Možete identificirati i popraviti najčešće višagentne pogreške koristeći tablicu brzog pregleda
- [ ] Znate kako provjeriti i popraviti konfiguracijske probleme `.env` datoteke
- [ ] Možete potvrditi da se verzije paketa podudaraju s potrebnom matricom
- [ ] Razumijete MCP zapise i možete dijagnosticirati kvarove alata
- [ ] Znate kako provjeriti zapisnike kontejnera za pogreške implementacije
- [ ] Možete potvrditi RBAC uloge u Azure portalu

---

**Prethodno:** [07 - Verify in Playground](07-verify-in-playground.md) · **Početna:** [Lab 02 README](../README.md) · [Početna radionice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Odricanje od odgovornosti**:
Ovaj dokument je preveden pomoću AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, molimo imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na njegovom izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporučuje se stručni ljudski prijevod. Ne snosimo odgovornost za bilo kakve nesporazume ili pogrešna tumačenja proizašla iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->