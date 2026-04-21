# Módulo 8 - Solución de problemas

Este módulo es una guía de referencia para cada problema común que se encuentra durante el taller. Añádelo a favoritos; volverás a él cada vez que algo salga mal.

---

## 1. Errores de permiso

### 1.1 Permiso `agents/write` denegado

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Causa raíz:** No tienes el rol `Azure AI User` a nivel de **proyecto**. Este es el error más común en el taller.

**Solución - paso a paso:**

1. Abre [https://portal.azure.com](https://portal.azure.com).
2. En la barra de búsqueda superior, escribe el nombre de tu **proyecto Foundry** (ejemplo, `workshop-agents`).
3. **Crítico:** Haz clic en el resultado que muestre el tipo **"Microsoft Foundry project"**, NO la cuenta principal/recurso hub padre. Son recursos diferentes con distintos alcances RBAC.
4. En la navegación izquierda de la página del proyecto, haz clic en **Control de acceso (IAM)**.
5. Haz clic en la pestaña **Asignaciones de roles** para verificar si ya tienes el rol:
   - Busca tu nombre o correo electrónico.
   - Si `Azure AI User` ya está listado → el error tiene otra causa (revisa el paso 8 abajo).
   - Si no está listado → procede a agregarlo.
6. Haz clic en **+ Agregar** → **Agregar asignación de rol**.
7. En la pestaña **Rol**:
   - Busca [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Selecciónalo en los resultados.
   - Haz clic en **Siguiente**.
8. En la pestaña **Miembros**:
   - Selecciona **Usuario, grupo o entidad de servicio**.
   - Haz clic en **+ Seleccionar miembros**.
   - Busca tu nombre o correo electrónico.
   - Selecciónate en los resultados.
   - Haz clic en **Seleccionar**.
9. Haz clic en **Revisar + asignar** → **Revisar + asignar** de nuevo.
10. **Espera 1-2 minutos** - los cambios RBAC tardan en propagarse.
11. Reintenta la operación que falló.

> **Por qué Owner/Contributor no es suficiente:** Azure RBAC tiene dos tipos de permisos: *acciones de gestión* y *acciones de datos*. Owner y Contributor conceden acciones de gestión (crear recursos, editar configuraciones), pero las operaciones de agente requieren la acción de datos `agents/write`, incluida solo en roles `Azure AI User`, `Azure AI Developer` o `Azure AI Owner`. Consulta [documentación RBAC de Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante aprovisionamiento de recurso

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Causa raíz:** No tienes permiso para crear o modificar recursos de Azure en esta suscripción/grupo de recursos.

**Solución:**
1. Pide a tu administrador de suscripciones que te asigne el rol **Contributor** en el grupo de recursos donde esté tu proyecto Foundry.
2. Alternativamente, pídele que cree el proyecto Foundry por ti y te conceda **Azure AI User** en el proyecto.

### 1.3 `SubscriptionNotRegistered` para [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Causa raíz:** La suscripción de Azure no ha registrado el proveedor de recursos necesario para Foundry.

**Solución:**

1. Abre un terminal y ejecuta:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Espera a que se complete el registro (puede tardar 1-5 minutos):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Salida esperada: `"Registered"`
3. Reintenta la operación.

---

## 2. Errores de Docker (solo si Docker está instalado)

> Docker es **opcional** para este taller. Estos errores solo aplican si tienes Docker Desktop instalado y la extensión Foundry intenta construir un contenedor localmente.

### 2.1 Demonio Docker no está ejecutándose

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Solución - paso a paso:**

1. **Encuentra Docker Desktop** en el menú Inicio (Windows) o Aplicaciones (macOS) y ejecútalo.
2. Espera a que la ventana de Docker Desktop muestre **"Docker Desktop is running"** - normalmente toma 30-60 segundos.
3. Busca el icono de la ballena de Docker en la bandeja del sistema (Windows) o barra de menú (macOS). Pasa el cursor sobre él para confirmar el estado.
4. Verifica en un terminal:
   ```powershell
   docker info
   ```
   Si imprime información del sistema Docker (Versión del servidor, Storage Driver, etc.), Docker está funcionando.
5. **Específico para Windows:** Si Docker aún no inicia:
   - Abre Docker Desktop → **Configuración** (icono de engranaje) → **General**.
   - Asegúrate que **Usar motor basado en WSL 2** esté marcado.
   - Haz clic en **Aplicar y reiniciar**.
   - Si WSL 2 no está instalado, ejecuta `wsl --install` en PowerShell elevado y reinicia el equipo.
6. Reintenta el despliegue.

### 2.2 Fallo en la construcción Docker con errores de dependencias

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Solución:**
1. Abre `requirements.txt` y verifica que todos los nombres de paquetes estén escritos correctamente.
2. Asegúrate de que las versiones estén fijadas correctamente:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Prueba la instalación local primero:
   ```bash
   pip install -r requirements.txt
   ```
4. Si usas un índice privado de paquetes, asegúrate que Docker tenga acceso de red a él.

### 2.3 Desajuste de plataforma del contenedor (Apple Silicon)

Si despliegas desde un Mac con Apple Silicon (M1/M2/M3/M4), el contenedor debe construirse para `linux/amd64` porque el runtime de contenedores de Foundry usa AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> El comando de despliegue de la extensión Foundry maneja esto automáticamente en la mayoría de los casos. Si ves errores relacionados con la arquitectura, construye manualmente con la bandera `--platform` y contacta al equipo de Foundry.

---

## 3. Errores de autenticación

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) falla al obtener un token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Causa raíz:** Ninguna de las fuentes de credenciales en la cadena `DefaultAzureCredential` tiene un token válido.

**Solución - prueba cada paso en orden:**

1. **Reinicia sesión vía Azure CLI** (la solución más común):
   ```bash
   az login
   ```
   Se abrirá una ventana del navegador. Inicia sesión y vuelve a VS Code.

2. **Configura la suscripción correcta:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Si no es la suscripción correcta:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Reinicia sesión vía VS Code:**
   - Haz clic en el icono **Cuentas** (icono de persona) en la esquina inferior izquierda de VS Code.
   - Haz clic en tu nombre de cuenta → **Cerrar sesión**.
   - Haz clic nuevamente en el icono Cuentas → **Iniciar sesión en Microsoft**.
   - Completa el flujo de inicio de sesión en el navegador.

4. **Entidad de servicio (para escenarios CI/CD solamente):**
   - Configura estas variables de entorno en tu `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Luego reinicia el proceso del agente.

5. **Verifica la caché de tokens:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Si falla, tu token CLI ha expirado. Vuelve a ejecutar `az login`.

### 3.2 El token funciona localmente pero no en despliegue alojado

**Causa raíz:** El agente alojado usa una identidad administrada por el sistema, distinta de tus credenciales personales.

**Solución:** Este comportamiento es esperado — la identidad administrada se provisiona automáticamente durante el despliegue. Si el agente alojado sigue dando errores de autenticación:
1. Verifica que la identidad administrada del proyecto Foundry tenga acceso al recurso Azure OpenAI.
2. Comprueba que `PROJECT_ENDPOINT` en `agent.yaml` es correcto.

---

## 4. Errores de modelo

### 4.1 Implementación de modelo no encontrada

```
Error: Model deployment not found / The specified deployment does not exist
```

**Solución - paso a paso:**

1. Abre tu archivo `.env` y anota el valor de `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Abre la barra lateral **Microsoft Foundry** en VS Code.
3. Expande tu proyecto → **Model Deployments**.
4. Compara el nombre de la implementación que aparece allí con el valor en `.env`.
5. El nombre es **sensible a mayúsculas y minúsculas** - `gpt-4o` es diferente de `GPT-4o`.
6. Si no coinciden, actualiza tu `.env` para usar el nombre exacto mostrado en la barra lateral.
7. Para despliegue alojado, actualiza también `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 El modelo responde con contenido inesperado

**Solución:**
1. Revisa la constante `EXECUTIVE_AGENT_INSTRUCTIONS` en `main.py`. Asegúrate que no esté truncada ni corrupta.
2. Verifica la configuración de temperatura del modelo (si es configurable) - valores bajos generan salidas más deterministas.
3. Compara el modelo desplegado (p. ej., `gpt-4o` vs `gpt-4o-mini`) - modelos diferentes tienen capacidades diferentes.

---

## 5. Errores de despliegue

### 5.1 Autorización para pull en ACR

```
Error: AcrPullUnauthorized
```

**Causa raíz:** La identidad administrada del proyecto Foundry no puede bajar la imagen del contenedor desde Azure Container Registry.

**Solución - paso a paso:**

1. Abre [https://portal.azure.com](https://portal.azure.com).
2. Busca **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** en la barra de búsqueda superior.
3. Haz clic en el registro asociado a tu proyecto Foundry (normalmente está en el mismo grupo de recursos).
4. En la navegación izquierda, haz clic en **Control de acceso (IAM)**.
5. Haz clic en **+ Agregar** → **Agregar asignación de rol**.
6. Busca **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** y selecciónalo. Haz clic en **Siguiente**.
7. Selecciona **Identidad administrada** → haz clic en **+ Seleccionar miembros**.
8. Busca y selecciona la identidad administrada del proyecto Foundry.
9. Haz clic en **Seleccionar** → **Revisar + asignar** → **Revisar + asignar**.

> Esta asignación de rol normalmente se configura automáticamente por la extensión Foundry. Si ves este error, la configuración automática pudo haber fallado. También puedes intentar redeplegar; la extensión podría reintentar la configuración.

### 5.2 El agente falla al iniciar después del despliegue

**Síntomas:** El estado del contenedor queda en "Pending" por más de 5 minutos o muestra "Failed".

**Solución - paso a paso:**

1. Abre la barra lateral **Microsoft Foundry** en VS Code.
2. Haz clic en tu agente alojado → selecciona la versión.
3. En el panel detallado, revisa **Container Details** → busca una sección o enlace **Logs**.
4. Lee los logs de inicio del contenedor. Causas comunes:

| Mensaje en log | Causa | Solución |
|----------------|-------|----------|
| `ModuleNotFoundError: No module named 'xxx'` | Dependencia faltante | Añádela a `requirements.txt` y redepliega |
| `KeyError: 'PROJECT_ENDPOINT'` | Variable de entorno faltante | Añade la variable en `agent.yaml` bajo `env:` |
| `OSError: [Errno 98] Address already in use` | Conflicto de puerto | Asegúrate que `agent.yaml` tenga `port: 8088` y solo un proceso use ese puerto |
| `ConnectionRefusedError` | El agente no inició la escucha | Revisa `main.py` - la llamada `from_agent_framework()` debe ejecutarse al inicio |

5. Corrige el problema y luego redepliega siguiendo [Módulo 6](06-deploy-to-foundry.md).

### 5.3 El despliegue se agota por tiempo

**Solución:**
1. Verifica tu conexión a internet - el push de Docker puede ser grande (>100MB en el primer despliegue).
2. Si estás detrás de un proxy corporativo, asegúrate que la configuración proxy de Docker Desktop esté configurada: **Docker Desktop** → **Configuración** → **Recursos** → **Proxies**.
3. Intenta de nuevo - fallas transitorias de red pueden ocurrir.

---

## 6. Referencia rápida: roles RBAC

| Rol | Alcance típico | Qué concede |
|------|---------------|-------------|
| **Azure AI User** | Proyecto | Acciones de datos: construir, desplegar e invocar agentes (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Proyecto o Cuenta | Acciones de datos + creación de proyecto |
| **Azure AI Owner** | Cuenta | Acceso total + gestión de asignaciones de rol |
| **Azure AI Project Manager** | Proyecto | Acciones de datos + puede asignar Azure AI User a otros |
| **Contributor** | Suscripción/GR | Acciones de gestión (crear/eliminar recursos). **NO incluye acciones de datos** |
| **Owner** | Suscripción/GR | Acciones de gestión + asignación de roles. **NO incluye acciones de datos** |
| **Reader** | Cualquiera | Acceso solo lectura de gestión |

> **Resumen clave:** `Owner` y `Contributor` **NO** incluyen acciones de datos. Siempre necesitas un rol `Azure AI *` para operaciones de agente. El rol mínimo para este taller es **Azure AI User** en el alcance de **proyecto**.

---

## 7. Lista de verificación para completar el taller

Úsala como confirmación final de que has completado todo:

| # | Ítem | Módulo | ¿Aprobado? |
|---|-------|--------|------------|
| 1 | Todos los prerrequisitos instalados y verificados | [00](00-prerequisites.md) | |
| 2 | Herramientas Foundry y extensiones instaladas | [01](01-install-foundry-toolkit.md) | |
| 3 | Proyecto Foundry creado (o proyecto existente seleccionado) | [02](02-create-foundry-project.md) | |
| 4 | Modelo desplegado (p. ej., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Rol de usuario de Azure AI asignado a nivel de proyecto | [02](02-create-foundry-project.md) | |
| 6 | Proyecto de agente alojado preparado (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` configurado con PROJECT_ENDPOINT y MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instrucciones del agente personalizadas en main.py | [04](04-configure-and-code.md) | |
| 9 | Entorno virtual creado y dependencias instaladas | [04](04-configure-and-code.md) | |
| 10 | Agente probado localmente con F5 o terminal (4 pruebas básicas aprobadas) | [05](05-test-locally.md) | |
| 11 | Desplegado en Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Estado del contenedor muestra "Started" o "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Verificado en VS Code Playground (4 pruebas básicas aprobadas) | [07](07-verify-in-playground.md) | |
| 14 | Verificado en Foundry Portal Playground (4 pruebas básicas aprobadas) | [07](07-verify-in-playground.md) | |

> **¡Felicidades!** Si todos los elementos están marcados, has completado todo el taller. Has creado un agente alojado desde cero, lo has probado localmente, lo has desplegado en Microsoft Foundry y lo has validado en producción.

---

**Anterior:** [07 - Verify in Playground](07-verify-in-playground.md) · **Inicio:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso legal**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o imprecisiones. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de ningún malentendido o interpretación errónea derivada del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->