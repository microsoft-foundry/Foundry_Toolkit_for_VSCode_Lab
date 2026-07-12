# मॉड्यूल ८ - त्रुटी निवारण

हा मॉड्यूल मल्टी-एजंट वर्कफ्लोशी संबंधित सामान्य चुका, दुरुस्ती आणि डिबगिंग धोरणे कव्हर करतो.

## एजंट आउटपुट समस्या

### GapAnalyzer म्हणतो “माझ्याकडे अजूनही जुळणारा अहवाल नाही”

**लक्षण:** GapAnalyzer चा प्रतिसाद तुम्हाला “गायब कौशल्ये” आणि “प्रमाणपत्राचा तफावत” असलेल्या जुळणाऱ्या अहवाल पेस्ट करण्यास विचारतो. हे तेव्हाही होते जेव्हा तुम्ही दोन्ही रेसुमे आणि नोकरीचे वर्णन पाठवले असते.

**कारण:** JD मजकूर JD एजंटकडे डाऊनस्ट्रीम मध्ये पास केला गेला नाही. `context_mode="last_agent"` सह, `resume_executor` हा एकला एक Executor आहे जो वापरकर्त्याचा मूळ संदेश पाहतो. जर `RESUME_PARSER_INSTRUCTIONS` मध्ये JD मजकूर त्याच्या आउटपुटमध्ये नसेल, तर JD एजंटकडे कोणताही JD नसतो, MatchingAgent जुळणी गुणांकन करू शकत नाही आणि GapAnalyzer ला निरर्थक इनपुट मिळतो.

**निदान:**

सर्व्हर लॉगमध्ये, MatchingAgent स्पॅन शोधा. जर त्यात:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
पास-थ्रू गायब किंवा तुटलेला आहे.

**दुरुस्ती:** `main.py` मधील `RESUME_PARSER_INSTRUCTIONS` मध्ये `[JOB DESCRIPTION PASS-THROUGH]` विभाग आणि नियम आहे का ते तपासा:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
तसेच `JOB_DESCRIPTION_INSTRUCTIONS` मध्ये `[PARSED RESUME PASS-THROUGH]` रेले नियम आहे का ते तपासा:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
जर कोणत्याही सूचना ब्लॉकमध्ये मशागत विजार्डमध्ये तयार केलेली टाचणी असेल, तर त्याऐवजी [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) मधील पूर्ण आवृत्ती वापरा.

### MatchingAgent “Cannot compute fit score - no JD provided” हा संदेश देतो

वरील सारखेच मूळ कारण आहे. MatchingAgent ला JD एजंटच्या आउटपुटची प्राप्ती झाली पण `[PARSED RESUME PASS-THROUGH]` विभाग गायब किंवा रिकामा होता, त्यामुळे ते दोन्ही प्रोफाइलची तुलना करू शकले नाही. याची खात्री करा:
१. `JOB_DESCRIPTION_INSTRUCTIONS` मध्ये रेले नियम आहे: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
२. `MATCHING_AGENT_INSTRUCTIONS` एजंटला `[JD REQUIREMENTS]` आणि `[PARSED RESUME PASS-THROUGH]` विभाग शोधायला सांगते.

दोन्ही सूचना ब्लॉक्स [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) मधील पूर्ण आवृत्तीसह बदला.

### प्रतिसाद दोनदा दिसतो

**लक्षण:** GapAnalyzer चा आउटपुट (किंवा संपूर्ण पाइपलाइन आउटपुट) एजंट इन्स्पेक्टर च्या प्रतिसादात दोनदा दिसतो.

**कारण:** `WorkflowBuilder` येणाऱ्या एजेसाठी OR-सेमॅंटिक्स वापरतो - कोणताही पूर्वीचा Executor पूर्ण होते तेव्हा डाऊनस्ट्रीम Executor चालेल. जर `matching_executor` ला दोन इनकमिंग एजेस असतील (एक `resume_executor` कडून आणि एक `jd_executor` कडून), तो दोनदा चालतो: एकदा ResumeParser पूर्ण झाल्यावर आणि दुसऱ्यांदा JD Agent पूर्ण झाल्यावर. त्यामुळे GapAnalyzer सुद्धा दोनदा चालतो.

**दुरुस्ती:** `WorkflowBuilder` ग्राफ ठराविक रित्या सलग पाइपलाइन असावा, ज्यामध्ये कोणतेही फॅन-इन नसावे:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # resume_executor कडून नाही
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

जर तुमच्याकडे अलिप्त `.add_edge(resume_executor, matching_executor)` ओळ असेल, तर ती काढा. JD एजंटच्या आउटपुटमधील `[PARSED RESUME PASS-THROUGH]` रेले आधीच MatchingAgent ला रेसुमेपर प्रवेश देते.

---

## पर्यावरण आणि कॉन्फिगरेशन समस्या

### `.env` मूल्ये हरवलेली किंवा चुकीची

`.env` फाइल `PersonalCareerCopilot/` निर्देशिकेत असावी (main.py शी समान स्तरावर):

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

> दोन्ही पथ `FOUNDRY_PROJECT_ENDPOINT` वापरतात. त्याची किंमत भिन्न आहे: क्लाउड एक `https://` Foundry एंडपॉइंट वापरतो; लोकल `http://localhost:5273/v1` वापरतो. Path B साठी अचूक मॉडेल उपनाम निश्चित करण्यासाठी `foundry model list` चालवा.

> **तुमचा `FOUNDRY_PROJECT_ENDPOINT` शोधणे:**
- VS कोडमधील **Foundry Toolkit** साइडबार उघडा → तुमच्या प्रकल्पावर उजवे-क्लिक करा → **Copy Project Endpoint**.
- किंवा [Azure Portal](https://portal.azure.com) → तुमचा Foundry प्रकल्प → **Overview** → **Project endpoint**.

> **तुमचा `AZURE_AI_MODEL_DEPLOYMENT_NAME` शोधणे:** Foundry Toolkit साइडबारमध्ये, प्रकल्प विस्तार → **Models** → तुमचा डिप्लॉय केलेला मॉडेल नाव शोधा (उदा., `gpt-4.1-mini`).

### एनव्हायरेन्मेंट व्हेरिएबल प्राधान्यक्रम

`main.py` मध्ये `load_dotenv(override=True)` वापरले आहे, ज्याचा अर्थ:

| प्राधान्यक्रम | स्रोत | दोन्ही सेट केल्यावर कोण जिंकतो? |
|----------|--------|------------------------|
| १ (सर्वोच्च) | `.env` फाइल | होय |
| २ | शेल / कंटेनर पर्यावरण व्हेरिएबल | `.env` मध्ये समान की नसेल तेव्हा वापरले जाते |

स्थानिक विकासामध्ये, हे `.env` ला सत्याचा स्रोत बनवते ( `.env` संपादित केल्यावर लगेच परिणाम होतो). होस्टेड डिप्लॉयमेंटमध्ये, Foundry कंटेनर स्तरावर पर्यावरण चलांची इंजेक्शन करते; कारण `.env` हे या लॅब सेटअपसाठी डिप्लॉय केलेल्या इमेजचा भाग नाही, इंजेक्ट केलेले कंटेनर मूल्य वापरले जाते.

---

## आवृत्ती सुसंगती

### पॅकेज आवृत्ती मॅट्रिक्स

मल्टी-एजंट वर्कफ्लोला विशिष्ट पॅकेज आवृत्ती आवश्यक आहे. विसंगत आवृत्त्या रनटाइम चुका निर्माण करतात.

| पॅकेज | आवश्यक आवृत्ती | तपासण्याची कमांड |
|---------|-----------------|---------------|
| `agent-framework-foundry` | नवीनतम | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | नवीनतम | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | नवीनतम | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### सामान्य आवृत्ती त्रुटी

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# दुरुस्ती: एजंट-फ्रेमवर्क-फाउंड्री पुन्हा स्थापित करा
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# दुरुस्ती: mcp पॅकेज सुधारित करा
pip install mcp --upgrade
```

### सर्व आवृत्त्या एकाच वेळी तपासा

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

## डिप्लॉयमेंट समस्या

### डिप्लॉयमेंटनंतर कंटेनर सुरू होत नाही

१. **कंटेनर लॉग तपासा:**
   - **Foundry Toolkit** साइडबार उघडा → **Hosted Agents (Preview)** विस्तार करा → तुमचा एजंट क्लिक करा → आवृत्ती विस्तार करा → **Container Details** → **Logs**.
   - Python स्टॅक ट्रेसेस किंवा मॉड्यूल गायब त्रुटी शोधा.

२. **सामान्य कंटेनर स्टार्टअप अपयश:**

   | लॉगमधील त्रुटी | कारण | दुरुस्ती |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` मध्ये पॅकेज गायब | पॅकेज जोडा, पुन्हा डिप्लॉय करा |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` किंवा `.env` एन्व्ह वेरिएबल सेट नाहीत | `agent.yaml` → `environment_variables` विभाग (होस्टेड) किंवा `.env` (लोकल) अद्यतनित करा |
   | `azure.identity.CredentialUnavailableError` | मॅनेज्ड आइडेंटिटी कॉन्फिगर नाही | Foundry हा आपोआप सेट करतो - खात्री करा तुम्ही एक्स्टेंशनद्वारे डिप्लॉय करत आहात |
   | `OSError: port 8088 already in use` | Dockerfile चुकीचा पोर्ट एक्सपोज करतो किंवा पोर्ट संघर्ष | Dockerfile मध्ये `EXPOSE 8088` आणि `CMD ["python", "main.py"]` तपासा |
   | कंटेनर कोड १ सह बाहेर पडतो | `main()` मध्ये हँडल न केलेली अपवाद | आधी स्थानिकपणे तपासणी करा ([Module 5](05-test-locally.md)) चुकी 잡ण्यासाठी |

३. **दुरुस्ती केल्यानंतर पुनः डिप्लॉय करा:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → तोच एजंट निवडा → नवीन आवृत्ती डिप्लॉय करा.

### डिप्लॉयमेंट खूप वेळ घेत आहे

मल्टी-एजंट कंटेनर सुरू होण्यासाठी अधिक वेळ घेतात कारण ते स्टार्टअप वेळी ४ एजंट उदाहरणे तयार करतात. सामान्य स्टार्टअप वेळा:

| टप्पा | अपेक्षित कालावधी |
|-------|------------------|
| कंटेनर इमेज बिल्ड | १-३ मिनिटे |
| इमेज ACR कडे पुश | ३०-६० सेकंद |
| कंटेनर स्टार्ट (एकल एजंट) | १५-३० सेकंद |
| कंटेनर स्टार्ट (मल्टी-एजंट) | ३०-१२० सेकंद |
| Playground मध्ये एजंट उपलब्ध | "Started" नंतर १-२ मिनिटे |

> जर "Pending" स्टेटस ५ मिनिटांपेक्षा जास्त राहिला, तर कंटेनर लॉगमध्ये त्रुटी तपासा.

---

## RBAC आणि परवानगी समस्या

### `403 Forbidden` किंवा `AuthorizationFailed`

तुम्हाला तुमच्या Foundry प्रकल्पावर **[Foundry User](https://aka.ms/foundry-ext-project-role)** भूमिका आवश्यक आहे (पूर्वीचे नाव **Azure AI User** - भूमिका आयडी अपरिवर्तित):

१. [Azure Portal](https://portal.azure.com) मध्ये जा → तुमचा Foundry **प्रकल्प** रिसोर्स निवडा.
२. **Access control (IAM)** → **Role assignments** क्लिक करा.
३. तुमचे नाव शोधा → **Foundry User** (किंवा पारंपरिक लेबल **Azure AI User**) आहे का ते पुष्टी करा.
४. जर गहाळ असेल: **Add** → **Add role assignment** → **Foundry User** शोधा → तुमच्या खात्याला असाइन करा.

तपशीलांसाठी [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) दस्तऐवज पहा.

### मॉडेल डिप्लॉयमेंट उपलब्ध नाही

जर एजंट मॉडेल-संबंधित त्रुटी देत असेल:

१. मॉडेल डिप्लॉय झाले आहे का तपासा: Foundry साइडबार → प्रकल्प विस्तार करा → **Models** → `gpt-4.1-mini` (किंवा तुमचा मॉडेल) तपासा, स्थिती **Succeeded** असावी.
२. डिप्लॉयमेंट नाव जुळते का तपासा: `.env` (किंवा `agent.yaml`) मधील `AZURE_AI_MODEL_DEPLOYMENT_NAME` आणि साइडबारमधील खरी डिप्लॉयमेंट नाव.
३. जर डिप्लॉयमेंट कालबाह्य झाला (मुफ्त स्तर): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) मधून पुनः डिप्लॉय करा (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local समस्या (पथ B)

### Foundry Local सेवा चालू नाही

```powershell
# स्थिती तपासा
foundry local status

# सेवा थांबलेली असल्यास ती सुरू करा
foundry local start
```

| लक्षण | कारण | दुरुस्ती |
|---------|-------|-----|
| हेल्थ चेक `503` परत देतो | सेवा सुरू नाही | `foundry local start` किंवा Foundry Toolkit साइडबारमध्ये **Start** क्लिक करा |
| हेल्थ चेक टाइमआउट होते | मॉडेल अद्याप लोड होतोय | सुरू केल्यानंतर ३०-६० सेकंद प्रतीक्षा करा; मोठ्या मॉडेल्सना अधिक वेळ लागतो |
| `/v1/health` वर `StatusCode: 404` | चुकीचा पोर्ट | डीफॉल्ट `5273` आहे. `foundry local status` चला आणि अचूक पोर्ट तपासा |
| अपुरे संसाधने | Foundry Local ला सुमारे ४ GB RAM मोकळी पाहिजे | इतर अनुप्रयोग बंद करा |
| मॉडेल डाउनलोड अयशस्वी | कमी डिस्क जागा | मॉडेल्स २-८ GB आहेत. जागा मोकळी करा आणि `foundry model pull <name>` चला |

### मॉडेल नाव विसंगती

```powershell
# डाउनलोड केलेल्या मॉडेल्सची आणि त्यांच्या अचूक उपनामांची यादी करा
foundry model list
```

`.env` मध्ये `AZURE_AI_MODEL_DEPLOYMENT_NAME` अचूक उपनाम सेट करा (उदा., `phi-4-mini`, `Phi-4-mini` नाही).

### स्थानिक चालवताना `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (पथ B)

या लाबच्या `main.py` मध्ये `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` वापरले आहे. Foundry Local ला ही चल स्थानिक सेवेकडे निर्देशित करणे आवश्यक आहे - **नाही** `AZURE_AI_PROJECT_ENDPOINT`. खात्री करा की तुमच्या `.env` मध्ये खालील आहे:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP टूल अजूनही बाह्य कॉल करते (पथ B)

हे अपेक्षित आहे. `search_microsoft_learn_for_plan` टूल `https://learn.microsoft.com/api/mcp` वरून शिक्षण संसाधने मिळवते. **फक्त कौशल्य-नाव क्वेरी** नेटवर्कवर जाते - रेसुमे आणि JD मजकूर पूर्णपणे तुमच्या डिव्हाइसवर प्रक्रिया करतात आणि कधीही ट्रान्समिट होत नाहीत. पूर्णपणे ऑफलाइन ऑपरेशन आवश्यक असल्यास, टूलमध्ये एक `try/except` फॉलबॅक जोडा जो एंडपॉइंट उपलब्ध नसल्यानंतर स्थिर `learn.microsoft.com` URL परत करेल.

---

## मदत मिळवणे

जर वरील दुरुस्ती केल्यावरही अडचण असेल:

१. **सर्व्हर लॉग तपासा** - बहुतांश चुका टर्मिनलमध्ये Python स्टॅक ट्रेस तयार करतात. संपूर्ण ट्रेसबॅक वाचा.
२. **त्रुटी संदेश शोधा** - त्रुटी मजकूर कॉपी करा आणि [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) मध्ये शोधा.
३. **इश्यू उघडा** - [वर्कशॉप रेपॉझिटरी](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) वर इश्यू फाईल करा:
   - त्रुटी संदेश किंवा स्क्रीनशॉट
   - तुमच्या पॅकेज आवृत्त्या (`pip list | Select-String "agent-framework"`)
   - तुमची Python आवृत्ती (`python --version`)
   - स्थानिक समस्या आहे की डिप्लॉयमेंटनंतर

---

### चेकपॉईंट

- [ ] तुम्हाला `.env` कॉन्फिगरेशन समस्या कशा तपासायच्या आणि दुरुस्त करायच्या माहिती आहे
- [ ] तुम्ही आवश्यक मॅट्रिक्सशी पॅकेज आवृत्त्या जुळतात का ते तपासू शकता
- [ ] तुम्हाला डिप्लॉयमेंट फेल्युअर्ससाठी कंटेनर लॉग कसे तपासायचे माहिती आहे
- [ ] तुम्ही Azure पोर्टलमध्ये RBAC भूमिका तपासू शकता

---

**मागील:** [07 - Verify in Playground](07-verify-in-playground.md) · **पुढे:** [09 - Summary →](09-summary.md) · **मुख्यपृष्ठ:** [Lab 02 README](../README.md) · [वर्कशॉप होम](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून अनुवादित केला आहे. जरी आम्ही अचूकतेसाठी प्रयत्न करतो, तरी कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या मूळ भाषेत अधिकृत स्रोत मानला पाहिजे. महत्त्वाची माहिती असल्यास, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थलावणीसाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->