# 如何进行本次课程讲授

感谢您参与本次课程的讲授！

在授课之前，请确保：

1. 完整阅读本文档及包含的所有资源。
2. 观看课程讲授录制视频和工作坊端到端演示视频。
3. 在活动开始前，至少在您的电脑上完整体验两次动手实验。
4. 验证您的 Microsoft Foundry 项目、模型部署及配额。
5. 如有任何不清楚的地方，请联系维护者。

---

## 文件概要

| 资源                        | 链接                                                                             | 描述                                                                                       |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| 工作坊幻灯片                | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | 本工作坊的演示幻灯片，含讲师备注和嵌入的演示视频                                          |
| 课程讲授录制                | _由维护者提供_                                                                               | 工作坊介绍和幻灯片讲解录制视频                                                             |
| 工作坊端到端录制           | _由维护者提供_                                                                               | 以学习者视角完整录制的两场动手实验                                                         |
| 工作坊文档                  | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | 源码仓库、实验阅读文件、逐步模块内容                                                       |
| 实验01 - 单代理              | [Lab 01](../workshop/lab01-single-agent/README.md)                               | 动手实验：构建、测试并部署<em>Explain Like I'm an Executive</em>托管代理                          |
| 实验02 - 多代理工作流        | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | 动手实验：构建包含4个代理的<em>Resume to Job Fit Evaluator</em>工作流                           |
| 演示1：执行代理              | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | 实验01演示：将技术术语翻译成执行摘要                                                      |
| 演示2：简历职位匹配评估器   | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | 实验02演示：4代理工作流，评分简历职位匹配度并生成推荐                                    |

> **讲师注意：** 一旦录制视频发布，我们将添加幻灯片和视频链接。在此之前，请联系维护者（参见[联系方式](#联系方式)）获取最新资料。

---

## 入门

本工作坊教授开发者如何使用 **Microsoft Foundry Toolkit** 扩展，通过 VS Code 完全构建、测试并部署 AI 代理到 **Microsoft Foundry Agent Service** 作为 <strong>托管代理</strong>。

工作坊分为多个部分，包括幻灯片、<strong>2个现场演示</strong>和<strong>2个动手实验</strong>。

### 时间安排

#### 全程讲授（约2小时）

| 时间           | 内容说明                                                           |
|----------------|-------------------------------------------------------------------|
| 0:00 - 10:00   | 介绍：托管代理、Foundry Agent 服务及工具包                        |
| 10:00 - 20:00  | 演示：执行代理端到端操作                                          |
| 20:00 - 60:00  | 实验01 - 单代理（构建、本地测试、部署、游乐场）                   |
| 60:00 - 110:00 | 实验02 - 多代理工作流（简历职位匹配评估器）                       |
| 110:00 - 120:00| 总结、答疑及持续学习资源                                          |

#### 简短讲授（约75分钟）

| 时间          | 内容说明                                                   |
|---------------|------------------------------------------------------------|
| 0:00 - 10:00  | 介绍和概览                                               |
| 10:00 - 20:00 | 演示：执行代理                                          |
| 20:00 - 70:00 | 仅实验01（指导学员自学实验02）                          |
| 70:00 - 75:00 | 总结和答疑                                              |

### 准备工作

| 资源                           | 链接                                                                                          | 描述                                               |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| 工作坊文档                     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | 工作坊文档及源码                                   |
| 实验01说明                     | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | 动手实验：单一托管代理                             |
| 实验02说明                     | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | 动手实验：多代理工作流                             |
| 先决条件检查列表              | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | 所需工具、账号及 Azure 访问权限                    |
| 托管代理快速入门（azd）        | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | 使用 `azd` 部署托管代理的官方快速入门文档          |
| 托管代理区域可用性            | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | 托管代理支持区域（预览）                           |

### 讲师先决条件

在进行讲授前，请确保您拥有：

- 一个具有创建资源权限的 **Azure 订阅**（资源组的所有者或参与者权限）。
- 访问位于[支持托管代理的区域](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)的 **Microsoft Foundry 项目**。
- 在您的 Foundry 项目中拥有 **gpt-4.1**（或 **gpt-4.1-mini**）的配额。
- 安装好以下工具：
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit 扩展](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/)（可选）
  - Python 3.10 或更高版本

最好在讲授之前至少运行一次[使用 `azd` 的托管代理快速入门](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)，以确保你拥有一个已验证的 Foundry 项目、模型部署和 Azure 容器注册表，如学员遇到问题可以作为参考。

---

## 幻灯片讲解流程

幻灯片内容与实验流程一致。每部分建议的讲解要点：

| 部分                       | 重点信息                                                                                               |
|---------------------------|-------------------------------------------------------------------------------------------------------|
| 标题和议程                | 将工作坊定位为 *从 VS Code 到 Foundry*，无需切换门户界面。                                            |
| 为什么选择托管代理？       | 管理型运行时，基于 ACR 部署，兼容 OpenAI 的 `/responses` API，作用域限定为 Foundry 项目。            |
| 架构图                   | 讲解[README 中的架构部分](../README.md#architecture)：脚手架、Inspector、ACR、Agent 服务。           |
| 托管代理结构              | `agent.yaml`、`Dockerfile`、`main.py`、`requirements.txt` —— 每个文件的功能说明。                         |
| 现场演示：执行代理         | 切换到 VS Code 并运行 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) 端到端演示（参见[演示1](#演示1：执行代理)）。 |
| 现场演示：简历职位匹配评估器 | 切换到 VS Code 并运行 [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4代理演示（参见[演示2](#演示2：简历职位匹配评估器)）。 |
| 实验01简述                | 交给学员，指向 [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md)。 |
| 多代理模式                | 顺序执行、并发执行和交接模式——在实验02开始前进行预览。                                               |
| 实验02简述                | 交给学员，指向 [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md)。   |
| 总结及资源                | 持续学习相关链接，详见[附加资源](#附加资源)章节。                                          |

---

## 演示

演讲中包含两个现场演示，每个演示分配10分钟时间。

| 演示       | 实验    | 文件路径                                                                        | 演示内容                                  |
|-----------|---------|---------------------------------------------------------------------------------|-------------------------------------------|
| 执行代理   | 实验01  | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)      | 单托管代理；将技术术语转化为执行摘要        |
| 简历职位匹配评估器 | 实验02  | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4代理编排；评分简历与职位匹配度并生成推荐  |

### 演示1：执行代理

此单代理位于[`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)，适合作为实验01前的10分钟演示。

1. 打开 [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py)，介绍代理定义（系统提示、模型、框架）。
2. 按 `F5` 启动本地 **Agent Inspector**。
3. 粘贴来自 [README](../README.md#see-it-in-action) 的示例提示，展示执行摘要响应。
4. 展示 [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) 和 [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile)，解释部署相关文件。
5. 演示部署流程（Docker 构建、ACR 推送、托管代理创建），无需等待完成。

### 演示2：简历职位匹配评估器

一个位于[`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)的4代理工作流，适合实验02前的10分钟演示。

1. 打开 [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)，展示四个代理如何在顺序编排中连接。
2. 按 `F5` 启动多代理工作流的 **Agent Inspector**。
3. 在 Inspector 聊天中粘贴一段简短的职位描述和示范简历。
4. 逐步讲解四代理流程：简历解析器、职位需求提取器、匹配度评分器和推荐编写器。
5. 指出每个子代理的输出如何成为下一个代理的上下文，突出交接模式。
6. 展示 [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml)，并与演示1中的单代理示例进行对比。

---

## 讲授技巧

- **提前设定期望。** 托管代理仍处于预览阶段——提前说明区域限制和配额，避免学员在实验中途惊讶。
- **先运行先决条件任务。** 两个实验都带有 `Validate prerequisites` VS Code 任务，要求学员在编写任何代码前先运行。
- **保持 Agent Inspector 可见。** 大多数“顿悟”时刻都发生在学员看到本地 `/responses` 往返请求高亮时。
- **准备备用项目。** 若学员的 Foundry 项目配额不足，提供预先配置好的项目用于部署，避免阻塞课堂进度。
- **配对学员。** 实验02（多代理）在学员能相互讨论编排时效果明显更佳。
- **利用文档模块作为检验点。** 每个实验的 `docs/` 目录分成8个编号模块，可作为自然的暂停点。
- **事先拉取基础 Docker 镜像**，特别是在共享实验机器上，避免因为注册表访问频率限制导致的阻塞。

---

## 讲授过程中的故障排查

| 现象                                    | 首选解决措施                                                                                   |
|---------------------------------------|------------------------------------------------------------------------------------------------|
| Agent Inspector 无法连接               | 确认端口 `8088` 空闲，且 `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` 任务正在运行。      |
| 调试器无法附加                       | 检查端口 `5679` 是否被占用；若 `debugpy` 已绑定，重启 VS Code。                               |
| `azd up` 认证失败                     | 运行 `az login` 和 `azd auth login`，确保选中正确租户。                                       |
| 部署过程卡在 ACR 推送阶段             | 检查 Docker Desktop 是否在运行，且用户对注册表具有 `AcrPush` 权限。                           |
| 模型返回 404 / 部署未找到             | `agent.yaml` 中模型部署名称必须与 Foundry 项目中的部署名称相符。                               |

| 托管代理卡在 `Provisioning` 状态         | 验证项目区域是否[支持托管代理](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)以及配额是否可用。 |
| Playground 返回 401                       | 从 VS Code 活动栏重新进行 Foundry 扩展的身份验证。                                     |

对于更深入的指导，每个实验室都附带自己的 `08-troubleshooting.md` 文档 - 引导学习者查看该文档：

- 实验室 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- 实验室 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## 自定义本次课程

欢迎根据您的受众调整本次工作坊。常见变体包括：

- **后端受众：** 花更多时间讲解 `agent.yaml`、Docker 和 ACR；精简 Playground 演示。
- **公民开发者受众：** 保持在 Foundry 扩展 UI 中进行脚手架操作；减少 CLI 步骤。
- **单轨 60 分钟时段：** 仅讲解介绍、演示和实验室 01。
- **仅工作坊（无幻灯片）格式：** 打开两个实验室的自述文件，并将其用作主要脚本。

如果您扩展了实验内容，请通过 PR 贡献变更，以惠及其他培训师。

---

## 附加资源

- [Microsoft Foundry 文档](https://learn.microsoft.com/azure/ai-foundry/)
- [托管代理概述](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [快速入门：部署您的第一个托管代理 (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [部署托管代理（操作指南）](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry VS Code 工具包](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## 联系方式

如果您对本次课程的讲授有任何疑问，请在[工作坊仓库](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues)中提出 issue 并标记维护者。

| 角色               | 姓名           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| 维护者 / 联系    | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->