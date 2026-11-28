# Módulo 8 - Solução de Problemas

Este módulo cobre erros comuns, correções e estratégias de depuração específicas para o fluxo de trabalho multiagente.

## Problemas de saída do agente

### GapAnalyzer diz “Ainda não tenho o relatório correspondente”

**Sintoma:** A resposta do GapAnalyzer pede para você colar um relatório correspondente com “Habilidades Ausentes” e “Lacunas de Certificação”. Isso acontece mesmo quando você enviou tanto um currículo quanto uma descrição de trabalho.

**Causa:** O texto do JD não foi passado para o agente JD. Com `context_mode="last_agent"`, `resume_executor` é o único executor que vê a mensagem original do usuário. Se `RESUME_PARSER_INSTRUCTIONS` não incluir o texto do JD na sua saída, o agente JD não tem JD para analisar, MatchingAgent não pode calcular uma pontuação de adequação, e GapAnalyzer recebe uma entrada sem sentido.

**Diagnóstico:**

Nos logs do servidor, procure pelo span do MatchingAgent. Se ele contiver:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
o encaminhamento está faltando ou quebrado.

**Correção:** Confirme que `RESUME_PARSER_INSTRUCTIONS` em `main.py` contém uma seção `[JOB DESCRIPTION PASS-THROUGH]` e a regra:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Confirme também que `JOB_DESCRIPTION_INSTRUCTIONS` contém uma regra de retransmissão `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Se qualquer bloco de instrução for um esqueleto do assistente scaffold, substitua-o pela versão completa de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent retorna “Não é possível calcular a pontuação de ajuste - nenhum JD fornecido”

Esta é a mesma causa raiz descrita acima. MatchingAgent recebeu a saída do agente JD mas a seção `[PARSED RESUME PASS-THROUGH]` estava faltando ou vazia, então ele não pôde comparar os dois perfis. Confirme:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inclui a regra de retransmissão: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` instrui o agente a procurar pelas seções `[JD REQUIREMENTS]` e `[PARSED RESUME PASS-THROUGH]`.

Substitua ambos os blocos de instruções pelas versões completas de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### A resposta aparece duas vezes

**Sintoma:** A saída do GapAnalyzer (ou do pipeline inteiro) aparece duas vezes na resposta do Inspetor de Agentes.

**Causa:** `WorkflowBuilder` usa semântica OU para arestas de entrada – um executor a jusante dispara assim que **qualquer** predecessor conclui. Se `matching_executor` tem duas arestas de entrada (uma do `resume_executor` e outra do `jd_executor`), ele dispara duas vezes: uma vez quando ResumeParser termina e outra quando o agente JD termina. GapAnalyzer também executa duas vezes.

**Correção:** Assegure que o grafo `WorkflowBuilder` seja um pipeline estritamente sequencial sem fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Se você tiver uma linha `.add_edge(resume_executor, matching_executor)` solta, remova-a. A retransmissão `[PARSED RESUME PASS-THROUGH]` na saída do agente JD já dá ao MatchingAgent acesso ao currículo.

---

## Problemas de ambiente e configuração

### Valores `.env` ausentes ou incorretos

O arquivo `.env` deve estar no diretório `PersonalCareerCopilot/` (mesmo nível do `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Conteúdo esperado de `.env`:

**Caminho A - nuvem Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Caminho B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Ambos os caminhos usam `FOUNDRY_PROJECT_ENDPOINT`. O valor difere: nuvem usa um endpoint `https://` Foundry; local usa `http://localhost:5273/v1`. Execute `foundry model list` para confirmar o alias exato do modelo para o Caminho B.

> **Como encontrar seu `FOUNDRY_PROJECT_ENDPOINT`:** 
- Abra a barra lateral **Foundry Toolkit** no VS Code → clique com o botão direito no seu projeto → **Copiar endpoint do projeto**. 
- Ou acesse [Azure Portal](https://portal.azure.com) → seu projeto Foundry → **Visão geral** → **Endpoint do projeto**.

> **Como encontrar seu `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Na barra lateral do Foundry Toolkit, expanda seu projeto → **Modelos** → encontre o nome do modelo implantado (ex., `gpt-4.1-mini`).

### Precedência da variável de ambiente

`main.py` usa `load_dotenv(override=True)`, o que significa:

| Prioridade | Fonte | Ganha quando ambos estão definidos? |
|----------|--------|------------------------------|
| 1 (mais alta) | arquivo `.env` | Sim |
| 2 | Variável de ambiente do shell/container | Usada quando a mesma chave não está presente em `.env` |

No desenvolvimento local, isso torna `.env` a fonte da verdade (editar `.env` afeta imediatamente as execuções). Na implantação hospedada, Foundry injeta variáveis de ambiente no nível do container; como `.env` não faz parte da imagem implantada para esta configuração do laboratório, os valores injetados no container são usados.

---

## Compatibilidade de versão

### Matriz de versões de pacotes

O fluxo de trabalho multiagente requer versões específicas dos pacotes. Versões incompatíveis causam erros em tempo de execução.

| Pacote | Versão exigida | Comando de verificação |
|---------|-----------------|---------------------|
| `agent-framework-foundry` | última | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | última | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | última | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Erros comuns de versão

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
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

### Container falha ao iniciar após a implantação

1. **Confira os logs do container:**
   - Abra a barra lateral **Foundry Toolkit** → sob seu projeto, clique em **Agentes** → guia **Agente Hospedado** → clique no seu agente. Verifique o **Status** na aba **Detalhes**, depois abra a aba **Playground** e use a aba **Logs** no painel **Detalhes da sessão** para ver a saída do container.
   - Procure por rastreamentos de pilha Python ou erros de módulo ausente.

2. **Falhas comuns na inicialização do container:**

   | Erro nos logs | Causa | Correção |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` falta um pacote | Adicione o pacote, reimplante |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variáveis de ambiente `agent.yaml` ou `.env` não definidas | Atualize `agent.yaml` → seção `environment_variables` (hospedado) ou `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Identidade Gerenciada não configurada | Foundry configura isso automaticamente - certifique-se de implantar via extensão |
   | `OSError: port 8088 already in use` | Dockerfile expõe porta errada ou conflito de porta | Verifique `EXPOSE 8088` no Dockerfile e `CMD ["python", "main.py"]` |
   | Container sai com código 1 | Exceção não tratada em `main()` | Teste localmente primeiro ([Módulo 5](05-test-locally.md)) para detectar erros antes de implantar |

3. **Reimplante após corrigir:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → selecione o mesmo agente → implante uma nova versão.

### Implantação demora muito

Containers multiagente levam mais tempo para iniciar porque criam 4 instâncias de agente na inicialização. Tempos normais de inicialização:

| Etapa | Duração esperada |
|-------|-----------------|
| Construção da imagem do container | 1-3 minutos |
| Push da imagem para ACR | 30-60 segundos |
| Inicialização do container (agente único) | 15-30 segundos |
| Inicialização do container (multiagente) | 30-120 segundos |
| Agente disponível no Playground | 1-2 minutos após “Iniciado” |

> Se o status “Pendente” persistir além de 5 minutos, verifique os logs do container para erros.

---

## Problemas de RBAC e permissões

### `403 Forbidden` ou `AuthorizationFailed`

Você precisa da função **[Foundry User](https://aka.ms/foundry-ext-project-role)** no seu projeto Foundry (anteriormente chamada **Azure AI User** - ID da função inalterado):

1. Vá para [Azure Portal](https://portal.azure.com) → seu recurso **projeto** Foundry.
2. Clique em **Controle de acesso (IAM)** → **Atribuições de função**.
3. Procure seu nome → confirme que **Foundry User** (ou o rótulo legado **Azure AI User**) está listado.
4. Se faltar: **Adicionar** → **Adicionar atribuição de função** → procure **Foundry User** → atribua à sua conta.

Veja a documentação [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para detalhes.

### Implantação do modelo inacessível

Se o agente retornar erros relacionados ao modelo:

1. Verifique se o modelo está implantado: barra lateral Foundry → expanda o projeto → **Modelos** → verifique `gpt-4.1-mini` (ou seu modelo) com status **Succeeded**.
2. Verifique se o nome da implantação corresponde: compare `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` (ou `agent.yaml`) com o nome real da implantação na barra lateral.
3. Se a implantação expirou (camada gratuita): reimplemente a partir do [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemas do Foundry Local (Caminho B)

### Serviço Foundry Local não está rodando

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Sintoma | Causa | Correção |
|---------|-------|---------|
| Verificação de integridade retorna `503` | Serviço não iniciado | `foundry local start` ou clique em **Iniciar** na barra lateral do Foundry Toolkit |
| Verificação de integridade expira | Modelo ainda carregando | Espere 30–60 s após iniciar; modelos maiores levam mais tempo |
| `StatusCode: 404` em `/v1/health` | Porta errada | O padrão é `5273`. Verifique `foundry local status` para a porta real |
| Recursos insuficientes | Foundry Local precisa de ~4 GB de RAM livre | Feche outros aplicativos |
| Falha no download do modelo | Espaço em disco baixo | Modelos pesam de 2 a 8 GB. Libere espaço e então `foundry model pull <name>` |

### Nome do modelo incompatível

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Defina `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` para o alias exato mostrado (ex., `phi-4-mini`, não `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` na execução local (Caminho B)

O `main.py` do laboratório usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local exige que essa variável aponte para o serviço local - **não** para `AZURE_AI_PROJECT_ENDPOINT`. Certifique-se que seu `.env` contém:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### A ferramenta MCP ainda faz uma chamada externa (Caminho B)

Isso é esperado. A ferramenta `search_microsoft_learn_for_plan` busca recursos de aprendizado do `https://learn.microsoft.com/api/mcp`. **Apenas a consulta pelo nome da habilidade** trafega pela rede - currículo e texto do JD são processados inteiramente no seu dispositivo e nunca são transmitidos. Se for necessário operar completamente offline, adicione um fallback `try/except` na ferramenta que retorna uma URL estática `learn.microsoft.com` quando o endpoint estiver inacessível.

---

## Obtendo ajuda

Se estiver travado após tentar as correções acima:

1. **Verifique os logs do servidor** - A maioria dos erros gera um rastreamento de pilha Python no terminal. Leia o traceback completo.
2. **Pesquise a mensagem de erro** - Copie o texto do erro e pesquise no [Microsoft Q&A para Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Abra uma issue** - Abra uma issue no [repositório do workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) com:
   - Mensagem de erro ou screenshot
   - Suas versões dos pacotes (`pip list | Select-String "agent-framework"`)
   - Sua versão do Python (`python --version`)
   - Se o problema é local ou após implantação

---

### Checkpoint

- [ ] Você sabe como verificar e corrigir problemas de configuração `.env`
- [ ] Você pode verificar se as versões dos pacotes correspondem à matriz exigida
- [ ] Você sabe como verificar logs do container para falhas de implantação
- [ ] Você pode verificar funções RBAC no portal do Azure

---

**Anterior:** [07 - Verificar no Playground](07-verify-in-playground.md) · **Próximo:** [09 - Resumo →](09-summary.md) · **Início:** [Lab 02 README](../README.md) · [Página inicial do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->