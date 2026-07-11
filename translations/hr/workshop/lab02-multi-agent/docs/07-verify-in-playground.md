# Modul 7 - Provjera u Playgroundu

⏱️ ~10 min

U ovom modulu testirate svoj distribuirani višestruki agentni tijek rada u VS Codeu i Foundry Portalu, potvrđujući da agent ponaša isto kao i kod lokalnog testiranja.

---

## Zašto testirati ponovno nakon objave?

Okruženje za hosting razlikuje se od lokalnog u nekoliko bitnih aspekata:

| | Lokalno | Hostano |
|--|-------|--------|
| **Identitet** | Vaša osobna prijava (`DefaultAzureCredential`) | Namjenski Entra identitet po agentu (automatski provisioniran prilikom objave) |
| **Krajnja točka** | `http://localhost:8088/responses` | Foundry Agent Service upravljani URL |
| **Mreža** | Vaše računalo → Azure OpenAI + MCP | Azure backbone (niža latencija) |

Neispravno konfigurirana varijabla okoline, RBAC problem ili blokirani MCP odlazni poziv prvo bi se ovdje otkrili.

---

## Opcija A: Testiranje u VS Code Playgroundu (preporučeno prvo)

### Korak 1: Pronađite svoj hostani agent

1. Kliknite ikonu **Foundry Toolkit** u Activity Baru.
2. Proširite svoj projekt → **Hosted Agents (Preview)** → pronađite svog agenta.

![Foundry Toolkit bočna traka prikazuje Hosted Agents (Preview) s resume-job-fit-evaluator i njegovim objavljenim verzijama](../../../../../translated_images/hr/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Korak 2: Odaberite verziju

1. Kliknite na agenta da proširite njegove verzije.
2. Kliknite `v1` → provjerite je li status **aktivan** (bočna traka može prikazati "Running" ili "Started" - oba označavaju isto stanje spremnosti).

### Korak 3: Otvorite Playground

1. Kliknite **Playground** (ili desni klik na verziju → **Open in Playground**).
2. Pojavit će se prozor chata u VS Code kartici.

### Korak 4: Pokrenite svoje preliminarne testove

Koristite ista 3 testa iz [Modula 5](05-test-locally.md). Upišite svaku poruku u ulazno polje Playgrounda i pritisnite **Send** (ili **Enter**).

#### Test 1 - Cijeli životopis + JD (standardni tijek)

Zalijepite cijeli prompt za životopis + JD iz Modula 5, Test 1 (Jane Doe + Senior Cloud Engineer u Contoso Ltd).

**Očekivano:**
- Fit score s razradom (škala od 100 bodova)
- Sekcija podudaranih vještina
- Sekcija nedostajućih vještina
- **Jedna kartica praznine po nedostajućoj vještini** sa Microsoft Learn URL-ovima
- Plan učenja s vremenskim okvirom

#### Test 2 - Brzi kratki test (minimalni unos)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Očekivano:**
- Niži fit score (< 40)
- Iskrena procjena sa faznim planom učenja
- Više kartica praznine (AWS, Kubernetes, Terraform, CI/CD, nedostatak iskustva)

#### Test 3 - Kandidat s visokim fit scoreom

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Očekivano:**
- Visok fit score (≥ 80)
- Fokus na spremnost za intervju i usavršavanje
- Malo ili nema kartica praznine
- Kratki vremenski okvir usmjeren na pripremu

### Korak 5: Usporedite s lokalnim rezultatima

Otvorite svoje bilješke ili karticu preglednika iz Modula 5 gdje ste spremili lokalne odgovore. Za svaki test:

- Ima li odgovor **istu strukturu** (fit score, kartice praznine, roadmapa)?
- Prati li **isti kriterij bodovanja** (razrada od 100 bodova)?
- Jesu li **Microsoft Learn URL-ovi** još prisutni u karticama praznine?
- Je li **jedna kartica praznine po nedostajućoj vještini** (nije skraćena)?

> **Male razlike u formulacijama su normalne** - model nije determinističan. Usredotočite se na strukturu, dosljednost bodovanja i korištenje MCP alata.

---

## Opcija B: Testiranje u Foundry Portalu

[Foundry Portal](https://ai.azure.com) nudi web bazirani playground koristan za dijeljenje s kolegama ili dionicima.

### Korak 1: Otvorite Foundry Portal

1. Otvorite preglednik i idite na [https://ai.azure.com](https://ai.azure.com).
2. Prijavite se sa istim Azure računom koji ste koristili tijekom radionice.

### Korak 2: Navigirajte do svog projekta

1. Na početnoj stranici potražite **Recent projects** u lijevom bočnom izborniku.
2. Kliknite ime svog projekta (npr., `workshop-agents`).
3. Ako ga ne vidite, kliknite **All projects** i potražite ga.

### Korak 3: Pronađite svog objavljenog agenta

1. U lijevom navigacijskom izborniku projekta kliknite **Build** → **Agents** (ili potražite odjeljak **Agents**).
2. Trebali biste vidjeti popis agenata. Pronađite svog objavljenog agenta (npr., `resume-job-fit-evaluator`).
3. Kliknite na ime agenta da otvorite njegovu stranicu s detaljima.

### Korak 4: Otvorite Playground

1. Na stranici s detaljima agenta pogledajte gornju alatnu traku.
2. Kliknite **Open in playground** (ili **Try in playground**).
3. Otvara se chat sučelje.

### Korak 5: Pokrenite iste preliminarne testove

Ponovite sva 3 testa iz odjeljka VS Code Playground gore. Usporedite svaki odgovor s lokalnim rezultatima (Modul 5) i rezultatima iz VS Code Playgrounda (Opcija A).

---

## Specifična verifikacija za višestruke agente

Osim osnovne ispravnosti, provjerite sljedeća ponašanja specifična za višestruke agente:

### Izvršenje MCP alata

| Provjera | Kako potvrditi | Uvjet prolaska |
|---------|---------------|-----------------|
| MCP pozivi uspijevaju | Kartice praznina sadrže `learn.microsoft.com` URL-ove | Stvarni URL-ovi, ne rezervne poruke |
| Višestruki MCP pozivi | Svaka praznina visokog/srednjeg prioriteta ima resurse | Ne samo prva kartica praznine |
| MCP rezervna opcija funkcionira | Ako URL-ovi nedostaju, provjerite za rezervni tekst | Agent i dalje generira kartice praznina (s ili bez URL-ova) |

### Koordinacija agenata

| Provjera | Kako potvrditi | Uvjet prolaska |
|---------|---------------|-----------------|
| Sva 4 agenta su izvršena | Izlaz sadrži fit score I kartice praznina | Rezultat dolazi iz MatchingAgent, kartice iz GapAnalyzer |
| Sekvencijalno izvršavanje | Vrijeme odgovora je razumno (< 2 min) | Ako > 3 min, provjerite greške u zapisniku terminala |
| Integritet prijenosa podataka | Kartice praznina referenciraju vještine iz izvještaja podudaranja | Nema izmišljenih vještina koje nisu u JD-u |

---

## Pravilnik za validaciju

Koristite ovaj pravilnik za evaluaciju ponašanja vašeg višestrukog agentnog tijeka rada u hostanom okruženju:

| # | Kriterij | Uvjet prolaska | Prolaz? |
|---|----------|---------------|-------|
| 1 | **Funkcionalna ispravnost** | Agent odgovara na životopis + JD s fit score i analizom praznina | |
| 2 | **Dosljednost bodovanja** | Fit score koristi 100-bodovnu skalu s razradom | |
| 3 | **Potpunost kartica praznina** | Jedna kartica po nedostajućoj vještini (nije skraćena ni spojena) | |
| 4 | **Integracija MCP alata** | Kartice praznina uključuju stvarne Microsoft Learn URL-ove | |
| 5 | **Strukturna dosljednost** | Izlazna struktura odgovara između lokalnog i hostanog pokretanja | |
| 6 | **Vrijeme odgovora** | Hostani agent odgovara unutar 2 minute za punu procjenu | |
| 7 | **Bez grešaka** | Nema HTTP 500 grešaka, timeouta ili praznih odgovora | |

> "Prolaz" znači da su svih 7 kriterija zadovoljena za sva 3 preliminarna testa u barem jednom playgroundu (VS Code ili Portal).

---

## Rješavanje problema s playgroundom

| Simptom | Vjerojatni uzrok | Rješenje |
|---------|-----------------|---------|
| Playground se ne učitava | Kontejner nije u `active` stanju | Vratite se na [Modul 6](06-deploy-to-foundry.md), provjerite status objave. Pričekajte ako je `creating` |
| Agent vraća prazan odgovor | Neusklađenost imena implementacije modela | Provjerite `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` odgovara vašem objavljenom modelu |
| Agent vraća poruku o grešci | Nedostajuće dopuštenje [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Dodijelite ulogu **[Foundry User](https://aka.ms/foundry-ext-project-role)** (ranije Azure AI User) na razini projekta |
| Nema Microsoft Learn URL-ova u karticama praznina | MCP odlazni pozivi blokirani ili MCP poslužitelj nedostupan | Provjerite može li kontejner pristupiti `learn.microsoft.com`. Pogledajte [Modul 8](08-troubleshooting.md) |
| Samo 1 kartica praznine (skraćena) | Upute GapAnalyzer-a nedostaju "CRITICAL" blok | Pregledajte [Modul 3, Korak 2.4](03-configure-agents.md) |
| Fit score znatno drugačiji od lokalnog | Raspoređen različiti model ili upute | Usporedite `agent.yaml` env var s lokalnim `.env`. Ponovno implementirajte ako je potrebno |
| "Agent nije pronađen" u Portalu | Implementacija se još propagira ili je neuspjela | Pričekajte 2 minute, osvježite. Ako i dalje nedostaje, ponovno implementirajte iz [Modul 6](06-deploy-to-foundry.md) |

---

### Kontrolna točka

- [ ] Testirali agenta u VS Code Playgroundu - sva 3 preliminarna testa su prošla
- [ ] Testirali agenta u [Foundry Portalu](https://ai.azure.com) Playgroundu - sva 3 preliminarna testa su prošla
- [ ] Odgovori su strukturno konzistentni s lokalnim testiranjem (fit score, kartice praznina, roadmapa)
- [ ] Microsoft Learn URL-ovi su prisutni u karticama praznina (MCP alat radi u hostanom okruženju)
- [ ] Jedna kartica praznine po nedostajućoj vještini (nema skraćivanja)
- [ ] Nema grešaka ili timeouta tijekom testiranja
- [ ] Završili pravilnik za validaciju (sva 7 kriterija su prošla)

---

**Prethodno:** [06 - Implementacija u Foundry](06-deploy-to-foundry.md) · **Sljedeće:** [08 - Rješavanje problema →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->