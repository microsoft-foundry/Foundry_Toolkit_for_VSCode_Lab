# ज्ञात समस्याएं

यह दस्तावेज़ वर्तमान रिपॉजिटरी स्थिति के साथ ज्ञात समस्याओं को ट्रैक करता है।

> अंतिम अपडेट: 2026-04-15। Python 3.13 / Windows में `.venv_ga_test` के खिलाफ परीक्षण किया गया।

---

## वर्तमान पैकेज पिन (सभी तीन एजेंट)

| पैकेज | वर्तमान संस्करण |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(fix हुआ — देखें KI-003)* |

---

## KI-001 — GA 1.0.0 अपग्रेड अवरुद्ध: `agent-framework-azure-ai` हटा दिया गया

**स्थिति:** खुला | **गंभीरता:** 🔴 उच्च | **प्रकार:** ब्रेकिंग

### विवरण

`agent-framework-azure-ai` पैकेज (पिन किया गया `1.0.0rc3` पर) GA रिलीज़ (1.0.0, जारी 2026-04-02) में **हटा दिया गया / डिप्रीकेटेड** है। इसे निम्न द्वारा बदल दिया गया है:

- `agent-framework-foundry==1.0.0` — Foundry-होस्टेड एजेंट पैटर्न
- `agent-framework-openai==1.0.0` — OpenAI-संचालित एजेंट पैटर्न

तीनों `main.py` फाइलें `agent_framework.azure` से `AzureAIAgentClient` इंपोर्ट करती हैं, जो GA पैकेज के तहत `ImportError` उठाती है। GA में `agent_framework.azure` namespace अभी भी मौजूद है लेकिन अब इसमें केवल Azure Functions क्लासेस (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) शामिल हैं — Foundry एजेंट नहीं।

### पुष्टि की गई त्रुटि (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### प्रभावित फाइलें

| फाइल | पंक्ति |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` के अनुकूल नहीं

**स्थिति:** खुला | **गंभीरता:** 🔴 उच्च | **प्रकार:** ब्रेकिंग (अपस्ट्रीम पर अवरुद्ध)

### विवरण

`azure-ai-agentserver-agentframework==1.0.0b17` (नवीनतम) कड़ा पिन करता है
`agent-framework-core<=1.0.0rc3`। इसे `agent-framework-core==1.0.0` (GA) के साथ इंस्टॉल करने पर pip को `agent-framework-core` को फिर से `rc3` पर **डाउनग्रेड** करना पड़ता है, जिससे `agent-framework-foundry==1.0.0` और `agent-framework-openai==1.0.0` टूट जाते हैं।

इसलिए HTTP सर्वर को बाइंड करने के लिए सभी एजेंट द्वारा उपयोग किए जाने वाले `from azure.ai.agentserver.agentframework import from_agent_framework` कॉल भी अवरुद्ध हो जाता है।

### पुष्टि की गई निर्भरता संघर्ष (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### प्रभावित फाइलें

तीनों `main.py` फाइलें — शीर्ष-स्तर इंपोर्ट और `main()` में इन-फंक्शन इंपोर्ट दोनों।

---

## KI-003 — `agent-dev-cli --pre` फ्लैग अब आवश्यक नहीं

**स्थिति:** ✅ फिक्सेड (गैर-टूटने वाला) | **गंभीरता:** 🟢 कम

### विवरण

सभी `requirements.txt` फाइलों में पहले `agent-dev-cli --pre` शामिल था ताकि प्री-रिलीज CLI खींचा जा सके। चूंकि GA 1.0.0 2026-04-02 को जारी हो चुका है, `agent-dev-cli` का स्थिर संस्करण अब `--pre` फ्लैग के बिना उपलब्ध है।

**लागू सुधार:** सभी तीन `requirements.txt` फाइलों से `--pre` फ्लैग हटा दिया गया है।

---

## KI-004 — Dockerfiles में `python:3.14-slim` (प्री-रिलीज बेस इमेज) का उपयोग

**स्थिति:** खुला | **गंभीरता:** 🟡 कम

### विवरण

सभी `Dockerfile` में `FROM python:3.14-slim` का उपयोग होता है जो एक प्री-रिलीज Python बिल्ड को ट्रैक करता है।
प्रोडक्शन डिप्लॉयमेंट के लिए इसे एक स्थिर रिलीज (जैसे, `python:3.12-slim`) पर पिन किया जाना चाहिए।

### प्रभावित फाइलें

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
यह दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके अनूदित किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियाँ या गलतियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही अधिकारिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या व्याख्या के लिए हम उत्तरदायी नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->