# Kako izvesti to sejo

Hvala, ker izvajaš to sejo!

Pred izvedbo delavnice, prosimo:

1. Preberi ta dokument in vse vključene vire v celoti.
2. Oglej si posnetek izvedbe seje in celoten pregled delavnice.
3. Na svojem računalniku **vsaj enkrat** preizkusi obe praktični delavnici od začetka do konca pred dogodkom.
4. Preveri svoj Microsoft Foundry projekt, namestitve modelov in kvote.
5. Obrni se na skrbnika, če je kaj nejasno.

---

## Povzetek datotek

| Vir                           | Povezava                                                                        | Opis                                                                                      |
|-------------------------------|---------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Predstavitvena datoteka delavnice | [Glavni diapozitivi](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                               | Diapozitivi delavnice z notami za predavatelja in vgrajenimi demo videi                    |
| Posnetek izvedbe seje          | _Bomo zagotovili skrbnik_                                                        | Posnetek uvoda v delavnico in predstavitev diapozitivov                                  |
| Posnetek celotne delavnice     | _Bomo zagotovili skrbnik_                                                        | Celovit posnetek obeh delavnic s perspektive udeleženca                                 |
| Dokumentacija delavnice         | [Repozitorij](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Izvorni repozitorij, navodila za delavnice, korak-po-korak moduli                         |
| Delavnica 01 - en sam agent     | [Delavnica 01](../workshop/lab01-single-agent/README.md)                         | Praktična delavnica: zgradi, preizkusi in namesti gostujočega agenta *Explain Like I'm an Executive* |
| Delavnica 02 - več agentov      | [Delavnica 02](../workshop/lab02-multi-agent/README.md)                          | Praktična delavnica: zgradi 4-agentni potek *Resume to Job Fit Evaluator*                 |
| Demo 1: Izvršni agent           | [Agent Delavnica01](../../../workshop/lab01-single-agent/agent)                       | Demo Delavnica 01: prevedi tehnični jezik v izvršni povzetek                             |
| Demo 2: Evalvator skladnosti CV s delom | [OsebniKarierniPomočnik](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Demo Delavnica 02: 4-agentni potek, ki oceni skladnost CV z delom in ustvari priporočila  |

> **Opomba za trenerje:** Diapozitivi in video povezave bodo dodane, ko bodo posnetki objavljeni. Do takrat kontaktirajte skrbnika (glej [Kontakte](#kontakti)) za najnovejše materiale.

---

## Začni

Ta delavnica uči razvijalce, kako zgraditi, preizkusiti in namestiti AI agente v **Microsoft Foundry Agent Service** kot **gostujoče agente**, vse skupaj iz okolja VS Code, z uporabo razširitve **Microsoft Foundry Toolkit**.

Delavnica je razdeljena na več delov, vključno z diapozitivi, **2 živima demonstracijama** in **2 praktičnima delavnicama**.

### Časovni okvir

#### Celotna izvedba (približno 2 uri)

| Čas            | Opis                                                                 |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Uvod: gostujoči agenti, Foundry Agent Service in orodna oprema       |
| 10:00 - 20:00   | Demo: Izvršni agent od začetka do konca                              |
| 20:00 - 60:00   | Delavnica 01 - en sam agent (gradnja, lokalno testiranje, namestitev, igralno okolje) |
| 60:00 - 110:00  | Delavnica 02 - večagentni potek (Evalvator skladnosti CV z delom)    |
| 110:00 - 120:00 | Zaključek, Q&A in viri za nadaljnje učenje                           |

#### Kratka izvedba (približno 75 minut)

| Čas          | Opis                                                            |
|---------------|----------------------------------------------------------------|
| 0:00 - 10:00  | Uvod in pregled                                                |
| 10:00 - 20:00 | Demo: Izvršni agent                                           |
| 20:00 - 70:00 | Samo Delavnica 01 (udeležencem pokaži Delavnico 02 kot samostojno) |
| 70:00 - 75:00 | Zaključek in Q&A                                              |

### Priprava

| Vir                        | Povezava                                                                                         | Opis                                                |
|-----------------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------|
| Dokumentacija delavnice      | [Repozitorij](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)               | Dokumentacija delavnice in izvorni kod               |
| Navodila za Delavnico 01    | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                   | Praktična delavnica: en sam gostujoči agent          |
| Navodila za Delavnico 02    | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                     | Praktična delavnica: večagentni potek                |
| Kontrolni seznam predpogojev | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                   | Orodja, računi in dostop do Azure, potrebni za delavnico|
| Hiter začetek z gostujočim agentom (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Uradni hiter začetek za namestitev gostujočega agenta z `azd` |
| Razpoložljivost regij za gostujoče agente | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Podprte regije za gostujoče agente (predogled)       |

### Zahteve za trenerja

Preden začneš, poskrbi, da imaš:

- **Azure naročnino** s pravico ustvarjanja virov (Lastnik ali Sodelavec na skupini virov).
- Dostop do **Microsoft Foundry projekta** v [regiji, ki podpira gostujoče agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kvoto za **gpt-4.1** (ali **gpt-4.1-mini**) v tvojem Foundry projektu.
- Namestljena naslednja orodja:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit razširitev](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (izbirno)
  - Python 3.10 ali novejši

Zaženi [hiter začetek z gostujočimi agenti `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) vsaj enkrat pred izvedbo, da imaš znan in ustrezen Foundry projekt, namestitev modela in Azure Container Registry, na katerega se lahko sklicuješ, če udeleženec obstane.

---

## Pregled diapozitivov

Predstavitev sledi istemu zaporedju kot delavnice. Priporočene točke za pogovor za vsak razdelek:

| Razdelek                   | Ključno sporočilo                                                                                     |
|----------------------------|-----------------------------------------------------------------------------------------------------|
| Naslov in agenda           | Predstavi delavnico kot *VS Code do Foundry*, brez preklapljanja na portale.                         |
| Zakaj gostujoči agenti?    | Upravljano izvajanje, namestitev na osnovi ACR, OpenAI združljiv `/responses` API, usmerjeno na Foundry projekte. |
| Diagram arhitekture         | Preglej [README arhitekturo](../README.md#architecture): ogrodje, pregledovalnik, ACR, Agent Service.|
| Zgradba gostujočega agenta | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - funkcije vsake datoteke.                  |
| Živa demonstracija: Izvršni agent | Preklopi v VS Code in zaženi demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) od začetka do konca (glej [Demo 1](#demo-1-izvršni-agent)). |
| Živa demonstracija: Evalvator skladnosti CV z delom | Preklopi v VS Code in zaženi 4-agentni demo [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (glej [Demo 2](#demo-2-evalvator-skladnosti-cv-z-delom)). |
| Kratek povzetek Delavnice 01 | Predaj naprej udeležencem. Pokaži [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Vzorce več agentov         | Zaporedno vs sočasno vs predaja - predogled pred začetkom Delavnice 02.                              |
| Kratek povzetek Delavnice 02 | Predaj naprej udeležencem. Pokaži [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Zaključek in viri          | Povezave za nadaljnje učenje iz razdelka [Dodatni viri](#dodatni-viri).                      |

---

## Demonstracije

V izvedbi sta vključeni dve živi demonstraciji. Za vsako načrtuj 10 minut.

| Demo | Delavnica | Datoteke | Kaj prikazati |
|------|-----------|----------|--------------|
| Izvršni agent | Delavnica 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | En sam gostujoči agent; prevod tehničnega jezika v izvršni povzetek |
| Evalvator skladnosti CV z delom | Delavnica 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orkestracija štirih agentov; ocena skladnosti CV z delom in predlog priporočila |

### Demo 1: Izvršni agent

Samostojen agent v [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Uporabi kot 10-minutni demo pred Delavnico 01.

1. Odpri [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) in preglej definicijo agenta (sistema prompt, model, ogrodje).
2. Pritisni `F5` za lokalni zagon **Agent Inspector**.
3. Prilepi vzorčni poziv iz [README](../README.md#see-it-in-action) in prikaži odgovor izvršnega povzetka.
4. Prikaži [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) in [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) ter pojasni artefakte namestitve.
5. Prikaži tok namestitve (Docker build, ACR push, ustvarjanje gostujočega agenta) brez čakanja na dokončanje.

### Demo 2: Evalvator skladnosti CV z delom

Štir- agentski potek v [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Uporabi kot 10-minutni demo pred Delavnico 02.

1. Odpri [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) in prikaži, kako so štirje agenti povezani v zaporedno orkestracijo.
2. Pritisni `F5` za zagon **Agent Inspector** za večagentni potek.
3. V Inspector klepet prilepi kratek opis delovnega mesta in vzorčni življenjepis.
4. Preberi potek štirih agentov: parser življenjepisa, izvleček zahtev delovnega mesta, ocenjevalec skladnosti, pisec priporočil.
5. Izpostavi, kako izhod vsakega podagenta postane kontekst naslednjega agenta, poudarjajoč vzorec predaje.
6. Prikaži [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) za primerjavo s samostojnim agentom iz Demo 1.

---

## Nasveti za izvedbo

- **Določi pričakovanja zgodaj.** Gostujoči agenti so v predogledu – jasno povej omejitve regij in kvote, da udeleženci med delavnico niso presenečeni.
- **Najprej zaženi preverjanje predpogojev.** Obe delavnici imata `Validate prerequisites` VS Code opravilo – udeleženci naj ga zaženejo pred pisanjem kode.
- **Ohrani vidnost Agent Inspector-ja.** Večina "aha" trenutkov se zgodi, ko udeleženci vidijo osvetlitev lokalnega `/responses` round-trip.
- **Ima rezervni projekt.** Če udeleženčev Foundry projekt naleti na omejitev kvote, deli vnaprej pripravljen projekt za namestitveni korak, namesto da bi blokiral sobo.
- **Poveži udeležence v pare.** Delavnica 02 (več agentov) je znatno lažja, če lahko udeleženci skupaj razpravljajo o orkestraciji.
- **Uporabi dokumentacijske module kot kontrolne točke.** Vsaka delavnica vsebuje `docs/` mapo razdeljeno na 8 številčenih modulov – uporabi jih kot naravne točke za premor.
- **Predhodno potegni osnovno Docker sliko** na skupnih delavnicah, da se izogneš omejitvam hitrosti v registru.

---

## Reševanje težav med izvedbo

| Simptomi                                     | Prvi korak za poskus rešitve                                                                           |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Agent Inspector se ne more povezati         | Preveri, da je vrata `8088` prosta in da sta opravili `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server`.  |
| Odpravljanje napak se ne more pritrditi      | Preveri, da je vrata `5679` prosta; znova zaženi VS Code, če je `debugpy` že zaseden.                  |
| `azd up` ne uspe zaradi napake pri avtentikaciji | Zaženi `az login` in `azd auth login`, preveri, da je izbran pravi zakupnik.                          |
| Namestitev se zatakne pri ACR push           | Preveri, da je Docker Desktop zagnan in da ima uporabnik pravico `AcrPush` v registru.                |
| Model vrne 404 / deployment-not-found         | Ime namestitve modela v `agent.yaml` mora ustrezati tisti v Foundry projektu.                          |

| Gostujoči agent zataknjen v `Provisioning`         | Preverite, ali regija projekta [podpira gostujoče agente](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) in ali je kvota na voljo. |
| Igralna površina vrne 401                       | Ponovno se overite v razširitvi Foundry iz vrstice dejavnosti VS Code.                                     |

Za poglobljena navodila ima vsak laboratorij svoj dokument `08-troubleshooting.md` - udeležence usmerite tja:

- Laboratorij 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Laboratorij 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Prilagajanje tega srečanja

Dobrodošli, da delavnico prilagodite svoji publiki. Pogoste različice:

- **Za backend publiko:** preživite več časa na `agent.yaml`, Dockerju in ACR; skrajšajte demo igralne površine.
- **Za občane-razvijalce:** ostanite v uporabniškem vmesniku razširitve Foundry za ustvarjanje ogrodja; zmanjšajte korake CLI.
- **Enostopenjski 60-minutni blok:** izvedite le uvod, demo in laboratorij 01.
- **Samo delavnica (brez diapozitivov):** odprite oba lab README-ja in ju uporabite kot glavni skript.

Če razširite laboratorije, prosim prispevajte spremembe nazaj preko PR, da drugi trenerji koristijo.

---

## Dodatni viri

- [Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/ai-foundry/)
- [Pregled gostujočih agentov](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Hitri začetek: namestite svojega prvega gostujočega agenta (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Namestitev gostujočega agenta (kako)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit za VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakti

Če imate vprašanja glede izvedbe tega srečanja, prosim odprite zadevo na [delavničnem repozitoriju](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) in označite vzdrževalca.

| Vloga                | Ime           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Vzdrževalec / kontakt| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->