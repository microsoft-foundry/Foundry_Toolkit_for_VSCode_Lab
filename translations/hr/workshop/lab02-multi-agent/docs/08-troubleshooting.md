# Modul 8 - Rješavanje problema

Ovaj modul pokriva uobičajene pogreške, popravke i strategije otklanjanja pogrešaka specifične za višestruki agentni radni tijek.

## Problemi s izlazom agenata

### GapAnalyzer kaže "Još uvijek nemam odgovarajući izvještaj"

**Simptom:** Odgovor GapAnalyzera traži da zalijepite izvještaj podudaranja s "Nedostajućim vještinama" i "Prazninama u certifikaciji." Ovo se događa čak i kada ste poslali i životopis i opis posla.

**Uzrok:** Tekst JD nije prenesen dalje JD agentu. S `context_mode="last_agent"`, `resume_executor` je jedini izvršitelj koji vidi izvornu poruku korisnika. Ako `RESUME_PARSER_INSTRUCTIONS` ne uključuju tekst JD u svoj izlaz, JD Agent nema JD za parsiranje, MatchingAgent ne može izračunati ocjenu podudarnosti, a GapAnalyzer prima nevažljiv unos.

**Dijagnoza:**

U zapisnicima poslužitelja potražite MatchingAgent span. Ako sadrži:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
prosljeđivanje nedostaje ili je pokvareno.

**Popravak:** Potvrdite da `RESUME_PARSER_INSTRUCTIONS` u `main.py` sadrži odjeljak `[JOB DESCRIPTION PASS-THROUGH]` i pravilo:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Također potvrdite da `JOB_DESCRIPTION_INSTRUCTIONS` sadrži pravilo prosljeđivanja `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Ako je bilo koji od blokova uputa privremeni iz čarobnjaka, zamijenite ga potpunom verzijom iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent daje izlaz "Ne mogu izračunati ocjenu podudarnosti - nije dostavljen JD"

Ovo je isti osnovni uzrok kao gore. MatchingAgent je primio izlaz JD agenta, ali odjeljak `[PARSED RESUME PASS-THROUGH]` je nedostajao ili je prazan, pa nije mogao usporediti dva profila. Potvrdite:
1. `JOB_DESCRIPTION_INSTRUCTIONS` uključuje pravilo prosljeđivanja: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` instruira agenta da traži odjeljke `[JD REQUIREMENTS]` i `[PARSED RESUME PASS-THROUGH]`.

Zamijenite oba bloka uputa potpunim verzijama iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odgovor se pojavljuje dva puta

**Simptom:** Izlaz GapAnalyzera (ili cijeli izlaz cjevovoda) pojavljuje se dvaput u odgovoru Agent Inspectora.

**Uzrok:** `WorkflowBuilder` koristi OR-semantiku za dolazne veze - izvršitelj nizvodno se aktivira čim bilo koji prethodnik završi. Ako `matching_executor` ima dvije dolazne veze (jednu od `resume_executor` i jednu od `jd_executor`), aktivira se dvaput: jednom kad ResumeParser završi i ponovo kad JD Agent završi. I GapAnalyzer tada radi dvaput.

**Popravak:** Osigurajte da je graf `WorkflowBuilder` strogo sekvencijalni cjevovod bez višestrukog ulaza:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NI iz resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Ako imate slučajnu liniju `.add_edge(resume_executor, matching_executor)`, uklonite je. Relay `[PARSED RESUME PASS-THROUGH]` u izlazu JD agenta već daje MatchingAgentu pristup životopisu.

---

## Problemi s okolinom i konfiguracijom

### Nedostajuće ili pogrešne vrijednosti u `.env`

`.env` datoteka mora biti u direktoriju `PersonalCareerCopilot/` (na istoj razini kao `main.py`):

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

**Put B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Oba puta koriste `FOUNDRY_PROJECT_ENDPOINT`. Vrijednost je različita: cloud koristi `https://` Foundry endpoint; lokalni koristi `http://localhost:5273/v1`. Pokrenite `foundry model list` za potvrdu točnog imena modela za Put B.

> **Kako pronaći svoj `FOUNDRY_PROJECT_ENDPOINT`:** 
- Otvorite **Foundry Toolkit** bočnu traku u VS Code → desni klik na svoj projekt → **Copy Project Endpoint**. 
- Ili idite na [Azure Portal](https://portal.azure.com) → svoj Foundry projekt → **Overview** → **Project endpoint**.

> **Kako pronaći svoj `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** U Foundry Toolkit bočnoj traci proširite projekt → **Models** → pronađite ime svog modela (npr. `gpt-4.1-mini`).

### Prioritet varijabli okoline

`main.py` koristi `load_dotenv(override=True)`, što znači:

| Prioritet | Izvor | Pobjednik kad su oba postavljena? |
|----------|--------|------------------------------|
| 1 (najviši) | `.env` datoteka | Da |
| 2 | Shell / varijabla okoline kontejnera | Koristi se ako isti ključ nije prisutan u `.env` |

U lokalnom razvoju `.env` je izvor istine (uređivanje `.env` odmah utječe na pokretanja). U hostiranoj implementaciji Foundry ubrizgava varijable okoline na razini kontejnera; budući da `.env` nije dio implementirane slike za ovu lab postavku, koriste se ubrizgani kontejnerski vrijednosti.

---

## Kompatibilnost verzija

### Matrica verzija paketa

Višestruki agentni radni tijek zahtijeva specifične verzije paketa. Nepodudarne verzije uzrokuju pogreške tijekom izvođenja.

| Paket | Zahtijevana verzija | Naredba za provjeru |
|-------|-------------------|--------------------|
| `agent-framework-foundry` | najnovija | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | najnovija | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | najnovija | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Uobičajene pogreške verzija

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Popravi: ponovno instaliraj agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Popravi: nadogradnja mcp paketa
pip install mcp --upgrade
```

### Provjerite sve verzije odjednom

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

### Kontejner ne može startati nakon implementacije

1. **Provjerite zapisnike kontejnera:**
   - Otvorite **Foundry Toolkit** bočnu traku → proširite **Hosted Agents (Preview)** → kliknite na svog agenta → proširite verziju → **Container Details** → **Logs**.
   - Potražite Python stogove pogrešaka ili pogreške o nedostajućim modulima.

2. **Uobičajeni uzroci neuspjeha pokretanja kontejnera:**

   | Pogreška u zapisima | Uzrok | Popravak |
   |---------------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` nedostaje paket | Dodajte paket, ponovo implementirajte |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | varijable okoline u `agent.yaml` ili `.env` nisu postavljene | Ažurirajte `agent.yaml` → odjeljak `environment_variables` (hostirano) ili `.env` (lokalno) |
   | `azure.identity.CredentialUnavailableError` | Upravljački identitet nije konfiguriran | Foundry to postavlja automatski - osigurajte da implementirate preko proširenja |
   | `OSError: port 8088 already in use` | Dockerfile izlaže pogrešan port ili sukob portova | Provjerite `EXPOSE 8088` u Dockerfile i `CMD ["python", "main.py"]` |
   | Kontejner izlazi s kodom 1 | Neuhvaćena iznimka u `main()` | Najprije testirajte lokalno ([Modul 5](05-test-locally.md)) da uhvatite pogreške prije implementacije |

3. **Ponovno implementirajte nakon popravljanja:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → odaberite istog agenta → implementirajte novu verziju.

### Implementacija traje predugo

Kontejneri za višestruke agente duže se pokreću jer prilikom starta kreiraju 4 instance agenta. Normalna trajanja pokretanja:

| Faza | Očekivano trajanje |
|------|--------------------|
| Izgradnja slike kontejnera | 1-3 minute |
| Slanje slike na ACR | 30-60 sekundi |
| Pokretanje kontejnera (jedan agent) | 15-30 sekundi |
| Pokretanje kontejnera (više agenata) | 30-120 sekundi |
| Agent dostupan u Playgroundu | 1-2 minute nakon "Started" statusa |

> Ako status "Pending" traje dulje od 5 minuta, provjerite zapisnike kontejnera zbog pogrešaka.

---

## RBAC i problemi s dopuštenjima

### `403 Forbidden` ili `AuthorizationFailed`

Potreban vam je **[Foundry User](https://aka.ms/foundry-ext-project-role)** uloga na vašem Foundry projektu (prije nazvana **Azure AI User** - ID uloge nepromijenjen):

1. Idite na [Azure Portal](https://portal.azure.com) → resurs svog Foundry **projekta**.
2. Kliknite **Access control (IAM)** → **Role assignments**.
3. Pretražite svoje ime → potvrdite da je navedena uloga **Foundry User** (ili stari naziv **Azure AI User**).
4. Ako nema: **Dodaj** → **Add role assignment** → potraži **Foundry User** → dodijeli svom računu.

Pogledajte dokumentaciju [RBAC za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) za detalje.

### Implementacija modela nije dostupna

Ako agent vraća pogreške vezane za model:

1. Provjerite je li model implementiran: Foundry bočna traka → proširite projekt → **Models** → provjerite ima li `gpt-4.1-mini` (ili vaš model) sa statusom **Succeeded**.
2. Provjerite da se ime implementacije podudara: usporedite `AZURE_AI_MODEL_DEPLOYMENT_NAME` u `.env` (ili `agent.yaml`) s stvarnim imenom implementacije u bočnoj traci.
3. Ako je implementacija istekla (besplatni sloj): ponovno implementirajte iz [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemi s Foundry Local (Put B)

### Foundry Local servis nije pokrenut

```powershell
# Provjeri status
foundry local status

# Pokreni uslugu ako je zaustavljena
foundry local start
```

| Simptom | Uzrok | Popravak |
|---------|-------|---------|
| Health check vraća `503` | Servis nije pokrenut | `foundry local start` ili kliknite **Start** u Foundry Toolkit bočnoj traci |
| Health check se tajmautira | Model se još učitava | Pričekajte 30–60 s nakon pokretanja; veći modeli traju dulje |
| `StatusCode: 404` na `/v1/health` | Pogrešan port | Zadano je `5273`. Provjerite `foundry local status` za stvarni port |
| Nedovoljno resursa | Foundry Local treba ~4 GB slobodne RAM memorije | Zatvorite druge aplikacije |
| Neuspjeh preuzimanja modela | Malo prostora na disku | Modeli zauzimaju 2–8 GB. Oslobodite prostor, potom `foundry model pull <name>` |

### Nepodudaranje imena modela

```powershell
# Popis preuzetih modela i njihovih točnih aliasa
foundry model list
```

Postavite `AZURE_AI_MODEL_DEPLOYMENT_NAME` u `.env` na točan alias prikazan (npr. `phi-4-mini`, ne `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` pri lokalnom pokretanju (Put B)

Lab `main.py` koristi `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local zahtijeva da ova varijabla pokazuje na lokalni servis - **ne** na `AZURE_AI_PROJECT_ENDPOINT`. Osigurajte da vaša `.env` sadrži:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP alat i dalje vrši odlazni poziv (Put B)

Ovo se očekuje. Alat `search_microsoft_learn_for_plan` dohvaća obrazovne resurse s `https://learn.microsoft.com/api/mcp`. **Samo upit za ime vještine** putuje mrežom - životopis i tekst JD obrađuju se u potpunosti na vašem uređaju i nikada se ne prenose. Ako je potrebna potpuna offline operacija, dodajte u alat `try/except` za vraćanje statičke `learn.microsoft.com` URL adrese kad je endpoint nedostupan.

---

## Dobivanje pomoći

Ako zapnete nakon pokušaja gore navedenih popravaka:

1. **Provjerite zapisnike poslužitelja** - Većina pogrešaka ispisuje Python stog u terminalu. Pročitajte cijeli traceback.
2. **Potražite poruku pogreške** - Kopirajte tekst pogreške i pretražite u [Microsoft Q&A za Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Otvorite issue** - Podnesite prijavu na [radnom spremištu radionice](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) s:
   - Tekstom pogreške ili screenshotom
   - Verzijama paketa (`pip list | Select-String "agent-framework"`)
   - Vašom verzijom Pythona (`python --version`)
   - Je li problem lokalni ili nakon implementacije

---

### Kontrolna točka

- [ ] Znate kako provjeriti i popraviti probleme s konfiguracijom `.env`
- [ ] Možete potvrditi odgovaraju li verzije paketa potrebnoj matrici
- [ ] Znate kako provjeriti zapisnike kontejnera za neuspjehe implementacije
- [ ] Možete provjeriti RBAC uloge u Azure portalu

---

**Prethodno:** [07 - Provjera u Playgroundu](07-verify-in-playground.md) · **Sljedeće:** [09 - Sažetak →](09-summary.md) · **Početna:** [Lab 02 README](../README.md) · [Početna radionice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->