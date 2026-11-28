# Moduł 0 - Wprowadzenie

⏱️ ~10 min

> [!WARNING]
> **Podgląd i ograniczenia:** [Hosted Agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) są obecnie w **publicznym podglądzie** – nie zaleca się ich do obciążeń produkcyjnych. Niektóre funkcje pokazane w tym warsztacie mogą się zmienić, gdy usługa będzie zmierzać do wersji GA.

## Co zbudujesz

W tym laboratorium rozbudujesz umiejętności pojedynczego agenta z Laboratorium 01, aby zbudować **wieloagentowy przepływ pracy** – Ocenę dopasowania CV do pracy.

Wklejasz **CV** i **opis stanowiska**. Czterech wyspecjalizowanych agentów przetwarza dane wejściowe kolejno, a następnie zwraca:
- Wskaźnik dopasowania (0–100 z podziałem punktacji)
- Listę brakujących umiejętności i certyfikatów
- Spersonalizowaną ścieżkę nauki z rzeczywistymi linkami Microsoft Learn dla każdej luki

**Przepływ pracy wykorzystuje:**
- **Microsoft Agent Framework** - `WorkflowBuilder` do sekwencyjnej orkiestracji potoku
- **Foundry Toolkit dla VS Code** - szablony, test lokalny, wdrożenie
- **Model AI** (np. `gpt-4.1-mini`) - używany przez wszystkich czterech agentów
- **Microsoft Learn MCP server** - zapewnia prawdziwe linki do materiałów edukacyjnych dla każdej luki umiejętności

---

## Wybierz swoją ścieżkę

> ⚠️ **Kontynuuj ścieżką, której używałeś w Laboratorium 01.**

<details open>
<summary><strong>🅰️ Ścieżka A - chmura Azure (wymaga subskrypcji Azure)</strong></summary>

| | Szczegóły |
|---|---|
| **Dla kogo?** | Ukończyłeś Laboratorium 01 korzystając z subskrypcji Azure |
| **Model** | Azure OpenAI przez Foundry (np. `gpt-4.1-mini`) |
| **Obsługiwane moduły** | Wszystkie moduły (00–09) |
| **Wdrożenie w chmurze?** | ✅ Tak - pełne wdrożenie end-to-end |

</details>

<details open>
<summary><strong>🅱️ Ścieżka B - Foundry Local (nie wymaga subskrypcji Azure)</strong></summary>

| | Szczegóły |
|---|---|
| **Dla kogo?** | Ukończyłeś Laboratorium 01 korzystając z Foundry Local |
| **Model** | Foundry Local (darmowy, działa na twojej maszynie) |
| **Obsługiwane moduły** | Moduły 00–05 (pomijaj 06–07 - wdrożenie i weryfikacja chmury) |
| **Wdrożenie w chmurze?** | ❌ Nie - tylko test lokalny przez Agent Inspector |

</details>

---

## Sprawdzenie Laboratorium 01

Laboratorium 02 bazuje bezpośrednio na Laboratorium 01. Najpierw ukończ Laboratorium 01, zanim zaczniesz tutaj.

Jeszcze nie zrobiłeś Laboratorium 01? Zacznij tutaj: [Laboratorium 01 – Wprowadzenie](../../lab01-single-agent/docs/00-prerequisites.md)

<details open>
<summary><strong>🅰️ Ścieżka A - chmura Azure</strong></summary>

```powershell
az account show --query "{name:name, id:id}" --output table
```

Jeśli to się nie powiedzie, uruchom `az login`. Następnie sprawdź w VS Code:

1. `Ctrl+Shift+P` → wpisz **Foundry Toolkit** → potwierdź, że pojawiły się polecenia.
2. Kliknij ikonę **Foundry Toolkit** → twój projekt i wdrożony model pokażą **Sukces**.

![Foundry Toolkit w pasku bocznym pokazujący projekt w Moje zasoby, z otwartym wyborem Przełącz projekt / Utwórz projekt](../../../../../translated_images/pl/00-foundry-sidebar-project-model.51036e8b9386e1f4.webp)

> **RBAC:** Przypisałeś rolę **Foundry User** w Laboratorium 01. Jeśli potrzebujesz przypisać ponownie, zobacz [Laboratorium 01, Moduł 1](../../lab01-single-agent/docs/01-setup.md#deploy-a-model--assign-rbac). Rola wcześniej nazywała się **Azure AI User** – te same uprawnienia.

</details>

<details open>
<summary><strong>🅱️ Ścieżka B - Foundry Local</strong></summary>

```powershell
Invoke-WebRequest -Uri "http://localhost:5273/v1/health" -UseBasicParsing | Select-Object StatusCode
```

Oczekiwany rezultat: `StatusCode: 200`. Jeśli nie, zrestartuj Foundry Local z paska bocznego Foundry Toolkit.

> Całe wnioskowanie odbywa się na twojej maszynie. Jedyny zewnętrzny ruch to narzędzie MCP do `https://learn.microsoft.com/api/mcp`.

</details>

---

## Co nowego w Laboratorium 02

| | Laboratorium 01 | Laboratorium 02 |
|--|--------|--------|
| Agenci | 1 | 4 (połączone z WorkflowBuilder) |
| Szablon szkieletu | Podstawowy – Agent Framework | Workflow – Agent Framework |
| Nowy pakiet | - | `mcp` |
| Orkiestracja | Jeden agent konwersacyjny | Sekwencyjny potok (WorkflowBuilder) |
| Nowe narzędzie | - | `search_microsoft_learn_for_plan` (MCP) |

---

**Następne:** [01 – Zrozumieć Architekturę →](01-understand-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->