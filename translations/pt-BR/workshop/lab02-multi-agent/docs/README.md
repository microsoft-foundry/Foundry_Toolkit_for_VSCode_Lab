# Lab 02 - Fluxo de Trabalho Multiagente: Avaliador de Compatibilidade Currículo → Vaga

## Caminho Completo de Aprendizagem

Esta documentação guia você na construção, teste e implantação de um **fluxo de trabalho multiagente** que avalia a compatibilidade entre currículo e vaga usando quatro agentes especializados orquestrados via **WorkflowBuilder**.

> **Pré-requisito:** Complete o [Lab 01 - Agente Único](../../lab01-single-agent/README.md) antes de iniciar o Lab 02.

---

## Módulos

| # | Módulo | O que você fará |
|---|--------|-----------------|
| 0 | [Introdução](00-prerequisites.md) | O que você construirá, verificação do Lab 01, comparação Lab 02 vs Lab 01 |
| 1 | [Entendendo a Arquitetura Multiagente](01-understand-multi-agent.md) | Aprenda WorkflowBuilder, papéis dos agentes, grafo de orquestração |
| 2 | [Estruturando o Projeto Multiagente](02-scaffold-multi-agent.md) | Use o assistente da extensão Foundry para estruturar o projeto base |
| 3 | [Configurar Agentes e Ambiente](03-configure-agents.md) | Escreva instruções para 4 agentes, configure ferramenta MCP, defina vars de ambiente |
| 4 | [Padrões de Orquestração](04-orchestration-patterns.md) | Cadeia sequencial, retransmissão de conteúdo e semântica OR do WorkflowBuilder |
| 5 | [Testar Localmente](05-test-locally.md) | Depuração F5 com Agent Inspector, execute testes básicos com currículo + JD |
| 6 | [Implantar no Foundry](06-deploy-to-foundry.md) | Construa container, envie para ACR, registre agente hospedado |
| 7 | [Verificar no Playground](07-verify-in-playground.md) | Teste agente implantado no VS Code e playground do Portal Foundry |
| 8 | [Resolução de Problemas](08-troubleshooting.md) | Solucione problemas comuns multiagente (erros MCP, saída truncada, versões de pacotes) |
| 9 | [Resumo e Próximos Passos](09-summary.md) | O que você construiu, conceitos-chave aprendidos, limpeza e próximos passos |

---

**Voltar para:** [Lab 02 README](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->