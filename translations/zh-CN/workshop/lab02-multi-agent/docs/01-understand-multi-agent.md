# 模块 1 - 理解架构

⏱️ 大约 5 分钟

在编写任何代码之前，先快速了解一下你正在构建的内容以及它的工作原理。

---

## 你正在构建的内容

你粘贴一个<strong>简历</strong>和一个<strong>职位描述</strong>。工作流程返回：

- 一个匹配度分数（0–100，并带有细分）
- 一份技能和认证缺口清单
- 一份个性化学习路线图，针对每个缺口包含 Microsoft Learn 链接

---

## 四个代理

单个代理试图一次性解析、评分和规划，往往会匆忙且产生浅显的输出。将工作拆分为四个专门代理，能产生更好的结果：

| 代理 | 功能 |
|-------|-------------|
| **ResumeParser** | 解析简历；将职位描述逐字复制到 `[JOB DESCRIPTION PASS-THROUGH]` 供下游代理使用 |
| **JobDescriptionAgent** | 从传递内容中提取职位要求；将 `[PARSED RESUME]` 转发为 `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | 比较两个标记区域；生成0–100的匹配分数和缺口列表 |
| **GapAnalyzer** | 构建学习路线图；为每个缺口在 Microsoft Learn 中搜索相关内容 |

---

## 编排图

工作流程是一个<strong>顺序管道</strong>——每个代理将其输出传递给下一个：

```mermaid
flowchart LR
    A["用户输入"] --> B["简历解析器"]
    B -- "解析的简历 + 职位描述转发" --> C["职位描述代理"]
    C -- "职位需求 + 简历转发" --> D["匹配代理"]
    D -- "适配报告 + 差距" --> E["差距分析器 + MCP"]
    E --> F["最终输出"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** 接收用户输入，解析简历，并将职位描述复制到 `[JOB DESCRIPTION PASS-THROUGH]`。
2. **JD代理** 提取结构化要求，转发 `[PARSED RESUME PASS-THROUGH]`。
3. **MatchingAgent** 比较两个部分，生成匹配分数和缺口列表。
4. **GapAnalyzer** 构建路线图，并为每个缺口调用 Microsoft Learn MCP 工具。

---

## 这如何映射到代码

在 `main.py` 中，你使用 `WorkflowBuilder` 描述这个图：

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # 第一个接收用户输入的代理
        output_executors=[gap_executor],      # 最后一个代理 - 它的输出即为响应
    )
    .add_edge(resume_executor, jd_executor)       # 简历解析器 → 职位代理
    .add_edge(jd_executor, matching_executor)     # 职位代理 → 匹配代理
    .add_edge(matching_executor, gap_executor)    # 匹配代理 → 间隙分析器
    .build()
    .as_agent()
)
```

每个 `Agent` 被包裹在 `AgentExecutor` 中。`add_edge()` 调用定义了严格的顺序管道——每个代理只接收其直接前驱的输出。

> `context_mode="last_agent"` 表示每个执行器只看到其直接前驱的输出。ResumeParser 和 JD代理在标记区域中转发数据，因此每个下游代理正好获得所需内容。

---

## MCP 工具

GapAnalyzer 有一个工具：`search_microsoft_learn_for_plan`。它连接到 `https://learn.microsoft.com/api/mcp`，为每个技能缺口返回真实的 Microsoft Learn 链接。

当工具运行时，你会看到这些日志——都是预期中的：

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

只有当 `POST` 返回错误时才需要担心。

---

**上一节：** [00 - 前提条件](00-prerequisites.md) · **下一节：** [02 - 搭建项目骨架 →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->