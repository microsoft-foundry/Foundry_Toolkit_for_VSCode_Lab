# मॉड्यूल 8 - समस्या निवारण

यह मॉड्यूल वर्कशॉप के दौरान मिलने वाली हर सामान्य समस्या के लिए एक संदर्भ गाइड है। इसे बुकमार्क करें - जब कुछ गलत होगा तो आप इसे वापस देखेंगे।

---

## 1. अनुमति त्रुटियाँ

### 1.1 `agents/write` अनुमति अस्वीकृत

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**मूल कारण:** आपके पास **प्रोजेक्ट** स्तर पर `Azure AI User` भूमिका नहीं है। यह वर्कशॉप में सबसे आम त्रुटि है।

**सुधार - चरण दर चरण:**

1. [https://portal.azure.com](https://portal.azure.com) खोलें।
2. शीर्ष खोज पट्टी में, अपने **Foundry प्रोजेक्ट** का नाम टाइप करें (जैसे, `workshop-agents`)।
3. **महत्वपूर्ण:** उस परिणाम पर क्लिक करें जो प्रकार **"Microsoft Foundry project"** दिखाता है, माता-पिता खाता/हब संसाधन नहीं। ये अलग संसाधन हैं जिनके अलग RBAC स्कोप हैं।
4. प्रोजेक्ट पृष्ठ के बाईं नेविगेशन में, **Access control (IAM)** पर क्लिक करें।
5. जांचने के लिए **Role assignments** टैब पर क्लिक करें कि क्या आपके पास पहले से यह भूमिका है:
   - अपना नाम या ईमेल खोजें।
   - यदि `Azure AI User` पहले से सूचीबद्ध है → त्रुटि का कारण अलग हो सकता है (नीचे चरण 8 देखें)।
   - यदि सूचीबद्ध नहीं है → इसे जोड़ने के लिए आगे बढ़ें।
6. **+ Add** → **Add role assignment** पर क्लिक करें।
7. **Role** टैब में:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) खोजें।
   - परिणामों में से इसे चुनें।
   - **Next** पर क्लिक करें।
8. **Members** टैब में:
   - **User, group, or service principal** चुनें।
   - **+ Select members** पर क्लिक करें।
   - अपना नाम या ईमेल खोजें।
   - परिणामों में से खुद को चुनें।
   - **Select** पर क्लिक करें।
9. **Review + assign** → फिर से **Review + assign** पर क्लिक करें।
10. **1-2 मिनट प्रतीक्षा करें** - RBAC परिवर्तन लागू होने में समय लेते हैं।
11. विफल ऑपरेशन को पुनः प्रयास करें।

> **क्यों Owner/Contributor पर्याप्त नहीं है:** Azure RBAC में दो प्रकार की अनुमतियाँ होती हैं - *management actions* और *data actions*। Owner और Contributor प्रबंधन क्रियाएं देते हैं (संसाधन बनाना, सेटिंग्स संपादित करना), लेकिन एजेंट ऑपरेशन के लिए `agents/write` **data action** की आवश्यकता होती है, जो केवल `Azure AI User`, `Azure AI Developer`, या `Azure AI Owner` भूमिकाओं में शामिल है। देखें [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)।

### 1.2 संसाधन प्रविजनिंग के दौरान `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**मूल कारण:** इस सब्सक्रिप्शन/संसाधन समूह में Azure संसाधन बनाने या संशोधित करने की अनुमति नहीं है।

**सुधार:**
1. अपने सब्सक्रिप्शन व्यवस्थापक से कहें कि वह Foundry प्रोजेक्ट वाले संसाधन समूह पर आपको **Contributor** भूमिका दें।
2. वैकल्पिक रूप से, उनसे कहें कि वे Foundry प्रोजेक्ट आपके लिए बनाएं और आपको प्रोजेक्ट पर **Azure AI User** दें।

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) के लिए `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**मूल कारण:** Azure सब्सक्रिप्शन ने Foundry के लिए आवश्यक संसाधन प्रदाता को पंजीकृत नहीं किया है।

**सुधार:**

1. टर्मिनल खोलें और चलाएँ:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. पंजीकरण पूरा होने का इंतजार करें (1-5 मिनट लग सकते हैं):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   अपेक्षित आउटपुट: `"Registered"`
3. ऑपरेशन को पुन: आज़माएँ।

---

## 2. Docker त्रुटियाँ (केवल यदि Docker इंस्टॉल है)

> Docker इस वर्कशॉप के लिए **वैकल्पिक** है। ये त्रुटियाँ केवल तब लागू होती हैं जब आपके पास Docker Desktop इंस्टॉल है और Foundry एक्सटेंशन स्थानीय कंटेनर बिल्ड का प्रयास करता है।

### 2.1 Docker daemon नहीं चल रहा

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**सुधार - चरण दर चरण:**

1. अपने Start मेनू (Windows) या Applications (macOS) में **Docker Desktop** ढूंढें और इसे लॉन्च करें।
2. Docker Desktop विंडो में **"Docker Desktop is running"** दिखने तक प्रतीक्षा करें - आमतौर पर 30-60 सेकंड लगते हैं।
3. सिस्टम ट्रे (Windows) या मेनू बार (macOS) में Docker व्हेल आइकन देखें। स्थिति पुष्टि के लिए उस पर होवर करें।
4. टर्मिनल में जांचें:
   ```powershell
   docker info
   ```
   यदि यह Docker सिस्टम जानकारी (Server Version, Storage Driver आदि) प्रिंट करता है, तो Docker चल रहा है।
5. **Windows विशेष:** यदि Docker अभी भी शुरू नहीं हो रहा है:
   - Docker Desktop खोलें → **Settings** (गियर आइकन) → **General**।
   - सुनिश्चित करें कि **Use the WSL 2 based engine** चेक किया गया है।
   - **Apply & restart** पर क्लिक करें।
   - यदि WSL 2 इंस्टॉल नहीं है तो उन्नत PowerShell में `wsl --install` चलाएँ और कंप्यूटर रीस्टार्ट करें।
6. पुनः डिप्लॉयमेंट करें।

### 2.2 डिपेंडेंसी त्रुटियों के साथ Docker build विफल

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**सुधार:**
1. `requirements.txt` खोलें और सभी पैकेज नाम सही वर्तनी के हों यह जांचें।
2. संस्करण पिनिंग सही है यह सुनिश्चित करें:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. पहले स्थानीय रूप से इंस्टॉल का परीक्षण करें:
   ```bash
   pip install -r requirements.txt
   ```
4. यदि निजी पैकेज इंडेक्स का उपयोग कर रहे हैं, तो सुनिश्चित करें कि Docker को नेटवर्क एक्सेस प्राप्त है।

### 2.3 कंटेनर प्लेटफ़ॉर्म मेल नहीं खाता (Apple Silicon)

यदि Apple Silicon मैक (M1/M2/M3/M4) से तैनात कर रहे हैं, तो कंटेनर को `linux/amd64` के लिए बनाया जाना चाहिए क्योंकि Foundry का कंटेनर रनटाइम AMD64 उपयोग करता है।

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry एक्सटेंशन का deploy कमांड अधिकांश मामलों में इसे स्वचालित रूप से संभालता है। यदि आपको आर्किटेक्चर-संबंधित त्रुटियाँ दिखती हैं, तो मैनुअली `--platform` फ्लैग के साथ बनाएं और Foundry टीम से संपर्क करें।

---

## 3. प्रमाणीकरण त्रुटियाँ

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) टोकन प्राप्त करने में विफल

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**मूल कारण:** `DefaultAzureCredential` चैन के किसी भी क्रेडेंशियल स्रोत के पास वैध टोकन नहीं है।

**सुधार - क्रम में प्रत्येक चरण आज़माएँ:**

1. **Azure CLI के माध्यम से पुनः लॉगिन करें** (सबसे आम सुधार):
   ```bash
   az login
   ```
   एक ब्राउज़र विंडो खुलेगा। साइन इन करें, फिर VS Code पर वापस जाएँ।

2. **सही सब्सक्रिप्शन सेट करें:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   यदि यह सही सब्सक्रिप्शन नहीं है:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code के माध्यम से पुनः लॉगिन करें:**
   - VS Code के नीचे-बाएँ में **Accounts** आइकन (व्यक्ति आइकन) पर क्लिक करें।
   - अपने अकाउंट नाम पर क्लिक करें → **Sign Out**।
   - फिर से Accounts आइकन पर क्लिक करें → **Sign in to Microsoft**।
   - ब्राउज़र साइन-इन प्रक्रिया पूरी करें।

4. **सर्विस प्रिंसिपल (केवल CI/CD मामलों में):**
   - अपनी `.env` में ये पर्यावरण चर सेट करें:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - फिर अपने एजेंट प्रक्रिया को पुनरारंभ करें।

5. **टोकन कैश जांचें:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   यदि यह विफल हो जाता है, तो आपका CLI टोकन समाप्त हो गया है। पुनः `az login` चलाएँ।

### 3.2 टोकन स्थानीय रूप से काम करता है लेकिन होस्टेड डिप्लॉयमेंट में नहीं

**मूल कारण:** होस्टेड एजेंट सिस्टम-प्रबंधित पहचान का उपयोग करता है, जो आपकी व्यक्तिगत क्रेडेंशियल से अलग है।

**सुधार:** यह अपेक्षित व्यवहार है - डिप्लॉयमेंट के दौरान प्रबंधित पहचान स्वचालित रूप से प्रोविजन की जाती है। यदि होस्टेड एजेंट को अभी भी प्रमाणीकरण त्रुटियां मिल रही हैं:
1. जांचें कि Foundry प्रोजेक्ट की प्रबंधित पहचान Azure OpenAI संसाधन तक पहुंच रखती है।
2. `agent.yaml` में `PROJECT_ENDPOINT` सही है यह सुनिश्चित करें।

---

## 4. मॉडल त्रुटियाँ

### 4.1 मॉडल तैनाती नहीं मिली

```
Error: Model deployment not found / The specified deployment does not exist
```

**सुधार - चरण दर चरण:**

1. अपनी `.env` फ़ाइल खोलें और `AZURE_AI_MODEL_DEPLOYMENT_NAME` का मान नोट करें।
2. VS Code में **Microsoft Foundry** साइडबार खोलें।
3. अपना प्रोजेक्ट एक्सपैंड करें → **Model Deployments**।
4. वहाँ सूचीबद्ध तैनाती नाम की तुलना अपनी `.env` मूल्य से करें।
5. नाम **केस-संवेदी** होता है - `gpt-4o` और `GPT-4o` अलग हैं।
6. यदि वे मेल नहीं खाते, तो अपनी `.env` को साइडबार में दिखाए गए सटीक नाम के अनुसार अपडेट करें।
7. होस्टेड डिप्लॉयमेंट के लिए, `agent.yaml` भी अपडेट करें:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 मॉडल अप्रत्याशित कंटेंट के साथ उत्तर देता है

**सुधार:**
1. `main.py` में `EXECUTIVE_AGENT_INSTRUCTIONS` स्थिरांक की समीक्षा करें। सुनिश्चित करें कि यह ट्रंकेट या भ्रष्ट नहीं हुआ है।
2. मॉडल तापमान सेटिंग की जांच करें (यदि कॉन्फ़िगर करने योग्य है) - कम मान अधिक निर्धारित आउटपुट देता है।
3. तैनात मॉडल की तुलना करें (जैसे, `gpt-4o` बनाम `gpt-4o-mini`) - अलग मॉडल की क्षमताएँ अलग होती हैं।

---

## 5. डिप्लॉयमेंट त्रुटियाँ

### 5.1 ACR पुल प्राधिकरण

```
Error: AcrPullUnauthorized
```

**मूल कारण:** Foundry प्रोजेक्ट की प्रबंधित पहचान Azure Container Registry से कंटेनर इमेज नहीं खींच पा रही है।

**सुधार - चरण दर चरण:**

1. [https://portal.azure.com](https://portal.azure.com) खोलें।
2. शीर्ष खोज बार में **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** खोजें।
3. उस रजिस्ट्री पर क्लिक करें जो आपके Foundry प्रोजेक्ट से जुड़ी है (सामान्यतः वही संसाधन समूह होगा)।
4. बाईं नेविगेशन में **Access control (IAM)** पर क्लिक करें।
5. **+ Add** → **Add role assignment** पर क्लिक करें।
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** खोजें और चुनें। **Next** पर क्लिक करें।
7. **Managed identity** चुनें → **+ Select members** पर क्लिक करें।
8. Foundry प्रोजेक्ट की प्रबंधित पहचान खोजें और चुनें।
9. **Select** → **Review + assign** → फिर से **Review + assign** पर क्लिक करें।

> यह भूमिका असाइनमेंट आमतौर पर Foundry एक्सटेंशन द्वारा स्वचालित रूप से सेट की जाती है। यदि आपको यह त्रुटि दिखती है, तो स्वतः सेटअप विफल हो सकता है। आप पुनः डिप्लॉयमेंट भी कर सकते हैं - एक्सटेंशन सेटअप पुन: प्रयास कर सकता है।

### 5.2 डिप्लॉयमेंट के बाद एजेंट शुरू नहीं होता

**लक्षण:** कंटेनर स्थिति 5 मिनट से अधिक समय तक "Pending" रहती है या "Failed" दिखाती है।

**सुधार - चरण दर चरण:**

1. VS Code में **Microsoft Foundry** साइडबार खोलें।
2. अपने होस्टेड एजेंट पर क्लिक करें → संस्करण चुनें।
3. डिटेल पैनल में, **Container Details** जांचें → **Logs** सेक्शन या लिंक खोजें।
4. कंटेनर स्टार्टअप लॉग पढ़ें। सामान्य कारण:

| लॉग संदेश | कारण | सुधार |
|-------------|-------|-------|
| `ModuleNotFoundError: No module named 'xxx'` | निर्भरता गायब | इसे `requirements.txt` में जोड़ें और पुनः डिप्लॉय करें |
| `KeyError: 'PROJECT_ENDPOINT'` | पर्यावरण चर गायब | `agent.yaml` में `env:` के तहत इसे जोड़ें |
| `OSError: [Errno 98] Address already in use` | पोर्ट संघर्ष | सुनिश्चित करें कि `agent.yaml` में `port: 8088` है और केवल एक प्रक्रिया इसे बांधती है |
| `ConnectionRefusedError` | एजेंट ने सुनना शुरू नहीं किया | `main.py` - `from_agent_framework()` कॉल स्टार्टअप पर चलना चाहिए |

5. समस्या ठीक करें, फिर [मॉड्यूल 6](06-deploy-to-foundry.md) से पुनः डिप्लॉय करें।

### 5.3 डिप्लॉयमेंट टाइमआउट हो जाता है

**सुधार:**
1. अपनी इंटरनेट कनेक्शन जांचें - Docker पुश बड़ा हो सकता है (>100MB पहली डिप्लॉयमेंट के लिए)।
2. यदि कॉर्पोरेट प्रॉक्सी के पीछे हैं, तो Docker Desktop प्रॉक्सी सेटिंग्स कॉन्फ़िगर करें: **Docker Desktop** → **Settings** → **Resources** → **Proxies**।
3. पुनः प्रयास करें - नेटवर्क अस्थिरता अस्थायी विफलताओं का कारण हो सकती है।

---

## 6. त्वरित संदर्भ: RBAC भूमिकाएँ

| भूमिका | सामान्य स्कोप | क्या प्रदान करता है |
|------|---------------|--------------------|
| **Azure AI User** | प्रोजेक्ट | डेटा क्रियाएं: एजेंट बनाना, डिप्लॉय, और इनवोक करना (`agents/write`, `agents/read`) |
| **Azure AI Developer** | प्रोजेक्ट या खाता | डेटा क्रियाएं + प्रोजेक्ट निर्माण |
| **Azure AI Owner** | खाता | पूर्ण पहुंच + भूमिका असाइनमेंट प्रबंधन |
| **Azure AI Project Manager** | प्रोजेक्ट | डेटा क्रियाएं + दूसरों को Azure AI User असाइन कर सकता है |
| **Contributor** | सब्सक्रिप्शन/आरजी | प्रबंधन क्रियाएं (संसाधन बनाना/हटाना)। **डेटा क्रियाओं को शामिल नहीं करता** |
| **Owner** | सब्सक्रिप्शन/आरजी | प्रबंधन क्रियाएं + भूमिका असाइनमेंट। **डेटा क्रियाओं को शामिल नहीं करता** |
| **Reader** | कोई भी | केवल पढ़ने वाला प्रबंधन एक्सेस |

> **मुख्य निष्कर्ष:** `Owner` और `Contributor` में डेटा क्रियाएँ **नहीं** होतीं। एजेंट ऑपरेशन के लिए हमेशा `Azure AI *` भूमिका की आवश्यकता होती है। इस वर्कशॉप के लिए न्यूनतम भूमिका **Azure AI User** है, वह भी **प्रोजेक्ट** स्कोप पर।

---

## 7. वर्कशॉप पूर्णता चेकलिस्ट

इसे अंतिम स्वीकृति के रूप में उपयोग करें कि आपने सब कुछ पूरा कर लिया है:

| # | आइटम | मॉड्यूल | पास? |
|---|-------|---------|------|
| 1 | सभी पूर्वापेक्षाएँ इंस्टॉल और सत्यापित | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit और Foundry एक्सटेंशन इंस्टॉल | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry प्रोजेक्ट बनाया गया (या मौजूदा प्रोजेक्ट चुना गया) | [02](02-create-foundry-project.md) | |
| 4 | मॉडल तैनात किया गया (जैसे, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | प्रोजेक्ट स्कोप पर Azure AI उपयोगकर्ता भूमिका आवंटित | [02](02-create-foundry-project.md) | |
| 6 | होस्टेड एजेंट प्रोजेक्ट स्कैफ़ोल्ड किया गया (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` को PROJECT_ENDPOINT और MODEL_DEPLOYMENT_NAME के साथ कॉन्फ़िगर किया गया | [04](04-configure-and-code.md) | |
| 8 | main.py में एजेंट निर्देश अनुकूलित किए गए | [04](04-configure-and-code.md) | |
| 9 | वर्चुअल एनवायरनमेंट बनाया गया और निर्भरताएँ स्थापित की गईं | [04](04-configure-and-code.md) | |
| 10 | F5 या टर्मिनल के साथ स्थानीय रूप से एजेंट का परीक्षण किया गया (4 स्मोक टेस्ट पास हुए) | [05](05-test-locally.md) | |
| 11 | Foundry Agent सेवा में तैनात किया गया | [06](06-deploy-to-foundry.md) | |
| 12 | कंटेनर स्थिति "शुरू किया गया" या "चल रहा है" दिखाती है | [06](06-deploy-to-foundry.md) | |
| 13 | VS कोड प्लेग्राउंड में सत्यापित (4 स्मोक टेस्ट पास हुए) | [07](07-verify-in-playground.md) | |
| 14 | Foundry पोर्टल प्लेग्राउंड में सत्यापित (4 स्मोक टेस्ट पास हुए) | [07](07-verify-in-playground.md) | |

> **बधाइयाँ!** यदि सभी आइटम चेक हो गए हैं, तो आपने पूरा कार्यशाला समाप्त कर ली है। आपने शून्य से होस्टेड एजेंट बनाया है, उसे स्थानीय रूप से परीक्षण किया है, Microsoft Foundry पर तैनात किया है, और इसे उत्पादन में मान्य किया है।

---

**पिछला:** [07 - प्लेग्राउंड में सत्यापित करें](07-verify-in-playground.md) · **होम:** [कार्यशाला README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनुवादित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियां या गलतियां हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में आधिकारिक स्रोत माना जाना चाहिए। महत्त्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->