# Módulo 8 - Solución de problemas

Este módulo es una guía de referencia para problemas comunes. Agréguelo a favoritos y regrese cuando algo salga mal.

---

## 1. Errores de permisos

### 1.1 `agents/write` permiso denegado

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Causa raíz:** Falta el rol `Azure AI User` a nivel de **proyecto**. Este es el error #1 del taller.

**Solución:**
1. Abra [portal.azure.com](https://portal.azure.com).
2. Busque el nombre de su **proyecto** Foundry → haga clic en el resultado de tipo **"Microsoft Foundry project"** (NO cuenta principal).
3. **Control de acceso (IAM)** → **+ Agregar** → **Agregar asignación de rol**.
4. Rol: **Usuario de Azure AI** → Siguiente.
5. Miembros: Selecciónese a usted mismo → Revisar + asignar → Revisar + asignar.
6. **Espere 1–2 minutos** → intente de nuevo.

> **Por qué Propietario/Colaborador no es suficiente:** Estos roles otorgan solo acciones de *gestión*. Las operaciones del agente requieren la `agents/write` *acción de datos*, que solo está en `Azure AI User`, `Azure AI Developer`, o `Azure AI Owner`. Ver [documentación RBAC de Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante la provisión

**Solución:** Pida a su administrador asignar **Colaborador** en el grupo de recursos, o que creen el proyecto por usted y le otorguen **Usuario de Azure AI** en él.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Errores de Docker

> Docker es **opcional**. Esto solo aplica si Docker Desktop está instalado y la extensión intenta una compilación local.

### 2.1 Demonio de Docker no está en ejecución

**Solución:** Inicie Docker Desktop → espere a que el estado sea "en ejecución" → verifique con `docker info` → intente de nuevo.

### 2.2 La compilación falla por errores de dependencia

**Solución:** Verifique la ortografía de `requirements.txt`, pruebe localmente primero: `pip install -r requirements.txt`.

### 2.3 Incompatibilidad de plataforma (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Errores de autenticación

### 3.1 `DefaultAzureCredential` falla

**Solución (intente en orden):**
1. `az login` (reautenticar)
2. `az account set --subscription "<id>"` (suscripción correcta)
3. VS Code → Cuentas → Cerrar sesión → Iniciar sesión nuevamente
4. Verifique: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 El token funciona localmente pero no en hospedado

**Esperado:** Los agentes hospedados usan identidad administrada por el sistema, no su credencial. Si el agente hospedado recibe errores de autenticación:
- Verifique que `AZURE_AI_MODEL_DEPLOYMENT_NAME` en `agent.yaml` resuelve el nombre de despliegue de su modelo (`FOUNDRY_PROJECT_ENDPOINT` es inyectado por Foundry en tiempo de ejecución - no lo declare en `agent.yaml`)
- Compruebe que la identidad administrada del proyecto tenga acceso al modelo

---

## 4. Errores de modelo

### 4.1 Despliegue de modelo no encontrado

**Solución:** El nombre es **sensible a mayúsculas y minúsculas**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` con el nombre exacto en la barra lateral de Foundry → Modelos.

### 4.2 Salida inesperada del modelo

**Solución:** Revise `AGENT_INSTRUCTIONS` en `main.py` (¿no está truncado?). Pruebe un modelo diferente (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Errores de despliegue

### 5.1 ACR pull no autorizado

**Solución:** Portal de Azure → Registro de contenedores → Control de acceso (IAM) → Añadir rol **AcrPull** a la identidad administrada del proyecto Foundry.

### 5.2 El agente no arranca (permanece en "Pendiente" o "Fallado")

Verifique los logs del contenedor en la barra lateral. Causas comunes:

| Mensaje de log | Solución |
|-------------|-----|
| `ModuleNotFoundError` | Añada el paquete faltante a `requirements.txt`, vuelva a desplegar |
| `ValueError: Missing required environment variables` | Confirme que `AZURE_AI_MODEL_DEPLOYMENT_NAME` está declarado en `agent.yaml` bajo `environment_variables` y tiene un valor, luego vuelva a desplegar. `FOUNDRY_PROJECT_ENDPOINT` es inyectado por Foundry en tiempo de ejecución |
| `Address already in use` | Asegúrese de que solo un proceso esté enlazado al puerto 8088 |

### 5.3 El despliegue caduca

**Solución:** Verifique su conexión a internet. La primera implementación envía >100MB. ¿Detrás de un proxy? Configure la configuración del proxy en Docker Desktop.

---

## 6. Camino B - Foundry Local

### 6.1 Foundry Local no se inicia

| Problema | Solución |
|-------|-----|
| `foundry: command not found` | Reinstale: `winget install Microsoft.FoundryLocal` |
| Recursos insuficientes | Foundry Local necesita ~4GB de RAM libre. Cierre otras aplicaciones. |
| Fallo en descarga de modelo | Verifique espacio en disco (los modelos son de 2–8 GB). Reintente: `foundry local models pull <name>` |

### 6.2 Errores de modelo en Foundry Local

| Problema | Solución |
|-------|-----|
| Respuestas lentas | Esperado: los modelos locales se ejecutan en CPU a menos que tenga GPU. Sea paciente. |
| Salida de mala calidad | Pruebe un modelo más grande si su hardware lo permite. `phi-4-mini` es un buen equilibrio. |
| Conexión rechazada | Verifique que Foundry Local esté corriendo: `foundry local status`. Reinicie si es necesario. |

---

## 7. Referencia rápida: Roles RBAC

| Rol | Alcance | Otorga |
|------|-------|--------|
| **Usuario de Azure AI** | Proyecto | Acciones de datos: `agents/write`, `agents/read` |
| **Desarrollador de Azure AI** | Proyecto/Cuenta | Acciones de datos + creación de proyecto |
| **Propietario de Azure AI** | Cuenta | Acceso completo + gestión de roles |
| **Colaborador** | Suscripción/GR | Solo acciones de gestión (**no** acciones de datos) |
| **Propietario** | Suscripción/GR | Gestión + asignación de roles (**no** acciones de datos) |

---

## 8. Lista de verificación para completar el taller

| # | Elemento | Módulo |
|---|------|--------|
| 1 | Prerrequisitos instalados y verificados | [00](00-prerequisites.md) |
| 2 | Extensión Foundry Toolkit instalada, proyecto conectado (o Camino B configurado) | [01](01-setup.md) |
| 3 | Agente hospedado estructurado | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurado, instrucciones escritas, dependencias instaladas | [03](03-configure-and-code.md) |
| 5 | Agente probado localmente - pasan 3 escenarios funcionales | [04](04-test-locally.md) |
| 6 | Desplegado a Foundry (solo Camino A) | [05](05-deploy-to-foundry.md) |
| 7 | Pruebas de casos extremos / seguridad pasan en la nube (solo Camino A) | [06](06-verify-in-playground.md) |
| 8 | Resumen revisado, siguientes pasos identificados | [07](07-summary.md) |

---

**Anterior:** [07 - Resumen](07-summary.md) · **Inicio:** [README del taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->