# Moduł 7 - Weryfikacja na Playground

⏱️ ~10 min

W tym module przetestujesz wdrożony wieloagentowy workflow w VS Code oraz w Foundry Portal, potwierdzając, że agent zachowuje się tak samo jak podczas lokalnego testowania.

---

## Dlaczego testować ponownie po wdrożeniu?

Środowisko hostowane różni się od lokalnego w kilku istotnych aspektach:

| | Lokalnie | Hostowane |
|--|----------|-----------|
| **Tożsamość** | Twoje osobiste logowanie (`DefaultAzureCredential`) | Dedykowana tożsamość Entra na agenta (automatycznie tworzone podczas wdrożenia) |
| **Endpoint** | `http://localhost:8088/responses` | URL zarządzany przez Foundry Agent Service |
| **Sieć** | Twój komputer → Azure OpenAI + MCP | Szkielet Azure (niższa latencja) |

Złe skonfigurowanie zmiennej środowiskowej, problem z RBAC lub zablokowane wywołanie MCP pojawi się tutaj jako pierwszy.

---

## Opcja A: Testowanie na VS Code Playground (zalecane na początek)

### Krok 1: Przejdź do swojego hostowanego agenta

1. Kliknij ikonę **Foundry Toolkit** na pasku aktywności.
2. Rozwiń swój projekt → **Hosted Agents (Preview)** → znajdź swojego agenta.

![Foundry Toolkit sidebar showing Hosted Agents (Preview) with resume-job-fit-evaluator and its deployed versions](../../../../../translated_images/pl/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Krok 2: Wybierz wersję

1. Kliknij na agenta, aby rozwinąć jego wersje.
2. Kliknij `v1` → sprawdź, czy status jest **aktywny** (w pasku bocznym może pojawić się "Running" lub "Started" - oba oznaczają stan gotowości).

### Krok 3: Otwórz Playground

1. Kliknij **Playground** (lub kliknij prawym przyciskiem wersję → **Open in Playground**).
2. Otworzy się okno rozmowy na karcie VS Code.

### Krok 4: Uruchom testy dymne

Użyj tych samych 3 testów z [Modułu 5](05-test-locally.md). Wpisz każdą wiadomość w polu wejściowym na Playground i naciśnij **Wyślij** (lub **Enter**).

#### Test 1 - Pełne CV + JD (standardowy przebieg)

Wklej pełny prompt CV + JD z Modułu 5, Test 1 (Jane Doe + Senior Cloud Engineer w Contoso Ltd).

**Oczekiwane:**
- Wynik dopasowania z rozbiciem matematycznym (skala 100 punktów)
- Sekcja Dopasowane Umiejętności
- Sekcja Brakujące Umiejętności
- **Jedna karta luki na każdą brakującą umiejętność** z linkami Microsoft Learn
- Plan nauki z harmonogramem

#### Test 2 - Szybki krótki test (minimalne dane wejściowe)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Oczekiwane:**
- Niższy wynik dopasowania (< 40)
- Uczciwa ocena ze etapową ścieżką nauki
- Wiele kart luk (AWS, Kubernetes, Terraform, CI/CD, brak doświadczenia)

#### Test 3 - Kandydat o wysokim dopasowaniu

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Oczekiwane:**
- Wysoki wynik dopasowania (≥ 80)
- Skupienie na gotowości do rozmowy i dopracowaniu
- Niewiele lub brak kart luk
- Krótki harmonogram skupiony na przygotowaniu

### Krok 5: Porównaj z wynikami lokalnymi

Otwórz swoje notatki lub kartę w przeglądarce z Modułu 5, gdzie zapisałeś lokalne odpowiedzi. Dla każdego testu:

- Czy odpowiedź ma **tę samą strukturę** (wynik dopasowania, karty luk, plan nauki)?
- Czy stosuje się do **tej samej skali punktacji** (rozbicie na 100 punktów)?
- Czy **linki Microsoft Learn** nadal są obecne na kartach luk?
- Czy jest **jedna karta luki na każdą brakującą umiejętność** (nie jest ucięta)?

> **Drobne różnice w sformułowaniach są normalne** - model jest niedeterministyczny. Skup się na strukturze, spójności punktacji i użyciu narzędzi MCP.

---

## Opcja B: Testowanie w Foundry Portal

[Foundry Portal](https://ai.azure.com) dostarcza webowe playground przydatne do współdzielenia z zespołem lub interesariuszami.

### Krok 1: Otwórz Foundry Portal

1. Otwórz przeglądarkę i przejdź do [https://ai.azure.com](https://ai.azure.com).
2. Zaloguj się tym samym kontem Azure, którego używałeś przez cały warsztat.

### Krok 2: Przejdź do swojego projektu

1. Na stronie głównej poszukaj **Ostatnich projektów** na lewym pasku bocznym.
2. Kliknij nazwę swojego projektu (np. `workshop-agents`).
3. Jeśli go nie widzisz, kliknij **Wszystkie projekty** i wyszukaj go.

### Krok 3: Znajdź swojego wdrożonego agenta

1. W nawigacji po projekcie z lewej kliknij **Build** → **Agents** (lub znajdź sekcję **Agents**).
2. Powinna pojawić się lista agentów. Znajdź swojego wdrożonego agenta (np. `resume-job-fit-evaluator`).
3. Kliknij nazwę agenta, aby otworzyć stronę szczegółów.

### Krok 4: Otwórz Playground

1. Na stronie szczegółów agenta spójrz na górny pasek narzędzi.
2. Kliknij **Open in playground** (lub **Try in playground**).
3. Otworzy się interfejs rozmowy.

### Krok 5: Uruchom te same testy dymne

Powtórz wszystkie 3 testy z sekcji VS Code Playground powyżej. Porównaj każdą odpowiedź z wynikami lokalnymi (Moduł 5) oraz wynikami z VS Code Playground (Opcja A powyżej).

---

## Weryfikacja specyficzna dla multi-agenta

Poza podstawową poprawnością, zweryfikuj te zachowania specyficzne dla multi-agentów:

### Wykonanie narzędzia MCP

| Sprawdzenie | Jak zweryfikować | Warunek zaliczenia |
|------------|------------------|--------------------|
| Wywołania MCP kończą się sukcesem | Karty luk zawierają URL `learn.microsoft.com` | Realne URL, nie komunikaty zastępcze |
| Wiele wywołań MCP | Każda luka o wysokim/średnim priorytecie ma zasoby | Nie tylko pierwsza karta luki |
| Działa fallback MCP | Jeśli URL-e brakują, sprawdź tekst fallback | Agent nadal generuje karty luk (z URL lub bez) |

### Koordynacja agentów

| Sprawdzenie | Jak zweryfikować | Warunek zaliczenia |
|------------|------------------|--------------------|
| Wszystkie 4 agenty zostały uruchomione | Wynik zawiera dopasowanie WYNIK i karty luk | Wynik pochodzi od MatchingAgent, karty od GapAnalyzer |
| Wykonanie sekwencyjne | Czas odpowiedzi jest rozsądny (< 2 min) | Jeśli > 3 min, sprawdź błędy w logu terminala |
| Integralność przepływu danych | Karty luk odnoszą się do umiejętności z raportu dopasowania | Brak zmyślonych umiejętności, które nie są w JD |

---

## Kryteria walidacji

Użyj tej skali do oceny zachowania Twojego multi-agentowego workflow w środowisku hostowanym:

| # | Kryteria | Warunek zaliczenia | Zaliczone? |
|---|----------|--------------------|-----------|
| 1 | **Poprawność funkcjonalna** | Agent odpowiada na CV + JD z wynikiem dopasowania i analizą luk | |
| 2 | **Spójność punktacji** | Wynik dopasowania używa skali 100 punktów z rozbiciem matematycznym | |
| 3 | **Pełność kart luk** | Jedna karta na każdą brakującą umiejętność (nie ucięta ani niepołączona) | |
| 4 | **Integracja narzędzia MCP** | Karty luk zawierają prawdziwe linki Microsoft Learn | |
| 5 | **Spójność strukturalna** | Struktura wyjścia zgodna między lokalnym a hostowanym uruchomieniem | |
| 6 | **Czas odpowiedzi** | Agent hostowany odpowiada w ciągu 2 minut dla pełnej oceny | |
| 7 | **Brak błędów** | Brak błędów HTTP 500, timeoutów lub pustych odpowiedzi | |

> "Zaliczenie" oznacza spełnienie wszystkich 7 kryteriów dla wszystkich 3 testów dymnych w co najmniej jednym playgroundzie (VS Code lub Portal).

---

## Rozwiązywanie problemów z playground

| Objaw | Prawdopodobna przyczyna | Naprawa |
|-------|-----------------------|--------|
| Playground się nie ładuje | Kontener nie jest w stanie `active` | Wróć do [Modułu 6](06-deploy-to-foundry.md), zweryfikuj status wdrożenia. Poczekaj jeśli `creating` |
| Agent zwraca pustą odpowiedź | Nazwa wdrożenia modelu niezgodna | Sprawdź `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` czy odpowiada wdrożonemu modelowi |
| Agent zwraca komunikat o błędzie | Brak uprawnień [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Przydziel rolę **[Foundry User](https://aka.ms/foundry-ext-project-role)** (wcześniej Azure AI User) na poziomie projektu |
| Brak linków Microsoft Learn w kartach luk | MCP outbound zablokowany lub serwer MCP niedostępny | Sprawdź, czy kontener ma dostęp do `learn.microsoft.com`. Zobacz [Moduł 8](08-troubleshooting.md) |
| Tylko jedna karta luki (ucięta) | Instrukcje GapAnalyzer brakują "CRITICAL" bloku | Przejrzyj [Moduł 3, Krok 2.4](03-configure-agents.md) |
| Wynik dopasowania znacznie różni się od lokalnego | Inny model lub instrukcje wdrożone | Porównaj zmienne środowiskowe z `agent.yaml` i lokalnego `.env`. W razie potrzeby wdroż ponownie |
| "Agent not found" w Portalu | Wdrażanie nadal się propaguje lub nie powiodło się | Poczekaj 2 minuty, odśwież. Jeśli nadal brak, wdroż ponownie z [Modułu 6](06-deploy-to-foundry.md) |

---

### Punkt kontrolny

- [ ] Przetestowano agenta na VS Code Playground - wszystkie 3 testy dymne zaliczone
- [ ] Przetestowano agenta w Playground [Foundry Portal](https://ai.azure.com) - wszystkie 3 testy dymne zaliczone
- [ ] Odpowiedzi są strukturalnie zgodne z lokalnym testowaniem (wynik dopasowania, karty luk, plan nauki)
- [ ] Linki Microsoft Learn są obecne na kartach luk (narzędzie MCP działa w środowisku hostowanym)
- [ ] Jedna karta luki na każdą brakującą umiejętność (brak ucięcia)
- [ ] Brak błędów lub timeoutów podczas testów
- [ ] Ukończono rubrykę walidacyjną (wszystkie 7 kryteriów zaliczone)

---

**Poprzedni:** [06 - Deploy to Foundry](06-deploy-to-foundry.md) · **Następny:** [08 - Rozwiązywanie problemów →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->