# Módulo 9 - Resumen y Próximos Pasos

⏱️ ~5 min

**¡Felicidades!** Has construido, probado y (si estás en el Camino A) desplegado un flujo de trabajo multi-agente usando Microsoft Foundry y Foundry Toolkit para VS Code.

---

## Lo que construiste

El **Evaluador de Ajuste Currículum → Trabajo** - un flujo de trabajo multi-agente alojado que:
- Recibe un currículum + descripción de trabajo vía HTTP (`POST /responses`)
- Ejecuta cuatro agentes especializados en una tubería secuencial - cada agente transmite los datos que su sucesor necesita
- Devuelve una puntuación de ajuste (0–100 con desglose), una lista de brechas de habilidades y certificaciones, y una hoja de ruta de aprendizaje personalizada con enlaces reales de Microsoft Learn para cada brecha
- Llama al servidor MCP de Microsoft Learn (`https://learn.microsoft.com/api/mcp`) para obtener recursos oficiales de aprendizaje para cada brecha identificada
- Funciona como un solo agente alojado en contenedor en Microsoft Foundry Agent Service

---

## Conceptos clave aprendidos

| Concepto | Lo que practicaste |
|---------|-------------------|
| **Orquestación multi-agente** | Tubería secuencial con `WorkflowBuilder` y `add_edge()` |
| **Especialización de agentes** | Cuatro agentes enfocados superan a un agente de propósito general |
| **Patrón Content Router** | ResumeParser funciona también como un enrutador - conserva el texto de JD en una sección `[JOB DESCRIPTION PASS-THROUGH]` para que los agentes posteriores puedan acceder a él (requerido porque `context_mode="last_agent"` significa que solo el `start_executor` ve el mensaje bruto del usuario) |
| **Patrón Content Relay** | El agente JD transmite hacia adelante `[PARSED RESUME PASS-THROUGH]` para que MatchingAgent obtenga ambos perfiles; evita el doble disparo semántico OR que causan los gráficos fan-in |
| **Integración de herramienta MCP** | `@tool` + `streamable_http_client` llamando a un servidor MCP externo |
| **Ciclo de vida de agente alojado** | Scaffold → Configurar → Probar localmente → Desplegar → Verificar en la nube |
| **`context_mode="last_agent"`** | Cada ejecutor ve solo la salida de su predecesor directo |
| **Flujo de trabajo Foundry Toolkit** | Asistente Scaffold, Inspector de Agente, Visualizador de Flujo, despliegue con un clic |

---

## Lo que completaste

<details open>
<summary><strong>🅰️ Camino A - Suscripción Foundry</strong></summary>

- [x] Verificada la configuración del Laboratorio 01: proyecto, modelo y RBAC todavía activos
- [x] Scaffolded un proyecto multi-agente usando la plantilla Workflows
- [x] Escribí cuatro conjuntos de instrucciones para agentes (ResumeParser, Agente JD, MatchingAgent, GapAnalyzer)
- [x] Integré la herramienta Microsoft Learn MCP con `streamable_http_client`
- [x] Conecté el gráfico de flujo con `WorkflowBuilder` (tubería secuencial con retransmisión de contenido)
- [x] Probado localmente con 3 pruebas rápidas (Agent Inspector) - puntuación de ajuste, tarjetas de brechas y URLs MCP
- [x] Desplegado en Foundry Agent Service (contenedor, identidad administrada)
- [x] Verificado en el playground en la nube - consistencia estructural con resultados locales

</details>

<details open>
<summary><strong>🅱️ Camino B - Foundry Local</strong></summary>

- [x] Verificada la configuración del Laboratorio 01: Foundry Local ejecutándose con un modelo local
- [x] Scaffolded un proyecto multi-agente usando la plantilla Workflows
- [x] Escribí cuatro conjuntos de instrucciones para agentes y conecté el gráfico de flujo
- [x] Integré la herramienta Microsoft Learn MCP
- [x] Probado localmente con 3 pruebas rápidas
- [x] Validado el comportamiento multi-agente sin necesidad de recursos en la nube

</details>

---

## Próximos pasos

### Continúa aprendiendo

| Recurso | Descripción |
|----------|-------------|
| **[Referencia Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentación API para `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catálogo de herramientas MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Conecta agentes a otros servidores MCP (Bing, GitHub, personalizado) |
| **[Agregar conocimiento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Fundamenta agentes con documentos, tiendas vectoriales o búsqueda Bing |
| **[Evaluaciones Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mide la calidad de agentes a escala con evaluadores automatizados |
| **[Documentación Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referencia completa de la plataforma |
| **[Foundry Toolkit - Novedades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas de lanzamiento y registro de cambios de la extensión |

### Ideas para extender este flujo de trabajo

- **Agregar un 5.º agente** - Un coach de entrevistas que genere posibles preguntas basadas en el reporte de brechas
- **Agregar una herramienta de fundamentación Bing** - Permitir que el agente JD busque ofertas de trabajo similares para enriquecer requisitos
- **Conectar a una base de datos de currículums** - Obtener perfiles de candidatos desde una base de datos mediante un `@tool` personalizado
- **Probar diferentes modelos** - Comparar calidad y latencia de salida de `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluar con Foundry** - Usar la función de Evaluaciones para puntuar informes de ajuste contra un conjunto de datos de referencia

### Para usuarios del Camino B: Actualizar a despliegue en la nube

Cuando estés listo para desplegar en la nube:
1. Obtén una suscripción Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Completa [Laboratorio 01, Módulo 01](../../lab01-single-agent/docs/01-setup.md) (crear proyecto, desplegar modelo, asignar RBAC)
3. Actualiza tu `.env` con el endpoint del proyecto Foundry y el nombre del despliegue del modelo
4. Continúa en [Módulo 06 - Desplegar en Foundry](06-deploy-to-foundry.md)

---

## Limpieza de recursos (opcional)

Si deseas eliminar los recursos de Azure creados durante este taller:

### Opción 1: Eliminar el grupo de recursos (elimina todo)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opción 2: Eliminar solo el agente alojado

1. Abre [ai.azure.com](https://ai.azure.com) → tu proyecto → **Build** → **Agents**.
2. Busca **PersonalCareerCopilot** → haz clic en **Delete**.

### Opción 3: Eliminar el despliegue del modelo

1. En la barra lateral de Foundry, expande tu proyecto → **Models**.
2. Haz clic derecho sobre el despliegue del modelo → **Delete**.

> **Nota de costos:** Los agentes alojados solo generan coste cuando están funcionando. Si detienes o eliminas el agente, no hay cargo recurrente. El despliegue del modelo puede generar un pequeño cargo por capacidad reservada; elimínalo si ya no lo necesitas.

---

**Anterior:** [08 - Solución de problemas](08-troubleshooting.md) · **Inicio:** [Lab 02 README](../README.md) · [Inicio del Taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->