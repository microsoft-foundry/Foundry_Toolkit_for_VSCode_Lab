# Moduł 2 - Szkielet projektu wieloagentowego

⏱️ ~5 minut

W tym module używasz [Foundry Toolkit for VS Code](https://aka.ms/foundrytk), aby **utworzyć szkielet projektu wieloagentowego**. Kreator generuje `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env` oraz konfigurację debugowania w VS Code — dzięki czemu możesz skupić się na połączeniu przepływu pracy 4-agentowego w Module 3.

> **Kluczowa koncepcja:** Szkielet to działający stub z jednym agentem. W Module 3 zastępujesz logikę zastępczą grafem `WorkflowBuilder`. Nie piszesz szablonu od zera.

> **Implementacja referencyjna:** [`PersonalCareerCopilot/`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot) to kompletny działający przykład. Użyj go do porównania swojej pracy na bieżąco.

### Przebieg kreatora szkieletu

```mermaid
flowchart LR
    A[Command Palette: Create New Hosted Agent] --> B[Language: Python]
    B --> C[API Type: Response API]
    C --> D[Template: Workflows]
    D --> E[Select Model]
    E --> F[Workspace Folder and Agent Name]
    F --> G[Generated Project]
```

---

## Krok 1: Otwórz kreatora Create Hosted Agent

1. Naciśnij `Ctrl+Shift+P`, aby otworzyć **Paletę poleceń**.
2. Wpisz: **Foundry Toolkit: Create new Hosted Agent** i wybierz to polecenie.
3. Kreator otworzy się na karcie **Agent Details**.

> **Alternatywa:** Kliknij ikonę **Foundry Toolkit** na pasku aktywności → kliknij ikonę **+** obok **Hosted Agents** → **Create New Hosted Agent**.

---

## Krok 2: Wybierz ustawienia

![Create Hosted Agent from Sample - karta Agent Details z wybraną szablonem Workflows](../../../../../translated_images/pl/02-scaffold-wizard-details.af4798708b4a87f4.webp)

1. W lewym panelu nawigacji/opcji wybierz:

| Menu | Wybór | Uwagi |
|--------|-----------|-------|
| **Language** | Python | Obsługiwany jest też C# (.NET) |
| **Framework** | Agent Framework | Zapewnia `Agent`, `AgentExecutor`, `WorkflowBuilder` |
| **API type** | Response API | `POST /responses` - historia zarządzana przez platformę, wsparcie streamingowe |
| **Template** | **Workflows** | Przetwarza żądania sekwencyjnie przez wielu agentów |

2. Po wyborze kliknij **Next**

![Create Hosted Agent from Sample - karta Create z nazwą folderu PersonalCareerCopilot](../../../../../translated_images/pl/02-scaffold-wizard-create.ae0c285c309698ba.webp)

3. W następnym oknie wybierz:

| Menu | Wybór | Uwagi |
|--------|-----------|-------|
| **Workspace folder** | Przeglądaj do docelowego folderu | np. `workshop/lab02-multi-agent/` w tym repozytorium |
| **Agent name** | `PersonalCareerCopilot` | To stanie się nazwą folderu projektu |
| **Model Deployment** | Wybierz swój wdrożony model | np. `gpt-4.1-mini` z Laboratorium 01 |

4. Kliknij **Create**, aby utworzyć szkielet projektu. VS Code wygeneruje pliki i otworzy folder.

> **Wskazówka:** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series) dobrze równoważy szybkość i jakość dla rozwoju wieloagentowego.

---

## Krok 3: Sprawdź wygenerowany projekt

Po zakończeniu tworzenia szkieletu upewnij się, że w Eksploratorze (`Ctrl+Shift+E`) widzisz następujące pliki:

```
📂 <your-agent-name>/
├── .azdignore          ← Files excluded from Azure Developer CLI deployments
├── .dockerignore       ← Files excluded from Docker builds
├── .env                ← Environment variables (placeholders - fill in Module 3)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted, protocol: responses)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Stub agent entry point (replace with WorkflowBuilder in Module 3)
└── requirements.txt    ← Python dependencies
```

> **Ważne:** Otwórz ten folder ze szkieletem bezpośrednio w VS Code, aby `.vscode/launch.json` i `tasks.json` działały poprawnie podczas debugowania przez F5.

### Wyjaśnienie kluczowych plików

| Plik | Przeznaczenie |
|------|-------------|
| `agent.yaml` | Deklaruje `kind: hosted`, mapuje zmienne środowiskowe, definiuje protokół `/responses` |
| `main.py` | Stub: jeden `FoundryChatClient` → `Agent` → `ResponsesHostServer`. W Module 3 zastąpisz to 4 agentami + `WorkflowBuilder` |
| `Dockerfile` | `python:3.12-slim`, instaluje `requirements.txt`, udostępnia port 8088, uruchamia `python main.py` |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp<2,>=1.24.0`, `debugpy` |

> **Referencja:** Zobacz [`PersonalCareerCopilot/agent.yaml`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) i [`PersonalCareerCopilot/requirements.txt`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/requirements.txt) dla pełnej zawartości wygenerowanej.

---

### ✅ Punkt kontrolny

- [ ] Kreator szkieletu ukończony – nowy folder projektu widoczny w Eksploratorze
- [ ] Wszystkie oczekiwane pliki obecne: `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`
- [ ] `agent.yaml` pokazuje `kind: hosted` i `protocol: responses`
- [ ] `main.py` importuje `Agent`, `FoundryChatClient`, `ResponsesHostServer`
- [ ] Folder ze szkieletem jest otwarty jako główny folder roboczy VS Code
- [ ] Rozumiesz, że `main.py` to stub — `WorkflowBuilder` zostanie dodany w Module 3

---

**Poprzedni:** [01 - Zrozumienie architektury wieloagentowej](01-understand-multi-agent.md) · **Następny:** [03 - Konfiguracja agentów i środowiska →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->