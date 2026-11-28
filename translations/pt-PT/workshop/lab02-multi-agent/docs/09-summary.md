# Módulo 9 - Resumo & Próximos Passos

⏱️ ~5 min

**Parabéns!** Construíste, testaste e (se seguiste o Caminho A) implementaste um workflow multiagente usando o Microsoft Foundry e o Foundry Toolkit para VS Code.

---

## O que construíste

O **Avaliação de Compatibilidade Currículo → Emprego** - um workflow multiagente alojado que:
- Recebe um currículo + descrição do emprego via HTTP (`POST /responses`)
- Executa quatro agentes especializados numa pipeline sequencial - cada agente transmite os dados que o seu sucessor precisa
- Devolve uma pontuação de compatibilidade (0–100 com detalhamento), uma lista de lacunas de competências e certificações, e um roteiro de aprendizagem personalizado com links reais da Microsoft Learn para cada lacuna
- Chama o servidor Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) para obter recursos oficiais de aprendizagem para cada lacuna de competência identificada
- Executa como um único agente alojado conteinerizado no Microsoft Foundry Agent Service

---

## Conceitos-chave aprendidos

| Conceito | O que praticaste |
|---------|-------------------|
| **Orquestração multiagente** | Pipeline sequencial `WorkflowBuilder` com `add_edge()` |
| **Especialização de agentes** | Quatro agentes focados superam um agente de propósito geral |
| **Padrão Content Router** | ResumeParser funciona também como router - preserva o texto do JD numa secção `[JOB DESCRIPTION PASS-THROUGH]` para que agentes a jusante possam aceder (necessário porque `context_mode="last_agent"` significa que só `start_executor` vê a mensagem bruta do utilizador) |
| **Padrão Content Relay** | Agente JD encaminha `[PARSED RESUME PASS-THROUGH]` para frente para que MatchingAgent tenha ambos os perfis; evita o gatilho duplo semântico-OU que os grafos fan-in causam |
| **Integração da ferramenta MCP** | Chamada externamente a `@tool` + `streamable_http_client` no servidor MCP |
| **Ciclo de vida do Agente Alojado** | Scaffold → Configuração → Teste local → Implantação → Verificação na cloud |
| **`context_mode="last_agent"`** | Cada executor vê apenas a saída do seu predecessor direto |
| **Workflow Foundry Toolkit** | Assistente Scaffold, Inspetor de Agentes, Visualizador de Workflow, implantação com um clique |

---

## O que concluíste

<details open>
<summary><strong>🅰️ Caminho A - Subscrição Foundry</strong></summary>

- [x] Verificado o setup do Lab 01: projeto, modelo e RBAC ainda ativos
- [x] Criado scaffolding de um projeto multiagente usando o template Workflows
- [x] Escrevi quatro conjuntos de instruções para agentes (ResumeParser, Agente JD, MatchingAgent, GapAnalyzer)
- [x] Integrei a ferramenta Microsoft Learn MCP com `streamable_http_client`
- [x] Liguei o gráfico do workflow com `WorkflowBuilder` (pipeline sequencial com content relay)
- [x] Testado localmente com 2 testes rápidos (Agent Inspector) - pontuação de compatibilidade, cartões de lacunas e URLs MCP
- [x] Implementado no Foundry Agent Service (conteinerizado, identidade gerida)
- [x] Verificado no playground cloud - consistência estrutural com resultados locais

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local</strong></summary>

- [x] Verificado setup do Lab 01: Foundry Local a funcionar com um modelo local
- [x] Criado scaffolding de um projeto multiagente usando o template Workflows
- [x] Escrevi quatro conjuntos de instruções para agentes e liguei o gráfico do workflow
- [x] Integrei a ferramenta Microsoft Learn MCP
- [x] Testado localmente com 2 testes rápidos
- [x] Validado comportamento multiagente sem necessidade de recursos na cloud

</details>

---

## Próximos passos

### Continua a aprender

| Recurso | Descrição |
|----------|-------------|
| **[Referência do Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentação API para `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catálogo da ferramenta MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Liga agentes a outros servidores MCP (Bing, GitHub, personalizados) |
| **[Adicionar conhecimento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Baseia agentes com documentos, lojas vetoriais ou pesquisa Bing |
| **[Avaliações Foundry](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mede a qualidade do agente em escala com avaliadores automatizados |
| **[Documentação Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referência completa da plataforma |
| **[Foundry Toolkit - Novidades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas de lançamento da extensão e changelog |

### Ideias para expandir este workflow

- **Adicionar um 5º agente** - Um treinador de entrevistas que gera prováveis perguntas com base no relatório de lacunas
- **Adicionar uma ferramenta de grounding Bing** - Permite que o Agente JD pesquise por ofertas de emprego semelhantes para enriquecer os requisitos
- **Ligar a uma base de dados de currículos** - Buscar perfis de candidatos de uma base de dados via um `@tool` personalizado
- **Experimentar modelos diferentes** - Comparar qualidade e latência de saída entre `gpt-4.1` vs. `gpt-4.1-mini`
- **Avaliar com Foundry** - Usar a funcionalidade Avaliações para pontuar relatórios de compatibilidade contra um conjunto de dados de referência

### Para utilizadores do Caminho B: Atualizar para implementação na cloud

Quando estiveres pronto para implementar na cloud:
1. Obtém uma subscrição Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Completa o [Lab 01, Módulo 01](../../lab01-single-agent/docs/01-setup.md) (criação de projeto, implementação de modelo, atribuição de RBAC)
3. Atualiza o teu `.env` com o endpoint do projeto Foundry e o nome da implementação do modelo
4. Continua a partir do [Módulo 06 - Implementar no Foundry](06-deploy-to-foundry.md)

---

## Limpeza de recursos (opcional)

Se quiseres remover os recursos do Azure criados durante este workshop:

### Opção 1: Eliminar o grupo de recursos (remove tudo)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opção 2: Eliminar apenas o agente alojado

1. Abre [ai.azure.com](https://ai.azure.com) → o teu projeto → **Build** → **Agents**.
2. Encontra **PersonalCareerCopilot** → clica em **Delete**.

### Opção 3: Eliminar a implementação do modelo

1. Na barra lateral do Foundry, expande o teu projeto → **Models**.
2. Clica com o botão direito na implementação do modelo → **Delete**.

> **Nota sobre custos:** Agentes alojados só geram custo quando estão a funcionar. Se parares ou eliminares o agente, não existe custo contínuo. A implementação do modelo pode gerar um custo pequeno por capacidade reservada - elimina-a se já não precisares.

---

**Anterior:** [08 - Resolução de Problemas](08-troubleshooting.md) · **Início:** [Lab 02 README](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->