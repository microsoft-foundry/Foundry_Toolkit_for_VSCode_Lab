# Module 8 - Dépannage (Multi-Agent)

Ce module couvre les erreurs courantes, les corrections et les stratégies de débogage spécifiques au flux de travail multi-agent. Pour les problèmes généraux de déploiement Foundry, consultez également le [guide de dépannage du laboratoire 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Référence rapide : Erreur → Correction

| Erreur / Symptôme | Cause probable | Correction |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Fichier `.env` manquant ou valeurs non définies | Créez `.env` avec `PROJECT_ENDPOINT=<votre-endpoint>` et `MODEL_DEPLOYMENT_NAME=<votre-modèle>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Environnement virtuel non activé ou dépendances non installées | Exécutez `.\.venv\Scripts\Activate.ps1` puis `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Package MCP non installé (manquant dans requirements) | Exécutez `pip install mcp` ou vérifiez que `requirements.txt` l'inclut comme dépendance transitive |
| L'agent démarre mais retourne une réponse vide | `output_executors` non conforme ou bords manquants | Vérifiez `output_executors=[gap_analyzer]` et que tous les bords existent dans `create_workflow()` |
| Une seule carte de lacune (les autres manquent) | Instructions GapAnalyzer incomplètes | Ajoutez le paragraphe `CRITICAL:` à `GAP_ANALYZER_INSTRUCTIONS` - voir [Module 3](03-configure-agents.md) |
| Le score d'ajustement est 0 ou absent | MatchingAgent n'a pas reçu de données en amont | Vérifiez que `add_edge(resume_parser, matching_agent)` et `add_edge(jd_agent, matching_agent)` existent |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Le serveur MCP a rejeté l'appel de l’outil | Vérifiez la connectivité internet. Essayez d’ouvrir `https://learn.microsoft.com/api/mcp` dans un navigateur. Réessayez |
| Pas d'URL Microsoft Learn dans la sortie | Outil MCP non enregistré ou point de terminaison incorrect | Vérifiez `tools=[search_microsoft_learn_for_plan]` sur GapAnalyzer et que `MICROSOFT_LEARN_MCP_ENDPOINT` est correct |
| `Address already in use: port 8088` | Un autre processus utilise le port 8088 | Exécutez `netstat -ano \| findstr :8088` (Windows) ou `lsof -i :8088` (macOS/Linux) et stoppez le processus en conflit |
| `Address already in use: port 5679` | Conflit sur le port Debugpy | Arrêtez les autres sessions de débogage. Exécutez `netstat -ano \| findstr :5679` pour trouver et tuer le processus |
| L'Agent Inspector ne s'ouvre pas | Serveur pas entièrement démarré ou conflit de port | Attendez le log "Server running". Vérifiez que le port 5679 est libre |
| `azure.identity.CredentialUnavailableError` | Non connecté à Azure CLI | Exécutez `az login` puis redémarrez le serveur |
| `azure.core.exceptions.ResourceNotFoundError` | Le déploiement du modèle n'existe pas | Vérifiez que `MODEL_DEPLOYMENT_NAME` correspond à un modèle déployé dans votre projet Foundry |
| Statut du conteneur "Failed" après déploiement | Plantage du conteneur au démarrage | Consultez les logs du conteneur dans la barre latérale Foundry. Commun : variable d’environnement manquante ou erreur d’import |
| Déploiement affiché "Pending" pendant plus de 5 minutes | Conteneur prend trop de temps à démarrer ou limites de ressources | Attendez jusqu'à 5 minutes pour multi-agent (création de 4 instances d’agents). Si toujours en attente, vérifiez les logs |
| `ValueError` provenant de `WorkflowBuilder` | Configuration du graphe invalide | Assurez-vous que `start_executor` est défini, `output_executors` est une liste, et qu’il n’y a pas de cycles |

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

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Trouver votre PROJECT_ENDPOINT :** 
- Ouvrez la barre latérale **Microsoft Foundry** dans VS Code → clic droit sur votre projet → **Copier le point de terminaison du projet**.
- Ou allez dans [Azure Portal](https://portal.azure.com) → votre projet Foundry → **Vue d'ensemble** → **Point de terminaison du projet**.

> **Trouver votre MODEL_DEPLOYMENT_NAME :** Dans la barre latérale Foundry, développez votre projet → **Modèles** → trouvez le nom de votre modèle déployé (ex : `gpt-4.1-mini`).

### Priorité des variables d’environnement

`main.py` utilise `load_dotenv(override=False)`, ce qui signifie :

| Priorité | Source | Est-ce que ça prévaut si les deux sont définis ? |
|----------|--------|------------------------------------------------|
| 1 (plus haute) | Variable d’environnement shell | Oui |
| 2 | Fichier `.env` | Seulement si la variable shell n’est pas définie |

Cela signifie que les variables d’environnement runtime Foundry (définies via `agent.yaml`) ont la priorité sur les valeurs `.env` lors du déploiement hébergé.

---

## Compatibilité des versions

### Matrice des versions des packages

Le flux multi-agent requiert des versions spécifiques de packages. Des versions non correspondantes causent des erreurs à l’exécution.

| Package | Version requise | Commande de vérification |
|---------|-----------------|-------------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | dernière pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Erreurs courantes de version

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Correction : mise à niveau vers rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` introuvable ou Inspector incompatible :**

```powershell
# Correction : installer avec l'option --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Correction : mise à jour du paquet mcp
pip install mcp --upgrade
```

### Vérification simultanée de toutes les versions

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Sortie attendue :

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

## Problèmes avec l’outil MCP

### L’outil MCP ne retourne aucun résultat

**Symptôme :** Les cartes de lacune indiquent "No results returned from Microsoft Learn MCP" ou "No direct Microsoft Learn results found".

**Causes possibles :**

1. **Problème réseau** - Le point de terminaison MCP (`https://learn.microsoft.com/api/mcp`) est inaccessible.
   ```powershell
   # Tester la connectivité
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Si cela retourne `200`, le point de terminaison est accessible.

2. **Requête trop spécifique** - Le nom de compétence est trop pointu pour la recherche Microsoft Learn.
   - C’est attendu pour des compétences très spécialisées. L’outil fournit une URL de secours dans la réponse.

3. **Expiration de session MCP** - La connexion HTTP Streamable a expiré.
   - Réessayez la requête. Les sessions MCP sont éphémères et peuvent nécessiter une reconnexion.

### Explication des journaux MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Journal | Signification | Action |
|-----|---------|--------|
| `GET → 405` | Probes du client MCP lors de l’initialisation | Normal - ignorer |
| `POST → 200` | Appel d’outil réussi | Attendu |
| `DELETE → 405` | Probes du client MCP lors du nettoyage | Normal - ignorer |
| `POST → 400` | Mauvaise requête (requête mal formée) | Vérifiez le paramètre `query` dans `search_microsoft_learn_for_plan()` |
| `POST → 429` | Limite de fréquence atteinte | Attendez et réessayez. Réduisez le paramètre `max_results` |
| `POST → 500` | Erreur serveur MCP | Transitoire - réessayez. Si persistant, l’API MCP Microsoft Learn est peut-être indisponible |
| Délai de connexion expiré | Problème réseau ou serveur MCP indisponible | Vérifiez internet. Essayez `curl https://learn.microsoft.com/api/mcp` |

---

## Problèmes de déploiement

### Le conteneur ne démarre pas après déploiement

1. **Vérifiez les logs du conteneur :**
   - Ouvrez la barre latérale **Microsoft Foundry** → développez **Agents hébergés (Preview)** → cliquez sur votre agent → développez la version → **Détails du conteneur** → **Journaux**.
   - Recherchez des traces Python ou des erreurs de module manquant.

2. **Échecs courants au démarrage du conteneur :**

   | Erreur dans les logs | Cause | Correction |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Package manquant dans `requirements.txt` | Ajoutez le package, redéployez |
   | `RuntimeError: Missing required environment variable` | Variables d’environnement dans `agent.yaml` non définies | Mettez à jour la section `environment_variables` de `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity non configurée | Foundry le configure automatiquement - assurez-vous de déployer via l’extension |
   | `OSError: port 8088 already in use` | Dockerfile expose un mauvais port ou conflit de port | Vérifiez `EXPOSE 8088` dans Dockerfile et `CMD ["python", "main.py"]` |
   | Conteneur sort avec le code 1 | Exception non gérée dans `main()` | Testez localement d’abord ([Module 5](05-test-locally.md)) pour détecter les erreurs avant déploiement |

3. **Redéployez après correction :**
   - `Ctrl+Shift+P` → **Microsoft Foundry : Déployer l’agent hébergé** → sélectionnez le même agent → déployez une nouvelle version.

### Le déploiement prend trop de temps

Les conteneurs multi-agent mettent plus de temps à démarrer car ils créent 4 instances d'agents au démarrage. Temps de démarrage normaux :

| Étape | Durée attendue |
|-------|------------------|
| Build de l’image conteneur | 1-3 minutes |
| Push de l’image vers ACR | 30-60 secondes |
| Démarrage du conteneur (agent unique) | 15-30 secondes |
| Démarrage du conteneur (multi-agent) | 30-120 secondes |
| Agent disponible dans Playground | 1-2 minutes après "Started" |

> Si le statut "Pending" persiste au-delà de 5 minutes, vérifiez les logs du conteneur pour des erreurs.

---

## Problèmes RBAC et d’autorisations

### `403 Forbidden` ou `AuthorizationFailed`

Vous avez besoin du rôle **[Azure AI User](https://aka.ms/foundry-ext-project-role)** sur votre projet Foundry :

1. Allez dans [Azure Portal](https://portal.azure.com) → votre ressource **projet** Foundry.
2. Cliquez sur **Contrôle d’accès (IAM)** → **Attributions de rôles**.
3. Recherchez votre nom → confirmez que **Azure AI User** est listé.
4. Si absent : **Ajouter** → **Ajouter une attribution de rôle** → recherchez **Azure AI User** → assignez à votre compte.

Voir la documentation [RBAC pour Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) pour plus de détails.

### Déploiement modèle inaccessible

Si l’agent retourne des erreurs liées au modèle :

1. Vérifiez que le modèle est déployé : barre latérale Foundry → développez projet → **Modèles** → vérifiez que `gpt-4.1-mini` (ou votre modèle) a le statut **Succeeded**.
2. Vérifiez que le nom du déploiement correspond : comparez `MODEL_DEPLOYMENT_NAME` dans `.env` (ou `agent.yaml`) avec le nom réel du déploiement dans la barre latérale.
3. Si le déploiement a expiré (offre gratuite) : redéployez depuis le [Catalogue des modèles](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry : Ouvrir le catalogue des modèles**).

---

## Problèmes avec Agent Inspector

### L’Inspector s’ouvre mais affiche "Disconnected"

1. Vérifiez que le serveur tourne : cherchez "Server running on http://localhost:8088" dans le terminal.
2. Vérifiez le port `5679` : l’Inspector se connecte via debugpy sur le port 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Redémarrez le serveur et rouvrez l’Inspector.

### L’Inspector affiche une réponse partielle

Les réponses multi-agent sont longues et s’acheminent par flux incrémentaux. Attendez la réponse complète (cela peut prendre 30-60 secondes selon le nombre de cartes de lacune et d’appels à l’outil MCP).

Si la réponse est systématiquement tronquée :
- Vérifiez que les instructions de GapAnalyzer contiennent le bloc `CRITICAL:` qui empêche la combinaison des cartes de lacune.
- Vérifiez la limite de tokens de votre modèle - `gpt-4.1-mini` supporte jusqu’à 32K tokens en sortie, ce qui devrait suffire.

---

## Conseils de performance

### Réponses lentes

Les workflows multi-agent sont intrinsèquement plus lents que single-agent à cause des dépendances séquentielles et des appels à l’outil MCP.

| Optimisation | Comment | Impact |
|-------------|-----|--------|
| Réduire les appels MCP | Diminuer le paramètre `max_results` dans l’outil | Moins de requêtes HTTP |
| Simplifier les instructions | Prompts d’agent plus courts et ciblés | Inférence LLM plus rapide |
| Utiliser `gpt-4.1-mini` | Plus rapide que `gpt-4.1` pour le développement | ~2x gain de vitesse |
| Réduire la précision des cartes de lacune | Simplifier le format des cartes dans les instructions GapAnalyzer | Moins de sortie à générer |

### Temps de réponse typiques (local)

| Configuration | Temps attendu |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 cartes de lacune | 30-60 secondes |
| `gpt-4.1-mini`, 8+ cartes de lacune | 60-120 secondes |
| `gpt-4.1`, 3-5 cartes de lacune | 60-120 secondes |
---

## Obtenir de l'aide

Si vous êtes bloqué après avoir essayé les correctifs ci-dessus :

1. **Vérifiez les journaux du serveur** - La plupart des erreurs produisent une trace de la pile Python dans le terminal. Lisez la trace complète.
2. **Recherchez le message d'erreur** - Copiez le texte de l'erreur et cherchez-le dans le [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Ouvrez un ticket** - Ouvrez un ticket dans le [dépôt de l’atelier](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) avec :
   - Le message d'erreur ou une capture d’écran
   - Les versions de vos paquets (`pip list | Select-String "agent-framework"`)
   - Votre version de Python (`python --version`)
   - Si le problème est local ou après déploiement

---

### Liste de contrôle

- [ ] Vous savez identifier et corriger les erreurs les plus courantes liées aux agents multiples en utilisant le tableau de référence rapide
- [ ] Vous savez comment vérifier et corriger les problèmes de configuration du fichier `.env`
- [ ] Vous pouvez vérifier que les versions des paquets correspondent à la matrice requise
- [ ] Vous comprenez les entrées des journaux MCP et pouvez diagnostiquer les pannes des outils
- [ ] Vous savez comment vérifier les journaux des conteneurs en cas d’échec de déploiement
- [ ] Vous pouvez vérifier les rôles RBAC dans le portail Azure

---

**Précédent :** [07 - Vérifier dans Playground](07-verify-in-playground.md) · **Accueil :** [Lab 02 README](../README.md) · [Accueil de l’atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :  
Ce document a été traduit à l’aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d’assurer l’exactitude, veuillez noter que les traductions automatiques peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant foi. Pour les informations essentielles, une traduction professionnelle réalisée par un humain est recommandée. Nous déclinons toute responsabilité en cas de malentendus ou de mauvaises interprétations résultant de l’utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->