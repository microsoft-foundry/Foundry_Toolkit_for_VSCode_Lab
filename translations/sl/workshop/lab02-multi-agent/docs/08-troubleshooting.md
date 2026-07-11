# Modul 8 - Odpravljanje težav

Ta modul obravnava pogoste napake, popravke in strategije odpravljanja napak, specifične za delovni tok z več agenti.

## Težave z izhodom agenta

### GapAnalyzer pravi “Še vedno nimam ustreznega poročila”

**Simptom:** Odziv GapAnalyzerja vas prosi, da prilepite ustrezno poročilo z “Manjkajočimi znanji” in “Pomanjkljivostmi certifikatov.” To se zgodi tudi, če ste poslali tako življenjepis kot opis delovnega mesta.

**Vzrok:** Besedilo JD ni bilo posredovano naprej do JD agent. Pri `context_mode="last_agent"` `resume_executor` je edini izvajalec, ki vidi izvirno uporabnikovo sporočilo. Če `RESUME_PARSER_INSTRUCTIONS` ne vključuje besedila JD v svojem izhodu, JD Agent nima JD za analizo, MatchingAgent ne more izračunati ocene ustreznosti, GapAnalyzer pa prejme nesmiselni vhod.

**Diagnoza:**

V strežniških dnevnikih poiščite časovni razpon MatchingAgent. Če vsebuje:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
prehod ni prisoten ali je poškodovan.

**Popravek:** Preverite, da `RESUME_PARSER_INSTRUCTIONS` v `main.py` vsebuje razdelek `[JOB DESCRIPTION PASS-THROUGH]` in pravilo:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Prav tako potrdite, da `JOB_DESCRIPTION_INSTRUCTIONS` vsebuje relay pravilo `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Če je kateri od teh blokov navodil začasni iz čarovnika, ga zamenjajte z dokončno različico iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent vrne “Ne more izračunati ocene ustreznosti - JD ni podan”

To je enak osnovni vzrok kot prej. MatchingAgent je prejel izhod JD Agenta, vendar je razdelek `[PARSED RESUME PASS-THROUGH]` manjkajoč ali prazen, zato ni mogel primerjati dveh profilov. Potrdite:
1. `JOB_DESCRIPTION_INSTRUCTIONS` vključuje relay pravilo: `Kopiraj [PARSED RESUME] dobesedno - Matching Agent to potrebuje naprej.`
2. `MATCHING_AGENT_INSTRUCTIONS` agentu naroča, naj išče razdelke `[JD REQUIREMENTS]` in `[PARSED RESUME PASS-THROUGH]`.

Zamenjajte oba bloka navodil s popolnimi različicami iz [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odziv se pojavi dvakrat

**Simptom:** Izpis GapAnalyzerja (ali celoten izpis cevovoda) se v odzivu Agent Inspectorja pojavi dvakrat.

**Vzrok:** `WorkflowBuilder` uporablja OR-semantiko za dohodne povezave – izvajalec spodaj sproži takoj, ko **katerikoli** predhodnik zaključi. Če ima `matching_executor` dve vhoda (enega od `resume_executor` in enega od `jd_executor`), se sproži dvakrat: enkrat, ko ResumeParser konča, in drugič, ko JD Agent konča. Nato se GapAnalyzer prav tako izvaja dvakrat.

**Popravek:** Zagotovite, da je graf `WorkflowBuilder` strogo zaporedni cevovod brez fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NI iz resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Če imate odvečno vrstico `.add_edge(resume_executor, matching_executor)`, jo odstranite. Relay `[PARSED RESUME PASS-THROUGH]` v izhodu JD Agenta že daje MatchingAgentu dostop do življenjepisa.

---

## Težave z okoljem in konfiguracijo

### Manjkajoče ali napačne vrednosti v `.env`

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

**Pot A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Pot B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Obe poti uporabljata `FOUNDRY_PROJECT_ENDPOINT`. Vrednost se razlikuje: oblak uporablja naslov z `https://`; lokalni način uporablja `http://localhost:5273/v1`. Za potrditev natančnega vzdevka modela za Pot B poženite `foundry model list`.

> **Iskanje vašega `FOUNDRY_PROJECT_ENDPOINT`:** 
- Odprite stranski meni **Foundry Toolkit** v VS Code → z desno tipko kliknite vaš projekt → **Copy Project Endpoint**. 
- Ali pojdite na [Azure Portal](https://portal.azure.com) → vaš Foundry projekt → **Pregled** → **Projektni konektor**.

> **Iskanje vašega `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** V stranskem meniju Foundry Toolkit razširite vaš projekt → **Modeli** → poiščite ime nameščenega modela (npr. `gpt-4.1-mini`).

### Prednost okolijskih spremenljivk

`main.py` uporablja `load_dotenv(override=True)`, kar pomeni:

| Prioriteta | Vir | Zmaga, če sta oba nastavljena? |
|----------|--------|----------------------------|
| 1 (najvišja) | `.env` datoteka | Da |
| 2 | Shell / okoljska spremenljivka kontejnerja | Uporabi, če ključ ni v `.env` |

Pri lokalnem razvoju to pomeni, da je `.env` vir resnice (urejanje `.env` takoj vpliva na zagon). Pri gostovanem uvajanju Foundry vstavi okoljske spremenljivke na ravni kontejnerja; ker `.env` ni del slike, ki se uvaja v tej nastavitvi laboratorija, se uporabljajo vrednosti kontejnerja.

---

## Združljivost različic

### Matrika različic paketov

Delovni tok z več agenti zahteva specifične različice paketov. Neujemanje različic povzroči napake med izvajanjem.

| Paket | Zahtevana različica | Ukaz za preverjanje |
|---------|-----------------|------------------|
| `agent-framework-foundry` | najnovejša | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | najnovejša | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | najnovejša | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Pogoste napake zaradi različic

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Popravek: znova namestite agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Popravek: nadgradnja paketa mcp
pip install mcp --upgrade
```

### Preverite vse različice hkrati

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Pričakovan izpis:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Težave pri uvajanju

### Kontejner ne uspe zagnati po uvajanju

1. **Preverite dnevnike kontejnerja:**
   - Odprite stransko vrstico **Foundry Toolkit** → razširite **Hosted Agents (Preview)** → kliknite vašega agenta → razširite različico → **Podrobnosti kontejnerja** → **Dnevniki**.
   - Poiščite sledove napak iz Python ali manjkajočih modulov.

2. **Pogoste napake zagona kontejnerja:**

   | Napaka v dnevnikih | Vzrok | Popravek |
   |--------------------|-------|---------|
   | `ModuleNotFoundError` | V `requirements.txt` manjka paket | Dodajte paket, ponovno uvedite |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Okoljske spremenljivke v `agent.yaml` ali `.env` niso nastavljene | Posodobite razdelek `environment_variables` v `agent.yaml` (gostovani) ali `.env` (lokalni) |
   | `azure.identity.CredentialUnavailableError` | Upravljana identiteta ni konfigurirana | Foundry to nastavi samodejno - zagotovite uvajanje preko razširitve |
   | `OSError: port 8088 already in use` | Dockerfile razkriva napačen port ali je konflikt portov | Preverite `EXPOSE 8088` v Dockerfile in `CMD ["python", "main.py"]` |
   | Kontejner se zapre s kodo 1 | Neobdelana izjema v `main()` | Najprej testirajte lokalno ([Modul 5](05-test-locally.md)) za odkrivanje napak pred uvajanjem |

3. **Ponovno uvedite po popravku:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → izberite istega agenta → uvedite novo različico.

### Uvajanje traja predolgo

Kontejnerji z več agenti potrebujejo več časa za zagon, ker ob zagonu ustvarijo 4 primere agenta. Normalni časi zagona:

| Stopnja | Pričakovano trajanje |
|--------|--------------------|
| Gradnja slike kontejnerja | 1-3 minute |
| Potisk slike v ACR | 30-60 sekund |
| Zagon kontejnerja (en agent) | 15-30 sekund |
| Zagon kontejnerja (več agentov) | 30-120 sekund |
| Agent na voljo v Playgroundu | 1-2 minuti po “Started” |

> Če status "Pending" traja več kot 5 minut, preverite dnevnike kontejnerja za napake.

---

## Težave z RBAC in dovoljenji

### `403 Forbidden` ali `AuthorizationFailed`

Potrebujete vlogo **[Foundry User](https://aka.ms/foundry-ext-project-role)** v vašem Foundry projektu (prej je bila poimenovana **Azure AI User** - ID vloge se ni spremenil):

1. Pojdite na [Azure Portal](https://portal.azure.com) → vaša Foundry **projekt**.
2. Kliknite **Nadzor dostopa (IAM)** → **Dodelitve vlog**.
3. Poiščite svoje ime → potrdite, da je navedena vloga **Foundry User** (ali stara oznaka **Azure AI User**).
4. Če manjka: **Dodaj** → **Dodaj dodelitev vloge** → poiščite **Foundry User** → dodelite račun.

Za podrobnosti glejte dokumentacijo o [RBAC za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Model ni dostopen po uvajanju

Če agent vrne napake povezane z modelom:

1. Preverite, da je model nameščen: v stranski vrstici Foundry razširite projekt → **Modeli** → preverite `gpt-4.1-mini` (ali vaš model) s statusom **Succeeded**.
2. Preverite, da ime uvajanja ustreza: primerjajte `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` (ali `agent.yaml`) z dejanskim imenom uvajanja v stranski vrstici.
3. Če je uvajanje poteklo (brezplačna stopnja): ponovno uvedite iz [Kataloga modelov](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Težave s Foundry Local (Pot B)

### Storitev Foundry Local ne teče

```powershell
# Preveri stanje
foundry local status

# Zaženi storitev, če je ustavljena
foundry local start
```

| Simptom | Vzrok | Popravek |
|--------|-------|---------|
| Preverjanje stanja vrne `503` | Storitev ni zagnana | Zaženite `foundry local start` ali kliknite **Start** v stranski vrstici Foundry Toolkit |
| Preverjanje stanja se izteče | Model se še nalaga | Počakajte 30–60 s po zagonu; večji modeli potrebujejo več časa |
| `StatusCode: 404` na `/v1/health` | Napačen port | Privzeti je `5273`. Preverite `foundry local status` za dejanski port |
| Premalo virov | Foundry Local potrebuje ~4 GB prostega RAM-a | Zaprite druge aplikacije |
| Prenos modela ne uspe | Premalo prostora na disku | Modeli so veliki 2–8 GB. Očistite prostor, nato `foundry model pull <ime>` |

### Neujemanje imena modela

```powershell
# Naštej prenesene modele in njihove natančne vzdevke
foundry model list
```

Nastavite `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `.env` na natanko prikazan vzdevek (npr. `phi-4-mini`, ne `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ob lokalnem zagonu (Pot B)

Laboratorijski `main.py` uporablja `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local zahteva, da ta spremenljivka kaže na lokalno storitev - **ne** na `AZURE_AI_PROJECT_ENDPOINT`. Prepričajte se, da vaša `.env` vsebuje:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Orodje MCP še vedno pošilja zahtevo zunaj (Pot B)

To je pričakovano. Orodje `search_microsoft_learn_for_plan` pridobiva učne vire iz `https://learn.microsoft.com/api/mcp`. **Samo poizvedba za ime veščine** potuje prek omrežja - življenjepis in besedilo JD se obdelujeta v celoti na vaši napravi in nista nikoli poslani. Če je potreben popolnoma brez povezave delovanje, dodajte v orodje `try/except` rezervno možnost, ki vrne statični URL `learn.microsoft.com`, ko je končna točka nedosegljiva.

---

## Iskanje pomoči

Če ste obtičali po preizkusu zgornjih popravkov:

1. **Preverite strežniške dnevnike** - Večina napak ustvari sled izvajanja Python v terminalu. Preberite celotno sled.
2. **Iskanje napake** - Kopirajte besedilo napake in ga poiščite na [Microsoft Q&A za Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Odprite težavo** - Oddajte težavo v [dokumentaciji delavnice](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) z:
   - Sporočilom o napaki ali posnetkom zaslona
   - Verzijo vaših paketov (`pip list | Select-String "agent-framework"`)
   - Verzijo Pythona (`python --version`)
   - Ali je težava lokalna ali po uvajanju

---

### Preverjanje znanja

- [ ] Znate preveriti in popraviti težave s `.env` konfiguracijo
- [ ] Znate preveriti, ali različice paketov ustrezajo zahtevani matriki
- [ ] Znate preveriti dnevnike kontejnerja za napake pri uvajanju
- [ ] Znate preveriti RBAC vloge v Azure Portalu

---

**Prejšnji:** [07 - Verify in Playground](07-verify-in-playground.md) · **Naslednji:** [09 - Povzetek →](09-summary.md) · **Domov:** [Lab 02 README](../README.md) · [Domov delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->