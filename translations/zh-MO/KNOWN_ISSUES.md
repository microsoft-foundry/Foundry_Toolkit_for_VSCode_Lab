# 已知問題

本文檔跟蹤當前儲存庫狀態的已知問題。

> 最後更新日期：2026-04-15。測試環境為 Python 3.13 / Windows 在 `.venv_ga_test`。

---

## 目前的套件釘選（所有三個代理）

| 套件 | 目前版本 |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(已修正 — 參見 KI-003)* |

---

## KI-001 — GA 1.0.0 升級阻擋：`agent-framework-azure-ai` 已移除

**狀態：** 開啟 | **嚴重性：** 🔴 高 | **類型：** 重大變更阻斷

### 描述

在 GA 發布版本（1.0.0，於 2026-04-02 發布）中，`agent-framework-azure-ai` 套件（釘選於 `1.0.0rc3`）已<strong>移除／棄用</strong>。取代方案為：

- `agent-framework-foundry==1.0.0` — Foundry 託管的代理模式
- `agent-framework-openai==1.0.0` — OpenAI 支援的代理模式

所有三個 `main.py` 檔案均從 `agent_framework.azure` 匯入 `AzureAIAgentClient`，在 GA 套件下會引發 `ImportError`。`agent_framework.azure` 命名空間在 GA 版本中仍存在，但現在僅包含 Azure Functions 類別（`DurableAIAgent`、`AzureAISearchContextProvider`、`CosmosHistoryProvider`），不包含 Foundry 代理。

### 確認錯誤（`.venv_ga_test`）

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### 受影響的檔案

| 檔案 | 行數 |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` 與 GA `agent-framework-core` 不相容

**狀態：** 開啟 | **嚴重性：** 🔴 高 | **類型：** 重大變更阻斷（受上游阻擋）

### 描述

`azure-ai-agentserver-agentframework==1.0.0b17`（最新）將 `agent-framework-core` 鎖定為 `<=1.0.0rc3`。安裝此套件同時搭配 `agent-framework-core==1.0.0`（GA）時，pip 將強制<strong>降級</strong>`agent-framework-core` 回 rc3 版本，此舉會破壞 `agent-framework-foundry==1.0.0` 和 `agent-framework-openai==1.0.0`。

所有代理使用的 `from azure.ai.agentserver.agentframework import from_agent_framework` 呼叫以綁定 HTTP 伺服器，因此也被阻擋。

### 確認依賴衝突（`.venv_ga_test`）

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### 受影響的檔案

所有三個 `main.py` 檔案——包括頂層匯入和 `main()` 函數內的匯入。

---

## KI-003 — 不再需要 `agent-dev-cli --pre` 標誌

**狀態：** ✅ 已修復（非重大破壞）| **嚴重性：** 🟢 低

### 描述

所有 `requirements.txt` 檔案先前均包含 `agent-dev-cli --pre` 以拉取預發布版本 CLI。自 2026-04-02 GA 1.0.0 發布後，`agent-dev-cli` 穩定版已可不經 `--pre` 標誌安裝。

**已採取修正措施：** 所有三個 `requirements.txt` 檔案都已移除 `--pre` 標誌。

---

## KI-004 — Dockerfile 使用 `python:3.14-slim`（預發布基礎映像）

**狀態：** 開啟 | **嚴重性：** 🟡 低

### 描述

所有 `Dockerfile` 均採用 `FROM python:3.14-slim`，該版本為 Python 的預發布版本。生產部署建議固定使用穩定版本（例如 `python:3.12-slim`）。

### 受影響的檔案

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## 參考資料

- [agent-framework-core 在 PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry 在 PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，請注意自動翻譯可能包含錯誤或不準確之處。原始文件之母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。對因使用本翻譯所產生之任何誤解或誤譯，我們概不負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->