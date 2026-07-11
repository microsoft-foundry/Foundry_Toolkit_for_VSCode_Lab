# Come tenere questa sessione

Grazie per aver tenuto questa sessione!

Prima di tenere il workshop, per favore:

1. Leggi questo documento e tutte le risorse incluse per intero.
2. Guarda la registrazione della sessione e la dimostrazione completa del workshop.
3. Esegui entrambi i laboratori pratici per intero sulla tua macchina **almeno una volta** prima dell'evento.
4. Verifica il tuo progetto Microsoft Foundry, le distribuzioni dei modelli e le quote.
5. Contatta il manutentore se qualcosa non è chiaro.

---

## Riepilogo file

| Risorsa                      | Link                                                                             | Descrizione                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Workshop slide deck           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Diapositive della presentazione per questo workshop con note del relatore e video demo incorporati        |
| Registrazione della sessione    | _Fornita dal manutentore_                                               | Registrazione dell'introduzione e della walkthrough delle diapositive del workshop                                              |
| Registrazione completa del workshop | _Fornita dal manutentore_                                               | Registrazione completa di entrambi i laboratori dal punto di vista di un partecipante                              |
| Documentazione del workshop        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repository sorgente, README dei laboratori, moduli passo-passo                                       |
| Lab 01 - agente singolo         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Laboratorio pratico: costruisci, testa e distribuisci l'agente *Explain Like I'm an Executive* ospitato     |
| Lab 02 - flusso di lavoro multi-agente | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Laboratorio pratico: costruisci il flusso di lavoro *Resume to Job Fit Evaluator* con 4 agenti                     |
| Demo 1: Agente Executive             | [Lab01 agente](../../../workshop/lab01-single-agent/agent)                                              | Demo Lab 01: traduci il gergo tecnico in un riepilogo esecutivo                          |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demo Lab 02: flusso di lavoro con 4 agenti che valuta la corrispondenza del CV al lavoro e genera raccomandazioni     |

> **Nota per i formatori:** Il deck delle diapositive e i link ai video saranno aggiunti una volta pubblicate le registrazioni. Fino ad allora, contatta il manutentore (vedi [Contatti](#contatti)) per gli ultimi materiali.

---

## Inizia qui

Questo workshop insegna agli sviluppatori come costruire, testare e distribuire agenti AI su **Microsoft Foundry Agent Service** come **Agenti Ospitati** interamente da VS Code, usando l'estensione **Microsoft Foundry Toolkit**.

Il workshop è diviso in più sezioni tra cui diapositive, **2 demo dal vivo** e **2 laboratori pratici**.

### Tempistiche

#### Erogazione completa (circa 2 ore)

| Ora            | Descrizione                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Introduzione: agenti ospitati, Foundry Agent Service e toolkit         |
| 10:00 - 20:00   | Demo: Agente Executive end-to-end                                     |
| 20:00 - 60:00   | Lab 01 - agente singolo (costruisci, testa localmente, distribuisci, playground)     |
| 60:00 - 110:00  | Lab 02 - flusso di lavoro multi-agente (Resume to Job Fit Evaluator)         |
| 110:00 - 120:00 | Conclusione, Q&A e risorse per l'apprendimento continuo                      |

#### Erogazione breve (circa 75 minuti)

| Ora          | Descrizione                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Introduzione e panoramica                                           |
| 10:00 - 20:00 | Demo: Agente Executive                                        |
| 20:00 - 70:00 | Solo Lab 01 (indirizza i partecipanti al Lab 02 in modalità autonoma)        |
| 70:00 - 75:00 | Conclusione e Q&A                                              |

### Preparazione

| Risorsa                       | Link                                                                                          | Descrizione                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Documentazione del workshop         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Documentazione del workshop e sorgente                 |
| Istruzioni Lab 01            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Laboratorio pratico: agente ospitato singolo                 |
| Istruzioni Lab 02            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Laboratorio pratico: flusso di lavoro multi-agente                |
| Lista prerequisiti        | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Strumenti, account e accesso Azure richiesti        |
| Avvio rapido agenti ospitati (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Avvio rapido ufficiale per distribuire un agente ospitato con `azd` |
| Disponibilità regionale agenti ospitati | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Regioni supportate per agenti ospitati (anteprima)     |

### Prerequisiti del formatore

Prima di tenere la sessione, assicurati di avere:

- Una **sottoscrizione Azure** con permessi per creare risorse (Proprietario o Collaboratore su un gruppo di risorse).
- Accesso a un **progetto Microsoft Foundry** in una [regione che supporta agenti ospitati](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Quota per **gpt-4.1** (o **gpt-4.1-mini**) nel tuo progetto Foundry.
- I seguenti strumenti installati:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Estensione Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opzionale)
  - Python 3.10 o versione successiva

Esegui almeno una volta l'[avvio rapido agenti ospitati con `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) prima della consegna in modo da avere un progetto Foundry funzionante, la distribuzione del modello e un Azure Container Registry di riferimento se un partecipante si blocca.

---

## Camminata attraverso le diapositive

Il deck segue lo stesso flusso dei laboratori. Punti chiave suggeriti per ogni sezione:

| Sezione                     | Messaggio chiave                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Titolo e agenda            | Inquadra il workshop come *Da VS Code a Foundry* senza bisogno di cambiare portale.                                |
| Perché agenti ospitati?          | Runtime gestito, distribuzione basata su ACR, API `/responses` compatibile OpenAI, limitata ai progetti Foundry.        |
| Diagramma architettura        | Cammina attraverso la [architettura nel README](../README.md#architecture): schema, Inspector, ACR, Agent Service.   |
| Anatomia di un agente ospitato   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - cosa fa ciascun file.                              |
| Demo dal vivo: Agente Executive  | Passa a VS Code ed esegui la demo end-to-end in [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) (vedi [Demo 1](#demo-1-agente-executive)). |
| Demo dal vivo: Resume to Job Fit Evaluator | Passa a VS Code ed esegui la demo con 4 agenti in [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (vedi [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Breve introduzione Lab 01                | Passa ai partecipanti. Indica [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Pattern multi-agente        | Sequenziale vs concorrente vs passaggio - anticipa prima che inizi Lab 02.                                           |
| Breve introduzione Lab 02                | Passa ai partecipanti. Indica [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Conclusione e risorse       | Link per l'apprendimento continuo dalla sezione [Risorse aggiuntive](#risorse-aggiuntive).                      |

---

## Demo

Sono incluse due demo dal vivo nella consegna. Dedica 10 minuti a ciascuna.

| Demo | Lab | File | Cosa mostrare |
|------|-----|-------|--------------|
| Agente Executive | Lab 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Agente ospitato singolo; traduce gergo tecnico in un riepilogo esecutivo |
| Resume to Job Fit Evaluator | Lab 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orchestrazione con 4 agenti; valuta la corrispondenza CV-lavoro e genera raccomandazioni |

### Demo 1: Agente Executive

Un agente standalone in [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Usalo come demo di 10 minuti prima di Lab 01.

1. Apri [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) ed esamina la definizione dell'agente (prompt di sistema, modello, framework).
2. Premi `F5` per avviare localmente l'**Agent Inspector**.
3. Incolla il prompt di esempio dal [README](../README.md#see-it-in-action) e mostra la risposta del riepilogo esecutivo.
4. Mostra [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) e [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) per spiegare gli artefatti di distribuzione.
5. Dimostra il flusso di distribuzione (build Docker, push su ACR, creazione agente ospitato) senza attendere il completamento.

### Demo 2: Resume to Job Fit Evaluator

Un flusso di lavoro con 4 agenti in [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Usalo come demo di 10 minuti prima di Lab 02.

1. Apri [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) e mostra come i quattro agenti sono collegati in un'orchestrazione sequenziale.
2. Premi `F5` per avviare l'**Agent Inspector** per il flusso multi-agente.
3. Incolla una breve descrizione del lavoro e un CV di esempio nella chat dell'Inspector.
4. Illustra la pipeline con i quattro agenti: analizzatore CV, estrattore requisiti di lavoro, valutatore di corrispondenza e scrittore di raccomandazioni.
5. Evidenzia come l'output di ciascun sotto-agente diventa il contesto per l'agente successivo, sottolineando il pattern di passaggio.
6. Mostra [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) per confrontarlo con l'agente singolo della Demo 1.

---

## Consigli per la consegna

- **Imposta le aspettative presto.** Gli agenti ospitati sono in anteprima – evidenzia subito i limiti regionali e le quote in modo che i partecipanti non si trovino sorpresi a metà laboratorio.
- **Esegui prima il task dei prerequisiti.** Entrambi i laboratori includono un task `Validate prerequisites` in VS Code – fai eseguire questo agli studenti prima di scrivere codice.
- **Mantieni l'Agent Inspector visibile.** La maggior parte dei momenti “aha” avviene quando i partecipanti vedono accendersi il round-trip locale di `/responses`.
- **Prevedi un progetto di riserva.** Se il progetto Foundry di un partecipante raggiunge una quota, condividi un progetto preconfigurato per la fase di distribuzione anziché bloccare la stanza.
- **Fai lavorare i partecipanti in coppia.** Il Lab 02 (multi-agente) è significativamente più facile quando si può discutere dell'orchestrazione con un partner.
- **Usa i moduli della documentazione come checkpoint.** La cartella `docs/` di ogni laboratorio è divisa in 8 moduli numerati – usali come punti di pausa naturali.
- **Pre-scarica l'immagine Docker base** sulle macchine del laboratorio condivise per evitare limiti di velocità del registro.

---

## Risoluzione dei problemi durante la consegna

| Sintomo                                      | Prima cosa da provare                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector non si connette               | Verifica che la porta `8088` sia libera e che il task `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` sia in esecuzione.   |
| Il debugger non si aggancia                     | Controlla che la porta `5679` sia libera; riavvia VS Code se `debugpy` è già in ascolto.                           |
| `azd up` fallisce con errore di autenticazione               | Esegui `az login` e `azd auth login`, assicurandoti che sia selezionato il tenant corretto.                              |
| La distribuzione si blocca durante il push su ACR                 | Controlla che Docker Desktop sia in esecuzione e che l'utente abbia permessi `AcrPush` sul registro.                              |
| Il modello restituisce 404 / deployment-not-found     | Il nome della distribuzione del modello in `agent.yaml` deve corrispondere a quello nella distribuzione del progetto Foundry.              |

| Agente hosted bloccato in `Provisioning`    | Verificare che la regione del progetto [supporti agenti hosted](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) e che sia disponibile la quota.       |
| Playground restituisce 401                   | Rieseguire l'autenticazione dell'estensione Foundry dalla barra delle attività di VS Code.                              |

Per una guida più approfondita, ogni laboratorio include il proprio documento `08-troubleshooting.md` - indirizzare gli utenti lì:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Personalizzare questa sessione

Sei libero di adattare il workshop per il tuo pubblico. Variazioni comuni:

- **Pubblico backend:** passare più tempo su `agent.yaml`, Docker e ACR; ridurre la demo del playground.
- **Pubblico citizen-developer:** rimanere nell'interfaccia dell'estensione Foundry per il scaffolding; ridurre i passaggi CLI.
- **Slot singolo di 60 minuti:** fornire solo introduzione, demo e Lab 01.
- **Formato solo workshop (senza slide):** aprire i README di entrambi i laboratori e usarli come script primario.

Se estendi i laboratori, ti preghiamo di contribuire con le modifiche tramite PR affinché altri formatori ne traggano vantaggio.

---

## Risorse aggiuntive

- [Documentazione Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Panoramica degli agenti hosted](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Guida rapida: distribuisci il tuo primo agente hosted (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Distribuire un agente hosted (how-to)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit per VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contatti

Se hai domande sulla conduzione di questa sessione, apri una issue sul [repository del workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) e tagga il manutentore.

| Ruolo              | Nome          | GitHub                                                    |
|--------------------|---------------|-----------------------------------------------------------|
| Manutentore / contatto | Shivam Goyal | [@ShivamGoyal03](https://github.com/ShivamGoyal03)          |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->