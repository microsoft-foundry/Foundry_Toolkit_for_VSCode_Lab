# 已知問題

本文件追蹤當前倉庫狀態下的已知問題。

> 最後更新：2026-04-15。於 `.venv_ga_test` 上以 Python 3.13 / Windows 測試。

---

## 當前套件鎖定版本（三個代理皆適用）

| 套件 | 當前版本 |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(已修正 — 請參考 KI-003)* |

---

## KI-001 — GA 1.0.0 升級受阻：`agent-framework-azure-ai` 被移除

**狀態：** 開啟中 | **嚴重性：** 🔴 高 | **類型：** 重大變更

### 描述

`agent-framework-azure-ai` 套件（鎖定在 `1.0.0rc3`）在 GA 版本（1.0.0，於 2026-04-02 發佈）中被<strong>移除/棄用</strong>。其被以下套件取代：

- `agent-framework-foundry==1.0.0` — Foundry 托管代理模式
- `agent-framework-openai==1.0.0` — 由 OpenAI 支援的代理模式

所有三個 `main.py` 檔案皆從 `agent_framework.azure` 匯入 `AzureAIAgentClient`，但在 GA 版本的套件中會拋出 `ImportError`。GA 中仍存在 `agent_framework.azure` 命名空間，但現在僅包含 Azure Functions 類別（`DurableAIAgent`、`AzureAISearchContextProvider`、`CosmosHistoryProvider`）— 並不包含 Foundry 代理。

### 確認錯誤（`.venv_ga_test`）

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### 受影響檔案

| 檔案 | 行數 |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` 與 GA `agent-framework-core` 不相容

**狀態：** 開啟中 | **嚴重性：** 🔴 高 | **類型：** 重大變更（受上游阻塞）

### 描述

`azure-ai-agentserver-agentframework==1.0.0b17`（最新）將 `agent-framework-core<=1.0.0rc3` 鎖定為嚴格版本。若同時安裝 `agent-framework-core==1.0.0`（GA 版本），pip 將<strong>降級</strong> `agent-framework-core` 回 rc3，導致 `agent-framework-foundry==1.0.0` 和 `agent-framework-openai==1.0.0` 失效。

所有代理用來綁定 HTTP 伺服器的 `from azure.ai.agentserver.agentframework import from_agent_framework` 呼叫也因此受阻。

### 確認依賴衝突（`.venv_ga_test`）

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### 受影響檔案

三個 `main.py` 檔案皆受影響 — 包含頂層匯入以及 `main()` 函式內部匯入。

---

## KI-003 — 不再需要 `agent-dev-cli --pre` 參數

**狀態：** ✅ 已修復（非中斷性） | **嚴重性：** 🟢 低

### 描述

所有 `requirements.txt` 檔案先前均包含 `agent-dev-cli --pre` 以拉取預發佈版 CLI。自 GA 1.0.0 於 2026-04-02 發佈後，`agent-dev-cli` 穩定版本已經可用，不再需要使用 `--pre` 參數。

**已應用修正：** 三個 `requirements.txt` 檔案中的 `--pre` 參數已被移除。

---

## KI-004 — Dockerfiles 使用 `python:3.14-slim`（預發佈基底映像）

**狀態：** 開啟中 | **嚴重性：** 🟡 低

### 描述

所有 `Dockerfile` 使用 `FROM python:3.14-slim`，該映像為 Python 預發佈版本。對於生產部署，應當固定至穩定版本（例如 `python:3.12-slim`）。

### 受影響檔案

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## 參考資料

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的本地語言版本應被視為權威來源。對於重要資訊，建議聘請專業人工翻譯。我們對於因使用本翻譯而引致的任何誤解或錯誤詮釋概不負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->