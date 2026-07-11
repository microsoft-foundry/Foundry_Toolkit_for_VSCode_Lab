# Modul 7 - Ověření v Playgroundu

⏱️ ~10 min

V tomto modulu otestujete nasazený víceagentní pracovní postup ve VS Code a Foundry Portálu a potvrdíte, že agent se chová stejně jako při lokálním testování.

---

## Proč testovat znovu po nasazení?

Hostované prostředí se od lokálního v několika důležitých ohledech liší:

| | Lokální | Hostované |
|--|-------|--------|
| **Identita** | Vaše osobní přihlášení (`DefaultAzureCredential`) | Dedikovaná identita Entra na agenta (automaticky vytvořená při nasazení) |
| **Koncový bod** | `http://localhost:8088/responses` | URL spravované Foundry Agent Service |
| **Síť** | Váš počítač → Azure OpenAI + MCP | Azure páteřní síť (nižší latence) |

Zde by se projevila chyba v nastavení prostředí, problém s RBAC nebo zablokovaný odchozí hovor MCP.

---

## Možnost A: Testování ve VS Code Playgroundu (doporučeno jako první)

### Krok 1: Přejděte na svého hostovaného agenta

1. Klikněte na ikonu **Foundry Toolkit** v panelu aktivit.
2. Rozbalte svůj projekt → **Hosted Agents (Preview)** → najděte svého agenta.

![Postranní panel Foundry Toolkit zobrazující Hosted Agents (Preview) se resume-job-fit-evaluator a jeho verzemi](../../../../../translated_images/cs/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Krok 2: Vyberte verzi

1. Klikněte na agenta pro rozbalení jeho verzí.
2. Klikněte na `v1` → ověřte, že stav je **aktivní** (postranní panel může zobrazovat "Running" nebo "Started" - obojí znamená stejný stav připravenosti).

### Krok 3: Otevřete Playground

1. Klikněte na **Playground** (nebo pravým klikem na verzi → **Open in Playground**).
2. Otevře se okno chatu na záložce VS Code.

### Krok 4: Spusťte své základní testy

Použijte tři stejné testy z [Modulu 5](05-test-locally.md). Napište každou zprávu do vstupního pole Playgroundu a stiskněte **Odeslat** (nebo **Enter**).

#### Test 1 – Kompletní životopis + JD (standardní průběh)

Vložte prompt kompletního životopisu + JD z Modulu 5, Test 1 (Jane Doe + Senior Cloud Engineer v Contoso Ltd).

**Očekáváno:**
- Skóre vhodnosti s rozpisem matematiky (škála 100 bodů)
- Sekce zkušeností odpovídajících dovednostem
- Sekce chybějících dovedností
- **Jedna karta nedostatků na chybějící dovednost** s odkazy na Microsoft Learn
- Výukový plán s časovým rámcem

#### Test 2 – Rychlý krátký test (minimální vstup)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Očekáváno:**
- Nižší skóre vhodnosti (< 40)
- Poctivé zhodnocení s etapizovanou učební cestou
- Více karet nedostatků (AWS, Kubernetes, Terraform, CI/CD, nedostatek zkušeností)

#### Test 3 – Kandidát s vysokou vhodností

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Očekáváno:**
- Vysoké skóre vhodnosti (≥ 80)
- Zaměření na připravenost na pohovor a doladění
- Málo nebo žádné karty nedostatků
- Krátký časový rámec zaměřený na přípravu

### Krok 5: Porovnejte s lokálními výsledky

Otevřete si poznámky nebo záložku z Modulu 5, kde jste si uložili lokální odpovědi. Pro každý test:

- Má odpověď **stejnou strukturu** (skóre vhodnosti, karty nedostatků, plán)?
- Dodržuje **stejná kritéria hodnocení** (rozpis 100 bodů)?
- Jsou v kartách nedostatků stále přítomny **odkazy Microsoft Learn**?
- Je zde **jedna karta nedostatků na každou chybějící dovednost** (není zkrácena)?

> **Drobný rozdíl v znění je normální** – model není deterministický. Zaměřte se na strukturu, konzistenci hodnocení a použití MCP nástroje.

---

## Možnost B: Testování ve Foundry Portálu

[Foundry Portal](https://ai.azure.com) nabízí webový playground vhodný pro sdílení s kolegy nebo stakeholdery.

### Krok 1: Otevřete Foundry Portal

1. Otevřete svůj prohlížeč a přejděte na [https://ai.azure.com](https://ai.azure.com).
2. Přihlaste se stejným Azure účtem, který jste používali během workshopu.

### Krok 2: Přejděte do svého projektu

1. Na domovské stránce hledejte vlevo na postranním panelu **Recent projects**.
2. Klikněte na název svého projektu (např. `workshop-agents`).
3. Pokud jej nevidíte, klikněte na **All projects** a vyhledejte jej.

### Krok 3: Najděte svého nasazeného agenta

1. V levé navigaci projektu klikněte na **Build** → **Agents** (nebo vyhledejte sekci **Agents**).
2. Měli byste vidět seznam agentů. Najděte svého nasazeného agenta (např. `resume-job-fit-evaluator`).
3. Klikněte na název agenta pro otevření detailní stránky.

### Krok 4: Otevřete Playground

1. Na detailní stránce agenta se podívejte do horního panelu nástrojů.
2. Klikněte na **Open in playground** (nebo **Try in playground**).
3. Otevře se chatové rozhraní.

### Krok 5: Proveďte stejné základní testy

Opakujte všechny 3 testy ze sekce VS Code Playground výše. Porovnejte každou odpověď s lokálními výsledky (Modul 5) a výsledky ve VS Code Playgroundu (Možnost A výše).

---

## Specifická ověření pro víceagentní scénář

Kromě základní správnosti ověřte tyto víceagentní specifické chování:

### Spouštění MCP nástrojů

| Kontrola | Jak ověřit | Podmínka úspěchu |
|-------|---------------|----------------|
| Volání MCP jsou úspěšná | Karty nedostatků obsahují URL `learn.microsoft.com` | Skutečné URL, ne náhradní zprávy |
| Více volání MCP | Každý vysoký/střední prioritní nedostatek má zdroje | Nejen první karta nedostatků |
| Náhradní řešení MCP funguje | Pokud URL chybí, hledejte náhradní text | Agent stále generuje karty nedostatků (s URL nebo bez) |

### Koordinace agentů

| Kontrola | Jak ověřit | Podmínka úspěchu |
|-------|---------------|----------------|
| Spustili se všichni 4 agenti | Výstup obsahuje skóre vhodnosti A karty nedostatků | Skóre od MatchingAgent, karty od GapAnalyzer |
| Sekvenční provedení | Doba odezvy je rozumná (< 2 min) | Pokud > 3 min, zkontrolujte chyby v terminálovém logu |
| Integrita datového toku | Karty nedostatků odkazují na dovednosti z matching reportu | Žádné vymyšlené dovednosti, které nejsou v JD |

---

## Hodnotící rubrika

Použijte tuto rubriku k vyhodnocení chování vašeho víceagentního pracovního postupu v hostovaném prostředí:

| # | Kritérium | Podmínka úspěchu | Splněno? |
|---|----------|---------------|-------|
| 1 | **Funkční správnost** | Agent odpovídá na životopis + JD skóre vhodnosti a analýzou nedostatků | |
| 2 | **Konzistence skórování** | Skóre vhodnosti využívá 100-bodovou škálu s rozpisem | |
| 3 | **Kompletnost karet nedostatků** | Jedna karta na každou chybějící dovednost (ne zkrácená nebo sloučená) | |
| 4 | **Integrace MCP nástroje** | Karty obsahují skutečné Microsoft Learn URL | |
| 5 | **Strukturální konzistence** | Struktura výstupu odpovídá mezi lokálním a hostovaným během | |
| 6 | **Doba odezvy** | Hostovaný agent odpovídá do 2 minut u plného hodnocení | |
| 7 | **Žádné chyby** | Žádné chyby HTTP 500, timeouty nebo prázdné odpovědi | |

> "Splněno" znamená, že všech 7 kritérií je splněno pro všechny 3 základní testy alespoň v jednom playgroundu (VS Code nebo Portál).

---

## Řešení problémů s playgroundem

| Příznak | Pravděpodobná příčina | Oprava |
|---------|-------------|-----|
| Playground se nenačítá | Kontejner není ve stavu `active` | Vraťte se k [Modulu 6](06-deploy-to-foundry.md), ověřte stav nasazení. Počkejte, pokud je `creating` |
| Agent vrací prázdnou odpověď | Název nasazení modelu nesouhlasí | Zkontrolujte `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` odpovídá modelu, který jste nasadili |
| Agent vrací chybovou zprávu | Chybějící oprávnění [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Přiřaďte **[Foundry User](https://aka.ms/foundry-ext-project-role)** (dříve Azure AI User) v rámci projektu |
| V kartách nedostatků nejsou odkazy Microsoft Learn | MCP odchozí spojení zablokováno nebo MCP server nedostupný | Zkontrolujte, zda kontejner může dosáhnout `learn.microsoft.com`. Viz [Modul 8](08-troubleshooting.md) |
| Pouze 1 karta nedostatků (zkrácená) | V instrukcích GapAnalyzer chybí blok "CRITICAL" | Prohlédněte si [Modul 3, krok 2.4](03-configure-agents.md) |
| Skóre vhodnosti výrazně odlišné od lokálního | Nasazen jiný model nebo instrukce | Porovnejte proměnné prostředí v `agent.yaml` s lokálním `.env`. Při potřeby znovu nasaďte |
| "Agent nenalezen" v Portálu | Nasazení se stále propaguje nebo selhalo | Počkejte 2 minuty, obnovte stránku. Pokud stále chybí, znovu nasaďte z [Modulu 6](06-deploy-to-foundry.md) |

---

### Kontrolní bod

- [ ] Otestován agent ve VS Code Playgroundu – všechny 3 základní testy prošly
- [ ] Otestován agent ve [Foundry Portálu](https://ai.azure.com) Playgroundu – všechny 3 základní testy prošly
- [ ] Odpovědi jsou strukturálně konzistentní s lokálním testováním (skóre vhodnosti, karty nedostatků, plán)
- [ ] Odkazy Microsoft Learn jsou přítomny v kartách nedostatků (MCP nástroj funguje v hostovaném prostředí)
- [ ] Jedna karta nedostatků na každou chybějící dovednost (bez zkrácení)
- [ ] Bez chyb nebo timeoutů během testování
- [ ] Dokončena validační rubrika (všech 7 kritérií splněno)

---

**Předchozí:** [06 - Nasazení do Foundry](06-deploy-to-foundry.md) · **Další:** [08 - Řešení problémů →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->