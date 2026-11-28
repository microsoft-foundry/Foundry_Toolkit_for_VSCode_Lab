# Modul 8 - Odpravljanje težav

Ta modul je referenčni vodnik za pogoste težave. Dodajte ga med zaznamke in se vrnite, ko nekaj ne deluje.

---

## 1. Napake pri dovoljenjih

### 1.1 `agents/write` zavrnjena dovoljenja

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Korenski vzrok:** Manjkajoča vloga `Azure AI User` na ravni **projekt**ta. To je #1 napaka v delavnici.

**Popravek:**
1. Odprite [portal.azure.com](https://portal.azure.com).
2. Poiščite ime vašega Foundry **projekt**a → kliknite rezultat tipa **"Microsoft Foundry project"** (NE nadrejeni račun).
3. **Nadzor dostopa (IAM)** → **+ Dodaj** → **Dodaj dodelitev vloge**.
4. Vloga: **Azure AI User** → Naprej.
5. Člani: Izberite sebe → Pregled + dodeli → Pregled + dodeli.
6. **Počakajte 1–2 minuti** → poskusite znova.

> **Zakaj lastnik/sodelavec ni dovolj:** Te vloge dodeljujejo samo *upravljavske* ukrepe. Agentove operacije zahtevajo `agents/write` *dejanje z podatki*, ki je na voljo le v `Azure AI User`, `Azure AI Developer` ali `Azure AI Owner`. Glejte [Foundry RBAC dokumentacijo](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` med pripravo

**Popravek:** Prosite svojega skrbnika, naj dodeli **Contributor** na skupini virov ali naj vam ustvari projekt in vam dodeli **Azure AI User** na njem.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Napake pri Dockerju

> Docker je **neobvezen**. To velja le, če je Docker Desktop nameščen in razširitev poskuša lokalno gradnjo.

### 2.1 Docker daemon ne deluje

**Popravek:** Zaženite Docker Desktop → počakajte na status "teče" → preverite z `docker info` → poskusite znova.

### 2.2 Gradnja ne uspe z napakami odvisnosti

**Popravek:** Preverite pravilnost `requirements.txt`, najprej preizkusite lokalno: `pip install -r requirements.txt`.

### 2.3 Neujemanje platforme (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Napake pri preverjanju pristnosti

### 3.1 `DefaultAzureCredential` ne uspe

**Popravek (poskusite v tem vrstnem redu):**
1. `az login` (ponovno preverjanje pristnosti)
2. `az account set --subscription "<id>"` (pravilna naročnina)
3. VS Code → Računi → Izpis → Ponovni vpis
4. Preverite: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Zeton deluje lokalno, a ne na gostovanem

**Pričakovano:** Gostovani agenti uporabljajo sistemsko upravljano identiteto, ne vaših poverilnic. Če gostovani agent dobi napake preverjanja pristnosti:
- Preverite, da se `AZURE_AI_MODEL_DEPLOYMENT_NAME` v `agent.yaml` razreši na ime vašega uvajanja modela (`FOUNDRY_PROJECT_ENDPOINT` je injektiran v Foundryu med izvajanjem - ne deklarirajte ga v `agent.yaml`)
- Preverite, da ima upravljana identiteta projekta dostop do modela

---

## 4. Napake modela

### 4.1 Uvajanje modela ni najdeno

**Popravek:** Ime je **občutljivo na velike in male črke**. Primerjajte `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` z natančnim imenom v stranski vrstici Foundry → Modeli.

### 4.2 Nepričakovani izhod modela

**Popravek:** Preglejte `AGENT_INSTRUCTIONS` v `main.py` (ni okrnjen?). Poskusite drug model (`gpt-4.1` nasproti `gpt-4.1-mini`).

---

## 5. Napake uvajanja

### 5.1 Neavtoriziran dostop do ACR za prenos

**Popravek:** Azure Portal → Registro vsebnikov → Nadzor dostopa (IAM) → Dodajte vlogo **AcrPull** upravljani identiteti Foundry projekta.

### 5.2 Agent ne uspe začeti (ostane "Čakanje" ali "Neuspešno")

Preverite dnevnike vsebnika v stranski vrstici. Pogosti vzroki:

| Sporočilo dnevnika | Popravek |
|-------------|-----|
| `ModuleNotFoundError` | Dodajte manjkajoči paket v `requirements.txt`, ponovno uvedite |
| `ValueError: Missing required environment variables` | Potrdite, da je `AZURE_AI_MODEL_DEPLOYMENT_NAME` deklariran v `agent.yaml` pod `environment_variables` in ima vrednost, nato znova uvedite. `FOUNDRY_PROJECT_ENDPOINT` je injektiran v Foundryu med izvajanjem |
| `Address already in use` | Zagotovite, da se samo en proces veže na vrata 8088 |

### 5.3 Uvajanje poteče

**Popravek:** Preverite internetno povezavo. Prvo uvajanje potisne >100MB. Za proxyjem? Konfigurirajte proxy nastavitve Docker Desktopa.

---

## 6. Pot B - Foundry Local

### 6.1 Foundry Local se ne zažene

| Težava | Popravek |
|-------|-----|
| `foundry: command not found` | Ponovna namestitev: `winget install Microsoft.FoundryLocal` |
| Premalo virov | Foundry Local potrebuje približno 4GB prostega RAM-a. Zaprite druge aplikacije. |
| Prenos modela ne uspe | Preverite diskovni prostor (modeli so 2–8 GB). Ponovno poskusite: `foundry local models pull <name>` |

### 6.2 Napake modela Foundry Local

| Težava | Popravek |
|-------|-----|
| Počasni odzivi | Pričakovano - lokalni modeli tečejo na CPU, razen če imate GPU. Bodite potrpežljivi. |
| Slaba kakovost izhoda | Poskusite večji model, če to omogoča vaša strojna oprema. `phi-4-mini` je dober kompromis. |
| Povezava zavrnjena | Preverite, da Foundry Local deluje: `foundry local status`. Po potrebi ponovno zaženite. |

---

## 7. Hitri pregled: RBAC vloge

| Vloga | Obseg | Dodeljuje |
|------|-------|--------|
| **Azure AI User** | Projekt | Dejavnosti z podatki: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Račun | Dejavnosti z podatki + ustvarjanje projekta |
| **Azure AI Owner** | Račun | Poln dostop + upravljanje vlog |
| **Contributor** | Naročnina/Skupina virov | Samo upravljavski ukrepi (**brez** dejavnosti z podatki) |
| **Owner** | Naročnina/Skupina virov | Upravljanje + dodeljevanje vlog (**brez** dejavnosti z podatki) |

---

## 8. Kontrolni seznam za dokončanje delavnice

| # | Postavka | Modul |
|---|------|--------|
| 1 | Namestitev in preverjanje predpogojev | [00](00-prerequisites.md) |
| 2 | Namestitev razširitve Foundry Toolkit, povezava s projektom (ali konfiguracija poti B) | [01](01-setup.md) |
| 3 | Gostovani agent ustvarjen | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfiguriran, napotki napisani, odvisnosti nameščene | [03](03-configure-and-code.md) |
| 5 | Agent testiran lokalno - uspešno opravljeni 3 funkcionalni scenariji | [04](04-test-locally.md) |
| 6 | Uveden v Foundry (samo pot A) | [05](05-deploy-to-foundry.md) |
| 7 | Opravljen test mejnih primerov/varnosti v oblaku (samo pot A) | [06](06-verify-in-playground.md) |
| 8 | Povzetek pregledan, naslednji koraki določeni | [07](07-summary.md) |

---

**Prejšnji:** [07 - Povzetek](07-summary.md) · **Domov:** [Uvodna stran delavnice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->