# Modulis 1 - Suprasti architektūrą

⏱️ ~5 min

Prieš rašant bet kokį kodą, štai trumpas apžvalga, ką kuriate ir kaip tai veikia.

---

## Ką kuriate

Jūs įklijuojate **gyvenimo aprašymą** ir **darbo aprašymą**. Darbo eiga gražina:

- Atitikties balą (0–100 su suskaidymu)
- Įgūdžių ir sertifikatų spragų sąrašą
- Asmeninę mokymosi programą su Microsoft Learn nuorodomis kiekvienai spragai

---

## Keturi agentai

Vienas agentas, bandantis iškart išanalizuoti, įvertinti ir suplanuoti, dažnai skuba ir pateikia paviršutinišką rezultatą. Darbas yra padalinamas keturiems specializuotiems agentams, kurie pasiekia geresnius rezultatus:

| Agentas | Ką jis daro |
|---------|-------------|
| **ResumeParser** | Analizuoja gyvenimo aprašymą; kopijuoja darbo aprašymą žodžiu į `[JOB DESCRIPTION PASS-THROUGH]` tolimesniems agentams |
| **JobDescriptionAgent** | Išskiria darbo aprašymo reikalavimus iš perdavimo; perduoda `[PARSED RESUME]` kaip `[PARSED RESUME PASS-THROUGH]` |
| **MatchingAgent** | Palygina abi paženklintas dalis; paskaičiuoja 0–100 atitikties balą ir spragų sąrašą |
| **GapAnalyzer** | Sudaro mokymosi planą; ieško Microsoft Learn kiekvienai spragai |

---

## Orkestracijos grafikas

Darbo eiga yra **vienas po kito einantis kanalas** – kiekvienas agentas perduoda savo rezultatą kitam:

```mermaid
flowchart LR
    A["Vartotojo įvestis"] --> B["Gyvenimo aprašymo analizatorius"]
    B -- "išanalizuotas CV + DA perdavimas" --> C["Darbo aprašymo agentas"]
    C -- "DA reikalavimai + CV perdavimas" --> D["Atitikties agentas"]
    D -- "tinkamumo ataskaita + spragos" --> E["Spragų analizatorius + MCP"]
    E --> F["Galutinis rezultatas"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** gauna vartotojo įvestį, analizuoja gyvenimo aprašymą ir kopijuoja darbo aprašymą į `[JOB DESCRIPTION PASS-THROUGH]`.
2. **JD Agent** išskiria struktūrizuotus reikalavimus ir perduoda `[PARSED RESUME PASS-THROUGH]` toliau.
3. **MatchingAgent** palygina abi dalis ir pateikia atitikties balą bei spragų sąrašą.
4. **GapAnalyzer** sudaro planą ir kiekvienai spragai kviečia Microsoft Learn MCP įrankį.

---

## Kaip tai pritaikoma kode

Faile `main.py` aprašote šį grafiką naudodami `WorkflowBuilder`:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # pirmasis agentas, gaunantis vartotojo įvestį
        output_executors=[gap_executor],      # paskutinis agentas - jo išvestis yra atsakymas
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JD agentas
    .add_edge(jd_executor, matching_executor)     # JD agentas → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

Kiekvienas `Agent` yra suvyniotas į `AgentExecutor`. `add_edge()` kvietimai apibrėžia griežtai sekantį kanalo srautą – kiekvienas agentas gauna tik savo tiesioginio pirmtako rezultatą.

> `context_mode="last_agent"` reiškia, kad kiekvienas vykdytojas mato tik savo tiesioginio pirmtako rezultatą. ResumeParser ir JD Agent perduoda duomenis toliau su žymėtais sekcijų pavadinimais, kad kiti agentai tiksliai gautų tai, ko jiems reikia.

---

## MCP įrankis

GapAnalyzer turi vieną įrankį: `search_microsoft_learn_for_plan`. Jis jungiasi prie `https://learn.microsoft.com/api/mcp` ir grąžina tikras Microsoft Learn nuorodas kiekvienai įgūdžių spragai.

Kai įrankis veikia, matysite šiuos žurnalus – visi jie yra tikėtini:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

Nerimaukite tik jei `POST` užklausa grąžina klaidą.

---

**Ankstesnis:** [00 - Prerequisites](00-prerequisites.md) · **Kitas:** [02 - Scaffold the Project →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->