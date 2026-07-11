# Moodul 9 - Kokkuvõte & Järgmised sammud

⏱️ ~5 min

**Palju õnne!** Olete loonud, testinud ja (kui kasutasite A-rada) juurutanud mitme agendi töövoo, kasutades Microsoft Foundry ja Foundry Toolkit VS Code jaoks.

---

## Mida te ehitasite

**CV → Töö sobivuse hindaja** - mitme agendi majutatud töövoog, mis:
- Võtab vastu CV + töö kirjelduse HTTP kaudu (`POST /responses`)
- Käitab nelja spetsialiseerunud agenti järjestikusest torujuhtmes - iga agent edastab andmed oma järglasele
- Tagastab sobivusskoori (0–100 koos jaotusega), oskuste ja sertifikaatide puudujääkide nimekirja ning isikupärastatud õppekava, millel on iga puudujäägi kohta ametlikud Microsoft Learn lingid
- Kutsub Microsoft Learn MCP serverit (`https://learn.microsoft.com/api/mcp`), et hankida iga tuvastatud oskuse puudujäägi ametlikke õppematerjale
- Käib kui üksik konteineris majutatud agent Microsoft Foundry Agent Service'is

---

## Põhikontseptsioonid, mida õppisite

| Kontseptsioon | Mida harjutasite |
|---------|-------------------|
| **Mitme agendi orkestreerimine** | `WorkflowBuilder` järjestikus torujuhtmes koos `add_edge()` |
| **Agendi spetsialiseerumine** | Neli fookustatud agenti annavad ühe üldotstarbelise agendiga võrreldes parema tulemuse |
| **Sisu marsruuteri muster** | ResumeParser toimib ka marsruuterina - säilitab töö kirjelduse teksti jaotises `[JOB DESCRIPTION PASS-THROUGH]`, et allpool olevad agendid saaksid sellele juurde pääseda (vajalik, kuna `context_mode="last_agent"` tähendab, et ainult `start_executor` näeb kasutaja sõnumi toorelt) |
| **Sisu edastamise muster** | JD Agent edastab `[PARSED RESUME PASS-THROUGH]` edasi, nii et MatchingAgent saab mõlema profiili; väldib OR-semantikaga topeltkäivitust, mille põhjustavad fan-in graafid |
| **MCP tööriista integreerimine** | `@tool` + `streamable_http_client`, mis kutsub välise MCP serveri |
| **Majutatud agendi elutsükkel** | Raamistiku loomine → Konfigureerimine → Kohalik testimine → Juurutamine → Kinnitus pilves |
| **`context_mode="last_agent"`** | Iga käitaja näeb ainult oma otsest eelkäijat väljundit |
| **Foundry Toolkit töövoog** | Raamistiku viisard, Agent Inspector, töövoo visualiseerija, ühe klõpsuga juurutus |

---

## Mida lõpetasite

<details open>
<summary><strong>🅰️ A-rada - Foundry tellimus</strong></summary>

- [x] Kontrollis Lab 01 seadistust: projekt, mudel ja RBAC on endiselt aktiivsed
- [x] Raamistikult mootoriga mitme agendi projekti töövoo mallega
- [x] Kirjutas neli agendi juhiste komplekti (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integreeris Microsoft Learn MCP tööriista koos `streamable_http_client`-iga
- [x] Ühendatud töövoograaf `WorkflowBuilder`-iga (järjestikune torujuhe koos sisu edastusega)
- [x] Testitud kohapeal 3 suitsutestiga (Agent Inspector) - sobivusskoor, puudujääkide kaardid ja MCP URLid
- [x] Juurutatud Foundry Agent Service'i (konteineriseeritud, haldusidentiteet)
- [x] Kontrollitud pilve mänguväljakul - struktuurne vastavus kohalikele tulemustele

</details>

<details open>
<summary><strong>🅱️ B-rada - Foundry kohalik</strong></summary>

- [x] Kontrollis Lab 01 seadistust: Foundry Local töötab kohalikuga mudeliga
- [x] Raamistiku mitme agendi projekti töövoo malli järgi
- [x] Kirjutas neli agendi juhist ja ühendas töövoograafiga
- [x] Integreeris Microsoft Learn MCP tööriista
- [x] Testis kohapeal 3 suitsutestiga
- [x] Kinnitas mitme agendi käitumise ilma pilve ressurssideta

</details>

---

## Järgmised sammud

### Jätka õppimist

| Ressurss | Kirjeldus |
|----------|-------------|
| **[Agent Framework SDK viide](https://learn.microsoft.com/agent-framework/)** | API dokumentatsioon `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` kohta |
| **[MCP tööriistakataloog](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Ühenda agendid teiste MCP serveritega (Bing, GitHub, kohandatud) |
| **[Lisa teadmisi (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Kanna agendid dokumentide, vektorite poodide või Bing otsinguga seotud teadmistega sisse |
| **[Foundry hindamised](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mõõda agentide kvaliteeti automaatsete hindajate abil suures mahus |
| **[Microsoft Foundry dokumentatsioon](https://learn.microsoft.com/azure/foundry/)** | Täielik platvormi viide |
| **[Foundry Toolkit - Mis on uut](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Laienduse väljalasete märkmed ja muudatuste logi |

### Ideid töövoo laiendamiseks

- **Lisa 5. agent** - Intervjuu treener, kes genereerib tõenäolisi intervjuu küsimusi puudujääkide aruande põhjal
- **Lisa Bing põhistamistööriist** - Luba JD Agentil otsida sarnaseid töökuulutusi, et rikastada nõudeid
- **Ühendu CV andmebaasiga** - Tõmba kandidaadi profiile andmebaasist läbi kohandatud `@tool`
- **Proovi erinevaid mudeleid** - Võrdle `gpt-4.1` ja `gpt-4.1-mini` väljundi kvaliteeti ja latentsust
- **Hinda Foundryga** - Kasuta Hindamiste funktsiooni, et anda sobivusaruannetele hinnang kuldse andmekogu vastu

### B-rada kasutajatele: uuendage pilve juurutuseks

Kui olete valmis pilve juurutamiseks:
1. Hangi Azure tellimus ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Lõpeta [Lab 01, Moodul 01](../../lab01-single-agent/docs/01-setup.md) (loo projekt, juuruta mudel, määra RBAC)
3. Uuenda oma `.env` fail Foundry projekti lõpp-punkti ja mudeli juurutuse nimega
4. Jätka [Moodul 06 - Juuruta Foundry’le](06-deploy-to-foundry.md)

---

## Ressursside puhastamine (valikuline)

Kui soovite eemaldada selle töötoa käigus loodud Azure ressursid:

### Valik 1: Kustuta ressursside grupp (eemaldab kõik)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Valik 2: Kustuta ainult majutatud agent

1. Ava [ai.azure.com](https://ai.azure.com) → oma projekt → **Build** → **Agents**.
2. Leia **PersonalCareerCopilot** → klõpsa **Delete**.

### Valik 3: Kustuta mudeli juurutus

1. Foundry küljeribal ava oma projekt → **Models**.
2. Paremklõps mudeli juurutusel → **Delete**.

> **Kulu märkus:** Majutatud agendid põhjustavad kulutusi ainult töö ajal. Kui peatad või kustutad agendi, siis kulusid ei teki. Mudeli juurutus võib põhjustada väikese tasu reservitud mahtuvuse eest - kustuta see, kui oled lõpetanud.

---

**Eelmine:** [08 - Veaotsing](08-troubleshooting.md) · **Kodu:** [Lab 02 LUGEME](../README.md) · [Töötoa avaleht](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->