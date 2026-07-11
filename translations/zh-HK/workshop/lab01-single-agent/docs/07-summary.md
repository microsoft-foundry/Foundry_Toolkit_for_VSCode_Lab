# 模組 7 - 總結與後續步驟

⏱️ 約 5 分鐘

**恭喜！** 你已使用 Microsoft Foundry 及 Foundry Toolkit for VS Code 建立、測試並（如果走路徑 A）部署了一個託管的 AI 代理。

---

## 你建立的內容

一個 **「用執行長容易理解的方式解釋」** 代理，能夠：
- 透過 HTTP (`POST /responses`) 接收技術事件報告或運維更新
- 將它們轉換成淺顯易懂的執行摘要
- 遵循結構化的輸出格式（發生了什麼 / 商業影響 / 下一步）
- 拒絕偏離主題的請求及提示注入攻擊
- 以容器化方式在 Microsoft Foundry Agent Service 中運行

---

## 你學到的關鍵概念

| 概念 | 你練習的項目 |
|---------|-------------------|
| <strong>代理框架架構</strong> | `FoundryChatClient` → `Agent` → `ResponsesHostServer` 流程 |
| <strong>託管代理生命週期</strong> | 搭建骨架 → 配置 → 本機測試 → 部署 → 雲端驗證 |
| <strong>系統提示工程</strong> | 角色、受眾、輸出格式、規則、安全限制及示例 |
| <strong>本機與託管差異</strong> | 身份（個人認證 vs. 托管身份）、端點、網路路徑 |
| <strong>安全邊界</strong> | 抵禦提示注入、角色遵守、優雅處理邊緣案例 |
| **Foundry Toolkit 流程** | 專案建立、模型部署、代理骨架建立、代理檢查器、一鍵部署 |

---

## 你完成的工作

### 路徑 A（Foundry 訂閱）

- [x] 設定 Foundry Toolkit 並建立一個有部署模型的 Foundry 專案
- [x] 搭建了自動生成專案結構的託管代理骨架
- [x] 撰寫有安全規則的結構化代理指令
- [x] 使用 3 個功能場景在本機測試（代理檢查器）
- [x] 部署至 Foundry Agent Service（容器化）
- [x] 在雲端遊樂場用 4 個邊緣/安全測試驗證

### 路徑 B（Foundry Local）

- [x] 設定 Foundry Toolkit 並使用本機模型端點
- [x] 搭建託管代理專案骨架
- [x] 撰寫有安全規則的結構化代理指令
- [x] 使用 3 個功能場景在本機測試
- [x] 驗證代理行為且不需雲端資源

---

## 後續步驟

### 繼續學習

| 資源 | 說明 |
|----------|-------------|
| **[Lab 02 - 多代理協調](../../lab02-multi-agent/docs/README.md)** | 建立一個 4 代理的工作流程（履歷 → 職務適配評估器）並運用協調模式 |
| **[為你的代理添加工具](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | 透過工具目錄連接 API、資料庫或自訂函式 |
| **[添加知識 (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 以文件、向量庫或 Bing 搜尋紮根你的代理 |
| **[Microsoft Foundry 文件](https://learn.microsoft.com/azure/foundry/)** | 完整平台參考 |
| **[代理框架 SDK 參考](https://learn.microsoft.com/agent-framework/)** | `agent-framework` 套件的 API 文件 |
| **[Foundry Toolkit - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 擴充功能發行說明及變更紀錄 |

### 擴展你的代理的想法

- <strong>新增日期工具</strong> - 讓代理在摘要中包含「截至今日」的時間背景
- <strong>連接至事件資料庫</strong> - 透過工具函式提取真實事件細節
- **新增 Bing 紮根工具** - 讓代理查詢近期新聞以獲得額外脈絡
- <strong>嘗試不同模型</strong> - 比較 `gpt-4.1` 與 `gpt-4.1-mini` 的輸出品質
- **用 Foundry 評估** - 利用評估功能於大規模評量代理品質

### 給路徑 B 使用者：升級到雲端部署

當你準備好部署到雲端時：
1. 取得 Azure 訂閱 ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. 完成 [模組 01，設定](01-setup.md#step-2-set-up-based-on-your-access)（建立專案、部署模型、指派 RBAC）
3. 更新你的 `.env` 檔案，加入 Foundry 專案端點及模型部署名稱
4. 從 [模組 05 - 部署到 Foundry](05-deploy-to-foundry.md) 繼續

---

## 清理資源（選擇性）

如果你想移除工作坊過程中建立的 Azure 資源：

### 選項 1：刪除資源群組（會刪除所有內容）

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 選項 2：僅刪除託管代理

1. 開啟 [ai.azure.com](https://ai.azure.com) → 你的專案 → <strong>建置</strong> → <strong>代理</strong>。
2. 點擊你的代理 → 點擊 <strong>刪除</strong>。

### 選項 3：刪除模型部署

1. 在 Foundry 側欄，展開你的專案 → <strong>模型</strong>。
2. 右鍵點擊模型部署 → <strong>刪除</strong>。

> **費用說明：** 託管代理只在運行時計費。若停止或刪除代理，則不會持續產生費用。模型部署可能會因保留容量而產生少量費用 - 若不再使用請刪除。

---

**上一節：** [06 - 在遊樂場驗證](06-verify-in-playground.md) · **下一節：** [08 - 疑難排解（參考）→](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->