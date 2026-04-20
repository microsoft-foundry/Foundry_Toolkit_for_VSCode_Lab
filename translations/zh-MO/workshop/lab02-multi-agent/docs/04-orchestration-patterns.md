# Module 4 - 編排模式

在本模組中，您將探索簡歷工作適配評估器中使用的編排模式，並學習如何閱讀、修改和擴展工作流圖。理解這些模式對於除錯資料流問題以及構建您自己的[多代理工作流](https://learn.microsoft.com/agent-framework/workflows/)至關重要。

---

## 模式 1：分叉（平行分支）

工作流中的第一個模式是<strong>分叉</strong>——將單一輸入同時傳送給多個代理。

```mermaid
flowchart LR
    A["用戶輸入"] --> B["履歷解析器"]
    A --> C["職位描述代理"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
```
在程式碼中，這是因為 `resume_parser` 是 `start_executor` —— 它最先接收用戶訊息。接著，因為 `jd_agent` 和 `matching_agent` 都有來自 `resume_parser` 的邊，框架會將 `resume_parser` 的輸出路由到這兩個代理：

```python
.add_edge(resume_parser, jd_agent)         # ResumeParser 輸出 → JD Agent
.add_edge(resume_parser, matching_agent)   # ResumeParser 輸出 → MatchingAgent
```

**為什麼這樣可行：** ResumeParser 和 JD Agent 處理同一輸入的不同面向。平行運行它們比依序執行可減少總延遲。

### 何時使用分叉

| 使用情況 | 範例 |
|----------|---------|
| 獨立子任務 | 解析簡歷 vs. 解析職務說明 |
| 冗餘 / 投票 | 兩個代理分析相同資料，第三個選擇最佳答案 |
| 多格式輸出 | 一個代理產生文本，另一個產生結構化 JSON |

---

## 模式 2：匯聚（聚合）

第二個模式是<strong>匯聚</strong>——收集多個代理輸出並傳送給單一下游代理。

```mermaid
flowchart LR
    B["履歷解析器"] --> D["匹配代理"]
    C["職位描述代理"] --> D

    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
```
在程式碼中：

```python
.add_edge(resume_parser, matching_agent)   # 簡歷解析器輸出 → 匹配代理
.add_edge(jd_agent, matching_agent)        # 工作描述代理輸出 → 匹配代理
```

**核心行為：** 當代理有<strong>兩條或以上的輸入邊</strong>時，框架會自動等待<strong>所有</strong>上游代理完成後才執行下游代理。MatchingAgent 會在 ResumeParser 和 JD Agent 都完成後才開始。

### MatchingAgent 收到的輸入

框架將所有上游代理的輸出串接在一起。MatchingAgent 的輸入類似：

```
[ResumeParser output]
---
Candidate Profile:
  Name: Jane Doe
  Technical Skills: Python, Azure, Kubernetes, ...
  ...

[JobDescriptionAgent output]
---
Role Overview: Senior Cloud Engineer
Required Skills: Python, Azure, Terraform, ...
...
```

> **注意：** 串接的確切格式取決於框架版本。代理的指示應撰寫為能處理結構化與非結構化的上游輸出。

![VS Code 偵錯主控台顯示 MatchingAgent 接收來自兩個上游代理串接的輸出](../../../../../translated_images/zh-MO/04-debug-console-matching-input.ed5c06395e25aec0.webp)

---

## 模式 3：序列鏈接

第三個模式是<strong>序列鏈接</strong>——一個代理的輸出直接作為下一個代理的輸入。

```mermaid
flowchart LR
    D["配對代理"] --> E["差距分析器"]

    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
```
在程式碼中：

```python
.add_edge(matching_agent, gap_analyzer)    # MatchingAgent 輸出 → GapAnalyzer
```

這是最簡單的模式。GapAnalyzer 接收 MatchingAgent 的適配分數、匹配/缺少技能與缺口。然後它針對每個缺口呼叫 [MCP 工具](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol) 以取得 Microsoft Learn 資源。

---

## 完整工作流程圖

結合這三種模式產生完整工作流程：

```mermaid
flowchart TD
    A["用戶輸入"] --> B["履歷解析器"]
    A --> C["職位說明代理"]
    B -->|"解析的簡歷"| D["配對代理"]
    C -->|"解析的需求"| D
    D -->|"匹配報告 + 差距"| E["差距分析器
    (+ MCP 工具)"]
    E --> F["最終輸出"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```
### 執行時間線

```mermaid
gantt
    title 代理執行時間表
    dateFormat X
    axisFormat %s

    section 平行
    Resume Parser       :rp, 0, 3
    JD Agent            :jd, 0, 2

    section 序列
    Matching Agent      :ma, 3, 5
    Gap Analyzer        :ga, 5, 9
```
> 總執行時間約為 `max(ResumeParser, JD Agent) + MatchingAgent + GapAnalyzer`。GapAnalyzer 通常是最慢的，因為它對每個缺口呼叫多次 MCP 工具。

---

## 閱讀 WorkflowBuilder 程式碼

以下是 `main.py` 中完整的 `create_workflow()` 函數，並附註說明：

```python
def create_workflow(resume_parser, jd_agent, matching_agent, gap_analyzer):
    workflow = (
        WorkflowBuilder(
            name="ResumeJobFitEvaluator",

            # 第一個接收用戶輸入的代理
            start_executor=resume_parser,

            # 輸出成為最終回應的代理
            output_executors=[gap_analyzer],
        )
        # 分流：ResumeParser 的輸出同時發送到 JD Agent 和 MatchingAgent
        .add_edge(resume_parser, jd_agent)
        .add_edge(resume_parser, matching_agent)

        # 匯流：MatchingAgent 等待 ResumeParser 和 JD Agent 兩者完成
        .add_edge(jd_agent, matching_agent)

        # 順序：MatchingAgent 的輸出用於 GapAnalyzer
        .add_edge(matching_agent, gap_analyzer)

        .build()
    )
    return workflow.as_agent()
```

### 邊緣摘要表

| # | 邊緣 | 模式 | 效果 |
|---|------|---------|--------|
| 1 | `resume_parser → jd_agent` | 分叉 | JD Agent 接收 ResumeParser 的輸出（加上原始用戶輸入） |
| 2 | `resume_parser → matching_agent` | 分叉 | MatchingAgent 接收 ResumeParser 的輸出 |
| 3 | `jd_agent → matching_agent` | 匯聚 | MatchingAgent 也接收 JD Agent 的輸出（等待兩者完成） |
| 4 | `matching_agent → gap_analyzer` | 序列 | GapAnalyzer 接收適配報告與缺口清單 |

---

## 修改圖表

### 新增代理

若要新增第五個代理（例如，根據缺口分析產生面試問題的 **InterviewPrepAgent**）：

```python
# 1. 定義指令
INTERVIEW_PREP_INSTRUCTIONS = """\
You are the Interview Prep Agent.
Given a gap analysis and fit report, generate 10 targeted interview questions
the candidate should prepare for.
"""

# 2. 創建代理（在 async with 區塊內）
AzureAIAgentClient(
    project_endpoint=PROJECT_ENDPOINT,
    model_deployment_name=MODEL_DEPLOYMENT_NAME,
    credential=credential,
).as_agent(
    name="InterviewPrepAgent",
    instructions=INTERVIEW_PREP_INSTRUCTIONS,
) as interview_prep,

# 3. 在 create_workflow() 中添加邊
.add_edge(matching_agent, interview_prep)   # 接收配合報告
.add_edge(gap_analyzer, interview_prep)     # 亦接收缺口卡

# 4. 更新 output_executors
output_executors=[interview_prep],  # 現在的最終代理
```

### 改變執行順序

讓 JD Agent 在 ResumeParser <strong>之後</strong>執行（由平行變成序列）：

```python
# 移除：.add_edge(resume_parser, jd_agent)  ← 已經存在，保留它
# 透過不讓 jd_agent 直接接收用戶輸入來移除隱含的並行
# start_executor 先發送到 resume_parser，jd_agent 僅通過邊獲取
# resume_parser 的輸出。這使它們成為順序執行。
```

> **重要提示：** `start_executor` 是唯一接收原始用戶輸入的代理。其他代理皆接收來自其上游邊的輸出。如果您希望某代理同時接收原始用戶輸入，該代理必須有來自 `start_executor` 的邊。

---

## 常見圖表錯誤

| 錯誤 | 症狀 | 解決方法 |
|---------|---------|-----|
| 缺少至 `output_executors` 的邊 | 代理有執行但輸出為空 | 確保存在從 `start_executor` 至每個 `output_executors` 的路徑 |
| 環狀依賴 | 無限迴圈或超時 | 確認沒有代理回傳給上游代理 |
| `output_executors` 中代理無輸入邊 | 輸出為空 | 新增至少一條 `add_edge(source, that_agent)` |
| 多個 `output_executors` 無匯聚 | 輸出僅包含一個代理回應 | 使用單一輸出代理聚合，或接受多重輸出 |
| 缺少 `start_executor` | 建構時出現 `ValueError` | 一定要在 `WorkflowBuilder()` 指定 `start_executor` |

---

## 除錯圖表

### 使用 Agent Inspector

1. 在本機啟動代理（F5 或終端機 - 參見 [Module 5](05-test-locally.md)）。
2. 打開 Agent Inspector (`Ctrl+Shift+P` → **Foundry Toolkit: Open Agent Inspector**)。
3. 發送測試訊息。
4. 在 Inspector 回應面板中，查看<strong>串流輸出</strong> —— 它可依序顯示每個代理的貢獻。

![Agent Inspector 顯示串流輸出並標示每個代理的貢獻](../../../../../translated_images/zh-MO/04-inspector-streaming-output.df2781aaa02df6bc.webp)

### 使用日誌記錄

在 `main.py` 中加入日誌記錄以追蹤資料流：

```python
import logging
logger = logging.getLogger("resume-job-fit")

# 在 create_workflow() 中，建立後：
logger.info("Workflow graph built with edges: RP→JD, RP→MA, JD→MA, MA→GA")
```

伺服器日誌顯示代理執行順序與 MCP 工具呼叫：

```
INFO:resume-job-fit:Starting Resume -> Job Fit Evaluator HTTP server...
INFO:resume-job-fit:Server running on http://localhost:8088
INFO:agent_framework:Executing agent: ResumeParser
INFO:agent_framework:Executing agent: JobDescriptionAgent
INFO:agent_framework:Waiting for upstream agents: ResumeParser, JobDescriptionAgent
INFO:agent_framework:Executing agent: MatchingAgent
INFO:agent_framework:Executing agent: GapAnalyzer
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Kubernetes")
POST https://learn.microsoft.com/api/mcp → 200
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Terraform")
POST https://learn.microsoft.com/api/mcp → 200
```

---

### 檢查點

- [ ] 您能識別工作流程中的三種編排模式：分叉、匯聚與序列鏈
- [ ] 您理解擁有多條輸入邊的代理會等待所有上游代理完成
- [ ] 您能閱讀 `WorkflowBuilder` 程式碼並將每個 `add_edge()` 呼叫對應到視覺化圖表
- [ ] 您了解執行時間線：先執行平行代理，再執行聚合，最後執行序列
- [ ] 您知道如何新增代理到圖表（定義指示、創建代理、新增邊、更新輸出）
- [ ] 您能識別常見圖表錯誤及其症狀

---

**上一節：** [03 - 配置代理與環境](03-configure-agents.md) · **下一節：** [05 - 本機測試 →](05-test-locally.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件是使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯的。雖然我們力求準確，但請注意自動翻譯可能存在錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。對於因使用此翻譯而引起的任何誤解或誤譯，我們不承擔任何責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->