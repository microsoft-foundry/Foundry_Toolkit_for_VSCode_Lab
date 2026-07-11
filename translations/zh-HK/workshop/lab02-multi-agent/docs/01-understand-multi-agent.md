# 模組 1 - 了解架構

⏱️ 約 5 分鐘

在寫任何程式碼之前，先快速看看你要建立的是什麼以及它如何運作。

---

## 你正在建立的東西

你會貼上一份 <strong>履歷</strong> 和一份 <strong>職位描述</strong>。工作流程會回傳：

- 一個配對分數（0–100 並有細目說明）
- 一份技能與認證缺口清單
- 一份個人化學習路線圖，包含對應每個缺口的 Microsoft Learn 連結

---

## 四個代理人

單一代理人試圖同時解析、評分和規劃，容易草率並產生膚淺的結果。將工作分割成四個專門的代理人會有較佳成果：

| 代理人 | 功能 |
|-------|-----|
| **ResumeParser** | 解析履歷；將職位描述逐字複製到 `[JOB DESCRIPTION PASS-THROUGH]` 供下游代理人使用 |
| **JobDescriptionAgent** | 從通過資料中提取職位需求；將 `[PARSED RESUME]` 作為 `[PARSED RESUME PASS-THROUGH]` 傳給下一階段 |
| **MatchingAgent** | 比較兩個標記過的部分；產生 0–100 的配對分數和缺口清單 |
| **GapAnalyzer** | 建立學習路線圖；為每個缺口搜尋 Microsoft Learn 資源 |

---

## 編排流程圖

工作流程為 <strong>序列管線</strong> — 每個代理人將輸出傳遞給下一個：

```mermaid
flowchart LR
    A["用戶輸入"] --> B["履歷解析器"]
    B -- "已解析的履歷 + 職位描述傳遞" --> C["職位描述代理"]
    C -- "職位描述要求 + 履歷傳遞" --> D["匹配代理"]
    D -- "適合度報告 + 差距" --> E["差距分析器 + MCP"]
    E --> F["最終輸出"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** 接收使用者輸入，解析履歷，並將職位描述複製到 `[JOB DESCRIPTION PASS-THROUGH]`。
2. **JD Agent** 提取結構化需求並將 `[PARSED RESUME PASS-THROUGH]` 傳遞至下一階段。
3. **MatchingAgent** 比較兩個部分並產生配對分數與缺口清單。
4. **GapAnalyzer** 建立路線圖並為每個缺口呼叫 Microsoft Learn MCP 工具。

---

## 這如何對應到程式碼

在 `main.py` 中，你會用 `WorkflowBuilder` 描述這個流程圖：

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # 第一個接收用戶輸入的代理
        output_executors=[gap_executor],      # 最後一個代理 - 其輸出即為回應
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JD 代理
    .add_edge(jd_executor, matching_executor)     # JD 代理 → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

每個 `Agent` 都包在一個 `AgentExecutor` 中。`add_edge()` 調用定義嚴格的序列管線—每個代理人只接收其直接前置代理的輸出。

> `context_mode="last_agent"` 意味著每個執行者只看到其直接前置者的輸出。ResumeParser 和 JD Agent 以標記的區段將資料往前傳遞，使得每個下游代理人剛好擁有它所需的資料。

---

## MCP 工具

GapAnalyzer 有一個工具：`search_microsoft_learn_for_plan`。它連接到 `https://learn.microsoft.com/api/mcp`，並為每個技能缺口回傳真正的 Microsoft Learn 連結。

工具執行時你會看到這些日誌 - 都是預期內：

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

唯一需要擔心的是 `POST` 回傳錯誤時。

---

**上一節：** [00 - 前置條件](00-prerequisites.md) · **下一節：** [02 - 建立專案架構 →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->