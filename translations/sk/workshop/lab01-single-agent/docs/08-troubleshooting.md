# Modul 8 - Riešenie problémov

Tento modul je referenčná príručka pre bežné problémy. Uložte si ho do záložiek a vráťte sa k nemu, keď niečo prestane fungovať.

---

## 1. Chyby povolení

### 1.1 Zamietnuté povolenie `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Hlavná príčina:** Chýba rola `Azure AI User` na úrovni **projektu**. Toto je chyba číslo 1 na workshope.

**Oprava:**
1. Otvorte [portal.azure.com](https://portal.azure.com).
2. Vyhľadajte názov vášho Foundry **projektu** → kliknite na výsledok typu **"Microsoft Foundry project"** (NIE na rodičovský účet).
3. **Prístupová kontrola (IAM)** → **+ Pridať** → **Pridať priradenie roly**.
4. Rola: **Azure AI User** → Ďalej.
5. Členovia: Vyberte seba → Skontrolovať + priradiť → Skontrolovať + priradiť.
6. **Počkajte 1–2 minúty** → skúste znova.

> **Prečo nie je postačujúce byť Owner/Contributor:** Tieto roly povoľujú iba *správcovské* akcie. Operácie agenta vyžadujú `agents/write` *dátovú akciu*, ktorá je dostupná iba v rolách `Azure AI User`, `Azure AI Developer` alebo `Azure AI Owner`. Viac nájdete v [Foundry RBAC dokumentácii](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` počas provisioning

**Oprava:** Požiadajte správcu, aby vám priradil rolu **Contributor** na skupinu prostriedkov, alebo nech vám vytvorí projekt a priradí rolu **Azure AI User**.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Počkajte, kým: "Registrovaný"
```

---

## 2. Chyby Dockeru

> Docker je **voliteľný**. Tieto chyby sa vyskytujú iba ak je nainštalovaný Docker Desktop a rozšírenie sa snaží o lokálnu zostavu.

### 2.1 Docker daemon neběží

**Oprava:** Spustite Docker Desktop → počkajte na stav "beží" → overte cez `docker info` → skúste znova.

### 2.2 Build zlyhá s chybami závislostí

**Oprava:** Skontrolujte pravopis `requirements.txt`, najskôr testujte lokálne: `pip install -r requirements.txt`.

### 2.3 Nezhoda platformy (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Chyby overenia

### 3.1 Zlyhanie `DefaultAzureCredential`

**Oprava (vyskúšajte v poradí):**
1. `az login` (znovu sa prihláste)
2. `az account set --subscription "<id>"` (správny predplatný plán)
3. VS Code → Účty → Odhlásiť sa → Prihlásiť sa znova
4. Overte: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token funguje lokálne, ale nie na hostingu

**Očakávané:** Hostované agenty používajú systémovú spravovanú identitu, nie vaše poverenia. Ak hostovaný agent dostáva chyby overenia:
- Overte, či je `AZURE_AI_PROJECT_ENDPOINT` v `agent.yaml` správny
- Skontrolujte, či má spravovaná identita projektu prístup k modelu

---

## 4. Chyby modelu

### 4.1 Nenájdené nasadenie modelu

**Oprava:** Názov je **citlivý na veľkosť písmen**. Porovnajte `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` s presným názvom v postrannom paneli Foundry → Modely.

### 4.2 Neočakávaný výstup modelu

**Oprava:** Skontrolujte `AGENT_INSTRUCTIONS` v `main.py` (nie je orezané?). Vyskúšajte iný model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Chyby nasadenia

### 5.1 Zákaz stiahnutia z ACR

**Oprava:** Azure Portal → Container Registry → Prístupová kontrola (IAM) → Pridať rolu **AcrPull** spravovanej identite Foundry projektu.

### 5.2 Agent sa nespustí (stále "Čaká" alebo "Zlyhané")

Skontrolujte logy kontajnera v postrannom paneli. Bežné príčiny:

| Chybové hlásenie | Oprava |
|-------------|-----|
| `ModuleNotFoundError` | Pridajte chýbajúci balík do `requirements.txt`, znovu nasadiť |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Pridajte env premennú do `agent.yaml` pod `environment_variables` |
| `Address already in use` | Uistite sa, že port 8088 viaže len jeden proces |

### 5.3 Nasadenie vypršalo

**Oprava:** Skontrolujte pripojenie na internet. Prvé nasadenie posiela >100MB dát. Ste za proxy? Nakonfigurujte proxy nastavenia v Docker Desktop.

---

## 6. Cesta B - Foundry Local

### 6.1 Foundry Local sa nespustí

| Problém | Oprava |
|-------|-----|
| `foundry: command not found` | Preinštalujte: `winget install Microsoft.FoundryLocal` |
| Nedostatok prostriedkov | Foundry Local potrebuje ~4GB voľnej RAM. Zatvorte iné aplikácie. |
| Sťahovanie modelu zlyhá | Skontrolujte voľné miesto na disku (modely majú 2–8 GB). Skúste znova: `foundry local models pull <name>` |

### 6.2 Chyby modelu vo Foundry Local

| Problém | Oprava |
|-------|-----|
| Pomalé odpovede | Očakávané - lokálne modely bežia na CPU, ak nemáte GPU. Buďte trpezliví. |
| Výstup nízkej kvality | Vyskúšajte väčší model, ak to váš hardvér dovoľuje. `phi-4-mini` je dobrý kompromis. |
| Pripojenie odmietnuté | Overte, že Foundry Local beží: `foundry local status`. Ak nie, reštartujte. |

---

## 7. Rýchla referencia: RBAC roly

| Rola | Rozsah | Udeľuje |
|------|-------|--------|
| **Azure AI User** | Projekt | Dátové akcie: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Účet | Dátové akcie + vytváranie projektov |
| **Azure AI Owner** | Účet | Plný prístup + správa rolí |
| **Contributor** | Predplatné/RG | Iba správcovské akcie (**bez** dátových akcií) |
| **Owner** | Predplatné/RG | Správcovské akcie + prideľovanie rolí (**bez** dátových akcií) |

---

## 8. Kontrolný zoznam dokončenia workshopu

| # | Položka | Modul |
|---|------|--------|
| 1 | Nainštalované a overené predpoklady | [00](00-prerequisites.md) |
| 2 | Rozšírenie Foundry Toolkit nainštalované, projekt pripojený (alebo nastavená Cesta B) | [01](01-setup.md) |
| 3 | Hostovaný agent vytvorený | [02](02-create-hosted-agent.md) |
| 4 | `.env` nastavený, napísané inštrukcie, nainštalované závislosti | [03](03-configure-and-code.md) |
| 5 | Agent otestovaný lokálne - 3 funkčné scenáre prešli | [04](04-test-locally.md) |
| 6 | Nasadené vo Foundry (len Cesta A) | [05](05-deploy-to-foundry.md) |
| 7 | Testy okrajových prípadov/bezpečnosti v cloude prešli (len Cesta A) | [06](06-verify-in-playground.md) |
| 8 | Preskúmané zhrnutie, identifikované ďalšie kroky | [07](07-summary.md) |

---

**Predchádzajúce:** [07 - Zhrnutie](07-summary.md) · **Domov:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->