# Moduł 8 - Rozwiązywanie problemów

Ten moduł to przewodnik referencyjny po typowych problemach. Dodaj go do zakładek i wracaj, gdy coś pójdzie nie tak.

---

## 1. Błędy uprawnień

### 1.1 Brak uprawnienia `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Przyczyna:** Brak roli `Azure AI User` na poziomie **projektu**. To błąd nr 1 na warsztatach.

**Naprawa:**
1. Otwórz [portal.azure.com](https://portal.azure.com).
2. Wyszukaj nazwę swojego **projektu** Foundry → kliknij wynik typu **"Microsoft Foundry project"** (NIE konto nadrzędne).
3. **Kontrola dostępu (IAM)** → **+ Dodaj** → **Dodaj przypisanie roli**.
4. Rola: **Azure AI User** → Dalej.
5. Członkowie: Wybierz siebie → Przejrzyj + przypisz → Przejrzyj + przypisz.
6. **Poczekaj 1–2 minuty** → spróbuj ponownie.

> **Dlaczego Owner/Contributor nie wystarcza:** Te role umożliwiają jedynie działania *zarządcze*. Operacje agenta wymagają *akcji danych* `agents/write`, która jest dostępna tylko w `Azure AI User`, `Azure AI Developer` lub `Azure AI Owner`. Zobacz [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` podczas provisioning

**Naprawa:** Poproś administratora o przypisanie roli **Contributor** na grupie zasobów lub, aby utworzył projekt dla Ciebie i nadał Ci **Azure AI User**.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Czekaj aż: "Zarejestrowany"
```

---

## 2. Błędy Dockera

> Docker jest **opcjonalny**. Poniższe dotyczą tylko, jeśli zainstalowano Docker Desktop i rozszerzenie próbuje wykonać lokalną kompilację.

### 2.1 Docker daemon nie działa

**Naprawa:** Uruchom Docker Desktop → poczekaj na status "running" → sprawdź poleceniem `docker info` → spróbuj ponownie.

### 2.2 Kompilacja nie powiodła się z powodu błędów zależności

**Naprawa:** Sprawdź pisownię `requirements.txt`, najpierw przetestuj lokalnie: `pip install -r requirements.txt`.

### 2.3 Niezgodność platformy (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Błędy uwierzytelniania

### 3.1 `DefaultAzureCredential` nie działa

**Naprawa (spróbuj po kolei):**
1. `az login` (ponowne uwierzytelnienie)
2. `az account set --subscription "<id>"` (prawidłowe subskrypcje)
3. VS Code → Konta → Wyloguj się → Zaloguj się ponownie
4. Sprawdź: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token działa lokalnie, ale nie na hostingu

**Oczekiwane:** Hostowane agenty używają tożsamości zarządzanej przez system, nie Twoich poświadczeń. Jeśli hostowany agent ma błędy uwierzytelniania:
- Sprawdź, czy `AZURE_AI_PROJECT_ENDPOINT` w `agent.yaml` jest poprawny
- Upewnij się, że tożsamość zarządzana projektu ma dostęp do modelu

---

## 4. Błędy modelu

### 4.1 Nie znaleziono wdrożenia modelu

**Naprawa:** Nazwa jest **wrażliwa na wielkość liter**. Porównaj `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` z dokładną nazwą w panelu bocznym Foundry → Modele.

### 4.2 Nieoczekiwany wynik modelu

**Naprawa:** Przejrzyj `AGENT_INSTRUCTIONS` w `main.py` (czy nie jest ucięty?). Spróbuj inny model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Błędy wdrożenia

### 5.1 Brak autoryzacji pobierania ACR

**Naprawa:** Portal Azure → Rejestr kontenerów → Kontrola dostępu (IAM) → Dodaj rolę **AcrPull** do tożsamości zarządzanej projektu Foundry.

### 5.2 Agent nie uruchamia się (pozostaje "Oczekujący" lub "Nie powiodło się")

Sprawdź logi kontenera w panelu bocznym. Typowe przyczyny:

| Komunikat w logu | Naprawa |
|-----------------|--------|
| `ModuleNotFoundError` | Dodaj brakujący pakiet do `requirements.txt`, wdroż ponownie |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Dodaj zmienną środowiskową w `agent.yaml` pod `environment_variables` |
| `Address already in use` | Upewnij się, że tylko jeden proces nasłuchuje na porcie 8088 |

### 5.3 Wdrożenie przekracza limit czasu

**Naprawa:** Sprawdź połączenie internetowe. Pierwsze wdrożenie przesyła >100MB. Za proxy? Skonfiguruj ustawienia proxy w Docker Desktop.

---

## 6. Ścieżka B - Foundry Local

### 6.1 Foundry Local się nie uruchamia

| Problem | Naprawa |
|---------|---------|
| `foundry: command not found` | Zainstaluj ponownie: `winget install Microsoft.FoundryLocal` |
| Niewystarczające zasoby | Foundry Local potrzebuje ~4GB wolnej pamięci RAM. Zamknij inne aplikacje. |
| Pobieranie modelu nie powiodło się | Sprawdź miejsce na dysku (modele zajmują 2–8 GB). Spróbuj ponownie: `foundry local models pull <name>` |

### 6.2 Błędy modelu Foundry Local

| Problem | Naprawa |
|---------|---------|
| Wolne odpowiedzi | Oczekiwane - modele lokalne działają na CPU, jeśli nie masz GPU. Bądź cierpliwy. |
| Niska jakość wyników | Spróbuj większy model, jeśli Twoje zasoby na to pozwalają. `phi-4-mini` to dobry kompromis. |
| Połączenie odrzucone | Sprawdź, czy Foundry Local działa: `foundry local status`. Uruchom ponownie, jeśli trzeba. |

---

## 7. Szybkie odniesienie: role RBAC

| Rola | Zakres | Uprawnienia |
|------|--------|------------|
| **Azure AI User** | Projekt | Akcje danych: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Akcje danych + tworzenie projektu |
| **Azure AI Owner** | Konto | Pełny dostęp + zarządzanie rolami |
| **Contributor** | Subskrypcja/GR | Tylko akcje zarządcze (**bez** akcji danych) |
| **Owner** | Subskrypcja/GR | Zarządzanie + przypisywanie ról (**bez** akcji danych) |

---

## 8. Lista kontrolna ukończenia warsztatów

| # | Element | Moduł |
|---|--------|--------|
| 1 | Zainstalowano i zweryfikowano wymagania wstępne | [00](00-prerequisites.md) |
| 2 | Zainstalowano rozszerzenie Foundry Toolkit, projekt połączony (lub skonfigurowana Ścieżka B) | [01](01-setup.md) |
| 3 | Utworzono hostowanego agenta | [02](02-create-hosted-agent.md) |
| 4 | Skonfigurowano `.env`, napisano instrukcje, zainstalowano zależności | [03](03-configure-and-code.md) |
| 5 | Przetestowano agenta lokalnie - 3 funkcjonalne scenariusze przeszły | [04](04-test-locally.md) |
| 6 | Wdrożono do Foundry (tylko Ścieżka A) | [05](05-deploy-to-foundry.md) |
| 7 | Testy skrajnych przypadków/bezpieczeństwa przeszły w chmurze (tylko Ścieżka A) | [06](06-verify-in-playground.md) |
| 8 | Przejrzano podsumowanie, określono kolejne kroki | [07](07-summary.md) |

---

**Poprzedni:** [07 - Podsumowanie](07-summary.md) · **Strona główna:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->