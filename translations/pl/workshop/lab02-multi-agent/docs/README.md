# Lab 02 - Wieloagentowy przepływ pracy: Oceniacz dopasowania CV do pracy

## Pełna ścieżka nauki

Ta dokumentacja przeprowadzi Cię przez tworzenie, testowanie i wdrażanie **wieloagentowego przepływu pracy**, który ocenia dopasowanie CV do pracy za pomocą czterech wyspecjalizowanych agentów zarządzanych przez **WorkflowBuilder**.

> **Wymaganie wstępne:** Ukończ [Lab 01 - Pojedynczy agent](../../lab01-single-agent/README.md) przed rozpoczęciem Laboratorium 02.

---

## Moduły

| # | Moduł | Co zrobisz |
|---|--------|---------------|
| 0 | [Wymagania wstępne](00-prerequisites.md) | Zweryfikuj ukończenie Laboratorium 01, poznaj koncepcje wieloagentowe |
| 1 | [Poznaj architekturę wieloagentową](01-understand-multi-agent.md) | Naucz się WorkflowBuilder, ról agentów, grafu orkiestracji |
| 2 | [Stwórz szkielet projektu wieloagentowego](02-scaffold-multi-agent.md) | Użyj rozszerzenia Foundry do stworzenia szkieletu wieloagentowego przepływu pracy |
| 3 | [Konfiguracja agentów i środowiska](03-configure-agents.md) | Napisz instrukcje dla 4 agentów, skonfiguruj narzędzie MCP, ustaw zmienne środowiskowe |
| 4 | [Wzorce orkiestracji](04-orchestration-patterns.md) | Poznaj równoległe rozgałęzienie, sekwencyjną agregację i alternatywne wzorce |
| 5 | [Testuj lokalnie](05-test-locally.md) | Debuguj za pomocą Agent Inspector, uruchom testy dymne z CV i opisem stanowiska |
| 6 | [Wdróż do Foundry](06-deploy-to-foundry.md) | Zbuduj kontener, wypchnij do ACR, zarejestruj hostowanego agenta |
| 7 | [Zweryfikuj w Playground](07-verify-in-playground.md) | Przetestuj wdrożonego agenta w VS Code i Foundry Portal playground |
| 8 | [Rozwiązywanie problemów](08-troubleshooting.md) | Napraw powszechne problemy wieloagentowe (błędy MCP, ucięty output, wersje pakietów) |

---

## Szacowany czas

| Poziom doświadczenia | Czas |
|-----------------|------|
| Niedawno ukończone Laboratorium 01 | 45-60 minut |
| Pewne doświadczenie z Azure AI | 60-90 minut |
| Pierwszy raz z wieloma agentami | 90-120 minut |

---

## Architektura w skrócie

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

**Powrót do:** [Lab 02 README](../README.md) · [Strona warsztatu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:  
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w języku źródłowym powinien być uznawany za wiarygodne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->