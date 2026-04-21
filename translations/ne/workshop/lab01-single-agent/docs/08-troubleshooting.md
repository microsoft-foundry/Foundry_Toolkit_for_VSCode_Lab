# Module 8 - समस्या समाधान

यो मोड्युल वर्कशपको दौरान सामना हुने हरेक सामान्य समस्याको लागि संदर्भ गाइड हो। यसलाई बुकमार्क गर्नुहोस् - केही गलत हुँदा तपाईं यसमा फेरि फर्कनुहुनेछ।

---

## 1. अनुमति त्रुटिहरू

### 1.1 `agents/write` अनुमति अस्वीकृत

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**मूल कारण:** तपाईंको **प्रोजेक्ट** स्तरमा `Azure AI User` भूमिका छैन। यो वर्कशपमा सबैभन्दा सामान्य त्रुटि हो।

**समाधान - चरणबद्ध:**

1. [https://portal.azure.com](https://portal.azure.com) खोल्नुहोस्।
2. शीर्ष खोज पट्टीमा, तपाईंको **Foundry प्रोजेक्ट** को नाम टाइप गर्नुहोस् (जस्तै, `workshop-agents`)।
3. **महत्वपूर्ण:** परिणाममा देखिएको प्रकार **"Microsoft Foundry project"** मा क्लिक गर्नुहोस्, अभिभावक खाता/हब संसाधनमा होइन। यी भिन्न RBAC स्कोप भएका अलग स्रोतहरू हुन्।
4. प्रोजेक्ट पृष्ठको बाँया नेभिगेसनमा, **Access control (IAM)** क्लिक गर्नुहोस्।
5. तपाईंसँग पहिले नै भूमिका छ कि छैन जाँच्न **Role assignments** ट्याब क्लिक गर्नुहोस्:
   - आफ्नो नाम वा इमेल खोज्नुहोस्।
   - यदि `Azure AI User` पहिले नै सूचीबद्ध छ → त्रुटिको कारण फरक छ (हेर्नुहोस् तलको चरण 8)।
   - सूचीबद्ध छैन भने → थप्न जारी राख्नुहोस्।
6. **+ Add** क्लिक गर्नुहोस् → **Add role assignment**।
7. **Role** ट्याबमा:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) खोज्नुहोस्।
   - परिणामबाट छान्नुहोस्।
   - **Next** क्लिक गर्नुहोस्।
8. **Members** ट्याबमा:
   - **User, group, or service principal** चयन गर्नुहोस्।
   - **+ Select members** क्लिक गर्नुहोस्।
   - आफ्नो नाम वा इमेल ठेगाना खोज्नुहोस्।
   - परिणामबाट आफूलाई चयन गर्नुहोस्।
   - **Select** क्लिक गर्नुहोस्।
9. **Review + assign** → फेरि **Review + assign** क्लिक गर्नुहोस्।
10. **१-२ मिनेट कुर्नुहोस्** - RBAC परिवर्तनहरू फैलिन समय लाग्छ।
11. असफल भएको अपरेशन पुनः प्रयास गर्नुहोस्।

> **किन Owner/Contributor पर्याप्त हुँदैन:** Azure RBAC मा दुई प्रकारका अनुमति हुन्छन् - *प्रबंधन क्रियाकलापहरू* र *डेटा क्रियाकलापहरू*। Owner र Contributor ले प्रबंधन क्रियाकलापहरू (संसाधनहरू सिर्जना, सेटिङहरू सम्पादन) दिन्छन्, तर एजेन्ट अपरेसनहरूका लागि `agents/write` **डेटा क्रियाकलाप** आवश्यक हुन्छ जुन केवल `Azure AI User`, `Azure AI Developer`, वा `Azure AI Owner` भूमिकाहरूमा समावेश हुन्छ। हेर्नुहोस् [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)।

### 1.2 स्रोत व्यवस्थापनको बेलामा `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**मूल कारण:** तपाईंलाई यस सदस्यता/संसाधन समूहमा Azure स्रोतहरू सिर्जना वा संसोधन गर्ने अनुमति छैन।

**समाधान:**
1. आफ्नो सदस्यता प्रशासकलाई Foundry प्रोजेक्ट बस्ने स्रोत समूहमा **Contributor** भूमिका प्रदान गर्न भन्नुहोस्।
2. वा, उनीहरूलाई Foundry प्रोजेक्ट तपाईंका लागि सिर्जना गर्न र तपाईंलाई प्रोजेक्टमा **Azure AI User** दिन भन्नुहोस्।

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) को लागि `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**मूल कारण:** Foundry को लागि आवश्यक स्रोत प्रदायक सदस्यतामा दर्ता गरिएको छैन।

**समाधान:**

1. टर्मिनल खोल्नुहोस् र चलाउनुहोस्:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. दर्ता पूरा हुन कुर्नुहोस् (१-५ मिनेट लाग्न सक्छ):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   अपेक्षित परिणाम: `"Registered"`
3. अपरेशन पुनः प्रयास गर्नुहोस्।

---

## 2. Docker त्रुटिहरू (Docker इन्स्टल भएको खण्डमा मात्र)

> Docker यो वर्कशपको लागि **वैकल्पिक** छ। यी त्रुटिहरू केवल तब लागु हुन्छ जब तपाईंले Docker Desktop इन्स्टल गर्नुभएको छ र Foundry विस्तार स्थानीय कन्टेनर निर्माण प्रयास गर्दछ।

### 2.1 Docker daemon चलिरहेको छैन

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**समाधान - चरणबद्ध:**

1. **Docker Desktop** तपाईंको Start मेनु (Windows) वा Applications (macOS) मा खोजी खोल्नुस्।
2. Docker Desktop विन्डोमा **"Docker Desktop is running"** देखिन कुर्नुहोस् - सामान्यतः ३०-६० सेकेन्ड लाग्छ।
3. तपाईंको प्रणाली ट्रे (Windows) वा मेनु बार (macOS) मा Docker ह्वेल आइकन हेर्नुहोस्। स्थिति देख्न माथि माउस राख्नुहोस्।
4. टर्मिनलमा जाँच गर्नुहोस्:
   ```powershell
   docker info
   ```
   यदि यसले Docker प्रणाली जानकारी (Server संस्करण, Storage Driver, आदि) देखाउँछ भने Docker चलिरहेको छ।
5. **Windows विशिष्ट:** Docker अझै सुरु नभए:
   - Docker Desktop खोल्नुहोस् → **Settings** (गियर आइकन) → **General**।
   - सुनिश्चित गर्नुहोस् कि **Use the WSL 2 based engine** चयन गरिएको छ।
   - **Apply & restart** क्लिक गर्नुहोस्।
   - यदि WSL 2 इन्स्टल छैन् भने, उचाइ भएको PowerShell मा `wsl --install` चलाउनुहोस् र कम्प्युटर पुनः सुरु गर्नुहोस्।
6. पुनः डिप्लोयमेन्ट प्रयास गर्नुहोस्।

### 2.2 Docker निर्माण निर्भरता त्रुटिहरू संग असफल

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**समाधान:**
1. `requirements.txt` खोल्नुहोस् र सबै प्याकेज नामहरू सही हिज्जेमा छन् भनेर जाँच गर्नुहोस्।
2. संस्करण पिनिंग सही छ कि छैन सुनिश्चित गर्नुहोस्:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. पहिले स्थानीय रूपमा इन्स्टल परीक्षण गर्नुहोस्:
   ```bash
   pip install -r requirements.txt
   ```
4. यदि निजी प्याकेज इन्डेक्स प्रयोग गर्दै हुनुहुन्छ भने Docker लाई त्यसको नेटवर्क पहुँच छ सुनिश्चित गर्नुहोस्।

### 2.3 कन्टेनर प्लेटफर्म मेल नखाने (Apple Silicon)

यदि Apple Silicon Mac (M1/M2/M3/M4) बाट डिप्लोय गर्दै हुनुहुन्छ भने, कन्टेनर `linux/amd64` को लागि बनाउनु पर्छ किनकि Foundry को कन्टेनर रनटाइम AMD64 प्रयोग गर्छ।

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry विस्तारको deploy आदेशले यो अधिकांश अवस्थामा स्वचालित रूपमा व्यवस्थापन गर्छ। यदि तपाईंलाई आर्किटेक्चर सम्बन्धी त्रुटिहरू देखिन्छन् भने, `--platform` फ्ल्याग साथ म्यानुअली निर्माण गर्नुहोस् र Foundry टोलीसँग सम्पर्क गर्नुहोस्।

---

## 3. प्रमाणीकरण त्रुटिहरू

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) टोकन प्राप्त गर्न असफल

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**मूल कारण:** `DefaultAzureCredential` चेनमा कुनै पनि प्रमाणीकरण स्रोतसँग मान्य टोकन छैन।

**समाधान - प्रत्येक चरण क्रमशः प्रयास गर्नुहोस्:**

1. **Azure CLI बाट पुनः लगइन गर्नुहोस्** (सबैभन्दा सामान्य समाधान):
   ```bash
   az login
   ```
   एउटा ब्राउजर विन्डो खुल्छ। लगइन गर्नुहोस्, त्यसपछि VS Code मा फर्कनुहोस्।

2. **सही सदस्यता सेट गर्नुहोस्:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   यदि यो सही सदस्यता होइन भने:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code मार्फत पुनः लगइन:**
   - VS Code को तल-बायाँमा रहेको **Accounts** आइकन (व्यक्ति आइकन) क्लिक गर्नुहोस्।
   - आफ्नो खाता नाम क्लिक गरेर → **Sign Out**।
   - पुन: Accounts आइकन क्लिक → **Sign in to Microsoft**।
   - ब्राउजर साइन-इन पूरा गर्नुहोस्।

4. **Service principal (CI/CD परिस्थितिहरूमा मात्र):**
   - आफ्नो `.env` मा यी वातावरण चरहरू सेट गर्नुहोस्:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - त्यसपछि एजेन्ट प्रक्रिया पुनः सुरु गर्नुहोस्।

5. **टोकन क्यास जाँच गर्नुहोस्:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   यदि यो असफल भयो भने, तपाईंको CLI टोकन म्याद सकिएको छ। `az login` फेरि चलाउनुहोस्।

### 3.2 टोकन स्थानीय रूपमा काम गर्छ तर होस्ट डिप्लोयमेन्टमा काम गर्दैन

**मूल कारण:** होस्ट गरिएको एजेन्टले सिस्टम व्यवस्थापित पहिचान प्रयोग गर्छ, जुन तपाईंको व्यक्तिगत प्रमाणीकरण फरक हुन्छ।

**समाधान:** यो अपेक्षित व्यवहार हो - व्यवस्थापित पहिचान डिप्लोयमेन्टको समयमा स्वचालित रूपमा बनाइन्छ। यदि होस्ट गरिएको एजेन्टले अझै प्रमाणीकरण त्रुटिहरू देखाउँछ भने:
1. Foundry प्रोजेक्टको व्यवस्थापित पहिचानसँग Azure OpenAI स्रोतमा पहुँच छ कि छैन जाँच गर्नुहोस्।
2. `agent.yaml` मा `PROJECT_ENDPOINT` सही छ कि छैन जाँच गर्नुहोस्।

---

## 4. मोडल त्रुटिहरू

### 4.1 मोडल डिप्लोयमेन्ट फेला परेन

```
Error: Model deployment not found / The specified deployment does not exist
```

**समाधान - चरणबद्ध:**

1. आफ्नो `.env` फाइल खोल्नुहोस् र `AZURE_AI_MODEL_DEPLOYMENT_NAME` को मान नोट गर्नुहोस्।
2. VS Code मा **Microsoft Foundry** साइडबार खोल्नुहोस्।
3. आफ्नो प्रोजेक्ट विस्तार गर्नुहोस् → **Model Deployments**।
4. त्यहाँ सूचीबद्ध डिप्लोयमेन्ट नामलाई तपाईंको `.env` मानसँग तुलना गर्नुहोस्।
5. नाम **case-sensitive** हुन्छ - `gpt-4o` र `GPT-4o` फरक हुन्।
6. मेल खाँदैन भने, आफ्नो `.env` लाई साइडबारमा देखिएको ठीक नाम प्रयोग गरेर अपडेट गर्नुहोस्।
7. होस्ट गरिएको डिप्लोयमेन्टको लागि, `agent.yaml` पनि अपडेट गर्नुहोस्:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 मोडलले अप्रत्याशित सामग्री प्रतिक्रिया दिन्छ

**समाधान:**
1. `main.py` मा रहेको `EXECUTIVE_AGENT_INSTRUCTIONS` स्थिराङ्क समीक्षा गर्नुहोस्। यो त्रुटिपूर्ण वा कटेको छैन सुनिश्चित गर्नुहोस्।
2. मोडल तापमान सेटिङ (यदि कन्फिगर योग्य छ) जाँच्नुहोस् - कम मानले अधिक निर्धारक आउटपुट दिन्छ।
3. प्रयोग गरिएको मोडल तुलना गर्नुहोस् (जस्तै, `gpt-4o` बनाम `gpt-4o-mini`) - विभिन्न मोडेलहरूले फरक क्षमताहरू राख्छन्।

---

## 5. डिप्लोयमेन्ट त्रुटिहरू

### 5.1 ACR पुल प्राधिकरण

```
Error: AcrPullUnauthorized
```

**मूल कारण:** Foundry प्रोजेक्टको व्यवस्थापित पहिचान Azure Container Registry बाट कन्टेनर इमेज तान्न सक्दैन।

**समाधान - चरणबद्ध:**

1. [https://portal.azure.com](https://portal.azure.com) खोल्नुहोस्।
2. शीर्ष खोज पट्टीमा **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** खोज्नुहोस्।
3. तपाईंको Foundry प्रोजेक्टसँग सम्बन्धित रजिस्ट्रीमा क्लिक गर्नुहोस् (सामान्यतया समान स्रोत समूहमा हुन्छ)।
4. बाँया नेभिगेसनमा, **Access control (IAM)** क्लिक गर्नुहोस्।
5. **+ Add** → **Add role assignment** क्लिक गर्नुहोस्।
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** खोज्नुहोस् र छान्नुहोस्। **Next** क्लिक गर्नुहोस्।
7. **Managed identity** चयन गर्नुहोस् → **+ Select members** क्लिक गर्नुहोस्।
8. Foundry प्रोजेक्टको व्यवस्थापित पहिचान खोजी चयन गर्नुहोस्।
9. **Select** → **Review + assign** → **Review + assign** क्लिक गर्नुहोस्।

> यो भूमिका नियुक्ति सामान्यतया Foundry विस्तारले स्वचालित रूपमा सेटअप गर्दछ। यदि तपाईंसँग यो त्रुटि छ भने, स्वत: सेटअप असफल भएको हुन सक्छ। तपाई पुनः डिप्लोय गरि सेटअप पुनः प्रयास गर्न सक्नुहुन्छ।

### 5.2 एजेन्ट डिप्लोय पछि सुरु हुन असफल

**लक्षणहरू:** कन्टेनर स्थिति ५ मिनेट भन्दा बढी "Pending" रहन्छ वा "Failed" देखाउँछ।

**समाधान - चरणबद्ध:**

1. VS Code मा **Microsoft Foundry** साइडबार खोल्नुहोस्।
2. तपाईंको होस्ट गरिएको एजेन्ट क्लिक गर्नुहोस् → संस्करण चयन गर्नुहोस्।
3. विवरण प्यानलमा **Container Details** जाँच्नुहोस् → **Logs** सेक्सन वा लिङ्क खोज्नुहोस्।
4. कन्टेनर स्टार्टअप लगहरू पढ्नुहोस्। सामान्य कारणहरू:

| लग सन्देश | कारण | समाधान |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | निर्भरता हराएको | `requirements.txt` मा थप्नुहोस् र पुनः डिप्लोय गर्नुहोस् |
| `KeyError: 'PROJECT_ENDPOINT'` | वातावरण चर हराएको | `agent.yaml` मा `env:` अन्तर्गत पर्यावरण चर थप्नुहोस् |
| `OSError: [Errno 98] Address already in use` | पोर्ट द्वन्द्व | `agent.yaml` मा `port: 8088` छ र केवल एक प्रक्रिया यसमा बाँधिएको छ सुनिश्चित गर्नुहोस् |
| `ConnectionRefusedError` | एजेन्टले सुनिरहेको छैन | `main.py` जाँच्नुहोस् - `from_agent_framework()` कल स्टार्टअपमा हुनुपर्छ |

5. समस्या समाधान गर्नुहोस्, त्यसपछि [Module 6](06-deploy-to-foundry.md) बाट पुनः डिप्लोय गर्नुहोस्।

### 5.3 डिप्लोयमेन्ट टाइमआउट हुन्छ

**समाधान:**
1. आफ्नो इन्टरनेट जडान जाँच गर्नुहोस् - Docker पुश ठूलो हुन सक्छ (>१००MB पहिलो डिप्लोयका लागि)।
2. यदि कर्पोरेट प्रोक्सी पछाडि हुनुहुन्छ भने, Docker Desktop प्रोक्सी सेटिङहरू कन्फिगर छ कि छैन जाँच गर्नुहोस्: **Docker Desktop** → **Settings** → **Resources** → **Proxies**।
3. फेरि प्रयास गर्नुहोस् - नेटवर्क झट्का कारण अस्थायी विफलताहरू हुन सक्छन्।

---

## 6. छिटो संदर्भ: RBAC भूमिका

| भूमिका | सामान्य स्कोप | के प्रदान गर्छ |
|------|---------------|----------------|
| **Azure AI User** | प्रोजेक्ट | डेटा क्रियाकलापहरू: एजेन्ट निर्माण, डिप्लोय, र कल गर्ने (`agents/write`, `agents/read`) |
| **Azure AI Developer** | प्रोजेक्ट वा खाता | डेटा क्रियाकलाप + प्रोजेक्ट सिर्जना |
| **Azure AI Owner** | खाता | पूर्ण पहुँच + भूमिका वितरण व्यवस्थापन |
| **Azure AI Project Manager** | प्रोजेक्ट | डेटा क्रियाकलाप + अरूलाई Azure AI User दिन सक्छ |
| **Contributor** | सदस्यता/स्रोत समूह | प्रबंधन क्रियाकलाप (संसाधन सिर्जना/मिटाउने)। **डेटा क्रियाकलाप समावेश छैन** |
| **Owner** | सदस्यता/स्रोत समूह | प्रबंधन क्रियाकलाप + भूमिका वितरण। **डेटा क्रियाकलाप समावेश छैन** |
| **Reader** | कुनै | केवल पढ्ने प्रबंधन पहुँच |

> **मुख्य कुरा:** `Owner` र `Contributor` मा डेटा क्रियाकलाप हुँदैनन्। एजेन्ट अपरेसनहरूका लागि तपाईंलाई सँधै `Azure AI *` भूमिका चाहिन्छ। यस वर्कशपको लागि न्यूनतम भूमिका **प्रोजेक्ट** स्तरमा **Azure AI User** हो।

---

## 7. वर्कशप समाप्ति चेकलिस्ट

यो सम्पूर्ण काम सम्पन्न भएको अन्तिम स्वीकृति को रूप मा प्रयोग गर्नुहोस्:

| # | वस्तु | मोड्युल | पास? |
|---|------|--------|---|
| 1 | सबै पूर्वापेक्षाहरू इन्स्टल र प्रमाणित गरिएका | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit र Foundry विस्तारहरू इन्स्टल गरिएका | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry प्रोजेक्ट सिर्जना गरिएको (वा अस्तित्वमा रहेको प्रोजेक्ट चयन गरिएको) | [02](02-create-foundry-project.md) | |
| 4 | मोडेल परिनियोजित (जस्तै, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Azure AI प्रयोगकर्ता भूमिका परियोजना स्कोपमा तोकिएको | [02](02-create-foundry-project.md) | |
| 6 | होस्ट गरिएका एजेन्ट परियोजना स्क्याफोल्ड गरिएको (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` PROJECT_ENDPOINT र MODEL_DEPLOYMENT_NAME सँग कन्फिगर गरिएको | [04](04-configure-and-code.md) | |
| 8 | एजेन्ट निर्देशनहरु main.py मा अनुकूलित गरिएको | [04](04-configure-and-code.md) | |
| 9 | भर्चुअल वातावरण सिर्जना गरिएको र निर्भरता स्थापना गरिएको | [04](04-configure-and-code.md) | |
| 10 | एजेन्टलाई स्थानीय रूपमा F5 वा टर्मिनलबाट परीक्षण गरिएको (4 वटा स्मोक टेस्ट पास) | [05](05-test-locally.md) | |
| 11 | Foundry Agent Service मा परिनियोजित गरिएको | [06](06-deploy-to-foundry.md) | |
| 12 | कन्टेनर स्थिति "सुरु भयो" वा "चलिरहेको" देखाउँछ | [06](06-deploy-to-foundry.md) | |
| 13 | VS Code Playground मा प्रमाणीकरण गरिएको (4 स्मोक टेस्ट पास) | [07](07-verify-in-playground.md) | |
| 14 | Foundry Portal Playground मा प्रमाणीकरण गरिएको (4 स्मोक टेस्ट पास) | [07](07-verify-in-playground.md) | |

> **बधाई छ!** यदि सबै वस्तुहरू जाँचिएको छ भने, तपाईंले सम्पूर्ण वर्कशप पूरा गर्नुभयो। तपाईंले शून्यबाट होस्ट गरिएका एजेन्ट बनाउनु भयो, यसलाई स्थानीय रूपमा परीक्षण गर्नुभयो, Microsoft Foundry मा परिनियोजित गर्नुभयो, र उत्पादनमा मान्य गर्नुभयो।

---

**अघिल्लो:** [07 - Verify in Playground](07-verify-in-playground.md) · **गृहपृष्ठ:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:  
यो दस्तावेज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी शुद्धताका लागि प्रयासरत छौं, तथापि कृपया जानकार हुनुस् कि स्वचालित अनुवादमा त्रुटिहरू वा गलतिहरू हुन सक्छन्। मूल भाषा मा रहेको दस्तावेजलाई विश्वसनीय स्रोत मान्नु पर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानवीय अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलतफहमी वा गलत व्याख्याहरूको लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->