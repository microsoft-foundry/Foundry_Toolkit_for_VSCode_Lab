# Módulo 5 - Implantar no Serviço Agent Foundry

⏱️ ~10 min

> ⚠️ **Usuários do Caminho B:** Este módulo requer uma assinatura Foundry. Se você estiver usando Foundry Local, pule para [Módulo 07 - Resumo](07-summary.md). Você concluiu com sucesso o fluxo de trabalho de desenvolvimento local!

Neste módulo, você implanta seu agente testado localmente na Microsoft Foundry como um **Agente Hospedado**. A implantação constrói uma imagem de contêiner, envia para o Azure Container Registry e inicia o agente na infraestrutura gerenciada do Foundry.

### Pipeline de implantação

```mermaid
flowchart LR
    A["Dockerfile
    main.py"] -->|docker build| B["Container
    Image"]
    B -->|docker push| C["Azure Container
    Registry (ACR)"]
    C -->|register agent| D["Foundry Agent
    Service"]
    D -->|start container| E["/responses
    endpoint ready"]

    style A fill:#9B59B6,color:#fff
    style B fill:#9B59B6,color:#fff
    style C fill:#E67E22,color:#fff
    style D fill:#3498DB,color:#fff
    style E fill:#27AE60,color:#fff
```

---

## Verificação de pré-requisitos

Antes de implantar, verifique:

- [ ] O agente passa por todos os 3 cenários locais do [Módulo 04](04-test-locally.md)
- [ ] Você possui a função **Usuário do Azure AI** no nível do projeto ([Módulo 01, Atribuir RBAC](01-setup.md#deploy-a-model--assign-rbac))
- [ ] Você está conectado no Azure no VS Code (ícone de Contas mostra seu nome)

---

## Passo 1: Inicie a implantação

### Opção A: Implantar pelo Agent Inspector (recomendado)

Se o Agent Inspector estiver aberto (após testes):
1. Clique no botão **Deploy** no canto superior direito (ícone de nuvem ↑).

### Opção B: Implantar pelo Command Palette

1. Pressione `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent**.

---

## Passo 2: Configure a implantação

O assistente solicita:

![Configuração do Projeto](../../../../../translated_images/pt-BR/05-foundry-project-setup.ca6ad16a6484e054.webp)

| Solicitação | Seleção |
|--------|-----------|
| **Assinatura** | Sua Assinatura do Azure |
| **Projeto alvo** | Seu projeto Foundry (ex., `workshop-agents`) |

Clique em **próximo** para configurar seu agente.

![Configuração básica](../../../../../translated_images/pt-BR/05-configure-basics.4d5f3d6b0d96f033.webp)

| Solicitação | Seleção |
|--------|-----------|
| **Método de implantação** | Contêiner |
| **Registro de contêiner** | **ACR padrão** (Microsoft Foundry cria e gerencia um para você) |
| **Implantar em** | Novo Agente (nome, `executive-summary-agent`) |

Clique em **próximo** para revisar e implantar seu agente.

![Revisar e implantar](../../../../../translated_images/pt-BR/05-review-deploy.12b449d426bff886.webp)

| Solicitação | Seleção |
|--------|-----------|
| **CPU e memória** | **0,5 núcleos de CPU, 1,0 Gi de memória** (padrão - suficiente para o workshop) |

---

## Passo 3: Implantar e monitorar

1. Clique em **Deploy**.
2. Observe o painel **Output** (selecione **Microsoft Foundry** no dropdown).
3. A implantação passa pelas seguintes etapas:
   - **Docker build** - constrói o contêiner a partir do seu Dockerfile
   - **Docker push** - envia a imagem para o ACR (1–3 min na primeira implantação)
   - **Registro do agente** - cria agente hospedado no Foundry
   - **Início do contêiner** - inicia com identidade gerenciada pelo sistema

4. Quando concluído, aparece uma notificação:
   > **executive-summary-agent foi implantado com sucesso.** `View logs` `Run agent`

5. Clique em **Run agent** para abrir o Agent Playground.

![Sucesso na implantação mostrando Agent Playground com status em execução](../../../../../translated_images/pt-BR/05-deployed-asset.b59e6a5eef31c0b1.webp)

### Valores de status da implantação

| Status | Significado |
|--------|---------|
| **Running** | Contêiner pronto, agente respondendo |
| **Pending** | Contêiner iniciando - aguarde 30–60 segundos |
| **Failed** | Verifique os logs (veja solução de problemas abaixo) |

---

## Erros comuns na implantação

| Erro | Causa raiz | Correção |
|-------|-----------|-----|
| `agents/write` permissão negada | Falta o papel **Azure AI User** no nível do projeto | [Módulo 01, Atribuir RBAC](01-setup.md#deploy-a-model--assign-rbac) |
| Docker não está em execução | Docker Desktop não iniciado | Inicie o Docker Desktop → verifique `docker info` |
| Autorização ACR | Identidade gerenciada não consegue puxar a imagem | Veja [Módulo 08 - Solução de Problemas](08-troubleshooting.md) |

---

### ✅ Ponto de verificação

- [ ] Implantação concluída sem erros
- [ ] Agente aparece na aba **Agente Hospedado** quando você clica em **Agentes** sob seu projeto na barra lateral do Foundry Toolkit
- [ ] O status do contêiner mostra **Executando**
- [ ] Aba Playground do Agente aberta mostrando detalhes do agente e URL do endpoint

---

**Anterior:** [04 - Testar Localmente](04-test-locally.md) · **Próximo:** [06 - Verificar no Playground →](06-verify-in-playground.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->