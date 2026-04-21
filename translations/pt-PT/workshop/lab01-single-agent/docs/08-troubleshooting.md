# Module 8 - Resolução de Problemas

Este módulo é um guia de referência para todos os problemas comuns encontrados durante o workshop. Favoritar - irá consultá-lo sempre que algo correr mal.

---

## 1. Erros de permissão

### 1.1 Permissão `agents/write` negada

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Causa raiz:** Não tem o papel `Azure AI User` ao nível do **projeto**. Este é o erro mais comum no workshop.

**Correção - passo a passo:**

1. Abra [https://portal.azure.com](https://portal.azure.com).
2. Na barra de pesquisa superior, escreva o nome do seu **projeto Foundry** (ex.: `workshop-agents`).
3. **Crítico:** Clique no resultado que mostra o tipo **"Microsoft Foundry project"**, NÃO na conta/central principal. São recursos diferentes com escopos RBAC diferentes.
4. Na navegação esquerda da página do projeto, clique em **Controlo de acesso (IAM)**.
5. Clique no separador **Atribuições de função** para verificar se já tem a função:
   - Procure pelo seu nome ou email.
   - Se `Azure AI User` já estiver listado → o erro tem outra causa (ver Passo 8 abaixo).
   - Se não estiver listado → prossiga para adicioná-la.
6. Clique em **+ Adicionar** → **Adicionar atribuição de função**.
7. No separador **Função**:
   - Procure [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Selecione-a nos resultados.
   - Clique em **Seguinte**.
8. No separador **Membros**:
   - Selecione **Utilizador, grupo ou principal de serviço**.
   - Clique em **+ Selecionar membros**.
   - Procure pelo seu nome ou endereço de email.
   - Selecione-se nos resultados.
   - Clique em **Selecionar**.
9. Clique em **Rever + atribuir** → **Rever + atribuir** novamente.
10. **Espere 1-2 minutos** - as alterações RBAC demoram a propagar.
11. Tente novamente a operação que falhou.

> **Por que Owner/Contributor não basta:** O Azure RBAC tem dois tipos de permissões - *ações de gestão* e *ações de dados*. Owner e Contributor concedem ações de gestão (criar recursos, editar definições), mas operações de agentes requerem a ação de dados `agents/write`, que só está incluída nas funções `Azure AI User`, `Azure AI Developer` ou `Azure AI Owner`. Veja [docs Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante a criação de recursos

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Causa raiz:** Não tem permissão para criar ou modificar recursos Azure nesta subscrição/grupo de recursos.

**Correção:**
1. Peça ao administrador da subscrição para lhe atribuir o papel **Contributor** no grupo de recursos onde vive o seu projeto Foundry.
2. Alternativamente, peça para criarem o projeto Foundry para si e lhe concederem **Azure AI User** no projeto.

### 1.3 `SubscriptionNotRegistered` para [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Causa raiz:** A subscrição Azure não registou o fornecedor de recursos necessário para o Foundry.

**Correção:**

1. Abra um terminal e execute:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Aguarde o registo completar (pode demorar 1-5 minutos):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Resultado esperado: `"Registered"`
3. Tente novamente a operação.

---

## 2. Erros Docker (apenas se Docker estiver instalado)

> O Docker é **opcional** para este workshop. Estes erros aplicam-se apenas se tem o Docker Desktop instalado e a extensão Foundry tenta uma construção local do contentor.

### 2.1 Docker daemon não está a correr

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Correção - passo a passo:**

1. **Encontre o Docker Desktop** no seu menu Iniciar (Windows) ou Aplicações (macOS) e inicie-o.
2. Aguarde a janela do Docker Desktop mostrar **"Docker Desktop is running"** - normalmente demora 30-60 segundos.
3. Procure o ícone da baleia Docker na barra do sistema (Windows) ou barra de menus (macOS). Passe o cursor sobre ele para confirmar o estado.
4. Verifique num terminal:
   ```powershell
   docker info
   ```
   Se isto imprimir informações do sistema Docker (Server Version, Storage Driver, etc.), o Docker está a correr.
5. **Específico Windows:** Se o Docker ainda não arrancar:
   - Abra Docker Desktop → **Settings** (ícone de engrenagem) → **General**.
   - Verifique que **Use the WSL 2 based engine** está marcado.
   - Clique em **Apply & restart**.
   - Se o WSL 2 não estiver instalado, execute `wsl --install` num PowerShell elevado e reinicie o computador.
6. Tente novamente a implantação.

### 2.2 A construção Docker falha com erros de dependência

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Correção:**
1. Abra o ficheiro `requirements.txt` e verifique se todos os nomes de pacotes estão escritos corretamente.
2. Garanta que o bloqueio de versões está correto:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Teste a instalação localmente primeiro:
   ```bash
   pip install -r requirements.txt
   ```
4. Se usar um índice privado de pacotes, assegure que o Docker tem acesso de rede a ele.

### 2.3 Incompatibilidade da plataforma do contentor (Apple Silicon)

Se estiver a implementar a partir de um Mac Apple Silicon (M1/M2/M3/M4), o contentor deve ser construído para `linux/amd64` porque o runtime do Foundry usa AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> O comando de deploy da extensão Foundry trata disto automaticamente na maioria dos casos. Se vir erros relacionados com arquitetura, construa manualmente com a flag `--platform` e contacte a equipa Foundry.

---

## 3. Erros de autenticação

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) falha ao obter token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Causa raiz:** Nenhuma das fontes de credenciais na cadeia `DefaultAzureCredential` tem token válido.

**Correção - tente cada passo por ordem:**

1. **Relogue via Azure CLI** (correção mais comum):
   ```bash
   az login
   ```
   Será aberta uma janela do navegador. Inicie sessão e depois volte ao VS Code.

2. **Defina a subscrição correta:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Se esta não for a subscrição correta:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Relogue via VS Code:**
   - Clique no ícone **Contas** (ícone de pessoa) no canto inferior esquerdo do VS Code.
   - Clique no nome da sua conta → **Sair**.
   - Clique novamente no ícone Contas → **Iniciar sessão na Microsoft**.
   - Complete o fluxo de login no navegador.

4. **Principal de serviço (cenários CI/CD apenas):**
   - Defina estas variáveis de ambiente no seu `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Depois reinicie o processo do agente.

5. **Verifique cache do token:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Se isto falhar, o seu token CLI expirou. Execute `az login` novamente.

### 3.2 Token funciona localmente mas não na implantação hospedada

**Causa raiz:** O agente hospedado usa uma identidade gerida pelo sistema, diferente da sua credencial pessoal.

**Correção:** Este é o comportamento esperado - a identidade gerida é provisionada automaticamente durante a implantação. Se o agente hospedado continuar a ter erros de autenticação:
1. Verifique que a identidade gerida do projeto Foundry tem acesso ao recurso Azure OpenAI.
2. Confirme que `PROJECT_ENDPOINT` em `agent.yaml` está correto.

---

## 4. Erros de modelo

### 4.1 Implantação do modelo não encontrada

```
Error: Model deployment not found / The specified deployment does not exist
```

**Correção - passo a passo:**

1. Abra o seu ficheiro `.env` e anote o valor de `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Abra a barra lateral **Microsoft Foundry** no VS Code.
3. Expanda o seu projeto → **Model Deployments**.
4. Compare o nome da implantação listado aí com o valor no seu `.env`.
5. O nome é **sensível a maiúsculas/minúsculas** - `gpt-4o` é diferente de `GPT-4o`.
6. Se não coincidir, atualize o seu `.env` para usar exatamente o nome mostrado na barra lateral.
7. Para implantação hospedada, atualize também o `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modelo responde com conteúdo inesperado

**Correção:**
1. Reveja a constante `EXECUTIVE_AGENT_INSTRUCTIONS` em `main.py`. Assegure que não foi truncada ou corrompida.
2. Verifique a temperatura do modelo (se configurável) - valores mais baixos geram respostas mais determinísticas.
3. Compare o modelo implantado (ex.: `gpt-4o` vs `gpt-4o-mini`) - modelos diferentes têm capacidades diferentes.

---

## 5. Erros de implantação

### 5.1 Autorização para pull do ACR

```
Error: AcrPullUnauthorized
```

**Causa raiz:** A identidade gerida do projeto Foundry não pode puxar a imagem do contentor do Azure Container Registry.

**Correção - passo a passo:**

1. Abra [https://portal.azure.com](https://portal.azure.com).
2. Procure **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** na barra de pesquisa superior.
3. Clique no registo associado ao seu projeto Foundry (normalmente no mesmo grupo de recursos).
4. Na navegação esquerda, clique em **Controlo de acesso (IAM)**.
5. Clique em **+ Adicionar** → **Adicionar atribuição de função**.
6. Procure **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** e selecione-a. Clique em **Seguinte**.
7. Selecione **Managed identity** → clique em **+ Selecionar membros**.
8. Encontre e selecione a identidade gerida do projeto Foundry.
9. Clique em **Selecionar** → **Rever + atribuir** → **Rever + atribuir**.

> Esta atribuição de função é normalmente configurada automaticamente pela extensão Foundry. Se vir este erro, a configuração automática pode ter falhado. Também pode tentar redeployar - a extensão pode tentar novamente.

### 5.2 Agente falha ao iniciar após implantação

**Sintomas:** Estado do contentor fica em "Pending" mais de 5 minutos ou mostra "Failed".

**Correção - passo a passo:**

1. Abra a barra lateral **Microsoft Foundry** no VS Code.
2. Clique no seu agente hospedado → selecione a versão.
3. No painel de detalhes, verifique **Detalhes do Contentor** → procure pela secção ou link **Logs**.
4. Leia os logs de arranque do contentor. Causas comuns:

| Mensagem do log | Causa | Correção |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Dependência em falta | Adicione ao `requirements.txt` e redeploy |
| `KeyError: 'PROJECT_ENDPOINT'` | Variável de ambiente em falta | Adicione a variável ao `agent.yaml` em `env:` |
| `OSError: [Errno 98] Address already in use` | Conflito de porta | Garanta que o `agent.yaml` tem `port: 8088` e só um processo usa essa porta |
| `ConnectionRefusedError` | Agente não começou a escutar | Verifique `main.py` - o chamado `from_agent_framework()` deve correr no arranque |

5. Corrija o problema e depois volte a implantar a partir do [Module 6](06-deploy-to-foundry.md).

### 5.3 Timeout na implantação

**Correção:**
1. Verifique a sua ligação à internet - o push Docker pode ser grande (>100MB na primeira implantação).
2. Se estiver atrás de um proxy corporativo, assegure que as definições de proxy do Docker Desktop estão configuradas: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Tente novamente - falhas de rede intermitentes podem causar erros temporários.

---

## 6. Referência rápida: papéis RBAC

| Papel | Escopo típico | O que concede |
|------|---------------|----------------|
| **Azure AI User** | Projeto | Ações de dados: construir, implantar e invocar agentes (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projeto ou Conta | Ações de dados + criação de projeto |
| **Azure AI Owner** | Conta | Acesso total + gestão de atribuições de função |
| **Azure AI Project Manager** | Projeto | Ações de dados + pode atribuir Azure AI User a outros |
| **Contributor** | Subscrição/GR | Ações de gestão (criar/apagar recursos). **NÃO inclui ações de dados** |
| **Owner** | Subscrição/GR | Ações de gestão + atribuição de funções. **NÃO inclui ações de dados** |
| **Reader** | Qualquer | Acesso de gestão só de leitura |

> **Conclusão:** `Owner` e `Contributor` não incluem ações de dados. Precisa sempre de um papel `Azure AI *` para operações de agente. O papel mínimo para este workshop é **Azure AI User** ao nível do **projeto**.

---

## 7. Lista de verificação para conclusão do workshop

Use isto como confirmação final de que completou tudo:

| # | Item | Módulo | Passou? |
|---|------|--------|---|
| 1 | Todos os pré-requisitos instalados e verificados | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit e extensões Foundry instalados | [01](01-install-foundry-toolkit.md) | |
| 3 | Projeto Foundry criado (ou projeto existente selecionado) | [02](02-create-foundry-project.md) | |
| 4 | Modelo implementado (ex., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Função de Utilizador Azure AI atribuída ao âmbito do projeto | [02](02-create-foundry-project.md) | |
| 6 | Projeto de agente alojado estruturado (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` configurado com PROJECT_ENDPOINT e MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instruções do agente personalizadas em main.py | [04](04-configure-and-code.md) | |
| 9 | Ambiente virtual criado e dependências instaladas | [04](04-configure-and-code.md) | |
| 10 | Agente testado localmente com F5 ou terminal (4 testes smoke aprovados) | [05](05-test-locally.md) | |
| 11 | Implantado no Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Estado do contentor mostra "Started" ou "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verificado no VS Code Playground (4 testes smoke aprovados) | [07](07-verify-in-playground.md) | |
| 14 | Verificado no Foundry Portal Playground (4 testes smoke aprovados) | [07](07-verify-in-playground.md) | |

> **Parabéns!** Se todos os itens estiverem assinalados, completou todo o workshop. Construiu um agente alojado do zero, testou-o localmente, implantou-o no Microsoft Foundry e validou-o em produção.

---

**Anterior:** [07 - Verificar no Playground](07-verify-in-playground.md) · **Início:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, tenha em conta que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autoritativa. Para informação crítica, recomenda-se a tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações erradas decorrentes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->