# Módulo 7 - Verificar no Playground

⏱️ ~10 min

Neste módulo, testa o seu fluxo de trabalho multi-agente implementado no VS Code e no Portal Foundry, confirmando que o agente se comporta da mesma forma que nos testes locais.

---

## Porque testar de novo após a implementação?

O ambiente hospedado difere do local em alguns aspetos importantes:

| | Local | Hospedado |
|--|-------|--------|
| **Identidade** | O seu login pessoal (`DefaultAzureCredential`) | Identidade Entra dedicada por agente (auto-provisionada na altura da implementação) |
| **Endpoint** | `http://localhost:8088/responses` | URL gerida pelo Serviço Foundry Agent |
| **Rede** | A sua máquina → Azure OpenAI + MCP | Backbone Azure (latência inferior) |

Uma variável de ambiente mal configurada, problema de RBAC, ou chamada MCP bloqueada surgirá aqui primeiro.

---

## Opção A: Testar no VS Code Playground (recomendado primeiro)

### Passo 1: Navegue até ao seu agente hospedado

1. Clique no ícone **Foundry Toolkit** na Barra de Atividades.
2. Expanda o seu projeto → **Hosted Agents (Preview)** → encontre o seu agente.

![Foundry Toolkit sidebar mostrando Hosted Agents (Preview) com resume-job-fit-evaluator e as suas versões implementadas](../../../../../translated_images/pt-PT/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Passo 2: Selecionar uma versão

1. Clique no agente para expandir as suas versões.
2. Clique em `v1` → verifique se o estado é **ativo** (a barra lateral pode mostrar "Running" ou "Started" - ambos indicam o mesmo estado pronto).

### Passo 3: Abrir o Playground

1. Clique em **Playground** (ou clique com o botão direito na versão → **Open in Playground**).
2. Abre uma janela de chat numa aba do VS Code.

### Passo 4: Execute os seus testes rápidos (smoke tests)

Use os mesmos 3 testes do [Módulo 5](05-test-locally.md). Escreva cada mensagem na caixa de entrada do Playground e pressione **Send** (ou **Enter**).

#### Teste 1 - Currículo completo + JD (fluxo standard)

Cole o prompt completo de currículo + JD do Módulo 5, Teste 1 (Jane Doe + Senior Cloud Engineer na Contoso Ltd).

**Esperado:**
- Pontuação de adequação com cálculo detalhado (escala de 100 pontos)
- Secção de Competências Correspondidas
- Secção de Competências em Falta
- **Um cartão de lacuna por competência em falta** com URLs da Microsoft Learn
- Roteiro de aprendizagem com cronograma

#### Teste 2 - Teste rápido curto (entrada mínima)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Esperado:**
- Pontuação de adequação inferior (< 40)
- Avaliação honesta com caminho de aprendizagem faseado
- Vários cartões de lacunas (AWS, Kubernetes, Terraform, CI/CD, lacuna de experiência)

#### Teste 3 - Candidato de alta adequação

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Esperado:**
- Pontuação alta de adequação (≥ 80)
- Foco na prontidão para entrevista e refinamento
- Poucos ou nenhuns cartões de lacuna
- Cronograma curto focado na preparação

### Passo 5: Compare com os resultados locais

Abra as suas notas ou a aba do navegador do Módulo 5 onde guardou as respostas locais. Para cada teste:

- A resposta tem a **mesma estrutura** (pontuação de adequação, cartões de lacunas, roteiro)?
- Segue a **mesma rubrica de pontuação** (desagregação em 100 pontos)?
- As **URLs da Microsoft Learn** ainda estão presentes nos cartões de lacunas?
- Há **um cartão de lacuna por competência em falta** (não truncado)?

> **Diferenças menores na redação são normais** - o modelo não é determinístico. Concentre-se na estrutura, consistência da pontuação e uso das ferramentas MCP.

---

## Opção B: Testar no Portal Foundry

O [Portal Foundry](https://ai.azure.com) fornece um playground baseado na web útil para partilhar com colegas de equipa ou stakeholders.

### Passo 1: Abra o Portal Foundry

1. Abra o seu navegador e navegue para [https://ai.azure.com](https://ai.azure.com).
2. Inicie sessão com a mesma conta Azure que tem usado durante o workshop.

### Passo 2: Navegue até ao seu projeto

1. Na página inicial, procure **Projetos recentes** na barra lateral esquerda.
2. Clique no nome do seu projeto (ex., `workshop-agents`).
3. Se não o vir, clique em **Todos os projetos** e pesquise.

### Passo 3: Encontre o seu agente implementado

1. Na navegação esquerda do projeto, clique em **Build** → **Agents** (ou procure a secção **Agents**).
2. Deve ver uma lista de agentes. Encontre o seu agente implementado (ex., `resume-job-fit-evaluator`).
3. Clique no nome do agente para abrir a página de detalhes.

### Passo 4: Abrir o Playground

1. Na página de detalhes do agente, olhe para a barra de ferramentas superior.
2. Clique em **Open in playground** (ou **Try in playground**).
3. Abre uma interface de chat.

### Passo 5: Execute os mesmos testes rápidos

Repita os 3 testes da secção Playground do VS Code acima. Compare cada resposta com os resultados locais (Módulo 5) e os do Playground VS Code (Opção A acima).

---

## Verificação específica multi-agente

Para além da correção básica, verifique estes comportamentos específicos multi-agente:

### Execução da ferramenta MCP

| Verificar | Como verificar | Condição de aprovação |
|-------|---------------|----------------|
| Chamadas MCP bem-sucedidas | Cartões de lacuna contêm URLs `learn.microsoft.com` | URLs reais, não mensagens de fallback |
| Múltiplas chamadas MCP | Cada lacuna de Alta/Média prioridade tem recursos | Não apenas o primeiro cartão de lacuna |
| Fallback MCP funciona | Se faltarem URLs, verifique texto de fallback | Agente ainda produz cartões de lacunas (com ou sem URLs) |

### Coordenação dos agentes

| Verificar | Como verificar | Condição de aprovação |
|-------|---------------|----------------|
| Todos os 4 agentes correram | Saída contém pontuação de adequação E cartões de lacunas | Pontuação do MatchingAgent, cartões do GapAnalyzer |
| Execução sequencial | Tempo de resposta razoável (< 2 min) | Se > 3 min, verifique erros no log do terminal |
| Integridade do fluxo de dados | Cartões de lacunas referenciam competências do relatório de matching | Nenhuma competência alucinada que não esteja no JD |

---

## Rubrica de validação

Use esta rubrica para avaliar o comportamento hospedado do seu fluxo multi-agente:

| # | Critério | Condição de aprovação | Aprovado? |
|---|----------|---------------|-------|
| 1 | **Correção funcional** | Agente responde a currículo + JD com pontuação e análise de lacunas | |
| 2 | **Consistência de pontuação** | Pontuação usa escala de 100 pontos com cálculo detalhado | |
| 3 | **Completude dos cartões de lacunas** | Um cartão por competência em falta (não truncado nem combinado) | |
| 4 | **Integração da ferramenta MCP** | Cartões de lacunas incluem URLs reais da Microsoft Learn | |
| 5 | **Consistência estrutural** | Estrutura da saída corresponde entre execuções local e hospedada | |
| 6 | **Tempo de resposta** | Agente hospedado responde dentro de 2 minutos para avaliação completa | |
| 7 | **Sem erros** | Sem erros HTTP 500, timeouts ou respostas vazias | |

> Um "pass" significa que todos os 7 critérios são cumpridos para os 3 testes rápidos em pelo menos um playground (VS Code ou Portal).

---

## Resolução de problemas de playground

| Sintoma | Causa provável | Correção |
|---------|-------------|-----|
| Playground não carrega | Contentor não está no estado `active` | Volte ao [Módulo 6](06-deploy-to-foundry.md), verifique o estado da implementação. Aguarde se estiver `creating` |
| Agente retorna resposta vazia | Nome da implementação do modelo incorreto | Verifique `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` corresponde ao seu modelo implementado |
| Agente retorna mensagem de erro | Permissão [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) em falta | Atribua **[Foundry User](https://aka.ms/foundry-ext-project-role)** (anteriormente Azure AI User) ao âmbito do projeto |
| Sem URLs da Microsoft Learn nos cartões de lacuna | MCP bloqueado ou servidor MCP indisponível | Verifique se o contentor consegue aceder a `learn.microsoft.com`. Veja [Módulo 8](08-troubleshooting.md) |
| Apenas 1 cartão de lacuna (truncado) | Instruções do GapAnalyzer sem bloco "CRITICAL" | Reveja [Módulo 3, Passo 2.4](03-configure-agents.md) |
| Pontuação de adequação muito diferente do local | Modelo ou instruções diferentes implementados | Compare variáveis de ambiente `agent.yaml` com `.env` local. Reimplemente se necessário |
| "Agente não encontrado" no Portal | Implementação ainda a propagar ou falhou | Aguarde 2 minutos, atualize. Se continuar em falta, reimplemente pelo [Módulo 6](06-deploy-to-foundry.md) |

---

### Ponto de verificação

- [ ] Testado agente no VS Code Playground - todos os 3 testes rápidos passaram
- [ ] Testado agente no Playground do [Portal Foundry](https://ai.azure.com) - todos os 3 testes rápidos passaram
- [ ] Respostas com consistência estrutural face aos testes locais (pontuação, cartões, roteiro)
- [ ] URLs da Microsoft Learn presentes nos cartões de lacunas (ferramenta MCP a funcionar no ambiente hospedado)
- [ ] Um cartão de lacuna por competência em falta (sem truncação)
- [ ] Sem erros ou timeouts durante os testes
- [ ] Rubrica de validação completa (todos os 7 critérios aprovados)

---

**Anterior:** [06 - Deploy to Foundry](06-deploy-to-foundry.md) · **Seguinte:** [08 - Troubleshooting →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->