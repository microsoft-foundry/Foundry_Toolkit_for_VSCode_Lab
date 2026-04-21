# Lab 02 - Višeagentni tijek rada: Evaluator usklađenosti životopisa s poslom

## Cijeli put učenja

Ova dokumentacija vas vodi kroz izradu, testiranje i implementaciju **višeagentnog tijeka rada** koji procjenjuje usklađenost životopisa s poslom koristeći četiri specijalizirana agenta orkestrirana putem **WorkflowBuilder**.

> **Preduvjet:** Završi [Lab 01 - Jedan agent](../../lab01-single-agent/README.md) prije početka Laba 02.

---

## Moduli

| # | Modul | Što ćete raditi |
|---|--------|---------------|
| 0 | [Preduvjeti](00-prerequisites.md) | Provjeri završetak Laba 01, razumij koncept više agenata |
| 1 | [Razumijevanje višeagentne arhitekture](01-understand-multi-agent.md) | Nauči WorkflowBuilder, uloge agenata, graf orkestracije |
| 2 | [Postavljanje višeagentnog projekta](02-scaffold-multi-agent.md) | Koristi Foundry ekstenziju za postavljanje višeagentnog tijeka rada |
| 3 | [Konfiguriranje agenata i okoline](03-configure-agents.md) | Napiši upute za 4 agenta, konfiguriraj MCP alat, postavi varijable okoline |
| 4 | [Orkestracijski obrasci](04-orchestration-patterns.md) | Istraži paralelno grananje, sekvencijalno agregiranje i alternativne obrasce |
| 5 | [Testiranje lokalno](05-test-locally.md) | F5 debug s Agent Inspector, pokreni brze testove s životopisom + opisom posla |
| 6 | [Implementacija u Foundry](06-deploy-to-foundry.md) | Izradi kontejner, pushaj u ACR, registriraj hostani agent |
| 7 | [Provjera u Playgroundu](07-verify-in-playground.md) | Testiraj implementiranog agenta u VS Code i Foundry portal playgroundovima |
| 8 | [Rješavanje problema](08-troubleshooting.md) | Popravi uobičajene probleme s više agenti (MCP greške, skraćeni output, verzije paketa) |

---

## Procijenjeno vrijeme

| Razina iskustva | Vrijeme |
|-----------------|---------|
| Nedavno završen Lab 01 | 45-60 minuta |
| Neko iskustvo s Azure AI | 60-90 minuta |
| Prvi put s više agenti | 90-120 minuta |

---

## Arhitektura na prvi pogled

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

**Natrag na:** [Lab 02 README](../README.md) · [Početna stranica radionice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Odricanje od odgovornosti**:  
Ovaj dokument preveden je pomoću AI usluge za prijevod [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo osigurati točnost, imajte na umu da automatizirani prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na njegovom izvornom jeziku treba smatrati autoritativnim izvorom. Za kritične informacije preporučuje se profesionalni ljudski prijevod. Ne snosimo odgovornost za bilo kakva nesporazuma ili pogrešna tumačenja koja proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->