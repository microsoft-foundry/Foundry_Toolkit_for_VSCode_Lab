# 7 modulis - Tikrinimas Playground

⏱️ ~10 min

Šiame modulyje testuojate savo išplatintą daugiaagentį darbo eigą VS Code ir Foundry portale, patvirtindami, kad agentas veikia taip pat kaip ir vietiniame testavime.

---

## Kodėl testuoti dar kartą po diegimo?

Talpinama aplinka skiriasi nuo vietinės keliais svarbiais aspektais:

| | Vietinė | Talpinama |
|--|-------|--------|
| **Tapatybė** | Jūsų asmeninis prisijungimas (`DefaultAzureCredential`) | Kiekvienam agentui dedikuota Entra tapatybė (automatiškai suteikiama diegimo metu) |
| **Galinis taškas** | `http://localhost:8088/responses` | Foundry Agent Service valdoma URL |
| **Tinklai** | Jūsų kompiuteris → Azure OpenAI + MCP | Azure tinklo pagrindas (mažesnis uždelsimas) |

Čia pirmiausia pasimatytų neteisingai sukonfigūruotas aplinkos kintamasis, RBAC problema arba užblokuotas MCP iškvietimas.

---

## Pasirinkimas A: Testuoti VS Code Playground (rekomenduojama pirmiausia)

### 1 žingsnis: Pereiti į savo talpinamą agentą

1. Spustelėkite **Foundry Toolkit** piktogramą Veiklos juostoje.
2. Išplėskite savo projektą → **Hosted Agents (Preview)** → suraskite savo agentą.

![Foundry Toolkit šoninė juosta rodanti Hosted Agents (Preview) su resume-job-fit-evaluator ir jos išplatintomis versijomis](../../../../../translated_images/lt/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### 2 žingsnis: Pasirinkite versiją

1. Spustelėkite ant agento, kad išplėstumėte jo versijas.
2. Spustelėkite `v1` → patikrinkite, ar būklė yra **aktyvi** (šoninė juosta gali rodyti "Running" arba "Started" – abu rodo pasiruošimo būseną).

### 3 žingsnis: Atidarykite Playground

1. Spustelėkite **Playground** (arba dešiniuoju pelės klavišu ant versijos → **Open in Playground**).
2. Atsidaro pokalbių langas VS Code skirtuke.

### 4 žingsnis: Vykdykite savo pasitikrinimus

Naudokite tuos pačius 3 testus iš [5 modulio](05-test-locally.md). Įveskite kiekvieną žinutę į Playground įvedimo langelį ir paspauskite **Send** (arba **Enter**).

#### Testas 1 - Pilnas CV + darbų aprašymas (standartinis srautas)

Įklijuokite pilną CV + JD užklausą iš 5 modulio, 1 testo (Jane Doe + vyresnysis debesų inžinierius Contoso Ltd).

**Tikėtina:**
- Atitikimo balas su atskaitos matematika (100 balų skalė)
- Atitinkančių įgūdžių skiltis
- Trūkstamų įgūdžių skiltis
- **Viena spragos kortelė kiekvienam trūkstamam įgūdžiui** su Microsoft Learn URL
- Mokymosi kelias su laiko planu

#### Testas 2 - Greitas trumpas testas (minimali įvestis)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Tikėtina:**
- Žemesnis atitikimo balas (< 40)
- Sąžininga vertinimo išvada su pakopine mokymosi eiga
- Kelios spragos kortelės (AWS, Kubernetes, Terraform, CI/CD, patirties spraga)

#### Testas 3 - Aukšto atitikimo kandidatas

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Tikėtina:**
- Aukštas atitikimo balas (≥ 80)
- Dėmesys interviu pasiruošimui ir tobulinimui
- Mažai arba jokios spragos kortelės
- Trumpas laiko planas skirtas pasiruošimui

### 5 žingsnis: Palyginkite su vietiniais rezultatais

Atidarykite savo užrašus arba naršyklės skirtuką iš 5 modulio, kuriame išsaugojote vietines atsakymų versijas. Kiekvienam testui:

- Ar atsakymas turi **tą pačią struktūrą** (atitikimo balas, spragos kortelės, mokymosi kelias)?
- Ar laikosi **tos pačios vertinimo skalės** (100 balų detalizavimas)?
- Ar **Microsoft Learn URL** vis dar yra spragos kortelėse?
- Ar yra **viena spragos kortelė kiekvienam trūkstamam įgūdžiui** (ne sutrumpinta)?

> **Nedideli žodžių skirtumai yra normalūs** – modelis yra netikslus. Dėmesį skirkite struktūrai, vertinimo nuoseklumui ir MCP įrankių naudojimui.

---

## Pasirinkimas B: Testuoti Foundry portale

[Foundry Portal](https://ai.azure.com) suteikia internetinį playground, naudingą dalinimuisi su komandos nariais ar suinteresuotais asmenimis.

### 1 žingsnis: Atidarykite Foundry portalą

1. Atidarykite naršyklę ir eikite į [https://ai.azure.com](https://ai.azure.com).
2. Prisijunkite su tuo pačiu Azure paskyros vardu, kurį naudojote viso seminaro metu.

### 2 žingsnis: Raskite savo projektą

1. Pradiniame puslapyje žiūrėkite į kairįjį šoninį meniu: **Recent projects**.
2. Spustelėkite savo projekto pavadinimą (pvz., `workshop-agents`).
3. Jei jo nematote, spustelėkite **All projects** ir suraskite jį paieška.

### 3 žingsnis: Suraskite savo išplatintą agentą

1. Projekto kairėje navigacijoje spustelėkite **Build** → **Agents** (ar paieškokite skilties **Agents**).
2. Turėtumėte matyti agentų sąrašą. Suraskite savo išplatintą agentą (pvz., `resume-job-fit-evaluator`).
3. Spustelėkite ant agento pavadinimo, kad atidarytumėte detalės puslapį.

### 4 žingsnis: Atidarykite Playground

1. Agentų detalės puslapyje pažvelkite į viršutinę įrankių juostą.
2. Spustelėkite **Open in playground** (arba **Try in playground**).
3. Atsidaro pokalbių sąsaja.

### 5 žingsnis: Vykdykite tuos pačius pasitikrinimus

Pakartokite visus 3 testus iš VS Code Playground skyriaus aukščiau. Palyginkite kiekvieną atsakymą tiek su vietiniais rezultatais (5 modulis), tiek su VS Code Playground rezultatais (Pasirinkimas A aukščiau).

---

## Daugiaagentinis specifinis patikrinimas

Be bazinio teisingumo, patikrinkite šiuos daugiaagentinius specifinius elgesius:

### MCP įrankio vykdymas

| Tikrinti | Kaip patikrinti | Įvykdymo sąlyga |
|-------|---------------|----------------|
| MCP kvietimai sėkmingi | Spragos kortelėse yra `learn.microsoft.com` URL | Tikri URL, ne atsarginiai pranešimai |
| Daugkartiniai MCP kvietimai | Kiekviena aukšto/vidutinio prioriteto spraga turi išteklių | Ne tik pirma spragos kortelė |
| MCP atsarginis veiksmas veikia | Jei URL trūksta, patikrinkite atsarginį tekstą | Agentas vis tiek generuoja spragos korteles (su arba be URL) |

### Agentų koordinavimas

| Tikrinti | Kaip patikrinti | Įvykdymo sąlyga |
|-------|---------------|----------------|
| Veikia visi 4 agentai | Išvestyje yra atitikimo balas IR spragos kortelės | Balas iš MatchingAgent, kortelės iš GapAnalyzer |
| Sekanti vykdymas | Atsakymo laikas yra pagrįstas (< 2 min) | Jei > 3 min, patikrinkite klaidas terminalo žurnale |
| Duomenų srauto vientisumas | Spragos kortelės remiasi įgūdžiais iš atitikimo ataskaitos | Nėra įsivaizduojamų įgūdžių, neegzistuojančių JD |

---

## Vertinimo lentelė

Naudokite šią lentelę vertindami daugiaagentės darbo eigos talpinamą elgesį:

| # | Kriterijus | Įvykdymo sąlyga | Atitinka? |
|---|----------|---------------|-------|
| 1 | **Funkcinis teisingumas** | Agentas atsako į CV + JD su atitikimo balu ir spragos analize | |
| 2 | **Vertinimo nuoseklumas** | Atitikimo balas naudoja 100 balų skalę su detalizacija | |
| 3 | **Spragos kortelių pilnumas** | Viena kortelė kiekvienam trūkstamam įgūdžiui (ne sutrumpinta ar sujungta) | |
| 4 | **MCP įrankio integracija** | Spragos kortelės turi tikrus Microsoft Learn URL | |
| 5 | **Struktūrinis nuoseklumas** | Išvesties struktūra sutampa tarp vietinio ir talpinimo vykdymų | |
| 6 | **Atsakymo laikas** | Talpinamas agentas atsako per 2 minutes pilname vertinime | |
| 7 | **Nėra klaidų** | Nėra HTTP 500 klaidų, nutrūkusių ryšių ar tuščių atsakymų | |

> „Atitinka“ reiškia, kad visi 7 kriterijai įvykdyti visiems 3 testams bent viename playground (VS Code ar Portal).

---

## Problemų sprendimas su playground

| Simptomas | Tikėtina priežastis | Sprendimas |
|---------|-------------|-----|
| Playground nesikrauna | Konteineris nėra `active` būklėje | Grįžkite į [6 modulį](06-deploy-to-foundry.md), patikrinkite diegimo būseną. Palaukite, jei `creating` |
| Agentas grąžina tuščią atsakymą | Modelio diegimo pavadinimo neatitikimas | Patikrinkite `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` atitinka išplatintą modelį |
| Agentas grąžina klaidos pranešimą | Trūksta [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) leidimų | Priskirkite **[Foundry User](https://aka.ms/foundry-ext-project-role)** (anksčiau Azure AI User) projekto lygiu |
| Spragos kortelėse nėra Microsoft Learn URL | MCP iškvietimai blokuojami arba MCP serveris nepasiekiamas | Patikrinkite, ar konteineris gali pasiekti `learn.microsoft.com`. Žr. [8 modulis](08-troubleshooting.md) |
| Tik 1 spragos kortelė (sutrumpinta) | GapAnalyzer nurodyme trūksta "CRITICAL" bloko | Peržiūrėkite [3 modulis, 2.4 žingsnis](03-configure-agents.md) |
| Atitikimo balas labai skiriasi nuo vietinio | Naudojamas kitas modelis arba kita instrukcija | Palyginkite `agent.yaml` aplinkos kintamuosius su vietiniu `.env`. Jei reikia, perkraukite |
| „Agentas nerastas“ Portalo puslapyje | Diegimo procesas dar nebaigtas arba nepavyko | Palaukite 2 minutes, atnaujinkite. Jei vis tiek nerandate, iš naujo įdiekite iš [6 modulio](06-deploy-to-foundry.md) |

---

### Patikros taškas

- [ ] Išbandytas agentas VS Code Playground - visi 3 testai išlaikyti
- [ ] Išbandytas agentas [Foundry portalo](https://ai.azure.com) Playground - visi 3 testai išlaikyti
- [ ] Atsakymai struktūriškai atitinka vietinius testus (atitikimo balas, spragos kortelės, mokymosi kelias)
- [ ] Microsoft Learn URL yra spragos kortelėse (MCP įrankis veikia talpinimo aplinkoje)
- [ ] Viena spragos kortelė kiekvienam trūkstamam įgūdžiui (nėra sutrumpinimų)
- [ ] Nėra klaidų ar laikmačių testavimo metu
- [ ] Užpildyta vertinimo lentelė (visi 7 kriterijai įvykdyti)

---

**Ankstesnis:** [06 - Diegimas į Foundry](06-deploy-to-foundry.md) · **Kitas:** [08 - Problemų sprendimas →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->