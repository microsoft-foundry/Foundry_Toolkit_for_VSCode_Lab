# Moodul 8 - Tõrkeotsing (mitmeagendi töövoog)

See moodul käsitleb levinumaid vigu, parandusi ja silumisstrateegiaid, mis on spetsiifilised mitmeagendi töövoole. Üldiste Foundry juurutusprobleemide korral vaata ka [Lab 01 tõrkeotsingu juhendit](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Kiirviide: Viga → Parandus

| Viga / Sündroom | Võimalik põhjus | Parandus |
|----------------|-----------------|----------|
| `RuntimeError: Missing required environment variable(s)` | `.env` fail puudub või väärtused pole seatud | Loo `.env`, mis sisaldab `PROJECT_ENDPOINT=<your-endpoint>` ja `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Virtuaalkeskkond pole aktiveeritud või sõltuvused pole installitud | Käivita `.\.venv\Scripts\Activate.ps1` ja seejärel `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP pakett pole installitud (puudub requirements failis) | Käivita `pip install mcp` või kontrolli, et `requirements.txt` sisaldab seda transitiivselt |
| Agent käivitub, kuid tagastab tühja vastuse | `output_executors` ei vasta või puuduvad servad | Kontrolli, et `output_executors=[gap_analyzer]` ja kõik servad on olemas `create_workflow()` funktsioonis |
| Ainult 1 gap-kaart (ülejäänud puuduvad) | GapAnalyzer’i juhised on puudulikud | Lisa `CRITICAL:` lõik `GAP_ANALYZER_INSTRUCTIONS`-i - vaata [Moodul 3](03-configure-agents.md) |
| Sobivusskoor on 0 või puudub | MatchingAgent ei saanud ülevalt tulevaid andmeid | Veendu, et olemas on nii `add_edge(resume_parser, matching_agent)` kui `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server keeldus tööriista kutsest | Kontrolli internetiühendust. Proovi avada `https://learn.microsoft.com/api/mcp` brauseris. Proovi uuesti |
| Väljundis pole Microsoft Learn URL-e | MCP tööriist pole registreeritud või endpoint on vale | Veendu, et `tools=[search_microsoft_learn_for_plan]` on GapAnalyzer’is ja `MICROSOFT_LEARN_MCP_ENDPOINT` on õige |
| `Address already in use: port 8088` | Teine protsess kasutab porti 8088 | Käivita `netstat -ano \| findstr :8088` (Windows) või `lsof -i :8088` (macOS/Linux) ja peata vastuoluline protsess |
| `Address already in use: port 5679` | Debugpy pordi konflikt | Peata teised debug seansid. Käivita `netstat -ano \| findstr :5679`, leia ja tapprotsess |
| Agent Inspector ei avane | Server pole täielikult käivitatud või port on hõivatud | Oota "Server running" logi. Kontrolli, et port 5679 oleks vaba |
| `azure.identity.CredentialUnavailableError` | Azure CLI-s pole sisse logitud | Käivita `az login` ja taaskäivita server |
| `azure.core.exceptions.ResourceNotFoundError` | Mudeli juurutus puudub | Kontrolli, et `MODEL_DEPLOYMENT_NAME` vastab sinu Foundry projekti juurutatud mudelile |
| Konteineri olek "Failed" pärast juurutust | Konteiner jooksis käivitamisel kokku | Kontrolli konteineri logisid Foundry küljeribal. Levinud põhjused: puudu env muutuja või importvead |
| Juurutus kuvab "Pending" üle 5 minuti | Konteiner võtab liiga kaua aega käivitamiseks või ressursipiirang | Oota kuni 5 minutit mitmeagendi puhul (loob 4 agendi instantsi). Kui jääb ootele, kontrolli logisid |
| `ValueError` `WorkflowBuilder`-ilt | Vale graafi konfiguratsioon | Veendu, et `start_executor` on seatud, `output_executors` on list ja puuduvad tsüklilised servad |

---

## Keskkonna ja konfiguratsiooni probleemid

### Puuduvad või valed `.env` väärtused

`.env` fail peab asuma kataloogis `PersonalCareerCopilot/` (sama taseme all kui `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Oodatav `.env` sisu:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Kuidas leida PROJECT_ENDPOINT:**
- Ava **Microsoft Foundry** küljeriba VS Code’is → paremklõps projektil → **Copy Project Endpoint**.
- Või mine [Azure Portal](https://portal.azure.com) → oma Foundry projekt → **Overview** → **Project endpoint**.

> **Kuidas leida MODEL_DEPLOYMENT_NAME:** Foundry küljeribal laienda oma projekt → **Models** → leia juurutatud mudeli nimi (nt `gpt-4.1-mini`).

### Keskkonnamuutujate prioriteet

`main.py` kasutab `load_dotenv(override=False)`, mis tähendab:

| Prioriteet | Allikas | Kas võidab, kui mõlemad on seatud? |
|------------|---------|-------------------------------------|
| 1 (kõrgeim) | Shell keskkonnamuutuja | Jah |
| 2 | `.env` fail | Ainult kui shell muutuja pole seatud |

See tähendab, et Foundry runtime keskkonnamuutujad (mida määrab `agent.yaml`) on eelisjärjekorras võrreldes `.env` väärtustega hostitud juurutuse ajal.

---

## Versiooni ühilduvus

### Pakettide versioonimaatriks

Mitmeagendi töövoog nõuab konkreetseid pakettide versioone. Mitteühilduvad versioonid põhjustavad jooksu ajal vigu.

| Pakett | Nõutav versioon | Kontrollkäsklus |
|--------|-----------------|-----------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | uusim eelversioon | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Levinumad versioonivead

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Parandus: uuenda versioonile rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` puudub või Inspector ei ühildu:**

```powershell
# Parandus: installi --pre lipuga
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Parandus: uuenda mcp paketti
pip install mcp --upgrade
```

### Kontrolli kõiki versioone korraga

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Oodatav väljund:

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

## MCP tööriista probleemid

### MCP tööriist ei tagasta tulemusi

**Sümptom:** Gap-kaardid ütlevad "No results returned from Microsoft Learn MCP" või "No direct Microsoft Learn results found".

**Võimalikud põhjused:**

1. **Võrgu probleem** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) ei ole kättesaadav.
   ```powershell
   # Testi ühenduvust
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Kui see tagastab koodi `200`, on endpoint kättesaadav.

2. **Päring on liiga spetsiifiline** - Oskuse nimi on liiga nišipõhine Microsoft Learn otsingus.
   - See on oodatav väga spetsiifiliste oskuste puhul. Tööriist tagastab vastuses varuplatsi URL-i.

3. **MCP seansi aegumine** - Streamable HTTP ühendus aegus.
   - Proovi päringut uuesti. MCP seansid on ajutised ja võivad vajada ühenduse taastamist.

### MCP logide selgitus

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Logi | Tähendus | Tegevus |
|-------|----------|---------|
| `GET → 405` | MCP klient kontrollib alglaadimisel | Tavaline - ignoreeri |
| `POST → 200` | Tööriista kutse õnnestus | Oodatud |
| `DELETE → 405` | MCP klient kontrollib lõpetamisel | Tavaline - ignoreeri |
| `POST → 400` | Vale päring (vigane päring) | Kontrolli `query` parameetrit `search_microsoft_learn_for_plan()` funktsioonis |
| `POST → 429` | Liiga palju päringuid | Oota ja proovi uuesti. Vähenda `max_results` parameetrit |
| `POST → 500` | MCP serveri viga | Ajutine - proovi uuesti. Kui püsib, võib Microsoft Learn MCP API olla maas |
| Ühenduse aegumine | Võrgu probleem või MCP server pole saadaval | Kontrolli internetiühendust. Proovi `curl https://learn.microsoft.com/api/mcp` |

---

## Juurutusküsimused

### Konteiner ebaõnnestub käivitamisel pärast juurutust

1. **Kontrolli konteineri logisid:**
   - Ava **Microsoft Foundry** küljeriba → laienda **Hosted Agents (Preview)** → kliki oma agendil → laienda versiooni → **Container Details** → **Logs**.
   - Otsi Python veateateid või moodulipuuduseid.

2. **Levinumad konteineri käivituse ebaõnnestumised:**

   | Logivea kirjeldus | Põhjus | Parandus |
   |-------------------|---------|----------|
   | `ModuleNotFoundError` | `requirements.txt` pakett puudub | Lisa pakett ja juuruta uuesti |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` keskkonnamuutujad pole seatud | Paranda `agent.yaml` → `environment_variables` sektsioon |
   | `azure.identity.CredentialUnavailableError` | Managed Identity pole konfigureeritud | Foundry teeb selle automaatselt - veendu, et kasutad laiendust juurutamiseks |
   | `OSError: port 8088 already in use` | Vale pordi eksponeerimine Dockerfile’is või pordi konflikt | Kontrolli, et Dockerfile'is on `EXPOSE 8088` ja käsku `CMD ["python", "main.py"]` |
   | Konteiner väljub koodi 1-ga | Käitlemata erand `main()` sees | Testi lokaalset ([Moodul 5](05-test-locally.md)) enne juurutamist |

3. **Juuruta pärast parandust uuesti:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → vali sama agent → juuruta uus versioon.

### Juurutus võtab kaua aega

Mitmeagendi konteinerid võtavad käivitamiseks rohkem aega, sest nad loovad 4 agendi instantsi. Tavalised käivitamise ajad:

| Etapp | Oodatav kestus |
|--------|----------------|
| Konteineripildi ehitus | 1-3 minutit |
| Pildi tõstmine ACR-i | 30-60 sekundit |
| Konteineri käivitamine (üks agent) | 15-30 sekundit |
| Konteineri käivitamine (mitme agent) | 30-120 sekundit |
| Agent saadaval mänguplatsil | 1-2 minutit pärast "Started" |

> Kui "Pending" kestab üle 5 minuti, kontrolli konteineri logisid vigade osas.

---

## RBAC ja õiguste probleemid

### `403 Forbidden` või `AuthorizationFailed`

Sulle on tarvis rolli **[Azure AI User](https://aka.ms/foundry-ext-project-role)** sinu Foundry projektis:

1. Mine [Azure Portal](https://portal.azure.com) → oma Foundry **projekti** ressurss.
2. Kliki **Access control (IAM)** → **Role assignments**.
3. Otsi oma nime → veendu, et roll **Azure AI User** on olemas.
4. Kui puudub: **Add** → **Add role assignment** → otsi **Azure AI User** → määrake oma kontole.

Vaata täpsemalt [RBAC Microsoft Foundry jaoks](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokumentatsiooni.

### Mudeli juurutus pole ligipääsetav

Kui agent näitab mudelipõhiseid vigu:

1. Kontrolli, et mudel on juurutatud: Foundry küljeriba → laienda projekt → **Models** → otsi mudelit `gpt-4.1-mini` (või oma mudelit), mille olek on **Succeeded**.
2. Kontrolli, et juurutuse nimi ühtib: võrdle `MODEL_DEPLOYMENT_NAME` `.env`-is (või `agent.yaml`-is) tegeliku nimega küljeribal.
3. Kui juurutus aegus (tasuta tier): juuruta uuesti [Mudeli kataloogist](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspectori probleemid

### Inspector avaneb, kuid kuvab "Disconnected"

1. Veendu, et server töötab: otsi terminalist "Server running on http://localhost:8088".
2. Kontrolli porti `5679`: Inspector teeb ühenduse debugpy kaudu porti 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Taaskäivita server ja ava Inspector uuesti.

### Inspector kuvab osalist vastust

Mitmeagendi vastused on pikad ja voogedastatakse järk-järgult. Oota täisvastuse lõppu (võib võtta 30-60 sekundit olenevalt gap-kaartidest ja MCP tööriista kutsetest).

Kui vastus on pidevalt katkestatud:
- Kontrolli GapAnalyzer’i juhiseid, et seal oleks `CRITICAL:` plokk, mis takistab gap-kaartide kokkusulandumist.
- Kontrolli mudeli tokeni limiiti - `gpt-4.1-mini` toetab kuni 32K output tokenit, mis peaks piisama.

---

## Jõudluse näpunäited

### Aeglased vastused

Mitmeagendi töövood on sisuliselt aeglasemad kui ühe agendi omad, sest on järjepidevad sõltuvused ja MCP tööriistakutsed.

| Optimeerimine | Kuidas | Mõju |
|---------------|--------|-------|
| MCP kutsete vähendamine | Alanda tööriista `max_results` parameetrit | Vähem HTTP päringuid |
| Juhiste lihtsustamine | Lühikesed, täpsemad agentide promptid | Kiirem LLM arvestus |
| Kasuta `gpt-4.1-mini` | Kiirem kui `gpt-4.1` arenduseks | Umbes 2x kiirem |
| Vähenda gap-kaardi detaili | Lihtsusta gap-kaartide vormingut GapAnalyzer juhistes | Vähem väljundit genereerida |

### Tavapärased vastusaegade näitajad (lokaalselt)

| Konfiguratsioon | Oodatav aeg |
|-----------------|-------------|
| `gpt-4.1-mini`, 3-5 gap-kaarti | 30-60 sekundit |
| `gpt-4.1-mini`, 8+ gap-kaarti | 60-120 sekundit |
| `gpt-4.1`, 3-5 gap-kaarti | 60-120 sekundit |
---

## Abi saamine

Kui olete pärast ülaltoodud paranduste proovimist ummikus:

1. **Kontrollige serveri logisid** – Enamik veateateid kuvab terminalis Python'i virna jälje. Lugeda kogu virna jälg.
2. **Otsige veateadet** – Kopeerige vea tekst ja otsige seda aadressil [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Avage probleem** – Esitage probleem [workshopi repos](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) koos:
   - Veateate või ekraanipildiga
   - Teie pakettide versioonidega (`pip list | Select-String "agent-framework"`)
   - Teie Python'i versiooniga (`python --version`)
   - Kas probleem on kohalik või pärast kasutuselevõttu

---

### Kontrollpunkt

- [ ] Te suudate kiire viite tabeli abil tuvastada ja parandada kõige tavalisemaid mitme agendi vigu
- [ ] Te teate, kuidas kontrollida ja parandada `.env` konfiguratsiooni probleeme
- [ ] Te suudate kontrollida, kas pakettide versioonid vastavad nõutud tabelile
- [ ] Te mõistate MCP logikirjeid ja suudate diagnoosida tööriistade tõrkeid
- [ ] Te teate, kuidas kontrollida konteineri logisid juurutamise tõrgete jaoks
- [ ] Te suudate kontrollida RBAC rolle Azure Portaalis

---

**Eelmine:** [07 - Verify in Playground](07-verify-in-playground.md) · **Kodu:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastutusest loobumine**:  
See dokument on tõlgitud kasutades tehisintellekti tõlke teenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi püüdleme täpsuse poole, palun arvestage, et automaatsed tõlked võivad sisaldada vigu või ebatäpsusi. Originaaldokument selle algses keeles tuleks pidada autoriteetseks allikaks. Kriitilise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta võimalike arusaamatuste või valesti tõlgenduste eest, mis võivad tuleneda selle tõlke kasutamisest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->