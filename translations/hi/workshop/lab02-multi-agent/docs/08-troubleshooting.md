# मॉड्यूल 8 - समस्या निवारण

यह मॉड्यूल मल्टी-एजेंट वर्कफ़्लो से संबंधित सामान्य त्रुटियों, सुधारों और डीबगिंग रणनीतियों को कवर करता है।

## एजेंट आउटपुट समस्याएँ

### GapAnalyzer कहता है “मेरे पास अभी भी मैचिंग रिपोर्ट नहीं है”

**लक्षण:** GapAnalyzer की प्रतिक्रिया आपको “Missing Skills” और “Certification Gaps” के साथ मैचिंग रिपोर्ट पेस्ट करने के लिए कहती है। ऐसा तब भी होता है जब आपने रेज़्यूमे और जॉब विवरण दोनों भेजे हों।

**कारण:** JD टेक्स्ट JD एजेंट को नीचे नहीं पहुंचाया गया। `context_mode="last_agent"` के साथ, `resume_executor` ही एकमात्र निष्पादक है जो कभी भी उपयोगकर्ता के मूल संदेश को देखता है। यदि `RESUME_PARSER_INSTRUCTIONS` अपने आउटपुट में JD टेक्स्ट शामिल नहीं करता तो JD एजेंट के पास पार्स करने के लिए कोई JD नहीं होता, MatchingAgent फिट स्कोर की गणना नहीं कर सकता, और GapAnalyzer को एक निरर्थक इनपुट प्राप्त होता है।

**निदान:**

सर्वर लॉग में, MatchingAgent स्पैन देखें। यदि इसमें:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
पास-थ्रू गायब या टूटा हुआ है।

**समाधान:** पुष्टि करें कि `main.py` में `RESUME_PARSER_INSTRUCTIONS` में `[JOB DESCRIPTION PASS-THROUGH]` अनुभाग और नियम शामिल है:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
यह भी पुष्टि करें कि `JOB_DESCRIPTION_INSTRUCTIONS` में `[PARSED RESUME PASS-THROUGH]` रिले नियम शामिल है:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
यदि कोई भी निर्देश ब्लॉक सैफोल्ड विज़ार्ड से स्टब है, तो उसे [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) से पूर्ण संस्करण से बदलें।

### MatchingAgent आउटपुट देता है “फिट स्कोर की गणना नहीं कर सकता - कोई JD प्रदान नहीं किया गया”

यह ऊपर के समान मूल कारण है। MatchingAgent को JD एजेंट का आउटपुट मिला लेकिन `[PARSED RESUME PASS-THROUGH]` खंड गायब या खाली था, इसलिए वह दोनों प्रोफाइल की तुलना नहीं कर पाया। पुष्टि करें:
1. `JOB_DESCRIPTION_INSTRUCTIONS` में रिले नियम शामिल हो: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` एजेंट को `[JD REQUIREMENTS]` और `[PARSED RESUME PASS-THROUGH]` खंडों को खोजने के लिए कहता है।

दोनों निर्देश ब्लॉकों को [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) से पूर्ण संस्करणों के साथ बदलें।

### प्रतिक्रिया दो बार दिखाई देती है

**लक्षण:** GapAnalyzer आउटपुट (या पूरी पाइपलाइन आउटपुट) एजेंट इंस्पेक्टर प्रतिक्रिया में दो बार दिखाई देता है।

**कारण:** `WorkflowBuilder` इनकमिंग एजेस के लिए OR-सिमेंटिक्स का उपयोग करता है - एक डाउनस्ट्रीम निष्पादक तब चलता है जब भी **कोई भी** पूर्ववर्ती पूर्ण हो जाए। यदि `matching_executor` के दो इनकमिंग एजेस हों (एक `resume_executor` से और एक `jd_executor` से), तो यह दो बार चलता है: एक बार ResumeParser समाप्त होने पर और एक बार JD एजेंट पूर्ण होने पर। फिर GapAnalyzer भी दो बार चलता है।

**समाधान:** सुनिश्चित करें कि `WorkflowBuilder` ग्राफ एक सख्त अनुक्रमिक पाइपलाइन हो जिसमें कोई fan-in न हो:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # रिज्यूमे_एक्जीक्यूटर से नहीं
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

यदि आपके पास एक अनजाना `.add_edge(resume_executor, matching_executor)` लाइन है, तो उसे हटा दें। JD एजेंट के आउटपुट में `[PARSED RESUME PASS-THROUGH]` रिले पहले से ही MatchingAgent को रेज़्यूमे तक पहुंच देता है।

---

## पर्यावरण और कॉन्फ़िगरेशन समस्याएँ

### गायब या गलत `.env` मान

`.env` फ़ाइल `PersonalCareerCopilot/` डायरेक्टरी में होनी चाहिए (जो `main.py` के समान स्तर पर है):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

अपेक्षित `.env` सामग्री:

**पथ A - Foundry क्लाउड:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**पथ B - Foundry लोकल:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> दोनों पथ `FOUNDRY_PROJECT_ENDPOINT` का उपयोग करते हैं। मान भिन्न है: क्लाउड `https://` Foundry एंडपॉइंट का उपयोग करता है; लोकल `http://localhost:5273/v1` का उपयोग करता है। पथ B के लिए सटीक मॉडल उपनाम सत्यापित करने के लिए `foundry model list` चलाएँ।

> **अपना `FOUNDRY_PROJECT_ENDPOINT` ढूंढना:** 
- VS Code में **Foundry Toolkit** साइडबार खोलें → अपने प्रोजेक्ट पर राइट-क्लिक करें → **Copy Project Endpoint**। 
- या [Azure Portal](https://portal.azure.com) जाएँ → अपने Foundry प्रोजेक्ट पर → **Overview** → **Project endpoint**।

> **अपना `AZURE_AI_MODEL_DEPLOYMENT_NAME` ढूंढना:** Foundry Toolkit साइडबार में, अपने प्रोजेक्ट को विस्तारित करें → **Models** → तैनात मॉडल का नाम खोजें (जैसे, `gpt-4.1-mini`)।

### Env var प्राथमिकता

`main.py` में `load_dotenv(override=True)` का उपयोग होता है, जिसका मतलब है:

| प्राथमिकता | स्रोत | दोनों सेट होने पर कौन जीतेगा? |
|----------|--------|-----------------------------|
| 1 (शीर्ष) | `.env` फ़ाइल | हाँ |
| 2 | शेल / कंटेनर पर्यावरण वेरिएबल | `.env` में यदि समान कुंजी मौजूद नहीं है तब उपयोग किया जाता है |

स्थानीय विकास में, यह `.env` को सत्य का स्रोत बनाता है (`.env` संपादन तुरंत रन में प्रभाव डालता है)। होस्टेड डिप्लॉयमेंट में, Foundry कंटेनर स्तर पर पर्यावरण चर इंजेक्ट करता है; चूंकि `.env` इस लैब सेटअप के लिए डिप्लॉइड इमेज का हिस्सा नहीं है, इंजेक्ट किए गए कंटेनर मानों का उपयोग किया जाता है।

---

## संस्करण संगतता

### पैकेज संस्करण मैट्रिक्स

मल्टी-एजेंट वर्कफ़्लो को विशिष्ट पैकेज संस्करणों की आवश्यकता होती है। मेल न खाने वाले संस्करण रनटाइम त्रुटियाँ पैदा करते हैं।

| पैकेज | आवश्यक संस्करण | जांच कमांड |
|---------|-----------------|---------------|
| `agent-framework-foundry` | नवीनतम | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | नवीनतम | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | नवीनतम | `pip show debugpy` |
| पायथन | 3.12+ | `python --version` |

### सामान्य संस्करण त्रुटियाँ

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# सुधारें: एजेंट-फ्रेमवर्क-फाउंड्री को पुनः स्थापित करें
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# सुधार: mcp पैकेज को अपग्रेड करें
pip install mcp --upgrade
```

### एक बार में सभी संस्करण सत्यापित करें

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

अपेक्षित आउटपुट:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## डिप्लॉयमेंट समस्याएँ

### डिप्लॉयमेंट के बाद कंटेनर शुरू नहीं होता

1. **कंटेनर लॉग जांचें:**
   - **Foundry Toolkit** साइडबार खोलें → **Hosted Agents (Preview)** विस्तारित करें → अपने एजेंट पर क्लिक करें → संस्करण विस्तारित करें → **Container Details** → **Logs**।
   - पायथन स्टैक ट्रेसेस या मॉड्यूल गायब होने की त्रुटियाँ देखें।

2. **सामान्य कंटेनर स्टार्टअप विफलताएँ:**

   | लॉग में त्रुटि | कारण | समाधान |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` में पैकेज गायब | पैकेज जोड़ें, पुन: डिप्लॉय करें |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` या `.env` पर्यावरण वेरिएबल सेट नहीं है | `agent.yaml` → `environment_variables` सेक्शन (होस्टेड) या `.env` (स्थानीय) अपडेट करें |
   | `azure.identity.CredentialUnavailableError` | मैनेज्ड आईडेंटिटी कॉन्फ़िगर नहीं है | Foundry इसे स्वचालित रूप से सेट करता है - सुनिश्चित करें आप एक्सटेंशन से डिप्लॉय कर रहे हैं |
   | `OSError: port 8088 already in use` | Dockerfile में गलत पोर्ट एक्सपोज़ या पोर्ट संघर्ष | Dockerfile में `EXPOSE 8088` और `CMD ["python", "main.py"]` सत्यापित करें |
   | कंटेनर कोड 1 के साथ बाहर निकलता है | `main()` में अनहैंडल्ड अपवाद | पहले स्थानीय रूप से टेस्ट करें ([Module 5](05-test-locally.md)) ताकि डिप्लॉयमेंट से पहले त्रुटियाँ पकड़ी जा सकें |

3. **सुधार के बाद पुनः डिप्लॉय करें:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → वही एजेंट चुनें → नया संस्करण डिप्लॉय करें।

### डिप्लॉयमेंट में बहुत समय लगता है

मल्टी-एजेंट कंटेनर स्टार्ट होने में अधिक समय लेते हैं क्योंकि वे स्टार्टअप पर 4 एजेंट इंस्टेंस बनाते हैं। सामान्य स्टार्टअप समय:

| चरण | अपेक्षित अवधि |
|-------|------------------|
| कंटेनर इमेज बिल्ड | 1-3 मिनट |
| इमेज ACR को पुश करना | 30-60 सेकंड |
| कंटेनर स्टार्ट (एकल एजेंट) | 15-30 सेकंड |
| कंटेनर स्टार्ट (मल्टी-एजेंट) | 30-120 सेकंड |
| एजेंट प्लेग्राउंड में उपलब्ध | "Started" के 1-2 मिनट बाद |

> यदि "Pending" स्थिति 5 मिनट से अधिक समय तक बनी रहती है, तो त्रुटियों के लिए कंटेनर लॉग्स जांचें।

---

## RBAC और अनुमति समस्याएँ

### `403 Forbidden` या `AuthorizationFailed`

आपको अपने Foundry प्रोजेक्ट पर **[Foundry User](https://aka.ms/foundry-ext-project-role)** भूमिका की आवश्यकता है (पूर्व में नामित **Azure AI User** - भूमिका ID अपरिवर्तित):

1. [Azure Portal](https://portal.azure.com) पर जाएँ → अपने Foundry **प्रोजेक्ट** संसाधन पर।
2. क्लिक करें **Access control (IAM)** → **Role assignments**।
3. अपना नाम खोजें → पुष्टि करें कि **Foundry User** (या पुराना लेबल **Azure AI User**) सूचीबद्ध है।
4. यदि गायब हो: **Add** → **Add role assignment** → **Foundry User** खोजें → अपने खाते को असाइन करें।

अधिक जानकारी के लिए [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) दस्तावेज़ देखें।

### मॉडल डिप्लॉयमेंट सुलभ नहीं है

यदि एजेंट मॉडल-संबंधित त्रुटियाँ लौटाता है:

1. पुष्टि करें कि मॉडल डिप्लॉय है: Foundry साइडबार → प्रोजेक्ट विस्तारित करें → **Models** → देखें कि `gpt-4.1-mini` (या आपका मॉडल) स्थिति **Succeeded** के साथ है।
2. पुष्टि करें कि डिप्लॉयमेंट नाम मेल खाता है: `.env` (या `agent.yaml`) में `AZURE_AI_MODEL_DEPLOYMENT_NAME` की तुलना साइडबार में वास्तविक डिप्लॉयमेंट नाम से करें।
3. यदि डिप्लॉयमेंट समाप्त हो गया हो (फ्री टियर): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) से पुनः डिप्लॉय करें (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)।

---

## Foundry लोकल समस्याएँ (पथ B)

### Foundry लोकल सेवा चल नहीं रही

```powershell
# स्थिति जांचें
foundry local status

# सेवा को शुरू करें यदि यह बंद है
foundry local start
```

| लक्षण | कारण | समाधान |
|---------|-------|-----|
| हेल्थ चेक जवाब देता है `503` | सेवा शुरू नहीं हुई | `foundry local start` चलाएँ या Foundry Toolkit साइडबार में **Start** क्लिक करें |
| हेल्थ चेक टाइम आउट होता है | मॉडल अभी भी लोड हो रहा है | स्टार्ट के 30–60 सेकंड बाद प्रतीक्षा करें; बड़े मॉडल को ज्यादा समय लगता है |
| `/v1/health` पर `StatusCode: 404` | गलत पोर्ट | डिफ़ॉल्ट `5273` है। वास्तविक पोर्ट के लिए `foundry local status` देखें |
| अपर्याप्त संसाधन | Foundry Local को करीब 4 GB RAM खाली चाहिए | अन्य एप्लिकेशन बंद करें |
| मॉडल डाउनलोड विफल होता है | कम डिस्क स्थान | मॉडल 2–8 GB के होते हैं। स्थान खाली करें, फिर `foundry model pull <name>` चलाएँ |

### मॉडल नाम मेल नहीं खाता

```powershell
# डाउनलोड किए गए मॉडलों और उनके सटीक उपनामों की सूची बनाएं
foundry model list
```

`.env` में `AZURE_AI_MODEL_DEPLOYMENT_NAME` को बिल्कुल वैसे ही सेट करें जैसा उपनाम दिखता है (जैसे, `phi-4-mini`, न कि `Phi-4-mini`)।

### स्थानीय रन पर `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (पथ B)

लैब का `main.py` `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` का उपयोग करता है। Foundry Local को इस वेरिएबल को लोकल सेवा की ओर इंगित करना आवश्यक है - **न कि** `AZURE_AI_PROJECT_ENDPOINT`। सुनिश्चित करें कि आपकी `.env` में यह हो:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP टूल अभी भी बाहरी कॉल करता है (पथ B)

यह अपेक्षित है। `search_microsoft_learn_for_plan` टूल `https://learn.microsoft.com/api/mcp` से लर्निंग संसाधन प्राप्त करता है। **केवल कौशल-नाम क्वेरी** नेटवर्क के माध्यम से जाती है - रेज़्यूमे और JD टेक्स्ट पूरी तरह आपके डिवाइस पर संसाधित होते हैं और कभी ट्रांसमिट नहीं होते। यदि पूर्ण ऑफ़लाइन संचालन आवश्यक है, तो टूल में एक `try/except` फॉलबैक जोड़ें जो जब एंडपॉइंट अनुपलब्ध हो तब एक स्थैतिक `learn.microsoft.com` URL लौटाए।

---

## सहायता प्राप्त करना

यदि ऊपर दिए गए सुधारों को आज़माने के बाद भी आप फंसे हैं:

1. **सर्वर लॉग जांचें** - अधिकांश त्रुटियाँ टर्मिनल में पायथन स्टैक ट्रेस उत्पन्न करती हैं। पूरा traceback पढ़ें।
2. **त्रुटि संदेश खोजें** - त्रुटि टेक्स्ट कॉपी करें और [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) में खोजें।
3. **इश्यू खोलें** - [वर्कशॉप रिपॉजिटरी](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) पर निम्न के साथ इश्यू फ़ाइल करें:
   - त्रुटि संदेश या स्क्रीनशॉट
   - आपके पैकेज संस्करण (`pip list | Select-String "agent-framework"`)
   - आपके पायथन संस्करण (`python --version`)
   - समस्या स्थानीय है या डिप्लॉयमेंट के बाद

---

### चेकपॉइंट

- [ ] आप जानते हैं कि `.env` कॉन्फ़िगरेशन समस्याओं की जांच और सुधार कैसे करें
- [ ] आप आवश्यक मैट्रिक्स के अनुसार पैकेज संस्करणों को सत्यापित कर सकते हैं
- [ ] आप डिप्लॉयमेंट विफलताओं के लिए कंटेनर लॉग्स कैसे जांचें जानते हैं
- [ ] आप Azure Portal में RBAC भूमिकाओं की जांच कर सकते हैं

---

**पिछला:** [07 - Playground में सत्यापन](07-verify-in-playground.md) · **अगला:** [09 - सारांश →](09-summary.md) · **होम:** [Lab 02 README](../README.md) · [वर्कशॉप होम](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
इस दस्तावेज़ का अनुवाद AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->