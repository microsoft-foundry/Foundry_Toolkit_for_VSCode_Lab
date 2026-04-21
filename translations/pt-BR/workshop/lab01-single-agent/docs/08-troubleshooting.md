# Módulo 8 - Solução de Problemas

Este módulo é um guia de referência para todo problema comum encontrado durante o workshop. Adicione aos favoritos - você voltará a ele sempre que algo der errado.

---

## 1. Erros de permissão

### 1.1 Permissão `agents/write` negada

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Causa principal:** Você não possui a função `Azure AI User` no nível do **projeto**. Este é o erro mais comum no workshop.

**Correção - passo a passo:**

1. Abra [https://portal.azure.com](https://portal.azure.com).
2. Na barra de pesquisa superior, digite o nome do seu **projeto Foundry** (por exemplo, `workshop-agents`).
3. **Crítico:** Clique no resultado que mostra o tipo **"Microsoft Foundry project"**, NÃO a conta pai/recurso hub. São recursos diferentes com escopos RBAC diferentes.
4. No menu lateral da página do projeto, clique em **Controle de acesso (IAM)**.
5. Clique na aba **Atribuições de função** para verificar se você já possui a função:
   - Procure seu nome ou e-mail.
   - Se `Azure AI User` já estiver listado → o erro tem outra causa (veja o passo 8 abaixo).
   - Se não listado → prossiga para adicioná-la.
6. Clique em **+ Adicionar** → **Adicionar atribuição de função**.
7. Na aba **Função**:
   - Pesquise por [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Selecione-a nos resultados.
   - Clique em **Avançar**.
8. Na aba **Membros**:
   - Selecione **Usuário, grupo ou principal de serviço**.
   - Clique em **+ Selecionar membros**.
   - Busque seu nome ou endereço de e-mail.
   - Selecione-se nos resultados.
   - Clique em **Selecionar**.
9. Clique em **Revisar + atribuir** → novamente em **Revisar + atribuir**.
10. **Aguarde 1-2 minutos** - alterações RBAC levam tempo para propagar.
11. Tente novamente a operação que falhou.

> **Por que Owner/Contributor não é suficiente:** O RBAC do Azure possui dois tipos de permissões - *ações de gerenciamento* e *ações de dados*. Owner e Contributor garantem ações de gerenciamento (criar recursos, editar configurações), mas operações do agente requerem a ação de dados `agents/write`, que está incluída somente nas funções `Azure AI User`, `Azure AI Developer` ou `Azure AI Owner`. Veja [docs de RBAC Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante provisionamento do recurso

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Causa principal:** Você não tem permissão para criar ou modificar recursos Azure nesta assinatura/grupo de recursos.

**Correção:**
1. Peça ao administrador da assinatura para atribuir a você a função **Contributor** no grupo de recursos onde seu projeto Foundry está localizado.
2. Alternativamente, peça que eles criem o projeto Foundry para você e concedam o papel **Azure AI User** no projeto.

### 1.3 `SubscriptionNotRegistered` para [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Causa principal:** A assinatura Azure não registrou o provedor de recursos necessário para o Foundry.

**Correção:**

1. Abra um terminal e execute:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Aguarde o registro ser concluído (pode levar de 1 a 5 minutos):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Saída esperada: `"Registered"`
3. Tente a operação novamente.

---

## 2. Erros Docker (somente se Docker estiver instalado)

> Docker é **opcional** para este workshop. Estes erros se aplicam somente se você tem o Docker Desktop instalado e a extensão Foundry tenta uma build local do container.

### 2.1 Docker daemon não está rodando

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Correção - passo a passo:**

1. **Encontre o Docker Desktop** no menu Iniciar (Windows) ou Aplicativos (macOS) e abra-o.
2. Aguarde a janela do Docker Desktop mostrar **"Docker Desktop está em execução"** - isso geralmente leva 30-60 segundos.
3. Procure pelo ícone da baleia do Docker na barra de sistema (Windows) ou barra de menu (macOS). Passe o mouse sobre ele para confirmar o status.
4. Verifique em um terminal:
   ```powershell
   docker info
   ```
   Se isto imprimir informações do sistema Docker (Versão do Servidor, Driver de Armazenamento, etc.) o Docker está rodando.
5. **Específico para Windows:** Se o Docker ainda não iniciar:
   - Abra o Docker Desktop → **Configurações** (ícone de engrenagem) → **Geral**.
   - Garanta que **Usar o mecanismo baseado em WSL 2** está marcado.
   - Clique em **Aplicar & Reiniciar**.
   - Se WSL 2 não estiver instalado, execute `wsl --install` no PowerShell com privilégios elevados e reinicie seu computador.
6. Tente o deploy novamente.

### 2.2 Build do Docker falha com erros de dependência

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Correção:**
1. Abra `requirements.txt` e verifique se todos os nomes dos pacotes estão escritos corretamente.
2. Assegure que a fixação de versões está correta:
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
4. Se estiver usando um índice de pacotes privado, garanta que o Docker tenha acesso de rede a ele.

### 2.3 Incompatibilidade da plataforma do container (Apple Silicon)

Se estiver fazendo deploy a partir de um Mac Apple Silicon (M1/M2/M3/M4), o container deve ser construído para `linux/amd64` porque o runtime de container do Foundry usa AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> O comando deploy da extensão Foundry trata isso automaticamente na maioria dos casos. Se você vir erros relacionados à arquitetura, construa manualmente com a flag `--platform` e contate a equipe Foundry.

---

## 3. Erros de autenticação

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) falha ao obter token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Causa principal:** Nenhuma das fontes de credenciais na cadeia `DefaultAzureCredential` tem um token válido.

**Correção - tente cada passo em ordem:**

1. **Relogue via Azure CLI** (correção mais comum):
   ```bash
   az login
   ```
   Uma janela do navegador se abrirá. Faça login e volte para o VS Code.

2. **Defina a assinatura correta:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Se esta não for a assinatura correta:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Relogue pelo VS Code:**
   - Clique no ícone **Contas** (ícone de pessoa) no canto inferior esquerdo do VS Code.
   - Clique no seu nome → **Sair**.
   - Clique no ícone Contas novamente → **Entrar na Microsoft**.
   - Complete o fluxo de login no navegador.

4. **Principal de serviço (somente cenários CI/CD):**
   - Defina estas variáveis de ambiente no seu `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Então reinicie seu processo de agente.

5. **Verifique o cache do token:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Se falhar, seu token CLI expirou. Rode `az login` novamente.

### 3.2 Token funciona localmente mas não no deploy hospedado

**Causa principal:** O agente hospedado usa uma identidade gerenciada do sistema, diferente das suas credenciais pessoais.

**Correção:** Este comportamento é esperado - a identidade gerenciada é provisionada automaticamente durante o deploy. Se o agente hospedado ainda obtiver erros de autenticação:
1. Verifique que a identidade gerenciada do projeto Foundry tem acesso ao recurso Azure OpenAI.
2. Confirme que `PROJECT_ENDPOINT` em `agent.yaml` está correto.

---

## 4. Erros de modelo

### 4.1 Implantação do modelo não encontrada

```
Error: Model deployment not found / The specified deployment does not exist
```

**Correção - passo a passo:**

1. Abra seu arquivo `.env` e anote o valor de `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Abra a barra lateral **Microsoft Foundry** no VS Code.
3. Expanda seu projeto → **Implantações de Modelos**.
4. Compare o nome da implantação listado lá com o valor no seu `.env`.
5. O nome é **case-sensitive** - `gpt-4o` é diferente de `GPT-4o`.
6. Se não corresponderem, atualize seu `.env` para usar exatamente o nome mostrado na barra lateral.
7. Para deploy hospedado, atualize também `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Modelo responde com conteúdo inesperado

**Correção:**
1. Revise a constante `EXECUTIVE_AGENT_INSTRUCTIONS` em `main.py`. Certifique-se de que não foi truncada ou corrompida.
2. Verifique a configuração da temperatura do modelo (se configurável) - valores mais baixos geram saídas mais determinísticas.
3. Compare o modelo implantado (ex., `gpt-4o` vs `gpt-4o-mini`) - modelos diferentes têm capacidades distintas.

---

## 5. Erros de implantação

### 5.1 Autorização para pull do ACR

```
Error: AcrPullUnauthorized
```

**Causa principal:** A identidade gerenciada do projeto Foundry não consegue puxar a imagem do container do Azure Container Registry.

**Correção - passo a passo:**

1. Abra [https://portal.azure.com](https://portal.azure.com).
2. Pesquise por **[Registros de contêiner](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** na barra de pesquisa superior.
3. Clique no registro associado ao seu projeto Foundry (normalmente está no mesmo grupo de recursos).
4. No menu lateral, clique em **Controle de acesso (IAM)**.
5. Clique em **+ Adicionar** → **Adicionar atribuição de função**.
6. Pesquise por **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** e selecione-o. Clique em **Avançar**.
7. Selecione **Identidade gerenciada** → clique em **+ Selecionar membros**.
8. Localize e selecione a identidade gerenciada do projeto Foundry.
9. Clique em **Selecionar** → **Revisar + atribuir** → **Revisar + atribuir**.

> Essa atribuição de função normalmente é configurada automaticamente pela extensão Foundry. Se você vir este erro, a configuração automática pode ter falhado. Você também pode tentar redeployar - a extensão pode tentar novamente a configuração.

### 5.2 Agente falha ao iniciar após deploy

**Sintomas:** Status do container fica "Pendente" por mais de 5 minutos ou mostra "Falhou".

**Correção - passo a passo:**

1. Abra a barra lateral **Microsoft Foundry** no VS Code.
2. Clique no seu agente hospedado → selecione a versão.
3. No painel de detalhes, verifique **Detalhes do container** → procure a seção ou link de **Logs**.
4. Leia os logs de inicialização do container. Causas comuns:

| Mensagem no log | Causa | Correção |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Dependência ausente | Adicione-a no `requirements.txt` e redeploy |
| `KeyError: 'PROJECT_ENDPOINT'` | Variável de ambiente ausente | Adicione a variável em `agent.yaml` sob `env:` |
| `OSError: [Errno 98] Address already in use` | Conflito de porta | Garanta que `agent.yaml` tenha `port: 8088` e apenas um processo a use |
| `ConnectionRefusedError` | Agente não começou a escutar | Confira `main.py` - a chamada `from_agent_framework()` deve rodar na inicialização |

5. Corrija o problema, então redeploy a partir do [Módulo 6](06-deploy-to-foundry.md).

### 5.3 Deploy expira

**Correção:**
1. Verifique sua conexão com a internet - o push do Docker pode ser grande (>100MB no primeiro deploy).
2. Se atrás de um proxy corporativo, certifique-se que as configurações proxy do Docker Desktop estão configuradas: **Docker Desktop** → **Configurações** → **Recursos** → **Proxies**.
3. Tente novamente - falhas de rede temporárias podem causar erros transitórios.

---

## 6. Referência rápida: funções RBAC

| Função | Escopo típico | O que concede |
|------|---------------|--------------|
| **Azure AI User** | Projeto | Ações de dados: build, deploy e invocação de agentes (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projeto ou Conta | Ações de dados + criação de projeto |
| **Azure AI Owner** | Conta | Acesso completo + gerenciamento de atribuições de função |
| **Azure AI Project Manager** | Projeto | Ações de dados + pode atribuir Azure AI User a outros |
| **Contributor** | Assinatura/GR | Ações de gerenciamento (criar/deletar recursos). **NÃO inclui ações de dados** |
| **Owner** | Assinatura/GR | Ações de gerenciamento + atribuição de função. **NÃO inclui ações de dados** |
| **Reader** | Qualquer | Acesso somente leitura ao gerenciamento |

> **Ponto chave:** `Owner` e `Contributor` **NÃO** incluem ações de dados. Você sempre precisa de um papel `Azure AI *` para operações do agente. A função mínima para este workshop é **Azure AI User** no escopo **projeto**.

---

## 7. Checklist de conclusão do workshop

Use isto como confirmação final de que você completou tudo:

| # | Item | Módulo | Aprovado? |
|---|------|--------|---|
| 1 | Todos os pré-requisitos instalados e verificados | [00](00-prerequisites.md) | |
| 2 | Toolkit Foundry e extensões Foundry instaladas | [01](01-install-foundry-toolkit.md) | |
| 3 | Projeto Foundry criado (ou projeto existente selecionado) | [02](02-create-foundry-project.md) | |
| 4 | Modelo implantado (por exemplo, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Função de usuário Azure AI atribuída no escopo do projeto | [02](02-create-foundry-project.md) | |
| 6 | Estrutura do projeto do agente hospedado criada (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` configurado com PROJECT_ENDPOINT e MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instruções do agente personalizadas em main.py | [04](04-configure-and-code.md) | |
| 9 | Ambiente virtual criado e dependências instaladas | [04](04-configure-and-code.md) | |
| 10 | Agente testado localmente com F5 ou terminal (4 testes rápidos aprovados) | [05](05-test-locally.md) | |
| 11 | Implantado no Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Status do container mostra "Started" ou "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verificado no VS Code Playground (4 testes rápidos aprovados) | [07](07-verify-in-playground.md) | |
| 14 | Verificado no Foundry Portal Playground (4 testes rápidos aprovados) | [07](07-verify-in-playground.md) | |

> **Parabéns!** Se todos os itens estiverem marcados, você completou todo o workshop. Você criou um agente hospedado do zero, testou localmente, implantou no Microsoft Foundry e validou em produção.

---

**Anterior:** [07 - Verificar no Playground](07-verify-in-playground.md) · **Início:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos empenhemos pela precisão, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações equivocadas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->