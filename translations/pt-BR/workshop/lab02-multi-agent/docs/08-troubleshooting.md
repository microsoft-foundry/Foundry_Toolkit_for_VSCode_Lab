# Módulo 8 - Solução de Problemas (Multi-Agente)

Este módulo aborda erros comuns, correções e estratégias de depuração específicas para o fluxo de trabalho multi-agente. Para problemas gerais de implantação no Foundry, consulte também o [guia de solução de problemas do Laboratório 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Referência rápida: Erro → Correção

| Erro / Sintoma | Causa Provável | Correção |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Arquivo `.env` ausente ou valores não definidos | Crie `.env` com `PROJECT_ENDPOINT=<seu-endpoint>` e `MODEL_DEPLOYMENT_NAME=<seu-modelo>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Ambiente virtual não ativado ou dependências não instaladas | Execute `.\.venv\Scripts\Activate.ps1` e depois `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Pacote MCP não instalado (ausente nos requisitos) | Execute `pip install mcp` ou verifique se `requirements.txt` o inclui como dependência transitiva |
| Agente inicia mas retorna resposta vazia | `output_executors` incorreto ou arestas ausentes | Verifique `output_executors=[gap_analyzer]` e se todas as arestas existem em `create_workflow()` |
| Apenas 1 cartão de gap (restantes ausentes) | Instruções do GapAnalyzer incompletas | Adicione o parágrafo `CRITICAL:` em `GAP_ANALYZER_INSTRUCTIONS` - veja [Módulo 3](03-configure-agents.md) |
| Score de ajuste é 0 ou ausente | MatchingAgent não recebeu dados a montante | Verifique se `add_edge(resume_parser, matching_agent)` e `add_edge(jd_agent, matching_agent)` existem |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Servidor MCP rejeitou a chamada da ferramenta | Verifique a conexão com a internet. Tente abrir `https://learn.microsoft.com/api/mcp` no navegador. Tente novamente |
| Nenhuma URL Microsoft Learn na saída | Ferramenta MCP não registrada ou endpoint incorreto | Verifique `tools=[search_microsoft_learn_for_plan]` no GapAnalyzer e `MICROSOFT_LEARN_MCP_ENDPOINT` está correto |
| `Address already in use: port 8088` | Outro processo está usando a porta 8088 | Execute `netstat -ano \| findstr :8088` (Windows) ou `lsof -i :8088` (macOS/Linux) e pare o processo conflitante |
| `Address already in use: port 5679` | Conflito na porta Debugpy | Pare outras sessões de depuração. Execute `netstat -ano \| findstr :5679` para encontrar e encerrar o processo |
| Agent Inspector não abre | Servidor não iniciado totalmente ou conflito de portas | Aguarde o log "Server running". Verifique se a porta 5679 está livre |
| `azure.identity.CredentialUnavailableError` | Não autenticado no Azure CLI | Execute `az login` e reinicie o servidor |
| `azure.core.exceptions.ResourceNotFoundError` | Implantação do modelo inexistente | Verifique se `MODEL_DEPLOYMENT_NAME` corresponde a um modelo implantado no seu projeto Foundry |
| Status do container "Failed" após implantação | Queda do container na inicialização | Verifique os logs do container na barra lateral do Foundry. Comum: variável de ambiente faltando ou erro de importação |
| Implantação fica "Pending" por > 5 minutos | Container demorando para iniciar ou limites de recursos | Aguarde até 5 minutos para multi-agente (cria 4 instâncias de agentes). Se ainda pendente, verifique os logs |
| `ValueError` do `WorkflowBuilder` | Configuração inválida do grafo | Garanta que `start_executor` está definido, `output_executors` é uma lista e não há arestas circulares |

---

## Problemas de ambiente e configuração

### Valores `.env` ausentes ou incorretos

O arquivo `.env` deve estar no diretório `PersonalCareerCopilot/` (no mesmo nível do `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Conteúdo esperado do `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Encontrando seu PROJECT_ENDPOINT:**  
- Abra a barra lateral **Microsoft Foundry** no VS Code → clique com o botão direito no seu projeto → **Copy Project Endpoint**.  
- Ou acesse o [Portal Azure](https://portal.azure.com) → seu projeto Foundry → **Overview** → **Project endpoint**.

> **Encontrando seu MODEL_DEPLOYMENT_NAME:** Na barra lateral do Foundry, expanda seu projeto → **Models** → localize o nome do modelo implantado (ex: `gpt-4.1-mini`).

### Precedência da variável de ambiente

`main.py` usa `load_dotenv(override=False)`, o que significa:

| Prioridade | Fonte | Vence se ambos estiverem definidos? |
|----------|--------|------------------------|
| 1 (mais alta) | Variável de ambiente do shell | Sim |
| 2 | Arquivo `.env` | Apenas se variáveis do shell não estiverem definidas |

Isso significa que variáveis de ambiente do runtime do Foundry (definidas via `agent.yaml`) têm precedência sobre valores do `.env` durante a implantação hospedada.

---

## Compatibilidade de versões

### Matriz de versões dos pacotes

O fluxo multi-agente exige versões específicas dos pacotes. Versões incompatíveis causam erros em tempo de execução.

| Pacote | Versão Requerida | Comando de Verificação |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | pré-lançamento mais recente | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Erros comuns de versão

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Correção: atualização para rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` não encontrado ou Inspector incompatível:**

```powershell
# Correção: instalar com a flag --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Correção: atualizar pacote mcp
pip install mcp --upgrade
```

### Verifique todas as versões de uma vez

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Saída esperada:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Problemas com a ferramenta MCP

### Ferramenta MCP retorna sem resultados

**Sintoma:** Cartões de Gap indicam "No results returned from Microsoft Learn MCP" ou "No direct Microsoft Learn results found".

**Possíveis causas:**

1. **Problema de rede** - O endpoint MCP (`https://learn.microsoft.com/api/mcp`) está inacessível.
   ```powershell
   # Testar conectividade
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Se retornar `200`, o endpoint está acessível.

2. **Consulta muito específica** - O nome da habilidade é muito nichado para a busca Microsoft Learn.  
   - Isso é esperado para habilidades muito especializadas. A ferramenta tem uma URL de fallback na resposta.

3. **Timeout da sessão MCP** - A conexão HTTP Streamable expirou.  
   - Tente novamente. Sessões MCP são efêmeras e podem precisar reconexão.

### Explicação dos logs MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Significado | Ação |
|-----|---------|--------|
| `GET → 405` | Probes do cliente MCP durante a inicialização | Normal - ignore |
| `POST → 200` | Chamada da ferramenta sucedida | Esperado |
| `DELETE → 405` | Probes do cliente MCP durante limpeza | Normal - ignore |
| `POST → 400` | Requisição inválida (query malformada) | Verifique o parâmetro `query` em `search_microsoft_learn_for_plan()` |
| `POST → 429` | Limite de taxa atingido | Aguarde e tente novamente. Reduza o parâmetro `max_results` |
| `POST → 500` | Erro no servidor MCP | Transitório - tente outra vez. Se persistir, a API MCP do Microsoft Learn pode estar indisponível |
| Timeout de conexão | Problema de rede ou servidor MCP indisponível | Verifique a internet. Tente `curl https://learn.microsoft.com/api/mcp` |

---

## Problemas de implantação

### Container falha ao iniciar após implantação

1. **Verifique os logs do container:**  
   - Abra a barra lateral **Microsoft Foundry** → expanda **Hosted Agents (Preview)** → clique no seu agente → expanda a versão → **Container Details** → **Logs**.  
   - Procure por rastreamentos de erro Python ou erros de módulo ausente.

2. **Falhas comuns na inicialização do container:**

   | Erro nos logs | Causa | Correção |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` falta algum pacote | Adicione o pacote, reimplante |
   | `RuntimeError: Missing required environment variable` | Variáveis env em `agent.yaml` não configuradas | Atualize a seção `environment_variables` em `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Identidade Gerenciada não configurada | Foundry configura automaticamente - certifique-se de implantar via extensão |
   | `OSError: port 8088 already in use` | Dockerfile expõe porta errada ou conflito de porta | Verifique `EXPOSE 8088` no Dockerfile e `CMD ["python", "main.py"]` |
   | Container sai com código 1 | Exceção não tratada em `main()` | Teste localmente primeiro ([Módulo 5](05-test-locally.md)) para capturar erros antes de implantar |

3. **Reimplante após corrigir:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → selecione o mesmo agente → implante nova versão.

### Implantação demora muito

Containers multi-agente demoram mais para iniciar porque criam 4 instâncias de agentes ao iniciar. Tempos normais:

| Etapa | Duração Esperada |
|-------|------------------|
| Construção da imagem do container | 1-3 minutos |
| Push da imagem para ACR | 30-60 segundos |
| Inicialização do container (agente único) | 15-30 segundos |
| Inicialização do container (multi-agente) | 30-120 segundos |
| Agente disponível no Playground | 1-2 minutos após "Started" |

> Se o status "Pending" persistir por mais de 5 minutos, verifique os logs do container para erros.

---

## Problemas de RBAC e permissões

### `403 Forbidden` ou `AuthorizationFailed`

Você precisa do papel **[Azure AI User](https://aka.ms/foundry-ext-project-role)** no seu projeto Foundry:

1. Vá ao [Portal Azure](https://portal.azure.com) → recurso **projeto** Foundry.
2. Clique em **Controle de acesso (IAM)** → **Atribuições de função**.
3. Pesquise seu nome → confirme que **Azure AI User** está listado.
4. Se ausente: **Adicionar** → **Adicionar atribuição de função** → pesquise **Azure AI User** → atribua à sua conta.

Consulte a documentação [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para detalhes.

### Implantação do modelo inacessível

Se o agente retorna erros relacionados ao modelo:

1. Verifique que o modelo está implantado: barra lateral Foundry → expanda projeto → **Models** → confira `gpt-4.1-mini` (ou seu modelo) com status **Succeeded**.  
2. Verifique se o nome da implantação corresponde: compare `MODEL_DEPLOYMENT_NAME` no `.env` (ou `agent.yaml`) com o nome real da implantação na barra lateral.  
3. Se a implantação expirou (camada gratuita): reimplante a partir do [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problemas com o Agent Inspector

### Inspector abre mas mostra "Disconnected"

1. Verifique se o servidor está rodando: procure por "Server running on http://localhost:8088" no terminal.  
2. Verifique a porta `5679`: Inspector conecta via debugpy na porta 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Reinicie o servidor e reabra o Inspector.

### Inspector mostra resposta parcial

Respostas multi-agente são longas e transmitidas incrementalmente. Aguarde a resposta completa (pode levar 30-60 segundos dependendo do número de cartões Gap e chamadas da ferramenta MCP).

Se a resposta for consistentemente truncada:  
- Verifique se as instruções do GapAnalyzer contêm o bloco `CRITICAL:` que impede a combinação dos cartões de gap.  
- Verifique o limite de tokens do seu modelo - `gpt-4.1-mini` suporta até 32K tokens de saída, o que deve ser suficiente.

---

## Dicas de desempenho

### Respostas lentas

Fluxos multi-agente são inerentemente mais lentos que single-agent devido a dependências sequenciais e chamadas da ferramenta MCP.

| Otimização | Como | Impacto |
|-------------|-----|--------|
| Reduzir chamadas MCP | Diminuir o parâmetro `max_results` da ferramenta | Menos requisições HTTP |
| Simplificar instruções | Prompts do agente mais curtos e focados | Inferência LLM mais rápida |
| Utilizar `gpt-4.1-mini` | Mais rápido que `gpt-4.1` para desenvolvimento | Aproximadamente 2x mais rápido |
| Reduzir detalhe dos cartões de gap | Simplificar o formato dos cartões nas instruções do GapAnalyzer | Menos saída para gerar |

### Tempos típicos de resposta (local)

| Configuração | Tempo esperado |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 cartões de gap | 30-60 segundos |
| `gpt-4.1-mini`, 8+ cartões de gap | 60-120 segundos |
| `gpt-4.1`, 3-5 cartões de gap | 60-120 segundos |
---

## Obtendo ajuda

Se você estiver preso depois de tentar as correções acima:

1. **Verifique os logs do servidor** - A maioria dos erros produz um rastreamento de pilha Python no terminal. Leia o rastreamento completo.
2. **Pesquise a mensagem de erro** - Copie o texto do erro e pesquise no [Microsoft Q&A para Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Abra um problema** - Registre um problema no [repositório do workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) com:
   - A mensagem de erro ou captura de tela
   - Suas versões dos pacotes (`pip list | Select-String "agent-framework"`)
   - Sua versão do Python (`python --version`)
   - Se o problema é local ou após a implantação

---

### Checklist

- [ ] Você pode identificar e corrigir os erros mais comuns de multiagentes usando a tabela de referência rápida
- [ ] Você sabe como verificar e corrigir problemas de configuração do `.env`
- [ ] Você pode verificar se as versões dos pacotes correspondem à matriz requerida
- [ ] Você entende as entradas de log do MCP e pode diagnosticar falhas de ferramentas
- [ ] Você sabe como verificar os logs do contêiner para falhas de implantação
- [ ] Você pode verificar os papéis RBAC no Portal Azure

---

**Anterior:** [07 - Verificar no Playground](07-verify-in-playground.md) · **Início:** [Lab 02 README](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->