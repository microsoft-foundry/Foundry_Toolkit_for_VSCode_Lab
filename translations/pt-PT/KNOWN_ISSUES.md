# Problemas Conhecidos

Este documento regista problemas conhecidos com o estado atual do repositório.

> Última atualização: 2026-04-15. Testado com Python 3.13 / Windows em `.venv_ga_test`.

---

## Versões Fixas Atuais dos Pacotes (todos os três agentes)

| Pacote | Versão Atual |
|---------|---------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(corrigido — ver KI-003)* |

---

## KI-001 — Bloqueio da Atualização GA 1.0.0: `agent-framework-azure-ai` Removido

**Estado:** Aberto | **Gravidade:** 🔴 Alta | **Tipo:** Quebra

### Descrição

O pacote `agent-framework-azure-ai` (fixado em `1.0.0rc3`) foi **removido/descontinuado**
na versão GA (1.0.0, lançada a 2026-04-02). Foi substituído por:

- `agent-framework-foundry==1.0.0` — padrão de agente alojado no Foundry
- `agent-framework-openai==1.0.0` — padrão de agente suportado pela OpenAI

Os três ficheiros `main.py` importam `AzureAIAgentClient` de `agent_framework.azure`, o que gera
`ImportError` com os pacotes GA. O namespace `agent_framework.azure` ainda existe
na GA, mas agora contém apenas classes Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — não agentes Foundry.

### Erro confirmado (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Ficheiros afetados

| Ficheiro | Linha |
|------|-------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Incompatível com GA `agent-framework-core`

**Estado:** Aberto | **Gravidade:** 🔴 Alta | **Tipo:** Quebra (bloqueado na fonte)

### Descrição

`azure-ai-agentserver-agentframework==1.0.0b17` (mais recente) fixa rigidamente
`agent-framework-core<=1.0.0rc3`. Instalá-lo juntamente com `agent-framework-core==1.0.0` (GA)
obriga o pip a **rebaixar** `agent-framework-core` de volta para `rc3`, o que depois quebra
`agent-framework-foundry==1.0.0` e `agent-framework-openai==1.0.0`.

A chamada `from azure.ai.agentserver.agentframework import from_agent_framework` usada por todos
os agentes para ligar o servidor HTTP está assim também bloqueada.

### Conflito de dependências confirmado (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Ficheiros afetados

Os três ficheiros `main.py` — tanto a importação ao topo como a importação dentro da função `main()`.

---

## KI-003 — Flag `agent-dev-cli --pre` Já Não É Necessária

**Estado:** ✅ Corrigido (não quebra) | **Gravidade:** 🟢 Baixa

### Descrição

Todos os ficheiros `requirements.txt` incluíam anteriormente `agent-dev-cli --pre` para obter a
pré-versão da CLI. Desde que a GA 1.0.0 foi lançada a 2026-04-02, a versão estável do
`agent-dev-cli` está agora disponível sem a flag `--pre`.

**Correção aplicada:** A flag `--pre` foi removida de todos os três ficheiros `requirements.txt`.

---

## KI-004 — Dockerfiles Usam `python:3.14-slim` (Imagem Base Pré-lançamento)

**Estado:** Aberto | **Gravidade:** 🟡 Baixa

### Descrição

Todos os `Dockerfile`s usam `FROM python:3.14-slim` que aponta para uma build Python pré-lançamento.
Para implantações em produção, deveria ser fixado numa versão estável (ex., `python:3.12-slim`).

### Ficheiros afetados

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referências

- [agent-framework-core no PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry no PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a exatidão, por favor tenha em atenção que traduções automáticas podem conter erros ou imprecisões. O documento original, no seu idioma nativo, deve ser considerado a fonte autoritativa. Para informações críticas, recomenda-se tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->