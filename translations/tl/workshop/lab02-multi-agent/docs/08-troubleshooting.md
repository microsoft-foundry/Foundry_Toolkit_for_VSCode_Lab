# Module 8 - Pag-aayos ng Problema

Tinatalakay ng module na ito ang mga karaniwang error, mga ayos, at mga estratehiya sa pag-debug na partikular sa multi-agent workflow.

## Mga isyu sa output ng Ahente

### Sinabi ng GapAnalyzer na “Wala pa rin akong katugmang ulat”

**Sintomas:** Humihiling ang sagot ng GapAnalyzer na i-paste mo ang katugmang ulat na may “Missing Skills” at “Certification Gaps.” Nangyayari ito kahit na nagpadala ka ng resume at deskripsyon ng trabaho.

**Sanhi:** Hindi naipasa ang teksto ng JD pababa kay JD Agent. Sa `context_mode="last_agent"`, si `resume_executor` lang ang executor na nakakakita ng orihinal na mensahe ng user. Kung ang `RESUME_PARSER_INSTRUCTIONS` ay hindi kasama ang teksto ng JD sa output nito, walang JD na mape-parse si JD Agent, hindi makakalkula ng MatchingAgent ang fit score, at makakatanggap ng walang saysay na input ang GapAnalyzer.

**Diagnostiko:**

Sa mga log ng server, hanapin ang MatchingAgent span. Kung ito ay naglalaman:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
nawawala o sira ang pass-through.

**Ayusin:** Kumpirmahin na ang `RESUME_PARSER_INSTRUCTIONS` sa `main.py` ay naglalaman ng seksyon na `[JOB DESCRIPTION PASS-THROUGH]` at ang patakaran:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Kumpirmahin din na ang `JOB_DESCRIPTION_INSTRUCTIONS` ay mayroong relay rule na `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Kung alinman sa mga instruction block ay stub mula sa scaffold wizard, palitan ito ng kumpletong bersyon mula sa [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Naglalabas ang MatchingAgent ng “Cannot compute fit score - no JD provided”

Parehong ugat ang sanhi gaya ng nasa itaas. Nakakuha ang MatchingAgent ng output mula sa JD Agent ngunit nawawala o walang laman ang `[PARSED RESUME PASS-THROUGH]` na seksyon, kaya hindi nito maikumpara ang dalawang profile. Kumpirmahin:
1. Kasama sa `JOB_DESCRIPTION_INSTRUCTIONS` ang relay rule na: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. Sinusubaybayan ng `MATCHING_AGENT_INSTRUCTIONS` ang mga seksyon na `[JD REQUIREMENTS]` at `[PARSED RESUME PASS-THROUGH]`.

Palitan ang parehong instruction blocks ng kumpletong bersyon mula sa [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Lumalabas nang doble ang sagot

**Sintomas:** Ang output ng GapAnalyzer (o ang buong pipeline output) ay lumalabas nang dalawang beses sa sagot ng Agent Inspector.

**Sanhi:** Gumagamit ang `WorkflowBuilder` ng OR-semantics para sa mga naghuhugpong dulo - nagpapasimula ang downstream executor kapag **anumang** predecessor ay natapos. Kung ang `matching_executor` ay may dalawang papasok na hugpong (isa mula sa `resume_executor` at isa mula sa `jd_executor`), mabilis itong masisimulan dalawang beses: minsan kapag natapos ang ResumeParser at muli kapag natapos ang JD Agent. Nagsisimula rin ang GapAnalyzer nang dalawang beses.

**Ayusin:** Siguraduhing ang graph ng `WorkflowBuilder` ay isang mahigpit na sequential pipeline na walang fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # HINDI mula sa resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Kung may labis na linya na `.add_edge(resume_executor, matching_executor)`, alisin ito. Ibinibigay na ng `[PARSED RESUME PASS-THROUGH]` relay sa output ng JD Agent ang access ng MatchingAgent sa resume.

---

## Mga isyu sa kapaligiran at konfigurasyon

### Nawawala o maling mga halaga sa `.env`

Dapat ang `.env` file ay nasa direktoryo ng `PersonalCareerCopilot/` (kapares ng `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Inaasahang nilalaman ng `.env`:

**Path A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Path B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Parehong path ang gumagamit ng `FOUNDRY_PROJECT_ENDPOINT`. Nagkakaiba ang halaga: ang cloud ay gumagamit ng `https://` Foundry endpoint; ang local ay gumagamit ng `http://localhost:5273/v1`. Patakbuhin ang `foundry model list` upang kumpirmahin ang eksaktong alias ng modelo para sa Path B.

> **Paano hanapin ang iyong `FOUNDRY_PROJECT_ENDPOINT`:** 
- Buksan ang **Foundry Toolkit** sidebar sa VS Code → i-right-click ang iyong proyekto → **Copy Project Endpoint**. 
- O pumunta sa [Azure Portal](https://portal.azure.com) → iyong Foundry project → **Overview** → **Project endpoint**.

> **Paano hanapin ang iyong `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Sa Foundry Toolkit sidebar, palawakin ang iyong proyekto → **Models** → hanapin ang pangalan ng iyong na-deploy na modelo (hal. `gpt-4.1-mini`).

### Prioidad ng mga env var

Gumagamit ang `main.py` ng `load_dotenv(override=True)`, ibig sabihin:

| Prayoridad | Pinagmulan | Panalo kapag pareho nakaset? |
|----------|--------|------------------------|
| 1 (pinakamataas) | `.env` file | Oo |
| 2 | Shell / environment variable ng container | Ginagamit kapag wala ang parehong key sa `.env` |

Sa lokal na pag-develop, ginagawa nitong totoo ang `.env` (ang pag-edit sa `.env` ay agad na nakakaapekto sa mga takbo). Sa naka-host na deployment, naglalagay ang Foundry ng mga environment variable sa antas ng container; dahil hindi bahagi ng deployed image ang `.env` para sa setup ng lab na ito, ginagamit ang mga pinagana sa container.

---

## Compatibilidad ng bersyon

### Matrix ng bersyon ng package

Nangangailangan ang multi-agent workflow ng mga espesipikong bersyon ng package. Nagdudulot ng error sa runtime ang hindi pagtutugma ng bersyon.

| Package | Kinakailangang Bersyon | Utos para Suriin |
|---------|-----------------|---------------|
| `agent-framework-foundry` | pinakabago | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | pinakabago | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | pinakabago | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Mga karaniwang error sa bersyon

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Ayusin: i-reinstall ang agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Ayusin: i-upgrade ang mcp package
pip install mcp --upgrade
```

### Suriin ang lahat ng bersyon nang sabay-sabay

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Inaasahang output:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Mga isyu sa deployment

### Nabibigo ang container na magsimula pagkatapos ng deployment

1. **Suriin ang logs ng container:**
   - Buksan ang **Foundry Toolkit** sidebar → palawakin ang **Hosted Agents (Preview)** → i-click ang iyong ahente → palawakin ang bersyon → **Container Details** → **Logs**.
   - Hanapin ang mga Python stack trace o mga error sa nawawalang module.

2. **Mga karaniwang dahilan ng pagkabigo sa pagsisimula ng container:**

   | Error sa logs | Sanhi | Ayusin |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | Kulang sa `requirements.txt` na package | Idagdag ang package, i-deploy muli |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Hindi nakaset ang `agent.yaml` o `.env` env vars | I-update ang `agent.yaml` → seksyon ng `environment_variables` (hosted) o `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Hindi naka-configure ang Managed Identity | Awtomatikong isinet ng Foundry - siguraduhing nagde-deploy gamit ang extension |
   | `OSError: port 8088 already in use` | Mali ang port na naka-expose sa Dockerfile o may conflict sa port | Suriin ang `EXPOSE 8088` sa Dockerfile at `CMD ["python", "main.py"]` |
   | Lumalabas ang container na may code 1 | Hindi nahahandle na exception sa `main()` | Subukan lokal muna ([Module 5](05-test-locally.md)) para mahuli ang mga error bago mag-deploy |

3. **I-deploy muli pagkatapos ayusin:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → piliin ang parehong ahente → mag-deploy ng bagong bersyon.

### Mabagal ang deployment

Mas matagal magsimula ang mga multi-agent container dahil lumilikha sila ng 4 na instance ng ahente sa pagsisimula. Karaniwang oras ng pagsisimula:

| Yugto | Inaasahang tagal |
|-------|------------------|
| Pagbuo ng container image | 1-3 minuto |
| Pagtulak ng image sa ACR | 30-60 segundo |
| Pagsisimula ng container (isang ahente) | 15-30 segundo |
| Pagsisimula ng container (multi-agent) | 30-120 segundo |
| Available na ang ahente sa Playground | 1-2 minuto pagkatapos ng "Started" |

> Kung ang “Pending” na status ay tumatagal nang lagpas sa 5 minuto, suriin ang logs ng container para sa mga error.

---

## Mga isyu sa RBAC at permiso

### `403 Forbidden` o `AuthorizationFailed`

Kailangan mo ng papel na **[Foundry User](https://aka.ms/foundry-ext-project-role)** sa iyong Foundry project (dating tinawag na **Azure AI User** - hindi nagbago ang role ID):

1. Pumunta sa [Azure Portal](https://portal.azure.com) → ang iyong Foundry **project** resource.
2. I-click ang **Access control (IAM)** → **Role assignments**.
3. Hanapin ang iyong pangalan → kumpirmahin ang **Foundry User** (o ang lumang label na **Azure AI User**) ay nakalista.
4. Kung wala: **Add** → **Add role assignment** → hanapin ang **Foundry User** → i-assign sa iyong account.

Tingnan ang dokumentasyon ng [RBAC para sa Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para sa mga detalye.

### Hindi maa-access ang deployment ng modelo

Kung nagbabalik ang ahente ng mga error tungkol sa modelo:

1. Kumpirmahin na na-deploy ang modelo: Foundry sidebar → palawakin ang proyekto → **Models** → hanapin ang `gpt-4.1-mini` (o iyong modelo) na may status na **Succeeded**.
2. Kumpirmahing tugma ang deployment name: ihambing ang `AZURE_AI_MODEL_DEPLOYMENT_NAME` sa `.env` (o `agent.yaml`) sa aktuwal na pangalan ng deployment sa sidebar.
3. Kung nag-expire ang deployment (free tier): mag-deploy muli mula sa [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Mga isyu sa Foundry Local (Path B)

### Hindi tumatakbo ang Foundry Local service

```powershell
# Suriin ang katayuan
foundry local status

# Simulan ang serbisyo kung ito ay huminto
foundry local start
```

| Sintomas | Sanhi | Ayusin |
|---------|-------|-----|
| Nagbabalik ang health check ng `503` | Hindi nagsimula ang serbisyo | `foundry local start` o i-click ang **Start** sa Foundry Toolkit sidebar |
| Nag-timeout ang health check | Nilo-load pa ang modelo | Maghintay ng 30–60 s pagkatapos magsimula; mas malaki ang modelo, mas matagal |
| `StatusCode: 404` sa `/v1/health` | Mali ang port | Default ay `5273`. Suriin ang `foundry local status` para sa aktuwal na port |
| Kulang sa resources | Nangangailangan ng ~4 GB RAM na libre ang Foundry Local | Isara ang ibang aplikasyon |
| Nabigo ang pag-download ng modelo | Mababa ang disk space | Ang mga modelo ay 2–8 GB. Magpataas ng space, pagkatapos ay `foundry model pull <name>` |

### Hindi tumutugma ang pangalan ng modelo

```powershell
# Ilahad ang mga na-download na modelo at ang kanilang eksaktong mga alyas
foundry model list
```

Itakda ang `AZURE_AI_MODEL_DEPLOYMENT_NAME` sa `.env` sa eksaktong alias na ipinapakita (hal. `phi-4-mini`, hindi `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` sa lokal na takbo (Path B)

Ginagamit ng lab na `main.py` ang `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Kailangan ng Foundry Local na ituro ang variable na ito sa lokal na serbisyo - **hindi** sa `AZURE_AI_PROJECT_ENDPOINT`. Siguraduhin na ang iyong `.env` ay naglalaman:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Patuloy pa ring gumagawa ng outbound call ang MCP tool (Path B)

Inaasahan ito. Kinukuha ng tool na `search_microsoft_learn_for_plan` ang mga learning resources mula sa `https://learn.microsoft.com/api/mcp`. **Ang query lang sa pangalan ng skill** ang dumadaan sa network - ang resume at teksto ng JD ay pinoproseso nang buo sa iyong device at hindi kailanman ipinapadala. Kung kailangan ng ganap na offline na operasyon, magdagdag ng `try/except` fallback sa tool na magbabalik ng static na `learn.microsoft.com` URL kapag hindi maabot ang endpoint.

---

## Paghahanap ng tulong

Kung natigil ka pagkatapos subukan ang mga ayos sa itaas:

1. **Suriin ang server logs** - Karamihan sa mga error ay gumagawa ng Python stack trace sa terminal. Basahin ang buong traceback.
2. **Hanapin ang mensahe ng error** - Kopyahin ang error text at hanapin sa [Microsoft Q&A para sa Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Magbukas ng isyu** - Mag-file ng isyu sa [workshop repository](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) na may:
   - Mensahe ng error o screenshot
   - Mga bersyon ng iyong package (`pip list | Select-String "agent-framework"`)
   - Iyong bersyon ng Python (`python --version`)
   - Kung lokal ba o pagkatapos ng deployment ang isyu

---

### Checkpoint

- [ ] Alam mo kung paano suriin at ayusin ang mga isyu sa konfigurasyon ng `.env`
- [ ] Kaya mong tiyakin na tumutugma ang mga bersyon ng package sa kinakailangang matrix
- [ ] Alam mo kung paano suriin ang mga log ng container para sa mga pagkabigo sa deployment
- [ ] Kaya mong tiyakin ang mga RBAC role sa Azure Portal

---

**Nakaraan:** [07 - Verify in Playground](07-verify-in-playground.md) · **Susunod:** [09 - Summary →](09-summary.md) · **Tahanan:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->