# 如何主持此課程

感謝您主持此課程！

在主持工作坊之前，請：

1. 完整閱讀此文件與所有附帶資源。
2. 觀看課程主持錄影與工作坊全流程示範。
3. 至少於活動前在您自己的機器上完整操作兩個實作課程一次。
4. 驗證您的 Microsoft Foundry 專案、模型部署與額度。
5. 若有不明之處，請聯絡維護者。

---

## 檔案摘要

| 資源                      | 連結                                                                             | 說明                                                                                      |
|-------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| 工作坊簡報                  | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | 此工作坊簡報含講者備註與嵌入示範影片                                                     |
| 課程主持錄影               | _維護者後續提供_                                                                  | 工作坊介紹與簡報講解錄影                                                                  |
| 工作坊全流程示範錄影       | _維護者後續提供_                                                                  | 兩個實作課程從學習者視角的端到端錄影                                                     |
| 工作坊文件                 | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | 程式原始碼庫、實驗手冊與逐步模組                                                           |
| 實作課程 01 - 單代理       | [Lab 01](../workshop/lab01-single-agent/README.md)                               | 實作課程：構建、測試與部署 *Explain Like I'm an Executive* 主機代理                         |
| 實作課程 02 - 多代理流程   | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | 實作課程：構建 4 代理 *Resume to Job Fit Evaluator* 工作流程                               |
| 示範 1: Executive Agent              | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | 實作課程 01 示範：將專業術語翻譯成高階摘要                                                |
| 示範 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | 實作課程 02 示範：4 代理工作流程，評分履歷與職務匹配並產生建議                            |

> **訓練師注意：** 簡報及影片連結將於錄影發布後加入，在此之前請聯絡維護者（參見 [聯絡方式](#聯絡資料)）索取最新資料。

---

## 開始

本工作坊教導開發者如何完全從 VS Code 使用 **Microsoft Foundry Toolkit** 延伸模組，構建、測試及部署 AI 代理至 **Microsoft Foundry Agent Service** 作為 **Hosted Agents**。

工作坊分為多個章節，包含簡報、<strong>2 個即時示範</strong>與<strong>2 個實作課程</strong>。

### 時間安排

#### 完整課程（約 2 小時）

| 時間            | 說明                                                             |
|-----------------|------------------------------------------------------------------|
| 0:00 - 10:00    | 介紹：Hosted Agents、Foundry Agent Service 及工具組              |
| 10:00 - 20:00   | 示範：Executive Agent 端到端運作                                 |
| 20:00 - 60:00   | 實作課程 01 - 單代理（建置、在地測試、部署、遊戲場）              |
| 60:00 - 110:00  | 實作課程 02 - 多代理工作流程（Resume to Job Fit Evaluator）      |
| 110:00 - 120:00 | 總結、問答與持續學習資源                                         |

#### 簡短課程（約 75 分鐘）

| 時間          | 說明                                                      |
|---------------|----------------------------------------------------------|
| 0:00 - 10:00  | 介紹與概覽                                              |
| 10:00 - 20:00 | 示範：Executive Agent                                   |
| 20:00 - 70:00 | 只做實作課程 01（引導學員自學課程 02）                 |
| 70:00 - 75:00 | 總結與問答                                            |

### 準備

| 資源                       | 連結                                                                                           | 說明                                                  |
|-----------------------------|----------------------------------------------------------------------------------------------|-------------------------------------------------------|
| 工作坊文件                 | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)            | 工作坊文件與原始碼                                     |
| 實作課程 01 指導           | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                               | 實作課程：單一 Hosted Agent                            |
| 實作課程 02 指導           | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                 | 實作課程：多代理工作流程                               |
| 前置條件清單               | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)               | 需要安裝的工具、帳戶與 Azure 存取                       |
| Hosted Agents 快速開始 (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | 使用 `azd` 部署 Hosted Agent 的官方快速開始教學   |
| Hosted Agents 地區可用性     | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Hosted Agents 支援地區（預覽）                         |

### 講師必備條件

在主持之前，請確保您已經：

- 具有能建立資源的 **Azure 訂閱**（在資源群組有擁有者或參與者權限）。
- 可使用在支持 Hosted Agents 的[地區](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)的 **Microsoft Foundry 專案**。
- 於 Foundry 專案中擁有 **gpt-4.1**（或 **gpt-4.1-mini**）的配額。
- 已安裝以下工具：
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit 延伸模組](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/)（選用）
  - Python 3.10 或以上版本

請在授課前至少執行一次 [Hosted Agents 快速開始（azd）](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)，以確保您擁有一個已確認正常的 Foundry 專案、模型部署及 Azure Container Registry，當學員遇到問題可作為參考。

---

## 簡報講解

簡報與實作課程流程相同。每個章節建議講解重點：

| 章節                       | 重點訊息                                                                                       |
|----------------------------|----------------------------------------------------------------------------------------------|
| 標題與議程                 | 將工作坊定位為 *VS Code 到 Foundry*，無需切換門戶網站。                                   |
| 為何使用 Hosted Agents？     | 託管執行環境、基於 ACR 的部署、相容 OpenAI 的 `/responses` API，範圍限定於 Foundry 專案。  |
| 架構圖                     | 講解 [README 架構](../README.md#architecture)：腳手架、Inspector、ACR、Agent Service。     |
| Hosted Agent 結構          | `agent.yaml`、`Dockerfile`、`main.py`、`requirements.txt` - 各檔案作用。                      |
| 即時示範：Executive Agent  | 切換至 VS Code 並執行 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) 端到端示範（詳見 [示範 1](#示範-1：executive-agent)）。 |
| 即時示範：Resume to Job Fit Evaluator | 切換至 VS Code 並執行 [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 四代理示範（詳見 [示範 2](#示範-2：resume-to-job-fit-evaluator)）。 |
| 實作課程 01 簡介           | 交給學員。指向 [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md)。 |
| 多代理模式                 | 順序執行 vs 並行 vs 交接—於實作課程 02 開始前預覽。                                          |
| 實作課程 02 簡介           | 交給學員。指向 [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md)。 |
| 總結與資源                 | 從 [其他資源](#額外資源) 章節提供持續學習連結。                                   |

---

## 示範

課程中包含兩個即時示範，各分配 10 分鐘。

| 示範 | 實作課程 | 檔案                                                    | 展示內容                                           |
|------|---------|---------------------------------------------------------|---------------------------------------------------|
| Executive Agent           | 實作 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)      | 單一 Hosted Agent；將專業術語翻譯成高層摘要         |
| Resume to Job Fit Evaluator | 實作 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4 代理編排；履歷與職務匹配評分並生成建議             |

### 示範 1：Executive Agent

在 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) 中的獨立代理。作為實作課程 01 前的 10 分鐘示範使用。

1. 開啟 [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py)，說明代理定義（系統提示、模型、框架）。
2. 按 `F5` 以本機啟動 **Agent Inspector**。
3. 貼上 [README](../README.md#see-it-in-action) 中的範例提示，展示執行摘要回應。
4. 展示 [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) 與 [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile)，說明部署檔案。
5. 示範部署流程（Docker build、ACR push、建立 Hosted Agent），無需等待完成。

### 示範 2：Resume to Job Fit Evaluator

在 [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 中的 4 代理工作流程。作為實作課程 02 前的 10 分鐘示範使用。

1. 開啟 [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)，展示四個代理如何串接成順序編排。
2. 按 `F5` 啟動多代理工作流程的 **Agent Inspector**。
3. 在 Inspector 聊天視窗貼上一段短職務說明及範例履歷。
4. 解說四代理流程：履歷解析器、職務需求擷取器、匹配評分器與建議撰寫者。
5. 說明每個子代理的輸出如何成為下一代理的上下文，強調交接範式。
6. 展示 [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml)，並與示範 1 的單代理版本比較。

---

## 主持技巧

- **提前設定期待。** Hosted Agents 正在預覽中—事先說明地域限制與配額狀況，避免學員中途驚訝。
- **先執行前置條件任務。** 兩個實作課程均提供 `Validate prerequisites` VS Code 任務，請學員先執行此任務再撰寫程式碼。
- **保持 Agent Inspector 顯示。** 多數 “啊哈” 時刻發生在學員見證本地 `/responses` 訊息循環亮起時。
- **準備備用專案。** 若學員的 Foundry 專案遭遇配額限制，請提供預先建置的專案以便部署，避免課堂受阻。
- **配對學員。** 進行實作課程 02（多代理）時，學員能與夥伴討論編排流程會顯著降低難度。
- **使用文件模組作為斷點。** 每個實作課程的 `docs/` 資料夾分成 8 個編號模組，作為自然中場停頓點。
- **事先拉取基底 Docker 映像** 於共用實驗機器，避免受註冊表速率限制影響。

---

## 主持過程中除錯

| 現象                                     | 首要嘗試方法                                                                           |
|-----------------------------------------|----------------------------------------------------------------------------------------|
| Agent Inspector 無法連線                 | 確認埠號 `8088` 是否空閒，且 `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` 任務是否在執行。 |
| 除錯器無法附加                         | 確認埠號 `5679` 是否空閒；若已被 `debugpy` 佔用，請重啟 VS Code。                        |
| `azd up` 驗證錯誤                       | 執行 `az login` 與 `azd auth login`，確保使用正確租戶。                               |
| 部署卡在 ACR push                       | 確認 Docker Desktop 正在運行且使用者對註冊表具備 `AcrPush` 權限。                         |
| 模型回傳 404 / deployment-not-found    | `agent.yaml` 中模型部署名稱必須與 Foundry 專案中部署一致。                               |

| 託管代理停留在 `Provisioning` 狀態         | 驗證專案區域是否[支援託管代理](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)以及是否有可用配額。 |
| Playground 返回 401                       | 從 VS Code 活動欄重新認證 Foundry 擴充功能。                                     |

如需更深入的指導，每個實驗室都會提供自己的 `08-troubleshooting.md` 文件 - 請將學習者導向該文件：

- 實驗室 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- 實驗室 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## 自訂此課程

歡迎您依據受眾調整工作坊。常見變體：

- **後端受眾：** 多花時間在 `agent.yaml`、Docker 和 ACR；縮短 playground 示範。
- **平民開發者受眾：** 留在 Foundry 擴充功能 UI 進行腳手架；減少 CLI 步驟。
- **單軌 60 分鐘時段：** 僅提供介紹、示範和實驗室 01。
- **僅工作坊（無投影片）格式：** 開啟兩個實驗室的 README，並將其作為主要腳本。

如果您擴充了實驗室，請透過 PR 貢獻回去，讓其他講師受益。

---

## 額外資源

- [Microsoft Foundry 文件](https://learn.microsoft.com/azure/ai-foundry/)
- [託管代理概述](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [快速開始：部署您的第一個託管代理 (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [部署託管代理（操作指南）](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## 聯絡資料

若對授課此課程有疑問，請在[工作坊儲存庫](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues)開啟議題並標記維護人員。

| 角色                | 姓名           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| 維護人 / 聯絡人     | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->