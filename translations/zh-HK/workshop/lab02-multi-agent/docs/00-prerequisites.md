# 模組 0 - 介紹

⏱️ 約 10 分鐘

> [!WARNING]
> **預覽與限制：** [Hosted Agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) 目前處於 <strong>公開預覽</strong> 階段，不建議用於生產工作負載。本工作坊中展示的一些功能，隨著服務邁向正式發布可能會變更。

## 你將會構建什麼

在本實驗中，你將擴充實驗 01 中的單一代理技能，建立一個 <strong>多代理工作流程</strong> —— 履歷 → 職務匹配評估器。

你會貼上 <strong>履歷</strong> 及 <strong>職務說明</strong>。四個專精代理會依序處理輸入，然後回傳：
- 配合度分數（0–100，含分數細目）
- 技能與認證缺口清單
- 針對每個缺口附帶實際 Microsoft Learn 連結的個人化學習路線圖

**此工作流程使用：**
- **Microsoft Agent Framework** - `WorkflowBuilder` 用於序列管線編排
- **Foundry Toolkit for VS Code** - 搭建框架、本地測試、部署
- **一個 AI 模型** (例如 `gpt-4.1-mini`) - 被所有四個代理使用
- **Microsoft Learn MCP 伺服器** - 為每個技能缺口提供真實的學習資源連結

---

## 選擇你的路徑

> ⚠️ **請繼續使用你在實驗 01 中所使用的相同路徑。**

<details open>
<summary><strong>🅰️ 路徑 A - Azure 雲端 (需要 Azure 訂閱)</strong></summary>

| | 詳情 |
|---|---|
| **適合對象？** | 你已使用 Azure 訂閱完成實驗 01 |
| <strong>模型</strong> | 透過 Foundry 使用 Azure OpenAI (例如 `gpt-4.1-mini`) |
| <strong>涵蓋模組</strong> | 所有模組 (00–09) |
| **部署到雲端？** | ✅ 是 - 完整的端到端部署 |

</details>

<details open>
<summary><strong>🅱️ 路徑 B - Foundry Local (無需 Azure 訂閱)</strong></summary>

| | 詳情 |
|---|---|
| **適合對象？** | 你已使用 Foundry Local 完成實驗 01 |
| <strong>模型</strong> | Foundry Local (免費，在你的機器上運行) |
| <strong>涵蓋模組</strong> | 模組 00–05 (跳過 06–07 - 部署與雲端驗證) |
| **部署到雲端？** | ❌ 否 - 僅限透過代理檢查器本地測試 |

</details>

---

## 實驗 01 檢查

實驗 02 是直接建立在實驗 01 之上。請先完成實驗 01 再開始這裡。

尚未做過實驗 01 嗎？請從這裡開始：[實驗 01 - 介紹](../../lab01-single-agent/docs/00-prerequisites.md)

<details open>
<summary><strong>🅰️ 路徑 A - Azure 雲端</strong></summary>

```powershell
az account show --query "{name:name, id:id}" --output table
```

如果失敗，請執行 `az login`。然後在 VS Code 中驗證：

1. `Ctrl+Shift+P` → 輸入 **Foundry Toolkit** → 確認命令是否出現。
2. 點擊 **Foundry Toolkit** 圖示 → 你的專案和部署模型顯示 <strong>成功</strong>。

![Foundry Toolkit 側邊欄顯示 My Resources 下的專案，並開啟切換專案 / 建立專案選擇器](../../../../../translated_images/zh-HK/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

> **RBAC：** 你在實驗 01 中已指派 **Foundry User**。若需重新指派，請參閱 [實驗 01，第 1 模組](../../lab01-single-agent/docs/01-setup.md#deploy-a-model--assign-rbac)。該角色原名為 **Azure AI User** - 權限相同。

</details>

<details open>
<summary><strong>🅱️ 路徑 B - Foundry Local</strong></summary>

```powershell
Invoke-WebRequest -Uri "http://localhost:5273/v1/health" -UseBasicParsing | Select-Object StatusCode
```

預期結果：`StatusCode: 200`。若無，請從 Foundry Toolkit 側邊欄重新啟動 Foundry Local。

> 所有推論都在你的機器上運行。唯一的外部呼叫是 MCP 工具到 `https://learn.microsoft.com/api/mcp`。

</details>

---

## 實驗 02 新增內容

| | 實驗 01 | 實驗 02 |
|--|--------|--------|
| 代理 | 1 | 4 (與 WorkflowBuilder 連鎖) |
| 骨架範本 | 基本 - 代理框架 | 工作流程 - 代理框架 |
| 新套件 | - | `mcp` |
| 編排 | 單一對話代理 | 順序流程 (WorkflowBuilder) |
| 新工具 | - | `search_microsoft_learn_for_plan` (MCP) |

---

**下一步：** [01 - 了解架構 →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->