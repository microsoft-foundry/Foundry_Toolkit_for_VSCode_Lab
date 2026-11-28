# Módulo 4 - Padrões de Orquestração

⏱️ ~10 min

Neste módulo, você explora os padrões de orquestração usados no Avaliador de Compatibilidade de Currículo e aprende como ler, modificar e estender o gráfico do fluxo de trabalho. Entender esses padrões é essencial para depurar problemas no fluxo de dados e construir seus próprios [fluxos de trabalho multiagente](https://learn.microsoft.com/agent-framework/workflows/).

---

## Padrão 1: Cadeia sequencial

O padrão fundamental no fluxo de trabalho é uma **cadeia sequencial** - a saída de cada agente alimenta diretamente o próximo.

```mermaid
flowchart LR
    RP[Resume Parser] --> JD[JD Agent]
    JD --> MA[Matching Agent]
    MA --> GA[Gap Analyzer]
```

No código, cada chamada `add_edge()` cria uma etapa na cadeia:

```python
.add_edge(resume_executor, jd_executor)       # ResumeParser output → JD Agent
.add_edge(jd_executor, matching_executor)     # JD Agent output → MatchingAgent
.add_edge(matching_executor, gap_executor)    # MatchingAgent output → GapAnalyzer
```

> **Por que sequencial, e não fan-out/fan-in?** `WorkflowBuilder` usa **semântica OR** para as arestas de entrada: um executor a jusante dispara assim que **qualquer** predecessor termina. Se `matching_executor` tivesse duas arestas de entrada (de `resume_executor` e `jd_executor`), ele seria acionado duas vezes - uma quando ResumeParser termina e outra quando JD Agent termina - fazendo com que GapAnalyzer também execute duas vezes e a saída apareça duas vezes. O pipeline sequencial evita isso completamente.

## Padrão 2: Retransmissão de Conteúdo

Como `context_mode="last_agent"` significa que cada executor vê apenas a **saída do seu predecessor direto**, agentes em uma cadeia sequencial devem passar explicitamente adiante quaisquer dados que os agentes a jusante precisem.

Neste fluxo de trabalho:
- **ResumeParser** copia o JD literalmente para `[JOB DESCRIPTION PASS-THROUGH]` (para que o JD Agent possa encontrá-lo).
- **JD Agent** copia o `[PARSED RESUME]` literalmente para `[PARSED RESUME PASS-THROUGH]` (para que MatchingAgent possa comparar ambos os perfis).

```
ResumeParser output
└─ [PARSED RESUME]               ← extracted by JD Agent
└─ [JOB DESCRIPTION PASS-THROUGH] ← extracted by JD Agent

JD Agent output
└─ [JD REQUIREMENTS]             ← extracted by MatchingAgent
└─ [PARSED RESUME PASS-THROUGH]  ← extracted by MatchingAgent
```

Cada seção de retransmissão deve ser copiada **literalmente** - resumir ou parafrasear quebra o agente a jusante que depende dela.

---

## O gráfico completo

Combinar os padrões cadeia sequencial e retransmissão de conteúdo produz o fluxo de trabalho completo:

```mermaid
flowchart LR
    U[User Input] --> RP[Resume Parser]
    RP --> JD[JD Agent]
    JD --> MA[Matching Agent]
    MA --> GA[Gap Analyzer + MCP]
    GA --> O[Final Output]
```

O Agent Inspector mostra essa mesma estrutura de gráfico quando o agente está rodando localmente. Consulte [Módulo 5 - Teste Localmente](05-test-locally.md) para capturas de tela.

---

## Lendo o código do WorkflowBuilder

O gráfico do fluxo de trabalho é construído na função `main()` em [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py). As três chamadas `add_edge()` constroem o pipeline sequencial:

| # | Aresta | Efeito |
|---|--------|--------|
| 1 | `resume_executor → jd_executor` | JD Agent recebe `[PARSED RESUME]` + `[JOB DESCRIPTION PASS-THROUGH]` |
| 2 | `jd_executor → matching_executor` | MatchingAgent recebe `[JD REQUIREMENTS]` + `[PARSED RESUME PASS-THROUGH]` |
| 3 | `matching_executor → gap_executor` | GapAnalyzer recebe relatório de compatibilidade + lista de lacunas |

---

## Modificando o gráfico

### Adicionando um novo agente

Para adicionar um quinto agente (por exemplo, um **InterviewPrepAgent** após o GapAnalyzer):

1. Defina uma constante `INTERVIEW_PREP_INSTRUCTIONS`.
2. Crie os objetos `Agent` + `AgentExecutor` (mesmo padrão dos quatro existentes).
3. Adicione `.add_edge(gap_executor, interview_exec)` dentro de `WorkflowBuilder`.
4. Atualize `output_executors=[interview_exec]`.

> **Importante:** `start_executor` é o único agente que recebe entrada bruta do usuário. Todos os outros agentes recebem saída da sua aresta a montante.

---

## Erros comuns no gráfico

| Erro | Sintoma | Correção |
|-------|---------|---------|
| Falta aresta para `output_executors` | Agente executa, mas saída está vazia | Certifique-se de que existe um caminho de `start_executor` a cada agente em `output_executors` |
| Dependência circular | Loop infinito ou timeout | Verifique que nenhum agente alimenta um agente a montante |
| Agente em `output_executors` sem aresta de entrada | Saída vazia | Adicione pelo menos uma `add_edge(source, that_agent)` |
| Múltiplas `output_executors` sem fan-in | Saída contém resposta de apenas um agente | Use um único agente de saída que agregue, ou aceite múltiplas saídas |
| Falta `start_executor` | `ValueError` na construção | Sempre especifique `start_executor` em `WorkflowBuilder()` |

---

## Depurando o gráfico

### Usando o Agent Inspector

1. Inicie o agente localmente com F5.
2. Abra o Agent Inspector (`Ctrl+Shift+P` → **Foundry Toolkit: Abrir Agent Inspector**).
3. Envie uma mensagem de teste.
4. No painel de respostas do Inspector, procure pela **saída em streaming** - ela mostra a contribuição de cada agente em sequência.


### Usando logs

Adicione logs a `main.py` para rastrear o fluxo de dados:

```python
import logging
logger = logging.getLogger("resume-job-fit")

# In main(), after building the workflow:
logger.info("Workflow graph built with edges: RP→JD, JD→MA, MA→GA")
```

Os logs do servidor mostram a ordem de execução dos agentes e chamadas da ferramenta MCP:

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

### Ponto de verificação

- [ ] Você consegue identificar os dois padrões de orquestração no fluxo de trabalho: cadeia sequencial e retransmissão de conteúdo
- [ ] Você entende por que `context_mode="last_agent"` requer retransmissão explícita de dados entre agentes
- [ ] Você consegue ler o código `WorkflowBuilder` e mapear cada chamada `add_edge()` para o gráfico visual
- [ ] Você sabe como adicionar um novo agente ao final do pipeline
- [ ] Você consegue identificar erros comuns no gráfico e seus sintomas

---

**Anterior:** [03 - Configurar Agentes & Ambiente](03-configure-agents.md) · **Próximo:** [05 - Teste Localmente →](05-test-locally.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->