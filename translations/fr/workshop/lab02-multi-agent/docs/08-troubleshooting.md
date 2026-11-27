# Module 8 - Dépannage

Ce module couvre les erreurs courantes, les corrections et les stratégies de débogage spécifiques au workflow multi-agent.

## Problèmes de sortie des agents

### GapAnalyzer dit « Je n’ai toujours pas le rapport correspondant »

**Symptôme :** La réponse de GapAnalyzer vous demande de coller un rapport de correspondance avec les « Compétences manquantes » et les « Lacunes de certification ». Cela se produit même lorsque vous avez envoyé à la fois un CV et une description de poste.

**Cause :** Le texte JD n’a pas été transmis en aval à JD Agent. Avec `context_mode="last_agent"`, `resume_executor` est le seul exécuteur à voir le message original de l’utilisateur. Si `RESUME_PARSER_INSTRUCTIONS` n’inclut pas le texte JD dans sa sortie, JD Agent n’a pas de JD à analyser, MatchingAgent ne peut pas calculer un score de correspondance, et GapAnalyzer reçoit une entrée dénuée de sens.

**Diagnostic :**

Dans les journaux du serveur, recherchez la portée de MatchingAgent. Si elle contient :
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
le passage direct est manquant ou cassé.

**Correction :** Confirmez que `RESUME_PARSER_INSTRUCTIONS` dans `main.py` contient une section `[JOB DESCRIPTION PASS-THROUGH]` et la règle :
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Confirmez également que `JOB_DESCRIPTION_INSTRUCTIONS` contient une règle de relais `[PARSED RESUME PASS-THROUGH]` :
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Si l’un ou l’autre des blocs d’instructions est un stub provenant de l’assistant d’ossature, remplacez-le par la version complète de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent affiche « Impossible de calculer le score de correspondance - aucun JD fourni »

C’est la même cause profonde que ci-dessus. MatchingAgent a reçu la sortie de JD Agent mais la section `[PARSED RESUME PASS-THROUGH]` était manquante ou vide, il n’a donc pas pu comparer les deux profils. Confirmez :
1. `JOB_DESCRIPTION_INSTRUCTIONS` inclut la règle de relais : `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` indique à l’agent de rechercher les sections `[JD REQUIREMENTS]` et `[PARSED RESUME PASS-THROUGH]`.

Remplacez les deux blocs d’instructions par les versions complètes de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### La réponse apparaît deux fois

**Symptôme :** La sortie de GapAnalyzer (ou l’ensemble de la sortie du pipeline) apparaît deux fois dans la réponse de l’inspecteur d’agent.

**Cause :** `WorkflowBuilder` utilise une sémantique OU pour les arêtes entrantes – un exécuteur en aval s’enclenche dès que **n’importe quel** prédécesseur termine. Si `matching_executor` a deux arêtes entrantes (une de `resume_executor` et une de `jd_executor`), il s’enclenche deux fois : une fois lorsque ResumeParser termine et une autre lorsque JD Agent termine. GapAnalyzer s’exécute alors aussi deux fois.

**Correction :** Assurez-vous que le graphe `WorkflowBuilder` est un pipeline strictement séquentiel sans convergence :

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Si vous avez une ligne `.add_edge(resume_executor, matching_executor)` errante, supprimez-la. Le relais `[PARSED RESUME PASS-THROUGH]` dans la sortie de JD Agent donne déjà à MatchingAgent l’accès au CV.

---

## Problèmes d’environnement et de configuration

### Valeurs `.env` manquantes ou incorrectes

Le fichier `.env` doit se trouver dans le répertoire `PersonalCareerCopilot/` (au même niveau que `main.py`) :

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Contenu attendu de `.env` :

**Chemin A – Foundry cloud :**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Chemin B – Foundry Local :**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Les deux chemins utilisent `FOUNDRY_PROJECT_ENDPOINT`. La valeur diffère : le cloud utilise un point de terminaison Foundry `https://` ; local utilise `http://localhost:5273/v1`. Exécutez `foundry model list` pour confirmer l’alias exact du modèle pour le chemin B.

> **Trouver votre `FOUNDRY_PROJECT_ENDPOINT` :** 
- Ouvrez la barre latérale **Foundry Toolkit** dans VS Code → clic droit sur votre projet → **Copier le point de terminaison du projet**. 
- Ou allez dans [Azure Portal](https://portal.azure.com) → votre projet Foundry → **Présentation** → **Point de terminaison du projet**.

> **Trouver votre `AZURE_AI_MODEL_DEPLOYMENT_NAME` :** Dans la barre latérale Foundry Toolkit, développez votre projet → **Modèles** → trouvez le nom de votre modèle déployé (ex. `gpt-4.1-mini`).

### Priorité des variables d’environnement

`main.py` utilise `load_dotenv(override=True)`, ce qui signifie :

| Priorité | Source | Vaut quand les deux sont définis ? |
|----------|--------|-----------------------------|
| 1 (la plus haute) | Fichier `.env` | Oui |
| 2 | Variable d’environnement shell / conteneur | Utilisée quand la même clé n’est pas présente dans `.env` |

En développement local, cela fait de `.env` la source de vérité (modifier `.env` affecte immédiatement les exécutions). En déploiement hébergé, Foundry injecte les variables d’environnement au niveau du conteneur ; comme `.env` ne fait pas partie de l’image déployée pour cette configuration de laboratoire, les valeurs injectées par le conteneur sont utilisées.

---

## Compatibilité des versions

### Matrice des versions des packages

Le workflow multi-agent nécessite des versions spécifiques des packages. Des versions incompatibles causent des erreurs à l’exécution.

| Package | Version requise | Commande de vérification |
|---------|-----------------|-----------------------|
| `agent-framework-foundry` | dernière | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | dernière | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | dernière | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Erreurs communes de version

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

### Vérifier toutes les versions à la fois

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Sortie attendue :

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problèmes de déploiement

### Le conteneur ne démarre pas après le déploiement

1. **Vérifiez les journaux du conteneur :**
   - Ouvrez la barre latérale **Foundry Toolkit** → sous votre projet, cliquez sur **Agents** → onglet **Hosted Agent** → cliquez sur votre agent. Vérifiez le **Statut** dans l’onglet **Détails**, puis ouvrez l’onglet **Playground** et utilisez l’onglet **Journaux** dans le panneau **Détails de session** pour voir la sortie du conteneur.
   - Cherchez des traces de pile Python ou des erreurs de module manquant.

2. **Échecs courants au démarrage du conteneur :**

   | Erreur dans les journaux | Cause | Correction |
   |-------------------------|-------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` package manquant | Ajoutez le package, redéployez |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` ou `.env` variables d’environnement non définies | Mettez à jour `agent.yaml` → section `environment_variables` (hébergé) ou `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Identité gérée non configurée | Foundry le configure automatiquement - assurez-vous de déployer via l’extension |
   | `OSError: port 8088 already in use` | Dockerfile expose un mauvais port ou conflit de port | Vérifiez `EXPOSE 8088` dans Dockerfile et `CMD ["python", "main.py"]` |
   | Le conteneur se ferme avec le code 1 | Exception non gérée dans `main()` | Testez en local d’abord ([Module 5](05-test-locally.md)) pour détecter les erreurs avant de déployer |

3. **Redéployez après correction :**
   - `Ctrl+Shift+P` → **Foundry Toolkit : Déployer Hosted Agent** → sélectionnez le même agent → déployez une nouvelle version.

### Le déploiement prend trop de temps

Les conteneurs multi-agents prennent plus de temps à démarrer car ils créent 4 instances d’agents au démarrage. Durée normale de démarrage :

| Étape | Durée attendue |
|-------|---------------|
| Construction de l’image du conteneur | 1-3 minutes |
| Push de l’image vers ACR | 30-60 secondes |
| Démarrage du conteneur (agent unique) | 15-30 secondes |
| Démarrage du conteneur (multi-agent) | 30-120 secondes |
| Agent disponible dans Playground | 1-2 minutes après « Démarré » |

> Si le statut « En attente » persiste au-delà de 5 minutes, vérifiez les journaux du conteneur pour des erreurs.

---

## Problèmes RBAC et d’autorisation

### `403 Forbidden` ou `AuthorizationFailed`

Vous avez besoin du rôle **[Foundry User](https://aka.ms/foundry-ext-project-role)** sur votre projet Foundry (anciennement nommé **Azure AI User** – l’ID de rôle n’a pas changé) :

1. Allez dans [Azure Portal](https://portal.azure.com) → votre ressource **projet** Foundry.
2. Cliquez sur **Contrôle d’accès (IAM)** → **Attributions de rôle**.
3. Recherchez votre nom → confirmez que **Utilisateur Foundry** (ou l’étiquette héritée **Utilisateur Azure AI**) est listé.
4. En cas d’absence : **Ajouter** → **Ajouter une attribution de rôle** → recherchez **Utilisateur Foundry** → assignez-le à votre compte.

Consultez la documentation [RBAC pour Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) pour plus de détails.

### Déploiement du modèle inaccessible

Si l’agent renvoie des erreurs liées au modèle :

1. Vérifiez que le modèle est déployé : barre latérale Foundry → développez le projet → **Modèles** → cherchez `gpt-4.1-mini` (ou votre modèle) avec le statut **Réussi**.
2. Vérifiez que le nom du déploiement correspond : comparez `AZURE_AI_MODEL_DEPLOYMENT_NAME` dans `.env` (ou `agent.yaml`) avec le nom réel du déploiement dans la barre latérale.
3. Si le déploiement a expiré (niveau gratuit) : redéployez depuis le [Catalogue des modèles](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit : Ouvrir le catalogue des modèles**).

---

## Problèmes Foundry Local (Chemin B)

### Service Foundry Local non démarré

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Symptôme | Cause | Solution |
|---------|-------|---------|
| La vérification de santé retourne `503` | Service non démarré | `foundry local start` ou cliquez sur **Démarrer** dans la barre latérale Foundry Toolkit |
| La vérification de santé expire | Modèle encore en chargement | Patientez 30–60 s après le démarrage ; les gros modèles prennent plus de temps |
| `StatusCode: 404` sur `/v1/health` | Mauvais port | Par défaut `5273`. Vérifiez `foundry local status` pour connaître le port réel |
| Ressources insuffisantes | Foundry Local nécessite environ 4 Go de RAM libre | Fermez d’autres applications |
| Échec du téléchargement du modèle | Espace disque faible | Les modèles font 2 à 8 Go. Libérez de l’espace, puis `foundry model pull <name>` |

### Non-correspondance du nom du modèle

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Définissez `AZURE_AI_MODEL_DEPLOYMENT_NAME` dans `.env` à l’alias exact affiché (ex. `phi-4-mini`, et non `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` lors d'une exécution locale (Chemin B)

Le `main.py` du laboratoire utilise `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local exige que cette variable pointe vers le service local - **pas** `AZURE_AI_PROJECT_ENDPOINT`. Assurez-vous que votre `.env` contient :

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### L’outil MCP effectue toujours un appel sortant (Chemin B)

C’est normal. L’outil `search_microsoft_learn_for_plan` récupère les ressources d’apprentissage depuis `https://learn.microsoft.com/api/mcp`. **Seule la requête du nom de compétence** circule sur le réseau - le CV et le texte de la description de poste sont entièrement traités sur votre appareil et ne sont jamais transmis. Si un fonctionnement complètement hors ligne est requis, ajoutez un `try/except` de secours dans l’outil qui renvoie une URL `learn.microsoft.com` statique lorsque le point de terminaison est injoignable.

---

## Obtenir de l’aide

Si vous êtes bloqué après avoir essayé les corrections ci-dessus :

1. **Consultez les logs du serveur** - La plupart des erreurs génèrent une trace de pile Python dans le terminal. Lisez la trace complète.
2. **Recherchez le message d’erreur** - Copiez le texte de l’erreur et cherchez dans [Microsoft Q&A pour Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Ouvrez un ticket** - Créez un problème dans le [dépôt du workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) avec :
   - Le message d’erreur ou une capture d’écran
   - Vos versions de package (`pip list | Select-String "agent-framework"`)
   - Votre version Python (`python --version`)
   - Indiquez si le problème est local ou après déploiement

---

### Point de contrôle

- [ ] Vous savez comment vérifier et corriger les problèmes de configuration `.env`
- [ ] Vous pouvez vérifier que les versions des packages correspondent à la matrice requise
- [ ] Vous savez comment consulter les logs du container pour les échecs de déploiement
- [ ] Vous pouvez vérifier les rôles RBAC dans le portail Azure

---

**Précédent :** [07 - Vérifier dans Playground](07-verify-in-playground.md) · **Suivant :** [09 - Résumé →](09-summary.md) · **Accueil :** [README Lab 02](../README.md) · [Accueil Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->