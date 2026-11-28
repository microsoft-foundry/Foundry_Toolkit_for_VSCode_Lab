# Módulo 2 - Criar um Novo Agente Hospedado

⏱️ ~5 min

Neste módulo, você usa o Foundry Toolkit para **criar um projeto de agente hospedado**. O scaffolding gera toda a estrutura do projeto - `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt` e a configuração de depuração do VS Code - para que possa concentrar-se na personalização do comportamento do agente.

> **Conceito-chave:** A pasta `agent/` neste laboratório é um exemplo do que o Foundry Toolkit gera. Você não escreve estes ficheiros do zero.

### Fluxo do assistente Scaffold

```mermaid
flowchart LR
    A["Command Palette:
    Create new Hosted Agent"] --> B["Language:
    Python"]
    B --> C["Framework:
    Agent Framework"]
    C --> D["API type:
    Response API"]
    D --> E["Template:
    Basic"]
    E --> F["Workspace folder
    & agent name"]
    F --> G["Generated project"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#7B68EE,color:#fff
    style E fill:#7B68EE,color:#fff
    style F fill:#7B68EE,color:#fff
    style G fill:#27AE60,color:#fff
```

---

## Passo 1: Abra o assistente Criar Agente Hospedado

1. Pressione `Ctrl+Shift+P` para abrir a **Paleta de Comandos**.
2. Escreva: **Foundry Toolkit: Create new Hosted Agent** e selecione.

> **Alternativa: Criar via Foundry Portal**
> Se preferir o navegador, pode criar o seu projeto em [https://ai.azure.com](https://ai.azure.com). Após o projeto ser provisionado, volte ao VS Code e use a barra lateral do **Foundry Toolkit** para se ligar a ele.

> **Alternativa:** Na barra lateral do Foundry Toolkit, passe o cursor sobre **Agents** no seu projeto, clique no ícone **+**, depois selecione **Create in Code With Template**.

## Passo 2: Escolher definições

![Create Hosted Agent a partir de Exemplo - separador Detalhes do Agente mostrando filtros de Linguagem, Framework, Protocolo e Template](../../../../../translated_images/pt-PT/02-hosted-agents-sample.0aabd1638936c591.webp)

1. Na secção de navegação/opções à esquerda, selecione o seguinte:

| Menu | Seleção | Notas |
|--------|-----------|-------|
| **Language** | Python | Também suportado C# |
| **Framework** | Agent Framework | Ponto de partida simples usando Agent Framework SDK |
| **API type** | Response API | `POST /responses` - conversacional, com histórico gerido pela plataforma |
| **Template** | Basic | Ponto de partida simples usando Agent Framework SDK |

2. Após selecionar, clique em **Next**

![Create Hosted Agent - separador Criar mostrando opções de Pasta de Trabalho, Nome da Pasta e Configuração de Ambiente](../../../../../translated_images/pt-PT/02-create-hosted-agents.9f10b6a566df3053.webp)

3. Na janela seguinte, selecione o seguinte:

| Menu | Seleção | Notas |
|--------|-----------|-------|
| **Workspace folder** | Escolha uma pasta de destino | ex., `/workspace/Foundry_Toolkit_for_VSCode_Lab/` ou uma subpasta neste repositório |
| **Agent name** | Introduza um nome | ex., `executive-summary-agent` |
| **Environment Setup** | ignore a configuração por agora |  |

Clique em **create** para criar o agente. Será criada uma nova pasta com o nome do agente hospedado.

## Passo 3: Inspecionar o projeto gerado

Após o scaffolding terminar, verifique que vê estes ficheiros no Explorer (`Ctrl+Shift+E`):

```
📂 executive-summary-agent/
├── .env                ← Environment variables (placeholders)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Agent entry point (your main code)
└── requirements.txt    ← Python dependencies
```

### Explicação dos ficheiros chave

| Ficheiro | Finalidade |
|------|---------|
| `agent.yaml` | Declara o agente como `kind: hosted`, mapeia variáveis do ambiente, define o protocolo `/responses` |
| `main.py` | Cria um `FoundryChatClient` → encapsula-o num `Agent` com instruções → serve via `ResponsesHostServer` na porta 8088 |
| `Dockerfile` | Usa `python:3.12-slim`, instala dependências, expõe a porta 8088, executa `main.py` |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp`, `debugpy` |

> **Importante:** Abra a pasta do agente criada diretamente no VS Code (a pasta `agent/` propriamente dita) para que `.vscode/launch.json` e `tasks.json` funcionem corretamente na depuração com F5.

---

### ✅ Ponto de Verificação

- [ ] Projeto scaffolded criado com todos os ficheiros esperados
- [ ] `agent.yaml` mostra `kind: hosted` e `protocol: responses`
- [ ] `main.py` importa `Agent`, `FoundryChatClient`, `ResponsesHostServer`
- [ ] A pasta do agente está aberta no VS Code como raiz do espaço de trabalho

---

**Anterior:** [01 - Setup](01-setup.md) · **Seguinte:** [03 - Configurar & Codificar →](03-configure-and-code.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->