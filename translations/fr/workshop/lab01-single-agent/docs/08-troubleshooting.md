# Module 8 - Dépannage

Ce module est un guide de référence pour les problèmes courants. Mettez-le en favori et revenez-y en cas de problème.

---

## 1. Erreurs de permission

### 1.1 `agents/write` permission refusée

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Cause principale :** Rôle `Azure AI User` manquant au niveau **projet**. C’est l'erreur numéro 1 de l’atelier.

**Correction :**
1. Ouvrez [portal.azure.com](https://portal.azure.com).
2. Recherchez le nom de votre **projet** Foundry → cliquez sur le résultat de type **« Microsoft Foundry project »** (PAS le compte parent).
3. **Contrôle d’accès (IAM)** → **+ Ajouter** → **Ajouter une attribution de rôle**.
4. Rôle : **Utilisateur Azure AI** → Suivant.
5. Membres : Sélectionnez-vous → Examiner + attribuer → Examiner + attribuer.
6. **Attendez 1 à 2 minutes** → réessayez.

> **Pourquoi le rôle Propriétaire/Contributeur n’est pas suffisant :** Ces rôles accordent uniquement des actions de *gestion*. Les opérations d’agent nécessitent l’`agents/write` *action sur les données*, qui se trouve uniquement dans `Azure AI User`, `Azure AI Developer`, ou `Azure AI Owner`. Voir [docs Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` lors du provisionnement

**Correction :** Demandez à votre administrateur d’attribuer **Contributeur** sur le groupe de ressources, ou qu’il crée le projet pour vous et vous accorde le rôle **Utilisateur Azure AI** dessus.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Erreurs Docker

> Docker est **optionnel**. Ces points ne s’appliquent que si Docker Desktop est installé et que l’extension tente une compilation locale.

### 2.1 Le démon Docker ne fonctionne pas

**Correction :** Démarrez Docker Desktop → attendez le statut "en cours d’exécution" → vérifiez avec `docker info` → réessayez.

### 2.2 Échec de la compilation avec erreurs de dépendances

**Correction :** Vérifiez l’orthographe de `requirements.txt`, testez localement d’abord : `pip install -r requirements.txt`.

### 2.3 Incompatibilité de plateforme (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Erreurs d’authentification

### 3.1 Échec de `DefaultAzureCredential`

**Correction (essayez dans cet ordre) :**
1. `az login` (réauthentification)
2. `az account set --subscription "<id>"` (abonnement correct)
3. VS Code → Comptes → Déconnexion → Reconnexion
4. Vérifiez : `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Le jeton fonctionne localement mais pas en hébergé

**Attendu :** Les agents hébergés utilisent une identité gérée par le système, pas vos identifiants. Si l’agent hébergé rencontre des erreurs d’authentification :
- Vérifiez que `AZURE_AI_MODEL_DEPLOYMENT_NAME` dans `agent.yaml` correspond au nom de déploiement de votre modèle (`FOUNDRY_PROJECT_ENDPOINT` est injecté par Foundry à l’exécution — ne le déclarez pas dans `agent.yaml`)
- Assurez-vous que l’identité gérée du projet a accès au modèle

---

## 4. Erreurs de modèle

### 4.1 Déploiement du modèle introuvable

**Correction :** Le nom est **sensible à la casse**. Comparez `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` avec le nom exact dans la barre latérale Foundry → Modèles.

### 4.2 Sortie du modèle inattendue

**Correction :** Examinez `AGENT_INSTRUCTIONS` dans `main.py` (pas tronqué ?). Essayez un modèle différent (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Erreurs de déploiement

### 5.1 Pull ACR non autorisé

**Correction :** Portail Azure → Registre de conteneurs → Contrôle d’accès (IAM) → Ajoutez le rôle **AcrPull** à l’identité gérée du projet Foundry.

### 5.2 L’agent ne démarre pas (reste "En attente" ou "Échec")

Consultez les logs du conteneur dans la barre latérale. Causes courantes :

| Message de log | Correction |
|-------------|------------|
| `ModuleNotFoundError` | Ajoutez le paquet manquant à `requirements.txt`, redéployez |
| `ValueError: Missing required environment variables` | Confirmez que `AZURE_AI_MODEL_DEPLOYMENT_NAME` est déclaré dans `agent.yaml` sous `environment_variables` et a une valeur, puis redéployez. `FOUNDRY_PROJECT_ENDPOINT` est injecté par Foundry à l’exécution |
| `Address already in use` | Assurez-vous qu’un seul processus écoute sur le port 8088 |

### 5.3 Le déploiement expire

**Correction :** Vérifiez la connexion internet. Le premier déploiement pousse >100Mo. Derrière un proxy ? Configurez les paramètres proxy de Docker Desktop.

---

## 6. Chemin B - Foundry Local

### 6.1 Foundry Local ne démarre pas

| Problème | Correction |
|---------|-----------|
| `foundry: command not found` | Réinstallez : `winget install Microsoft.FoundryLocal` |
| Ressources insuffisantes | Foundry Local nécessite ~4Go de RAM libres. Fermez les autres applications. |
| Échec du téléchargement du modèle | Vérifiez l’espace disque (les modèles font 2 à 8 Go). Réessayez : `foundry local models pull <name>` |

### 6.2 Erreurs de modèle Foundry Local

| Problème | Correction |
|---------|-----------|
| Réponses lentes | Attendu - les modèles locaux tournent sur CPU sauf si vous avez un GPU. Soyez patient. |
| Sortie de mauvaise qualité | Essayez un modèle plus grand si votre matériel le permet. `phi-4-mini` est un bon compromis. |
| Connexion refusée | Vérifiez que Foundry Local est en cours : `foundry local status`. Redémarrez si nécessaire. |

---

## 7. Référence rapide : rôles RBAC

| Rôle | Portée | Attributions |
|------|--------|-------------|
| **Utilisateur Azure AI** | Projet | Actions sur les données : `agents/write`, `agents/read` |
| **Développeur Azure AI** | Projet/Compte | Actions sur les données + création de projet |
| **Propriétaire Azure AI** | Compte | Accès complet + gestion des rôles |
| **Contributeur** | Subscription/Groupe de ressources | Actions de gestion uniquement (**pas** d’actions sur les données) |
| **Propriétaire** | Subscription/Groupe de ressources | Gestion + attribution de rôles (**pas** d’actions sur les données) |

---

## 8. Liste de vérification de fin d’atelier

| # | Élément | Module |
|---|---------|--------|
| 1 | Prérequis installés et vérifiés | [00](00-prerequisites.md) |
| 2 | Extension Foundry Toolkit installée, projet connecté (ou Chemin B configuré) | [01](01-setup.md) |
| 3 | Agent hébergé structuré | [02](02-create-hosted-agent.md) |
| 4 | `.env` configuré, instructions écrites, dépendances installées | [03](03-configure-and-code.md) |
| 5 | Agent testé localement - 3 scénarios fonctionnels réussis | [04](04-test-locally.md) |
| 6 | Déployé sur Foundry (seulement Chemin A) | [05](05-deploy-to-foundry.md) |
| 7 | Tests d’angle mort/sécurité réussis dans le cloud (seulement Chemin A) | [06](06-verify-in-playground.md) |
| 8 | Résumé passé en revue, prochaines étapes identifiées | [07](07-summary.md) |

---

**Précédent :** [07 - Résumé](07-summary.md) · **Accueil :** [README de l’atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->