# Módulo 8 - Resolução de Problemas

Este módulo aborda erros comuns, correções e estratégias de depuração específicas para o fluxo de trabalho multi-agente.

## Problemas com a saída do agente

### O GapAnalyzer diz “Ainda não tenho o relatório correspondente”

**Sintoma:** A resposta do GapAnalyzer pede para colar um relatório correspondente com "Competências em Falta" e "Lacunas de Certificação". Isto acontece mesmo quando enviou tanto um currículo como uma descrição de trabalho.

**Causa:** O texto do JD não foi passado para o agente JD a jusante. Com `context_mode="last_agent"`, `resume_executor` é o único executor que alguma vez vê a mensagem original do utilizador. Se `RESUME_PARSER_INSTRUCTIONS` não incluir o texto do JD na sua saída, o agente JD não tem o JD para analisar, o MatchingAgent não pode calcular uma pontuação de ajuste, e o GapAnalyzer recebe uma entrada sem sentido.

**Diagnóstico:**

Nos registos do servidor, procure a span do MatchingAgent. Se contiver:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
a passagem direta está ausente ou está com falhas.

**Correção:** Confirme que `RESUME_PARSER_INSTRUCTIONS` em `main.py` contém uma secção `[JOB DESCRIPTION PASS-THROUGH]` e a regra:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Também confirme que `JOB_DESCRIPTION_INSTRUCTIONS` contém uma regra de retransmissão `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Se algum dos blocos de instrução for um esboço do assistente de scaffold, substitua-o pela versão completa de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### O MatchingAgent apresenta “Não é possível calcular a pontuação de ajuste - nenhum JD fornecido”

Esta é a mesma causa raiz indicada acima. O MatchingAgent recebeu a saída do agente JD mas a secção `[PARSED RESUME PASS-THROUGH]` estava ausente ou vazia, por isso não conseguiu comparar os dois perfis. Confirme:
1. `JOB_DESCRIPTION_INSTRUCTIONS` inclui a regra de retransmissão: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` indica ao agente para procurar as secções `[JD REQUIREMENTS]` e `[PARSED RESUME PASS-THROUGH]`.

Substitua ambos os blocos de instruções pelas versões completas de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### A resposta aparece duas vezes

**Sintoma:** A saída do GapAnalyzer (ou toda a saída do pipeline) aparece duas vezes na resposta do Agent Inspector.

**Causa:** `WorkflowBuilder` utiliza semântica OR para arestas de entrada - um executor a jusante dispara assim que **qualquer** predecessor completa. Se `matching_executor` tem duas arestas de entrada (uma do `resume_executor` e outra do `jd_executor`), dispara duas vezes: uma quando ResumeParser termina e outra quando o agente JD termina. O GapAnalyzer também é executado duas vezes.

**Correção:** Assegure que o gráfico `WorkflowBuilder` é um pipeline estritamente sequencial sem fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Se tiver uma linha `.add_edge(resume_executor, matching_executor)` fora do lugar, remova-a. A retransmissão `[PARSED RESUME PASS-THROUGH]` na saída do agente JD já dá ao MatchingAgent acesso ao currículo.

---

## Problemas de ambiente e configuração

### Valores `.env` ausentes ou errados

O ficheiro `.env` deve estar no diretório `PersonalCareerCopilot/` (no mesmo nível de `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Conteúdo esperado em `.env`:

**Caminho A - Cloud Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Caminho B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Ambos os caminhos usam `FOUNDRY_PROJECT_ENDPOINT`. O valor difere: cloud usa um endpoint Foundry `https://`; o local usa `http://localhost:5273/v1`. Execute `foundry model list` para confirmar o alias exato do modelo para o Caminho B.

> **Encontrar o seu `FOUNDRY_PROJECT_ENDPOINT`:** 
- Abra a barra lateral **Foundry Toolkit** no VS Code → clique com o botão direito no seu projeto → **Copiar Endpoint do Projeto**. 
- Ou vá a [Portal Azure](https://portal.azure.com) → o seu projeto Foundry → **Visão geral** → **Endpoint do projeto**.

> **Encontrar o seu `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Na barra lateral do Foundry Toolkit, expanda o seu projeto → **Modelos** → encontre o nome do seu modelo implementado (ex.: `gpt-4.1-mini`).

### Precedência das variáveis de ambiente

`main.py` usa `load_dotenv(override=True)`, o que significa:

| Prioridade | Fonte | Ganha quando ambos estão definidos? |
|----------|--------|-------------------------------|
| 1 (mais alta) | Ficheiro `.env` | Sim |
| 2 | Variável de ambiente no shell / container | Usada quando a mesma chave não está presente em `.env` |

No desenvolvimento local, isto torna `.env` a fonte de verdade (editar `.env` afeta imediatamente as execuções). Na implementação alojada, o Foundry injeta variáveis de ambiente ao nível do container; uma vez que `.env` não faz parte da imagem implementada para esta configuração de laboratório, os valores injetados no container são usados.

---

## Compatibilidade de versões

### Matriz de versões de pacotes

O fluxo multi-agente requer versões específicas de pacotes. Versões incompatíveis causam erros em tempo de execução.

| Pacote | Versão Requerida | Comando de verificação |
|---------|-----------------|-----------------------|
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

### Verificar todas as versões de uma só vez

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

## Problemas de implementação

### O container não inicia após a implementação

1. **Verifique os registos do container:**
   - Abra a barra lateral **Foundry Toolkit** → sob o seu projeto, clique em **Agentes** → separador **Agente alojado** → clique no seu agente. Verifique o **Estado** no separador **Detalhes**, depois abra o separador **Playground** e use o separador **Registos** no painel **Detalhes da sessão** para ver a saída do container.
   - Procure por traces de stack do Python ou erros de módulos em falta.

2. **Falhas comuns no arranque do container:**

   | Erro nos registos | Causa | Correção |
   |-------------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` com um pacote em falta | Adicione o pacote, implemente novamente |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variáveis de ambiente `agent.yaml` ou `.env` não definidas | Atualize `agent.yaml` → secção `environment_variables` (alojado) ou `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Identidade Gerida não configurada | Foundry define isto automaticamente - assegure que está a implementar via a extensão |
   | `OSError: port 8088 already in use` | Dockerfile expõe porta errada ou conflito de portas | Verifique `EXPOSE 8088` no Dockerfile e `CMD ["python", "main.py"]` |
   | Container sai com código 1 | Excepção não tratada em `main()` | Teste localmente primeiro ([Módulo 5](05-test-locally.md)) para apanhar erros antes de implementar |

3. **Reimplemente após corrigir:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Implementar Agente Alojado** → selecione o mesmo agente → implemente uma nova versão.

### A implementação demora demasiado tempo

Os containers multi-agente demoram mais a iniciar porque criam 4 instâncias do agente no arranque. Tempos normais de arranque:

| Etapa | Duração esperada |
|-------|------------------|
| Construção da imagem do container | 1-3 minutos |
| Push da imagem para o ACR | 30-60 segundos |
| Arranque do container (agente único) | 15-30 segundos |
| Arranque do container (multi-agente) | 30-120 segundos |
| Agente disponível no Playground | 1-2 minutos após "Iniciado" |

> Se o estado "Pendente" persistir para além de 5 minutos, verifique os registos do container para erros.

---

## Problemas de RBAC e permissões

### `403 Forbidden` ou `AuthorizationFailed`

Precisa do papel **[Utilizador Foundry](https://aka.ms/foundry-ext-project-role)** no seu projeto Foundry (anteriormente chamado **Azure AI User** - ID do papel inalterado):

1. Vá a [Portal Azure](https://portal.azure.com) → o seu recurso **projeto** Foundry.
2. Clique em **Controlo de acesso (IAM)** → **Atribuições de papel**.
3. Pesquise o seu nome → confirme que **Utilizador Foundry** (ou a etiqueta antiga **Azure AI User**) está listado.
4. Se ausente: **Adicionar** → **Adicionar atribuição de papel** → procure por **Utilizador Foundry** → atribua à sua conta.

Consulte a documentação [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para detalhes.

### Implementação do modelo não acessível

Se o agente retornar erros relacionados com o modelo:

1. Verifique se o modelo está implementado: barra lateral Foundry → expanda o projeto → **Modelos** → veja se `gpt-4.1-mini` (ou o seu modelo) está com estado **Succeeded**.
2. Verifique se o nome da implementação corresponde: compare `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` (ou `agent.yaml`) com o nome real da implementação na barra lateral.
3. Se a implementação expirou (nível gratuito): reimplemente a partir do [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Abrir Catálogo de Modelos**).

---

## Problemas do Foundry Local (Caminho B)

### Serviço Foundry Local não está em execução

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Sintoma | Causa | Correção |
|---------|-------|---------|
| Verificação de estado retorna `503` | Serviço não iniciado | `foundry local start` ou clique em **Iniciar** na barra lateral do Foundry Toolkit |
| Verificação de estado excede o tempo limite | Modelo ainda a carregar | Espere 30–60 s após iniciar; modelos maiores demoram mais |
| `StatusCode: 404` em `/v1/health` | Porta errada | O padrão é `5273`. Verifique `foundry local status` para a porta real |
| Recursos insuficientes | Foundry Local precisa de ~4 GB RAM livres | Feche outras aplicações |
| Falha no download do modelo | Espaço em disco insuficiente | Modelos têm 2–8 GB. Libere espaço e depois `foundry model pull <name>` |

### Incompatibilidade de nome do modelo

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Defina `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `.env` para o alias exato mostrado (ex.: `phi-4-mini`, não `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` na execução local (Caminho B)

O laboratório `main.py` usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local requer que esta variável aponte para o serviço local - **não** para `AZURE_AI_PROJECT_ENDPOINT`. Assegure que o seu `.env` contém:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### A ferramenta MCP ainda faz uma chamada externa (Caminho B)

Isto é esperado. A ferramenta `search_microsoft_learn_for_plan` busca recursos de aprendizagem do `https://learn.microsoft.com/api/mcp`. **Só a consulta do nome da competência** viaja pela rede - o currículo e o texto do JD são processados inteiramente no seu dispositivo e nunca transmitidos. Se for necessária operação totalmente offline, adicione uma reserva `try/except` na ferramenta que retorne um URL estático `learn.microsoft.com` quando o endpoint estiver inacessível.

---

## Obter ajuda

Se estiver bloqueado após tentar as correções acima:

1. **Verifique os registos do servidor** - A maioria dos erros produz uma trace de stack do Python no terminal. Leia o rastreio completo.
2. **Pesquise a mensagem de erro** - Copie o texto do erro e pesquise em [Microsoft Q&A para Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Abra uma questão** - Crie uma questão no [repositório do workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) com:
   - A mensagem de erro ou captura de ecrã
   - As suas versões de pacotes (`pip list | Select-String "agent-framework"`)
   - A sua versão do Python (`python --version`)
   - Se o problema é local ou após implementação

---

### Ponto de verificação

- [ ] Sabe como verificar e corrigir problemas de configuração `.env`
- [ ] Pode verificar se as versões dos pacotes correspondem à matriz requerida
- [ ] Sabe como verificar registos do container para falhas na implementação
- [ ] Pode verificar os papéis RBAC no Portal Azure

---

**Anterior:** [07 - Verificar no Playground](07-verify-in-playground.md) · **Próximo:** [09 - Resumo →](09-summary.md) · **Início:** [Lab 02 README](../README.md) · [Início do Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->