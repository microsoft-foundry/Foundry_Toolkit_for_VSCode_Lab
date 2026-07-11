# Módulo 7 - Verificar no Playground

⏱️ ~10 min

Neste módulo, você testa seu fluxo de trabalho multiagente implantado no VS Code e no Foundry Portal, confirmando que o agente se comporta da mesma forma que nos testes locais.

---

## Por que testar novamente após a implantação?

O ambiente hospedado difere do local em alguns aspectos importantes:

| | Local | Hospedado |
|--|-------|--------|
| **Identidade** | Seu login pessoal (`DefaultAzureCredential`) | Identidade Entra dedicada por agente (auto-provisionada na implantação) |
| **Endpoint** | `http://localhost:8088/responses` | URL gerenciada pelo Foundry Agent Service |
| **Rede** | Sua máquina → Azure OpenAI + MCP | Backbone Azure (menor latência) |

Uma variável de ambiente mal configurada, problema de RBAC ou chamada MCP bloqueada apareceria aqui primeiro.

---

## Opção A: Testar no VS Code Playground (recomendado primeiro)

### Passo 1: Navegar até seu agente hospedado

1. Clique no ícone **Foundry Toolkit** na Barra de Atividades.
2. Expanda seu projeto → **Hosted Agents (Preview)** → encontre seu agente.

![Foundry Toolkit sidebar mostrando Hosted Agents (Preview) com resume-job-fit-evaluator e suas versões implantadas](../../../../../translated_images/pt-BR/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Passo 2: Selecionar uma versão

1. Clique no agente para expandir suas versões.
2. Clique em `v1` → verifique se o status está **ativo** (a barra lateral pode mostrar "Running" ou "Started" - ambos indicam o mesmo estado pronto).

### Passo 3: Abrir o Playground

1. Clique em **Playground** (ou clique com o botão direito na versão → **Open in Playground**).
2. Uma janela de bate-papo abre em uma aba do VS Code.

### Passo 4: Executar seus testes básicos

Use os mesmos 3 testes do [Módulo 5](05-test-locally.md). Digite cada mensagem na caixa de entrada do Playground e pressione **Enviar** (ou **Enter**).

#### Teste 1 - Currículo completo + JD (fluxo padrão)

Cole o prompt do currículo completo + JD do Módulo 5, Teste 1 (Jane Doe + Engenheira Sênior de Nuvem na Contoso Ltd).

**Esperado:**
- Pontuação de encaixe com detalhamento matemático (escala de 100 pontos)
- Seção de habilidades correspondentes
- Seção de habilidades ausentes
- **Um cartão de lacuna por habilidade ausente** com URLs do Microsoft Learn
- Roteiro de aprendizado com cronograma

#### Teste 2 - Teste rápido curto (entrada mínima)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Esperado:**
- Pontuação de encaixe baixa (< 40)
- Avaliação honesta com plano de aprendizado em etapas
- Vários cartões de lacuna (AWS, Kubernetes, Terraform, CI/CD, lacuna de experiência)

#### Teste 3 - Candidato de alto encaixe

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Esperado:**
- Pontuação de encaixe alta (≥ 80)
- Foco na preparação para entrevista e refinamento
- Poucos ou nenhum cartão de lacuna
- Cronograma curto focado na preparação

### Passo 5: Comparar com resultados locais

Abra suas anotações ou aba do navegador do Módulo 5 onde salvou as respostas locais. Para cada teste:

- A resposta tem a **mesma estrutura** (pontuação de encaixe, cartões de lacuna, roteiro)?
- Segue a **mesma rubrica de pontuação** (detalhamento de 100 pontos)?
- As **URLs do Microsoft Learn** ainda estão presentes nos cartões de lacuna?
- Há **um cartão de lacuna por habilidade ausente** (não truncado)?

> **Diferenças menores na redação são normais** - o modelo é não determinístico. Foque na estrutura, consistência da pontuação e uso da ferramenta MCP.

---

## Opção B: Testar no Foundry Portal

O [Foundry Portal](https://ai.azure.com) oferece um playground baseado na web útil para compartilhamento com colegas ou partes interessadas.

### Passo 1: Abrir o Foundry Portal

1. Abra seu navegador e acesse [https://ai.azure.com](https://ai.azure.com).
2. Faça login com a mesma conta Azure que você usou durante o workshop.

### Passo 2: Navegar até seu projeto

1. Na página inicial, procure **Projetos recentes** na barra lateral esquerda.
2. Clique no nome do seu projeto (ex.: `workshop-agents`).
3. Se não encontrar, clique em **Todos os projetos** e pesquise por ele.

### Passo 3: Encontrar seu agente implantado

1. Na navegação à esquerda do projeto, clique em **Build** → **Agents** (ou procure pela seção **Agents**).
2. Você deve ver uma lista de agentes. Encontre seu agente implantado (ex.: `resume-job-fit-evaluator`).
3. Clique no nome do agente para abrir a página de detalhes.

### Passo 4: Abrir o Playground

1. Na página de detalhes do agente, olhe na barra de ferramentas superior.
2. Clique em **Open in playground** (ou **Try in playground**).
3. Uma interface de bate-papo será aberta.

### Passo 5: Executar os mesmos testes básicos

Repita os 3 testes do Playground do VS Code acima. Compare cada resposta tanto com os resultados locais (Módulo 5) quanto com os resultados no Playground do VS Code (Opção A acima).

---

## Verificação específica para multi-agentes

Além da correção básica, verifique estes comportamentos específicos de multi-agentes:

### Execução da ferramenta MCP

| Verificar | Como verificar | Condição de aprovação |
|-------|---------------|----------------|
| Chamadas MCP bem-sucedidas | Cartões de lacuna contêm URLs `learn.microsoft.com` | URLs reais, não mensagens fallback |
| Múltiplas chamadas MCP | Cada lacuna de prioridade Alta/Média tem recursos | Não apenas o primeiro cartão de lacuna |
| Funcionamento do fallback MCP | Se URLs faltam, verificar texto fallback | Agente ainda produz cartões de lacuna (com ou sem URLs) |

### Coordenação dos agentes

| Verificar | Como verificar | Condição de aprovação |
|-------|---------------|----------------|
| Todos os 4 agentes foram executados | Saída contém pontuação de encaixe E cartões de lacuna | Pontuação vem do MatchingAgent, cartões do GapAnalyzer |
| Execução sequencial | Tempo de resposta razoável (< 2 min) | Se > 3 min, verificar erros no log do terminal |
| Integridade do fluxo de dados | Cartões de lacuna referenciam habilidades do relatório de encaixe | Sem habilidades alucinadas que não estão no JD |

---

## Rubrica de validação

Use esta rubrica para avaliar o comportamento hospedado do seu fluxo de trabalho multi-agente:

| # | Critério | Condição de aprovação | Passou? |
|---|----------|---------------|-------|
| 1 | **Correção funcional** | Agente responde a currículo + JD com pontuação de encaixe e análise de lacunas | |
| 2 | **Consistência na pontuação** | Pontuação de encaixe usa escala de 100 pontos com detalhamento matemático | |
| 3 | **Completude dos cartões de lacuna** | Um cartão por habilidade ausente (não truncado ou combinado) | |
| 4 | **Integração da ferramenta MCP** | Cartões de lacuna incluem URLs reais do Microsoft Learn | |
| 5 | **Consistência estrutural** | Estrutura da saída corresponde entre execuções locais e hospedadas | |
| 6 | **Tempo de resposta** | Agente hospedado responde em até 2 minutos para avaliação completa | |
| 7 | **Sem erros** | Sem erros HTTP 500, timeouts ou respostas vazias | |

> Um "pass" significa que os 7 critérios são atendidos para os 3 testes básicos em pelo menos um playground (VS Code ou Portal).

---

## Solução de problemas no playground

| Sintoma | Causa provável | Correção |
|---------|-------------|-----|
| Playground não carrega | Container não está em estado `active` | Volte ao [Módulo 6](06-deploy-to-foundry.md), verifique o status da implantação. Aguarde se estiver `creating` |
| Agente retorna resposta vazia | Nome da implantação do modelo incompatível | Verifique em `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` se confere com seu modelo implantado |
| Agente retorna mensagem de erro | Permissão [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ausente | Atribua **[Usuário Foundry](https://aka.ms/foundry-ext-project-role)** (anteriormente Azure AI User) no escopo do projeto |
| URLs do Microsoft Learn ausentes nos cartões de lacuna | MCP outbound bloqueado ou servidor MCP indisponível | Verifique se o container pode acessar `learn.microsoft.com`. Veja [Módulo 8](08-troubleshooting.md) |
| Apenas 1 cartão de lacuna (truncado) | Instruções do GapAnalyzer sem o bloco "CRITICAL" | Revise [Módulo 3, Passo 2.4](03-configure-agents.md) |
| Pontuação de encaixe muito diferente do local | Modelo ou instruções diferentes implantadas | Compare variáveis de ambiente em `agent.yaml` com `.env` local. Reimplante se necessário |
| "Agente não encontrado" no Portal | Implantação ainda propagando ou falhou | Aguarde 2 minutos, atualize a página. Se continuar ausente, reimplante pelo [Módulo 6](06-deploy-to-foundry.md) |

---

### Ponto de verificação

- [ ] Testei o agente no VS Code Playground - todos os 3 testes básicos foram aprovados
- [ ] Testei o agente no Playground do [Foundry Portal](https://ai.azure.com) - todos os 3 testes básicos foram aprovados
- [ ] As respostas são estruturalmente consistentes com o teste local (pontuação de encaixe, cartões de lacuna, roteiro)
- [ ] URLs do Microsoft Learn estão presentes nos cartões de lacuna (ferramenta MCP funcionando no ambiente hospedado)
- [ ] Um cartão de lacuna por habilidade ausente (sem truncamento)
- [ ] Sem erros ou timeouts durante os testes
- [ ] Rubrica de validação concluída (todos os 7 critérios aprovados)

---

**Anterior:** [06 - Implantar no Foundry](06-deploy-to-foundry.md) · **Próximo:** [08 - Solução de problemas →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->