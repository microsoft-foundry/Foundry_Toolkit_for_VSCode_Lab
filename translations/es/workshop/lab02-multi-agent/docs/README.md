# Laboratorio 02 - Flujo de Trabajo Multi-Agente: Evaluador de Ajuste Currículum → Trabajo

## Ruta de Aprendizaje Completa

Esta documentación te guía para construir, probar y desplegar un **flujo de trabajo multi-agente** que evalúa el ajuste currículum-trabajo usando cuatro agentes especializados orquestados mediante **WorkflowBuilder**.

> **Requisito previo:** Completa [Laboratorio 01 - Agente Único](../../lab01-single-agent/README.md) antes de comenzar el Laboratorio 02.

---

## Módulos

| # | Módulo | Lo que harás |
|---|--------|--------------|
| 0 | [Introducción](00-prerequisites.md) | Qué construirás, verificación del Laboratorio 01, comparación Laboratorio 02 vs Laboratorio 01 |
| 1 | [Comprender la Arquitectura Multi-Agente](01-understand-multi-agent.md) | Aprende WorkflowBuilder, roles de agentes, grafo de orquestación |
| 2 | [Escaffold del Proyecto Multi-Agente](02-scaffold-multi-agent.md) | Usa el asistente de extensión Foundry para generar el proyecto base |
| 3 | [Configurar Agentes y Entorno](03-configure-agents.md) | Escribe instrucciones para 4 agentes, configura la herramienta MCP, establece variables de entorno |
| 4 | [Patrones de Orquestación](04-orchestration-patterns.md) | Cadena secuencial, retransmisión de contenido y semántica OR de WorkflowBuilder |
| 5 | [Prueba Localmente](05-test-locally.md) | Depura con F5 usando Agent Inspector, ejecuta pruebas básicas con currículum + JD |
| 6 | [Desplegar en Foundry](06-deploy-to-foundry.md) | Construye el contenedor, sube a ACR, registra el agente alojado |
| 7 | [Verifica en Playground](07-verify-in-playground.md) | Prueba el agente desplegado en los playgrounds de VS Code y Foundry Portal |
| 8 | [Solución de Problemas](08-troubleshooting.md) | Soluciona problemas comunes multi-agente (errores MCP, salida truncada, versiones de paquetes) |
| 9 | [Resumen y Próximos Pasos](09-summary.md) | Lo que construiste, conceptos clave aprendidos, limpieza y hacia dónde ir después |

---

**Volver a:** [Laboratorio 02 README](../README.md) · [Inicio del Taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->