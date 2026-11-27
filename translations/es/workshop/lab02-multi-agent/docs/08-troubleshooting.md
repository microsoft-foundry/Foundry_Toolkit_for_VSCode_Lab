# Módulo 8 - Solución de problemas

Este módulo cubre errores comunes, correcciones y estrategias de depuración específicas para el flujo de trabajo multiagente.

## Problemas de salida del agente

### GapAnalyzer dice “Todavía no tengo el informe coincidente”

**Síntoma:** La respuesta de GapAnalyzer te pide pegar un informe coincidente con “Habilidades faltantes” y “Brechas de certificación.” Esto sucede incluso cuando enviaste tanto un currículum como una descripción del trabajo.

**Causa:** El texto JD no fue pasado río abajo al agente JD. Con `context_mode="last_agent"`, `resume_executor` es el único ejecutor que ve el mensaje original del usuario. Si `RESUME_PARSER_INSTRUCTIONS` no incluye el texto JD en su salida, el agente JD no tiene un JD para analizar, MatchingAgent no puede calcular una puntuación de ajuste y GapAnalyzer recibe una entrada sin sentido.

**Diagnóstico:**

En los registros del servidor, busca el span de MatchingAgent. Si contiene:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
el paso a través está ausente o roto.

**Corrección:** Confirma que `RESUME_PARSER_INSTRUCTIONS` en `main.py` contiene una sección `[JOB DESCRIPTION PASS-THROUGH]` y la regla:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
También confirma que `JOB_DESCRIPTION_INSTRUCTIONS` contiene una regla de retransmisión `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Si cualquiera de los bloques de instrucciones es un esqueleto del asistente de configuración, reemplázalo con la versión completa de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent muestra “No se puede calcular la puntuación de ajuste - no se proporcionó JD”

Esta es la misma causa raíz que la anterior. MatchingAgent recibió la salida del agente JD pero la sección `[PARSED RESUME PASS-THROUGH]` estaba ausente o vacía, así que no pudo comparar los dos perfiles. Confirma:
1. `JOB_DESCRIPTION_INSTRUCTIONS` incluye la regla de retransmisión: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` indica al agente buscar las secciones `[JD REQUIREMENTS]` y `[PARSED RESUME PASS-THROUGH]`.

Reemplaza ambos bloques de instrucciones con las versiones completas de [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### La respuesta aparece dos veces

**Síntoma:** La salida de GapAnalyzer (o toda la salida del pipeline) aparece dos veces en la respuesta del Inspector de Agentes.

**Causa:** `WorkflowBuilder` usa semántica OR para las conexiones entrantes - un ejecutor río abajo se activa tan pronto como **cualquier** predecesor termina. Si `matching_executor` tiene dos entradas (una de `resume_executor` y otra de `jd_executor`), se activa dos veces: una cuando ResumeParser termina y otra cuando el agente JD termina. Entonces GapAnalyzer también se ejecuta dos veces.

**Corrección:** Asegúrate que el grafo `WorkflowBuilder` sea una secuencia estrictamente lineal sin fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Si tienes una línea `.add_edge(resume_executor, matching_executor)` suelta, elimínala. La retransmisión `[PARSED RESUME PASS-THROUGH]` en la salida del agente JD ya da acceso a MatchingAgent al currículum.

---

## Problemas de entorno y configuración

### Valores `.env` faltantes o incorrectos

El archivo `.env` debe estar en el directorio `PersonalCareerCopilot/` (mismo nivel que `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Contenido esperado `.env`:

**Ruta A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Ruta B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Ambas rutas usan `FOUNDRY_PROJECT_ENDPOINT`. El valor difiere: cloud usa un endpoint `https://` Foundry; local usa `http://localhost:5273/v1`. Ejecuta `foundry model list` para confirmar el alias exacto del modelo para la ruta B.

> **Encontrar tu `FOUNDRY_PROJECT_ENDPOINT`:** 
- Abre la barra lateral **Foundry Toolkit** en VS Code → clic derecho en tu proyecto → **Copiar endpoint del proyecto**. 
- O ve a [Azure Portal](https://portal.azure.com) → tu proyecto Foundry → **Descripción general** → **Endpoint del proyecto**.

> **Encontrar tu `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** En la barra lateral Foundry Toolkit, expande tu proyecto → **Modelos** → encuentra el nombre de tu modelo desplegado (ej., `gpt-4.1-mini`).

### Precedencia de variables de entorno

`main.py` usa `load_dotenv(override=True)`, lo que significa:

| Prioridad | Fuente | ¿Gana cuando ambos están configurados? |
|----------|--------|-------------------------------|
| 1 (más alto) | Archivo `.env`  | Sí |
| 2 | Variable del entorno Shell / contenedor | Usado cuando no está presente la misma clave en `.env` |

En desarrollo local, esto hace que `.env` sea la fuente de la verdad (editar `.env` afecta las ejecuciones de inmediato). En despliegue hospedado, Foundry inyecta variables de entorno a nivel de contenedor; dado que `.env` no forma parte de la imagen desplegada para esta configuración de laboratorio, se usan los valores inyectados en el contenedor.

---

## Compatibilidad de versiones

### Matriz de versiones de paquetes

El flujo de trabajo multiagente requiere versiones específicas de paquetes. Las versiones desajustadas causan errores en tiempo de ejecución.

| Paquete | Versión requerida | Comando para verificar |
|---------|------------------|------------------------|
| `agent-framework-foundry` | última | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | última | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | última | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Errores comunes de versiones

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

### Verificar todas las versiones de una vez

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

## Problemas de despliegue

### El contenedor no se inicia tras el despliegue

1. **Revisar los logs del contenedor:**
   - Abre la barra lateral **Foundry Toolkit** → bajo tu proyecto, clic en **Agentes** → pestaña **Agente Hospedado** → clic en tu agente. Revisa el **Estado** en la pestaña **Detalles**, luego abre la pestaña **Playground** y usa la pestaña **Logs** en el panel **Detalles de sesión** para ver la salida del contenedor.
   - Busca trazas de pila de Python o errores de módulos faltantes.

2. **Fallas comunes de inicio del contenedor:**

   | Error en logs | Causa | Corrección |
   |--------------|-------|------------|
   | `ModuleNotFoundError` | Falta paquete `requirements.txt` | Añade el paquete, vuelve a desplegar |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variables de entorno `agent.yaml` o `.env` no configuradas | Actualiza `agent.yaml` → sección `environment_variables` (hospedado) o `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Identidad Administrada no configurada | Foundry lo establece automáticamente - asegúrate de desplegar a través de la extensión |
   | `OSError: port 8088 already in use` | Dockerfile expone puerto incorrecto o conflicto de puertos | Verifica `EXPOSE 8088` en Dockerfile y `CMD ["python", "main.py"]` |
   | Salida del contenedor con código 1 | Excepción no manejada en `main()` | Prueba local primero ([Módulo 5](05-test-locally.md)) para detectar errores antes de desplegar |

3. **Re-despliega después de corregir:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Desplegar Agente Hospedado** → selecciona el mismo agente → despliega una nueva versión.

### El despliegue tarda demasiado

Los contenedores multiagente tardan más en iniciarse porque crean 4 instancias de agentes al inicio. Tiempos normales de inicio:

| Etapa | Duración esperada |
|-------|------------------|
| Construcción de la imagen del contenedor | 1-3 minutos |
| Push de imagen a ACR | 30-60 segundos |
| Inicio del contenedor (agente único) | 15-30 segundos |
| Inicio del contenedor (multiagente) | 30-120 segundos |
| Agente disponible en Playground | 1-2 minutos después de "Iniciado" |

> Si el estado "Pendiente" persiste más de 5 minutos, revisa los logs del contenedor en busca de errores.

---

## Problemas de RBAC y permisos

### `403 Forbidden` o `AuthorizationFailed`

Necesitas el rol **[Usuario Foundry](https://aka.ms/foundry-ext-project-role)** en tu proyecto Foundry (antes llamado **Usuario Azure AI** - ID de rol sin cambios):

1. Ve a [Azure Portal](https://portal.azure.com) → recurso del **proyecto** Foundry.
2. Haz clic en **Control de acceso (IAM)** → **Asignaciones de roles**.
3. Busca tu nombre → confirma que está listado **Usuario Foundry** (o la etiqueta heredada **Usuario Azure AI**).
4. Si falta: **Agregar** → **Agregar asignación de rol** → busca **Usuario Foundry** → asígnalo a tu cuenta.

Consulta la documentación [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para más detalles.

### Despliegue del modelo no accesible

Si el agente devuelve errores relacionados con el modelo:

1. Verifica que el modelo esté desplegado: barra lateral de Foundry → expande proyecto → **Modelos** → verifica `gpt-4.1-mini` (o tu modelo) con estado **Succeeded**.
2. Verifica que el nombre del despliegue coincida: compara `AZURE_AI_MODEL_DEPLOYMENT_NAME` en `.env` (o `agent.yaml`) con el nombre real del despliegue en la barra lateral.
3. Si el despliegue expiró (nivel gratuito): vuelve a desplegar desde [Catálogo de modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Abrir Catálogo de Modelos**).

---

## Problemas con Foundry Local (Ruta B)

### Servicio Foundry Local no está en ejecución

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Síntoma | Causa | Corrección |
|---------|-------|------------|
| La verificación de estado devuelve `503` | Servicio no iniciado | `foundry local start` o clic en **Iniciar** en la barra lateral Foundry Toolkit |
| La verificación de estado expira | Modelo aún cargando | Espera 30–60 s después de iniciar; modelos más grandes tardan más |
| `StatusCode: 404` en `/v1/health` | Puerto incorrecto | Por defecto es `5273`. Revisa `foundry local status` para el puerto real |
| Recursos insuficientes | Foundry Local necesita ~4 GB RAM libres | Cierra otras aplicaciones |
| Falla la descarga de modelo | Espacio en disco bajo | Los modelos ocupan 2–8 GB. Libera espacio y luego `foundry model pull <name>` |

### Discordancia en el nombre del modelo

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Define `AZURE_AI_MODEL_DEPLOYMENT_NAME` en `.env` al alias exacto mostrado (ej., `phi-4-mini`, no `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` en ejecución local (Ruta B)

El `main.py` del laboratorio usa `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local requiere que esta variable apunte al servicio local - **no** a `AZURE_AI_PROJECT_ENDPOINT`. Asegura que tu `.env` contenga:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### La herramienta MCP aún hace una llamada externa (Ruta B)

Esto es esperado. La herramienta `search_microsoft_learn_for_plan` busca recursos de aprendizaje desde `https://learn.microsoft.com/api/mcp`. **Sólo la consulta del nombre de la habilidad** viaja por la red - el currículum y el texto JD se procesan totalmente en tu dispositivo y nunca se transmiten. Si se requiere operación totalmente sin conexión, añade un `try/except` como respaldo en la herramienta que retorne una URL `learn.microsoft.com` estática cuando el endpoint no sea accesible.

---

## Obtener ayuda

Si estás atorado después de probar las correcciones arriba:

1. **Revisa los registros del servidor** - La mayoría de los errores producen una traza de pila de Python en la terminal. Lee el seguimiento completo.
2. **Busca el mensaje de error** - Copia el texto del error y búscalo en [Microsoft Q&A para Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Abre un issue** - Crea un issue en el [repositorio del taller](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) con:
   - El mensaje de error o captura de pantalla
   - Las versiones de tus paquetes (`pip list | Select-String "agent-framework"`)
   - Tu versión de Python (`python --version`)
   - Si el problema es local o después del despliegue

---

### Punto de control

- [ ] Sabes cómo verificar y corregir problemas de configuración `.env`
- [ ] Puedes verificar que las versiones de los paquetes coincidan con la matriz requerida
- [ ] Sabes cómo revisar los logs del contenedor para fallas de despliegue
- [ ] Puedes verificar los roles RBAC en el portal de Azure

---

**Anterior:** [07 - Verificar en Playground](07-verify-in-playground.md) · **Siguiente:** [09 - Resumen →](09-summary.md) · **Inicio:** [README del Laboratorio 02](../README.md) · [Inicio del taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->