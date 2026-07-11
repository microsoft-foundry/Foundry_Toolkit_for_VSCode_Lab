# Jak przeprowadzić tę sesję

Dziękujemy za przeprowadzenie tej sesji!

Przed przeprowadzeniem warsztatu, proszę:

1. Przeczytać ten dokument i wszystkie załączone zasoby w całości.
2. Obejrzeć nagranie z dostarczenia sesji oraz pełne przejście przez warsztat.
3. Przejść oba laboratoria praktyczne na własnym komputerze **przynajmniej raz** przed wydarzeniem.
4. Zweryfikować swój projekt Microsoft Foundry, wdrożenia modeli i limity.
5. Skontaktować się z opiekunem, jeśli coś jest niejasne.

---

## Podsumowanie plików

| Zasób                        | Link                                                                             | Opis                                                                                      |
|------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Prezentacja warsztatu         | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Slajdy prezentacji warsztatu z notatkami prowadzącego i wbudowanymi filmami demonstracyjnymi|
| Nagranie sesji                | _Do dostarczenia przez opiekuna_                                               | Nagranie wprowadzenia do warsztatu i przeglądu slajdów                                    |
| Nagranie całego warsztatu     | _Do dostarczenia przez opiekuna_                                               | Nagranie całych laboratoriów z perspektywy uczestnika                                     |
| Dokumentacja warsztatu        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repozytorium źródłowe, pliki README laboratoriów, moduły krok po kroku                     |
| Lab 01 - pojedynczy agent     | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Laboratorium praktyczne: budowa, test i wdrożenie *Explain Like I'm an Executive* hostowanego agenta |
| Lab 02 - workflow wieloagentowy | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Laboratorium praktyczne: budowa workflow 4-agentowego *Resume to Job Fit Evaluator*        |
| Demo 1: Executive Agent       | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Demo z Lab 01: tłumaczenie żargonu technicznego na streszczenie dla zarządu                |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demo z Lab 02: workflow 4-agentowy oceniający dopasowanie CV do pracy i generujący rekomendacje |

> **Uwaga dla trenerów:** Prezentacja i linki do nagrań zostaną dodane po publikacji nagrań. Do tego czasu prosimy kontaktować się z opiekunem (patrz [Kontakt](#kontakty)) w celu uzyskania najnowszych materiałów.

---

## Rozpoczęcie

Ten warsztat uczy programistów, jak budować, testować i wdrażać agentów AI do **Microsoft Foundry Agent Service** jako **hostowanych agentów** całkowicie z poziomu VS Code, korzystając z rozszerzenia **Microsoft Foundry Toolkit**.

Warsztat jest podzielony na kilka sekcji, w tym slajdy, **2 prezentacje na żywo** oraz **2 laboratoria praktyczne**.

### Harmonogram

#### Pełna sesja (około 2 godziny)

| Czas            | Opis                                                             |
|-----------------|------------------------------------------------------------------|
| 0:00 - 10:00    | Wprowadzenie: hostowani agenci, Foundry Agent Service i toolkit  |
| 10:00 - 20:00   | Demo: Executive Agent od początku do końca                       |
| 20:00 - 60:00   | Lab 01 - pojedynczy agent (budowa, lokalne testy, wdrożenie, plac zabaw) |
| 60:00 - 110:00  | Lab 02 - workflow wieloagentowy (Resume to Job Fit Evaluator)    |
| 110:00 - 120:00 | Podsumowanie, pytania i odpowiedzi oraz materiały do dalszej nauki |

#### Skrócona sesja (około 75 minut)

| Czas          | Opis                                                |
|---------------|----------------------------------------------------|
| 0:00 - 10:00  | Wprowadzenie i przegląd                            |
| 10:00 - 20:00 | Demo: Executive Agent                              |
| 20:00 - 70:00 | Tylko Lab 01 (wskazanie Lab 02 jako samodzielne)  |
| 70:00 - 75:00 | Podsumowanie i pytania                             |

### Przygotowanie

| Zasób                        | Link                                                                                          | Opis                                               |
|-------------------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------|
| Dokumentacja warsztatu       | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Dokumentacja i źródło warsztatu                      |
| Instrukcje do Lab 01         | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Laboratorium praktyczne: pojedynczy hostowany agent |
| Instrukcje do Lab 02         | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Laboratorium praktyczne: workflow wieloagentowy      |
| Lista wymagań wstępnych     | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Niezbędne narzędzia, konta i dostęp do Azure         |
| Szybki start hostowanych agentów (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Oficjalny szybki start wdrażania hostowanego agenta przez `azd` |
| Dostępność regionów hostowanych agentów | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Wspierane regiony dla hostowanych agentów (wersja zapoznawcza) |

### Wymagania dla trenera

Przed przeprowadzeniem upewnij się, że masz:

- **Subskrypcję Azure** z uprawnieniami do tworzenia zasobów (właściciel lub współautor na grupie zasobów).
- Dostęp do **projektu Microsoft Foundry** w [regionie obsługującym hostowanych agentów](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Limit dla **gpt-4.1** (lub **gpt-4.1-mini**) w Twoim projekcie Foundry.
- Zainstalowane następujące narzędzia:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Rozszerzenie Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (opcjonalnie)
  - Python 3.10 lub nowszy

Uruchom [Hosted agents quickstart z `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) przynajmniej raz przed sesją, aby mieć sprawdzony projekt Foundry, wdrożenie modelu i rejestr Azure Container Registry do odwołań, jeśli uczestnik napotka problem.

---

## Przegląd slajdów

Prezentacja podąża tym samym schematem co laboratoria. Sugerowane punkty do omówienia dla każdej sekcji:

| Sekcja                      | Kluczowy przekaz                                                                                            |
|-----------------------------|------------------------------------------------------------------------------------------------------------|
| Tytuł i agenda              | Przedstaw warsztat jako *VS Code do Foundry* bez potrzeby przełączania się między portalami.              |
| Dlaczego hostowani agenci? | Zarządzane środowisko wykonawcze, wdrożenie oparte na ACR, kompatybilny z OpenAI API `/responses`, związany z projektami Foundry. |
| Diagram architektury        | Omów [architekturę z README](../README.md#architecture): szkielet, Inspektor, ACR, Agent Service.           |
| Budowa hostowanego agenta  | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - co robi każdy plik.                             |
| Demo na żywo: Executive Agent | Przełącz się do VS Code i uruchom demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) od początku do końca (patrz [Demo 1](#demo-1-executive-agent)). |
| Demo na żywo: Resume to Job Fit Evaluator | Przełącz się do VS Code i uruchom demo 4-agentowe [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (patrz [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Skrót Lab 01               | Przekaż uczestnikom. Wskaż [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Wzorce wieloagentowe       | Sekwencyjne vs równoległe vs przekazywanie - podgląd przed rozpoczęciem Lab 02.                             |
| Skrót Lab 02               | Przekaż uczestnikom. Wskaż [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Podsumowanie i zasoby      | Linki do dalszej nauki z sekcji [Dodatkowe zasoby](#dodatkowe-zasoby).                                 |

---

## Dema

W sesji zawarte są dwie demonstracje na żywo, każda po 10 minut.

| Demo                 | Lab   | Pliki                                                      | Co pokazać                                          |
|----------------------|-------|------------------------------------------------------------|----------------------------------------------------|
| Executive Agent      | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Pojedynczy hostowany agent; tłumaczenie żargonu technicznego na streszczenie dla zarządu |
| Resume to Job Fit Evaluator | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orkiestracja 4-agentowa; ocena dopasowania CV do pracy i generowanie rekomendacji |

### Demo 1: Executive Agent

Samodzielny agent w [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Użyj tego jako 10-minutowego demo przed Lab 01.

1. Otwórz [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) i przejdź przez definicję agenta (prompt systemowy, model, framework).
2. Naciśnij `F5`, aby uruchomić **Agent Inspector** lokalnie.
3. Wklej przykładowy prompt z [README](../README.md#see-it-in-action) i pokaż odpowiedź w formie podsumowania dla zarządu.
4. Pokaż [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) oraz [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile), aby wyjaśnić artefakty wdrożenia.
5. Zaprezentuj proces wdrażania (budowanie Dockera, push do ACR, tworzenie hostowanego agenta) bez czekania na zakończenie.

### Demo 2: Resume to Job Fit Evaluator

Workflow 4-agentowy w [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Użyj tego jako 10-minutowego demo przed Lab 02.

1. Otwórz [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) i pokaż, jak cztery agenty są połączone sekwencyjnie.
2. Naciśnij `F5`, aby uruchomić **Agent Inspector** dla workflow wieloagentowego.
3. Wklej krótki opis stanowiska i przykładowe CV w czat Inspektora.
4. Przeprowadź przez czteroagentową linię produkcyjną: parser CV, ekstraktor wymagań pracy, oceniacz dopasowania i generator rekomendacji.
5. Wskaż, jak output każdego sub-agenta staje się kontekstem dla kolejnego agenta, podkreślając wzorzec przekazywania.
6. Pokaż [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml), aby porównać z odpowiednikiem z Demonstracji 1 (pojedynczy agent).

---

## Wskazówki do prowadzenia

- **Ustal oczekiwania na wstępie.** Hostowani agenci są w wersji zapoznawczej – poinformuj o ograniczeniach regionalnych i limitach na początku, aby uczestnicy nie byli zaskoczeni w trakcie laboratorium.
- **Najpierw wykonaj zadanie weryfikacji wymagań.** Oba laboratoria zawierają zadanie VS Code „Validate prerequisites” – poproś uczestników o jego uruchomienie zanim zaczną pisać kod.
- **Utrzymuj widoczność Agent Inspector.** Większość momentów „aha” dzieje się, gdy uczestnicy widzą świecące, lokalne `/responses`.
- **Miej projekt zapasowy.** Jeśli projekt Foundry uczestnika napotka limit, udostępnij wcześniej przygotowany projekt do kroku wdrożenia zamiast blokować całą grupę.
- **Dobieraj uczestników parami.** Lab 02 (wieloagentowe) jest znacząco łatwiejsze, gdy uczestnicy mogą omówić orkiestrację z partnerem.
- **Używaj modułów dokumentacji jako punktów kontrolnych.** Każde laboratorium ma folder `docs/` podzielony na 8 ponumerowanych modułów – wykorzystaj je jako naturalne miejsca na przerwy.
- **Wstępnie pobierz bazowy obraz Docker** na wspólnych maszynach labowych, aby uniknąć limitów rejestru.

---

## Rozwiązywanie problemów podczas prowadzenia

| Objaw                                          | Pierwsza rzecz do wypróbowania                                                                             |
|------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Agent Inspector nie może się połączyć           | Sprawdź, czy port `8088` jest wolny i czy zadanie `Run Lab01 HTTP Server` lub `Run Lab02 HTTP Server` działa.|
| Debugger nie chce się podłączyć                   | Sprawdź, czy port `5679` jest wolny; zrestartuj VS Code, jeśli `debugpy` już nasłuchuje.                    |
| `azd up` zwraca błąd uwierzytelnienia            | Uruchom `az login` oraz `azd auth login`, upewnij się, że jest wybrany właściwy tenant.                     |
| Wdrożenie zatrzymuje się na puszczaniu do ACR     | Sprawdź, czy działa Docker Desktop i czy użytkownik ma uprawnienia `AcrPush` na rejestrze.                 |
| Model zwraca 404 / deployment-not-found           | Nazwa wdrożenia modelu w `agent.yaml` musi zgadzać się z wdrożeniem w projekcie Foundry.                    |

| Hostowany agent utknął w `Provisioning`         | Sprawdź, czy region projektu [obsługuje hostowanych agentów](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) oraz czy dostępne są limity. |
| Playground zwraca 401                       | Ponownie uwierzytelnij rozszerzenie Foundry z paska aktywności VS Code.                                     |

Dla głębszych wskazówek, każdy laboratorium zawiera swój własny dokument `08-troubleshooting.md` - skieruj do niego uczestników:

- Laboratorium 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Laboratorium 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Dostosowywanie tej sesji

Zachęcamy do dostosowania warsztatu dla swojej publiczności. Popularne warianty:

- **Dla odbiorców backendowych:** spędź więcej czasu na `agent.yaml`, Dockerze i ACR; skróć demo playground.
- **Dla programistów obywatelskich:** pozostań w interfejsie rozszerzenia Foundry do szkieletowania; zmniejsz ilość kroków w CLI.
- **Jednoszlakowy 60-minutowy slot:** dostarcz tylko wprowadzenie, demo i Laboratorium 01.
- **Format tylko warsztatowy (bez slajdów):** otwórz oba README laboratoriów i używaj ich jako głównego scenariusza.

Jeśli rozszerzasz laboratoria, prosimy o wniesienie zmian poprzez PR, aby skorzystali inni trenerzy.

---

## Dodatkowe zasoby

- [Dokumentacja Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Przegląd hostowanych agentów](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Szybki start: wdroż swój pierwszy hostowany agent (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Wdrożenie hostowanego agenta (instrukcja)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit dla VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontakty

Jeśli masz pytania dotyczące prowadzenia tej sesji, prosimy o otwarcie zgłoszenia na [repozytorium warsztatu](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) i oznaczenie opiekuna.

| Rola                | Imię           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Opiekun / kontakt   | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->