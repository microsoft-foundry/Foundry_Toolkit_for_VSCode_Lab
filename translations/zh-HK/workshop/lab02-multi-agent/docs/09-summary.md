# 模組 9 - 總結與後續步驟

⏱️ 約 5 分鐘

**恭喜！** 你已經使用 Microsoft Foundry 和 Foundry Toolkit for VS Code 建立、測試並（如果是路徑 A）部署了多代理工作流程。

---

## 你所建立的內容

**履歷 → 職位匹配評估器** - 一個多代理托管工作流程，其功能包括：
- 通過 HTTP 接收履歷 + 職位描述（`POST /responses`）
- 依序執行四個專業代理 —— 每個代理轉交其後續代理所需的資料
- 返回適合度分數（0–100，帶詳細分解）、技能及證照缺口清單，以及針對每個缺口附帶真實 Microsoft Learn 連結的個人化學習路線圖
- 呼叫 Microsoft Learn MCP 伺服器（`https://learn.microsoft.com/api/mcp`），取得每個識別出的技能缺口的官方學習資源
- 以單一容器化托管代理形式，在 Microsoft Foundry 代理服務運行

---

## 主要學習概念

| 概念 | 你所練習的內容 |
|---------|-------------------|
| <strong>多代理協調</strong> | 使用 `WorkflowBuilder` 建立的序列化管線，配合 `add_edge()` |
| <strong>代理專業化</strong> | 四個專注代理的表現優於一個通用代理 |
| <strong>內容路由器模式</strong> | ResumeParser 同時作為路由器 —— 它將職位描述文字保留在 `[JOB DESCRIPTION PASS-THROUGH]` 區段，讓下游代理可存取（必要，因為 `context_mode="last_agent"` 意味只有 `start_executor` 能看到原始用戶訊息） |
| <strong>內容轉發模式</strong> | JD Agent 向前轉發 `[PARSED RESUME PASS-THROUGH]`，讓 MatchingAgent 可以拿到兩者資料；避免匯入點圖形造成的「或連結」雙重觸發問題 |
| **MCP 工具整合** | 使用 `@tool` + `streamable_http_client` 呼叫外部 MCP 伺服器 |
| <strong>托管代理生命週期</strong> | 搭建架構 → 配置 → 本地測試 → 部署 → 雲端驗證 |
| **`context_mode="last_agent"`** | 每個執行者只能看到其直接前任的輸出 |
| **Foundry 工具包工作流程** | 搭建精靈、代理檢視器、工作流程視覺化、一鍵部署 |

---

## 你完成的事項

<details open>
<summary><strong>🅰️ 路徑 A - Foundry 訂閱</strong></summary>

- [x] 驗證實驗室 01 設定：專案、模型及 RBAC 狀態正常
- [x] 使用工作流程範本搭建多代理專案
- [x] 撰寫四個代理指令集（ResumeParser、JD Agent、MatchingAgent、GapAnalyzer）
- [x] 整合 Microsoft Learn MCP 工具與 `streamable_http_client`
- [x] 使用 `WorkflowBuilder` 連接工作流程圖（序列管線與內容轉發）
- [x] 用三種燒煙測試（代理檢視器）進行本地測試 —— 適合度分數、缺口卡片與 MCP 網址
- [x] 部署至 Foundry 代理服務（容器化，使用管理身分）
- [x] 在雲端遊樂場驗證 —— 結構與本地結果一致

</details>

<details open>
<summary><strong>🅱️ 路徑 B - Foundry Local</strong></summary>

- [x] 驗證實驗室 01 設定：Foundry Local 運作正常，並有本地模型
- [x] 使用工作流程範本搭建多代理專案
- [x] 撰寫四個代理指令集並連接工作流程圖
- [x] 整合 Microsoft Learn MCP 工具
- [x] 使用三種燒煙測試進行本地測試
- [x] 驗證多代理行為，無需雲端資源

</details>

---

## 後續步驟

### 持續學習

| 資源 | 說明 |
|----------|-------------|
| **[Agent Framework SDK 參考](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`、`WorkflowBuilder`、`AgentExecutor` 的 API 文件 |
| **[MCP 工具目錄](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | 連接代理至其他 MCP 伺服器（Bing、GitHub、自訂） |
| **[新增知識 (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 以文件、向量庫或 Bing 搜尋豐富代理基礎知識 |
| **[Foundry 評估](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | 透過自動評估器大規模衡量代理品質 |
| **[Microsoft Foundry 文件](https://learn.microsoft.com/azure/foundry/)** | 完整平台參考 |
| **[Foundry Toolkit - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 擴充功能版本說明與更新日志 |

### 工作流程擴展構想

- <strong>新增第五個代理</strong> —— 根據缺口報告生成可能面試問題的面試教練
- **新增 Bing 資源工具** —— 讓 JD Agent 搜尋類似職缺以豐富職位需求
- <strong>連接履歷資料庫</strong> —— 透過自訂 `@tool` 從資料庫拉取候選人資料
- <strong>嘗試不同模型</strong> —— 比較 `gpt-4.1` 與 `gpt-4.1-mini` 的輸出品質與延遲
- **使用 Foundry 評估** —— 利用評估功能針對黃金資料集評分適合度報告

### 對路徑 B 使用者：升級至雲端部署

當你準備好部署雲端時：
1. 取得 Azure 訂閱（[azure.microsoft.com/free](https://azure.microsoft.com/free/)）
2. 完成 [實驗室 01，模組 01](../../lab01-single-agent/docs/01-setup.md)（創建專案、部署模型、指派 RBAC）
3. 更新你的 `.env`，填入 Foundry 專案端點與模型部署名稱
4. 從 [模組 06 - 部署至 Foundry](06-deploy-to-foundry.md) 繼續

---

## 清理資源（選擇性）

如果你想移除在本工作坊期間建立的 Azure 資源：

### 選項 1：刪除資源群組（會移除所有資源）

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 選項 2：只刪除托管代理

1. 開啟 [ai.azure.com](https://ai.azure.com) → 你的專案 → <strong>建置</strong> → <strong>代理</strong>。
2. 找到 **PersonalCareerCopilot** → 點擊 <strong>刪除</strong>。

### 選項 3：刪除模型部署

1. 在 Foundry 側欄展開你的專案 → <strong>模型</strong>。
2. 右鍵點擊模型部署 → <strong>刪除</strong>。

> **費用提醒：** 托管代理僅在運行時產生費用。停止或刪除代理後，無持續費用。模型部署可能因保留容量而產生少量費用 — 使用完成後可刪除。

---

**上一節：** [08 - 疑難排解](08-troubleshooting.md) · **首頁：** [實驗室 02 說明檔](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->