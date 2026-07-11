# 實驗室 02 - 多代理工作流程：履歷 → 工作適配評估器

## 完整學習路徑

本文件將引導你建立、測試及部署一個<strong>多代理工作流程</strong>，此流程使用四個專業代理，透過<strong>WorkflowBuilder</strong>協調，來評估履歷與工作的匹配度。

> **先決條件：** 在開始實驗室 02 前，請先完成 [實驗室 01 - 單一代理](../../lab01-single-agent/README.md)。

---

## 模組

| # | 模組 | 你將會做什麼 |
|---|--------|---------------|
| 0 | [介紹](00-prerequisites.md) | 你將建造什麼、實驗室 01 驗證、實驗室 02 與實驗室 01 的比較 |
| 1 | [了解多代理架構](01-understand-multi-agent.md) | 學習 WorkflowBuilder、代理角色、協調圖 |
| 2 | [搭建多代理專案框架](02-scaffold-multi-agent.md) | 使用 Foundry 擴充精靈來搭建基礎專案 |
| 3 | [配置代理與環境](03-configure-agents.md) | 撰寫四個代理的指令，配置 MCP 工具，設置環境變數 |
| 4 | [協調模式](04-orchestration-patterns.md) | 順序鏈、內容轉送，以及 WorkflowBuilder 的 OR 語義 |
| 5 | [本地測試](05-test-locally.md) | 使用 Agent Inspector 進行 F5 除錯，以履歷和職務說明進行煙霧測試 |
| 6 | [部署到 Foundry](06-deploy-to-foundry.md) | 建構容器，推送到 ACR，註冊託管代理 |
| 7 | [在 Playground 驗證](07-verify-in-playground.md) | 在 VS Code 及 Foundry Portal playground 測試已部署的代理 |
| 8 | [故障排解](08-troubleshooting.md) | 修正常見的多代理問題（MCP 錯誤、截斷輸出、套件版本） |
| 9 | [總結與下一步](09-summary.md) | 你建造了什麼、學到的關鍵概念、清理以及下一步去哪裡 |

---

**返回：** [實驗室 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->