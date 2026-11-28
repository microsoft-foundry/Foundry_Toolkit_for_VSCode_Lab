# Módulo 8 - Resolução de problemas

Este módulo é um guia de referência para problemas comuns. Adicione-o aos favoritos e volte quando algo correr mal.

---

## 1. Erros de permissão

### 1.1 `agents/write` permissão negada

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Causa raiz:** Falta da função `Azure AI User` a nível do **projeto**. Este é o erro nº1 no workshop.

**Correção:**
1. Abra [portal.azure.com](https://portal.azure.com).
2. Pesquise o nome do seu **projeto** Foundry → clique no resultado do tipo **"Microsoft Foundry project"** (NÃO na conta principal).
3. **Controlo de acesso (IAM)** → **+ Adicionar** → **Adicionar atribuição de função**.
4. Função: **Azure AI User** → Seguinte.
5. Membros: Selecione-se a si próprio → Rever + atribuir → Rever + atribuir.
6. **Aguarde 1–2 minutos** → tente novamente.

> **Por que Owner/Contributor não é suficiente:** Estas funções concedem apenas ações de *gestão*. Operações de agente requerem a `agents/write` *ação de dados*, que está apenas em `Azure AI User`, `Azure AI Developer`, ou `Azure AI Owner`. Consulte [documentação RBAC Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante o provisionamento

**Correção:** Peça ao seu administrador para atribuir **Contributor** ao grupo de recursos, ou que crie o projeto para si e lhe conceda **Azure AI User**.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Erros do Docker

> Docker é **opcional**. Estes aplicam-se apenas se o Docker Desktop estiver instalado e a extensão tentar uma compilação local.

### 2.1 Daemon do Docker não está a correr

**Correção:** Inicie o Docker Desktop → aguarde o estado "a correr" → verifique com `docker info` → tente novamente.

### 2.2 Falha no build com erros de dependência

**Correção:** Verifique a ortografia do `requirements.txt`, teste localmente primeiro: `pip install -r requirements.txt`.

### 2.3 Incompatibilidade de plataforma (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Erros de autenticação

### 3.1 Falha de `DefaultAzureCredential`

**Correção (tente por ordem):**
1. `az login` (reautenticar)
2. `az account set --subscription "<id>"` (assinatura correta)
3. VS Code → Contas → Terminar sessão → Iniciar sessão novamente
4. Verifique: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funciona localmente mas não em alojamento

**Esperado:** Os agentes alojados usam identidade gerida pelo sistema, não as suas credenciais. Se o agente alojado obtiver erros de autenticação:
- Verifique que `AZURE_AI_MODEL_DEPLOYMENT_NAME` em `agent.yaml` resolve para o nome do seu deployment de modelo (`FOUNDRY_PROJECT_ENDPOINT` é injetado pelo Foundry em runtime - não o declare em `agent.yaml`)
- Confirme que a identidade gerida do projeto tem acesso ao modelo

---

## 4. Erros de modelo

### 4.1 Deployment do modelo não encontrado

**Correção:** O nome é **sensível a maiúsculas/minúsculas**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` com o nome exato na barra lateral do Foundry → Modelos.

### 4.2 Saída inesperada do modelo

**Correção:** Reveja `AGENT_INSTRUCTIONS` em `main.py` (não está truncado?). Experimente um modelo diferente (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Erros de deployment

### 5.1 Pull no ACR não autorizado

**Correção:** Portal Azure → Container Registry → Controlo de acesso (IAM) → Adicionar função **AcrPull** à identidade gerida do projeto Foundry.

### 5.2 O agente falha ao iniciar (permanece "Pendente" ou "Falhou")

Verifique os logs do contentor na barra lateral. Causas comuns:

| Mensagem de log | Correção |
|-------------|-----|
| `ModuleNotFoundError` | Adicione o pacote em falta a `requirements.txt`, redeploy |
| `ValueError: Missing required environment variables` | Confirme que `AZURE_AI_MODEL_DEPLOYMENT_NAME` está declarado em `agent.yaml` sob `environment_variables` e tem um valor, depois redeploy. `FOUNDRY_PROJECT_ENDPOINT` é injetado pelo Foundry em runtime |
| `Address already in use` | Assegure que só um processo está a ligar-se à porta 8088 |

### 5.3 Deployment expira por tempo esgotado

**Correção:** Verifique a ligação à Internet. O primeiro deploy envia >100MB. Está atrás de um proxy? Configure as definições de proxy do Docker Desktop.

---

## 6. Caminho B - Foundry Local

### 6.1 O Foundry Local não inicia

| Problema | Correção |
|-------|-----|
| `foundry: command not found` | Reinstale: `winget install Microsoft.FoundryLocal` |
| Recursos insuficientes | O Foundry Local precisa de cerca de 4GB de RAM livre. Feche outras aplicações. |
| Falha no download do modelo | Verifique espaço no disco (modelos têm entre 2–8 GB). Tente de novo: `foundry local models pull <name>` |

### 6.2 Erros de modelo no Foundry Local

| Problema | Correção |
|-------|-----|
| Respostas lentas | Esperado - modelos locais correm na CPU a menos que tenha uma GPU. Tenha paciência. |
| Saída de qualidade pobre | Tente um modelo maior se o seu hardware permitir. `phi-4-mini` é um bom compromisso. |
| Ligação recusada | Verifique que o Foundry Local está a correr: `foundry local status`. Reinicie se necessário. |

---

## 7. Referência rápida: funções RBAC

| Função | Âmbito | Concede |
|------|-------|--------|
| **Azure AI User** | Projeto | Ações de dados: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projeto/Conta | Ações de dados + criação de projeto |
| **Azure AI Owner** | Conta | Acesso total + gestão de funções |
| **Contributor** | Subscrição/GR | Apenas ações de gestão (**sem** ações de dados) |
| **Owner** | Subscrição/GR | Gestão + atribuição de funções (**sem** ações de dados) |

---

## 8. Lista de verificação para conclusão do workshop

| # | Item | Módulo |
|---|------|--------|
| 1 | Pré-requisitos instalados e verificados | [00](00-prerequisites.md) |
| 2 | Extensão Foundry Toolkit instalada, projeto conectado (ou Caminho B configurado) | [01](01-setup.md) |
| 3 | Agente alojado estruturado | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurado, instruções escritas, dependências instaladas | [03](03-configure-and-code.md) |
| 5 | Agente testado localmente - 3 cenários funcionais aprovados | [04](04-test-locally.md) |
| 6 | Desplegado no Foundry (apenas Caminho A) | [05](05-deploy-to-foundry.md) |
| 7 | Testes de casos extremos/segurança aprovados na cloud (apenas Caminho A) | [06](06-verify-in-playground.md) |
| 8 | Resumo revisto, próximos passos identificados | [07](07-summary.md) |

---

**Anterior:** [07 - Resumo](07-summary.md) · **Início:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->