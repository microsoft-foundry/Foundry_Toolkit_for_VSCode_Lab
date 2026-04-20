# Laboratorio 02 - Flujo de Trabajo Multi-Agente: Evaluador de Ajuste Currículum → Empleo

## Ruta Completa de Aprendizaje

Esta documentación te guía para construir, probar y desplegar un **flujo de trabajo multi-agente** que evalúa el ajuste entre currículum y empleo utilizando cuatro agentes especializados orquestados mediante **WorkflowBuilder**.

> **Prerequisito:** Completa [Laboratorio 01 - Agente Único](../../lab01-single-agent/README.md) antes de comenzar el Laboratorio 02.

---

## Módulos

| # | Módulo | Qué harás |
|---|--------|-----------|
| 0 | [Prerrequisitos](00-prerequisites.md) | Verificar la finalización del Laboratorio 01, entender conceptos multi-agente |
| 1 | [Comprender Arquitectura Multi-Agente](01-understand-multi-agent.md) | Aprender WorkflowBuilder, roles de agentes, grafo de orquestación |
| 2 | [Estructurar el Proyecto Multi-Agente](02-scaffold-multi-agent.md) | Usar la extensión Foundry para estructurar un flujo de trabajo multi-agente |
| 3 | [Configurar Agentes y Entorno](03-configure-agents.md) | Escribir instrucciones para 4 agentes, configurar herramienta MCP, definir variables de entorno |
| 4 | [Patrones de Orquestación](04-orchestration-patterns.md) | Explorar fan-out paralelo, agregación secuencial y patrones alternativos |
| 5 | [Prueba Local](05-test-locally.md) | Depurar con F5 usando Agent Inspector, ejecutar pruebas básicas con currículum + descripción de trabajo |
| 6 | [Desplegar en Foundry](06-deploy-to-foundry.md) | Construir contenedor, subir a ACR, registrar agente hospedado |
| 7 | [Verificar en Playground](07-verify-in-playground.md) | Probar agente desplegado en VS Code y el playground de Foundry Portal |
| 8 | [Solución de Problemas](08-troubleshooting.md) | Corregir problemas comunes multi-agente (errores MCP, salida truncada, versiones de paquetes) |

---

## Tiempo estimado

| Nivel de experiencia | Tiempo |
|----------------------|---------|
| Completaste Laboratorio 01 recientemente | 45-60 minutos |
| Algo de experiencia con Azure AI | 60-90 minutos |
| Primera vez con multi-agente | 90-120 minutos |

---

## Arquitectura de un vistazo

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Volver a:** [Lectura del Laboratorio 02](../README.md) · [Inicio del Taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda la traducción profesional realizada por humanos. No nos responsabilizamos por malentendidos o interpretaciones erróneas que surjan del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->