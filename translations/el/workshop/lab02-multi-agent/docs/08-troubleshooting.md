# Ενότητα 8 - Επίλυση προβλημάτων

Αυτή η ενότητα καλύπτει κοινά σφάλματα, διορθώσεις και στρατηγικές αποσφαλμάτωσης ειδικές για τη ροή εργασίας με πολλούς πράκτορες.

## Προβλήματα εξόδου πράκτορα

### Ο GapAnalyzer λέει «Δεν έχω ακόμα την αντίστοιχη αναφορά»

**Σύμπτωμα:** Η απάντηση του GapAnalyzer σας ζητά να επικολλήσετε μια αντίστοιχη αναφορά με «Ελλείποντες Δεξιότητες» και «Ελλείψεις Πιστοποίησης». Αυτό συμβαίνει ακόμη και όταν στείλατε τόσο βιογραφικό όσο και περιγραφή εργασίας.

**Αιτία:** Το κείμενο της περιγραφής εργασίας (JD) δεν περάστηκε προς τα κάτω στον πράκτορα JD. Με `context_mode="last_agent"`, ο `resume_executor` είναι ο μόνος εκτελεστής που βλέπει ποτέ το αρχικό μήνυμα του χρήστη. Αν οι `RESUME_PARSER_INSTRUCTIONS` δεν περιλαμβάνουν το κείμενο της περιγραφής εργασίας στην έξοδό τους, ο πράκτορας JD δεν έχει JD να αναλύσει, ο MatchingAgent δεν μπορεί να υπολογίσει βαθμολογία αντιστοίχισης και ο GapAnalyzer λαμβάνει άσκοπη είσοδο.

**Διάγνωση:**

Στα αρχεία καταγραφής του διακομιστή, αναζητήστε το διάστημα MatchingAgent. Εάν περιέχει:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
το πέρασμα είναι ελλιπές ή κατεστραμμένο.

**Διόρθωση:** Επιβεβαιώστε ότι οι `RESUME_PARSER_INSTRUCTIONS` στο `main.py` περιέχουν μια ενότητα `[JOB DESCRIPTION PASS-THROUGH]` και τον κανόνα:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Επιβεβαιώστε επίσης ότι οι `JOB_DESCRIPTION_INSTRUCTIONS` περιέχουν έναν κανόνα ανάμεσης `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Εάν κάποιο από αυτά τα μπλοκ οδηγιών είναι υποκείμενο από τον οδηγό σκελετού, αντικαταστήστε το με την πλήρη έκδοση από το [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Ο MatchingAgent εμφανίζει το μήνυμα «Δεν μπορεί να υπολογίσει βαθμολογία αντιστοίχισης - δεν δόθηκε JD»

Αυτή είναι η ίδια βασική αιτία όπως παραπάνω. Ο MatchingAgent έλαβε την έξοδο του πράκτορα JD αλλά η ενότητα `[PARSED RESUME PASS-THROUGH]` έλειπε ή ήταν κενή, οπότε δεν μπορούσε να συγκρίνει τα δύο προφίλ. Επιβεβαιώστε:
1. Οι `JOB_DESCRIPTION_INSTRUCTIONS` περιλαμβάνουν τον κανόνα ανάμεσης: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. Οι `MATCHING_AGENT_INSTRUCTIONS` λένε στον πράκτορα να αναζητήσει τις ενότητες `[JD REQUIREMENTS]` και `[PARSED RESUME PASS-THROUGH]`.

Αντικαταστήστε και τα δύο μπλοκ οδηγιών με τις πλήρεις εκδόσεις από το [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Η απόκριση εμφανίζεται δύο φορές

**Σύμπτωμα:** Η έξοδος του GapAnalyzer (ή ολόκληρη η έξοδος του pipeline) εμφανίζεται δύο φορές στην απάντηση του Agent Inspector.

**Αιτία:** Το `WorkflowBuilder` χρησιμοποιεί λογική OR για τις εισερχόμενες άκρες - ένας εκτελεστής εκτελείται μόλις ολοκληρωθεί **οποιοσδήποτε** προκάτοχος. Αν ο `matching_executor` έχει δύο εισερχόμενες άκρες (μία από τον `resume_executor` και μία από τον `jd_executor`), ενεργοποιείται δύο φορές: μία όποτε τελειώνει ο ResumeParser και ξανά όταν τελειώνει ο JD Agent. Στη συνέχεια, ο GapAnalyzer τρέχει επίσης δύο φορές.

**Διόρθωση:** Βεβαιωθείτε ότι το γράφημα `WorkflowBuilder` είναι αυστηρά αλληλουχιακό pipeline χωρίς συγχώνευση ροών:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # ΟΧΙ από το resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Αν έχετε μια γραμμή `.add_edge(resume_executor, matching_executor)` που περιττεύει, αφαιρέστε την. Η ανάμεση `[PARSED RESUME PASS-THROUGH]` στην έξοδο του JD Agent ήδη δίνει στον MatchingAgent πρόσβαση στο βιογραφικό.

---

## Προβλήματα περιβάλλοντος και ρυθμίσεων

### Ελλείποντα ή λανθασμένα τιμές `.env`

Το αρχείο `.env` πρέπει να βρίσκεται στον κατάλογο `PersonalCareerCopilot/` (στο ίδιο επίπεδο με το `main.py`):

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

> Και οι δύο διαδρομές χρησιμοποιούν `FOUNDRY_PROJECT_ENDPOINT`. Η τιμή διαφέρει: το cloud χρησιμοποιεί έναν endpoint Foundry με `https://`, τοπικά χρησιμοποιείται `http://localhost:5273/v1`. Εκτελέστε `foundry model list` για να επιβεβαιώσετε το ακριβές ψευδώνυμο μοντέλου για τη Διαδρομή Β.

> **Εύρεση του `FOUNDRY_PROJECT_ENDPOINT`:** 
- Ανοίξτε το πλαϊνό μενού του **Foundry Toolkit** στο VS Code → δεξί κλικ στο έργο σας → **Copy Project Endpoint**. 
- Ή πηγαίνετε στο [Azure Portal](https://portal.azure.com) → το έργο Foundry σας → **Overview** → **Project endpoint**.

> **Εύρεση του `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Στο πλαϊνό μενού Foundry Toolkit, επεκτείνετε το έργο σας → **Models** → βρείτε το όνομα του αναπτυγμένου μοντέλου σας (π.χ., `gpt-4.1-mini`).

### Προτεραιότητα μεταβλητών περιβάλλοντος

Το `main.py` χρησιμοποιεί το `load_dotenv(override=True)`, που σημαίνει:

| Προτεραιότητα | Πηγή | Κερδίζει όταν είναι και οι δύο ορισμένες; |
|----------|--------|------------------------|
| 1 (η υψηλότερη) | Αρχείο `.env` | Ναι |
| 2 | Μεταβλητή περιβάλλοντος του shell / container | Χρησιμοποιείται αν το ίδιο κλειδί δεν είναι παρόν στο `.env` |

Στην τοπική ανάπτυξη, αυτό κάνει το `.env` την πηγή της αλήθειας (η επεξεργασία του `.env` επηρεάζει άμεσα τις εκτελέσεις). Σε φιλοξενούμενη ανάπτυξη, το Foundry εγχέει μεταβλητές περιβάλλοντος σε επίπεδο container· δεδομένου ότι το `.env` δεν αποτελεί μέρος της αναπτυγμένης εικόνας για αυτή τη ρύθμιση εργαστηρίου, χρησιμοποιούνται οι εγχέονται τιμές container.

---

## Συμβατότητα έκδοσης

### Μήτρα εκδόσεων πακέτων

Η ροή εργασίας με πολλούς πράκτορες απαιτεί συγκεκριμένες εκδόσεις πακέτων. Οι ασυμβίβαστες εκδόσεις προκαλούν σφάλματα κατά την εκτέλεση.

| Πακέτο | Απαιτούμενη Έκδοση | Εντολή για έλεγχο |
|---------|-----------------|---------------|
| `agent-framework-foundry` | πιο πρόσφατη | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | πιο πρόσφατη | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | πιο πρόσφατη | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Συνηθισμένα σφάλματα έκδοσης

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Διόρθωση: επανεγκατάσταση του agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Διόρθωση: ενημέρωση του πακέτου mcp
pip install mcp --upgrade
```

### Επαλήθευση όλων των εκδόσεων ταυτόχρονα

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Αναμενόμενη έξοδος:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Προβλήματα ανάπτυξης

### Ο container αποτυγχάνει να ξεκινήσει μετά την ανάπτυξη

1. **Ελέγξτε τα αρχεία καταγραφής του container:**
   - Ανοίξτε το πλαϊνό μενού **Foundry Toolkit** → επεκτείνετε το **Hosted Agents (Preview)** → κάντε κλικ στον πράκτορά σας → επεκτείνετε την έκδοση → **Container Details** → **Logs**.
   - Αναζητήστε Python stack traces ή σφάλματα απουσίας modules.

2. **Συνηθισμένοι λόγοι αποτυχίας εκκίνησης container:**

   | Σφάλμα στα αρχεία καταγραφής | Αιτία | Διόρθωση |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Στο `requirements.txt` λείπει ένα πακέτο | Προσθέστε το πακέτο, αναπτύξτε ξανά |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Στο `agent.yaml` ή `.env` δεν έχουν οριστεί μεταβλητές περιβάλλοντος | Ενημερώστε το `agent.yaml` → ενότητα `environment_variables` (φιλοξενούμενο) ή `.env` (τοπικό) |
   | `azure.identity.CredentialUnavailableError` | Δεν έχει ρυθμιστεί το Managed Identity | Το Foundry το ρυθμίζει αυτόματα - βεβαιωθείτε ότι αναπτύσσετε μέσω της επέκτασης |
   | `OSError: port 8088 already in use` | Στο Dockerfile εκτίθεται λάθος θύρα ή υπάρχει σύγκρουση θυρών | Ελέγξτε το `EXPOSE 8088` στο Dockerfile και την εντολή `CMD ["python", "main.py"]` |
   | O container τερματίζει με κωδικό 1 | Ανεπεξέργαστη εξαίρεση στο `main()` | Δοκιμάστε το τοπικά πρώτα ([Ενότητα 5](05-test-locally.md)) για να εντοπίσετε σφάλματα πριν αναπτύξετε |

3. **Αναπτύξτε ξανά μετά τη διόρθωση:**
   - Πατήστε `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → επιλέξτε τον ίδιο πράκτορα → αναπτύξτε νέα έκδοση.

### Η ανάπτυξη διαρκεί πολύ

Οι containers με πολλούς πράκτορες χρειάζονται περισσότερο χρόνο εκκίνησης επειδή δημιουργούν 4 στιγμιότυπα πράκτορα κατά την εκκίνηση. Οι κανονικοί χρόνοι εκκίνησης:

| Στάδιο | Εκτιμώμενη διάρκεια |
|-------|------------------|
| Κατασκευή εικόνας container | 1-3 λεπτά |
| Μεταφόρτωση εικόνας στο ACR | 30-60 δευτερόλεπτα |
| Εκκίνηση container (single agent) | 15-30 δευτερόλεπτα |
| Εκκίνηση container (multi-agent) | 30-120 δευτερόλεπτα |
| Πράκτορας διαθέσιμος στο Playground | 1-2 λεπτά μετά το «Started» |

> Αν η κατάσταση «Pending» διαρκεί πάνω από 5 λεπτά, ελέγξτε τα αρχεία καταγραφής του container για σφάλματα.

---

## Προβλήματα RBAC και δικαιωμάτων

### `403 Forbidden` ή `AuthorizationFailed`

Χρειάζεστε τον ρόλο **[Foundry User](https://aka.ms/foundry-ext-project-role)** στο έργο Foundry σας (προηγουμένως ονομαζόταν **Azure AI User** - ο ID ρόλου παραμένει ο ίδιος):

1. Μεταβείτε στο [Azure Portal](https://portal.azure.com) → στον πόρο του έργου Foundry σας.
2. Κάντε κλικ στο **Access control (IAM)** → **Role assignments**.
3. Αναζητήστε το όνομά σας → επιβεβαιώστε ότι εμφανίζεται ο ρόλος **Foundry User** (ή το παλιό όνομα **Azure AI User**).
4. Αν λείπει: **Προσθήκη** → **Προσθήκη ανάθεσης ρόλου** → αναζητήστε **Foundry User** → εκχωρήστε τον στον λογαριασμό σας.

Δείτε την τεκμηρίωση [RBAC για Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) για λεπτομέρειες.

### Η ανάπτυξη μοντέλου δεν είναι προσβάσιμη

Αν ο πράκτορας επιστρέφει σφάλματα σχετικά με το μοντέλο:

1. Επαληθεύστε ότι το μοντέλο έχει αναπτυχθεί: πλαϊνό μενού Foundry → επεκτείνετε το έργο → **Models** → ελέγξτε αν το `gpt-4.1-mini` (ή το μοντέλο σας) έχει κατάσταση **Succeeded**.
2. Επαληθεύστε ότι το όνομα ανάπτυξης ταιριάζει: συγκρίνετε το `AZURE_AI_MODEL_DEPLOYMENT_NAME` στο `.env` (ή `agent.yaml`) με το πραγματικό όνομα ανάπτυξης στο πλαϊνό μενού.
3. Αν η ανάπτυξη έληξε (δωρεάν επίπεδο): αναπτύξτε ξανά από τον [Κατάλογο Μοντέλων](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Προβλήματα Foundry Local (Διαδρομή Β)

### Η υπηρεσία Foundry Local δεν εκτελείται

```powershell
# Έλεγχος κατάστασης
foundry local status

# Ξεκινήστε την υπηρεσία αν έχει σταματήσει
foundry local start
```

| Σύμπτωμα | Αιτία | Διόρθωση |
|---------|-------|-----|
| Ο έλεγχος υγείας επιστρέφει `503` | Η υπηρεσία δεν έχει ξεκινήσει | `foundry local start` ή κάντε κλικ στο **Start** στο πλαϊνό μενού Foundry Toolkit |
| Ο έλεγχος υγείας υπερβαίνει τον χρόνο αναμονής | Το μοντέλο φορτώνει ακόμα | Περιμένετε 30–60 δευτερόλεπτα μετά την εκκίνηση· τα μεγαλύτερα μοντέλα χρειάζονται περισσότερο χρόνο |
| `StatusCode: 404` στο `/v1/health` | Λάθος θύρα | Η προεπιλεγμένη είναι η `5273`. Ελέγξτε το `foundry local status` για την πραγματική θύρα |
| Ανεπαρκείς πόροι | Το Foundry Local χρειάζεται ~4 GB ελεύθερη RAM | Κλείστε άλλες εφαρμογές |
| Αποτυχία λήψης μοντέλου | Λίγος ελεύθερος χώρος δίσκου | Τα μοντέλα είναι 2–8 GB. Απελευθερώστε χώρο, έπειτα `foundry model pull <name>` |

### Μη ταύτιση ονόματος μοντέλου

```powershell
# Λίστα των ληφθέντων μοντέλων και των ακριβών ψευδωνύμων τους
foundry model list
```

Ορίστε το `AZURE_AI_MODEL_DEPLOYMENT_NAME` στο `.env` στο ακριβές ψευδώνυμο που εμφανίζεται (π.χ., `phi-4-mini`, όχι `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` κατά το τοπικό τρέξιμο (Διαδρομή Β)

Το `main.py` του εργαστηρίου χρησιμοποιεί το `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Το Foundry Local απαιτεί αυτή τη μεταβλητή να δείχνει στην τοπική υπηρεσία - **όχι** το `AZURE_AI_PROJECT_ENDPOINT`. Βεβαιωθείτε ότι το `.env` σας περιέχει:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Το εργαλείο MCP εξακολουθεί να κάνει έξοδο δικτύου (Διαδρομή Β)

Αυτό είναι αναμενόμενο. Το εργαλείο `search_microsoft_learn_for_plan` αναζητά εκπαιδευτικούς πόρους από το `https://learn.microsoft.com/api/mcp`. **Μόνο το ερώτημα με το όνομα δεξιότητας** ταξιδεύει στο δίκτυο - το βιογραφικό και το κείμενο της περιγραφής εργασίας επεξεργάζονται πλήρως στη συσκευή σας και δεν μεταβιβάζονται. Αν απαιτείται πλήρως εκτός σύνδεσης λειτουργία, προσθέστε μια εφεδρική `try/except` στο εργαλείο που επιστρέφει ένα στατικό URL `learn.microsoft.com` όταν το endpoint δεν είναι προσβάσιμο.

---

## Λήψη βοήθειας

Αν κολλήσετε μετά τις παραπάνω προσπάθειες διόρθωσης:

1. **Ελέγξτε τα αρχεία καταγραφής του διακομιστή** - Τα περισσότερα σφάλματα παράγουν ένα Python stack trace στο τερματικό. Διαβάστε το πλήρες traceback.
2. **Αναζητήστε το μήνυμα σφάλματος** - Αντιγράψτε το κείμενο του σφάλματος και ψάξτε στο [Microsoft Q&A για Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Ανοίξτε ένα ζήτημα** - Καταθέστε ένα ζήτημα στο [αποθετήριο εργαστηρίου](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) με:
   - Το μήνυμα σφάλματος ή screenshot
   - Τις εκδόσεις των πακέτων σας (`pip list | Select-String "agent-framework"`)
   - Την έκδοση Python σας (`python --version`)
   - Αν το ζήτημα είναι τοπικό ή μετά την ανάπτυξη

---

### Σημείο ελέγχου

- [ ] Ξέρετε πώς να ελέγχετε και να διορθώνετε προβλήματα ρυθμίσεων `.env`
- [ ] Μπορείτε να επαληθεύετε ότι οι εκδόσεις πακέτων ταιριάζουν με τη απαιτούμενη μήτρα
- [ ] Ξέρετε πώς να ελέγχετε τα αρχεία καταγραφής container για αποτυχίες ανάπτυξης
- [ ] Μπορείτε να επαληθεύετε ρόλους RBAC στο Azure Portal

---

**Προηγούμενο:** [07 - Verify in Playground](07-verify-in-playground.md) · **Επόμενο:** [09 - Περίληψη →](09-summary.md) · **Αρχική:** [Lab 02 README](../README.md) · [Αρχική Εργαστηρίου](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Αποποίηση ευθυνών**:
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία μετάφρασης με τεχνητή νοημοσύνη [Co-op Translator](https://github.com/Azure/co-op-translator). Ενώ επιδιώκουμε την ακρίβεια, παρακαλούμε να έχετε υπόψη ότι οι αυτοματοποιημένες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->