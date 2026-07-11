# Moduli 8 - Kutatua Matatizo

Moduli hii ni mwongozo wa marejeleo kwa matatizo ya kawaida. Iweke alama na urudi ukiwa na tatizo lolote.

---

## 1. Makosa ya Ruhusa

### 1.1 Ruhusa ya `agents/write` imenyimwa

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Sababu kuu:** Ukosefu wa jukumu la `Azure AI User` kwenye kiwango cha **mradi**. Hili ndilo kosa #1 la warsha.

**Jibu:**
1. Fungua [portal.azure.com](https://portal.azure.com).
2. Tafuta jina la mradi wako wa Foundry → bonyeza matokeo ya aina **"Microsoft Foundry project"** (SI akaunti ya mzazi).
3. **Udhibiti wa upatikanaji (IAM)** → **+ Ongeza** → **Ongeza utumishi wa jukumu**.
4. Jukumu: **Azure AI User** → Ifuatayo.
5. Wanachama: Jichague wewe mwenyewe → Kagua + toa jukumu → Kagua + toa.
6. **Subiri dakika 1–2** → jaribu tena.

> **Kwa nini Miliki/Kichangiaji haitoshi:** Majukumu haya yanatoa tu vitendo vya *usimamizi*. Operesheni za wakala zinahitaji *kitendo cha data* cha `agents/write`, ambacho kiko tu katika `Azure AI User`, `Azure AI Developer`, au `Azure AI Owner`. Angalia [nyaraka za Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` wakati wa upatikanaji

**Jibu:** Muombe msimamizi wako kumpa **Mchangiaji** kwenye kundi la rasilimali, au awapange waweze kuunda mradi na kukupa **Azure AI User** kwa mradi huo.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Subiri hadi: "Imesajiliwa"
```

---

## 2. Makosa ya Docker

> Docker ni **hiari**. Haya yanatumika tu ikiwa Docker Desktop imewekwa na kifunga kina jaribu kujenga eneo la ndani.

### 2.1 Docker daemon haifanyi kazi

**Jibu:** Anzisha Docker Desktop → subiri hali ya "inaendelea" → hakiki kwa `docker info` → jaribu tena.

### 2.2 Ujenzi unashindwa na makosa ya utegemezi

**Jibu:** Hakiki tahajia ya `requirements.txt`, jaribu kwanza eneo la ndani: `pip install -r requirements.txt`.

### 2.3 Mlingano wa jukwaa (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Makosa ya Uthibitishaji

### 3.1 `DefaultAzureCredential` inashindwa

**Jibu (jaribu kwa mpangilio):**
1. `az login` (thibitisha tena)
2. `az account set --subscription "<id>"` (choo sahihi cha usajili)
3. VS Code → Akaunti → Toka → Ingia tena
4. Hakiki: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token inafanya kazi eneo la ndani lakini si kwenye mwenyeji

**Inatarajiwa:** Wakala waliowekwa mgeni hutumia utambulisho unaosimamiwa na mfumo, si sifa zako. Ikiwa wakala mgeni anapokea makosa ya uthibitishaji:
- Hakikisha `AZURE_AI_PROJECT_ENDPOINT` katika `agent.yaml` iko sahihi
- Angalia kwamba utambulisho wa mradi una ruhusa ya kutumia mfano

---

## 4. Makosa ya Mfano

### 4.1 Usambazaji wa mfano haupatikani

**Jibu:** Jina ni **linalotegemea herufi**. Linganisha `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` na jina halisi kwenye nafasi ya upande ya Foundry → Models.

### 4.2 Matokeo ya mfano yasiyotarajiwa

**Jibu:** Kagua `AGENT_INSTRUCTIONS` katika `main.py` (si ikatafsiriwa?). Jaribu mfano tofauti (`gpt-4.1` dhidi ya `gpt-4.1-mini`).

---

## 5. Makosa ya Usambazaji

### 5.1 Kukosa ruhusa ya kuvuta kutoka ACR

**Jibu:** Azure Portal → Usajili wa Kontena → Udhibiti wa upatikanaji (IAM) → Ongeza jukumu la **AcrPull** kwa utambulisho unaosimamiwa wa mradi wa Foundry.

### 5.2 Wakala anashindwa kuanzisha (anabaki "Pending" au "Failed")

Angalia kumbukumbu za kontena upande wa mti. Sababu za kawaida:

| Ujumbe wa kumbukumbu | Jibu |
|----------------------|-------|
| `ModuleNotFoundError` | Ongeza kifurushi kilichokosekana kwa `requirements.txt`, wasambaze tena |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Ongeza var ya mazingira kwenye `agent.yaml` chini ya `environment_variables` |
| `Address already in use` | Hakikisha mchakato mmoja tu unaunganisha bandari 8088 |

### 5.3 Usambazaji umekoma muda wake

**Jibu:** Hakiki muunganisho wa intaneti. Usambazaji wa kwanza hutuma >100MB. Unatumia wakala wa mwelekeo? Sanidi mipangilio ya wakala wa Docker Desktop.

---

## 6. Njia B - Foundry Local

### 6.1 Foundry Local haishehi kuanza

| Tatizo | Jibu |
|---------|-------|
| `foundry: command not found` | Sakinisha tena: `winget install Microsoft.FoundryLocal` |
| Rasilimali hazitoshi | Foundry Local inahitaji takriban 4GB RAM huru. Funga programu nyingine. |
| Downlod ya mfano inashindwa | Angalia nafasi ya disk (mifano ni 2–8 GB). Jaribu tena: `foundry local models pull <name>` |

### 6.2 Makosa ya mfano wa Foundry Local

| Tatizo | Jibu |
|---------|-------|
| Majibu polepole | Ni ya kawaida - mifano ya ndani hufanya kazi kwenye CPU isipokuwa una GPU. Kuwa na subira. |
| Matokeo mabaya | Jaribu mfano mkubwa ikiwa vifaa vyako vinaruhusu. `phi-4-mini` ni mpangilio mzuri. |
| Muunganisho umekataliwa | Hakiki Foundry Local ipo hai: `foundry local status`. Anzisha tena ikiwezekana. |

---

## 7. Marejeleo ya haraka: Majukumu ya RBAC

| Jukumu | Upeo | Hutoa |
|---------|-------|--------|
| **Azure AI User** | Mradi | Vitendo vya data: `agents/write`, `agents/read` |
| **Azure AI Developer** | Mradi/Akaunti | Vitendo vya data + uundaji wa mradi |
| **Azure AI Owner** | Akaunti | Upatikanaji kamili + usimamizi wa majukumu |
| **Contributor** | Usajili/Kundi la Rasilimali | Vitendo vya usimamizi tu (**hapana** vitendo vya data) |
| **Owner** | Usajili/Kundi la Rasilimali | Usimamizi + utoaji wa jukumu (**hapana** vitendo vya data) |

---

## 8. Orodha ya ukamilishaji wa warsha

| # | Kipengele | Moduli |
|---|----------|--------|
| 1 | Vifaa vya kuanza vimewekwa na kuthibitishwa | [00](00-prerequisites.md) |
| 2 | Kiendelezi cha Foundry Toolkit kimewekwa, mradi umeunganishwa (au Njia B imesanidiwa) | [01](01-setup.md) |
| 3 | Wakala mgeni ameundwa | [02](02-create-hosted-agent.md) |
| 4 | `.env` imesanidiwa, maelekezo yameandikwa, utegemezi umewekwa | [03](03-configure-and-code.md) |
| 5 | Wakala amejaribiwa eneo la ndani - matukio 3 ya utendaji yanapita | [04](04-test-locally.md) |
| 6 | Imewekwa kwenye Foundry (Njia A pekee) | [05](05-deploy-to-foundry.md) |
| 7 | Vipimo vya kesi za kivuli/usalama vinapita kwenye wingu (Njia A pekee) | [06](06-verify-in-playground.md) |
| 8 | Muhtasari umepitiwa, hatua zinazofuata zimetambuliwa | [07](07-summary.md) |

---

**Iliyopita:** [07 - Muhtasari](07-summary.md) · **Nyumbani:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->