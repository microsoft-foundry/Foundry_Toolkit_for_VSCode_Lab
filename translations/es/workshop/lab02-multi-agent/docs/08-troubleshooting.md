# Módulo 8 - Solución de problemas

Este módulo cubre errores comunes, correcciones y estrategias de depuración específicas para el flujo de trabajo multiagente.

## Problemas con la salida del agente

### GapAnalyzer dice “Todavía no tengo el informe de coincidencias”

**Síntoma:** La respuesta de GapAnalyzer te pide que pegues un informe de coincidencias con “Habilidades faltantes” y “Brechas de certificación”. Esto sucede incluso cuando enviaste tanto un currículum como una descripción del puesto.

**Causa:** El texto del JD no se pasó a downstream al Agente JD. Con `context_mode="last_agent"`, `resume_executor` es el único ejecutor que ve el mensaje original del usuario. Si `RESUME_PARSER_INSTRUCTIONS` no incluye el texto del JD en su salida, el Agente JD no tiene JD para analizar, MatchingAgent no puede calcular una puntuación de ajuste, y GapAnalyzer recibe una entrada sin sentido.

**Diagnóstico:**

En los logs del servidor, busca el span de MatchingAgent. Si contiene:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
la transmisión está ausente o rota.

**Corrección:** Confirma que `RESUME_PARSER_INSTRUCTIONS` en `main.py` contiene una sección `[JOB DESCRIPTION PASS-THROUGH]` y la regla:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
También confirma que `JOB_DESCRIPTION_INSTRUCTIONS` contenga una regla de retransmisión `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Si alguno de los bloques de instrucciones es un borrador del asistente de scaffolding, reemplázalo por la versión completa de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent muestra “No se puede calcular la puntuación de ajuste - no se proporcionó JD”

Esta es la misma causa raíz que la anterior. MatchingAgent recibió la salida del Agente JD pero la sección `[PARSED RESUME PASS-THROUGH]` faltaba o estaba vacía, así que no pudo comparar los dos perfiles. Confirma:
1. `JOB_DESCRIPTION_INSTRUCTIONS` incluye la regla de retransmisión: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` indica al agente buscar las secciones `[JD REQUIREMENTS]` y `[PARSED RESUME PASS-THROUGH]`.

Reemplaza ambos bloques de instrucciones con las versiones completas de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### La respuesta aparece dos veces

**Síntoma:** La salida de GapAnalyzer (o la salida completa del pipeline) aparece dos veces en la respuesta del Inspector de Agente.

**Causa:** `WorkflowBuilder` usa semántica OR para las aristas entrantes: un ejecutor downstream se activa tan pronto como **cualquiera** de sus predecesores termina. Si `matching_executor` tiene dos aristas entrantes (una desde `resume_executor` y otra desde `jd_executor`), se activa dos veces: una cuando termina ResumeParser y otra cuando termina el Agente JD. GapAnalyzer entonces también se ejecuta dos veces.

**Corrección:** Asegúrate de que el gráfico `WorkflowBuilder` sea una pipeline estrictamente secuencial sin fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NO de resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Si tienes una línea `.add_edge(resume_executor, matching_executor)` descartada, elimínala. La retransmisión `[PARSED RESUME PASS-THROUGH]` en la salida del Agente JD ya da acceso a MatchingAgent al currículum.

---

## Problemas de entorno y configuración

### Valores `.env` faltantes o incorrectos

El archivo `.env` debe estar en el directorio `PersonalCareerCopilot/` (al mismo nivel que `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Contenido esperado de `.env`:

**Ruta A - cloud de Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Ruta B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Ambas rutas usan `FOUNDRY_PROJECT_ENDPOINT`. El valor difiere: cloud usa un endpoint Foundry con `https://`; local usa `http://localhost:5273/v1`. Ejecuta `foundry model list` para confirmar el alias exacto del modelo en la Ruta B.

> **Cómo encontrar tu `FOUNDRY_PROJECT_ENDPOINT`:** 
- Abre la barra lateral de **Foundry Toolkit** en VS Code → clic derecho en tu proyecto → **Copy Project Endpoint**. 
- O ve a [Azure Portal](https://portal.azure.com) → tu proyecto Foundry → **Overview** → **Project endpoint**.

> **Cómo encontrar tu `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** En la barra lateral de Foundry Toolkit, expande tu proyecto → **Models** → encuentra el nombre de tu modelo desplegado (por ejemplo, `gpt-4.1-mini`).

### Precedencia de variables de entorno

`main.py` usa `load_dotenv(override=True)`, lo que significa:

| Prioridad | Fuente | ¿Gana cuando ambos están establecidos? |
|----------|--------|------------------------|
| 1 (más alta) | Archivo `.env` | Sí |
| 2 | Variable de entorno de shell / contenedor | Se usa cuando la misma clave no está en `.env` |

En desarrollo local, esto hace que `.env` sea la fuente de verdad (editar `.env` afecta inmediatamente las ejecuciones). En despliegue hospedado, Foundry inyecta variables de entorno a nivel de contenedor; dado que `.env` no forma parte de la imagen desplegada para este laboratorio, se usan los valores inyectados en el contenedor.

---

## Compatibilidad de versiones

### Matriz de versiones de paquetes

El flujo de trabajo multiagente requiere versiones específicas de paquetes. Las versiones incompatibles causan errores en tiempo de ejecución.

| Paquete | Versión requerida | Comando para verificar |
|---------|-----------------|----------------------|
| `agent-framework-foundry` | última | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | última | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | última | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Errores comunes de versión

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Solución: reinstalar agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Corregir: actualizar el paquete mcp
pip install mcp --upgrade
```

### Verifica todas las versiones a la vez

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Salida esperada:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Problemas con el despliegue

### El contenedor no inicia después del despliegue

1. **Revisa los logs del contenedor:**
   - Abre la barra lateral de **Foundry Toolkit** → expande **Hosted Agents (Preview)** → clic en tu agente → expande la versión → **Container Details** → **Logs**.
   - Busca trazas de pila de Python o errores de módulo faltante.

2. **Errores comunes en el inicio del contenedor:**

   | Error en logs | Causa | Corrección |
   |--------------|-------|-----------|
   | `ModuleNotFoundError` | Falta un paquete en `requirements.txt` | Añadir el paquete, redeplegar |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variables de entorno faltantes en `agent.yaml` o `.env` | Actualizar sección `environment_variables` en `agent.yaml` (hospedado) o `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | No se configuró la Identidad Administrada | Foundry lo configura automáticamente - asegurarse de desplegar mediante la extensión |
   | `OSError: port 8088 already in use` | Dockerfile expone el puerto incorrecto o conflicto de puertos | Verificar `EXPOSE 8088` en Dockerfile y `CMD ["python", "main.py"]` |
   | Salida del contenedor con código 1 | Excepción no manejada en `main()` | Probar localmente primero ([Módulo 5](05-test-locally.md)) para detectar errores antes de desplegar |

3. **Redeplegar después de corregir:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → seleccionar el mismo agente → desplegar una nueva versión.

### El despliegue tarda demasiado

Los contenedores multiagente tardan más en iniciar porque crean 4 instancias de agente al inicio. Tiempos normales de inicio:

| Etapa | Duración esperada |
|-------|------------------|
| Construcción de imagen de contenedor | 1-3 minutos |
| Push de imagen al ACR | 30-60 segundos |
| Inicio del contenedor (agente único) | 15-30 segundos |
| Inicio del contenedor (multiagente) | 30-120 segundos |
| Agente disponible en Playground | 1-2 minutos después de "Started" |

> Si el estado "Pending" persiste más de 5 minutos, revisa los logs del contenedor por errores.

---

## Problemas de RBAC y permisos

### `403 Forbidden` o `AuthorizationFailed`

Necesitas el rol **[Foundry User](https://aka.ms/foundry-ext-project-role)** en tu proyecto Foundry (antes llamado **Azure AI User** - ID del rol sin cambios):

1. Ve a [Azure Portal](https://portal.azure.com) → recurso **proyecto** Foundry.
2. Haz clic en **Access control (IAM)** → **Asignaciones de roles**.
3. Busca tu nombre → confirma que aparece el rol **Foundry User** (o la etiqueta legacy **Azure AI User**).
4. Si falta: **Agregar** → **Agregar asignación de rol** → busca **Foundry User** → asignar a tu cuenta.

Consulta la documentación de [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para más detalles.

### Despliegue del modelo no accesible

Si el agente devuelve errores relacionados con el modelo:

1. Verifica que el modelo esté desplegado: barra lateral de Foundry → expande proyecto → **Models** → busca `gpt-4.1-mini` (o tu modelo) con estado **Succeeded**.
2. Verifica que el nombre de despliegue coincida: compara `AZURE_AI_MODEL_DEPLOYMENT_NAME` en `.env` (o `agent.yaml`) con el nombre real en la barra lateral.
3. Si el despliegue expiró (nivel gratuito): redepliega desde [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Problemas con Foundry Local (Ruta B)

### El servicio de Foundry Local no está funcionando

```powershell
# Comprobar estado
foundry local status

# Iniciar el servicio si está detenido
foundry local start
```

| Síntoma | Causa | Corrección |
|---------|-------|------------|
| La verificación de estado devuelve `503` | Servicio no iniciado | `foundry local start` o clic en **Start** en la barra lateral de Foundry Toolkit |
| La verificación de estado agota el tiempo | Modelo aún cargando | Espera 30–60 s después de iniciar; modelos grandes tardan más |
| `StatusCode: 404` en `/v1/health` | Puerto incorrecto | El puerto por defecto es `5273`. Verifica con `foundry local status` el puerto actual |
| Recursos insuficientes | Foundry Local necesita ~4 GB de RAM libre | Cierra otras aplicaciones |
| Fallo en descarga del modelo | Espacio en disco insuficiente | Los modelos ocupan 2–8 GB. Libera espacio y luego `foundry model pull <nombre>` |

### Desajuste en el nombre del modelo

```powershell
# Listar modelos descargados y sus alias exactos
foundry model list
```

Establece `AZURE_AI_MODEL_DEPLOYMENT_NAME` en `.env` con el alias exacto mostrado (por ejemplo, `phi-4-mini`, no `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` al ejecutar localmente (Ruta B)

El `main.py` del laboratorio usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local requiere que esta variable apunte al servicio local - **no** a `AZURE_AI_PROJECT_ENDPOINT`. Asegúrate de que tu `.env` contenga:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### La herramienta MCP aún realiza una llamada externa (Ruta B)

Esto es esperado. La herramienta `search_microsoft_learn_for_plan` obtiene recursos de aprendizaje desde `https://learn.microsoft.com/api/mcp`. **Solo la consulta del nombre de la habilidad** viaja por la red - el currículum y el texto JD se procesan completamente en tu dispositivo y nunca se transmiten. Si se requiere operación completamente offline, añade una excepción `try/except` en la herramienta que retorne una URL estática `learn.microsoft.com` cuando el endpoint no esté disponible.

---

## Obtener ayuda

Si estás atascado después de probar las correcciones anteriores:

1. **Revisa los logs del servidor** - La mayoría de errores generan una traza de pila de Python en el terminal. Lee el traceback completo.
2. **Busca el mensaje de error** - Copia el texto del error y busca en [Microsoft Q&A para Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Abre un issue** - Crea un issue en el [repositorio del taller](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) con:
   - El mensaje de error o captura de pantalla
   - Las versiones de tus paquetes (`pip list | Select-String "agent-framework"`)
   - Tu versión de Python (`python --version`)
   - Si el problema es local o tras el despliegue

---

### Punto de control

- [ ] Sabes cómo verificar y corregir problemas de configuración del `.env`
- [ ] Puedes verificar que las versiones de los paquetes coincidan con la matriz requerida
- [ ] Sabes cómo revisar logs de contenedores para fallos de despliegue
- [ ] Puedes verificar roles RBAC en el Portal de Azure

---

**Anterior:** [07 - Verificar en Playground](07-verify-in-playground.md) · **Siguiente:** [09 - Resumen →](09-summary.md) · **Inicio:** [Lab 02 README](../README.md) · [Inicio del Taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->