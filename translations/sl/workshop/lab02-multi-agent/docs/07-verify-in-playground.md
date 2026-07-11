# Modul 7 - Preverjanje v Playground

⏱️ ~10 min

V tem modulu preizkusite svoj nameščeni večagentni delovni tok v VS Code in Foundry portalu ter potrdite, da agent deluje enako kot pri lokalnem testiranju.

---

## Zakaj ponovno testirati po namestitvi?

Gostujoče okolje se od lokalnega razlikuje v nekaj pomembnih pogledih:

| | Lokalno | Gostujoče |
|--|-------|--------|
| **Identiteta** | Vaša osebna prijava (`DefaultAzureCredential`) | Dodeljena Entra identiteta na agenta (samodejno zagotovljena ob namestitvi) |
| **Končna točka** | `http://localhost:8088/responses` | URL, ki ga upravlja Foundry Agent Service |
| **Omrežje** | Vaš računalnik → Azure OpenAI + MCP | Hrbtno omrežje Azure (nižja latenca) |

Napačno nastavljena spremenljivka okolja, težava z RBAC ali blokiran izhodni klic MCP bi se tukaj pojavili najprej.

---

## Možnost A: Test v VS Code Playground (priporočeno najprej)

### Korak 1: Pomaknite se do svojega gostujočega agenta

1. Kliknite ikono **Foundry Toolkit** v vrstici z dejavnostmi.
2. Razširite svoj projekt → **Gostujoči agenti (predogled)** → poiščite svojega agenta.

![V stranski vrstici Foundry Toolkit prikazani Gostujoči agenti (predogled) z resume-job-fit-evaluator in njegovimi nameščenimi različicami](../../../../../translated_images/sl/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Korak 2: Izberite različico

1. Kliknite na agenta, da razširite njegove različice.
2. Kliknite `v1` → preverite, da je stanje **aktivno** (stranska vrstica lahko prikazuje "Running" ali "Started" - oba pomenita pripravljenost).

### Korak 3: Odprite Playground

1. Kliknite **Playground** (ali z desnim klikom na različico → **Odpri v Playground**).
2. Odpre se pogovorno okno v zavihku VS Code.

### Korak 4: Zaženite svoje osnovne teste

Uporabite iste 3 teste iz [Modula 5](05-test-locally.md). Vsako sporočilo vnesite v vhodno polje Playground in pritisnite **Pošlji** (ali **Enter**).

#### Test 1 - Celoten življenjepis + opis delovnega mesta (standardni postopek)

Prilepite poziv za celoten življenjepis + opis delovnega mesta iz Modula 5, Test 1 (Jane Doe + višji oblačni inženir pri Contoso Ltd).

**Pričakovano:**
- Ocena ustreznosti z razčlenitvijo (lestvica do 100 točk)
- Sekcija ujemajočih se veščin
- Sekcija manjkajočih veščin
- **Ena kartica vrzeli za vsako manjkajočo veščino** z URL-ji Microsoft Learn
- Načrt učenja z časovnico

#### Test 2 - Hitri kratek test (minimalni vnos)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Pričakovano:**
- Nižja ocena ustreznosti (< 40)
- Poštena ocena z načrtom učenja v fazah
- Več kartic vrzeli (AWS, Kubernetes, Terraform, CI/CD, razlika v izkušnjah)

#### Test 3 - Kandidat z visoko ustreznostjo

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Pričakovano:**
- Visoka ocena ustreznosti (≥ 80)
- Osredotočenost na pripravljenost za razgovor in izpopolnjevanje
- Malo ali nobenih kartic vrzeli
- Kratka časovnica osredotočena na pripravo

### Korak 5: Primerjajte z lokalnimi rezultati

Odprite svoje zapiske ali zavihek brskalnika iz Modula 5, kjer ste shranili lokalne odzive. Za vsak test preverite:

- Ali ima odgovor **isto strukturo** (ocena ustreznosti, kartice vrzeli, načrt)?
- Ali sledi **isti sistemu ocenjevanja** (razčlenitev do 100 točk)?
- Ali so **URL-ji Microsoft Learn** še vedno prisotni v karticah vrzeli?
- Ali je **ena kartica vrzeli na vsako manjkajočo veščino** (neokrajšano)?

> **Manjše razlike v besedilu so običajne** - model ni determinističen. Osredotočite se na strukturo, konsistentnost ocenjevanja in uporabo orodja MCP.

---

## Možnost B: Test v Foundry portalu

[Foundry portal](https://ai.azure.com) ponuja spletni Playground, ki je uporaben za deljenje s sodelavci ali deležniki.

### Korak 1: Odprite Foundry portal

1. Odprite brskalnik in pojdite na [https://ai.azure.com](https://ai.azure.com).
2. Prijavite se z istim Azure računom, ki ste ga uporabljali v celotnem delavnici.

### Korak 2: Pomaknite se do svojega projekta

1. Na domači strani poglejte na **Nedavni projekti** na levi stranski vrstici.
2. Kliknite ime svojega projekta (npr. `workshop-agents`).
3. Če ga ne vidite, kliknite **Vsi projekti** in ga poiščite.

### Korak 3: Poiščite svoj nameščeni agent

1. V levi navigaciji projekta kliknite **Build** → **Agents** (ali poiščite razdelek **Agents**).
2. Videli boste seznam agentov. Poiščite svoj nameščeni agent (npr. `resume-job-fit-evaluator`).
3. Kliknite na ime agenta, da odprete njegovo stran z informacijami.

### Korak 4: Odprite Playground

1. Na strani z informacijami o agentu glejte na zgornjo orodno vrstico.
2. Kliknite **Open in playground** (ali **Try in playground**).
3. Odpre se pogovorni vmesnik.

### Korak 5: Zaženite iste osnovne teste

Ponovite vseh 3 teste iz razdelka VS Code Playground zgoraj. Primerjajte vsak odgovor tako z lokalnimi rezultati (Modul 5) kot z rezultati VS Code Playground (Možnost A zgoraj).

---

## Večagentno specifična preverjanja

Poleg osnovne pravilnosti preverite naslednje posebnosti večagentnega delovanja:

### Izvajanje orodja MCP

| Preveri | Kako preveriti | Pogoj za uspeh |
|-------|---------------|----------------|
| Klici MCP uspešni | Kartice vrzeli vsebujejo URL-je `learn.microsoft.com` | Pravi URL-ji, ne nadomestna sporočila |
| Več klicev MCP | Vsaka vrzel z visoko/srednjo prioriteto ima vire | Ne samo prva kartica vrzeli |
| Rezervna možnost MCP deluje | Če URL-ji manjkajo, preverite rezervno besedilo | Agent še vedno tvori kartice vrzeli (z ali brez URL-jev) |

### Koordinacija agentov

| Preveri | Kako preveriti | Pogoj za uspeh |
|-------|---------------|----------------|
| Vsi 4 agenti so se zagnali | Izhod vsebuje oceno ustreznosti IN kartice vrzeli | Oceno daje MatchingAgent, kartice GapAnalyzer |
| Zaporedno izvajanje | Čas odgovora je razumen (< 2 min) | Če > 3 min, preverite napake v terminalnem dnevniku |
| Celovitost pretoka podatkov | Kartice vrzeli se sklicujejo na veščine iz poročila primernosti | Brez zamišljenih veščin, ki niso v JD |

---

## Merila za validacijo

Uporabite to merila za oceno vedenja vašega večagentnega delovnega toka v gostujočem okolju:

| # | Merilo | Pogoj za uspeh | Opravljen? |
|---|----------|---------------|-------|
| 1 | **Funkcionalna pravilnost** | Agent odgovori na življenjepis + JD z oceno ustreznosti in analizo vrzeli | |
| 2 | **Konsistentnost ocenjevanja** | Ocena ustreznosti temelji na lestvici do 100 z razčlenitvijo | |
| 3 | **Popolnost kartic vrzeli** | Ena kartica na vsako manjkajočo veščino (neokrajšano ali združeno) | |
| 4 | **Integracija orodja MCP** | Kartice vrzeli vključujejo prave URL-je Microsoft Learn | |
| 5 | **Strukturna konsistentnost** | Struktura izhoda se ujema med lokalnim in gostujočim izvajanjem | |
| 6 | **Čas odgovora** | Gostujoči agent odgovori v 2 minutah za celotno oceno | |
| 7 | **Brez napak** | Brez HTTP 500 napak, časovnih omejitev ali praznih odgovorov | |

> "Uspeh" pomeni, da so vsa 7 merila izpolnjena za vseh 3 osnovne teste v vsaj enem playgroundu (VS Code ali portal).

---

## Odpravljanje težav s playgroundom

| Simptom | Verjetni vzrok | Popravek |
|---------|-------------|-----|
| Playground se ne naloži | Kontejner ni v stanju `active` | Vrnite se na [Modul 6](06-deploy-to-foundry.md), preverite stanje namestitve. Počakajte, če je `creating` |
| Agent vrne prazen odgovor | Ime namestitve modela se ne ujema | Preverite `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` naj ustreza vašemu nameščenemu modelu |
| Agent vrne sporočilo o napaki | Manjkajoče dovoljenje [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Dodelite **[Foundry User](https://aka.ms/foundry-ext-project-role)** (prej Azure AI User) na obsegu projekta |
| V karticah vrzeli ni URL-jev Microsoft Learn | MCP izhodni klic blokiran ali MCP strežnik ni dosegljiv | Preverite, ali kontejner doseže `learn.microsoft.com`. Glej [Modul 8](08-troubleshooting.md) |
| Le 1 kartica vrzeli (okrajšano) | Manjkajoča navodila GapAnalyzer z blokom "CRITICAL" | Preglejte [Modul 3, Korak 2.4](03-configure-agents.md) |
| Ocena ustreznosti se močno razlikuje od lokalne | Nameščen drugačen model ali navodila | Primerjajte spremenljivke okolja `agent.yaml` z lokalnim `.env`. Po potrebi znova namestite |
| "Agent ni najden" v portalu | Namestitev se še uveljavlja ali ni uspela | Počakajte 2 minuti, osvežite. Če še vedno manjka, znova namestite iz [Modula 6](06-deploy-to-foundry.md) |

---

### Kontrolna točka

- [ ] Preizkusili agenta v VS Code Playground - vsi 3 osnovni testi uspešni
- [ ] Preizkusili agenta v [Foundry portalu](https://ai.azure.com) Playground - vsi 3 osnovni testi uspešni
- [ ] Odzivi so strukturno skladni z lokalnim testiranjem (ocena ustreznosti, kartice vrzeli, načrt)
- [ ] URL-ji Microsoft Learn so prisotni v karticah vrzeli (orodje MCP deluje v gostujočem okolju)
- [ ] Ena kartica vrzeli na vsako manjkajočo veščino (brez okrajšav)
- [ ] Brez napak ali časovnih omejitev med testiranjem
- [ ] Izpolnili ste rubriko za validacijo (vse 7 meril uspešno)

---

**Prejšnje:** [06 - Deploy to Foundry](06-deploy-to-foundry.md) · **Naslednje:** [08 - Odpravljanje težav →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->