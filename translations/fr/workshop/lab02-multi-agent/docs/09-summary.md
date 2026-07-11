# Module 9 - Résumé & Étapes suivantes

⏱️ ~5 min

**Félicitations !** Vous avez construit, testé et (si vous êtes sur le chemin A) déployé un workflow multi-agent utilisant Microsoft Foundry et le Foundry Toolkit pour VS Code.

---

## Ce que vous avez construit

Le **Resume → Job Fit Evaluator** – un workflow multi-agent hébergé qui :
- Reçoit un CV + une description de poste via HTTP (`POST /responses`)
- Exécute quatre agents spécialisés en pipeline séquentiel – chaque agent relaie les données dont son successeur a besoin
- Renvoie un score de correspondance (0 à 100 avec une ventilation), une liste des écarts de compétences et certifications, et une feuille de route d'apprentissage personnalisée avec des liens Microsoft Learn réels pour chaque écart
- Interroge le serveur Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) pour récupérer les ressources d'apprentissage officielles correspondant à chaque écart de compétence identifié
- Fonctionne comme un agent hébergé conteneurisé unique dans le Microsoft Foundry Agent Service

---

## Concepts clés appris

| Concept | Ce que vous avez pratiqué |
|---------|-------------------------|
| **Orchestration multi-agent** | Pipeline séquentiel `WorkflowBuilder` avec `add_edge()` |
| **Spécialisation des agents** | Quatre agents spécialisés surpassent un agent polyvalent unique |
| **Pattern Content Router** | ResumeParser fait aussi office de routeur – il conserve le texte de la description de poste dans une section `[JOB DESCRIPTION PASS-THROUGH]` pour que les agents en aval puissent y accéder (nécessaire car `context_mode="last_agent"` signifie que seul le `start_executor` voit le message utilisateur brut) |
| **Pattern Content Relay** | JD Agent relaie le `[PARSED RESUME PASS-THROUGH]` vers l'avant pour que MatchingAgent ait les deux profils ; évite le double déclenchement en mode OU que les graphes en entonnoir provoquent |
| **Intégration de l'outil MCP** | `@tool` + `streamable_http_client` appelant un serveur MCP externe |
| **Cycle de vie de l’agent hébergé** | Génération → Configuration → Test local → Déploiement → Vérification dans le cloud |
| **`context_mode="last_agent"`** | Chaque exécuteur ne voit que la sortie directe de son prédécesseur |
| **Workflow Foundry Toolkit** | Assistant de génération, Agent Inspector, Workflow Visualizer, déploiement en un clic |

---

## Ce que vous avez complété

<details open>
<summary><strong>🅰️ Chemin A - Abonnement Foundry</strong></summary>

- [x] Vérification de la configuration du Lab 01 : projet, modèle, et RBAC toujours actifs
- [x] Génération d’un projet multi-agent avec le template Workflows
- [x] Rédaction de quatre ensembles d’instructions pour agents (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Intégration de l’outil Microsoft Learn MCP avec `streamable_http_client`
- [x] Câblage du graphe de workflow avec `WorkflowBuilder` (pipeline séquentiel avec relais de contenu)
- [x] Tests locaux avec 3 tests de fumée (Agent Inspector) – score de correspondance, cartes d’écart, et URLs MCP
- [x] Déploiement dans Foundry Agent Service (conteneurisé, identité gérée)
- [x] Vérification dans le playground cloud — cohérence structurelle avec résultats locaux

</details>

<details open>
<summary><strong>🅱️ Chemin B - Foundry Local</strong></summary>

- [x] Vérification du Lab 01 : Foundry Local fonctionnant avec un modèle local
- [x] Génération d’un projet multi-agent avec le template Workflows
- [x] Rédaction de quatre ensembles d’instructions pour agents et câblage du graphe workflow
- [x] Intégration de l’outil Microsoft Learn MCP
- [x] Tests locaux avec 3 tests de fumée
- [x] Validation du comportement multi-agent sans ressources cloud nécessaires

</details>

---

## Étapes suivantes

### Continuer à apprendre

| Ressource | Description |
|----------|-------------|
| **[Référence Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentation API pour `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catalogue outil MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Connecter les agents à d’autres serveurs MCP (Bing, GitHub, personnalisé) |
| **[Ajouter des connaissances (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ancrer les agents avec des documents, des magasins vectoriels ou la recherche Bing |
| **[Evaluations Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mesurer la qualité des agents à grande échelle avec des évaluateurs automatisés |
| **[Documentation Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Référence complète de la plateforme |
| **[Foundry Toolkit - Nouveautés](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notes de version et journal des modifications de l’extension |

### Idées pour étendre ce workflow

- **Ajouter un 5e agent** – Un coach d’entretien qui génère des questions probables basées sur le rapport d’écart
- **Ajouter un outil d’ancrage Bing** – Permettre à l’agent JD de rechercher des offres d’emploi similaires pour enrichir les exigences
- **Se connecter à une base de CV** – Extraire les profils candidats d’une base de données via un `@tool` personnalisé
- **Tester différents modèles** – Comparer la qualité et la latence des sorties `gpt-4.1` vs `gpt-4.1-mini`
- **Évaluer avec Foundry** – Utiliser la fonctionnalité Évaluations pour noter les rapports de correspondance sur un jeu de données de référence

### Pour les utilisateurs du chemin B : migration vers un déploiement cloud

Quand vous êtes prêt à déployer sur le cloud :
1. Obtenez un abonnement Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complétez le [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (créez un projet, déployez un modèle, assignez RBAC)
3. Mettez à jour votre `.env` avec le point de terminaison du projet Foundry et le nom du déploiement du modèle
4. Poursuivez depuis le [Module 06 - Déploiement vers Foundry](06-deploy-to-foundry.md)

---

## Nettoyer les ressources (optionnel)

Si vous souhaitez supprimer les ressources Azure créées durant cet atelier :

### Option 1 : Supprimer le groupe de ressources (supprime tout)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2 : Supprimer uniquement l’agent hébergé

1. Ouvrez [ai.azure.com](https://ai.azure.com) → votre projet → **Créer** → **Agents**.
2. Trouvez **PersonalCareerCopilot** → cliquez sur **Supprimer**.

### Option 3 : Supprimer le déploiement du modèle

1. Dans la barre latérale Foundry, développez votre projet → **Modèles**.
2. Clic droit sur le déploiement du modèle → **Supprimer**.

> **Note sur les coûts :** Les agents hébergés engendrent des coûts uniquement lorsqu’ils sont en fonctionnement. Si vous arrêtez ou supprimez l’agent, il n’y a pas de frais récurrents. Le déploiement du modèle peut engendrer un petit coût pour la capacité réservée – supprimez-le si vous avez terminé.

---

**Précédent :** [08 - Dépannage](08-troubleshooting.md) · **Accueil :** [Lab 02 README](../README.md) · [Accueil de l’atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->