# Module 7 - Résumé & Prochaines étapes

⏱️ ~5 min

**Félicitations !** Vous avez créé, testé et (si sur le Chemin A) déployé un agent IA hébergé utilisant Microsoft Foundry et le Foundry Toolkit pour VS Code.

---

## Ce que vous avez construit

Un agent **"Expliquez-le comme si j'étais un cadre dirigeant"** qui :
- Reçoit des rapports d'incidents techniques ou des mises à jour opérationnelles via HTTP (`POST /responses`)
- Les traduit en résumés exécutifs en langage clair
- Suit un format de sortie structuré (Ce qui s'est passé / Impact commercial / Prochaine étape)
- Refuse les demandes hors sujet et les tentatives d'injection de prompt
- Fonctionne comme un agent hébergé conteneurisé dans Microsoft Foundry Agent Service

---

## Concepts clés appris

| Concept | Ce que vous avez pratiqué |
|---------|------------------------|
| **Architecture Agent Framework** | Pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Cycle de vie d'un agent hébergé** | Scaffolding → Configuration → Test local → Déploiement → Vérification dans le cloud |
| **Ingénierie du prompt système** | Rôle, audience, format de sortie, règles, contraintes de sécurité, et exemples |
| **Différences local vs hébergé** | Identité (identifiants personnels vs identité gérée), point de terminaison, chemin réseau |
| **Limites de sécurité** | Défense contre l'injection de prompt, respect du rôle, gestion élégante des cas limites |
| **Flux de travail Foundry Toolkit** | Création de projet, déploiement de modèle, création d'agent, Agent Inspector, déploiement en un clic |

---

## Ce que vous avez accompli

### Chemin A (abonnement Foundry)

- [x] Installation de Foundry Toolkit et création d'un projet Foundry avec un modèle déployé
- [x] Scaffold d'un agent hébergé avec structure de projet auto-générée
- [x] Rédaction d'instructions d'agent structurées avec règles de sécurité
- [x] Test local avec 3 scénarios fonctionnels (Agent Inspector)
- [x] Déploiement sur Foundry Agent Service (conteneurisé)
- [x] Vérification dans le bac à sable cloud avec 4 tests de cas limites/sécurité

### Chemin B (Foundry Local)

- [x] Installation de Foundry Toolkit avec un point de terminaison de modèle local
- [x] Scaffold d'un projet agent hébergé
- [x] Rédaction d'instructions d'agent structurées avec règles de sécurité
- [x] Test local avec 3 scénarios fonctionnels
- [x] Validation du comportement de l'agent sans besoin des ressources cloud

---

## Prochaines étapes

### Continuer à apprendre

| Ressource | Description |
|----------|-------------|
| **[Lab 02 - Orchestration Multi-Agent](../../lab02-multi-agent/docs/README.md)** | Créez un workflow à 4 agents (CV → Évaluateur d'adéquation au poste) avec des patterns d'orchestration |
| **[Ajoutez des outils à votre agent](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Connectez des API, bases de données, ou fonctions personnalisées via le Catalogue d'Outils |
| **[Ajoutez des connaissances (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ancrez votre agent avec des documents, des stores vectoriels, ou la recherche Bing |
| **[Documentation Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Référence complète de la plateforme |
| **[Référence Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentation API pour le package `agent-framework` |
| **[Foundry Toolkit - Nouveautés](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notes de version et journal des modifications de l'extension |

### Idées pour étendre votre agent

- **Ajoutez un outil date** - Permet à l'agent d'inclure le contexte "à ce jour" dans les résumés
- **Connectez-vous à une base de données d'incidents** - Récupérez de vraies informations d'incident via une fonction outil
- **Ajoutez un outil d'ancrage Bing** - Permet à l'agent de rechercher les actualités récentes pour plus de contexte
- **Essayez différents modèles** - Comparez la qualité de sortie entre `gpt-4.1` et `gpt-4.1-mini`
- **Évaluez avec Foundry** - Utilisez la fonctionnalité d'Évaluations pour mesurer la qualité de l'agent à grande échelle

### Pour les utilisateurs du Chemin B : passez au déploiement cloud

Quand vous serez prêt à déployer dans le cloud :
1. Obtenez un abonnement Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complétez [Module 01, Configuration](01-setup.md#step-2-set-up-based-on-your-access) (créez un projet, déployez un modèle, attribuez RBAC)
3. Mettez à jour votre `.env` avec le point de terminaison du projet Foundry et le nom du déploiement modèle
4. Continuez depuis [Module 05 - Déployer sur Foundry](05-deploy-to-foundry.md)

---

## Nettoyer les ressources (optionnel)

Si vous souhaitez supprimer les ressources Azure créées pendant cet atelier :

### Option 1 : Supprimez le groupe de ressources (supprime tout)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Option 2 : Supprimez uniquement l'agent hébergé

1. Ouvrez [ai.azure.com](https://ai.azure.com) → votre projet → **Construire** → **Agents**.
2. Cliquez sur votre agent → cliquez sur **Supprimer**.

### Option 3 : Supprimez le déploiement du modèle

1. Dans la barre latérale de Foundry, développez votre projet → **Modèles**.
2. Clic-droit sur le déploiement du modèle → **Supprimer**.

> **Note sur les coûts :** Les agents hébergés génèrent un coût uniquement lorsqu'ils fonctionnent. Si vous arrêtez ou supprimez l'agent, il n'y a pas de charge continue. Le déploiement du modèle peut engendrer une petite charge pour la capacité réservée - supprimez-le si vous avez terminé.

---

**Précédent :** [06 - Vérifier dans Playground](06-verify-in-playground.md) · **Suivant :** [08 - Dépannage (Référence) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->