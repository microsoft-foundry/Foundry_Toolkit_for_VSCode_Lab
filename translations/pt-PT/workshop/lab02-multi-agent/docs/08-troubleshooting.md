# Módulo 8 - Resolução de Problemas

Este módulo cobre erros comuns, correções e estratégias de depuração específicas do fluxo de trabalho multi-agente.

## Problemas de output do Agente

### GapAnalyzer diz “Ainda não tenho o relatório de matching”

**Sintoma:** A resposta do GapAnalyzer pede para colar um relatório de matching com “Skills em Falta” e “Lacunas de Certificação”. Isto acontece mesmo quando enviou tanto um currículo como uma descrição de trabalho.

**Causa:** O texto da JD não foi passado para o agente JD. Com `context_mode="last_agent"`, o `resume_executor` é o único executor que vê a mensagem original do utilizador. Se as `RESUME_PARSER_INSTRUCTIONS` não incluem o texto da JD na sua saída, o agente JD não tem JD para analisar, o MatchingAgent não pode calcular uma pontuação de ajuste, e o GapAnalyzer recebe uma entrada sem sentido.

**Diagnóstico:**

Nos logs do servidor, procure a span do MatchingAgent. Se contiver:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
o passthrough está em falta ou está partido.

**Correção:** Confirme que `RESUME_PARSER_INSTRUCTIONS` em `main.py` contém uma secção `[JOB DESCRIPTION PASS-THROUGH]` e a regra:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Confirme também que `JOB_DESCRIPTION_INSTRUCTIONS` contém uma regra de retransmissão `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Se algum dos blocos de instruções for um stub do assistente scaffolding, substitua-o pela versão completa do [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent mostra “Cannot compute fit score - no JD provided”

Esta é a mesma causa raiz que acima. O MatchingAgent recebeu a saída do agente JD mas a secção `[PARSED RESUME PASS-THROUGH]` estava em falta ou vazia, por isso não pôde comparar os dois perfis. Confirme:
1. Que `JOB_DESCRIPTION_INSTRUCTIONS` inclui a regra: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. Que `MATCHING_AGENT_INSTRUCTIONS` diz ao agente para procurar as secções `[JD REQUIREMENTS]` e `[PARSED RESUME PASS-THROUGH]`.

Substitua ambos os blocos de instruções pelas versões completas do [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### A resposta aparece duas vezes

**Sintoma:** A saída do GapAnalyzer (ou a saída completa do pipeline) aparece duas vezes na resposta do Agent Inspector.

**Causa:** `WorkflowBuilder` usa semântica OR para as arestas de entrada - um executor downstream dispara assim que qualquer predecessor termina. Se `matching_executor` tem duas arestas de entrada (uma do `resume_executor` e outra do `jd_executor`), dispara duas vezes: uma vez quando o ResumeParser termina e outra vez quando o agente JD termina. O GapAnalyzer também corre duas vezes.

**Correção:** Assegure que o grafo `WorkflowBuilder` é uma pipeline estritamente sequencial sem fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NÃO proveniente do resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Se tiver uma linha solta `.add_edge(resume_executor, matching_executor)`, remova-a. O relay `[PARSED RESUME PASS-THROUGH]` na saída do agente JD já dá ao MatchingAgent acesso ao currículo.

---

## Problemas de ambiente e configuração

### Valores `.env` em falta ou errados

O ficheiro `.env` deve estar no diretório `PersonalCareerCopilot/` (mesmo nível que `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Conteúdo esperado do `.env`:

**Caminho A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Caminho B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Ambos os caminhos usam `FOUNDRY_PROJECT_ENDPOINT`. O valor difere: cloud usa um endpoint Foundry `https://`; local usa `http://localhost:5273/v1`. Corra `foundry model list` para confirmar o alias exato do modelo para o Caminho B.

> **Como encontrar o seu `FOUNDRY_PROJECT_ENDPOINT`:** 
- Abra a barra lateral do **Foundry Toolkit** no VS Code → clique com o botão direito no seu projeto → **Copy Project Endpoint**. 
- Ou vá a [Azure Portal](https://portal.azure.com) → seu projeto Foundry → **Overview** → **Project endpoint**.

> **Como encontrar o seu `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Na barra lateral do Foundry Toolkit, expanda seu projeto → **Models** → encontre o nome do modelo implementado (ex.: `gpt-4.1-mini`).

### Prioridade das variáveis de ambiente

`main.py` usa `load_dotenv(override=True)`, o que significa:

| Prioridade | Fonte | Vence se ambos definidos? |
|----------|--------|------------------------|
| 1 (mais alto) | Ficheiro `.env` | Sim |
| 2 | Variável de ambiente do shell/conteiner | Usada se a mesma chave não estiver em `.env` |

No desenvolvimento local, isto faz com que `.env` seja a fonte de verdade (editar `.env` afeta imediatamente as execuções). No deployment alojado, Foundry injeta variáveis de ambiente ao nível do container; como `.env` não faz parte da imagem deployada para este laboratório, usam-se os valores injetados no container.

---

## Compatibilidade de versões

### Matriz de versões dos pacotes

O fluxo de trabalho multi-agente requer versões específicas dos pacotes. Versões incompatíveis causam erros em runtime.

| Pacote | Versão Obrigatória | Comando para Verificar |
|---------|-----------------|---------------|
| `agent-framework-foundry` | última | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | última | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | última | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Erros comuns de versão

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Correção: reinstalar agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Correção: atualizar o pacote mcp
pip install mcp --upgrade
```

### Verificar todas as versões de uma vez

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Saída esperada:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problemas de deployment

### Container não arranca depois do deployment

1. **Verifique os logs do container:**
   - Abra a barra lateral do **Foundry Toolkit** → expanda **Hosted Agents (Preview)** → clique no seu agente → expanda a versão → **Container Details** → **Logs**.
   - Procure por traces de stack Python ou erros de módulos em falta.

2. **Falhanços comuns no arranque do container:**

   | Erro nos logs | Causa | Correção |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` está sem um pacote | Adicione o pacote e redeploy |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variáveis de ambiente `agent.yaml` ou `.env` não definidas | Atualize `agent.yaml` → secção `environment_variables` (alojado) ou `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity não configurada | Foundry configura isto automaticamente - assegure-se que está a deployar pela extensão |
   | `OSError: port 8088 already in use` | Dockerfile expõe a porta errada ou conflito de portas | Verifique `EXPOSE 8088` no Dockerfile e `CMD ["python", "main.py"]` |
   | Container sai com código 1 | Exceção não tratada em `main()` | Teste localmente primeiro ([Módulo 5](05-test-locally.md)) para apanhar erros antes de deployar |

3. **Volte a deployar depois de corrigir:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → selecione o mesmo agente → deploy de uma nova versão.

### Deployment demora demasiado tempo

Containers multi-agente demoram mais a arrancar porque criam 4 instâncias de agentes no arranque. Tempos normais de arranque:

| Etapa | Duração Esperada |
|-------|------------------|
| Build da imagem do container | 1-3 minutos |
| Push da imagem para ACR | 30-60 segundos |
| Arranque do container (agente único) | 15-30 segundos |
| Arranque do container (multi-agente) | 30-120 segundos |
| Agente disponível no Playground | 1-2 minutos após "Started" |

> Se o estado "Pending" persistir além de 5 minutos, verifique os logs do container para erros.

---

## Problemas de RBAC e permissões

### `403 Forbidden` ou `AuthorizationFailed`

Necessita do papel **[Foundry User](https://aka.ms/foundry-ext-project-role)** no seu projeto Foundry (anteriormente chamado **Azure AI User** - o ID do papel não mudou):

1. Vá a [Azure Portal](https://portal.azure.com) → o recurso do seu projeto Foundry.
2. Clique em **Access control (IAM)** → **Role assignments**.
3. Procure pelo seu nome → confirme que o papel **Foundry User** (ou o rótulo antigo **Azure AI User**) está listado.
4. Se faltar: **Add** → **Add role assignment** → procure **Foundry User** → atribua à sua conta.

Veja a documentação [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para detalhes.

### Deploy do modelo inacessível

Se o agente devolver erros relacionados com o modelo:

1. Verifique se o modelo está deployado: barra lateral Foundry → expanda projeto → **Models** → verifique `gpt-4.1-mini` (ou seu modelo) com estado **Succeeded**.
2. Verifique se o nome do deployment corresponde: compare `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` (ou em `agent.yaml`) com o nome real do deployment na barra lateral.
3. Se o deployment expirou (free tier): redeploy a partir do [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemas Foundry Local (Caminho B)

### Serviço Foundry Local não a correr

```powershell
# Verificar estado
foundry local status

# Iniciar o serviço se estiver parado
foundry local start
```

| Sintoma | Causa | Correção |
|---------|-------|-----|
| Health check retorna `503` | Serviço não iniciado | `foundry local start` ou clique em **Start** na barra lateral Foundry Toolkit |
| Health check expira | Modelo ainda a carregar | Espere 30–60 s após iniciar; modelos maiores demoram mais |
| `StatusCode: 404` em `/v1/health` | Porta errada | O padrão é `5273`. Verifique `foundry local status` para a porta real |
| Recursos insuficientes | Foundry Local precisa de ~4 GB RAM livres | Feche outras aplicações |
| Falha no download do modelo | Espaço em disco baixo | Modelos têm 2–8 GB. Libere espaço, depois `foundry model pull <name>` |

### Incompatibilidade do nome do modelo

```powershell
# Listar modelos descarregados e os seus pseudónimos exactos
foundry model list
```

Defina `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` exatamente como o alias mostrado (ex.: `phi-4-mini`, não `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ao correr localmente (Caminho B)

O `main.py` do laboratório usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local exige que esta variável aponte para o serviço local - **não** para `AZURE_AI_PROJECT_ENDPOINT`. Assegure que o seu `.env` contém:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### A ferramenta MCP ainda faz uma chamada externa (Caminho B)

Isto é esperado. A ferramenta `search_microsoft_learn_for_plan` obtém recursos de aprendizagem de `https://learn.microsoft.com/api/mcp`. **Só a consulta do nome da skill** viaja pela rede - currículo e texto da JD são totalmente processados no seu dispositivo e nunca transmitidos. Se for necessária operação completamente offline, adicione um fallback try/except na ferramenta que retorna uma URL estática do `learn.microsoft.com` quando o endpoint não está acessível.

---

## Obtenção de ajuda

Se ficar bloqueado depois de tentar as correções acima:

1. **Verifique os logs do servidor** - A maioria dos erros produz um traceback Python no terminal. Leia todo o traceback.
2. **Pesquise a mensagem de erro** - Copie o texto do erro e pesquise em [Microsoft Q&A para Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Abra um issue** - Crie um issue no [repositório do workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) incluindo:
   - A mensagem de erro ou screenshot
   - As versões dos seus pacotes (`pip list | Select-String "agent-framework"`)
   - A sua versão do Python (`python --version`)
   - Se o problema é local ou após deploy

---

### Checkpoint

- [ ] Sabe como verificar e corrigir problemas de configuração `.env`
- [ ] Pode verificar se as versões dos pacotes correspondem à matriz exigida
- [ ] Sabe como verificar os logs do container para falhas no deployment
- [ ] Pode verificar as roles RBAC no Portal Azure

---

**Anterior:** [07 - Verificar no Playground](07-verify-in-playground.md) · **Seguinte:** [09 - Sumário →](09-summary.md) · **Início:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->