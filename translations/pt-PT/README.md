# Foundry Toolkit + Workshop Agentes Hospedados Foundry

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.0.0rc3-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents/)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Construa, teste e implemente agentes de IA para o **Microsoft Foundry Agent Service** como **Agentes Hospedados** – tudo a partir do VS Code usando a **extensão Microsoft Foundry** e o **Foundry Toolkit**.

> **Os Agentes Hospedados estão atualmente em pré-visualização.** As regiões suportadas são limitadas - consulte a [disponibilidade por região](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> A pasta `agent/` dentro de cada laboratório é **automaticamente criada** pela extensão Foundry - depois personaliza o código, testa localmente e implementa.

### 🌐 Suporte Multilingue

#### Suportado via GitHub Action (Automatizado & Sempre Atualizado)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Árabe](../ar/README.md) | [Bengali](../bn/README.md) | [Búlgaro](../bg/README.md) | [Birmanês (Myanmar)](../my/README.md) | [Chinês (Simplificado)](../zh-CN/README.md) | [Chinês (Tradicional, Hong Kong)](../zh-HK/README.md) | [Chinês (Tradicional, Macau)](../zh-MO/README.md) | [Chinês (Tradicional, Taiwan)](../zh-TW/README.md) | [Croata](../hr/README.md) | [Checo](../cs/README.md) | [Dinamarquês](../da/README.md) | [Holandês](../nl/README.md) | [Estónio](../et/README.md) | [Finlandês](../fi/README.md) | [Francês](../fr/README.md) | [Alemão](../de/README.md) | [Grego](../el/README.md) | [Hebraico](../he/README.md) | [Hindi](../hi/README.md) | [Húngaro](../hu/README.md) | [Indonésio](../id/README.md) | [Italiano](../it/README.md) | [Japonês](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malaio](../ms/README.md) | [Malaiala](../ml/README.md) | [Marata](../mr/README.md) | [Nepali](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Norueguês](../no/README.md) | [Persa (Farsi)](../fa/README.md) | [Polaco](../pl/README.md) | [Português (Brasil)](../pt-BR/README.md) | [Português (Portugal)](./README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romeno](../ro/README.md) | [Russo](../ru/README.md) | [Sérvio (Cirílico)](../sr/README.md) | [Eslovaco](../sk/README.md) | [Esloveno](../sl/README.md) | [Espanhol](../es/README.md) | [Suaíli](../sw/README.md) | [Sueco](../sv/README.md) | [Tagalo (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tailandês](../th/README.md) | [Turco](../tr/README.md) | [Ucraniano](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **Prefere Clonar Localmente?**
>
> Este repositório inclui mais de 50 traduções, o que aumenta significativamente o tamanho do download. Para clonar sem traduções, utilize checkout esparso:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Isto fornece tudo o que necessita para completar o curso com um download muito mais rápido.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arquitetura

```mermaid
flowchart TB
    subgraph Local["Desenvolvimento Local (VS Code)"]
        direction TB
        FE["Extensão Microsoft Foundry"]
        FoundryToolkit["Extensão Foundry Toolkit"]
        Scaffold["Código de Agente Scaffolded
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Inspetor de Agente
        (Teste Local)"]
        FE -- "Criar Novo
        Agente Hospedado" --> Scaffold
        Scaffold -- "F5 Depurar" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Registo de Contentores Azure"]
        AgentService["Serviço de Agente Foundry
        (Runtime do Agente Hospedado)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Playground Foundry
        & Playground VS Code"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Implantar
    (Build Docker + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Testar prompts" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**Fluxo:** A extensão Foundry cria a estrutura do agente → você personaliza o código e as instruções → testa localmente com o Agent Inspector → implementa no Foundry (imagem Docker enviada para o ACR) → verifica no Playground.

---

## O que vai construir

| Laboratório | Descrição | Estado |
|-------------|-----------|--------|
| **Lab 01 - Agente Único** | Construa o **Agente "Explique Como se Eu Fosse um Executivo"**, teste localmente e implemente no Foundry | ✅ Disponível |
| **Lab 02 - Fluxo de Trabalho Multiagente** | Construa o **"Avaliador de Compatibilidade entre Currículo e Emprego"** - 4 agentes colaboram para avaliar a compatibilidade e gerar um plano de aprendizagem | ✅ Disponível |

---

## Conheça o Agente Executivo

Neste workshop irá construir o **Agente "Explique Como se Eu Fosse um Executivo"** – um agente de IA que transforma jargão técnico complicado em resumos calmos e prontos para reuniões de conselho. Porque sejamos honestos, ninguém na alta direção quer ouvir sobre “exaustão do pool de threads causada por chamadas síncronas introduzidas na v3.2.”

Construí este agente após incidentes em que a minha análise pós-morte perfeitamente elaborada recebeu como resposta: *“Então... o site está em baixo ou não?”*

### Como funciona

Fornece uma atualização técnica. Ele devolve um resumo executivo – três pontos curtos, sem jargão, sem rastos de pilha, sem pânico existencial. Apenas **o que aconteceu**, **impacto no negócio** e **próximo passo**.

### Veja em ação

**Você diz:**
> "A latência da API aumentou devido à exaustão do pool de threads causada por chamadas síncronas introduzidas na v3.2."

**O agente responde:**

> **Resumo Executivo:**
> - **O que aconteceu:** Após a última versão, o sistema ficou mais lento.
> - **Impacto no negócio:** Alguns utilizadores experienciaram atrasos ao usar o serviço.
> - **Próximo passo:** A alteração foi revertida e uma correção está a ser preparada antes da nova implementação.

### Por que este agente?

É um agente simples e com propósito único – perfeito para aprender o fluxo de agentes hospedados de ponta a ponta sem se perder em cadeias complexas de ferramentas. E honestamente? Toda equipa de engenharia poderia usar um destes.

---

## Estrutura do workshop

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
├── 📂 ExecutiveAgent/                ← Standalone hosted agent project
│   ├── agent.yaml
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-install-foundry-toolkit.md
    │   │   ├── 02-create-foundry-project.md
    │   │   ├── 03-create-hosted-agent.md
    │   │   ├── 04-configure-and-code.md
    │   │   ├── 05-test-locally.md
    │   │   ├── 06-deploy-to-foundry.md
    │   │   ├── 07-verify-in-playground.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **Nota:** A pasta `agent/` dentro de cada laboratório é gerada pela **extensão Microsoft Foundry** quando executa `Microsoft Foundry: Create a New Hosted Agent` no Command Palette. Os ficheiros são depois personalizados com as instruções, ferramentas e configuração do agente. O Lab 01 guia-o para recriar este processo do zero.

---

## Começar

### 1. Clonar o repositório

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Configurar um ambiente virtual Python

```bash
python -m venv venv
```

Ative-o:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependências

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o ficheiro `.env` de exemplo dentro da pasta do agente e preencha os seus valores:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Edite `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Siga os laboratórios do workshop

Cada laboratório é autónomo com os seus próprios módulos. Comece pelo **Lab 01** para aprender o básico, depois avance para o **Lab 02** para fluxos multiagente.

#### Lab 01 - Agente Único ([instruções completas](workshop/lab01-single-agent/README.md))

| # | Módulo | Link |
|---|--------|------|
| 1 | Leia os pré-requisitos | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Instale Foundry Toolkit & extensão Foundry | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Crie um projeto Foundry | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | Crie um agente hospedado | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | Configure instruções & ambiente | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | Teste localmente | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Implemente no Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verifique no playground | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | Resolução de problemas | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Fluxo de Trabalho Multiagente ([instruções completas](workshop/lab02-multi-agent/README.md))

| # | Módulo | Link |
|---|--------|------|
| 1 | Pré-requisitos (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Compreender a arquitetura multiagente | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Criar a estrutura do projeto multiagente | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Configure agentes & ambiente | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Padrões de orquestração | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Teste localmente (multiagente) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Implantar no Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verificar no playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Resolução de problemas (multi-agente) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Mantenedor

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## Permissões necessárias (referência rápida)

| Cenário | Funções necessárias |
|----------|-------------------|
| Criar novo projeto Foundry | **Azure AI Owner** no recurso Foundry |
| Implantar em projeto existente (novos recursos) | **Azure AI Owner** + **Contributor** na subscrição |
| Implantar em projeto totalmente configurado | **Reader** na conta + **Azure AI User** no projeto |

> **Importante:** As funções `Owner` e `Contributor` do Azure incluem apenas permissões de *gerenciamento*, não permissões de *desenvolvimento* (ação de dados). Precisa de **Azure AI User** ou **Azure AI Owner** para construir e implantar agentes.

---

## Referências

- [Início rápido: Implemente o seu primeiro agente alojado (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [O que são agentes alojados?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Criar fluxos de trabalho de agente alojado no VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Implantar um agente alojado](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Exemplo de agente de revisão de arquitetura](https://github.com/Azure-Samples/agent-architecture-review-sample) - Agente alojado real com ferramentas MCP, diagramas Excalidraw e implantação dual

---


## Licença

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, tenha em atenção que traduções automáticas podem conter erros ou imprecisões. O documento original no seu idioma nativo deve ser considerado a fonte autorizada. Para informação crítica, recomenda-se tradução humana profissional. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações erradas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->