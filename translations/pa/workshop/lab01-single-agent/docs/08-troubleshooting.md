# Module 8 - ਸਮੱਸਿਆ ਮੁਕਾਬਲਾ

ਇਹ ਮਾਡਿਊਲ ਵਰਕਸ਼ਾਪ ਦੌਰਾਨ ਆਏ ਹਰ ਆਮ ਮੁੱਦੇ ਲਈ ਰੇਫਰੈਂਸ ਮਾਰਗਦਰਸ਼ਿਕ ਹੈ। ਇਸਨੂੰ ਬੁੱਕਮਾਰਕ ਕਰੋ - ਤੁਸੀਂ ਇਸ ਨੂੰ ਕਿਸੇ ਵੀ ਸਮੇਂ ਗਲਤ ਹੋਣ 'ਤੇ ਵਾਪਸ ਆਓਗੇ।

---

## 1. ਅਧਿਕਾਰ ਗਲਤੀਆਂ

### 1.1 `agents/write` ਅਧਿਕਾਰ ਨਾਹ ਮਿਲੇ

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**ਮੂਲ ਕਾਰਨ:** ਤੁਹਾਡੇ ਕੋਲ **ਪ੍ਰੋਜੈਕਟ** ਪੱਧਰ 'ਤੇ `Azure AI User` ਭੂਮਿਕਾ ਨਹੀਂ ਹੈ। ਇਹ ਵਰਕਸ਼ਾਪ ਵਿੱਚ ਸਭ ਤੋਂ ਆਮ ਗਲਤੀ ਹੈ।

**ਸੁਧਾਰ - ਕਦਮ ਦਰ ਕਦਮ:**

1. [https://portal.azure.com](https://portal.azure.com) ਖੋਲ੍ਹੋ।
2. ਉੱਪਰਲੇ ਖੋਜ ਵਾਲੇ ਬਾਰ ਵਿੱਚ ਆਪਣੀ **Foundry ਪ੍ਰੋਜੈਕਟ** ਦਾ ਨਾਮ ਲਿਖੋ (ਉਦਾਹਰਨ: `workshop-agents`)।
3. **ਮਹੱਤਵਪੂਰਨ:** ਉਸ ਨਤੀਜੇ 'ਤੇ ਕਲਿਕ ਕਰੋ ਜੋ ਕਿਸਮ **"Microsoft Foundry project"** ਹੋਵੇ, ਮਾਪੇ ਖਾਤਾ/ਹਬ ਸਰੋਤ ਨਹੀਂ। ਇਹ ਵੱਖ-ਵੱਖ ਸਰੋਤ ਹਨ ਜਿਨ੍ਹਾਂ ਦੇ ਵੱਖ-ਵੱਖ RBAC ਸਕੋਪ ਹਨ।
4. ਪ੍ਰੋਜੈਕਟ ਪੰਨੇ ਦੀ ਖੱਬੇ ਪਾਸੇ ਨੈਵੀਗੇਸ਼ਨ ਵਿੱਚ **Access control (IAM)** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
5. ਦੇਖੋ ਕਿ ਤੁਹਾਡੇ ਕੋਲ ਭੂਮਿਕਾ ਹੈ ਜਾਂ ਨਹੀਂ, ਇਸ ਲਈ **Role assignments** ਟੈਬ ‘ਤੇ ਕਲਿਕ ਕਰੋ:
   - ਆਪਣਾ ਨਾਮ ਜਾਂ ਇਮੇਲ ਖੋਜੋ।
   - ਜੇ `Azure AI User` ਪਹਿਲਾਂ ਤੋਂ ਸੂਚੀਬੱਧ ਹੈ → ਗਲਤੀ ਦਾ ਕਾਰਨ ਵੱਖਰਾ ਹੈ (ਹੇਠਾਂ ਕਦਮ 8 ਵੇਖੋ)।
   - ਜੇ ਸੂਚੀ ਵਿੱਚ ਨਹੀਂ → ਇਸਨੂੰ ਸ਼ਾਮਲ ਕਰਨ ਲਈ ਅੱਗੇ ਵਧੋ।
6. **+ Add** → **Add role assignment** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
7. **Role** ਟੈਬ ਵਿੱਚ:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) ਖੋਜੋ।
   - ਨਤੀਜਿਆਂ ਵਿੱਚੋਂ ਚੁਣੋ।
   - **Next** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
8. **Members** ਟੈਬ ਵਿੱਚ:
   - **User, group, or service principal** ਚੁਣੋ।
   - **+ Select members** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
   - ਆਪਣਾ ਨਾਮ ਜਾਂ ਈਮੇਲ ਖੋਜੋ।
   - ਨਤੀਜਿਆਂ ਵਿੱਚੋਂ ਆਪਣੇ ਆਪ ਨੂੰ ਚੁਣੋ।
   - **Select** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
9. **Review + assign** → ਫਿਰ **Review + assign** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
10. **1-2 ਮਿੰਟ ਦੀ ਉਡੀਕ ਕਰੋ** - RBAC ਤਬਦੀਲੀਆਂ ਨੂੰ ਫੈਲਣ ਲਈ ਸਮਾਂ ਲੱਗਦਾ ਹੈ।
11. ਫੇਰ ਓਹ ਕੰਮ ਦੁਹਰਾਉ ਜੋ ਅਸਫਲ ਹੋਇਆ ਸੀ।

> **ਮਾਲਕ/ਭਾਗੀਦਾਰ ਕਿਉਂ ਕਾਫ਼ੀ ਨਹੀਂ ਹਨ:** Azure RBAC ਦੇ ਦੋ ਤਰ੍ਹਾਂ ਦੇ ਅਧਿਕਾਰ ਹਨ - *ਮੇਨੇਜਮੈਂਟ ਐਕਸ਼ਨਜ਼* ਅਤੇ *ਡਾਟਾ ਐਕਸ਼ਨਜ਼*। ਮਾਲਕ ਅਤੇ ਭਾਗੀਦਾਰ ਮੇਨੇਜਮੈਂਟ ਐਕਸ਼ਨ (ਸਰੋਤ ਬਣਾਉਣਾ, ਸੈਟਿੰਗਸ ਸੋਧਣਾ) ਦਿੰਦੇ ਹਨ, ਪਰ ਏਜੰਟ ਕਾਰਜਾਂ ਨੂੰ `agents/write` **ਡਾਟਾ ਐਕਸ਼ਨ** ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ, ਜੋ ਸਿਰਫ `Azure AI User`, `Azure AI Developer`, ਜਾਂ `Azure AI Owner` ਭੂਮਿਕਾਵਾਂ ਵਿੱਚ ਹੁੰਦੀ ਹੈ। ਵੇਖੋ [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)।

### 1.2 ਸਰੋਤ ਪ੍ਰਦਾਨ ਕਰਦੇ ਸਮੇਂ `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**ਮੂਲ ਕਾਰਨ:** ਤੁਹਾਡੇ ਕੋਲ ਇਸ ਸਬਸਕ੍ਰਿਪਸ਼ਨ/ਸਰੋਤ ਗਰੁੱਪ ਵਿੱਚ Azure ਸਰੋਤ ਬਣਾਉਣ ਜਾਂ ਸੋਧਣ ਦਾ ਅਧਿਕਾਰ ਨਹੀਂ ਹੈ।

**ਸੁਧਾਰ:**
1. ਆਪਣੇ ਸਬਸਕ੍ਰਿਪਸ਼ਨ ਪ੍ਰਸ਼ਾਸਕ ਨੂੰ ਅਪੀਲ ਕਰੋ ਕਿ ਉਹ ਤੁਹਾਨੂੰ ਸਰੋਤ ਗਰੁੱਪ 'ਤੇ **Contributor** ਭੂਮਿਕਾ ਦੇਵੇ ਜਿਥੇ ਤੁਹਾਡਾ Foundry ਪ੍ਰੋਜੈਕਟ ਹੈ।
2. ਬਦਲੀ ਵਜੋਂ, ਉਹ ਤੁਹਾਡੇ ਲਈ Foundry ਪ੍ਰੋਜੈਕਟ ਬਣਾਉਂ ਅਤੇ ਤੁਹਾਨੂੰ ਪ੍ਰੋਜੈਕਟ 'ਤੇ **Azure AI User** ਅਧਿਕਾਰ ਦੇਵੇ।

### 1.3 `[SubscriptionNotRegistered]` Microsoft.CognitiveServices ਲਈ

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**ਮੂਲ ਕਾਰਨ:** Azure ਸਬਸਕ੍ਰਿਪਸ਼ਨ ਨੇ Foundry ਲਈ ਜ਼ਰੂਰੀ ਸਰੋਤ ਪ੍ਰਦਾਤਾ ਨੂੰ ਰਜਿਸਟਰ ਨਹੀਂ ਕੀਤਾ।

**ਸੁਧਾਰ:**

1. ਟਰਮੀਨਲ ਖੋਲ੍ਹ ਕੇ ਚਲਾਓ:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਮੁਕੰਮਲ ਹੋਣ ਦੀ ਉਡੀਕ ਕਰੋ (1-5 ਮਿੰਟ ਲੱਗ ਸਕਦੇ ਹਨ):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   ਉਮੀਦ ਕੀਤੀ ਗਈ ਨਤੀਜਾ: `"Registered"`
3. ਆਪਣਾ ਕੰਮ ਦੁਹਰਾਓ।

---

## 2. Docker ਗਲਤੀਆਂ (ਸਿਰਫ ਜੇ Docker ਸਥਾਪਿਤ ਹੈ)

> Docker ਇਸ ਵਰਕਸ਼ਾਪ ਲਈ **ਵਿਕਲਪਿਕ** ਹੈ। ਇਹ ਗਲਤੀਆਂ ਸਿਰਫ ਉਸ ਵੇਲੇ ਲਾਗੂ ਹੁੰਦੀਆਂ ਹਨ ਜਦੋਂ ਤੁਹਾਡੇ ਕੋਲ Docker ਡੈੱਸਕਟਾਪ ਇੰਸਟਾਲ ਹੈ ਅਤੇ Foundry ਐਕਸਟੈਨਸ਼ਨ ਲੋਕਲ ਕન્ટੇਨਰ ਬਿਲਡ ਕਰਨ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰਦਾ ਹੈ।

### 2.1 Docker daemon ਚਲ ਰਿਹਾ ਨਹੀਂ

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**ਸੁਧਾਰ - ਕਦਮ ਦਰ ਕਦਮ:**

1. ਆਪਣੇ ਸਟਾਰਟ ਮੀਨੂ (Windows) ਜਾਂ ਐਪਲੀਕੇਸ਼ਨ (macOS) ਵਿੱਚ **Docker Desktop** ਲੱਭੋ ਅਤੇ ਚਲਾਓ।
2. Docker Desktop ਵਿੰਡੋ ਵਿੱਚ **"Docker Desktop is running"** ਦੇਖਣ ਲਈ ਉਡੀਕ ਕਰੋ - ਆਮ ਤੌਰ ’ਤੇ 30-60 ਸਕਿੰਟ ਲੱਗਦੇ ਹਨ।
3. ਆਪਣੇ ਸਿਸਟਮ ਟਰੇ (Windows) ਜਾਂ ਮੇਨੂ ਬਾਰ (macOS) ਵਿੱਚ Docker ਵਿਹੀਕਲ ਚਿੰਨ੍ਹ ਜਾਂ ਇਸਤੇਮਾਲ ਹਾਲਤ ਦੇਖੋ। ਹੋਵਰ ਕਰਕੇ ਕੀ ਸਥਿਤੀ ਹੈ ਪੱਕਾ ਕਰੋ।
4. ਟਰਮੀਨਲ ਵਿੱਚ ਇਹ ਚਕ ਕਰੋ:
   ```powershell
   docker info
   ```
   ਜੇ ਇਹ Docker ਸਿਸਟਮ ਜਾਣਕਾਰੀ (Server Version, Storage Driver ਆਦਿ) ਛਾਪਦਾ ਹੈ, ਤਾਂ Docker ਚੱਲ ਰਿਹਾ ਹੈ।
5. **Windows ਲਈ ਖ਼ਾਸ:** ਜੇ Docker ਫਿਰ ਵੀ ਸ਼ੁਰੂ ਨਹੀਂ ਹੁੰਦਾ:
   - Docker Desktop → **Settings** (ਗੀਅਰ ਆਈਕਨ) → **General** ਖੋਲ੍ਹੋ।
   - ਯਕੀਨੀ ਬਣਾਓ ਕਿ **Use the WSL 2 based engine** ਚੈਕ ਹੈ।
   - **Apply & restart** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
   - ਜੇ WSL 2 ਇੰਸਟਾਲ ਨਹੀਂ ਹੈ, ਤਾਂ ਉੱਚਤ ਸਤਹ ਪਾਵਰਸ਼ੈਲ ਵਿਚ `wsl --install` ਚਲਾਓ ਅਤੇ ਕੰਪਿਊਟਰ ਨੂੰ ਪੂਨਰਾਰੰਭ ਕਰੋ।
6. ਤਬਦੀਲੀ ਦੁਬਾਰਾ ਕਰਕੇ ਕੋਸ਼ਿਸ਼ ਕਰੋ।

### 2.2 Docker ਬਿਲਡ ਡਿਪੈਂਡੈਂਸੀ ਗਲਤੀਆਂ ਨਾਲ ਅਸਫਲ

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**ਸੁਧਾਰ:**
1. `requirements.txt` ਖੋਲ੍ਹੋ ਅਤੇ ਸਾਰੇ ਪੈਕੇਜਾਂ ਦੇ ਨਾਮ ਠੀਕ ਹਨ ਜਾਂ ਨਹੀਂ ਜਾਂਚੋ।
2. ਸੰਸਕਰਣ ਜੁੜਾਈ ਸਹੀ ਹੈ ਇਹ ਯਕੀਨੀ ਬਣਾਓ:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. ਪਹਿਲਾਂ ਸਥਾਨਕ ਤੌਰ ‘ਤੇ ਇੰਸਟਾਲ ਦੀ ਜਾਂਚ ਕਰੋ:
   ```bash
   pip install -r requirements.txt
   ```
4. ਜੇ ਪ੍ਰਾਈਵੇਟ ਪੈਕੇਜ ਇੰਡੈਕਸ ਦੀ ਵਰਤੋਂ ਕਰ ਰਹੇ ਹੋ, ਤਾਂ ਯਕੀਨੀ ਬਣਾਓ ਕਿ Docker ਨੂੰ ਇਹਨੂੰ ਐਕਸੈੱਸ ਕਰਨ ਲਈ ਨੈਟਵਰਕ ਹੈ।

### 2.3 ਕਨਟੇਨਰ ਪਲੇਟਫਾਰਮ ਅਸਮਰੱਥਾ (Apple Silicon)

ਜੇ ਤੁਸੀਂ Apple Silicon Mac (M1/M2/M3/M4) ਤੋਂ ਤੈਨਾਤ ਕਰ ਰਹੇ ਹੋ, ਤਾਂ ਕਨਟੇਨਰ ਨੂੰ `linux/amd64` ਲਈ ਬਣਾਇਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ ਕਿਉਂਕਿ Foundry ਦਾ ਕਨਟੇਨਰ ਰਨਟਾਈਮ AMD64 ਵਰਤਦਾ ਹੈ।

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry ਐਕਸਟੈਨਸ਼ਨ ਦਾ deploy ਕਮਾਂਡ ਜਿਆਦਾਤਰ ਕੇਸਾਂ ਵਿੱਚ ਇਸਨੂੰ ਆਪਣਾ ਆਪ ਸੰਭਾਲਦਾ ਹੈ। ਜੇ ਤੁਹਾਨੂੰ ਆਰਕੀਟੈਕਚਰ ਸੰਬੰਧੀ ਗਲਤੀਆਂ ਮਿਲਦੀਆਂ ਹਨ, ਤਾਂ `--platform` ਫਲੈਗ ਨਾਲ ਹੱਥੋਂ ਬਿਲਡ ਕਰੋ ਅਤੇ Foundry ਟੀਮ ਨਾਲ ਸੰਪਰਕ ਕਰੋ।

---

## 3. ਪ੍ਰਮਾਣਿਕਤਾ ਗਲਤੀਆਂ

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ਟੋਕਨ ਪ੍ਰਾਪਤ ਕਰਨ ਵਿੱਚ ਅਸਫਲ

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**ਮੂਲ ਕਾਰਨ:** `DefaultAzureCredential` ਚੇਨ ਵਿੱਚ ਕੋਈ ਵੀ ਪ੍ਰਮਾਣਿਕਤਾ ਸਰੋਤ ਮਾਨਯ ਟੋਕਨ ਨਹੀਂ ਰੱਖਦਾ।

**ਸੁਧਾਰ - ਕਦਮ ਕਦਮ ਨਾਲ ਕੋਸ਼ਿਸ਼ ਕਰੋ:**

1. **Azure CLI ਰਾਹੀਂ ਦੁਬਾਰਾ ਲੌਗਇਨ ਕਰੋ** (ਅਕਸਰ ਸਭ ਤੋਂ ਆਮ ਸੁਧਾਰ):
   ```bash
   az login
   ```
   ਇੱਕ ਬ੍ਰਾузਰ ਵਿੰਡੋ ਖੁਲਦੀ ਹੈ। ਸਾਈਨ ਇਨ ਕਰੋ, ਫਿਰ VS Code 'ਤੇ ਵਾਪਸ ਜਾਓ।

2. **ਸਹੀ ਸਬਸਕ੍ਰਿਪਸ਼ਨ ਸੈੱਟ ਕਰੋ:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   ਜੇ ਇਹ ਸਹੀ ਸਬਸਕ੍ਰਿਪਸ਼ਨ ਨਹੀਂ ਹੈ:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code ਰਾਹੀਂ ਦੁਬਾਰਾ ਲੌਗਇਨ:**
   - VS Code ਦੇ ਨੀਵੇਂ ਖੱਬੇ ਵਿੱਚ **Accounts** ਆਈਕਨ (ਵਿਅਕਤੀ ਆਈਕਨ) ‘ਤੇ ਕਲਿਕ ਕਰੋ।
   - ਆਪਣੇ ਖਾਤੇ ਦੇ ਨਾਮ 'ਤੇ ਕਲਿਕ ਕਰੋ → **Sign Out**।
   - ਫਿਰ ਦੁਬਾਰਾ Accounts ਆਈਕਨ ‘ਤੇ ਕਲਿਕ ਕਰੋ → **Sign in to Microsoft**।
   - ਬ੍ਰਾузਰ ਸਾਈਨ-ਇਨ ਪ੍ਰਕਿਰਿਆ ਪੂਰੀ ਕਰੋ।

4. **ਸੇਵਾ ਪ੍ਰਧਾਨ (ਕੇਵਲ CI/CD ਸਥਿਤੀਆਂ):**
   - ਆਪਣੇ `.env` ਵਿੱਚ ਇਹ ਵਾਤਾਵਰਣ ਵੈਰੀਏਬਲ ਸੈੱਟ ਕਰੋ:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - ਫਿਰ ਆਪਣੇ ਏਜੰਟ ਪ੍ਰਕਿਰਿਆ ਨੂੰ ਰੀਸਟਾਰਟ ਕਰੋ।

5. **ਟੋਕਨ ਕੈਸ਼ ਨੂੰ ਚੈੱਕ ਕਰੋ:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   ਜੇ ਇਹ ਫੇਲ ਹੁੰਦਾ ਹੈ, ਤਾਂ ਤੁਹਾਡਾ CLI ਟੋਕਨ ਸਮਾਪਤ ਹੋ ਚੁਕਾ ਹੈ। `az login` ਫਿਰ ਚਲਾਓ।

### 3.2 ਟੋਕਨ ਸਥਾਨਕ ਵਰਤੋਂ ਵਿੱਚ ਸਹੀ ਹੈ ਪਰ ਹੋਸਟ ਕੀਤੇ ਡਿਪਲੋਇਮੈਂਟ ਵਿੱਚ ਨਹੀਂ

**ਮੂਲ ਕਾਰਨ:** ਹੋਸਟ ਕੀਤੇ ਏਜੰਟ ਨੇ ਸਿਸਟਮ-ਮੈਨੇਜਡ ਆਈਡੈਂਟਿਟੀ ਵਰਤੀ ਹੈ, ਜੋ ਤੁਹਾਡੇ ਨਿੱਜੀ ਪ੍ਰਮਾਣ ਪੱਤਰ ਤੋਂ ਵੱਖ-ਵੱਖ ਹੈ।

**ਸੁਧਾਰ:** ਇਹ ਉਮੀਦਵਾਰ ਵਿਹਾਰ ਹੈ - ਮੈਨੇਜਡ ਆਈਡੈਂਟਿਟੀ ਆਟੋਮੈਟਿਕ ਤੌਰ 'ਤੇ ਡਿਪਲੋਇਮੈਂਟ ਦੌਰਾਨ ਬਣਾਈ ਜਾਂਦੀ ਹੈ। ਜੇ ਹੋਸਟ ਕੀਤੇ ਏਜੰਟ ਨੂੰ ਫਿਰ ਵੀ ਪ੍ਰਮਾਣੀਕਰਨ ਗਲਤੀਆਂ ਮਿਲਦੀਆਂ ਹਨ:
1. ਜਾਂਚੋ ਕਿ Foundry ਪ੍ਰੋਜੈਕਟ ਦੀ ਮੈਨੇਜਡ ਆਈਡੈਂਟਿਟੀ Azure OpenAI ਸਰੋਤ ਤੱਕ ਪਹੁੰਚ ਰੱਖਦੀ ਹੈ।
2. `PROJECT_ENDPOINT` ਨੂੰ `agent.yaml` ਵਿੱਚ ਸਹੀ ਰੱਖੋ।

---

## 4. ਮਾਡਲ ਗਲਤੀਆਂ

### 4.1 ਮਾਡਲ ਡਿਪਲੋਇਮੈਂਟ ਨਹੀਂ ਮਿਲਿਆ

```
Error: Model deployment not found / The specified deployment does not exist
```

**ਸੁਧਾਰ - ਕਦਮ ਦਰ ਕਦਮ:**

1. ਆਪਣੀ `.env` ਫਾਈਲ ਖੋਲ੍ਹੋ ਅਤੇ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ਦਾ ਮੁੱਲ ਨੋਟ ਕਰੋ।
2. VS Code 'ਚ **Microsoft Foundry** ਸਾਈਡਬਾਰ ਖੋਲ੍ਹੋ।
3. ਆਪਣਾ ਪ੍ਰੋਜੈਕਟ ਵਧਾਓ → **Model Deployments**।
4. ਉਥੇ ਲਿਖੇ ਡਿਪਲੋਇਮੈਂਟ ਨਾਮ ਨੂੰ ਆਪਣੇ `.env` ਮੁੱਲ ਨਾਲ ਤੁਲਨਾ ਕਰੋ।
5. ਨਾਮ **ਕੇਸ-ਸੰਵੇਦਨਸ਼ੀਲ** ਹੁੰਦਾ ਹੈ - `gpt-4o` ਅਤੇ `GPT-4o` ਵੱਖ-ਵੱਖ ਹਨ।
6. ਜੇ ਇਹ ਮੇਲ ਨਹੀਂ ਖਾਂਦੇ, ਆਪਣੀ `.env` ਫਾਈਲ ਨੂੰ ਬਿਲਕੁਲ ਸਹੀ ਨਾਮ ਨਾਲ ਅਪਡੇਟ ਕਰੋ ਜੋ ਸਾਈਡਬਾਰ 'ਚ ਹੈ।
7. ਹੋਸਟ ਕੀਤੇ ਡਿਪਲੋਇਮੈਂਟ ਲਈ, `agent.yaml` ਵੀ ਅਪਡੇਟ ਕਰੋ:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 ਮਾਡਲ ਅਣਅਪੇक्षित ਸਮੱਗਰੀ ਨਾਲ ਜਵਾਬ ਦਿੰਦਾ ਹੈ

**ਸੁਧਾਰ:**
1. `main.py` ਵਿੱਚ `EXECUTIVE_AGENT_INSTRUCTIONS` ਸਥਿਰਾਂ ਨੂੰ ਜ਼ਰੂਰ ਮਿਸ਼ਰ ਵਿੱਚ ਜਾਂ ਕਰਪਟ ਨਹੀਂ ਹੋਇਆ ਹੈ ਜਾਂ ਨਹੀਂ।
2. ਮਾਡਲ ਤਾਪਮਾਨ ਸੈਟਿੰਗ (ਜੇ ਸੰਰਚਿਤ ਹੈ) ਜਾਂਚੋ - ਘੱਟ ਮੁੱਲ ਹੋਰ ਨਿਰਧਾਰਤ ਜਵਾਬ ਦਿੰਦੇ ਹਨ।
3. ਡਿਪਲੋਇਮੈਂਟ ਮਾਡਲ ਦੀ ਤੁਲਨਾ ਕਰੋ (ਜਿਵੇਂ ਕਿ `gpt-4o` ਅਤੇ `gpt-4o-mini`) - ਵੱਖ-ਵੱਖ ਮਾਡਲਾਂ ਦੀਆਂ ਵੱਖਰੀਆਂ ਸਮਰੱਥਾਵਾਂ ਹੁੰਦੀਆਂ ਹਨ।

---

## 5. ਡਿਪਲੋਇਮੈਂਟ ਗਲਤੀਆਂ

### 5.1 ACR ਪੱਲ ਅਧਿਕਾਰ

```
Error: AcrPullUnauthorized
```

**ਮੂਲ ਕਾਰਨ:** Foundry ਪ੍ਰੋਜੈਕਟ ਦੀ ਮੈਨੇਜਡ ਆਈਡੈਂਟਿਟੀ Azure Container Registry ਵਿੱਚੋਂ ਕਨਟੇਨਰ ਚਿੱਤਰ ਖਿੱਚਣ ਲਈ ਅਧਿਕਾਰ ਨਹੀਂ ਰੱਖਦੀ।

**ਸੁਧਾਰ - ਕਦਮ ਦਰ ਕਦਮ:**

1. [https://portal.azure.com](https://portal.azure.com) ਖੋਲ੍ਹੋ।
2. ਉੱਪਰਲੇ ਖੋਜ ਵਾਲੇ ਬਾਰ ਵਿੱਚ **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** ਖੋਜੋ।
3. ਉਸ ਰਜਿਸਟਰੀ 'ਤੇ ਕਲਿਕ ਕਰੋ ਜੋ ਤੁਹਾਡੇ Foundry ਪ੍ਰੋਜੈਕਟ ਨਾਲ ਸੰਬੰਧਿਤ ਹੈ (ਆਮ ਤੌਰ 'ਤੇ ਉਹੀ ਸਰੋਤ ਗਰੁੱਪ ਵਿੱਚ ਹੁੰਦੀ ਹੈ)।
4. ਖੱਬੀ ਨੈਵੀਗੇਸ਼ਨ ਵਿਚ **Access control (IAM)** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
5. **+ Add** → **Add role assignment** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** ਖੋਜੋ ਅਤੇ ਚੁਣੋ। **Next** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
7. **Managed identity** ਚੁਣੋ → **+ Select members** ‘ਤੇ ਕਲਿਕ ਕਰੋ।
8. Foundry ਪ੍ਰੋਜੈਕਟ ਦੀ ਮੈਨੇਜਡ ਆਈਡੈਂਟਿਟੀ ਲੱਭੋ ਅਤੇ ਚੁਣੋ।
9. **Select** → **Review + assign** → **Review + assign** ‘ਤੇ ਕਲਿਕ ਕਰੋ।

> ਇਹ ਭੂਮਿਕਾ ਨਿਰਧਾਰਨ ਆਮ ਤੌਰ ‘ਤੇ Foundry ਐਕਸਟੈਨਸ਼ਨ ਵੱਲੋਂ ਆਟੋਮੈਟਿਕ ਤੌਰ ‘ਤੇ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। ਜੇ ਤੁਹਾਨੂੰ ਇਹ ਗਲਤੀ ਮਿਲਦੀ ਹੈ, ਤਾਂ ਆਟੋਮੈਟਿਕ ਸੈੱਟਅਪ ਅਸਫਲ ਹੋਇਆ ਹੋ ਸਕਦਾ ਹੈ। ਤੁਸੀਂ ਐਕਸਟੈਨਸ਼ਨ ਦੁਬਾਰਾ ਸੈੱਟਅਪ ਕਰਨ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰ ਸਕਦੇ ਹੋ।

### 5.2 ਡਿਪਲੋਇਮੈਂਟ ਤੋਂ ਬਾਅਦ ਏਜੰਟ ਸ਼ੁਰੂ ਨਹੀਂ ਹੁੰਦਾ

**ਲੱਛਣ:** ਕਨਟੇਨਰ ਸਥਿਤੀ 5 ਮਿੰਟ ਤੋਂ ਜ਼ਿਆਦਾ ਸਮੇਂ "Pending" ਰਹਿੰਦੀ ਹੈ ਜਾਂ "Failed" ਦਿਖਾਉਂਦੀ ਹੈ।

**ਸੁਧਾਰ - ਕਦਮ ਦਰ ਕਦਮ:**

1. VS Code ਵਿੱਚ **Microsoft Foundry** ਸਾਈਡਬਾਰ ਖੋਲ੍ਹੋ।
2. ਆਪਣੇ ਹੋਸਟ ਕੀਤੇ ਏਜੰਟ 'ਤੇ ਕਲਿਕ ਕਰੋ → ਵਰਜਨ ਚੁਣੋ।
3. ਵਿਸਥਾਰ ਪੈਨਲ ਵਿੱਚ **Container Details** ਦੇਖੋ → **Logs** ਸੈਕਸ਼ਨ ਜਾਂ ਲਿੰਕ ਲੱਭੋ।
4. ਕਨਟੇਨਰ ਸ਼ੁਰੂਅਾਤ ਲੌਗ ਪੜ੍ਹੋ। ਆਮ ਕਾਰਨ:

| ਲੌਗ ਮੈਸੇਜ | ਕਾਰਨ | ਸੁਧਾਰ |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | ਲੋੜੀਂਦੀ ਡਿਪੈਂਡੈਂਸੀ ਨਹੀਂ | ਇਸਨੂੰ `requirements.txt` ਵਿੱਚ ਸ਼ਾਮਲ ਕਰੋ ਅਤੇ ਦੁਬਾਰਾ ਡਿਪਲੋਇ |
| `KeyError: 'PROJECT_ENDPOINT'` | ਮਿਸਿੰਗ ਵਾਤਾਵਰਣ ਚਲ ਰਹੀ ਹੈ | `agent.yaml` ਵਿੱਚ env: ਹੇਠਾਂ env ਵੈਰੀਏਬਲ ਸ਼ਾਮਲ ਕਰੋ |
| `OSError: [Errno 98] Address already in use` | ਪੋਰਟ ਟਕਰਾਅ | ਯਕੀਨੀ ਬਣਾਓ ਕਿ `agent.yaml` ਵਿੱਚ `port: 8088` ਹੈ ਅਤੇ ਕਈ ਪ੍ਰਕਿਰਿਆਵਾਂ ਇੱਕੋ ਸਮੇਂ ਪੋਰਟ ਨਹੀਂ ਵਰਤ ਰਹੀਆਂ |
| `ConnectionRefusedError` | ਏਜੰਟ ਨੇ ਸੁਣਨਾ ਸ਼ੁਰੂ ਨਹੀਂ ਕੀਤਾ | `main.py` ਦੇ `from_agent_framework()` ਕਾਲ ਨੂੰ ਸਟਾਰਟਅਪ 'ਤੇ ਚਲਾਉਣਾ ਜਰੂਰੀ ਹੈ |

5. ਸਮੱਸਿਆ ਸੁਧਾਰੋ, ਫਿਰ [Module 6](06-deploy-to-foundry.md) ਤੋਂ ਦੁਬਾਰਾ ਡਿਪਲੋਇ ਕਰੋ।

### 5.3 ਡਿਪਲੋਇਮੈਂਟ ਸਮਾਂ ਖਤਮ ਹੋ ਗਿਆ

**ਸੁਧਾਰ:**
1. ਆਪਣਾ ਇੰਟਰਨੈੱਟ ਕਨੈਕਸ਼ਨ ਚੈੱਕ ਕਰੋ - Docker ਪੁਸ਼ ਵੱਡਾ ਹੋ ਸਕਦਾ ਹੈ (>100MB ਪਹਿਲੀ ਵਾਰ ਡਿਪਲੋਇ ਲਈ)।
2. ਜੇ ਤੁਸੀਂ ਕੋਰਪੋਰੇਟ ਪ੍ਰਾਕਸੀ ਪਿੱਛੇ ਹੋ, ਤਾਂ Docker Desktop ਪ੍ਰਾਕਸੀ ਸੈਟਿੰਗਜ਼ ਨੂੰ ਸੰਰਚਿਤ ਕਰੋ: **Docker Desktop** → **Settings** → **Resources** → **Proxies**।
3. ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ - ਨੈਟਵਰਕ ਵਿੱਚ ਛੋਟੇ ਬਾਰ-ਬਾਰ ਆਉਣ ਵਾਲੇ ਅਟਕਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ।

---

## 6. ਤੇਜ਼ ਸੰਦਰਭ: RBAC ਭੂਮਿਕਾਵਾਂ

| ਭੂਮਿਕਾ | ਆਮ ਸਕੋਪ | ਕੀ ਮਿਲਦਾ ਹੈ |
|--------|----------|--------------|
| **Azure AI User** | ਪ੍ਰੋਜੈਕਟ | ਡਾਟਾ ਐਕਸ਼ਨ: ਏਜੰਟ ਬਣਾਉਣਾ, ਡਿਪਲੋਇ ਅਤੇ ਕਾਲ ਕਰਨਾ (`agents/write`, `agents/read`) |
| **Azure AI Developer** | ਪ੍ਰੋਜੈਕਟ ਜਾਂ ਖਾਤਾ | ਡਾਟਾ ਐਕਸ਼ਨ + ਪ੍ਰੋਜੈਕਟ ਬਣਾਉਣਾ |
| **Azure AI Owner** | ਖਾਤਾ | ਪੂਰੀ ਪਹੁੰਚ + ਭੂਮਿਕਾ ਨਿਯੁਕਤੀ ਪਰਬੰਧਨ |
| **Azure AI Project Manager** | ਪ੍ਰੋਜੈਕਟ | ਡਾਟਾ ਐਕਸ਼ਨ + ਹੋਰਾਂ ਨੂੰ Azure AI User ਨਿਯੁਕਤ ਕਰ ਸਕਦਾ ਹੈ |
| **Contributor** | ਸਬਸਕ੍ਰਿਪਸ਼ਨ/ਰਿਸੋਰਸ ਗਰੁੱਪ | ਮੇਨੇਜਮੈਂਟ ਐਕਸ਼ਨ (ਸਰੋਤ ਬਣਾਉਣਾ/ਹਟਾਉਣਾ)। **ਡਾਟਾ ਐਕਸ਼ਨ ਸ਼ਾਮਲ ਨਹੀਂ** |
| **Owner** | ਸਬਸਕ੍ਰਿਪਸ਼ਨ/ਰਿਸੋਰਸ ਗਰੁੱਪ | ਮੇਨੇਜਮੈਂਟ ਐਕਸ਼ਨ + ਭੂਮਿਕਾ ਨਿਯੁਕਤੀ। **ਡਾਟਾ ਐਕਸ਼ਨ ਸ਼ਾਮਲ ਨਹੀਂ** |
| **Reader** | ਕਿਸੇ ਵੀ | ਸਿਰਫ ਪੜ੍ਹਨ ਲਈ ਮੇਨੇਜਮੈਂਟ ਪਹੁੰਚ |

> **ਮੁੱਖ ਸਿੱਖਿਆ:** `Owner` ਅਤੇ `Contributor` ਵਿੱਚ ਡਾਟਾ ਐਕਸ਼ਨ ਸ਼ਾਮਲ ਨਹੀਂ ਹਨ। ਏਜੰਟ ਕਾਰਜਾਂ ਲਈ ਤੁਹਾਨੂੰ ਸਦਾ `Azure AI *` ਭੂਮਿਕਾ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ। ਇਸ ਵਰਕਸ਼ਾਪ ਲਈ ਘੱਟੋ-ਘੱਟ ਭੂਮਿਕਾ **Azure AI User** ਹੈ ਜੋ **ਪ੍ਰੋਜੈਕਟ** ਸਕੋਪ 'ਤੇ ਹੈ।

---

## 7. ਵਰਕਸ਼ਾਪ ਸਮਾਪਤੀ ਸੂਚੀ

ਇਸਨੂੰ अंतिम ਪ੍ਰਮਾਣ ਵਜੋਂ ਵਰਤੋ ਕਿ ਤੁਸੀਂ ਸਭ ਕੁਝ ਪੂਰਾ ਕਰ ਲਿਆ ਹੈ:

| # | ਵਸਤੂ | ਮਾਡਿਊਲ | ਪਾਸ? |
|---|------|--------|------|
| 1 | ਸਾਰੇ ਪ੍ਰੀਰੀਕੁਇਜ਼ਿਟਸ ਇੰਸਟਾਲ ਅਤੇ ਵਰਿਫਾਈ ਕੀਤੇ ਹੋਏ | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit ਅਤੇ Foundry ਐਕਸਟੈਨਸ਼ਨ ਇੰਸਟਾਲ ਕੀਤੇ ਹੋਏ | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry ਪ੍ਰੋਜੈਕਟ ਬਣਾਇਆ ਗਿਆ (ਜਾਂ ਮੌਜੂਦਾ ਪ੍ਰੋਜੈਕਟ ਚੁਣਿਆ) | [02](02-create-foundry-project.md) | |
| 4 | ਮਾਡਲ ਤੈਨਾਤ ਕੀਤਾ ਗਿਆ (ਜਿਵੇਂ, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | ਪ੍ਰੋਜੈਕਟ ਸਕੋਪ ਤੇ Azure AI ਯੂਜ਼ਰ ਰੋਲ ਦਿੱਤਾ ਗਿਆ | [02](02-create-foundry-project.md) | |
| 6 | ਹੋਸਟਡ ਏਜੰਟ ਪ੍ਰੋਜੈਕਟ ਸਕੈਫੋਲਡ ਕੀਤਾ ਗਿਆ (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` ਨੂੰ PROJECT_ENDPOINT ਅਤੇ MODEL_DEPLOYMENT_NAME ਨਾਲ ਸੰਰਚਿਤ ਕੀਤਾ ਗਿਆ | [04](04-configure-and-code.md) | |
| 8 | Agent ਨਿਰਦੇਸ਼ਾਂ ਨੂੰ main.py ਵਿੱਚ ਕસ્ટમਾਈਜ਼ ਕੀਤਾ ਗਿਆ | [04](04-configure-and-code.md) | |
| 9 | ਵਰਚੁਅਲ ਵਾਤਾਵਰਣ ਬਣਾਇਆ ਗਿਆ ਅਤੇ ਡਿਪੈਂਡੈਂਸੀਜ਼ ਇੰਸਟਾਲ ਕੀਤੀਆਂ ਗਈਆਂ | [04](04-configure-and-code.md) | |
| 10 | Agent ਨੂੰ F5 ਜਾਂ ਟਰਮੀਨਲ ਨਾਲ ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਟੈਸਟ ਕੀਤਾ ਗਿਆ (4 ਸ్మੋਕ ਟੈਸਟ ਪਾਸ) | [05](05-test-locally.md) | |
| 11 | Foundry Agent ਸੇਵਾ ਤੇ ਤੈਨਾਤ ਕੀਤਾ ਗਿਆ | [06](06-deploy-to-foundry.md) | |
| 12 | ਕੰਟੇਨਰ ਸਥਿਤੀ "ਸ਼ੁਰੂ" ਜਾਂ "ਚੱਲ ਰਹੀ" ਦਿਖਾਉਂਦੀ ਹੈ | [06](06-deploy-to-foundry.md) | |
| 13 | VS ਕੋਡ ਪਲੇਗ੍ਰਾਉਂਡ ਵਿੱਚ ਵੈਰੀਫਾਈ ਕੀਤਾ ਗਿਆ (4 ਸ੍ਮੋਕ ਟੈਸਟ ਪਾਸ) | [07](07-verify-in-playground.md) | |
| 14 | Foundry ਪੋਰਟਲ ਪਲੇਗ੍ਰਾਉਂਡ ਵਿੱਚ ਵੈਰੀਫਾਈ ਕੀਤਾ ਗਿਆ (4 ਸ੍ਮੋਕ ਟੈਸਟ ਪਾਸ) | [07](07-verify-in-playground.md) | |

> **ਵਧਾਈ ਹੋਵੇ!** ਜੇ ਸਾਰੇ ਆਈਟਮ ਚੈੱਕ ਹੋ ਗਏ ਹਨ, ਤਾਂ ਤੁਸੀਂ ਪੂਰਾ ਵਰਕਸ਼ਾਪ مکمل ਕਰ ਲਿਆ ਹੈ। ਤੁਸੀਂ ਸ਼ੁਰੂ ਤੋਂ ਇੱਕ ਹੋਸਟਡ ਏਜੰਟ ਬਣਾਇਆ, ਉਸਨੂੰ ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਟੈਸਟ ਕੀਤਾ, Microsoft Foundry ਤੇ ਤੈਨਾਤ ਕੀਤਾ, ਅਤੇ ਉਤਪਾਦਨ ਵਿੱਚ ਇਸਦੀ ਸBiztaHbt मरीज की पुष्टि की।

---

**ਪਿਛੋਕੜ:** [07 - Verify in Playground](07-verify-in-playground.md) · **ਹੋਮ:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਇਨਕਾਰ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਵਿੱਚ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਤੀਕਤਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੇ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁਸ਼ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੇ ਉਪਯੋਗ ਤੋਂ ਉਪਜਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਮੀਆਂ ਜਾਂ ਭਾਸ਼ਾ ਵਿਕਲਪਾਂ ਲਈ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->