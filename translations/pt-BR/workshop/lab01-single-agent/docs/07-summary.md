# Módulo 7 - Resumo e Próximos Passos

⏱️ ~5 min

**Parabéns!** Você construiu, testou e (se estiver no Caminho A) implantou um agente de IA hospedado usando o Microsoft Foundry e o Foundry Toolkit para VS Code.

---

## O que você construiu

Um agente **"Explique Como se Eu Fosse um Executivo"** que:
- Recebe relatórios técnicos de incidentes ou atualizações operacionais via HTTP (`POST /responses`)
- Traduz eles em resumos executivos em linguagem simples
- Segue um formato estruturado de saída (O que aconteceu / Impacto nos negócios / Próximo passo)
- Recusa solicitações fora do tópico e tentativas de injeção de prompt
- Executa como um agente hospedado containerizado no Microsoft Foundry Agent Service

---

## Conceitos principais aprendidos

| Conceito | O que você praticou |
|---------|-------------------|
| **Arquitetura do Agent Framework** | Pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Ciclo de vida do Agente Hospedado** | Scaffold → Configurar → Testar localmente → Implantar → Verificar na nuvem |
| **Engenharia de prompt do sistema** | Papel, público, formato de saída, regras, restrições de segurança e exemplos |
| **Diferenças local vs. hospedado** | Identidade (credencial pessoal vs. identidade gerenciada), endpoint, caminho de rede |
| **Limites de segurança** | Defesa contra injeção de prompt, cumprimento de papel, manejo elegante de casos extremos |
| **Fluxo de trabalho do Foundry Toolkit** | Criação de projeto, implantação de modelo, scaffold de agente, Agent Inspector, implantação com um clique |

---

## O que você completou

### Caminho A (assinatura Foundry)

- [x] Configurou o Foundry Toolkit e criou um projeto Foundry com um modelo implantado
- [x] Scaffoldou um agente hospedado com estrutura de projeto gerada automaticamente
- [x] Escreveu instruções estruturadas para o agente com regras de segurança
- [x] Testou localmente com 3 cenários funcionais (Agent Inspector)
- [x] Implantou no Foundry Agent Service (containerizado)
- [x] Verificou no playground da nuvem com 4 testes de casos extremos/segurança

### Caminho B (Foundry Local)

- [x] Configurou o Foundry Toolkit com um endpoint de modelo local
- [x] Scaffoldou um projeto de agente hospedado
- [x] Escreveu instruções estruturadas para o agente com regras de segurança
- [x] Testou localmente com 3 cenários funcionais
- [x] Validou o comportamento do agente sem precisar de recursos na nuvem

---

## Próximos passos

### Continue aprendendo

| Recurso | Descrição |
|----------|-------------|
| **[Lab 02 - Orquestração Multi-Agente](../../lab02-multi-agent/docs/README.md)** | Construa um fluxo de trabalho com 4 agentes (Currículo → Avaliador de Compatibilidade para Vaga) com padrões de orquestração |
| **[Adicione ferramentas ao seu agente](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Conecte APIs, bancos de dados ou funções customizadas via Catálogo de Ferramentas |
| **[Adicione conhecimento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Fundamente seu agente com documentos, armazenamentos vetoriais ou busca Bing |
| **[Documentação Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referência completa da plataforma |
| **[Referência do Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentação da API para o pacote `agent-framework` |
| **[Foundry Toolkit - Novidades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas de versão e changelog da extensão |

### Ideias para expandir seu agente

- **Adicione uma ferramenta de data** - Permita que o agente inclua o contexto "até hoje" nos resumos
- **Conecte a um banco de dados de incidentes** - Obtenha detalhes reais de incidentes por meio de uma função de ferramenta
- **Adicione uma ferramenta de fundamentação Bing** - Permita que o agente pesquise notícias recentes para contexto adicional
- **Experimente modelos diferentes** - Compare a qualidade da saída entre `gpt-4.1` e `gpt-4.1-mini`
- **Avalie com Foundry** - Use o recurso de Avaliações para medir a qualidade do agente em escala

### Para usuários do Caminho B: Atualize para implantação na nuvem

Quando estiver pronto para implantar na nuvem:
1. Obtenha uma assinatura Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete [Módulo 01, Configuração](01-setup.md#step-2-set-up-based-on-your-access) (crie projeto, implante modelo, atribua RBAC)
3. Atualize seu `.env` com o endpoint do projeto Foundry e o nome da implantação do modelo
4. Continue a partir de [Módulo 05 - Implantar no Foundry](05-deploy-to-foundry.md)

---

## Limpeza dos recursos (opcional)

Se você quiser remover os recursos do Azure criados durante este workshop:

### Opção 1: Excluir o grupo de recursos (remove tudo)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opção 2: Excluir apenas o agente hospedado

1. Abra [ai.azure.com](https://ai.azure.com) → seu projeto → **Build** → **Agents**.
2. Clique no seu agente → clique em **Excluir**.

### Opção 3: Excluir a implantação do modelo

1. Na barra lateral do Foundry, expanda seu projeto → **Models**.
2. Clique com o botão direito na implantação do modelo → **Excluir**.

> **Nota de custo:** Agentes hospedados só geram custo enquanto estiverem em execução. Se você parar ou excluir o agente, não haverá cobrança contínua. A implantação do modelo pode gerar uma pequena cobrança por capacidade reservada - exclua-a se não precisar mais.

---

**Anterior:** [06 - Verificar no Playground](06-verify-in-playground.md) · **Próximo:** [08 - Solução de problemas (Referência) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->