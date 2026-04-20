# Moduli 8 - Utatuzi wa Matatizo

Moduli hii ni mwongozo wa rufaa kwa kila tatizo la kawaida linalokumbwa wakati wa warsha. Iweke kwenye alama - utarudi kwenye hii kila wakati kitu kinapokosea.

---

## 1. Makosa ya ruhusa

### 1.1 Ruhusa ya `agents/write` imetolewa kosa

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Sababu kuu:** Huna jukumu la `Azure AI User` kwenye ngazi ya **mradi**. Hii ni kosa la kawaida zaidi katika warsha.

**Marekebisho - hatua kwa hatua:**

1. Fungua [https://portal.azure.com](https://portal.azure.com).
2. Katika kisanduku cha utafutaji juu, andika jina la **mradi wako wa Foundry** (mfano, `workshop-agents`).
3. **Muhimu:** Bonyeza matokeo yanayoonyesha aina **"Microsoft Foundry project"**, SI akaunti mama/hub rasilimali. Hizi ni rasilimali tofauti na maeneo tofauti ya RBAC.
4. Katika navugazi ya kushoto ya ukurasa wa mradi, chagua **Udhibiti wa upatikanaji (IAM)**.
5. Bonyeza kichupo cha **Role assignments** ili kuangalia kama tayari una jukumu hilo:
   - Tafuta jina lako au barua pepe.
   - Ikiwa `Azure AI User` tayari iko katika orodha → kosa lina sababu tofauti (angaliza Hatua 8 hapo chini).
   - Ikiwa haipo → endelea kuongeza.
6. Bonyeza **+ Add** → **Add role assignment**.
7. Katika kichupo cha **Role**:
   - Tafuta [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Ichague kutoka kwenye matokeo.
   - Bonyeza **Next**.
8. Katika kichupo cha **Members**:
   - Chagua **User, group, or service principal**.
   - Bonyeza **+ Select members**.
   - Tafuta jina lako au barua pepe.
   - Ji chague mwenyewe kutoka kwenye matokeo.
   - Bonyeza **Select**.
9. Bonyeza **Review + assign** → tena **Review + assign**.
10. **Subiri kwa dakika 1-2** - mabadiliko ya RBAC yanachukua muda kusambaa.
11. Jaribu tena operesheni iliyoshindwa.

> **Kwa nini Owner/Contributor haizitoshi:** Azure RBAC ina aina mbili za ruhusa - *vitendo vya usimamizi* na *vitendo vya data*. Owner na Contributor hutoa vitendo vya usimamizi (kuunda rasilimali, kuhariri mipangilio), lakini operesheni za wakala zinahitaji `agents/write` **kitendo cha data**, ambacho kiko tu katika majukumu ya `Azure AI User`, `Azure AI Developer`, au `Azure AI Owner`. Angalia [kuhusu RBAC ya Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` wakati wa upangaji wa rasilimali

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Sababu kuu:** Huna ruhusa ya kuunda au kubadilisha rasilimali za Azure katika usajili/gari la rasilimali hii.

**Marekebisho:**
1. Muulize msimamizi wa usajili wako kukupa jukumu la **Contributor** kwenye kundi la rasilimali ambapo mradi wako wa Foundry uko.
2. Vinginevyo, muulize waunde mradi wa Foundry kwa niaba yako na akupe **Azure AI User** kwenye mradi.

### 1.3 `SubscriptionNotRegistered` kwa [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Sababu kuu:** Usajili wa Azure bado haujasajili mtoa rasilimali anayehitajika kwa Foundry.

**Marekebisho:**

1. Fungua terminali na endesha:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Subiri usajili ukamilike (inaweza kuchukua dakika 1-5):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Matokeo yanayotarajiwa: `"Registered"`
3. Jaribu tena operesheni.

---

## 2. Makosa ya Docker (ikiwa Docker imewekwa tu)

> Docker ni **hiari** kwa warsha hii. Makosa haya yatumika tu ikiwa umeweka Docker Desktop na nyongeza ya Foundry inajaribu ujenzi wa kontena kwa ndani.

### 2.1 Docker daemon haijasimama

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Marekebisho - hatua kwa hatua:**

1. **Tafuta Docker Desktop** katika menyu yako ya Start (Windows) au Applications (macOS) na uzindue.
2. Subiri dirisha la Docker Desktop lionyeshe **"Docker Desktop is running"** - kawaida huchukua sekunde 30-60.
3. Tafuta ikoni ya simba wa Docker kwenye tray ya mfumo (Windows) au bar ya menyu (macOS). Piga utaftaji kando yake kuthibitisha hali.
4. Thibitisha kupitia terminali:
   ```powershell
   docker info
   ```
   Ikiwa hii inachapisha taarifa za mfumo wa Docker (Version ya Server, Storage Driver, nk), Docker inafanya kazi.
5. **Maelezo maalum kwa Windows:** Ikiwa Docker bado haianzi:
   - Fungua Docker Desktop → **Settings** (ikoni ya gia) → **General**.
   - Hakikisha **Use the WSL 2 based engine** imeshawashwa.
   - Bonyeza **Apply & restart**.
   - Ikiwa WSL 2 haijawekwa, run `wsl --install` kwenye PowerShell iliyo na ruhusa za juu na anzisha upya kompyuta.
6. Jaribu tena upangaji.

### 2.2 Ujenzi wa Docker unashindwa na makosa ya utegemezi

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Marekebisho:**
1. Fungua `requirements.txt` na hakikisha majina ya vifurushi yameandikwa kwa usahihi.
2. Hakikisha mabadiliko ya toleo ni sahihi:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Jaribu usakinishaji eneo lako kwanza:
   ```bash
   pip install -r requirements.txt
   ```
4. Ikiwa unatumia rejista ya kifurushi binafsi, hakikisha Docker ina upatikanaji wa mtandao.

### 2.3 Usawa wa jukwaa la kontena (Apple Silicon)

Ikiwa unatekeleza kutoka Mac ya Apple Silicon (M1/M2/M3/M4), kontena lazima lijengwe kwa `linux/amd64` kwa sababu runtime ya kontena ya Foundry inatumia AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Amri ya deploy ya nyongeza ya Foundry hushughulikia hili moja kwa moja kawaida. Ikiwa unaona makosa yanayohusiana na usanifu, tengeneza kwa mkono ukitumia bendera ya `--platform` na wasiliana na timu ya Foundry.

---

## 3. Makosa ya uthibitishaji

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) inashindwa kupata tokeni

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Sababu kuu:** Hakuna chanzo cha uthibitisho kwenye mnyororo wa `DefaultAzureCredential` kinachomiliki tokeni halali.

**Marekebisho - jaribu kila hatua kwa mpangilio:**

1. **Ingia upya kupitia Azure CLI** (marekebisho ya kawaida):
   ```bash
   az login
   ```
   Dirisha la kivinjari linafunguka. Ingia, kisha rudi VS Code.

2. **Weka usajili sahihi:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Ikiwa huu sio usajili sahihi:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Ingia upya kupitia VS Code:**
   - Bonyeza ikoni ya **Accounts** (ikoni ya mtu) chini kushoto ya VS Code.
   - Bonyeza jina lako → **Sign Out**.
   - Bonyeza ikoni ya Accounts tena → **Sign in to Microsoft**.
   - Kamilisha taratibu za kuingia kwenye kivinjari.

4. **Service principal (hali za CI/CD pekee):**
   - Weka hizi mazingira ya mazingira kwenye `.env` yako:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Kisha anzisha upya mchakato wa wakala wako.

5. **Angalia cache ya tokeni:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Ikiwa hii inashindwa, tokeni yako ya CLI imeisha muda wake. Endesha tena `az login`.

### 3.2 Tokeni inafanya kazi kwa eneo lako lakini si kwenye upangaji wa mwenyeji

**Sababu kuu:** Wakala mwenyeji anatumia utambulisho unaosimamiwa na mfumo, tofauti na uthibitisho wako binafsi.

**Marekebisho:** Hili ni tabia inayotarajiwa - utambulisho unaosimamiwa hutolewa moja kwa moja wakati wa upangaji. Ikiwa wakala mwenyeji bado anapata makosa ya uthibitisho:
1. Thibitisha utambulisho unasimamiwa wa mradi wa Foundry una upatikanaji wa rasilimali ya Azure OpenAI.
2. Hakiki `PROJECT_ENDPOINT` ndani ya `agent.yaml` ni sahihi.

---

## 4. Makosa ya mfano (model)

### 4.1 Upangaji wa mfano haujapatikana

```
Error: Model deployment not found / The specified deployment does not exist
```

**Marekebisho - hatua kwa hatua:**

1. Fungua faili lako `.env` na kumbuka thamani ya `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Fungua pembeni la **Microsoft Foundry** ndani ya VS Code.
3. Panua mradi wako → **Model Deployments**.
4. Linganisha jina la upangaji lililoonyeshwa hapo na thamani yako ya `.env`.
5. Jina lina **kubwa na kidogo** husababisha tofauti - `gpt-4o` si sawa na `GPT-4o`.
6. Ikiwa hazilingani, sasisha `.env` kutumia jina halisi lililo kwenye pembeni.
7. Kwa upangaji wa mwenyeji, pia sasisha `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Mfano unajibu kwa maudhui yasiyotarajiwa

**Marekebisho:**
1. Pitia thibitisho la `EXECUTIVE_AGENT_INSTRUCTIONS` kwenye `main.py`. Hakikisha halijakata au kuharibika.
2. Angalia mpangilio wa joto la mfano (ikiwa unaweza kubadilika) - thamani za chini huleta matokeo ya uhakika zaidi.
3. Linganisha mfano uliotangazwa (mfano `gpt-4o` vs `gpt-4o-mini`) - mifano tofauti ina uwezo tofauti.

---

## 5. Makosa ya upangaji

### 5.1 Ruhusa ya kutoa ACR

```
Error: AcrPullUnauthorized
```

**Sababu kuu:** Utambulisho unasimamiwa wa mradi wa Foundry hauwezi kutoa picha ya kontena kutoka kwenye Azure Container Registry.

**Marekebisho - hatua kwa hatua:**

1. Fungua [https://portal.azure.com](https://portal.azure.com).
2. Tafuta **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** katika kisanduku cha juu cha utafutaji.
3. Bonyeza rejista inayohusiana na mradi wako wa Foundry (kawaida iko katika kundi la rasilimali moja).
4. Katika navugazi ya kushoto, bonyeza **Access control (IAM)**.
5. Bonyeza **+ Add** → **Add role assignment**.
6. Tafuta **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** na ichague. Bonyeza **Next**.
7. Chagua **Managed identity** → bonyeza **+ Select members**.
8. Tafuta na chagua utambulisho unasimamiwa wa mradi wa Foundry.
9. Bonyeza **Select** → **Review + assign** → **Review + assign**.

> Utoaji huu wa jukumu kawaida huwekwa moja kwa moja na nyongeza ya Foundry. Ikiwa unakutana na kosa hili, usanidi wa moja kwa moja unaweza kushindwa. Pia unaweza jaribu upangaji tena - nyongeza inaweza jaribu tena usanidi.

### 5.2 Wakala anashindwa kuanza baada ya upangaji

**Dalili:** Hali ya kontena inabaki "Pending" kwa zaidi ya dakika 5 au inaonyesha "Failed".

**Marekebisho - hatua kwa hatua:**

1. Fungua pembeni la **Microsoft Foundry** ndani ya VS Code.
2. Bonyeza wakala wako wa mwenyeji → chagua toleo.
3. Katika paneli ya maelezo, angalia **Container Details** → tafuta sehemu ya **Logs** au kiungo.
4. Soma majalada ya kuanzisha kontena. Sababu za kawaida:

| Ujumbe wa logi | Sababu | Marekebisho |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Utegemezi umepotea | Ongeza kwenye `requirements.txt` na upangie tena |
| `KeyError: 'PROJECT_ENDPOINT'` | Mazingira ya mazingira hayajawekwa | Ongeza env var kwenye `agent.yaml` chini ya `env:` |
| `OSError: [Errno 98] Address already in use` | Mgogoro wa bandari | Hakikisha `agent.yaml` ina `port: 8088` na mchakato mmoja tu unafanya bind |
| `ConnectionRefusedError` | Wakala hakuanza kusikiliza | Angalia `main.py` - simu ya `from_agent_framework()` lazima iendeshwe wakati wa kuanzisha |

5. Rekebisha tatizo, kisha upangie tena kutoka [Moduli 6](06-deploy-to-foundry.md).

### 5.3 Muda wa upangaji umeisha

**Marekebisho:**
1. Hakiki muunganisho wako wa intaneti - usukani wa Docker unaweza kuwa mkubwa (>100MB kwa upangaji wa kwanza).
2. Ikiwa uko nyuma ya wakala wa kampuni, hakikisha mipangilio ya wakala wa Docker Desktop imesanidiwa: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Jaribu tena - matatizo ya mtandao yanaweza kusababisha kushindwa kwa muda mfupi.

---

## 6. Marejeo ya haraka: majukumu ya RBAC

| Jukumu | Eneo la kawaida | Kinatoa Nini |
|------|---------------|----------------|
| **Azure AI User** | Mradi | Vitendo vya data: kujenga, upangilia, na kuitisha mawakala (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Mradi au Akaunti | Vitendo vya data + uundaji wa mradi |
| **Azure AI Owner** | Akaunti | Ufikiaji kamili + usimamizi wa uteuzi wa jukumu |
| **Azure AI Project Manager** | Mradi | Vitendo vya data + anaweza kutoa Azure AI User kwa wengine |
| **Contributor** | Usajili/ RG | Vitendo vya usimamizi (kuunda/kufuta rasilimali). **HAVIJUMUUSHA vitendo vya data** |
| **Owner** | Usajili/ RG | Vitendo vya usimamizi + uteuzi wa jukumu. **HAVIJUMUUSHA vitendo vya data** |
| **Reader** | Yoyote | Ufikiaji wa kusoma tu usimamizi |

> **Ufupi muhimu:** `Owner` na `Contributor` HAVIJUMUUSHI vitendo vya data. Daima unahitaji jukumu la `Azure AI *` kwa operesheni za wakala. Jukumu la chini kabisa kwa warsha hii ni **Azure AI User** kwenye **mradi**.

---

## 7. Orodha ya mchakato wa kumaliza warsha

Tumia hii kama uthibitisho wa mwisho kwamba umefanya kila kitu:

| # | Kitu | Moduli | Imepita? |
|---|------|--------|---|
| 1 | Misingi yote imewekwa na kuthibitishwa | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit na nyongeza za Foundry zimewekwa | [01](01-install-foundry-toolkit.md) | |
| 3 | Mradi wa Foundry umeundwa (au mradi uliopo umechaguliwa) | [02](02-create-foundry-project.md) | |
| 4 | Mfano umewekwa (mfano, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Nafasi ya Mtumiaji wa Azure AI imetolewa kwa kiwango cha mradi | [02](02-create-foundry-project.md) | |
| 6 | Mradi wa mawakala mwenyeji umeanzishwa (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` imewezeshwa na PROJECT_ENDPOINT na MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Maelekezo ya wakala yamebinafsishwa katika main.py | [04](04-configure-and-code.md) | |
| 9 | Mazingira pepe yameundwa na utegemezi umewekwa | [04](04-configure-and-code.md) | |
| 10 | Wakala amejaribiwa kwa ndani kwa F5 au terminali (vipimo 4 vya moshi vimefaulu) | [05](05-test-locally.md) | |
| 11 | Imewekwa kwenye Huduma ya Foundry Agent | [06](06-deploy-to-foundry.md) | |
| 12 | Hali ya kontena inaonyesha "Imeanzishwa" au "Inafanya kazi" | [06](06-deploy-to-foundry.md) | |
| 13 | Imethibitishwa kwenye VS Code Playground (vipimo 4 vya moshi vimefaulu) | [07](07-verify-in-playground.md) | |
| 14 | Imethibitishwa kwenye Foundry Portal Playground (vipimo 4 vya moshi vimefaulu) | [07](07-verify-in-playground.md) | |

> **Hongera!** Ikiwa vitu vyote vimehakikiwa, umemaliza warsha yote. Umejenga wakala mwenyeji kutoka mwanzo, kujaribu kwa ndani, kuuweka Microsoft Foundry, na kuuthibitisha katika uzalishaji.

---

**Iliyotangulia:** [07 - Thibitisha katika Playground](07-verify-in-playground.md) · **Nyumbani:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Maelezo ya Kukataa**:  
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mwakati tunajitahidi kwa usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upotovu. Hati ya asili katika lugha yake ya asili inapaswa kuzingatiwa kama chanzo halali. Kwa taarifa muhimu, inapendekezwa kupata tafsiri ya kisanii kutoka kwa mtafsiri wa binadamu. Hatubebwi na lawama kwa maelezo au tafsiri zisizo sahihi zitokanazo na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->