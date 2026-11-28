# Módulo 0 - Introdução

⏱️ ~10 min

> [!WARNING]
> **Prévia e Limitações:** [Agentes hospedados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) estão atualmente em **pré-visualização pública** - não recomendado para cargas de trabalho em produção. Alguns recursos mostrados neste workshop podem mudar à medida que o serviço avança para GA.

## O que você vai construir

Neste laboratório, você amplia as habilidades de agente único do Laboratório 01 para construir um **fluxo de trabalho multiagente** - o Avaliador de Compatibilidade Currículo → Vaga.

Você cola um **currículo** e uma **descrição de vaga**. Quatro agentes especializados processam a entrada sequencialmente e depois retornam:
- Uma pontuação de compatibilidade (0–100 com detalhamento da pontuação)
- Uma lista de lacunas de habilidades e certificações
- Um roadmap de aprendizado personalizado com links reais do Microsoft Learn para cada lacuna

**O fluxo de trabalho usa:**
- **Microsoft Agent Framework** - `WorkflowBuilder` para orquestração sequencial de pipeline
- **Foundry Toolkit para VS Code** - scaffolding, teste local, deploy
- **Um modelo de IA** (exemplo, `gpt-4.1-mini`) - usado por todos os quatro agentes
- **Servidor MCP do Microsoft Learn** - fornece links reais de recursos de aprendizado para cada lacuna de habilidade

---

## Escolha seu caminho

> ⚠️ **Continue com o mesmo caminho usado no Laboratório 01.**

<details open>
<summary><strong>🅰️ Caminho A - Azure cloud (requer assinatura Azure)</strong></summary>

| | Detalhes |
|---|---|
| **Para quem é?** | Você completou o Laboratório 01 usando uma assinatura Azure |
| **Modelo** | Azure OpenAI via Foundry (exemplo, `gpt-4.1-mini`) |
| **Módulos abordados** | Todos os módulos (00–09) |
| **Deploy na nuvem?** | ✅ Sim - deploy completo ponta a ponta |

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local (não requer assinatura Azure)</strong></summary>

| | Detalhes |
|---|---|
| **Para quem é?** | Você completou o Laboratório 01 usando Foundry Local |
| **Modelo** | Foundry Local (gratuito, roda na sua máquina) |
| **Módulos abordados** | Módulos 00–05 (pule 06–07 - deploy e verificação na nuvem) |
| **Deploy na nuvem?** | ❌ Não - apenas testes locais via Agent Inspector |

</details>

---

## Verificação do Laboratório 01

O Laboratório 02 baseia-se diretamente no Laboratório 01. Complete o Laboratório 01 antes de começar aqui.

Ainda não fez o Laboratório 01? Comece aqui: [Laboratório 01 - Introdução](../../lab01-single-agent/docs/00-prerequisites.md)

<details open>
<summary><strong>🅰️ Caminho A - Azure cloud</strong></summary>

```powershell
az account show --query "{name:name, id:id}" --output table
```

Se falhar, execute `az login`. Depois verifique no VS Code:

1. `Ctrl+Shift+P` → digite **Foundry Toolkit** → confirme se os comandos aparecem.
2. Clique no ícone **Foundry Toolkit** → seu projeto e modelo implantado mostram **Succeeded**.

![Barra lateral do Foundry Toolkit mostrando o projeto em Meus Recursos, com o seletor de Alternar projeto / Criar projeto aberto](../../../../../translated_images/pt-BR/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

> **RBAC:** Você atribuiu **Foundry User** no Laboratório 01. Se precisar reatribuir, veja [Laboratório 01, Módulo 1](../../lab01-single-agent/docs/01-setup.md#deploy-a-model--assign-rbac). A função era anteriormente chamada **Azure AI User** - mesmas permissões.

</details>

<details open>
<summary><strong>🅱️ Caminho B - Foundry Local</strong></summary>

```powershell
Invoke-WebRequest -Uri "http://localhost:5273/v1/health" -UseBasicParsing | Select-Object StatusCode
```

Esperado: `StatusCode: 200`. Se não, reinicie o Foundry Local pela barra lateral do Foundry Toolkit.

> Toda inferência roda em sua máquina. A única chamada externa é a ferramenta MCP para `https://learn.microsoft.com/api/mcp`.

</details>

---

## Novidades no Laboratório 02

| | Laboratório 01 | Laboratório 02 |
|--|--------|--------|
| Agentes | 1 | 4 (encadeados com WorkflowBuilder) |
| Template scaffold | Básico - Agent Framework | Fluxos de trabalho - Agent Framework |
| Novo pacote | - | `mcp` |
| Orquestração | Agente de conversação único | Pipeline sequencial (WorkflowBuilder) |
| Nova ferramenta | - | `search_microsoft_learn_for_plan` (MCP) |

---

**Próximo:** [01 - Entenda a Arquitetura →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->