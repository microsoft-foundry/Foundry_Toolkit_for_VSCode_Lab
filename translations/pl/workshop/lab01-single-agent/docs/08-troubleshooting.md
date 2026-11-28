# Moduł 8 - Rozwiązywanie problemów

Ten moduł jest przewodnikiem referencyjnym po typowych problemach. Dodaj go do zakładek i wróć, gdy coś pójdzie nie tak.

---

## 1. Błędy związane z uprawnieniami

### 1.1 `agents/write` odmowa dostępu

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Przyczyna:** Brak roli `Azure AI User` na poziomie **projektu**. To jest #1 błąd warsztatów.

**Naprawa:**
1. Otwórz [portal.azure.com](https://portal.azure.com).
2. Wyszukaj nazwę swojego **projektu** Foundry → kliknij wynik typu **"Microsoft Foundry project"** (NIE konto nadrzędne).
3. **Kontrola dostępu (IAM)** → **+ Dodaj** → **Dodaj przypisanie roli**.
4. Rola: **Azure AI User** → Dalej.
5. Członkowie: wybierz siebie → Przejrzyj + przypisz → Przejrzyj + przypisz.
6. **Poczekaj 1–2 minuty** → spróbuj ponownie.

> **Dlaczego Owner/Contributor to za mało:** Te role przyznają tylko działania *zarządcze*. Operacje agenta wymagają `agents/write` *operacji na danych*, które są dostępne tylko w `Azure AI User`, `Azure AI Developer` lub `Azure AI Owner`. Zobacz [dokumentację Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` podczas uruchamiania

**Naprawa:** Poproś administratora o przypisanie roli **Contributor** do grupy zasobów lub niech utworzy projekt dla Ciebie i nada Ci rolę **Azure AI User**.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Błędy Dockera

> Docker jest **opcjonalny**. Dotyczy to tylko, jeśli Docker Desktop jest zainstalowany, a rozszerzenie próbuje lokalnie zbudować obraz.

### 2.1 Demon Dockera nie działa

**Naprawa:** Uruchom Docker Desktop → poczekaj na status "running" → sprawdź za pomocą `docker info` → spróbuj ponownie.

### 2.2 Budowanie nie powiodło się z błędami zależności

**Naprawa:** Sprawdź pisownię `requirements.txt`, najpierw przetestuj lokalnie: `pip install -r requirements.txt`.

### 2.3 Niezgodność platformy (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Błędy uwierzytelniania

### 3.1 Nie powiodło się `DefaultAzureCredential`

**Naprawa (spróbuj po kolei):**
1. `az login` (ponowne uwierzytelnienie)
2. `az account set --subscription "<id>"` (poprawna subskrypcja)
3. VS Code → Konta → Wyloguj się → Zaloguj się ponownie
4. Sprawdź: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token działa lokalnie, ale nie na hostingu

**Oczekiwane:** Hostowani agenci używają tożsamości zarządzanej przez system, nie Twoich poświadczeń. Jeśli hostowany agent otrzymuje błędy uwierzytelniania:
- Sprawdź, czy `AZURE_AI_MODEL_DEPLOYMENT_NAME` w `agent.yaml` odpowiada nazwie wdrożenia modelu (`FOUNDRY_PROJECT_ENDPOINT` jest wstrzykiwany przez Foundry podczas uruchamiania — nie deklaruj go w `agent.yaml`)
- Upewnij się, że tożsamość zarządzana projektu ma dostęp do modelu

---

## 4. Błędy modelu

### 4.1 Nie znaleziono wdrożenia modelu

**Naprawa:** Nazwa jest **wrażliwa na wielkość liter**. Porównaj `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` z dokładną nazwą w panelu Foundry → Modele.

### 4.2 Nieoczekiwany wynik modelu

**Naprawa:** Sprawdź `AGENT_INSTRUCTIONS` w `main.py` (nie jest obcięty?). Spróbuj inny model (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Błędy wdrożenia

### 5.1 Brak uprawnienia do pobrania z ACR

**Naprawa:** Portal Azure → Rejestr Kontenerów → Kontrola dostępu (IAM) → dodaj rolę **AcrPull** do zarządzanej tożsamości projektu Foundry.

### 5.2 Agent nie uruchamia się (pozostaje "Pending" lub "Failed")

Sprawdź logi kontenera w panelu bocznym. Typowe przyczyny:

| Komunikat w logu | Naprawa |
|-----------------|--------|
| `ModuleNotFoundError` | Dodaj brakujący pakiet do `requirements.txt`, wdroż ponownie |
| `ValueError: Missing required environment variables` | Potwierdź, że `AZURE_AI_MODEL_DEPLOYMENT_NAME` jest zadeklarowany w `agent.yaml` pod `environment_variables` i ma wartość, następnie wdroż ponownie. `FOUNDRY_PROJECT_ENDPOINT` jest wstrzykiwany przez Foundry podczas uruchamiania |
| `Address already in use` | Upewnij się, że tylko jeden proces korzysta z portu 8088 |

### 5.3 Wdrożenie przekracza czas oczekiwania

**Naprawa:** Sprawdź połączenie internetowe. Pierwsze wdrożenie przesyła >100MB. Jesteś za proxy? Skonfiguruj ustawienia proxy w Docker Desktop.

---

## 6. Ścieżka B - Foundry Local

### 6.1 Foundry Local nie chce się uruchomić

| Problem | Naprawa |
|---------|---------|
| `foundry: command not found` | Zainstaluj ponownie: `winget install Microsoft.FoundryLocal` |
| Niewystarczające zasoby | Foundry Local potrzebuje ~4GB wolnej pamięci RAM. Zamknij inne aplikacje. |
| Pobieranie modelu się nie powiodło | Sprawdź miejsce na dysku (modele mają 2–8 GB). Spróbuj ponownie: `foundry local models pull <name>` |

### 6.2 Błędy modeli w Foundry Local

| Problem | Naprawa |
|---------|---------|
| Wolne odpowiedzi | Oczekiwane - lokalne modele działają na CPU, chyba że masz GPU. Bądź cierpliwy. |
| Słaba jakość wyników | Spróbuj większego modelu, jeśli pozwala na to twoje sprzętowe wyposażenie. `phi-4-mini` to dobry kompromis. |
| Połączenie odrzucone | Sprawdź, czy Foundry Local działa: `foundry local status`. Uruchom ponownie w razie potrzeby. |

---

## 7. Skrócony przegląd: role RBAC

| Rola | Zakres | Uprawnienia |
|------|--------|-------------|
| **Azure AI User** | Projekt | Operacje na danych: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projekt/Konto | Operacje na danych + tworzenie projektów |
| **Azure AI Owner** | Konto | Pełny dostęp + zarządzanie rolami |
| **Contributor** | Subskrypcja/GR | Tylko działania zarządcze (**bez** operacji na danych) |
| **Owner** | Subskrypcja/GR | Zarządzanie + przypisywanie ról (**bez** operacji na danych) |

---

## 8. Lista kontrolna ukończenia warsztatu

| # | Element | Moduł |
|---|---------|--------|
| 1 | Wymagania wstępne zainstalowane i zweryfikowane | [00](00-prerequisites.md) |
| 2 | Rozszerzenie Foundry Toolkit zainstalowane, projekt połączony (lub Konfiguracja Ścieżki B) | [01](01-setup.md) |
| 3 | Hostowany agent utworzony | [02](02-create-hosted-agent.md) |
| 4 | `.env` skonfigurowany, instrukcje napisane, zależności zainstalowane | [03](03-configure-and-code.md) |
| 5 | Agent przetestowany lokalnie - 3 scenariusze funkcjonalne zaliczone | [04](04-test-locally.md) |
| 6 | Wdrożony do Foundry (tylko Ścieżka A) | [05](05-deploy-to-foundry.md) |
| 7 | Testy krawędziowe/bezpieczeństwa przeszły w chmurze (tylko Ścieżka A) | [06](06-verify-in-playground.md) |
| 8 | Podsumowanie przeglądnięte, zidentyfikowano dalsze kroki | [07](07-summary.md) |

---

**Poprzedni:** [07 - Podsumowanie](07-summary.md) · **Strona główna:** [README warsztatów](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->