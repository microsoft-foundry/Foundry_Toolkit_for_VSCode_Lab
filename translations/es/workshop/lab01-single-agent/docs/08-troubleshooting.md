# Módulo 8 - Solución de problemas

Este módulo es una guía de referencia para problemas comunes. Marque esta página y regrese cuando algo salga mal.

---

## 1. Errores de permisos

### 1.1 Permiso `agents/write` denegado

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Causa raíz:** Falta el rol `Azure AI User` a nivel de **proyecto**. Este es el error número 1 en el taller.

**Solución:**
1. Abra [portal.azure.com](https://portal.azure.com).
2. Busque el nombre de su **proyecto** Foundry → haga clic en el resultado de tipo **"Microsoft Foundry project"** (NO en la cuenta principal).
3. **Control de acceso (IAM)** → **+ Agregar** → **Agregar asignación de rol**.
4. Rol: **Azure AI User** → Siguiente.
5. Miembros: Selecciónese a usted mismo → Revisar + asignar → Revisar + asignar.
6. **Espere 1–2 minutos** → reintente.

> **Por qué Owner/Contributor no es suficiente:** Estos roles otorgan solo acciones de *gestión*. Las operaciones del agente requieren la *acción de datos* `agents/write`, que solo está en `Azure AI User`, `Azure AI Developer` o `Azure AI Owner`. Consulte [docs Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` durante la provisión

**Solución:** Pida a su administrador que le asigne **Contributor** en el grupo de recursos, o que cree el proyecto para usted y le conceda **Azure AI User** en él.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Esperar hasta: "Registrado"
```

---

## 2. Errores de Docker

> Docker es **opcional**. Estos solo aplican si Docker Desktop está instalado y la extensión intenta una compilación local.

### 2.1 El demonio de Docker no está en ejecución

**Solución:** Inicie Docker Desktop → espere a que el estado sea "en ejecución" → verifique con `docker info` → reintente.

### 2.2 La compilación falla con errores de dependencias

**Solución:** Verifique la ortografía de `requirements.txt`, pruebe localmente primero: `pip install -r requirements.txt`.

### 2.3 Incompatibilidad de plataforma (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Errores de autenticación

### 3.1 `DefaultAzureCredential` falla

**Solución (intente en orden):**
1. `az login` (reauthenticar)
2. `az account set --subscription "<id>"` (suscripción correcta)
3. VS Code → Cuentas → Cerrar sesión → Iniciar sesión de nuevo
4. Verifique: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 El token funciona localmente pero no en el hospedado

**Esperado:** Los agentes hospedados usan identidad administrada por el sistema, no sus credenciales. Si el agente hospedado obtiene errores de autenticación:
- Verifique que `AZURE_AI_PROJECT_ENDPOINT` en `agent.yaml` esté correcto
- Compruebe que la identidad administrada del proyecto tenga acceso al modelo

---

## 4. Errores de modelo

### 4.1 Despliegue del modelo no encontrado

**Solución:** El nombre es **sensible a mayúsculas y minúsculas**. Compare `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` con el nombre exacto en la barra lateral de Foundry → Modelos.

### 4.2 Salida inesperada del modelo

**Solución:** Revise `AGENT_INSTRUCTIONS` en `main.py` (¿no está truncado?). Pruebe un modelo diferente (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Errores de despliegue

### 5.1 Pull de ACR no autorizado

**Solución:** Portal de Azure → Registro de contenedores → Control de acceso (IAM) → Agregar rol **AcrPull** a la identidad administrada del proyecto Foundry.

### 5.2 El agente no inicia (permanece en "Pendiente" o "Error")

Revise los registros del contenedor en la barra lateral. Causas comunes:

| Mensaje de registro | Solución |
|-------------|-----|
| `ModuleNotFoundError` | Agregue el paquete faltante a `requirements.txt`, redepliegue |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Agregue variable de entorno a `agent.yaml` bajo `environment_variables` |
| `Address already in use` | Asegúrese de que solo un proceso esté enlazando el puerto 8088 |

### 5.3 Tiempo de despliegue agotado

**Solución:** Verifique la conexión a internet. El primer despliegue sube >100MB. ¿Está detrás de un proxy? Configure las opciones de proxy en Docker Desktop.

---

## 6. Camino B - Foundry Local

### 6.1 Foundry Local no inicia

| Problema | Solución |
|-------|-----|
| `foundry: command not found` | Reinstale: `winget install Microsoft.FoundryLocal` |
| Recursos insuficientes | Foundry Local requiere ~4GB de RAM libre. Cierre otras aplicaciones. |
| Descarga del modelo falla | Verifique el espacio en disco (los modelos pesan 2–8 GB). Reintente: `foundry local models pull <name>` |

### 6.2 Errores de modelo en Foundry Local

| Problema | Solución |
|-------|-----|
| Respuestas lentas | Esperado - los modelos locales se ejecutan en CPU a menos que tenga GPU. Sea paciente. |
| Salida de mala calidad | Pruebe un modelo más grande si su hardware lo permite. `phi-4-mini` es un buen equilibrio. |
| Conexión rechazada | Verifique que Foundry Local esté en ejecución: `foundry local status`. Reinicie si es necesario. |

---

## 7. Referencia rápida: roles RBAC

| Rol | Alcance | Otorga |
|------|-------|--------|
| **Azure AI User** | Proyecto | Acciones de datos: `agents/write`, `agents/read` |
| **Azure AI Developer** | Proyecto/Cuenta | Acciones de datos + creación de proyectos |
| **Azure AI Owner** | Cuenta | Acceso completo + gestión de roles |
| **Contributor** | Suscripción/Gupo de recursos | Solo acciones de gestión (**no** acciones de datos) |
| **Owner** | Suscripción/Grupo de recursos | Gestión + asignación de roles (**no** acciones de datos) |

---

## 8. Lista de verificación para completar el taller

| # | Ítem | Módulo |
|---|------|--------|
| 1 | Prerrequisitos instalados y verificados | [00](00-prerequisites.md) |
| 2 | Extensión Foundry Toolkit instalada, proyecto conectado (o Camino B configurado) | [01](01-setup.md) |
| 3 | Agente hospedado configurado | [02](02-create-hosted-agent.md) |
| 4 | `.env` configurado, instrucciones escritas, dependencias instaladas | [03](03-configure-and-code.md) |
| 5 | Agente probado localmente - 3 escenarios funcionales aprobados | [04](04-test-locally.md) |
| 6 | Desplegado en Foundry (solo Camino A) | [05](05-deploy-to-foundry.md) |
| 7 | Pruebas de casos límite/seguridad aprobadas en la nube (solo Camino A) | [06](06-verify-in-playground.md) |
| 8 | Resumen revisado, próximos pasos identificados | [07](07-summary.md) |

---

**Anterior:** [07 - Resumen](07-summary.md) · **Inicio:** [README del taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->