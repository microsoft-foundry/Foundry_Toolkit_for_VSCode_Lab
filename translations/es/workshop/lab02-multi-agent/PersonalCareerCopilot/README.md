# PersonalCareerCopilot - Evaluador de Compatibilidad de Currículum con el Trabajo

Una aplicación multiagente centrada en el flujo de trabajo que evalúa qué tan bien un currículum coincide con una descripción de trabajo, y luego genera una hoja de ruta de aprendizaje personalizada para cerrar las brechas.

---

## Agentes

| Agente | Rol | Herramientas |
|-------|------|-------|
| **ResumeParser** | Extrae habilidades, experiencia, certificaciones estructuradas del texto del currículum | - |
| **JobDescriptionAgent** | Extrae habilidades, experiencia, certificaciones requeridas/preferidas de una descripción de trabajo | - |
| **MatchingAgent** | Compara perfil vs requisitos → puntaje de compatibilidad (0-100) + habilidades coincidentes/faltantes | - |
| **GapAnalyzer** | Construye una hoja de ruta de aprendizaje personalizada con recursos de Microsoft Learn | `search_microsoft_learn_for_plan` (MCP) |

## Flujo de trabajo

```mermaid
flowchart LR
    UserInput["User Input: Resume + Job Description"] --> ResumeParser
    ResumeParser -- "parsed resume + JD relay" --> JobDescriptionAgent
    JobDescriptionAgent -- "JD requirements + resume relay" --> MatchingAgent
    MatchingAgent -- "fit report + gaps" --> GapAnalyzerMCP["Gap Analyzer +\nMicrosoft Learn MCP"]
    GapAnalyzerMCP --> FinalOutput["Final Output:\nFit Score + Roadmap"]
```

---

## Inicio rápido

### 1. Configurar el entorno

Esta carpeta es la implementación de referencia para el esqueleto basado en flujo de trabajo del Lab 02. Su `main.py` usa los bloques de instrucciones existentes más `WorkflowBuilder` para conectar los cuatro agentes.

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. Configurar credenciales

Crea un archivo `.env` en esta carpeta:

```powershell
copy .env .env.bak 2>$null; echo $null > .env
```

Edita `.env`:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| Valor | Dónde encontrarlo |
|-------|------------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Barra lateral de Foundry Toolkit → clic derecho en tu proyecto → **Copiar Endpoint del Proyecto** |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Barra lateral de Foundry → expandir proyecto → **Modelos + endpoints** → nombre de despliegue |

### 3. Ejecutar localmente

```powershell
python -m debugpy --listen 127.0.0.1:5679 main.py --port 8088
```

O usa la tarea de VS Code: `Ctrl+Shift+P` → **Tareas: Ejecutar tarea** → **Ejecutar servidor HTTP del agente**.

Para depuración con F5, usa **Depurar servidor HTTP local del agente**.

### 4. Probar con Agent Inspector

Abre Agent Inspector: `Ctrl+Shift+P` → **Foundry Toolkit: Abrir Agent Inspector**.

Pega este prompt de prueba:

```
Resume:
Jane Doe
Senior Software Engineer with 5 years of experience in Python, Django, and AWS.
Built microservices handling 10K+ requests/second. Led a team of 4 developers.
Certifications: AWS Solutions Architect Associate.
Education: B.S. Computer Science, State University.

Job Description:
Senior Cloud Engineer at Contoso Ltd.
Required: Python, Azure, Kubernetes, Terraform, CI/CD pipelines.
Preferred: Go, monitoring (Prometheus/Grafana), cost optimization.
Experience: 5+ years in cloud infrastructure.
Certifications: Azure Solutions Architect Expert preferred.
```

**Esperado:** Un puntaje de compatibilidad (0-100), habilidades coincidentes/faltantes y una hoja de ruta de aprendizaje personalizada con URLs de Microsoft Learn.

### 5. Desplegar en Foundry

`Ctrl+Shift+P` → **Foundry Toolkit: Desplegar agente alojado** → selecciona tu proyecto → confirma.

---

## Estructura del proyecto

```
PersonalCareerCopilot/
├── .env                ← Your credentials (git-ignored)
├── agent.yaml          ← Hosted agent definition (name, resources, env vars)
├── Dockerfile          ← Container image for Foundry deployment
├── main.py             ← 4-agent workflow (instructions, MCP tool, WorkflowBuilder)
└── requirements.txt    ← Python dependencies
```

## Archivos clave

### `agent.yaml`

Define el agente alojado para el Servicio de Agentes Foundry:
- `kind: hosted` - se ejecuta como un contenedor gestionado
- `protocols` - protocolo `responses` con `version: 2.0.0`, expone el endpoint HTTP `/responses`
- `environment_variables` - `AZURE_AI_MODEL_DEPLOYMENT_NAME` se declara aquí; `FOUNDRY_PROJECT_ENDPOINT` se inyecta automáticamente al desplegar

### `main.py`

Contiene:
- **Instrucciones del agente** - cuatro constantes `*_INSTRUCTIONS`, una por agente
- **Herramienta MCP** - `search_microsoft_learn_for_plan()` llama a `https://learn.microsoft.com/api/mcp` vía HTTP Streamable
- **Creación de agentes** - cuatro instancias `Agent()` + `AgentExecutor()` compartiendo un `FoundryChatClient`
- **Gráfico de flujo de trabajo** - `WorkflowBuilder` conecta agentes como una cadena secuencial: ResumeParser → JD Agent → MatchingAgent → GapAnalyzer
- **Inicio del servidor** - `ResponsesHostServer` se ejecuta en el puerto 8088

### `requirements.txt`

| Paquete | Propósito |
|---------|----------|
| `agent-framework-foundry` | Núcleo de ejecución: `Agent`, `AgentExecutor`, `WorkflowBuilder`, `@tool`, `FoundryChatClient` |
| `agent-framework-foundry-hosting` | Integración hosting Foundry + `ResponsesHostServer` |
| `mcp<2,>=1.24.0` | Cliente MCP para GapAnalyzer (`streamable_http_client`) |
| `debugpy` | Depuración Python (F5 en VS Code) |

---

## Solución de problemas

| Problema | Solución |
|-------|-----|
| `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` o `KeyError: 'AZURE_AI_MODEL_DEPLOYMENT_NAME'` | Crea `.env` con ambos `FOUNDRY_PROJECT_ENDPOINT` y `AZURE_AI_MODEL_DEPLOYMENT_NAME` configurados |
| `ModuleNotFoundError: No module named 'agent_framework'` | Activa venv y ejecuta `pip install -r requirements.txt` |
| No hay URLs de Microsoft Learn en la salida | Verifica conexión a internet hacia `https://learn.microsoft.com/api/mcp` |
| Solo 1 tarjeta de brecha (cortada) | Verifica que `GAP_ANALYZER_INSTRUCTIONS` incluya el bloque `CRITICAL:` |
| Puerto 8088 en uso | Detén otros servidores: `netstat -ano \| findstr :8088` |

Para solución detallada, consulta [Módulo 8 - Solución de Problemas](../docs/08-troubleshooting.md).

---

**Recorrido completo:** [Documentación Lab 02](../docs/README.md) · **Volver a:** [README Lab 02](../README.md) · [Inicio del taller](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->