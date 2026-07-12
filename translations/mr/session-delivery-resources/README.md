# हा सेशन कसा सादर करायचा

हा सेशन सादर केल्याबद्दल धन्यवाद!

कार्यशाळा सादर करण्यापूर्वी, कृपया:

1. हा दस्तऐवज आणि सर्व अंतर्भूत स्रोत पूर्णपणे वाचा.
2. सेशन वितरणाचे रेकॉर्डिंग आणि कार्यशाळेचे अखेरपर्यंत चालणारे walkthrough पहा.
3. प्रत्येक हाताळणी लॅब आपल्या स्वतःच्या संगणकावर **किमान एकदा** संपूर्णपणे चालवून पहा.
4. आपल्या Microsoft Foundry प्रकल्प, मॉडेल तैनाती, आणि कोटा तपासा.
5. काहीही अस्पष्ट असल्यास देखभाल करणाऱ्याशी संपर्क करा.

---

## फाइल सारांश

| संसाधन                      | दुवा                                                                             | वर्णन                                                                                     |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| कार्यशाळा स्लाइड डेक           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | प्रस्तुती स्लाइड्स या कार्यशाळेसाठी सादर करणाऱ्याचे नोट्स आणि एम्बेड केलेले डेमो व्हिडिओसह |
| सेशन वितरण रेकॉर्डिंग        | _देखभाल करणाऱ्याद्वारे पुरवले जाईल_                                               | कार्यशाळा परिचय आणि स्लाइड walkthrough रेकॉर्डिंग                                          |
| कार्यशाळा अखेरपर्यंत रेकॉर्डिंग | _देखभाल करणाऱ्याद्वारे पुरवले जाईल_                                               | दोन्ही लॅब्सचे शिकणाऱ्याच्या दृष्टीकोनातून अखेरपर्यंत रेकॉर्डिंग                            |
| कार्यशाळा दस्तऐवज            | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | स्रोत रिपॉझिटरी, लॅब README, टप्प्याटप्प्याने मॉड्यूल                                      |
| लॅब 01 - सिंगल एजंट          | [Lab 01](../workshop/lab01-single-agent/README.md)                               | हाताळणी लॅब: *Explain Like I'm an Executive* होस्टेड एजंट तयार करा, चाचणी द्या, आणि तैनात करा     |
| लॅब 02 - मल्टी-एजंट वर्कफ्लो | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | हाताळणी लॅब: 4-एजंट *Resume to Job Fit Evaluator* वर्कफ्लो तयार करा                     |
| डेमो 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | लॅब 01 डेमो: तांत्रिक झागण (jargon) चे कार्यकारी सारांशात भाषांतर करा                          |
| डेमो 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | लॅब 02 डेमो: 4-एजंट वर्कफ्लो जो रिज्युमे-जॉब फिट स्कोर करतो आणि शिफारशी तयार करतो            |

> **ट्रेनर्ससाठी नोंद:** स्लाइड डेक आणि व्हिडिओ दुवे रेकॉर्डिंग प्रकाशित झाल्यानंतर जोडले जातील. तोपर्यंत, ताज्या स्रोतांसाठी देखभाल करणाऱ्याला (बघा [Contacts](#संपर्क)) विचारा.

---

## सुरूवात करा

ही कार्यशाळा विकसकांना शिकवते की कसे AI एजंट तयार, चाचणी, आणि तैनात करायचे **Microsoft Foundry Agent Service** मध्ये **Hosted Agents** म्हणून संपूर्णपणे VS Code वापरून, **Microsoft Foundry Toolkit** विस्तार वापरून.

कार्यशाळा अनेक विभागांमध्ये विभागलेले आहे ज्यात स्लाइड्स, **2 थेट डेमो**, आणि **2 हाताळणी लॅब्स** आहेत.

### वेळापत्रक

#### पूर्ण वितरण (सुमारे 2 तास)

| वेळ            | वर्णन                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | परिचय: होस्टेड एजंट, Foundry Agent Service, आणि टूलकिट         |
| 10:00 - 20:00   | डेमो: Executive Agent अखेरपर्यंत                                     |
| 20:00 - 60:00   | लॅब 01 - सिंगल एजंट (बिल्ड, स्थानिक चाचणी, तैनात, प्लेग्राउंड)     |
| 60:00 - 110:00  | लॅब 02 - मल्टी-एजंट वर्कफ्लो (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00 | समाप्ती, प्रश्नोत्तरे, आणि पुढील शिक्षण संसाधने                       |

#### लहान वितरण (सुमारे 75 मिनिटे)

| वेळ          | वर्णन                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | परिचय आणि आढावा                                           |
| 10:00 - 20:00 | डेमो: Executive Agent                                        |
| 20:00 - 70:00 | फक्त लॅब 01 (सुधारितपणे लॅब 02 कडे पाहण्याचा निर्देश द्या)        |
| 70:00 - 75:00 | समाप्ती आणि प्रश्नोत्तरे                                              |

### तयारी

| संसाधन                       | दुवा                                                                                          | वर्णन                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| कार्यशाळा दस्तऐवज         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | कार्यशाळा दस्तऐवज आणि स्रोत                 |
| लॅब 01 सूचना            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | हाताळणी लॅब: एकल होस्टेड एजंट                 |
| लॅब 02 सूचना            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | हाताळणी लॅब: मल्टी-एजंट वर्कफ्लो                |
| पूर्वअट यादी        | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | आवश्यक उपकरणे, खाते, आणि Azure प्रवेश        |
| होस्टेड एजंट्स जलद प्रारंभ (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | `azd` सह होस्टेड एजंट तैनात करण्यासाठी अधिकृत जलद प्रारंभ  |
| होस्टेड एजंट्स प्रदेश उपलब्धता | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | होस्टेड एजंटसाठी समर्थित प्रदेश (आधीच पाहणी)     |

### ट्रेनर पूर्वअटी

आपण वितरित करण्यापूर्वी, याची खात्री करा की:

- संसाधने तयार करण्याचा परवानग्यांसह एक **Azure सदस्यता** (Owner किंवा Contributor म्हणून).
- एक **Microsoft Foundry प्रकल्प** [होस्टेड एजंटसाठी समर्थित प्रदेशामध्ये](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- आपल्या Foundry प्रकल्पात **gpt-4.1** (किंवा **gpt-4.1-mini**) साठी कोटा.
- पुढील उपकरणे स्थापित केली आहेत:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (ऐच्छिक)
  - Python 3.10 किंवा नंतरचे आवृत्ती

किमान एकदा [Hosted agents quickstart with `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) चालवा जेणेकरून आपल्याकडे चांगला ओळखलेला Foundry प्रकल्प, मॉडेल तैनाती, आणि Azure कंटेनर रजिस्ट्रि संदर्भासाठी असेल जर शिकणारा अडकला तर.

---

## स्लाइड walkthrough

डेक लॅब्सप्रमाणेच फ्लो अनुसरते. प्रत्येक विभागासाठी सूचित केल्या गेलेल्या बोलण्याच्या मुद्द्यांचा सारांश:

| विभाग                     | मुख्य संदेश                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| शीर्षक आणि अजेंडाः            | कार्यशाळा *VS Code ते Foundry* म्हणून फ्रेम करा जिथे कोणतेही पोर्टल स्विचिंग आवश्यक नाही.                                |
| का होस्टेड एजंट्स?          | व्यवस्थापित रनटाइम, ACR-आधारित तैनाती, OpenAI-शी सुसंगत `/responses` API, Foundry प्रकल्पांशी मर्यादित.        |
| वास्तुकला आरेख            | [README वास्तुकला](../README.md#architecture) मधून पुढे जा: scaffold, Inspector, ACR, Agent Service.   |
| होस्टेड एजंट ची रचना   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - प्रत्येक फाइल काय करते.                              |
| थेट डेमो: Executive Agent  | VS Code कडे स्विच करा आणि [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) डेमो अखेरपर्यंत चालवा (बघा [Demo 1](#डेमो-1-executive-agent)). |
| थेट डेमो: Resume to Job Fit Evaluator | VS Code कडे स्विच करा आणि [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-एजंट डेमो चालवा (बघा [Demo 2](#डेमो-2-resume-to-job-fit-evaluator)). |
| लॅब 01 सारांश                | शिकणाऱ्यांना सोपवा. [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md) कडे निर्देश करा. |
| मल्टी-एजंट नमुने        | साखळीप्रमाणे विरुद्ध एकाचवेळी विरुद्ध हँडऑफ - लॅब 02 सुरू होण्यापूर्वी पूर्वावलोकन करा.                                           |
| लॅब 02 सारांश                | शिकणाऱ्यांना सोपवा. [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md) कडे निर्देश करा. |
| समाप्ती आणि संसाधने       | [अतिरिक्त संसाधने](#अतिरिक्त-संसाधने) विभागाकडून पुढील शिक्षणासाठी दुवे.                      |

---

## डेमो

वितरणात दोन थेट डेमो समाविष्ट आहेत. प्रत्येकासाठी 10 मिनिटे राखून ठेवा.

| डेमो | लॅब | फाइल्स | काय दाखवायचे |
|------|-----|-------|--------------|
| Executive Agent | लॅब 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | एकल होस्टेड एजंट; तांत्रिक झागण (jargon) चे कार्यकारी सारांशात भाषांतर करा |
| Resume to Job Fit Evaluator | लॅब 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-एजंट संयोजन; रिज्युमे-जॉब फिट स्कोर करा आणि शिफारस तयार करा |

### डेमो 1: Executive Agent

[`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) मध्ये एक स्वतंत्र एजंट. लॅब 01 पूर्वी 10 मिनिटांचा डेमो म्हणून वापरा.

1. [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) उघडा आणि एजंट परिभाषा (सिस्टम प्रॉम्प्ट, मॉडेल, फ्रेमवर्क) चांगले समजून घ्या.
2. **Agent Inspector** स्थानिकरित्या चालू करण्यासाठी `F5` दाबा.
3. [README](../README.md#see-it-in-action) मधील नमुना प्रॉम्प्ट पेस्ट करा आणि कार्यकारी सारांशाचे प्रतिसाद दाखवा.
4. तैनातीसाठीचे घटक समजावून सांगण्यासाठी [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) आणि [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) दाखवा.
5. पूर्ण होण्याची वाट पाहता न घालता, तैनातीचा प्रवाह (Docker बिल्ड, ACR पुश, होस्टेड एजंट तयार करणे) दाखवा.

### डेमो 2: Resume to Job Fit Evaluator

[`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) मध्ये एक 4-एजंट वर्कफ्लो. लॅब 02 पूर्वी 10 मिनिटांचा डेमो म्हणून वापरा.

1. [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) उघडा आणि चार एजंट कसे साखळीप्रमाणे जोडलेले आहेत ते दाखवा.
2. मल्टी-एजंट वर्कफ्लोसाठी **Agent Inspector** सुरू करण्यासाठी `F5` दाबा.
3. Inspector चॅटमध्ये एक लहान नोकरीचे वर्णन आणि नमुना रिज्युमे पेस्ट करा.
4. चार एजंटांची प्रक्रिया समजावून सांगा: रिज्युमे पार्सर, कामाची गरज काढणारा, फिट स्कोअरर, आणि शिफारस लेखक.
5. प्रत्येक उप-अॅजंटचे आउटपुट पुढील एजंटच्या संदर्भासाठी कसे जाते ते दाखवा, हँडऑफ नमुना अधोरेखित करा.
6. सिंगल एजंटच्या तुलनेत [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) दाखवा.

---

## वितरण टिपणे

- **पूर्वीच अपेक्षा ठरवा.** होस्टेड एजंट अजून पूर्वावलोकनात आहेत - प्रदेश मर्यादा आणि कोटा आधीच स्पष्ट करा जेणेकरून उपस्थितांना मध्य लॅबमध्ये आश्चर्य वाटणार नाही.
- **पूर्वअटी काम आधी चालवा.** दोन्ही लॅब्समध्ये `Validate prerequisites` नावाचा VS Code टास्क आहे - कोड लिहिण्यापूर्वी उपस्थितांनी हा टास्क चालवावा.
- **Agent Inspector दिसत ठेवा.** बहुतेक "आहा" क्षण तेव्हा घडतात जेव्हा शिकणाऱ्यांना स्थानिक `/responses` राऊंड-ट्रिप उजळताना दिसते.
- **बॅकअप प्रकल्प ठेवा.** जर शिकणाऱ्याच्या Foundry प्रकल्पाला कोटा अडचण आली, तर कक्ष अडकवण्याऐवजी तैनाती टप्प्यासाठी पूर्वतयार प्रकल्प शेअर करा.
- **उपस्थितांना जोडून द्या.** लॅब 02 (मल्टी-एजंट) अधिक सहज होतो जेव्हा शिकणारे जोडीने चर्चा करतात.
- **दस्तऐवज मॉड्यूल्सला तपासणी ठप्प म्हणून वापरा.** प्रत्येक लॅबचा `docs/` फोल्डर 8 क्रमांक दिलेल्या मॉड्यूल्समध्ये आहे - या नैसर्गिक ब्रेक पॉइंट्ससारखे वापरा.
- **पाठवणाऱ्यांवर बेस Docker इमेज आधीच डाउनलोड करा** जेणेकरून रजिस्ट्री रेट लिमिट टाळता येतील.

---

## वितरण दरम्यान समस्या निवारण

| लक्षण                                      | प्रथम काय प्रयत्न करायचा                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector कनेक्ट होऊ शकत नाही               | `8088` पोर्ट मोकळा आहे का ते तपासा आणि `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` टास्क चालू आहे का पाहा.  |
| डिबगर संलग्न होण्यास अपयशी                     | `5679` पोर्ट मोकळा आहे का तपासा; जर `debugpy` आधीच जोडले असेल तर VS Code पुनरारंभ करा.                           |
| `azd up` प्रमाणपत्र त्रुटी येते               | `az login` आणि `azd auth login` चालवा, खात्री करा की योग्य टेनेट निवडलेला आहे.                              |
| तैनाती ACR पुशवर अडकले                 | Docker Desktop चालू आहे का आणि वापरकर्त्यास रजिस्ट्रीवर `AcrPush` प्रमाणपत्र आहे का ते तपासा.                              |
| मॉडेल 404 / deployment-not-found परत करते     | `agent.yaml` मधील मॉडेल तैनातीचे नाव Foundry प्रकल्पातील तैनातीशी जुळणे आवश्यक आहे.              |

| होस्टेड एजंट `Provisioning` मध्ये अडकलेले आहे         | प्रकल्प प्रदेश [होस्टेड एजंटला समर्थन देतो](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) आणि कोटा उपलब्ध असल्याची तपासणी करा. |
| Playground 401 परत करते                       | VS कोड क्रियाकलाप पट्टीतून Foundry विस्तार पुन्हा प्रमाणीकरण करा.                                     |

अधिक सखोल मार्गदर्शनासाठी, प्रत्येक प्रयोगशाळा स्वतःचा `08-troubleshooting.md` दस्तऐवज देते - शिकणाऱ्यांना तेथे लिंक करा:

- प्रयोगशाळा 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- प्रयोगशाळा 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## या सत्राचा सानुकूलन

आपण आपल्या प्रेक्षकांसाठी कार्यशाळा अनुकूलित करू शकता. सामान्य प्रकारांमध्ये:

- **बॅकएंड प्रेक्षक:** `agent.yaml`, Docker, आणि ACR वर अधिक वेळ द्या; playground डेमो कमी करा.
- **नागरिक-विकासक प्रेक्षक:** Foundry विस्तार UI मध्ये स्कॅफोल्डिंगसाठी थांबा; CLI पायऱ्या कमी करा.
- **सिंगल-ट्रॅक 60-मिनिट स्लॉट:** फक्त परिचय, डेमो, आणि प्रयोगशाळा 01 द्या.
- **फक्त कार्यशाळा (कोणतेही स्लाइड नाही) स्वरूप:** दोन्ही प्रयोगशाळा README उघडा आणि त्यांचा प्राथमिक स्क्रिप्ट म्हणून वापर करा.

जर तुम्ही प्रयोगशाळा वाढविल्या तर कृपया बदल PR द्वारे परत द्या जेणेकरून इतर प्रशिक्षकांचा फायदा होईल.

---

## अतिरिक्त संसाधने

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [होस्टेड एजंटचे आढावा](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [जलद प्रारंभ: आपला पहिला होस्टेड एजंट तैनात करा (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [होस्टेड एजंट तैनाती कशी करावी (कसे)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## संपर्क

जर तुम्हाला हे सत्र प्रदान करताना प्रश्न असतील, तर कृपया [कार्यशाळा संग्रहित ठिकाणी](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) एक समस्या उघडा आणि देखरेख करणाऱ्याला टॅग करा.

| भूमिका                | नाव           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| देखरेख करणारा / संपर्क| शिवम गोयल   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून अनुवादित केला आहे. जरी आम्ही अचूकतेसाठी प्रयत्न करतो, तरी कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या मूळ भाषेत अधिकृत स्रोत मानला पाहिजे. महत्त्वाची माहिती असल्यास, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थलावणीसाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->