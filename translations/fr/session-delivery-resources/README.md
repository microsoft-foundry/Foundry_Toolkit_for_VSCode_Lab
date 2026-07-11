# Comment animer cette session

Merci d’animer cette session !

Avant d’animer l’atelier, veuillez :

1. Lire ce document et toutes les ressources incluses dans leur intégralité.
2. Regarder l’enregistrement de la présentation de la session et la démonstration complète de l’atelier.
3. Parcourir les deux laboratoires pratiques en intégralité sur votre propre machine **au moins une fois** avant l’événement.
4. Valider votre projet Microsoft Foundry, les déploiements de modèles, et les quotas.
5. Contacter le mainteneur si quelque chose n’est pas clair.

---

## Résumé des fichiers

| Ressource                    | Lien                                                                             | Description                                                                                    |
|-----------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Présentation de l'atelier   | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                   | Diapositives de présentation pour cet atelier avec notes du présentateur et vidéos de démonstration intégrées |
| Enregistrement de la session | _Fourni par le mainteneur_                                                      | Enregistrement de l’introduction de l’atelier et passage des diapositives                      |
| Enregistrement complet de l’atelier | _Fourni par le mainteneur_                                                      | Enregistrement complet des deux laboratoires du point de vue d’un apprenant                     |
| Documentation de l’atelier  | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Dépôt source, README des laboratoires, modules étape par étape                                |
| Laboratoire 01 - agent unique | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Laboratoire pratique : construire, tester et déployer l’agent *Explain Like I'm an Executive* hébergé |
| Laboratoire 02 - workflow multi-agent | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Laboratoire pratique : construire le workflow 4 agents *Resume to Job Fit Evaluator*            |
| Démo 1 : Agent Exécutif      | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                            | Démo du labo 01 : traduire le jargon technique en résumé exécutif                              |
| Démo 2 : Évaluateur adéquation CV-emploi | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)   | Démo du labo 02 : workflow 4 agents qui évalue l'adéquation CV-emploi et génère des recommandations |

> **Note pour les formateurs :** La présentation et les liens vidéo seront ajoutés une fois les enregistrements publiés. Jusqu'à ce moment, contactez le mainteneur (voir [Contacts](#contacts)) pour obtenir les derniers matériels.

---

## Démarrage

Cet atelier apprend aux développeurs comment construire, tester et déployer des agents IA sur le **Microsoft Foundry Agent Service** en tant qu’**agents hébergés**, entièrement depuis VS Code, en utilisant l’extension **Microsoft Foundry Toolkit**.

L’atelier est divisé en plusieurs sections incluant des diapositives, **2 démonstrations en direct**, et **2 laboratoires pratiques**.

### Durée

#### Session complète (environ 2 heures)

| Temps           | Description                                                         |
|-----------------|---------------------------------------------------------------------|
| 0:00 - 10:00    | Introduction : agents hébergés, Foundry Agent Service et la boîte à outils |
| 10:00 - 20:00   | Démo : Agent Exécutif de bout en bout                                |
| 20:00 - 60:00   | Labo 01 - agent unique (construire, tester localement, déployer, playground) |
| 60:00 - 110:00  | Labo 02 - workflow multi-agent (Évaluateur adéquation CV-emploi)    |
| 110:00 - 120:00 | Conclusion, questions-réponses et ressources pour aller plus loin    |

#### Session courte (environ 75 minutes)

| Temps          | Description                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Introduction et aperçu                                      |
| 10:00 - 20:00 | Démo : Agent Exécutif                                       |
| 20:00 - 70:00 | Labo 01 seulement (orienter les participants vers le Labo 02 en autonomie) |
| 70:00 - 75:00 | Conclusion et questions-réponses                            |

### Préparation

| Ressource                      | Lien                                                                                          | Description                              |
|-------------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------|
| Documentation de l’atelier     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Documentation et source de l’atelier     |
| Instructions Labo 01           | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Laboratoire pratique : agent hébergé unique |
| Instructions Labo 02           | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Laboratoire pratique : workflow multi-agent |
| Liste de prérequis            | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Outils, comptes et accès Azure nécessaires |
| Démarrage rapide agents hébergés (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Démarrage officiel du déploiement d’un agent hébergé avec `azd` |
| Disponibilité des régions pour agents hébergés | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Régions supportées pour agents hébergés (aperçu) |

### Prérequis pour le formateur

Avant d’animer, assurez-vous de disposer de :

- Un **abonnement Azure** avec la permission de créer des ressources (propriétaire ou contributeur sur un groupe de ressources).
- Accès à un **projet Microsoft Foundry** dans une [région qui supporte les agents hébergés](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota pour **gpt-4.1** (ou **gpt-4.1-mini**) dans votre projet Foundry.
- Les outils suivants installés :
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Extension Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Optionnel)
  - Python 3.10 ou version ultérieure

Exécutez le [démarrage rapide des agents hébergés avec `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) au moins une fois avant la session pour avoir un projet Foundry, un déploiement de modèle et un registre Azure Container Registry fonctionnels à référencer en cas de blocage d’un apprenant.

---

## Parcours des diapositives

La présentation suit le même déroulement que les laboratoires. Points clés suggérés pour chaque section :

| Section                    | Message clé                                                                                                   |
|----------------------------|--------------------------------------------------------------------------------------------------------------|
| Titre et agenda            | Positionner l’atelier comme *VS Code vers Foundry* sans changer de portail.                                 |
| Pourquoi les agents hébergés ? | Runtime managé, déploiement basé sur ACR, API `/responses` compatible OpenAI, avec périmètre sur les projets Foundry. |
| Schéma d’architecture      | Parcourir la [architecture du README](../README.md#architecture) : squelette, Inspector, ACR, Agent Service.   |
| Anatomie d’un agent hébergé | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` – rôle de chaque fichier.                           |
| Démo en direct : Agent Exécutif | Passer à VS Code et lancer la démo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) de bout en bout (voir [Démo 1](#démo-1-agent-exécutif)). |
| Démo en direct : Évaluateur adéquation CV-emploi | Passer à VS Code et lancer la démo 4 agents [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (voir [Démo 2](#démo-2-évaluateur-adéquation-cv-emploi)). |
| Brève présentation Labo 01 | Passer la main aux apprenants. Indiquer [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Patterns multi-agents      | Séquentiel vs concurrent vs transfert – aperçu avant de démarrer le Labo 02.                                |
| Brève présentation Labo 02 | Passer la main aux apprenants. Indiquer [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Conclusion et ressources   | Liens pour continuer l’apprentissage depuis la section [Ressources supplémentaires](#ressources-supplémentaires). |

---

## Démos

Deux démos en direct sont incluses dans la présentation. Allouez 10 minutes pour chacune.

| Démo                  | Labo  | Fichiers                                                            | À montrer                                                    |
|-----------------------|-------|--------------------------------------------------------------------|-------------------------------------------------------------|
| Agent Exécutif        | Labo 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Agent hébergé unique ; traduire le jargon technique en résumé exécutif |
| Évaluateur adéquation CV-emploi | Labo 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orchestration 4 agents ; évaluer l’adéquation CV-emploi et générer une recommandation |

### Démo 1 : Agent Exécutif

Un agent autonome dans [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Utiliser comme démo de 10 minutes avant le Labo 01.

1. Ouvrir [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) et parcourir la définition de l’agent (invite système, modèle, framework).
2. Appuyer sur `F5` pour lancer localement l’**Agent Inspector**.
3. Coller l’invite d’exemple depuis le [README](../README.md#see-it-in-action) et montrer la réponse du résumé exécutif.
4. Montrer [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) et [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) pour expliquer les artefacts de déploiement.
5. Démontrer le flux de déploiement (construction Docker, push ACR, création agent hébergé) sans attendre la fin.

### Démo 2 : Évaluateur adéquation CV-emploi

Un workflow 4 agents dans [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Utiliser comme démo de 10 minutes avant le Labo 02.

1. Ouvrir [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) et montrer comment les quatre agents sont reliés dans une orchestration séquentielle.
2. Appuyer sur `F5` pour lancer l’**Agent Inspector** pour le workflow multi-agent.
3. Coller une courte description de poste et un CV d’exemple dans la discussion de l’Inspector.
4. Parcourir les quatre étapes du pipeline : parseur de CV, extracteur des exigences de poste, évaluateur d’adéquation, rédacteur de recommandations.
5. Souligner comment la sortie de chaque sous-agent devient le contexte pour l’agent suivant, mettant en avant le pattern de transfert.
6. Montrer [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) pour comparer avec l’équivalent agent unique de la Démo 1.

---

## Conseils pour l’animation

- **Fixez les attentes dès le départ.** Les agents hébergés sont en aperçu - précisez les limites régionales et les quotas au début pour éviter les surprises en pleine session.
- **Exécutez d’abord la tâche des prérequis.** Les deux laboratoires proposent une tâche VS Code `Validate prerequisites` - faites-la lancer par les participants avant toute écriture de code.
- **Gardez l’Agent Inspector visible.** La plupart des moments « aha » arrivent quand les apprenants voient l’aller-retour local `/responses` s’éclairer.
- **Ayez un projet de secours.** Si un apprenant atteint une limite de quota dans son projet Foundry, fournissez un projet pré-provisionné pour la phase de déploiement afin de ne pas bloquer la salle.
- **Faites travailler les participants par paires.** Le labo 02 (multi-agent) est nettement plus facile quand les apprenants peuvent discuter de l’orchestration avec un partenaire.
- **Utilisez les modules docs comme points de contrôle.** Chaque labo a un dossier `docs/` divisé en 8 modules numérotés - utilisez-les comme points naturels de pause.
- **Préchauffez l’image Docker de base** sur les machines de laboratoire partagées pour éviter les limites de taux du registre.

---

## Dépannage pendant l’animation

| Symptôme                                    | Première chose à essayer                                                                                  |
|--------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Agent Inspector ne peut pas se connecter   | Vérifier que le port `8088` est libre et que la tâche `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` tourne. |
| Le débogueur ne s’attache pas               | Vérifier que le port `5679` est libre ; redémarrer VS Code si `debugpy` est déjà lié.                     |
| `azd up` échoue avec une erreur d’authentification | Exécuter `az login` et `azd auth login`, s’assurer que le bon locataire est sélectionné.                     |
| Le déploiement bloque au push ACR           | Vérifier que Docker Desktop est lancé et que l’utilisateur a le rôle `AcrPush` sur le registre.           |
| Modèle retourne 404 / deployment-not-found  | Le nom du déploiement dans `agent.yaml` doit correspondre à celui dans le projet Foundry.                 |

| Agent hébergé bloqué en `Provisioning`       | Vérifiez que la région du projet [prend en charge les agents hébergés](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) et que le quota est disponible. |
| Playground renvoie 401                        | Ré-authentifiez l'extension Foundry depuis la barre d'activité de VS Code.                          |

Pour une aide plus approfondie, chaque laboratoire comprend son propre fichier `08-troubleshooting.md` – orientez les apprenants vers celui-ci :

- Lab 01 : [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02 : [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Personnalisation de cette session

Vous pouvez adapter l’atelier pour votre public. Variantes courantes :

- **Public backend :** consacrez plus de temps à `agent.yaml`, Docker et ACR ; réduisez la démonstration playground.
- **Public développeur citoyen :** restez dans l’interface de l’extension Foundry pour le scaffolding ; réduisez les étapes CLI.
- **Créneau unique de 60 minutes :** livrez uniquement l’introduction, la démo et le Lab 01.
- **Format atelier uniquement (sans slides) :** ouvrez les deux README des labs et utilisez-les comme script principal.

Si vous étendez les labs, merci de contribuer vos modifications via une PR pour en faire bénéficier les autres formateurs.

---

## Ressources supplémentaires

- [Documentation Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Présentation des agents hébergés](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Démarrage rapide : déployez votre premier agent hébergé (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Déployer un agent hébergé (mode d’emploi)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit pour VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contacts

Si vous avez des questions concernant la conduite de cette session, veuillez ouvrir un ticket sur le [répertoire de l’atelier](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) et taguer le mainteneur.

| Rôle               | Nom            | GitHub                                                      |
|--------------------|----------------|-------------------------------------------------------------|
| Mainteneur / contact| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)          |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->