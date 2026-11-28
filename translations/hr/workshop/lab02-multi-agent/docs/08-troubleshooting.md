# Modul 8 - Rješavanje problema

Ovaj modul pokriva uobičajene pogreške, popravke i strategije ispravljanja pogrešaka specifične za višagentni tijek rada.

## Problemi s izlazom agenta

### GapAnalyzer kaže „Još uvijek nemam odgovarajući izvještaj“

**Simptom:** Odgovor GapAnalyzer-a traži od vas da zalijepite izvještaj o podudaranju s „Nedostajućim vještinama“ i „Prazninama u certifikaciji.“ To se događa čak i kada ste poslali i životopis i opis posla.

**Uzrok:** Tekst opisa posla nije proslijeđen Agentu za opis posla. S `context_mode="last_agent"`, `resume_executor` je jedini izvršitelj koji ikada vidi izvornu poruku korisnika. Ako `RESUME_PARSER_INSTRUCTIONS` ne uključuje tekst opisa posla u svoj izlaz, Agent za opis posla nema opis za parsiranje, MatchingAgent ne može izračunati ocjenu podudaranja, a GapAnalyzer prima besmisleni ulaz.

**Dijagnoza:**

U zapisima poslužitelja potražite MatchingAgent opseg. Ako sadrži:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
prosljeđivanje nedostaje ili je prekinuto.

**Popravak:** Potvrdite da `RESUME_PARSER_INSTRUCTIONS` u `main.py` sadrži `[JOB DESCRIPTION PASS-THROUGH]` dio i pravilo:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Također potvrdite da `JOB_DESCRIPTION_INSTRUCTIONS` sadrži `[PARSED RESUME PASS-THROUGH]` pravilo prosljeđivanja:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Ako je bilo koji blok uputa privremeni iz čarobnjaka za kosture, zamijenite ga potpunom verzijom iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent ispisuje “Cannot compute fit score - no JD provided”

Ovo je isti temeljni uzrok kao gore. MatchingAgent je primio izlaz JD Agenta, ali je odjeljak `[PARSED RESUME PASS-THROUGH]` nedostajao ili je bio prazan, pa nije mogao usporediti dva profila. Potvrdite:
1. `JOB_DESCRIPTION_INSTRUCTIONS` uključuje pravilo relaya: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` govori agentu da traži odjeljke `[JD REQUIREMENTS]` i `[PARSED RESUME PASS-THROUGH]`.

Zamijenite oba bloka uputa potpunim verzijama iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odgovor se pojavljuje dva puta

**Simptom:** Izlaz GapAnalyzer-a (ili cijeli izlaz pipelinea) pojavljuje se dva puta u odgovoru Agent Inspectora.

**Uzrok:** `WorkflowBuilder` koristi OR-semantiku za dolazne bridove - izvršitelj niže razine pokreće se čim **bilo koji** prethodnik završi. Ako `matching_executor` ima dva dolazna brida (jedan od `resume_executor` i jedan od `jd_executor`), pokreće se dva puta: jednom kad ResumeParser završi i opet kad JD Agent završi. GapAnalyzer se tada također izvršava dva puta.

**Popravak:** Osigurajte da je graf `WorkflowBuilder` strogo sekvencijalni pipeline bez fan-ina:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Ako imate nepovezanu liniju `.add_edge(resume_executor, matching_executor)`, uklonite je. `[PARSED RESUME PASS-THROUGH]` relay u izlazu JD Agenta već daje MatchingAgentu pristup životopisu.

---

## Problemi s okolinom i konfiguracijom

### Nedostajuće ili pogrešne vrijednosti `.env`

Datoteka `.env` mora biti u direktoriju `PersonalCareerCopilot/` (isti nivo kao `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Očekivani sadržaj `.env`:

**Put A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Put B - Foundry lokalno:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Oba puta koriste `FOUNDRY_PROJECT_ENDPOINT`. Vrijednost se razlikuje: cloud koristi `https://` Foundry endpoint; lokalno koristi `http://localhost:5273/v1`. Pokrenite `foundry model list` da potvrdite točan alias modela za Put B.

> **Pronalazak vašeg `FOUNDRY_PROJECT_ENDPOINT`:** 
- Otvorite bočnu traku **Foundry Toolkit** u VS Code → desni klik na vaš projekt → **Copy Project Endpoint**. 
- Ili idite na [Azure Portal](https://portal.azure.com) → vaš Foundry projekt → **Overview** → **Project endpoint**.

> **Pronalazak vašeg `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** U Foundry Toolkit bočnoj traci, proširite vaš projekt → **Models** → pronađite ime vašeg raspoređenog modela (npr. `gpt-4.1-mini`).

### Prednost varijabli okoline

`main.py` koristi `load_dotenv(override=True)`, što znači:

| Prioritet | Izvor | Pobjednik kada su oba postavljena? |
|----------|--------|------------------------------|
| 1 (najveći) | Datoteka `.env` | Da |
| 2 | Shell / varijabla okoline u kontejneru | Koristi se ako isti ključ nije prisutan u `.env` |

U lokalnom razvoju to čini `.env` izvorom istine (uređivanje `.env` odmah utječe na izvođenje). U hostanoj implementaciji, Foundry ubrizgava varijable okoline na razini kontejnera; budući da `.env` nije dio raspoređene slike za ovaj lab postav, koriste se ubrizgane vrijednosti kontejnera.

---

## Kompatibilnost verzija

### Matrica verzija paketa

Viški agent workflow zahtijeva specifične verzije paketa. Nepodudarne verzije uzrokuju pogreške u izvođenju.

| Paket | Potrebna verzija | Komanda za provjeru |
|---------|-----------------|------------------|
| `agent-framework-foundry` | najnovija | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | najnovija | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | najnovija | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Uobičajene pogreške verzija

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Potvrdite sve verzije odjednom

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Očekivani izlaz:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problemi s implementacijom

### Kontejner ne uspijeva pokrenuti nakon implementacije

1. **Provjerite logove kontejnera:**
   - Otvorite bočnu traku **Foundry Toolkit** → ispod vašeg projekta kliknite **Agents** → kartica **Hosted Agent** → kliknite na vašeg agenta. Provjerite **Status** na kartici **Details**, zatim otvorite karticu **Playground** i upotrijebite karticu **Logs** u panelu **Session Details** za pregled izlaza kontejnera.
   - Potražite Python stogove pogrešaka ili greške zbog nedostajućih modula.

2. **Uobičajeni uzroci neuspjeha pokretanja kontejnera:**

   | Pogreška u logovima | Uzrok | Popravak |
   |---------------------|-------|---------|
   | `ModuleNotFoundError` | Nedostaje paket `requirements.txt` | Dodajte paket, ponovno rasporedite |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` ili `.env` varijable okoline nisu postavljene | Ažurirajte `agent.yaml` → odjeljak `environment_variables` (hostano) ili `.env` (lokalno) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity nije konfiguriran | Foundry to automatski postavlja - osigurajte da implementirate putem nastavka |
   | `OSError: port 8088 already in use` | Dockerfile izlaže pogrešan port ili sukob portova | Provjerite `EXPOSE 8088` u Dockerfile i `CMD ["python", "main.py"]` |
   | Kontejner izlazi s kodom 1 | Neuhvaćeni izuzetak u `main()` | Prvo testirajte lokalno ([Modul 5](05-test-locally.md)) da biste uhvatili pogreške prije implementacije |

3. **Ponovno rasporedite nakon popravka:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → odaberite istog agenta → rasporedite novu verziju.

### Implementacija traje predugo

Multi-agent kontejneri se sporije pokreću jer stvaraju 4 instance agenta pri pokretanju. Normalna vremena pokretanja:

| Faza | Očekivano trajanje |
|-------|-------------------|
| Izgradnja slike kontejnera | 1-3 minute |
| Guranje slike u ACR | 30-60 sekundi |
| Pokretanje kontejnera (jedan agent) | 15-30 sekundi |
| Pokretanje kontejnera (više agenata) | 30-120 sekundi |
| Agent dostupan u Playgroundu | 1-2 minute nakon "Started" |

> Ako status "Pending" traje dulje od 5 minuta, provjerite logove kontejnera za pogreške.

---

## RBAC i problemi s dopuštenjima

### `403 Forbidden` ili `AuthorizationFailed`

Potrebna vam je uloga **[Foundry User](https://aka.ms/foundry-ext-project-role)** u vašem Foundry projektu (ranije nazvana **Azure AI User** - ID uloge nije promijenjen):

1. Idite na [Azure Portal](https://portal.azure.com) → resurs vašeg Foundry **projekta**.
2. Kliknite **Access control (IAM)** → **Role assignments**.
3. Potražite svoje ime → potvrdite da je **Foundry User** (ili staro ime **Azure AI User**) na popisu.
4. Ako nedostaje: **Dodaj** → **Add role assignment** → potražite **Foundry User** → dodijelite svom računu.

Pogledajte dokumentaciju [RBAC za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) za detalje.

### Nema pristupa implementaciji modela

Ako agent vraća pogreške vezane uz model:

1. Provjerite je li model implementiran: Foundry bočna traka → proširite projekt → **Models** → provjerite postoji li `gpt-4.1-mini` (ili vaš model) sa statusom **Succeeded**.
2. Provjerite da ime implementacije odgovara: usporedite `AZURE_AI_MODEL_DEPLOYMENT_NAME` u `.env` (ili `agent.yaml`) s stvarnim imenom implementacije u bočnoj traci.
3. Ako je implementacija istekla (besplatni sloj): ponovno implementirajte iz [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemi s Foundry Local (Put B)

### Foundry Local servis nije pokrenut

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Simptom | Uzrok | Popravak |
|---------|-------|---------|
| Health check vraća `503` | Servis nije pokrenut | Pokrenite `foundry local start` ili kliknite **Start** u Foundry Toolkit bočnoj traci |
| Health check istječe | Model se još učitava | Pričekajte 30–60 s nakon pokretanja; veći modeli trebaju više vremena |
| `StatusCode: 404` na `/v1/health` | Pogrešan port | Zadano je `5273`. Provjerite `foundry local status` za stvarni port |
| Nedovoljno resursa | Foundry Local treba ~4 GB slobodne RAM memorije | Zatvorite druge aplikacije |
| Preuzimanje modela ne uspijeva | Malo slobodnog mjesta na disku | Modeli su 2–8 GB. Oslobodite prostor pa pokrenite `foundry model pull <name>` |

### Nepodudaranje imena modela

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Postavite `AZURE_AI_MODEL_DEPLOYMENT_NAME` u `.env` na točan alias prikazan (npr. `phi-4-mini`, a ne `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` pri lokalnom pokretanju (Put B)

Labov `main.py` koristi `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local zahtijeva da ova varijabla pokazuje na lokalni servis - **ne** na `AZURE_AI_PROJECT_ENDPOINT`. Provjerite da vaš `.env` sadrži:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP alat ipak pravi odlazni poziv (Put B)

Ovo je očekivano. Alat `search_microsoft_learn_for_plan` dohvaća obrazovne resurse sa `https://learn.microsoft.com/api/mcp`. **Samo upit za ime vještine** putuje preko mreže - životopis i tekst JD-a obrađuju se u potpunosti na vašem uređaju i nikad se ne prenose. Ako je potrebni rad u potpunosti offline, dodajte u alat `try/except` rezervu koja vraća statični URL `learn.microsoft.com` kad endpoint nije dostupan.

---

## Dobivanje pomoći

Ako zapnete nakon pokušaja gore navedenih popravaka:

1. **Provjerite logove servera** - Većina pogrešaka proizvodi Python stog pogrešaka u terminalu. Pročitajte puni traceback.
2. **Pretražite poruku o pogrešci** - Kopirajte tekst pogreške i pretražite u [Microsoft Q&A za Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Otvorite issue** - Podnesite issue na [workshop repozitoriju](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) sa:
   - Porukom o pogrešci ili snimkom zaslona
   - Verzijama paketa (`pip list | Select-String "agent-framework"`)
   - Verzijom Pythona (`python --version`)
   - Je li problem lokalni ili nakon implementacije

---

### Kontrolna tačka

- [ ] Znate kako provjeriti i popraviti probleme konfiguracije `.env`
- [ ] Možete provjeriti podudaraju li se verzije paketa s potrebnom matricom
- [ ] Znate kako provjeriti logove kontejnera za neuspjele implementacije
- [ ] Možete provjeriti RBAC uloge u Azure portalu

---

**Prethodno:** [07 - Verify in Playground](07-verify-in-playground.md) · **Sljedeće:** [09 - Summary →](09-summary.md) · **Početna:** [Lab 02 README](../README.md) · [Početna radionice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->