# 模块 8 - 故障排除

本模块为常见问题参考指南。请收藏，遇到问题时返回查阅。

---

## 1. 权限错误

### 1.1 `agents/write` 权限被拒绝

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**根本原因：** 缺少在 <strong>项目</strong> 级别的 `Azure AI User` 角色。这是最常见的工作坊错误。

**修复方法：**
1. 打开 [portal.azure.com](https://portal.azure.com)。
2. 搜索你的 Foundry <strong>项目</strong> 名称 → 点击类型为 **"Microsoft Foundry project"** 的结果（非上级账户）。
3. **访问控制 (IAM)** → **+ 添加** → <strong>添加角色分配</strong>。
4. 角色：**Azure AI User** → 下一步。
5. 成员：选择你自己 → 审查 + 分配 → 审查 + 分配。
6. **等待1–2分钟** → 重试。

> **为什么 Owner/Contributor 不够：** 这些角色仅授予<em>管理</em>操作。代理操作需要 `agents/write` <em>数据操作</em>，该权限仅存在于 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner` 中。详见 [Foundry RBAC 文档](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 配置时出现 `AuthorizationFailed`

**修复：** 让管理员在资源组上分配 **Contributor** 角色，或让他们为你创建项目并授予你 **Azure AI User** 角色。

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# 等待直到：“已注册”
```

---

## 2. Docker 错误

> Docker 是<strong>可选</strong>的。以下只适用于安装了 Docker Desktop 且扩展尝试本地构建的情况。

### 2.1 Docker 守护进程未运行

**修复：** 启动 Docker Desktop → 等待“运行中”状态 → 使用 `docker info` 验证 → 重试。

### 2.2 构建因依赖错误失败

**修复：** 检查 `requirements.txt` 拼写，本地先测试：`pip install -r requirements.txt`。

### 2.3 平台不匹配（Apple Silicon）

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. 认证错误

### 3.1 `DefaultAzureCredential` 失败

**修复（按顺序尝试）：**
1. 运行 `az login`（重新认证）
2. 运行 `az account set --subscription "<id>"`（切换正确订阅）
3. VS Code → 账户 → 登出 → 重新登录
4. 验证：`az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 本地令牌有效，托管环境无效

**预期行为：** 托管代理使用系统托管身份，而非你的凭据。如果托管代理出现认证错误：
- 验证 `agent.yaml` 中的 `AZURE_AI_PROJECT_ENDPOINT` 是否正确
- 检查项目的托管身份是否具有模型访问权限

---

## 4. 模型错误

### 4.1 找不到模型部署

**修复：** 名称<strong>区分大小写</strong>。对比 `.env` 文件中 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 与 Foundry 侧边栏 → 模型中的精确名称。

### 4.2 模型输出异常

**修复：** 检查 `main.py` 中的 `AGENT_INSTRUCTIONS`（是否被截断？）。尝试不同模型（`gpt-4.1` vs `gpt-4.1-mini`）。

---

## 5. 部署错误

### 5.1 ACR 拉取权限不足

**修复：** 在 Azure 门户 → 容器注册表 → 访问控制 (IAM) → 为 Foundry 项目托管身份添加 **AcrPull** 角色。

### 5.2 代理启动失败（状态为“等待中”或“失败”）

检查侧边栏容器日志。常见原因：

| 日志信息 | 修复 |
|-------------|-----|
| `ModuleNotFoundError` | 在 `requirements.txt` 添加缺失包，重新部署 |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | 在 `agent.yaml` 的 `environment_variables` 添加该环境变量 |
| `Address already in use` | 确保只有一个进程绑定端口 8088 |

### 5.3 部署超时

**修复：** 检查网络连接。首次部署会推送 >100MB。如果在代理环境下？配置 Docker Desktop 代理设置。

---

## 6. 路径 B - Foundry Local

### 6.1 Foundry Local 无法启动

| 问题 | 修复 |
|-------|-----|
| `foundry: command not found` | 重新安装：`winget install Microsoft.FoundryLocal` |
| 资源不足 | Foundry Local 需要约4GB空闲内存。关闭其他应用。 |
| 模型下载失败 | 检查磁盘空间（模型大小2–8 GB）。重试：`foundry local models pull <name>` |

### 6.2 Foundry Local 模型错误

| 问题 | 修复 |
|-------|-----|
| 响应缓慢 | 正常 - 本地模型除非有GPU，否则运行在CPU上。请耐心等待。 |
| 输出质量差 | 如果硬件条件允许，尝试更大模型。`phi-4-mini` 是较好的平衡选择。 |
| 连接被拒绝 | 验证 Foundry Local 是否运行：`foundry local status`。需要时重启。 |

---

## 7. 快速参考：RBAC 角色

| 角色 | 范围 | 授权权限 |
|------|-------|--------|
| **Azure AI User** | 项目 | 数据操作：`agents/write`, `agents/read` |
| **Azure AI Developer** | 项目/账户 | 数据操作 + 项目创建 |
| **Azure AI Owner** | 账户 | 完全访问 + 角色管理 |
| **Contributor** | 订阅/资源组 | 仅管理操作（<strong>无</strong>数据操作） |
| **Owner** | 订阅/资源组 | 管理 + 角色分配（<strong>无</strong>数据操作） |

---

## 8. 工作坊完成清单

| # | 项目 | 模块 |
|---|------|--------|
| 1 | 安装并验证前置条件 | [00](00-prerequisites.md) |
| 2 | 安装 Foundry Toolkit 扩展，连接项目（或配置路径 B） | [01](01-setup.md) |
| 3 | 搭建托管代理骨架 | [02](02-create-hosted-agent.md) |
| 4 | 配置 `.env`，编写指令，安装依赖 | [03](03-configure-and-code.md) |
| 5 | 本地测试代理 - 3 个功能场景通过 | [04](04-test-locally.md) |
| 6 | 部署到 Foundry（仅路径 A） | [05](05-deploy-to-foundry.md) |
| 7 | 边缘情况/安全测试云端通过（仅路径 A） | [06](06-verify-in-playground.md) |
| 8 | 审阅总结，确定下一步 | [07](07-summary.md) |

---

**上一篇：** [07 - 总结](07-summary.md) · **首页：** [工作坊自述文件](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->