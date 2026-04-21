# PersonalCareerCopilot - Avaliador de Adequação Currículo → Vaga

Um fluxo de trabalho multiagente que avalia quão bem um currículo corresponde a uma descrição de vaga, depois gera um roteiro de aprendizado personalizado para fechar as lacunas.

---

## Agentes

| Agente | Função | Ferramentas |
|--------|--------|-------------|
| **ResumeParser** | Extrai habilidades estruturadas, experiência, certificações do texto do currículo | - |
| **JobDescriptionAgent** | Extrai habilidades, experiência, certificações requeridas/preferidas de uma vaga | - |
| **MatchingAgent** | Compara perfil vs requisitos → pontuação de adequação (0-100) + habilidades correspondentes/faltantes | - |
| **GapAnalyzer** | Constrói um roteiro de aprendizado personalizado com recursos da Microsoft Learn | `search_microsoft_learn_for_plan` (MCP) |

## Fluxo de trabalho

```mermaid
flowchart TD
    UserInput["Entrada do Usuário: Currículo + Descrição do Trabalho"] --> ResumeParser
    UserInput --> JobDescriptionAgent
    ResumeParser --> MatchingAgent
    JobDescriptionAgent --> MatchingAgent
    MatchingAgent --> GapAnalyzerMCP["Analisador de Lacunas &
    Documentos MCP do Microsoft Learn"]
    GapAnalyzerMCP --> FinalOutput["Resultado Final:
     Pontuação de Adequação + Roteiro"]
```
---

## Início rápido

### 1. Configurar ambiente

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. Configurar credenciais

Copie o arquivo de exemplo .env e preencha com os detalhes do seu projeto Foundry:

```powershell
cp .env.example .env
```

Edite `.env`:

```env
PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| Valor | Onde encontrar |
|-------|----------------|
| `PROJECT_ENDPOINT` | Barra lateral do Microsoft Foundry no VS Code → clique com o botão direito no seu projeto → **Copiar Endpoint do Projeto** |
| `MODEL_DEPLOYMENT_NAME` | Barra lateral do Foundry → expanda o projeto → **Models + endpoints** → nome do deployment |

### 3. Executar localmente

```powershell
python -m debugpy --listen 127.0.0.1:5679 -m agentdev run main.py --verbose --port 8088
```

Ou use a tarefa do VS Code: `Ctrl+Shift+P` → **Tasks: Run Task** → **Run Lab02 HTTP Server**.

### 4. Testar com Agent Inspector

Abra o Agent Inspector: `Ctrl+Shift+P` → **Foundry Toolkit: Open Agent Inspector**.

Cole este prompt de teste:

```
Resume:
Jane Doe
Senior Software Engineer with 5 years of experience in Python, Django, and AWS.
Built microservices handling 10K+ requests/second. Led a team of 4 developers.
Certifications: AWS Solutions Architect Associate.
Education: B.S. Computer Science, State University.

Job Description:
Senior Cloud Engineer at Contoso Ltd.
Required: Python, Azure, Kubernetes, Terraform, CI/CD pipelines.
Preferred: Go, monitoring (Prometheus/Grafana), cost optimization.
Experience: 5+ years in cloud infrastructure.
Certifications: Azure Solutions Architect Expert preferred.
```

**Esperado:** Uma pontuação de adequação (0-100), habilidades correspondentes/faltantes e um roteiro de aprendizado personalizado com URLs da Microsoft Learn.

### 5. Fazer o deploy no Foundry

`Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → selecione seu projeto → confirme.

---

## Estrutura do projeto

```
PersonalCareerCopilot/
├── .env.example        ← Template for environment variables
├── .env                ← Your credentials (git-ignored)
├── agent.yaml          ← Hosted agent definition (name, resources, env vars)
├── Dockerfile          ← Container image for Foundry deployment
├── main.py             ← 4-agent workflow (instructions, MCP tool, WorkflowBuilder)
└── requirements.txt    ← Python dependencies
```

## Arquivos principais

### `agent.yaml`

Define o agente hospedado para o Foundry Agent Service:
- `kind: hosted` - roda como um container gerenciado
- `protocols: [responses v1]` - expõe o endpoint HTTP `/responses`
- `environment_variables` - `PROJECT_ENDPOINT` e `MODEL_DEPLOYMENT_NAME` são injetados no momento do deploy

### `main.py`

Contém:
- **Instruções dos agentes** - quatro constantes `*_INSTRUCTIONS`, uma para cada agente
- **Ferramenta MCP** - `search_microsoft_learn_for_plan()` faz chamada ao `https://learn.microsoft.com/api/mcp` via Streamable HTTP
- **Criação dos agentes** - gerenciador de contexto `create_agents()` usando `AzureAIAgentClient.as_agent()`
- **Fluxo de trabalho** - `create_workflow()` usa `WorkflowBuilder` para conectar agentes com padrões fan-out/fan-in/seqüenciais
- **Inicialização do servidor** - `from_agent_framework(agent).run_async()` na porta 8088

### `requirements.txt`

| Pacote | Versão | Propósito |
|--------|--------|-----------|
| `agent-framework-azure-ai` | `1.0.0rc3` | Integração Azure AI para Microsoft Agent Framework |
| `agent-framework-core` | `1.0.0rc3` | Runtime principal (inclui WorkflowBuilder) |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | Runtime do servidor de agente hospedado |
| `azure-ai-agentserver-core` | `1.0.0b16` | Abstrações principais do servidor de agentes |
| `debugpy` | última | Depuração Python (F5 no VS Code) |
| `agent-dev-cli` | `--pre` | CLI local de desenvolvimento + backend do Agent Inspector |

---

## Solução de problemas

| Problema | Solução |
|----------|---------|
| `RuntimeError: Missing required environment variable(s)` | Crie `.env` com `PROJECT_ENDPOINT` e `MODEL_DEPLOYMENT_NAME` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Ative o venv e execute `pip install -r requirements.txt` |
| Nenhum URL da Microsoft Learn na saída | Verifique a conectividade com `https://learn.microsoft.com/api/mcp` |
| Apenas 1 cartão de lacuna (cortado) | Verifique se `GAP_ANALYZER_INSTRUCTIONS` inclui o bloco `CRITICAL:` |
| Porta 8088 já em uso | Pare outros servidores: `netstat -ano \| findstr :8088` |

Para solução detalhada, veja [Módulo 8 - Troubleshooting](../docs/08-troubleshooting.md).

---

**Guia completo:** [Lab 02 Docs](../docs/README.md) · **Voltar para:** [Lab 02 README](../README.md) · [Página Inicial do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, é recomendada a tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->