# Modul 8 - Rješavanje problema

Ovaj modul je referentni vodič za uobičajene probleme. Dodajte ga u oznake i vratite se kad nešto pođe po zlu.

---

## 1. Pogreške dozvola

### 1.1 Odbijena dozvola `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Glavni uzrok:** Nedostaje uloga `Azure AI User` na razini **projekta**. Ovo je #1 greška na radionici.

**Rješenje:**
1. Otvorite [portal.azure.com](https://portal.azure.com).
2. Potražite ime vašeg Foundry **projekta** → kliknite rezultat tipa **"Microsoft Foundry project"** (NE nadređeni račun).
3. **Upravljanje pristupom (IAM)** → **+ Dodaj** → **Dodaj dodjelu uloge**.
4. Uloga: **Azure AI User** → Dalje.
5. Članovi: Odaberite sebe → Pregledajte + dodijelite → Pregledajte + dodijelite.
6. **Pričekajte 1–2 minute** → ponovno pokušajte.

> **Zašto uloge Owner/Contributor nisu dovoljne:** Te uloge daju samo *upravljanje*. Operacije agenta zahtijevaju `agents/write` *data action*, koja je dostupna samo u `Azure AI User`, `Azure AI Developer` ili `Azure AI Owner`. Pogledajte [Foundry RBAC dokumentaciju](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` tijekom provisioninga

**Rješenje:** Zamolite svog administratora da vam dodijeli ulogu **Contributor** na grupi resursa ili neka vam oni kreiraju projekt i dodijele ulogu **Azure AI User** na njemu.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Pričekajte dok ne bude: "Registrirano"
```

---

## 2. Docker pogreške

> Docker je **opcionalan**. Ovo se odnosi samo ako je Docker Desktop instaliran i ekstenzija pokušava lokalnu izgradnju.

### 2.1 Docker daemon nije pokrenut

**Rješenje:** Pokrenite Docker Desktop → pričekajte status "running" → provjerite s `docker info` → pokušajte ponovno.

### 2.2 Izgradnja ne uspijeva zbog ovisnosti

**Rješenje:** Provjerite pravopis `requirements.txt`, prvo testirajte lokalno: `pip install -r requirements.txt`.

### 2.3 Neusklađenost platforme (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Pogreške autentikacije

### 3.1 Neuspjeh `DefaultAzureCredential`

**Rješenje (pokušajte po redu):**
1. `az login` (ponovno se prijavite)
2. `az account set --subscription "<id>"` (odaberite ispravnu pretplatu)
3. VS Code → Računi → Odjava → Ponovna prijava
4. Provjerite: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token radi lokalno, ali ne na hostingu

**Očekivano:** Hostirani agenti koriste identitet kojim upravlja sustav, ne vaše vjerodajnice. Ako hostirani agent dobiva pogreške autentikacije:
- Provjerite je li `AZURE_AI_PROJECT_ENDPOINT` u `agent.yaml` ispravan
- Provjerite ima li upravljani identitet projekta pristup modelu

---

## 4. Pogreške modela

### 4.1 Nije pronađeno postavljanje modela

**Rješenje:** Ime je **osjetljivo na velika i mala slova**. Usporedite `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` s točnim imenom u Foundry bočnoj traci → Models.

### 4.2 Neočekivani izlaz modela

**Rješenje:** Pregledajte `AGENT_INSTRUCTIONS` u `main.py` (nije li skraćeno?). Probajte drugi model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Pogreške implementacije

### 5.1 Neautorizirano povlačenje iz ACR

**Rješenje:** Azure portal → Container Registry → Upravljanje pristupom (IAM) → Dodajte ulogu **AcrPull** upravljanom identitetu Foundry projekta.

### 5.2 Agent ne uspijeva pokrenuti se (ostaje "Pending" ili "Failed")

Provjerite logove kontejnera u bočnoj traci. Uobičajeni uzroci:

| Poruka u logu | Rješenje |
|-------------|-----|
| `ModuleNotFoundError` | Dodajte nedostajuću biblioteku u `requirements.txt`, ponovno implementirajte |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Dodajte varijablu okoliša u `agent.yaml` unutar `environment_variables` |
| `Address already in use` | Osigurajte da samo jedan proces koristi port 8088 |

### 5.3 Implementacija ističe

**Rješenje:** Provjerite internetsku vezu. Prva implementacija šalje >100MB. Koristite li proxy? Konfigurirajte proxy postavke u Docker Desktopu.

---

## 6. Put B - Foundry Local

### 6.1 Foundry Local se ne pokreće

| Problem | Rješenje |
|-------|-----|
| `foundry: command not found` | Ponovna instalacija: `winget install Microsoft.FoundryLocal` |
| Nedostatak resursa | Foundry Local treba ~4GB slobodne RAM memorije. Zatvorite ostale aplikacije. |
| Preuzimanje modela ne uspijeva | Provjerite slobodni prostor na disku (modeli su 2–8 GB). Ponovno pokušajte: `foundry local models pull <name>` |

### 6.2 Pogreške modela u Foundry Local

| Problem | Rješenje |
|-------|-----|
| Spori odgovori | Očekivano - lokalni modeli rade na CPU osim ako nemate GPU. Budite strpljivi. |
| Loša kvaliteta izlaza | Probajte veći model ako vam hardver dopušta. `phi-4-mini` je dobar kompromis. |
| Povezivanje odbijeno | Provjerite radi li Foundry Local: `foundry local status`. Ponovo pokrenite ako treba. |

---

## 7. Kratki pregled: RBAC uloge

| Uloga | Opseg | Dodjeljuje |
|------|-------|--------|
| **Azure AI User** | Projekt | Data actions: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Račun | Data actions + kreiranje projekta |
| **Azure AI Owner** | Račun | Potpuni pristup + upravljanje ulogama |
| **Contributor** | Pretplata/RG | Samo upravljačke radnje (**nema** data actions) |
| **Owner** | Pretplata/RG | Upravljanje + dodjela uloga (**nema** data actions) |

---

## 8. Popis za dovršetak radionice

| # | Stavka | Modul |
|---|------|--------|
| 1 | Preduvjeti instalirani i verificirani | [00](00-prerequisites.md) |
| 2 | Ekstenzija Foundry Toolkit instalirana, projekt povezan (ili konfiguriran Put B) | [01](01-setup.md) |
| 3 | Hostirani agent postavljen | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfiguriran, upute napisane, ovisnosti instalirane | [03](03-configure-and-code.md) |
| 5 | Agent testiran lokalno - 3 funkcionalna scenarija uspješna | [04](04-test-locally.md) |
| 6 | Implementiran na Foundry (samo Put A) | [05](05-deploy-to-foundry.md) |
| 7 | Prolazak testova rubnih slučajeva/sigurnosti u oblaku (samo Put A) | [06](06-verify-in-playground.md) |
| 8 | Sažetak pregledan, identificirani sljedeći koraci | [07](07-summary.md) |

---

**Prethodno:** [07 - Sažetak](07-summary.md) · **Početna:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->