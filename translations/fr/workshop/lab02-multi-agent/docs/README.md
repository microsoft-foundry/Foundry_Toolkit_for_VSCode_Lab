# Laboratoire 02 - Workflow Multi-Agent : Évaluateur d'Ajustement CV → Emploi

## Parcours Complet d'Apprentissage

Cette documentation vous guide dans la construction, le test et le déploiement d'un **workflow multi-agent** qui évalue l'adéquation d'un CV à un emploi en utilisant quatre agents spécialisés orchestrés via **WorkflowBuilder**.

> **Prérequis :** Terminez [Laboratoire 01 - Agent Unique](../../lab01-single-agent/README.md) avant de commencer le Laboratoire 02.

---

## Modules

| # | Module | Ce que vous ferez |
|---|--------|-------------------|
| 0 | [Introduction](00-prerequisites.md) | Ce que vous allez construire, vérification du Lab 01, comparaison Lab 02 vs Lab 01 |
| 1 | [Comprendre l'Architecture Multi-Agent](01-understand-multi-agent.md) | Apprendre WorkflowBuilder, rôles des agents, graphe d'orchestration |
| 2 | [Échafauder le Projet Multi-Agent](02-scaffold-multi-agent.md) | Utiliser l'assistant d'extension Foundry pour échafauder le projet de base |
| 3 | [Configurer les Agents & l'Environnement](03-configure-agents.md) | Rédiger les instructions pour 4 agents, configurer l'outil MCP, définir les variables d'environnement |
| 4 | [Modèles d'Orchestration](04-orchestration-patterns.md) | Chaîne séquentielle, relais de contenu, et sémantique OU de WorkflowBuilder |
| 5 | [Tester Localement](05-test-locally.md) | Déboguer avec F5 et Agent Inspector, exécuter des tests de fumée avec CV + description de poste |
| 6 | [Déployer sur Foundry](06-deploy-to-foundry.md) | Construire un conteneur, pousser sur ACR, enregistrer un agent hébergé |
| 7 | [Vérifier dans le Playground](07-verify-in-playground.md) | Tester l'agent déployé dans VS Code et les playgrounds du portail Foundry |
| 8 | [Dépannage](08-troubleshooting.md) | Résoudre les problèmes courants multi-agent (erreurs MCP, sortie tronquée, versions de paquets) |
| 9 | [Résumé & Étapes Suivantes](09-summary.md) | Ce que vous avez construit, concepts clés appris, nettoyage, et où aller ensuite |

---

**Retour à :** [README du Lab 02](../README.md) · [Accueil de l'Atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->