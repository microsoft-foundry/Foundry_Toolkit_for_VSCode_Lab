# Módulo 7 - Resumen y próximos pasos

⏱️ ~5 min

**¡Felicidades!** Has construido, probado y (si estás en el Camino A) desplegado un agente de IA alojado usando Microsoft Foundry y Foundry Toolkit para VS Code.

---

## Lo que construiste

Un agente **"Explícalo como si fuera un Ejecutivo"** que:
- Recibe informes técnicos de incidentes o actualizaciones operativas vía HTTP (`POST /responses`)
- Los traduce a resúmenes ejecutivos en lenguaje sencillo
- Sigue un formato de salida estructurado (Qué pasó / Impacto en el negocio / Próximo paso)
- Rechaza solicitudes fuera de tema e intentos de inyección de instrucciones
- Funciona como un agente alojado contenedorizado en Microsoft Foundry Agent Service

---

## Conceptos clave aprendidos

| Concepto | Lo que practicaste |
|---------|-------------------|
| **Arquitectura del Agent Framework** | Pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Ciclo de vida del agente alojado** | Scaffold → Configurar → Probar localmente → Desplegar → Verificar en la nube |
| **Ingeniería del prompt del sistema** | Rol, audiencia, formato de salida, reglas, restricciones de seguridad y ejemplos |
| **Diferencias local vs. alojado** | Identidad (credencial personal vs. identidad gestionada), endpoint, ruta de red |
| **Límites de seguridad** | Defensa contra inyección de instrucciones, adherencia al rol, manejo elegante de casos extremos |
| **Flujo de trabajo Foundry Toolkit** | Creación de proyecto, despliegue del modelo, scaffolding de agente, Agent Inspector, despliegue con un clic |

---

## Lo que completaste

### Camino A (suscripción Foundry)

- [x] Configuraste Foundry Toolkit y creaste un proyecto Foundry con un modelo desplegado
- [x] Scaffoldaste un agente alojado con estructura de proyecto autogenerada
- [x] Escribiste instrucciones estructuradas para el agente con reglas de seguridad
- [x] Probaste localmente con 3 escenarios funcionales (Agent Inspector)
- [x] Desplegaste en Foundry Agent Service (contenedorizado)
- [x] Verificaste en el playground en la nube con 4 pruebas de casos extremos/seguridad

### Camino B (Foundry Local)

- [x] Configuraste Foundry Toolkit con un endpoint local para el modelo
- [x] Scaffoldaste un proyecto de agente alojado
- [x] Escribiste instrucciones estructuradas para el agente con reglas de seguridad
- [x] Probaste localmente con 3 escenarios funcionales
- [x] Validaste el comportamiento del agente sin necesidad de recursos en la nube

---

## Próximos pasos

### Continúa aprendiendo

| Recurso | Descripción |
|----------|-------------|
| **[Lab 02 - Orquestación Multi-Agente](../../lab02-multi-agent/docs/README.md)** | Construye un flujo de trabajo con 4 agentes (Currículum → Evaluador de ajuste laboral) con patrones de orquestación |
| **[Agrega herramientas a tu agente](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Conecta APIs, bases de datos o funciones personalizadas mediante el Catálogo de Herramientas |
| **[Agrega conocimiento (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Fundamenta tu agente con documentos, almacenes vectoriales o búsqueda Bing |
| **[Documentación de Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referencia completa de la plataforma |
| **[Referencia del Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Documentación API para el paquete `agent-framework` |
| **[Foundry Toolkit - Novedades](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notas de versión y registro de cambios de la extensión |

### Ideas para extender tu agente

- **Agrega una herramienta de fecha** - Permite que el agente incluya contexto "a día de hoy" en los resúmenes
- **Conéctate a una base de datos de incidentes** - Obtén detalles reales de incidentes mediante función de herramienta
- **Agrega una herramienta de fundamentación con Bing** - Permite que el agente consulte noticias recientes para contexto adicional
- **Prueba diferentes modelos** - Compara la calidad de salida entre `gpt-4.1` y `gpt-4.1-mini`
- **Evalúa con Foundry** - Usa la función Evaluaciones para medir la calidad del agente a gran escala

### Para usuarios del Camino B: Actualiza a despliegue en la nube

Cuando estés listo para desplegar en la nube:
1. Obtén una suscripción Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Completa [Módulo 01, Configuración](01-setup.md#step-2-set-up-based-on-your-access) (crea proyecto, despliega modelo, asigna RBAC)
3. Actualiza tu `.env` con el endpoint del proyecto Foundry y el nombre del despliegue del modelo
4. Continúa desde [Módulo 05 - Desplegar a Foundry](05-deploy-to-foundry.md)

---

## Limpieza de recursos (opcional)

Si deseas eliminar los recursos de Azure creados durante este taller:

### Opción 1: Eliminar el grupo de recursos (elimina todo)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opción 2: Eliminar solo el agente alojado

1. Abre [ai.azure.com](https://ai.azure.com) → tu proyecto → **Crear** → **Agentes**.
2. Haz clic en tu agente → haz clic en **Eliminar**.

### Opción 3: Eliminar el despliegue del modelo

1. En la barra lateral de Foundry, expande tu proyecto → **Modelos**.
2. Haz clic derecho en el despliegue del modelo → **Eliminar**.

> **Nota de costos:** Los agentes alojados solo generan costo cuando están en ejecución. Si detienes o eliminas el agente, no hay cargo continuo. El despliegue del modelo puede generar un pequeño cargo por capacidad reservada - elimínalo si has terminado.

---

**Anterior:** [06 - Verificar en Playground](06-verify-in-playground.md) · **Siguiente:** [08 - Solución de problemas (Referencia) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->