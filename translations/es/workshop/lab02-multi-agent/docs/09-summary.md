# Módulo 9 - Resumen y próximos pasos

⏱️ ~5 min

**¡Felicidades!** Has construido, probado y (si estás en la Ruta A) desplegado un flujo de trabajo multiagente usando Microsoft Foundry y el Foundry Toolkit para VS Code.

---

## Lo que construiste

El **Evaluador de Ajuste Currículum → Puesto** - un flujo de trabajo multiagente alojado que:
- Recibe un currículum + descripción de puesto vía HTTP (`POST /responses`)
- Ejecuta cuatro agentes especializados en una pipeline secuencial - cada agente transmite los datos que su sucesor necesita
- Devuelve una puntuación de ajuste (0–100 con desglose), una lista de brechas en habilidades y certificaciones, y una hoja de ruta personalizada de aprendizaje con enlaces reales de Microsoft Learn para cada brecha
- Llama al servidor MCP de Microsoft Learn (`https://learn.microsoft.com/api/mcp`) para obtener recursos oficiales de aprendizaje para cada brecha de habilidad identificada
- Se ejecuta como un solo agente alojado containerizado en el Microsoft Foundry Agent Service

---

## Conceptos clave aprendidos

| Concepto | Lo que practicaste |
|---------|-------------------|
| **Orquestación multiagente** | `WorkflowBuilder` pipeline secuencial con `add_edge()` |
| **Especialización de agentes** | Cuatro agentes enfocados superan a un agente de propósito general |
| **Patrón Content Router** | ResumeParser también actúa como router - conserva el texto JD en una sección `[JOB DESCRIPTION PASS-THROUGH]` para que los agentes descendentes puedan acceder a él (requerido porque `context_mode="last_agent"` significa que solo el `start_executor` ve el mensaje crudo del usuario) |
| **Patrón Content Relay** | JD Agent transmite `[PARSED RESUME PASS-THROUGH]` adelante para que MatchingAgent obtenga ambos perfiles; evita el doble disparo semántico OR que causan los gráficos fan-in |
| **Integración herramienta MCP** | `@tool` + `streamable_http_client` llamando a un servidor externo MCP |
| **Ciclo de vida de un agente alojado** | Scaffold → Configurar → Probar localmente → Desplegar → Verificar en la nube |
| **`context_mode="last_agent"`** | Cada ejecutor ve solo la salida de su predecesor directo |
| **Flujo de trabajo Foundry Toolkit** | Asistente scaffold, Inspector de Agentes, Visualizador de flujo, despliegue con un clic |

---

## Lo que completaste

<details open>
<summary><strong>🅰️ Ruta A - Subscripción Foundry</strong></summary>

- [x] Verificado el setup del Laboratorio 01: proyecto, modelo, y RBAC aún activos
- [x] Scaffold de un proyecto multiagente usando la plantilla Workflows
- [x] Escribí cuatro conjuntos de instrucciones para agentes (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integré la herramienta MCP de Microsoft Learn con `streamable_http_client`
- [x] Conecté el grafo del flujo de trabajo con `WorkflowBuilder` (pipeline secuencial con content relay)
- [x] Probado localmente con 2 pruebas básicas (Agent Inspector) - puntuación de ajuste, tarjetas de brechas, y URLs MCP
- [x] Desplegado en Foundry Agent Service (containerizado, identidad administrada)
- [x] Verificado en playground en la nube - consistencia estructural con resultados locales

</details>

<details open>
<summary><strong>🅱️ Ruta B - Foundry Local</strong></summary>

- [x] Verificado el setup del Laboratorio 01: Foundry Local ejecutándose con un modelo local
- [x] Scaffold de un proyecto multiagente usando la plantilla Workflows
- [x] Escribí cuatro conjuntos de instrucciones para agentes y configuré el grafo del flujo de trabajo
- [x] Integré la herramienta MCP de Microsoft Learn
- [x] Probado localmente con 2 pruebas básicas
- [x] Validado el comportamiento multiagente sin necesidad de recursos en la nube

</details>

---

## Próximos pasos

### Continúa aprendiendo

| Recurso | Descripción |
|----------|-------------|
| **[Referencia del SDK Agent Framework](https://learn.microsoft.com/agent-framework/)** | Documentación API para `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Catálogo herramienta MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Conecta agentes a otros servidores MCP (Bing, GitHub, personalizado) |
| **[Agregar conocimiento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Fundamenta agentes con documentos, almacenes vectoriales o búsqueda Bing |
| **[Evaluaciones Foundry](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mide la calidad del agente a escala con evaluadores automáticos |
| **[Documentación Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referencia completa de la plataforma |
| **[Foundry Toolkit - Novedades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas de la versión de la extensión y registro de cambios |

### Ideas para extender este flujo de trabajo

- **Agregar un 5º agente** - Un coach de entrevistas que genera preguntas probables basadas en el reporte de brechas
- **Agregar una herramienta de fundamentación Bing** - Permite que el JD Agent busque ofertas laborales similares para enriquecer los requisitos
- **Conectar a una base de datos de currículums** - Extraer perfiles de candidatos de una base de datos vía un `@tool` personalizado
- **Probar modelos diferentes** - Comparar calidad y latencia de salida entre `gpt-4.1` y `gpt-4.1-mini`
- **Evaluar con Foundry** - Usar la función Evaluaciones para puntuar reportes de ajuste contra un conjunto de datos dorado

### Para usuarios de la Ruta B: Actualizar a despliegue en la nube

Cuando estés listo para desplegar en la nube:
1. Obtén una suscripción Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Completa [Laboratorio 01, Módulo 01](../../lab01-single-agent/docs/01-setup.md) (crear proyecto, desplegar modelo, asignar RBAC)
3. Actualiza tu `.env` con el endpoint del proyecto Foundry y el nombre del despliegue del modelo
4. Continua desde [Módulo 06 - Desplegar en Foundry](06-deploy-to-foundry.md)

---

## Limpieza de recursos (opcional)

Si quieres eliminar los recursos de Azure creados durante este taller:

### Opción 1: Eliminar el grupo de recursos (elimina todo)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opción 2: Eliminar solo el agente alojado

1. Abre [ai.azure.com](https://ai.azure.com) → tu proyecto → **Construir** → **Agentes**.
2. Encuentra **PersonalCareerCopilot** → haz clic en **Eliminar**.

### Opción 3: Eliminar el despliegue del modelo

1. En la barra lateral de Foundry, expande tu proyecto → **Modelos**.
2. Haz clic derecho en el despliegue del modelo → **Eliminar**.

> **Nota sobre costos:** Los agentes alojados solo generan costo cuando están activos. Si detienes o eliminas el agente, no hay cargos en curso. El despliegue del modelo puede generar un pequeño cargo por capacidad reservada - elimínalo si ya no lo necesitas.

---

**Anterior:** [08 - Solución de problemas](08-troubleshooting.md) · **Inicio:** [Lab 02 README](../README.md) · [Inicio del taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->