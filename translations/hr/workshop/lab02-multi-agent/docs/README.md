# Laboratorij 02 - Višestruki agenti: Procjena usklađenosti životopisa i posla

## Cijeli put učenja

Ova dokumentacija vodi vas kroz izradu, testiranje i implementaciju **višestrukog agenata sklopa zadataka** koji ocjenjuje usklađenost životopisa s poslom pomoću četiri specijalizirana agenta orkestrirana putem **WorkflowBuilder-a**.

> **Preduvjet:** Dovršite [Laboratorij 01 - Jedan agent](../../lab01-single-agent/README.md) prije početka Laboratorija 02.

---

## Moduli

| # | Modul | Što ćete raditi |
|---|--------|---------------|
| 0 | [Uvod](00-prerequisites.md) | Što ćete izgraditi, provjera Laboratorija 01, usporedba Laboratorija 02 i 01 |
| 1 | [Razumijevanje arhitekture višestrukih agenata](01-understand-multi-agent.md) | Učenje WorkflowBuilder-a, uloga agenata, orkestracijski graf |
| 2 | [Izgradnja projekta višestrukih agenata](02-scaffold-multi-agent.md) | Korištenje guiding wizards Foundry ekstenzije za izgradnju osnovnog projekta |
| 3 | [Konfiguracija agenata i okoline](03-configure-agents.md) | Pisanje uputa za 4 agenta, konfiguracija MCP alata, postavljanje varijabli okoline |
| 4 | [Orkestracijski obrasci](04-orchestration-patterns.md) | Sekvencijalni lanac, prijenos sadržaja i OR-semantika u WorkflowBuilder-u |
| 5 | [Lokalno testiranje](05-test-locally.md) | F5 debug s Agent Inspector, pokretanje osnovnih testova s životopisom + JD |
| 6 | [Implementacija u Foundry](06-deploy-to-foundry.md) | Izgradnja kontejnera, push u ACR, registracija hostiranog agenta |
| 7 | [Provjera na Playgroundu](07-verify-in-playground.md) | Testiranje implementiranog agenta u VS Code i Foundry Portal playgroundima |
| 8 | [Rješavanje problema](08-troubleshooting.md) | Popravak uobičajenih problema s višestrukim agentima (MCP pogreške, skraćeni izlaz, verzije paketa) |
| 9 | [Sažetak i sljedeći koraci](09-summary.md) | Što ste izgradili, ključni naučeni koncepti, čišćenje, i kamo dalje |

---

**Natrag na:** [Laboratorij 02 README](../README.md) · [Početak radionice](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Napomena**:
Ovaj dokument je preveden korištenjem AI prevoditeljskog servisa [Co-op Translator](https://github.com/Azure/co-op-translator). Iako težimo točnosti, imajte na umu da automatski prijevodi mogu sadržavati greške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za važne informacije preporuča se profesionalni ljudski prijevod. Nismo odgovorni za bilo kakva nesporazumevanja ili pogrešne interpretacije koje proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->