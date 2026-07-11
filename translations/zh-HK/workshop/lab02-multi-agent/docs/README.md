# 實驗室 02 - 多代理工作流程：履歷 → 職務適配評估器

## 全學習路徑

本文件將帶您完成建立、測試及部署一個<strong>多代理工作流程</strong>，該流程使用 4 個專門代理藉由 **WorkflowBuilder** 進行協調，以評估履歷與職務的適配度。

> <strong>先決條件：</strong>開始實驗室 02 前，請先完成[實驗室 01 - 單一代理](../../lab01-single-agent/README.md)。

---

## 模組

| # | 模組 | 您將進行的內容 |
|---|--------|---------------|
| 0 | [介紹](00-prerequisites.md) | 您將打造的內容、實驗室 01 驗證、實驗室 02 與 01 之比較 |
| 1 | [了解多代理架構](01-understand-multi-agent.md) | 學習 WorkflowBuilder、代理角色、協調圖 |
| 2 | [搭建多代理專案骨架](02-scaffold-multi-agent.md) | 使用 Foundry 擴充精靈搭建基底專案 |
| 3 | [配置代理及環境](03-configure-agents.md) | 撰寫 4 個代理的指示，配置 MCP 工具，設定環境變數 |
| 4 | [協調模式](04-orchestration-patterns.md) | 連續鏈、內容中繼，以及 WorkflowBuilder 的 OR 語意 |
| 5 | [本地測試](05-test-locally.md) | 使用 Agent Inspector 進行 F5 除錯，搭配履歷及職務說明執行冒煙測試 |
| 6 | [部署至 Foundry](06-deploy-to-foundry.md) | 建立容器、推送至 ACR、註冊託管代理 |
| 7 | [於 Playground 驗證](07-verify-in-playground.md) | 在 VS Code 與 Foundry Portal playground 中測試部署的代理 |
| 8 | [疑難排解](08-troubleshooting.md) | 修正常見多代理問題（MCP 錯誤、輸出截斷、套件版本） |
| 9 | [總結與後續步驟](09-summary.md) | 您所打造的內容、學到的核心概念、清理以及下一步方向 |

---

**返回：** [實驗室 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->