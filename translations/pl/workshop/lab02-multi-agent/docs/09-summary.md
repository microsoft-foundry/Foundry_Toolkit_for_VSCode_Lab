# Moduł 9 - Podsumowanie i kolejne kroki

⏱️ ~5 min

**Gratulacje!** Zbudowałeś, przetestowałeś i (jeśli na ścieżce A) wdrożyłeś wieloagentowy przepływ pracy korzystając z Microsoft Foundry oraz Foundry Toolkit dla VS Code.

---

## Co zbudowałeś

**Resume → Job Fit Evaluator** - wieloagentowy hostowany przepływ pracy, który:
- Otrzymuje CV + opis stanowiska przez HTTP (`POST /responses`)
- Uruchamia czterech wyspecjalizowanych agentów w sekwencyjnej pętli - każdy agent przekazuje danym następcy, których on potrzebuje
- Zwraca wynik dopasowania (0–100 z rozbiciem), listę braków w umiejętnościach i certyfikatach oraz spersonalizowaną ścieżkę nauki z prawdziwymi linkami Microsoft Learn dla każdego braku
- Wywołuje serwer Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`), aby pobrać oficjalne zasoby nauki dla każdego wykrytego braku umiejętności
- Działa jako pojedynczy, konteneryzowany hostowany agent w usłudze Microsoft Foundry Agent Service

---

## Kluczowe poznane koncepcje

| Koncepcja | Co ćwiczyłeś |
|---------|-------------------|
| **Orkiestracja wieloagentowa** | `WorkflowBuilder` sekwencyjny pipeline z `add_edge()` |
| **Specjalizacja agentów** | Czterech wyspecjalizowanych agentów przewyższa jednego ogólnego |
| **Wzorzec Content Router** | ResumeParser pełni również rolę routera - zachowuje tekst JD w sekcji `[JOB DESCRIPTION PASS-THROUGH]`, aby agenci dalej w przepływie mogli do niego dotrzeć (wymagane, ponieważ `context_mode="last_agent"` oznacza, że tylko `start_executor` widzi surową wiadomość użytkownika) |
| **Wzorzec Content Relay** | Agent JD przekazuje dalej `[PARSED RESUME PASS-THROUGH]`, żeby MatchingAgent otrzymał oba profile; unika to podwójnego wyzwalania semantyki OR, która zdarza się w grafach fan-in |
| **Integracja narzędzia MCP** | `@tool` + `streamable_http_client` wywołujący zewnętrzny serwer MCP |
| **Cykl życia Hostowanego Agenta** | Scaffold → Konfiguracja → Test lokalny → Wdrożenie → Weryfikacja w chmurze |
| **`context_mode="last_agent"`** | Każdy executor widzi tylko wyjście swojego bezpośredniego poprzednika |
| **Foundry Toolkit workflow** | Kreator szkieletu, Inspektor Agenta, Wizualizator Przepływu, wdrożenie jednym kliknięciem |

---

## Co ukończyłeś

<details open>
<summary><strong>🅰️ Ścieżka A - subskrypcja Foundry</strong></summary>

- [x] Zweryfikowano konfigurację Lab 01: projekt, model i RBAC nadal aktywne
- [x] Utworzono szkielet projektu z wieloma agentami korzystając z szablonu Workflows
- [x] Napisano cztery zestawy instrukcji dla agentów (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Zintegrowano narzędzie Microsoft Learn MCP z `streamable_http_client`
- [x] Połączono graf przepływu pracy za pomocą `WorkflowBuilder` (sekwencyjny pipeline z przekazywaniem treści)
- [x] Przetestowano lokalnie trzema testami podstawowymi (Inspektor Agenta) - wynik dopasowania, karty braków i adresy URL MCP
- [x] Wdrożono do Foundry Agent Service (konteneryzowane, zarządzana tożsamość)
- [x] Zweryfikowano w chmurowym środowisku testowym - spójność strukturalna z wynikami lokalnymi

</details>

<details open>
<summary><strong>🅱️ Ścieżka B - Foundry Local</strong></summary>

- [x] Zweryfikowano konfigurację Lab 01: Foundry Local działa z lokalnym modelem
- [x] Utworzono szkielet projektu z wieloma agentami korzystając z szablonu Workflows
- [x] Napisano cztery zestawy instrukcji dla agentów i połączono graf przepływu pracy
- [x] Zintegrowano narzędzie Microsoft Learn MCP
- [x] Przetestowano lokalnie trzema testami podstawowymi
- [x] Zweryfikowano zachowanie wieloagentowe bez potrzeby zasobów chmurowych

</details>

---

## Kolejne kroki

### Kontynuuj naukę

| Zasób | Opis |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | Dokumentacja API dla `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalog narzędzi MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Połącz agentów z innymi serwerami MCP (Bing, GitHub, niestandardowe) |
| **[Dodaj wiedzę (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Podstaw agenta na dokumentach, magazynach wektorów lub wyszukiwarce Bing |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mierz jakość agentów na dużą skalę za pomocą zautomatyzowanych ocen |
| **[Dokumentacja Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Pełna referencja platformy |
| **[Foundry Toolkit - Co nowego](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notatki dotyczące wersji rozszerzenia i dziennik zmian |

### Pomysły na rozszerzenie tego przepływu

- **Dodaj 5. agenta** - Trenera do rozmów kwalifikacyjnych, który generuje prawdopodobne pytania na podstawie raportu braków
- **Dodaj narzędzie Bing grounding** - Pozwól agentowi JD wyszukać podobne oferty pracy, aby wzbogacić wymagania
- **Podłącz się do bazy CV** - Pobieraj profile kandydatów z bazy za pomocą niestandardowego `@tool`
- **Wypróbuj różne modele** - Porównaj jakość i szybkość wyjścia `gpt-4.1` i `gpt-4.1-mini`
- **Oceń za pomocą Foundry** - Skorzystaj z funkcji Evaluations, aby ocenić raporty dopasowania w stosunku do zestawu wzorcowego

### Dla użytkowników ścieżki B: Aktualizacja do wdrożenia w chmurze

Gdy będziesz gotowy do wdrożenia w chmurze:
1. Uzyskaj subskrypcję Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Ukończ [Lab 01, Moduł 01](../../lab01-single-agent/docs/01-setup.md) (utwórz projekt, wdroż model, przypisz RBAC)
3. Zaktualizuj swój plik `.env` o endpoint projektu Foundry i nazwę wdrożenia modelu
4. Kontynuuj od [Moduł 06 - Wdrożenie do Foundry](06-deploy-to-foundry.md)

---

## Sprzątanie zasobów (opcjonalne)

Jeśli chcesz usunąć zasoby Azure utworzone podczas tego warsztatu:

### Opcja 1: Usuń grupę zasobów (usuwa wszystko)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opcja 2: Usuń tylko hostowanego agenta

1. Otwórz [ai.azure.com](https://ai.azure.com) → swój projekt → **Build** → **Agents**.
2. Znajdź **PersonalCareerCopilot** → kliknij **Delete**.

### Opcja 3: Usuń wdrożenie modelu

1. W panelu Foundry rozwiń swój projekt → **Models**.
2. Kliknij prawym przyciskiem wdrożenie modelu → **Delete**.

> **Uwaga kosztowa:** Hostowani agenci generują koszty tylko podczas działania. Jeśli zatrzymasz lub usuniesz agenta, nie będzie dalszych opłat. Wdrożenie modelu może generować niewielkie opłaty za zarezerwowaną pojemność - usuń je, jeśli skończyłeś.

---

**Poprzedni:** [08 - Rozwiązywanie problemów](08-troubleshooting.md) · **Strona główna:** [Lab 02 README](../README.md) · [Strona główna warsztatu](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->