# Módulo 8 - Solución de problemas (Multi-Agente)

Este módulo cubre errores comunes, soluciones y estrategias de depuración específicas para el flujo de trabajo multi-agente. Para problemas generales de implementación en Foundry, consulte también la [guía de solución de problemas del Laboratorio 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Referencia rápida: Error → Solución

| Error / Síntoma | Causa probable | Solución |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Archivo `.env` faltante o valores no establecidos | Crear `.env` con `PROJECT_ENDPOINT=<tu-endpoint>` y `MODEL_DEPLOYMENT_NAME=<tu-modelo>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Entorno virtual no activado o dependencias no instaladas | Ejecutar `.\.venv\Scripts\Activate.ps1` luego `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Paquete MCP no instalado (falta en requirements) | Ejecutar `pip install mcp` o revisar que `requirements.txt` lo incluya como dependencia transitiva |
| El agente inicia pero responde vacío | Desajuste en `output_executors` o faltan conexiones | Verificar `output_executors=[gap_analyzer]` y que todas las conexiones existan en `create_workflow()` |
| Solo una card gap (las demás faltan) | Instrucciones de GapAnalyzer incompletas | Añadir el párrafo `CRITICAL:` a `GAP_ANALYZER_INSTRUCTIONS` - ver [Módulo 3](03-configure-agents.md) |
| La puntuación de ajuste es 0 o está ausente | MatchingAgent no recibió datos upstream | Verificar que existen `add_edge(resume_parser, matching_agent)` y `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | El servidor MCP rechazó la llamada a la herramienta | Comprobar conectividad a internet. Intentar abrir `https://learn.microsoft.com/api/mcp` en el navegador. Reintentar |
| No hay URLs de Microsoft Learn en la salida | Herramienta MCP no registrada o endpoint incorrecto | Verificar `tools=[search_microsoft_learn_for_plan]` en GapAnalyzer y que `MICROSOFT_LEARN_MCP_ENDPOINT` sea correcto |
| `Address already in use: port 8088` | Otro proceso está usando el puerto 8088 | Ejecutar `netstat -ano \| findstr :8088` (Windows) o `lsof -i :8088` (macOS/Linux) y detener el proceso en conflicto |
| `Address already in use: port 5679` | Conflicto en el puerto para Debugpy | Detener otras sesiones de depuración. Ejecutar `netstat -ano \| findstr :5679` para encontrar y terminar el proceso |
| No se abre Agent Inspector | Servidor no ha iniciado completamente o conflicto de puerto | Esperar al mensaje "Server running". Comprobar que el puerto 5679 esté libre |
| `azure.identity.CredentialUnavailableError` | No se ha iniciado sesión en Azure CLI | Ejecutar `az login` y reiniciar el servidor |
| `azure.core.exceptions.ResourceNotFoundError` | El despliegue del modelo no existe | Verificar que `MODEL_DEPLOYMENT_NAME` coincida con un modelo desplegado en tu proyecto Foundry |
| Estado del contenedor "Failed" tras despliegue | Fallo del contenedor al iniciar | Revisar logs del contenedor en la barra lateral de Foundry. Común: variable de entorno faltante o error de importación |
| Despliegue en estado "Pending" > 5 minutos | Contenedor tarda mucho en iniciar o limitaciones de recursos | Esperar hasta 5 minutos para multi-agente (crea 4 instancias). Si sigue pendiente, revisar logs |
| `ValueError` desde `WorkflowBuilder` | Configuración inválida del grafo | Asegurar que `start_executor` esté asignado, `output_executors` sea una lista y no existan conexiones circulares |

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

Contenido esperado del `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Cómo encontrar tu PROJECT_ENDPOINT:** 
- Abrir la barra lateral **Microsoft Foundry** en VS Code → clic derecho en tu proyecto → **Copiar Endpoint del Proyecto**. 
- O ir al [Portal de Azure](https://portal.azure.com) → tu proyecto Foundry → **Resumen** → **Endpoint del proyecto**.

> **Cómo encontrar tu MODEL_DEPLOYMENT_NAME:** En la barra lateral de Foundry, expandir tu proyecto → **Models** → encontrar el nombre de tu modelo desplegado (ej. `gpt-4.1-mini`).

### Precedencia de variables de entorno

`main.py` usa `load_dotenv(override=False)`, lo que significa:

| Prioridad | Origen | ¿Gana cuando ambos están establecidos? |
|----------|--------|------------------------|
| 1 (más alto) | Variable de entorno del shell | Sí |
| 2 | Archivo `.env` | Solo si la variable de shell no está establecida |

Esto significa que las variables de entorno en tiempo de ejecución de Foundry (establecidas vía `agent.yaml`) tienen precedencia sobre los valores `.env` durante el despliegue alojado.

---

## Compatibilidad de versiones

### Matriz de versiones de paquetes

El flujo multi-agente requiere versiones específicas de paquetes. Las versiones incorrectas causan errores en tiempo de ejecución.

| Paquete | Versión requerida | Comando para verificar |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | última pre-lanzamiento | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Errores comunes de versión

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Corrección: actualización a rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` no encontrado o Inspector incompatible:**

```powershell
# Arreglar: instalar con la bandera --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Corrección: actualizar el paquete mcp
pip install mcp --upgrade
```

### Verificar todas las versiones a la vez

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Salida esperada:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Problemas con la herramienta MCP

### Herramienta MCP no devuelve resultados

**Síntoma:** Las cards de lagunas indican "No results returned from Microsoft Learn MCP" o "No direct Microsoft Learn results found".

**Posibles causas:**

1. **Problema de red** - El endpoint MCP (`https://learn.microsoft.com/api/mcp`) no está accesible.
   ```powershell
   # Probar conectividad
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Si devuelve `200`, el endpoint está accesible.

2. **Consulta demasiado específica** - El nombre de la habilidad es muy nicho para la búsqueda de Microsoft Learn.
   - Esto es esperado para habilidades muy especializadas. La herramienta proporciona una URL alternativa en la respuesta.

3. **Tiempo de espera agotado en la sesión MCP** - La conexión Streamable HTTP expiró.
   - Reintentar la solicitud. Las sesiones MCP son efímeras y pueden requerir reconexión.

### Explicación de logs MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Significado | Acción |
|-----|---------|--------|
| `GET → 405` | Sondeos del cliente MCP durante la inicialización | Normal - ignorar |
| `POST → 200` | Llamada a la herramienta exitosa | Esperado |
| `DELETE → 405` | Sondeos del cliente MCP durante la limpieza | Normal - ignorar |
| `POST → 400` | Solicitud incorrecta (consulta malformada) | Revisar el parámetro `query` en `search_microsoft_learn_for_plan()` |
| `POST → 429` | Límite de tasa alcanzado | Esperar y reintentar. Reducir el parámetro `max_results` |
| `POST → 500` | Error del servidor MCP | Transitorio - reintentar. Si persiste, el API de Microsoft Learn MCP podría estar caído |
| Tiempo de espera de conexión | Problema de red o servidor MCP no disponible | Comprobar internet. Intentar `curl https://learn.microsoft.com/api/mcp` |

---

## Problemas de despliegue

### El contenedor falla al iniciar tras el despliegue

1. **Revisar logs del contenedor:**
   - Abrir la barra lateral **Microsoft Foundry** → expandir **Hosted Agents (Preview)** → seleccionar tu agente → expandir la versión → **Detalles del Contenedor** → **Logs**.
   - Buscar rastros de pila de Python o errores de módulos faltantes.

2. **Errores comunes al iniciar el contenedor:**

   | Error en logs | Causa | Solución |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Falta paquete en `requirements.txt` | Agregar el paquete, redeplegar |
   | `RuntimeError: Missing required environment variable` | Variables de entorno en `agent.yaml` no establecidas | Actualizar sección `environment_variables` en `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Identidad administrada no configurada | Foundry la asigna automáticamente - asegurar despliegue vía extensión |
   | `OSError: port 8088 already in use` | Dockerfile expone puerto incorrecto o conflicto de puertos | Verificar `EXPOSE 8088` en Dockerfile y `CMD ["python", "main.py"]` |
   | Contenedor sale con código 1 | Excepción no manejada en `main()` | Probar localmente primero ([Módulo 5](05-test-locally.md)) para detectar errores antes del despliegue |

3. **Redeplegar tras corregir:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → seleccionar el mismo agente → desplegar nueva versión.

### El despliegue tarda demasiado

Los contenedores multi-agente tardan más en iniciar porque crean 4 instancias de agente al arrancar. Tiempos normales de inicio:

| Etapa | Duración esperada |
|-------|------------------|
| Construcción imagen contenedor | 1-3 minutos |
| Push de imagen a ACR | 30-60 segundos |
| Inicio contenedor (agente único) | 15-30 segundos |
| Inicio contenedor (multi-agente) | 30-120 segundos |
| Agente disponible en Playground | 1-2 minutos después de "Started" |

> Si el estado "Pending" persiste más de 5 minutos, revisar logs del contenedor por errores.

---

## Problemas de RBAC y permisos

### `403 Forbidden` o `AuthorizationFailed`

Necesitas el rol **[Azure AI User](https://aka.ms/foundry-ext-project-role)** en tu proyecto Foundry:

1. Ir al [Portal de Azure](https://portal.azure.com) → recurso **proyecto** de Foundry.
2. Click en **Control de acceso (IAM)** → **Asignaciones de roles**.
3. Buscar tu nombre → confirmar que **Azure AI User** está listado.
4. Si falta: **Agregar** → **Agregar asignación de rol** → buscar **Azure AI User** → asignar a tu cuenta.

Consulta la documentación de [RBAC para Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para más detalles.

### Despliegue del modelo no accesible

Si el agente devuelve errores relacionados con el modelo:

1. Verificar que el modelo esté desplegado: barra lateral Foundry → expandir proyecto → **Models** → buscar `gpt-4.1-mini` (o tu modelo) con estado **Succeeded**.
2. Verificar que el nombre de despliegue coincida: comparar `MODEL_DEPLOYMENT_NAME` en `.env` (o `agent.yaml`) con el nombre real en la barra lateral.
3. Si el despliegue expiró (nivel gratuito): redeplegar desde el [Catálogo de Modelos](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Problemas con Agent Inspector

### Inspector se abre pero muestra "Disconnected"

1. Verificar que el servidor esté corriendo: buscar "Server running on http://localhost:8088" en el terminal.
2. Comprobar el puerto `5679`: Inspector se conecta mediante debugpy en el puerto 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Reiniciar el servidor y volver a abrir Inspector.

### Inspector muestra respuesta parcial

Las respuestas en multi-agente son largas y se transmiten incrementalmente. Esperar a que la respuesta completa finalice (puede tomar 30-60 segundos según número de gap cards y llamadas a la herramienta MCP).

Si la respuesta se trunca sistemáticamente:
- Comprobar que las instrucciones de GapAnalyzer incluyen el bloque `CRITICAL:` que evita combinar las gap cards.
- Verificar el límite de tokens de tu modelo - `gpt-4.1-mini` soporta hasta 32K tokens de salida, lo cual debería ser suficiente.

---

## Consejos de rendimiento

### Respuestas lentas

Los flujos multi-agente son inherentemente más lentos que los de un solo agente debido a dependencias secuenciales y llamadas a la herramienta MCP.

| Optimización | Cómo | Impacto |
|-------------|-----|--------|
| Reducir llamadas MCP | Disminuir el parámetro `max_results` en la herramienta | Menos viajes HTTP |
| Simplificar instrucciones | Prompts más cortos y enfocados para el agente | Inferencia LLM más rápida |
| Usar `gpt-4.1-mini` | Más rápido que `gpt-4.1` para desarrollo | Aproximadamente 2x más rápido |
| Reducir detalle en gap card | Simplificar formato de gap card en instrucciones de GapAnalyzer | Menos salida que generar |

### Tiempos típicos de respuesta (local)

| Configuración | Tiempo esperado |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap cards | 30-60 segundos |
| `gpt-4.1-mini`, 8+ gap cards | 60-120 segundos |
| `gpt-4.1`, 3-5 gap cards | 60-120 segundos |
---

## Obtener ayuda

Si estás atascado después de intentar las correcciones anteriores:

1. **Revisa los registros del servidor** - La mayoría de los errores producen un seguimiento de pila de Python en la terminal. Lee el rastreo completo.
2. **Busca el mensaje de error** - Copia el texto del error y búscalo en [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Abre un problema** - Abre un issue en el [repositorio del taller](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) con:
   - El mensaje de error o captura de pantalla
   - Tus versiones de paquetes (`pip list | Select-String "agent-framework"`)
   - Tu versión de Python (`python --version`)
   - Si el problema es local o después del despliegue

---

### Lista de verificación

- [ ] Puedes identificar y corregir los errores más comunes de múltiples agentes usando la tabla de referencia rápida
- [ ] Sabes cómo revisar y corregir problemas de configuración en `.env`
- [ ] Puedes verificar que las versiones de los paquetes coincidan con la matriz requerida
- [ ] Comprendes las entradas de registro MCP y puedes diagnosticar fallos de herramientas
- [ ] Sabes cómo revisar los registros de contenedores para fallos en el despliegue
- [ ] Puedes verificar los roles RBAC en el Portal de Azure

---

**Anterior:** [07 - Verificar en Playground](07-verify-in-playground.md) · **Inicio:** [Lab 02 README](../README.md) · [Inicio del taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda la traducción profesional humana. No somos responsables de ningún malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->