# Module 8 - Dépannage

Ce module est un guide de référence pour tous les problèmes courants rencontrés lors de l'atelier. Mettez-le en favori - vous y reviendrez chaque fois que quelque chose ne fonctionne pas.

---

## 1. Erreurs de permissions

### 1.1 Permission `agents/write` refusée

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Cause principale :** Vous n'avez pas le rôle `Azure AI User` au niveau du **projet**. C'est l'erreur la plus courante dans l'atelier.

**Correction - étape par étape :**

1. Ouvrez [https://portal.azure.com](https://portal.azure.com).
2. Dans la barre de recherche en haut, tapez le nom de votre **projet Foundry** (par exemple, `workshop-agents`).
3. **Important :** Cliquez sur le résultat de type **"Microsoft Foundry project"**, PAS sur le compte parent / ressource hub. Ce sont des ressources différentes avec des portées RBAC différentes.
4. Dans la navigation gauche de la page du projet, cliquez sur **Contrôle d’accès (IAM)**.
5. Cliquez sur l’onglet **Attributions de rôle** pour vérifier si vous avez déjà le rôle :
   - Recherchez votre nom ou votre email.
   - Si `Azure AI User` est déjà listé → l’erreur vient d’une autre cause (vérifiez l'étape 8 ci-dessous).
   - Sinon → poursuivez pour l’ajouter.
6. Cliquez sur **+ Ajouter** → **Ajouter une attribution de rôle**.
7. Dans l’onglet **Rôle** :
   - Recherchez [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Sélectionnez-le dans les résultats.
   - Cliquez sur **Suivant**.
8. Dans l’onglet **Membres** :
   - Sélectionnez **Utilisateur, groupe ou principal de service**.
   - Cliquez sur **+ Sélectionner des membres**.
   - Recherchez votre nom ou adresse email.
   - Sélectionnez-vous dans les résultats.
   - Cliquez sur **Sélectionner**.
9. Cliquez sur **Examiner + attribuer** → **Examiner + attribuer** à nouveau.
10. **Attendez 1-2 minutes** - les modifications RBAC prennent du temps à se propager.
11. Retentez l’opération qui a échoué.

> **Pourquoi Owner/Contributor ne suffit pas :** Azure RBAC a deux types de permissions – *actions de gestion* et *actions de données*. Owner et Contributor accordent les actions de gestion (création de ressources, modification des paramètres), mais les opérations des agents nécessitent l’action de données `agents/write`, incluse uniquement dans les rôles `Azure AI User`, `Azure AI Developer`, ou `Azure AI Owner`. Voir [docs Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` lors de la création de ressources

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Cause principale :** Vous n’avez pas les permissions pour créer ou modifier des ressources Azure dans cet abonnement/groupe de ressources.

**Correction :**
1. Demandez à l’administrateur de votre abonnement de vous attribuer le rôle **Contributeur** sur le groupe de ressources où se trouve votre projet Foundry.
2. Sinon, demandez-lui de créer le projet Foundry pour vous et de vous attribuer le rôle **Azure AI User** sur le projet.

### 1.3 `SubscriptionNotRegistered` pour [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Cause principale :** L’abonnement Azure n’a pas enregistré le fournisseur de ressources nécessaire pour Foundry.

**Correction :**

1. Ouvrez un terminal et lancez :
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Attendez la fin de l’enregistrement (cela peut prendre 1-5 minutes) :
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Sortie attendue : `"Registered"`
3. Retentez l’opération.

---

## 2. Erreurs Docker (uniquement si Docker est installé)

> Docker est **optionnel** pour cet atelier. Ces erreurs concernent uniquement si vous avez Docker Desktop installé et que l’extension Foundry tente une compilation locale de conteneur.

### 2.1 Le démon Docker ne fonctionne pas

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Correction - étape par étape :**

1. **Trouvez Docker Desktop** dans votre menu Démarrer (Windows) ou Applications (macOS) et lancez-le.
2. Attendez que la fenêtre Docker Desktop affiche **"Docker Desktop is running"** - cela prend généralement 30-60 secondes.
3. Cherchez l’icône de la baleine Docker dans votre barre des tâches (Windows) ou barre de menus (macOS). Survolez-la pour confirmer son statut.
4. Vérifiez dans un terminal :
   ```powershell
   docker info
   ```
   Si cela affiche les informations système Docker (Version serveur, pilote de stockage, etc.), Docker est démarré.
5. **Spécifique à Windows :** Si Docker ne démarre toujours pas :
   - Ouvrez Docker Desktop → **Paramètres** (icône engrenage) → **Général**.
   - Assurez-vous que **Use the WSL 2 based engine** est coché.
   - Cliquez sur **Appliquer & redémarrer**.
   - Si WSL 2 n’est pas installé, lancez `wsl --install` dans un PowerShell en mode administrateur et redémarrez votre ordinateur.
6. Retentez le déploiement.

### 2.2 La construction Docker échoue avec des erreurs de dépendances

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Correction :**
1. Ouvrez `requirements.txt` et vérifiez que tous les noms de paquets sont correctement orthographiés.
2. Assurez-vous que le verrouillage des versions est correct :
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Testez l’installation localement d’abord :
   ```bash
   pip install -r requirements.txt
   ```
4. Si vous utilisez un index privé de paquets, assurez-vous que Docker y a accès au réseau.

### 2.3 Incompatibilité de plateforme du conteneur (Apple Silicon)

Si vous déployez depuis un Mac Apple Silicon (M1/M2/M3/M4), le conteneur doit être construit pour `linux/amd64` car le runtime conteneur Foundry utilise AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> La commande de déploiement de l’extension Foundry gère cela automatiquement dans la plupart des cas. Si vous voyez des erreurs liées à l’architecture, construisez manuellement avec le flag `--platform` et contactez l’équipe Foundry.

---

## 3. Erreurs d’authentification

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ne parvient pas à récupérer un jeton

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Cause principale :** Aucune source de crédential dans la chaîne `DefaultAzureCredential` ne possède un jeton valide.

**Correction - essayez chaque étape dans l’ordre :**

1. **Reconnectez-vous via Azure CLI** (correction la plus courante) :
   ```bash
   az login
   ```
   Une fenêtre de navigateur s’ouvre. Connectez-vous, puis revenez dans VS Code.

2. **Définissez l’abonnement correct :**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Si ce n’est pas le bon abonnement :
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Reconnectez-vous via VS Code :**
   - Cliquez sur l’icône **Comptes** (icône personne) en bas à gauche de VS Code.
   - Cliquez sur votre nom de compte → **Se déconnecter**.
   - Cliquez à nouveau sur l’icône Comptes → **Se connecter à Microsoft**.
   - Terminez le processus de connexion dans le navigateur.

4. **Principal de service (scénarios CI/CD uniquement) :**
   - Définissez ces variables d’environnement dans votre `.env` :
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Puis redémarrez votre processus agent.

5. **Vérifiez le cache du jeton :**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Si cela échoue, votre jeton CLI a expiré. Lancez `az login` à nouveau.

### 3.2 Le jeton fonctionne localement mais pas dans le déploiement hébergé

**Cause principale :** L’agent hébergé utilise une identité gérée par le système, différente de vos informations personnelles.

**Correction :** C’est un comportement attendu - l’identité gérée est automatiquement configurée lors du déploiement. Si l’agent hébergé reçoit toujours des erreurs d’authentification :
1. Vérifiez que l’identité gérée du projet Foundry a accès à la ressource Azure OpenAI.
2. Vérifiez que `PROJECT_ENDPOINT` dans `agent.yaml` est correct.

---

## 4. Erreurs de modèle

### 4.1 Déploiement du modèle introuvable

```
Error: Model deployment not found / The specified deployment does not exist
```

**Correction - étape par étape :**

1. Ouvrez votre fichier `.env` et notez la valeur de `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Ouvrez le panneau latéral **Microsoft Foundry** dans VS Code.
3. Déroulez votre projet → **Modèles déployés**.
4. Comparez le nom du déploiement affiché avec la valeur dans `.env`.
5. Le nom est **sensible à la casse** - `gpt-4o` est différent de `GPT-4o`.
6. S’ils ne correspondent pas, mettez à jour votre `.env` avec le nom exact affiché dans le panneau latéral.
7. Pour le déploiement hébergé, mettez aussi à jour `agent.yaml` :
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Le modèle répond avec un contenu inattendu

**Correction :**
1. Passez en revue la constante `EXECUTIVE_AGENT_INSTRUCTIONS` dans `main.py`. Assurez-vous qu’elle n’a pas été tronquée ou corrompue.
2. Vérifiez le paramètre de température du modèle (si configurable) – des valeurs plus basses donnent des sorties plus déterministes.
3. Comparez le modèle déployé (par ex., `gpt-4o` vs `gpt-4o-mini`) – différents modèles ont différentes capacités.

---

## 5. Erreurs de déploiement

### 5.1 Autorisation de tirage ACR

```
Error: AcrPullUnauthorized
```

**Cause principale :** L’identité gérée du projet Foundry ne peut pas tirer l’image du conteneur depuis Azure Container Registry.

**Correction - étape par étape :**

1. Ouvrez [https://portal.azure.com](https://portal.azure.com).
2. Recherchez **[Registres de conteneurs](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** dans la barre de recherche en haut.
3. Cliquez sur le registre associé à votre projet Foundry (il se trouve généralement dans le même groupe de ressources).
4. Dans la navigation gauche, cliquez sur **Contrôle d’accès (IAM)**.
5. Cliquez sur **+ Ajouter** → **Ajouter une attribution de rôle**.
6. Recherchez **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** et sélectionnez-le. Cliquez sur **Suivant**.
7. Sélectionnez **Identité gérée** → cliquez sur **+ Sélectionner des membres**.
8. Trouvez et sélectionnez l’identité gérée du projet Foundry.
9. Cliquez sur **Sélectionner** → **Examiner + attribuer** → **Examiner + attribuer**.

> Cette attribution de rôle est normalement configurée automatiquement par l’extension Foundry. Si vous voyez cette erreur, la configuration automatique a peut-être échoué. Vous pouvez aussi essayer de redéployer – l’extension peut réessayer la configuration.

### 5.2 L’agent ne démarre pas après déploiement

**Symptômes :** Le statut du conteneur reste "Pending" plus de 5 minutes ou affiche "Failed".

**Correction - étape par étape :**

1. Ouvrez le panneau latéral **Microsoft Foundry** dans VS Code.
2. Cliquez sur votre agent hébergé → sélectionnez la version.
3. Dans le panneau de détail, vérifiez **Détails du conteneur** → recherchez une section ou un lien **Logs**.
4. Lisez les logs de démarrage du conteneur. Causes fréquentes :

| Message de log | Cause | Correction |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Dépendance manquante | Ajoutez-la dans `requirements.txt` et redéployez |
| `KeyError: 'PROJECT_ENDPOINT'` | Variable d’environnement manquante | Ajoutez la variable dans `agent.yaml` sous `env:` |
| `OSError: [Errno 98] Address already in use` | Conflit de port | Assurez-vous que `agent.yaml` a `port: 8088` et qu’un seul processus utilise ce port |
| `ConnectionRefusedError` | L’agent n’a pas commencé à écouter | Vérifiez dans `main.py` - l’appel `from_agent_framework()` doit s’exécuter au démarrage |

5. Corrigez le problème, puis redéployez en suivant [Module 6](06-deploy-to-foundry.md).

### 5.3 Le déploiement expire

**Correction :**
1. Vérifiez votre connexion internet - le push Docker peut être volumineux (>100 Mo pour le premier déploiement).
2. Si vous êtes derrière un proxy en entreprise, assurez-vous que les paramètres proxy de Docker Desktop sont configurés : **Docker Desktop** → **Paramètres** → **Ressources** → **Proxies**.
3. Réessayez - les coupures réseau peuvent provoquer des échecs temporaires.

---

## 6. Référence rapide : rôles RBAC

| Rôle | Portée typique | Ce que ça accorde |
|------|---------------|----------------|
| **Azure AI User** | Projet | Actions de données : construire, déployer et invoquer les agents (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projet ou Compte | Actions de données + création de projet |
| **Azure AI Owner** | Compte | Accès complet + gestion des attributions de rôle |
| **Azure AI Project Manager** | Projet | Actions de données + peut attribuer Azure AI User à d’autres |
| **Contributor** | Abonnement/Groupe de ressources | Actions de gestion (création/suppression de ressources). **N’inclut PAS les actions de données** |
| **Owner** | Abonnement/Groupe de ressources | Actions de gestion + attribution de rôle. **N’inclut PAS les actions de données** |
| **Reader** | N'importe où | Accès en lecture seule aux actions de gestion |

> **À retenir :** `Owner` et `Contributor` n’incluent **pas** les actions de données. Vous avez toujours besoin d’un rôle `Azure AI *` pour les opérations d’agents. Le rôle minimum pour cet atelier est **Azure AI User** à la **portée projet**.

---

## 7. Liste de contrôle de fin d’atelier

Utilisez ceci comme confirmation finale que vous avez tout terminé :

| # | Élément | Module | Validé ? |
|---|------|--------|---|
| 1 | Tous les prérequis installés et vérifiés | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit et extensions Foundry installés | [01](01-install-foundry-toolkit.md) | |
| 3 | Projet Foundry créé (ou projet existant sélectionné) | [02](02-create-foundry-project.md) | |
| 4 | Modèle déployé (par ex., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Rôle Utilisateur Azure AI attribué au niveau du projet | [02](02-create-foundry-project.md) | |
| 6 | Projet d'agent hébergé structuré (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` configuré avec PROJECT_ENDPOINT et MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instructions de l'agent personnalisées dans main.py | [04](04-configure-and-code.md) | |
| 9 | Environnement virtuel créé et dépendances installées | [04](04-configure-and-code.md) | |
| 10 | Agent testé localement avec F5 ou terminal (4 tests de fumée réussis) | [05](05-test-locally.md) | |
| 11 | Déployé sur Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Statut du conteneur affiche "Démarré" ou "En cours" | [06](06-deploy-to-foundry.md) | |
| 13 | Vérifié dans VS Code Playground (4 tests de fumée réussis) | [07](07-verify-in-playground.md) | |
| 14 | Vérifié dans Foundry Portal Playground (4 tests de fumée réussis) | [07](07-verify-in-playground.md) | |

> **Félicitations !** Si tous les éléments sont cochés, vous avez terminé tout l'atelier. Vous avez construit un agent hébergé à partir de zéro, l'avez testé localement, déployé sur Microsoft Foundry, et validé en production.

---

**Précédent :** [07 - Vérifier dans le Playground](07-verify-in-playground.md) · **Accueil :** [Lecture du fichier README de l’atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :  
Ce document a été traduit à l’aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d’assurer l’exactitude, veuillez noter que les traductions automatiques peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, une traduction professionnelle humaine est recommandée. Nous ne sommes pas responsables des malentendus ou des interprétations erronées résultant de l’utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->