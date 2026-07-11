# Moduli 7 - Thibitisha kwenye Playground

⏱️ ~dakika 10

Katika moduli hii, unajaribu mtiririko wako wa kazi wa mawakala wengi uliowekwa katika VS Code na Portal ya Foundry, ukihakikisha wakala anafanya kazi sawa na majaribio ya ndani.

---

## Kwa nini ujifunze tena baada ya kuweka kazi?

Mazingira yaliohifadhiwa yanatofautiana na ya ndani kwa njia kadhaa muhimu:

| | Ndani | Imehifadhiwa |
|--|-------|--------|
| **Utambulisho** | Kuingia kwa kibinafsi (`DefaultAzureCredential`) | Utambulisho wa kila wakala wa Entra uliopewa (huhakikisha kiotomatiki wakati wa kuweka kazi) |
| **Kituo** | `http://localhost:8088/responses` | Anuani ya huduma ya Foundry Agent inasimamiwa |
| **Mtandao** | Mashine yako → Azure OpenAI + MCP | Mgongo wa Azure (muda mdogo wa kuchelewa) |

Kigezo kibaya kilichopangwa vibaya, tatizo la RBAC, au simu ya MCP ya kutoka iliyozuiwa itaonekana hapa kwanza.

---

## Chaguo A: Jaribu katika VS Code Playground (inapendekezwa kwanza)

### Hatua 1: Elekea kwa wakala wako aliyehifadhiwa

1. Bonyeza ikoni ya **Foundry Toolkit** katika Ukuta wa Shughuli.
2. Panua mradi wako → **Wakala Waliowekwa (Mapitio)** → tafuta wakala wako.

![Upau wa Foundry Toolkit ukionyesha Wakala Waliowekwa (Mapitio) na resume-job-fit-evaluator na matoleo yake yaliyowekwa](../../../../../translated_images/sw/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Hatua 2: Chagua toleo

1. Bonyeza wakala ili kupanua matoleo yake.
2. Bonyeza `v1` → thibitisha kuwa hali ni **hai** (upau wa pembeni unaweza kuonyesha "Inakwenda" au "Imesababishwa" - vyote vinaonyesha hali sawa ya tayari).

### Hatua 3: Fungua Playground

1. Bonyeza **Playground** (au bonyeza kulia toleo → **Fungua Playground**).
2. Dirisha la mazungumzo linafunguka kwenye kichupo cha VS Code.

### Hatua 4: Endesha majaribio ya awali

Tumia majaribio 3 yale yale kutoka [Moduli 5](05-test-locally.md). Andika kila ujumbe kwenye kisanduku cha ingizo cha Playground na bonyeza **Tuma** (au **Enter**).

#### Jaribio 1 - Wasifu kamili + JD (mtiririko wa kawaida)

Bandika maelekezo ya wasifu kamili + JD kutoka Moduli 5, Jaribio 1 (Jane Doe + Mhandisi Mwandamizi wa Wingu katika Contoso Ltd).

**Inayotarajiwa:**
- Alama ya kuendana na hesabu ya mgawanyo (kipimo cha alama 100)
- Sehemu ya Ujuzi Uliolingana
- Sehemu ya Ujuzi Uliokosekana
- **Kadi moja ya pengo kwa ujuzi uliokosekana kila mmoja** na viungo vya Microsoft Learn
- Ramani ya kujifunza na mfululizo wa muda

#### Jaribio 2 - Jaribio fupi la haraka (kiingilio kidogo)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Inayotarajiwa:**
- Alama ya kuendana ya chini (< 40)
- Tathmini ya uaminifu na njia ya kujifunza ya hatua kwa hatua
- Kadi nyingi za pengo (AWS, Kubernetes, Terraform, CI/CD, pengo la uzoefu)

#### Jaribio 3 - Mgombea mwenye uendano mkubwa

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Inayotarajiwa:**
- Alama ya kuendana juu (≥ 80)
- Kuzingatia maandalizi ya mahojiano na kusafisha
- Kadi chache au hakuna kadi za pengo
- Mfululizo mfupi unaolenga maandalizi

### Hatua 5: Linganisha na matokeo ya ndani

Fungua maelezo yako au kichupo cha kivinjari kutoka Moduli 5 ambapo ulihifadhi majibu ya ndani. Kwa kila jaribio:

- Je, jibu lina **muundo uleule** (alama ya kuendana, kadi za pengo, ramani)?
- Je, linazingatia **kigezo sawa cha alama** (mgawanyo wa alama 100)?
- Je, **viungo vya Microsoft Learn** bado vipo katika kadi za pengo?
- Je, kuna **kadi moja ya pengo kwa ujuzi uliokosekana kila mmoja** (haijaondolewa)?

> **Tofauti ndogo za maneno ni za kawaida** - mfano sio lazima ufanye matokeo sawa kila mara. Lenga muundo, uthabiti wa alama, na matumizi ya zana za MCP.

---

## Chaguo B: Jaribu kwenye Portal ya Foundry

[Portal ya Foundry](https://ai.azure.com) hutoa playground ya mtandao inayofaa kwa kushiriki na wenzako au washiriki wa mradi.

### Hatua 1: Fungua Portal ya Foundry

1. Fungua kivinjari chako na nenda [https://ai.azure.com](https://ai.azure.com).
2. Ingia kwa akaunti ile ile ya Azure ulicha kutumia wakati wote wa warsha.

### Hatua 2: Elekea kwenye mradi wako

1. Kwenye ukurasa wa nyumbani, angalia **Miradi ya Hivi Karibuni** kwenye upau wa pembeni wa kushoto.
2. Bonyeza jina la mradi wako (mfano, `workshop-agents`).
3. Ikiwa huitaona, bonyeza **Miradi yote** na utafute.

### Hatua 3: Tafuta wakala aliyewekwa

1. Kwenye upau wa urambazaji wa mradi upande wa kushoto, bonyeza **Jenga** → **Wakala** (au tafuta sehemu ya **Wakala**).
2. Unapaswa kuona orodha ya mawakala. Tafuta wakala wako aliyewekwa (mfano, `resume-job-fit-evaluator`).
3. Bonyeza jina la wakala kufungua ukurasa wa maelezo yake.

### Hatua 4: Fungua Playground

1. Kwenye ukurasa wa maelezo ya wakala, angalia bar ya zana ya juu.
2. Bonyeza **Fungua playground** (au **Jaribu katika playground**).
3. Kiolesura cha mazungumzo kinafunguka.

### Hatua 5: Endesha majaribio yale yale ya awali

Rudia majaribio yote 3 kutoka sehemu ya VS Code Playground hapo juu. Linganisha kila jibu na matokeo ya ndani (Moduli 5) na matokeo ya VS Code Playground (Chaguo A hapo juu).

---

## Uhakiki maalum wa wakala wengi

Mbali na usahihi wa msingi, hakikisha tabia hizi za wakala wengi zifuatwe:

### Utekelezaji wa zana ya MCP

| Angalia | Jinsi ya kuhakiki | Hali ya kupitisha |
|-------|---------------|----------------|
| Simu za MCP zinafanikiwa | Kadi za pengo zina URL za `learn.microsoft.com` | URL halisi, si ujumbe wa nafasi |
| Simu nyingi za MCP | Kila pengo la Kipaumbele Kuu/Kati lina rasilimali | Si kadi ya pengo ya kwanza tu |
| Msaada wa MCP unafanya kazi | Ikiwa URL hazipo, angalia maandishi ya msaada | Wakala bado anatengeneza kadi za pengo (ikiwa na au bila URL) |

### Uratibu wa wakala

| Angalia | Jinsi ya kuhakiki | Hali ya kupitisha |
|-------|---------------|----------------|
| Wakala wote 4 walikimbia | Matokeo yana alama ya kuendana NA kadi za pengo | Alama inatoka kwa MatchingAgent, kadi kutoka GapAnalyzer |
| Utekelezaji mfululizo | Muda wa jibu ni wa sababu (< dakika 2) | Ikiwa zaidi ya dakika 3, angalia makosa kwenye kumbukumbu ya terminal |
| Uadilifu wa mtiririko wa data | Kadi za pengo zinahusisha ujuzi kutoka ripoti ya kuendana | Hakuna ujuzi uliozuiliwa usiokuwepo katika JD |

---

## Vipimo vya uthibitishaji

Tumia vipimo hivi kutathmini tabia ya mtiririko wa mawakala wengi ulihifadhiwa:

| # | Vigezo | Hali ya kupitisha | Kupita? |
|---|----------|---------------|-------|
| 1 | **Usahihi wa utendaji** | Wakala hutoa majibu ya wasifu + JD na alama ya kufaa na uchambuzi wa pengo | |
| 2 | **Uthabiti wa alama** | Alama ya kufaa hutumia kipimo cha alama 100 pamoja na mgawanyo | |
| 3 | **Ukamilifu wa kadi za pengo** | Kadi moja kwa ujuzi uliokosekana (si iliyokatwa au kuunganishwa) | |
| 4 | **Uunganisho wa zana ya MCP** | Kadi za pengo zina URL halisi za Microsoft Learn | |
| 5 | **Uthabiti wa muundo** | Muundo wa matokeo unalingana kati ya majaribio ya ndani na yale yaliyowekwa | |
| 6 | **Muda wa jibu** | Wakala aliyohifadhiwa hutoa jibu ndani ya dakika 2 kwa tathmini kamili | |
| 7 | **Hakuna makosa** | Hakuna makosa ya HTTP 500, muda wa kusubiri kumalizika, au majibu tupu | |

> "Kupita" maana yake ni kwamba vigezo vyote 7 vimetimizwa kwa majaribio 3 yote katika angalau playground moja (VS Code au Portal).

---

## Kutatua matatizo ya playground

| Dalili | Sababu inayowezekana | Suluhisho |
|---------|-------------|-----|
| Playground haipaki | Kontena si katika hali ya `hai` | Rudi [Moduli 6](06-deploy-to-foundry.md), thibitisha hali ya kuweka. Subiri ikiwa `inaundwa` |
| Wakala hurejesha jibu tupu | Jina la kuweka mfano halilingani | Angalia `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` linalingana na mfano uliowekwa |
| Wakala hurejesha ujumbe wa kosa | [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ruhusa haipo | Weka **[Mtumiaji wa Foundry](https://aka.ms/foundry-ext-project-role)** (awali Mtumiaji wa Azure AI) kwa kiwango cha mradi |
| Hakuna URLs za Microsoft Learn katika kadi za pengo | MCP ya kutoka imezuiwa au seva ya MCP haipatikani | Angalia kama kontena linaweza kufikia `learn.microsoft.com`. Tazama [Moduli 8](08-troubleshooting.md) |
| Kadi moja ya pengo tu (katwa) | Maelekezo ya GapAnalyzer hayajumuishi sehemu ya "CRITICAL" | Pitia [Moduli 3, Hatua 2.4](03-configure-agents.md) |
| Alama ya kufaa ni tofauti sana na ile ya ndani | Mfano tofauti au maagizo yaliyowekwa | Linganisha env vars za `agent.yaml` na `.env` ya ndani. Weka upya ikiwa inahitajika |
| "Wakala haipatikani" katika Portal | Uwekaji bado unasambazwa au umefaulu | Subiri dakika 2, fanya upya ukurasa. Ikiwa bado haipo, weka upya kutoka [Moduli 6](06-deploy-to-foundry.md) |

---

### Kidhibiti cha hatua

- [ ] Nimejaribu wakala katika VS Code Playground - majaribio yote 3 ya awali yamefaulu
- [ ] Nimejaribu wakala katika [Portal ya Foundry](https://ai.azure.com) Playground - majaribio yote 3 ya awali yamefaulu
- [ ] Majibu yana muundo sawa na majaribio ya ndani (alama ya kufaa, kadi za pengo, ramani)
- [ ] URLs za Microsoft Learn zipo katika kadi za pengo (zintaumia za MCP zikipatikana katika mazingira yaliyo hifadhiwa)
- [ ] Kadi moja ya pengo kwa ujuzi uliokosekana (hakuna kukatwa)
- [ ] Hakuna makosa au muda wa kusubiri wakati wa majaribio
- [ ] Nimekamilisha vipimo vya uthibitishaji (vigezo 7 vyote vimepitwa)

---

**Iliyotangulia:** [06 - Weka Kwenye Foundry](06-deploy-to-foundry.md) · **Ifuatayo:** [08 - Kutatua matatizo →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->