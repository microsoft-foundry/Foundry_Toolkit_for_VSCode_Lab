# Modul 8 - Depanare (Multi-Agent)

Acest modul acoperă erorile comune, remedierile și strategiile de depanare specifice fluxului de lucru multi-agent. Pentru probleme generale de implementare Foundry, consultați și [Ghidul de depanare Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Referință rapidă: Eroare → Remediere

| Eroare / Simptom | Cauză Probabilă | Remediere |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Fișier `.env` lipsește sau valorile nu sunt setate | Creați `.env` cu `PROJECT_ENDPOINT=<your-endpoint>` și `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Mediul virtual nu este activat sau dependențele nu sunt instalate | Rulați `.\.venv\Scripts\Activate.ps1` apoi `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Pachetul MCP nu este instalat (lipsește din requirements) | Rulați `pip install mcp` sau verificați dacă `requirements.txt` îl include ca dependență tranzitivă |
| Agentul pornește, dar returnează răspuns gol | nepotrivire `output_executors` sau muchii lipsă | Verificați `output_executors=[gap_analyzer]` și că toate muchiile există în `create_workflow()` |
| Doar 1 carte gap (restul lipsesc) | Instrucțiunile GapAnalyzer incomplete | Adăugați paragraful `CRITICAL:` la `GAP_ANALYZER_INSTRUCTIONS` - vezi [Modul 3](03-configure-agents.md) |
| Scorul de potrivire este 0 sau absent | MatchingAgent nu a primit date în amonte | Verificați existența ambelor `add_edge(resume_parser, matching_agent)` și `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Serverul MCP a respins apelul instrumentului | Verificați conectivitatea la internet. Încercați să deschideți `https://learn.microsoft.com/api/mcp` în browser. Reîncercați |
| Niciun URL Microsoft Learn în ieșire | Instrumentul MCP nu este înregistrat sau endpointul este greșit | Verificați `tools=[search_microsoft_learn_for_plan]` pe GapAnalyzer și că `MICROSOFT_LEARN_MCP_ENDPOINT` este corect |
| `Address already in use: port 8088` | Alt proces folosește portul 8088 | Rulați `netstat -ano \| findstr :8088` (Windows) sau `lsof -i :8088` (macOS/Linux) și opriți procesul în conflict |
| `Address already in use: port 5679` | Conflict port Debugpy | Opriți alte sesiuni de depanare. Rulați `netstat -ano \| findstr :5679` pentru a găsi și termina procesul |
| Agent Inspector nu se deschide | Serverul nu a pornit complet sau conflict port | Așteptați logul "Server running". Verificați dacă portul 5679 este liber |
| `azure.identity.CredentialUnavailableError` | Nu sunteți autentificat în Azure CLI | Rulați `az login` apoi reporniți serverul |
| `azure.core.exceptions.ResourceNotFoundError` | Implementarea modelului nu există | Verificați dacă `MODEL_DEPLOYMENT_NAME` corespunde unui model implementat în proiectul Foundry |
| Starea containerului „Failed” după implementare | Containerul s-a blocat la pornire | Verificați jurnalele containerului în bara laterală Foundry. Frecvent: variabilă de mediu lipsă sau eroare la import |
| Implementarea arată „Pending” > 5 minute | Containerul durează prea mult să pornească sau limite de resurse | Așteptați până la 5 minute pentru multi-agent (creează 4 instanțe agent). Dacă este încă în așteptare, verificați jurnalele |
| `ValueError` de la `WorkflowBuilder` | Configurație grafic invalidă | Asigurați-vă că `start_executor` este setat, `output_executors` este o listă, și nu există muchii ciclice |

---

## Probleme de mediu și configurare

### Lipsă sau valori greșite în `.env`

Fișierul `.env` trebuie să fie în directorul `PersonalCareerCopilot/` (același nivel cu `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Conținutul așteptat al `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Cum găsiți PROJECT_ENDPOINT:** 
- Deschideți bara laterală **Microsoft Foundry** în VS Code → click dreapta pe proiectul dvs. → **Copy Project Endpoint**. 
- Sau mergeți la [Azure Portal](https://portal.azure.com) → proiectul dvs. Foundry → **Overview** → **Project endpoint**.

> **Cum găsiți MODEL_DEPLOYMENT_NAME:** În bara laterală Foundry, extindeți proiectul → **Models** → găsiți numele modelului implementat (ex: `gpt-4.1-mini`).

### Ordinea de prioritate a variabilelor de mediu

`main.py` folosește `load_dotenv(override=False)`, ceea ce înseamnă:

| Prioritate | Sursă | Câștigă când ambele sunt setate? |
|----------|--------|------------------------|
| 1 (cea mai mare) | Variabilă de mediu shell | Da |
| 2 | Fișier `.env` | Doar dacă variabila shell nu este setată |

Aceasta înseamnă că variabilele de mediu runtime Foundry (setate prin `agent.yaml`) au prioritate în fața valorilor din `.env` în timpul implementării găzduite.

---

## Compatibilitate versiuni

### Matrice versiuni pachete

Fluxul multi-agent necesită versiuni specifice ale pachetelor. Versiunile nepotrivite provoacă erori la runtime.

| Pachet | Versiune Cerută | Comandă de verificare |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | cea mai recentă versiune pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Erori comune de versiune

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Remediere: actualizare la rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nu este găsit sau Inspectorul este incompatibil:**

```powershell
# Remediere: instalare cu flagul --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Remediere: actualizează pachetul mcp
pip install mcp --upgrade
```

### Verificați toate versiunile simultan

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Ieșire așteptată:

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

## Probleme cu instrumentul MCP

### Instrumentul MCP nu returnează rezultate

**Simptom:** Cărțile gap afișează „No results returned from Microsoft Learn MCP” sau „No direct Microsoft Learn results found”.

**Cauze posibile:**

1. **Probleme de rețea** - Endpoint-ul MCP (`https://learn.microsoft.com/api/mcp`) nu este accesibil.
   ```powershell
   # Testați conectivitatea
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Dacă acesta returnează `200`, endpoint-ul este accesibil.

2. **Interogare prea specifică** - Numele competenței este prea nișat pentru căutarea Microsoft Learn.
   - Acest lucru este normal pentru competențe foarte specializate. Instrumentul oferă o adresă URL de rezervă în răspuns.

3. **Timeout sesiune MCP** - Conexiunea Streamable HTTP a expirat.
   - Reîncercați solicitarea. Sesiunile MCP sunt efemere și pot necesita reconectare.

### Explicație jurnale MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Jurnal | Semnificație | Acțiune |
|-----|---------|--------|
| `GET → 405` | Probe MCP în timpul inițializării | Normal - ignorați |
| `POST → 200` | Apelul instrumentului a reușit | Așteptat |
| `DELETE → 405` | Probe MCP în timpul curățării | Normal - ignorați |
| `POST → 400` | Cerere greșită (query malformat) | Verificați parametrul `query` în `search_microsoft_learn_for_plan()` |
| `POST → 429` | Limitare de rată | Așteptați și reîncercați. Reduceți parametrul `max_results` |
| `POST → 500` | Eroare server MCP | Temporar - reîncercați. Dacă persistă, API-ul Microsoft Learn MCP poate fi căzut |
| Timeout conexiune | Problemă de rețea sau server MCP indisponibil | Verificați internetul. Încercați `curl https://learn.microsoft.com/api/mcp` |

---

## Probleme la implementare

### Containerul nu pornește după implementare

1. **Verificați jurnalele containerului:**
   - Deschideți bara laterală **Microsoft Foundry** → extindeți **Hosted Agents (Preview)** → dați click pe agentul dvs. → extindeți versiunea → **Container Details** → **Logs**.
   - Căutați traceback-uri Python sau erori de module lipsă.

2. **Eșecuri frecvente la pornirea containerului:**

   | Eroare în jurnale | Cauză | Remediere |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` lipsește un pachet | Adăugați pachetul, reimplementați |
   | `RuntimeError: Missing required environment variable` | Variabilele de mediu din `agent.yaml` nu sunt setate | Actualizați secțiunea `environment_variables` din `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity neconfigurat | Foundry setează automat - asigurați-vă că implementați prin extensie |
   | `OSError: port 8088 already in use` | Dockerfile expune port greșit sau conflict port | Verificați `EXPOSE 8088` în Dockerfile și `CMD ["python", "main.py"]` |
   | Container iese cu cod 1 | Excepție negestionată în `main()` | Testați local mai întâi ([Modul 5](05-test-locally.md)) pentru a depista erori înainte de implementare |

3. **Reimplementați după remediere:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → selectați același agent → implementați o versiune nouă.

### Implementarea durează prea mult

Containerele multi-agent durează mai mult să pornească fiindcă creează 4 instanțe agent la pornire. Timpuri normale de pornire:

| Etapă | Durată așteptată |
|-------|------------------|
| Construire imagine container | 1-3 minute |
| Împingere imagine în ACR | 30-60 secunde |
| Pornire container (agent unic) | 15-30 secunde |
| Pornire container (multi-agent) | 30-120 secunde |
| Agent disponibil în Playground | 1-2 minute după „Started” |

> Dacă starea „Pending” persistă mai mult de 5 minute, verificați jurnalele containerului pentru erori.

---

## Probleme RBAC și permisiuni

### `403 Forbidden` sau `AuthorizationFailed`

Aveți nevoie de rolul **[Azure AI User](https://aka.ms/foundry-ext-project-role)** pe proiectul dvs. Foundry:

1. Mergeți la [Azure Portal](https://portal.azure.com) → resursa proiectului Foundry.
2. Click pe **Access control (IAM)** → **Role assignments**.
3. Căutați-vă numele → verificați dacă este listat **Azure AI User**.
4. Dacă lipsește: **Add** → **Add role assignment** → căutați **Azure AI User** → atribuiți contului dvs.

Consultați documentația [RBAC pentru Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) pentru detalii.

### Implementarea modelului inaccesibilă

Dacă agentul returnează erori legate de model:

1. Verificați că modelul este implementat: bara laterală Foundry → extindeți proiectul → **Models** → verificați dacă `gpt-4.1-mini` (sau modelul dvs.) are starea **Succeeded**.
2. Verificați dacă numele implementării corespunde: comparați `MODEL_DEPLOYMENT_NAME` din `.env` (sau `agent.yaml`) cu numele real al implementării din bara laterală.
3. Dacă implementarea a expirat (tier gratuit): reimplementați din [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Probleme cu Agent Inspector

### Inspectorul se deschide, dar afișează "Disconnected"

1. Verificați dacă serverul rulează: căutați mesajul "Server running on http://localhost:8088" în terminal.
2. Verificați portul `5679`: Inspectorul se conectează prin debugpy pe portul 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Reporniti serverul și redeschideți Inspectorul.

### Inspector arată răspuns parțial

Răspunsurile multi-agent sunt lungi și se transmit incremental. Așteptați completarea răspunsului complet (poate dura 30-60 secunde în funcție de numărul de cărți gap și apeluri MCP).

Dacă răspunsul este tăiat constant:
- Verificați că instrucțiunile GapAnalyzer au blocul `CRITICAL:` care împiedică combinarea cărților gap.
- Verificați limita tokenilor modelului dvs. - `gpt-4.1-mini` suportă până la 32K de tokeni ieșire, ceea ce ar trebui să fie suficient.

---

## Sfaturi de performanță

### Răspunsuri lente

Fluxurile multi-agent sunt în mod inerent mai lente decât cele single-agent din cauza dependențelor secvențiale și a apelurilor instrumentului MCP.

| Optimizare | Cum | Impact |
|-------------|-----|--------|
| Reduceți apelurile MCP | Reduceți parametrul `max_results` în instrument | Mai puține cereri HTTP |
| Simplificați instrucțiunile | Prompturi agent mai scurte, mai concentrate | Infernță LLM mai rapidă |
| Folosiți `gpt-4.1-mini` | Mai rapid decât `gpt-4.1` pentru dezvoltare | Îmbunătățire de aproximativ 2x |
| Reduceți detaliile cărții gap | Simplificați formatul cărții gap din instrucțiunile GapAnalyzer | Mai puțin output de generat |

### Timpuri tipice de răspuns (local)

| Configurație | Timp așteptat |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 cărți gap | 30-60 secunde |
| `gpt-4.1-mini`, 8+ cărți gap | 60-120 secunde |
| `gpt-4.1`, 3-5 cărți gap | 60-120 secunde |
---

## Obținerea ajutorului

Dacă ești blocat după ce ai încercat soluțiile de mai sus:

1. **Verifică jurnalele serverului** - Majoritatea erorilor produc un traceback Python în terminal. Citește întregul traceback.
2. **Caută mesajul de eroare** - Copiază textul erorii și caută în [Microsoft Q&A pentru Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Deschide un tichet** - Deschide un tichet în [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) cu:
   - Mesajul de eroare sau o captură de ecran
   - Versiunile pachetelor tale (`pip list | Select-String "agent-framework"`)
   - Versiunea ta de Python (`python --version`)
   - Dacă problema este locală sau după implementare

---

### Lista de verificare

- [ ] Poți identifica și rezolva cele mai comune erori multi-agent folosind tabelul de referință rapidă
- [ ] Știi cum să verifici și să remediezi problemele de configurare `.env`
- [ ] Poți verifica dacă versiunile pachetelor corespund cu matricea cerută
- [ ] Înțelegi intrările de jurnal MCP și poți diagnostica erorile uneltelor
- [ ] Știi cum să verifici jurnalele containerului pentru erorile de implementare
- [ ] Poți verifica rolurile RBAC în Portalul Azure

---

**Anterior:** [07 - Verify in Playground](07-verify-in-playground.md) · **Acasă:** [Lab 02 README](../README.md) · [Pagina principală a workshop-ului](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm răspunderea pentru eventuale neînțelegeri sau interpretări greșite rezultate din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->