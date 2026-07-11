# Laboratorium 02 - Przepływ pracy wielu agentów: Ocena dopasowania CV do pracy

## Pełna ścieżka nauki

Ta dokumentacja przeprowadzi Cię przez proces budowania, testowania i wdrażania **przepływu pracy wielu agentów**, który ocenia dopasowanie CV do pracy przy użyciu czterech wyspecjalizowanych agentów zarządzanych przez **WorkflowBuilder**.

> **Wymaganie wstępne:** Ukończ [Laboratorium 01 - Jeden agent](../../lab01-single-agent/README.md) przed rozpoczęciem Laboratorium 02.

---

## Moduły

| # | Moduł | Co zrobisz |
|---|--------|------------|
| 0 | [Wprowadzenie](00-prerequisites.md) | To, co zbudujesz, weryfikacja Laboratorium 01, porównanie Laboratorium 02 i 01 |
| 1 | [Zrozum architekturę wielu agentów](01-understand-multi-agent.md) | Poznaj WorkflowBuilder, role agentów, graf orkiestracji |
| 2 | [Szkielet projektu wielu agentów](02-scaffold-multi-agent.md) | Użyj kreatora rozszerzenia Foundry do utworzenia szkieletu projektu |
| 3 | [Konfiguracja agentów i środowiska](03-configure-agents.md) | Napisz instrukcje dla 4 agentów, skonfiguruj narzędzie MCP, ustaw zmienne środowiskowe |
| 4 | [Wzorce orkiestracji](04-orchestration-patterns.md) | Łańcuch sekwencyjny, przekazywanie treści i semantyka OR w WorkflowBuilder |
| 5 | [Testowanie lokalne](05-test-locally.md) | Debugowanie F5 z Agent Inspector, uruchamianie testów dymnych z CV + opisem pracy |
| 6 | [Wdrażanie do Foundry](06-deploy-to-foundry.md) | Budowanie kontenera, push do ACR, rejestracja hostowanego agenta |
| 7 | [Weryfikacja na Playground](07-verify-in-playground.md) | Testowanie wdrożonego agenta w VS Code i Playground Portalu Foundry |
| 8 | [Rozwiązywanie problemów](08-troubleshooting.md) | Naprawa typowych problemów z wieloma agentami (błędy MCP, obcięte wyjścia, wersje pakietów) |
| 9 | [Podsumowanie i dalsze kroki](09-summary.md) | Co zbudowałeś, kluczowe koncepcje, sprzątanie i co dalej |

---

**Wróć do:** [Lab 02 README](../README.md) · [Strona główna warsztatu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->