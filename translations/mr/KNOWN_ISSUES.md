# ज्ञात समस्या

हा दस्तऐवज सध्याच्या रेपॉझिटरी स्थितीसह ज्ञात समस्या ट्रॅक करतो.

> शेवटचे अद्यतन: 2026-04-15. Python 3.13 / Windows मध्ये `.venv_ga_test` साठी चाचणी घेतलेली.

---

## सध्याच्या पॅकेज पिन (सर्व तीन एजंटसाठी)

| पॅकेज | सध्याचा आवृत्ती |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(निश्चित केलेले — पहा KI-003)* |

---

## KI-001 — GA 1.0.0 सुधारणा अडवली: `agent-framework-azure-ai` काढले गेले

**स्थिती:** खुले | **तीव्रता:** 🔴 उच्च | **प्रकार:** ब्रेकिंग

### वर्णन

`agent-framework-azure-ai` पॅकेज (पिन केलेले `1.0.0rc3` येथे) GA रिलीजमध्ये (1.0.0, 2026-04-02 रोजी प्रकाशित) **काढले/डिप्रिकेट केले** गेले आहे. हे खालीलने बदलले गेले आहे:

- `agent-framework-foundry==1.0.0` — Foundry-होस्ट केलेला एजंट पॅटर्न
- `agent-framework-openai==1.0.0` — OpenAI-आधारित एजंट पॅटर्न

सर्व तीन `main.py` फाइल्स `agent_framework.azure` मधून `AzureAIAgentClient` आयात करतात, जे GA पॅकेजेसमध्ये `ImportError` निर्माण करते. `agent_framework.azure` नावावरील जागा GA मध्ये अजूनही आहे परंतु आता त्यात फक्त Azure Functions वर्ग आहेत (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — Foundry एजंट नाहीत.

### निश्चित झालेली त्रुटी (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### प्रभावित फाइल्स

| फाइल | ओळ |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` सह सुसंगत नाही

**स्थिती:** खुले | **तीव्रता:** 🔴 उच्च | **प्रकार:** ब्रेकिंग (अपस्ट्रीमवर अवलंबून)

### वर्णन

`azure-ai-agentserver-agentframework==1.0.0b17` (सर्वात अलीकडील) कडकपणे पिन करते `agent-framework-core<=1.0.0rc3`. त्यास `agent-framework-core==1.0.0` (GA) सह स्थापित केल्यास pip ला `agent-framework-core` परत `rc3` पर्यंत डाउनग्रेड करावे लागते, ज्यामुळे `agent-framework-foundry==1.0.0` आणि `agent-framework-openai==1.0.0` मोडतात.

सर्व एजंटसाठी HTTP सर्वर बांधण्यासाठी वापरण्यात येणारा `from azure.ai.agentserver.agentframework import from_agent_framework` कॉल देखील अडवलेला आहे.

### निश्चित झालेली अवलंबित्व संघर्ष (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### प्रभावित फाइल्स

सर्व तीन `main.py` फाइल्स — टॉप-लेव्हल आयात आणि `main()` मधील इन-फंक्शन आयात दोन्ही.

---

## KI-003 — `agent-dev-cli --pre` फ्लॅग आवश्यक नाही

**स्थिती:** ✅ निश्चित (ब्रेकिंग नाही) | **तीव्रता:** 🟢 कमी

### वर्णन

सर्व `requirements.txt` फाइल्स आधी `agent-dev-cli --pre` याचा वापर प्री-रिलीज CLI डाउनलोड करण्यासाठी करायच्या. 2026-04-02 रोजी GA 1.0.0 रिलीज झाल्यानंतर, `agent-dev-cli` चा स्थिर प्रकाशन आता `--pre` फ्लॅगशिवाय उपलब्ध आहे.

**सुधारणा लागू केली:** सर्व तीन `requirements.txt` फाइल्समधून `--pre` फ्लॅग काढले गेले आहे.

---

## KI-004 — Dockerfile मध्ये `python:3.14-slim` (प्री-रिलीज बेस इमेज) चा वापर

**स्थिती:** खुले | **तीव्रता:** 🟡 कमी

### वर्णन

सर्व Dockerfile मध्ये `FROM python:3.14-slim` वापरले आहे, जे प्री-रिलीज Python बिल्डवर आधारित आहे. उत्पादनासाठी हे स्थिर रिलीज (उदा. `python:3.12-slim`) वर पिन केले पाहिजे.

### प्रभावित फाइल्स

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## संदर्भ

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित केला आहे. जरी आम्ही अचूकतेसाठी प्रयत्नशील आहोत, तरी कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये त्रुटी किंवा गैरसमज असू शकतात. मूळ दस्तऐवज त्याच्या मातृभाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहिती साठी व्यावसायिक मानवी अनुवाद शिफारस केलेला आहे. या अनुवादाच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थव्यवस्थेसाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->