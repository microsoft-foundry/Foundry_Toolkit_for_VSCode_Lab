# Moodul 8 - Tõrkeotsing

See moodul on juhend levinud probleemide lahendamiseks. Lisa see järjehoidjaks ja tule tagasi, kui midagi läheb valesti.

---

## 1. Luba vead

### 1.1 `agents/write` luba keelatud

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Peamine põhjus:** Puudub `Azure AI User` roll **projekti** tasandil. See on #1 töötoa viga.

**Parandus:**
1. Ava [portal.azure.com](https://portal.azure.com).
2. Otsi oma Foundry **projekti** nime → klõpsa tulemusele tüüpi **"Microsoft Foundry projekt"** (MITTE vanemkontol).
3. **Juurdepääsu kontroll (IAM)** → **+ Lisa** → **Lisa rolli määramine**.
4. Roll: **Azure AI User** → Järgmine.
5. Liikmed: Vali iseennast → Kinnita + määra → Kinnita + määra.
6. **Oota 1–2 minutit** → proovi uuesti.

> **Miks Owner/Contributor ei piisa:** Need rollid annavad ainult *haldustegevusi*. Agendi toimingud vajavad `agents/write` *andmetoimingut*, mida leidub ainult `Azure AI User`, `Azure AI Developer` või `Azure AI Owner`. Vaata [Foundry RBAC dokumentatsiooni](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` provisjonimise ajal

**Parandus:** Palu oma administraatoril määrata **Contributor** ressursigrupile või lase tal luua projekt sinu jaoks ja anda sulle **Azure AI User** sellele.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Dockeri vead

> Docker on **valikuline**. Need kehtivad ainult siis, kui Docker Desktop on installitud ja laiendus üritab kohalikku ehitust.

### 2.1 Docker daemon ei tööta

**Parandus:** Käivita Docker Desktop → oota "töötab" staatus → kontrolli `docker info` → proovi uuesti.

### 2.2 Ehitus ebaõnnestub sõltuvusvigade tõttu

**Parandus:** Kontrolli `requirements.txt` õigekirja, testi esmalt kohapeal: `pip install -r requirements.txt`.

### 2.3 Platvormi sobimatus (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentimise vead

### 3.1 `DefaultAzureCredential` ebaõnnestub

**Parandus (proovi järjekorras):**
1. `az login` (uuesti autentimine)
2. `az account set --subscription "<id>"` (õige tellimus)
3. VS Code → Kontod → Logi välja → Logi uuesti sisse
4. Kontrolli: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token töötab kohapeal, kuid mitte hostitud

**Oodatud:** Hostitud agendid kasutavad süsteemihaldatud identiteeti, mitte sinu mandaati. Kui hostitud agendi autentimise vead:
- Kontrolli, et `AZURE_AI_MODEL_DEPLOYMENT_NAME` `agent.yaml` viib sinu mudeli paigalduse nimele (`FOUNDRY_PROJECT_ENDPOINT` süstitakse Foundry poolt jooksuajal - ära deklareeri seda `agent.yaml`)
- Veendu, et projekti hallatud identiteedil on mudelile ligipääs

---

## 4. Mudeli vead

### 4.1 Mudeli paigaldust ei leitud

**Parandus:** Nimi on **tuntundlik**. Võrdle `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` täpse nimega Foundry küljeribal → Models.

### 4.2 Ootamatu mudeli väljund

**Parandus:** Vaata üle `AGENT_INSTRUCTIONS` `main.py` (kas pole lühendatud?). Proovi erinevat mudelit (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Paigalduse vead

### 5.1 ACR tõmbamine keelatud

**Parandus:** Azure Portaal → Container Registry → Juurdepääsu kontroll (IAM) → Lisa **AcrPull** roll Foundry projekti hallatud identiteedile.

### 5.2 Agent ei käivitu (jääb "Ootama" või "Ebaõnnestunud")

Kontrolli konteineri logisid küljeribal. Levinumad põhjused:

| Logi sõnum | Parandus |
|-------------|-----|
| `ModuleNotFoundError` | Lisa puuduolev pakett `requirements.txt`, paigalda uuesti |
| `ValueError: Missing required environment variables` | Kinnita `AZURE_AI_MODEL_DEPLOYMENT_NAME` on deklareeritud `agent.yaml` all `environment_variables` ja sellel on väärtus, seejärel paigalda uuesti. `FOUNDRY_PROJECT_ENDPOINT` süstitakse Foundry poolt jooksuajal |
| `Address already in use` | Veendu, et ainult üks protsess kasutab porti 8088 |

### 5.3 Paigaldus aegub

**Parandus:** Kontrolli internetiühendust. Esimene paigaldus tõmbab >100 MB. Kas oled proksi taga? Seadista Docker Desktopi proksi seaded.

---

## 6. Tee B - Foundry Local

### 6.1 Foundry Local ei käivitu

| Probleem | Parandus |
|-------|-----|
| `foundry: command not found` | Installi uuesti: `winget install Microsoft.FoundryLocal` |
| Ebapiisavad ressursid | Foundry Local vajab ~4GB RAM vaba. Sulge teised rakendused. |
| Mudeli allalaadimine ebaõnnestub | Kontrolli kettaruumi (mudelid on 2–8 GB). Proovi uuesti: `foundry local models pull <name>` |

### 6.2 Foundry Local mudeli vead

| Probleem | Parandus |
|-------|-----|
| Aeglased vastused | Oodatav - kohalikud mudelid töötavad CPU peal, kui sul pole GPU-d. Ole kannatlik. |
| Kehv väljundkvaliteet | Proovi suuremat mudelit, kui su riistvara seda lubab. `phi-4-mini` on hea tasakaal. |
| Ühendus keelatud | Kontrolli, et Foundry Local töötab: `foundry local status`. Taaskäivita vajadusel. |

---

## 7. Kiire viide: RBAC rollid

| Roll | Ulatus | Õigused |
|------|-------|--------|
| **Azure AI User** | Projekt | Andmetoimingud: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Andmetoimingud + projekti loomine |
| **Azure AI Owner** | Konto | Täielik juurdepääs + rollihaldus |
| **Contributor** | Tellimus/RG | Ainult haldustoimingud (**ei** andmetoimingud) |
| **Owner** | Tellimus/RG | Haldus + rolli määramine (**ei** andmetoimingud) |

---

## 8. Töötoa lõpetamise kontrollnimekiri

| # | Punkt | Moodul |
|---|------|--------|
| 1 | Eeltingimused paigaldatud ja kontrollitud | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit laiendus paigaldatud, projekt ühendatud (või Tee B konfigureeritud) | [01](01-setup.md) |
| 3 | Hostitud agent üles seatud | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfigureeritud, juhised kirja pandud, sõltuvused paigaldatud | [03](03-configure-and-code.md) |
| 5 | Agent testitud lokaalselt - 3 funktsionaalset stsenaariumi läbitud | [04](04-test-locally.md) |
| 6 | Paigaldatud Foundry-sse (ainult Tee A) | [05](05-deploy-to-foundry.md) |
| 7 | Äärmuslikud/sõltumatud testid edukad pilves (ainult Tee A) | [06](06-verify-in-playground.md) |
| 8 | Kokkuvõte üle vaadatud, järgmised sammud määratletud | [07](07-summary.md) |

---

**Eelmine:** [07 - Kokkuvõte](07-summary.md) · **Avaleht:** [Töötoa LUGEJA](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->