# Module 8 - समस्या समाधान (बहु-एजेन्ट)

यो मोड्युल बहु-एजेन्ट कार्यप्रवाहसँग सम्बन्धित सामान्य त्रुटिहरू, समाधानहरू, र डिबग रणनीतिहरू समेट्छ। साधारण Foundry डिप्लोयमेन्ट समस्याहरूका लागि, कृपया [Lab 01 समस्या समाधान गाइड](../../lab01-single-agent/docs/08-troubleshooting.md) पनि सन्दर्भ गर्नुहोस्।

---

## छिटो सन्दर्भ: त्रुटि → समाधान

| त्रुटि / लक्षण | सम्भावित कारण | समाधान |
|----------------|--------------|--------|
| `RuntimeError: Missing required environment variable(s)` | `.env` फाइल हराएको वा मानहरू सेट गरिएको छैन | `.env` बनाउनुहोस् `PROJECT_ENDPOINT=<your-endpoint>` र `MODEL_DEPLOYMENT_NAME=<your-model>` सहित |
| `ModuleNotFoundError: No module named 'agent_framework'` | भर्चुअल वातावरण सक्रिय गरिएको छैन वा निर्भरताहरू इन्स्टल गरिएको छैन | चलाउनुहोस् `.\.venv\Scripts\Activate.ps1` त्यसपछि `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP प्याकेज इन्स्टल गरिएको छैन (requirements बाट हराएको) | चलाउनुहोस् `pip install mcp` वा जाँच गर्नुहोस् `requirements.txt` मा ट्रान्जिटिभ निर्भरता रूपमा रहेको छ |
| एजेन्ट सुरु हुन्छ तर खाली प्रतिक्रिया फर्काउँछ | `output_executors` मेल खाएको छैन वा एजहरू हराएका छन् | सुनिश्चित गर्नुहोस् `output_executors=[gap_analyzer]` र सबै एजहरू `create_workflow()` मा छन् |
| केवल १ ग्याप कार्ड (बाकी हराएका) | GapAnalyzer निर्देशन अधुरो छ | `CRITICAL:` अनुच्छेद थप्नुहोस् `GAP_ANALYZER_INSTRUCTIONS` मा - हेर्नुहोस् [Module 3](03-configure-agents.md) |
| फिट स्कोर ० छ वा छैन | MatchingAgent माथिल्लो डेटा प्राप्त गरेको छैन | दुईवटै `add_edge(resume_parser, matching_agent)` र `add_edge(jd_agent, matching_agent)` सुनिश्चित गर्नुहोस् |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP सर्भरले टुल कल अस्वीकृत गर्‍यो | इन्टरनेट जडान जाँच गर्नुहोस्। ब्राउजरमा `https://learn.microsoft.com/api/mcp` खोल्नुहोस्। फेरि प्रयास गर्नुहोस् |
| आउटपुटमा माइक्रोसफ्ट लर्न URLs छैन | MCP टुल दर्ता गरिएको छैन वा अन्तबिन्दु गलत छ | सुनिश्चित गर्नुहोस् `tools=[search_microsoft_learn_for_plan]` GapAnalyzer मा र `MICROSOFT_LEARN_MCP_ENDPOINT` सही छ |
| `Address already in use: port 8088` | अर्को प्रक्रिया पोर्ट ८०८८ प्रयोग गर्दैछ | चलाउनुहोस् `netstat -ano \| findstr :8088` (Windows) वा `lsof -i :8088` (macOS/Linux) र टकराव हुने प्रक्रिया बन्द गर्नुहोस् |
| `Address already in use: port 5679` | Debugpy पोर्ट टकराव | अन्य डिबग सेसनहरू रोक्नुहोस्। चलाउनुहोस् `netstat -ano \| findstr :5679` प्रक्रिया पत्ता लगाउन र समाप्त गर्न |
| एजेन्ट इन्स्पेक्टर खोल्दैन | सर्भर पूर्णरुपमा सुरु भएको छैन वा पोर्ट टकराव छ | "Server running" लग सुन्नुहोस्। पोर्ट 5679 खाली छ कि छैन जाँच्नुहोस् |
| `azure.identity.CredentialUnavailableError` | Azure CLI मा लगइन गरिएको छैन | चलाउनुहोस् `az login` त्यसपछि सर्भर पुनः सुरु गर्नुहोस् |
| `azure.core.exceptions.ResourceNotFoundError` | मोडेल डिप्लोयमेन्ट अवस्थित छैन | `MODEL_DEPLOYMENT_NAME` ले तपाईंको Foundry प्रोजेक्टमा डिप्लोय गरिएको मोडेलसँग मेल खान्छ कि छैन जाँच्नुहोस् |
| डिप्लोयमेन्ट पछि कन्टेनर स्थिति "Failed" | सुरु हुँदाचाहिँ कन्टेनर क्र्यास भयो | Foundry साइडबारमा कन्टेनर लगहरू जाँच्नुहोस्। सामान्य: env var हराएको वा इम्पोर्ट त्रुटि |
| डिप्लोयमेन्ट "Pending" > ५ मिनेट देखाइएको छ | कन्टेनर सुरु हुन धेरै समय लागिरहेको छ वा स्रोत सीमाहरू | बहु-एजेन्टका लागि ५ मिनेटसम्म पर्खनुहोस् (४ एजेन्ट इन्स्टान्सहरू सिर्जना गर्छ)। यदि अझै Pending छ भने लगहरू जाँच्नुहोस् |
| `ValueError` `WorkflowBuilder` बाट | अवैध ग्राफ कन्फिगरेसन | सुनिश्चित गर्नुहोस् `start_executor` सेट गरिएको छ, `output_executors` सूची हो, र कुनै परिक्रमण एजहरू छैनन् |

---

## वातावरण र कन्फिगरेसन समस्याहरू

### हराएको वा गलत `.env` मानहरू

`.env` फाइल `PersonalCareerCopilot/` डिरेक्टोरीमा हुनुपर्छ (`main.py` सँगै):

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

> **तपाईंको PROJECT_ENDPOINT कसरी पत्ता लगाउने:**  
- VS Code मा **Microsoft Foundry** साइडबार खोल्नुहोस् → आफ्नो प्रोजेक्टमा र क्लिक गर्नुहोस् र **Copy Project Endpoint** चयन गर्नुहोस्।  
- वा [Azure Portal](https://portal.azure.com) मा जानुहोस् → आफ्नो Foundry प्रोजेक्ट → **Overview** → **Project endpoint**।

> **तपाईंको MODEL_DEPLOYMENT_NAME कसरी पत्ता लगाउने:** Foundry साइडबारमा आफ्नो प्रोजेक्ट विस्तार गर्नुहोस् → **Models** → तपाईंले डिप्लोय गरेको मोडेल नाम फेला पार्नुहोस् (जस्तै `gpt-4.1-mini`)।

### Env var प्राथमिकता

`main.py` ले `load_dotenv(override=False)` प्रयोग गर्दछ, जसको अर्थ:

| प्राथमिकता | स्रोत | दुबै सेट हुँदा कस्को जीत हुन्छ? |
|----------|--------|-----------------------|
| १ (सबैभन्दा माथि) | शेल वातावरण भेरिएबल | हो |
| २ | `.env` फाइल | शेल भेरिएबल सेट नभए मात्र |

यसको अर्थ Foundry रनटाइम वातावरण भेरिएबलहरू (`agent.yaml` मार्फत सेट गरिएका) होस्टेड डिप्लोयमेन्टमा `.env` मानहरू भन्दा प्राथमिक हुन्छन्।

---

## संस्करण अनुकूलता

### प्याकेज संस्करण म्याट्रिक्स

बहु-एजेन्ट कार्यप्रवाहलाई निश्चित प्याकेज संस्करणहरू आवश्यक पर्छन्। बेमेल संस्करणहरूले रनटाइम त्रुटिहरू ल्याउन सक्छन्।

| प्याकेज | आवश्यक संस्करण | जाँच आदेश |
|---------|----------------|-----------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | नयाँ प्रि-रिलिज | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### सामान्य संस्करण त्रुटिहरू

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# सुधार गर्नुहोस्: rc3 मा उन्नयन गर्नुहोस्
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` फेला परेन वा इन्स्पेक्टर असंगत:**

```powershell
# समाधान: --pre फ्ल्यागसहित स्थापना गर्नुहोस्
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# सुधार गर्नुहोस्: mcp प्याकेज उन्नयन गर्नुहोस्
pip install mcp --upgrade
```

### सबै संस्करणहरू एकैचोटि जाँच्नुहोस्

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

## MCP टुल समस्याहरू

### MCP टुलले परिणाम फर्काउँदैन

**लक्षण:** Gap कार्डहरूले "No results returned from Microsoft Learn MCP" वा "No direct Microsoft Learn results found" भन्छ।

**सम्भावित कारणहरू:**

1. **नेटवर्क समस्या** - MCP अन्तबिन्दु (`https://learn.microsoft.com/api/mcp`) पहुँचयोग्य छैन।
   ```powershell
   # जडान जाँच्नुहोस्
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   यदि यसले `200` फर्कायो भने, अन्तबिन्दु पहुँचयोग्य छ।

2. **प्रश्न धेरै विशेष** - कौशल नाम Microsoft Learn खोजका लागि धेरै निचो छ।
   - यसलाई अत्यन्त विशेष गरिएका कौशलहरूका लागि अपेक्षित मानिन्छ। टुलसँग प्रतिक्रिया भित्र फ्यालब्याक URL हुन्छ।

3. **MCP सत्र टाइमआउट** - Streamable HTTP जडान टाइमआउट भयो।
   - अनुरोध फेरि प्रयास गर्नुहोस्। MCP सत्रहरू अस्थायी हुन्छन् र पुनः जडान आवश्यक हुन सक्छ।

### MCP लगहरू व्याख्या

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| लग | अर्थ | क्रिया |
|----|-------|--------|
| `GET → 405` | इनिसियलाइजसनको क्रममा MCP क्लाइन्ट प्रब्स | सामान्य - बेवास्ता गर्नुहोस् |
| `POST → 200` | टुल कल सफल भयो | अपेक्षित |
| `DELETE → 405` | क्लिनअपमा MCP क्लाइन्ट प्रब्स | सामान्य - बेवास्ता गर्नुहोस् |
| `POST → 400` | खराब अनुरोध (गलत ढाँचाको प्रश्न) | `search_microsoft_learn_for_plan()` मा `query` प्यारामिटर जाँच्नुहोस् |
| `POST → 429` | रेट लिमिटेड | पर्खनुहोस् र पुन: प्रयास गर्नुहोस्। `max_results` प्यारामिटर घटाउनुहोस् |
| `POST → 500` | MCP सर्भर त्रुटि | अस्थायी - पुन: प्रयास गर्नुहोस्। यदि लगातार छ भने Microsoft Learn MCP API डाउन हुन सक्छ |
| जडान टाइमआउट | नेटवर्क समस्या वा MCP सर्भर अनुपलब्ध | इन्टरनेट जाँच गर्नुहोस्। चलाउनुहोस् `curl https://learn.microsoft.com/api/mcp` |

---

## डिप्लोयमेन्ट समस्याहरू

### डिप्लोयमेन्टपछि कन्टेनर सुरु हुन असफल

1. **कन्टेनर लगहरू जाँच्नुहोस्:**
   - Microsoft Foundry साइडबार खोल्नुहोस् → **Hosted Agents (Preview)** विस्तार गर्नुहोस् → आफ्नो एजेन्टमा क्लिक गर्नुहोस् → संस्करण विस्तार गर्नुहोस् → **Container Details** → **Logs**।
   - Python स्ट्याक ट्रेस वा हराएको मोड्युल त्रुटि खोज्नुहोस्।

2. **सामान्य कन्टेनर स्टार्टअप असफलताहरू:**

   | लगमा त्रुटि | कारण | समाधान |
   |-------------|-------|--------|
   | `ModuleNotFoundError` | `requirements.txt` मा प्याकेज हराएको | प्याकेज थप्नुहोस्, पुन: डिप्लोय गर्नुहोस् |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` मा env vars सेट छैनन् | `agent.yaml` → `environment_variables` खण्ड अपडेट गर्नुहोस् |
   | `azure.identity.CredentialUnavailableError` | Managed Identity कन्फिगर गरिएको छैन | Foundry यसलाई स्वचालित रूपमा सेट गर्छ - विस्तारमार्फत डिप्लोय गरिरहेको छ कि छैन सुनिश्चित गर्नुहोस् |
   | `OSError: port 8088 already in use` | Dockerfile मा गलत पोर्ट एक्सपोज गरिएको वा पोर्ट टकराव | Dockerfile मा `EXPOSE 8088` र `CMD ["python", "main.py"]` जाँच्नुहोस् |
   | कन्टेनर कोड 1 संग बाहिरिन्छ | `main()` मा ह्यान्डल नगरिएको अपवाद | पहिले स्थानीय परीक्षण गर्नुहोस् ([Module 5](05-test-locally.md)) ताकि त्रुटिहरू पत्ता लगाउन सकियोस् |

3. **समस्या समाधानपछि पुन:डिप्लोय:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → उही एजेन्ट चयन गर्नुहोस् → नयाँ संस्करण डिप्लोय गर्नुहोस्।

### डिप्लोयमेन्ट धेरै समय लिन्छ

बहु-एजेन्ट कन्टेनरहरूले सुरु हुँदा ४ एजेन्ट इन्स्टान्स सिर्जना गर्ने भएकाले स्टार्टअप समय बढी लाग्छ। सामान्य स्टार्टअप समयहरू:

| चरण | अपेक्षित अवधि |
|-------|------------------|
| कन्टेनर इमेज निर्माण | १-३ मिनेट |
| इमेज ACR मा पठाउने | ३०-६० सेकेन्ड |
| कन्टेनर सुरु (एकल एजेन्ट) | १५-३० सेकेन्ड |
| कन्टेनर सुरु (बहु-एजेन्ट) | ३०-१२० सेकेन्ड |
| प्लेग्राउन्डमा एजेन्ट उपलब्ध | "Started" पछि १-२ मिनेट |

> यदि "Pending" स्थिति ५ मिनेटभन्दा लामो रहन्छ भने, कन्टेनर लगहरूमा त्रुटिहरू जाँच्नुहोस्।

---

## RBAC र अनुमतिहरू समस्या

### `403 Forbidden` वा `AuthorizationFailed`

तपाईंलाई Foundry प्रोजेक्टमा **[Azure AI User](https://aka.ms/foundry-ext-project-role)** भूमिका आवश्यक छ:

1. [Azure Portal](https://portal.azure.com) मा जानुहोस् → तपाईंको Foundry **प्रोजेक्ट** स्रोत।
2. क्लिक गर्नुहोस् **Access control (IAM)** → **Role assignments**।
3. तपाईंको नाम खोज्नुहोस् → पुष्टि गर्नुहोस् **Azure AI User** सूचीमा छ।
4. यदि छैन भने: **Add** → **Add role assignment** → **Azure AI User** खोज्नुहोस् → तपाईंको खातामा असाइन गर्नुहोस्।

विवरणहरूको लागि [Microsoft Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) कागजात हेर्नुहोस्।

### मोडेल डिप्लोयमेन्ट पहुँचयोग्य छैन

एजेन्टले मोडेल सम्बन्धित त्रुटि फर्काएमा:

1. मोडेल डिप्लोय गरिएको छ कि छैन सुनिश्चित गर्नुहोस्: Foundry साइडबार → प्रोजेक्ट विस्तार → **Models** → `gpt-4.1-mini` (वा तपाईंको मोडेल) स्थिति **Succeeded** छ कि छैन जाँच्नुहोस्।
2. डिप्लोयमेन्ट नाम मिलेको छ कि छैन जाँच्नुहोस्: `.env` (वा `agent.yaml`) मा `MODEL_DEPLOYMENT_NAME` साइडबारको वास्तविक डिप्लोयमेन्ट नामसँग तुलना गर्नुहोस्।
3. यदि डिप्लोयमेन्ट समाप्त भयो (फ्री टियरमा): [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) बाट पुनःडिप्लोय गर्नुहोस् (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)।

---

## एजेन्ट इन्स्पेक्टर समस्याहरू

### इन्स्पेक्टर खुल्छ तर "Disconnected" देखाउँछ

1. सर्भर चलिरहेको छ कि छैन सुनिश्चित गर्नुहोस्: टर्मिनलमा "Server running on http://localhost:8088" देखिन्छ कि हेर्नुहोस्।
2. पोर्ट `5679` जाँच्नुहोस्: इन्स्पेक्टर debugpy मार्फत पोर्ट 5679 मा जडान हुन्छ।
   ```powershell
   netstat -ano | findstr :5679
   ```
3. सर्भर पुनः सुरु गरेर इन्स्पेक्टर फेरी खोल्नुहोस्।

### इन्स्पेक्टरले आंशिक प्रतिक्रिया देखाउँछ

बहु-एजेन्ट प्रतिक्रियाहरू लामो हुन्छन् र क्रमशः स्ट्रिम हुन्छन्। पूर्ण प्रतिक्रिया सकिएपछि मात्र हेर्नुहोस् (जति ग्याप कार्डहरू र MCP टुल कलहरू छन् त्यस अनुसार ३०-६० सेकेन्ड लाग्न सक्छ)।

यदि प्रतिक्रिया नियमित रूपमा कटौती हुन्छ भने:  
- GapAnalyzer निर्देशनहरूमा `CRITICAL:` ब्लक रहेको छ कि हेर्नुहोस् जसले ग्याप कार्डहरू जोड्नबाट रोक्छ।  
- तपाईंको मोडेलको टोकन सीमा जाँच्नुहोस् - `gpt-4.1-mini` ले ३२ हजार आउटपुट टोकन समर्थन गर्छ, जुन पर्याप्त हुनु पर्छ।

---

## प्रदर्शन सुझावहरू

### बिस्तारै प्रतिक्रियाहरू

बहु-एजेन्ट कार्यप्रवाहहरू एकल एजेन्टको तुलनामा क्रमागत निर्भरताहरू र MCP टुल कलहरूको कारण स्वाभाविक रूपमा ढिलो हुन्छन्।

| अनुकूलन | कसरी गर्ने | प्रभाव |
|-------------|--------------|---------|
| MCP कलहरू घटाउनुहोस् | टुलमा `max_results` प्यारामिटर कम गर्नुहोस् | कम HTTP राउन्ड-ट्रिप्स |
| निर्देशनहरू सजिलो बनाउनुहोस् | एजेन्ट प्रॉम्प्टहरू छोटा र फोकस्ड बनाउनुहोस् | छिटो LLM inference |
| `gpt-4.1-mini` प्रयोग गर्नुहोस् | विकासका लागि `gpt-4.1` भन्दा छिटो | करिब २ गुणा गति सुधार |
| ग्याप कार्ड विवरण घटाउनुहोस् | GapAnalyzer निर्देशनमा ग्याप कार्ड फारम्याट सजिलो बनाउनुहोस् | उत्पादन कम गर्नुहोस् |

### सामान्य प्रतिक्रिया समय (स्थानीय)

| कन्फिगरेसन | अपेक्षित समय |
|--------------|---------------|
| `gpt-4.1-mini`, ३-५ ग्याप कार्ड | ३०-६० सेकेन्ड |
| `gpt-4.1-mini`, ८+ ग्याप कार्ड | ६०-१२० सेकेन्ड |
| `gpt-4.1`, ३-५ ग्याप कार्ड | ६०-१२० सेकेन्ड |
---

## सहयोग प्राप्त गर्नुहोस्

माथि उल्लेखित समाधानहरू प्रयास गरेपछि यदि तपाईं अड्किनु भयो भने:

1. **सर्भर लगहरू जाँच गर्नुहोस्** - धेरै त्रुटिहरूले टर्मिनलमा Python स्ट्याक ट्रेस उत्पादन गर्छन्। पूर्ण ट्रेसब्याक पढ्नुहोस्।
2. **त्रुटि सन्देश खोज्नुहोस्** - त्रुटि पाठलाई कपी गरी [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) मा खोज्नुहोस्।
3. **समस्या खोल्नुहोस्** - [वर्कशप रिपोजिटरी](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) मा समस्या दर्ता गर्नुहोस् जसमा:
   - त्रुटि सन्देश वा स्क्रीनसट
   - तपाईंको प्याकेज भर्सनहरू (`pip list | Select-String "agent-framework"`)
   - तपाईंको Python भर्सन (`python --version`)
   - समस्या स्थानीय छ कि परिनियोजन पछि

---

### जाँच बिन्दु

- [ ] तपाईं छिटो सन्दर्भ तालिका प्रयोग गरेर सबैभन्दा सामान्य बहु-एजेन्ट त्रुटिहरू पहिचान र समाधान गर्न सक्नुहुन्छ
- [ ] तपाईं `.env` कन्फिगरेसन समस्याहरू जाँच र समाधान गर्ने तरिका जान्नुहुन्छ
- [ ] तपाईं प्याकेज भर्सनहरू आवाश्यक म्याट्रिक्ससँग मेल खान्छ वा भेरिफाइ गर्न सक्नुहुन्छ
- [ ] तपाईं MCP लग प्रविष्टिहरू बुझ्नुहुन्छ र उपकरण विफलताहरूको निदान गर्न सक्नुहुन्छ
- [ ] तपाईं परिनियोजन असफलताका लागि कन्टेनर लगहरू जाँच गर्ने तरिका जान्नुहुन्छ
- [ ] तपाईं Azure पोर्टलमा RBAC भूमिका प्रमाणित गर्न सक्नुहुन्छ

---

**अघिल्लो:** [07 - Verify in Playground](07-verify-in-playground.md) · **गृहपृष्ठ:** [Lab 02 README](../README.md) · [वर्कशप गृहपृष्ठ](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:  
यस दस्तावेजलाई AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी शुद्धताको प्रयास गर्छौं, तर कृपया बुझ्नुस् कि स्वचालित अनुवादमा त्रुटि वा असत्यताहरू हुन सक्ने सम्भावना छ। मूल दस्तावेज यसको मूल भाषामा मात्र आधिकारिक स्रोत मानिन्छ। महत्वपूर्ण जानकारीका लागि, व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट हुने कुनै पनि गलत बुझाइ वा गलत व्याख्याका लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->