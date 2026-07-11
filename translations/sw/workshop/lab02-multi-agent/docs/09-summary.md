# Moduli 9 - Muhtasari & Hatua Zinazo Fuata

⏱️ ~5 min

**Hongera!** Umetengeneza, kujaribu, na (ikiwa uko Kwenye Njia A) kupeleka mchakato wa kazi wa mawakala wengi ukitumia Microsoft Foundry na Foundry Toolkit kwa VS Code.

---

## Uliujenga Nini

**Mchingatisho wa Kazi → Mkaguzi wa Kufaa Kazi** - mchakato wa kazi wa mawakala wengi uliowekwa mwenyeji unaofanya yafuatayo:
- Unapokea mchingatisho wa kazi + maelezo ya kazi kupitia HTTP (`POST /responses`)
- Unasimamia mawakala wanne maalum katika mfululizo wa mchakato - kila wakala hupitisha data ambayo mfuatiliaji wake anahitaji
- Unarudisha alama ya ufaa (0–100 pamoja na muhtasari), orodha ya mapungufu ya ujuzi na vyeti, na ramani ya kujifunza binafsi yenye viungo rasmi vya Microsoft Learn kwa kila upungufu
- Unaita seva ya Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) kuvutia rasilimali rasmi za kujifunza kwa kila upungufu wa ujuzi uliotambuliwa
- Unafanya kazi kama wakala mmoja aliyefungashwa mwenyeji katika Huduma ya Wakala ya Microsoft Foundry

---

## Misingi Mikuu Uliyojifunza

| Dhana | Uliyofanya Mazoezi |
|---------|-------------------|
| **Usimamizi wa mawakala wengi** | `WorkflowBuilder` mlolongo wa mchakato na `add_edge()` |
| **Utaalam wa wakala** | Mawakala wanne waliolengwa wanafanya kazi vizuri zaidi kuliko wakala mmoja wa ujumla |
| **Mfumo wa Mpangaji wa Yaliyomo** | ResumeParser inahudumu pia kama mpangaji - huhifadhi maandishi ya JD katika sehemu ya `[JOB DESCRIPTION PASS-THROUGH]` ili mawakala waliopo chini waweze kuyapata (hii ni muhimu kwa sababu `context_mode="last_agent"` inamaanisha mtekelezaji wa mwanzoni ndiye anayeona ujumbe wa mtumiaji wa asili pekee) |
| **Mfumo wa Uwasilishaji Yaliyomo** | Wakala wa JD hutuma mbele `[PARSED RESUME PASS-THROUGH]` ili MatchingAgent apate maelezo yote mawili; inazuia kuchochea mara mbili kutokana na semantiki ya OR kwenye michoro ya kuingiza wingi |
| **Uingizaji wa zana ya MCP** | `@tool` + `streamable_http_client` kuwasiliana na seva ya MCP ya nje |
| **Mzunguko wa maisha wa Wakala mwenyeji** | Anza → Sanidi → Jaribu kwa ndani → Peleka → Thibitisha katika wingu |
| **`context_mode="last_agent"`** | Kila mtekelezaji anaona tu matokeo ya mfuatiliaji wake wa moja kwa moja |
| **Mchakato wa kazi wa Foundry Toolkit** | Mhandisi wa skripti, Mchakaguzi wa Wakala, Muwakilishi wa Mchakato, uenezaji kwa kitufe kimoja |

---

## Ulikamilisha Nini

<details open>
<summary><strong>🅰️ Njia A - Usajili wa Foundry</strong></summary>

- [x] Umehakiki usanidi wa maabara 01: mradi, mfano, na RBAC bado vinafanya kazi
- [x] Umetengeneza mradi wa wakala wengi ukitumia kiolezo cha Workflows
- [x] Umeandika seti nne za maagizo za wakala (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Umeunganisha zana ya Microsoft Learn MCP na `streamable_http_client`
- [x] Umetunga mchoro wa mchakato wa kazi ukitumia `WorkflowBuilder` (mlolongo wa mchakato na usambazaji wa yaliyomo)
- [x] Umejaribu kwa ndani na majaribio 3 ya thamani (Mchakaguzi wa Wakala) - alama ya ufaa, kadi za mapungufu, na viungo vya MCP
- [x] Umepeleka kwenye Huduma ya Wakala ya Foundry (imefungashwa, kitambulisho kilichosimamiwa)
- [x] Umehakiki matokeo kwenye uwanja wa majaribio wa wingu - ulinganifu wa muundo na matokeo ya ndani

</details>

<details open>
<summary><strong>🅱️ Njia B - Foundry Lokali</strong></summary>

- [x] Umehakiki usanidi wa maabara 01: Foundry Lokali inafanya kazi na mfano wa ndani
- [x] Umetengeneza mradi wa wakala wengi ukitumia kiolezo cha Workflows
- [x] Umeandika seti nne za maagizo za wakala na kutengeneza mchoro wa mchakato wa kazi
- [x] Umeunganisha zana ya Microsoft Learn MCP
- [x] Umejaribu kwa ndani na majaribio 3 ya thamani
- [x] Umehakiki tabia ya wakala wengi bila hitaji la rasilimali za wingu

</details>

---

## Hatua Zinazo Fuata

### Endelea kujifunza

| Rasilimali | Maelezo |
|----------|-------------|
| **[Rejea SDK ya Agent Framework](https://learn.microsoft.com/agent-framework/)** | Hati za API za `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalogi ya zana za MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Unganisha mawakala na seva nyingine za MCP (Bing, GitHub, maalum) |
| **[Ongeza ujuzi (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Weka mawakala kwa hati, maduka ya vector, au utafutaji wa Bing |
| **[Tathmini za Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Pima ubora wa wakala kwa kiwango kikubwa kwa kutumia wataalam wa kiotomatiki |
| **[Hati za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Marejeo kamili ya jukwaa |
| **[Foundry Toolkit - Mabadiliko mapya](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Taarifa za toleo la nyongeza na historia ya mabadiliko |

### Mawazo ya kupanua mchakato huu

- **Ongeza wakala wa tano** - Kocha wa mahojiano anayetoa maswali yanayoweza kuulizwa kulingana na ripoti ya mapungufu
- **Ongeza zana ya kutilia msingi Bing** - Weka Wakala wa JD atafute matangazo ya kazi yanayofanana kuongeza mahitaji
- **Unganisha na hifadhidata ya mchingatisho** - Vuta wasifu wa wagombea kutoka hifadhidata kupitia `@tool` maalum
- **Jaribu mifano tofauti** - Linganisha ubora na ucheleweshaji wa `gpt-4.1` dhidi ya `gpt-4.1-mini`
- **Tathmini na Foundry** - Tumia kipengele cha Tathmini kupima ripoti za ufaa dhidi ya seti ya dhahabu

### Kwa watumiaji wa Njia B: Sasa boresha kwenye uenezaji wa wingu

Unapokuwa tayari kupeleka kwenye wingu:
1. Pata usajili wa Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Kamilisha [Maabara 01, Moduli 01](../../lab01-single-agent/docs/01-setup.md) (tengeneza mradi, peleka mfano, tumia RBAC)
3. Sasisha `.env` yako na kiungo cha mradi wa Foundry na jina la uenezaji wa mfano
4. Endelea kutoka [Moduli 06 - Peleka kwenye Foundry](06-deploy-to-foundry.md)

---

## Safisha rasilimali (hiari)

Ikiwa unataka kuondoa rasilimali za Azure zilizoanzishwa wakati wa warsha hii:

### Chaguo 1: Futa kikundi cha rasilimali (huondoa kila kitu)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Chaguo 2: Futa wakala mwenyeji tu

1. Fungua [ai.azure.com](https://ai.azure.com) → mradi wako → **Build** → **Agents**.
2. Tafuta **PersonalCareerCopilot** → bofya **Delete**.

### Chaguo 3: Futa uenezaji wa mfano

1. Katika menyu ya pembeni ya Foundry, panua mradi wako → **Models**.
2. Bofya kulia uenezaji wa mfano → **Delete**.

> **Kumbuka gharama:** Mawakala waliowekwa mwenyeji huleta gharama tu wakati wanapofanya kazi. Ukizuia au kufuta wakala, hakuna malipo yanayoendelea. Uenezaji wa mfano unaweza kuleta gharama ndogo ya uwezo ulihifadhiwa - ufute ikiwa umeisha kutumia.

---

**Iliyopita:** [08 - Matatizo na Ufumbuzi](08-troubleshooting.md) · **Nyumbani:** [Lab 02 README](../README.md) · [Nyumbani Warsha](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->