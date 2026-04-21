# Problèmes connus

Ce document suit les problèmes connus avec l'état actuel du dépôt.

> Dernière mise à jour : 2026-04-15. Testé avec Python 3.13 / Windows dans `.venv_ga_test`.

---

## Verrouillages de paquets actuels (tous les trois agents)

| Paquet | Version actuelle |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(corrigé — voir KI-003)* |

---

## KI-001 — Blocage de la mise à jour GA 1.0.0 : `agent-framework-azure-ai` supprimé

**Statut :** Ouvert | **Gravité :** 🔴 Élevée | **Type :** Rupture

### Description

Le paquet `agent-framework-azure-ai` (verrouillé à `1.0.0rc3`) a été **supprimé/déprécié**
dans la version GA (1.0.0, sortie le 2026-04-02). Il est remplacé par :

- `agent-framework-foundry==1.0.0` — modèle d’agent hébergé par Foundry
- `agent-framework-openai==1.0.0` — modèle d’agent supporté par OpenAI

Les trois fichiers `main.py` importent `AzureAIAgentClient` depuis `agent_framework.azure`, ce qui
lance `ImportError` avec les paquets GA. L’espace de noms `agent_framework.azure` existe toujours
dans GA mais contient uniquement des classes pour Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — pas les agents Foundry.

### Erreur confirmée (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Fichiers affectés

| Fichier | Ligne |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` incompatible avec `agent-framework-core` GA

**Statut :** Ouvert | **Gravité :** 🔴 Élevée | **Type :** Rupture (bloqué en amont)

### Description

`azure-ai-agentserver-agentframework==1.0.0b17` (dernier) verrouille strictement
`agent-framework-core<=1.0.0rc3`. L’installation en parallèle avec `agent-framework-core==1.0.0` (GA)
force pip à **rétrograder** `agent-framework-core` à la version `rc3`, ce qui casse ensuite
`agent-framework-foundry==1.0.0` et `agent-framework-openai==1.0.0`.

L’appel `from azure.ai.agentserver.agentframework import from_agent_framework` utilisé par tous
les agents pour lier le serveur HTTP est également bloqué.

### Conflit de dépendances confirmé (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Fichiers affectés

Les trois fichiers `main.py` — à la fois l’import global et l’import dans la fonction `main()`.

---

## KI-003 — Le drapeau `agent-dev-cli --pre` n’est plus nécessaire

**Statut :** ✅ Corrigé (non bloquant) | **Gravité :** 🟢 Faible

### Description

Tous les fichiers `requirements.txt` incluaient auparavant `agent-dev-cli --pre` pour récupérer
la version préliminaire de la CLI. Depuis la sortie GA 1.0.0 le 2026-04-02, la version stable
de `agent-dev-cli` est maintenant disponible sans le drapeau `--pre`.

**Correction appliquée :** Le drapeau `--pre` a été retiré des trois fichiers `requirements.txt`.

---

## KI-004 — Les Dockerfiles utilisent `python:3.14-slim` (image de base pré-release)

**Statut :** Ouvert | **Gravité :** 🟡 Faible

### Description

Tous les `Dockerfile` utilisent `FROM python:3.14-slim` qui suit une version préliminaire de Python.
Pour les déploiements en production, cela devrait être fixé à une version stable (par exemple `python:3.12-slim`).

### Fichiers affectés

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Références

- [agent-framework-core sur PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry sur PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avis de non-responsabilité** :  
Ce document a été traduit à l’aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d’assurer l’exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour des informations critiques, une traduction professionnelle réalisée par un expert humain est recommandée. Nous déclinons toute responsabilité en cas de malentendus ou de mauvaises interprétations résultant de l’utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->