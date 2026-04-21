# Znane problemy

Ten dokument śledzi znane problemy z aktualnym stanem repozytorium.

> Ostatnia aktualizacja: 2026-04-15. Testowano na Python 3.13 / Windows w `.venv_ga_test`.

---

## Aktualne przypięcia pakietów (wszystkie trzy agenty)

| Pakiet | Aktualna wersja |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(naprawiono — patrz KI-003)* |

---

## KI-001 — Aktualizacja GA 1.0.0 zablokowana: usunięto `agent-framework-azure-ai`

**Status:** Otwarte | **Waga:** 🔴 Wysoka | **Typ:** Łamiące

### Opis

Pakiet `agent-framework-azure-ai` (przypięty do `1.0.0rc3`) został **usunięty/wycofany**
w wersji GA (1.0.0, wydanej 2026-04-02). Został zastąpiony przez:

- `agent-framework-foundry==1.0.0` — wzorzec agenta hostowany na Foundry
- `agent-framework-openai==1.0.0` — wzorzec agenta oparty na OpenAI

Wszystkie trzy pliki `main.py` importują `AzureAIAgentClient` z `agent_framework.azure`, co
wywołuje `ImportError` przy pakietach GA. Przestrzeń nazw `agent_framework.azure` nadal istnieje
w GA, ale teraz zawiera tylko klasy Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — nie agentów Foundry.

### Potwierdzony błąd (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Pliki dotknięte

| Plik | Linia |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` niekompatybilny z GA `agent-framework-core`

**Status:** Otwarte | **Waga:** 🔴 Wysoka | **Typ:** Łamiące (zablokowane przez zależności)

### Opis

`azure-ai-agentserver-agentframework==1.0.0b17` (najnowszy) sztywno przypina
`agent-framework-core<=1.0.0rc3`. Instalacja go obok `agent-framework-core==1.0.0` (GA)
wymusza na pip **obniżenie wersji** `agent-framework-core` do `rc3`, co następnie łamie
`agent-framework-foundry==1.0.0` i `agent-framework-openai==1.0.0`.

Wywołanie `from azure.ai.agentserver.agentframework import from_agent_framework` używane przez wszystkie
agenty do powiązania serwera HTTP jest zatem także zablokowane.

### Potwierdzony konflikt zależności (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Pliki dotknięte

Wszystkie trzy pliki `main.py` — zarówno import na najwyższym poziomie, jak i import wewnątrz funkcji `main()`.

---

## KI-003 — Flaga `agent-dev-cli --pre` nie jest już potrzebna

**Status:** ✅ Naprawione (niełamliwe) | **Waga:** 🟢 Niska

### Opis

Wszystkie pliki `requirements.txt` wcześniej zawierały `agent-dev-cli --pre`, aby pobrać
wersję wstępną CLI. Od czasu wydania GA 1.0.0 (2026-04-02) stabilna wersja
`agent-dev-cli` jest już dostępna bez flagi `--pre`.

**Naprawa:** Flaga `--pre` została usunięta ze wszystkich trzech plików `requirements.txt`.

---

## KI-004 — Dockerfile używają `python:3.14-slim` (obraz bazowy w wersji przedpremierowej)

**Status:** Otwarte | **Waga:** 🟡 Niska

### Opis

Wszystkie `Dockerfile` używają `FROM python:3.14-slim`, który śledzi wersję przedpremierową Pythona.
Dla wdrożeń produkcyjnych powinien być przypięty do stabilnego wydania (np. `python:3.12-slim`).

### Pliki dotknięte

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Odnośniki

- [agent-framework-core na PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry na PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:  
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Chociaż dążymy do dokładności, prosimy mieć na uwadze, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w języku źródłowym powinien być uznawany za źródło wiarygodne. W przypadku istotnych informacji zaleca się skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z korzystania z tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->