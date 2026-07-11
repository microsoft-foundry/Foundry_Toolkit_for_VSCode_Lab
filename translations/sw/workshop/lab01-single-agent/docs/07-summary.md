# Moduli 7 - Muhtasari & Hatua Zinazo Fuata

⏱️ ~5 dakika

**Hongera!** Umejenga, kujaribu, na (ikiwa upo Njia A) kuweka wakala wa AI mwenyeji kwa kutumia Microsoft Foundry na Foundry Toolkit kwa VS Code.

---

## Umejenga nini

Wakala wa **"Eleza Kama Mimi Ni Mtendaji Mkubwa"** ambaye:
- Anapokea ripoti za kiufundi za matukio au masasisho ya uendeshaji kupitia HTTP (`POST /responses`)
- Anatafsiri kwa muhtasari rahisi wa mtendaji
- Anafuata muundo uliopangwa wa matokeo (Kilichotokea / Athari za biashara / Hatua inayofuata)
- Anakataa maombi yasiyo ya mada na jaribio la kuchanganya maelekezo
- Anaendesha kama wakala mwenyeji katika chombo cha kontena cha Microsoft Foundry Agent Service

---

## Dhana kuu ulizojifunza

| Dhana | Ulizofanya mazoezi |
|---------|-------------------|
| **Miundo ya Msingi ya Agent Framework** | Mmoja wa `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Mzunguko wa maisha wa Wakala Mwenyeji** | Kuunda muundo → Kusanidi → Kuanzisha mtandaoni → Kuweka huduma → Kuangalia kwenye wingu |
| **Uhandisi wa prompt ya mfumo** | Nafasi, wasikilizaji, muundo wa matokeo, sheria, vikwazo vya usalama, na mifano |
| **Tofauti kati ya eneo la ndani na mwenyeji** | Utambulisho (cheti binafsi vs utambulisho ulioendeshwa), kiungo cha huduma, njia ya mtandao |
| **Mipaka ya usalama** | Kinga dhidi ya uchanganyaji wa maelekezo, kufuata nafasi, kushughulikia hali maalum kwa unyenyekevu |
| **Mtiririko wa kazi wa Foundry Toolkit** | Kuanzisha mradi, kuweka mfano, kuunda wakala, Mchunguzi wa Wakala, kuweka huduma kwa bonyeza moja |

---

## Ulimaliza nini

### Njia A (Usajili wa Foundry)

- [x] Umeanzisha Foundry Toolkit na kuunda mradi wa Foundry uliowekwa mfano
- [x] Umeunda wakala mwenyeji kwa muundo wa mradi uliotengenezwa moja kwa moja
- [x] Umeandika maelekezo ya wakala yenye muundo na sheria za usalama
- [x] Umejaribu mtandaoni kwa matukio 3 ya kazi (Mchunguzi wa Wakala)
- [x] Umeweka huduma kwenye Foundry Agent Service (katika kontena)
- [x] Umehakiki katika uwanja wa majaribio wa wingu kwa vipimo 4 vya usalama na hali maalum

### Njia B (Foundry Local)

- [x] Umeanzisha Foundry Toolkit na kiungo cha mfano cha eneo la ndani
- [x] Umeunda mradi wa wakala mwenyeji
- [x] Umeandika maelekezo ya wakala yenye muundo na sheria za usalama
- [x] Umejaribu mtandaoni kwa matukio 3 ya kazi
- [x] Umehifadhi tabia ya wakala bila hitaji la rasilimali za wingu

---

## Hatua zinazofuata

### Endelea kujifunza

| Rasilimali | Maelezo |
|----------|-------------|
| **[Lab 02 - Usanidi wa Wakala Wengi](../../lab02-multi-agent/docs/README.md)** | Jenga mtiririko wa wakala 4 (Resume → Mtathmini Ulinganifu wa Kazi) ukitumia mifumo ya usanidi |
| **[Ongeza zana kwa wakala wako](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Unganisha API, hifadhidata, au kazi za kawaida kupitia Katalogi ya Zana |
| **[Ongeza maarifa (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Weka wakala wako kwa hati, hifadhi za vector, au utafutaji wa Bing |
| **[Nyaraka za Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Rejea kamili ya jukwaa |
| **[Rejea SDK ya Agent Framework](https://learn.microsoft.com/agent-framework/)** | Nyaraka za API za kifurushi `agent-framework` |
| **[Foundry Toolkit - Nini Kipya](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Taarifa za kutolewa kwa nyongeza na mabadiliko |

### Mawazo ya kuongeza wakala wako

- **Ongeza zana ya tarehe** - Ruhusu wakala kujumuisha muktadha wa "hadi leo" katika muhtasari
- **Unganisha na hifadhidata ya matukio** - Pata maelezo halisi ya matukio kupitia kazi ya zana
- **Ongeza zana ya kutegemea Bing** - Ruhusu wakala kutafuta habari mpya kwa muktadha zaidi
- **Jaribu miundo tofauti** - Linganisha ubora wa matokeo ya `gpt-4.1` dhidi ya `gpt-4.1-mini`
- **Tathmini na Foundry** - Tumia kipengele cha Tathmini kupima ubora wa wakala kwa kiwango kikubwa

### Kwa watumiaji wa Njia B: Sasisha kwa uwekaji wingu

Ukijiandaa kuweka huduma kwenye wingu:
1. Pata usajili wa Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Kamilisha [Moduli 01, Usanidi](01-setup.md#step-2-set-up-based-on-your-access) (unda mradi, weka mfano, toa RBAC)
3. Sasisha `.env` yako na kiungo cha mradi wa Foundry na jina la kuweka mfano
4. Endelea kutoka [Moduli 05 - Weka kwenye Foundry](05-deploy-to-foundry.md)

---

## Safisha rasilimali (hiari)

Ikiwa unataka kuondoa rasilimali za Azure zilizoundwa wakati wa warsha hii:

### Chaguo 1: Futa kundi la rasilimali (huondoa kila kitu)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Chaguo 2: Futa wakala mwenyeji pekee

1. Fungua [ai.azure.com](https://ai.azure.com) → mradi wako → **Build** → **Agents**.
2. Bonyeza wakala wako → bonyeza **Delete**.

### Chaguo 3: Futa kuweka mfano

1. Kwenye pembeni ya Foundry, panua mradi wako → **Models**.
2. Bonyeza kulia kuweka mfano → **Delete**.

> **Kumbuka gharama:** Wakala wenyeji hushusha gharama tu wanapokuwa wakifanya kazi. Ikiwa unasitisha au kufuta wakala, haina gharama ya kuendelea. Kuweka mfano kunaweza kusababisha gharama ndogo kwa uwezo ulihifadhiwa - futa ikiwa umemaliza.

---

**Iliyotangulia:** [06 - Hakiki kwenye Uwanja wa Mchezo](06-verify-in-playground.md) · **Inayofuata:** [08 - Kutatua Matatizo (Rejea) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->