# Module 7 - Vérification dans le Playground

⏱️ ~10 min

Dans ce module, vous testez votre workflow multi-agent déployé dans VS Code et le portail Foundry, en confirmant que l'agent se comporte de la même manière qu'en test local.

---

## Pourquoi tester à nouveau après le déploiement ?

L'environnement hébergé diffère du local à plusieurs égards importants :

| | Local | Hébergé |
|--|-------|--------|
| **Identité** | Votre connexion personnelle (`DefaultAzureCredential`) | Identité Entra dédiée par agent (auto-provisionnée au moment du déploiement) |
| **Point de terminaison** | `http://localhost:8088/responses` | URL gérée par le service Foundry Agent |
| **Réseau** | Votre machine → Azure OpenAI + MCP | Backbone Azure (latence plus faible) |

Une variable d'environnement mal configurée, un problème RBAC ou un appel sortant MCP bloqué se manifesteraient d'abord ici.

---

## Option A : Tester dans le Playground VS Code (recommandé en premier)

### Étape 1 : Accédez à votre agent hébergé

1. Cliquez sur l'icône **Foundry Toolkit** dans la barre d'activités.
2. Développez votre projet → **Hosted Agents (Preview)** → trouvez votre agent.

![Barre latérale Foundry Toolkit affichant Hosted Agents (aperçu) avec resume-job-fit-evaluator et ses versions déployées](../../../../../translated_images/fr/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Étape 2 : Sélectionnez une version

1. Cliquez sur l'agent pour développer ses versions.
2. Cliquez sur `v1` → vérifiez que le statut est **actif** (la barre latérale peut afficher "Running" ou "Started" - les deux indiquent le même état prêt).

### Étape 3 : Ouvrez le Playground

1. Cliquez sur **Playground** (ou clic droit sur la version → **Open in Playground**).
2. Une fenêtre de chat s'ouvre dans un onglet VS Code.

### Étape 4 : Exécutez vos tests de fumée

Utilisez les mêmes 3 tests du [Module 5](05-test-locally.md). Tapez chaque message dans la boîte de saisie du Playground et appuyez sur **Envoyer** (ou **Entrée**).

#### Test 1 - Résumé complet + JD (flux standard)

Collez l'invite du résumé complet + JD du Module 5, Test 1 (Jane Doe + Senior Cloud Engineer chez Contoso Ltd).

**Attendu :**
- Score d'adéquation avec calcul détaillé (échelle de 100 points)
- Section Compétences correspondantes
- Section Compétences manquantes
- **Une carte d'écart par compétence manquante** avec des URL Microsoft Learn
- Feuille de route d'apprentissage avec chronologie

#### Test 2 - Test rapide court (entrée minimale)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Attendu :**
- Score d'adéquation plus faible (< 40)
- Évaluation honnête avec parcours d'apprentissage étagé
- Plusieurs cartes d'écart (AWS, Kubernetes, Terraform, CI/CD, écart d'expérience)

#### Test 3 - Candidat à haute adéquation

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Attendu :**
- Score d'adéquation élevé (≥ 80)
- Focalisation sur la préparation à l'entretien et le polissage
- Peu ou pas de cartes d'écart
- Chronologie courte axée sur la préparation

### Étape 5 : Comparez avec les résultats locaux

Ouvrez vos notes ou l'onglet de navigateur du Module 5 où vous avez sauvegardé les réponses locales. Pour chaque test :

- La réponse a-t-elle la **même structure** (score d'adéquation, cartes d'écart, feuille de route) ?
- Suit-elle la **même grille de notation** (détail sur 100 points) ?
- Les **URL Microsoft Learn** sont-elles toujours présentes dans les cartes d'écart ?
- Y a-t-il **une carte d'écart par compétence manquante** (non tronquée) ?

> **Des différences mineures de formulation sont normales** - le modèle est non déterministe. Concentrez-vous sur la structure, la cohérence de la notation et l'utilisation de l'outil MCP.

---

## Option B : Tester dans le portail Foundry

Le [portail Foundry](https://ai.azure.com) propose un playground web utile pour le partage avec des coéquipiers ou parties prenantes.

### Étape 1 : Ouvrir le portail Foundry

1. Ouvrez votre navigateur et rendez-vous sur [https://ai.azure.com](https://ai.azure.com).
2. Connectez-vous avec le même compte Azure que vous avez utilisé tout au long de l'atelier.

### Étape 2 : Accédez à votre projet

1. Sur la page d'accueil, repérez **Projets récents** dans la barre latérale gauche.
2. Cliquez sur le nom de votre projet (par exemple, `workshop-agents`).
3. Si vous ne le voyez pas, cliquez sur **Tous les projets** et recherchez-le.

### Étape 3 : Trouver votre agent déployé

1. Dans la navigation gauche du projet, cliquez sur **Build** → **Agents** (ou cherchez la section **Agents**).
2. Vous devriez voir une liste d'agents. Trouvez votre agent déployé (par exemple, `resume-job-fit-evaluator`).
3. Cliquez sur le nom de l'agent pour ouvrir sa page de détails.

### Étape 4 : Ouvrir le Playground

1. Sur la page de détails de l'agent, regardez la barre d'outils en haut.
2. Cliquez sur **Ouvrir dans le playground** (ou **Essayer dans le playground**).
3. Une interface de chat s'ouvre.

### Étape 5 : Exécuter les mêmes tests de fumée

Répétez les 3 tests du Playground VS Code ci-dessus. Comparez chaque réponse avec les résultats locaux (Module 5) et les résultats du Playground VS Code (option A ci-dessus).

---

## Vérification spécifique multi-agent

Au-delà de la simple exactitude, vérifiez ces comportements spécifiques multi-agent :

### Exécution des outils MCP

| Vérifier | Comment vérifier | Condition de réussite |
|-------|---------------|----------------|
| Appels MCP réussis | Les cartes d'écart contiennent des URL `learn.microsoft.com` | URL réelles, pas des messages de secours |
| Appels MCP multiples | Chaque écart de priorité élevée/moyenne a des ressources | Pas seulement la première carte d'écart |
| Repli MCP fonctionne | Si les URL manquent, vérifier la présence d'un texte de secours | L'agent produit toujours des cartes d'écart (avec ou sans URL) |

### Coordination des agents

| Vérifier | Comment vérifier | Condition de réussite |
|-------|---------------|----------------|
| Les 4 agents ont fonctionné | La sortie contient le score d'adéquation ET les cartes d'écart | Le score vient de MatchingAgent, les cartes de GapAnalyzer |
| Exécution séquentielle | Le temps de réponse est raisonnable (< 2 min) | Si > 3 min, vérifier les erreurs dans le journal du terminal |
| Intégrité du flux de données | Les cartes d'écart référencent des compétences du rapport de correspondance | Pas de compétences hallucinées absentes de la JD |

---

## Grille de validation

Utilisez cette grille pour évaluer le comportement hébergé de votre workflow multi-agent :

| # | Critère | Condition de réussite | Validé ? |
|---|----------|---------------|-------|
| 1 | **Correction fonctionnelle** | L'agent répond au résumé + JD avec score d'adéquation et analyse des écarts | |
| 2 | **Cohérence de notation** | Le score d'adéquation utilise une échelle 100 points avec détails | |
| 3 | **Complétude des cartes d'écart** | Une carte par compétence manquante (non tronquée ni combinée) | |
| 4 | **Intégration outil MCP** | Les cartes d'écart incluent des URL Microsoft Learn réelles | |
| 5 | **Cohérence structurelle** | La structure de sortie correspond entre exécutions locale et hébergée | |
| 6 | **Temps de réponse** | L'agent hébergé répond en moins de 2 minutes pour l'évaluation complète | |
| 7 | **Absence d'erreurs** | Pas d'erreurs HTTP 500, dépassements de délai ou réponses vides | |

> Une "validation" signifie que les 7 critères sont remplis pour les 3 tests de fumée dans au moins un playground (VS Code ou Portail).

---

## Dépannage des problèmes de playground

| Symptôme | Cause probable | Correction |
|---------|-------------|-----|
| Le playground ne charge pas | Conteneur pas en état `active` | Retournez au [Module 6](06-deploy-to-foundry.md), vérifiez l'état de déploiement. Patientez si `creating` |
| L'agent renvoie une réponse vide | Nom de déploiement du modèle incorrect | Vérifiez dans `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` correspond au modèle déployé |
| L'agent renvoie un message d'erreur | Permission [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) manquante | Assignez **[Foundry User](https://aka.ms/foundry-ext-project-role)** (anciennement Azure AI User) au niveau projet |
| Pas d'URL Microsoft Learn dans les cartes d'écart | MCP sortant bloqué ou serveur MCP indisponible | Vérifiez si le conteneur peut atteindre `learn.microsoft.com`. Voir [Module 8](08-troubleshooting.md) |
| Une seule carte d'écart (tronquée) | Instructions GapAnalyzer manquent le bloc "CRITICAL" | Consultez le [Module 3, Étape 2.4](03-configure-agents.md) |
| Score d'adéquation très différent du local | Modèle ou instructions déployés différents | Comparez les variables d'env dans `agent.yaml` avec le `.env` local. Redéployez si nécessaire |
| "Agent introuvable" dans le portail | Déploiement encore en propagation ou échoué | Attendez 2 minutes, actualisez. Si toujours absent, redéployez depuis [Module 6](06-deploy-to-foundry.md) |

---

### Point de contrôle

- [ ] Agent testé dans le Playground VS Code - les 3 tests de fumée réussis
- [ ] Agent testé dans le Playground [Foundry Portal](https://ai.azure.com) - les 3 tests de fumée réussis
- [ ] Réponses structurellement cohérentes avec les tests locaux (score d'adéquation, cartes d'écart, feuille de route)
- [ ] URL Microsoft Learn présentes dans les cartes d'écart (outil MCP fonctionnant en environnement hébergé)
- [ ] Une carte d'écart par compétence manquante (pas de troncature)
- [ ] Pas d'erreurs ni de dépassements de délai lors des tests
- [ ] Grille de validation complétée (les 7 critères validés)

---

**Précédent :** [06 - Deploy to Foundry](06-deploy-to-foundry.md) · **Suivant :** [08 - Dépannage →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->