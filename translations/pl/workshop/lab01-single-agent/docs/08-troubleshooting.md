# Moduł 8 - Rozwiązywanie problemów

Ten moduł jest przewodnikiem referencyjnym dla każdego powszechnego problemu napotkanego podczas warsztatów. Dodaj go do zakładek — wrócisz do niego za każdym razem, gdy coś pójdzie nie tak.

---

## 1. Błędy uprawnień

### 1.1 Odmowa uprawnień `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Przyczyna:** Nie masz roli `Azure AI User` na poziomie **projektu**. To jest najczęstszy błąd podczas warsztatów.

**Naprawa - krok po kroku:**

1. Otwórz [https://portal.azure.com](https://portal.azure.com).
2. W górnym pasku wyszukiwania wpisz nazwę swojego **projektu Foundry** (np. `workshop-agents`).
3. **Krytyczne:** Kliknij wynik, który pokazuje typ **"Microsoft Foundry project"**, NIE nadrzędne konto/hub zasobu. To są różne zasoby z różnymi zakresami RBAC.
4. Po lewej stronie na stronie projektu kliknij **Kontrola dostępu (IAM)**.
5. Kliknij zakładkę **Przypisania ról**, aby sprawdzić, czy masz już rolę:
   - Wyszukaj swoje imię lub adres e-mail.
   - Jeśli `Azure AI User` jest już na liście → błąd ma inną przyczynę (sprawdź punkt 8 poniżej).
   - Jeśli nie ma na liście → przejdź do dodania roli.
6. Kliknij **+ Dodaj** → **Dodaj przypisanie roli**.
7. Na karcie **Rola**:
   - Wyszukaj [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Wybierz ją z wyników.
   - Kliknij **Dalej**.
8. W karcie **Członkowie**:
   - Wybierz **Użytkownik, grupa lub podmiot usługi**.
   - Kliknij **+ Wybierz członków**.
   - Wyszukaj swoje imię lub adres e-mail.
   - Wybierz siebie z wyników.
   - Kliknij **Wybierz**.
9. Kliknij **Przejrzyj + przydziel** → ponownie **Przejrzyj + przydziel**.
10. **Poczekaj 1-2 minuty** - zmiany RBAC potrzebują czasu na propagację.
11. Spróbuj ponownie wykonać operację, która nie powiodła się.

> **Dlaczego rola Owner/Contributor nie wystarcza:** Azure RBAC ma dwa rodzaje uprawnień - *akcje zarządzania* i *akcje danych*. Owner i Contributor przyznają akcje zarządzania (tworzenie zasobów, edycja ustawień), ale operacje agenta wymagają akcji danych `agents/write`, która jest dostępna tylko w rolach `Azure AI User`, `Azure AI Developer` lub `Azure AI Owner`. Zobacz [dokumentację Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` podczas tworzenia zasobu

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Przyczyna:** Nie masz uprawnień do tworzenia lub modyfikowania zasobów Azure w tej subskrypcji/grupie zasobów.

**Naprawa:**
1. Poproś administratora subskrypcji o przypisanie Ci roli **Contributor** w grupie zasobów, w której znajduje się Twój projekt Foundry.
2. Alternatywnie poproś, aby stworzył projekt Foundry za Ciebie i nadał Ci rolę **Azure AI User** na tym projekcie.

### 1.3 `SubscriptionNotRegistered` dla [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Przyczyna:** Subskrypcja Azure nie zarejestrowała dostawcy zasobów potrzebnego dla Foundry.

**Naprawa:**

1. Otwórz terminal i uruchom:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Poczekaj na zakończenie rejestracji (może potrwać 1-5 minut):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Oczekiwany wynik: `"Registered"`
3. Spróbuj ponownie wykonać operację.

---

## 2. Błędy Dockera (tylko jeśli Docker jest zainstalowany)

> Docker jest **opcjonalny** dla tych warsztatów. Te błędy dotyczą tylko sytuacji, gdy masz zainstalowany Docker Desktop i rozszerzenie Foundry próbuje lokalnie zbudować kontener.

### 2.1 Demon Dockera nie działa

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Naprawa - krok po kroku:**

1. **Znajdź Docker Desktop** w menu Start (Windows) lub w folderze Aplikacje (macOS) i uruchom go.
2. Poczekaj, aż okno Docker Desktop wyświetli komunikat **„Docker Desktop is running”** - zazwyczaj trwa to 30-60 sekund.
3. Sprawdź ikonę wieloryba Dockera na pasku systemowym (Windows) lub w pasku menu (macOS). Najedź kursorem, aby potwierdzić status.
4. Zweryfikuj w terminalu:
   ```powershell
   docker info
   ```
   Jeśli zostanie wyświetlona informacja o systemie Docker (wersja serwera, sterownik magazynu itd.), Docker działa.
5. **Specyficzne dla Windows:** Jeśli Docker nadal się nie uruchamia:
   - Otwórz Docker Desktop → **Ustawienia** (ikona koła zębatego) → **Ogólne**.
   - Upewnij się, że jest zaznaczone **Use the WSL 2 based engine**.
   - Kliknij **Zastosuj i uruchom ponownie**.
   - Jeśli WSL 2 nie jest zainstalowany, uruchom `wsl --install` w podniesionym PowerShell i zrestartuj komputer.
6. Spróbuj ponownie wdrożyć.

### 2.2 Budowa Dockera nie powiodła się z powodu błędów zależności

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Naprawa:**
1. Otwórz plik `requirements.txt` i sprawdź, czy wszystkie nazwy pakietów są poprawnie zapisane.
2. Upewnij się, że ustalenie wersji jest poprawne:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Przetestuj instalację lokalnie najpierw:
   ```bash
   pip install -r requirements.txt
   ```
4. Jeśli używasz prywatnego indeksu pakietów, upewnij się, że Docker ma do niego dostęp sieciowy.

### 2.3 Niezgodność platformy kontenera (Apple Silicon)

Jeśli wdrażasz z komputera Mac Apple Silicon (M1/M2/M3/M4), kontener musi być zbudowany dla `linux/amd64`, ponieważ środowisko uruchomieniowe Foundry używa AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Polecenie wdrażania w rozszerzeniu Foundry automatycznie obsługuje to w większości przypadków. Jeśli pojawią się błędy związane z architekturą, zbuduj ręcznie z flagą `--platform` i skontaktuj się z zespołem Foundry.

---

## 3. Błędy uwierzytelniania

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) nie może pobrać tokenu

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Przyczyna:** Żadne z źródeł uwierzytelniania w łańcuchu `DefaultAzureCredential` nie ma ważnego tokenu.

**Naprawa - przejdź przez kroki po kolei:**

1. **Zaloguj się ponownie przez Azure CLI** (najczęściej działające rozwiązanie):
   ```bash
   az login
   ```
   Otworzy się okno przeglądarki. Zaloguj się, a następnie wróć do VS Code.

2. **Ustaw poprawną subskrypcję:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Jeśli to nie jest właściwa subskrypcja:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Zaloguj się ponownie przez VS Code:**
   - Kliknij ikonę **Konta** (ikona osoby) w lewym dolnym rogu VS Code.
   - Kliknij swoje konto → **Wyloguj się**.
   - Kliknij ponownie ikonę konta → **Zaloguj się do Microsoft**.
   - Dokończ logowanie w przeglądarce.

4. **Podmiot usługi (tylko scenariusze CI/CD):**
   - Ustaw te zmienne środowiskowe w pliku `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Następnie uruchom ponownie proces agenta.

5. **Sprawdź pamięć podręczną tokenów:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Jeśli nie powiodło się, token CLI wygasł. Uruchom ponownie `az login`.

### 3.2 Token działa lokalnie, ale nie w wdrożeniu hostowanym

**Przyczyna:** Agent hostowany używa tożsamości zarządzanej przez system, która różni się od twoich osobistych poświadczeń.

**Naprawa:** To jest oczekiwane zachowanie - tożsamość zarządzana jest automatycznie przypisywana podczas wdrożenia. Jeśli agent hostowany nadal ma błędy uwierzytelniania:
1. Sprawdź, czy tożsamość zarządzana projektu Foundry ma dostęp do zasobu Azure OpenAI.
2. Zweryfikuj, czy `PROJECT_ENDPOINT` w `agent.yaml` jest poprawny.

---

## 4. Błędy modeli

### 4.1 Nie znaleziono wdrożenia modelu

```
Error: Model deployment not found / The specified deployment does not exist
```

**Naprawa - krok po kroku:**

1. Otwórz swój plik `.env` i zanotuj wartość `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Otwórz boczny pasek **Microsoft Foundry** w VS Code.
3. Rozwiń swój projekt → **Model Deployments** (wdrożenia modeli).
4. Porównaj nazwę wdrożenia tam wyświetlaną z wartością w `.env`.
5. Nazwa jest **wrażliwa na wielkość liter** - `gpt-4o` różni się od `GPT-4o`.
6. Jeśli się nie zgadzają, zaktualizuj `.env`, używając dokładnie takiej nazwy jak w bocznym pasku.
7. Dla wdrożenia hostowanego, także zaktualizuj `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model odpowiada nieoczekiwaną treścią

**Naprawa:**
1. Sprawdź stałą `EXECUTIVE_AGENT_INSTRUCTIONS` w `main.py`. Upewnij się, że nie została ucięta lub uszkodzona.
2. Sprawdź ustawienie temperatury modelu (jeśli jest konfigurowalne) - niższe wartości dają bardziej deterministyczne wyniki.
3. Porównaj użyty model (np. `gpt-4o` vs `gpt-4o-mini`) - różne modele mają różne możliwości.

---

## 5. Błędy wdrożeń

### 5.1 Autoryzacja pobierania z ACR

```
Error: AcrPullUnauthorized
```

**Przyczyna:** Tożsamość zarządzana projektu Foundry nie może pobrać obrazu kontenera z Azure Container Registry.

**Naprawa - krok po kroku:**

1. Otwórz [https://portal.azure.com](https://portal.azure.com).
2. W pasku wyszukiwania wpisz **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)**.
3. Kliknij na rejestr powiązany z Twoim projektem Foundry (zazwyczaj jest w tej samej grupie zasobów).
4. Po lewej stronie kliknij **Kontrola dostępu (IAM)**.
5. Kliknij **+ Dodaj** → **Dodaj przypisanie roli**.
6. Wyszukaj i wybierz **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Kliknij **Dalej**.
7. Wybierz **Tożsamość zarządzana** → kliknij **+ Wybierz członków**.
8. Znajdź i wybierz tożsamość zarządzaną projektu Foundry.
9. Kliknij **Wybierz** → **Przejrzyj + przydziel** → **Przejrzyj + przydziel**.

> To przypisanie roli jest zwykle konfigurowane automatycznie przez rozszerzenie Foundry. Jeśli widzisz ten błąd, automatyczna konfiguracja mogła się nie powieść. Możesz też spróbować ponownie wdrożyć — rozszerzenie może powtórzyć konfigurację.

### 5.2 Agent nie uruchamia się po wdrożeniu

**Objawy:** Status kontenera pozostaje “Pending” dłużej niż 5 minut lub pokazuje “Failed”.

**Naprawa - krok po kroku:**

1. Otwórz boczny pasek **Microsoft Foundry** w VS Code.
2. Kliknij swojego hostowanego agenta → wybierz wersję.
3. W panelu szczegółów sprawdź **Szczegóły kontenera** → poszukaj sekcji lub linku **Logi**.
4. Przeczytaj logi uruchomienia kontenera. Częste przyczyny:

| Komunikat w logu | Przyczyna | Naprawa |
|------------------|-----------|---------|
| `ModuleNotFoundError: No module named 'xxx'` | Brakująca zależność | Dodaj ją do `requirements.txt` i wdroż ponownie |
| `KeyError: 'PROJECT_ENDPOINT'` | Brakująca zmienna środowiskowa | Dodaj zmienną do `agent.yaml` w sekcji `env:` |
| `OSError: [Errno 98] Address already in use` | Konflikt portu | Upewnij się, że w `agent.yaml` jest `port: 8088` i tylko jeden proces korzysta z tego portu |
| `ConnectionRefusedError` | Agent nie zaczął nasłuchiwać | Sprawdź `main.py` - wywołanie `from_agent_framework()` musi się uruchomić podczas startu |

5. Napraw problem, a następnie wdroż ponownie zgodnie z [Modułem 6](06-deploy-to-foundry.md).

### 5.3 Wdrożenie przekracza limit czasu

**Naprawa:**
1. Sprawdź swoje połączenie internetowe - wysyłanie Dockera może być duże (>100MB przy pierwszym wdrożeniu).
2. Jeśli jesteś za korporacyjnym proxy, upewnij się, że ustawienia proxy Dockera są poprawne: **Docker Desktop** → **Ustawienia** → **Zasoby** → **Proxies**.
3. Spróbuj ponownie - problemy sieciowe mogą powodować przejściowe błędy.

---

## 6. Szybka ściąga: Role RBAC

| Rola | Typowy zakres | Co zapewnia |
|-------|--------------|-------------|
| **Azure AI User** | Projekt | Akcje danych: budowanie, wdrażanie i wywoływanie agentów (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projekt lub konto | Akcje danych + tworzenie projektów |
| **Azure AI Owner** | Konto | Pełny dostęp + zarządzanie przypisaniami ról |
| **Azure AI Project Manager** | Projekt | Akcje danych + możliwość przypisywania roli Azure AI User innym |
| **Contributor** | Subskrypcja/grupa zasobów | Akcje zarządzania (tworzenie/usuwanie zasobów). **Nie obejmuje akcji danych** |
| **Owner** | Subskrypcja/grupa zasobów | Akcje zarządzania + przypisywanie ról. **Nie obejmuje akcji danych** |
| **Reader** | Dowolny | Tylko do odczytu dostęp zarządzania |

> **Najważniejsze:** Roli `Owner` i `Contributor` **NIE** obejmują akcje danych. Zawsze potrzebujesz roli `Azure AI *` dla operacji agenta. Minimalna rola dla tych warsztatów to **Azure AI User** na poziomie **projektu**.

---

## 7. Lista kontrolna ukończenia warsztatów

Użyj tego jako ostateczne potwierdzenie, że ukończyłeś wszystko:

| # | Element | Moduł | Zaliczone? |
|---|---------|-------|------------|
| 1 | Wszystkie wymagania wstępne zainstalowane i zweryfikowane | [00](00-prerequisites.md) | |
| 2 | Narzędzia Foundry Toolkit i rozszerzenia Foundry zainstalowane | [01](01-install-foundry-toolkit.md) | |
| 3 | Projekt Foundry utworzony (lub wybrany istniejący projekt) | [02](02-create-foundry-project.md) | |
| 4 | Model wdrożony (np. gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Przypisana rola użytkownika Azure AI na poziomie projektu | [02](02-create-foundry-project.md) | |
| 6 | Szablon projektu hostowanego agenta (agent/) utworzony | [03](03-create-hosted-agent.md) | |
| 7 | `.env` skonfigurowany z PROJECT_ENDPOINT i MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instrukcje agenta dostosowane w main.py | [04](04-configure-and-code.md) | |
| 9 | Utworzone wirtualne środowisko i zainstalowane zależności | [04](04-configure-and-code.md) | |
| 10 | Agent przetestowany lokalnie za pomocą F5 lub terminala (zaliczone 4 testy dymne) | [05](05-test-locally.md) | |
| 11 | Wdrożony do Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Status kontenera pokazuje „Started” lub „Running” | [06](06-deploy-to-foundry.md) | |
| 13 | Zweryfikowany w VS Code Playground (zaliczone 4 testy dymne) | [07](07-verify-in-playground.md) | |
| 14 | Zweryfikowany w Foundry Portal Playground (zaliczone 4 testy dymne) | [07](07-verify-in-playground.md) | |

> **Gratulacje!** Jeśli wszystkie pozycje zostały zaznaczone, zakończyłeś cały warsztat. Zbudowałeś hostowanego agenta od podstaw, przetestowałeś go lokalnie, wdrożyłeś do Microsoft Foundry i zweryfikowałeś w środowisku produkcyjnym.

---

**Poprzedni:** [07 - Verify in Playground](07-verify-in-playground.md) · **Strona główna:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:  
Dokument ten został przetłumaczony za pomocą automatycznej usługi tłumaczeniowej AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dążymy do dokładności, prosimy pamiętać, że tłumaczenia automatyczne mogą zawierać błędy lub nieścisłości. Oryginalny dokument w języku źródłowym powinien być traktowany jako źródło autorytatywne. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->