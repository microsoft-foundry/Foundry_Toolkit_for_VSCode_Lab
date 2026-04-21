# Moduł 8 - Rozwiązywanie problemów (wiele agentów)

Ten moduł obejmuje typowe błędy, poprawki i strategie debugowania specyficzne dla przepływu pracy wielu agentów. W przypadku ogólnych problemów z wdrożeniem Foundry, zobacz także [przewodnik rozwiązywania problemów Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Szybki przegląd: Błąd → Naprawa

| Błąd / Objaw | Prawdopodobna przyczyna | Naprawa |
|--------------|-------------------------|---------|
| `RuntimeError: Missing required environment variable(s)` | Brak pliku `.env` lub brak ustawionych wartości | Utwórz `.env` z `PROJECT_ENDPOINT=<twoj-endpoint>` oraz `MODEL_DEPLOYMENT_NAME=<twoj-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Środowisko wirtualne nieaktywne lub zależności nie zostały zainstalowane | Uruchom `.\.venv\Scripts\Activate.ps1`, następnie `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Pakiet MCP nie jest zainstalowany (brak w requirements) | Uruchom `pip install mcp` lub sprawdź, czy `requirements.txt` zawiera go jako zależność pośrednią |
| Agent uruchamia się, ale zwraca pustą odpowiedź | Niezgodność `output_executors` lub brakujące krawędzie | Zweryfikuj `output_executors=[gap_analyzer]` oraz obecność wszystkich krawędzi w `create_workflow()` |
| Tylko jedna karta luk (pozostałe brak) | Instrukcje GapAnalyzer niepełne | Dodaj akapit `CRITICAL:` do `GAP_ANALYZER_INSTRUCTIONS` - zobacz [Moduł 3](03-configure-agents.md) |
| Wynik dopasowania (fit score) to 0 lub brak | MatchingAgent nie otrzymał danych od agentów upstream | Zweryfikuj obecność `add_edge(resume_parser, matching_agent)` oraz `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Serwer MCP odrzucił wywołanie narzędzia | Sprawdź połączenie internetowe. Spróbuj otworzyć `https://learn.microsoft.com/api/mcp` w przeglądarce. Ponów próbę |
| Brak adresów URL Microsoft Learn w odpowiedzi | Narzędzie MCP nie zarejestrowane lub zły endpoint | Zweryfikuj `tools=[search_microsoft_learn_for_plan]` dla GapAnalyzer oraz poprawność `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | Inny proces używa portu 8088 | Uruchom `netstat -ano \| findstr :8088` (Windows) lub `lsof -i :8088` (macOS/Linux) i zatrzymaj konfliktujący proces |
| `Address already in use: port 5679` | Konflikt portu debugpy | Zatrzymaj inne sesje debugowania. Uruchom `netstat -ano \| findstr :5679` aby znaleźć i zakończyć proces |
| Agent Inspector się nie otwiera | Serwer nie jest w pełni uruchomiony lub konflikt portu | Poczekaj na log "Server running". Sprawdź, czy port 5679 jest wolny |
| `azure.identity.CredentialUnavailableError` | Brak zalogowania do Azure CLI | Uruchom `az login` i ponownie uruchom serwer |
| `azure.core.exceptions.ResourceNotFoundError` | Wdrożenie modelu nie istnieje | Sprawdź, czy `MODEL_DEPLOYMENT_NAME` odpowiada wdrożonemu modelowi w projekcie Foundry |
| Status kontenera "Failed" po wdrożeniu | Awaria kontenera przy starcie | Sprawdź logi kontenera w panelu Foundry. Częste przyczyny: brakująca zmienna środowiskowa lub błąd importu |
| Wdrożenie pokazuje "Pending" dłużej niż 5 minut | Kontener długo się uruchamia lub ograniczenia zasobów | Poczekaj do 5 minut, multi-agent tworzy 4 instancje agenta. Jeśli nadal na "Pending", sprawdź logi |
| `ValueError` z `WorkflowBuilder` | Nieprawidłowa konfiguracja grafu | Upewnij się, że `start_executor` jest ustawiony, `output_executors` jest listą, brak krawędzi cyklicznych |

---

## Problemy ze środowiskiem i konfiguracją

### Brakujące lub błędne wartości `.env`

Plik `.env` musi znajdować się w katalogu `PersonalCareerCopilot/` (na tym samym poziomie co `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Oczekiwana zawartość `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Jak znaleźć PROJECT_ENDPOINT:** 
- Otwórz pasek boczny **Microsoft Foundry** w VS Code → kliknij prawym przyciskiem na projekt → **Kopiuj endpoint projektu**. 
- Lub wejdź na [Azure Portal](https://portal.azure.com) → swój projekt Foundry → **Przegląd** → **Endpoint projektu**.

> **Jak znaleźć MODEL_DEPLOYMENT_NAME:** W panelu Foundry rozwiń swój projekt → **Modele** → znajdź nazwę wdrożonego modelu (np. `gpt-4.1-mini`).

### Priorytet zmiennych env

`main.py` korzysta z `load_dotenv(override=False)`, co oznacza:

| Priorytet | Źródło | Czy wygrywa, gdy oba ustawione? |
|-----------|--------|---------------------------------|
| 1 (najwyższy) | Zmienna środowiskowa powłoki | Tak |
| 2 | Plik `.env` | Tylko jeśli zmienna powłoki nie jest ustawiona |

Oznacza to, że zmienne środowiskowe Foundry runtime (ustawiane przez `agent.yaml`) mają wyższy priorytet niż wartości w `.env` podczas hostowanego wdrożenia.

---

## Kompatybilność wersji

### Macierz wersji pakietów

Przepływ wielu agentów wymaga konkretnych wersji pakietów. Niezgodności powodują błędy w czasie działania.

| Pakiet | Wymagana wersja | Komenda do sprawdzenia |
|---------|-----------------|-----------------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | najnowsza wersja przedpremierowa | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Typowe błędy wersji

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Naprawa: aktualizacja do rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` nie znaleziony lub Inspector niezgodny:**

```powershell
# Poprawka: instalacja z flagą --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Poprawka: aktualizacja pakietu mcp
pip install mcp --upgrade
```

### Sprawdzenie wszystkich wersji jednocześnie

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Oczekiwany wynik:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Problemy z narzędziem MCP

### Narzędzie MCP nie zwraca wyników

**Objaw:** Karty luk pokazują „Brak wyników zwróconych przez Microsoft Learn MCP” lub „Brak bezpośrednich wyników Microsoft Learn”.

**Możliwe przyczyny:**

1. **Problem z siecią** – Endpoint MCP (`https://learn.microsoft.com/api/mcp`) jest niedostępny.
   ```powershell
   # Testuj łączność
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Jeśli zwraca `200`, endpoint jest dostępny.

2. **Zapytanie zbyt specyficzne** – Nazwa umiejętności jest zbyt niszowa dla wyszukiwarki Microsoft Learn.
   - To oczekiwane przy bardzo specjalistycznych umiejętnościach. Narzędzie ma zapasowy URL w odpowiedzi.

3. **Limit sesji MCP** – Połączenie Streamable HTTP wygasło.
   - Ponów żądanie. Sesje MCP są efemeryczne i mogą wymagać ponownego połączenia.

### Wyjaśnienie logów MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Znaczenie | Działanie |
|-----|-----------|-----------|
| `GET → 405` | Klient MCP wykonuje testy podczas inicjalizacji | Normalne - ignoruj |
| `POST → 200` | Wywołanie narzędzia powiodło się | Oczekiwane |
| `DELETE → 405` | Klient MCP wykonuje testy podczas czyszczenia | Normalne - ignoruj |
| `POST → 400` | Nieprawidłowe żądanie (błędne zapytanie) | Sprawdź parametr `query` w `search_microsoft_learn_for_plan()` |
| `POST → 429` | Ograniczenie liczby wywołań | Poczekaj i spróbuj ponownie. Zmniejsz `max_results` |
| `POST → 500` | Błąd serwera MCP | Przejściowy - spróbuj ponownie. Jeśli trwa, API MCP Microsoft Learn może być niedostępne |
| Timeout połączenia | Problem sieciowy lub niedostępny serwer MCP | Sprawdź internet. Spróbuj `curl https://learn.microsoft.com/api/mcp` |

---

## Problemy z wdrożeniem

### Kontener nie uruchamia się po wdrożeniu

1. **Sprawdź logi kontenera:**
   - Otwórz pasek boczny **Microsoft Foundry** → rozwiń **Hosted Agents (Preview)** → kliknij swojego agenta → rozwiń wersję → **Szczegóły kontenera** → **Logi**.
   - Szukaj śladów stosu Pythona lub błędów braku modułów.

2. **Typowe przyczyny awarii startu kontenera:**

   | Błąd w logach | Przyczyna | Naprawa |
   |--------------|-----------|---------|
   | `ModuleNotFoundError` | Brak pakietu w `requirements.txt` | Dodaj pakiet, wdroż ponownie |
   | `RuntimeError: Missing required environment variable` | Zmienne środowiskowe w `agent.yaml` nie ustawione | Zaktualizuj sekcję `environment_variables` w `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Nie skonfigurowano Managed Identity | Foundry ustawia to automatycznie - upewnij się, że wdrażasz przez rozszerzenie |
   | `OSError: port 8088 already in use` | Dockerfile wystawia zły port lub konflikt portów | Sprawdź `EXPOSE 8088` w Dockerfile oraz `CMD ["python", "main.py"]` |
   | Kontener kończy działanie z kodem 1 | Nieobsługiwany wyjątek w `main()` | Przetestuj lokalnie ([Moduł 5](05-test-locally.md)) przed wdrożeniem |

3. **Ponowne wdrożenie po poprawce:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → wybierz tego samego agenta → wdroż nową wersję.

### Wdrożenie trwa zbyt długo

Kontenery multi-agentów potrzebują więcej czasu na start, ponieważ tworzą 4 instancje agenta przy uruchomieniu. Typowe czasy startu:

| Etap | Oczekiwany czas |
|-------|-----------------|
| Budowa obrazu kontenera | 1-3 minuty |
| Wypchnięcie obrazu do ACR | 30-60 sekund |
| Start kontenera (pojedynczy agent) | 15-30 sekund |
| Start kontenera (wiele agentów) | 30-120 sekund |
| Agent dostępny w Playground | 1-2 minuty po logu "Started" |

> Jeśli status "Pending" trwa powyżej 5 minut, sprawdź logi kontenera w poszukiwaniu błędów.

---

## Problemy z RBAC i uprawnieniami

### `403 Forbidden` lub `AuthorizationFailed`

Potrzebujesz roli **[Azure AI User](https://aka.ms/foundry-ext-project-role)** w swoim projekcie Foundry:

1. Przejdź do [Azure Portal](https://portal.azure.com) → zasób **projektu** Foundry.
2. Kliknij **Kontrola dostępu (IAM)** → **Przydziały ról**.
3. Wyszukaj swoje imię → potwierdź, że jest tam rola **Azure AI User**.
4. Jeśli brak: **Dodaj** → **Dodaj przydział roli** → wyszukaj **Azure AI User** → przypisz do swojego konta.

Szczegóły w dokumentacji [RBAC dla Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Brak dostępu do wdrożenia modelu

Jeśli agent zwraca błędy związane z modelem:

1. Sprawdź, czy model jest wdrożony: panel Foundry → rozwiń projekt → **Modele** → potwierdź obecność `gpt-4.1-mini` (lub innego) ze statusem **Succeeded**.
2. Zweryfikuj zgodność nazwy wdrożenia: porównaj `MODEL_DEPLOYMENT_NAME` w `.env` (lub `agent.yaml`) z faktyczną nazwą wdrożenia.
3. Jeśli wdrożenie wygasło (darmowy tier): wdroż ponownie z [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problemy z Agent Inspector

### Inspector się otwiera, ale pokazuje "Disconnected"

1. Sprawdź, czy serwer działa: szukaj logu "Server running on http://localhost:8088" w terminalu.
2. Sprawdź port `5679`: Inspector łączy się przez debugpy na porcie 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Uruchom ponownie serwer i otwórz Inspector ponownie.

### Inspector pokazuje częściową odpowiedź

Odpowiedzi multi-agentów są długie i strumieniowane inkrementalnie. Poczekaj na pełne zakończenie odpowiedzi (może to trwać 30-60 sekund, zależnie od liczby kart luk i wywołań narzędzia MCP).

Jeśli odpowiedź jest stale skracana:
- Zweryfikuj, czy instrukcje GapAnalyzer zawierają blok `CRITICAL:`, który zapobiega łączeniu kart luk.
- Sprawdź limit tokenów modelu - `gpt-4.1-mini` obsługuje do 32K tokenów wyjściowych, co powinno wystarczyć.

---

## Wskazówki dotyczące wydajności

### Wolne odpowiedzi

Przepływy pracy z wieloma agentami są z natury wolniejsze niż pojedynczy agent z powodu zależności sekwencyjnych i wywołań narzędzia MCP.

| Optymalizacja | Jak | Wpływ |
|---------------|-----|-------|
| Zmniejsz liczbę wywołań MCP | Obniż parametr `max_results` w narzędziu | Mniej zapytań HTTP |
| Uprość instrukcje | Krótsze, bardziej skoncentrowane polecenia dla agenta | Szybsze wnioskowanie LLM |
| Używaj `gpt-4.1-mini` | Szybszy niż `gpt-4.1` podczas rozwoju | Około 2x szybsze |
| Zmniejsz szczegółowość kart luk | Uprość format kart luk w instrukcjach GapAnalyzer | Mniej generowanego wyjścia |

### Typowe czasy odpowiedzi (lokalnie)

| Konfiguracja | Oczekiwany czas |
|--------------|-----------------|
| `gpt-4.1-mini`, 3-5 kart luk | 30-60 sekund |
| `gpt-4.1-mini`, 8+ kart luk | 60-120 sekund |
| `gpt-4.1`, 3-5 kart luk | 60-120 sekund |
---

## Uzyskanie pomocy

Jeśli utkniesz po wypróbowaniu powyższych poprawek:

1. **Sprawdź logi serwera** - Większość błędów generuje w terminalu ślad stosu Pythona. Przeczytaj cały traceback.
2. **Wyszukaj komunikat o błędzie** - Skopiuj tekst błędu i wyszukaj w [Microsoft Q&A dla Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Otwórz zgłoszenie** - Zgłoś problem w [repozytorium warsztatów](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) wraz z:
   - Komunikatem o błędzie lub zrzutem ekranu
   - Wersjami pakietów (`pip list | Select-String "agent-framework"`)
   - Twoją wersją Pythona (`python --version`)
   - Informacją, czy problem występuje lokalnie, czy po wdrożeniu

---

### Kontrola

- [ ] Potrafisz zidentyfikować i naprawić najczęstsze błędy wieloagentowe, korzystając z tabeli szybkiego odniesienia
- [ ] Wiesz, jak sprawdzić i naprawić problemy z konfiguracją `.env`
- [ ] Potrafisz zweryfikować, czy wersje pakietów odpowiadają wymaganej macierzy
- [ ] Rozumiesz wpisy w logach MCP i potrafisz diagnozować awarie narzędzi
- [ ] Wiesz, jak sprawdzić logi kontenerów w przypadku niepowodzeń wdrożenia
- [ ] Potrafisz zweryfikować role RBAC w Azure Portal

---

**Poprzedni:** [07 - Verify in Playground](07-verify-in-playground.md) · **Strona główna:** [Lab 02 README](../README.md) · [Strona główna warsztatów](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:  
Dokument ten został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w jego języku źródłowym powinien być uważany za wiarygodne źródło. W przypadku informacji krytycznych zaleca się skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z korzystania z tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->