# Módulo 2 - Estruturar o Projeto Multi-Agente

⏱️ ~5 min

Neste módulo, usa o [Foundry Toolkit para VS Code](https://aka.ms/foundrytk) para **estruturar um projeto multi-agente**. O assistente gera `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`, e a configuração de depuração do VS Code - para que possa concentrar-se em ligar o fluxo de trabalho dos 4 agentes no Módulo 3.

> **Conceito chave:** A estrutura é um esboço funcional com um agente. Substitui a lógica temporária pelo grafo `WorkflowBuilder` no Módulo 3. Não precisa de escrever o código base do zero.

> **Implementação de referência:** [`PersonalCareerCopilot/`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot) é um exemplo funcional completo. Use-o para comparar o seu trabalho à medida que avança.

### Fluxo do assistente de estruturação

```mermaid
flowchart LR
    A[Command Palette: Create New Hosted Agent] --> B[Language: Python]
    B --> C[API Type: Response API]
    C --> D[Template: Workflows]
    D --> E[Select Model]
    E --> F[Workspace Folder and Agent Name]
    F --> G[Generated Project]
```

---

## Passo 1: Abrir o assistente Criar Agente Hospedado

1. Pressione `Ctrl+Shift+P` para abrir a **Paleta de Comandos**.
2. Escreva: **Foundry Toolkit: Create new Hosted Agent** e selecione.
3. O assistente abre no separador **Detalhes do Agente**.

> **Alternativa:** Clique no ícone **Foundry Toolkit** na Barra de Atividades → clique no ícone **+** ao lado de **Hosted Agents** → **Create New Hosted Agent**.

---

## Passo 2: Escolher configurações

![Criar Agente Hospedado a partir de Exemplo - Separador Detalhes do Agente com o modelo Workflows selecionado](../../../../../translated_images/pt-PT/02-scaffold-wizard-details.af4798708b4a87f4.webp)

1. Na secção de navegação/opções à esquerda selecione o seguinte:

| Menu | Seleção | Notas |
|--------|-----------|-------|
| **Linguagem** | Python | C# (.NET) também suportado |
| **Framework** | Agent Framework | Fornece `Agent`, `AgentExecutor`, `WorkflowBuilder` |
| **Tipo de API** | Response API | `POST /responses` - histórico gerido pela plataforma, suporte a streaming |
| **Modelo** | **Workflows** | Processa pedidos através de múltiplos agentes em sequência |

2. Uma vez selecionado, clique em **Next**

![Criar Agente Hospedado a partir de Exemplo - Separador Criar mostrando PersonalCareerCopilot como nome da pasta](../../../../../translated_images/pt-PT/02-scaffold-wizard-create.ae0c285c309698ba.webp)

3. Na janela seguinte, selecione o seguinte:

| Menu | Seleção | Notas |
|--------|-----------|-------|
| **Pasta do espaço de trabalho** | Procurar pasta destino | ex., `workshop/lab02-multi-agent/` neste repositório |
| **Nome do agente** | `PersonalCareerCopilot` | Este será o nome da diretoria do projeto |
| **Deploy do Modelo** | Selecione o seu modelo implantado | ex., `gpt-4.1-mini` do Lab 01 |

4. Clique em **Create** para estruturar o projeto. O VS Code gera os ficheiros e abre a pasta.

> **Dica:** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series) equilibra bem velocidade e qualidade para desenvolvimento multi-agente.

---

## Passo 3: Inspecionar o projeto gerado

Após a estruturação, verifique que vê estes ficheiros no Explorador (`Ctrl+Shift+E`):

```
📂 <your-agent-name>/
├── .azdignore          ← Files excluded from Azure Developer CLI deployments
├── .dockerignore       ← Files excluded from Docker builds
├── .env                ← Environment variables (placeholders - fill in Module 3)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted, protocol: responses)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Stub agent entry point (replace with WorkflowBuilder in Module 3)
└── requirements.txt    ← Python dependencies
```

> **Importante:** Abra esta pasta estruturada diretamente no VS Code para que `.vscode/launch.json` e `tasks.json` funcionem corretamente para depuração com F5.

### Ficheiros chave explicados

| Ficheiro | Propósito |
|------|---------|
| `agent.yaml` | Declara `kind: hosted`, mapeia variáveis de ambiente, define o protocolo `/responses` |
| `main.py` | Esboço: um `FoundryChatClient` → `Agent` → `ResponsesHostServer`. Vai substituir por 4 agentes + `WorkflowBuilder` no Módulo 3 |
| `Dockerfile` | `python:3.12-slim`, instala `requirements.txt`, expõe a porta 8088, executa `python main.py` |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp<2,>=1.24.0`, `debugpy` |

> **Referência:** Veja [`PersonalCareerCopilot/agent.yaml`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) e [`PersonalCareerCopilot/requirements.txt`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/requirements.txt) para o conteúdo gerado completo.

---

### ✅ Ponto de verificação

- [ ] Assistente de estruturação concluído - nova pasta do projeto visível no Explorador
- [ ] Todos os ficheiros esperados presentes: `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`
- [ ] `agent.yaml` mostra `kind: hosted` e `protocol: responses`
- [ ] `main.py` importa `Agent`, `FoundryChatClient`, `ResponsesHostServer`
- [ ] Pasta estruturada está aberta como raiz do espaço de trabalho VS Code
- [ ] Compreende que `main.py` é um esboço - `WorkflowBuilder` é adicionado no Módulo 3

---

**Anterior:** [01 - Compreender a Arquitetura Multi-Agente](01-understand-multi-agent.md) · **Seguinte:** [03 - Configurar Agentes & Ambiente →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->