# Module 5 - Deploy to Foundry Agent Service

⏱️ ~10 min

> ⚠️ **Path B users:** Dis module need Foundry subscription. If you dey use Foundry Local, waka go [Module 07 - Summary](07-summary.md). You don finish local development workflow well well!

For dis module, you go deploy your locally-tested agent go Microsoft Foundry as **Hosted Agent**. The deployment go build container image, push am go Azure Container Registry, den start the agent for Foundry managed infrastructure.

### Deployment pipeline

```mermaid
flowchart LR
    A["Dockerfile
    main.py"] -->|docker build| B["Container
    Image"]
    B -->|docker push| C["Azure Container
    Registry (ACR)"]
    C -->|register agent| D["Foundry Agent
    Service"]
    D -->|start container| E["/responses
    endpoint ready"]

    style A fill:#9B59B6,color:#fff
    style B fill:#9B59B6,color:#fff
    style C fill:#E67E22,color:#fff
    style D fill:#3498DB,color:#fff
    style E fill:#27AE60,color:#fff
```

---

## Prerequisites check

Before you deploy, make sure:

- [ ] Agent pass all 3 local scenarios from [Module 04](04-test-locally.md)
- [ ] You get the **Azure AI User** role for project level ([Module 01, Assign RBAC](01-setup.md#deploy-a-model--assign-rbac))
- [ ] You don sign inside Azure for VS Code (Accounts icon go show your name)

---

## Step 1: Start the deployment

### Option A: Deploy from Agent Inspector (we recommend dis)

If the Agent Inspector dey open (from testing):
1. Click the **Deploy** button for top-right corner (cloud icon ↑).

### Option B: Deploy from Command Palette

1. Press `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent**.

---

## Step 2: Configure the deployment

The wizard go ask you for:

![Project Config](../../../../../translated_images/pcm/05-foundry-project-setup.ca6ad16a6484e054.webp)

| Prompt | Selection |
|--------|-----------|
| **Subscription** | Your Azure Subscription |
| **Target project** | Your Foundry project (like `workshop-agents`) |

Click **next** to configure your agent.

![Basics config](../../../../../translated_images/pcm/05-configure-basics.4d5f3d6b0d96f033.webp)

| Prompt | Selection |
|--------|-----------|
| **Deployment Method** | Container |
| **Container registry** | **Default ACR** (Microsoft Foundry dey create and manage one for you) |
| **Deploy to** | New Agent (name, `executive-summary-agent`) |

Click **next** make you fit review and deploy your agent.

![Review and deploy](../../../../../translated_images/pcm/05-review-deploy.12b449d426bff886.webp)

| Prompt | Selection |
|--------|-----------|
| **CPU and memory** | **0.5 CPU cores, 1.0 Gi memory** (na the default - e dey enough for workshop) |

---

## Step 3: Deploy and monitor

1. Click **Deploy**.
2. Watch the **Output** panel (choose **Microsoft Foundry** from dropdown).
3. The deployment go follow dis stages:
   - **Docker build** - e go build container from your Dockerfile
   - **Docker push** - e go push image to ACR (e fit take 1–3 min first time)
   - **Agent registration** - e go create hosted agent for Foundry
   - **Container start** - e go start with system-managed identity

4. When e finish, notification go show:
   > **executive-summary-agent don deploy successful.** `View logs` `Run agent`

5. Click **Run agent** to open the Agent Playground.

![Deployment success showing Agent Playground with Running status](../../../../../translated_images/pcm/05-deployed-asset.b59e6a5eef31c0b1.webp)

### Deployment status values

| Status | Meaning |
|--------|---------|
| **Running** | Container don ready, agent dey respond |
| **Pending** | Container dey start - wait 30–60 seconds |
| **Failed** | Check logs (see troubleshooting below) |

---

## Common deployment errors

| Error | Root cause | Fix |
|-------|-----------|-----|
| `agents/write` permission denied | You no get **Azure AI User** role for project level | [Module 01, Assign RBAC](01-setup.md#deploy-a-model--assign-rbac) |
| Docker no dey run | Docker Desktop neva start | Start Docker Desktop → check `docker info` |
| ACR authorization | Managed identity no fit pull image | See [Module 08 - Troubleshooting](08-troubleshooting.md) |

---

### ✅ Checkpoint

- [ ] Deployment don complete without errors
- [ ] Agent show for the **Hosted Agent** tab wen you click **Agents** under your project for Foundry Toolkit sidebar
- [ ] Container status show **Running**
- [ ] Agent Playground tab open show agent details and endpoint URL

---

**Previous:** [04 - Test Locally](04-test-locally.md) · **Next:** [06 - Verify in Playground →](06-verify-in-playground.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document don translate wit AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator). Even tho we dey try make am correct, abeg make you know say automated translation fit get errors or mistakes. Di original document for dia own language na im be di correct source. For important info, make person wey sabi human translation do am. We no go responsible for any misunderstanding or wrong understanding wey fit happen because of dis translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->