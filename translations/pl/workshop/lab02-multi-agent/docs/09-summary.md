# Moduł 9 - Podsumowanie i kolejne kroki

⏱️ ~5 min

**Gratulacje!** Zbudowałeś, przetestowałeś i (jeśli na Ścieżce A) wdrożyłeś wieloagentowy przepływ pracy używając Microsoft Foundry i Foundry Toolkit dla VS Code.

---

## Co zbudowałeś

**Resume → Job Fit Evaluator** – wieloagentowy hostowany przepływ pracy, który:
- Otrzymuje CV + opis stanowiska przez HTTP (`POST /responses`)
- Uruchamia czterech specjalistycznych agentów w sekwencyjnym potoku – każdy agent przekazuje dane swojemu następcy
- Zwraca ocenę dopasowania (0–100 z rozbiciem), listę braków w umiejętnościach i certyfikatach oraz spersonalizowaną ścieżkę nauki z rzeczywistymi linkami Microsoft Learn do każdego braku
- Wywołuje serwer Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`), aby pobrać oficjalne zasoby edukacyjne dla każdego zidentyfikowanego braku umiejętności
- Działa jako pojedynczy, konteneryzowany hostowany agent w Microsoft Foundry Agent Service

---

## Kluczowe poznane koncepcje

| Koncepcja | Co ćwiczyłeś |
|---------|-------------------|
| **Orkiestracja wieloagentowa** | `WorkflowBuilder` sekwencyjny potok z `add_edge()` |
| **Specjalizacja agentów** | Czterech skupionych agentów przewyższa jednego uniwersalnego |
| **Wzorzec Content Router** | ResumeParser pełni też rolę routera – zachowuje tekst JD w sekcji `[JOB DESCRIPTION PASS-THROUGH]` tak, aby agenci poniżej mogli do niego dotrzeć (konieczne, bo `context_mode="last_agent"` oznacza, że tylko `start_executor` widzi surową wiadomość użytkownika) |
| **Wzorzec Content Relay** | Agent JD przekazuje dalej `[PARSED RESUME PASS-THROUGH]`, aby MatchingAgent otrzymał oba profile; unika to podwójnego wyzwalania OR, jakie pojawia się w grafach fan-in |
| **Integracja narzędzia MCP** | `@tool` + `streamable_http_client` wywołujące zewnętrzny serwer MCP |
| **Cykl życia hostowanego agenta** | Scaffold → Konfiguracja → Test lokalny → Wdrożenie → Weryfikacja w chmurze |
| **`context_mode="last_agent"`** | Każdy executor widzi tylko wynik swojego bezpośredniego poprzednika |
| **Przepływ pracy Foundry Toolkit** | Kreator scaffoldingu, Agent Inspector, Workflow Visualizer, wdrożenie jednym kliknięciem |

---

## Co ukończyłeś

<details open>
<summary><strong>🅰️ Ścieżka A – subskrypcja Foundry</strong></summary>

- [x] Zweryfikowano konfigurację Laboratorium 01: projekt, model i RBAC nadal aktywne
- [x] Scaffoldowano projekt wieloagentowy wykorzystując szablon Workflows
- [x] Napisano cztery zestawy instrukcji dla agentów (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Zintegrowano narzędzie Microsoft Learn MCP z `streamable_http_client`
- [x] Połączono graf przepływu pracy z `WorkflowBuilder` (sekwencyjny potok z relay treści)
- [x] Przetestowano lokalnie dwoma testami (Agent Inspector) – ocena dopasowania, karty braków, i URL-e MCP
- [x] Wdrożono do Foundry Agent Service (konteneryzowany, zarządzana tożsamość)
- [x] Zweryfikowano w chmurowym placu zabaw – spójność strukturalna z wynikami lokalnymi

</details>

<details open>
<summary><strong>🅱️ Ścieżka B – Foundry Local</strong></summary>

- [x] Zweryfikowano konfigurację Laboratorium 01: Foundry Local działa z lokalnym modelem
- [x] Scaffoldowano projekt wieloagentowy wykorzystując szablon Workflows
- [x] Napisano cztery zestawy instrukcji dla agentów i połączono graf przepływu pracy
- [x] Zintegrowano narzędzie Microsoft Learn MCP
- [x] Przetestowano lokalnie dwoma testami dymnymi
- [x] Zweryfikowano zachowanie wieloagentowe bez konieczności użycia zasobów chmurowych

</details>

---

## Kolejne kroki

### Kontynuuj naukę

| Zasób | Opis |
|----------|-------------|
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | Dokumentacja API dla `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP tool catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Podłącz agentów do innych serwerów MCP (Bing, GitHub, niestandardowe) |
| **[Add knowledge (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Ugruntuj agentów dokumentami, bazami wektorowymi lub wyszukiwaniem Bing |
| **[Foundry Evaluations](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mierz jakość agentów na dużą skalę za pomocą automatycznych ewaluatorów |
| **[Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/)** | Pełna dokumentacja platformy |
| **[Foundry Toolkit - What's New](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notatki z wydania rozszerzenia i dziennik zmian |

### Pomysły na rozbudowę tego przepływu pracy

- **Dodaj 5. agenta** – Coach do rozmów kwalifikacyjnych generujący prawdopodobne pytania na podstawie raportu braków
- **Dodaj narzędzie Bing grounding** – Pozwól agentowi JD wyszukiwać podobne oferty pracy, aby wzbogacić wymagania
- **Połącz z bazą CV** – Pobieraj profile kandydatów z bazy przez niestandardowy `@tool`
- **Wypróbuj różne modele** – Porównaj jakość i opóźnienie wyników `gpt-4.1` vs. `gpt-4.1-mini`
- **Oceń z Foundry** – Wykorzystaj funkcję Evaluations do oceniania raportów dopasowania względem złotego zbioru danych

### Dla użytkowników Ścieżki B: Aktualizacja do wdrożenia w chmurze

Gdy będziesz gotowy do wdrożenia w chmurze:
1. Uzyskaj subskrypcję Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Ukończ [Laboratorium 01, Moduł 01](../../lab01-single-agent/docs/01-setup.md) (utwórz projekt, wdroż model, przypisz RBAC)
3. Zaktualizuj swój `.env` o punkt końcowy projektu Foundry i nazwę wdrożenia modelu
4. Kontynuuj od [Modułu 06 - Wdrożenie do Foundry](06-deploy-to-foundry.md)

---

## Czyszczenie zasobów (opcjonalne)

Jeśli chcesz usunąć zasoby Azure utworzone podczas tego warsztatu:

### Opcja 1: Usuń grupę zasobów (usuwa wszystko)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opcja 2: Usuń tylko hostowanego agenta

1. Otwórz [ai.azure.com](https://ai.azure.com) → swój projekt → **Build** → **Agents**.
2. Znajdź **PersonalCareerCopilot** → kliknij **Delete**.

### Opcja 3: Usuń wdrożenie modelu

1. W pasku bocznym Foundry rozwiń swój projekt → **Models**.
2. Kliknij prawym przyciskiem na wdrożenie modelu → **Delete**.

> **Informacja o kosztach:** Hostowani agenci generują koszty tylko podczas działania. Jeśli zatrzymasz lub usuniesz agenta, nie ma dalszych opłat. Wdrożenie modelu może generować niewielkie koszty za zarezerwowaną pojemność – usuń je, jeśli skończyłeś.

---

**Poprzedni:** [08 - Rozwiązywanie problemów](08-troubleshooting.md) · **Strona główna:** [Lab 02 README](../README.md) · [Strona główna warsztatów](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->