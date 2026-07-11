# Module 8 - Dépannage

Ce module couvre les erreurs courantes, les corrections et les stratégies de débogage spécifiques au flux de travail multi-agent.

## Problèmes de sortie des agents

### GapAnalyzer indique « Je n’ai toujours pas le rapport de correspondance »

**Symptôme :** La réponse de GapAnalyzer vous demande de coller un rapport de correspondance avec les « Compétences manquantes » et les « Lacunes de certification ». Cela se produit même lorsque vous avez envoyé à la fois un CV et une description de poste.

**Cause :** Le texte de la description de poste (JD) n’a pas été transmis en aval à l’agent JD. Avec `context_mode="last_agent"`, `resume_executor` est le seul exécuteur à voir le message original de l’utilisateur. Si `RESUME_PARSER_INSTRUCTIONS` n’inclut pas le texte JD dans sa sortie, l’agent JD n’a pas de JD à analyser, MatchingAgent ne peut pas calculer le score de correspondance, et GapAnalyzer reçoit une entrée dénuée de sens.

**Diagnostic :**

Dans les journaux du serveur, recherchez la portée MatchingAgent. Si elle contient :
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
le passage est manquant ou cassé.

**Correction :** Confirmez que `RESUME_PARSER_INSTRUCTIONS` dans `main.py` contient une section `[JOB DESCRIPTION PASS-THROUGH]` et la règle :
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Confirmez également que `JOB_DESCRIPTION_INSTRUCTIONS` contient une règle relais `[PARSED RESUME PASS-THROUGH]` :
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Si l’un des blocs d’instructions est un modèle incomplet du générateur de squelette, remplacez-le par la version complète provenant de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent affiche « Impossible de calculer le score de correspondance - pas de JD fourni »

Il s’agit de la même cause racine que ci-dessus. MatchingAgent a reçu la sortie de l’agent JD mais la section `[PARSED RESUME PASS-THROUGH]` était manquante ou vide, il n’a donc pas pu comparer les deux profils. Vérifiez :
1. `JOB_DESCRIPTION_INSTRUCTIONS` inclut la règle relais : `Copier [PARSED RESUME] mot pour mot - Matching Agent en dépend en aval.`
2. `MATCHING_AGENT_INSTRUCTIONS` indique à l’agent de rechercher les sections `[JD REQUIREMENTS]` et `[PARSED RESUME PASS-THROUGH]`.

Remplacez les deux blocs d’instructions par les versions complètes de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### La réponse apparaît deux fois

**Symptôme :** La sortie de GapAnalyzer (ou la sortie complète du pipeline) apparaît deux fois dans la réponse de l’inspecteur d’agents.

**Cause :** `WorkflowBuilder` utilise une sémantique OU pour les arêtes entrantes - un exécuteur en aval se déclenche dès qu’**un** prédécesseur termine. Si `matching_executor` a deux arêtes entrantes (une de `resume_executor` et une de `jd_executor`), il se déclenche deux fois : une fois lorsque ResumeParser termine et une fois lorsque JD Agent termine. GapAnalyzer s’exécute alors aussi deux fois.

**Correction :** Assurez-vous que le graphe `WorkflowBuilder` est un pipeline strictement séquentiel sans jonction (fan-in) :

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # PAS de resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Si vous avez une ligne isolée `.add_edge(resume_executor, matching_executor)`, supprimez-la. Le relais `[PARSED RESUME PASS-THROUGH]` dans la sortie de JD Agent donne déjà à MatchingAgent l’accès au CV.

---

## Problèmes d’environnement et de configuration

### Valeurs `.env` manquantes ou incorrectes

Le fichier `.env` doit être dans le répertoire `PersonalCareerCopilot/` (au même niveau que `main.py`) :

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Contenu attendu du `.env` :

**Chemin A - Foundry cloud :**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Chemin B - Foundry Local :**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Les deux chemins utilisent `FOUNDRY_PROJECT_ENDPOINT`. La valeur diffère : le cloud utilise un endpoint Foundry en `https://` ; le local utilise `http://localhost:5273/v1`. Exécutez `foundry model list` pour confirmer l’alias exact du modèle pour le Chemin B.

> **Pour trouver votre `FOUNDRY_PROJECT_ENDPOINT` :** 
- Ouvrez la barre latérale **Foundry Toolkit** dans VS Code → clic droit sur votre projet → **Copier l’endpoint du projet**. 
- Ou allez sur [Azure Portal](https://portal.azure.com) → votre projet Foundry → **Présentation** → **Endpoint du projet**.

> **Pour trouver votre `AZURE_AI_MODEL_DEPLOYMENT_NAME` :** Dans la barre latérale Foundry Toolkit, développez votre projet → **Modèles** → trouvez le nom de votre modèle déployé (ex. `gpt-4.1-mini`).

### Priorité des variables d’environnement

`main.py` utilise `load_dotenv(override=True)`, ce qui signifie :

| Priorité | Source | Prime en cas de doublon ? |
|----------|--------|-------------------------|
| 1 (la plus haute) | Fichier `.env` | Oui |
| 2 | Variable d'environnement shell / conteneur | Utilisée si la clé est absente dans `.env` |

En développement local, cela fait du `.env` la source de vérité (édition immédiate prend effet lors des exécutions). En déploiement hébergé, Foundry injecte les variables à l’échelle du conteneur ; comme `.env` ne fait pas partie de l’image déployée pour ce laboratoire, les valeurs injectées du conteneur sont utilisées.

---

## Compatibilité des versions

### Matrice des versions des packages

Le flux multi-agent requiert des versions spécifiques de paquets. Des versions non correspondantes provoquent des erreurs en runtime.

| Package | Version requise | Commande de vérification |
|---------|-----------------|-------------------------|
| `agent-framework-foundry` | dernière | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | dernière | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | dernière | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Erreurs courantes de version

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Correction : réinstaller agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Correction : mise à niveau du paquet mcp
pip install mcp --upgrade
```

### Vérifier toutes les versions d’un coup

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
   - Ouvrez la barre latérale **Foundry Toolkit** → développez **Agents hébergés (aperçu)** → cliquez sur votre agent → développez la version → **Détails du conteneur** → **Journaux**.
   - Recherchez des traces de pile Python ou des erreurs de module manquant.

2. **Échecs courants de démarrage du conteneur :**

   | Erreur dans les journaux | Cause | Correction |
   |-------------------------|-------|------------|
   | `ModuleNotFoundError` | `requirements.txt` manque un paquet | Ajoutez le paquet, redéployez |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variables env dans `agent.yaml` ou `.env` non définies | Mettez à jour la section `environment_variables` de `agent.yaml` (hébergé) ou `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity non configurée | Foundry le configure automatiquement - assurez-vous de déployer via l’extension |
   | `OSError: port 8088 already in use` | Dockerfile expose un mauvais port ou conflit de port | Vérifiez `EXPOSE 8088` dans Dockerfile et `CMD ["python", "main.py"]` |
   | Conteneur quitte avec le code 1 | Exception non gérée dans `main()` | Testez localement d’abord ([Module 5](05-test-locally.md)) pour attraper les erreurs avant déploiement |

3. **Redéployez après correction :**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → sélectionnez le même agent → déployez une nouvelle version.

### Le déploiement prend trop de temps

Les conteneurs multi-agents prennent plus de temps à démarrer car ils créent 4 instances d’agent au démarrage. Délais normaux :

| Étape | Durée attendue |
|--------|---------------|
| Construction de l’image du conteneur | 1-3 minutes |
| Poussée de l’image vers ACR | 30-60 secondes |
| Démarrage du conteneur (agent unique) | 15-30 secondes |
| Démarrage du conteneur (multi-agent) | 30-120 secondes |
| Agent disponible dans Playground | 1-2 minutes après "Démarré" |

> Si le statut "En attente" persiste au-delà de 5 minutes, vérifiez les journaux du conteneur pour des erreurs.

---

## Problèmes RBAC et d’autorisation

### `403 Forbidden` ou `AuthorizationFailed`

Vous devez avoir le rôle **[Foundry User](https://aka.ms/foundry-ext-project-role)** sur votre projet Foundry (anciennement nommé **Azure AI User** - identifiant du rôle inchangé) :

1. Rendez-vous sur [Azure Portal](https://portal.azure.com) → ressource **projet** Foundry.
2. Cliquez sur **Contrôle d’accès (IAM)** → **Attributions de rôles**.
3. Recherchez votre nom → confirmez que **Foundry User** (ou l’étiquette ancestrale **Azure AI User**) est listé.
4. Si absent : **Ajouter** → **Ajouter une attribution de rôle** → cherchez **Foundry User** → assignez-le à votre compte.

Consultez la documentation [RBAC pour Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) pour plus de détails.

### Le déploiement du modèle n’est pas accessible

Si l’agent retourne des erreurs liées au modèle :

1. Vérifiez que le modèle est déployé : barre latérale Foundry → développez le projet → **Modèles** → vérifiez la présence de `gpt-4.1-mini` (ou votre modèle) avec le statut **Réussi**.
2. Vérifiez que le nom du déploiement correspond : comparez `AZURE_AI_MODEL_DEPLOYMENT_NAME` dans `.env` (ou `agent.yaml`) avec le nom effectif dans la barre latérale.
3. Si le déploiement a expiré (offre gratuite) : redéployez depuis [Catalogue de modèles](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit : Ouvrir le catalogue de modèles**).

---

## Problèmes Foundry Local (Chemin B)

### Le service Foundry Local ne tourne pas

```powershell
# Vérifier le statut
foundry local status

# Démarrer le service s'il est arrêté
foundry local start
```

| Symptôme | Cause | Correction |
|---------|-------|-----------|
| Le contrôle de santé renvoie `503` | Service non démarré | `foundry local start` ou cliquez sur **Démarrer** dans la barre latérale Foundry Toolkit |
| Le contrôle de santé expire | Modèle en charge | Attendez 30–60 s après démarrage ; les modèles plus grands prennent plus de temps |
| `StatusCode: 404` sur `/v1/health` | Mauvais port | Le port par défaut est `5273`. Vérifiez le port réel avec `foundry local status` |
| Ressources insuffisantes | Foundry Local requiert ~4 Go de RAM libre | Fermez les autres applications |
| Échec de téléchargement du modèle | Espace disque faible | Les modèles pèsent 2 à 8 Go. Libérez de l’espace, puis `foundry model pull <nom>` |

### Nom du modèle incorrect

```powershell
# Lister les modèles téléchargés et leurs alias exacts
foundry model list
```

Définissez `AZURE_AI_MODEL_DEPLOYMENT_NAME` dans `.env` avec l’alias exact affiché (ex. `phi-4-mini`, pas `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` lors d’une exécution locale (Chemin B)

Le `main.py` du laboratoire utilise `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local exige que cette variable pointe vers le service local - **pas** `AZURE_AI_PROJECT_ENDPOINT`. Assurez-vous que votre `.env` contient :

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP fait encore un appel sortant (Chemin B)

C’est attendu. L’outil `search_microsoft_learn_for_plan` récupère des ressources d’apprentissage depuis `https://learn.microsoft.com/api/mcp`. **Seule la requête du nom de compétence** voyage sur le réseau - le texte du CV et de la description de poste est entièrement traité sur votre appareil et jamais transmis. Si un fonctionnement totalement hors ligne est requis, ajoutez un fallback `try/except` dans l’outil qui renvoie une URL statique `learn.microsoft.com` lorsque le point de terminaison est injoignable.

---

## Obtenir de l’aide

Si vous êtes bloqué après avoir essayé les corrections ci-dessus :

1. **Vérifiez les journaux du serveur** - La plupart des erreurs produisent une trace d’exception Python dans le terminal. Lisez la trace complète.
2. **Cherchez le message d’erreur** - Copiez le texte de l’erreur et recherchez dans [Microsoft Q&A pour Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Ouvrez une issue** - Créez une issue sur le [dépôt du workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) avec :
   - Le message d’erreur ou une capture d’écran
   - Vos versions des paquets (`pip list | Select-String "agent-framework"`)
   - Votre version de Python (`python --version`)
   - Si le problème est local ou après déploiement

---

### Point de contrôle

- [ ] Vous savez comment vérifier et corriger les problèmes de configuration `.env`
- [ ] Vous pouvez vérifier que les versions des paquets correspondent à la matrice requise
- [ ] Vous savez comment vérifier les journaux du conteneur en cas d’échecs de déploiement
- [ ] Vous pouvez vérifier les rôles RBAC dans le portail Azure

---

**Précédent :** [07 - Vérifier dans Playground](07-verify-in-playground.md) · **Suivant :** [09 - Résumé →](09-summary.md) · **Accueil :** [Lab 02 README](../README.md) · [Accueil du Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->