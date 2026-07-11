# 模組 5 - 部署至 Foundry 代理服務

⏱️ 約 10 分鐘

> ⚠️ **路徑 B 使用者：** 此模組需要 Foundry 訂閱。如果您使用 Foundry Local，請跳至 [模組 07 - 總結](07-summary.md)。您已成功完成本地開發工作流程！

在本模組中，您將本地測試完成的代理部署到 Microsoft Foundry 作為 <strong>託管代理</strong>。部署將構建容器映像，推送至 Azure 容器註冊表，並在 Foundry 的管理基礎架構中啟動代理。

### 部署流程

```mermaid
flowchart LR
    A["Dockerfile
    main.py"] -->|docker 構建| B["Container
    Image"]
    B -->|docker 推送| C["Azure Container
    Registry (ACR)"]
    C -->|註冊代理| D["Foundry Agent
    Service"]
    D -->|啟動容器| E["/responses
    endpoint ready"]

    style A fill:#9B59B6,color:#fff
    style B fill:#9B59B6,color:#fff
    style C fill:#E67E22,color:#fff
    style D fill:#3498DB,color:#fff
    style E fill:#27AE60,color:#fff
```

---

## 前置條件檢查

部署前請確認：

- [ ] 代理已通過 [模組 04](04-test-locally.md) 中的全部 3 項本地場景測試
- [ ] 您在專案層級擁有 **Azure AI User** 角色 ([模組 01，指定 RBAC](01-setup.md#deploy-a-model--assign-rbac))
- [ ] 您在 VS Code 已登入 Azure（帳戶圖示顯示您的名稱）

---

## 步驟 1：開始部署

### 選項 A：從 Agent Inspector 部署（建議）

若 Agent Inspector 已開啟（來自測試）：
1. 點擊右上角的 <strong>部署</strong> 按鈕（雲端圖示 ↑）。

### 選項 B：從命令面板部署

1. 按 `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent**。

---

## 步驟 2：設定部署

精靈將提示您：

![Project Config](../../../../../translated_images/zh-HK/05-foundry-project-setup.ca6ad16a6484e054.webp)

| 提示 | 選擇內容 |
|--------|-----------|
| <strong>訂閱</strong> | 您的 Azure 訂閱 |
| <strong>目標專案</strong> | 您的 Foundry 專案（例如 `workshop-agents`） |

點擊 <strong>下一步</strong> 以配置您的代理。

![Basics config](../../../../../translated_images/zh-HK/05-configure-basics.4d5f3d6b0d96f033.webp)

| 提示 | 選擇內容 |
|--------|-----------|
| <strong>部署方法</strong> | 容器 |
| <strong>容器註冊表</strong> | **預設 ACR**（Microsoft Foundry 為您建立並管理） |
| <strong>部署到</strong> | 新代理（名稱，`executive-summary-agent`） |

點擊 <strong>下一步</strong>，審查並部署您的代理。

![Review and deploy](../../../../../translated_images/zh-HK/05-review-deploy.12b449d426bff886.webp)

| 提示 | 選擇內容 |
|--------|-----------|
| **CPU 和記憶體** | **0.25 CPU 核心，0.5 Gi 記憶體**（足夠工作坊使用） |

---

## 步驟 3：部署和監控

1. 點擊 <strong>部署</strong>。
2. 監看 <strong>輸出</strong> 面板（從下拉選單選擇 **Microsoft Foundry**）。
3. 部署完成以下階段：
   - **Docker 建置** - 從您的 Dockerfile 建置容器
   - **Docker 推送** - 推送映像至 ACR（首次部署約 1–3 分鐘）
   - <strong>代理註冊</strong> - 在 Foundry 建立託管代理
   - <strong>容器啟動</strong> - 以系統管理的身分啟動

4. 完成後，會出現通知：
   > **my-agent 已成功部署。** `查看日誌` `執行代理`

5. 點擊 <strong>執行代理</strong> 打開代理遊樂場。

![Deployment success showing Agent Playground with Running status](../../../../../translated_images/zh-HK/05-deployed-asset.b59e6a5eef31c0b1.webp)

### 部署狀態說明

| 狀態 | 意義 |
|--------|---------|
| <strong>執行中</strong> | 容器已就緒，代理回應中 |
| <strong>待處理</strong> | 容器啟動中 - 請等待 30–60 秒 |
| <strong>失敗</strong> | 請檢查日誌（參見下方故障排除） |

---

## 常見部署錯誤

| 錯誤 | 根本原因 | 解決方案 |
|-------|-----------|-----|
| `agents/write` 權限被拒 | 專案層級缺少 **Azure AI User** 角色 | [模組 01，指定 RBAC](01-setup.md#deploy-a-model--assign-rbac) |
| Docker 未啟動 | Docker Desktop 未啟動 | 啟動 Docker Desktop → 確認 `docker info` |
| ACR 授權問題 | 管理身分無法拉取映像 | 參見 [模組 08 - 故障排除](08-troubleshooting.md) |

---

### ✅ 檢查點

- [ ] 部署完成且無錯誤
- [ ] 代理在 Foundry 側邊欄的 **託管代理 (預覽)** 下可見
- [ ] 容器狀態顯示為 <strong>執行中</strong>
- [ ] 已打開代理遊樂場標籤，顯示代理詳細資訊和端點 URL

---

**上一節：** [04 - 本地測試](04-test-locally.md) · **下一節：** [06 - 遊樂場驗證 →](06-verify-in-playground.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->