# 如何進行此會議

感謝您負責進行本會議！

在進行工作坊之前，請：

1. 完整閱讀本文件以及所有附加資源。
2. 觀看會議錄影及工作坊端到端示範影片。
3. 在自己的機器上<strong>至少完成一次</strong>兩個實作實驗的端到端演練。
4. 驗證您的 Microsoft Foundry 專案、模型部署與配額。
5. 如有不清楚之處，請聯絡維護者。

---

## 檔案摘要

| 資源                         | 連結                                                                              | 說明                                                                                    |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| 工作坊投影片                 | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                     | 講者使用講義，附帶講稿與內嵌示範影片                                                    |
| 會議錄影                   | _由維護者提供_                                                                     | 工作坊介紹與投影片導覽錄影                                                                |
| 工作坊端到端錄影            | _由維護者提供_                                                                     | 從學習者視角錄製兩個實作實驗的端到端過程                                                |
| 工作坊文件                  | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | 來源碼倉庫、實驗說明、逐步模組說明                                                      |
| 實驗 01 - 單一代理          | [Lab 01](../workshop/lab01-single-agent/README.md)                               | 實作實驗：構建、測試及部署 <em>解釋給行政人員聽</em> 的單一託管代理                            |
| 實驗 02 - 多代理工作流程    | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | 實作實驗：構建 4 代理 <em>履歷到職務匹配評估器</em> 工作流程                                  |
| 示範 1：行政代理             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                             | 實驗 01 示範：將技術術語翻譯成行政摘要                                                   |
| 示範 2：履歷到職務匹配評估器 | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)    | 實驗 02 示範：4 代理工作流程，評分履歷-職務匹配並生成建議                               |

> **講師備註：** 投影片與示範影片連結將於錄影完成後新增。完成前請聯絡維護者（請參閱 [聯絡資訊](#聯絡方式)）以取得最新資源。

---

## 開始使用

本工作坊教導開發者如何使用 **Microsoft Foundry Toolkit** 擴充套件，完全從 VS Code 建構、測試及部署 AI 代理至 **Microsoft Foundry Agent Service** 作為 <strong>託管代理</strong>。

工作坊分為多個部分，包括投影片、<strong>2 個即時示範</strong>與 **2 個實作實驗**。

### 時間安排

#### 全程授課（約 2 小時）

| 時間            | 說明                                                                 |
|-----------------|-----------------------------------------------------------------------|
| 0:00 - 10:00    | 介紹：託管代理、Foundry Agent Service 及工具套件                    |
| 10:00 - 20:00   | 示範：行政代理端到端                                                 |
| 20:00 - 60:00   | 實驗 01 - 單一代理（建構、在地測試、部署、練習場）                  |
| 60:00 - 110:00  | 實驗 02 - 多代理工作流程（履歷到職務匹配評估器）                     |
| 110:00 - 120:00 | 總結、問答與後續學習資源                                            |

#### 簡短授課（約 75 分鐘）

| 時間          | 說明                                                      |
|---------------|------------------------------------------------------------|
| 0:00 - 10:00  | 介紹與概覽                                               |
| 10:00 - 20:00 | 示範：行政代理                                           |
| 20:00 - 70:00 | 僅做實驗 01（引導學員自行完成實驗 02）                   |
| 70:00 - 75:00 | 總結與問答                                              |

### 準備工作

| 資源                           | 連結                                                                                          | 說明                                             |
|--------------------------------|------------------------------------------------------------------------------------------------|---------------------------------------------------|
| 工作坊文件                     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | 工作坊文件與來源                                  |
| 實驗 01 指示                  | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | 實作實驗：單一託管代理                            |
| 實驗 02 指示                  | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | 實作實驗：多代理工作流程                          |
| 先決條件檢查清單              | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | 工具、帳戶與 Azure 存取要求                        |
| 託管代理快速上手（azd）         | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | 官方使用 `azd` 部署託管代理快速教學              |
| 託管代理區域可用性              | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | 託管代理支援的區域（預覽）                        |

### 講師先決條件

在開始授課前，請確保您擁有：

- 具有建立資源權限的 **Azure 訂閱**（資源群組擁有者或貢獻者權限）。
- 可存取含[支援託管代理區域](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) 的 **Microsoft Foundry 專案**。
- Foundry 專案中有 **gpt-4.1**（或 **gpt-4.1-mini**）配額。
- 安裝以下工具：
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit 擴充套件](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/)（可選）
  - Python 3.10 或更高版本

在授課前至少執行一次[使用 `azd` 部署託管代理快速教學](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)，以便您擁有一個功能正常的 Foundry 專案、模型部署和 Azure Container Registry，進而在學員遇到問題時提供協助。

---

## 投影片導覽

投影片流程與實驗一致。每章節建議講解重點：

| 章節                        | 重要訊息                                                                                         |
|-----------------------------|------------------------------------------------------------------------------------------------|
| 標題與議程                  | 將工作坊定位為「從 VS Code 到 Foundry」，無需切換入口網站。                                   |
| 為何選擇託管代理？          | 管理式執行環境、基於 ACR 的部署、兼容 OpenAI 的 `/responses` API、針對 Foundry 專案範圍設定。  |
| 架構圖                      | 演示[README 架構說明](../README.md#architecture)：骨架、檢查器、ACR、代理服務。                 |
| 託管代理的結構              | `agent.yaml`、`Dockerfile`、`main.py`、`requirements.txt` - 每個檔案的角色說明。                 |
| 即時示範：行政代理          | 切換至 VS Code 運行 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) 示範（詳見[示範 1](#示範-1：行政代理)）。 |
| 即時示範：履歷到職務匹配評估器 | 切換至 VS Code 運行 [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4 代理示範（詳見[示範 2](#示範-2：履歷到職務匹配評估器)）。 |
| 實驗 01 簡介               | 交棒給學員。指向 [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md)。 |
| 多代理模式                 | 串行、並行與交接模式 - 在實驗 02 開始前預覽說明。                                              |
| 實驗 02 簡介               | 交棒給學員。指向 [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md)。 |
| 總結與資源                 | 從[附加資源](#額外資源)章節分享更多持續學習連結。                                  |

---

## 示範

配授課包含兩個即時示範，各分配約 10 分鐘。

| 示範             | 實驗  | 檔案                                                                    | 示範內容                                                   |
|-----------------|-------|-------------------------------------------------------------------------|------------------------------------------------------------|
| 行政代理         | 實驗 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | 單一託管代理；將技術術語翻譯成行政摘要                       |
| 履歷到職務匹配評估器 | 實驗 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4 代理協調工作流程；評分履歷與職務匹配並生成推薦            |

### 示範 1：行政代理

在 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) 中的獨立代理。作為實驗 01 前的 10 分鐘示範。

1. 開啟 [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py)，逐步說明代理定義（系統提示、模型、框架）。
2. 按下 `F5` 本機啟動 **Agent Inspector**。
3. 貼上 [README](../README.md#see-it-in-action) 中的範例提示，展示行政摘要回應。
4. 顯示 [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) 與 [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile)，說明部署資料。
5. 示範部署流程（Docker 建置、ACR 推送、建立託管代理），無需等待完成。

### 示範 2：履歷到職務匹配評估器

在 [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 的 4 代理工作流程。作為實驗 02 前的 10 分鐘示範。

1. 開啟 [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)，展示四個代理如何串接成串行協調工作流程。
2. 按下 `F5` 啟動多代理工作流程的 **Agent Inspector**。
3. 在 Inspector 聊天視窗貼上簡短的職務描述與範例履歷。
4. 說明四代理流程：履歷解析器、職務需求擷取器、匹配分數評估器與推薦撰寫器。
5. 指出每個子代理的輸出成為下一代理的上下文，強調交接模式。
6. 顯示 [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml)，與示範 1 的單一代理作比較。

---

## 授課小技巧

- **提前設定預期。** 託管代理目前處於預覽階段—請事先說明區域限制與配額，避免學員在實驗期間遭遇意外。
- **先執行先決條件任務。** 兩個實驗皆提供「驗證先決條件」VS Code 任務，請學員先完成此任務再開始編寫程式碼。
- **保持 Agent Inspector 可見。** 多數『恍然大悟』的時刻發生在學員看到本機的 `/responses` 反覆照亮。
- **準備備用專案。** 若學員的 Foundry 專案配額不足，提供預先佈建好的專案以供部署，避免全場停擺。
- **學員配對。** 實驗 02（多代理）在學員可彼此討論協調流程時，會輕鬆不少。
- **使用文件模組作為檢查點。** 每個實驗資料夾中的 `docs/` 細分為 8 個編號模組，推薦作為自然停頓點使用。
- **事先拉取基底 Docker 映像** 到共用實驗機器，避免註冊表速率限制。

---

## 授課期間常見問題排解

| 徵狀                                     | 首要嘗試動作                                                                             |
|----------------------------------------|-----------------------------------------------------------------------------------------|
| Agent Inspector 無法連線               | 確認埠號 `8088` 可用，且 `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` 任務正在執行。 |
| 偵錯器無法附加                        | 確認埠號 `5679` 可用；若 `debugpy` 已被綁定，請重啟 VS Code。                           |
| `azd up` 認證錯誤                     | 執行 `az login` 與 `azd auth login`，確定已選擇正確的租戶。                             |
| 部署在 ACR 推送時掛起                | 確認 Docker Desktop 正在執行且使用者擁有註冊表的 `AcrPush` 權限。                      |
| 模型回應 404 / 找不到部署             | `agent.yaml` 中的模型部署名稱必須與 Foundry 專案中的部署名稱一致。                      |

| 託管代理卡在 `Provisioning`                     | 驗證專案區域是否[支援託管代理](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)且配額可用。         |
| Playground 返回 401                             | 從 VS Code 活動列重新驗證 Foundry 擴充功能。                                     |

若需更深入指引，每個實驗室都有自己的 `08-troubleshooting.md` 文件 - 導向學員參考：

- 實驗室 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- 實驗室 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## 自訂本次課程

歡迎根據您的受眾調整工作坊。常見變體包括：

- **後端受眾：** 花更多時間在 `agent.yaml`、Docker 和 ACR；縮減 playground 示範。
- **市民開發者受眾：** 停留在 Foundry 擴充功能 UI 進行搭建；減少 CLI 步驟。
- **單軌 60 分鐘時段：** 僅交付簡介、示範及實驗室 01。
- **僅工作坊（無簡報）格式：** 同時開啟兩個實驗室說明檔，並用作主要講稿。

如果您擴展了實驗室內容，請透過 PR 回饋更改，以便其他講師受益。

---

## 額外資源

- [Microsoft Foundry 文件](https://learn.microsoft.com/azure/ai-foundry/)
- [託管代理概述](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [快速入門：部署您的第一個託管代理 (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [部署託管代理（操作指南）](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft 代理架構](https://github.com/microsoft/agents)
- [Microsoft Foundry VS Code 工具組](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## 聯絡方式

若您對交付本次課程有疑問，請在[工作坊存放庫](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues)開啟 issue 並標記維護者。

| 角色                | 姓名           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| 維護者 / 聯絡人      | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->