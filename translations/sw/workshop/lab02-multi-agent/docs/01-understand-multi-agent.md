# Kifurushi cha 1 - Elewa Miundo

⏱️ ~5 dakika

Kabla ya kuandika msimbo wowote, hapa kuna muhtasari mfupi wa kile unachojenga na jinsi inavyofanya kazi.

---

## Kile unachojenga

Unaweke **wasifu** na **maelezo ya kazi**. Mchakato unarudisha:

- Alama ya ulinganifu (0–100 na mgawanyo)
- Orodha ya ucheleweshaji wa ujuzi na vyeti
- Ramani ya kujifunza iliyobinafsishwa na viungo vya Microsoft Learn kwa kila ucheleweshaji

---

## Wakala wanne

Wakala mmoja anajaribu kusoma, kupima, na kupanga yote mara moja huwa haraka na kutoa matokeo mepesi. Kugawanya kazi kwa wakala wanne maalum hutoa matokeo bora:

| Wakala | Kinachofanya |
|-------|-------------|
| **ResumeParser** | Husoma wasifu; hurekebisha maelezo ya kazi kama yalivyo katika `[JOB DESCRIPTION PASS-THROUGH]` kwa wakala wa baadaye |
| **JobDescriptionAgent** | Hutoa mahitaji ya maelezo ya kazi kutoka pass-through; husafirisha `[PARSED RESUME]` mbele kama `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | Hulinganisha sehemu zote zilizotambulishwa; hutengeneza alama ya ulinganifu ya 0–100 na orodha ya mapungufu |
| **GapAnalyzer** | Hutengeneza ramani ya kujifunza; hutafuta Microsoft Learn kwa kila pengo |

---

## Mchoro wa upangaji kazi

Mchakato ni **mfululizo wa hatua** - kila wakala hupitisha matokeo yake kwa wakala wa karibu:

```mermaid
flowchart LR
    A["Ingizo la Mtumiaji"] --> B["Chambua Wasifu"]
    B -- "wasifu uliopimwa + kuwasilisha JD" --> C["Wakala wa Maelezo ya Kazi"]
    C -- "mahitaji ya JD + kuwasilisha wasifu" --> D["Wakala wa Kulinganisha"]
    D -- "ripoti ya ulinganifu + mapungufu" --> E["Mchambuzi wa Mapungufu + MCP"]
    E --> F["Matokeo ya Mwisho"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** hupokea ingizo la mtumiaji, husoma wasifu, na kunakili maelezo ya kazi katika `[JOB DESCRIPTION PASS-THROUGH]`.
2. **JD Agent** hutenganisha mahitaji yaliyopangwa na husafirisha `[PARSED RESUME PASS-THROUGH]` mbele.
3. **MatchingAgent** hulinganisha sehemu zote mbili na hutengeneza alama ya ulinganifu na orodha ya mapungufu.
4. **GapAnalyzer** hutengeneza ramani ya kujifunza na kuitisha zana ya MCP ya Microsoft Learn kwa kila pengo.

---

## Jinsi hii inavyolingana na msimbo

Katika `main.py`, unaelezea mchoro huu kwa kutumia `WorkflowBuilder`:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # wakala wa kwanza kupokea maoni ya mtumiaji
        output_executors=[gap_executor],      # wakala wa mwisho - pato lake ni jibu
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → Wakala wa JD
    .add_edge(jd_executor, matching_executor)     # Wakala wa JD → Wakala wa Ulinganifu
    .add_edge(matching_executor, gap_executor)    # Wakala wa Ulinganifu → Mchambuzi wa Mapengo
    .build()
    .as_agent()
)
```

Kila `Agent` imefungwa ndani ya `AgentExecutor`. Mito ya `add_edge()` inaweka mfululizo muafaka - kila wakala hupokea tu matokeo ya mtangulizi wake wa moja kwa moja.

> `context_mode="last_agent"` inamaanisha kila mtendaji anaona tu matokeo ya mtangulizi wake wa moja kwa moja. ResumeParser na JD Agent hurejesha data mbele katika sehemu zenye lebo ili kila wakala wa chini awe na kile anachohitaji cha moja kwa moja.

---

## Zana ya MCP

GapAnalyzer ina zana moja: `search_microsoft_learn_for_plan`. Inajiunga na `https://learn.microsoft.com/api/mcp` na inarudisha viungo halisi vya Microsoft Learn kwa kila pengo la ujuzi.

Wakati zana inapoendesha utaona kumbukumbu hizi - zote zinatarajiwa:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

Usijali isipokuwa kama `POST` inarudisha kosa.

---

**Iliyopita:** [00 - Prerequisites](00-prerequisites.md) · **Inayofuata:** [02 - Scaffold the Project →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->