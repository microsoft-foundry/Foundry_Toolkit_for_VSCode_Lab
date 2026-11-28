# Módulo 9 - Resumo e Próximos Passos

⏱️ ~5 min

**Parabéns!** Você construiu, testou e (se estiver no Caminho A) implantou um fluxo de trabalho multiagente usando Microsoft Foundry e o Foundry Toolkit para VS Code.

---

## O que você construiu

O **Avaliação de Compatibilidade Currículo → Vaga** - um fluxo de trabalho multiagente hospedado que:
- Recebe um currículo + descrição da vaga via HTTP (`POST /responses`)
- Executa quatro agentes especializados em uma pipeline sequencial - cada agente transmite os dados que seu sucessor precisa
- Retorna uma pontuação de compatibilidade (0–100 com detalhamento), uma lista de lacunas de habilidades e certificações, e um roteiro de aprendizado personalizado com links reais do Microsoft Learn para cada lacuna
- Chama o servidor Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) para buscar recursos oficiais de aprendizado para cada lacuna identificada
- Executa como um único agente hospedado conteinerizado no Microsoft Foundry Agent Service

---

## Conceitos chave aprendidos

| Conceito | O que você praticou |
|---------|-------------------|
| **Orquestração multiagente** | `WorkflowBuilder` pipeline sequencial com `add_edge()` |
| **Especialização de agentes** | Quatro agentes focados superam um agente de uso geral |
| **Padrão Content Router** | ResumeParser também funciona como um roteador - preserva o texto do JD em uma seção `[JOB DESCRIPTION PASS-THROUGH]` para que agentes posteriores possam acessá-lo (necessário porque `context_mode="last_agent"` significa que só o `start_executor` vê a mensagem bruta do usuário) |
| **Padrão Content Relay** | O agente JD encaminha `[PARSED RESUME PASS-THROUGH]` para frente para que o MatchingAgent receba ambos os perfis; evita o gatilho duplo com semântica OU que gráficos de fan-in causam |
| **Integração com ferramenta MCP** | `@tool` + `streamable_http_client` chamando um servidor MCP externo |
| **Ciclo de vida do Agente Hospedado** | Estruturar → Configurar → Testar localmente → Implantar → Verificar na nuvem |
| **`context_mode="last_agent"`** | Cada executor vê apenas a saída do seu predecessor direto |
| **Workflow do Foundry Toolkit** | Assistente de scaffold, Inspetor de Agentes, Visualizador de Workflow, implantação com um clique |

---

## O que você completou

<details open>
<summary><strong>🅰️ Caminho A - assinatura Foundry</strong></summary>

- [x] Verificou a configuração do Lab 01: projeto, modelo e RBAC ainda ativos
- [x] Criou um projeto multiagente usando o template Workflows
- [x] Escreveu quatro conjuntos de instruções para agentes (ResumeParser, Agente JD, MatchingAgent, GapAnalyzer)
- [x] Integração da ferramenta Microsoft Learn MCP com `streamable_http_client`
- [x] Conectou o gráfico do workflow com `WorkflowBuilder` (pipeline sequencial com retransmissão de conteúdo)
- [x] Testou localmente com 2 testes smoke (Inspetor de Agentes) - pontuação de compatibilidade, cartões de lacunas e URLs MCP
- [x] Implantou no Foundry Agent Service (conteinerizado, identidade gerenciada)
- [x] Verificou no playground em nuvem - consistência estrutural com resultados locais

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local</strong></summary>

- [x] Verificou a configuração do Lab 01: Foundry Local rodando com modelo local
- [x] Criou um projeto multiagente usando o template Workflows
- [x] Escreveu quatro conjuntos de instruções para agentes e conectou o gráfico do workflow
- [x] Integração da ferramenta Microsoft Learn MCP
- [x] Testou localmente com 2 testes smoke
- [x] Validou comportamento multiagente sem precisar de recursos na nuvem

</details>

---

## Próximos passos

### Continue aprendendo

| Recurso | Descrição |
|----------|-------------|
| **[Referência do Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentação da API para `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catálogo da ferramenta MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Conecte agentes a outros servidores MCP (Bing, GitHub, customizados) |
| **[Adicionar conhecimento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Fundamentar agentes com documentos, repositórios vetoriais ou busca Bing |
| **[Avaliações Foundry](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Meça a qualidade dos agentes em escala com avaliadores automáticos |
| **[Documentação Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referência completa da plataforma |
| **[Foundry Toolkit - Novidades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas da versão da extensão e changelog |

### Ideias para estender este workflow

- **Adicionar um 5º agente** - Um treinador de entrevistas que gera perguntas prováveis com base no relatório de lacunas
- **Adicionar uma ferramenta de fundamentação Bing** - Permita que o agente JD pesquise vagas similares para enriquecer os requisitos
- **Conectar a um banco de currículos** - Buscar perfis de candidatos de um banco de dados via um `@tool` customizado
- **Experimentar diferentes modelos** - Comparar qualidade e latência da saída de `gpt-4.1` vs. `gpt-4.1-mini`
- **Avaliar com Foundry** - Use o recurso Avaliações para pontuar relatórios de compatibilidade contra um conjunto de dados padrão

### Para usuários do Caminho B: Faça upgrade para implantação na nuvem

Quando estiver pronto para implantar na nuvem:
1. Obtenha uma assinatura Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Lab 01, Módulo 01](../../lab01-single-agent/docs/01-setup.md) (crie projeto, implante modelo, atribua RBAC)
3. Atualize seu `.env` com o endpoint do projeto Foundry e nome da implantação do modelo
4. Continue a partir do [Módulo 06 - Implantar no Foundry](06-deploy-to-foundry.md)

---

## Limpeza de recursos (opcional)

Se você quiser remover os recursos do Azure criados durante este workshop:

### Opção 1: Excluir o grupo de recursos (remove tudo)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opção 2: Excluir apenas o agente hospedado

1. Abra [ai.azure.com](https://ai.azure.com) → seu projeto → **Build** → **Agents**.
2. Encontre **PersonalCareerCopilot** → clique em **Delete**.

### Opção 3: Excluir a implantação do modelo

1. Na barra lateral do Foundry, expanda seu projeto → **Models**.
2. Clique com o botão direito na implantação do modelo → **Delete**.

> **Nota sobre custo:** Agentes hospedados só geram custo enquanto estão rodando. Se você parar ou excluir o agente, não há cobrança contínua. A implantação do modelo pode gerar uma pequena cobrança por capacidade reservada - exclua se tiver terminado.

---

**Anterior:** [08 - Solução de Problemas](08-troubleshooting.md) · **Início:** [README do Lab 02](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->