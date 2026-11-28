# Módulo 0 - Introducción

⏱️ ~10 min

> [!WARNING]
> **Vista previa y limitaciones:** [Agentes alojados](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) están actualmente en **vista previa pública** - no se recomienda para cargas de trabajo en producción. Ten en cuenta lo siguiente:
> - **Las regiones soportadas son limitadas** - consulta la [disponibilidad por región](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) antes de crear recursos. Si eliges una región no soportada, la implementación fallará.
> - El paquete `agent-framework-foundry-hosting` está en versión preliminar - las API pueden cambiar entre versiones.
> - Límites de escala: los agentes alojados soportan de 0 a 5 réplicas (incluido escalar a cero).
> - Algunas características mostradas en este taller pueden cambiar a medida que el servicio se acerca a GA.

## Lo que construirás

En este taller, construirás un agente **"Explícame como si fuera un ejecutivo"** - un agente de IA alojado que toma actualizaciones técnicas complejas y las reescribe como resúmenes ejecutivos en inglés sencillo.

```mermaid
flowchart LR
    A["🧑‍💻 You send a\ntechnical update"] --> B["🤖 Executive Summary\nAgent"]
    B --> C["📝 Plain-English\nexecutive summary"]
```

**El agente usa:**
- **Microsoft Agent Framework** - para la lógica y estructura del agente
- **Foundry Toolkit para VS Code** - para scaffolding, pruebas locales y despliegue
- **Un modelo de IA** (por ejemplo, `gpt-4.1-mini/gpt-5-mini`) - para generar los resúmenes

Al final de este laboratorio, tendrás un agente funcional que podrás probar localmente mediante el Inspector de Agentes, y opcionalmente desplegar en la nube.

---

## ¿Qué son los agentes alojados?

Un **agente alojado** es un agente de IA que se ejecuta como un servicio gestionado en Microsoft Foundry. En lugar de administrar tu propia infraestructura, empaquetas el código de tu agente en un contenedor y Foundry maneja el escalado, alojamiento y exposición mediante un endpoint HTTP estándar.

| Concepto | Significado |
|---------|--------------|
| **Agente** | Tu código Python que recibe un mensaje del usuario, llama a un modelo de IA y devuelve una respuesta estructurada |
| **Alojado** | Foundry ejecuta tu contenedor por ti - sin máquinas virtuales, sin Kubernetes, sin infraestructura para gestionar |
| **Protocolo de respuestas** | Una API HTTP estándar (`POST /responses`) que cualquier cliente puede llamar para interactuar con tu agente |
| **Inspector de Agentes** | Una interfaz de prueba local (integrada en Foundry Toolkit) que te permite chatear con tu agente antes de desplegar |

En este taller, irás de cero a un agente completamente alojado - o puedes detenerte en la prueba local si lo prefieres.

---

## Elige tu camino

> ⚠️ **Elige un camino antes de continuar.** Tu elección determina qué herramientas instalar y qué módulos aplicar. Puedes cambiar de Camino B → Camino A más adelante si obtienes una suscripción.

<details open>
<summary><strong>🅰️ Camino A - nube Azure (requiere suscripción Azure)</strong></summary>

| | Detalles |
|---|---|
| **¿Para quién es?** | Tienes una suscripción Azure activa y puedes crear recursos Foundry |
| **Modelo** | Azure OpenAI vía Foundry (por ejemplo, `gpt-4.1-mini/gpt-5-mini`) |
| **Módulos cubiertos** | Todos los módulos (00–07) |
| **¿Desplegar en la nube?** | ✅ Sí - despliegue completo de extremo a extremo |

</details>

<details open>
<summary><strong>🅱️ Camino B - Local / nivel gratuito (no necesita suscripción Azure)</strong></summary>

| | Detalles |
|---|---|
| **¿Para quién es?** | MVPs, estudiantes, o cualquier persona sin acceso a Azure |
| **Modelo** | **Foundry Local** (gratuito, se ejecuta en tu máquina) |
| **Módulos cubiertos** | Módulos 00–04 (omitir deploy y verificación en la nube) |
| **¿Desplegar en la nube?** | ❌ No - solo pruebas locales vía Agent Inspector |

</details>

---

## Todas las rutas: Herramientas requeridas

Instala cada herramienta a continuación. Después de instalarlas, verifica que funcionen ejecutando el comando de comprobación.

| # | Herramienta | Versión | Instalación | Verificación (Salida esperada) |
|---|------|---------|---------|---------------------------|
| 1 | **Visual Studio Code** | Última | [code.visualstudio.com](https://code.visualstudio.com/) | Se abre sin errores |
| 2 | **Python** | 3.12 o superior| [python.org/downloads](https://www.python.org/downloads/) | `python --version` $\rightarrow$ `Python 3.12.x` |
| 3 | **Foundry Toolkit para VS Code** | Última | Extension ID: `ms-windows-ai-studio.windows-ai-studio` | Icono de Foundry en la barra de actividad |
| 4 | **Extensión de Python para VS Code** | Última | Extension ID: `ms-python.python` | Instalado en el panel de extensiones |

> [!TIP]
> **Consejos profesionales para la instalación:**
> - **Ruta de Python (Windows):** Siempre marca **"Agregar Python a PATH"** en la primera pantalla del instalador de Python. Sin esto, `python` no será reconocido en tu terminal.
> - **Múltiples versiones de Python:** Si tienes Python 3.10 y 3.12 instalados, usa `python3.12 -m venv .venv` para asegurarte de que la versión correcta se use para tu entorno virtual.
> - **Docker WSL 2 (Windows):** Durante la instalación de Docker Desktop, asegúrate de seleccionar el **backend WSL 2**. Docker con Hyper-V es más lento y puede causar problemas con la construcción de contenedores Foundry.
> - **¿Docker no inicia?** Espera 30–60 segundos después de lanzar Docker Desktop. Ejecuta `docker info` - si ves "Cannot connect to the Docker daemon," Docker todavía se está inicializando.
> - **¿Las extensiones de VS Code no cargan?** Después de instalar extensiones, recarga la ventana: `Ctrl+Shift+P` → `Developer: Reload Window`.

> **Usuarios de Windows:** Marquen **"Agregar Python a PATH"** durante la instalación de Python.



**Siguiente:** [01 - Configuración →](01-setup.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->