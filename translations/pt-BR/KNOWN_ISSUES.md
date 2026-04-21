# Problemas Conhecidos

Este documento rastreia problemas conhecidos com o estado atual do repositório.

> Última atualização: 2026-04-15. Testado com Python 3.13 / Windows em `.venv_ga_test`.

---

## Versões Fixadas Atuais dos Pacotes (todos os três agentes)

| Pacote | Versão Atual |
|--------|--------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(corrigido — veja KI-003)* |

---

## KI-001 — Atualização GA 1.0.0 Bloqueada: `agent-framework-azure-ai` Removido

**Status:** Aberto | **Gravidade:** 🔴 Alta | **Tipo:** Quebra

### Descrição

O pacote `agent-framework-azure-ai` (fixado na versão `1.0.0rc3`) foi **removido/obsoleto**
na versão GA (1.0.0, lançada em 2026-04-02). Ele é substituído por:

- `agent-framework-foundry==1.0.0` — padrão de agente hospedado no Foundry
- `agent-framework-openai==1.0.0` — padrão de agente suportado pela OpenAI

Todos os três arquivos `main.py` importam `AzureAIAgentClient` de `agent_framework.azure`, o que
gera `ImportError` sob os pacotes GA. O namespace `agent_framework.azure` ainda existe
na GA, mas agora contém somente classes de Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — não agentes Foundry.

### Erro confirmado (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Arquivos afetados

| Arquivo | Linha |
|---------|-------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Incompatível com GA `agent-framework-core`

**Status:** Aberto | **Gravidade:** 🔴 Alta | **Tipo:** Quebra (bloqueado por dependência externa)

### Descrição

`azure-ai-agentserver-agentframework==1.0.0b17` (mais recente) fixa rigidamente
`agent-framework-core<=1.0.0rc3`. Instalá-lo junto com `agent-framework-core==1.0.0` (GA)
força o pip a **fazer downgrade** do `agent-framework-core` para `rc3`, o que quebra
`agent-framework-foundry==1.0.0` e `agent-framework-openai==1.0.0`.

A chamada `from azure.ai.agentserver.agentframework import from_agent_framework` usada por todos
os agentes para vincular o servidor HTTP também é bloqueada.

### Conflito de dependência confirmado (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Arquivos afetados

Todos os três arquivos `main.py` — tanto a importação no topo quanto a importação dentro da função `main()`.

---

## KI-003 — Flag `--pre` do `agent-dev-cli` Não é Mais Necessária

**Status:** ✅ Corrigido (não quebra) | **Gravidade:** 🟢 Baixa

### Descrição

Todos os arquivos `requirements.txt` incluíam anteriormente `agent-dev-cli --pre` para obter a
versão pré-lançamento da CLI. Desde o lançamento GA 1.0.0 em 2026-04-02, a versão estável do
`agent-dev-cli` está disponível sem a flag `--pre`.

**Correção aplicada:** A flag `--pre` foi removida de todos os três arquivos `requirements.txt`.

---

## KI-004 — Dockerfiles Usam `python:3.14-slim` (Imagem Base de Pré-lançamento)

**Status:** Aberto | **Gravidade:** 🟡 Baixa

### Descrição

Todos os `Dockerfile`s usam `FROM python:3.14-slim` que acompanha uma build pré-lançamento do Python.
Para implantações de produção, isso deve ser fixado para uma versão estável (ex., `python:3.12-slim`).

### Arquivos afetados

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
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se a tradução profissional por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações equivocadas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->