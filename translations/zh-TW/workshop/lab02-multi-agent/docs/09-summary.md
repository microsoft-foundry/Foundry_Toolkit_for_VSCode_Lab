# 模組 9 - 摘要與後續步驟

⏱️ 約 5 分鐘

**恭喜！** 您已使用 Microsoft Foundry 與 Foundry Toolkit for VS Code 建立、測試並（如果是路徑 A）部署了一個多代理工作流程。

---

## 您所建立的內容

**履歷 → 工作適配評估器** — 一個多代理託管工作流程，功能為：
- 透過 HTTP 接收履歷和職務描述（`POST /responses`）
- 以串連管線方式執行四個專門代理—每個代理傳遞其後續代理所需的資料
- 回傳適配分數（0–100 含細項分解）、技能與認證差距清單，以及針對每個差距的個人化學習路徑，並附上真正的 Microsoft Learn 連結
- 呼叫 Microsoft Learn MCP 伺服器（`https://learn.microsoft.com/api/mcp`）取得每個識別技能差距的官方學習資源
- 以單一容器化託管代理執行於 Microsoft Foundry Agent 服務中

---

## 主要學習概念

| 概念 | 實作內容 |
|---------|-------------------|
| <strong>多代理編排</strong> | 使用 `WorkflowBuilder` 建置串連管線，並使用 `add_edge()` |
| <strong>代理專精化</strong> | 四個專注代理勝過一個通用代理 |
| <strong>內容路由器模式</strong> | ResumeParser 兼任路由器—在 `[JOB DESCRIPTION PASS-THROUGH]` 區段保留 JD 文字，使下游代理能存取（必要，因為 `context_mode="last_agent"` 意味著只有 `start_executor` 看到原始使用者訊息） |
| <strong>內容轉接模式</strong> | JD Agent 向前轉接 `[PARSED RESUME PASS-THROUGH]`，讓 MatchingAgent 同時取得兩個履歷；避免了匯聚圖造成的 OR 觸發重複 |
| **MCP 工具整合** | 使用 `@tool` 與 `streamable_http_client` 呼叫外部 MCP 伺服器 |
| <strong>託管代理生命週期</strong> | 從骨架 → 配置 → 本地測試 → 部署 → 雲端驗證 |
| **`context_mode="last_agent"`** | 每個執行者只看到其直接前任的輸出 |
| **Foundry Toolkit 工作流程** | 骨架精靈、代理檢視器、流程視覺化器、一鍵部署 |

---

## 您所完成的事項

<details open>
<summary><strong>🅰️ 路徑 A - Foundry 訂閱</strong></summary>

- [x] 驗證實驗 01 設定：專案、模型和 RBAC 持續有效
- [x] 利用工作流程範本搭建多代理專案骨架
- [x] 撰寫四組代理說明（ResumeParser、JD Agent、MatchingAgent、GapAnalyzer）
- [x] 整合 Microsoft Learn MCP 工具與 `streamable_http_client`
- [x] 使用 `WorkflowBuilder` 接線工作流程圖（串連管線，內容轉接）
- [x] 本地以 Agent Inspector 進行 3 項煙霧測試—適配分數、差距卡片與 MCP URL
- [x] 部署至 Foundry Agent 服務（容器化，管理式識別）
- [x] 雲端操作台驗證，與本地結果結構一致

</details>

<details open>
<summary><strong>🅱️ 路徑 B - Foundry Local</strong></summary>

- [x] 驗證實驗 01 設定：Foundry Local 正常執行，本地模型正常
- [x] 利用工作流程範本搭建多代理專案骨架
- [x] 撰寫四組代理說明並接線工作流程圖
- [x] 整合 Microsoft Learn MCP 工具
- [x] 進行本地 3 項煙霧測試
- [x] 驗證多代理行為，無須使用雲端資源

</details>

---

## 後續步驟

### 繼續學習

| 資源 | 說明 |
|----------|-------------|
| **[Agent Framework SDK 參考](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`、`WorkflowBuilder`、`AgentExecutor` 的 API 文件 |
| **[MCP 工具目錄](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | 將代理連接到其他 MCP 伺服器（Bing、GitHub、自訂） |
| **[新增知識（RAG）](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 利用文件、向量庫或 Bing 搜尋為代理提供依據 |
| **[Foundry 評估](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | 使用自動評估器在規模上衡量代理品質 |
| **[Microsoft Foundry 文件](https://learn.microsoft.com/azure/foundry/)** | 完整平台參考 |
| **[Foundry Toolkit - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 擴充功能版本說明與變更紀錄 |

### 擴充此工作流程的想法

- **新增第 5 個代理** — 依據差距報告產生可能的面試問題的面試教練
- **新增 Bing 地基工具** — 讓 JD 代理搜尋類似職務發布以豐富需求分析
- <strong>連接履歷資料庫</strong> — 透過自訂 `@tool` 從資料庫拉取候選人資料
- <strong>嘗試不同模型</strong> — 比較 `gpt-4.1` 與 `gpt-4.1-mini` 的輸出品質與延遲
- **使用 Foundry 進行評估** — 利用評估功能對適配報告與黃金資料集進行評分

### 對路徑 B 使用者：升級至雲端部署

準備好部署雲端時：
1. 取得 Azure 訂閱（[azure.microsoft.com/free](https://azure.microsoft.com/free/)）
2. 完成 [實驗 01，模組 01](../../lab01-single-agent/docs/01-setup.md)（建立專案、部署模型、指派 RBAC）
3. 用 Foundry 專案端點與模型部署名稱更新您的 `.env`
4. 從 [模組 06 - 部署到 Foundry](06-deploy-to-foundry.md) 繼續

---

## 清理資源（選用）

如果您想移除本工作坊建立的 Azure 資源：

### 選項 1：刪除資源群組（會移除所有資源）

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 選項 2：僅刪除託管代理

1. 開啟 [ai.azure.com](https://ai.azure.com) → 您的專案 → <strong>建立</strong> → <strong>代理</strong>。
2. 找到 **PersonalCareerCopilot** → 點擊 <strong>刪除</strong>。

### 選項 3：刪除模型部署

1. 在 Foundry 側邊欄展開您的專案 → <strong>模型</strong>。
2. 右鍵點擊該模型部署 → <strong>刪除</strong>。

> **費用提醒：** 託管代理只有在運行時才產生費用。若停止或刪除代理，即不會再有持續費用。模型部署可能會產生少量保留容量費用—用畢後請刪除。

---

**上一篇：** [08 - 疑難排解](08-troubleshooting.md) · **首頁：** [實驗 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->