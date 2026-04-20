# 已知问题

本文档跟踪当前仓库状态下的已知问题。

> 最后更新：2026-04-15。测试环境为 Python 3.13 / Windows，使用 `.venv_ga_test`。

---

## 当前包版本固定（所有三个代理）

| 包 | 当前版本 |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(已修复 — 见 KI-003)* |

---

## KI-001 — GA 1.0.0 升级阻塞：`agent-framework-azure-ai` 被移除

**状态：** 开放 | **严重性：** 🔴 高 | **类型：** 破坏性

### 描述

`agent-framework-azure-ai` 包（固定为 `1.0.0rc3`）在 GA 版本（1.0.0，发布于 2026-04-02）中被<strong>移除/弃用</strong>。
它被以下包替代：

- `agent-framework-foundry==1.0.0` — Foundry 托管代理模式
- `agent-framework-openai==1.0.0` — OpenAI 支持的代理模式

所有三个 `main.py` 文件都从 `agent_framework.azure` 导入 `AzureAIAgentClient`，
在 GA 包下会引发 `ImportError`。
尽管 GA 版本仍存在 `agent_framework.azure` 命名空间，
但现在仅包含 Azure Functions 类（`DurableAIAgent`、`AzureAISearchContextProvider`、`CosmosHistoryProvider`）—
不再包含 Foundry 代理。

### 确认错误（`.venv_ga_test`）

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### 受影响文件

| 文件 | 行号 |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` 与 GA 版本 `agent-framework-core` 不兼容

**状态：** 开放 | **严重性：** 🔴 高 | **类型：** 破坏性（依赖上游阻塞）

### 描述

`azure-ai-agentserver-agentframework==1.0.0b17`（最新）将
`agent-framework-core` 锁定为 `<=1.0.0rc3`。
与 GA 版本的 `agent-framework-core==1.0.0` 一起安装时，
pip 会强制将 `agent-framework-core` <strong>降级</strong>回 `rc3`，这会导致
`agent-framework-foundry==1.0.0` 和 `agent-framework-openai==1.0.0` 不能正常工作。

因此，所有代理用来绑定 HTTP 服务器的调用
`from azure.ai.agentserver.agentframework import from_agent_framework` 也会被阻塞。

### 确认依赖冲突（`.venv_ga_test`）

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### 受影响文件

所有三个 `main.py` 文件 — 包括顶层导入和 `main()` 函数中的内部导入。

---

## KI-003 — 不再需要 `agent-dev-cli --pre` 标志

**状态：** ✅ 已修复（非破坏性） | **严重性：** 🟢 低

### 描述

所有 `requirements.txt` 文件之前都包含了 `agent-dev-cli --pre` 来拉取预发布 CLI。
自从 GA 1.0.0 于 2026-04-02 发布后，
`agent-dev-cli` 稳定版无需 `--pre` 标志即可使用。

**已应用修复：** 已从所有三个 `requirements.txt` 文件中移除 `--pre` 标志。

---

## KI-004 — Dockerfiles 使用 `python:3.14-slim`（预发布基础镜像）

**状态：** 开放 | **严重性：** 🟡 低

### 描述

所有 `Dockerfile` 都使用 `FROM python:3.14-slim`，这是一个预发布的 Python 版本。
生产环境部署应固定使用稳定版本（例如 `python:3.12-slim`）。

### 受影响文件

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## 参考资料

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：  
本文件使用 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 进行翻译。虽然我们努力确保准确性，但请注意自动翻译可能包含错误或不准确之处。原始文档的母语版本应被视为权威来源。对于重要信息，建议使用专业人工翻译。对于因使用本翻译而产生的任何误解或误释，我们不承担任何责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->