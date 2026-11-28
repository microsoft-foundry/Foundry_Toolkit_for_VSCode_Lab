# Módulo 4 - Padrões de Orquestração

⏱️ ~10 min

Neste módulo, explora os padrões de orquestração usados no Avaliador de Adequação de Emprego por Currículo e aprende a ler, modificar e expandir o gráfico do fluxo de trabalho. Compreender estes padrões é essencial para depurar problemas de fluxo de dados e construir os seus próprios [fluxos de trabalho multi-agente](https://learn.microsoft.com/agent-framework/workflows/).

---

## Padrão 1: Cadeia sequencial

O padrão fundamental no fluxo de trabalho é uma **cadeia sequencial** - a saída de cada agente alimenta diretamente o seguinte.

```mermaid
flowchart LR
    RP[Resume Parser] --> JD[JD Agent]
    JD --> MA[Matching Agent]
    MA --> GA[Gap Analyzer]
```

Em código, cada chamada `add_edge()` cria um passo na cadeia:

```python
.add_edge(resume_executor, jd_executor)       # ResumeParser output → JD Agent
.add_edge(jd_executor, matching_executor)     # JD Agent output → MatchingAgent
.add_edge(matching_executor, gap_executor)    # MatchingAgent output → GapAnalyzer
```

> **Porquê sequencial, e não fan-out/fan-in?** `WorkflowBuilder` usa **semântica OU** para as arestas de entrada: um executor a jusante é ativado assim que **qualquer** antecessor completa. Se `matching_executor` tivesse duas arestas de entrada (de `resume_executor` e `jd_executor`), acionaria duas vezes - uma quando ResumeParser termina e outra quando JD Agent termina - fazendo com que GapAnalyzer também execute duas vezes e a saída apareça em duplicado. A pipeline sequencial evita isto completamente.

## Padrão 2: Relevo de Conteúdo

Como `context_mode="last_agent"` significa que cada executor vê apenas a **saída do seu antecessor direto**, os agentes numa cadeia sequencial têm de passar explicitamente para a frente qualquer dado necessário para agentes a jusante.

Neste fluxo de trabalho:
- **ResumeParser** copia o JD na íntegra para `[JOB DESCRIPTION PASS-THROUGH]` (para que o JD Agent possa encontrá-lo).
- **JD Agent** copia o `[PARSED RESUME]` na íntegra para `[PARSED RESUME PASS-THROUGH]` (para que MatchingAgent possa comparar ambos os perfis).

```
ResumeParser output
└─ [PARSED RESUME]               ← extracted by JD Agent
└─ [JOB DESCRIPTION PASS-THROUGH] ← extracted by JD Agent

JD Agent output
└─ [JD REQUIREMENTS]             ← extracted by MatchingAgent
└─ [PARSED RESUME PASS-THROUGH]  ← extracted by MatchingAgent
```

Cada secção de relevo deve ser copiada **na íntegra** – resumir ou parafrasear quebra o agente a jusante que depende dela.

---

## O gráfico completo

Combinando os padrões de cadeia sequencial e relevo de conteúdo produz-se o fluxo de trabalho completo:

```mermaid
flowchart LR
    U[User Input] --> RP[Resume Parser]
    RP --> JD[JD Agent]
    JD --> MA[Matching Agent]
    MA --> GA[Gap Analyzer + MCP]
    GA --> O[Final Output]
```

O Inspetor de Agentes mostra esta mesma estrutura do gráfico quando o agente está a correr localmente. Consulte [Módulo 5 - Testar Localmente](05-test-locally.md) para imagens.

---

## A ler o código do WorkflowBuilder

O gráfico do fluxo de trabalho é construído na função `main()` em [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py). As três chamadas `add_edge()` constroem a pipeline sequencial:

| # | Aresta | Efeito |
|---|------|--------|
| 1 | `resume_executor → jd_executor` | JD Agent recebe `[PARSED RESUME]` + `[JOB DESCRIPTION PASS-THROUGH]` |
| 2 | `jd_executor → matching_executor` | MatchingAgent recebe `[JD REQUIREMENTS]` + `[PARSED RESUME PASS-THROUGH]` |
| 3 | `matching_executor → gap_executor` | GapAnalyzer recebe relatório de adequação + lista de lacunas |

---

## Modificar o gráfico

### Adicionar um novo agente

Para adicionar um quinto agente (ex., um **InterviewPrepAgent** após o GapAnalyzer):

1. Defina uma constante `INTERVIEW_PREP_INSTRUCTIONS`.
2. Crie os objetos `Agent` + `AgentExecutor` (mesmo padrão que os quatro existentes).
3. Adicione `.add_edge(gap_executor, interview_exec)` em `WorkflowBuilder`.
4. Atualize `output_executors=[interview_exec]`.

> **Importante:** `start_executor` é o único agente que recebe a entrada bruta do utilizador. Todos os demais agentes recebem a saída da sua aresta a montante.

---

## Erros comuns no gráfico

| Erro | Sintoma | Correção |
|---------|---------|-----|
| Aresta em falta para `output_executors` | Agente corre mas saída está vazia | Certifique-se que há um caminho de `start_executor` para todos os agentes em `output_executors` |
| Dependência circular | Loop infinito ou timeout | Verifique se nenhum agente retroalimenta um agente a montante |
| Agente em `output_executors` sem aresta de entrada | Saída vazia | Adicione pelo menos uma `add_edge(source, that_agent)` |
| Vários `output_executors` sem fan-in | Saída contém apenas a resposta de um agente | Use um único agente de saída que agregue, ou aceite múltiplas saídas |
| `start_executor` em falta | `ValueError` em tempo de construção | Especifique sempre `start_executor` em `WorkflowBuilder()` |

---

## Depurar o gráfico

### Usar o Inspetor de Agentes

1. Inicie o agente localmente com F5.
2. Abra o Inspetor de Agentes (`Ctrl+Shift+P` → **Foundry Toolkit: Open Agent Inspector**).
3. Envie uma mensagem de teste.
4. No painel de resposta do Inspetor, procure pela **saída em streaming** - mostra a contribuição de cada agente em sequência.


### Usar logging

Adicione logging a `main.py` para rastrear o fluxo de dados:

```python
import logging
logger = logging.getLogger("resume-job-fit")

# In main(), after building the workflow:
logger.info("Workflow graph built with edges: RP→JD, JD→MA, MA→GA")
```

Os logs do servidor mostram a ordem de execução do agente e chamadas à ferramenta MCP:

```
INFO:agent_framework:Executing agent: ResumeParser
INFO:agent_framework:Executing agent: JobDescriptionAgent
INFO:agent_framework:Executing agent: MatchingAgent
INFO:agent_framework:Executing agent: GapAnalyzer
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Kubernetes")
POST https://learn.microsoft.com/api/mcp → 200
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Terraform")
POST https://learn.microsoft.com/api/mcp → 200
```

---

### Checkpoint

- [ ] Pode identificar os dois padrões de orquestração no fluxo de trabalho: cadeia sequencial e relevo de conteúdo
- [ ] Compreende porque `context_mode="last_agent"` requer um relevo explícito de dados entre agentes
- [ ] Consegue ler o código `WorkflowBuilder` e mapear cada chamada `add_edge()` para o gráfico visual
- [ ] Sabe como adicionar um novo agente ao final da pipeline
- [ ] Pode identificar erros comuns no gráfico e os seus sintomas

---

**Anterior:** [03 - Configurar Agentes & Ambiente](03-configure-agents.md) · **Seguinte:** [05 - Testar Localmente →](05-test-locally.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->