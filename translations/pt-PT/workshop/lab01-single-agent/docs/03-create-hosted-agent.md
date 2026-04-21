# Módulo 3 - Criar um Novo Agente Hospedado (Auto-Escaffolded pela Extensão Foundry)

Neste módulo, utiliza a extensão Microsoft Foundry para **criar um novo projeto de [agente hospedado](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)**. A extensão gera toda a estrutura do projeto para si - incluindo `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, um ficheiro `.env` e uma configuração de depuração do VS Code. Após o scaffold, personaliza estes ficheiros com as instruções, ferramentas e configuração do seu agente.

> **Conceito-chave:** A pasta `agent/` neste laboratório é um exemplo do que a extensão Foundry gera quando executa este comando de scaffold. Não escreve estes ficheiros do zero - a extensão cria-os e depois você os modifica.

### Fluxo do assistente de scaffold

```mermaid
flowchart LR
    A["Paleta de Comandos:
    Criar Agente Hospedado"] --> B["Escolher Modelo:
    Agente Único"]
    B --> C["Escolher Linguagem:
    Python"]
    C --> D["Selecionar Modelo:
    gpt-4.1-mini"]
    D --> E["Escolher Pasta +
    Nome do Agente"]
    E --> F["Projeto Estruturado:
    agent.yaml, main.py,
    Dockerfile, .env"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#7B68EE,color:#fff
    style E fill:#7B68EE,color:#fff
    style F fill:#27AE60,color:#fff
```
---

## Passo 1: Abrir o assistente Criar Agente Hospedado

1. Prima `Ctrl+Shift+P` para abrir a **Paleta de Comandos**.
2. Escreva: **Microsoft Foundry: Create a New Hosted Agent** e selecione-o.
3. O assistente de criação de agente hospedado abre.

> **Caminho alternativo:** Também pode aceder a este assistente pelo separador lateral do Microsoft Foundry → clique no ícone **+** junto a **Agents** ou clique com o botão direito e selecione **Create New Hosted Agent**.

---

## Passo 2: Escolher o seu modelo

O assistente pede-lhe para selecionar um modelo. Vai ver opções como:

| Modelo | Descrição | Quando usar |
|--------|------------|-------------|
| **Agente Único** | Um agente com o seu próprio modelo, instruções e ferramentas opcionais | Este workshop (Laboratório 01) |
| **Fluxo Multi-Agente** | Múltiplos agentes que colaboram em sequência | Laboratório 02 |

1. Selecione **Agente Único**.
2. Clique em **Seguinte** (ou a seleção avança automaticamente).

---

## Passo 3: Escolher a linguagem de programação

1. Selecione **Python** (recomendado para este workshop).
2. Clique em **Seguinte**.

> **C# também é suportado** se preferir .NET. A estrutura do scaffold é semelhante (usa `Program.cs` em vez de `main.py`).

---

## Passo 4: Selecionar o seu modelo

1. O assistente mostra os modelos implantados no seu projeto Foundry (do Módulo 2).
2. Selecione o modelo que implantou - por exemplo, **gpt-4.1-mini**.
3. Clique em **Seguinte**.

> Se não vir nenhum modelo, volte ao [Módulo 2](02-create-foundry-project.md) e implante um primeiro.

---

## Passo 5: Escolher a localização da pasta e o nome do agente

1. Abre-se uma caixa de diálogo para escolher uma **pasta destino** onde o projeto será criado. Para este workshop:
   - Se estiver a começar do zero: escolha qualquer pasta (ex: `C:\Projects\my-agent`)
   - Se estiver a trabalhar dentro do repositório do workshop: crie uma nova subpasta em `workshop/lab01-single-agent/agent/`
2. Introduza um **nome** para o agente hospedado (ex: `executive-summary-agent` ou `my-first-agent`).
3. Clique em **Criar** (ou prima Enter).

---

## Passo 6: Aguardar a conclusão do scaffold

1. O VS Code abre uma **nova janela** com o projeto scaffolded.
2. Aguarde alguns segundos até o projeto carregar completamente.
3. Deve ver os seguintes ficheiros no painel do Explorador (`Ctrl+Shift+E`):

```
📂 my-first-agent/
├── .env                ← Environment variables (auto-generated with placeholders)
├── .vscode/
│   └── launch.json     ← Debug configuration (F5 to run + Agent Inspector)
├── agent.yaml          ← Agent definition (kind: hosted)
├── Dockerfile          ← Container configuration for deployment
├── main.py             ← Agent entry point (your main code file)
└── requirements.txt    ← Python dependencies
```

> **Esta é a mesma estrutura da pasta `agent/`** neste laboratório. A extensão Foundry gera estes ficheiros automaticamente - não precisa criá-los manualmente.

> **Nota do workshop:** Neste repositório do workshop, a pasta `.vscode/` está na **raiz do espaço de trabalho** (não dentro de cada projeto). Contém um `launch.json` e `tasks.json` partilhados com duas configurações de depuração - **"Lab01 - Single Agent"** e **"Lab02 - Multi-Agent"** - cada uma apontando para o `cwd` correto do laboratório. Quando premir F5, selecione a configuração correspondente ao laboratório em que está a trabalhar no menu dropdown.

---

## Passo 7: Compreender cada ficheiro gerado

Tire um momento para inspecionar cada ficheiro criado pelo assistente. Compreendê-los é importante para o Módulo 4 (personalização).

### 7.1 `agent.yaml` - Definição do agente

Abra o `agent.yaml`. Tem este aspeto:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/microsoft/AgentSchema/refs/heads/main/schemas/v1.0/ContainerAgent.yaml

kind: hosted
name: my-first-agent
description: >
  A hosted agent deployed to Microsoft Foundry Agent Service.
metadata:
  authors:
    - Microsoft
  tags:
    - Azure AI AgentServer
    - Microsoft Agent Framework
    - Hosted Agent
protocols:
  - protocol: responses
    version: v1
environment_variables:
  - name: AZURE_AI_PROJECT_ENDPOINT
    value: ${PROJECT_ENDPOINT}
  - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
    value: ${MODEL_DEPLOYMENT_NAME}
dockerfile_path: Dockerfile
resources:
  cpu: '0.25'
  memory: 0.5Gi
```

**Campos-chave:**

| Campo | Propósito |
|-------|-----------|
| `kind: hosted` | Declara que este é um agente hospedado (baseado em container, implantado no [Foundry Agent Service](https://learn.microsoft.com/azure/foundry/agents/overview)) |
| `protocols: responses v1` | O agente expõe o endpoint HTTP `/responses` compatível com OpenAI |
| `environment_variables` | Mapeia valores do `.env` para variáveis de ambiente do container na implantação |
| `dockerfile_path` | Aponta para o Dockerfile usado para construir a imagem do container |
| `resources` | Alocação de CPU e memória para o container (0.25 CPU, 0.5Gi de memória) |

### 7.2 `main.py` - Ponto de entrada do agente

Abra o `main.py`. Este é o ficheiro principal em Python onde a lógica do seu agente reside. O scaffold inclui:

```python
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.identity.aio import DefaultAzureCredential
```

**Importações-chave:**

| Importação | Propósito |
|------------|-----------|
| `AzureAIAgentClient` | Liga-se ao seu projeto Foundry e cria agentes via `.as_agent()` |
| [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) | Gere a autenticação (Azure CLI, início de sessão do VS Code, identidade gerida ou principal de serviço) |
| `from_agent_framework` | Envolve o agente como um servidor HTTP expondo o endpoint `/responses` |

O fluxo principal é:
1. Criar uma credencial → criar um cliente → chamar `.as_agent()` para obter um agente (gestor de contexto assíncrono) → envolver como servidor → executar

### 7.3 `Dockerfile` - Imagem do container

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY ./ .

RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    else \
        echo "No requirements.txt found" >&2; exit 1; \
    fi

EXPOSE 8088

CMD ["python", "main.py"]
```

**Detalhes-chave:**
- Usa `python:3.14-slim` como imagem base.
- Copia todos os ficheiros do projeto para `/app`.
- Atualiza o `pip`, instala dependências do `requirements.txt` e falha rapidamente se esse ficheiro estiver em falta.
- **Expõe a porta 8088** - esta é a porta obrigatória para agentes hospedados. Não a altere.
- Inicia o agente com `python main.py`.

### 7.4 `requirements.txt` - Dependências

```
agent-framework-azure-ai==1.0.0rc3
agent-framework-core==1.0.0rc3
azure-ai-agentserver-agentframework==1.0.0b16
azure-ai-agentserver-core==1.0.0b16
debugpy
agent-dev-cli
```

| Pacote | Propósito |
|--------|-----------|
| `agent-framework-azure-ai` | Integração Azure AI para o Microsoft Agent Framework |
| `agent-framework-core` | Runtime central para construir agentes (inclui `python-dotenv`) |
| `azure-ai-agentserver-agentframework` | Runtime de servidor para agentes hospedados no Foundry Agent Service |
| `azure-ai-agentserver-core` | Abstrações centrais do servidor de agentes |
| `debugpy` | Suporte à depuração Python (permite depuração F5 no VS Code) |
| `agent-dev-cli` | CLI para desenvolvimento local e teste de agentes (usado pela configuração de depuração/execução) |

---

## Compreender o protocolo do agente

Agentes hospedados comunicam via o protocolo **OpenAI Responses API**. Quando a correr (localmente ou na cloud), o agente expõe um único endpoint HTTP:

```
POST http://localhost:8088/responses
Content-Type: application/json

{
  "input": "Your prompt here",
  "stream": false
}
```

O Foundry Agent Service chama este endpoint para enviar prompts do utilizador e receber respostas do agente. Este é o mesmo protocolo usado pela API OpenAI, pelo que o seu agente é compatível com qualquer cliente que suporte o formato OpenAI Responses.

---

### Ponto de verificação

- [ ] O assistente de scaffold concluiu com sucesso e uma **nova janela VS Code** abriu
- [ ] Pode ver os 5 ficheiros: `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`
- [ ] O ficheiro `.vscode/launch.json` existe (permite depuração F5 - neste workshop está na raiz do espaço de trabalho com configurações específicas para cada laboratório)
- [ ] Leu cada ficheiro e compreendeu o seu propósito
- [ ] Compreende que a porta `8088` é obrigatória e que o endpoint `/responses` é o protocolo

---

**Anterior:** [02 - Criar Projeto Foundry](02-create-foundry-project.md) · **Seguinte:** [04 - Configurar & Codificar →](04-configure-and-code.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informação crítica, é recomendada a tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->