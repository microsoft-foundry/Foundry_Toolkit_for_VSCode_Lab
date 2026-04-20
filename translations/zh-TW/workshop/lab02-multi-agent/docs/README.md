# Lab 02 - 多代理工作流程：履歷 → 職缺匹配評估器

## 完整學習路徑

本文件引導您建立、測試並部署一個使用四個專門代理人，並透過 **WorkflowBuilder** 編排的 <strong>多代理工作流程</strong>，來評估履歷與職缺的匹配度。

> **前置條件：** 請先完成 [Lab 01 - 單一代理人](../../lab01-single-agent/README.md)，再開始 Lab 02。

---

## 模組

| # | 模組 | 你將會做什麼 |
|---|--------|---------------|
| 0 | [前置條件](00-prerequisites.md) | 驗證 Lab 01 完成狀況，理解多代理概念 |
| 1 | [理解多代理架構](01-understand-multi-agent.md) | 學習 WorkflowBuilder、代理角色、編排圖 |
| 2 | [搭建多代理專案骨架](02-scaffold-multi-agent.md) | 使用 Foundry 擴充工具搭建多代理工作流程骨架 |
| 3 | [設定代理及環境](03-configure-agents.md) | 撰寫 4 位代理指令碼，設定 MCP 工具，設置環境變數 |
| 4 | [編排模式](04-orchestration-patterns.md) | 探索平行風扇展開、序列彙整及替代模式 |
| 5 | [本地測試](05-test-locally.md) | 使用 Agent Inspector F5 偵錯，搭配履歷與職缺說明進行簡測 |
| 6 | [部署至 Foundry](06-deploy-to-foundry.md) | 建置容器、推送至 ACR、註冊托管代理 |
| 7 | [於 Playground 驗證](07-verify-in-playground.md) | 在 VS Code 及 Foundry Portal playground 測試部署的代理 |
| 8 | [故障排除](08-troubleshooting.md) | 修正常見多代理問題（MCP 錯誤、輸出截斷、套件版本） |

---

## 預估時間

| 經驗程度 | 時間 |
|-----------------|------|
| 最近完成 Lab 01 | 45-60 分鐘 |
| 有些 Azure AI 經驗 | 60-90 分鐘 |
| 初次接觸多代理 | 90-120 分鐘 |

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
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。儘管我們力求準確，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->