# Kako održati ovaj sat

Hvala što održavate ovaj sat!

Prije održavanja radionice, molimo:

1. Pročitajte ovaj dokument i sve uključene resurse u cijelosti.
2. Pogledajte snimku održavanja sesije i cjelokupan pregled radionice.
3. Prođite oba praktična laboratorija u cijelosti na vlastitom računalu **barem jednom** prije događaja.
4. Provjerite svoj Microsoft Foundry projekt, rasporede modela i kvote.
5. Obratite se održavatelju ako nešto nije jasno.

---

## Sažetak datoteka

| Resurs                       | Veza                                                                             | Opis                                                                                      |
|-----------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Prezentacija radionice       | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                             | Slajdovi prezentacije za ovu radionicu s bilješkama predavača i ugrađenim demo video zapisima |
| Snimka održavanja sesije     | _Bit će dostavljeno od strane održavatelja_                                      | Uvod u radionicu i snimka prolaska kroz slajdove                                           |
| Cjelovita snimka radionice   | _Bit će dostavljeno od strane održavatelja_                                      | Cjelovita snimka oba laboratorija iz perspektive polaznika                                 |
| Dokumentacija radionice      | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Izvorni repozitorij, README dokumenti laboratorija, moduli korak-po-korak                 |
| Lab 01 - jedinstveni agent    | [Lab 01](../workshop/lab01-single-agent/README.md)                           | Praktični lab: izgradnja, testiranje i raspoređivanje *Explain Like I'm an Executive* hostiranog agenta |
| Lab 02 - višestruki agent    | [Lab 02](../workshop/lab02-multi-agent/README.md)                            | Praktični lab: izgradnja 4-agentskog *Resume to Job Fit Evaluator* tijeka rada             |
| Demo 1: Executive Agent       | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                            | Demo iz Lab 01: prevođenje tehničkog žargona u izvršni sažetak                             |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                   | Demo iz Lab 02: 4-agentski tijek rada koji ocjenjuje podudarnost životopisa i posla te generira preporuke |

> **Napomena za trenere:** Veze na prezentaciju i video zapise bit će dodane nakon što snimke budu objavljene. Do tada kontaktirajte održavatelja (vidi [Kontakti](#contacts)) za najnovije materijale.

---

## Početak

Ova radionica podučava developere kako izgraditi, testirati i rasporediti AI agente u **Microsoft Foundry Agent Service** kao **Hostirane agente** potpuno iz VS Code, koristeći ekstenziju **Microsoft Foundry Toolkit**.

Radionica je podijeljena u više dijelova uključujući slajdove, **2 živa demo prikaza** i **2 praktična laboratorija**.

### Vrijeme trajanja

#### Cjelovito održavanje (oko 2 sata)

| Vrijeme          | Opis                                                                      |
|-----------------|--------------------------------------------------------------------------|
| 0:00 - 10:00    | Uvod: hostirani agenti, Foundry Agent Service i toolkit                   |
| 10:00 - 20:00   | Demo: Executive Agent od početka do kraja                               |
| 20:00 - 60:00   | Lab 01 - jedan agent (izgradi, testiraj lokalno, rasporedi, playground)  |
| 60:00 - 110:00  | Lab 02 - višestruki agent tijek rada (Resume to Job Fit Evaluator)       |
| 110:00 - 120:00 | Zaključak, pitanja i odgovori, resursi za daljnje učenje                  |

#### Skraćeno održavanje (oko 75 minuta)

| Vrijeme        | Opis                                                              |
|---------------|------------------------------------------------------------------|
| 0:00 - 10:00  | Uvod i pregled                                                   |
| 10:00 - 20:00 | Demo: Executive Agent                                            |
| 20:00 - 70:00 | Samo Lab 01 (uputite polaznike na Lab 02 kao samostalni rad)     |
| 70:00 - 75:00 | Zaključak i pitanja                                              |

### Priprema

| Resurs                      | Veza                                                                                                | Opis                                         |
|----------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------|
| Dokumentacija radionice     | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)                   | Dokumentacija radionice i izvorni kod          |
| Upute za Lab 01             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                               | Praktični lab: jedan hostirani agent          |
| Upute za Lab 02             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                 | Praktični lab: višestruki agent tijek rada    |
| Kontrolni popis preduvjeta | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                    | Potrebni alati, računi i pristup Azureu        |
| Brzi početak za hostirane agente (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Službeni brzi početak za raspoređivanje hostiranog agenta s `azd` |
| Dostupnost regija za hostirane agente | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Podržane regije za hostirane agente (preview) |

### Preduvjeti za trenera

Prije nego što održite sat, pobrinite se da imate:

- **Pretplatu na Azure** s dopuštenjem za stvaranje resursa (Vlasnik ili Suradnik na grupi resursa).
- Pristup **Microsoft Foundry projektu** u [regiji koja podržava hostirane agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvotu za **gpt-4.1** (ili **gpt-4.1-mini**) u svom Foundry projektu.
- Sljedeće alate instalirane:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit ekstenzija](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opcionalno)
  - Python 3.12 ili noviji

Pokrenite [Brzi početak hostiranih agenata s `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) barem jednom prije održavanja kako biste imali provjereni Foundry projekt, raspored modela i Azure Container Registry za referencu ako netko od polaznika zaglavi.

---

## Prolaz kroz slajdove

Prezentacija prati isti tijek kao i laboratoriji. Predložene teme za svaku sekciju:

| Sekcija                   | Glavna poruka                                                                                                  |
|---------------------------|--------------------------------------------------------------------------------------------------------------|
| Naslov i agenda           | Postavite radionicu kao *VS Code do Foundry* bez potrebe za mijenjanjem portala.                              |
| Zašto hostirani agenti?   | Upravljano izvršavanje, raspoređivanje na osnovi ACR, OpenAI-kompatibilni `/responses` API, ograničeno na Foundry projekte. |
| Dijagram arhitekture      | Prođite kroz [README arhitekturu](../README.md#architecture): skelet, Inspector, ACR, Agent Service.            |
| Anatomija hostiranog agenta | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - što svaka datoteka radi.                          |
| Živi demo: Executive Agent | Prebacite se na VS Code i pokrenite [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demo od početka do kraja (vidi [Demo 1](#demo-1-executive-agent)). |
| Živi demo: Resume to Job Fit Evaluator | Prebacite se na VS Code i pokrenite [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4-agentni demo (vidi [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Kratki uvod za Lab 01     | Prebacite inicijativu na polaznike. Uputite na [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md).                  |
| Obrasci za višestruke agente | Sekvencijalni vs paralelni vs prijelaz - pregled prije početka Lab 02.                                     |
| Kratki uvod za Lab 02     | Prebacite inicijativu na polaznike. Uputite na [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md).                  |
| Zaključak i resursi       | Linkovi za daljnje učenje iz sekcije [Dodatni resursi](#additional-resources).                             |

---

## Demo prikazi

U dostavi su uključena dva živa demo prikaza. Dodijelite po 10 minuta za svaki.

| Demo                     | Lab      | Datoteke                 | Što prikazati                                                     |
|--------------------------|----------|-------------------------|-----------------------------------------------------------------|
| Executive Agent          | Lab 01   | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Jedan hostirani agent; prevodite tehnički žargon u izvršni sažetak |
| Resume to Job Fit Evaluator | Lab 02   | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4-agentna orkestracija; ocjena podudarnosti životopisa i generiranje preporuke |

### Demo 1: Executive Agent

Samostalni agent u [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Koristite ovo kao 10-minutni demo prije Lab 01.

1. Otvorite [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) i prođite definiciju agenta (sistemski prompt, model, framework).
2. Pritisnite `F5` za pokretanje **Agent Inspectora** lokalno.
3. Zalijepite primjer prompta iz [README](../README.md#see-it-in-action) i prikažite odgovor sažetka za izvršne.
4. Prikažite [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) i [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) kako biste objasnili artefakte raspoređivanja.
5. Demonstrirajte tijek raspoređivanja (Docker build, ACR push, kreiranje hostiranog agenta) bez čekanja na završetak.

### Demo 2: Resume to Job Fit Evaluator

Tijek rada sa 4 agenta u [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Koristite ovo kao 10-minutni demo prije Lab 02.

1. Otvorite [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) i pokažite kako su četvorica agenata povezani u sekvencijalnu orkestraciju.
2. Pritisnite `F5` za pokretanje **Agent Inspectora** za višestruki agent tijek rada.
3. Zalijepite kratak opis posla i primjer životopisa u chat Inspectora.
4. Prođite kroz četveroagentačnu pipeline: parser životopisa, izdavač zahtjeva posla, bodovanje podudarnosti i pisac preporuka.
5. Istaknite kako izlaz svakog pod-agenta postaje kontekst sljedećeg agenta, naglašavajući obrazac prijenosa.
6. Prikažite [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) kao usporedbu s ekvivalentom jednog agenta iz Demo 1.

---

## Savjeti za održavanje

- **Postavite očekivanja rano.** Hostirani agenti su u preview fazi - odmah istaknite ograničenja regije i kvotu da polaznici ne budu iznenađeni usred laboratorija.
- **Prvo pokrenite zadatak preduvjeta.** Oba laboratorija sadrže `Validate prerequisites` VS Code zadatak - neka polaznici to pokrenu prije pisanja bilo kakvog koda.
- **Držite Agent Inspectora vidljivim.** Većina "aha" trenutaka događa se kad polaznici vide lokalno osvjetljenje `/responses` runde.
- **Imate rezervni projekt.** Ako polaznikov Foundry projekt dosegne kvotu, podijelite unaprijed pripremljeni projekt za fazu raspoređivanja umjesto da blokirate prostoriju.
- **Uparite polaznike.** Lab 02 (višestruki agent) je znatno lakši kad polaznici mogu razgovarati o orkestraciji s partnerom.
- **Koristite dokumentacijske module kao kontrolne točke.** Svaka `docs/` mapa laboratorija podijeljena je u numerirane module - koristite ih kao prirodne točke za pauzu.
- **Preuzmite osnovnu Docker sliku** na zajedničkim lab računalima kako biste izbjegli limite brzine registra.

---

## Rješavanje problema tijekom održavanja

| Simptom                                      | Prva stvar koju treba probati                                                                             |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector se ne može povezati          | Provjerite da je port `8088` slobodan i da zadatak `Run Agent HTTP Server` radi.                   |
| Debugger se ne može priključiti               | Provjerite da je port `5679` slobodan; ponovno pokrenite VS Code ako je `debugpy` već zauzet. |
| `azd up` ne uspijeva zbog greške autorizacije | Pokrenite `az login` i `azd auth login`, provjerite je li odabran ispravan tenant.                |
| Raspoređivanje zapinje pri ACR push           | Provjerite da Docker Desktop radi i da korisnik ima `AcrPush` na registru.                        |
| Model vraća 404 / deployment-not-found        | Naziv raspoređivanja modela u `agent.yaml` mora odgovarati raspoređivanju u Foundry projektu.       |
| Hostirani agent zapne u `Provisioning`   | Provjerite podržava li regija projekt [hostirane agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) i je li dostupna kvota. |
| Playground vraća 401                          | Ponovno se prijavite u Foundry ekstenziju iz VS Code trake aktivnosti.                                   |

Za detaljnije upute, svaki laboratorij dolazi sa svojom `08-troubleshooting.md` dokumentacijom - uputite polaznike tamo:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Prilagođavanje ove sesije

Slobodno prilagodite radionicu svojoj publici. Uobičajene varijacije:

- **Publika backend developera:** provedite više vremena na `agent.yaml`, Docker i ACR; skratite playground demo.
- **Publika građanskih developera:** ostanite u Foundry ekstenzijskom korisničkom sučelju za scaffolding; smanjite količinu CLI koraka.
- **Jednokratan termin od 60 minuta:** održite samo uvod, demo i Lab 01.
- **Samo radionica (bez slajdova) format:** otvorite oba lab READMEs i koristite ih kao glavni skript.

Ako proširite laboratorije, molimo vas da promjene doprinesete natrag putem PR kako bi drugi treneri imali koristi.

---

## Dodatni resursi

- [Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/ai-foundry/)
- [Pregled hostiranih agenata](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Brzi početak: postavite svog prvog hostiranog agenta (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Postavljanje hostiranog agenta (kako)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
- [Microsoft Foundry Toolkit za VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakti

Ako imate pitanja o vođenju ove sesije, molimo otvorite issue na [workshop repozitoriju](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) i označite održavatelja.

| Uloga               | Ime            | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Održavatelj / kontakt| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->