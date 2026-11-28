# Module 9 - Résumé & Prochaines étapes

⏱️ ~5 min

**Félicitations !** Vous avez construit, testé et (si vous êtes sur le chemin A) déployé un workflow multi-agent en utilisant Microsoft Foundry et le Foundry Toolkit pour VS Code.

---

## Ce que vous avez construit

Le **Resume → Job Fit Evaluator** - un workflow multi-agent hébergé qui :
- Reçoit un CV + une description de poste via HTTP (`POST /responses`)
- Exécute quatre agents spécialisés dans une pipeline séquentielle - chaque agent relaie les données nécessaires à son successeur
- Retourne un score d’adéquation (0–100 avec un détail), une liste d’écarts de compétences et certifications, et une feuille de route d’apprentissage personnalisée avec de vrais liens Microsoft Learn pour chaque écart
- Interroge le serveur Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) pour récupérer les ressources d’apprentissage officielles pour chaque écart de compétences identifié
- Fonctionne en tant qu’agent hébergé conteneurisé unique dans Microsoft Foundry Agent Service

---

## Concepts clés appris

| Concept | Ce que vous avez pratiqué |
|---------|-------------------------|
| **Orchestration multi-agent** | Pipeline séquentielle `WorkflowBuilder` avec `add_edge()` |
| **Spécialisation des agents** | Quatre agents spécialisés surpassent un agent à usage général |
| **Pattern Content Router** | ResumeParser fait aussi office de routeur - il conserve le texte de la JD dans une section `[JOB DESCRIPTION PASS-THROUGH]` pour que les agents en aval puissent y accéder (nécessaire parce que `context_mode="last_agent"` signifie que seul le `start_executor` voit le message utilisateur brut) |
| **Pattern Content Relay** | L’agent JD relaie `[PARSED RESUME PASS-THROUGH]` vers l’avant pour que MatchingAgent ait les deux profils ; évite le double déclenchement en OR que provoquent les graphes en fan-in |
| **Intégration outil MCP** | `@tool` + `streamable_http_client` appelant un serveur MCP externe |
| **Cycle de vie Agent hébergé** | Générer → Configurer → Tester localement → Déployer → Vérifier dans le cloud |
| **`context_mode="last_agent"`** | Chaque exécuteur ne voit que la sortie directe de son prédécesseur |
| **Workflow Foundry Toolkit** | Assistant de génération, Agent Inspector, Visualiseur de workflow, déploiement en un clic |

---

## Ce que vous avez complété

<details open>
<summary><strong>🅰️ Chemin A - Abonnement Foundry</strong></summary>

- [x] Vérification du Lab 01 : projet, modèle et RBAC toujours actifs
- [x] Généré un projet multi-agent avec le modèle Workflows
- [x] Rédigé quatre jeux d’instructions d’agent (ResumeParser, Agent JD, MatchingAgent, GapAnalyzer)
- [x] Intégré l’outil Microsoft Learn MCP avec `streamable_http_client`
- [x] Connecté le graphe du workflow avec `WorkflowBuilder` (pipeline séquentielle avec relais de contenu)
- [x] Testé localement avec 2 tests de fumée (Agent Inspector) - score d’adéquation, cartes d’écart et URLs MCP
- [x] Déployé dans Foundry Agent Service (conteneurisé, identité managée)
- [x] Vérifié dans le playground cloud - cohérence structurelle avec les résultats locaux

</details>

<details open>
<summary><strong>🅱️ Chemin B - Foundry Local</strong></summary>

- [x] Vérification du Lab 01 : Foundry Local fonctionnel avec un modèle local
- [x] Généré un projet multi-agent avec le modèle Workflows
- [x] Rédigé quatre jeux d’instructions d’agent et connecté le graphe du workflow
- [x] Intégré l’outil Microsoft Learn MCP
- [x] Testé localement avec 2 tests de fumée
- [x] Validé le comportement multi-agent sans besoin de ressources cloud

</details>

---

## Prochaines étapes

### Continuer à apprendre

| Ressource | Description |
|----------|-------------|
| **[Référence SDK Agent Framework](https://learn.microsoft.com/agent-framework/)** | Docs API pour `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catalogue outil MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Connecter les agents à d’autres serveurs MCP (Bing, GitHub, custom) |
| **[Ajouter connaissance (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ancrer les agents avec documents, magasins vectoriels ou recherche Bing |
| **[Évaluations Foundry](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mesurer la qualité des agents à grande échelle avec des évaluateurs automatisés |
| **[Documentation Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Référence complète de la plateforme |
| **[Foundry Toolkit - Nouvelles fonctionnalités](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notes de version et journal des modifications de l’extension |

### Idées pour étendre ce workflow

- **Ajouter un 5e agent** - Un coach d’entretien qui produit des questions probables basées sur le rapport d’écart
- **Ajouter un outil d’ancrage Bing** - Permettre à l’agent JD de rechercher des offres d’emploi similaires pour enrichir les exigences
- **Se connecter à une base de CV** - Récupérer les profils de candidats depuis une base via un `@tool` personnalisé
- **Essayer différents modèles** - Comparer la qualité et la latence de sortie entre `gpt-4.1` et `gpt-4.1-mini`
- **Évaluer avec Foundry** - Utiliser la fonction Évaluations pour noter les rapports d’adéquation par rapport à un jeu de données de référence

### Pour les utilisateurs du chemin B : passer au déploiement cloud

Quand vous êtes prêt à déployer dans le cloud :
1. Obtenez un abonnement Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complétez [Lab 01, Module 01](../../lab01-single-agent/docs/01-setup.md) (créez projet, déployez modèle, assignez RBAC)
3. Mettez à jour votre `.env` avec le point de terminaison projet Foundry et le nom du déploiement modèle
4. Continuez depuis [Module 06 - Déployer sur Foundry](06-deploy-to-foundry.md)

---

## Nettoyer les ressources (optionnel)

Si vous souhaitez supprimer les ressources Azure créées pendant cet atelier :

### Option 1 : Supprimer le groupe de ressources (supprime tout)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2 : Supprimer uniquement l’agent hébergé

1. Ouvrez [ai.azure.com](https://ai.azure.com) → votre projet → **Build** → **Agents**.
2. Trouvez **PersonalCareerCopilot** → cliquez sur **Delete**.

### Option 3 : Supprimer le déploiement du modèle

1. Dans la barre latérale Foundry, développez votre projet → **Models**.
2. Clic droit sur le déploiement du modèle → **Delete**.

> **Note coût :** les agents hébergés n’engendrent des coûts que lorsqu’ils fonctionnent. Si vous arrêtez ou supprimez l’agent, il n’y a pas de charge continue. Le déploiement du modèle peut engendrer une petite charge pour la capacité réservée - supprimez-le si vous avez terminé.

---

**Précédent :** [08 - Dépannage](08-troubleshooting.md) · **Accueil :** [Lab 02 README](../README.md) · [Accueil atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->