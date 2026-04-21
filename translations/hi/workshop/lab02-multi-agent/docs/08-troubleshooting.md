# मॉड्यूल 8 - समस्या निवारण (मल्टी-एजेंट)

यह मॉड्यूल मल्टी-एजेंट वर्कफ़्लो से संबंधित सामान्य त्रुटियाँ, सुधार और डिबगिंग रणनीतियों को कवर करता है। सामान्य Foundry डिप्लॉयमेंट समस्याओं के लिए, [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md) भी देखें।

---

## त्वरित संदर्भ: त्रुटि → सुधार

| त्रुटि / लक्षण | संभावित कारण | सुधार |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` फ़ाइल गायब है या मान सेट नहीं हैं | `.env` फ़ाइल बनाएँ जिसमें `PROJECT_ENDPOINT=<your-endpoint>` और `MODEL_DEPLOYMENT_NAME=<your-model>` हो |
| `ModuleNotFoundError: No module named 'agent_framework'` | वर्चुअल वातावरण सक्रिय नहीं है या निर्भरताएँ इंस्टॉल नहीं हुई हैं | चलाएँ `.\.venv\Scripts\Activate.ps1` फिर `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP पैकेज इंस्टॉल नहीं है (requirements में नहीं है) | चलाएँ `pip install mcp` या `requirements.txt` में इसकी ट्रांजिटिव डिपेंडेंसी जांचें |
| एजेंट शुरू होता है लेकिन खाली प्रतिक्रिया देता है | `output_executors` असंगत या एजेस गायब हैं | सत्यापित करें कि `output_executors=[gap_analyzer]` है और `create_workflow()` में सभी एजेस मौजूद हैं |
| केवल 1 गैप कार्ड (बाकी गायब) | GapAnalyzer निर्देश अधूरे हैं | `GAP_ANALYZER_INSTRUCTIONS` में `CRITICAL:` पैराग्राफ जोड़ें - देखें [मॉड्यूल 3](03-configure-agents.md) |
| फिट स्कोर 0 या अनुपस्थित है | MatchingAgent को अपर स्ट्रीम डेटा नहीं मिला | सत्यापित करें कि `add_edge(resume_parser, matching_agent)` और `add_edge(jd_agent, matching_agent)` दोनों हैं |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP सर्वर ने टूल कॉल को अस्वीकार किया | इंटरनेट कनेक्टिविटी जांचें। ब्राउज़र में `https://learn.microsoft.com/api/mcp` खोलने की कोशिश करें। पुनः प्रयास करें |
| आउटपुट में कोई Microsoft Learn URL नहीं | MCP टूल पंजीकृत नहीं है या एंडपॉइंट गलत है | सत्यापित करें `tools=[search_microsoft_learn_for_plan]` GapAnalyzer पर और `MICROSOFT_LEARN_MCP_ENDPOINT` सही है |
| `Address already in use: port 8088` | कोई अन्य प्रक्रिया पोर्ट 8088 का उपयोग कर रही है | चलाएँ `netstat -ano \| findstr :8088` (Windows) या `lsof -i :8088` (macOS/Linux) और टकराव वाली प्रक्रिया बंद करें |
| `Address already in use: port 5679` | Debugpy पोर्ट टकराव | अन्य डिबग सेशन बंद करें। चलाएँ `netstat -ano \| findstr :5679` प्रक्रिया खोजने और खत्म करने के लिए |
| Agent Inspector नहीं खुलता | सर्वर पूरी तरह से शुरू नहीं हुआ है या पोर्ट टकराव | "Server running" लॉग का इंतजार करें। जांचें कि पोर्ट 5679 खाली है |
| `azure.identity.CredentialUnavailableError` | Azure CLI में साइन इन नहीं किया गया | चलाएँ `az login` फिर सर्वर पुनः शुरू करें |
| `azure.core.exceptions.ResourceNotFoundError` | मॉडल डिप्लॉयमेंट मौजूद नहीं है | जांचें कि `MODEL_DEPLOYMENT_NAME` आपके Foundry प्रोजेक्ट में डिप्लॉय किए मॉडल से मेल खाता है |
| कंटेनर स्टेटस "Failed" डिप्लॉयमेंट के बाद | स्टार्टअप पर कंटेनर क्रैश हुआ | Foundry साइडबार में कंटेनर लॉग्स जांचें। सामान्य: env var गायब या इम्पोर्ट त्रुटि |
| डिप्लॉयमेंट "Pending" 5 मिनट से अधिक दिखाता है | कंटेनर को शुरू होने में अधिक समय लग रहा है या संसाधन सीमाएँ | मल्टी-एजेंट के लिए 5 मिनट तक प्रतीक्षा करें (4 एजेंट इंस्टेंस बनाता है)। फिर भी पेंडिंग हो तो लॉग देखें |
| `ValueError` from `WorkflowBuilder` | अमान्य ग्राफ कॉन्फ़िगरेशन | सुनिश्चित करें कि `start_executor` सेट है, `output_executors` सूची है, और कोई सर्कुलर एज नहीं है |

---

## पर्यावरण और कॉन्फ़िगरेशन समस्याएं

### `.env` मान गायब या गलत

`.env` फ़ाइल `PersonalCareerCopilot/` डायरेक्टरी में होनी चाहिए (main.py के समान स्तर):

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

> **अपना PROJECT_ENDPOINT खोजें:**  
- VS Code में **Microsoft Foundry** साइडबार खोलें → अपने प्रोजेक्ट पर राइट-क्लिक करें → **Copy Project Endpoint**।  
- या [Azure Portal](https://portal.azure.com) जाएँ → अपना Foundry प्रोजेक्ट → **Overview** → **Project endpoint**।

> **अपना MODEL_DEPLOYMENT_NAME खोजें:** Foundry साइडबार में अपने प्रोजेक्ट को विस्तृत करें → **Models** → अपना डिप्लॉय किया गया मॉडल नाम खोजें (जैसे, `gpt-4.1-mini`)।

### Env var प्राथमिकता

`main.py` में `load_dotenv(override=False)` उपयोग होता है, जिसका मतलब है:

| प्राथमिकता | स्रोत | जब दोनों सेट हों तो कौन जीते? |
|----------|--------|------------------------|
| 1 (सबसे उच्च) | शेल पर्यावरण चर | हाँ |
| 2 | `.env` फ़ाइल | जब तक शेल चर सेट न हो |

इसका मतलब है कि Foundry रनटाइम env vars (`agent.yaml` के माध्यम से सेट) होस्टेड डिप्लॉयमेंट के दौरान `.env` मानों से प्राथमिक होते हैं।

---

## संस्करण संगतता

### पैकेज संस्करण मैट्रिक्स

मल्टी-एजेंट वर्कफ़्लो को विशिष्ट पैकेज संस्करणों की आवश्यकता होती है। मेल न खाने वाले संस्करण रनटाइम त्रुटियाँ उत्पन्न करते हैं।

| पैकेज | आवश्यक संस्करण | जांच कमांड |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | नवीनतम प्री-रिलीज़ | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### सामान्य संस्करण त्रुटियाँ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# सुधार: rc3 में अपग्रेड करें
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` नहीं मिला या Inspector असंगत:**

```powershell
# सुधारें: --pre फ्लैग के साथ इंस्टॉल करें
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# सुधारें: mcp पैकेज को अपग्रेड करें
pip install mcp --upgrade
```

### सभी संस्करण एक साथ जांचें

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

## MCP टूल समस्याएं

### MCP टूल कोई परिणाम नहीं देता

**लक्षण:** गैप कार्ड कहते हैं "No results returned from Microsoft Learn MCP" या "No direct Microsoft Learn results found"।

**संभावित कारण:**

1. **नेटवर्क समस्या** - MCP एंडपॉइंट (`https://learn.microsoft.com/api/mcp`) पहुंच योग्य नहीं है।  
   ```powershell
   # कनेक्टिविटी का परीक्षण करें
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
 यदि यह `200` लौटाता है, तो एंडपॉइंट पहुंच योग्य है।

2. **क्वेरी बहुत विशिष्ट है** - कौशल नाम Microsoft Learn खोज के लिए बहुत निच है।  
   - यह बहुत विशिष्ट कौशलों के लिए अपेक्षित है। टूल के उत्तर में एक फॉलबैक URL भी होता है।

3. **MCP सत्र टाइमआउट** - Streamable HTTP कनेक्शन का टाइमआउट हो गया।  
   - अनुरोध पुनः प्रयास करें। MCP सत्र क्षणिक होते हैं और पुनः कनेक्शन की आवश्यकता हो सकती है।

### MCP लॉग्स की व्याख्या

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| लॉग | अर्थ | क्रिया |
|-----|---------|--------|
| `GET → 405` | MCP क्लाइंट प्रारंभिक जांच | सामान्य - उपेक्षा करें |
| `POST → 200` | टूल कॉल सफल | अपेक्षित |
| `DELETE → 405` | MCP क्लाइंट सफाई जांच | सामान्य - उपेक्षा करें |
| `POST → 400` | खराब अनुरोध (गलत क्वेरी) | `search_microsoft_learn_for_plan()` में `query` पैरामीटर जांचें |
| `POST → 429` | रेट लिमिट | प्रतीक्षा करें और पुनः प्रयास करें। `max_results` कम करें |
| `POST → 500` | MCP सर्वर त्रुटि | अस्थायी - पुनः प्रयास करें। अगर बनी रहे, तो Microsoft Learn MCP API डाउन हो सकती है |
| कनेक्शन टाइमआउट | नेटवर्क समस्या या MCP सर्वर अनुपलब्ध | इंटरनेट जांचें। चलाएँ `curl https://learn.microsoft.com/api/mcp` |

---

## डिप्लॉयमेंट समस्याएं

### डिप्लॉयमेंट के बाद कंटेनर शुरू नहीं होता

1. **कंटेनर लॉग्स जांचें:**
   - **Microsoft Foundry** साइडबार खोलें → **Hosted Agents (Preview)** विस्तृत करें → अपने एजेंट पर क्लिक करें → संस्करण विस्तृत करें → **Container Details** → **Logs**।
   - Python स्टैक ट्रेस या मॉड्यूल गायब त्रुटि देखें।

2. **सामान्य कंटेनर स्टार्टअप विफलताएं:**

   | लॉग में त्रुटि | कारण | सुधार |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` में पैकेज नहीं | पैकेज जोड़ें, पुनः डिप्लॉय करें |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` में env vars सेट नहीं हैं | `agent.yaml` के `environment_variables` सेक्शन को अपडेट करें |
   | `azure.identity.CredentialUnavailableError` | Managed Identity कॉन्फ़िगर नहीं | Foundry यह स्वचालित सेट करता है - सुनिश्चित करें कि एक्सटेंशन से डिप्लॉय हो रहा है |
   | `OSError: port 8088 already in use` | Dockerfile गलत पोर्ट एक्सपोज़ करता है या पोर्ट टकराव | Dockerfile में `EXPOSE 8088` और `CMD ["python", "main.py"]` जांचें |
   | कंटेनर कोड 1 के साथ बंद | `main()` में अप्रबंधित अपवाद | पहले लोकल में टेस्ट करें ([मॉड्यूल 5](05-test-locally.md)) ताकि डिप्लॉय से पहले त्रुटियां पकड़ सकें |

3. **सुधार के बाद पुनः डिप्लॉय करें:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → वही एजेंट चुनें → नया संस्करण डिप्लॉय करें।

### डिप्लॉयमेंट में बहुत समय लगना

मल्टी-एजेंट कंटेनर शुरू होने में अधिक समय लेते हैं क्योंकि वे स्टार्टअप पर 4 एजेंट इंस्टेंस बनाते हैं। सामान्य स्टार्टअप समय:

| चरण | अपेक्षित अवधि |
|-------|------------------|
| कंटेनर इमेज बिल्ड | 1-3 मिनट |
| इमेज को ACR में पुश करना | 30-60 सेकंड |
| कंटेनर स्टार्ट (सिंगल एजेंट) | 15-30 सेकंड |
| कंटेनर स्टार्ट (मल्टी-एजेंट) | 30-120 सेकंड |
| एजेंट Playground में उपलब्ध | "Started" के 1-2 मिनट बाद |

> अगर "Pending" स्थिति 5 मिनट से अधिक रहती है, तो कंटेनर लॉग्स में त्रुटियाँ जांचें।

---

## RBAC और अनुमतियाँ समस्याएं

### `403 Forbidden` या `AuthorizationFailed`

आपके Foundry प्रोजेक्ट पर **[Azure AI User](https://aka.ms/foundry-ext-project-role)** भूमिका आवश्यक है:

1. [Azure Portal](https://portal.azure.com) पर जाएं → अपने Foundry **प्रोजेक्ट** संसाधन पर क्लिक करें।
2. **Access control (IAM)** → **Role assignments** पर क्लिक करें।
3. अपना नाम खोजें → पुष्टि करें कि **Azure AI User** सूचीबद्ध है।
4. यदि नहीं है: **Add** → **Add role assignment** → **Azure AI User** खोजें → अपने खाते को असाइन करें।

विस्तार के लिए [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) दस्तावेज़ देखें।

### मॉडल डिप्लॉयमेंट सुलभ नहीं

अगर एजेंट मॉडल संबंधित त्रुटियाँ देता है:

1. सत्यापित करें कि मॉडल डिप्लॉय किया गया है: Foundry साइडबार → प्रोजेक्ट विस्तृत करें → **Models** → `gpt-4.1-mini` (या आपका मॉडल) के साथ स्थिति **Succeeded** देखें।
2. डिप्लॉयमेंट नाम मेल खाता है: `.env` (या `agent.yaml`) में `MODEL_DEPLOYMENT_NAME` को साइडबार में वास्तविक डिप्लॉयमेंट नाम से मिलाएं।
3. अगर डिप्लॉयमेंट एक्सपायर हो गया है (फ्री Tier): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) से पुनः डिप्लॉय करें (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)।

---

## Agent Inspector समस्याएं

### Inspector खुलता है लेकिन "Disconnected" दिखाता है

1. सत्यापित करें सर्वर चल रहा है: टर्मिनल में "Server running on http://localhost:8088" देखें।
2. पोर्ट `5679` जांचें: Inspector debugpy पोर्ट 5679 पर कनेक्ट करता है।  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. सर्वर पुनः शुरू करें और Inspector फिर से खोलें।

### Inspector आंशिक प्रतिक्रिया दिखाता है

मल्टी-एजेंट प्रतिक्रियाएँ लंबी होती हैं और क्रमशः स्ट्रीम होती हैं। पूर्ण प्रतिक्रिया के लिए प्रतीक्षा करें (30-60 सेकंड तक लग सकते हैं, गैप कार्ड और MCP टूल कॉल की संख्या पर निर्भर करता है)।

यदि प्रतिक्रिया लगातार अधूरी रहती है:  
- जांचें कि GapAnalyzer निर्देशों में `CRITICAL:` ब्लॉक है जो गैप कार्ड को संयोजित होने से रोकता है।  
- अपने मॉडल के टोकन सीमा जांचें - `gpt-4.1-mini` 32K आउटपुट टोकन तक समर्थित है, जो पर्याप्त होना चाहिए।

---

## प्रदर्शन सुझाव

### धीमी प्रतिक्रियाएँ

मल्टी-एजेंट वर्कफ़्लोज़ स्वाभाविक रूप से सिंगल-एजेंट से धीमे होते हैं क्योंकि इनमें अनुक्रमिक निर्भरता और MCP टूल कॉल होते हैं।

| अनुकूलन | कैसे | प्रभाव |
|-------------|-----|--------|
| MCP कॉल्स कम करें | टूल में `max_results` पैरामीटर कम करें | HTTP राउंड-ट्रिप्स घटेंगे |
| निर्देश सरल करें | एजेंट प्रॉम्प्ट को छोटा और लक्षित करें | तेज LLM अभिव्यक्ति |
| `gpt-4.1-mini` का उपयोग करें | विकास के लिए `gpt-4.1` से तेज़ | लगभग 2x गति वृद्धि |
| गैप कार्ड विवरण कम करें | GapAnalyzer निर्देशों में गैप कार्ड फॉर्मेट सरल करें | आउटपुट उत्पादन कम होगा |

### सामान्य प्रतिक्रिया समय (लोकल)

| कॉन्फ़िगरेशन | अपेक्षित समय |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 गैप कार्ड | 30-60 सेकंड |
| `gpt-4.1-mini`, 8+ गैप कार्ड | 60-120 सेकंड |
| `gpt-4.1`, 3-5 गैप कार्ड | 60-120 सेकंड |
---

## सहायता प्राप्त करना

यदि उपरोक्त सुधारों को आजमाने के बाद आप फंस गए हैं:

1. **सर्वर लॉग जांचें** - अधिकांश त्रुटियां टर्मिनल में एक Python स्टैक ट्रेस उत्पन्न करती हैं। पूर्ण ट्रेसबैक पढ़ें।
2. **त्रुटि संदेश खोजें** - त्रुटि टेक्स्ट को कॉपी करें और [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) में खोजें।
3. **एक मुद्दा खोलें** - [वर्कशॉप रिपॉजिटरी](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) पर एक मुद्दा दर्ज करें जिसमें शामिल हो:
   - त्रुटि संदेश या स्क्रीनशॉट
   - आपके पैकेज संस्करण (`pip list | Select-String "agent-framework"`)
   - आपका Python संस्करण (`python --version`)
   - क्या समस्या स्थानीय है या परिनियोजन के बाद

---

### चेकपॉइंट

- [ ] आप त्वरित संदर्भ तालिका का उपयोग करके सबसे सामान्य मल्टी-एजेंट त्रुटियों की पहचान और सुधार कर सकते हैं
- [ ] आप जानते हैं कि `.env` कॉन्फ़िगरेशन समस्याओं को कैसे जांचें और सुधारें
- [ ] आप सत्यापित कर सकते हैं कि पैकेज संस्करण आवश्यक मैट्रिक्स से मेल खाते हैं
- [ ] आप MCP लॉग प्रविष्टियों को समझते हैं और टूल विफलताओं का निदान कर सकते हैं
- [ ] आप परिनियोजन विफलताओं के लिए कंटेनर लॉग जांचना जानते हैं
- [ ] आप Azure पोर्टल में RBAC भूमिकाओं को सत्यापित कर सकते हैं

---

**पिछला:** [07 - Verify in Playground](07-verify-in-playground.md) · **होम:** [Lab 02 README](../README.md) · [वर्कशॉप होम](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:  
इस दस्तावेज़ का अनुवाद एआई अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान रखें कि स्वचालित अनुवादों में त्रुटियाँ या अक्षमताएँ हो सकती हैं। अपने मूल भाषा में मूल दस्तावेज़ को अधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->