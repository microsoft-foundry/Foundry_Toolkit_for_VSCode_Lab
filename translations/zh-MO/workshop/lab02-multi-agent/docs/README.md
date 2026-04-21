# Lab 02 - 多智能體工作流程：履歷 → 職務適配評估器

## 完整學習路徑

本文件引導你建立、測試及部署一個使用四個專門代理人，透過 **WorkflowBuilder** 進行協調的<strong>多智能體工作流程</strong>，用以評估履歷與職務的匹配度。

> **先決條件：** 請先完成 [Lab 01 - 單智能體](../../lab01-single-agent/README.md)，再開始 Lab 02。

---

## 模組

| # | 模組 | 你將進行的工作 |
|---|--------|---------------|
| 0 | [先決條件](00-prerequisites.md) | 確認完成 Lab 01，了解多智能體概念 |
| 1 | [理解多智能體架構](01-understand-multi-agent.md) | 學習 WorkflowBuilder、代理人角色、協調圖 |
| 2 | [建立多智能體專案框架](02-scaffold-multi-agent.md) | 使用 Foundry 擴充工具建立多智能體工作流程框架 |
| 3 | [設定代理人與環境](03-configure-agents.md) | 撰寫四個代理人的指令，設定 MCP 工具與環境變數 |
| 4 | [協調模式](04-orchestration-patterns.md) | 探索平行分支、序列聚合與替代模式 |
| 5 | [本機測試](05-test-locally.md) | 使用 Agent Inspector F5 偵錯，搭配履歷與職務說明進行測試 |
| 6 | [部署至 Foundry](06-deploy-to-foundry.md) | 建置容器，推送至 ACR，註冊託管代理人 |
| 7 | [在 Playground 驗證](07-verify-in-playground.md) | 在 VS Code 與 Foundry Portal playground 測試已部署代理人 |
| 8 | [疑難排解](08-troubleshooting.md) | 解決常見多智能體問題（MCP 錯誤、輸出截斷、套件版本） |

---

## 預估時間

| 經驗層級 | 時間 |
|-----------------|------|
| 最近完成 Lab 01 | 45-60 分鐘 |
| 有些 Azure AI 經驗 | 60-90 分鐘 |
| 首次接觸多智能體 | 90-120 分鐘 |

---

## 架構一覽

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

**返回：** [Lab 02 README](../README.md) · [工作坊首頁](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我哋致力確保準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件以其原文語言版本為權威依據。對於重要資訊，建議採用專業人工翻譯。我哋對因使用此翻譯所引起嘅任何誤解或誤譯概不負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->