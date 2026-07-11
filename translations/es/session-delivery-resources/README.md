# Cómo impartir esta sesión

¡Gracias por impartir esta sesión!

Antes de impartir el taller, por favor:

1. Lea este documento y todos los recursos incluidos en su totalidad.
2. Mire la grabación de la entrega de la sesión y el recorrido completo del taller.
3. Realice ambos laboratorios prácticos completamente en su propia máquina **al menos una vez** antes del evento.
4. Valide su proyecto de Microsoft Foundry, los despliegues de modelos y las cuotas.
5. Contacte al mantenedor si algo no está claro.

---

## Resumen de archivos

| Recurso                      | Enlace                                                                           | Descripción                                                                               |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Presentación del taller          | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Diapositivas de presentación para este taller con notas del presentador y vídeos de demos integrados        |
| Grabación de la entrega de la sesión | _Será proporcionada por el mantenedor_                                               | Introducción del taller y grabación del repaso de las diapositivas                                              |
| Grabación completa del taller     | _Será proporcionada por el mantenedor_                                               | Grabación completa de ambos laboratorios desde la perspectiva de un aprendiz                              |
| Documentación del taller          | [Repositorio](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repositorio fuente, archivos README de los laboratorios, módulos paso a paso                                       |
| Laboratorio 01 - agente único     | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Laboratorio práctico: construir, probar y desplegar el agente alojado *Explain Like I'm an Executive*     |
| Laboratorio 02 - flujo multiagente | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Laboratorio práctico: construir el flujo de trabajo de 4 agentes *Resume to Job Fit Evaluator*                     |
| Demo 1: Agente Ejecutivo          | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Demo Laboratorio 01: traducir jerga técnica a un resumen ejecutivo                          |
| Demo 2: Evaluador de ajuste CV-Empleo | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demo Laboratorio 02: flujo de trabajo de 4 agentes que puntúa el ajuste CV-empleo y genera recomendaciones     |

> **Nota para los formadores:** La presentación y los enlaces a vídeos se añadirán cuando se publiquen las grabaciones. Hasta entonces, contacte al mantenedor (véase [Contactos](#contactos)) para obtener los activos más recientes.

---

## Comenzar

Este taller enseña a los desarrolladores a construir, probar y desplegar agentes de IA en el **Microsoft Foundry Agent Service** como **Agentes alojados** completamente desde VS Code, usando la extensión **Microsoft Foundry Toolkit**.

El taller está dividido en múltiples secciones que incluyen diapositivas, **2 demos en vivo** y **2 laboratorios prácticos**.

### Duración

#### Entrega completa (aproximadamente 2 horas)

| Tiempo          | Descripción                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Introducción: agentes alojados, Foundry Agent Service y toolkit      |
| 10:00 - 20:00   | Demo: Agente Ejecutivo completo                                     |
| 20:00 - 60:00   | Laboratorio 01 - agente único (construir, probar localmente, desplegar, espacio de pruebas)     |
| 60:00 - 110:00  | Laboratorio 02 - flujo de trabajo multiagente (Evaluador de ajuste CV-Empleo)         |
| 110:00 - 120:00 | Conclusión, preguntas y recursos para continuar aprendiendo                       |

#### Entrega corta (aproximadamente 75 minutos)

| Tiempo          | Descripción                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Introducción y resumen general                                           |
| 10:00 - 20:00 | Demo: Agente Ejecutivo                                        |
| 20:00 - 70:00 | Solo Laboratorio 01 (indicar a los asistentes el Laboratorio 02 como autodidacta)        |
| 70:00 - 75:00 | Conclusión y preguntas                                              |

### Preparación

| Recurso                       | Enlace                                                                                          | Descripción                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Documentación del taller        | [Repositorio](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Documentación y código fuente del taller                 |
| Instrucciones Laboratorio 01    | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Laboratorio práctico: agente alojado único                 |
| Instrucciones Laboratorio 02    | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Laboratorio práctico: flujo de trabajo multiagente                |
| Lista de requisitos previos      | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Herramientas, cuentas, y acceso a Azure necesarios        |
| Guía rápida agentes alojados (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Guía rápida oficial para desplegar un agente alojado con `azd` |
| Disponibilidad regional de agentes alojados | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Regiones soportadas para agentes alojados (vista previa)     |

### Requisitos del formador

Antes de impartir, asegúrese de tener:

- Una **suscripción de Azure** con permisos para crear recursos (Propietario o Colaborador en un grupo de recursos).
- Acceso a un **proyecto Microsoft Foundry** en una [región que soporta agentes alojados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Cuota para **gpt-4.1** (o **gpt-4.1-mini**) en su proyecto Foundry.
- Las siguientes herramientas instaladas:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Extensión Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opcional)
  - Python 3.10 o superior

Ejecute la [Guía rápida de agentes alojados con `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) al menos una vez antes de la entrega para tener un proyecto Foundry, despliegue de modelo y Azure Container Registry conocidos y funcionando si algún aprendiz se atasca.

---

## Recorrido por las diapositivas

La presentación sigue el mismo flujo que los laboratorios. Puntos de conversación sugeridos para cada sección:

| Sección                     | Mensaje clave                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Título y agenda            | Enmarcar el taller como *VS Code a Foundry* sin necesidad de cambiar de portal.                                |
| ¿Por qué agentes alojados?          | Tiempo de ejecución gestionado, despliegue basado en ACR, API compatible con OpenAI `/responses`, limitado a proyectos Foundry.        |
| Diagrama de arquitectura        | Recorrer la [arquitectura del README](../README.md#architecture): scaffold, Inspector, ACR, Agent Service.   |
| Anatomía de un agente alojado   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - qué hace cada archivo.                              |
| Demo en vivo: Agente Ejecutivo  | Cambiar a VS Code y ejecutar la demo completa en [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) (ver [Demo 1](#demo-1-agente-ejecutivo)). |
| Demo en vivo: Evaluador Ajuste CV-Empleo | Cambiar a VS Code y ejecutar la demo de 4 agentes en [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (ver [Demo 2](#demo-2-evaluador-de-ajuste-cv-empleo)). |
| Breve reseña del Laboratorio 01                | Entregar a los aprendices. Señalar [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Patrones multiagente        | Secuencial vs concurrente vs entrega - vista previa antes de comenzar el Laboratorio 02.                                           |
| Breve reseña del Laboratorio 02                | Entregar a los aprendices. Señalar [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Conclusión y recursos       | Enlaces para continuar aprendiendo desde la sección [Recursos adicionales](#recursos-adicionales).                      |

---

## Demos

Se incluyen dos demos en vivo en la entrega. Asigne 10 minutos para cada una.

| Demo | Laboratorio | Archivos | Qué mostrar |
|------|------------|----------|-------------|
| Agente Ejecutivo | Laboratorio 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Agente alojado único; traducir jerga técnica a un resumen ejecutivo |
| Evaluador de ajuste CV-Empleo | Laboratorio 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orquestación de 4 agentes; puntúa ajuste CV-empleo y genera una recomendación |

### Demo 1: Agente Ejecutivo

Un agente independiente en [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Úselo como demo de 10 minutos antes del Laboratorio 01.

1. Abra [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) y revise la definición del agente (prompt del sistema, modelo, framework).
2. Presione `F5` para lanzar el **Inspector de Agentes** localmente.
3. Pegue el prompt de ejemplo del [README](../README.md#see-it-in-action) y muestre la respuesta del resumen ejecutivo.
4. Muestre [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) y [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) para explicar los artefactos de despliegue.
5. Demuestre el flujo de despliegue (construcción Docker, push a ACR, creación de agente alojado) sin esperar a que termine.

### Demo 2: Evaluador de ajuste CV-Empleo

Un flujo de trabajo de 4 agentes en [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Úselo como demo de 10 minutos antes del Laboratorio 02.

1. Abra [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) y muestre cómo se conectan los cuatro agentes en una orquestación secuencial.
2. Presione `F5` para lanzar el **Inspector de Agentes** para el flujo multiagente.
3. Pegue una descripción corta del puesto y un CV de muestra en el chat del Inspector.
4. Revise la canalización de cuatro agentes: analizador de CV, extractor de requisitos del puesto, evaluador de ajuste y escritor de recomendaciones.
5. Señale cómo la salida de cada sub-agente se convierte en el contexto para el siguiente agente, destacando el patrón de entrega.
6. Muestre [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) para comparar con el equivalente de agente único del Demo 1.

---

## Consejos para la entrega

- **Establezca expectativas temprano.** Los agentes alojados están en vista previa – destaque los límites regionales y las cuotas desde el principio para que los asistentes no se sorprendan a mitad del laboratorio.
- **Ejecute primero la tarea de requisitos previos.** Ambos laboratorios incluyen una tarea de VS Code llamada `Validate prerequisites` – haga que los asistentes la ejecuten antes de escribir cualquier código.
- **Mantenga visible el Inspector de Agentes.** La mayoría de los momentos “aha” ocurren cuando los aprendices ven iluminarse el ida y vuelta local de `/responses`.
- **Tenga un proyecto de respaldo.** Si el proyecto Foundry de un aprendiz llega a un tope de cuota, comparta un proyecto pre-provisionado para el paso de despliegue en lugar de bloquear el grupo.
- **Empareje a los asistentes.** El Laboratorio 02 (multi-agente) es mucho más fácil cuando los aprendices pueden discutir la orquestación con un compañero.
- **Use los módulos de la documentación como puntos de control.** La carpeta `docs/` de cada laboratorio está dividida en 8 módulos numerados – úselos como puntos naturales de pausa.
- **Precargue la imagen base Docker** en máquinas de laboratorio compartidas para evitar límites de tasa del registro.

---

## Solución de problemas durante la entrega

| Síntoma                                      | Primera cosa que intentar                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| El Inspector de Agentes no puede conectar               | Confirme que el puerto `8088` está libre y que la tarea `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` está en ejecución.   |
| El depurador no se conecta                     | Verifique que el puerto `5679` esté libre; reinicie VS Code si `debugpy` ya está en uso.                           |
| `azd up` falla con error de autenticación               | Ejecute `az login` y `azd auth login`, asegurándose de que está seleccionado el tenant correcto.                              |
| El despliegue se queda atascado en push a ACR                 | Verifique que Docker Desktop esté en ejecución y que el usuario tenga permiso `AcrPush` en el registro.                              |
| El modelo devuelve 404 / deployment-not-found     | El nombre del despliegue del modelo en `agent.yaml` debe coincidir con el despliegue en el proyecto Foundry.              |

| Agente alojado atascado en `Provisioning`         | Verifique que la región del proyecto [soporte agentes alojados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) y que haya cuota disponible. |
| Playground devuelve 401                        | Reautentique la extensión Foundry desde la barra de actividad de VS Code.                                     |

Para una guía más profunda, cada laboratorio incluye su propio documento `08-troubleshooting.md` - dirija a los aprendices allí:

- Laboratorio 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Laboratorio 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Personalizando esta sesión

Usted puede adaptar el taller para su audiencia. Variaciones comunes:

- **Audiencias de backend:** dedique más tiempo a `agent.yaml`, Docker y ACR; reduzca la demo del playground.
- **Audiencias de ciudadanos-desarrolladores:** permanezca en la interfaz de la extensión Foundry para scaffolding; reduzca los pasos de la CLI.
- **Sesión de pista única de 60 minutos:** entregue solo la introducción, demo y Laboratorio 01.
- **Formato solo taller (sin diapositivas):** abra ambos README de los laboratorios y úselos como guion principal.

Si extiende los laboratorios, por favor contribuya con los cambios a través de PR para que otros formadores se beneficien.

---

## Recursos adicionales

- [Documentación de Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Resumen de agentes alojados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Inicio rápido: despliegue su primer agente alojado (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Despliegue un agente alojado (cómo hacerlo)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Marco de Agentes de Microsoft](https://github.com/microsoft/agents)
- [Kit de herramientas Microsoft Foundry para VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Contactos

Si tiene preguntas sobre cómo impartir esta sesión, por favor abra un issue en el [repositorio del taller](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) y etiquete al mantenedor.

| Rol                | Nombre           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Mantenedor / contacto| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->