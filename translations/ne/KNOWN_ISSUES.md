# ज्ञात समस्याहरू

यो दस्तावेजले हालको रिपोजिटरी अवस्थासँग सम्बन्धित ज्ञात समस्याहरूलाई ट्र्याक गर्दछ।

> अन्तिम अद्यावधिक: 2026-04-15। Python 3.13 / Windows मा `.venv_ga_test` अनुसार परीक्षण गरिएको।

---

## हालको प्याकेज पिनहरू (तीनवटै एजेन्टहरू)

| प्याकेज | हालको संस्करण |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(सुधारिएको — हेर्नुहोस् KI-003)* |

---

## KI-001 — GA 1.0.0 अपग्रेड अवरुद्ध: `agent-framework-azure-ai` हटाइयो

**स्थिति:** खुलेको | **गम्भीरता:** 🔴 उच्च | **प्रकार:** ब्रेकिंग

### वर्णन

`agent-framework-azure-ai` प्याकेज (पिन गरिएको `1.0.0rc3`) GA रिलिजमा (1.0.0, रिलिज मिति 2026-04-02) **हटाइयो/एबन्डन गरियो**।
यसलाई यसले प्रतिस्थापन गर्दछ:

- `agent-framework-foundry==1.0.0` — Foundry-होस्ट गरिएको एजेन्ट प्याटर्न
- `agent-framework-openai==1.0.0` — OpenAI-समर्थित एजेन्ट प्याटर्न

तीनवटै `main.py` फाइलहरूले `AzureAIAgentClient` लाई `agent_framework.azure` बाट इम्पोर्ट गर्छन्, जुन GA प्याकेजहरू अन्तर्गत `ImportError` उत्पन्न गर्दछ। GA मा `agent_framework.azure` नेमस्पेस अझै छ तर अब यसले Azure Functions क्लासहरू मात्र समावेश गर्दछ (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — Foundry एजेन्टहरू होइन।

### पुष्टि गरिएको त्रुटि (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### प्रभावित फाइलहरू

| फाइल | लाइन |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` सँग असंगत

**स्थिति:** खुलेको | **गम्भीरता:** 🔴 उच्च | **प्रकार:** ब्रेकिंग (अपस्ट्रीममा अवरुद्ध)

### वर्णन

`azure-ai-agentserver-agentframework==1.0.0b17` (सबैभन्दा नयाँ) ले कडा पिन गर्दछ
`agent-framework-core<=1.0.0rc3` लाई। यसलाई `agent-framework-core==1.0.0` (GA) सँग सँगै इन्स्टल गर्दा pip ले
`agent-framework-core` लाई फिर्ता `rc3` मा डाउनग्रेड गर्न बाध्य पार्छ, जसले `agent-framework-foundry==1.0.0` र
`agent-framework-openai==1.0.0` लाई भंग गर्दछ।

`from azure.ai.agentserver.agentframework import from_agent_framework` कल जुन सबै एजेन्टहरूले HTTP सर्भर बाइन्ड गर्न प्रयोग गर्छन्, त्यसैले पनि अवरुद्ध गरिएको छ।

### पुष्टि गरिएको निर्भरता द्वन्द्व (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### प्रभावित फाइलहरू

तीनवटै `main.py` फाइलहरू — माथिल्लो तहको इम्पोर्ट र `main()` भित्रको इम्पोर्ट दुवै।

---

## KI-003 — `agent-dev-cli --pre` झण्डा अब आवश्यक छैन

**स्थिति:** ✅ समाधान गरिएको (नॉन-ब्रेकिंग) | **गम्भीरता:** 🟢 कम

### वर्णन

सबै `requirements.txt` फाइलहरूले पहिले `agent-dev-cli --pre` समावेश गर्थे प्रि-रिलिज CLI ल्याउन। GA 1.0.0 रिलिज भएपछि (2026-04-02), `agent-dev-cli` को स्थिर रिलीज अब `--pre` झण्डा बिना उपलब्ध छ।

**समाधान लागू गरियो:** `--pre` झण्डा तीनवटै `requirements.txt` फाइलबाट हटाइयो।

---

## KI-004 — Dockerfileहरूले `python:3.14-slim` (प्रि-रिलिज बेस इमेज) प्रयोग गर्छन्

**स्थिति:** खुलेको | **गम्भीरता:** 🟡 कम

### वर्णन

सबै `Dockerfile` हरूले `FROM python:3.14-slim` प्रयोग गर्छन् जुन प्रि-रिलिज Python निर्माण ट्र्याक गर्छ।
उत्पादन डिप्लोइमेन्टहरूको लागि यसलाई स्थिर रिलीजमा पिन गर्नुपर्दछ (जस्तै, `python:3.12-slim`)।

### प्रभावित फाइलहरू

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## सन्दर्भहरू

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:  
यो दस्तावेज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी शुद्धताको प्रयास गर्छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धता हुनसक्छन्। मूल भाषामा रहेको दस्तावेजलाई आधिकारिक स्रोतको रूपमा मान्नु पर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलतफहमी वा गलत व्याख्याका लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->