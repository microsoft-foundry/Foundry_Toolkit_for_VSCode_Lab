# Módulo 0 - Introdução

⏱️ ~10 min

> [!WARNING]
> **Pré-visualização e Limitações:** [Hosted Agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) estão atualmente em **pré-visualização pública** - não recomendado para cargas de trabalho em produção. Algumas funcionalidades apresentadas neste workshop podem mudar à medida que o serviço avança para GA.

## O que vais construir

Neste laboratório, vais expandir as competências de agente único do Laboratório 01 para construir um **fluxo de trabalho multi-agente** - o Avaliador de Ajuste Currículo → Emprego.

Vais colar um **currículo** e uma **descrição do trabalho**. Quatro agentes especializados processam a entrada sequencialmente, depois retornam:
- Uma pontuação de ajuste (0–100 com uma decomposição da pontuação)
- Uma lista de lacunas de competências e certificações
- Um roteiro de aprendizagem personalizado com links reais do Microsoft Learn para cada lacuna

**O fluxo de trabalho utiliza:**
- **Microsoft Agent Framework** - `WorkflowBuilder` para orquestração sequencial de pipeline
- **Foundry Toolkit para VS Code** - scaffolding, teste local, deploy
- **Um modelo de IA** (por exemplo, `gpt-4.1-mini`) - usado por todos os quatro agentes
- **Servidor Microsoft Learn MCP** - fornece links reais de recursos de aprendizagem para cada lacuna de competências

---

## Escolhe o teu caminho

> ⚠️ **Continua com o mesmo caminho que usaste no Laboratório 01.**

<details open>
<summary><strong>🅰️ Caminho A - Cloud Azure (requer subscrição Azure)</strong></summary>

| | Detalhes |
|---|---|
| **Para quem é?** | Completaste o Laboratório 01 usando uma subscrição Azure |
| **Modelo** | Azure OpenAI via Foundry (por exemplo, `gpt-4.1-mini`) |
| **Módulos cobertos** | Todos os módulos (00–09) |
| **Deploy para a cloud?** | ✅ Sim - deploy completo end-to-end |

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local (não é necessária subscrição Azure)</strong></summary>

| | Detalhes |
|---|---|
| **Para quem é?** | Completaste o Laboratório 01 usando Foundry Local |
| **Modelo** | Foundry Local (gratuito, executa na tua máquina) |
| **Módulos cobertos** | Módulos 00–05 (pula 06–07 - deploy & verificação na cloud) |
| **Deploy para a cloud?** | ❌ Não - só testes locais via Agent Inspector |

</details>

---

## Verificação do Laboratório 01

O Laboratório 02 baseia-se diretamente no Laboratório 01. Completa o Laboratório 01 antes de começares aqui.

Ainda não fizeste o Laboratório 01? Começa aqui: [Laboratório 01 - Introdução](../../lab01-single-agent/docs/00-prerequisites.md)

<details open>
<summary><strong>🅰️ Caminho A - Cloud Azure</strong></summary>

```powershell
az account show --query "{name:name, id:id}" --output table
```

Se isto falhar, executa `az login`. Depois verifica no VS Code:

1. `Ctrl+Shift+P` → digita **Foundry Toolkit** → confirma que os comandos aparecem.
2. Clica no ícone **Foundry Toolkit** → o teu projeto e modelo implementado mostram **Succeeded**.

![Barra lateral do Foundry Toolkit mostrando o projeto em Meus Recursos, com o selecionador de mudar/criar projeto aberto](../../../../../translated_images/pt-PT/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

> **RBAC:** Atribuíste o papel de **Foundry User** no Laboratório 01. Se precisares de o reatribuir, vê [Laboratório 01, Módulo 1](../../lab01-single-agent/docs/01-setup.md#deploy-a-model--assign-rbac). O papel era anteriormente chamado **Azure AI User** - mesmas permissões.

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local</strong></summary>

```powershell
Invoke-WebRequest -Uri "http://localhost:5273/v1/health" -UseBasicParsing | Select-Object StatusCode
```

Esperado: `StatusCode: 200`. Se não, reinicia o Foundry Local a partir da barra lateral do Foundry Toolkit.

> Toda a inferência corre na tua máquina. A única chamada externa é a ferramenta MCP para `https://learn.microsoft.com/api/mcp`.

</details>

---

## Novidades no Laboratório 02

| | Laboratório 01 | Laboratório 02 |
|--|--------|--------|
| Agentes | 1 | 4 (encadeados com WorkflowBuilder) |
| Template scaffold | Básico - Agent Framework | Fluxos de trabalho - Agent Framework |
| Novo pacote | - | `mcp` |
| Orquestração | Agente conversacional único | Pipeline sequencial (WorkflowBuilder) |
| Nova ferramenta | - | `search_microsoft_learn_for_plan` (MCP) |

---

**A seguir:** [01 - Compreender a Arquitetura →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->