# Modul 8 - Odpravljanje težav

Ta modul pokriva pogoste napake, popravke in strategije razhroščevanja, specifične za večagentni potek dela.

## Težave z izhodom agenta

### GapAnalyzer pravi "Še vedno nimam ujemajočega se poročila"

**Simptomi:** Odgovor GapAnalyzer vas prosi, da prilepite poročilo o ujemanju z "Manjkajočimi veščinami" in "Pomanjkljivostmi certifikatov." To se zgodi tudi, ko ste poslali bodisi življenjepis kot tudi opis delovnega mesta.

**Vzrok:** Besedilo JD ni bilo poslano naprej agentu JD. Pri `context_mode="last_agent"`, `resume_executor` je edini izvajalec, ki kdaj vidi izvirno uporabniško sporočilo. Če `RESUME_PARSER_INSTRUCTIONS` ne vključuje besedila JD v svojem izhodu, agent JD nima besedila JD za analizo, MatchingAgent ne more izračunati ocene ujemanja, GapAnalyzer pa prejme nepomemben vhod.

**Diagnoza:**

V strežniških dnevnikih poiščite prostor MatchingAgent. Če vsebuje:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
prenos je izpuščen ali pokvarjen.

**Popravek:** Potrdite, da `RESUME_PARSER_INSTRUCTIONS` v `main.py` vsebuje razdelek `[JOB DESCRIPTION PASS-THROUGH]` in pravilo:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Potrdite tudi, da `JOB_DESCRIPTION_INSTRUCTIONS` vsebuje prenosno pravilo `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Če je kateri koli blok navodil le izhodišče iz čarovnika za ogrodje, ga zamenjajte s popolno različico iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent izpiše "Ni mogoče izračunati ocene ujemanja - JD ni podan"

To je isti osnovni vzrok kot zgoraj. MatchingAgent je prejel izhod od agenta JD, a razdelek `[PARSED RESUME PASS-THROUGH]` je bil izpuščen ali prazen, zato ni mogel primerjati obeh profilov. Potrdite:
1. `JOB_DESCRIPTION_INSTRUCTIONS` vključuje prenosno pravilo: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` agenta usmeri k iskanju razdelkov `[JD REQUIREMENTS]` in `[PARSED RESUME PASS-THROUGH]`.

Zamenjajte oba bloka navodil s popolnimi različicami iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odgovor se prikaže dvakrat

**Simptomi:** Izhod GapAnalyzer (ali celoten izhod cevovoda) se v odzivu Agent Inspector prikaže dvakrat.

**Vzrok:** `WorkflowBuilder` uporablja OR-semantiko za vhodne povezave - naslednji izvajalec se sproži takoj, ko **kateri koli** predhodnik konča. Če ima `matching_executor` dve vhodni povezavi (ena iz `resume_executor` in ena iz `jd_executor`), se sproži dvakrat: enkrat, ko ResumeParser konča, in še enkrat, ko JD Agent konča. GapAnalyzer nato tudi teče dvakrat.

**Popravek:** Poskrbite, da je graf `WorkflowBuilder` strogo zaporedni cevovod brez navzkrižnih vhodov:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Če imate kakšno odvečno vrstico `.add_edge(resume_executor, matching_executor)`, jo odstranite. Prenos `[PARSED RESUME PASS-THROUGH]` v izhodu agenta JD že omogoča, da MatchingAgent dostopa do življenjepisa.

---

## Težave z okoljem in konfiguracijo

### Manjkajoče ali napačne vrednosti `.env`

Datoteka `.env` mora biti v imeniku `PersonalCareerCopilot/` (na isti ravni kot `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Pričakovana vsebina `.env`:

**Pot A - Foundry oblak:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Pot B - Foundry lokalno:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Obe poti uporabljata `FOUNDRY_PROJECT_ENDPOINT`. Vrednosti se razlikujejo: oblak uporablja končno točko Foundry z oznako `https://`; lokalno uporablja `http://localhost:5273/v1`. Za pot B za potrditev modelskega vzdevka zaženite `foundry model list`.

> **Iskanje vašega `FOUNDRY_PROJECT_ENDPOINT`:** 
- Odprite stransko vrstico **Foundry Toolkit** v VS Code → desni klik na vaš projekt → **Kopiraj končno točko projekta**. 
- Ali pojdite na [Azure Portal](https://portal.azure.com) → vaš Foundry projekt → **Pregled** → **Končna točka projekta**.

> **Iskanje vašega `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** V stranski vrstici Foundry Toolkit razširite projekt → **Modeli** → poiščite ime nameščenega modela (npr. `gpt-4.1-mini`).

### Prednost okoljske spremenljivke

`main.py` uporablja `load_dotenv(override=True)`, kar pomeni:

| Prednost | Vir | Zmaga, če sta oba nastavljena? |
|----------|--------|----------------------------|
| 1 (najvišja) | Datoteka `.env` | Da |
| 2 | Okolje lupine / vsebnik | Uporabi se, če istega ključa ni v `.env` |

V lokalnem razvoju to naredi `.env` vir resnice (urejanje `.env` takoj vpliva na zaganjanja). V gostovanem okolju Foundry polni okoljske spremenljivke na nivoju vsebnika; ker `.env` ni del nameščene slike za to delavnico, se uporabljajo vrednosti, vbrizgane v vsebnik.

---

## Združljivost različic

### Matrika različic paketov

Večagentni potek dela zahteva specifične različice paketov. Neujemanje različic povzroča napake med izvajanjem.

| Paket | Zahtevana različica | Ukaz za preverjanje |
|---------|-----------------|--------------------|
| `agent-framework-foundry` | najnovejša | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | najnovejša | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | najnovejša | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Pogoste napake različic

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

### Preverite vse različice naenkrat

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Pričakovan izhod:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Težave z namestitvijo

### Vsebnik se ne zažene po namestitvi

1. **Preverite dnevnike vsebnika:**
   - Odprite stransko vrstico **Foundry Toolkit** → pod vašim projektom kliknite **Agenti** → zavihek **Gostovani agent** → kliknite svojega agenta. Preverite **Status** na zavihku **Podrobnosti**, nato odprite zavihek **Igralnica** in uporabite zavihek **Dnevniki** v panelu **Podrobnosti seje** za ogled izhoda vsebnika.
   - Poiščite sledove v Pythonu ali napake pri manjkajočih modulih.

2. **Pogoste napake pri zagonu vsebnika:**

   | Napaka v dnevniku | Vzrok | Popravek |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` manjka paket | Dodajte paket, znova namestite |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Niso nastavljene okoljske spremenljivke `agent.yaml` ali `.env` | Posodobite `agent.yaml` → razdelek `environment_variables` (gostovano) ali `.env` (lokalno) |
   | `azure.identity.CredentialUnavailableError` | Upravljana identiteta ni konfigurirana | Foundry to nastavi samodejno - poskrbite, da nameščate preko razširitve |
   | `OSError: port 8088 already in use` | Dockerfile razkriva napačen priključek ali konflikt priključkov | Preverite `EXPOSE 8088` v Dockerfile in `CMD ["python", "main.py"]` |
   | Vsebnik se zapre z izhodno kodo 1 | Neobdelana izjema v `main()` | Najprej preizkusite lokalno ([Modul 5](05-test-locally.md)) za odkrivanje napak pred nameščanjem |

3. **Ponovna namestitev po popravku:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Namesti gostovanega agenta** → izberite istega agenta → namestite novo različico.

### Namestitev traja predolgo

Večagentni vsebniki potrebujejo več časa za začetek, ker ob zagonu ustvarijo 4 primerke agentov. Običajni časi zagona:

| Faza | Pričakovan čas |
|-------|-----------------|
| Izgradnja slike vsebnika | 1-3 minute |
| Potisk slike v ACR | 30-60 sekund |
| Zagon vsebnika (en agent) | 15-30 sekund |
| Zagon vsebnika (več agentov) | 30-120 sekund |
| Agent na voljo v igralnici | 1-2 minuti po "Začetku" |

> Če status "Čakajoče" traja več kot 5 minut, preverite dnevnike vsebnika zaradi napak.

---

## Težave z RBAC in dovoljenji

### `403 Forbidden` ali `AuthorizationFailed`

Potrebujete vlogo **[Foundry User](https://aka.ms/foundry-ext-project-role)** na vašem Foundry projektu (prej imenovano **Azure AI User** - ID vloge nespremenjen):

1. Pojdite na [Azure Portal](https://portal.azure.com) → vir vašega Foundry **projekta**.
2. Kliknite **Upravljanje dostopa (IAM)** → **Dodelitve vlog**.
3. Poiščite svoje ime → potrdite, da je navedena **Foundry User** (ali staro ime **Azure AI User**).
4. Če manjka: **Dodaj** → **Dodaj dodelitev vloge** → poiščite **Foundry User** → dodelite svojemu računu.

Za podrobnosti preberite dokumentacijo [RBAC za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Model ni dostopen po namestitvi

Če agent vrne napake, povezane z modelom:

1. Preverite, ali je model nameščen: v stranski vrstici Foundry razširite projekt → **Modeli** → preverite za `gpt-4.1-mini` (ali vaš model) s statusom **Uspešno**.
2. Preverite, ali se ime namestitve ujema: primerjajte `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` (ali `agent.yaml`) s pravim imenom namestitve v stranski vrstici.
3. Če je namestitev potekla (brezplačni razred): ponovno namestite iz [Kataloga modelov](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Odpri Katalog modelov**).

---

## Težave z Foundry Local (Pot B)

### Storitev Foundry Local ne deluje

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Simptomi | Vzrok | Popravek |
|---------|-------|-----|
| Preverjanje stanja vrne `503` | Storitev ni zagnana | `foundry local start` ali kliknite **Začni** v stranski vrstici Foundry Toolkit |
| Preverjanje stanja poteče | Model se še nalaga | Počakajte 30–60 s po zagonu; večji modeli potrebujejo dlje |
| `StatusCode: 404` na `/v1/health` | Napačen priključek | Privzeto je `5273`. Preverite `foundry local status` za resnični priključek |
| Premalo virov | Foundry Local potrebuje ~4 GB RAM-a prostega | Zaprite druge aplikacije |
| Ne uspe prenos modela | Premalo prostora na disku | Modeli so veliki 2–8 GB. Očistite prostor in nato `foundry model pull <name>` |

### Neujemajoče se ime modela

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Nastavite `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` na točen vzdevek, prikazan (npr. `phi-4-mini`, ne `Phi-4-mini`).

### Napaka `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` pri lokalnem zagonu (Pot B)

Laboratorijski `main.py` uporablja `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local zahteva, da ta spremenljivka kaže na lokalno storitev - **ne** na `AZURE_AI_PROJECT_ENDPOINT`. Poskrbite, da vaš `.env` vsebuje:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Orodje MCP še vedno vzpostavlja odhodni klic (Pot B)

To je pričakovano. Orodje `search_microsoft_learn_for_plan` pridobiva učne vire iz `https://learn.microsoft.com/api/mcp`. **Le poizvedba po imenu veščine** potuje po omrežju - življenjepis in besedilo JD se obdelujeta popolnoma na vaši napravi in nikoli nista prenesena. Če je potreben popoln brez povezave način delovanja, dodajte v orodje rezervno možnost `try/except`, ki vrne statični URL `learn.microsoft.com`, kadar konekcija ni dosegljiva.

---

## Iskanje pomoči

Če po poskusu zgornjih popravkov obstanete:

1. **Preverite strežniške dnevnike** - Večina napak proizvede sledi Python v terminalu. Preberite celoten sled.
2. **Poiščite sporočilo o napaki** - Kopirajte besedilo napake in poiščite v [Microsoft Q&A za storitev Foundry Agent](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Odprite zadevo** - Pošljite zadevo v [delavnico na repozitoriju](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) z:
   - sporočilom o napaki ali zaslonsko sliko
   - vašimi različicami paketov (`pip list | Select-String "agent-framework"`)
   - vašo različico Pythona (`python --version`)
   - ali je težava lokalna ali po namestitvi

---

### Kontrolna točka

- [ ] Znate preveriti in popraviti težave s konfiguracijo `.env`
- [ ] Lahko preverite, ali se različice paketov ujemajo z zahtevano matriko
- [ ] Znate preveriti dnevnike vsebnika za napake pri namestitvi
- [ ] Znate preveriti RBAC vloge v Azure Portalu

---

**Prejšnji:** [07 - Preveri v igralnici](07-verify-in-playground.md) · **Naslednji:** [09 - Povzetek →](09-summary.md) · **Domov:** [Lab 02 README](../README.md) · [Domača stran delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->