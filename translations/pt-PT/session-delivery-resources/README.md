# Como realizar esta sessão

Obrigado por realizar esta sessão!

Antes de realizar o workshop, por favor:

1. Leia este documento e todos os recursos incluídos na sua totalidade.
2. Veja a gravação da entrega da sessão e a explicação do workshop de ponta a ponta.
3. Faça ambos os laboratórios práticos na sua própria máquina **pelo menos uma vez** antes do evento.
4. Valide o seu projeto Microsoft Foundry, implantações de modelos e quotas.
5. Contacte o mantenedor se algo não estiver claro.

---

## Resumo do ficheiro

| Recurso                        | Ligação                                                                          | Descrição                                                                                  |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Apresentação do workshop       | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                   | Slides da apresentação deste workshop com notas do apresentador e vídeos de demonstração incorporados  |
| Gravação da entrega da sessão  | _A ser fornecida pelo mantenedor_                                               | Gravação introdutória do workshop e explicação dos slides                                 |
| Gravação do workshop de ponta a ponta | _A ser fornecida pelo mantenedor_                                               | Gravação completa dos dois laboratórios na perspetiva de um participante                  |
| Documentação do workshop       | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repositório fonte, READMEs dos laboratórios, módulos passo a passo                       |
| Laboratório 01 - agente único  | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Laboratório prático: construir, testar e implantar o agente hóspede *Explique como se fosse um executivo*  |
| Laboratório 02 - fluxo multi-agente | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Laboratório prático: construir o fluxo com 4 agentes *Avaliador de Compatibilidade de Currículo para Emprego* |
| Demonstração 1: Agente Executivo             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Demonstração do Lab 01: traduzir linguagem técnica em resumo executivo                         |
| Demonstração 2: Avaliador de Compatibilidade Currículo-Emprego | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demonstração do Lab 02: fluxo com 4 agentes que avalia compatibilidade e gera recomendações    |

> **Nota para formadores:** O deck de slides e os links dos vídeos serão adicionados assim que as gravações forem publicadas. Até lá, contacte o mantenedor (ver [Contactos](#contactos)) para obter os ativos mais recentes.

---

## Começar

Este workshop ensina os programadores a construir, testar e implantar agentes de IA para o **Microsoft Foundry Agent Service** como **Agentes Hospedados** inteiramente a partir do VS Code, utilizando a extensão **Microsoft Foundry Toolkit**.

O workshop está dividido em várias secções, incluindo slides, **2 demonstrações ao vivo** e **2 laboratórios práticos**.

### Duração

#### Entrega completa (cerca de 2 horas)

| Tempo          | Descrição                                                           |
|----------------|---------------------------------------------------------------------|
| 0:00 - 10:00   | Introdução: agentes hospedados, Foundry Agent Service e toolkit     |
| 10:00 - 20:00  | Demonstração: Agente Executivo de ponta a ponta                     |
| 20:00 - 60:00  | Lab 01 - agente único (construir, testar localmente, implantar, playground) |
| 60:00 - 110:00 | Lab 02 - fluxo multi-agente (Avaliador de Compatibilidade Currículo-Emprego) |
| 110:00 - 120:00| Conclusão, Q&A, e recursos para aprendizagem contínua               |

#### Entrega curta (cerca de 75 minutos)

| Tempo          | Descrição                                                  |
|----------------|------------------------------------------------------------|
| 0:00 - 10:00   | Introdução e visão geral                                   |
| 10:00 - 20:00  | Demonstração: Agente Executivo                            |
| 20:00 - 70:00  | Apenas Lab 01 (indicar aos participantes o Lab 02 como autoaprendizagem) |
| 70:00 - 75:00  | Conclusão e sessão de perguntas                           |

### Preparação

| Recurso                      | Ligação                                                                                     | Descrição                                       |
|-----------------------------|---------------------------------------------------------------------------------------------|------------------------------------------------|
| Documentação do workshop     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)           | Documentação do workshop e código-fonte         |
| Instruções do Lab 01         | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                              | Laboratório prático: agente hóspede único       |
| Instruções do Lab 02         | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                | Laboratório prático: fluxo multi-agente         |
| Lista de pré-requisitos      | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)              | Ferramentas, contas e acesso Azure necessários  |
| Guia rápido de agentes hospedados (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Guia oficial para implantar um agente hospedado com `azd` |
| Disponibilidade regional dos agentes hospedados | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Regiões suportadas para agentes hospedados (pré-visualização) |

### Pré-requisitos para formadores

Antes de realizar a sessão, certifique-se que tem:

- Uma **subscrição Azure** com permissão para criar recursos (Proprietário ou Contribuidor num grupo de recursos).
- Acesso a um **projeto Microsoft Foundry** numa [região que suporta agentes hospedados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota para **gpt-4.1** (ou **gpt-4.1-mini**) no seu projeto Foundry.
- As ferramentas seguintes instaladas:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Extensão Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opcional)
  - Python 3.10 ou superior

Execute o [guia rápido de agentes hospedados com `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) pelo menos uma vez antes da entrega para ter um projeto Foundry válido, implantação de modelo e Azure Container Registry conhecidos para referência caso um participante fique bloqueado.

---

## Explicação dos slides

O deck segue o mesmo fluxo dos laboratórios. Pontos sugeridos a abordar para cada secção:

| Secção                       | Mensagem chave                                                                                              |
|-----------------------------|------------------------------------------------------------------------------------------------------------|
| Título e agenda              | Apresente o workshop como *VS Code para Foundry* sem necessidade de mudar de portal.                        |
| Porquê agentes hospedados?  | Runtime gerido, implantação baseada em ACR, API `/responses` compatível com OpenAI, com escopo para projetos Foundry. |
| Diagrama da arquitetura     | Explique a [arquitetura do README](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.      |
| Anatomia de um agente hospedado | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - o que cada ficheiro faz.                      |
| Demonstração ao vivo: Agente Executivo | Mude para VS Code e execute de ponta a ponta a demo em [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) (ver [Demo 1](#demonstração-1-agente-executivo)). |
| Demonstração ao vivo: Avaliador de Compatibilidade Currículo-Emprego | Mude para VS Code e execute a demo de 4 agentes em [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (ver [Demo 2](#demonstração-2-avaliador-de-compatibilidade-currículo-emprego)). |
| Resumo do Lab 01             | Passe a palavra aos participantes. Aponte para [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Padrões multi-agente         | Sequencial vs concorrente vs passagem de tarefas - introdução antes de começar o Lab 02.                   |
| Resumo do Lab 02             | Passe a palavra aos participantes. Aponte para [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Conclusão e recursos         | Ligações para aprendizagem contínua na secção de [Recursos adicionais](#recursos-adicionais).              |

---

## Demonstrações

Duas demonstrações ao vivo estão incluídas na entrega. Dedique 10 minutos a cada uma.

| Demonstração | Laboratório | Ficheiros                                                                                           | O que mostrar                                           |
|-------------|-------------|---------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| Agente Executivo | Lab 01     | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)                      | Agente hóspede único; traduzir jargão técnico em resumo executivo |
| Avaliador de Compatibilidade Currículo-Emprego | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orquestração com 4 agentes; avaliar compatibilidade e gerar recomendação      |

### Demonstração 1: Agente Executivo

Um agente autónomo em [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Use isto como uma demonstração de 10 minutos antes do Lab 01.

1. Abra [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) e explique a definição do agente (prompt do sistema, modelo, framework).
2. Prima `F5` para lançar o **Agent Inspector** localmente.
3. Cole o prompt de exemplo do [README](../README.md#see-it-in-action) e mostre a resposta do resumo executivo.
4. Mostre [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) e [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) para explicar os artefactos de implantação.
5. Demonstre o fluxo de implantação (Docker build, push para ACR, criação do agente hospedado) sem aguardar a conclusão.

### Demonstração 2: Avaliador de Compatibilidade Currículo-Emprego

Um fluxo com 4 agentes em [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Use isto como uma demonstração de 10 minutos antes do Lab 02.

1. Abra [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) e mostre como os quatro agentes estão ligados numa orquestração sequencial.
2. Prima `F5` para lançar o **Agent Inspector** para o fluxo multi-agente.
3. Cole uma breve descrição do trabalho e um currículo de exemplo no chat do Inspector.
4. Explique a pipeline dos quatro agentes: parser de currículo, extrator de requisitos do trabalho, avaliador de compatibilidade e escritor de recomendações.
5. Aponte como a saída de cada sub-agente se torna o contexto do agente seguinte, destacando o padrão de passagem.
6. Mostre [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) para comparar com o agente único do Demo 1.

---

## Dicas para a entrega

- **Defina expectativas desde cedo.** Agentes hospedados estão em pré-visualização - destaque os limites regionais e quotas inicialmente para evitar surpresas no meio do laboratório.
- **Execute a tarefa de pré-requisitos primeiro.** Ambos os laboratórios incluem uma tarefa VS Code `Validate prerequisites` - faça os participantes executá-la antes de começar a codificar.
- **Mantenha o Agent Inspector visível.** A maioria dos momentos "aha" acontecem quando os participantes veem o ciclo local `/responses` acender.
- **Tenha um projeto de reserva.** Se o projeto Foundry de um participante atingir o limite de quota, partilhe um projeto pré-provisionado para a etapa de implantação em vez de atrasar a sessão.
- **Emparelhe os participantes.** O Lab 02 (multi-agente) é consideravelmente mais fácil quando os participantes podem discutir a orquestração com um parceiro.
- **Use os módulos de documentação como pontos de verificação.** A pasta `docs/` de cada laboratório está dividida em 8 módulos numerados - use-os como pontos naturais de pausa.
- **Faça o pré-download da imagem base Docker** nas máquinas de laboratório partilhadas para evitar limites de taxa do registo.

---

## Resolução de problemas durante a entrega

| Sintoma                                     | Primeira coisa a tentar                                                                          |
|--------------------------------------------|------------------------------------------------------------------------------------------------|
| Agent Inspector não consegue conectar       | Confirme que a porta `8088` está livre e que a tarefa `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` está a correr. |
| O depurador não consegue anexar              | Verifique se a porta `5679` está livre; reinicie o VS Code se o `debugpy` já estiver ligado.    |
| `azd up` falha com erro de autenticação      | Execute `az login` e `azd auth login`, assegure que o tenant correto está selecionado.          |
| Implantação fica bloqueada no push para ACR | Verifique se o Docker Desktop está a correr e se o utilizador tem permissão `AcrPush` no registo. |
| Modelo retorna 404 / deployment-not-found    | O nome da implantação do modelo em `agent.yaml` deve coincidir com a implantação no projeto Foundry. |

| O agente hospedado está bloqueado em `Provisioning`         | Verifique se a região do projeto [suporta agentes hospedados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) e se há quota disponível. |
| O playground retorna 401                                    | Reautentique a extensão Foundry a partir da barra de atividades do VS Code.                                     |

Para uma orientação mais aprofundada, cada laboratório contém o seu próprio documento `08-troubleshooting.md` - encaminhe os formandos para lá:

- Laboratório 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Laboratório 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Personalizar esta sessão

Está à vontade para adaptar o workshop ao seu público. Variações comuns:

- **Públicos de backend:** dedique mais tempo ao `agent.yaml`, Docker, e ACR; reduza a demonstração do playground.
- **Públicos de cidadãos-desenvolvedores:** permaneça na interface da extensão Foundry para scaffoldings; reduza os passos da CLI.
- **Sessão de 60 minutos em uma única faixa:** apresente apenas a introdução, demonstração e o Laboratório 01.
- **Formato apenas workshop (sem slides):** abra ambos os READMEs dos laboratórios e use-os como roteiro principal.

Se estender os laboratórios, por favor contribua com as alterações através de PR para que outros formadores beneficiem.

---

## Recursos adicionais

- [Documentação Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Visão geral dos agentes hospedados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Início rápido: implemente o seu primeiro agente hospedado (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Implantar um agente hospedado (como fazer)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit para VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contactos

Se tiver dúvidas sobre como apresentar esta sessão, por favor abra uma issue no [repositório do workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) e marque o mantenedor.

| Função              | Nome           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Mantenedor / contacto| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->