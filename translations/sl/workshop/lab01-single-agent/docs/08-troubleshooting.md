# Modul 8 - Odpravljanje težav

Ta modul je referenčni vodnik za pogoste težave. Dodajte ga med zaznamke in se vrnite, ko gre kaj narobe.

---

## 1. Napake pri dovoljenjih

### 1.1 Zavrnjen dostop `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Glavni vzrok:** Manjka vloga `Azure AI User` na ravni **projekt**. To je #1 napaka na delavnicah.

**Popravek:**
1. Odprite [portal.azure.com](https://portal.azure.com).
2. Poiščite ime vašega Foundry **projekta** → kliknite rezultat tipa **"Microsoft Foundry project"** (NE nadrejeni račun).
3. **Upravljanje dostopa (IAM)** → **+ Dodaj** → **Dodaj dodelitev vloge**.
4. Vloga: **Azure AI User** → Naprej.
5. Člani: Izberite sebe → Pregled + dodeli → Pregled + dodeli.
6. **Počakajte 1–2 minuti** → poskusite znova.

> **Zakaj vloga Lastnik/Sodelujoči ni zadostna:** Te vloge dovoljujejo samo *upravljanje*. Operacije agentov zahtevajo `agents/write` *podatkovno dejanje*, ki je na voljo samo v vlogah `Azure AI User`, `Azure AI Developer` ali `Azure AI Owner`. Oglejte si [Foundry RBAC dokumentacijo](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` med zagonom

**Popravek:** Prosite skrbnika, naj vam dodeli vlogo **Contributor** na skupini virov ali naj ustvari projekt za vas ter vam dodeli **Azure AI User**.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Počakajte do: "Registriran"
```

---

## 2. Napake z Dockerjem

> Docker je **neobvezen**. Ti napotki veljajo le, če je Docker Desktop nameščen in se razširitev poskuša lokalno zgraditi.

### 2.1 Docker daemon ne deluje

**Popravek:** Zaženite Docker Desktop → počakajte na status "running" → preverite z `docker info` → poskusite znova.

### 2.2 Gradnja spodleti zaradi napak odvisnosti

**Popravek:** Preverite pravopis v `requirements.txt`, najprej preizkusite lokalno: `pip install -r requirements.txt`.

### 2.3 Neujemanje platforme (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Napake pri preverjanju pristnosti

### 3.1 `DefaultAzureCredential` spodleti

**Popravek (poskusite po vrsti):**
1. `az login` (ponovno avtorizirajte)
2. `az account set --subscription "<id>"` (pravilna naročnina)
3. VS Code → Računi → Odjava → Ponovna prijava
4. Preverite: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Zadetki veljajo lokalno, a ne v gostovanju

**Pričakovano:** Gostujoči agenti uporabljajo sistemsko upravljano identiteto, ne vaših poverilnic. Če gostujoči agent prejme napake pristnosti:
- Preverite, da je `AZURE_AI_PROJECT_ENDPOINT` v `agent.yaml` pravilen
- Preverite, da ima upravljana identiteta projekta dostop do modela

---

## 4. Napake modela

### 4.1 Namestitev modela ni najdena

**Popravek:** Ime je **občutljivo na velike/male črke**. Primerjajte `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` z natančnim imenom v stranski vrstici Foundry → Models.

### 4.2 Nepričakovani izhod modela

**Popravek:** Preverite `AGENT_INSTRUCTIONS` v `main.py` (ali niso skrajšane?). Preizkusite drug model (`gpt-4.1` proti `gpt-4.1-mini`).

---

## 5. Napake pri nameščanju

### 5.1 Odklonjen dostop do ACR-povleci

**Popravek:** Azure Portal → Container Registry → Upravljanje dostopa (IAM) → Dodajte vlogo **AcrPull** upravljani identiteti Foundry projekta.

### 5.2 Agent ne začne (ostane "Pending" ali "Failed")

Preverite dnevnike vsebnika v stranski vrstici. Pogosti vzroki:

| Sporočilo dnevnika | Popravek |
|-------------|-----|
| `ModuleNotFoundError` | Dodajte manjkajoči paket v `requirements.txt`, znova namestite |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Dodajte spremenljivko okolja v `agent.yaml` pod `environment_variables` |
| `Address already in use` | Poskrbite, da le en proces uporablja vrata 8088 |

### 5.3 Čas namestitve poteče

**Popravek:** Preverite internetno povezavo. Prva namestitev potisne >100MB. Ste za proxyjem? Konfigurirajte nastavitve proxyja v Docker Desktop.

---

## 6. Pot B - Foundry Local

### 6.1 Foundry Local se ne zažene

| Težava | Popravek |
|-------|-----|
| `foundry: command not found` | Ponovna namestitev: `winget install Microsoft.FoundryLocal` |
| Premalo virov | Foundry Local potrebuje ~4GB prostega RAM-a. Zaprite druge aplikacije. |
| Prenos modela spodleti | Preverite prostor na disku (modeli so veliki 2–8 GB). Poskusite znova: `foundry local models pull <name>` |

### 6.2 Napake pri Foundry Local modelu

| Težava | Popravek |
|-------|-----|
| Počasni odgovori | Pričakovano - lokalni modeli delujejo na CPU, razen če imate GPU. Bodite potrpežljivi. |
| Slaba kakovost izhoda | Poskusite večji model, če vam strojna oprema to omogoča. `phi-4-mini` je dobra izbira. |
| Povezava zavrnjena | Preverite, da Foundry Local teče: `foundry local status`. Po potrebi znova zaženite. |

---

## 7. Hiter pregled: RBAC vloge

| Vloga | Območje | Dovoljenja |
|------|-------|--------|
| **Azure AI User** | Projekt | Podatkovna dejanja: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Račun | Podatkovna dejanja + ustvarjanje projektov |
| **Azure AI Owner** | Račun | Poln dostop + upravljanje vlog |
| **Contributor** | Naročnina/RG | Samo upravljalska dejanja (**ni** podatkovnih dejanj) |
| **Owner** | Naročnina/RG | Upravljanje + dodelitev vlog (**ni** podatkovnih dejanj) |

---

## 8. Kontrolni seznam zaključka delavnice

| # | Postavka | Modul |
|---|------|--------|
| 1 | Namestitev in preverjanje predpogojev | [00](00-prerequisites.md) |
| 2 | Namestitev razširitve Foundry Toolkit, povezava projekta (ali konfiguracija Poti B) | [01](01-setup.md) |
| 3 | Ustvarjen gostujoči agent | [02](02-create-hosted-agent.md) |
| 4 | Konfigurirana `.env`, napisani ukazi, nameščene odvisnosti | [03](03-configure-and-code.md) |
| 5 | Lokalno preizkušen agent - uspešno preizkušene 3 funkcionalne situacije | [04](04-test-locally.md) |
| 6 | Namestitev v Foundry (samo Pot A) | [05](05-deploy-to-foundry.md) |
| 7 | Preizkusi robnih primerov / varnosti v oblaku opravljen (samo Pot A) | [06](06-verify-in-playground.md) |
| 8 | Povzetek pregledan, določeni naslednji koraki | [07](07-summary.md) |

---

**Prejšnji:** [07 - Povzetek](07-summary.md) · **Domov:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->