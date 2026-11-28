# Modul 8 - Felsökning

Denna modul är en referensguide för vanliga problem. Bokmärk den och återkom när något går fel.

---

## 1. Behörighetsfel

### 1.1 `agents/write` behörighet nekad

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Rotorsak:** Saknas `Azure AI User`-roll på **projekt**-nivå. Detta är det vanligaste felet i workshopen.

**Lösning:**
1. Öppna [portal.azure.com](https://portal.azure.com).
2. Sök efter ditt Foundry **projekt**-namn → klicka på resultatet av typen **"Microsoft Foundry project"** (INTE överordnad konto).
3. **Åtkomstkontroll (IAM)** → **+ Lägg till** → **Lägg till rolltilldelning**.
4. Roll: **Azure AI User** → Nästa.
5. Medlemmar: Välj dig själv → Granska + tilldela → Granska + tilldela.
6. **Vänta 1–2 minuter** → prova igen.

> **Varför Owner/Contributor inte räcker:** Dessa roller ger endast *hanterings*åtgärder. Agentoperationer kräver `agents/write` *data action*, vilket endast finns i `Azure AI User`, `Azure AI Developer` eller `Azure AI Owner`. Se [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` under provisionering

**Lösning:** Be din administratör att tilldela **Contributor** på resursgruppen, eller låt dem skapa projektet åt dig och ge dig **Azure AI User** på det.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker-fel

> Docker är **valfritt**. Dessa gäller endast om Docker Desktop är installerat och tillägget försöker en lokal byggning.

### 2.1 Docker daemon körs inte

**Lösning:** Starta Docker Desktop → vänta på status "running" → verifiera med `docker info` → prova igen.

### 2.2 Bygg misslyckas med beroendefel

**Lösning:** Verifiera att `requirements.txt` är rättstavad, testa lokalt först: `pip install -r requirements.txt`.

### 2.3 Plattformsmissmatch (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentiseringsfel

### 3.1 `DefaultAzureCredential` misslyckas

**Lösning (försök i ordning):**
1. `az login` (auktorisera om)
2. `az account set --subscription "<id>"` (rätt prenumeration)
3. VS Code → Konton → Logga ut → Logga in igen
4. Verifiera: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token fungerar lokalt men inte hostat

**Förväntat:** Hosted agenter använder systemhanterad identitet, inte dina inloggningsuppgifter. Om den hostade agenten får autentiseringsfel:
- Verifiera att `AZURE_AI_MODEL_DEPLOYMENT_NAME` i `agent.yaml` pekar på ditt modellutvecklingsnamn (`FOUNDRY_PROJECT_ENDPOINT` injiceras av Foundry vid körning - deklarera det inte i `agent.yaml`)
- Kontrollera att projektets hanterade identitet har åtkomst till modellen

---

## 4. Modellfel

### 4.1 Modellutveckling hittades inte

**Lösning:** Namnet är **skiftlägeskänsligt**. Jämför `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` med exakt namn i Foundry sidofält → Modeller.

### 4.2 Ovӓntat modellutdata

**Lösning:** Granska `AGENT_INSTRUCTIONS` i `main.py` (inte trunkerat?). Testa en annan modell (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Utrullningsfel

### 5.1 ACR pull obehörig

**Lösning:** Azure Portal → Container Registry → Åtkomstkontroll (IAM) → Lägg till **AcrPull** roll till Foundry projektets hanterade identitet.

### 5.2 Agent misslyckas att starta (fastnar på "Pending" eller "Failed")

Kontrollera container-loggar i sidofältet. Vanliga orsaker:

| Loggmeddelande | Lösning |
|-------------|-----|
| `ModuleNotFoundError` | Lägg till saknat paket i `requirements.txt`, distribuera om |
| `ValueError: Missing required environment variables` | Bekräfta att `AZURE_AI_MODEL_DEPLOYMENT_NAME` är deklarerat i `agent.yaml` under `environment_variables` och har ett värde, sedan distribuera om. `FOUNDRY_PROJECT_ENDPOINT` injiceras av Foundry vid körning |
| `Address already in use` | Säkerställ att endast en process binder till port 8088 |

### 5.3 Utrullningen timear ut

**Lösning:** Kontrollera internetanslutningen. Första utrullningen pushar >100MB. Bakom en proxy? Konfigurera proxyinställningar i Docker Desktop.

---

## 6. Väg B - Foundry Local

### 6.1 Foundry Local startar inte

| Problem | Lösning |
|-------|-----|
| `foundry: command not found` | Installera om: `winget install Microsoft.FoundryLocal` |
| Otillräckliga resurser | Foundry Local behöver ~4GB ledigt RAM. Stäng andra appar. |
| Modellnedladdning misslyckas | Kontrollera diskutrymme (modeller är 2–8 GB). Försök igen: `foundry local models pull <name>` |

### 6.2 Modellfel i Foundry Local

| Problem | Lösning |
|-------|-----|
| Långsamma svar | Förväntat - lokala modeller körs på CPU om du inte har GPU. Ha tålamod. |
| Dålig kvalitet på output | Prova en större modell om din hårdvara tillåter. `phi-4-mini` är en bra balans. |
| Anslutning nekas | Verifiera att Foundry Local körs: `foundry local status`. Starta om vid behov. |

---

## 7. Snabbreferens: RBAC-roller

| Roll | Omfång | Ger |
|------|-------|--------|
| **Azure AI User** | Projekt | Dataåtgärder: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Dataåtgärder + projektskapande |
| **Azure AI Owner** | Konto | Full åtkomst + rollhantering |
| **Contributor** | Prenumeration/RG | Endast hanteringsåtgärder (**inga** dataåtgärder) |
| **Owner** | Prenumeration/RG | Hantering + rolltilldelning (**inga** dataåtgärder) |

---

## 8. Checklista för att slutföra workshopen

| # | Punkt | Modul |
|---|------|--------|
| 1 | Förutsättningar installerade och verifierade | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit tillägg installerat, projekt anslutet (eller Väg B konfigurerad) | [01](01-setup.md) |
| 3 | Hosted agent upprättad | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfigurerad, instruktioner skrivna, beroenden installerade | [03](03-configure-and-code.md) |
| 5 | Agent testad lokalt - 3 funktionella scenarier klarar | [04](04-test-locally.md) |
| 6 | Distribuerad till Foundry (endast Väg A) | [05](05-deploy-to-foundry.md) |
| 7 | Edge-case/säkerhetstester passerar i molnet (endast Väg A) | [06](06-verify-in-playground.md) |
| 8 | Sammanfattning granskad, nästa steg identifierade | [07](07-summary.md) |

---

**Föregående:** [07 - Sammanfattning](07-summary.md) · **Hem:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->