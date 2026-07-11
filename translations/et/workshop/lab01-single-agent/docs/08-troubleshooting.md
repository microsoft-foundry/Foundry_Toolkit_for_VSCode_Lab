# Moodul 8 - Tõrkeotsing

See moodul on viide korduvatele probleemidele. Lisa see järjehoidjasse ja tule tagasi, kui midagi läheb valesti.

---

## 1. Õiguste vead

### 1.1 `agents/write` luba keelatud

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Põhjus:** Puudub `Azure AI User` roll **projekti** tasandil. See on #1 töötoa viga.

**Lahendus:**
1. Ava [portal.azure.com](https://portal.azure.com).
2. Otsi oma Foundry **projekti** nime → klõpsa tulemusele tüüpi **"Microsoft Foundry project"** (EI lapse konto).
3. **Juurdepääsu kontroll (IAM)** → **+ Lisa** → **Lisa rolli määramine**.
4. Roll: **Azure AI User** → Järgmine.
5. Liikmed: Vali iseenda konto → Kinnita + määra → Kinnita + määra.
6. **Oota 1–2 minutit** → proovi uuesti.

> **Miks Owner/Contributor ei piisa:** Need rollid annavad ainult *haldustegevusi*. Agendi toimingud vajavad `agents/write` *andmetoimingut*, mis on ainult `Azure AI User`, `Azure AI Developer` või `Azure AI Owner` rollides. Vaata [Foundry RBAC dokumentatsiooni](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` provisioneerimisel

**Lahendus:** Palu adminil määrata **Contributor** ressursside rühmale või las tal luua projekt sinu eest ja anda sulle seal **Azure AI User** õigused.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Oota kuni: "Registreeritud"
```

---

## 2. Dockeri vead

> Docker on **valikuline**. Need kehtivad ainult juhul, kui Docker Desktop on installitud ja laiendus proovib lokaalset ehitust.

### 2.1 Dockeri daemon ei tööta

**Lahendus:** Käivita Docker Desktop → oota, kuni olek on "töötab" → kontrolli `docker info` käsuga → proovi uuesti.

### 2.2 Ehitus ebaõnnestub sõltuvuste vigade tõttu

**Lahendus:** Kontrolli `requirements.txt` õigekirja, testi esmalt lokaalselt: `pip install -r requirements.txt`.

### 2.3 Platvormi mittevastavus (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Autentimise vead

### 3.1 `DefaultAzureCredential` ebaõnnestub

**Lahendus (proovi järjekorras):**
1. `az login` (uuesti autentimine)
2. `az account set --subscription "<id>"` (õige tellimus)
3. VS Code → Kontod → Logi välja → Logi uuesti sisse
4. Kontrolli: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token töötab lokaalselt, kuid mitte hostitud keskkonnas

**Oodatav:** Hostitud agendid kasutavad süsteemi hallatavat identiteeti, mitte sinu volitusi. Kui hostitud agent saab autentimisvigu:
- Kontrolli `AZURE_AI_PROJECT_ENDPOINT` väärtust `agent.yaml` failis, et see oleks õige
- Veendu, et projekti hallataval identiteedil on mudeli juurde pääs

---

## 4. Mudeli vead

### 4.1 Mudeli rakendus ei leitud

**Lahendus:** Nimi on **tõstutundlik**. Võrdle `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` täpset nime Foundry küljeribal → Mudelid.

### 4.2 Mudeli ootamatu väljund

**Lahendus:** Vaata üle `AGENT_INSTRUCTIONS` failis `main.py` (kas pole lühendatud?). Proovi teist mudelit (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Rakenduse vead

### 5.1 ACR tõmbamine on volitamata

**Lahendus:** Azure Portaal → Container Registry → Juurdepääsu kontroll (IAM) → Lisa **AcrPull** roll Foundry projekti hallatavale identiteedile.

### 5.2 Agent ei käivitu (jääb olekusse "Ootel" või "Ebaõnnestunud")

Vaata konteineri logisid küljeribal. Levinumad põhjused:

| Logi teade | Lahendus |
|-------------|-----|
| `ModuleNotFoundError` | Lisa puuduv pakett `requirements.txt`-i, uuesti juurutamine |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Lisa keskkonnamuutuja `agent.yaml` alla `environment_variables` |
| `Address already in use` | Väldi, et ainult üks protsess kasutab porti 8088 |

### 5.3 Rakenduse juurutamine aegub

**Lahendus:** Kontrolli internetiühendust. Esimene juurutamine kannab üle >100MB. Kas oled puhverserveri taga? Sea Docker Desktop puhverserveri seaded.

---

## 6. Tee B - Foundry Local

### 6.1 Foundry Local ei käivitu

| Probleem | Lahendus |
|-------|-----|
| `foundry: command not found` | Paigalda uuesti: `winget install Microsoft.FoundryLocal` |
| Ebapiisavad ressursid | Foundry Local vajab vabaks ~4GB RAM-i. Sulge teised rakendused. |
| Mudeli allalaadimine ebaõnnestub | Kontrolli kettaruumi (mudelid on 2–8 GB). Proovi uuesti: `foundry local models pull <name>` |

### 6.2 Foundry Local mudeli vead

| Probleem | Lahendus |
|-------|-----|
| Aeglased vastused | Oodatud - kohalikud mudelid töötavad CPU-l, kui sul pole GPU-d. Ole kannatlik. |
| Kehv kvaliteediga väljund | Proovi suuremat mudelit, kui sinu riistvara seda võimaldab. `phi-4-mini` on hea tasakaal. |
| Ühendus keelatud | Kontrolli, et Foundry Local töötab: `foundry local status`. Taaskäivita vajadusel. |

---

## 7. Kiirreferents: RBAC rollid

| Roll | Ulatus | Annab õiguse |
|------|-------|--------|
| **Azure AI User** | Projekt | Andmetoimingud: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Andmetoimingud + projekti loomine |
| **Azure AI Owner** | Konto | Täielik ligipääs + rollihaldus |
| **Contributor** | Tellimus/ressursside grupp | Ainult haldustoimingud (**mitte** andmetoimingud) |
| **Owner** | Tellimus/ressursside grupp | Haldus + rolli määramine (**mitte** andmetoimingud) |

---

## 8. Töötoa lõpetamise kontrollnimekiri

| # | Ülesanne | Moodul |
|---|------|--------|
| 1 | Eeldused paigaldatud ja kontrollitud | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit laiendus paigaldatud, projekt ühendatud (või Tee B konfigureeritud) | [01](01-setup.md) |
| 3 | Hostitud agent loodud | [02](02-create-hosted-agent.md) |
| 4 | `.env` seadistatud, juhised kirjutatud, sõltuvused paigaldatud | [03](03-configure-and-code.md) |
| 5 | Agent testitud lokaalselt - 3 tegevusolukorda läbitud | [04](04-test-locally.md) |
| 6 | Juhtimine Foundry-sse (ainult Tee A) | [05](05-deploy-to-foundry.md) |
| 7 | Äärmusjuhtumite/turvalisuse testid pilves läbitud (ainult Tee A) | [06](06-verify-in-playground.md) |
| 8 | Kokkuvõte vaadatud üle, järgmised sammud määratud | [07](07-summary.md) |

---

**Eelmine:** [07 - Kokkuvõte](07-summary.md) · **Kodu:** [Töötoa README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->