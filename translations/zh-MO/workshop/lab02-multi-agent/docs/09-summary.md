# 模組 9 - 總結與後續步驟

⏱️ 約 5 分鐘

**恭喜！** 你已使用 Microsoft Foundry 及 Foundry Toolkit for VS Code 建立、測試及（如果是路徑 A）部署了多代理工作流程。

---

## 你所建立的內容

**履歷 → 工作配對評估器** — 一個多代理的托管工作流程，具備以下功能：
- 透過 HTTP 接收履歷與職務描述（`POST /responses`）
- 執行四個專門化代理，以線性管線方式運行 — 每個代理傳遞其後繼代理所需的資料
- 回傳配對分數（0–100 含詳解）、技能與認證差距清單，以及包含 Microsoft Learn 官方連結的個人化學習路線圖
- 呼叫 Microsoft Learn MCP 伺服器（`https://learn.microsoft.com/api/mcp`）以取得每項識別技能差距的官方學習資源
- 以單一容器化的托管代理在 Microsoft Foundry Agent Service 中執行

---

## 你學到的關鍵概念

| 概念 | 你練習了什麼 |
|---------|-------------------|
| <strong>多代理編排</strong> | 使用 `WorkflowBuilder` 建立依序管線並透過 `add_edge()` |
| <strong>代理專精化</strong> | 四個專注代理效果勝過一個通用代理 |
| <strong>內容路由器模式</strong> | ResumeParser 同時擔任路由器角色 — 它在 `[JOB DESCRIPTION PASS-THROUGH]` 區域保留職務描述文字，供後續代理存取（因 `context_mode="last_agent"` 意味著只有 `start_executor` 能看見原始使用者訊息） |
| <strong>內容轉發模式</strong> | JD Agent 轉發 `[PARSED RESUME PASS-THROUGH]`，使 MatchingAgent 可取得雙方簡介；避免了匯聚圖導致的 OR 語意重複觸發 |
| **MCP 工具整合** | `@tool` + `streamable_http_client` 呼叫外部 MCP 伺服器 |
| <strong>托管代理生命週期</strong> | 建立骨架 → 配置 → 本地測試 → 部署 → 雲端驗證 |
| **`context_mode="last_agent"`** | 每個執行器只看見直接前任的輸出 |
| **Foundry Toolkit 工作流程** | 骨架嚮導、代理檢查器、工作流程視覺化器、一鍵部署 |

---

## 你完成的內容

<details open>
<summary><strong>🅰️ 路徑 A - Foundry 訂閱</strong></summary>

- [x] 檢查實驗室 01 設定：專案、模型及 RBAC 仍然有效
- [x] 使用 Workflows 範本建立多代理專案骨架
- [x] 撰寫四個代理說明集（ResumeParser、JD Agent、MatchingAgent、GapAnalyzer）
- [x] 整合 Microsoft Learn MCP 工具與 `streamable_http_client`
- [x] 使用 `WorkflowBuilder` 連結工作流程圖（線性管線加內容轉發）
- [x] 透過三個快速測試（代理檢查器）在本地測試 — 配對分數、差距卡片與 MCP 網址
- [x] 部署至 Foundry Agent Service（容器化，使用受管身份）
- [x] 在雲端試玩場驗證，結構與本地結果一致

</details>

<details open>
<summary><strong>🅱️ 路徑 B - Foundry 本地端</strong></summary>

- [x] 檢查實驗室 01 設定：Foundry 本地端運行，並搭配本地模型
- [x] 使用 Workflows 範本建立多代理專案骨架
- [x] 撰寫四個代理說明集並連結工作流程圖
- [x] 整合 Microsoft Learn MCP 工具
- [x] 在本地端透過三個快速測試驗證
- [x] 驗證多代理行為，不需雲端資源

</details>

---

## 後續步驟

### 持續學習

| 資源 | 說明 |
|----------|-------------|
| **[代理框架 SDK 參考](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`、`WorkflowBuilder`、`AgentExecutor` 的 API 文件 |
| **[MCP 工具目錄](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | 將代理連接至其他 MCP 伺服器（Bing、GitHub、自訂等） |
| **[新增知識 (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 以文件、向量庫或 Bing 搜尋為代理提供基礎 |
| **[Foundry 評估](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | 透過自動化評估器量測代理品質 |
| **[Microsoft Foundry 文件](https://learn.microsoft.com/azure/foundry/)** | 完整平台參考 |
| **[Foundry Toolkit - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 擴充功能發布說明與變更日誌 |

### 擴展此工作流程的想法

- <strong>新增第五個代理</strong> — 依差距報告產出可能的面試問題的面試教練
- **新增 Bing 基地工具** — 允許 JD Agent 搜尋類似職缺來豐富需求
- <strong>連接履歷資料庫</strong> — 透過自訂 `@tool` 從資料庫拉取候選人簡介
- <strong>嘗試不同模型</strong> — 比較 `gpt-4.1` 與 `gpt-4.1-mini` 的輸出質量和延遲
- **使用 Foundry 評估** — 利用評估功能針對黃金資料集對配對報告打分

### 道路 B 用戶：升級至雲端部署

當你準備好部署到雲端時：
1. 取得 Azure 訂閱（[azure.microsoft.com/free](https://azure.microsoft.com/free/)）
2. 完成 [實驗室 01，模組 01](../../lab01-single-agent/docs/01-setup.md)（建立專案、部署模型、指派 RBAC）
3. 更新 `.env` 為 Foundry 專案端點與模型部署名稱
4. 從 [模組 06 - 部署到 Foundry](06-deploy-to-foundry.md) 繼續

---

## 清理資源（可選）

如果你想移除本工作坊期間建立的 Azure 資源：

### 選項 1：刪除資源群組（會刪除全部）

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 選項 2：僅刪除托管代理

1. 開啟 [ai.azure.com](https://ai.azure.com) → 你的專案 → <strong>建置</strong> → <strong>代理</strong>。
2. 找到 **PersonalCareerCopilot** → 點選 <strong>刪除</strong>。

### 選項 3：刪除模型部署

1. 在 Foundry 側邊欄展開你的專案 → <strong>模型</strong>。
2. 右鍵點選模型部署 → <strong>刪除</strong>。

> **成本說明：** 托管代理只有在運行時才會產生費用。停止或刪除代理後，將不會有持續收費。模型部署可能因保留容量而有少量費用 — 若不再使用請刪除。

---

**上一篇：** [08 - 疑難排解](08-troubleshooting.md) · **首頁：** [Lab 02 說明](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->