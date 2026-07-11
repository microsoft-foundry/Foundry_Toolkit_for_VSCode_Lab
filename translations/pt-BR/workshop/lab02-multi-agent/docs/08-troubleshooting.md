# Módulo 8 - Solução de Problemas

Este módulo cobre erros comuns, correções e estratégias de depuração específicas para o fluxo de trabalho multiagente.

## Problemas de saída do agente

### GapAnalyzer diz “Ainda não tenho o relatório de correspondência”

**Sintoma:** A resposta do GapAnalyzer pede para você colar um relatório de correspondência com “Habilidades Faltantes” e “Lacunas de Certificação.” Isso acontece mesmo quando você enviou tanto um currículo quanto uma descrição de trabalho.

**Causa:** O texto da descrição do trabalho (JD) não foi passado para o agente JD. Com `context_mode="last_agent"`, `resume_executor` é o único executor que vê a mensagem original do usuário. Se `RESUME_PARSER_INSTRUCTIONS` não inclui o texto do JD na sua saída, o agente JD não tem JD para analisar, o MatchingAgent não pode calcular o score de adequação, e o GapAnalyzer recebe uma entrada sem sentido.

**Diagnóstico:**

Nos logs do servidor, procure pelo span do MatchingAgent. Se contiver:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
a passagem está faltando ou quebrada.

**Correção:** Confirme que `RESUME_PARSER_INSTRUCTIONS` em `main.py` contém uma seção `[JOB DESCRIPTION PASS-THROUGH]` e a regra:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Também confirme que `JOB_DESCRIPTION_INSTRUCTIONS` contém uma regra de retransmissão `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Se qualquer bloco de instruções for um stub do assistente de scaffold, substitua-o pela versão completa de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent exibe “Cannot compute fit score - no JD provided”

Esta é a mesma causa raiz acima. MatchingAgent recebeu a saída do agente JD, mas a seção `[PARSED RESUME PASS-THROUGH]` estava ausente ou vazia, então não pôde comparar os dois perfis. Confirme:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inclui a regra de retransmissão: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` indica ao agente para procurar pelas seções `[JD REQUIREMENTS]` e `[PARSED RESUME PASS-THROUGH]`.

Substitua ambos os blocos de instruções pelas versões completas de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### A resposta aparece duas vezes

**Sintoma:** A saída do GapAnalyzer (ou a saída inteira do pipeline) aparece duas vezes na resposta do Agent Inspector.

**Causa:** `WorkflowBuilder` usa semântica OR para as arestas de entrada - um executor a jusante dispara assim que **qualquer** predecessor termina. Se `matching_executor` tem duas arestas de entrada (uma do `resume_executor` e outra do `jd_executor`), ele dispara duas vezes: uma quando o ResumeParser termina e outra quando o agente JD termina. O GapAnalyzer então também executa duas vezes.

**Correção:** Garanta que o grafo `WorkflowBuilder` seja um pipeline estritamente sequencial sem fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NÃO do resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Se você tiver uma linha `.add_edge(resume_executor, matching_executor)` sobrando, remova-a. O retransmissor `[PARSED RESUME PASS-THROUGH]` na saída do agente JD já dá ao MatchingAgent acesso ao currículo.

---

## Problemas de ambiente e configuração

### Valores `.env` ausentes ou errados

O arquivo `.env` deve estar no diretório `PersonalCareerCopilot/` (nível igual a `main.py`):

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

> Ambos os caminhos usam `FOUNDRY_PROJECT_ENDPOINT`. O valor difere: o cloud usa um endpoint Foundry `https://`; local usa `http://localhost:5273/v1`. Execute `foundry model list` para confirmar o alias exato do modelo para o Caminho B.

> **Encontrando seu `FOUNDRY_PROJECT_ENDPOINT`:** 
- Abra a barra lateral do **Foundry Toolkit** no VS Code → clique com o botão direito no seu projeto → **Copy Project Endpoint**. 
- Ou vá para [Azure Portal](https://portal.azure.com) → seu projeto Foundry → **Overview** → **Project endpoint**.

> **Encontrando seu `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Na barra lateral do Foundry Toolkit, expanda seu projeto → **Models** → encontre o nome do modelo implantado (ex.: `gpt-4.1-mini`).

### Precedência de variável de ambiente

`main.py` usa `load_dotenv(override=True)`, o que significa:

| Prioridade | Fonte | Ganha quando ambos estão definidos? |
|----------|--------|------------------------------|
| 1 (mais alta) | arquivo `.env` | Sim |
| 2 | Variável de ambiente do shell/container | Usado quando a mesma chave não está presente no `.env` |

No desenvolvimento local, isso faz do `.env` a fonte da verdade (editar `.env` afeta imediatamente as execuções). Na implantação hospedada, o Foundry injeta variáveis de ambiente no nível do container; como `.env` não faz parte da imagem implantada para esta configuração do laboratório, os valores injetados no container são usados.

---

## Compatibilidade de versões

### Matriz de versões de pacotes

O fluxo multiagente requer versões específicas de pacotes. Versões incompatíveis causam erros de tempo de execução.

| Pacote | Versão requerida | Comando para checar |
|---------|-----------------|---------------------|
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

### Verifique todas as versões de uma vez

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

## Problemas de implantação

### Container falha ao iniciar após implantação

1. **Verifique os logs do container:**
   - Abra a barra lateral do **Foundry Toolkit** → expanda **Hosted Agents (Preview)** → clique no seu agente → expanda a versão → **Container Details** → **Logs**.
   - Procure por rastreamentos de stack Python ou erros de módulo ausente.

2. **Falhas comuns na inicialização do container:**

   | Erro nos logs | Causa | Correção |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` não tem um pacote | Adicione o pacote, reimplante |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variáveis de ambiente em `agent.yaml` ou `.env` não definidas | Atualize a seção `environment_variables` em `agent.yaml` (hospedado) ou `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Identidade gerenciada não configurada | Foundry configura automaticamente - garanta que implante via extensão |
   | `OSError: port 8088 already in use` | Dockerfile expõe porta errada ou conflito de porta | Verifique `EXPOSE 8088` no Dockerfile e `CMD ["python", "main.py"]` |
   | Container sai com código 1 | Exceção não tratada em `main()` | Teste localmente primeiro ([Módulo 5](05-test-locally.md)) para capturar erros antes de implantar |

3. **Reimplante após correção:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → selecione o mesmo agente → implante uma nova versão.

### Implantação demora muito

Containers multiagentes demoram mais para iniciar porque criam 4 instâncias de agente na inicialização. Tempos normais de inicialização:

| Etapa | Duração esperada |
|-------|------------------|
| Build da imagem do container | 1-3 minutos |
| Push da imagem para ACR | 30-60 segundos |
| Inicialização do container (agente único) | 15-30 segundos |
| Inicialização do container (multiagente) | 30-120 segundos |
| Agente disponível no Playground | 1-2 minutos após "Started" |

> Se o status "Pending" persistir por mais de 5 minutos, verifique os logs do container para erros.

---

## Problemas de RBAC e permissões

### `403 Forbidden` ou `AuthorizationFailed`

Você precisa do papel **[Foundry User](https://aka.ms/foundry-ext-project-role)** no seu projeto Foundry (anteriormente chamado **Azure AI User** - o ID do papel permanece o mesmo):

1. Vá para [Azure Portal](https://portal.azure.com) → seu recurso de projeto Foundry.
2. Clique em **Access control (IAM)** → **Role assignments**.
3. Procure seu nome → confirme que **Foundry User** (ou o rótulo legado **Azure AI User**) está listado.
4. Se estiver ausente: **Add** → **Add role assignment** → procure por **Foundry User** → atribua à sua conta.

Veja a documentação [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para detalhes.

### Implantação do modelo não acessível

Se o agente retornar erros relacionados ao modelo:

1. Verifique se o modelo está implantado: barra lateral do Foundry → expanda projeto → **Models** → confira `gpt-4.1-mini` (ou seu modelo) com status **Succeeded**.
2. Verifique se o nome da implantação coincide: compare `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` (ou `agent.yaml`) com o nome real da implantação na barra lateral.
3. Se a implantação expirou (nível gratuito): reimplante a partir do [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemas Foundry Local (Caminho B)

### Serviço Foundry Local não está rodando

```powershell
# Verificar status
foundry local status

# Iniciar o serviço se estiver parado
foundry local start
```

| Sintoma | Causa | Correção |
|---------|-------|---------|
| Health check retorna `503` | Serviço não iniciado | `foundry local start` ou clique **Start** na barra lateral do Foundry Toolkit |
| Health check expira | Modelo ainda carregando | Espere 30–60 s após iniciar; modelos maiores demoram mais |
| `StatusCode: 404` em `/v1/health` | Porta errada | O padrão é `5273`. Verifique `foundry local status` para a porta atual |
| Recursos insuficientes | Foundry Local precisa de ~4 GB RAM livres | Feche outros aplicativos |
| Falha no download do modelo | Espaço em disco baixo | Modelos têm 2–8 GB. Libere espaço e execute `foundry model pull <name>` |

### Nome do modelo incompatível

```powershell
# Liste modelos baixados e seus aliases exatos
foundry model list
```

Defina `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` para o alias exato mostrado (ex.: `phi-4-mini`, não `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` ao rodar localmente (Caminho B)

O `main.py` do laboratório usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local requer essa variável apontando para o serviço local - **não** `AZURE_AI_PROJECT_ENDPOINT`. Garanta que seu `.env` contenha:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Ferramenta MCP ainda faz chamada externa (Caminho B)

Isto é esperado. A ferramenta `search_microsoft_learn_for_plan` busca recursos de aprendizado de `https://learn.microsoft.com/api/mcp`. **Apenas a consulta do nome da habilidade** viaja pela rede - texto do currículo e da descrição do trabalho são processados totalmente no seu dispositivo e nunca transmitidos. Se for necessário funcionamento totalmente offline, adicione um fallback `try/except` na ferramenta que retorne uma URL estática do `learn.microsoft.com` quando o endpoint estiver inacessível.

---

## Obtendo ajuda

Se você estiver preso após tentar as correções acima:

1. **Verifique os logs do servidor** - A maioria dos erros gera um rastreamento Python no terminal. Leia o traceback completo.
2. **Pesquise a mensagem de erro** - Copie o texto do erro e pesquise no [Microsoft Q&A para Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Abra um issue** - Registre um issue no [repositório do workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) com:
   - A mensagem de erro ou screenshot
   - Suas versões de pacote (`pip list | Select-String "agent-framework"`)
   - Sua versão do Python (`python --version`)
   - Se o problema é local ou após a implantação

---

### Checkpoint

- [ ] Você sabe como verificar e corrigir problemas de configuração `.env`
- [ ] Você pode verificar se as versões dos pacotes correspondem à matriz requerida
- [ ] Você sabe como checar logs do container para falhas de implantação
- [ ] Você pode verificar papéis RBAC no Azure Portal

---

**Anterior:** [07 - Verify in Playground](07-verify-in-playground.md) · **Próximo:** [09 - Summary →](09-summary.md) · **Início:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->