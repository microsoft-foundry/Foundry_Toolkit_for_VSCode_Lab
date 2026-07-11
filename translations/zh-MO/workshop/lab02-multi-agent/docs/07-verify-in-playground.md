# 模組 7 - 在 Playground 驗證

⏱️ 約 10 分鐘

在本模組中，您將在 VS Code 與 Foundry Portal 中測試您的已部署多代理工作流，確認代理的行為與本地測試一致。

---

## 為什麼部署後還要再測試？

主機環境與本地環境在幾個重要方面有所不同：

| | 本地 | 主機 |
|--|-------|--------|
| <strong>身份</strong> | 您的個人登入（`DefaultAzureCredential`） | 每個代理專用的 Entra 身份（部署時自動配置） |
| <strong>端點</strong> | `http://localhost:8088/responses` | 由 Foundry Agent Service 管理的 URL |
| <strong>網路</strong> | 您的機器 → Azure OpenAI + MCP | Azure 主幹網路（較低延遲） |

環境變數配置錯誤、RBAC 問題或 MCP 出站呼叫被阻擋，會先在這裡顯示。

---

## 選項 A：在 VS Code Playground 測試（建議優先）

### 步驟 1：導覽至您的主機代理

1. 點擊活動列的 **Foundry Toolkit** 圖示。
2. 展開您的專案 → **Hosted Agents (Preview)** → 找到您的代理。

![Foundry Toolkit 側邊欄顯示 Hosted Agents (Preview)，包含 resume-job-fit-evaluator 及其已部署版本](../../../../../translated_images/zh-MO/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### 步驟 2：選擇版本

1. 點擊代理以展開其版本列表。
2. 點擊 `v1` → 確認狀態為 **active**（側邊欄可能顯示「Running」或「Started」，兩者皆表示已就緒）。

### 步驟 3：開啟 Playground

1. 點擊 **Playground**（或右鍵版本 → **Open in Playground**）。
2. 對話視窗會在 VS Code 分頁中打開。

### 步驟 4：執行您的煙霧測試

使用 [模組 5](05-test-locally.md) 中的相同 3 項測試。於 Playground 輸入框鍵入每則訊息並按 **Send**（或 **Enter**）。

#### 測試 1 - 完整履歷與職缺描述（標準流程）

貼上模組 5 測試 1 中的完整履歷與職缺描述提示（Jane Doe + Contoso Ltd 高級雲端工程師）。

**預期結果：**
- 配合度分數與細項計算（100 分制）
- 匹配技能區塊
- 缺少技能區塊
- <strong>每個缺少技能一張差距卡</strong>，附帶 Microsoft Learn URL
- 學習路線圖與時間表

#### 測試 2 - 快速簡單測試（最小輸入）

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**預期結果：**
- 配合度較低（< 40）
- 誠實評估與分階段學習路線
- 多張差距卡（AWS、Kubernetes、Terraform、CI/CD、經驗差距）

#### 測試 3 - 高配合度候選人

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**預期結果：**
- 高配合度分數（≥ 80）
- 著重於面試準備與打磨
- 差距卡很少或沒有
- 短時間表，專注準備

### 步驟 5：與本地結果比較

打開您在模組 5 中保存的本地回應筆記或瀏覽器分頁。針對每個測試：

- 回應是否有<strong>相同結構</strong>（配合度分數、差距卡、路線圖）？
- 是否遵循<strong>相同的評分標準</strong>（100 分細項）？
- 差距卡中是否仍包含<strong>Microsoft Learn URL</strong>？
- 是否為<strong>每個缺少技能一張差距卡</strong>（無截斷）？

> <strong>輕微措詞差異屬正常</strong> — 模型本質是非確定性的。重點在結構、評分一致性及 MCP 工具使用。

---

## 選項 B：在 Foundry Portal 測試

[Foundry Portal](https://ai.azure.com) 提供網頁版 Playground，方便與團隊或利害關係人分享。

### 步驟 1：開啟 Foundry Portal

1. 開啟瀏覽器並前往 [https://ai.azure.com](https://ai.azure.com)。
2. 使用您在整個研討會中使用的相同 Azure 帳號登入。

### 步驟 2：導覽至您的專案

1. 在首頁，查看左側邊欄的 **Recent projects**。
2. 點擊您的專案名稱（例如 `workshop-agents`）。
3. 若未看到，點擊 **All projects** 並搜尋。

### 步驟 3：尋找您的已部署代理

1. 在專案左側導覽列，點擊 **Build** → **Agents**（或尋找 **Agents** 區段）。
2. 您應該會看到代理列表。找到您已部署的代理（例如 `resume-job-fit-evaluator`）。
3. 點擊代理名稱打開詳細頁。

### 步驟 4：打開 Playground

1. 在代理詳細頁，查看頂部工具列。
2. 點擊 **Open in playground**（或 **Try in playground**）。
3. 會打開聊天介面。

### 步驟 5：執行相同的煙霧測試

重複 VS Code Playground 部分中的 3 項測試。將每次回應與本地結果（模組 5）及 VS Code Playground 結果（上述選項 A）比較。

---

## 多代理特定驗證

除基本正確性外，驗證以下多代理特定行為：

### MCP 工具執行

| 檢查 | 如何驗證 | 通過條件 |
|-------|---------------|----------------|
| MCP 呼叫成功 | 差距卡包含 `learn.microsoft.com` URL | 真实 URL，而非備用訊息 |
| 多次 MCP 呼叫 | 每個高/中優先差距都有資源 | 不只第一張差距卡 |
| MCP 備用機制工作 | 缺少 URL 時檢查備用文字 | 代理仍生成差距卡（有無 URL 均可） |

### 代理協調

| 檢查 | 如何驗證 | 通過條件 |
|-------|---------------|----------------|
| 所有 4 個代理有執行 | 輸出包含配合度分數及差距卡 | 分數由 MatchingAgent 產生，差距卡由 GapAnalyzer 提供 |
| 順序執行 | 回應時間合理（< 2 分鐘） | 若超過 3 分鐘，檢查終端日誌是否有錯誤 |
| 資料流完整性 | 差距卡參照匹配報告的技能 | 無業務虛構技能（JD 中不存在的） |

---

## 驗證評分標準

使用此標準評估您的多代理工作流在主機環境中的行為：

| 編號 | 標準 | 通過條件 | 通過？ |
|---|----------|---------------|-------|
| 1 | <strong>功能正確性</strong> | 代理對履歷與職缺描述回應具配合度分數與差距分析 | |
| 2 | <strong>評分一致性</strong> | 配合度分數使用 100 分制及細項計算 | |
| 3 | <strong>差距卡完整性</strong> | 每個缺少技能都有一張卡（無截斷或合併） | |
| 4 | **MCP 工具整合** | 差距卡含真實 Microsoft Learn URL | |
| 5 | <strong>結構一致性</strong> | 本地與主機輸出結構匹配 | |
| 6 | <strong>回應時間</strong> | 主機代理於 2 分鐘內回應完整評估 | |
| 7 | <strong>無錯誤</strong> | 無 HTTP 500 錯誤、逾時或空回應 | |

> 「通過」意指所有 7 項標準於任一 Playground（VS Code 或 Portal）中對 3 項煙霧測試皆符合。

---

## 排除 Playground 問題

| 症狀 | 可能原因 | 解決方案 |
|---------|-------------|-----|
| Playground 無法加載 | 容器狀態非 `active` | 回到 [模組 6](06-deploy-to-foundry.md)，確認部署狀態。若為 `creating`，請等待 |
| 代理回應為空 | 模型部署名稱不符 | 檢查 `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` 是否與已部署模型匹配 |
| 代理回應錯誤訊息 | 缺少 [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 權限 | 在專案層級指派 **[Foundry User](https://aka.ms/foundry-ext-project-role)**（先前名稱為 Azure AI User） |
| 差距卡無 Microsoft Learn URL | MCP 出站被阻擋或 MCP 伺服器不可用 | 檢查容器是否可連 `learn.microsoft.com`。詳見 [模組 8](08-troubleshooting.md) |
| 只有 1 張差距卡（被截斷） | GapAnalyzer 指令缺少「CRITICAL」區塊 | 複習 [模組 3，步驟 2.4](03-configure-agents.md) |
| 配合度分數與本地差異大 | 部署了不同的模型或指令 | 比較 `agent.yaml` 環境變數與本地 `.env`。如有需要重新部署 |
| Portal 顯示「找不到代理」 | 部署仍在傳播或失敗 | 等待 2 分鐘後刷新。若仍然不存在，從 [模組 6](06-deploy-to-foundry.md) 重新部署 |

---

### 檢查點

- [ ] 在 VS Code Playground 測試代理 - 3 項煙霧測試皆通過
- [ ] 在 [Foundry Portal](https://ai.azure.com) Playground 測試代理 - 3 項煙霧測試皆通過
- [ ] 回應結構與本地測試一致（配合度分數、差距卡、路線圖）
- [ ] 差距卡含有 Microsoft Learn URL（MCP 工具在主機環境正常運作）
- [ ] 每個缺少技能一張差距卡（無截斷）
- [ ] 測試過程中無錯誤或逾時情況
- [ ] 完成驗證評分表（所有 7 項標準皆通過）

---

**上一章：** [06 - 部署至 Foundry](06-deploy-to-foundry.md) · **下一章：** [08 - 疑難排解 →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->