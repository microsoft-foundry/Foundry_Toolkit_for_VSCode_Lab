# Lab 02 - Workflow Multi-Agents : Évaluateur Adaptation CV → Poste

## Parcours d'apprentissage complet

Cette documentation vous guide pour construire, tester et déployer un **workflow multi-agents** qui évalue l'adéquation CV-poste en utilisant quatre agents spécialisés orchestrés via **WorkflowBuilder**.

> **Prérequis :** Terminer le [Lab 01 - Agent Unique](../../lab01-single-agent/README.md) avant de commencer le Lab 02.

---

## Modules

| # | Module | Ce que vous ferez |
|---|--------|-------------------|
| 0 | [Prérequis](00-prerequisites.md) | Vérifier la complétion du Lab 01, comprendre les concepts multi-agents |
| 1 | [Comprendre l’Architecture Multi-Agents](01-understand-multi-agent.md) | Apprendre WorkflowBuilder, rôles des agents, graph d’orchestration |
| 2 | [Création de la Structure du Projet Multi-Agents](02-scaffold-multi-agent.md) | Utiliser l’extension Foundry pour générer un workflow multi-agents |
| 3 | [Configurer Agents & Environnement](03-configure-agents.md) | Écrire les instructions pour 4 agents, configurer l’outil MCP, définir les variables d’environnement |
| 4 | [Patrons d’Orchestration](04-orchestration-patterns.md) | Explorer fan-out parallèle, agrégation séquentielle et autres patrons |
| 5 | [Tester Localement](05-test-locally.md) | Déboguer avec Agent Inspector (F5), lancer des tests rapides avec CV + description de poste |
| 6 | [Déployer sur Foundry](06-deploy-to-foundry.md) | Construire le conteneur, pousser sur ACR, enregistrer l’agent hébergé |
| 7 | [Vérifier dans Playground](07-verify-in-playground.md) | Tester l’agent déployé dans VS Code et les playgrounds du portail Foundry |
| 8 | [Dépannage](08-troubleshooting.md) | Corriger les problèmes courants multi-agents (erreurs MCP, sortie tronquée, versions de paquets) |

---

## Durée estimée

| Niveau d’expérience | Durée |
|---------------------|-------|
| Lab 01 terminé récemment | 45-60 minutes |
| Quelques expériences avec Azure AI | 60-90 minutes |
| Première fois avec multi-agents | 90-120 minutes |

---

## Architecture en un coup d’œil

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Retour à :** [Lab 02 README](../README.md) · [Accueil Atelier](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :  
Ce document a été traduit à l’aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d’assurer la précision, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour des informations critiques, une traduction humaine professionnelle est recommandée. Nous ne sommes pas responsables des malentendus ou des mauvaises interprétations découlant de l’utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->