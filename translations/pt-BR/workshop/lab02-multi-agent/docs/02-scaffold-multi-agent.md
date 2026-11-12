# Módulo 2 - Estruture o Projeto Multiagente

⏱️ ~5 min

Neste módulo, você usa [Foundry Toolkit para VS Code](https://aka.ms/foundrytk) para **estruturar um projeto multiagente**. O assistente gera `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`, e a configuração de depuração do VS Code - para que você possa se concentrar em conectar o fluxo de trabalho de 4 agentes no Módulo 3.

> **Conceito-chave:** O scaffold é um esqueleto funcional com um agente. Você substitui a lógica de espaço reservado pelo grafo `WorkflowBuilder` no Módulo 3. Você não precisa escrever o boilerplate do zero.

> **Implementação de referência:** [`PersonalCareerCopilot/`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot) é um exemplo completo de funcionamento. Use-o para comparar seu trabalho conforme avança.

### Fluxo do assistente de scaffold

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

## Etapa 1: Abra o assistente Create Hosted Agent

1. Pressione `Ctrl+Shift+P` para abrir a **Paleta de Comandos**.
2. Digite: **Foundry Toolkit: Create a New Hosted Agent** e selecione-o.
3. O assistente abre na aba **Agent Details**.

> **Alternativa:** Clique no ícone **Foundry Toolkit** na Activity Bar → clique no ícone **+** ao lado de **Hosted Agents** → **Create New Hosted Agent**.

---

## Etapa 2: Escolha as configurações

![Criar Hosted Agent a partir do Exemplo - aba Agent Details com o template Workflows selecionado](../../../../../workshop/lab02-multi-agent/docs/images/02-scaffold-wizard-details.png)

1. Na seção de navegação/opções à esquerda, selecione o seguinte:

| Menu | Seleção | Observações |
|--------|-----------|-------|
| **Linguagem** | Python | C# (.NET) também suportado |
| **Framework** | Agent Framework | Fornece `Agent`, `AgentExecutor`, `WorkflowBuilder` |
| **Tipo de API** | Response API | `POST /responses` - histórico gerenciado pela plataforma, suporte a streaming |
| **Modelo** | **Workflows** | Processa solicitações por múltiplos agentes em sequência |

2. Depois de selecionar, clique em **Next**

![Criar Hosted Agent a partir do Exemplo - aba Create mostrando PersonalCareerCopilot como o nome da pasta](../../../../../workshop/lab02-multi-agent/docs/images/02-scaffold-wizard-create.png)

3. Na próxima janela, selecione o seguinte:

| Menu | Seleção | Observações |
|--------|-----------|-------|
| **Pasta do workspace** | Navegue até a pasta de destino | ex.: `workshop/lab02-multi-agent/` neste repositório |
| **Nome do agente** | `PersonalCareerCopilot` | Isto se tornará o nome do diretório do projeto |
| **Implantação do Modelo** | Selecione seu modelo implantado | ex.: `gpt-4.1-mini` do Lab 01 |

4. Clique em **Create** para estruturar o projeto. O VS Code gera os arquivos e abre a pasta.

> **Dica:** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series) equilibra bem velocidade e qualidade para desenvolvimento multiagente.

---

## Etapa 3: Inspecione o projeto gerado

Após a conclusão do scaffold, verifique se você vê estes arquivos no Explorer (`Ctrl+Shift+E`):

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

> **Importante:** Abra esta pasta gerada diretamente no VS Code para que `.vscode/launch.json` e `tasks.json` se apliquem corretamente para depuração com F5.

### Arquivos principais explicados

| Arquivo | Finalidade |
|------|---------|
| `agent.yaml` | Declara `kind: hosted`, mapeia variáveis de ambiente, define o protocolo `/responses` |
| `main.py` | Stub: um `FoundryChatClient` → `Agent` → `ResponsesHostServer`. Você substitui isto por 4 agentes + `WorkflowBuilder` no Módulo 3 |
| `Dockerfile` | `python:3.12-slim`, instala `requirements.txt`, expõe a porta 8088, executa `python main.py` |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp<2,>=1.24.0`, `debugpy` |

> **Referência:** Veja [`PersonalCareerCopilot/agent.yaml`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) e [`PersonalCareerCopilot/requirements.txt`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/requirements.txt) para o conteúdo completo gerado.

---

### ✅ Ponto de verificação

- [ ] Assistente de scaffold concluído - nova pasta do projeto está visível no Explorer
- [ ] Todos os arquivos esperados presentes: `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`
- [ ] `agent.yaml` mostra `kind: hosted` e `protocol: responses`
- [ ] `main.py` importa `Agent`, `FoundryChatClient`, `ResponsesHostServer`
- [ ] A pasta gerada está aberta como raiz do espaço de trabalho do VS Code
- [ ] Você entende que `main.py` é um stub - `WorkflowBuilder` é adicionado no Módulo 3

---

**Anterior:** [01 - Entenda a Arquitetura Multiagente](01-understand-multi-agent.md) · **Próximo:** [03 - Configure Agentes & Ambiente →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->