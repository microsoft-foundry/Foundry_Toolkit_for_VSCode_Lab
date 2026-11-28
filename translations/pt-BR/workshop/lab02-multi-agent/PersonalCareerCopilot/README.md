# PersonalCareerCopilot - Avaliador de Adequação Currículo → Vaga

Um aplicativo multiagente orientado por fluxo de trabalho que avalia o quanto um currículo corresponde a uma descrição de vaga, e então gera um roteiro de aprendizado personalizado para fechar as lacunas.

---

## Agentes

| Agente | Função | Ferramentas |
|-------|--------|------------|
| **ResumeParser** | Extrai habilidades estruturadas, experiência, certificações do texto do currículo | - |
| **JobDescriptionAgent** | Extrai habilidades, experiência, certificações obrigatórias/preferidas de uma descrição de vaga | - |
| **MatchingAgent** | Compara o perfil vs requisitos → pontuação de adequação (0-100) + habilidades comprovadas/faltantes | - |
| **GapAnalyzer** | Constrói um roteiro de aprendizado personalizado com recursos Microsoft Learn | `search_microsoft_learn_for_plan` (MCP) |

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

Esta pasta é a implementação de referência para o esqueleto do Lab 02 baseado no fluxo de trabalho. Seu `main.py` usa os blocos de prompt existentes mais `WorkflowBuilder` para conectar os quatro agentes.

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. Configurar credenciais

Crie um arquivo `.env` nesta pasta:

```powershell
copy .env .env.bak 2>$null; echo $null > .env
```

Edite `.env`:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| Valor | Onde encontrar |
|-------|----------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Barra lateral do Foundry Toolkit → clique direito no seu projeto → **Copiar endpoint do projeto** |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Barra lateral do Foundry → expanda o projeto → **Modelos + endpoints** → nome do deployment |

### 3. Executar localmente

```powershell
python -m debugpy --listen 127.0.0.1:5679 main.py --port 8088
```

Ou use a tarefa do VS Code: `Ctrl+Shift+P` → **Tarefas: Executar tarefa** → **Executar servidor HTTP do agente**.

Para depuração com F5, use **Depurar servidor HTTP local do agente**.

### 4. Testar com o Agent Inspector

Abra o Agent Inspector: `Ctrl+Shift+P` → **Foundry Toolkit: Abrir Agent Inspector**.

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

**Esperado:** Uma pontuação de adequação (0-100), habilidades comprovadas/faltantes, e um roteiro de aprendizado personalizado com URLs do Microsoft Learn.

### 5. Publicar no Foundry

`Ctrl+Shift+P` → **Foundry Toolkit: Publicar agente hospedado** → selecione seu projeto → confirme.

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

## Arquivos chave

### `agent.yaml`

Define o agente hospedado para o Foundry Agent Service:
- `kind: hosted` - executa como um container gerenciado
- `protocols` - protocolo `responses` com `version: 2.0.0`, expondo o endpoint HTTP `/responses`
- `environment_variables` - `AZURE_AI_MODEL_DEPLOYMENT_NAME` é declarado aqui; `FOUNDRY_PROJECT_ENDPOINT` é injetado automaticamente na implantação

### `main.py`

Contém:
- **Instruções do agente** - quatro constantes `*_INSTRUCTIONS`, uma por agente
- **Ferramenta MCP** - `search_microsoft_learn_for_plan()` chama `https://learn.microsoft.com/api/mcp` via HTTP Streamable
- **Criação do agente** - quatro instâncias `Agent()` + `AgentExecutor()` compartilhando um `FoundryChatClient`
- **Gráfico do fluxo de trabalho** - `WorkflowBuilder` conecta agentes como pipeline sequencial: ResumeParser → Agente JD → MatchingAgent → GapAnalyzer
- **Inicialização do servidor** - `ResponsesHostServer` roda na porta 8088

### `requirements.txt`

| Pacote | Propósito |
|---------|-----------|
| `agent-framework-foundry` | Runtime principal: `Agent`, `AgentExecutor`, `WorkflowBuilder`, `@tool`, `FoundryChatClient` |
| `agent-framework-foundry-hosting` | `ResponsesHostServer` + Integração com hospedagem Foundry |
| `mcp<2,>=1.24.0` | Cliente MCP para GapAnalyzer (`streamable_http_client`) |
| `debugpy` | Depuração Python (F5 no VS Code) |

---

## Solução de problemas

| Problema | Solução |
|---------|---------|
| `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ou `KeyError: 'AZURE_AI_MODEL_DEPLOYMENT_NAME'` | Crie `.env` com `FOUNDRY_PROJECT_ENDPOINT` e `AZURE_AI_MODEL_DEPLOYMENT_NAME` configurados |
| `ModuleNotFoundError: No module named 'agent_framework'` | Ative o venv e execute `pip install -r requirements.txt` |
| Sem URLs Microsoft Learn na saída | Verifique a conectividade com a internet para `https://learn.microsoft.com/api/mcp` |
| Apenas 1 cartão de lacuna (truncado) | Verifique se `GAP_ANALYZER_INSTRUCTIONS` inclui o bloco `CRITICAL:` |
| Porta 8088 em uso | Pare outros servidores: `netstat -ano \| findstr :8088` |

Para solução detalhada de problemas, veja [Módulo 8 - Solução de Problemas](../docs/08-troubleshooting.md).

---

**Tutorial completo:** [Documentação do Lab 02](../docs/README.md) · **Voltar para:** [README do Lab 02](../README.md) · [Página Inicial do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->