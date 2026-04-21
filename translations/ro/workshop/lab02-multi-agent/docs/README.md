# Laborator 02 - Flux de lucru multi-agent: Evaluator potrivire CV → Job

## Parcurs complet de învățare

Această documentație te ghidează prin construirea, testarea și implementarea unui **flux de lucru multi-agent** care evaluează potrivirea unui CV cu un job folosind patru agenți specializați orchestrați prin **WorkflowBuilder**.

> **Precondiție:** Finalizează [Laborator 01 - Agent singur](../../lab01-single-agent/README.md) înainte de a începe Laboratorul 02.

---

## Module

| # | Modul | Ce vei face |
|---|--------|-------------|
| 0 | [Precondiții](00-prerequisites.md) | Verifică finalizarea Laboratorului 01, înțelege conceptele multi-agent |
| 1 | [Înțelege arhitectura multi-agent](01-understand-multi-agent.md) | Învață WorkflowBuilder, rolurile agenților, graficul de orchestrare |
| 2 | [Configurează proiectul multi-agent](02-scaffold-multi-agent.md) | Folosește extensia Foundry pentru a scana un flux de lucru multi-agent |
| 3 | [Configurează agenții și mediul](03-configure-agents.md) | Scrie instrucțiuni pentru 4 agenți, configurează instrumentul MCP, setează variabilele de mediu |
| 4 | [Modele de orchestrare](04-orchestration-patterns.md) | Explorează paralelismul fan-out, agregarea secvențială și modele alternative |
| 5 | [Testează local](05-test-locally.md) | Debug F5 cu Agent Inspector, rulează teste de fum cu CV + descriere job |
| 6 | [Implementează în Foundry](06-deploy-to-foundry.md) | Construiește containerul, împinge în ACR, înregistrează agentul găzduit |
| 7 | [Verifică în Playground](07-verify-in-playground.md) | Testează agentul implementat în playground-uri VS Code și Foundry Portal |
| 8 | [Depanare](08-troubleshooting.md) | Rezolvă probleme comune multi-agent (erori MCP, ieșire trunchiată, versiuni pachete) |

---

## Timp estimat

| Nivel experiență | Timp |
|-----------------|------|
| Ai finalizat recent Laboratorul 01 | 45-60 minute |
| Ai experiență cu Azure AI | 60-90 minute |
| Este prima dată când lucrezi cu multi-agent | 90-120 minute |

---

## Arhitectura pe scurt

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

**Înapoi la:** [Laborator 02 README](../README.md) · [Acasă Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care pot rezulta din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->