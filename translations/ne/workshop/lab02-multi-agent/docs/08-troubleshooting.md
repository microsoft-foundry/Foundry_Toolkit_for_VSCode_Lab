# मोड्युल ८ - समस्या समाधान

यो मोड्युलले बहु-एजेन्ट workflow का सामान्य त्रुटिहरू, समाधानहरू, र डिबगिङ रणनीतिहरू समेट्छ।

## एजेन्ट आउटपुट समस्याहरू

### GapAnalyzer भन्छ “मसँग अझै मेल खाने रिपोर्ट छैन”

**लक्षण:** GapAnalyzer को प्रतिक्रिया गर्दा तपाईलाई "Missing Skills" र "Certification Gaps" सहितको मेल खाने रिपोर्ट टाँस्न भनिन्छ। यो तब पनि हुन्छ जब तपाईले रिजुमे र जागिर विवरण दुवै पठाउनु भएको छ।

**कारण:** JD टेक्स्ट JD एजेन्टमा डाउनस्ट्रीम पास गरिएको थिएन। `context_mode="last_agent"` सँग `resume_executor` मात्र प्रयोगकर्ताको मूल सन्देशलाई देख्ने Executor हो। यदि `RESUME_PARSER_INSTRUCTIONS` मा JD टेक्स्ट आउटपुटमा समावेश छैन भने, JD एजेन्टले पार्स गर्ने JD हुँदैन, MatchingAgent फिट स्कोर गणना गर्न सक्दैन, र GapAnalyzer ले अर्थहीन इनपुट प्राप्त गर्छ।

**निदान:**

सर्भर लगहरूमा, MatchingAgent को स्प्यान खोज्नुहोस्। यदि त्यहाँ:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
 पास-थ्रु हराइएको वा बिग्रिएको छ।

**समाधान:** सुनिश्चित गर्नुहोस् कि `main.py` मा रहेको `RESUME_PARSER_INSTRUCTIONS` मा `[JOB DESCRIPTION PASS-THROUGH]` सेक्सन र नियम समावेश छ:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
 साथै सुनिश्चित गर्नुहोस् कि `JOB_DESCRIPTION_INSTRUCTIONS` मा `[PARSED RESUME PASS-THROUGH]` रिलेको नियम छ:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
 यदि कुनै निर्देशन ब्लक स्क्याफोल्ड विजार्डबाट स्टब हो भने, यसलाई [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) बाट पूरा संस्करणले प्रतिस्थापन गर्नुहोस्।

### MatchingAgent ले “Cannot compute fit score - no JD provided” आउटपुट गर्छ

यो माथिको जस्तै मूल कारण हो। MatchingAgent ले JD एजेन्टको आउटपुट प्राप्त गर्यो तर `[PARSED RESUME PASS-THROUGH]` सेक्सन हरायो वा खाली थियो, त्यसैले उनीहरूले प्रोफाइलहरू तुलना गर्न सकेन। पुष्टि गर्नुहोस्:
1. `JOB_DESCRIPTION_INSTRUCTIONS` ले रिलेको नियम समावेश गर्छ: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` एजेन्टलाई `[JD REQUIREMENTS]` र `[PARSED RESUME PASS-THROUGH]` सेक्सन खोज्न भन्छ।

दुबै निर्देशन ब्लकहरू [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) बाट पूरा संस्करणसँग प्रतिस्थापन गर्नुहोस्।

### प्रतिक्रिया दुई पटक देखा पर्छ

**लक्षण:** GapAnalyzer आउटपुट (वा सम्पूर्ण पाइपलाइन आउटपुट) एजेन्ट इन्स्पेक्टरको प्रतिक्रियामा दुई पटक देखा पर्ने।

**कारण:** `WorkflowBuilder` ले इनकमिङ एजहरूको लागि OR-सेम्यान्टिक्स प्रयोग गर्छ - कुनै पनि पूर्ववर्ती पूरा भए पछि डाउनस्ट्रीम executor चल्छ। यदि `matching_executor` सँग दुई इनकमिङ एजहरू छन् (एक `resume_executor` बाट र अर्को `jd_executor` बाट), यो दुई पटक चल्छ: एक पटक ResumeParser सकिएपछि र अर्को पटक JD एजेन्ट सकिएपछि। त्यसपछि GapAnalyzer पनि दुई पटक चल्छ।

**समाधान:** `WorkflowBuilder` ग्राफ कडाईका साथ अनुक्रमिक पाइपलाइन होस् जसमा कुनै फ्यान-इन नहोस्:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # resume_executor बाट होइन
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

यदि तपाईंसँग कुनै बिटमार्क `.add_edge(resume_executor, matching_executor)` लाइन् छ भने, त्यसलाई हटाउनुहोस्। JD एजेन्टको आउटपुटमा `[PARSED RESUME PASS-THROUGH]` रिलेमैचिङ एजेन्टलाई रिजुमेसम्म पहुँच दिन्छ।

---

## वातावरण र कन्फिगरेसन समस्याहरू

### हराएको वा गलत `.env` मानहरू

`.env` फाइल `PersonalCareerCopilot/` डाइरेक्टरीमा हुनुपर्छ (`main.py` संगै):

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

> दुवै पथहरूले `FOUNDRY_PROJECT_ENDPOINT` प्रयोग गर्छन्। मान फरक छ: क्लाउडले `https://` Foundry endpoint र लोकलले `http://localhost:5273/v1` प्रयोग गर्छ। Path B को लागि सही मोडेल एलियस पुष्टि गर्न `foundry model list` चलाउनुहोस्।

> **तपाईंको `FOUNDRY_PROJECT_ENDPOINT` कसरी फेला पार्ने:**
- VS Code मा **Foundry Toolkit** साइडबार खोल्नुहोस् → आफ्नो प्रोजेक्टमा राइट-क्लिक गर्नुहोस् → **Copy Project Endpoint**। 
- वा [Azure Portal](https://portal.azure.com) मा जानुहोस् → आफ्नो Foundry प्रोजेक्ट → **Overview** → **Project endpoint**।

> **तपाईंको `AZURE_AI_MODEL_DEPLOYMENT_NAME` कसरी फेला पार्ने:** Foundry Toolkit साइडबारमा, आफ्नो प्रोजेक्टलाई विस्तार गर्नुहोस् → **Models** → तपाईंले डिप्लोय गरेको मोडेल नाम खोज्नुहोस् (जस्तै, `gpt-4.1-mini`)।

### वातावरण चर प्राथमिकता

`main.py` मा `load_dotenv(override=True)` प्रयोग गरिएको छ, जसको मतलब:

| प्राथमिकता | स्रोत | दुवै सेट हुँदा को जीत्छ? |
|----------|--------|------------------------|
| 1 (सबैभन्दा उच्च) | `.env` फाइल | हो |
| 2 | Shell/कन्टेनर वातावरण चर | डुप्लिकेट नभएको अवस्थामा प्रयोग गरिन्छ |

स्थानीय विकासमा, `.env` सत्यको स्रोत हुन्छ (सम्पादनले तुरुन्तै रनहरू प्रभावित गर्छ)। होस्ट गरिएको डिप्लोयमेन्टमा, Foundry कन्टेनर स्तरमा वातावरण चरहरू इन्जेक्ट गर्छ; `.env` यो सेटअपमा इमेजमा छैन, त्यसैले इन्जेक्ट गरिएको कन्टेनर मानहरू प्रयोग हुन्छन्।

---

## संस्करण अनुकूलता

### प्याकेज संस्करण म्याट्रिक्स

बहु-एजेन्ट workflow का लागि विशेष प्याकेज संस्करणहरू आवश्यक छन्। संस्करणहरू मेल नखाने हो भने रनटाइम त्रुटि आउँछ।

| प्याकेज | आवश्यक संस्करण | जाँच कमाण्ड |
|---------|-----------------|---------------|
| `agent-framework-foundry` | पछिल्लो | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | पछिल्लो | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | पछिल्लो | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### सामान्य संस्करण त्रुटिहरू

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# सुधार: एजेन्ट-फ्रेमवर्क-फाउन्ड्री पुनःस्थापना गर्नुहोस्
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# समाधान: mcp प्याकेज अपडेट गर्नुहोस्
pip install mcp --upgrade
```

### सबै संस्करणहरू एकैचोटी जाँच्नुहोस्

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

अपेक्षित परिणाम:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## डिप्लोयमेन्ट समस्याहरू

### डिप्लोयमेन्ट पछि कन्टेनर सुरु हुँदैन

1. **कन्टेनर लगहरू जाँच गर्नुहोस्:**
   - **Foundry Toolkit** साइडबार खोल्नुहोस् → **Hosted Agents (Preview)** विस्तार गर्नुहोस् → आफ्नो एजेन्ट क्लिक गर्नुहोस् → भर्सन विस्तार गर्नुहोस् → **Container Details** → **Logs**।
   - Python stack trace वा हराएको मोड्युल त्रुटि हेर्नुहोस्।

2. **सामान्य कन्टेनर सुरु त्रुटिहरू:**

   | लगमा त्रुटि | कारण | समाधान |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` मा प्याकेज हरायो | प्याकेज थपेर पुन: डिप्लोय गर्नुहोस् |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` वा `.env` वातावरण चरहरू सेट छैनन् | `agent.yaml` → `environment_variables` सेक्सन (होस्टेड) वा `.env` (लोकल) अपडेट गर्नुहोस् |
   | `azure.identity.CredentialUnavailableError` | Managed Identity कन्फिगर गरिएको छैन | Foundry ले स्वचालित सेटअप गर्छ - विस्तारमार्फत डिप्लोय गरेर सुनिश्चित गर्नुहोस् |
   | `OSError: port 8088 already in use` | Dockerfile मा गलत पोर्ट खुला वा पोर्ट द्वन्द्व | Dockerfile मा `EXPOSE 8088` र `CMD ["python", "main.py"]` सुनिश्चित गर्नुहोस् |
   | कन्टेनर कोड 1 सहित बाहिर जान्छ | `main()` मा अपठित अपवाद | स्थानीय रूपमा पहिले परीक्षण गर्नुहोस् ([मोड्युल ५](05-test-locally.md)) त्रुटि समात्न |

3. **समस्या समाधान पछि पुन: डिप्लोय गर्नुहोस्:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → सो एजेन्ट चयन गर्नुहोस् → नयाँ संस्करण डिप्लोय गर्नुहोस्।

### डिप्लोयमेन्ट धेरै लामो समय लिन्छ

बहु-एजेन्ट कन्टेनरहरू सुरु हुँदा ४ एजेन्ट इन्स्ट्यान्सहरू बनाउँछन्, त्यसैले सुरु समय बढी लाग्छ। सामान्य सुरु समयहरू:

| चरण | अपेक्षित अवधि |
|-------|------------------|
| कन्टेनर इमेज बिल्ड | १-३ मिनेट |
| ACR मा इमेज पठाउने | ३०-६० सेकेन्ड |
| कन्टेनर सुरु (एक एजेन्ट) | १५-३० सेकेन्ड |
| कन्टेनर सुरु (बहु-एजेन्ट) | ३०-१२० सेकेन्ड |
| प्लेग्राउन्डमा एजेन्ट उपलब्ध | "Started" पछि १-२ मिनेट |

> यदि "Pending" स्थिति ५ मिनेटभन्दा बढी रहन्छ भने, कन्टेनर लगहरूमा त्रुटिहरू जाँच्नुहोस्।

---

## RBAC र अनुमति सम्बन्धी समस्या

### `403 Forbidden` वा `AuthorizationFailed`

तपाईंलाई Foundry प्रोजेक्टमा **[Foundry User](https://aka.ms/foundry-ext-project-role)** भूमिका आवश्यक छ (पहिलेको नाम **Azure AI User** - भूमिका ID अपरिवर्तित):

1. [Azure Portal](https://portal.azure.com) मा जानुहोस् → आफ्नो Foundry **प्रोजेक्ट** स्रोत।
2. **Access control (IAM)** क्लिक गर्नुहोस् → **Role assignments**।
3. आफ्नो नाम खोज्नुहोस् → **Foundry User** (वा पुरानो लेबल **Azure AI User**) सूचीमा छ कि हेर्नुहोस्।
4. यदि छैन भने: **Add** → **Add role assignment** → **Foundry User** खोज्नुहोस् → आफ्नो खातामा असाइन गर्नुहोस्।

विस्तृत जानकारीका लागि [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) दस्तावेज हेर्नुहोस्।

### मोडेल डिप्लोयमेन्ट पहुँचयोग्य छैन

यदि एजेन्टले मोडेल सम्बन्धी त्रुटिहरू फिर्ता गर्छ भने:

1. मोडेल डिप्लोय गरिएको छ कि छैन पुष्टि गर्नुहोस्: Foundry साइडबार → प्रोजेक्ट विस्तार गर्नुहोस् → **Models** → `gpt-4.1-mini` (वा तपाईंको मोडेल) स्टेटस **Succeeded** छ कि हेर्नुहोस्।
2. डिप्लोयमेन्ट नाम मिल्छ कि छैन पुष्टि गर्नुहोस्: `.env` (वा `agent.yaml`) मा `AZURE_AI_MODEL_DEPLOYMENT_NAME` र साइडबारमा वास्तविक डिप्लोयमेन्ट नाम तुलना गर्नुहोस्।
3. यदि डिप्लोयमेन्ट म्याद सकियो (फ्री टियर): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) बाट पुनः डिप्लोय गर्नुहोस् (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)।

---

## Foundry लोकल समस्याहरू (Path B)

### Foundry लोकल सेवा चलिरहेको छैन

```powershell
# स्थिति जाँच गर्नुहोस्
foundry local status

# सेवा रोकिने हो भने सुरु गर्नुहोस्
foundry local start
```

| लक्षण | कारण | समाधान |
|---------|-------|-----|
| हेल्थ चेकले `503` फर्काउँछ | सेवा सुरु भएको छैन | `foundry local start` चलाउनुहोस् वा Foundry Toolkit साइडबारमा **Start** क्लिक गर्नुहोस् |
| हेल्थ चेक टाइमआउट भयो | मोडेल अझै लोड हुँदैछ | सुरु भएपछि ३०–६० सेकेन्ड प्रतीक्षा गर्नुहोस्; ठूला मोडेलहरूलाई बढी समय लाग्छ |
| `/v1/health` मा `StatusCode: 404` | गलत पोर्ट | डिफल्ट `5273` हो। वास्तविक पोर्ट `foundry local status` बाट जाँच गर्नुहोस् |
| स्रोतहरू पर्याप्त छैनन् | Foundry लोकललाई लगभग ४ जीबी RAM खाली चाहिन्छ | अन्य एप्लिकेसनहरू बन्द गर्नुहोस् |
| मोडेल डाउनलोड असफल भयो | डिस्क ठाउँ कम छ | मोडेलहरू २–८ जीबी हुन्छन्। ठाउँ खाली गरेर `foundry model pull <name>` चलाउनुहोस् |

### मोडेल नाम मेल खाँदैन

```powershell
# डाउनलोड गरिएका मोडेलहरू र तिनीहरूको सटीक प्रतिरूपहरूको सूची बनाएर राख्नुहोस्
foundry model list
```

`.env` मा `AZURE_AI_MODEL_DEPLOYMENT_NAME` ठीक त्यही एलियस राख्नुहोस् जुन देखाइन्छ (जस्तै, `phi-4-mini`, `Phi-4-mini` होइन)।

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` लोकल रनमा (Path B)

ल्याबको `main.py` मा `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` प्रयोग गरिएको छ। Foundry लोकललाई यो चर स्थानीय सेवा देखाउनुपर्छ - **`AZURE_AI_PROJECT_ENDPOINT` होइन**। सुनिश्चित गर्नुहोस् कि तपाईको `.env` मा:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP टुल अझै बाहिरी कल गर्छ (Path B)

यो अपेक्षित छ। `search_microsoft_learn_for_plan` टुलले `https://learn.microsoft.com/api/mcp` बाट सिकाइ स्रोतहरू ल्याउँछ। **केवल कौशल-नाम प्रश्न नेटवर्कमा जान्छ** - रिजुमे र JD टेक्स्ट तपाईंको उपकरणमा पूर्णतः प्रशोधित हुन्छ र कहिल्यै प्रसारित हुँदैन। यदि पूर्ण अफलाइन अपरेशन चाहिन्छ भने, टुलमा एउटा `try/except` फालब्याक थप्नुहोस् जसले अन्तर्प्रयोग पहुँच नहुँदा स्थिर `learn.microsoft.com` URL फर्काउँछ।

---

## सहयोग लिनुहोस्

माथिका समाधान प्रयासपछि पनि समस्यामा परेमा:

1. **सर्भर लगहरू जाँच्नुहोस्** - धेरै त्रुटिहरू टर्मिनलमा Python stack trace उत्पन्न गर्छ। पूर्ण traceback पढ्नुहोस्।
2. **त्रुटि सन्देशन खोजी गर्नुहोस्** - त्रुटि पाठ कपी गरेर [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) मा खोज्नुहोस्।
3. **इश्यू खोल्नुहोस्** - [वर्कशप रिपोजिटरी](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) मा इश्यू फाइल गर्नुहोस् जसमा:
   - त्रुटि सन्देश वा स्क्रिनसट
   - तपाईंको प्याकेज संस्करणहरू (`pip list | Select-String "agent-framework"`)
   - तपाईंको Python संस्करण (`python --version`)
   - समस्या स्थानीय हो वा डिप्लोयमेन्ट पछि

---

### चेकप्वाइन्ट

- [ ] तपाईलाई `.env` कन्फिगरेसन समस्या जाँच्न र समाधान गर्न आउँछ
- [ ] तपाई प्याकेज संस्करणहरू आवश्यक म्याट्रिक्ससँग मेल गर्छ भनेर पुष्टि गर्न सक्नुहुन्छ
- [ ] कन्टेनर लगहरू डिप्लोयमेन्ट असफलताहरूको लागि कसरी जाँच्ने थाहा छ
- [ ] Azure Portal मा RBAC भूमिकाहरू जाँच्न सक्नुहुन्छ

---

**अघिल्लो:** [07 - Verify in Playground](07-verify-in-playground.md) · **पछिल्लो:** [09 - सारांश →](09-summary.md) · **होम:** [Lab 02 README](../README.md) · [वर्कशप होम](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी सही हुन प्रयास गर्छौं, तर कृपया जानकार हुनुस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छन्। मूल दस्तावेज़ यसको मूल भाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलत बुझाइ वा त्रुटिको लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->