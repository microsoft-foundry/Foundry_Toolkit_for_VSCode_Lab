# 實驗室 02 - 多代理工作流程：履歷 → 職務適配評估器

## 完整學習路徑

本文件將引導你建立、測試及部署一個透過四個專業代理由 **WorkflowBuilder** 編排的<strong>多代理工作流程</strong>，用以評估履歷與職務的適配度。

> **先決條件：** 在開始實驗室 02 前，請先完成 [實驗室 01 - 單代理](../../lab01-single-agent/README.md)。

---

## 模組

| # | 模組 | 你將進行的內容 |
|---|--------|---------------|
| 0 | [介紹](00-prerequisites.md) | 你會建立什麼、實驗室 01 驗證、實驗室 02 與實驗室 01 比較 |
| 1 | [了解多代理架構](01-understand-multi-agent.md) | 學習 WorkflowBuilder、代理角色、編排圖 |
| 2 | [建立多代理專案骨架](02-scaffold-multi-agent.md) | 使用 Foundry 擴充功能精靈建立基礎專案 |
| 3 | [配置代理與環境](03-configure-agents.md) | 撰寫 4 個代理的指令，配置 MCP 工具，設定環境變數 |
| 4 | [編排模式](04-orchestration-patterns.md) | 依序鏈結、內容轉接及 WorkflowBuilder 的 OR 語義 |
| 5 | [本地測試](05-test-locally.md) | 使用 Agent Inspector 進行 F5 除錯，使用履歷+職務說明運行快速測試 |
| 6 | [部署至 Foundry](06-deploy-to-foundry.md) | 建構容器，推送至 ACR，註冊託管代理 |
| 7 | [於 Playground 驗證](07-verify-in-playground.md) | 在 VS Code 與 Foundry Portal playground 測試已部署代理 |
| 8 | [故障排除](08-troubleshooting.md) | 修正常見多代理問題 (MCP 錯誤、輸出截斷、套件版本) |
| 9 | [總結與後續步驟](09-summary.md) | 你建立了什麼、學到的關鍵概念、清理及後續方向 |

---

**返回：** [實驗室 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->