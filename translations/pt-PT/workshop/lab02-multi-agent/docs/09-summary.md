# Módulo 9 - Resumo e Próximos Passos

⏱️ ~5 min

**Parabéns!** Construiu, testou e (se estiver no Caminho A) implantou um fluxo de trabalho multi-agente usando Microsoft Foundry e o Foundry Toolkit para VS Code.

---

## O que construiu

O **Avaliação de Currículo → Ajuste ao Emprego** - um fluxo de trabalho hospedado multi-agente que:
- Recebe um currículo + descrição do trabalho via HTTP (`POST /responses`)
- Executa quatro agentes especializados numa pipeline sequencial - cada agente transmite os dados que o seu sucessor necessita
- Retorna uma pontuação de ajuste (0–100 com um detalhamento), uma lista de lacunas de competências e certificações, e um roteiro personalizado de aprendizagem com links reais do Microsoft Learn para cada lacuna
- Chama o servidor Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) para obter recursos oficiais de aprendizagem para cada lacuna identificada
- Executa como um único agente hospedado em contentor no Microsoft Foundry Agent Service

---

## Conceitos chave aprendidos

| Conceito | O que praticou |
|---------|---------------|
| **Orquestração multi-agente** | Pipeline sequencial com `WorkflowBuilder` e `add_edge()` |
| **Especialização de agentes** | Quatro agentes focados superam um agente de propósito geral |
| **Padrão Content Router** | ResumeParser funciona também como router - preserva o texto da JD numa secção `[JOB DESCRIPTION PASS-THROUGH]` para que os agentes seguintes possam aceder a ele (necessário porque `context_mode="last_agent"` significa que só o `start_executor` vê a mensagem bruta do utilizador) |
| **Padrão Content Relay** | Agente JD retransmite `[PARSED RESUME PASS-THROUGH]` para frente para que MatchingAgent receba ambos os perfis; evita o duplo disparo semântico OR que os grafos fan-in causam |
| **Integração com ferramenta MCP** | `@tool` + `streamable_http_client` a chamar um servidor MCP externo |
| **Ciclo de vida do Agente Hospedado** | Scaffold → Configurar → Testar localmente → Implantar → Verificar na cloud |
| **`context_mode="last_agent"`** | Cada executante vê apenas a saída do seu predecessor direto |
| **Fluxo de trabalho Foundry Toolkit** | Assistente Scaffold, Inspector de Agentes, Visualizador de Fluxo de Trabalho, implantação com um clique |

---

## O que concluiu

<details open>
<summary><strong>🅰️ Caminho A - Subscrição Foundry</strong></summary>

- [x] Verificou a configuração do Lab 01: projeto, modelo e RBAC ainda ativos
- [x] Scaffoldou um projeto multi-agente usando o template Workflows
- [x] Escreveu quatro conjuntos de instruções para agentes (ResumeParser, Agente JD, MatchingAgent, GapAnalyzer)
- [x] Integração da ferramenta Microsoft Learn MCP com `streamable_http_client`
- [x] Ligou o grafo do fluxo de trabalho com `WorkflowBuilder` (pipeline sequencial com retransmissão de conteúdo)
- [x] Testou localmente com 3 testes simples (Agent Inspector) - pontuação de ajuste, cartões de lacunas, e URLs MCP
- [x] Implantado no Foundry Agent Service (contentorizado, identidade gerida)
- [x] Verificado no playground cloud - consistência estrutural com resultados locais

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local</strong></summary>

- [x] Verificou a configuração do Lab 01: Foundry Local a correr com um modelo local
- [x] Scaffoldou um projeto multi-agente usando o template Workflows
- [x] Escreveu quatro conjuntos de instruções para agentes e ligou o grafo do fluxo de trabalho
- [x] Integração da ferramenta Microsoft Learn MCP
- [x] Testou localmente com 3 testes simples
- [x] Validou o comportamento multi-agente sem necessidade de recursos cloud

</details>

---

## Próximos passos

### Continue a aprender

| Recurso | Descrição |
|--------|-----------|
| **[Referência do SDK Agent Framework](https://learn.microsoft.com/agent-framework/)** | Documentação API para `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catálogo da ferramenta MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Conecte agentes a outros servidores MCP (Bing, GitHub, personalizados) |
| **[Adicionar conhecimento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Fundamente agentes com documentos, armazenamentos vetoriais, ou pesquisa Bing |
| **[Avaliações Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Meça a qualidade dos agentes em escala com avaliadores automáticos |
| **[Documentação Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referência completa da plataforma |
| **[Foundry Toolkit - Novidades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas da versão da extensão e registo de alterações |

### Ideias para expandir este fluxo de trabalho

- **Adicionar um 5º agente** - Um treinador de entrevistas que produz prováveis perguntas de entrevista com base no relatório de lacunas
- **Adicionar uma ferramenta de fundamentação Bing** - Permitir que o Agente JD pesquise publicações de emprego similares para enriquecer os requisitos
- **Ligar a uma base de dados de currículos** - Puxar perfis de candidatos de uma base de dados via um `@tool` personalizado
- **Experimentar modelos diferentes** - Comparar qualidade e latência da saída entre `gpt-4.1` e `gpt-4.1-mini`
- **Avaliar com Foundry** - Usar a funcionalidade de Avaliações para pontuar relatórios de ajuste contra um conjunto de dados ouro

### Para utilizadores do Caminho B: Atualize para implantação na cloud

Quando estiver pronto para implantar na cloud:
1. Obtenha uma subscrição Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Lab 01, Módulo 01](../../lab01-single-agent/docs/01-setup.md) (criar projeto, implantar modelo, atribuir RBAC)
3. Atualize o seu `.env` com o endpoint do projeto Foundry e o nome de implantação do modelo
4. Continue a partir de [Módulo 06 - Implantar no Foundry](06-deploy-to-foundry.md)

---

## Limpar recursos (opcional)

Se desejar remover os recursos Azure criados durante este workshop:

### Opção 1: Apagar o grupo de recursos (remove tudo)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opção 2: Apagar apenas o agente hospedado

1. Abra [ai.azure.com](https://ai.azure.com) → o seu projeto → **Build** → **Agents**.
2. Encontre **PersonalCareerCopilot** → clique em **Delete**.

### Opção 3: Apagar a implantação do modelo

1. Na barra lateral do Foundry, expanda o seu projeto → **Models**.
2. Clique com o botão direito na implantação do modelo → **Delete**.

> **Nota de custo:** Agentes hospedados só geram custos quando estão a correr. Se parar ou apagar o agente, não há cobrança contínua. A implantação do modelo pode gerar uma pequena cobrança por capacidade reservada - apague-a se tiver terminado.

---

**Anterior:** [08 - Resolução de problemas](08-troubleshooting.md) · **Início:** [Lab 02 README](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->