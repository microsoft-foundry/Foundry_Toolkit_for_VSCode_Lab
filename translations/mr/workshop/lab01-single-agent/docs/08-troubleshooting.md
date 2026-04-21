# Module 8 - समस्या निवारण

हा मॉड्यूल कार्यशाळेदरम्यान सामान्यपणे उद्भवणाऱ्या प्रत्येक समस्येसाठी संदर्भ मार्गदर्शक आहे. त्यास बुकमार्क करा - काहीतरी चूक झाल्यास तुम्ही याकडे परत येणार आहात.

---

## 1. परवानगी संबंधित त्रुटी

### 1.1 `agents/write` परवानगी नाकारली गेली

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**मूळ कारण:** तुमच्याकडे **प्रोजेक्ट** पातळीवर `Azure AI User` भूमिका नाही. ही कार्यशाळेत सर्वात सामान्य त्रुटी आहे.

**दुरुस्ती - चरणानुसार:**

1. [https://portal.azure.com](https://portal.azure.com) उघडा.
2. वरच्या शोध पट्टीत तुमच्या **Foundry प्रोजेक्ट**चे नाव टाका (उदा., `workshop-agents`).
3. **महत्वाचे:** तो निकाल क्लिक करा ज्यात प्रकार **"Microsoft Foundry project"** दिसतो, मुख्य खाते/हब स्त्रोत नाही. हे वेगळे स्रोत आहेत ज्यांचे वेगळे RBAC परिमाणे आहेत.
4. प्रोजेक्ट पानाच्या डाव्या नेव्हिगेशनमध्ये, **Access control (IAM)** क्लिक करा.
5. **Role assignments** टॅबमध्ये पाहा की तुमच्याकडे आधीपासूनच भूमिका आहे का:
   - तुमचे नाव किंवा ईमेल शोधा.
   - जर `Azure AI User` आधीपासून नोंदलेले असेल → त्रुटीचा कारण वेगळा आहे (कृपया खालील चरण 8 तपासा).
   - नसेल तर पुढे भूमिका जोडणे सुरू करा.
6. **+ Add** → **Add role assignment** क्लिक करा.
7. **Role** टॅबमध्ये:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) शोधा.
   - निकालांमधून निवडा.
   - **Next** क्लिक करा.
8. **Members** टॅबमध्ये:
   - **User, group, or service principal** निवडा.
   - **+ Select members** क्लिक करा.
   - तुमचे नाव किंवा ईमेल शोधा.
   - निकालांमधून स्वतःला निवडा.
   - **Select** क्लिक करा.
9. **Review + assign** → पुन्हा **Review + assign** क्लिक करा.
10. **1-2 मिनिटे थांबा** - RBAC बदल पसरायला वेळ लागतो.
11. परत अयशस्वी झालेले ऑपरेशन पुन्हा करा.

> **का Owner/Contributor पुरेसे नाहीत:** Azure RBAC मध्ये दोन प्रकारच्या परवानग्या आहेत - *management actions* आणि *data actions*. Owner आणि Contributor कडे management actions (स्रोत तयार करणे, सेटिंग्ज संपादित करणे) मिळतात, पण एजंट ऑपरेशन्ससाठी `agents/write` **data action** आवश्यक आहे, जी फक्त `Azure AI User`, `Azure AI Developer`, किंवा `Azure AI Owner` भूमिकांमध्ये असते. पाहा [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 संसाधन पुरवठा करताना `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**मूळ कारण:** तुमच्याकडे या सदस्यत्व/संसाधन गटात Azure संसाधने तयार किंवा बदल करण्याची परवानगी नाही.

**दुरुस्ती:**
1. तुमच्या सदस्यत्व प्रशासकाला सांगाअ की तुम्हाला Foundry प्रोजेक्ट असलेल्या संसाधन गटावर **Contributor** भूमिका द्यावी.
2. किंवा त्यांनी तुमच्यासाठी Foundry प्रोजेक्ट तयार करून दिला आणि प्रोजेक्टवर तुम्हाला **Azure AI User** परवानगी द्यावी.

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) साठी `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**मूळ कारण:** Azure सदस्यत्वाने Foundry साठी आवश्यक संसाधन प्रदाता नोंदणी केलेली नाही.

**दुरुस्ती:**

1. टर्मिनल उघडा आणि चालवा:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. नोंदणी पूर्ण होईपर्यंत थांबा (1-5 मिनिटे लागू शकतात):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   अपेक्षित परिणाम: `"Registered"`
3. पुन्हा ऑपरेशन प्रयत्न करा.

---

## 2. Docker त्रुटी (फक्त Docker स्थापित असल्यास)

> या कार्यशाळेसाठी Docker **ऐच्छिक** आहे. तुम्ही Docker Desktop स्थापित केला असल्यास आणि Foundry विस्तार स्थानिक कंटेनर बिल्डचा प्रयत्न करत असल्यासच या त्रुटी लागू होतात.

### 2.1 Docker डेमन चालू नाही

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**दुरुस्ती - चरणानुसार:**

1. **Start मेनूमध्ये Windows साठी किंवा Applications मध्ये macOS साठी** Docker Desktop शोधा आणि सुरू करा.
2. Docker Desktop विंडोमध्ये **"Docker Desktop is running"** दिसेपर्यंत थांबा - सामान्यतः 30-60 सेकंद लागतात.
3. तुमच्या सिस्टम ट्रे (Windows) किंवा मेनू बार (macOS) मध्ये Docker व्हेल चिन्ह शोधा. स्थितीची पुष्टी करण्यासाठी त्यावर माउस ठेवा.
4. टर्मिनलमध्ये तपासा:
   ```powershell
   docker info
   ```
   जर येथे Docker सिस्टम माहिती (Server Version, Storage Driver, इ.) दिसत असेल, तर Docker चालू आहे.
5. **Windows साठी विशेष:** Docker अजूनही सुरू होत नसेल तर:
   - Docker Desktop → **Settings** (गिअर चिन्ह) → **General** उघडा.
   - **Use the WSL 2 based engine** हा बॉक्स तपासा.
   - **Apply & restart** क्लिक करा.
   - जर WSL 2 स्थापित नसेल, तर उंचवलेल्या PowerShell मध्ये `wsl --install` चालवा आणि संगणक पुन्हा सुरू करा.
6. डिप्लॉयमेंट पुन्हा प्रयत्न करा.

### 2.2 अवलंबित्व त्रुटींसह Docker बिल्ड अयशस्वी

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**दुरुस्ती:**
1. `requirements.txt` उघडा आणि सर्व पॅकेज नावे बरोबर लिहिलेली आहेत का ते तपासा.
2. आवृत्ती पिनिंग बरोबर आहे का ते पाहा:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. स्थानिकपणे प्रथम इन्स्टॉल टेस्ट करा:
   ```bash
   pip install -r requirements.txt
   ```
4. जर खाजगी पॅकेज निर्देशिका वापरत असाल तर Docker ला त्याचा नेटवर्क प्रवेश आहे याची खात्री करा.

### 2.3 कंटेनर प्लॅटफॉर्म जुळणी नाही (Apple Silicon)

Apple Silicon Mac (M1/M2/M3/M4) वरून डिप्लॉय करत असाल, तर कंटेनर `linux/amd64` साठी बांधले पाहिजे कारण Foundry चा कंटेनर रनटाइम AMD64 वापरतो.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry विस्ताराचा डिप्लॉय कमांड बहुतेक वेळा आपोआप याची हाताळणी करतो. तुम्हाला आर्किटेक्चरशी संबंधित त्रुटी दिसल्यास `--platform` फ्लॅग वापरून हाताने बिल्ड करा आणि Foundry टीमशी संपर्क करा.

---

## 3. प्रमाणीकरण त्रुटी

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) टोकन मिळवण्यात अयशस्वी

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**मूळ कारण:** `DefaultAzureCredential` साखळीतल्या कोणत्याही क्रेडेन्शियल स्रोताला वैध टोकन नाही.

**दुरुस्ती - प्रत्येक चरण क्रमाने प्रयत्न करा:**

1. **Azure CLI द्वारे पुन्हा लॉगिन करा** (सर्वात सामान्य दुरुस्ती):
   ```bash
   az login
   ```
   एक ब्राउझर विंडो उघडेल. साइन इन करा आणि मग VS Code मध्ये परत या.

2. **योग्य सदस्यत्व सेट करा:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   जर हे योग्य सदस्यत्व नसेल तर:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code मधून पुन्हा लॉगिन करा:**
   - VS Code च्या खाली डाव्या कोपर्यातील **Accounts** चिन्ह (व्यक्ती चिन्ह) क्लिक करा.
   - तुमचे खाते नाव क्लिक करा → **Sign Out**.
   - पुन्हा Accounts चिन्ह क्लिक करा → **Sign in to Microsoft**.
   - ब्राउझर साइन-इन प्रक्रिया पूर्ण करा.

4. **सेवा प्रमुख (CI/CD परिस्थितीतच):**
   - तुमच्या `.env` मध्ये या पर्यावरणीय चल सेट करा:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - नंतर तुमचा एजंट प्रक्रिया पुन्हा सुरू करा.

5. **टोकन कॅश तपासा:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   जर हे अपयशी झाले, तर CLI टोकन कालबाह्य झाला आहे. पुन्हा `az login` करा.

### 3.2 टोकन स्थानिकपणे चालतो पण होस्टेड डिप्लॉयमेंटमध्ये नाही

**मूळ कारण:** होस्टेड एजंट एक प्रणाली-व्यवस्थापित ओळख वापरतो, जी तुमच्या वैयक्तिक क्रेडेन्शियलपेक्षा वेगळी आहे.

**दुरुस्ती:** हे अपेक्षित वर्तन आहे - व्यवस्थापित ओळख डिप्लॉयमेंटदरम्यान आपोआप पुरविली जाते. तरीही होस्टेड एजंटला प्रमाणीकरण त्रुटी येत असल्यास:
1. Foundry प्रोजेक्टच्या व्यवस्थापित ओळखेला Azure OpenAI संसाधनाचा प्रवेश दिला आहे का तपासा.
2. `agent.yaml` मधील `PROJECT_ENDPOINT` योग्य आहे का याची खात्री करा.

---

## 4. मॉडेल त्रुटी

### 4.1 मॉडेल डिप्लॉयमेंट सापडले नाही

```
Error: Model deployment not found / The specified deployment does not exist
```

**दुरुस्ती - चरणानुसार:**

1. तुमचा `.env` फाइल उघडा आणि `AZURE_AI_MODEL_DEPLOYMENT_NAME` चे मूल्य लक्षात ठेवा.
2. VS Code मध्ये **Microsoft Foundry** साइडबार उघडा.
3. तुमचा प्रोजेक्ट विस्तार करा → **Model Deployments**.
4. तिथल्या सूचीबद्ध डिप्लॉयमेंट नावाला तुमच्या `.env` मधील नावाशी तुलना करा.
5. नाव **case-sensitive** आहे - `gpt-4o` हे `GPT-4o` प्रमाणे नाही.
6. जर जुळत नसेल, तर तुमचा `.env` अचूक नावाने अपडेट करा जे साइडबारमध्ये दिसते.
7. होस्टेड डिप्लॉयमेंटसाठी, `agent.yaml` मध्ये सुद्धा अपडेट करा:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 मॉडेल अनपेक्षित सामग्रीने प्रतिसाद देते

**दुरुस्ती:**
1. `main.py` मधील `EXECUTIVE_AGENT_INSTRUCTIONS` स्थिरांक तपासा. ते कापलेले किंवा नुकसान झालेले नाही याची खात्री करा.
2. मॉडेल तापमान सेटिंग (जर कॉन्फिगर करता येत असेल) तपासा - कमी मूल्ये अधिक ठराविक आउटपुट देतात.
3. वापरलेले मॉडेल (उदा., `gpt-4o` विरुद्ध `gpt-4o-mini`) तपासा - वेगवेगळ्या मॉडेल्सचे क्षमतांचे फरक असतात.

---

## 5. डिप्लॉयमेंट त्रुटी

### 5.1 ACR पुल परवानगी

```
Error: AcrPullUnauthorized
```

**मूळ कारण:** Foundry प्रोजेक्टची व्यवस्थापित ओळख Azure कंटेनर रेजिस्ट्रीमधून कंटेनर इमेज पुल करू शकत नाही.

**दुरुस्ती - चरणानुसार:**

1. [https://portal.azure.com](https://portal.azure.com) उघडा.
2. वरच्या शोध पट्टीत **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** शोधा.
3. Foundry प्रोजेक्टशी संबंधित रेजिस्ट्री क्लिक करा (सामान्यतः तोच संसाधन गट).
4. डाव्या नेव्हिगेशनमध्ये **Access control (IAM)** क्लिक करा.
5. **+ Add** → **Add role assignment** क्लिक करा.
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** शोधा आणि निवडा. **Next** क्लिक करा.
7. **Managed identity** निवडा → **+ Select members** क्लिक करा.
8. Foundry प्रोजेक्टची व्यवस्थापित ओळख शोधा आणि निवडा.
9. **Select** → **Review + assign** → **Review + assign** क्लिक करा.

> ही भूमिका सामान्यतः Foundry विस्ताराकडून आपोआप सेट होते. ही त्रुटी दिसल्यास, स्वयंचलित सेटअप अपयशी झालेला असू शकतो. तुम्ही पुन्हा डिप्लॉय करून सुद्धा प्रयत्न करू शकता - विस्तार सेटअप पुन्हा सुरु करू शकतो.

### 5.2 एजंट डिप्लॉयमेंट नंतर सुरू होत नाही

**लक्षणे:** कंटेनर स्थिती 5 मिनिटांहून जास्त वेळ "Pending" असेल किंवा "Failed" दाखवेल.

**दुरुस्ती - चरणानुसार:**

1. VS Code मध्ये **Microsoft Foundry** साइडबार उघडा.
2. तुमचा होस्टेड एजंट क्लिक करा → आवृत्ती निवडा.
3. तपशील पॅनेलमध्ये **Container Details** तपासा → **Logs** विभाग किंवा लिंक पहा.
4. कंटेनर स्टार्टअप लॉग वाचा. सामान्य कारणे:

| लॉग संदेश | कारण | दुरुस्ती |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | आवश्यक अवलंबित्व नाही | `requirements.txt` मध्ये जोडा आणि पुन्हा डिप्लॉय करा |
| `KeyError: 'PROJECT_ENDPOINT'` | पर्यावरणीय चल गहाळ | `agent.yaml` मध्ये `env:` अंतर्गत पर्यावरणीय चल जोडा |
| `OSError: [Errno 98] Address already in use` | पोर्ट संघर्ष | `agent.yaml` मध्ये `port: 8088` सुनिश्चित करा आणि केवळ एक प्रक्रिया त्याला वापरते |
| `ConnectionRefusedError` | एजंटने ऐकणे सुरू केले नाही | `main.py` तपासा - `from_agent_framework()` कॉल स्टार्टअपवेळी चालविला पाहिजे |

5. समस्या दुरुस्त करा, मग [Module 6](06-deploy-to-foundry.md) मधून पुन्हा डिप्लॉय करा.

### 5.3 डिप्लॉयमेंट वेळ संपल्याचे

**दुरुस्ती:**
1. तुमची इंटरनेट कनेक्शन तपासा - Docker चा पुश मोठा असू शकतो (>100MB पहिल्या डिप्लॉयसाठी).
2. कॉर्पोरेट प्रॉक्सीमागे असाल तर Docker Desktop प्रॉक्सी सेटिंग्ज तपासा: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. पुन्हा प्रयत्न करा - नेटवर्क अडथळ्यांमुळे तात्पुरत्या अयशस्वी होण्याची शक्यता असते.

---

## 6. जलद संदर्भ: RBAC भूमिका

| भूमिका | सामान्य क्षेत्र | काय दिले जाते |
|---------|----------------|---------------|
| **Azure AI User** | प्रोजेक्ट | डेटा क्रिया: एजंट तयार करणे, डिप्लॉय करणे, कॉल करणे (`agents/write`, `agents/read`) |
| **Azure AI Developer** | प्रोजेक्ट किंवा खाते | डेटा क्रिया + प्रोजेक्ट तयार करणे |
| **Azure AI Owner** | खाते | संपूर्ण प्रवेश + भूमिका नियुक्ती व्यवस्थापन |
| **Azure AI Project Manager** | प्रोजेक्ट | डेटा क्रिया + Azure AI User इतरांना नियुक्त करू शकतो |
| **Contributor** | सदस्यत्व/रिसोर्स ग्रुप | व्यवस्थापन क्रिया (स्रोत तयार/हटवणे). **डेटा क्रियांचा समावेश नाही** |
| **Owner** | सदस्यत्व/रिसोर्स ग्रुप | व्यवस्थापन क्रिया + भूमिका नियुक्ती. **डेटा क्रियांचा समावेश नाही** |
| **Reader** | कुठेही | केवळ वाचन व्यवस्थापन प्रवेश |

> **महत्त्वाचा मुद्दा:** `Owner` आणि `Contributor` मध्ये डेटा क्रिया **नाहीत**. एजंट ऑपरेशन्ससाठी तुम्हाला नेहमी `Azure AI *` भूमिका हवी असते. या कार्यशाळेसाठी किमान भूमिका म्हणजे **Azure AI User** **प्रोजेक्ट** क्षेत्रावर.

---

## 7. कार्यशाळा पूर्णता तपासणी यादी

हे वापरा याची अंतिम खात्री करण्यासाठी की तुम्ही सर्व काही पूर्ण केले आहे:

| # | आयटम | मॉड्यूल | पास? |
|---|-------|---------|-------|
| 1 | सर्व पूर्वअटी स्थापित आणि पडताळणी | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit आणि Foundry विस्तार स्थापित | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry प्रोजेक्ट तयार केला (किंवा विद्यमान प्रोजेक्ट निवडला) | [02](02-create-foundry-project.md) | |
| 4 | मॉडेल तैनात केले गेले (उदा., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | प्रकल्प परिसरेवर Azure AI वापरकर्ता भूमिका नियुक्त केली | [02](02-create-foundry-project.md) | |
| 6 | होस्टेड एजंट प्रकल्प तयार केले (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` मध्ये PROJECT_ENDPOINT आणि MODEL_DEPLOYMENT_NAME कॉन्फिगर केले | [04](04-configure-and-code.md) | |
| 8 | main.py मध्ये एजंट सूचना सानुकूलित केल्या | [04](04-configure-and-code.md) | |
| 9 | वर्चुअल एन्व्हायर्नमेंट तयार केला आणि अवलंबित्वे स्थापित केली | [04](04-configure-and-code.md) | |
| 10 | एलोकलमध्ये F5 किंवा टर्मिनलसह एजंटची चाचणी केली (4 स्मोक चाचण्या उत्तीर्ण) | [05](05-test-locally.md) | |
| 11 | Foundry Agent Service मध्ये तैनात केले | [06](06-deploy-to-foundry.md) | |
| 12 | कंटेनर स्थिती "सुरू झाले" किंवा "चालू आहे" दर्शवते | [06](06-deploy-to-foundry.md) | |
| 13 | VS Code Playground मध्ये पुष्टी केली (4 स्मोक चाचण्या उत्तीर्ण) | [07](07-verify-in-playground.md) | |
| 14 | Foundry Portal Playground मध्ये पुष्टी केली (4 स्मोक चाचण्या उत्तीर्ण) | [07](07-verify-in-playground.md) | |

> **अभिनंदन!** जर सर्व आयटम तपासले गेले असतील, तर आपण संपूर्ण कार्यशाळा पूर्ण केली आहे. आपण पूर्णपणे एक होस्टेड एजंट तयार केला, स्थानिकपणे चाचणी केली, Microsoft Foundry मध्ये तैनात केला आणि उत्पादनात त्याची पुष्टी केली आहे.

---

**मागील:** [07 - Verify in Playground](07-verify-in-playground.md) · **मुखपृष्ठ:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून अनुवादित केला आहे. आम्ही अचूकतेसाठी प्रयत्नशील आहोत, परंतु कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये चुका किंवा अचूकतेच्या त्रुटी असू शकतात. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानव भाषांतर शिफारस केली जाते. या भाषांतराचा वापर करून उद्भवणाऱ्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थलहरीसाठी आम्ही जबाबदार नाही आहोत.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->