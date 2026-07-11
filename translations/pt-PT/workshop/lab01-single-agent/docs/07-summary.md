# Módulo 7 - Resumo & Próximos Passos

⏱️ ~5 min

**Parabéns!** Construiu, testou e (se seguiu o Caminho A) implementou um agente de IA alojado usando o Microsoft Foundry e o Foundry Toolkit para VS Code.

---

## O que construiu

Um agente **"Explique como se eu fosse um Executivo"** que:
- Recebe relatórios técnicos de incidentes ou atualizações operacionais via HTTP (`POST /responses`)
- Traduza-os em resumos executivos em linguagem simples
- Segue um formato de saída estruturado (O que aconteceu / Impacto no negócio / Próximo passo)
- Recusa pedidos fora do tema e tentativas de injeção de prompt
- Executa como um agente alojado em contentor no Microsoft Foundry Agent Service

---

## Conceitos chave aprendidos

| Conceito | O que praticou |
|---------|-------------------|
| **Arquitetura do Framework de Agentes** | Pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Ciclo de vida do Agente Alojado** | Scaffold → Configurar → Testar localmente → Implementar → Verificar na cloud |
| **Engenharia do prompt do sistema** | Papel, público, formato de saída, regras, restrições de segurança e exemplos |
| **Diferenças local vs. alojado** | Identidade (credencial pessoal vs. identidade gerida), endpoint, caminho de rede |
| **Limites de segurança** | Defesa contra injeção de prompt, adesão ao papel, gestão elegante de casos limite |
| **Fluxo de trabalho do Foundry Toolkit** | Criação de projeto, implementação de modelo, scaffold do agente, Agent Inspector, deploy com um clique |

---

## O que concluiu

### Caminho A (assinatura Foundry)

- [x] Configurou o Foundry Toolkit e criou um projeto Foundry com um modelo implementado
- [x] Scaffoldou um agente alojado com estrutura de projeto auto-gerada
- [x] Escreveu instruções estruturadas do agente com regras de segurança
- [x] Testou localmente com 3 cenários funcionais (Agent Inspector)
- [x] Implementou no Foundry Agent Service (em contentor)
- [x] Verificou na playground da cloud com 4 testes de casos limite/segurança

### Caminho B (Foundry Local)

- [x] Configurou o Foundry Toolkit com um endpoint de modelo local
- [x] Scaffoldou um projeto de agente alojado
- [x] Escreveu instruções estruturadas do agente com regras de segurança
- [x] Testou localmente com 3 cenários funcionais
- [x] Validou o comportamento do agente sem necessitar de recursos cloud

---

## Próximos passos

### Continue a aprender

| Recurso | Descrição |
|----------|-------------|
| **[Lab 02 - Orquestração Multi-Agente](../../lab02-multi-agent/docs/README.md)** | Construa um workflow de 4 agentes (Resume → Job Fit Evaluator) com padrões de orquestração |
| **[Adicione ferramentas ao seu agente](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Conecte APIs, bases de dados ou funções personalizadas via Catálogo de Ferramentas |
| **[Adicione conhecimento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Fundamente o seu agente com documentos, armazenamento vetorial ou pesquisa Bing |
| **[Documentação Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referência completa da plataforma |
| **[Referência SDK Agent Framework](https://learn.microsoft.com/agent-framework/)** | Documentação API para o pacote `agent-framework` |
| **[Foundry Toolkit - Novidades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas de lançamento da extensão e histórico de alterações |

### Ideias para expandir o seu agente

- **Adicione uma ferramenta de data** - Permita que o agente inclua contexto "a partir de hoje" nos resumos
- **Conecte a uma base de dados de incidentes** - Obtenha detalhes reais de incidentes via uma função de ferramenta
- **Adicione uma ferramenta de fundamentação Bing** - Permita que o agente consulte notícias recentes para contexto adicional
- **Experimente diferentes modelos** - Compare a qualidade de saída do `gpt-4.1` vs. `gpt-4.1-mini`
- **Avalie com Foundry** - Use a funcionalidade de Avaliações para medir a qualidade do agente em escala

### Para utilizadores do Caminho B: Atualize para implementação na cloud

Quando estiver pronto para implementar na cloud:
1. Obtenha uma subscrição Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Complete o [Módulo 01, Configuração](01-setup.md#step-2-set-up-based-on-your-access) (crie projeto, implemente modelo, atribua RBAC)
3. Atualize o seu `.env` com o endpoint do projeto Foundry e nome de implementação do modelo
4. Continue a partir do [Módulo 05 - Implementar no Foundry](05-deploy-to-foundry.md)

---

## Limpar recursos (opcional)

Se desejar remover os recursos Azure criados durante este workshop:

### Opção 1: Apagar o grupo de recursos (remove tudo)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opção 2: Apagar apenas o agente alojado

1. Abra [ai.azure.com](https://ai.azure.com) → seu projeto → **Construir** → **Agentes**.
2. Clique no seu agente → clique em **Apagar**.

### Opção 3: Apagar a implementação do modelo

1. No menu lateral do Foundry, expanda o seu projeto → **Modelos**.
2. Clique com o botão direito na implementação do modelo → **Apagar**.

> **Nota de custo:** Agentes alojados só geram custos enquanto funcionam. Se parar ou apagar o agente, não há cobrança contínua. A implementação do modelo pode gerar uma pequena cobrança por capacidade reservada - apague-a se não precisar mais.

---

**Anterior:** [06 - Verificar na Playground](06-verify-in-playground.md) · **Próximo:** [08 - Resolução de Problemas (Referência) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->