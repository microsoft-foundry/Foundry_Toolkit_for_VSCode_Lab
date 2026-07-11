# Laboratório 02 - Fluxo de Trabalho Multi-Agente: Avaliador de Compatibilidade Currículo → Emprego

## Caminho de Aprendizagem Completo

Esta documentação guia-o na construção, teste e implementação de um **fluxo de trabalho multi-agente** que avalia a compatibilidade do currículo com o emprego usando quatro agentes especializados orquestrados via **WorkflowBuilder**.

> **Pré-requisito:** Complete o [Laboratório 01 - Agente Único](../../lab01-single-agent/README.md) antes de iniciar o Laboratório 02.

---

## Módulos

| # | Módulo | O que vai fazer |
|---|--------|-----------------|
| 0 | [Introdução](00-prerequisites.md) | O que vai construir, verificação do Laboratório 01, comparação Laboratório 02 vs Laboratório 01 |
| 1 | [Compreender Arquitetura Multi-Agente](01-understand-multi-agent.md) | Aprender WorkflowBuilder, papéis dos agentes, gráfico de orquestração |
| 2 | [Estruturar o Projeto Multi-Agente](02-scaffold-multi-agent.md) | Usar o assistente da extensão Foundry para estruturar o projeto base |
| 3 | [Configurar Agentes & Ambiente](03-configure-agents.md) | Escrever instruções para 4 agentes, configurar a ferramenta MCP, definir variáveis de ambiente |
| 4 | [Padrões de Orquestração](04-orchestration-patterns.md) | Cadeia sequencial, retransmissão de conteúdo e semântica OR do WorkflowBuilder |
| 5 | [Testar Localmente](05-test-locally.md) | Depuração F5 com Agent Inspector, executar testes básicos com currículo + descrição do trabalho |
| 6 | [Implementar no Foundry](06-deploy-to-foundry.md) | Construir container, enviar para ACR, registar agente hospedado |
| 7 | [Verificar no Playground](07-verify-in-playground.md) | Testar agente implementado nos ambientes VS Code e Foundry Portal playground |
| 8 | [Resolução de Problemas](08-troubleshooting.md) | Corrigir problemas comuns multi-agente (erros MCP, saída truncada, versões de pacotes) |
| 9 | [Resumo & Próximos Passos](09-summary.md) | O que construiu, conceitos chave aprendidos, limpeza, e para onde ir a seguir |

---

**Voltar para:** [Laboratório 02 README](../README.md) · [Página Principal do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->