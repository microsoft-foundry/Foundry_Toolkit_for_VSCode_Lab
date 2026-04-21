# Lab 02 - 多代理工作流程：履歷 → 職位匹配評估器

## 完整學習路徑

本文件將引導你建立、測試及部署一個利用四個專業代理並由 **WorkflowBuilder** 協調的 <strong>多代理工作流程</strong>，用於評估履歷與職位的匹配度。

> **先決條件：** 請先完成 [Lab 01 - 單代理](../../lab01-single-agent/README.md) 再開始 Lab 02。

---

## 模組

| # | 模組 | 你將做什麼 |
|---|--------|---------------|
| 0 | [先決條件](00-prerequisites.md) | 驗證 Lab 01 完成狀況，理解多代理概念 |
| 1 | [了解多代理架構](01-understand-multi-agent.md) | 學習 WorkflowBuilder、代理角色及協調圖 |
| 2 | [搭建多代理專案框架](02-scaffold-multi-agent.md) | 使用 Foundry 擴充功能搭建多代理工作流程 |
| 3 | [配置代理及環境](03-configure-agents.md) | 撰寫 4 個代理指令，配置 MCP 工具，設定環境變數 |
| 4 | [協調模式](04-orchestration-patterns.md) | 探索平行分支、序列聚合及替代模式 |
| 5 | [本機測試](05-test-locally.md) | 使用 Agent Inspector 進行 F5 除錯，搭配履歷與職位描述執行冒煙測試 |
| 6 | [部署至 Foundry](06-deploy-to-foundry.md) | 建置容器，推送至 ACR，註冊託管代理 |
| 7 | [在 Playground 驗證](07-verify-in-playground.md) | 在 VS Code 與 Foundry 入口網站 playground 中測試已部署代理 |
| 8 | [故障排除](08-troubleshooting.md) | 修正常見多代理問題（MCP 錯誤、輸出截斷、套件版本） |

---

## 預估時間

| 經驗程度 | 時間 |
|-----------------|------|
| 最近完成 Lab 01 | 45-60 分鐘 |
| 有部分 Azure AI 經驗 | 60-90 分鐘 |
| 第一次接觸多代理 | 90-120 分鐘 |

---

## 架構概覽

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**回到：** [Lab 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件經由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威資料來源。對於重要資訊，建議聘用專業人工翻譯。我們對因使用此翻譯而引起的任何誤解或錯誤詮釋概不負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->