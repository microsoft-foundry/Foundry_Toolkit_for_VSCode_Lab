# Modulul 8 - Depanare

Acest modul acoperă erorile comune, remedierile și strategiile de depanare specifice fluxului de lucru cu mai mulți agenți.

## Probleme cu ieșirea agentului

### GapAnalyzer spune „Încă nu am raportul corespunzător”

**Simptom:** Răspunsul GapAnalyzer vă cere să lipiți un raport corespunzător cu „Competențe lipsă” și „Lacune de certificare”. Acest lucru se întâmplă chiar și atunci când ați trimis atât un CV, cât și o descriere a postului.

**Cauză:** Textul JD nu a fost transmis mai departe către agentul JD. Cu `context_mode="last_agent"`, `resume_executor` este singurul executant care vede mesajul original al utilizatorului. Dacă `RESUME_PARSER_INSTRUCTIONS` nu include textul JD în ieșirea sa, agentul JD nu are niciun JD de analizat, MatchingAgent nu poate calcula un scor de potrivire, iar GapAnalyzer primește o intrare lipsită de sens.

**Diagnostic:**

În jurnalele serverului, căutați spanul MatchingAgent. Dacă conține:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
transmiterea este lipsă sau întreruptă.

**Remediere:** Confirmați că `RESUME_PARSER_INSTRUCTIONS` din `main.py` conține o secțiune `[JOB DESCRIPTION PASS-THROUGH]` și regula:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
De asemenea, confirmați că `JOB_DESCRIPTION_INSTRUCTIONS` conține o regulă de retransmisie `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Dacă oricare bloc de instrucțiuni este un șablon din vrăjitorul scheletului, înlocuiți-l cu versiunea completă din [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent afișează „Cannot compute fit score - no JD provided”

Aceasta este aceeași cauză principală ca mai sus. MatchingAgent a primit ieșirea agentului JD, dar secțiunea `[PARSED RESUME PASS-THROUGH]` lipsea sau era goală, deci nu a putut compara cele două profiluri. Confirmați:
1. `JOB_DESCRIPTION_INSTRUCTIONS` include regula de retransmisie: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` spune agentului să caute secțiunile `[JD REQUIREMENTS]` și `[PARSED RESUME PASS-THROUGH]`.

Înlocuiți ambele blocuri de instrucțiuni cu versiunile complete din [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Răspunsul apare de două ori

**Simptom:** Ieșirea GapAnalyzer (sau întreaga ieșire a pipeline-ului) apare de două ori în răspunsul Inspectorului de Agenti.

**Cauză:** `WorkflowBuilder` folosește semantica OR pentru muchiile de intrare - un executant downstream se declanșează imediat ce **oricare** predecesor se termină. Dacă `matching_executor` are două muchii de intrare (una de la `resume_executor` și una de la `jd_executor`), se declanșează de două ori: o dată când ResumeParser se termină și încă o dată când agentul JD termină. GapAnalyzer rulează apoi și el de două ori.

**Remediere:** Asigurați-vă că graficul `WorkflowBuilder` este un pipeline strict secvențial fără fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NU din resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Dacă aveți o linie în plus `.add_edge(resume_executor, matching_executor)`, o eliminați. Retransmisia `[PARSED RESUME PASS-THROUGH]` din ieșirea agentului JD îi oferă deja MatchingAgent acces la CV.

---

## Probleme de mediu și configurare

### Valori `.env` lipsă sau greșite

Fișierul `.env` trebuie să fie în directorul `PersonalCareerCopilot/` (același nivel cu `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Conținutul așteptat pentru `.env`:

**Calea A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Calea B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Ambele căi folosesc `FOUNDRY_PROJECT_ENDPOINT`. Valoarea diferă: cloud folosește un endpoint Foundry `https://`; local folosește `http://localhost:5273/v1`. Rulați `foundry model list` pentru a confirma aliasul exact al modelului pentru Calea B.

> **Cum găsiți `FOUNDRY_PROJECT_ENDPOINT`:** 
- Deschideți bara laterală **Foundry Toolkit** în VS Code → click dreapta pe proiectul dvs → **Copy Project Endpoint**. 
- Sau mergeți la [Azure Portal](https://portal.azure.com) → proiectul dvs Foundry → **Overview** → **Project endpoint**.

> **Cum găsiți `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** În bara laterală Foundry Toolkit, extindeți proiectul → **Models** → găsiți numele modelului implementat (ex: `gpt-4.1-mini`).

### Prioritatea variabilelor de mediu

`main.py` folosește `load_dotenv(override=True)`, ceea ce înseamnă:

| Prioritate | Sursă | Câștigă când ambele sunt setate? |
|----------|--------|------------------------------|
| 1 (cea mai înaltă) | fișier `.env` | Da |
| 2 | variabilă mediu Shell/container | Folosită când cheia respectivă nu este prezentă în `.env` |

În dezvoltarea locală, aceasta face din `.env` sursa de adevăr (editarea `.env` afectează imediat rulările). În implementarea găzduită, Foundry injectează variabilele de mediu la nivelul containerului; deoarece `.env` nu face parte din imaginea implementată pentru această configurație, valorile injectate ale containerului sunt folosite.

---

## Compatibilitatea versiunilor

### Matricea versiunilor pachetelor

Fluxul de lucru multi-agent necesită versiuni specifice de pachete. Versiunile nepotrivite provoacă erori la rulare.

| Pachet | Versiune necesară | Comandă de verificare |
|---------|-----------------|----------------------|
| `agent-framework-foundry` | cea mai recentă | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | cea mai recentă | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | cea mai recentă | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Erori comune de versiune

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Remediere: reinstalați agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Remediere: actualizează pachetul mcp
pip install mcp --upgrade
```

### Verifică toate versiunile odată

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Ieșire așteptată:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Probleme de implementare

### Containerul nu pornește după implementare

1. **Verificați jurnalele containerului:**
   - Deschideți bara laterală **Foundry Toolkit** → extindeți **Hosted Agents (Preview)** → click pe agentul dvs → extindeți versiunea → **Container Details** → **Logs**.
   - Căutați trace-uri Python sau erori de module lipsă.

2. **Eșecuri comune la pornirea containerului:**

   | Eroare în jurnale | Cauză | Remediere |
   |-------------------|-------|----------|
   | `ModuleNotFoundError` | `requirements.txt` lipsă pachet | Adăugați pachetul, reimplementați |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | variabile de mediu în `agent.yaml` sau `.env` neconfigurate | Actualizați secțiunea `environment_variables` din `agent.yaml` (hosted) sau `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Identitate gestionată neconfigurată | Foundry o setează automat - asigurați-vă că implementați prin extensie |
   | `OSError: port 8088 already in use` | Dockerfile expune port greșit sau conflict port | Verificați `EXPOSE 8088` în Dockerfile și `CMD ["python", "main.py"]` |
   | Container se închide cu cod 1 | Excepție necontrolată în `main()` | Testați local mai întâi ([Modul 5](05-test-locally.md)) pentru a prinde erori înainte de implementare |

3. **Reimplementați după remediere:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → selectați același agent → implementați o versiune nouă.

### Implementarea durează prea mult

Containerele multi-agent durează mai mult să pornească deoarece creează 4 instanțe de agenți la pornire. Timpuri normale de pornire:

| Etapă | Durată estimată |
|--------|-----------------|
| Construirea imaginii container | 1-3 minute |
| Împingerea imaginii către ACR | 30-60 secunde |
| Pornirea containerului (agent unic) | 15-30 secunde |
| Pornirea containerului (multi-agent) | 30-120 secunde |
| Agent disponibil în Playground | 1-2 minute după „Started” |

> Dacă starea „Pending” persistă mai mult de 5 minute, verificați jurnalele containerului pentru erori.

---

## Probleme RBAC și permisiuni

### `403 Forbidden` sau `AuthorizationFailed`

Aveți nevoie de rolul **[Foundry User](https://aka.ms/foundry-ext-project-role)** în proiectul dvs Foundry (anterior numit **Azure AI User** – ID-ul rolului neschimbat):

1. Accesați [Azure Portal](https://portal.azure.com) → resursa proiectului dvs Foundry.
2. Click pe **Access control (IAM)** → **Role assignments**.
3. Căutați numele dvs → confirmați că este listat **Foundry User** (sau eticheta veche **Azure AI User**).
4. Dacă lipsește: **Add** → **Add role assignment** → căutați **Foundry User** → atribuiți contului dvs.

Consultați documentația [RBAC pentru Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) pentru detalii.

### Implementarea modelului inaccesibilă

Dacă agentul returnează erori legate de model:

1. Verificați că modelul este implementat: bara laterală Foundry → extindeți proiectul → **Models** → verificați dacă `gpt-4.1-mini` (sau modelul dvs) are statusul **Succeeded**.
2. Verificați dacă numele implementării corespunde: comparați `AZURE_AI_MODEL_DEPLOYMENT_NAME` din `.env` (sau `agent.yaml`) cu numele real al implementării din bara laterală.
3. Dacă implementarea a expirat (nivel gratuit): reimplementați din [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Probleme Foundry Local (Calea B)

### Serviciul Foundry Local nu rulează

```powershell
# Verificați starea
foundry local status

# Porniți serviciul dacă este oprit
foundry local start
```

| Simptom | Cauză | Remediere |
|---------|-------|----------|
| Health check returnează `503` | Serviciul nu a pornit | `foundry local start` sau click pe **Start** în bara laterală Foundry Toolkit |
| Health check expiră timpul | Modelul încă se încarcă | Așteptați 30–60 s după pornire; modelele mai mari durează mai mult |
| `StatusCode: 404` pe `/v1/health` | Port greșit | Implicit este `5273`. Verificați `foundry local status` pentru portul real |
| Resurse insuficiente | Foundry Local necesită ~4 GB RAM liber | Închideți alte aplicații |
| Descărcarea modelului eșuează | Spațiu insuficient pe disc | Modelele au 2–8 GB. Eliberați spațiu, apoi `foundry model pull <name>` |

### Nume model nepotrivit

```powershell
# Listează modelele descărcate și aliasurile lor exacte
foundry model list
```

Configurează `AZURE_AI_MODEL_DEPLOYMENT_NAME` în `.env` la aliasul exact afișat (ex: `phi-4-mini`, nu `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` la rulare locală (Calea B)

`main.py` al laboratorului folosește `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local necesită ca această variabilă să indice către serviciul local – **nu** `AZURE_AI_PROJECT_ENDPOINT`. Asigurați-vă că `.env` conține:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Instrumentul MCP face încă un apel extern (Calea B)

Acest lucru este de așteptat. Instrumentul `search_microsoft_learn_for_plan` accesează resurse de învățare de la `https://learn.microsoft.com/api/mcp`. **Doar interogarea pentru numele competenței** circulă prin rețea – textul CV-ului și al descrierii postului sunt procesate integral pe dispozitivul dvs și nu sunt transmise niciodată. Dacă este necesară o funcționare complet offline, adăugați un fallback `try/except` în instrument care returnează o adresă statică `learn.microsoft.com` când endpointul nu este accesibil.

---

## Obținerea ajutorului

Dacă sunteți blocat după ce ați încercat remedierile de mai sus:

1. **Verificați jurnalele serverului** – Majoritatea erorilor generează un traceback Python în terminal. Citiți întregul traceback.
2. **Căutați mesajul de eroare** – Copiați textul erorii și căutați în [Microsoft Q&A pentru Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Deschideți o problemă** – Raportați o problemă în [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) cu:
   - Mesajul de eroare sau captură de ecran
   - Versiunile pachetelor dvs (`pip list | Select-String "agent-framework"`)
   - Versiunea dvs Python (`python --version`)
   - Dacă problema este locală sau după implementare

---

### Punct de control

- [ ] Știți cum să verificați și să remediați problemele de configurare `.env`
- [ ] Puteți verifica dacă versiunile pachetelor corespund matricei cerute
- [ ] Știți cum să verificați jurnalele containerului pentru eșecurile de implementare
- [ ] Puteți verifica rolurile RBAC în Azure Portal

---

**Anterior:** [07 - Verifică în Playground](07-verify-in-playground.md) · **Următor:** [09 - Rezumat →](09-summary.md) · **Acasă:** [Lab 02 README](../README.md) · [Acasă Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->