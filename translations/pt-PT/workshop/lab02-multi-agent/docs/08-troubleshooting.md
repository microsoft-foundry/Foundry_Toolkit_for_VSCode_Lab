# Módulo 8 - Resolução de problemas (Multi-Agente)

Este módulo cobre erros comuns, correções e estratégias de depuração específicas para o fluxo de trabalho multi-agente. Para problemas gerais de implantação no Foundry, consulte também o [guia de resolução de problemas do Laboratório 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Referência rápida: Erro → Correção

| Erro / Sintoma | Causa provável | Correção |
|----------------|---------------|----------|
| `RuntimeError: Missing required environment variable(s)` | Ficheiro `.env` em falta ou valores não definidos | Criar `.env` com `PROJECT_ENDPOINT=<your-endpoint>` e `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Ambiente virtual não ativado ou dependências não instaladas | Executar `.\.venv\Scripts\Activate.ps1` seguido de `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Pacote MCP não instalado (em falta em requirements) | Executar `pip install mcp` ou verificar se `requirements.txt` o inclui como dependência transitiva |
| O agente inicia mas devolve resposta vazia | Discordância em `output_executors` ou arestas em falta | Verificar `output_executors=[gap_analyzer]` e se todas as arestas existem em `create_workflow()` |
| Apenas 1 carta de gap (restantes em falta) | Instruções do GapAnalyzer incompletas | Adicionar o parágrafo `CRITICAL:` a `GAP_ANALYZER_INSTRUCTIONS` - ver [Módulo 3](03-configure-agents.md) |
| Pontuação Fit é 0 ou ausente | MatchingAgent não recebeu dados ascendentes | Verificar que existem `add_edge(resume_parser, matching_agent)` e `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Servidor MCP rejeitou a chamada da ferramenta | Verificar conectividade à Internet. Tentar abrir `https://learn.microsoft.com/api/mcp` no navegador. Tentar novamente |
| Nenhum URL da Microsoft Learn na saída | Ferramenta MCP não registada ou endpoint incorreto | Confirmar `tools=[search_microsoft_learn_for_plan]` no GapAnalyzer e se `MICROSOFT_LEARN_MCP_ENDPOINT` está correto |
| `Address already in use: port 8088` | Outro processo está a usar a porta 8088 | Executar `netstat -ano \| findstr :8088` (Windows) ou `lsof -i :8088` (macOS/Linux) e terminar processo conflitante |
| `Address already in use: port 5679` | Conflito na porta Debugpy | Parar outras sessões de depuração. Executar `netstat -ano \| findstr :5679` para identificar e matar o processo |
| Inspector do Agente não abre | Servidor não iniciou completamente ou conflito de portas | Aguardar log "Server running". Verificar se a porta 5679 está livre |
| `azure.identity.CredentialUnavailableError` | Não autenticado no Azure CLI | Executar `az login` e reiniciar o servidor |
| `azure.core.exceptions.ResourceNotFoundError` | Implantação do modelo não existe | Verificar se `MODEL_DEPLOYMENT_NAME` corresponde a um modelo implantado no seu projeto Foundry |
| Estado do container "Failed" após implantação | Container falha ao iniciar | Verificar logs do container na barra lateral do Foundry. Comum: variável de ambiente em falta ou erro de importação |
| Implantação mostra "Pending" > 5 minutos | Container demora demasiado a iniciar ou limites de recursos | Aguardar até 5 minutos para multi-agente (cria 4 instâncias). Se persistir, verificar logs |
| `ValueError` do `WorkflowBuilder` | Configuração inválida do grafo | Garantir que `start_executor` está definido, `output_executors` é lista e não existem arestas circulares |

---

## Problemas com ambiente e configuração

### Valores `.env` em falta ou incorretos

O ficheiro `.env` deve estar na diretoria `PersonalCareerCopilot/` (ao mesmo nível que `main.py`):

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

> **Como encontrar o seu PROJECT_ENDPOINT:**
- Abra a barra lateral **Microsoft Foundry** no VS Code → clique com o botão direito no seu projeto → **Copy Project Endpoint**.
- Ou aceda ao [Azure Portal](https://portal.azure.com) → projeto Foundry → **Overview** → **Project endpoint**.

> **Como encontrar o seu MODEL_DEPLOYMENT_NAME:** Na barra lateral do Foundry, expanda o seu projeto → **Models** → encontre o nome do modelo implantado (ex: `gpt-4.1-mini`).

### Precedência das variáveis de ambiente

`main.py` usa `load_dotenv(override=False)`, o que significa:

| Prioridade | Fonte | Vence se ambas definidas? |
|------------|-------|--------------------------|
| 1 (mais alta) | Variável de ambiente do shell | Sim |
| 2 | Ficheiro `.env` | Apenas se a variável shell não estiver definida |

Isto significa que as variáveis ambientes do runtime Foundry (definidas via `agent.yaml`) têm precedência sobre os valores `.env` durante a implantação hospedada.

---

## Compatibilidade de versões

### Matriz de versões dos pacotes

O fluxo multi-agente requer versões específicas dos pacotes. Versões incompatíveis causam erros em runtime.

| Pacote | Versão requerida | Comando de verificação |
|--------|------------------|-----------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | versão pré-lançamento mais recente | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Erros comuns de versão

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Correção: atualizar para rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` não encontrado ou Inspector incompatível:**

```powershell
# Correção: instalar com a flag --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Correção: atualizar o pacote mcp
pip install mcp --upgrade
```

### Verificar todas as versões de uma vez

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

### A ferramenta MCP não retorna resultados

**Sintoma:** As cartas de gap indicam "No results returned from Microsoft Learn MCP" ou "No direct Microsoft Learn results found".

**Possíveis causas:**

1. **Problema de rede** - O endpoint MCP (`https://learn.microsoft.com/api/mcp`) está inacessível.
   ```powershell
   # Testar a conectividade
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Se isto retornar `200`, o endpoint está acessível.

2. **Consulta demasiado específica** - O nome da competência é muito específico para a pesquisa da Microsoft Learn.
   - Isto é esperado para competências muito especializadas. A ferramenta devolve uma URL alternativa na resposta.

3. **Timeout da sessão MCP** - A ligação HTTP Streamable expirou.
   - Tente novamente a requisição. As sessões MCP são efémeras e podem necessitar de reconexão.

### Logs do MCP explicados

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Significado | Ação |
|-----|------------|-------|
| `GET → 405` | Provas do cliente MCP durante inicialização | Normal - ignore |
| `POST → 200` | Chamada da ferramenta bem-sucedida | Esperado |
| `DELETE → 405` | Provas do cliente MCP durante limpeza | Normal - ignore |
| `POST → 400` | Pedido inválido (query malformada) | Verificar parâmetro `query` em `search_microsoft_learn_for_plan()` |
| `POST → 429` | Limite de taxa atingido | Aguarde e tente novamente. Reduzir parâmetro `max_results` |
| `POST → 500` | Erro no servidor MCP | Transitório - tentar de novo. Se persistir, a API MCP da Microsoft Learn poderá estar indisponível |
| Timeout de ligação | Problema de rede ou servidor MCP indisponível | Verificar internet. Tentar `curl https://learn.microsoft.com/api/mcp` |

---

## Problemas de implantação

### O container não inicia após implantação

1. **Verificar os logs do container:**
   - Abra a barra lateral **Microsoft Foundry** → expanda **Hosted Agents (Preview)** → clique no seu agente → expanda a versão → **Container Details** → **Logs**.
   - Procure por rastreamentos de exceções Python ou erros de módulo em falta.

2. **Falhas comuns na inicialização do container:**

   | Erro nos logs | Causa | Correção |
   |---------------|-------|----------|
   | `ModuleNotFoundError` | Pacote em falta em `requirements.txt` | Adicionar o pacote, redesplegar |
   | `RuntimeError: Missing required environment variable` | Variáveis de ambiente em `agent.yaml` não definidas | Atualizar a secção `environment_variables` de `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Identidade gerida não configurada | Foundry configura automaticamente - garantir implantação via extensão |
   | `OSError: port 8088 already in use` | Dockerfile expõe porta errada ou conflito de portas | Confirmar `EXPOSE 8088` no Dockerfile e `CMD ["python", "main.py"]` |
   | Container termina com código 1 | Exceção não tratada em `main()` | Testar localmente primeiro ([Módulo 5](05-test-locally.md)) para apanhar erros antes da implantação |

3. **Redesplegar após correção:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → selecionar o mesmo agente → implantar nova versão.

### Implantação demora demasiado

Os containers multi-agente demoram mais a iniciar porque criam 4 instâncias de agente ao arrancar. Tempos normais de arranque:

| Etapa | Duração esperada |
|-------|------------------|
| Construção da imagem do container | 1-3 minutos |
| Push da imagem para ACR | 30-60 segundos |
| Arranque do container (agente único) | 15-30 segundos |
| Arranque do container (multi-agente) | 30-120 segundos |
| Agente disponível no Playground | 1-2 minutos após "Started" |

> Se o estado "Pending" persistir mais de 5 minutos, verificar logs do container para erros.

---

## Problemas RBAC e permissões

### `403 Forbidden` ou `AuthorizationFailed`

Necessita do papel **[Azure AI User](https://aka.ms/foundry-ext-project-role)** no seu projeto Foundry:

1. Vá ao [Azure Portal](https://portal.azure.com) → recurso do seu projeto Foundry.
2. Clique em **Access control (IAM)** → **Role assignments**.
3. Pesquise pelo seu nome → confirme se tem o papel **Azure AI User** listado.
4. Se faltar: **Add** → **Add role assignment** → procure **Azure AI User** → atribua à sua conta.

Consulte a documentação [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para mais detalhes.

### Implantação do modelo inacessível

Se o agente retorna erros relacionados com o modelo:

1. Verifique se o modelo está implantado: barra lateral do Foundry → expandir projeto → **Models** → confirmar se `gpt-4.1-mini` (ou seu modelo) está com estado **Succeeded**.
2. Verifique se o nome da implantação corresponde: comparar `MODEL_DEPLOYMENT_NAME` no `.env` (ou `agent.yaml`) com o nome real da implantação na barra lateral.
3. Se a implantação expirou (nível gratuito): redesplegar a partir do [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problemas com o Agent Inspector

### Inspector abre mas mostra "Disconnected"

1. Verifique se o servidor está a correr: procure "Server running on http://localhost:8088" no terminal.
2. Verifique a porta `5679`: o Inspector conecta via debugpy nessa porta.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Reinicie o servidor e reabra o Inspector.

### Inspector mostra resposta parcial

As respostas multi-agente são longas e são transmitidas incrementalmente. Aguarde a resposta completa (pode levar 30-60 segundos dependendo do número de cartas de gap e chamadas MCP).

Se a resposta for consistentemente truncada:
- Verifique se as instruções do GapAnalyzer têm o bloco `CRITICAL:` que impede combinar cartas de gap.
- Verifique o limite de tokens do seu modelo - `gpt-4.1-mini` suporta até 32K tokens de saída, o que deve ser suficiente.

---

## Dicas de desempenho

### Respostas lentas

Fluxos multi-agente são inerentemente mais lentos que agentes únicos devido a dependências sequenciais e chamadas MCP.

| Otimização | Como | Impacto |
|------------|------|---------|
| Reduzir chamadas MCP | Diminuir o parâmetro `max_results` na ferramenta | Menos idas e voltas HTTP |
| Simplificar instruções | Prompts do agente mais curtos e focados | Inferência LLM mais rápida |
| Usar `gpt-4.1-mini` | Mais rápido que `gpt-4.1` para desenvolvimento | Aproximadamente 2x mais rápido |
| Reduzir detalhe nas cartas de gap | Simplificar formato das cartas no GapAnalyzer | Menos saída a gerar |

### Tempos típicos de resposta (local)

| Configuração | Tempo esperado |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 cartas de gap | 30-60 segundos |
| `gpt-4.1-mini`, 8+ cartas de gap | 60-120 segundos |
| `gpt-4.1`, 3-5 cartas de gap | 60-120 segundos |
---

## Obter ajuda

Se ficar bloqueado após tentar as correções acima:

1. **Verifique os logs do servidor** - A maioria dos erros produz um rastreio da pilha Python no terminal. Leia o rastreio completo.
2. **Pesquise a mensagem de erro** - Copie o texto do erro e pesquise no [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Abra um problema** - Crie um problema no [repositório do workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) com:
   - A mensagem de erro ou captura de ecrã
   - As versões dos seus pacotes (`pip list | Select-String "agent-framework"`)
   - A sua versão do Python (`python --version`)
   - Se o problema é local ou após o deploy

---

### Lista de verificação

- [ ] Consegue identificar e corrigir os erros mais comuns de multi-agentes usando a tabela de referência rápida
- [ ] Sabe como verificar e corrigir problemas de configuração do `.env`
- [ ] Consegue verificar se as versões dos pacotes correspondem à matriz exigida
- [ ] Compreende as entradas do log MCP e consegue diagnosticar falhas nas ferramentas
- [ ] Sabe como verificar os logs dos contentores para falhas no deploy
- [ ] Consegue verificar os papéis RBAC no Portal Azure

---

**Anterior:** [07 - Verificar no Playground](07-verify-in-playground.md) · **Início:** [Lab 02 README](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, por favor tenha em conta que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autoritativa. Para informações críticas, a tradução profissional humana é recomendada. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->