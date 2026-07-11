# Cum să susțineți această sesiune

Mulțumim că susțineți această sesiune!

Înainte de a susține atelierul, vă rugăm să:

1. Citiți acest document și toate resursele incluse în întregime.
2. Vizionați înregistrarea susținerii sesiunii și prezentarea completă a atelierului.
3. Parcurgeți ambele laboratoare practice end-to-end pe propriul calculator **cel puțin o dată** înainte de eveniment.
4. Verificați proiectul Microsoft Foundry, implementările modelului și cotele dumneavoastră.
5. Contactați managerul dacă ceva nu este clar.

---

## Rezumat fișiere

| Resursă                      | Link                                                                             | Descriere                                                                                |
|-----------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Slide-urile atelierului      | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                    | Slide-uri pentru acest atelier cu note pentru prezentator și videoclipuri demo integrate  |
| Înregistrare sesiune         | _Va fi oferită de către manager_                                                | Înregistrare introductivă și prezentare a slide-urilor atelierului                        |
| Înregistrare completă atelier| _Va fi oferită de către manager_                                                | Înregistrare completă a ambelor laboratoare din perspectiva unui cursant                  |
| Documentație atelier         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repozitoriu sursă, fișiere README pentru laboratoare, module pas cu pas                   |
| Laborator 01 - agent unic    | [Lab 01](../workshop/lab01-single-agent/README.md)                              | Laborator practic: construire, testare și implementare a agentului *Explain Like I'm an Executive* |
| Laborator 02 - flux multi-agent | [Lab 02](../workshop/lab02-multi-agent/README.md)                             | Laborator practic: construire fluxul *Resume to Job Fit Evaluator* cu 4 agenți           |
| Demo 1: Agent Executiv       | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                            | Demo Laborator 01: traduceți jargon tehnic într-un rezumat executiv                      |
| Demo 2: Evaluator Adecvare CV la Job | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Demo Laborator 02: flux de lucru cu 4 agenți care evaluează adecvarea CV-ului la job și generează recomandări |

> **Notă pentru instructori:** Slide-urile și linkurile video vor fi adăugate odată ce înregistrările vor fi publicate. Până atunci, contactați managerul (vedeți [Contacte](#contacte)) pentru cele mai noi resurse.

---

## Începeți

Acest atelier îi învață pe dezvoltatori cum să construiască, să testeze și să implementeze agenți inteligenți artificiali în **Microsoft Foundry Agent Service** ca **Agenți găzduiți** complet din VS Code, folosind extensia **Microsoft Foundry Toolkit**.

Atelierul este împărțit în mai multe secțiuni, inclusiv slide-uri, **2 demo-uri live** și **2 laboratoare practice**.

### Timp de desfășurare

#### Susținere completă (aproximativ 2 ore)

| Timp           | Descriere                                                             |
|----------------|----------------------------------------------------------------------|
| 0:00 - 10:00   | Introducere: agenți găzduiți, Foundry Agent Service și toolkit        |
| 10:00 - 20:00  | Demo: Agent Executiv end-to-end                                       |
| 20:00 - 60:00  | Laborator 01 - agent unic (construire, testare locală, implementare, zona de joacă) |
| 60:00 - 110:00 | Laborator 02 - flux multi-agent (Evaluator Adecvare CV la Job)        |
| 110:00-120:00  | Concluzii, întrebări și resurse pentru învățare continuă              |

#### Susținere scurtă (aproximativ 75 minute)

| Timp          | Descriere                                                   |
|--------------|-------------------------------------------------------------|
| 0:00 - 10:00 | Introducere și privire de ansamblu                         |
| 10:00 - 20:00| Demo: Agent Executiv                                        |
| 20:00 - 70:00| Doar Laborator 01 (indicați participanților laboratoarele 02 pentru auto-studiu) |
| 70:00 - 75:00| Concluzii și sesiune Q&A                                   |

### Pregătire

| Resursă                          | Link                                                                                          | Descriere                                      |
|---------------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------------|
| Documentație atelier             | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Documentație atelier și sursă                    |
| Instrucțiuni Laborator 01        | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Laborator practic: agent unic                    |
| Instrucțiuni Laborator 02        | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Laborator practic: flux multi-agent             |
| Listă de verificare a prerechizitelor | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Instrumente, conturi și acces Azure necesare     |
| Quickstart agenți găzduiți (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Quickstart oficial pentru implementarea unui agent găzduit cu `azd` |
| Disponibilitatea regiunilor pentru agenți găzduiți | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Regiuni suportate pentru agenți găzduiți (previzualizare) |

### Prerechizite pentru instructori

Înainte de a susține, asigurați-vă că aveți:

- Un **abonament Azure** cu permisiune pentru crearea de resurse (proprietar sau colaborator pe un grup de resurse).
- Acces la un **proiect Microsoft Foundry** în [regiune care acceptă agenți găzduiți](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Cotă pentru **gpt-4.1** (sau **gpt-4.1-mini**) în proiectul dumneavoastră Foundry.
- Următoarele instrumente instalate:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Extensia Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (opțional)
  - Python 3.10 sau versiune ulterioară

Rulați cel puțin o dată [quickstart-ul agenților găzduiți cu `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) înainte de susținere pentru a avea un proiect Foundry, o implementare a modelului și un registru Azure Container Registry (ACR) validate la care să faceți referire în caz că un cursant se blochează.

---

## Parcurgerea slide-urilor

Deck-ul urmează aceeași structură ca laboratoarele. Puncte sugerate de discuție pentru fiecare secțiune:

| Secțiune                  | Mesaj cheie                                                                                                  |
|---------------------------|--------------------------------------------------------------------------------------------------------------|
| Titlu și agendă           | Prezentați atelierul ca *VS Code către Foundry* fără a fi nevoie de schimbare între portale.                 |
| De ce agenți găzduiți?    | Runtime gestionat, implementare bazată pe ACR, API `/responses` compatibilă OpenAI, limitată la proiecte Foundry. |
| Diagramă arhitectură      | Parcurgeți [architectura din README](../README.md#architecture): schelet, Inspector, ACR, Agent Service.       |
| Anatomia unui agent găzduit | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - ce face fiecare fișier.                            |
| Demo live: Agent Executiv  | Comutați la VS Code și rulați demo-ul [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) end-to-end (vedeți [Demo 1](#demo-1-agent-executiv)). |
| Demo live: Evaluator Adecvare CV la Job | Comutați la VS Code și rulați demo-ul cu 4 agenți [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (vedeți [Demo 2](#demo-2-evaluator-adecvare-cv-la-job)). |
| Prezentare Laborator 01    | Predați participanților. Indicați către [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Modele multi-agent        | Secvențial vs concurent vs transfer - previzualizare înainte să înceapă Laboratorul 02.                        |
| Prezentare Laborator 02    | Predați participanților. Indicați către [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Concluzii și resurse       | Legături pentru învățare continuă din secțiunea [Resurse suplimentare](#resurse-suplimentare).                  |

---

## Demo-uri

Două demo-uri live sunt incluse în prezentare. Alocați câte 10 minute fiecăruia.

| Demo                       | Laborator | Fișiere                                                       | Ce să arătați                                     |
|----------------------------|-----------|---------------------------------------------------------------|--------------------------------------------------|
| Agent Executiv             | Laborator 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)       | Agent unic găzduit; traduce jargon tehnic într-un rezumat executiv |
| Evaluator Adecvare CV la Job | Laborator 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)  | Orchestrare cu 4 agenți; evaluează adecvarea CV-ului la job și oferă recomandări |

### Demo 1: Agent Executiv

Un agent autonom în [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Folosiți-l ca demo de 10 minute înainte de Laborator 01.

1. Deschideți [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) și parcurgeți definiția agentului (prompt sistem, model, framework).
2. Apăsați `F5` pentru a lansa **Agent Inspector** local.
3. Lipiți promptul exemplu din [README](../README.md#see-it-in-action) și afișați răspunsul cu rezumat executiv.
4. Arătați [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) și [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) pentru a explica artefactele de implementare.
5. Demonstrați fluxul de implementare (construire Docker, push în ACR, creare agent găzduit) fără a aștepta finalizarea.

### Demo 2: Evaluator Adecvare CV la Job

Un flux de lucru cu 4 agenți în [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Folosiți-l ca demo de 10 minute înainte de Laborator 02.

1. Deschideți [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) și arătați cum cei patru agenți sunt conectați într-o orchestrare secvențială.
2. Apăsați `F5` pentru a lansa **Agent Inspector** pentru fluxul multi-agent.
3. Lipiți o descriere scurtă a jobului și un CV exemplu în chat-ul Inspectorului.
4. Parcurgeți fluxul celor patru agenți: parser CV, extractor cerințe job, evaluator potrivire, și scriitor recomandări.
5. Evidențiați cum ieșirea fiecărui sub-agent devine contextul agentului următor, arătând modelul transferului.
6. Arătați [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) pentru a compara cu echivalentul pentru un singur agent din Demo 1.

---

## Sfaturi pentru susținere

- **Stabiliți așteptările încă de la început.** Agenții găzduiți sunt în previzualizare - subliniați limitele regionale și cotele imediat ca să nu surprindă participanții în timpul laboratorului.
- **Rulați mai întâi task-ul de prerechizite.** Ambele laboratoare au un task VS Code `Validate prerequisites` - faceți-i pe participanți să îl ruleze înainte de a scrie cod.
- **Mențineți vizibil Agent Inspector.** Cele mai multe momente de „aha” apar când cursanții văd iluminarea răspunsurilor locale `/responses`.
- **Aveți un proiect de rezervă.** Dacă proiectul Foundry al unui cursant ajunge la o cotă maximă, împărtășiți un proiect pre-provizionat pentru pasul de implementare, în loc să blocați sala.
- **Faceți perechi între participanți.** Laboratorul 02 (multi-agent) este semnificativ mai ușor când cursanții pot discuta orchestrarea cu un partener.
- **Folosiți modulele din docs ca puncte de oprire.** Fiecare folder `docs/` al laboratorului este împărțit în 8 module numerotate - folosiți-le ca pauze naturale.
- **Pre-descărcați imaginea Docker de bază** pe calculatoarele de lab comun pentru a evita limitările ratei înregistrării.

---

## Depanare în timpul susținerii

| Simptom                                      | Prima acțiune de încercat                                                                              |
|----------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Agent Inspector nu se conectează            | Confirmați că portul `8088` este liber și task-ul `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` rulează. |
| Debugger nu se atașează                      | Verificați dacă portul `5679` este liber; reporniți VS Code dacă `debugpy` este deja legat de port.       |
| `azd up` eșuează cu eroare de autentificare  | Rulați `az login` și `azd auth login`, asigurați-vă că ați selectat chiriașul corect.                     |
| Implementarea se blochează la push în ACR     | Verificați că Docker Desktop rulează și că utilizatorul are permisiunea `AcrPush` pe registru.          |
| Modelul returnează 404 / deployment-not-found | Numele implementării modelului din `agent.yaml` trebuie să corespundă cu implementarea din proiectul Foundry. |

| Agentul găzduit blocat în `Provisioning` | Verificați dacă regiunea proiectului [suportă agenți găzduiți](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) și dacă Quota este disponibilă. |
| Playground returnează 401                   | Reautentificați extensia Foundry din bara de activități VS Code.                                     |

Pentru ghidare mai aprofundată, fiecare laborator are propriul său document `08-troubleshooting.md` - direcționați cursanții acolo:

- Laborator 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Laborator 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Personalizarea acestei sesiuni

Sunteți bineveniți să adaptați atelierul pentru audiența dumneavoastră. Varietățile comune:

- **Audiențe de backend:** petreceți mai mult timp pe `agent.yaml`, Docker și ACR; reduceți demonstrația playground.
- **Audiențe de cetățeni-dezvoltatori:** rămâneți în UI-ul extensiei Foundry pentru scaffold; reduceți pașii din CLI.
- **Interval unic de 60 de minute:** livrați doar introducerea, demonstrația și Laboratorul 01.
- **Format doar atelier (fără slide-uri):** deschideți ambele README-uri ale laboratoarelor și folosiți-le ca script principal.

Dacă extindeți laboratoarele, vă rugăm să contribuiți modificările prin PR pentru ca alți traineri să beneficieze.

---

## Resurse suplimentare

- [Documentația Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Prezentarea generală a agenților găzduiți](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Quickstart: implementați primul agent găzduit (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Implementarea unui agent găzduit (cum să)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit pentru VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contacte

Dacă aveți întrebări despre livrarea acestei sesiuni, vă rugăm să deschideți un issue pe [repositorul atelierului](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) și să dați tag persoanei de contact.

| Rol                  | Nume           | GitHub                                                  |
|----------------------|----------------|---------------------------------------------------------|
| Întreținător / contact| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->