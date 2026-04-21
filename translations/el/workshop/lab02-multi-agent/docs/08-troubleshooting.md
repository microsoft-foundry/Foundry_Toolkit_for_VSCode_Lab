# Ενότητα 8 - Αντιμετώπιση προβλημάτων (Πολυ-Πράκτορας)

Αυτή η ενότητα καλύπτει κοινά σφάλματα, διορθώσεις και στρατηγικές αποσφαλμάτωσης συγκεκριμένες για τη ροή εργασίας πολυ-πράκτορα. Για γενικά θέματα ανάπτυξης Foundry, ανατρέξτε επίσης στον [οδηγό αντιμετώπισης προβλημάτων του Εργαστηρίου 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Γρήγορη αναφορά: Σφάλμα → Διόρθωση

| Σφάλμα / Σύμπτωμα | Πιθανή αιτία | Διόρθωση |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Απουσία αρχείου `.env` ή μη ορισμένες τιμές | Δημιουργήστε `.env` με `PROJECT_ENDPOINT=<your-endpoint>` και `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Το εικονικό περιβάλλον δεν έχει ενεργοποιηθεί ή δεν έχουν εγκατασταθεί οι εξαρτήσεις | Εκτελέστε `.\.venv\Scripts\Activate.ps1` και μετά `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Το πακέτο MCP δεν έχει εγκατασταθεί (λείπει από τα requirements) | Εκτελέστε `pip install mcp` ή ελέγξτε αν το `requirements.txt` το περιλαμβάνει ως μεταβατική εξάρτηση |
| Ο πράκτορας ξεκινά αλλά επιστρέφει κενή απάντηση | Μη ταύτιση `output_executors` ή λείπουν ακμές | Επαληθεύστε `output_executors=[gap_analyzer]` και ότι όλες οι ακμές υπάρχουν στο `create_workflow()` |
| Μόνο 1 κάρτα κενών (οι υπόλοιπες λείπουν) | Οι οδηγίες του GapAnalyzer είναι ατελείς | Προσθέστε την παράγραφο `CRITICAL:` στο `GAP_ANALYZER_INSTRUCTIONS` - δείτε [Ενότητα 3](03-configure-agents.md) |
| Το σκορ Fit είναι 0 ή απουσιάζει | Ο MatchingAgent δεν έλαβε ανάντη δεδομένα | Επαληθεύστε ότι υπάρχουν `add_edge(resume_parser, matching_agent)` και `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Ο διακομιστής MCP απέρριψε την κλήση εργαλείου | Ελέγξτε τη σύνδεση στο διαδίκτυο. Προσπαθήστε να ανοίξετε το `https://learn.microsoft.com/api/mcp` στο πρόγραμμα περιήγησης. Επαναλάβετε |
| Δεν εμφανίζονται URLs από το Microsoft Learn στην έξοδο | Το εργαλείο MCP δεν είναι καταχωρημένο ή λάθος endpoint | Επαληθεύστε `tools=[search_microsoft_learn_for_plan]` στον GapAnalyzer και ότι το `MICROSOFT_LEARN_MCP_ENDPOINT` είναι σωστό |
| `Address already in use: port 8088` | Άλλη διεργασία χρησιμοποιεί την θύρα 8088 | Εκτελέστε `netstat -ano \| findstr :8088` (Windows) ή `lsof -i :8088` (macOS/Linux) και τερματίστε τη διεργασία που την καταλαμβάνει |
| `Address already in use: port 5679` | Σύγκρουση θύρας debugpy | Σταματήστε άλλες συνεδρίες αποσφαλμάτωσης. Εκτελέστε `netstat -ano \| findstr :5679` για να βρείτε και να σκοτώσετε τη διεργασία |
| Ο Agent Inspector δεν ανοίγει | Ο διακομιστής δεν είναι πλήρως εκκινημένος ή σύγκρουση θύρας | Περιμένετε το μήνυμα "Server running". Ελέγξτε ότι η θύρα 5679 είναι ελεύθερη |
| `azure.identity.CredentialUnavailableError` | Δεν έχετε συνδεθεί στο Azure CLI | Εκτελέστε `az login` και επανεκκινήστε το διακομιστή |
| `azure.core.exceptions.ResourceNotFoundError` | Η ανάπτυξη μοντέλου δεν υπάρχει | Ελέγξτε ότι το `MODEL_DEPLOYMENT_NAME` ταιριάζει με αναπτυγμένο μοντέλο στο έργο Foundry σας |
| Κατάσταση container "Failed" μετά την ανάπτυξη | Σφάλμα του container κατά την εκκίνηση | Ελέγξτε τα logs του container στο sidebar του Foundry. Συνήθως: λείπει μεταβλητή env ή σφάλμα εισαγωγής |
| Η ανάπτυξη εμφανίζει "Pending" για > 5 λεπτά | Το container καθυστερεί να εκκινήσει ή όρια πόρων | Περιμένετε έως 5 λεπτά για τον πολυ-πράκτορα (δημιουργεί 4 instances). Αν συνεχίζει, ελέγξτε τα logs |
| `ValueError` από `WorkflowBuilder` | Μη έγκυρη διαμόρφωση γραφήματος | Βεβαιωθείτε ότι το `start_executor` είναι ορισμένο, το `output_executors` είναι λίστα και δεν υπάρχουν κυκλικές ακμές |

---

## Προβλήματα περιβάλλοντος και ρυθμίσεων

### Λείπουν ή λάθος τιμές στο `.env`

Το αρχείο `.env` πρέπει να βρίσκεται στον φάκελο `PersonalCareerCopilot/` (στο ίδιο επίπεδο με το `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Αναμενόμενο περιεχόμενο `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Πώς βρίσκετε το PROJECT_ENDPOINT:** 
- Ανοίξτε το πλάι της **Microsoft Foundry** στο VS Code → δεξί κλικ στο έργο σας → **Copy Project Endpoint**. 
- Ή μεταβείτε στο [Azure Portal](https://portal.azure.com) → το έργο Foundry σας → **Overview** → **Project endpoint**.

> **Πώς βρίσκετε το MODEL_DEPLOYMENT_NAME:** Στο sidebar του Foundry, αναπτύξτε το έργο σας → **Models** → βρείτε το όνομα του αναπτυγμένου μοντέλου (π.χ. `gpt-4.1-mini`).

### Προτεραιότητα μεταβλητών περιβάλλοντος

Το `main.py` χρησιμοποιεί `load_dotenv(override=False)`, που σημαίνει:

| Προτεραιότητα | Πηγή | Κερδίζει όταν υπάρχουν και οι δύο; |
|--------------|-------|----------------------------------|
| 1 (υψηλότερη) | Μεταβλητή περιβάλλοντος shell | Ναι |
| 2 | Αρχείο `.env` | Μόνο αν η μεταβλητή shell δεν είναι ορισμένη |

Αυτό σημαίνει ότι οι μεταβλητές περιβάλλοντος Foundry κατά το runtime (που ορίζονται μέσω `agent.yaml`) έχουν προτεραιότητα έναντι των τιμών `.env` κατά την φιλοξενούμενη ανάπτυξη.

---

## Συμβατότητα εκδόσεων

### Πίνακας εκδόσεων πακέτων

Η ροή εργασίας πολυ-πράκτορα απαιτεί συγκεκριμένες εκδόσεις πακέτων. Μη ταιριαστές εκδόσεις προκαλούν σφάλματα κατά την εκτέλεση.

| Πακέτο | Απαραίτητη έκδοση | Εντολή ελέγχου |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | τελευταία προ-έκδοση | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Συνηθισμένα σφάλματα εκδόσεων

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Διόρθωση: αναβάθμιση σε rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` δεν βρέθηκε ή ο Inspector είναι ασύμβατος:**

```powershell
# Διόρθωση: εγκατάσταση με την επιλογή --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Διόρθωση: αναβάθμιση πακέτου mcp
pip install mcp --upgrade
```

### Επαλήθευση όλων των εκδόσεων ταυτόχρονα

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Αναμενόμενη έξοδος:

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

## Προβλήματα εργαλείου MCP

### Το εργαλείο MCP δεν επιστρέφει αποτελέσματα

**Σύμπτωμα:** Οι κάρτες κενών εμφανίζουν "No results returned from Microsoft Learn MCP" ή "No direct Microsoft Learn results found".

**Πιθανές αιτίες:**

1. **Πρόβλημα δικτύου** - Το endpoint MCP (`https://learn.microsoft.com/api/mcp`) δεν είναι προσβάσιμο.
   ```powershell
   # Δοκιμή σύνδεσης
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Αν επιστρέφει `200`, το endpoint είναι προσβάσιμο.

2. **Ερώτημα πολύ συγκεκριμένο** - Το όνομα δεξιότητας είναι πολύ εξειδικευμένο για την αναζήτηση στο Microsoft Learn.
   - Αυτό αναμένεται για πολύ εξειδικευμένες δεξιότητες. Το εργαλείο έχει fallback URL στην απάντηση.

3. **Timeout σύνδεσης MCP** - Η σύνδεση Streamable HTTP έληξε.
   - Επαναλάβετέ το. Οι συνεδρίες MCP είναι εφήμερες και μπορεί να χρειαστεί επανασύνδεση.

### Επεξήγηση logs MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Σημασία | Ενέργεια |
|-----|---------|--------|
| `GET → 405` | Probes MCP client κατά την αρχικοποίηση | Κανονικό - αγνοήστε |
| `POST → 200` | Επιτυχής κλήση εργαλείου | Αναμενόμενο |
| `DELETE → 405` | Probes MCP client κατά το cleanup | Κανονικό - αγνοήστε |
| `POST → 400` | Άσχημο αίτημα (λάθος μορφή ερωτήματος) | Ελέγξτε την παράμετρο `query` στη `search_microsoft_learn_for_plan()` |
| `POST → 429` | Περιορισμός ρυθμού | Περιμένετε και επαναλάβετέ το. Μειώστε την παράμετρο `max_results` |
| `POST → 500` | Σφάλμα διακομιστή MCP | Παροδικό - επαναλάβετε. Αν επιμένει, το Microsoft Learn MCP API μπορεί να είναι εκτός λειτουργίας |
| Timeout σύνδεσης | Πρόβλημα δικτύου ή διακομιστής MCP μη διαθέσιμος | Ελέγξτε το διαδίκτυο. Δοκιμάστε `curl https://learn.microsoft.com/api/mcp` |

---

## Προβλήματα ανάπτυξης

### Το container αποτυγχάνει να ξεκινήσει μετά την ανάπτυξη

1. **Ελέγξτε τα logs του container:**
   - Ανοίξτε το sidebar **Microsoft Foundry** → αναπτύξτε **Hosted Agents (Preview)** → κάντε κλικ στον πράκτορα → αναπτύξτε την έκδοση → **Container Details** → **Logs**.
   - Αναζητήστε Python stack traces ή σφάλματα απουσίας module.

2. **Συνήθη σφάλματα εκκίνησης container:**

   | Σφάλμα στα logs | Αιτία | Διόρθωση |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Στο `requirements.txt` λείπει πακέτο | Προσθέστε το πακέτο, αναπτύξτε ξανά |
   | `RuntimeError: Missing required environment variable` | Στο `agent.yaml` δεν έχουν οριστεί env vars | Ενημερώστε το `agent.yaml` → τμήμα `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | Δεν έχει ρυθμιστεί Managed Identity | Το Foundry το ενεργοποιεί αυτόματα - βεβαιωθείτε ότι αναπτύσσετε μέσω της επέκτασης |
   | `OSError: port 8088 already in use` | Στο Dockerfile εκτίθεται λάθος θύρα ή υπάρχει σύγκρουση θύρας | Ελέγξτε το `EXPOSE 8088` στο Dockerfile και το `CMD ["python", "main.py"]` |
   | Το container τερματίζει με κωδικό 1 | Ανεπεξέργαστη εξαίρεση στο `main()` | Δοκιμάστε το τοπικά πρώτα ([Ενότητα 5](05-test-locally.md)) για να πιάσετε σφάλματα πριν την ανάπτυξη |

3. **Επανααναπτύξτε μετά τη διόρθωση:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → επιλέξτε τον ίδιο πράκτορα → αναπτύξτε νέα έκδοση.

### Η ανάπτυξη διαρκεί πολύ

Τα container πολυ-πράκτορα χρειάζονται περισσότερο χρόνο εκκίνησης επειδή δημιουργούν 4 instances πράκτορα κατά την εκκίνηση. Συνηθισμένοι χρόνοι εκκίνησης:

| Στάδιο | Αναμενόμενη διάρκεια |
|-------|------------------|
| Κατασκευή εικόνας container | 1-3 λεπτά |
| Push εικόνας σε ACR | 30-60 δευτ. |
| Εκκίνηση container (μονός πράκτορας) | 15-30 δευτ. |
| Εκκίνηση container (πολυ-πράκτορας) | 30-120 δευτ. |
| Πράκτορας διαθέσιμος στο Playground | 1-2 λεπτά μετά το "Started" |

> Αν η κατάσταση "Pending" διαρκεί πάνω από 5 λεπτά, ελέγξτε τα logs του container για σφάλματα.

---

## Προβλήματα RBAC και δικαιωμάτων

### `403 Forbidden` ή `AuthorizationFailed`

Χρειάζεστε τον ρόλο **[Azure AI User](https://aka.ms/foundry-ext-project-role)** στο έργο Foundry σας:

1. Μεταβείτε στο [Azure Portal](https://portal.azure.com) → στον πόρο **project** του Foundry σας.
2. Κάντε κλικ στο **Access control (IAM)** → **Role assignments**.
3. Αναζητήστε το όνομά σας → επιβεβαιώστε ότι υπάρχει ο ρόλος **Azure AI User**.
4. Αν λείπει: **Add** → **Add role assignment** → αναζητήστε **Azure AI User** → αναθέστε τον στον λογαριασμό σας.

Δείτε την [τεκμηρίωση RBAC για Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) για λεπτομέρειες.

### Μη προσβάσιμη ανάπτυξη μοντέλου

Αν ο πράκτορας επιστρέφει σφάλματα σχετικά με μοντέλο:

1. Επαληθεύστε ότι το μοντέλο είναι αναπτυγμένο: sidebar Foundry → αναπτύξτε το έργο → **Models** → ελέγξτε αν υπάρχει `gpt-4.1-mini` (ή το δικό σας) με κατάσταση **Succeeded**.
2. Επαληθεύστε ότι το όνομα ανάπτυξης ταιριάζει: συγκρίνετε το `MODEL_DEPLOYMENT_NAME` στο `.env` (ή `agent.yaml`) με το πραγματικό όνομα ανάπτυξης στο sidebar.
3. Αν η ανάπτυξη έχει λήξει (free tier): επανααναπτύξτε από το [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Προβλήματα Agent Inspector

### Ο Inspector ανοίγει αλλά δείχνει "Disconnected"

1. Επαληθεύστε ότι ο διακομιστής τρέχει: ψάξτε τη φράση "Server running on http://localhost:8088" στο τερματικό.
2. Ελέγξτε τη θύρα `5679`: Ο Inspector συνδέεται μέσω debugpy στη θύρα 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Επανεκκινήστε τον διακομιστή και ανοίξτε ξανά τον Inspector.

### Ο Inspector δείχνει μερική απάντηση

Οι απαντήσεις πολυ-πράκτορα είναι μακροσκελείς και ρέουν σταδιακά. Περιμένετε να ολοκληρωθεί η πλήρης απάντηση (μπορεί να πάρει 30-60 δευτερόλεπτα ανάλογα με τον αριθμό των gap cards και των κλήσεων εργαλείου MCP).

Αν η απάντηση κόβεται συνεχώς:
- Ελέγξτε ότι οι οδηγίες του GapAnalyzer περιλαμβάνουν το μπλοκ `CRITICAL:` που αποτρέπει το συνδυασμό gap cards.
- Ελέγξτε το όριο token του μοντέλου σας - το `gpt-4.1-mini` υποστηρίζει έως 32K έξοδους token, που θα πρέπει να είναι αρκετό.

---

## Συμβουλές απόδοσης

### Αργές απαντήσεις

Οι ροές εργασίας πολυ-πράκτορα είναι εγγενώς πιο αργές από των μονών πρακτόρων λόγω διαδοχικών εξαρτήσεων και κλήσεων εργαλείου MCP.

| Βελτιστοποίηση | Πώς | Επίδραση |
|-------------|-----|--------|
| Μειώστε κλήσεις MCP | Μειώστε την παράμετρο `max_results` στο εργαλείο | Λιγότερα HTTP round-trips |
| Απλοποιήστε τις οδηγίες | Συντομότερα, πιο εστιασμένα prompts πράκτορα | Γρηγορότερη επεξεργασία LLM |
| Χρησιμοποιήστε `gpt-4.1-mini` | Πιο γρήγορο από `gpt-4.1` για ανάπτυξη | Περίπου διπλάσια ταχύτητα |
| Μειώστε την λεπτομέρεια των gap cards | Απλοποιήστε τη μορφή των gap cards στις οδηγίες GapAnalyzer | Λιγότερη έξοδος να παραχθεί |

### Τυπικοί χρόνοι απάντησης (τοπικά)

| Διαμόρφωση | Αναμενόμενος χρόνος |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap cards | 30-60 δευτ. |
| `gpt-4.1-mini`, 8+ gap cards | 60-120 δευτ. |
| `gpt-4.1`, 3-5 gap cards | 60-120 δευτ. |
---

## Λήψη βοήθειας

Εάν κολλήσετε αφού δοκιμάσετε τις παραπάνω διορθώσεις:

1. **Ελέγξτε τα αρχεία καταγραφής του διακομιστή** - Τα περισσότερα σφάλματα παράγουν ένα ίχνος στοίβας Python στο τερματικό. Διαβάστε ολόκληρο το ίχνος.
2. **Αναζητήστε το μήνυμα σφάλματος** - Αντιγράψτε το κείμενο του σφάλματος και αναζητήστε στο [Microsoft Q&A για το Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Ανοίξτε ένα ζήτημα** - Δημιουργήστε ένα ζήτημα στο [αποθετήριο εργαστηρίου](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) με:
   - Το μήνυμα σφάλματος ή ένα στιγμιότυπο οθόνης
   - Τις εκδόσεις των πακέτων σας (`pip list | Select-String "agent-framework"`)
   - Την έκδοση της Python σας (`python --version`)
   - Εάν το πρόβλημα είναι τοπικό ή μετά την ανάπτυξη

---

### Σημείο Ελέγχου

- [ ] Μπορείτε να εντοπίσετε και να διορθώσετε τα πιο συνηθισμένα σφάλματα πολλαπλών πρακτόρων χρησιμοποιώντας τον πίνακα γρήγορης αναφοράς
- [ ] Γνωρίζετε πώς να ελέγξετε και να διορθώσετε προβλήματα ρύθμισης `.env`
- [ ] Μπορείτε να επαληθεύσετε ότι οι εκδόσεις των πακέτων ταιριάζουν με τον απαιτούμενο πίνακα
- [ ] Κατανοείτε τις καταχωρήσεις καταγραφής MCP και μπορείτε να διαγνώσετε αποτυχίες εργαλείων
- [ ] Γνωρίζετε πώς να ελέγξετε τα αρχεία καταγραφής κοντέινερ για αποτυχίες ανάπτυξης
- [ ] Μπορείτε να επαληθεύσετε τους ρόλους RBAC στην Πύλη Azure

---

**Προηγούμενο:** [07 - Επιβεβαίωση στο Playground](07-verify-in-playground.md) · **Αρχική:** [Lab 02 README](../README.md) · [Αρχική Εργαστηρίου](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Αποποίηση ευθυνών**:
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία μετάφρασης AI [Co-op Translator](https://github.com/Azure/co-op-translator). Παρόλο που επιδιώκουμε την ακρίβεια, παρακαλούμε να γνωρίζετε ότι οι αυτοματοποιημένες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη γλώσσα του πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν ευθυνόμαστε για οποιεσδήποτε παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->