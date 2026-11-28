# Moduł 8 - Rozwiązywanie problemów

Ten moduł obejmuje typowe błędy, poprawki i strategie debugowania specyficzne dla przepływu pracy wieloagentowej.

## Problemy z outputem agenta

### GapAnalyzer mówi „Wciąż nie mam dopasowanego raportu”

**Objaw:** Odpowiedź GapAnalyzer prosi cię o wklejenie dopasowanego raportu z „Brakującymi umiejętnościami” i „Lukami w certyfikacji”. Dzieje się tak nawet wtedy, gdy wysłałeś zarówno CV, jak i opis stanowiska.

**Przyczyna:** Tekst JD nie został przekazany dalej do agenta JD. W `context_mode="last_agent"`, `resume_executor` jest jedynym wykonawcą, który kiedykolwiek widzi oryginalną wiadomość użytkownika. Jeśli `RESUME_PARSER_INSTRUCTIONS` nie zawiera tekstu JD w swojej odpowiedzi, agent JD nie ma JD do analizowania, MatchingAgent nie może obliczyć oceny dopasowania, a GapAnalyzer otrzymuje bezwartościowe dane wejściowe.

**Diagnoza:**

W logach serwera poszukaj zakresu MatchingAgent. Jeśli zawiera:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
brak przejścia lub jest ono uszkodzone.

**Naprawa:** Potwierdź, że `RESUME_PARSER_INSTRUCTIONS` w `main.py` zawiera sekcję `[JOB DESCRIPTION PASS-THROUGH]` oraz regułę:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Potwierdź również, że `JOB_DESCRIPTION_INSTRUCTIONS` zawiera regułę przekazywania `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jeśli którykolwiek z bloków instrukcji jest szkieletem ze kreatora szablonów, zastąp go kompletną wersją z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent zwraca „Nie można obliczyć oceny dopasowania - JD nie dostarczono”

To ten sam podstawowy problem jak wyżej. MatchingAgent otrzymał wyjście agenta JD, ale sekcja `[PARSED RESUME PASS-THROUGH]` była pusta lub brakowało jej, więc nie mógł porównać dwóch profili. Potwierdź:
1. `JOB_DESCRIPTION_INSTRUCTIONS` zawiera regułę przekazywania: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` mówi agentowi, aby szukał sekcji `[JD REQUIREMENTS]` i `[PARSED RESUME PASS-THROUGH]`.

Zamień oba bloki instrukcji na kompletne wersje z [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Odpowiedź pojawia się dwukrotnie

**Objaw:** Output GapAnalyzer (lub cały output potoku) pojawia się dwukrotnie w odpowiedzi Inspektora Agenta.

**Przyczyna:** `WorkflowBuilder` używa semantyki LUB dla nadchodzących krawędzi - wykonawca niższego poziomu uruchamia się, gdy ukończy się **którykolwiek** z poprzedników. Jeśli `matching_executor` ma dwa nadchodzące połączenia (jedno z `resume_executor` i drugie z `jd_executor`), uruchomi się dwa razy: raz po zakończeniu ResumeParser, drugi raz po zakończeniu agenta JD. GapAnalyzer wtedy także działa dwukrotnie.

**Naprawa:** Upewnij się, że graf `WorkflowBuilder` to wyłącznie sekwencyjny potok bez ściągania:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jeśli masz zbędną linię `.add_edge(resume_executor, matching_executor)`, usuń ją. Przekaźnik `[PARSED RESUME PASS-THROUGH]` w wyjściu agenta JD już zapewnia dostęp MatchingAgent do CV.

---

## Problemy środowiskowe i konfiguracyjne

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

**Ścieżka B - Foundry lokalne:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Obie ścieżki używają `FOUNDRY_PROJECT_ENDPOINT`. Wartość się różni: chmura korzysta z punktu końcowego Foundry `https://`; lokalne z `http://localhost:5273/v1`. Uruchom `foundry model list`, aby potwierdzić dokładny alias modelu dla Ścieżki B.

> **Znajdowanie swojego `FOUNDRY_PROJECT_ENDPOINT`:** 
- Otwórz **Foundry Toolkit** w pasku bocznym VS Code → kliknij prawym przyciskiem projekt → **Kopiuj punkt końcowy projektu**. 
- Lub przejdź do [Azure Portal](https://portal.azure.com) → swój projekt Foundry → **Przegląd** → **Punkt końcowy projektu**.

> **Znajdowanie swojego `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** W pasku bocznym Foundry Toolkit rozwiń projekt → **Modele** → znajdź nazwę wdrożonego modelu (np. `gpt-4.1-mini`).

### Priorytet zmiennych środowiskowych

`main.py` używa `load_dotenv(override=True)`, co oznacza:

| Priorytet | Źródło | Wygrywa, gdy oba ustawione? |
|----------|--------|--------------------------|
| 1 (najwyższy) | Plik `.env` | Tak |
| 2 | Zmienna środowiskowa powłoki/kontenera | Używana gdy ten sam klucz nie występuje w `.env` |

W lokalnym środowisku deweloperskim `.env` jest źródłem prawdy (edycja `.env` natychmiast wpływa na uruchomienia). W wdrożeniu hostowanym Foundry wstrzykuje zmienne środowiskowe na poziomie kontenera; ponieważ `.env` nie jest częścią wdrożonego obrazu w tym zestawie laboratoryjnym, używane są wstrzyknięte wartości kontenera.

---

## Kompatybilność wersji

### Matryca wersji pakietów

Przepływ pracy wieloagentowej wymaga określonych wersji pakietów. Niezgodność wersji powoduje błędy czasu wykonywania.

| Pakiet | Wymagana wersja | Komenda do sprawdzenia |
|--------|-----------------|-----------------------|
| `agent-framework-foundry` | najnowsza | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | najnowsza | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | najnowsza | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Typowe błędy wersji

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Sprawdź wszystkie wersje jednocześnie

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Oczekiwany output:

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
   - Otwórz pasek boczny **Foundry Toolkit** → pod swoim projektem kliknij **Agenci** → zakładka **Hosted Agent** → kliknij swojego agenta. Sprawdź **Status** na zakładce **Szczegóły**, następnie otwórz zakładkę **Place zabaw** i użyj zakładki **Logi** w panelu **Szczegóły sesji**, aby zobaczyć output kontenera.
   - Szukaj śladów stosów Pythona lub błędów braku modułów.

2. **Typowe przyczyny niepowodzenia startu kontenera:**

   | Błąd w logach | Przyczyna | Naprawa |
   |--------------|----------|--------|
   | `ModuleNotFoundError` | `requirements.txt` brak pakietu | Dodaj pakiet, ponownie wdroż |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` lub `.env` zmienne środowiskowe nie ustawione | Zaktualizuj sekcję `agent.yaml` → `environment_variables` (hostowane) lub `.env` (lokalne) |
   | `azure.identity.CredentialUnavailableError` | Nie skonfigurowano Managed Identity | Foundry ustawia to automatycznie - upewnij się, że wdrażasz za pomocą rozszerzenia |
   | `OSError: port 8088 already in use` | Dockerfile ujawnia nieprawidłowy port lub konflikt portu | Zweryfikuj `EXPOSE 8088` w Dockerfile i `CMD ["python", "main.py"]` |
   | Kontener zakończył się kodem 1 | Nieobsłużony wyjątek w `main()` | Najpierw testuj lokalnie ([Moduł 5](05-test-locally.md)), aby wychwycić błędy przed wdrożeniem |

3. **Wdroż ponownie po naprawie:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → wybierz tego samego agenta → wdroż nową wersję.

### Wdrożenie trwa zbyt długo

Kontenery multi-agentowe startują wolniej, ponieważ tworzą 4 instancje agenta podczas uruchamiania. Normalny czas startu:

| Etap | Oczekiwany czas trwania |
|-------|---------------------|
| Budowa obrazu kontenera | 1-3 minuty |
| Wypchnięcie obrazu do ACR | 30-60 sekund |
| Start kontenera (pojedynczy agent) | 15-30 sekund |
| Start kontenera (multi-agent) | 30-120 sekund |
| Agent dostępny w Place zabaw | 1-2 minuty po „Uruchomiono” |

> Jeśli status „Oczekujący” utrzymuje się dłużej niż 5 minut, sprawdź logi kontenera pod kątem błędów.

---

## Problemy z RBAC i uprawnieniami

### `403 Forbidden` lub `AuthorizationFailed`

Potrzebujesz roli **[Foundry User](https://aka.ms/foundry-ext-project-role)** w swoim projekcie Foundry (wcześniej nazywana **Azure AI User** - identyfikator roli bez zmian):

1. Przejdź do [Azure Portal](https://portal.azure.com) → zasób twojego projektu **Foundry**.
2. Kliknij **Access control (IAM)** → **Role assignments**.
3. Wyszukaj swoje imię → potwierdź, że na liście jest **Foundry User** (lub przestarzała etykieta **Azure AI User**).
4. Jeśli brak: **Dodaj** → **Dodaj przypisanie roli** → wyszukaj **Foundry User** → przypisz na swoje konto.

Zobacz dokumentację [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) po szczegóły.

### Brak dostępu do wdrożenia modelu

Jeśli agent zwraca błędy związane z modelem:

1. Sprawdź, czy model jest wdrożony: pasek boczny Foundry → rozwiń projekt → **Models** → sprawdź obecność `gpt-4.1-mini` (lub twojego modelu) ze statusem **Succeeded**.
2. Sprawdź zgodność nazwy wdrożenia: porównaj `AZURE_AI_MODEL_DEPLOYMENT_NAME` w `.env` (lub `agent.yaml`) z rzeczywistą nazwą wdrożenia w pasku bocznym.
3. Jeśli wdrożenie wygasło (w warstwie darmowej): wdroż ponownie z [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemy z Foundry Local (Ścieżka B)

### Usługa Foundry Local nie działa

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Objaw | Przyczyna | Rozwiązanie |
|---------|-------|-----|
| Health check zwraca `503` | Usługa nie została uruchomiona | `foundry local start` lub kliknij **Start** w pasku bocznym Foundry Toolkit |
| Health check wygasa | Model nadal się ładuje | Poczekaj 30–60 s po uruchomieniu; większe modele ładują się dłużej |
| `StatusCode: 404` na `/v1/health` | Błędny port | Domyślnie to `5273`. Sprawdź `foundry local status` w celu znalezienia aktualnego portu |
| Niewystarczające zasoby | Foundry Local potrzebuje ~4 GB wolnej pamięci RAM | Zamknij inne aplikacje |
| Pobieranie modelu nie powiodło się | Mała ilość miejsca na dysku | Modele zajmują 2–8 GB. Zwolnij miejsce, następnie `foundry model pull <name>` |

### Niezgodność nazwy modelu

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Ustaw `AZURE_AI_MODEL_DEPLOYMENT_NAME` w `.env` dokładnie na alias pokazany (np. `phi-4-mini`, a nie `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` podczas lokalnego uruchomienia (Ścieżka B)

Laboratorium `main.py` korzysta z `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local wymaga, aby ta zmienna wskazywała lokalną usługę - **nie** `AZURE_AI_PROJECT_ENDPOINT`. Upewnij się, że twoje `.env` zawiera:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Narzędzie MCP nadal wykonuje połączenie wychodzące (Ścieżka B)

To normalne. Narzędzie `search_microsoft_learn_for_plan` pobiera zasoby edukacyjne z `https://learn.microsoft.com/api/mcp`. **Tylko zapytanie o nazwę umiejętności** jest przesyłane przez sieć - tekst CV i opisu stanowiska jest przetwarzany całkowicie na twoim urządzeniu i nigdy nie jest przesyłany. Jeśli wymagana jest pełna praca offline, dodaj w narzędziu fallback `try/except`, który zwraca statyczny `learn.microsoft.com` URL, gdy punkt końcowy jest nieosiągalny.

---

## Uzyskiwanie pomocy

Jeśli utkniesz po próbach powyższych napraw:

1. **Sprawdź logi serwera** - Większość błędów generuje ślad stosu Pythona w terminalu. Przeczytaj cały traceback.
2. **Wyszukaj komunikat o błędzie** - Skopiuj tekst błędu i wyszukaj w [Microsoft Q&A for Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Zgłoś problem** - Załóż zgłoszenie w [repozytorium warsztatów](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) zawierające:
   - Komunikat o błędzie lub zrzut ekranu
   - Twoje wersje pakietów (`pip list | Select-String "agent-framework"`)
   - Twoją wersję Pythona (`python --version`)
   - Czy problem występuje lokalnie, czy po wdrożeniu

---

### Punkt kontrolny

- [ ] Wiesz, jak sprawdzić i naprawić problemy z konfiguracją `.env`
- [ ] Potrafisz zweryfikować wersje pakietów zgodne z wymaganą matrycą
- [ ] Wiesz, jak sprawdzić logi kontenera w przypadku niepowodzenia wdrożenia
- [ ] Potrafisz zweryfikować role RBAC w Azure Portal

---

**Poprzedni:** [07 - Verify in Playground](07-verify-in-playground.md) · **Następny:** [09 - Summary →](09-summary.md) · **Strona główna:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->