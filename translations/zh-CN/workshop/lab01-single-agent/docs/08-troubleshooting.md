# 第8模块 - 故障排除

本模块是工作坊中遇到的每个常见问题的参考指南。请收藏它——每当出现问题时，您都会回来查看。

---

## 1. 权限错误

### 1.1 `agents/write` 权限被拒绝

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**根本原因：** 您在<strong>项目</strong>级别没有 `Azure AI User` 角色。这是工作坊中最常见的错误。

**解决方法 - 逐步：**

1. 打开 [https://portal.azure.com](https://portal.azure.com)。
2. 在顶部搜索栏中输入您的<strong>Foundry项目</strong>名称（例如，`workshop-agents`）。
3. **关键：** 点击显示类型为 **“Microsoft Foundry project”** 的结果，而不是父账户/中心资源。这些是不同的资源，具有不同的RBAC作用域。
4. 在项目页面左侧导航中，点击 **访问控制（IAM）**。
5. 点击 <strong>角色分配</strong> 选项卡，检查您是否已经拥有该角色：
   - 搜索您的姓名或邮箱。
   - 如果已列出 `Azure AI User` → 错误原因是其他（请查看下面第8步）。
   - 如果未列出 → 继续添加。
6. 点击 **+ 添加** → <strong>添加角色分配</strong>。
7. 在 <strong>角色</strong> 选项卡：
   - 搜索 [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles)。
   - 从结果中选择它。
   - 点击 <strong>下一步</strong>。
8. 在 <strong>成员</strong> 选项卡：
   - 选择 **用户、组或服务主体**。
   - 点击 **+ 选择成员**。
   - 搜索您的姓名或邮箱。
   - 从结果中选择自己。
   - 点击 <strong>选择</strong>。
9. 点击 **审查 + 分配** → 再次点击 **审查 + 分配**。
10. **等待1-2分钟** - RBAC更改需要时间传播。
11. 重试失败的操作。

> **为什么Owner/Contributor角色不够用：** Azure RBAC具有两种权限类型——<em>管理操作</em>和<em>数据操作</em>。Owner和Contributor授予管理操作（创建资源，编辑设置），但代理操作需要 `agents/write` <strong>数据操作</strong>，该权限只包含在 `Azure AI User`、`Azure AI Developer` 或 `Azure AI Owner` 角色中。详情见 [Foundry RBAC文档](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)。

### 1.2 资源配置期间出现 `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**根本原因：** 您没有权限在此订阅/资源组中创建或修改Azure资源。

**解决方法：**
1. 请订阅管理员为您分配Foundry项目所在资源组的<strong>贡献者(Contributor)</strong>角色。
2. 或者，要求他们为您创建Foundry项目，并授予您项目的<strong>Azure AI User</strong>角色。

### 1.3 出现 `SubscriptionNotRegistered`，针对 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**根本原因：** 该Azure订阅尚未注册Foundry所需的资源提供程序。

**解决方法：**

1. 打开终端，运行：
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. 等待注册完成（可能需要1-5分钟）：
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   预期输出：“Registered”
3. 重试操作。

---

## 2. Docker错误（仅当已安装Docker时）

> Docker 对本次工作坊是<strong>可选的</strong>。以下错误仅适用于安装了Docker Desktop且Foundry扩展尝试本地容器构建时。

### 2.1 Docker守护进程未运行

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**解决方法 - 逐步：**

1. 在开始菜单（Windows）或应用程序文件夹（macOS）中找到并启动 **Docker Desktop**。
2. 等待Docker Desktop窗口显示 **"Docker Desktop is running"** ——通常需30-60秒。
3. 在系统托盘（Windows）或菜单栏（macOS）中查找Docker鲸鱼图标。鼠标悬停确认状态。
4. 在终端验证：
   ```powershell
   docker info
   ```
   如果打印出Docker系统信息（服务器版本、存储驱动等），说明Docker正在运行。
5. **Windows专用：** 如果Docker仍无法启动：
   - 打开Docker Desktop → <strong>设置</strong>（齿轮图标）→ <strong>常规</strong>。
   - 确保勾选了 **使用基于WSL 2的引擎**。
   - 点击 <strong>应用并重启</strong>。
   - 如果未安装WSL 2，请在提升权限的PowerShell中运行 `wsl --install` 并重启计算机。
6. 重试部署。

### 2.2 Docker构建因依赖错误失败

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**解决方法：**
1. 打开 `requirements.txt`，确认所有包名拼写正确。
2. 确认版本固定正确：
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. 在本地测试安装：
   ```bash
   pip install -r requirements.txt
   ```
4. 如果使用私有包索引，确保Docker有网络访问权限。

### 2.3 容器平台不匹配（苹果硅芯片）

如果从Apple Silicon Mac（M1/M2/M3/M4）部署，容器必须为 `linux/amd64` 构建，因为Foundry的容器运行时使用AMD64架构。

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry扩展的部署命令在大多数情况下会自动处理此问题。如果出现与架构相关的错误，请使用 `--platform` 标志手动构建，并联系Foundry团队。

---

## 3. 认证错误

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) 令牌获取失败

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**根本原因：** `DefaultAzureCredential`链中的所有凭据来源均无有效令牌。

**解决方法 - 按顺序尝试：**

1. **通过Azure CLI重新登录**（最常见的修复方法）：
   ```bash
   az login
   ```
   会打开浏览器窗口。登录后回到VS Code。

2. **设置正确的订阅：**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   如果这不是正确的订阅：
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **通过VS Code重新登录：**
   - 点击VS Code左下角的<strong>账户</strong>图标（人物图标）。
   - 点击您的账户名 → <strong>注销</strong>。
   - 再次点击账户图标 → <strong>登录微软账户</strong>。
   - 完成浏览器登录流程。

4. **服务主体（仅限CI/CD场景）：**
   - 在您的 `.env` 文件中设置以下环境变量：
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - 然后重启代理进程。

5. **检查令牌缓存：**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   如果失败，说明CLI令牌已过期。请再次运行 `az login`。

### 3.2 本地令牌有效，托管部署中无效

**根本原因：** 托管代理使用系统托管身份，与个人凭据不同。

**解决方法：** 这是预期行为——托管身份会在部署时自动配置。如果托管代理仍然出现认证错误：
1. 检查Foundry项目的托管身份是否有权限访问Azure OpenAI资源。
2. 确认 `agent.yaml` 中的 `PROJECT_ENDPOINT` 是否正确。

---

## 4. 模型错误

### 4.1 找不到模型部署

```
Error: Model deployment not found / The specified deployment does not exist
```

**解决方法 - 逐步：**

1. 打开您的 `.env` 文件，记下 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 的值。
2. 打开VS Code中的 **Microsoft Foundry** 侧边栏。
3. 展开您的项目 → <strong>模型部署</strong>。
4. 比较侧边栏列出的部署名称与您 `.env` 文件中的值。
5. 名称<strong>区分大小写</strong> —— `gpt-4o` 与 `GPT-4o` 是不同的。
6. 如果不匹配，更新 `.env` 以使用侧边栏中显示的准确名称。
7. 对于托管部署，还需更新 `agent.yaml`：
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 模型返回内容异常

**解决方法：**
1. 检查 `main.py` 中的 `EXECUTIVE_AGENT_INSTRUCTIONS` 常量。确保其未被截断或损坏。
2. 检查模型温度设置（如果可配置）——较低值输出更确定。
3. 比较部署的模型（例如 `gpt-4o` 和 `gpt-4o-mini`）——不同模型功能不同。

---

## 5. 部署错误

### 5.1 ACR拉取授权

```
Error: AcrPullUnauthorized
```

**根本原因：** Foundry项目的托管身份无法从Azure容器注册表拉取容器镜像。

**解决方法 - 逐步：**

1. 打开 [https://portal.azure.com](https://portal.azure.com)。
2. 在顶部搜索栏中搜索 **[容器注册表](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**。
3. 单击与您的Foundry项目关联的注册表（通常在相同资源组）。
4. 在左侧导航中，点击 **访问控制（IAM）**。
5. 点击 **+ 添加** → <strong>添加角色分配</strong>。
6. 搜索 **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**，选择它。点击 <strong>下一步</strong>。
7. 选择 <strong>托管身份</strong> → 点击 **+ 选择成员**。
8. 查找并选择Foundry项目的托管身份。
9. 点击 <strong>选择</strong> → **审查 + 分配** → **审查 + 分配**。

> 此角色分配通常由Foundry扩展自动设置。如果出现此错误，自动设置可能失败。您也可以尝试重新部署——扩展可能会重试设置。

### 5.2 部署后代理启动失败

**症状：** 容器状态保持“Pending”超过5分钟或显示“失败”。

**解决方法 - 逐步：**

1. 打开VS Code中的 **Microsoft Foundry** 侧边栏。
2. 点击您的托管代理 → 选择版本。
3. 在详情面板，检查 <strong>容器详情</strong> → 查找 <strong>日志</strong> 部分或链接。
4. 阅读容器启动日志。常见原因：

| 日志信息 | 原因 | 解决方案 |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | 缺少依赖 | 添加到 `requirements.txt` 并重新部署 |
| `KeyError: 'PROJECT_ENDPOINT'` | 缺少环境变量 | 在 `agent.yaml` 的 `env:` 下添加该环境变量 |
| `OSError: [Errno 98] Address already in use` | 端口冲突 | 确保 `agent.yaml` 中 `port: 8088` 且只有一个进程绑定该端口 |
| `ConnectionRefusedError` | 代理未开始监听 | 检查 `main.py` - 确保 `from_agent_framework()` 调用在启动时执行 |

5. 修复问题后，从[第6模块](06-deploy-to-foundry.md)重新部署。

### 5.3 部署超时

**解决方法：**
1. 检查网络连接——Docker推送可能较大（初次部署超过100MB）。
2. 如果处于企业代理后，请确保配置了Docker Desktop代理设置：**Docker Desktop** → <strong>设置</strong> → <strong>资源</strong> → <strong>代理</strong>。
3. 重试——网络故障可能导致暂时性失败。

---

## 6. 快速参考：RBAC角色

| 角色 | 典型作用域 | 授予权限 |
|------|------------|----------|
| **Azure AI User** | 项目 | 数据操作：构建、部署和调用代理（`agents/write`，`agents/read`） |
| **Azure AI Developer** | 项目或账户 | 数据操作 + 项目创建 |
| **Azure AI Owner** | 账户 | 完全访问 + 角色分配管理 |
| **Azure AI Project Manager** | 项目 | 数据操作 + 可分配 Azure AI User 角色给他人 |
| **Contributor** | 订阅/资源组 | 管理操作（创建/删除资源）。<strong>不包含数据操作</strong> |
| **Owner** | 订阅/资源组 | 管理操作 + 角色分配。<strong>不包含数据操作</strong> |
| **Reader** | 任意 | 只读管理访问 |

> **关键结论：** `Owner` 和 `Contributor` 不包含数据操作权限。代理操作始终需要 `Azure AI *` 相关角色。对本工作坊而言，最低角色是<strong>项目</strong>范围内的 **Azure AI User**。

---

## 7. 工作坊完成检查清单

当完成所有工作时，请使用此清单作为最终签收：

| # | 项目 | 模块 | 通过？ |
|---|------|------|-------|
| 1 | 安装并验证所有先决条件 | [00](00-prerequisites.md) | |
| 2 | 安装Foundry Toolkit和Foundry扩展 | [01](01-install-foundry-toolkit.md) | |
| 3 | 创建Foundry项目（或选择现有项目） | [02](02-create-foundry-project.md) | |
| 4 | 部署模型（例如，gpt-4o） | [02](02-create-foundry-project.md) | |
| 5 | 在项目范围内分配 Azure AI 用户角色 | [02](02-create-foundry-project.md) | |
| 6 | 搭建托管代理项目脚手架（agent/） | [03](03-create-hosted-agent.md) | |
| 7 | 在 `.env` 中配置 PROJECT_ENDPOINT 和 MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | 在 main.py 中自定义代理指令 | [04](04-configure-and-code.md) | |
| 9 | 创建虚拟环境并安装依赖项 | [04](04-configure-and-code.md) | |
| 10 | 使用 F5 或终端在本地测试代理（4 个冒烟测试通过） | [05](05-test-locally.md) | |
| 11 | 部署到 Foundry Agent 服务 | [06](06-deploy-to-foundry.md) | |
| 12 | 容器状态显示为“Started”或“Running” | [06](06-deploy-to-foundry.md) | |
| 13 | 在 VS Code Playground 中验证（4 个冒烟测试通过） | [07](07-verify-in-playground.md) | |
| 14 | 在 Foundry Portal Playground 中验证（4 个冒烟测试通过） | [07](07-verify-in-playground.md) | |

> **恭喜！** 如果所有项目均已勾选，说明您已完成整个工作坊。您已从零开始构建了托管代理，在本地进行了测试，部署到了 Microsoft Foundry，并在生产环境中验证了它。

---

**上一篇：** [07 - 在 Playground 中验证](07-verify-in-playground.md) · **首页：** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译。虽然我们努力保证准确性，但请注意自动翻译可能包含错误或不准确之处。原始文件的母语版本应被视为权威来源。对于关键信息，建议采用专业人工翻译。本公司不对因使用此翻译而产生的任何误解或误读承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->