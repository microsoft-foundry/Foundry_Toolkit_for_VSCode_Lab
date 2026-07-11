# Kako održati ovu sesiju

Hvala što održavate ovu sesiju!

Prije održavanja radionice, molimo:

1. Pročitajte ovaj dokument i sve uključene resurse u cijelosti.
2. Pogledajte snimku održavanja sesije i pregled radionice od početka do kraja.
3. Prođite oba praktična laboratorija od početka do kraja na vlastitom stroju **barem jednom** prije događaja.
4. Provjerite svoj Microsoft Foundry projekt, implementacije modela i kvote.
5. Obratite se održavatelju ako nešto nije jasno.

---

## Sažetak datoteka

| Resurs                       | Poveznica                                                                       | Opis                                                                                     |
|-----------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Prezentacija radionice       | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                   | Slajdovi prezentacije za ovu radionicu s bilješkama predavača i ugrađenim demo videozapisima |
| Snimka održavanja sesije     | _Dostavit će održavatelj_                                                       | Snimka uvoda u radionicu i prolazak kroz slajdove                                        |
| Snimka radionice od početka do kraja | _Dostavit će održavatelj_                                                      | Snimka oba laboratorija iz perspektive polaznika                                         |
| Dokumentacija radionice      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Izvorni repozitorij, README datoteke za laboratorije, korak-po-korak moduli                |
| Lab 01 - pojedinačni agent   | [Lab 01](../workshop/lab01-single-agent/README.md)                             | Praktični laboratorij: izgradnja, testiranje i implementacija *Explain Like I'm an Executive* hostiranog agenta |
| Lab 02 - višestruki agent workflow | [Lab 02](../workshop/lab02-multi-agent/README.md)                              | Praktični laboratorij: izgradnja 4-agentskog *Resume to Job Fit Evaluator* workflowa      |
| Demo 1: Executive Agent      | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                           | Demo Lab 01: prevod tehničkog žargona u izvršni sažetak                                  |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)  | Demo Lab 02: 4-agent workflow koji ocjenjuje podudarnost životopisa s poslom i generira preporuke |

> **Napomena za trenere:** Poveznice na prezentaciju i videozapise bit će dodane nakon objave snimki. Do tada, kontaktirajte održavatelja (vidi [Kontakti](#kontakti)) za najnovije materijale.

---

## Početak rada

Ova radionica podučava programere kako izgraditi, testirati i implementirati AI agente u **Microsoft Foundry Agent Service** kao **hostirane agente** potpuno iz VS Codea, koristeći ekstenziju **Microsoft Foundry Toolkit**.

Radionica je podijeljena u nekoliko dijelova uključujući slajdove, **2 živa demo prikaza** i **2 praktična laboratorija**.

### Trajanje

#### Cjelovito održavanje (oko 2 sata)

| Vrijeme         | Opis                                                                 |
|-----------------|-----------------------------------------------------------------------|
| 0:00 - 10:00    | Uvod: hostirani agenti, Foundry Agent Service i toolkit               |
| 10:00 - 20:00   | Demo: Executive Agent od početka do kraja                            |
| 20:00 - 60:00   | Lab 01 - pojedinačni agent (izgradnja, lokalno testiranje, implementacija, playground) |
| 60:00 - 110:00  | Lab 02 - višestruki agentski workflow (Resume to Job Fit Evaluator)  |
| 110:00 - 120:00 | Završetak, pitanja i odgovori, resursi za daljnje učenje              |

#### Skraćeno održavanje (oko 75 minuta)

| Vrijeme        | Opis                                                       |
|----------------|------------------------------------------------------------|
| 0:00 - 10:00   | Uvod i pregled                                            |
| 10:00 - 20:00  | Demo: Executive Agent                                     |
| 20:00 - 70:00  | Samo Lab 01 (usmjeriti sudionike na Lab 02 kao samostalno)|
| 70:00 - 75:00  | Završetak i pitanja i odgovori                            |

### Priprema

| Resurs                      | Poveznica                                                                                        | Opis                                                |
|-----------------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------------|
| Dokumentacija radionice     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                | Dokumentacija i izvorni kod radionice               |
| Upute za Lab 01             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                 | Praktični laboratorij: pojedinačni hostirani agent |
| Upute za Lab 02             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                   | Praktični laboratorij: višestruki agentski workflow|
| Popis preduvjeta           | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                   | Potrebni alati, računi i pristup Azureu              |
| Brzi početak hostiranih agenata (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Službeni brzi početak za implementaciju hostiranog agenta s `azd` |
| Dostupnost regija za hostirane agente | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Podržane regije za hostirane agente (pregled)      |

### Preduvjeti za trenera

Prije održavanja, pobrinite se da imate:

- **Pretplatu na Azure** s dozvolom za kreiranje resursa (Vlasnik ili Suradnik na skupini resursa).
- Pristup **Microsoft Foundry projektu** u [regiji koja podržava hostirane agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvotu za **gpt-4.1** (ili **gpt-4.1-mini**) u vašem Foundry projektu.
- Instalirane sljedeće alate:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit ekstenzija](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (opcionalno)
  - Python 3.10 ili noviji

Pokrenite [Hosted agents quickstart with `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) barem jednom prije održavanja kako biste imali poznat i ispravan Foundry projekt, implementaciju modela i Azure Container Registry za referencu ako se polaznik zatekne u problemu.

---

## Prolazak kroz slajdove

Prezentacija prati isti tijek kao i laboratoriji. Predložene teme za svaku sekciju:

| Sekcija                    | Ključna poruka                                                                                             |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| Naslov i agenda            | Predstavite radionicu kao *VS Code do Foundry* bez potrebe za prebacivanjem portala.                       |
| Zašto hostirani agenti?    | Upravljačko vrijeme izvođenja, implementacija bazirana na ACR-u, OpenAI-kompatibilni `/responses` API, ograničeno na Foundry projekte. |
| Dijagram arhitekture       | Prođite kroz [README arhitekturu](../README.md#architecture): kostur, Inspector, ACR, Agent Service.         |
| Anatomija hostiranog agenta | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - što svaka datoteka radi.                         |
| Živi demo: Executive Agent  | Prebacite se na VS Code i pokrenite demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) od početka do kraja (vidi [Demo 1](#demo-1-executive-agent)). |
| Živi demo: Resume to Job Fit Evaluator | Prebacite se na VS Code i pokrenite 4-agent demo [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (vidi [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Kratko o Lab 01            | Predajte sudionicima. Uputite ih na [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Obrasci višestrukih agenata | Sekvencijalno vs istovremeno vs predaja - ukratko prije početka Lab 02.                                     |
| Kratko o Lab 02            | Predajte sudionicima. Uputite ih na [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Zaključak i resursi        | Linkovi za daljnje učenje iz odjeljka [Dodatni resursi](#dodatni-resursi).                             |

---

## Demo prikazi

U dostavi su uključena dva živa demo prikaza. Odvojite po 10 minuta za svaki.

| Demo                    | Laboratorij | Datoteke                                                 | Što prikazati                                                   |
|-------------------------|-------------|----------------------------------------------------------|----------------------------------------------------------------|
| Executive Agent         | Lab 01      | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Pojedinačni hostirani agent; prevod tehničkog žargona u izvršni sažetak |
| Resume to Job Fit Evaluator | Lab 02      | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agent orkestracija; ocjena podudarnosti životopisa s poslom i generiranje preporuke |

### Demo 1: Executive Agent

Samostalni agent u [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Koristite ga kao desetominutni demo prije Lab 01.

1. Otvorite [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) i prođite kroz definiciju agenta (sistemski prompt, model, okvir).
2. Pritisnite `F5` za lokalno pokretanje **Agent Inspectora**.
3. Zalijepite primjer prompta iz [README](../README.md#see-it-in-action) i pokažite odgovor sažetka za izvršnog direktora.
4. Pokažite [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) i [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) da objasnite artefakte implementacije.
5. Demonstrirajte tok implementacije (Docker build, ACR push, kreiranje hostiranog agenta) bez čekanja na dovršetak.

### Demo 2: Resume to Job Fit Evaluator

4-agent workflow u [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Koristite ga kao desetominutni demo prije Lab 02.

1. Otvorite [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) i pokažite kako su četiri agenta povezana u sekvencijalnu orkestraciju.
2. Pritisnite `F5` za pokretanje **Agent Inspectora** za višestruki agentski workflow.
3. Zalijepite kratki opis posla i primjer životopisa u razgovor Inspectora.
4. Prođite kroz pipeline sa četiri agenta: parser životopisa, ekstraktor zahtjeva posla, ocjenjivač podudarnosti i pisac preporuka.
5. Istaknite kako je izlaz svakog pod-agenta kontekst za sljedećeg agenta, naglašavajući obrazac predaje.
6. Pokažite [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) za usporedbu s ekvivalentom pojedinačnog agenta iz Demo 1.

---

## Savjeti za održavanje

- **Postavite očekivanja odmah.** Hostirani agenti su u pregledu - unaprijed istaknite ograničenja regija i kvote da sudionici ne budu iznenađeni usred laboratorija.
- **Prvo pokrenite zadatak preduvjeta.** Oba laboratorija imaju `Validate prerequisites` VS Code zadatak - neka sudionici pokrenu taj zadatak prije pisanja bilo kakvog koda.
- **Držite Agent Inspector vidljivim.** Većina "aha" trenutaka događa se kada polaznici vide osvjetljenje lokalnih `/responses` povratnih okvira.
- **Imajte rezervni projekt.** Ako polaznikov Foundry projekt dosegne kvotu, podijelite unaprijed pripremljeni projekt za korak implementacije umjesto da blokirate prostoriju.
- **Povežite sudionike u parove.** Lab 02 (višestruki agent) je znatno lakši kada polaznici mogu razgovarati o orkestraciji s partnerom.
- **Koristite modules iz dokumentacije kao kontrolne točke.** Svaka `docs/` mapa laboratorija podijeljena je u 8 numeriranih modula - koristite ih kao prirodne točke za pauzu.
- **Preuzmite baznu Docker sliku unaprijed** na zajedničkim strojevima za laboratorij kako biste izbjegli ograničenja brzine registra.

---

## Rješavanje problema tijekom održavanja

| Simptom                               | Prva stvar koja se treba pokušati                                                              |
|-------------------------------------|------------------------------------------------------------------------------------------------|
| Agent Inspector se ne može povezati | Provjerite da je port `8088` slobodan i da je zadatak `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` u tijeku. |
| Debugger ne uspije spojiti           | Provjerite da je port `5679` slobodan; ponovo pokrenite VS Code ako je `debugpy` već vezan.       |
| `azd up` ne uspije zbog greške s autentifikacijom | Pokrenite `az login` i `azd auth login`, provjerite je li odabrani ispravan zakupac.               |
| Implementacija zastane na ACR push  | Provjerite radi li Docker Desktop i ima li korisnik dozvolu `AcrPush` na registru.                |
| Model vraća 404 / deployment-not-found | Naziv implementacije modela u `agent.yaml` mora odgovarati implementaciji u Foundry projektu.     |

| Hostirani agent zapeo u `Provisioning`         | Provjerite podržava li regija projekta [hostirane agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) i je li kvota dostupna. |
| Playground vraća 401                       | Ponovno se autentificirajte u Foundry ekstenziji iz VS Code trake aktivnosti.                                     |

Za detaljnije upute, svaki laboratorij dolazi sa svojim `08-troubleshooting.md` dokumentom - uputite polaznike tamo:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Prilagodba ove sesije

Slobodno prilagodite radionicu svojoj publici. Uobičajene varijacije:

- **Backend publike:** provedite više vremena na `agent.yaml`, Docker i ACR; skratite demonstraciju playgrounda.
- **Publike građana-razvijatelja:** ostanite u Foundry ekstenziji za UI za strukturiranje; smanjite CLI korake.
- **Jedan 60-minutni termin:** izvedite samo uvod, demo i Lab 01.
- **Format samo radionice (bez slajdova):** otvorite oba lab READMea i koristite ih kao glavni scenarij.

Ako proširite laboratorije, molimo doprinesite promjenama putem PR-a kako bi drugi treneri imali koristi.

---

## Dodatni resursi

- [Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/ai-foundry/)
- [Pregled hostiranih agenata](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Brzi početak: postavite svog prvog hostiranog agenta (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Kako postaviti hostiranog agenta](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit za VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakti

Ako imate pitanja o izvođenju ove sesije, molimo otvorite issue na [workshop repozitoriju](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) i označite održavatelja.

| Uloga               | Ime            | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Održavatelj / kontakt| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->