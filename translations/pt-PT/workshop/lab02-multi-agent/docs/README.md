# Laboratório 02 - Workflow Multi-Agente: Avaliador de Compatibilidade Currículo → Emprego

## Caminho Completo de Aprendizagem

Esta documentação orienta-o na construção, teste e implementação de um **workflow multi-agente** que avalia a compatibilidade entre currículo e emprego utilizando quatro agentes especializados orquestrados através do **WorkflowBuilder**.

> **Pré-requisito:** Complete o [Laboratório 01 - Agente Único](../../lab01-single-agent/README.md) antes de iniciar o Laboratório 02.

---

## Módulos

| # | Módulo | O que vai fazer |
|---|--------|-----------------|
| 0 | [Pré-requisitos](00-prerequisites.md) | Verificar conclusão do Laboratório 01, compreender conceitos multi-agente |
| 1 | [Entender a Arquitetura Multi-Agente](01-understand-multi-agent.md) | Aprender WorkflowBuilder, papéis dos agentes, gráfico de orquestração |
| 2 | [Estruturar o Projeto Multi-Agente](02-scaffold-multi-agent.md) | Usar a extensão Foundry para estruturar um workflow multi-agente |
| 3 | [Configurar Agentes & Ambiente](03-configure-agents.md) | Escrever instruções para 4 agentes, configurar ferramenta MCP, definir variáveis de ambiente |
| 4 | [Padrões de Orquestração](04-orchestration-patterns.md) | Explorar paralelismo fan-out, agregação sequencial e padrões alternativos |
| 5 | [Testar Localmente](05-test-locally.md) | Depurar com F5 usando o Agent Inspector, executar testes com currículo + descrição de trabalho |
| 6 | [Implementar no Foundry](06-deploy-to-foundry.md) | Construir container, enviar para ACR, registar agente hospedado |
| 7 | [Verificar no Playground](07-verify-in-playground.md) | Testar agente implementado nos playgrounds do VS Code e Foundry Portal |
| 8 | [Resolução de Problemas](08-troubleshooting.md) | Corrigir problemas comuns multi-agente (erros MCP, saída truncada, versões de pacotes) |

---

## Tempo Estimado

| Nível de experiência | Tempo |
|---------------------|-------|
| Concluiu o Laboratório 01 recentemente | 45-60 minutos |
| Alguma experiência em Azure AI | 60-90 minutos |
| Primeira vez com multi-agente | 90-120 minutos |

---

## Arquitetura numa perspetiva geral

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Voltar para:** [Leia-me do Laboratório 02](../README.md) · [Página Principal do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->