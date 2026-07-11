# Módulo 8 - Resolução de problemas

Este módulo é um guia de referência para problemas comuns. Faça um marcador e volte quando algo correr mal.

---

## 1. Erros de permissão

### 1.1 Permissão `agents/write` negada

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Causa raiz:** Falta o papel `Azure AI User` ao nível do **projeto**. Este é o erro nº 1 no workshop.

**Correção:**
1. Abra [portal.azure.com](https://portal.azure.com).
2. Pesquise o nome do seu **projeto** Foundry → clique no resultado do tipo **"Microsoft Foundry project"** (NÃO conta pai).
3. **Controlos de acesso (IAM)** → **+ Adicionar** → **Adicionar atribuição de papel**.
4. Papel: **Azure AI User** → Seguinte.
5. Membros: Selecione-se a si próprio → Rever + atribuir → Rever + atribuir.
6. **Espere 1–2 minutos** → tente novamente.

> **Por que Owner/Contributor não é suficiente:** Estes papéis concedem apenas ações de *gestão*. Operações de agentes requerem a *ação de dados* `agents/write`, que existe apenas no `Azure AI User`, `Azure AI Developer` ou `Azure AI Owner`. Veja a [documentação RBAC do Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante o provisionamento

**Correção:** Peça ao seu administrador para atribuir **Contributor** no grupo de recursos, ou que crie o projeto para si e lhe conceda **Azure AI User** nesse projeto.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Aguarde até: "Registado"
```

---

## 2. Erros do Docker

> Docker é **opcional**. Estes erros aplicam-se apenas se tiver instalado o Docker Desktop e a extensão tentar uma construção local.

### 2.1 O daemon do Docker não está a correr

**Correção:** Inicie o Docker Desktop → aguarde pelo estado "executar" → verifique com `docker info` → tente novamente.

### 2.2 A construção falha com erros de dependências

**Correção:** Verifique a ortografia do `requirements.txt`, teste localmente primeiro: `pip install -r requirements.txt`.

### 2.3 Incompatibilidade de plataforma (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Erros de autenticação

### 3.1 `DefaultAzureCredential` falha

**Correção (tente pela ordem):**
1. `az login` (reautentique-se)
2. `az account set --subscription "<id>"` (subscrição correta)
3. VS Code → Contas → Terminar sessão → Iniciar sessão novamente
4. Verificar: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funciona localmente mas não em alojamento

**Esperado:** Agentes alojados usam identidade gerida pelo sistema, não a sua credencial. Se o agente alojado apresentar erros de autenticação:
- Verifique se `AZURE_AI_PROJECT_ENDPOINT` em `agent.yaml` está correto
- Verifique se a identidade gerida do projeto tem acesso ao modelo

---

## 4. Erros de modelo

### 4.1 Implantação do modelo não encontrada

**Correção:** O nome é **sensível a maiúsculas/minúsculas**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` com o nome exato na barra lateral do Foundry → Modelos.

### 4.2 Saída inesperada do modelo

**Correção:** Reveja `AGENT_INSTRUCTIONS` em `main.py` (não estará truncado?). Experimente outro modelo (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Erros de implantação

### 5.1 ACR pull não autorizado

**Correção:** Portal Azure → Registo de Contentores → Controlos de Acesso (IAM) → Adicionar papel **AcrPull** à identidade gerida do projeto Foundry.

### 5.2 O agente falha a iniciar (fica "Pendente" ou "Falhado")

Verifique os logs do contentor na barra lateral. Causas comuns:

| Mensagem de log | Correção |
|-------------|-----|
| `ModuleNotFoundError` | Adicionar pacote em falta no `requirements.txt`, reimplantar |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Adicionar variável ambiente a `agent.yaml` em `environment_variables` |
| `Address already in use` | Assegurar que só um processo liga a porta 8088 |

### 5.3 A implantação expira

**Correção:** Verifique a ligação à internet. O primeiro push de implantação tem >100MB. Está atrás de proxy? Configure o proxy no Docker Desktop.

---

## 6. Caminho B - Foundry Local

### 6.1 Foundry Local não inicia

| Problema | Correção |
|-------|-----|
| `foundry: command not found` | Reinstalar: `winget install Microsoft.FoundryLocal` |
| Recursos insuficientes | O Foundry Local precisa de ~4GB de RAM livre. Feche outras aplicações. |
| Falha na transferência do modelo | Verifique espaço em disco (modelos têm 2–8 GB). Tente novamente: `foundry local models pull <nome>` |

### 6.2 Erros de modelo no Foundry Local

| Problema | Correção |
|-------|-----|
| Respostas lentas | Esperado - modelos locais correm no CPU a menos que tenha GPU. Tenha paciência. |
| Saída de baixa qualidade | Experimente um modelo maior se o seu hardware permitir. `phi-4-mini` é um bom equilíbrio. |
| Ligação recusada | Verifique se o Foundry Local está a correr: `foundry local status`. Reinicie se necessário. |

---

## 7. Referência rápida: papéis RBAC

| Papel | Âmbito | Concede |
|------|-------|--------|
| **Azure AI User** | Projeto | Ações de dados: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projeto/Conta | Ações de dados + criação de projeto |
| **Azure AI Owner** | Conta | Acesso total + gestão de papéis |
| **Contributor** | Subscrição/Grupo de recursos | Apenas ações de gestão (**sem** ações de dados) |
| **Owner** | Subscrição/Grupo de recursos | Gestão + atribuição de papéis (**sem** ações de dados) |

---

## 8. Lista de verificação para conclusão do workshop

| # | Item | Módulo |
|---|------|--------|
| 1 | Pré-requisitos instalados e verificados | [00](00-prerequisites.md) |
| 2 | Extensão Foundry Toolkit instalada, projeto ligado (ou Caminho B configurado) | [01](01-setup.md) |
| 3 | Agente alojado criado | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurado, instruções escritas, dependências instaladas | [03](03-configure-and-code.md) |
| 5 | Agente testado localmente - passam 3 cenários funcionais | [04](04-test-locally.md) |
| 6 | Implantado no Foundry (apenas Caminho A) | [05](05-deploy-to-foundry.md) |
| 7 | Testes de casos excecionais/segurança passam na cloud (apenas Caminho A) | [06](06-verify-in-playground.md) |
| 8 | Resumo revisto, próximos passos identificados | [07](07-summary.md) |

---

**Anterior:** [07 - Sumário](07-summary.md) · **Início:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->