# Module 8 - Dépannage

Ce module est un guide de référence pour les problèmes courants. Mettez-le en favori et revenez-y en cas de problème.

---

## 1. Erreurs de permission

### 1.1 Permission `agents/write` refusée

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Cause principale :** Rôle `Azure AI User` manquant au niveau du **projet**. C’est l’erreur la plus fréquente en atelier.

**Correction :**
1. Ouvrez [portal.azure.com](https://portal.azure.com).
2. Recherchez le nom de votre **projet** Foundry → cliquez sur le résultat de type **"Microsoft Foundry project"** (PAS le compte parent).
3. **Contrôle d’accès (IAM)** → **+ Ajouter** → **Ajouter une attribution de rôle**.
4. Rôle : **Azure AI User** → Suivant.
5. Membres : Sélectionnez-vous → Examiner + attribuer → Examiner + attribuer.
6. **Attendez 1–2 minutes** → réessayez.

> **Pourquoi Owner/Contributor ne suffit pas :** Ces rôles accordent uniquement des actions de *gestion*. Les opérations d’agent nécessitent l’*action de données* `agents/write`, disponible uniquement dans les rôles `Azure AI User`, `Azure AI Developer` ou `Azure AI Owner`. Voir la [doc RBAC Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` lors du provisionnement

**Correction :** Demandez à votre admin de vous attribuer le rôle **Contributor** sur le groupe de ressources, ou demandez-lui de créer le projet pour vous et de vous accorder le rôle **Azure AI User**.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Attendre jusqu'à : "Enregistré"
```

---

## 2. Erreurs Docker

> Docker est **optionnel**. Ces erreurs s’appliquent uniquement si Docker Desktop est installé et que l’extension tente une compilation locale.

### 2.1 Le démon Docker ne tourne pas

**Correction :** Lancez Docker Desktop → attendez le statut "en cours d’exécution" → vérifiez avec `docker info` → réessayez.

### 2.2 La compilation échoue avec des erreurs de dépendances

**Correction :** Vérifiez l’orthographe de `requirements.txt`, testez localement d’abord : `pip install -r requirements.txt`.

### 2.3 Incompatibilité de plateforme (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Erreurs d’authentification

### 3.1 Échec de `DefaultAzureCredential`

**Correction (essayez dans l’ordre) :**
1. `az login` (ré-authentification)
2. `az account set --subscription "<id>"` (abonnement correct)
3. VS Code → Comptes → Déconnexion → Reconnexion
4. Vérifiez : `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Le token fonctionne localement mais pas en hébergement

**Attendu :** Les agents hébergés utilisent une identité gérée par le système, pas vos identifiants. Si l’agent hébergé rencontre des erreurs d’authentification :
- Vérifiez que `AZURE_AI_PROJECT_ENDPOINT` dans `agent.yaml` est correct
- Vérifiez que l’identité gérée du projet a accès au modèle

---

## 4. Erreurs de modèle

### 4.1 Déploiement du modèle introuvable

**Correction :** Le nom est **sensible à la casse**. Comparez `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` avec le nom exact dans la barre latérale Foundry → Modèles.

### 4.2 Sortie inattendue du modèle

**Correction :** Revoyez `AGENT_INSTRUCTIONS` dans `main.py` (pas tronqué ?). Essayez un autre modèle (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Erreurs de déploiement

### 5.1 Tirage ACR non autorisé

**Correction :** Azure Portal → Registre de conteneurs → Contrôle d’accès (IAM) → Ajouter le rôle **AcrPull** à l’identité gérée du projet Foundry.

### 5.2 L’agent ne démarre pas (reste "Pending" ou "Failed")

Consultez les logs du conteneur dans la barre latérale. Causes courantes :

| Message de log | Correction |
|-------------|-----------|
| `ModuleNotFoundError` | Ajoutez le paquet manquant dans `requirements.txt`, redéployez |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Ajoutez la variable d’environnement dans `agent.yaml` sous `environment_variables` |
| `Address already in use` | Assurez-vous qu’un seul processus utilise le port 8088 |

### 5.3 Le déploiement expire

**Correction :** Vérifiez la connexion internet. Le premier déploiement pousse >100MB. Derrière un proxy ? Configurez le proxy de Docker Desktop.

---

## 6. Chemin B - Foundry Local

### 6.1 Foundry Local ne démarre pas

| Problème | Correction |
|---------|-----------|
| `foundry: command not found` | Réinstallez : `winget install Microsoft.FoundryLocal` |
| Ressources insuffisantes | Foundry Local a besoin d’environ 4GB de RAM libre. Fermez les autres applications. |
| Échec du téléchargement du modèle | Vérifiez l’espace disque (les modèles font 2–8 GB). Réessayez : `foundry local models pull <name>` |

### 6.2 Erreurs des modèles Foundry Local

| Problème | Correction |
|---------|-----------|
| Réponses lentes | Normal - les modèles locaux tournent sur CPU sauf si vous avez un GPU. Soyez patient. |
| Résultats de faible qualité | Essayez un modèle plus grand si votre matériel le permet. `phi-4-mini` est un bon compromis. |
| Connexion refusée | Vérifiez que Foundry Local tourne : `foundry local status`. Redémarrez si nécessaire. |

---

## 7. Référence rapide : rôles RBAC

| Rôle | Portée | Accorde |
|------|--------|---------|
| **Azure AI User** | Projet | Actions sur données : `agents/write`, `agents/read` |
| **Azure AI Developer** | Projet/Compte | Actions sur données + création de projet |
| **Azure AI Owner** | Compte | Accès complet + gestion des rôles |
| **Contributor** | Abonnement/Groupe de ressources | Actions de gestion uniquement (**pas** d’actions sur données) |
| **Owner** | Abonnement/Groupe de ressources | Gestion + attribution de rôles (**pas** d’actions sur données) |

---

## 8. Checklist de fin d’atelier

| # | Éléments | Module |
|---|----------|--------|
| 1 | Prérequis installés et vérifiés | [00](00-prerequisites.md) |
| 2 | Extension Foundry Toolkit installée, projet connecté (ou Chemin B configuré) | [01](01-setup.md) |
| 3 | Agent hébergé mis en place | [02](02-create-hosted-agent.md) |
| 4 | `.env` configuré, instructions écrites, dépendances installées | [03](03-configure-and-code.md) |
| 5 | Agent testé localement - 3 scénarios fonctionnels validés | [04](04-test-locally.md) |
| 6 | Déployé sur Foundry (Chemin A uniquement) | [05](05-deploy-to-foundry.md) |
| 7 | Tests de cas limites/sécurité réussis dans le cloud (Chemin A uniquement) | [06](06-verify-in-playground.md) |
| 8 | Résumé revu, prochaines étapes identifiées | [07](07-summary.md) |

---

**Précédent :** [07 - Résumé](07-summary.md) · **Accueil :** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->