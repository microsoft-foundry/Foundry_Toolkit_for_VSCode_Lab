# Modul 8 - Řešení problémů

Tento modul je referenční příručka pro běžné problémy. Přidejte si ji do záložek a vraťte se sem, když něco nefunguje.

---

## 1. Chyby oprávnění

### 1.1 Zamítnuto oprávnění `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Hlavní příčina:** Chybějící role `Azure AI User` na úrovni **projektu**. Toto je nejčastější chyba na školení.

**Oprava:**
1. Otevřete [portal.azure.com](https://portal.azure.com).
2. Vyhledejte název vašeho Foundry **projektu** → klikněte na výsledek typu **"Microsoft Foundry project"** (NE rodičovský účet).
3. **Řízení přístupu (IAM)** → **+ Přidat** → **Přidat přiřazení role**.
4. Role: **Azure AI User** → Další.
5. Členové: Vyberte sebe → Přezkoumat a přiřadit → Přezkoumat a přiřadit.
6. **Počkejte 1–2 minuty** → zkuste to znovu.

> **Proč nestačí rolí Owner/Contributor:** Tyto role povolují pouze *správcovské* akce. Pro operace agenta je potřeba datová akce `agents/write`, kterou mají jen `Azure AI User`, `Azure AI Developer`, nebo `Azure AI Owner`. Viz [Foundry RBAC dokumentace](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` během nasazování

**Oprava:** Požádejte správce o přiřazení role **Contributor** na skupinu prostředků, nebo aby za vás vytvořil projekt a přidělil vám roli **Azure AI User**.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Počkejte, dokud nebude: "Registrováno"
```

---

## 2. Chyby Dockeru

> Docker je **volitelný**. Tyto chyby platí jen pokud je nainstalován Docker Desktop a rozšíření se pokouší o lokální build.

### 2.1 Docker démon neběží

**Oprava:** Spusťte Docker Desktop → počkejte na stav "running" → ověřte příkazem `docker info` → zkuste to znovu.

### 2.2 Build selže kvůli chybějícím závislostem

**Oprava:** Ověřte správnost `requirements.txt`, nejprve otestujte lokálně: `pip install -r requirements.txt`.

### 2.3 Nesoulad platformy (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Chyby autentizace

### 3.1 Selhání `DefaultAzureCredential`

**Oprava (zkuste v tomto pořadí):**
1. `az login` (reautentizace)
2. `az account set --subscription "<id>"` (správné předplatné)
3. VS Code → Účty → Odhlásit → Přihlásit znovu
4. Ověřte: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funguje lokálně, ale ne na hostovaném agentu

**Očekávané:** Hostovaní agenti používají systémovou spravovanou identitu, nikoliv vaše přihlašovací údaje. Pokud hostovaný agent dostává chyby autentizace:
- Ověřte, že `AZURE_AI_PROJECT_ENDPOINT` v `agent.yaml` je správně nastaven
- Zkontrolujte, že spravovaná identita projektu má přístup k modelu

---

## 4. Chyby modelu

### 4.1 Nasazení modelu nenalezeno

**Oprava:** Název je **case-sensitive** (rozlišuje malá a velká písmena). Porovnejte `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` s přesným názvem v postranním panelu Foundry → Models.

### 4.2 Neočekávaný výstup modelu

**Oprava:** Zkontrolujte `AGENT_INSTRUCTIONS` v `main.py` (není zkrácený?). Vyzkoušejte jiný model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Chyby nasazení

### 5.1 Nenaautorizované stažení z ACR

**Oprava:** Azure Portal → Container Registry → Řízení přístupu (IAM) → Přidejte roli **AcrPull** spravované identitě Foundry projektu.

### 5.2 Agent se nespustí (zůstává na "Pending" nebo "Failed")

Zkontrolujte protokoly kontejneru v postranním panelu. Běžné příčiny:

| Chybová zpráva | Oprava |
|-------------|-----|
| `ModuleNotFoundError` | Přidejte chybějící balíček do `requirements.txt`, znovu nasadit |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Přidejte proměnnou prostředí do `agent.yaml` pod `environment_variables` |
| `Address already in use` | Ujistěte se, že port 8088 není obsazen více procesy |

### 5.3 Vypršení časového limitu nasazení

**Oprava:** Zkontrolujte připojení k internetu. První nasazení posílá >100MB dat. Jste za proxy? Nakonfigurujte proxy v nastavení Docker Desktop.

---

## 6. Cesta B - Foundry Local

### 6.1 Foundry Local se nespustí

| Problém | Oprava |
|-------|-----|
| `foundry: command not found` | Přeinstalujte: `winget install Microsoft.FoundryLocal` |
| Nedostatek zdrojů | Foundry Local potřebuje ~4GB volné RAM. Zavřete ostatní aplikace. |
| Stahování modelu selhalo | Zkontrolujte místo na disku (modely mají 2–8 GB). Zkuste znovu: `foundry local models pull <name>` |

### 6.2 Chyby modelu Foundry Local

| Problém | Oprava |
|-------|-----|
| Pomalé odpovědi | Očekávané - lokální modely běží na CPU, pokud nemáte GPU. Buďte trpěliví. |
| Špatná kvalita výstupu | Vyzkoušejte větší model, pokud to hardware dovolí. `phi-4-mini` je dobrý kompromis. |
| Připojení odmítnuto | Ověřte, že Foundry Local běží: `foundry local status`. Pokud ne, restartujte. |

---

## 7. Rychlá reference: RBAC role

| Role | Rozsah | Uděluje |
|------|-------|--------|
| **Azure AI User** | Projekt | Datové akce: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Účet | Datové akce + vytváření projektů |
| **Azure AI Owner** | Účet | Plný přístup + správa rolí |
| **Contributor** | Předplatné/skupina prostředků | Jen správcovské akce (**bez** datových akcí) |
| **Owner** | Předplatné/skupina prostředků | Správcovské akce + přiřazování rolí (**bez** datových akcí) |

---

## 8. Kontrolní seznam dokončení školení

| # | Položka | Modul |
|---|------|--------|
| 1 | Nainstalované a ověřené předpoklady | [00](00-prerequisites.md) |
| 2 | Nainstalované rozšíření Foundry Toolkit, projekt připojen (nebo nastavená cesta B) | [01](01-setup.md) |
| 3 | Vytvořen hostovaný agent | [02](02-create-hosted-agent.md) |
| 4 | Konfigurace `.env`, napsané instrukce, nainstalované závislosti | [03](03-configure-and-code.md) |
| 5 | Agent otestován lokálně - úspěšné 3 funkční scénáře | [04](04-test-locally.md) |
| 6 | Nasazeno do Foundry (pouze cesta A) | [05](05-deploy-to-foundry.md) |
| 7 | Úspěšně projity testy okrajových případů / bezpečnosti v cloudu (pouze cesta A) | [06](06-verify-in-playground.md) |
| 8 | Shrnutí projito, definovány další kroky | [07](07-summary.md) |

---

**Předchozí:** [07 - Shrnutí](07-summary.md) · **Domů:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o omezení odpovědnosti**:
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o co největší přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Originální dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro kritické informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoli nedorozumění nebo nesprávné interpretace vzniklé použitím tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->