# Module 8 - 故障排除（多代理）

本模块涵盖多代理工作流中特有的常见错误、修复方法和调试策略。有关一般 Foundry 部署问题，也请参阅[实验 01 故障排除指南](../../lab01-single-agent/docs/08-troubleshooting.md)。

---

## 快速参考：错误 → 修复

| 错误 / 症状 | 可能原因 | 解决方法 |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | 缺少 `.env` 文件或变量未设置 | 创建 `.env`，内容包括 `PROJECT_ENDPOINT=<your-endpoint>` 和 `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | 未激活虚拟环境或依赖未安装 | 运行 `.\.venv\Scripts\Activate.ps1` 然后 `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | 未安装 MCP 包（缺失于 requirements） | 运行 `pip install mcp` 或检查 `requirements.txt` 是否作为传递依赖包含 |
| 代理启动却返回空响应 | `output_executors` 不匹配或缺少边 | 确认 `output_executors=[gap_analyzer]` 并且 `create_workflow()` 中所有边都存在 |
| 只有 1 张 gap 卡（其余缺失） | GapAnalyzer 指令不完整 | 在 `GAP_ANALYZER_INSTRUCTIONS` 中添加 `CRITICAL:` 段落 - 参见[模块 3](03-configure-agents.md) |
| 适配分数为 0 或缺失 | MatchingAgent 没有收到上游数据 | 确认存在 `add_edge(resume_parser, matching_agent)` 和 `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP 服务器拒绝工具调用 | 检查网络连接。尝试在浏览器打开 `https://learn.microsoft.com/api/mcp`。重试 |
| 输出中无 Microsoft Learn URL | MCP 工具未注册或端点错误 | 确认 GapAnalyzer 中 `tools=[search_microsoft_learn_for_plan]` 且 `MICROSOFT_LEARN_MCP_ENDPOINT` 正确 |
| `Address already in use: port 8088` | 端口 8088 被其他进程占用 | 运行 `netstat -ano \| findstr :8088`（Windows）或 `lsof -i :8088`（macOS/Linux）并停止冲突进程 |
| `Address already in use: port 5679` | Debugpy 端口冲突 | 停止其他调试会话。运行 `netstat -ano \| findstr :5679` 找到并结束进程 |
| 代理检查器打不开 | 服务器未完全启动或端口冲突 | 等待出现 “Server running” 日志。检查端口 5679 是否空闲 |
| `azure.identity.CredentialUnavailableError` | 未登录 Azure CLI | 运行 `az login` 后重启服务器 |
| `azure.core.exceptions.ResourceNotFoundError` | 模型部署不存在 | 检查 `MODEL_DEPLOYMENT_NAME` 是否匹配 Foundry 项目中已部署模型 |
| 部署后容器状态显示 "Failed" | 容器启动时崩溃 | 查看 Foundry 侧边栏的容器日志。常见原因：缺少环境变量或导入错误 |
| 部署显示 "Pending" 超过 5 分钟 | 容器启动过慢或资源限制 | 多代理启动时容器需等待最多 5 分钟（创建 4 个代理实例）。若仍未启动，查看日志 |
| `ValueError` 来自 `WorkflowBuilder` | 图配置无效 | 确保设置了 `start_executor`，`output_executors` 是列表，且不存在循环边 |

---

## 环境和配置问题

### 缺失或错误的 `.env` 值

`.env` 文件必须位于 `PersonalCareerCopilot/` 目录（与 `main.py` 同级）：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

预期 `.env` 内容：

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **查找你的 PROJECT_ENDPOINT：**  
- 在 VS Code 中打开 **Microsoft Foundry** 侧边栏 → 右键点击你的项目 → <strong>复制项目端点</strong>。  
- 或访问 [Azure 门户](https://portal.azure.com) → 你的 Foundry 项目 → <strong>概览</strong> → <strong>项目端点</strong>。

> **查找你的 MODEL_DEPLOYMENT_NAME：** 在 Foundry 侧边栏展开你的项目 → <strong>模型</strong> → 找到你已部署的模型名称（例如 `gpt-4.1-mini`）。

### 环境变量优先级

`main.py` 使用 `load_dotenv(override=False)`，意味着：

| 优先级 | 来源 | 两者均设置时哪个生效？ |
|----------|--------|------------------------|
| 1（最高） | Shell 环境变量 | 生效 |
| 2 | `.env` 文件 | 仅当 shell 变量未设置时生效 |

这意味着在托管部署期间，Foundry 运行时环境变量（通过 `agent.yaml` 设置）优先于 `.env` 文件值。

---

## 版本兼容性

### 包版本矩阵

多代理工作流需要特定包版本。版本不匹配会导致运行时错误。

| 包 | 需求版本 | 检查命令 |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | 最新预发布 | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### 常见版本错误

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修复：升级到rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` 未找到或检查器不兼容：**

```powershell
# 修复：使用 --pre 标志安装
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修复：升级 mcp 包
pip install mcp --upgrade
```

### 一次检查所有版本

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

预期输出：

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## MCP 工具问题

### MCP 工具无返回结果

**症状：** Gap 卡显示 “No results returned from Microsoft Learn MCP” 或 “No direct Microsoft Learn results found”。

**可能原因：**

1. <strong>网络问题</strong> - MCP 端点 (`https://learn.microsoft.com/api/mcp`) 不可达。  
   ```powershell
   # 测试连接性
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
  如果返回 `200`，说明端点可达。

2. <strong>查询过于具体</strong> - 技能名称对 Microsoft Learn 搜索来说过于细分。  
   - 对于非常专业的技能这是预期行为。工具响应中含有备用 URL。

3. **MCP 会话超时** - Streamable HTTP 连接超时。  
   - 重试该请求。MCP 会话是临时的，可能需要重新连接。

### MCP 日志说明

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| 日志 | 含义 | 操作 |
|-----|---------|--------|
| `GET → 405` | MCP 客户端初始化时探测 | 正常 - 忽略 |
| `POST → 200` | 工具调用成功 | 预期结果 |
| `DELETE → 405` | MCP 客户端清理时探测 | 正常 - 忽略 |
| `POST → 400` | 请求错误（查询格式错误） | 检查 `search_microsoft_learn_for_plan()` 中的 `query` 参数 |
| `POST → 429` | 速率限制 | 等待后重试。减少 `max_results` 参数 |
| `POST → 500` | MCP 服务器错误 | 临时错误 - 重试。若持续发生，Microsoft Learn MCP API 可能不可用 |
| 连接超时 | 网络问题或 MCP 服务器不可用 | 检查网络。尝试 `curl https://learn.microsoft.com/api/mcp` |

---

## 部署问题

### 容器部署后启动失败

1. **检查容器日志：**  
   - 打开 **Microsoft Foundry** 侧边栏 → 展开 **Hosted Agents (Preview)** → 点击你的代理 → 展开版本 → <strong>容器详情</strong> → <strong>日志</strong>。  
   - 查找 Python 堆栈跟踪或缺少模块错误。

2. **常见容器启动失败：**

   | 日志错误 | 原因 | 解决方法 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` 缺少依赖包 | 添加依赖，重新部署 |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` 中环境变量未设置 | 更新 `agent.yaml` → `environment_variables` 部分 |
   | `azure.identity.CredentialUnavailableError` | 未配置托管身份 | Foundry 自动设置 - 确保通过扩展部署 |
   | `OSError: port 8088 already in use` | Dockerfile 暴露端口错误或端口冲突 | 确认 Dockerfile 中 `EXPOSE 8088` 和 `CMD ["python", "main.py"]` 正确 |
   | 容器以代码 1 退出 | `main()` 中未捕获异常 | 本地先测试（[模块 5](05-test-locally.md)），捕获错误后再部署 |

3. **修复后重新部署：**  
   - 按 `Ctrl+Shift+P` → 选择 **Microsoft Foundry: Deploy Hosted Agent** → 选中同一代理 → 部署新版本。

### 部署时间过长

多代理容器启动时创建 4 个代理实例，启动时间更长。正常启动时间：

| 阶段 | 预估时长 |
|-------|------------------|
| 容器镜像构建 | 1-3 分钟 |
| 镜像推送到 ACR | 30-60 秒 |
| 容器启动（单代理） | 15-30 秒 |
| 容器启动（多代理） | 30-120 秒 |
| Playground 代理可用 | “Started” 后 1-2 分钟 |

> 如果“Pending”状态超过 5 分钟，检查容器日志是否有错误。

---

## RBAC 和权限问题

### `403 Forbidden` 或 `AuthorizationFailed`

你需要在 Foundry 项目中拥有 **[Azure AI User](https://aka.ms/foundry-ext-project-role)** 角色：

1. 访问 [Azure 门户](https://portal.azure.com) → 你的 Foundry <strong>项目</strong> 资源。  
2. 点击 **访问控制 (IAM)** → <strong>角色分配</strong>。  
3. 搜索你的用户名 → 确认是否包含 **Azure AI User**。  
4. 如缺失：点击 <strong>添加</strong> → <strong>添加角色分配</strong> → 搜索 **Azure AI User** → 分配给你的账户。

详情请参阅 [Microsoft Foundry 的 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 文档。

### 模型部署不可访问

若代理返回与模型相关错误：

1. 确认模型已部署：Foundry 侧边栏 → 展开项目 → <strong>模型</strong> → 查看 `gpt-4.1-mini`（或你的模型）状态为 **Succeeded**。  
2. 确认部署名称匹配：比较 `.env`（或 `agent.yaml`）中的 `MODEL_DEPLOYMENT_NAME` 与侧边栏中实际部署名。  
3. 若部署过期（免费层）：从[模型目录](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)重新部署（`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**）。

---

## 代理检查器问题

### 检查器打开却显示 “Disconnected”

1. 确认服务器已运行：终端出现 “Server running on http://localhost:8088”。  
2. 检查端口 `5679`：检查检查器通过 debugpy 连接此端口。  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. 重启服务器并重新打开检查器。

### 检查器显示部分响应

多代理响应内容较长，并以流式形式递增。请等待完整响应完成（根据 gap 卡数量及 MCP 工具调用，可能需 30-60 秒）。

如果响应持续被截断：  
- 确认 GapAnalyzer 指令中有 `CRITICAL:` 段阻止合并 gap 卡。  
- 检查模型令牌限制——`gpt-4.1-mini` 支持最高 32K 输出令牌，应足够。

---

## 性能提示

### 响应缓慢

多代理工作流本质上比单代理慢，因为存在顺序依赖和 MCP 工具调用。

| 优化 | 方法 | 影响 |
|-------------|-----|--------|
| 减少 MCP 调用 | 降低工具中 `max_results` 参数 | 减少 HTTP 往返次数 |
| 简化指令 | 提供更短、更聚焦的代理提示 | 加快 LLM 推理速度 |
| 使用 `gpt-4.1-mini` | 开发时比 `gpt-4.1` 快 | 约 2 倍速度提升 |
| 减少 gap 卡细节 | 在 GapAnalyzer 指令中简化 gap 卡格式 | 减少生成输出量 |

### 典型响应时间（本地）

| 配置 | 预期时间 |
|--------------|---------------|
| `gpt-4.1-mini`，3-5 张 gap 卡 | 30-60 秒 |
| `gpt-4.1-mini`，8 张以上 gap 卡 | 60-120 秒 |
| `gpt-4.1`，3-5 张 gap 卡 | 60-120 秒 |
---

## 获取帮助

如果尝试上述修复后仍然卡住：

1. <strong>检查服务器日志</strong> - 大多数错误会在终端生成一个 Python 堆栈跟踪。阅读完整的追踪信息。
2. <strong>搜索错误信息</strong> - 复制错误文本并在 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 中搜索。
3. <strong>提出问题</strong> - 在 [workshop 仓库](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 提交问题，附上：
   - 错误信息或截图
   - 你的包版本 (`pip list | Select-String "agent-framework"`)
   - 你的 Python 版本 (`python --version`)
   - 问题是本地的还是部署后的

---

### 检查点

- [ ] 你能够使用快速参考表识别并修复最常见的多代理错误
- [ ] 你知道如何检查和修复 `.env` 配置问题
- [ ] 你可以验证包版本是否符合要求的矩阵
- [ ] 你理解 MCP 日志条目并能够诊断工具故障
- [ ] 你知道如何检查容器日志以排查部署失败
- [ ] 你能够在 Azure 门户中验证 RBAC 角色

---

**上一步:** [07 - 在 Playground 中验证](07-verify-in-playground.md) · **主页:** [实验 02 README](../README.md) · [研讨会主页](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：  
本文档由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译而成。尽管我们努力确保准确性，但请注意，自动翻译可能包含错误或不准确之处。原始语言的文档应被视为权威来源。对于重要信息，建议采用专业人工翻译。我们不对因使用此翻译而产生的任何误解或误释承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->