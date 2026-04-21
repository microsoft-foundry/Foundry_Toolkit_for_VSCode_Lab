# Module 8 - समस्या निवारण (मल्टी-एजंट)

हा मोड्यूल मल्टी-एजंट वर्कफ्लोशी संबंधित सामान्य चुका, दुरुस्ती आणि डीबगिंग धोरणे कव्हर करतो. सामान्य Foundry तैनातीच्या समस्या असल्यास, कृपया [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md) देखील पहा.

---

## त्वरीत संदर्भ: त्रुटी → दुरुस्ती

| त्रुटी / लक्षण | संभाव्य कारण | दुरुस्ती |
|----------------|--------------|----------|
| `RuntimeError: Missing required environment variable(s)` | `.env` फाइल गायब किंवा मूल्ये सेट नसलेली | `.env` तयार करा ज्यात `PROJECT_ENDPOINT=<your-endpoint>` आणि `MODEL_DEPLOYMENT_NAME=<your-model>` असेल |
| `ModuleNotFoundError: No module named 'agent_framework'` | व्हर्च्युअल एन्व्हायरनमेंट सक्रिय नाही किंवा अवलंबित्वे इंस्टॉल केलेली नाहीत | `.\.venv\Scripts\Activate.ps1` चालवा, नंतर `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP पॅकेज इंस्टॉल केलेले नाही (requirements मध्ये नाही) | `pip install mcp` चालवा किंवा `requirements.txt` मध्ये ते ट्रांझिटिव्ह अवलंबित्व म्हणून आहे का तपासा |
| एजंट चालू होतो पण रिकामा प्रतिसाद देतो | `output_executors` जुळत नाही किंवा एजेस गायब | `output_executors=[gap_analyzer]` आहे का तपासा आणि `create_workflow()` मधील सर्व एजेस अस्तित्वात आहेत का तपासा |
| फक्त १ gap कार्ड आहे (इतर गायब) | GapAnalyzer सूचना अपूर्ण | `GAP_ANALYZER_INSTRUCTIONS` मध्ये `CRITICAL:` परिच्छेद जोडा - बघा [Module 3](03-configure-agents.md) |
| फिट स्कोर 0 किंवा अनुपस्थित आहे | MatchingAgent ला अपस्ट्रीम डेटा मिळालेला नाही | `add_edge(resume_parser, matching_agent)` आणि `add_edge(jd_agent, matching_agent)` अस्तित्वात आहेत का तपासा |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP सर्व्हरने टूल कॉल नाकारला | इंटरनेट कनेक्टिव्हिटी तपासा. ब्राउझरमध्ये `https://learn.microsoft.com/api/mcp` उघडण्याचा प्रयत्न करा. पुन्हा प्रयत्न करा |
| आउटपुटमध्ये Microsoft Learn URLs नाहीत | MCP टूल नोंदणीकृत नाही किंवा एंडपॉइंट चुकीचा | GapAnalyzer मध्ये `tools=[search_microsoft_learn_for_plan]` आहे का तपासा आणि `MICROSOFT_LEARN_MCP_ENDPOINT` बरोबर आहे का तपासा |
| `Address already in use: port 8088` | दुसरा प्रोसेस पोर्ट 8088 वापरत आहे | `netstat -ano \| findstr :8088` (Windows) किंवा `lsof -i :8088` (macOS/Linux) चालवा आणि विरोधी प्रोसेस थांबवा |
| `Address already in use: port 5679` | Debugpy पोर्ट संघर्ष | इतर डिबग सत्र बंद करा. `netstat -ano \| findstr :5679` चालवा आणि प्रक्रिया शोधून बंद करा |
| एजंट इन्स्पेक्टर उघडत नाही | सर्व्हर पूर्णपणे सुरु नाही किंवा पोर्ट संघर्ष | "Server running" लॉगची प्रतीक्षा करा. पोर्ट 5679 मोकळा आहे का तपासा |
| `azure.identity.CredentialUnavailableError` | Azure CLI मध्ये साइन इन केलेलं नाही | `az login` चालवा, नंतर सर्व्हर रीस्टार्ट करा |
| `azure.core.exceptions.ResourceNotFoundError` | मॉडेल तैनात केलेला नाही | `MODEL_DEPLOYMENT_NAME` तुमच्या Foundry प्रोजेक्टमधील तैनात मॉडेलशी जुळत आहे का तपासा |
| कंटेनर स्थिती तैनाती नंतर "Failed" आहे | कंटेनर सुरुवातीला क्रॅश झाला | Foundry साइडबारमधील कंटेनर लॉग्स तपासा. सर्वसाधारण: env var गायब किंवा आयात त्रुटी |
| तैनाती "Pending" > 5 मिनिटे दाखवते | कंटेनरला सुरु होण्यात जास्त वेळ लागत आहे किंवा रिसोर्स मर्यादा | मल्टी-एजंटसाठी 5 मिनिटे वाट पाहा (हे 4 एजंट इंस्टन्स तयार करते). अजूनही पेंडिंग असल्यास लॉग तपासा |
| `ValueError` `WorkflowBuilder` कडून | अवैध ग्राफ कॉन्फिगरेशन | `start_executor` सेट आहे का, `output_executors` यादी आहे का, आणि सर्क्युलर एजेस नाहीत का ते सुनिश्चित करा |

---

## पर्यावरण आणि कॉन्फिगरेशन समस्या

### गायब किंवा चुकीची `.env` मूल्ये

`.env` फाइल `PersonalCareerCopilot/` डिरेक्टरीमध्ये असावी (जिथे `main.py` आहे):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

अपेक्षित `.env` सामग्री:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **तुमचा PROJECT_ENDPOINT कसा शोधाल:**  
- VS Code मधील **Microsoft Foundry** साइडबार उघडा → तुमच्या प्रोजेक्टवर राइट-क्लिक करा → **Copy Project Endpoint**.  
- अथवा [Azure Portal](https://portal.azure.com) → तुमचा Foundry प्रोजेक्ट → **Overview** → **Project endpoint**.

> **तुमचा MODEL_DEPLOYMENT_NAME कसा शोधाल:** Foundry साइडबारमध्ये प्रोजेक्ट विस्तृत करा → **Models** → तैनात मॉडेल नाव शोधा (उदा. `gpt-4.1-mini`).

### Env var प्राधान्यक्रम

`main.py` मध्ये `load_dotenv(override=False)` वापरले आहे, म्हणजे:

| प्राधान्यक्रम | स्रोत | दोन्ही सेट असतील तर कोण जिंकतो? |
|---------------|--------|-------------------------------|
| 1 (सर्वोच्च) | शेल एन्व्हायरनमेंट व्हरिएबल | होय |
| 2 | `.env` फाइल | फक्त जर शेल व्हरिएबल सेट केलेले नसेल तर |

म्हणजे Foundry रनटाइम एन्व्हायरनमेंट व्हरिएबल (`agent.yaml` द्वारे सेट) हा `.env` मधील मूल्यांवर तैनाती दरम्यान प्राधान्य आहे.

---

## आवृत्ती सुसंगतता

### पॅकेज आवृत्ती मॅट्रिक्स

मल्टी-एजंट वर्कफ्लोला विशिष्ट पॅकेज आवृत्त्या लागतात. जुळत नसलेल्या आवृत्त्यांमुळे रनटाइम त्रुटी होतात.

| पॅकेज | आवश्यक आवृत्ती | तपासणी कमांड |
|---------|------------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | नवीनतम प्री-रिलीज | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### सामान्य आवृत्ती त्रुटी

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# दुरुस्ती: rc3 कडे अद्ययावत करा
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` सापडले नाही किंवा Inspector असंगत:**

```powershell
# दुरुस्ती: --pre ध्वजासह इंस्टॉल करा
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# दुरुस्त करा: mcp पॅकेजचे आवृत्ती सुधारित करा
pip install mcp --upgrade
```

### सर्व आवृत्त्या एकत्र तपासा

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

अपेक्षित आउटपुट:

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

## MCP टूल समस्या

### MCP टूल परिणाम देत नाही

**लक्षण:** Gap कार्ड्स मध्ये "No results returned from Microsoft Learn MCP" किंवा "No direct Microsoft Learn results found" असं दिसतं.

**संभाव्य कारणे:**

1. **नेटवर्क समस्या** - MCP एंडपॉइंट (`https://learn.microsoft.com/api/mcp`) उपलब्ध नाही.
   ```powershell
   # कनेक्टिव्हिटी चाचणी करा
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   जर `200` रिटर्न झाला, तर एंडपॉइंट पोहोचू शकतो.

2. **शोध प्रश्न खूप विशिष्ट** - कौशल्य नांव Microsoft Learn साठी खूप निघाईल.
   - अत्यंत विशेषज्ञ कौशल्यांसाठी हे अपेक्षित आहे. टूल प्रतिसादात फॉलबॅक URL देतो.

3. **MCP सत्र वेळ संपला** - स्ट्रीमेबल HTTP कनेक्शन वेळ संपली.
   - पुन्हा प्रयत्न करा. MCP सत्र लवकर संपणारे असतात आणि पुन्हा कनेक्ट करावे लागू शकते.

### MCP लॉग समजावून सांगणे

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| लॉग | अर्थ | कृती |
|-----|-------|-------|
| `GET → 405` | MCP क्लायंट इनिशियलायझेशन दरम्यान तपासणी | सामान्य - दुर्लक्षित करा |
| `POST → 200` | टूल कॉल यशस्वी | अपेक्षित |
| `DELETE → 405` | MCP क्लायंट क्लिनअप दरम्यान तपासणी | सामान्य - दुर्लक्षित करा |
| `POST → 400` | वाईट विनंती (अयोग्य क्वेरी) | `search_microsoft_learn_for_plan()` मधील `query` पॅरामीटर तपासा |
| `POST → 429` | रेट लिमिट | थांबा आणि पुन्हा प्रयत्न करा. `max_results` कमी करा |
| `POST → 500` | MCP सर्व्हर चूक | तात्पुरती - पुन्हा प्रयत्न करा. दीर्घकालीन असल्यास Microsoft Learn MCP API डाउन असू शकते |
| कनेक्शन टाइमआउट | नेटवर्क समस्या किंवा MCP सर्व्हर अनुपलब्ध | इंटरनेट तपासा. `curl https://learn.microsoft.com/api/mcp` चालवा |

---

## तैनातीच्या समस्या

### तैनाती नंतर कंटेनर सुरु होत नाही

1. **कंटेनर लॉग्स तपासा:**
   - **Microsoft Foundry** साइडबार उघडा → **Hosted Agents (Preview)** विस्तृत करा → तुमचा एजंट क्लिक करा → आवृत्ती विस्तृत करा → **Container Details** → **Logs**.
   - Python स्टॅक ट्रेसेस किंवा मॉड्यूल नसण्याच्या त्रुटी पहा.

2. **सामान्य कंटेनर सुरुवात चुकाः**

   | लॉगमधील त्रुटी | कारण | दुरुस्ती |
   |----------------|--------|----------|
   | `ModuleNotFoundError` | `requirements.txt` मध्ये पॅकेज गायब | पॅकेज जोडा, पुन्हा तैनात करा |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` मध्ये env vars सेट नाहीत | `agent.yaml` मधील `environment_variables` विभाग अद्ययावत करा |
   | `azure.identity.CredentialUnavailableError` | Managed Identity कॉन्फिगर केलेलं नाही | Foundry हे आपोआप सेट करते - विस्तार वापरून तैनात करत असल्याची खात्री करा |
   | `OSError: port 8088 already in use` | Dockerfile चुकीचा पोर्ट उघडतो किंवा पोर्ट संघर्ष | Dockerfile मध्ये `EXPOSE 8088` आणि `CMD ["python", "main.py"]` तपासा |
   | कंटेनर कोड 1 ने थांबतो | `main()` मध्ये अनहँडल त्रुटी | स्थानिकपणे प्रथम चाचणी करा ([Module 5](05-test-locally.md)) म्हणजे त्रुटी कॅच करता येतील |

3. **दुरुस्ती नंतर पुन्हा तैनात करा:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → तेच एजंट निवडा → नवीन आवृत्ती तैनात करा.

### तैनातीसाठी जास्त वेळ लागू लागतो

मल्टी-एजंट कंटेनर्स सुरुवात करताना 4 एजंट इंस्टन्स तयार करतात, त्यामुळे वेळ वाढतो. सामान्य सुरुवातीचा वेळ:

| टप्पा | अपेक्षित वेळ |
|--------|-------------|
| कंटेनर इमेज बिल्ड | 1-3 मिनिटे |
| ACR वर इमेज पुश | 30-60 सेकंद |
| कंटेनर सुरु (सिंगल एजंट) | 15-30 सेकंद |
| कंटेनर सुरु (मल्टी-एजंट) | 30-120 सेकंद |
| "Started" नंतर Playground मध्ये एजंट उपलब्ध | 1-2 मिनिटे |

> जर "Pending" स्टेटस 5 मिनिटांपेक्षा जास्त राहिला, कंटेनर लॉग्स तपासा.

---

## RBAC आणि परवानगी समस्या

### `403 Forbidden` किंवा `AuthorizationFailed`

तुमच्या Foundry प्रोजेक्टवर तुमच्याकडे **[Azure AI User](https://aka.ms/foundry-ext-project-role)** भूमिका असायला हवी:

1. [Azure Portal](https://portal.azure.com) → तुमचा Foundry **प्रोजेक्ट** रिसोर्स उघडा.
2. **Access control (IAM)** → **Role assignments** क्लिक करा.
3. तुमचं नाव शोधा → खात्री करा की **Azure AI User** यादीत आहे.
4. जर नसेल: **Add** → **Add role assignment** → **Azure AI User** शोधा → तुमच्या खात्यावर नियुक्त करा.

[Microsoft Foundry साठी RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) दस्तऐवज पहा.

### मॉडेल तैनाती उपलब्ध नाही

जर एजंट मॉडेल संबंधी त्रुटी दर्शवत असेल:

1. मॉडेल तैनात केले आहे का तपासा: Foundry साइडबार → प्रोजेक्ट विस्तार करा → **Models** → `gpt-4.1-mini` (किंवा तुमचा मॉडेल) स्थिती **Succeeded** आहे का पहा.
2. तैनाती नाव जुळत आहे का तपासा: `.env` (किंवा `agent.yaml`) मधील `MODEL_DEPLOYMENT_NAME` आणि साइडबारमधील प्रत्यक्ष तैनाती नाव याची तुलना करा.
3. जर तैनाती कालबाह्य झाली असेल (मुक्त स्तरात): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) मधून पुन्हा तैनात करा (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## एजंट इन्स्पेक्टर समस्या

### इन्स्पेक्टर उघडतो पण "Disconnected" दाखवतो

1. सर्व्हर चालू आहे का तपासा: टर्मिनलमध्ये "Server running on http://localhost:8088" शोधा.
2. पोर्ट `5679` तपासा: इन्स्पेक्टर debugpy वापरून या पोर्टवर जोडतो.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. सर्व्हर रीस्टार्ट करा आणि इन्स्पेक्टर पुन्हा उघडा.

### इन्स्पेक्टर अंशतः प्रतिसाद दाखवतो

मल्टी-एजंट प्रतिसाद लांबट आणि स्ट्रीमिंग प्रकारे येतात. संपूर्ण प्रतिसाद पूर्ण होईपर्यंत थांबा (gap कार्ड्स आणि MCP टूल कॉलच्या संख्येनुसार 30-60 सेकंद लागू शकतात).

जर प्रतिसाद नियमितपणे फुटलेला असेल:
- GapAnalyzer सूचनांमध्ये `CRITICAL:` ब्लॉक आहे का तपासा जो gap कार्ड्स एकत्र होण्यापासून प्रतिबंधित करतो.
- तुमच्या मॉडेलच्या टोकन लिमिटची तपासणी करा - `gpt-4.1-mini` पर्यंत 32K आउटपुट टोकन्स समर्थित आहे, जी पुरेशी आहे.

---

## कामगिरी टिपा

### प्रतिसाद मंदी

मल्टी-एजंट वर्कफ्लो सिंगल एजंट पेक्षा नैसर्गिकतः मंद असतो कारण अनुक्रमिक अवलंबित्वे आणि MCP टूल कॉल्स आहेत.

| ऑप्टिमायझेशन | कसे | परिणाम |
|----------------|-------|---------|
| MCP कॉल कमी करा | टूलमध्ये `max_results` पॅरामीटर कमी करा | HTTP राउंड-ट्रिप्स कमी होतात |
| सूचना सोपा करा | एजंट प्रॉम्प्ट शॉर्ट आणि लक्ष केंद्रीत करा | LLM इन्फरन्स वेगवान होतो |
| `gpt-4.1-mini` वापरा | विकासासाठी `gpt-4.1` पेक्षा जलद | सुमारे 2 पट वेगवान |
| gap कार्ड तपशील कमी करा | GapAnalyzer सूचनांमधील gap कार्ड स्वरूप सोपे करा | आउटपुट निर्माण कमी |

### साधारण प्रतिसाद वेळा (स्थानीय)

| कॉन्फिगरेशन | अपेक्षित वेळ |
|--------------|-------------|
| `gpt-4.1-mini`, 3-5 gap कार्ड्स | 30-60 सेकंद |
| `gpt-4.1-mini`, 8+ gap कार्ड्स | 60-120 सेकंद |
| `gpt-4.1`, 3-5 gap कार्ड्स | 60-120 सेकंद |
---

## मदत घेणे

वरील दुरुस्त्या करूनही अडचण येत असल्यास:

1. **सर्व्हर लॉग तपासा** - बहुतेक त्रुटी टर्मिनलमध्ये Python स्टॅक ट्रेस निर्माण करतात. संपूर्ण ट्रेसबॅक वाचा.
2. **त्रुटी संदेश शोधा** - त्रुटीचा मजकूर कॉपी करा आणि [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) मध्ये शोधा.
3. **इश्यू उघडा** - [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) वर इश्यू द्या ज्यामध्ये:
   - त्रुटीचा संदेश किंवा स्क्रीनशॉट
   - तुमची पॅकेज आवृत्त्या (`pip list | Select-String "agent-framework"`)
   - तुमची Python आवृत्ती (`python --version`)
   - ही समस्या स्थानिक आहे की डिप्लॉयमेंट नंतर

---

### चेकपॉइंट

- [ ] तुम्ही जलद संदर्भ तक्त्यासह सर्वसाधारण बहुऐजेंट त्रुटी ओळखू व दुरुस्त करू शकता
- [ ] `.env` कॉन्फिगरेशन समस्या कशी तपासायची व दुरुस्त करायची हे तुम्हाला माहीत आहे
- [ ] तुम्ही पॅकेज आवृत्त्या आवश्यक मॅट्रिक्सशी जुळतात याची पुष्टी करू शकता
- [ ] तुम्हाला MCP लॉग नोंदी समजतात व टूल खराबीचे निदान करू शकता
- [ ] तुम्हाला डिप्लॉयमेंट अयशस्वी झाल्यास कंटेनर लॉग कसे तपासायचे हे माहीत आहे
- [ ] तुम्ही Azure Portal मध्ये RBAC भूमिका तपासू शकता

---

**पूर्वीचे:** [07 - Verify in Playground](07-verify-in-playground.md) · **मुख्य पान:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:  
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित करण्यात आला आहे. आम्ही अचूकतेसाठी प्रयत्नशील आहोत, तरी कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये त्रुटी किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्त्रोत मानावा. महत्त्वपूर्ण माहितीसाठी व्यावसायिक मानवी अनुवाद करण्याची शिफारस केली जाते. या अनुवादाचा वापर केल्यामुळे झालेल्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थसंग्रहासाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->