# 模組 7 - 總結與後續步驟

⏱️ 約 5 分鐘

**恭喜！** 您已使用 Microsoft Foundry 和 Foundry Toolkit for VS Code 建立、測試並（如果是路徑 A）部署了一個託管的 AI 代理。

---

## 您建立了什麼

一個 **「解釋給我這位主管聽」** 的代理，具有以下功能：
- 透過 HTTP (`POST /responses`) 接收技術事故報告或運營更新
- 把它們翻譯成簡明易懂的主管摘要
- 遵循結構化輸出格式（發生了什麼 / 商業影響 / 下一步）
- 拒絕題外請求和提示注入嘗試
- 作為容器化的託管代理運行於 Microsoft Foundry Agent 服務中

---

## 學到的主要概念

| 概念 | 您實作了什麼 |
|---------|-------------------|
| <strong>代理框架架構</strong> | `FoundryChatClient` → `Agent` → `ResponsesHostServer` 流程 |
| <strong>託管代理生命週期</strong> | 支架 → 配置 → 本地測試 → 部署 → 雲端驗證 |
| <strong>系統提示工程</strong> | 角色、受眾、輸出格式、規則、安全限制及範例 |
| <strong>本地與託管差異</strong> | 身份（個人憑證 vs. 管理身份）、端點、網絡路徑 |
| <strong>安全邊界</strong> | 提示注入防禦、角色遵循、優雅處理邊緣案例 |
| **Foundry Toolkit 工作流程** | 專案建立、模型部署、代理腳手架、Agent Inspector、一鍵部署 |

---

## 您完成了什麼

### 路徑 A（Foundry 訂閱）

- [x] 設置 Foundry Toolkit 並建立一個含有已部署模型的 Foundry 專案
- [x] 腳手架化一個帶自動生成專案結構的託管代理
- [x] 寫出具安全規則的結構化代理說明
- [x] 使用三個功能場景在本地測試 (Agent Inspector)
- [x] 部署到 Foundry Agent 服務（容器化）
- [x] 在雲端遊樂場以四個邊緣案例/安全測試驗證

### 路徑 B（Foundry 本地）

- [x] 設置 Foundry Toolkit 並用本地模型端點
- [x] 腳手架化一個託管代理專案
- [x] 寫出具安全規則的結構化代理說明
- [x] 使用三個功能場景在本地測試
- [x] 驗證代理行為，不需雲端資源

---

## 後續步驟

### 持續學習

| 資源 | 說明 |
|----------|-------------|
| **[實驗室 02 - 多代理協調](../../lab02-multi-agent/docs/README.md)** | 建立一個包含 4 個代理的工作流程（履歷 → 工作適配評估員）及協調模式 |
| **[為您的代理新增工具](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | 透過工具目錄連接 API、資料庫或自訂功能 |
| **[新增知識 (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 讓您的代理有文件、向量存儲或 Bing 搜尋作為根基 |
| **[Microsoft Foundry 文件](https://learn.microsoft.com/azure/foundry/)** | 完整平台參考 |
| **[Agent Framework SDK 參考](https://learn.microsoft.com/agent-framework/)** | `agent-framework` 套件的 API 文件 |
| **[Foundry Toolkit - 新功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 擴充功能發行說明與變更日誌 |

### 擴展您代理的點子

- <strong>新增日期工具</strong> - 讓代理摘要時包含「截至今天」的語境
- <strong>連接事故資料庫</strong> - 透過工具功能取得真實事故細節
- **新增 Bing 根基工具** - 讓代理查詢最新新聞以取得額外語境
- <strong>嘗試不同模型</strong> - 比較 `gpt-4.1` 與 `gpt-4.1-mini` 的輸出品質
- **使用 Foundry 評估** - 利用評估功能大規模測量代理質量

### 路徑 B 使用者：升級到雲端部署

當您準備好部署到雲端：
1. 申請 Azure 訂閱 ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. 完成 [模組 01，設定](01-setup.md#step-2-set-up-based-on-your-access) （建立專案、部署模型、指派 RBAC）
3. 更新您的 `.env` 檔案，填入 Foundry 專案端點與模型部署名稱
4. 從 [模組 05 - 部署到 Foundry](05-deploy-to-foundry.md) 繼續

---

## 清理資源（可選）

如果您想移除本研討會期間建立的 Azure 資源：

### 選項 1：刪除資源群組（會移除所有資源）

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 選項 2：只刪除託管代理

1. 開啟 [ai.azure.com](https://ai.azure.com) → 您的專案 → <strong>建立</strong> → <strong>代理</strong>。
2. 點選您的代理 → 點選 <strong>刪除</strong>。

### 選項 3：刪除模型部署

1. 在 Foundry 側邊欄展開您的專案 → <strong>模型</strong>。
2. 右鍵點擊模型部署 → <strong>刪除</strong>。

> **費用提示：** 託管代理只於執行時產生費用。如果您停止或刪除代理，則不會持續扣費。模型部署可能因保留容量而產生少量費用 - 用畢請刪除。

---

**前一篇：** [06 - 在遊樂場驗證](06-verify-in-playground.md) · **下一篇：** [08 - 疑難排解（參考）→](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->