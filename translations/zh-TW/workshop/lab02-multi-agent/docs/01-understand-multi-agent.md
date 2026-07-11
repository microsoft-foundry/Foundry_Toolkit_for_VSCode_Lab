# 模組 1 - 理解架構

⏱️ 約 5 分鐘

在撰寫任何程式碼之前，先快速了解一下你正在建立的內容以及它的運作方式。

---

## 你正在建立的內容

你會貼上 <strong>履歷</strong> 和 <strong>職務說明</strong>。工作流程會回傳：

- 一個適配分數（0–100，並附詳細分析）
- 技能與證照的缺口清單
- 一份個人化的學習路線圖，內附 Microsoft Learn 的連結對應每項缺口

---

## 四個代理程式

單一代理程式同時嘗試解析、評分及規劃，往往會匆促而產出膚淺的結果。拆分成四個專業代理程式會有更好的成效：

| 代理程式 | 功能 |
|-------|-------------|
| **ResumeParser** | 解析履歷；將職務說明逐字複製到 `[JOB DESCRIPTION PASS-THROUGH]`，供下游代理使用 |
| **JobDescriptionAgent** | 從傳遞過來的內容中擷取職務說明需求；將 `[PARSED RESUME]` 轉發為 `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | 比較兩個標註區段；產生 0–100 的適配分數和缺口清單 |
| **GapAnalyzer** | 擬定學習路線圖；為每項缺口搜尋 Microsoft Learn 資源 |

---

## 協調流程圖

這個工作流程是 <strong>順序管線</strong> - 每個代理程式將輸出傳遞給下一個：

```mermaid
flowchart LR
    A["使用者輸入"] --> B["履歷解析器"]
    B -- "解析後的履歷 + 職務說明轉接" --> C["職務說明代理"]
    C -- "職務需求 + 履歷轉接" --> D["匹配代理"]
    D -- "適配報告 + 差距" --> E["差距分析器 + MCP"]
    E --> F["最終輸出"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** 接收使用者輸入，解析履歷，並將職務說明複製到 `[JOB DESCRIPTION PASS-THROUGH]`。
2. <strong>職務說明代理</strong> 提取結構化需求並將 `[PARSED RESUME PASS-THROUGH]` 轉發出去。
3. **MatchingAgent** 比較兩個區段，產生適配分數和缺口清單。
4. **GapAnalyzer** 擬定路線圖，並為每項缺口呼叫 Microsoft Learn MCP 工具。

---

## 這如何對應到程式碼

在 `main.py` 中，你使用 `WorkflowBuilder` 描述這個圖：

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # 第一個接收使用者輸入的代理
        output_executors=[gap_executor],      # 最後一個代理 - 它的輸出即為回應
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JD Agent
    .add_edge(jd_executor, matching_executor)     # JD Agent → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

每個 `Agent` 都包裹在 `AgentExecutor` 中。`add_edge()` 呼叫定義了一條嚴格的順序管線—每個代理程式僅接收其直接前任的輸出。

> `context_mode="last_agent"` 表示每個執行個體只看到它直接前任的輸出。ResumeParser 和職務說明代理以標註區段向前傳遞資料，使下游代理擁有剛好所需的資訊。

---

## MCP 工具

GapAnalyzer 有一個工具：`search_microsoft_learn_for_plan`。它連接至 `https://learn.microsoft.com/api/mcp`，並回傳每項技能缺口的真實 Microsoft Learn 連結。

當工具執行時，你會看到這些日誌 - 全部都是預期內的：

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

只有 `POST` 傳回錯誤時才需擔心。

---

**前一篇：** [00 - 先決條件](00-prerequisites.md) · **下一篇：** [02 - 建立專案骨架 →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->