# PersonalCareerCopilot - Avaliador de Ajuste CV → Emprego

Uma aplicação multi-agente, orientada por fluxo de trabalho, que avalia o quão bem um currículo corresponde a uma descrição de trabalho, e depois gera um roteiro de aprendizagem personalizado para colmatar as lacunas.

---

## Agentes

| Agente | Função | Ferramentas |
|-------|------|-------|
| **ResumeParser** | Extrai competências estruturadas, experiência, certificações do texto do currículo | - |
| **JobDescriptionAgent** | Extrai competências requeridas/preferenciais, experiência, certificações de uma JD | - |
| **MatchingAgent** | Compara perfil vs requisitos → pontuação de ajuste (0-100) + competências correspondentes/faltantes | - |
| **GapAnalyzer** | Constrói um roteiro de aprendizagem personalizado com recursos do Microsoft Learn | `search_microsoft_learn_for_plan` (MCP) |

## Fluxo de trabalho

```mermaid
flowchart LR
    UserInput["User Input: Resume + Job Description"] --> ResumeParser
    ResumeParser -- "parsed resume + JD relay" --> JobDescriptionAgent
    JobDescriptionAgent -- "JD requirements + resume relay" --> MatchingAgent
    MatchingAgent -- "fit report + gaps" --> GapAnalyzerMCP["Gap Analyzer +\nMicrosoft Learn MCP"]
    GapAnalyzerMCP --> FinalOutput["Final Output:\nFit Score + Roadmap"]
```

---

## Início rápido

### 1. Configurar ambiente

Esta pasta é a implementação de referência para o esqueleto do Lab 02 baseado em fluxo de trabalho. O seu `main.py` usa os blocos de prompt existentes mais `WorkflowBuilder` para ligar os quatro agentes.

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. Configurar credenciais

Crie um ficheiro `.env` nesta pasta:

```powershell
copy .env .env.bak 2>$null; echo $null > .env
```

Edite `.env`:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| Valor | Onde encontrar |
|-------|------------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Barra lateral do Foundry Toolkit → clique direito no seu projeto → **Copiar Ponto de Extremidade do Projeto** |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Barra lateral do Foundry → expandir projeto → **Modelos + pontos finais** → nome do deployment |

### 3. Executar localmente

```powershell
python -m debugpy --listen 127.0.0.1:5679 main.py --port 8088
```

Ou use a tarefa do VS Code: `Ctrl+Shift+P` → **Tarefas: Executar Tarefa** → **Executar Servidor HTTP do Agente**.

Para depuração F5, use **Depurar Servidor HTTP do Agente Local**.

### 4. Testar com Agent Inspector

Abra Agent Inspector: `Ctrl+Shift+P` → **Foundry Toolkit: Abrir Agent Inspector**.

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

**Esperado:** Uma pontuação de ajuste (0-100), competências correspondentes/faltantes, e um roteiro de aprendizagem personalizado com URLs do Microsoft Learn.

### 5. Fazer deploy no Foundry

`Ctrl+Shift+P` → **Foundry Toolkit: Fazer Deploy do Agente Hospedado** → selecione o seu projeto → confirmar.

---

## Estrutura do projeto

```
PersonalCareerCopilot/
├── .env                ← Your credentials (git-ignored)
├── agent.yaml          ← Hosted agent definition (name, resources, env vars)
├── Dockerfile          ← Container image for Foundry deployment
├── main.py             ← 4-agent workflow (instructions, MCP tool, WorkflowBuilder)
└── requirements.txt    ← Python dependencies
```

## Ficheiros chave

### `agent.yaml`

Define o agente hospedado para Foundry Agent Service:
- `kind: hosted` - executa-se como um contentor gerido
- `protocols` - protocolo `responses` com `version: 2.0.0`, expondo o endpoint HTTP `/responses`
- `environment_variables` - `AZURE_AI_MODEL_DEPLOYMENT_NAME` é declarado aqui; `FOUNDRY_PROJECT_ENDPOINT` é injetado automaticamente em tempo de deploy

### `main.py`

Contém:
- **Instruções de agente** - quatro constantes `*_INSTRUCTIONS`, uma por agente
- **Ferramenta MCP** - `search_microsoft_learn_for_plan()` chama `https://learn.microsoft.com/api/mcp` via HTTP Streamable
- **Criação de agente** - quatro instâncias `Agent()` + `AgentExecutor()` compartilhando um `FoundryChatClient`
- **Grafo do fluxo de trabalho** - `WorkflowBuilder` liga agentes num pipeline sequencial: ResumeParser → Agente JD → MatchingAgent → GapAnalyzer
- **Arranque do servidor** - `ResponsesHostServer` corre na porta 8088

### `requirements.txt`

| Pacote | Propósito |
|---------|----------|
| `agent-framework-foundry` | Runtime central: `Agent`, `AgentExecutor`, `WorkflowBuilder`, `@tool`, `FoundryChatClient` |
| `agent-framework-foundry-hosting` | Integração de hosting com Foundry + `ResponsesHostServer` |
| `mcp<2,>=1.24.0` | Cliente MCP para GapAnalyzer (`streamable_http_client`) |
| `debugpy` | Depuração Python (F5 no VS Code) |

---

## Resolução de problemas

| Problema | Correção |
|-------|-----|
| `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ou `KeyError: 'AZURE_AI_MODEL_DEPLOYMENT_NAME'` | Crie `.env` com ambos `FOUNDRY_PROJECT_ENDPOINT` e `AZURE_AI_MODEL_DEPLOYMENT_NAME` configurados |
| `ModuleNotFoundError: No module named 'agent_framework'` | Ative venv e execute `pip install -r requirements.txt` |
| Nenhum URL do Microsoft Learn na saída | Verifique a conectividade à internet para `https://learn.microsoft.com/api/mcp` |
| Apenas 1 cartão de lacuna (cortado) | Verifique se `GAP_ANALYZER_INSTRUCTIONS` inclui o bloco `CRITICAL:` |
| Porta 8088 em uso | Pare outros servidores: `netstat -ano \| findstr :8088` |

Para resolução de problemas detalhada, veja [Módulo 8 - Resolução de Problemas](../docs/08-troubleshooting.md).

---

**Guia completo:** [Documentos do Lab 02](../docs/README.md) · **Voltar para:** [README do Lab 02](../README.md) · [Página Principal do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->