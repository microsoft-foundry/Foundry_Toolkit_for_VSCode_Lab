# 模块 7 - 在 Playground 中验证

⏱️ ~10 分钟

在本模块中，您将在 VS Code 和 Foundry 门户中测试已部署的多代理工作流，确认代理行为与本地测试一致。

---

## 为什么部署后还要测试？

托管环境与本地环境有几个重要差异：

| | 本地 | 托管 |
|--|-------|--------|
| <strong>身份</strong> | 您的个人登录（`DefaultAzureCredential`） | 每个代理专用的 Entra 身份（在部署时自动配置） |
| <strong>端点</strong> | `http://localhost:8088/responses` | 由 Foundry 代理服务管理的 URL |
| <strong>网络</strong> | 您的机器 → Azure OpenAI + MCP | Azure 骨干网（更低延迟） |

配置错误的环境变量、RBAC 问题或被阻止的 MCP 出站调用会首先在这里显现。

---

## 选项 A：在 VS Code Playground 测试（推荐先做）

### 第 1 步：导航到托管代理

1. 点击活动栏中的 **Foundry Toolkit** 图标。
2. 展开您的项目 → **Hosted Agents (Preview)** → 找到您的代理。

![Foundry Toolkit 侧边栏显示 Hosted Agents (Preview) 包含 resume-job-fit-evaluator 及其已部署版本](../../../../../translated_images/zh-CN/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### 第 2 步：选择一个版本

1. 点击代理以展开其版本列表。
2. 点击 `v1` → 验证状态为 **active**（侧边栏可能显示“Running”或“Started”，两者均表示准备就绪状态）。

### 第 3 步：打开 Playground

1. 点击 **Playground**（或右键点击版本 → **Open in Playground**）。
2. 聊天窗口会在 VS Code 标签页中打开。

### 第 4 步：运行冒烟测试

使用来自[模块 5](05-test-locally.md)的相同 3 个测试。在 Playground 输入框中输入每条消息并按 <strong>发送</strong>（或 <strong>回车</strong>）。

#### 测试 1 - 完整简历 + 职位说明（标准流程）

粘贴模块 5 中测试 1 的完整简历 + 职位说明提示（Jane Doe + Contoso Ltd 高级云工程师）。

**预期结果：**
- 带细分数学的适配评分（100分制）
- 匹配技能部分
- 缺少技能部分
- <strong>每个缺失技能一张差距卡</strong>，带 Microsoft Learn 链接
- 具备时间线的学习路线图

#### 测试 2 - 快速简短测试（最小输入）

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**预期结果：**
- 较低的适配评分（< 40）
- 诚实的评估及分阶段学习路径
- 多张差距卡（AWS、Kubernetes、Terraform、CI/CD、经验差距）

#### 测试 3 - 高适配候选人

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**预期结果：**
- 高适配评分（≥ 80）
- 重点关注面试准备和润色
- 差距卡很少或没有
- 短时间线，专注准备工作

### 第 5 步：与本地结果对比

打开您在模块 5 中保存本地响应的笔记或浏览器标签页。针对每个测试：

- 响应是否具有<strong>相同结构</strong>（适配评分、差距卡、路线图）？
- 是否遵循<strong>相同的评分标准</strong>（100分细分）？
- 差距卡中是否仍包含<strong>Microsoft Learn 链接</strong>？
- 是否<strong>每个缺失技能对应一张差距卡</strong>（未被截断）？

> <strong>少量措辞差异是正常的</strong> — 模型非确定性。关注结构、评分一致性及 MCP 工具的使用。

---

## 选项 B：在 Foundry 门户测试

[Foundry 门户](https://ai.azure.com) 提供基于网页的 Playground，方便与团队成员或利益相关者共享。

### 第 1 步：打开 Foundry 门户

1. 打开浏览器，访问 [https://ai.azure.com](https://ai.azure.com)。
2. 使用您在整个工作坊中使用的相同 Azure 账号登录。

### 第 2 步：导航到您的项目

1. 在首页左侧栏找到 **Recent projects**。
2. 点击您的项目名称（例如 `workshop-agents`）。
3. 如果看不到，点击 **All projects** 并搜索项目。

### 第 3 步：找到您已部署的代理

1. 在项目左侧导航中，点击 **Build** → **Agents**（或查找 **Agents** 部分）。
2. 您会看到代理列表，找到您已部署的代理（例如 `resume-job-fit-evaluator`）。
3. 点击代理名称打开其详情页面。

### 第 4 步：打开 Playground

1. 在代理详情页顶部工具栏中查看。
2. 点击 **Open in playground**（或 **Try in playground**）。
3. 会打开聊天界面。

### 第 5 步：运行相同的冒烟测试

重复上面 VS Code Playground 部分的所有 3 个测试。将每个响应与本地结果（模块 5）和 VS Code Playground 结果（选项 A）进行比较。

---

## 多代理特定验证

除了基本正确性外，还需验证这些多代理特定行为：

### MCP 工具执行

| 检查 | 如何验证 | 通过条件 |
|-------|---------------|----------------|
| MCP 调用成功 | 差距卡包含 `learn.microsoft.com` 链接 | 是真实链接，而非回退提示 |
| 多次 MCP 调用 | 每个高/中优先级差距均有资源 | 不只是第一张差距卡 |
| MCP 回退工作正常 | 如果缺少链接，则检查回退文本 | 代理仍产生差距卡（有无链接均可） |

### 代理协调

| 检查 | 如何验证 | 通过条件 |
|-------|---------------|----------------|
| 4 个代理均运行 | 输出包含适配评分和差距卡 | 评分来自 MatchingAgent，卡片来自 GapAnalyzer |
| 顺序执行 | 响应时间合理（< 2 分钟） | 若 > 3 分钟，检查终端日志是否有错误 |
| 数据流完整性 | 差距卡引用匹配报告中的技能 | 不包含职位说明中未提及的幻觉技能 |

---

## 验证评分标准

使用该评分标准评估多代理工作流的托管行为：

| # | 标准 | 通过条件 | 通过？ |
|---|----------|---------------|-------|
| 1 | <strong>功能正确性</strong> | 代理对简历 + 职位说明响应具备适配评分和差距分析 | |
| 2 | <strong>评分一致性</strong> | 适配评分使用 100 分标准及细分计算 | |
| 3 | <strong>差距卡完整性</strong> | 每个缺失技能一张卡（无截断或合并） | |
| 4 | **MCP 工具集成** | 差距卡包含真实的 Microsoft Learn 链接 | |
| 5 | <strong>结构一致性</strong> | 本地与托管运行输出结构匹配 | |
| 6 | <strong>响应时间</strong> | 托管代理对完整评估响应时间在 2 分钟内 | |
| 7 | <strong>无错误</strong> | 无 HTTP 500 错误、超时或空响应 | |

> “通过”表示在至少一个 Playground（VS Code 或门户）中，所有 3 个冒烟测试均满足上述 7 条标准。

---

## 解决 Playground 问题

| 症状 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| Playground 无法加载 | 容器状态非 `active` | 返回[模块 6](06-deploy-to-foundry.md)，验证部署状态。如果显示 `creating`，请稍等 |
| 代理返回空响应 | 模型部署名称不匹配 | 检查 `agent.yaml` 中 `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` 是否与已部署模型一致 |
| 代理返回错误消息 | 缺少 [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 权限 | 在项目范围内分配 **[Foundry User](https://aka.ms/foundry-ext-project-role)**（之前称为 Azure AI User）角色 |
| 差距卡无 Microsoft Learn 链接 | MCP 出站被阻止或 MCP 服务器不可用 | 检查容器是否能访问 `learn.microsoft.com`。参见[模块 8](08-troubleshooting.md) |
| 只有 1 张差距卡（被截断） | GapAnalyzer 指令缺少 "CRITICAL" 块 | 复查 [模块 3，步骤 2.4](03-configure-agents.md) |
| 适配评分与本地相差较大 | 部署了不同模型或指令 | 比较 `agent.yaml` 环境变量和本地 `.env` 文件。必要时重新部署 |
| 门户显示“Agent not found” | 部署尚在传播或失败 | 等待 2 分钟后刷新，若仍缺失，从[模块 6](06-deploy-to-foundry.md)重新部署 |

---

### 检查点

- [ ] 在 VS Code Playground 中测试代理 - 所有 3 个冒烟测试通过
- [ ] 在 [Foundry 门户](https://ai.azure.com) Playground 中测试代理 - 所有 3 个冒烟测试通过
- [ ] 响应结构与本地测试保持一致（适配评分、差距卡、路线图）
- [ ] 差距卡中存在 Microsoft Learn 链接（托管环境中 MCP 工具正常工作）
- [ ] 每个缺失技能对应一张差距卡（无截断）
- [ ] 测试中无错误或超时
- [ ] 完成验证评分标准（全部 7 条标准通过）

---

**上一步：** [06 - 部署到 Foundry](06-deploy-to-foundry.md) · **下一步：** [08 - 故障排除 →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->