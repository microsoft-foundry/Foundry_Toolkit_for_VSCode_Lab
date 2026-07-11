# Laboratorinis darbas 02 - Daugiaprogramė darbo eiga: gyvenimo aprašymas → darbo atitikties vertintojas

## Pilnas mokymosi kelias

Ši dokumentacija žingsnis po žingsnio parodyta, kaip sukurti, testuoti ir diegti **daugiaprogramę darbo eigą**, kuri įvertina gyvenimo aprašymo ir darbo atitiktį, naudojant keturis specializuotus agentus, koordinuojamus per **WorkflowBuilder**.

> **Reikalavimas:** Prieš pradedant atlikti Laboratorinį darbą 02, įvykdykite [Laboratorinį darbą 01 - Vienas agentas](../../lab01-single-agent/README.md).

---

## Skyriai

| # | Skyrius | Ką atliksite |
|---|--------|--------------|
| 0 | [Įvadas](00-prerequisites.md) | Ką kursite, Laboratorinio darbo 01 patikrinimas, Laboratorinis darbas 02 prie Laboratorinio darbo 01 palyginimas |
| 1 | [Suprasti daugiaprogramę architektūrą](01-understand-multi-agent.md) | Mokysitės WorkflowBuilder, agentų vaidmenų, koordinavimo grafą |
| 2 | [Paruošti daugiaprogramį projektą](02-scaffold-multi-agent.md) | Naudokite Foundry plėtinio vedlį bazinio projekto parengimui |
| 3 | [Konfigūruoti agentus ir aplinką](03-configure-agents.md) | Parašykite nurodymus 4 agentams, konfigūruokite MCP įrankį, nustatykite aplinkos kintamuosius |
| 4 | [Koordinavimo šablonai](04-orchestration-patterns.md) | Sekos grandinė, turinio perdavimas, ir WorkflowBuilder ARBA semantika |
| 5 | [Testuoti lokaliai](05-test-locally.md) | F5 derinimas su Agent Inspector, atlikite pirminių testų su gyvenimo aprašymu + darbo aprašymu |
| 6 | [Diegti į Foundry](06-deploy-to-foundry.md) | Sukurkite konteinerį, įkelkite į ACR, užregistruokite talpinamą agentą |
| 7 | [Patvirtinti Playground aplinkoje](07-verify-in-playground.md) | Testuokite įdiegta agentą VS Code ir Foundry portalo žaidimų aplinkose |
| 8 | [Trikčių šalinimas](08-troubleshooting.md) | Ištaisykite dažnas daugiaprogramių problemų priežastis (MCP klaidos, truputis išvesties, paketo versijos) |
| 9 | [Santrauka ir kiti žingsniai](09-summary.md) | Ką sukūrėte, pagrindinės sąvokos, valymas ir kur toliau eiti |

---

**Atgal į:** [Laboratorinio darbo 02 README](../README.md) · [Dirbtuvių pradžia](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->