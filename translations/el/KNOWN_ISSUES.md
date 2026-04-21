# Γνωστά Ζητήματα

Αυτό το έγγραφο παρακολουθεί τα γνωστά ζητήματα με την τρέχουσα κατάσταση του αποθετηρίου.

> Τελευταία ενημέρωση: 2026-04-15. Δοκιμάστηκε με Python 3.13 / Windows στο `.venv_ga_test`.

---

## Τρέχουσες Καρφίτσες Πακέτων (και οι τρεις πράκτορες)

| Package | Current Version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(διορθώθηκε — δείτε KI-003)* |

---

## KI-001 — Αποκλεισμός Αναβάθμισης GA 1.0.0: Αφαιρέθηκε το `agent-framework-azure-ai`

**Κατάσταση:** Ανοιχτό | **Σοβαρότητα:** 🔴 Υψηλή | **Τύπος:** Διακοπή

### Περιγραφή

Το πακέτο `agent-framework-azure-ai` (καρφιτσωμένο στο `1.0.0rc3`) **αφαιρέθηκε/αποσύρθηκε**
στην κυκλοφορία GA (1.0.0, κυκλοφόρησε 2026-04-02). Αντικαθίσταται από:

- `agent-framework-foundry==1.0.0` — Πρότυπο πράκτορα φιλοξενούμενο στο Foundry
- `agent-framework-openai==1.0.0` — Πρότυπο πράκτορα με υποστήριξη OpenAI

Όλα τα τρία αρχεία `main.py` εισάγουν το `AzureAIAgentClient` από `agent_framework.azure`, το οποίο
προκαλεί `ImportError` με τα πακέτα GA. Το namespace `agent_framework.azure` εξακολουθεί να υπάρχει
στο GA αλλά τώρα περιέχει μόνο κλάσεις Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — όχι πράκτορες Foundry.

### Επιβεβαιωμένο σφάλμα (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Αρχεία που επηρεάζονται

| Αρχείο | Γραμμή |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Μη Συμβατό με το GA `agent-framework-core`

**Κατάσταση:** Ανοιχτό | **Σοβαρότητα:** 🔴 Υψηλή | **Τύπος:** Διακοπή (εξαρτάται από upstream)

### Περιγραφή

Το `azure-ai-agentserver-agentframework==1.0.0b17` (τελευταία έκδοση) καρφιτσώνει
αυστηρά το `agent-framework-core<=1.0.0rc3`. Η εγκατάστασή του παράλληλα με το `agent-framework-core==1.0.0` (GA)
αναγκάζει το pip να **υποβαθμίσει** το `agent-framework-core` πίσω στην `rc3`, κάτι που στη συνέχεια σπάει
τα `agent-framework-foundry==1.0.0` και `agent-framework-openai==1.0.0`.

Η κλήση `from azure.ai.agentserver.agentframework import from_agent_framework` που χρησιμοποιούν όλοι
οι πράκτορες για να δεσμεύσουν τον HTTP server μπλοκάρεται κι αυτή.

### Επιβεβαιωμένη σύγκρουση εξαρτήσεων (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Αρχεία που επηρεάζονται

Όλα τα τρία αρχεία `main.py` — τόσο η εισαγωγή στην κορυφή όσο και η εισαγωγή μέσα στη συνάρτηση `main()`.

---

## KI-003 — Δεν Απαιτείται Πλέον το Σημάδι `agent-dev-cli --pre`

**Κατάσταση:** ✅ Διορθώθηκε (χωρίς διακοπή) | **Σοβαρότητα:** 🟢 Χαμηλή

### Περιγραφή

Όλα τα αρχεία `requirements.txt` πριν περιελάμβαναν το `agent-dev-cli --pre` για να τραβήξουν
την προ-κυκλοφορία του CLI. Από την κυκλοφορία GA 1.0.0 στις 2026-04-02, η σταθερή έκδοση του
`agent-dev-cli` είναι πλέον διαθέσιμη χωρίς την παράμετρο `--pre`.

**Εφαρμοσμένη διόρθωση:** Η παράμετρος `--pre` αφαιρέθηκε από όλα τα τρία αρχεία `requirements.txt`.

---

## KI-004 — Τα Dockerfiles Χρησιμοποιούν το `python:3.14-slim` (Εικόνα Βάσης Προ-κυκλοφορίας)

**Κατάσταση:** Ανοιχτό | **Σοβαρότητα:** 🟡 Χαμηλή

### Περιγραφή

Όλα τα `Dockerfile` χρησιμοποιούν το `FROM python:3.14-slim` που παρακολουθεί μια προ-κυκλοφορία Python.
Για παραγωγικές αναπτύξεις θα πρέπει να καρφιτσώνεται σε σταθερή έκδοση (π.χ., `python:3.12-slim`).

### Αρχεία που επηρεάζονται

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Αναφορές

- [agent-framework-core στο PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry στο PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Αποποίηση ευθυνών**:  
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία μετάφρασης AI [Co-op Translator](https://github.com/Azure/co-op-translator). Παρόλο που επιδιώκουμε ακρίβεια, παρακαλούμε να λάβετε υπόψη ότι οι αυτοματοποιημένες μεταφράσεις μπορεί να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για οποιεσδήποτε παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->