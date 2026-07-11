# 模組 7 - 在 Playground 驗證

⏱️ 約 10 分鐘

在本模組中，您將在 VS Code 和 Foundry 入口網站中測試您所部署的多代理工作流程，確認代理的行為與本機測試相同。

---

## 為什麼部署後還要測試？

托管環境與本地在幾個重要方面有所不同：

| | 本地 | 托管 |
|--|-------|--------|
| <strong>身分識別</strong> | 您個人的登入 (`DefaultAzureCredential`) | 每個代理專用的 Entra 身分 (在部署時自動配置) |
| <strong>端點</strong> | `http://localhost:8088/responses` | Foundry 代理服務管理的 URL |
| <strong>網路</strong> | 您的機器 → Azure OpenAI + MCP | Azure 主幹網路（較低延遲） |

一個錯誤配置的環境變數、RBAC 問題或被阻擋的 MCP 出站呼叫會先在這裡顯現。

---

## 選項 A：在 VS Code Playground 測試（推薦優先）

### 步驟 1：前往您的托管代理

1. 點擊活動列上的 **Foundry Toolkit** 圖示。
2. 展開您的專案 → **Hosted Agents (Preview)** → 找到您的代理。

![Foundry Toolkit 側邊欄顯示 Hosted Agents (Preview) 與 resume-job-fit-evaluator 及其部署版本](../../../../../translated_images/zh-TW/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### 步驟 2：選擇版本

1. 點擊代理以展開其版本列表。
2. 點擊 `v1` → 確認狀態為 **active**（側邊欄可能顯示「Running」或「Started」—兩者都代表已準備就緒）。

### 步驟 3：開啟 Playground

1. 點擊 **Playground**（或右鍵點擊版本 → **Open in Playground**）。
2. 會在 VS Code 分頁中開啟聊天視窗。

### 步驟 4：執行您的煙霧測試

使用 [模組 5](05-test-locally.md) 中相同的 3 個測試。在 Playground 輸入框輸入每條訊息並按 <strong>傳送</strong>（或 **Enter**）。

#### 測試 1 - 完整履歷 + 職務描述（標準流程）

貼上模組 5 測試 1 中的完整履歷 + 職務描述提示（Jane Doe + Contoso Ltd 高級雲端工程師）。

**預期結果：**
- 合適度分數及細分計算（100分制）
- 匹配技能章節
- 缺少技能章節
- **每個缺失技能一張 gap 卡**，附帶 Microsoft Learn 連結
- 含有時間軸的學習路線圖

#### 測試 2 - 快速簡短測試（最小輸入）

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**預期結果：**
- 合適度分數較低（< 40）
- 誠實評估且附分階段學習路徑
- 多張 gap 卡（AWS、Kubernetes、Terraform、CI/CD、經驗缺口）

#### 測試 3 - 高合適度候選人

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**預期結果：**
- 高合適度分數（≥ 80）
- 著重面試準備與精煉
- 少量或沒有 gap 卡
- 以準備為重點的短期時間軸

### 步驟 5：與本機結果比較

打開您在模組 5 中保存本機回應的筆記或瀏覽器分頁，針對每個測試：

- 回應是否有<strong>相同結構</strong>（合適度分數、gap 卡、路線圖）？
- 是否遵循<strong>相同的評分標準</strong>（100分細分）？
- gap 卡中是否仍有<strong>Microsoft Learn 連結</strong>？
- 是否為<strong>每個缺失技能一張 gap 卡</strong>（未被截斷）？

> <strong>文字細節差異屬正常現象</strong> — 模型非決定性。重點放在結構、評分一致性和 MCP 工具的使用。

---

## 選項 B：在 Foundry 入口網站測試

[Foundry Portal](https://ai.azure.com) 提供基於網頁的 playground，方便與團隊成員或利害關係人分享。

### 步驟 1：開啟 Foundry 入口網站

1. 打開瀏覽器並前往 [https://ai.azure.com](https://ai.azure.com)。
2. 使用您在研討會中一直使用的相同 Azure 帳戶登入。

### 步驟 2：前往您的專案

1. 在首頁左側邊欄尋找 **Recent projects**。
2. 點擊您的專案名稱（例如 `workshop-agents`）。
3. 若看不到，點選 **All projects** 並搜尋您的專案。

### 步驟 3：找到您部署的代理

1. 在專案左側導覽列點選 **Build** → **Agents**（或尋找 **Agents** 區段）。
2. 您應該會看到代理清單。找到您已部署的代理（例如 `resume-job-fit-evaluator`）。
3. 點擊代理名稱以開啟詳細頁面。

### 步驟 4：開啟 Playground

1. 在代理詳細頁面頂部工具列查看。
2. 點擊 **Open in playground**（或 **Try in playground**）。
3. 會開啟聊天介面。

### 步驟 5：執行相同煙霧測試

重複上述 VS Code Playground 區段的所有 3 項測試。將每項回應與本機結果（模組 5）及 VS Code Playground 結果（選項 A）比較。

---

## 多代理特定驗證

除了基本正確性外，還需驗證以下多代理特定行為：

### MCP 工具執行

| 檢查項目 | 如何驗證 | 通過條件 |
|-------|---------------|----------------|
| MCP 呼叫成功 | gap 卡包含 `learn.microsoft.com` 連結 | 真實 URL，而非替代訊息 |
| 多次 MCP 呼叫 | 每個高/中優先缺口都有資源 | 不只是第一張 gap 卡 |
| MCP 備用機制有效 | 若 URL 遺失，檢查是否有替代文字 | 代理仍能產生 gap 卡（有或無 URL） |

### 代理協調

| 檢查項目 | 如何驗證 | 通過條件 |
|-------|---------------|----------------|
| 四個代理皆執行 | 輸出含合適度分數及 gap 卡 | 分數由 MatchingAgent 提供，卡由 GapAnalyzer 產生 |
| 順序執行 | 回應時間合理（< 2 分鐘） | 超過 3 分鐘，查看終端機日誌是否有錯誤 |
| 資料流完整性 | gap 卡所指技能與匹配報告相符 | 無在職務描述中未出現的幻覺技能 |

---

## 驗證標準

使用此標準評估您多代理工作流程的托管行為：

| 編號 | 標準 | 通過條件 | 是否通過？ |
|---|----------|---------------|-------|
| 1 | <strong>功能正確性</strong> | 代理對履歷 + 職務描述回應合適度分數與缺口分析 | |
| 2 | <strong>評分一致性</strong> | 合適度分數採用 100 分制且計算明確 | |
| 3 | **gap 卡完整性** | 每個缺失技能一張卡（未截斷或合併） | |
| 4 | **MCP 工具整合** | gap 卡包含真實 Microsoft Learn 連結 | |
| 5 | <strong>結構一致性</strong> | 托管與本地輸出結構一致 | |
| 6 | <strong>回應時間</strong> | 托管代理對完整評估回應時間在 2 分鐘內 | |
| 7 | <strong>無錯誤</strong> | 無 HTTP 500 錯誤、逾時或空回應 | |

> 「通過」代表所有 7 項標準於至少一個 playground（VS Code 或入口網站）中的 3 項煙霧測試均達成。

---

## playground 問題排解

| 症狀 | 可能原因 | 解決方法 |
|---------|-------------|-----|
| playground 無法載入 | 容器非 `active` 狀態 | 返回 [模組 6](06-deploy-to-foundry.md)，確認部署狀態。若為 `creating`，請稍候 |
| 代理回應為空 | 模型部署名稱不匹配 | 檢查 `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` 是否與部署模型相符 |
| 代理回應錯誤訊息 | [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 權限缺失 | 在專案範圍內指定 **[Foundry User](https://aka.ms/foundry-ext-project-role)**（前稱 Azure AI User）角色 |
| gap 卡中無 Microsoft Learn 連結 | MCP 出站被阻擋或 MCP 伺服器不可用 | 檢查容器是否能連線至 `learn.microsoft.com`。詳見 [模組 8](08-troubleshooting.md) |
| 只有 1 張 gap 卡（被截斷） | GapAnalyzer 指令缺少「CRITICAL」區塊 | 複習 [模組 3，第 2.4 步](03-configure-agents.md) |
| 合適度分數與本地差異大 | 部署模型或指令不同 | 比對 `agent.yaml` 環境變數與本地 `.env`。必要時重新部署 |
| 入口網站顯示「找不到代理」 | 部署仍在傳播或失敗 | 等待 2 分鐘並刷新。如仍缺少，從 [模組 6](06-deploy-to-foundry.md) 重新部署 |

---

### 檢查點

- [ ] 在 VS Code Playground 測試代理 - 所有 3 項煙霧測試通過
- [ ] 在 [Foundry Portal](https://ai.azure.com) Playground 測試代理 - 所有 3 項煙霧測試通過
- [ ] 回應在結構上與本地測試一致（合適度分數、gap 卡、路線圖）
- [ ] gap 卡中含有 Microsoft Learn 連結（MCP 工具在托管環境中運作正常）
- [ ] 每個缺失技能僅有一張 gap 卡（無截斷）
- [ ] 測試過程無錯誤或逾時
- [ ] 完成驗證標準（全部 7 項標準通過）

---

**前一章：** [06 - 部署到 Foundry](06-deploy-to-foundry.md) · **下一章：** [08 - 故障排除 →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->