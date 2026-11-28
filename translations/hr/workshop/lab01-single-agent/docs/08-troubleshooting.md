# Modul 8 - Rješavanje problema

Ovaj modul je referentni vodič za uobičajene probleme. Označite ga i vratite se kada nešto pođe po zlu.

---

## 1. Pogreške s dopuštenjima

### 1.1 `agents/write` pristup odbijen

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Primarni uzrok:** Nedostaje `Azure AI User` uloga na razini **projekta**. Ovo je greška #1 na radionici.

**Popravak:**
1. Otvorite [portal.azure.com](https://portal.azure.com).
2. Pretražite naziv svog Foundry **projekta** → kliknite rezultat tipa **"Microsoft Foundry project"** (NE roditeljski račun).
3. **Kontrola pristupa (IAM)** → **+ Dodaj** → **Dodaj dodjelu uloge**.
4. Uloga: **Azure AI User** → Dalje.
5. Članovi: Odaberite sebe → Pregled + dodjela → Pregled + dodjela.
6. **Pričekajte 1–2 minute** → pokušajte ponovo.

> **Zašto uloge Owner/Contributor nisu dovoljne:** Te uloge dopuštaju samo *upravljanje*. Operacije agenta zahtijevaju `agents/write` *data action*, koja je dostupna samo u `Azure AI User`, `Azure AI Developer` ili `Azure AI Owner`. Pogledajte [Foundry RBAC dokumentaciju](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` tijekom provisioninga

**Popravak:** Zamolite administratora da vam dodijeli **Contributor** na grupi resursa ili da vam kreira projekt i dodijeli **Azure AI User** ulogu.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Docker pogreške

> Docker je **opcionalan**. Ovo se odnosi samo ako je Docker Desktop instaliran i proširenje pokušava lokalno graditi.

### 2.1 Docker daemon nije pokrenut

**Popravak:** Pokrenite Docker Desktop → pričekajte status "running" → provjerite s `docker info` → pokušajte ponovo.

### 2.2 Gradnja ne uspijeva zbog pogrešaka u ovisnostima

**Popravak:** Provjerite pravopis `requirements.txt`, prvo testirajte lokalno: `pip install -r requirements.txt`.

### 2.3 Neusklađenost platforme (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Pogreške provjere autentičnosti

### 3.1 `DefaultAzureCredential` ne uspijeva

**Popravak (pokušajte redom):**
1. `az login` (ponovna autentifikacija)
2. `az account set --subscription "<id>"` (ispravna pretplata)
3. VS Code → Računi → Odjava → Ponovna prijava
4. Provjerite: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token radi lokalno, ali ne i na hostu

**Očekivano:** Hostani agenti koriste identitet kojim upravlja sustav, a ne vaše vjerodajnice. Ako hostani agent dobiva pogreške autentičnosti:
- Provjerite da `AZURE_AI_MODEL_DEPLOYMENT_NAME` u `agent.yaml` pokazuje na naziv vaše implementacije modela (`FOUNDRY_PROJECT_ENDPOINT` se ubacuje od strane Foundryja u vrijeme izvođenja - nemojte ga deklarirati u `agent.yaml`)
- Provjerite da upravljani identitet projekta ima pristup modelu

---

## 4. Pogreške modela

### 4.1 Implementacija modela nije pronađena

**Popravak:** Naziv je **osjetljiv na velika i mala slova**. Usporedite `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` s točnim nazivom u Foundry bočnoj traci → Models.

### 4.2 Neočekivani izlaz iz modela

**Popravak:** Pregledajte `AGENT_INSTRUCTIONS` u `main.py` (nije li skraćeno?). Pokušajte s drugim modelom (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Pogreške implementacije

### 5.1 Nije dozvoljeno povlačenje iz ACR-a

**Popravak:** Azure Portal → Container Registry → Kontrola pristupa (IAM) → Dodajte ulogu **AcrPull** upravljanom identitetu Foundry projekta.

### 5.2 Agent ne uspijeva pokrenuti se (ostaje "Pending" ili "Failed")

Provjerite zapise kontejnera u bočnoj traci. Uobičajeni uzroci:

| Poruka u zapisu | Popravak |
|-------------|-----|
| `ModuleNotFoundError` | Dodajte nedostajući paket u `requirements.txt`, ponovo implementirajte |
| `ValueError: Missing required environment variables` | Potvrdite da je `AZURE_AI_MODEL_DEPLOYMENT_NAME` deklariran u `agent.yaml` pod `environment_variables` i ima vrijednost, zatim ponovo implementirajte. `FOUNDRY_PROJECT_ENDPOINT` se ubacuje od strane Foundryja u runtime |
| `Address already in use` | Osigurajte da samo jedan proces koristi port 8088 |

### 5.3 Vrijeme implementacije ističe

**Popravak:** Provjerite internetsku vezu. Prva implementacija gura >100MB. Jeste li iza proxyja? Konfigurirajte proxy postavke Docker Desktopa.

---

## 6. Put B - Foundry Local

### 6.1 Foundry Local se neće pokrenuti

| Problem | Popravak |
|-------|-----|
| `foundry: command not found` | Ponovna instalacija: `winget install Microsoft.FoundryLocal` |
| Nedovoljno resursa | Foundry Local treba ~4GB slobodne RAM memorije. Zatvorite druge aplikacije. |
| Preuzimanje modela ne uspije | Provjerite prostor na disku (modeli su 2–8 GB). Pokušajte ponovo: `foundry local models pull <name>` |

### 6.2 Pogreške modela u Foundry Local

| Problem | Popravak |
|-------|-----|
| Spora odzivnost | Očekivano - lokalni modeli se pokreću na CPU-u osim ako nemate GPU. Budite strpljivi. |
| Loša kvaliteta izlaza | Pokušajte s većim modelom ako to vaš hardver dopušta. `phi-4-mini` je dobar kompromis. |
| Veza odbijena | Provjerite pokrenutost Foundry Locala: `foundry local status`. Ponovo pokrenite ako je potrebno. |

---

## 7. Brzi pregled: RBAC uloge

| Uloga | Opseg | Dopuštenja |
|------|-------|--------|
| **Azure AI User** | Projekt | Data actions: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Račun | Data actions + kreiranje projekata |
| **Azure AI Owner** | Račun | Puni pristup + upravljanje ulogama |
| **Contributor** | Pretplata/GR | Samo upravljanje (**nema** data actions) |
| **Owner** | Pretplata/GR | Upravljanje + dodjela uloga (**nema** data actions) |

---

## 8. Popis za završetak radionice

| # | Stavka | Modul |
|---|------|--------|
| 1 | Preduvjeti instalirani i potvrđeni | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit proširenje instalirano, projekt povezan (ili Put B konfiguriran) | [01](01-setup.md) |
| 3 | Postavljen hostani agent | [02](02-create-hosted-agent.md) |
| 4 | `.env` konfiguriran, upute napisane, ovisnosti instalirane | [03](03-configure-and-code.md) |
| 5 | Agent testiran lokalno - 3 funkcionalna scenarija uspješna | [04](04-test-locally.md) |
| 6 | Implementirano u Foundry (samo Put A) | [05](05-deploy-to-foundry.md) |
| 7 | Testovi rubnih slučajeva/sigurnosti uspješni u oblaku (samo Put A) | [06](06-verify-in-playground.md) |
| 8 | Sažetak pregledan, identificirani sljedeći koraci | [07](07-summary.md) |

---

**Prethodno:** [07 - Sažetak](07-summary.md) · **Početna:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->