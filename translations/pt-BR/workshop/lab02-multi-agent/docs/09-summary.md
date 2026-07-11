# Módulo 9 - Resumo & Próximos Passos

⏱️ ~5 min

**Parabéns!** Você construiu, testou e (se no Caminho A) implantou um fluxo de trabalho multi-agente usando Microsoft Foundry e o Foundry Toolkit para VS Code.

---

## O que você construiu

O **Avaliador de Compatibilidade Currículo → Vaga** - um fluxo de trabalho multi-agente hospedado que:
- Recebe um currículo + descrição da vaga via HTTP (`POST /responses`)
- Executa quatro agentes especializados em uma pipeline sequencial - cada agente repassa os dados que seu sucessor precisa
- Retorna uma pontuação de compatibilidade (0–100 com detalhamento), uma lista de lacunas de habilidades e certificações, e um roteiro de aprendizado personalizado com links reais do Microsoft Learn para cada lacuna
- Chama o servidor Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) para obter recursos oficiais de aprendizado para cada lacuna identificada
- Executa como um agente hospedado em container único no Microsoft Foundry Agent Service

---

## Conceitos chave aprendidos

| Conceito | O que você praticou |
|---------|-------------------|
| **Orquestração multi-agente** | Pipeline sequencial com `WorkflowBuilder` e `add_edge()` |
| **Especialização do agente** | Quatro agentes focados superam um agente de propósito geral |
| **Padrão Content Router** | ResumeParser funciona também como um roteador - preserva o texto da descrição da vaga em uma seção `[JOB DESCRIPTION PASS-THROUGH]` para que agentes downstream possam acessá-la (necessário porque `context_mode="last_agent"` significa que apenas o `start_executor` vê a mensagem original do usuário) |
| **Padrão Content Relay** | O agente de descrição da vaga (JD Agent) retransmite `[PARSED RESUME PASS-THROUGH]` adiante para que MatchingAgent receba ambos os perfis; evita o disparo duplo semântico OR que grafos fan-in causam |
| **Integração da ferramenta MCP** | `@tool` + `streamable_http_client` chamando um servidor MCP externo |
| **Ciclo de vida do Agente Hospedado** | Scaffold → Configurar → Testar localmente → Implantar → Verificar na nuvem |
| **`context_mode="last_agent"`** | Cada executor vê apenas a saída do seu antecessor direto |
| **Fluxo de trabalho Foundry Toolkit** | Assistente Scaffold, Inspetor de Agentes, Visualizador do Fluxo de Trabalho, implantação com um clique |

---

## O que você completou

<details open>
<summary><strong>🅰️ Caminho A - Assinatura Foundry</strong></summary>

- [x] Verificado o setup do Lab 01: projeto, modelo e RBAC ainda ativos
- [x] Scaffolded o projeto multi-agente usando o template Workflows
- [x] Escreveu quatro conjuntos de instruções para agentes (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integrado a ferramenta Microsoft Learn MCP com `streamable_http_client`
- [x] Conectado o grafo do fluxo de trabalho com `WorkflowBuilder` (pipeline sequencial com retransmissão de conteúdo)
- [x] Testado localmente com 3 testes rápidos (Agent Inspector) - pontuação, cartões de lacunas e URLs MCP
- [x] Implantado no Foundry Agent Service (containerizado, identidade gerenciada)
- [x] Verificado no playground da nuvem - consistência estrutural com resultados locais

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local</strong></summary>

- [x] Verificado setup do Lab 01: Foundry Local funcionando com modelo local
- [x] Scaffolded projeto multi-agente com template Workflows
- [x] Escreveu quatro conjuntos de instruções para agentes e conectou o grafo do fluxo de trabalho
- [x] Integrado a ferramenta Microsoft Learn MCP
- [x] Testado localmente com 3 testes rápidos
- [x] Validado comportamento multi-agente sem necessidade de recursos na nuvem

</details>

---

## Próximos passos

### Continue aprendendo

| Recurso | Descrição |
|----------|-------------|
| **[Referência do Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentação da API para `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catálogo de ferramentas MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Conecte agentes a outros servidores MCP (Bing, GitHub, customizados) |
| **[Adicionar conhecimento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Fundamente agentes com documentos, stores vetoriais ou busca Bing |
| **[Avaliações Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Meça a qualidade do agente em escala com avaliadores automatizados |
| **[Documentação Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referência completa da plataforma |
| **[Foundry Toolkit - Novidades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas de lançamento da extensão e changelog |

### Ideias para ampliar este fluxo de trabalho

- **Adicionar um 5º agente** - Um coach de entrevistas que gera possíveis perguntas com base no relatório de lacunas
- **Adicionar uma ferramenta de base Bing** - Permitir que o agente JD procure vagas similares para enriquecer os requisitos
- **Conectar a um banco de currículos** - Buscar perfis de candidatos em um banco de dados via um `@tool` customizado
- **Testar modelos diferentes** - Comparar qualidade e latência das saídas entre `gpt-4.1` e `gpt-4.1-mini`
- **Avaliar com Foundry** - Usar a funcionalidade de Avaliações para pontuar relatórios de compatibilidade contra um conjunto de dados padrão

### Para usuários do Caminho B: Atualizar para implantação na nuvem

Quando estiver pronto para implantar na nuvem:
1. Obtenha uma assinatura Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Lab 01, Módulo 01](../../lab01-single-agent/docs/01-setup.md) (criar projeto, implantar modelo, configurar RBAC)
3. Atualize seu `.env` com o endpoint do projeto Foundry e o nome da implantação do modelo
4. Continue a partir de [Módulo 06 - Implantar no Foundry](06-deploy-to-foundry.md)

---

## Limpeza de recursos (opcional)

Se desejar remover os recursos Azure criados durante este workshop:

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

> **Nota sobre custos:** Agentes hospedados geram custo apenas quando estão em execução. Se você parar ou excluir o agente, não há cobrança contínua. A implantação do modelo pode gerar uma pequena cobrança por capacidade reservada - exclua se não for mais usar.

---

**Anterior:** [08 - Resolução de Problemas](08-troubleshooting.md) · **Início:** [README Lab 02](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->