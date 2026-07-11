# Módulo 7 - Verificar en Playground

⏱️ ~10 min

En este módulo, pruebas tu flujo de trabajo multi-agente desplegado en VS Code y el Portal Foundry, confirmando que el agente se comporta igual que en las pruebas locales.

---

## ¿Por qué probar de nuevo después de desplegar?

El entorno alojado difiere del local en algunos aspectos importantes:

| | Local | Alojado |
|--|-------|--------|
| **Identidad** | Tu inicio de sesión personal (`DefaultAzureCredential`) | Identidad Entra dedicada por agente (provisionada automáticamente en el momento del despliegue) |
| **Punto final** | `http://localhost:8088/responses` | URL gestionada por Foundry Agent Service |
| **Red** | Tu máquina → Azure OpenAI + MCP | Backbone de Azure (latencia menor) |

Una variable de entorno mal configurada, un problema de RBAC, o una llamada MCP saliente bloqueada se mostrarían aquí primero.

---

## Opción A: Probar en VS Code Playground (se recomienda primero)

### Paso 1: Navega a tu agente alojado

1. Haz clic en el ícono **Foundry Toolkit** en la barra de actividades.
2. Expande tu proyecto → **Hosted Agents (Preview)** → encuentra tu agente.

![Foundry Toolkit sidebar mostrando Hosted Agents (Preview) con resume-job-fit-evaluator y sus versiones desplegadas](../../../../../translated_images/es/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Paso 2: Selecciona una versión

1. Haz clic en el agente para expandir sus versiones.
2. Haz clic en `v1` → verifica que el estado sea **activo** (la barra lateral puede mostrar "Running" o "Started"; ambos indican el mismo estado listo).

### Paso 3: Abre el Playground

1. Haz clic en **Playground** (o clic derecho en la versión → **Open in Playground**).
2. Se abre una ventana de chat en una pestaña de VS Code.

### Paso 4: Ejecuta tus pruebas iniciales

Usa las mismas 3 pruebas del [Módulo 5](05-test-locally.md). Escribe cada mensaje en la caja de entrada del Playground y presiona **Enviar** (o **Enter**).

#### Prueba 1 - Currículum completo + JD (flujo estándar)

Pega el prompt de currículum completo + JD del Módulo 5, Prueba 1 (Jane Doe + Senior Cloud Engineer en Contoso Ltd).

**Esperado:**
- Puntuación de ajuste con desglose matemático (escala de 100 puntos)
- Sección de habilidades coincidentes
- Sección de habilidades faltantes
- **Una tarjeta de brecha por cada habilidad faltante** con URLs de Microsoft Learn
- Hoja de ruta de aprendizaje con línea de tiempo

#### Prueba 2 - Prueba rápida corta (entrada mínima)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Esperado:**
- Puntuación de ajuste más baja (< 40)
- Evaluación honesta con camino de aprendizaje por etapas
- Múltiples tarjetas de brecha (AWS, Kubernetes, Terraform, CI/CD, brecha de experiencia)

#### Prueba 3 - Candidato con alta coincidencia

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Esperado:**
- Alta puntuación de ajuste (≥ 80)
- Enfoque en preparación para entrevistas y pulido
- Pocas o ninguna tarjeta de brecha
- Línea de tiempo corta enfocada en preparación

### Paso 5: Compara con resultados locales

Abre tus notas o pestaña del navegador del Módulo 5 donde guardaste las respuestas locales. Para cada prueba:

- ¿La respuesta tiene la **misma estructura** (puntuación de ajuste, tarjetas de brechas, hoja de ruta)?
- ¿Sigue la **misma rúbrica de puntuación** (desglose en escala de 100 puntos)?
- ¿Las **URLs de Microsoft Learn** siguen presentes en las tarjetas de brecha?
- ¿Hay **una tarjeta de brecha por cada habilidad faltante** (no truncada)?

> **Diferencias menores en redacción son normales** - el modelo es no determinista. Céntrate en la estructura, consistencia de puntuación y uso de la herramienta MCP.

---

## Opción B: Probar en el Portal Foundry

El [Portal Foundry](https://ai.azure.com) ofrece un playground basado en web útil para compartir con compañeros o interesados.

### Paso 1: Abre el Portal Foundry

1. Abre tu navegador y navega a [https://ai.azure.com](https://ai.azure.com).
2. Inicia sesión con la misma cuenta de Azure que has usado durante el taller.

### Paso 2: Navega a tu proyecto

1. En la página de inicio, busca **Proyectos recientes** en la barra lateral izquierda.
2. Haz clic en el nombre de tu proyecto (por ejemplo, `workshop-agents`).
3. Si no lo ves, haz clic en **Todos los proyectos** y búscalo.

### Paso 3: Encuentra tu agente desplegado

1. En la navegación izquierda del proyecto, haz clic en **Build** → **Agents** (o busca la sección **Agents**).
2. Deberías ver una lista de agentes. Encuentra tu agente desplegado (p. ej., `resume-job-fit-evaluator`).
3. Haz clic en el nombre del agente para abrir su página de detalles.

### Paso 4: Abre el Playground

1. En la página de detalles del agente, mira la barra de herramientas superior.
2. Haz clic en **Open in playground** (o **Try in playground**).
3. Se abre una interfaz de chat.

### Paso 5: Ejecuta las mismas pruebas iniciales

Repite las 3 pruebas del apartado de VS Code Playground arriba. Compara cada respuesta con los resultados locales (Módulo 5) y los del VS Code Playground (Opción A).

---

## Verificación específica multi-agente

Más allá de la corrección básica, verifica estos comportamientos específicos multi-agente:

### Ejecución de herramienta MCP

| Verificar | Cómo verificar | Condición de aprobación |
|-------|---------------|----------------|
| Llamadas MCP exitosas | Las tarjetas de brechas contienen URLs de `learn.microsoft.com` | URLs reales, no mensajes de respaldo |
| Múltiples llamadas MCP | Cada brecha de prioridad Alta/Media tiene recursos | No solo la primera tarjeta de brecha |
| Respaldo MCP funciona | Si faltan URLs, verifica texto de respaldo | El agente aún produce tarjetas de brecha (con o sin URLs) |

### Coordinación entre agentes

| Verificar | Cómo verificar | Condición de aprobación |
|-------|---------------|----------------|
| Los 4 agentes se ejecutaron | La salida contiene puntuación de ajuste Y tarjetas de brecha | La puntuación viene de MatchingAgent, tarjetas de GapAnalyzer |
| Ejecución secuencial | El tiempo de respuesta es razonable (< 2 min) | Si > 3 min, verifica errores en el log de terminal |
| Integridad del flujo de datos | Las tarjetas de brecha referencian habilidades del informe de matching | No hay habilidades inventadas que no estén en el JD |

---

## Rúbrica de validación

Usa esta rúbrica para evaluar el comportamiento alojado de tu flujo multi-agente:

| # | Criterio | Condición de aprobación | ¿Aprobado? |
|---|----------|---------------|-------|
| 1 | **Corrección funcional** | El agente responde a currículum + JD con puntuación de ajuste y análisis de brechas | |
| 2 | **Consistencia de puntuación** | La puntuación de ajuste usa escala de 100 puntos con desglose matemático | |
| 3 | **Completitud de tarjetas de brecha** | Una tarjeta por cada habilidad faltante (sin truncar ni combinar) | |
| 4 | **Integración de herramienta MCP** | Las tarjetas de brecha incluyen URLs reales de Microsoft Learn | |
| 5 | **Consistencia estructural** | La estructura de salida coincide entre ejecuciones locales y alojadas | |
| 6 | **Tiempo de respuesta** | El agente alojado responde en menos de 2 minutos para evaluación completa | |
| 7 | **Sin errores** | No hay errores HTTP 500, tiempos de espera o respuestas vacías | |

> Un "aprobado" significa que se cumplen los 7 criterios para las 3 pruebas iniciales en al menos un playground (VS Code o Portal).

---

## Resolución de problemas en playground

| Síntoma | Causa probable | Solución |
|---------|-------------|-----|
| El playground no carga | Contenedor no está en estado `active` | Regresa a [Módulo 6](06-deploy-to-foundry.md), verifica estado del despliegue. Espera si está `creating` |
| El agente devuelve respuesta vacía | Nombre de despliegue de modelo incorrecto | Verifica en `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` que coincida con el modelo desplegado |
| El agente devuelve mensaje de error | Permiso [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) faltante | Asigna **[Foundry User](https://aka.ms/foundry-ext-project-role)** (antes Azure AI User) a nivel proyecto |
| No hay URLs de Microsoft Learn en tarjetas de brecha | Bloqueo de salida MCP o servidor MCP no disponible | Verifica si el contenedor puede acceder a `learn.microsoft.com`. Consulta [Módulo 8](08-troubleshooting.md) |
| Solo 1 tarjeta de brecha (truncada) | Falta el bloque "CRITICAL" en las instrucciones de GapAnalyzer | Revisa [Módulo 3, Paso 2.4](03-configure-agents.md) |
| Puntuación de ajuste muy diferente a la local | Modelo o instrucciones diferentes desplegados | Compara variables de entorno `agent.yaml` con `.env` local. Re-despliega si es necesario |
| "Agent not found" en Portal | Despliegue aún propagándose o falló | Espera 2 minutos, actualiza. Si sigue faltando, re-despliega desde [Módulo 6](06-deploy-to-foundry.md) |

---

### Punto de control

- [ ] Probado agente en VS Code Playground - las 3 pruebas iniciales pasaron
- [ ] Probado agente en Playground del [Portal Foundry](https://ai.azure.com) - las 3 pruebas iniciales pasaron
- [ ] Respuestas estructuralmente consistentes con pruebas locales (puntuación ajuste, tarjetas de brecha, hoja de ruta)
- [ ] URLs de Microsoft Learn presentes en tarjetas de brecha (herramienta MCP funcionando en entorno alojado)
- [ ] Una tarjeta de brecha por cada habilidad faltante (sin truncamientos)
- [ ] Sin errores ni tiempos de espera durante pruebas
- [ ] Rúbrica de validación completada (los 7 criterios cumplen)

---

**Anterior:** [06 - Deploy to Foundry](06-deploy-to-foundry.md) · **Siguiente:** [08 - Resolución de problemas →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->