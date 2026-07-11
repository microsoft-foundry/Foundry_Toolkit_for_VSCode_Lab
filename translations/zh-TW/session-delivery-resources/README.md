# 如何進行本次課程

感謝您主講本次課程！

在進行工作坊之前，請先：

1. 完整閱讀本文件及所有包含的資源。
2. 觀看課程演示錄影及工作坊端到端示範影片。
3. 在您的電腦上<strong>至少完整進行一次</strong>兩個動手實作實驗。
4. 驗證您的 Microsoft Foundry 專案、模型部署及配額。
5. 若有任何不清楚之處，請聯繫維護者。

---

## 文件總結

| 資源                          | 連結                                                                             | 說明                                                                                     |
|-------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| 工作坊簡報                   | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | 本工作坊簡報含講者備註及內嵌示範影片                                                  |
| 課程演示錄影                | _由維護者提供_                                                                    | 工作坊簡介與簡報導覽的錄影                                                              |
| 工作坊端到端錄影            | _由維護者提供_                                                                    | 從學員視角端到端錄製兩個實驗的過程                                                   |
| 工作坊文件                  | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | 原始碼倉庫、實驗 README、逐步模組                                                        |
| 實驗 01 - 單一 Agent        | [Lab 01](../workshop/lab01-single-agent/README.md)                               | 動手實作：建立、測試並部署 *Explain Like I'm an Executive* 託管代理                    |
| 實驗 02 - 多代理工作流程    | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | 動手實作：建立 4 代理 *Resume to Job Fit Evaluator* 工作流程                           |
| 示範 1: Executive Agent        | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                              | 實驗 01 示範：將技術術語翻譯成執行長摘要                                              |
| 示範 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)     | 實驗 02 示範：4 代理工作流程，評分履歷與職務匹配度並生成建議                           |

> **講師備註：** 簡報及影片連結會在錄製完成後新增。期間請聯繫維護者（參見[聯絡資訊](#聯絡方式)）索取最新資源。

---

## 開始使用

本工作坊教導開發者如何使用 **Microsoft Foundry Toolkit** 擴充功能，從 VS Code 完全建立、測試並部署 AI 代理到 **Microsoft Foundry Agent Service** 作為 <strong>託管代理</strong>。

工作坊分成多個部分，包括簡報、<strong>2 個即時示範</strong>以及<strong>2 個動手實作實驗</strong>。

### 時間安排

#### 全程授課（約 2 小時）

| 時間            | 說明                                                               |
|-----------------|--------------------------------------------------------------------|
| 0:00 - 10:00    | 介紹：託管代理、Foundry Agent Service 與工具組                    |
| 10:00 - 20:00   | 示範：Executive Agent 端到端流程                                  |
| 20:00 - 60:00   | 實驗 01 - 單一代理（建立、在地測試、部署、遊戲場）                |
| 60:00 - 110:00  | 實驗 02 - 多代理工作流程（Resume to Job Fit Evaluator）           |
| 110:00 - 120:00 | 結語、問答與持續學習資源                                          |

#### 簡短授課（約 75 分鐘）

| 時間          | 說明                                                               |
|---------------|--------------------------------------------------------------------|
| 0:00 - 10:00  | 介紹與概覽                                                        |
| 10:00 - 20:00 | 示範：Executive Agent                                            |
| 20:00 - 70:00 | 僅實驗 01（指導學員自學實驗 02）                                 |
| 70:00 - 75:00 | 結語與問答                                                      |

### 準備工作

| 資源                           | 連結                                                                                        | 說明                                                |
|--------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------|
| 工作坊文件                     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)           | 工作坊文件與原始碼                                    |
| 實驗 01 指南                  | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                              | 動手實作：單一託管代理                                |
| 實驗 02 指南                  | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                | 動手實作：多代理工作流程                              |
| 先決條件清單                  | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)              | 所需工具、帳戶與 Azure 訪問權限                        |
| 託管代理快速開始 (azd)        | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | 使用 `azd` 部署託管代理的官方快速開始                  |
| 託管代理區域可用性            | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | 託管代理支援的區域（預覽）                             |

### 講師先決條件

進行授課前，請確保您具備：

- **Azure 訂閱**，且有建立資源權限（資源群組的擁有者或貢獻者角色）。
- 可使用支援託管代理的 [Microsoft Foundry 專案區域](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)。
- 在 Foundry 專案中有 **gpt-4.1**（或 **gpt-4.1-mini**）配額。
- 以下工具已安裝：
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit 擴充功能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/)（可選）
  - Python 3.10 或更高版本

授課前至少執行一次 [使用 `azd` 的託管代理快速開始](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)，以擁有良好狀態的 Foundry 專案、模型部署及 Azure Container Registry，方便當學員遇到問題時參考。

---

## 簡報導讀

簡報與實驗流程一致。每個部分建議的講解要點：

| 部分                      | 主要訊息                                                                                             |
|---------------------------|----------------------------------------------------------------------------------------------------|
| 標題與議程               | 將工作坊定位為「從 VS Code 到 Foundry」，無需切換入口網站。                                      |
| 為何選擇託管代理？        | 管理式執行環境、基於 ACR 的部署、相容 OpenAI 的 `/responses` API，限於 Foundry 專案。           |
| 架構圖                   | 解說 [README 架構](../README.md#architecture)：腳手架、Inspecter、ACR、Agent 服務。            |
| 託管代理結構              | `agent.yaml`、`Dockerfile`、`main.py`、`requirements.txt` - 各檔案功用介紹。                       |
| 即時示範：Executive Agent  | 切換至 VS Code，端到端執行 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) 示範（參見[示範 1](#示範-1：executive-agent)）。 |
| 即時示範：Resume to Job Fit Evaluator | 切換至 VS Code，執行 [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4 代理示範（參見[示範 2](#示範-2：resume-to-job-fit-evaluator)）。 |
| 實驗 01 簡介              | 交由學員操作，指向 [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md)。 |
| 多代理模式                | 介紹序列式、併發式與交接式，作為實驗 02 的預覽。                                               |
| 實驗 02 簡介              | 交由學員操作，指向 [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md)。 |
| 結語與資源                | 從[附加資源](#附加資源)章節提供持續學習連結。                                       |

---

## 示範

本課程包含兩個即時示範，每個示範擬分配 10 分鐘。

| 示範   | 實驗  | 檔案路徑                                                            | 示範內容                                                      |
|--------|-------|-------------------------------------------------------------------|--------------------------------------------------------------|
| Executive Agent             | 實驗 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)      | 單一託管代理；將技術術語翻譯為執行摘要                      |
| Resume to Job Fit Evaluator | 實驗 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4 代理協調流程；評分履歷與職務匹配並生成建議方案            |

### 示範 1：Executive Agent

單一代理位於 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)。作為實驗 01 前的 10 分鐘示範使用。

1. 開啟 [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py)，講解代理定義（系統指令、模型、框架）。
2. 按 `F5` 在本地啟動 **Agent Inspector**。
3. 貼上 README 中的範例提示（[README](../README.md#see-it-in-action)），示範執行摘要的回應。
4. 展示 [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) 與 [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile)，說明部署產物。
5. 示範部署流程（Docker 建置、ACR 推送、託管代理建立），不必等待完成。

### 示範 2：Resume to Job Fit Evaluator

4 代理工作流程位於 [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)。作為實驗 02 前的 10 分鐘示範使用。

1. 開啟 [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)，展示四個代理如何串接成序列化協調。
2. 按 `F5` 啟動多代理工作流程的 **Agent Inspector**。
3. 在 Inspector 聊天視窗中貼上一段簡短的職務描述與範例履歷。
4. 講解四代理管道：履歷解析器、職務需求擷取器、匹配評分器及建議撰寫器。
5. 指出每個子代理的輸出如何成為下一代理的上下文，強調交接模式。
6. 展示 [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml)，與示範 1 的單一代理檔案做比較。

---

## 演講技巧

- **提前設定預期。** 託管代理仍在預覽階段，預先提醒區域限制和配額，避免學員中途驚訝。
- **先執行先決條件任務。** 兩個實驗均內建「驗證先決條件」的 VS Code 任務，請讓學員於寫程式前先執行。
- **保持 Agent Inspector 視窗開啟。** 大多數學習「啊哈」時刻發生在學員看到本地 `/responses` 回傳時。
- **備有備用專案。** 若學員的 Foundry 專案碰到配額阻礙，提供一個預先建立好的專案，避免全班停擺。
- **搭配雙人組。** 實驗 02（多代理）學習時與同伴討論協調流程，能大幅降低難度。
- **利用文件模組作為檢查點。** 每個實驗的 `docs/` 資料夾均切分為 8 個編號模組，適合用作自然中場休息點。
- **事先拉取基礎 Docker 映像檔**，於共用實驗機器上避免註冊表的頻率限制。

---

## 授課時故障排除

| 症狀                                   | 初步嘗試辦法                                                     |
|----------------------------------------|-----------------------------------------------------------------|
| Agent Inspector 無法連線               | 確認 8088 通訊埠未被佔用，且「執行 Lab01 HTTP Server」/「執行 Lab02 HTTP Server」任務正在執行。 |
| 除錯程式無法附加                     | 確認 5679 通訊埠未被佔用；若 `debugpy` 已被綁定，重新啟動 VS Code。           |
| `azd up` 發生驗證錯誤                 | 執行 `az login` 與 `azd auth login`，確保選擇正確租戶。                             |
| 部署卡在 ACR 推送                    | 確認 Docker Desktop 正常運行且使用者對註冊表擁有 `AcrPush` 權限。               |
| 模型返回 404 / 找不到部署             | `agent.yaml` 的模型部署名稱必須與 Foundry 專案中的部署名稱一致。                       |

| 託管代理卡在 `Provisioning`          | 驗證專案區域[是否支持託管代理](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)且配額是否可用。 |
| Playground 返回 401                   | 從 VS Code 活動列重新認證 Foundry 擴充功能。                                   |

更深入的指引，每個實驗室都附有自己的 `08-troubleshooting.md` 文件 — 請引導學員查看： 

- 實驗室 01：[`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- 實驗室 02：[`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## 自訂此課程

歡迎根據您的聽眾調整工作坊。常見變化包括：

- <strong>後端受眾：</strong>花更多時間講解 `agent.yaml`、Docker 和 ACR；減少 playground 示範時間。
- <strong>市民開發者受眾：</strong>停留在 Foundry 擴充功能 UI 進行骨架搭建；減少 CLI 步驟。
- <strong>單軌 60 分鐘時段：</strong>僅完成介紹、示範和實驗室 01。
- <strong>僅工作坊（無投影片）格式：</strong>同時打開兩個實驗室的 README，並用其作為主要講稿。

如果您擴展實驗室，請通過 PR 回饋更改，讓其他講師受益。

---

## 附加資源

- [Microsoft Foundry 文件](https://learn.microsoft.com/azure/ai-foundry/)
- [託管代理概述](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [快速入門：部署您的第一個託管代理 (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [部署託管代理（操作指南）](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## 聯絡方式

若您對講授此課程有疑問，請在 [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) 開啟議題並標記維護者。

| 角色            | 姓名           | GitHub                                                 |
|-----------------|----------------|---------------------------------------------------------|
| 維護者 / 聯絡人 | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->