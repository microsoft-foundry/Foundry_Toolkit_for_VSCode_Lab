# 模块 8 - 故障排除

本模块涵盖多代理工作流中特有的常见错误、修复方法和调试策略。

## 代理输出问题

### GapAnalyzer 提示“我仍然没有匹配报告”

**症状：** GapAnalyzer 响应要求你粘贴包含“缺失技能”和“认证差距”的匹配报告。即使你发送了简历和职位描述，也会出现这种情况。

**原因：** 职位描述文本未传递给 JD Agent。在 `context_mode="last_agent"` 模式下，`resume_executor` 是唯一能看到用户原始消息的执行器。如果 `RESUME_PARSER_INSTRUCTIONS` 的输出中不包含职位描述文本，JD Agent 就无法解析职位描述，MatchingAgent 无法计算匹配得分，GapAnalyzer 收到无效输入。

**诊断：**

在服务器日志中，查找 MatchingAgent 的跨度(span)。如果包含：
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
传递过程缺失或中断。

**修复：** 确认 `main.py` 中的 `RESUME_PARSER_INSTRUCTIONS` 包含 `[JOB DESCRIPTION PASS-THROUGH]` 部分及以下规则：
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
还要确认 `JOB_DESCRIPTION_INSTRUCTIONS` 中包含 `[PARSED RESUME PASS-THROUGH]` 传递规则：
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
如果任一指令块是脚手架向导的占位符，替换为 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 中的完整版本。

### MatchingAgent 输出“无法计算匹配分数 - 未提供职位描述”

这是上述相同的根本原因。MatchingAgent 收到了 JD Agent 的输出，但缺少或空的 `[PARSED RESUME PASS-THROUGH]` 部分，无法比较两个档案。确认：
1. `JOB_DESCRIPTION_INSTRUCTIONS` 包含传递规则：`Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` 告诉代理查找 `[JD REQUIREMENTS]` 和 `[PARSED RESUME PASS-THROUGH]` 部分。

用 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) 中的完整版本替换两个指令块。

### 响应出现两次

**症状：** GapAnalyzer 输出（或整个管道输出）在 Agent Inspector 响应中出现两次。

**原因：** `WorkflowBuilder` 对输入边使用“或”语义——只要<strong>任一</strong>前驱完成，下游执行器就触发。如果 `matching_executor` 有两个输入边（一条来自 `resume_executor`，一条来自 `jd_executor`），则它会触发两次：一次是 ResumeParser 完成时，一次是 JD Agent 完成时。GapAnalyzer 也会因此运行两次。

**修复：** 确保 `WorkflowBuilder` 图是严格的顺序管道，无汇合(fan-in)：

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # 不是来自resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

如果有多余的 `.add_edge(resume_executor, matching_executor)` 行，请删除它。JD Agent 输出中的 `[PARSED RESUME PASS-THROUGH]` 传递已经让 MatchingAgent 能访问简历。

---

## 环境和配置问题

### 缺失或错误的 `.env` 值

`.env` 文件必须位于 `PersonalCareerCopilot/` 目录下（与 `main.py` 同级）：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

预期的 `.env` 内容：

**路径 A - Foundry 云端：**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**路径 B - Foundry 本地：**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> 两个路径均使用 `FOUNDRY_PROJECT_ENDPOINT`。值不同：云端使用 `https://` Foundry 端点；本地使用 `http://localhost:5273/v1`。运行 `foundry model list` 确认路径 B 的具体模型别名。

> **查找你的 `FOUNDRY_PROJECT_ENDPOINT`:** 
- 打开 VS Code 中的 **Foundry Toolkit** 侧边栏 → 右键你的项目 → <strong>复制项目端点</strong>。 
- 或访问 [Azure 门户](https://portal.azure.com) → 你的 Foundry 项目 → <strong>概览</strong> → <strong>项目端点</strong>。

> **查找你的 `AZURE_AI_MODEL_DEPLOYMENT_NAME`:<strong> 在 Foundry Toolkit 侧边栏，展开你的项目 → </strong>模型** → 找到已部署的模型名称（如 `gpt-4.1-mini`）。

### 环境变量优先级

`main.py` 使用 `load_dotenv(override=True)`，意味着：

| 优先级 | 来源 | 同时设置时哪个生效？ |
|--------|-------|------------------------|
| 1（最高） | `.env` 文件 | 是 |
| 2 | Shell / 容器环境变量 | `.env` 无对应键时使用 |

在本地开发中，`.env` 是配置的权威来源（编辑 `.env` 立即影响运行）。在托管部署时，Foundry 在容器级注入环境变量；由于 `.env` 不包含在该实验室设置的部署镜像中，因此使用注入的容器变量。

---

## 版本兼容性

### 软件包版本矩阵

多代理工作流需要特定的软件包版本。不匹配会导致运行时错误。

| 软件包 | 需要版本 | 检查命令 |
|--------|----------|-----------|
| `agent-framework-foundry` | 最新版本 | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | 最新版本 | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | 最新版本 | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### 常见版本错误

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修复：重新安装 agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修复：升级 mcp 包
pip install mcp --upgrade
```

### 一次性验证所有版本

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

预期输出：

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## 部署问题

### 部署后容器启动失败

1. **检查容器日志：**
   - 打开 **Foundry Toolkit** 侧边栏 → 展开 **托管代理（预览）** → 点击你的代理 → 展开版本 → <strong>容器详情</strong> → <strong>日志</strong>。
   - 查找 Python 堆栈跟踪或缺失模块错误。

2. **常见容器启动失败原因：**

   | 日志中的错误 | 原因 | 解决方法 |
   |--------------|-------|---------|
   | `ModuleNotFoundError` | `requirements.txt` 缺少包 | 添加相应包，重新部署 |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` 或 `.env` 环境变量未设置 | 更新 `agent.yaml` → `environment_variables` 部分（托管）或 `.env`（本地） |
   | `azure.identity.CredentialUnavailableError` | 未配置托管身份 | Foundry 会自动设置 - 确保通过扩展部署 |
   | `OSError: port 8088 already in use` | Dockerfile暴露错误端口或端口冲突 | 验证 Dockerfile 中的 `EXPOSE 8088` 和命令 `CMD ["python", "main.py"]` |
   | 容器退出代码为 1 | `main()` 中未处理异常 | 本地测试先行（见[模块 5](05-test-locally.md)）以捕获错误 |

3. **修复后重新部署：**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → 选择相同代理 → 部署新版本。

### 部署时间过长

多代理容器启动时间更长，因为启动时创建了 4 个代理实例。正常启动时间：

| 阶段 | 预期时长 |
|-------|----------|
| 容器镜像构建 | 1-3 分钟 |
| 镜像推送到 ACR | 30-60 秒 |
| 容器启动（单代理） | 15-30 秒 |
| 容器启动（多代理） | 30-120 秒 |
| 代理在 Playground 可用 | “启动”后 1-2 分钟 |

> 如果“挂起”（Pending）状态持续超过 5 分钟，请检查容器日志是否有错误。

---

## RBAC 及权限问题

### `403 Forbidden` 或 `AuthorizationFailed`

你需要在 Foundry 项目中拥有 **[Foundry User](https://aka.ms/foundry-ext-project-role)** 角色（之前称为 **Azure AI User**，角色 ID 未变）：

1. 访问 [Azure 门户](https://portal.azure.com) → 你的 Foundry <strong>项目</strong> 资源。
2. 点击 **访问控制（IAM）** → <strong>角色分配</strong>。
3. 搜索你的姓名 → 确认列表中有 **Foundry User**（或旧标签 **Azure AI User**）。
4. 如果缺失：点击 <strong>添加</strong> → <strong>添加角色分配</strong> → 搜索 **Foundry User** → 分配给你的账户。

详情请参阅 [Microsoft Foundry 的 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 文档。

### 模型部署无法访问

如果代理返回模型相关错误：

1. 验证模型已部署：Foundry 侧边栏 → 展开项目 → <strong>模型</strong> → 检查 `gpt-4.1-mini`（或你的模型）状态为 <strong>成功</strong>。
2. 验证部署名称一致：比较 `.env`（或 `agent.yaml`）中的 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 与侧边栏中的实际部署名称。
3. 如果部署已过期（免费层）：从 [模型目录](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) 重新部署（`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**）。

---

## Foundry 本地问题（路径 B）

### Foundry 本地服务未运行

```powershell
# 检查状态
foundry local status

# 如果服务已停止，则启动服务
foundry local start
```

| 症状 | 原因 | 解决方法 |
|-------|-------|----------|
| 健康检查返回 `503` | 服务未启动 | 运行 `foundry local start` 或点击 Foundry Toolkit 侧边栏的 <strong>启动</strong> |
| 健康检查超时 | 模型仍在加载 | 启动后等待 30-60 秒；大型模型需更长时间 |
| `/v1/health` 返回 `StatusCode: 404` | 端口错误 | 默认是 `5273`。通过 `foundry local status` 查看实际端口 |
| 资源不足 | Foundry Local 需大约 4 GB 空闲内存 | 关闭其他应用 |
| 模型下载失败 | 磁盘空间不足 | 模型大小 2-8 GB。释放空间后执行 `foundry model pull <name>` |

### 模型名称不匹配

```powershell
# 列出已下载的模型及其准确的别名
foundry model list
```

在 `.env` 中将 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 设置为显示的准确别名（如 `phi-4-mini`，不要写成 `Phi-4-mini`）。

### 本地运行出现 `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'`（路径 B）

该实验的 `main.py` 使用 `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`。Foundry Local 要求此变量指向本地服务——<strong>而非</strong> `AZURE_AI_PROJECT_ENDPOINT`。确保你的 `.env` 包含：

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP 工具仍会发出外部调用（路径 B）

这是预期的。`search_microsoft_learn_for_plan` 工具从 `https://learn.microsoft.com/api/mcp` 获取学习资源。<strong>只有技能名称查询</strong>通过网络传输，简历和职位描述文本完全在你的设备上处理，绝不传输。如果需要完全离线操作，可在工具中添加 `try/except` 回退，当端点无法访问时返回一个静态的 `learn.microsoft.com` URL。

---

## 获取帮助

如果在尝试上述修复后仍卡住：

1. <strong>检查服务器日志</strong> - 大多数错误会在终端输出 Python 堆栈跟踪。认真阅读完整回溯。
2. <strong>搜索错误消息</strong> - 复制错误文本，在 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) 搜索。
3. <strong>提交问题</strong> - 在 [workshop 仓库](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) 中提交问题，包含：
   - 错误消息或截图
   - 软件版本（`pip list | Select-String "agent-framework"`）
   - Python 版本（`python --version`）
   - 问题发生在本地还是部署后

---

### 检查点

- [ ] 你知道如何检查和修复 `.env` 配置问题
- [ ] 你能验证软件包版本是否符合要求矩阵
- [ ] 你知道如何查看容器日志来诊断部署失败
- [ ] 你能在 Azure 门户验证 RBAC 角色

---

**上一篇：** [07 - Playground 验证](07-verify-in-playground.md) · **下一篇：** [09 - 总结 →](09-summary.md) · **首页：** [实验室 02 说明](../README.md) · [工作坊首页](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->