# Lab 02 - Fluxo de Trabalho Multiagente: Avaliador de Compatibilidade Currículo → Vaga

## Caminho Completo de Aprendizado

Esta documentação guia você na construção, teste e implantação de um **fluxo de trabalho multiagente** que avalia a compatibilidade entre currículo e vaga usando quatro agentes especializados orquestrados via **WorkflowBuilder**.

> **Pré-requisito:** Complete o [Lab 01 - Agente Único](../../lab01-single-agent/README.md) antes de iniciar o Lab 02.

---

## Módulos

| # | Módulo | O que você fará |
|---|--------|-----------------|
| 0 | [Pré-requisitos](00-prerequisites.md) | Verificar conclusão do Lab 01, entender conceitos multiagente |
| 1 | [Entender Arquitetura Multiagente](01-understand-multi-agent.md) | Aprender WorkflowBuilder, papéis dos agentes, grafo de orquestração |
| 2 | [Estruturar o Projeto Multiagente](02-scaffold-multi-agent.md) | Usar a extensão Foundry para estruturar um fluxo de trabalho multiagente |
| 3 | [Configurar Agentes & Ambiente](03-configure-agents.md) | Escrever instruções para 4 agentes, configurar ferramenta MCP, definir variáveis de ambiente |
| 4 | [Padrões de Orquestração](04-orchestration-patterns.md) | Explorar paralelismo fan-out, agregação sequencial e padrões alternativos |
| 5 | [Testar Localmente](05-test-locally.md) | Depurar com F5 usando Agent Inspector, rodar testes rápidos com currículo + descrição da vaga |
| 6 | [Implantar no Foundry](06-deploy-to-foundry.md) | Construir container, enviar para ACR, registrar agente hospedado |
| 7 | [Verificar no Playground](07-verify-in-playground.md) | Testar agente implantado nos playgrounds do VS Code e Foundry Portal |
| 8 | [Solução de Problemas](08-troubleshooting.md) | Corrigir problemas comuns multiagente (erros MCP, saída truncada, versões de pacotes) |

---

## Tempo estimado

| Nível de experiência | Tempo |
|----------------------|-------|
| Completou Lab 01 recentemente | 45-60 minutos |
| Alguma experiência com Azure AI | 60-90 minutos |
| Primeira vez com multiagente | 90-120 minutos |

---

## Arquitetura em resumo

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

**Voltar para:** [Lab 02 README](../README.md) · [Página Inicial do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autoritativa. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->