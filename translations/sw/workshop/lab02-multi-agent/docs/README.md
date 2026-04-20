# Maabara 02 - Mtiririko wa Kazi wa Wakala Wengi: Mkadirio wa Kuendana Kazi kwa Wasifu

## Njia Kamili ya Kujifunza

Nyaraka hii inakuongoza kujenga, kupima, na kuweka katika mazingira **mtiririko wa kazi wa wakala wengi** unaotathmini kuendana kwa wasifu na kazi kwa kutumia mawakala wanne maalum wanaoratibiwa kupitia **WorkflowBuilder**.

> **Sharti:** Kamilisha [Maabara 01 - Wakala Mmoja](../../lab01-single-agent/README.md) kabla ya kuanza Maabara 02.

---

## Moduli

| # | Moduli | Utakayofanya |
|---|--------|--------------|
| 0 | [Sharti za Awali](00-prerequisites.md) | Thibitisha ukamilifu wa Maabara 01, elewa dhana za wakala wengi |
| 1 | [Elewa Muundo wa Wakala Wengi](01-understand-multi-agent.md) | Jifunze WorkflowBuilder, majukumu ya wakala, mchoro wa uratibu |
| 2 | [Weka Msingi wa Mradi wa Wakala Wengi](02-scaffold-multi-agent.md) | Tumia ugani wa Foundry kuunda msingi wa mtiririko wa kazi wa wakala wengi |
| 3 | [Sakinisha Wakala & Mazingira](03-configure-agents.md) | Andika maagizo kwa mawakala 4, panga chombo cha MCP, weka mabadiliko ya mazingira |
| 4 | [Mifumo ya Uratibu](04-orchestration-patterns.md) | Chunguza ugawaji sambamba, mkusanyiko wa mfululizo, na mifumo mbadala |
| 5 | [Pima Kwenye Sehemu ya Mitaani](05-test-locally.md) | Tumia F5 debug na Agent Inspector, fanya majaribio ya harufu kwa wasifu + JD |
| 6 | [Weka Kwenye Foundry](06-deploy-to-foundry.md) | Tengeneza kontena, tuma kwenye ACR, jisajili wakala mwenyeji |
| 7 | [Thibitisha kwenye Playground](07-verify-in-playground.md) | Pima wakala uliofungwa kwenye VS Code na viwanja vya Foundry Portal |
| 8 | [Matatizo na Ufumbuzi](08-troubleshooting.md) | Rekebisha matatizo ya kawaida ya wakala wengi (makosa ya MCP, matokeo yaliyokatizwa, matoleo ya pakiti) |

---

## Muda unaokadiriwa

| Kiwango cha uzoefu | Muda |
|---------------------|------|
| Umehitimu Maabara 01 hivi karibuni | Dakika 45-60 |
| Uzoefu wa Azure AI kidogo | Dakika 60-90 |
| Mara ya kwanza na wakala wengi | Dakika 90-120 |

---

## Muundo kwa haraka

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Rudi kwa:** [Maabara 02 README](../README.md) · [Nyumbani kwa Warsha](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kielekezi cha Serikali**:  
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kwa usahihi, tafadhali fahamu kwamba tafsiri za moja kwa moja zinaweza kuwa na makosa au upungufu wa maana. Hati ya asili katika lugha yake ya asili inapaswa kuzingatiwa kama chanzo chenye mamlaka. Kwa taarifa muhimu, tafsiri ya kitaaluma inayofanywa na binadamu inashauriwa. Hatutawajibika kwa kutokuelewana au tofauti za tafsiri zinazotokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->