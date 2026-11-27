# Module 8 - Pagsasaayos ng Problema

Tinatalakay ng module na ito ang mga karaniwang error, pag-ayos, at mga estratehiya sa pag-debug na partikular sa multi-agent workflow.

## Mga isyu sa output ng Agent

### Sinasabi ng GapAnalyzer na “Wala pa rin akong matching report”

**Sintomas:** Humihiling ang tugon ng GapAnalyzer na i-paste mo ang matching report na may “Missing Skills” at “Certification Gaps.” Nangyayari ito kahit na nagpadala ka ng resume at job description.

**Sanhi:** Hindi ipinasa ang teksto ng JD pababa kay JD Agent. Sa `context_mode="last_agent"`, si `resume_executor` lang ang executor na nakakakita ng orihinal na mensahe ng user. Kung hindi isinasama ni `RESUME_PARSER_INSTRUCTIONS` ang teksto ng JD sa output nito, walang JD na maipapasok kay JD Agent para i-parse, hindi makakalkula ng MatchingAgent ang fit score, at makakatanggap ng walang kabuluhang input ang GapAnalyzer.

**Diagnostiko:**

Sa mga server log, hanapin ang span ng MatchingAgent. Kung ito ay naglalaman ng:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
nawawala o sira ang pass-through.

**Ayusin:** Kumpirmahin na ang `RESUME_PARSER_INSTRUCTIONS` sa `main.py` ay may seksyong `[JOB DESCRIPTION PASS-THROUGH]` at ang patakaran:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Kumpirmahin din na ang `JOB_DESCRIPTION_INSTRUCTIONS` ay may patakarang relay na `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Kung ang alinman sa mga instruction block ay stub mula sa scaffold wizard, palitan ito ng kumpletong bersyon mula sa [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Naglalabas ang MatchingAgent ng “Cannot compute fit score - no JD provided”

Pareho pa rin ang ugat na sanhi tulad ng nasa itaas. Natanggap ng MatchingAgent ang output ni JD Agent ngunit ang seksyon ng `[PARSED RESUME PASS-THROUGH]` ay nawawala o walang laman, kaya hindi nito mai-kumpara ang dalawang profile. Kumpirmahin:
1. Kasama sa `JOB_DESCRIPTION_INSTRUCTIONS` ang patakarang relay: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. Sinasabi ng `MATCHING_AGENT_INSTRUCTIONS` sa agent na hanapin ang mga seksyon ng `[JD REQUIREMENTS]` at `[PARSED RESUME PASS-THROUGH]`.

Palitan ang parehong mga instruction block ng mga kumpletong bersyon mula sa [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Lumilitaw ang tugon nang dalawang beses

**Sintomas:** Ang output ng GapAnalyzer (o ang buong pipeline output) ay lumilitaw nang dalawang beses sa tugon ng Agent Inspector.

**Sanhi:** Ginagamit ng `WorkflowBuilder` ang OR-semantics para sa mga papasok na edges - isang downstream executor ang tatakbo kapag natapos na ang **anumang** predecessor. Kung ang `matching_executor` ay may dalawang papasok na edges (isa mula sa `resume_executor` at isa mula sa `jd_executor`), tatakbo ito nang dalawang beses: isang beses pag natapos ang ResumeParser at muli pag natapos ang JD Agent. Tatakbo rin nang dalawang beses ang GapAnalyzer.

**Ayusin:** Siguraduhing ang graph ng `WorkflowBuilder` ay isang mahigpit na sunud-sunod na pipeline na walang fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Kung may labis na linyang `.add_edge(resume_executor, matching_executor)`, alisin ito. Nagbibigay na ang relay ng `[PARSED RESUME PASS-THROUGH]` sa output ni JD Agent ng access ng MatchingAgent sa resume.

---

## Mga isyu sa kapaligiran at pagsasaayos

### Nawawala o maling mga halaga ng `.env`

Ang `.env` na file ay kailangang nasa direktoryo ng `PersonalCareerCopilot/` (parehong antas ng `main.py`):

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

> Parehong gumagamit ng `FOUNDRY_PROJECT_ENDPOINT` ang dalawang path. Nagkakaiba ang halaga: ang cloud ay gumagamit ng `https://` Foundry endpoint; ang local ay gumagamit ng `http://localhost:5273/v1`. Patakbuhin ang `foundry model list` para kumpirmahin ang eksaktong alias ng modelo para sa Path B.

> **Paano hanapin ang iyong `FOUNDRY_PROJECT_ENDPOINT`:** 
- Buksan ang **Foundry Toolkit** sidebar sa VS Code → right-click ang iyong proyekto → **Copy Project Endpoint**. 
- O pumunta sa [Azure Portal](https://portal.azure.com) → iyong Foundry project → **Overview** → **Project endpoint**.

> **Paano hanapin ang iyong `AZURE_AI_MODEL_DEPLOYMENT_NAME`:** Sa Foundry Toolkit sidebar, palawakin ang iyong proyekto → **Models** → hanapin ang pangalan ng deployed na modelo (hal. `gpt-4.1-mini`).

### Pagkakasunod-sunod ng precedence ng env var

Ginagamit ng `main.py` ang `load_dotenv(override=True)`, na nangangahulugang:

| Prayoridad | Pinagmulan | Nanalo kapag parehong na-set? |
|----------|--------|------------------------|
| 1 (pinakamataas) | file ng `.env` | Oo |
| 2 | Shell / container environment variable | Ginagamit kapag walang parehong key sa `.env` |

Sa local development, ginagawa nitong source of truth ang `.env` (ang pag-edit ng `.env` ay agad na nakaapekto sa mga pagtakbo). Sa hosted deployment, nag-iinject ang Foundry ng mga environment variable sa antas ng container; dahil hindi bahagi ang `.env` ng deployed image para sa setup ng lab na ito, ginagamit ang mga injected na halaga ng container.

---

## Pagkakatugma ng bersyon

### Matrix ng bersyon ng package

Nangangailangan ang multi-agent workflow ng mga tiyak na bersyon ng package. Ang hindi pagkakatugma ng mga bersyon ay nagdudulot ng mga error sa runtime.

| Package | Kinakailangang Bersyon | Command para Suriin |
|---------|-----------------|---------------|
| `agent-framework-foundry` | pinakabago | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | pinakabago | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | pinakabago | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Mga karaniwang error sa bersyon

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Suriin lahat ng bersyon ng sabay-sabay

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

### Nabibigo ang container na magsimula pagkatapos i-deploy

1. **Suriin ang mga log ng container:**
   - Buksan ang **Foundry Toolkit** sidebar → sa ilalim ng iyong proyekto, i-click ang **Agents** → tab na **Hosted Agent** → i-click ang iyong agent. Suriin ang **Status** sa tab na **Details**, pagkatapos buksan ang tab na **Playground** at gamitin ang tab na **Logs** sa panel ng **Session Details** upang makita ang output ng container.
   - Hanapin ang mga Python stack trace o mga error ng nawawalang module.

2. **Mga karaniwang pagkabigo sa pagsisimula ng container:**

   | Error sa mga log | Sanhi | Ayusin |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` nawawalang package | Idagdag ang package, muling i-deploy |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` o `.env` env vars hindi nakaset | I-update ang `agent.yaml` → `environment_variables` seksyon (hosted) o `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity hindi naka-configure | Awtomatikong sine-set ng Foundry ito - siguraduhing nagde-deploy ka gamit ang extension |
   | `OSError: port 8088 already in use` | Dockerfile nag-eexpose ng maling port o may port conflict | Verify `EXPOSE 8088` sa Dockerfile at `CMD ["python", "main.py"]` |
   | Container lumalabas na may code 1 | Unhandled exception sa `main()` | Subukan muna lokal ([Module 5](05-test-locally.md)) para makahuli ng mga error bago i-deploy |

3. **Muling i-deploy pagkatapos ayusin:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → piliin ang parehong agent → i-deploy ang bagong bersyon.

### Matagal ang deployment

Mas tumatagal ang pagsisimula ng multi-agent containers dahil gumagawa ito ng 4 agent instances sa pagsisimula. Normal na oras ng pagsisimula:

| Yugto | Inaasahang tagal |
|-------|------------------|
| Pagtayo ng container image | 1-3 minuto |
| Pag-push ng image sa ACR | 30-60 segundo |
| Pagsisimula ng container (single agent) | 15-30 segundo |
| Pagsisimula ng container (multi-agent) | 30-120 segundo |
| Agent available sa Playground | 1-2 minuto pagkatapos ng "Started" |

> Kung ang status na "Pending" ay tumatagal nang higit sa 5 minuto, tingnan ang mga log ng container para sa mga error.

---

## Mga isyu sa RBAC at permiso

### `403 Forbidden` o `AuthorizationFailed`

Kailangan mo ang **[Foundry User](https://aka.ms/foundry-ext-project-role)** role sa iyong Foundry project (dating tinatawag na **Azure AI User** - hindi nagbago ang role ID):

1. Pumunta sa [Azure Portal](https://portal.azure.com) → resource ng iyong Foundry **project**.
2. I-click ang **Access control (IAM)** → **Role assignments**.
3. Hanapin ang iyong pangalan → kumpirmahin na nakalista ang **Foundry User** (o ang legacy label na **Azure AI User**).
4. Kung wala: **Add** → **Add role assignment** → hanapin ang **Foundry User** → i-assign sa iyong account.

Tingnan ang dokumentasyon ng [RBAC for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) para sa detalye.

### Hindi ma-access ang deployment ng modelo

Kung nagbabalik ang agent ng mga error na may kinalaman sa modelo:

1. I-verify na na-deploy ang modelo: sa Foundry sidebar → palawakin ang project → **Models** → tingnan kung nandiyan ang `gpt-4.1-mini` (o ang iyong modelo) na may status na **Succeeded**.
2. I-verify na tugma ang pangalan ng deployment: ikumpara ang `AZURE_AI_MODEL_DEPLOYMENT_NAME` sa `.env` (o `agent.yaml`) sa totoong pangalan ng deployment sa sidebar.
3. Kung nag-expire ang deployment (free tier): mag-redeploy mula sa [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Mga isyu sa Foundry Local (Path B)

### Hindi tumatakbo ang Foundry Local service

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Sintomas | Sanhi | Ayusin |
|---------|-------|-----|
| Nagbabalik ang health check ng `503` | Hindi nagsimula ang serbisyo | `foundry local start` o i-click ang **Start** sa Foundry Toolkit sidebar |
| Nagtatagal ng timeout ang health check | Naka-load pa ang modelo | Maghintay ng 30–60 s pagkatapos simulan; mas malalaking modelo ay mas matagal |
| `StatusCode: 404` sa `/v1/health` | Maling port | Default ay `5273`. Tingnan ang `foundry local status` para sa totoong port |
| Kakulangan sa resources | Nangangailangan ang Foundry Local ng halos 4 GB RAM na libre | Isara ang ibang mga aplikasyon |
| Nabigo ang pag-download ng modelo | Mababa ang disk space | Ang mga modelo ay 2–8 GB. Magpalaya ng espasyo, pagkatapos `foundry model pull <name>` |

### Hindi tugmang pangalan ng modelo

```powershell
# List downloaded models and their exact aliases
foundry model list
```

I-set ang `AZURE_AI_MODEL_DEPLOYMENT_NAME` sa `.env` sa eksaktong alias na ipinakita (hal., `phi-4-mini`, hindi `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` sa lokal na pagpapatakbo (Path B)

Ang `main.py` ng lab ay gumagamit ng `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Nangangailangan ang Foundry Local na ituro ang variable na ito sa lokal na serbisyo - **hindi** sa `AZURE_AI_PROJECT_ENDPOINT`. Siguraduhing ang iyong `.env` ay naglalaman ng:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Ang MCP tool ay gumagawa pa rin ng outbound call (Path B)

Ito ay inaasahan. Kinukuha ng `search_microsoft_learn_for_plan` tool ang mga learning resources mula sa `https://learn.microsoft.com/api/mcp`. **Ang query lamang ng skill-name** ang dumadaan sa network - ang resume at JD text ay pinoproseso nang buo sa iyong device at hindi ipinapadala kailanman. Kung kailangan ang ganap na offline na operasyon, magdagdag ng `try/except` fallback sa tool na nagbabalik ng static na `learn.microsoft.com` URL kapag hindi maabot ang endpoint.

---

## Pagkuha ng tulong

Kung na-stuck ka pagkatapos subukan ang mga ayos sa itaas:

1. **Suriin ang mga server logs** - Karamihan sa mga error ay naglalabas ng Python stack trace sa terminal. Basahin ang buong traceback.
2. **Hanapin ang mensahe ng error** - Kopyahin ang teksto ng error at hanapin ito sa [Microsoft Q&A para sa Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Magbukas ng isyu** - Mag-file ng isyu sa [workshop repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) na may kasamang:
   - Mensahe ng error o screenshot
   - Mga bersyon ng package (`pip list | Select-String "agent-framework"`)
   - Bersyon ng iyong Python (`python --version`)
   - Kung ang isyu ay lokal o pagkatapos ng deployment

---

### Checkpoint

- [ ] Alam mo kung paano suriin at ayusin ang mga isyu sa configuration ng `.env`
- [ ] Kaya mong beripikahin na tugma ang mga bersyon ng package sa kinakailangang matrix
- [ ] Alam mo kung paano tingnan ang mga log ng container para sa mga pagkabigo sa deployment
- [ ] Kaya mong beripikahin ang mga RBAC roles sa Azure Portal

---

**Nagdaan:** [07 - Verify in Playground](07-verify-in-playground.md) · **Susunod:** [09 - Summary →](09-summary.md) · **Bahay:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Pagtatanggi**:
Ang dokumentong ito ay isinalin gamit ang serbisyo ng AI translation na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagama't nagsusumikap kami para sa katumpakan, pakatandaan na ang awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o hindi pagkakatugma. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang maling pagkakaintindi o maling interpretasyon na nagmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->