# Laborator 02 - Flux de lucru multi-agent: Evaluator potrivire CV → job

## Calea completă de învățare

Această documentație te ghidează pas cu pas în construirea, testarea și implementarea unui **flux de lucru multi-agent** care evaluează potrivirea CV-ului cu jobul folosind patru agenți specializați orchestrați prin **WorkflowBuilder**.

> **Precondiție:** Finalizează [Laboratorul 01 - Agent unic](../../lab01-single-agent/README.md) înainte de a începe Laboratorul 02.

---

## Module

| # | Modul | Ce vei face |
|---|--------|---------------|
| 0 | [Introducere](00-prerequisites.md) | Ce vei construi, verificarea Laboratorului 01, comparație Laborator 02 vs Laborator 01 |
| 1 | [Înțelegerea arhitecturii multi-agent](01-understand-multi-agent.md) | Învățare WorkflowBuilder, rolurile agenților, graficul de orchestrare |
| 2 | [Scaffold pentru proiectul multi-agent](02-scaffold-multi-agent.md) | Folosește vrăjitorul extensiei Foundry pentru a scaffolda proiectul de bază |
| 3 | [Configurarea agenților și a mediului](03-configure-agents.md) | Scrie instrucțiuni pentru 4 agenți, configurează uneltele MCP, setează variabilele de mediu |
| 4 | [Modele de orchestrare](04-orchestration-patterns.md) | Lanț secvențial, retransmitere conținut, și semantica OR în WorkflowBuilder |
| 5 | [Testare locală](05-test-locally.md) | Debug F5 cu Agent Inspector, rulează teste rapide cu CV + descriere job |
| 6 | [Implementare pe Foundry](06-deploy-to-foundry.md) | Construiește containerul, împinge pe ACR, înregistrează agentul găzduit |
| 7 | [Verificare în Playground](07-verify-in-playground.md) | Testează agentul implementat în playground-urile VS Code și Foundry Portal |
| 8 | [Depanare](08-troubleshooting.md) | Remediază probleme comune multi-agent (erori MCP, ieșire trunchiată, versiuni pachete) |
| 9 | [Rezumat & pași următori](09-summary.md) | Ce ai construit, conceptele cheie învățate, curățenie, și ce urmează |

---

**Înapoi la:** [Laborator 02 README](../README.md) · [Acasă Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->