# Module 0 - Pré-requisitos

Antes de começar o Lab 02, confirme que você concluiu o seguinte. Este laboratório baseia-se diretamente no Lab 01 - não o pule.

---

## 1. Complete o Lab 01

O Lab 02 pressupõe que você já:

- [x] Concluiu todos os 8 módulos do [Lab 01 - Agente Único](../../lab01-single-agent/README.md)
- [x] Implantou com sucesso um único agente no Foundry Agent Service
- [x] Verificou que o agente funciona tanto no Agent Inspector local quanto no Foundry Playground

Se você não concluiu o Lab 01, volte e termine agora: [Documentação do Lab 01](../../lab01-single-agent/docs/00-prerequisites.md)

---

## 2. Verifique a configuração existente

Todas as ferramentas do Lab 01 devem estar instaladas e funcionando. Execute essas verificações rápidas:

### 2.1 Azure CLI

```powershell
az account show --query "{name:name, id:id}" --output table
```

Esperado: Mostra o nome e ID da sua assinatura. Se isso falhar, execute [`az login`](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively).

### 2.2 Extensões do VS Code

1. Pressione `Ctrl+Shift+P` → digite **"Microsoft Foundry"** → confirme que vê comandos (por exemplo, `Microsoft Foundry: Create a New Hosted Agent`).
2. Pressione `Ctrl+Shift+P` → digite **"Foundry Toolkit"** → confirme que vê comandos (por exemplo, `Foundry Toolkit: Open Agent Inspector`).

### 2.3 Projeto e modelo do Foundry

1. Clique no ícone **Microsoft Foundry** na Barra de Atividades do VS Code.
2. Confirme que seu projeto está listado (por exemplo, `workshop-agents`).
3. Expanda o projeto → verifique se existe um modelo implantado (por exemplo, `gpt-4.1-mini`) com status **Succeeded**.

> **Se a implantação do seu modelo expirou:** Algumas implantações gratuitas expiram automaticamente. Reimplante a partir do [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

![Barra lateral do Foundry mostrando projeto e modelo implantado com status Succeeded](../../../../../translated_images/pt-BR/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

### 2.4 Funções RBAC

Verifique se você tem o papel **Azure AI User** no seu projeto Foundry:

1. [Portal Azure](https://portal.azure.com) → recurso de **projeto** do Foundry → **Controle de acesso (IAM)** → aba **[Atribuições de função](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)**.
2. Pesquise seu nome → confirme que **[Azure AI User](https://aka.ms/foundry-ext-project-role)** está listado.

---

## 3. Entenda os conceitos multi-agente (novo para o Lab 02)

O Lab 02 introduz conceitos não abordados no Lab 01. Leia-os antes de prosseguir:

### 3.1 O que é um fluxo de trabalho multi-agente?

Em vez de um agente fazer tudo, um **fluxo de trabalho multi-agente** divide o trabalho entre vários agentes especializados. Cada agente tem:

- Suas próprias **instruções** (prompt do sistema)
- Seu próprio **papel** (pelo qual é responsável)
- **Ferramentas** opcionais (funções que pode chamar)

Os agentes comunicam-se por meio de um **grafo de orquestração** que define como os dados transitam entre eles.

### 3.2 WorkflowBuilder

A classe [`WorkflowBuilder`](https://learn.microsoft.com/agent-framework/workflows/agents-in-workflows) do `agent_framework` é o componente do SDK que conecta os agentes:

```python
from agent_framework import WorkflowBuilder

workflow = (
    WorkflowBuilder(
        name="MyWorkflow",
        start_executor=agent_a,
        output_executors=[agent_d],
    )
    .add_edge(agent_a, agent_b)
    .add_edge(agent_a, agent_c)
    .add_edge(agent_b, agent_d)
    .add_edge(agent_c, agent_d)
    .build()
)
```

- **`start_executor`** - O primeiro agente que recebe a entrada do usuário
- **`output_executors`** - O(s) agente(s) cuja saída se torna a resposta final
- **`add_edge(source, target)`** - Define que o `target` recebe a saída do `source`

### 3.3 Ferramentas MCP (Model Context Protocol)

O Lab 02 usa uma **ferramenta MCP** que chama a API Microsoft Learn para buscar recursos de aprendizado. [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction) é um protocolo padronizado para conectar modelos de IA a fontes de dados e ferramentas externas.

| Termo | Definição |
|------|-----------|
| **Servidor MCP** | Um serviço que expõe ferramentas/recursos via [protocolo MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol) |
| **Cliente MCP** | Seu código de agente que conecta a um servidor MCP e chama suas ferramentas |
| **[Streamable HTTP](https://learn.microsoft.com/agent-framework/agents/tools/hosted-mcp-tools)** | Método de transporte usado para comunicação com o servidor MCP |

### 3.4 Como o Lab 02 difere do Lab 01

| Aspecto | Lab 01 (Agente Único) | Lab 02 (Multi-Agente) |
|--------|----------------------|---------------------|
| Agentes | 1 | 4 (funções especializadas) |
| Orquestração | Nenhuma | WorkflowBuilder (paralelo + sequencial) |
| Ferramentas | Função `@tool` opcional | Ferramenta MCP (chamada API externa) |
| Complexidade | Prompt simples → resposta | Currículo + JD → pontuação de adequação → roadmap |
| Fluxo de contexto | Direto | Passagem entre agentes |

---

## 4. Estrutura do repositório do workshop para o Lab 02

Garanta que você saiba onde estão os arquivos do Lab 02:

```
workshop/
└── lab02-multi-agent/
    ├── README.md                       ← Lab overview
    ├── docs/                           ← You are here
    │   ├── README.md                   ← Learning path index
    │   ├── 00-prerequisites.md         ← This file
    │   ├── 01-understand-multi-agent.md
    │   ├── ...
    │   └── 08-troubleshooting.md
    └── PersonalCareerCopilot/          ← The agent project
        ├── agent.yaml                  ← Agent definition
        ├── main.py                     ← 4-agent workflow code
        ├── Dockerfile                  ← Container configuration
        └── requirements.txt            ← Python dependencies
```

---

### Verificação

- [ ] Lab 01 está totalmente concluído (todos os 8 módulos, agente implantado e verificado)
- [ ] `az account show` retorna sua assinatura
- [ ] Extensões Microsoft Foundry e Foundry Toolkit estão instaladas e funcionando
- [ ] Projeto Foundry tem um modelo implantado (ex: `gpt-4.1-mini`)
- [ ] Você tem o papel **Azure AI User** no projeto
- [ ] Você leu a seção de conceitos multi-agente acima e entende o WorkflowBuilder, MCP e orquestração de agentes

---

**Próximo:** [01 - Entenda a Arquitetura Multi-Agente →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->