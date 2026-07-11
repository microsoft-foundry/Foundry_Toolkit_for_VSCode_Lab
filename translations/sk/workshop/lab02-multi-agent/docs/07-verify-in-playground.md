# Modul 7 - Overenie na ihrisku

⏱️ ~10 min

V tomto module otestujete nasadený workflow s viacerými agentmi vo VS Code a Foundry Portáli, čím potvrdíte, že agent sa správa rovnako ako pri miestnom testovaní.

---

## Prečo testovať znova po nasadení?

Hostované prostredie sa od miestneho líši v niekoľkých dôležitých ohľadoch:

| | Lokálne | Hostované |
|--|-------|--------|
| **Identita** | Vaše osobné prihlásenie (`DefaultAzureCredential`) | Vyhradená identita Entra na agenta (automaticky pridelená pri nasadení) |
| **Konfigurácia** | `http://localhost:8088/responses` | URL spravovaná Foundry Agent Service |
| **Sieť** | Vaše zariadenie → Azure OpenAI + MCP | Azure sieťové jadro (nižšia latencia) |

Zlá konfigurácia premennej prostredia, problém s RBAC alebo zablokovaný MCP odchádzajúci hovor by sa tu prejavili ako prvé.

---

## Možnosť A: Testovanie v VS Code Playground (odporúča sa najskôr)

### Krok 1: Prejdite na svojho hostovaného agenta

1. Kliknite na ikonu **Foundry Toolkit** v paneli aktivít.
2. Rozbaľte svoj projekt → **Hosted Agents (Preview)** → nájdite svojho agenta.

![Bočný panel Foundry Toolkitu zobrazujúci Hosted Agents (Preview) s resume-job-fit-evaluator a jeho nasadenými verziami](../../../../../translated_images/sk/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Krok 2: Vyberte verziu

1. Kliknite na agenta, aby sa zobrazili jeho verzie.
2. Kliknite na `v1` → overte, že stav je **aktívny** (bočný panel môže zobrazovať "Running" alebo "Started" - oboje znamená pripravený stav).

### Krok 3: Otvorte Playground

1. Kliknite na **Playground** (alebo kliknite pravým tlačidlom myši na verziu → **Open in Playground**).
2. Chat okno sa otvorí vo VS Code záložke.

### Krok 4: Spustite svoje kontrolné testy

Použite rovnaké 3 testy z [Modulu 5](05-test-locally.md). Napíšte každú správu do vstupného poľa Playground a stlačte **Odoslať** (alebo **Enter**).

#### Test 1 - Kompletné CV + pracovná ponuka (štandardný tok)

Vložte prompt s kompletným CV + pracovnou ponukou z Modulu 5, Test 1 (Jane Doe + Senior Cloud Engineer v Contoso Ltd).

**Očakávané:**
- Hodnotenie fit skóre s matematickým rozpisom (stupnica 100 bodov)
- Sekcia zodpovedajúcich zručností
- Sekcia chýbajúcich zručností
- **Jedna kartička na každú chýbajúcu zručnosť** s URL na Microsoft Learn
- Učebný plán s časovou osou

#### Test 2 - Rýchly krátky test (minimálny vstup)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Očakávané:**
- Nižšie fit skóre (< 40)
- Poctivé hodnotenie s navrhnutou učebnou cestou
- Viacero kartičiek chýbajúcich zručností (AWS, Kubernetes, Terraform, CI/CD, chýbajúce skúsenosti)

#### Test 3 - Kandidát s vysokým fit skóre

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Očakávané:**
- Vysoké fit skóre (≥ 80)
- Zameranie na pripravenosť na pohovor a zdokonalenie
- Málo alebo žiadne kartičky chýbajúcich zručností
- Krátka časová os zameraná na prípravu

### Krok 5: Porovnajte s lokálnymi výsledkami

Otvorte svoje poznámky alebo prehliadač z Modulu 5, kde ste uložili lokálne odpovede. Pre každý test:

- Má odpoveď **rovnakú štruktúru** (fit skóre, kartičky chýbajúcich zručností, plán)?
- Dodržiava **rovnaké hodnotiace kritériá** (rozpis na 100 bodov)?
- Sú v kartičkách chýbajúcich zručností stále **URL Microsoft Learn**?
- Je **jedna kartička na každú chýbajúcu zručnosť** (nie je skrátená)?

> **Menšie formulácie odlišností sú normálne** - model je nedeterministický. Zamerajte sa na štruktúru, konzistenciu hodnotenia a použitie MCP nástroja.

---

## Možnosť B: Testovanie vo Foundry Portáli

[Foundry Portál](https://ai.azure.com) poskytuje webové ihrisko vhodné na zdieľanie s tímom alebo zainteresovanými stranami.

### Krok 1: Otvorte Foundry Portál

1. Otvorte si prehliadač a prejdite na [https://ai.azure.com](https://ai.azure.com).
2. Prihláste sa rovnakým Azure účtom, ktorý ste používali počas workshopu.

### Krok 2: Prejdite do vášho projektu

1. Na domovskej stránke hľadajte **Nedávne projekty** v ľavom bočnom paneli.
2. Kliknite na názov svojho projektu (napr. `workshop-agents`).
3. Ak ho nevidíte, kliknite na **Všetky projekty** a vyhľadajte ho.

### Krok 3: Nájdite svoj nasadený agent

1. V ľavej navigácii projektu kliknite na **Build** → **Agents** (alebo vyhľadajte sekciu **Agents**).
2. Mali by ste vidieť zoznam agentov. Nájdite svoj nasadený agent (napr. `resume-job-fit-evaluator`).
3. Kliknite na názov agenta, aby sa zobrazila stránka s detailmi.

### Krok 4: Otvorte Playground

1. Na stránke detailu agenta sa pozrite na horný panel nástrojov.
2. Kliknite na **Open in playground** (alebo **Try in playground**).
3. Otvorí sa chatové rozhranie.

### Krok 5: Spustite rovnaké kontrolné testy

Opakujte všetky 3 testy zo sekcie VS Code Playground vyššie. Porovnajte každú odpoveď s lokálnymi výsledkami (Modul 5) aj s výsledkami VS Code Playground (Možnosť A vyššie).

---

## Overenie špecifické pre viacerých agentov

Okrem základnej správnosti overte tieto správanie špecifické pre viac-agentový workflow:

### Spustenie MCP nástroja

| Kontrola | Ako overiť | Podmienka úspechu |
|-------|---------------|----------------|
| MCP volania sú úspešné | Kartičky chýbajúcich zručností obsahujú URL `learn.microsoft.com` | Skutočné URL, nie náhradné správy |
| Viacnásobné MCP volania | Každá vysoká/stredná priorita má zdroje | Nielen prvá kartička |
| Náhradné spracovanie MCP | Ak chýbajú URL, skontrolujte náhradný text | Agent stále generuje kartičky (s URL alebo bez nich) |

### Koordinácia agentov

| Kontrola | Ako overiť | Podmienka úspechu |
|-------|---------------|----------------|
| Všetci 4 agenti bežali | Výstup obsahuje fit skóre AJ kartičky | Skóre od MatchingAgent, kartičky od GapAnalyzer |
| Sekvenčné spustenie | Čas odpovede je rozumný (< 2 min) | Ak > 3 min, skontrolujte chyby v termináli |
| Integrita toku dát | Kartičky odkazujú na zručnosti z matching reportu | Žiadne vymyslené zručnosti, ktoré nie sú v pracovnej ponuke |

---

## Hodnotiaca mriežka

Použite túto mriežku na vyhodnotenie správania vášho workflow s viacerými agentmi v hostovanom prostredí:

| č. | Kritériá | Podmienka úspechu | Úspešné? |
|---|----------|---------------|-------|
| 1 | **Funkčná správnosť** | Agent odpovedá na CV + pracovnú ponuku fit skóre a analýzou chýbajúcich zručností | |
| 2 | **Konzistentnosť hodnotenia** | Fit skóre používa stupnicu 100 bodov s rozpisom | |
| 3 | **Kompletnosť kartičiek** | Jedna kartička na každú chýbajúcu zručnosť (nie je skrátená alebo zlúčená) | |
| 4 | **Integrácia MCP nástroja** | Kartičky obsahujú skutočné URL Microsoft Learn | |
| 5 | **Štrukturálna konzistentnosť** | Štruktúra výstupu zhodná medzi lokálnymi a hostovanými behmi | |
| 6 | **Čas odpovede** | Hostovaný agent odpovie do 2 minút pri úplnom hodnotení | |
| 7 | **Žiadne chyby** | Žiadne HTTP 500 chyby, časové limity alebo prázdne odpovede | |

> "Úspech" znamená splnenie všetkých 7 kritérií pre všetky 3 kontrolné testy v aspoň jednom ihrisku (VS Code alebo Portál).

---

## Riešenie problémov s ihriskom

| Príznak | Pravdepodobná príčina | Riešenie |
|---------|-------------|-----|
| Ihrisko sa nenačíta | Kontajner nie je v stave `active` | Vráťte sa do [Modulu 6](06-deploy-to-foundry.md), overte stav nasadenia. Počkajte, ak je v stave `creating` |
| Agent vracia prázdnu odpoveď | Nekompatibilný názov nasadenia modelu | Skontrolujte `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` či zodpovedá vášmu nasadenému modelu |
| Agent vracia chybovú správu | Chýbajúce oprávnenie [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Priraďte rolu **[Foundry User](https://aka.ms/foundry-ext-project-role)** (predtým Azure AI User) v rámci projektu |
| V kartičkách chýbajúce zručnosti nie sú URL Microsoft Learn | MCP odchádzajúce blokované alebo MCP server nedostupný | Skontrolujte, či kontajner má prístup na `learn.microsoft.com`. Viď [Modul 8](08-troubleshooting.md) |
| Len 1 kartička chýbajúcej zručnosti (skrátená) | Chýbajú inštrukcie “CRITICAL” v GapAnalyzer | Prezrite [Modul 3, Krok 2.4](03-configure-agents.md) |
| Fit skóre výrazne odlišné od lokálneho | Nasadený iný model alebo iné inštrukcie | Porovnajte env premenné v `agent.yaml` s lokálnym `.env`. Ak treba, realokujte |
| „Agent nenájdený“ v Portáli | Nasadenie sa stále propaguje alebo zlyhalo | Počkajte 2 minúty, obnovte stránku. Ak chýba stále, znovu nasadte podľa [Modulu 6](06-deploy-to-foundry.md) |

---

### Kontrolný bod

- [ ] Otestovaný agent vo VS Code Playground - všetky 3 kontrolné testy prešli
- [ ] Otestovaný agent vo [Foundry Portáli](https://ai.azure.com) Playground - všetky 3 kontrolné testy prešli
- [ ] Odpovede sú štrukturálne konzistentné s lokálnym testovaním (fit skóre, kartičky, plán)
- [ ] URL Microsoft Learn sú prítomné v kartičkách (MCP nástroj funguje v hostovanom prostredí)
- [ ] Jedna kartička na každú chýbajúcu zručnosť (žiadne skracovanie)
- [ ] Žiadne chyby alebo časové limity počas testovania
- [ ] Dokončený hodnotiaci rubrik (všetky 7 kritérií splnených)

---

**Predchádzajúce:** [06 - Nasadenie do Foundry](06-deploy-to-foundry.md) · **Ďalšie:** [08 - Riešenie problémov →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->