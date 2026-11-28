# Módulo 8 - Solução de Problemas

Este módulo é um guia de referência para problemas comuns. Marque-o e retorne quando algo der errado.

---

## 1. Erros de permissão

### 1.1 `agents/write` permissão negada

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Causa raiz:** Falta da função `Azure AI User` no nível do **projeto**. Este é o erro número 1 do workshop.

**Correção:**
1. Abra [portal.azure.com](https://portal.azure.com).
2. Pesquise pelo nome do seu **projeto** Foundry → clique no resultado do tipo **"Microsoft Foundry project"** (NÃO conta pai).
3. **Controle de acesso (IAM)** → **+ Adicionar** → **Adicionar atribuição de função**.
4. Função: **Usuário Azure AI** → Próximo.
5. Membros: Selecione você mesmo → Revisar + atribuir → Revisar + atribuir.
6. **Aguarde 1–2 minutos** → tente novamente.

> **Por que Proprietário/Colaborador não é suficiente:** Essas funções concedem apenas ações de *gerenciamento*. Operações de agente requerem a `agents/write` *ação de dados*, que está apenas em `Azure AI User`, `Azure AI Developer`, ou `Azure AI Owner`. Veja [documentação Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante o provisionamento

**Correção:** Peça ao seu administrador para atribuir **Colaborador** no grupo de recursos, ou que ele crie o projeto para você e conceda a você o papel **Usuário Azure AI** nele.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Erros do Docker

> Docker é **opcional**. Estes só se aplicam se o Docker Desktop estiver instalado e a extensão tentar uma compilação local.

### 2.1 Docker daemon não está executando

**Correção:** Inicie o Docker Desktop → aguarde o status "em execução" → verifique com `docker info` → tente novamente.

### 2.2 Falha na compilação com erros de dependência

**Correção:** Verifique a ortografia de `requirements.txt`, teste localmente primeiro: `pip install -r requirements.txt`.

### 2.3 Incompatibilidade de plataforma (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Erros de autenticação

### 3.1 Falha em `DefaultAzureCredential`

**Correção (tente na ordem):**
1. `az login` (reautentique)
2. `az account set --subscription "<id>"` (assinatura correta)
3. VS Code → Contas → Sair → Entrar novamente
4. Verifique: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funciona localmente mas não no hospedado

**Esperado:** Agentes hospedados usam identidade gerenciada pelo sistema, não suas credenciais. Se o agente hospedado obtiver erros de autenticação:
- Verifique se `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `agent.yaml` resolve para o nome do seu deployment do modelo (`FOUNDRY_PROJECT_ENDPOINT` é injetado pelo Foundry em tempo de execução - não declare em `agent.yaml`)
- Confira se a identidade gerenciada do projeto tem acesso ao modelo

---

## 4. Erros do modelo

### 4.1 Deployment do modelo não encontrado

**Correção:** O nome é **sensível a maiúsculas e minúsculas**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` com o nome exato na barra lateral do Foundry → Modelos.

### 4.2 Saída inesperada do modelo

**Correção:** Reveja `AGENT_INSTRUCTIONS` em `main.py` (não truncado?). Tente um modelo diferente (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Erros de deployment

### 5.1 Pull do ACR não autorizado

**Correção:** Portal Azure → Registro de Contêiner → Controle de acesso (IAM) → Adicione a função **AcrPull** à identidade gerenciada do projeto Foundry.

### 5.2 Agente falha ao iniciar (fica "Pendente" ou "Falhou")

Verifique os logs do contêiner na barra lateral. Causas comuns:

| Mensagem do log | Correção |
|----------------|---------|
| `ModuleNotFoundError` | Adicione pacote faltante em `requirements.txt`, redeploy |
| `ValueError: Missing required environment variables` | Confirme que `AZURE_AI_MODEL_DEPLOYMENT_NAME` está declarado em `agent.yaml` sob `environment_variables` e tem um valor, depois redeploy. `FOUNDRY_PROJECT_ENDPOINT` é injetado pelo Foundry em tempo de execução |
| `Address already in use` | Assegure que somente um processo está ligado à porta 8088 |

### 5.3 Deployment expira

**Correção:** Verifique a conexão com a internet. O primeiro push de deployment é >100MB. Está atrás de um proxy? Configure as definições de proxy do Docker Desktop.

---

## 6. Caminho B - Foundry Local

### 6.1 Foundry Local não inicia

| Problema | Correção |
|---------|---------|
| `foundry: command not found` | Reinstale: `winget install Microsoft.FoundryLocal` |
| Recursos insuficientes | Foundry Local precisa de ~4GB RAM livres. Feche outros apps. |
| Falha no download de modelos | Verifique espaço em disco (modelos têm 2–8 GB). Tente novamente: `foundry local models pull <name>` |

### 6.2 Erros de modelo no Foundry Local

| Problema | Correção |
|---------|---------|
| Respostas lentas | Esperado - modelos locais rodam na CPU a menos que tenha GPU. Tenha paciência. |
| Saída com qualidade ruim | Tente um modelo maior se seu hardware permitir. `phi-4-mini` é um bom equilíbrio. |
| Conexão recusada | Verifique se Foundry Local está rodando: `foundry local status`. Reinicie se precisar. |

---

## 7. Referência rápida: funções RBAC

| Função | Escopo | Concede |
|--------|--------|---------|
| **Usuário Azure AI** | Projeto | Ações de dados: `agents/write`, `agents/read` |
| **Desenvolvedor Azure AI** | Projeto/Conta | Ações de dados + criação de projeto |
| **Proprietário Azure AI** | Conta | Acesso total + gerenciamento de funções |
| **Colaborador** | Assinatura/GR | Apenas ações de gerenciamento (**sem** ações de dados) |
| **Proprietário** | Assinatura/GR | Gerenciamento + atribuição de funções (**sem** ações de dados) |

---

## 8. Lista de verificação para conclusão do workshop

| # | Item | Módulo |
|---|------|---------|
| 1 | Pré-requisitos instalados e verificados | [00](00-prerequisites.md) |
| 2 | Extensão Foundry Toolkit instalada, projeto conectado (ou Caminho B configurado) | [01](01-setup.md) |
| 3 | Agente hospedado estruturado | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurado, instruções escritas, dependências instaladas | [03](03-configure-and-code.md) |
| 5 | Agente testado localmente - 3 cenários funcionais aprovados | [04](04-test-locally.md) |
| 6 | Implantado no Foundry (só Caminho A) | [05](05-deploy-to-foundry.md) |
| 7 | Testes de casos extremos/segurança aprovados na nuvem (só Caminho A) | [06](06-verify-in-playground.md) |
| 8 | Resumo revisado, próximos passos identificados | [07](07-summary.md) |

---

**Anterior:** [07 - Resumo](07-summary.md) · **Início:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->