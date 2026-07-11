# Como ministrar esta sessão

Obrigado por ministrar esta sessão!

Antes de ministrar o workshop, por favor:

1. Leia este documento e todos os recursos incluídos na íntegra.
2. Assista à gravação da entrega da sessão e à apresentação completa do workshop.
3. Realize os dois laboratórios práticos completos em sua própria máquina **pelo menos uma vez** antes do evento.
4. Valide seu projeto Microsoft Foundry, implantações de modelo e cotas.
5. Entre em contato com o mantenedor se algo estiver claro.

---

## Resumo do arquivo

| Recurso                      | Link                                                                             | Descrição                                                                                |
|-----------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Apresentação do workshop     | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                    | Slides da apresentação deste workshop com notas do apresentador e vídeos de demonstração  |
| Gravação da entrega da sessão | _A ser fornecida pelo mantenedor_                                               | Gravação da introdução e apresentação dos slides do workshop                             |
| Gravação completa do workshop | _A ser fornecida pelo mantenedor_                                               | Gravação completa dos dois laboratórios do ponto de vista de um participante             |
| Documentação do workshop     | [Repositório](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repositório fonte, README dos laboratórios, módulos passo a passo                       |
| Laboratório 01 - agente único | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Laboratório prático: construir, testar e implantar o agente hospedado *Explain Like I'm an Executive* |
| Laboratório 02 - fluxo multi-agentes | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Laboratório prático: construir o fluxo de trabalho *Resume to Job Fit Evaluator* com 4 agentes             |
| Demo 1: Agente Executivo     | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                            | Demo do Lab 01: traduzir jargão técnico em um resumo executivo                            |
| Demo 2: Avaliador de Ajuste Currículo-Emprego | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)    | Demo do Lab 02: fluxo com 4 agentes que avalia ajuste currículo-emprego e gera recomendações  |

> **Nota para treinadores:** A apresentação e os links dos vídeos serão adicionados assim que as gravações forem publicadas. Até lá, contate o mantenedor (veja [Contatos](#contatos)) para obter os recursos mais recentes.

---

## Começando

Este workshop ensina desenvolvedores a construir, testar e implantar agentes de IA no **Microsoft Foundry Agent Service** como **Agentes Hospedados** inteiramente pelo VS Code, usando a extensão **Microsoft Foundry Toolkit**.

O workshop é dividido em várias seções, incluindo slides, **2 demonstrações ao vivo** e **2 laboratórios práticos**.

### Duração

#### Entrega completa (aproximadamente 2 horas)

| Horário         | Descrição                                                          |
|-----------------|--------------------------------------------------------------------|
| 0:00 - 10:00    | Introdução: agentes hospedados, Foundry Agent Service e toolkit    |
| 10:00 - 20:00   | Demonstração: Agente Executivo de ponta a ponta                   |
| 20:00 - 60:00   | Lab 01 - agente único (construir, testar localmente, implantar, playground) |
| 60:00 - 110:00  | Lab 02 - fluxo multi-agentes (Avaliador de Ajuste Currículo-Emprego) |
| 110:00 - 120:00 | Encerramento, perguntas e respostas, e recursos para aprendizado contínuo |

#### Entrega curta (aproximadamente 75 minutos)

| Horário         | Descrição                                                      |
|----------------|----------------------------------------------------------------|
| 0:00 - 10:00   | Introdução e visão geral                                       |
| 10:00 - 20:00  | Demonstração: Agente Executivo                                |
| 20:00 - 70:00  | Apenas Lab 01 (indicar Lab 02 para estudo individual)          |
| 70:00 - 75:00  | Encerramento e perguntas e respostas                          |

### Preparação

| Recurso                       | Link                                                                                          | Descrição                                       |
|------------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------|
| Documentação do workshop      | [Repositório](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Documentação do workshop e código fonte         |
| Instruções do Lab 01          | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Laboratório prático: agente hospedado único     |
| Instruções do Lab 02          | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Laboratório prático: fluxo multi-agentes         |
| Checklist de pré-requisitos   | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Ferramentas, contas e acesso ao Azure necessários|
| Guia rápido para agentes hospedados (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Guia oficial para implantar um agente hospedado com `azd`  |
| Disponibilidade regional dos agentes hospedados | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Regiões suportadas para agentes hospedados (preview)       |

### Pré-requisitos para o treinador

Antes de ministrar, certifique-se de que você tem:

- Uma **assinatura Azure** com permissão para criar recursos (Proprietário ou Colaborador em um grupo de recursos).
- Acesso a um **projeto Microsoft Foundry** em uma [região que suporta agentes hospedados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Cota para **gpt-4.1** (ou **gpt-4.1-mini**) em seu projeto Foundry.
- As seguintes ferramentas instaladas:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Extensão Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opcional)
  - Python 3.10 ou superior

Execute o [Guia rápido para agentes hospedados com `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) pelo menos uma vez antes da entrega para ter um projeto Foundry, implantação de modelo e Registro de Contêiner Azure conhecidos bons para referência caso algum participante tenha dificuldades.

---

## Passagem pelos slides

O deck segue o mesmo fluxo dos laboratórios. Pontos sugeridos para falar em cada seção:

| Seção                      | Mensagem chave                                                                                               |
|----------------------------|-------------------------------------------------------------------------------------------------------------|
| Título e agenda           | Apresente o workshop como *VS Code para Foundry* sem necessidade de trocar de portal.                       |
| Por que agentes hospedados? | Runtime gerenciado, implantação via ACR, API `/responses` compatível com OpenAI, escopo para projetos Foundry.|
| Diagrama de arquitetura    | Explique a [arquitetura do README](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.      |
| Anatomia de um agente hospedado | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - o que cada arquivo faz.                          |
| Demonstração ao vivo: Agente Executivo | Troque para o VS Code e execute a demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) completa (veja [Demo 1](#demo-1-agente-executivo)). |
| Demonstração ao vivo: Avaliador de Ajuste Currículo-Emprego | Troque para o VS Code e execute a demo de 4 agentes [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (veja [Demo 2](#demo-2-avaliador-de-ajuste-currículo-emprego)). |
| Resumo do Lab 01          | Passe a palavra aos participantes. Aponte para [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Padrões multi-agentes     | Sequencial vs concorrente vs handoff - apresente antes do início do Lab 02.                                |
| Resumo do Lab 02          | Passe a palavra aos participantes. Aponte para [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Encerramento e recursos   | Links para aprendizado contínuo da seção [Recursos adicionais](#recursos-adicionais).                      |

---

## Demonstrações

Duas demonstrações ao vivo são incluídas na entrega. Reserve 10 minutos para cada uma.

| Demo                 | Lab  | Arquivos                                                                   | O que mostrar                                                |
|----------------------|------|---------------------------------------------------------------------------|-------------------------------------------------------------|
| Agente Executivo      | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Agente hospedado único; traduza jargão técnico em um resumo executivo |
| Avaliador Ajuste Currículo-Emprego | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orquestração com 4 agentes; avalia ajuste currículo-emprego e gera recomendação |

### Demo 1: Agente Executivo

Um agente autônomo em [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Use esta demo de 10 minutos antes do Lab 01.

1. Abra [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) e explique a definição do agente (prompt do sistema, modelo, framework).
2. Pressione `F5` para iniciar localmente o **Agent Inspector**.
3. Cole o prompt de exemplo do [README](../README.md#see-it-in-action) e mostre a resposta do resumo executivo.
4. Mostre [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) e [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) para explicar os artefatos de implantação.
5. Demonstre o fluxo de implantação (build Docker, push ACR, criação do agente hospedado) sem esperar pela conclusão.

### Demo 2: Avaliador de Ajuste Currículo-Emprego

Um fluxo de trabalho com 4 agentes em [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Use esta demo de 10 minutos antes do Lab 02.

1. Abra [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) e mostre como os quatro agentes estão conectados em uma orquestração sequencial.
2. Pressione `F5` para iniciar o **Agent Inspector** para o fluxo multi-agentes.
3. Cole uma descrição curta de vaga e um currículo de exemplo no chat do Inspector.
4. Explique a pipeline de quatro agentes: analisador de currículo, extrator de requisitos do trabalho, avaliador de ajuste e gerador de recomendação.
5. Aponte como a saída de cada sub-agente se torna o contexto do próximo agente, destacando o padrão de handoff.
6. Mostre [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) para comparar com o equivalente de agente único da Demo 1.

---

## Dicas para a entrega

- **Defina as expectativas cedo.** Agentes hospedados estão em prévia - informe desde o início as limitações de região e cotas para que os participantes não se surpreendam durante o laboratório.
- **Execute a tarefa de pré-requisitos primeiro.** Ambos os laboratórios incluem uma tarefa `Validate prerequisites` no VS Code - faça com que os participantes a executem antes de escrever qualquer código.
- **Mantenha o Agent Inspector visível.** A maioria dos momentos "aha" acontecem quando os participantes veem o tráfego local do endpoint `/responses` acender.
- **Tenha um projeto reserva.** Se o projeto Foundry de alguém atingir a cota, compartilhe um projeto pré-provisionado para o passo de implantação em vez de travar a sala.
- **Faça duplas entre os participantes.** O Lab 02 (multi-agente) fica muito mais fácil quando os participantes podem discutir a orquestração com um parceiro.
- **Use os módulos da documentação como checkpoints.** A pasta `docs/` de cada laboratório está dividida em 8 módulos numerados - use-os como pontos naturais para pausas.
- **Pré-baixe a imagem base do Docker** nas máquinas compartilhadas para evitar limites de taxa de registro.

---

## Solução de problemas durante a entrega

| Sintoma                                     | Primeira coisa a tentar                                                                                  |
|---------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector não conecta                   | Confirme que a porta `8088` está livre e que a tarefa `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` está rodando. |
| Depurador não conecta                         | Verifique se a porta `5679` está livre; reinicie o VS Code se `debugpy` já estiver ligado.                |
| `azd up` falha com erro de autenticação       | Execute `az login` e `azd auth login`, certifique-se de que o locatário correto está selecionado.         |
| Implantação trava no push para o ACR          | Verifique se o Docker Desktop está rodando e o usuário tem permissão `AcrPush` no registro.               |
| Modelo retorna 404 / deployment-not-found     | O nome da implantação no `agent.yaml` deve coincidir com a implantação no projeto Foundry.                |

| Agente hospedado travado em `Provisioning`    | Verifique se a região do projeto [suporta agentes hospedados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) e se há cota disponível. |
| Playground retorna 401                         | Reautentique a extensão Foundry a partir da barra de atividades do VS Code.                    |

Para orientações mais detalhadas, cada laboratório possui seu próprio documento `08-troubleshooting.md` - direcione os aprendizes para ele:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Personalizando esta sessão

Você está convidado a adaptar o workshop para seu público. Variações comuns:

- **Públicos de backend:** dedique mais tempo ao `agent.yaml`, Docker e ACR; encurte a demonstração do playground.
- **Públicos de cidadão-desenvolvedor:** permaneça na interface da extensão Foundry para scaffolding; reduza os passos pelo CLI.
- **Sessão única de 60 minutos:** ofereça apenas a introdução, demonstração e o Lab 01.
- **Formato só workshop (sem slides):** abra os dois READMEs dos laboratórios e use-os como roteiro principal.

Se você expandir os laboratórios, por favor contribua com as alterações via PR para que outros instrutores possam se beneficiar.

---

## Recursos adicionais

- [Documentação Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Visão geral dos agentes hospedados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Introdução rápida: implante seu primeiro agente hospedado (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Implantar um agente hospedado (como fazer)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit para VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contatos

Se você tiver dúvidas sobre como ministrar esta sessão, por favor abra uma issue no [repositório do workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) e marque o mantenedor.

| Função              | Nome           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Mantenedor / contato | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->