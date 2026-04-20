# 已知問題

本文檔追蹤目前資料庫狀態的已知問題。

> 最後更新：2026-04-15。於 `.venv_ga_test` 中使用 Python 3.13 / Windows 測試。

---

## 目前套件鎖定版本（三個代理皆適用）

| 套件 | 目前版本 |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(已修正 — 請參見 KI-003)* |

---

## KI-001 — GA 1.0.0 升級阻塞：`agent-framework-azure-ai` 已移除

**狀態：** 開放 | **嚴重度：** 🔴 高 | **類型：** 破壞性變更

### 說明

`agent-framework-azure-ai` 套件（鎖定於 `1.0.0rc3`）在 GA 版本（1.0.0，發布於 2026-04-02）中已被<strong>移除/棄用</strong>。
它由以下兩個套件取代：

- `agent-framework-foundry==1.0.0` — 由 Foundry 托管的代理範例
- `agent-framework-openai==1.0.0` — 由 OpenAI 支援的代理範例

三個 `main.py` 檔案均從 `agent_framework.azure` 匯入 `AzureAIAgentClient`，在 GA 套件中會引發 `ImportError`。
`agent_framework.azure` 命名空間仍存在，但 GA 版本中僅包含 Azure Functions 類別（`DurableAIAgent`、`AzureAISearchContextProvider`、`CosmosHistoryProvider`），並不包含 Foundry 代理。

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

**狀態：** 開放 | **嚴重度：** 🔴 高 | **類型：** 破壞性（受上游阻塞）

### 說明

`azure-ai-agentserver-agentframework==1.0.0b17`（最新）嚴格鎖定 `agent-framework-core<=1.0.0rc3`。
若與 GA 版本 `agent-framework-core==1.0.0` 一起安裝，pip 將被迫**將 `agent-framework-core` 降級回 rc3**，此舉會破壞 `agent-framework-foundry==1.0.0` 與 `agent-framework-openai==1.0.0`。

因此，所有代理用於綁定 HTTP 伺服器的 `from azure.ai.agentserver.agentframework import from_agent_framework` 呼叫也被阻塞。

### 確認套件衝突（`.venv_ga_test`）

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### 受影響檔案

三個 `main.py` 全部受影響 — 包含頂層匯入及 `main()` 函式內的匯入。

---

## KI-003 — 不再需要 `agent-dev-cli --pre` 參數

**狀態：** ✅ 已修正（非破壞性） | **嚴重度：** 🟢 低

### 說明

所有 `requirements.txt` 檔案之前包含 `agent-dev-cli --pre`，用來拉取預發佈 CLI。
自 2026-04-02 GA 1.0.0 發佈後，正式版 `agent-dev-cli` 現已可於無需 `--pre` 參數下使用。

**已套用修正：** 已從三個 `requirements.txt` 檔案移除 `--pre` 參數。

---

## KI-004 — Dockerfile 使用 `python:3.14-slim`（預發行基底映像）

**狀態：** 開放 | **嚴重度：** 🟡 低

### 說明

所有 `Dockerfile` 均使用 `FROM python:3.14-slim`，此為 Python 預發佈版本。
對於生產環境部署，建議鎖定穩定版本 (例如 `python:3.12-slim`)。

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
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用本翻譯所產生的任何誤解或誤釋負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->