# Ενότητα 8 - Επίλυση προβλημάτων

Αυτή η ενότητα καλύπτει κοινά σφάλματα, διορθώσεις και στρατηγικές αποσφαλμάτωσης ειδικά για τη ροή εργασίας πολλαπλών πρακτόρων.

## Προβλήματα εξόδου πράκτορα

### Ο GapAnalyzer λέει «Ακόμα δεν έχω την αντίστοιχη αναφορά»

**Συμπτώματα:** Η απάντηση του GapAnalyzer ζητά να επικολλήσετε μια αντίστοιχη αναφορά με «Ελλείποντες Δεξιότητες» και «Κενά Πιστοποίησης». Αυτό συμβαίνει ακόμη και όταν στείλατε τόσο βιογραφικό όσο και περιγραφή εργασίας.

**Αιτία:** Το κείμενο της JD δεν μεταδόθηκε στον JD Agent. Με `context_mode="last_agent"`, `resume_executor` είναι ο μόνος εκτελεστής που βλέπει το αρχικό μήνυμα του χρήστη. Εάν `RESUME_PARSER_INSTRUCTIONS` δεν περιλαμβάνει το κείμενο της JD στην έξοδό του, ο JD Agent δεν έχει JD για ανάλυση, ο MatchingAgent δεν μπορεί να υπολογίσει βαθμολογία ταύτισης και ο GapAnalyzer λαμβάνει άχρηστη είσοδο.

**Διάγνωση:**

Στα αρχεία καταγραφής του διακομιστή, αναζητήστε την περίοδο MatchingAgent. Εάν περιέχει:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
το πέρασμα λείπει ή είναι σπασμένο.

**Διόρθωση:** Επιβεβαιώστε ότι `RESUME_PARSER_INSTRUCTIONS` στο `main.py` περιέχει μια ενότητα `[JOB DESCRIPTION PASS-THROUGH]` και τον κανόνα:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Επιβεβαιώστε επίσης ότι `JOB_DESCRIPTION_INSTRUCTIONS` περιέχει έναν κανόνα ροής `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Εάν κάποιο από τα μπλοκ οδηγιών είναι υπόδειγμα από τον οδηγό σκελετού, αντικαταστήστε το με την ολοκληρωμένη έκδοση από [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Ο MatchingAgent εμφανίζει «Δεν είναι δυνατός ο υπολογισμός της βαθμολογίας ταύτισης - δεν παρέχεται JD»

Πρόκειται για την ίδια βασική αιτία όπως παραπάνω. Ο MatchingAgent έλαβε την έξοδο του JD Agent αλλά η ενότητα `[PARSED RESUME PASS-THROUGH]` έλειπε ή ήταν άδεια, οπότε δεν μπορούσε να συγκρίνει τα δύο προφίλ. Επιβεβαιώστε:
1. `JOB_DESCRIPTION_INSTRUCTIONS` περιλαμβάνει τον κανόνα ροής: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` λέει στον πράκτορα να αναζητήσει ενότητες `[JD REQUIREMENTS]` και `[PARSED RESUME PASS-THROUGH]`.

Αντικαταστήστε και τα δύο μπλοκ οδηγιών με τις ολοκληρωμένες εκδόσεις από [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Η απάντηση εμφανίζεται δύο φορές

**Συμπτώματα:** Η έξοδος του GapAnalyzer (ή ολόκληρη η έξοδος της ροής) εμφανίζεται δύο φορές στην απάντηση του Agent Inspector.

**Αιτία:** `WorkflowBuilder` χρησιμοποιεί λογική OR για τις εισερχόμενες ακμές - ένας εκτελεστής εκκινείται μόλις ολοκληρωθεί **οποιοσδήποτε** πρόγονος. Εάν ο `matching_executor` έχει δύο εισερχόμενες ακμές (μια από `resume_executor` και μια από `jd_executor`), εκκινείται δύο φορές: μία όταν ολοκληρωθεί ο ResumeParser και ξανά όταν ολοκληρωθεί ο JD Agent. Μετά, και ο GapAnalyzer τρέχει δύο φορές.

**Διόρθωση:** Βεβαιωθείτε ότι το γράφημα `WorkflowBuilder` είναι αυστηρά σειριακή ροή χωρίς συγχώνευση ακμών:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Αν έχετε μια ανεπιθύμητη γραμμή `.add_edge(resume_executor, matching_executor)`, αφαιρέστε την. Η ροή `[PARSED RESUME PASS-THROUGH]` στην έξοδο του JD Agent ήδη δίνει στον MatchingAgent πρόσβαση στο βιογραφικό.

---

## Προβλήματα περιβάλλοντος και ρυθμίσεων

### Λείπουν ή λανθασμένες τιμές `.env`

Το αρχείο `.env` πρέπει να βρίσκεται στον κατάλογο `PersonalCareerCopilot/` (στο ίδιο επίπεδο με `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Αναμενόμενο περιεχόμενο `.env`:

**Διαδρομή Α - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Διαδρομή Β - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Και οι δύο διαδρομές χρησιμοποιούν `FOUNDRY_PROJECT_ENDPOINT`. Η τιμή διαφέρει: το cloud χρησιμοποιεί ένα `https://` Foundry endpoint· το τοπικό χρησιμοποιεί `http://localhost:5273/v1`. Εκτελέστε `foundry model list` για να επιβεβαιώσετε το ακριβές ψευδώνυμο του μοντέλου για τη Διαδρομή Β.

> **Εύρεση του `FOUNDRY_PROJECT_ENDPOINT` σας:** 
- Ανοίξτε το πλαϊνό μενού **Foundry Toolkit** στο VS Code → κάντε δεξί κλικ στο έργο σας → **Copy Project Endpoint**. 
- Ή πηγαίνετε στο [Azure Portal](https://portal.azure.com) → στο έργο Foundry σας → **Overview** → **Project endpoint**.

> **Εύρεση του `AZURE_AI_MODEL_DEPLOYMENT_NAME` σας:** Στο πλάι Foundry Toolkit, ανοίξτε το έργο σας → **Models** → βρείτε το όνομα του εκτελεσμένου μοντέλου (π.χ., `gpt-4.1-mini`).

### Προτεραιότητα περιβαλλοντικών μεταβλητών

`main.py` χρησιμοποιεί `load_dotenv(override=True)`, που σημαίνει:

| Προτεραιότητα | Πηγή | Νικά όταν και οι δύο είναι ορισμένοι; |
|-------------|-------|-------------------------------|
| 1 (υψηλότερη) | Αρχείο `.env` | Ναι |
| 2 | Μεταβλητή περιβάλλοντος Shell / κοντέινερ | Χρησιμοποιείται όταν το ίδιο κλειδί δεν υπάρχει στο `.env` |

Στην τοπική ανάπτυξη, αυτό κάνει το `.env` την πηγή αλήθειας (η επεξεργασία του `.env` επηρεάζει άμεσα τις εκτελέσεις). Σε φιλοξενούμενη ανάπτυξη, το Foundry εγχύει μεταβλητές περιβάλλοντος στο επίπεδο του κοντέινερ· καθώς το `.env` δεν είναι μέρος της αναπτυγμένης εικόνας για αυτό το εργαστήριο, χρησιμοποιούνται οι εγχυμένες τιμές κοντέινερ.

---

## Συμβατότητα εκδόσεων

### Πίνακας εκδόσεων πακέτων

Η ροή εργασίας πολλαπλών πρακτόρων απαιτεί συγκεκριμένες εκδόσεις πακέτων. Ασυμβατότητες εκδόσεων προκαλούν σφάλματα κατά το χρόνο εκτέλεσης.

| Πακέτο | Απαιτούμενη Έκδοση | Εντολή Ελέγχου |
|--------|---------------------|-----------------|
| `agent-framework-foundry` | τελευταία | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | τελευταία | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | τελευταία | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Συνήθη σφάλματα έκδοσης

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

### Επαλήθευση όλων των εκδόσεων ταυτόχρονα

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Αναμενόμενο αποτέλεσμα:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Προβλήματα ανάπτυξης

### Ο κοντέινερ αποτυγχάνει να ξεκινήσει μετά την ανάπτυξη

1. **Ελέγξτε τα αρχεία καταγραφής κοντέινερ:**
   - Ανοίξτε το πλαϊνό Foundry Toolkit → κάτω από το έργο σας, κάντε κλικ στο **Agents** → καρτέλα **Hosted Agent** → κάντε κλικ στον πράκτορά σας. Ελέγξτε το **Status** στην καρτέλα **Details**, στη συνέχεια ανοίξτε την καρτέλα **Playground** και χρησιμοποιήστε την καρτέλα **Logs** στο πάνελ **Session Details** για να δείτε την έξοδο του κοντέινερ.
   - Αναζητήστε Python stack traces ή σφάλματα απουσίας module.

2. **Συχνά σφάλματα εκκίνησης κοντέινερ:**

   | Σφάλμα στα αρχεία | Αιτία | Διόρθωση |
   |-------------------|-------|---------|
   | `ModuleNotFoundError` | Λείπει πακέτο `requirements.txt` | Προσθέστε το πακέτο, αναπτύξτε ξανά |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Μεταβλητές περιβάλλοντος `agent.yaml` ή `.env` δεν έχουν οριστεί | Ενημερώστε το `agent.yaml` → ενότητα `environment_variables` (φιλοξενούμενο) ή `.env` (τοπικό) |
   | `azure.identity.CredentialUnavailableError` | Το Managed Identity δεν έχει ρυθμιστεί | Το Foundry το ρυθμίζει αυτόματα - βεβαιωθείτε ότι αναπτύσσετε μέσω του πρόσθετου |
   | `OSError: port 8088 already in use` | Dockerfile εκθέτει λάθος θύρα ή υπάρχει σύγκρουση θυρών | Επαληθεύστε `EXPOSE 8088` στο Dockerfile και `CMD ["python", "main.py"]` |
   | Ο κοντέινερ ολοκληρώνεται με κωδικό 1 | Απερίσκεπτη εξαίρεση στο `main()` | Δοκιμάστε το τοπικά πρώτα ([Ενότητα 5](05-test-locally.md)) για να πιάσετε σφάλματα πριν την ανάπτυξη |

3. **Αναπτύξτε ξανά μετά τη διόρθωση:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → επιλέξτε τον ίδιο πράκτορα → αναπτύξτε νέα έκδοση.

### Η ανάπτυξη διαρκεί πολύ

Τα κοντέινερ πολλαπλών πρακτόρων χρειάζονται περισσότερο χρόνο για εκκίνηση επειδή δημιουργούν 4 στιγμιότυπα πρακτόρων κατά την εκκίνηση. Κανονικοί χρόνοι εκκίνησης:

| Στάδιο | Αναμενόμενη διάρκεια |
|--------|---------------------|
| Δημιουργία εικόνας κοντέινερ | 1-3 λεπτά |
| Πίεση εικόνας σε ACR | 30-60 δευτερόλεπτα |
| Εκκίνηση κοντέινερ (μονός πράκτορας) | 15-30 δευτερόλεπτα |
| Εκκίνηση κοντέινερ (πολλαπλοί πράκτορες) | 30-120 δευτερόλεπτα |
| Πράκτορας διαθέσιμος στο Playground | 1-2 λεπτά μετά το "Started" |

> Αν η κατάσταση "Pending" παραμένει περισσότερο από 5 λεπτά, ελέγξτε τα αρχεία καταγραφής κοντέινερ για σφάλματα.

---

## Προβλήματα RBAC και δικαιωμάτων

### `403 Forbidden` ή `AuthorizationFailed`

Χρειάζεστε τον ρόλο **[Foundry User](https://aka.ms/foundry-ext-project-role)** στο έργο Foundry σας (προηγουμένως ονομαζόταν **Azure AI User** - το ID ρόλου παραμένει αμετάβλητο):

1. Πηγαίνετε στο [Azure Portal](https://portal.azure.com) → στο πόρο **έργου** Foundry σας.
2. Κάντε κλικ στο **Access control (IAM)** → **Role assignments**.
3. Αναζητήστε το όνομά σας → επιβεβαιώστε ότι εμφανίζεται **Foundry User** (ή η παλιά ετικέτα **Azure AI User**).
4. Εάν λείπει: **Προσθήκη** → **Add role assignment** → αναζητήστε **Foundry User** → αναθέστε στο λογαριασμό σας.

Δείτε την τεκμηρίωση [RBAC για Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) για λεπτομέρειες.

### Η ανάπτυξη μοντέλου δεν είναι προσβάσιμη

Εάν ο πράκτορας επιστρέφει σφάλματα σχετικά με το μοντέλο:

1. Επιβεβαιώστε ότι το μοντέλο έχει αναπτυχθεί: Foundry sidebar → ανοίξτε το έργο → **Models** → ελέγξτε αν `gpt-4.1-mini` (ή το μοντέλο σας) έχει κατάσταση **Succeeded**.
2. Επιβεβαιώστε ότι το όνομα ανάπτυξης ταιριάζει: συγκρίνετε το `AZURE_AI_MODEL_DEPLOYMENT_NAME` στο `.env` (ή `agent.yaml`) με το πραγματικό όνομα ανάπτυξης στο πλάι.
3. Εάν η ανάπτυξη έληξε (δωρεάν επίπεδο): αναπτύξτε ξανά από τον [Κατάλογο Μοντέλων](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Προβλήματα Foundry Local (Διαδρομή Β)

### Η υπηρεσία Foundry Local δεν τρέχει

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Σύμπτωμα | Αιτία | Διόρθωση |
|---------|-------|---------|
| Ο έλεγχος υγείας επιστρέφει `503` | Η υπηρεσία δεν ξεκίνησε | `foundry local start` ή κάντε κλικ στο **Start** στο Foundry Toolkit sidebar |
| Ο έλεγχος υγείας ξεπερνά τον χρόνο | Το μοντέλο φορτώνει ακόμα | Περιμένετε 30–60 δευτερόλεπτα μετά την εκκίνηση; τα μεγαλύτερα μοντέλα χρειάζονται περισσότερο χρόνο |
| `StatusCode: 404` στο `/v1/health` | Λάθος θύρα | Η προεπιλογή είναι `5273`. Ελέγξτε `foundry local status` για την πραγματική θύρα |
| Ανεπαρκείς πόροι | Το Foundry Local χρειάζεται ~4 GB RAM ελεύθερη | Κλείστε άλλες εφαρμογές |
| Η λήψη μοντέλου αποτυγχάνει | Χαμηλός χώρος δίσκου | Τα μοντέλα είναι 2–8 GB. Ελευθερώστε χώρο και μετά `foundry model pull <name>` |

### Ασυμφωνία ονόματος μοντέλου

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Ορίστε το `AZURE_AI_MODEL_DEPLOYMENT_NAME` στο `.env` στην ακριβή ψευδωνυμία που εμφανίζεται (π.χ., `phi-4-mini`, όχι `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` σε τοπική εκτέλεση (Διαδρομή Β)

Το `main.py` του εργαστηρίου χρησιμοποιεί `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Το Foundry Local απαιτεί αυτή τη μεταβλητή να δείχνει στην τοπική υπηρεσία - **όχι** στο `AZURE_AI_PROJECT_ENDPOINT`. Βεβαιωθείτε ότι το `.env` σας περιέχει:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Το εργαλείο MCP εξακολουθεί να κάνει εξερχόμενη κλήση (Διαδρομή Β)

Αυτό είναι αναμενόμενο. Το εργαλείο `search_microsoft_learn_for_plan` αντλεί πόρους μάθησης από `https://learn.microsoft.com/api/mcp`. **Μόνο το ερώτημα με το όνομα δεξιότητας** ταξιδεύει στο δίκτυο - το βιογραφικό και το κείμενο JD επεξεργάζονται πλήρως στη συσκευή σας και δεν μεταδίδονται ποτέ. Εάν απαιτείται πλήρης λειτουργία εκτός σύνδεσης, προσθέστε μια εναλλακτική `try/except` στο εργαλείο που επιστρέφει μια στατική `learn.microsoft.com` URL όταν το endpoint δεν είναι προσβάσιμο.

---

## Ζήτηση βοήθειας

Εάν κολλήσετε αφού δοκιμάσετε τις παραπάνω διορθώσεις:

1. **Ελέγξτε τα αρχεία καταγραφής του διακομιστή** - Τα περισσότερα σφάλματα παράγουν Python stack trace στο τερματικό. Διαβάστε ολόκληρο το traceback.
2. **Αναζητήστε το μήνυμα σφάλματος** - Αντιγράψτε το κείμενο σφάλματος και αναζητήστε στο [Microsoft Q&A για Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Ανοίξτε ένα ζήτημα** - Καταχωρίστε ένα ζήτημα στο [αποθετήριο του εργαστηρίου](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) με:
   - Το μήνυμα σφάλματος ή στιγμιότυπο οθόνης
   - Τις εκδόσεις των πακέτων σας (`pip list | Select-String "agent-framework"`)
   - Την έκδοση Python σας (`python --version`)
   - Εάν το πρόβλημα είναι τοπικό ή μετά την ανάπτυξη

---

### Σημείο ελέγχου

- [ ] Γνωρίζετε πώς να ελέγχετε και να διορθώνετε προβλήματα ρύθμισης `.env`
- [ ] Μπορείτε να επαληθεύσετε ότι οι εκδόσεις πακέτων ταιριάζουν με τον απαιτούμενο πίνακα
- [ ] Γνωρίζετε πώς να ελέγχετε αρχεία καταγραφής κοντέινερ για αποτυχίες ανάπτυξης
- [ ] Μπορείτε να επαληθεύσετε ρόλους RBAC στο Azure Portal

---

**Προηγούμενο:** [07 - Επαλήθευση στο Playground](07-verify-in-playground.md) · **Επόμενο:** [09 - Περίληψη →](09-summary.md) · **Αρχική:** [Lab 02 README](../README.md) · [Αρχική εργαστηρίου](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Αποποίηση ευθυνών**:
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία μετάφρασης με τεχνητή νοημοσύνη [Co-op Translator](https://github.com/Azure/co-op-translator). Ενώ επιδιώκουμε την ακρίβεια, παρακαλούμε να έχετε υπόψη ότι οι αυτοματοποιημένες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->