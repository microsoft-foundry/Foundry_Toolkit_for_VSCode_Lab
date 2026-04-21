# 2 laboratorinis darbas - Daugelio agentų darbo eiga: gyvenimo aprašymas → darbo atitikimo vertintojas

## Pilnas mokymosi kelias

Ši dokumentacija padės jums sukurti, išbandyti ir įdiegti **daugelio agentų darbo eigą**, kuri įvertina gyvenimo aprašymo ir darbo tinkamumą, naudojant keturis specializuotus agentus, kuriuos valdo **WorkflowBuilder**.

> **Prieš tai būtina:** baigti [1 laboratorinį darbą - Vienas agentas](../../lab01-single-agent/README.md) prieš pradedant 2 laboratorinį darbą.

---

## Moduliai

| # | Modulis | Ką darysite |
|---|---------|-------------|
| 0 | [Priešistorė](00-prerequisites.md) | Patikrinti 1 laboratorinio darbo užbaigimą, suprasti daugelio agentų sąvokas |
| 1 | [Suprasti daugelio agentų architektūrą](01-understand-multi-agent.md) | Susipažinti su WorkflowBuilder, agentų vaidmenimis, orkestracijos grafiku |
| 2 | [Sukurti daugelio agentų projektą](02-scaffold-multi-agent.md) | Naudoti Foundry plėtinį, kad būtų paruošta daugelio agentų darbo eiga |
| 3 | [Konfigūruoti agentus ir aplinką](03-configure-agents.md) | Parašyti instrukcijas keturiems agentams, sukonfigūruoti MCP įrankį, nustatyti aplinkos kintamuosius |
| 4 | [Orkestracijos modeliai](04-orchestration-patterns.md) | Išnagrinėti lygiagretų paskirstymą, sekančią agregaciją ir alternatyvius modelius |
| 5 | [Testuoti vietoje](05-test-locally.md) | F5 derinimas su Agent Inspector, paleisti greitus testus su gyvenimo aprašymu ir darbo aprašymu (JD) |
| 6 | [Diegti į Foundry](06-deploy-to-foundry.md) | Sukurti konteinerį, įkelti į ACR, užregistruoti valdomą agentą |
| 7 | [Patikrinti Playground aplinkoje](07-verify-in-playground.md) | Testuoti įdiegtą agentą VS Code ir Foundry portalo žaidimų aikštelėse |
| 8 | [Trikčių šalinimas](08-troubleshooting.md) | Išspręsti dažnas daugelio agentų problemas (MCP klaidos, sutrumpintas rezultatas, paketų versijos) |

---

## Numatomos trukmės

| Patirties lygis | Laikas |
|-----------------|---------|
| Neseniai baigė 1 laboratorinį darbą | 45-60 minučių |
| Šiek tiek patirties su Azure AI | 60-90 minučių |
| Pirmą kartą su daugelio agentų sistema | 90-120 minučių |

---

## Architektūra apžvalga

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

**Atgal į:** [2 laboratorinio darbo README](../README.md) · [Dirbtuvių pradžia](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:  
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, atkreipkite dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojame profesionalų žmogaus vertimą. Mes neatsakome už bet kokius nesusipratimus ar neteisingą interpretaciją, kilusią dėl šio vertimo naudojimo.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->