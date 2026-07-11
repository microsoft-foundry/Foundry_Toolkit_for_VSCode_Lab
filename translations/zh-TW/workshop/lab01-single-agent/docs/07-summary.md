# 模組 7 - 總結與後續步驟

⏱️ ~5 分鐘

**恭喜！** 你已使用 Microsoft Foundry 和 Foundry Toolkit for VS Code 建立、測試，並（如果是路徑 A）部署了一個託管的 AI 代理。

---

## 你所建立的內容

一個 **「用主管能理解的方式解釋」** 代理，具備以下功能：
- 接收透過 HTTP 的技術事件報告或營運更新（`POST /responses`）
- 將其翻譯為簡明易懂的主管摘要
- 遵循結構化的輸出格式（發生了什麼／商業影響／後續步驟）
- 拒絕與主題無關的請求及提示注入攻擊
- 以容器化託管代理在 Microsoft Foundry Agent Service 中運行

---

## 學習到的關鍵概念

| 概念 | 你練習了什麼 |
|---------|-------------------|
| **Agent Framework 架構** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` 流程 |
| <strong>托管代理生命週期</strong> | 搭建架構 → 配置 → 本地測試 → 部署 → 雲端驗證 |
| <strong>系統提示工程</strong> | 角色、受眾、輸出格式、規則、安全限制與範例 |
| **本地 vs. 托管 差異** | 身份（個人憑證 vs. 管理身份）、端點、網路路徑 |
| <strong>安全邊界</strong> | 防止提示注入、角色遵守、邊緣狀況的優雅處理 |
| **Foundry Toolkit 工作流程** | 專案建立、模型部署、代理搭建、Agent Inspector、點擊即部署 |

---

## 你完成的事項

### 路徑 A（Foundry 訂閱）

- [x] 設定 Foundry Toolkit 並建立帶有已部署模型的 Foundry 專案
- [x] 搭建具自動產生專案結構的托管代理
- [x] 撰寫包含安全規則的結構化代理指令
- [x] 使用 3 個功能場景在本地測試（Agent Inspector）
- [x] 部署至 Foundry Agent Service（容器化）
- [x] 在雲端遊樂場以 4 個邊緣案例 / 安全測試驗證

### 路徑 B（Foundry Local）

- [x] 設定 Foundry Toolkit 與本地模型端點
- [x] 搭建托管代理專案
- [x] 撰寫包含安全規則的結構化代理指令
- [x] 使用 3 個功能場景在本地測試
- [x] 在不需雲端資源下驗證代理行為

---

## 後續步驟

### 持續學習

| 資源 | 說明 |
|----------|-------------|
| **[Lab 02 - 多代理協調](../../lab02-multi-agent/docs/README.md)** | 建立 4 代理工作流程（履歷→職務適配評估）與協調模式 |
| **[為代理加入工具](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | 透過工具目錄連接 API、資料庫或自訂函數 |
| **[加入知識（RAG）](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 以文件、向量庫或 Bing 搜尋為代理扎根 |
| **[Microsoft Foundry 文件](https://learn.microsoft.com/azure/foundry/)** | 平台完整參考 |
| **[Agent Framework SDK 參考](https://learn.microsoft.com/agent-framework/)** | `agent-framework` 套件 API 文件 |
| **[Foundry Toolkit - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 擴充套件發布說明與變更記錄 |

### 擴充代理的想法

- <strong>新增日期工具</strong> - 讓代理在摘要中包含「截至今日」的時效背景
- <strong>連接事故資料庫</strong> - 透過工具函數取得實際事故細節
- **新增 Bing 扎根工具** - 讓代理查詢近期新聞以獲取更多背景
- <strong>嘗試不同模型</strong> - 比較 `gpt-4.1` 與 `gpt-4.1-mini` 的輸出品質
- **使用 Foundry 評估** - 利用評估功能大規模測量代理品質

### 路徑 B 使用者：升級到雲端部署

當你準備好部署至雲端時：
1. 取得 Azure 訂閱（[azure.microsoft.com/free](https://azure.microsoft.com/free/)）
2. 完成 [模組 01，設定](01-setup.md#step-2-set-up-based-on-your-access)（建立專案、部署模型、指派 RBAC）
3. 更新你的 `.env`，設定 Foundry 專案端點和模型部署名稱
4. 從 [模組 05 - 部署到 Foundry](05-deploy-to-foundry.md) 繼續

---

## 清理資源（選擇性）

如果你想移除本工作坊期間建立的 Azure 資源：

### 選項 1：刪除資源群組（會移除所有東西）

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 選項 2：只刪除託管代理

1. 開啟 [ai.azure.com](https://ai.azure.com) → 你的專案 → <strong>建置</strong> → <strong>代理</strong>。
2. 點選你的代理 → 點選 <strong>刪除</strong>。

### 選項 3：刪除模型部署

1. 在 Foundry 側邊欄展開你的專案 → <strong>模型</strong>。
2. 右鍵點擊模型部署 → <strong>刪除</strong>。

> **費用提示：** 託管代理僅在運作時產生費用。若停止或刪除代理，則不會有持續費用。模型部署在保留容量時可能產生少量費用 - 如不再需要，請刪除。

---

**上一節：** [06 - 在遊樂場驗證](06-verify-in-playground.md) · **下一節：** [08 - 疑難排解（參考）→](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->