# Módulo 8 - Solução de problemas

Este módulo é um guia de referência para problemas comuns. Adicione aos favoritos e retorne quando algo der errado.

---

## 1. Erros de permissão

### 1.1 Permissão `agents/write` negada

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Causa raiz:** Falta do papel `Azure AI User` no nível do **projeto**. Este é o erro mais comum do workshop.

**Correção:**
1. Abra [portal.azure.com](https://portal.azure.com).
2. Procure o nome do seu **projeto** Foundry → clique no resultado do tipo **"Microsoft Foundry project"** (NÃO conta pai).
3. **Controle de acesso (IAM)** → **+ Adicionar** → **Adicionar atribuição de função**.
4. Função: **Azure AI User** → Avançar.
5. Membros: Selecione você → Revisar + atribuir → Revisar + atribuir.
6. **Aguarde 1–2 minutos** → tente novamente.

> **Por que Owner/Contributor não é suficiente:** Esses papéis concedem apenas ações de *gerenciamento*. Operações de agente exigem a *ação de dados* `agents/write`, que está presente somente em `Azure AI User`, `Azure AI Developer` ou `Azure AI Owner`. Veja os [docs RBAC do Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante provisionamento

**Correção:** Peça ao administrador para atribuir **Contributor** no grupo de recursos, ou para criar o projeto para você e conceder **Azure AI User** nele.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Espere até: "Registrado"
```

---

## 2. Erros do Docker

> Docker é **opcional**. Estas situações só se aplicam se o Docker Desktop estiver instalado e a extensão tentar uma compilação local.

### 2.1 Docker daemon não está rodando

**Correção:** Inicie o Docker Desktop → aguarde o status "em execução" → verifique com `docker info` → tente novamente.

### 2.2 Falha na compilação com erros de dependência

**Correção:** Verifique a ortografia do arquivo `requirements.txt`, teste localmente primeiro: `pip install -r requirements.txt`.

### 2.3 Incompatibilidade de plataforma (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Erros de autenticação

### 3.1 `DefaultAzureCredential` falha

**Correção (tente na ordem):**
1. `az login` (reauthenticar)
2. `az account set --subscription "<id>"` (assinatura correta)
3. VS Code → Contas → Sair → Entrar novamente
4. Verificar: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funciona localmente mas não no hospedado

**Esperado:** Agentes hospedados usam identidade gerenciada do sistema, não sua credencial. Se o agente hospedado apresentar erros de autenticação:
- Verifique se `AZURE_AI_PROJECT_ENDPOINT` em `agent.yaml` está correto
- Confirme se a identidade gerenciada do projeto tem acesso ao modelo

---

## 4. Erros de modelo

### 4.1 Implantação do modelo não encontrada

**Correção:** O nome é **case-sensitive**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` com o nome exato na barra lateral do Foundry → Modelos.

### 4.2 Saída inesperada do modelo

**Correção:** Revise `AGENT_INSTRUCTIONS` em `main.py` (não está truncado?). Tente um modelo diferente (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Erros de implantação

### 5.1 Pull ACR não autorizado

**Correção:** Portal do Azure → Registro de Contêiner → Controle de acesso (IAM) → Adicione a função **AcrPull** à identidade gerenciada do projeto Foundry.

### 5.2 Agente falha ao iniciar (fica "Pendente" ou "Falhou")

Verifique os logs do contêiner na barra lateral. Causas comuns:

| Mensagem do log | Correção |
|-------------|-----|
| `ModuleNotFoundError` | Adicione o pacote faltante em `requirements.txt`, reimplante |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Adicione a variável de ambiente no `agent.yaml` em `environment_variables` |
| `Address already in use` | Garanta que apenas um processo use a porta 8088 |

### 5.3 Tempo de implantação esgotado

**Correção:** Verifique a conexão com a internet. A primeira implantação envia >100MB. Está atrás de um proxy? Configure as definições de proxy do Docker Desktop.

---

## 6. Caminho B - Foundry Local

### 6.1 Foundry Local não inicia

| Problema | Correção |
|-------|-----|
| `foundry: command not found` | Reinstale: `winget install Microsoft.FoundryLocal` |
| Recursos insuficientes | Foundry Local precisa de ~4GB de RAM livre. Feche outros aplicativos. |
| Falha no download do modelo | Verifique espaço em disco (modelos têm 2–8 GB). Tente novamente: `foundry local models pull <nome>` |

### 6.2 Erros em modelos Foundry Local

| Problema | Correção |
|-------|-----|
| Respostas lentas | Esperado - modelos locais usam CPU a não ser que tenha GPU. Tenha paciência. |
| Saída de baixa qualidade | Tente um modelo maior se seu hardware permitir. `phi-4-mini` é um bom equilíbrio. |
| Conexão recusada | Verifique se Foundry Local está rodando: `foundry local status`. Reinicie se precisar. |

---

## 7. Referência rápida: papéis RBAC

| Papel | Escopo | Concede |
|------|-------|--------|
| **Azure AI User** | Projeto | Ações de dados: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projeto/Conta | Ações de dados + criação de projeto |
| **Azure AI Owner** | Conta | Acesso total + gerenciamento de papéis |
| **Contributor** | Assinatura/Grupo de Recursos | Apenas ações de gerenciamento (**sem** ações de dados) |
| **Owner** | Assinatura/Grupo de Recursos | Gerenciamento + atribuição de papéis (**sem** ações de dados) |

---

## 8. Checklist de conclusão do workshop

| # | Item | Módulo |
|---|------|--------|
| 1 | Pré-requisitos instalados e verificados | [00](00-prerequisites.md) |
| 2 | Extensão Foundry Toolkit instalada, projeto conectado (ou Caminho B configurado) | [01](01-setup.md) |
| 3 | Agente hospedado criado | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurado, instruções escritas, dependências instaladas | [03](03-configure-and-code.md) |
| 5 | Agente testado localmente - 3 cenários funcionais passaram | [04](04-test-locally.md) |
| 6 | Implantado no Foundry (somente Caminho A) | [05](05-deploy-to-foundry.md) |
| 7 | Testes de caso extremo/segurança passados na nuvem (somente Caminho A) | [06](06-verify-in-playground.md) |
| 8 | Resumo revisado, próximos passos identificados | [07](07-summary.md) |

---

**Anterior:** [07 - Resumo](07-summary.md) · **Início:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->