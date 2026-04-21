# Problemas Conocidos

Este documento rastrea los problemas conocidos con el estado actual del repositorio.

> Última actualización: 2026-04-15. Probado con Python 3.13 / Windows en `.venv_ga_test`.

---

## Pines Actuales de Paquetes (los tres agentes)

| Paquete | Versión Actual |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(corregido — ver KI-003)* |

---

## KI-001 — Actualización GA 1.0.0 Bloqueada: `agent-framework-azure-ai` Eliminado

**Estado:** Abierto | **Gravedad:** 🔴 Alta | **Tipo:** Rompedor

### Descripción

El paquete `agent-framework-azure-ai` (fijado en `1.0.0rc3`) fue **eliminado/descontinuado**
en el lanzamiento GA (1.0.0, lanzado el 2026-04-02). Es reemplazado por:

- `agent-framework-foundry==1.0.0` — patrón de agente alojado en Foundry
- `agent-framework-openai==1.0.0` — patrón de agente respaldado por OpenAI

Los tres archivos `main.py` importan `AzureAIAgentClient` desde `agent_framework.azure`, lo cual
genera un `ImportError` con los paquetes GA. El espacio de nombres `agent_framework.azure` aún existe
en GA pero ahora contiene solo clases de Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — no agentes Foundry.

### Error confirmado (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Archivos afectados

| Archivo | Línea |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Incompatible con GA `agent-framework-core`

**Estado:** Abierto | **Gravedad:** 🔴 Alta | **Tipo:** Rompedor (bloqueado en upstream)

### Descripción

`azure-ai-agentserver-agentframework==1.0.0b17` (última versión) fija estrictamente
`agent-framework-core<=1.0.0rc3`. Instalarlo junto con `agent-framework-core==1.0.0` (GA)
fuerza a pip a **degradar** `agent-framework-core` nuevamente a `rc3`, lo que rompe
`agent-framework-foundry==1.0.0` y `agent-framework-openai==1.0.0`.

Por lo tanto, la llamada `from azure.ai.agentserver.agentframework import from_agent_framework` usada por todos
los agentes para enlazar el servidor HTTP también está bloqueada.

### Conflicto de dependencias confirmado (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Archivos afectados

Los tres archivos `main.py` — tanto la importación inicial como la importación dentro de la función `main()`.

---

## KI-003 — Flag `agent-dev-cli --pre` Ya No Es Necesario

**Estado:** ✅ Corregido (no rompedor) | **Gravedad:** 🟢 Baja

### Descripción

Todos los archivos `requirements.txt` incluían previamente `agent-dev-cli --pre` para obtener
la CLI pre-lanzamiento. Desde que GA 1.0.0 se lanzó el 2026-04-02, la versión estable de
`agent-dev-cli` está ahora disponible sin la bandera `--pre`.

**Corrección aplicada:** La bandera `--pre` ha sido removida de los tres archivos `requirements.txt`.

---

## KI-004 — Dockerfiles Usan `python:3.14-slim` (Imagen Base Pre-lanzamiento)

**Estado:** Abierto | **Gravedad:** 🟡 Baja

### Descripción

Todos los `Dockerfile` usan `FROM python:3.14-slim` que rastrea una compilación pre-lanzamiento de Python.
Para despliegues en producción, esto debería fijarse a una versión estable (p. ej., `python:3.12-slim`).

### Archivos afectados

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referencias

- [agent-framework-core en PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry en PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso legal**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No nos responsabilizamos por ningún malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->