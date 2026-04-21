# Module 8 - Pag-troubleshoot (Multi-Agent)

Saklaw ng module na ito ang mga karaniwang error, pag-aayos, at mga estratehiya sa pag-debug na partikular sa multi-agent workflow. Para sa pangkalahatang mga isyu sa Foundry deployment, tingnan din ang [Lab 01 troubleshooting guide](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Mabilis na sanggunian: Error → Ayusin

| Error / Sintomas | Posibleng Sanhi | Ayusin |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Nawawala ang `.env` file o hindi na-set ang mga halaga | Gumawa ng `.env` na may `PROJECT_ENDPOINT=<your-endpoint>` at `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Hindi na-activate ang virtual environment o hindi na-install ang mga dependencies | Patakbuhin ang `.\.venv\Scripts\Activate.ps1` pagkatapos `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Hindi naka-install ang MCP package (nawala sa requirements) | Patakbuhin ang `pip install mcp` o siguraduhing kasama sa `requirements.txt` bilang transitive dependency |
| Nagsisimula ang Agent pero walang sagot | Mismatch sa `output_executors` o nawawalang mga edges | Siguraduhing `output_executors=[gap_analyzer]` at lahat ng edges ay nandiyan sa `create_workflow()` |
| Isa lang ang gap card (kulang ang iba) | Hindi kumpleto ang instruction ng GapAnalyzer | Idagdag ang `CRITICAL:` na talata sa `GAP_ANALYZER_INSTRUCTIONS` - tingnan ang [Module 3](03-configure-agents.md) |
| Ang fit score ay 0 o wala | Hindi nakatanggap ng upstream data ang MatchingAgent | Siguraduhing parehong nandiyan ang `add_edge(resume_parser, matching_agent)` at `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Tinanggihan ng MCP server ang tawag sa tool | Suriin ang koneksyon sa internet. Subukang buksan ang `https://learn.microsoft.com/api/mcp` sa browser. Subukang muli |
| Walang Microsoft Learn URLs sa output | Hindi nakarehistro ang MCP tool o maling endpoint | Siguraduhing `tools=[search_microsoft_learn_for_plan]` sa GapAnalyzer at tama ang `MICROSOFT_LEARN_MCP_ENDPOINT` |
| `Address already in use: port 8088` | Ginagamit ng ibang proseso ang port 8088 | Patakbuhin ang `netstat -ano \| findstr :8088` (Windows) o `lsof -i :8088` (macOS/Linux) at itigil ang prosesong salungat |
| `Address already in use: port 5679` | Conflict sa debugpy port | Itigil ang ibang debug sessions. Patakbuhin ang `netstat -ano \| findstr :5679` para hanapin at patayin ang proseso |
| Hindi nagbubukas ang Agent Inspector | Hindi pa ganap na nagsimula ang server o may port conflict | Maghintay para sa "Server running" na log. Suriin kung libre ang port 5679 |
| `azure.identity.CredentialUnavailableError` | Hindi naka-login sa Azure CLI | Patakbuhin ang `az login` pagkatapos i-restart ang server |
| `azure.core.exceptions.ResourceNotFoundError` | Hindi umiiral ang deployment ng modelo | Suriing tugma ang `MODEL_DEPLOYMENT_NAME` sa isang deployed na modelo sa iyong Foundry project |
| Status ng container na "Failed" pagkatapos ng deployment | Nag-crash ang container sa simula | Suriin ang logs ng container sa Foundry sidebar. Karaniwan: nawawalang env var o import error |
| Deployment ay "Pending" nang > 5 minuto | Matagal magsimula ng container o limitasyon sa resources | Maghintay hanggang 5 minuto para sa multi-agent (gumagawa ng 4 na instance ng agent). Kung nakatengga pa rin, suriin ang logs |
| `ValueError` mula sa `WorkflowBuilder` | Mali ang configuration ng graph | Siguraduhing naka-set ang `start_executor`, ang `output_executors` ay listahan, at walang circular edges |

---

## Mga isyu sa Environment at configuration

### Nawawala o mali ang mga value sa `.env`

Dapat ang `.env` file ay nasa direktoryo ng `PersonalCareerCopilot/` (kaparehong level ng `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Inaasahang nilalaman ng `.env`:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Paano hanapin ang PROJECT_ENDPOINT:** 
- Buksan ang **Microsoft Foundry** sidebar sa VS Code → right-click sa iyong project → **Copy Project Endpoint**. 
- O pumunta sa [Azure Portal](https://portal.azure.com) → iyong Foundry project → **Overview** → **Project endpoint**.

> **Paano hanapin ang MODEL_DEPLOYMENT_NAME:** Sa Foundry sidebar, palawakin ang project → **Models** → hanapin ang pangalan ng deployed model (hal. `gpt-4.1-mini`).

### Pagkakasunod-sunod ng precedence ng Env var

Gumagamit ang `main.py` ng `load_dotenv(override=False)`, ibig sabihin:

| Prayoridad | Pinagmulan | Sinusundan kapag parehong nakaset? |
|----------|--------|------------------------|
| 1 (pinakamataas) | Shell environment variable | Oo |
| 2 | `.env` file | Kung walang shell var na nakaset |

Ibig sabihin, ang Foundry runtime env vars (naka-set sa pamamagitan ng `agent.yaml`) ay nauuna kaysa sa `.env` values kapag naka-host na deployment.

---

## Version compatibility

### Package version matrix

Kinakailangan ng multi-agent workflow ang mga tiyak na version ng mga package. Nagdudulot ng runtime errors ang hindi tugmang mga bersyon.

| Package | Kailangang Bersyon | Command para Suriin |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | pinakabagong pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Karaniwang mga errors sa version

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Ayusin: i-upgrade sa rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` hindi makita o hindi compatible ang Inspector:**

```powershell
# Ayusin: mag-install gamit ang --pre na flag
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Ayusin: i-upgrade ang mcp package
pip install mcp --upgrade
```

### Pagsuri ng lahat ng version nang sabay-sabay

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Inaasahang output:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Mga isyu sa MCP tool

### Walang resulta mula sa MCP tool

**Sintomas:** Sinasabi ng Gap cards na "No results returned from Microsoft Learn MCP" o "No direct Microsoft Learn results found".

**Posibleng sanhi:**

1. **Isyu sa network** - Hindi maabot ang MCP endpoint (`https://learn.microsoft.com/api/mcp`).
   ```powershell
   # Subukan ang konektividad
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Kung mag-return ng `200`, abot-kamay ang endpoint.

2. **Masyadong espesipiko ang query** - Napaka-espesyal na pangalan ng skill para sa Microsoft Learn search.
   - Inaasahan ito para sa mga napaka-espesyal na kasanayan. May fallback URL ang tool sa sagot.

3. **MCP session timeout** - Nag-timeout ang Streamable HTTP connection.
   - Subukang muli ang request. Pansamantalang mga sesyon ang MCP at maaaring kailangang kumonekta uli.

### Paliwanag ng mga MCP logs

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Kahulugan | Gawin |
|-----|---------|--------|
| `GET → 405` | MCP client probes sa initialization | Normal lang - huwag pansinin |
| `POST → 200` | Matagumpay ang tawag sa tool | Inaasahan |
| `DELETE → 405` | MCP client probes sa cleanup | Normal lang - huwag pansinin |
| `POST → 400` | Bad request (mali ang query) | Suriin ang `query` parameter sa `search_microsoft_learn_for_plan()` |
| `POST → 429` | Rate limited | Maghintay at subukang muli. Bawasan ang `max_results` parameter |
| `POST → 500` | Error sa MCP server | Pansamantala - subukang muli. Kung patuloy, maaaring down ang Microsoft Learn MCP API |
| Connection timeout | Isyu sa network o MCP server hindi available | Suriin ang internet. Subukang `curl https://learn.microsoft.com/api/mcp` |

---

## Mga isyu sa Deployment

### Hindi magsimula ang container pagkatapos ng deployment

1. **Suriin ang logs ng container:**
   - Buksan ang **Microsoft Foundry** sidebar → palawakin ang **Hosted Agents (Preview)** → i-click ang iyong agent → palawakin ang version → **Container Details** → **Logs**.
   - Hanapin ang Python stack traces o error sa nawawalang module.

2. **Karaniwang mga pagkabigo sa pagsisimula ng container:**

   | Error sa logs | Sanhi | Ayusin |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Kulang sa `requirements.txt` na package | Idagdag ang package, i-redeploy |
   | `RuntimeError: Missing required environment variable` | Hindi na-set ang env vars sa `agent.yaml` | I-update ang `agent.yaml` → seksyon ng `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | Hindi na-configure ang Managed Identity | Awtomatikong sine-set ng Foundry - siguraduhing ginagamit ang extension sa deployment |
   | `OSError: port 8088 already in use` | Maling port na ini-expose sa Dockerfile o conflict sa port | Siguraduhing `EXPOSE 8088` sa Dockerfile at `CMD ["python", "main.py"]` |
   | Container lumabas na may code 1 | Hindi nahawakang exception sa `main()` | Subukan muna lokal ([Module 5](05-test-locally.md)) para ma-catch ang mga error bago ideploy |

3. **I-redeploy pagkatapos ayusin:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → piliin ang parehong agent → mag-deploy ng bagong version.

### Matagal ang deployment

Mas matagal magsimula ang mga multi-agent container dahil gumagawa ito ng 4 na instance ng agent sa pagsisimula. Karaniwang oras ng pagsisimula:

| Yugto | Inaasahang tagal |
|-------|------------------|
| Pag-build ng container image | 1-3 minuto |
| Pag-push ng image sa ACR | 30-60 segundo |
| Pagsisimula ng container (isang agent) | 15-30 segundo |
| Pagsisimula ng container (multi-agent) | 30-120 segundo |
| Available ang agent sa Playground | 1-2 minuto pagkatapos ng "Started" |

> Kung patuloy ang status na "Pending" ng higit sa 5 minuto, suriin ang logs ng container para sa mga error.

---

## Mga isyu sa RBAC at permiso

### `403 Forbidden` o `AuthorizationFailed`

Kailangan mo ang **[Azure AI User](https://aka.ms/foundry-ext-project-role)** na role sa iyong Foundry project:

1. Pumunta sa [Azure Portal](https://portal.azure.com) → resource ng iyong Foundry **project**.
2. I-click ang **Access control (IAM)** → **Role assignments**.
3. Hanapin ang iyong pangalan → siguraduhing nakalista ang **Azure AI User**.
4. Kung wala: **Add** → **Add role assignment** → hanapin ang **Azure AI User** → i-assign sa iyong account.

Tingnan ang dokumentasyon ng [RBAC para sa Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para sa detalye.

### Hindi ma-access ang deployment ng modelo

Kung nagpapakita ang agent ng mga error tungkol sa modelo:

1. Siguraduhing naka-deploy ang modelo: sa sidebar ng Foundry → palawakin ang proyekto → **Models** → tingnan kung nandun ang `gpt-4.1-mini` (o iyong modelo) na may status na **Succeeded**.
2. Siguraduhing tugma ang pangalan ng deployment: i-compare ang `MODEL_DEPLOYMENT_NAME` sa `.env` (o `agent.yaml`) sa totoong pangalan ng deployment sa sidebar.
3. Kung expired na ang deployment (free tier): i-redeploy mula sa [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Mga isyu sa Agent Inspector

### Nagbubukas ang Inspector pero "Disconnected" ang ipinapakita

1. Siguraduhing tumatakbo ang server: suriin ang "Server running on http://localhost:8088" sa terminal.
2. Suriin ang port `5679`: Kumokonekta ang Inspector gamit ang debugpy sa port 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. I-restart ang server at buksan muli ang Inspector.

### Bahagi lang ng sagot ang ipinapakita ng Inspector

Mahaba ang sagot ng multi-agent at dahan-dahang nagsi-stream nang incrementally. Maghintay hanggang matapos ang buong sagot (maaaring umabot sa 30-60 segundo depende sa bilang ng mga gap card at tawag sa MCP tool).

Kung palaging napuputol ang sagot:
- Suriin ang GapAnalyzer instructions na may `CRITICAL:` block na pumipigil sa pagsasama-sama ng mga gap card.
- Suriin ang token limit ng iyong modelo - sinusuportahan ng `gpt-4.1-mini` ang hanggang 32K output tokens, na dapat sapat na.

---

## Mga tip para sa pagganap

### Mabagal na mga sagot

Mas mabagal ang mga multi-agent workflow kumpara sa single-agent dahil sa mga sumusunod at mga tawag sa MCP tool.

| Pag-optimize | Paano | Epekto |
|-------------|-----|--------|
| Bawasan ang MCP calls | Bawasan ang `max_results` parameter sa tool | Mas kaunting HTTP round-trips |
| Pagaanin ang instructions | Mas maikli, mas pokus na mga prompt ng agent | Mas mabilis ang LLM inference |
| Gamitin ang `gpt-4.1-mini` | Mas mabilis kaysa `gpt-4.1` para sa development | Mga ~2x na bilis |
| Bawasan ang detalye ng gap card | Paliitin ang format ng gap card sa GapAnalyzer instructions | Mas kaunting output na kailangan i-generate |

### Karaniwang oras ng sagot (lokal)

| Configuration | Inaasahang oras |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap cards | 30-60 segundo |
| `gpt-4.1-mini`, 8+ gap cards | 60-120 segundo |
| `gpt-4.1`, 3-5 gap cards | 60-120 segundo |
---

## Paghingi ng tulong

Kung na-stuck ka pagkatapos subukan ang mga pag-aayos sa itaas:

1. **Suriin ang mga log ng server** - Karamihan sa mga error ay naglalabas ng Python stack trace sa terminal. Basahin ang buong traceback.
2. **Hanapin ang mensahe ng error** - Kopyahin ang teksto ng error at hanapin ito sa [Microsoft Q&A para sa Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Magbukas ng isyu** - Mag-file ng isyu sa [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) kasama ang:
   - Mensahe ng error o screenshot
   - Mga bersyon ng iyong package (`pip list | Select-String "agent-framework"`)
   - Bersyon ng iyong Python (`python --version`)
   - Kung ang isyu ba ay lokal o pagkatapos ng deployment

---

### Checkpoint

- [ ] Maaari mong tukuyin at ayusin ang mga pinaka-karaniwang multi-agent error gamit ang mabilisang talaan
- [ ] Alam mo kung paano suriin at ayusin ang mga isyu sa `.env` configuration
- [ ] Maaari mong beripikahin ang mga bersyon ng package na tumutugma sa kinakailangang matrix
- [ ] Nauunawaan mo ang mga entry sa MCP log at kayang mag-diagnose ng mga pagkabigo ng tool
- [ ] Alam mo kung paano suriin ang mga log ng container para sa mga pagkabigo ng deployment
- [ ] Maaari mong beripikahin ang mga RBAC role sa Azure Portal

---

**Nauna:** [07 - Verify in Playground](07-verify-in-playground.md) · **Bahay:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagaman nagsusumikap kami para sa katumpakan, pakatandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa kanyang sariling wika ang dapat ituring na pangunahing pinagkunan. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na nagmumula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->