# Moduł 8 - Rozwiązywanie problemów

Ten moduł obejmuje typowe błędy, poprawki i strategie debugowania specyficzne dla wieloagentowego przepływu pracy.

## Problemy z wyjściem agenta

### GapAnalyzer mówi „Wciąż nie mam pasującego raportu”

**Objaw:** Odpowiedź GapAnalyzera prosi o wklejenie pasującego raportu z „Brakującymi umiejętnościami” i „Lukami w certyfikacji”. Dzieje się tak nawet wtedy, gdy wysłano zarówno CV, jak i opis stanowiska.

**Przyczyna:** Tekst JD nie został przekazany dalej do agenta JD. Przy `context_mode="last_agent"` `resume_executor` jest jedynym wykonawcą, który kiedykolwiek widzi oryginalną wiadomość użytkownika. Jeśli `RESUME_PARSER_INSTRUCTIONS` nie zawiera tekstu JD w swoim wyjściu, agent JD nie ma JD do parsowania, MatchingAgent nie może obliczyć wyniku dopasowania, a GapAnalyzer otrzymuje bezsensowne dane wejściowe.

**Diagnoza:**

W logach serwera poszukaj zakresu MatchingAgent. Jeśli zawiera:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
to przekazywanie jest brakujące lub uszkodzone.

**Naprawa:** Potwierdź, że `RESUME_PARSER_INSTRUCTIONS` w `main.py` zawiera sekcję `[JOB DESCRIPTION PASS-THROUGH]` oraz regułę:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Potwierdź także, że `JOB_DESCRIPTION_INSTRUCTIONS` zawiera regułę przekaźnikową `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jeśli którykolwiek blok instrukcji jest szkieletem z kreatora szablonów, zastąp go pełną wersją z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent wyświetla „Nie można obliczyć wyniku dopasowania - nie podano JD”

To ta sama podstawowa przyczyna co wyżej. MatchingAgent otrzymał wyjście agenta JD, ale sekcja `[PARSED RESUME PASS-THROUGH]` była brakująca lub pusta, więc nie mógł porównać dwóch profili. Potwierdź:
1. `JOB_DESCRIPTION_INSTRUCTIONS` zawiera regułę przekaźnikową: `Skopiuj [PARSED RESUME] dosłownie - Matching Agent zależy od tego w dalszych etapach.`
2. `MATCHING_AGENT_INSTRUCTIONS` nakazuje agentowi szukać sekcji `[JD REQUIREMENTS]` i `[PARSED RESUME PASS-THROUGH]`.

Zamień oba bloki instrukcji na pełne wersje z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odpowiedź pojawia się dwukrotnie

**Objaw:** Wyjście GapAnalyzera (lub całe wyjście potoku) pojawia się dwukrotnie w odpowiedzi Agenta w Inspektorze.

**Przyczyna:** `WorkflowBuilder` używa semantyki LUB dla nadchodzących krawędzi - wykonawca uruchamia się, gdy **jakikolwiek** poprzednik zakończy działanie. Jeśli `matching_executor` ma dwie nadchodzące krawędzie (jedną z `resume_executor` i jedną z `jd_executor`), uruchamia się dwukrotnie: raz po zakończeniu ResumeParsera i ponownie po zakończeniu agenta JD. GapAnalyzer również wtedy działa dwukrotnie.

**Naprawa:** Upewnij się, że graf `WorkflowBuilder` jest ściśle sekwencyjnym potokiem bez fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NIE z resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jeśli masz luźną linię `.add_edge(resume_executor, matching_executor)`, usuń ją. Przekaźnik `[PARSED RESUME PASS-THROUGH]` w wyjściu agenta JD już udostępnia MatchingAgentowi dostęp do CV.

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

**Ścieżka A - chmura Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Ścieżka B - Foundry lokalnie:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Obie ścieżki używają `FOUNDRY_PROJECT_ENDPOINT`. Wartość jest różna: chmura używa punktu końcowego Foundry `https://`; lokalnie `http://localhost:5273/v1`. Uruchom `foundry model list`, aby potwierdzić dokładny alias modelu dla Ścieżki B.

> **Znajdowanie `FOUNDRY_PROJECT_ENDPOINT`:**
- Otwórz pasek boczny **Foundry Toolkit** w VS Code → kliknij prawym przyciskiem projekt → **Copy Project Endpoint**.
- Lub przejdź do [Azure Portal](https://portal.azure.com) → projekt Foundry → **Overview** → **Project endpoint**.

> **Znajdowanie `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** W pasku bocznym Foundry Toolkit rozwiń projekt → **Models** → znajdź nazwę wdrożonego modelu (np. `gpt-4.1-mini`).

### Priorytet zmiennych środowiskowych

`main.py` używa `load_dotenv(override=True)`, co oznacza:

| Priorytet | Źródło | Wygrywa, gdy oba są ustawione? |
|----------|--------|-------------------------------|
| 1 (najwyższy) | Plik `.env` | Tak |
| 2 | Zmienna środowiskowa powłoki/kontenera | Używana, gdy ten sam klucz nie jest obecny w `.env` |

W lokalnym rozwoju `.env` jest źródłem prawdy (edycja `.env` natychmiast wpływa na uruchomienia). W wdrożeniu hostowanym Foundry wstrzykuje zmienne środowiskowe na poziomie kontenera; ponieważ `.env` nie jest częścią wdrożonego obrazu w tym laboratorium, używane są wartości kontenera.

---

## Zgodność wersji

### Macierz wersji pakietów

Wieloagentowy przepływ pracy wymaga określonych wersji pakietów. Niekompatybilne wersje powodują błędy podczas działania.

| Pakiet | Wymagana wersja | Komenda sprawdzająca |
|--------|-----------------|---------------------|
| `agent-framework-foundry` | najnowsza | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | najnowsza | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | najnowsza | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Typowe błędy wersji

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Poprawka: ponowna instalacja agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Poprawka: uaktualnij pakiet mcp
pip install mcp --upgrade
```

### Zweryfikuj wszystkie wersje naraz

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Oczekiwane wyjście:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problemy z wdrożeniem

### Kontener nie uruchamia się po wdrożeniu

1. **Sprawdź logi kontenera:**
   - Otwórz pasek boczny **Foundry Toolkit** → rozwiń **Hosted Agents (Preview)** → kliknij swojego agenta → rozwiń wersję → **Container Details** → **Logs**.
   - Szukaj śladów stosu Pythona lub błędów brakujących modułów.

2. **Typowe przyczyny niepowodzenia startu kontenera:**

   | Błąd w logach | Przyczyna | Naprawa |
   |--------------|----------|--------|
   | `ModuleNotFoundError` | Brak pakietu w `requirements.txt` | Dodaj pakiet, wdroż ponownie |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | W `agent.yaml` lub `.env` brak zmiennych środowiskowych | Zaktualizuj sekcję `environment_variables` w `agent.yaml` (hostowane) lub `.env` (lokalne) |
   | `azure.identity.CredentialUnavailableError` | Nie skonfigurowano Managed Identity | Foundry robi to automatycznie - upewnij się, że wdrażasz przez rozszerzenie |
   | `OSError: port 8088 already in use` | Dockerfile udostępnia zły port lub kolizja portu | Sprawdź `EXPOSE 8088` w Dockerfile i `CMD ["python", "main.py"]` |
   | Kontener kończy się kodem 1 | Nieobsłużony wyjątek w `main()` | Najpierw testuj lokalnie ([Moduł 5](05-test-locally.md)) by łapać błędy przed wdrożeniem |

3. **Wdroż ponownie po naprawie:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → wybierz tego samego agenta → wdroż nową wersję.

### Wdrożenie zajmuje zbyt długo

Kontenery wieloagentowe potrzebują więcej czasu na start, bo tworzą 4 instancje agentów przy starcie. Normalne czasy startu:

| Etap | Oczekiwany czas trwania |
|-------|----------------------|
| Budowa obrazu kontenera | 1-3 minuty |
| Wypychanie obrazu do ACR | 30-60 sekund |
| Start kontenera (pojedynczy agent) | 15-30 sekund |
| Start kontenera (wieloagentowy) | 30-120 sekund |
| Agent dostępny na Playground | 1-2 minuty po statusie „Started” |

> Jeśli status „Pending” trwa ponad 5 minut, sprawdź logi kontenera pod kątem błędów.

---

## Problemy z RBAC i uprawnieniami

### `403 Forbidden` lub `AuthorizationFailed`

Potrzebujesz roli **[Foundry User](https://aka.ms/foundry-ext-project-role)** w projekcie Foundry (dawniej nazywana **Azure AI User** - identyfikator roli bez zmian):

1. Przejdź do [Azure Portal](https://portal.azure.com) → zasób projektu Foundry.
2. Kliknij **Access control (IAM)** → **Role assignments**.
3. Wyszukaj swoje imię → potwierdź, że jest wymieniona rola **Foundry User** (lub starsza etykieta **Azure AI User**).
4. Jeśli brakuje: **Dodaj** → **Add role assignment** → wyszukaj **Foundry User** → przypisz do swojego konta.

Szczegóły znajdziesz w dokumentacji [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### Wdrożony model jest niedostępny

Jeśli agent zwraca błędy związane z modelem:

1. Zweryfikuj, że model jest wdrożony: pasek boczny Foundry → rozwiń projekt → **Models** → sprawdź `gpt-4.1-mini` (lub swój model) ze statusem **Succeeded**.
2. Sprawdź, czy nazwa wdrożenia pasuje: porównaj `AZURE_AI_MODEL_DEPLOYMENT_NAME` w `.env` (lub `agent.yaml`) z faktyczną nazwą wdrożenia z paska bocznego.
3. Jeśli wdrożenie wygasło (darmowy poziom): wdroż ponownie z [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemy z Foundry Local (Ścieżka B)

### Usługa Foundry Local nie działa

```powershell
# Sprawdź status
foundry local status

# Uruchom usługę, jeśli jest zatrzymana
foundry local start
```

| Objaw | Przyczyna | Naprawa |
|-------|----------|--------|
| Kontrola stanu zwraca `503` | Usługa nie została uruchomiona | `foundry local start` lub kliknij **Start** w pasku bocznym Foundry Toolkit |
| Kontrola stanu przekroczyła limit czasu | Model nadal się ładuje | Poczekaj 30–60 s po starcie; większe modele ładują się dłużej |
| `StatusCode: 404` na `/v1/health` | Zły port | Domyślny to `5273`. Sprawdź `foundry local status` dla aktualnego portu |
| Niewystarczające zasoby | Foundry Local potrzebuje ~4 GB wolnej pamięci RAM | Zamknij inne aplikacje |
| Pobieranie modelu nie powiodło się | Mało miejsca na dysku | Modele ważą 2–8 GB. Zwolnij miejsce, potem `foundry model pull <name>` |

### Niedopasowanie nazwy modelu

```powershell
# Wymień pobrane modele i ich dokładne aliasy
foundry model list
```

Ustaw `AZURE_AI_MODEL_DEPLOYMENT_NAME` w `.env` na dokładny alias podany (np. `phi-4-mini`, nie `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` przy lokalnym uruchomieniu (Ścieżka B)

W laboratorium `main.py` używa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local wymaga, aby ta zmienna wskazywała na lokalną usługę - **nie** na `AZURE_AI_PROJECT_ENDPOINT`. Upewnij się, że Twoje `.env` zawiera:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP tool nadal wykonuje wywołanie zewnętrzne (Ścieżka B)

To jest spodziewane. Narzędzie `search_microsoft_learn_for_plan` pobiera zasoby edukacyjne z `https://learn.microsoft.com/api/mcp`. **Tylko zapytanie o nazwę umiejętności** jest przesyłane przez sieć - CV i tekst JD są przetwarzane w całości na Twoim urządzeniu i nigdy nie są transmitowane. Jeśli wymagana jest całkowicie offline praca, dodaj `try/except` z fallbackiem w narzędziu, który zwraca statyczny URL `learn.microsoft.com` gdy punkt końcowy jest niedostępny.

---

## Uzyskiwanie pomocy

Jeśli utkniesz po próbach powyższych poprawek:

1. **Sprawdź logi serwera** - Większość błędów generuje ślad stosu Pythona w terminalu. Przeczytaj cały traceback.
2. **Wyszukaj komunikat błędu** - Skopiuj tekst błędu i poszukaj w [Microsoft Q&A dla Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Zgłoś problem** - Utwórz zgłoszenie w repozytorium [workshopu](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) zawierające:
   - Komunikat błędu lub zrzut ekranu
   - Twoje wersje pakietów (`pip list | Select-String "agent-framework"`)
   - Wersję Pythona (`python --version`)
   - Informację, czy problem pojawia się lokalnie, czy po wdrożeniu

---

### Punkt kontrolny

- [ ] Wiesz, jak sprawdzić i naprawić problemy z konfiguracją `.env`
- [ ] Potrafisz zweryfikować, czy wersje pakietów pasują do wymaganej macierzy
- [ ] Wiesz, jak sprawdzić logi kontenerów w przypadku błędów wdrożenia
- [ ] Potrafisz zweryfikować role RBAC w Azure Portal

---

**Poprzedni:** [07 - Weryfikacja w Playground](07-verify-in-playground.md) · **Następny:** [09 - Podsumowanie →](09-summary.md) · **Start:** [Lab 02 README](../README.md) · [Strona warsztatów](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->