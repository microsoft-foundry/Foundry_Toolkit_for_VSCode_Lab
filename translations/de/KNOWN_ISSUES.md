# Bekannte Probleme

Dieses Dokument verfolgt bekannte Probleme mit dem aktuellen Zustand des Repositories.

> Letzte Aktualisierung: 2026-04-15. Getestet mit Python 3.13 / Windows in `.venv_ga_test`.

---

## Aktuelle Paket-Pins (alle drei Agenten)

| Paket | Aktuelle Version |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(behoben — siehe KI-003)* |

---

## KI-001 — GA 1.0.0 Upgrade blockiert: `agent-framework-azure-ai` entfernt

**Status:** Offen | **Schweregrad:** 🔴 Hoch | **Typ:** Brechend

### Beschreibung

Das Paket `agent-framework-azure-ai` (gepinnt auf `1.0.0rc3`) wurde in der GA-Version (1.0.0, veröffentlicht am 2026-04-02) **entfernt/abgekündigt**.
Es wurde ersetzt durch:

- `agent-framework-foundry==1.0.0` — Foundry-gehostetes Agent-Muster
- `agent-framework-openai==1.0.0` — OpenAI-gestütztes Agent-Muster

Alle drei `main.py`-Dateien importieren `AzureAIAgentClient` aus `agent_framework.azure`, was unter den GA-Paketen einen `ImportError` auslöst. Der Namespace `agent_framework.azure` existiert in GA zwar noch, enthält aber nur Azure Functions Klassen (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — keine Foundry-Agenten.

### Bestätigter Fehler (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Betroffene Dateien

| Datei | Zeile |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` inkompatibel mit GA `agent-framework-core`

**Status:** Offen | **Schweregrad:** 🔴 Hoch | **Typ:** Brechend (blockiert durch Upstream)

### Beschreibung

`azure-ai-agentserver-agentframework==1.0.0b17` (neueste Version) pinnt `agent-framework-core<=1.0.0rc3` streng fest. Die Installation zusammen mit `agent-framework-core==1.0.0` (GA) erzwingt durch pip ein **Downgrade** von `agent-framework-core` zurück auf `rc3`, was dann `agent-framework-foundry==1.0.0` und `agent-framework-openai==1.0.0` zerstört.

Der Import `from azure.ai.agentserver.agentframework import from_agent_framework`, der von allen Agenten zur Bindung des HTTP-Servers verwendet wird, ist somit ebenfalls blockiert.

### Bestätigter Abhängigkeitskonflikt (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Betroffene Dateien

Alle drei `main.py`-Dateien — sowohl der Import oben als auch der Import in der Funktion `main()`.

---

## KI-003 — `agent-dev-cli --pre` Flag nicht mehr erforderlich

**Status:** ✅ Behoben (nicht brechend) | **Schweregrad:** 🟢 Niedrig

### Beschreibung

Alle `requirements.txt`-Dateien enthielten bisher `agent-dev-cli --pre`, um die Pre-Release-CLI zu beziehen. Seit der GA-Version 1.0.0 (veröffentlicht am 2026-04-02) ist die stabile Version von `agent-dev-cli` ohne das `--pre` Flag verfügbar.

**Behoben:** Das `--pre` Flag wurde aus allen drei `requirements.txt` Dateien entfernt.

---

## KI-004 — Dockerfiles verwenden `python:3.14-slim` (Pre-Release Basis-Image)

**Status:** Offen | **Schweregrad:** 🟡 Niedrig

### Beschreibung

Alle `Dockerfile`s verwenden `FROM python:3.14-slim`, welches eine Pre-Release-Version von Python nachverfolgt.
Für Produktionseinsätze sollte dies auf eine stabile Version festgelegt werden (z.B. `python:3.12-slim`).

### Betroffene Dateien

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referenzen

- [agent-framework-core auf PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry auf PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, können automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten. Das Originaldokument in seiner ursprünglichen Sprache gilt als maßgebliche Quelle. Für wichtige Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Nutzung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->